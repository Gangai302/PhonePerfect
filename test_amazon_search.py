import urllib.request
import urllib.parse
import re
import html
import sys

sys.stdout.reconfigure(encoding='utf-8')

def get_amazon_image(query):
    q_enc = urllib.parse.quote(query)
    url = f"https://www.amazon.in/s?k={q_enc}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            # Look for product images: https://m.media-amazon.com/images/I/...
            # Usually inside class="s-image"
            imgs = re.findall(r'<img\s+[^>]*class="[^"]*s-image[^"]*"[^>]*src="(https://m\.media-amazon\.com/images/I/[^"]+)"', content)
            if not imgs:
                imgs = re.findall(r'src="(https://m\.media-amazon\.com/images/I/[A-Za-z0-9+%-]+\._[A-Za-z0-9_+,-]+_\.jpg)"', content)
            if imgs:
                return imgs[0]
    except Exception as e:
        print(f"Error Amazon for {query}: {e}")
    return None

test_phones = [
    'OnePlus 12 5G smartphone',
    'Samsung Galaxy S24 5G smartphone',
    'iQOO Neo 9 Pro 5G smartphone',
    'Xiaomi 14 Civi smartphone',
    'Google Pixel 9 smartphone',
    'Nothing Phone 2a smartphone',
    'Motorola Edge 50 Pro smartphone',
    'Realme GT 6 smartphone',
    'Vivo V40 Pro smartphone',
    'Poco F6 5G smartphone'
]

for p in test_phones:
    img = get_amazon_image(p)
    print(f"Amazon: {p:35} => {img}")
