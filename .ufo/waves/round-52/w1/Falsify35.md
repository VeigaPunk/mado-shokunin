# Falsify35 — round 52: C1 no-work control validity

Seat: falsification item 35. Target: C1 no-work control validity. Source-only; no claim,
predicate, control or tracked-lane edit was made.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify35.md` (this report)
- `.ufo/waves/round-52/w1/Falsify35/run.sh` — reproducible driver (absolute paths; writes only to scratch)
- `.ufo/waves/round-52/w1/Falsify35/f35-hollow.py` — seat-local probe of the frozen predicate text (not the absent round-52 counter)
- `.ufo/waves/round-52/w1/Falsify35/c1-fixture-c.md` — 2-row generic self-pointer ledger in the committed grammar
- `.ufo/waves/round-52/w1/Falsify35/c1-fixture-d.md` — 82-row population-shaped generic self-pointer ledger in the committed grammar
- `.ufo/waves/round-52/w1/Falsify35/receipts.txt` — captured output of every command below (reproduce with: bash run.sh, redirecting stdout to receipts.txt)

## Attacked items (named, not generic)

1. `claims-frozen.md:7` — “Demonstrate production pass and control fail at the frozen revision.”
2. `registration.md:7` — “It must pass on the existing production ledger at the base revision and fail on
   `controls/c1-do-nothing.md` specifically for self-pointer/context defects.”
3. `registration.md:15` — “C1 do-nothing control `controls/c1-do-nothing.md` is the committed ledger
   shape with only repeated generic self-pointers.”

Nothing here touches prose entailment, the C2 claim, or any predicate value.

## Axes

- **Operability** (primary): whether the frozen control exercises the two clauses that are new
  relative to the base instrument (non-self pointer, instrument-specific context).
- **Coverage** (secondary, only as the ledger population the control must be shaped like).

## Reproducible setup

```bash
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
BASE=85d57a818c3707397e21c840b6498b105ba798aa
SEAT=$LANE/.ufo/waves/round-52/w1/Falsify35
bash "$SEAT/run.sh"            # scratch: /fast/scratch/hyaku/mado-r52/Falsify35 (overridable)
```

`run.sh` extracts the base revision with `git -C "$LANE" archive "$BASE" | tar -x -C $W/repo-prod`
(read-only), derives the population with the committed rule (`tools/*`, `quality/*.py`,
`quality/counters/*.py` → 82 rows: 17 + 19 + 46), builds fixtures C/D from the base bytes, and
scores four artifacts with three probe modes. Disk guard checked before the run
(`/fast` 599G available, 26% used). Scratch was removed after the receipt copies were taken.

Pinned inputs (sha256):

```
ad72f72f64708d1b877d0f2233f32a065bd11689d644af669176d1844ba2eba6  .ufo/waves/round-52/controls/c1-do-nothing.md
df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b  base:quality/tool-ledger.md
6dd4061c1d8a82d5a9efa8ae954ff1c4559e43abefbb69210fa831bd758a98d4  base:quality/check-tool-ledger.py
d5c2447d098681251fd41c04414d4e8823b41b78f150a5fc6bedd526a4a35b56  base:quality/counters/c1-r51-ledger.py
```

## Findings

### F1 — the frozen control is not the committed ledger shape

`registration.md:15` calls it “the committed ledger shape”. The bytes say otherwise.

```
production ledger:   line 30  | instrument | description | accountability pointer |     (3 columns)
                     82 unfenced data rows, all 3 cells (the 83rd pipe-line is the fenced
                     grammar example at quality/tool-ledger.md:12)
frozen control:      line 1   | Tool | Reads | Writes | Owner and adjacent lanes |        (4 columns)
                     lines 3-4, both 4 cells
```

The committed parser rejects any row whose cell count is not exactly 3
(`quality/check-tool-ledger.py:251-254`: `if len(cells) != 3: malformed.append(...)`).
Scoring the control at the tracked ledger path with the committed checker at the base bytes:

```
LEDGER: population=82 ledger_rows=0 uncovered=82 dangling=2 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED  rc=1
```

So the control contributes **zero** ledger rows: its failure is a parse/grammar failure, before
any pointer or description clause is evaluated.

### F2 — under the base's own lenient grammar the control fails on “no pointer named”, still not self-pointer

The round-51 counter parses any row with ≥3 cells and takes `cells[2:]` as the pointer cell
(`quality/counters/c1-r51-ledger.py:155-174`). For the control that maps:

```
row path  = tools/mado-verify.sh
desc      = quality/tool-ledger.md (commentary only)      <- cell 2
pointer   = nothing | generic accountability pointer to this ledger itself   <- cells 3+4
```

Result:

```
C1_R51: population=82 ledger_rows=2 uncovered=81 dangling=0 bad_pointer=1 empty_desc=0 selftest=ok dup=1 checker=failed verdict=TARGET_MISSED
```

First-failing clause is `bad_pointer` (“nothing” names no path) with `dup=1`. The generic
self-pointer sentence lives in a **fourth column that the committed contract does not define**,
so no pointer-cell mapping derived from the production grammar surfaces it as a pointer.

### F3 — the required red receipt is produced by instruments that implement none of the three clauses

The claim says the base counter “does not measure context” (`registration.md:7`). That same
instrument already yields the demanded pair:

```
r51 counter, production : C1_R51: ... selftest=ok verdict=TARGET_MET    rc=0
r51 counter, control    : C1_R51: ... dup=1 checker=failed verdict=TARGET_MISSED  rc=1
```

A probe whose only rule is “≥10 parsed rows” also yields the pair:

```
prod    mode=count rows=82 malformed=0                 verdict=PASS  rc=0
control mode=count rows=0  malformed=2                 verdict=FAIL  rc=1
```

Therefore “production pass and control fail at the frozen revision” cannot evidence the
existence or operation of the non-self clause or the instrument-specific context clause: the
observation is reproduced by a counter with zero of the three predicates.

### F4 — the control is not population-shaped, so coverage/shape, not the target clauses, explains the fail

The control has 2 data rows against a population of 82. Fixture C re-cuts the control's *stated*
content into the committed grammar (2 rows, distinct instruments, self-pointer, generic
description): `uncovered=80`, `dup=0`, `nonself=2` — it fails coverage and count, not only the
target clauses.

Fixture D is the population-shaped version of the same no-work idea (82 unique rows, every
pointer `quality/tool-ledger.md`, every description the same generic sentence):

```
base checker on fixture D : LEDGER: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MET  rc=0
f35-hollow, count         : rows=82 malformed=0            verdict=PASS
f35-hollow, unique        : rows=82 dup=0                  verdict=PASS
f35-hollow, semantic      : rows=82 uncovered=0 nonself=82 verdict=FAIL
```

The base checker **passes** an entirely no-work ledger (the round-51 defect this claim targets),
and the two syntactic probe modes pass it as well. No artifact in the frozen control set is
population-shaped, so no frozen control isolates the self-pointer clause — the shape that would
is absent from `.ufo/waves/round-52/controls/`.

### F5 — the control is neither committed nor addressable at the frozen revision

```
git -C $LANE cat-file -e 85d57a8:.ufo/waves/round-52/controls/c1-do-nothing.md
  fatal: path '...' exists on disk, but not in '85d57a8'
git -C $LANE cat-file -e HEAD:.ufo/waves/round-52/controls/c1-do-nothing.md
  fatal: path '...' exists on disk, but not in 'HEAD'
git -C $LANE status --short   ->   ?? .ufo/waves/round-52/
```

“Fail on `controls/c1-do-nothing.md` … at the frozen revision” therefore requires an
off-revision byte copy, and the frozen predicate does not say how the counter addresses it: as a
ledger at an arbitrary path, or as control bytes substituted at `quality/tool-ledger.md`. Both
dispositions were scored; both are malformed 4-cell rows.

### F6 — “non-self” is parameterisation-dependent and does not bite at the delivered path

Scored at its delivered path with `self = <ledger argument>`, the control's pointer
`quality/tool-ledger.md` is not the control file, so a pointer-based non-self clause reports
`nonself=0`. Only a counter that hardcodes `self = quality/tool-ledger.md` (or scans the whole
row rather than the pointer cell) can surface the self-pointer — a design choice the frozen text
does not fix, and one that changes the answer.

## Reproduced: yes

Every finding is reproduced by `bash .ufo/waves/round-52/w1/Falsify35/run.sh`; the full output is
`receipts.txt` in the seat directory. No finding depends on host state, live reads, package data,
or network.

## Overlap with peer seat (recorded, not hidden)

`w1/C1ControlAttack.md` reached the same three structural observations (4-column control vs
3-column grammar, duplicated row, `nothing` as the parsed pointer) by source reading alone, and
stated it ran no fixture driver. This seat's increment is executed evidence: the base checker's
`ledger_rows=0` on the control, the base r51 counter's production-pass/control-fail pair, the
population-shaped fixture D that the base checker scores `TARGET_MET`, the control's absence from
both base and HEAD, and the self-parameterisation result. F4-F6 are not in that report.

## Limitations

- The round-52 C1 counter does not exist at base (0 `r52` entries under `quality/counters` at
  `85d57a8`), so I could not run the claimed counter. I tested the frozen demonstration
  requirement and the frozen control, which is what the claim requires the future counter to
  satisfy.
- `f35-hollow.py` is a seat-local probe of the predicate text, not a proposed counter; its
  `semantic` mode deliberately stubs the instrument-specific context clause (`context=stub-ok`)
  so the receipt shows which clauses are actually forced by the control.
- Cell-mapping choices are inferred from the two parsers in the lane (`check-tool-ledger.py`
  strict 3-cell, `c1-r51-ledger.py` lenient `cells[2:]`); a third plausible mapping (“last cell
  is the pointer”) was reasoned through but not coded — it also fails on “no pointer named”,
  because the control's last cell is a bare sentence.
- No statement is made about prose entailment or about C2; the claim explicitly excludes both.

## Dissent and failed controls (honest record)

- My `semantic` mode reports `nonself=0` for the delivered-path control. That is a result about
  the clause's parameterisation, not a pass of the control.
- Fixture D passing `count`/`unique` is not a counter proposal; it is the demonstration that those
  modes cannot stand in for the target clauses.
- The base checker's `TARGET_MET` on fixture D is the clearest counter-example to “a new counter
  is what distinguishes no-work from work”: the same ledger shape is accepted today.

## Bounded move (no predicate edit; for the seat that owns construction)

A control that can carry the claim must be population-shaped (82 unique rows), in the committed
3-cell grammar, materialised at the tracked ledger path, with pointers that resolve and
descriptions that are non-generic — so the only failing clauses are non-self and context. The
counter should report the failing clause per row (not just a global verdict), and the receipt
should show that removing either clause flips the control from FAIL to PASS. That improves
operability without touching C1's coverage and harms no axis.

## Evidence

- `.ufo/waves/round-52/claims-frozen.md:7` (C1 target and demonstration sentence)
- `.ufo/waves/round-52/registration.md:7,15` (frozen predicate, control description)
- `.ufo/waves/round-52/controls/c1-do-nothing.md:1-4` (4-column table, two identical rows, sha256 `ad72f72f…`)
- `quality/tool-ledger.md:12,30` (fenced grammar example; 3-column header; 82 unfenced rows)
- `quality/check-tool-ledger.py:234-255` (strict 3-cell parser), `:268-327` (coverage/pointer evaluation)
- `quality/counters/c1-r51-ledger.py:155-174` (lenient parser), `:177-208` (pointer resolution by basename)
- `.ufo/waves/round-52/receipts/c1-base.txt:3` (base 82/82 `TARGET_MET`)
- Seat receipts: `.ufo/waves/round-52/w1/Falsify35/receipts.txt`

No external source candidates or URLs were used; no source checkout was written. No package
queries, live reads, process/compositor probes, input capture or screenshots were performed. The
only executables run were the lane's file-only gate `quality/check-tool-ledger.py` (including its
50-case selftest) and `quality/counters/c1-r51-ledger.py`, both against seat-local `git archive`
snapshots and a scratch git fixture; no mado producer that reads the host or compositor was
executed and no host state was consulted. No installs. Scratch
`/fast/scratch/hyaku/mado-r52/Falsify35` removed after the receipt copies.

## Report

Report: .ufo/waves/round-52/w1/Falsify35.md
