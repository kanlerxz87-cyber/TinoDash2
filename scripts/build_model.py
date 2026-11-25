#!/usr/bin/env python3
"""Build the PRIVACY-SAFE public model (docs/data/model.json).

Policy (see COORDINATION.md, session s-95fcebfc privacy position):
  * No household values are written here: no assessed values, tax bills,
    rents, utility bills, insurance quotes, or prices for Property A or B.
  * Published numbers are official-law anchors, rates, ratios, and
    official index levels with their source URLs.
  * Historical index levels are reproduced only as ratios (percent change).
"""
from __future__ import annotations
import json, os
from datetime import datetime, timezone

OUT = os.path.join(os.path.dirname(__file__), '..', 'docs', 'data', 'model.json')

def pct_change(a, b):
    return round((b / a - 1) * 100, 1)

# Official index levels (values as published by the cited source).
CRASH = [
    {
        "id": "1929-1932-equity",
        "label": "1929–1932 US equity (NBER monthly index, via FRED)",
        "source": "https://fred.stlouisfed.org/series/M1109BUSM293NNBR",
        "peak_date": "1929-09", "peak_level": 362.35,
        "trough_date": "1932-06", "trough_level": 46.85,
        "drawdown_pct": pct_change(362.35, 46.85),
        "status": "verified-fetch",
    },
    {
        "id": "2007-2009-equity",
        "label": "2007–2009 Nasdaq Composite (daily close, via FRED)",
        "source": "https://fred.stlouisfed.org/series/NASDAQCOM",
        "peak_date": "2007-10-31", "peak_level": 2859.12,
        "trough_date": "2009-03-09", "trough_level": 1268.64,
        "drawdown_pct": pct_change(2859.12, 1268.64),
        "status": "verified-fetch",
        "note": "Nasdaq used because the S&P 500 FRED graph endpoint returned only 2016+ data in this session.",
    },
]

PRICE_LEVEL = {
    "id": "1929-1933-cpi",
    "label": "US CPI-U (all items, NSA), Sep 1929 → Jun 1932 (via FRED)",
    "source": "https://fred.stlouisfed.org/series/CPIAUCNS",
    "from_date": "1929-09", "from_level": 17.3,
    "to_date": "1932-06", "to_level": 13.6,
    "change_pct": pct_change(17.3, 13.6),
}

TBILL = [
    {"period": "2007-10 to 2008-12", "tb3ms_low_pct": 0.03, "tb3ms_high_pct": 3.90,
     "low_month": "2008-12", "high_month": "2007-09",
     "source": "https://fred.stlouisfed.org/series/TB3MS"},
    {"period": "1934-01 to 1940-12", "tb3ms_low_pct": 0.01, "tb3ms_high_pct": 0.72,
     "low_month": "1940-01", "high_month": "1934-01",
     "source": "https://fred.stlouisfed.org/series/TB3MS"},
]

MODEL = {
    "as_of": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    "privacy": "No household values published. Figures here are official anchors, rates, ratios, and index moves only.",
    "rounding_rule": "Any currency amount shown on this site is rounded to the nearest $10. This file contains no currency amounts for households.",
    "official_anchors": [
        {"item": "Federal estate & gift basic exclusion, CY2026", "value": "$15,000,000",
         "source": "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax",
         "status": "enacted"},
        {"item": "Federal estate filing threshold, year of death 2026", "value": "$15,000,000",
         "source": "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax", "status": "enacted"},
        {"item": "CA Prop 19 parent-child value allowance (2/16/2025–2/15/2027)", "value": "$1,044,586",
         "source": "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf", "status": "enacted"},
        {"item": "CA state estate/inheritance return required for deaths on/after 1/1/2005", "value": "No",
         "source": "https://www.sco.ca.gov/ardtax_estate_tax.html", "status": "enacted"},
        {"item": "CA homeowners' exemption reduction", "value": "$7,000 (taxable value)",
         "source": "https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf", "status": "enacted"},
        {"item": "CA property tax base rate (Prop 13 1% general levy)", "value": "1% plus voter-approved bonds/special taxes",
         "source": "https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf", "status": "enacted"},
        {"item": "Prop 13 annual base-year value inflation cap", "value": "2% maximum",
         "source": "https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf", "status": "enacted"},
        {"item": "Federal LTCG 0% bracket top (single, 2025)", "value": "$48,350",
         "source": "https://www.irs.gov/taxtopics/tc409", "status": "enacted"},
        {"item": "Federal NIIT rate / threshold (single, MAGI)", "value": "3.8% / $200,000",
         "source": "https://www.irs.gov/taxtopics/tc559", "status": "enacted"},
        {"item": "CA Mental Health Services surtax (line 62)", "value": "1% of taxable income over $1,000,000",
         "source": "https://www.ftb.ca.gov/forms/2025/2025-540-booklet.html", "status": "enacted"},
        {"item": "CA 2025 top marginal rate (Schedule X, single)", "value": "12.3% above $742,953 (+1% BHS)",
         "source": "https://www.ftb.ca.gov/forms/2025/2025-540-tax-rate-schedules.pdf", "status": "enacted"},
    ],
    "pending_or_proposed": [
        {"item": "SB 284 (Property taxation: change in ownership: family homes and farms)",
         "status": "Active bill — in committee process; NOT law",
         "source": "https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260SB284"},
        {"item": "SB 293 (generational transfers / base-year value; chaptered as Stats. 2025 ch. 539, eff. 1/1/2026)",
         "status": "ENACTED — the amended RTC 63.2 applies; not a proposal",
         "source": "https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260SB293"},
    ],
    "macro_baseline_refs": [
        {"item": "Fed Dec-2025 SEP median PCE inflation: 2026 / 2027 / longer run",
         "value": "2.4% / 2.1% / 2.0%", "source": "https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20251210.htm"},
        {"item": "Fed Dec-2025 SEP median real GDP growth: 2026 / longer run",
         "value": "2.3% / 1.8%", "source": "https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20251210.htm"},
        {"item": "Fed Dec-2025 SEP median fed funds, longer run", "value": "3.0%",
         "source": "https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20251210.htm"},
        {"item": "CBO (Jan 2025) real GDP growth, 2027–2035 average", "value": "~1.8% per year",
         "source": "https://www.cbo.gov/publication/61189"},
        {"item": "SSA 2025 Trustees Report — referenced for long-run benefit/tax context (values not extracted)",
         "value": "[flagged — not extracted]", "source": "https://www.ssa.gov/oact/TR/2025/trTOC.html"},
    ],
    "black_swan": {
        "description": "Official-data crash moves used as stress inputs. Not forecasts. Replays use percent moves only; no household dollar outcomes are published.",
        "equity_crashes": CRASH,
        "price_level_1929_1933": PRICE_LEVEL,
        "treasury_bill_3m_ranges": TBILL,
        "reinvestment_risk_note": "3-month bill yields fell from ~3.9% (Sep 2007) to ~0.03% (Dec 2008); a 3M–2Y ladder reprices each rollover, so a staged cash position earns whatever rate exists at each rollover date.",
    },
    "flagged": [
        "Full monthly 1929–1932 equity path not reproduced: only peak and trough values were fetched; phased-entry path results are therefore NOT published.",
        "SF transfer-tax rate schedule: official pages failed to load in this session. Not published.",
        "Santa Clara assessor Prop 13 / Prop 19 guidance pages: not reached. Not published.",
        "Treasury daily par yield curve, SF Rent Board allowable increase, HUD FMR SF, insurance and rent comparables: not verified. Not published.",
        "Git history contains pre-policy commits with household figures (PR #12 era). History rewrite NOT performed; owner decision required.",
    ],
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(MODEL, f, indent=2, ensure_ascii=False)
    f.write('\n')
print('wrote', os.path.normpath(OUT))
