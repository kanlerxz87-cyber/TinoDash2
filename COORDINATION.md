# TinoDash2 coordination board

**Last reviewed:** 2026-11-26 UTC
**Current Arena session/branch:** `arena/83202936-tinodash2` (fixed assignment; all work remains on this branch).
**Current phase:** privacy-first integration and verification.

## Privacy policy — applies to the public website and repository

- Do not publish personal identifiers, address/ZIP/parcel details, household-specific property values, assessments, rents, costs, lease details, or household-derived projections—even rounded or replaced with labels.
- Property A / Property B are generic labels only. Public pages may include law and public-market values when relevant, source-linked, and clearly distinguished from household facts.
- What-if forms start blank. Browser calculations must not use network requests, analytics, or persistent storage. No household values are embedded in HTML, JS, JSON, CSS, Markdown, generators, examples, or test fixtures.
- Personal working calculations, if any, belong only in ignored `private/` artifacts. Never stage or commit that directory.
- Before every commit/push: run `python3 scripts/check_site.py`, `python3 scripts/privacy_check.py --selftest`, relevant JavaScript checks, and review the diff for new identifiers or household-derived values.
- History is **not** scrubbed. Previous commits, merged PR refs, closed PR refs, caches, search indexes, forks, and clones may still retain earlier exposures. Ordinary PR deletion/redaction cannot purge those objects. This session will remove sensitive material from the current working tree and document the remaining owner-level purge steps; it will not rewrite or force-push `main` or other branches.

## Task board — current session

| Task | Status | Owner | Files / scope | Verification / notes |
|---|---|---|---|---|
| Reconcile privacy policy and clear stale merge-conflict markers in this board | in progress | `arena/83202936-tinodash2` | `COORDINATION.md` | Claim committed before implementation; no household values in the claim. |
| Remove household-derived data from every current website route and generated asset | in progress | `arena/83202936-tinodash2` | root pages, `companion/**`, `docs/**`, `data/**`, relevant generators | Preserve a useful, source-linked, blank-input decision workspace; do not publish private values. |
| Harden privacy checks and link/build validation | in progress | `arena/83202936-tinodash2` | `scripts/check_site.py`, `scripts/privacy_check.py`, tests/workflow if needed | Scan served content and repository text/assets; test blank defaults and no persistence/network. |
| Re-verify current legal/public-data anchors and label unknowns/proposals | in progress | `arena/83202936-tinodash2` | `sources.md`, `research/**`, safe public pages | Mark only claims verified against official sources as verified; record source, date, scope and limits. |
| Keep the questions, suggestions and printable adviser brief reviewable and private | in progress | `arena/83202936-tinodash2` | safe public pages and navigation | One-page print layout; no household information. |
| Report prior exposure and history-purge limitations | in progress | `arena/83202936-tinodash2` | this board, `research/HISTORY_PURGE_RUNBOOK.md`, flagged page | No claim that history is scrubbed; list maintainer actions without repeating exposed values. |

## Prior-exposure status

Earlier versions of the repository and Git objects contained household-derived information. The current branch must not republish it. Reachable history, PR references, and external caches have not been fully purged or independently certified clean. Complete purge requires owner/maintainer action, including reviewing GitHub support options, search caches, forks, and clones. See `research/HISTORY_PURGE_RUNBOOK.md` and the public Flagged for Review page. Do not include household values or identifiers in this log.

## Source and verification anchors

| Area | Official reference | What it can establish | Limitation |
|---|---|---|---|
| Federal estate and gift tax | [IRS estate and gift tax updates](https://www.irs.gov/businesses/small-businesses-self-employed/whats-new-estate-and-gift-tax) | Current published federal exclusion and year-specific rules | Future law in a later transfer year is unknown; recheck then. |
| Federal estate return | [IRS Form 706 instructions](https://www.irs.gov/instructions/i706) | Filing, portability, election and deadline rules | Use the edition for the year of death; counsel must assess facts. |
| California property-tax inheritance rules | [California BOE Proposition 19](https://www.boe.ca.gov/prop19/) · [Revenue and Taxation Code §63.2](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=63.2) | Current statutory eligibility and claim framework | Parcel-specific eligibility, value and assessment require assessor/adviser confirmation. |
| California income-tax rules | [FTB forms and instructions](https://www.ftb.ca.gov/forms/) | Year-specific California filing instructions | The transfer-year form and taxpayer facts control. |
| Estate basis and rental depreciation | [IRS Publication 551](https://www.irs.gov/publications/p551) · [IRS Publication 527](https://www.irs.gov/publications/p527) | Basis and residential-rental depreciation framework | Obtain a date-of-death appraisal and CPA schedules; no household basis is published. |
| Federal residence-sale exclusion | [IRS Publication 523](https://www.irs.gov/publications/p523) | Current principal-residence exclusion framework | Eligibility depends on facts and current law. |
| Treasury rates | [U.S. Treasury daily interest-rate data](https://home.treasury.gov/resource-center/data-chart-center/interest-rates) | Dated published Treasury yields | Past rates do not forecast future reinvestment yields. |
| Historical market data | [Robert Shiller data portal](https://www.econ.yale.edu/~shiller/data.htm) · [FRED](https://fred.stlouisfed.org/) | Public historical series for stress testing | A replay is not a forecast or guaranteed sequence; cite exact series/method. |
| California estate-tax framework | [California State Controller](https://www.sco.ca.gov/ardtax_estate_tax.html) | Current state estate-tax reporting framework | Recheck for the actual transfer year. |

## Prior-session work preserved during integration

- **Session `arena/3d344315-tinodash2` (2026-11-26; PR #36, commit `59be3b0`):** removed stale conflict markers from the previous board, rechecked official federal/California anchors, clarified the California Form 540 line-62 surcharge as an income-tax item rather than an inheritance tax, and rebuilt the generated model. Its source re-check is retained in the source register; personalized generated output is being removed from public routes under the current privacy-first requirement.
- **Session `arena/d7cf2428-tinodash2` (2026-11-26; PR #35):** addressed a static validation warning in a preserved companion page. That page is included in this session's full privacy audit; no household-derived aggregate will be retained in the public tree.
- Earlier sessions built the privacy-safe calculator framework, adviser brief, questions/suggestions queues, source list, timeline, and crash replay. Those deliverables are being reviewed and retained only where they meet the current privacy and source-verification rules.

## Release checklist

- [ ] Current public tree contains no household-specific inputs or derived projections.
- [ ] Every factual table row links to an official source or is explicitly blank/unverified.
- [ ] Enacted laws and proposals are distinguished.
- [ ] Local links/anchors resolve; adviser brief print layout stays to one page.
- [ ] Blank-input browser model has no network, analytics, or storage APIs.
- [ ] `python3 scripts/check_site.py` passes.
- [ ] `python3 scripts/privacy_check.py --selftest` passes.
- [ ] JavaScript syntax and calculator tests pass.
- [ ] Git diff, staged files, commit message, and public tree contain no household identifiers or values.
- [ ] Run `git pull --rebase` immediately before pushing only this branch.
- [ ] Record PR/check/Pages status and remaining history-purge limitations here.
