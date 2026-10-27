import re
import json
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def get_clean_phone_name(raw_name):
    if not raw_name or not isinstance(raw_name, str):
        return ''
    cleaned = re.sub(r'\s*(?:special\s+)?edition(?:\s*\(?v?\d+\)?)?', '', raw_name, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s*\(?v\d+\)?$', '', cleaned, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', cleaned).strip()

def get_phone_full_name(brand, name):
    brand = (brand or '').strip()
    clean_name = get_clean_phone_name(name)
    if not brand:
        return clean_name
    if clean_name.lower().startswith(brand.lower()):
        return clean_name
    return f"{brand} {clean_name}".strip()

def get_phone_numeric_price(price, price_numeric=None):
    if price_numeric is not None:
        try:
            val = float(price_numeric)
            if val > 0:
                return int(round(val))
        except (ValueError, TypeError):
            pass
    if price is None:
        return 0
    if isinstance(price, (int, float)) and price > 0:
        return int(round(price))
    s = str(price).replace(',', '').replace('₹', '').replace('INR', '').replace('.00', '').strip()
    m = re.search(r'\d+', s)
    return int(m.group(0)) if m else 0

def is_phone_in_budget(price_val, budget_cat):
    p = price_val
    if p <= 0:
        return False
    if budget_cat in ('under-10000', 0):
        return p < 10000
    elif budget_cat in ('10000-20000', 1):
        return 10000 <= p <= 20000
    elif budget_cat in ('20000-30000', 2):
        return 20000 <= p <= 30000
    elif budget_cat in ('30000-50000', 3):
        return 30000 <= p <= 50000
    elif budget_cat in ('50000-80000', 4):
        return 50000 <= p <= 80000
    elif budget_cat in ('above-80000', 5):
        return p > 80000
    return True

def run_tests():
    print("====================================================")
    print("RUNNING BUDGET FILTERING & PRICE NORMALIZATION TESTS")
    print("====================================================")
    
    # 1. Price Normalization
    price_tests = [
        ("₹24,999", 24999),
        ("24999", 24999),
        ("₹24,999.00", 24999),
        ("24,999", 24999),
        (24999, 24999),
        ("₹20,000", 20000),
        ("₹30,000", 30000)
    ]
    price_passed = 0
    for raw, expected in price_tests:
        res = get_phone_numeric_price(raw)
        status = "PASSED" if res == expected else f"FAILED (got {res})"
        if res == expected:
            price_passed += 1
        print(f"Price '{raw}' -> {res} | {status}")
    print(f"Price Normalization: {price_passed}/{len(price_tests)} passed.\n")

    # 2. Budget Range Hard Filter Test for ₹20,000 – ₹30,000
    print("--- Test Range: ₹20,000 – ₹30,000 ---")
    budget_test_cases = [
        (18999, False, "REMOVE"),
        (19999, False, "REMOVE"),
        (20000, True, "ALLOW"),
        (22999, True, "ALLOW"),
        (25999, True, "ALLOW"),
        (29999, True, "ALLOW"),
        (30000, True, "ALLOW"),
        (30999, False, "REMOVE"),
        (35999, False, "REMOVE"),
        (49999, False, "REMOVE"),
        (79999, False, "REMOVE"),
    ]
    
    b2030_passed = 0
    for price, expected_allowed, action_str in budget_test_cases:
        allowed = is_phone_in_budget(price, '20000-30000')
        ok = (allowed == expected_allowed)
        if ok:
            b2030_passed += 1
        res_str = "ALLOW" if allowed else "REMOVE"
        status = "PASSED" if ok else "FAILED"
        print(f"Price ₹{price:,} -> Expected: {action_str} | Result: {res_str} | {status}")
    print(f"₹20,000 – ₹30,000 Range Test: {b2030_passed}/{len(budget_test_cases)} passed.\n")

    # 3. All Other Budget Ranges
    other_ranges = [
        ("under-10000", [5000, 9999], [10000, 15000]),
        ("10000-20000", [10000, 15000, 20000], [9999, 20001]),
        ("30000-50000", [30000, 40000, 50000], [29999, 50001]),
        ("50000-80000", [50000, 65000, 80000], [49999, 80001]),
        ("above-80000", [80001, 120000], [80000, 50000])
    ]
    
    all_ranges_ok = True
    for cat, should_allow, should_remove in other_ranges:
        print(f"--- Testing Budget Tier '{cat}' ---")
        for p in should_allow:
            if not is_phone_in_budget(p, cat):
                print(f"  FAIL: ₹{p:,} should be ALLOWED in {cat}")
                all_ranges_ok = False
        for p in should_remove:
            if is_phone_in_budget(p, cat):
                print(f"  FAIL: ₹{p:,} should be REMOVED in {cat}")
                all_ranges_ok = False
    if all_ranges_ok:
        print("All Other Budget Tiers: PASSED.\n")

    # 4. Special Edition & Edition (number) Name Cleanup Tests
    print("====================================================")
    print("RUNNING EDITION (NUMBER) PHONE NAME CLEANUP TESTS")
    print("====================================================")
    name_test_cases = [
        ("OnePlus 12 Special Edition", "OnePlus 12"),
        ("Samsung Galaxy S24 SPECIAL EDITION", "Samsung Galaxy S24"),
        ("Phone X SPECIAL EDITION", "Phone X"),
        ("Xiaomi 14 Pro", "Xiaomi 14 Pro"),
        ("Nothing Phone (2a) Special Edition (v17)", "Nothing Phone (2a)"),
        ("Google Pixel 9 Pro XL Special Edition v3", "Google Pixel 9 Pro XL"),
        ("Samsung Galaxy S23 FE 5G", "Samsung Galaxy S23 FE 5G"),
        ("iPhone 15 Pro Max", "iPhone 15 Pro Max"),
        ("iPhone SE", "iPhone SE"),
        ("Realme GT 5 Pro Special Edition v2", "Realme GT 5 Pro"),
        ("Vivo X100 Pro 5G Special Edition v5", "Vivo X100 Pro 5G"),
        ("OnePlus 12 Edition (v2)", "OnePlus 12"),
        ("Samsung Galaxy S24 Edition 5", "Samsung Galaxy S24"),
        ("Phone X Edition (12)", "Phone X"),
        ("Motorola Edge 50 Pro Edition", "Motorola Edge 50 Pro"),
    ]
    
    name_passed = 0
    for input_name, expected_output in name_test_cases:
        res = get_clean_phone_name(input_name)
        ok = (res == expected_output)
        if ok:
            name_passed += 1
        status = "PASSED" if ok else f"FAILED (got '{res}')"
        print(f"Input: '{input_name}' -> Output: '{res}' | {status}")
    print(f"Special Edition Cleanup: {name_passed}/{len(name_test_cases)} passed.\n")

    overall_ok = (price_passed == len(price_tests)) and (b2030_passed == len(budget_test_cases)) and all_ranges_ok and (name_passed == len(name_test_cases))
    if overall_ok:
        print("ALL AUTOMATED TESTS PASSED SUCCESSFULLY!")
    else:
        print("SOME TESTS FAILED - PLEASE REVIEW!")

if __name__ == "__main__":
    run_tests()
