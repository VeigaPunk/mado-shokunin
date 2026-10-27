# Falsify17 — C1 self-pointer / context bypass (mado round 52, w1)

Seat: Falsify17 · item 17 · source-only · base `85d57a818c3707397e21c840b6498b105ba798aa`
Read first: `.ufo/waves/round-52/claims-frozen.md`, `registration.md`, `controls/c1-do-nothing.md`,
`receipts/c1-base.txt`, `quality/counters/c1-r51-ledger.py`, `quality/check-tool-ledger.py`.
No tracked file, control, claim or predicate was edited. No install, package query, live read,
producer execution or host mutation.

## Axes named (godspeed)

- **operability** (C1's axis): the ledger's accountability is only as strong as the negative
  sample that certifies it. This seat attacks that sample.
- **coverage**: untouched; this seat proposes no entry and opens no source. Coverage-neutral by
  construction, so it cannot harm the axis.

## Attacked item and predicate (exact frozen wording)

`claims-frozen.md`, C1:

> Target: a new committed counter distinguishes the production ledger from a no-work control of
> repeated generic self-pointers using unique population, non-self resolvable evidence targets,
> and instrument-specific context checks. Demonstrate production pass and control fail at the
> frozen revision.

`registration.md`, C1:

> It must pass on the existing production ledger at the base revision and fail on
> `controls/c1-do-nothing.md` specifically for self-pointer/context defects.

Attacked: the **discrimination claim** — that "production pass + control fail" evidences the
`non-self` and `instrument-specific context` predicates, and that the control's self-pointer is
reachable by a ledger-grammar-faithful counter.

## Setup (reproducible)

`python3.14.8`, `git 2.56.0`, disk guard `/fast` 26% used at start. Scratch:
`/fast/scratch/hyaku/mado-r52/Falsify17` (removed on exit; receipts copied into this seat dir).
Fixture is a **seat-local** git repo, no lane writes; `git rev-parse --show-toplevel` asserted to
be the fixture dir before `git init/commit`:

```
sh .ufo/waves/round-52/w1/Falsify17/fixture/build-fixture.sh /fast/scratch/hyaku/mado-r52/Falsify17/fixture
# fixture_head=c4403e4b0de06504c8653d993bccba5c6c0f56f6
```

Fixture population: `tools/ti-alpha.py`, `tools/ti-beta.py`, `tools/ti-gamma.py`,
`quality/check-tool-ledger.py`, `quality/counters/c1-r51-ledger.py` (base bytes). Two ledgers:

- `quality/tool-ledger.md` — **no-work, unique rows**, description = the instrument's own
  docstring, every pointer = `` `quality/tool-ledger.md` `` (self-pointer).
- `docs/ledger-control.md` — byte-identical copy of that ledger at a **different path**
  (`sha256 b12c779e…` for both; `diff` empty). This is the bypass vehicle.

Reference implementation of the four frozen predicates (not a lane artifact):
`pred4.py` — p1 unique population (uncovered/dup/dangling/malformed = 0), p2 resolvable pointer,
p3 non-self (**`arg`** = pointer ≠ scored ledger path, **`canonical`** = pointer ≠
`quality/tool-ledger.md`), p4 instrument context (description names the basename **or** shares
≥2 non-stopword tokens of length ≥5 with the instrument's own source bytes).

```
python3 -I pred4.py --repo <repo> --rev <rev> --ledger-rel REL | --ledger-file ABS \
        [--columns 3|4] [--checks p1,p2,p3,p4]
```

## Measured results

Full transcript: `receipts/pred4-matrix.txt`; control cell dump: `receipts/control-parse.txt`;
old-counter transcript: `receipts/old-counter.txt`; pins: `receipts/inputs.txt`.

| # | subject | reading | verdict | key fields |
|---|---|---|---|---|
| 1 | production ledger @ base | 3-cell, p1–p4 | **TARGET_MET** | population=82 rows=82, all defects 0 |
| 2 | production ledger @ base | 3-cell, p1,p2 | TARGET_MET | (before-state behaviour) |
| 3 | frozen control | 3-cell (checker's own grammar) | TARGET_MISSED | **uncovered=82 dangling=2 malformed=2**, bad_pointer=0, self_arg=self_canon=0, bad_context=0 |
| 4 | frozen control | 4-cell, p2,p3,p4 | **TARGET_MET** | bad_pointer=0, self_arg=0, bad_context=0 (self_canon=1) |
| 5 | frozen control | 4-cell, p4 only | **TARGET_MET** | bad_context=0 on the control's generic text |
| 6 | frozen control | 4-cell, p1–p4 | TARGET_MISSED | **dup=1** (+uncovered=81) — the only failing field |
| 7 | fixture self-pointer ledger (canonical path) | p1–p4 | TARGET_MISSED | self_arg=5 self_canon=5 |
| 8 | fixture self-pointer ledger (canonical path) | p1,p2 | **TARGET_MET** | r51 counter also TARGET_MET 5/5 |
| 9 | same bytes at `docs/ledger-control.md` | p1–p4 | **TARGET_MET** | self_arg=0, self_canon=5, bad_context=0 |
| 10 | old counter, production @ base | — | TARGET_MET | `population=82 ledger_rows=82 … verdict=TARGET_MET` (matches `receipts/c1-base.txt`) |
| 11 | old counter, fixture | — | **TARGET_MET** | `population=5 ledger_rows=5 … verdict=TARGET_MET` |

### F17-1 — the frozen control fails on population structure, never on the named predicates

Control bytes (337 B, `sha256 ad72f72f…`), parsed (`receipts/control-parse.txt`):

```
line=3 cells=4
  cell1='tools/mado-verify.sh'
  cell2='quality/tool-ledger.md (commentary only)'
  cell3='nothing'
  cell4='generic accountability pointer to this ledger itself'
duplicate_row=1
```

Two facts follow directly from the bytes:

1. The control is a **4-column table** (`Tool | Reads | Writes | Owner`), not the 3-cell ledger
   grammar the production ledger uses and `quality/check-tool-ledger.py` enforces
   (`| path | description | pointer |`). Under the enforced grammar both rows are **malformed**:
   row 3 above gives `dangling=2, uncovered=82` with `bad_pointer=0, self* =0, bad_context=0` —
   the pointer and context predicates are **never consulted** (result row 3).
2. Read in its own 4-column shape (pointer := `Reads`, description := `Writes+Owner`), the
   self-pointer becomes visible (`self_canon=1`) but **p2/p3/p4 all pass** (result row 4), and
   p4 passes on the control's own generic prose (result row 5). The only failing field in the
   whole-row run is `dup=1` (result row 6), i.e. population uniqueness.

So "fail on `controls/c1-do-nothing.md` specifically for self-pointer/context defects" is
**not reproducible as worded**: in every reading the control is caught by uniqueness/malformed
rows first, and when those are excluded the self/context predicates accept it.

### F17-2 — non-self defined by the scored ledger path is bypassed

The counter must accept a non-canonical ledger path to score the control: the control is
**untracked at the base revision** (`git status --porcelain` → `?? .ufo/waves/round-52/controls/`),
so it can only be fed as a file/alternate path. With `--ledger-file`, "self = scored ledger" can
never fire (`self_arg=0` in results 4–6) even though the pointer names a ledger (`self_canon=1`).

The same construction is a full bypass for a work-free ledger: the fixture's five unique rows
point only at the ledger itself, and all four predicates return **TARGET_MET** when the ledger is
scored at `docs/ledger-control.md` (result 9: `uncovered=0 dup=0 dangling=0 bad_pointer=0
self_arg=0 bad_context=0`). The identical bytes are rejected only when scored at the canonical
path (result 7). Reproduced: **yes**.

### F17-3 — context predicate passes the control's generic description, and docstrings

- Control description `nothing | generic accountability pointer to this ledger itself` shares
  three tokens (`nothing`, `pointer`, `itself`) with `tools/mado-verify.sh` bytes, clearing the
  ≥2-token threshold → `bad_context=0` (result 5). A large instrument's own vocabulary is enough
  to certify "instrument-specific" context.
- The fixture's descriptions are the instruments' docstrings (zero accountability: no reads,
  writes, owner) and still score `bad_context=0` (results 7–9). The production ledger is composed
  the same way by design ("read from its own header"), so the context check as operationalised
  certifies self-description, not accountability.

### F17-4 — the before-state survives a counter that only fails the control

`quality/counters/c1-r51-ledger.py` at base reproduces the frozen receipt exactly
(`receipts/c1-base.txt` vs result 10), and it accepts the no-work self-pointer fixture at
`population=5/5` (result 11). A new counter that keeps the r51 checks and adds a duplicate/
population-balance clause fails the control (F17-1) while leaving the ledger-wide self-pointer
defect fully open — the claim's stated target is then unmeasured.

## Production-side pins (for the implementer)

`receipts/pointer-classes.txt`, production ledger @ base: 82 rows; pointer roots
`SCORECARD.md` 42, `PROVINCE.md` 20, `corpus/` 12, `.ufo/` 8 (of which **3** are
`.ufo/waves/round-51/registration.md`); **0** rows point at their own path or at
`quality/tool-ledger.md`; description length min/median/max 92/175/212. A "non-self" rule that
treats predicate-registration documents as self would fail production on 3 rows — the class
definition has to be stated, and the frozen text does not state it.

## Reproduced

| finding | reproduced |
|---|---|
| F17-1 control fails only on population structure (results 3,4,5,6) | **yes** |
| F17-2 non-self-by-scored-path bypass (results 7 vs 9) | **yes** |
| F17-3 generic/docstring context passes (results 5,7,8,9) | **yes** |
| F17-4 r51 before-state accepts no-work self-pointers (results 10,11) | **yes** |
| C1 production pass under all four predicates (result 1) | **yes** (82/82) |

## Dissent / failed controls, honestly

- I could not test a **built** C1 counter: none exists at base (`quality/counters/` has no r52
  file). The attack is on the frozen predicate text and its negative sample, using a reference
  implementation; a counter that hardcodes `quality/tool-ledger.md` as self and rejects
  self-referential boilerplate in the description would resist F17-2/F17-3 — but it would then
  implement definitions the frozen sentence does not name, and its control would still pass the
  raw predicates (F17-1).
- p4 is one faithful lexical reading (token overlap/basename). A stricter reading (require a
  read/write artefact token absent from the ledger's own text) would reject the control; that
  variation *is* the under-specification being reported.
- The control is a 2-row sample, not a full 82-row ledger; I scored it both as a 2-row ledger
  (population from base) and in its own 4-column shape. Scale does not change the ordering
  (structure before predicates), but the 82-row production run is the only real-scale check.
- Control bytes were frozen before this seat ran; checksums pinned in `receipts/inputs.txt`
  (`sha256 ad72f72f64708d1b877d0f2233f32a065bd11689d644af669176d1844ba2eba6`). The control is
  untracked, so "committed control" in the registration could not be verified against a revision.

## What would close the hole (constructive, no predicate edit proposed)

1. Score the control through the **same grammar** as production (3-cell), with unique rows, so the
   self/context predicates are actually reached.
2. Define **self by class**, not by the scored path: any pointer into a ledger or predicate
   registration (`.ufo/waves/*/registration.md`, `controls/*.md`) is self, and state it.
3. Make context reject self-referential boilerplate: require the description to name a read or
   write artefact (path, flag, socket, stream) distinct from the ledger, not merely the
   instrument's own vocabulary.
4. Add the F17-2 fixture (`docs/ledger-control.md` shape: unique rows, ledger-class pointers,
   docstring descriptions) as a second negative sample; it is the sample the frozen control fails
   to be.

## Limitations

- Source-only: no package queries, live reads, producer execution, screenshots or input capture.
- No semantic entailment is claimed: p1–p4 are bounded accountability checks, as the claim
  requires.
- Fixture is 5 files; production is 82. Only the production run exercises real scale.
- Reference implementation is seat-local (`pred4.py`); it is a measuring instrument for the
  frozen wording, not a proposed lane artifact. Its own p3 `canonical` reading is shown alongside
  `arg` precisely because the frozen text does not choose between them.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify17.md` — this report
- `.ufo/waves/round-52/w1/Falsify17/pred4.py` — reference implementation of p1–p4 (`sha256 f9ff260c…`)
- `.ufo/waves/round-52/w1/Falsify17/receipts/inputs.txt` — pins, versions, checksums, disk guard
- `.ufo/waves/round-52/w1/Falsify17/receipts/pred4-matrix.txt` — results 1–9 with commands
- `.ufo/waves/round-52/w1/Falsify17/receipts/old-counter.txt` — results 10–11
- `.ufo/waves/round-52/w1/Falsify17/receipts/pointer-classes.txt` — production pointer histogram
- `.ufo/waves/round-52/w1/Falsify17/receipts/control-parse.txt` — control cell/duplicate dump
- `.ufo/waves/round-52/w1/Falsify17/receipts/production-ledger-at-base.md` — `85d57a8:quality/tool-ledger.md`
- `.ufo/waves/round-52/w1/Falsify17/fixture/build-fixture.sh` — rebuilds the seat-local fixture repo
- `.ufo/waves/round-52/w1/Falsify17/fixture/controls/c1-do-nothing.md` — control bytes as scored
- `.ufo/waves/round-52/w1/Falsify17/fixture/tools/ti-alpha.py`
- `.ufo/waves/round-52/w1/Falsify17/fixture/tools/ti-beta.py`
- `.ufo/waves/round-52/w1/Falsify17/fixture/tools/ti-gamma.py`
- `.ufo/waves/round-52/w1/Falsify17/fixture/quality/tool-ledger.md`
- `.ufo/waves/round-52/w1/Falsify17/fixture/quality/check-tool-ledger.py` — base bytes, fixture pin
- `.ufo/waves/round-52/w1/Falsify17/fixture/quality/counters/c1-r51-ledger.py` — base bytes, fixture pin
- `.ufo/waves/round-52/w1/Falsify17/fixture/docs/ledger-control.md` — bypass vehicle (identical bytes, other path)

Report: .ufo/waves/round-52/w1/Falsify17.md
