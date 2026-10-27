import urllib.request
import urllib.parse
import re
import html
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def get_yahoo_images(query):
    q_enc = urllib.parse.quote(query)
    url = f"https://images.search.yahoo.com/search/images?p={q_enc}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            # Look for image URLs in JSON or img tags
            # Yahoo embeds: data-src="https://..." or src="https://tse..." or {"iurl":"..."}
            iurls = re.findall(r'"iurl":"(https?://[^"]+)"', content)
            turls = re.findall(r'src="(https://tse\d+\.mm\.bing\.net/th/id/[^"]+)"', content)
            if iurls:
                return [html.unescape(u) for u in iurls[:3]]
            if turls:
                return [html.unescape(u) for u in turls[:3]]
    except Exception as e:
        print(f"Error Yahoo for {query}: {e}")
    return []

test_phones = [
    'OnePlus 12 smartphone official render',
    'Samsung Galaxy S24 smartphone official render',
    'Samsung Galaxy S25 Ultra smartphone official render',
    'iQOO Neo 9 Pro smartphone official render',
    'Xiaomi 14 Civi smartphone official render',
    'Google Pixel 9 smartphone official render',
    'Nothing Phone 2a smartphone official render',
    'Motorola Edge 50 Pro smartphone official render',
    'Realme GT 6 smartphone official render',
    'Vivo V40 Pro smartphone official render',
    'Poco F6 smartphone official render'
]

for p in test_phones:
    imgs = get_yahoo_images(p)
    print(f"Yahoo: {p[:30]} => {imgs[0] if imgs else 'None'}")
