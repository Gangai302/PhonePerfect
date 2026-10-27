import json
import re
import sys
from exact_images_catalog import EXACT_PHONE_MODEL_IMAGES

sys.stdout.reconfigure(encoding='utf-8')

# Read phones.js
with open('phones.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse the PHONES array
start_idx = content.find('var PHONES = [') + len('var PHONES = ')
end_idx = content.find('];\n\nconst CRITERIA', start_idx)
if end_idx == -1:
    end_idx = content.find('];\n\nif', start_idx)
if end_idx == -1:
    end_idx = content.find('];', start_idx)

json_str = content[start_idx:end_idx + 1]
phones = json.loads(json_str)

print(f"Loaded {len(phones)} phones from phones.js")

def find_best_image(phone):
    brand = phone.get('brand', '').lower().strip()
    name = phone.get('name', '').lower().strip()
    pid = phone.get('id', '').lower().strip()

    # Clean name
    clean_name = re.sub(r'\s*\((edition|v|edition \d+|v\d+|\d{4})\s*\d*\)', '', name, flags=re.IGNORECASE)
    clean_name = re.sub(r'\s*\(edition\s*\d+\)', '', clean_name, flags=re.IGNORECASE)
    clean_name = re.sub(r'\s*\(v\d+\)', '', clean_name, flags=re.IGNORECASE)
    clean_name = re.sub(r'\s*edition\s*\d+', '', clean_name, flags=re.IGNORECASE)
    clean_name = re.sub(r'\s*v\d+$', '', clean_name, flags=re.IGNORECASE).strip()

    full_target = f"{brand} {clean_name}" if brand not in clean_name else clean_name

    # 1. Exact match in catalog
    if full_target in EXACT_PHONE_MODEL_IMAGES:
        return EXACT_PHONE_MODEL_IMAGES[full_target]

    # 2. Substring matching (longest match first)
    matched_img = None
    max_len = 0
    for model_key, img_url in EXACT_PHONE_MODEL_IMAGES.items():
        if model_key in full_target or model_key in pid:
            if len(model_key) > max_len:
                max_len = len(model_key)
                matched_img = img_url

    if matched_img:
        return matched_img

    # 3. Keyword matching (brand + key model series)
    for model_key, img_url in EXACT_PHONE_MODEL_IMAGES.items():
        key_parts = model_key.split()
        if len(key_parts) >= 2:
            if all(p in full_target or p in pid for p in key_parts):
                return img_url

    # 4. Fallback if not matched: check existing image or clean brand representative image
    existing = phone.get('image') or (phone.get('images', [None])[0])
    if existing and str(existing).startswith('http'):
        return existing

    return "https://m.media-amazon.com/images/I/717Qo4MH97L._SL1500_.jpg"

# Apply to all phones
matched_count = 0
for phone in phones:
    img = find_best_image(phone)
    phone['image'] = img
    phone['images'] = [img]
    matched_count += 1

print(f"Updated images for all {matched_count} phones.")

# Verify critical test models
critical_models = [
    'OnePlus 12',
    'Galaxy S24',
    'iQOO Neo 9 Pro',
    'Xiaomi 14 Civi',
    'Google Pixel 9',
    'Nothing Phone (2a)',
    'Realme GT 6',
    'Motorola Edge 50 Pro',
    'Vivo V40 Pro',
    'Poco F6'
]

print("\n=== CRITICAL TEST MODELS VERIFICATION ===")
for test_name in critical_models:
    found = [p for p in phones if test_name.lower() in p['name'].lower() or test_name.lower() in p['id'].lower()]
    if found:
        p = found[0]
        print(f"  {p['brand']} {p['name']} (ID: {p['id']})")
        print(f"    Image: {p['image']}")
    else:
        print(f"  {test_name} -> NOT FOUND")

# Write back to phones.js preserving all rest of file
new_json = json.dumps(phones, indent=2)
prefix = content[:start_idx]
suffix = content[end_idx + 1:]
new_content = prefix + new_json + suffix

with open('phones.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\nSuccessfully updated phones.js!")
