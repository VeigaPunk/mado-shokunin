# R55W2SentTool — scoped findings (round 55, wave w2, falsify)

Full evidence, exact commands and the verdict table: `.ufo/waves/round-55/w2/R55W2SentTool/security.md` (receipts beside it: `attack.py`, `receipts.txt`, `diag.py`, `diag2.py`, `extra-checks.txt`).

Target: `tools/mado-kbdopts.py` and `quality/r55_ctl_c2.py` at scored rev `57584ed6`. Attacks ran against unmodified copies in scratch (sha256-matched to the rev). No lane write, no git mutation, no host read, no installs, no mutation test.

## Verdicts

- FIFO as `--config` and as `--getoption`, FIFO with data and an open writer, open pipe on `/dev/stdin`: **SURVIVES** (rc 2 `unreadable`, ≤0.02 s, no hang).
- Symlink to `/dev/zero` (both flags) and `/dev/zero`, `/dev/null`, directory, `/proc/kcore`: **SURVIVES** (`unreadable`).
- Symlink to a regular file: **SURVIVES** (followed; policy not written down).
- `/proc` file with `st_size` 0 and 22,508,348 bytes of content: **SURVIVES** (`too_large`). Exact 1,048,576 B accepted; 1,048,577 B `too_large`.
- 200,000-deep JSON (bare and inside an option object): **SURVIVES** (`bad_json` rc 2, no traceback).
- 5,000- and 1,000,000-digit integers: **SURVIVES** (no crash; printed in full; 1 MB line in 0.53 s).
- `--keyboard` with `\n`, `\r`, ESC, DEL, VT, FF, TAB: **SURVIVES** (7/7 `usage`).
- `--keyboard` with U+0085, U+2028 or U+2029 followed by a forged `MADO_KBDOPT: DONE ... live=AGREE`: **BROKEN (narrow)**. Accepted; a `str.splitlines` consumer sees the forged DONE line. A newline-split consumer and the byte-compare harness are not affected.
- Harness: 200 MiB child stdout captured at exactly 67,108,864 bytes, rc 1, 0.13 s: **SURVIVES**. Spinning child killed at timeout: **SURVIVES**. Same-group forked grandchild killed: **SURVIVES**.
- Harness: a grandchild that calls `setsid()` survives `run_prog` returning, and survives the timeout kill: **BROKEN (new)**.
- Aggregate `--config` (N × 1 MiB): **BROKEN (open from w1)**. 400 pairs under a 400 MB address-space cap: `rc=1`, empty stdout, traceback ending `MemoryError` (rc outside the contract's {0,2}). About 1 MB retained per pair; ARG_MAX allows about 24,917 pairs, projected ≈25 GB (projection, not run).
- Harness `run_isolated` with an argv `../../../../name.conf`: **BROKEN (new, low)**. Copies a file from outside the tree into a path outside the run dir, and the tool reads it. Committed `c2` args contain no `..`.
- `--getoption` decoded with `errors="replace"`: **NOT-REPRODUCED as a security issue** (no effect on any verdict).

## Fixed vs open

- Fixed: w1 R1, R2, R4, R6, R7 (no crash), R10 for newline and control bytes, harness 64 MiB cap, same-group fork reaping.
- Open from w1: R5 aggregate input (memory and CPU amplification), R14 unhandled exception (`MemoryError` gives rc 1), R3 symlink policy undocumented, R9 decode policy.
- New: N1 U+0085/U+2028/U+2029 residual (narrow), N2 escaped process survival in the harness, N3 argv `..` traversal in `run_isolated`.
- Hold-out (w1 F1): `fixtures/c2-holdout/H01..H08` is committed at the scored rev. Not re-tested as an attack. The sealed-set property does not hold for this round.

## Smallest remediations (not applied)

- Parse each `--config` as read; cap the cumulative size or document the argv bound; catch `MemoryError` and `RecursionError` to a `SETUP` line.
- Reject NAME with C1 controls (0x80–0x9F) and U+2028/U+2029 (usage).
- Run each tool under `unshare --pid --fork --kill-child` (or a cgroup) so escapees die with it; not tested.
- In `run_isolated`, reject `..` and absolute argv paths and assert resolved paths stay under `tree` and `rd`.

## Not verified

- Full-scale aggregate memory (projection only); cross-fixture effect of an escaped process; `killpg` pid-reuse race (theoretical, untested); the F1 sealed-set status for future rounds.
- Driver `ru_maxrss` readings are an inherited artifact and were not used.
