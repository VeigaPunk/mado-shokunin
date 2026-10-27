# MistakeMiner — mado round 52, w1

Seat `MistakeMiner` (scribe, leaf). Lane `mado-shokunin`, base `85d57a818c3707397e21c840b6498b105ba798aa`.
Axes named: **coverage** and **operability**. Source-only round per `SKILL.md` standing rules; no claim or
predicate edits, no tracked writes, no live reads, no package queries, no producer execution. This report is
not a vote and grades no axis.

Assignment read order honoured: `.ufo/waves/round-52/claims-frozen.md` and `registration.md` first, then the
round-51 lesson and verifier spot-check.

## 1. What I read

- Frozen claims: `claims-frozen.md:5-7` (C1 target), `:9-11` (C2 target), `:13` (causal separation).
- Frozen registration: `registration.md:7` (C1 predicate incl. "fail on `controls/c1-do-nothing.md`
  specifically for self-pointer/context defects"), `:9` (C2 predicate), `:15` (frozen controls; "Controls
  cannot be changed after workers score them").
- Round-51 lesson: `corpus/lessons/round-51.md:25` (ledger-wide self-pointer satisfies the r51 predicate),
  `:36` (M51-2, captured-by none at predicate level), `:38` (M51-3 fixture mismatch), `:40` (W2 residuals).
- Round-51 verifier spot-check: `corpus/lessons/round-51-verifier-spotcheck.md:34-35` (C1 verdict text: proves
  inventory/name presence, not contextual accountability), `:80-81` (routed defects for round 52).
- QUALITY: `corpus/QUALITY.md:324` (36), `:362` (56), `:364` (57), `:366` (59), `:576` (104), `:580` (105).
- Instruments: `quality/counters/c1-r51-ledger.py` (`:24-29` clause docs, `:158-174` row parser, `:197`
  substring containment), `quality/check-tool-ledger.py:258-325`, `quality/check-counter-discrimination.py:8-10`.
- Committed controls and receipts: `.ufo/waves/round-52/controls/c1-do-nothing.md:1-4` (sha256
  `ad72f72f64708d1b877d0f2233f32a065bd11689d644af669176d1844ba2eba6`), `controls/c2-do-nothing.md:1`,
  `receipts/c1-base.txt:3`, `receipts/c2-base.txt:7`.
- Round-51 C1/C2 evidence: `w2/SentinelC1Pointers/pointer-audit.md:48-52` and
  `receipts/fixture-allself-counter.txt:4`; `w2/CritC1GenericDesc.md:8-16`; `w2/RevC2EntryTruth/entry-truth.md`
  `:7,27,46,54,61,77,95`; `receipts/c2-at-data.txt:7`; `receipts/c2-after-errata.txt:7`.
- Round-36 class origin: `corpus/lessons/round-36.md:163-189` (M36-3, attribution).
- Round-52 plan intent: `SCORECARD.md:2781`, `:2791-2793`; candidate seeded at
  `.ufo/waves/round-52/mistake-candidate.md:5` (M52-1).

No new source was opened and no source candidate is proposed; no source URL/access date is owed by this seat.

## 2. Mistake class: **non-attributable red arm**

**Class.** A claim's failing control fails for a reason the claim did not name, or the predicate is invariant
to the named defect, so `TARGET_MISSED` does not demonstrate the clause the claim credits. This is M36-3
raised from counter-internal clauses to the *claim's* control set; the grammar half is M51-3 recurring one
level up. Prior art already states the test: `corpus/QUALITY.md:362` (every live clause must name a control
for which it is load-bearing), `:364` (score frozen and competing-clause-free copies; a control whose two
verdicts differ in which cite is open has an attribution defect), and the gate design at
`quality/check-counter-discrimination.py:8-10` ("each differing from an accept control in exactly one
committed input").

### 2.1 Finding M52-M1 — the frozen C1 control is not the ledger shape and fires four competing clauses

**Items attacked (no text edit).** `controls/c1-do-nothing.md` as the red arm for PRED-C1-r52
(`registration.md:7,15`; `claims-frozen.md:7`). Not attacked: the target sentence, the production ledger.

**Committed-bytes shape (measured).** `wc -l` = 4; every line has 4 pipe cells (`awk -F'|'`); two rows for one
instrument; no backticked path; the pointer path appears in the *Reads* column, while the pointer columns hold
`nothing | generic accountability pointer to this ledger itself`. The base ledger contract is 3 cells with a
backticked path in cell 1 (`quality/tool-ledger.md:9-18` at base; parser `c1-r51-ledger.py:155-174`).

**Fixture A (control bytes as the ledger value).** Clone of the lane at base, `quality/tool-ledger.md`
replaced by the control file, one fixture commit; toplevel asserted to the fixture path:

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo <fx/control> --rev a42e3e78... --work <scratch>
C1_R51: population=82 ledger_rows=2 uncovered=81 dangling=0 bad_pointer=1 empty_desc=0 selftest=ok dup=1 checker=failed verdict=TARGET_MISSED rev=a42e3e780388b2d78d6a9adf7ec97616316b14a4
exit=1
# child checker on the same bytes: LEDGER: population=82 ledger_rows=0 uncovered=82 dangling=2 ... TARGET_MISSED
```

Receipt: `w1/MistakeMiner/receipt-control-as-ledger.txt` (full 81-line uncovered list and checker rows). The
MISS is closed by uncovered=81, dup=1 and bad_pointer=1 (no pointer token at all), before any non-self or
context rule can be load-bearing. The lane's two instruments even disagree on the same bytes (2 rows vs 0
rows), which shows two grammars rather than one control shape.

**Fixture B (isolating self-pointer defect).** Same clone; only cell 3 of each of the 82 data rows rewritten
to `quality/tool-ledger.md` (cells 1-2 unchanged, verified 82/82:

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo <fx/allself> --rev d60ea788... --work <scratch>
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=d60ea78851ffdb67277c357dc4856d7e5d1d5bfb
exit=0
```

Receipts: `w1/MistakeMiner/receipt-allself-at-base.txt`, `w1/MistakeMiner/receipt-b-rewrite-check.txt`.

**Why actionable now.** `registration.md:7` requires the control to fail **specifically** for self-pointer/
context defects. Fixture A cannot do that: a counter that implements only the pre-existing coverage and
uniqueness checks already returns MISS on it, and the control does not exercise a resolvable non-self target
or an instrument-specific description in isolation. The defect the claim names is instead exercised by
Fixture B, which the *base* predicate marks `TARGET_MET` — so the defect is real and measured at the frozen
base, but the frozen control does not measure it.

**Captured-by.** QUALITY 56 (`corpus/QUALITY.md:362`) and 57 (`:364`) already state the requirement; QUALITY 36
(`:324`) only keys control receipts by file-name shape. Gap: no instrument in `quality/` scores a claim-level
control's clause attribution (the only clause-ledger instrument is the r36 predicate's own counter,
`quality/counters/c2-ledger.py:32`, which scores that predicate rather than a round claim), and the round-52
registration does not require a clause ledger or attribution receipt for PRED-C1-r52.

**Fix, shown able to fail.** (a) Each red control is the accept fixture with exactly one input family changed
(precedent `check-counter-discrimination.py:8-10`): Fixture B for the non-self clause; a second copy with all
82 descriptions replaced by one generic sentence for the context clause (shape already receipted in round 51,
`w2/CritC1GenericDesc.md:8-16`); (b) score frozen and competing-clause-free copies and commit the attribution
receipt naming the load-bearing clause (QUALITY 57). The criterion is shown able to fail on committed bytes:
it rejects the frozen control (Fixture A, four competing clauses incl. grammar) and accepts Fixture B as the
correct isolating arm. The new counter then owes the pair: production ledger `TARGET_MET`
(`receipts/c1-base.txt:3`) and Fixture B `TARGET_MISSED`. The new counter is absent at base
(`ls quality/counters | grep -c r52` → 0; `claims-frozen.md:7`), so that MISS is an acceptance test, **not an
observed result**; I did not build or run it.

**Limits.** Fixture A is the only faithful reading of "is the committed ledger shape" (`registration.md:15`);
if the new counter instead treats the file as a shape descriptor, no ledger-shaped control exists and the
demonstration is not reproducible at all — the attribution gap holds either way, but the exact counts would
depend on the harness. Controls cannot be changed after scoring (`registration.md:15`), so the fix is an
*additional* attribution fixture, not an edit to the frozen control.

### 2.2 Finding M52-M2 — the C2 red arm exercises entry presence only; the structural counter is invariant

**Item attacked.** `controls/c2-do-nothing.md:1` as the red arm for PRED-C2-r52 (`registration.md:9,15`;
`claims-frozen.md:11`).

**Measured invariance.** PRED-C2-r51 checks four clauses — index, source rows/pins/quotes, shingle overlap,
held tokens (`quality/counters/c2-r51-dispatch-entry.py:10-20`) — and no proposition→source mapping. At the
defective data revision the counter reports `clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET`
(`round-51/receipts/c2-at-data.txt:7`, rev `a0e34387`); at the corrected revision it reports the identical
line (`c2-after-errata.txt:7`, rev `b742d54c`). The defects between those revisions are enumerated at
`round-51/w2/RevC2EntryTruth/entry-truth.md:7,27,46,54,61,77,95` (unsupported comma preservation, runtime
called config-time, five-name miscount, mouse reporting misattributed, running-host branch from a directory
listing). The same counter is `TARGET_MET` at the round base on the already-landed entry
(`receipts/c2-base.txt:7`).

**Why actionable.** "A new committed counter checks proposition count, row/pin/quote bindings and complete
mapping" (`registration.md:9`) has no reject fixture. The base-absence control closes clause (a) only; the
mapping clauses have no control, so they are uncontrolled and cannot be shown load-bearing (QUALITY 56).

**Captured-by.** QUALITY 56/57 as above. QUALITY 104 (`corpus/QUALITY.md:576`) does capture the prose defect —
it names the RevC2EntryTruth findings as its shown-fail arm — but it is a post-hoc manual audit and its own
text records that "the frozen C2 predicate still returns TARGET_MET at the corrected revision"; it does not
gate the predicate. QUALITY 105 (`:580`) covers attack-fixture grammar only.

**Fix, shown able to fail.** Three reject variants of the accept entry — (i) one material proposition with no
row/pin/quote, (ii) a 26-word quote against the ≤25-word cap, (iii) a wrong pin line or row id — each must
return `TARGET_MISSED` for its named clause, beside an accept copy that returns `TARGET_MET`; receipts name
the clause (QUALITY 57). Shown able to fail: the pre-fix instrument is demonstrably invariant across a
defective and a corrected entry (`c2-at-data.txt:7` vs `c2-after-errata.txt:7`), so a criterion requiring the
counter to disagree on variant (i) is already falsified by committed bytes. The new counter's MISS on the
variants is **unmeasured** (counter absent at base; `C2CounterDraft` seat owns it).

**Limits.** Semantic entailment stays outside any counter (`claims-frozen.md:11` admits this); the outside
reviewer arm remains the only source-truth test. I built no variants and ran no new counter.

## 3. Prior related evidence sweep

| Round | Pointer | What it establishes for this class |
|---|---|---|
| 36 | `corpus/lessons/round-36.md:163-189` (M36-3) | Ten reject controls died at an earlier fence; `TARGET_MISSED` named no clause; fix = score frozen + competing-clause-free copy; limit recorded honestly. |
| 35-36 | `corpus/QUALITY.md:362` (56), `:364` (57), `:366` (59) | Clause ledger, load-bearing attribution, vacuous-control rule — text exists since r35/r36. |
| 35 | `quality/check-counter-discrimination.py:8-10` | Accept/reject design where each reject differs from an accept in exactly one committed input — the model for an isolating control. |
| 51 | `corpus/lessons/round-51.md:25` | Ledger-wide self-pointer satisfies the r51 basename-presence check (stronger residual than the earlier comment-only pointer). |
| 51 | `w2/SentinelC1Pointers/pointer-audit.md:48-52`, `receipts/fixture-allself-counter.txt:4` | 82-row all-self-pointer ledger: checker and counter both `TARGET_MET` at freeze `56026fcb`. |
| 51 | `w2/CritC1GenericDesc.md:8-16` | 82 rows with one identical generic description and a basename dump: `TARGET_MET` at `4801609f`. |
| 51 | `corpus/lessons/round-51.md:38` (M51-3) | Attack fixture rejected for grammar, not for the claimed defect — same family, one level down; fix landed as QUALITY 105. |
| 51 | `w2/RevC2EntryTruth/entry-truth.md:7,27,46,54,61,77,95` | Concrete unsupported propositions in the admitted entry. |
| 51 | `receipts/c2-at-data.txt:7` vs `c2-after-errata.txt:7` | Structural counter invariant to those propositions; `TARGET_MET` before and after errata. |
| 51 | `corpus/lessons/round-51-verifier-spotcheck.md:34,80-81` | Outside verifier: predicate proves name presence, not contextual accountability; both residuals routed to round 52. |
| 52 | `controls/c1-do-nothing.md:1-4`; `controls/c2-do-nothing.md:1` | The frozen red arms, non-isolating as committed (measured §2.1/§2.2). |
| 52 | `w1/MistakeMiner/receipt-*.txt` | Base-revision measurement: control MISS for four competing clauses; isolating all-self ledger MET. |

## 4. Recommendation routed to the round (report only; no edits)

1. C1 seats: treat the committed control as a shape illustration, not the attribution arm; add the isolating
   82-row self-pointer fixture and a generic-description copy, each with a clause-named receipt, and require
   the new counter to MISS both while MET on production.
2. C2 seats: add the three reject variants and clause-named receipts before the mapping clauses are credited;
   keep the outside source-truth sample as the only entailment arm.
3. Integration/closure: apply QUALITY 56/57 to the two new counters' control sets; the frozen controls remain
   untouched per `registration.md:15`.

## 5. Boundaries, safety, cleanup

- Writes: this report and `w1/MistakeMiner/` only. No tracked lane file, fleet file, state/watchdog,
  scripts/templates, or shokuknow write; `git status --porcelain` at the lane shows only the untracked
  round-52 directory.
- Scratch: `/fast/scratch/hyaku/mado-r52/MistakeMiner/` (disk guard read first: /fast 600 G free). Two
  throwaway `git clone --shared` fixtures at the base revision, toplevel asserted before each fixture commit
  (`git rev-parse --show-toplevel` printed the fixture path). Fixtures and work dirs deleted after capture;
  receipts retained here.
- Executions: the committed counter/checker only, over committed blobs in the fixture clones — no host probe,
  no compositor/process read, no package query, no install, no producer run, no lane git/jj mutation.
- Not established: no new counter, no claim verdict, no axis score, no source-truth judgment beyond citing the
  round-51 audit, no C2 variant measurement, no statement about the round's eventual TARGET_MET.

## Deliverables

- `.ufo/waves/round-52/w1/MistakeMiner.md`
- `.ufo/waves/round-52/w1/MistakeMiner/measure-control-shape.sh`
- `.ufo/waves/round-52/w1/MistakeMiner/receipt-control-as-ledger.txt`
- `.ufo/waves/round-52/w1/MistakeMiner/receipt-allself-at-base.txt`
- `.ufo/waves/round-52/w1/MistakeMiner/receipt-b-rewrite-check.txt`

Report: .ufo/waves/round-52/w1/MistakeMiner.md
