import urllib.request
import urllib.parse
import re
import html
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_queries(brand, model):
    queries = [
        f"{brand} {model} mobile phone official",
        f"{brand} {model} smartphone",
        f"{brand} {model} gsmarena",
        f"{brand} {model} flipkart"
    ]
    print(f"=== {brand} {model} ===")
    for q in queries:
        q_enc = urllib.parse.quote(q)
        url = f"https://www.bing.com/images/search?q={q_enc}&form=HDRSC2&first=1"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
                tse = re.findall(r'src="(https://tse\d+\.mm\.bing\.net/th/id/[^"]+)"', content)
                if tse:
                    print(f"  [{q}] => {tse[0]}")
        except Exception as e:
            print(f"  [{q}] => Error {e}")

test_queries('Samsung', 'Galaxy S24')
test_queries('Samsung', 'Galaxy S25 Ultra')
test_queries('Samsung', 'Galaxy Z Flip 6')
test_queries('OnePlus', '12')
test_queries('OnePlus', 'Nord 4')
