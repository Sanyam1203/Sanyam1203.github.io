"""
Saffire EV - Automated SEO & GEO Test Suite
Tests HTML sanitation, icon snippets protection, canonical URLs,
OpenGraph metadata, JSON-LD schemas, API endpoints, and TCO calculations.
"""
import os
import sys
import json
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from bs4 import BeautifulSoup
from fastapi.testclient import TestClient

from app import app
from src.tco_engine import calculate_tco, generate_tco_matrix
from src.catalog_data import COMPANY_INFO, VEHICLE_PLATFORMS

client = TestClient(app)


def test_required_root_artifacts_exist():
    """Verify all critical SEO/GEO endpoints and root files exist and are non-empty."""
    required_files = [
        "CNAME",
        "robots.txt",
        "sitemap.xml",
        "llms.txt",
        "llms-full.txt",
        "api/v1/catalog.json",
        "api/v1/tco-matrix.json"
    ]
    for rel_path in required_files:
        full_path = os.path.join(ROOT_DIR, rel_path)
        assert os.path.isfile(full_path), f"Required file '{rel_path}' is missing!"
        assert os.path.getsize(full_path) > 0, f"File '{rel_path}' is empty!"

    # Verify CNAME domain
    with open(os.path.join(ROOT_DIR, "CNAME"), "r", encoding="utf-8") as f:
        cname = f.read().strip()
        assert cname == "saffireev.com", f"Expected 'saffireev.com' in CNAME, got '{cname}'"


def test_robots_txt_ai_bot_allowances():
    """Verify robots.txt explicitly allows major search and AI crawlers."""
    with open(os.path.join(ROOT_DIR, "robots.txt"), "r", encoding="utf-8") as f:
        content = f.read()

    expected_bots = [
        "Googlebot",
        "Bingbot",
        "GPTBot",
        "OAI-SearchBot",
        "PerplexityBot",
        "ClaudeBot",
        "Google-Extended"
    ]
    for bot in expected_bots:
        assert f"User-agent: {bot}" in content, f"User-agent: {bot} not found in robots.txt"
    assert "Sitemap: https://saffireev.com/sitemap.xml" in content


def test_llms_txt_standard_and_disambiguation():
    """Verify llms.txt and llms-full.txt conform to llmstxt.org and contain company facts."""
    with open(os.path.join(ROOT_DIR, "llms.txt"), "r", encoding="utf-8") as f:
        txt = f.read()
    assert "# Saffire EV by Koyo Gears India Pvt. Ltd." in txt
    assert "Koyo Gears India Private Limited" in txt
    assert "Panther E-Rickshaw" in txt
    assert "14.61 kWh" in txt
    assert "200 km*" in txt
    assert "6.3 kW" in txt
    assert "₹1.20 / km" in txt

    with open(os.path.join(ROOT_DIR, "llms-full.txt"), "r", encoding="utf-8") as f:
        full_txt = f.read()
    assert "Complete Commercial & Technical Q&A" in full_txt
    assert "Q25:" in full_txt or "Q1:" in full_txt


def test_tco_calculation_accuracy():
    """Verify TCO formulas match the verified benchmark numbers."""
    # 120 km/day over 5 years against diesel
    calc = calculate_tco(daily_km=120, years=5, fuel="diesel")
    assert calc["monthly_extra_profit"] == 14126
    assert calc["roi_percent_gain"] == 358

    # 100 km/day over 5 years against diesel
    calc_100 = calculate_tco(daily_km=100, years=5, fuel="diesel")
    assert calc_100["monthly_extra_profit"] == 11771
    assert calc_100["lifetime_savings"] == 706275


def test_fastapi_endpoints():
    """Verify FastAPI API preview endpoints return valid JSON."""
    # GET /api/v1/catalog
    res = client.get("/api/v1/catalog")
    assert res.status_code == 200
    data = res.json()
    assert data["brand"] == "Saffire EV"
    assert len(data["platforms"]) >= 2

    # GET /api/v1/tco-matrix
    res_tco = client.get("/api/v1/tco-matrix")
    assert res_tco.status_code == 200
    matrix_data = res_tco.json()
    assert "matrix" in matrix_data
    assert len(matrix_data["matrix"]) > 0

    # GET /api/v1/calculate-tco
    res_calc = client.get("/api/v1/calculate-tco?km=120&years=5&fuel=diesel")
    assert res_calc.status_code == 200
    calc_data = res_calc.json()
    assert calc_data["monthly_extra_profit"] == 14126

    # POST /api/v1/submit-query
    payload = {
        "name": "Test Dealer",
        "phone": "9876543210",
        "city": "Meerut",
        "platform": "Saffire Smart Ride (Passenger)",
        "intent": "dealer",
        "notes": "Testing pytest submission",
        "source": "https://saffireev.com/ev-dealership-india/"
    }
    res_post = client.post("/api/v1/submit-query", json=payload)
    assert res_post.status_code == 201
    assert res_post.json()["status"] == "success"


def test_html_pages_sanitization_and_metadata():
    """Verify all primary HTML pages have canonical, og metadata, valid JSON-LD, and sanitized icon spans."""
    core_pages = [
        "index.html",
        "koyo-gears-india/index.html",
        "about/index.html",
        "vision/index.html",
        "products/index.html",
        "products/saffire-smart-ride/index.html",
        "products/saffire-swiss-cargo/index.html",
        "ev-dealership-india/index.html",
        "contact/index.html",
        "terms/index.html",
        "404.html"
    ]

    for rel_path in core_pages:
        full_path = os.path.join(ROOT_DIR, rel_path)
        if not os.path.isfile(full_path):
            continue

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")

        # Skip document-level metadata assertions for 404 error page
        if rel_path == "404.html":
            continue

        # 1. Canonical check
        canonical = soup.find("link", rel=lambda r: r and "canonical" in r)
        assert canonical is not None, f"Page {rel_path} is missing <link rel='canonical'>"
        assert canonical.get("href"), f"Page {rel_path} canonical has empty href"

        # 2. OpenGraph check
        og_title = soup.find("meta", property="og:title")
        assert og_title is not None, f"Page {rel_path} is missing <meta property='og:title'>"
        assert og_title.get("content"), f"Page {rel_path} has empty og:title"

        og_desc = soup.find("meta", property="og:description")
        assert og_desc is not None, f"Page {rel_path} is missing <meta property='og:description'>"

        # 3. JSON-LD check
        jsonld = soup.find("script", type="application/ld+json")
        assert jsonld is not None, f"Page {rel_path} is missing JSON-LD schema"
        # Verify valid JSON
        try:
            schema = json.loads(jsonld.string)
            assert "@context" in schema or "@graph" in schema
        except Exception as e:
            pytest.fail(f"Invalid JSON-LD on {rel_path}: {e}")

        # 4. Icon spans leak check
        icon_spans = soup.find_all("span", class_=lambda c: c and "material-symbols-outlined" in c)
        for span in icon_spans:
            assert span.get("aria-hidden") == "true", f"Icon span in {rel_path} missing aria-hidden='true': {span}"
            assert span.has_attr("data-nosnippet"), f"Icon span in {rel_path} missing data-nosnippet: {span}"


def test_exact_keyword_clusters_and_pillar_page():
    """Verify that all target keyword clusters are hardwired into titles, headings, and JSON-LD."""
    # 1. Homepage titles & keywords
    with open(os.path.join(ROOT_DIR, "index.html"), "r", encoding="utf-8") as f:
        home_html = f.read()
    home_soup = BeautifulSoup(home_html, "html.parser")
    assert "Saffire EV (Saffire Auto) | L5 Electric 3 Wheeler & Auto Rickshaw by Koyo Gears India" in home_soup.title.string
    assert "Why Choose a Saffire L5 Auto Rickshaw" in home_html
    assert "Saffire Auto" in home_html
    assert "Koyo L5" in home_html

    # 2. Smart Ride title & keywords
    with open(os.path.join(ROOT_DIR, "products", "saffire-smart-ride", "index.html"), "r", encoding="utf-8") as f:
        smart_html = f.read()
    smart_soup = BeautifulSoup(smart_html, "html.parser")
    assert "Saffire Smart Ride — L5 Auto Rickshaw & Electric 3 Wheeler Auto" in smart_soup.title.string
    assert "Why Choose a Saffire L5 Auto Rickshaw" in smart_html

    # 3. Swiss Cargo title & keywords
    with open(os.path.join(ROOT_DIR, "products", "saffire-swiss-cargo", "index.html"), "r", encoding="utf-8") as f:
        cargo_html = f.read()
    cargo_soup = BeautifulSoup(cargo_html, "html.parser")
    assert "Saffire Swiss Cargo — L5 Electric 3 Wheeler Cargo Loader" in cargo_soup.title.string
    assert "Koyo L5" in cargo_html or "Koyo Gears India" in cargo_html

    # 4. About title & keywords
    with open(os.path.join(ROOT_DIR, "about", "index.html"), "r", encoding="utf-8") as f:
        about_html = f.read()
    about_soup = BeautifulSoup(about_html, "html.parser")
    assert "Koyo Gears India Pvt. Ltd. | Manufacturer of Koyo Auto, Koyo L5 & Saffire Electric 3 Wheelers" in about_soup.title.string

    # 5. OEM Pillar Page
    koyo_page = os.path.join(ROOT_DIR, "koyo-gears-india", "index.html")
    assert os.path.isfile(koyo_page), "Pillar page /koyo-gears-india/index.html is missing!"
    with open(koyo_page, "r", encoding="utf-8") as f:
        koyo_html = f.read()
    koyo_soup = BeautifulSoup(koyo_html, "html.parser")
    assert "Koyo Gears India Pvt. Ltd. | Manufacturer of Koyo Auto, Koyo L5 & Saffire Electric 3 Wheelers" in koyo_soup.title.string
    assert "https://saffireev.com/koyo-gears-india/" in koyo_html

    # 6. JSON-LD alternateName & knowsAbout in compiled catalog API
    with open(os.path.join(ROOT_DIR, "api", "v1", "catalog.json"), "r", encoding="utf-8") as f:
        cat_data = json.load(f)
    assert "alternate_names" in cat_data
    assert "Koyo Auto" in cat_data["alternate_names"]
    assert "Saffire Auto" in cat_data["alternate_names"]
    assert "knows_about" in cat_data
    assert "L5 Auto" in cat_data["knows_about"]

    # 7. State directory on dealership page
    with open(os.path.join(ROOT_DIR, "ev-dealership-india", "index.html"), "r", encoding="utf-8") as f:
        dealership_html = f.read()
    assert 'id="city-directory"' in dealership_html
    assert "/locations/meerut/" in dealership_html

