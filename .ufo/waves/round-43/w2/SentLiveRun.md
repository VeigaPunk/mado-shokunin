# SentLiveRun — security/safety of the installed tool's real host use (round 43, w2)

STATUS: **complete**. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, data commit
`1959770657f1f8665097c1aed4be6c1cbb07139f` (base `a35cfdf`). Host 2026-10-26, Hyprland 0.56.2,
Python 3.14.8, strace 7.2 (preinstalled; nothing installed). Target of the attack:
`tools/mado-geometry.py:14` — "It reads files and standard input only; it starts no process and
opens no socket." — and the PROVINCE restatement of it, `PROVINCE.md:32`. Evidence:
`.ufo/waves/round-43/w2/SentLiveRun/` (`findings.md` has the trace excerpts; `verify.sh` re-checks
every quote and number and currently prints `VERIFY: PASS`).

## Verdict

The claim **holds for the tool's own syscalls in every scenario run**: one `execve`
(`/usr/bin/python3`), zero `clone`/`fork`/`vfork`, zero socket/connect syscalls, zero
open-for-write/create/truncate, zero mutating-fs syscalls, and the only `write(2)` is the tool's own
`write(1)` of its output. The live host receipt reproduces exactly. One **landed-data defect**
(low) and one **tool defect** (low-medium, w1 V5 confirmed and broadened) are reported; three
bounded caveats are informational. Nothing here falsifies the C1 capability or the C2 predicate.

| id | severity | attacks / supports | one line |
|---|---|---|---|
| F1 | — supports | docstring claim `tools/mado-geometry.py:14` | strace of 4 scenarios + 2 fd-level passes: no process, no socket, no write-open |
| F2 | — supports | `receipts/live-geometry-host.txt` | same 3 lines, `NO_MATCHING_CLIENT`, rc 3 at 2026-10-26T05:33:44-03:00; sha of tool and rules file match the receipt |
| F3 | low (defect) | landed data `PROVINCE.md:32` | "`--selftest` opens no file" is false: it opens `/nonexistent/none`, `/`, `/dev/null` (all rejected) |
| F4 | low-medium (defect) | tool `tools/mado-geometry.py:410`, w1 `RevRefTool` V5 | closed fd 0 crashes **every** mode, including `--selftest`; w1 recorded only `--clients -` |
| F5 | low (caveat) | docstring usage `:10`, `SKILL.md:225` | the documented command omits `-I`; a shadow `json.py` beside the script then executes (measured) |
| F6 | info | interpreter trust root | even `-I` executes system `site-packages` `.pth` code (`_distutils_hack`) |
| F7 | low (caveat) | `read_regular` `tools/mado-geometry.py:90-104` | non-regular paths are opened before the mode check (`/dev/ptmx` open succeeded); no `O_NOCTTY`/`O_NOFOLLOW` |
| F8 | — note | w1 `SentReDoS` SR-1 / `RevRefTool` V1 | ReDoS still holds (0.005 s → 1.560 s for n=24→36); already declared at `SKILL.md:290-295` (w1 commit `2a3707c`), not re-reported |

## What was run (all read-only; scratch copy of the tool from the data commit)

Under `strace -f -e trace=process,network,file`, with the tool blob `e3c2e471…` extracted by
`git show 1959770:tools/mado-geometry.py`:

1. `python3 -I tool --selftest` → `73/73 passed`, exit 0.
2. `hyprctl clients -j | python3 -I tool --clients - --rules ~/.config/hypr/gkeep.conf` → the
   receipt's three lines, exit 3.
3. FIFO as `--clients` and as `--rules` (no writer, 10 s cap) → `SETUP unreadable`, exit 2, in
   milliseconds (`O_NONBLOCK` on the open), no read on the FIFO.
4. fd 0 closed (`bash -c 'exec 0<&-; exec python3 -I tool --clients - …'`, and separately
   `--selftest`, `--clients /dev/stdin`) → traceback (F4), zero syscalls beyond reads.
5. Extras: `/dev/ptmx` as `--rules` (F7), `/dev/null` and `/` through the selftest, a
   `write`+`openat` pass, `-I` vs no-`-I` import-isolation demo (F5), one ReDoS re-measure (F8).

## F1 — supports: starts no process, opens no socket, writes no file

`summary.txt` (per-trace counts over the tool process only):

```
trace                      execve clone/fork  network write-open  mutating-fs nonblock-opens
tr-selftest.log                 1          0        0          0            0         10
tr-hostpipe.log                 1          0        0          0            0          8
tr-fifo-clients.log             1          0        0          0            0          8
tr-fifo-rules.log               1          0        0          0            0          9
tr-stdin-closed3.log            1          0        0          0            0          7
tr-ptmx.log                     1          0        0          0            0          9
```

Key excerpts (verbatim in the seat logs):

```
486701 execve("/usr/bin/python3", ["python3", "-I", "/fast/scratch/hyaku/mado-r43/SentLiveRun/mado-geometry.py", "--clients", "-", "--rules", "/home/vgpnk/.config/hypr/gkeep.conf"], 0x7ffe9f5c2d88 /* 267 vars */) = 0
openat(AT_FDCWD, "/home/vgpnk/.config/hypr/gkeep.conf", O_RDONLY|O_NONBLOCK|O_CLOEXEC) = 3
928282 write(1, "MADO_GEOMETRY_SELFTEST: 73/73 passed\n", 37) = 37
openat(AT_FDCWD, "/fast/scratch/hyaku/mado-r43/SentLiveRun/fifo-test", O_RDONLY|O_NONBLOCK|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFIFO|0644, st_size=0, ...}) = 0
```

`--rules`/`--clients` are opened `O_RDONLY|O_NONBLOCK|O_CLOEXEC`, `fstat`ed regular, read once and
closed. The `O_RDONLY|O_NONBLOCK` flags are the tool's; importlib's own `O_DIRECTORY` opens carry
the same flags and are separated in `summary.txt`.

## F2 — supports: the live receipt reproduces now

`live-repro.txt`, seat run `2026-10-26T08:33:44Z / 05:33:44-03:00`:

```
MADO_GEOM_RULE: n=1 file=1 effect=float arg=on class=^(org.omarchy.gkeep)$
MADO_GEOM_RULE: n=2 file=1 effect=size arg=420x500 class=^(org.omarchy.gkeep)$
MADO_GEOMETRY: rules=1 float_rules=1 other=1 unsupported=0 clients=4 matched=0 unmapped=0 agree=0 differ=0 tiled=0 badsize=0 verdict=NO_MATCHING_CLIENT
exit=3
```

`diff` against the committed receipt's four lines: identical. Tool sha `e3c2e471…` and
`~/.config/hypr/gkeep.conf` sha `3726e488…` equal the receipt's and the S295 pin; the live client
set is byte-equal (reduced projection) to the w1 dump (4 tiled clients, same addresses, no gkeep
window); the pinned reduced dump `fetch/host-clients-r43.json` and the w1 full dump both replay to
the same three lines and rc 3, so the receipt is a deterministic function of its inputs.

## F3 — defect (landed data, low): `PROVINCE.md:32` "`--selftest` opens no file"

The selftest's own rejection cases call `read_regular("/nonexistent/none")`, `read_regular("/")` and
`read_regular("/dev/null")` (`tools/mado-geometry.py:353-358`). Trace:

```
openat(AT_FDCWD, "/nonexistent/none", O_RDONLY|O_NONBLOCK|O_CLOEXEC) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/", O_RDONLY|O_NONBLOCK|O_CLOEXEC) = 3
openat(AT_FDCWD, "/dev/null", O_RDONLY|O_NONBLOCK|O_CLOEXEC) = 3
```

None is read. The row's cited `grep` (`mkfifo|O_WRONLY|O_CREAT`) proves "writes nothing", not "opens
no file". Smallest remediation: reword to "opens no caller-supplied file (only the three rejection
paths) and writes nothing"; tool bytes unchanged. This is a prose [OBS] overstatement, the exact
class the province is meant to prevent.

## F4 — defect (tool, low-medium; w1 `RevRefTool` V5 still holds, broadened)

`main()` reads `sys.stdin.buffer` before dispatch (`tools/mado-geometry.py:410`), so with fd 0
closed at exec every mode raises `AttributeError: 'NoneType' object has no attribute 'buffer'`,
exit 1, no SETUP line — including `--selftest`, which needs no stdin, and `--clients /dev/stdin`.
Contract says stdout is one `MADO_GEOMETRY: SETUP <reason>` line and exit 2. Remediation: pass
`None` when `sys.stdin is None` and map a `None`/`OSError` stdin read in `clients == "-"` to
`Setup("unreadable")`. The C1 counter always supplies stdin with `-I` (`c1-r42-geometry.py:205,435`),
so 37/37 does not cover this.

## F5 — caveat (invocation, low): the documented command is not import-isolated

Counter and receipt use `python3 -I`; `SKILL.md:225` (also `:158`, `:248`, `:251`, `:281`, `:294`)
and the docstring usage (`tools/mado-geometry.py:10`) do not. Measured with a copy of the tool beside
a `json.py` that writes a marker file: with `-I`, selftest `73/73`, shadow module never imported;
without `-I`, `SHADOW_JSON_EXECUTED` on stderr, marker written, exit 1. So "writes nothing / starts
no process" is a property of the isolated invocation; a module shadowing a stdlib import in
`tools/` would run with the operator's privileges. Requires write access to `tools/`. Remediation:
add `-I` to the SKILL rows and the docstring usage.

## F6 — note: `-I` still executes system site-packages code

`tr-hostpipe.log:78-100`: `/usr/lib/python3.14/site-packages/distutils-precedence.pth` is read and
`_distutils_hack/__init__.py` imported before the tool runs. That code does no process/socket/write
here, so the claim stands; the trust root is "tool + stdlib + root-owned system site-packages", not
"tool + stdlib". No action proposed.

## F7 — note: non-regular paths are opened before the mode check

`--rules /dev/ptmx`: `openat(..., "/dev/ptmx", O_RDONLY|O_NONBLOCK|O_CLOEXEC) = 3`,
`fstat(3, {st_mode=S_IFCHR|0666, st_rdev=makedev(0x5, 0x2), ...}) = 0`, `close(3)`, `SETUP
unreadable`. No read follows. The open uses neither `O_NOCTTY` nor `O_NOFOLLOW`, and a device whose
open has side effects is touched; `/dev/watchdog` is the named class (arming on open — kernel
semantics, **not tested** here). Operator-supplied path, so severity low. Remediation: classify by
`lstat` before opening (or `O_PATH`), then re-check `st_dev/st_ino` after, and add
`O_NOCTTY|O_NOFOLLOW`.

## F8 — w1 ReDoS still holds (declared; not re-reported)

`redos-remeasure.txt` (regex `(a|aa)+$`, failing class `"a"*n+"b"`): n=24 `0.005 s`, n=28 `0.034 s`,
n=32 `0.220 s`, n=36 `1.560 s`. Exponential, matching `w1/SentReDoS` SR-1 and `w1/RevRefTool` V1;
the w1 commit `2a3707c` added the SKILL note (`SKILL.md:290-295`). Availability only; it attacks
none of the three verbs.

## Limits

- Absence is established for the scenarios and inputs traced, not for every fixture branch.
- The C1 counter's bubblewrap/`RLIMIT_NPROC` sandbox was not entered and 37/37 was not re-run.
- `read(2)`/`write(2)` are outside `trace=process,network,file`; they were measured by a separate
  `write,openat,ftruncate` pass and an `openat,fstat,read,close` pass.
- TTY stdin was not tested (no tty available to a leaf; w1 V-residual).

## Verification, tooling, cleanup

- `bash .ufo/waves/round-43/w2/SentLiveRun/verify.sh` → `VERIFY: PASS` (every quote/number in this
  report and in `findings.md` is grepped from this seat's receipts or from the lane's commits;
  the seat copy is checked to be the data-commit blob and the tool sha `e3c2e471…`).
- Nothing installed; no `pacman`; no fetch; compositor contact limited to `hyprctl version` and
  `hyprctl clients -j`.
- Scratch `/fast/scratch/hyaku/mado-r43/SentLiveRun/` removed after its cited files were copied into
  this seat directory. No lane file other than `.ufo/waves/round-43/w2/SentLiveRun*` was written;
  no git/jj write.
