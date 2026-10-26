# w2 SentC1Tripwire — clause r (strace tripwire) falsification, C1 / PRED-C1-r47

Seat `SentC1Tripwire`, wave `w2` (falsify), 2026-10-26. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`,
freeze `d7527d608ad2b2e3cc398fdde34db7947b254a1a` (base `60edb66e`). Scope: **clause r only** — "strace around
bwrap counts process starts and sockets". Every count below used `--nonce 47`.

Everything here is reproducible from this directory: `cand/` (candidate tools, sha256 in
`receipts/candidate-digests.txt`), `receipts/` (frozen-counter output per candidate), `harness/` (the same clause r
run by `probe.py`, which imports the frozen counter and reuses its `Box` / `check_trace` verbatim, so a harness trip
count *is* the counter's trip count), `probe.py`, `probe_pct.py` (same, with a substituted `TRACE_SET`).

## Verdict

| # | Claim tested | Result |
|---|---|---|
| **H1** | clause r sees "a process started" | **FALSE** — `fork`/`clone`/`clone3`/`vfork` are not in `TRACE_SET`. A candidate that forks a worker on **every scored run** scores `readonly=ok trips=0 verdict=TARGET_MET`. Live hole. |
| **H2** | clause r sees "a socket made" | **TRUE for `socket`/`socketpair`/i386 `socketcall`, UNPROVEN for io_uring** — io_uring-issued syscalls never appear in the trace (`IORING_OP_OPENAT` → fd 4, trips 0), but the only socket-creating opcode, `IORING_OP_SOCKET`, returns `EINVAL` on this host even unsandboxed, so no live socket bypass was demonstrable here. Latent hole. |
| **H3** | clause r is the "read-only" clause | **FALSE** — no write syscall is traced. A candidate that writes a file on every run scores `TARGET_MET readonly=ok`. |
| — | exec anywhere (execve/execveat/fexecve/posix_spawn/vfork+exec/thread exec/`#!`) | closed, 10 closures, all with `trips>=1` |
| — | signal the tracer, clearenv injection, inherited fds | closed (strace unreachable from the pid namespace; env is exactly 5 keys; no inherited socket) |

All three holes hold the *counter* while the reference tool (`cand/ref.py`, sha256 `762d042c…`) stays honest — they are
gaps between the clause and its own statement, not defects of the reference.

## What clause r states vs. what it measures

- Clause text, `quality/counters/c1-r47-terminal.py:46-49`: "after the line recording the execve of the sandboxed
  python3, any further traced event (a process started, a socket made or connected - by the tool or anything it
  forks) is a trip." The parenthetical asserts that a process started *is* a traced event. It is not.
- The filter, `quality/counters/c1-r47-terminal.py:82`: `TRACE_SET = "trace=execve,execveat,socket,socketpair,connect"`
  — no `clone`, `clone3`, `fork`, `vfork`; no `io_uring_enter`; no write syscall.
- Registration claim, `.ufo/waves/round-47/registration.md:36-37`: "r (strace around bwrap: no process
  and no socket after the sandboxed python3's execve)".
- Every line after the python3 execve is a trip (`quality/counters/c1-r47-terminal.py:174-190`), so the clause is
  purely "which syscall numbers show up": whatever the list omits is invisible.

## H1 — a process started is invisible (live, demonstrated on the full clause set)

**Exploit path.** Any candidate that starts a child with `os.fork()` (or `malloc`-free `clone`/`clone3`/`vfork`)
without an exec afterwards runs a second process in the sandbox and the trace shows nothing, because the only
process-creation syscall in the filter is `execve`/`execveat`. The child is confined (it cannot escape the
namespace), but it *exists*, which is exactly what the clause and the registration claim it rules out.

**Evidence 1 — the strongest form: all clauses pass.** `cand/ref_pipe.py` (sha256 `f93474de…`) is the L1 reference
with `print` computed *inside a forked worker*: the parent forks, the child calls `run_print` and writes
`out\0rc` into a pipe, the parent relays it. If the fork failed there would be no output at all, so
`fixtures=190/190` is itself proof that the second process ran, computed every answer, and exited normally.
Frozen counter, `receipts/ref_pipe.txt`:

```
PRED-C1-r47 clause=r trips=0
PRED-C1-r47: fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET
```

**Evidence 2 — the bare event.** `cand/ref_fork.py` (sha256 `880ad78e…`, reference + fork in the print path):
`receipts/ref_fork.txt` → `clause=r trips=0`, `verdict=TARGET_MET`.

**Evidence 3 — the fork really happens, and the child really runs.** `cand/fork_only.py` (sha256 `6d9f1ef9…`) forks,
the child writes its own pid file; `harness/fork_only.txt`:

```
rc=0 trips=0
  MARKER fork_only = b'child pid=3 ppid=2'
  MARKER fork_only_parent = b'parent saw child 3'
```

The frozen counter on the same candidate, `receipts/fork_only.txt`: `clause=r trips=0`, `readonly=ok` (the count is
`TARGET_MISSED` only because the tool answers nothing; clause r is what is being tested).

**Evidence 4 — `fork` + `_exit` in the parent, child detached**: `cand/fork_detach.py`, harness trips 0,
`receipts/fork_detach.txt` `readonly=ok`. (The detached child *is* then killed: its marker never appears —
namespace teardown when the sandbox's init exits. Liveness is closed; the event is not.)

**Severity / impact.** Medium, claim-level. The reference passes, and the forked child cannot leave the sandbox, so
nothing on the host changes. But the registered property "no process" is not measured at all: a future
`tools/mado-terminal.py` may fork workers, leak children or run a fork-based pipeline in every counted run and score
`TARGET_MET`. Any reader of `readonly=ok` believes something the counter did not check.

**Smallest remediation (verified).** Add the four creation calls to `TRACE_SET`:
`trace=execve,execveat,clone,clone3,fork,vfork,socket,socketpair,connect`. Measured with `probe_pct.py`
(`TRACE_SET` substituted, everything else untouched), `harness/` transcripts:

| candidate | old list | new list |
|---|---|---|
| `ref` (no fork) | 0 | **0** — no false positive |
| `ref_fork` (print path) | 0 | 1 (`clone(...)`) |
| `ref_pipe` (print path) | 0 | 1 (`clone(...)`) |
| `fork_only` (selftest) | 0 | 1 (`clone(...)`) |
| `fork_detach` (selftest) | 0 | 1 (`clone(...)`) |

Do **not** simply use `-e trace=%process,socket`: it also traces `exit_group`/`wait4`, and the counter turns every
post-execve line into a trip, so the honest reference then trips 7 times (`ref`, `%process,socket`) — the class must be
narrowed to creation syscalls, or `check_trace` must learn to ignore exit/wait.

## H2 — io_uring syscalls are invisible; socket creation through them is blocked on this host

`cand/iou_openat.py` (sha256 `ea60aa1a…`) builds a real io_uring ring with ctypes and issues four ops;
`harness/iou_openat.txt`, `trips=0`:

```
MARKER iou_openat = b"{'openat18': 4, 'socket45': -22, 'bind56': -88, 'pipe62': -22}"
```

`IORING_OP_OPENAT` returned **fd 4** — the kernel executed a syscall for the tool and the trace recorded nothing.
`IORING_OP_BIND` reached the kernel's socket path (`-88` = `ENOTSOCK`, expected for a bogus fd), so socket-family
opcodes are dispatched. `IORING_OP_SOCKET` returned `-22` (`EINVAL`).

That `EINVAL` is a host property, not a sandbox artifact: the same candidate run **outside** bwrap, with no strace and
no namespace (host kernel 7.2.11-arch1-1, `kernel.io_uring_disabled=0`), prints `socket45: -22` for the same SQE
(`harness/iou_openat_outside.txt`). So on this host a tool cannot create a socket through io_uring, and the frozen counter correctly
reports `receipts/io_uring_socket.txt` `trips=0` for an attempt that produced no socket (`harness/io_uring_socket.txt`
marker: `socket_fd=-22 cqe_res=-22`). The counter is not shown wrong here; the design is unproven.

**Why it still matters.** The invisibility is proven (openat fd 4 through the ring, trips 0) and is unmitigated by
anything in the counter: `io_uring_enter` is not in `TRACE_SET`. On a kernel where `IORING_OP_SOCKET` is accepted, or
for any other capability reachable through an SQE (write, unlink, rename), clause r sees nothing. The filter enumerates
five syscall numbers; io_uring is a general bypass of syscall-number filters.

**Severity.** Latent / medium. **Smallest remediation.** Add `io_uring_setup,io_uring_enter` to `TRACE_SET` (a tool
that models the resolver has no reason to build a submission ring; the reference makes none). That is a
config-only change with no false positive for the reference — not measured here, since measuring it would need the
opcode to succeed to mean anything.

## H3 — the clause labelled "read-only" traces no write

Clause r's label (`quality/counters/c1-r47-terminal.py:46`) is "read-only", and the reference's own contract
(`.ufo/waves/round-47/l1-draft/mado-terminal.py:4`) is "Read-only. Starts no process, opens no socket, writes no file."
Nothing in `TRACE_SET` observes a write.

`cand/ref_write.py` (sha256 `0da764f3…`) is the reference plus a stray write on every run —
`$TMPDIR/mado-stray-<pid>` and `<case root>/.rw/stray-write-<pid>`. `harness/ref_write.txt` shows the file really
exists on the host after the run (`MARKER stray-write-2 = b'mado-terminal wrote this'`, `trips=0`), and the frozen
counter, `receipts/ref_write.txt`:

```
PRED-C1-r47 clause=r trips=0
PRED-C1-r47: fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET
```

**Severity.** Low–medium. Writes are confined (ro-bind elsewhere, `EROFS`; `/tmp` is a per-run tmpfs; the case-root
`.rw` is the resolver's own cache directory), so nothing survives the run. But "read-only" is asserted by the label
and unenforced, and a candidate may rewrite its own cache bytes on every counted run without a mark.

**Smallest remediation.** Either drop the word from the clause and state "no process, no socket" (which is what the
code measures and what the registration's own line says), or teach `check_trace` to parse write-intent from
`openat`/`openat2`/`unlinkat`/`renameat2` — `-e trace=%file` cannot be used as-is, because the "any post-execve
line is a trip" rule makes every read a trip and the reference trips immediately.

## Closures (attempt → harness trips → frozen-counter trips / readonly)

All candidates in `cand/`, receipts in `receipts/` (frozen counter) and `harness/` (identical clause r).

| attempt | mechanism | harness trips | counter trips / readonly |
|---|---|---|---|
| `posix_spawn` | glibc `posix_spawn` (clone+execve) | 1 | 1 / fail |
| `vfork_exec` | ctypes `vfork` + `execve` | 1 | 1 / fail (selftest child crashed, rc 139) |
| `execveat` | ctypes `syscall(322, AT_FDCWD, "/bin/sh")` | 1 | 1 / fail |
| `memfd_fexecve` | `memfd_create` + `execveat(fd, "", AT_EMPTY_PATH)` | 1 | 1 / fail |
| `thread_exec` | `os.execl` from a Python thread | 3 | 3 / fail |
| `shebang` | `execv` of a `#!` script in the case root | 1 | 1 / fail |
| `fork_exec_after_exit` | fork, child execs while parent `_exit`s | 1 | — |
| `signal_then_exec` | SIGKILL every reachable pid (only pid 1 survives), then exec | 1 | 1 / fail |
| `ctypes_socket` | `libc.syscall(41, AF_UNIX, SOCK_STREAM, 0)` → fd 3 | 1 | 1 / fail |
| `int80_socketcall` | i386 `socketcall` via `int 0x80`, args in `MAP_32BIT` memory → fd 3 | 1 | 1 / fail (`socket(AF_UNIX, SOCK_STREAM, 0)  = 3`) |
| `io_uring_socket` | `IORING_OP_SOCKET` — kernel says `EINVAL`, no socket | 0 | 0 / ok (nothing happened) |
| `fdscan` | what the sandboxed python3 inherits | 0 | — `0 -> /dev/null`, `1,2 -> pipe:[…]`, no socket |
| `envscan` | does `--clearenv` hold | 0 | — env is exactly `HOME,LANG,PATH,PWD,TMPDIR`; no `LD_PRELOAD` reachable |
| `inert` | negative control | 0 | — |
| `missing tool` | path that does not exist | 1 (`python-execve-not-seen`) | — fails **closed**, no vacuous pass |

Notable: strace **decodes the i386 `socketcall` subcall as `socket(...)` and the filter matches it**, so the 32-bit
compatibility path is not a bypass; and the sandboxed process cannot reach the tracer (separate pid namespace — the
only pid `signal_then_exec` could kill is pid 1, its own).

## Reproduction

Hole H1 end to end (about 50 s; the clone lives outside the lane):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
S=/fast/scratch/hyaku/mado-r47/SentC1Tripwire; mkdir -p "$S"
D=$(mktemp -d -p "$S"); git clone -q --shared --no-checkout "$PWD" "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach d7527d608ad2b2e3cc398fdde34db7947b254a1a
cp .ufo/waves/round-47/w2/SentC1Tripwire/cand/ref_pipe.py "$D/tools/mado-terminal.py"
git -C "$D" add tools/mado-terminal.py
git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m cand
mkdir -p "$S/w"
python3 -I quality/counters/c1-r47-terminal.py --repo "$D" --rev HEAD --work "$S/w" --nonce 47
# -> clause=r trips=0 ; fixtures=190/190 explained=190/190 generated=150/150 readonly=ok verdict=TARGET_MET
```

Single-shot harness (no clone, ~1 s) — imports the frozen counter and runs one clause-r run:

```
python3 -I .ufo/waves/round-47/w2/SentC1Tripwire/probe.py "$S/w" \
        .ufo/waves/round-47/w2/SentC1Tripwire/cand/fork_only.py            # --selftest
python3 -I .ufo/waves/round-47/w2/SentC1Tripwire/probe.py "$S/w" \
        .ufo/waves/round-47/w2/SentC1Tripwire/cand/ref_pipe.py print --print-id
```

Remediation check (substitutes only `TRACE_SET`):

```
PCT_TRACE="trace=execve,execveat,clone,clone3,fork,vfork,socket,socketpair,connect" \
  python3 -I .ufo/waves/round-47/w2/SentC1Tripwire/probe_pct.py "$S/w" \
          .ufo/waves/round-47/w2/SentC1Tripwire/cand/ref_fork.py print --print-id   # trips=1
```

## Limits of this report

- I did not find a live socket bypass; the io_uring socket path is blocked by this host kernel (`EINVAL`, reproduced
  outside the sandbox). H2 is a proven invisibility of io_uring syscalls plus an unproven socket path on this host.
- Fork-family escapes are confined by the namespace: the detached child does not outlive the run (marker absent in
  `harness/fork_detach.txt`). No host-level effect was attempted or observed; nothing outside the sandbox was touched.
- Clause r was exercised through the frozen counter and through `probe.py`; the harness reuses the counter's own
  `Box`/`check_trace`, so harness trip counts are not an independent reimplementation. Both agree on every row above.
- Everything ran with `--nonce 47`; no other clause's verdict is claimed here (C2 untouched).
- No tool installs or upgrades were needed or made; `pacman` was not run; every resolver-shaped run used `--print-*`
  only and `XDG_CACHE_HOME` inside scratch. `/fast/scratch/hyaku/mado-r47/SentC1Tripwire` was removed after the
  receipts were copied here.

## Files

- `cand/` — 23 candidate tools (the reference, three reference variants, 15 attacks/controls, 4 probe/scan tools);
  digests in `receipts/candidate-digests.txt`.
- `receipts/*.txt` — 16 frozen-counter outputs, one per scored candidate (`candidate=`, `candidate_sha256=`,
  `committed_sha256=`, full clause lines, final `PRED-C1-r47:` line), plus `candidate-digests.txt`.
- `harness/*.txt` — clause-r transcripts: the same run once per candidate by `probe.py`, with the host-visible
  markers; `missing_tool.txt` (fail-closed control), `iou_openat_outside.txt` (no sandbox, no strace), and the
  `remediation-*.txt` pairs, each holding the new list and, below it, the frozen list on the same candidate.
- `probe.py`, `probe_pct.py` — clause-r harness (takes the work directory as argv[1]; no hardcoded `/tmp`).
