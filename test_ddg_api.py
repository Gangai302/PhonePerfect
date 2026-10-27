import urllib.request
import urllib.parse
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def get_ddg_images(query):
    # Step 1: get vqd token
    url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            vqd_match = re.search(r'vqd=([\d-]+)', html) or re.search(r'vqd="([^"]+)"', html)
            if not vqd_match:
                return []
            vqd = vqd_match.group(1)

        # Step 2: fetch images
        img_url = f"https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(query)}&vqd={vqd}&f=,,,&p=1"
        req2 = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(req2, timeout=5) as resp2:
            data = json.loads(resp2.read().decode('utf-8'))
            results = data.get('results', [])
            return [r.get('image') for r in results if r.get('image')]
    except Exception as e:
        print(f"Error for {query}: {e}")
        return []

phones = [
    'OnePlus 12',
    'Samsung Galaxy S24',
    'iQOO Neo 9 Pro',
    'Xiaomi 14 Civi',
    'Google Pixel 9'
]

for p in phones:
    imgs = get_ddg_images(f"{p} smartphone official")
    print(f"DDG: {p} => {imgs[:2] if imgs else 'None'}")
