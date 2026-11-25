# TinoDash2 coordination board

## Session / branch constraints

Current integration work belongs to `arena/57bd7c20-tinodash2` and remains on this Arena-managed branch. The request's separate session-branch convention cannot be followed because the Arena session is fixed to the current branch. Previous sessions `arena/c059149b` and `arena/78b5ae8f` merged PRs #3 and #4 to `main`; their work was reviewed and preserved where safe during this integration.

## Task board

| Task | Status | Owner | Scope / note |
|---|---|---|---|
| Official tax and law research | needs review | `arena/c059149b` | Prior research merged in PR #4. Current integration checked IRS / BOE / FTB / SCO / official Legislature sources; stale or overbroad prior conclusions are not reused without review. |
| Core dashboard and what-if model | needs review | `arena/c059149b` | Prior work merged in PR #4. New landing page replaces household-specific public defaults with browser-only inputs; old model data files must be removed or quarantined before publication. |
| Subpages (comparison, properties, black swan, timeline, briefing, flagged, suggestions) | needs review | `arena/c059149b` | Prior pages merged in PR #4. Useful categories are represented in the new safe dashboard; old pages with user figures / unsupported scenarios must not be published. |
| Privacy remediation / safe public site integration | in progress | `arena/57bd7c20-tinodash2` | Current branch; dashboard, sources, private template, flags, static checks and Pages artifact. |
| Final verification, PR #5, Pages deploy | in progress | `arena/57bd7c20-tinodash2` | Rebase in progress against latest main; re-run all checks, privacy audit, PR checks and deploy confirmation. |

## Privacy and verification policy

- Never commit identifiable names, trust details, street addresses, parcel/APN IDs, account numbers, exact household values, leases or private tax records.
- Public site must not publish user-submitted property prices, tax bills, rents, utility figures or ZIP codes. Earlier merged pages are treated as a privacy incident and are being removed from the current tree before the new site is deployed.
- What-if calculations run only in browser memory, transmit nothing, and display values rounded to the nearest $10. No remote fonts, scripts, analytics or network submission.
- The empty estate-inventory template is Git-ignored under `private/` and excluded from the Pages artifact. Completed inventories must remain encrypted and outside Git.
- Public facts are linked to official sources; current law, proposals and unverifiable household facts are distinguished.

## Prior public-data exposure — urgent

PRs #3 and #4 merged to the public `main` before this integration. The `main` tree and prior commits contain household-provided ZIP codes, exact property estimates, rents, taxes and derived forecasts in `README.md`, `index.html`, `properties.html`, `pages/properties.html`, `assets/model.js`, `js/model.js`, `pages/briefing.html` and other files. The deployed page may have exposed these values. PR #5 must remove the figures from the current published files and publish only privacy-safe content.

**Git history still retains prior merged commit objects.** A normal PR cannot erase those commits. A history purge / force-push of the default branch and any cache/search-index removal require repository-owner action and are outside this session's current-branch-only restriction. Do not claim that history has been scrubbed. This is flagged for urgent owner review.

## Official source register and current verification

- IRS: [2026 estate/gift tax update](https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax), [Form 706 instructions](https://www.irs.gov/instructions/i706), inherited-basis FAQ, Publications 523/544, and Section 1031 real-estate guidance.
- California BOE: [Proposition 19](https://www.boe.ca.gov/prop19/) and [2025–2027 allowance notice](https://www.boe.ca.gov/news/2025/nr-25-02.htm). The $1,044,586 amount applies only to transfer dates Feb. 16, 2025–Feb. 15, 2027.
- California FTB: [2025 Form 540 instructions](https://www.ftb.ca.gov/forms/2025/2025-540-instructions.html); the 1% Behavioral Health Services Tax applies above $1,000,000 taxable income for that tax year. Site sensitivity is reference-only, not a full tax calculation.
- California State Controller: [estate tax page](https://www.sco.ca.gov/ardtax_estate_tax.html), which says no California estate return is required for deaths on or after Jan. 1, 2005 under the current framework.
- California Legislature: [SB 284 status](https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260SB284) and [amended text](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260SB284). Official page lists an active committee bill; last five-history item shown is July 14, 2025, held under submission. Treated as proposed, not enacted.
- County and local starting points: Santa Clara County Assessor, SF Treasurer, Rent Board / DBI, official SF Elections / Prop H. Full URLs and use limits are in `sources.md` and on the site.

## Verification performed on the privacy-safe implementation

- `python3 scripts/check_site.py`: local pages/assets/anchors exist, every data row in public tables is source-linked, no remote scripts/styles.
- `node --check app.js`, `git diff --check`: passed.
- Synthetic browser-model smoke test: comparison paths, year-by-year projections and CA surtax sensitivity rendered; test values were not saved.
- Privacy grep was clean before rebase; it must be repeated against the integrated tree before any push.
- Local HTTP preview returned 200 for dashboard and Flagged for Review pages.

## Known limitations / flagged items

No independently verified date-of-death appraisal, parcel tax rate area, market-rent comparables, leases, legal unit records, insurance quotes, utility bills, maintenance plan, debt, depreciation/basis records, estate inventory, eligibility facts or tax-adviser estimates are available. No numeric 1929/2008 replay is published without a reproducible total-return series and method. The model is illustrative / pre-tax, omits parcel reassessment and other tax details, and does not recommend a winner. See `FLAGGED_FOR_REVIEW.html`.

## Deployment / PR log

PR #5: https://github.com/kanlerxz87-cyber/TinoDash2/pull/5 — open; needs integrated privacy remediation and checks. Merge and Pages deployment status pending.
