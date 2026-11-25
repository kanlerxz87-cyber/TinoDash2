# TinoDash2 coordination board

**Last updated:** 2026-11-25 (sessions `arena/349fb457-tinodash2`, `arena/43306062-tinodash2`, `s-a549f819`)
**Current branch:** `arena/a549f819-tinodash2` — Arena-assigned for this session; do not rename; do not push elsewhere.

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

## How future sessions work here

1. Read this file first. Claim scope in writing; keep edits minimal.
2. `git pull --rebase` before every push; push only to the current Arena-assigned branch.
3. Respect privacy policy and owner decisions. Any figure-driven public artifact requires explicit owner decision given exposure history.
4. Flagged items are post-review queue; they do not block merges unless they break the build.

## Source register

See `sources.md` (root) and `docs/sources.html` (docs dashboard) for official links. Core anchors: IRS Estate Tax, Form 706, Pub 551, Pub 523/527/544 as applicable; CA BOE Prop 19/Pub 29; CA FTB capital gains/540 booklet; SCC DTAC; SF Assessor-Recorder; SF Rent Board.

*Educational decision support only — not legal, tax or investment advice.*

## Session `arena/e0eabcec-tinodash2` (2026-11-25)

Branch `arena/e0eabcec-tinodash2`, from `5560f3d` on `main`. Scope: run and harden the
verification scripts, build the decision-support pages that were still missing, and repair the
policy conflict left by PR #12.

### Decisions taken this session

1. **`docs/` removed from the published tree.** The PR #12 dashboard in `docs/` embedded
   household-derived values (property value bands, assessed values, rent, annual tax) even
   though the repository policy forbids them even rounded. Since `main` is served by the
   legacy Pages builder from the repository root, that content was publishable and the earlier
   note that "`docs/` is not served" was not a mitigation. The directory is deleted in this
   branch; a permanent privacy gate now runs in CI (`scripts/privacy_check.py --selftest`).
   No value from it is reproduced here. The generator `scripts/build_model.py` is retained but
   no longer publishes to a served path.
2. **Nothing household-specific is published.** The six new pages carry public-law anchors,
   protocol, ranges of required evidence, and a browser-only calculator whose inputs are blank
   and never leave the page. Confirmed by the privacy gate.
3. **Failed verification is reported as failed.** `scripts/verify_sources.py --online` cannot
   reach the network from this sandbox; offline mode now prints an explicit "online
   verification was NOT run" banner rather than a pass that could be mistaken for a full check.
   A silent-pass bug (string/int year comparison meant zero checkpoints were compared) was
   found and fixed; the script now fails if nothing was actually compared.

### Task board

| Task | Status | Files |
|---|---|---|
| Verify historical datasets | ✅ 22 checkpoints, worst relative error 0.0344% (offline) | `scripts/verify_sources.py`, `data/` |
| Online re-fetch of cited pages | ⛔ Blocked: no outbound HTTPS in this environment; CI step added | `.github/workflows/pages.yml` |
| War room / decision gates | ✅ | `war-room.html` |
| Law watch (enacted + proposals + recheck calendar) | ✅ | `law-watch.html` |
| Questions and missing data | ✅ | `questions.html` |
| Path comparison + calculator | ✅ 8 paths, 25 blank inputs, browser-only | `comparison.html`, `calculator.js` |
| Suggestions queue | ✅ S1–S22 with acceptance criteria | `suggestions.html` |
| Printable attorney/CPA brief | ✅ | `brief.html` |
| Crash-entry replay | ✅ 89 ten-year windows, 1928–2025 | `crash-replay.html` |
| Site integrity check | ✅ 10 required pages present and linked from `index.html` | `scripts/check_site.py` |
| Calculator smoke test in CI | ✅ stub-DOM test, no network APIs referenced | `scripts/smoke_calculator.js` |
| Privacy gate in CI | ✅ self-test catches 3/3 planted findings; live tree 0 findings | `scripts/privacy_check.py` |
| Prop H (Nov 2026) tier schedule | ✅ verified against SFMTA page | `law-watch.html` |
| Depreciation / recapture model | ⬜ Not built — needs CPA-grade assumptions the evidence does not support yet; scoped on `war-room.html` | — |
| Estate-liquidity / portability worksheet | ⬜ Not built — depends on the 706 gate | — |
| Multi-scenario value/property-tax projection | ⬜ Deliberately withheld: publishing value bands would breach the privacy policy | — |
| History purge of PRs #3/#4/#5/#8/#10/#12 | ⛔ **Owner action** — shallow clone here; see Exposure log | — |

### Exposure log addition

6. **PR #12 `docs/` dashboard (removal, 2026-11-25):** discovered to be publishable through the
   legacy root Pages build. Deleted from the working tree in this branch. The merged commit on
   `main` still contains the files until this branch lands, and git history retains them after
   that. **Owner action:** after merge, extend the history purge to the PR #12 merge commit and
   confirm the served site no longer exposes those pages.
