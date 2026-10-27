import urllib.request
import urllib.parse
import re
import html
import sys

sys.stdout.reconfigure(encoding='utf-8')

def get_gsmarena_image(phone_name):
    clean_name = phone_name.replace('5G', '').strip()
    url = f"https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName={urllib.parse.quote(clean_name)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            # Look for makers results
            # e.g., <img src="https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-5g-sm-s921.jpg" title="Samsung Galaxy S24">
            imgs = re.findall(r'<img\s+src=[\"\'](https://fdn2\.gsmarena\.com/vv/bigpic/[^\"\']+)[\"\']\s+title=[\"\']([^\"\']+)[\"\']', content)
            if not imgs:
                imgs = re.findall(r'<img\s+src=[\"\'](https://fdn2\.gsmarena\.com/vv/bigpic/[^\"\']+)[\"\']', content)
                if imgs:
                    return imgs[0]
            else:
                return imgs[0][0]
    except Exception as e:
        return None
    return None

test_models = ['Samsung Galaxy S24', 'OnePlus 12', 'iQOO Neo 9 Pro', 'Xiaomi 14 Civi', 'Motorola Edge 50 Pro', 'Nothing Phone (2a)', 'Realme GT 6', 'Google Pixel 9', 'Vivo V40 Pro', 'Poco F6']

for m in test_models:
    img = get_gsmarena_image(m)
    print(f"{m} (GSMArena) -> {img}")
