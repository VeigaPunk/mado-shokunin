# R56W2CritScopeFix: able-to-fail demonstration for M56-1 (criterion 107 draft)

Seat: R56W2CritScopeFix (leaf; no subagents). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin. Scored trees: 63f48dc1b240b707c5ab9d634e2395ab90e1540c (round-55 entry) and 28fc86ac2359ec27406d8a2c63bef82ea6e947ed (round-56 integrated content). No lane file was edited; no git mutation was run against the lane (`git show` / `git archive` / `cat-file` only). Fixtures lived under /fast/scratch/hyaku/mado-r56/R56W2CritScopeFix/work and were removed before yield. Receipts: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w2/R56W2CritScopeFix/receipts/. Corrected criterion text: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w2/R56W2CritScopeFix/criterion-107-corrected.md.

## Verdict

1. The draft's core rule is falsifiable and it does catch the round-55 defect. On the committed r55 entry the draft checker reproduces the cited receipt row for row (rows=32 covered=25 miss=7, K14 and K17 among them). The round-56 counter's `scope_covers`, replayed on the 18 K rows, fails exactly K14 and K17 (`scope-replay-r55.txt` matches).
2. The same rule passes all 30 K rows of the r56 entry, and the r56 counter reports `scope=30/30`.
3. The draft as written is NOT sufficient, and it is not green on the integrated r56 entry. (a) It has no length (EOF) clause, so a widened anchor past EOF passes; (b) it leaves reversed ranges and duplicate registry ids undefined, and the two checkers disagree on them; (c) it silently skips any evidence row whose fourth cell is not `<file>:<N>`, so six uncovered rows of r56 can be made to disappear by writing `file:N-N`; (d) its declared limit on directory-qualified names is false. The counter also lacks the identifier-boundary test the criterion states.
4. On the integrated r56 entry at 28fc86, the draft "any row class" rule FAILS: `CHECK107: rows=39 covered=33 miss=6 verdict=FAIL`, misses E01, E03, E04, E05, E06, E07. The frozen r56 counter's `scope=30/30` covers K rows only and is not evidence that the E rows are anchored. This is a blocking defect for any claim that criterion 107 holds on r56. It is not a defect of the criterion's logic; the criterion is right to flag these rows.
5. The r55 counter at 63f48dc1 could not have caught K14/K17. It has no leg that reads registry cell 6 (the anchor), no locator parser and no line-coverage concept; see item (4) below.

## Items

### (1) Replay of the scope rule on the r55 entry (63f48dc1), K rows

Commands: `git -C $LANE show 28fc86ac…:quality/counters/c1-r56-autoreload-entry.py > $W/c1r56.py`, then `importlib.util.spec_from_file_location("c1r56", …)` and call `scope_covers(anchor, basename, line)`. Basename = last path component of the last http(s) URL in the registry source cell (the draft's NAME; for r56 this equals `basename_of(pin)`). Registry and entry read from `git show 63f48dc1…:corpus/SOURCES.md` and `…:corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`. Script: receipts/replay.py; output: receipts/replay-r55.out.

Output (decisive lines):
```
K14 S318 280 url_base=ConfigValues.cpp nlines=None counter_scope(url)=False ... draft_covers=False
K17 S052 2741 url_base=wayland.xml nlines=None counter_scope(url)=False ... draft_covers=False
(other 16 K rows: counter_scope(url)=True)
```
K14 anchor `ConfigValues.cpp:271-279,296` against 280; K17 anchor names no `wayland.xml:` at all. Matches receipts/scope-replay-r55.txt ("K rows 18 scope-failing 2").

Note: the cell-4 file name (`Hyprland-ConfigValues.cpp`) is not the rule's NAME; using it changes the result for many rows (the `Hyprland-` prefix is not in the anchors). The rule uses the URL basename, as the criterion says. Recorded for completeness only.

### (2) Same rule on all 30 K rows of the r56 entry (28fc86)

`replay.py r56` with `nlines` = line count of the pin blob at 28fc86 (`.ufo/waves/round-56/fetch/<pin>`: ConfigValues 735, ConfigWatcher 112, EventLoopManager 283, PropRefresher 160, legacy ConfigManager 2185, MiscFunctions 845, HyprCtl 2347, inotify.7.html 920, PropRefresher.hpp 41). Output: receipts/replay-r56.out. All 30 K rows: `counter_scope(url)=True`, `draft_covers=True`.

Full counter at 28fc86 (receipts/c1-r56-counter-28fc86.out):
`MADO_AUTORELOAD_ENTRY: rev=28fc86… rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none` (rc 0).

Any row class (the draft's grammar, E rows included), `python3 -I .ufo/waves/round-56/w1/R56RevQuality/check-anchor-cover.py --repo $LANE --rev 28fc86… --entry corpus/knowledge/hyprland-config-autoreload-r56.md --work $W/dc56` (receipts/draft-r56.out):
```
ANCHOR_COVER: row=E01 sid=S388 line=66 name=MiscFunctions.cpp locators=65,68 verdict=MISS reason=no-cover
ANCHOR_COVER: row=E03 sid=S383 line=106 name=ConfigWatcher.cpp locators=33-34,46,54-56,60,67,69,105 verdict=MISS reason=no-cover
ANCHOR_COVER: row=E04 sid=S389 line=1190 name=HyprCtl.cpp locators=1223,1276 verdict=MISS reason=no-cover
ANCHOR_COVER: row=E05 sid=S387 line=630 name=ConfigManager.cpp locators=776,1070,1079-1080,1816,1835-1836,1844 verdict=MISS reason=no-cover
ANCHOR_COVER: row=E06 sid=S387 line=1838 ...  verdict=MISS reason=no-cover
ANCHOR_COVER: row=E07 sid=S387 line=2134 ... verdict=MISS reason=no-cover
CHECK107: rows=39 covered=33 miss=6 verdict=FAIL
```
I confirmed each by reading the entry and registry rows directly: E03 quotes line 106 (`.file = WD->file`) while S383 lists 105; E01 quotes 66 while S388 lists 65,68. These are real gaps.

Counter-vs-draft agreement: for all 71 rows (32 at r55, 39 at r56), counter `scope_covers` (URL basename, nlines where known) and draft `covers` give the same verdict. The two diverge only on hand-built inputs (items 5 and the defects below).

### (3) Registry mutations (fixture commits; scratch repo; base 40b7bfe1 = 28fc86 tree)

Driver: receipts/mut.py; commits: receipts/mut-shas.txt; per-commit outputs: receipts/cnt-<name>.out (counter) and receipts/drf-<name>.out (draft). Each mutant is a single-file change from base.

| mutant | S383 / entry change | counter (full legs) | draft (K rows / total) | reading |
|---|---|---|---|---|
| base | none | TARGET_MET, scope=30/30 | K all OK; miss=6 (E01,E03–E07) | baseline |
| v1 widen past EOF | anchor `…,105-200` (pin = 112 lines) | scope=20/30 missed scope:K03…K12, TARGET_MISSED | K all OK; miss=5 | draft lacks EOF clause (D1) |
| v2 narrow below K12 | `…,69,104` | scope=29/30 missed scope:K12 | K12 MISS | both fail |
| v3 narrow below K08 | `54-55` | scope=29/30 missed scope:K08 | K08 MISS | both fail |
| v4 drop basename | `lines 33-34,…,105` | scope=20/30 (K03…K12) | K03…K12 no-name | both fail |
| v5 reversed range | `…,105-104` | scope=29/30 missed scope:K12 | K12 OK | reversed range: checkers disagree (D3) |
| v6 identifier prefix | `OldConfigWatcher.cpp:…` | TARGET_MET, scope=30/30 | K03…K12 no-name | counter lacks boundary (D2) |
| v7 E rows as `file:N-N` | E01,E03,E04,E05,E06,E07 cell 4 → `file:N-N` | TARGET_MET (K-only) | rows=33 covered=33 miss=0 OK | draft skips malformed pins (D4) |
| v8 duplicate S383 | first S383 narrowed to `1-2`, second (original) appended | TARGET_MISSED: source_cell K03…K12, scope K03…K12, new_rows 7/8 | K rows OK; miss=6 (E only) | draft last-wins on duplicate id (D5) |

Each registry mutant fails the scope legs as the task required: widened-past-EOF (v1), narrowed below a K row (v2, v3), dropped basename (v4). The counter shows `scope:<id>` legs for each.

### (4) Could the r55 counter (quality/counters/c1-r55-kbd-entry.py at 63f48dc1) have caught K14/K17?

Run: `python3 -I c1r55.py --repo $LANE --rev 63f48dc1… --work $W/cr55b` → `MADO_KBD_ENTRY: rev=63f48dc1… rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none` (receipts/c1-r55-counter-63f48dc1.out). So it says green on an entry with two K rows and five E rows that the scope rule fails.

What it lacked, read from the code (`grep` of c1r55.py):
- No leg reads registry cell 6 (the anchor). `source_ok` reads only cells 1 (URL) and 7 (status); `count_new_rows` reads cells 3, 7, 8, 10. Its `anchor:<id>` leg is the entry's own `<pin>:<line>` cell, not the registry anchor, so the name collides and does not test coverage.
- No locator parser and no concept of a line covered by a range.
- It evaluates only the 18 K rows and 6 H rows (`rows=18/18 hosts=6/6`); the 14 E rows are outside it, so E04, E05, E08, E11, E14 (the five other draft misses at r55) could never be seen.
Adding a K-row registry-anchor leg (the r56 `scope_covers`) would have caught K14 and K17. Covering the E rows would also have been needed to catch the five E rows.

### (5) Review of the draft criterion text (w1/R56RevQuality/criterion.md)

Defects, with the input that shows each and a severity:

- D1 (weakens the criterion): no length clause. Input: v1 (`ConfigWatcher.cpp:…,105-200`). Draft passes K03–K12; the counter's scope leg fails 10 rows. Fixed in corrected text, clause 6.
- D2 (weakens the counter): identifier boundary. The criterion says NAME is "not preceded by an identifier character"; `scope_covers` only does `find(basename + ":")`. Input: v6 (`OldConfigWatcher.cpp:…`) → counter TARGET_MET, draft fails. No current r56 row is affected (both agree on all 71 rows). Fixed in criterion clause 3; the counter needs the same test.
- D3 (weakens the criterion): "includes N" is undefined for reversed ranges. Input: v5 (`105-104`): counter fails K12, draft passes it. Fixed in corrected clause 4 (M < N covers nothing); the draft checker's `min/max` must change.
- D4 (weakens the criterion): evidence rows whose fourth cell is not `<file>:<N>` are not counted. Input: v7 (six r56 E rows written `file:N-N`) → draft `rows=33 covered=33 miss=0 verdict=OK` while six quoted lines remain uncovered. Fixed in corrected scope paragraph (`reason=malformed-pin`).
- D5 (weakens the criterion): no uniqueness clause; the draft's dict is last-wins. Input: v8 (two S383 rows) → draft passes K03–K12, counter fails source_cell/scope/new_rows. Fixed in corrected clause 1.
- D6 (weakens the declared limits; the claim is false): "a directory-qualified name such as legacy/ConfigManager.cpp cited as ConfigManager.cpp reads MISS". Both checkers PASS it: `scope_covers('legacy/ConfigManager.cpp:776','ConfigManager.cpp',776)` → True; `covers(...)` → (True, '776'), because `/` is not an identifier character. Corrected limit: identity is by basename; the directory is not checked.
- D7 (blocking for any r56 claim that 107 holds): r56 E rows E01, E03, E04, E05, E06, E07 fail under the draft's "any row class" and under the counter's own `scope_covers`. The frozen r56 leg is K-only, so `scope=30/30` is correct for K rows and must be reported as K-only. Fix path in the corrected text: a supersession row with a widened anchor and a re-cite, logged in the round lesson. The lane is frozen; no edit was made.
- D8 (cosmetic): tab after a comma (`10,\t20`) is accepted by the draft and rejected by the counter. Corrected clause 4 allows one optional space only; the draft's `\s*` should be narrowed to match.
- D9 (cosmetic): the criterion's receipt paths (`receipts/anchor-cover-r55-63f48dc1.out`) live at `.ufo/waves/round-56/w1/R56RevQuality/receipts/`, not beside `round-56/receipts/`. The r55 receipt reproduces byte-identical per row (diff of the ANCHOR_COVER lines is empty).

Declared limits in the corrected text: the anchor text is read, not the upstream statement; identity by basename; a rename reads MISS; `eof=unchecked` where no `pin <path>` is named; an entry with no evidence rows reads FAIL.

### Corrected criterion

Full text: receipts/../criterion-107-corrected.md (in this directory). It adds: uniqueness (clause 1); malformed fourth cell is a violation, never skipped (scope); bounded identifier prefix (clause 3); M < N covers nothing (clause 4); length bound against the named pin, with `eof=unchecked` where no pin is named (clause 6); corrected declared limits (D6). Mapping from mutants to clauses: v1 → 6; v5 → 4; v6 → 3; v7 → scope paragraph; v8 → 1. The corrected text is not executed by any checker; the mapping is by reading the rule against the mutants, not by running a fixed checker.

Recommendation: criterion 107 may land with the corrected text, but the r56 entry must not be reported as passing it. Either (a) land it with an explicit exception list naming E01, E03, E04, E05, E06, E07 for r56 and a supersession plan, or (b) scope it to K rows for r56 and say so in the declared limits. Option (b) would repeat the frozen counter's blind spot that M56-1 was about; (a) is the one consistent with "any row class".

## Commands, deliverables, checks not run

- Tools: none installed; read-only git plus python3 -I scripts in scratch. No pacman/uv/npm activity.
- Host: no host reads (no hyprctl, no ~/.config access). Not relevant to this seat.
- Not verified:
  - The variant-positive and variant-negative receipts (`anchor-cover-variant-*.out`) were inspected for content only; I did not regenerate them. The negative receipt's K13/K14 misses are consistent with the rule.
  - I did not count how many r56 registry anchors carry a named `pin <path>` token; the corrected length clause reads `eof=unchecked` for any that do not. Not checked.
  - The corrected 107 text was not implemented as a checker; its claims are from reading the rule against the eight mutants.
  - The directory-collision case (same basename in two upstream directories) is reasoned from the code, not tested on a live pair of files in the lane.
- Deliverables: this report; receipts/ (replay.py, replay-r55.out, replay-r56.out, draft-r55.out, draft-r56.out, c1-r55-counter-63f48dc1.out, c1-r56-counter-28fc86.out, mut.py, mut-shas.txt, cnt-*.out, drf-*.out); criterion-107-corrected.md.
