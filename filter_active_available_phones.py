import json
import re

# List of discontinued / obsolete / legacy phone name patterns that are unavailable on Amazon India
DISCONTINUED_PATTERNS = [
    r'fairphone\s*(?:3|4)?',
    r'nokia\s*(?:x20|x10|g20|c20|g10|1\.4|2\.4|3\.4|5\.4|8\.3)',
    r'sony\s*xperia\s*(?:5\s*v|10\s*v|1\s*v|5\s*iv|10\s*iv|1\s*iv|5\s*iii|10\s*iii|1\s*iii)',
    r'zte',
    r'asus\s*zenfone\s*(?:8|9|10)',
    r'lg\s*',
    r'htc\s*',
    r'blackberry\s*',
    r'gionee\s*',
    r'micromax\s*(?:in\s*note|canvas|evok)',
    r'coolpad\s*',
    r'leeco\s*',
    r'meizu\s*',
    r'lenovo\s*(?:k12|k13|k14|lemon)',
    r'motorola\s*moto\s*e[0-9]+',
    r'samsung\s*galaxy\s*(?:s10|s20|s21|s9|s8|s7|note\s*10|note\s*20|a50|a51|a52|a70|a71|a30|a20|a10|m10|m20|m30)',
    r'iphone\s*(?:6|7|8|x|xs|xr|11|12)\b',
    r'oneplus\s*(?:6|7|8|9|nord\s*ce\s*2|nord\s*n10|nord\s*n100)\b',
    r'xiaomi\s*redmi\s*(?:note\s*8|note\s*9|note\s*10|note\s*11|9a|9c|10a|10c)\b',
    r'realme\s*(?:3|5|6|7|8|c11|c12|c15|narzo\s*20|narzo\s*30)\b',
    r'vivo\s*(?:y11|y12|y15|y17|y19|v15|v17|v19|v20)\b',
    r'oppo\s*(?:a12|a15|a31|a53|f15|f17|reno\s*3|reno\s*4)\b'
]

def filter_available_phones():
    print("Reading phones.js...")
    with open('phones.js', 'r', encoding='utf-8') as f:
        content = f.read()

    start_idx = content.find('var PHONES = [') + len('var PHONES = ')
    end_idx = content.find('];\n\nif', start_idx) + 1
    if end_idx == 0:
        end_idx = content.find('];\n', start_idx) + 1

    raw_json = content[start_idx:end_idx]
    phones = json.loads(raw_json)

    total_initial = len(phones)
    print(f"Total initial devices in database: {total_initial}")

    compiled_patterns = [re.compile(p, re.IGNORECASE) for p in DISCONTINUED_PATTERNS]

    available_phones = []
    removed_count = 0

    seen_names = set()

    for phone in phones:
        name = phone.get('name') or ''
        brand = phone.get('brand') or ''
        full_name = f"{brand} {name}".lower()

        # Check if matches any discontinued pattern
        is_discontinued = any(pat.search(full_name) for pat in compiled_patterns)

        if is_discontinued:
            removed_count += 1
            continue

        # Prevent duplicate entries
        clean_key = re.sub(r'\s+', ' ', full_name).strip()
        if clean_key in seen_names:
            removed_count += 1
            continue

        seen_names.add(clean_key)
        available_phones.append(phone)

    print(f"Purged {removed_count} discontinued/unavailable/duplicate devices.")
    print(f"Retained {len(available_phones)} active, available smartphones in database.")

    prefix = content[:start_idx]
    suffix = content[end_idx:]
    new_json_str = json.dumps(available_phones, indent=2)

    with open('phones.js', 'w', encoding='utf-8') as f:
        f.write(prefix + new_json_str + suffix)

    print("Successfully updated phones.js!")

if __name__ == '__main__':
    filter_available_phones()
