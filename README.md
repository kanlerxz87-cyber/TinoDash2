# Estate Pathways

A privacy-first, static decision workspace for comparing possible inherited-home and existing-property paths. The site is plain HTML/CSS/JavaScript and runs locally in a browser; the what-if form does not transmit or save inputs. Do not enter names, parcel IDs, addresses, trust documents, or account details.

## Preview locally

Open `index.html` in a modern browser. No build dependencies, trackers, external fonts, or third-party scripts are used. The printable attorney and CPA briefing sheet is available from the top-right print button.

## Privacy boundary

- The public site intentionally omits household identifiers and the submitted exact property figures. Current local-law and federal-law references are official source links, not personalized conclusions.
- `private/estate-inventory-template.md` is a blank working template, ignored by Git and not part of the Pages deployment artifact. Keep any completed inventory encrypted and outside the repository. `.gitignore` is a guardrail, not a security boundary; check staged files before every commit.
- The initial repository history consisted of a README only. No household values were in the history to scrub. Do not add source documents or private inputs in future commits.

## GitHub Pages

The GitHub Actions workflow in `.github/workflows/pages.yml` validates local links on pull requests and deploys the root static site from `main`. The site does not include a backend. If Pages has not been enabled for GitHub Actions on the repository, select **Settings → Pages → Build and deployment → GitHub Actions** after merging.

## Evidence limitations

Published legal/tax claims have direct official links. Current values are not forecasts for a 2040–2050 transfer. Parcel-specific assessments, rent, insurance, utilities, capital costs, rental legality and taxes require private records and professional review. Unverified claims and missing evidence are listed in `FLAGGED_FOR_REVIEW.html`.
