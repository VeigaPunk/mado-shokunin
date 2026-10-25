# ScrReadmeIndex — README index row, route text and Frontier line for the C2 entry (round 40, w1)

STATUS: DONE. Draft only; no tracked file was edited and nothing outside my seat directory was
written. Leaf seat: no subagent dispatch, no background jobs, no package transaction, no
compositor verb beyond none at all (this seat ran no `hyprctl`).

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Claims read at the freeze commit
`5e7e88525cc539563de7746361b2650802e81809` (`registration.md` § C2, base
`9fc511ddce708327377161202f358ce37dc266ba`).

## Artifact

`.ufo/waves/round-40/w1/ScrReadmeIndex/index.md` (7965 B) carries, in committable form:

1. **§1 the index row** — one physical line, column zero, ``| `knowledge/hyprctl-getoption-native-forms-r40.md` ``
   with one literal space after the pipe, 3 cells, 1218 B.
2. **§2 the route text** — `### Round-40 getoption native-forms route`, modelled on the round-38
   section (`corpus/README.md:277-286`), appended after it.
3. **§3 the `## Frontier` bullet** — appended as the last bullet of the Frontier list (after the
   round-20 bullet at `corpus/README.md:175-184`, before `### Round-21 correction…` at line 186):
   native reply forms + conversions moved onto sourced ground; runtime `hyprctl keyword`
   overrides, options the host never declares and the Lua-era config stay unknown.
4. **§4 provenance table, §5 the checks run, §6 the substitutions the L1 must make.**

## What the draft asserts, and its ground

| Assertion | Ground (read by this seat) |
|---|---|
| forms `int 44, float 5, str 8, custom 13`, 70 keys | counted over the frozen `.ufo/waves/round-40/c1/native-capture.jsonl`: 70 lines, one form key each → `{'int': 44, 'float': 5, 'custom': 13, 'str': 8}` |
| labels `62 agreement / 8 agreement* / 0 mismatch` | `.ufo/waves/round-40/w1/ExecLiveCensus/census-receipt.txt:15` `labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0`; the same counts are frozen in `.ufo/waves/round-40/ctl/run-c2-controls.py:24` |
| forms/labels line formats the entry must repeat | `census-receipt.txt:14-15`; `quality/counters/c2-r40-forms-entry.py:210-224` (clause h regexes) |
| 70 declared keys, one `getoption -j` per key, `no such option`, angle inheritance `ffe68e0d 45deg` | `registration.md` § C1/§ C2 and "Provisional facts" — frozen text, not re-measured here |
| round-39 row shape and the phrase the route text narrows | `corpus/README.md:67`; "no live dump was taken this round" is that row's own last clause |
| row fidelity rules | `quality/check-index-rows.py:225-268` (`evaluate`: 3 non-empty cells, S-ids defined in SOURCES, backticked repo-relative paths must resolve) |
| column-zero single row | `quality/counters/c2-r40-forms-entry.py:226-227` (`^\| `knowledge/<entry>``) |

## Gates actually exercised (and their output)

1. Scratch row-fidelity run, `--root` mode on a `tempfile.mkdtemp` tree (draft row + SOURCES rows
   S162/S173/S278/S279 + stub note + stub `tools/mado-options.py` + stub fetch member):
   exit **0**, `MADO_INDEX_ROWS: root=/tmp/readmeindex-ev2rpy68 rows=1 errors=0 warns=0`. Tree removed.
2. `python3 -I quality/check-index-rows.py --repo . --rev HEAD` (read-only, current tree):
   `MADO_INDEX_ROWS: rev=HEAD rows=56 errors=0 warns=3` — the 3 warns are pre-existing
   (round-12/24 glob rows), so my row adds no error and the baseline is clean.
3. Row-shape metrics of the draft line: 4 pipes = 3 cells; clause-f regex matches; `row[0]=='|'`,
   `row[1]==' '`.
4. Rev-mode resolution of the Sources cell's ticks (read-only): `git cat-file -e
   HEAD:.ufo/waves/round-38/fetch/` → `TRAILING_SLASH_DIR_OK` (trailing-slash dir form, as the
   round-38 rows already use); `git cat-file -e HEAD:tools/mado-options.py` → `TOOL_OK`.
5. Cross-seat id agreement: `.ufo/waves/round-40/w1/ScrSourcesRowsForms/rows.md` § "Id placeholders"
   independently assigns `S278` (ComplexDataTypes.hpp) and `S279` (own-work census) as the next free
   ids after S277 — the pair my row cites.
6. Overlap re-run once both entry drafts landed, each used as the note text of the same scratch tree:
   `ScrFormsEntryA 0 MADO_INDEX_ROWS: root=/tmp/readmeindex-50pgdeb1 rows=1 errors=0 warns=0`,
   `ScrFormsEntryB 0 MADO_INDEX_ROWS: root=/tmp/readmeindex-j8n8wq24 rows=1 errors=0 warns=0`.

Not run, deliberately: `quality/counters/c2-r40-forms-entry.py` (the entry, the registry rows, the
lesson `## Gate` lines and the `fetch/` receipts are other seats' deliverables and none is
committed; a run now scores clause-a/b setup errors, not this draft) and `quality/check-index.py`
(needs the note to exist).

## Findings

- **F1 (blocking for the L1, not for this seat):** the row cites `S278`/`S279` as placeholders.
  `check-index-rows.py` raises `cited-s-undefined` for any S-id absent from `corpus/SOURCES.md`,
  and the C2 counter's clause c requires exactly one registry row per cited id — so the L1 must
  land the two new rows and use the ids actually assigned, consistently in the row, the entry's
  `source:` lines and the `## Gate` lines. Partial substitution breaks clause c.
- **F2:** the row's Sources cell cites `.ufo/waves/round-40/fetch/` (trailing-slash directory), the
  same form the round-38 rows use. It resolves at rev mode only once the L1 commits receipts under
  it; if the L1 lands no member there, drop the tick (it is the only path in the row that depends
  on round-40 data landing).
- **F3:** the label `MADO-R40-1` is my choice (round-39's single entry is `MADO-R39-1`); no gate
  reads it, so the L1 may substitute the label it uses in the scorecard.
- **F4:** the route section and the Frontier bullet are prose, read by no counter; they state what
  the entry and census support and repeat no count the entry does not carry (62/8/0 and 44/5/8/13
  are the census receipt's own lines).
- **F5:** the Holds cell's word overlap with the note (`check-index-rows.py` `overlap`, warn-only) was
  re-run against both landed entry drafts (`ScrFormsEntryA/entry.md`, `ScrFormsEntryB/entry.md`) as
  the note text of the scratch tree: both exit 0 with `errors=0 warns=0`, so no `holds-no-overlap`
  warn arises against either draft.

## Touched surfaces

- Written: `.ufo/waves/round-40/w1/ScrReadmeIndex/index.md`, this report
  `.ufo/waves/round-40/w1/ScrReadmeIndex.md`. Nothing else.
- `git status --porcelain --untracked-files=all -- corpus/ tools/ quality/` → empty: no tracked
  file in those trees changed. No git/jj mutating command was run. Scratch lived under `/tmp` and
  was removed.

## Out of scope / not claimed

- Not integrated: no edit to `corpus/README.md`, `corpus/SOURCES.md`, `corpus/lessons/round-40.md`
  or the entry — the L1 is the only integrator.
- No compositor read, no config-tree write, no live measurement was taken by this seat; the live
  numbers are cited from the frozen capture and the census seat's receipt, not re-derived here.

## Tools

None installed or updated (no channel used). Existing `git`, `python3` only.

Report: .ufo/waves/round-40/w1/ScrReadmeIndex.md
