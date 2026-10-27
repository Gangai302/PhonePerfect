"""
Test improved GSMArena direct URL construction with multiple slug variants.
GSMArena bigpic URLs follow patterns like:
- samsung-galaxy-s24-ultra.jpg
- apple-iphone-16-pro-max.jpg
- google-pixel-9-pro.jpg
"""
import urllib.request
import re
import sys
import ssl
import time

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}

# Brand-specific slug rules for GSMArena
BRAND_SLUG_MAP = {
    'apple': lambda m: f'apple-{m}',
    'samsung': lambda m: m,  # Already includes "Galaxy"
    'google': lambda m: f'google-{m}',
    'xiaomi': lambda m: m,  # Xiaomi Redmi/Poco already prefixed
    'oneplus': lambda m: m,
    'realme': lambda m: m,
    'vivo': lambda m: m,
    'oppo': lambda m: m,
    'motorola': lambda m: m,
    'nothing': lambda m: m,
    'iqoo': lambda m: m,
    'poco': lambda m: m,
    'tecno': lambda m: m,
    'infinix': lambda m: m,
    'lava': lambda m: m,
}

def make_gsmarena_slug(model_name, brand=''):
    """Generate possible GSMArena slugs for a phone model."""
    name = model_name.strip()
    brand = brand.strip().lower()
    
    # Remove (Edition XX), (vXX) suffixes
    name = re.sub(r'\s*\(Edition\s+\d+\)', '', name)
    name = re.sub(r'\s*\(v\d+\)', '', name)
    name = re.sub(r'\s*Special Edition.*', '', name)
    name = name.strip()
    
    slugs = set()
    
    # Base slug: lowercase, spaces to hyphens, remove special chars
    base = name.lower()
    base = base.replace('+', '-plus')
    base = base.replace('(', '').replace(')', '')
    base = re.sub(r'[^a-z0-9]+', '-', base).strip('-')
    slugs.add(base)
    
    # With brand prefix if not already there
    if brand and not base.startswith(brand):
        slugs.add(f'{brand}-{base}')
    
    # Samsung specific: "Galaxy S24 Ultra" -> "samsung-galaxy-s24-ultra"
    if brand == 'samsung' and 'samsung' not in base:
        slugs.add(f'samsung-{base}')
    
    # Google specific: "Pixel 9 Pro" -> "google-pixel-9-pro"
    if brand == 'google' and 'google' not in base:
        slugs.add(f'google-{base}')
    
    # Apple specific: "iPhone 16 Pro Max" -> "apple-iphone-16-pro-max"
    if brand == 'apple' and 'apple' not in base:
        slugs.add(f'apple-{base}')
    
    # Xiaomi/Redmi: "Redmi Note 14 Pro" -> "xiaomi-redmi-note-14-pro"
    if brand == 'xiaomi' and 'xiaomi' not in base:
        slugs.add(f'xiaomi-{base}')
    
    # Try without "5g" suffix
    for s in list(slugs):
        if s.endswith('-5g'):
            slugs.add(s[:-3])
    
    # Try with "5g" suffix  
    for s in list(slugs):
        if not s.endswith('-5g'):
            slugs.add(f'{s}-5g')
    
    return list(slugs)

def check_gsmarena_image(slug):
    """Check if a GSMArena bigpic URL exists."""
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

test_phones = [
    ('Samsung Galaxy S24 Ultra', 'Samsung'),
    ('Samsung Galaxy S24', 'Samsung'),
    ('Samsung Galaxy A55', 'Samsung'),
    ('iPhone 16 Pro Max', 'Apple'),
    ('iPhone 16', 'Apple'),
    ('iPhone 15 Pro', 'Apple'),
    ('OnePlus 12', 'OnePlus'),
    ('OnePlus Nord 4', 'OnePlus'),
    ('Xiaomi 14', 'Xiaomi'),
    ('Xiaomi 14 Ultra', 'Xiaomi'),
    ('Redmi Note 14 Pro 5G', 'Xiaomi'),
    ('Redmi Note 13 Pro+', 'Xiaomi'),
    ('Nothing Phone (2a)', 'Nothing'),
    ('Nothing Phone (1)', 'Nothing'),
    ('Google Pixel 9 Pro', 'Google'),
    ('Google Pixel 9', 'Google'),
    ('Poco F6', 'Poco'),
    ('Poco X6 Pro', 'Poco'),
    ('Motorola Edge 50 Pro', 'Motorola'),
    ('Motorola Moto G45 5G', 'Motorola'),
    ('Vivo X200 Pro', 'Vivo'),
    ('Vivo V40', 'Vivo'),
    ('iQOO Neo 9 Pro', 'iQOO'),
    ('iQOO Z9s Pro', 'iQOO'),
    ('Realme GT 6', 'Realme'),
    ('Realme 13 Pro+', 'Realme'),
    ('Oppo Reno 12 Pro', 'Oppo'),
    ('Tecno Phantom V Flip 2', 'Tecno'),
    ('Infinix Note 40 Pro', 'Infinix'),
    ('Lava Blaze 3 5G', 'Lava'),
]

print(f"Testing GSMArena slug-based image fetch for {len(test_phones)} models:\n")

success = 0
fail = 0
for model, brand in test_phones:
    slugs = make_gsmarena_slug(model, brand)
    found = None
    tried = []
    for slug in slugs:
        img = check_gsmarena_image(slug)
        tried.append(slug)
        if img:
            found = img
            break
        time.sleep(0.3)
    
    if found:
        success += 1
        print(f'[OK]   {model} -> {found}')
    else:
        fail += 1
        print(f'[FAIL] {model}')
        print(f'       Tried: {", ".join(tried[:5])}')

print(f'\nResults: {success}/{len(test_phones)} success, {fail} failed')
