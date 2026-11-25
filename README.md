# Decision Atlas

A static, privacy-first educational decision framework for property and estate planning. No household data is included or stored. The black-swan calculator uses synthetic returns, not actual historical data or tax-aware property projections. See the Flagged for Review page for gaps.

## Build and test

Requires Python 3; no package installation or secrets. Run `python3 scripts/build.py` to regenerate the HTML from the source, and `python3 -m unittest discover -s tests` to test build, privacy and internal links. Serve with `python3 -m http.server 8000 --bind 0.0.0.0`. The site also works as static files on GitHub Pages.

Never commit private documents, property identifiers, estate inventories, precise household values, or credentials. Rounding is not sufficient anonymization. The public site is not professional advice and cannot refresh itself; review the sources with an attorney and CPA.
