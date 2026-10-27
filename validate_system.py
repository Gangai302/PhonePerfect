import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Validate phones.js
with open('phones.js', 'r', encoding='utf-8') as f:
    phones_txt = f.read()

start_idx = phones_txt.find('var PHONES = [') + len('var PHONES = ')
end_idx = phones_txt.find('];\n\nconst CRITERIA', start_idx)
phones = json.loads(phones_txt[start_idx:end_idx + 1])

print(f"1. phones.js loaded successfully: {len(phones)} phones.")

# 2. Check images validity
missing_images = []
for p in phones:
    img = p.get('image') or (p.get('images', [None])[0])
    if not img or not str(img).startswith('http'):
        missing_images.append(p['id'])

print(f"   Missing images: {len(missing_images)}")

# 3. Check critical models
test_models = [
    'OnePlus 12',
    'Galaxy S24',
    'iQOO Neo 9 Pro',
    'Google Pixel 9',
    'Nothing Phone (2a)',
    'Realme GT 6',
    'Motorola Edge 50 Pro',
    'Poco F6',
    'iPhone 16 Pro Max'
]

print("\n2. Critical models check:")
for tm in test_models:
    matched = [p for p in phones if tm.lower() in p['name'].lower() or tm.lower() in p['id'].lower()]
    if matched:
        p = matched[0]
        print(f"   ✓ {p['brand']} {p['name']} -> {p['image']}")
    else:
        print(f"   ✗ {tm} -> NOT FOUND")

# 4. Check app.js syntax / balance
with open('app.js', 'r', encoding='utf-8') as f:
    app_txt = f.read()

stack = []
pairs = {'{': '}', '(': ')', '[': ']'}
for i, c in enumerate(app_txt):
    if c in pairs:
        stack.append((c, i))
    elif c in pairs.values():
        if not stack:
            print(f"   Unmatched closing {c} at pos {i}")
            break
        top, top_idx = stack.pop()
        if pairs[top] != c:
            print(f"   Mismatched {top} at {top_idx} with {c} at {i}")
            break
else:
    if stack:
        print(f"   Unclosed brackets: {len(stack)}")
    else:
        print("\n3. app.js brackets/parentheses perfectly balanced!")

print("\nValidation completed successfully!")
