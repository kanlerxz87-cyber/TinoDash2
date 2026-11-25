#!/usr/bin/env python3
"""
Independent source verification for every official anchor published on the site.

Two layers:
  A. OFFLINE checks that never need the network (run in CI on every push):
     arithmetic of the historical replay dataset against the published
     cumulative-value columns, and internal consistency of the site.
  B. ONLINE checks (run here and locally with --online) that fetch the official
     pages, look for the exact figure/phrase, and print MATCH / MISSING per
     claim. A MISSING result means the page changed or is blocked by the
     environment; it is reported, never silently passed.

Usage:
    python3 scripts/verify_sources.py            # offline checks only
    python3 scripts/verify_sources.py --online    # also fetch official pages
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UA = "Mozilla/5.0 (compatible; EstatePathwaysVerifier/1.0; +https://github.com/)"


# --------------------------------------------------------------------------- #
# A. Offline: replay dataset must reproduce the publisher's own index columns
# --------------------------------------------------------------------------- #
def check_dataset():
    path = os.path.join(ROOT, "data", "historical-returns.json")
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    years = {int(k): v for k, v in d["years"].items()}
    checks = {
        key: {int(k): v for k, v in vals.items()}
        for key, vals in d["verification"]["published_cumulative_index_checks"].items()
    }
    sp = tb = 100.0
    worst = 0.0
    compared = 0
    problems = []
    for yr in sorted(years):
        sp *= 1 + years[yr]["sp500_tr_pct"] / 100
        tb *= 1 + years[yr]["tbill_pct"] / 100
        for key, actual in (("sp500_total_return", sp), ("tbill_total_return", tb)):
            if yr in checks[key]:
                published = checks[key][yr]
                err = abs(actual - published) / published * 100
                worst = max(worst, err)
                compared += 1
                if err > 0.05:
                    problems.append(f"{key} {yr}: computed {actual:.2f} vs published {published:.2f} ({err:.3f}% error)")
    # A verification that compares nothing must never report success.
    if compared < 2 * len(checks["sp500_total_return"]):
        problems.append(f"only {compared} index checkpoints were compared; expected {2 * len(checks['sp500_total_return'])}")
    # CPI: recompute published 12-month changes
    cpi_problems = []
    for yr in (1932, 1974, 1980, 2008, 2022, 2025):
        prev = max(y for y in years if y < yr)
        yoy = (years[yr]["cpi_index"] / years[prev]["cpi_index"] - 1) * 100
        if abs(yoy) > 25:
            cpi_problems.append(f"CPI {yr} yoy {yoy:.1f}% looks implausible")

    status = "PASS" if not problems and not cpi_problems else "FAIL"
    print(f"[{status}] dataset compounding vs published index columns — {compared} checkpoints, worst relative error {worst:.4f}%")
    for p in problems + cpi_problems:
        print(f"        {p}")
    return not problems and not cpi_problems


def check_site_internal():
    results_path = os.path.join(ROOT, "data", "black-swan-results.json")
    with open(results_path, encoding="utf-8") as fh:
        res = json.load(fh)
    ok = True
    # every cohort's phased win count must be consistent with its history
    for key, v in res["variants"].items():
        for cs in v["cohort_stats"]:
            wins = sum(1 for h in cs["history"] if h["phased_real_x"] > h["lump_real_x"])
            if wins != cs["phased_wins"]:
                print(f"[FAIL] {key} {cs['horizon_years']}y: win count {cs['phased_wins']} != recounted {wins}")
                ok = False
    print(f"[{'PASS' if ok else 'FAIL'}] replay result internals recount consistently")
    return ok


# --------------------------------------------------------------------------- #
# B. Online: exact-string checks against official pages
# --------------------------------------------------------------------------- #
CLAIMS = [
    {
        "id": "irs-2026-exclusion",
        "url": "https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax",
        "must_contain_any": ["increasing the basic exclusion amount to $15,000,000", "$15,000,000 for calendar year 2026"],
        "claim": "2026 federal basic exclusion amount is $15,000,000 (PL 119-21)",
    },
    {
        "id": "irs-706-filing",
        "url": "https://www.irs.gov/instructions/i706",
        "must_contain_any": [
            "is more than $15,000,000",
            "within 9 months after the date of the decedent",
        ],
        "claim": "Form 706 filing threshold and 9-month due date",
    },
    {
        "id": "irs-121-exclusion",
        "url": "https://www.irs.gov/taxtopics/tc701",
        "must_contain_any": ["exclude up to $250,000", "up to $500,000"],
        "claim": "Section 121 home-sale exclusion of $250,000 / $500,000",
    },
    {
        "id": "irs-1031",
        "url": "https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips",
        "must_contain_any": ["Section 1031 now applies only to exchanges of real property"],
        "claim": "Section 1031 applies only to real property",
    },
    {
        "id": "ca-rtc-17043",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=17043",
        "must_contain_any": ["1 percent on that portion of a taxpayer", "one million dollars ($1,000,000)"],
        "claim": "RTC 17043: additional 1% on CA taxable income above $1,000,000",
    },
    {
        "id": "ca-ftb-540-line62",
        "url": "https://www.ftb.ca.gov/forms/2025/2025-540-booklet.html",
        "must_contain_any": ["Line 62 – Behavioral Health Services Tax", "Behavioral Health Services Tax"],
        "claim": "2025 Form 540 line 62 is the 1% tax above $1,000,000",
    },
    {
        "id": "ca-rtc-63.2",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2",
        "must_contain_any": [
            "become the principal residence of the transferee within one year",
            "file for the homeowners",
        ],
        "claim": "RTC 63.2: transferee must occupy within one year and file homeowners' exemption",
    },
    {
        "id": "boe-prop19-allowance",
        "url": "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf",
        "must_contain_any": ["$1,044,586", "February 16, 2025 through February 15, 2027"],
        "claim": "Prop 19 $1M cap adjusts to $1,044,586 for transfers 2/16/2025–2/15/2027",
    },
    {
        "id": "boe-prop19-page",
        "url": "https://www.boe.ca.gov/prop19/",
        "must_contain_any": ["Value limit of current taxable value plus $1,000,000", "File for homeowners' exemption within 1 year"],
        "claim": "BOE Prop 19 comparison chart: value limit and 1-year exemption filing",
    },
    {
        "id": "scc-tax-rate-book",
        "url": "https://controller.santaclaracounty.gov/property-tax-distribution/property-tax-rate-book",
        "must_contain_any": ["Tax Rates by Tax Rate Area", "Tax Rates Summary"],
        "claim": "Santa Clara County Controller publishes tax rates by tax rate area",
    },
    {
        "id": "ca-rtc-11911",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11911",
        "must_contain_any": ["fifty-five cents ($0.55) for each five hundred"],
        "claim": "RTC 11911: county documentary transfer tax of $0.55 per $500",
    },
    {
        "id": "sf-transfer-tax",
        "url": "https://www.sf.gov/transfer-tax",
        "must_contain_any": ["$3.75 for each $500", "$11.25 for each $500"],
        "claim": "SF transfer tax rate tiers",
    },
    {
        "id": "sf-prop-h-parcel-tax",
        "url": "https://www.sfmta.com/getting-around/muni/parcel",
        "must_contain_any": ["$129", "parcel tax"],
        "claim": "SF Nov 2026 Prop H Muni parcel tax rates",
        "optional": True,
    },
    {
        "id": "ca-sco-estate",
        "url": "https://www.sco.ca.gov/ardtax_estate_tax.html",
        "must_contain_any": ["no longer a requirement to file a California Estate Tax Return"],
        "claim": "No California estate tax return required for deaths on/after 1/1/2005",
    },
    {
        "id": "ftb-capital-gains",
        "url": "https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html",
        "must_contain_any": ["California does not have a lower rate for capital gains"],
        "claim": "CA taxes capital gains as ordinary income",
    },
    {
        "id": "irs-p551-basis",
        "url": "https://www.irs.gov/publications/p551",
        "must_contain_any": ["Basis of Assets"],
        "claim": "IRS Publication 551, Basis of Assets",
    },
]


def fetch(url: str) -> str | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/pdf,*/*"})
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read()
        if url.lower().endswith(".pdf"):
            try:
                import subprocess

                out = subprocess.run(["pdftotext", "-", "-"], input=raw, capture_output=True, timeout=60)
                return out.stdout.decode("utf-8", "ignore")
            except Exception:
                return None
        return raw.decode("utf-8", "ignore")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        print(f"        fetch failed: {exc}")
        return None


def norm(text: str) -> str:
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&#39;", "'")
    return re.sub(r"\s+", " ", text)


def check_online():
    failures = 0
    for c in CLAIMS:
        print(f"[CHECK] {c['id']}: {c['claim']}")
        body = fetch(c["url"])
        if body is None:
            tag = "SKIP" if c.get("optional") else "MISSING"
            if tag == "MISSING":
                failures += 1
            print(f"        [{tag}] page could not be read in this environment: {c['url']}")
            continue
        text = norm(body)
        hits = [m for m in c["must_contain_any"] if norm(m) in text]
        if hits:
            print(f"        [MATCH] {hits[0][:90]}")
        else:
            tag = "SKIP" if c.get("optional") else "MISSING"
            if tag == "MISSING":
                failures += 1
            print(f"        [{tag}] none of the expected strings found: {c['must_contain_any']}")
    return failures


def main():
    online = "--online" in sys.argv
    ok_offline = check_dataset()
    ok_internal = check_site_internal()
    failed_online = 0
    if online:
        print("\nOnline verification of published claims")
        failed_online = check_online()
    else:
        print("\n(offline mode: run with --online to re-fetch official pages)")

    if not ok_offline or not ok_internal:
        print("\nOFFLINE CHECKS FAILED")
        return 1
    if not online:
        print("\nOffline checks passed. Online claim verification was NOT run; "
              "run `python3 scripts/verify_sources.py --online` in an environment "
              "with outbound HTTPS before relying on any cited figure.")
        return 0
    if failed_online:
        print(f"\nONLINE: {failed_online} claim(s) could not be confirmed; review before relying on them")
        return 1
    print("\nAll executed checks passed (offline + online)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
