import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('phones.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract PHONES array using bracket counting
start = content.index('var PHONES = [') + len('var PHONES = ')
depth = 0
end_idx = start
for i in range(start, len(content)):
    if content[i] == '[':
        depth += 1
    elif content[i] == ']':
        depth -= 1
        if depth == 0:
            end_idx = i + 1
            break

text = content[start:end_idx]
phones = json.loads(text)

print(f'Total phones: {len(phones)}')

has_image = sum(1 for p in phones if p.get('image'))
has_images = sum(1 for p in phones if p.get('images'))
no_img = sum(1 for p in phones if not p.get('image') and not p.get('images'))

print(f'Has image field: {has_image}')
print(f'Has images field: {has_images}')
print(f'No image at all: {no_img}')

all_imgs = set()
for p in phones:
    img = p.get('image', '')
    if img:
        all_imgs.add(img)
    for im in p.get('images', []):
        all_imgs.add(im)
print(f'Unique image URLs: {len(all_imgs)}')

# Check image URL patterns
patterns = {}
for img in all_imgs:
    if 'gsmarena' in img:
        patterns['gsmarena'] = patterns.get('gsmarena', 0) + 1
    elif 'amazon' in img:
        patterns['amazon'] = patterns.get('amazon', 0) + 1
    elif 'flipkart' in img:
        patterns['flipkart'] = patterns.get('flipkart', 0) + 1
    elif 'fdn.gsmarena' in img:
        patterns['fdn.gsmarena'] = patterns.get('fdn.gsmarena', 0) + 1
    elif 'placeholder' in img.lower() or 'default' in img.lower():
        patterns['placeholder'] = patterns.get('placeholder', 0) + 1
    else:
        domain = img.split('/')[2] if img.startswith('http') and len(img.split('/')) > 2 else 'other'
        patterns[domain] = patterns.get(domain, 0) + 1

print(f'\nImage URL patterns:')
for k, v in sorted(patterns.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')

# Sample phones
print('\nFirst 10 phones with images:')
for p in phones[:10]:
    name = p.get('name', '?')
    img = p.get('image', 'NO IMAGE')
    trunc = img[:100] if img else 'NO IMAGE'
    print(f'  {name} -> {trunc}')

# Check for duplicate images (same URL for different phones)
img_to_phones = {}
for p in phones:
    img = p.get('image', '')
    if img:
        if img not in img_to_phones:
            img_to_phones[img] = []
        img_to_phones[img].append(p.get('name', '?'))

dups = {k: v for k, v in img_to_phones.items() if len(v) > 1}
print(f'\nImages shared by multiple phones: {len(dups)}')
for img, names in sorted(dups.items(), key=lambda x: -len(x[1]))[:10]:
    print(f'  {len(names)} phones share: {img[:80]}...')
    for n in names[:5]:
        print(f'    - {n}')
    if len(names) > 5:
        print(f'    ... and {len(names)-5} more')
