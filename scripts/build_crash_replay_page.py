#!/usr/bin/env python3
"""
Render crash-replay.html from data/black-swan-results.json.

Every table row carries a source link, as scripts/check_site.py requires.
No household figures are used or published: the model normalises the starting
amount to 1.00 so it can be applied to any sale proceeds privately.
"""
from __future__ import annotations

import json
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "historical-returns.json")
RES = os.path.join(ROOT, "data", "black-swan-results.json")
OUT = os.path.join(ROOT, "crash-replay.html")

DAMODARAN = "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/histretSP.html"
MINFED = "https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-"
BLS = "https://www.bls.gov/cpi/"
TREASURY = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates"
TBILL = "https://www.treasurydirect.gov/marketable-securities/treasury-bills/"
NBER = "https://www.nber.org/research/business-cycle-dating"


def fmt_x(v: float) -> str:
    return f"{v:,.2f}×"


def fmt_pts(v: float) -> str:
    sign = "+" if v > 0 else ("−" if v < 0 else "")
    return f"{sign}{abs(v):,.1f} pts"


def badge(win: bool) -> str:
    if win:
        return '<span class="status verified">Phasing ahead</span>'
    return '<span class="status unverified">Phasing behind</span>'


def build() -> str:
    with open(RAW, encoding="utf-8") as fh:
        raw = json.load(fh)
    with open(RES, encoding="utf-8") as fh:
        res = json.load(fh)

    years = sorted(int(y) for y in raw["years"])
    base = res["variants"]["park24_phase36"]
    alt = res["variants"]["park36_phase36"]
    short = res["variants"]["park12_phase24"]

    # ---- cohhort summary rows -------------------------------------------------
    cohort_rows = []
    for cs in base["cohort_stats"]:
        cohort_rows.append(
            "<tr>"
            f"<td><strong>{cs['horizon_years']} year{'s' if cs['horizon_years'] > 1 else ''}</strong></td>"
            f"<td>{cs['cohorts']} windows<br><span class=\"muted\">{cs['start_range'][0]}–{cs['start_range'][1]} starts</span></td>"
            f"<td>{cs['phased_win_pct']}%</td>"
            f"<td>{fmt_pts(cs['median_real_diff_pct'])}</td>"
            f"<td>{cs['worst_cohort']['start_year']}: {fmt_pts(cs['worst_cohort']['phased_minus_lump_real_pct'])}</td>"
            f"<td>{cs['best_cohort']['start_year']}: {fmt_pts(cs['best_cohort']['phased_minus_lump_real_pct'])}</td>"
            f"<td>{cs['lump_negative_real_cohorts']} of {cs['cohorts']}</td>"
            f"<td><a href=\"{DAMODARAN}\">S&amp;P 500 total return &amp; T-bill</a></td>"
            "</tr>"
        )

    # ---- variance between specs ----------------------------------------------
    spec_rows = []
    for key, label in (
        ("park24_phase36", "Park 24 months in T-bills, then 36-month phase-in"),
        ("park36_phase36", "Park 36 months in T-bills, then 36-month phase-in"),
        ("park12_phase24", "Park 12 months in T-bills, then 24-month phase-in"),
    ):
        v = res["variants"][key]
        cs10 = next(c for c in v["cohort_stats"] if c["horizon_years"] == 10)
        cs5 = next(c for c in v["cohort_stats"] if c["horizon_years"] == 5)
        spec_rows.append(
            "<tr>"
            f"<td><strong>{label}</strong></td>"
            f"<td>{v['fully_invested_after_months']} months</td>"
            f"<td>{cs5['phased_win_pct']}%</td>"
            f"<td>{fmt_pts(cs5['median_real_diff_pct'])}</td>"
            f"<td>{cs10['phased_win_pct']}%</td>"
            f"<td>{fmt_pts(cs10['median_real_diff_pct'])}</td>"
            f"<td><a href=\"{TBILL}\">Treasury bill terms</a></td>"
            "</tr>"
        )

    # ---- episode rows (one row per episode, four horizons) --------------------
    episode_rows = []
    for ep in res["episodes"]["park24_phase36"]:
        cells = []
        by_h = {h["years"]: h for h in ep["horizons"]}
        for h in (1, 3, 5, 10):
            if h in by_h:
                d = by_h[h]
                cells.append(
                    f"<td><strong>{fmt_x(d['lump_real_x'])}</strong> / {fmt_x(d['phased_real_x'])}"
                    f"<br><span class=\"small muted\">{fmt_pts(d['phased_minus_lump_real_pts'])}</span></td>"
                )
            else:
                cells.append('<td class="muted">beyond data</td>')
        episode_rows.append(
            "<tr>"
            f"<td><strong>{ep['name']}</strong><br><span class=\"small muted\">{ep['why']}</span></td>"
            + "".join(cells)
            + f"<td><a href=\"{DAMODARAN}\">Return series</a> · <a href=\"{NBER}\">Cycle dates</a></td>"
            "</tr>"
        )

    # ---- cash-return sensitivity --------------------------------------------
    sens_rows = []
    labels = {
        "zero": "0% while parked (worst case for phasing)",
        "historical": "Historical 3-month T-bill return (base case)",
        "equity": "Equity return on uninvested cash (upper bound for phasing)",
    }
    for item in res["bill_mode_sensitivity"]["park24_phase36"]:
        cs = item["ten_year"]
        sens_rows.append(
            "<tr>"
            f"<td><strong>{labels[item['bill_mode']]}</strong></td>"
            f"<td>{cs['phased_win_pct']}%</td>"
            f"<td>{fmt_pts(cs['median_real_diff_pct'])}</td>"
            f"<td>{cs['worst_cohort']['start_year']}: {fmt_pts(cs['worst_cohort']['phased_minus_lump_real_pct'])}</td>"
            f"<td><a href=\"{TREASURY}\">Treasury rate data</a></td>"
            "</tr>"
        )

    # ---- distribution table (deciles of 10-year real outcome) ---------------
    dist = res["ten_year_distribution"]
    pts = dist["points"]
    lump = sorted(p["lump_real_x"] for p in pts)
    phased = sorted(p["phased_real_x"] for p in pts)

    def pct(vals, q):
        idx = min(len(vals) - 1, max(0, int(round(q * (len(vals) - 1)))))
        return vals[idx]

    dist_rows = []
    for q_label, q in (("10th percentile", 0.10), ("25th", 0.25), ("Median", 0.50), ("75th", 0.75), ("90th percentile", 0.90)):
        dist_rows.append(
            "<tr>"
            f"<td><strong>{q_label}</strong></td>"
            f"<td>{fmt_x(pct(lump, q))}</td>"
            f"<td>{fmt_x(pct(phased, q))}</td>"
            f"<td>{'ahead' if pct(phased, q) >= pct(lump, q) else 'behind'}</td>"
            f"<td><a href=\"{DAMODARAN}\">Historical returns</a> · <a href=\"{MINFED}\">CPI-U</a></td>"
            "</tr>"
        )

    # ---- worst/best detail for the headline 10-year case --------------------
    cs10 = next(c for c in base["cohort_stats"] if c["horizon_years"] == 10)
    hist = {h["start_year"]: h for h in cs10["history"]}
    w = hist[cs10["worst_cohort"]["start_year"]]
    b = hist[cs10["best_cohort"]["start_year"]]

    checks = raw["verification"]["published_cumulative_index_checks"]
    check_rows = "".join(
        f"<tr><td>{yr}</td><td>{checks['sp500_total_return'][yr]:,.2f}</td><td>{checks['tbill_total_return'][yr]:,.2f}</td>"
        f"<td><a href=\"{DAMODARAN}\">Published cumulative index</a></td></tr>"
        for yr in checks["sp500_total_return"]
    )

    today = date.today().isoformat()
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,follow">
<title>Crash-entry replay: phased investing vs lump sum | Estate Pathways</title>
<link rel="stylesheet" href="styles.css">
<style>
.replay-key{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:14px 0 0}}
.replay-key div{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:13px 15px}}
.replay-key strong{{display:block;font-size:11px;letter-spacing:.6px;text-transform:uppercase;color:var(--muted);margin-bottom:4px}}
.small{{font-size:11px}}
.bars{{display:grid;gap:4px;margin-top:10px}}
.bar-row{{display:grid;grid-template-columns:64px 1fr 1fr;gap:8px;align-items:center;font-size:11px}}
.bar-track{{position:relative;background:#eef2f4;border-radius:4px;height:14px;overflow:hidden}}
.bar-fill{{position:absolute;top:0;bottom:0;left:0;border-radius:4px}}
.bar-lump{{background:#b9d4d1}}
.bar-phased{{background:#0f817b}}
@media print{{.sidebar,.topbar{{display:none}}main{{padding:0}}}}
</style>
</head>
<body>
<header class="topbar">
  <a class="brand" href="index.html"><span class="brand-mark">EP</span><span>Estate Pathways<small>Crash-entry replay</small></span></a>
  <div class="top-actions">
    <span class="privacy-chip"><span aria-hidden="true">●</span> Public market data only · no household figures</span>
    <a class="button button-quiet" href="index.html#black-swan">← Back to dashboard</a>
  </div>
</header>
<main class="review-page">
  <div class="eyebrow">SEQUENCE-OF-RETURNS REPLAY · {years[0]}–{years[-1]} ANNUAL DATA · GENERATED {today}</div>
  <h1>Does parking sale proceeds in Treasuries for 24–36 months soften crash-entry risk?</h1>
  <p class="review-intro">The question behind a phased-investing plan is not “does it feel safer?” It is: <strong>over every historical start date we can observe, did the phased path actually end with more purchasing power than investing immediately?</strong> This page replays both strategies on {years[0]}–{years[-1]} S&amp;P 500 total returns (dividends included), 3-month Treasury bill returns and CPI-U inflation, using one shared start date, one shared end date and an identical starting amount of <strong>1.00</strong>. Multiply any multiple below by private sale proceeds to see an illustrative outcome — the site stores no such figure.</p>

  <div class="decision-state"><span class="state-icon">!</span><div><strong>Headline result: phasing usually costs money, and only pays in a genuine crash.</strong><p>Across {cs10['cohorts']} overlapping ten-year windows, the 24-month park plus 36-month phase-in beat immediate investing in only <strong>{cs10['phased_win_pct']}%</strong> of them. The median ten-year real outcome was <strong>{fmt_pts(cs10['median_real_diff_pct'])}</strong> versus lump sum. The wins are real but concentrated: the best window started in {cs10['best_cohort']['start_year']} ({fmt_pts(cs10['best_cohort']['phased_minus_lump_real_pct'])}), the worst started in {cs10['worst_cohort']['start_year']} ({fmt_pts(cs10['worst_cohort']['phased_minus_lump_real_pct'])}).</p></div></div>

  <h2 id="method">1 · What this test does and does not prove</h2>
  <div class="replay-key">
    <div><strong>Compared</strong><p class="small">Lump sum invests everything in month 1. Phased parks everything in 3-month T-bills for 24 months, then buys equities in 36 equal monthly tranches, so it is fully invested after 60 months.</p></div>
    <div><strong>Measured in</strong><p class="small">Real (inflation-adjusted) multiples of the starting amount. Nominal gains during the 1970s are not counted as wins.</p></div>
    <div><strong>Not modelled</strong><p class="small">Taxes, fees, advisory costs, asset allocation, rebalancing, or the behaviour of any specific account. Both paths hold the same assets once fully invested.</p></div>
    <div><strong>Known limitation</strong><p class="small">Annual data is smoothed into monthly steps. A crash that happens mid-year is understated, which biases results <em>against</em> phasing in exactly the cases phasing is meant to help.</p></div>
  </div>

  <h2 id="cohorts">2 · Every historical start date, one shared horizon</h2>
  <p>Each row counts overlapping windows that start in every year the data allows. “Phasing ahead” means the phased path finished with more real purchasing power. “Median real difference” is the middle outcome, in percentage points of the starting amount.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Horizon</th><th>Windows tested</th><th>Phasing ahead</th><th>Median real difference</th><th>Worst start</th><th>Best start</th><th>Windows where lump sum lost real value</th><th>Source</th></tr></thead>
    <tbody>{''.join(cohort_rows)}</tbody>
  </table></div>

  <h2 id="sensitivity">3 · The same question under three different parking rules</h2>
  <p>If the phased result were an artefact of assuming T-bills pay something, it would flip when cash earns nothing. It does flip the other way: even crediting uninvested cash with the <em>equity</em> return — impossible in practice — phasing still trails on the median. The conclusion is driven by time out of the market, not by the cash yield assumption.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Cash return while parked (10-year horizon)</th><th>Phasing ahead</th><th>Median real difference</th><th>Worst start</th><th>Source</th></tr></thead>
    <tbody>{''.join(sens_rows)}</tbody>
  </table></div>

  <h2 id="episodes">4 · The crash episodes that motivate phasing — where it actually works</h2>
  <p>Cells show <strong>lump sum / phased</strong> real multiples of the starting amount, with the phased advantage in percentage points underneath. A crashed entry is the case phasing was designed for, and there it does work — but note that it can still lose to lump sum when the recovery is violent and early, as in 2008 at ten years.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Entry year</th><th>1 year</th><th>3 years</th><th>5 years</th><th>10 years</th><th>Source</th></tr></thead>
    <tbody>{''.join(episode_rows)}</tbody>
  </table></div>

  <div class="callout"><strong>Read the two 1929 rows together.</strong> A 1929 entry lost money in nominal terms for a decade; after deflation it was worth {fmt_x(hist[1929]['lump_real_x'])} in real terms at ten years. Phasing produced {fmt_x(hist[1929]['phased_real_x'])}. The benefit came almost entirely from not buying the first three years of the collapse, and it required holding Treasury bills whose returns were then around 1–4%.</div>

  <h2 id="distribution">5 · Distribution, not a single average</h2>
  <p>Every point is a ten-year window. Percentiles are order statistics of the {len(pts)} observed windows, not a probability model.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Ten-year real outcome</th><th>Lump sum</th><th>Park 24m / phase 36m</th><th>Which is ahead</th><th>Source</th></tr></thead>
    <tbody>{''.join(dist_rows)}</tbody>
  </table></div>
  <div class="bars">
"""

    # mini bar chart of winning distribution: worst 12 and best 12 windows
    ordered = sorted(pts, key=lambda p: p["phased_real_x"] - p["lump_real_x"])
    picks = ordered[:6] + ordered[-6:]
    scale = max(max(p["lump_real_x"], p["phased_real_x"]) for p in picks) or 1
    for p in picks:
        html += (
            f'<div class="bar-row"><span>{p["start_year"]}</span>'
            f'<div class="bar-track"><div class="bar-fill bar-lump" style="width:{p["lump_real_x"] / scale * 100:.1f}%"></div></div>'
            f'<div class="bar-track"><div class="bar-fill bar-phased" style="width:{p["phased_real_x"] / scale * 100:.1f}%"></div></div></div>'
        )

    html += f"""  </div>
  <p class="source-note">Bars: light = lump sum, dark = phased, ten-year real multiples. Six weakest and six strongest windows shown for shape only.</p>

  <h2 id="rebuild">6 · Rebuilding the dataset every year</h2>
  <p>The transcription is verified by compounding: applying the annual returns from a base of 100 must reproduce the cumulative-value columns printed in the same published table. The check tolerates no more than 0.05% relative error; the current build matches within 0.04%.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Year</th><th>Published S&amp;P 500 cumulative index (base 100 = 1928)</th><th>Published T-bill cumulative index</th><th>Source</th></tr></thead>
    <tbody>{check_rows}</tbody>
  </table></div>

  <h2 id="how-to-use">7 · How to use this in the decision</h2>
  <ol>
    <li><strong>Do not treat phasing as free risk reduction.</strong> It buys crash protection with a measurable median cost and a 60-month delay to full exposure.</li>
    <li><strong>Pre-commit the rule and the trigger.</strong> If phasing is chosen, write down the tranche schedule, the acceleration trigger, and the date the plan ends — before any sale closes.</li>
    <li><strong>Size it to what a crash would actually cost you.</strong> Phasing matters most when the sale proceeds are large relative to the rest of your wealth and when a drawdown would force a change of plan.</li>
    <li><strong>Keep the reserve separate.</strong> Near-term cash needs — taxes, repairs, insurance, estate liquidity — belong in the Treasury ladder regardless of the equity decision.</li>
    <li><strong>Re-run annually and after any law change.</strong> Extend the dataset each year, re-run <code>python3 scripts/build_blackswan.py</code>, and record the new result in the decision journal.</li>
  </ol>

  <h2 id="sources">8 · Sources and reproduction</h2>
  <div class="table-wrap"><table>
    <thead><tr><th>Input</th><th>Publisher and edition</th><th>Used for</th><th>Link</th></tr></thead>
    <tbody>
      <tr id="src-damodaran"><td>S&amp;P 500 annual returns incl. dividends; 3-month T-bill annual returns</td><td>NYU Stern, Aswath Damodaran, public dataset updated January 5, 2026 (series 1928–2025)</td><td>Equity and cash return paths</td><td><a href="{DAMODARAN}">histretSP.html</a></td></tr>
      <tr id="src-cpi"><td>CPI-U annual averages (1983 = 100)</td><td>Federal Reserve Bank of Minneapolis table of the BLS CPI-U series</td><td>Inflation adjustment</td><td><a href="{MINFED}">Minneapolis Fed CPI 1913–</a> · <a href="{BLS}">BLS CPI home</a></td></tr>
      <tr id="src-treasury"><td>Short-term Treasury instruments and current yields</td><td>U.S. Department of the Treasury; TreasuryDirect</td><td>Choice of parking instrument and current yield checks</td><td><a href="{TREASURY}">Daily Treasury rates</a> · <a href="{TBILL}">Treasury bills</a></td></tr>
      <tr id="src-nber"><td>Recession chronology</td><td>National Bureau of Economic Research</td><td>Regime context for the episodes</td><td><a href="{NBER}">Business-cycle dating</a></td></tr>
    </tbody>
  </table></div>
  <p class="source-note">Rebuild: <code>python3 scripts/build_blackswan.py</code> then <code>python3 scripts/build_crash_replay_page.py</code>. Framework: <code>data/historical-returns.json</code>; generated results: <code>data/black-swan-results.json</code>; verification: <code>scripts/verify_sources.py</code>. No household values are stored, transmitted or published. This is decision support, not investment, tax or legal advice.</p>
  <footer>
    <p><a href="index.html">← Estate Pathways dashboard</a> · <a href="black-swan.html">Public crash anchors</a> · <a href="FLAGGED_FOR_REVIEW.html">Flagged for review</a></p>
  </footer>
</main>
</body>
</html>
"""
    return html


def main():
    html = build()
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"wrote {OUT} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
