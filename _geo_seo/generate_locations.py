#!/usr/bin/env python3
"""
Saffire EV — Location Page Generator
Generates /locations/ directory page and individual city pages.
Run from the repository root: python3 _geo_seo/generate_locations.py

Only cities with index=true are added to the XML sitemap.
Cities with index=false are generated but carry <meta name="robots" content="noindex">.
"""

import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "_geo_seo", "city_data.json")
LOCATIONS_DIR = os.path.join(ROOT, "locations")
SITEMAP_FILE = os.path.join(ROOT, "sitemap.xml")
TODAY = date.today().isoformat()

# ── Shared design tokens (identical to index.html) ─────────────────────────
TAILWIND_CFG = """
tailwind.config = {
    darkMode: "class",
    theme: {
        extend: {
            "colors": {
                "primary": "#97fdff",
                "inverse-on-surface": "#303032",
                "surface-container-lowest": "#0e0e10",
                "surface-container-low": "#1b1b1d",
                "secondary-container": "#47494e",
                "tertiary-fixed-dim": "#f3bf26",
                "tertiary-container": "#fec931",
                "surface-tint": "#2ddbde",
                "outline-variant": "#3b494c",
                "on-secondary": "#2e3035",
                "on-primary": "#003738",
                "on-secondary-fixed": "#191c20",
                "on-surface-variant": "#bac9cc",
                "secondary": "#c5c6cc",
                "inverse-primary": "#00696b",
                "surface-container-high": "#2a2a2c",
                "primary-container": "#3fe6e8",
                "on-background": "#e5e1e4",
                "surface-container": "#201f21",
                "on-surface": "#e5e1e4",
                "surface": "#131315",
                "surface-variant": "#353437",
                "surface-dim": "#131315",
                "on-error": "#690005",
                "primary-fixed-dim": "#2ddbde",
                "on-primary-fixed-variant": "#004f51",
                "surface-bright": "#39393b",
                "on-primary-container": "#006365",
                "background": "#131315",
                "surface-container-highest": "#353437",
                "outline": "#849396"
            },
            "borderRadius": {
                "DEFAULT": "0.125rem",
                "lg": "0.25rem",
                "xl": "0.5rem",
                "full": "0.75rem"
            },
            "fontFamily": {
                "headline": ["Space Grotesk"],
                "body": ["Manrope"],
                "label": ["Space Grotesk"]
            }
        },
    },
}
""".strip()

SHARED_CSS = """
body { font-family: 'Manrope', sans-serif; background-color: #131315; color: #E5E1E4; }
.font-headline { font-family: 'Space Grotesk', sans-serif; }
.material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; }
.kinetic-gradient { background: linear-gradient(45deg, #97FDFF 0%, #3FE6E8 100%); }
.glass-panel { backdrop-filter: blur(20px); background: rgba(53, 52, 55, 0.6); }
""".strip()

NAVBAR = """
<nav class="fixed top-0 w-full z-50 bg-[#131315]/80 backdrop-blur-xl border-b border-[#3B494C]/15 shadow-[0_0_40px_rgba(151,253,255,0.06)]">
  <div class="flex justify-between items-center px-6 md:px-8 h-20 w-full max-w-screen-2xl mx-auto">
    <a class="flex items-center gap-3 group" href="/">
      <div class="relative flex items-center justify-center w-10 h-10 md:w-11 md:h-11 shrink-0">
        <img alt="Saffire EV by Koyo Gears India Private Limited Logo" class="absolute inset-0 w-full h-full object-contain" src="/images/logo_final.png"/>
      </div>
      <div class="flex flex-col justify-center">
        <span class="text-[20px] md:text-[22px] font-bold tracking-tighter text-[#97FDFF] uppercase font-headline leading-none hover:text-white transition-colors">SAFFIRE</span>
        <span class="text-[8px] md:text-[9px] font-label tracking-[0.2em] text-on-surface-variant leading-none mt-1 uppercase">BY KOYO GEARS INDIA</span>
      </div>
    </a>
    <div class="hidden md:flex items-center space-x-12">
      <a class="text-[#E5E1E4]/70 hover:text-[#E5E1E4] transition-colors font-label text-xs tracking-widest uppercase" href="/">Home</a>
      <a class="text-[#E5E1E4]/70 hover:text-[#E5E1E4] transition-colors font-label text-xs tracking-widest uppercase" href="/products/">Products</a>
      <a class="text-[#E5E1E4]/70 hover:text-[#E5E1E4] transition-colors font-label text-xs tracking-widest uppercase" href="/about/">About</a>
      <a class="text-[#E5E1E4]/70 hover:text-[#E5E1E4] transition-colors font-label text-xs tracking-widest uppercase" href="/vision/">Vision</a>
      <a class="text-[#97FDFF] border-b-2 border-[#97FDFF] pb-1 font-label text-xs tracking-widest uppercase" href="/locations/">Locations</a>
      <a class="text-[#E5E1E4]/70 hover:text-[#E5E1E4] transition-colors font-label text-xs tracking-widest uppercase" href="/contact/">Contact</a>
    </div>
    <a class="hidden md:flex kinetic-gradient text-on-primary px-6 py-2 text-xs font-bold tracking-widest rounded-sm duration-200 uppercase" href="/contact/">PRE-ORDER</a>
    <button aria-expanded="false" aria-label="Toggle navigation menu" class="md:hidden text-white flex items-center" id="mobile-menu-btn">
      <span class="material-symbols-outlined text-3xl">menu</span>
    </button>
  </div>
  <div class="absolute top-20 left-0 w-full bg-[#131315]/95 backdrop-blur-3xl border-b border-outline-variant/30 flex flex-col gap-6 shadow-[0_8px_30px_rgba(0,0,0,0.5)] origin-top transition-all duration-300 scale-y-0 opacity-0 pointer-events-none md:hidden p-6 z-40" id="mobile-menu">
    <a class="font-label text-lg uppercase tracking-wider pb-2 border-b border-outline-variant/20 text-[#E5E1E4]/70" href="/">Home</a>
    <a class="font-label text-lg uppercase tracking-wider pb-2 border-b border-outline-variant/20 text-[#E5E1E4]/70" href="/products/">Products</a>
    <a class="font-label text-lg uppercase tracking-wider pb-2 border-b border-outline-variant/20 text-[#E5E1E4]/70" href="/about/">About</a>
    <a class="font-label text-lg uppercase tracking-wider pb-2 border-b border-outline-variant/20 text-[#E5E1E4]/70" href="/vision/">Vision</a>
    <a class="font-label text-lg uppercase tracking-wider pb-2 border-b border-outline-variant/20 text-[#97FDFF]" href="/locations/">Locations</a>
    <a class="font-label text-lg uppercase tracking-wider pb-2 text-[#E5E1E4]/70" href="/contact/">Contact</a>
    <a class="kinetic-gradient text-on-primary px-8 py-4 w-full mt-2 text-sm font-label font-bold uppercase tracking-widest rounded-full text-center" href="/contact/">Pre-Order</a>
  </div>
</nav>
<script>
const menuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
menuBtn.addEventListener('click', () => {
    const isClosed = mobileMenu.classList.contains('opacity-0');
    if (isClosed) {
        mobileMenu.classList.remove('opacity-0','scale-y-0','pointer-events-none');
        mobileMenu.classList.add('opacity-100','scale-y-100','pointer-events-auto');
        menuBtn.querySelector('span').textContent = 'close';
    } else {
        mobileMenu.classList.add('opacity-0','scale-y-0','pointer-events-none');
        mobileMenu.classList.remove('opacity-100','scale-y-100','pointer-events-auto');
        menuBtn.querySelector('span').textContent = 'menu';
    }
});
</script>
""".strip()

FOOTER = """
<footer class="bg-[#0E0E10] border-t border-[#3B494C]/15 mt-auto">
  <div class="max-w-screen-2xl mx-auto px-8 md:px-12 py-10 md:py-16">
    <div class="grid grid-cols-1 lg:grid-cols-4 md:grid-cols-2 gap-10 mb-10">
      <div class="flex flex-col items-center md:items-start text-center md:text-left">
        <span class="text-2xl font-bold tracking-tighter text-[#97FDFF] uppercase font-headline mb-1">SAFFIRE</span>
        <span class="text-[8px] md:text-[9px] tracking-[0.3em] text-slate-500 font-label">BY KOYO GEARS INDIA PRIVATE LIMITED</span>
      </div>
      <div class="flex flex-col items-center md:items-start text-center md:text-left">
        <span class="font-label text-xs tracking-widest uppercase text-on-surface mb-4">Company</span>
        <a class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors" href="/products/">Products</a>
        <a class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors" href="/about/">About</a>
        <a class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors" href="/vision/">Vision</a>
        <a class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors" href="/locations/">Locations</a>
        <a class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors" href="/contact/">Contact</a>
      </div>
      <div class="flex flex-col items-center md:items-start text-center md:text-left">
        <span class="font-label text-xs tracking-widest uppercase text-on-surface mb-4">EV Guides</span>
        <a class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors" href="/electric-cargo-loader/">Electric Cargo Loader</a>
        <a class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors" href="/electric-passenger-auto/">Electric Passenger Auto</a>
        <a class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors" href="/l5-electric-vehicle/">L5 Electric Vehicle</a>
        <a class="text-sm font-light text-slate-400 hover:text-white mb-2 transition-colors" href="/ev-dealership-india/">EV Dealership in India</a>
        <a class="text-sm font-light text-slate-400 hover:text-white transition-colors" href="/electric-three-wheeler-running-cost/">Running Cost</a>
      </div>
      <div class="flex flex-col items-center md:items-start text-center md:text-left">
        <span class="font-label text-xs tracking-widest uppercase text-on-surface mb-4">Connect With Us</span>
        <a aria-label="Follow Saffire EV on Instagram" class="text-sm font-light text-slate-400 hover:text-primary mb-2 transition-colors" href="https://www.instagram.com/saffire.ev/" rel="noopener noreferrer" target="_blank">Instagram</a>
        <a aria-label="Follow Saffire EV on Facebook" class="text-sm font-light text-slate-400 hover:text-primary mb-2 transition-colors" href="https://www.facebook.com/share/1EWsS3CnwN/?mibextid=wwXIfr" rel="noopener noreferrer" target="_blank">Facebook</a>
        <a aria-label="Follow Saffire EV on LinkedIn" class="text-sm font-light text-slate-400 hover:text-primary mb-2 transition-colors" href="https://www.linkedin.com/in/saffire-ev-822009402" rel="noopener noreferrer" target="_blank">LinkedIn</a>
        <a aria-label="Chat with Saffire EV on WhatsApp" class="text-sm font-light text-slate-400 hover:text-primary transition-colors" href="https://wa.me/919258172967?text=Hello%20Saffire%20EV%2C%20I%20want%20to%20know%20more%20about%20your%20vehicles." rel="noopener noreferrer" target="_blank">WhatsApp</a>
      </div>
    </div>
    <div class="border-t border-[#3B494C]/15 pt-6 flex flex-col md:flex-row justify-between items-center gap-6">
      <div class="text-slate-500 font-label text-[9px] md:text-[10px] tracking-[0.05em] uppercase text-center md:text-left">
        &copy; 2026 KOYO GEARS INDIA PRIVATE LIMITED. ALL RIGHTS RESERVED.
      </div>
      <div class="flex flex-wrap justify-center gap-6">
        <a class="font-label text-[10px] md:text-xs uppercase tracking-[0.05em] text-slate-500 hover:text-white transition-opacity" href="/terms/">Privacy</a>
        <a class="font-label text-[10px] md:text-xs uppercase tracking-[0.05em] text-slate-500 hover:text-white transition-opacity" href="/terms/">Terms</a>
      </div>
    </div>
  </div>
</footer>
""".strip()

HEAD_COMMON = """
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<link href="/images/logo_final.png" rel="icon" type="image/jpeg"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Manrope:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<meta content="#131315" name="theme-color"/>
<meta content="D334E6EBCA70575B360E942A1A5E4D8E" name="msvalidate.01"/>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XV903N1WWH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XV903N1WWH');
  function trackEvent(e,p={}) { if(typeof gtag==='function') gtag('event',e,p); }
</script>
<script>
if (window.location.hostname.includes('github.io')) {
  var m=document.createElement('meta');m.name='robots';m.content='noindex';
  document.getElementsByTagName('head')[0].appendChild(m);
}
</script>
""".strip()

# ── WhatsApp enquiry helper ──────────────────────────────────────────────────
def wa_link(city, product=""):
    msg = f"Hello Saffire EV, I am interested in your electric vehicles for {city}."
    if product:
        msg += f" I want to know more about the {product}."
    return f"https://wa.me/919258172967?text={msg.replace(' ', '%20')}"

# ── City intro paragraphs (unique per city tier/region) ────────────────────
def city_intro(city):
    name = city["name"]
    state = city["state"]
    region = city["region"]
    use = city["use_cases"]
    tier = city["tier"]

    if tier == "metro":
        scale = f"{name} is one of India's largest metropolitan centres"
    elif tier == "tier1":
        scale = f"{name} is a major commercial and urban centre in {state}"
    else:
        scale = f"{name} is an important city in {state}"

    return (
        f'<a href="/about/" class="text-primary hover:underline font-medium">KOYO GEARS INDIA PRIVATE LIMITED</a> '
        f'(widely searched as <strong>KOYO</strong>, <strong>KOYO Gears India</strong>, <strong>KOYO Auto</strong>, and <strong>KOYO L5</strong>) '
        f'is the official manufacturer behind the <a href="/" class="text-primary hover:underline font-medium">SAFFIRE EV</a> brand, '
        f'building heavy-duty <a href="/l5-electric-vehicle/" class="text-primary hover:underline">KOYO L5 electric three-wheelers</a> '
        f'for India\'s passenger and commercial transport needs. '
        f"{scale}, where the demand for affordable, reliable and low-emission commercial vehicles is growing steadily. "
        f'The <a href="/products/" class="text-primary hover:underline">SAFFIRE EV (KOYO Auto)</a> range is engineered for the {region} region, '
        f"covering use cases such as {use}. "
        f'This page provides verified specifications for <a href="/" class="text-primary hover:underline">SAFFIRE EV</a> '
        f'(<a href="/products/saffire-smart-ride/" class="text-primary hover:underline">Smart Ride KOYO Passenger Auto</a> &amp; '
        f'<a href="/products/saffire-swiss-cargo/" class="text-primary hover:underline">Swiss Cargo KOYO Loader</a>) '
        f"relevant to operators, fleet buyers, and prospective dealers based in or near {name}, {state}."
    )

# ── City-specific FAQ (varies by region/use case) ──────────────────────────
def city_faqs(city):
    name = city["name"]
    state = city["state"]
    use = city["use_cases"]
    slug = city["slug"]

    faqs = [
        {
            "q": f"What is the on-road price of Saffire Auto & Koyo L5 electric auto rickshaw in {name}?",
            "a": (
                f"The on-road price of Saffire Auto (Saffire Smart Ride / Koyo L5) in {name}, {state} depends on "
                f"applicable state EV subsidies, commercial RTO permit fees, and insurance coverage. "
                f"Operating at just ₹1.20/km, Saffire Auto saves commercial drivers in {name} over ₹14,126 every month "
                f"compared to traditional diesel auto rickshaws. Click 'Get Instant Quotation' or WhatsApp +91-92581-72967 for an exact {name} price quote."
            )
        },
        {
            "q": f"Are KOYO Auto, KOYO L5, Saffire Auto, and SAFFIRE EV the same brand in {name}?",
            "a": (
                f"Yes. KOYO GEARS INDIA PRIVATE LIMITED (KOYO Gears India Pvt Ltd) is the parent engineering organization and manufacturer "
                f"that markets its L5 electric three-wheelers under the SAFFIRE EV brand. When customers in {name}, {state} "
                f"search for KOYO Auto, KOYO L5, KOYO Electric 3 Wheeler, Saffire Auto, or Saffire 3 Wheeler Auto, the official vehicles "
                f"are the SAFFIRE Smart Ride (passenger auto rickshaw) and SAFFIRE Swiss Cargo (commercial cargo loader)."
            )
        },
        {
            "q": f"How can I apply for a Saffire Auto & Koyo L5 electric 3 wheeler dealership in {name}?",
            "a": (
                f"Automobile dealers, fleet managers, and commercial distributors in {name} or {state} can apply for an "
                f"exclusive SAFFIRE EV (Koyo Gears India) dealership through saffireev.com/ev-dealership-india/ or by sending a WhatsApp "
                f"to +91-92581-72967. Koyo Gears India provides territorial exclusivity across {name}, technician training, and marketing support."
            )
        },
        {
            "q": f"How much extra profit does a Saffire 3 wheeler auto earn compared to diesel autos in {name}?",
            "a": (
                f"A commercial auto driver covering 100 to 120 km daily in {name} spends approximately ₹120 to ₹144 per day on electricity "
                f"with a Saffire 3 wheeler auto (₹1.20/km), compared to ₹550 to ₹660 per day with a diesel auto (₹5.50/km). "
                f"This generates a net extra profit of over ₹14,126 every month or over ₹8.4 Lakhs in cumulative savings over 5 years."
            )
        },
        {
            "q": f"Who manufactures KOYO electric autos sold in {name}, {state}?",
            "a": (
                f"KOYO electric autos are manufactured by KOYO GEARS INDIA PRIVATE LIMITED (KOYO Gears India), "
                f"operating under the SAFFIRE EV brand. The company is headquartered in Meerut, Uttar Pradesh, India. "
                f"For enquiries about KOYO Auto / SAFFIRE EV products available for {name} and surrounding areas, "
                f"contact the company directly via the official website at saffireev.com or by WhatsApp."
            )
        },
        {
            "q": f"What are the running cost advantages of KOYO Auto (SAFFIRE EV) vehicles compared to diesel autos in {name}?",
            "a": (
                f"KOYO L5 electric three-wheelers by SAFFIRE EV generally have significantly lower running costs per kilometre than "
                f"diesel or CNG autos because electricity tariffs are lower than fossil fuel costs and "
                f"EVs have fewer mechanical components requiring routine servicing. "
                f"The exact savings depend on local electricity tariffs, usage patterns, and route conditions in {name}. "
                f"SAFFIRE EV provides an illustrative profitability calculator at saffireev.com to help operators estimate savings."
            )
        },
        {
            "q": f"How can I enquire about a KOYO Auto / SAFFIRE EV dealership opportunity in {name}, {state}?",
            "a": (
                f"Businesses interested in becoming an authorised SAFFIRE EV (KOYO Gears India) dealer in {name} or the surrounding {state} region "
                f"can submit an enquiry through the official contact page at saffireev.com/contact/ or "
                f"send a WhatsApp message to +91-92581-72967. "
                f"KOYO GEARS INDIA PRIVATE LIMITED evaluates dealer applications based on regional market potential and business capability."
            )
        },
        {
            "q": f"Does KOYO Gears India (SAFFIRE EV) have a service centre or showroom in {name}?",
            "a": (
                f"At the time of this page's last update, SAFFIRE EV by KOYO Gears India has not published a confirmed showroom or "
                f"service centre address specifically in {name}. "
                f"For the most current information on authorised KOYO Auto / SAFFIRE EV service and sales points near {name}, "
                f"please contact the company directly at inquiry@saffireev.com or via WhatsApp at +91-92581-72967."
            )
        }
    ]
    return faqs

# ── Nearby city links ──────────────────────────────────────────────────────
def nearby_links(city, all_cities_by_slug):
    links = []
    for s in city.get("nearby", [])[:5]:
        c = all_cities_by_slug.get(s)
        if c:
            links.append(f'<a href="/locations/{s}/" class="text-primary hover:underline text-sm">{c["name"]}</a>')
    return links

# ── GENERATE CITY PAGE ─────────────────────────────────────────────────────
def generate_city_page(city, all_cities_by_slug):
    name = city["name"]
    slug = city["slug"]
    state = city["state"]
    hindi = city.get("hindi_name", "")
    region = city["region"]
    index_page = city.get("index", False)
    canonical = f"https://saffireev.com/locations/{slug}/"

    robots_meta = '<meta content="index, follow" name="robots"/>' if index_page else '<meta content="noindex, follow" name="robots"/>'
    noindex_comment = "" if index_page else "<!-- noindex: insufficient city-specific data to index -->\n    "

    seo_title = f"Saffire Auto & Koyo L5 Electric 3 Wheeler in {name} | Best L5 Auto Rickshaw Price"
    seo_desc = (
        f"Looking for Saffire Auto, Koyo Auto, or Koyo L5 in {name}, {state}? "
        f"Saffire EV by Koyo Gears India manufactures ICAT certified L5 electric auto rickshaws & 3 wheeler loaders "
        f"with 200 km range, 600 kg payload, and ₹1.20/km running cost in {name}."
    )
    seo_keywords = (
        f"Saffire Auto {name}, Saffire 3 Wheeler {name}, Saffire 3 Wheeler Auto {name}, "
        f"KOYO Auto {name}, KOYO L5 {name}, KOYO Gears India {name}, L5 Auto {name}, "
        f"L5 Auto Rickshaw {name}, Electric Auto Rickshaw {name}, Auto Rickshaw {name}, "
        f"Electric 3 Wheeler {name}, SAFFIRE Smart Ride {name}, SAFFIRE Swiss Cargo {name}, {state}"
    )
    og_title = seo_title
    og_desc = seo_desc
    state_slug = state.lower().replace(" ", "-")

    intro = city_intro(city)
    faqs = city_faqs(city)
    nearby = nearby_links(city, all_cities_by_slug)
    use_cases = city["use_cases"]

    # Organization + Brand Entity JSON-LD
    org_jsonld = f"""{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://saffireev.com/#organization",
  "name": "SAFFIRE EV",
  "legalName": "KOYO GEARS INDIA PRIVATE LIMITED",
  "alternateName": [
    "KOYO",
    "KOYO Auto",
    "KOYO Electric Auto",
    "KOYO L5",
    "KOYO Electric Rickshaw",
    "KOYO Three Wheeler",
    "KOYO Gears India",
    "KOYO Gears India Private Limited",
    "Saffire EV by Koyo Gears India"
  ],
  "url": "https://saffireev.com",
  "logo": "https://saffireev.com/images/logo_final.png",
  "areaServed": {{
    "@type": "City",
    "name": "{name}",
    "containedInPlace": {{
      "@type": "AdministrativeArea",
      "name": "{state}"
    }}
  }},
  "brand": {{
    "@type": "Brand",
    "name": "SAFFIRE EV",
    "alternateName": ["KOYO Auto", "KOYO L5", "KOYO Electric Auto", "KOYO Gears India"]
  }},
  "sameAs": [
    "https://www.instagram.com/saffire.ev/",
    "https://www.facebook.com/share/1EWsS3CnwN/?mibextid=wwXIfr",
    "https://www.linkedin.com/in/saffire-ev-822009402"
  ]
}}"""

    # ItemList JSON-LD for Products in City
    itemlist_jsonld = f"""{{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "KOYO L5 / SAFFIRE EV Electric Three-Wheelers for {name}, {state}",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "SAFFIRE Smart Ride — KOYO L5 Electric Passenger Auto",
      "url": "https://saffireev.com/products/saffire-smart-ride/"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "SAFFIRE Swiss Cargo — KOYO L5 Electric Cargo Loader",
      "url": "https://saffireev.com/products/saffire-swiss-cargo/"
    }}
  ]
}}"""

    # Breadcrumb JSON-LD
    breadcrumb_jsonld = f"""{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "SAFFIRE EV (KOYO Gears India)", "item": "https://saffireev.com/"}},
    {{"@type": "ListItem", "position": 2, "name": "KOYO Auto Locations", "item": "https://saffireev.com/locations/"}},
    {{"@type": "ListItem", "position": 3, "name": "KOYO Electric Auto in {name}", "item": "{canonical}"}}
  ]
}}"""

    # FAQ JSON-LD
    faq_items = ",\n    ".join([
        f'{{"@type":"Question","name":{json.dumps(f["q"])},"acceptedAnswer":{{"@type":"Answer","text":{json.dumps(f["a"])}}}}}'
        for f in faqs
    ])
    faq_jsonld = f"""{{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "mainEntity": [\n    {faq_items}\n  ]\n}}"""

    nearby_html = ""
    if nearby:
        nearby_html = f"""
<section class="mt-16 pt-10 border-t border-outline-variant/20">
  <h2 class="font-headline text-2xl font-bold mb-6 text-[#E5E1E4]">Nearby Cities</h2>
  <p class="text-on-surface-variant text-sm mb-4">Explore SAFFIRE EV information for cities near {name}:</p>
  <div class="flex flex-wrap gap-3">
    {"".join(f'<a href="/locations/{s}/" class="glass-panel border border-outline-variant/20 px-4 py-2 rounded text-sm text-primary hover:border-primary/40 transition-colors">{all_cities_by_slug[s]["name"]}</a>' for s in city.get("nearby", [])[:5] if s in all_cities_by_slug)}
  </div>
</section>""".strip()

    faq_html_items = "\n".join([
        f"""<div class="border border-outline-variant/20 rounded-xl p-6 bg-surface-container-low">
  <h3 class="font-headline font-bold text-base md:text-lg mb-3 text-[#E5E1E4]">{f["q"]}</h3>
  <p class="text-on-surface-variant text-sm font-light leading-relaxed">{f["a"]}</p>
</div>"""
        for f in faqs
    ])

    hindi_section = f'<p class="text-on-surface-variant text-sm mt-2 font-light">{hindi} में KOYO इलेक्ट्रिक ऑटो — SAFFIRE EV के L5 इलेक्ट्रिक थ्री-व्हीलर वाहनों की जानकारी के लिए यहाँ संपर्क करें।</p>' if hindi else ""

    html = f"""<!DOCTYPE html>
<html class="dark" lang="en">
<head>
{HEAD_COMMON}
<title>{seo_title}</title>
<link href="{canonical}" rel="canonical"/>
{robots_meta}
<meta content="{seo_desc}" name="description"/>
<meta content="{seo_keywords}" name="keywords"/>
<meta content="{og_title}" property="og:title"/>
<meta content="{og_desc}" property="og:description"/>
<meta content="https://saffireev.com/images/herobanner.png" property="og:image"/>
<meta content="{canonical}" property="og:url"/>
<meta content="website" property="og:type"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="{og_title}" name="twitter:title"/>
<meta content="{og_desc}" name="twitter:description"/>
<meta content="https://saffireev.com/images/herobanner.png" name="twitter:image"/>
<script type="application/ld+json">{org_jsonld}</script>
<script type="application/ld+json">{itemlist_jsonld}</script>
<script type="application/ld+json">{breadcrumb_jsonld}</script>
<script type="application/ld+json">{faq_jsonld}</script>
<script>{TAILWIND_CFG}</script>
<style>{SHARED_CSS}</style>
</head>
<body class="selection:bg-primary selection:text-on-primary scroll-smooth flex flex-col min-h-screen">

{NAVBAR}

<main class="flex-grow pt-28 pb-24 px-6 md:px-8 max-w-screen-xl mx-auto w-full">

  <!-- Breadcrumb -->
  <nav aria-label="Breadcrumb" class="mb-8 flex flex-wrap items-center gap-2 text-[10px] md:text-xs font-label uppercase tracking-widest text-on-surface-variant">
    <a class="hover:text-primary transition-colors" href="/">SAFFIRE EV (KOYO)</a>
    <span class="material-symbols-outlined text-[14px]">chevron_right</span>
    <a class="hover:text-primary transition-colors" href="/locations/">KOYO Auto Locations</a>
    <span class="material-symbols-outlined text-[14px]">chevron_right</span>
    <span class="text-primary">{name}, {state}</span>
  </nav>

  <!-- Hero -->
  <section class="mb-16">
    <span class="inline-block text-primary font-label text-[10px] font-bold tracking-widest uppercase mb-3">Saffire Auto &amp; Koyo L5 Electric 3 Wheeler Dealership in {name} · {region}</span>
    <h1 class="font-headline font-bold text-4xl md:text-6xl tracking-tighter mb-3 text-[#E5E1E4]">
      Saffire Auto &amp; Koyo L5 Electric 3 Wheeler in {name}
    </h1>
    <h2 class="font-headline text-lg md:text-2xl font-bold text-primary mb-4">
      Best L5 Auto Rickshaw &amp; Electric 3 Wheeler Auto Price in {name}, {state}
    </h2>
    {hindi_section}
    <p class="text-on-surface-variant text-base md:text-lg font-light leading-relaxed mt-6 max-w-3xl">
      {intro}
    </p>
    <div class="flex flex-col sm:flex-row gap-4 mt-8">
      <a class="kinetic-gradient text-on-primary font-headline font-bold py-4 px-8 rounded-sm tracking-widest uppercase text-sm hover:brightness-110 transition-all text-center"
         href="{wa_link(name)}" onclick="trackEvent('city_wa_enquiry',{{city:'{name}'}})" rel="noopener noreferrer" target="_blank">
        Enquire on WhatsApp
      </a>
      <a class="border border-outline-variant/30 text-on-surface font-headline font-bold py-4 px-8 rounded-sm tracking-widest uppercase text-sm hover:bg-surface-container-highest transition-all text-center"
         href="/contact/?city={slug}&amp;state={state_slug}&amp;type=vehicle">Enquire for {name}</a>
    </div>
  </section>

  <!-- Brand Entity Interlinking Box: KOYO <-> SAFFIRE EV -->
  <section class="mb-16 bg-surface-container-low rounded-2xl border border-primary/20 p-6 md:p-8">
    <span class="inline-block text-primary font-label text-[10px] font-bold tracking-widest uppercase mb-2">Official Brand &amp; Manufacturer Reference</span>
    <h2 class="font-headline text-2xl font-bold mb-3 text-[#E5E1E4]">KOYO, KOYO Auto &amp; KOYO L5 in {name} — Powered by SAFFIRE EV &amp; KOYO Gears India</h2>
    <p class="text-on-surface-variant text-sm font-light leading-relaxed mb-4">
      When commercial drivers, fleet owners, and dealers in <strong>{name}, {state}</strong> search for <strong>KOYO</strong>, <strong>KOYO Auto</strong>, <strong>KOYO Electric Auto</strong>, or <strong>KOYO L5</strong>, they are looking for the electric three-wheelers manufactured by <a href="/about/" class="text-primary hover:underline font-medium">KOYO GEARS INDIA PRIVATE LIMITED (KOYO Gears India)</a> under the official brand <a href="/" class="text-primary hover:underline font-medium">SAFFIRE EV</a>. Explore our complete <a href="/l5-electric-vehicle/" class="text-primary hover:underline">KOYO L5 Electric Vehicle</a> lineup below, including the <a href="/electric-passenger-auto/" class="text-primary hover:underline">KOYO Electric Passenger Auto</a> (<a href="/products/saffire-smart-ride/" class="text-primary hover:underline">SAFFIRE Smart Ride</a>) and the <a href="/electric-cargo-loader/" class="text-primary hover:underline">KOYO Electric Cargo Loader</a> (<a href="/products/saffire-swiss-cargo/" class="text-primary hover:underline">SAFFIRE Swiss Cargo</a>).
    </p>
    <div class="flex flex-wrap gap-3 text-xs font-label uppercase tracking-wider">
      <a href="/" class="px-3 py-1.5 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors">SAFFIRE EV Home</a>
      <a href="/about/" class="px-3 py-1.5 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors">KOYO Gears India Profile</a>
      <a href="/l5-electric-vehicle/" class="px-3 py-1.5 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors">KOYO L5 Guide</a>
      <a href="/products/saffire-smart-ride/" class="px-3 py-1.5 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors">KOYO Auto: Smart Ride</a>
      <a href="/products/saffire-swiss-cargo/" class="px-3 py-1.5 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors">KOYO Loader: Swiss Cargo</a>
      <a href="/ev-dealership-india/" class="px-3 py-1.5 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors">KOYO / SAFFIRE EV Dealership</a>
    </div>
  </section>

  <!-- Products -->
  <section class="mb-16">
    <h2 class="font-headline text-3xl md:text-4xl font-bold mb-10 text-[#E5E1E4]">SAFFIRE EV (KOYO L5) Products for {name}</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">

      <!-- Smart Ride -->
      <div class="bg-surface-container-low rounded-2xl border border-outline-variant/10 hover:border-primary/30 transition-colors overflow-hidden flex flex-col">
        <div class="relative aspect-[16/10] overflow-hidden bg-[#0E0E10] p-2">
          <div class="relative w-full h-full rounded-[14px] overflow-hidden">
            <img alt="SAFFIRE Smart Ride — KOYO L5 electric passenger auto three-wheeler in {name}" class="absolute inset-0 w-full h-full object-contain object-center opacity-90" loading="lazy" src="/images/SAFFIRE_PASSANGER.png"/>
            <div class="absolute inset-0 bg-gradient-to-t from-[#0e0e10] via-transparent to-transparent pointer-events-none"></div>
          </div>
        </div>
        <div class="p-8 pt-4 flex flex-col flex-grow justify-between">
          <div>
            <span class="inline-block text-primary font-label text-[10px] font-bold tracking-widest uppercase mb-2">KOYO Auto · D+3 Passenger Electric Three-Wheeler · KOYO L5</span>
            <h3 class="font-headline text-2xl font-bold mb-3 text-[#E5E1E4]"><a href="/products/saffire-smart-ride/" class="hover:text-primary transition-colors">SAFFIRE Smart Ride (KOYO Passenger Auto)</a></h3>
            <p class="text-on-surface-variant text-sm font-light leading-relaxed mb-4">
              The <a href="/products/saffire-smart-ride/" class="text-primary hover:underline">SAFFIRE Smart Ride</a> is <a href="/" class="text-primary hover:underline">SAFFIRE EV</a>'s flagship <a href="/l5-electric-vehicle/" class="text-primary hover:underline">KOYO L5</a> <a href="/electric-passenger-auto/" class="text-primary hover:underline">electric passenger auto</a> by <a href="/about/" class="text-primary hover:underline">KOYO Gears India</a>, designed to carry a driver and three passengers (D+3 layout) in {name}.
            </p>
            <ul class="space-y-2 text-sm text-on-surface-variant mb-6">
              <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">battery_charging_full</span> Battery: 14.61 kWh (63V 232Ah)</li>
              <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">electric_bolt</span> Motor peak power: 6.3 kW</li>
              <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">route</span> Claimed range: up to 200 km per charge</li>
              <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">speed</span> Top speed: 50 km/h</li>
              <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">schedule</span> Charging time: 5–6 hours (standard charger)</li>
              <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">group</span> Capacity: Driver + 3 passengers</li>
            </ul>
          </div>
          <div class="flex flex-col sm:flex-row gap-3">
            <a class="kinetic-gradient text-on-primary font-headline font-bold py-3 px-6 rounded-sm tracking-widest uppercase text-xs hover:brightness-110 transition-all text-center"
               href="/contact/?city={slug}&amp;state={state_slug}&amp;product=smart-ride&amp;type=vehicle">
              Enquire: Smart Ride
            </a>
            <a class="border border-outline-variant/30 text-on-surface font-headline font-bold py-3 px-6 rounded-sm tracking-widest uppercase text-xs hover:bg-surface-container-highest transition-all text-center"
               href="/products/saffire-smart-ride/">View Full Specs</a>
          </div>
        </div>
      </div>

      <!-- Swiss Cargo -->
      <div class="bg-surface-container-low rounded-2xl border border-outline-variant/10 hover:border-primary/30 transition-colors overflow-hidden flex flex-col">
        <div class="relative aspect-[16/10] overflow-hidden bg-[#0E0E10] p-2">
          <div class="relative w-full h-full rounded-[14px] overflow-hidden">
            <img alt="SAFFIRE Swiss Cargo — KOYO L5 electric cargo loader three-wheeler in {name}" class="absolute inset-0 w-full h-full object-contain object-center opacity-90" loading="lazy" src="/images/saffire_loader.png"/>
            <div class="absolute inset-0 bg-gradient-to-t from-[#0e0e10] via-transparent to-transparent pointer-events-none"></div>
          </div>
        </div>
        <div class="p-8 pt-4 flex flex-col flex-grow justify-between">
          <div>
            <span class="inline-block text-primary font-label text-[10px] font-bold tracking-widest uppercase mb-2">KOYO Loader · Electric Cargo Loader · KOYO L5</span>
            <h3 class="font-headline text-2xl font-bold mb-3 text-[#E5E1E4]"><a href="/products/saffire-swiss-cargo/" class="hover:text-primary transition-colors">SAFFIRE Swiss Cargo (KOYO Cargo Loader)</a></h3>
            <p class="text-on-surface-variant text-sm font-light leading-relaxed mb-4">
              The <a href="/products/saffire-swiss-cargo/" class="text-primary hover:underline">SAFFIRE Swiss Cargo</a> is <a href="/" class="text-primary hover:underline">SAFFIRE EV</a>'s heavy-duty <a href="/l5-electric-vehicle/" class="text-primary hover:underline">KOYO L5</a> <a href="/electric-cargo-loader/" class="text-primary hover:underline">electric cargo loader</a> by <a href="/about/" class="text-primary hover:underline">KOYO Gears India</a>, built for last-mile delivery and commercial goods transport in {name}.
            </p>
            <ul class="space-y-2 text-sm text-on-surface-variant mb-6">
              <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">battery_charging_full</span> Battery: 14.61 kWh (63V 232Ah)</li>
              <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">electric_bolt</span> Motor peak power: 6.3 kW</li>
              <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">route</span> Claimed range: up to 200 km per charge</li>
              <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">speed</span> Top speed: 50 km/h</li>
              <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">schedule</span> Charging time: 5–6 hours (standard charger)</li>
              <li class="flex items-center gap-2"><span class="material-symbols-outlined text-primary text-[16px]">inventory_2</span> Payload capacity: 600 kg</li>
            </ul>
          </div>
          <div class="flex flex-col sm:flex-row gap-3">
            <a class="kinetic-gradient text-on-primary font-headline font-bold py-3 px-6 rounded-sm tracking-widest uppercase text-xs hover:brightness-110 transition-all text-center"
               href="/contact/?city={slug}&amp;state={state_slug}&amp;product=swiss-cargo&amp;type=vehicle">
              Enquire: Swiss Cargo
            </a>
            <a class="border border-outline-variant/30 text-on-surface font-headline font-bold py-3 px-6 rounded-sm tracking-widest uppercase text-xs hover:bg-surface-container-highest transition-all text-center"
               href="/products/saffire-swiss-cargo/">View Full Specs</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Battery & Charging -->
  <section class="mb-16 bg-surface-container-low rounded-2xl border border-outline-variant/10 p-8">
    <h2 class="font-headline text-2xl font-bold mb-6 text-[#E5E1E4]">Battery &amp; Charging Information</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="text-center p-4">
        <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-3">
          <span class="material-symbols-outlined text-primary">battery_charging_full</span>
        </div>
        <p class="font-headline font-bold text-lg text-primary mb-1">14.61 kWh</p>
        <p class="text-on-surface-variant text-xs font-label uppercase tracking-widest">Battery Capacity (63V 232Ah)</p>
      </div>
      <div class="text-center p-4">
        <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-3">
          <span class="material-symbols-outlined text-primary">route</span>
        </div>
        <p class="font-headline font-bold text-lg text-primary mb-1">Up to 200 km</p>
        <p class="text-on-surface-variant text-xs font-label uppercase tracking-widest">Claimed Range Per Charge</p>
      </div>
      <div class="text-center p-4">
        <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-3">
          <span class="material-symbols-outlined text-primary">schedule</span>
        </div>
        <p class="font-headline font-bold text-lg text-primary mb-1">5–6 Hours</p>
        <p class="text-on-surface-variant text-xs font-label uppercase tracking-widest">Charging Time (Standard Charger)</p>
      </div>
    </div>
    <p class="text-on-surface-variant text-xs mt-6 italic">
      Note: Claimed range figures are based on manufacturer specifications under standard test conditions.
      Actual range may vary depending on load, terrain, temperature, and driving patterns.
    </p>
  </section>

  <!-- Local Use Cases -->
  <section class="mb-16">
    <h2 class="font-headline text-2xl font-bold mb-6 text-[#E5E1E4]">Commercial Vehicle Applications in {name}</h2>
    <p class="text-on-surface-variant text-base font-light leading-relaxed mb-6 max-w-3xl">
      SAFFIRE EV's L5 electric three-wheelers are suited to a range of commercial and passenger transport applications
      common in {name} and the broader {region} area. Typical use cases include: {use_cases}.
    </p>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-surface-container-low p-6 rounded-xl border-l-4 border-primary">
        <h3 class="font-headline text-lg font-bold mb-2 text-[#E5E1E4]">For Passenger Transport Operators</h3>
        <p class="text-on-surface-variant text-sm font-light">
          The Smart Ride electric auto reduces daily fuel spend for drivers operating regular passenger routes in and around {name}.
          Its D+3 configuration provides practical passenger capacity for city and inter-city feeder routes.
        </p>
      </div>
      <div class="bg-surface-container-low p-6 rounded-xl border-l-4 border-primary">
        <h3 class="font-headline text-lg font-bold mb-2 text-[#E5E1E4]">For Cargo &amp; Logistics Businesses</h3>
        <p class="text-on-surface-variant text-sm font-light">
          The Swiss Cargo electric loader offers businesses in {name} a cost-effective solution for
          last-mile delivery, wholesale market supply, and commercial goods movement with a 600 kg payload capacity.
        </p>
      </div>
    </div>
  </section>

  <!-- Dealer / Enquiry CTA -->
  <section class="mb-16 bg-primary/5 border border-primary/20 rounded-2xl p-8 md:p-12 text-center">
    <h2 class="font-headline text-2xl md:text-3xl font-bold mb-4 text-[#E5E1E4]">Interested in KOYO Auto / SAFFIRE EV in {name}?</h2>
    <p class="text-on-surface-variant text-base font-light mb-8 max-w-2xl mx-auto">
      Whether you are looking to purchase a <a href="/l5-electric-vehicle/" class="text-primary hover:underline">KOYO L5</a> vehicle, explore fleet options, or apply for <a href="/ev-dealership-india/" class="text-primary hover:underline">SAFFIRE EV (KOYO Gears India) dealership opportunities</a>
      in {name} or {state}, get in touch with our team directly.
    </p>
    <div class="flex flex-col sm:flex-row gap-4 justify-center">
      <a class="kinetic-gradient text-on-primary font-headline font-bold py-4 px-10 rounded-sm tracking-widest uppercase text-sm hover:brightness-110 transition-all"
         href="{wa_link(name)}" onclick="trackEvent('city_cta_wa',{{city:'{name}'}})" rel="noopener noreferrer" target="_blank">
        WhatsApp Enquiry
      </a>
      <a class="border border-outline-variant/40 text-on-surface font-headline font-bold py-4 px-10 rounded-sm tracking-widest uppercase text-sm hover:bg-surface-container-highest transition-all"
         href="/contact/?city={slug}&amp;state={state_slug}&amp;type=vehicle">
        Vehicle Enquiry ({name})
      </a>
      <a class="border border-outline-variant/40 text-on-surface font-headline font-bold py-4 px-10 rounded-sm tracking-widest uppercase text-sm hover:bg-surface-container-highest transition-all"
         href="/contact/?city={slug}&amp;state={state_slug}&amp;type=dealer">
        Apply for Dealership ({name})
      </a>
    </div>
  </section>

  <!-- FAQ -->
  <section class="mb-16">
    <h2 class="font-headline text-2xl md:text-3xl font-bold mb-8 text-[#E5E1E4]">Frequently Asked Questions — {name}</h2>
    <div class="space-y-4">
      {faq_html_items}
    </div>
  </section>

  <!-- Running Cost -->
  <section class="mb-16 bg-surface-container-low rounded-xl p-6 border border-outline-variant/10">
    <h2 class="font-headline text-xl font-bold mb-3 text-[#E5E1E4]">Running Cost Comparison</h2>
    <p class="text-on-surface-variant text-sm font-light leading-relaxed mb-4">
      Electric three-wheelers typically have lower running costs per kilometre than diesel or petrol autos.
      SAFFIRE EV offers an interactive profitability calculator on its homepage to help operators
      in {name} estimate their potential monthly savings over traditional fuel vehicles.
    </p>
    <a class="text-primary font-label text-xs font-bold uppercase tracking-widest hover:underline flex items-center gap-1 w-fit"
       href="/electric-three-wheeler-running-cost/">
      View Running Cost Guide <span class="material-symbols-outlined text-[14px]">arrow_forward</span>
    </a>
  </section>

  {nearby_html}

  <!-- Back to Directory -->
  <div class="mt-12 pt-8 border-t border-outline-variant/20">
    <a class="text-primary font-label text-xs font-bold uppercase tracking-widest hover:underline flex items-center gap-2 w-fit"
       href="/locations/">
      <span class="material-symbols-outlined text-[14px]">arrow_back</span> Back to All Locations
    </a>
  </div>

</main>

{FOOTER}

</body>
</html>"""

    return html


# ── GENERATE DIRECTORY PAGE ────────────────────────────────────────────────
def generate_directory_page(cities):
    # Group by state
    states = {}
    for c in cities:
        s = c["state"]
        states.setdefault(s, []).append(c)

    state_order = [
        "Uttar Pradesh", "Delhi", "Haryana", "Rajasthan", "Bihar",
        "Gujarat", "Maharashtra", "Madhya Pradesh", "Punjab", "Chandigarh",
        "Uttarakhand", "Odisha", "West Bengal", "Jharkhand",
        "Karnataka", "Telangana", "Tamil Nadu", "Kerala", "Andhra Pradesh"
    ]

    state_sections = ""
    total_indexable = sum(1 for c in cities if c.get("index"))

    for state in state_order:
        if state not in states:
            continue
        state_cities = states[state]
        city_cards = ""
        for c in state_cities:
            badge = ""
            if not c.get("index"):
                badge = '<span class="text-[9px] font-label text-on-surface-variant/50 ml-1">(coming soon)</span>'
            if c.get("index"):
                city_cards += f"""<a href="/locations/{c['slug']}/"
                   class="glass-panel border border-outline-variant/20 rounded-lg px-4 py-3 text-sm text-on-surface hover:border-primary/40 hover:text-primary transition-all flex items-center gap-2 group">
                  <span class="material-symbols-outlined text-[14px] text-primary/60 group-hover:text-primary">location_on</span>
                  {c['name']}
                </a>"""
            else:
                city_cards += f"""<div class="glass-panel border border-outline-variant/10 rounded-lg px-4 py-3 text-sm text-on-surface-variant/50 flex items-center gap-2 cursor-default">
                  <span class="material-symbols-outlined text-[14px]">location_on</span>
                  {c['name']}{badge}
                </div>"""

        state_sections += f"""
<div class="mb-10" data-state="{state.lower().replace(' ', '-')}">
  <h2 class="font-headline text-xl font-bold mb-4 text-primary tracking-tight">{state}</h2>
  <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
    {city_cards}
  </div>
</div>"""

    html = f"""<!DOCTYPE html>
<html class="dark" lang="en">
<head>
{HEAD_COMMON}
<title>KOYO Electric Auto Locations Across India | SAFFIRE EV (KOYO L5) by KOYO Gears India</title>
<link href="https://saffireev.com/locations/" rel="canonical"/>
<meta content="index, follow" name="robots"/>
<meta content="Find KOYO, KOYO Auto, KOYO L5, and SAFFIRE EV electric three-wheelers by KOYO Gears India Private Limited across 100 Indian cities. Electric passenger autos (Smart Ride) and cargo loaders (Swiss Cargo)." name="description"/>
<meta content="KOYO, KOYO Auto, KOYO Electric Auto, KOYO L5, KOYO Gears India, SAFFIRE EV, KOYO Auto Locations India, SAFFIRE Smart Ride, SAFFIRE Swiss Cargo, L5 Electric Three Wheeler India" name="keywords"/>
<meta content="KOYO Electric Auto Locations Across India | SAFFIRE EV (KOYO L5) by KOYO Gears India" property="og:title"/>
<meta content="Find KOYO, KOYO Auto, KOYO L5, and SAFFIRE EV electric three-wheelers by KOYO Gears India across 100 Indian cities." property="og:description"/>
<meta content="https://saffireev.com/images/herobanner.png" property="og:image"/>
<meta content="https://saffireev.com/locations/" property="og:url"/>
<meta content="website" property="og:type"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="KOYO Electric Auto Locations Across India | SAFFIRE EV (KOYO L5)" name="twitter:title"/>
<meta content="Find SAFFIRE EV (KOYO Auto / KOYO L5) by KOYO Gears India across 100 Indian cities." name="twitter:description"/>
<meta content="https://saffireev.com/images/herobanner.png" name="twitter:image"/>
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://saffireev.com/#organization",
  "name": "SAFFIRE EV",
  "legalName": "KOYO GEARS INDIA PRIVATE LIMITED",
  "alternateName": ["KOYO", "KOYO Auto", "KOYO Electric Auto", "KOYO L5", "KOYO Electric Rickshaw", "KOYO Gears India", "KOYO Gears India Private Limited", "Saffire EV by Koyo Gears India"],
  "url": "https://saffireev.com",
  "logo": "https://saffireev.com/images/logo_final.png"
}}</script>
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "SAFFIRE EV (KOYO Gears India)", "item": "https://saffireev.com/"}},
    {{"@type": "ListItem", "position": 2, "name": "KOYO Auto Locations", "item": "https://saffireev.com/locations/"}}
  ]
}}</script>
<script>{TAILWIND_CFG}</script>
<style>{SHARED_CSS}</style>
</head>
<body class="selection:bg-primary selection:text-on-primary scroll-smooth flex flex-col min-h-screen">

{NAVBAR}

<main class="flex-grow pt-28 pb-24 px-6 md:px-8 max-w-screen-xl mx-auto w-full">

  <!-- Hero -->
  <section class="mb-14 text-center md:text-left">
    <span class="inline-block text-primary font-label text-[10px] font-bold tracking-widest uppercase mb-3">India-Wide Coverage · KOYO Gears India · KOYO L5</span>
    <h1 class="font-headline font-bold text-4xl md:text-6xl tracking-tighter mb-4 text-[#E5E1E4]">
      KOYO Electric Auto &amp; SAFFIRE EV Locations Across India
    </h1>
    <p class="text-on-surface-variant text-base md:text-lg font-light leading-relaxed max-w-3xl mb-6">
      <a href="/about/" class="text-primary hover:underline font-medium">KOYO GEARS INDIA PRIVATE LIMITED (KOYO Gears India)</a> — the manufacturer behind the <a href="/" class="text-primary hover:underline font-medium">SAFFIRE EV</a> brand (widely known as <strong>KOYO</strong>, <strong>KOYO Auto</strong>, and <a href="/l5-electric-vehicle/" class="text-primary hover:underline">KOYO L5</a>) — builds heavy-duty
      L5 <a href="/electric-passenger-auto/" class="text-primary hover:underline">electric passenger autos</a> (<a href="/products/saffire-smart-ride/" class="text-primary hover:underline">SAFFIRE Smart Ride</a>) and <a href="/electric-cargo-loader/" class="text-primary hover:underline">electric cargo loaders</a> (<a href="/products/saffire-swiss-cargo/" class="text-primary hover:underline">SAFFIRE Swiss Cargo</a>) for operators,
      fleet buyers, and dealers across India. Find city-specific KOYO Auto &amp; SAFFIRE EV information across {len(cities)} target Indian cities ({total_indexable} live pages) below.
    </p>
    <div class="flex flex-col sm:flex-row gap-4">
      <a class="kinetic-gradient text-on-primary font-headline font-bold py-4 px-8 rounded-sm tracking-widest uppercase text-sm hover:brightness-110 transition-all text-center"
         href="https://wa.me/919258172967?text=Hello%20Saffire%20EV%2C%20I%20want%20to%20know%20about%20your%20vehicles%20in%20my%20city." rel="noopener noreferrer" target="_blank">
        WhatsApp Enquiry
      </a>
      <a class="border border-outline-variant/30 text-on-surface font-headline font-bold py-4 px-8 rounded-sm tracking-widest uppercase text-sm hover:bg-surface-container-highest transition-all text-center"
         href="/contact/">Contact Saffire EV</a>
    </div>
  </section>

  <!-- Search + Filter -->
  <section class="mb-10">
    <div class="flex flex-col md:flex-row gap-4">
      <div class="relative flex-grow">
        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[18px]">search</span>
        <input class="w-full bg-surface-container-low border border-outline-variant/30 rounded-lg pl-10 pr-4 py-3 text-sm text-on-surface placeholder-on-surface-variant/50 focus:outline-none focus:border-primary/50 transition-colors"
               id="city-search" placeholder="Search city name..." type="text"/>
      </div>
      <select class="bg-surface-container-low border border-outline-variant/30 rounded-lg px-4 py-3 text-sm text-on-surface focus:outline-none focus:border-primary/50 transition-colors" id="state-filter">
        <option value="">All States</option>
        {"".join(f'<option value="{s.lower().replace(" ","-")}">{s}</option>' for s in state_order if s in states)}
      </select>
    </div>
  </section>

  <!-- Products Quick Reference -->
  <section class="mb-14">
    <h2 class="sr-only">KOYO L5 Electric Three-Wheeler Lineup</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div class="bg-surface-container-low rounded-xl border border-outline-variant/10 p-6 flex gap-4 items-start">
      <div class="w-12 h-12 shrink-0 rounded-lg bg-primary/10 flex items-center justify-center">
        <span class="material-symbols-outlined text-primary">electric_rickshaw</span>
      </div>
      <div>
        <span class="text-primary font-label text-[10px] font-bold tracking-widest uppercase">D+3 Passenger</span>
        <h3 class="font-headline font-bold text-lg mb-1 text-[#E5E1E4]">SAFFIRE Smart Ride</h3>
        <p class="text-on-surface-variant text-sm font-light">Electric passenger auto · 200 km range · 6.3 kW motor · 50 km/h top speed</p>
        <a class="text-primary font-label text-[11px] font-bold uppercase tracking-widest hover:underline flex items-center gap-1 mt-3 w-fit" href="/products/saffire-smart-ride/">
          Full Specs <span class="material-symbols-outlined text-[14px]">arrow_forward</span>
        </a>
      </div>
    </div>
    <div class="bg-surface-container-low rounded-xl border border-outline-variant/10 p-6 flex gap-4 items-start">
      <div class="w-12 h-12 shrink-0 rounded-lg bg-primary/10 flex items-center justify-center">
        <span class="material-symbols-outlined text-primary">local_shipping</span>
      </div>
      <div>
        <span class="text-primary font-label text-[10px] font-bold tracking-widest uppercase">Electric Cargo Loader</span>
        <h3 class="font-headline font-bold text-lg mb-1 text-[#E5E1E4]">SAFFIRE Swiss Cargo</h3>
        <p class="text-on-surface-variant text-sm font-light">Electric cargo loader · 600 kg payload · 200 km range · 6.3 kW motor</p>
        <a class="text-primary font-label text-[11px] font-bold uppercase tracking-widest hover:underline flex items-center gap-1 mt-3 w-fit" href="/products/saffire-swiss-cargo/">
          Full Specs <span class="material-symbols-outlined text-[14px]">arrow_forward</span>
        </a>
      </div>
    </div>
    </div>
  </section>

  <!-- City Directory -->
  <section id="city-directory">
    <h2 class="font-headline text-2xl font-bold mb-8 text-[#E5E1E4]">Cities by State</h2>
    <div id="directory-content">
      {state_sections}
    </div>
    <p class="text-on-surface-variant text-xs mt-4 italic" id="no-results" style="display:none">No cities found matching your search.</p>
  </section>

  <!-- Dealer CTA -->
  <section class="mt-16 bg-primary/5 border border-primary/20 rounded-2xl p-8 md:p-12 text-center">
    <h2 class="font-headline text-2xl md:text-3xl font-bold mb-4 text-[#E5E1E4]">Scale Your Enterprise With SAFFIRE EV</h2>
    <p class="text-on-surface-variant text-base font-light mb-8 max-w-2xl mx-auto">
      KOYO GEARS INDIA PRIVATE LIMITED is expanding its national footprint.
      Partner as a dealer or distributor in your city to supply SAFFIRE EV L5 electric three-wheelers.
    </p>
    <div class="flex flex-col sm:flex-row gap-4 justify-center">
      <a class="kinetic-gradient text-on-primary font-headline font-bold py-4 px-10 rounded-sm tracking-widest uppercase text-sm hover:brightness-110 transition-all"
         href="/contact/?type=dealer">Become a Dealer</a>
      <a class="border border-outline-variant/40 text-on-surface font-headline font-bold py-4 px-10 rounded-sm tracking-widest uppercase text-sm hover:bg-surface-container-highest transition-all"
         href="/ev-dealership-india/">Dealer Opportunities</a>
    </div>
  </section>

</main>

{FOOTER}

<script>
const searchInput = document.getElementById('city-search');
const stateFilter = document.getElementById('state-filter');
const noResults = document.getElementById('no-results');

function filterCities() {{
  const q = searchInput.value.toLowerCase().trim();
  const st = stateFilter.value;
  let found = false;
  document.querySelectorAll('[data-state]').forEach(section => {{
    const stateMatch = !st || section.dataset.state === st;
    const cards = section.querySelectorAll('a[href], div.cursor-default');
    let visibleCount = 0;
    cards.forEach(card => {{
      const text = card.textContent.toLowerCase();
      const show = stateMatch && (!q || text.includes(q));
      card.style.display = show ? '' : 'none';
      if (show) visibleCount++;
    }});
    section.style.display = (stateMatch && visibleCount > 0) ? '' : 'none';
    if (stateMatch && visibleCount > 0) found = true;
  }});
  noResults.style.display = found ? 'none' : 'block';
}}

searchInput.addEventListener('input', filterCities);
stateFilter.addEventListener('change', filterCities);

// Support SearchAction URL parameters (?city=...&state=...)
(function initFromQuery() {{
  const params = new URLSearchParams(window.location.search);
  const qCity = params.get('city') || params.get('q') || '';
  const qState = params.get('state') || '';
  if (qCity) searchInput.value = qCity;
  if (qState) stateFilter.value = qState.toLowerCase();
  if (qCity || qState) filterCities();
}})();
</script>

</body>
</html>"""
    return html


# ── SITEMAP UPDATE ─────────────────────────────────────────────────────────
def update_sitemap(cities):
    # Read existing sitemap (non-location entries)
    try:
        with open(SITEMAP_FILE, 'r', encoding='utf-8') as f:
            existing = f.read()
    except FileNotFoundError:
        existing = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>'

    # Strip old location entries if any
    existing = re.sub(r'\s*<url>\s*<loc>https://saffireev\.com/locations/[^<]*</loc>.*?</url>', '', existing, flags=re.DOTALL)

    location_entries = f"""
  <url>
    <loc>https://saffireev.com/locations/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>"""

    for city in cities:
        if city.get("index"):
            location_entries += f"""
  <url>
    <loc>https://saffireev.com/locations/{city['slug']}/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.65</priority>
  </url>"""

    # Insert before closing tag
    new_sitemap = existing.replace('</urlset>', location_entries + '\n</urlset>')

    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(new_sitemap)
    print(f"  Updated sitemap.xml with locations directory + {sum(1 for c in cities if c.get('index'))} city URLs")


# ── MAIN ───────────────────────────────────────────────────────────────────
def main():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    cities = data["cities"]

    all_cities_by_slug = {c["slug"]: c for c in cities}

    # Create /locations/
    os.makedirs(LOCATIONS_DIR, exist_ok=True)
    dir_html = generate_directory_page(cities)
    with open(os.path.join(LOCATIONS_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(dir_html)
    print(f"Generated /locations/index.html")

    # Create individual city pages
    indexable = 0
    draft = 0
    for city in cities:
        city_dir = os.path.join(LOCATIONS_DIR, city["slug"])
        os.makedirs(city_dir, exist_ok=True)
        html = generate_city_page(city, all_cities_by_slug)
        with open(os.path.join(city_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html)
        status = "INDEX" if city.get("index") else "NOINDEX(draft)"
        print(f"  Generated /locations/{city['slug']}/ [{status}]")
        if city.get("index"):
            indexable += 1
        else:
            draft += 1

    update_sitemap(cities)

    print(f"\nDone. {indexable} indexable city pages, {draft} draft/noindex pages.")
    print(f"Total cities: {len(cities)}")


if __name__ == "__main__":
    main()
