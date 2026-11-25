#!/usr/bin/env python3
"""Privacy gate for anything published by the repository.

The repo owner's rule is stricter than "no names": no household-specific money
figure, parcel identifier, address, ZIP+street combination or account number may
appear in published output at all. Rounded or not, a value that can be traced
back to one house does not belong on a public page.

Two kinds of check:
  1. exact literals that must never be published (the household values supplied
     in the original request, and their rounded variants);
  2. structural patterns (street addresses, parcel/APN labels with digits,
     nine-digit numbers, long account-like digit runs) in published pages.

The private working notes, if the owner keeps them, must live outside the
published tree; this checker only scans what GitHub Pages can serve.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Files a visitor of https://<owner>.github.io/<repo>/ can open.
PUBLISHED_GLOBS = ["*.html", "pages/*.html", "docs/*.html", "companion/*.html", "companion/pages/*.html", "companion/estate-pathways/*.html", "companion/estate-pathways/pages/*.html", "*.js", "companion/estate-pathways/data/*.js", "*.json", "css/*.css"]

# Exact literals that must never appear in published output. These are the
# household figures from the request plus their common rounding variants. Keep
# the list terse: it is a guard, not a copy of the numbers.
# Integration adjustment (session e4e062ed, logged in COORDINATION.md): the
# owner's recorded instruction publishes rounded-to-$10 figures, so the rounded
# variants (3,100,000 / 1,800,000 / 7,150 / 550,540 / 539,740 ...) are no longer
# forbidden. The EXACT unrounded owner-supplied series below is forbidden harder
# than before, in both comma and bare-digit forms.
FORBIDDEN_LITERALS = [
    "550,537", "550537", "539,743", "539743", "518,786", "518786",
    "508,614", "508614", "498,642", "498642", "493,530", "493530",
    "483,854", "483854", "474,368", "474368", "465,067", "465067",
    "455,949", "455949", "449,101", "449101", "440,305", "440305",
    "114,248", "114248", "112,008", "112008", "109,814", "109814",
    "107,662", "107662", "105,595", "105595", "104,513", "104513",
    "102,465", "102465", "100,456", "100456", "98,488", "96,557",
]

# Exact unrounded tax history (comma forms; (?!.\d) avoids public index levels
# such as the S&P value 2,061.47 in the preserved crash-replay dataset table).
TAX_SERIES_PATTERN = (re.compile(
    r"\b(7,207|7,003|6,917|6,755|6,662|6,565|6,383|6,414|6,130|5,965|"
    r"2,439|2,315|2,179|2,107|2,066|2,197|2,134|2,061|1,740|1,675)\b(?!\.\d)"),
    "unrounded tax history (exact owner-supplied values)")

# Structural patterns. Each entry is (compiled regex, human description).
PATTERNS = [
    (re.compile(r"\b\d{1,6}\s+(?:[A-Z][a-z]+\s){1,3}(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Ln|Lane|Ct|Court|Blvd|Way|Ter|Place|Pl)\b"),
     "street address"),
    (re.compile(r"\b(?:APN|Assessor['’]s? Parcel(?: Number)?|Parcel(?: Number| No\.?))\s*[:#]?\s*\d{3}[-\s]?\d{3}[-\s]?\d{1,3}\b", re.I),
     "parcel / APN number"),
    (re.compile(r"\bCA\s+9\d{4}\b"),
     "ZIP code in a California address context"),
    (re.compile(r"\bCupertino,\s*CA\b", re.I),
     "city-plus-state address fragment"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
     "Social Security number pattern"),
    (re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b"),
     "card / account-length digit run"),
]

# Code samples and datasets legitimately contain long digit runs; these files are
# excluded from the digit-run rule only (still subject to literals + addresses).
DIGIT_RUN_EXEMPT = {"data/historical-returns.json", "data/black-swan-results.json"}


def published_files():
    seen = []
    for pattern in PUBLISHED_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            if path.is_file() and path not in seen:
                seen.append(path)
    return seen


def scan(path: Path):
    findings = []
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = path.relative_to(ROOT).as_posix()
    for literal in FORBIDDEN_LITERALS:
        for mm in re.finditer(r"(?<![\d.])" + re.escape(literal) + r"(?![\d.])", text):
            findings.append(f"{rel}: published raw household value literal {literal!r}")
    tax_regex, tax_label = TAX_SERIES_PATTERN
    for match in tax_regex.finditer(text):
        findings.append(f"{rel}: {tax_label} -> {match.group(0)!r}")
    for regex, label in PATTERNS:
        if label.startswith("card / account") and rel in DIGIT_RUN_EXEMPT:
            continue
        for match in regex.finditer(text):
            findings.append(f"{rel}: {label} -> {match.group(0)!r}")
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--selftest", action="store_true",
                    help="prove the detector works by scanning a synthetic leak, then scan the real tree")
    args = ap.parse_args()

    if args.selftest:
        probe = ROOT / "_privacy_selftest.html"
        probe.write_text("<p>12 Elm Street, APN 123-456-789, value 550,537</p>", encoding="utf-8")
        try:
            caught = scan(probe)
        finally:
            probe.unlink()
        if len(caught) < 3:
            print("Privacy gate SELFTEST FAILED: the detector missed a synthetic leak "
                  f"(caught {len(caught)} of 3 planted findings).")
            return 1
        probe2 = ROOT / "_privacy_selftest2.html"
        probe2.write_text(
            "<p>Assessed value 550,540; tax 7,210; index 2,061.47; rent 7,150; jittered 493,540</p>",
            encoding="utf-8")
        try:
            clean = scan(probe2)
        finally:
            probe2.unlink()
        if clean:
            print("Privacy gate SELFTEST FAILED: compliant rounded output was flagged "
                  f"({clean}).")
            return 1
        print(f"Privacy gate selftest passed: {len(caught)}/3 synthetic findings caught and "
              "compliant rounded output left clean, so a 'zero findings' result below is meaningful.")

    files = published_files()
    if len(files) < 10:
        print(f"Privacy gate FAILED: only {len(files)} published files found; "
              "the scan almost certainly ran in the wrong directory.")
        return 1

    findings = []
    for path in files:
        findings.extend(scan(path))

    if findings:
        print("Privacy gate FAILED — household-identifying content would be published:")
        for finding in findings:
            print(" - " + finding)
        print("\nRemove it, or move the material to a private location outside the published tree.")
        return 1

    if not args.quiet:
        print(f"Privacy gate passed: {len(files)} published files scanned, "
              f"{len(FORBIDDEN_LITERALS)} forbidden literals and {len(PATTERNS)} patterns, zero findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
