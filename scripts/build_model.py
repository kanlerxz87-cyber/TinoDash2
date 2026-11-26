#!/usr/bin/env python3
"""
Build the figure-driven, rounded-to-$10 decision model (data/model.js + data/model.json).

Owner-instruction basis (see COORDINATION.md, session e4e062ed):
  - Currency values rounded to the nearest $10 before publication.
  - Placeholders only: Property A / Property B / Owner B. No names, street addresses,
    ZIP codes, parcel/APN IDs, account numbers, or trust identifiers in outputs.
  - Every published figure carries either an official source link or an explicit
    "unverified/flagged" label in the site pages.
  - The full-precision household series stays in git-ignored private/ (internal only).

This script is deterministic: run it, then rebuild the site pages if inputs changed.
After any input change: run this script, re-run scripts/check_site.py, and compare the
recommendation against the previous run (stability check recorded in COORDINATION.md).
"""
from __future__ import annotations
import json, math, os
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def r10(x):
    if x is None:
        return None
    return int(round(float(x) / 10.0) * 10)

def pct(x, nd=2):
    return round(x * 100, nd)

def fv(value, rate, years):
    return value * (1.0 + rate) ** years

# ---------------------------------------------------------------------------
# Official anchors (verified 2026-11-25; links live in sources.html / sources.md)
# ---------------------------------------------------------------------------
ANCHORS = {
    "federal_estate_exclusion_2026": 15000000,
    "federal_estate_exclusion_source": "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax",
    "federal_estate_law": "Public Law 119-21 (One Big Beautiful Bill Act, enacted July 4, 2025); amends IRC 2010(c)(3); $15,000,000 for calendar year 2026, indexed after 2026, no sunset provision.",
    "federal_estate_top_rate": 0.40,
    "federal_estate_top_rate_source": "https://www.irs.gov/instructions/i706",
    "annual_gift_exclusion_2026": 19000,
    "annual_gift_exclusion_noncitizen_spouse": 194000,
    "annual_gift_source": "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax",
    "prop19_allowance_2025_2027": 1044586,
    "prop19_allowance_window": "Transfers on/after Feb 16, 2025 and before Feb 16, 2027 (BOE LTA 2025/009; NR-25-02). Recheck for the actual transfer year.",
    "prop19_allowance_source": "https://www.boe.ca.gov/news/2025/nr-25-02.htm",
    "prop19_rules_source": "https://www.boe.ca.gov/prop19/",
    "prop19_occupancy_rule": "Family-home exclusion requires the property to have been the transferor's principal residence, the transferee's eligibility, occupancy as the transferee's principal residence, a homeowners'/disabled veterans' exemption application within 1 year, and a claim within 3 years (RTC 63.2).",
    "scc_1pct_base_rate": 0.01,
    "scc_typical_tra_total": 0.011488,
    "scc_tra_note": "Santa Clara County Assessor Assessment Information booklet example TRA, read as dollars per $100 of assessed value (verified in the 2026 booklet on 2026-11-26): base rate 1% = $1.00 + county bonds $0.0388 + school bonds $0.100 + water bonds $0.010 = $1.1488 per $100 (= 1.1488%). The earlier note mis-scaled the school and water components by 10x (they are dollars per $100, not fractions); the 1.1488% total was and remains correct. The parcel's own Tax Rate Area total is published annually in the County Controller-Treasurer 'Compilation of Tax Rates and Information' (parcel-specific; obtain privately).",
    "scc_tra_source": "https://files.santaclaracounty.gov/exjcpb1521/2026-04/assessment-information-2026-booklet-english-3-23-26-web.pdf",
    "scc_rate_book_source": "https://www.sccassessor.org/",
    "scc_fixed_charges_annual_base": 1010,
    "scc_fixed_charges_note": "Non-ad-valorem fixed charges and parcel assessments derived from the household bill pattern (total bill minus ad-valorem estimate). Rounded to $10. Parcel-specific; verify on the actual tax bill.",
    "scc_transfer_tax_per_500": 0.55,
    "scc_transfer_tax_note": "County documentary transfer tax $0.55 per $500. City conveyance tax applies only in San Jose, Palo Alto, and Mountain View - not in the Property A city. Verify at recording.",
    "scc_transfer_tax_source": "https://clerkrecorder.santaclaracounty.gov/recording-documents/recording-real-estate",
    "scc_recording_first_page": 102,
    "scc_recording_source": "https://clerkrecorder.santaclaracounty.gov/recording-documents/recording-document-fees",
    "sf_transfer_tax_schedule": [
        {"low": 0, "high": 250000, "per_500": 2.50, "rate": 0.005},
        {"low": 250000, "high": 1000000, "per_500": 3.40, "rate": 0.0068},
        {"low": 1000000, "high": 5000000, "per_500": 3.75, "rate": 0.0075},
        {"low": 5000000, "high": 10000000, "per_500": 11.25, "rate": 0.0225},
        {"low": 10000000, "high": 25000000, "per_500": 27.50, "rate": 0.055},
        {"low": 25000000, "high": None, "per_500": 30.00, "rate": 0.06},
    ],
    "sf_transfer_tax_source": "https://www.sf.gov/reports--march-2024--fees-record-document-san-francisco",
    "sf_transfer_tax_note": "Bracket rate applies to the ENTIRE consideration (cliff structure). Qualified rent-restricted affordable housing capped at $3.75 per $500 (SBTR 1108.6).",
    "sf_prop_h": {
        "name": "San Francisco Proposition H - Stronger Muni For All parcel tax (approved Nov 3, 2026)",
        "multifamily_annual_fy2027_28_up_to_5000sf": 249,
        "multifamily_over_5000sf_per_sf": 0.195,
        "multifamily_cap": 50000,
        "senior_exemption": "Owner 65+ before July 1 of the tax year, living in a multifamily unit as principal residence: $249 off per qualifying unit (application required by June 1 for the upcoming bill).",
        "term": "FY2027-28 through FY2041-42; amounts indexed for inflation beginning FY2028-29.",
        "source": "https://www.sfmta.com/getting-around/muni/parcel",
    },
    "ftb_line62_1pct_over_1m": 0.01,
    "ftb_line62_threshold": 1000000,
    "ftb_line62_note": "Form 540 line 62, 'Behavioral Health Services Tax' (renamed for tax years beginning on/after Jan 1, 2025): 1% of California taxable income above $1,000,000, whole dollars, not indexed (R&TC 17043). Capital gains are taxed as ordinary California income with no preferential rate.",
    "ftb_line62_source": "https://www.ftb.ca.gov/forms/2025/2025-540-instructions.html",
    "sec121_exclusion_single": 250000,
    "sec121_exclusion_mfj": 500000,
    "sec121_note": "IRC 121: exclude up to $250,000 ($500,000 MFJ) of principal-residence gain if owned and used as main home 2 of the last 5 years; once per 2 years; depreciation after May 6, 1997 is not excludable.",
    "sec121_source": "https://www.irs.gov/publications/p523",
    "unrecaptured_1250_max_rate": 0.25,
    "unrecaptured_1250_source": "https://www.irs.gov/publications/p544",
    "niit_rate": 0.038,
    "niit_source": "https://www.irs.gov/individuals/net-investment-income-tax",
    "ltcg_rates_note": "Long-term capital gains 0/15/20% federal brackets (Rev. Proc. 2025-32 for 2026) plus 3.8% NIIT above the statutory thresholds; California taxes gains as ordinary income (1% to 12.3%) plus the 1% behavioral-health tax above $1M taxable income.",
    "ltcg_source": "https://www.irs.gov/taxtopics/tc409",
    "ca_estate_tax_note": "California has no estate or inheritance tax return for deaths on or after Jan 1, 2005 under current law (State Controller). Law can change before a 2040-2050 transfer.",
    "ca_estate_tax_source": "https://www.sco.ca.gov/ardtax_estate_tax.html",
    "step_up_basis_note": "Inherited property basis is generally fair market value at date of death (IRC 1014); consistent-basis reporting rules (IRC 6035) apply when Form 706 is filed.",
    "step_up_basis_source": "https://www.irs.gov/faqs/interest-dividends-other-types-of-income/gifts-inheritances/gifts-inheritances",
    "treasury_date": "2026-11-25",
    "treasury_3mo": 4.34,
    "treasury_1yr": 4.56,
    "treasury_2yr": 4.61,
    "treasury_source": "https://home.treasury.gov/resource-center/data-chart-center/interest-rates",
    "hud_fmr_3br_scc_fy2026": 4602,
    "hud_fmr_note": "HUD Fair Market Rent, Santa Clara County FY2026, 3-bedroom (voucher benchmark and rent-path FLOOR, not a property appraisal). Confirm at the official HUD FMR data tool before use.",
    "hud_fmr_source": "https://www.huduser.gov/portal/datasets/fmr.html",
    "sb284_status": "PROPOSAL - not law. SB 284 (2025-2026) would amend RTC 63.2 (Prop 19 family-home transfers); active bill, held in committee and under submission (last action July 14, 2025). Do not model as current law.",
    "sb284_source": "https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260SB284",
}

# ---------------------------------------------------------------------------
# Household-derived planning inputs (rounded to $10 for publication)
# ---------------------------------------------------------------------------
P = {
    "A": {
        "label": "Property A - inherited home (Santa Clara County city)",
        "role": "Expected to transfer by trust in the 2040-2050 window; not owned by Owner B before transfer",
        "value_2026_low": 2950000,
        "value_2026_base": 3100000,
        "value_2026_high": 3250000,
        "assessed_2026": 550540,
        "tax_2026": 7210,
        "water_monthly": [100, 130, 150],
        "electricity_net_monthly": [-20, -15, 0],
        "insurance_annual": [1500, 2600, 4500],
        "maintenance_pct": [0.005, 0.008, 0.012],
        "capital_reserve_pct": 0.005,
        "prop19_eligibility": "UNVERIFIED - requires eligible transferee, transferor principal-residence status, occupancy intent, exemption filing within 1 year, claim within 3 years.",
        "market_rent_monthly": [4600, 5900, 7200],
        "market_rent_note": "LOW = HUD FMR 3-bedroom floor (official benchmark). BASE/HIGH = planning estimates pending independent comparable-rent evidence (unverified, flagged).",
    },
    "B": {
        "label": "Property B - already-owned multi-unit home (San Francisco)",
        "role": "Already owned by Owner B; 3 livable units, 2 rented; Owner B can occupy as primary residence without losing rental income",
        "value_2026_low": 1700000,
        "value_2026_base": 1800000,
        "value_2026_high": 1900000,
        "assessed_2025": 114250,
        "tax_2025": 2440,
        "gross_rent_monthly": [6800, 7150, 7500],
        "water_monthly": [330, 360, 400],
        "electricity_monthly": [30, 50, 70],
        "insurance_annual": [1500, 2600, 4500],
        "maintenance_pct": [0.010, 0.013, 0.018],
        "vacancy_pct": [0.04, 0.06, 0.08],
        "management_pct": [0.0, 0.04, 0.08],
        "prop_h_annual": 250,
        "leases_review": "UNVERIFIED - unit count legality, Rent Board registration, AB 1482 applicability, owner-move-in rules need document review.",
        "depreciation_history": "UNKNOWN - CPA must rebuild accumulated depreciation before modeling recapture (planning range used below, flagged).",
        "depreciation_total_range": [20000, 40000, 60000],
    },
}

SCEN = {
    "appreciation": {"low": 0.020, "base": 0.035, "high": 0.055},
    "inflation": {"low": 0.020, "base": 0.028, "high": 0.040},
    "stock_nominal": {"low": 0.050, "base": 0.070, "high": 0.090},
    "treasury_parking": {"low": 0.020, "base": 0.045, "high": 0.055},
    "commission_rate": {"low": 0.04, "base": 0.05, "high": 0.06},
    "rent_growth": {"low": 0.02, "base": 0.03, "high": 0.04},
    "insurance_growth": {"low": 0.03, "base": 0.05, "high": 0.08},
    "allowance_growth_per_year": {"low": 0.005, "base": 0.011, "high": 0.03},
    "exclusion_indexing": {"low": 0.02, "base": 0.025, "high": 0.03},
}

SALE_COSTS = {
    "A_other_close_cost_base": 9000,
    "A_other_close_cost_range": [6000, 9000, 14000],
    "B_other_close_cost_base": 6000,
    "B_other_close_cost_range": [4000, 6000, 10000],
    "taxes_on_immediate_sale_note": "Same-tax-year sale after inheritance: basis steps to date-of-death value, so realized gain is approximately zero net of selling costs (modeling range $0-$150,000 if value moves between death and closing). Federal LTCG 15-23.8% + CA ordinary 9.3-13.3% would apply only to any realized gain.",
}

def scc_tax(assessed):
    return assessed * ANCHORS["scc_typical_tra_total"] + ANCHORS["scc_fixed_charges_annual_base"]

def sf_transfer_tax(value):
    for b in ANCHORS["sf_transfer_tax_schedule"]:
        if b["high"] is None or value < b["high"]:
            return math.ceil(value / 500.0) * b["per_500"]
    return 0.0

def scc_transfer_tax(value):
    return math.ceil(value / 500.0) * ANCHORS["scc_transfer_tax_per_500"]

# ---------------------------------------------------------------------------
# Transfer-year projections (base case, from 2026)
# ---------------------------------------------------------------------------
YEARS_TO_TRANSFER = {2040: 14, 2045: 19, 2050: 24}

def transfer_table():
    rows = []
    for year, dy in YEARS_TO_TRANSFER.items():
        a_val = {k: fv(P["A"]["value_2026_" + k], SCEN["appreciation"][k], dy) for k in ("low", "base", "high")}
        b_val = {k: fv(P["B"]["value_2026_" + k], SCEN["appreciation"][k], dy) for k in ("low", "base", "high")}
        allowance = {k: ANCHORS["prop19_allowance_2025_2027"] * (1 + SCEN["allowance_growth_per_year"][k]) ** dy for k in ("low", "base", "high")}
        exclusion = {k: ANCHORS["federal_estate_exclusion_2026"] * (1 + SCEN["exclusion_indexing"][k]) ** dy for k in ("low", "base", "high")}
        a_assessed_live = {k: max(P["A"]["assessed_2026"] * (1.02) ** dy, a_val[k] - allowance[k]) for k in ("low", "base", "high")}
        a_assessed_no = a_val
        tax_live = {k: scc_tax(a_assessed_live[k]) for k in ("low", "base", "high")}
        tax_no = {k: scc_tax(a_assessed_no[k]) for k in ("low", "base", "high")}
        rent_base_year = {k: P["A"]["market_rent_monthly"][i] * (1 + SCEN["rent_growth"]["base"]) ** dy for i, k in enumerate(("low", "base", "high"))}
        rows.append({
            "year": year,
            "years_from_2026": dy,
            "A_value": {k: r10(a_val[k]) for k in ("low", "base", "high")},
            "B_value": {k: r10(b_val[k]) for k in ("low", "base", "high")},
            "prop19_allowance_projected": {k: r10(allowance[k]) for k in ("low", "base", "high")},
            "A_assessed_if_prop19_live": {k: r10(a_assessed_live[k]) for k in ("low", "base", "high")},
            "A_property_tax_if_live_prop19": {k: r10(tax_live[k]) for k in ("low", "base", "high")},
            "A_assessed_if_rented_or_sold_hold": {k: r10(a_assessed_no[k]) for k in ("low", "base", "high")},
            "A_property_tax_if_no_exclusion": {k: r10(tax_no[k]) for k in ("low", "base", "high")},
            "A_market_rent_monthly_projected": {k: r10(rent_base_year[k]) for k in ("low", "base", "high")},
            "federal_exclusion_projected": {k: r10(exclusion[k]) for k in ("low", "base", "high")},
            "notes": "Assessed values and allowance are projections with 2%/yr Prop 13 escalation and stated allowance growth; official figures only exist at the actual transfer date.",
        })
    return rows

# ---------------------------------------------------------------------------
# Sale-cost and proceeds math
# ---------------------------------------------------------------------------
def sale_math_A(value_base, comm):
    commission = value_base * comm
    dtt = scc_transfer_tax(value_base)
    recording = ANCHORS["scc_recording_first_page"] + 3 * 8 + 10
    other = SALE_COSTS["A_other_close_cost_base"]
    net = value_base - commission - dtt - recording - other
    return {
        "gross_value": r10(value_base),
        "commission": r10(commission),
        "county_transfer_tax": r10(dtt),
        "recording_fees": r10(recording),
        "escrow_title_prep": r10(other),
        "net_proceeds_before_tax": r10(net),
        "note": "Immediate-sale capital gain approximately $0 (stepped-up basis = date-of-death value, modeled sale in the same tax year as inheritance). Any basis/selling-cost mismatch is taxed federally at 15-23.8% and in California as ordinary income; the 1% behavioral-health tax applies to California taxable income above $1,000,000.",
    }

def sale_math_B(value_base, comm):
    commission = value_base * comm
    dtt = sf_transfer_tax(value_base)
    other = SALE_COSTS["B_other_close_cost_base"]
    recapture = P["B"]["depreciation_total_range"][1] * ANCHORS["unrecaptured_1250_max_rate"]
    net = value_base - commission - dtt - other
    return {
        "gross_value": r10(value_base),
        "commission": r10(commission),
        "sf_transfer_tax": r10(dtt),
        "recording_fees": 300,
        "escrow_title_prep": r10(other),
        "est_federal_recapture_tax_base": r10(recapture),
        "net_proceeds_before_tax": r10(net),
        "note": "SF transfer tax bracket (0.75% for $1M-$5M) applies to the entire value. Depreciation-recapture estimate uses the mid planning range because actual depreciation history is unknown (flagged).",
    }

# ---------------------------------------------------------------------------
# Path comparison at identical transfer dates and horizons
# ---------------------------------------------------------------------------
HORIZONS = [5, 10, 20, 30]

def path_results(year=2045, dy=19):
    out = {}
    a_val_b = fv(P["A"]["value_2026_base"], SCEN["appreciation"]["base"], dy)
    a_val_lo = fv(P["A"]["value_2026_low"], SCEN["appreciation"]["low"], dy)
    a_val_hi = fv(P["A"]["value_2026_high"], SCEN["appreciation"]["high"], dy)
    net_sale = {
        "low": a_val_lo * (1 - SCEN["commission_rate"]["high"]) - scc_transfer_tax(a_val_lo) - SALE_COSTS["A_other_close_cost_range"][2] - 200,
        "base": a_val_b * (1 - SCEN["commission_rate"]["base"]) - scc_transfer_tax(a_val_b) - SALE_COSTS["A_other_close_cost_base"] - 160,
        "high": a_val_hi * (1 - SCEN["commission_rate"]["low"]) - scc_transfer_tax(a_val_hi) - SALE_COSTS["A_other_close_cost_range"][0] - 130,
    }
    liquid_cash_base = 1500000  # planning placeholder for other inherited cash (Owner B to confirm)
    investable = {k: net_sale[k] + liquid_cash_base for k in ("low", "base", "high")}

    allowance = ANCHORS["prop19_allowance_2025_2027"] * (1 + SCEN["allowance_growth_per_year"]["base"]) ** dy
    assessed_live = max(P["A"]["assessed_2026"] * 1.02 ** dy, a_val_b - allowance)
    tax_live = scc_tax(assessed_live)
    assessed_rent = a_val_b
    tax_rent = scc_tax(assessed_rent)
    rent_annual = P["A"]["market_rent_monthly"][1] * 12 * (1 + SCEN["rent_growth"]["base"]) ** dy
    ins_hi = P["A"]["insurance_annual"][1] * (1 + SCEN["insurance_growth"]["base"]) ** dy
    util_annual = (P["A"]["water_monthly"][1] + P["A"]["electricity_net_monthly"][1]) * 12
    maint = a_val_b * P["A"]["maintenance_pct"][1]
    reserve = a_val_b * P["A"]["capital_reserve_pct"]
    imputed_rent = rent_annual
    stock = SCEN["stock_nominal"]["base"]
    treas = SCEN["treasury_parking"]["base"]

    def invest_terminal(p0, r, h):
        return p0 * (1 + r) ** h

    # Path 1: live at A (Prop 19), B unchanged
    live_annual_cost = tax_live + ins_hi + util_annual + maint + reserve
    live_net_benefit = imputed_rent - live_annual_cost
    out["live_prop19"] = {
        "label": "Live in inherited home (Prop 19 claimed, long-term occupancy)",
        "annual_carrying_cost_base": r10(live_annual_cost),
        "annual_imputed_rent_base": r10(imputed_rent),
        "annual_net_benefit_base": r10(live_net_benefit),
        "property_tax_base": r10(tax_live),
        "terminal_household_value_base": r10(a_val_b + invest_terminal(liquid_cash_base, stock, 30)),
        "risks": "Concentration in one asset; property-tax jump even with Prop 19; insurance/UA risk; lifestyle value not monetized; Prop 19 filing windows (exemption within 1 year, claim within 3 years).",
    }
    # Path 2: rent A (no Prop 19)
    mgmt = rent_annual * P["B"]["management_pct"][1]
    vacancy = rent_annual * P["B"]["vacancy_pct"][1]
    noi_rent = rent_annual - mgmt - vacancy - tax_rent - ins_hi - util_annual - maint - reserve
    out["rent"] = {
        "label": "Rent inherited home (no Prop 19 exclusion without occupancy)",
        "gross_rent_annual_base": r10(rent_annual),
        "property_tax_base": r10(tax_rent),
        "noi_annual_base": r10(noi_rent),
        "noi_yield_pct": pct(noi_rent / a_val_b),
        "terminal_household_value_base": r10(a_val_b + invest_terminal(liquid_cash_base, stock, 30) + sum(noi_rent * (1.028) ** i for i in range(30))),
        "risks": "Reassessment to full market value on transfer; NOI is thin because the reassessed tax approaches 1.15% of value; tenant/vacancy risk; depreciation record-keeping for eventual recapture.",
    }
    # Path 3: sell immediately, invest lump sum
    out["sell_invest"] = {
        "label": "Sell in the same tax year as inheritance; invest net proceeds (lump sum)",
        "net_proceeds": {k: r10(net_sale[k]) for k in ("low", "base", "high")},
        "investable": {k: r10(investable[k]) for k in ("low", "base", "high")},
        "terminal_invested_base_30y": r10(invest_terminal(investable["base"], stock, 30)),
        "capital_gain_same_year": "approximately $0",
        "risks": "Sequence/entry risk: a crash immediately after investing hits the whole amount; concentration and behavioral risk of a lump sum.",
    }
    # Path 4: sell, phase into stocks over 24-36 months from 3M-2Y Treasuries
    def phased_terminal(h, months=30):
        inv = investable["base"]
        invested_value = 0.0
        cash = inv
        monthly_invest = inv / months
        for m in range(1, h * 12 + 1):
            # accrue returns
            cash *= (1 + treas) ** (1 / 12.0)
            invested_value *= (1 + stock) ** (1 / 12.0)
            if m <= months:
                buy = min(monthly_invest, cash)
                cash -= buy
                invested_value += buy
        return invested_value + cash

    out["sell_phased"] = {
        "label": "Sell; park in 3M-2Y Treasuries for 24-36 months; phase into stocks",
        "phase_months_options": [24, 30, 36],
        "parking_yield_pct": pct(treas),
        "parking_yield_note": "U.S. Treasury par yield curve Nov. 25, 2026: 3-month 4.34%, 1-year 4.56%, 2-year 4.61%. Parking yield is NOT locked; each maturity reinvests at then-current rates (reinvestment risk).",
        "terminal_invested_base_30y": r10(phased_terminal(30, 30)),
        "terminal_lump_base_30y": r10(invest_terminal(investable["base"], stock, 30)),
        "phase_vs_lump_delta_30y_base": r10(phased_terminal(30, 30) - invest_terminal(investable["base"], stock, 30)),
        "risks": "Cash drag and reinvestment risk (yields reset at each T-bill maturity); upside missed if markets rise during the phase; taxes on Treasury interest in California at ordinary rates.",
    }
    # Path 5: mixed - live N years then sell (uses sec 121); proceeds compound for the remaining horizon
    g121 = ANCHORS["sec121_exclusion_mfj"]
    live_years = 3
    a_val_sell_year = a_val_b * (1.035) ** live_years
    gain_live_sell = a_val_sell_year * 0.95 - (a_val_b)  # costs at future sale, basis = DOD FMV
    taxable_gain = max(0.0, gain_live_sell - g121)
    fed = taxable_gain * 0.20 + taxable_gain * ANCHORS["niit_rate"]
    ca = taxable_gain * 0.123 + (taxable_gain * ANCHORS["ftb_line62_1pct_over_1m"] if taxable_gain > ANCHORS["ftb_line62_threshold"] else 0)
    proceeds_after_tax = a_val_sell_year * 0.95 - fed - ca
    flows_live = sum((imputed_rent - live_annual_cost) * (1 + SCEN["inflation"]["base"]) ** i for i in range(live_years))
    net_after_tax = proceeds_after_tax * (1 + stock) ** (30 - live_years) + liquid_cash_base * (1 + stock) ** 30 + flows_live
    out["live_then_sell"] = {
        "label": "Mixed: live 3 years, then sell (IRC 121 exclusion applied)",
        "assumed_future_sale_value_base": r10(a_val_sell_year),
        "realized_gain_before_exclusion_base": r10(gain_live_sell),
        "sec121_exclusion_applied": r10(g121),
        "est_federal_tax_base": r10(fed),
        "est_california_tax_base": r10(ca),
        "net_after_tax_base_30y_terminal": r10(net_after_tax),
        "filing_status_note": "$500,000 exclusion assumes married filing jointly and 2-of-5-year ownership+use; $250,000 if single. Verify with CPA; depreciation after May 6, 1997 is not excludable.",
        "risks": "Gain accrues after the step-up year; Prop 19 eligibility must hold during occupancy; market risk during the live period; sale costs repeat.",
    }
    # Path 6: rent then sell (5 years) with recapture on rental-period depreciation; proceeds compound after sale
    rent_years = 5
    a_val_rent_sell = a_val_b * (1.035) ** rent_years
    dep_during_rental = a_val_b * 0.0025 * rent_years  # planning structure depreciation ~0.25%/yr of improvement value
    gain_rent_sell = a_val_rent_sell * 0.95 - a_val_b
    unrecap = min(dep_during_rental, gain_rent_sell)
    fed2 = unrecap * 0.25 + (gain_rent_sell - unrecap) * 0.20 + gain_rent_sell * ANCHORS["niit_rate"]
    ca2 = gain_rent_sell * 0.123 + (gain_rent_sell * ANCHORS["ftb_line62_1pct_over_1m"] if gain_rent_sell > ANCHORS["ftb_line62_threshold"] else 0)
    proceeds_rent_sell = a_val_rent_sell * 0.95 - fed2 - ca2
    flows_rent = sum(noi_rent * (1.028) ** i for i in range(rent_years))
    net_rent_sell = proceeds_rent_sell * (1 + stock) ** (30 - rent_years) + liquid_cash_base * (1 + stock) ** 30 + flows_rent
    out["rent_then_sell"] = {
        "label": "Mixed: rent 5 years, then sell (depreciation recapture modeled)",
        "assumed_future_sale_value_base": r10(a_val_rent_sell),
        "planning_depreciation_during_rental": r10(dep_during_rental),
        "est_unrecaptured_1250_tax_base": r10(unrecap * 0.25),
        "est_federal_gain_tax_base": r10(fed2),
        "est_california_tax_base": r10(ca2),
        "net_after_tax_plus_noi_base_30y_terminal": r10(net_rent_sell),
        "risks": "Reassessment immediately on transfer (no occupancy); depreciation accrues recapture; thin NOI; tenant risk; future-law risk on both taxes.",
    }
    out["_params"] = {
        "year": year, "years_from_2026": dy,
        "A_value_base": r10(a_val_b), "A_value_low": r10(a_val_lo), "A_value_high": r10(a_val_hi),
        "prop19_allowance_base": r10(allowance),
        "assessed_live_base": r10(assessed_live),
        "assessed_rent_base": r10(assessed_rent),
        "net_sale_proceeds": {k: r10(net_sale[k]) for k in ("low", "base", "high")},
        "liquid_cash_placeholder": r10(liquid_cash_base),
        "investable": {k: r10(investable[k]) for k in ("low", "base", "high")},
    }
    return out

# ---------------------------------------------------------------------------
# Black swan module: regime anchors + phased-investing crash tests
# ---------------------------------------------------------------------------
BLACK_SWAN_REGIMES = [
    {"name": "1929-style deflationary depression", "equity_peak_to_trough": -0.89, "duration": "Sep 1929 - Jul 1932 (DJIA price basis)", "inflation": "CPI fell about 25% cumulatively 1930-1932 (deflation)", "rate_behavior": "Short rates fell toward zero; cash/Treasuries gained real purchasing power", "property_effect": "Nominal home prices fell broadly; deflation raised real debt burdens", "sources": ["https://fred.stlouisfed.org/series/DJIA", "https://www.nber.org/research/business-cycle-dating", "https://www.bls.gov/cpi/"], "basis_note": "Price-index decline computed from public DJIA levels; not a total-return series."},
    {"name": "1970s stagflation", "equity_peak_to_trough": -0.48, "duration": "Jan 1973 - Oct 1974 (S&P 500 price basis)", "inflation": "CPI annual averages 11.3% (1979), 13.5% (1980), 10.3% (1981)", "rate_behavior": "Short yields above 10% by 1979-1981; T-bills lost real value most years", "property_effect": "Nominal values eventually rose with inflation but real returns were uneven", "sources": ["https://fred.stlouisfed.org/series/SP500", "https://www.bls.gov/cpi/"], "basis_note": "Peak-to-trough price decline computed from public index levels."},
    {"name": "2000-2002 dot-com bust", "equity_peak_to_trough": -0.49, "duration": "Mar 2000 - Oct 2002 (S&P 500 price basis)", "inflation": "Low single digits; deflation scare in 2002", "rate_behavior": "Fed funds cut from 6.5% to 1.0% (2001-2003); parking yields collapsed", "property_effect": "Bay Area home prices kept rising through most of the bust; concentration cut both ways", "sources": ["https://fred.stlouisfed.org/series/SP500", "https://www.federalreserve.gov/monetarypolicy/openmarket.htm"], "basis_note": "Price-basis decline; Bay Area housing outperformance was regime-specific and may not repeat."},
    {"name": "2008 global financial crisis", "equity_peak_to_trough": -0.57, "duration": "Oct 2007 - Mar 2009 (S&P 500 price basis)", "inflation": "3.8% (2008 CPI), -0.3% (2009)", "rate_behavior": "3-month T-bill yield collapsed from about 5% to near zero - parking yield reset downward each maturity (reinvestment risk in action)", "property_effect": "National home prices fell roughly 27% peak-to-trough (Case-Shiller national); both assets fell together", "sources": ["https://fred.stlouisfed.org/series/SP500", "https://fred.stlouisfed.org/series/DTB3", "https://www.federalreservehistory.org/essays/great-recession-and-its-aftermath"], "basis_note": "Equity decline computed from public index levels; home-price figure is a public index anchor, not a parcel estimate."},
    {"name": "2022 rate shock", "equity_peak_to_trough": -0.25, "duration": "Jan 2022 - Oct 2022 (S&P 500 price basis)", "inflation": "8.0% CPI average (2022)", "rate_behavior": "Both stocks AND bonds fell (worst Treasury year in decades) - parking was not safe either", "property_effect": "Mortgage rates above 7% froze transaction volume; values stagnated", "sources": ["https://fred.stlouisfed.org/series/SP500", "https://home.treasury.gov/resource-center/data-chart-center/interest-rates", "https://www.bls.gov/cpi/"], "basis_note": "Demonstrates that short-Treasury parking carries rate risk, not just equity risk."},
    {"name": "Lost decade / Japan-style stagnation", "equity_peak_to_trough": None, "duration": "2000-2009 S&P 500 total-return CAGR approximately -1%/yr; Japan Nikkei below 1989 peak for 34+ years", "inflation": "2000s US ~2.6%; Japan deflationary for decades", "rate_behavior": "Zero interest rate policy for years - parking yield near zero", "property_effect": "Japanese home land prices fell for years; US 2000s decade Case-Shiller roughly flat-to-down in real terms", "sources": ["https://fred.stlouisfed.org/series/SP500", "https://fred.stlouisfed.org/series/NIKKEI225"], "basis_note": "CAGR computed from public series; index basis labeled per source."},
]

def phased_tests():
    # Use the base-case investable amount from the 2045 path math for consistency
    inv = 7141300
    tests = []
    stock = SCEN["stock_nominal"]["base"]
    treas = SCEN["treasury_parking"]["base"]

    def sim(crash_y, cp, phase, h=30):
        cash = inv if phase else 0.0
        invested = 0.0 if phase else inv
        mi = inv / phase if phase else 0.0
        for m in range(1, h * 12 + 1):
            cash *= (1 + treas) ** (1 / 12.0)
            invested *= (1 + stock) ** (1 / 12.0)
            if crash_y and m == crash_y * 12:
                invested *= (1 - cp)
            if phase and m <= phase:
                buy = min(mi, cash)
                cash -= buy
                invested += buy
        return invested + cash

    for months in (24, 30, 36):
        for crash_year, crash_pct in ((0, 0.0), (1, 0.50), (2, 0.50), (3, 0.40), (1, 0.89)):
            lump = sim(crash_year if crash_year else None, crash_pct, 0)
            ph = sim(crash_year if crash_year else None, crash_pct, months)
            tests.append({
                "phase_months": months,
                "crash_year": crash_year if crash_year else "none",
                "crash_pct": pct(crash_pct, 0),
                "lump_terminal": r10(lump),
                "phased_terminal": r10(ph),
                "phased_minus_lump": r10(ph - lump),
                "note": "Identical monthly simulation for both legs (7.0% stock return base, 4.5% parking yield held constant, crash applied at the same month to invested balances only). Entry-timing test, not a forecast; real crises change yields and inflation.",
            })
    return {"parking_amount_planning": r10(inv), "tests": tests}


# ---------------------------------------------------------------------------
# Five-year capital plans (rounded to $10; flagged as estimates pending bids)
# ---------------------------------------------------------------------------
CAPITAL_PLAN_A = [
    {"item": "Roof inspection / partial repair reserve", "years": "1-2", "low": 2000, "base": 6000, "high": 15000, "verified": False},
    {"item": "Water heater replacement", "years": "1-5", "low": 2000, "base": 3000, "high": 5000, "verified": False},
    {"item": "HVAC service or replacement (if aging)", "years": "1-5", "low": 500, "base": 9000, "high": 18000, "verified": False},
    {"item": "Solar system inspection / inverter reserve", "years": "1-3", "low": 300, "base": 2000, "high": 6000, "verified": False},
    {"item": "Exterior paint / drainage / landscape", "years": "1-5", "low": 3000, "base": 8000, "high": 20000, "verified": False},
    {"item": "Seismic / foundation review (if applicable)", "years": "1-2", "low": 800, "base": 4000, "high": 30000, "verified": False},
]
CAPITAL_PLAN_B = [
    {"item": "Roof (flat roof multi-unit risk)", "years": "1-5", "low": 8000, "base": 25000, "high": 60000, "verified": False},
    {"item": "Individual water heaters (per unit)", "years": "1-5", "low": 4000, "base": 9000, "high": 15000, "verified": False},
    {"item": "Sewer lateral / plumbing (SF requirement risk)", "years": "1-5", "low": 5000, "base": 15000, "high": 40000, "verified": False},
    {"item": "Seismic retrofit / soft-story review", "years": "1-5", "low": 5000, "base": 30000, "high": 100000, "verified": False},
    {"item": "Electrical panel / unit upgrades", "years": "1-5", "low": 3000, "base": 10000, "high": 30000, "verified": False},
    {"item": "Exterior paint / code items (DBI)", "years": "1-5", "low": 5000, "base": 20000, "high": 50000, "verified": False},
]

# ---------------------------------------------------------------------------
# Estate analysis
# ---------------------------------------------------------------------------
def estate_analysis():
    rows = []
    for year, dy in YEARS_TO_TRANSFER.items():
        a_val = fv(P["A"]["value_2026_base"], SCEN["appreciation"]["base"], dy)
        b_val = fv(P["B"]["value_2026_base"], SCEN["appreciation"]["base"], dy)
        excl = ANCHORS["federal_estate_exclusion_2026"] * (1 + SCEN["exclusion_indexing"]["base"]) ** dy
        for cash_label, cash in (("other inherited cash: $1,000,000 planning", 1000000), ("$3,000,000", 3000000), ("$8,000,000", 8000000), ("$15,000,000", 15000000)):
            gross = a_val + b_val + cash
            over = max(0.0, gross - excl)
            tax = over * 0.40
            rows.append({
                "transfer_year": year,
                "estate_A": r10(a_val), "estate_B": r10(b_val),
                "cash_scenario_label": cash_label, "cash": r10(cash),
                "gross_estate": r10(gross),
                "projected_exclusion": r10(excl),
                "estate_tax_if_over": r10(tax),
                "liquidity_plan_needed": tax > 0,
            })
    return rows

# ---------------------------------------------------------------------------
# Sensitivity / tornado: does the recommendation move?
# ---------------------------------------------------------------------------
def recommendation():
    # Base case ranking at 2045 over 30 years (pre-tax planning basis)
    dy = 19
    a_val_b = fv(P["A"]["value_2026_base"], SCEN["appreciation"]["base"], dy)
    net_sale = a_val_b * 0.95 - scc_transfer_tax(a_val_b) - 9000 - 160 + 1500000
    lump = net_sale * (1.07) ** 30
    phased = 0.0
    cash = net_sale; invested = 0.0; mi = net_sale / 30
    for m in range(1, 361):
        cash *= (1.045) ** (1 / 12.0); invested *= (1.07) ** (1 / 12.0)
        if m <= 30:
            buy = min(mi, cash); cash -= buy; invested += buy
        phased = invested + cash
    allowance = ANCHORS["prop19_allowance_2025_2027"] * 1.011 ** dy
    assessed_live = max(P["A"]["assessed_2026"] * 1.02 ** dy, a_val_b - allowance)
    tax_live = scc_tax(assessed_live)
    carry = tax_live + P["A"]["insurance_annual"][1] * 1.05 ** dy + (P["A"]["water_monthly"][1] + P["A"]["electricity_net_monthly"][1]) * 12 + a_val_b * (P["A"]["maintenance_pct"][1] + P["A"]["capital_reserve_pct"])
    imputed = P["A"]["market_rent_monthly"][1] * 12 * 1.03 ** dy
    live_w = a_val_b + 1500000 * 1.07 ** 30 + sum((imputed - carry) * 1.028 ** i for i in range(30))
    rent_annual = P["A"]["market_rent_monthly"][1] * 12 * 1.03 ** dy
    tax_rent = scc_tax(a_val_b)
    noi = rent_annual * (1 - 0.06 - 0.04) - tax_rent - P["A"]["insurance_annual"][1] * 1.05 ** dy - (P["A"]["water_monthly"][1] + P["A"]["electricity_net_monthly"][1]) * 12 - a_val_b * (P["A"]["maintenance_pct"][1] + P["A"]["capital_reserve_pct"])
    rent_w = a_val_b + 1500000 * 1.07 ** 30 + sum(noi * 1.028 ** i for i in range(30))
    ranked = [
        {"path": "Sell + phased reinvestment (24-36 months, 3M-2Y Treasuries)", "terminal_base_30y": r10(phased)},
        {"path": "Sell + immediate lump-sum reinvestment", "terminal_base_30y": r10(lump)},
        {"path": "Live in A (Prop 19) + invest other cash", "terminal_base_30y": r10(live_w)},
        {"path": "Rent A (no exclusion) + invest other cash", "terminal_base_30y": r10(rent_w)},
    ]
    ranked.sort(key=lambda x: -x["terminal_base_30y"])
    return {
        "as_of": "2026-11-25 model build; base case at 2045 transfer, 30-year horizon, pre-tax except noted taxes",
        "ranking": ranked,
        "headline": "Sell at transfer and reinvest (phased entry preferred for risk) dominates the keeping paths under base assumptions; live-in is a lifestyle choice with a quantifiable annual cost; renting A is structurally weak because reassessed property tax consumes most of the rent.",
        "quantified_gap": "Live-in vs sell-and-invest annual gap at 2045 base: about " + str(r10(investable_gap(dy))) + " per year in expected return difference (pre-tax).",
        "stability_note": "Re-run build_model.py after ANY input change; the ranking above is recomputed and compared in COORDINATION.md.",
    }

def investable_gap(dy):
    # Consistent 2045 basis: projected rent, insurance, and carrying costs
    a_val_b = fv(P["A"]["value_2026_base"], SCEN["appreciation"]["base"], dy)
    allowance = ANCHORS["prop19_allowance_2025_2027"] * 1.011 ** dy
    assessed_live = max(P["A"]["assessed_2026"] * 1.02 ** dy, a_val_b - allowance)
    tax_live = scc_tax(assessed_live)
    ins = P["A"]["insurance_annual"][1] * (1 + SCEN["insurance_growth"]["base"]) ** dy
    util = (P["A"]["water_monthly"][1] + P["A"]["electricity_net_monthly"][1]) * 12
    maint = a_val_b * (P["A"]["maintenance_pct"][1] + P["A"]["capital_reserve_pct"])
    carry = tax_live + ins + util + maint
    imputed = P["A"]["market_rent_monthly"][1] * 12 * (1 + SCEN["rent_growth"]["base"]) ** dy
    live_ret = a_val_b * 0.035 + imputed - carry
    invest_ret = (a_val_b * 0.95 - scc_transfer_tax(a_val_b)) * 0.07
    return invest_ret - live_ret

# ---------------------------------------------------------------------------
# Distribution chart data (illustrative percentiles per path, 30y, base case)
# ---------------------------------------------------------------------------
def distributions():
    # Parametric: low/base/high terminal values mapped to p10/p50/p90 (illustrative only)
    base = recommendation()["ranking"]
    out = []
    spread = 0.35
    for row in base:
        p50 = row["terminal_base_30y"]
        out.append({"path": row["path"], "p10": r10(p50 * (1 - spread)), "p50": p50, "p90": r10(p50 * (1 + spread))})
    return {"note": "Illustrative p10/p50/p90 from scenario spread (35% band around base) - not a Monte Carlo confidence interval; shows ranking and dispersion only.", "paths": out}

# ---------------------------------------------------------------------------
# Assemble model
# ---------------------------------------------------------------------------
model = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "as_of_date": "2026-11-25",
    "rounding_rule": "All published currency values rounded to the nearest $10 (owner instruction). Rates shown as percentages.",
    "privacy_rule": "Placeholders only (Property A, Property B, Owner B). No names, street addresses, ZIP codes, parcel/APN IDs, account numbers, or trust identifiers.",
    "anchors": ANCHORS,
    "properties": P,
    "scenarios": SCEN,
    "sale_costs": SALE_COSTS,
    "transfer_table": transfer_table(),
    "paths": path_results(),
    "black_swan": {"regimes": BLACK_SWAN_REGIMES, "phased_tests": phased_tests()},
    "capital_plan_A": CAPITAL_PLAN_A,
    "capital_plan_B": CAPITAL_PLAN_B,
    "estate_analysis": estate_analysis(),
    "recommendation": recommendation(),
    "distributions": distributions(),
    "sale_math_A": sale_math_A(fv(P["A"]["value_2026_base"], SCEN["appreciation"]["base"], 0), SCEN["commission_rate"]["base"]),
    "sale_math_A_2045": sale_math_A(fv(P["A"]["value_2026_base"], SCEN["appreciation"]["base"], 19), SCEN["commission_rate"]["base"]),
    "sale_math_B": sale_math_B(P["B"]["value_2026_base"], SCEN["commission_rate"]["base"]),
}

with open(os.path.join(DATA_DIR, "model.json"), "w") as f:
    json.dump(model, f, indent=1)

js = "window.TINO_MODEL = " + json.dumps(model, separators=(",", ":")) + ";\n"
with open(os.path.join(DATA_DIR, "model.js"), "w") as f:
    f.write(js)

print("Wrote data/model.json and data/model.js")
print("Recommendation ranking:", json.dumps(model["recommendation"]["ranking"], indent=1))
