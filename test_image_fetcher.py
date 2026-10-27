import urllib.request
import urllib.parse
import re
import html
import sys

sys.stdout.reconfigure(encoding='utf-8')

def get_exact_phone_image(brand, phone_name):
    # Strip edition numbers, versions, etc.
    clean_name = re.sub(r'\s*\((Edition|v|Edition \d+|v\d+|\d{4})\s*\d*\)', '', phone_name, flags=re.IGNORECASE)
    clean_name = re.sub(r'\s*\(Edition\s*\d+\)', '', clean_name, flags=re.IGNORECASE)
    clean_name = re.sub(r'\s*\(v\d+\)', '', clean_name, flags=re.IGNORECASE)
    
    # If brand not already in name
    if brand.lower() not in clean_name.lower():
        full_query = f"{brand} {clean_name}"
    else:
        full_query = clean_name

    query = f"{full_query} smartphone official product render white background"
    q_enc = urllib.parse.quote(query)
    url = f"https://www.bing.com/images/search?q={q_enc}&form=HDRSC2&first=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            # Extract mimg src or murl
            # murl is high resolution direct image URL: {"murl":"https://..."}
            murls = re.findall(r'murl&quot;:&quot;(https?://[^&]+)&quot;', content)
            if not murls:
                murls = re.findall(r'"murl":"(https?://[^"]+)"', content)
            
            # Also get thumbnail fallback
            tse_urls = re.findall(r'src="(https://tse\d+\.mm\.bing\.net/th/id/[^"]+)"', content)
            
            # Prefer tse thumbnail as it is ultra-fast, permanently cached by Microsoft CDN, and won't 403 / break!
            if tse_urls:
                clean_url = html.unescape(tse_urls[0])
                return clean_url
            elif murls:
                clean_url = html.unescape(murls[0])
                return clean_url
    except Exception as e:
        print(f"Error fetching for {full_query}: {e}")
        return None
    return None

test_cases = [
    ('OnePlus', 'OnePlus 12'),
    ('Samsung', 'Galaxy S24'),
    ('iQOO', 'iQOO Neo 9 Pro'),
    ('Xiaomi', 'Xiaomi 14 Civi'),
    ('Google', 'Google Pixel 9'),
    ('Nothing', 'Nothing Phone (2a)'),
    ('Motorola', 'Motorola Moto G85'),
    ('Realme', 'Realme GT 6'),
    ('Vivo', 'Vivo T3 Ultra'),
    ('Apple', 'iPhone 15 Pro')
]

for brand, name in test_cases:
    img = get_exact_phone_image(brand, name)
    print(f"[{brand}] {name} => {img}")
