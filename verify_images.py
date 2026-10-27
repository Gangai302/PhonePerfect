import json

with open('phones.js', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('var PHONES = [') + len('var PHONES = ')
depth = 0
for i in range(start, len(content)):
    if content[i] == '[': depth += 1
    elif content[i] == ']':
        depth -= 1
        if depth == 0:
            end_idx = i + 1
            break
phones = json.loads(content[start:end_idx])

sample_queries = [
    'OnePlus 12',
    'Galaxy S24',
    'iQOO Neo 9 Pro',
    'Xiaomi 14',
    'Nothing Phone (2a)',
    'Realme GT 6',
    'Motorola Edge 50 Pro',
    'Pixel 9'
]

print("=== Verification of Specific Target Phone Models ===")
for q in sample_queries:
    matches = [p for p in phones if q.lower() in p.get('name', '').lower()]
    if matches:
        p = matches[0]
        print(f"Model: {p.get('name')}")
        print(f"Image: {p.get('image')}\n")

# Check overall coverage
has_img = [p for p in phones if p.get('image') and p.get('image').startswith('http')]
print(f"Total Phones: {len(phones)}")
print(f"Phones with Valid HTTP Images: {len(has_img)} ({len(has_img)/len(phones)*100:.1f}%)")

unique_images = len(set(p.get('image') for p in has_img))
print(f"Distinct Image URLs: {unique_images}")
