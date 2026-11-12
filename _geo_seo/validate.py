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
    f"{BASE_URL}/locations/aurangabad-bihar/",
    f"{BASE_URL}/locations/baripada/",
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
    robots_match = re.search(
        r'<meta[^>]+(?:name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']'
        r'|content=["\']([^"\']+)["\'][^>]+name=["\']robots["\'])',
        content
    )
    robots_val = (robots_match.group(1) or robots_match.group(2)) if robots_match else ""
    if is_sitemap_url:
        if 'noindex' in robots_val:
            err(f"Sitemap page has noindex: {label}")
        else:
            ok()
    else:
        # Draft pages should have noindex
        if 'noindex' in robots_val:
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

# ── 3. Comprehensive site-wide HTML, asset, link, heading & FAQ check ──────
print("\n=== Checking all active HTML pages for links, assets, headings & FAQ sync ===")

class FullPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.srcs = []
        self.link_hrefs = []
        self.h_levels = []
        self.imgs = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.add(d["id"])
        if tag == 'a' and d.get("href"):
            self.links.append(d["href"])
        if tag in ("script", "img", "source", "video") and d.get("src"):
            self.srcs.append((tag, d["src"]))
        if tag == "link" and d.get("href") and d.get("rel") in ("icon", "stylesheet", "shortcut icon", "apple-touch-icon"):
            self.link_hrefs.append(d["href"])
        if tag == "img":
            self.imgs.append((d.get("src", ""), d.get("alt")))
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.h_levels.append(int(tag[1]))

def resolve_local(html_path, url):
    if url.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "data:")):
        return True
    if url.startswith("#"):
        return True
    clean = url.split("?")[0].split("#")[0]
    if not clean:
        return True
    if clean.startswith("/"):
        target = os.path.join(ROOT, clean.lstrip("/"))
    else:
        target = os.path.normpath(os.path.join(os.path.dirname(html_path), clean))
    if os.path.isdir(target):
        return os.path.exists(os.path.join(target, "index.html"))
    return os.path.exists(target) or os.path.exists(os.path.join(target, "index.html"))

all_html = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in ("_geo_seo", "stitch_saffire_ev_pre_launch", "stitch_saffire_ev_pre_launch 2")]
    for fn in filenames:
        if fn.endswith(".html"):
            all_html.append(os.path.join(dirpath, fn))

import html as html_mod
for fp in sorted(all_html):
    rel = os.path.relpath(fp, ROOT)
    content = read_file(fp)
    if not content:
        continue
    is_refresh = bool(re.search(r'http-equiv=["\']refresh["\']', content, re.I))
    parser = FullPageParser()
    parser.feed(content)

    for l in parser.links:
        if not resolve_local(fp, l):
            err(f"Broken internal link on {rel}: {l}")
    ok()

    for tag, s in parser.srcs:
        if not resolve_local(fp, s):
            err(f"Broken local {tag} src on {rel}: {s}")
    for lh in parser.link_hrefs:
        if not resolve_local(fp, lh):
            err(f"Broken local link href on {rel}: {lh}")
    ok()

    for src, alt in parser.imgs:
        if alt is None or alt.strip() == "":
            err(f"Missing/empty img alt on {rel}: {src}")

    if not is_refresh and rel != "404.html":
        h1_cnt = parser.h_levels.count(1)
        if h1_cnt != 1:
            err(f"Expected 1 <h1>, found {h1_cnt} on {rel}")
        for a, b in zip(parser.h_levels, parser.h_levels[1:]):
            if b > a + 1:
                err(f"Heading hierarchy skip h{a}->h{b} on {rel}")
        for og in ("og:title", "og:description", "og:url", "og:image", "twitter:card"):
            if og not in content:
                err(f"Missing {og} on {rel}")

    if re.search(r'@keyframes\s*\{', content):
        err(f"Empty CSS @keyframes name on {rel}")

    descs = re.findall(r'<meta[^>]+name=["\']description["\']', content)
    if len(descs) > 1:
        err(f"Duplicate meta description ({len(descs)}) on {rel}")

    # Verify FAQPage questions appear visibly in page text
    unescaped_page = html_mod.unescape(re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL))
    unescaped_norm = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', unescaped_page))
    for block in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.DOTALL):
        try:
            data = json.loads(block.strip())
        except Exception:
            continue
        if data.get("@type") == "FAQPage":
            for q in data.get("mainEntity", []):
                q_name = re.sub(r'\s+', ' ', q.get("name", "")).strip()
                if q_name and q_name not in unescaped_norm:
                    err(f"FAQPage question not visible in HTML on {rel}: {q_name}")
            ok()

# Verify key fragment anchor (#calculator) exists on index.html
idx_txt = read_file(os.path.join(ROOT, "index.html")) or ""
if 'id="calculator"' in idx_txt or "id='calculator'" in idx_txt:
    ok()
else:
    err("Missing id='calculator' target on index.html")

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
