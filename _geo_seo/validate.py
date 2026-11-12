#!/usr/bin/env python3
"""
Saffire EV — Local Validation Script
Run from repo root: python3 _geo_seo/validate.py

Checks:
1. All pages referenced in sitemap.xml exist on disk
2. JSON-LD blocks parse as valid JSON
3. Canonical tags are present and match expected URL
4. Robots meta is correct (no noindex on indexable pages)
5. Title and description meta exist
6. No broken internal links (href) pointing to files that don't exist
"""

import json
import os
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(ROOT, "sitemap.xml")
BASE_URL = "https://saffireev.com"

errors = []
warnings = []
ok_count = 0

def err(msg): errors.append(f"ERROR: {msg}")
def warn(msg): warnings.append(f"WARN:  {msg}")
def ok(): global ok_count; ok_count += 1

def url_to_path(url):
    path = url.replace(BASE_URL, "").lstrip("/")
    if path == "" or path.endswith("/"):
        path = path.rstrip("/")
        return os.path.join(ROOT, path, "index.html") if path else os.path.join(ROOT, "index.html")
    return os.path.join(ROOT, path)

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None

# ── 1. Sitemap existence check ─────────────────────────────────────────────
print("=== Checking sitemap URLs ===")
tree = ET.parse(SITEMAP)
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls = [e.text for e in tree.findall('.//sm:loc', ns)]
print(f"  {len(urls)} URLs in sitemap")

for url in urls:
    p = url_to_path(url)
    if os.path.exists(p):
        ok()
    else:
        err(f"Sitemap URL missing on disk: {url} → {p}")

# ── 2. Per-page checks ─────────────────────────────────────────────────────
print("\n=== Checking page content ===")
pages_to_check = []
for url in urls:
    pages_to_check.append(url)

# Also check some non-sitemap pages (draft cities)
draft_check = [
    f"{BASE_URL}/locations/araria/",
    f"{BASE_URL}/locations/forbesganj/",
]
for u in draft_check:
    pages_to_check.append(u)

for url in pages_to_check:
    path = url_to_path(url)
    content = read_file(path)
    if content is None:
        # Already caught above for sitemap URLs
        continue

    is_sitemap_url = url in urls
    label = url.replace(BASE_URL, "") or "/"

    # Title
    if re.search(r'<title>[^<]+</title>', content):
        ok()
    else:
        err(f"Missing <title>: {label}")

    # Meta description
    if re.search(r'<meta[^>]+name=["\']description["\'][^>]+>', content):
        ok()
    else:
        warn(f"Missing meta description: {label}")

    # Canonical — handle both attribute orders (rel first or href first)
    canon_match = re.search(
        r'<link[^>]+(?:rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']'
        r'|href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\'])',
        content
    )
    if canon_match:
        canon = canon_match.group(1) or canon_match.group(2)
        if canon != url:
            err(f"Canonical mismatch: {label} has canonical={canon} but expected {url}")
        else:
            ok()
    else:
        err(f"Missing canonical: {label}")

    # Robots meta (draft pages should have noindex)
    robots_match = re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']', content)
    if is_sitemap_url:
        if robots_match and 'noindex' in robots_match.group(1):
            err(f"Sitemap page has noindex: {label}")
        else:
            ok()
    else:
        # Draft pages should have noindex
        if robots_match and 'noindex' in robots_match.group(1):
            ok()
        else:
            warn(f"Non-sitemap page missing noindex: {label}")

    # JSON-LD validity
    jsonld_blocks = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.DOTALL)
    for i, block in enumerate(jsonld_blocks):
        try:
            json.loads(block.strip())
            ok()
        except json.JSONDecodeError as e:
            err(f"Invalid JSON-LD block {i+1} on {label}: {e}")

# ── 3. Internal link check (sample city pages) ────────────────────────────
print("\n=== Spot-checking internal links on key pages ===")
sample_pages = [
    "/locations/meerut/",
    "/locations/delhi/",
    "/locations/index.html",
    "/",
]

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, val in attrs:
                if name == 'href' and val:
                    self.links.append(val)

for page_url_path in sample_pages:
    if page_url_path == "/locations/index.html":
        path = os.path.join(ROOT, "locations", "index.html")
    else:
        path = url_to_path(BASE_URL + page_url_path)
    content = read_file(path)
    if not content:
        continue
    parser = LinkParser()
    parser.feed(content)
    internal = [l for l in parser.links if l.startswith('/') and not l.startswith('//')]
    broken = []
    for link in internal:
        link_clean = link.split('?')[0].split('#')[0]
        if link_clean.endswith('/'):
            fp = os.path.join(ROOT, link_clean.lstrip('/'), 'index.html')
        else:
            fp = os.path.join(ROOT, link_clean.lstrip('/'))
        if not os.path.exists(fp):
            broken.append(link)
    if broken:
        warn(f"Possibly broken internal links on {page_url_path}: {broken[:3]}")
    else:
        ok()

# ── Report ─────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"VALIDATION RESULTS")
print(f"{'='*50}")
print(f"  OK checks:   {ok_count}")
print(f"  Warnings:    {len(warnings)}")
print(f"  Errors:      {len(errors)}")
print()

if warnings:
    for w in warnings:
        print(f"  {w}")
    print()

if errors:
    for e in errors:
        print(f"  {e}")
    print()
    print("FAILED — resolve errors before deploying.")
else:
    print("PASSED — no errors found.")
