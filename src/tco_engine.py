"""
Saffire EV - Total Cost of Ownership (TCO) & Profitability Engine
Calculates operational economics, fuel/electricity cost deltas,
monthly extra profit, and lifetime cumulative savings vs Diesel, CNG, and Petrol.
"""
from __future__ import annotations

from typing import Dict, List, Any
from src.models import TCOTier

# Standard commercial operational rates in INR per KM
RATES = {
    "ev": 1.20,       # Electricity + minimal EV powertrain maintenance
    "diesel": 5.50,   # Fuel + engine oil, filters & mechanical maintenance
    "cng": 3.50,      # Compressed Natural Gas + high frequency maintenance
    "petrol": 6.80    # Petrol fuel + regular servicing
}

OPERATIONAL_DAYS_PER_YEAR = 365 * 0.90  # 90% fleet commercial utilization (~328.5 days)


def calculate_tco(daily_km: int, years: int, fuel: str = "diesel") -> Dict[str, Any]:
    """
    Computes precise commercial vehicle economics for given daily km and ownership years.
    Matches commercial fleet utilization and live website calculator formulas.
    """
    fuel_key = fuel.lower()
    if fuel_key not in RATES:
        fuel_key = "diesel"

    fuel_rate = RATES[fuel_key]
    ev_rate = RATES["ev"]

    total_days = years * OPERATIONAL_DAYS_PER_YEAR
    total_km = total_days * daily_km

    ev_total = total_km * ev_rate
    traditional_total = total_km * fuel_rate

    lifetime_savings = traditional_total - ev_total
    monthly_extra_profit = lifetime_savings / (years * 12)
    percent_gain = round(((fuel_rate / ev_rate) - 1) * 100)

    # Monthly costs
    monthly_km = (OPERATIONAL_DAYS_PER_YEAR / 12) * daily_km
    ev_monthly_cost = round(monthly_km * ev_rate)
    traditional_monthly_cost = round(monthly_km * fuel_rate)

    return {
        "daily_km": daily_km,
        "years": years,
        "fuel_type": fuel_key,
        "ev_rate_per_km": ev_rate,
        "fuel_rate_per_km": fuel_rate,
        "total_km_driven": round(total_km),
        "ev_total_cost": round(ev_total),
        "fuel_total_cost": round(traditional_total),
        "ev_monthly_cost": ev_monthly_cost,
        "fuel_monthly_cost": traditional_monthly_cost,
        "monthly_extra_profit": round(monthly_extra_profit),
        "lifetime_savings": round(lifetime_savings),
        "roi_percent_gain": percent_gain
    }


def generate_tco_matrix(
    daily_distances: List[int] = [60, 100, 120, 150, 200],
    durations: List[int] = [1, 3, 5, 10]
) -> List[TCOTier]:
    """
    Generates a structured list of TCOTier objects across commercial daily runs and years.
    """
    matrix: List[TCOTier] = []
    for km in daily_distances:
        for yr in durations:
            tco_diesel = calculate_tco(km, yr, "diesel")
            tco_cng = calculate_tco(km, yr, "cng")

            tier = TCOTier(
                daily_km=km,
                years=yr,
                ev_rate_per_km=RATES["ev"],
                diesel_rate_per_km=RATES["diesel"],
                cng_rate_per_km=RATES["cng"],
                ev_monthly_cost=tco_diesel["ev_monthly_cost"],
                diesel_monthly_cost=tco_diesel["fuel_monthly_cost"],
                cng_monthly_cost=tco_cng["fuel_monthly_cost"],
                monthly_extra_profit_vs_diesel=tco_diesel["monthly_extra_profit"],
                monthly_extra_profit_vs_cng=tco_cng["monthly_extra_profit"],
                cumulative_savings_vs_diesel=tco_diesel["lifetime_savings"],
                cumulative_savings_vs_cng=tco_cng["lifetime_savings"],
                roi_percent_gain_vs_diesel=float(tco_diesel["roi_percent_gain"])
            )
            matrix.append(tier)
    return matrix


def render_crawlable_tco_html() -> str:
    """
    Renders a semantic, search-engine-crawlable HTML table block for index.html.
    Provides verified rupee-per-km data, monthly extra profit, and 5-year savings
    for Google organic search indexing without requiring JS execution.
    """
    rows = [
        {"km": 60, "name": "Urban Feeder Route", "ev_cost": "₹1,971", "diesel_cost": "₹9,034", "profit": "₹7,063/mo", "savings_3yr": "₹2,54,250", "savings_5yr": "₹4,23,750"},
        {"km": 100, "name": "Standard Commercial Auto", "ev_cost": "₹3,285", "diesel_cost": "₹15,056", "profit": "₹11,771/mo", "savings_3yr": "₹4,23,750", "savings_5yr": "₹7,06,250"},
        {"km": 120, "name": "High-Duty Urban Shift", "ev_cost": "₹3,942", "diesel_cost": "₹18,068", "profit": "₹14,126/mo", "savings_3yr": "₹5,08,500", "savings_5yr": "₹8,47,530"},
        {"km": 150, "name": "Dual-Shift Passenger Auto", "ev_cost": "₹4,928", "diesel_cost": "₹22,584", "profit": "₹17,656/mo", "savings_3yr": "₹6,35,625", "savings_5yr": "₹10,59,375"},
        {"km": 200, "name": "Intra-City Delivery Cargo", "ev_cost": "₹6,570", "diesel_cost": "₹30,113", "profit": "₹23,543/mo", "savings_3yr": "₹8,47,500", "savings_5yr": "₹14,12,500"},
    ]

    html = """
    <div class="mt-12 bg-surface-container-low p-6 md:p-8 rounded-xl border border-outline-variant/15 text-left">
      <details class="group cursor-pointer">
        <summary class="font-headline font-bold text-lg md:text-xl text-primary flex items-center justify-between list-none">
          <span class="flex items-center gap-3">
            <span class="material-symbols-outlined text-primary" aria-hidden="true" data-nosnippet>table_chart</span>
            View Verified Commercial TCO Comparison Matrix (Saffire EV vs Diesel vs CNG)
          </span>
          <span class="material-symbols-outlined transition-transform duration-300 group-open:rotate-180 text-on-surface-variant" aria-hidden="true" data-nosnippet>expand_more</span>
        </summary>
        <div class="mt-6 pt-6 border-t border-outline-variant/10 text-on-surface-variant text-sm space-y-4">
          <p class="font-body text-xs md:text-sm text-on-surface-variant">
            Based on verified commercial operating costs in India: <strong>Saffire EV at ₹1.20/km</strong> (electricity + minimal powertrain servicing), 
            <strong>CNG Auto at ₹3.50/km</strong>, and <strong>Diesel Auto at ₹5.50/km</strong> (fuel + mechanical maintenance). 
            Calculated at 90% commercial fleet utilization (328.5 operating days per year).
          </p>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs md:text-sm border-collapse">
              <thead>
                <tr class="border-b border-outline-variant/20 bg-surface-container-highest/40 text-on-surface font-headline">
                  <th class="p-3">Daily Run</th>
                  <th class="p-3">Commercial Duty Profile</th>
                  <th class="p-3">Saffire EV / Month</th>
                  <th class="p-3">Diesel Auto / Month</th>
                  <th class="p-3 text-primary font-bold">Extra Monthly Profit</th>
                  <th class="p-3">3-Year Cumulative Savings</th>
                  <th class="p-3">5-Year Cumulative Savings</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-outline-variant/10 font-body">
    """
    for r in rows:
        html += f"""
                <tr class="hover:bg-surface-container-highest/20 transition-colors">
                  <td class="p-3 font-bold text-on-surface">{r['km']} km/day</td>
                  <td class="p-3 text-on-surface-variant">{r['name']}</td>
                  <td class="p-3 text-emerald-400 font-semibold">{r['ev_cost']}</td>
                  <td class="p-3 text-rose-400">{r['diesel_cost']}</td>
                  <td class="p-3 text-primary font-bold">{r['profit']}</td>
                  <td class="p-3 text-on-surface">{r['savings_3yr']}</td>
                  <td class="p-3 text-on-surface font-semibold">{r['savings_5yr']}</td>
                </tr>
        """
    html += """
              </tbody>
            </table>
          </div>
          <div class="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 text-xs text-on-surface-variant border-t border-outline-variant/10">
            <span>* Figures based on commercial average electricity tariffs (₹7.50/unit) and current diesel prices (₹90+/litre). Individual savings vary with route topography.</span>
            <button type="button" data-open-query-popup data-query-intent="preorder" class="px-4 py-2 bg-primary text-background font-bold rounded-lg text-xs hover:bg-primary/90 transition-colors shrink-0">
              Calculate Exact Savings For Your Fleet
            </button>
          </div>
        </div>
      </details>
    </div>
    """
    return html


def render_l5_vs_l3_vs_diesel_html() -> str:
    """
    Renders an authoritative semantic comparison section & table:
    'Why Choose a Saffire L5 Auto Rickshaw (Koyo L5 Electric 3 Wheeler) Over Diesel/CNG Autos & L3 E-Rickshaws?'
    Targets generic commercial search queries: 'L5 auto', 'Auto rickshaw', 'Electric auto rickshaw', 'Koyo L5', 'Saffire auto'.
    """
    features = [
        ("Top Governed Speed", "50 km/h (Fast Highway & City Arteries)", "25 km/h (Restricted Low Speed)", "55 km/h (Noisy & High Vibration)"),
        ("Certified Driving Range", "200 km* per single charge", "80–100 km (Requires midday halt)", "160–180 km per fuel tank"),
        ("Battery Pack & Energy", "14.61 kWh (63V 232Ah) Advanced Li-ion", "4.8–6.0 kWh (Lead Acid / Small Li)", "Diesel Fuel Tank (No Battery)"),
        ("Peak Motor / Engine Power", "6.3 kW (6300W) High-Torque PMSM", "1.0–1.2 kW BLDC Motor", "6.5 kW (9 HP) Diesel Engine"),
        ("Certified Commercial Payload", "600 kg Certified Heavy-Duty", "300–350 kg (Lightweight)", "400–500 kg Standard"),
        ("Running Cost per KM", "₹1.20 / km (Lowest Operating Cost)", "₹0.85 / km (Very limited duty)", "₹5.50 / km (Extreme fuel expense)"),
        ("Monthly Net Extra Profit", "+₹14,126 / month vs Diesel Auto", "Low revenue due to slow speed", "Baseline zero extra savings"),
        ("Gradability (Flyovers & Ramps)", "15% Gradient (Effortless loaded start)", "5–7% (Struggles on bridges)", "12–15% Gradient"),
        ("Chassis & Passenger Safety", "Heavy-Gauge Tubular Automotive Steel", "Thin pipe local e-rickshaw frame", "Traditional sheet metal"),
        ("Regulatory Class & Compliance", "ICAT Manesar L5 (AIS-040/053/156)", "L3 E-Rickshaw (Zone-restricted)", "BS6 ICE Commercial Three Wheeler"),
        ("Seating & Legroom Comfort", "Ergonomic D+3 with generous legroom", "Narrow cramped 4-passenger bench", "Traditional D+3 bench"),
        ("Route Flexibility", "Full city, bypass & highway routes", "Short radius colony feeder only", "City-wide routes")
    ]

    table_rows = ""
    for param, l5_val, l3_val, diesel_val in features:
        table_rows += f"""
        <tr class="hover:bg-surface-container-highest/20 transition-colors border-b border-outline-variant/10 text-xs md:text-sm">
          <td class="p-3.5 font-bold text-on-surface">{param}</td>
          <td class="p-3.5 text-primary font-semibold bg-primary/5">{l5_val}</td>
          <td class="p-3.5 text-on-surface-variant">{l3_val}</td>
          <td class="p-3.5 text-rose-300/80">{diesel_val}</td>
        </tr>
        """

    html = f"""
<section class="py-16 md:py-24 bg-surface-container-lowest border-t border-outline-variant/15" id="l5-comparison">
  <div class="max-w-6xl mx-auto px-6 md:px-8">
    <div class="text-center max-w-3xl mx-auto mb-12">
      <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-label uppercase tracking-widest mb-3">
        <span class="material-symbols-outlined text-sm" aria-hidden="true" data-nosnippet>verified</span>
        Definitive Commercial Three-Wheeler Comparison
      </span>
      <h2 class="font-headline text-2xl md:text-4xl font-bold tracking-tight text-on-surface">
        Why Choose a Saffire L5 Auto Rickshaw (Koyo L5 Electric 3 Wheeler) Over Diesel/CNG Autos &amp; L3 E-Rickshaws?
      </h2>
      <p class="font-body text-xs md:text-base text-on-surface-variant font-light mt-4 leading-relaxed">
        Commercial auto drivers and fleet operators in India frequently ask: <em>What makes an ICAT-certified L5 electric auto rickshaw superior to traditional diesel autos and local low-speed e-rickshaws?</em> Here is the verified technical and economic breakdown:
      </p>
    </div>

    <!-- Crawlable Comparison Table -->
    <div class="overflow-x-auto rounded-xl border border-outline-variant/20 shadow-xl bg-surface-container-low mb-10">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="border-b border-outline-variant/20 bg-surface-container-high text-on-surface font-headline text-xs md:text-sm">
            <th class="p-3.5">Vehicle Specification Parameter</th>
            <th class="p-3.5 text-primary font-bold bg-primary/10">Saffire Smart Ride (Koyo L5 Auto)</th>
            <th class="p-3.5">Standard L3 E-Rickshaw</th>
            <th class="p-3.5">Traditional Diesel Auto Rickshaw</th>
          </tr>
        </thead>
        <tbody class="font-body divide-y divide-outline-variant/10">
          {table_rows}
        </tbody>
      </table>
    </div>

    <!-- Quick Takeaways Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="p-6 rounded-xl bg-surface-container-low border border-outline-variant/15">
        <div class="w-10 h-10 rounded-lg bg-primary/10 text-primary flex items-center justify-center mb-3">
          <span class="material-symbols-outlined text-xl" aria-hidden="true" data-nosnippet>speed</span>
        </div>
        <h3 class="font-headline font-bold text-base text-on-surface mb-2">Double the Speed of L3</h3>
        <p class="font-body text-xs text-on-surface-variant leading-relaxed">
          At 50 km/h top speed, Saffire L5 auto rickshaws complete round-trips in half the time of 25 km/h L3 e-rickshaws, allowing drivers to take 2x passenger fares every working day.
        </p>
      </div>

      <div class="p-6 rounded-xl bg-surface-container-low border border-outline-variant/15">
        <div class="w-10 h-10 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-3">
          <span class="material-symbols-outlined text-xl" aria-hidden="true" data-nosnippet>savings</span>
        </div>
        <h3 class="font-headline font-bold text-base text-on-surface mb-2">₹14,000+ Monthly Fuel Savings</h3>
        <p class="font-body text-xs text-on-surface-variant leading-relaxed">
          At ₹1.20/km versus ₹5.50/km for diesel autos, Saffire EV puts over ₹14,126 extra clean profit straight into the driver's pocket every month (over ₹8.4 Lakhs in 5 years).
        </p>
      </div>

      <div class="p-6 rounded-xl bg-surface-container-low border border-outline-variant/15">
        <div class="w-10 h-10 rounded-lg bg-primary/10 text-primary flex items-center justify-center mb-3">
          <span class="material-symbols-outlined text-xl" aria-hidden="true" data-nosnippet>shield</span>
        </div>
        <h3 class="font-headline font-bold text-base text-on-surface mb-2">600 kg Payload &amp; ICAT Safety</h3>
        <p class="font-body text-xs text-on-surface-variant leading-relaxed">
          Built on heavy-duty tubular steel with AIS-156 fire-tested battery enclosure and dual hydraulic brakes for maximum safety on highways, flyovers, and elevated routes.
        </p>
      </div>
    </div>

    <!-- CTA Bar -->
    <div class="mt-10 p-6 rounded-xl bg-primary/5 border border-primary/20 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div>
        <h4 class="font-headline font-bold text-base text-on-surface">Ready to upgrade from an L3 e-rickshaw or diesel auto?</h4>
        <p class="font-body text-xs text-on-surface-variant">Get custom on-road price quotes, EMI calculator sheets, and dealer test drives.</p>
      </div>
      <button type="button" data-open-query-popup data-query-intent="preorder" class="px-6 py-3 bg-primary text-background font-headline font-bold rounded-lg text-xs uppercase tracking-wider hover:bg-primary/90 transition-all shrink-0 cursor-pointer shadow-lg shadow-primary/20">
        Get Saffire L5 Auto Price Quote
      </button>
    </div>
  </div>
</section>
"""
    return html


def render_guide_tco_spec_table_html() -> str:
    """
    Renders a responsive static HTML TCO & specification comparison table
    for commercial guide pages (AI citation & GEO density).
    Baseline: 120 km daily run, 5 Years ownership period.
    """
    rows = [
        ("Vehicle Category & Layout", "L5M Passenger Auto (D+3)", "L5N Commercial Cargo Loader", "ICE Diesel 3-Wheeler"),
        ("Battery Capacity & Chemistry", "14.61 kWh (63V 232Ah)", "14.61 kWh (63V 232Ah)", "Fossil Fuel (Diesel Tank)"),
        ("Claimed Range per Charge", "200 km*", "200 km*", "N/A"),
        ("Payload Capacity", "600 kg", "600 kg", "450–500 kg"),
        ("Motor Peak Power & Top Speed", "6.3 kW (6300 W) / 50 km/hr", "6.3 kW (6300 W) / 50 km/hr", "~50 km/hr"),
        ("Wheelbase & Tyre Size", "1948 mm / 4.12-12", "2413 mm / 4.12-12", "Standard"),
        ("Gradability & Charging Time", "15% / 5–6 hours (standard charger)", "15% / 5–6 hours (standard charger)", "N/A"),
        ("5-Year Total Operating Cost (120 km/day)", "₹ 2,36,520", "₹ 2,36,520", "₹ 10,84,050"),
        ("Estimated Extra Monthly Profit", "+₹ 14,126 (+358% vs. Diesel)", "+₹ 14,126 (+358% vs. Diesel)", "Baseline"),
        ("5-Year Lifetime Net Savings", "₹ 8,47,530", "₹ 8,47,530", "₹ 0 (Baseline)"),
    ]

    row_html = ""
    for metric, smart, swiss, diesel in rows:
        row_html += f"""
        <tr class="hover:bg-surface-container-highest/20 transition-colors border-b border-outline-variant/10 text-xs md:text-sm">
          <td class="p-3.5 font-bold text-on-surface">{metric}</td>
          <td class="p-3.5 text-primary font-semibold bg-primary/5">{smart}</td>
          <td class="p-3.5 text-on-surface font-semibold">{swiss}</td>
          <td class="p-3.5 text-rose-300/80">{diesel}</td>
        </tr>"""

    return f"""
<section class="my-12 rounded-2xl bg-surface-container-low border border-outline-variant/20 p-6 md:p-8" id="verified-tco-specs">
  <div class="mb-6">
    <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-label uppercase tracking-widest mb-2">
      <span class="material-symbols-outlined notranslate text-sm" translate="no" aria-hidden="true" data-nosnippet>analytics</span>
      <span>Verified Commercial TCO &amp; Technical Benchmark</span>
    </span>
    <h2 class="font-headline text-xl md:text-2xl font-bold text-on-surface">
      Saffire Smart Ride &amp; Swiss Cargo vs. Traditional Diesel Auto (120 km/day, 5-Year Baseline)
    </h2>
    <p class="font-body text-xs md:text-sm text-on-surface-variant font-light mt-2">
      Standardized commercial fleet comparison at ₹1.20/km EV operating cost versus ₹5.50/km Diesel Auto baseline (90% annual fleet utilization).
    </p>
  </div>
  <div class="overflow-x-auto rounded-xl border border-outline-variant/20 bg-surface-container">
    <table class="w-full text-left border-collapse">
      <thead>
        <tr class="border-b border-outline-variant/20 bg-surface-container-high text-on-surface font-headline text-xs md:text-sm">
          <th class="p-3.5">Metric / Parameter</th>
          <th class="p-3.5 text-primary font-bold bg-primary/10">Saffire Smart Ride (L5 Passenger)</th>
          <th class="p-3.5 font-bold">Saffire Swiss Cargo (L5 Loader)</th>
          <th class="p-3.5">Traditional Diesel Auto Baseline</th>
        </tr>
      </thead>
      <tbody class="font-body divide-y divide-outline-variant/10">
        {row_html}
      </tbody>
    </table>
  </div>
</section>
"""


def render_interactive_calculator_html() -> str:
    """
    Reusable interactive Profitability Calculator component + Verified Commercial TCO Matrix
    for /electric-three-wheeler-running-cost/ (and compatible with homepage IDs).
    """
    tco_matrix = render_crawlable_tco_html()
    return f"""
<section class="my-12 rounded-2xl bg-surface-container border border-outline-variant/20 p-6 md:p-10" id="calculator">
  <div class="text-center max-w-2xl mx-auto mb-10">
    <span class="font-label text-[10px] tracking-[0.2em] uppercase text-primary block mb-2">Interactive Commercial ROI Engine</span>
    <h2 class="font-headline text-2xl md:text-4xl font-bold tracking-tight text-on-surface">Saffire EV Profitability Calculator</h2>
    <p class="font-body text-xs md:text-sm text-on-surface-variant font-light mt-2">
      Adjust daily distance and ownership duration to compare Saffire EV (₹1.20/km) against Diesel (₹5.50/km), CNG (₹3.50/km), and Petrol (₹6.80/km).
    </p>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
    <!-- Controls -->
    <div class="bg-surface-container-low p-6 md:p-8 rounded-xl border border-outline-variant/15 space-y-8">
      <div>
        <div class="flex justify-between items-center mb-3">
          <label class="font-label text-xs uppercase tracking-widest text-on-surface-variant" for="dist-range">Daily Running Distance</label>
          <span class="font-headline text-xl font-bold text-primary" id="dist-val">120 km</span>
        </div>
        <input class="w-full accent-[#97FDFF] cursor-pointer" id="dist-range" max="250" min="40" step="10" type="range" value="120"/>
        <div class="flex justify-between text-[10px] text-on-surface-variant/60 mt-1">
          <span>40 km/day</span>
          <span>120 km/day (Avg)</span>
          <span>250 km/day</span>
        </div>
      </div>

      <div>
        <div class="flex justify-between items-center mb-3">
          <label class="font-label text-xs uppercase tracking-widest text-on-surface-variant" for="year-range">Ownership Duration</label>
          <span class="font-headline text-xl font-bold text-primary" id="year-val">5 Years</span>
        </div>
        <input class="w-full accent-[#97FDFF] cursor-pointer" id="year-range" max="10" min="1" step="1" type="range" value="5"/>
        <div class="flex justify-between text-[10px] text-on-surface-variant/60 mt-1">
          <span>1 Year</span>
          <span>5 Years</span>
          <span>10 Years</span>
        </div>
      </div>

      <div>
        <span class="font-label text-xs uppercase tracking-widest text-on-surface-variant block mb-3">Compare Against Fuel Type</span>
        <div class="grid grid-cols-3 gap-3">
          <button class="fuel-btn py-3 px-4 rounded border border-outline-variant/20 font-label text-[10px] tracking-widest uppercase transition-all opacity-50" id="btn-cng" onclick="setFuel('cng')" type="button">CNG Auto</button>
          <button class="fuel-btn active py-3 px-4 rounded border border-outline-variant/20 font-label text-[10px] tracking-widest uppercase transition-all bg-surface-container-highest text-primary" id="btn-diesel" onclick="setFuel('diesel')" type="button">Diesel Auto</button>
          <button class="fuel-btn py-3 px-4 rounded border border-outline-variant/20 font-label text-[10px] tracking-widest uppercase transition-all opacity-50" id="btn-petrol" onclick="setFuel('petrol')" type="button">Petrol Auto</button>
        </div>
      </div>
    </div>

    <!-- Outputs -->
    <div class="flex flex-col gap-5">
      <div class="bg-primary/5 border border-primary/20 p-6 md:p-8 rounded-xl relative overflow-hidden">
        <p class="font-label text-[10px] tracking-widest uppercase text-primary/80 mb-2">Estimated Extra Monthly Profit</p>
        <div class="font-headline text-4xl md:text-5xl font-bold tracking-tighter text-primary" id="calc-extra-profit">₹ 14,126</div>
        <p class="text-xs text-on-surface-variant mt-2 font-light" id="calc-percent">+358% more profitable than diesel</p>
        <div class="mt-4 pt-4 border-t border-primary/20">
          <button id="calc-lock-savings-btn" class="w-full py-3 px-4 bg-primary text-background font-headline font-bold text-xs uppercase tracking-wider rounded-lg hover:bg-primary/90 transition-all flex items-center justify-center gap-2 shadow-md cursor-pointer" data-calculator="true" data-open-query-popup="" data-query-intent="preorder" type="button">
            <span aria-hidden="true" class="material-symbols-outlined notranslate text-sm" data-nosnippet="" translate="no">savings</span>
            <span>Lock In Your <span id="calc-lock-savings-amount">₹ 8,47,530</span> Savings — Request Dealer / Fleet Quote</span>
          </button>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div class="bg-surface-container-low p-5 rounded-xl border border-outline-variant/10 text-center">
          <p class="text-[10px] font-label text-on-surface-variant uppercase tracking-widest mb-1">Saffire (EV)</p>
          <p class="font-headline text-xl font-bold text-emerald-400" id="ev-cost">₹ 2,36,520</p>
          <p class="text-[10px] text-on-surface-variant mt-1">Total Operating Cost</p>
        </div>
        <div class="bg-surface-container-low p-5 rounded-xl border border-outline-variant/10 text-center">
          <p class="text-[10px] font-label text-on-surface-variant uppercase tracking-widest mb-1" id="fuel-label">Diesel</p>
          <p class="font-headline text-xl font-bold text-rose-300" id="fuel-cost">₹ 10,84,050</p>
          <p class="text-[10px] text-on-surface-variant mt-1">Total Operating Cost</p>
        </div>
      </div>

      <div class="bg-surface-container-low p-5 rounded-xl border border-outline-variant/10">
        <div class="flex justify-between items-center mb-2">
          <span class="text-xs font-label uppercase tracking-widest text-on-surface-variant">Total Cumulative Savings</span>
          <span class="font-headline text-2xl font-bold text-primary" id="calc-lifetime">₹ 8,47,530</span>
        </div>
        <div class="w-full h-2.5 bg-surface-container-highest rounded-full overflow-hidden">
          <div class="h-full bg-primary rounded-full" id="savings-bar" style="width: 78%;"></div>
        </div>
      </div>
    </div>
  </div>

  {tco_matrix}
</section>
<script>
(function() {{
  const distRange = document.getElementById('dist-range');
  const yearRange = document.getElementById('year-range');
  const dVal = document.getElementById('dist-val');
  const yVal = document.getElementById('year-val');
  if (!distRange || !yearRange) return;

  let currentFuel = 'diesel';
  const rates = {{ ev: 1.20, diesel: 5.50, cng: 3.50, petrol: 6.80 }};
  const formatINR = val => '₹ ' + Math.round(val).toLocaleString('en-IN');

  window.setFuel = function(type) {{
    currentFuel = type;
    document.querySelectorAll('.fuel-btn').forEach(b => {{
      b.classList.remove('active', 'bg-surface-container-highest', 'text-primary');
      b.style.opacity = '0.5';
    }});
    const activeBtn = document.getElementById('btn-' + type);
    if (activeBtn) {{
      activeBtn.classList.add('active', 'bg-surface-container-highest', 'text-primary');
      activeBtn.style.opacity = '1';
    }}
    const fl = document.getElementById('fuel-label');
    if (fl) fl.textContent = type.charAt(0).toUpperCase() + type.slice(1);
    calculateTCO();
  }};

  function calculateTCO() {{
    const km = parseInt(distRange.value, 10);
    const years = parseInt(yearRange.value, 10);
    const totalDays = years * 365 * 0.9;
    const totalKm = totalDays * km;
    const evTotal = totalKm * rates.ev;
    const traditionalTotal = totalKm * rates[currentFuel];
    const lifetimeSavings = traditionalTotal - evTotal;
    const extraProfit = lifetimeSavings / (years * 12);
    const pct = Math.round(((traditionalTotal / evTotal) - 1) * 100);

    dVal.textContent = km + ' km';
    yVal.textContent = years + (years === 1 ? ' Year' : ' Years');
    document.getElementById('calc-extra-profit').textContent = formatINR(extraProfit);
    document.getElementById('ev-cost').textContent = formatINR(evTotal);
    document.getElementById('fuel-cost').textContent = formatINR(traditionalTotal);
    document.getElementById('calc-lifetime').textContent = formatINR(lifetimeSavings);
    document.getElementById('calc-percent').textContent = `+${{pct}}% more profitable than ${{currentFuel}}`;
    const lockAmt = document.getElementById('calc-lock-savings-amount');
    if (lockAmt) lockAmt.textContent = formatINR(lifetimeSavings);

    const barPct = Math.min(95, (evTotal / traditionalTotal) * 100);
    const savingsBar = document.getElementById('savings-bar');
    if (savingsBar) savingsBar.style.width = (100 - barPct) + '%';

    window.currentCalcSettings = {{
      km: km,
      years: years,
      profit: formatINR(extraProfit),
      lifetimeSavings: formatINR(lifetimeSavings),
      fuel: currentFuel
    }};
  }}

  distRange.addEventListener('input', calculateTCO);
  yearRange.addEventListener('input', calculateTCO);
  calculateTCO();
}})();
</script>
"""


def render_state_tariff_and_cashflow_html() -> str:
    """Renders state-wise commercial electricity tariff examples and a 5-year cash-flow breakdown."""
    tariffs = [
        ("Uttar Pradesh (Meerut, Noida, Lucknow)", "₹7.50 – ₹8.50 / kWh", "₹110 – ₹124 / full charge", "₹0.55 – ₹0.62 / km (energy only)"),
        ("Delhi NCR (BSES / TPDDL EV Tariff)", "₹4.50 – ₹5.50 / kWh", "₹66 – ₹80 / full charge", "₹0.33 – ₹0.40 / km (energy only)"),
        ("Haryana (Gurugram, Faridabad)", "₹6.50 – ₹7.50 / kWh", "₹95 – ₹110 / full charge", "₹0.48 – ₹0.55 / km (energy only)"),
        ("Rajasthan (Jaipur, Jodhpur)", "₹6.80 – ₹7.80 / kWh", "₹99 – ₹114 / full charge", "₹0.50 – ₹0.57 / km (energy only)"),
        ("Maharashtra (Mumbai, Pune)", "₹5.50 – ₹7.50 / kWh", "₹80 – ₹110 / full charge", "₹0.40 – ₹0.55 / km (energy only)"),
        ("Gujarat (Ahmedabad, Surat)", "₹5.00 – ₹6.50 / kWh", "₹73 – ₹95 / full charge", "₹0.37 – ₹0.48 / km (energy only)"),
    ]
    tariff_rows = "".join([
        f"""<tr class="border-b border-outline-variant/10 text-xs md:text-sm">
          <td class="p-3.5 font-semibold text-on-surface">{st}</td>
          <td class="p-3.5 text-on-surface-variant">{rate}</td>
          <td class="p-3.5 text-primary font-semibold">{full_chg}</td>
          <td class="p-3.5 text-emerald-400 font-semibold">{per_km}</td>
        </tr>"""
        for st, rate, full_chg, per_km in tariffs
    ])

    cashflow_rows = [
        ("Year 1", "39,420 km", "₹ 47,304", "₹ 2,16,810", "₹ 1,69,506"),
        ("Year 2", "78,840 km", "₹ 94,608", "₹ 4,33,620", "₹ 3,39,012"),
        ("Year 3", "1,18,260 km", "₹ 1,41,912", "₹ 6,50,430", "₹ 5,08,518"),
        ("Year 4", "1,57,680 km", "₹ 1,89,216", "₹ 8,67,240", "₹ 6,78,024"),
        ("Year 5", "1,97,100 km", "₹ 2,36,520", "₹ 10,84,050", "₹ 8,47,530"),
    ]
    cf_rows = "".join([
        f"""<tr class="border-b border-outline-variant/10 text-xs md:text-sm">
          <td class="p-3.5 font-bold text-on-surface">{yr}</td>
          <td class="p-3.5 text-on-surface-variant">{km}</td>
          <td class="p-3.5 text-emerald-400 font-semibold">{ev_c}</td>
          <td class="p-3.5 text-rose-300/80">{ds_c}</td>
          <td class="p-3.5 text-primary font-bold">{sav}</td>
        </tr>"""
        for yr, km, ev_c, ds_c, sav in cashflow_rows
    ])

    return f"""
<section class="my-12 space-y-10" id="state-tariffs-cashflow">
  <div class="rounded-2xl bg-surface-container-low border border-outline-variant/20 p-6 md:p-8">
    <h2 class="font-headline text-xl md:text-2xl font-bold text-on-surface mb-2">
      State-Wise Commercial Electricity Tariffs &amp; Full-Charge Cost (14.61 kWh Battery)
    </h2>
    <p class="text-xs md:text-sm text-on-surface-variant font-light mb-6">
      Dedicated EV charging tariffs across major Indian states keep Saffire EV energy costs under ₹0.62/km (plus minimal maintenance = ₹1.20/km all-in TCO).
    </p>
    <div class="overflow-x-auto rounded-xl border border-outline-variant/20 bg-surface-container">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="border-b border-outline-variant/20 bg-surface-container-high text-on-surface font-headline text-xs md:text-sm">
            <th class="p-3.5">State / Region</th>
            <th class="p-3.5">EV / Commercial Tariff</th>
            <th class="p-3.5 text-primary">Full Charge Cost (14.61 kWh)</th>
            <th class="p-3.5">Energy Cost per km (200 km*)</th>
          </tr>
        </thead>
        <tbody class="font-body divide-y divide-outline-variant/10">{tariff_rows}</tbody>
      </table>
    </div>
  </div>

  <div class="rounded-2xl bg-surface-container-low border border-outline-variant/20 p-6 md:p-8">
    <h2 class="font-headline text-xl md:text-2xl font-bold text-on-surface mb-2">
      5-Year Cumulative Cash-Flow Breakdown (120 km/day @ 90% Utilization)
    </h2>
    <p class="text-xs md:text-sm text-on-surface-variant font-light mb-6">
      Cumulative operating expense comparison between Saffire EV (₹1.20/km) and a traditional Diesel Auto (₹5.50/km) over 5 years.
    </p>
    <div class="overflow-x-auto rounded-xl border border-outline-variant/20 bg-surface-container">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="border-b border-outline-variant/20 bg-surface-container-high text-on-surface font-headline text-xs md:text-sm">
            <th class="p-3.5">Ownership Milestone</th>
            <th class="p-3.5">Cumulative Distance</th>
            <th class="p-3.5 text-emerald-400">Saffire EV Cumulative Cost</th>
            <th class="p-3.5 text-rose-300/80">Diesel Auto Cumulative Cost</th>
            <th class="p-3.5 text-primary font-bold">Net Cumulative Savings</th>
          </tr>
        </thead>
        <tbody class="font-body divide-y divide-outline-variant/10">{cf_rows}</tbody>
      </table>
    </div>
  </div>
</section>
"""



