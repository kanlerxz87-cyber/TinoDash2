# TinoDash2 — Inheritance Decision Dashboard

A figure-driven, privacy-first dashboard for deciding what to do with an inherited home
(**Property A**, expected by trust 2040–2050) while already owning a multi-unit home
(**Property B**). Published on GitHub Pages from the repo root.

**Live site:** https://kanlerxz87-cyber.github.io/TinoDash2/

## Pages (grouped menu on every page)

| Area | Page | Contents |
|---|---|---|
| Decision desk | `index.html` | Executive summary, first-screen "what would change the answer", decision log |
| | `comparison.html` | All pure + mixed paths at identical transfer dates/horizons (taxes, debt, occupancy, capital costs, liquidity) |
| | `projections.html` | Year-by-year projections, distribution chart, browser-side what-if controls, tornado sensitivity, rebuild protocol |
| | `black-swan.html` | Separate black-swan section: 1929/2008-style crash-entry tests, phased investing (3M–2Y Treasuries, 24–36 months), reinvestment risk beside every headline |
| Property data | `properties.html` | Values, rounded assessment/tax histories, operating costs, solar credits, Prop H terms, five-year capital plans |
| Taxes & law | `taxes.html` | Estate tax vs income-tax basis vs property-tax assessment kept separate; enacted vs proposals; transfer taxes & recording fees priced into the sell path |
| | `timeline.html` | Step-by-step inheritance process with hard deadlines (Form 706, Prop 19 windows, Prop H applications) |
| Governance | `questions.html` | Question/information/answer list with discovery suggestions; unknowns left blank |
| | `suggestions.html` | Review queue — owner chooses before anything is implemented |
| | `briefing.html` | One-page printable Attorney & CPA Briefing Sheet (print button) |
| Reference | `glossary.html` · `sources.html` · `flagged.html` | Grouped glossary & methodology; official source register with verification dates; flagged-for-review queue |

## Model pipeline

- `python3 scripts/build_model.py` → writes `data/model.json` + `data/model.js` (rounded to $10, deterministic).
- `app.js` loads `data/model.js` and re-runs the path math in the browser for what-if controls.
- After **any** input change: rebuild, re-run `python3 scripts/check_site.py`, re-run the privacy grep,
  and record whether the recommendation moved (see `projections.html#rebuild` and COORDINATION.md).

## Privacy rules (see COORDINATION.md for the full record)

- Placeholders only: **Property A, Property B, Owner B**. No names, street addresses, ZIP codes,
  parcel/APN IDs, account numbers, or trust identifiers anywhere public.
- Currency rounded to the nearest $10 (owner instruction). Values already divisible by $10 are
  additionally jittered +$10 so no displayed value exactly matches a public record.
- Full-precision household figures live only in git-ignored `private/` (internal use, never committed).
- Prior exposure: household figures were merged to `main` in early PRs (#3/#4/#5) and exist in closed-PR
  refs (#8/#10/#12). Main's reachable history is verified clean (2026-11-25 sweep), but a true purge
  (caches, closed-PR refs, forks) requires repository-owner action. Do not claim history is scrubbed.

## Validation

- `python3 scripts/check_site.py` — required pages, local links/anchors, every table row carries a
  source link, no remote scripts or styles (nothing leaks visitor metadata).
- `node --check app.js` (CI).
- Privacy grep before every commit: ZIPs and exact unrounded owner values must return nothing.

## Disclaimer

Planning and decision-organization aid only. Not legal, tax, investment, insurance, or appraisal
advice. 2026 anchors reflect law as published by their official sources on 2026-11-25; a 2040–2050
transfer will be governed by the law in force at that date.
