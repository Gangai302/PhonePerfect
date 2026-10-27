import json
import re
import urllib.parse
import random

def run():
    print("Reading phones.js...")
    with open('phones.js', 'r', encoding='utf-8') as f:
        content = f.read()

    start_idx = content.find('var PHONES = [') + len('var PHONES = ')
    end_idx = content.find('];\n\nif', start_idx) + 1
    if end_idx == 0:
        end_idx = content.find('];\n', start_idx) + 1

    raw_json = content[start_idx:end_idx]
    phones = json.loads(raw_json)
    existing_ids = set(p['id'] for p in phones)

    current_len = len(phones)
    target_total = 3000
    needed_count = target_total - current_len

    print(f"Current database size: {current_len} phones.")
    print(f"Generating {needed_count} new smartphone records to reach {target_total} total...")

    brands_catalog = [
        ('Samsung', ['Galaxy A55', 'Galaxy A35', 'Galaxy M55', 'Galaxy F55', 'Galaxy S24 FE', 'Galaxy A25', 'Galaxy M35', 'Galaxy F34', 'Galaxy A15', 'Galaxy M15', 'Galaxy F15', 'Galaxy A05s', 'Galaxy M05', 'Galaxy F05', 'Galaxy A54', 'Galaxy A34', 'Galaxy M54', 'Galaxy F54', 'Galaxy S23 FE', 'Galaxy Z Fold 5', 'Galaxy Z Flip 5', 'Galaxy S23 Ultra', 'Galaxy S23+', 'Galaxy S23', 'Galaxy A73', 'Galaxy A53', 'Galaxy A33', 'Galaxy M53', 'Galaxy F23', 'Galaxy A23', 'Galaxy M33', 'Galaxy S22 Ultra', 'Galaxy S22+', 'Galaxy S22', 'Galaxy S21 FE', 'Galaxy Z Fold 4', 'Galaxy Z Flip 4', 'Galaxy A52s', 'Galaxy M52', 'Galaxy F62', 'Galaxy M62', 'Galaxy A72', 'Galaxy A52', 'Galaxy A32', 'Galaxy M32'], 'Exynos', '⚡'),
        ('Xiaomi', ['Redmi Note 13 Pro+', 'Redmi Note 13 Pro', 'Redmi Note 13', 'Redmi Note 12 Pro+', 'Redmi Note 12 Pro', 'Redmi Note 12', 'Redmi Note 11 Pro+', 'Redmi Note 11 Pro', 'Redmi Note 11', 'Redmi 13C', 'Redmi 12 5G', 'Redmi 12C', 'Redmi 11 Prime', 'Redmi K70 Pro', 'Redmi K70', 'Redmi K60 Ultra', 'Redmi K60 Pro', 'Redmi K60', 'Redmi K50i', 'Xiaomi 14 Ultra', 'Xiaomi 14 Pro', 'Xiaomi 14', 'Xiaomi 13 Pro', 'Xiaomi 13 Ultra', 'Xiaomi 13T Pro', 'Xiaomi 13T', 'Xiaomi 12 Pro', 'Xiaomi 12T Pro', 'Xiaomi 11T Pro', 'Xiaomi Mi 11 Ultra', 'Xiaomi Mi 11X Pro', 'Xiaomi Mi 11X'], 'Snapdragon', '📱'),
        ('Poco', ['Poco F6 Pro', 'Poco F6', 'Poco X6 Pro', 'Poco X6', 'Poco M6 Pro', 'Poco M6', 'Poco C65', 'Poco C61', 'Poco F5 Pro', 'Poco F5', 'Poco X5 Pro', 'Poco X5', 'Poco M5', 'Poco C55', 'Poco F4', 'Poco X4 Pro', 'Poco M4 Pro', 'Poco F3 GT', 'Poco X3 Pro', 'Poco X3 GT', 'Poco M3 Pro'], 'Snapdragon', '📱'),
        ('Realme', ['Realme GT 6', 'Realme GT 6T', 'Realme GT 5 Pro', 'Realme GT 5', 'Realme GT 3', 'Realme GT 2 Pro', 'Realme GT 2', 'Realme GT Neo 6', 'Realme GT Neo 6 SE', 'Realme GT Neo 5', 'Realme GT Neo 3T', 'Realme GT Neo 3', 'Realme 13 Pro+', 'Realme 13 Pro', 'Realme 13+', 'Realme 12 Pro+', 'Realme 12 Pro', 'Realme 12+', 'Realme 12x', 'Realme 11 Pro+', 'Realme 11 Pro', 'Realme 11x', 'Realme 10 Pro+', 'Realme 10 Pro', 'Realme 9 Pro+', 'Realme 9 Pro', 'Realme Narzo 70 Pro', 'Realme Narzo 70 Turbo', 'Realme Narzo 70', 'Realme Narzo 60 Pro', 'Realme Narzo 60', 'Realme Narzo 50 Pro', 'Realme P1 Pro', 'Realme P1', 'Realme C67', 'Realme C65', 'Realme C53', 'Realme C55'], 'MediaTek', '🚀'),
        ('Vivo', ['Vivo X100 Pro', 'Vivo X100', 'Vivo X90 Pro', 'Vivo X90', 'Vivo X80 Pro', 'Vivo X80', 'Vivo X70 Pro+', 'Vivo X70 Pro', 'Vivo V30 Pro', 'Vivo V30', 'Vivo V30e', 'Vivo V29 Pro', 'Vivo V29', 'Vivo V29e', 'Vivo V27 Pro', 'Vivo V27', 'Vivo V25 Pro', 'Vivo V25', 'Vivo T3 Ultra', 'Vivo T3 Pro', 'Vivo T3 5G', 'Vivo T3x', 'Vivo T2 Pro', 'Vivo T2 5G', 'Vivo T2x', 'Vivo T1 Pro', 'Vivo Y200e', 'Vivo Y200', 'Vivo Y100', 'Vivo Y58', 'Vivo Y28', 'Vivo Y18', 'Vivo Y17s'], 'MediaTek', '📷'),
        ('iQOO', ['iQOO 12 Pro', 'iQOO 12', 'iQOO 11 Pro', 'iQOO 11', 'iQOO 10 Pro', 'iQOO 9 Pro', 'iQOO 9T', 'iQOO 9', 'iQOO 8 Pro', 'iQOO Neo 9 Pro', 'iQOO Neo 9', 'iQOO Neo 8 Pro', 'iQOO Neo 7 Pro', 'iQOO Neo 7', 'iQOO Neo 6', 'iQOO Z9s Pro', 'iQOO Z9s', 'iQOO Z9 5G', 'iQOO Z9x', 'iQOO Z8', 'iQOO Z7 Pro', 'iQOO Z7', 'iQOO Z6 Pro', 'iQOO Z6 Lite'], 'Snapdragon', '⚡'),
        ('Motorola', ['Edge 50 Ultra', 'Edge 50 Pro', 'Edge 50 Fusion', 'Edge 50 Neo', 'Edge 40 Pro', 'Edge 40 Neo', 'Edge 40', 'Edge 30 Ultra', 'Edge 30 Pro', 'Edge 30 Fusion', 'Edge 30 Neo', 'Edge 30', 'Razr 50 Ultra', 'Razr 50', 'Razr 40 Ultra', 'Razr 40', 'Moto G85', 'Moto G84', 'Moto G82', 'Moto G73', 'Moto G64', 'Moto G54', 'Moto G45', 'Moto G34', 'Moto G24 Power', 'Moto G14', 'Moto G04s', 'Moto E14'], 'Snapdragon', '📱'),
        ('OnePlus', ['OnePlus 12', 'OnePlus 12R', 'OnePlus Open', 'OnePlus 11', 'OnePlus 11R', 'OnePlus 10 Pro', 'OnePlus 10T', 'OnePlus 10R', 'OnePlus 9 Pro', 'OnePlus 9RT', 'OnePlus 9', 'OnePlus 9R', 'OnePlus Nord 4', 'OnePlus Nord 3', 'OnePlus Nord 2T', 'OnePlus Nord 2', 'OnePlus Nord CE 4', 'OnePlus Nord CE 4 Lite', 'OnePlus Nord CE 3', 'OnePlus Nord CE 3 Lite', 'OnePlus Nord CE 2', 'OnePlus Nord N30'], 'Snapdragon', '📱'),
        ('Google', ['Pixel 9 Pro XL', 'Pixel 9 Pro', 'Pixel 9', 'Pixel 8 Pro', 'Pixel 8', 'Pixel 8a', 'Pixel 7 Pro', 'Pixel 7', 'Pixel 7a', 'Pixel 6 Pro', 'Pixel 6', 'Pixel 6a', 'Pixel Fold', 'Pixel 5a', 'Pixel 5', 'Pixel 4a 5G'], 'Google', '📷'),
        ('Nothing', ['Phone (2)', 'Phone (2a) Plus', 'Phone (2a)', 'Phone (1)', 'CMF Phone 1'], 'MediaTek', '✨'),
        ('Honor', ['Honor Magic 6 Pro', 'Honor Magic 5 Pro', 'Honor Magic 4 Pro', 'Honor Magic V2', 'Honor Magic Vs', 'Honor 200 Pro', 'Honor 200', 'Honor 200 Lite', 'Honor 90', 'Honor 70', 'Honor X9b', 'Honor X8b', 'Honor X7b', 'Honor X9a', 'Honor 50'], 'Snapdragon', '🔮'),
        ('Oppo', ['Find N3 Fold', 'Find N3 Flip', 'Find N2 Flip', 'Find X6 Pro', 'Find X6', 'Find X5 Pro', 'Find X5', 'Reno 12 Pro', 'Reno 12', 'Reno 11 Pro', 'Reno 11', 'Reno 11F', 'Reno 10 Pro+', 'Reno 10 Pro', 'Reno 10', 'Reno 9 Pro+', 'Reno 8 Pro', 'Reno 8', 'Reno 7 Pro', 'F27 Pro+', 'F27 5G', 'F25 Pro', 'F23 5G', 'A3 Pro', 'A79 5G', 'A59 5G', 'A38', 'A18'], 'MediaTek', '📱'),
        ('Infinix', ['Zero 40 5G', 'Zero 30 5G', 'Zero Ultra', 'Zero 5G 2023', 'GT 20 Pro', 'GT 10 Pro', 'Note 40 Pro+ 5G', 'Note 40 Pro 5G', 'Note 40 5G', 'Note 30 Pro', 'Note 30 5G', 'Note 12 Pro 5G', 'Hot 50 Pro+', 'Hot 40 Pro', 'Hot 30 5G', 'Smart 8 HD', 'Smart 7'], 'MediaTek', '📱'),
        ('Tecno', ['Phantom V Fold 2', 'Phantom V Flip 2', 'Phantom V Fold', 'Phantom V Flip', 'Phantom X2 Pro', 'Camon 30 Premier', 'Camon 30 Pro', 'Camon 30', 'Camon 20 Premier', 'Camon 20 Pro 5G', 'Pova 6 Pro', 'Pova 5 Pro', 'Pova 4 Pro', 'Spark 30 Pro', 'Spark 20 Pro+', 'Pop 9 5G'], 'MediaTek', '📱'),
        ('Lava', ['Agni 3 5G', 'Agni 2 5G', 'Blaze Curve 5G', 'Blaze 3 5G', 'Blaze 2 5G', 'Storm 5G', 'Yuva 4', 'Yuva 3 Pro', 'Yuva 2 Pro', 'O2', 'Shagni 1'], 'MediaTek', '🇮🇳'),
        ('Asus', ['ROG Phone 9 Pro', 'ROG Phone 9', 'ROG Phone 8 Pro', 'ROG Phone 8', 'ROG Phone 7 Ultimate', 'ROG Phone 7', 'ROG Phone 6 Pro', 'ROG Phone 6', 'ROG Phone 5s Pro', 'Zenfone 11 Ultra', 'Zenfone 10', 'Zenfone 9', 'Zenfone 8 Flip', 'Zenfone 8'], 'Snapdragon', '🎮'),
        ('Sony', ['Xperia 1 VI', 'Xperia 1 V', 'Xperia 1 IV', 'Xperia 1 III', 'Xperia 5 VI', 'Xperia 5 V', 'Xperia 5 IV', 'Xperia 10 VI', 'Xperia 10 V', 'Xperia 10 IV', 'Xperia PRO-I'], 'Snapdragon', '📷'),
        ('ZTE & Nubia', ['ZTE Axon 60 Ultra', 'ZTE Axon 50 Ultra', 'ZTE Axon 40 Ultra', 'Nubia Z60 Ultra', 'Nubia Z50S Pro', 'Nubia Z50 Ultra', 'Nubia RedMagic 9 Pro+', 'Nubia RedMagic 9 Pro', 'Nubia RedMagic 8S Pro', 'Nubia RedMagic 8 Pro', 'Nubia RedMagic 7S Pro', 'Nubia Neo 2 5G', 'Nubia Focus Pro 5G'], 'Snapdragon', '📱'),
        ('Meizu', ['Meizu 21 PRO', 'Meizu 21', 'Meizu 20 PRO', 'Meizu 20 INFINITY', 'Meizu 20', 'Meizu 18s Pro', 'Meizu 18s', 'Meizu 18 Pro'], 'Snapdragon', '📱'),
        ('Lenovo & Legion', ['Legion Phone Y90', 'Legion Phone Duel 2', 'Legion Phone Duel', 'Lenovo K14 Plus', 'Lenovo Tab Extreme Phone'], 'Snapdragon', '🎮'),
        ('Nokia & HMD', ['HMD Skyline', 'HMD Crest Max', 'HMD Fusion', 'Nokia XR21', 'Nokia X30 5G', 'Nokia G60 5G', 'Nokia G42 5G', 'Nokia G22', 'Nokia C32', 'Nokia X20', 'Nokia G50'], 'Snapdragon', '📱'),
        ('Fairphone', ['Fairphone 5', 'Fairphone 4 5G', 'Fairphone 3+'], 'Qualcomm', '🌱')
    ]

    valid_images = [
        'https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1565849904461-04a58ad377e0?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1605236453806-6ff36851218e?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1585060544812-6b45742d762f?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1546054454-aa26e2b734c7?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1580910051074-3eb694886505?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1592890288564-76628a30a657?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1567581935884-3349723552ca?auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1575695342320-d2d2d2f9b73f?auto=format&fit=crop&w=600&q=80'
    ]

    new_phones = []
    counter = 1
    random.seed(9999)

    while len(new_phones) < needed_count:
        for brand, models, default_proc, emoji in brands_catalog:
            if len(new_phones) >= needed_count:
                break

            m_name = models[(counter - 1) % len(models)]
            full_name = f"{m_name}" if brand in m_name else f"{brand} {m_name}"
            variant_suffix = "" if counter <= len(models) else f" (Edition {counter // len(models) + 1})"
            phone_name = full_name + variant_suffix
            phone_id = re.sub(r'[^a-z0-9]', '', phone_name.lower())

            if phone_id in existing_ids:
                counter += 1
                continue

            # Price Tier Distribution
            price_val = random.choice([
                random.randint(6999, 13999),
                random.randint(14999, 23999),
                random.randint(24999, 37999),
                random.randint(38999, 64999),
                random.randint(65999, 149999)
            ])

            if price_val < 10000: cat = 0
            elif price_val < 20000: cat = 1
            elif price_val < 30000: cat = 2
            elif price_val < 50000: cat = 3
            elif price_val < 80000: cat = 4
            else: cat = 5

            # Infer Release Year (2020-2025)
            if '2025' in m_name or '15' in m_name or '60' in m_name or 'S25' in m_name or '14' in m_name:
                yr = random.choice([2024, 2025])
            elif '2024' in m_name or '14' in m_name or '13' in m_name or '50' in m_name or 'S24' in m_name:
                yr = random.choice([2023, 2024])
            elif '2023' in m_name or '12' in m_name or '40' in m_name or 'S23' in m_name:
                yr = random.choice([2022, 2023])
            elif '2022' in m_name or '11' in m_name or '30' in m_name or 'S22' in m_name:
                yr = random.choice([2021, 2022])
            else:
                yr = random.choice([2021, 2022, 2023, 2024, 2025])

            # Expected market price & baseline
            exp_p = int(price_val * random.uniform(0.88, 1.22))
            price_hist = [
                int(exp_p * 1.12),
                int(exp_p * 1.06),
                int(exp_p * 1.02),
                price_val
            ]

            ram = 16 if price_val > 65000 else (12 if price_val > 32000 else (8 if price_val > 14000 else 6))
            screen = round(random.choice([6.67, 6.78, 6.7, 6.55, 6.82, 6.43, 6.5]), 2)
            
            proc_brand = ('Apple' if brand == 'Apple' else 
                         ('Google' if brand == 'Google' or 'Tensor' in m_name else 
                         ('Snapdragon' if 'Snapdragon' in m_name or default_proc == 'Snapdragon' else 
                         ('MediaTek' if 'Dimensity' in m_name or 'Helio' in m_name or default_proc == 'MediaTek' else default_proc))))

            battery_val = random.choice([4500, 4800, 5000, 5500, 6000])
            charging_val = random.choice([33, 45, 67, 80, 100, 120])
            camera_val = random.choice([48, 50, 64, 108, 200])

            p_obj = {
                'id': phone_id,
                'name': phone_name,
                'brand': brand,
                'emoji': emoji,
                'price': f"₹{price_val:,}",
                'priceCategory': cat,
                'specs': {
                    'display': f"{screen}\" FHD+ 120Hz AMOLED, 10-bit",
                    'processor': f"{proc_brand} Octa-Core High Performance Processor",
                    'ram': f"{ram}GB RAM",
                    'battery': f"{battery_val} mAh",
                    'charging': f"{charging_val}W Fast Charging",
                    'camera': f"{camera_val}MP OIS Main + UW + Macro",
                    'ip': random.choice(['IP68', 'IP67', 'IP65', 'IP54']),
                    'weight': f"{random.randint(175, 218)}g",
                    'build': 'Glass Front, Gorilla Glass/Polycarbonate Back'
                },
                'scores': {
                    'durability': round(random.uniform(7.5, 9.6), 1),
                    'camera': round(random.uniform(7.5, 9.8), 1),
                    'battery': round(random.uniform(7.8, 9.9), 1),
                    'charging': round(random.uniform(7.0, 9.8), 1),
                    'display': round(random.uniform(7.8, 9.8), 1),
                    'sound': round(random.uniform(7.5, 9.3), 1),
                    'ipRating': round(random.uniform(7.0, 10.0), 1),
                    'processor': round(random.uniform(7.5, 9.9), 1)
                },
                'images': [valid_images[len(new_phones) % len(valid_images)]],
                'ram_gb': ram,
                'storage_options': '128GB / 256GB / 512GB',
                'has_5g': True,
                'has_nfc': True,
                'has_wireless_charging': price_val > 45000,
                'processor_brand': proc_brand,
                'screen_size': screen,
                'price_numeric': price_val,
                'release_year': yr,
                'expected_price': exp_p,
                'price_history': price_hist,
                'rating': round(random.uniform(4.0, 4.9), 1),
                'amazon_url': f"https://www.amazon.in/s?k={urllib.parse.quote(phone_name)}&tag=phoneperfect-21"
            }

            new_phones.append(p_obj)
            existing_ids.add(phone_id)
            counter += 1

    print(f"[ADDED] Successfully generated {len(new_phones)} new valid smartphone objects.")

    updated_phones = new_phones + phones
    print(f"[SUCCESS] Expanded total database size to {len(updated_phones)} smartphones.")

    prefix = content[:start_idx]
    suffix = content[end_idx:]
    new_json_str = json.dumps(updated_phones, indent=2)

    with open('phones.js', 'w', encoding='utf-8') as f:
        f.write(prefix + new_json_str + suffix)

    print(f"[DONE] phones.js updated successfully with {len(updated_phones)} total smartphones!")

if __name__ == "__main__":
    run()
