import json

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

    print(f"Total phones before filtering: {len(phones)}")

    # Filter out outdated phones (keep release_year >= 2023)
    active_phones = [p for p in phones if p.get('release_year', 2024) >= 2023]

    # Sort active phones: newest release year first, then by price
    active_phones.sort(key=lambda p: (p.get('release_year', 2024), p.get('price_numeric', 0)), reverse=True)

    print(f"[SUCCESS] Filtered out {len(phones) - len(active_phones)} outdated phones.")
    print(f"[RETAINED] {len(active_phones)} active modern smartphones (2023–2026 active market lineup).")

    # Update phones.js file
    prefix = content[:start_idx]
    suffix = content[end_idx:]
    new_json_str = json.dumps(active_phones, indent=2)

    with open('phones.js', 'w', encoding='utf-8') as f:
        f.write(prefix + new_json_str + suffix)

    print("[DONE] phones.js successfully updated with active market phones!")

if __name__ == "__main__":
    run()
