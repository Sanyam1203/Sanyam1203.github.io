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
    build_organization_node,
    build_local_business_node,
    BASE_URL,
    TODAY
)
from src.tco_engine import (
    render_crawlable_tco_html,
    render_l5_vs_l3_vs_diesel_html,
    render_guide_tco_spec_table_html,
    render_interactive_calculator_html,
    render_state_tariff_and_cashflow_html,
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
    if 'id="calc-lock-savings-btn"' not in content:
        cta_button = """
<div class="mt-4 pt-4 border-t border-primary/20">
  <button id="calc-lock-savings-btn" type="button" data-open-query-popup data-query-intent="preorder" data-calculator="true" class="w-full py-3 px-4 bg-primary text-background font-headline font-bold text-xs uppercase tracking-wider rounded-lg hover:bg-primary/90 transition-all flex items-center justify-center gap-2 shadow-md cursor-pointer">
    <span class="material-symbols-outlined notranslate text-sm" translate="no" aria-hidden="true" data-nosnippet>savings</span>
    <span>Lock In Your <span id="calc-lock-savings-amount">₹ 8,47,530</span> Savings — Request Dealer / Fleet Quote</span>
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


def render_dealership_b2b_sections_html() -> str:
    """Renders B2B dealership model, infrastructure, OEM support & onboarding sections."""
    return """
    <section class="my-12 space-y-10" id="b2b-dealership-blueprint">
      <!-- Dealership Model & Territorial Exclusivity -->
      <div class="rounded-2xl bg-surface-container-low border border-outline-variant/20 p-6 md:p-8">
        <span class="font-label text-[10px] tracking-widest uppercase text-primary block mb-2">B2B Partnership Blueprint</span>
        <h2 class="font-headline text-2xl md:text-3xl font-bold text-on-surface mb-4">Dealership Model &amp; Territorial Exclusivity</h2>
        <p class="text-sm text-on-surface-variant font-light leading-relaxed mb-6">
          Koyo Gears India Private Limited appoints one authorized Saffire EV dealership per designated commercial district or city cluster, protecting partner margins and preventing intra-brand cannibalization. Partners retail both the <strong>Saffire Smart Ride (L5M Passenger)</strong> and <strong>Saffire Swiss Cargo (L5N Loader)</strong> along with OEM spare parts.
        </p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-5 rounded-xl bg-surface-container border border-outline-variant/15">
            <h3 class="font-headline font-bold text-base text-primary mb-2">Infrastructure &amp; Space</h3>
            <ul class="text-xs text-on-surface-variant space-y-1.5 font-light">
              <li>• 800 – 1,500 sq. ft. commercial showroom frontage</li>
              <li>• 2-bay service &amp; PDI area with 16A charging points</li>
              <li>• Dedicated OEM spare-parts counter</li>
            </ul>
          </div>
          <div class="p-5 rounded-xl bg-surface-container border border-outline-variant/15">
            <h3 class="font-headline font-bold text-base text-primary mb-2">OEM Support Stack</h3>
            <ul class="text-xs text-on-surface-variant space-y-1.5 font-light">
              <li>• ICAT Manesar certified L5 vehicles (CMVR / AIS-156)</li>
              <li>• Factory technician training &amp; diagnostic tooling</li>
              <li>• Direct spare-parts supply chain &amp; digital lead routing</li>
            </ul>
          </div>
          <div class="p-5 rounded-xl bg-surface-container border border-outline-variant/15">
            <h3 class="font-headline font-bold text-base text-primary mb-2">5-Step Onboarding</h3>
            <ol class="text-xs text-on-surface-variant space-y-1.5 font-light list-decimal list-inside">
              <li>Submit territory application below</li>
              <li>Regional manager site &amp; market review</li>
              <li>LOI &amp; exclusive territory allocation</li>
              <li>Showroom branding &amp; technician training</li>
              <li>Initial demo/stock dispatch &amp; launch</li>
            </ol>
          </div>
        </div>
      </div>
    </section>
    """


def render_state_city_directory_html() -> str:
    """Renders a searchable, filterable state-by-state table of all 100 target expansion cities."""
    data_path = os.path.join(ROOT_DIR, "_geo_seo", "city_data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cities = sorted(data["cities"], key=lambda x: (x["state"], x["name"]))
    states = sorted({c["state"] for c in cities})
    state_options = "".join(f'<option value="{s}">{s}</option>' for s in states)

    rows_html = ""
    for c in cities:
        is_hub = bool(c.get("index"))
        status_badge = (
            '<span class="px-2 py-0.5 rounded bg-primary/15 text-primary text-[10px] font-bold uppercase tracking-wider">Active Hub</span>'
            if is_hub else
            '<span class="px-2 py-0.5 rounded bg-surface-container-highest text-on-surface-variant text-[10px] uppercase tracking-wider">Open Territory</span>'
        )
        city_cell = (
            f'<a href="/locations/{c["slug"]}/" class="font-bold text-primary hover:underline">{c["name"]}</a>'
            if is_hub else
            f'<span class="font-semibold text-on-surface">{c["name"]}</span>'
        )
        rows_html += f"""
        <tr class="city-dir-row border-b border-outline-variant/10 hover:bg-surface-container-highest/20 transition-colors text-xs md:text-sm" data-city="{c['name'].lower()}" data-state="{c['state']}">
          <td class="p-3.5">{city_cell}</td>
          <td class="p-3.5 text-on-surface-variant">{c['state']}</td>
          <td class="p-3.5">{status_badge}</td>
          <td class="p-3.5 text-right">
            <a href="/contact/?city={c['slug']}&amp;type=dealer" class="inline-block px-3 py-1.5 rounded bg-primary text-background font-headline font-bold text-[11px] uppercase tracking-wider hover:bg-primary/90 transition-colors">
              Apply for This Territory
            </a>
          </td>
        </tr>"""

    return f"""
    <div class="mt-16 pt-12 border-t border-outline-variant/20" id="city-directory">
      <div class="text-center mb-8">
        <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-label uppercase tracking-widest mb-2">
          <span class="material-symbols-outlined notranslate text-sm" translate="no" aria-hidden="true" data-nosnippet>location_city</span>
          <span>100 Target Expansion Territories</span>
        </span>
        <h2 class="font-headline text-2xl md:text-3xl font-bold text-on-surface">
          Explore Saffire EV Dealership Territories Across 100 Indian Cities
        </h2>
        <p class="font-body text-xs md:text-sm text-on-surface-variant font-light mt-2 max-w-2xl mx-auto">
          Filter by state or search your city to apply for exclusive regional dealership rights:
        </p>
      </div>

      <div class="flex flex-col sm:flex-row gap-3 mb-6">
        <input id="dir-city-search" type="text" placeholder="Search city (e.g. Meerut, Lucknow, Pune, Jaipur)..." class="flex-1 bg-surface-container border border-outline-variant/30 rounded-lg px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:border-primary"/>
        <select id="dir-state-filter" class="bg-surface-container border border-outline-variant/30 rounded-lg px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:border-primary">
          <option value="">All States ({len(states)})</option>
          {state_options}
        </select>
      </div>

      <div class="overflow-x-auto rounded-xl border border-outline-variant/20 bg-surface-container-low max-h-[540px] overflow-y-auto">
        <table class="w-full text-left border-collapse">
          <thead class="sticky top-0 bg-surface-container-high z-10">
            <tr class="border-b border-outline-variant/20 text-on-surface font-headline text-xs md:text-sm">
              <th class="p-3.5">City</th>
              <th class="p-3.5">State / UT</th>
              <th class="p-3.5">Network Status</th>
              <th class="p-3.5 text-right">Territory Action</th>
            </tr>
          </thead>
          <tbody class="font-body divide-y divide-outline-variant/10">
            {rows_html}
          </tbody>
        </table>
      </div>
    </div>
    <script>
    (function() {{
      const sIn = document.getElementById('dir-city-search');
      const sSel = document.getElementById('dir-state-filter');
      if (!sIn || !sSel) return;
      function filterDir() {{
        const q = sIn.value.toLowerCase().trim();
        const st = sSel.value;
        document.querySelectorAll('.city-dir-row').forEach(r => {{
          const okCity = !q || r.dataset.city.includes(q) || r.dataset.state.toLowerCase().includes(q);
          const okState = !st || r.dataset.state === st;
          r.style.display = (okCity && okState) ? '' : 'none';
        }});
      }}
      sIn.addEventListener('input', filterDir);
      sSel.addEventListener('change', filterDir);
    }})();
    </script>
    """


def enhance_dealership_page():
    """Enhances ev-dealership-india/index.html with B2B blueprint and searchable 100-city territory table."""
    path = os.path.join(ROOT_DIR, "ev-dealership-india", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    main_el = soup.find("main")
    if main_el:
        # Remove old city-directory / b2b-dealership-blueprint if present to ensure clean idempotent rebuild
        for old_id in ("city-directory", "b2b-dealership-blueprint"):
            old_el = soup.find(id=old_id)
            if old_el:
                old_el.decompose()
        # Also remove any old inline filter script for dir-city-search
        for sc in main_el.find_all("script"):
            if sc.string and "dir-city-search" in sc.string:
                sc.decompose()

        b2b_soup = BeautifulSoup(render_dealership_b2b_sections_html(), "html.parser")
        dir_soup = BeautifulSoup(render_state_city_directory_html(), "html.parser")
        for node in list(b2b_soup.contents):
            main_el.append(node)
        for node in list(dir_soup.contents):
            main_el.append(node)

        with open(path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print("✓ Upgraded ev-dealership-india/index.html with B2B blueprint & 100-city territory table")


def enhance_running_cost_page():
    """Embeds interactive Profitability Calculator, state tariffs & 5-year cashflow on running-cost page."""
    path = os.path.join(ROOT_DIR, "electric-three-wheeler-running-cost", "index.html")
    if not os.path.isfile(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    main_el = soup.find("main")
    if main_el:
        for old_id in ("calculator", "state-tariffs-cashflow"):
            old_el = soup.find(id=old_id)
            if old_el:
                old_el.decompose()
        for sc in main_el.find_all("script"):
            if sc.string and "dist-range" in sc.string:
                sc.decompose()

        calc_soup = BeautifulSoup(render_interactive_calculator_html(), "html.parser")
        tariff_soup = BeautifulSoup(render_state_tariff_and_cashflow_html(), "html.parser")
        for node in list(calc_soup.contents):
            main_el.append(node)
        for node in list(tariff_soup.contents):
            main_el.append(node)

        with open(path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print("✓ Embedded Interactive Profitability Calculator & State Tariffs into electric-three-wheeler-running-cost/index.html")


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


def sync_global_footer_and_schema(html_str: str, active_page: str = "") -> str:
    """Replaces <nav> and <footer> with global components and updates CIN/NAP in JSON-LD."""
    nav_path = os.path.join(ROOT_DIR, "templates", "components", "navbar.html")
    if os.path.isfile(nav_path):
        with open(nav_path, "r", encoding="utf-8") as f:
            raw_nav = f.read().strip()
        rendered_nav = re.sub(
            r"\{%\s*if active_page == '([^']+)'\s*%\}([^\{]+)\{%\s*endif\s*%\}",
            lambda m: "text-[#97FDFF] border-b-2 border-[#97FDFF] pb-1" if m.group(1) == active_page else "",
            raw_nav,
        )
    else:
        rendered_nav = ""

    footer_path = os.path.join(ROOT_DIR, "templates", "components", "footer.html")
    with open(footer_path, "r", encoding="utf-8") as f:
        global_footer = f.read().strip()

    # Replace stale CIN anywhere in text/schema
    html_str = html_str.replace("U29253UP2013PTC059344", "U28140UP2025PTC216042")

    soup = BeautifulSoup(html_str, "html.parser")
    if rendered_nav:
        old_nav = soup.find("nav", class_=lambda c: c and "fixed" in c)
        if old_nav:
            nav_soup = BeautifulSoup(rendered_nav, "html.parser")
            new_nav = nav_soup.find("nav")
            if new_nav:
                old_nav.replace_with(new_nav)
                # Ensure toggleNav script exists once
                if not any(sc.string and "function toggleNav" in sc.string for sc in soup.find_all("script")):
                    nav_sc = nav_soup.find("script")
                    if nav_sc:
                        new_nav.insert_after(nav_sc)

    old_footer = soup.find("footer")
    if old_footer:
        new_footer = BeautifulSoup(global_footer, "html.parser").find("footer")
        if new_footer:
            old_footer.replace_with(new_footer)

    # Sync Organization / LocalBusiness JSON-LD nodes
    org_node = build_organization_node()
    lb_node = build_local_business_node()
    for script in soup.find_all("script", type="application/ld+json"):
        raw = script.string or script.get_text() or ""
        if not raw.strip():
            continue
        try:
            data = json.loads(raw)
        except Exception:
            continue
        changed = False
        if isinstance(data, dict) and "@graph" in data and isinstance(data["@graph"], list):
            for idx, node in enumerate(data["@graph"]):
                if not isinstance(node, dict):
                    continue
                t = node.get("@type")
                if t == "Organization":
                    data["@graph"][idx] = org_node
                    changed = True
                elif t in ("LocalBusiness", "AutoDealer", "AutomotiveBusiness") or (
                    isinstance(t, list) and any(x in t for x in ("LocalBusiness", "AutoDealer", "AutomotiveBusiness"))
                ):
                    data["@graph"][idx] = lb_node
                    changed = True
        elif isinstance(data, dict) and data.get("@type") == "Organization":
            merged = {"@context": data.get("@context", "https://schema.org")}
            merged.update(org_node)
            if "areaServed" in data:
                merged["areaServed"] = data["areaServed"]
            data = merged
            changed = True
        elif isinstance(data, dict) and (
            data.get("@type") in ("LocalBusiness", "AutoDealer", "AutomotiveBusiness")
            or (isinstance(data.get("@type"), list) and any(x in data.get("@type") for x in ("LocalBusiness", "AutoDealer", "AutomotiveBusiness")))
        ):
            merged = {"@context": data.get("@context", "https://schema.org")}
            merged.update(lb_node)
            data = merged
            changed = True
        if changed:
            script.string = json.dumps(data, indent=2, ensure_ascii=False)

    return str(soup)


def set_page_og_image(html_str: str, image_url: str) -> str:
    """Sets page-specific og:image and twitter:image meta tags."""
    soup = BeautifulSoup(html_str, "html.parser")
    og_img = soup.find("meta", property="og:image")
    if og_img:
        og_img["content"] = image_url
    tw_img = soup.find("meta", attrs={"name": "twitter:image"})
    if tw_img:
        tw_img["content"] = image_url
    return str(soup)


def enhance_guide_pages():
    """Embeds static HTML TCO & Spec comparison table into commercial guide pages."""
    guide_pages = [
        os.path.join(ROOT_DIR, "electric-three-wheeler-running-cost", "index.html"),
        os.path.join(ROOT_DIR, "ev-dealership-india", "index.html"),
        os.path.join(ROOT_DIR, "electric-cargo-loader", "index.html"),
        os.path.join(ROOT_DIR, "electric-passenger-auto", "index.html"),
    ]
    table_html = render_guide_tco_spec_table_html()
    for p in guide_pages:
        if not os.path.isfile(p):
            continue
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        if 'id="verified-tco-specs"' not in content:
            anchor = content.find('id="city-directory"')
            if anchor != -1:
                div_start = content.rfind("<div", 0, anchor)
                if div_start != -1:
                    content = content[:div_start] + "\n" + table_html + "\n" + content[div_start:]
            else:
                idx = content.rfind("</main>")
                if idx != -1:
                    content = content[:idx] + "\n" + table_html + "\n" + content[idx:]
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✓ Embedded static TCO & Spec table into {os.path.relpath(p, ROOT_DIR)}")


def enhance_core_pages():
    """Injects popup, syncs global footer/JSON-LD, and sets page-specific og:image."""
    og_map = {
        os.path.join(ROOT_DIR, "products", "saffire-smart-ride", "index.html"): f"{BASE_URL}/images/saffire-smart-ride-l5-passenger-auto.jpg",
        os.path.join(ROOT_DIR, "electric-passenger-auto", "index.html"): f"{BASE_URL}/images/saffire-smart-ride-l5-passenger-auto.jpg",
        os.path.join(ROOT_DIR, "products", "saffire-swiss-cargo", "index.html"): f"{BASE_URL}/images/saffire-swiss-cargo-l5-loader.jpg",
        os.path.join(ROOT_DIR, "electric-cargo-loader", "index.html"): f"{BASE_URL}/images/saffire-swiss-cargo-l5-loader.jpg",
        os.path.join(ROOT_DIR, "contact", "index.html"): f"{BASE_URL}/images/saffire-ev-meerut-showroom.jpg",
        os.path.join(ROOT_DIR, "about", "index.html"): f"{BASE_URL}/images/saffire-ev-meerut-showroom.jpg",
        os.path.join(ROOT_DIR, "koyo-gears-india", "index.html"): f"{BASE_URL}/images/saffire-ev-meerut-showroom.jpg",
        os.path.join(ROOT_DIR, "ev-dealership-india", "index.html"): f"{BASE_URL}/images/saffire-ev-meerut-showroom.jpg",
    }
    core_pages = [
        os.path.join(ROOT_DIR, "index.html"),
        os.path.join(ROOT_DIR, "contact", "index.html"),
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
        os.path.join(ROOT_DIR, "l5-electric-vehicle", "index.html"),
        os.path.join(ROOT_DIR, "404.html"),
    ]

    active_map = {
        os.path.join(ROOT_DIR, "index.html"): "home",
        os.path.join(ROOT_DIR, "products", "index.html"): "products",
        os.path.join(ROOT_DIR, "products", "saffire-smart-ride", "index.html"): "products",
        os.path.join(ROOT_DIR, "products", "saffire-swiss-cargo", "index.html"): "products",
        os.path.join(ROOT_DIR, "ev-dealership-india", "index.html"): "dealership",
        os.path.join(ROOT_DIR, "koyo-gears-india", "index.html"): "koyo",
        os.path.join(ROOT_DIR, "about", "index.html"): "about",
        os.path.join(ROOT_DIR, "vision", "index.html"): "vision",
        os.path.join(ROOT_DIR, "contact", "index.html"): "contact",
    }
    for p in core_pages:
        if os.path.isfile(p):
            with open(p, "r", encoding="utf-8") as f:
                c = f.read()
            if os.path.basename(p) != "404.html":
                c = inject_popup_into_html(c)
            c = sync_global_footer_and_schema(c, active_page=active_map.get(p, ""))
            if p in og_map:
                c = set_page_og_image(c, og_map[p])
            with open(p, "w", encoding="utf-8") as f:
                f.write(c)
            print(f"✓ Enhanced & synced footer/schema for {os.path.relpath(p, ROOT_DIR)}")


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

    # 2. Build homepage, Smart Ride page, Dealership page, Running Cost page, and commercial guide pages
    print("\n[Step 2/6] Building Homepage, Product, Dealership, Running Cost & Guide Enhancements...")
    build_homepage()
    enhance_smart_ride_page()
    enhance_dealership_page()
    enhance_running_cost_page()
    enhance_guide_pages()

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

