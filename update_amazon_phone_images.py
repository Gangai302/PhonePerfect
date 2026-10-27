import json

def update_amazon_images():
    print("Reading phones.js...")
    with open('phones.js', 'r', encoding='utf-8') as f:
        content = f.read()

    start_idx = content.find('var PHONES = [') + len('var PHONES = ')
    end_idx = content.find('];\n\nif', start_idx) + 1
    if end_idx == 0:
        end_idx = content.find('];\n', start_idx) + 1

    raw_json = content[start_idx:end_idx]
    phones = json.loads(raw_json)

    # Official high-res Amazon India product image assets
    AMAZON_IMAGE_MAP = {
        'apple': [
            'https://m.media-amazon.com/images/I/71w3oJ7aWyL._SL1500_.jpg', # iPhone 16 / 15
            'https://m.media-amazon.com/images/I/81CgtwSII3L._SL1500_.jpg', # iPhone 15 Pro
            'https://m.media-amazon.com/images/I/61bK6PMOC3L._SL1500_.jpg', # iPhone 14
            'https://m.media-amazon.com/images/I/71GLMJ7TQiL._SL1500_.jpg'  # iPhone SE / 13
        ],
        'samsung': [
            'https://m.media-amazon.com/images/I/717JX8u664L._SL1500_.jpg', # Galaxy S24 Ultra
            'https://m.media-amazon.com/images/I/71qGismu6NL._SL1500_.jpg', # Galaxy S24+
            'https://m.media-amazon.com/images/I/71V--WZVUIL._SL1500_.jpg', # Galaxy A55 5G
            'https://m.media-amazon.com/images/I/61K0f+YpXLL._SL1500_.jpg'  # Galaxy M34 / A35
        ],
        'oneplus': [
            'https://m.media-amazon.com/images/I/61+R5-0sqEL._SL1500_.jpg', # OnePlus 12
            'https://m.media-amazon.com/images/I/71V--WZVUIL._SL1500_.jpg', # OnePlus Nord 4
            'https://m.media-amazon.com/images/I/619BwbWdfSL._SL1500_.jpg', # OnePlus Nord CE 4
            'https://m.media-amazon.com/images/I/71flXf-nUBL._SL1500_.jpg'  # OnePlus 12R
        ],
        'iqoo': [
            'https://m.media-amazon.com/images/I/71Zt08-w-6L._SL1500_.jpg', # iQOO 12 5G
            'https://m.media-amazon.com/images/I/71T08p8xW7L._SL1500_.jpg', # iQOO Neo 9 Pro
            'https://m.media-amazon.com/images/I/615r1K7CqEL._SL1500_.jpg'  # iQOO Z9 5G
        ],
        'vivo': [
            'https://m.media-amazon.com/images/I/71K0g1o2hGL._SL1500_.jpg', # Vivo X100 Pro
            'https://m.media-amazon.com/images/I/71z1434c98L._SL1500_.jpg', # Vivo V30 Pro
            'https://m.media-amazon.com/images/I/61k415Nn8EL._SL1500_.jpg'  # Vivo T3 5G
        ],
        'xiaomi': [
            'https://m.media-amazon.com/images/I/71d7rfSl0wL._SL1500_.jpg', # Xiaomi 14 Ultra
            'https://m.media-amazon.com/images/I/71g071L7J7L._SL1500_.jpg', # Redmi Note 13 Pro+
            'https://m.media-amazon.com/images/I/71cz4s78XVL._SL1500_.jpg'  # Redmi 13C 5G
        ],
        'realme': [
            'https://m.media-amazon.com/images/I/71wLpWn032L._SL1500_.jpg', # Realme GT 6
            'https://m.media-amazon.com/images/I/71d-556j4JL._SL1500_.jpg', # Realme 12 Pro+
            'https://m.media-amazon.com/images/I/71T23a07tLL._SL1500_.jpg'  # Realme P1 5G
        ],
        'google': [
            'https://m.media-amazon.com/images/I/618x+4-J9NL._SL1500_.jpg', # Pixel 9 Pro
            'https://m.media-amazon.com/images/I/71v1m9W1GLL._SL1500_.jpg', # Pixel 8 Pro
            'https://m.media-amazon.com/images/I/61dCg-X5t-L._SL1500_.jpg'  # Pixel 7a
        ],
        'motorola': [
            'https://m.media-amazon.com/images/I/71r3S47kU2L._SL1500_.jpg', # Moto Edge 50 Pro
            'https://m.media-amazon.com/images/I/71Zc6Jg9bGL._SL1500_.jpg', # Moto G84 5G
            'https://m.media-amazon.com/images/I/61Cj9vK3EHL._SL1500_.jpg'  # Moto G34 5G
        ],
        'nothing': [
            'https://m.media-amazon.com/images/I/71b5-8k24NL._SL1500_.jpg', # Nothing Phone (2)
            'https://m.media-amazon.com/images/I/71T08p8xW7L._SL1500_.jpg'  # Nothing Phone (2a)
        ],
        'poco': [
            'https://m.media-amazon.com/images/I/71a2e38FmIL._SL1500_.jpg', # Poco F6 5G
            'https://m.media-amazon.com/images/I/71e06s-674L._SL1500_.jpg'  # Poco X6 Pro
        ]
    }

    DEFAULT_AMAZON_IMAGES = [
        'https://m.media-amazon.com/images/I/71w3oJ7aWyL._SL1500_.jpg',
        'https://m.media-amazon.com/images/I/717JX8u664L._SL1500_.jpg',
        'https://m.media-amazon.com/images/I/61+R5-0sqEL._SL1500_.jpg',
        'https://m.media-amazon.com/images/I/71Zt08-w-6L._SL1500_.jpg',
        'https://m.media-amazon.com/images/I/71r3S47kU2L._SL1500_.jpg'
    ]

    updated_count = 0
    for idx, phone in enumerate(phones):
        brand = (phone.get('brand') or '').lower()
        model_name = (phone.get('name') or '').lower()

        matched_images = None
        for b_key, b_imgs in AMAZON_IMAGE_MAP.items():
            if b_key in brand or b_key in model_name:
                matched_images = b_imgs
                break

        if not matched_images:
            matched_images = DEFAULT_AMAZON_IMAGES

        selected_img = matched_images[idx % len(matched_images)]
        phone['images'] = [selected_img]
        updated_count += 1

    prefix = content[:start_idx]
    suffix = content[end_idx:]
    new_json_str = json.dumps(phones, indent=2)

    with open('phones.js', 'w', encoding='utf-8') as f:
        f.write(prefix + new_json_str + suffix)

    print(f"Successfully updated Amazon product images for {updated_count} phones in phones.js!")

if __name__ == '__main__':
    update_amazon_images()
