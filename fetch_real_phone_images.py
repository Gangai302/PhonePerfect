"""
Comprehensive phone image fetcher for PhonePerfect.
Fetches real product images for all unique phone models in phones.js.

Strategy:
1. Amazon India search (primary - 100% hit rate for real phones)
2. GSMArena CDN direct URL (secondary - 50% hit rate)
3. Brand fallback for fake "Series XX" models

Output: image_map.json mapping "brand|model" -> image_url
Then applies the map to phones.js
"""
import urllib.request
import urllib.parse
import re
import sys
import json
import ssl
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.5',
}

# =====================================================
# IMAGE SOURCE 1: Amazon India Search
# =====================================================
def fetch_amazon_image(model_name, brand=''):
    """Search Amazon.in and extract the first product image."""
    try:
        search_term = model_name
        # Ensure brand is in the search for better accuracy
        if brand and brand.lower() not in model_name.lower():
            search_term = f'{brand} {model_name}'
        
        query = urllib.parse.quote(search_term)
        url = f'https://www.amazon.in/s?k={query}&i=electronics'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        
        # Find product images with s-image class
        images = re.findall(
            r'<img[^>]+class="s-image"[^>]+src="(https://m\.media-amazon\.com/images/I/[^"]+)"',
            html, re.IGNORECASE
        )
        
        if images:
            img_url = images[0]
            # Convert to high-res
            img_url = re.sub(r'\._[A-Z]+_[A-Z]+_\d+_\.', '._SL1500_.', img_url)
            if '._SL1500_.' not in img_url:
                img_url = re.sub(r'\._[^.]+\.jpg', '._SL1500_.jpg', img_url)
            return img_url
        
        return None
    except Exception as e:
        return None

# =====================================================
# IMAGE SOURCE 2: GSMArena CDN
# =====================================================
def fetch_gsmarena_image(model_name, brand=''):
    """Try GSMArena CDN direct URL with multiple slug variations."""
    name = model_name.strip()
    brand_lower = brand.strip().lower()
    
    # Clean model name
    name = re.sub(r'\s*\(Edition\s+\d+\)', '', name)
    name = re.sub(r'\s*\(v\d+\)', '', name)
    name = re.sub(r'\s*Special Edition.*', '', name)
    name = name.strip()
    
    def make_slug(n):
        s = n.lower()
        s = s.replace('+', '-plus')
        s = s.replace('(', '').replace(')', '')
        s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
        return s
    
    base = make_slug(name)
    
    slugs = [base]
    
    # Brand-specific variations
    if brand_lower == 'apple' and 'apple' not in base:
        slugs.insert(0, f'apple-{base}')
    if brand_lower == 'samsung' and 'samsung' not in base:
        slugs.insert(0, f'samsung-{base}')
    if brand_lower == 'google' and 'google' not in base:
        slugs.insert(0, f'google-{base}')
    if brand_lower == 'xiaomi' and 'xiaomi' not in base:
        slugs.insert(0, f'xiaomi-{base}')
    if brand_lower in ('redmi', 'poco') and 'xiaomi' not in base:
        slugs.insert(0, f'xiaomi-{base}')
    
    # With/without 5G
    for s in list(slugs):
        if s.endswith('-5g'):
            slugs.append(s[:-3])
        else:
            slugs.append(f'{s}-5g')
    
    # Deduplicate while preserving order
    seen = set()
    unique_slugs = []
    for s in slugs:
        if s not in seen:
            seen.add(s)
            unique_slugs.append(s)
    
    for slug in unique_slugs:
        url = f'https://fdn2.gsmarena.com/vv/bigpic/{slug}.jpg'
        try:
            req = urllib.request.Request(url, method='HEAD', headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
                if resp.status == 200:
                    ct = resp.headers.get('Content-Type', '')
                    cl = resp.headers.get('Content-Length', '0')
                    if 'image' in ct and int(cl) > 1000:
                        return url
        except:
            pass
    
    return None


# =====================================================
# LOAD PHONES DATABASE
# =====================================================
def load_phones():
    with open('phones.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    start = content.index('var PHONES = [') + len('var PHONES = ')
    depth = 0
    for i in range(start, len(content)):
        if content[i] == '[': depth += 1
        elif content[i] == ']':
            depth -= 1
            if depth == 0:
                end_idx = i + 1
                break
    
    phones = json.loads(content[start:end_idx])
    return phones, content, start, end_idx


def get_base_model(name):
    """Strip Edition/version suffixes to get base model name."""
    clean = re.sub(r'\s*\(Edition\s+\d+\)', '', name)
    clean = re.sub(r'\s*\(v\d+\)', '', clean)
    clean = clean.strip()
    return clean


def is_fake_model(name):
    """Check if model is a generated/fake 'Series XX' name."""
    return bool(re.search(r'Series \d+', name))


# =====================================================
# MAIN EXECUTION
# =====================================================
def main():
    phones, content, arr_start, arr_end = load_phones()
    print(f'Loaded {len(phones)} phones')
    
    # Get unique base models
    models = {}
    for p in phones:
        name = p.get('name', '')
        brand = p.get('brand', '')
        base = get_base_model(name)
        key = f'{brand}|{base}'
        if key not in models:
            models[key] = {'brand': brand, 'name': base, 'fake': is_fake_model(name)}
    
    real_models = {k: v for k, v in models.items() if not v['fake']}
    fake_models = {k: v for k, v in models.items() if v['fake']}
    print(f'Unique models: {len(models)} ({len(real_models)} real, {len(fake_models)} fake)')
    
    # Load existing image map if present
    image_map = {}
    map_file = 'image_map.json'
    if os.path.exists(map_file):
        with open(map_file, 'r', encoding='utf-8') as f:
            image_map = json.load(f)
        print(f'Loaded {len(image_map)} existing mappings')
    
    # Fetch images for real models that don't have mappings yet
    to_fetch = {k: v for k, v in real_models.items() if k not in image_map}
    print(f'Need to fetch: {len(to_fetch)} models')
    
    if to_fetch:
        fetched = 0
        failed = 0
        total = len(to_fetch)
        
        for i, (key, info) in enumerate(to_fetch.items()):
            brand = info['brand']
            name = info['name']
            
            # Try Amazon first
            img = fetch_amazon_image(name, brand)
            source = 'amazon'
            
            # Try GSMArena if Amazon fails
            if not img:
                img = fetch_gsmarena_image(name, brand)
                source = 'gsmarena'
            
            if img:
                image_map[key] = img
                fetched += 1
                print(f'[{i+1}/{total}] OK ({source}): {brand} {name}')
            else:
                failed += 1
                print(f'[{i+1}/{total}] FAIL: {brand} {name}')
            
            # Save progress every 50 phones
            if (i + 1) % 50 == 0:
                with open(map_file, 'w', encoding='utf-8') as f:
                    json.dump(image_map, f, indent=2)
                print(f'  -- Saved progress: {fetched} fetched, {failed} failed --')
            
            # Rate limiting
            time.sleep(2.5)
        
        # Final save
        with open(map_file, 'w', encoding='utf-8') as f:
            json.dump(image_map, f, indent=2)
        print(f'\nFetch complete: {fetched} success, {failed} failed')
    
    # For fake models, use the brand's flagship image
    brand_flagship = {}
    for key, url in image_map.items():
        brand = key.split('|')[0]
        if brand not in brand_flagship:
            brand_flagship[brand] = url
    
    for key, info in fake_models.items():
        if key not in image_map:
            brand = info['brand']
            if brand in brand_flagship:
                image_map[key] = brand_flagship[brand]
    
    # Save final map
    with open(map_file, 'w', encoding='utf-8') as f:
        json.dump(image_map, f, indent=2)
    
    print(f'\nTotal image mappings: {len(image_map)}')
    print(f'Coverage: {len(image_map)}/{len(models)} ({100*len(image_map)//len(models)}%)')
    
    # Apply to phones.js
    apply_images(phones, image_map, content, arr_start, arr_end)


def apply_images(phones, image_map, content, arr_start, arr_end):
    """Apply image mappings back to phones.js"""
    updated = 0
    for p in phones:
        name = p.get('name', '')
        brand = p.get('brand', '')
        base = get_base_model(name)
        key = f'{brand}|{base}'
        
        if key in image_map:
            new_img = image_map[key]
            if p.get('image') != new_img:
                p['image'] = new_img
                if 'images' in p:
                    p['images'] = [new_img]
                updated += 1
    
    print(f'\nUpdated {updated} phone image fields')
    
    if updated > 0:
        # Rebuild phones.js
        before = content[:arr_start]
        after = content[arr_end:]
        
        phones_json = json.dumps(phones, indent=2, ensure_ascii=False)
        
        new_content = before + phones_json + after
        
        with open('phones.js', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f'Written updated phones.js ({len(new_content)} bytes)')
        
        # Verify
        unique_imgs = set()
        for p in phones:
            img = p.get('image', '')
            if img:
                unique_imgs.add(img)
        print(f'Unique images after update: {len(unique_imgs)}')


if __name__ == '__main__':
    main()
