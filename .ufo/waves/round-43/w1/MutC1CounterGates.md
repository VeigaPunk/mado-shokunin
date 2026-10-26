# MutC1CounterGates — seat report (round 43, w1)

Status: DONE. Every gate of the C1 counter was challenged with one-edit mutants of a scratch copy;
the frozen counter was never modified.

## What ran
- Counter under mutation: `quality/counters/c1-r42-geometry.py` (frozen, sha256
  `ed78d6930545aedc1b529f06dd3f9bce0d1ead88832ae3f53a125263a316ff99` before AND after — byte-identical,
  restoration evidence; all work was done on copies under `/fast/scratch/hyaku/mado-r43/MutC1CounterGates/`,
  which was deleted at close).
- 81 mutants, one minimal edit each, covering: TOTAL and the `passed == TOTAL` gate, MIN_SELFTEST,
  MIN_SITES, N_MUT, KILL_NEED, the teeth kill-definition / forced-site rule / `and`→`or`, neutrality
  (`&=`→`|`, MIN_SELFTEST drop), judge (stderr check, rc check), the timeout breaker, the model
  (verdict branch, exit code, summary/client field order, truthiness), nonce handling (fixed default,
  nonce-less fixture rng, nonce-less teeth rng), every sandbox flag (cap-drop, unshare-all, proc,
  nproc lead, HOME, clearenv), and every deny-list entry of `imports_ok` (STDLIB_DENY 9, CALL_DENY 4,
  NAME_DENY 8, OS_DENY 13, STR_DENY 3, STR_EQ_DENY 9) plus the allow-side and `bool(mods)` gates.
- Each mutant scored on (a) the reference `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` and (b) 8 bad
  controls regenerated into scratch by the frozen runner's own generation logic
  (`.ufo/waves/round-42/ctl/run-c1-controls.py`): M01-fifo-block, M04-toolarge-ge, M27-nomatch-rc,
  K1-zero-test-selftest, K3-exec-model, K4-child-interpreter, K5-getattr, D1-constant.
- Nonce fixed `42aa42aa42aa42aa`, rev `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f` (round-43 base):
  all 10 pristine anchor rows reproduce the frozen receipt `receipts/ctl-c1.txt` exactly
  (REF 37/37 TARGET_MET rc=0; every control MISSED rc=1). Detector baseline valid.
- 749 counter runs (704 + 27 + 18), ~9 min wall on 14 workers.

## Verdicts (full table: `w1/MutC1CounterGates/matrix.md`)
- **5 GATE-BROKEN** (mutant counter scores a bad control full MET, rc=0, all clauses 1):
  - `call-exec` (drop `"exec"` from CALL_DENY) → admits **K3-exec-model**.
  - `name-getattr` (drop `"getattr"` from NAME_DENY) → admits **K5-getattr**.
  - `total-ge` (`passed == TOTAL` → `>= TOTAL-1`) → admits **M01-fifo-block** and **M04-toolarge-ge**
    (each fails exactly one fixture; the P==TOTAL gate is their only failing gate).
  - `allow-open` (drop the `mods <= STDLIB_ALLOW` conjunct) → admits **K4-child-interpreter**.
  - `verdict-string` (always print `TARGET_MET`) → all 8 controls print MET (rc still 1): the printed
    verdict channel is broken; the frozen runner, which parses only that line, marks every control BAD
    (so the runner detects this counter defect).
- **1 SPLIT**: `exit-always-0` — printed line stays honest, exit code always 0. The frozen runner
  ignores the counter's exit code entirely, so CTL_C1 still says PASS while every bad control exits 0:
  a runner-side coverage gap (exit-code consumers are unprotected by the control suite).
- **7 OVER-STRICT** (reject the reference): `model-nosize`, `model-rc-differ`, `model-summary-swap`,
  `model-client-labels` (byte-exact judge catches any model drift), `n-mut` (N_MUT=2 < KILL_NEED=4 →
  teeth impossible — fails closed), `teeth-forced-site` (forced site from all functions rejects the
  reference at this nonce — the forced-site rule is load-bearing), `total-const` (TOTAL=36 trips the
  `assert len(cases) == TOTAL` — fails closed by crash).
- **3 EQUIVALENT (proved)**: `model-differ-truthy` (int truthiness), `clause-a-1` (verdict needs
  `passed == TOTAL`, so the absent-tool verdict is unchanged; only the printed clause value differs),
  `teeth-no-summ` (summary-less tool: clean reject vs crash — admission identical, diagnostics degrade).
- **65 SURVIVORS, each with a named missing control** (matrix.md, "Per-mutant classification"):
  no control isolates a single STDLIB_DENY entry (the allow-side gate independently rejects K4 — the
  deny lists are defense in depth, not load-bearing), os.* calls, string-constant equality,
  non-getattr NAME_DENY entries, eval/compile/__import__, b3-neutrality in isolation, weak-count
  selftests (1≤n<50), 1–11-site selftests, partial teeth (1–3 kills), the `k!=n` half of the kill
  definition, stderr cleanliness, exit-code-only defects with a passing selftest, nonce
  predictability/overfitting, sandbox flags (cap-drop, unshare, proc, nproc, HOME, clearenv), or the
  timeout breaker.

## Bottom line for the counter's gates
Every gate CAN fail, in both directions: 5 mutants let a bad tool through (missed defect), 7 reject
the good tool (over-strict), 1 breaks the exit channel invisibly to the runner. The gates that hold
single-handedly against the current control suite: the P==TOTAL fixture count, the exec-name and
getattr-name deny entries, and the allow-list side of `imports_ok`. The gates with no isolating
control (survivors) are coverage findings, not permission to change the contract.

## Tooling record
No tools installed (operator 2026-10-19 authorization unused): bwrap 0.13.1, Python 3.14.8 and
coreutils were already present; pacman untouched (paused host-wide).

## Evidence (seat dir)
- `matrix.md` — full matrix, anchors, per-mutant classification, control→flip index, findings.
- `evidence/results.jsonl`, `results2.jsonl`, `results3.jsonl` — all 749 run records
  (counter, target, rc, seconds, met, final line, clauses, failed fixtures).
- `evidence/driver.py`, `driver2.py`, `driver3.py`, `gen.py`, `emit.py`, `matrix.py` — the harness.
- `evidence/pristine-REF.log` — full pristine reference run (37/37 MET).
- `evidence/counter-after.sha256` — frozen counter hash after the seat (== before).
