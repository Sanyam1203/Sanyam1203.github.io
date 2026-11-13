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


def test_zero_unhidden_icon_ligatures_all_pages():
    """Verify every icon tag across all generated HTML pages has aria-hidden, translate='no', data-nosnippet, and notranslate."""
    exclude_dirs = {".git", ".venv", "venv", "__pycache__", "templates", "stitch_saffire_ev_pre_launch", "stitch_saffire_ev_pre_launch 2"}
    checked_files = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for fname in files:
            if not fname.endswith(".html"):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")
            checked_files += 1
            icons = soup.find_all(["i", "span"], class_=lambda c: c and (
                "material-symbols-outlined" in c or "material-icons" in c or "material-symbols" in c
            ))
            for icon in icons:
                classes = icon.get("class") or []
                assert icon.get("aria-hidden") == "true", f"Missing aria-hidden in {fpath}"
                assert icon.get("translate") == "no", f"Missing translate='no' in {fpath}"
                assert icon.has_attr("data-nosnippet"), f"Missing data-nosnippet in {fpath}"
                assert "notranslate" in classes, f"Missing notranslate class in {fpath}"
    assert checked_files >= 110


def test_zero_orphaned_sitemap_urls():
    """Verify all 111 sitemap URLs exist on disk and are reachable via HTML crawl from index.html."""
    import xml.etree.ElementTree as ET
    from collections import deque

    sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
    tree = ET.parse(sitemap_path)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [el.text.strip() for el in tree.getroot().findall("sm:url/sm:loc", ns)]
    assert len(urls) == 111, f"Expected 111 sitemap URLs, found {len(urls)}"

    def url_to_rel_path(url: str) -> str:
        path = url.replace("https://saffireev.com", "").split("#")[0].split("?")[0]
        if not path or path == "/":
            return "index.html"
        path = path.strip("/")
        if os.path.isfile(os.path.join(ROOT_DIR, path)):
            return path
        return os.path.join(path, "index.html")

    # 1. Verify every URL exists on disk
    expected_rel_paths = set()
    for u in urls:
        rel = url_to_rel_path(u)
        assert os.path.isfile(os.path.join(ROOT_DIR, rel)), f"Missing file on disk for sitemap URL {u}: {rel}"
        expected_rel_paths.add(rel)

    # 2. BFS crawl from index.html
    visited = set()
    queue = deque(["index.html"])
    while queue:
        curr = queue.popleft()
        if curr in visited:
            continue
        visited.add(curr)
        full = os.path.join(ROOT_DIR, curr)
        if not os.path.isfile(full):
            continue
        with open(full, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith(("http://", "https://")) and not href.startswith("https://saffireev.com"):
                continue
            if href.startswith(("mailto:", "tel:", "javascript:", "#")):
                continue
            if href.startswith("https://saffireev.com"):
                href = href.replace("https://saffireev.com", "")
            href = href.split("#")[0].split("?")[0]
            if not href:
                continue
            target = "index.html" if href == "/" else (href.strip("/") if href.endswith(".html") else os.path.join(href.strip("/"), "index.html"))
            if target not in visited and os.path.isfile(os.path.join(ROOT_DIR, target)):
                queue.append(target)

    orphaned = expected_rel_paths - visited
    assert not orphaned, f"Orphaned sitemap URLs unreachable from index.html: {sorted(orphaned)}"


def test_nap_and_cin_consistency():
    """Verify dual Meerut NAP, phone, and CIN U28140UP2025PTC216042 across HTML and JSON-LD."""
    for rel in ["contact/index.html", "about/index.html", "koyo-gears-india/index.html"]:
        with open(os.path.join(ROOT_DIR, rel), "r", encoding="utf-8") as f:
            html = f.read()
        assert "Plot 5, Om Tower, Mohkampur Phase 1" in html, f"Missing HQ address in {rel}"
        assert "173/2, Delhi Road, Mohkampur (New Shambhu Nagar Road)" in html, f"Missing Registered Office in {rel}"
        assert "U28140UP2025PTC216042" in html, f"Missing CIN U28140UP2025PTC216042 in {rel}"
        assert "+91-92581-72967" in html, f"Missing phone in {rel}"
        assert "U29253UP2013PTC059344" not in html, f"Stale CIN found in {rel}"


def test_guide_tco_tables_and_cro_ctas():
    """Verify static TCO & spec tables in guides, single calculator CTA, and page-specific og:image."""
    for rel in [
        "electric-three-wheeler-running-cost/index.html",
        "ev-dealership-india/index.html",
        "electric-cargo-loader/index.html",
        "electric-passenger-auto/index.html",
    ]:
        with open(os.path.join(ROOT_DIR, rel), "r", encoding="utf-8") as f:
            html = f.read()
        assert 'id="verified-tco-specs"' in html, f"Missing TCO spec table in {rel}"
        assert "₹ 2,36,520" in html
        assert "₹ 10,84,050" in html
        assert "₹ 8,47,530" in html

    with open(os.path.join(ROOT_DIR, "index.html"), "r", encoding="utf-8") as f:
        home = f.read()
    assert home.count('id="calc-lock-savings-btn"') == 1
    assert "Lock In Your" in home and "Savings — Request Dealer / Fleet Quote" in home

    with open(os.path.join(ROOT_DIR, "products", "saffire-smart-ride", "index.html"), "r", encoding="utf-8") as f:
        assert "saffire-smart-ride-l5-passenger-auto.jpg" in f.read()
    with open(os.path.join(ROOT_DIR, "products", "saffire-swiss-cargo", "index.html"), "r", encoding="utf-8") as f:
        assert "saffire-swiss-cargo-l5-loader.jpg" in f.read()
    with open(os.path.join(ROOT_DIR, "contact", "index.html"), "r", encoding="utf-8") as f:
        assert "saffire-ev-meerut-showroom.jpg" in f.read()


