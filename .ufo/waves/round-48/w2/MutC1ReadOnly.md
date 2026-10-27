# w2 / MutC1ReadOnly — mutate the C1 no-process / no-write boundary

Seat: `MutC1ReadOnly`. Round 48, wave w2 (FALSIFY), policy v1, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`.
Target under attack: `PRED-C1-r48`, clause `r` and the "no subprocess, socket or file write" sentence of the C1 contract.

Frozen bytes actually driven (all verified by SHA-256 inside this seat's replay repo):

| artefact | SHA-256 |
|---|---|
| `quality/counters/c1-r48-terminal-cache.py` | `2a7d03d96d6ea5489fecc110de8d29b83d6c3d2d6abd4e5d4138096d01ccddd4` |
| `quality/counters/c1-r48-fixtures.json` (warm) | `4d946bd7934d4afc40d16676a300a7a10ee077404a2d51e289d9db871cb311aa` |
| `quality/counters/c1-r47-fixtures.json` (cold) | `4836cc1d9e493af7bf15fa52f6e6855fe71c5c27911880847da668e1e313dd86` |
| pinned resolver `.ufo/waves/round-47/fetch/xdg-terminal-exec` | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` |
| reference tool `tools/mado-terminal.py` (= `l1-draft/mado-terminal.py`) | `1dfde36cfa68beffb6b2bc2ae9cf04875bd48702669812ce3ecd10b986753a92` |

Freeze state: commit `3e6c848a` ("round-48: freeze v1") is the lane tip; `git ls-tree -r --name-only HEAD` contains **no**
`corpus/knowledge/xkb-keymap-compile-r48.md` and no round-48 data file, so the pre-data window is still open and this
report is a **pre-freeze repair request**, not a post-data erratum.

## 1. Result

Two independent boundary violations **meet** the frozen predicate end-to-end:

| attack | violation | frozen functional clauses | clause `r` | frozen verdict |
|---|---|---|---|---|
| **M-WRITE** | writes files: a real file write into the sandbox `/tmp`, `tempfile.mkdtemp`, and write attempts on `$XDG_CACHE_HOME/xdg-terminal-exec`, `$HOME/.cache/xdg-terminal-exec`, the tree root | cold 190/190, warm 204/204, explained 394/394, generated 230/230, selftest 69/69 | `trips=0` | **TARGET_MET** |
| **M-FORK** | starts a process: `fork()`, md5 computed in the child, byte passed over a pipe, child reaped | cold 190/190, warm 204/204, explained 394/394, generated 230/230, selftest 69/69 | `trips=0` | **TARGET_MET** |
| M-SOCKET | `socketpair`, `socket(AF_INET)`, `socket(AF_UNIX)` + `connect` | sample 10/10 | `trips=4` per run | **caught** |
| M-EXECABS | absolute-path exec `/oracle/bin/ls` | cold 190/190, warm 204/204, explained 394/394, generated 230/230, selftest 69/69 | `trips=2454` | **TARGET_MISSED** |
| M-EXECMISS | exec **attempt** of a missing absolute path `/oracle/bin/r48-w2-no-such-binary` | sample 10/10 | `trips=1` per run | **caught** |
| M-EXECPATH | `ls` through `PATH` (first `<root>/bin/ls` → `ENOENT`, then `/oracle/bin/ls`) | sample 10/10 | `trips=33` (two `execve` per tool run) | **caught** |

Read the table as: **clause `r` is sound for the exec and socket axis and blind for the process-without-exec and
write axis.** Both blind classes are reachable by a tool that is otherwise a perfect C1 answer, so a control built on
either class MEETS — which the registration's own rule (`registration.md:14`: "every skip/mutant must miss, and a control
that meets triggers a fixture/counter repair before freeze") forbids.

`registration.md:11` claims for C1: "…; no subprocess, socket or file write." `registration.md:12` defines clause `r` as
"(r) strace after the sandboxed Python exec sees no further exec/socket/connect" — i.e. the registered contract is wider
than the registered instrument, in exactly two places.

## 2. Why the instrument is blind (frozen text, not inference)

* `quality/counters/c1-r48-terminal-cache.py:141` — `TRACE_SET = "trace=execve,execveat,socket,socketpair,connect"`.
  No `clone`, `clone3`, `fork`, `vfork`; no `open`, `openat`, `openat2`, `creat`, `write`, `mkdir`, `unlink`, `rename`,
  `truncate`.
* `:305-308` — the tool is always wrapped: `if tool: … [strace, "-f", "-qq", "-e", TRACE_SET, "-e", "signal=none", "-o",
  trace] + argv`. Every tool invocation (selftest, fixtures, generated, explain, explain --observed) goes through it, so
  the gap is the filter, not a missed call site.
* `:331-363` — `check_trace` scores `trip = re.compile(r"^(execve|execveat|socket|socketpair|connect)\(")` on lines that
  appear **after** the `execve("/usr/bin/python3"` line. `:983` — `readonly = "fail" if box.trips else "ok"`.
* There is **no tree fingerprint anywhere** in the counter: the only `os.walk` is `:411` inside `apply_mtime`
  (`grep -n "os.walk\|fingerprint\|snapshot" quality/counters/c1-r48-terminal-cache.py` → `411:    for d, ds, fs in
  os.walk(root):`). So the "tree check" half of this seat's assignment does not exist in the frozen instrument.
* `:279` — `mode = "--ro-bind" if tool else "--bind"`, applied to the tool tree **and** its `.rw` at `:282-284`. For tool
  runs the whole fixture tree incl. the cache path is mounted read-only; that mount, not clause `r`, is what stops a
  cache write from landing in the scored tree.

## 3. Evidence

All runs used a fresh replay repo built from the frozen bytes and driven only from scratch
(`/fast/scratch/hyaku/mado-r48/MutC1ReadOnly`), `--nonce 4848`, `--work` outside the repo. Mutants are the frozen
reference with **one hook inserted immediately before `if __name__ == "__main__":`**; the hook does its violation, prints
one `R48PROBE …` line on **stderr** and never touches stdout or the exit status. stderr is discarded by the counter
(`run_case` keeps `_t_err` and drops it; `explain_case` likewise), so a mutant is functionally the reference tool unless
the hook raises — and it never raises. Exact insertions: `receipts/mutants.diff` (7 308 B).

### A1 — M-WRITE: file writes are unobservable (full counter run)

```
cp <mut>/M-WRITE.py $D/tools/mado-terminal.py; git -C $D commit -m "mut M-WRITE"   # rev af870e18fe2ae6ddfc027350871dbd8eb3dcb14c
python3 -I $D/quality/counters/c1-r48-terminal-cache.py --repo $D --rev af870e18… --work $S/work/full-M-WRITE --nonce 4848
```

```
PRED-C1-r48 clause=a tool=present
PRED-C1-r48 clause=s rc=0 last='MADO_TERMINAL_SELFTEST: 69/69 passed'
PRED-C1-r48 clause=f cold=190/190
PRED-C1-r48 clause=w warm=204/204
PRED-C1-r48 clause=x explained=394/394
PRED-C1-r48 clause=g generated=230/230
PRED-C1-r48 clause=r trips=0
PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
rc=0                                   (7m36s, receipts/full-M-WRITE.head)
```

What the hook actually did, reported by the tool itself on the stderr the counter ignores
(`receipts/probe-M-WRITE.txt`, one selftest run under the frozen sandbox argv):

```
TOOL_STDERR R48PROBE cache=EROFS homecache=EROFS tmp=ok treeroot=EROFS mkdtemp=ok:r48-w2-j16_agwg
TREEFP pre=debf06a45cc8818b post=debf06a45cc8818b same=True
TRIPS_AFTER_HOOK 0
```

So: the cache write and the tree-root write are refused by the `--ro-bind` mount (EROFS), while a temp directory and a
real 7-byte file inside `/tmp` succeed — and **neither** is visible to clause `r` (`trips=0`) **nor** to a tree
fingerprint of the tool tree (`same=True`). Wide-filter trace of the same run, tool pid `40140`
(`receipts/traces/trace-M-WRITE-wide.txt:355-364`):

```
40140 openat(AT_FDCWD, "<root>/.rw/cache/xdg-terminal-exec", O_WRONLY|O_CREAT|O_TRUNC|O_CLOEXEC, 0666) = -1 EROFS
40140 mkdir("<root>/home/.cache", 0777) = -1 EROFS
40140 openat(AT_FDCWD, "/tmp/r48-w2-probe", O_WRONLY|O_CREAT|O_TRUNC|O_CLOEXEC, 0666) = 3
40140 write(3, "r48-w2\n", 7) = 7
40140 openat(AT_FDCWD, "r48-w2-probe", O_WRONLY|O_CREAT|O_TRUNC|O_CLOEXEC, 0666) = -1 EROFS
40140 mkdir("/tmp/r48-w2-lcmzqj4r", 0700) = 0
```

The frozen trace of the same run contains four lines and no write of any kind
(`receipts/traces/trace-M-WRITE.txt`): `execve("/usr/bin/bwrap")`, two bwrap `socket()`s, `execve("/usr/bin/python3")`.

Write-surface partition inside a tool run (`receipts/probe-M-WRITE2.txt`, hook reporting per target):

```
TOOL_STDERR R48PROBE tmp=ok devshm=ok dev=ok run=ok vartmp=ok root=ok oraclebin=EROFS usrlib=EROFS proc=ENOENT etc=ok cwd=EROFS
TRIPS_TOTAL 0
```

Every `=ok` target is inside bwrap's own tmpfs (`--tmpfs /`, `--tmpfs /tmp`, `--dev`); every host-backed path
(`/oracle/bin`, `/usr/lib`, the tool tree, its `.rw`) is `EROFS`. So the property that actually matters — *nothing the
tool writes survives to the host or reaches the scored tree* — is enforced by the **mount table**, and is not measured
by any clause.

**And the reference itself writes.** Wide trace of the untouched reference during `--selftest`
(`receipts/traces/trace-REF-wide.txt`), pid-scoped to the sandboxed python `1745964`:
220 `openat(… O_WRONLY|O_CREAT|O_TRUNC …)`, 513 `mkdir`, 677 `unlinkat`, **all** under
`/tmp/mado-terminal-selftest.5h0k2kv6`, zero outside it. Read literally, `registration.md:11`'s "no … file write" and the
tool's own docstring line 4 ("Read-only. Starts no process, opens no socket, writes no file.") are false of the reference
implementation. The claim needs restating before it can be frozen as a contract.

### A2 — M-FORK: a process without an exec is unobservable (full counter run)

```
git -C $D commit -m "mut M-FORK"          # rev 0cca36e546727bf1e93c144eb172aadbcde95b50
python3 -I $D/quality/counters/c1-r48-terminal-cache.py --repo $D --rev 0cca36e5… --work $S/work/full-M-FORK --nonce 4848
```

```
PRED-C1-r48 clause=r trips=0
PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET
rc=0                                   (6m33s, receipts/full-M-FORK.head)
```

Hook report (`receipts/probe-M-FORK.txt`): `TOOL_STDERR R48PROBE fork=ok:pid_rc=0:md5_in_child=603422e3`, `TRIPS_TOTAL 0`.
The process really existed; wide trace, tool pid `43905` (`receipts/traces/trace-M-FORK-wide.txt:355`):

```
43905 clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0x7f4dd5794e90) = 3
```

The frozen trace of the same run (`receipts/traces/trace-M-FORK.txt`) is four lines again: bwrap execve, two bwrap
sockets, python execve. `clone`/`fork`/`vfork`/`clone3` are not in `TRACE_SET`, so "starts no process" is enforced only
for processes that `exec`.

### A3 — absolute-path executables (caught, positive control for clause `r`)

* `M-EXECABS` `subprocess.run(["/oracle/bin/ls","-d","/oracle"])`, output discarded. Probe: `execabs=ok:rc=0:out=b'/oracle\n'`,
  trip `execve("/oracle/bin/ls", ["/oracle/bin/ls", "-d", "/oracle"]…`, `trips=17` over 17 tool runs. Full counter:
  `clause=r trips=2454`, `readonly=fail`, `verdict=TARGET_MISSED` with every functional clause still perfect
  (`cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok`; `receipts/full-M-EXECABS.head`).
* `M-EXECMISS` exec of a path that does not exist: `execmiss=ENOENT`, trip
  `execve("/oracle/bin/r48-w2-no-such-binary", …) = -1 ENOENT`. A mere *probe* for executables is already a trip.
* `M-EXECPATH` `subprocess.run(["ls", …])`: the trip set contains both `<root>/bin/ls … = -1 ENOENT` and
  `/oracle/bin/ls … = 0`, so PATH lookups are covered as well (`receipts/traces/trace-w1-dl-fx-02.txt`).

### A4 — sockets (caught)

`M-SOCKET` (`socketpair` + send/recv, `socket(AF_INET)`, `socket(AF_UNIX)` + `connect` to a missing path):
`R48PROBE socketpair=ok:b'r' socket=ok:fd=3 connect=ENOENT`, `trips=4` in the first run, `TRIPS_TOTAL 68`.
Frozen trip lines (`receipts/probe-M-SOCKET.txt`, `receipts/traces/trace-M-SOCKET.txt`):

```
socketpair(AF_UNIX, SOCK_STREAM|SOCK_CLOEXEC, 0, [3, 4]) = 0
socket(AF_INET, SOCK_STREAM|SOCK_CLOEXEC, IPPROTO_IP) = 3
socket(AF_UNIX, SOCK_STREAM|SOCK_CLOEXEC, 0) = 3
connect(3, {sa_family=AF_UNIX, sun_path="/r48-w2-no-such.soc…
```

Note the failed `connect` (ENOENT) still trips: the socket axis is enforced on the syscall, not on success.

### A5 — re-scoring the w1 control set on the frozen instrument

`w1/ExecControlsC1/controls` tools driven unchanged through the frozen counter module (they are base-tool mutants,
selftest 43/43):

| control | sample | trips | note |
|---|---|---|---|
| `reference.py` | 10/10 | 0 | baseline |
| `writes-cache.py` | 7/7 (2 cold, 3 primed warm, 2 explain) | **0** | MEETS on the frozen instrument; only w1's own local fingerprint caught it (their F4) |
| `delegate-ls.py` | 10/10 (cold + literal-cache warm, no gen_hash) | **0** | the sample never reaches `gen_hash` → the exec trips disappear |
| `delegate-ls.py` | 7/7 (2 primed warm) | **20** | `execve("/oracle/bin/ls", ["ls","-LRl",…])` |
| `md5-subproc.py` | 7/7 (2 primed warm) | **20** | `execve("/oracle/bin/md5sum", …)` |

Two consequences. (i) `writes-cache` as shipped in w1 is built on the base tool, so on the frozen merged fixture set it
will miss on clause `w` for the wrong reason (no warm model), which masks the boundary gap — my M-WRITE isolates it by
being the frozen reference *plus* a write. (ii) A control sample made only of cold and literal-cache warm fixtures
silently skips the exec trips; any re-scored control set must include primed warm fixtures.

## 4. The clause that is needed

The seat used three independent instruments on the same runs (frozen trace, wide-filter trace, host-side tree
fingerprint). The minimum repair that makes each blind class observable:

1. **Processes.** Add `clone,clone3,fork,vfork` to `TRACE_SET` and score them by the tool's pid tree rather than by the
   `seen` ordering. Soundness measured on the reference: post-exec `clone|clone3|fork|vfork` lines for the reference's
   pid = **0** (and 0 across the whole post-exec trace), so the reference does not false-positive; bwrap's own
   namespace `clone(… CLONE_NEWNS|…|SIGCHLD)` happens *before* the python execve and is skipped by the existing gate.
2. **Writes.** `openat` write-intent cannot be expressed in `-e trace=` (flags, not syscall names), so it has to be
   post-filtered in `check_trace`: count `open|openat|openat2|creat|mkdir|mkdirat|unlink|unlinkat|rename|renameat2|
   truncate|ftruncate` for the tool's pid and fail on any path **not under `$TMPDIR`** (and on any cache-path or tree
   write). Measured baseline so the clause can be written without breaking the reference: the reference's own selftest
   performs 220 write-intent opens, 513 mkdirs and 677 unlinkats, **all** under `/tmp/mado-terminal-selftest*`, so a
   `$TMPDIR` exemption keeps it green while M-WRITE's cache/home/tree attempts are flagged.
3. **A tree fingerprint alone is not enough** (and is currently absent). It cannot see `/tmp`, and the ro-bind already
   makes tree writes `EROFS`, so it would buy only belt-and-braces. If it is added, it must be taken around the tool
   `run()` only — `explain_case` deliberately creates the three `--observed` captures inside the tool tree's `.rw`
   (counter `:699-703`), so a fingerprint spanning `explain` would fail on the counter's own writes.
4. **Registration text.** `registration.md:11` must stop claiming "no … file write" as written, because the reference
   writes under `$TMPDIR` during `--selftest`. State it as: *no write outside a private `$TMPDIR` tree; the scored tree
   and the cache path are read-only by mount; no process other than the tool itself.*
5. **A fourth, cheaper option** for the temp-file half: bind an empty host directory at `/tmp` instead of `--tmpfs /tmp`
   and require the run to leave nothing there except a single documented `mado-terminal-selftest.*` tree. This catches
   "creates a temp file outside its own workspace" with no tracing at all.

Until one of 1/2 (or 5) lands, `TARGET_MET` does not distinguish the reference from M-WRITE or M-FORK.

## 5. Residuals and notes (not scored)

* The pre-`seen` gate (`:350-356`) exempts **every** traced event that appears before the python execve, including
  bwrap's own two `socket()`s (visible in `trace-M-WRITE.txt`). It is not pid-scoped. Currently unexploitable — the tool
  cannot emit an event before its own exec — but any future change that puts another traced process in the same strace
  run would be silently exempt.
* stderr is not compared anywhere in `PRED-C1-r48`; this seat's hooks rely on it. It is a free channel for a tool to
  report anything, including the fact that it violated the contract.
* The counter's own `readonly` gate is a single AND-ed term (`:983`, `:986`), so one trip anywhere already forces
  `TARGET_MISSED`. That is why M-SOCKET / M-EXECMISS / M-EXECPATH are reported "caught" from sampled probes: their first
  run trips, so the verdict is fixed independently of the fixture outcome (`[derived from :983/:986]`), whereas M-WRITE
  and M-FORK were run end-to-end.
* The host-facing `save_cache` risk is untested by any clause: the sandbox ro-binds the cache path, so `PRED-C1-r48`
  never exercises a tool writing the *real* `$XDG_CACHE_HOME`. A tool could write the host cache in a normal run and this
  counter would not notice.
* Filed per the seat rules: this is a **miss**, not an erratum. No predicate, counter, fixture, claim or target was
  changed, narrowed or re-frozen by this seat.
* State at hand-in: `quality/counters/c1-r48-terminal-cache.py` still hashes `2a7d03d9…` and the warm fixtures
  `4d946bd7…`, i.e. every measurement above is against the instrument the freeze commit ships. An **untracked**
  `l1-draft/v2/` tree (`c1-r48-terminal-cache-v2.py`, `c1-r48-fixtures-v2.json`) and `receipts/v2/` appeared in the lane
  while this seat ran; it was not read as an instrument, not scored, and none of the numbers above apply to it. If v2
  lands, M-WRITE and M-FORK must be replayed against it — they are the two controls v1 passes.
* Host tooling: nothing was installed or upgraded in this seat (no pacman transaction; the wave's `bwrap` 0.13.1 and
  `strace` 7.2 were already present).

## 6. Reproduce

```
# scratch (all of it under /fast/scratch/hyaku/mado-r48/MutC1ReadOnly, deleted after the receipts were copied)
D=$(mktemp -d -p /fast/scratch/hyaku/mado-r48/MutC1ReadOnly) && git -C "$D" init -q
mkdir -p "$D/tools" "$D/quality/counters" "$D/.ufo/waves/round-47/fetch"
cp <lane>/.ufo/waves/round-47/fetch/xdg-terminal-exec "$D/.ufo/waves/round-47/fetch/"
cp <lane>/quality/counters/c1-r47-fixtures.json "$D/quality/counters/"
cp <lane>/quality/counters/c1-r48-terminal-cache.py <lane>/quality/counters/c1-r48-fixtures.json "$D/quality/counters/"
cp <lane>/tools/mado-terminal.py "$D/tools/"      # = l1-draft tool, sha 1dfde36c…
git -C "$D" add -A && git -C "$D" -c user.name=m -c user.email=m@m commit -qm "r48 w2 replay base+draft"

# mutants (one inserted hook each, stderr only)
python3 mkmutants.py --ref "$D/tools/mado-terminal.py" --out "$S/mut" --diff receipts/mutants.diff

# the frozen counter, unmodified
python3 -I "$D/quality/counters/c1-r48-terminal-cache.py" --repo "$D" --rev <rev> --work "$S/work/<tag>" --nonce 4848

# frozen-check machinery only (imports the counter unchanged; no scoring)
python3 -I probe.py --counter …/c1-r48-terminal-cache.py --tool <mut>.py --work "$S/work" --tag <tag> \
        --cold 4 --warm 4 --prime 0 --explain 1
python3 -I dump.py  --counter …/c1-r48-terminal-cache.py --tool <mut>.py --work "$S/work" --tag <tag> \
        --out receipts/traces [--extend | --fixtures 1]
```

Revs of the four full runs (all on top of `a1ffbaa2f6ad8ecfc83e965240ea5929419c9e2d`, the replay base):
ref `a1ffbaa2…` (TARGET_MET, 4m50s), M-WRITE `af870e18…` (TARGET_MET, 7m36s), M-FORK `0cca36e5…` (TARGET_MET, 6m33s),
M-EXECABS `8616140b…` (TARGET_MISSED via `readonly`, 3m30s).

## 7. Guards, limits, cleanup

* Every writer shell started with `ulimit -f 2048` (512-byte units = 1 MiB per regular file). The probe subshell raised
  the soft limit to `8192` (4 MiB) **only** because the frozen counter itself copies `/usr/bin/gawk`
  (1 274 872 B) into its sandbox bin dir and aborts on `EFBIG` below that. Nothing this seat wrote into its own seat
  directory exceeded 1 MiB; the only >1 MiB files anywhere in scratch were those transient `bin-*/awk` copies, created by
  the frozen counter, not by this seat.
* Largest file produced by this seat: `receipts/traces/trace-REF-wide.txt`, 213 503 B. Every receipt is < 1 MiB.
* Total scratch: 54 897 187 B (≈ 52 MiB), deleted at the end of the seat (`rm -rf /fast/scratch/hyaku/mado-r48/MutC1ReadOnly`);
  seat evidence kept in this directory (796 KB).
* Fixture repo was `mktemp -d -p /fast/scratch/hyaku/mado-r48/MutC1ReadOnly`, `git init -q`; `git -C "$D"
  rev-parse --show-toplevel` was asserted equal to `$D` before every commit; identity was passed per-command
  (`-c user.name=m -c user.email=m@m`). No lane Git/jj operation, no commit/push outside that fixture repo, no pacman,
  no compositor/input/GUI action, no relative-path writes.

## 8. Files

* `w2/MutC1ReadOnly.md` — this report.
* `w2/MutC1ReadOnly/probe.py` — samples the frozen counter's own `Box`/`selftest_clause`/`run_case`/`explain_case`,
  prints the tool stderr it discards and a host-side tree fingerprint.
* `w2/MutC1ReadOnly/dump.py` — keeps the frozen trace for one run, and renders the same sandbox argv under a wide filter.
* `w2/MutC1ReadOnly/mkmutants.py` — builds M-WRITE, M-WRITE2, M-FORK, M-SOCKET, M-EXECABS, M-EXECMISS, M-EXECPATH.
* `w2/MutC1ReadOnly/receipts/` — `full-ref.txt`, `full-M-WRITE.head`, `full-M-FORK.head`, `full-M-EXECABS.head`,
  `probe-*.txt` (14), `mutants.diff`, `traces/` (10: the frozen and wide traces of REF/M-WRITE/M-FORK/M-SOCKET/
  M-EXECPATH plus the selftest and two fixture-run traces of `delegate-ls`).
