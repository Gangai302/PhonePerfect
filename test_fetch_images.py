import urllib.request
import urllib.parse
import re
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

test_models = [
    'Samsung Galaxy S24',
    'OnePlus 12',
    'iQOO Neo 9 Pro',
    'Xiaomi 14 Civi',
    'Motorola Edge 50 Pro',
    'Nothing Phone (2a)',
    'Realme GT 6',
    'Google Pixel 9',
    'Vivo V40 Pro',
    'Poco F6'
]

for model in test_models:
    q = urllib.parse.quote(f'{model} smartphone official white background')
    url = f'https://www.bing.com/images/search?q={q}&form=HDRSC2&first=1'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            m = re.findall(r'src="(https://tse\d+\.mm\.bing\.net/th/id/[^"]+)"', html)
            if m:
                print(f'{model} -> {m[0]}')
            else:
                print(f'{model} -> No image found')
    except Exception as e:
        print(f'{model} -> Error: {e}')
    time.sleep(0.5)
