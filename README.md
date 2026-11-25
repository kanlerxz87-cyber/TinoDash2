# TinoDash2 — Cupertino Inheritance Decision Desk

Private, **anonymized** decision-support model for one question: *what should happen to an
inherited Cupertino home (“Property A”) — live, rent, sell-and-reinvest (staged), or a mixed
path — versus the San Francisco rental triplex (“Property B”) the heir already owns outright?*

**Live site:** https://kanlerxz87-cyber.github.io/TinoDash2/

## Privacy posture (non-negotiable)

- **No real names, street addresses, parcel numbers, account numbers or trust document names
  anywhere** — in the site, the repo, commits, or issues. Placeholders only.
- **All monetary figures are rounded to the nearest $10** so they cannot be reversed to a
  source document or listing.
- Git history audit (2026-11-25): a single pre-existing commit (`1d0fd60`, “Initial commit”,
  README only). **No pre-rounding figures, no personal data exist in any commit or tag.**
- Public Pages exposure is limited to this anonymized content by construction.
- If raw personal data is ever committed by accident: rotate secrets, remove the file in a
  follow-up commit **and** request a GitHub Support cache purge; a force-push alone does not
  expunge forks/caches.

## What’s inside `/docs` (the published site)

| Page | What it answers |
|---|---|
| `index.html` | Executive dashboard — “what would change the answer” first, headline + reinvestment risk paired |
| `brief.html` | One-page printable Attorney & CPA Briefing Sheet (pre-commitment signatures) |
| `property-a.html` / `property-b.html` | Rounded tax/assessment ledgers, Prop 19 math, capital plans, rent P&L, SF Prop H model |
| `compare.html` | Pure vs mixed paths, same dates/horizons — taxes, debt, occupancy, capital costs, liquidity |
| `mixed.html` | Mixed paths incl. Black-Swan staged entry (24–36 mo T-bills → equities) |
| `black-swan.html` | 1929/1973/2000/2008/2020 stress tables + annual extreme-scenario review |
| `projections.html` | 50-year projections, Monte Carlo fan + outcome distribution, live what-if sliders |
| `taxes.html` | Estate ≠ basis ≠ property tax; Form 540 line 62 (1% over $1M); recapture; §121; step-up |
| `process.html` | Step-by-step inheritance sequence with red-flag deadlines (Form 706 9 mo; Prop 19 3 yr) |
| `questions.html` | 40 open questions — who answers, how to discover, what they change |
| `suggestions.html` | Review board of site improvements — nothing auto-implements |
| `policy.html` | Investment Policy Statement + written pre-commitment rulebook (anti-reverse-engineering) |
| `journal.html` | Decision journal — decision + date beside every item |
| `glossary.html` | Grouped glossary |
| `sources.html` | Verification log; enacted vs proposed legislation; annual re-check calendar |
| `flagged.html` | Flagged for Review — every irregularity/unverified figure with its settling source |

## Method notes

- Figures are rounded to $10 and are planning estimates, not quotes; formulas shown on each page.
- Model baseline: Nov 2026, inheritance ≈ 2040; property growth 4%/yr (3–5% band), equity 7%/yr (2–12% band), CPI 2.4%, 2% assessed-value cap (RTC §51), 1.34% property-tax composite (Property A ledger-implied), Prop 19 allowance $1,044,586 (Feb 2025–Feb 2027 window).
- Every unverifiable figure is listed on `flagged.html` with the official source that would close it.
- Educational decision-support only — **not legal, tax or investment advice**. Attorney and CPA outrank this site.

## Coordination & parallel sessions

See [COORDINATION.md](COORDINATION.md) — the shared task board (claims, irregularities log, handoff protocol). This session executed and integrated the full site; the final integration merge records PR/deploy there.

## Disclaimer

Not affiliated with any county, state or federal agency. No warranty; verify everything against official sources linked on the Sources page before acting.
