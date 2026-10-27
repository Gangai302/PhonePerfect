import os
from PIL import Image, ImageDraw

def generate_icons():
    source_path = r"c:\Users\nisha\.gemini\antigravity\scratch\app_icon_source.png"
    img = Image.open(source_path).convert("RGBA")
    
    # 1. Update manifest.json icon (icon-512.png)
    assets_dir = r"c:\Users\nisha\.gemini\antigravity\scratch\android-app\app\src\main\assets"
    os.makedirs(assets_dir, exist_ok=True)
    img.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(assets_dir, "icon-512.png"), format="PNG")
    img.resize((192, 192), Image.Resampling.LANCZOS).save(os.path.join(assets_dir, "icon-192.png"), format="PNG")
    print("Saved web/PWA assets icon-512.png and icon-192.png")

    # Mipmap densities and sizes
    densities = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192
    }
    
    res_dir = r"c:\Users\nisha\.gemini\antigravity\scratch\android-app\app\src\main\res"
    
    # Adaptive foreground size (108x108 dp)
    # The inner 72dp is the safe viewport (2/3 of 108dp)
    adaptive_foreground_sizes = {
        "mipmap-mdpi": 108,
        "mipmap-hdpi": 162,
        "mipmap-xhdpi": 216,
        "mipmap-xxhdpi": 324,
        "mipmap-xxxhdpi": 432
    }
    
    # Prepare round mask function
    def make_round(image):
        w, h = image.size
        mask = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, w, h), fill=255)
        round_img = image.copy()
        round_img.putalpha(mask)
        return round_img

    for folder, size in densities.items():
        folder_path = os.path.join(res_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        # Standard icon
        standard_icon = img.resize((size, size), Image.Resampling.LANCZOS)
        standard_path = os.path.join(folder_path, "ic_launcher.webp")
        standard_icon.save(standard_path, format="WEBP", lossless=True)
        
        # Round icon (circle mask)
        round_icon = make_round(standard_icon)
        round_path = os.path.join(folder_path, "ic_launcher_round.webp")
        round_icon.save(round_path, format="WEBP", lossless=True)
        
        # Adaptive foreground layer:
        # Full canvas size is adaptive_foreground_sizes[folder]
        # Content placed within the safe 66-72% zone so it isn't clipped by any launcher mask
        canvas_size = adaptive_foreground_sizes[folder]
        fg_canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
        # icon size inside adaptive viewport: 72dp equivalent (size * 72/48 for mdpi ratio, which is size)
        inner_size = int(canvas_size * 0.72)
        inner_icon = img.resize((inner_size, inner_size), Image.Resampling.LANCZOS)
        offset = ((canvas_size - inner_size) // 2, (canvas_size - inner_size) // 2)
        fg_canvas.paste(inner_icon, offset, inner_icon)
        
        fg_path = os.path.join(folder_path, "ic_launcher_fg.webp")
        fg_canvas.save(fg_path, format="WEBP", lossless=True)
        
        print(f"Generated {folder}: ic_launcher ({size}x{size}), ic_launcher_round ({size}x{size}), ic_launcher_fg ({canvas_size}x{canvas_size})")

    # Also update ic_launcher_background.xml or create solid dark blue background matching icon corners #000c2e
    bg_xml = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#010726"
        android:pathData="M0,0h108v108h-108z" />
</vector>
"""
    drawable_dir = os.path.join(res_dir, "drawable")
    with open(os.path.join(drawable_dir, "ic_launcher_background.xml"), "w", encoding="utf-8") as f:
        f.write(bg_xml)
    print("Updated ic_launcher_background.xml with matching deep blue tone #010726.")

    # Update mipmap-anydpi-v26 to reference the foreground and background properly
    v26_dir = os.path.join(res_dir, "mipmap-anydpi-v26")
    v26_xml = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@mipmap/ic_launcher_fg" />
</adaptive-icon>
"""
    with open(os.path.join(v26_dir, "ic_launcher.xml"), "w", encoding="utf-8") as f:
        f.write(v26_xml)
    with open(os.path.join(v26_dir, "ic_launcher_round.xml"), "w", encoding="utf-8") as f:
        f.write(v26_xml)
    print("Updated adaptive icon configs in mipmap-anydpi-v26.")

if __name__ == "__main__":
    generate_icons()
