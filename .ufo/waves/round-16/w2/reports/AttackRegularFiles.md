# AttackRegularFiles — round 16, wave w2

Seat: `MadoR16.AttackRegularFiles` (reviewer, leaf, no dispatch).
Target: `tools/mado-action-plan.py` (752 lines), JSON read path only: `_read_regular` :150-178, `_load_json` :194-208, `_sha256` :211-215, `_evaluate` :354-372, `run_frozen` :380-430, selftest fixtures :491-704.
Mode: source reading only. No gate, selftest, frozen run, probe, or install. One `find -printf` metadata listing of lane `tools/`, `.ufo/waves/round-16/`, `corpus/`, and one `python3 -c` interpreter version query (not the gate). No `~/.omp`, credential, or raw input path was opened.
Installs/updates: none.

## Verdict

FIFO, directory, socket, and device inputs are rejected correctly. Symlink inputs are not rejected. Frozen mode reads each input twice, so its digest pin does not cover the bytes it classifies. The byte bound is enforced on the stat value only, and no fixture pins any file-type or size behavior except "directory".

## What holds (source-verified)

- **FIFO:** `os.open(O_RDONLY|O_NONBLOCK)` at :154 returns without blocking on a FIFO with no writer. `fstat` + `S_ISREG` at :158-160 rejects it before any `read`. No hang path.
- **Directory:** `os.open` succeeds, `fstat` rejects (:160). Pinned by selftest `plan-is-directory` (:564-565, :631-632).
- **Socket:** `os.open` raises `ENXIO`, caught at :155-156, exit 2 with no traceback.
- **Character/block device:** rejected by `fstat` at :160 before any `read`.
- **Symlink to FIFO/dir/socket/device:** `fstat` sees the resolved target, so these are rejected. Correct behaviour, though the docstring does not state it.
- **Oversize by stat:** `st_size > 16 MiB` rejected before reading (:161-162).
- **Read cap:** `remaining = st_size + 1` (:164) bounds memory to about 16 MiB + 1.
- **Strict JSON:** duplicate keys, NaN/Infinity, invalid UTF-8, and BOM all exit 2 (:199-207; the `except Exception` covers `RecursionError` and int-digit limits).
- **fd discipline within one call:** stat and read use the same fd, so there is no stat-then-open race inside a single `_read_regular`. The races below are between separate calls.

## Findings (by severity)

### F1 — Medium: frozen verdict is computed from a second, unpinned read (TOCTOU)

`run_frozen` hashes each input with `_sha256(path)` at :416, which opens, reads, and hashes. It then calls `_evaluate(plan_path, policy_path)` at :424, which calls `_load_json` again for the policy (:356) and the plan (:364). That is two independent open-and-read cycles. The verdict at :424-430 is derived from bytes that the digest check at :420-422 never saw.

Counterexample (static reasoning, not executed): the pinned plan P1 hashes to the pinned digest at :420. Between :416 and :424, the path is replaced with plan P2 that yields the same finding and exit as `expected.json`. The gate prints `frozen_match` with exit 0 while the classified bytes were never the pinned bytes. The reverse also holds: a swap turns a true match into `frozen_verdict_mismatch`.

Limits: this needs a writer who can modify the frozen directory during a short window, so it is not a remote exploit. The snapshot-binding claim (`snapshot_tampered` on tamper) is still weaker than the docstring implies, and F2 widens the swap surface. The frozen selftests (:674-704) run sequentially and cannot exercise the window.

Fix direction: read each file once through `_read_regular`, hash those same bytes, and classify those bytes.

### F2 — Medium: symlinks are followed and accepted as inputs (contract gap)

`_read_regular` at :154 calls `os.open(path, O_RDONLY|O_NONBLOCK)`. There is no `O_NOFOLLOW`, no `os.lstat` before open, and no containment check. `run_frozen` joins fixed names under `root` at :383-385 and never checks that they resolve inside `root`.

Counterexample: `frozen/plan.json -> /elsewhere/plan.json`, where the target's bytes match the pin. The gate accepts it, and the verdict is `plan_safe`/`frozen_match` with the snapshot root not self-contained. The same applies to `policy.json`, `expected.json`, and a `--plan` or `--policy` symlink.

Design anchors that expect rejection:
- `.ufo/waves/round-13/w1/reports/ExitMap.md:52`: frozen "symlink or `..` escape" maps to `frozen_error`/`snapshot_tampered`, exit 2.
- `.ufo/waves/round-13/w1/reports/FindingStability.md:86`: "path escapes frozen root … checked before any content read" maps to `snapshot_tampered`.

Context that narrows the claim: `.ufo/waves/round-16/w1/reports/ClosureDebt.md:111` (V14-R6) says symlink-to-directory/FIFO/socket cases are not acceptance criteria. That excuses fixtures for those cases, not symlink-to-regular. The module docstring (:31-33) lists "unreadable paths, directories, FIFOs, devices, and other non-regular inputs" and does not mention symlinks, so the accepted behaviour is undocumented.

Fix direction: `lstat` the final path component (or `O_NOFOLLOW`), and for `--frozen` check that realpath containment holds. Otherwise state the symlink policy explicitly in the docstring and the registry row.

### F3 — Medium: no fixture pins file-type or size behaviour except directory

The selftest case list (:491-614) contains one non-regular case (`plan-is-directory`, :564-565). It has no case for FIFO, symlink, device node, oversize (>16 MiB), or zero-size regular files. The frozen fixtures (:674-704) have no file-type cases either. `.ufo/waves/round-16/safety-cases.json` has no file-type or size case; its only `/dev/input` strings (:76, :89, :102) are argv data, not input paths.

So the FIFO, device, and bound claims in the docstring (:31-33) are supported by code reading only. Recommended fixtures, for L1 to decide: `mkfifo` in the temp dir, symlink-to-regular, symlink-to-directory, a sparse 16 MiB + 1 file via `truncate`, and a `/dev/null` plan path. These are not executed here.

### F4 — Low: the bound is enforced on `st_size`; the `+1` sentinel is never checked

`_read_regular` at :161-173 rejects oversize only by the stat value. It reads up to `st_size + 1` bytes and never compares the total to `st_size` or to the cap. If a regular file grows after `fstat`, it returns `st_size + 1` bytes with no error. If `st_size` is 0 (typical of procfs and sysfs regular files), only one byte is read.

Consequence: fail-closed, because the truncated JSON gives `plan_malformed`/`policy_malformed` (exit 2), and in frozen mode the digest mismatches (`snapshot_tampered`, exit 2). But the finding text misattributes the cause ("not strict JSON") and the 16 MiB bound is not enforced on the bytes actually read.

Fix direction: read to EOF with a total cap of 16 MiB + 1, and refuse if the cap is exceeded or the total differs from `st_size`.

### F5 — Low: device nodes are opened before they are rejected

`os.open` at :154 runs before `fstat` at :158. `O_NONBLOCK` prevents blocking for FIFOs and most devices, so the FIFO and device rejections work. But opening a device node invokes its driver `open()`, and `O_NOCTTY` is absent, so a tty path could in principle become the controlling terminal of a session-leader process. Session-leader is an unusual case for a child process, so impact is low.

Fix direction: `os.lstat` before open, and `O_NOFOLLOW|O_NOCTTY` on open.

### F6 — Low: unbounded path and digest echo in verdict detail

`_evaluate` at :359, :363, :367, :371 and `run_frozen` at :419, :422 embed the caller path and digest verbatim in `detail`. FindingStability P4 (`FindingStability.md:70-73`) asks for bounded, non-absolute detail. This does not affect the regular-file check itself; it is an adjacent hygiene point.

### F7 — Observation (process): untracked bytecode in `tools/`

`tools/__pycache__/mado-action-plan.cpython-314.pyc` (36541 bytes, mtime 2026-10-20 05:46) carries the same minute as the last source edit of `tools/mado-action-plan.py`. Host `python3` is 3.14.7. A `.pyc` is written on import or `py_compile`, not on direct script execution. I did not run anything. L1 should confirm the import came from an authorised author check, that no seat ran the gate outside the verification wave, and that `__pycache__` is excluded from the commit.

## Residual risk and verification gaps

- F1 and F2 are static reasoning about stdlib `os.open` and `os.fstat` semantics [INFERENCE: documented stdlib behaviour, not executed here].
- No fixture or receipt in the lane pins any finding above. Every claim here is a source-derived counterexample.
- I did not check the frozen `expected.json` pins against the current `plan.json`/`policy.json` bytes. That is a hash computation outside this attack's scope.
- Distinguished from broader limits: the classifier's argv-basename limits are declared (`safety-cases.json:17`, `ExecBasename.md`), not part of this regular-file attack.

## Handoff for L1 (no edits made by this seat)

1. Decide F1 first: classify the bytes that were hashed (single read in frozen mode).
2. Decide F2's symlink policy and implement it or document it in the docstring and registry.
3. Add file-type and size fixtures (F3) and fix the sentinel (F4).
4. F5 and F6 are optional hygiene.
5. Confirm F7 before commit.
