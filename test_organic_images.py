import urllib.request
import urllib.parse
import re
import html
import sys

sys.stdout.reconfigure(encoding='utf-8')

def get_organic_images(query):
    q_enc = urllib.parse.quote(query)
    url = f"https://www.bing.com/images/search?q={q_enc}&form=HDRSC2&first=1"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            # Extract organic OIP thumbnails
            oip_urls = re.findall(r'src="(https://tse\d+\.mm\.bing\.net/th/id/OIP\.[^"]+)"', content)
            
            # Extract murl direct links
            murls = re.findall(r'murl&quot;:&quot;(https?://[^&]+)&quot;', content)
            if not murls:
                murls = re.findall(r'"murl":"(https?://[^"]+)"', content)
                
            return {
                'oip': [html.unescape(u) for u in oip_urls[:3]],
                'murl': [html.unescape(u) for u in murls[:3]]
            }
    except Exception as e:
        return {'error': str(e)}

phones_to_test = [
    'Samsung Galaxy S24',
    'Samsung Galaxy S25 Ultra',
    'Samsung Galaxy Z Flip 6',
    'Samsung Galaxy A55',
    'Samsung Galaxy M34',
    'OnePlus 12',
    'OnePlus 12R',
    'OnePlus Nord 4',
    'iQOO Neo 9 Pro',
    'iQOO 12',
    'Xiaomi 14 Civi',
    'Xiaomi Redmi Note 13 Pro',
    'Google Pixel 9',
    'Google Pixel 9 Pro Fold',
    'Nothing Phone (2a)',
    'Realme GT 6',
    'Motorola Edge 50 Pro',
    'Vivo V40 Pro',
    'Poco F6',
    'Apple iPhone 16 Pro Max'
]

for p in phones_to_test:
    res = get_organic_images(f"{p} smartphone official")
    oips = res.get('oip', [])
    first_oip = oips[0] if oips else 'NONE'
    print(f"{p:30} => {first_oip}")
