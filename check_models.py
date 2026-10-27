import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('phones.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('var PHONES = [') + len('var PHONES = ')
end_idx = content.find('];\n\nconst CRITERIA', start_idx)
phones = json.loads(content[start_idx:end_idx + 1])

print("=== Xiaomi phones matching 14 ===")
for p in phones:
    if 'xiaomi' in p['brand'].lower() and '14' in p['name'].lower():
        print(f"  {p['id']} | {p['brand']} {p['name']} | Img: {p['image']}")

print("\n=== Vivo phones ===")
for p in phones:
    if 'vivo' in p['brand'].lower():
        if any(k in p['name'].lower() for k in ['x', 'v', 't', 'y']):
            print(f"  {p['id']} | {p['brand']} {p['name']} | Img: {p['image']}")
