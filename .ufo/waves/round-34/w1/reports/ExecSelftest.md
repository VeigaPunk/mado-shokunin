# ExecSelftest — mado-shokunin axis gate selftest

## Scope

Read `quality/check-axis-scores.py`, explain its total, run its `--selftest`,
capture the full transcript. No edits to the gate.

## How the total is computed

The selftest total is a **hardcoded constant**, not a count derived at runtime:

- `selftest()` sets `total = 18` (quality/check-axis-scores.py:243) and prints
  `MADO_AXIS_SELFTEST: %d/%d assertions passed` with `total - fails` over `total`
  (line 244). `fails` is incremented by the inner `check(name, cond)` helper each
  time an assertion is false (lines 165-171). There are exactly 18 `check(...)`
  calls, matching the constant.
- Exit code: `1` if any check failed, else `0` (line 245).

Meaning of the fractions:

- `18/18` on the final line: all 18 assertions passed; exit 0. A denominator
  other than 18 is impossible — it is a literal.
- `12/12` would be a **per-axis fraction**, not the selftest total. In the gate's
  model each axis publishes `A/B` (line 14: operability = `check-index.py
  --selftest` → `A/B assertions passed`). `12/12` = the underlying instrument
  passed 12 of its own 12 assertions, i.e. a perfect axis score. The selftest
  uses `12/12` only as fixture data for the operability cell (e.g. lines 185,
  223, 230); it never appears as the selftest's own denominator.

## Run

Command (from lane root):

    python3 quality/check-axis-scores.py --selftest

Transcript (stdout, stderr, exit code):
`.ufo/waves/round-34/scratch/ExecSelftest/selftest.txt`

- stdout: 18 `PASS` lines, 0 `FAIL` lines, then the summary.
- stderr: empty.
- exit code: `0`.

## Exact final line

    MADO_AXIS_SELFTEST: 18/18 assertions passed

## Real pass count

**18** — counted directly from the transcript (18 `PASS` lines, 0 `FAIL` lines);
consistent with the printed `18/18`.

## Evidence

- Gate source: `quality/check-axis-scores.py` (lines 32, 72-94, 162-245 cited above).
- Transcript: `.ufo/waves/round-34/scratch/ExecSelftest/selftest.txt` (written this round, reproduced verbatim above).
