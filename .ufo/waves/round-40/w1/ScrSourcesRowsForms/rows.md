# Registry rows for C2 — draft (round 40, w1, seat ScrSourcesRowsForms)

Draft only: the L1 is the integrator. Nothing here is committed. Schema = the lane's 11 columns
from `corpus/SOURCES.md` `## Registry`, verified against `CORPUS.md` § SOURCES.md "Shape":
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.
No cell contains `|`.

## Id placeholders

The registry at HEAD holds 214 rows, ids S001..S277, no duplicate id, no 11-column defect
(`corpus/SOURCES.md`). Next free = S278, then S279. This draft uses **`S278`** for the new code
row and **`S279`** for the new own-work row as *placeholders*: the L1 assigns the next free ids and
rewrites both cell 1 values and every cross-reference (the two used-by lists, the `## Gate` lines,
the entry's `source:` lines) in one move. A partial id rewrite breaks counter clause c.

## FINDING — the bare commit URL collides with held row S180 (clause e)

`corpus/SOURCES.md:192` already registers the *same file at the same bytes*:

```
| S180 | Hyprland v0.56.2 CCssGapData parser — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp | code | A | Four-sided gap parsing used by legacy workspace-rule gapsin and gapsout | src/config/shared/complex/ComplexDataTypes.hpp:80-120 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807, 6116 B | Maps one to four integer values to CSS-like top/right/bottom/left gaps; the default branch warns and constructs from the first four tokens | mined | 2026-10-23 | on-release | corpus/knowledge/workspace-rules-r27.md, tools/mado-wsrules.py |
```

Measured with the frozen counter's own clause-e code (`loc = cells[1].split()[-1]`,
`same == [i]`) over all 214 registry rows, a new row whose cell 2 ends in that bare commit URL
yields `same == ['S180', 'S278']` → **clause e fails**. Two sibling seats reached the same
conclusion independently (`.ufo/waves/round-40/w1/ConnSourcePatterns.md` F7;
`.ufo/waves/round-40/w1/ExecFetchComplexTypes/quotes.md:241-252`).

So the new row keeps the same *source* but must denote it by a location token no other row ends
in. Three resolutions, primary first.

### Resolution used by (a): the release-tag URL of the same tree

`https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/config/shared/complex/ComplexDataTypes.hpp`
— measured this seat: `HTTP=200 SIZE=6116`, sha256
`95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807`, i.e. **byte-identical to the
pinned-commit receipt** (`.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin`). The host
reports `hyprland 0.56.2 commit efb50993780079460b0cbed1363e2166a2de1d9f tag v0.56.2`, so the tag
URL and the commit URL denote one tree. This token has zero other users in the registry
(measured). Caveat the L1 must record: it is the same *file* as S180, split by scope (S180 = gap
parser :80-120; the new row = the serialisers), not a second source.

## (a) NEW row — Hyprland ComplexDataTypes.hpp serialisers

```
| S278 | Hyprland v0.56.2 ComplexDataTypes.hpp custom-value serialisers — https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/config/shared/complex/ComplexDataTypes.hpp | code | A | The native serialisation of the custom option values getoption prints (gradient colours and angle, CSS gap expansion, font-weight names) | src/config/shared/complex/ComplexDataTypes.hpp:69-77,94-135,154-161 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807, 6116 B; receipt .ufo/waves/round-40/fetch/complex-data-types-efb5099.bin | Prints a custom value from the compositor's own serializer: colours as lowercase unpadded hex each followed by a space, then the angle as Ndeg, gaps as four integers, font weight as its integer | mined | 2026-10-25 | on-change | corpus/knowledge/hyprctl-getoption-native-forms-r40.md |
```

Cell provenance, each read from the committed receipt bytes (sha256 above, 6116 B, 178 lines):

| cell | grounding |
|---|---|
| source | tag URL verified `HTTP=200`, 6116 B, sha256 identical to the commit-pinned receipt (this seat, 2026-10-25); last token unique across the registry (measured) |
| kind / tier | `code` / `A` — pinned source code is A for this scope per CORPUS.md tier definitions |
| anchor | `:69-77` `CGradientValueData::toString` — `std::format("{:x} ", c.getAsHex())` :72, `std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI))` :75; `:94-135` `CCssGapData::parseGapData` :94 (1/2/3/4-token switch, default branch warns) and `toString` :133-135 `"{} {} {} {}"`; `:154-161` `CFontWeightConfigValueData::toString` :154-156 and the `WEIGHTS` name→int map :158-161 |
| teaches | the three custom-form text shapes the entry compares against (gradient colour + angle, gap 4-tuple, weight integer) |
| status | `mined` — cell 11 names the C2 entry (clause c) |
| opened | `2026-10-25` — new id (clause c) |
| recheck | `on-change` — the row is a conversion rule, not a release note; recheck when the source file or the pinned host changes |

Alternative spellings, for the L1's decision (not the draft):

- **A1 — bare commit URL.** Fails clause e as measured above. Do not use.
- **A2 — drop this row, extend S180 instead.** Then S180's cell 11 grows exactly as in
  "S180 (optional)" below, and the counter's `len(new_ids) >= 2` needs a *different* new
  non-own-work row. The nearest genuinely new location that supports the entry is
  `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataType.hpp`
  — measured this seat: `HTTP=200`, 481 B, sha256
  `e7fee893be361e6e11102aeac549dd8ed527dd2c0e1a5a879f717b4c8222882e`, holding
  `enum eConfigValueDataTypes : int8_t` with `CVD_TYPE_GRADIENT/CSS_VALUE/FONT_WEIGHT` (:7-11) and
  `virtual eConfigValueDataTypes getDataType() = 0` (:18). It supports only the type-tag half of
  the claim and has **no committed fetch receipt yet**, so clause d would need one landed first.

## (b) NEW row — own-work live census receipt

```
| S279 | mado live getoption census - tools/mado-options.py --live over the host tree and the compositor's replies (measured on this host) - .ufo/waves/round-40/fetch/S279.receipt.txt | own-work | A | How the host's 70 declared option keys answer hyprctl getoption -j and how the native model labels them (native form, agreement class, declarers) | receipt lines tool sha256 TOOLSHA (the sha256 of tools/mado-options.py at the data commit), forms and labels in .ufo/waves/round-40/fetch/S279.receipt.txt; Hyprland v0.56.2 efb5099, hyprlang 0.6.8, 70 declared keys, one hyprctl getoption -j per key, config root parsed read-only | The host answers the 70 declared keys in four native forms (int=44 float=5 str=8 custom=13) and the native model labels them agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0 | mined | 2026-10-25 | on-change | corpus/knowledge/hyprctl-getoption-native-forms-r40.md |
```

- `TOOLSHA` is the **tool sha placeholder**: the census receipt's `tool sha256` line must be
  filled by the L1 with the sha256 of `tools/mado-options.py` at the data commit (clause h reads
  that literal hash out of the receipt). Current tip tool bytes hash to
  `461f8c3c245bdfb6dcaac068a5ab378326c75dc91992b8012f9ca0e5019fb03a` — not the data commit's tool,
  so it must be re-derived after the tool lands.
- Cell 2 ends in the receipt path (S219 shape), so clause e's location token is
  `S279.receipt.txt` — zero other users in the registry (measured). The placeholder keeps that
  true only if the L1 names the landed receipt after the id it assigns; if it picks a different
  file name, cells 2, 6 and the `## Gate` line must change together.
- The two counts are re-derived, not copied: `int=44 float=5 str=8 custom=13` from
  `.ufo/waves/round-40/c1/native-capture.jsonl` (70 records; form histogram computed by this seat
  as `{'int': 44, 'float': 5, 'custom': 13, 'str': 8}`); `agreement=62 agreement*=8 mismatch=0
  config-only=0 live-default=0` from `.ufo/waves/round-40/w1/ExecLiveCensus/census-receipt.txt:15`.
  Both sums are 70 (44+5+8+13 and 62+8+0+0+0), which clause h requires to agree.
- **Landing dependency:** those bytes currently live only at
  `.ufo/waves/round-40/w1/ExecLiveCensus/census-receipt.txt`, whose line 6 is
  `tool sha256 <TOOLSHA>`. Clause d/h need the receipt under `.ufo/waves/round-40/fetch/`, so the
  L1 lands a copy there with the placeholder substituted, under the name cell 2 and cell 6 state.

## (c) used-by EXTENSION for held rows S162 and S173

Rule: cells 1-10 stay byte-equal to the BASE row (clause c); only cell 11 grows. Verified:
`git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff 9fc511ddce708327377161202f358ce37dc266ba --
corpus/SOURCES.md` prints nothing, so both rows are byte-identical to BASE and the cells quoted
below are the BASE cells verbatim.

### S162 — old → new cell 11

old:

```
corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md, corpus/knowledge/workspace-rules-r27.md, corpus/knowledge/config-option-table-r39.md
```

new:

```
corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md, corpus/knowledge/workspace-rules-r27.md, corpus/knowledge/config-option-table-r39.md, corpus/knowledge/hyprctl-getoption-native-forms-r40.md
```

Full replacement row (cells 1-10 byte-for-byte from BASE, only cell 11 changed):

```
| S162 | Hyprland ConfigManager.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp | code | A | Hyprlang-era legacy windowrule keyword handlers, named special-category reconstruction, and reload traversal | src/config/legacy/ConfigManager.cpp:419-451,590-623,893-968,2016-2093 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b, 90963 B | Shows callback parsing, name-keyed category consumption, and local reload call sequence; does not establish Hyprlang block grammar or engine precedence | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md, corpus/knowledge/animation-table-r26.md, corpus/knowledge/workspace-rules-r27.md, corpus/knowledge/config-option-table-r39.md, corpus/knowledge/hyprctl-getoption-native-forms-r40.md |
```

### S173 — old → new cell 11

old:

```
tools/mado-binds.py, corpus/knowledge/config-option-table-r39.md
```

new:

```
tools/mado-binds.py, corpus/knowledge/config-option-table-r39.md, corpus/knowledge/hyprctl-getoption-native-forms-r40.md
```

Full replacement row (cells 1-10 byte-for-byte from BASE, only cell 11 changed):

```
| S173 | Hyprlang v0.6.8 expression evaluation — https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp | code | A | Hyprlang RHS `{{…}}` expression parsing relevant to bind config values; not bind-table semantics | `src/config.cpp:619-667,755-827,983-986 @ 3a1c1b25b059dae2c6bbc46991562ba1158d125c, sha256:fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e, 43049 B` | Documents the single-operator float evaluator, variable lookup, escaped expression starts, default result formatting, and parse-error propagation | mined | 2026-10-23 | on-release | tools/mado-binds.py, corpus/knowledge/config-option-table-r39.md, corpus/knowledge/hyprctl-getoption-native-forms-r40.md |
```

### S180 (conditional) — old → new cell 11, only if the entry cites S180

The entry's gap-expansion claim reads the same bytes S180 registers. If the entry's `source:` lines
include S180, clause c then also requires S180's cell 11 to name the entry:

old:

```
corpus/knowledge/workspace-rules-r27.md, tools/mado-wsrules.py
```

new:

```
corpus/knowledge/workspace-rules-r27.md, tools/mado-wsrules.py, corpus/knowledge/hyprctl-getoption-native-forms-r40.md
```

Cells 1-10 of S180 stay byte-equal (same text as quoted in the FINDING above); cell 9 `2026-10-23`
and cell 10 `on-release` do not move — a re-opened row keeps its cells.

Each cell-11 change is logged old→new in `corpus/lessons/round-40.md` (SOURCES.md rule 2). The
Gate-draft seat owns that text; this seat only supplies the strings.

## Placement

Append both new rows at the end of `## Registry`, after the `S220` line (currently line 226) and
before the blank line 227 that precedes `## Paths`. The registry is not id-sorted inside an append
block (S277 sits above S218-S220), so ascending id order in the new block is consistent.

## Clause map (what the L1 must satisfy with these rows)

- **c** one row per cited id, 11 cells, status `mined`, cell 11 names
  `corpus/knowledge/hyprctl-getoption-native-forms-r40.md`; new ids carry opened `2026-10-25`;
  held ids keep cells 1-10 byte-equal → (a), (b), (c) above.
- **e** new-id location unique → `ComplexDataTypes.hpp` is *not* usable as the location token
  (S180 holds it); the tag URL used in (a) and `S279.receipt.txt` in (b) have zero other users.
- **d** per cited id, `GATE <id> receipt=.ufo/waves/round-40/fetch/… sha256=<64 hex> quote="<3-25
  words>"` with the quote inside the receipt's normalized text. Receipts already present in
  `fetch/` and hash-matched to the held rows' own anchors:
  - S162 → `config-manager-efb5099.bin`, sha256 `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` (= S162 cell 6);
  - S173 → `hyprlang-config-v0.6.8.bin`, sha256 `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e` (= S173 cell 6);
  - S278 → `complex-data-types-efb5099.bin`, sha256 `95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807`;
  - S279 → the census receipt path landed per (b).
- **h** exactly one new cited row with kind `own-work` → S279 is the only one, and its receipt
  must carry the tool sha plus both count lines, repeated verbatim in the entry.

## Validation run by this seat (on a scratch copy, /tmp)

Scratch: `corpus/SOURCES.md` copied to a `mktemp -d` dir, S162/S173 cell 11 replaced by the rows
above, the two new rows inserted after `S220`; parsed with the frozen counter's own `registry()`
code and with the CORPUS.md census commands. Results:

- rows 214 → 216; both new rows parse to exactly 11 cells; no `|` inside any cell.
- S162, S173: `cells 1-10 equal to base: True`, cell 11 strictly longer; `status mined`.
- S278, S279: 11 cells, `status mined`, `opened 2026-10-25`, cell 11 ends in the entry path.
- clause-e check: `S278 → [S278]` only (tag URL), `S279 → [S279]` only; the bare commit URL
  measured `['S180', 'S278']` (the finding above).
- CORPUS.md census on the scratch copy: malformed-row count 0, duplicate ids none, tier/status/kind
  enums valid, no tier inflation. The "mined rows whose used-by paths do not exist" sweep flags
  `corpus/knowledge/hyprctl-getoption-native-forms-r40.md` — expected, it does not exist yet; it
  must exist at the data commit.

## Open dependencies (not this seat's to close)

1. `corpus/knowledge/hyprctl-getoption-native-forms-r40.md` must exist at the data commit (every
   cell 11 above names it; clause f needs its single column-zero `corpus/README.md` index row).
2. The census receipt must be landed under `.ufo/waves/round-40/fetch/` with `TOOLSHA` substituted.
3. The entry's first 20 lines need `source:` lines for its cited ids (≥4 distinct, clause b), plus
   `verified-at: 2026-10-25` and a `recheck:` value.
4. The L1 must decide the S180 overlap (tag URL in (a), or A2) and record it in the round lesson —
   the registry should not silently hold two rows for one file without that note.
