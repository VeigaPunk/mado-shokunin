# R100MExecGate — C2 harm-watch gate (elapsed_ms)

## What was built
Candidate `build/harm-watch.py` = `quality/harm-watch.py` at `43309e6a` plus per-leg
`elapsed_ms` (monotonic, integer, >= 0):

- `run_leg` records `time.monotonic()` at entry and computes `elapsed_ms` on every
  return path (normal, timeout, spawn-failed, setup), so timeout legs report
  `elapsed_ms >= timeout*1000` by construction.
- Human line: `LEG <id> rc=<n> expect=<n> marker=<ok|MISS> <detail> elapsed_ms=<n>`
  (appended last; existing substrings keep matching).
- `--json` leg objects gain `elapsed_ms`; all other json keys/census/exit map
  (0/1/2)/`--only`/`--timeout`/scratch isolation are byte-identical per diff.
- Selftest +7 checks: `clean-elapsed-ms`, `clean-elapsed-ms-second`,
  `clean-elapsed-ms-integer`, `timeout-elapsed-ms`, `json-elapsed-ms`,
  `elapsed-monotone`, `elapsed-human-line`.

## Evidence (retained)
- `HARM_WATCH_SELFTEST: checks=33 failed=0` (3 runs, ~2.6-3.5 s wall each).
- Candidate sha256 `2d604f7b654f2e2710b612358fedf81fc028dddd47fd0934d9f82c065b226167`,
  ASCII-only, `ast.parse` OK.
- Instrument disclosure: the candidate is the gate tool itself; it spawns panel legs
  (instrument, not candidate logic beyond timing).

## Panel re-freeze
- `controls/harm-panel-r100.json` sha256 `bec81a3e3d34625bcdaac0e30d1de5761404f753ed3bb4ea6ada2d0ed3ac9461`.
- `receipts/panel-timing-r100.txt` did NOT exist at run time (only `c2-panel-r100.txt`),
  so per spec `timeout_s` is a placeholder `3600`; **L1 must set the final value**
  (>= 2 * max_elapsed_ms from the timing receipt) before scoring.
- Diff proof: raw `diff` vs `harm-panel-r99.json` = single line
  (`"timeout_s": 600` -> `"timeout_s": 3600`); parsed compare confirms 28 leg rows
  byte-identical.

## Files written
- `.ufo/waves/round-100/build/harm-watch.py`
- `.ufo/waves/round-100/controls/harm-panel-r100.json`
- `.ufo/waves/round-100/receipts/c2-gate-r100.txt`
- `.ufo/waves/round-100/w1/R100MExecGate.md`

## Risks / notes
- `clean-leg-line` pre-existing substring check still passes (elapsed appended last).
- New `elapsed-monotone` uses a 0.3 s `python -c` sleep leg vs a fast leg; robust
  under load since the gap is 300 ms vs tens-of-ms legs.
- No full-panel run (host loaded; L1 owns integration gate). Scratch deleted prior to yield.

Report: .ufo/waves/round-100/w1/R100MExecGate.md
