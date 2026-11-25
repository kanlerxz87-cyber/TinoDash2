# TinoDash2 coordination board

**Last updated:** 2026-11-25 (session `arena/349fb457-tinodash2`)
**Current branch:** `arena/349fb457-tinodash2` — Arena-assigned; do not rename; do not push elsewhere.

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
  redaction (2026-11, see “Exposure log”). History still contains them. PR #8 (this branch)
  repeated the mistake and was closed unmerged. A history purge requires **repository-owner
  action** (GitHub Support; cache/search-index removal; fork review) and is outside this
  session’s branch restrictions. **Do not claim history is scrubbed.**

## Status summary (2026-11-25)

| Item | Status | Notes |
|---|---|---|
| Legacy Pages serving `main` root | ✅ Live | `https://kanlerxz87-cyber.github.io/TinoDash2/`; `pages build and deployment` runs succeed |
| `Validate site` workflow | ✅ Fixed | Deploy job removed (legacy Pages cannot be deployed by `actions/deploy-pages`; run 45620071167 failed at “Deploy to GitHub Pages”) |
| PR #8 (figure-driven site) | ❌ Closed unmerged | Household figures in commits `993b85a`, `e0adbc6`; exposure remains via closed-PR refs; owner decision needed |
| Branch `arena/349fb457-tinodash2` | Reset to `origin/main` | Force-push (`--force-with-lease`) so the branch tip no longer serves the figures; closed-PR objects persist regardless |
| Black-swan page | ✅ Added (`black-swan.html`) | Cited public anchors only; zero household figures |
| Sources / Flagged additions | ✅ Done | Prop H (SFMTA), line-62 naming, 2027 indexing, SF transfer-tax flux, PR #8 exposure flag |
| Private analysis annex | ✅ Done | `private/ANALYSIS_ANNEX.md` — git-ignored |
| Full figure site rebuilt | ⛔ Blocked | Needs: (1) owner history-purge decision, (2) DOD appraisal, TRA/rate books, leases, insurance quotes, trust terms, adviser sign-off. Do not rebuild with figures on public `main`. |
| History purge (PRs #3/#4/#5/#8) | ⛔ **Owner action** | See Exposure log |

## Exposure log (verbatim, append-only)

1. **PRs #3/#4/#5 (before 2026-11-25):** household-provided estimates, ZIP-level property
   descriptions, rents and tax figures merged to public `main`. PR #5 redacted the working
   tree; prior commits retain the data. Recorded by earlier sessions.
2. **PR #8 (this session, 2026-11-25):** opened “Integration: anonymized inheritance decision
   desk” containing a complete figure-driven site (rounded to $10) in `docs/`. Not merged.
   Self-reviewed and **closed unmerged**; the branch was then force-reset to `origin/main`.
   Closed-PR ref still retains commits `993b85a` and `e0adbc6` until GitHub purges.
   **Owner must decide on history rewrite/purge including these commits and all caches.**
3. Nothing from the figure-driven site exists in the current working tree; quarantine wiped.

## Task board (current branch)

| Task | Status |
|---|---|
| Research official law (estate/gift, Prop 19, Form 540 line 62, SF Prop H, transfer taxes, Treasury, S&P/DJIA anchors) | done (2026-11-25) |
| Privacy-safe site: validation CI, black-swan anchors, sources, flags | done (this PR) |
| Private annex with full model | done (git-ignored) |
| Attorney/CPA one-pager, decision journal, 40-question register, suggestions board | done **inside annex only**; public equivalents are on `main` as browser-only/blank worksheets |
| Figure-driven dashboard rebuilt | blocked (needs purge decision + private inputs) |

## How future sessions work here

1. Read this file first. Claim scope in writing; keep edits minimal; `python3 scripts/check_site.py` before push.
2. `git pull --rebase` before every push; push only to `arena/349fb457-tinodash2`.
3. Never add household figures. When the owner has made the purge decision and private inputs
   exist, the figure-driven dashboard can return as a **private** deployment or stays local-only.
4. Flagged items (`FLAGGED_FOR_REVIEW.html`) are the post-review queue; they do not block merges.

## Source register

See `sources.md` (official links, annotated). Public legal anchors used on-site:
IRS ($15M 2026 exclusion; Form 706; §1014; Pub 523/544; §1031), CA BOE (Prop 19; Feb 2025–Feb 2027
allowance $1,044,586), CA FTB (Form 540 line 62), CA SCO (no CA estate tax), SFMTA (Prop H
Stronger Muni for All), Santa Clara County Assessor, US Treasury yields, officialdata.org
(S&P 500 1926→present), NBER, Federal Reserve History.

*Educational decision support only — not legal, tax or investment advice.*
