import urllib.request
import urllib.parse
from html.parser import HTMLParser
import sys

sys.stdout.reconfigure(encoding='utf-8')

class BingHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs_dict = dict(attrs)
            # Bing search result images have class 'mimg'
            if 'class' in attrs_dict and 'mimg' in attrs_dict['class']:
                src = attrs_dict.get('src') or attrs_dict.get('data-src')
                if src and src.startswith('http') and src not in self.urls:
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
            parser = BingHTMLParser()
            parser.feed(html)
            return parser.urls
    except Exception as e:
        return []

phones_to_test = [
    'Samsung Galaxy S24',
    'Samsung Galaxy S25 Ultra',
    'Samsung Galaxy Z Flip 6',
    'Samsung Galaxy A55',
    'OnePlus 12',
    'OnePlus Nord 4',
    'iQOO Neo 9 Pro',
    'Xiaomi 14 Civi',
    'Google Pixel 9',
    'Nothing Phone (2a)',
    'Realme GT 6',
    'Motorola Edge 50 Pro',
    'Vivo V40 Pro',
    'Apple iPhone 16 Pro Max'
]

for p in phones_to_test:
    urls = get_phone_img(f"{p} smartphone front back")
    print(f"{p:30} => {urls[0] if urls else 'NONE'}")
