from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class BrandBase(BaseModel):
    id: str
    name: str
    country: Optional[str] = None
    official_website: Optional[str] = None
    logo_url: Optional[str] = None

    class Config:
        from_attributes = True


class VariantBase(BaseModel):
    id: str
    ram_gb: int
    storage_gb: int
    color_name: Optional[str] = None
    is_base_variant: bool = False
    launch_price_inr: Optional[float] = None

    class Config:
        from_attributes = True


class SpecificationBase(BaseModel):
    chipset: str
    chipset_tier: str
    cpu_summary: Optional[str] = None
    gpu: Optional[str] = None
    display_size_in: float
    display_tech: str
    refresh_rate_hz: int
    peak_brightness_nits: Optional[int] = None
    rear_camera_primary_mp: float
    rear_camera_has_ois: bool
    rear_camera_telephoto_zoom: Optional[float] = None
    selfie_camera_mp: float
    battery_mah: int
    charging_wattage: float
    wireless_charging: bool
    ip_rating: Optional[str] = None
    os_version: str
    update_support_years: Optional[int] = None
    has_5g: bool
    has_nfc: bool
    weight_grams: Optional[float] = None

    class Config:
        from_attributes = True


class PriceObservationBase(BaseModel):
    source_id: str
    source_name: Optional[str] = None
    price_amount: float
    currency: str = "INR"
    verification_status: str
    source_url: Optional[str] = None
    observed_at: datetime

    class Config:
        from_attributes = True


class PhoneCardSchema(BaseModel):
    id: str
    brand_id: str
    brand_name: str
    model_name: str
    release_year: int
    canonical_image_url: str
    best_price: Optional[float] = None
    price_verification: str = "VERIFIED"
    chipset: Optional[str] = None
    ram_gb: Optional[int] = None
    storage_gb: Optional[int] = None
    battery_mah: Optional[int] = None
    rear_camera_mp: Optional[float] = None

    class Config:
        from_attributes = True


class PhoneDetailSchema(BaseModel):
    id: str
    brand: BrandBase
    model_name: str
    release_year: int
    canonical_image_url: str
    is_active: bool
    specification: Optional[SpecificationBase] = None
    variants: List[VariantBase] = []
    prices: List[PriceObservationBase] = []

    class Config:
        from_attributes = True


class CatalogFilterParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    brand: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    search: Optional[str] = None
    chipset_tier: Optional[str] = None
    sort_by: Optional[str] = "price_asc"


class RecommendationRequestSchema(BaseModel):
    budget_max: float = Field(..., gt=0, description="Strict hard upper budget limit in INR")
    primary_use: str = Field("DAILY", description="GAMING, CAMERA, DAILY, BATTERY, WORK")
    priorities: Dict[str, int] = Field(
        default_factory=lambda: {
            "performance": 3,
            "camera": 3,
            "battery": 3,
            "display": 3,
            "longevity": 3
        }
    )
    min_ram_gb: Optional[int] = Field(None, ge=4)
    min_storage_gb: Optional[int] = Field(None, ge=64)
    excluded_brands: List[str] = Field(default_factory=list)
    require_5g: bool = True
    require_ois: bool = False


class RecommendationItemSchema(BaseModel):
    phone: PhoneCardSchema
    match_score: int = Field(..., ge=0, le=100)
    current_price: float
    price_verification: str
    why_recommended: List[str]
    trade_offs: List[str]
    score_breakdown: Dict[str, int]
    risk_summary: Dict[str, Any]


class RecommendationResponseSchema(BaseModel):
    budget_max: float
    eligible_count: int
    total_evaluated: int
    recommendations: List[RecommendationItemSchema]


class ComparisonRequestSchema(BaseModel):
    phone_ids: List[str] = Field(..., min_length=2, max_length=4)


class ComparisonResponseSchema(BaseModel):
    phones: List[PhoneDetailSchema]
    spec_comparison: Dict[str, Dict[str, Any]]
    advantages: Dict[str, List[str]]


class RiskReportSchema(BaseModel):
    phone_id: str
    model_name: str
    overall_risk_level: str  # LOW, MODERATE, HIGH, CRITICAL
    overall_risk_score: int  # 0 to 100
    price_freshness_status: str
    spec_completeness_pct: int
    device_age_months: int
    factors: List[Dict[str, str]]
    buyer_checklist: List[str]
