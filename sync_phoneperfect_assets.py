import os
import shutil

src_dir = r"c:\Users\nisha\.gemini\antigravity\scratch"
android_assets = os.path.join(src_dir, "android-app", "app", "src", "main", "assets")

os.makedirs(android_assets, exist_ok=True)

files_to_sync = [
    "index.html",
    "style.css",
    "app.js",
    "phones.js",
    "ai-chat.js",
    "price-tracker.js",
    "auto-updater.js",
    "manifest.json",
    "privacy-policy.html"
]

for filename in files_to_sync:
    src_file = os.path.join(src_dir, filename)
    dest_file = os.path.join(android_assets, filename)
    if os.path.exists(src_file):
        shutil.copy2(src_file, dest_file)
        size_kb = os.path.getsize(dest_file) / 1024
        print(f"Synced {filename} ({size_kb:.1f} KB) -> {android_assets}")
    else:
        print(f"Warning: {filename} does not exist in source directory.")

print("All PhonePerfect assets successfully synchronized!")
