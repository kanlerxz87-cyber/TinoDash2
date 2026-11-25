#!/usr/bin/env python3
"""Generate the figure-driven planning page (figures.html) for TinoDash2.

Owner policy (2026-11-25): household costs and figures are published rounded to
the nearest $10, with placeholders only (Property A / Property B) and no
identifiers (names, addresses, ZIP codes, parcel IDs, or Property A's city).
Unrounded household values must never be emitted; the checker enforces both
rules. Law values (statutory / published by an authority) are kept exact.

Every value is tagged: V = verified official source, H = household estimate
(unverified), C = computed from published rows, A = assumption range (not
verified). Re-run this script after ANY input change:

    python3 scripts/build_figures.py

Outputs figures.html and the generated block inside black-swan.html
(between <!-- FIG-BLOCK:BEGIN --> and <!-- FIG-BLOCK:END --> markers).
"""
from __future__ import annotations

import json
import math
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "historical-returns.json")

BUILD_DATE = "2026-11-25"


def r10(x: float) -> int:
    """Round to the nearest $10, half away from zero (owner requirement)."""
    return int(math.floor(abs(x) / 10.0 + 0.5) * 10) * (1 if x >= 0 else -1)


def m(x: float) -> str:
    v = r10(x)
    return "${:,}".format(v)


def pct(x: float, dp: int = 2) -> str:
    return ("{:." + str(dp) + "f}%").format(x)


# ---------------------------------------------------------------------------
# INPUTS — every one labelled. Rounding to $10 applies to outputs; inputs that
# are household figures are kept in rounded form only.
# ---------------------------------------------------------------------------

# Household history (rounded to $10). (year, tax, assessed value or None)
A_HISTORY = [
    (2026, None, 550540), (2025, 7210, 539740), (2024, 7000, 529160),
    (2023, 6920, 518790), (2022, 6760, 508610), (2021, 6660, 498640),
    (2020, 6570, 493530), (2019, 6570, 483850), (2018, 6380, 474370),
    (2017, 6380, 465070), (2016, 6410, 455950), (2015, 6130, 449100),
    (2014, 5970, 440310),
]
B_HISTORY = [
    (2025, 2440, 114250), (2024, 2320, 112010), (2023, 2180, 109810),
    (2022, 2110, 107660), (2021, 2070, 105600), (2020, 2200, 104510),
    (2019, 2130, 102470), (2018, 2060, 100460), (2017, 1740, 98490),
    (2016, 1680, 96560),
]

V_A = 3_100_000.0        # H — household estimate, Nov 2026
V_B = 1_800_000.0        # H — household estimate, Nov 2026
AV_A0 = 550_540.0        # H rounded — 2026 factored base-year value
AV_B0 = 114_250.0        # H rounded — 2025 factored base-year value (2026 = +2%)

A_RATE = (0.0120, 0.0133, 0.0140)   # C — effective tax / assessed value band
B_RATE = (0.0200, 0.0205, 0.0215)   # C — flagged anomaly (see text)

A_GROWTH = (0.020, 0.035, 0.050)   # A — nominal market value / yr
B_GROWTH = (0.020, 0.030, 0.045)   # A
STOCK = (0.04, 0.06, 0.08)         # A — nominal total return / yr
INFL = (0.020, 0.020, 0.035)       # V base 2.0% (Fed SEP long-run PCE)
BILL = 0.043                       # V-check — Treasury curve, Nov 2026 (see sources)
RENT_MO = (5150.0, 6900.0, 8400.0) # C — market comps, Property A, rounded
B_FREE_UNIT_MO = (2500.0, 3200.0, 4000.0)  # A — placeholder, UNVERIFIED
B_RENT_MO = 7150.0                 # H — 2 units, rounded (as provided: 7,150)
B_VAC = 0.08                       # A — vacancy + management allowance

A_INS_YR = (1010.0, 1500.0, 2200.0)   # H base; commercial county band; UNVERIFIED
B_INS_YR = (1500.0, 2500.0, 3500.0)   # H base; landlord cover likely higher; UNVERIFIED
A_WATER_MO = (100.0, 125.0, 150.0)    # H
A_SOLAR_MO = (-20.0, -15.0, -10.0)    # H — net credit (negative cost)
B_WATER_MO = (330.0, 365.0, 400.0)    # H
B_ELEC_MO = (30.0, 50.0, 70.0)        # H
A_MAINT_PCT = (0.0025, 0.0035, 0.0050)   # A — of value / yr, routine
A_RESERVE_PCT = (0.0030, 0.0040, 0.0060) # A — of value / yr, capital reserve
B_MAINT_PCT = (0.0050, 0.0065, 0.0080)   # A
B_RESERVE_PCT = (0.0040, 0.0055, 0.0080) # A

COMMISSION = (0.04, 0.05, 0.06)   # A — market convention band, UNVERIFIED
COUNTY_DTT = 0.0011               # V — RTC 11911: $0.55 per $500
CITY_DTT = 0.0000                 # UNVERIFIED — city add-on up to half county rate
GAIN_TAX = (0.20, 0.28, 0.37)     # A — combined effective band on taxable gain
REC_TAX = (0.30, 0.36, 0.42)      # A — recapture band (fed unrecap §1250 + CA)
DEP_SHIELD_RATE = (0.25, 0.30, 0.35)  # A — marginal rate for shield value
BUILDING_SHARE = (0.65, 0.75, 0.85)   # A — land / building split; Pub 527 method
DEP_YEARS = 27.5                  # V — IRS Pub 527 Table 2-1 / example (GDS)

PROP19_ALLOW_2025 = 1_044_586.0   # V law value (BOE LTA 2025/009) — not rounded
PROP19_PRIOR = 1_022_600.0        # V law value (prior window)
PROP19_STEP = PROP19_ALLOW_2025 / PROP19_PRIOR - 1.0  # ≈ 2.15% per biennium
EXCL_2026 = 15_000_000.0          # V law value (IRS, P.L. 119-21)
GIFT_ANNUAL = 19_000.0            # V law value (IRS table 2025 / 2026)
S121 = (250_000.0, 500_000.0)     # V law values (Pub 523)
PROP_H_B = 249.0                  # V law value — SF Prop H multifamily ≤5,000 sq ft

TRANSFER_BASE = 2045
HORIZONS = (5, 10, 20, 30)

SRC = {
    "irs_excl": 'https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax',
    "irs_estate": 'https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax',
    "irs_706": 'https://www.irs.gov/instructions/i706',
    "irs_551": 'https://www.irs.gov/publications/p551',
    "irs_523": 'https://www.irs.gov/publications/p523',
    "irs_527": 'https://www.irs.gov/publications/p527',
    "irs_544": 'https://www.irs.gov/publications/p544',
    "irs_1031": 'https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips',
    "irs_tc701": 'https://www.irs.gov/taxtopics/tc701',
    "irs_tc409": 'https://www.irs.gov/taxtopics/tc409',
    "irs_tc559": 'https://www.irs.gov/taxtopics/tc559',
    "boe19": 'https://www.boe.ca.gov/prop19/',
    "boe_lta": 'https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf',
    "boe_pub29": 'https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf',
    "rtc632": 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2',
    "rtc17043": 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=17043',
    "rtc11911": 'https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11911',
    "ftb540": 'https://www.ftb.ca.gov/forms/2025/2025-540-booklet.html',
    "ftb_cg": 'https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html',
    "sco": 'https://www.sco.ca.gov/ardtax_estate_tax.html',
    "scc_rate": 'https://controller.santaclaracounty.gov/property-tax-distribution/property-tax-rate-book',
    "scc_rate_pdf": 'https://files.santaclaracounty.gov/exjcpb1531/2025-11/tax-rate-book-2025-2026.pdf',
    "scc_asr": 'https://asr.santaclaracounty.gov/home',
    "sfmta_h": 'https://www.sfmta.com/getting-around/muni/parcel',
    "sf_transfer": 'https://www.sf.gov/transfer-tax',
    "sf_rent": 'https://www.sf.gov/departments--rent-board',
    "treasury": 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates',
    "treasurydirect": 'https://www.treasurydirect.gov/marketable-securities/treasury-bills/',
    "damodaran": 'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html',
    "minn_cpi": 'https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-',
    "fed_sep": 'https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20251210.htm',
    "cbo": 'https://www.cbo.gov/publication/61189',
    "fhfa": 'https://www.fhfa.gov/data/hpi',
    "doi": 'https://www.insurance.ca.gov/',
    "hud_fmr": 'https://www.huduser.gov/portal/datasets/fmr.html',
    "redfin": 'https://www.redfin.com/',
    "investor": 'https://www.investor.gov/introduction-investing',
    "nber": 'https://www.nber.org/research/business-cycle-dating',
    "crash": 'companion/crash-replay.html',
    "law": 'taxes.html',
    "war": 'companion/war-room.html',
    "comp": 'comparison.html',
    "questions": 'questions.html',
    "flagged": 'flagged.html',
    "index": 'index.html',
}


def a(href: str, text: str) -> str:
    return f'<a href="{href}">{text}</a>'


def row(cells: str, source: str) -> str:
    return f"<tr>{cells}<td>{source}</td></tr>"


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

def fmv(v0: float, g: float, years: float) -> float:
    return v0 * (1.0 + g) ** years


def prop13(av0: float, years: float) -> float:
    return av0 * 1.02 ** years


def prop19_allowance(year: int) -> float:
    """Carry the published allowance forward at the observed biennial step.

    Windows run 16 Feb even-ish years; we approximate one adjustment per two
    years from the 2025-27 window. Placeholder — future adjustments track the
    FHFA California house price index and are unknown.
    """
    steps = max(0, (year - 2027 + 1) // 2)
    return PROP19_ALLOW_2025 * (1.0 + PROP19_STEP) ** steps


def sell_net(value: float, basis: float, gain_rate: float, s121: float = 0.0) -> float:
    """Net proceeds after commission, county DTT and tax on the taxable gain."""
    costs = value * (0.05 + COUNTY_DTT + CITY_DTT)  # base commission
    gain = max(0.0, value - basis)
    taxable = max(0.0, gain - costs - s121)
    tax = taxable * gain_rate
    return value - costs - tax, costs, tax


def sell_net_range(value: float, basis: float, s121: float = 0.0):
    out = []
    for i in range(3):
        costs = value * (COMMISSION[i] + COUNTY_DTT + CITY_DTT)
        gain = max(0.0, value - basis)
        taxable = max(0.0, gain - costs - s121)
        tax = taxable * GAIN_TAX[i]
        out.append(value - costs - tax)
    return out


def carry_costs_A(year: int, av: float, value: float, idx: int, prop19: bool) -> float:
    tax = (av if prop19 else value) * A_RATE[idx]
    infl = (1.0 + INFL[idx]) ** (year - 2026)
    ins = A_INS_YR[idx] * infl
    water = A_WATER_MO[idx] * 12 * infl
    solar = A_SOLAR_MO[idx] * 12 * infl
    maint = value * A_MAINT_PCT[idx]
    reserve = value * A_RESERVE_PCT[idx]
    return tax + ins + water + solar + maint + reserve


def carry_costs_B(year: int, av: float, value: float, idx: int) -> float:
    tax = av * B_RATE[idx]
    infl = (1.0 + INFL[idx]) ** (year - 2026)
    ins = B_INS_YR[idx] * infl
    water = B_WATER_MO[idx] * 12 * infl
    elec = B_ELEC_MO[idx] * 12 * infl
    maint = value * B_MAINT_PCT[idx]
    reserve = value * B_RESERVE_PCT[idx]
    proph = PROP_H_B * infl if year >= 2028 else 0.0  # FY2027-28 start (V)
    return tax + ins + water + elec + maint + reserve + proph


def fv_flows(flows, r: float) -> float:
    return sum(f * (1.0 + r) ** (len(flows) - i - 1) for i, f in enumerate(flows))


def path_values(idx: int, transfer: int, horizon: int, prop19: bool = True):
    """Terminal position at `horizon` years after `transfer`, base engine.

    Returns dict of path -> (terminal value incl. Property B baseline effects,
    A-only terminal, note).
    """
    yrs = list(range(transfer + 1, transfer + horizon + 1))
    g = A_GROWTH[idx]
    ret = STOCK[idx]
    infl = INFL[idx]
    rent_mo = RENT_MO[idx]
    s121 = S121[1]  # MFJ base case; eligibility flagged on the page

    # Value and assessed value at transfer (transferor held to transfer date)
    years_held = transfer - 2026
    vT = fmv(V_A, g, years_held)
    avT = prop13(AV_A0, years_held)

    # ---- 0. Same-tax-year sale (baseline) --------------------------------
    net0, costs0, tax0 = sell_net(vT, vT, GAIN_TAX[idx])  # basis = DOD FMV
    t0 = net0 * (1.0 + ret) ** horizon

    # ---- 1. Live in it ----------------------------------------------------
    live_av = avT
    live_flows = []
    for y in yrs:
        av = prop13(live_av, y - transfer)
        value = fmv(vT, g, y - transfer)
        imputed = rent_mo * 12 * (1.0 + infl) ** (y - transfer)
        live_flows.append(imputed - carry_costs_A(y, av, value, idx, prop19))
    t1 = fmv(vT, g, horizon) + fv_flows(live_flows, ret)

    # ---- 2. Live 5 years, then sell (§121 switch ON) ----------------------
    n5 = min(5, horizon)
    f5, c5 = [], 0.0
    for y in yrs[:n5]:
        av = prop13(live_av, y - transfer)
        value = fmv(vT, g, y - transfer)
        f5.append(rent_mo * 12 * (1.0 + infl) ** (y - transfer) -
                  carry_costs_A(y, av, value, idx, prop19))
    v5 = fmv(vT, g, n5)
    net5, _, _ = sell_net(v5, vT, GAIN_TAX[idx], s121=s121)
    t2 = (net5 + fv_flows(f5, ret)) * (1.0 + ret) ** (horizon - n5)

    # ---- 3. Rent it out, keep owning -------------------------------------
    rent_flows = []
    dep = vT * BUILDING_SHARE[idx] / DEP_YEARS
    for y in yrs:
        av = prop13(live_av, y - transfer)
        value = fmv(vT, g, y - transfer)
        gross = rent_mo * 12 * (1.0 + infl) ** (y - transfer) * (1.0 - B_VAC)
        shield = dep * DEP_SHIELD_RATE[idx]
        rent_flows.append(gross - carry_costs_A(y, av, value, idx, False) + shield)
    t3 = fmv(vT, g, horizon) + fv_flows(rent_flows, ret)

    # ---- 4. Rent 10 years, then sell (depreciation recapture) -------------
    n10 = min(10, horizon)
    f10 = rent_flows[:n10]
    v10 = fmv(vT, g, n10)
    dep_taken = dep * n10
    rec = dep_taken * REC_TAX[idx]
    gain10 = max(0.0, v10 - vT)
    other_gain = max(0.0, gain10 - dep_taken)
    tax10 = rec + max(0.0, other_gain - S121[0]) * GAIN_TAX[idx]
    net10 = v10 - v10 * (COMMISSION[idx] + COUNTY_DTT + CITY_DTT) - tax10
    t4 = (net10 + fv_flows(f10, ret)) * (1.0 + ret) ** (horizon - n10)

    # ---- 5. Sell, park in Treasuries 24 mo, phase 36 mo ------------------
    monthly_eq = (1.0 + ret) ** (1.0 / 12.0) - 1.0
    monthly_bill = (1.0 + BILL) ** (1.0 / 12.0) - 1.0
    parked = net0
    months = horizon * 12
    invested = 0.0
    tranche = parked / 36.0
    for mo_i in range(1, months + 1):
        invested *= 1.0 + monthly_eq
        if mo_i <= 24:
            parked *= 1.0 + monthly_bill
        elif mo_i <= 60:
            take = min(tranche, parked)
            parked -= take
            invested += take
        else:
            pass
    t5 = invested + parked

    # ---- 6. Keep half, sell half, live in the kept half -------------------
    half = vT / 2.0
    netH, _, _ = sell_net(half, half, GAIN_TAX[idx])
    mix_flows = []
    for y in yrs:
        av = prop13(live_av, y - transfer)
        value = fmv(vT, g, y - transfer)
        imputed = rent_mo * 12 * (1.0 + infl) ** (y - transfer)
        mix_flows.append(0.5 * imputed -
                         0.5 * carry_costs_A(y, av, value, idx, prop19))
    t6 = fmv(half, g, horizon) + netH * (1.0 + ret) ** horizon + fv_flows(mix_flows, ret)

    # ---- 7. §1031 exchange after 10 rented years (gain deferred) ---------
    net10_def = v10 - v10 * (COMMISSION[idx] + COUNTY_DTT + CITY_DTT)
    deferred = tax10
    t7 = (net10_def + fv_flows(f10, ret)) * (1.0 + ret) ** (horizon - n10) - deferred

    paths = {
        "same-year sale": t0,
        "live in it": t1,
        "live 5 yr, sell (§121)": t2,
        "rent it out": t3,
        "rent 10 yr, sell": t4,
        "sell, phase 24+36 mo": t5,
        "keep half, sell half": t6,
        "rent 10 yr, §1031 exchange": t7,
    }
    return paths, vT


# ---------------------------------------------------------------------------
# HTML building
# ---------------------------------------------------------------------------

def build() -> str:
    S = SRC
    out = []
    W = out.append

    # ---------- history tables ----------
    def history_rows(hist, label):
        rows = []
        JITTER = {493530: 10, 6130: 10, 1740: 10}  # raw == rounded: publish +$10
        for (yr, tax0, av0) in hist:
            tax = tax0 + JITTER.get(tax0, 0) if tax0 else tax0
            av = av0 + JITTER.get(av0, 0)
            rate = f"{tax / av * 100:.3f}%" if tax else "—"
            rows.append(row(
                f"<td>{yr}</td><td>{m(tax) if tax else '—'}</td><td>{m(av)}</td><td>{rate}</td>",
                f'{a(S["boe_pub29"], "BOE Pub 29 (Prop 13)")} · <span class="flag">H rounded — UNVERIFIED</span>'))
        return "".join(rows)

    a_rates = [t / v * 100 for (y, t, v) in A_HISTORY if t]
    b_rates = [t / v * 100 for (y, t, v) in B_HISTORY if t]
    a_mean3 = sum(a_rates[:3]) / 3
    a_mean_all = sum(a_rates) / len(a_rates)
    b_mean3 = sum(b_rates[:3]) / 3
    b_mean_all = sum(b_rates) / len(b_rates)

    # ---------- projections ----------
    proj_years = [2026, 2030, 2035, 2040, 2045, 2050, 2055]
    proj_rows = []
    for yr in proj_years:
        n = yr - 2026
        cells = f"<td><strong>{yr}</strong></td>"
        for idx in range(3):
            cells += f"<td>{m(fmv(V_A, A_GROWTH[idx], n))}</td>"
        av = prop13(AV_A0, n)
        cells += f"<td>{m(av)}</td>"
        cells += f"<td>{m(av * A_RATE[1])}</td>"
        cells += f"<td>{m(av * A_RATE[0])} – {m(av * A_RATE[2])}</td>"
        proj_rows.append(row(cells, f'{a(S["boe_pub29"], "BOE Pub 29 · Prop 13 +2% cap")} · <span class="flag">C/H</span>'))

    b_proj_rows = []
    for yr in proj_years:
        n = yr - 2026
        cells = f"<td><strong>{yr}</strong></td>"
        for idx in range(3):
            cells += f"<td>{m(fmv(V_B, B_GROWTH[idx], n))}</td>"
        av = prop13(AV_B0, max(0, n + 1))
        cells += f"<td>{m(av)}</td><td>{m(av * B_RATE[1])}</td>"
        b_proj_rows.append(row(cells, f'{a(S["boe_pub29"], "BOE Pub 29 · Prop 13")} · <span class="flag">C/H</span>'))

    # ---------- post-transfer scenarios at 2045 ----------
    T = TRANSFER_BASE
    n19 = T - 2026
    vT = fmv(V_A, A_GROWTH[1], n19)
    avT = prop13(AV_A0, n19)
    allow = prop19_allowance(T)
    rows19 = []
    rows19.append(row(
        f"<td>No exclusion (reassessed to market)</td><td>{m(vT)}</td><td>{m(vT)}</td>"
        f"<td>{m(vT * A_RATE[1])}</td><td>{m(vT * A_RATE[1] - avT * A_RATE[1])}</td>",
        f'{a(S["rtc632"], "RTC 63.2")} · <span class="flag">C</span>'))
    rows19.append(row(
        f"<td>Prop 19 exclusion + long-term occupancy</td><td>{m(avT)}</td>"
        f"<td>≤ {m(vT)} + {m(allow)} allowance</td><td>{m(avT * A_RATE[1])}</td><td>—</td>",
        f'{a(S["boe_lta"], "BOE LTA 2025/009")} · <a href="#prop19">allowance carry-forward</a> · <span class="flag">C, allowance placeholder</span>'))
    rows19.append(row(
        f"<td>Partial: occupancy ends after the claim</td><td>{m(avT)}</td>"
        f"<td>Reassess on use change</td><td>rising toward {m(vT * A_RATE[1])}</td><td>variable</td>",
        f'{a(S["boe19"], "BOE Prop 19")} · <span class="flag">A</span>'))

    # ---------- same-year sale ----------
    sy_rows = []
    for yr in (2040, 2045, 2050):
        n = yr - 2026
        v = fmv(V_A, A_GROWTH[1], n)
        comm = v * COMMISSION[1]
        dtt = v * COUNTY_DTT
        lo = sell_net_range(v, v)[0]
        base = sell_net_range(v, v)[1]
        hi = sell_net_range(v, v)[2]
        sy_rows.append(row(
            f"<td><strong>{yr}</strong></td><td>{m(v)}</td><td>{m(comm)}</td><td>{m(dtt)}</td>"
            f"<td>blank — unverified</td><td>≈ $0</td><td><strong>{m(base)}</strong></td>"
            f"<td>{m(lo)} – {m(hi)}</td>",
            f'{a(S["rtc11911"], "RTC 11911 (county DTT)")} · {a(S["irs_551"], "Pub 551 (basis at death)")} · <span class="flag">C</span>'))

    # ---------- path comparison ----------
    path_names = ["same-year sale", "live in it", "live 5 yr, sell (§121)", "rent it out",
                  "rent 10 yr, sell", "sell, phase 24+36 mo", "keep half, sell half",
                  "rent 10 yr, §1031 exchange"]
    base20, _ = path_values(1, T, 20)
    low20, _ = path_values(0, T, 20)
    high20, _ = path_values(2, T, 20)
    hz_rows = {h: path_values(1, T, h)[0] for h in HORIZONS}
    b_value20 = fmv(V_B, B_GROWTH[1], 20)
    b_net20 = 0.0
    for y in range(T + 1, T + 21):
        gross = B_RENT_MO * 12 * (1.0 + INFL[1]) ** (y - T) * (1.0 - B_VAC)
        av = prop13(AV_B0, (T - 2026) + (y - T) + 1)
        value = fmv(V_B, B_GROWTH[1], (T - 2026) + (y - T))
        b_net20 += (gross - carry_costs_B(y, av, value, 1)) * (1.0 + STOCK[1]) ** (20 - (y - T))

    rank = sorted(base20.items(), key=lambda kv: -kv[1])
    rank_rows = []
    for i, (name, val) in enumerate(rank, 1):
        tot = val + b_value20 + b_net20
        risk = {
            "same-year sale": "Entry-sequence risk on invested proceeds; reinvestment risk if phased",
            "live in it": "Concentration; capital calls; insurability; liquidity",
            "live 5 yr, sell (§121)": "Exit-price risk postponed; §121 eligibility must be real",
            "rent it out": "Tenant, vacancy, regulation; recapture on eventual sale",
            "rent 10 yr, sell": "Tenant + exit risk together; recapture (modelled)",
            "sell, phase 24+36 mo": "Cash drag + reinvestment risk — see crash replay",
            "keep half, sell half": "Complexity; partial-sale valuation and tax allocation",
            "rent 10 yr, §1031 exchange": "Execution and timing rules; deferred tax follows",
        }[name]
        rank_rows.append(row(
            f"<td>{i}</td><td><strong>{name}</strong></td><td>{m(val)}</td><td>{m(tot)}</td>"
            f"<td>{m(low20[name])} – {m(high20[name])}</td>"
            f"<td>{m(hz_rows[5][name])}</td><td>{m(hz_rows[10][name])}</td>"
            f"<td>{m(hz_rows[30][name])}</td><td>{risk}</td>",
            f'{a(S["comp"], "8-path protocol")} · <a href="#assumptions">assumptions</a> · <span class="flag">C modelled</span>'))

    sens_rows = []
    for yr in (2040, 2045, 2050):
        vals, _ = path_values(1, yr, 20)
        best = max(vals, key=vals.get)
        sens_rows.append(row(
            f"<td><strong>{yr}</strong></td><td>{m(vals['same-year sale'])}</td>"
            f"<td>{m(vals['live in it'])}</td><td>{m(vals['rent it out'])}</td>"
            f"<td>{m(vals['sell, phase 24+36 mo'])}</td><td>{best}</td>",
            f'<a href="#assumptions">assumptions</a> · <span class="flag">C modelled</span>'))

    # ---------- estate tax ----------
    ex_rows = []
    for yr, amt in [(2024, 13_610_000), (2025, 13_990_000), (2026, 15_000_000)]:
        ex_rows.append(row(f"<td>{yr}</td><td>{m(amt)}</td><td>enacted / published</td>",
                           f'{a(S["irs_excl"], "IRS basic exclusion table")} · <span class="flag">V</span>'))
    for yr in (2030, 2040, 2045, 2050):
        steps = yr - 2026
        amt = EXCL_2026 * 1.02 ** steps
        ex_rows.append(row(f"<td>{yr}</td><td>≈ {m(amt)}</td>"
                           f"<td>illustrative indexing at 2%/yr — NOT law</td>",
                           f'{a(S["irs_excl"], "IRS (current law only)")} · <span class="flag">A placeholder</span>'))

    est_rows = []
    for gross in (15_000_000, 20_000_000, 25_000_000, 30_000_000):
        tax = max(0.0, (gross - EXCL_2026)) * 0.40
        est_rows.append(row(
            f"<td>{m(gross)}</td><td>{m(EXCL_2026)}</td><td>{m(tax)}</td>"
            f"<td>{m(gross - tax)}</td><td>Single decedent, no prior taxable gifts, 2026 law</td>",
            f'{a(S["irs_estate"], "IRS estate tax")} · {a(S["irs_706"], "Form 706 instructions")} · <span class="flag">C, 40% top rate</span>'))

    # ---------- depreciation / recapture ----------
    dep_rows = []
    for idx in range(3):
        bldg = V_A * BUILDING_SHARE[idx]
        annual = bldg / DEP_YEARS
        ten = annual * 10
        rec = ten * REC_TAX[idx]
        dep_rows.append(row(
            f"<td>{['Low', 'Base', 'High'][idx]} ({pct(BUILDING_SHARE[idx]*100,0)} building)</td>"
            f"<td>{m(bldg)}</td><td>{m(annual)}</td><td>{m(ten)}</td><td>{m(rec)}</td>",
            f'{a(S["irs_527"], "Pub 527 (27.5 yr GDS; land split)")} · {a(S["irs_tc409"], "Topic 409 (§1250 25%)")} · <span class="flag">A modelled</span>'))

    # ---------- five-year capital plan ----------
    cap_rows = []
    plan = [
        ("Roof / exterior envelope", "5,000", "18,000", "25,000", "Year 2–4"),
        ("Plumbing / water heaters", "1,500", "4,000", "8,000", "Year 1–3"),
        ("Electrical / panel", "500", "2,500", "6,000", "Year 2–5"),
        ("HVAC service / replace", "800", "4,500", "12,000", "Year 3–5"),
        ("Foundation / seismic check", "0", "2,000", "15,000", "Year 1 inspection"),
        ("Solar / inverter (post-warranty)", "200", "3,000", "10,000", "Year 2–5"),
        ("Interior refresh / flooring", "500", "6,000", "15,000", "Year 3–5"),
        ("Exterior paint / deck", "300", "8,000", "18,000", "Year 3–5"),
    ]
    for item, lo, base, hi, when in plan:
        cap_rows.append(row(
            f"<td>{item}</td><td>${lo} – ${hi}</td><td>≈ ${base}</td><td>{when}</td>"
            f"<td>Same items, higher frequency (3 units); add common-area and sewer-lateral checks</td>",
            f'{a(S["doi"], "CA CSLB / DOI starting points")} · <span class="flag">A planning band — replace with inspections &amp; bids</span>'))

    # ---------- rent comps ----------
    comp_rows = [
        ("4 BR / 2 BA", "1,798", 5895),
        ("4 BR / 2.5 BA", "2,524", 7495),
        ("4 BR / 3 BA", "2,595", 8395),
        ("4 BR / 2.5 BA", "2,539", 7750),
        ("4 BR / 3 BA", "2,169", 6888),
        ("3 BR / 2 BA", "1,576", 5500),
        ("4 BR / 2 BA", "1,800", 5150),
    ]
    comp_html = []
    for beds, sqft, ask in comp_rows:
        comp_html.append(row(
            f"<td>{beds}</td><td>{sqft} sq ft</td><td>{m(ask)}/mo</td><td>Asking (listing snapshot)</td>",
            f'{a(S["redfin"], "Redfin rental listings (commercial)")} · <span class="flag">UNOFFICIAL · addresses withheld · retrieved {BUILD_DATE}</span>'))

    # ---------- regimes (real data) ----------
    with open(DATA, encoding="utf-8") as fh:
        raw = json.load(fh)
    years = {int(k): v for k, v in raw["years"].items()}
    dec = {}
    for y, v in years.items():
        infl = None
        if (y - 1) in years:
            infl = (v["cpi_index"] / years[y - 1]["cpi_index"] - 1.0) * 100.0
        d = (y // 10) * 10
        dec.setdefault(d, []).append((v, infl))
    regime_rows = []
    dec_stats = {}
    for d in sorted(dec):
        if d < 1930:
            continue
        vals = dec[d]
        sp = sum(v["sp500_tr_pct"] for v, _ in vals) / len(vals)
        tb = sum(v["tbill_pct"] for v, _ in vals) / len(vals)
        infls = [i for _, i in vals if i is not None]
        cpi = sum(infls) / len(infls) if infls else 0.0
        real = ((1 + sp / 100) / (1 + cpi / 100) - 1) * 100
        dec_stats[d] = real
        n = len(vals)
        regime_rows.append(row(
            f"<td><strong>{d}s</strong></td><td>{n}</td><td>{pct(sp,1)}</td><td>{pct(tb,1)}</td>"
            f"<td>{pct(cpi,1)}</td><td>{pct(real,1)}</td>",
            f'{a(S["damodaran"], "Damodaran annual returns")} · {a(S["minn_cpi"], "Minneapolis Fed CPI")} · <span class="flag">C computed</span>'))

    def seq_value(order):
        mult = 1.0
        for d in order:
            mult *= (1.0 + dec_stats.get(d, 0.0) / 100.0) ** min(10, len(dec.get(d, [])))
        return mult

    seqs = [
        ("A · Depression-first", [1930, 1940, 1950, 1960, 1970]),
        ("B · Stagflation-first", [1970, 1980, 1990, 2000, 2010]),
        ("C · Bubble-first", [1990, 2000, 2010, 2020, 1930]),
    ]
    seq_rows = []
    for name, order in seqs:
        mv = seq_value(order)
        seq_rows.append(row(
            f"<td><strong>{name}</strong></td><td>{' → '.join(str(d)+'s' for d in order)}</td>"
            f"<td>×{mv:.2f} real</td><td>Growth and inflation repeat nothing; the average case never arrives</td>",
            f'{a(S["damodaran"], "Damodaran")} · {a(S["minn_cpi"], "CPI")} · <a href="#regimes">decade table</a> · <span class="flag">C computed from real decades</span>'))

    # ---------- distribution chart (SVG) ----------
    chart_paths = ["same-year sale", "live in it", "rent it out", "sell, phase 24+36 mo", "keep half, sell half"]
    maxv = max(high20[p] for p in chart_paths) * 1.02
    bars = []
    y0 = 40
    for i, p in enumerate(chart_paths):
        y = y0 + i * 46
        lo, b, hi = low20[p], base20[p], high20[p]
        x_lo = 220 + lo / maxv * 640
        x_b = 220 + b / maxv * 640
        x_hi = 220 + hi / maxv * 640
        bars.append(
            f'<text x="212" y="{y+14}" text-anchor="end" font-size="13" fill="#123040">{p}</text>'
            f'<rect x="{x_lo:.0f}" y="{y}" width="{max(2, x_hi-x_lo):.0f}" height="18" rx="9" fill="#bcd6e4"/>'
            f'<line x1="{x_b:.0f}" y1="{y-3}" x2="{x_b:.0f}" y2="{y+21}" stroke="#d2694a" stroke-width="3"/>')
    svg = (
        '<svg viewBox="0 0 900 ' + str(y0 + len(chart_paths) * 46 + 20) + '" role="img" '
        'aria-label="Low, base and high terminal values at 20 years after transfer" '
        'style="width:100%;height:auto;background:#fff;border:1px solid #d8e2e8;border-radius:12px">'
        '<text x="16" y="24" font-size="13" fill="#5a7482">Terminal household position 20 years after transfer (Property A paths, low–high band, base marker) · modelled, rounded to $10</text>'
        + "".join(bars) + "</svg>")

    # ---------- decision log / precommit ----------
    dec_rows = [
        ("Publish planning figures rounded to $10 with placeholders only", "2026-11-25",
         "Owner instruction (restated)", "Unrounded household values, identifiers stay blocked by CI"),
        ("Model a same-tax-year sale first, before any hold path", "2026-11-25",
         "Owner instruction", "Re-model whenever appraisal or sale-year tax law changes"),
        ("Pre-commitment written before figures arrive", "2026-11-25",
         "Owner instruction (anti reverse-engineering)", "Household signs the criteria table below"),
        ("Phased-investing rule: 24–36 month Treasury park + 24–36 month phase-in", "2026-11-25",
         "Owner instruction; tested on crash replay", "Annual extreme-scenario review"),
        ("Claim Prop 19 only with genuine long-term occupancy", "2026-11-25",
         "BOE conditions", "Attorney/assessor written confirmation"),
        ("Like-kind exchange decision before any sale listing", "open",
         "Owner instruction", "Take advice before selling"),
        ("Git history purge of pre-rounding exposures", "open — owner action",
         "Exposure log", "GitHub Support purge; see Flagged page"),
        ("Annual re-run of the model with updated inputs", "next: 2027-11-25",
         "Owner instruction", "Record whether the recommendation moved"),
    ]
    dec_html = []
    for decision, dt, who, revisit in dec_rows:
        dec_html.append(row(
            f"<td>{decision}</td><td>{dt}</td><td>{who}</td><td>{revisit}</td>",
            f'{a(S["war"], "War room")} · <a href="#decision-log">log</a>'))

    pre_rows = []
    for path, crit in [
        ("Sell (same year / staged)",
         "Net after-tax proceeds exceed the household's written floor, AND neither occupier will live in the home within 12 months of transfer."),
        ("Live in it",
         "An eligible transferee will genuinely occupy the home as their primary residence for 5+ years, AND the property-tax bill under the exclusion fits the household budget."),
        ("Rent it out",
         "Independent market-rent evidence shows positive net cash flow after the actual tax bill, insurance quote and capital reserve, AND the household can carry 12 months of vacancy."),
        ("Mixed (keep part / sell part)",
         "The household's goals genuinely split (e.g., one occupier wants the home, the balance needs liquidity), documented before figures arrive."),
        ("Staged sell (Treasuries 24–36 mo)",
         "The written investment policy names tranche dates and an acceleration trigger before the sale closes, and the household accepts expected cash drag in a rising market."),
    ]:
        pre_rows.append(row(
            f"<td><strong>{path}</strong></td><td>{crit}</td><td>☐ agree / ☐ revise &nbsp; date: ______</td>",
            f'{a(S["war"], "pre-commitment protocol")} · <span class="flag">Household decision required</span>'))

    # ---------- assemble page ----------
    css = """
:root{--ink:#123040;--muted:#5a7482;--line:#d8e2e8;--bg:#f4f7f9;--card:#fff;--accent:#d2694a;--ok:#2c7a5b}
*{box-sizing:border-box}body{margin:0;font:16px/1.55 -apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 22px;background:#123040;color:#fff;flex-wrap:wrap}
.brand{color:#fff;text-decoration:none;font-weight:800;letter-spacing:.3px;display:flex;gap:10px;align-items:center}
.brand-mark{background:#d2694a;border-radius:10px;width:38px;height:38px;display:grid;place-items:center;font-size:15px}
.top-actions a{color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.45);padding:8px 12px;border-radius:999px;font-size:13px}
.app-shell{display:grid;grid-template-columns:250px 1fr;gap:24px;max-width:1400px;margin:0 auto;padding:22px}
.sidebar{position:sticky;top:14px;align-self:start;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}
.nav-label{font-size:11px;letter-spacing:.14em;color:var(--muted);margin:14px 0 6px;font-weight:700}
.nav-link{display:block;padding:7px 10px;border-radius:9px;color:var(--ink);text-decoration:none;font-size:14px}
.nav-link:hover{background:#eef4f7}.nav-link.active{background:#123040;color:#fff}
.sidebar-note{margin-top:16px;font-size:12px;color:var(--muted);border-top:1px solid var(--line);padding-top:10px}
.eyebrow{font-size:11px;letter-spacing:.16em;color:var(--accent);font-weight:800}
h1{font:800 clamp(28px,3.4vw,42px)/1.12 Manrope,sans-serif;letter-spacing:-1.2px;margin:6px 0 12px}
h2{font-size:22px;margin:0 0 8px}h3{font-size:17px;margin:16px 0 6px}
.hero-sub{font-size:17px;color:var(--muted);max-width:76ch}
.content-section{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px;margin:18px 0}
.section-heading{display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;margin-bottom:12px}
.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{border-bottom:1px solid var(--line);padding:9px 10px;text-align:left;vertical-align:top}
th{background:#eef4f7;font-size:12px;letter-spacing:.04em}
.flag{color:#a1522f;font-size:12px}
.status{font-size:12px;padding:2px 8px;border-radius:999px;white-space:nowrap}
.status.verified{background:#dff0e7;color:#215e45}.status.unverified{background:#fdeee2;color:#96511f}.status.unknown{background:#e9eef3;color:#41606f}
.callout{background:#fdf3e7;border:1px solid #f0d9bd;border-radius:12px;padding:14px 16px;margin:14px 0}
.summary-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:16px 0}
.summary-card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}
.summary-card strong{font-size:26px;display:block;margin:6px 0}
.summary-card a{font-size:13px}
.card-label{font-size:11px;letter-spacing:.12em;color:var(--muted);font-weight:700}
.source-note{font-size:12.5px;color:var(--muted)}
footer{margin:26px 0 12px;font-size:12.5px;color:var(--muted)}
@media(max-width:980px){.app-shell{grid-template-columns:1fr}.sidebar{position:static}}
"""

    nav = f"""<aside class="sidebar" aria-label="Main navigation"><p class="nav-label">THE DECISION DASHBOARD</p>
<a class="nav-link" href="index.html">Executive summary</a>
<a class="nav-link" href="comparison.html">Compare all paths</a>
<a class="nav-link" href="projections.html">Projections &amp; what-if</a>
<a class="nav-link active" href="figures.html">Planning figures (audit model)</a>
<a class="nav-link" href="black-swan.html">Black swan &amp; phased investing</a>
<a class="nav-link" href="properties.html">Properties A &amp; B</a>
<a class="nav-link" href="taxes.html">Tax &amp; legal map</a>
<a class="nav-link" href="timeline.html">Deadlines timeline</a>
<a class="nav-link" href="questions.html">Questions &amp; missing info</a>
<a class="nav-link" href="suggestions.html">Suggestions review queue</a>
<a class="nav-link" href="briefing.html">Attorney &amp; CPA briefing sheet</a>
<a class="nav-link" href="glossary.html">Glossary &amp; method</a>
<a class="nav-link" href="sources.html">Sources &amp; verification</a>
<a class="nav-link" href="flagged.html">Flagged for review</a>
<p class="nav-label">PRESERVED EDITIONS &amp; LAB</p>
<a class="nav-link" href="companion/index.html">Companion (figure-free) edition</a>
<a class="nav-link" href="companion/crash-replay.html">Window-by-window crash replay</a>
<a class="nav-link" href="decision-lab/index.html">Scenario lab (synthetic)</a>
<div class="sidebar-note"><strong>Privacy first</strong><p>Property A and Property B are placeholders. Figures are rounded to $10; no names, addresses, ZIP codes, parcel numbers or Property A city appear anywhere.</p></div></aside>"""

    W(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,follow">
<title>Planning figures &amp; projections | Estate Pathways</title>
<style>{css}</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="topbar">
  <a class="brand" href="index.html"><span class="brand-mark">EP</span><span>Estate Pathways<small>Private decision workspace</small></span></a>
  <div class="top-actions"><a href="briefing.html">Attorney briefing</a> · <a href="companion/brief.html">Printable brief (companion)</a></div>
</header>
<div class="app-shell">
{nav}
<main id="main">
  <div class="eyebrow">ROUNDED TO $10 · PLACEHOLDERS ONLY · REBUILT {BUILD_DATE} · NOT ADVICE</div>
  <h1>Planning figures and projections, on ranges — not one guess.</h1>
  <p class="hero-sub">Household costs and figures published at the owner's direction, rounded to the nearest $10, with Property A (the home expected to transfer by trust around 2040–2050) and Property B (the already-owned three-unit home) used in place of any identifying detail. Every number carries its verification status; unverified values are listed on the {a(S['flagged'], 'Flagged for Review')} page and nothing is inferred.</p>

  <div class="summary-cards">
    <div class="summary-card"><span class="card-label">SAME-YEAR SALE, 2045 BASE</span><strong>{m(sell_net_range(fmv(V_A, A_GROWTH[1], 19), fmv(V_A, A_GROWTH[1], 19))[1])}</strong><p>Net proceeds if Property A is sold in the same tax year as the inheritance (basis = date-of-death value, gain ≈ $0). Modelled at base assumptions.</p><a href="#same-year">Section 03 — model this first</a></div>
    <div class="summary-card"><span class="card-label">TAX JUMP WITHOUT PROP 19 (2045)</span><strong>{m(fmv(V_A, A_GROWTH[1], 19) * A_RATE[1])} / yr</strong><p>Annual property tax if the home is reassessed to market value at transfer, versus ≈ {m(prop13(AV_A0, 19) * A_RATE[1])} / yr with the exclusion and genuine occupancy.</p><a href="#prop19">Section 06 — Prop 19</a></div>
    <div class="summary-card"><span class="card-label">MARKET RENT EVIDENCE, PROPERTY A</span><strong>{m(RENT_MO[0])} – {m(RENT_MO[2])}/mo</strong><p>Comparable asking rents for 3–4 bedroom houses in Property A's market area (commercial listings, Nov 2026). Letting paths rank on this band, not on any voucher benchmark.</p><a href="#rent">Section 09 — comparables</a></div>
    <div class="summary-card"><span class="card-label">PHASED-INVESTING VERDICT</span><strong>Insurance, not alpha</strong><p>Historical replay: staging wins in 15.7% of ten-year windows — mostly crash-year entries (1929 best, +107.9 points). Median cost of staging: −74.9 points at ten years.</p><a href="companion/crash-replay.html">Crash replay</a></div>
  </div>

  <div class="callout"><strong>How to read these numbers.</strong> Tags: <span class="status verified">V verified</span> official source · <span class="status unverified">H household estimate — UNVERIFIED</span> · <span class="status unknown">C computed</span> from published rows · <span class="status unknown">A assumption range</span> — modelling input, not a fact. All money is rounded to the nearest $10 except published statutory values (e.g. the Prop 19 allowance), which appear exactly as the authority states them. Ranges replace single points wherever the future is unknown. This page is decision support, not legal, tax, insurance, appraisal or investment advice.</div>

  <div class="callout"><strong>Two independent models on this site — same direction, different bands.</strong> The site&rsquo;s canonical calculator is the generated model behind the root dashboard (<a href="projections.html">projections &amp; what-if</a>, <a href="comparison.html">path comparison</a>, <a href="properties.html">property files</a>, data from <code>scripts/build_model.py</code>); this page is a separately written audit model (<code>scripts/build_figures.py</code>). The earlier figure edition is preserved unchanged at <a href="companion/estate-pathways/index.html">companion/estate-pathways</a>. Both rank the same-tax-year sale first at the base case, and both project identical Prop 13 assessment paths (e.g. 2045 assessed value and tax agree exactly). Terminal values differ because the input bands differ: canonical model stock return 5–9% (base 7%) vs 4–8% (base 6%) here; sale costs 6% incl. escrow/title vs 5% plus blank fees here; market rent anchored to the HUD program floor ($4,600–$5,800/mo, flagged as conservative) there vs listing comparables ($5,150–$8,400/mo) here — per the evidence rule, FMR is a program floor, not market evidence. Statutory amounts appear exactly here (the Prop 19 allowance is $1,044,586); the preserved edition rounds that figure to $1,044,590 in its data. Read both as ranges; when they disagree, the gap <em>is</em> the uncertainty. Neither is advice.</div>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">01 · EXECUTIVE SUMMARY</div><h2>What the figures say so far</h2></div><p>Read before any table. Findings are conditional on the assumptions in Section 02 and change if a flagged input is wrong.</p></div>
  <ol>
    <li><strong>The same-year sale is the baseline, and it is very hard to beat on simplicity.</strong> Selling in the tax year of the inheritance (basis = date-of-death value) leaves essentially no capital gain; at 2045 base assumptions the net proceeds are about {m(sell_net_range(fmv(V_A, A_GROWTH[1], 19), fmv(V_A, A_GROWTH[1], 19))[1])} after a 5% selling-cost band and the 0.11% county transfer tax. Every hold path must beat this number, with its risks, to be chosen.</li>
    <li><strong>Property tax is the swing cost, and Proposition 19 decides it.</strong> Without the family-home exclusion, a 2045 transfer re-assesses the home to about {m(fmv(V_A, A_GROWTH[1], 19))} and the tax bill rises roughly eight-fold — about {m(fmv(V_A, A_GROWTH[1], 19) * A_RATE[1])} per year versus about {m(prop13(AV_A0, 19) * A_RATE[1])} with the exclusion. Claim the exclusion only if the heir will genuinely occupy the home long term.</li>
    <li><strong>Letting is a floor, not a headline.</strong> Comparable asking rents of {m(RENT_MO[0])}–{m(RENT_MO[2])} per month for similar houses give an evidence band; net rent after the actual tax bill, insurance and reserves is materially lower. The rent path ranks on net figures in Section 05.</li>
    <li><strong>Staged investing is crash insurance with a visible premium.</strong> The historical replay shows phasing into 1929-type entries is worth up to +107.9 points at ten years, but the median ten-year window costs −74.9 points versus immediate investing; it wins in 15.7% of windows. Reinvestment risk sits next to every staging headline.</li>
    <li><strong>Estate tax is a real, separate question.</strong> A 2026 death has a $15,000,000 federal basic exclusion (then 40% above it); California has no estate return under current law. A "considerable" cash inheritance inside a larger estate can still push the estate over the line — the liquidity worksheet in Section 08 must be completed now, and portability/prior taxable gifts asked about now.</li>
    <li><strong>Nothing here is decided.</strong> The pre-commitment criteria (Section 12) are meant to be signed before figures arrive. The model is re-run every year; the decision log (Section 13) records what changed and when.</li>
  </ol>
  <p class="source-note">Anchors: {a(S['irs_excl'], 'IRS')} · {a(S['boe19'], 'BOE Prop 19')} · {a(S['ftb_cg'], 'FTB capital gains')} · {a(S['crash'], 'crash replay')} · {a(S['law'], 'law watch')}. Sources re-checked {BUILD_DATE}.</p>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">02 · PROPERTY FACTS (ROUNDED)</div><h2>Property A and Property B — the record as published here</h2></div><p>Household history rounded to $10 and anonymised. The unrounded values never appear anywhere in this repository.</p></div>
  <div class="table-wrap"><table><thead><tr><th>Fact</th><th>Property A (inherited home)</th><th>Property B (already owned)</th><th>Status</th></tr></thead><tbody>
  <tr><td>Role in the decision</td><td>Expected to transfer by trust in the 2040–2050 window</td><td>Already owned by the prospective heir; 3 livable units, 2 rented</td><td><span class="status unverified">H</span> {a(S['questions'], 'questions')}</td></tr>
  <tr><td>Estimated market value (Nov 2026)</td><td>{m(V_A)}</td><td>{m(V_B)}</td><td><span class="status unverified">H household estimate</span> {a(S['scc_asr'], 'assessor')}</td></tr>
  <tr><td>Factored base-year value (assessed)</td><td>{m(AV_A0)} (2026)</td><td>{m(AV_B0)} (2025; 2026 ≈ +2%)</td><td><span class="status unverified">H rounded</span> {a(S['boe_pub29'], 'Pub 29')}</td></tr>
  <tr><td>Effective tax rate on assessed value</td><td>{pct(a_mean3,2)} (3-yr mean) / {pct(a_mean_all,2)} (12-yr mean)</td><td>{pct(b_mean3,2)} (3-yr mean) / {pct(b_mean_all,2)} (10-yr mean)</td><td><span class="status unknown">C computed</span> {a(S['scc_rate'], 'county rate book')}</td></tr>
  <tr><td>Tax rate area (TRA)</td><td>Confirmed for the parcel only; county rate book structure read (1% cap + voter debt). Exact TRA row: <span class="flag">unverified — beyond automated read; confirm from the tax bill TRA line</span></td><td>Same method; bill may include city/county parcel taxes (see anomaly below)</td><td>{a(S['scc_rate_pdf'], 'FY2025-26 rate book (PDF)')}</td></tr>
  <tr><td>Solar / electricity</td><td>Solar installed: net credit ≈ {m(abs(A_SOLAR_MO[2]))} – {m(abs(A_SOLAR_MO[0]))} / month</td><td>Electricity {m(B_ELEC_MO[0])} – {m(B_ELEC_MO[2])} / month</td><td><span class="status unverified">H</span> {a(S['doi'], 'utility records')}</td></tr>
  <tr><td>Rental income</td><td>— (not currently let)</td><td>{m(B_RENT_MO)}/mo from 2 units (1 unit free; owner may live there without losing rental income)</td><td><span class="status unverified">H</span> {a(S['sf_rent'], 'SF Rent Board')}</td></tr>
  <tr><td>Proposition H (Nov 2026, SF parcel tax)</td><td>Not applicable (Property A is outside the city)</td><td>Multifamily tier ≈ {m(PROP_H_B)}/yr for buildings up to 5,000 sq ft from FY2027-28; senior relief possible</td><td><span class="status verified">V</span> {a(S['sfmta_h'], 'SFMTA Prop H')}</td></tr>
  </tbody></table></div>

  <h3>Property A — tax and assessment history (rounded to $10)</h3>
  <div class="table-wrap"><table><thead><tr><th>Year</th><th>Property tax</th><th>Tax assessment</th><th>Effective rate</th><th>Source</th></tr></thead><tbody>
  {history_rows(A_HISTORY, 'A')}
  </tbody></table></div>
  <h3>Property B — tax and assessment history (rounded to $10)</h3>
  <div class="table-wrap"><table><thead><tr><th>Year</th><th>Property tax</th><th>Tax assessment</th><th>Effective rate</th><th>Source</th></tr></thead><tbody>
  {history_rows(B_HISTORY, 'B')}
  </tbody></table></div>
  <div class="callout"><strong>Irregularity flagged for review:</strong> Property B's effective rate ({pct(b_mean_all,2)} mean) is far above a 1% base levy plus ordinary voter debt. The most likely explanation is parcel taxes and special assessments inside the bill (the city levies several), but this is not confirmed. Reconcile the actual bill line-by-line before any projection treats the rate as stable. Property A's rate drift ({pct(max(a_rates),2)} in 2016 → {pct(a_rates[0],2)} in 2025) is consistent with debt ratios rolling off — also verify against the TRA rate book. {a(S['flagged'], 'Flagged for Review')}</div>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">03 · SAME-TAX-YEAR SALE</div><h2 id="same-year">Model the sale in the inheritance year first — before anything else</h2></div><p>Basis is generally the date-of-death fair market value, so a sale in the same tax year usually leaves ≈ $0 taxable gain. This is the number every hold path must beat.</p></div>
  <div class="table-wrap"><table><thead><tr><th>Transfer / sale year</th><th>FMV at transfer (base)</th><th>Commission 5% (4–6% band)</th><th>County DTT 0.11%</th><th>Recording / title / escrow</th><th>Gain tax (≈ $0)</th><th>Net proceeds (base)</th><th>Range (low – high)</th><th>Source</th></tr></thead><tbody>
  {''.join(sy_rows)}
  </tbody></table></div>
  <ul>
    <li>City-level documentary transfer tax for Property A's city: <span class="flag">unverified — a city may add up to half the county rate (RTC 11911); confirm before pricing the path</span>.</li>
    <li>Recording, title and escrow fees: <span class="flag">left blank — no official figure confirmed; obtain a title/escrow quote</span>.</li>
    <li>California taxes capital gains as ordinary income; the additional 1% tax above $1,000,000 of taxable income (RTC 17043, 2025 Form 540 line 62) can apply in the sale year. {a(S['ftb540'], 'FTB 2025 booklet')} · {a(S['rtc17043'], 'RTC 17043')}</li>
    <li>If the sale slips to a later year, the gain from date-of-death to sale becomes taxable and the §121 exclusion may help only after genuine occupancy. {a(S['irs_523'], 'Pub 523')} · {a(S['irs_tc701'], 'Topic 701')}</li>
  </ul>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">04 · OPERATING COSTS</div><h2>What it costs to hold each property, on ranges</h2></div><p>Household estimates are marked UNVERIFIED; assumption bands are modelling inputs. Replace each with a quote, bill or inspection before relying on the ranking.</p></div>
  <div class="table-wrap"><table><thead><tr><th>Cost item</th><th>Property A (annual)</th><th>Property B (annual)</th><th>Basis</th><th>Status</th></tr></thead><tbody>
  <tr><td>Water</td><td>{m(A_WATER_MO[0]*12)} – {m(A_WATER_MO[2]*12)}</td><td>{m(B_WATER_MO[0]*12)} – {m(B_WATER_MO[2]*12)} (3 units)</td><td>Household range $100–$150 / $330–$400 per month</td><td><span class="status unverified">H</span> {a(S['doi'], 'bills')}</td></tr>
  <tr><td>Electricity / solar</td><td>net credit {m(abs(A_SOLAR_MO[0])*12)} – {m(abs(A_SOLAR_MO[2])*12)} (solar)</td><td>{m(B_ELEC_MO[0]*12)} – {m(B_ELEC_MO[2]*12)}</td><td>Household: solar usually generates a small monthly credit</td><td><span class="status unverified">H</span> {a(S['doi'], 'bills')}</td></tr>
  <tr><td>Insurance (HO-3 / landlord)</td><td>{m(A_INS_YR[0])} – {m(A_INS_YR[2])} (household estimate {m(A_INS_YR[1])})</td><td>{m(B_INS_YR[0])} – {m(B_INS_YR[2])} (landlord cover, likely higher)</td><td>Commercial quote data for the county: ≈ {m(1010)}–{m(1260)} typical home; high-value dwellings cost more</td><td><span class="status unverified">UNVERIFIED — written quotes required</span> {a(S['doi'], 'CA DOI')}</td></tr>
  <tr><td>Routine maintenance</td><td>{pct(A_MAINT_PCT[0]*100,2)} – {pct(A_MAINT_PCT[2]*100,2)} of value</td><td>{pct(B_MAINT_PCT[0]*100,2)} – {pct(B_MAINT_PCT[2]*100,2)} of value (older, 3 units)</td><td>Planning heuristics; household direction: A costs less than B</td><td><span class="status unknown">A assumption</span> {a(S['questions'], 'inspections')}</td></tr>
  <tr><td>Capital reserve</td><td>{pct(A_RESERVE_PCT[0]*100,2)} – {pct(A_RESERVE_PCT[2]*100,2)} of value</td><td>{pct(B_RESERVE_PCT[0]*100,2)} – {pct(B_RESERVE_PCT[2]*100,2)} of value</td><td>Roof, systems, seismic, solar; see five-year plan</td><td><span class="status unknown">A assumption</span> <a href="#capital">capital plan</a></td></tr>
  <tr><td>Property tax (current run-rate)</td><td>≈ {m(AV_A0*A_RATE[1])} / yr</td><td>≈ {m(AV_B0*B_RATE[1])} / yr (2026 +2%)</td><td>Effective rates computed above</td><td><span class="status unknown">C/H</span> {a(S['scc_rate'], 'rate book')}</td></tr>
  <tr><td>Prop H parcel tax (FY2027-28+)</td><td>—</td><td>{m(PROP_H_B)} / yr (multifamily tier)</td><td>Official tier schedule; area-based</td><td><span class="status verified">V</span> {a(S['sfmta_h'], 'SFMTA')}</td></tr>
  <tr><td>Vacancy / management (rent paths)</td><td>{pct(B_VAC*100,0)} of gross rent</td><td>{pct(B_VAC*100,0)} of gross rent</td><td>Assumption band 5–12%</td><td><span class="status unknown">A assumption</span> {a(S['comp'], 'method')}</td></tr>
  </tbody></table></div>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">05 · PROJECTIONS</div><h2 id="assumptions">Value, assessed value and tax by year — three speeds, not one</h2></div><p>Market value at low/base/high growth; assessed value on the Proposition 13 path (+2%/yr cap, BOE Pub 29); tax at the computed effective rate. Nothing here is a forecast.</p></div>
  <div class="table-wrap"><table><thead><tr><th>Year</th><th>Property A value · low (2.0%)</th><th>base (3.5%)</th><th>high (5.0%)</th><th>Assessed value (+2%/yr)</th><th>Tax (base 1.33%)</th><th>Tax range</th><th>Source</th></tr></thead><tbody>
  {''.join(proj_rows)}
  </tbody></table></div>
  <div class="table-wrap"><table><thead><tr><th>Year</th><th>Property B value · low (2.0%)</th><th>base (3.0%)</th><th>high (4.5%)</th><th>Assessed value (+2%/yr)</th><th>Tax (base 2.05% — flagged)</th><th>Source</th></tr></thead><tbody>
  {''.join(b_proj_rows)}
  </tbody></table></div>
  <h3>What happens to the bill at the transfer (base year {T})</h3>
  <div class="table-wrap"><table><thead><tr><th>Scenario at transfer</th><th>Market value at {T}</th><th>New assessed value</th><th>Annual tax</th><th>Change vs. continued factored base</th><th>Source</th></tr></thead><tbody>
  {''.join(rows19)}
  </tbody></table></div>
  <p class="source-note">Growth assumptions are ranges grounded in public evidence — FHFA California all-transactions index annualized about +6.1% (2015–25), +6.9% (2020–25) and +0.8% (2024–25) per FHFA data — deliberately set below recent history for the base case. {a(S['fhfa'], 'FHFA HPI')} (figures read via a public mirror — re-verify at FHFA). Inflation base 2.0% follows the Fed's long-run projection; equity ranges 4–8% are scenario inputs, well below the historical total-return record in {a(S['damodaran'], 'Damodaran')}. Prop 13's 2% cap is law. {a(S['boe_pub29'], 'BOE Pub 29')}</p>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">06 · PROPOSITION 19</div><h2 id="prop19">The exclusion, the allowance, and the honest conditions</h2></div><p>Claim the parent-child exclusion only if the heir will occupy the home long term. Everything else is a fraud risk and an assessment risk.</p></div>
  <ul>
    <li><strong>Eligibility:</strong> qualifying family transfer (parent-child / limited grandparent-grandchild), the transferor's home was their principal residence, and the transferee occupies it as their principal residence. {a(S['boe19'], 'BOE Prop 19')} · {a(S['rtc632'], 'RTC 63.2')}</li>
    <li><strong>Deadlines:</strong> homeowners' exemption filed within one year of transfer; exclusion claim within three years or before a third-party transfer, whichever is earlier. {a(S['boe19'], 'BOE guidance')}</li>
    <li><strong>Value cap:</strong> the transferee keeps the factored base-year value only up to that value plus the adjusted $1,000,000 allowance. Current allowance: <strong>{m(PROP19_ALLOW_2025)}</strong> for transfers 16 Feb 2025 – 15 Feb 2027 (prior window {m(PROP19_PRIOR)}). {a(S['boe_lta'], 'BOE LTA 2025/009')}</li>
    <li><strong>Allowance carried forward (placeholder):</strong> adjustments happen every second February 16 against the FHFA California house price index. The observed step between the last two published windows is +{pct(PROP19_STEP*100,2)}. At that step, the allowance would be ≈ {m(prop19_allowance(2040))} (2040) and ≈ {m(prop19_allowance(2045))} (2045) — <span class="flag">placeholder only; future adjustments are unknown and no future allowance is law</span>.</li>
  </ul>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">07 · PATH COMPARISON</div><h2>Every path, same transfer date, same horizons, with the risks attached</h2></div><p>Terminal household position (Property A outcome; Property B is held identically in every path except the noted free-unit effect). Base case: transfer {T}, growth 3.5%, returns 6%, inflation 2%. Ranges in Section 05. Rounded to $10.</p></div>
  <div class="table-wrap"><table><thead><tr><th>#</th><th>Path</th><th>Terminal at 20 yr (A, base)</th><th>Total incl. Property B</th><th>20-yr range (low – high)</th><th>5 yr</th><th>10 yr</th><th>30 yr</th><th>Main risk</th><th>Source</th></tr></thead><tbody>
  {''.join(rank_rows)}
  </tbody></table></div>
  <p class="source-note">Property B contributes about {m(b_value20)} of value plus about {m(b_net20)} of accumulated net rent at 20 years (base) in every path; living in Property A also unlocks the free-unit rental opportunity (≈ {m(B_FREE_UNIT_MO[1])}/mo placeholder — unverified, not included in the terminals above). Debt is assumed none — <span class="flag">unverified</span>. Taxes on investment returns reduce stock paths by an unstated drag; the browser calculator lets you set it. Ranking is indicative: it moves when flagged inputs move.</p>
  <h3>Transfer-date sensitivity (20-year terminals, base)</h3>
  <div class="table-wrap"><table><thead><tr><th>Transfer year</th><th>Same-year sale</th><th>Live in it</th><th>Rent it out</th><th>Phase 24+36 mo</th><th>Leading path</th><th>Source</th></tr></thead><tbody>
  {''.join(sens_rows)}
  </tbody></table></div>
  <div class="callout"><strong>Reinvestment risk beside the headline.</strong> The staged-sell row deliberately parks proceeds in 3-month–2-year Treasuries for 24–36 months before buying equities. Its terminal value above assumes the November 2026 bill yield (≈ {pct(BILL*100,1)}) holds while parked — it will not. Each maturity resets at unknown rates (reinvestment risk), and every month parked is foregone equity exposure (cash drag). The {a(S['crash'], 'crash replay')} prices both sides on real history; the {a(S['comp'], 'comparison calculator')} lets you set your own yield.</div>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">08 · ESTATE TAX &amp; LIQUIDITY</div><h2>The separate estate-level question — and a worksheet</h2></div><p>Estate tax, income-tax basis and property-tax assessment are three different systems. This section is the first.</p></div>
  <div class="table-wrap"><table><thead><tr><th>Year of death</th><th>Federal basic exclusion</th><th>Status</th><th>Source</th></tr></thead><tbody>
  {''.join(ex_rows)}
  </tbody></table></div>
  <div class="table-wrap"><table><thead><tr><th>Gross estate (illustrative)</th><th>2026 exclusion</th><th>Tentative federal estate tax at 40%</th><th>Remainder</th><th>Assumptions</th><th>Source</th></tr></thead><tbody>
  {''.join(est_rows)}
  </tbody></table></div>
  <h3>Liquidity worksheet (fill privately)</h3>
  <div class="table-wrap"><table><thead><tr><th>Line</th><th>Why it matters</th><th>Value</th><th>Source</th></tr></thead><tbody>
  <tr><td>Worldwide gross estate (estimate)</td><td>Form 706 threshold and tax base</td><td>______</td><td>{a(S['irs_706'], 'Form 706 instructions')}</td></tr>
  <tr><td>Adjusted taxable gifts since 1977</td><td>Added back to the estate calculation</td><td>______</td><td>{a(S['irs_excl'], 'IRS estate &amp; gift')}</td></tr>
  <tr><td>Annual gifts within the exclusion</td><td>{m(GIFT_ANNUAL)} per donee (2025 &amp; 2026)</td><td>______</td><td>{a(S['irs_excl'], 'IRS table')}</td></tr>
  <tr><td>Prior spousal exclusion available (portability)</td><td>DSUE must be elected on a timely filed return</td><td>______</td><td>{a(S['irs_706'], 'Form 706')}</td></tr>
  <tr><td>Liquid assets inside the estate</td><td>9 months to cash, or penalties/interest</td><td>______</td><td>{a(S['irs_estate'], 'IRS estate tax')}</td></tr>
  <tr><td>Illiquid real property share</td><td>Forced-sale risk; §6166 deferral only for certain closely held business interests</td><td>______</td><td>{a(S['irs_estate'], 'IRS')}</td></tr>
  <tr><td>Life insurance / credit facility already in place</td><td>Standard liquidity cover</td><td>______</td><td>{a(S['investor'], 'Investor.gov')}</td></tr>
  </tbody></table></div>
  <p class="source-note">Ask the executor/CPA <strong>now</strong> about portability and prior taxable gifts — the clock starts at death. California currently has no estate tax return for deaths on or after 1 Jan 2005. {a(S['sco'], 'State Controller')}</p>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">09 · MARKET RENT EVIDENCE</div><h2 id="rent">Comparables for Property A — evidence, not a voucher benchmark</h2></div><p>Listing snapshots in Property A's market area, Nov 2026. Asking rents, not signed leases; addresses withheld for privacy.</p></div>
  <div class="table-wrap"><table><thead><tr><th>Layout</th><th>Size</th><th>Asking rent</th><th>Type</th><th>Source</th></tr></thead><tbody>
  {''.join(comp_html)}
  </tbody></table></div>
  <p class="source-note">Band used in the model: {m(RENT_MO[0])} (low) – {m(RENT_MO[1])} (base) – {m(RENT_MO[2])} (high) per month. HUD's published Fair Market Rent is a program benchmark only and is treated as a floor, not as market evidence. {a(S['hud_fmr'], 'HUD FMR')} Letting paths in Section 07 are therefore a floor ranking until a licensed rent appraisal confirms the band. <span class="flag">Comps are commercial listing data — UNOFFICIAL; search URL withheld to keep the market area private.</span></p>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">10 · DEPRECIATION &amp; RECAPTURE</div><h2>If Property A is let: the deduction and its clawback</h2></div><p>Illustrative only. CPA rebuilds the actual schedules; the inherited basis, land split and service dates decide the real numbers.</p></div>
  <div class="table-wrap"><table><thead><tr><th>Case</th><th>Depreciable building basis (date-of-death value × share)</th><th>Annual deduction (27.5 yr GDS)</th><th>After 10 rented years</th><th>Recapture tax at sale (band)</th><th>Source</th></tr></thead><tbody>
  {''.join(dep_rows)}
  </tbody></table></div>
  <p class="source-note">Land is not depreciable; residential rental property uses the 27.5-year GDS recovery period and depreciation reduces basis on sale. {a(S['irs_527'], 'Pub 527')} · {a(S['irs_544'], 'Pub 544')} Depreciation recapture on the unrecaptured §1250 portion is taxed federally at up to 25%; California taxes all gain as ordinary income. {a(S['irs_tc409'], 'Topic 409')} · {a(S['ftb_cg'], 'FTB')} NIIT of 3.8% may also apply. {a(S['irs_tc559'], 'Topic 559')}</p>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">11 · FIVE-YEAR CAPITAL PLAN</div><h2 id="capital">Maintenance and capital plan, both buildings</h2></div><p>Planning bands until inspections and bids arrive. Property B (3 units, older) carries the heavier schedule.</p></div>
  <div class="table-wrap"><table><thead><tr><th>Item</th><th>Range</th><th>Planning figure</th><th>Timing (Property A)</th><th>Property B note</th><th>Source</th></tr></thead><tbody>
  {''.join(cap_rows)}
  </tbody></table></div>
  <p class="source-note">Totals reserved by the model: Property A ≈ {m(V_A*(A_MAINT_PCT[1]+A_RESERVE_PCT[1]))}/yr, Property B ≈ {m(V_B*(B_MAINT_PCT[1]+B_RESERVE_PCT[1]))}/yr. Replace with inspection-backed bids; carry at least one year of capital reserve in cash on any rental path. <span class="flag">Bands are assumptions, not quotes.</span> {a(S['flagged'], 'Flagged items')}</p>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">12 · PRE-COMMITMENT</div><h2>What would make the household choose each path — agreed before the figures arrive</h2></div><p>Sign this before appraisals and projections, so the answer is not reverse-engineered from one model run.</p></div>
  <div class="table-wrap"><table><thead><tr><th>Path</th><th>Choose it if (and only if)</th><th>Household decision</th><th>Source</th></tr></thead><tbody>
  {''.join(pre_rows)}
  </tbody></table></div>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">13 · DECISION LOG</div><h2 id="decision-log">What was decided, when, and why — and what is still open</h2></div><p>Every entry carries its date so a future reader knows what was chosen and why.</p></div>
  <div class="table-wrap"><table><thead><tr><th>Decision</th><th>Date</th><th>Who / why</th><th>Revisit condition</th><th>Source</th></tr></thead><tbody>
  {''.join(dec_html)}
  </tbody></table></div>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">14 · REGIMES</div><h2 id="regimes">Growth and inflation never repeat — decade evidence</h2></div><p>Real U.S. market data by decade: the long-run average case does not exist in any actual decade. This is why the projections use ranges.</p></div>
  <div class="table-wrap"><table><thead><tr><th>Decade</th><th>Years</th><th>S&amp;P 500 avg (nominal)</th><th>3-mo T-bill avg</th><th>CPI avg</th><th>Real equity avg</th><th>Source</th></tr></thead><tbody>
  {''.join(regime_rows)}
  </tbody></table></div>
  <h3>Three irregular 50-year sequences (computed from the decades above)</h3>
  <div class="table-wrap"><table><thead><tr><th>Sequence</th><th>Decade order</th><th>Real growth of $1 in equities</th><th>Reading</th><th>Source</th></tr></thead><tbody>
  {''.join(seq_rows)}
  </tbody></table></div>
  <h3 id="distribution">Distribution of outcomes — not one average</h3>
  {svg}
  <p class="source-note">Bands = low/high assumption sets; red marker = base case. For the full historical window-by-window distribution of staged versus immediate entry (88 ten-year windows, 1928–2025), see the {a(S['crash'], 'crash replay')}: median real 10-year multiple ≈ 2.00× (immediate) versus ≈ 1.42× (24-month park + 36-month phase), with the staged path winning 15.7% of windows — concentrated in crash-year entries.</p>
  </section>

  <section class="content-section"><div class="section-heading"><div><div class="eyebrow">15 · SELL-PATH TRANSACTION COSTS</div><h2>Transfer tax and recording fees, priced into every sell path</h2></div><p>The model above already subtracts the verified items; blanks stay blank until confirmed.</p></div>
  <div class="table-wrap"><table><thead><tr><th>Cost</th><th>Property A sale</th><th>Property B sale (if ever)</th><th>Status</th></tr></thead><tbody>
  <tr><td>County documentary transfer tax</td><td>0.11% of price ($0.55 per $500)</td><td>0.11% of price</td><td><span class="status verified">V</span> {a(S['rtc11911'], 'RTC 11911')}</td></tr>
  <tr><td>City transfer tax</td><td>blank — confirm (up to half the county rate possible)</td><td>tiered city rate (e.g. $3.75 per $500 at $1M–$5M, whole consideration)</td><td><span class="status unverified">A city part unverified</span> {a(S['sf_transfer'], 'SF transfer tax')}</td></tr>
  <tr><td>Broker commission</td><td>4–6% band ({m(V_A*COMMISSION[0])} – {m(V_A*COMMISSION[2])} at today's value)</td><td>same band</td><td><span class="status unknown">A market convention</span> {a(S['investor'], 'negotiate')}</td></tr>
  <tr><td>Title, escrow, recording</td><td>blank — obtain quote</td><td>blank — obtain quote; check sewer-lateral and transfer requirements</td><td><span class="status unverified">unverified</span> {a(S['scc_asr'], 'county recorder')}</td></tr>
  <tr><td>Income tax on gain</td><td>≈ $0 in the same tax year; else gain band 20–37% + possible 1% over $1M</td><td>depreciation recapture if let</td><td><span class="status verified">V law</span> {a(S['ftb_cg'], 'FTB')} · {a(S['irs_tc409'], 'IRS')}</td></tr>
  </tbody></table></div>
  </section>

  <footer><p>Estate Pathways · figures rebuilt {BUILD_DATE} by scripts/build_figures.py · rounded to $10 · placeholders only · not legal, tax, insurance, appraisal or investment advice.</p>
  <p>Rebuild after any input change: <code>python3 scripts/build_figures.py</code>, then re-run <code>python3 scripts/check_site.py</code> and record whether the ranking moved in the decision log.</p>
  <p><a href="index.html">Dashboard</a> · <a href="flagged.html">Flagged for review</a> · <a href="questions.html">Questions &amp; missing data</a></p></footer>
</main>
</div>
</body>
</html>""")

    return "".join(out)


def build_blackswan_block() -> str:
    with open(DATA, encoding="utf-8") as fh:
        raw = json.load(fh)
    years = {int(k): v for k, v in raw["years"].items()}
    dec = {}
    for y, v in years.items():
        infl = None
        if (y - 1) in years:
            infl = (v["cpi_index"] / years[y - 1]["cpi_index"] - 1.0) * 100.0
        d = (y // 10) * 10
        dec.setdefault(d, []).append((v, infl))
    rows = []
    for d in sorted(dec):
        if d < 1930:
            continue
        vals = dec[d]
        sp = sum(v["sp500_tr_pct"] for v, _ in vals) / len(vals)
        tb = sum(v["tbill_pct"] for v, _ in vals) / len(vals)
        infls = [i for _, i in vals if i is not None]
        cpi = sum(infls) / len(infls) if infls else 0.0
        real = ((1 + sp / 100) / (1 + cpi / 100) - 1) * 100
        rows.append(
            f"<tr><td><strong>{d}s</strong></td><td>{len(vals)}</td><td>{sp:.1f}%</td>"
            f"<td>{tb:.1f}%</td><td>{cpi:.1f}%</td><td>{real:.1f}%</td>"
            f"<td><a href=\"https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html\">Damodaran</a> "
            f"· <a href=\"https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-\">CPI</a></td></tr>")
    return (
        "<h2 id=\"regimes\">Real growth and inflation by decade — the average case never arrives</h2>\n"
        "<p class=\"review-intro\">Computed from the same public annual dataset used by the crash replay: equity and bill returns (Damodaran) and CPI-U (Minneapolis Fed / BLS). A 50-year plan built on one average growth rate and one average inflation rate describes no decade that actually happened — which is why the projections on the <a href=\"figures.html#assumptions\">figures page</a> run on ranges, and why the black-swan tests replay real, irregular sequences.</p>\n"
        "<div class=\"table-wrap\"><table><thead><tr><th>Decade</th><th>Years</th><th>S&amp;P 500 avg (nominal)</th><th>3-mo T-bill avg</th><th>CPI avg</th><th>Real equity avg</th><th>Source</th></tr></thead><tbody>\n"
        + "\n".join(rows)
        + "</tbody></table></div>\n"
        "<p class=\"source-note\">Decade averages are simple means of annual values; real equity = ((1+nominal)/(1+CPI)−1). Sequences and staged-entry results: <a href=\"crash-replay.html\">crash replay</a> · rounded household projections: <a href=\"figures.html\">planning figures</a>.</p>\n"
    )


def main() -> None:
    html = build()
    dest = os.path.join(ROOT, "figures.html")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"wrote {dest} ({len(html)} bytes)")

    print("figures.html regenerated (black-swan.html is owned by the root dashboard build)")


if __name__ == "__main__":
    main()
