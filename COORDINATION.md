# Coordination board

Session: `arena/3ba11c7d-tinodash2` (Arena-assigned active branch). The requested per-task branches / integration branch cannot be used because Arena fixes this session to the current branch. No other task claims existed at start.

| Task | Status | Owner | Files |
|---|---|---|---|
| Audit starter history; build privacy-first, source-linked inheritance decision dashboard, model worksheets, print brief and supporting pages; verify sources/build | done | arena/3ba11c7d-tinodash2 | `COORDINATION.md`, `README.md`, `.nojekyll`, `.github/workflows/pages.yml`, `assets/*`, `*.html` |

## Verification and handoff log

### Initial repository / privacy audit
- Repository initially contained only a generic 22-byte `README.md`; no site, case data, property values, user information or sensitive historical file was present in the available Git history. The initial commit was not rewritten because the available history contained no personal/property data to remove. Public-host caches outside this repository cannot be purged from this checkout.
- Exact property values, postal codes, property-tax histories, rents, utilities, insurance estimates, personal identities, parcel/APN identifiers and account records from the conversation were intentionally not copied into the public website. Public site labels use only Property A / Property B. `robots` metadata requests no indexing; it is not a privacy guarantee.
- The static app has no backend, analytics, external fonts, cookies or application persistence. Calculators run client-side. Users are warned not to enter confidential data; browsers/hosting infrastructure may process ordinary page requests/session metadata.

### Official sources checked (research date: Nov. 25, 2026)
- IRS, 2026 federal basic estate exclusion: https://www.irs.gov/newsroom/working-families-tax-cuts
- IRS estate-tax / Form 706 / portability FAQ: https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes
- IRS inherited basis, Pub. 551: https://www.irs.gov/publications/p551
- IRS home sale, Pub. 523; residential rental depreciation, Pub. 527; like-kind exchange, Form 8824: https://www.irs.gov/publications/p523 ; https://www.irs.gov/publications/p527 ; https://www.irs.gov/instructions/i8824
- California BOE Prop 19 and transfer-date allowance: https://www.boe.ca.gov/prop19/
- California BOE assessment / Proposition 13 / Proposition 8 guidance: https://www.boe.ca.gov/pdf/pub800-10.pdf ; https://www.boe.ca.gov/proptaxes/decline-in-value/
- California FTB 2025 Form 540 (1% Behavioral Health Services Tax above $1 million taxable income) and Schedule CA capital-gain treatment: https://www.ftb.ca.gov/forms/2025/2025-540-instructions.html ; https://www.ftb.ca.gov/forms/2025/2025-540-ca-instructions.html
- California State Controller current estate-tax filing guidance (no CA estate-tax return required for post-2004 deaths under current guidance): https://www.sco.ca.gov/ardtax_taxinfo_estate_return.html
- SF Department of Elections preliminary Nov. 3, 2026 results (updated Nov. 23): https://www.sfelections.org/results/20261103/index.html
- Official SF Proposition H ballot title/summary and voter pamphlet; SF Controller parcel-tax economic impact report: https://media.api.sf.gov/documents/Title_and_Summary_-_Parcel_Tax_to_Fund_Public_Transit_Operations_002.pdf ; https://media.api.sf.gov/documents/N26_EN_VIP.pdf ; https://media.api.sf.gov/documents/MUNI_parcel_tax_economic_impact_final.pdf
- SF rental-law guide and transfer-tax information: https://www.sf.gov/learn-about-san-francisco-rental-laws ; https://www.sf.gov/information--transfer-tax-reduction-union-labor-built-and-union-pension-fund-financed-housing
- Santa Clara County / San Francisco assessor portals; California DOI homeowners’ guide; HUD fair-market-rent dataset (explicitly flagged as not a local rent comparable); TreasuryDirect bill/reinvestment guidance; BLS historical CPI-U; NBER business-cycle chronology: https://www.sccassessor.org/ ; https://www.sfassessor.org/ ; https://www.insurance.ca.gov/01-consumers/105-type/95-guides/03-res/ ; https://www.huduser.gov/portal/datasets/fmr.html ; https://www.treasurydirect.gov/marketable-securities/reinvesting-a-marketable-security/ ; https://www.bls.gov/cpi/tables/supplemental-files/historical-cpi-u-202204.pdf ; https://www.nber.org/cycles/recessions_faq.html

### Work and verification performed
- Created grouped static dashboard pages: executive summary / decision readiness; pure and mixed choice comparison; property-value, assessed-value, tax, cost, rent and imputed-rent range worksheet; phased Treasury / equity stress test; one-page-target Attorney & CPA print/PDF brief; legal source table; deadlines timeline; question/answer/evidence register; suggestion approval register; flagged review page; glossary.
- Private model inputs are blank by default. Property model requires user-entered low/base/high appreciation, actual TRA rates, assessed base, operating-cost/lease evidence and separately selected Prop 19 / Prop H scenarios. No automatic “best path” is published because evidence is insufficient. The investment stress test uses explicit user inputs and labels its shaded range as a deterministic scenario envelope, not probabilities; it does not claim a historical 1929/2008 replay.
- California Proposition H update: official SF result page shows preliminary YES 74.42% as of Nov. 23; the result page explicitly says results remain preliminary until certified. Official ballot terms are linked and a conditional Property B parcel-tax scenario is implemented. Building area, SRO/shared area, indexation and pass-through eligibility remain private/unverified.
- Checked all static relative links with Python HTML parser; no broken local links. Checked table body rows for official source links. `node --check assets/app.js` passed. Ran synthetic-only Node smoke tests for both calculators; test figures were not written to repository/site. No real property forecast or CPA/legal validation was possible without private records.
- Added GitHub Actions Pages deployment workflow; local static server started successfully on port 4173. Actual GitHub Pages domain/deployment must be checked after merge; workflow execution depends on repository Pages settings and GitHub Actions permissions.

### Flagged items / irregularities
- No parcel/APN was searched or used; Property A Tax Rate Area and published rate remain unverified. Exact user-provided historic tables and property amounts were withheld for privacy. Insurance, market rent, utilities, capital costs, lease/unit legality, basis/depreciation, tax outcomes, debts and estate inventory are not verified.
- No date-of-death appraisal, full estate inventory, lifetime gifts, portability records, trust instrument, lease, tax return, insurance quote, or contractor plan is available. No single choice can be responsibly ranked; future 2040–2050 federal/state/local law and rates cannot be known today.
- The SF Prop H result is preliminary (not certified in the retrieved source as of the research cutoff); the site labels it accordingly and keeps the scenario conditional. Do not treat a proposal or preliminary count as final law.
- The task claim was committed and pushed immediately. Initial `git pull --rebase origin arena/3ba11c7d-tinodash2` failed because that remote branch did not exist yet; the new current branch was pushed successfully. Future pushes will first fetch/rebase the existing current branch.

### Coordination handoff / urgent privacy request (Nov. 25, 2026)
- While this task was in progress, `origin/main` advanced through merged PRs #1, #3 and #4. The main-branch coordination board shows core dashboard/subpages assigned to `arena/c059149b`; its integration task remains unclaimed. This session did not overwrite those files. Its PR #6 now conflicts with updated main and is a duplicate integration candidate, not safe to merge as-is.
- A read-only audit of current `origin/main` found public case-specific ZIP/postal identifiers, property estimates, rent, assessed-value histories, insurance estimates and derived projections in `README.md`, `COORDINATION.md`, `index.html`, `properties.html`, `properties` subpages, `briefing` pages, `taxes.html`, `questions.html`, `flagged.html`, `assets/model.js` and `js/model.js`. These details should be removed from all public pages/data/defaults and replaced by Property A/B labels, blank/unverified fields and client-entered private inputs. Do not repeat the values in issue text or screenshots. This is a high-priority request to the session that owns the main-branch dashboard/subpages and to the final integration owner; no edits were made to their files from this branch.
- The main-branch GitHub Pages deployment action reports success (run `45618100292`), but deployment success is not evidence that the content meets the user’s privacy requirement. Before a safe public release, rerun the privacy scan and confirm that exact property identifiers/amounts and derived personalized forecasts are absent.
- This branch’s independent static dashboard is privacy-sanitized but its PR conflicts with current main. It is not being merged over the already-deployed integration. The current branch retains the candidate code for review/possible scoped cherry-pick; final integration must coordinate and re-verify it.
