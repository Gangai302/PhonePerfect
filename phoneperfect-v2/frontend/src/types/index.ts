export interface Brand {
  id: string;
  name: string;
  country?: string;
  official_website?: string;
  logo_url?: string;
}

export interface Specification {
  chipset: string;
  chipset_tier: string;
  cpu_summary?: string;
  gpu?: string;
  display_size_in: number;
  display_tech: string;
  refresh_rate_hz: number;
  peak_brightness_nits?: number;
  rear_camera_primary_mp: number;
  rear_camera_has_ois: boolean;
  rear_camera_telephoto_zoom?: number;
  selfie_camera_mp: number;
  battery_mah: number;
  charging_wattage: number;
  wireless_charging: boolean;
  ip_rating?: string;
  os_version: string;
  update_support_years?: number;
  has_5g: boolean;
  has_nfc: boolean;
  weight_grams?: number;
}

export interface PriceObservation {
  source_id: string;
  source_name?: string;
  price_amount: number;
  currency: string;
  verification_status: 'VERIFIED' | 'UNVERIFIED' | 'ESTIMATED' | 'OUT_OF_STOCK';
  source_url?: string;
  observed_at: string;
}

export interface PhoneCard {
  id: string;
  brand_id: string;
  brand_name: string;
  model_name: string;
  release_year: number;
  canonical_image_url: string;
  best_price?: number;
  price_verification: string;
  chipset?: string;
  ram_gb?: number;
  storage_gb?: number;
  battery_mah?: number;
  rear_camera_mp?: number;
}

export interface PhoneDetail {
  id: string;
  brand: Brand;
  model_name: string;
  release_year: number;
  canonical_image_url: string;
  is_active: boolean;
  specification?: Specification;
  variants: Array<{
    id: string;
    ram_gb: number;
    storage_gb: number;
    color_name?: string;
    is_base_variant: boolean;
    launch_price_inr?: number;
  }>;
  prices: PriceObservation[];
}

export interface RecommendationRequest {
  budget_max: number;
  primary_use: string;
  priorities: {
    performance: number;
    camera: number;
    battery: number;
    display: number;
    longevity: number;
  };
  min_ram_gb?: number;
  min_storage_gb?: number;
  excluded_brands?: string[];
  require_5g?: boolean;
  require_ois?: boolean;
}

export interface RecommendationItem {
  phone: PhoneCard;
  match_score: number;
  current_price: number;
  price_verification: string;
  why_recommended: string[];
  trade_offs: string[];
  score_breakdown: {
    performance: number;
    camera: number;
    battery: number;
    display: number;
    value: number;
  };
  risk_summary: {
    level: string;
    price_fresh: boolean;
    verified: boolean;
  };
}

export interface RecommendationResponse {
  budget_max: number;
  eligible_count: number;
  total_evaluated: number;
  recommendations: RecommendationItem[];
}

export interface RiskReport {
  phone_id: string;
  model_name: string;
  overall_risk_level: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  overall_risk_score: number;
  price_freshness_status: string;
  spec_completeness_pct: number;
  device_age_months: number;
  factors: Array<{
    name: string;
    severity: string;
    description: string;
    action_item: string;
  }>;
  buyer_checklist: string[];
}
