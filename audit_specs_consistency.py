import json
import re

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

# Check canonical fields across records
required_fields = ['id', 'name', 'brand', 'price', 'specs', 'scores', 'image']
missing_counts = {k: 0 for k in required_fields}
spec_keys_dist = {}

for p in phones:
    for rf in required_fields:
        if rf not in p or p[rf] is None or p[rf] == '':
            missing_counts[rf] += 1
    specs = p.get('specs', {})
    for sk in ['battery', 'ram', 'storage', 'camera', 'processor', 'display', 'charging']:
        if sk not in specs or not specs[sk]:
            spec_keys_dist[sk] = spec_keys_dist.get(sk, 0) + 1

print('Total phone records:', len(phones))
print('Missing required top-level fields:', missing_counts)
print('Missing specs fields count:', spec_keys_dist)

# Clean name check
with_special_ed = [p['name'] for p in phones if 'special edition' in p['name'].lower()]
with_edition_num = [p['name'] for p in phones if re.search(r'\(edition\s+\d+\)', p['name'].lower())]
with_v_num = [p['name'] for p in phones if re.search(r'\(v\d+\)', p['name'].lower())]

print(f"Names with 'Special Edition': {len(with_special_ed)}")
print(f"Names with '(Edition XX)': {len(with_edition_num)}")
print(f"Names with '(vXX)': {len(with_v_num)}")
