# CritSeparability — critic report, mado round 36 wave 1

Seat: `L1Mado36.CritSeparability` (critic). Lane: mado-shokunin.
Assignment: `round-36/w1/prompts/CritSeparability.md` — attack causal separability
between C1 and C2.

**Reading of the claim map (verified against `registration.md:24-124` and the frozen
specs):** claim **C1** (calibration) is scored by the discrimination gate
`quality/check-counter-discrimination.py` over **both** repaired counters
(`quality/counters/c1-idle-lock.py` = `PRED-C1-r36-v1`, `quality/counters/c2-ledger.py`
= `PRED-C2-r36-v1`). Claim **C2** (operability) is scored by the pointer gate
`quality/check-evidence-pointers.py` (`PRED-PTR-r36-v1`). The registration calls the two
claims "causally separable" (`registration.md:22`, `:227`). This report tests that claim
on the committed artifacts.

## Verdict summary

**The two verdicts are causally separable; a shared ARTIFACT surface couples them

one direction, and that coupling is structural, not incidental.** C2's target cannot be
met with C1's artifacts absent *if* the round-36 records cite them (they do, today, in
C1's own section); C2 *can* be met with C1's cheap still red. C1's target can be met
with C2 entirely absent. This is not a defect in either claim — it follows from the
gate designs — but the registration's "neither reads the other's output" sentence
(`SCORECARD.md § Round 36`) is only true at the *instrument* level, not at the
*record* level.

## 1. Input topology (from the shipped code)

C1 gate inputs (`quality/check-counter-discrimination.py:75-197`): the manifest, the two
counter scripts, the `c1` control trees, `gen-mutants.py` + the `c2` ledger inputs for
the eight mutants, and a receipt directory (`--receipts`, default
`.ufo/waves/round-36/controls/receipts`) **which the gate itself writes**. C1 does not
read `LOG.md`, `SCORECARD.md`, the lesson, `quality/receipts/`, or `git status`.

C2 gate inputs (`quality/check-evidence-pointers.py:115-215`): `LOG.md`, `SCORECARD.md`,
`corpus/lessons/round-36.md` at the checked rev, `git ls-tree` of that rev, `git status
--porcelain` over the ten `INHERITED_PATHS`, and `quality/receipts/axis-<40hex>.txt`.
C2 never runs the counters and never reads the manifest, `clauses.json`, the blob ledger,
or the control receipts. There is **no path from C1's verdict to C2's verdict**.

## 2. Counterexample A: C2 target met while C1's claim is red (the instruments say so)

- C2's target has five conjuncts (`check-evidence-pointers.py:192-199`): `setup_ok`,
  `dangling_r35_closed==1`, `len(dangling36)==0`, `inherited_dirty==0`,
  `scratch_disposition_ok==1`, `tip_axis_transcript==1`. None of them reads any C1
  outcome.
- The gate's before-run at the freeze commit already had `dangling_r36=0` and
  `inherited_dirty=0` with **zero** round-36 artifacts present
  (`before-pointers.txt`: `pointers_r36=0 dangling_r36=0 inherited_dirty=0 …
  setup=missing-r36-sections`). The only things standing between that state and
  `TARGET_MET` are record fixes (correction pair, disposition, axis transcript,
  round-36 sections) — none of which requires C1's counters to discriminate.
- Today, C2 passes at tip: `PRED-PTR-r36-v1 rev=HEAD pointers_r35=8 dangling_r35=2
  dangling_r35_closed=1 pointers_r36=34 dangling_r36=0 inherited_dirty=0
  scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok
  verdict=TARGET_MET` (exit 0). C1's counters could be replaced by degenerate ones and
  C2's line would not change.
- **Direction-1 conclusion: C2 does not depend on C1's target.**

## 3. Counterexample B: C1's counter met while C2 is entirely absent (empirically)

Run of C1's gate with receipts and mutants redirected outside the lane (no lane write):

```
$ python3 -I quality/check-counter-discrimination.py --profile r36 \
    --manifest .ufo/waves/round-36/controls/manifest.json \
    --receipts /tmp/critsep-c1/receipts --mutants /tmp/critsep-c1/mutants
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=25/25 label='round-36 repaired counters' verdict=TARGET_MET
exit=0
```

The gate's verdict depends on the manifest, the counters, the control trees, the
generator, and the receipts it writes itself — never on any C2 deliverable (LOG/SCORECARD
corrections, scratch disposition, axis transcript all untouched; the gate never reads
them). Even the do-nothing "before" leg (`--profile r35`, `correct=14/25`, recorded in
`before-discrimination.txt`) ran before any round-36 build.

- **Direction-2 conclusion: C1 does not depend on C2's target.**

## 4. The coupling artifact: `.ufo/waves/round-36/controls/receipts/` and the records

The one surface that couples the two claims is the **round-36 record** (LOG § Round 36,
SCORECARD § Round 36, `corpus/lessons/round-36.md`):

- C2's `dangling_r36` observable resolves **every** lane-relative backtick pointer in
  those sections at the checked rev (`check-evidence-pointers.py:145-147`).
- The round-36 sections cite C1's artifacts by path: LOG.md:2130-2138 cites
  `quality/counters/c1-idle-lock.py`, `quality/counters/c2-ledger.py`,
  `quality/check-counter-discrimination.py`; `corpus/lessons/round-36.md` cites
  `quality/counters/c1-idle-lock.py`, `quality/counters/c2-ledger.py`,
  `quality/check-counter-discrimination.py`, `.ufo/waves/round-36/c2/gen-mutants.py`,
  `.ufo/waves/round-36/ledger/RevFrozenBlobs-r36.md`, `.ufo/waves/round-36/c2/frozen.json`.
- Therefore C2's gate *structurally inherits* the existence (not the correctness) of
  C1's artifacts. If C1's deliverable were missing, the sections would cite unresolvable
  paths, `dangling_r36` would be >0, and C2 would fail — even if every C2-specific fix
  were in place. This is a requirements-level coupling: **C2's target is not met if C1's
  artifacts do not exist as cited**.

Two related observations, both minor:

1. The default `--receipts` directory
   (`.ufo/waves/round-36/controls/receipts/`) is produced by the C1 gate, but C2 only
   touches it *if the records cite it*. Today no record section cites it, so the
   directory is not currently on C2's surface; the coupling rides the prose, not the
   directory.
2. Within **C1 itself** there is a *self*-reference: `clauses.json`
   (`CLAUSES-r36-v1`) names the same receipt paths the discrimination gate writes, and
   `c2-ledger.py:148-153` reads them from the working tree. The predicate's word
   "committed" (frozen.json/c2:3) is not enforced — the counter accepts uncommitted
   receipts (`receipt.is_file()` on the working tree). I record this as an instrument
   nit (it weakens C1's own kill-rule slightly and contradicts the predicate text), but
   it does not affect the C1↔C2 coupling question: C2 still reads only committed bytes
   via `git ls-tree`, so C2's target genuinely requires C1's artifacts *committed*
   when cited.

## 5. Is the coupling incidental or structural?

**Structural.** It is not an accident of who wrote the LOG. C2's gate is defined as a
claim about "the lane's own records" (`registration.md:91-97`), and the round-36 records
must describe the round's work — which includes C1. Any truthful round-36 record that
names C1's counters and evidence imports C1's artifact existence into C2's observable.
The only way to decouple them would be to exempt C1's own artifacts from the round-36
record — which would make the record unverifiable — or to change C2's claim to
"records except C1's evidence", which would be a different claim. The register's own
"causally separable" phrasing (`registration.md:22`) is therefore accurate for the
**verdicts** but overbroad for the **artifacts**.

## 6. Minimal separation

C1 needs nothing from C2 (verified in §3). The minimal separation is a **one-sided
convention**, not a design change:

- **Required:** C1's artifacts must be committed before the round-36 record sections are
  written, and the record sections must cite only committed paths (today, both hold —
  the gate passes). This is the "C2 gate runs after C1's artifacts land" ordering.
- **Sufficient:** C2's `dangling_r36` stays as-is. The receipts/existence coupling does
  not need to be removed because it never *falsely blocks* C2: it only makes C2 fail
  when the record is dishonest, which is the gate's entire purpose.
- **Optional tightening (does not change either verdict):** the c2-ledger counter's
  claim "committed receipt" should be made true by reading `git ls-tree`/`git show`
  rather than the working tree (`c2-ledger.py:148-153`), which would also make C1's own
  before/after discrimination more honest (currently a stale uncommitted receipt
  satisfies `c2-live`).

## Evidence commands quoted

```
$ python3 -I quality/check-counter-discrimination.py --profile r36 --manifest .ufo/waves/round-36/controls/manifest.json --receipts /tmp/critsep-c1/receipts --mutants /tmp/critsep-c1/mutants
MADO_DISCRIMINATION: profile=r36 instruments=c1,c2 controls=25 correct=25/25 label='round-36 repaired counters' verdict=TARGET_MET
exit=0

$ python3 -I quality/check-evidence-pointers.py --rev HEAD --repo .
PRED-PTR-r36-v1 rev=HEAD pointers_r35=8 dangling_r35=2 dangling_r35_closed=1 pointers_r36=34 dangling_r36=0 inherited_dirty=0 scratch_tracked=124 scratch_disposition_ok=1 tip_axis_transcript=1 setup=ok verdict=TARGET_MET
exit=0
```

Frozen receipts re-read, not rerun: `before-discrimination.txt` (14/25) and
`before-pointers.txt` (TARGET_MISSED at 4243d03 with `dangling_r36=0`). Git tip at
audit: `a5f76c9a018319ae04dea9206f5339325a41b31d` (only 3 dirty working-tree files —
two after-receipts, one wave report — none on any C1/C2 read path).

## Bounds compliance

Read-only on all production files; the only lane write is this file (scratch dir).
Scratch /tmp used: `/tmp/critsep-c1/receipts`, `/tmp/critsep-c1/mutants` (C1 gate runs).
No tools installed (no new tool was needed).
