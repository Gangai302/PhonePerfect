import urllib.request
import urllib.parse
import re
import html
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def inspect_bing_data(query):
    q_enc = urllib.parse.quote(query)
    url = f"https://www.bing.com/images/search?q={q_enc}&form=HDRSC2&first=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=8) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        
        # Look for m="{...}" attributes which contain individual image metadata
        # e.g. <a class="iusc" m="{&quot;cid&quot;:&quot;...&quot;,&quot;murl&quot;:&quot;...&quot;,&quot;turl&quot;:&quot;...&quot;}">
        m_matches = re.findall(r'class="iusc"[^>]*\sm="([^"]+)"', content)
        print(f"Query '{query}' found {len(m_matches)} iusc blocks")
        for i, m_raw in enumerate(m_matches[:5]):
            unescaped = html.unescape(m_raw)
            try:
                data = json.loads(unescaped)
                print(f"  Result {i+1}:")
                print(f"    murl (source): {data.get('murl')}")
                print(f"    turl (thumbnail): {data.get('turl')}")
                print(f"    title: {data.get('t')}")
            except Exception as err:
                print(f"    JSON error: {err}")

inspect_bing_data('Samsung Galaxy S24')
inspect_bing_data('Samsung Galaxy S25 Ultra')
inspect_bing_data('OnePlus 12')
