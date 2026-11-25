# TinoDash2 coordination board

## Session / branch constraint

Current integration work is owned by `arena/57bd7c20-tinodash2` and remains on that Arena-managed branch. The request's separate `session/<id>/<task>` branch convention cannot be followed because Arena requires this session to use the current branch only. Previous sessions `arena/c059149b` and `arena/78b5ae8f` have merged PRs #3 and #4 to `main`; their work is preserved in the repository history and was reviewed during this integration.

## Task board

| Task | Status | Owner | Scope / note |
|---|---|---|---|
| Official tax and law research | needs review | `arena/c059149b` | Prior source work in `pages/flagged.html` and `js/model.js`; verified against current IRS / BOE / FTB / SCO / official Legislature sources in this integration. Some previous conclusions were overbroad or tied to stale forms and are not reused without review. |
| Core dashboard and what-if model | needs review | `arena/c059149b` | Prior work merged in PR #4. Replaced public landing page with a private-input, browser-only dashboard; older model/data are being removed or quarantined from the published app due to household figures and unsourced assumptions. |
| Subpages (comparison, properties, black swan, timeline, briefing, flagged, suggestions) | needs review | `arena/c059149b` | Prior pages merged in PR #4. Preserve useful categories but redact submitted property values/ZIPs and unsupported scenario outputs before publication. Current safe dashboard includes equivalent sections and a separate flagged page. |
| Privacy remediation / safe public site integration | in progress | `arena/57bd7c20-tinodash2` | Current branch; public HTML, model, flags, source register, workflow and repository docs. Private inventory stays ignored and outside Pages. |
| Final verification, PR #5, Pages deploy | in progress | `arena/57bd7c20-tinodash2` | Awaiting rebase/merge with latest main, privacy scan, workflow, and deployment confirmation. |

## Privacy and verification policy

- Never commit identifiable names, trust terms, street addresses, parcel/APN IDs, account numbers, exact household values, leases or tax records.
- Public site must not publish any user-submitted property value, tax bill, rent, utility figure, or ZIP code. The user data in previous merged commits is treated as a privacy incident and is being removed from current published files.
- Browser what-if inputs are memory-only and rounded to the nearest $10 when displayed. No remote fonts, scripts, analytics or network submission.
- The empty estate-inventory template is Git-ignored under `private/` and excluded from the Pages artifact. A completed inventory must remain encrypted and outside Git.
- Every factual table row on the current site links to an official source or identifies a missing source. Current law, proposals, and unverifiable household claims are distinguished.

## Prior public-data exposure — urgent

PRs #3 and #4 were merged to the public `main` branch before this integration. The resulting current `main` tree and its prior commits contain household-provided ZIP codes, exact property estimates, rents, taxes, and derived forecasts in files including `README.md`, `index.html`, `properties.html`, `pages/properties.html`, `assets/model.js`, `js/model.js`, and `pages/briefing.html`. The current published page may therefore have exposed these values. PR #5 must remove/redact these values from the current tree and publish only the privacy-safe site. **Git history still retains earlier merged commits on public `main`; a normal PR cannot erase those commit objects.** A repository-history purge / force-push of the default branch and cache/index purge require repository-owner action outside this session's current-branch-only limit. Do not claim history has been scrubbed; this is flagged for urgent owner review.

## Official source register and current verification

- IRS: [2026 estate/gift tax update](https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax), [Form 706 instructions](https://www.irs.gov/instructions/i706), inherited-basis FAQ, Publications 523/544, and Section 1031 real-estate guidance.
- California BOE: [Proposition 19](https://www.boe.ca.gov/prop19/) and [2025–2027 allowance notice](https://www.boe.ca.gov/news/2025/nr-25-02.htm). The $1,044,586 amount applies only to transfers Feb. 16, 2025–Feb. 15, 2027.
- California FTB: [2025 Form 540 instructions](https://www.ftb.ca.gov/forms/2025/2025-540-instructions.html); 1% Behavioral Health Services Tax on taxable income over $1,000,000 for that tax year; separate reference-only sensitivity, not a full tax calculation.
- California State Controller: [estate tax page](https://www.sco.ca.gov/ardtax_estate_tax.html), which says no state estate return is required for deaths on or after Jan. 1, 2005 under its current framework.
- California Legislature: [SB 284 status](https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260SB284) and [amended text](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202520260SB284). Official status lists an active committee bill; the last five-history action shown is July 14, 2025, held under submission. Treated as proposed, not enacted.
- County and local starting points: Santa Clara County Assessor, SF Treasurer, SF Rent Board / DBI and official SF Elections / Prop H sources. Other official references and limitations are in `sources.md` and the site's Official Sources section.

## Verification results (current implementation)

- `python3 scripts/check_site.py`: local pages/assets/anchors exist; every data row in the public tables has a source link; no remote scripts/styles.
- `node --check app.js`, `git diff --check`: passed.
- Synthetic browser-model smoke test: comparison paths, year-by-year table and CA surtax sensitivity rendered; test values were not written to files.
- Privacy grep: submitted figures and ZIPs were absent from this branch before rebase; re-run against the integrated tree before pushing.
- Local HTTP preview returned 200 for dashboard and Flagged for Review page.

## Known limitations / flagged items

No independently verified date-of-death appraisal, actual parcel TRA/tax rate, market-rent comparables, leases, legal unit records, insurance quotes, utility bills, maintenance plan, debt, depreciation/basis records, estate inventory, eligibility facts or tax-adviser estimates are available. No numerical 1929/2008 replay is published without a documented total-return series and methodology. The browser model is simplified/pre-tax, leaves parcel assessment and tax complexity unmodeled, and deliberately does not rank a winner. See `FLAGGED_FOR_REVIEW.html`.

## Deployment / PR log

PR #5: https://github.com/kanlerxz87-cyber/TinoDash2/pull/5 — open; needs updated tree / checks after integration. Merge and Pages deployment status pending.
