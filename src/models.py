"""
Saffire EV - Pydantic Data Models
Defines strict schemas for vehicle platforms, technical specs, TCO calculations,
FAQs, regional hubs, and JSON-LD structured data.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, HttpUrl, ConfigDict


class TechnicalSpec(BaseModel):
    category: str = Field(..., description="Specification category, e.g. Powertrain, Chassis")
    label: str = Field(..., description="Specification label, e.g. Battery Capacity")
    value: str = Field(..., description="Human-readable specification value")
    icon: Optional[str] = Field(None, description="Material Symbols icon name")
    highlight: bool = Field(False, description="Whether to highlight in quick glance tables")


class VehiclePlatform(BaseModel):
    id: str = Field(..., description="Unique slug identifier (saffire-smart-ride, saffire-swiss-cargo)")
    name: str = Field(..., description="Official vehicle commercial name")
    tagline: str = Field(..., description="Marketing/engineering tagline")
    segment: str = Field(..., description="Vehicle category / classification")
    l5_category: str = Field(..., description="L5M (Passenger) or L5N (Cargo)")
    url_path: str = Field(..., description="Clean canonical URL path")
    battery_kwh: float = Field(..., description="Battery pack energy capacity in kWh")
    battery_spec: str = Field(..., description="Detailed battery configuration")
    range_km: int = Field(..., description="Certified operating range per single charge in km")
    peak_power_kw: float = Field(..., description="Peak electric motor output in kW")
    peak_power_spec: str = Field(..., description="Detailed powertrain motor specification")
    top_speed_kmh: int = Field(..., description="Top governed speed in km/h")
    payload_kg: int = Field(..., description="Rated commercial payload capacity in kg")
    wheelbase_mm: int = Field(..., description="Wheelbase measurement in mm")
    tyre_spec: str = Field(..., description="Tyre size and configuration")
    gradability_pct: int = Field(..., description="Grade climbing capability in percentage")
    charging_time_hrs: str = Field(..., description="Charging time from standard socket")
    seating_capacity: Optional[str] = Field(None, description="Seating layout if passenger")
    cargo_volume: Optional[str] = Field(None, description="Cargo bed dimensions / volume if cargo")
    hero_image: str = Field(..., description="Hero vehicle render path")
    transparent_image: str = Field(..., description="Transparent cutout image path")
    brochure_pdf: str = Field(..., description="Direct link to downloadable PDF brochure")
    key_features: List[str] = Field(default_factory=list, description="List of signature features")
    specs: List[TechnicalSpec] = Field(default_factory=list, description="Complete technical specs table")
    description: str = Field(..., description="Rich technical description for SEO/GEO")
    meta_title: str = Field(..., description="Page SEO meta title")
    meta_description: str = Field(..., description="Page SEO meta description")
    h1_title: str = Field(..., description="Page H1 title")


class TCOTier(BaseModel):
    daily_km: int = Field(..., description="Daily operating distance in km")
    years: int = Field(..., description="Duration of vehicle ownership in years")
    ev_rate_per_km: float = Field(1.20, description="Saffire EV electricity cost per km")
    diesel_rate_per_km: float = Field(5.50, description="Standard diesel running cost per km")
    cng_rate_per_km: float = Field(3.50, description="Standard CNG running cost per km")
    ev_monthly_cost: int = Field(..., description="Total monthly fuel/power cost for EV")
    diesel_monthly_cost: int = Field(..., description="Total monthly fuel cost for Diesel")
    cng_monthly_cost: int = Field(..., description="Total monthly fuel cost for CNG")
    monthly_extra_profit_vs_diesel: int = Field(..., description="Net extra monthly profit vs diesel")
    monthly_extra_profit_vs_cng: int = Field(..., description="Net extra monthly profit vs CNG")
    cumulative_savings_vs_diesel: int = Field(..., description="Total savings over ownership duration")
    cumulative_savings_vs_cng: int = Field(..., description="Total savings over ownership duration vs CNG")
    roi_percent_gain_vs_diesel: float = Field(..., description="Percentage profit gain vs diesel")


class FAQItem(BaseModel):
    question: str = Field(..., description="User query / intent-focused question")
    answer: str = Field(..., description="Comprehensive factual answer")
    category: str = Field("General", description="Topic category for grouping")


class RegionalDealerHub(BaseModel):
    city: str = Field(..., description="City name")
    state: str = Field(..., description="State or Union Territory")
    slug: str = Field(..., description="URL slug")
    hub_type: str = Field("Regional Experience & Service Hub", description="Hub classification")
    address: str = Field(..., description="Full operational postal address")
    pincode: str = Field(..., description="Indian Postal PIN code")
    latitude: float = Field(..., description="Geographical latitude")
    longitude: float = Field(..., description="Geographical longitude")
    phone: str = Field(..., description="Direct contact phone number")
    email: str = Field(..., description="Official correspondence email")
    operating_hours: str = Field("Mon - Sat: 9:00 AM - 7:00 PM", description="Business hours")
    is_headquarters: bool = Field(False, description="True if corporate HQ / primary factory")


class JSONLDGraph(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    context: str = Field("https://schema.org", alias="@context")
    graph: List[Dict[str, Any]] = Field(..., alias="@graph")
