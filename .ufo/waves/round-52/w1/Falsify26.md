# Falsify26 — C1 uniqueness/population falsification

Seat: Falsify26 (leaf, no dispatch). Item 26 target: **C1 uniqueness/population falsification**.
All work seat-local; lane repo read-only. Base: `85d57a818c3707397e21c840b6498b105ba798aa`.

## Attacked clause

`registration.md` C1 frozen predicate (round-52): the new counter "validates population row
uniqueness, resolvable evidence pointer, non-self pointer, and a description containing
instrument-specific functional context. It must pass on the existing production ledger at
the base revision and **fail on `controls/c1-do-nothing.md` specifically for self-pointer/context
defects**." Registration additionally describes that control as "the committed ledger shape
with only repeated generic self-pointers." Attacked: the red-path attribution clause
("specifically for self-pointer/context defects") plus the "committed ledger shape" description,
both uniqueness/population-bound.

## Finding 1 — the frozen control is not the committed ledger shape; under the committed
grammar it fails malformed/uniqueness, and its self-pointer is not in the pointer column (reproduced: YES)

Bytes: `.ufo/waves/round-52/controls/c1-do-nothing.md` is a **4-column** table:

```
| Tool | Reads | Writes | Owner and adjacent lanes |
|---|---|---|---|
| tools/mado-verify.sh | quality/tool-ledger.md (commentary only) | nothing | generic accountability pointer to this ledger itself |
| tools/mado-verify.sh | quality/tool-ledger.md (commentary only) | nothing | generic accountability pointer to this ledger itself |
```

That header is the **PROVINCE.md inventory shape**, not the tool-ledger shape:
`git show 85d57a8:PROVINCE.md` line 22 = `| Tool | Reads | Writes | Owner and adjacent lanes |`
(confirmed; also cited by `.ufo/waves/round-41/w1/ScrSkillProvince/province-row.md`).
The committed ledger grammar is 3 cells
(`git show 85d57a8:quality/tool-ledger.md` line 27: `| instrument | description | accountability pointer |`,
contract enforced by `quality/check-tool-ledger.py`, whose docstring scores as `dangling` any
"malformed row (not exactly three cells)" and any "repeated path").

Consequences under the committed grammar:

- Each control row has 4 cells → both rows are malformed → the control fails as
  **uniqueness/population-shaped `dangling` defects** before any pointer/context logic runs.
- The only literal self-reference, `quality/tool-ledger.md`, sits in the **description (Reads)
  cell**; the pointer cell contains `nothing` (no path token at all). The "generic accountability
  pointer to this ledger itself" text is in a fourth column a 3-cell parser never reads.
- Therefore an honest counter that parses the committed grammar **cannot** report the control's
  failure as "specifically for self-pointer/context defects": the failure is
  malformed/repeated/unresolvable-pointer, and the self-pointer text is in the wrong column.
  A counter that special-cases the 4-cell shape to surface self-pointer/context would be
  deviating from the grammar it must use to pass production.

Reproduction (fixture = scratch git repo, control bytes verbatim as `quality/tool-ledger.md`,
plus `tools/mado-verify.sh` which does exist at base — production ledger row 47):

```
python3 quality/check-tool-ledger.py --repo fixture-a --rev HEAD --verbose
LEDGER-ROW reason=dangling path=- detail=row-malformed-cells-4-line-3
LEDGER-ROW reason=dangling path=- detail=row-malformed-cells-4-line-4
LEDGER-ROW reason=uncovered path=tools/mado-verify.sh detail=no-row
LEDGER: population=1 ledger_rows=0 uncovered=1 dangling=2 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED
```

## Finding 2 — on the red path, uniqueness is neither necessary nor sufficient (reproduced: YES)

- **Not necessary**: fixture B = control with the duplicate row removed (1 row) still fails:
  `dangling=1 detail=row-malformed-cells-4-line-3`. The malformed 4-cell shape alone drives the red.
- **Classification of uniqueness violations**: fixture D = proper 3-cell ledger listing the same
  path twice (valid pointers, functional descriptions) fails as
  `reason=dangling detail=row-duplicate-line-4` — under the committed grammar a pure uniqueness
  violation is a population/`dangling` finding, not a self-pointer/context finding.
- **Not sufficient**: fixture C = the control's own text re-grammared into the committed 3-cell
  shape (path | "generic accountability pointer to this ledger itself" | `quality/tool-ledger.md`)
  **passes the round-51 checker**: `LEDGER: population=1 ledger_rows=1 ... verdict=TARGET_MET exit=0`,
  because the ledger file contains the row basename — exactly the round-51 hole the claim wants
  closed. This shows the frozen control's discriminating power lives entirely in checks the
  registration names (non-self, context), while its frozen bytes place the self-pointer where
  those checks, applied to the parsed pointer cell, cannot see it.

## Finding 3 — production green path is genuinely clean (supporting measurement)

Independent probe of `quality/tool-ledger.md` at base (`receipts/production-probe.out`,
script `receipts/probe.py`, run in scratch, read-only git): population per
`c1-r51-ledger.py` rules = 82, ledger rows = 82, extras = 0, missing = 0; duplicate row paths =
0 under 7 normalizations (exact, emphasis-stripped, whitespace-removed, leading-`./`-stripped,
slash-collapsed, case-folded, NFKC); raw-cell anomalies = 0; non-ASCII paths = 0; distinct
population members colliding under case-fold/NFKC = 0; rows pointing at
`quality/tool-ledger.md` = 0. So "pass on the existing production ledger at the base revision"
is achievable, and this falsification is confined to the red-path attribution clause.

## Impacted axes and harm check

- **Operability (C1)**: red-path attribution ("specifically for self-pointer/context defects")
  is unsatisfiable under the committed grammar; registration's "committed ledger shape"
  description of the control is factually wrong (it is the PROVINCE inventory shape).
- **Coverage (C2)**: untouched. No axis harmed; measurement-only, no tracked edits, no installs.

## Smallest safe correction

For the judge/builder (no predicate or control edit by this seat; controls are frozen):

1. Score the control with an explicitly declared row grammar; the committed grammar forces
   malformed/`dangling` findings — so accept a red receipt that reports per-check defect classes
   (uniqueness, resolvable-pointer, non-self-pointer, context) and shows **self-pointer and
   context checks firing** on the control, or
2. read the control semantically as authored (Reads column = the accountability pointer
   candidate, Owner column = description) and require the counter to classify its defects as
   self-pointer + context, documenting that deviation from the 3-cell grammar; or
3. relax "specifically" to "self-pointer/context defects must be among the reported causes".

Without one of these, any counter that honestly applies the four named checks to the committed
grammar will report the control's failure under uniqueness/malformed/unresolvable classes, and a
strict judge reading "specifically" literally must reject the C1 red receipt.

## Commands and results

- `python3 /fast/scratch/hyaku/mado-r52/Falsify26/probe.py` → `receipts/production-probe.out` (Finding 3).
- `git init` + commit of fixture repos under `/fast/scratch/hyaku/mado-r52/Falsify26/fixture-{a,b,c,d}`;
  `python3 quality/check-tool-ledger.py --repo <fixture> --rev HEAD --verbose` →
  `receipts/control-fixture-a-checker.out`, `receipts/control-dedup-fixture-b-checker.out`,
  `receipts/selfpointer-3cell-fixture-c-checker.out`, `receipts/repeated-path-fixture-d-checker.out`.
- Provenance checks: `git show 85d57a8:PROVINCE.md | grep -n 'Tool | Reads'` (line 22);
  `git show 85d57a8:quality/tool-ledger.md | sed -n '18,24p'` (grammar block);
  `git ls-tree -r --name-only 85d57a8 | grep -c '^tools/mado-verify.sh$'` → 1.

## Limitations

The round-52 counter is not yet committed; this attack falsifies the frozen predicate's
testability using the committed grammar checker (`check-tool-ledger.py` at base) as the reference
parser and seat-local fixtures built from frozen control bytes. The implementer could choose a
different parse, but any parse that passes production must read the 3-cell ledger rows, and the
control's frozen 4-cell shape then forces malformed/uniqueness findings ahead of, or alongside,
any self-pointer/context attribution. No live reads, probes, package queries, producer execution,
or checkout writes were performed. No installs (none needed). Scratch `/fast/scratch/hyaku/mado-r52/Falsify26/`
(fixture repos, probe, raw outputs) was removed on exit after receipt copies landed in the seat
dir; no `/tmp` evidence was used.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify26.md` (this report)
- `.ufo/waves/round-52/w1/Falsify26/receipts/production-probe.out`
- `.ufo/waves/round-52/w1/Falsify26/receipts/probe.py`
- `.ufo/waves/round-52/w1/Falsify26/receipts/control-fixture-a-checker.out`
- `.ufo/waves/round-52/w1/Falsify26/receipts/control-dedup-fixture-b-checker.out`
- `.ufo/waves/round-52/w1/Falsify26/receipts/selfpointer-3cell-fixture-c-checker.out`
- `.ufo/waves/round-52/w1/Falsify26/receipts/repeated-path-fixture-d-checker.out`

## Report

- `.ufo/waves/round-52/w1/Falsify26.md`
