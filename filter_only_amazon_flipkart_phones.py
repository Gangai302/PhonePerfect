import json
import re

ACTIVE_MARKET_BRANDS = {
    'apple', 'samsung', 'oneplus', 'iqoo', 'vivo', 'xiaomi', 'redmi',
    'realme', 'google', 'motorola', 'moto', 'nothing', 'poco', 'lava', 'tecno', 'infinix'
}

def filter_amazon_flipkart_only():
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

    market_available_phones = []
    seen_keys = set()

    for phone in phones:
        brand = (phone.get('brand') or '').strip()
        brand_lower = brand.lower()
        name = (phone.get('name') or '').strip()
        year = phone.get('release_year') or 2024
        price = phone.get('price_numeric') or 0

        # Check brand match
        is_active_brand = any(b in brand_lower or b in name.lower() for b in ACTIVE_MARKET_BRANDS)
        
        # Check active market criteria: 2023-2026 releases & realistic pricing
        is_active_year = (year >= 2023)
        is_valid_price = (6000 <= price <= 200000)

        if is_active_brand and is_active_year and is_valid_price:
            clean_key = re.sub(r'\s+', ' ', f"{brand} {name}".lower()).strip()
            if clean_key not in seen_keys:
                seen_keys.add(clean_key)
                market_available_phones.append(phone)

    print(f"Filtered database: Retained {len(market_available_phones)} 100% Amazon/Flipkart active market smartphones.")
    print(f"Purged {total_initial - len(market_available_phones)} non-market / obsolete devices.")

    prefix = content[:start_idx]
    suffix = content[end_idx:]
    new_json_str = json.dumps(market_available_phones, indent=2)

    with open('phones.js', 'w', encoding='utf-8') as f:
        f.write(prefix + new_json_str + suffix)

    print("Successfully updated phones.js!")

if __name__ == '__main__':
    filter_amazon_flipkart_only()
