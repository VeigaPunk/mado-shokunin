# ExecStraceTrip — read-only tripwire probe (round 47 / w1)

Seat: ExecStraceTrip. Lane: `mado-shokunin`. Base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`.
Scope: probe the C1 tripwire design **before the L1 freezes it**. No lane file touched, no
mutation of host state, no terminal launched. Everything measured here was measured on this host
in this session; nothing is inferred from documentation.

Seat dir: `.ufo/waves/round-47/w1/ExecStraceTrip/` — `probe.py` (matrix harness), `tripwire.sh`
(reference tripwire), `auditwrap.py` (layer 2), `verify.sh` (evidence generator),
`receipts/` (raw output).

---

## 1. Bottom line

The draft tripwire works here, **but the naive spelling of it is unsound in four ways**, three of
which produce a silent false CLEAN. Freeze the corrected form below, not the sketch in the card.

| # | The sketch in the card | Measured consequence | Fix |
|---|---|---|---|
| 1 | `-e trace=execve,socket,connect` | misses `execveat` (ctypes `syscall(322,…)`) **and** misses a bare `os.fork()` — a real new process with no execve | use the syscall **classes** `%process,%network` and name-filter afterwards |
| 2 | count `execve` lines only | `fork_only` = 1 execve, 1 process → a pure-Python child process passes | also count `clone/clone3/fork/vfork` whose flags lack `CLONE_THREAD` |
| 3 | assume strace attached | when strace cannot write its log or the wrapper is not bound, the log is empty ⇒ "0 forbidden syscalls" ⇒ **CLEAN** | require a positive control: `execve == 0` or a missing log is **FAIL** |
| 4 | fake shells bound over `/bin/sh` | cannot bind over a symlink; a `#!/bin/sh` stub over the shells resolves to itself (ELOOP); a bind at `/usr/bin/bash` does not cover `/bin/sh` (separate mounts) | drop the shell stubs — the syscall layer already catches every execve; keep only the `xdg-terminal-exec` stub, and make it non-shell |

Layer 2 (`sys.addaudithook`) is stronger than the card assumes: on CPython 3.14 the **C extension**
raises `ctypes.call_function` for every foreign call, so a `ctypes.*` deny-list is a hard wall, and
hooks cannot be removed (no API; `PySys_ClearAuditHooks` is not reachable through ctypes).
Layer 2 still cannot see a syscall made without a ctypes call, which is why it stays the second
layer and strace stays the boundary.

Host probe: **47/47 expectations held** (`receipts/probe-run.txt:68`), tripwire cost **12–14 ms/run**.
Reference tripwire: 2/2 clean tools CLEAN, 6/6 forbidden behaviours FAIL, both fail-closed controls
FAIL correctly (`receipts/tripwire-matrix.txt:1-8`, `receipts/fail-closed.txt:1-3`).

---

## 2. Measured environment

`receipts/environment.txt:1-7`:

```
kernel 7.2.11-arch1-1 | python Python 3.14.8 | strace 7.2 | bubblewrap 0.13.1
yama_scope 1 | seccomp 0
```

Inside the sandbox the tool sees `CapEff: 0000000000000000`, `NoNewPrivs: 1`, `Seccomp: 0`, and
`yama ptrace_scope` is still 1 — the parent/tracer relationship is what makes `strace -f` legal,
not a relaxed host setting (`receipts/probe-run.txt:2-6`).

---

## 3. Layer 1 — the syscall boundary

### 3.1 It works inside `bwrap --unshare-all`

`receipts/probe-run.txt:2-6` — PASS on three sandbox spellings:

- `--unshare-all` full root (only `/usr /bin /sbin /lib /lib64 /etc /proc /dev` + `/tmp` tmpfs),
- `--unshare-user --unshare-pid --unshare-net` only,
- log via `-o /dev/stderr` — needs **no writable bind at all**.

`strace -f` follows children across the pid namespace (`subprocess` shows the child's execve with
the child's own pid) — so the counter does not need a second sandbox per test.

### 3.2 Exactly one execve for a pure-Python tool

`receipts/trace-clean.txt:1-2` — the whole trace of a clean run is two lines: the interpreter
execve and `exit_group(0)`. Zero sockets, zero clones. 46 matrix rows agree
(`receipts/probe-run.txt:9-26`).

### 3.3 What fires, and what nearly does not

From `receipts/probe-run.txt:9-26` (`exec / socket / net / process / thread`):

| case | counts | tripwire |
|---|---|---|
| `pure` | 1 / 0 / 0 / 0 / 0 | clean |
| `thread` (Python threading) | 1 / 0 / 0 / 0 / **1** | clean — `CLONE_THREAD` |
| `execv`, `execve`, and a **failed** `execv` to a missing path | 2 / … | FIRES |
| `subprocess`, `subprocess(shell=True)`, `os.system`, `posix_spawn`, `os.spawnv` | 2 / … / process 1 | FIRES |
| **`fork_only`** | **1** / 0 / 0 / **1** / 0 | FIRES only because clone is counted |
| `ctypes_execve`, `ctypes_execveat` | 2 / … | FIRES |
| `socket(AF_UNIX)`, `socket(AF_INET)`, socket via ctypes | 1 / **1** / … | FIRES |
| `socket.getaddrinfo("localhost")` | 1 / **4** / **7** | FIRES (netlink + resolv) |

Two calibration facts for the freeze:

- The threshold `execve == 1` is exactly right, not merely "about right": the **real pinned judge**
  under the same sandbox is `execve_total 6` — `/usr/bin/{tr,find,ls,md5sum,awk}` plus the script
  itself (`receipts/real-judge.txt:25`). Any shell-based implementation of the tool is caught.
- Threads are invisible to an execve rule and would be a false positive under a clone rule, so
  the rule must be `clone without CLONE_THREAD`, not `clone`. `receipts/trace-threads.txt:2` shows
  the discriminating flag on this host (`flags=CLONE_VM|…|CLONE_THREAD|…`), and
  `receipts/trace-bad-fork.txt` shows the process variant (`flags=CLONE_CHILD_CLEARTID|…|SIGCHLD`).

### 3.4 The filter must be the CDN of syscall classes

`receipts/probe-run.txt:29-30`: with `-e trace=execve` alone, both `ctypes_execveat` and
`fork_only` read as `exec=1 process=0 → MISSED`. `%process,%network` catches both and survives
kernel/strace version drift better than a hand-written name list, because a name list is a promise
about the kernel ABI that nothing enforces. `%process` is noisy (`wait4`, `exit_group`, `SIGCHLD`
records), so the parser must dispatch on the syscall name, which `tripwire.sh` does.

---

## 4. Layer 2 — `sys.addaudithook`

### 4.1 Coverage

`receipts/probe-run.txt:33-42`. Fires for `os.exec`, `os.system`, `os.posix_spawn`, `os.fork`,
`subprocess.Popen`, `socket.__new__`, and — the one a hand-written deny-list will miss —
**`_posixsubprocess.fork_exec`** when `_posixsubprocess` is called directly
(`receipts/audit-bad-forkexec.txt:1`). Deny-list by **prefix**, not by enumeration.

### 4.2 ctypes does *not* bypass it on CPython 3.14

This is the correction the card's phrasing ("whether ctypes bypasses them") needs:
`ctypes.call_function` is raised **from `_ctypes` (C), not from Python** — `'call_function' in
inspect.getsource(ctypes)` is `False`, and `strings _ctypes*.so` lists `ctypes.call_function`,
`ctypes.dlsym/handle`, `ctypes.cdata`. Consequently:

- `ctypes.CDLL(None).getpid()` ⇒ `ctypes.dlopen ×2, ctypes.dlsym, ctypes.call_function`
  (`receipts/audit-bad-ffi.txt:1-4`);
- the `_ctypes`-only route that skips every Python-level ctypes wrapper
  (`type("F", (_ctypes.CFuncPtr,), …)(dlsym_addr)()`) **still** raises `ctypes.call_function`
  (`receipts/probe-run.txt:47`);
- a `ctypes.*` deny-list therefore closes the FFI route, including for a tool that never imports
  `ctypes` deliberately.

### 4.3 It cannot be switched off

`receipts/probe-run.txt:45-50`:

- `sys.audit = lambda *a, **k: None` → `os.exec` still fires;
- `ctypes.CDLL(None).PySys_ClearAuditHooks` resolves to `None` (`symbol_reachable=False`) and the
  following `os.exec` still fires — the C symbol is not exported.

### 4.4 The wrapper is byte-transparent

`receipts/fail-closed.txt:1` — stdout is byte-identical through `runpy` (checked with `cmp`, UTF-8
payload), and exit codes 0/1/2/3 pass through unchanged (`receipts/probe-run.txt:59,62`). So the
counter can run layer 2 **and** still compare stdout + rc against the pinned script.

---

## 5. Layer 3 — fake binaries (keep, but only one of them)

`receipts/probe-run.txt:53-56`:

- binding a stub over `/usr/bin/xdg-terminal-exec` works: the tool sees `rc=42`, `STUB-XDG`;
- a bind at `/usr/bin/bash` does **not** cover `/bin/sh` — `/bin` and `/usr/bin` are separate
  mounts in the sandbox, `/bin/sh` still resolved to the real interpreter;
- binding a `#!/bin/sh` stub over **both** `/bin/bash` and `/usr/bin/bash` makes `/bin/sh` resolve
  to the stub, which itself needs `/bin/sh`: `execvp /bin/sh: Too many levels of symbolic links`.
  A shell-script stub for the shells is self-recursive by construction.

Also: `bwrap` refuses `--ro-bind` onto a symlink destination outright
(`Can't mount on symlink destination /usr/bin/sh`, `receipts/probe-run.txt:56`), so the card's
"fake binaries bound over … the shells" cannot be spelled that way at all.

Recommendation: keep the `xdg-terminal-exec` stub (cheap, catches a launcher shim), drop the shell
stubs, and make the stub `#!/bin/false` + `exit 42` rather than a shell script.

---

## 6. The recommended C1 tripwire (freeze-ready)

Three predicates, each with the boundary this probe measured. `tripwire.sh` in the seat dir is a
working implementation; `verify.sh` regenerates every receipt.

```
bwrap --unshare-all --die-with-parent --new-session \
      --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /sbin /sbin \
      --ro-bind /lib /lib --ro-bind /lib64 /lib64 --ro-bind-try /etc /etc \
      --proc /proc --dev /dev --tmpfs /tmp \
      --ro-bind "$TOOLDIR" "$TOOLDIR" --ro-bind "$CASEDIR" "$CASEDIR" \
      --bind "$LOGDIR" "$LOGDIR" \
  strace -f -qq -e trace=%process,%network -o "$LOGDIR/trace" \
      python3 -I "$TOOLDIR/mado-terminal.py" print …
```

**P1 (processes).** `execve + execveat == 1` — the single interpreter execve. `>1` fails, including
a *failed* execve attempt (a missing helper is still an attempt to start a process).
**P2 (processes that do not exec).** `clone/clone3/fork/vfork == 0` after discarding lines whose
flags mention `CLONE_THREAD`. Threads are allowed; a forked child is not.
**P3 (sockets).** `socket + socketpair == 0`, and `connect/bind/sendmsg/recvmsg/sendto == 0`.

Plus two **mandatory fail-closed conditions**, both demonstrated failing correctly
(`receipts/fail-closed.txt:2-3`):
**P0a** the trace file must exist and be non-empty (`trace_missing`);
**P0b** the audit wrapper must print `AUDIT_SUMMARY <n>` (`audit_layer_did_not_run`).
Without these, a broken sandbox is indistinguishable from a clean tool — this is exactly the bug
this seat found in its own first draft, when a bind-order mistake made every case "CLEAN".

Layers, in order of authority:

1. strace predicates P0a/P1/P2/P3 — the boundary; language-independent.
2. `python3 -I auditwrap.py TOOL …` with a `ctypes. / socket. / subprocess. / os.exec… / os.fork…
   / _posixsubprocess.` prefix deny-list — defence in depth and the only layer that names *what*
   the tool tried to do.
3. the `xdg-terminal-exec` stub — belt only.

Do **not** put the verdict on stdout: stdout must carry the tool's bytes so the counter can compare
it byte-for-byte with the pinned script (`receipts/fail-closed.txt:1`); `tripwire.sh` writes
`MADO_TRIPWIRE:` to stderr for exactly that reason.

`python3 -I` also constrains the *tool*: `sys.path[0]` is `…/python314.zip`, not the script dir, so
`import` of a sibling module fails. That is fine for a single-file stdlib-only tool and should be
stated in the contract as a requirement, not discovered later as a flake.

---

## 7. Interop with the judge side (verified, not assumed)

The same sandbox spelling runs the pinned real script (`sha256 89f2be9a…3127ac`,
`receipts/real-judge.txt:2`, matching the declared pin) with **byte-identical** stdout to the
unsandboxed cold-cache run (`receipts/real-judge.txt:6-9` vs `:12-15`), provided
`XDG_CACHE_HOME` is bound read-write (its print modes write a cache file). `socket_connect_lines 0`
for the judge (`receipts/real-judge.txt:25`), so the judge itself is clean under the same instrument
that judges the tool. Reproduced by `verify.sh` step 5, which also asserts host/sandbox equality.

---

## 8. Residual risk — what this probe did **not** prove

1. **`strace -f` inside an unprivileged userns is host-configuration dependent.** It works here
   (kernel 7.2.11-arch1-1, bwrap 0.13.1, yama 1). On a host with `kernel.unprivileged_userns_clone=0`
   or a locked-down `ptrace_scope`+LSM, the trace comes back empty — which is why P0a is not
   optional. [INFERENCE] on hosts other than this one; measured only here.
2. **A tool that makes a raw syscall without any ctypes call** would be invisible to layer 2. Pure
   Python cannot do this on 3.14 (executable memory cannot be called without a ctypes call, and
   every ctypes call raises `ctypes.call_function`), so this is a *theoretical* residual, not a
   demonstrated one — and P1/P2/P3 would still catch the syscall.
3. **`%process,%network` is strace's vocabulary, not the kernel's.** Verified with strace 7.2; an
   older strace may reject an unknown class, which yields an empty trace and a P0a FAIL (safe), not
   a silent pass.
4. **A stdlib call that touches netlink trips P3.** `socket.getaddrinfo` produced 4 sockets and 7
   net syscalls in a single call. The tool must avoid `getaddrinfo`/`gethostbyname` (and any
   `uuid.getnode()`-style probe). This is a *tool-side* constraint the C1 contract should name,
   otherwise a legitimate implementation can be failed for a stdlib side effect.
5. The audit layer's event vocabulary is CPython-version specific. Measured on 3.14.8 only; pin
   `python3` in the counter or the deny-list may under-match on another interpreter.

---

## 9. Files written (all inside this seat's dir; no tracked lane file touched)

| path | role |
|---|---|
| `.ufo/waves/round-47/w1/ExecStraceTrip/probe.py` | 47-row matrix harness; `--work`, `--keep`, `--json`; exit 0 iff every expectation holds |
| `.ufo/waves/round-47/w1/ExecStraceTrip/tripwire.sh` | reference tripwire (strace + audit + fail-closed guards); verdict on stderr |
| `.ufo/waves/round-47/w1/ExecStraceTrip/auditwrap.py` | layer-2 runpy wrapper |
| `.ufo/waves/round-47/w1/ExecStraceTrip/verify.sh` | regenerates `receipts/` and re-checks the tripwire matrix |
| `.ufo/waves/round-47/w1/ExecStraceTrip/quotecheck.sh` | greps every fragment quoted above against `receipts/`; exits non-zero if any quote is absent |
| `.ufo/waves/round-47/w1/ExecStraceTrip/receipts/**` | 12 files: `environment.txt`, `probe-run.txt`, `tripwire-matrix.txt`, `fail-closed.txt`, `trace-{clean,threads,bad-fork,bad-subprocess}.txt`, `audit-{clean,bad-ffi,bad-forkexec}.txt`, `real-judge.txt` |

Reproduce: `TMPDIR=<scratch> bash .ufo/waves/round-47/w1/ExecStraceTrip/verify.sh --work <scratch>`
→ `MADO_VERIFY: all expectations held`, then `bash .ufo/waves/round-47/w1/ExecStraceTrip/quotecheck.sh`
→ `MADO_QUOTECHECK: all quotes located` (31/31 fragments).

Scratch `/fast/scratch/hyaku/mado-r47/ExecStraceTrip/` deleted at the end of this seat. Tool
installs/upgrades: **none** (no `pacman`, no `uv`, no network fetch).

---

## 10. Evidence index (locators computed with `grep -n`, never typed)

- `receipts/probe-run.txt:68` — `MADO_STRACE_PROBE: 47/47 expectations`
- `receipts/probe-run.txt:3-6` — sandbox + strace capability rows (PASS×4)
- `receipts/probe-run.txt:9-26` — 18-row syscall matrix
- `receipts/probe-run.txt:29-30` — execve-only filter gaps (both MISSED)
- `receipts/probe-run.txt:33-50` — audit coverage, FFI gateways, evasion attempts
- `receipts/probe-run.txt:53-56` — stub-bind behaviour, the ELOOP self-recursion and the refused symlink bind
- `receipts/probe-run.txt:59,62` — exit-status passthrough (0,1,2,3,4,126) + wrapper transparency
- `receipts/trace-clean.txt:1-2` — a clean run is exactly 1 execve + exit_group
- `receipts/trace-threads.txt:2` — `CLONE_THREAD` on the thread clone
- `receipts/trace-bad-fork.txt:2` — the process clone (`CLONE_CHILD_CLEARTID`, no `CLONE_THREAD`)
- `receipts/tripwire-matrix.txt:1-8` — reference tripwire: 2 CLEAN, 6 FAIL as declared
- `receipts/fail-closed.txt:1-3` — stdout byte-transparency + both fail-closed controls
- `receipts/audit-bad-ffi.txt:1-4` — ctypes route with `call_function`
- `receipts/audit-bad-forkexec.txt:1` — `_posixsubprocess.fork_exec` event
- `receipts/real-judge.txt:2,24,25` — judge pin, `execve_total 6`, `socket_connect_lines 0`
