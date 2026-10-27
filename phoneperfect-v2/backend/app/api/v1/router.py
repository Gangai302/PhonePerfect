from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.core.database import get_db
from app.models.phone import Phone, Brand, DeviceVariant, Specification, PriceObservation
from app.schemas.phone import (
    PhoneCardSchema, PhoneDetailSchema, BrandBase, 
    RecommendationRequestSchema, RecommendationResponseSchema,
    ComparisonRequestSchema, ComparisonResponseSchema,
    RiskReportSchema, PriceObservationBase
)
from app.services.recommendation_engine import ModernRecommendationEngine
from app.services.risk_service import PurchaseRiskAssessmentService

api_router = APIRouter()

# --- HEALTH & STATUS ---
@api_router.get("/health")
def get_health(db: Session = Depends(get_db)):
    catalog_count = db.query(Phone).count()
    return {
        "status": "healthy",
        "app": "PhonePerfect 2.0 API",
        "version": "2.0.0",
        "database_connected": True,
        "total_catalog_devices": catalog_count
    }

# --- BRANDS ---
@api_router.get("/brands", response_model=List[BrandBase])
def get_brands(db: Session = Depends(get_db)):
    return db.query(Brand).order_by(Brand.name.asc()).all()

# --- CATALOG SEARCH & LISTING ---
@api_router.get("/catalog")
def get_catalog(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    chipset_tier: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Phone).filter(Phone.is_active == True)

    if brand:
        query = query.filter(Phone.brand_id == brand.lower().strip())
    
    if search:
        search_term = f"%{search.strip()}%"
        query = query.join(Phone.specification, isouter=True).filter(
            or_(
                Phone.model_name.ilike(search_term),
                Phone.brand_id.ilike(search_term),
                Specification.chipset.ilike(search_term)
            )
        )

    if chipset_tier:
        query = query.join(Phone.specification).filter(Specification.chipset_tier == chipset_tier.upper())

    total = query.count()
    phones = query.offset((page - 1) * limit).limit(limit).all()

    items = []
    for p in phones:
        # Get latest active price
        latest_price_obs = db.query(PriceObservation).filter(
            PriceObservation.phone_id == p.id,
            PriceObservation.is_current == True
        ).first()

        best_price = latest_price_obs.price_amount if latest_price_obs else 0.0
        price_status = latest_price_obs.verification_status if latest_price_obs else "UNVERIFIED"

        # Apply price filters if given
        if min_price and best_price < min_price:
            continue
        if max_price and best_price > max_price:
            continue

        base_variant = next((v for v in p.variants if v.is_base_variant), None) or (p.variants[0] if p.variants else None)

        items.append(PhoneCardSchema(
            id=p.id,
            brand_id=p.brand_id,
            brand_name=p.brand.name if p.brand else p.brand_id.title(),
            model_name=p.model_name,
            release_year=p.release_year,
            canonical_image_url=p.canonical_image_url,
            best_price=best_price,
            price_verification=price_status,
            chipset=p.specification.chipset if p.specification else None,
            ram_gb=base_variant.ram_gb if base_variant else None,
            storage_gb=base_variant.storage_gb if base_variant else None,
            battery_mah=p.specification.battery_mah if p.specification else None,
            rear_camera_mp=p.specification.rear_camera_primary_mp if p.specification else None
        ))

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

# --- PHONE DETAIL ---
@api_router.get("/catalog/{phone_id}", response_model=PhoneDetailSchema)
def get_phone_detail(phone_id: str, db: Session = Depends(get_db)):
    phone = db.query(Phone).filter(Phone.id == phone_id).first()
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found in catalog")
    
    price_observations = db.query(PriceObservation).filter(PriceObservation.phone_id == phone_id).all()
    price_list = [
        PriceObservationBase(
            source_id=obs.source_id,
            source_name=obs.source.display_name if obs.source else obs.source_id,
            price_amount=obs.price_amount,
            currency=obs.currency,
            verification_status=obs.verification_status,
            source_url=obs.source_url,
            observed_at=obs.observed_at
        ) for obs in price_observations
    ]

    return PhoneDetailSchema(
        id=phone.id,
        brand=BrandBase.from_orm(phone.brand),
        model_name=phone.model_name,
        release_year=phone.release_year,
        canonical_image_url=phone.canonical_image_url,
        is_active=phone.is_active,
        specification=phone.specification,
        variants=phone.variants,
        prices=price_list
    )

# --- RECOMMENDATION ENGINE ---
@api_router.post("/recommendations", response_model=RecommendationResponseSchema)
def get_recommendations(request: RecommendationRequestSchema, db: Session = Depends(get_db)):
    all_phones = db.query(Phone).filter(Phone.is_active == True).all()

    evaluated_items = []
    for p in all_phones:
        latest_price_obs = db.query(PriceObservation).filter(
            PriceObservation.phone_id == p.id,
            PriceObservation.is_current == True
        ).first()

        price_amount = latest_price_obs.price_amount if latest_price_obs else 0.0
        price_status = latest_price_obs.verification_status if latest_price_obs else "UNVERIFIED"

        evaluated = ModernRecommendationEngine.evaluate_phone(
            phone=p,
            request=request,
            best_price=price_amount,
            price_status=price_status
        )
        if evaluated:
            evaluated_items.append(evaluated)

    # Sort descending by match_score
    evaluated_items.sort(key=lambda x: x.match_score, reverse=True)

    return RecommendationResponseSchema(
        budget_max=request.budget_max,
        eligible_count=len(evaluated_items),
        total_evaluated=len(all_phones),
        recommendations=evaluated_items[:15]  # Top 15 matching picks
    )

# --- PHONE COMPARISON ---
@api_router.post("/compare", response_model=ComparisonResponseSchema)
def compare_phones(request: ComparisonRequestSchema, db: Session = Depends(get_db)):
    phones = db.query(Phone).filter(Phone.id.in_(request.phone_ids)).all()
    if len(phones) < 2:
        raise HTTPException(status_code=400, detail="At least 2 valid phones are required for comparison")

    phone_details = []
    advantages = {p.id: [] for p in phones}

    for p in phones:
        obs = db.query(PriceObservation).filter(PriceObservation.phone_id == p.id).all()
        prices = [
            PriceObservationBase(
                source_id=o.source_id,
                price_amount=o.price_amount,
                currency=o.currency,
                verification_status=o.verification_status,
                source_url=o.source_url,
                observed_at=o.observed_at
            ) for o in obs
        ]
        phone_details.append(PhoneDetailSchema(
            id=p.id,
            brand=BrandBase.from_orm(p.brand),
            model_name=p.model_name,
            release_year=p.release_year,
            canonical_image_url=p.canonical_image_url,
            is_active=p.is_active,
            specification=p.specification,
            variants=p.variants,
            prices=prices
        ))

    # Evaluate relative advantages
    max_battery = max(p.specification.battery_mah for p in phones if p.specification)
    max_charging = max(p.specification.charging_wattage for p in phones if p.specification)
    max_refresh = max(p.specification.refresh_rate_hz for p in phones if p.specification)

    for p in phones:
        if p.specification:
            if p.specification.battery_mah == max_battery and p.specification.battery_mah > 5000:
                advantages[p.id].append(f"Class-leading battery: {p.specification.battery_mah}mAh")
            if p.specification.charging_wattage == max_charging and p.specification.charging_wattage > 45:
                advantages[p.id].append(f"Fastest charging: {int(p.specification.charging_wattage)}W")
            if p.specification.refresh_rate_hz == max_refresh and max_refresh > 60:
                advantages[p.id].append(f"Highest refresh rate: {p.specification.refresh_rate_hz}Hz")
            if p.specification.rear_camera_has_ois:
                advantages[p.id].append("Optical Image Stabilization (OIS)")
            if p.specification.wireless_charging:
                advantages[p.id].append("Wireless charging supported")

    spec_comparison = {
        "chipset": {p.id: p.specification.chipset if p.specification else "N/A" for p in phones},
        "display": {p.id: f"{p.specification.display_size_in}\" {p.specification.display_tech} {p.specification.refresh_rate_hz}Hz" if p.specification else "N/A" for p in phones},
        "battery": {p.id: f"{p.specification.battery_mah}mAh ({int(p.specification.charging_wattage)}W)" if p.specification else "N/A" for p in phones},
        "camera": {p.id: f"{p.specification.rear_camera_primary_mp}MP (OIS: {'Yes' if p.specification and p.specification.rear_camera_has_ois else 'No'})" if p.specification else "N/A" for p in phones},
        "ip_rating": {p.id: p.specification.ip_rating if p.specification else "None" for p in phones}
    }

    return ComparisonResponseSchema(
        phones=phone_details,
        spec_comparison=spec_comparison,
        advantages=advantages
    )

# --- PURCHASE RISK ASSESSMENT ---
@api_router.get("/risk/{phone_id}", response_model=RiskReportSchema)
def get_phone_risk(phone_id: str, db: Session = Depends(get_db)):
    phone = db.query(Phone).filter(Phone.id == phone_id).first()
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found")

    latest_price_obs = db.query(PriceObservation).filter(
        PriceObservation.phone_id == phone.id,
        PriceObservation.is_current == True
    ).first()

    price = latest_price_obs.price_amount if latest_price_obs else 0.0
    status = latest_price_obs.verification_status if latest_price_obs else "UNVERIFIED"

    return PurchaseRiskAssessmentService.evaluate_risk(phone, price, status)

# --- PRICING OBSERVATIONS ---
@api_router.get("/pricing/{phone_id}")
def get_phone_pricing(phone_id: str, db: Session = Depends(get_db)):
    phone = db.query(Phone).filter(Phone.id == phone_id).first()
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found")

    observations = db.query(PriceObservation).filter(PriceObservation.phone_id == phone_id).all()
    return {
        "phone_id": phone_id,
        "model_name": phone.model_name,
        "observations": [
            {
                "source": obs.source.display_name if obs.source else obs.source_id,
                "price": obs.price_amount,
                "currency": obs.currency,
                "verification_status": obs.verification_status,
                "source_url": obs.source_url,
                "observed_at": obs.observed_at
            }
            for obs in observations
        ]
    }
