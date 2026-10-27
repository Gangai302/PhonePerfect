import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('report_figures', exist_ok=True)

# 1. Figure 3.1: Existing System vs Limitations
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis('off')

# Background boxes
# Sources
ax.add_patch(patches.FancyBboxPatch((0.5, 3.8), 2.5, 2.7, boxstyle="round,pad=0.2", ec="#D32F2F", fc="#FFEBEE", lw=1.5))
ax.text(1.75, 6.2, "Current Information Sources", ha="center", va="center", fontsize=11, fontweight="bold", color="#C62828")
sources = ["• Fragmented E-Commerce Portals\n  (Amazon, Flipkart)", "• Static Specification Sites\n  (GSMArena, 91mobiles)", "• Promotional Tech Videos & Blogs\n  (Unvetted marketing claims)"]
for idx, s in enumerate(sources):
    ax.text(0.7, 5.4 - idx*0.75, s, ha="left", va="center", fontsize=9, color="#212121")

# Bottlenecks
ax.add_patch(patches.FancyBboxPatch((3.7, 3.8), 2.7, 2.7, boxstyle="round,pad=0.2", ec="#F57C00", fc="#FFF3E0", lw=1.5))
ax.text(5.05, 6.2, "Manual & Disconnected Process", ha="center", va="center", fontsize=11, fontweight="bold", color="#EF6C00")
bottlenecks = ["1. Technical Jargon Overload\n   (Opaque specs & chip tiers)", "2. Rigid Price Bracket Filters\n   (Missing near-budget deals)", "3. Extreme Price Volatility\n   (Opaque retail discounts)", "4. Inconsistent Spec Records\n   (Missing sensors, fake MP)"]
for idx, b in enumerate(bottlenecks):
    ax.text(3.9, 5.5 - idx*0.55, b, ha="left", va="center", fontsize=8.5, color="#212121")

# Outcomes
ax.add_patch(patches.FancyBboxPatch((7.0, 3.8), 2.5, 2.7, boxstyle="round,pad=0.2", ec="#C2185B", fc="#FCE4EC", lw=1.5))
ax.text(8.25, 6.2, "Consumer Outcomes", ha="center", va="center", fontsize=11, fontweight="bold", color="#AD1457")
outcomes = ["• Severe Choice Paralysis\n  (Endless scrolling & doubt)", "• Suboptimal Purchases\n  (Overpaying for weak specs)", "• Missed Festive Deals\n  (No historic price context)", "• Frustrating Returns\n  (Post-purchase regret)"]
for idx, o in enumerate(outcomes):
    ax.text(7.2, 5.5 - idx*0.55, o, ha="left", va="center", fontsize=8.5, color="#212121")

# Arrows
ax.annotate('', xy=(3.6, 5.15), xytext=(3.1, 5.15), arrowprops=dict(facecolor='#E53935', shrink=0.05, width=2, headwidth=8))
ax.annotate('', xy=(6.9, 5.15), xytext=(6.5, 5.15), arrowprops=dict(facecolor='#E53935', shrink=0.05, width=2, headwidth=8))

# Bottom banner
ax.add_patch(patches.FancyBboxPatch((0.5, 0.8), 9.0, 2.2, boxstyle="round,pad=0.2", ec="#1976D2", fc="#E3F2FD", lw=1.5))
ax.text(5.0, 2.6, "KEY CHALLENGES ADDRESSED BY PHONEPERFECT", ha="center", va="center", fontsize=11, fontweight="bold", color="#0D47A1")
challenges = [
    "• Absence of Multi-Criteria Utility Weighting: Existing portals cannot weigh Camera, Battery, and Gaming simultaneously.",
    "• Fragmented Data & Verification: No central verified catalog linking exact hardware benchmarks to real retail ASINs.",
    "• Zero Conversational Support: Conventional search bars require exact model strings and cannot answer guided queries.",
    "• High Framework Bloat: Heavy commercial web portals suffer from high memory consumption and jank on mobile devices."
]
for idx, c in enumerate(challenges):
    ax.text(0.8, 2.1 - idx*0.4, c, ha="left", va="center", fontsize=9, color="#1565C0")

plt.tight_layout()
plt.savefig('report_figures/fig_3_1_existing_system.png', dpi=300)
plt.close()
print("Generated fig_3_1_existing_system.png")

# 2. Figure 5.5: Proposed System Architecture (PhonePerfect)
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis('off')

# Tier 1: User Entities / Clients
ax.add_patch(patches.FancyBboxPatch((0.5, 5.6), 9.0, 1.1, boxstyle="round,pad=0.15", ec="#2E7D32", fc="#E8F5E9", lw=1.5))
ax.text(1.2, 6.4, "CLIENT LAYER", ha="left", va="center", fontsize=10, fontweight="bold", color="#1B5E20")
ax.add_patch(patches.Rectangle((2.7, 5.8), 3.0, 0.7, ec="#388E3C", fc="#C8E6C9", lw=1))
ax.text(4.2, 6.15, "Mobile & Desktop PWA (Browser)\nService Worker • HTML5 / CSS3 / ES6+", ha="center", va="center", fontsize=8, color="#1B5E20")
ax.add_patch(patches.Rectangle((6.2, 5.8), 3.0, 0.7, ec="#388E3C", fc="#C8E6C9", lw=1))
ax.text(7.7, 6.15, "Native Android App (WebView Container)\nKotlin • Jetpack • Synchronous Inset Padding", ha="center", va="center", fontsize=8, color="#1B5E20")

# Tier 2: Application Intelligence Layer
ax.add_patch(patches.FancyBboxPatch((0.5, 3.8), 9.0, 1.5, boxstyle="round,pad=0.15", ec="#1565C0", fc="#E3F2FD", lw=1.5))
ax.text(1.2, 5.0, "CORE APPLICATION & INTELLIGENCE LAYER", ha="left", va="center", fontsize=10, fontweight="bold", color="#0D47A1")

# Sub modules in app
ax.add_patch(patches.Rectangle((0.8, 4.0), 2.5, 0.8, ec="#1976D2", fc="#BBDEFB", lw=1))
ax.text(2.05, 4.4, "DecisionEngine (app.js)\n• Multi-Criteria Utility Weighting\n• Budget Mapping & Score Ranking", ha="center", va="center", fontsize=7.5, color="#0D47A1")

ax.add_patch(patches.Rectangle((3.6, 4.0), 2.5, 0.8, ec="#1976D2", fc="#BBDEFB", lw=1))
ax.text(4.85, 4.4, "AI Buying Advisor (ai-chat.js)\n• 12 Intent Detection Grammars\n• Price Slot & Brand Keyword Parser", ha="center", va="center", fontsize=7.5, color="#0D47A1")

ax.add_patch(patches.Rectangle((6.4, 4.0), 2.8, 0.8, ec="#1976D2", fc="#BBDEFB", lw=1))
ax.text(7.8, 4.4, "Comparison Matrix & UI (style.css)\n• 4-Device Simultaneous Diff\n• Responsive Glassmorphic Dark UI", ha="center", va="center", fontsize=7.5, color="#0D47A1")

# Tier 3: Data & Backend Layer
ax.add_patch(patches.FancyBboxPatch((0.5, 2.0), 9.0, 1.5, boxstyle="round,pad=0.15", ec="#6A1B9A", fc="#F3E5F5", lw=1.5))
ax.text(1.2, 3.2, "DATA STORAGE & LIVE BACKEND MICROSERVICE", ha="left", va="center", fontsize=10, fontweight="bold", color="#4A148C")

ax.add_patch(patches.Rectangle((0.8, 2.2), 3.8, 0.8, ec="#8E24AA", fc="#E1BEE7", lw=1))
ax.text(2.7, 2.6, "Verified Smartphone Catalog Dataset\n• phones.js & phones.json (1,597+ devices, 16 brands)\n• phone_images_cache.json (Optimized CDN URLs)", ha="center", va="center", fontsize=7.5, color="#4A148C")

ax.add_patch(patches.Rectangle((5.0, 2.2), 4.2, 0.8, ec="#8E24AA", fc="#E1BEE7", lw=1))
ax.text(7.1, 2.6, "Flask Price Monitoring Microservice (price_server.py)\n• ASIN-Verified Price Tracking & 10-Min In-Memory TTL Cache\n• REST Endpoints: /api/price/<asin>, /api/deals, /api/catalog", ha="center", va="center", fontsize=7.5, color="#4A148C")

# Tier 4: Outcomes
ax.add_patch(patches.FancyBboxPatch((0.5, 0.4), 9.0, 1.3, boxstyle="round,pad=0.15", ec="#E65100", fc="#FFF3E0", lw=1.5))
ax.text(1.2, 1.4, "SYSTEM OUTCOMES & VALUE DELIVERED", ha="left", va="center", fontsize=10, fontweight="bold", color="#BF360C")
ax.add_patch(patches.Rectangle((0.8, 0.6), 2.6, 0.6, ec="#FB8C00", fc="#FFE0B2", lw=1))
ax.text(2.1, 0.9, "Zero Choice Paralysis\nTransparent Mathematical Scoring", ha="center", va="center", fontsize=8, color="#BF360C")
ax.add_patch(patches.Rectangle((3.7, 0.6), 2.6, 0.6, ec="#FB8C00", fc="#FFE0B2", lw=1))
ax.text(5.0, 0.9, "100% Offline Resilience\nEmbedded Catalog & PWA Caching", ha="center", va="center", fontsize=8, color="#BF360C")
ax.add_patch(patches.Rectangle((6.6, 0.6), 2.6, 0.6, ec="#FB8C00", fc="#FFE0B2", lw=1))
ax.text(7.9, 0.9, "Verified E-Commerce Deals\nReal-time Status Badges & Alerts", ha="center", va="center", fontsize=8, color="#BF360C")

# Connecting Arrows
ax.annotate('', xy=(5.0, 5.3), xytext=(5.0, 5.6), arrowprops=dict(facecolor='#1976D2', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(5.0, 3.5), xytext=(5.0, 3.8), arrowprops=dict(facecolor='#6A1B9A', shrink=0.05, width=1.5, headwidth=6))
ax.annotate('', xy=(5.0, 1.7), xytext=(5.0, 2.0), arrowprops=dict(facecolor='#E65100', shrink=0.05, width=1.5, headwidth=6))

plt.tight_layout()
plt.savefig('report_figures/fig_5_5_proposed_system.png', dpi=300)
plt.close()
print("Generated fig_5_5_proposed_system.png")

# 3. Figure 9.1: Existing Practice vs PhonePerfect Matrix Diagram
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Table header
headers = ["Capability / Feature", "Conventional Portals", "PhonePerfect Platform"]
widths = [4.5, 2.5, 2.5]
starts = [0.3, 4.8, 7.3]

ax.add_patch(patches.Rectangle((0.2, 7.0), 9.6, 0.8, ec="#37474F", fc="#455A64"))
for idx, h in enumerate(headers):
    ax.text(starts[idx] + widths[idx]/2, 7.4, h, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#FFFFFF")

rows = [
    ("Personalized Multi-Criteria Scoring (Camera, Battery, Gaming)", "No (Static sorting only)", "Yes (Normalized Utility Weights)"),
    ("Feature Trade-off & Compromise Detection", "No (Manual user analysis)", "Yes (Automated highlight engine)"),
    ("Conversational Natural Language Advisor", "No (Keyword search only)", "Yes (12-Intent NLP engine)"),
    ("Simultaneous Multi-Device Hardware Comparison", "Limited (2 devices rigidly)", "Yes (Up to 4 devices dynamic)"),
    ("Real-Time E-Commerce Deal & Margin Verification", "No (Sponsored rankings)", "Yes (ASIN verified, 10-min cache)"),
    ("100% Offline Execution without Internet", "No (Completely network-bound)", "Yes (Offline-ready PWA & Android)"),
    ("Zero Third-Party Tracking & Framework Bloat", "No (Heavy ads & megabyte JS)", "Yes (Vanilla JS ES6+, zero telemetry)")
]

for r_idx, (cap, exist, prop) in enumerate(rows):
    y = 6.2 - r_idx*0.8
    bg = "#F5F5F5" if r_idx % 2 == 0 else "#FFFFFF"
    ax.add_patch(patches.Rectangle((0.2, y), 9.6, 0.8, ec="#CFD8DC", fc=bg))
    ax.text(starts[0] + 0.1, y + 0.4, cap, ha="left", va="center", fontsize=8, color="#212121")
    ax.text(starts[1] + widths[1]/2, y + 0.4, "X  " + exist, ha="center", va="center", fontsize=7.5, color="#D32F2F", fontweight="bold")
    ax.text(starts[2] + widths[2]/2, y + 0.4, "✓  " + prop, ha="center", va="center", fontsize=7.5, color="#2E7D32", fontweight="bold")

plt.tight_layout()
plt.savefig('report_figures/fig_9_1_existing_vs_proposed.png', dpi=300)
plt.close()
print("Generated fig_9_1_existing_vs_proposed.png")

# 4. Figure 9.2: Feature Permission & Access Matrix Diagram
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

ax.add_patch(patches.Rectangle((0.2, 7.0), 9.6, 0.8, ec="#1A237E", fc="#283593"))
headers2 = ["Application Feature / Workflow", "General Shopper", "Power User / Gamer", "Price Hunter"]
starts2 = [0.3, 4.3, 6.3, 8.1]
widths2 = [4.0, 2.0, 1.8, 1.7]
for idx, h in enumerate(headers2):
    ax.text(starts2[idx] + widths2[idx]/2, 7.4, h, ha="center", va="center", fontsize=9, fontweight="bold", color="#FFFFFF")

rows2 = [
    ("Interactive Phone Finder Quiz & Budget Carousel", "Full Access", "Full Access", "Full Access"),
    ("Multi-Attribute Scoring (Camera / Battery / Display)", "Simplified View", "Deep Weight Tuning", "Budget-Clipped"),
    ("Simultaneous 4-Device Comparison Matrix", "Standard Specs", "Chipset & Thermal Diff", "Price & Margin Diff"),
    ("Conversational AI Buying Advisor (ai-chat.js)", "General Guidance", "Chipset / FPS Queries", "Discount / Deal Queries"),
    ("Live E-Commerce Price Verification & Deal Badges", "Good/Fair Status", "Hardware Value Status", "Price Drop Alerts"),
    ("Offline Catalog Browsing (phones.js)", "1,597+ Devices", "1,597+ Devices", "1,597+ Devices"),
    ("External E-Commerce Direct Purchase Routing", "Amazon / Flipkart", "Amazon / Flipkart", "Lowest Verified Store")
]

for r_idx, (feat, g, p, pr) in enumerate(rows2):
    y = 6.2 - r_idx*0.8
    bg = "#F9FBE7" if r_idx % 2 == 0 else "#FFFFFF"
    ax.add_patch(patches.Rectangle((0.2, y), 9.6, 0.8, ec="#C5E1A5", fc=bg))
    ax.text(starts2[0] + 0.1, y + 0.4, feat, ha="left", va="center", fontsize=8, color="#212121")
    ax.text(starts2[1] + widths2[1]/2, y + 0.4, "✓ " + g, ha="center", va="center", fontsize=7.5, color="#1B5E20")
    ax.text(starts2[2] + widths2[2]/2, y + 0.4, "✓ " + p, ha="center", va="center", fontsize=7.5, color="#0D47A1")
    ax.text(starts2[3] + widths2[3]/2, y + 0.4, "✓ " + pr, ha="center", va="center", fontsize=7.5, color="#E65100")

plt.tight_layout()
plt.savefig('report_figures/fig_9_2_role_matrix.png', dpi=300)
plt.close()
print("Generated fig_9_2_role_matrix.png")
