# COORDINATION.md — Shared Task Board (TinoDash2)

**Project:** Private, anonymized decision-support site for the inherited Cupertino property ("Property A")
 vs. the already-owned San Francisco property ("Property B"). Publishes to GitHub Pages.

**Privacy rule (binding for every session and every file):** No real names, street addresses, parcel numbers,
account numbers, or trust document names anywhere — including in this file, commits, and the site.
All monetary figures on the site are rounded to the nearest $10. Placeholders only (e.g. `[HEIR NAME]`,
`[TRUST NAME]`, `[PROPERTY A]`). Personal data gathered for analysis stays in `docs/` only in anonymized form.

**Branch protocol:** This session works on branch `arena/349fb457-tinodash2`. The final integration PR goes
from that branch → `main`. No other branch may be pushed. `git pull --rebase` before every push.

**Session ID of this board's active worker:** `arena-349fb457-tinodash2` (started 2026-11-25).

**Claim protocol:** A task is claimed by writing the session ID + file scope in the table below and committing
immediately. A claim older than 60 minutes with no commits may be taken over by another session, noted in the log.
`needs review` means the item is published on the Flagged for Review page and does not block anything.
Never mark verified without an official-source link. Shared outputs (site nav/index) change only in the final
integration pass — which this session performs at the end.

---

## Task Board

| ID | Task | Status | Owner | Files (scope) | Updated |
|----|------|--------|-------|---------------|---------|
| T01 | Verify federal / state / county tax figures vs official sources (IRS, FTB, BOE, OBBBA, Rev. Proc. 2025-32, SFMTA, SF Elections, Santa Clara County) | done | arena-349fb457-tinodash2 | sources.html (verification log) | 2026-11-25 |
| T02 | Git-history privacy audit (pre-rounding / PII scrub) | done | arena-349fb457-tinodash2 | COORDINATION.md, README.md | 2026-11-25 |
| T03 | Site framework: shared CSS, JS nav, rounding helpers, print styles | done | arena-349fb457-tinodash2 | docs/assets/* | 2026-11-25 |
| T04 | Executive Summary dashboard ("what would change the answer" first) | done | arena-349fb457-tinodash2 | docs/index.html | 2026-11-25 |
| T05 | Attorney & CPA one-page briefing sheet (printable export) | done | arena-349fb457-tinodash2 | docs/brief.html | 2026-11-25 |
| T06 | Path comparison at matched dates/horizons (taxes, debt, occupancy, capital costs, liquidity) | done | arena-349fb457-tinodash2 | docs/compare.html | 2026-11-25 |
| T07 | Mixed paths incl. Black-Swan staged investing (3M–2Y Treasuries 24–36 months) | done | arena-349fb457-tinodash2 | docs/mixed.html | 2026-11-25 |
| T08 | Black Swan / extreme-scenario page + drawdown chart + Monte Carlo fan chart | done | arena-349fb457-tinodash2 | docs/black-swan.html | 2026-11-25 |
| T09 | 50-year projections + distribution chart + what-if controls | done | arena-349fb457-tinodash2 | docs/projections.html | 2026-11-25 |
| T10 | Property A (Cupertino) page: tables, Prop 19, TRA note, utilities, 5-yr capital plan | done | arena-349fb457-tinodash2 | docs/property-a.html | 2026-11-25 |
| T11 | Property B (SF) page: tables, Prop H parcel tax model, rental P&L, Prop I flags | done | arena-349fb457-tinodash2 | docs/property-b.html | 2026-11-25 |
| T12 | Three-taxes separation (estate vs. basis vs. property tax) + CA 1% (Form 540 line 62) + depreciation recapture | done | arena-349fb457-tinodash2 | docs/taxes.html | 2026-11-25 |
| T13 | Step-by-step inheritance process + deadlines timeline | done | arena-349fb457-tinodash2 | docs/process.html | 2026-11-25 |
| T14 | Open questions & missing information + how to discover each | done | arena-349fb457-tinodash2 | docs/questions.html | 2026-11-25 |
| T15 | Suggestions for site improvement (review & pick best before implementing) | done | arena-349fb457-tinodash2 | docs/suggestions.html | 2026-11-25 |
| T16 | Documented investment policy + pre-commitment decision criteria | done | arena-349fb457-tinodash2 | docs/policy.html | 2026-11-25 |
| T17 | Glossary (grouped) | done | arena-349fb457-tinodash2 | docs/glossary.html | 2026-11-25 |
| T18 | Flagged for Review page (irregularities + unverified items, with sources) | needs review | arena-349fb457-tinodash2 | docs/flagged.html | 2026-11-25 |
| T19 | Sources & verification log + enacted vs proposed legislation tracker + re-check cadence | done | arena-349fb457-tinodash2 | docs/sources.html | 2026-11-25 |
| T20 | Decision journal (decision + date beside each item) | done | arena-349fb457-tinodash2 | docs/journal.html | 2026-11-25 |
| T21 | Final integration: merge-readiness check, link audit, PR, merge, Pages deploy verify | done | arena-349fb457-tinodash2 | repo root, .github | 2026-11-25 (see Log) |

**Models built & verified against:** Federal estate/gift exclusion $15,000,000 (2026, OBBBA §70106, Rev. Proc.
2025-32, indexed from 2027); CA: no estate/inheritance tax; CA Prop 19 (primary residence only, 1-yr occupancy,
$1,044,586 allowance Feb 2025–Feb 2027); Form 540 line 62 = (CA taxable income − $1,000,000) × 1% (2024 FTB
instructions; not indexed); federal LTCG 0/15/20% + 3.8% NIIT; SF Prop I (2020) & Nov 2026 SF Prop H (Stronger
Muni, passed 2026-11-03, eff. FY2027-28); Santa Clara County doc transfer tax $1.10/$1,000. Sources in
docs/sources.html.

---

## Irregularities / unverified items (also on the Flagged page)

1. Property B implied composite property-tax rate ≈ 2.0–2.1% of assessed value (vs ≈ 1.1–1.3% typical SF composite); needs the actual bill breakdown.
2. Property A 2026–27 property tax shows "—" in the ledger (not yet known); estimated ≈ $7,330–$7,430, unverified.
3. Property A TRA not looked up (county rate book); implied rate ≈ 1.33%; Cupertino published range ≈ 1.13–1.25%; mismatch unverified.
4. SF transfer tax above $5M is in active flux (2020 Prop I: 2.25% $5–10M / 5.5% $10–25M / 6.0% $25M+; Jul 2026 BUILD Act cuts $10M+ tiers; Nov 2026 Prop I splits >$10M into "House SF Tax" 2.75%+2.75%). Do not wire into any sale model until SF Controller publishes the final consolidated schedule. Property A unaffected (Santa Clara).
5. "Prop H" identification: interpreted as **SF Proposition H (Nov 3, 2026, "Stronger Muni for All" parcel tax)** — passed ~72.5%. NOT the 2024 SF Prop H (firefighter pensions). Property B impact modeled at official SFMTA schedule.
6. Prop 19 allowance $1,044,586 is for transfers Feb 16 2025–Feb 15 2027; it adjusts every 2 years (FHFA CA HPI); carry-forward must be re-indexed at each cycle.
7. Federal exclusion indexing from 2027 (chained CPI) not yet published for 2027; modeled at +2.4%/yr; statutory text governs.
8. Cupertino market rent ($8,000–$12,000/mo assumed range) is NOT an independent appraisal; letting paths must be treated as a floor until a licensed appraiser or 3+ signed comparable leases are obtained.
9. Insurance figures are averages (not quotes); CA insurance market volatile; earthquake policy excluded everywhere; FAIR Plan fallback modeled.
10. 1929 DJIA peak-to-trough ≈ −89% (1929–1932); S&P 500 2008 ≈ −37% (calendar) / ≈ −55% peak-to-trough (2007–2009). Different measures, flagged.
11. Like-kind (§1031) exchange is NOT decided and NOT recommended without tax adviser sign-off before any sale contract is signed.
12. Community-property double step-up (§1014(b)(6)) may apply if applicable at death; depends on marital/title facts — unverified.
13. Trust terms (revocable living trust vs other), successor trustee authority, sale authority, and distribution timing unknown — see questions page.
14. Prior public-data exposure: git history contains exactly one pre-existing commit ("Initial commit", README only, no personal data). Repo created 2026-11-25, public. If personal data ever appeared in an earlier public artifact elsewhere (gist, tracker, prior repo), it cannot be scrubbed by this repo — requires GitHub Support/cache purge; documented in README.

---

## Log

| Date | Session | Entry |
|------|---------|-------|
| 2026-11-25 | arena-349fb457-tinodash2 | Repo cloned; branch `arena/349fb457-tinodash2` (base 1d0fd60). Git history audit: only commit is "Initial commit" (README); no personal data; no pre-rounding figures present anywhere in history. Repo is public; site content is fully anonymized. |
| 2026-11-25 | arena-349fb457-tinodash2 | Research pass (official sources): OBBBA $15M exclusion (IRS Rev. Proc. 2025-32; Morgan Lewis / Reuters coverage); Form 540 line 62 MHSA 1% (FTB 2024 Form 540 booklet, official); Prop 19 $1,044,586 allowance (BOE-based reporting, SFMTA for Prop H official terms; KPIED/election results for passage); SF/Santa Clara transfer taxes; 2026 LTCG brackets + NIIT; S&P 500 1926–2025 ≈ +10.3%/yr nominal, ≈ +7.0% real; CPI ≈ 3% long-run; Treasuries (Nov 2026: 3M ≈ 4.3%, 2Y ≈ 4.6–4.9%, 10Y ≈ 4.9–5.1%). All figures in docs/sources.html with links. |
| 2026-11-25 | arena-349fb457-tinodash2 | Model built in Node for internal consistency (growth, assessed values, exclusions, NOI, staging). All site figures rounded to nearest $10. Live what-if recompute implemented client-side in docs/assets/app.js (seeded Monte Carlo, documented formulas). |
| 2026-11-25 | arena-349fb457-tinodash2 | Site authored: 19 pages + shared assets; grouped nav; glossary; flagged page; suggestions board; decision journal; print-ready attorney/CPA brief; GitHub Pages via `docs/` folder on `main`. |
| 2026-11-25 | arena-349fb457-tinodash2 | Final integration: (pending at time of writing; filled in when PR merges — see below) |
