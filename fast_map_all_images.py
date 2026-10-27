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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.9',
}

def clean_model_name(name):
    clean = re.sub(r'\s*\(Edition\s+\d+\)', '', name)
    clean = re.sub(r'\s*\(v\d+\)', '', clean)
    clean = re.sub(r'\s*Special Edition.*', '', clean, flags=re.IGNORECASE)
    clean = clean.strip()
    return clean

def fetch_gsmarena_image(model_name, brand=''):
    name = clean_model_name(model_name)
    brand_lower = brand.strip().lower()

    def make_slug(n):
        s = n.lower()
        s = s.replace('+', '-plus')
        s = s.replace('(', '').replace(')', '')
        s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
        return s
    
    base = make_slug(name)
    slugs = [base]
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
    if brand_lower == 'vivo' and 'vivo' not in base:
        slugs.insert(0, f'vivo-{base}')
    if brand_lower == 'motorola' and 'motorola' not in base:
        slugs.insert(0, f'motorola-{base}')
    if brand_lower == 'oneplus' and 'oneplus' not in base:
        slugs.insert(0, f'oneplus-{base}')
    if brand_lower == 'realme' and 'realme' not in base:
        slugs.insert(0, f'realme-{base}')
    if brand_lower == 'iqoo' and 'iqoo' not in base:
        slugs.insert(0, f'iqoo-{base}')
    if brand_lower == 'nothing' and 'nothing' not in base:
        slugs.insert(0, f'nothing-{base}')
    
    for s in list(slugs):
        if s.endswith('-5g'):
            slugs.append(s[:-3])
        else:
            slugs.append(f'{s}-5g')
    
    seen = set()
    unique_slugs = [s for s in slugs if not (s in seen or seen.add(s))]

    for slug in unique_slugs:
        url = f'https://fdn2.gsmarena.com/vv/bigpic/{slug}.jpg'
        try:
            req = urllib.request.Request(url, method='HEAD', headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=4) as resp:
                if resp.status == 200:
                    ct = resp.headers.get('Content-Type', '')
                    cl = int(resp.headers.get('Content-Length', '0'))
                    if 'image' in ct and cl > 1000:
                        return url
        except Exception:
            pass
    return None

def fetch_bing_image(model_name, brand=''):
    try:
        query = f"{brand} {model_name} official phone".strip()
        encoded = urllib.parse.quote(query)
        url = f"https://www.bing.com/images/search?q={encoded}&qft=+filterui:aspect-square+filterui:photo-photo&form=HDRSC2"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=6) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        
        # Look for media URLs murl in Bing image search
        matches = re.findall(r'murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png|webp))&quot;', html)
        if not matches:
            matches = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png|webp))&quot;', html)
        if matches:
            for m in matches[:3]:
                # Filter out suspicious or non-image cdn
                if not any(bad in m.lower() for bad in ['logo', 'icon', 'banner', 'avatar', 'vector', 'transparent']):
                    return m
        return None
    except Exception:
        return None

def fetch_amazon_image(model_name, brand=''):
    try:
        search_term = f'{brand} {model_name}'.strip()
        query = urllib.parse.quote(search_term)
        url = f'https://www.amazon.in/s?k={query}&i=electronics'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=6) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        
        images = re.findall(
            r'<img[^>]+class="s-image"[^>]+src="(https://m\.media-amazon\.com/images/I/[^"]+)"',
            html, re.IGNORECASE
        )
        if images:
            img_url = images[0]
            img_url = re.sub(r'\._[A-Z0-9_,]+_\.', '._SL1500_.', img_url)
            return img_url
        return None
    except Exception:
        return None

def get_best_image_for_model(brand, model_name):
    # Try GSMArena first (crisp high quality official renders)
    img = fetch_gsmarena_image(model_name, brand)
    if img:
        return img, 'gsmarena'
    
    # Try Bing high quality image search
    img = fetch_bing_image(model_name, brand)
    if img:
        return img, 'bing'
        
    # Try Amazon search
    img = fetch_amazon_image(model_name, brand)
    if img:
        return img, 'amazon'
        
    return None, 'none'

def process_model(item):
    brand, model_name = item
    img, src = get_best_image_for_model(brand, model_name)
    return brand, model_name, img, src

def main():
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
    
    # Build unique (brand, cleaned_name)
    model_set = set()
    for p in phones:
        b = p.get('brand', '').strip()
        n = clean_model_name(p.get('name', ''))
        model_set.add((b, n))
        
    print(f"Total unique models to resolve: {len(model_set)}")

    # Load existing cache if present
    cache = {}
    if os.path.exists('phone_images_cache.json'):
        try:
            with open('phone_images_cache.json', 'r', encoding='utf-8') as f:
                cache = json.load(f)
            print(f"Loaded {len(cache)} existing cached images.")
        except Exception:
            pass

    to_fetch = [m for m in model_set if f"{m[0]}||{m[1]}" not in cache or not cache[f"{m[0]}||{m[1]}"]]
    print(f"Remaining to fetch: {len(to_fetch)}")

    # Fetch concurrently with 8 workers
    completed_count = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_model, item): item for item in to_fetch}
        for future in as_completed(futures):
            brand, model_name, img, src = future.result()
            key = f"{brand}||{model_name}"
            if img:
                cache[key] = img
            completed_count += 1
            if completed_count % 25 == 0 or completed_count == len(to_fetch):
                print(f"Progress: {completed_count}/{len(to_fetch)} processed (Cached total: {len(cache)})")
                with open('phone_images_cache.json', 'w', encoding='utf-8') as cf:
                    json.dump(cache, cf, indent=2)

    with open('phone_images_cache.json', 'w', encoding='utf-8') as cf:
        json.dump(cache, cf, indent=2)

    # Now update phones in phones.js
    updated_count = 0
    unique_images = set()
    for p in phones:
        b = p.get('brand', '').strip()
        n = clean_model_name(p.get('name', ''))
        key = f"{b}||{n}"
        if key in cache and cache[key]:
            img_url = cache[key]
            p['image'] = img_url
            p['images'] = [img_url]
            unique_images.add(img_url)
            updated_count += 1

    print(f"Applied images to {updated_count}/{len(phones)} phone records.")
    print(f"Total unique phone images across dataset: {len(unique_images)}")

    # Write back to phones.js
    new_phones_json = json.dumps(phones, indent=2, ensure_ascii=False)
    new_content = content[:start] + new_phones_json + content[end_idx:]
    with open('phones.js', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("Successfully updated phones.js with exact phone model images!")

if __name__ == '__main__':
    main()
