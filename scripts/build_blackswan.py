#!/usr/bin/env python3
"""
Crash-entry (sequence-of-returns) replay for a phased-investing decision.

Public-market data only. No household figures, no personal information.

What it does
------------
Given a transfer date, compare:
  * LUMP  - invest the whole after-tax sale proceeds immediately.
  * PHASED- park everything in short U.S. Treasury bills for a chosen parking
            window (24 or 36 months), then buy equities in equal monthly
            tranches over a chosen phase-in window (24 or 36 months).

Every variant is measured on the SAME start date, the SAME end date, the same
starting amount, and both nominal and inflation-adjusted (real) terms.

Method and its limits (also printed on the site)
------------------------------------------------
* Annual returns are converted to monthly equivalents geometrically:
  (1 + r_annual) ** (1/12) - 1. This is a smoothing assumption, not observed
  monthly data. It therefore cannot reproduce an intra-year crash (for example
  the autumn 2008 collapse) and will understate the benefit of phasing into a
  crash that happens after the start month.
* No taxes, fees, advisory costs, dividends timing, or rebalancing are modelled.
  Both variants hold the same asset mix once fully invested.
* Inflation uses the annual CPI-U average, interpolated monthly.
* Real values divide nominal values by the CPI ratio over the same window.

Sources are in data/historical-returns.json and are re-checked by
scripts/verify_sources.py.
"""
from __future__ import annotations

import json
import math
import os
from statistics import median

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "historical-returns.json")
OUT = os.path.join(ROOT, "data", "black-swan-results.json")

# Phase-in specifications tested. Values are (park months, phase-in months).
VARIANTS = {
    "park24_phase36": (24, 36),
    "park36_phase36": (36, 36),
    "park12_phase24": (12, 24),
}


def load():
    with open(DATA, encoding="utf-8") as fh:
        raw = json.load(fh)
    years = {int(k): v for k, v in raw["years"].items()}
    return raw, years


def monthly_factors(annual_pct: float):
    """Return (equity_factor, bill_factor) for each of 12 months of a year."""
    eq = (1.0 + annual_pct / 100.0) ** (1.0 / 12.0)
    return eq


def simulate(years: dict, start: int, horizon_years: int, park: int, phase: int,
             bill_mode: str = "historical") -> dict:
    """Monthly simulation from January 1 of `start` for horizon_years*12 months.

    bill_mode:
        historical - use that year's 3-month T-bill return
        zero       - 0% on uninvested cash (pessimistic bound)
        equity     - uninvested cash earns the equity return (optimistic bound)
    """
    months = horizon_years * 12
    if start not in years:
        raise KeyError(start)

    lump = 1.0
    phased_cash = 1.0      # uninvested
    phased_invested = 0.0
    tranche = 1.0 / phase  # fraction of the whole bought each month of phase-in

    for m in range(months):
        year = start + m // 12
        if year not in years:
            raise KeyError(f"data ends before {year}")
        row = years[year]
        eq_f = (1.0 + row["sp500_tr_pct"] / 100.0) ** (1.0 / 12.0)
        if bill_mode == "zero":
            bill_f = 1.0
        elif bill_mode == "equity":
            bill_f = eq_f
        else:
            bill_f = (1.0 + row["tbill_pct"] / 100.0) ** (1.0 / 12.0)

        lump *= eq_f
        if m < park:
            phased_cash *= bill_f
        elif m < park + phase:
            phased_invested *= eq_f
            buy = phased_cash * tranche
            phased_cash -= buy
            phased_invested += buy
        else:
            phased_invested *= eq_f
            phased_cash *= bill_f
        # months inside the phase-in window that are already invested earn equity
        if park <= m < park + phase:
            pass

    phased = phased_invested + phased_cash

    start_cpi = years[start]["cpi_index"]
    end_year = start + horizon_years - 1
    end_cpi = years[end_year]["cpi_index"]
    cpi_ratio = end_cpi / start_cpi

    return {
        "lump_nominal": lump,
        "phased_nominal": phased,
        "cpi_ratio": cpi_ratio,
        "lump_real": lump / cpi_ratio,
        "phased_real": phased / cpi_ratio,
        "equity_cagr_pct": (lump ** (1.0 / horizon_years) - 1.0) * 100.0,
    }


def r(x: float, nd: int = 4):
    return round(x, nd)


def cohort_stats(years: dict, horizon: int, park: int, phase: int, bill_mode="historical"):
    first, last = min(years), max(years)
    rows = []
    for start in range(first, last - horizon + 2):
        s = simulate(years, start, horizon, park, phase, bill_mode)
        rows.append((start, s))
    diffs = [s["phased_nominal"] - s["lump_nominal"] for _, s in rows]
    diffs_real = [s["phased_real"] - s["lump_real"] for _, s in rows]
    wins = sum(1 for d in diffs if d > 0)
    worst = min(rows, key=lambda t: t[1]["phased_real"] - t[1]["lump_real"])
    best = max(rows, key=lambda t: t[1]["phased_real"] - t[1]["lump_real"])
    lump_negative = sum(1 for _, s in rows if s["lump_real"] < 1.0)
    return {
        "horizon_years": horizon,
        "cohorts": len(rows),
        "start_range": [rows[0][0], rows[-1][0]],
        "phased_wins": wins,
        "phased_win_pct": r(100.0 * wins / len(rows), 1),
        "median_diff_pct_of_start": r(100.0 * median(diffs) / 1.0, 2),
        "median_real_diff_pct": r(100.0 * median(diffs_real), 2),
        "worst_cohort": {
            "start_year": worst[0],
            "phased_minus_lump_real_pct": r(100.0 * (worst[1]["phased_real"] - worst[1]["lump_real"]), 2),
        },
        "best_cohort": {
            "start_year": best[0],
            "phased_minus_lump_real_pct": r(100.0 * (best[1]["phased_real"] - best[1]["lump_real"]), 2),
        },
        "lump_negative_real_cohorts": lump_negative,
        "history": [
            {
                "start_year": start,
                "lump_real_x": r(s["lump_real"], 3),
                "phased_real_x": r(s["phased_real"], 3),
                "equity_cagr_pct": r(s["equity_cagr_pct"], 2),
            }
            for start, s in rows
        ],
    }


EPISODES = [
    {"start": 1929, "name": "1929 - pre-crash peak", "why": "Entry at the top of the 1929 bubble."},
    {"start": 1937, "name": "1937 - second leg of the Depression", "why": "Entry just before a second severe decline."},
    {"start": 1973, "name": "1973 - stagflation onset", "why": "Falling real returns with high inflation."},
    {"start": 2000, "name": "2000 - dot-com peak", "why": "Three consecutive negative years."},
    {"start": 2007, "name": "2007 - pre-crisis", "why": "Entry one year before the financial crisis."},
    {"start": 2008, "name": "2008 - crisis year", "why": "Entry during the crash itself."},
    {"start": 2020, "name": "2020 - pandemic crash", "why": "Fast crash and fast recovery."},
    {"start": 2022, "name": "2022 - rate shock", "why": "Equities and bonds fell together."},
    {"start": 1995, "name": "1995 - strong bull entry (control)", "why": "A good entry year, for contrast."},
]


def episode_table(years: dict, park: int, phase: int):
    out = []
    for ep in EPISODES:
        row = {"start": ep["start"], "name": ep["name"], "why": ep["why"], "horizons": []}
        for horizon in (1, 3, 5, 10):
            if ep["start"] + horizon - 1 > max(years):
                continue
            s = simulate(years, ep["start"], horizon, park, phase)
            row["horizons"].append({
                "years": horizon,
                "lump_real_x": r(s["lump_real"], 3),
                "phased_real_x": r(s["phased_real"], 3),
                "phased_minus_lump_real_pts": r(100.0 * (s["phased_real"] - s["lump_real"]), 2),
                "phased_won": s["phased_real"] > s["lump_real"],
                "cpi_change_pct": r(100.0 * (s["cpi_ratio"] - 1.0), 1),
            })
        out.append(row)
    return out


def main():
    raw, years = load()
    result = {
        "generated_by": "scripts/build_blackswan.py",
        "data_as_of": "2026-11-25",
        "data_sources": [{"publisher": s["publisher"], "url": s["url"], "edition": s["edition"]} for s in raw["sources"]],
        "method_notes": [
            "Annual S&P 500 total returns (dividends included) and 3-month Treasury bill returns, converted to monthly equivalents geometrically.",
            "Inflation is the annual CPI-U average in the same dataset, interpolated the same way.",
            "No taxes, fees, advisory costs, or asset allocation changes are modelled; both variants hold the same assets once fully invested.",
            "Monthly smoothing cannot reproduce an intra-year crash, so the phased benefit in a late-in-year collapse is understated.",
            "Starting amount is normalised to 1.0; results are multiples of the starting amount, net of nothing.",
        ],
        "variants": {},
        "episodes": {},
        "bill_mode_sensitivity": {},
    }

    for key, (park, phase) in VARIANTS.items():
        result["variants"][key] = {
            "park_months": park,
            "phase_months": phase,
            "fully_invested_after_months": park + phase,
            "cohort_stats": [cohort_stats(years, h, park, phase) for h in (1, 3, 5, 10, 20)],
        }
        result["episodes"][key] = episode_table(years, park, phase)
        result["bill_mode_sensitivity"][key] = [
            {"bill_mode": mode,
             "ten_year": cohort_stats(years, 10, park, phase, mode)}
            for mode in ("zero", "historical", "equity")
        ]

    # Distribution of 10-year real multiples for a 10-year horizon (base variant)
    park, phase = VARIANTS["park24_phase36"]
    dist = []
    for start in range(min(years), max(years) - 9):
        s = simulate(years, start, 10, park, phase)
        dist.append((start, s["lump_real"], s["phased_real"]))
    result["ten_year_distribution"] = {
        "note": "Each point is one historical 10-year window starting in the listed year; real multiples of the starting amount.",
        "points": [
            {"start_year": y, "lump_real_x": r(a, 3), "phased_real_x": r(b, 3)}
            for y, a, b in dist
        ],
        "lump_median_real_x": r(median([a for _, a, _ in dist]), 3),
        "phased_median_real_x": r(median([b for _, _, b in dist]), 3),
        "lump_p10_real_x": r(sorted(a for _, a, _ in dist)[len(dist) // 10], 3),
        "lump_p90_real_x": r(sorted(a for _, a, _ in dist)[int(len(dist) * 0.9)], 3),
        "phased_p10_real_x": r(sorted(b for _, _, b in dist)[len(dist) // 10], 3),
        "phased_p90_real_x": r(sorted(b for _, _, b in dist)[int(len(dist) * 0.9)], 3),
    }

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)
    print(f"wrote {OUT}")

    # Console summary for the build log
    for key, v in result["variants"].items():
        print(f"\n== {key} (park {v['park_months']}m, phase {v['phase_months']}m)")
        for cs in v["cohort_stats"]:
            print(f"  {cs['horizon_years']:>2}y  cohorts {cs['cohorts']:>3}  "
                  f"phased wins {cs['phased_win_pct']:>5}%  "
                  f"median real diff {cs['median_real_diff_pct']:>7}%  "
                  f"worst {cs['worst_cohort']['start_year']} "
                  f"({cs['worst_cohort']['phased_minus_lump_real_pct']}%)  "
                  f"best {cs['best_cohort']['start_year']} "
                  f"(+{cs['best_cohort']['phased_minus_lump_real_pct']}%)")


if __name__ == "__main__":
    main()
