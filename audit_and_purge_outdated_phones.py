import json

def audit_and_purge():
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

    # Active active market criteria:
    # 1. release_year >= 2022 (or 2021+ active 4G/5G models)
    # 2. price_numeric > 0 and price_numeric < 250000
    # 3. Not an ancient obsolete model (e.g. 2G feature phones, decade-old models)

    active_phones = []
    purged_outdated = []

    for phone in phones:
        year = phone.get('release_year') or 2022
        price = phone.get('price_numeric') or 0
        name = (phone.get('name') or '').lower()
        specs = phone.get('specs') or {}
        display = (specs.get('display') or '').lower()

        # Check if legacy 2G or ancient screen sizes (< 5.0 inch feature phones)
        is_feature_phone = 'feature' in name or '2g' in name or ('tft' in display and year < 2021)
        is_ancient_year = year < 2022

        if is_ancient_year or is_feature_phone or price <= 0:
            purged_outdated.append(phone)
        else:
            active_phones.append(phone)

    print(f"Purged {len(purged_outdated)} outdated / unavailable devices.")
    print(f"Retained {len(active_phones)} active, modern smartphones in database.")

    prefix = content[:start_idx]
    suffix = content[end_idx:]
    new_json_str = json.dumps(active_phones, indent=2)

    with open('phones.js', 'w', encoding='utf-8') as f:
        f.write(prefix + new_json_str + suffix)

    print("Successfully updated phones.js!")

if __name__ == '__main__':
    audit_and_purge()
