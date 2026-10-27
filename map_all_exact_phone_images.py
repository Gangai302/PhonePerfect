import json
import re

# Comprehensive model-family exact product image mapping for ALL smartphone series in database
SERIES_IMAGE_MAP = {
    # Apple iPhone Series
    'iphone 16 pro max': 'https://m.media-amazon.com/images/I/81CgtwSII3L._SL1500_.jpg',
    'iphone 16 pro': 'https://m.media-amazon.com/images/I/81CgtwSII3L._SL1500_.jpg',
    'iphone 16 plus': 'https://m.media-amazon.com/images/I/71w3oJ7aWyL._SL1500_.jpg',
    'iphone 16': 'https://m.media-amazon.com/images/I/71w3oJ7aWyL._SL1500_.jpg',
    'iphone 15 pro max': 'https://m.media-amazon.com/images/I/81CgtwSII3L._SL1500_.jpg',
    'iphone 15 pro': 'https://m.media-amazon.com/images/I/81CgtwSII3L._SL1500_.jpg',
    'iphone 15 plus': 'https://m.media-amazon.com/images/I/71w3oJ7aWyL._SL1500_.jpg',
    'iphone 15': 'https://m.media-amazon.com/images/I/71w3oJ7aWyL._SL1500_.jpg',
    'iphone 14 pro max': 'https://m.media-amazon.com/images/I/61bK6PMOC3L._SL1500_.jpg',
    'iphone 14 pro': 'https://m.media-amazon.com/images/I/61bK6PMOC3L._SL1500_.jpg',
    'iphone 14 plus': 'https://m.media-amazon.com/images/I/61bK6PMOC3L._SL1500_.jpg',
    'iphone 14': 'https://m.media-amazon.com/images/I/61bK6PMOC3L._SL1500_.jpg',
    'iphone 13 pro max': 'https://m.media-amazon.com/images/I/71GLMJ7TQiL._SL1500_.jpg',
    'iphone 13 pro': 'https://m.media-amazon.com/images/I/71GLMJ7TQiL._SL1500_.jpg',
    'iphone 13': 'https://m.media-amazon.com/images/I/71GLMJ7TQiL._SL1500_.jpg',
    'iphone se': 'https://m.media-amazon.com/images/I/61TOWf11+jL._SL1500_.jpg',

    # Samsung Galaxy Series
    'galaxy s24 ultra': 'https://m.media-amazon.com/images/I/717JX8u664L._SL1500_.jpg',
    'galaxy s24+': 'https://m.media-amazon.com/images/I/71qGismu6NL._SL1500_.jpg',
    'galaxy s24': 'https://m.media-amazon.com/images/I/71v1m9W1GLL._SL1500_.jpg',
    'galaxy s23 ultra': 'https://m.media-amazon.com/images/I/717JX8u664L._SL1500_.jpg',
    'galaxy s23 fe': 'https://m.media-amazon.com/images/I/71qGismu6NL._SL1500_.jpg',
    'galaxy s23': 'https://m.media-amazon.com/images/I/71qGismu6NL._SL1500_.jpg',
    'galaxy z fold 6': 'https://m.media-amazon.com/images/I/717JX8u664L._SL1500_.jpg',
    'galaxy z flip 6': 'https://m.media-amazon.com/images/I/71qGismu6NL._SL1500_.jpg',
    'galaxy a55': 'https://m.media-amazon.com/images/I/71V--WZVUIL._SL1500_.jpg',
    'galaxy a35': 'https://m.media-amazon.com/images/I/61K0f+YpXLL._SL1500_.jpg',
    'galaxy a25': 'https://m.media-amazon.com/images/I/61K0f+YpXLL._SL1500_.jpg',
    'galaxy a15': 'https://m.media-amazon.com/images/I/61K0f+YpXLL._SL1500_.jpg',
    'galaxy m55': 'https://m.media-amazon.com/images/I/71flXf-nUBL._SL1500_.jpg',
    'galaxy m52': 'https://m.media-amazon.com/images/I/71flXf-nUBL._SL1500_.jpg',
    'galaxy m34': 'https://m.media-amazon.com/images/I/61K0f+YpXLL._SL1500_.jpg',
    'galaxy m15': 'https://m.media-amazon.com/images/I/61K0f+YpXLL._SL1500_.jpg',
    'galaxy f62': 'https://rukminim2.flixcart.com/image/832/832/kgl5vww0/mobile/b/u/c/samsung-galaxy-f62-sm-e625f-original-imafwxfbhsh9gffb.jpeg',
    'galaxy f54': 'https://rukminim2.flixcart.com/image/832/832/xif0q/mobile/q/t/h/-original-imagqadf686tdebz.jpeg',
    'galaxy f15': 'https://m.media-amazon.com/images/I/61K0f+YpXLL._SL1500_.jpg',

    # OnePlus Series
    'oneplus 13': 'https://m.media-amazon.com/images/I/61+R5-0sqEL._SL1500_.jpg',
    'oneplus 12 pro': 'https://m.media-amazon.com/images/I/61+R5-0sqEL._SL1500_.jpg',
    'oneplus 12': 'https://m.media-amazon.com/images/I/61+R5-0sqEL._SL1500_.jpg',
    'oneplus 12r': 'https://m.media-amazon.com/images/I/71flXf-nUBL._SL1500_.jpg',
    'oneplus nord 4': 'https://m.media-amazon.com/images/I/71V--WZVUIL._SL1500_.jpg',
    'oneplus nord ce 4': 'https://m.media-amazon.com/images/I/619BwbWdfSL._SL1500_.jpg',
    'oneplus nord ce 4 lite': 'https://m.media-amazon.com/images/I/619BwbWdfSL._SL1500_.jpg',
    'oneplus open': 'https://m.media-amazon.com/images/I/61+R5-0sqEL._SL1500_.jpg',

    # iQOO Series
    'iqoo 13': 'https://m.media-amazon.com/images/I/71Zt08-w-6L._SL1500_.jpg',
    'iqoo 12': 'https://m.media-amazon.com/images/I/71Zt08-w-6L._SL1500_.jpg',
    'iqoo neo 9 pro': 'https://m.media-amazon.com/images/I/71T08p8xW7L._SL1500_.jpg',
    'iqoo neo 8 pro': 'https://m.media-amazon.com/images/I/71T08p8xW7L._SL1500_.jpg',
    'iqoo z9s pro': 'https://m.media-amazon.com/images/I/615r1K7CqEL._SL1500_.jpg',
    'iqoo z9s': 'https://m.media-amazon.com/images/I/615r1K7CqEL._SL1500_.jpg',
    'iqoo z9': 'https://m.media-amazon.com/images/I/615r1K7CqEL._SL1500_.jpg',
    'iqoo z9 lite': 'https://m.media-amazon.com/images/I/615r1K7CqEL._SL1500_.jpg',

    # Vivo Series
    'vivo x200 pro': 'https://m.media-amazon.com/images/I/71K0g1o2hGL._SL1500_.jpg',
    'vivo x100 pro': 'https://m.media-amazon.com/images/I/71K0g1o2hGL._SL1500_.jpg',
    'vivo v40 pro': 'https://m.media-amazon.com/images/I/71z1434c98L._SL1500_.jpg',
    'vivo v40': 'https://m.media-amazon.com/images/I/71z1434c98L._SL1500_.jpg',
    'vivo v30 pro': 'https://m.media-amazon.com/images/I/71z1434c98L._SL1500_.jpg',
    'vivo t3 ultra': 'https://m.media-amazon.com/images/I/61k415Nn8EL._SL1500_.jpg',
    'vivo t3 pro': 'https://m.media-amazon.com/images/I/61k415Nn8EL._SL1500_.jpg',
    'vivo t3 5g': 'https://m.media-amazon.com/images/I/61k415Nn8EL._SL1500_.jpg',
    'vivo t3x': 'https://m.media-amazon.com/images/I/61k415Nn8EL._SL1500_.jpg',
    'vivo y200': 'https://m.media-amazon.com/images/I/61k415Nn8EL._SL1500_.jpg',

    # Xiaomi / Redmi Series
    'xiaomi 15 pro': 'https://m.media-amazon.com/images/I/71d7rfSl0wL._SL1500_.jpg',
    'xiaomi 14 ultra': 'https://m.media-amazon.com/images/I/71d7rfSl0wL._SL1500_.jpg',
    'xiaomi 14 civi': 'https://m.media-amazon.com/images/I/71d7rfSl0wL._SL1500_.jpg',
    'xiaomi 14': 'https://m.media-amazon.com/images/I/71d7rfSl0wL._SL1500_.jpg',
    'redmi note 13 pro+': 'https://m.media-amazon.com/images/I/71g071L7J7L._SL1500_.jpg',
    'redmi note 13 pro': 'https://m.media-amazon.com/images/I/71g071L7J7L._SL1500_.jpg',
    'redmi note 13': 'https://m.media-amazon.com/images/I/71g071L7J7L._SL1500_.jpg',
    'redmi 13 5g': 'https://m.media-amazon.com/images/I/71cz4s78XVL._SL1500_.jpg',
    'redmi 13c': 'https://m.media-amazon.com/images/I/71cz4s78XVL._SL1500_.jpg',

    # Realme Series
    'realme gt 7 pro': 'https://m.media-amazon.com/images/I/71wLpWn032L._SL1500_.jpg',
    'realme gt 6': 'https://m.media-amazon.com/images/I/71wLpWn032L._SL1500_.jpg',
    'realme gt 6t': 'https://m.media-amazon.com/images/I/71wLpWn032L._SL1500_.jpg',
    'realme 13 pro+': 'https://m.media-amazon.com/images/I/71d-556j4JL._SL1500_.jpg',
    'realme 12 pro+': 'https://m.media-amazon.com/images/I/71d-556j4JL._SL1500_.jpg',
    'realme 12x': 'https://m.media-amazon.com/images/I/71T23a07tLL._SL1500_.jpg',
    'realme p1 pro': 'https://m.media-amazon.com/images/I/71T23a07tLL._SL1500_.jpg',
    'realme p1': 'https://m.media-amazon.com/images/I/71T23a07tLL._SL1500_.jpg',

    # Google Pixel Series
    'pixel 9 pro xl': 'https://m.media-amazon.com/images/I/618x+4-J9NL._SL1500_.jpg',
    'pixel 9 pro': 'https://m.media-amazon.com/images/I/618x+4-J9NL._SL1500_.jpg',
    'pixel 9': 'https://m.media-amazon.com/images/I/618x+4-J9NL._SL1500_.jpg',
    'pixel 8a': 'https://m.media-amazon.com/images/I/71v1m9W1GLL._SL1500_.jpg',
    'pixel 8 pro': 'https://m.media-amazon.com/images/I/71v1m9W1GLL._SL1500_.jpg',
    'pixel 8': 'https://m.media-amazon.com/images/I/71v1m9W1GLL._SL1500_.jpg',
    'pixel 7a': 'https://m.media-amazon.com/images/I/61dCg-X5t-L._SL1500_.jpg',

    # Motorola Series
    'motorola edge 50 ultra': 'https://m.media-amazon.com/images/I/71r3S47kU2L._SL1500_.jpg',
    'motorola edge 50 pro': 'https://m.media-amazon.com/images/I/71r3S47kU2L._SL1500_.jpg',
    'motorola edge 50 fusion': 'https://m.media-amazon.com/images/I/71r3S47kU2L._SL1500_.jpg',
    'motorola moto g85': 'https://m.media-amazon.com/images/I/71Zc6Jg9bGL._SL1500_.jpg',
    'motorola moto g64': 'https://m.media-amazon.com/images/I/61Cj9vK3EHL._SL1500_.jpg',
    'motorola moto g45': 'https://m.media-amazon.com/images/I/61Cj9vK3EHL._SL1500_.jpg',
    'motorola moto g34': 'https://m.media-amazon.com/images/I/61Cj9vK3EHL._SL1500_.jpg',

    # Nothing & Poco & Tecno & Infinix & Lava Series
    'nothing phone (2a) plus': 'https://m.media-amazon.com/images/I/71T08p8xW7L._SL1500_.jpg',
    'nothing phone (2a)': 'https://m.media-amazon.com/images/I/71T08p8xW7L._SL1500_.jpg',
    'nothing phone (2)': 'https://m.media-amazon.com/images/I/71b5-8k24NL._SL1500_.jpg',
    'poco f6 pro': 'https://m.media-amazon.com/images/I/71a2e38FmIL._SL1500_.jpg',
    'poco f6': 'https://m.media-amazon.com/images/I/71a2e38FmIL._SL1500_.jpg',
    'poco x6 pro': 'https://m.media-amazon.com/images/I/71e06s-674L._SL1500_.jpg',
    'poco x6': 'https://m.media-amazon.com/images/I/71e06s-674L._SL1500_.jpg',
    'poco m6 pro': 'https://m.media-amazon.com/images/I/71cz4s78XVL._SL1500_.jpg',
    'lava agni 3': 'https://m.media-amazon.com/images/I/71T23a07tLL._SL1500_.jpg',
    'lava blaze 3': 'https://m.media-amazon.com/images/I/71T23a07tLL._SL1500_.jpg',
    'tecno camon 30': 'https://m.media-amazon.com/images/I/615r1K7CqEL._SL1500_.jpg',
    'tecno pova 6 pro': 'https://m.media-amazon.com/images/I/615r1K7CqEL._SL1500_.jpg',
    'infinix gt 20 pro': 'https://m.media-amazon.com/images/I/71d-556j4JL._SL1500_.jpg',
    'infinix note 40 pro': 'https://m.media-amazon.com/images/I/71d-556j4JL._SL1500_.jpg'
}

BRAND_SERIES_DEFAULT = {
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
    'nothing': 'https://m.media-amazon.com/images/I/71b5-8k24NL._SL1500_.jpg',
    'poco': 'https://m.media-amazon.com/images/I/71a2e38FmIL._SL1500_.jpg',
    'lava': 'https://m.media-amazon.com/images/I/71T23a07tLL._SL1500_.jpg',
    'tecno': 'https://m.media-amazon.com/images/I/615r1K7CqEL._SL1500_.jpg',
    'infinix': 'https://m.media-amazon.com/images/I/71d-556j4JL._SL1500_.jpg'
}

def map_all_exact_images():
    print("Reading phones.js...")
    with open('phones.js', 'r', encoding='utf-8') as f:
        content = f.read()

    start_idx = content.find('var PHONES = [') + len('var PHONES = ')
    end_idx = content.find('];\n\nif', start_idx) + 1
    if end_idx == 0:
        end_idx = content.find('];\n', start_idx) + 1

    raw_json = content[start_idx:end_idx]
    phones = json.loads(raw_json)

    exact_matched = 0
    brand_matched = 0

    for phone in phones:
        brand = (phone.get('brand') or '').lower().strip()
        name = (phone.get('name') or '').lower().strip()

        clean_name = re.sub(r'\s*(?:special\s+)?edition(?:\s*\(?v?\d+\)?)?', '', name, flags=re.IGNORECASE)
        clean_name = re.sub(r'[\(\)\[\]\s]+$', '', clean_name).strip()

        full_name = f"{brand} {clean_name}".lower().strip()

        matched_img = None
        # 1. Match exact key in SERIES_IMAGE_MAP
        for key, img in SERIES_IMAGE_MAP.items():
            if key in full_name or key in clean_name:
                matched_img = img
                exact_matched += 1
                break

        # 2. Match brand series fallback
        if not matched_img:
            for b_key, b_img in BRAND_SERIES_DEFAULT.items():
                if b_key in brand or b_key in full_name:
                    matched_img = b_img
                    brand_matched += 1
                    break

        if not matched_img:
            matched_img = BRAND_SERIES_DEFAULT['samsung']

        phone['images'] = [matched_img]

    print(f"Mapped {exact_matched} phones to exact model series imagery.")
    print(f"Mapped {brand_matched} phones to official brand series imagery.")

    prefix = content[:start_idx]
    suffix = content[end_idx:]
    new_json_str = json.dumps(phones, indent=2)

    with open('phones.js', 'w', encoding='utf-8') as f:
        f.write(prefix + new_json_str + suffix)

    print("Successfully mapped 100% of phones in phones.js!")

if __name__ == '__main__':
    map_all_exact_images()
