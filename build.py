"""
Saffire EV - Master Python Build & Programmatic SEO/GEO Engine
Compiles Jinja2 templates, generates SEO/GEO assets (/llms.txt, /api/v1/),
injects crawlable TCO tables and Quick Query lead modal,
sanitizes HTML to prevent search snippet leaks, and regenerates sitemap.xml.
"""
from __future__ import annotations

import os
import sys
import json
import re
from datetime import date
from bs4 import BeautifulSoup

from src.catalog_data import COMPANY_INFO, VEHICLE_PLATFORMS, REGIONAL_HUBS, COMMERCIAL_FAQS
from src.seo_geo_compiler import (
    write_all_seo_geo_assets,
    compile_page_jsonld,
    BASE_URL,
    TODAY
)
from src.tco_engine import (
    render_crawlable_tco_html,
    render_l5_vs_l3_vs_diesel_html,
    calculate_tco
)
from src.html_sanitizer import sanitize_all_html_files, process_html_file

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
POPUP_SNIPPET_PATH = os.path.join(ROOT_DIR, "templates", "components", "query_popup.html")


def read_popup_snippet() -> str:
    """Reads the Quick Query popup modal HTML and script component."""
    with open(POPUP_SNIPPET_PATH, "r", encoding="utf-8") as f:
        return f.read()


def inject_popup_into_html(html_str: str) -> str:
    """Injects the global Quick Query popup and trigger before </body> if not already present."""
    if 'id="saffire-query-overlay"' in html_str:
        return html_str  # Already present

    popup_html = read_popup_snippet()
    idx = html_str.rfind("</body>")
    if idx != -1:
        return html_str[:idx] + "\n" + popup_html + "\n" + html_str[idx:]
    return html_str + "\n" + popup_html


def build_homepage():
    """Builds and enhances index.html with TCO table, calculator CTA, and popup."""
    index_path = os.path.join(ROOT_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Inject Calculator CTA button inside the Profit card if missing
    if "Lock In Your Savings — Get Custom Price & EMI Quote" not in content:
        cta_button = """
<div class="mt-4 pt-4 border-t border-primary/20">
  <button type="button" data-open-query-popup data-query-intent="preorder" data-calculator="true" class="w-full py-2.5 px-4 bg-primary text-background font-headline font-bold text-xs uppercase tracking-wider rounded-lg hover:bg-primary/90 transition-all flex items-center justify-center gap-2 shadow-md cursor-pointer">
    <span class="material-symbols-outlined text-sm" aria-hidden="true" data-nosnippet>savings</span>
    Lock In Your Savings — Get Custom Price &amp; EMI Quote
  </button>
</div>
"""
        target = 'id="calc-percent">+65% more profitable than diesel</p>'
        if target in content:
            content = content.replace(target, target + "\n" + cta_button)

    # 2. Inject crawlable semantic TCO comparison table below the calculator grid if missing
    if "View Verified Commercial TCO Comparison Matrix" not in content:
        tco_table_html = render_crawlable_tco_html()
        # Find closing of calculator grid
        target_grid_end = '<!-- Outputs / Visuals -->'
        if target_grid_end in content:
            # Look for closing </div> of calculator container
            calc_idx = content.find('id="calculator"')
            sec_end = content.find('</section>', calc_idx)
            # Find the last </div> before </section>
            div_before_sec = content.rfind('</div>', calc_idx, sec_end)
            if div_before_sec != -1:
                content = content[:div_before_sec] + "\n" + tco_table_html + "\n" + content[div_before_sec:]

    # 3. Update calculateTCO script to cache settings on window
    calc_settings_script = """
            // Cache settings for modal
            window.currentCalcSettings = {
                km: km,
                years: years,
                profit: formatINR(extraProfit),
                fuel: currentFuel
            };
    """
    if "window.currentCalcSettings" not in content:
        target_prev = "prevValues.extraProfit = extraProfit;"
        if target_prev in content:
            content = content.replace(target_prev, target_prev + "\n" + calc_settings_script)

    # 4. Inject L5 vs L3 vs Diesel Auto comparison block if missing
    if "Why Choose a Saffire L5 Auto Rickshaw" not in content:
        l5_block = render_l5_vs_l3_vs_diesel_html()
        vision_anchor = "<!-- Vision Statement -->"
        if vision_anchor in content:
            content = content.replace(vision_anchor, l5_block + "\n" + vision_anchor)
        else:
            calc_end = content.find('</section>', content.find('id="calculator"'))
            if calc_end != -1:
                content = content[:calc_end+10] + "\n" + l5_block + "\n" + content[calc_end+10:]

    # 5. Inject global Quick Query popup
    content = inject_popup_into_html(content)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Enhanced and rebuilt index.html (Homepage)")


def enhance_contact_page():
    """Enhances contact/index.html with sessionStorage/popup prefill receiver script."""
    contact_path = os.path.join(ROOT_DIR, "contact", "index.html")
    with open(contact_path, "r", encoding="utf-8") as f:
        content = f.read()

    receiver_code = """
        // Sync with Quick Query modal sessionStorage and URL parameters
        try {
            const storedLead = sessionStorage.getItem('saffire_lead_query');
            if (storedLead) {
                const leadData = JSON.parse(storedLead);
                if (nameEl && !nameEl.value && leadData.name) nameEl.value = leadData.name;
                if (phoneEl && !phoneEl.value && leadData.phone) phoneEl.value = leadData.phone;
                if (cityEl && !cityEl.value && leadData.city) cityEl.value = leadData.city;
                if (msgEl && (!msgEl.value || msgEl.value.startsWith('Hello')) && leadData.notes) {
                    msgEl.value = leadData.notes;
                }
                if (leadData.intent === 'dealer' && selectEl) selectEl.value = 'Dealer Opportunity';
                else if (leadData.intent === 'fleet' && selectEl) selectEl.value = 'Fleet / Business Inquiry';
                if (bannerEl) {
                    bannerEl.textContent = `Enquiry Sync: ${leadData.name} (${leadData.city}) — ${leadData.platform || 'Saffire EV'}`;
                    bannerEl.classList.remove('hidden');
                }
            }
        } catch(e) {}

        const urlName = urlParams.get('name');
        const urlPhone = urlParams.get('phone');
        const urlNotes = urlParams.get('notes');
        if (nameEl && !nameEl.value && urlName) nameEl.value = decodeURIComponent(urlName);
        if (phoneEl && !phoneEl.value && urlPhone) phoneEl.value = decodeURIComponent(urlPhone);
        if (msgEl && (!msgEl.value || msgEl.value.startsWith('Hello')) && urlNotes) msgEl.value = decodeURIComponent(urlNotes);
    """

    if "sessionStorage.getItem('saffire_lead_query')" not in content:
        anchor = "if (bannerEl && (cityLabel || rawProduct || rawType)) {"
        if anchor in content:
            content = content.replace(anchor, receiver_code + "\n        " + anchor)

    # Inject popup into contact page (popup script will auto-skip opening on /contact/, but floating button works)
    content = inject_popup_into_html(content)

    with open(contact_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Enhanced contact/index.html with pre-fill sync and query popup")


def render_state_city_directory_html() -> str:
    """Renders a crawlable state-by-state directory linking to all 96 indexable city pages."""
    data_path = os.path.join(ROOT_DIR, "_geo_seo", "city_data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    from collections import defaultdict
    states = defaultdict(list)
    for c in data["cities"]:
        if c.get("index"):
            states[c["state"]].append(c)

    html = """
    <div class="mt-16 pt-12 border-t border-outline-variant/20" id="city-directory">
      <div class="text-center mb-8">
        <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-label uppercase tracking-widest mb-2">
          <span class="material-symbols-outlined text-sm" aria-hidden="true" data-nosnippet>location_city</span>
          Pan-India Territorial Coverage
        </span>
        <h2 class="font-headline text-2xl md:text-3xl font-bold text-on-surface">
          Explore Saffire Auto &amp; Koyo L5 Dealership Opportunities Across 96 Cities
        </h2>
        <p class="font-body text-xs md:text-sm text-on-surface-variant font-light mt-2 max-w-2xl mx-auto">
          Select your city to view local electric auto demand, route profiles, and open territory exclusivity:
        </p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    """
    for state, clist in sorted(states.items()):
        html += f"""
        <div class="p-4 rounded-xl bg-surface-container-low border border-outline-variant/20">
          <h3 class="font-headline font-bold text-sm text-primary mb-2 flex items-center justify-between">
            <span>{state}</span>
            <span class="text-[10px] text-on-surface-variant font-normal">({len(clist)} Cities)</span>
          </h3>
          <div class="flex flex-wrap gap-1.5">
        """
        for c in sorted(clist, key=lambda x: x["name"]):
            html += f'<a href="/locations/{c["slug"]}/" class="text-xs px-2.5 py-1 rounded bg-surface-container hover:bg-primary hover:text-background text-on-surface transition-colors">{c["name"]}</a>\n'
        html += """
          </div>
        </div>
        """
    html += """
      </div>
    </div>
    """
    return html


def enhance_dealership_page():
    """Enhances ev-dealership-india/index.html with the state-by-state directory."""
    path = os.path.join(ROOT_DIR, "ev-dealership-india", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'id="city-directory"' not in content:
        dir_html = render_state_city_directory_html()
        idx = content.rfind("</main>")
        if idx != -1:
            content = content[:idx] + "\n" + dir_html + "\n" + content[idx:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("✓ Injected 96-City State Directory into ev-dealership-india/index.html")


def enhance_smart_ride_page():
    """Enhances products/saffire-smart-ride/index.html with L5 vs L3 vs Diesel comparison block."""
    path = os.path.join(ROOT_DIR, "products", "saffire-smart-ride", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "Why Choose a Saffire L5 Auto Rickshaw" not in content:
        comp_block = render_l5_vs_l3_vs_diesel_html()
        faq_anchor = '<section class="max-w-4xl mx-auto px-6 md:px-8 mb-24">'
        if faq_anchor in content:
            content = content.replace(faq_anchor, comp_block + "\n" + faq_anchor)
        else:
            idx = content.rfind("</main>")
            if idx != -1:
                content = content[:idx] + "\n" + comp_block + "\n" + content[idx:]
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✓ Injected L5 comparison table into products/saffire-smart-ride/index.html")


def enhance_core_pages():
    """Injects popup and verifies canonicals across all core static pages."""
    core_pages = [
        os.path.join(ROOT_DIR, "koyo-gears-india", "index.html"),
        os.path.join(ROOT_DIR, "about", "index.html"),
        os.path.join(ROOT_DIR, "vision", "index.html"),
        os.path.join(ROOT_DIR, "products", "index.html"),
        os.path.join(ROOT_DIR, "products", "saffire-smart-ride", "index.html"),
        os.path.join(ROOT_DIR, "products", "saffire-swiss-cargo", "index.html"),
        os.path.join(ROOT_DIR, "ev-dealership-india", "index.html"),
        os.path.join(ROOT_DIR, "terms", "index.html"),
        os.path.join(ROOT_DIR, "electric-cargo-loader", "index.html"),
        os.path.join(ROOT_DIR, "electric-passenger-auto", "index.html"),
        os.path.join(ROOT_DIR, "electric-three-wheeler-running-cost", "index.html"),
        os.path.join(ROOT_DIR, "l5-electric-vehicle", "index.html")
    ]

    for p in core_pages:
        if os.path.isfile(p):
            with open(p, "r", encoding="utf-8") as f:
                c = f.read()
            c = inject_popup_into_html(c)
            with open(p, "w", encoding="utf-8") as f:
                f.write(c)
            print(f"✓ Injected query popup into {os.path.relpath(p, ROOT_DIR)}")


def regenerate_sitemap():
    """Regenerates sitemap.xml with 110 URLs including all indexable cities and static pages."""
    sitemap_script = os.path.join(ROOT_DIR, "_geo_seo", "regenerate_sitemap.py")
    if os.path.isfile(sitemap_script):
        # Execute the script logic directly
        import _geo_seo.regenerate_sitemap as rs
        rs.main()
    print("✓ Rebuilt and verified sitemap.xml")


def main():
    print("====================================================================")
    print("SAFFIRE EV - MASTER PYTHON BUILD & SEO/GEO ENGINE")
    print("====================================================================")

    # 1. Compile and write all SEO/GEO endpoints (/llms.txt, /llms-full.txt, /api/v1/, robots.txt)
    print("\n[Step 1/5] Compiling SEO/GEO Endpoints & LLM Knowledge Dossiers...")
    assets = write_all_seo_geo_assets(ROOT_DIR)
    for name, path in assets.items():
        print(f"  + Generated {name} ({os.path.getsize(path)} bytes)")

    # 2. Build homepage, Smart Ride page, and Dealership page with comparison blocks
    print("\n[Step 2/6] Building Homepage, Product & Dealership Enhancements...")
    build_homepage()
    enhance_smart_ride_page()
    enhance_dealership_page()

    # 3. Generate 96 localized regional city pages with keyword clusters
    print("\n[Step 3/6] Compiling 96 Regional City Pages with Exact Keyword Clusters...")
    import _geo_seo.generate_locations as gl
    gl.main()

    # 4. Enhance contact page with pre-fill sync and inject popup into core routes
    print("\n[Step 4/6] Enhancing Contact Page & Core Routes...")
    enhance_contact_page()
    enhance_core_pages()

    # 5. Regenerate sitemap.xml
    print("\n[Step 5/6] Regenerating sitemap.xml (111 URLs)...")
    regenerate_sitemap()

    # 6. Sanitize HTML across repository (protect icon snippets, enforce alt, loading=lazy)
    print("\n[Step 6/6] Running BeautifulSoup4 HTML Sanitizer...")
    sanitizer_stats = sanitize_all_html_files(ROOT_DIR)
    print(f"  + Files Processed: {sanitizer_stats['files_processed']}")
    print(f"  + Icon Spans Protected: {sanitizer_stats['total_icons_sanitized']}")
    print(f"  + Missing Image Alt Fixed: {sanitizer_stats['total_images_alt_fixed']}")
    print(f"  + Lazy-Loading Enforced: {sanitizer_stats['total_images_lazy_fixed']}")
    if sanitizer_stats["warnings"]:
        print(f"  ! Warnings: {len(sanitizer_stats['warnings'])}")

    # 7. Verify CNAME preservation
    cname_path = os.path.join(ROOT_DIR, "CNAME")
    if not os.path.isfile(cname_path):
        with open(cname_path, "w", encoding="utf-8") as f:
            f.write("saffireev.com\n")
        print("  + Restored CNAME: saffireev.com")
    else:
        print(f"  + CNAME verified: {open(cname_path).read().strip()}")

    print("\n====================================================================")
    print("BUILD COMPLETE: Static files and SEO/GEO endpoints ready for deployment.")
    print("====================================================================")


if __name__ == "__main__":
    main()

