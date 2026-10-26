# ExecLocatorGate — locator gate for prose locators (round 43, w1)

**Deliverable:** `.ufo/waves/round-43/w1/ExecLocatorGate/check-locators.py` — sha256 `c1ea52ad5db21fdf81022d0425e7cad42fc3e34dd5083915b127a46ab948a27e`,
Python 3.14.8, stdlib only (imports at `receipt.txt` §12), read-only, runs under `python3 -I`.
**Evidence:** `.ufo/waves/round-43/w1/ExecLocatorGate/receipt.txt` (400 lines, sha256 `ad27d44cbd520bfad300200eccb89944783f2711ead395eecda84151ad0a28d2`) — every output verbatim.

## What it does

Given `--fetch DIR` (a directory of pinned receipts) and prose files, it finds every token `<name>:<N>[-<M>][,<N2>[-<M2>]...]`
whose basename is a file in `DIR`, takes the backticked code fragments of the same prose line, and decides whether the cited
receipt lines carry the identifiers of the fragment that locator is attached to. Output is one line per locator
`LOC <file>:<line> <locator> fragments=<k> supported=<j> verdict=OK|MISS|NOFRAG`, then `CHECK_LOCATORS: locators=<n> miss=<m>`;
exit 1 when `miss > 0`, 0 otherwise, 2 on usage errors (5 such invocations in the receipt §10). `--explain` adds
`SKIP`/`ATTR`/`FRAG` detail; `--selftest` builds its fixtures in a private temp dir.

Range test lives in one function (`in_ranges`) which `cited_text` uses for every line, so the selftest's flipped comparison
reaches every verdict.

## Evidence, in order (all in `receipt.txt`)

1. **Selftest** — `SELFTEST: cases=18 passed=18 locators=19 miss=6`; `SELFTEST: teeth flipped_table_broken=yes flips=11
   ok_to_miss=4 miss_to_ok=5`; `SELFTEST: PASS`, exit 0. The teeth are measured, not asserted: the whole 18-case table is re-run
   with the range-inclusion comparison inverted, and the selftest fails unless the table breaks in **both** directions. It also
   asserts the exit codes (a run with misses → 1, three usage paths → 2).
2. **The real mistake, MISS** — `LOG-a35cfdf.md` (sha256 `f6c27a36…`, byte-identical to `git show a35cfdf:LOG.md`) line 2483:
   `LOC …:2483 Hyprland-HyprCtl.cpp:394-395,412-413 fragments=6 supported=1 verdict=MISS`, `locators=1 miss=1`, exit 1.
3. **Corrected copy, OK** — same line with `Hyprland-HyprCtl.cpp:427-428,448` (sha256 `4025a183…`):
   `fragments=6 supported=2 verdict=OK`, exit 0.
4. **Frozen round-42 registration, MISS** — `.ufo/waves/round-42/registration.md:61`
   `Hyprland-HyprCtl.cpp:394-395,412-413 fragments=1 supported=0 verdict=MISS`, exit 1; corrected copy (`6d640f5a…`) `verdict=OK`, exit 0.
5. **True locators computed from the receipt, not guessed** — `grep -n GEOMETRIC_GOAL .ufo/waves/round-42/fetch/Hyprland-HyprCtl.cpp`
   → `426, 427, 428, 447, 448` (`w->size(…GEOMETRIC_GOAL)` at **427-428** and **448**);
   `grep -n 'FullMatch\|negative' …/Hyprland-RegexMatchEngine.cpp` → `7` (`starts_with("negative:")`), `8`, `16` (`RE2::FullMatch`).
   The round-42 cited lines 394-395,412-413 print as `"size": [{}, {}]` / `"grouped": [{}]` — template text, not the fact.
6. **`corpus/knowledge/*.md` at the base (59 entries)** — every entry `locators=0 miss=0`; `summary: entries=59 zero-locator=59`.
   No entry cites a round-42 fetch receipt, so there is no miss to report ("none", not MISS). Provenance:
   `knowledge-base-manifest.txt` (59 sha256 + extraction command), receipt §7 `manifest-verify: entries=59 mismatched=0`.
7. **`corpus/lessons/*.md` at the base (60 files)** — 59 with zero locators; `round-42-verifier-spotcheck.md locators=2 miss=1`.
   The closure lesson is copied into the seat dir (`lesson-r42-closure-a35cfdf.md`, sha256 `118765c2…` = the git blob) so the run
   cites a seat file, not scratch.
8. **Frozen round-43 registration** against the round-43 fetch dir — `locators=0`: the registration names receipts without `:line`,
   so it carries no locator this checker can score.
9. **Working-tree `LOG.md` snapshot** (`LOG-worktree-at-run.md`, sha256 `c1cf804b…`; another seat was appending the round-43 entry —
   I did not write it) — `locators=3 miss=1`. The new Round 43 correction line 2487 verifies **OK** at both
   `Hyprland-HyprCtl.cpp:427-428` (attr `w->size(GEOMETRIC_GOAL)`) and `Hyprland-RegexMatchEngine.cpp:7-8` (attr `negative:`);
   the untouched Round 42 line 2483 still MISSes, which is what "append a correction, never rewrite" implies.

## Limits (named, each demonstrated or structurally visible)

- **Identifier tokens are a proxy for the fact.** A cited range that carries the same identifiers for a different statement is
  supported falsely; a paraphrase that drops the identifier is a false miss. Nothing checks what the line *says*.
- **Prose without backticks is not checked.** `NOFRAG` = "locator resolved, nothing to check". Shown live: the closure lesson's
  line 83 (`Hyprland-HyprCtl.cpp:394-395,412-413` → `:427-428` …) prints `fragments=0 verdict=NOFRAG` because markdown wrapped the
  fragment to the next source line.
- **Attribution is line-local (nearest preceding fragment).** Line-wrapped prose breaks it: closure lesson line 84
  (`Hyprland-RegexMatchEngine.cpp:10-16 …`) is attributed to `w->size(GEOMETRIC_GOAL)`, a fragment carried over from the previous
  sentence. Its `MISS` is right by coincidence; **do not cite this run as evidence about `:10-16`** — the real defect there
  (`starts_with("negative:")` at 7-8, outside 10-16) is what the closure's own line-64 table states.
- **Quotation and assertion are indistinguishable.** The closure lesson quotes the round-42 wrong locator in order to correct it;
  the checker flags the quotation exactly like an assertion.
- **`supported=<j>` counts every same-line fragment; the verdict uses the attributed one.** `supported=1 verdict=MISS` is normal
  (LOG:2483 — `size` occurs at line 394, `w->size(GEOMETRIC_GOAL)` does not). Read `verdict`; use `--explain` to see attribution.
- **Only *named* locators are checked.** 17 of the 18 locator-shaped tokens in the base LOG resolve to nothing in `--fetch` and are
  skipped (receipt §6); bare range continuations such as `:448` and `:16` are not locator tokens at all, so a correction's *second*
  line reference is never scored.
- **The receipt bytes are the trust root.** A locator is judged against `--fetch`, not against the commit the prose intended; a
  receipt from another upstream version yields false misses. `--fetch` must be the round's own pins.
- **Range policy chosen here:** 1-based, `N-M` inclusive, reversed `M-N` normalised (selftest case 7), out-of-file numbers simply
  absent (case 3). Nothing flags `:0`, and nothing requires the cited range to be the *tightest* one that holds the fact.
- **Advisory, not a predicate.** No counter, no control set, no MET claim; this seat touched neither C1 nor C2 paths.

## Consequences the L1 can act on

- Two prose sites carry the round-42 wrong locator and both MISS: `LOG-a35cfdf.md:2483` (base bytes) and
  `.ufo/waves/round-42/registration.md:61` (frozen). The corrected copies pass at `:427-428,448`.
- Because the wrong sentence is left as written, a whole-file run keeps one MISS by design. A round-43 close-out gate must scope
  this checker to the new entry's lines (excerpt file or prose line range), not the whole `LOG.md`.
- Keep `fragment` and `locator` on one physical line in the round-43 lesson and LOG correction, or the checker degrades to `NOFRAG`
  (measured on the closure lesson line 83).
- The checker cannot be used to prove a fact. It can only refuse a locator whose cited lines lack the fragment's identifiers.

## Files (seat dir, all sha256 recorded above or in `receipt.txt`)

`check-locators.py`, `receipt.txt`, `LOG-a35cfdf.md`, `LOG-corrected.md`, `LOG-worktree-at-run.md`,
`registration-r42-corrected.md`, `lesson-r42-closure-a35cfdf.md`, `knowledge-base-manifest.txt`, `report.md`, this report.

No blockers. Tools installed: none. Scratch `/fast/scratch/hyaku/mado-r43/ExecLocatorGate/` used, then deleted.
