import urllib.request
import urllib.parse
import re
import html
import sys
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

def fetch_model_image(model_name):
    query = f"{model_name} smartphone official product render"
    q_enc = urllib.parse.quote(query)
    url = f"https://www.bing.com/images/search?q={q_enc}&form=HDRSC2&first=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            # Extract tse thumbnail url
            tse_urls = re.findall(r'src="(https://tse\d+\.mm\.bing\.net/th/id/[^"]+)"', content)
            if tse_urls:
                # remove &amp; encoding
                clean_url = html.unescape(tse_urls[0])
                return model_name, clean_url
    except Exception as e:
        pass
    return model_name, None

test_sample = [
    'OnePlus 12',
    'Samsung Galaxy S24',
    'iQOO Neo 9 Pro',
    'Xiaomi 14 Civi',
    'Google Pixel 9 Pro',
    'Motorola Edge 50 Fusion',
    'Nothing Phone (2a)',
    'Realme GT 6T',
    'Vivo V40 Pro',
    'Poco F6 5G',
    'Lava Agni 3 5G',
    'Infinix Note 40 Pro',
    'Tecno Phantom V Flip 2',
    'Apple iPhone 16 Pro Max',
    'Samsung Galaxy Z Flip 6',
    'OnePlus Nord 4',
    'Xiaomi Redmi Note 13 Pro+',
    'Vivo X100 Pro',
    'Motorola Moto G85',
    'Samsung Galaxy S25 Ultra'
]

start_t = time.time()
results = {}
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_model_image, m) for m in test_sample]
    for fut in as_completed(futures):
        m_name, img_url = fut.result()
        results[m_name] = img_url

elapsed = time.time() - start_t
print(f"Fetched {len(results)} models in {elapsed:.2f}s:")
for m, u in results.items():
    print(f"  {m} => {u}")
