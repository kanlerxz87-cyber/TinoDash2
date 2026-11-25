# TinoDash2 — Inheritance Decision Workspace

This repository contains privacy-first planning materials for comparing inherited-home and existing-property paths. It currently includes two static site surfaces:

1. **Root site (Estate Pathways)** — plain HTML/CSS/JS at repo root, served by legacy GitHub Pages from `main` root. Browser-only what-if tools; no embedded household values.
2. **Docs dashboard (`docs/`)** — static dashboard added in session `s-a549f819` with executive summary, decision criteria, timelines, scenarios, black-swan/phased-investing analysis, tax/legal map, questions, printable attorney/CPA briefing sheet, sources, and flagged-for-review pages. Values displayed are anonymized placeholders and rounded to nearest $10 per user request; see privacy notes below.

## Privacy

- Public outputs should use placeholders only (Property A, Property B, Owner B).
- No names, street addresses, ZIP codes, parcel/APN IDs, account numbers, or exact traceable public-record values should be published.
- Sensitive details discovered during research are for internal use only.
- `private/` and other ignored private paths are guardrails, not security boundaries; check staged files before every commit.
- Prior public-data exposure exists in repository history/closed PR refs (see `COORDINATION.md` Exposure log). Do not claim history is scrubbed.

## Docs dashboard (s-a549f819)

- Landing page: `docs/index.html`
- Model build: `python3 scripts/build_model.py` -> `docs/data/model.json`
- Verification: `docs/sources.html`, `docs/flagged.html`

## Root site

- Open `index.html` in a modern browser for the root Estate Pathways site.
- Validation: `python3 scripts/check_site.py` (if present on branch).

## GitHub Pages

Legacy Pages currently serves `main` root. If the `docs/` dashboard should be published, configure Pages source accordingly or integrate into the root site; confirm with repository owner.

## Disclaimer

Planning and decision-organization aid only. Not legal, tax, investment, appraisal, or insurance advice.
