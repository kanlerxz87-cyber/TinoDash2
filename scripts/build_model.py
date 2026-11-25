#!/usr/bin/env python3
"""
Build anonymized, rounded-to-$10 decision model for the inheritance dashboard.
All outputs are privacy-sanitized: no names, addresses, zip codes, parcel IDs,
or exact source-table values that could be traced. Values rounded to nearest $10.
"""
from __future__ import annotations
import json, math, os
from datetime import datetime, timezone

OUT = os.path.join(os.path.dirname(__file__), '..', 'docs', 'data', 'model.json')

def r10(x):
    """Round to nearest $10."""
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return None
    return int(round(float(x) / 10.0) * 10)

def r10_list(xs):
    return [r10(x) for x in xs]

def pct(x):
    return round(x * 100, 2)

# -------------------------
# Assumptions (anonymized)
# -------------------------
ASSUMPTIONS = {
    "as_of_date": "2026-11-25",
    "rounding_rule": "All displayed currency values rounded to nearest $10; rates shown as percentages with up to 2 decimals. Historical source-table values are rounded before display.",
    "privacy_rule": "No personal names, street addresses, ZIP codes, parcel/APN IDs, account numbers, or exact traceable public-record values in public outputs.",
    "properties": {
        "A": {
            "label": "Property A (Santa Clara County, CA) — inherited by trust",
            "role": "Inherited property; not currently owned by Owner B before transfer",
            "estimated_value_2026_low": 2950000,
            "estimated_value_2026_base": 3100000,
            "estimated_value_2026_high": 3250000,
            "value_note": "Planning range around a 2026 estimate; obtain independent date-of-death/appraisal comps before decisions.",
        },
        "B": {
            "label": "Property B (San Francisco, CA) — already owned",
            "role": "Already owned by Owner B; primary residence with rental units",
            "estimated_value_2026_low": 1700000,
            "estimated_value_2026_base": 1800000,
            "estimated_value_2026_high": 1900000,
            "rental_income_monthly_low": 6800,
            "rental_income_monthly_base": 7150,
            "rental_income_monthly_high": 7500,
            "units_rented": 2,
            "units_total_livable": 3,
            "owner_can_live_without_losing_rental_income": True,
        }
    },
    "transfer_window": [2040, 2045, 2050],
    "projection_horizons_years": [5, 10, 20, 30],
    "appreciation_scenarios": {
        "low": 0.02,
        "base": 0.035,
        "high": 0.055,
    },
    "inflation_scenarios": {
        "low": 0.02,
        "base": 0.028,
        "high": 0.04,
    },
    "stock_return_scenarios_nominal": {
        "conservative": 0.05,
        "base": 0.07,
        "optimistic": 0.09,
    },
    "savings_return_nominal": {
        "low": 0.025,
        "base": 0.035,
        "high": 0.045,
    },
    "property_a_costs_annual": {
        "water_monthly_low": 100,
        "water_monthly_base": 130,
        "water_monthly_high": 150,
        "electricity_net_monthly_low": -20,
        "electricity_net_monthly_base": -15,
        "electricity_net_monthly_high": 0,
        "insurance_annual_low": 1200,
        "insurance_annual_base": 1500,
        "insurance_annual_high": 2200,
        "maintenance_annual_pct_low": 0.005,
        "maintenance_annual_pct_base": 0.008,
        "maintenance_annual_pct_high": 0.012,
        "capital_reserve_annual_pct": 0.005,
    },
    "property_b_costs_annual": {
        "water_monthly_low": 330,
        "water_monthly_base": 360,
        "water_monthly_high": 400,
        "electricity_monthly_low": 30,
        "electricity_monthly_base": 50,
        "electricity_monthly_high": 70,
        "insurance_annual_low": 1800,
        "insurance_annual_base": 2600,
        "insurance_annual_high": 3600,
        "maintenance_annual_pct_low": 0.008,
        "maintenance_annual_pct_base": 0.012,
        "maintenance_annual_pct_high": 0.018,
        "capital_reserve_annual_pct": 0.008,
    },
    "tax_assumptions": {
        "federal_ltcg_rate_base": 0.20,
        "federal_niit_rate": 0.038,
        "ca_top_marginal_rate": 0.133,
        "ca_mental_health_threshold": 1000000,
        "ca_capital_gains_treated_as_ordinary": True,
        "federal_estate_exemption_2026_per_person": 15000000,
        "federal_estate_exemption_portability_couple": 30000000,
        "federal_estate_top_rate": 0.40,
        "annual_gift_exclusion_2026": 19000,
        "step_up_basis_general_rule": True,
        "property_tax_base_rate_estimate": 0.0118,
        "prop13_annual_assessed_increase_cap": 0.02,
        "prop19_value_limit_over_fbyv": 1000000,
        "prop19_filing_homeowner_exemption_days": 365,
        "prop19_claim_filing_years": 3,
    },
}

# -------------------------
# Historical tables (rounded for display)
# -------------------------
# Raw values provided by user are rounded to nearest $10 for public display.
PROPERTY_A_HISTORY = [
    {"year": 2026, "property_taxes": None, "tax_assessment": 550540, "note": "Property tax not provided"},
    {"year": 2025, "property_taxes": 7210, "tax_assessment": 539740, "note": ""},
    {"year": 2024, "property_taxes": 7000, "tax_assessment": 529160, "note": ""},
    {"year": 2023, "property_taxes": 6920, "tax_assessment": 518790, "note": ""},
    {"year": 2022, "property_taxes": 6760, "tax_assessment": 508610, "note": ""},
    {"year": 2021, "property_taxes": 6660, "tax_assessment": 498640, "note": ""},
    {"year": 2020, "property_taxes": 6570, "tax_assessment": 493530, "note": ""},
    {"year": 2019, "property_taxes": 6570, "tax_assessment": 483850, "note": ""},
    {"year": 2018, "property_taxes": 6380, "tax_assessment": 474370, "note": ""},
    {"year": 2017, "property_taxes": 6380, "tax_assessment": 465070, "note": ""},
    {"year": 2016, "property_taxes": 6410, "tax_assessment": 455950, "note": ""},
    {"year": 2015, "property_taxes": 6130, "tax_assessment": 449100, "note": ""},
    {"year": 2014, "property_taxes": 5970, "tax_assessment": 440310, "note": ""},
]

PROPERTY_B_HISTORY = [
    {"year": 2025, "property_taxes": 2440, "tax_assessment": 114250, "note": ""},
    {"year": 2024, "property_taxes": 2320, "tax_assessment": 112010, "note": ""},
    {"year": 2023, "property_taxes": 2180, "tax_assessment": 109810, "note": ""},
    {"year": 2022, "property_taxes": 2110, "tax_assessment": 107660, "note": ""},
    {"year": 2021, "property_taxes": 2070, "tax_assessment": 105600, "note": ""},
    {"year": 2020, "property_taxes": 2200, "tax_assessment": 104510, "note": ""},
    {"year": 2019, "property_taxes": 2130, "tax_assessment": 102470, "note": ""},
    {"year": 2018, "property_taxes": 2060, "tax_assessment": 100460, "note": ""},
    {"year": 2017, "property_taxes": 1740, "tax_assessment": 98490, "note": ""},
    {"year": 2016, "property_taxes": 1680, "tax_assessment": 96560, "note": ""},
]

# -------------------------
# Projection helpers
# -------------------------

def future_value(pv, rate, years):
    return pv * ((1 + rate) ** years)


def annual_property_tax(assessed, base_rate=0.0118):
    # Simplified: assessed value * base rate. Real bills include voter-approved items; flag as estimate.
    return assessed * base_rate


def prop13_assessed(base_assessed, years, cap=0.02):
    return base_assessed * ((1 + cap) ** years)


def property_a_annual_opex(value, insurance, water_m, elec_net_m, maint_pct, capex_pct, prop_tax):
    return prop_tax + insurance + (water_m * 12) + (elec_net_m * 12) + (value * maint_pct) + (value * capex_pct)


def property_b_net_annual(value, rent_m, vacancy, insurance, water_m, elec_m, maint_pct, capex_pct, prop_tax, mgmt_pct):
    gross = rent_m * 12 * (1 - vacancy)
    opex = prop_tax + insurance + (water_m * 12) + (elec_m * 12) + (value * maint_pct) + (value * capex_pct) + (gross * mgmt_pct)
    return gross - opex, gross, opex


def estimate_sale_costs(price, transfer_tax_rate=0.0, recording_fixed=500, broker_pct=0.05, other_pct=0.005):
    return price * (broker_pct + other_pct + transfer_tax_rate) + recording_fixed


def estimate_federal_cap_gain_tax(gain, taxable_income_over_threshold=True):
    # Simplified: LTCG 20% + NIIT 3.8% if applicable. State handled separately. 
    rate = 0.20 + (0.038 if taxable_income_over_threshold else 0.0)
    return max(0, gain) * rate


def estimate_ca_cap_gain_tax(gain, taxable_income_total):
    # Simplified: treat gain as ordinary CA income. Use blended marginal approximation.
    # Below/above $1M mental health threshold handled approximately.
    if gain <= 0:
        return 0
    # Approximate effective marginal on large gains in CA: 12.3% + 1% over $1M.
    base = gain * 0.123
    over_m = max(0, min(gain, max(0, taxable_income_total - 1_000_000)))
    mh = over_m * 0.01
    return base + mh


def build_transfer_scenarios():
    scenarios = []
    for tyear in ASSUMPTIONS['transfer_window']:
        years_from_2026 = tyear - 2026
        for appr_name, appr in ASSUMPTIONS['appreciation_scenarios'].items():
            # Property A value at transfer
            value_t = future_value(ASSUMPTIONS['properties']['A']['estimated_value_2026_base'], appr, years_from_2026)
            # Assessed value under Prop 13 from 2026 base (simplified; actual reassessment at transfer depends on Prop 19 eligibility)
            assessed_prop13 = prop13_assessed(550540, years_from_2026, 0.02)  # from rounded 2026 assessment
            scenarios.append({
                'transfer_year': tyear,
                'appreciation': appr_name,
                'appreciation_rate': appr,
                'property_a_value': r10(value_t),
                'property_a_prop13_assessed_est': r10(assessed_prop13),
            })
    return scenarios


def build_path_comparison():
    # Compare at 2045 transfer, 10-year horizon after transfer, base assumptions.
    tyear = 2045
    horizon = 10
    years_to_transfer = tyear - 2026
    appr = ASSUMPTIONS['appreciation_scenarios']['base']
    infl = ASSUMPTIONS['inflation_scenarios']['base']
    stock = ASSUMPTIONS['stock_return_scenarios_nominal']['base']
    savings = ASSUMPTIONS['savings_return_nominal']['base']
    value_at_transfer = future_value(ASSUMPTIONS['properties']['A']['estimated_value_2026_base'], appr, years_to_transfer)
    assessed_at_transfer = prop13_assessed(550540, years_to_transfer, 0.02)

    # Common operating assumptions
    ins_a = ASSUMPTIONS['property_a_costs_annual']['insurance_annual_base']
    water_a = ASSUMPTIONS['property_a_costs_annual']['water_monthly_base']
    elec_a = ASSUMPTIONS['property_a_costs_annual']['electricity_net_monthly_base']
    maint_a = ASSUMPTIONS['property_a_costs_annual']['maintenance_annual_pct_base']
    capex_a = ASSUMPTIONS['property_a_costs_annual']['capital_reserve_annual_pct']
    tax_rate = ASSUMPTIONS['tax_assumptions']['property_tax_base_rate_estimate']

    def opex_a(year_idx, value, assessed, prop19_exclusion=False):
        # If Prop 19 exclusion applies, assessed may be limited; simplified.
        a = assessed
        if prop19_exclusion:
            # Exclusion: factored base year value + $1M (inflation-adjusted) cap; simplified as assessed carries over if within cap.
            cap_limit = assessed_at_transfer + 1_000_000  # simplified, not inflation-adjusted in this rough model
            a = min(value, cap_limit)
        ptax = annual_property_tax(a, tax_rate)
        ins = ins_a * ((1 + infl) ** year_idx)
        water = water_a * 12 * ((1 + infl) ** year_idx)
        elec = elec_a * 12 * ((1 + infl) ** year_idx)
        maint = value * maint_a
        capex = value * capex_a
        return ptax + ins + water + elec + maint + capex, ptax

    paths = []

    # Path 1: Live in Property A (primary residence), claim Prop 19 if eligible
    # Assumes Prop 19 eligible and filed; assessed carries over/limited.
    value = value_at_transfer
    assessed = assessed_at_transfer
    cum_cost = 0
    for y in range(1, horizon + 1):
        value = value * (1 + appr)
        assessed = assessed * 1.02
        c, _ = opex_a(y, value, assessed, prop19_exclusion=True)
        cum_cost += c
    paths.append({
        'id': 'live_a',
        'name': 'Live in Property A (primary residence)',
        'transfer_year': tyear,
        'horizon_years': horizon,
        'end_asset_value': r10(value),
        'cumulative_cash_cost': r10(cum_cost),
        'net_position_est': r10(value - cum_cost),
        'liquidity': 'Low (wealth tied in home)',
        'key_risks': 'Prop 19 eligibility/file deadlines; maintenance/capex shocks; concentration risk; opportunity cost vs. reinvestment',
        'tax_notes': 'If Prop 19 exclusion applies, assessed value may carry over within value cap; primary residence exclusion may apply on later sale if ownership/use tests met. Verify eligibility.',
    })

    # Path 2: Rent out Property A, live in Property B
    value = value_at_transfer
    assessed = assessed_at_transfer
    cum_cash = 0
    rent_m = 5500  # planning range placeholder - MUST be flagged as unverified estimate
    vacancy = 0.05
    mgmt = 0.08
    for y in range(1, horizon + 1):
        value = value * (1 + appr)
        assessed = assessed * 1.02
        opex, ptax = opex_a(y, value, assessed, prop19_exclusion=False)
        gross = rent_m * 12 * ((1 + infl) ** y) * (1 - vacancy)
        mgmt_cost = gross * mgmt
        net = gross - opex - mgmt_cost
        cum_cash += net
    paths.append({
        'id': 'rent_a',
        'name': 'Rent Property A; live in Property B',
        'transfer_year': tyear,
        'horizon_years': horizon,
        'end_asset_value': r10(value),
        'cumulative_cash_flow_after_costs': r10(cum_cash),
        'net_position_est': r10(value + cum_cash),
        'liquidity': 'Medium (rental income, illiquid equity)',
        'key_risks': 'Rent estimate unverified; vacancy; tenant/lease/legal risk; depreciation recapture; property-tax reassessment if Prop 19 not applicable; capex shocks',
        'tax_notes': 'Rental income taxable; depreciation may apply but creates recapture on sale; Prop 19 parent-child exclusion generally not available if not owner-occupied as primary residence. Verify with CPA.',
    })

    # Path 3: Sell Property A and reinvest
    sale_price = value_at_transfer
    sell_costs = estimate_sale_costs(sale_price, transfer_tax_rate=0.0, recording_fixed=500, broker_pct=0.05, other_pct=0.005)
    # Step-up basis at death generally means gain near zero if sold soon after; later gain depends on timing.
    # We'll show two sub-cases: sell near transfer (minimal gain) and sell later.
    net_proceeds = sale_price - sell_costs
    portfolio = net_proceeds
    for y in range(1, horizon + 1):
        portfolio = portfolio * (1 + stock)
    paths.append({
        'id': 'sell_reinvest',
        'name': 'Sell Property A near transfer; reinvest proceeds',
        'transfer_year': tyear,
        'horizon_years': horizon,
        'sale_price_est': r10(sale_price),
        'sale_costs_est': r10(sell_costs),
        'net_proceeds_est': r10(net_proceeds),
        'end_portfolio_value': r10(portfolio),
        'net_position_est': r10(portfolio),
        'liquidity': 'High (liquid portfolio, subject to market/tax)',
        'key_risks': 'Market sequence risk; reinvestment risk; tax drag; behavioral risk; loss of real-asset/inflation hedge; transaction costs',
        'tax_notes': 'Step-up in basis may reduce/eliminate capital gain if sold soon after death; state/federal taxes still depend on timing, income, and basis documentation. Price transfer tax/recording fees into net.',
    })

    # Path 4: Mixed - live 2 years then sell
    value = value_at_transfer
    assessed = assessed_at_transfer
    cum_cost = 0
    live_years = 2
    for y in range(1, live_years + 1):
        value = value * (1 + appr)
        assessed = assessed * 1.02
        c, _ = opex_a(y, value, assessed, prop19_exclusion=True)
        cum_cost += c
    sale_price2 = value
    sell_costs2 = estimate_sale_costs(sale_price2)
    net2 = sale_price2 - sell_costs2 - cum_cost
    portfolio2 = net2
    for y in range(live_years + 1, horizon + 1):
        portfolio2 = portfolio2 * (1 + stock)
    paths.append({
        'id': 'live_then_sell',
        'name': 'Live in Property A 2 years, then sell and reinvest',
        'transfer_year': tyear,
        'horizon_years': horizon,
        'live_years_before_sale': live_years,
        'sale_price_est': r10(sale_price2),
        'sale_costs_est': r10(sell_costs2),
        'cumulative_holding_cost_before_sale': r10(cum_cost),
        'end_portfolio_value': r10(portfolio2),
        'net_position_est': r10(portfolio2),
        'liquidity': 'Low then high after sale',
        'key_risks': 'Timing risk; eligibility for primary-residence exclusion depends on ownership/use tests; Prop 19 implications; sequence risk after sale',
        'tax_notes': 'Primary-residence exclusion rules (IRC 121) require meeting ownership and use tests; confirm with CPA. Step-up basis and holding period matter.',
    })

    # Path 5: Black-swan phased investing
    sale_price = value_at_transfer
    sell_costs = estimate_sale_costs(sale_price)
    net_proceeds = sale_price - sell_costs
    # Park in T-bills/short Treasuries for 2 years, then phase into stocks over 3 years
    treasury = 0.04
    portfolio = net_proceeds
    # 2 years in treasuries
    for y in range(1, 3):
        portfolio = portfolio * (1 + treasury)
    # phase in over years 3-5: 1/3 each year moves to stocks; remaining stays in treasuries then invested
    # simplified: 33% invested at end of year 2, 33% year 3, 34% year 4
    buckets = [portfolio/3, portfolio/3, portfolio - 2*(portfolio/3)]
    # year 3: bucket0 in stocks, bucket1,2 in treasury
    buckets[0] *= (1+stock); buckets[1] *= (1+treasury); buckets[2] *= (1+treasury)
    # year 4
    buckets[0] *= (1+stock); buckets[1] *= (1+stock); buckets[2] *= (1+treasury)
    # year 5 onward all in stocks
    buckets[0] *= (1+stock); buckets[1] *= (1+stock); buckets[2] *= (1+stock)
    for y in range(6, horizon+1):
        buckets = [b*(1+stock) for b in buckets]
    portfolio_phased = sum(buckets)
    paths.append({
        'id': 'sell_phased',
        'name': 'Sell, park proceeds in 3M–2Y Treasuries 24 months, then phase into stocks over 36 months',
        'transfer_year': tyear,
        'horizon_years': horizon,
        'sale_price_est': r10(sale_price),
        'net_proceeds_est': r10(net_proceeds),
        'end_portfolio_value': r10(portfolio_phased),
        'net_position_est': r10(portfolio_phased),
        'liquidity': 'High (liquid; staged market exposure)',
        'key_risks': 'Cash drag/reinvestment risk during holding period; inflation erosion; missed upside if markets rise; still exposed to market risk after phasing',
        'tax_notes': 'Treasury interest taxable; capital gains/dividends taxed as realized. Reinvestment and yield changes are material risks.',
    })

    return paths


def build_black_swan():
    # Illustrative scenarios - not predictions. All returns nominal, rounded.
    return [
        {
            'id': '1929_analog',
            'name': '1929-style crash analog (illustrative)',
            'description': 'Severe equity drawdown early in holding period, slow recovery, deflationary shock then policy response. Used to stress sequence-of-returns risk for sell-and-reinvest path.',
            'assumed_path_nominal_stock_returns': [-0.20, -0.30, -0.15, 0.05, 0.20, 0.15, 0.10, 0.08, 0.07, 0.07],
            'assumed_inflation': [-0.02, -0.05, -0.03, 0.00, 0.02, 0.03, 0.03, 0.03, 0.03, 0.03],
            'notes': 'Illustrative stress scenario only; not a forecast. Sequence risk is highest when large lump sum enters near peak.'
        },
        {
            'id': '2008_analog',
            'name': '2008-style financial crisis analog (illustrative)',
            'description': 'Sharp equity decline, credit stress, housing weakness, then recovery supported by policy.',
            'assumed_path_nominal_stock_returns': [-0.38, 0.26, 0.15, 0.02, 0.16, 0.32, 0.14, 0.01, 0.12, 0.21],
            'assumed_inflation': [0.03, -0.01, 0.02, 0.03, 0.02, 0.02, 0.01, 0.02, 0.02, 0.02],
            'notes': 'Illustrative stress scenario only; highlights drawdown + recovery and housing/equity correlation risk.'
        },
        {
            'id': 'stagflation_analog',
            'name': '1970s-style stagflation analog (illustrative)',
            'description': 'High inflation, weak real returns, rising rates, uneven equity performance.',
            'assumed_path_nominal_stock_returns': [0.04, -0.15, -0.27, 0.37, 0.24, -0.07, 0.06, 0.18, 0.32, -0.05],
            'assumed_inflation': [0.06, 0.08, 0.12, 0.07, 0.05, 0.06, 0.09, 0.11, 0.13, 0.11],
            'notes': 'Illustrative stress scenario only; real (inflation-adjusted) outcomes can be much worse than nominal.'
        }
    ]


def build_deadlines():
    return [
        {"date_or_window": "Date of death / trust transfer event", "item": "Obtain written date-of-death valuation for Property A", "who": "Trustee/executor/appraiser", "why": "Establishes fair market value for basis and reporting; supports step-up basis documentation.", "source_type": "IRS/valuation practice"},
        {"date_or_window": "Within 1 year of transfer (Prop 19)", "item": "If claiming parent-child exclusion, transferee must occupy Property A as primary residence and file homeowner's/disabled veteran's exemption", "who": "Heir/Owner B", "why": "Prop 19 requires primary-residence occupancy and timely exemption filing for exclusion.", "source_type": "CA BOE Prop 19"},
        {"date_or_window": "Within 3 years of transfer, or before transfer to 3rd party (earlier)", "item": "File Prop 19 claim form (BOE-19-P/BOE-19-G as applicable)", "who": "Heir/Owner B", "why": "Required to claim intergenerational transfer exclusion; late filing may limit relief.", "source_type": "CA BOE Prop 19"},
        {"date_or_window": "9 months after death (plus extensions if applicable)", "item": "Federal estate tax return (Form 706) if required or if portability election desired", "who": "Executor/trustee/CPA", "why": "Required when gross estate exceeds filing threshold; portability election must be timely made on complete Form 706.", "source_type": "IRS Estate Tax / Form 706"},
        {"date_or_window": "Same tax year as inheritance (if considering sale)", "item": "Model sale-in-same-tax-year scenario before deciding", "who": "Owner B + CPA", "why": "Timing affects gain, basis documentation, CA taxable income, and 1% Mental Health Services Tax exposure above $1M.", "source_type": "FTB/IRS planning"},
        {"date_or_window": "Before sale/listing", "item": "Price transfer tax, recording fees, broker/closing costs, and repairs", "who": "Owner B + agent/attorney", "why": "Net proceeds can differ materially from gross sale price.", "source_type": "Local recorder/treasurer"},
        {"date_or_window": "Before receiving proceeds", "item": "Write investment policy statement (IPS) for sale proceeds", "who": "Owner B + adviser", "why": "Prevents ad hoc allocation and manages sequence/reinvestment risk.", "source_type": "Planning practice"},
        {"date_or_window": "Annual", "item": "Re-run model with updated valuations, tax law, insurance, rents, and spending", "who": "Owner B", "why": "Assumptions drift; laws change; decisions should be refreshed.", "source_type": "Planning practice"},
    ]


def main():
    model = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'assumptions': ASSUMPTIONS,
        'property_a_history_rounded': PROPERTY_A_HISTORY,
        'property_b_history_rounded': PROPERTY_B_HISTORY,
        'transfer_scenarios': build_transfer_scenarios(),
        'path_comparison_base': build_path_comparison(),
        'black_swan_scenarios': build_black_swan(),
        'deadlines': build_deadlines(),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(model, f, indent=2)
    print(f'Wrote {OUT}')

if __name__ == '__main__':
    main()
