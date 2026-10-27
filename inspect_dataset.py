import json

with open("phones.json", "r", encoding="utf-8") as f:
    phones = json.load(f)

print(f"Total phones in phones.json: {len(phones)}")

brands = {}
price_categories = {}
has_asin = 0
has_img = 0

for p in phones:
    b = p.get("brand", "Unknown")
    brands[b] = brands.get(b, 0) + 1
    cat = p.get("priceCategory", "Unknown")
    price_categories[cat] = price_categories.get(cat, 0) + 1
    if p.get("asin"):
        has_asin += 1
    if p.get("image") or p.get("images"):
        has_img += 1

print("Brands count:", len(brands))
print("Top 10 brands:", sorted(brands.items(), key=lambda x: x[1], reverse=True)[:10])
print("Price categories:", price_categories)
print(f"Phones with ASIN: {has_asin} / {len(phones)}")
print(f"Phones with Image: {has_img} / {len(phones)}")
