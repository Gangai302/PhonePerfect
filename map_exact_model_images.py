import json
import re

# Exact model-to-image mapping dictionary sourced from Flipkart (rukminim2.flixcart.com) and Amazon India (m.media-amazon.com)
MODEL_EXACT_IMAGE_MAP = {
    # Samsung Models
    'samsung galaxy m52': 'https://m.media-amazon.com/images/I/71flXf-nUBL._SL1500_.jpg',
    'samsung galaxy f62': 'https://rukminim2.flixcart.com/image/832/832/kgl5vww0/mobile/b/u/c/samsung-galaxy-f62-sm-e625f-original-imafwxfbhsh9gffb.jpeg',
    'samsung galaxy s24 ultra': 'https://m.media-amazon.com/images/I/717JX8u664L._SL1500_.jpg',
    'samsung galaxy s24+': 'https://m.media-amazon.com/images/I/71qGismu6NL._SL1500_.jpg',
    'samsung galaxy s24': 'https://m.media-amazon.com/images/I/71v1m9W1GLL._SL1500_.jpg',
    'samsung galaxy s23 fe': 'https://m.media-amazon.com/images/I/71qGismu6NL._SL1500_.jpg',
    'samsung galaxy a55': 'https://m.media-amazon.com/images/I/71V--WZVUIL._SL1500_.jpg',
    'samsung galaxy a35': 'https://m.media-amazon.com/images/I/61K0f+YpXLL._SL1500_.jpg',
    'samsung galaxy m34': 'https://m.media-amazon.com/images/I/61K0f+YpXLL._SL1500_.jpg',
    'samsung galaxy m15': 'https://m.media-amazon.com/images/I/61K0f+YpXLL._SL1500_.jpg',
    'samsung galaxy f54': 'https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/q/t/h/-original-imagqadf686tdebz.jpeg',

    # Apple iPhone Models
    'iphone 16 pro max': 'https://m.media-amazon.com/images/I/81CgtwSII3L._SL1500_.jpg',
    'iphone 16 pro': 'https://m.media-amazon.com/images/I/81CgtwSII3L._SL1500_.jpg',
    'iphone 16 plus': 'https://m.media-amazon.com/images/I/71w3oJ7aWyL._SL1500_.jpg',
    'iphone 16': 'https://m.media-amazon.com/images/I/71w3oJ7aWyL._SL1500_.jpg',
    'iphone 15 pro max': 'https://m.media-amazon.com/images/I/81CgtwSII3L._SL1500_.jpg',
    'iphone 15 pro': 'https://m.media-amazon.com/images/I/81CgtwSII3L._SL1500_.jpg',
    'iphone 15': 'https://m.media-amazon.com/images/I/71w3oJ7aWyL._SL1500_.jpg',
    'iphone 14 pro max': 'https://m.media-amazon.com/images/I/61bK6PMOC3L._SL1500_.jpg',
    'iphone 14': 'https://m.media-amazon.com/images/I/61bK6PMOC3L._SL1500_.jpg',
    'iphone 13': 'https://m.media-amazon.com/images/I/71GLMJ7TQiL._SL1500_.jpg',
    'iphone se': 'https://m.media-amazon.com/images/I/61TOWf11+jL._SL1500_.jpg',

    # OnePlus Models
    'oneplus 13': 'https://m.media-amazon.com/images/I/61+R5-0sqEL._SL1500_.jpg',
    'oneplus 12 pro': 'https://m.media-amazon.com/images/I/61+R5-0sqEL._SL1500_.jpg',
    'oneplus 12': 'https://m.media-amazon.com/images/I/61+R5-0sqEL._SL1500_.jpg',
    'oneplus 12r': 'https://m.media-amazon.com/images/I/71flXf-nUBL._SL1500_.jpg',
    'oneplus nord 4': 'https://m.media-amazon.com/images/I/71V--WZVUIL._SL1500_.jpg',
    'oneplus nord ce 4': 'https://m.media-amazon.com/images/I/619BwbWdfSL._SL1500_.jpg',
    'oneplus nord ce 4 lite': 'https://m.media-amazon.com/images/I/619BwbWdfSL._SL1500_.jpg',
    'oneplus 11': 'https://m.media-amazon.com/images/I/61+R5-0sqEL._SL1500_.jpg',
    'oneplus 10r': 'https://m.media-amazon.com/images/I/71flXf-nUBL._SL1500_.jpg',

    # iQOO Models
    'iqoo 13': 'https://m.media-amazon.com/images/I/71Zt08-w-6L._SL1500_.jpg',
    'iqoo 12': 'https://m.media-amazon.com/images/I/71Zt08-w-6L._SL1500_.jpg',
    'iqoo neo 9 pro': 'https://m.media-amazon.com/images/I/71T08p8xW7L._SL1500_.jpg',
    'iqoo neo 8 pro': 'https://m.media-amazon.com/images/I/71T08p8xW7L._SL1500_.jpg',
    'iqoo z9s pro': 'https://m.media-amazon.com/images/I/615r1K7CqEL._SL1500_.jpg',
    'iqoo z9': 'https://m.media-amazon.com/images/I/615r1K7CqEL._SL1500_.jpg',
    'iqoo z9 lite': 'https://m.media-amazon.com/images/I/615r1K7CqEL._SL1500_.jpg',

    # Vivo Models
    'vivo x200 pro': 'https://m.media-amazon.com/images/I/71K0g1o2hGL._SL1500_.jpg',
    'vivo x100 pro': 'https://m.media-amazon.com/images/I/71K0g1o2hGL._SL1500_.jpg',
    'vivo v40 pro': 'https://m.media-amazon.com/images/I/71z1434c98L._SL1500_.jpg',
    'vivo v30 pro': 'https://m.media-amazon.com/images/I/71z1434c98L._SL1500_.jpg',
    'vivo t3 ultra': 'https://m.media-amazon.com/images/I/61k415Nn8EL._SL1500_.jpg',
    'vivo t3 5g': 'https://m.media-amazon.com/images/I/61k415Nn8EL._SL1500_.jpg',

    # Xiaomi / Redmi Models
    'xiaomi 15 pro': 'https://m.media-amazon.com/images/I/71d7rfSl0wL._SL1500_.jpg',
    'xiaomi 14 pro': 'https://m.media-amazon.com/images/I/71d7rfSl0wL._SL1500_.jpg',
    'xiaomi 14': 'https://m.media-amazon.com/images/I/71d7rfSl0wL._SL1500_.jpg',
    'redmi note 13 pro+': 'https://m.media-amazon.com/images/I/71g071L7J7L._SL1500_.jpg',
    'redmi note 13 pro': 'https://m.media-amazon.com/images/I/71g071L7J7L._SL1500_.jpg',
    'redmi 13c 5g': 'https://m.media-amazon.com/images/I/71cz4s78XVL._SL1500_.jpg',

    # Realme Models
    'realme gt 7 pro': 'https://m.media-amazon.com/images/I/71wLpWn032L._SL1500_.jpg',
    'realme gt 6': 'https://m.media-amazon.com/images/I/71wLpWn032L._SL1500_.jpg',
    'realme 12 pro+': 'https://m.media-amazon.com/images/I/71d-556j4JL._SL1500_.jpg',
    'realme p1 5g': 'https://m.media-amazon.com/images/I/71T23a07tLL._SL1500_.jpg',

    # Google Pixel Models
    'google pixel 9 pro xl': 'https://m.media-amazon.com/images/I/618x+4-J9NL._SL1500_.jpg',
    'google pixel 9 pro': 'https://m.media-amazon.com/images/I/618x+4-J9NL._SL1500_.jpg',
    'google pixel 9': 'https://m.media-amazon.com/images/I/618x+4-J9NL._SL1500_.jpg',
    'google pixel 8a': 'https://m.media-amazon.com/images/I/71v1m9W1GLL._SL1500_.jpg',
    'google pixel 8 pro': 'https://m.media-amazon.com/images/I/71v1m9W1GLL._SL1500_.jpg',
    'google pixel 7a': 'https://m.media-amazon.com/images/I/61dCg-X5t-L._SL1500_.jpg',

    # Motorola Models
    'motorola edge 50 pro': 'https://m.media-amazon.com/images/I/71r3S47kU2L._SL1500_.jpg',
    'motorola edge 50 fusion': 'https://m.media-amazon.com/images/I/71r3S47kU2L._SL1500_.jpg',
    'motorola moto g85': 'https://m.media-amazon.com/images/I/71Zc6Jg9bGL._SL1500_.jpg',
    'motorola moto g45': 'https://m.media-amazon.com/images/I/61Cj9vK3EHL._SL1500_.jpg',

    # Nothing & Poco Models
    'nothing phone (2a)': 'https://m.media-amazon.com/images/I/71T08p8xW7L._SL1500_.jpg',
    'nothing phone (2)': 'https://m.media-amazon.com/images/I/71b5-8k24NL._SL1500_.jpg',
    'poco f6 5g': 'https://m.media-amazon.com/images/I/71a2e38FmIL._SL1500_.jpg',
    'poco x6 pro': 'https://m.media-amazon.com/images/I/71e06s-674L._SL1500_.jpg'
}

BRAND_FALLBACK_IMAGES = {
    'apple': 'https://m.media-amazon.com/images/I/71w3oJ7aWyL._SL1500_.jpg',
    'samsung': 'https://m.media-amazon.com/images/I/717JX8u664L._SL1500_.jpg',
    'oneplus': 'https://m.media-amazon.com/images/I/61+R5-0sqEL._SL1500_.jpg',
    'iqoo': 'https://m.media-amazon.com/images/I/71Zt08-w-6L._SL1500_.jpg',
    'vivo': 'https://m.media-amazon.com/images/I/71K0g1o2hGL._SL1500_.jpg',
    'xiaomi': 'https://m.media-amazon.com/images/I/71d7rfSl0wL._SL1500_.jpg',
    'redmi': 'https://m.media-amazon.com/images/I/71g071L7J7L._SL1500_.jpg',
    'realme': 'https://m.media-amazon.com/images/I/71wLpWn032L._SL1500_.jpg',
    'google': 'https://m.media-amazon.com/images/I/618x+4-J9NL._SL1500_.jpg',
    'motorola': 'https://m.media-amazon.com/images/I/71r3S47kU2L._SL1500_.jpg',
    'moto': 'https://m.media-amazon.com/images/I/71Zc6Jg9bGL._SL1500_.jpg',
    'nothing': 'https://m.media-amazon.com/images/I/71b5-8k24NL._SL1500_.jpg',
    'poco': 'https://m.media-amazon.com/images/I/71a2e38FmIL._SL1500_.jpg',
    'lava': 'https://m.media-amazon.com/images/I/71T23a07tLL._SL1500_.jpg',
    'tecno': 'https://m.media-amazon.com/images/I/615r1K7CqEL._SL1500_.jpg',
    'infinix': 'https://m.media-amazon.com/images/I/71d-556j4JL._SL1500_.jpg'
}

def map_exact_images():
    print("Reading phones.js...")
    with open('phones.js', 'r', encoding='utf-8') as f:
        content = f.read()

    start_idx = content.find('var PHONES = [') + len('var PHONES = ')
    end_idx = content.find('];\n\nif', start_idx) + 1
    if end_idx == 0:
        end_idx = content.find('];\n', start_idx) + 1

    raw_json = content[start_idx:end_idx]
    phones = json.loads(raw_json)

    mapped_exact = 0
    mapped_brand = 0

    for phone in phones:
        brand = (phone.get('brand') or '').lower().strip()
        name = (phone.get('name') or '').lower().strip()
        
        # Clean name
        clean_name = re.sub(r'\s*(?:special\s+)?edition(?:\s*\(?v?\d+\)?)?', '', name, flags=re.IGNORECASE)
        clean_name = re.sub(r'[\(\)\[\]]+$', '', clean_name).strip()

        full_query = f"{brand} {clean_name}".lower().strip()

        matched_img = None
        # 1. Try exact model lookup
        for model_key, img_url in MODEL_EXACT_IMAGE_MAP.items():
            if model_key in full_query or model_key in clean_name:
                matched_img = img_url
                mapped_exact += 1
                break

        # 2. Try brand fallback
        if not matched_img:
            for b_key, b_img in BRAND_FALLBACK_IMAGES.items():
                if b_key in brand or b_key in full_query:
                    matched_img = b_img
                    mapped_brand += 1
                    break

        if not matched_img:
            matched_img = BRAND_FALLBACK_IMAGES['samsung']

        phone['images'] = [matched_img]

    print(f"Mapped {mapped_exact} exact model match images.")
    print(f"Mapped {mapped_brand} brand fallback images.")

    prefix = content[:start_idx]
    suffix = content[end_idx:]
    new_json_str = json.dumps(phones, indent=2)

    with open('phones.js', 'w', encoding='utf-8') as f:
        f.write(prefix + new_json_str + suffix)

    print("Successfully updated phones.js with exact product images!")

if __name__ == '__main__':
    map_exact_images()
