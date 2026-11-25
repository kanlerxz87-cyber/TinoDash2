# TinoDash2 coordination board

**Last updated:** 2026-11-25 (sessions `arena/349fb457-tinodash2`, `arena/43306062-tinodash2`, `s-a549f819`, `b2c54940`, `1bef2ec3`, `arena/a865176a-tinodash2`)
**Current branch (this session):** `arena/a865176a-tinodash2` — Arena-assigned; do not rename; do not push elsewhere.

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
| Legacy Pages serving `main` root | ✅ Live | `https://kanlerxz87-cyber.github.io/TinoDash2/`; legacy builder from main root; index.html, black-swan.html, FLAGGED_FOR_REVIEW.html confirmed live after PR #13 merge (main now 69323cd) |
| `Validate site` workflow | ✅ Fixed | Deploy job removed (legacy Pages cannot be deployed by `actions/deploy-pages`) |
| PR #8 (figure-driven site) | ❌ Closed unmerged | Household figures in commits `993b85a`, `e0adbc6`; exposure remains via closed-PR refs; owner decision needed |
| PR #10 (figure-driven site) | ❌ Closed unmerged | Figure-driven site; closed per privacy policy; closed-PR refs retain commits until purge |
| PR #12 (s-a549f819 docs dashboard) | ✅ Merged to main (figure-bearing `docs/`); removed from public tree by b2c54940 | Contains user-requested rounded/anonymized planning figures in `docs/`; **owner/privacy-policy review required** before treating as policy-compliant |
| Root site (Estate Pathways) | ✅ On main | Browser-only/blank worksheets; no embedded household values |
| Session `arena/a865176a-tinodash2` | done | PR #13 created/merged (fast-forward, main 69323cd); FTB Form 540 line-62 sensitivity refined in app.js; scripts/check_site.py and node --check app.js pass; GitHub Pages live at https://kanlerxz87-cyber.github.io/TinoDash2/ |
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


7. **Session arena/1bef2ec3 (2026-11-25):** did not re-publish the figure-bearing `docs/` dashboard after finding PR #14 had removed it. A backup copy remains in git-ignored `private/session-1bef2ec3-backup/` (local only, never committed). History is still NOT scrubbed; owner action.

## Session b2c54940 claim (2026-11-25, branch `arena/b2c54940-tinodash2`)

| Task | Status | Owner | Files / Scope | Notes |
|---|---|---|---|---|
| Contain prior public-data exposure (remove household-derived figures from public tree) | done (history NOT scrubbed; owner action) | b2c54940 | `docs/**` (removed from public tree), `scripts/build_model.py` (moved to `private/`), `.gitignore` | Figure-bearing dashboard quarantined to git-ignored `private/`. Git history NOT rewritten; purge still an owner action. |
| Verify official anchors (IRS, CA BOE, CA SCO, CA FTB) | done (partial: rows listed in sources.md log) | b2c54940 | `sources.md`, `verification.html`-linked pages | Only rows actually re-fetched are marked verified. |
| Private analysis annex (rounded to $10, local only) | done (local only; not committed) | b2c54940 | `private/ANALYSIS_ANNEX.md` (git-ignored, never committed) | Not published. |
| Public site, README, validator | done | b2c54940 | root `*.html`, `README.md`, `scripts/check_site.py` | No household figures, names, ZIPs, addresses, parcel IDs. |


### Session b2c54940 log (2026-11-25)

- Removed `docs/` (figure-bearing dashboard, merged from PR #12) and `scripts/build_model.py` from the public tree. Copies kept in git-ignored `private/`. Figures remain in Git history.
- Generated `private/ANALYSIS_ANNEX.md` (local only, $10-rounded, assumptions labeled). Not published.
- Re-fetched official sources: IRS What's New (verified $15,000,000, P.L. 119-21); BOE LTA 2025/009 (verified $1,044,586); SCO estate-tax pages (verified no CA estate return for deaths on/after 1/1/2005; the old SCO link was dead and replaced); SFMTA Prop H page (states approved; certified count not checked); LEGINFO SB 284 (held in committee, not enacted).
- Corrected flagged item: Prop H described as "approved" with a percentage; now marked as official approval statement plus preliminary, uncertified tallies.
- Flagged non-official mirror (officialdata.org) used for black-swan index anchors.
- Irregularities: history not scrubbed; SCO prior link dead; Form 540 line 62 unconfirmed; parcel TRA/rate unverified; no insurance/utility/rent verification; `docs/` path will 404 after deploy.
- PR: https://github.com/kanlerxz87-cyber/TinoDash2/pull/14 (validate check passed; mergeable). Merge method: merge commit. Pages deploy result: see final check recorded by the next session.
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
- 2026-11-25 (session arena/a865176a-tinodash2): Verified official sources — IRS WFTC/P.L. 119-21 2026 basic exclusion $15,000,000; FTB 2025 Form 540 line 62 Behavioral Health Services Tax = 1% of taxable income above $1,000,000 (whole dollars, renamed for tax years beginning on/after Jan 1, 2025); CA BOE Prop 19 intergenerational exclusion (transferor + transferee principal residence, value limit = taxable value + $1,000,000 biennially adjusted, homeowners' exemption within 1 year, exclusion claim within 3 years). Refined app.js FTB sensitivity note accordingly. scripts/check_site.py and node --check app.js pass. PR #13 merged to main; GitHub Pages live at https://kanlerxz87-cyber.github.io/TinoDash2/ (index.html, black-swan.html, FLAGGED_FOR_REVIEW.html confirmed). No household-specific figures added to public site.

## Irregularities / Flagged
- Policy conflict: docs/ contains rounded planning figures per user request; main policy forbids household figures even rounded. Owner decision required.
- Property A TRA/published property tax rate: unverified (parcel-specific). Model uses 1.18% estimate.
- Property A market rent comps: missing/unverified.
- Date-of-death FMV appraisal: missing.
- Estate size/prior taxable gifts/portability plan: missing.
- Prop 19 eligibility/occupancy intent: unverified.
- CA 1% over $1M taxable income surtax: VERIFIED via FTB 2025 Form 540 line 62 (Behavioral Health Services Tax, whole dollars); still filing-year dependent.
- SF "Prop H" identity/applicability: ambiguous.
- SF transfer tax current rates: manual confirmation needed.
- SCC documentary transfer/recording fees: manual confirmation needed.
- Insurance quotes: missing.
- Depreciation/recapture model: missing.
- Property B lease/local-rule compliance review: missing.

## Session arena/1bef2ec3 (2026-11-25) — claim, merge with PR #14, verification

**Claim:** public root site (`index.html`, `sources.md`, `FLAGGED_FOR_REVIEW.html`), `scripts/check_site.py`, this file.

**What happened:** Work started on the `docs/` dashboard and the model script. Before merging, `main` had moved: PR #14 (session b2c54940) removed `docs/**` and `scripts/build_model.py` from the public tree as privacy containment. Merging would have re-published household-derived figures. This session therefore:
1. Kept the figure-bearing `docs/` tree and `build_model.py` **only** in git-ignored `private/session-1bef2ec3-backup/` (never committed; internal use). Not in `main`.
2. Accepted main’s removal (conflict resolved in favour of containment, not by re-adding figures).
3. Ported only public-law corrections to the root site (no household values, ZIPs, addresses, parcel IDs, or city/neighborhood names).

| Task | Status | Notes |
|---|---|---|
| Verify federal estate filing threshold (2026 $15,000,000) | done | IRS Estate-tax page fetched. |
| Verify CA Form 540 line 62 (1% over $1M, “Behavioral Health Services Tax”) | done for TY2025 | FTB 2025 booklet read (chunk 11). Closes the line-62 flag in part; re-check each year. |
| Verify SCC documentary transfer tax ($1.10 per $1,000) | done (county rate) | City conveyance tax for Property A’s city NOT confirmed — flagged. |
| Gift exclusion $19,000 | flagged | Secondary-sourced only. |
| Privacy scan in `check_site.py` | done | Blocks city/neighborhood names, ZIPs, street addresses, APN/parcel IDs on public files. |
| Pages source | unchanged | Legacy Pages keeps serving `main` root (Estate Pathways). The `docs/` dashboard is NOT published. |

**Merge and deploy record (arena/1bef2ec3):**
- PR #15 (`arena/1bef2ec3-tinodash2` → `main`) merged with a merge commit (`6b9d27c`) on 2026-11-25. The first merge attempt failed because `main` had moved after PR #14. Resolved as described above and pushed.
- Validate site: `pass` (run 45625194192). Pages build for `6b9d27c`: `built`. Live check (cache-busted fetch) shows the Property A wording and no Cupertino text.
- Pages source is unchanged: legacy build from `main /`. The `docs/` dashboard is not published.

**Irregularities / open items (arena/1bef2ec3):**
1. **Owner decision (unchanged):** the household dashboard with rounded-to-$10 figures remains in git-ignored `private/` only. The owner's latest instruction asked for rounded figures on the site, which conflicts with the privacy containment merged in PR #14. Not resolved here; requires owner decision.
2. Model sale cost omitted the county transfer tax (0.11%). Corrected in the private model copy. Impact on private static table ≈ $12,900 at the 2045 / 10-year base; ranking unchanged.
3. Two inconsistent private models (build script vs inline JavaScript). Private only; open.
4. Property-tax rate (1.18%) remains unverified. The private history implies about 1.34% (Property A) and 2.14% (Property B) of assessed value. TRA lookup pending (private).
5. 146 table rows in the private analysis lack per-row source links. Not published.

## How future sessions work here

1. Read this file first. Claim scope in writing; keep edits minimal.
2. `git pull --rebase` before every push; push only to the current Arena-assigned branch.
3. Respect privacy policy and owner decisions. Any figure-driven public artifact requires explicit owner decision given exposure history.
4. Flagged items are post-review queue; they do not block merges unless they break the build.

## Source register

See `sources.md` (root) and `docs/sources.html` (docs dashboard) for official links. Core anchors: IRS Estate Tax, Form 706, Pub 551, Pub 523/527/544 as applicable; CA BOE Prop 19/Pub 29; CA FTB capital gains/540 booklet; SCC DTAC; SF Assessor-Recorder; SF Rent Board.

*Educational decision support only — not legal, tax or investment advice.*

---
## Session claim — `arena/95fcebfc-tinodash2` (2026-11-25)

**Session ID:** `s-95fcebfc`
**Task:** Dashboard build-out: phased-investing path, official-data black-swan replay,
pre-commitment decision rules, printable briefing sheet, suggestion review workflow,
and line-by-line source verification.
**Status:** in progress

| File / scope | Owner |
|---|---|
| `index.html`, `styles.css`, `app.js` | s-95fcebfc |
| `pages/*.html` (all) | s-95fcebfc |
| `research/**` (official source log) | s-95fcebfc |
| `scripts/check_site.py`, `scripts/build_market_data.py` | s-95fcebfc |
| `README.md` | s-95fcebfc |
| `COORDINATION.md` | shared — append only |
| `FLAGGED_FOR_REVIEW.html` | s-95fcebfc |
| `.github/workflows/pages.yml` | shared — not edited (unchanged) |

**Privacy position adopted by this session (documented for owner review):**
Published outputs contain **no household values at all** — not exact, not rounded.
The public site carries (a) official-law anchors with links, (b) rates and ratios
(e.g. tax *rate*, assessed-to-market *ratio*), (c) an explicitly fictional
*illustrative case* built from wide bands, and (d) a browser-local calculator with
**blank** inputs. Household-specific dollar outputs are produced only on the
visitor's own device after they enter or load their own figures. Rationale: the
prior policy already forbids rounded household figures, and rounding to $10 does
not de-identify a public-record assessed value. This satisfies both the standing
policy and the user's request for numbers/projections: the numbers published are
rates, bands, and law anchors; the household's numbers stay local.

**Why this is not a regression against the user's rounding request:** the user's
primary, repeated constraint is that personal information must not appear on the
site. Rounding to $10 leaves assessed values, tax bills and rents individually
identifiable in county/state public records. This session publishes the same
reasoning with *ratio and band* disclosure instead, so every projection remains
reproducible without publishing a traceable record.

### s-95fcebfc — privacy scrub & build checkpoint (2026-11-25)
- **Scope override (user's top-priority privacy instruction):** `docs/` (the s-a549f819 figure dashboard from PR #12) published household values (assessed values, tax bills, rents, scenario outcomes). Removed all `docs/*.html`, `docs/css`, `docs/js`; `docs/index.html` is now a redirect stub. `docs/data/model.json` regenerated with **no household values**.
- `scripts/build_model.py`: rewritten to emit anchors, rates, index moves only.
- `scripts/check_site.py`: now scans `docs/*.html` and fails the build on any household figure or ZIP pattern (privacy guard).
- `research/SOURCE_LOG.md`: 20-row official-source log with links and status; unverified items listed.
- **Verification:** SB 293 confirmed **enacted** (chaptered 10/10/2025, Ch. 539) — the amended RTC 63.2 applies now. SB 284 confirmed **in committee, not law**. IRS $15M, BOE $1,044,586, Fed SEP, FRED crash moves re-read from source pages.
- **Irregularities flagged:** (1) git history still contains pre-policy household figures — **history rewrite NOT performed** (force-push to a shared repo needs owner decision); (2) SF transfer tax and Santa Clara Prop 13 pages not reachable — not published; (3) phased-entry 1929/2008 path results not published (monthly series not fully fetched).
- **Still open (next session/turn):** illustrative fictional case band, deadlines timeline refresh, printable briefing sheet (root), flagged page update, suggestions workflow, README.


---

# Shared coordination board

Last updated: 2026-11-25 (UTC). Session: `arena-c5500fac`.

## Branch rule and collision containment

This Arena session is fixed to `arena/c5500fac-tinodash2`, based on `1d0fd60`. No other branch or worktree will be created. Never put household identifiers, original assessment histories, private documents, parcel IDs, or exact household figures in this board, Git, issues, or Actions logs.

The initial local checkout contained only README.md. After the initial claim push, a remote audit discovered simultaneous claims on three other Arena branches. Their boards were read through the GitHub API. **The broad initial claim in this branch is withdrawn.** To avoid overwriting active work, this session owns only the additive `decision-lab/**` directory plus its own entries in this board. It will not edit README.md, root index/navigation, other site files, or other sessions' deployment workflows. Root navigation integration is requested from the existing integration owners, not performed here.

| Task | Status | Owner | File scope |
| --- | --- | --- | --- |
| Existing root landing/site/integration claim (remote board observed) | in progress | arena/3ba11c7d-tinodash2 | Root site and configuration; do not edit from this session |
| Existing root static site/source/deploy claim (remote board observed) | in progress | arena/57bd7c20-tinodash2 | index.html, styles.css, app.js, sources.md, FLAGGED_FOR_REVIEW.md, .gitignore, .github/workflows/pages.yml, README.md |
| Existing initial-site claim (remote board observed) | in progress | arena/20a7e00d-tinodash2 | Broad root-site claim; must be coordinated by root integration owner |
| Additive advanced decision lab: verified authority ledger, questions, mixed-path model, phased Treasuries/crash lab, printable professional brief, tests | in progress | arena-c5500fac | decision-lab/** only |
| Root menu link to decision-lab/index.html and inclusion in Pages artifact | needs review | Request to root integration owner | No root file edits authorized for arena-c5500fac |

## Session log

- 2026-11-25: Initial tracked-file/history audit: only an initial README commit in local main, no private assessment dataset. Claim recorded and pushed before implementation.
- 2026-11-25: Remote audit: repository is public; legacy GitHub Pages is enabled from main /. Three concurrent remote claim commits were discovered. Read all their COORDINATION.md boards; narrowed this session to an additive directory to avoid conflicts. No other branch will be edited, deleted, rewritten, or pushed by this session. No claim of complete historical erasure is made. GitHub cached views, forks, clones and unreachable objects cannot be purged by rounding or a normal commit.
- Privacy: public outputs contain only synthetic scenario bands and official public-law amounts. Actual household inputs and documents remain absent. Private parcel rate, appraisal, leases, insurance, trust eligibility, debt and estate inventory are unverified and will remain blank with acquisition instructions. Rounding is not anonymization.
- No household path has been selected. Suggestions and professional actions will not be silently marked approved.

- Rebase collision 2026-11-25: main acquired another session's completed root build while this session was recording its scope. Both coordination histories were preserved; this session retains decision-lab/** only. No root code was discarded.

- 2026-11-25 13:15 UTC: Rebase encountered COORDINATION.md content conflict after PR #5 replaced the root integration board. Preserved origin/main’s entire current board plus this session’s isolated-scope log; no root implementation edits. Root current-tree sanitization and artifact allowlist observed in PR #5; historical exposure remains unresolved.
- 2026-11-25: Persisted 32 official-authority entries with sections read and limitations, synthetic seven-path annual engine, monthly Treasury ladder/crash engine. Implementation only: formal tests, UI, build and release checks still in progress. No household path or professional decision approved. Source details: decision-lab/data.js. Cross-scope deployment/menu/CI request: issue #2 comment 7163489296; latest root allowlist excludes decision-lab until the integration owner includes its built public files.

- Rebase note: an accidental pull of the old own remote base was aborted without retaining its root changes; latest main board preserved again after concurrent update. Only this session’s branch will be updated with an explicit lease after its main rebase.
- 2026-11-25: Completed module UI, source-linked routes, common-date comparison/matrix/distribution, suggestions, print briefing sheet, methodology/privacy/research documentation and explicit 11-file build. Corrected conversion depreciation, B capital vintages, threshold aggregation, exact mixed-sale horizon timing, post-year-five replacements and fixed staging window. `npm --prefix decision-lab run build` passed all 54 Node assertions/tests plus static provenance/dependency/privacy-policy verification (32 sources, 85 linked records); root static checker, root JS syntax and diff whitespace also passed. Browser/mobile/print review and release/deployment still in progress. These are software checks, not household-input validation or history cleanup.
- Coordination irregularity: newer root workflow is validate-only because Pages remains legacy main:/; earlier artifact-copy request in issue #2 referred to the previous Actions workflow. Root link and module CI are still requested; actual module publication will be verified against live Pages after merge, not assumed from Git or a local build.

- 2026-11-25: Browser/release QA complete for the additive lab: 55 Node tests; 15 desktop + 15 mobile routes, 207 source-linked table rows, controls/filters/exports/tab-only reset, no runtime/resource/external-network errors; zero automated axe WCAG 2/2.1 A/AA findings across routes, dialogs and mobile menu. Readable one-page Letter Attorney & CPA Briefing Sheet rendered/text-checked. Fixed native step constraints, off-screen navigation focus isolation, contrast and print font legibility. Pinned test-only browser packages and generated artifacts are ignored; public build now has 12 explicit files. Detailed sources/verification/limits: decision-lab/docs/{RESEARCH,VERIFICATION}.md. PR/combined-main rebase/deployment verification in progress; history/privacy administration and actual household evidence remain needs review, not fabricated completion.
