import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('phones.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('var PHONES = [') + len('var PHONES = ')
end_idx = content.find('];\n\nconst CRITERIA', start_idx)
phones = json.loads(content[start_idx:end_idx + 1])

civi_found = [p for p in phones if 'civi' in p['name'].lower() or 'civi' in p['id'].lower()]
print(f"Civi phones found: {len(civi_found)}")
for p in civi_found:
    print(f"  {p['id']} | {p['brand']} {p['name']}")

s24_found = [p for p in phones if 's24' in p['name'].lower() or 's24' in p['id'].lower()]
print(f"\nS24 phones found: {len(s24_found)}")
for p in s24_found:
    print(f"  {p['id']} | {p['brand']} {p['name']} | Img: {p['image']}")

op12_found = [p for p in phones if '12' in p['name'].lower() and 'oneplus' in p['brand'].lower()]
print(f"\nOnePlus 12 phones found: {len(op12_found)}")
for p in op12_found:
    print(f"  {p['id']} | {p['brand']} {p['name']} | Img: {p['image']}")
