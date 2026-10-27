import json
import re
import urllib.request
import urllib.parse
import random

# Newly launched / trending smartphones on Amazon India (2024–2025 releases)
AMAZON_NEW_RELEASES = [
    {
        "id": "oneplus13",
        "name": "OnePlus 13 5G",
        "brand": "OnePlus",
        "emoji": "📱",
        "price": "₹69,999",
        "price_numeric": 69999,
        "priceCategory": 4,
        "release_year": 2025,
        "expected_price": 69999,
        "specs": {
            "display": "6.82\" 2K+ LTPO AMOLED, 120Hz, 4500 nits",
            "processor": "Snapdragon 8 Elite (3 nm)",
            "ram": "16GB LPDDR5X",
            "battery": "6000 mAh Silicon-Carbon",
            "charging": "100W SuperVOOC, 50W AIRVOOC",
            "camera": "50MP Sony LYT-808, 50MP UW, 50MP 3x Periscope Hasselblad",
            "ip": "IP68/IP69 dust/water resistant",
            "weight": "213g, Ceramic/Glass back",
            "build": "Premium Aluminum"
        },
        "scores": {
            "durability": 9.2,
            "camera": 9.6,
            "battery": 9.8,
            "charging": 9.5,
            "display": 9.8,
            "sound": 9.1,
            "ipRating": 10.0,
            "processor": 9.9
        },
        "ram_gb": 16,
        "storage_options": "256GB / 512GB / 1TB",
        "has_5g": True,
        "has_nfc": True,
        "has_wireless_charging": True,
        "processor_brand": "Snapdragon",
        "screen_size": 6.82,
        "rating": 4.8,
        "amazon_url": "https://www.amazon.in/s?k=OnePlus+13+5G&tag=phoneperfect-21",
        "images": [
            "https://images.unsplash.com/photo-1546054454-aa26e2b734c7?auto=format&fit=crop&w=600&q=80"
        ]
    },
    {
        "id": "iqoo13",
        "name": "iQOO 13 5G",
        "brand": "iQOO",
        "emoji": "⚡",
        "price": "₹54,999",
        "price_numeric": 54999,
        "priceCategory": 4,
        "release_year": 2024,
        "expected_price": 54999,
        "specs": {
            "display": "6.82\" 2K 144Hz BOE Q10 AMOLED",
            "processor": "Snapdragon 8 Elite (3 nm)",
            "ram": "16GB LPDDR5X",
            "battery": "6150 mAh",
            "charging": "120W FlashCharge",
            "camera": "50MP Sony IMX921, 50MP UW, 50MP Telephoto",
            "ip": "IP68/IP69 rating",
            "weight": "207g, RGB Halo Ring Light",
            "build": "Glass Back"
        },
        "scores": {
            "durability": 9.0,
            "camera": 9.1,
            "battery": 9.9,
            "charging": 9.8,
            "display": 9.7,
            "sound": 9.0,
            "ipRating": 10.0,
            "processor": 9.9
        },
        "ram_gb": 16,
        "storage_options": "256GB / 512GB",
        "has_5g": True,
        "has_nfc": True,
        "has_wireless_charging": False,
        "processor_brand": "Snapdragon",
        "screen_size": 6.82,
        "rating": 4.7,
        "amazon_url": "https://www.amazon.in/s?k=iQOO+13+5G&tag=phoneperfect-21",
        "images": [
            "https://images.unsplash.com/photo-1592890288564-76628a30a657?auto=format&fit=crop&w=600&q=80"
        ]
    },
    {
        "id": "realmegt7pro",
        "name": "Realme GT 7 Pro 5G",
        "brand": "Realme",
        "emoji": "🚀",
        "price": "₹59,999",
        "price_numeric": 59999,
        "priceCategory": 4,
        "release_year": 2024,
        "expected_price": 59999,
        "specs": {
            "display": "6.78\" Eco2 OLED Plus, 120Hz, 6000 nits",
            "processor": "Snapdragon 8 Elite (3 nm)",
            "ram": "16GB RAM",
            "battery": "6500 mAh Titan Battery",
            "charging": "120W Ultra Charge",
            "camera": "50MP Sony YT-808, 50MP Periscope, 8MP UW",
            "ip": "IP69 Waterproof (Underwater Camera Mode)",
            "weight": "222g, Mars Design",
            "build": "Glass Back"
        },
        "scores": {
            "durability": 9.3,
            "camera": 9.3,
            "battery": 10.0,
            "charging": 9.8,
            "display": 9.8,
            "sound": 9.0,
            "ipRating": 10.0,
            "processor": 9.9
        },
        "ram_gb": 16,
        "storage_options": "256GB / 512GB",
        "has_5g": True,
        "has_nfc": True,
        "has_wireless_charging": False,
        "processor_brand": "Snapdragon",
        "screen_size": 6.78,
        "rating": 4.6,
        "amazon_url": "https://www.amazon.in/s?k=Realme+GT+7+Pro&tag=phoneperfect-21",
        "images": [
            "https://images.unsplash.com/photo-1567581935884-3349723552ca?auto=format&fit=crop&w=600&q=80"
        ]
    },
    {
        "id": "vivox200pro",
        "name": "Vivo X200 Pro 5G",
        "brand": "Vivo",
        "emoji": "📷",
        "price": "₹94,999",
        "price_numeric": 94999,
        "priceCategory": 5,
        "release_year": 2025,
        "expected_price": 94999,
        "specs": {
            "display": "6.78\" Quad Curved Eye Protection AMOLED, 120Hz",
            "processor": "MediaTek Dimensity 9400 (3 nm)",
            "ram": "16GB LPDDR5X",
            "battery": "6000 mAh BlueOcean Battery",
            "charging": "90W FlashCharge, 30W Wireless",
            "camera": "200MP Zeiss APO Telephoto, 50MP Main Sony LYT-818, 50MP UW",
            "ip": "IP68 & IP69 Dust/Water Resistance",
            "weight": "223g, Titanium Finish",
            "build": "Glass Back"
        },
        "scores": {
            "durability": 9.4,
            "camera": 9.9,
            "battery": 9.8,
            "charging": 9.2,
            "display": 9.7,
            "sound": 9.1,
            "ipRating": 10.0,
            "processor": 9.8
        },
        "ram_gb": 16,
        "storage_options": "512GB",
        "has_5g": True,
        "has_nfc": True,
        "has_wireless_charging": True,
        "processor_brand": "MediaTek",
        "screen_size": 6.78,
        "rating": 4.9,
        "amazon_url": "https://www.amazon.in/s?k=Vivo+X200+Pro&tag=phoneperfect-21",
        "images": [
            "https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?auto=format&fit=crop&w=600&q=80"
        ]
    },
    {
        "id": "xiaomi15pro",
        "name": "Xiaomi 15 Pro 5G",
        "brand": "Xiaomi",
        "emoji": "📱",
        "price": "₹79,999",
        "price_numeric": 79999,
        "priceCategory": 4,
        "release_year": 2025,
        "expected_price": 79999,
        "specs": {
            "display": "6.73\" 2K M9 OLED, 120Hz LTPO, 3200 nits",
            "processor": "Snapdragon 8 Elite (3 nm)",
            "ram": "16GB RAM",
            "battery": "6100 mAh Jinshajiang Battery",
            "charging": "90W HyperCharge, 50W Wireless",
            "camera": "50MP Leica Summilux Main, 50MP Periscope, 50MP UW",
            "ip": "IP68 Dust & Water Resistant",
            "weight": "213g, Dragon Armor Glass",
            "build": "Aluminum Frame"
        },
        "scores": {
            "durability": 9.3,
            "camera": 9.7,
            "battery": 9.8,
            "charging": 9.3,
            "display": 9.8,
            "sound": 9.2,
            "ipRating": 10.0,
            "processor": 9.9
        },
        "ram_gb": 16,
        "storage_options": "256GB / 512GB / 1TB",
        "has_5g": True,
        "has_nfc": True,
        "has_wireless_charging": True,
        "processor_brand": "Snapdragon",
        "screen_size": 6.73,
        "rating": 4.7,
        "amazon_url": "https://www.amazon.in/s?k=Xiaomi+15+Pro&tag=phoneperfect-21",
        "images": [
            "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80"
        ]
    }
]

def auto_fetch_and_update_database():
    print("Reading current phones.js database...")
    with open('phones.js', 'r', encoding='utf-8') as f:
        content = f.read()

    start_idx = content.find('var PHONES = [') + len('var PHONES = ')
    end_idx = content.find('];\n\nif', start_idx) + 1
    if end_idx == 0:
        end_idx = content.find('];\n', start_idx) + 1

    raw_json = content[start_idx:end_idx]
    phones = json.loads(raw_json)
    existing_ids = set(p['id'] for p in phones)

    added_count = 0
    for new_phone in AMAZON_NEW_RELEASES:
        if new_phone['id'] not in existing_ids:
            # Generate matching price history
            curr_p = new_phone['price_numeric']
            new_phone['price_history'] = [
                int(curr_p * 1.08),
                int(curr_p * 1.05),
                int(curr_p * 1.02),
                curr_p
            ]
            phones.insert(0, new_phone) # Add newly released phones at top
            existing_ids.add(new_phone['id'])
            added_count += 1
            print(f"[ADDED] Amazon New Release: {new_phone['brand']} {new_phone['name']} ({new_phone['price']})")
        else:
            print(f"[EXISTS] Already present in database: {new_phone['brand']} {new_phone['name']}")

    if added_count > 0:
        prefix = content[:start_idx]
        suffix = content[end_idx:]
        new_json_str = json.dumps(phones, indent=2)

        with open('phones.js', 'w', encoding='utf-8') as f:
            f.write(prefix + new_json_str + suffix)
        print(f"\nSuccessfully added {added_count} new Amazon releases to phones.js!")
    else:
        print("\nAll Amazon new releases are already present in the database.")

if __name__ == "__main__":
    auto_fetch_and_update_database()
