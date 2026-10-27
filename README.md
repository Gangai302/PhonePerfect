# PhonePerfect – Smartphone Recommendation & Live Price Tracker

PhonePerfect is an advanced smartphone recommendation engine, comparison platform, and live price tracking application. It is available as both a high-performance **Progressive Web Application (PWA)** and an **Android Native WebView Application**.

---

## 📱 Features

- **Smart Phone Finder & Quiz:** Custom recommendation algorithm weighing user priorities (Camera, Battery, Performance, Durability, Display, Audio, Charging speed).
- **Comprehensive Database:** 1,597+ curated smartphones with verified Indian Rupee (₹) pricing, ASINs, and complete hardware specifications.
- **Side-by-Side Comparison:** Compare up to 4 devices simultaneously with highlighted spec differences.
- **AI Buying Advisor Assistant:** Interactive conversational agent to help users choose phones based on budget and requirements.
- **Real-Time Price Server:** Flask-based backend API querying and caching live e-commerce prices with deal badges and stock availability.
- **Offline-Ready Android App:** Hardware-accelerated Android WebView integration with bidirectional JavaScript bridge and back-gesture handling.

---

## 📂 Project Architecture & Directory Structure

```
phoneperfect/
├── android-app/                   # Complete Android Studio project
│   ├── app/
│   │   ├── build.gradle.kts       # Application-level Gradle build configuration
│   │   └── src/main/
│   │       ├── AndroidManifest.xml# Android application manifest and permissions
│   │       ├── assets/            # Embedded offline web assets
│   │       ├── java/com/phoneperfect/finder/
│   │       │   └── MainActivity.kt# WebView container & AndroidBridge
│   │       └── res/               # Android drawables, icons, strings, themes
│   ├── gradle/
│   │   └── libs.versions.toml     # Version catalog for Android dependencies
│   ├── build.gradle.kts           # Top-level Gradle build script
│   ├── settings.gradle.kts        # Gradle project settings
│   ├── gradlew & gradlew.bat      # Gradle wrapper binaries
│   └── release-key.jks            # Android keystore for release signing
│
├── Frontend Web Application:
│   ├── index.html                 # Main single-page application interface
│   ├── style.css                  # Responsive design system & glassmorphism theme
│   ├── app.js                     # Core app logic: filtering, search, scoring, UI
│   ├── ai-chat.js                 # Conversational AI assistant module
│   ├── auto-updater.js            # OTA catalog update client
│   ├── price-tracker.js           # Live pricing and deals tracker client
│   ├── service-worker.js          # Service worker for offline PWA caching
│   ├── manifest.json              # PWA manifest metadata
│   └── privacy-policy.html        # App store compliance privacy policy
│
├── Datasets:
│   ├── phones.js                  # Primary phone specifications dataset (JS array)
│   ├── phones.json                # Complete smartphone specifications dataset (JSON)
│   └── phone_images_cache.json    # Verified device image URLs & cache
│
├── Backend & Pipeline:
│   ├── price_server.py            # Flask API server for real-time prices & catalog
│   ├── sync_phoneperfect_assets.py# Syncs web assets to Android app/src/main/assets/
│   ├── scrape_*.py                # GSMArena & portal scraping utilities
│   ├── calibrate_*.py             # Price calibration & verification scripts
│   └── audit_*.py                 # Consistency & spec validation scripts
│
├── Configuration & Instructions:
│   ├── README.md                  # This documentation file
│   ├── requirements.txt           # Python backend & tool dependencies
│   └── package.json               # Node.js dev scripts & dependencies
```

---

## 🚀 Quick Start & Build Instructions

### 1. Frontend Web App (PWA)

To run the web interface locally without any setup:

**Using Python:**
```bash
python -m http.server 3000
```
Open your browser and navigate to `http://localhost:3000`.

**Using Node.js:**
```bash
npm install
npm start
```

---

### 2. Backend Live Price Server

The backend provides real-time pricing and stock status for devices in the catalog.

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the API server:**
   ```bash
   python price_server.py
   ```
   The server will start on `http://127.0.0.1:5000`.

3. **API Endpoints:**
   - `GET /api/price/<asin>` – Fetches live or cached price for a given ASIN.
   - `GET /api/prices?asins=B0...,B0...` – Bulk price check for multiple devices.
   - `GET /api/deals` – Curated discounted devices and limited-time deals.
   - `GET /api/catalog/search?q=<query>` – Catalog search by keyword.

---

### 3. Android Application

#### Prerequisites
- **JDK 17** installed and configured (`JAVA_HOME` pointing to JDK 17).
- **Android SDK** (API 36 / Android 16 Preview or standard API 34+).
- **Android Studio Ladybug (2024.2+)** or command-line Gradle.

#### Sync Web Assets to Android
Whenever frontend changes are made (`index.html`, `app.js`, `phones.js`, etc.), synchronize them into the Android assets directory:
```bash
python sync_phoneperfect_assets.py
```

#### Build with Gradle CLI
Navigate to the `android-app` directory:
```bash
cd android-app
```

- **Build Debug APK:**
  ```bash
  ./gradlew assembleDebug
  ```
  Output: `app/build/outputs/apk/debug/app-debug.apk`

- **Build Signed Release APK:**
  ```bash
  ./gradlew assembleRelease
  ```
  Output: `app/build/outputs/apk/release/app-release.apk`

- **Build Release Android App Bundle (AAB for Google Play):**
  ```bash
  ./gradlew bundleRelease
  ```
  Output: `app/build/outputs/bundle/release/app-release.aab`

---

## 📊 Dataset Maintenance & Pipeline Scripts

- `python sync_phoneperfect_assets.py`: Syncs root web files to `android-app/app/src/main/assets/`.
- `python audit_specs_consistency.py`: Runs automated sanity checks on specifications, prices, and IDs.
- `python calibrate_all_1597_phone_prices.py`: Normalizes and validates current Indian market prices.
- `python run_e2e_tests.py`: Runs end-to-end tests across recommendation scores and UI selectors.

---

## 📄 License & Attribution

- Built with modern Web Standards (HTML5, Vanilla CSS3, ES6+ JavaScript).
- Native Android container powered by Android Jetpack & Modern WebView.
- Source repository: Nishar29/PhonePerfect.
