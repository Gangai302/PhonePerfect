from datetime import datetime, timezone
from typing import Dict, Any, List
from app.models.phone import Phone
from app.schemas.phone import RiskReportSchema

class PurchaseRiskAssessmentService:
    """
    Transparent Purchase-Risk Analysis Service for PhonePerfect 2.0.
    Evaluates real purchase risks on:
    - Price reliability & freshness
    - Specification completeness
    - Product release age
    - Ambiguity / gray market exposure
    """

    @classmethod
    def evaluate_risk(cls, phone: Phone, current_price: float, verification_status: str, observed_at: datetime = None) -> RiskReportSchema:
        factors: List[Dict[str, str]] = []
        checklist: List[str] = [
            "Verify box seal and serial/IMEI match invoice",
            "Verify official manufacturer warranty card inside box"
        ]

        risk_score = 15  # Baseline minimal retail risk

        # 1. Price Verification Assessment
        if verification_status == "VERIFIED":
            price_freshness = "Current Verified Catalog / Merchant Data"
        elif verification_status == "ESTIMATED":
            risk_score += 25
            price_freshness = "Estimated pricing based on launch MSRP and category depreciation"
            factors.append({
                "name": "Unconfirmed Live Price",
                "severity": "MEDIUM",
                "description": "Observed price is an algorithmic estimate. Double check live storefront before purchasing.",
                "action_item": "Click Amazon/Flipkart search to confirm live cart price"
            })
            checklist.append("Confirm active pricing and available instant bank discounts at checkout")
        else:
            risk_score += 15
            price_freshness = "Unverified Marketplace Observation"
            factors.append({
                "name": "Marketplace Price Variability",
                "severity": "LOW",
                "description": "Price may vary by vendor, stock batch, or seller rating.",
                "action_item": "Select 'Fulfilled by Amazon' or 'Flipkart Assured' sellers only"
            })

        # 2. Spec Completeness Assessment
        spec = phone.specification
        if not spec:
            risk_score += 35
            spec_completeness = 40
            factors.append({
                "name": "Incomplete Hardware Telemetry",
                "severity": "HIGH",
                "description": "Detailed sensor, cooling, or update metrics are unverified.",
                "action_item": "Verify exact regional variant specs on manufacturer portal"
            })
        else:
            spec_completeness = 95
            if not spec.ip_rating or spec.ip_rating == "None":
                factors.append({
                    "name": "No Official Water/Dust Ingress Rating",
                    "severity": "LOW",
                    "description": "Phone lacks certified IP68/IP65 water protection.",
                    "action_item": "Avoid exposure to moisture or immersion"
                })

        # 3. Device Age & Software Longevity Assessment
        current_year = datetime.now().year
        device_age_months = max(0, (current_year - phone.release_year) * 12)

        if phone.release_year < current_year - 2:
            risk_score += 20
            factors.append({
                "name": "Aging Device Generation",
                "severity": "MEDIUM",
                "description": f"Model was released in {phone.release_year}. Software updates will be limited compared to newer models.",
                "action_item": "Check remaining official Android OS & security patch support schedule"
            })
            checklist.append("Check device manufacture date on box to ensure battery has not sat drained for >12 months")
        else:
            checklist.append("Ensure charger is included in box (some modern flagships omit power adapters)")

        # Final Risk Level Mapping
        risk_score = min(100, max(5, risk_score))
        if risk_score <= 25:
            overall_level = "LOW"
        elif risk_score <= 50:
            overall_level = "MODERATE"
        elif risk_score <= 75:
            overall_level = "HIGH"
        else:
            overall_level = "CRITICAL"

        return RiskReportSchema(
            phone_id=phone.id,
            model_name=phone.model_name,
            overall_risk_level=overall_level,
            overall_risk_score=risk_score,
            price_freshness_status=price_freshness,
            spec_completeness_pct=spec_completeness,
            device_age_months=device_age_months,
            factors=factors,
            buyer_checklist=checklist
        )
