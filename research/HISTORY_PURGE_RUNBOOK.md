# History purge runbook — repository owner action required

**Why:** PRs #3/#4/#5 (and closed, unmerged PRs #8/#10) placed household-derived figures —
including unrounded property values, tax bills and ZIP-level descriptions — into public
commits and closed-PR refs. The working tree is now clean (rounded figures only, per the
owner's 2026-11-25 policy), but **Git history and GitHub caches still contain the old data**.
Only the repository owner can complete this purge. Do not claim history is scrubbed until
every step below is verified.

## Steps

1. **Inventory the exposure** (do not paste outputs anywhere public):
   ```bash
   git log --all --oneline
   git rev-list --all | while read c; do git grep -l -E "$ZIP_A|$ZIP_B"   # set to the two property ZIPs from private/ESTATE_INVENTORY.md $c -- 2>/dev/null; done | sort -u
   gh api repos/kanlerxz87-cyber/TinoDash2/pulls?state=closed --jq '.[].number'
   ```
2. **Rewrite history** with `git filter-repo` (or BFG) to strip/redact the offending files
   and blobs across all branches and tags:
   ```bash
   pip install git-filter-repo
   git clone --mirror git@github.com:kanlerxz87-cyber/TinoDash2.git tino-mirror.git
   cd tino-mirror.git
   python3 -m git_filter_repo --sensitive-data-removal   # or --replace-text ../expressions.txt
   git push --force --mirror origin
   ```
3. **Closed-PR refs:** force-pushing main does not delete closed-PR refs (`refs/pull/N/head`).
   Contact GitHub Support and request deletion of the stale PR refs for PRs #3, #4, #5,
   #8, #10 (and any other figure-bearing PRs) plus a **cache and search-index purge**.
4. **Caches & search:** request GitHub purge of cached views (raw.githubusercontent,
   api.github.com, github.com search index) for the removed SHAs.
5. **Forks & clones:** enumerate forks (`gh api repos/.../forks`); ask owners to delete or
   re-sync after the purge. Audit any local clones/backups and rotate anything sensitive.
6. **Verify:**
   ```bash
   git clone git@github.com:kanlerxz87-cyber/TinoDash2.git verify && cd verify
   git rev-list --all | while read c; do git grep -l -E "$ZIP_A|$ZIP_B"   # set to the two property ZIPs from private/ESTATE_INVENTORY.md $c -- 2>/dev/null; done   # expect empty
   ```
   Confirm the closed PR commits no longer resolve (e.g. `git fetch origin refs/pull/8/head`).
7. **Record completion** in `COORDINATION.md` (append-only exposure log) with the date.

## Until then

- Treat the historical exposure as live: do not add more identifying detail anywhere.
- The public site publishes rounded figures only (owner policy, 2026-11-25) and no
  identifiers; exact values live only in the git-ignored `private/` annex.
- If any new exposure is discovered: `git rm --cached`, rewrite the commit before pushing,
  and log the incident in `COORDINATION.md` immediately.

*Reference: FTC privacy/security guidance — https://www.ftc.gov/business-guidance/privacy-security*
