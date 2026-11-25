# Estate Pathways · privacy-first decision workspace

Static decision-support site for comparing an inherited California residence (Property A) with an already-owned multi-unit residence (Property B). It is intended to help a household and its attorney/CPA identify missing evidence and compare live, rent, sell/reinvest, staged investing and mixed paths on common dates/horizons.

## Privacy and public-data policy

- This repository is public. Do **not** commit names, addresses, ZIP codes, parcel/APN identifiers, tax bills, leases, appraisals, return records, bank/investment statements or other private facts.
- The site deliberately does not publish the user-provided exact property values, historical assessments, rent, utility and insurance estimates. It uses generic labels and leaves case-specific inputs blank/unverified.
- There is no server-side model, form submission, analytics, external font, cookie or application storage. Calculator values are computed in the browser session. Ordinary browser/hosting infrastructure can still process page requests/session metadata; do not enter confidential information in the public site.
- `robots` metadata requests no indexing, but cannot guarantee confidentiality or prevent access to a public URL.
- Source links are outbound to official government or primary authorities where available. A general official source does not verify any private property value, local tax-rate-area rate, insurance premium, rent comparable, lease or Prop 19 eligibility.

## Pages

- `index.html` — executive summary, first-screen answer-changing facts and current-law anchors.
- `decisions.html` — pure and mixed paths, black-swan regimes, local Treasury parking / phased equity stress test and input-bound scenario envelope.
- `property.html` — user-input low/base/high property value, assessment, tax, operating-cost, rent and imputed-rent projection. No default financial values are supplied.
- `brief.html` — one-page-target Attorney & CPA sheet; browser Print → Save as PDF.
- `law.html`, `timeline.html`, `questions.html`, `suggestions.html`, `flagged.html`, `glossary.html` — authorities, process, unresolved questions, approvals backlog, flags and reference terms.

All calculations are simplified planning illustrations, not tax, legal, valuation, insurance, landlord or investment advice. Projections have no default forecasts and do not resolve taxes. Update assumptions from dated primary evidence and professional advice; current law cannot be assumed to remain in force in 2040–2050.

## Local preview

Open `index.html` in a browser or serve the repository with any static HTTP server. No package installation or build step is needed. JavaScript syntax can be checked with `node --check assets/app.js`.

## GitHub Pages

A GitHub Actions workflow at `.github/workflows/pages.yml` deploys static HTML/CSS/JS after changes reach `main` (and on manual workflow dispatch). The repository’s Pages setting must use GitHub Actions as its deployment source. The Arena session branch is fixed to `arena/3ba11c7d-tinodash2`; task execution stays on that branch.

## Research date and source limitations

Legal summaries were checked against linked official sources on Nov. 25, 2026. They are not updated automatically. A proposed measure remains flagged until an official final outcome/effective-law source is checked. See `COORDINATION.md` for task status, verification notes and known irregularities.
