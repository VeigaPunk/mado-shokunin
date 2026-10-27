# Falsify27 — C1 no-work control validity

Seat: Falsify27 (leaf, no delegation). Target: C1 no-work control validity
(`controls/c1-do-nothing.md`). Base `85d57a818c3707397e21c840b6498b105ba798aa`.
Method: source bytes + seat-local scratch fixtures under
`/fast/scratch/hyaku/mado-r52/Falsify27/`; no tracked edits, no producer execution,
no package queries, no live reads, no installs.

## Deliverables

- This report: `.ufo/waves/round-52/w1/Falsify27.md`
- Control byte copy + digest: `.ufo/waves/round-52/w1/Falsify27/c1-do-nothing.copy.md`
  (sha256 `ad72f72f64708d1b877d0f2233f32a065bd11689d644af669176d1844ba2eba6`, identical to the frozen control)
- D1 grammar-layout evidence: `.ufo/waves/round-52/w1/Falsify27/d1-grammar-layout.txt`
- D2 control-installed counter run: `.ufo/waves/round-52/w1/Falsify27/d2-control-run.txt`
- D2 checker full findings on the same fixture: `.ufo/waves/round-52/w1/Falsify27/d2-checker-full.txt`
- D3 in-grammar no-work fixture run: `.ufo/waves/round-52/w1/Falsify27/d3-nowork-run.txt`
- D3 fixture ledger bytes: `.ufo/waves/round-52/w1/Falsify27/d3-nowork-ledger.md`

## Attacked clause

- `registration.md` §Frozen predicates, C1: "It must pass on the existing production ledger at
  the base revision and **fail on `controls/c1-do-nothing.md` specifically for self-pointer/context
  defects**."
- `claims-frozen.md` §C1: "a new committed counter **distinguishes the production ledger from a
  no-work control of repeated generic self-pointers** using unique population, **non-self
  resolvable evidence targets**, and **instrument-specific context checks**."
- `claims-frozen.md` §C1: "Demonstrate production pass and control fail at the frozen revision."

## Failure mode (control invalid as discriminator for the named defects)

The committed control bytes are not rows in either enforced ledger grammar, and the
self-referential path never appears in a pointer cell:

1. **Checker grammar** (`quality/check-tool-ledger.py:234-260`, rows require exactly 3 cells;
   first pipe row with first cell in `{path,file,instrument,tool,artifact}` is the header):
   the control is a 4-column table (`Tool | Reads | Writes | Owner`); both data rows have
   4 cells → **malformed**. The checker parses **0 rows** and reports
   `ledger_rows=0 uncovered=82 dangling=2` with findings `row-malformed-cells-4-line-3/4`.
2. **Counter grammar** (`quality/counters/c1-r51-ledger.py:186-206`, no 3-cell requirement,
   no header skip): the control parses as 2 rows, both `tools/mado-verify.sh` (a duplicate).
   The self-referential path `quality/tool-ledger.md` sits in the **description/READS cell**
   (pipe column 2); the pointer cell is
   `nothing | generic accountability pointer to this ledger itself`, which yields **zero
   resolvable path tokens** under both tokenizers (`c1-r51-ledger.py:208-227`,
   `check-tool-ledger.py:214-231` — no backticked spans; whitespace-split words carry no `/`
   and no known extension).
3. Consequence for the frozen clauses: a **non-self clause has no pointer token to compare
   against the ledger path** on these bytes — it cannot be the clause that fires. The rows fail
   as *unresolvable-pointer / malformed / duplicate / coverage* defects. The **context defect is
   present** (descriptions are generic) but under the checker grammar there are no parsed cells
   to check, and the base machinery has no context field at all (`empty_desc=0`).
4. **Contrast (D3):** the no-work shape the control is *named* for — "repeated generic
   self-pointers" — expressed in the enforced 3-cell grammar (82 rows, one per population
   instrument, identical generic description, every pointer the ledger itself) **passes the base
   machinery outright**: `verdict=TARGET_MET`, exit 0, checker agreement. So the defect class the
   control must exercise is real and undetected at base, but it is only expressible in-grammar —
   which the committed control bytes are not.

Therefore the registration's demonstration requirement — control fail "specifically for
self-pointer/context defects" — is not satisfiable by exercising the committed control bytes
through the frozen machinery (counter + clause-max checker agreement). Any red receipt carrying
that attribution must come from builder re-cut in-grammar bytes (which are not the committed
control) or from control-specific parsing glue.

## Reproducible setup / commands

All under `/fast/scratch/hyaku/mado-r52/Falsify27/` (disk guard checked first:
`df -h /fast/scratch` → 599G available). Lane repo untouched; every git mutation happened inside
a scratch clone after asserting `git rev-parse --show-toplevel` printed that fixture dir.

D1 (byte-level, pure text functions reimplemented 1:1 from the cited source lines):

```
python3 /fast/scratch/hyaku/mado-r52/Falsify27/d1-grammar-layout.py
```

D2 (control bytes installed as the ledger at a scratch clone of base):

```
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin fixture-control && cd fixture-control
git rev-parse --show-toplevel   # asserted == /fast/scratch/hyaku/mado-r52/Falsify27/fixture-control
git checkout -q --detach 85d57a818c3707397e21c840b6498b105ba798aa
cp <lane>/.ufo/waves/round-52/controls/c1-do-nothing.md quality/tool-ledger.md
git -c user.name='Falsify27 fixture' -c user.email='falsify27@scratch.invalid' commit -q -am 'fixture: control bytes as ledger'
# rev ef87c3fef8bfa309f6b8bb2cfed2d28bf8d04482
TMPDIR=/fast/scratch/hyaku/mado-r52/Falsify27/tmp python3 -I \
  <lane>/quality/counters/c1-r51-ledger.py --repo <...>/fixture-control \
  --rev ef87c3fef8bfa309f6b8bb2cfed2d28bf8d04482 --work <...>/work
TMPDIR=... python3 -I <lane>/quality/check-tool-ledger.py --repo <...>/fixture-control --rev ef87c3fe...
```

D3 (in-grammar no-work fixture: 82 rows, generic descriptions, self-pointers):

```
git clone -q <lane> fixture-nowork && cd fixture-nowork
git rev-parse --show-toplevel   # asserted == /fast/scratch/hyaku/mado-r52/Falsify27/fixture-nowork
git checkout -q --detach 85d57a818c3707397e21c840b6498b105ba798aa
# generate quality/tool-ledger.md: header + | `<path>` | tracked lane instrument | `quality/tool-ledger.md` |
#   for the 82 population paths (counter population rule, c1-r51-ledger.py:133-148)
git -c user.name='Falsify27 fixture' -c user.email='falsify27@scratch.invalid' commit -q -am 'fixture: in-grammar no-work ledger'
# rev 9f6e02c8cb1d21f6773a2b2cf0c8df74b3dffd3a
TMPDIR=... python3 -I <lane>/quality/counters/c1-r51-ledger.py --repo <...>/fixture-nowork \
  --rev 9f6e02c8cb1d21f6773a2b2cf0c8df74b3dffd3a --work <...>/work
```

## Actual results

D1 (`.ufo/waves/round-52/w1/Falsify27/d1-grammar-layout.txt`): counter grammar yields 2 rows
(both `tools/mado-verify.sh`, 1 duplicate); desc cell = `'quality/tool-ledger.md (commentary
only)'`; pointer cell = `'nothing | generic accountability pointer to this ledger itself'`;
pointer tokens `[]`; desc not placeholder-only. Checker grammar yields **0 rows, 2 malformed**
(4 cells ≠ 3). Self-path appears only in pipe column 2 (description/READS), never in a pointer
cell.

D2 (`.ufo/waves/round-52/w1/Falsify27/d2-control-run.txt`):

```
C1_R51: population=82 ledger_rows=2 uncovered=81 dangling=0 bad_pointer=1 empty_desc=0 selftest=ok dup=1 checker=failed verdict=TARGET_MISSED rev=ef87c3fef8bfa309f6b8bb2cfed2d28bf8d04482
exit=1
```

Checker on the same fixture (`.ufo/waves/round-52/w1/Falsify27/d2-checker-full.txt`):

```
LEDGER-ROW reason=dangling path=- detail=row-malformed-cells-4-line-3
LEDGER-ROW reason=dangling path=- detail=row-malformed-cells-4-line-4
LEDGER: population=82 ledger_rows=0 uncovered=82 dangling=2 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED rev=ef87c3fe...
```

Failure attribution is coverage/malformed/duplicate/unresolvable-pointer. No self-pointer field
exists or fires; no context field exists (`empty_desc=0`).

D3 (`.ufo/waves/round-52/w1/Falsify27/d3-nowork-run.txt`):

```
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=9f6e02c8cb1d21f6773a2b2cf0c8df74b3dffd3a)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=9f6e02c8cb1d21f6773a2b2cf0c8df74b3dffd3a
exit=0
```

The in-grammar no-work ledger (identical generic description on all 82 rows, every pointer the
ledger itself) **passes** the base machinery at the round-52 base.

## Reproduced

**Yes.** All three demonstrations executed with the captured outputs above. The green side
(production 82/82 TARGET_MET at base) is already committed evidence
(`.ufo/waves/round-52/receipts/c1-base.txt`) and was not re-run.

## Verdict on the attacked clause

The frozen no-work control, as committed, **cannot carry the registration's "specifically for
self-pointer/context defects" attribution**: under the checker grammar its rows are malformed
(no cells exist for any clause), and under the counter grammar its pointer cells contain no
resolvable token, so a non-self clause has nothing to compare; the measured failure is
`uncovered=81 / dup=1 / bad_pointer=1` (counter) and `malformed=2 / uncovered=82` (checker).
Meanwhile the defect class the control is named for passes in-grammar (D3). This is a control
validity finding, not permission to change the frozen control (registration: "Controls cannot be
changed after workers score them"). Actionable for the C1 builder: the red receipt must come
from an in-grammar self-pointer/generic fixture (as in D3), and the report must state plainly
that the committed control file's own bytes cannot produce that attribution — otherwise the
"control fail" half of the demonstration is vacuous (it fails for grammar/coverage, whatever the
clauses do).

## Limitations / dissent

- The round-52 counter is absent at base (frozen claim: "new counter absent"), so the runs
  exercise the base machinery the frozen claim requires the new counter to retain (unique
  population, resolvability, clause-max checker agreement). The finding is a property of the
  control bytes vs. the enforced grammars, so it transfers to any counter that keeps those two
  anchors; it does not prejudge a counter that abandons them.
- Named escape hatches a builder could take, with their costs: (i) re-cut the control into
  3-cell rows inside a selftest fixture — then the red receipt is not the committed control
  bytes; (ii) lenient 4-cell parsing plus a whole-row self-reference text scan — then "non-self
  resolvable evidence targets" is no longer a pointer-cell clause, and `uncovered=81`/`dup=1`
  still co-fire, so the failure is not "specifically" self-pointer/context; (iii) a control-mode
  harness suppressing the population clause — a harness not described in claim or registration.
- The context defect (generic descriptions) is genuinely present in the control bytes and a
  context clause could fire on the counter-grammar parse; the defect demonstrated is the
  non-self clause's unexercisability plus the grammar/coverage domination of the failure.
- Execution-scope note: SKILL.md:40-44 prohibits "producer execution" (live-state tools;
  SKILL.md:333-339, round-16 override). The counter and checker judge committed git bytes in
  seat scratch and touch no live state; the registration expects red/green receipts and the
  C1Fixture seat tasking requires verifying exact outputs, so fixture runs of counters/checkers
  are the sanctioned path. Two sibling seats (Falsify18, Falsify36) chose not to execute; their
  "reproduced: no" results are consistent with, and subsumed by, the runs here.
- No external source candidates were opened (local bytes only); no URL/access-date/quote block
  applies. No package queries, installs, host mutations, or /tmp usage. Scratch
  `/fast/scratch/hyaku/mado-r52/Falsify27/` is removed after this report; receipts were copied
  to the seat dir first.

Report: `.ufo/waves/round-52/w1/Falsify27.md`
