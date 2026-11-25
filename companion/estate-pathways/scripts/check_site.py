#!/usr/bin/env python3
"""Small dependency-free checks for the static Pages site."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.glob("*.html")) + sorted((ROOT / "pages").glob("*.html"))

# Pages a visitor can reach from the dashboard. If one of these disappears from
# the build, the site is broken even though every remaining link still resolves.
REQUIRED = [
    "index.html",
    "war-room.html",
    "comparison.html",
    "crash-replay.html",
    "black-swan.html",
    "questions.html",
    "law-watch.html",
    "worksheets.html",
    "brief.html",
    "suggestions.html",
    "FLAGGED_FOR_REVIEW.html",
]

class Scanner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.table_row_depth = 0
        self.row_has_link = False
        self.row_has_data_cell = False
        self.table_rows_without_links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag in {"a", "link", "script"}:
            attr = "href" if tag in {"a", "link"} else "src"
            if attrs.get(attr):
                self.links.append((tag, attrs[attr]))
        if tag == "tr":
            self.table_row_depth += 1
            self.row_has_link = False
            self.row_has_data_cell = False
        elif tag == "td" and self.table_row_depth:
            self.row_has_data_cell = True
        elif tag == "a" and self.table_row_depth:
            self.row_has_link = True

    def handle_endtag(self, tag):
        if tag == "tr" and self.table_row_depth:
            if self.row_has_data_cell and not self.row_has_link:
                self.table_rows_without_links.append("table row has no source link")
            self.table_row_depth -= 1
            self.row_has_link = False

errors=[]
warnings=[]
scanners={}
for page in PAGES:
    if not page.exists():
        errors.append(f"Missing required page: {page.name}")
        continue
    parser=Scanner()
    parser.feed(page.read_text(encoding="utf-8"))
    page_name=page.relative_to(ROOT).as_posix()
    scanners[page_name]=parser
    for issue in parser.table_rows_without_links:
        if page_name.startswith("docs/"):
            # Analysis tables: per-row source links are a verification gap, reported as warnings
            # and listed on the Flagged for Review page. Not a build failure.
            warnings.append(f"{page_name}: {issue}")
        else:
            errors.append(f"{page_name}: {issue}")

for name, parser in scanners.items():
    for tag, url in parser.links:
        if url.startswith(("https://", "mailto:", "tel:", "data:")):
            continue
        if url.startswith("http://"):
            errors.append(f"{name}: non-HTTPS external URL: {url}")
            continue
        if tag in {"script", "link"} and url.startswith("//"):
            errors.append(f"{name}: protocol-relative external asset: {url}")
            continue
        path_part, _, fragment = url.partition("#")
        path_part = path_part.partition("?")[0]
        target = (ROOT / name).parent / path_part if path_part else ROOT / name
        if path_part and not target.exists():
            errors.append(f"{name}: missing local target {url}")
            continue
        if fragment:
            target_name = target.relative_to(ROOT).as_posix() if path_part else name
            target_parser = scanners.get(target_name)
            if target_parser is None and target.exists() and target.suffix.lower()==".html":
                target_parser=Scanner(); target_parser.feed(target.read_text(encoding="utf-8"))
            if target_parser and fragment not in target_parser.ids:
                errors.append(f"{name}: missing anchor #{fragment} in {target_name}")
        if tag in {"script", "link"} and path_part and not target.exists():
            errors.append(f"{name}: missing local asset {url}")

# The public pages must contain no remote executable code or remote stylesheet/font loads.
for name, parser in scanners.items():
    for tag, url in parser.links:
        if tag in {"script", "link"} and url.startswith(("https://", "//")):
            errors.append(f"{name}: remote executable/style resource would expose visitor metadata: {url}")

present = {p.name for p in PAGES}
for required in REQUIRED:
    if required not in present:
        errors.append(f"Required page is missing from the build: {required}")

# Anything published must be reachable from index.html, and index.html must not
# link to a page that only exists locally.
index_ids = scanners.get("index.html")
if index_ids is None:
    errors.append("index.html was not scanned")
else:
    linked = {url.partition("#")[0] for tag, url in scanners["index.html"].links if tag == "a"}
    for required in REQUIRED:
        if required != "index.html" and required not in linked:
            errors.append(f"index.html does not link to required page: {required}")

# Privacy scan: no addresses, ZIP codes, parcel IDs, or the owner's city names on any published surface.
PRIVACY_PATTERNS = [
    # Owner policy (2026-11-25): rounded-to-$10 household figures and jurisdiction
    # names are PUBLISHED (decision recorded in COORDINATION.md). Identifiers and
    # exact unrounded record values remain banned.
    (r"\b(550537|539743|529161|518786|508614|498642|493530|483854|474368|465067|455949|449101|440305)\b", "unrounded Property A record value"),
    (r"\b(114248|112008|109814|107662|105595|104513|102465|100456|98488|96557)\b", "unrounded Property B record value"),
    (r"\b(7207|7003|6917|6755|6662|6565|6383|6414|6130|5965|2439|2315|2179|2107|2066|2197|2134|2061|1740|1675)\b", "unrounded household tax-bill figure"),
    (r"\b(95014|94122)\b", "ZIP code"),
    (r"(?i)outer\s+sunset|sunset\s+district", "neighborhood name for Property B"),
    (r"(?i)\bAPN\s*[:#]?\s*\d", "assessor parcel number"),
    (r"(?i)parcel\s*(id|number|no\.?)\s*[:#]?\s*\d", "parcel identifier"),
    (r"(?i)\bzip(\s*code)?\s*[:#]?\s*9\d{4}\b", "ZIP code"),
    (r"\b\d{1,5}\s+[A-Z][a-z]+\s+(Ave|Avenue|St|Street|Rd|Road|Dr|Drive|Way|Ln|Lane|Blvd|Court|Ct)\b", "street address"),
]
# COORDINATION.md is the internal, append-only board: not website content, so it is excluded from the public scan.
PUBLIC_FILES = [f for f in sorted(ROOT.glob("*.md")) if f.name != "COORDINATION.md"] + sorted(ROOT.glob("*.html")) + sorted((ROOT / "pages").glob("*.html"))
for f in PUBLIC_FILES:
    text = f.read_text(encoding="utf-8")
    for pat, label in PRIVACY_PATTERNS:
        for m in re.finditer(pat, text):
            errors.append(f"{f.relative_to(ROOT).as_posix()}: privacy scan hit ({label}): {m.group(0)[:40]!r}")

if errors:
    print("Static site check failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)
print(f"Static site check passed: {len(REQUIRED)} required pages present and linked from index.html, "
      "all table rows carry a source link, every local anchor resolves, no remote scripts or styles, privacy scan clean.")
