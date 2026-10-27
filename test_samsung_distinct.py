import urllib.request
import urllib.parse
from html.parser import HTMLParser
import sys

sys.stdout.reconfigure(encoding='utf-8')

class BingOrganicParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs_dict = dict(attrs)
            if 'class' in attrs_dict and 'mimg' in attrs_dict['class']:
                src = attrs_dict.get('src') or attrs_dict.get('data-src')
                # ONLY take organic images (OIP), reject sponsored (OIF)
                if src and '/th/id/OIP.' in src and src not in self.urls:
                    self.urls.append(src)

def get_phone_img(query):
    q_enc = urllib.parse.quote(query)
    url = f"https://www.bing.com/images/search?q={q_enc}&form=HDRSC2&first=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            parser = BingOrganicParser()
            parser.feed(html)
            return parser.urls
    except Exception as e:
        return []

samsung_models = [
    'Samsung Galaxy S24',
    'Samsung Galaxy S25 Ultra',
    'Samsung Galaxy Z Flip 6',
    'Samsung Galaxy Z Fold 6',
    'Samsung Galaxy A55 5G',
    'Samsung Galaxy A35 5G',
    'Samsung Galaxy M34 5G',
    'Samsung Galaxy F54 5G',
    'Samsung Galaxy S23 FE',
    'OnePlus 12',
    'OnePlus 12R',
    'OnePlus Nord CE 4',
    'iQOO Neo 9 Pro',
    'iQOO 12',
    'Xiaomi 14 Ultra',
    'Xiaomi 14 Civi',
    'Google Pixel 9 Pro XL',
    'Google Pixel 9',
    'Nothing Phone (2a) Plus',
    'Nothing Phone (2)'
]

for p in samsung_models:
    urls = get_phone_img(f"{p} smartphone")
    print(f"{p:30} => {urls[0] if urls else 'NONE'}")
