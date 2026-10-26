# ScrEntryB - C2 entry draft (round 43, w1)

Status: **complete draft**, self-checked against `PRED-C2-r43` in a scratch clone of the lane.
The lane tree, the frozen counters, the fetch receipts and the shrink-wrapped controls were not
modified; every artifact below is inside this seat directory.

## Deliverable

- Draft entry: `.ufo/waves/round-43/w1/ScrEntryB/hyprland-gkeep-geometry-r43.md`
  (70 lines, sha256 `a429672c7f33ea1b4a5c06a3c36ae72f00416279dd0ca3470a3b065dc4bbd2b5`).
  Structure: title (carrying the README holds sequence "What determines the size of the host's
  gkeep window, end to end:"), `Lane:` line, `ground:`, `assimilated-from:`, ten `source:` lines
  (S290-S299) and one `verified-at: 2026-10-26` / one `recheck: 30d - ...` inside raw lines 1-17;
  then the 6-row decision table, five short evidence sections with exactly one claim line per id
  (quote + `receipt:line` locator, tagged OBS/INF/UNK), and the three census lines.
- `quotes.tsv` - id, receipt, sha256, locator line, word count, kind, quote (10 rows).
- `gate-lines.txt` - the 10 `GATE` lines for `corpus/lessons/round-43.md` `## Gate` plus the
  `ADMIT`/`REFUSE` proposal (tested bytes, not prose).
- `registry-rows.md` - the 10 registry rows exactly as tested (11 cells, status `mined`,
  opened 2026-10-26, used-by = the entry).
- `readme-row.md` - the coverage-map index row, tested with `quality/check-index-rows.py`.
- `c2-fixture-check.txt` - the full counter run in the scratch clone (target and base control).
- `verify-quotes.py`, `verify-quotes.txt` - re-opens the ten receipts and recomputes every locator
  with `PRED-C2-r43`'s own `quote_at`.

## Behaviour of the predicate on the draft

Simulated the L1 integration in a `--no-hardlinks` clone of the lane at
`5add5b45a65ddaa18fad00c6afa9dbfda29ee0b0` (clone toplevel verified equal to the clone path;
fixture commit `a55c92e6c672fde5bc5648f2ca5cf971ef8815bc`; scratch tree deleted after copying the
transcript): append the ten rows, create `corpus/lessons/round-43.md` `## Gate` with the
ADMIT/REFUSE and ten GATE lines, add the README row.

```
PRED-C2-r43 hyprland-gkeep-geometry-r43.md clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1
PRED-C2-r43: admitted=1/1 verdict=TARGET_MET rev=a55c92e6c672fde5bc5648f2ca5cf971ef8815bc
exit=0
```

Base control in the same clone: `rev=a35cfdf... clauses=a:0 ... i:0 admitted=0 verdict=TARGET_MISSED exit=1`.
Index gate on the same fixture: `MADO_INDEX_ROWS: rev=HEAD rows=60 errors=0 warns=3`, the three warns
all pre-existing (`getprop-*`, `drift-*`, `rule-attribution-r24` globs); no `holds-no-overlap` warn
for the new row. Quote verifier: `VERDICT: PASS` (10/10 sha match, 10 distinct receipts and quotes).

## Findings

**F1 - S291/S296 collide with existing rows (supports clause e; attacks the seat context's id plan).**
`corpus/SOURCES.md:167` S155 and `:170` S158 already carry the exact raw URLs of
`WindowRuleApplicator.cpp` and `HyprCtl.cpp` at commit `efb5099`, with the same sha256 as the round-43
fetch pins. Minting S291/S296 with the same URL makes the registry location of two rows identical,
which clause e rejects (`same == [i]` fails; observed `same=['S155','S291']` and
`['S158','S296']` on the first fixture run, exit 1). The rows I propose therefore give S291/S296 the
pinned receipt path (`.ufo/waves/round-43/fetch/...`) as their location token and keep the commit +
sha256 in the anchor cell; clause e then holds and no duplicate URL is added. The alternative
(cite S155/S158 directly, no new ids) is viable for the predicate but contradicts the frozen
registration's "rows S290-S299 are opened this round", so I did not take it.

**F2 - locators re-derived, round-42 prose defects confirmed (supports the entry's own locators).**
`Hyprland-HyprCtl.cpp` prints `size` from `GEOMETRIC_GOAL` in the JSON branch's argument list at
`:427-428` (the `"size"` key itself is `:395`) and in the text branch at `:448`;
`Hyprland-RegexMatchEngine.cpp` has the `negative:` prefix at `:7-9` and `FullMatch` at `:16`.
The quotes and their locators were recomputed by the counter's `quote_at`, not typed from the round-42 prose.

**F3 - the honest state is UNK, and the wave's live run agrees (supports the entry's UNK rows).**
The pinned census (`host-clients-r43.json`, 4 mapped clients, none floating, none gkeep) licenses no
rendered-geometry claim. The wave also holds an untracked live run
(`.ufo/waves/round-43/receipts/live-geometry-host.txt`) of the C1 tool over the host, reporting
`clients=4 matched=0 ... verdict=NO_MATCHING_CLIENT`. It is **not** cited in the entry: it is not a
pinned receipt (clause d requires a PINS hit for a new id) and C2 must not depend on C1's tool
(separability). It supports the UNK statement as context only.

**F4 - the 3-25 word rule forces quote choices (supports clause d).**
The natural one-call quotes `window.set_default_size(420, 500)` and `"floating": false,` split into two
whitespace tokens, below the counter's floor. S299's quote spans the two adjacent lines
(`window.set_decorated(False) window.set_default_size(420, 500)`, locator `:32` - the line where the
quote starts, not `:33` where the call sits) and S298's spans the `floating` and `size` members
(locator `:6`). Both are inside the receipt at a true locator.

**F5 - census lines are the counter's own output, not hand-typed (supports clause h).**
The three lines were recomputed by `host_census` from the three own-work receipts during the fixture
run (`h:1`); the size rule is line 4 of the config copy, `float`/`center` are `on`, the dump has four
mapped clients with `floating: false`, and the excerpt has one `set_default_size(420, 500)` and one
`application_id="org.omarchy.gkeep"` that `^(org.omarchy.gkeep)$` fullmatches.

## Known limits / open items for the L1

- The entry alone cannot be admitted: registry rows, the lesson `## Gate` and the README row are the
  L1's to publish; my tested drafts are in this seat directory. Any rewording of the rows' scope or
  teaches cells is safe for the counter (it checks shape, status and used-by), any rewording of a
  GATE quote or a claim line is not.
- The ADMIT (`gkeep-size-to-real-size-r11.md`) and REFUSE (`glyph-and-geometry-r31.md`) targets are a
  proposal; clause i only needs one admit to the entry and one refuse of a different staged file with
  >=4 distinct words. If the L1 prefers refusing `gkeep-rendered-geometry-record-r13.md` (superseded by
  its own r14), the predicate still holds.
- The entry is INF about the size a first-mapped gkeep window receives and UNK about the live result;
  it never asserts an observed 420x500 window.
- Tool installs: none. Scratch: `/fast/scratch/hyaku/mado-r43/ScrEntryB` removed after the transcript
  was copied into this seat directory; the citable receipts are the files above, not the clone.

## Seat artifacts

```
.ufo/waves/round-43/w1/ScrEntryB/hyprland-gkeep-geometry-r43.md
.ufo/waves/round-43/w1/ScrEntryB/quotes.tsv
.ufo/waves/round-43/w1/ScrEntryB/gate-lines.txt
.ufo/waves/round-43/w1/ScrEntryB/registry-rows.md
.ufo/waves/round-43/w1/ScrEntryB/readme-row.md
.ufo/waves/round-43/w1/ScrEntryB/c2-fixture-check.txt
.ufo/waves/round-43/w1/ScrEntryB/verify-quotes.py
.ufo/waves/round-43/w1/ScrEntryB/verify-quotes.txt
```
