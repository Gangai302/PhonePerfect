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

clean_names_modified = 0
storage_added = 0

for p in phones:
    # 1. Clean display name while preserving phone ID and actual model identities
    orig_name = p.get('name', '')
    cleaned_name = re.sub(r'\s*special\s+edition(?:\s*\(?v?\d+\)?)?', '', orig_name, flags=re.IGNORECASE)
    cleaned_name = re.sub(r'\s*\(?edition\s+\d+\)?', '', cleaned_name, flags=re.IGNORECASE)
    cleaned_name = re.sub(r'\s*\(?v\d+\)?', '', cleaned_name, flags=re.IGNORECASE)
    cleaned_name = re.sub(r'[\(\)\[\]\s]+$', '', cleaned_name)
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
    
    if cleaned_name and cleaned_name != orig_name:
        p['name'] = cleaned_name
        clean_names_modified += 1
        
    # 2. Ensure specs.storage is always canonically populated
    specs = p.setdefault('specs', {})
    if not specs.get('storage'):
        storage_gb = p.get('storage_gb')
        storage_options = p.get('storage_options')
        if storage_gb:
            specs['storage'] = f"{storage_gb}GB Storage"
        elif storage_options and 'GB' in storage_options:
            specs['storage'] = storage_options
        else:
            specs['storage'] = "128GB Storage"
        storage_added += 1

print(f"Cleaned names count: {clean_names_modified}")
print(f"Canonical storage specs added: {storage_added}")

# Write back updated phones.js
new_phones_json = json.dumps(phones, indent=2, ensure_ascii=False)
new_content = content[:start] + new_phones_json + content[end_idx:]
with open('phones.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("phones.js successfully updated and saved!")
