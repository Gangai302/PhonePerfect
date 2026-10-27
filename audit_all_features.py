import os
import re
import subprocess

scratch_dir = r"c:\Users\nisha\.gemini\antigravity\scratch"
index_html_path = os.path.join(scratch_dir, "index.html")

js_files = ["app.js", "phones.js", "price-tracker.js", "ai-chat.js", "auto-updater.js"]

# 1. Syntax check JS files
print("=== Step 1: Reading JS Files ===")
for js in js_files:
    full_path = os.path.join(scratch_dir, js)
    if os.path.exists(full_path):
        print(f"[OK] File exists: {js}")
    else:
        print(f"[ERROR] File missing: {js}")

# 2. Check HTML for all IDs
print("\n=== Step 2: Checking HTML IDs referenced in JS ===")
with open(index_html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Find all id="..." in index.html
html_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html_content))
print(f"Total HTML element IDs found: {len(html_ids)}")

missing_ids = []
for js in js_files:
    full_path = os.path.join(scratch_dir, js)
    with open(full_path, "r", encoding="utf-8") as f:
        js_code = f.read()
    
    # getElementById
    get_ids = re.findall(r'getElementById\(["\']([^"\']+)["\']\)', js_code)
    # querySelector with #id
    qs_ids = re.findall(r'querySelector\(["\']#([^"\'\.\s>\[:]+)["\']\)', js_code)
    
    all_referenced_ids = set(get_ids + qs_ids)
    for rid in all_referenced_ids:
        if "${" in rid or "`" in rid or "'" in rid or "+" in rid:
            continue
        if rid not in html_ids:
            missing_ids.append((js, rid))

if missing_ids:
    print(f"[WARNING] Missing IDs referenced in JS: {len(missing_ids)}")
    for js, rid in missing_ids:
        print(f"  - {js}: element ID '{rid}' NOT found in index.html!")
else:
    print("[OK] All element IDs referenced in JS exist in index.html!")

# 3. Check inline onclick / onchange in index.html vs defined JS functions
print("\n=== Step 3: Inline Handlers Check ===")
inline_handlers = re.findall(r'on\w+=["\']([^"\']+)["\']', html_content)
all_js_content = ""
for js in js_files:
    with open(os.path.join(scratch_dir, js), "r", encoding="utf-8") as f:
        all_js_content += "\n" + f.read()

missing_handlers = []
for handler in inline_handlers:
    match = re.match(r'([a-zA-Z0-9_]+)\s*\(', handler.strip())
    if match:
        func_name = match.group(1)
        if not re.search(r'\b(function\s+' + func_name + r'|const\s+' + func_name + r'|let\s+' + func_name + r'|var\s+' + func_name + r'|window\.' + func_name + r')\b', all_js_content):
            missing_handlers.append((handler, func_name))

if missing_handlers:
    print(f"[WARNING] Missing handler functions in JS: {len(missing_handlers)}")
    for handler, fname in missing_handlers:
        print(f"  - Handler '{handler}' -> function '{fname}' not defined in JS!")
else:
    print("[OK] All inline handlers in index.html have defined functions in JS!")

print("\nAudit Complete.")
