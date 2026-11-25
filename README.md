# Estate Pathways

A privacy-first, static decision workspace for comparing possible inherited-home and existing-property paths. The site is plain HTML/CSS/JavaScript and runs locally in a browser; the what-if form does not transmit or save inputs. Do not enter names, parcel IDs, addresses, trust documents, or account details.

## Preview locally

Open `index.html` in a modern browser. No build dependencies, trackers, external fonts, or third-party scripts are used. The printable attorney and CPA briefing sheet is available from the top-right print button. `black-swan.html` publishes cited public-market stress anchors (no household figures).

## Privacy boundary

- The public site intentionally omits household identifiers and the submitted exact property figures. Current local-law and federal-law references are official source links, not personalized conclusions.
- `private/estate-inventory-template.md` is a blank working template, ignored by Git and not part of the Pages deployment artifact. Keep any completed inventory encrypted and outside the repository. `.gitignore` is a guardrail, not a security boundary; check staged files before every commit.
- A privacy audit after other session PRs merged found user-submitted property figures and ZIP codes in earlier public `main` commits and pages. This branch redacts the current pages, but public `main` still exposes the earlier versions until the change merges, and prior commits retain the data; a normal PR cannot erase them. The repository owner must decide on a history rewrite and cache/index purge. See `COORDINATION.md` before treating the history as cleaned.

## GitHub Pages

Pages is served by the **legacy builder** (source: `main` branch, root). Merging to `main` updates the live site automatically (`https://kanlerxz87-cyber.github.io/TinoDash2/`). The GitHub Actions workflow only **validates** the site (local links, JS syntax); its former deploy job was removed in Nov 2026 because a legacy-built Pages site cannot be deployed by `actions/deploy-pages`. If Pages is switched to “GitHub Actions” in Settings → Pages, restore a deploy job. The site does not include a backend.

## Evidence limitations

Published legal/tax claims have direct official links. Current values are not forecasts for a 2040–2050 transfer. Parcel-specific assessments, rent, insurance, utilities, capital costs, rental legality and taxes require private records and professional review. Unverified claims and missing evidence are listed in `FLAGGED_FOR_REVIEW.html`.
