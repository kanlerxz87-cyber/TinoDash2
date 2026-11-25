# TinoDash2 — Inheritance Decision Workspace

Privacy-first planning materials for comparing inherited-home and existing-property paths.
The public site is the root **Estate Pathways** site (`index.html` and subpages), served by GitHub Pages from `main`.

## Privacy rules (binding — see COORDINATION.md)

- No household-specific figures in the public tree or Git, even rounded to $10. Rounding does not anonymize.
- Public outputs use placeholders only (Property A, Property B, Owner B).
- No names, street addresses, ZIP codes, parcel/APN IDs, account numbers, leases, or trust details.
- Household analysis lives only in `private/` (git-ignored, never committed or published).
- Prior exposure: household figures were merged to `main` in earlier PRs (#3/#4/#5 and the figure-bearing `docs/` dashboard from PR #12). Removing files from the tree does **not** remove them from Git history. A history purge requires repository-owner action. See the Exposure log in COORDINATION.md.

## What is in the public site

- `index.html` — executive summary, "what would change the answer", path comparison (pure and mixed), what-if calculator with blank inputs (browser-only, nothing stored), Prop 19 / estate / California checks, timeline, legislation watch, suggestions review queue, official sources, glossary.
- `flagged.html` / `FLAGGED_FOR_REVIEW.html` — unverified, irregular, or conflicting items with links for manual review.
- `sources.md` — official source register and the 2026-11-25 verification log.
- Subpages (`black-swan.html`, `briefing.html`, `glossary.html`, `questions.html`, `suggestions.html`, `verification.html`, and redirect stubs) — redirects or narrow pages into the sections above.

## Validation

- `python3 scripts/check_site.py` — required pages, local links, anchors, every table row has a link, no remote scripts.
- `node --check app.js`
- Privacy check before every commit: `git grep` for dollar figures, ZIP codes, parcel IDs and names must return nothing household-specific.

## Disclaimer

Planning and decision-organization aid only. Not legal, tax, investment, appraisal, or insurance advice.
