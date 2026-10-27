# PhonePerfect Figure Placeholders & Visual Descriptions

FIGURE_BOXES = {
    4: {  # Figure 5.1 (Table index 4)
        "caption": "Figure 5.1 Overall System Architecture of PhonePerfect",
        "description": (
            "[ SYSTEM ARCHITECTURE DIAGRAM: PHONEPERFECT ]\n\n"
            "+---------------------------------------------------------------------------------------------------------+\n"
            "|                                       CLIENT PRESENTATION SURFACES                                      |\n"
            "|  +-------------------------------------------------+  +----------------------------------------------+  |\n"
            "|  |   Android Native Host (com.phoneperfect.finder) |  |   Desktop & Mobile Web Browsers (PWA)        |  |\n"
            "|  |   - MainActivity.kt (Hardware-Accelerated WebV) |  |   - Service Worker (Cache-First Offline)     |  |\n"
            "|  |   - Synchronous Status/Nav Inset Management     |  |   - Web App Manifest (manifest.json)         |  |\n"
            "|  |   - AndroidBridge Bidirectional JS Interface    |  |   - Responsive Glassmorphic Dark Layout      |  |\n"
            "|  +------------------------+------------------------+  +----------------------+-----------------------+  |\n"
            "+---------------------------|--------------------------------------------------|--------------------------+\n"
            "                            v                                                  v                           \n"
            "+---------------------------------------------------------------------------------------------------------+\n"
            "|                                CORE APPLICATION & INTELLIGENCE LAYER                                    |\n"
            "|  +-------------------------------------------------+  +----------------------------------------------+  |\n"
            "|  |   app.js: DecisionEngine & Multi-Criteria Quiz  |  |   ai-chat.js: Conversational Buying Advisor  |  |\n"
            "|  |   - Normalized Utility Weighting Algorithm      |  |   - NLP Intent Classifier (INTENTS grammar)  |  |\n"
            "|  |   - Budget Constraints & Price Sorting Engine   |  |   - Regex Slot Extraction (Budget, Brands)   |  |\n"
            "|  |   - 4-Device Comparison Matrix & Spec Diff      |  |   - Dynamic Recommendation Response Pipeline |  |\n"
            "|  +-------------------------------------------------+  +----------------------------------------------+  |\n"
            "+---------------------------------------------------------------------------------------------------------+\n"
            "                            |                                                  |                           \n"
            "                            v                                                  v                           \n"
            "+----------------------------------------------------+  +----------------------------------------------+  |\n"
            "|   LOCAL SMARTPHONE SPECIFICATION DATASETS          |  |   BACKEND API & LIVE PRICE SERVICE           |  |\n"
            "|   - phones.js (Client Embedded Dataset, 2.8 MB)    |  |   - price_server.py (Flask 3.0 REST API)     |  |\n"
            "|   - phones.json (Canonical JSON Repository)        |  |   - price-tracker.js (Live Price Client)     |  |\n"
            "|   - 1,597+ Verified Devices across 16 Brands       |  |   - ASIN Identity Verification & Cache (TTL) |  |\n"
            "|   - phone_images_cache.json (Optimized CDN URLs)   |  |   - Deal Badging Engine (GOOD, FAIR, WARN)   |  |\n"
            "+----------------------------------------------------+  +----------------------------------------------+  |\n"
            "                                                        |   EXTERNAL RETAIL & CATALOG SOURCES          |  |\n"
            "                                                        |   - Amazon India (ASIN Product Feeds)        |  |\n"
            "                                                        |   - Flipkart / GSMArena Spec Portals         |  |\n"
            "+---------------------------------------------------------------------------------------------------------+"
        )
    },
    5: {  # Figure 5.2 (Table index 5)
        "caption": "Figure 5.2 End-to-End Processing Workflow of the Recommendation Pipeline",
        "description": (
            "[ WORKFLOW DIAGRAM: RECOMMENDATION & DECISION PIPELINE ]\n\n"
            "  [ User Accesses App ]\n"
            "            |\n"
            "            v\n"
            "  [ Discovery Path Selection ] ---> (A) Interactive Quiz  /  (B) Conversational Advisor  /  (C) Manual Filters\n"
            "            |\n"
            "            v\n"
            "  [ Input Parsing & Constraint Mapping ]\n"
            "    - Target Budget Tier (e.g., <Rs.25,000 via DecisionEngine.BUDGET_MAP)\n"
            "    - Feature Priorities Selected (Camera, Battery, Gaming, Display, Charging, Durability)\n"
            "            |\n"
            "            v\n"
            "  [ Normalized Utility Weight Calculation ]\n"
            "    - Base weight = 1.0; Selected priority = +4.0 (5.0); Price weight = 2.0\n"
            "    - Normalized weight w_i = W_i / SUM(W_k)\n"
            "            |\n"
            "            v\n"
            "  [ Candidate Filtering & Hard Constraints ]\n"
            "    - Prune devices with price > budget threshold\n"
            "    - Enforce brand/network/storage constraints if specified\n"
            "            |\n"
            "            v\n"
            "  [ Multi-Criteria Scoring & Sorting ]\n"
            "    - Score = SUM(w_i * S_ij) across all hardware dimensions\n"
            "    - Rank candidates in descending order of calculated match score\n"
            "            |\n"
            "            v\n"
            "  [ Price Status & Deal Verification ]\n"
            "    - Query /api/price/<asin> via price_server.py (10-min cache check)\n"
            "    - Calculate diffPct = ((currentPrice - expectedMarketPrice) / expectedMarketPrice) * 100\n"
            "    - Assign status badge: GOOD_PRICE, FAIR_PRICE, SLIGHTLY_EXPENSIVE, OVERPRICED\n"
            "            |\n"
            "            v\n"
            "  [ UI Render & Interactive Actions ]\n"
            "    - Display Ranked Cards with Spec Badges, Match Percentage & Deal Tag\n"
            "    - Enable Side-by-Side Comparison (up to 4 phones) & Direct Retailer Navigation"
        )
    },
    10: {  # Figure 7.1 (Table index 10)
        "caption": "Figure 7.1 Home Screen and Smartphone Catalog Dashboard of PhonePerfect",
        "description": (
            "[ UI SCREENSHOT PLACEHOLDER: DASHBOARD & CATALOG SCREEN ]\n\n"
            "Shows the primary PhonePerfect single-page application interface (index.html, style.css):\n"
            "- Modern Glassmorphic Dark Theme (#090D16 background, #131A2A card containers, #00D2FF accent gradients).\n"
            "- Sticky Navigation Header with Live Search Input, Brand Filter Pills (Samsung, Xiaomi, Vivo, OnePlus, Apple, etc.),\n"
            "  and Quick Mode Switchers (Phone Finder Quiz, AI Buying Advisor, Comparison Drawer).\n"
            "- Dynamic Catalog Grid rendering smartphone cards with high-resolution device renders, full Indian Rupee (₹) pricing,\n"
            "  key hardware specification badges (Snapdragon/Dimensity SoC, 50MP OIS, 5,000mAh, 120Hz AMOLED), and 'Compare' toggle."
        )
    },
    11: {  # Figure 7.2 (Table index 11)
        "caption": "Figure 7.2 Interactive Multi-Criteria Phone Finder and Scoring Quiz Screen",
        "description": (
            "[ UI SCREENSHOT PLACEHOLDER: MULTI-CRITERIA FINDER & QUIZ SCREEN ]\n\n"
            "Shows the interactive recommendation wizard modal (app.js - DecisionEngine):\n"
            "- Step 1: Budget Selection Carousel (Under ₹10k, ₹10k-₹20k, ₹20k-₹30k, ₹30k-₹50k, ₹50k-₹80k, Above ₹80k).\n"
            "- Step 2: Multi-Select Hardware Priorities with visual iconography (Camera & Photography, Battery & Endurance,\n"
            "  Gaming & Heavy Multitasking, Display Quality & Ergonomics, Fast Charging, Durability & Water Resistance).\n"
            "- Real-Time Recommendation Output: Ranked device recommendations displaying calculated Match Percentage scores\n"
            "  (e.g., '96% Match for Gaming & Battery'), highlight summary of winning attributes, and direct modal link."
        )
    },
    13: {  # Figure 7.3 (Table index 13)
        "caption": "Figure 7.3 Conversational AI Buying Advisor and Natural Language Query Screen",
        "description": (
            "[ UI SCREENSHOT PLACEHOLDER: CONVERSATIONAL AI ADVISOR SCREEN ]\n\n"
            "Shows the embedded conversational shopping assistant (ai-chat.js):\n"
            "- Floating chat overlay with animated bot greeting and suggested quick-prompt chips (e.g., 'Best gaming phone under 25k',\n"
            "  'Flagship camera phones under 50k', 'Compare Galaxy S24 vs OnePlus 12').\n"
            "- Conversational message stream demonstrating client-side intent parsing, budget extraction, and synthesized\n"
            "  recommendation response with embedded clickable phone cards, key specs, and instant comparison triggers."
        )
    },
    15: {  # Figure 7.4 (Table index 15)
        "caption": "Figure 7.4 Multi-Device Side-by-Side Hardware Comparison Matrix Screen",
        "description": (
            "[ UI SCREENSHOT PLACEHOLDER: HARDWARE COMPARISON MATRIX SCREEN ]\n\n"
            "Shows the side-by-side comparison modal evaluating up to 4 devices simultaneously:\n"
            "- Floating bottom dock tracking actively pinned devices with thumbnail badges.\n"
            "- Comparison Matrix Table highlighting parameter-by-parameter differences:\n"
            "  * Chipset & Antutu benchmark score tier\n"
            "  * Camera sensor configuration, OIS support, and video recording capabilities\n"
            "  * Battery capacity (mAh) and bundled charging wattage\n"
            "  * Display technology, peak nits brightness, and refresh rate\n"
            "  * Form factor, weight, ingress protection rating, and software update promise\n"
            "- Visual color-coding emphasizing superior hardware attributes across columns."
        )
    },
    18: {  # Figure 7.5 (Table index 18)
        "caption": "Figure 7.5 Real-Time Price Tracking, Deal Badging, and Stock Alert Modal",
        "description": (
            "[ UI SCREENSHOT PLACEHOLDER: LIVE PRICE TRACKER & DEAL BADGING SCREEN ]\n\n"
            "Shows the real-time pricing and deal analysis dialog (price-tracker.js & price_server.py):\n"
            "- ASIN-verified product detail view displaying live Amazon/Flipkart selling price versus expected market baseline.\n"
            "- Calculated percentage variance (diffPct) with color-coded status badges: 'Good Price' (Green), 'Fair Price' (Blue),\n"
            "  'Slightly Expensive' (Orange), or 'Overpriced' (Red).\n"
            "- In-Stock availability confirmation, last timestamp of price verification, and direct affiliate purchase link."
        )
    },
    19: {  # Figure 7.6 (Table index 19)
        "caption": "Figure 7.6 Progressive Web App Offline Caching and Installation Flow",
        "description": (
            "[ UI SCREENSHOT PLACEHOLDER: PWA OFFLINE CAPABILITY & INSTALLATION SCREEN ]\n\n"
            "Shows the Progressive Web Application execution on mobile and desktop browsers:\n"
            "- Browser 'Install PhonePerfect' prompt generated via manifest.json.\n"
            "- Chrome DevTools Application tab verifying Service Worker registration (service-worker.js) with pre-cached\n"
            "  assets (HTML, CSS, JS, catalog dataset, and iconography).\n"
            "- Demonstration of 100% offline functionality with disconnected network state: catalog browsing, search,\n"
            "  quiz scoring, and multi-device comparison executing seamlessly with zero network latency."
        )
    },
    20: {  # Figure 7.7 (Table index 20)
        "caption": "Figure 7.7 Android Native Container with Synchronous Inset Handling Screen",
        "description": (
            "[ UI SCREENSHOT PLACEHOLDER: NATIVE ANDROID CONTAINER & INSETS SCREEN ]\n\n"
            "Shows the native Android application running on a physical Android 15/16 device (com.phoneperfect.finder):\n"
            "- Full-screen edge-to-edge layout with synchronous status-bar and navigation-bar padding implemented in MainActivity.kt.\n"
            "- Hardware-accelerated WebView rendering the embedded local assets from file:///android_asset/.\n"
            "- Verification of native hardware back-button interceptor dismissing modals gracefully before navigating history.\n"
            "- Production APK/AAB package signatures and Gradle compilation output."
        )
    }
}
