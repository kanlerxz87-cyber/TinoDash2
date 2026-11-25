# COORDINATION.md — Shared Task Board & Verification Log

**Repository:** `kanlerxz87-cyber/TinoDash2`  
**Active Branch:** `arena/43306062-tinodash2`  
**Coordinator / Integration Session ID:** `session-43306062`  
**Privacy Policy:** STRICT PRIVACY-FIRST — All parcel-identifying tax and assessment numbers are rounded to the nearest **$10 increment** prior to commit. Property addresses, APNs, owner names, and trust names are strictly anonymized (`Property A — Cupertino 95014 Single-Family Residence` and `Property B — San Francisco 94122 Outer Sunset 3-Unit Property`). Zero raw unrounded parcel figures appear anywhere in Git history or the published site. Official published statutory rates (e.g., BOE $1,044,586 cap, HUD FMRs) are shown as published.

---

## Task Board

| Task ID | Task Name | Status | Owning Session ID | File Scope |
| :--- | :--- | :--- | :--- | :--- |
| **T-01** | **Privacy-First Architecture & $10-Increment Historical Table Verification** | `done` | `session-43306062` | `data/verified_data.json`, `scripts/build_model.py`, `.nojekyll` |
| **T-02** | **Tax, Legal, Prop 19, Prop H, Form 540 (1% MHSA) & Federal Estate Tax ($15M OBBBA) Research** | `done` | `session-43306062` | `data/verified_data.json`, `tax-legal.html` |
| **T-03** | **Multi-Path Quantitative Projection Engine (Pure + Mixed Paths, Ranges, Same-Year Sale, 1031, Depreciation Recapture, Imputed Rent)** | `done` | `session-43306062` | `scripts/build_model.py`, `data/model_output.json`, `projections.html` |
| **T-04** | **Black Swan Economic Regimes (1929, 1970s Stagflation, 2000 Dot-Com, 2008 GFC, Bay Area M7.0 Quake) & 24–36m 3M–2Y Treasury Phased-Investing Stress Test** | `done` | `session-43306062` | `scripts/build_model.py`, `data/model_output.json`, `black-swan.html` |
| **T-05** | **Property A & Property B Operations, Comps vs HUD SAFMR, Insurance, Solar/Water & 5-Year Capital Maintenance Plan** | `done` | `session-43306062` | `operations-capital.html`, `data/verified_data.json` |
| **T-06** | **Step-by-Step Trust Inheritance Timeline, Deadlines, Private Estate Inventory & Liquidity Plan** | `done` | `session-43306062` | `timeline-inventory.html`, `data/verified_data.json` |
| **T-07** | **Missing Information Discovery Matrix, Pre-Commitment Governance Log, Investment Policy Statement (IPS) & Site Improvement Suggestions** | `done` | `session-43306062` | `governance-suggestions.html`, `glossary.html` |
| **T-08** | **Flagged for Review Page (Unverified Cells, Mathematical Variance Audit & Official Source Links)** | `done` | `session-43306062` | `flagged-review.html`, `data/verified_data.json` |
| **T-09** | **One-Page Printable Attorney & CPA Briefing Sheet Export** | `done` | `session-43306062` | `briefing-sheet.html`, `assets/styles.css` |
| **T-10** | **Final Integration: Landing Dashboard (`index.html`), Shared Navigation, Interactive What-If Controls, Link Verification, PR & Merge to `main`** | `done` | `session-43306062` | `index.html`, `assets/styles.css`, `assets/app.js`, `README.md`, `COORDINATION.md` |

---

## Verification Log

- **2026-11-25 (`session-43306062`):** Initialized `COORDINATION.md` on `arena/43306062-tinodash2`. Claimed tasks `T-01` through `T-10`. Enforced strict $10 rounding rule before writing any data files to preserve a clean, privacy-first Git history.
- **2026-11-25 (`session-43306062`):** Built `scripts/build_model.py` → `data/verified_data.json` (Property A 13 rows 2014–2026, Property B 11 rows 2016–2026) and `data/model_output.json` (51 yearly projections 2026–2076, 6 paths, 5 Black Swan regimes, 7-point distribution fan). All parcel figures $10-rounded. Verified against BOE LTA CCPI factors (2013/060–2025/048), Rev. Proc. 2025-32 (OBBBA $15M), FTB Form 540 (12.3% + 1% MHSA = 13.3%), BOE LTA 2025/009 (Prop 19 $1,044,586), SCC TRA, SF Rent Board §37.9C, HUD FY2026 FMR/SAFMR.
- **2026-11-25 (`session-43306062`):** Created 10 HTML pages + `assets/styles.css` + `assets/app.js` (interactive What-If engine mirroring Python model, "Did the Recommendation Move?" banner, SVG fan/drawdown/bar charts). Verified: all internal links resolve, all What-If control IDs match, local HTTP 200 on all pages, `python3 scripts/build_model.py` rebuilds cleanly with Path 1A #1 ($34,995,260).
- **Flagged irregularities (do not block merge):** Property A 2026 tax `--` (unverified); Property B 2026 tax/assessed `--` (not in source); Property B 2018 +18.4% parcel tax jump (Measure G-type flat charge); Property B 2022 +1.95% vs +2.0% (0.04% rounding variance); Property B 2016 2015 base omitted. All published on `flagged-review.html` with source links.

## PR & Merge

- **PR:** _pending — to be recorded after `gh pr create`_
- **Merge status:** _pending_
- **GitHub Pages:** Active on `main` root (`/`) at `https://kanlerxz87-cyber.github.io/TinoDash2/` — verify deployment after merge.
