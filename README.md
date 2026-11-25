# TinoDash2 — Privacy-First Inheritance Decision Dashboard

Cupertino Property A (95014, trust ~2040–2050) vs San Francisco Property B (94122, already owned) — live GitHub Pages dashboard comparing 6 pure & mixed paths at identical transfer dates/horizons.

**Live site:** https://kanlerxz87-cyber.github.io/TinoDash2/

## Pages

- `index.html` — Dashboard: "What Would Change the Answer" first screen, headline + reinvestment risk, interactive What-If controls, 6-path ranking, verified $10-rounded historical tables
- `projections.html` — Multi-horizon ranges, 10th–90th percentile fan, same-year vs §121 vs depreciation/§1250/§1031, year-by-year 2026–2076
- `black-swan.html` — 1929, 1973, 2000, 2008, M7.0 quake + 24–36m 3M–2Y Treasury phased-investing simulator
- `tax-legal.html` — Estate tax ($15M OBBBA) vs basis (IRC §1014, CA 13.3%) vs assessment (Prop 13/19), SCC/SF local rules, enacted vs proposed
- `operations-capital.html` — 95014 comps vs HUD SAFMR, water/solar/insurance, 5-year capital plans
- `timeline-inventory.html` — Step-by-step deadlines timeline, anonymized inventory, liquidity plan
- `governance-suggestions.html` — Missing-information checklist, pre-commitment matrix (decision & date), IPS, site suggestions
- `flagged-review.html` — Unverified cells, irregularities, privacy audit
- `glossary.html` — Plain-English glossary
- `briefing-sheet.html` — One-page printable Attorney & CPA Briefing Sheet

## Privacy

All parcel figures rounded to nearest **$10**. Placeholders only (Property A / Property B). No PII/APN/addresses. See `COORDINATION.md`.

## Rebuild model

```bash
python3 scripts/build_model.py
```

Generates `data/verified_data.json` and `data/model_output.json`. Interactive engine in `assets/app.js` mirrors the Python model; the dashboard banner shows whether the recommendation moved after input changes.

## Sources

BOE LTA CCPI factors, BOE LTA 2025/009 (Prop 19), Rev. Proc. 2025-32 (OBBBA), FTB Form 540, SCC Assessor, SF Rent Board, HUD FY2026 FMR/SAFMR — linked per row. Not tax/legal advice.
