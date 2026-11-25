# TinoDash2 — Inheritance Decision Workspace

A privacy-first static site for deciding what to do with an inherited home while an existing
multi-unit property is already owned. Everything published here is plain HTML, CSS and
JavaScript served from the repository root by GitHub Pages (legacy builder, `main` root).

**Live site:** <https://kanlerxz87-cyber.github.io/TinoDash2/>

## What is published

| Page | What it is for |
|---|---|
| `index.html` | Dashboard: decision state, what would change the answer, evidence inventory, timeline, sources, glossary |
| `war-room.html` | The nine gates that block a decision, the pre-commitment register, requirement coverage, decision journal |
| `crash-replay.html` | Does parking sale proceeds for 24 months and phasing in over 36 actually help? Tested on 89 ten-year windows, 1928–2025 |
| `black-swan.html` | Method notes for the historical replay |
| `comparison.html` | Eight paths on one calendar, including four mixed paths, with a 25-input browser-only calculator |
| `questions.html` | Every open question, its owner, and the evidence that closes it |
| `law-watch.html` | Enacted anchors, live proposals, re-check calendar, change procedure |
| `suggestions.html` | Twenty-two reviewable actions with acceptance criteria |
| `brief.html` | One printable page for the attorney and CPA |
| `FLAGGED_FOR_REVIEW.html` | Everything unverified, blocked, or needing a human decision |

## What is deliberately *not* published

No household-specific figure appears anywhere in this repository — no property values, rent,
assessed values, tax bills, utility costs, insurance premiums, addresses, ZIP codes, parcel
numbers, or names. Rounding does not anonymize, so rounded figures are excluded too. The
calculator's inputs are blank by design and are never sent, stored, or logged.

## Checks (all run in CI on every push and pull request)

```bash
python3 scripts/check_site.py            # required pages present and linked, every table row sourced, all local anchors resolve, no remote scripts/styles
python3 scripts/privacy_check.py --selftest   # proves the detector works, then scans every published file
python3 scripts/verify_sources.py        # recomputes the historical datasets against published index levels
node --check app.js && node --check calculator.js
node scripts/smoke_calculator.js         # drives the calculator against a stub DOM; asserts no network/storage APIs
```

`scripts/verify_sources.py --online` additionally re-fetches the cited official pages. It
cannot run in a sandbox without outbound HTTPS, and it says so explicitly rather than reporting
a pass.

## Rebuilding the generated pages

```bash
python3 scripts/build_pages.py           # war-room, law-watch, questions, comparison, suggestions, brief
python3 scripts/build_crash_replay_page.py
```

Both generators are dependency-free (Python standard library only) and write into the
repository root, because that is what Pages serves.

## Privacy and history

`COORDINATION.md` holds the binding policy, the exposure log, and the owner actions still
outstanding. Earlier public commits and closed pull-request references contain household
figures from before the policy was tightened; **history is not scrubbed** and doing so requires
repository-owner action. See `FLAGGED_FOR_REVIEW.html`.

## Disclaimer

Planning and decision-organization aid only. Not legal, tax, investment, appraisal, or
insurance advice.
