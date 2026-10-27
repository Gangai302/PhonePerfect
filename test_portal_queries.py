import urllib.request
import urllib.parse
import re
import html
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_query_sources(brand, model):
    queries = [
        f"{brand} {model} 91mobiles",
        f"{brand} {model} gadgets360",
        f"{brand} {model} smartprix",
        f"{brand} {model} amazon.in"
    ]
    print(f"=== Testing {brand} {model} ===")
    for q in queries:
        q_enc = urllib.parse.quote(q)
        url = f"https://www.bing.com/images/search?q={q_enc}&form=HDRSC2&first=1"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
                m_matches = re.findall(r'class="iusc"[^>]*\sm="([^"]+)"', content)
                for m_raw in m_matches[:2]:
                    data = json.loads(html.unescape(m_raw))
                    turl = data.get('turl')
                    title = data.get('t')
                    if '/th?id=OIP.' in turl or '/th/id/OIP.' in turl:
                        print(f"  [{q[:30]}] -> {title[:40]} | {turl}")
        except Exception as e:
            print(f"  Error: {e}")

test_query_sources('Samsung', 'Galaxy S24')
test_query_sources('Samsung', 'Galaxy S25 Ultra')
test_query_sources('Samsung', 'Galaxy S24 Ultra')
test_query_sources('OnePlus', '12')
test_query_sources('iQOO', 'Neo 9 Pro')
test_query_sources('Xiaomi', '14 Civi')
