# MutC2NoReceiptBind — mutation-tester report (mado round 36 wave 1)

Seat: `L1Mado36.MutC2NoReceiptBind`. Role: mutation-tester.
Prompt: `.ufo/waves/round-36/w1/prompts/MutC2NoReceiptBind.md`.
Assignment: write a `/tmp` variant of the round-36 C2 design whose receipt test is the
round-35 token grep (`verdict=TARGET_MISSED` anywhere in the file); run it against the
generated fixtures `c2-receipt-token` and `c2-receipt-unbound`; report each verdict and
prove the **binding** is what kills them.

## Target of mutation

The round-36 C2 design is `quality/counters/c2-ledger.py` (`PRED-C2-r36-v1`,
commit `a3094c99ab85bec35534de2447552c47dd2b647f`, sha256
`92db777e7573411835b8686f86520e1f891e8f5e44d6a9c3c18fe8c488193833`). The
repaired receipt test that separates this round from round 35 is its
`receipt_observable()` (lines 95–99), which requires all four of: `clause=<clause_id>`,
`observed=TARGET_MISSED`, and either `control=<control_id>` or `# control <control_id> `
in the receipt text. Round 35's check was only `verdict=TARGET_MISSED` anywhere in the
file (registration.md:16 mentions the round-35 fail-open token greps; the C2 counter docstring
states "A 'covered' clause only needed `verdict=TARGET_MISSED` to appear anywhere in a
receipt file").

## Mutant

Copied `quality/counters/c2-ledger.py` verbatim to `/tmp/mado-r36-mut-c2-no-receipt-bind.py`
(sha256 `27189c07b2074bcc9a3d4a5c15e75077ebfd08933232be93ababc65d2c2190a3`) and replaced
only the body of `receipt_observable()` with the round-35 token grep:

```python
def receipt_observable(text: str, clause_id: str, control_id: str) -> bool:
    # MUTANT (MutC2NoReceiptBind): round-35 token grep — the receipt test is
    # `verdict=TARGET_MISSED` appearing anywhere in the file. No clause-id or
    # control-id binding, no observed= requirement.
    return "verdict=TARGET_MISSED" in text
```

`diff` pristine → mutant shows exactly this one hunk (the earlier draft had a second,
unintended ROW-regex transcription change; it was corrected and the diff re-checked, so the
mutant differs from pristine in exactly the receipt test). The predicate/drift guard is kept
byte-identical: the mutant still refuses to run if the frozen spec text or target drifts.
The lane-run baseline below shows the mutant `TARGET_MET` on the live lane, so the mutation is
contained to the receipt test and does not break the rest of the gate.

## Fixtures

`/tmp/mado-r36-mutants-r36/c2-receipt-token` and `c2-receipt-unbound` existed; I
regenerated to `/tmp/mado-r36-mutants-r36-fresh` with the committed generator and
`diff -r` confirms the assigned fixtures are byte-identical to a fresh generation
(both `echo`-verified). Mutation notes (`mutation.txt`) confirm the single changed input:

- `c2-receipt-token`: `mutation=receipt-token`,
  `changed=['.ufo/waves/round-36/controls/receipts/c1-entry-symlink.txt']` — that file is
  now `verdict=TARGET_MISSED\n` (a one-line token file).
- `c2-receipt-unbound`: `mutation=receipt-unbound`,
  `changed=['.ufo/waves/round-36/controls/receipts/c1-entry-symlink.txt']` — that file now
  contains the `c1-row-duplicate` receipt, which names clause `row-unique` and control
  `c1-row-duplicate`, i.e. it does not bind to the `entry-regular` clause it sits under.

Both fixtures also received the lane's `RevFrozenBlobs-r36.md` blob ledger and the mutated
`clauses.json` (the fixture `clauses.json` sha256
`1762fde61f99f6954cd58b8f9e382fc66a0bbaec4225819568b78c150497bf79` in both fixtures; the
live lane's is `23896383e6012ed5e84eb3f47efdfe3248b9c15b1b2b5e22f33bcf11c0d7b44c` — the
fixtures are mutants of the live ledger, as intended for rejection controls).

## Runs (detector contract: `c2-ledger.py --repo <root> --frozen .ufo/waves/round-36/c2/frozen.json`,
`GIT_DIR=<lane>/.git`, `PYTHONDONTWRITEBYTECODE=1`)

### Baseline — pristine `quality/counters/c2-ledger.py`

```
### PRISTINE lane ###
PRED-C2-r36-v1 uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived
exit=0
### PRISTINE c2-receipt-token ###
PRED-C2-r36-v1 uncovered=1 retired=1 tip_ok=1 verdict=TARGET_MISSED
  uncovered: entry-regular receipt does not bind clause and control
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived
exit=1
### PRISTINE c2-receipt-unbound ###
PRED-C2-r36-v1 uncovered=1 retired=1 tip_ok=1 verdict=TARGET_MISSED
  uncovered: entry-regular receipt does not bind clause and control
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived
exit=1
```

The baseline passes (lane `TARGET_MET`, both fixtures `TARGET_MISSED`), so the verdicts
below are attributable to the mutant. (One earlier mutated fixture run hit a transient
`error=clause-ledger-missing`, exit 2, while a sibling seat was regenerating the shared
`/tmp/mado-r36-mutants-r36/` tree — the generator does a non-atomic `rmtree`+recreate.
The fixture dirs were byte-identical to fresh regeneration afterwards and the reruns below
are stable; runs are also corroborated on private copies under
`/tmp/mut-c2-no-receipt-bind/fixtures/`.)

### Mutant runs

```
### MUTANT lane (still-met check) ###
PRED-C2-r36-v1 uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived
exit=0
### MUTANT c2-receipt-token (assigned path) ###
PRED-C2-r36-v1 uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived
exit=0
### MUTANT c2-receipt-unbound (assigned path) ###
PRED-C2-r36-v1 uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived
exit=0
### MUTANT c2-receipt-token (scratch copy) ###
PRED-C2-r36-v1 uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived
exit=0
### MUTANT c2-receipt-unbound (scratch copy) ###
PRED-C2-r36-v1 uncovered=0 retired=1 tip_ok=1 verdict=TARGET_MET
  tip: computed 6d754bd599caa7ab21c4c20b548c0fa83914ffce, 7 rows re-derived
exit=0
```

## Verdict per fixture

| Fixture | Pristine | Mutant (r35 token grep) | Verdict |
|---|---|---|---|
| `c2-receipt-token` | `TARGET_MISSED` (exit 1) | `TARGET_MET` (exit 0) | **SURVIVED** — the mutant accepts the reject control. |
| `c2-receipt-unbound` | `TARGET_MISSED` (exit 1) | `TARGET_MET` (exit 0) | **SURVIVED** — the mutant accepts the reject control. |
| lane (still-met sanity) | `TARGET_MET` (exit 0) | `TARGET_MET` (exit 0) | mutant did not break the accept side |

## Proof that the binding is what kills them

`c2-receipt-token` passes only the token test: its changed receipt is exactly `verdict=TARGET_MISSED\n`
with **no** `clause=` line, **no** `observed=` line, **no** `control=` line. The pristine
counter rejects it (`uncovered: entry-regular receipt does not bind clause and control`);
the mutant's `receipt_observable` returns `True` for it, `uncovered=0`, and every other
observable is already at target (`retired=1`, `tip_ok=1`), so the verdict flips to
`TARGET_MET`. The only difference between the two verdicts is the receipt test itself — the
mutant is byte-identical to pristine everywhere else (verified by `diff`). Hence the
clause/control binding (the `clause=<id>` + `observed=` + `control=<id>` requirement) is
exactly what kills the token fixture.

`c2-receipt-unbound` passes the token test for the same reason: its changed receipt
(`c1-row-duplicate`'s) contains `verdict=TARGET_MISSED` on the PRED line, so the token grep
covers it, but it does not name the `entry-regular` clause id and names the wrong control
(`c1-row-duplicate`), so the binding check rejects it. Pristine: `TARGET_MISSED` with exactly
the same `uncovered: entry-regular receipt does not bind clause and control` detail as the
token fixture. Mutant: `TARGET_MET`. The binding is the discriminating condition.

Both fixtures share the identical `uncovered` detail under the pristine counter (`entry-regular
receipt does not bind clause and control`), confirming both are killed by the same binding
requirement and by nothing else (tip and retired observables are at target in all runs).

## Coverage finding

The binding survives this probe: `receipt_observable`'s clause-id/control-id/observed
requirements are load-bearing — flipping them to the round-35 token grep alone is enough to
make two of the eight frozen rejection controls pass (a 2/8 miss rate on the C2 reject set).
The result is a **SURVIVED** mutant in the `TARGET_MISSED`-reject class; the lane's own
C2 instrument is not at fault, which is expected at freeze (the instrument is the subject
under test, and its binding is what must be kept).

## Restoration

No lane file was modified. The mutant lives only in `/tmp`; `quality/counters/c2-ledger.py`
was never edited (sha256 `92db777e7573411835b8686f86520e1f891e8f5e44d6a9c3c18fe8c488193833`
before and after; `git status --porcelain -- quality/counters/c2-ledger.py` shows no entry).
The assigned fixture dirs were not overwritten (regeneration went to a separate fresh dir,
and copies to `/tmp/mut-c2-no-receipt-bind/fixtures/`).

## Tools

No tool installs/updates were needed; only `python3 -I` and `diff`/`sha256sum` were used.
