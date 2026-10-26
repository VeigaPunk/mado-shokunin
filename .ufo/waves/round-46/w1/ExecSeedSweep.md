# ExecSeedSweep — determinism / nonce independence of PRED-C1-r46 (final)

Seat: ExecSeedSweep (leaf, round 46 w1). No lane file edited; counter, fixtures, reference and receipts
verified unchanged (freeze = lane HEAD `e0be61e` = disk, sha256 below). All evidence in
`.ufo/waves/round-46/w1/ExecSeedSweep/`; detailed report in `ExecSeedSweep/report.md`.

**Result: deterministic and nonce-independent. 412 scored runs, 0 non-MET.**

- Scored revision: scratch clone of freeze `8c5434c` with the reference installed as
  `tools/mado-devices.py` → `30f2e2792d49ea6bcfa24ac2706e3e708d7d0fa5`
  (tool bytes `b229efd0…a33b`, counter `dfeaa440…50a`, fixtures `027ed508…fc1`).
- **Nonces 1..120**: 120/120 `TARGET_MET`, exit 0 (`evidence/runs-block1.txt`).
- **Nonce 46 under `PYTHONHASHSEED` 0 / 1 / random**, plus 4 repeats, 2 serial runs and the first timing
  run: 11/11 `TARGET_MET`, and all eleven logs are **byte-identical**
  (`sha256 d3fbd7305c0990961ccf1338d975c138db9e11c578f5aef740780a19c996ccaf`,
  `evidence/log-nonce46-serial.txt`).
- **Extra breadth**: nonces 121..400 plus extremes `0, -1, 2³²−1, 2⁶³−1, 10¹⁸` — 285/285 `TARGET_MET`
  (`evidence/runs-block2.txt`).
- **Non-MET records: none.** Each failure mechanism the assignment names was tested and ruled out:
  placeholder collision impossible (`subst` replaces `{A}`-`{D}` tokens only; 10,800 in-process
  fixture checks over nonces 1..120 with 0 mismatches); prefix/substring overlap excluded by the
  `n not in p and p not in n` guard over **200,000** seeds (0 bad seeds, universe has 486 containment
  pairs); model vs installed copy are the same bytes and diverged on **0 of 61,800** generated cases
  (17,939 distinct cases; all five verdicts present).
- **`names()` character audit**: universe 567 names, alphabet `[+0-9a-z-]`, regex `[\[\]\$#=A-Z]`
  never matches; also no whitespace/comma/brace/backslash; max length 62. (`evidence/names-analysis.txt`.)
- **Detection control** (proves the empty set is measured, not blind): a clone with the `scroll_factor`
  clamp removed scores `TARGET_MISSED` at nonces 1/46/77 with `mouse-clamp-high`/`mouse-clamp-low`
  fixture FAILs and `generated=149/150` (`evidence/control-mutation-missed.txt`).
- **Time**: 8.3–9.2 s per run serial (idle); 12.0–18.7 s per run at 12-way concurrency; block 1 (127
  runs) 168 s wall, block 2 (285 runs) 350 s wall.

Residuals recorded in the report: clause f's environment-B axis is inert for this contract (the
reference reads no env var and no locale; `evidence/no-env-and-order-scan.txt`), and the harness never
propagates `PYTHONHASHSEED` into the tool subprocess, so the tool always starts with a randomized seed —
which makes fixture/generated runs a stronger hash-order probe than the counter-process sweep.

Tool installs: none. Host untouched (no `hyprctl`/`libinput`/`journalctl`/`udevadm`, no pacman, no
compositor or Wayland call, no git/jj mutation in the lane). Scratch removed after receipts were copied.
