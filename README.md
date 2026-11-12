# SAFFIRE EV — GEO + SEO System

**Repository:** `geo-seo-implementation` branch  
**Company:** KOYO GEARS INDIA PRIVATE LIMITED  
**Brand:** SAFFIRE EV  
**Website:** https://saffireev.com

---

## What Was Built

This branch adds a production-ready Generative Engine Optimization (GEO) + Local SEO system to the existing saffireev.com website without changing its visual design. It introduces:

- **96 city location pages** at `/locations/<city>/` (92 indexable, 4 draft/noindex)
- **Location directory page** at `/locations/` with city search and state filter
- **Improved structured data** (Organization, WebSite, Product, BreadcrumbList, FAQPage, ItemList)
- **Improved `llms.txt`** for AI search engine readability
- **Updated `robots.txt`** with AI crawler permissions
- **Updated `sitemap.xml`** with 106 total URLs (14 static + 92 city pages)
- **"Locations" link** added to the main navigation and footer

---

## How to Add a New City

1. Open `_geo_seo/city_data.json`
2. Add a new object to the `"cities"` array with these fields:

```json
{
  "slug": "your-city-name",
  "name": "Your City Name",
  "hindi_name": "हिंदी नाम",
  "state": "State Name",
  "state_slug": "state-name",
  "region": "Region Name",
  "tier": "tier2",
  "population_approx": "0.5M",
  "index": false,
  "notes": "Internal notes about the city's commercial context.",
  "use_cases": "describe main use cases here",
  "nearby": ["slug1", "slug2", "slug3"]
}
```

3. Set `"index": false` initially (keeps it as draft/noindex)
4. Run the generator:

```bash
python3 _geo_seo/generate_locations.py
```

5. Review the generated page at `locations/<your-city-name>/index.html`
6. When you're satisfied the page has sufficient accurate content, set `"index": true`
7. Regenerate:

```bash
python3 _geo_seo/generate_locations.py
```

---

## How to Update City Content

The city page content is primarily driven by fields in `city_data.json`:

| Field | Used For |
|-------|----------|
| `name` | H1, page title, meta description |
| `hindi_name` | Hindi language reference on the page |
| `state` / `region` | Context paragraphs, state grouping in directory |
| `notes` | Internal only — not shown on page |
| `use_cases` | "Local Applications" section copy |
| `nearby` | Nearby city links at page bottom |

After updating `city_data.json`, re-run:

```bash
python3 _geo_seo/generate_locations.py
```

**Important:** City pages are fully generated from templates. Do not hand-edit the generated HTML in `locations/` — your changes will be overwritten on the next generation run. If you need to customise specific pages heavily, extract those city objects into a separate "custom content" section in the generator.

---

## How to Add a Verified Dealer

Currently, **no dealer locations are confirmed** for any city outside Meerut. If a dealer is confirmed:

1. Add a `"dealer"` field to the city object in `city_data.json`:

```json
"dealer": {
  "name": "Dealer Business Name",
  "address": "Full verified address",
  "phone": "+91-XXXXXXXXXX",
  "verified_date": "2026-11-12"
}
```

2. Update the generator (`_geo_seo/generate_locations.py`) in `generate_city_page()` to render the dealer section when `city.get("dealer")` is present.
3. Only add dealer information from **confirmed, verified** sources. Do not guess or infer.

---

## How to Mark a City Page Indexable

1. Open `_geo_seo/city_data.json`
2. Find the city and change `"index": false` to `"index": true`
3. Re-run the generator: `python3 _geo_seo/generate_locations.py`
4. The page will now carry `<meta content="index, follow" name="robots"/>` and be included in `sitemap.xml`

**Criteria before marking a page indexable:**
- Use cases are specific to that city (not just generic copy)
- The city notes field has meaningful commercial context
- The page would genuinely help a user searching for KOYO/SAFFIRE EV in that city

---

## How to Regenerate the Sitemap

The generator automatically updates `sitemap.xml`. You can also run just the sitemap script:

```bash
python3 _geo_seo/regenerate_sitemap.py
```

This rebuilds `sitemap.xml` from scratch based on:
- The hardcoded static pages list in the script
- All `index: true` cities in `city_data.json`

---

## How to Run Validation Checks

```bash
python3 _geo_seo/validate.py
```

Checks:
- All sitemap URLs exist on disk
- JSON-LD blocks are valid JSON
- Canonical tags are present and match the expected URL
- Indexable pages do not have `noindex`
- Key internal links are not broken
- Titles and meta descriptions are present

---

## How to Deploy Updates

This site is hosted on **GitHub Pages** (custom domain: saffireev.com).

1. Ensure you are on the `geo-seo-implementation` branch:
   ```bash
   git branch --show-current
   ```

2. Run all generators and validation:
   ```bash
   python3 _geo_seo/generate_locations.py
   python3 _geo_seo/validate.py
   ```

3. Commit changes:
   ```bash
   git add -A
   git commit -m "Your commit message"
   ```

4. Create a Pull Request from `geo-seo-implementation` → `main`
5. Review the PR, then merge
6. GitHub Pages will deploy automatically from `main`

---

## Submitting the Sitemap to Search Engines

### Google Search Console

1. Go to https://search.google.com/search-console/
2. Select `saffireev.com`
3. Navigate to **Sitemaps** in the left menu
4. Enter: `https://saffireev.com/sitemap.xml`
5. Click **Submit**

### Bing Webmaster Tools

1. Go to https://www.bing.com/webmasters/
2. Sign in and select your site
3. Navigate to **Sitemaps**
4. Add: `https://saffireev.com/sitemap.xml`
5. Click **Submit**

---

## Project Structure

```
saffireev.com/
├── _geo_seo/                        ← SEO tooling (not served)
│   ├── city_data.json               ← All 96 city records (source of truth)
│   ├── generate_locations.py        ← Generates /locations/ pages
│   ├── regenerate_sitemap.py        ← Rebuilds sitemap.xml from scratch
│   └── validate.py                  ← Validation checks
├── locations/
│   ├── index.html                   ← /locations/ directory page
│   ├── meerut/index.html            ← /locations/meerut/
│   ├── delhi/index.html             ← /locations/delhi/
│   └── ... (96 city folders total)
├── products/
│   ├── saffire-smart-ride/index.html
│   └── saffire-swiss-cargo/index.html
├── index.html                       ← Homepage (Locations nav link added)
├── sitemap.xml                      ← 106 URLs
├── robots.txt                       ← AI-crawler permissions
└── llms.txt                         ← AI-readable company/product summary
```

---

## Important Notes

- **Do not publish low-quality doorway pages.** City pages with `index: false` will not be in the sitemap.
- **Do not invent dealer addresses, subsidy eligibility, or certifications.** Only add information that is confirmed.
- **Range and spec figures** (200 km, 6.3 kW, 600 kg) are from the existing `llms.txt` and product pages. Only update them if official manufacturer data changes.
- **The existing website design is preserved.** Only the navigation and footer gained a "Locations" link.
