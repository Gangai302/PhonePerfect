import os
import zipfile
import sys

source_dir = r"C:\Users\nisha\OneDrive\Desktop\scratch"
dest_zip = r"C:\Users\nisha\Downloads\PhonePerfect.zip"

# Folders to completely exclude anywhere in path
exclude_dirs = {
    ".git",
    ".gradle",
    "build",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".vscode"
}

# Specific dist folder under phoneperfect-v2/frontend
# Extensions to exclude (build artifacts, keys, pre-existing zip/binaries)
exclude_extensions = {
    ".jks",
    ".keystore",
    ".aab",
    ".apk",
    ".zip",
    ".pyc"
}

# Specific filenames to exclude (secrets/local config/databases)
exclude_filenames = {
    "local.properties",
    "phoneperfect_v2.db"
}

print(f"Scanning source directory: {source_dir}")

included_files = []
skipped_summary = {"dirs": 0, "extensions": 0, "secrets": 0}

for root, dirs, files in os.walk(source_dir):
    # Filter directories in-place so os.walk doesn't descend into them
    dirs[:] = [d for d in dirs if d not in exclude_dirs and not (d == "dist" and "frontend" in root)]
    
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, source_dir)
        
        name_lower = file.lower()
        _, ext_lower = os.path.splitext(name_lower)
        
        # Check extensions
        if ext_lower in exclude_extensions:
            skipped_summary["extensions"] += 1
            continue
            
        # Check excluded filenames
        if name_lower in exclude_filenames:
            skipped_summary["secrets"] += 1
            continue
            
        # Check sensitive environment files (.env, .env.local, etc. but keep .env.example)
        if name_lower.startswith(".env") and not name_lower.endswith(".example"):
            skipped_summary["secrets"] += 1
            continue
            
        included_files.append((file_path, rel_path))

print(f"Found {len(included_files)} source and asset files to archive.")
print(f"Excluded: {skipped_summary}")

# Verify key files are present
key_files = [
    "index.html",
    "style.css",
    "app.js",
    "ai-chat.js",
    "price-tracker.js",
    "price_server.py",
    "phones.js",
    "phones.json"
]

rel_paths_set = {r for _, r in included_files}
for kf in key_files:
    found = any(r == kf or r.endswith("/" + kf) or r.endswith("\\" + kf) for r in rel_paths_set)
    print(f"Key file '{kf}' included: {found}")

# Create ZIP archive
print(f"\nCreating ZIP file at: {dest_zip}")
os.makedirs(os.path.dirname(dest_zip), exist_ok=True)

with zipfile.ZipFile(dest_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
    for file_path, rel_path in included_files:
        # Preserve structure under 'PhonePerfect/' root directory inside zip for clean extraction
        archive_name = os.path.join("PhonePerfect", rel_path)
        zipf.write(file_path, archive_name)

zip_size_mb = os.path.getsize(dest_zip) / (1024 * 1024)
print(f"Successfully created: {dest_zip} ({zip_size_mb:.2f} MB)")

# Verify archive integrity
print("\nVerifying archive integrity...")
with zipfile.ZipFile(dest_zip, 'r') as zipf:
    bad_file = zipf.testzip()
    if bad_file:
        print(f"ERROR: Corrupt file detected in archive: {bad_file}")
        sys.exit(1)
    
    namelist = zipf.namelist()
    print(f"Verification successful! ZIP contains {len(namelist)} items with 0 corrupted files.")
