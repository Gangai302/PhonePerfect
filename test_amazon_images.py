"""
Test fetching real phone images using Amazon India search.
Amazon product images can be fetched reliably using their search API.
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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-IN,en;q=0.5',
}

def search_amazon_india(model_name):
    """Search Amazon.in for a phone and extract product image."""
    try:
        query = urllib.parse.quote(f'{model_name}')
        url = f'https://www.amazon.in/s?k={query}&i=electronics'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        
        # Find product images - Amazon uses specific image patterns
        # Pattern 1: s-image class on search results
        images = re.findall(
            r'<img[^>]+class="s-image"[^>]+src="(https://m\.media-amazon\.com/images/I/[^"]+)"',
            html, re.IGNORECASE
        )
        
        if not images:
            # Pattern 2: any amazon media image
            images = re.findall(
                r'src="(https://m\.media-amazon\.com/images/I/[^"]+\._[^"]*\.jpg)"',
                html, re.IGNORECASE
            )
        
        if images:
            # Get the first product image and make it high-res
            img_url = images[0]
            # Convert to high-res: replace ._AC_UY218_.jpg with ._SL1500_.jpg
            img_url = re.sub(r'\._[A-Z]+_[A-Z]+_\d+_\.', '._SL1500_.', img_url)
            # If no such pattern, try simpler replacement
            if '._SL1500_.' not in img_url:
                img_url = re.sub(r'\._[^.]+\.jpg', '._SL1500_.jpg', img_url)
            return img_url, len(images)
        
        # Also extract ASINs for reference
        asins = re.findall(r'data-asin="([A-Z0-9]{10})"', html)
        return None, len(asins)
        
    except Exception as e:
        return None, str(e)

def get_amazon_image_by_asin(asin):
    """Try to get an Amazon product image directly from ASIN."""
    try:
        url = f'https://www.amazon.in/dp/{asin}'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        
        # Find main product image
        images = re.findall(
            r'"hiRes":"(https://m\.media-amazon\.com/images/I/[^"]+)"',
            html
        )
        if not images:
            images = re.findall(
                r'"large":"(https://m\.media-amazon\.com/images/I/[^"]+)"',
                html
            )
        if not images:
            images = re.findall(
                r'id="landingImage"[^>]+src="(https://m\.media-amazon\.com/images/I/[^"]+)"',
                html
            )
        
        if images:
            return images[0]
        return None
    except Exception as e:
        return None

# Known real ASINs for verification
known_asins = {
    'Samsung Galaxy S24 Ultra': 'B0CS5XBCCM',
    'iPhone 16 Pro Max': 'B0DGHWMHD8', 
    'OnePlus 12': 'B0CX23V2ZK',
    'Redmi Note 13 Pro+': 'B0CR4JF77N',
    'Nothing Phone (2a)': 'B0CXD3M8JG',
    'Google Pixel 9': 'B0D7G68TYG',
}

test_models = [
    'Samsung Galaxy S24 Ultra',
    'iPhone 16 Pro Max',
    'OnePlus 12',
    'Nothing Phone (2a)',
    'Google Pixel 9',
    'Redmi Note 13 Pro+',
    'Poco F6',
    'Lava Blaze 3 5G',
]

print("=== Test 1: Amazon Search ===\n")
for model in test_models:
    img, count = search_amazon_india(model)
    status = 'OK' if img else 'FAIL'
    print(f'[{status}] {model}: {img[:80] if img else f"No images (info: {count})"}')
    time.sleep(2)

print("\n=== Test 2: Amazon ASIN Direct ===\n")
for model, asin in known_asins.items():
    img = get_amazon_image_by_asin(asin)
    status = 'OK' if img else 'FAIL'
    print(f'[{status}] {model} ({asin}): {img[:80] if img else "No image found"}')
    time.sleep(2)
