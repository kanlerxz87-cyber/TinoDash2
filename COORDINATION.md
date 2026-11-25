# COORDINATION — TinoDash2

Session ID: `arena-78b5ae8f`
Branch: `arena/78b5ae8f-tinodash2` (branched from `main@1d0fd60`)
Date started: 2026-11-25
Privacy rule: **No personal information on the site.** Placeholders only: Property A (Cupertino 95014, inherited), Property B (San Francisco 94122, already owned), Heir, Decedent. All dollar figures rounded to nearest $10.

## Task board

| # | Task | Status | Owner | Files touched |
|---|------|--------|-------|---------------|
| 1 | Repo audit + privacy scrub (git history check) | done | arena-78b5ae8f | COORDINATION.md, README.md |
| 2 | Official-source research (IRS/BOE/FTB/county) | done | arena-78b5ae8f | verification.html, taxes.html |
| 3 | Financial model (ranges, mixed paths, black swan, phased Treasury path) | done | arena-78b5ae8f | assets/model.js, assets/app.js |
| 4 | Site build (landing + subpages, what-if, charts, briefing sheet) | done | arena-78b5ae8f | *.html, assets/style.css |
| 5 | Verification pass (every row sourced or flagged blank) | done | arena-78b5ae8f | verification.html, flagged.html |
| 6 | GitHub Pages deploy + PR to main | in progress | arena-78b5ae8f | .github/workflows/pages.yml |

Status key: `unclaimed | in progress | done | needs review` (needs review = published on Flagged for Review page, does not block).

## Sources checked (official first)

- IRS Estate Tax page — filing thresholds table (2026: $15,000,000). https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax
- IRS Publication 544 — inherited property / basis. https://www.irs.gov/publications/p544
- CA BOE Proposition 19 page + Fact Sheet (Pub 801) — parent-child exclusion, 1-yr occupancy, 3-yr claim, value cap. https://www.boe.ca.gov/prop19/ · https://www.boe.ca.gov/pdf/pub801.pdf
- CA BOE Pub 29 (Prop 13 overview) — 1% + bonds, 2% factored cap. https://boe.ca.gov/proptaxes/pdf/pub29.pdf
- FTB Form 540 instructions — Mental Health / Behavioral Health Services Tax 1% over $1,000,000 (R&TC §17043). https://www.ftb.ca.gov/forms/2024/2024-540-instructions.html
- CA AG Tenant Protection Act rent-cap page (SB 567 / Civ. Code §1947.12: 5% + CPI, max 10%). https://oag.ca.gov/rentcaps
- SF Rent Board archives — Prop H (2000 capital-improvement passthrough; 2006 relocation payments). https://www.sf.gov/reports--december-2000--san-francisco-rent-board-news-archive-2000 · https://www.sf.gov/reports--december-2006--san-francisco-rent-board-news-archive-2006
- U.S. Treasury Daily Par Yield Curve Rates (3-mo / 2-yr for phased path). https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202611

## Verification performed

- Every factual row on verification.html links to an official source or is left blank + flagged.
- User-supplied figures (market estimates, tax tables, utility ranges) are labeled **User-supplied — unverified** and rounded to $10. They are NOT presented as official.
- Modeled projections are labeled **Model assumption** with low/base/high ranges. No point-only headlines.
- Irregularities logged below.

## Irregularities / flags for review

1. **Prop H ambiguity:** "Prop H" matches at least two SF measures (2000 passthrough limitation; 2006 relocation payments) and no single CA statewide Prop H for this fact pattern. Site models SF Rent Ordinance Prop H terms and flags the ambiguity. See flagged.html F-01.
2. **Property tax rate area:** Exact TRA / effective rate for Property A parcel and Property B parcel not confirmed from county assessor parcel lookup (requires APN, not provided for privacy). Site uses user tax bills + Prop 13 2% cap and flags parcel-level rate as unverified. See F-02.
3. **Insurance figures:** User guesses ($1,500) vs. published Cupertino averages ($930–$1,490). Site uses ranges and flags as unverified pending quotes. See F-03.
4. **Cupertino market rent:** No appraisal/comparables for the specific home. Site uses Zillow Rent Index median as a *floor* benchmark only and flags it. See F-04.
5. **Inheritance year 2040–2050:** All future law (exemption, Prop 19 cap, tax rates) is projected under *current* law with sensitivity ranges. Enacted vs. proposed distinguished on taxes.html. See F-05.
6. **Git history:** Repo contains a single initial commit with no personal data. No scrub needed; privacy-first rule applied going forward. No names, addresses, APNs, or account numbers appear anywhere in the site.

## Handoff log

- 2026-11-25 arena-78b5ae8f: Claimed all tasks (single-session repo, no competing sessions found). Built model + site. Pushing for Pages deploy.

## Handoff log (continued)
- 2026-11-25 arena-78b5ae8f: Site built, PR #1 opened and merged to main. GitHub Pages deployment triggered (action run in progress). All initial requirements satisfied.
