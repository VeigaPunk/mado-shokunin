# Round 55 w2 — R55W2SentTool: re-attack of the integrated C2 tool and harness

Scope: the w1 sentinel findings (`../../w1/R55Sentinel/security.md`, F2–F4 and R1–R15) re-run against the integrated files at scored rev `57584ed67716340b3d466fa04333ac0bab3fb79e` (an ancestor of lane HEAD `721ba9c1`). Attacks were run with `python3 -I` against **copies** in scratch (`/fast/scratch/hyaku/mado-r55/R55W2SentTool/`), which were produced by `git show 57584ed6:<path>`. Their sha256 matches the scored blobs and the lane working tree:

- `tools/mado-kbdopts.py` = `9c69dd62c1737d4842a4a0e73db3f8317eda71ee103e71ad3cda11a19c837c2e`
- `quality/r55_ctl_c2.py` = `3f6b8bb882ea91445489415dcdddc7c939c7b23e76ae7e570514afd2865262e6`

Nothing in the lane was written. No git/jj mutation ran; the only git calls were `show`, `grep`, `ls-tree` and `cat-file` at the rev. No mutation test was run. No host read was made (no hyprctl, no `~/.config` read). No tool was installed or upgraded. Python is 3.14.8.

Receipts (copied into this directory): `attack.py` (driver for the main matrix), `receipts.txt` (its full log), `diag.py` and `diag2.py` (follow-up probes), `extra-checks.txt` (selftest, NaN, the two diagnostics). Re-run: `python3 -I attack.py` with `S` = the scratch path above.

Environment note: the `ru_maxrss` of the driver process reads 8,398,496 KB even at fresh `python3 -I` startup (an inherited value). Driver RSS is therefore not used as evidence. Child-process RSS values (from `wait4`) are used.

## Verdict table

Verdict keys: SURVIVES (attack fails against integrated code), BROKEN (attack succeeds), NOT-REPRODUCED, UNVERIFIED.

| # | Target | Attack | Verdict | Status vs w1 | Evidence (receipts.txt unless noted) |
|---|---|---|---|---|---|
| T1 | tool `--config` | FIFO, no writer | SURVIVES | F2/R1 fixed | `F2a FIFO --config (no writer) | rc=2 t=0.02s`, out `MADO_KBDOPT: SETUP unreadable` |
| T2 | tool `--getoption` | FIFO, no writer | SURVIVES | F2/R1 fixed | `F2a FIFO --getoption (no writer) | rc=2 t=0.02s` |
| T3 | tool `--config` | FIFO holding data, writer open (`O_RDWR`) | SURVIVES | F2/R1 fixed | `F2a FIFO with data and an open writer | rc=2 t=0.02s` |
| T4 | tool `--config` | `/dev/stdin` = open pipe, nothing written | SURVIVES | F2/R1 fixed | `F2a /dev/stdin is an open pipe with no writes | rc=2`, no hang |
| T5 | tool | symlink → regular file | SURVIVES (policy undocumented) | R3 policy open | `F2b symlink -> regular file | rc=0`, `from=G/-/-` |
| T6 | tool | symlink → `/dev/zero` (`--config` and `--getoption`) | SURVIVES | F2/R2 fixed | `F2b symlink -> /dev/zero as --config | rc=2 t=0.02s`; `--getoption` `rc=2 t=0.041s` |
| T7 | tool | `/dev/zero`, `/dev/null`, a directory, `/proc/kcore`, `/proc/self/mem` | SURVIVES | F2/R2 fixed | all `rc=2 unreadable` in ≤0.02 s |
| T8 | tool | `/proc` file with `st_size` 0 and content over 1 MiB (`/proc/kallsyms`, 22,508,348 bytes) | SURVIVES | F2/R4 fixed | `F2c /proc/kallsyms (st_size 0) | rc=2 t=0.051s`, `SETUP too_large`; `wc -c` = 22508348 |
| T9 | tool | regular file exactly 1,048,576 B / 1,048,577 B | SURVIVES | R4 fixed | `exact.conf` `rc=0`; `over.conf` `rc=2 SETUP too_large` |
| T10 | tool `--getoption` | 200,000-deep nested array (bare line; and inside a valid option object) | SURVIVES | F2/R6 fixed | both `rc=2 SETUP bad_json`, t=0.03 s, no traceback |
| T11 | tool `--getoption` | depth boundary (extra-checks/diag) | SURVIVES (note) | — | depth 5,000 / 20,000 / 50,000 accepted; 100,000 → `SETUP bad_json`. Limit depends on the interpreter (3.14.8 here), not a constant of the tool. Valid JSON that is too deep is refused as `bad_json`: a false refusal, no security effect |
| T12 | tool `--getoption` | 5,000-digit integer `"int"` | SURVIVES | R7 no crash | `rc=0`; live field length 5000; `live=DIFFER` (no crash, no traceback) |
| T13 | tool `--getoption` | 1,000,000-digit integer (1 MB line) | SURVIVES | R7 | `rc=0 t=0.525s`, output 1,000,381 bytes |
| T14 | tool `--keyboard NAME` | `x\ny`, `x\rMADO`, `x\x1b[2J`, `x\x7f`, `x\x0bq`, `x\x0cq`, `x\tq` | SURVIVES (7/7) | F3/R10 fixed for these | each `rc=2 SETUP usage`; forged-DONE-via-`\n` case `rc=2` |
| T15 | tool `--keyboard NAME` | `a` + U+0085 / U+2028 / U+2029 + `MADO_KBDOPT: DONE keyboards=1 unsupported=0 live=AGREE` | **BROKEN (narrow residual)** | R10 partly fixed; new | `rc=0`; output contains a line whose prefix is `MADO_KBDOPT: DONE ... live=AGREE`. `str.splitlines()` yields 6 lines and a DONE-prefix line appears before the real one; a newline-split consumer sees only the real DONE (`live=DIFFER`). The harness compares bytes and is not fooled. The docstring's claim "cannot forge an output line" holds only for `\n`-splitting consumers |
| T16 | tool `--keyboard NAME` | non-UTF-8 byte in argv (0x85, 0xff) | SURVIVES | R10 | byte written raw, no new line for byte-based consumers |
| T17 | tool | aggregate: N × 1 MiB `--config` | **BROKEN** (open) | F4/R5 open; R14 | 10 / 50 / 200 pairs: `rc=0`, tool RSS 23,812 / 64,388 / 219,268 KB (≈1 MB retained per pair). 400 pairs under `ulimit -v 400000`: **`rc=1`, stdout empty, traceback ending `MemoryError`** (not a `SETUP` line, outside the contract's rc set {0,2}). Projection from ARG_MAX=2,097,152 and 68 B per pair (path 59 B): ≈24,917 pairs → ≈25 GB retained (every config text is kept in `configs`). Not run at full scale (host has 30 GB, 15 GB used) |
| T18 | tool | aggregate CPU, worst-case content (1 MiB of `x\n` lines) | SURVIVES as a measurement, amplifies T17 | F4 | 1 file 0.04 s; 20 files 0.58 s (≈29 ms/file), so ≈12 min CPU at 24,917 files |
| T19 | tool `--getoption` | invalid UTF-8 inside a JSON string / outside JSON | NOT-REPRODUCED as a security issue | R9 divergence | inside a string: `rc=0` (replace decode); outside: `SETUP bad_json`. Only exact option names match, so no effect on any verdict |
| T20 | harness `score`/`run_prog` | child writes 200 MiB to stdout | SURVIVES | 64 MiB cap | `rc=1 stdout_bytes=67108864` (exactly the cap), returned in 0.13 s (EFBIG; Python ignores SIGXFSZ, so the child gets an exception, not a signal) |
| T21 | harness | child spins ignoring EFBIG (TIMEOUT patched to 3 s for the run) | SURVIVES | timeout | `rc=None stdout_bytes=0 t=3.01s` (killed by the group kill) |
| T22 | harness | child forks a grandchild in the same process group, then parent exits | SURVIVES | fork reaping | grandchild alive after `run_prog` returned: `False` |
| T23 | harness | child forks a grandchild that calls `os.setsid()`; parent exits | **BROKEN** (new) | not in w1 | `rc=0`; grandchild alive after `run_prog` returned: `True` (killed by the test afterwards) |
| T24 | harness | parent hangs; grandchild `setsid()`s; timeout | **BROKEN** (new) | not in w1 | `rc=None t=3.50s`; grandchild alive: `True`. The `killpg` covers only the group |
| T25 | harness `run_isolated` | committed-looking argv `../../../../name.conf` | **BROKEN** (new, low) | not in w1 | tool reads the copy: `READ b'input:repeat_rate = 30\n'`; file written at `trav/a/name.conf` (outside the run dir and the tree; `run dir removed: True` yet the copy persists). Committed `c2` args contain no `..` (`git grep '\.\.'` at the rev: no output), so no committed fixture triggers it |
| T26 | harness | `killpg` after a normal exit can hit a reused pid | UNVERIFIED | theoretical | not tested; needs pid reuse inside the wait window |
| T27 | F1 hold-out path (w1 §2) | committed names | UNVERIFIED (out of the attack list) | status changed | `git grep c2-holdout` at the rev: `fixtures/c2-holdout/H01..H08/args.json` are committed (revealed at integration). The sealed-set property no longer holds for this round, and any future round must not reuse those fixtures |

## Fixed, declared, new

**Fixed (w1 items closed by the integrated code):** R1 stat-then-open race and R2 special files (T1–T4, T7); R4 `st_size` bypass (T8–T9); R6 deep JSON, now `bad_json` rc 2 without traceback (T10); R7 huge integers, no crash (T12–T13); R10 newline and control bytes in `--keyboard` (T14); the harness 64 MiB stdout cap (T20–T21); same-group fork reaping (T22).

**Declared / accepted by contract text:** R15 argv trust (`--config /proc/...` is accepted; the tool has no sandbox and reads what argv names). The harness docstring already declares that a hostile tool can scan the filesystem.

**Open from w1 (not closed):** R5 aggregate input (T17–T18); R14 unexpected exception gives rc 1 (T17, `MemoryError`); R3 symlink policy (followed, not written down in the docstring or the frozen text); R9 getoption decoding is `replace`, not strict (T19, no exploit).

**New in this wave:**
- N1 (narrow, low): U+0085, U+2028 and U+2029 pass the control-byte rule (T15). The rule is `ord(c) < 32 or ord(c) == 127`; C1 controls and Unicode line separators are not covered. The tool's own `\n` grammar is not forgeable, but the docstring's "cannot forge an output line" is overstated for `splitlines`-style consumers.
- N2 (medium, harness, unsandboxed process survival): a `setsid()` grandchild survives both normal return and the timeout kill (T23–T24). Verdict capture is unaffected, because rc and stdout are read before the reap. But the survivor keeps running, and nothing in the docstring declares it. An unsandboxed survivor can write into the exported tree that later fixtures read (`score` reads `expected.*` from the tree), so a later fixture could be affected. Not shown in this run (UNVERIFIED for cross-fixture effect).
- N3 (low, harness, argv traversal): `run_isolated` copies `tree/<arg>` to `rd/<arg>`, and both paths honour `..` (T25). It defeats the stated isolation for any fixture that names a `..` path, and leaves the copy outside the run dir.

## Smallest remediations (not applied; the lane is frozen for this wave)

- R5/R14 (T17): do not retain config texts. Parse each `--config` as it is read (state is order-dependent only through `st`). Enforce a cumulative byte cap (e.g. total ≤ 1,048,576, reason `too_large`), or amend the contract to say the argv bound is the limit. Catch `MemoryError` and `RecursionError` in `run_cli` and return a `SETUP` line with an existing reason, so rc stays in {0, 2}.
- N1 (T15): reject a NAME containing any char with `ord(c) < 32`, `ord(c) == 127`, `0x80 <= ord(c) <= 0x9f`, `ord(c) in (0x2028, 0x2029)` (usage), or print such bytes escaped. Update the docstring claim to match.
- N2 (T23–T24): run the tool under `unshare --pid --fork --kill-child` (or a cgroup scope) so that a `setsid()` escapee dies with the namespace. Not tested here, because I did not install or change any namespace tooling.
- N3 (T25): in `run_isolated`, reject any argv path with a `..` component or a leading `/`, and assert `os.path.realpath(src)` is under `tree` and `realpath(tp)` under `rd` before copying.
- R3/R9: write the symlink and getoption-decoding policies into the docstring (they are behaviour, not text).

## Not verified / limits

- No hostile tool was run at full aggregate scale (24,917 pairs). The ~25 GB figure is a projection from the measured ~1 MB per pair, not an observation.
- The escaped-grandchild effect on later fixtures (N2) was not demonstrated end to end.
- The `killpg` pid-reuse window (T26) was not tested.
- The hold-out sealing status for future rounds (T27) is outside this seat's attack list.
- Controls and the harness's full verdict were not re-run; this seat attacked the tool and harness, it did not score them.
