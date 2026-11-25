# COORDINATION

Shared task board for parallel agent sessions. Update this file before starting work, commit and push claims immediately.

## Session
- Session ID: `s-a549f819`
- Branch: `arena/a549f819-tinodash2`
- Started: 2026-11-25
- Status: complete (pending PR/merge/deploy)

## Tasks

| Task | Status | Owner | Files / Scope | Notes |
|------|--------|-------|---------------|-------|
| Repo review & coordination setup | done | s-a549f819 | COORDINATION.md, .gitignore, README.md | Reviewed repo; only initial commit present. |
| Privacy audit & history scrub check | done | s-a549f819 | git history, docs/**, scripts/** | No personal data in pre-existing history. Public outputs anonymized; values rounded to nearest $10; no ZIP codes/addresses/parcel IDs/names published. |
| Official-source research (federal/state/local) | done (with flags) | s-a549f819 | docs/sources.html, docs/tax-legal.html | Verified IRS estate tax, IRS Pub 551, CA BOE Prop 19, BOE Pub 29, FTB capital gains, FTB 540 booklet. Some local rate pages could not be fully extracted by automated fetch; official links provided and flagged. |
| Data model & projections | done (simplified) | s-a549f819 | scripts/build_model.py, docs/data/model.json, docs/scenarios.html, docs/black-swan.html | Anonymized rounded model. Includes pure/mixed paths, black-swan analogs, phased Treasury-to-stock path, what-if controls. Not CPA tax model. |
| Static site/dashboard build | done | s-a549f819 | docs/** | GitHub Pages-ready static site in docs/ with .nojekyll. Includes executive summary, decision criteria, timeline, properties, scenarios, black swan, tax/legal, questions, briefing, suggestions, glossary, sources, flagged pages. |
| Verification pass & flagged-for-review page | done | s-a549f819 | docs/flagged.html, docs/sources.html, COORDINATION.md | Unverified/missing items explicitly flagged; no fabricated values filled in. |
| PR, merge, deploy | in progress | s-a549f819 | PR/Pages | Will create PR from arena/a549f819-tinodash2 to main, merge, and confirm Pages deployment. |

## Handoff / Requests
- None.

## Verification Log
- 2026-11-25: `git log --all -p` reviewed; only initial commit `1d0fd60` before session work. No personal data found.
- 2026-11-25: Scanned docs/ for ZIP codes/personal identifiers; none found. User-supplied historical values rounded to nearest $10 before display.
- 2026-11-25: Internal link check passed (`python3` scan over docs/*.html href/src).
- 2026-11-25: Official sources cited: IRS Estate Tax, IRS Form 706 instructions, IRS Pub 551, CA BOE Prop 19, CA BOE Pub 29, CA FTB capital gains, CA FTB 2025 Form 540 booklet, SCC DTAC portal, SF Assessor-Recorder transfer tax portal, SF Rent Board portal.
- 2026-11-25: Automated fetch limitations prevented full extraction of some official local pages (SF transfer tax table, SCC documentary transfer/recording fee schedule, exact 540 line naming for filing year). Items flagged; no values fabricated.

## Irregularities / Flagged
- Property A TRA/published property tax rate: unverified (parcel-specific; privacy). Model uses 1.18% estimate.
- Property A market rent comps: missing/unverified; rent path is planning floor only.
- Date-of-death FMV appraisal: missing.
- Estate size/prior taxable gifts/portability plan: missing.
- Prop 19 eligibility/occupancy intent: unverified.
- CA 1% over $1M taxable income surtax: general rule cited from official FTB sources; filing-year line confirmation needed.
- SF "Prop H" identity/applicability: ambiguous; flagged.
- SF transfer tax current rates: official link provided; manual confirmation needed.
- SCC documentary transfer/recording fees: official portal linked; manual confirmation needed.
- Insurance quotes: missing.
- Depreciation/recapture model: missing; CPA required.
- Property B lease/local-rule compliance review: missing.

## PR / Deploy
- PR: pending
- Merge: pending
- GitHub Pages: pending (configure main /docs)
