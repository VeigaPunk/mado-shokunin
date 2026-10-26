# ExecLocatorGate — seat status (complete; full report in `.ufo/waves/round-43/w1/ExecLocatorGate.md`)

Built `check-locators.py` (sha256 `c1ea52ad…`, stdlib, `python3 -I`, read-only). Selftest `cases=18 passed=18` with measured teeth
(`flipped_table_broken=yes flips=11 ok_to_miss=4 miss_to_ok=5`). The round-42 wrong locator MISSes (LOG:2483, registration:61) and
the corrected `Hyprland-HyprCtl.cpp:427-428,448` is OK. All 59 `corpus/knowledge/*.md` at base: no fetch-dir locator ("none").
Working-tree round-43 correction line 2487 verifies OK on both of its locators.

## Limits (the short list)

- Identifier tokens are a proxy for the fact; the tool never reads what a line says.
- Prose without backticks is not checked — `NOFRAG` means "in range, nothing checked" (closure lesson line 83).
- Attribution is line-local, nearest preceding fragment. A line-wrapped markdown sentence misattributes (closure lesson line 84 is
  attributed to `w->size(GEOMETRIC_GOAL)` from the previous sentence; its MISS must not be cited as evidence about `:10-16`).
- A quotation of a wrong locator is flagged like an assertion.
- `supported=<j>` counts all same-line fragments; the verdict uses the attributed one, so `supported=1 verdict=MISS` is normal.
- Only named locators are checked: 17 of 18 locator-shaped tokens in the base LOG are skipped (name not in `--fetch`); bare range
  continuations (`:448`, `:16`) are never scored.
- A locator is judged against the `--fetch` bytes, not the intended commit — the fetch dir must be the round's own pins.
- Advisory only: not a counter, not scored, outside both C1 and C2 paths.

Artifacts: `receipt.txt` (sha256 `ad27d44c…`, verbatim outputs), `LOG-a35cfdf.md` (`f6c27a36…` = `git show a35cfdf:LOG.md`),
`LOG-corrected.md`, `LOG-worktree-at-run.md` (`c1cf804b…`), `registration-r42-corrected.md`, `lesson-r42-closure-a35cfdf.md`
(`118765c2…` = git blob), `knowledge-base-manifest.txt` (59 sha256, verify 59/0).
