import urllib.request
import urllib.parse
import re
import html
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def find_exact_model_image(brand, model_name):
    # Clean model name
    clean_model = re.sub(r'\s*\((Edition|v|Edition \d+|v\d+|\d{4})\s*\d*\)', '', model_name, flags=re.IGNORECASE).strip()
    if brand.lower() not in clean_model.lower():
        full_name = f"{brand} {clean_model}"
    else:
        full_name = clean_model

    # Model keywords for title matching
    keywords = [w.lower() for w in clean_model.split() if len(w) > 1 and w.lower() not in ['smartphone', '5g', '4g', 'edition', 'series']]
    
    query = f"{full_name} smartphone official"
    q_enc = urllib.parse.quote(query)
    url = f"https://www.bing.com/images/search?q={q_enc}&form=HDRSC2&first=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            m_matches = re.findall(r'class="iusc"[^>]*\sm="([^"]+)"', content)
            
            # Pass 1: find result where title contains all keywords
            for m_raw in m_matches:
                data = json.loads(html.unescape(m_raw))
                title = data.get('t', '').lower()
                murl = data.get('murl', '')
                turl = data.get('turl', '')
                
                # Check if all keywords are in title or murl
                if all(k in title or k in murl.lower() for k in keywords):
                    # We have an exact match!
                    # Prefer turl or murl
                    # turl from Bing is reliable and fast
                    if turl:
                        return turl, title, data.get('murl')
            
            # Pass 2: find result where title contains brand and at least primary model number
            for m_raw in m_matches:
                data = json.loads(html.unescape(m_raw))
                title = data.get('t', '').lower()
                turl = data.get('turl', '')
                if brand.lower() in title and any(k in title for k in keywords):
                    if turl:
                        return turl, title, data.get('murl')
                        
            # Pass 3: first organic result if none matched
            for m_raw in m_matches:
                data = json.loads(html.unescape(m_raw))
                turl = data.get('turl', '')
                if turl and 'OIP.' in turl:
                    return turl, data.get('t', ''), data.get('murl')
                    
    except Exception as e:
        print(f"Error fetching for {full_name}: {e}")
    return None, None, None

test_models = [
    ('Samsung', 'Galaxy S24'),
    ('Samsung', 'Galaxy S24 Ultra'),
    ('Samsung', 'Galaxy S25 Ultra'),
    ('Samsung', 'Galaxy Z Flip 6'),
    ('Samsung', 'Galaxy A55 5G'),
    ('OnePlus', 'OnePlus 12'),
    ('OnePlus', 'OnePlus 12R'),
    ('OnePlus', 'OnePlus Nord 4'),
    ('iQOO', 'iQOO Neo 9 Pro'),
    ('iQOO', 'iQOO 12'),
    ('Xiaomi', 'Xiaomi 14 Civi'),
    ('Xiaomi', 'Xiaomi 14 Ultra'),
    ('Google', 'Google Pixel 9'),
    ('Google', 'Google Pixel 9 Pro Fold'),
    ('Nothing', 'Nothing Phone (2a)'),
    ('Realme', 'Realme GT 6'),
    ('Motorola', 'Motorola Edge 50 Pro'),
    ('Motorola', 'Motorola Moto G85'),
    ('Vivo', 'Vivo V40 Pro'),
    ('Vivo', 'Vivo T3 Ultra'),
    ('Poco', 'Poco F6'),
    ('Apple', 'iPhone 16 Pro Max'),
    ('Apple', 'iPhone 15')
]

for brand, name in test_models:
    img, title, src = find_exact_model_image(brand, name)
    print(f"[{brand}] {name:25} => {img}")
    print(f"     Title: {title}")
