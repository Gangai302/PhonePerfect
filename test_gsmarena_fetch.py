"""
Fetch real phone images for each unique base model using GSMArena's phone database.
GSMArena stores images at predictable CDN URLs based on phone slug.

Strategy:
1. Search GSMArena for each phone model name
2. Extract the phone's page URL from search results
3. Extract the main product image from the phone's page
4. Map back to phones.js and update all entries for that base model
"""
import urllib.request
import urllib.parse
import re
import sys
import time
import json
import ssl

sys.stdout.reconfigure(encoding='utf-8')

# Bypass SSL issues on Windows
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

def search_gsmarena(model_name):
    """Search GSMArena and return (phone_page_url, image_url) tuple."""
    try:
        query = urllib.parse.quote(model_name)
        url = f'https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName={query}'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        
        # Find phone links and images in results
        # Pattern: <a href="samsung_galaxy_s24-12345.php"><img src="..." ...>
        matches = re.findall(
            r'<a\s+href="([^"]+\.php)"[^>]*>\s*<img\s+src="(https?://[^"]+)"',
            html, re.IGNORECASE
        )
        
        if matches:
            page_url, thumb_url = matches[0]
            # Convert thumbnail to full-size image
            # GSMArena thumbnails: https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24.jpg
            # or: https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s24.jpg
            return f'https://www.gsmarena.com/{page_url}', thumb_url
        
        return None, None
    except Exception as e:
        return None, str(e)

def get_phone_detail_image(page_url):
    """Fetch the main product image from a GSMArena phone detail page."""
    try:
        req = urllib.request.Request(page_url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        
        # Find the main phone image in specs-photo-main
        match = re.search(
            r'class="specs-photo-main"[^>]*>\s*(?:<a[^>]*>)?\s*<img\s+src="(https?://[^"]+)"',
            html, re.IGNORECASE
        )
        if match:
            return match.group(1)
        
        # Fallback: any big image in the phone-display area
        match = re.search(
            r'<div[^>]*class="[^"]*phone-display[^"]*"[^>]*>.*?<img\s+src="(https?://[^"]+)"',
            html, re.IGNORECASE | re.DOTALL
        )
        if match:
            return match.group(1)
        
        return None
    except Exception as e:
        return None

# Test with a few phone models
test_models = [
    'Samsung Galaxy S24 Ultra',
    'iPhone 16 Pro Max',
    'OnePlus 12',
    'Xiaomi 14',
    'Redmi Note 14 Pro',
    'Motorola Edge 50 Pro',
    'Nothing Phone (2a)',
    'Realme GT 6',
    'Google Pixel 9 Pro',
    'iQOO Neo 9 Pro',
    'Vivo X200 Pro',
    'Poco F6',
    'Oppo Reno 12 Pro',
    'Tecno Phantom V Flip 2',
    'Lava Blaze 3 5G',
]

print("Testing GSMArena image fetch for 15 models:\n")
results = {}
for model in test_models:
    page_url, thumb_url = search_gsmarena(model)
    detail_img = None
    if page_url and page_url.startswith('http'):
        time.sleep(1)  # Be respectful
        detail_img = get_phone_detail_image(page_url)
    
    final_img = detail_img or thumb_url
    results[model] = final_img
    status = 'OK' if final_img and final_img.startswith('http') else 'FAIL'
    print(f'[{status}] {model}')
    if final_img and final_img.startswith('http'):
        print(f'       {final_img}')
    else:
        print(f'       Error: {thumb_url}')
    
    time.sleep(2)  # Rate limiting

print(f'\nSuccess: {sum(1 for v in results.values() if v and v.startswith("http"))}/{len(test_models)}')
