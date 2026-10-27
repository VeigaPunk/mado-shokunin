# W2 Attack03 — C1 population and row grammar omission

Seat: Attack03 (mutation-tester, W2 attack item #03). Scope: falsify round-52 frozen
claim C1 (operability) on its **population** and **row-grammar** clauses only, after W1
evidence. Attack wave, not a vote; no predicate amendment; no claim made about C2 or
about any non-author's judgment. Read-only against the lane: every run below executes a
counter copy that issues `git ls-tree` / `git show` / `git rev-parse` only.

- Base / HEAD: `85d57a818c3707397e21c840b6498b105ba798aa` (`git rev-parse HEAD` == base;
  the lane worktree already carries the round's own untracked/modified files; my probes
  changed nothing — restoration evidence in §6).
- Scratch: `/fast/scratch/hyaku/mado-r52/Attack03/` (removed after this report; §7).

## 1. Artifacts under test (three divergent r52 counter variants)

| variant | lane-root path | sha256 | state |
|---|---|---|---|
| A "lane copy" | `quality/counters/c1-r52-ledger.py` | `923faf02cd0c2db374f7757d38ef24fc8381c2882cb3d853882f0fadce1c17d7` (78 lines) | **untracked** working-tree file; this is the integration path named by the W1 draft header |
| B "draft" | `.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py` | `0fe862f116a789e8f6bebf38dea74b1f5ee20b3c810190ecf295621a3c34dc31` (847 lines) | wave-dir copy of the C1CounterDesign draft |
| C "reference" | `.ufo/waves/round-52/w1/C1Simplify/c1-r52-ledger.py` | `0d31fc6c748c018752d76730c3f539fe1449c94ea6114eef4ec1821d3c298957` (194 lines) | C1Simplify minimum reference |

Landing fact: `git log --all -- quality/counters/c1-r52-ledger.py` is empty and
`git ls-tree 85d57a818… -- quality/counters/c1-r52-ledger.py` is empty — **no r52 C1
counter is committed anywhere**; the frozen C1 clause "a new committed counter" is not
yet satisfied by any revision. All tested bytes are untracked candidates.

Provenance drift (observation, not judgment): C1Simplify §9 cites a "final" draft
`382a0606…` (787 lines); no file with that hash or length exists in the wave dir today.
Variant B (847 lines) reproduces the recorded W1 receipts byte-for-byte where it matters:
my B0-draft stdout sha256 `352d6bf67f6810a01502c67cea315d78edfae4c0e103e53f4141595c87db0b12`
equals `receipts/harness-summary.json` green `stdout_sha256`, and my R1-draft counts equal
`receipts/receipts.txt:31`. Variant A matches neither W1-measured byte string.

## 2. Attacked clauses

- `claims-frozen.md` C1: "a new committed counter distinguishes the production ledger
  from a no-work control … using unique population, non-self resolvable evidence targets,
  and instrument-specific context checks. **Demonstrate production pass and control fail
  at the frozen revision.**"
- `registration.md` C1: "validates **population row uniqueness**, resolvable evidence
  pointer, non-self pointer, and a description containing instrument-specific functional
  context. It must **pass on the existing production ledger at the base revision** and
  **fail on `controls/c1-do-nothing.md` specifically for self-pointer/context defects**."
- Row grammar context: production ledger `quality/tool-ledger.md` declares a three-cell
  grammar and contains a fenced grammar example (blob lines 11–13, sha256 of base blob
  `df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b`).
- W1 baseline being re-opened: C1ControlAttack / Falsify10 / Falsify19 / Falsify26
  (control confound), Falsify34 (anchored-duplicate uniqueness blindness in r51),
  Falsify02 (population P undefined in the predicate text).

## 3. Probes — mutant, expected detector, observed output, verdict

Driver: `probe.sh` in scratch (rebuildable from the commands below). Every run:
`python3 -I <counter.py> --repo <lane> --rev 85d57a818c3707397e21c840b6498b105ba798aa
[--ledger <fixture>] --work <scratch>/work`; fixtures are scratch copies; base ledger
fixture = `git show 85d57a818…:quality/tool-ledger.md`. Detector = the counter's own
bounded measurement; exit 0 = TARGET_MET, 1 = TARGET_MISSED, 2 = setup error.

| # | mutant / input | expected (frozen clause) | A lane copy | B draft | C reference |
|---|---|---|---|---|---|
| B0 | pristine production ledger (rev blob) | TARGET_MET, 82/82, exit 0 | **FAIL: `ledger_rows=83 dangling=1 bad_pointer=1` MISSED, exit 1** | MET `82/0`, exit 0 | MET `82/0`, exit 0 |
| M4 | pristine minus the fenced block (lines 11–13) | same as B0 if the fence caused B0's failure | MET `82/0`, exit 0 (causal isolation proven) | — | — |
| R1 | frozen control `controls/c1-do-nothing.md` (sha `ad72f72f…`) | MISSED **with self_pointer and/or generic_desc firing** | **VACUOUS: `ledger_rows=0 uncovered=82 dup=0 self_pointer=0 generic_desc=0`** — byte-identical counts to an empty file (probe E0) | **SPECIFIC: `ledger_rows=2 uncovered=81 dup=1 self_pointer=1 generic_desc=1`** (matches W1 receipt) | VACUOUS: `ledger_rows=2 uncovered=82 dup=0 dangling=2 self_pointer=0 generic_desc=0` |
| E0 | empty file | MISSED | `ledger_rows=0 uncovered=82 …` — **all counters identical to R1-A** | — | — |
| M1 | verbatim duplicate of the `tools/mado-verify.sh` row | dup=1, MISSED | killed: `dup=1` (note: also `uncovered=1`; A's `uncovered` counts a twice-covered instrument because it tests `by.get(p,0)!=1`) | killed: `dup=1`, `uncovered=0` | — |
| M2 | duplicate row with cell 1 `` `tools/mado-verify.sh:12` `` (Falsify34 shape) | dup=1 (uniqueness leg normalizes anchors), MISSED | **DETECTOR DEFECT: exit=2 `setup=error detail=fatal: path 'tools/mado-verify.sh:12' does not exist …`** — a ledger-content defect surfaces as a setup error; `dup` never evaluated | killed: `dup=1` (LINE_SUFFIX normalization on cell 1) | **DUP-BLIND: `dup=0 dangling=1 bad_pointer=0`** — killed only incidentally by the dangling leg; uniqueness leg sees the anchored duplicate as a distinct string |
| M3 | duplicate row placed inside a fenced block | fenced documentation must not be scored | `dup=1` from inside the fence (fenced content scored as rows, `ledger_rows=84`) | MET (fence skipped) | — |
| RC | `.ufo/waves/round-52/controls/c1-row-context-control.md` | MISSED, ideally naming self-pointer/context | `dup=1 generic_desc=2 self_pointer=0 bad_pointer=0` — fails for dup/coverage/short-desc; **self_pointer never fires** (pointer `PROVINCE.md:20` is not self; `PROVINCE.md` exists at base with 4 `mado-verify.sh` mentions) | — | — |

## 4. Findings (verdicts against the frozen clauses)

- **F1 — production-pass clause falsified for the integration-path bytes. REPRODUCED.**
  Variant A reports TARGET_MISSED on the pristine production ledger at the frozen base
  (`dangling=1 bad_pointer=1`); M4 isolates the cause to the fenced grammar example: with
  the fence removed the same counter returns MET. Root cause: `cells()`/`parse_ledger`
  in `quality/counters/c1-r52-ledger.py` have no fenced-block handling. Clauses hit:
  "must pass on the existing production ledger at the base revision" /
  "Demonstrate production pass … at the frozen revision". Variants B and C pass.
- **F2 — control-specificity clause not demonstrated by variants A and C. REPRODUCED**
  (this is the W1 C1ControlAttack confound, now measured against candidate bytes).
  On A, the frozen control yields exactly the same defect counters as an empty file
  (`ledger_rows=0 uncovered=82`, `self_pointer=0 generic_desc=0`): the registered
  "control fail" is satisfiable by any unparseable input, so a red receipt on A proves
  nothing about self-pointer or context detection. On C the control's rows are scored
  `dangling` (4-cell) with `self_pointer=0 generic_desc=0` — same vacuity, different leg.
  Only variant B fails the control *specifically* (`self_pointer=1 generic_desc=1`),
  because it scores >3-cell rows and derives the self signal from path-shaped tokens in
  every cell. Clause hit: "fail on `controls/c1-do-nothing.md` specifically for
  self-pointer/context defects". Consequence: the acceptance clause is variant-dependent;
  the bytes sitting at the integration path cannot support it.
- **F3 — population row uniqueness is anchor-blind outside variant B; variant A
  additionally misclassifies the defect as a setup error. REPRODUCED.** With cell 1
  suffixed `:12` (the Falsify34 shape), A crashes with exit 2 (`setup=error … does not
  exist`) and never evaluates `dup`; a harness that reads exit 2 as "counter rejected the
  argument set" (C1Fixture convention, per C1Simplify §5.4) would misreport this ledger
  defect. C reports `dup=0` and catches the mutant only via `dangling`. Only B normalizes
  cell-1 anchors and reports `dup=1`. Clause hit: "validates population row uniqueness".
  The mutant is killed in all three cases, but for A the *uniqueness leg itself* never
  fires and the failure surfaces in the wrong channel; that is a coverage/robustness
  finding on the uniqueness clause, not a surviving bypass.
- **F4 — fenced content is scored as ledger rows by variant A. REPRODUCED** (M3:
  `dup=1` from a row inside a fence). Same root cause as F1; stated separately because it
  means A's row/population accounting includes documentation bytes.
- **F5 — the second committed control cannot name self-pointer either. REPRODUCED
  (supplementary).** `.ufo/waves/round-52/controls/c1-row-context-control.md` drives A to
  `self_pointer=0`; its failure legs are dup + coverage + short description. Neither
  committed control isolates the self-pointer clause under variant A's grammar.

## 5. What this does NOT establish

- No verdict on variant B's context clause beyond population/grammar: the F3-forgery
  lexical ceiling (C1Simplify §6) was Attack01's seat and was not re-attacked here.
- No claim that any candidate is "the" scored artifact: nothing is committed; the claim's
  own "new counter absent → target not yet met" remains true at `85d57a818…`.
- No judgment of non-author reports beyond reproducing their measured outputs; where my
  numbers match a W1 receipt I say so explicitly (B0/R1 vs `C1CounterDesign/receipts`).
- Population definition deltas between variants (A includes any depth under
  `quality/counters/`, B only depth-1) are immaterial at base (both measure 82) and were
  not stress-tested on other tree shapes.

## 6. Restoration evidence

- All counter/ledger/control inputs were copied into scratch before any run; lane and
  wave originals were never opened for writing. sha256 before == after for all four
  guarded files (§1 table, re-measured post-probes, identical).
- `git status --porcelain` captured before and after the probe session: byte-identical
  (no new modified/untracked paths beyond the round's pre-existing ones).
- Detector on restored pristine bytes: A re-run exit 1 with output diff-empty vs first
  B0-lane run; B re-run exit 0, diff-empty vs first B0-draft run.
- Deviation recorded: one intermediate command redirected `git status` output to
  `/tmp/.a3-after.porcelain` (outside the seat scratch). The file was deleted in the next
  command; no other out-of-scratch write occurred. No git/jj mutation, no package query,
  no install, no live/probe/screen operation.

## 7. Scratch

`/fast/scratch/hyaku/mado-r52/Attack03/` (probe.sh, pristine/ copies, mutants/
m1-dup.md m2-anchor.md m3-fence-dup.md m4-unfence.md e-empty.md, runs/*.out, evidence/)
— removed after this report was written.

## 8. Reproduction (commands)

```
BASE=85d57a818c3707397e21c840b6498b105ba798aa; LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
git -C $LANE show $BASE:quality/tool-ledger.md > /tmp-ledger-copy   # into your scratch
python3 -I $LANE/quality/counters/c1-r52-ledger.py --repo $LANE --rev $BASE
#   -> C1_R52: population=82 ledger_rows=83 uncovered=0 dup=0 dangling=1 bad_pointer=1
#      self_pointer=0 generic_desc=0 verdict=TARGET_MISSED ... exit 1        (F1)
python3 -I $LANE/quality/counters/c1-r52-ledger.py --repo $LANE --rev $BASE \
  --ledger $LANE/.ufo/waves/round-52/controls/c1-do-nothing.md
#   -> ledger_rows=0 uncovered=82 dup=0 self_pointer=0 generic_desc=0 MISSED exit 1 (F2)
#      compare: --ledger <empty file> gives identical counters               (F2)
python3 -I $LANE/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py --repo $LANE \
  --rev $BASE --work <scratch>/work --ledger $LANE/.ufo/waves/round-52/controls/c1-do-nothing.md
#   -> ledger_rows=2 uncovered=81 dup=1 self_pointer=1 generic_desc=1 MISSED exit 1
```

Report: `.ufo/waves/round-52/w2/Attack03.md`
