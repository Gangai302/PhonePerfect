import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class Brand(Base):
    __tablename__ = "brands"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=True)
    country = Column(String(64), nullable=True)
    official_website = Column(String(256), nullable=True)
    logo_url = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    phones = relationship("Phone", back_populates="brand", cascade="all, delete-orphan")


class Phone(Base):
    __tablename__ = "phones"

    id = Column(String(128), primary_key=True, index=True)
    brand_id = Column(String(64), ForeignKey("brands.id"), nullable=False, index=True)
    model_name = Column(String(160), nullable=False, index=True)
    release_year = Column(Integer, nullable=False, default=2024)
    release_date = Column(Date, nullable=True)
    canonical_image_url = Column(String(512), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    brand = relationship("Brand", back_populates="phones")
    specification = relationship("Specification", back_populates="phone", uselist=False, cascade="all, delete-orphan")
    variants = relationship("DeviceVariant", back_populates="phone", cascade="all, delete-orphan")
    price_observations = relationship("PriceObservation", back_populates="phone", cascade="all, delete-orphan")
    saved_entries = relationship("SavedPhone", back_populates="phone", cascade="all, delete-orphan")


class DeviceVariant(Base):
    __tablename__ = "device_variants"

    id = Column(String(160), primary_key=True, index=True)
    phone_id = Column(String(128), ForeignKey("phones.id"), nullable=False, index=True)
    ram_gb = Column(Integer, nullable=False)
    storage_gb = Column(Integer, nullable=False)
    color_name = Column(String(64), nullable=True)
    sku = Column(String(64), nullable=True)
    is_base_variant = Column(Boolean, nullable=False, default=False)
    launch_price_inr = Column(Float, nullable=True)

    phone = relationship("Phone", back_populates="variants")
    price_observations = relationship("PriceObservation", back_populates="variant")


class Specification(Base):
    __tablename__ = "specifications"

    phone_id = Column(String(128), ForeignKey("phones.id"), primary_key=True)
    chipset = Column(String(128), nullable=False)
    chipset_tier = Column(String(32), nullable=False, default="MIDRANGE")  # FLAGSHIP, UPPER_MID, MIDRANGE, ENTRY
    cpu_summary = Column(String(128), nullable=True)
    gpu = Column(String(64), nullable=True)
    
    display_size_in = Column(Float, nullable=False, default=6.5)
    display_tech = Column(String(64), nullable=False, default="AMOLED")
    refresh_rate_hz = Column(Integer, nullable=False, default=120)
    peak_brightness_nits = Column(Integer, nullable=True, default=1000)
    
    rear_camera_primary_mp = Column(Float, nullable=False, default=50.0)
    rear_camera_has_ois = Column(Boolean, nullable=False, default=False)
    rear_camera_telephoto_zoom = Column(Float, nullable=True, default=0.0)
    selfie_camera_mp = Column(Float, nullable=False, default=16.0)
    
    battery_mah = Column(Integer, nullable=False, default=5000)
    charging_wattage = Column(Float, nullable=False, default=33.0)
    wireless_charging = Column(Boolean, nullable=False, default=False)
    
    ip_rating = Column(String(16), nullable=True)
    os_version = Column(String(64), nullable=False, default="Android 14")
    update_support_years = Column(Integer, nullable=True, default=3)
    has_5g = Column(Boolean, nullable=False, default=True)
    has_nfc = Column(Boolean, nullable=False, default=True)
    weight_grams = Column(Float, nullable=True, default=190.0)
    raw_specs_json = Column(JSON, nullable=True)

    phone = relationship("Phone", back_populates="specification")


class PriceSource(Base):
    __tablename__ = "price_sources"

    id = Column(String(32), primary_key=True)  # amazon_in, flipkart, official_store
    display_name = Column(String(64), nullable=False)
    base_url = Column(String(256), nullable=False)
    is_verified_partner = Column(Boolean, nullable=False, default=False)
    reliability_rating = Column(Float, nullable=False, default=0.85)

    price_observations = relationship("PriceObservation", back_populates="source")


class PriceObservation(Base):
    __tablename__ = "price_observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_id = Column(String(128), ForeignKey("phones.id"), nullable=False, index=True)
    variant_id = Column(String(160), ForeignKey("device_variants.id"), nullable=True)
    source_id = Column(String(32), ForeignKey("price_sources.id"), nullable=False)
    price_amount = Column(Float, nullable=False)
    currency = Column(String(8), nullable=False, default="INR")
    verification_status = Column(String(24), nullable=False, default="VERIFIED")  # VERIFIED, UNVERIFIED, ESTIMATED
    source_url = Column(String(1024), nullable=True)
    observed_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    is_current = Column(Boolean, nullable=False, default=True)

    phone = relationship("Phone", back_populates="price_observations")
    variant = relationship("DeviceVariant", back_populates="price_observations")
    source = relationship("PriceSource", back_populates="price_observations")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(String(64), primary_key=True)
    budget_max_inr = Column(Float, nullable=False)
    primary_use = Column(String(32), nullable=False, default="DAILY")
    gaming_priority = Column(Integer, nullable=False, default=3)
    camera_priority = Column(Integer, nullable=False, default=3)
    battery_priority = Column(Integer, nullable=False, default=3)
    min_ram_gb = Column(Integer, nullable=True)
    min_storage_gb = Column(Integer, nullable=True)
    excluded_brands = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class SavedPhone(Base):
    __tablename__ = "saved_phones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_session_id = Column(String(64), nullable=False, index=True)
    phone_id = Column(String(128), ForeignKey("phones.id"), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    phone = relationship("Phone", back_populates="saved_entries")
