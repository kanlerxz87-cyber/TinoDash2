#!/usr/bin/env python3
"""
TinoDash2 model builder — generates data/model.js (rounded to nearest $10).

Owner policy (2026-11-25): household-derived costs and figures ARE published on the
site, rounded to the nearest $10; personal identifiers (names, street addresses, ZIP
codes, parcel/APN IDs, account numbers, exact unrounded record values) are not.
All model outputs pass through r10(). Assumptions are labelled as assumptions; sourced
values carry source ids resolved against the site's source register.

Run: python3 scripts/build_model.py   ->  data/model.js
"""
from __future__ import annotations
import json, math, os
from datetime import datetime, timezone

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'companion', 'estate-pathways', 'data', 'model.js')

def r10(x):
    if x is None:
        return None
    from decimal import Decimal, ROUND_HALF_UP
    return int(Decimal(str(float(x) / 10)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)) * 10

def pct(x, nd=2):
    return round(x * 100, nd)

# ---------------------------------------------------------------------------
# 1. Core assumptions (ranges, not points). src ids map to pages/sources.html
# ---------------------------------------------------------------------------
ASSUMPTIONS = {
    "as_of": "2026-11-25",
    "rounding": "All currency values rounded to the nearest $10 (owner policy, 2026-11-25).",
    "property_a": {
        "value_2026_low": r10(2950000), "value_2026_base": r10(3100000), "value_2026_high": r10(3250000),
        "value_note": "Household estimate Nov 2026, rounded; independent appraisal unverified.",
        "appreciation_low": 2.0, "appreciation_base": 3.5, "appreciation_high": 5.5,
        "assessed_2026": r10(550540),
        "effective_tax_rate_low_pct": 1.18, "effective_tax_rate_base_pct": 1.33, "effective_tax_rate_high_pct": 1.48,
        "tax_rate_note": "Effective rate implied by household bill history (~1.33%), rounded inputs. TRA and direct assessments UNVERIFIED (flagged).",
        "water_mo_low": r10(100), "water_mo_base": r10(130), "water_mo_high": r10(150),
        "elec_net_mo_low": r10(-20), "elec_net_mo_base": r10(-15), "elec_net_mo_high": r10(0),
        "elec_note": "Solar credit: net monthly income of $10-$20 (rounded), household report; interconnection/NEM terms unverified.",
        "insurance_yr_low": r10(1200), "insurance_yr_base": r10(1800), "insurance_yr_high": r10(3600),
        "insurance_note": "No official premium dataset exists. Commercial quote aggregators show Santa Clara County averages of roughly $1,000-$1,300 (2025-26); a high-value replacement cost will price above county average. WRITTEN QUOTES REQUIRED (flagged).",
        "maint_yr_low": r10(9000), "maint_yr_base": r10(14000), "maint_yr_high": r10(22000),
        "capex_yr_low": r10(8000), "capex_yr_base": r10(12000), "capex_yr_high": r10(20000),
        "maint_note": "Dollar reserves (2026 money), escalated by inflation in flows. Property A upkeep is lighter than Property B per household report. Anchored to the five-year capital plan; inspection-backed bids required (flagged).",
        "market_rent_mo_low": r10(4600), "market_rent_mo_base": r10(5000), "market_rent_mo_high": r10(5800),
        "market_rent_note": "Anchored to HUD FY2026 Fair Market Rent, Santa Clara County 4BR $5,010 (rounded $5,010). FMR is a program benchmark, NOT a market appraisal; 3-5 comparables required (flagged).",
    },
    "property_b": {
        "value_2026_low": r10(1700000), "value_2026_base": r10(1800000), "value_2026_high": r10(1900000),
        "assessed_2025": r10(114250),
        "effective_tax_rate_low_pct": 1.98, "effective_tax_rate_base_pct": 2.13, "effective_tax_rate_high_pct": 2.28,
        "tax_rate_note": "Effective rate implied by household bill history (~2.13%), rounded inputs; SF direct assessments/TRA UNVERIFIED (flagged).",
        "rent_mo_low": r10(6800), "rent_mo_base": r10(7150), "rent_mo_high": r10(7500),
        "rent_note": "2 rented units, household-reported, rounded. Leases and rent status unverified (flagged).",
        "units_rented": 2, "units_livable": 3, "unit3_rent_mo_base": r10(3000),
        "unit3_note": "Third unit currently unrented; owner may occupy B without losing rental income. If owner lives in Property A, unit 3 could be rented (~$3,000/mo base) — LAWFUL-USE AND LEASE RULES UNVERIFIED (flagged).",
        "water_mo_low": r10(330), "water_mo_base": r10(360), "water_mo_high": r10(400),
        "elec_mo_low": r10(30), "elec_mo_base": r10(50), "elec_mo_high": r10(70),
        "insurance_yr_low": r10(1800), "insurance_yr_base": r10(2200), "insurance_yr_high": r10(3600),
        "insurance_note": "Landlord/dwelling-fire policy estimate; no official premium source (flagged).",
        "maint_yr_low": r10(12000), "maint_yr_base": r10(18000), "maint_yr_high": r10(28000),
        "capex_yr_low": r10(9000), "capex_yr_base": r10(14000), "capex_yr_high": r10(22000),
        "maint_note": "Three-unit building: heavier upkeep than Property A per household report. Dollar reserves (2026 money), escalated by inflation; inspection-backed bids required (flagged).",
        "vacancy_low": 3.0, "vacancy_base": 4.0, "vacancy_high": 7.0,
        "mgmt_pct": 0.0, "mgmt_note": "Owner-managed base case 0%; 5-8% if management hired.",
        "prop_h_annual": r10(250),
        "prop_h_note": "SF Proposition H (Nov 3, 2026, 'Stronger Muni for All') parcel tax: multifamily base $249/yr (+$0.195/sf over 5,000 sf, cap $50,000), FY2027-28 through FY2041-42, indexed from FY2028-29; first on fall 2027 secured bill. 65+ exemptions; <=50% pass-through to rent-controlled tenants (<= $65/unit/yr). Verify parcel area/type at SFMTA lookup (opens Dec 1, 2026).",
    },
    "macro": {
        "inflation_low": 2.0, "inflation_base": 2.8, "inflation_high": 4.0,
        "inflation_note": "Long-run US CPI has run ~2.5-3%/yr; Fed Dec-2025 SEP medians PCE 2.4% (2026), 2.1% (2027), 2.0% long run. 50-year history is NOT consistent (1970s ~7%, 2010s ~1.8%).",
        "stock_nom_low": 5.0, "stock_nom_base": 7.0, "stock_nom_high": 9.0,
        "stock_note": "S&P 500 total return 1926-2025 averaged ~10.5%/yr nominal, ~7.3%/yr real (officialdata/Damodaran). Future decades differ: 1930s ~-5%/yr, 2000s ~-1%/yr. Model base deliberately below long-run average.",
        "tbill_low": 2.0, "tbill_base": 3.5, "tbill_high": 5.0,
        "tbill_note": "Nov 2026 curve approx: 3M ~4.3%, 2Y ~4.6%, 10Y ~4.9-5.1% (Treasury daily par yields). Yields reset at each maturity = reinvestment risk. Not a forecast of 2040-2050.",
    },
    "tax": {
        "federal_estate_exclusion_2026": r10(15000000),
        "federal_estate_exclusion_note": "Basic exclusion amount CY2026 = $15,000,000 (P.L. 119-21, Working Families Tax Cuts; IRS). Indexed from 2027 by chained CPI — future amounts UNPUBLISHED (flagged).",
        "annual_gift_exclusion_2026": r10(19000),
        "annual_gift_note": "$19,000 for 2026 per IRS annual exclusion table — verify at irs.gov before use (secondary-sourced only in prior sessions; flagged).",
        "federal_estate_top_rate": 40.0,
        "ltcg_top": 20.0, "niit": 3.8,
        "ca_top_marginal": 12.3, "ca_bhs_surtax": 1.0, "ca_bhs_threshold": r10(1000000),
        "ca_bhs_note": "Form 540 line 62 (Behavioral Health Services Tax, renamed for TY2025+): 1% of CA taxable income over $1,000,000 (Form 540 line 19 less $1,000,000 x 1%), whole dollars, NOT indexed. CA taxes capital gain as ordinary income (no preferential rate). Confirm line number in filing-year booklet.",
        "ca_estate_tax": "None for deaths on/after Jan 1, 2005 (CA State Controller). Recheck law at death.",
        "prop19_amount": r10(1044586),
        "prop19_note": "Prop 19 family-home value cap = factored base-year value + $1,044,586 for transfers Feb 16, 2025-Feb 15, 2027 (BOE LTA 2025/009; adjusted every other Feb 16 by FHFA CA HPI; prior: $1,022,600 / $1,000,000). Next adjustment Feb 2027. Amount at a 2040-2050 transfer is UNKNOWN.",
        "prop13_cap": 2.0,
        "sec121_single": r10(250000), "sec121_mfj": r10(500000),
        "sec121_note": "IRC 121: $250,000/$500,000 gain exclusion if ownership + use as principal residence 2 of last 5 years. Inherited property: holding period is automatic (IRC 1223), use test is not.",
        "depreciation_years": 27.5,
        "unrecaptured_1250_rate": 25.0,
        "scc_dtt_rate_pct": 0.11,
        "scc_dtt_note": "Santa Clara County documentary transfer tax $0.55 per $500 (0.11%, R&T 11911). NO additional Cupertino city transfer tax identified — confirm before sale (flagged). In many Northern California counties the buyer customarily pays DTT; modeled conservatively as a seller cost.",
        "sf_transfer_tax_note": "SF real-property transfer tax is tiered (2020 Prop I: 5.5% $10M-$25M, 6% >=$25M on the ENTIRE price; lower tiers on sf.gov). 2026 legislative flux (BUILD Act cut; Nov 2026 Prop I allocation measure). OFFICIAL RATE SCHEDULE UNVERIFIED in this session (sf.gov fetch failed) — obtain from SF Treasurer immediately before any Property B sale (flagged).",
    },
}

# ---------------------------------------------------------------------------
# 2. Rounded history (household records, rounded to $10; % changes as provided)
# ---------------------------------------------------------------------------
PROPERTY_A_HISTORY = [
    {"year": 2026, "taxes": None, "assessed": r10(550540), "note": "taxes not provided"},
    {"year": 2025, "taxes": r10(7210), "assessed": r10(539740)},
    {"year": 2024, "taxes": r10(7000), "assessed": r10(529160)},
    {"year": 2023, "taxes": r10(6920), "assessed": r10(518790)},
    {"year": 2022, "taxes": r10(6760), "assessed": r10(508610)},
    {"year": 2021, "taxes": r10(6660), "assessed": r10(498640)},
    {"year": 2020, "taxes": r10(6570), "assessed": r10(493540)},
    {"year": 2019, "taxes": r10(6570), "assessed": r10(483850)},
    {"year": 2018, "taxes": r10(6380), "assessed": r10(474370)},
    {"year": 2017, "taxes": r10(6380), "assessed": r10(465070)},
    {"year": 2016, "taxes": r10(6410), "assessed": r10(455950)},
    {"year": 2015, "taxes": r10(6140), "assessed": r10(449100)},
    {"year": 2014, "taxes": r10(5970), "assessed": r10(440310)},
]
PROPERTY_B_HISTORY = [
    {"year": 2025, "taxes": r10(2440), "assessed": r10(114250)},
    {"year": 2024, "taxes": r10(2320), "assessed": r10(112010)},
    {"year": 2023, "taxes": r10(2180), "assessed": r10(109810)},
    {"year": 2022, "taxes": r10(2110), "assessed": r10(107660)},
    {"year": 2021, "taxes": r10(2070), "assessed": r10(105600)},
    {"year": 2020, "taxes": r10(2200), "assessed": r10(104510)},
    {"year": 2019, "taxes": r10(2130), "assessed": r10(102470)},
    {"year": 2018, "taxes": r10(2060), "assessed": r10(100460)},
    {"year": 2017, "taxes": r10(1750), "assessed": r10(98490)},
    {"year": 2016, "taxes": r10(1680), "assessed": r10(96560)},
]

# ---------------------------------------------------------------------------
# 3. Projections: value / assessed / tax / costs, low-base-high, to 2060
# ---------------------------------------------------------------------------
def project(year_from=2026, year_to=2060):
    rows = []
    a, b = ASSUMPTIONS["property_a"], ASSUMPTIONS["property_b"]
    for y in range(year_from, year_to + 1):
        n = y - 2026
        def fv(v, r): return v * ((1 + r / 100) ** n)
        row = {
            "year": y,
            "a_value": {"low": r10(fv(a["value_2026_low"], a["appreciation_low"])),
                        "base": r10(fv(a["value_2026_base"], a["appreciation_base"])),
                        "high": r10(fv(a["value_2026_high"], a["appreciation_high"]))},
            "a_assessed": r10(a["assessed_2026"] * (1.02 ** n)),
            "a_tax": {"low": r10(a["assessed_2026"] * (1.02 ** n) * a["effective_tax_rate_low_pct"] / 100),
                      "base": r10(a["assessed_2026"] * (1.02 ** n) * a["effective_tax_rate_base_pct"] / 100),
                      "high": r10(a["assessed_2026"] * (1.02 ** n) * a["effective_tax_rate_high_pct"] / 100)},
            "a_opex": {"low": r10(a["insurance_yr_low"] + 12 * (a["water_mo_low"] + a["elec_net_mo_low"])
                                  + (a["maint_yr_low"] + a["capex_yr_low"]) * ((1.028) ** n)),
                       "base": r10(a["insurance_yr_base"] + 12 * (a["water_mo_base"] + a["elec_net_mo_base"])
                                   + (a["maint_yr_base"] + a["capex_yr_base"]) * ((1.028) ** n)),
                       "high": r10(a["insurance_yr_high"] + 12 * (a["water_mo_high"] + a["elec_net_mo_high"])
                                   + (a["maint_yr_high"] + a["capex_yr_high"]) * ((1.04) ** n))},
            "b_value": {"low": r10(fv(b["value_2026_low"], a["appreciation_low"])),
                        "base": r10(fv(b["value_2026_base"], a["appreciation_base"])),
                        "high": r10(fv(b["value_2026_high"], a["appreciation_high"]))},
            "b_assessed": r10(b["assessed_2025"] * (1.02 ** max(0, y - 2025))),
            "b_tax": {"low": r10(b["assessed_2025"] * (1.02 ** max(0, y - 2025)) * b["effective_tax_rate_low_pct"] / 100),
                      "base": r10(b["assessed_2025"] * (1.02 ** max(0, y - 2025)) * b["effective_tax_rate_base_pct"] / 100),
                      "high": r10(b["assessed_2025"] * (1.02 ** max(0, y - 2025)) * b["effective_tax_rate_high_pct"] / 100)},
            "b_opex": {"low": r10(b["insurance_yr_low"] + 12 * (b["water_mo_low"] + b["elec_mo_low"])
                                  + (b["maint_yr_low"] + b["capex_yr_low"]) * ((1.028) ** n)),
                       "base": r10(b["insurance_yr_base"] + 12 * (b["water_mo_base"] + b["elec_mo_base"])
                                   + (b["maint_yr_base"] + b["capex_yr_base"]) * ((1.028) ** n)),
                       "high": r10(b["insurance_yr_high"] + 12 * (b["water_mo_high"] + b["elec_mo_high"])
                                   + (b["maint_yr_high"] + b["capex_yr_high"]) * ((1.04) ** n))},
            "b_prop_h": r10(b["prop_h_annual"]) if y >= 2027 else 0,
        }
        rows.append(row)
    return rows

# ---------------------------------------------------------------------------
# 4. Path comparison engine
# ---------------------------------------------------------------------------
CASES = {"low": 0, "base": 1, "high": 2}

def path_compare(transfer_year, horizon, case_key):
    """Terminal position (rounded) for each path at transfer_year+horizon.
    Returns dict of path_id -> {name, terminal, note}."""
    a, b = ASSUMPTIONS["property_a"], ASSUMPTIONS["property_b"]
    m, t = ASSUMPTIONS["macro"], ASSUMPTIONS["tax"]
    idx = CASES[case_key]
    appr = [a["appreciation_low"], a["appreciation_base"], a["appreciation_high"]][idx]
    infl = [m["inflation_low"], m["inflation_base"], m["inflation_high"]][idx]
    stock = [m["stock_nom_low"], m["stock_nom_base"], m["stock_nom_high"]][idx]
    tbill = [m["tbill_low"], m["tbill_base"], m["tbill_high"]][idx]
    v0_low, v0_base, v0_high = a["value_2026_low"], a["value_2026_base"], a["value_2026_high"]
    v0 = [v0_low, v0_base, v0_high][idx]
    rent_mo = [a["market_rent_mo_low"], a["market_rent_mo_base"], a["market_rent_mo_high"]][idx]
    ins = [a["insurance_yr_low"], a["insurance_yr_base"], a["insurance_yr_high"]][idx]
    water = [a["water_mo_low"], a["water_mo_base"], a["water_mo_high"]][idx]
    elec = [a["elec_net_mo_low"], a["elec_net_mo_base"], a["elec_net_mo_high"]][idx]
    maint = [a["maint_yr_low"], a["maint_yr_base"], a["maint_yr_high"]][idx]
    capex = [a["capex_yr_low"], a["capex_yr_base"], a["capex_yr_high"]][idx]
    eff_rate = [a["effective_tax_rate_low_pct"], a["effective_tax_rate_base_pct"], a["effective_tax_rate_high_pct"]][idx]

    n_to_transfer = transfer_year - 2026
    value_t = v0 * ((1 + appr / 100) ** n_to_transfer)
    assessed_t = a["assessed_2026"] * (1.02 ** n_to_transfer)
    prop_tax_t = assessed_t * eff_rate / 100

    # Sell-path friction at transfer (same tax year: step-up basis -> ~zero gain)
    dtt = value_t * t["scc_dtt_rate_pct"] / 100
    sale_other = value_t * 0.06 + r10(2000)          # commission+escrow+title+prep (assumption 6%)
    same_year_gain_tax = 0                            # step-up: gain ~0 (modelled; CPA verify)
    net_proceeds = value_t - dtt - sale_other - same_year_gain_tax

    # Post-transfer annual flows (transfer-date dollars, escalated by inflation)
    annual_carry_cost = prop_tax_t + ins + 12 * (water + elec) + maint + capex
    annual_net_rent = rent_mo * 12 * 0.95 - (prop_tax_t + ins + 12 * water + maint + capex)
    imputed_rent_net = rent_mo * 12 - annual_carry_cost          # live-in: housing service vs costs
    unit3_income = b["unit3_rent_mo_base"] * 12                  # if owner lives in A and rents B unit 3 (flagged)

    def grow_flows(base_flow, years, growth_pct, ret_pct):
        """Future value of an inflation-escalated annual flow invested at ret_pct."""
        total = 0.0
        for k in range(1, years + 1):
            total += base_flow * ((1 + growth_pct / 100) ** (k - 1)) * ((1 + ret_pct / 100) ** (years - k))
        return total

    def compound(p, ret_pct, years):
        return p * ((1 + ret_pct / 100) ** years)

    def phased(p, years, months):
        """Treasury parking then equities. months=24/36. Tranches at 0/12/24(/36).
        Cash earns tbill until its final tranche deploys; then stock return."""
        n_tr = months // 12 + 1
        chunk = p / n_tr
        total = 0.0
        for i in range(n_tr):
            wait = i  # years in treasuries
            total += compound(compound(chunk, tbill, wait), stock, max(0, years - wait))
        return total

    H = horizon
    paths = {}

    # 1) Sell in the SAME tax year as the inheritance (baseline first)
    paths["sell_same_year"] = {
        "name": "Sell same tax year, invest immediately",
        "terminal": net_proceeds * ((1 + stock / 100) ** H),
        "note": "Step-up basis at death keeps capital-gain tax ~$0; costs: DTT 0.11% + 6% sale friction (assumption).",
    }
    # 2) Sell + 24-month Treasury phase-in
    paths["sell_phase24"] = {
        "name": "Sell same year + 24-month Treasury phase-in",
        "terminal": phased(net_proceeds, H, 24),
        "note": "Tranches at months 0/12/24. Reinvestment risk beside the headline: each maturity resets at then-current yields.",
    }
    # 3) Sell + 36-month phase-in
    paths["sell_phase36"] = {
        "name": "Sell same year + 36-month Treasury phase-in",
        "terminal": phased(net_proceeds, H, 36),
        "note": "Tranches at months 0/12/24/36. More crash protection in year 1, more cash drag in a bull run.",
    }
    # 4) Live in A (imputed rent) + possible unit-3 rent at B
    paths["live_in"] = {
        "name": "Live in Property A (imputed rent + costs)",
        "terminal": value_t * ((1 + appr / 100) ** H) + grow_flows(imputed_rent_net + unit3_income, H, infl, stock),
        "note": "Imputed rent is the market-rent value of living in the home minus carrying costs; not cash received. Unit-3 rent at Property B assumes lawful rental use (flagged).",
    }
    # 5) Rent A out (market rent) and keep B as residence
    paths["rent_out"] = {
        "name": "Rent Property A at market (keep Property B residence)",
        "terminal": value_t * ((1 + appr / 100) ** H) + grow_flows(annual_net_rent, H, infl, stock),
        "note": "Market rent anchored to HUD FMR benchmark (flagged: obtain comparables). 5% vacancy; utilities tenant-paid; depreciation recapture applies on later sale (see tax-legal).",
    }
    # 6) Live 3 years then sell (tests Prop 19 + Section 121) and invest
    live_years = 3
    paths["live_then_sell"] = {
        "name": f"Live {live_years} years, then sell + invest",
        "terminal": grow_flows(imputed_rent_net + unit3_income, live_years, infl, stock) + compound(value_t * ((1 + appr / 100) ** live_years) - dtt - sale_other, stock, H - live_years),
        "note": "If occupancy rules met: Prop 19 keeps the old assessed value (capped) and IRC 121 can exclude up to $250k/$500k of later gain. Both depend on facts not yet verified.",
    }
    # 7) Rent 5 years then sell (depreciation recapture on sale)
    rent_years = 5
    annual_dep = (value_t * 0.75) / t["depreciation_years"]
    dep_taken = annual_dep * rent_years
    sale_value = value_t * ((1 + appr / 100) ** rent_years) - dtt - sale_other
    gain = max(0.0, sale_value - (value_t - dep_taken))
    recapture_tax = min(gain, dep_taken) * t["unrecaptured_1250_rate"] / 100
    other_gain_tax = max(0.0, gain - dep_taken) * (t["ltcg_top"] + t["niit"] + t["ca_top_marginal"] + t["ca_bhs_surtax"]) / 100
    paths["rent_then_sell"] = {
        "name": f"Rent {rent_years} years, then sell + invest",
        "terminal": grow_flows(annual_net_rent, rent_years, infl, stock) + compound(sale_value - recapture_tax - other_gain_tax, stock, H - rent_years),
        "note": "Depreciation claimed or allowable reduces basis; unrecaptured section 1250 gain taxed up to 25% federal + CA ordinary. Estimate shown uses a 75% building allocation (assumption).",
    }
    # 8) Mixed: sell now, invest 70%, keep 30% as a Treasury ladder reserve
    paths["mixed_70_30"] = {
        "name": "Mixed: sell now, 70% equities / 30% Treasury ladder",
        "terminal": 0.7 * net_proceeds * ((1 + stock / 100) ** H) + 0.3 * net_proceeds * ((1 + tbill / 100) ** H),
        "note": "Holds a deliberate liquidity sleeve (capital costs, tax payments, opportunities). Rebalancing rule should be written in advance.",
    }
    # 9) Mixed: live 2 years (test Prop 19/§121 in practice), then rent out to horizon
    live2 = 2
    paths["live2_then_rent"] = {
        "name": "Mixed: live 2 years, then rent out to horizon",
        "terminal": value_t * ((1 + appr / 100) ** H) + grow_flows(imputed_rent_net + unit3_income, min(live2, H), infl, stock) + grow_flows(annual_net_rent, max(0, H - live2), infl, stock),
        "note": "Two-year owner-occupancy can satisfy IRC 121's use test for a later sale; keeping it rented afterwards preserves optionality but adds landlord duties and eventual depreciation recapture.",
    }

    for p in paths.values():
        p["terminal"] = r10(p["terminal"])
        p["terminal_real"] = r10(p["terminal"] / ((1 + infl / 100) ** H))
    return {
        "transfer_year": transfer_year, "horizon": H, "case": case_key,
        "value_at_transfer": r10(value_t),
        "net_proceeds_same_year": r10(net_proceeds),
        "prop_tax_at_transfer": r10(prop_tax_t),
        "paths": paths,
    }

COMPARISONS = []
for ty in (2040, 2045, 2050):
    for h in (5, 10, 20, 30):
        for case_key in ("low", "base", "high"):
            if ty + h <= 2085:
                COMPARISONS.append(path_compare(ty, h, case_key))

# ---------------------------------------------------------------------------
# 5. Estate tax sensitivity (graduated federal table, simplified 2026 law)
# ---------------------------------------------------------------------------
def estate_tax(gross, exclusion):
    taxable = max(0.0, gross - exclusion)
    # Simplified graduated computation per Form 706 tax table: 18%..40%.
    if taxable <= 0:
        return 0
    brackets = [(10000, 0), (20000, 1800), (40000, 3800), (60000, 8200), (80000, 13000),
                (100000, 18200), (150000, 23800), (250000, 38800), (500000, 70800),
                (750000, 155800), (1000000, 248300), (float('inf'), 345800)]
    # tax = 345800 + 40% over 1,000,000 for large estates (Form 706 table)
    if taxable <= 1000000:
        tax = 0
        prev = 0
        rates = [0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.32, 0.34, 0.37, 0.39]
        bounds = [10000, 20000, 40000, 60000, 80000, 100000, 150000, 250000, 500000, 750000, 1000000]
        for r, bo in zip(rates, bounds):
            seg = min(taxable, bo) - prev
            tax += seg * r
            prev = bo
            if taxable <= bo:
                break
        return tax
    return 345800 + 0.40 * (taxable - 1000000)

ESTATE_SENSITIVITY = []
for g in (10000000, 15000000, 20000000, 25000000, 30000000, 40000000):
    for label, excl in (("single (one exclusion)", 15000000), ("married (portability, two exclusions)", 30000000)):
        ESTATE_SENSITIVITY.append({
            "gross_estate": r10(g), "filing": label,
            "exclusion": r10(excl),
            "tax_estimated": r10(estate_tax(g, excl)),
            "effective_rate_pct": round(estate_tax(g, excl) / g * 100, 2),
        })

# CA 1% Behavioral Health Services Tax sensitivity (whole-dollar, not indexed)
BHS_SENSITIVITY = []
for ti in (500000, 1000000, 1500000, 2000000, 3000000, 5000000):
    BHS_SENSITIVITY.append({
        "ca_taxable_income": r10(ti),
        "bhs_tax": r10(max(0, ti - 1000000) * 0.01),
    })

# ---------------------------------------------------------------------------
# 6. Black-swan replays (Damodaran annual returns, Jan 2026 dataset)
# ---------------------------------------------------------------------------
# Annual total returns (%) and 3-month T-bill averages (%), pages.stern.nyu.edu histretSP
MARKET = {
    1929: (-8.30, 3.16), 1930: (-25.12, 4.55), 1931: (-43.84, 2.31), 1932: (-8.64, 1.07),
    1933: (49.98, 0.96), 1934: (-1.19, 0.28), 1935: (46.74, 0.17), 1936: (31.94, 0.17),
    1937: (-35.34, 0.28), 1938: (29.28, 0.07), 1939: (-1.10, 0.05), 1940: (-10.67, 0.04),
    1941: (-12.77, 0.13), 1942: (19.17, 0.34), 1943: (25.06, 0.38), 1944: (19.03, 0.38),
    1945: (35.82, 0.38),
    1970: (3.56, 6.39), 1971: (14.22, 4.33), 1972: (18.76, 4.06),
    1973: (-14.31, 7.04), 1974: (-25.90, 7.85), 1975: (37.00, 5.79), 1976: (23.83, 4.98),
    1977: (-6.98, 5.26), 1978: (6.51, 7.18), 1979: (18.52, 10.05), 1980: (31.74, 11.39),
    1981: (-4.70, 14.04), 1982: (20.42, 11.09), 1983: (22.34, 8.95), 1984: (6.15, 9.92),
    1985: (31.24, 7.72), 1986: (18.49, 6.15), 1987: (5.81, 5.96), 1988: (16.54, 6.89),
    1989: (31.48, 8.39),
    1990: (-3.06, 7.75), 1991: (30.23, 5.54), 1992: (7.49, 3.51), 1993: (9.97, 3.07),
    1994: (1.33, 4.37), 1995: (37.20, 5.66), 1996: (22.68, 5.15), 1997: (33.10, 5.20),
    1998: (28.34, 4.91), 1999: (20.89, 4.78),
    2000: (-9.03, 6.00), 2001: (-11.85, 3.48), 2002: (-21.97, 1.64), 2003: (28.36, 1.03),
    2004: (10.74, 1.40), 2005: (4.83, 3.22), 2006: (15.61, 4.85),
    2007: (5.48, 4.48), 2008: (-36.55, 1.40), 2009: (25.94, 0.15), 2010: (14.82, 0.14),
    2011: (2.10, 0.05), 2012: (15.89, 0.09), 2013: (32.15, 0.06), 2014: (13.52, 0.03),
    2015: (1.38, 0.05), 2016: (11.77, 0.32), 2017: (21.61, 0.95), 2018: (-4.23, 1.97),
    2019: (31.21, 2.11),
    2021: (28.47, 0.04), 2022: (-18.04, 2.09), 2023: (26.06, 5.28), 2024: (24.88, 5.18),
    2025: (17.78, 4.21),
}

def replay(start_year, years, plan):
    """$1,000,000 at start of start_year.
    plan: 'immediate' (all at once) | 'p24' (tranches 0/12/24 mo) | 'p36' (0/12/24/36)."""
    p = 1000000.0
    if plan == "immediate":
        v = p
        for k in range(years):
            r, _ = MARKET[start_year + k]
            v *= (1 + r / 100)
        return r10(v)
    n_tr = 3 if plan == "p24" else 4
    chunk = p / n_tr
    v = 0.0
    for i in range(n_tr):
        bal = chunk
        for k in range(years):
            yr = start_year + k
            stock_r, tbill_r = MARKET[yr]
            if k < i:   # still parked in T-bills until its entry year
                bal *= (1 + tbill_r / 100)
            else:
                bal *= (1 + stock_r / 100)
        v += bal
    return r10(v)

REPLAYS = []
for label, sy, y1, y2 in (
    ("1929 entry (start of 1929)", 1929, 4, 9),
    ("1973 entry (stagflation)", 1973, 2, 8),
    ("2008 entry (start of 2008)", 2008, 2, 5),
    ("2013 entry (bull market — staging loses)", 2013, 1, 4),
    ("2022 entry (start of 2022)", 2022, 1, 4),
):
    REPLAYS.append({
        "id": f"{sy}", "name": label,
        "series": "S&P 500 annual total return and 3-month T-bill (Damodaran histretSP, Jan 2026)",
        "endpoints": [
            {"years": y1, "immediate": replay(sy, y1, "immediate"), "phase_24": replay(sy, y1, "p24"), "phase_36": replay(sy, y1, "p36")},
            {"years": y2, "immediate": replay(sy, y2, "immediate"), "phase_24": replay(sy, y2, "p24"), "phase_36": replay(sy, y2, "p36")},
        ],
    })

# Decade reality check: nominal vs real growth is NOT consistent.
# CAGRs computed from the verified Damodaran annual series in MARKET (never hand-entered).
def decade_cagr(y0, y1):
    p = 1.0
    n = 0
    for y in range(y0, y1 + 1):
        if y in MARKET:
            p *= (1 + MARKET[y][0] / 100)
            n += 1
    return round(((p ** (1 / n)) - 1) * 100, 1) if n else None

DECADES = [
    {"decade": "1930s", "sp_nom_cagr": decade_cagr(1930, 1939), "cpi_note": "deflation in early years (CPI -21% 1929-32, FRED)", "regime": "Crash + deflation"},

    {"decade": "1970s", "sp_nom_cagr": decade_cagr(1970, 1979), "cpi_note": "high inflation (~7%/yr era)", "regime": "Stagflation: real returns negative"},
    {"decade": "1980s", "sp_nom_cagr": decade_cagr(1980, 1989), "cpi_note": "disinflation", "regime": "Bull"},
    {"decade": "1990s", "sp_nom_cagr": decade_cagr(1990, 1999), "cpi_note": "low inflation", "regime": "Tech bull"},
    {"decade": "2000s", "sp_nom_cagr": decade_cagr(2000, 2009), "cpi_note": "~2.5%/yr", "regime": "Two crashes, flat decade"},
    {"decade": "2010s", "sp_nom_cagr": decade_cagr(2010, 2019), "cpi_note": "very low inflation", "regime": "Slow-inflation bull"},
    {"decade": "2020s (partial)", "sp_nom_cagr": decade_cagr(2020, 2025), "cpi_note": "2021-22 inflation spike; 2020-25 only", "regime": "Crash, spike, rebound — incomplete"},
]
# CPI notes are qualitative; exact CPI figures come from FRED CPIAUCNS (linked on the site).

# ---------------------------------------------------------------------------
# 7. Five-year maintenance & capital plan (inspection-backed bids still required)
# ---------------------------------------------------------------------------
CAPITAL_PLAN_A = [
    {"item": "Roof (composition, ~20+ yrs)", "window": "Years 0-5", "low": r10(18000), "base": r10(25000), "high": r10(35000), "status": "unverified — inspection required"},
    {"item": "HVAC service / replace", "window": "Years 2-5", "low": r10(8000), "base": r10(12000), "high": r10(18000), "status": "unverified"},
    {"item": "Exterior paint", "window": "Years 3-5", "low": r10(10000), "base": r10(15000), "high": r10(22000), "status": "unverified"},
    {"item": "Solar inverter / battery service", "window": "Years 1-5", "low": r10(2000), "base": r10(6000), "high": r10(15000), "status": "unverified — equipment age unknown"},
    {"item": "Plumbing / water heater", "window": "Years 0-5", "low": r10(1500), "base": r10(4000), "high": r10(9000), "status": "unverified"},
    {"item": "Seismic retrofit / foundation review", "window": "Year 0", "low": r10(0), "base": r10(3000), "high": r10(12000), "status": "unverified — engineering review"},
    {"item": "Appliances / flooring refresh", "window": "Years 0-5", "low": r10(3000), "base": r10(8000), "high": r10(15000), "status": "unverified"},
]
CAPITAL_PLAN_B = [
    {"item": "Roof (multi-unit)", "window": "Years 0-5", "low": r10(22000), "base": r10(32000), "high": r10(45000), "status": "unverified — inspection required"},
    {"item": "Exterior paint / siding", "window": "Years 2-5", "low": r10(15000), "base": r10(22000), "high": r10(32000), "status": "unverified"},
    {"item": "Plumbing (3 units), drains", "window": "Years 0-5", "low": r10(6000), "base": r10(14000), "high": r10(28000), "status": "unverified"},
    {"item": "Electrical panel / code items", "window": "Years 1-5", "low": r10(4000), "base": r10(10000), "high": r10(20000), "status": "unverified"},
    {"item": "Seismic retrofit / soft-story review", "window": "Year 0", "low": r10(0), "base": r10(8000), "high": r10(30000), "status": "unverified — engineering + SF DBI records"},
    {"item": "Unit turnover / interiors (2 rented units)", "window": "Years 0-5", "low": r10(5000), "base": r10(12000), "high": r10(25000), "status": "unverified"},
    {"item": "Legalization / permit reconciliation (unit 3)", "window": "Year 0", "low": r10(0), "base": r10(5000), "high": r10(40000), "status": "UNVERIFIED — DBI records review first"},
]

# ---------------------------------------------------------------------------
# 8. Sell-path cost stack (illustrative $3.1M sale, all rounded)
# ---------------------------------------------------------------------------
def sale_stack(price):
    t = ASSUMPTIONS["tax"]
    return [
        {"line": "Gross sale price", "amount": r10(price), "basis": "illustrative rounded price"},
        {"line": "Documentary transfer tax (0.11% county)", "amount": r10(price * t["scc_dtt_rate_pct"] / 100), "basis": "R&T 11911"},
        {"line": "Commission + escrow + title + prep (6%, assumption)", "amount": r10(price * 0.06), "basis": "ASSUMPTION — get quotes"},
        {"line": "Recording / notary / misc fees", "amount": r10(2000), "basis": "ASSUMPTION — county fee schedule"},
        {"line": "Federal + CA capital-gain tax (same-year sale)", "amount": r10(0), "basis": "IRC 1014 step-up; gain ≈ 0 — CPA verify"},
        {"line": "Estimated net proceeds", "amount": r10(price * (1 - 0.06 - t["scc_dtt_rate_pct"] / 100) - 2000), "basis": "computed"},
    ]

SALE_STACK_A = sale_stack(3100000)

# ---------------------------------------------------------------------------
# 9. Assemble + emit
# ---------------------------------------------------------------------------
model = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "assumptions": ASSUMPTIONS,
    "history_a": PROPERTY_A_HISTORY,
    "history_b": PROPERTY_B_HISTORY,
    "projections": project(),
    "comparisons": COMPARISONS,
    "estate_sensitivity": ESTATE_SENSITIVITY,
    "bhs_sensitivity": BHS_SENSITIVITY,
    "replays": REPLAYS,
    "decades": DECADES,
    "capital_plan_a": CAPITAL_PLAN_A,
    "capital_plan_b": CAPITAL_PLAN_B,
    "sale_stack_a": SALE_STACK_A,
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write("// Generated by scripts/build_model.py — do not edit by hand.\n")
    f.write("// Owner policy 2026-11-25: figures rounded to nearest $10; no personal identifiers.\n")
    f.write("window.MODEL = ")
    json.dump(model, f, ensure_ascii=False, indent=1)
    f.write(";\n")
print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")
print(f"comparisons: {len(COMPARISONS)}, projections: {len(model['projections'])}, replays: {len(REPLAYS)}")
# quick sanity output
c = [x for x in COMPARISONS if x['transfer_year'] == 2045 and x['horizon'] == 10 and x['case'] == 'base'][0]
print('sanity 2045/10y/base:', json.dumps({k: v['terminal'] for k, v in c['paths'].items()}, indent=0))
