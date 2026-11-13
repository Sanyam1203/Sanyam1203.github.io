"""
Saffire EV - HTML Post-Processor & Sanitizer
Cleanses compiled HTML to prevent search snippet leakage, optimizes image SEO,
and verifies canonical URLs and OpenGraph tags.
"""
from __future__ import annotations

import os
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup


def sanitize_html_content(html_str: str, file_path: str = "") -> Dict[str, Any]:
    """
    Sanitizes HTML content:
    1. Adds aria-hidden="true" and data-nosnippet to all icon spans (.material-symbols-outlined).
    2. Enforces alt tags on all <img> elements.
    3. Adds loading="lazy" to non-hero images.
    4. Checks canonical and og tags (skipping partial templates and redirect stubs).
    """
    soup = BeautifulSoup(html_str, "html.parser")
    stats = {
        "icons_sanitized": 0,
        "images_alt_fixed": 0,
        "images_lazy_fixed": 0,
        "canonical_present": False,
        "og_title_present": False,
        "og_desc_present": False,
        "jsonld_count": 0,
        "warnings": []
    }

    # 1. Sanitize Material Symbols icons
    for span in soup.find_all("span", class_=lambda c: c and "material-symbols-outlined" in c):
        span["aria-hidden"] = "true"
        span["data-nosnippet"] = ""
        stats["icons_sanitized"] += 1

    # Also catch any <i> or <span> with material icon classes
    for el in soup.find_all(["i", "span"], class_=lambda c: c and ("material-icons" in c or "material-symbols" in c)):
        el["aria-hidden"] = "true"
        el["data-nosnippet"] = ""

    # 2. Images audit & optimization
    for idx, img in enumerate(soup.find_all("img")):
        src = img.get("src", "")
        alt = img.get("alt", "").strip()

        # Fix missing or generic alt attributes
        if not alt:
            inferred_alt = "Saffire EV Commercial Electric Three Wheeler by Koyo Gears India"
            if "logo" in src.lower():
                inferred_alt = "Saffire EV by Koyo Gears India Pvt. Ltd. Logo"
            elif "smart" in src.lower() or "passenger" in src.lower():
                inferred_alt = "Saffire Smart Ride L5 Electric Passenger Auto Rickshaw"
            elif "cargo" in src.lower() or "loader" in src.lower() or "swiss" in src.lower():
                inferred_alt = "Saffire Swiss Cargo L5 Commercial Electric Loader"
            img["alt"] = inferred_alt
            stats["images_alt_fixed"] += 1

        # Add loading="lazy" for below-the-fold images (skip first 2 images or hero)
        is_hero = "hero" in src.lower() or "banner" in src.lower() or "logo" in src.lower() or idx == 0
        if not is_hero and not img.get("loading"):
            img["loading"] = "lazy"
            stats["images_lazy_fixed"] += 1

    # Skip document-level metadata checks for component partials, 404, or redirect stubs
    is_partial = "templates" in file_path or not soup.find("html")
    is_redirect_stub = bool(soup.find("meta", attrs={"http-equiv": lambda h: h and h.lower() == "refresh"}))
    is_404 = "404" in file_path

    if not is_partial and not is_redirect_stub and not is_404:
        # 3. Canonical check
        canonical = soup.find("link", rel=lambda r: r and "canonical" in r)
        if canonical and canonical.get("href"):
            stats["canonical_present"] = True
        else:
            stats["warnings"].append(f"Missing canonical link in {file_path}")

        # 4. OpenGraph check
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            stats["og_title_present"] = True
        else:
            stats["warnings"].append(f"Missing og:title in {file_path}")

        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            stats["og_desc_present"] = True

        # 5. JSON-LD check
        json_lds = soup.find_all("script", type="application/ld+json")
        stats["jsonld_count"] = len(json_lds)
        if stats["jsonld_count"] == 0:
            stats["warnings"].append(f"Missing JSON-LD script in {file_path}")

    # Convert back to clean HTML string
    cleaned_html = str(soup)
    stats["cleaned_html"] = cleaned_html
    return stats


def process_html_file(file_path: str) -> Dict[str, Any]:
    """Reads, sanitizes, and overwrites an HTML file in place."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    result = sanitize_html_content(content, file_path)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(result["cleaned_html"])

    del result["cleaned_html"]
    return result


def sanitize_all_html_files(root_dir: str = ".") -> Dict[str, Any]:
    """Recursively traverses all HTML files and applies sanitization."""
    overall = {
        "files_processed": 0,
        "total_icons_sanitized": 0,
        "total_images_alt_fixed": 0,
        "total_images_lazy_fixed": 0,
        "warnings": []
    }

    exclude_dirs = {".git", ".venv", "venv", "__pycache__", "stitch_saffire_ev_pre_launch", "stitch_saffire_ev_pre_launch 2"}

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            if f.endswith(".html"):
                full_path = os.path.join(root, f)
                res = process_html_file(full_path)
                overall["files_processed"] += 1
                overall["total_icons_sanitized"] += res["icons_sanitized"]
                overall["total_images_alt_fixed"] += res["images_alt_fixed"]
                overall["total_images_lazy_fixed"] += res["images_lazy_fixed"]
                if res["warnings"]:
                    overall["warnings"].extend(res["warnings"])

    return overall
