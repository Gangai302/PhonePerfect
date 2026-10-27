import math
from typing import List, Dict, Any, Optional
from app.models.phone import Phone
from app.schemas.phone import RecommendationRequestSchema, RecommendationItemSchema, PhoneCardSchema

class ModernRecommendationEngine:
    """
    Independent multi-criteria recommendation engine for PhonePerfect 2.0.
    Enforces strict hard filtering before applying normalized utility scoring.
    """

    CHIPSET_SCORES = {
        # Flagship Tier (90 - 100)
        "snapdragon 8 elite": 100,
        "apple a18 pro": 99,
        "dimensity 9400": 98,
        "apple a18": 96,
        "snapdragon 8 gen 3": 95,
        "apple a17 pro": 94,
        "dimensity 9300+": 93,
        "dimensity 9300": 92,
        "snapdragon 8s gen 3": 89,
        "apple a16 bionic": 88,
        "snapdragon 8 gen 2": 87,
        # Upper Midrange Tier (75 - 86)
        "dimensity 8300-ultra": 84,
        "snapdragon 7+ gen 3": 83,
        "dimensity 8300": 82,
        "snapdragon 7+ gen 2": 80,
        "tensor g4": 82,
        "tensor g3": 78,
        "snapdragon 7s gen 2": 72,
        "dimensity 7200": 71,
        "dimensity 7050": 68,
        # Midrange Tier (55 - 70)
        "snapdragon 6 gen 1": 65,
        "snapdragon 695": 58,
        "dimensity 6080": 56,
        "helio g99": 50,
    }

    @classmethod
    def get_chipset_score(cls, chipset_name: str) -> float:
        if not chipset_name:
            return 50.0
        chipset_lower = chipset_name.lower().strip()
        for k, v in cls.CHIPSET_SCORES.items():
            if k in chipset_lower:
                return float(v)
        if "snapdragon 8" in chipset_lower or "a18" in chipset_lower or "dimensity 9" in chipset_lower:
            return 90.0
        if "snapdragon 7" in chipset_lower or "dimensity 8" in chipset_lower:
            return 75.0
        if "snapdragon 6" in chipset_lower or "dimensity 7" in chipset_lower:
            return 65.0
        return 55.0

    @classmethod
    def evaluate_phone(
        cls, 
        phone: Phone, 
        request: RecommendationRequestSchema,
        best_price: float,
        price_status: str
    ) -> Optional[RecommendationItemSchema]:
        spec = phone.specification
        base_variant = next((v for v in phone.variants if v.is_base_variant), None) or (phone.variants[0] if phone.variants else None)

        ram = base_variant.ram_gb if base_variant else 8
        storage = base_variant.storage_gb if base_variant else 128

        # --- HARD CONSTRAINTS FILTERING ---
        # 1. Budget Hard Constraint
        if best_price > request.budget_max:
            return None
        
        # 2. Excluded Brands Constraint
        if phone.brand_id.lower() in [b.lower() for b in request.excluded_brands]:
            return None

        # 3. Minimum RAM / Storage Hard Constraints
        if request.min_ram_gb and ram < request.min_ram_gb:
            return None
        if request.min_storage_gb and storage < request.min_storage_gb:
            return None

        # 4. Feature Hard Requirements
        if request.require_5g and spec and not spec.has_5g:
            return None
        if request.require_ois and spec and not spec.rear_camera_has_ois:
            return None

        # --- MULTI-CRITERIA SCORING ---
        why_reasons: List[str] = []
        trade_offs: List[str] = []

        # 1. Performance Dimension (0 - 100)
        chipset_val = cls.get_chipset_score(spec.chipset if spec else "")
        ram_bonus = min(15.0, (ram - 6) * 3.0) if ram >= 6 else -10.0
        perf_score = max(0.0, min(100.0, chipset_val * 0.85 + ram_bonus))

        if perf_score >= 88:
            why_reasons.append(f"Top-tier performance ({spec.chipset if spec else 'Flagship SoC'}, {ram}GB RAM)")
        elif perf_score < 60:
            trade_offs.append(f"Entry-level chipset ({spec.chipset if spec else 'Standard'}) may struggle with intense 3D gaming")

        # 2. Camera Dimension (0 - 100)
        cam_score = 50.0
        if spec:
            cam_score = min(80.0, (spec.rear_camera_primary_mp / 200.0) * 40.0 + 40.0)
            if spec.rear_camera_has_ois:
                cam_score += 12.0
                why_reasons.append("Main camera features Optical Image Stabilization (OIS) for blur-free low-light shots")
            else:
                trade_offs.append("Main camera lacks Optical Image Stabilization (OIS)")
            if spec.rear_camera_telephoto_zoom and spec.rear_camera_telephoto_zoom >= 3.0:
                cam_score += 10.0
                why_reasons.append(f"Dedicated {spec.rear_camera_telephoto_zoom}x optical telephoto lens")
            if spec.selfie_camera_mp >= 32:
                cam_score += 5.0
        cam_score = max(0.0, min(100.0, cam_score))

        # 3. Battery & Charging Dimension (0 - 100)
        battery_score = 60.0
        if spec:
            capacity_score = min(60.0, (spec.battery_mah / 6000.0) * 60.0)
            charge_score = min(40.0, (spec.charging_wattage / 120.0) * 40.0)
            battery_score = capacity_score + charge_score
            if spec.battery_mah >= 5500:
                why_reasons.append(f"High-capacity {spec.battery_mah}mAh battery for prolonged multi-day endurance")
            if spec.charging_wattage >= 67:
                why_reasons.append(f"Ultra-fast {int(spec.charging_wattage)}W rapid wired charging")
            elif spec.charging_wattage <= 25:
                trade_offs.append(f"Charging speed limited to {int(spec.charging_wattage)}W")
            if spec.wireless_charging:
                battery_score = min(100.0, battery_score + 8.0)
                why_reasons.append("Convenient Qi wireless charging supported")
        battery_score = max(0.0, min(100.0, battery_score))

        # 4. Display Dimension (0 - 100)
        display_score = 65.0
        if spec:
            tech_val = 50.0 if "amoled" in spec.display_tech.lower() or "oled" in spec.display_tech.lower() else 30.0
            refresh_val = 30.0 if spec.refresh_rate_hz >= 120 else 15.0
            brightness_val = min(20.0, ((spec.peak_brightness_nits or 1000) / 2500.0) * 20.0)
            display_score = tech_val + refresh_val + brightness_val
            if spec.refresh_rate_hz >= 120:
                why_reasons.append(f"Silky smooth {spec.refresh_rate_hz}Hz {spec.display_tech} panel")
            if "lcd" in spec.display_tech.lower():
                trade_offs.append("Display uses IPS LCD rather than OLED/AMOLED")
        display_score = max(0.0, min(100.0, display_score))

        # 5. Value for Money Dimension (0 - 100)
        # Ratio of overall hardware capability to price utilization
        budget_ratio = best_price / request.budget_max
        hardware_mean = (perf_score + cam_score + battery_score + display_score) / 4.0
        # If high hardware score at lower % of user's budget, value score is very high
        value_score = max(20.0, min(100.0, hardware_mean * 1.15 * (1.1 - 0.2 * budget_ratio)))

        # Weighted aggregate score
        weights = {
            "performance": request.priorities.get("performance", 3),
            "camera": request.priorities.get("camera", 3),
            "battery": request.priorities.get("battery", 3),
            "display": request.priorities.get("display", 3),
            "value": 3
        }

        # Boost primary use weight
        if request.primary_use == "GAMING":
            weights["performance"] += 3
            weights["display"] += 1
        elif request.primary_use == "CAMERA":
            weights["camera"] += 3
        elif request.primary_use == "BATTERY":
            weights["battery"] += 3

        total_weight = sum(weights.values())
        raw_final_score = (
            perf_score * weights["performance"] +
            cam_score * weights["camera"] +
            battery_score * weights["battery"] +
            display_score * weights["display"] +
            value_score * weights["value"]
        ) / total_weight

        final_match_score = int(round(max(10, min(99, raw_final_score))))

        # Summary risk check
        risk_level = "LOW"
        if price_status != "VERIFIED":
            risk_level = "MODERATE"
        if not spec or not spec.rear_camera_has_ois and best_price > 35000:
            trade_offs.append("Lacks OIS at a premium price point")

        phone_card = PhoneCardSchema(
            id=phone.id,
            brand_id=phone.brand_id,
            brand_name=phone.brand.name if phone.brand else phone.brand_id.title(),
            model_name=phone.model_name,
            release_year=phone.release_year,
            canonical_image_url=phone.canonical_image_url,
            best_price=best_price,
            price_verification=price_status,
            chipset=spec.chipset if spec else None,
            ram_gb=ram,
            storage_gb=storage,
            battery_mah=spec.battery_mah if spec else None,
            rear_camera_mp=spec.rear_camera_primary_mp if spec else None
        )

        return RecommendationItemSchema(
            phone=phone_card,
            match_score=final_match_score,
            current_price=best_price,
            price_verification=price_status,
            why_recommended=why_reasons[:4],
            trade_offs=trade_offs[:3],
            score_breakdown={
                "performance": int(round(perf_score)),
                "camera": int(round(cam_score)),
                "battery": int(round(battery_score)),
                "display": int(round(display_score)),
                "value": int(round(value_score))
            },
            risk_summary={
                "level": risk_level,
                "price_fresh": True,
                "verified": price_status == "VERIFIED"
            }
        )
