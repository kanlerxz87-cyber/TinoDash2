# TinoDash2 — Inheritance Decision Dashboard

Privacy-first static dashboard for organizing an inheritance decision involving:
- **Property A**: Santa Clara County, CA property to be inherited by trust (planned 2040–2050).
- **Property B**: San Francisco, CA property already owned by Owner B.

## Privacy

- Public outputs use placeholders only (Property A, Property B, Owner B).
- No names, street addresses, ZIP codes, parcel/APN IDs, account numbers, or exact traceable public-record values are published.
- Currency values are rounded to the nearest $10 in published outputs.
- Sensitive details discovered during research are for internal use only and must not be published.

## Site

The static site lives in [`docs/`](docs/) and is intended for GitHub Pages.

- Landing page: `docs/index.html`
- Data model: `docs/data/model.json`
- Model build script: `scripts/build_model.py`

To rebuild the model data:

```bash
python3 scripts/build_model.py
```

## GitHub Pages

Configure GitHub Pages to serve from the `main` branch, `/docs` folder.

## Verification

Every table row should include an official source link where possible. Values that cannot be confirmed from an official source are left blank/flagged as unverified. See `docs/sources.html` and `docs/flagged.html`.

## Disclaimer

This repository is a planning and decision-organization aid. It is not legal, tax, investment, appraisal, or insurance advice.
