"""
Saffire EV - FastAPI Local Preview & API Server
Provides dynamic endpoints for local development, testing,
TCO calculations, catalog data, and lead query submissions.

Run with:
    uvicorn app:app --reload --port 8000
"""
from __future__ import annotations

import os
import json
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Query, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.seo_geo_compiler import compile_catalog_api, compile_tco_api
from src.tco_engine import calculate_tco, RATES

app = FastAPI(
    title="Saffire EV & KOYO Gears India Engine API",
    description="High-performance programmatic API engine for Saffire EV vehicle specs, commercial TCO matrix, and customer lead acquisition.",
    version="1.0.0"
)

# In-memory store or local log for inquiry leads
LEADS_FILE = os.path.join(os.path.dirname(__file__), "lead_submissions.jsonl")


class LeadSubmission(BaseModel):
    name: str = Field(..., min_length=2, description="Customer or prospective dealer full name")
    phone: str = Field(..., pattern=r"^[6-9]\d{9}$", description="10-digit Indian phone number")
    city: str = Field(..., description="Customer city")
    platform: Optional[str] = Field("Both Platforms", description="Selected vehicle model")
    intent: Optional[str] = Field("preorder", description="Inquiry intent: preorder, dealer, fleet")
    notes: Optional[str] = Field("", description="Optional requirement notes or calculator context")
    source: Optional[str] = Field("", description="Source URL where inquiry originated")
    timestamp: Optional[str] = Field(None, description="ISO timestamp")


@app.get("/api/v1/catalog", summary="Get Saffire EV Vehicle Platforms & Entity Data")
def get_catalog():
    """Returns complete machine-readable vehicle platform specifications, hubs, and company details."""
    return JSONResponse(content=compile_catalog_api())


@app.get("/api/v1/tco-matrix", summary="Get Pre-Computed Commercial TCO Matrix")
def get_tco_matrix_endpoint():
    """Returns pre-computed multi-year TCO matrix comparing Saffire EV against Diesel, CNG, and Petrol."""
    return JSONResponse(content=compile_tco_api())


@app.get("/api/v1/calculate-tco", summary="Calculate On-the-Fly Commercial TCO Savings")
def calculate_custom_tco(
    km: int = Query(120, ge=10, le=500, description="Daily run distance in km"),
    years: int = Query(5, ge=1, le=10, description="Ownership period in years"),
    fuel: str = Query("diesel", description="Fuel to compare against: diesel, cng, petrol")
):
    """Calculates custom operational economics, fuel costs, monthly extra profit, and lifetime savings."""
    if fuel.lower() not in RATES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid fuel type '{fuel}'. Valid types: {list(RATES.keys())}"
        )
    result = calculate_tco(daily_km=km, years=years, fuel=fuel)
    return JSONResponse(content=result)


@app.post("/api/v1/submit-query", summary="Submit Quick Query / Dealership Lead")
def submit_query(lead: LeadSubmission):
    """Accepts and records customer and prospective dealer inquiries."""
    record = lead.model_dump()
    if not record.get("timestamp"):
        record["timestamp"] = datetime.utcnow().isoformat() + "Z"

    # Append to local JSONL log
    try:
        with open(LEADS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as e:
        pass

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "status": "success",
            "message": "Lead received successfully. Regional sales hub will respond within 2 hours.",
            "data": record
        }
    )


# Serve root static assets and directory indexes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
def serve_home():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/about/")
@app.get("/about")
def serve_about():
    return FileResponse(os.path.join(BASE_DIR, "about", "index.html"))

@app.get("/koyo-gears-india/")
@app.get("/koyo-gears-india")
def serve_koyo_gears():
    return FileResponse(os.path.join(BASE_DIR, "koyo-gears-india", "index.html"))

@app.get("/vision/")
@app.get("/vision")
def serve_vision():
    return FileResponse(os.path.join(BASE_DIR, "vision", "index.html"))

@app.get("/products/")
@app.get("/products")
def serve_products():
    return FileResponse(os.path.join(BASE_DIR, "products", "index.html"))

@app.get("/products/saffire-smart-ride/")
@app.get("/products/saffire-smart-ride")
def serve_smart_ride():
    return FileResponse(os.path.join(BASE_DIR, "products", "saffire-smart-ride", "index.html"))

@app.get("/products/saffire-swiss-cargo/")
@app.get("/products/saffire-swiss-cargo")
def serve_swiss_cargo():
    return FileResponse(os.path.join(BASE_DIR, "products", "saffire-swiss-cargo", "index.html"))

@app.get("/ev-dealership-india/")
@app.get("/ev-dealership-india")
def serve_dealership():
    return FileResponse(os.path.join(BASE_DIR, "ev-dealership-india", "index.html"))

@app.get("/contact/")
@app.get("/contact")
def serve_contact():
    return FileResponse(os.path.join(BASE_DIR, "contact", "index.html"))

@app.get("/terms/")
@app.get("/terms")
def serve_terms():
    return FileResponse(os.path.join(BASE_DIR, "terms", "index.html"))

# Mount remaining static files (images, assets, etc.)
if os.path.isdir(os.path.join(BASE_DIR, "images")):
    app.mount("/images", StaticFiles(directory=os.path.join(BASE_DIR, "images")), name="images")
if os.path.isdir(os.path.join(BASE_DIR, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(BASE_DIR, "assets")), name="assets")
if os.path.isdir(os.path.join(BASE_DIR, "locations")):
    app.mount("/locations", StaticFiles(directory=os.path.join(BASE_DIR, "locations"), html=True), name="locations")

