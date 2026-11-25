# TinoDash2 — Inheritance Decision Dashboard (Privacy-First)

Decision-support site for: **live in / rent / sell + reinvest** the inherited Cupertino house (Property A, 95014, via trust ~2040–2050), given the already-owned San Francisco house (Property B, 94122).

- **Privacy:** placeholders only (Property A / Property B / Heir / Decedent). No names, addresses, APNs, or account numbers. All dollars rounded to nearest $10.
- **Ranges, not points:** every path shows low/base/high. Mixed paths included. Black-swan stress tests + phased Treasury investing path (24–36 mo) with reinvestment risk shown beside headlines.
- **Verified:** every factual row on `verification.html` links to an official source (IRS, CA BOE, FTB, CA AG, SF Rent Board, U.S. Treasury) or is flagged blank. Unverified/irregular items on `flagged.html`.
- **What-if controls** on the dashboard rebuild the model live. Distribution chart + cumulative-cash chart included.
- **Printable** Attorney & CPA Briefing Sheet (`briefing.html`).

## Pages
`index.html` (dashboard + what-would-change-the-answer) · `properties.html` · `projections.html` (50-yr) · `paths.html` · `black-swan.html` · `taxes.html` (estate/basis/property-tax separated, deadlines timeline, enacted vs. proposed) · `verification.html` · `questions.html` (blocking Q&A + pre-agreement) · `suggestions.html` (choose-best-path) · `briefing.html` · `flagged.html` · `glossary.html`

## Model
`assets/model.js` — transparent year-by-year engine. Official rules (Prop 13 2% cap, Prop 19 cap, $15M exemption, 1% MHST) are parameters; forecasts are labeled assumptions with sensitivities. `assets/app.js` — UI, charts, what-if binding, suggestions voting (localStorage only).

## Deploy
GitHub Pages from root (`.github/workflows/pages.yml`). See `COORDINATION.md` for task board, sources, and handoff log.

> Not tax/legal advice. Confirm with attorney + CPA before acting. Re-run annually with updated inputs.
