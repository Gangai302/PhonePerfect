"""
Test multiple image sources for phone product images.
Try Amazon image from ASIN, DuckDuckGo Instant Answer, and other sources.
"""
import urllib.request
import urllib.parse
import re
import sys
import json
import ssl
import time

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

def try_duckduckgo_instant(model_name):
    """Use DDG Instant Answer API to find phone image."""
    try:
        query = urllib.parse.quote(f'{model_name} smartphone')
        url = f'https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1&skip_disambig=1'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        
        # Check Image field
        img = data.get('Image', '')
        if img and img.startswith('http'):
            return img, 'instant_answer'
        
        # Check RelatedTopics for image
        for topic in data.get('RelatedTopics', []):
            icon = topic.get('Icon', {}).get('URL', '')
            if icon and icon.startswith('http'):
                return icon, 'related_topic'
        
        return None, None
    except Exception as e:
        return None, str(e)

def try_gsmarena_direct_url(model_name):
    """Try constructing GSMArena image URL directly from model name."""
    # GSMArena CDN pattern: https://fdn2.gsmarena.com/vv/bigpic/brand-model-name.jpg
    slug = model_name.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    
    urls = [
        f'https://fdn2.gsmarena.com/vv/bigpic/{slug}.jpg',
        f'https://fdn.gsmarena.com/imgroot/phone/bigpic/{slug}.jpg',
    ]
    
    for url in urls:
        try:
            req = urllib.request.Request(url, method='HEAD', headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=5) as resp:
                if resp.status == 200:
                    return url, 'gsmarena_direct'
        except:
            pass
    
    return None, None

def try_wikipedia_image(model_name):
    """Use Wikipedia API to find phone image."""
    try:
        query = urllib.parse.quote(model_name)
        url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&titles={query}&pithumbsize=500'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        
        pages = data.get('query', {}).get('pages', {})
        for page in pages.values():
            thumb = page.get('thumbnail', {}).get('source', '')
            if thumb:
                return thumb, 'wikipedia'
        
        return None, None
    except Exception as e:
        return None, str(e)

def try_phonearena_image(model_name):
    """Try PhoneArena search."""
    try:
        query = urllib.parse.quote(model_name)
        url = f'https://www.phonearena.com/phones?s={query}'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        
        # Find phone images
        match = re.search(r'<img[^>]+src="(https?://[^"]*phonearena[^"]*phone[^"]*\.(jpg|png|webp))"', html, re.IGNORECASE)
        if match:
            return match.group(1), 'phonearena'
        
        return None, None
    except Exception as e:
        return None, str(e)

def try_kimovil_image(model_name):
    """Try Kimovil/GSMChoice search."""
    try:
        slug = model_name.lower().replace(' ', '-')
        url = f'https://www.kimovil.com/en/where-to-buy-{slug}'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        
        match = re.search(r'<img[^>]+src="(https?://[^"]+)"[^>]*class="[^"]*phone[^"]*"', html, re.IGNORECASE)
        if match:
            return match.group(1), 'kimovil'
        
        return None, None
    except Exception as e:
        return None, str(e)


test_models = [
    'Samsung Galaxy S24 Ultra',
    'iPhone 16 Pro Max', 
    'OnePlus 12',
    'Xiaomi 14',
    'Nothing Phone (2a)',
    'Google Pixel 9 Pro',
    'Poco F6',
    'Lava Blaze 3 5G',
]

print("Testing multiple image sources:\n")

for model in test_models:
    print(f'\n=== {model} ===')
    
    # Try DDG
    img, src = try_duckduckgo_instant(model)
    if img:
        print(f'  [DDG] {img}')
    else:
        print(f'  [DDG] FAIL: {src}')
    
    # Try Wikipedia
    img, src = try_wikipedia_image(model)
    if img:
        print(f'  [WIKI] {img}')
    else:
        print(f'  [WIKI] FAIL: {src}')
    
    # Try GSMArena direct
    img, src = try_gsmarena_direct_url(model)
    if img:
        print(f'  [GSM] {img}')
    else:
        print(f'  [GSM] FAIL: {src}')
    
    time.sleep(1)
