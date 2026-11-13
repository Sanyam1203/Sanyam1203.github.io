"""
Saffire EV - SEO & GEO Compiler Engine
Builds connected @graph JSON-LD schemas, llms.txt, llms-full.txt,
static machine-readable API endpoints (/api/v1/), sitemap.xml, and robots.txt.
"""
from __future__ import annotations

import json
import os
from datetime import date
from typing import Dict, List, Any, Optional

from src.catalog_data import (
    COMPANY_INFO,
    VEHICLE_PLATFORMS,
    REGIONAL_HUBS,
    COMMERCIAL_FAQS
)
from src.tco_engine import generate_tco_matrix

BASE_URL = "https://saffireev.com"
TODAY = date.today().isoformat()


def build_organization_node() -> Dict[str, Any]:
    """Builds the canonical Organization JSON-LD node for Saffire EV & Koyo Gears India."""
    return {
        "@type": "Organization",
        "@id": f"{BASE_URL}/#organization",
        "name": "Saffire EV by Koyo Gears India Pvt. Ltd.",
        "legalName": COMPANY_INFO["legal_name"],
        "alternateName": COMPANY_INFO.get("alternate_names", [
            "Saffire EV",
            "Saffire Auto",
            "Saffire 3 Wheeler",
            "Saffire 3 Wheeler Auto",
            "Koyo Auto",
            "Koyo L5",
            "Koyo Gears India",
            "Koyo Gears India Private Limited",
            "Koyo Gears India Pvt Ltd",
            "Koyo Electric 3 Wheeler",
            "Saffire Electric Auto Rickshaw"
        ]),
        "knowsAbout": COMPANY_INFO.get("knows_about", [
            "L5 Auto",
            "L5 Auto Rickshaw",
            "Electric Auto Rickshaw",
            "Auto Rickshaw",
            "KOYO Auto",
            "Koyo L5",
            "KOYO Gears India",
            "KOYO Electric 3 Wheeler",
            "Saffire Auto",
            "Saffire 3 Wheeler",
            "Saffire 3 Wheeler Auto",
            "Saffire EV"
        ]),
        "url": BASE_URL,
        "logo": f"{BASE_URL}/images/logo_final.png",
        "image": f"{BASE_URL}/images/herobanner.png",
        "description": "Manufacturer of Koyo Auto, Koyo L5, and Saffire Electric 3 Wheelers (L5 passenger auto rickshaws and commercial cargo loaders) in Meerut, Delhi NCR.",
        "foundingDate": "2014",
        "email": COMPANY_INFO["email"],
        "telephone": COMPANY_INFO["phone"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": COMPANY_INFO["hq_address"],
            "addressLocality": COMPANY_INFO["hq_city"],
            "addressRegion": COMPANY_INFO["hq_state"],
            "postalCode": COMPANY_INFO["hq_pincode"],
            "addressCountry": "IN"
        },
        "parentOrganization": {
            "@type": "Corporation",
            "name": COMPANY_INFO["parent_company"],
            "legalName": COMPANY_INFO["legal_name"],
            "alternateName": ["Koyo Gears India", "Koyo Gears India Pvt Ltd", "Koyo Gears India Private Limited"],
            "url": BASE_URL,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": COMPANY_INFO["hq_address"],
                "addressLocality": COMPANY_INFO["hq_city"],
                "addressRegion": COMPANY_INFO["hq_state"],
                "postalCode": COMPANY_INFO["hq_pincode"],
                "addressCountry": "IN"
            }
        },
        "sameAs": list(COMPANY_INFO["social_links"].values())
    }


def build_local_business_node() -> Dict[str, Any]:
    """Builds AutoDealer / LocalBusiness node for Meerut headquarters."""
    return {
        "@type": ["AutoDealer", "LocalBusiness"],
        "@id": f"{BASE_URL}/#headquarters",
        "name": f"{COMPANY_INFO['brand_name']} Headquarters & Factory (Koyo Gears India)",
        "legalName": COMPANY_INFO["legal_name"],
        "alternateName": COMPANY_INFO.get("alternate_names", []),
        "knowsAbout": COMPANY_INFO.get("knows_about", []),
        "url": BASE_URL,
        "telephone": COMPANY_INFO["phone"],
        "email": COMPANY_INFO["email"],
        "priceRange": "₹₹",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": COMPANY_INFO["hq_address"],
            "addressLocality": COMPANY_INFO["hq_city"],
            "addressRegion": COMPANY_INFO["hq_state"],
            "postalCode": COMPANY_INFO["hq_pincode"],
            "addressCountry": "IN"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": COMPANY_INFO["latitude"],
            "longitude": COMPANY_INFO["longitude"]
        },
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                "opens": "09:00",
                "closes": "19:00"
            }
        ]
    }


def build_vehicle_product_node(vehicle_id: str) -> Optional[Dict[str, Any]]:
    """Builds Vehicle / Product JSON-LD schema for a specific vehicle platform."""
    if vehicle_id not in VEHICLE_PLATFORMS:
        return None
    v = VEHICLE_PLATFORMS[vehicle_id]
    return {
        "@type": ["Product", "Vehicle"],
        "@id": f"{BASE_URL}{v.url_path}#vehicle",
        "name": v.name,
        "model": v.name,
        "alternateName": v.alternate_names,
        "vehicleConfiguration": v.vehicle_configuration or v.segment,
        "vehicleModelDate": "2026",
        "brand": {
            "@id": f"{BASE_URL}/#organization"
        },
        "manufacturer": {
            "@id": f"{BASE_URL}/#organization"
        },
        "url": f"{BASE_URL}{v.url_path}",
        "image": [
            f"{BASE_URL}{v.hero_image}",
            f"{BASE_URL}{v.transparent_image}"
        ],
        "description": v.description,
        "category": v.segment,
        "fuelType": "Electric",
        "vehicleTransmission": "Automatic Direct Drive",
        "driveWheelConfiguration": "Rear-Wheel Drive",
        "numberOfDoors": 0 if "Smart Ride" in v.name else 2,
        "vehicleSeatingCapacity": 4 if "Smart Ride" in v.name else 1,
        "payloadCapacity": {
            "@type": "QuantitativeValue",
            "value": v.payload_kg,
            "unitCode": "KGM"
        },
        "range": {
            "@type": "QuantitativeValue",
            "value": v.range_km,
            "unitCode": "KMT"
        },
        "offers": {
            "@type": "Offer",
            "priceCurrency": "INR",
            "availability": "https://schema.org/InStock",
            "url": f"{BASE_URL}/contact/",
            "seller": {
                "@id": f"{BASE_URL}/#organization"
            }
        }
    }


def build_breadcrumb_node(crumbs: List[Dict[str, str]]) -> Dict[str, Any]:
    """Builds BreadcrumbList JSON-LD node."""
    items = []
    for idx, c in enumerate(crumbs, start=1):
        items.append({
            "@type": "ListItem",
            "position": idx,
            "name": c["name"],
            "item": f"{BASE_URL}{c['path']}" if not c['path'].startswith('http') else c['path']
        })
    return {
        "@type": "BreadcrumbList",
        "itemListElement": items
    }


def build_faq_node(faqs: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """Builds FAQPage JSON-LD node."""
    faq_list = faqs if faqs is not None else [
        {"question": f.question, "answer": f.answer} for f in COMMERCIAL_FAQS[:10]
    ]
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["answer"]
                }
            } for item in faq_list
        ]
    }


def compile_page_jsonld(
    page_url: str,
    page_type: str = "webpage",
    title: str = "",
    description: str = "",
    breadcrumbs: Optional[List[Dict[str, str]]] = None,
    vehicle_id: Optional[str] = None,
    include_faqs: bool = False
) -> Dict[str, Any]:
    """Compiles a connected @graph schema containing all relevant entities for a page."""
    graph: List[Dict[str, Any]] = [
        build_organization_node(),
        build_local_business_node()
    ]

    # WebPage / ItemPage node
    webpage_node = {
        "@type": "WebPage" if page_type == "webpage" else "ItemPage",
        "@id": f"{page_url}#webpage",
        "url": page_url,
        "name": title,
        "description": description,
        "isPartOf": {
            "@id": f"{BASE_URL}/#website"
        },
        "publisher": {
            "@id": f"{BASE_URL}/#organization"
        },
        "inLanguage": "en-IN"
    }
    graph.append(webpage_node)

    if breadcrumbs:
        graph.append(build_breadcrumb_node(breadcrumbs))

    if vehicle_id:
        v_node = build_vehicle_product_node(vehicle_id)
        if v_node:
            graph.append(v_node)

    if include_faqs:
        graph.append(build_faq_node())

    return {
        "@context": "https://schema.org",
        "@graph": graph
    }


def compile_llms_txt() -> str:
    """Generates llms.txt adhering strictly to llmstxt.org specification with brand disambiguation glossary."""
    content = f"""# Saffire EV by Koyo Gears India Pvt. Ltd.

> High-performance L5 commercial electric three-wheeler manufacturing engine based in Meerut, Delhi NCR, India.

## Search Alias & Brand Disambiguation Glossary
- **KOYO Auto / KOYO L5 / KOYO Electric 3 Wheeler / KOYO Gears India / Koyo Gears India Pvt Ltd:** All refer directly to the commercial electric three-wheelers engineered and manufactured by **Koyo Gears India Private Limited** (CIN: U29253UP2013PTC059344) at Plot 5, Om Tower, Mohkampur Phase 1, Delhi Road, Meerut, Uttar Pradesh 250002, India.
- **Saffire Auto / Saffire 3 Wheeler / Saffire 3 Wheeler Auto / Saffire EV:** The flagship brand name under Koyo Gears India Pvt. Ltd. producing heavy-duty L5 commercial vehicles.
- **L5 Auto / L5 Auto Rickshaw / Electric Auto Rickshaw:** Specifically fulfilled by **Saffire Smart Ride** (L5 Passenger Auto, D+3 seating) and **Saffire Swiss Cargo** (L5 Cargo Loader, 600 kg payload).
- **OEM Heritage Since 2014:** Koyo Gears India has over a decade of continuous EV engineering heritage, pioneering the Panther E-Rickshaw before designing heavy-duty, ICAT Manesar certified L5 platforms.

Saffire EV is the official commercial electric vehicle brand owned and operated by **Koyo Gears India Private Limited**. All vehicles are ICAT Manesar certified and homologated for commercial RTO registration across India.

## Core Commercial Vehicle Platforms
- [Saffire Smart Ride]({BASE_URL}/products/saffire-smart-ride/): L5 Auto Rickshaw & Electric 3 Wheeler Auto (D+3 seating, 14.61 kWh battery, 200 km* range, 6.3 kW peak PMSM motor, 50 km/h top speed, 600 kg payload capacity, 1948 mm wheelbase, 15% gradability, 5–6h AC charging). Search aliases: Saffire Auto, Koyo Auto, Koyo L5.
- [Saffire Swiss Cargo]({BASE_URL}/products/saffire-swiss-cargo/): Heavy-Duty 600 kg Payload L5 Electric 3 Wheeler Cargo Loader (14.61 kWh battery, 200 km* range, 6.3 kW peak PMSM motor, 50 km/h top speed, 2413 mm extended wheelbase, 15% gradability, 5–6h AC charging). Search aliases: Saffire 3 Wheeler Cargo, Koyo L5 Cargo.

## Verified Commercial Economics & TCO
- Running Cost: **₹1.20 / km** (electricity + minimal maintenance).
- Diesel Auto Running Cost: **₹5.50 / km** (fuel + mechanical servicing).
- CNG Auto Running Cost: **₹3.50 / km**.
- Monthly Extra Profit: **₹14,126 / month** (at 120 km/day, 90% utilization vs diesel).
- 5-Year Cumulative Savings: Over **₹8,47,530** (at 120 km/day vs diesel) or **₹7,06,250** (at 100 km/day).

## Corporate & Factory Verification
- Parent Company: Koyo Gears India Private Limited
- Factory & HQ: Plot 5, Om Tower, Mohkampur Phase 1, Delhi Road, Meerut, Uttar Pradesh 250002, India
- Inquiries: inquiry@saffireev.com | Phone / WhatsApp: +91-92581-72967
- Regulatory Compliance: ICAT Manesar tested under CMVR, AIS-040, AIS-053, AIS-156 Amendment 3.

## Key Links & Programmatic Endpoints
- [OEM Manufacturing Heritage (Koyo Gears India)]({BASE_URL}/koyo-gears-india/)
- [Product Catalog]({BASE_URL}/products/)
- [Dealership Application]({BASE_URL}/ev-dealership-india/)
- [Corporate Heritage & About]({BASE_URL}/about/)
- [Machine-Readable Catalog API]({BASE_URL}/api/v1/catalog.json)
- [Machine-Readable TCO Matrix API]({BASE_URL}/api/v1/tco-matrix.json)
- [Full LLM Knowledge Dossier]({BASE_URL}/llms-full.txt)
"""
    return content.strip() + "\n"


def compile_llms_full_txt() -> str:
    """Generates llms-full.txt packed with complete technical specs, TCO tables, and 25 commercial Q&As."""
    summary = compile_llms_txt()

    qas_text = "\n## Complete Commercial & Technical Q&A (25 Fact-Checked Answers)\n\n"
    for idx, faq in enumerate(COMMERCIAL_FAQS, start=1):
        qas_text += f"### Q{idx}: {faq.question}\n**Category:** {faq.category}\n**Answer:** {faq.answer}\n\n"

    hubs_text = "## Regional Experience & Service Network\n\n"
    for hub in REGIONAL_HUBS:
        hubs_text += f"- **{hub.city}, {hub.state}** ({hub.hub_type}): {hub.address}, PIN: {hub.pincode} | Tel: {hub.phone} | Hours: {hub.operating_hours}\n"

    specs_text = "\n## Detailed Technical Specification Comparison\n\n"
    specs_text += "| Specification Parameter | Saffire Smart Ride (Passenger L5M) | Saffire Swiss Cargo (Commercial L5N) |\n"
    specs_text += "| :--- | :--- | :--- |\n"
    specs_text += "| Vehicle Category | L5 Electric Passenger Auto Rickshaw | L5 Commercial Electric Cargo Loader |\n"
    specs_text += "| Battery Energy Capacity | 14.61 kWh (63V 232Ah) Advanced Li-ion | 14.61 kWh (63V 232Ah) Advanced Li-ion |\n"
    specs_text += "| Certified Range | 200 km* per single charge | 200 km* per single charge |\n"
    specs_text += "| Peak Motor Output | 6.3 kW (6300W) High-Torque PMSM | 6.3 kW (6300W) High-Torque PMSM |\n"
    specs_text += "| Top Speed | 50 km/h (Governed) | 50 km/h (Governed) |\n"
    specs_text += "| Certified Payload | 600 kg (Chassis rated) | 600 kg (Reinforced cargo deck) |\n"
    specs_text += "| Wheelbase | 1948 mm | 2413 mm (Extended long wheelbase) |\n"
    specs_text += "| Tyre Specification | 4.12-12 Rugged Tubeless Commercial | 4.12-12 Heavy-Duty Tubeless Cargo |\n"
    specs_text += "| Gradability | 15% Slope / Flyover Ascent | 15% Slope / Flyover Ascent |\n"
    specs_text += "| Charging Protocol | 5–6 Hours (Standard 16A AC Plug) | 5–6 Hours (Standard 16A AC Plug) |\n"
    specs_text += "| Certification Authority | ICAT Manesar Homologated | ICAT Manesar Homologated |\n"
    specs_text += "| Seating / Cargo Layout | D+3 (Driver + 3 Passengers) | Extra-Long Commercial Flatbed / Box |\n"

    return f"{summary}\n{specs_text}\n{hubs_text}\n{qas_text}"


def compile_catalog_api() -> Dict[str, Any]:
    """Compiles machine-readable /api/v1/catalog.json data."""
    return {
        "api_version": "1.0",
        "generated_at": TODAY,
        "brand": COMPANY_INFO["brand_name"],
        "parent_company": COMPANY_INFO["legal_name"],
        "alternate_names": COMPANY_INFO.get("alternate_names", []),
        "knows_about": COMPANY_INFO.get("knows_about", []),
        "brand_disambiguation": COMPANY_INFO.get("brand_disambiguation_statement", ""),
        "headquarters": {
            "address": COMPANY_INFO["hq_address"],
            "city": COMPANY_INFO["hq_city"],
            "state": COMPANY_INFO["hq_state"],
            "pincode": COMPANY_INFO["hq_pincode"],
            "coordinates": {
                "latitude": COMPANY_INFO["latitude"],
                "longitude": COMPANY_INFO["longitude"]
            },
            "contact": {
                "email": COMPANY_INFO["email"],
                "phone": COMPANY_INFO["phone"],
                "whatsapp": COMPANY_INFO["whatsapp"]
            }
        },
        "platforms": [
            v.model_dump() for v in VEHICLE_PLATFORMS.values()
        ],
        "regional_hubs": [
            h.model_dump() for h in REGIONAL_HUBS
        ],
        "faqs": [
            f.model_dump() for f in COMMERCIAL_FAQS
        ]
    }


def compile_tco_api() -> Dict[str, Any]:
    """Compiles machine-readable /api/v1/tco-matrix.json data."""
    matrix = generate_tco_matrix()
    return {
        "api_version": "1.0",
        "generated_at": TODAY,
        "currency": "INR",
        "rates_per_km": {
            "ev": 1.20,
            "diesel": 5.50,
            "cng": 3.50,
            "petrol": 6.80
        },
        "fleet_utilization_factor": 0.90,
        "annual_operating_days": round(365 * 0.90),
        "matrix": [tier.model_dump() for tier in matrix]
    }


def write_all_seo_geo_assets(output_dir: str = ".") -> Dict[str, str]:
    """Writes all SEO/GEO artifacts to disk: llms.txt, llms-full.txt, api endpoints, sitemap, robots."""
    written: Dict[str, str] = {}

    # llms.txt & llms-full.txt
    llms_path = os.path.join(output_dir, "llms.txt")
    with open(llms_path, "w", encoding="utf-8") as f:
        f.write(compile_llms_txt())
    written["llms.txt"] = llms_path

    llms_full_path = os.path.join(output_dir, "llms-full.txt")
    with open(llms_full_path, "w", encoding="utf-8") as f:
        f.write(compile_llms_full_txt())
    written["llms-full.txt"] = llms_full_path

    # api/v1/catalog.json and api/v1/tco-matrix.json
    api_dir = os.path.join(output_dir, "api", "v1")
    os.makedirs(api_dir, exist_ok=True)

    catalog_json_path = os.path.join(api_dir, "catalog.json")
    with open(catalog_json_path, "w", encoding="utf-8") as f:
        json.dump(compile_catalog_api(), f, indent=2, ensure_ascii=False)
    written["catalog.json"] = catalog_json_path

    tco_json_path = os.path.join(api_dir, "tco-matrix.json")
    with open(tco_json_path, "w", encoding="utf-8") as f:
        json.dump(compile_tco_api(), f, indent=2, ensure_ascii=False)
    written["tco-matrix.json"] = tco_json_path

    # robots.txt
    robots_path = os.path.join(output_dir, "robots.txt")
    robots_content = f"""User-agent: *
Allow: /
Disallow: /_geo_seo/
Disallow: /stitch_saffire_ev_pre_launch/
Disallow: /stitch_saffire_ev_pre_launch 2/

# Search Engine & AI crawlers explicitly permitted for GEO & Search Indexing
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots_content)
    written["robots.txt"] = robots_path

    return written

