# README index row, route text and Frontier line — `knowledge/hyprctl-getoption-native-forms-r40.md`

Seat `ScrReadmeIndex`, round 40 w1. Draft only: no tracked file is edited here (the L1 integrates).
Frozen claims: `.ufo/waves/round-40/registration.md` § C2. Fidelity rules read from
`quality/check-index-rows.py` (`evaluate`, lines 225-268) and from the C2 counter's clause f
(`quality/counters/c2-r40-forms-entry.py:226-227`: a line matching ``^\| `knowledge/<entry>``).

## 1. The index row (insert as the last row of the `## Coverage map` table)

Model: the round-39 row (`corpus/README.md:67`), 3 cells, one physical line, no `|` inside a cell.
The line below begins at column zero with ``| `knowledge/hyprctl-getoption-native-forms-r40.md` `` —
one literal space after the pipe, as the C2 counter's clause f requires.

| `knowledge/hyprctl-getoption-native-forms-r40.md` (MADO-R40-1, round 40; lane-authored, coverage claim C2) | The compositor's own answer to a config key, in its native forms instead of a config-only table: one `hyprctl getoption -j KEY` per declared key returns one object `{"option":…,"set":…,"<form>":…}` with form `int` 44, `float` 5, `str` 8, `custom` 13 over this host's 70 keys, and an undeclared key prints `no such option` at exit 0; the per-form conversion of a declared string (hyprlang v0.6.8 `configStringToInt` colour/bool/hex forms, Hyprland v0.56.2 gradient colours and angle, CSS gap expansion, font-weight names); the angle-inheritance rule observed here — the theme's single-colour `col.active_border` reads `ffe68e0d 45deg` because the defaults tree declared a 45deg gradient first; and the host census under that model, 62 agreement / 8 agreement* / 0 mismatch. Tool `tools/mado-options.py --live` (round-40 C1) is what takes the dump. Runtime `hyprctl keyword` overrides, options this host never declares and the Lua config era stay outside it. | `source:` S162, S173, S278, S279 in [SOURCES](SOURCES.md); tool `tools/mado-options.py`; receipts `.ufo/waves/round-40/fetch/`; recheck on-change. |

## 2. Coverage-map route text (append after the `### Round-38 request-socket bound route` block)

### Round-40 getoption native-forms route

- The compositor's own answer to a config key moves onto sourced ground: what
  `hyprctl getoption -j` returns for the 70 keys this host declares — one JSON object
  per key in a native form (`int` 44, `float` 5, `str` 8, `custom` 13) and
  `no such option` for a name the compositor never declares — and how a declared
  string is converted per form (hyprlang v0.6.8 `configStringToInt`, Hyprland
  v0.56.2 gradient colours with angle inheritance, CSS gap expansion, font-weight
  names): [native forms](knowledge/hyprctl-getoption-native-forms-r40.md). This
  narrows the round-39 table's "no live dump was taken this round"
  ([config-option-table](knowledge/config-option-table-r39.md)) for the declared
  keys only: the dump is taken through the compositor's own read verb by
  `tools/mado-options.py --live` (round-40 C1), and the host census under the
  native model is 62 agreement, 8 agreement*, 0 mismatch. Still open: runtime
  `hyprctl keyword` overrides, options this host never declares, and the Lua-era
  config surface. No config tree and no compositor state was written.

## 3. `## Frontier` line (append as the last bullet of the Frontier list, before `### Round-21 correction…`)

- Round 40 (2026-10-25) moves the compositor's own reply to a config key onto
  sourced ground — the four native forms of `hyprctl getoption -j` and their
  per-form conversions, read at the host's versions (hyprlang 0.6.8,
  Hyprland v0.56.2): [native forms](knowledge/hyprctl-getoption-native-forms-r40.md).
  It narrows, for the 70 declared keys only, the round-39 table's "no live dump
  was taken this round"; it moves no earlier Frontier bullet. Still unknown:
  runtime `hyprctl keyword` overrides, options this host never declares, and the
  Lua-era config surface.

## 4. Facts this draft rests on, and where each was read

| Fact in the draft | Ground |
|---|---|
| form counts `int 44 float 5 str 8 custom 13`, total 70 | counted by me over the frozen `.ufo/waves/round-40/c1/native-capture.jsonl` (70 lines, one form key per object): `python3 -c` counter, output `lines 70 {'int': 44, 'float': 5, 'custom': 13, 'str': 8}` |
| label counts `62 agreement / 8 agreement* / 0 mismatch` | `.ufo/waves/round-40/w1/ExecLiveCensus/census-receipt.txt:15` (`labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0`), same numbers in the frozen control fixture `.ufo/waves/round-40/ctl/run-c2-controls.py:24` |
| 70 declared keys, one `getoption -j` per key, exit 5/exit 2 semantics | `registration.md` § C1 deliverable (frozen); not re-measured by this seat |
| `col.active_border` reads `ffe68e0d 45deg` with the defaults tree's 45deg gradient first | `registration.md` "Provisional facts", host finding (frozen); not re-measured by this seat |
| row shape, 3 non-empty cells, S-ids defined in SOURCES, artifact paths resolving at REV | `quality/check-index-rows.py:225-268`; exercised on a scratch tree (§5) |
| column-zero row start, exactly one row for the entry | `quality/counters/c2-r40-forms-entry.py:226-227` |

## 5. Gate checks actually run on this draft

1. Scratch-tree run of the row-fidelity gate (`--root` mode, `tempfile.mkdtemp` under `/tmp`, removed
   after): the draft row inside a `|Note|Holds|Sources|` table, `corpus/SOURCES.md` carrying S162,
   S173, S278, S279, a stub entry note, a stub `tools/mado-options.py` and a stub
   `.ufo/waves/round-40/fetch/S279.receipt.txt` → exit 0,
   `MADO_INDEX_ROWS: root=/tmp/readmeindex-ev2rpy68 rows=1 errors=0 warns=0`. The same row measures
   4 pipes = 3 cells, 1218 bytes on one physical line, and matches the C2 counter's clause-f regex
   with column zero and one literal space.
2. `python3 -I quality/check-index-rows.py --repo . --rev HEAD` (read-only, current tree):
   `MADO_INDEX_ROWS: rev=HEAD rows=56 errors=0 warns=3` — the three warns are pre-existing
   (round-12/24 glob rows), so the gate's baseline is clean and my row adds no error by shape.
3. The C2 counter itself was **not** run by this seat: the entry, registry rows, lesson Gate lines
   and fetch receipts are other seats' deliverables and none is committed yet, so a run now would
   score clause a/b setup errors, not this draft.
4. Rev-mode path resolution for the two repo-relative ticks in the Sources cell (read-only):
   `git cat-file -e HEAD:.ufo/waves/round-38/fetch/` → `TRAILING_SLASH_DIR_OK` (the trailing-slash
   directory form the round-38 rows already use resolves under `check-index-rows.py`'s rev mode) and
   `git cat-file -e HEAD:tools/mado-options.py` → `TOOL_OK`.
5. Cross-seat agreement on the placeholder ids: `.ufo/waves/round-40/w1/ScrSourcesRowsForms/rows.md`
   § "Id placeholders" independently assigns `S278` (ComplexDataTypes.hpp) and `S279` (own-work
   census) as the next free ids after S277, the same pair this row cites.
6. Overlap re-run against both entry drafts once they landed
   (`.ufo/waves/round-40/w1/ScrFormsEntryA/entry.md`, `…/ScrFormsEntryB/entry.md`) as the note text
   of the same scratch tree: `ScrFormsEntryA 0 MADO_INDEX_ROWS: … rows=1 errors=0 warns=0` and
   `ScrFormsEntryB 0 … errors=0 warns=0` — no `holds-no-overlap` warn against either draft.

## 6. Substitution the L1 must make (the draft is not committable as-is on this point)

- `S278` / `S279` are the next free ids after S277 (`registration.md` C2: ">=2 new rows"), and the
  registry seat writes placeholders (`ScrSourcesRowsForms`: "the L1 assigns the next free ids").
  L1 MUST replace both in the row with the ids actually assigned, and they MUST equal the ids the
  entry cites (`c2-r40-forms-entry.py` clauses c and g) — an id in the row that no `## Registry` row
  defines is a `cited-s-undefined` error in `check-index-rows.py` and a clause-c failure in the counter.
- `MADO-R40-1` is my label choice (round-39's single entry is `MADO-R39-1`); if the L1 labels the
  entry otherwise, substitute it — no gate reads the label.
- The route section and the Frontier bullet are text only; neither is read by a counter, and the
  round-38 route section's own wording ("no Frontier bullet above is moved by it") is the model.
