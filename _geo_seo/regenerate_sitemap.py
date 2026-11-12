#!/usr/bin/env python3
"""
Saffire EV — Sitemap Regenerator
Run from repo root: python3 _geo_seo/regenerate_sitemap.py

Rebuilds sitemap.xml from scratch based on:
1. Known static pages (hardcoded list)
2. Indexable location pages (from city_data.json, index=true only)
"""

import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "_geo_seo", "city_data.json")
SITEMAP_FILE = os.path.join(ROOT, "sitemap.xml")
TODAY = date.today().isoformat()

STATIC_PAGES = [
    {"url": "https://saffireev.com/", "freq": "weekly", "priority": "1.0"},
    {"url": "https://saffireev.com/products/", "freq": "weekly", "priority": "0.9"},
    {"url": "https://saffireev.com/about/", "freq": "monthly", "priority": "0.8"},
    {"url": "https://saffireev.com/vision/", "freq": "monthly", "priority": "0.7"},
    {"url": "https://saffireev.com/contact/", "freq": "monthly", "priority": "0.8"},
    {"url": "https://saffireev.com/terms/", "freq": "yearly", "priority": "0.3"},
    {"url": "https://saffireev.com/products/saffire-smart-ride/", "freq": "weekly", "priority": "0.85"},
    {"url": "https://saffireev.com/products/saffire-swiss-cargo/", "freq": "weekly", "priority": "0.85"},
    {"url": "https://saffireev.com/electric-cargo-loader/", "freq": "monthly", "priority": "0.8"},
    {"url": "https://saffireev.com/electric-passenger-auto/", "freq": "monthly", "priority": "0.8"},
    {"url": "https://saffireev.com/l5-electric-vehicle/", "freq": "monthly", "priority": "0.6"},
    {"url": "https://saffireev.com/ev-dealership-india/", "freq": "monthly", "priority": "0.8"},
    {"url": "https://saffireev.com/electric-three-wheeler-running-cost/", "freq": "monthly", "priority": "0.7"},
    {"url": "https://saffireev.com/locations/", "freq": "weekly", "priority": "0.8"},
]

def build_url_entry(url, freq, priority, lastmod=None):
    lm = lastmod or TODAY
    return f"""  <url>
    <loc>{url}</loc>
    <lastmod>{lm}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>"""

def main():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    cities = [c for c in data["cities"] if c.get("index")]

    entries = []
    for p in STATIC_PAGES:
        entries.append(build_url_entry(p["url"], p["freq"], p["priority"]))

    for c in cities:
        entries.append(build_url_entry(
            f"https://saffireev.com/locations/{c['slug']}/",
            "monthly", "0.65"
        ))

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "\n".join(entries)
    sitemap += "\n</urlset>\n"

    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(sitemap)

    print(f"Regenerated sitemap.xml: {len(STATIC_PAGES)} static + {len(cities)} city URLs = {len(STATIC_PAGES)+len(cities)} total")

if __name__ == "__main__":
    main()

