# PhonePerfect Tables Content

TABLE_2_1 = [
    ("S.No", "Author(s) and Year", "Title and Source", "Brief Summary"),
    ("1", "Adomavicius & Tuzhilin (2021)", "Context-Aware Recommender Systems. ACM Computing Surveys", "Establishes multi-dimensional recommendation foundations, proving that incorporating situational context and dynamic user preference weighting yields significantly higher satisfaction than static popularity-based ranking."),
    ("2", "Triantaphyllou (2020)", "Multi-Criteria Decision Making Methods: A Comparative Study. Springer", "Analyzes quantitative Multi-Attribute Utility Theory (MAUT) and weighted scoring formulations, demonstrating that normalized additive utility models maintain ranking consistency and explainability in high-dimensional hardware evaluations."),
    ("3", "Bi et al. (2023)", "Conversational Recommender Systems: A Survey. ACM TOIS", "Investigates conversational intent recognition and slot-filling in interactive shopping advisors, emphasizing that lightweight rule-based and grammar parsing engines provide zero-latency execution on client-side browsers."),
    ("4", "Gao & Liu (2022)", "Dynamic E-Commerce Price Tracking and Volatility Analytics. IEEE Access", "Examines price volatility and promotional discount mechanics across major online retail marketplaces, highlighting the necessity of short-TTL caching and verified product catalog identity matching (e.g., ASIN normalization)."),
    ("5", "Malavolta et al. (2021)", "Hybrid Mobile Apps and WebViews: A Performance Benchmark. Empirical Software Engineering", "Performs extensive benchmarking of native Android WebViews, demonstrating that hardware-accelerated rendering and synchronous system inset management eliminate frame drops and memory spikes in data-dense catalogs."),
    ("6", "Jindal et al. (2024)", "Smart Device Recommendation via Feature Trade-off Modeling. IEEE Trans. Consumer Electronics", "Proposes constraint-driven consumer electronics recommendation models, verifying that explicit hardware compromises (e.g., battery endurance vs. slim ergonomics) must be transparently exposed to users during device selection."),
    ("7", "Russell & Norvig (2022)", "Artificial Intelligence: A Modern Approach (4th Ed.). Pearson", "Covers rational decision-making agents, utility functions, and constraint satisfaction problems, forming the foundational theoretical basis for PhonePerfect's DecisionEngine scoring and budget clipping algorithms."),
    ("8", "He et al. (2023)", "Progressive Web Applications: A Comprehensive Performance Study. ACM Web Conference (WWW)", "Evaluates Service Worker caching strategies for data-intensive offline-first web applications, demonstrating sub-second load times and robust offline resilience when asset manifests are locally cached."),
    ("9", "Venkatesh & Davis (2020)", "User Acceptance of Information Technology: Consumer Choice Overload. MIS Quarterly", "Demonstrates that excessive specification dimensions in electronics purchasing induce choice paralysis, and that guided multi-step interactive quizzes significantly increase purchase confidence."),
    ("10", "Chou & Lin (2021)", "Automated Product Specification Extraction and Data Deduplication. Expert Systems with Applications", "Presents automated web extraction and canonical record deduplication algorithms for consumer electronics catalogs, inspiring PhonePerfect's catalog enrichment, normalization, and verification pipeline.")
]

TABLE_5_1 = [
    ("Feature", "Conventional E-Commerce", "Static Spec Repositories", "PhonePerfect Platform"),
    ("Personalized Decision Scoring", "None (Static price/popularity sorting)", "None (Manual filtering only)", "Dynamic Multi-Criteria Weighting (DecisionEngine)"),
    ("Feature Trade-off Analysis", "None (Opaque vendor listings)", "Manual side-by-side specs only", "Automated advantage & compromise scoring"),
    ("Conversational Buying Advisor", "Generic chatbot / Sales-driven", "None", "Deterministic NLP intent & constraint parser (ai-chat.js)"),
    ("Multi-Device Comparison", "Limited (2 devices, rigid format)", "Tabular specs (up to 3 devices)", "Interactive side-by-side comparison for up to 4 devices"),
    ("Price Verification & Deals", "Single-portal list price only", "Outdated or affiliate MSRP only", "Real-time Flask microservice with ASIN verification & deal badges"),
    ("Offline Usability", "No (Completely network-blocked)", "No (Network required)", "100% offline-ready PWA & pre-cached Android WebView"),
    ("Platform Architecture", "Heavy React/Angular bundle", "Server-side HTML with heavy ads", "Lightweight Vanilla JS ES6+ (Zero external UI dependencies)"),
    ("Client Performance & Jank", "High DOM latency & script jank", "Intrusive scripts & video ads", "Hardware-accelerated 60/120 FPS rendering with synchronous insets")
]

TABLE_6_1 = [
    ("Component", "Specification"),
    ("Client Mobile Device (Target)", "Android smartphone running Android 8.0 (API 26) through Android 16 (API 36); 3 GB RAM minimum (4 GB+ recommended)"),
    ("Client Storage Requirement", "50 MB available internal storage for cached PWA assets, SQLite web database, and Android APK installation"),
    ("Development Workstation CPU", "Quad-Core 64-bit Intel Core i5 / AMD Ryzen 5 processor or higher (8-core workstation recommended for Android builds)"),
    ("Development Workstation RAM", "8 GB RAM minimum; 16 GB DDR4/DDR5 recommended for running Gradle daemon and Android emulator simultaneously"),
    ("Development Storage", "20 GB available SSD storage for Android SDK packages, Gradle caches, Python virtual environments, and project repositories"),
    ("Network Interface", "Standard broadband / cellular connection for fetching live e-commerce prices via REST endpoints (optional for offline client)")
]

TABLE_6_2 = [
    ("Component", "Specification"),
    ("Operating Systems (Host)", "Microsoft Windows 10/11 (64-bit), Linux (Ubuntu 22.04 LTS+), or macOS (Sonoma+)"),
    ("Mobile Container Framework", "Android Jetpack SDK (Compile SDK 36, Target SDK 35, Min SDK 26) with Android Gradle Plugin (AGP) 8.7+"),
    ("Android Programming Language", "Kotlin 2.0.21 with Java 17 LTS (OpenJDK 17.0.12) and Android Kotlin Extensions"),
    ("Native Android UI Container", "Hardware-accelerated Android WebView with JavaScriptInterface bidirectional bridge and Edge-to-Edge inset management"),
    ("Web Client Languages", "Modern Web Standards: Semantic HTML5, Vanilla CSS3 (Custom Glassmorphism Design Tokens), and ECMAScript 2022 (ES6+)"),
    ("Web Application Architecture", "Single-Page Application (SPA) with Progressive Web App (PWA) Service Worker caching (Cache-First offline strategy)"),
    ("Backend API Microservice", "Python 3.10+ with Flask 3.0+ microframework, Flask-CORS for secure cross-origin resource sharing"),
    ("Data Processing & Pipeline", "Python standard library (json, os, re, time, datetime) alongside Requests, BeautifulSoup4, and urllib3"),
    ("Smartphone Catalog Format", "Dual format: JavaScript array (phones.js, 2.8 MB) for instant zero-fetch client execution and JSON (phones.json, 2.8 MB)"),
    ("Application Package Identifier", "com.phoneperfect.finder (Signed Release APK and Google Play Store App Bundle AAB)"),
    ("Android Signing Keystore", "Java KeyStore (release-key.jks) with RSA 2048-bit private key and SHA-256 with RSA signature algorithm"),
    ("Development IDEs & Tools", "Android Studio Ladybug (2024.2+) / Koala, VS Code, Git CLI, and PowerShell 7.4 / Bash shell")
]

TABLE_7_1 = [
    ("Component Group", "Primary Files & Artifacts", "Architectural Responsibility"),
    ("Presentation & UI", "index.html, style.css, manifest.json", "Single-page responsive layout, glassmorphic dark theme, CSS variable tokens, and PWA metadata"),
    ("Decision Engine & Core", "app.js (DecisionEngine, UIController)", "Multi-criteria scoring algorithm, budget clipping, hardware feature weighting, catalog rendering, and modal controllers"),
    ("Conversational Advisor", "ai-chat.js (INTENTS, detectIntent)", "Natural language intent classification, slot extraction (price range, brand keywords), and guided phone recommendations"),
    ("Price Tracking Service", "price-tracker.js, price_server.py", "Frontend live price client, Flask REST API endpoints (/api/price, /api/deals), ASIN verification, and 10-minute TTL caching"),
    ("Dataset & Image Cache", "phones.js, phones.json, phone_images_cache.json", "Curated catalog of 1,597+ verified devices, hardware specifications, normalized INR prices, and verified image CDN URLs"),
    ("Native Android Host", "MainActivity.kt, AndroidManifest.xml, build.gradle.kts", "Android WebView host container, synchronous status/navigation bar inset padding, edge-to-edge support, and back navigation"),
    ("Pipeline & Validation", "sync_phoneperfect_assets.py, audit_*.py, calibrate_*.py", "Asset synchronization into Android assets/, specification consistency auditing, duplicate elimination, and price calibration")
]

TABLE_7_2 = [
    ("Hardware Dimension", "Mapped Key", "Default Weight", "User Selected Weight", "Normalized Impact Description"),
    ("Processor & Performance", "processor", "1.0", "+4.0 (5.0)", "Evaluates CPU core architecture, clock speeds, and Antutu benchmark tier"),
    ("Gaming & Graphics", "processor (mapped)", "1.0", "+4.0 (5.0)", "Increases compute weight for GPU rendering capability and sustained gaming frame rates"),
    ("Camera & Photography", "camera", "1.0", "+4.0 (5.0)", "Weights primary sensor megapixels, optical image stabilization (OIS), and aperture tier"),
    ("Battery & Endurance", "battery", "1.0", "+4.0 (5.0)", "Weights battery capacity (mAh) and battery efficiency relative to display size"),
    ("Display & Ergonomics", "display", "1.0", "+4.0 (5.0)", "Evaluates AMOLED/OLED panel type, high refresh rates (90/120/144Hz), and peak brightness"),
    ("Fast Charging Speed", "charging", "1.0", "+4.0 (5.0)", "Weights wired charging wattage (e.g., 33W, 67W, 120W) and wireless charging presence"),
    ("Durability & Build", "durability", "1.0", "+4.0 (5.0)", "Weights ingress protection ratings (IP68/IP67/IP54) and Corning Gorilla Glass protection"),
    ("Storage Capacity", "storage", "1.0", "+4.0 (5.0)", "Weights internal UFS storage tier (128GB, 256GB, 512GB) and RAM capacity"),
    ("Value for Money", "price", "2.0 (Baseline)", "Constant baseline", "Normalized inverse price weight prioritizing higher hardware specs per Rupee spent")
]

TABLE_7_3 = [
    ("Intent Category", "Sample Trigger Keywords", "Extraction & Resolution Action", "Target UI Output"),
    ("COMPARE", "compare, vs, versus, between, difference", "Extracts two to four phone entities from query; verifies existence in catalog", "Populates comparison modal with selected devices side-by-side"),
    ("BEST", "best, top, recommend, suggest, ideal, perfect", "Executes multi-attribute utility scoring filtered by detected constraints", "Displays top 3 recommended phones with match scores and highlights"),
    ("CHEAPEST / BUDGET", "cheapest, affordable, budget, lowest price, cheap", "Applies budget constraint; sorts candidate phones in ascending order of price", "Displays lowest-priced verified phones meeting minimum baseline specs"),
    ("EXPENSIVE / FLAGSHIP", "expensive, premium, flagship, high-end, costly", "Filters devices in premium tier (>₹50,000); sorts by overall benchmark score", "Presents premium flagship recommendations with top-tier hardware specs"),
    ("SPECS / DETAILS", "specs, specification, details, features, info", "Extracts exact phone entity name; fetches complete hardware specification record", "Opens device details modal displaying full technical spec sheet"),
    ("BATTERY / CHARGING", "battery, mah, charge, charging, endurance, backup", "Applies battery priority bonus; filters devices with >=5,000 mAh and fast charging", "Recommends smartphones with exceptional battery life and fast charging"),
    ("GAMING / CHIPSET", "gaming, game, processor, performance, fps, snapdragon", "Applies processor priority bonus; filters flagship Snapdragon/Dimensity chipsets", "Ranks devices with high gaming performance and cooling architectures"),
    ("CAMERA / PHOTO", "camera, photo, megapixel, mp, photography, video, zoom", "Applies camera priority bonus; prioritizes high-MP and OIS-equipped devices", "Ranks smartphones optimized for photography and 4K/8K video capture")
]

TABLE_7_4 = [
    ("Price Status Code", "Percentage Deviation (diffPct)", "Display Badge Label", "CSS Class", "Commercial Implication"),
    ("GOOD_PRICE", "diffPct <= +8.0%", "Good Price", "deal-good", "Device is selling at or near historic low / launch price; highly recommended purchase"),
    ("FAIR_PRICE", "+8.0% < diffPct <= +20.0%", "Fair Price", "deal-fair", "Selling price is within standard retail operating margin; acceptable purchase"),
    ("SLIGHTLY_EXPENSIVE", "+20.0% < diffPct <= +35.0%", "Slightly Expensive", "deal-warn", "Device price is elevated above typical market baseline; buyers should monitor or await sales"),
    ("OVERPRICED", "diffPct > +35.0%", "Overpriced", "deal-overpriced", "Price significantly exceeds fair market value; purchasing strongly discouraged")
]

TABLE_7_5 = [
    ("Security Guarantee", "Implementation Mechanism", "Operational Benefit"),
    ("Client-Side Data Privacy", "Zero user tracking, no third-party analytic telemetry, local preference storage", "User search history and questionnaire responses never leave the local device storage"),
    ("Offline Autonomy", "Full catalog (1,597+ records) embedded in phones.js and cached via Service Worker", "Complete discovery, quiz scoring, and comparison work without active internet connection"),
    ("API Sandboxing & CORS", "Flask @app.after_request handler restricts methods to GET, POST, OPTIONS with explicit headers", "Prevents unauthorized cross-origin tampering with price monitoring microservice"),
    ("Product Identity Verification", "Bidirectional ASIN-to-Catalog cross-referencing and exact model ID matching", "Eliminates fraudulent affiliate redirects and prevents pricing mismatches across retailers"),
    ("Android WebView Isolation", "Explicit @JavascriptInterface annotations; disallows arbitrary file access or reflection", "Hardens mobile container against cross-site scripting and unauthorized native capability access")
]
