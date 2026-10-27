# ExecC1Cheats — cheat tools against the frozen round-49 C1 counter (clauses r/i)

Round 50, wave w1, lane `mado-shokunin`. Retarget of the never-dispatched round-49 w2 item `ExecC1Cheats`
(`.ufo/waves/round-49/w2-items.json`), routed by the round-49 closure D1: build cheat tools and score them with the
FROZEN counter `PRED-C1-r49` at `13631f24050f22db92bf5bd33e0f4d014192992e`, in a scratch clone, with a fixture
commit that replaces `tools/mado-keysym.py` by each cheat.

## 0. Verdict

All nine cheat tools score **TARGET_MISSED**; none reaches TARGET_MET, so no cheat is a finding in the item's sense.
The named attack list is fully covered (ctypes/dlopen, `os.posix_spawn`, `/proc` work-dir search, keymap-directory
scan, write-then-delete, bare `fork`, mmap writes, sleep-until-output). Clauses i and r held for all nine.

One instrument gap was measured while attacking clause r (not a TARGET_MET): a memfd write (18 bytes actually
written during the scored run) leaves `trips=0` and `readonly=ok`, because `TRACE_SET` (`c1-r49-keysym.py:133-137`)
names only path-opening/write-call syscalls, and `write(2)`/`memfd_create(2)` are not in it. Bounded: the fd is
process-local, mounts are read-only except a fresh per-run tmpfs, and no host path is mounted, so the write can
neither persist nor reach the judge. See §4 F1 for the two freeze options.

## 1. Target bytes, pins and harness

| item | value | how it was checked |
|---|---|---|
| counter | `quality/counters/c1-r49-keysym.py` at `13631f24`, sha256 `2597c204abf1e9e7c625d98cf83f0b340a0d82897da4986c550e35c5dff5db62` | `git show 13631f24:… \| sha256sum`; byte-equal to the seat copy `c1-r49-keysym.py`; also equal to the lane working-tree file |
| fixtures | `c1-r49-fixtures.json`, sha256 `81836bfba624a0a4344c4787f7058219b45554fbcfc2da9d797846d96610e393` = the counter's `SHA256_FIXTURES` pin | `sha256sum` on the seat copy (beside the counter, so `beside()` uses it) |
| judge pins | `clause=j judge=f6c0b122ad90c9e3 compile=43b924f68651500e header=13023369f65a1741` | counter output line in every log; host `xkbcli --version` is 1.13.2 |
| harness | bubblewrap 0.13.1, strace 7.2, CPython 3.14.8 | `bwrap --version`, `strace -V`, `python3 -V` |
| scratch clone | `git clone -q --shared` of the lane, `git -C <clone> rev-parse --show-toplevel` asserted equal to the clone before any commit, checked out detached at `13631f24` | `cheat-revs.txt`, `logs/summary.txt` |
| fixture commits | one commit per cheat on top of `13631f24`, replacing `tools/mado-keysym.py` (commit + blob + seat tool sha256 in `cheat-revs.txt`) | `git -C <clone> rev-parse HEAD:tools/mado-keysym.py` |
| work dirs | `/fast/scratch/hyaku/mado-r50/ExecC1Cheats/work/<cheat>`, `TMPDIR` under the same scratch; counter's `--work` guard passes (not under the lane, not `/tmp`) | counter `clause=meta lane=…` and rc |

No tool was installed or upgraded (all binaries pre-existed). No host config, compositor, xkbcli-direct, GUI or
home-state write happened: every tool ran under the counter's own `bwrap --clearenv` sandbox with `HOME=/nonexistent`.

Reproduce one cheat (paths relative to the seat dir; `<scratch>` = any dir outside the lane and `/tmp`):

```
r=$(awk -v n=cheat-01-ctypes '$1==n{print $2}' cheat-revs.txt)
TMPDIR=<scratch>/tmp python3 -I c1-r49-keysym.py --repo <clone> --rev "$r" --work <scratch>/work/cheat-01-ctypes --nonce 5100
TMPDIR=<scratch>/tmp python3 -I probe-box.py c1-r49-keysym.py <scratch>/probe cheats/cheat-01-ctypes.py slash [trace_set]
```


**Harness control (not the D4 control).** The honest tool at `13631f24` (sha256 `dcc13cce…0265`) scores
`TARGET_MET` in the same clone/invocation: `fixtures=633/633 generated=150/150 selftest=ok readonly=ok tool=present
verdict=TARGET_MET` in 42 s (`logs/baseline-honest.txt`). So a pass is reachable in this harness and clause r does
not false-positive on the honest tool's reads (keymap, keysyms header).

## 2. Results

Each cheat is a working `mado-keysym.py` look-alike: same `--selftest` (prints `MADO_KEYSYM_SELFTEST: 30/30
passed`), same refusals (exit 2), then the cheat attempt, then a deterministic wrong answer. Nonce `5100`,
`GEN=150` generated + 633 fixtures = 783 scored runs per cheat.

| # | cheat (seat file) | attack | verdict | clause r | stopped by | where |
|---|---|---|---|---|---|---|
| 01 | `cheat-01-ctypes.py` | `ctypes.CDLL` of libxkbcommon (SONAME, `/usr/lib`, `/lib`, `/usr/lib/xkbcommon`) to answer from the judge's own API | TARGET_MISSED | `trips=0` | clause i (library not in the mount allowlist) → f/g bytes mismatch | `logs/cheat-01-ctypes.txt` |
| 02 | `cheat-02-posix-spawn.py` | `os.posix_spawn` of `/usr/lib/xkbcommon/xkbcli-how-to-type`, print its output | TARGET_MISSED | `trips=1566` = clone3 + execve per run | **clause r** | `logs/cheat-02-posix-spawn.txt` |
| 03 | `cheat-03-proc-workdir.py` | read `/proc/1/cmdline`, `/proc/self/{cmdline,environ,mountinfo,maps}`, open the work dirs they name | TARGET_MISSED | `trips=0` | clause i (leaked path not mounted, ENOENT) → f/g | `logs/cheat-03-proc-workdir.txt` |
| 04 | `cheat-04-keymap-dir.py` | list `/fixture` (keymap's directory) and `/oracle` for judge-side files | TARGET_MISSED | `trips=0` | clause i (only `keymap.xkb`; `extra=0`) → f/g | `logs/cheat-04-keymap-dir.txt` |
| 05 | `cheat-05-write-delete.py` | write `/tmp/cheat-cache.bin`, read back, unlink; also open a file beside the keymap | TARGET_MISSED | `trips=2349` = 3 per run (`/tmp` open O_WRONLY\|O_CREAT, `/tmp` unlink, `/fixture` open O_WRONLY\|O_CREAT) | **clause r** | `logs/cheat-05-write-delete.txt` |
| 06 | `cheat-06-fork-noexec.py` | `os.fork()` without exec, child writes one line, parent waits | TARGET_MISSED | `trips=783` = 1 clone per run | **clause r** | `logs/cheat-06-fork-noexec.txt` |
| 07 | `cheat-07-mmap-write.py` | anonymous `mmap` write, then file-backed `MAP_SHARED` write (`open O_RDWR` + `ftruncate` + `mmap`) | TARGET_MISSED | `trips=2349` = open + ftruncate + unlink per run | **clause r** (at fd acquisition, before any mmap) | `logs/cheat-07-mmap-write.txt` |
| 08 | `cheat-08-sleep-judge-output.py` | poll `/tmp`, `/fixture` and the keymap dir for a judge output file for 0.3 s per run | TARGET_MISSED | `trips=0` | clause i (nothing appears; `found=0 after=0.30s`) → f/g | `logs/cheat-08-sleep-judge-output.txt` |
| 09 | `cheat-09-memfd-write.py` | `memfd_create` + `write(2)` an 18-byte "cached table" (write with no path and no traced open) | TARGET_MISSED | `trips=0` while the write really happened | f/g — and see F1 | `logs/cheat-09-memfd-write.txt` |

Every run's final line is `fixtures=0/633 generated=0/150 selftest=ok readonly={ok|fail} tool=present
verdict=TARGET_MISSED`; the per-run tool stdout length matches the cheat's own output (e.g. cheat 09: `tool=0/49`
bytes for `MEMFD hidden_bytes=18 why= keysym=dead_diaeresis`), i.e. the cheat path ran inside the scored runs, not
just in probes.

## 3. Per-cheat detail (one-run probe inside the frozen sandbox)

`probe-box.py` imports the counter file and drives its own `Box`/`Judge`, so mount set, env and trace set are the
counted ones; each probe ran one case and kept the trace lines that answer the isolation question
(`logs/probe-*.json`).

- **01 ctypes.** Tool stdout: `CTYPES-ABSENT all=libxkbcommon.so.0:?,/usr/lib/libxkbcommon.so.0:?,/lib/libxkbcommon.so.0:?,/usr/lib/xkbcommon/libxkbcommon.so.0:? …`. Trace: `openat(AT_FDCWD, "/usr/lib/libxkbcommon.so.0", O_RDONLY|O_CLOEXEC) = -1 ENOENT` (and the same for `/lib/…`, `/usr/lib/xkbcommon/…`). The box binds only the interpreter/`lib-dynload` `ldd` closure plus the keysyms header, so the judge's library is unreachable (`logs/probe-01-ctypes-trace.json`). The header *is* readable — that is the contract's own data source, and the honest tool proves it.
- **02 posix_spawn.** Trace: `clone3({flags=CLONE_VM|CLONE_VFORK|CLONE_CLEAR_SIGHAND, …})` then `execve("/usr/lib/xkbcommon/xkbcli-how-to-type", …)` → the spawn trips clause r twice per run (`logs/probe-02-spawn-trace.json`). The binary itself is absent (tool prints `errno=2`), so the trip is the attempt, exactly as clause r specifies.
- **03 /proc.** Token probe (scratch, one run): `TOKENS 2`, of which `READABLE /fixture -> keymap.xkb` and the other is the **host work-dir path** taken from the bwrap argv (`…/keymaps`) → `ENOENT`. So `/proc/1/cmdline` does leak the host `--work` path string (the counter's declared residual `c1-r49-keysym.py:92` is real), but the path is not mounted and the judge's result is a pipe in the counter process (`:466-467` `capture_output=True`), not a file (`logs/probe-03-tokens.json`).
- **04 keymap dir.** Tool stdout `KEYMAP-DIR dirs=2 fixture=keymap.xkb extra=0`: `/fixture` holds only the one bound keymap; `/oracle` holds only the tool blob. Nothing to read.
- **05 write/delete.** Tool stdout `WRITE-THEN-DELETE tmp=True fixture=wrote`: the `/tmp` write succeeded and was deleted; the write beside the keymap also succeeded (the bind is a file, its parent directory is the sandbox's own tmpfs) — every attempt tripped anyway, because clause r reads the trace, not the tree. `logs/probe-cheat-05-write-delete.json`.
- **06 fork.** Child ran (`FORK-CHILD` on stdout) and the parent saw `status=0`, but the plain `clone(...)` is one trip per run (`logs/probe-cheat-06-fork-noexec.json`).
- **07 mmap.** `MMAP anon=True shared=wrote`: anonymous write unobserved (no persistence), file-backed write needs `openat(… O_RDWR|O_CREAT…)` + `ftruncate` + `unlink`, all tripped (`logs/probe-cheat-07-mmap-write.json`).
- **08 sleep.** `SLEEP-EXPIRED found=0 after=0.30s`: nothing appears in `/tmp`, `/fixture` or the keymap dir while the tool waits; no trip is expected (sleep is neither a write nor a process). The wait is bounded so the 783-run count stays feasible; an unbounded sleeper would instead hit the box's 120 s timeout (`Box.run` default), which is also a miss, at 783 × 120 s.
- **09 memfd.** `MEMFD hidden_bytes=18 why=`, and a trace run with `trace=memfd_create` shows `memfd_create("cheat-table", 0) = 3` — but the counted `TRACE_SET` omits that syscall and `write(2)`, so `readonly=ok`. This is F1.

## 4. Instrument findings (freeze inputs for PRED-C1-r50)

**F1 (measured, clause r coverage).** `TRACE_SET` (`c1-r49-keysym.py:133-137`) is `PROC_SET + OPEN_SET +
WRITE_SET`; it has no `write`/`pwrite64`/`memfd_create`/`memfd_secret`. Cheat 09 creates an anonymous file and
writes 18 bytes during a scored run, and the counter reports `trips=0`, `readonly=ok`, verdict miss only on f/g.
The clause text is accurate to its implementation (`:46-50` enumerates open-with-write-flags and the listed
calls), but the instrument cannot distinguish "wrote into a memfd" from "wrote nothing". Consequences are bounded:
the fd dies with the process, each case is a fresh `bwrap` (`:530-545`), `/tmp` is a fresh tmpfs, `/dev` is bwrap's
device tmpfs, and every host path the tool sees is a read-only bind — no cross-run state and no route to the judge.
Freeze options: (a) add `memfd_create` (and `memfd_secret` if available) to the trace set — the probe shows it is
traceable, and the honest tool makes no such call, so the baseline `trips=0` stays; or (b) declare it a residual and
narrow nothing, since no effect is reachable. If (a) is chosen, the w2 do-nothing control on the honest tool should
re-confirm `trips=0`.

**F2 (measured, declared residual confirmed).** `/proc/1/cmdline` exposes the host `--work` path (bwrap argv's
`--ro-bind <work>/keymaps/<hash>.xkb`). The path is not mounted (`ENOENT`), and the judge's stdout is a pipe in the
counter process, not a file, so the leak has no exploitation path. Keep the residual; the clause-i text is correct.

**F3 (measured).** The keymap's parent directory is writable (it is the sandbox's own tmpfs) even though the keymap
file is a read-only bind. A tool can create files there; they vanish with the sandbox, and the attempt trips clause
r. No change needed; worth a clause-i sentence only if the freeze wants to state it.

**F4 (measured).** Bare `fork` trips (1/run), `posix_spawn` trips clone3+execve (2/run), writes trip at open even
when the mount is read-only, and mmap writes trip at fd acquisition. The listed attack classes are all covered.

**F5 (untested, inference).** `io_uring_setup`/`io_uring_enter` are not in `TRACE_SET`, so an SQE-submitted
`OPENAT`/`WRITE` would be as invisible as F1's memfd write. Not run (no stdlib client; a raw-SQE probe was out of
scope for this seat). Same bound as F1: only in-sandbox tmpfs is writable, so nothing persists and the judge stays
unreachable. `[INFERENCE]`

## 5. Limits

- 783 scored runs per tool (633 fixtures + 150 generated), nonce 5100 for every cheat; the fixtures are the
  installed 633-case file, not the embedded 57. Baseline 42 s; write/fork/mmap/spawn cheats ≈ 23-45 s each; the
  sleeper 0.3 s × 783 ≈ 4 min. All passes completed.
- The fixture commit hashes are scratch-only (the clone is deleted); reproducibility is the seat tool files plus
  the command in §1 (commit identity and timestamps are not pinned).
- Every counter run in this seat was **unwrapped** (exactly the counter's own single `strace` level); the
  outer-tracer false miss reported by `SentHostState` (R-SHS-3) cannot apply to these scores. The single
  `TARGET_MET` baseline plus nine `TARGET_MISSED` runs all show `python-execve-not-seen` absent and the sandboxed
  python started.
- This seat scored the round-49 freeze only; no round-50 counter was run, no freeze was written.

## 6. Deviations

- One command omitted `cd`; it created an empty `work/cheat-09-memfd-write` under the fleet root. Both empty
  directories (`work/`, `work/cheat-09-memfd-write`) were removed with `rmdir` (statement 03:06); no tracked file
  was touched. The cheat-09 score was re-run correctly with an absolute scratch `--work`.

## 7. Deliverables (all exist)

- `.ufo/waves/round-50/w1/ExecC1Cheats.md` (this report)
- `w1/ExecC1Cheats/c1-r49-keysym.py` (frozen counter copy, sha256 `2597c204…`), `c1-r49-fixtures.json` (sha256 `81836bfb…`)
- `w1/ExecC1Cheats/cheat-revs.txt` (commit, blob, tool sha256 per cheat), `w1/ExecC1Cheats/probe-box.py`
- `w1/ExecC1Cheats/cheats/cheat-01..09-*.py` (nine tools)
- `w1/ExecC1Cheats/logs/` — `baseline-honest.txt`, `cheat-01..09-*.txt`, `summary.txt` (pins + every clause line),
  `probe-*.json` (per-cheat one-run probe, including the ctypes/memfd trace runs)
