# ScrSourcesRowsForms — registry rows for C2 (round 40, w1)

STATUS: COMPLETE (draft only; nothing committed, no tracked file edited).

## Deliverable

`.ufo/waves/round-40/w1/ScrSourcesRowsForms/rows.md` — the C2 registry draft in the lane's
11-column schema:

- **(a)** new code row for Hyprland `ComplexDataTypes.hpp` (kind `code`, tier `A`, status `mined`,
  opened `2026-10-25`, recheck `on-change`, used-by the C2 entry), id placeholder `S278`.
- **(b)** new own-work row for the live census receipt, id placeholder `S279`; cell 2 ends in
  `.ufo/waves/round-40/fetch/S279.receipt.txt`, cell 6 names the receipt path and the tool sha
  placeholder `TOOLSHA`.
- **(c)** used-by extensions for held rows S162 and S173 shown as old → new cell 11, plus the full
  replacement rows with cells 1-10 copied byte-for-byte from BASE; plus a conditional S180
  extension if the entry cites S180.

Id placeholders: the registry holds 214 rows, ids S001..S277, no duplicates, no 11-column defect;
next free is S278/S279. The L1 must rewrite cells 1 and every cross-reference together.

## Finding (HIGH) — the bare commit URL for ComplexDataTypes.hpp fails clause e

`corpus/SOURCES.md:192` (S180, `mined`, opened `2026-10-23`) already registers the *same file at
the same bytes*: same URL ending, same `sha256:95733223…`, same `6116 B`, scope "four-sided gap
parsing". Running the frozen counter's own clause-e code (`loc = cells[1].split()[-1]`,
`same == [i]`) over all 214 rows for a new row ending in that bare URL gives
`same == ['S180', 'S278']` → **clause e fails**. Two sibling seats reached the same conclusion
independently (`w1/ConnSourcePatterns.md` F7, `w1/ExecFetchComplexTypes/quotes.md:241-252`).

Resolution used in the draft: cell 2 uses the **release-tag URL of the same tree**,
`https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/src/config/shared/complex/ComplexDataTypes.hpp`
— measured this seat: `HTTP=200 SIZE=6116`, sha256
`95733223b115510dda23e753aae64e373205cc7081b0eeb204df866ea7e68807`, byte-identical to the
pinned-commit receipt, and the token has zero other users in the registry. The host reports
`hyprland 0.56.2 commit efb5099… tag v0.56.2`, so tag URL and commit URL denote one tree.
The draft states the caveat the L1 must record: same file as S180, split by scope (S180 = gap
parser `:80-120`; new row = the serialisers), not a second source.

Alternatives documented in `rows.md`, not used: (A1) bare commit URL — fails clause e as measured;
(A2) drop the new row, extend S180, and open a different new row at
`…/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataType.hpp`
(measured this seat: `HTTP=200`, 481 B, sha256
`e7fee893be361e6e11102aeac549dd8ed527dd2c0e1a5a879f717b4c8222882e`, holds
`enum eConfigValueDataTypes` :7-11 and `getDataType()` :18) — that file has no committed fetch
receipt yet, so clause d would need one landed first.

## Evidence this seat re-derived (not restated)

- Row anchors pinned in the committed receipt bytes
  `.ufo/waves/round-40/fetch/complex-data-types-efb5099.bin` (sha256 `95733223…`, 6116 B, 178
  lines): `CGradientValueData::toString` :69-77 (`std::format("{:x} ", c.getAsHex())` :72,
  `"{}deg"` :75), `CCssGapData::parseGapData` :94 and `toString` :133-135
  (`"{} {} {} {}"`), `CFontWeightConfigValueData::toString` :154-156 and `WEIGHTS` :158-161.
- Forms histogram recomputed from `.ufo/waves/round-40/c1/native-capture.jsonl`: 70 records,
  `{'int': 44, 'float': 5, 'custom': 13, 'str': 8}` (sum 70).
- Labels line read from `.ufo/waves/round-40/w1/ExecLiveCensus/census-receipt.txt:15`:
  `labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0` (sum 70); receipt
  line 6 is `tool sha256 <TOOLSHA>` — the placeholder the L1 must substitute with the data
  commit's `tools/mado-options.py` sha256 (tip bytes now
  `461f8c3c245bdfb6dcaac068a5ab378326c75dc91992b8012f9ca0e5019fb03a`, not the data commit's).
- Held-row receipts already hash-match their rows' own anchors:
  `fetch/config-manager-efb5099.bin` = `9db68cf4…` (= S162 cell 6),
  `fetch/hyprlang-config-v0.6.8.bin` = `fa1b6898…` (= S173 cell 6).
- `git -C … diff 9fc511dd… -- corpus/SOURCES.md` prints nothing → S162/S173 are byte-identical to
  BASE, so the cells quoted for the extensions are the BASE cells.
- Scratch validation (`mktemp -d` copy, CORPUS.md census commands): rows 214 → 216, malformed 0,
  duplicate ids none, tier/status/kind enums valid, no tier inflation; both new rows parse to 11
  cells with no `|` in any cell; S162/S173 cells 1-10 equal to base and cell 11 strictly longer;
  clause-e `S278 → [S278]`, `S279 → [S279]`. The "mined used-by path missing" sweep reports only
  `corpus/knowledge/hyprctl-getoption-native-forms-r40.md` (4 rows) — expected, the entry does not
  exist yet.
- Two read-only network fetches this seat performed (tag URL and `ComplexDataType.hpp`); no
  compositor verb, no package manager, no host write. Scratch cleaned (`rm -rf` of the mktemp dir).

## Gates

No gate is claimed by this seat: it writes no product code, no counter, no entry. Counter clauses
c/e were exercised only as parsers over a /tmp copy of the registry, which is a check of the
draft's shape, not a claim verdict. The L1 runs
`python3 -I quality/counters/c2-r40-forms-entry.py --repo . --rev <rev>` at the data commit.

## Touched surfaces

- written: `.ufo/waves/round-40/w1/ScrSourcesRowsForms/rows.md`,
  `.ufo/waves/round-40/w1/ScrSourcesRowsForms.md` (this report).
- read-only: `corpus/SOURCES.md`, `CORPUS.md`, `quality/counters/c2-r40-forms-entry.py`,
  `.ufo/waves/round-40/{registration.md,c1/native-capture.jsonl,fetch/*}`,
  `.ufo/waves/round-40/w1/{ConnSourcePatterns.md,ExecLiveCensus/census-receipt.txt,…}`, `tools/mado-options.py`,
  `git diff/show` at base `9fc511dd…`.
- no tool installs, no package transactions, no tracked-file edits, no git/jj mutation.

## Out of scope / handed to L1

1. Id assignment (S278/S279 are placeholders) and the joint rewrite of cells 1, used-by lists and
   Gate lines.
2. Landing the census receipt under `.ufo/waves/round-40/fetch/` with `TOOLSHA` substituted.
3. The `corpus/knowledge/hyprctl-getoption-native-forms-r40.md` entry and its `corpus/README.md`
   index row (clause f).
4. The `## Gate` block and the old→new used-by log in `corpus/lessons/round-40.md`.
5. The S180 overlap decision (tag URL as drafted, or alternative A2) and its lesson note.
