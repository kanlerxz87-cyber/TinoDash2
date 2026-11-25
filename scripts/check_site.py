#!/usr/bin/env python3
"""Small dependency-free checks for the static Pages site."""
import re
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted(ROOT.glob("*.html")) + sorted((ROOT / "pages").glob("*.html")) + sorted((ROOT / "docs").glob("*.html"))

# Privacy guard: household figures and identifiers must never be published.
PRIVACY_PATTERNS = [
    r"2,950,000", r"3,100,000", r"3,250,000", r"1,700,000", r"1,800,000", r"1,900,000",
    r"7,150", r"6,800", r"7,500", r"550,5\d\d", r"539,7\d\d", r"114,2\d\d", r"\b95014\b", r"\b94122\b",
    r"3\.1M\b", r"1\.8M\b", r"2\.95M\b", r"3\.25M\b",
]
PRIVACY_FILES = [p for p in list(ROOT.rglob("*.html")) + list(ROOT.rglob("*.js")) + list(ROOT.rglob("*.json")) + list(ROOT.rglob("*.css")) + list(ROOT.rglob("*.md")) if ".git" not in p.parts and "node_modules" not in p.parts]

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
for f in PRIVACY_FILES:
    txt=f.read_text(encoding="utf-8",errors="ignore")
    for pat in PRIVACY_PATTERNS:
        if re.search(pat, txt):
            errors.append(f"{f.relative_to(ROOT).as_posix()}: privacy pattern {pat} found")
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

if errors:
    print("Static site check failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)
print("Static site check passed: required pages/assets/anchors present, all table rows linked, no remote scripts or styles.")
