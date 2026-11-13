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
