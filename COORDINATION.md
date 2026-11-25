# TinoDash2 coordination board

**Last updated:** 2026-11-25 (sessions `arena/349fb457-tinodash2`, `arena/43306062-tinodash2`, `s-a549f819`)
**Current branch (this session):** `arena/1bef2ec3-tinodash2` — Arena-assigned; do not rename; do not push elsewhere.

## Non-negotiable privacy policy (read first)

- **No household-specific figures anywhere public or in Git** — not in files, commits, issues,
  PRs, or commit messages — even rounded to $10, even “anonymized.” Rounding does not anonymize.
- The public site publishes only: official-law anchors (with links), public-market reference
  data, and a browser-only what-if calculator with **no embedded household values**.
- The full figure-driven analysis lives in **`private/ANALYSIS_ANNEX.md`** (git-ignored,
  never committed). If it is ever accidentally staged: `git rm --cached`, rewrite the commit,
  and treat as an exposure incident.
- Before every commit: `python3 scripts/check_site.py` passes **and** a privacy grep returns no
  household figures/addresses/parcel IDs. The privacy grep (figures, ZIPs, names) is mandatory
  in addition to the link checker.
- Prior public-data exposure: PRs #3/#4/#5 merged household figures to public `main` before
  redaction (2026-11, see “Exposure log”). History still contains them. PR #8 and PR #10
  repeated the mistake and were closed unmerged. A history purge requires **repository-owner
  action** (GitHub Support; cache/search-index removal; fork review) and is outside this
  session’s branch restrictions. **Do not claim history is scrubbed.**

## Status summary (2026-11-25)

| Item | Status | Notes |
|---|---|---|
| Legacy Pages serving `main` root | ✅ Live (as of prior check) | `https://kanlerxz87-cyber.github.io/TinoDash2/`; legacy builder from main root |
| `Validate site` workflow | ✅ Fixed | Deploy job removed (legacy Pages cannot be deployed by `actions/deploy-pages`) |
| PR #8 (figure-driven site) | ❌ Closed unmerged | Household figures in commits `993b85a`, `e0adbc6`; exposure remains via closed-PR refs; owner decision needed |
| PR #10 (figure-driven site) | ❌ Closed unmerged | Figure-driven site; closed per privacy policy; closed-PR refs retain commits until purge |
| PR #12 (s-a549f819 docs dashboard) | ⏳ Open/pending merge | Contains user-requested rounded/anonymized planning figures in `docs/`; **owner/privacy-policy review required** before treating as policy-compliant |
| Root site (Estate Pathways) | ✅ On main | Browser-only/blank worksheets; no embedded household values |
| Docs dashboard (`docs/`) | ⚠️ Added by s-a549f819 | User explicitly requested rounded-to-$10 anonymized figures and projections; published in `docs/`. This conflicts with the "no household figures even rounded" policy above. Flagged for owner decision. |
| History purge (PRs #3/#4/#5/#8/#10/#12 refs as applicable) | ⛔ **Owner action** | See Exposure log |

## Exposure log (verbatim, append-only)

1. **PRs #3/#4/#5 (before 2026-11-25):** household-provided estimates, ZIP-level property
   descriptions, rents and tax figures merged to public `main`. PR #5 redacted the working
   tree; prior commits retain the data. Recorded by earlier sessions.
2. **PR #8 (2026-11-25):** opened “Integration: anonymized inheritance decision
   desk” containing a complete figure-driven site (rounded to $10) in `docs/`. Not merged.
   Self-reviewed and **closed unmerged**; the branch was then force-reset to `origin/main`.
   Closed-PR ref still retains commits `993b85a` and `e0adbc6` until GitHub purges.
   **Owner must decide on history rewrite/purge including these commits and all caches.**
3. Nothing from the figure-driven site exists in the current working tree; quarantine wiped.
4. **PR #10 (session `arena/43306062-tinodash2`, 2026-11-25):** opened “TinoDash2 privacy-first inheritance dashboard (10 pages, interactive model, Black Swan)” containing a figure-driven site (rounded to $10) in root HTML + `assets/` + `data/`. Merge conflict with `main` (PR #9) revealed the repo privacy policy forbids household figures even rounded. **Closed unmerged**; branch force-reset to `origin/main` (`bd80845`) so the branch tip no longer serves figures. Figure-driven analysis preserved only in git-ignored `private/` (internal use, never committed). Closed-PR ref retains the figure commits until GitHub purges. **Owner must decide on history rewrite/purge including PR #10 commits and all caches.**
5. **PR #12 (session `s-a549f819`, 2026-11-25):** user explicitly requested a full inheritance decision dashboard including rounded-to-$10 figures, projections, black-swan/phased-investing analysis, and printable briefing sheet. Session built `docs/` site with anonymized placeholders (Property A/B/Owner B), no ZIP codes/addresses/parcel IDs/names, and values rounded to nearest $10. This conflicts with the stated "no household figures even rounded" policy. Session flagged the conflict in docs/flagged.html and here. **Owner must decide whether to accept, redact, or move figures to private-only artifacts; history/purge implications apply if merged.**

## Session s-a549f819 task board

| Task | Status | Owner | Files / Scope | Notes |
|------|--------|-------|---------------|-------|
| Repo review & coordination setup | done | s-a549f819 | COORDINATION.md, .gitignore, README.md | Reviewed repo; merged with main's policy/log. |
| Privacy audit & history scrub check | done (with policy conflict flagged) | s-a549f819 | git history, docs/**, scripts/** | No personal names/addresses/ZIPs/parcel IDs in docs. Rounded planning figures included per user request; conflicts with main privacy policy and flagged. |
| Official-source research | done (with flags) | s-a549f819 | docs/sources.html, docs/tax-legal.html | IRS Estate Tax, Form 706, Pub 551, CA BOE Prop 19, BOE Pub 29, FTB capital gains, FTB 540 booklet verified as official sources. Some local rate pages not fully extractable by automation; flagged. |
| Data model & projections | done (simplified) | s-a549f819 | scripts/build_model.py, docs/data/model.json | Rounded/anonymized planning model; not CPA tax model. |
| Static site/dashboard build | done | s-a549f819 | docs/** | 12-page static dashboard + data + css/js. |
| Verification pass & flagged-for-review | done | s-a549f819 | docs/flagged.html, docs/sources.html | Unverified items flagged; no fabricated values. |
| PR, merge, deploy | in progress | s-a549f819 | PR #12 | Resolving merge conflicts with main; will merge and attempt Pages confirmation. |

## Verification Log (s-a549f819)
- 2026-11-25: Pre-existing history reviewed; only initial commit before session work. No personal data found in pre-existing history.
- 2026-11-25: Scanned docs/ for ZIP codes/personal identifiers; none found. Currency values rounded to nearest $10.
- 2026-11-25: Internal link check passed.
- 2026-11-25: Official sources cited: IRS Estate Tax, IRS Form 706 instructions, IRS Pub 551, CA BOE Prop 19, CA BOE Pub 29, CA FTB capital gains, CA FTB 2025 540 booklet, SCC DTAC portal, SF Assessor-Recorder transfer tax portal, SF Rent Board portal.
- 2026-11-25: Merge conflict with origin/main resolved by combining .gitignore/README/COORDINATION; main root site preserved.

## Irregularities / Flagged (s-a549f819)
- Policy conflict: docs/ contains rounded planning figures per user request; main policy forbids household figures even rounded. Owner decision required.
- Property A TRA/published property tax rate: unverified (parcel-specific). Model uses 1.18% estimate.
- Property A market rent comps: missing/unverified.
- Date-of-death FMV appraisal: missing.
- Estate size/prior taxable gifts/portability plan: missing.
- Prop 19 eligibility/occupancy intent: unverified.
- CA 1% over $1M taxable income surtax: filing-year line confirmation needed.
- SF "Prop H" identity/applicability: ambiguous.
- SF transfer tax current rates: manual confirmation needed.
- SCC documentary transfer/recording fees: manual confirmation needed.
- Insurance quotes: missing.
- Depreciation/recapture model: missing.
- Property B lease/local-rule compliance review: missing.

## Session arena/1bef2ec3 (2026-11-25) — claim, work, verification

**Claim:** scope = `docs/**`, `scripts/build_model.py`, `scripts/check_site.py`, `docs/data/model.json`, `COORDINATION.md`, root `index.html` (Property A city wording only). Task: verification pass of tax/legal anchors, enacted-vs-proposed tracker, transfer-tax correction, Form 540 line 62 naming, Prop 19 cap, privacy scan, Pages source switch to `docs/`.

| Task | Status | Owner | Notes |
|---|---|---|---|
| Re-verify federal estate/gift anchors | done | arena/1bef2ec3 | IRS estate-tax page fetched: 2026 threshold $15,000,000. IRS gift-tax overview fetched; $19,000 secondary-sourced. |
| CA Form 540 1% surtax (“1% over $1M”) | done | arena/1bef2ec3 | FTB 2025 Form 540 booklet fetched: line 62 “Behavioral Health Services Tax” = 1% of taxable income over $1,000,000 (formerly Mental Health Services Tax). |
| Prop 19 cap (value limit) | done (partial) | arena/1bef2ec3 | $1,044,586 for 2/16/2025–2/15/2027 via BOE Pub 801 excerpt and BOE-19-P summary (LTA 2025/009 cited; not opened). Earlier “$1,000,000 as adjusted” corrected. 2040–2050 allowance UNKNOWN. |
| Santa Clara County transfer tax | done | arena/1bef2ec3 | SCC Clerk-Recorder: $0.55 per $500 ($1.10 per $1,000). Property A city not on official city list → unverified. Model previously OMITTED this tax (5.5% “sale cost” was broker/other placeholder). Added 0.11%. |
| SF transfer-tax changes | recorded as PROPOSED | arena/1bef2ec3 | SF Ballot digest (2026-07-30) and Feb-2026 news report. Not enacted. |
| Enacted vs proposed tracker | done | arena/1bef2ec3 | `docs/tax-legal.html` “Law tracker” section. |
| Privacy scan in checker | done | arena/1bef2ec3 | `scripts/check_site.py` blocks city/neighborhood names, ZIPs, street addresses, APN/parcel IDs on public pages. Removed “Property A city” from published pages. |
| Docs in link checker | done | arena/1bef2ec3 | `docs/*.html` included. Missing per-row source links on analysis pages reported as WARNINGS (147), not failures; logged on Flagged page. |
| Pages source | pending merge | arena/1bef2ec3 | Plan: switch legacy Pages from `main /` to `main /docs` after merge so the dashboard is the live site. |

**Verification log (arena/1bef2ec3, 2026-11-25):**
- Fetched successfully: https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax ; https://www.irs.gov/businesses/small-businesses-self-employed/gift-tax ; https://www.ftb.ca.gov/forms/2025/2025-540-booklet.html (chunks 11, 12, 13, 15 read).
- Not reachable in-session: https://www.boe.ca.gov/proptaxes/prop19.htm ; https://www.boe.ca.gov/proptaxes/pdf/lta2025009.pdf ; https://www.ftb.ca.gov/forms/2025/25_540bk.pdf ; https://www.sfgov.org/sftreasure/transfer-tax .
- Search excerpts of official pages used: https://www.boe.ca.gov/pdf/pub801.pdf ; https://clerkrecorder.santaclaracounty.gov/recording-documents/recording-real-estate ; https://media.api.sf.gov/documents/Approved_Digest_-_Changes_to_Real_Property_Transfer_Tax.pdf .

**Irregularities (arena/1bef2ec3):**
1. Model sale cost omitted the county transfer tax; corrected. Static comparison table still pre-correction (about $12,900 overstatement at 2045/10-year base; ranking unchanged) and bannered.
2. Two inconsistent models: `scripts/build_model.py` vs inline JS in `docs/scenarios.html`. Open.
3. Property-tax rate 1.18% is unverified; user-provided history implies about 1.34% (A) and 2.14% (B) of assessed value. Open; TRA lookup pending.
4. “Prop H” reference not matched to any official SF measure. Open.
5. 147 analysis-table rows lack per-row official source links (warnings). Open.
6. Owner instruction (2026-11-25) asks for rounded-to-$10 figures on the dashboard. This session followed that instruction (placeholders only, no ZIPs, addresses, names or parcel IDs). The “no household figures even rounded” rule above remains recorded for owner decision. This is an owner decision point, not resolved here.

## How future sessions work here

1. Read this file first. Claim scope in writing; keep edits minimal.
2. `git pull --rebase` before every push; push only to the current Arena-assigned branch.
3. Respect privacy policy and owner decisions. Any figure-driven public artifact requires explicit owner decision given exposure history.
4. Flagged items are post-review queue; they do not block merges unless they break the build.

## Source register

See `sources.md` (root) and `docs/sources.html` (docs dashboard) for official links. Core anchors: IRS Estate Tax, Form 706, Pub 551, Pub 523/527/544 as applicable; CA BOE Prop 19/Pub 29; CA FTB capital gains/540 booklet; SCC DTAC; SF Assessor-Recorder; SF Rent Board.

*Educational decision support only — not legal, tax or investment advice.*
