# ScrScorecard — round 48 w1: SCORECARD Round 48 section draft, README index row and Frontier bullet

STATUS: COMPLETE. Draft: `.ufo/waves/round-48/w1/ScrScorecard/draft.md` (19,589 B; three copy blocks:
SCORECARD section 6,908 B, README index row 911 B, README Frontier bullet 1,120 B). No file outside the seat dir was
touched; `SCORECARD.md`, `corpus/README.md`, `corpus/SOURCES.md`, the counters and the entry are the L1's to write.
Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Placeholder census at hand-off: 43 distinct tokens, 50 occurrences,
every one routed in §4 (checked by a script, scratch removed after the run).

## 1. Shape taken (and where it was read from)

| Element | Template | Insert point at base |
|---|---|---|
| section head + registration paragraph | `SCORECARD.md:2654-2656` (Round 47) | after `SCORECARD.md:2697` (file is 2697 lines; the block appends) |
| claim table (4 columns: Claim / axis, Before -> after, Counting command, Self-verdict) | `SCORECARD.md:2658-2661` | — |
| `Separable:` paragraph | `SCORECARD.md:2663` | — |
| `### Capabilities (round 48)` table (4 columns) | `SCORECARD.md:2665-2669` | — |
| `### Sources, saturation, planned` paragraph + axis publication line | `SCORECARD.md:2671-2675` | — |
| `### Errata (round 48)` append-only block | `SCORECARD.md:2677-2692` (the Round-47 E1-E6/N1 block) | — |
| `### Planned (round 49; intent only)` | `SCORECARD.md:2693-2697` | — |
| README index row (3 columns: Note, Holds, Sources) | `corpus/README.md:75` (round-47 row) | new last row of the table, after `:75`, before the blank line at `:76` |
| README Frontier bullet | `corpus/README.md:110` (round-47 bullet) | first bullet under `## Frontier` (`:108`), above `:110` |

## 2. Anchors measured while drafting (all read-only, all at `579f694`)

| Fact | Command | Result |
|---|---|---|
| the C1 "before" tool exists and passes | `python3 -I tools/mado-terminal.py --selftest` | `MADO_TERMINAL_SELFTEST: 43/43 passed`, exit 0 |
| registry size / top | `grep -c '^\| S[0-9]' corpus/SOURCES.md` | `276`, tops `S339` |
| C2 entry absent at base | `git cat-file -e 579f694:corpus/knowledge/xkb-keymap-compile-r48.md` → rc `128`; `git grep -q xkb-keymap-compile 579f694 -- corpus/` → rc `1` | absent (the C2 counter's precondition holds) |
| C1 counter absent at base | `git cat-file -e 579f694:quality/counters/c1-r48-terminal-cache.py` | rc `128` |
| the warm-cache open line | `git grep -n 'warm-cache path' 579f694 -- corpus/README.md` | `:110` |
| the XKB-compile open line | `grep -n 'XKB compile itself' corpus/knowledge/hyprland-input-devices-r46.md` | `:69` |
| the cache paragraph C1 replaces | `grep -n 'Cache (out of contract)' tools/mado-terminal.py` | `:82` (paragraph `:82-85`) |
| duplicate-URL census at base | `awk '$2=="W04"' .ufo/waves/round-48/receipts/census-before.txt \| wc -l` | `17` |
| no assimilation theme | `ls merge` | `ls: cannot access 'merge': No such file or directory` |
| Frontier is prepend-only | `git diff -U1 1001bda 0c699605 -- corpus/README.md` | one `+` index row, one `+` bullet, one `+` blank, zero `-` content lines |
| capability rows per round | section split over `SCORECARD.md` | rounds 39-47: exactly 1 each |
| axis publication parser tokens | `sed -n '60,68p' quality/check-axis-scores.py` | `navigation (\d+)/(\d+)`, `calibration resolved-active (\d+)/(\d+)`, `operability selftest (\d+)/(\d+)` |
| D4 locator correction | `awk 'NR>=149&&NR<=151{print NR": "$0}' corpus/knowledge/terminal-route-r17.md` | `:149-150` hold the `--dir=` sentence ("… is valid at" / "launch time. The helper is not run."), `:151` is blank → the r47 Limits `:150-151` is one low |
| script anchors used in the draft | `sed -n '1179p;179,182p;217,220p' .ufo/waves/round-47/fetch/xdg-terminal-exec`; `grep -n save_cache` | `:1179` the `XTE__CACHE_ENABLED && read_cache` test; `gen_hash()` `:179-215`; `read_cache()` `:217-298`; `save_cache()` `:300`; the background save `:1455-1458`, `save_cache "$1" &` at `:1457` |

## 3. Placeholders routed (43 in the blocks, all in the draft's §4 fill map)

- C1: `<C1-BEFORE-LINE>` `<C1-BEFORE-RC>` `<C1-AFTER-LINE>` `<C1-AFTER-RC>` `<C1-VERDICT>` `<CTL-C1-N>`
  `<SELFTEST>` `<C1-COLD-CLAUSE>` `<LIVE-RECEIPT>` → `receipts/c1-{before-base,after-data}.txt`,
  `receipts/ctl-c1.txt`, `w1/ExecCounterC1/`, the committed live cache receipt.
- C2: `<C2-VERDICT>` `<CTL-C2-N>` `<XKB-LIVE-RECEIPT>` `<NEG>` `<ROWS>` `<TOP>` `<TIERS>` → `receipts/c2-*.txt`,
  `receipts/ctl-c2/`, `w1/ExecXkbLive/receipts/`, `w1/ScrRows/rows.md`.
- Registration/data: `<REG-SHA>` `<DATA-SHA>` `<W1-SEATS>` `<W2-SEATS>` `<SEP-POINTER>`.
- Sources/lesson: `<DUP-ROWS>` `<REJ-ROWS>` `<W04-AFTER>` `<IDGUARD>` `<QUAR>` `<CT-PROP>` `<CT-LANDING>`
  `<CT-CRIT>` `<M48-M>` `<Q-LO>` `<Q-HI>`.
- Round-47 closure slots: `<D1>` `<D2>` `<D3>` `<R3>` `<R4B>` `<H12>` `<XM>` `<F14>` — each states done+pointer or
  `open`; an `open` keeps the defect on round 49's Planned list.
- Axis: `<NAV>` `<CAL>` `<OPS>` from `receipts/axis-data.txt` (must equal what `quality/check-axis-scores.py`
  re-derives at the published revision).

A leftover `<TOKEN>` in the axis line is not cosmetic: the gate's regex needs `\d+/\d+`, so a placeholder there is a
`NOT-PUBLISHED`/`STALE` mismatch, not a pass.

## 4. Decisions taken (with the evidence that made them)

1. **One capability row, not two.** The draft first carried an XKB row; it was removed because `SCORECARD.md:209`
   admits a row only for a capability demonstrated *running*, and rounds 39-47 each carry exactly one (counted). The C2
   entry enters through the README index row, as in every prior round.
2. **Frontier bullet is prepend-only.** Round 47 added its bullet with a `+` line and no `-` line
   (`git diff -U1 1001bda 0c699605 -- corpus/README.md`), so the round-48 bullet answers the open items at
   `corpus/README.md:110` ("the warm-cache path") and `:112` ("the XKB compile itself") in its own "Still open" list
   rather than rewriting them. The draft's §5 states this as an invariant.
3. **The errata block is one line (D4) and names a seat owner.** Round 47's errata section exists because six routed
   round-44 items were re-confirmed; round 48 routes one (D4), and its sweep of every other
   `terminal-route-r17.md` locator is `w1/ScrErrataD4`'s. The draft supplies the located line and defers final wording
   instead of duplicating another seat's artifact.
4. **Line references were corrected, not copied.** `claims.md` gives `:1455` for the cache save; the pin has
   `save_cache "$1" &` at `:1457` inside the `:1455-1458` block, so the draft cites the range and the call separately.
   `gen_hash()`/`read_cache()` bounds (`:179-215`, `:217-298`) were confirmed against the pin's function braces.
5. **`cmd=` and HOME unset sit in the capability row, not a new claim.** They are round-47 routed items
   (`w2/CritC1Explain.md`, closure D1) carried into the frozen contract, so they are part of what C1's row describes,
   with the closure slots in Sources naming the receipts.

## 5. Invariants handed to the L1 (draft §5, condensed)

1. No `<…>` survives the commit; in the axis line a leftover is a gate failure.
2. The round-48 axis publication must remain the **last** unquoted "Axis table re-derived at" in the body
   (`quality/check-axis-scores.py` takes the last one, 2000-character window, and skips it when preceded by a quote or
   backtick) — a later mention must be backticked, and a mismatch is repaired by re-deriving, never by republishing an
   older revision's fractions.
3. Append-only: `SCORECARD.md:2654-2697`, `corpus/README.md:75`, `:110` and `:112` are not edited.
4. No `|` inside a cell (sources/README tables split on the pipe); the `cache=` enum appears as `absent\|hit\|…`.
5. Quotes stay ≤ 25 words with a computed `file:line`; claim-table numbers are receipt lines, not reconstructions;
   live receipts stay shape-only (no titles, no device names, no home listings).
6. A claim whose separability receipt is missing publishes no verdict (round-44 N1 is the precedent for a row that gave
   a pointer instead of a value — do not repeat it).

## 6. Out of scope (untouched, and by whom)

- `SCORECARD.md` and `corpus/README.md` themselves (L1 integration); `LOG.md`'s Round 48 entry (not this seat); the
  counters, fixtures, entry, SOURCES rows, lesson, QUALITY criteria, PROVINCE line (their own seats).
- No verdict is asserted: `<C1-VERDICT>`/`<C2-VERDICT>` and every closure slot belong to the seats and the post-w1 runs.
- No host probe beyond the read-only selftest and `git`/`grep` reads; no `xdg-terminal-exec` run, no terminal launched,
  no compositor verb, no package transaction. Tool installs: none. Scratch `/fast/scratch/hyaku/mado-r48/ScrScorecard/`
  held only the structure checker and was removed.
