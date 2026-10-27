import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('report_figures', exist_ok=True)

def create_ui_mockup(title, subtitle, filename, items, accent_color="#00D2FF"):
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Mobile / Tablet frame
    ax.add_patch(patches.FancyBboxPatch((0.5, 0.5), 9.0, 6.0, boxstyle="round,pad=0.2", ec="#37474F", fc="#090D16", lw=2))
    
    # Header bar
    ax.add_patch(patches.Rectangle((0.7, 5.5), 8.6, 0.8, ec="#1E293B", fc="#131A2A"))
    ax.text(1.0, 5.9, title, ha="left", va="center", fontsize=11, fontweight="bold", color="#FFFFFF")
    ax.text(9.0, 5.9, "PhonePerfect", ha="right", va="center", fontsize=10, fontweight="bold", color=accent_color)
    
    # Subtitle / info
    ax.text(1.0, 5.2, subtitle, ha="left", va="center", fontsize=9, color="#94A3B8")

    # Content cards
    for idx, (head, body) in enumerate(items):
        y = 4.1 - idx * 1.3
        ax.add_patch(patches.FancyBboxPatch((0.8, y), 8.4, 1.1, boxstyle="round,pad=0.1", ec="#334155", fc="#131A2A", lw=1))
        ax.text(1.1, y + 0.8, head, ha="left", va="center", fontsize=9, fontweight="bold", color="#38BDF8")
        ax.text(1.1, y + 0.4, body, ha="left", va="center", fontsize=8, color="#CBD5E1")

    # Footer dock
    ax.add_patch(patches.Rectangle((0.7, 0.6), 8.6, 0.5, ec="#1E293B", fc="#0F172A"))
    ax.text(5.0, 0.85, "Search  •  Phone Finder Quiz  •  Compare (4)  •  AI Advisor  •  Deals", ha="center", va="center", fontsize=8.5, color="#64748B")

    plt.tight_layout()
    plt.savefig(f'report_figures/{filename}', dpi=300)
    plt.close()
    print(f"Generated {filename}")

# B.1: Login / App Shell
create_ui_mockup(
    "PhonePerfect – Device Discovery Shell",
    "PWA Client Registration & Local Preferences Storage",
    "fig_B_1_login.png",
    [
        ("User Profile & Device Preferences", "Email: student.research@krct.ac.in | Role: Consumer / Tech Enthusiast\nSaved Budget Category: ₹20,000 - ₹30,000 | Target Priorities: Gaming & Battery"),
        ("Local Storage Persistence", "Catalog Dataset: 1,597 Verified Devices Cached | Offline Mode: Ready (PWA Active)\nSession State: Authenticated | Sync Status: Local Cache Fresh (TTL 10 min)"),
        ("Security & Sandboxing", "Zero Third-Party Telemetry • Client-Side Execution • Sandboxed Android WebView")
    ]
)

# B.2: Catalog & Dashboard
create_ui_mockup(
    "Smart Phone Finder & Catalog Dashboard",
    "1,597+ Verified Devices Across 16 Indian Brands with Dynamic Filters",
    "fig_B_2_catalog.png",
    [
        ("Realme GT 6T (8GB/256GB)", "Price: ₹28,999 (Launch: ₹30,999) | Deal: Good Price (Green Badge)\nSpecs: Snapdragon 7+ Gen 3 | 5500 mAh Battery | 120W SuperVOOC | 120Hz LTPO AMOLED"),
        ("OnePlus Nord 4 (8GB/128GB)", "Price: ₹27,999 (Launch: ₹29,999) | Deal: Good Price (Green Badge)\nSpecs: Snapdragon 7+ Gen 3 | 5500 mAh Battery | 100W SuperVOOC | Full Metal Unibody"),
        ("Poco F6 5G (8GB/256GB)", "Price: ₹29,999 (Launch: ₹29,999) | Deal: Fair Price (Blue Badge)\nSpecs: Snapdragon 8s Gen 3 | 5000 mAh Battery | 90W Turbo Charge | 1.5K 120Hz AMOLED")
    ]
)

# B.3: Multi-Criteria Quiz
create_ui_mockup(
    "Multi-Criteria Scoring & Recommendation Wizard",
    "Dynamic Additive Utility Weighting (DecisionEngine.getUserNormalizedWeights)",
    "fig_B_3_quiz.png",
    [
        ("Step 1: Budget Tier Selection", "Active Selection: ₹20,000 - ₹30,000 (Max Cap: ₹30,000 enforced)\nCandidate Phones In Range: 308 Verified Models Evaluated"),
        ("Step 2: Selected Hardware Priorities", "Priorities: [Gaming & Performance (+4.0)] • [Battery & Charging (+4.0)]\nNormalized Weights: Processor 0.313, Battery 0.313, Price 0.125, Camera 0.063, Display 0.063"),
        ("Top Ranked Match: Poco F6 5G (96.4% Match)", "Winning Factors: Flagship Snapdragon 8s Gen 3 Processor, Fast 90W Charging, 1.5K Display\nCalculated Utility Score: 9.64 / 10 | Direct Action: Pin to Compare / View Deal")
    ]
)

# B.4: Side-by-Side Comparison Matrix
create_ui_mockup(
    "Side-by-Side Hardware Comparison Matrix",
    "Evaluating 4 Pinned Devices Simultaneously Across Key Hardware Parameters",
    "fig_B_4_comparison.png",
    [
        ("Hardware Metric: Processor & Gaming Antutu", "Poco F6: Snapdragon 8s Gen 3 (1.53M) [WINNER] | Realme GT 6T: Snapdragon 7+ Gen 3 (1.33M)\nOnePlus Nord 4: Snapdragon 7+ Gen 3 (1.31M) | Motorola Edge 50 Pro: Snapdragon 7 Gen 3 (830K)"),
        ("Hardware Metric: Battery & Fast Charging", "Realme GT 6T: 5500mAh + 120W [WINNER] | OnePlus Nord 4: 5500mAh + 100W\nPoco F6: 5000mAh + 90W | Motorola Edge 50 Pro: 4500mAh + 125W Turbo"),
        ("Hardware Metric: Camera & Sensor Setup", "Motorola Edge 50 Pro: 50MP OIS + 3X Telephoto [WINNER] | Realme GT 6T: 50MP Sony LYT-600 OIS\nOnePlus Nord 4: 50MP Sony LYT-600 OIS | Poco F6: 50MP Sony IMX882 OIS")
    ]
)

# B.5: Conversational AI Advisor
create_ui_mockup(
    "Conversational AI Buying Advisor (ai-chat.js)",
    "Natural Language Intent Classification & Regex Slot-Filling Assistant",
    "fig_B_5_ai_advisor.png",
    [
        ("User Natural Query", "'Suggest me the best gaming phone under 25k with good battery'"),
        ("Advisor NLP Parsing Engine", "Detected Intent: [BEST, GAMING, BATTERY] | Extracted Budget: [0, 25000]\nPriority Weights Boosted: Processor +4.0, Battery +4.0 | Candidates Scored: 290"),
        ("Synthesized Response & Cards", "'Based on your budget under ₹25,000, here are the top 2 gaming performers:\n1. iQOO Z9 Turbo (Dimensity 7200 / 6000mAh) - 94% Match\n2. Realme Narzo 70 Pro (Dimensity 7050 / 5000mAh / 67W) - 91% Match'")
    ]
)

# B.6: Real-Time Price Tracking & Deal Modal
create_ui_mockup(
    "Real-Time E-Commerce Price Monitoring & Deal Modal",
    "Python Flask Microservice (price_server.py) with ASIN Verification & TTL Cache",
    "fig_B_6_deals.png",
    [
        ("Device Identity & Verification", "Model: OnePlus 12R (16GB/256GB) | Verified ASIN: B0CS7W6NKB (Amazon India)\nBaseline Launch Price: ₹45,999 | Expected Market Price: ₹42,999"),
        ("Live Price Status & Margin", "Live Verified Price: ₹38,999 | Percentage Variance: -9.3% (Price Drop)\nStatus Badge: [GOOD PRICE] (Green) | Stock Availability: In Stock (Verified Amazon)"),
        ("Microservice Caching & Security", "Server TTL Cache: Valid (Expires in 8 min 24s) | Endpoint: GET /api/price/B0CS7W6NKB\nDirect Link: Verified Affiliate Portal with Zero Fraudulent Redirect")
    ]
)
