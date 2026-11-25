# TinoDash2 — Inheritance Decision Workspace

Privacy-first decision materials for comparing inherited-home and existing-property paths.
The public site is the root **Estate Pathways** site served by GitHub Pages from `main` (legacy
builder, repository root).

**Live site:** <https://kanlerxz87-cyber.github.io/TinoDash2/>

## Privacy rules (binding — see COORDINATION.md)

- No household-specific figures in the public tree or in Git, even rounded to $10. Rounding does
  not anonymize.
- Public outputs use placeholders only (Property A, Property B, Owner B).
- No names, street addresses, ZIP codes, parcel/APN IDs, account numbers, leases, or trust details.
- Household analysis lives only in `private/` (git-ignored, never committed or published).
- Prior exposure: household figures were merged to `main` in earlier PRs (#3/#4/#5) and in the
  figure-bearing `docs/` dashboard from PR #12. Removing files from the tree does **not** remove
  them from Git history. A history purge requires repository-owner action. See the Exposure log
  in COORDINATION.md.

## What is in the public site

| Page | What it is for |
|---|---|
| `index.html` | Dashboard: decision state, what would change the answer, evidence inventory, path comparison, what-if calculator (blank inputs, browser-only), timeline, legislation watch, suggestions queue, sources, glossary |
| `war-room.html` | The nine gates that block a decision, the pre-commitment register, requirement coverage, decision journal |
| `crash-replay.html` · `black-swan.html` | Does parking sale proceeds for 24 months and phasing in over 36 actually help? 89 ten-year windows, 1928–2025, plus method notes |
| `comparison.html` · `calculator.js` | Eight paths on one calendar, including four mixed paths, with a 25-input browser-only model |
| `questions.html` | Every open question, its owner, and the evidence that closes it |
| `law-watch.html` | Enacted anchors, live proposals, re-check calendar, change procedure |
| `suggestions.html` | Twenty-two reviewable actions with acceptance criteria |
| `brief.html` | One printable page for the attorney and CPA |
| `flagged.html` · `FLAGGED_FOR_REVIEW.html` | Unverified, irregular, or conflicting items, with links for manual review |
| `sources.md` | Official source register and verification log |

## Validation

Every push and pull request runs:

```bash
python3 scripts/check_site.py                   # required pages exist and are linked from index.html,
                                               # every table row carries a source link, all local
                                               # anchors resolve, no remote scripts/styles, privacy scan
python3 scripts/privacy_check.py --selftest    # plants a synthetic leak to prove the detector fires,
                                               # then scans every published file
python3 scripts/verify_sources.py              # recomputes the historical datasets against published index levels
node --check app.js && node --check calculator.js
node scripts/smoke_calculator.js               # drives the calculator against a stub DOM and asserts
                                               # it references no network or storage APIs
```

`scripts/verify_sources.py --online` additionally re-fetches the cited official pages. It cannot
run in a sandbox without outbound HTTPS, and it says so explicitly rather than reporting a pass.

## Rebuilding generated pages

```bash
python3 scripts/build_pages.py            # war-room, law-watch, questions, comparison, suggestions, brief
python3 scripts/build_crash_replay_page.py
```

Both generators are dependency-free (Python standard library only) and write into the repository
root, because that is the path Pages serves. The household model script (`scripts/build_model.py`)
is not in the public tree at all: any household-derived output belongs in the git-ignored
`private/` directory and must never target a published path.

## Disclaimer

Planning and decision-organization aid only. Not legal, tax, investment, appraisal, or insurance
advice.
