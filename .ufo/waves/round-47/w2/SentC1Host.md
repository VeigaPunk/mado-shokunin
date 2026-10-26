# SentC1Host — host risk of `explain` on the real `~/.config` (round 47, w2 FALSIFY)

Reviewed artifact: `.ufo/waves/round-47/l1-draft/mado-terminal.py`, sha256
`762d042c96e7e5f2c3187133b0ffe670c1d076b698b958199602cfa019aa6c08` (grep-verified copy of the frozen L1 draft at
d7527d60). Real resolver used as oracle: `.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (matches the pin), run by direct `execve`
(NOT `bash script` — under `bash script` its `alias`/`eval` candidate loop does not expand aliases and every case
fails; that cost one wasted round and is recorded here so no other seat repeats it).

Scratch: `/fast/scratch/hyaku/mado-r47/SentC1Host` (harness + case trees, deleted at the end; receipts copied to
`.ufo/waves/round-47/w2/SentC1Host/`). Every case tree is built under `env -i` with `XDG_*`, `HOME`, `PATH`,
`TMPDIR` pointed into scratch; every run is wrapped in `timeout -k 2`; no run touched the host config tree, and
`XDG_CACHE_HOME` was always in scratch when the real script ran.

## Verdict

`explain` on **this host's real trees is read-only, non-blocking and cheap**: 0.02 s wall, 15.9 MB peak RSS, 506 B
stdout, 111 traced syscalls, no creating open, no write to a descriptor above 2, no socket, no `execve`, host cache
file unchanged (`mtime=1793047345 size=190` before and after), and `verdict=AGREE` against a cold-cache capture of
the real script (`Alacritty.desktop`). Symlink loops, FIFOs and device files used as *list files or entries*, `/proc`
inside the XDG vars and permission errors are all handled without a hang and without a traceback.

Three defects remain outside that clean path, all reproduced below: a **blocking, unbounded read of the
`--observed` argument** (hang on a FIFO, memory blow-up on a character device), an **uncapped whole-file read**
(MemoryError/OOM on a large list or entry file where the real script streams), and a **recursion cap** in the
directory walk (RecursionError on trees deeper than ~995 where `find -L` succeeds). One fidelity divergence is
host-relevant in the other direction: a non-regular entry planted in `~/.local/share/applications` makes the *real*
resolver hang while the tool reports OK.

## Findings

### H1 — `--observed` is opened with a blocking, unbounded read (hang; memory blow-up). Severity: medium (availability)

`main` hands the operator's `--observed` path straight to `read_file` (`.ufo/.../l1-draft/mado-terminal.py:1043`,
`read_file` at `:167-169`), which does `open(path,"rb")` then `fh.read()` with no `fstat`, no `S_ISREG` test, no
size cap and no `O_NONBLOCK`. The list-file path does check `os.path.isfile` (`:436`); this path does not.

Reproduce (each command is complete):

```bash
mkdir -p /fast/scratch/hyaku/mado-r47/SentC1Host/ch && cd /fast/scratch/hyaku/mado-r47/SentC1Host
mkfifo ch/obs.fifo
timeout 5 /usr/bin/python3 -I tool.py explain --observed ch/obs.fifo ; echo rc=$?
#   rc=124                     (no output, no exit: blocked inside open)
strace -f -qq -e trace=openat -o ch/t.log /usr/bin/python3 -I tool.py explain --observed ch/obs.fifo
#   openat(AT_FDCWD, "ch/obs.fifo", O_RDONLY|O_CLOEXEC) = ? ERESTARTSYS (To be restarted if SA_RESTART is set)
# a symlink to the same FIFO, /dev/full and /dev/zero behave the same way (r04-observed-classes.txt)
```

Same class, measured: `--observed <symlink to a FIFO>` → `rc=124` at 5 s; `--observed /dev/full` → `rc=124` at 10 s
(reads zeroes for ever); `--observed /dev/zero` under `RLIMIT_AS=1.5 GiB` → exit 1 with an uncaught `MemoryError`
traceback ending at `read_file` `:169`. Without the cap the same call grows until the kernel OOM killer fires.

Exploit path: the operator types the documented usage — the docstring calls `--observed FILE` "the captured stdout
of …", and shell users reach for process substitution (`--observed <(xdg-terminal-exec --print-…)`) or `/dev/stdin`
on a terminal. A FIFO, a tty or a character device blocks the diagnostic for ever; the tool's own docs give no
bound. (A process-substitution FIFO is harmless while its writer keeps producing and then exits — measured rc 1 on
`--observed <(printf 'x\n')`; it blocks as soon as the writer stops writing without closing.) No host mutation, no
privilege gained — this is an availability defect in the tool, not in the host.

Smallest remediation: in `main`, `st = os.stat(rest[1])`, require `stat.S_ISREG(st.st_mode) and st.st_size <= CAP`
(e.g. 1 MiB), else `sys.stderr.write(...); return 2`; and open with `os.open(path, os.O_RDONLY|os.O_NONBLOCK)` if a
belt-and-braces FIFO guard is wanted. Three lines, no behaviour change for a real capture (84 B on this host).

### H2 — whole-file reads have no cap: MemoryError/OOM where the resolver streams. Severity: low-medium (availability)

`read_file` (`:167-169`) materialises the entire file as `bytes` and then again as `str` (latin-1). Measured with a
fresh child per run (`resource.getrusage(RUSAGE_CHILDREN).ru_maxrss` in a one-shot wrapper):

| input | tool | real script |
|---|---|---|
| clean tree (P1) | rc 0, 0.03 s, 15.6 MB | rc 0, 0.01 s, 11.9 MB |
| 270 MB `.desktop` of 1.8 M short lines (P3) | rc 0, **6.1 s, 984 MB RSS** | rc 0, **47.3 s, 11.6 MB RSS** |
| 42 MB list file, 2 M entry lines (P2) | rc 0, 4.0 s, **562 MB RSS** | rc 124: not finished in 180 s (no output in a 60 s re-run) |
| 4.2 MB list file, 200 k entry lines (P8, sweep only) | rc 0, 0.45 s, **71 MB RSS** | interrupted: still running when the harness hit its 300 s wall |
| 4 GiB sparse `.desktop`, no newline, `RLIMIT_AS=1.5 GiB` (C16) | rc 1, uncaught `MemoryError` traceback at `:534`→`:169` | not run (`read` in bash would also grow — declared as inference) |

The amplification is ~3.6× file size for an entry file (984 MB for 270 MB) and ~13× for a list file (562 MB for 42 MB, every line kept as a parsed id), so a 4 GB list file is tens of GB of RAM. The real
script's `while IFS= read -r` loop (`x:970`) streams at 12 MB. Reachability on a real host: an XDG data dir that
holds a large file whose name ends in `.desktop` (a stray log or dump), or a list file that grew.

Reproduce: build the tree, then
`python3 meas.py /usr/bin/python3 -I tool.py explain` vs `python3 meas.py <real> --print-id --print-path`
(`meas.py` in the receipts prints `rc/wall/rss_kb`).

Smallest remediation: cap in `read_file` (`fh.read(CAP)` and treat a truncated read as "unreadable"), or read the
list/entry files line by line as the shell loop does.

### H3 — the directory walk recurses to ~995 and then dies. Severity: low (crash; fidelity)

`_walk` (`:495-520`) recurses once per directory level (`:517`); nothing raises the recursion limit and the
`RecursionError` is not caught (`explain` catches only `Exit`, `:832-834`), so the process exits 1 with a traceback
and **no `MADO_TERM:` line** — `explain` produces no verdict at all.

Measured, same fixture shape, tool and real script on identical trees (`r03-deep.txt`):

- depth 990 (path 2071 chars, tree built by `python os.makedirs`): tool **rc 0**, selects `d…/deep.desktop`, 0.07 s.
- depth 1000 (tree built by `mkdir -p`): tool **rc 1**, `RecursionError: maximum recursion depth exceeded`, last
  frame `_walk` `:517`; 1100/1200/1300 in the sweep behaved identically; depth 1400 (C7): tool rc 1.
- the real script on the same 1400 tree: **rc 0**, prints the deep entry id and its path (0.06 s).
- The real script has no such limit (`find -L`, `x:766`, `x:795`): it walks 1400 levels and selects the entry.

Reachability: a tree deeper than ~995 under an applications dir — implausible by accident, possible through a
symlinked directory (both implementations follow symlinks, `find -L` = `os.stat`) or a generated tree. This is
simultaneously a host crash (traceback on a diagnostic run) and a contract divergence: the tool is defined as
"stdout+rc == the script".

Note the counter cannot express this case even if someone wanted to add it: `materialize` in
`quality/counters/c1-r47-terminal.py:198-217` builds paths with `os.makedirs`, which itself raises `RecursionError`
past ~995 (it did, in my harness, before the tool ran).

Smallest remediation: replace the recursion with an explicit stack (`pending = [start]`) and keep the
`(st_dev, st_ino)` ancestor set per branch.

### H4 — non-regular entries in the LAST application dir are candidates for the real script and not for the tool; a planted FIFO hangs the real resolver. Severity: low for C1, real for the host

The script's `find` gets one `-type f` and then one `( -path … ! -path … )` group per application dir (`x:766-776`),
so `-type f` binds only to the **first** group; the last group is `-o`-ed at top level and matches any file type.
`find -type f` therefore does not protect the user's own applications dir (the last one, built by prepending,
`x:168`). Verified with the script's own argv (captured by `strace -s 4000 -e trace=execve`) in three fixtures:

| fixture | real script | tool |
|---|---|---|
| FIFO `pipe.desktop` in `$XDG_DATA_HOME/applications` (**last** dir), no list file (C2) | **rc 124, blocked**; strace ends `openat(…"/applications/./pipe.desktop", O_RDONLY) = ? ERESTARTSYS` | rc 0, selects `good.desktop`, FIFO skipped (S_ISREG at `:519`) |
| FIFO `pipe.desktop` in the `$XDG_DATA_DIRS` dir (**first**) (G2) | rc 0, FIFO never listed | rc 0 |
| directory `x.desktop` in the user dir (G3) | rc 0, lists it and opens it: `line 985: read: 0: read error: Is a directory`, then falls through to `good.desktop` | rc 0, recurses into the directory instead |
| FIFO present but the list file names `good.desktop` first (G4) | rc 0 (the FIFO id is never reached) | rc 0 |

Impact on the host: a FIFO any process can drop in `~/.local/share/applications/` (or a `.desktop`-named symlink to
a FIFO/`/dev/zero`) makes SUPER+RETURN *hang* on this host for as long as it sits there, and makes the cache path
re-run the same walk. Impact on C1: the tool's answer (`selected=… verdict=OK`) is then false — the resolver does
not return at all — and the tool is the declared reference. The declared docstring line 39 ("a file that is not a
regular file is skipped") is true of the *first* group only, so the model's `-type f` is uniform where the script's
is not.

Not reachable through C1 as frozen: `materialize` writes regular files only and the fixture JSON has no way to
express a FIFO, symlink or device (`c1-r47-terminal.py:198-217`), so no fixture can catch it before or after data.
Recorded here as a declared residual, not as a claim-breaker.

Smallest remediation (tool): none needed for safety — the tool is the safe side; for fidelity the docstring must
say that the last application dir is matched without `-type f`, and the walk must admit non-regular paths in that
last dir. For the host: nothing this lane may do (upstream v0.14.3 bug) — worth an erratum row.

### N1 — the C1 "readonly" clause does not trace writes (claim-scope note, no defect found)

Clause r's trace set is `trace=execve,execveat,socket,socketpair,connect` (`quality/counters/c1-r47-terminal.py:82`),
so a tool that wrote files would still pass C1. The property held under my own trace anyway:

```
strace -f -e trace=openat,open,creat,mkdir,mkdirat,unlink,unlinkat,rename,renameat,renameat2,symlink,symlinkat,ftruncate,truncate
  → creating-syscall lines: 0     (fixture run and real-host run)
strace -f -e trace=write,pwrite64,writev,pwritev,ftruncate,truncate
  → writes to fd > 2: 0           (real-host run; one write, to fd 1)
strace -f -e trace=socket        → 0
```

and the host cache file is untouched in size and mtime by both `explain` and `explain --observed`.

## Cases that are safe (receipts: `r01-cases.tsv`, `r02-scale.txt`, `r04-observed-classes.txt` in the seat dir)

| case | result |
|---|---|
| clean tree (C0/P1) | rc 0, `selected=good.desktop … verdict=OK`, tool 0.03 s vs real 0.01 s |
| FIFO as a **list file** (C1) | skipped, rc 0; real script `[ -f ]` also skips (rc 0, verified) — no block on either side |
| `/dev/zero` as a list file (C11) | skipped (isfile false), rc 0 |
| `/dev/zero` as an entry, first position (C12) | skipped, rc 0 (in the last dir the real script would block — see H4) |
| UNIX socket as an entry (C17) | skipped, rc 0 |
| symlink `loop -> .` in the applications dir (C5) | walked once, rc 0 (ancestor `(st_dev, st_ino)` set at `:495-508`) |
| two dirs symlinked to each other (D6) | rc 0 |
| `.desktop` symlink loop `a->b->a` (D5) | skipped by `os.stat` ELOOP, rc 0 |
| symlink out to `/usr/share/doc` (24 244 files) (C6/P5) | rc 0, whole walk 0.21 s / 16 MB vs real 0.02 s — bounded |
| `XDG_CONFIG_HOME=XDG_DATA_HOME=XDG_DATA_DIRS=XDG_CONFIG_DIRS=XDG_CACHE_HOME=/proc/self` (C9) | rc 3 `NO_TERMINAL`, no crash, no hang |
| list file symlinked to `/proc/self/mem` (C10) | modelled errexit path, rc 3, trace "unreadable" |
| list file mode 000 (C13a) | rc 3, trace "unreadable"; real script: `line 361: Permission denied`, rc 1 (tool models the resolver's 1 as explain's 3, as documented) |
| entry mode 000 (C13b) | rejected "unreadable", next candidate selected → rc 3 with no other entry, no traceback |
| applications dir mode 000 (C13c) | not walked, rc 3 — **silent** (no trace line says the dir was unreadable; cosmetic) |
| glob char in `XDG_DATA_HOME` (C14) | `MADO_TERM_OUT_OF_CONTRACT`, rc 2 |
| `--observed` a directory (C15) | `cannot read …: Is a directory`, rc 2 |
| `--observed /proc/self/mem` (E2) | `Input/output error`, rc 2 |
| `HOME` unset (D2) | `MADO_TERM_OUT_OF_CONTRACT: HOME unset`, rc 2 |
| `HOME=""` (D1) | falls through to `/usr/share` defaults, rc 0 — same as the script |
| extra argv (D3) | usage, rc 2 |

## Real host, measured

```
tool.py explain                    rc=0 wall=0.02s maxrss_kb=15892 stdout=506B stderr=0B
tool.py explain --observed capture rc=0 wall=0.03s maxrss_kb=16164
MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop cmd=alacritty cache=present verdict=AGREE
real (cold scratch XDG_CACHE_HOME, --print-id --print-path --print-cmd)  rc=0, 84 B, identical id/path/cmd
opens: 111 traced lines, 109 unique paths, exactly ONE .desktop opened (the selected entry); the rest are python
libs + the two list files. creating opens 0, sockets 0, execve 0, writes to fd>2 0.
host cache file: mtime 1793047345 / size 190 before and after.
```

## Receipts (`.ufo/waves/round-47/w2/SentC1Host/`)

| file | content |
|---|---|
| `r01-cases.tsv` | every hostile case of the first sweep: name, exit status, stdout/stderr tails |
| `r02-scale.txt` | P1/P2/P3 and P8 wall + per-run peak RSS, tool vs real script |
| `r03-deep.txt` | 990 / 1000 / 1400-deep trees, tool vs real |
| `r04-observed-classes.txt` | FIFO / symlink-FIFO / `/dev/full` / `/dev/zero` / `/proc/self/mem` / directory as `--observed` |
| `r04-strace-fifo.txt` | the blocked `openat` |
| `r05-strace-fixture.txt`, `r05-strace-writes-host.txt` | creating-open trace, fixture and real host |
| `r06-host-explain.txt`, `r06-host-capture.txt` | the real-host trace and the cold-cache capture it agrees with |
| `r07-h4-find.txt` | the last-app-dir divergence: real hang, `find` argv, controls G2/G3/G4 |
| `r08-hashes.txt` | sha256 of tool and real script, kernel, python |
| `r09-fixture-space.txt` | the frozen fixture space limits |
| `harness/` | `run.sh`, `run3.py`, `meas.py` — the drivers used |

Every number above is reproduced by those drivers under `/fast/scratch/hyaku/mado-r47/SentC1Host` (that scratch
tree is deleted after the receipts were copied; a re-run rebuilds it). No package was installed (tool installs: none).

## Residuals and what I did not run

- `/dev/zero` named `*.desktop` in the *last* application dir (the H4 class with a character device) was **not run
  against the real script**: bash `read` would allocate without bound for the whole timeout. It is the same code
  path as the FIFO block, which is measured.
- The 2 M-line list file makes the real script take >180 s (its per-id `alias`/`eval` loop); the tool takes 4 s.
  That is a real-script cost, not a tool defect, and both are pathological on that input.
- Fixture space of the frozen C1: `fixtures=190 classes=29 max_path_depth=6 max_file_bytes=10021
  symlink_or_fifo_cases=0` — H2/H3/H4 are structurally outside it, so no C1 verdict, before or after data, can
  move because of them. H1 is outside the counter entirely (`--observed` is not exercised by any fixture).
- Tool installs: none. No package transaction was run.
