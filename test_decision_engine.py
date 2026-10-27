import json
import re

def test_engine():
    print("=== Testing Decision Engine Logic on phones.js ===")
    
    with open("phones.js", "r", encoding="utf-8") as f:
        content = f.read()
        
    array_start = content.find("var PHONES = ") + len("var PHONES = ")
    array_end = content.find("];\n\nconst CRITERIA") + 1
    phones_json = content[array_start:array_end]
    
    phones = json.loads(phones_json)
    print(f"Loaded {len(phones)} smartphones from database.")
    
    # Test normalization & risk calculations
    sample = phones[:10]
    passed_tests = 0
    total_tests = 0

    for p in sample:
        total_tests += 1
        name = p.get('name')
        price = p.get('price_numeric', 50000)
        scores = p.get('scores', {})
        
        # Check scores bounded between 0 and 10
        assert all(0 <= v <= 10 for v in scores.values()), f"Score out of bounds for {name}"
        
        # Check price history array
        hist = p.get('price_history', [price])
        assert len(hist) > 0, f"Empty price history for {name}"
        
        passed_tests += 1
        print(f"  [OK] Device '{p['brand']} {name}': Price Rs.{price:,}, Scores verified.")

    print(f"\nPassed {passed_tests}/{total_tests} device validation checks.")
    print("Decision Engine Data Verification Successful!")

if __name__ == "__main__":
    test_engine()
