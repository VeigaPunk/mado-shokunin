# SentHost — host safety of the round-49 probes, counters and controls

> Seat report (leaf). This file is the seat's `Report:` deliverable; it mirrors `w1/SentHost/report.md`
> (same body below this block). Receipts: `w1/SentHost/receipts/` (11 files); locator check:
> `w1/SentHost/verify-quotes.py` (`checked=74 bad=0`); probe driver: `w1/SentHost/probe.sh`.


Seat `SentHost` (sentinel, leaf). Round 49, wave `w1` = BUILD, policy v1. Base `03e4ae76aff7a4be59cb69970dd553baa319695a`.
Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`. This seat wrote no tracked file and no file outside
`.ufo/waves/round-49/w1/SentHost/`.

**Axes** (what every finding is scored against):

| axis | question |
|---|---|
| **A1 mutation** | can anything this round runs write host state (home, `/etc`, `/usr`, compositor)? |
| **A2 read leak** | which host paths does a probe read that the contract did not name? |
| **A3 determinism** | is the result a function of pinned inputs only, or of ambient host state? |
| **A4 tripwire fidelity** | does each guard stop the exploit it claims (no false negative) without tripping on a legitimate run (no false positive, cf. round-48 `M48-12`)? |

**Method.** Everything below is a traced, executed probe: `strace -f -e trace=%file[,%process|,%network]` around the
pinned binaries with `HOME`/`XDG_*` inside scratch, plus a `bubblewrap 0.13.1` sandbox whose bind set is the one proposed
for the counters. No counter exists yet this wave (ExecCounterC1/ExecCounterC2 are drafting), so this reviews the *surface*
they will run on. Receipts regenerate with `probe.sh` (`S=<scratch> OUT=<seat>/receipts`); every quotation below carries the
receipt and a `grep`-computed line number.

Pins used (`receipts/r10-pins.txt`):

```
43b924f6…77250  /usr/lib/xkbcommon/xkbcli-compile-keymap
f6c0b122…27e54  /usr/lib/xkbcommon/xkbcli-how-to-type
13023369…a463f3 /usr/include/xkbcommon/xkbcommon-keysyms.h
af42b0e6…1bd1f   /usr/bin/xkbcli
216626…f8c66    /usr/bin/hyprctl
```

Verdict up front: **the pinned binaries are clean** — no write syscall in any allowed invocation (`r1-compile-fs.txt:10`,
`:14-16` for `--test`, `--layout us`, `--options compose:caps`; `r4-howtotype-fs.txt:13,14`; `r11-tool-run.txt:13` for
`xkbcli list`; `r7-hyprctl.txt:2-13` = `writes=0` for all four read verbs), no home read once the contract's flags are given
(`--keymap`, `--disable-compose`), and `hyprctl`'s read verbs touch nothing under `$HOME` (`home-path hits: 0`). **The host risk is entirely in the
three places the draft recipe is underspecified**: the compile's *default include path* (H2/H3), the judge's *mode*
(H1/H4), and the *sandbox bind/tool-run mechanics* (H6/H7). Two of those can produce a passing verdict with a broken
instrument (H4 is the worst: zero rows on both sides), which is the failure class worth freezing against.

---

## H1 — `--disable-compose` is a home-read guard, not a stylistic flag (High, A2)

`quality/…` nothing yet enforces it beyond the argv; the contract names it only as an output-shape rule.

Evidence — `how-to-type --keymap=FILE`, compose ON vs OFF, `%file` trace (`receipts/r4-howtotype-fs.txt`):

```
:6  openat(AT_FDCWD, "<scratch>/home/.config/XCompose", O_RDONLY) = 4
:8  openat(AT_FDCWD, "/usr/share/X11/locale/en_US.UTF-8/Compose", O_RDONLY) = 5
:9  ## non-loader paths read WITH --disable-compose:
:10 execve(… "--keymap=br.xkb", "--disable-compose", "--keysym", "slash" …)
:13 t-ht-compose.txt:0        (write-opens, compose ON)
:14 t-ht-nocompose.txt:0      (write-opens, compose OFF)
:18 > === Access via Compose sequences ===
```

Compose ON reads, in order, `$XCOMPOSEFILE` (`r4-howtotype-fs.txt:21-22`), `$XDG_CONFIG_HOME/XCompose` or
`$HOME/.config/XCompose`, then **`$HOME/.XCompose`** (`:23-25`, probed when the XDG copy is absent), then
`/usr/share/X11/locale/{locale.alias,compose.dir,<locale>/Compose}`. With `--disable-compose` the only file opened is the
keymap itself (`:9-11`).

Exploit path (no privilege): the operator's real `~/.XCompose` exists on this host (240 B, digest in
`receipts/r9-operator-state.txt:2`). A counter that invokes the judge — or the tool — without `--disable-compose` (a) reads
that operator file on every case, (b) gets four extra stdout lines (`r4-howtotype-fs.txt:18`), so a tool that is correct
under the contract fails, and (c) makes the verdict depend on a file outside the lane.

Impact: A2 leak + A3 — one missing flag turns a pinned oracle into an ambient-state oracle.
Smallest remediation: pass `--disable-compose` on **both** sides and assert the invariant on the judge's stdout: no line
`=== Access via Compose sequences ===` and no `#  KEYSYM` column header.

## H2 — the compile's default include path searches user-writable directories first (High, A3)

`strace` of the pinned `compile-keymap` in the draft's "clean env"
(`HOME`/`XDG_CONFIG_HOME` in scratch, `receipts/r1-compile-fs.txt:5-7`):

```
newfstatat(… "<scratch>/home/.config/xkb", …) = -1 ENOENT
newfstatat(… "<scratch>/home/.xkb",        …) = -1 ENOENT
newfstatat(… "/etc/xkb",                   …) = -1 ENOENT
```

i.e. libxkbcommon appends `$XDG_CONFIG_HOME/xkb`, `$HOME/.xkb`, `/etc/xkb` **ahead of** `/usr/share/xkeyboard-config-2`
(later `strace` shows `-2.d`, `.d`, then `-2`). The "clean env with HOME in scratch" recipe in the claim therefore only
holds while the scratch home stays *empty*: the counter reuses one work dir, and the same process under test may write it.

Exploit path, executed (`receipts/r3-workdir-planting.txt:2-5`) — plants `$XDG_CONFIG_HOME/xkb/symbols/br` **inside the
counter's own work dir between two compiles of the same fixture**:

```
:2 before  default-include  6ef2127653b0…7a0  -
:3 after   default-include  5021473cee49…a0   evil=1
:4 before  --include        6ef2127653b0…7a0  -
:5 after   --include        6ef2127653b0…7a0  evil=0
```

Same command, same env, different keymap — silently. And `XKB_CONFIG_EXTRA_PATH` does the same from the environment
(`r2-include-matrix.txt:7`: `6637586f…` with `evil=1`), so `env -i` is load-bearing too.

Impact: A3 + A4 — a control that writes into the work dir (ExecControlsC1 builds exactly such controls) changes the
fixture both sides are judged on; the counter cannot tell a rewritten fixture from a correct one.
Smallest remediation: H3.

## H3 — `--include=<root>` is the isolating compile form, and it is byte-free to adopt (High, A3)

Isolation matrix, all `--layout br` (`receipts/r2-include-matrix.txt:2-8`):

| row | invocation | keymap sha256 | hostile symbols visible |
|---|---|---|---|
| clean | default include path, pristine scratch home | `6ef2127653b0…` | 0 |
| hostile | default, scratch home holding `xkb/symbols/br` | `4f07b6d5b70a…` | **1** |
| inc-clean | `--include=/usr/share/xkeyboard-config-2` | `6ef2127653b0…` | 0 |
| inc-hostile | `--include=…`, hostile home | `6ef2127653b0…` | 0 |
| root | `XKB_CONFIG_ROOT=<fake>` | *(compile fails)* | 0 |
| extra | `XKB_CONFIG_EXTRA_PATH=<fake>` | `6637586fc663…` | **1** |
| extra-inc | `--include=…`, `XKB_CONFIG_EXTRA_PATH=<fake>` | `6ef2127653b0…` | 0 |

`--include` replaces the default list (`--help`: "If an include path is given, the default include path list is not used"),
so it removes the user-dir, `/etc/xkb` and `XKB_CONFIG_*` classes at once, and it produces **the same bytes** as the
pristine default compile (`:2` == `:4`). The `root` row also proves the env lever is real: `XKB_CONFIG_ROOT` replaced the
search list and the compile died (`r2-include-matrix.txt:11-16`, `1 include paths searched: …/fake-xkb`,
`1 include paths could not be added: /etc/xkb`).

Impact: adopting it costs nothing and closes H2 completely; not adopting it leaves the fixture writable by the process
under test.
Smallest remediation (both-ways, so the isolation cannot itself narrow the fixture): compile each fixture **twice** —

```
# guarded (the one the tool and judge get)
env -i PATH=/usr/bin /usr/lib/xkbcommon/xkbcli-compile-keymap \
    --include=/usr/share/xkeyboard-config-2 --layout L --variant V --options O > "$k.xkb"
# reference (default search path, pristine empty scratch home)
env -i PATH=/usr/bin HOME="$W/refhome" XDG_CONFIG_HOME="$W/refhome/.config" \
    /usr/lib/xkbcommon/xkbcli-compile-keymap --layout L --variant V --options O | cmp -s - "$k.xkb"
```
and require equality (`Setup` error otherwise). Pin the resulting fixture digests: a keymap whose digest moved is a host
change, not a scoring event.

## H4 — a judge run without `--keymap` reads the host tree and can produce a vacuous verdict (Medium-High, A3/A4)

`hyprctl`-style RMLVO mode (`--rules evdev --layout br`, no `--keymap`) opens 40 files under
`/usr/share/xkeyboard-config-2` (`receipts/r5-judge-contract.txt:11`) and, under a hostile `$XDG_CONFIG_HOME/xkb`,
**collapses from 5 rows to 0** (`:12` `clean rows=5 hostile-rows=0`). With `--keymap`, `XKB_CONFIG_ROOT` sabotage has no
effect at all (`:8-9` "identical to the clean-env run"), because the only file opened is the keymap
(`r4-howtotype-fs.txt:9-11`).

Exploit path: a counter builds the judge argv from a case struct; one case type (or one refactor) drops `--keymap`. The
judge then re-derives a keymap from ambient state. Two outcomes, both bad: 0 rows vs the tool's 5 → false `TARGET_MISSED`
for a correct tool; or, if the tool is also fed the RMLVO-derived host keymap, **both sides print the same empty table and
the case passes having verified nothing**.

Impact: a wrong instrument reported as a pass — the class the round-48 lesson calls fabricated readiness.
Smallest remediation: build the judge argv in one place and assert on the built list before running:
`--keymap` present, and none of `--rules --model --layout --variant --options --enable-environment-names`. Reject a case
whose expected stdout has zero data rows (a 0-row judge is a `Setup` error, never a pass).

## H5 — the compile depends on host package state that nothing pins (Medium, A3)

`/etc/xkb`, `/usr/share/xkeyboard-config-2.d`, `/usr/share/xkeyboard-config.d` are stat'ed on every compile
(`r1-compile-fs.txt:5-7`, `r2-include-matrix.txt:11-16`). All three are absent today (`receipts/r9-operator-state.txt:6`, `:8`, `:9`), so today's answer equals `xkeyboard-config 2.48-1` — but nothing in the lane records that, and a future
package install (pacman is paused, not forbidden forever) would change every fixture silently while both sides still agree.

Smallest remediation: (a) the guarded compile from H3, which never consults them; (b) a one-line tripwire in the counter's
`meta` clause: `absent ?/etc/xkb ?/usr/share/xkeyboard-config-2.d`; (c) pin the two files the fixtures actually consume —
`symbols/br` `8cf65550…`, `rules/evdev` `0cc48ee1…` (`r9-operator-state.txt:10`, `:11`) — plus the package version string read
from `/var/lib/pacman/local/xkeyboard-config-2.48-1/desc` (`r9-operator-state.txt:13`, no pacman transaction).

## H6 — the sandbox works, but two mechanics break a naive implementation (Medium, A4)

Verified binding set for the **judge** (`receipts/r6-bwrap.txt:1-12`, rc=0, output identical to the host run):

```
bwrap --unshare-user --unshare-pid --unshare-ipc --unshare-uts --unshare-net \
      --die-with-parent --new-session --clearenv \
      --ro-bind /usr/lib/xkbcommon/xkbcli-how-to-type /judge \
      --ro-bind /usr/lib/libxkbcommon.so.0 /usr/lib/libxkbcommon.so.0 \
      --ro-bind /usr/lib/libc.so.6 /usr/lib/libc.so.6 \
      --ro-bind /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2 \
      --ro-bind /etc/ld.so.cache /etc/ld.so.cache \
      --bind <keymap> /k.xkb --dev /dev --proc /proc --tmpfs /tmp \
      /judge --keymap=/k.xkb --disable-compose --keysym "$ARG"
```

Two traps, both executed:

1. **Loader path.** The ELF declares `/lib64/ld-linux-x86-64.so.2` (`r6-bwrap.txt:16`) and on this host `/lib` is a symlink
   to `usr/lib` while `/lib64` is a real directory. Binding the loader at `/usr/lib/ld-linux-x86-64.so.2` makes `execvp`
   fail (`bwrap: execvp /judge: No such file or directory`, `r6-bwrap.txt:18`) — which a counter would read as a tool
   failure, i.e. a false `TARGET_MISSED`.
2. **`--clearenv` is load-bearing.** Without it bwrap passes the ambient environment through — measured, variable names only
   (`r6-bwrap.txt:35-36`): `without --clearenv: 269 vars; sample: HYPRLAND_CMD HYPRLAND_INSTANCE_SIGNATURE WINDOWID
   XDG_CONFIG_DIRS` vs `with --clearenv: 1 vars`. `XDG_CONFIG_DIRS` + a bound `/etc` would re-open the compose path H1
   closes; `XKB_CONFIG_ROOT`/`XKB_CONFIG_EXTRA_PATH` would re-open H2 for any non-`--include` compile; and the compositor
   signature would be handed to the process under test.

Visibility inside the proven set: no `/home`, no `/root`, no `/run/user`, no `/etc/xkb`, no `/sys/class/net`
(`r6-bwrap.txt:27-31`), and the rw canary is byte-identical afterwards (`r6-bwrap.txt:33`).

## H7 — Python tool-run mechanics: `-I` kills sibling imports, and bytecode is a write (Medium, A1/A4)

Executed (`receipts/r11-tool-run.txt`):

```
:2 python: Python 3.14.8
:4 ModuleNotFoundError: No module named 'helper'          # python3 -I main.py, helper.py beside it
:7   ./__pycache__/helper.cpython-314.pyc                 # the same import without -I
:9   pyc files after -I (with the env var set) + -B: 0
```

- `-I` (isolated) removes the script's directory from `sys.path` on 3.14, so **the C1 tool must be a single file** — no
  `import keysym_table` next to it. This constrains ExecRefKeysymA/ExecGen's design now, not at freeze time: the keysym
  table has to be embedded in the tool (or read as *data*, see H8/H9).
- `-I` implies `-E`, so `PYTHONDONTWRITEBYTECODE=1` in the environment is **inert**; `-B` must be a command-line flag. A
  tool that imports a helper without `-B` writes `<dir>/__pycache__/*.pyc` — inside the sandbox that is either a false
  write trip on a correct tool or a real host write if the tool's dir is bound rw.
- `python3 -I -B` is the right invocation: it also fixes the "tool reads a cached answer table" control class to a
  deterministic failure.

Impact: A4 (false trips) and A1 (a write channel nobody named).
Smallest remediation: run the tool as `python3 -I -B /oracle/tool.py`, bind `/oracle` read-only, and state
"single-file, stdlib only, no sibling module" in the contract text.

## H8 — `hyprctl` read verbs are write-free and home-free, but two receipt hazards are real (Low-Medium, A1/A2)

`%file` trace of all four allowed verbs (`receipts/r7-hyprctl.txt:2-13`): `writes=0`, `home-path hits: 0` for each; the only
path roots touched are `/usr/lib`, `/usr/bin`, `/etc/ld.so.cache`, `/etc/ld.so.preload`. The only network syscall is one
`connect` to the compositor socket, redacted here (`r7-hyprctl.txt:21`):

```
connect(3, {sa_family=AF_UNIX, sun_path="/run/user/<uid>/hypr/<sig>/.socket.sock"}, 96) = 0
```

Two hazards: (a) without `HYPRLAND_INSTANCE_SIGNATURE` in the environment the verb exits 1 with
`HYPRLAND_INSTANCE_SIGNATURE not set!` (`r7-hyprctl.txt:23-24`), so a counter must pass it explicitly rather than inherit
it; (b) `hyprctl devices -j` returns 4.5 kB of **input-device names** — session material that must never be committed, and
the instance signature embedded in the socket path is a live per-session value.

Smallest remediation: the C2 counter, if it re-runs the live receipt, records only shape — `binds=192` and the field list
(`r7-hyprctl.txt:15`), the `getoption` object verbatim (`{"option": …, "int": 0, "set": false }`, `:17`) — and redacts any
`/run/user/<uid>/hypr/<sig>` substring it echoes. Never bind `$XDG_RUNTIME_DIR` into a sandbox that does not need the
compositor.

## H9 — the claim carries an unreproducible number (Low, but freeze-relevant)

The claim text (and the task text) states the keysym header has **2659 `#define XKB_KEY_` lines**. Measured on the pinned
header (`receipts/r8-header.txt:4-6`):

```
sha256 13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3
lines: 3545  bytes: 264502
#define XKB_KEY_ lines: 2638
occurrences of XKB_KEY_: 2792
lines containing XKB_KEY_: 2783
```

2638, 2783 and 2792 are all reproducible; 2659 is none of them. This is the `M48-11` class (a carried number that no
instrument emits) landing on the very sentence that will freeze the C1 data-source rule.

Smallest remediation: replace 2659 with `2638` and the command that emits it (`grep -c '^#define XKB_KEY_' FILE`), or let
the counter print it in `meta`.

## H10 — `M48-10`'s root cause is still the shape of this round's mutants (Medium, A1)

Round 48's incident was `mkmutants.py:31` deriving its write target from the ambient `HOME`. This round's mutant seats
(`MutCounterC1Draft`, `ExecControlsC1`'s "a tool that writes a file" control, `ExecMutantSandbox`) reproduce the same shape:
the target is whatever the harness names. H2 shows that redirecting `HOME` alone is **not** containment, because the process
under test can write *inside* the redirected home and change its own fixture.

Smallest remediation: the guard is an allowlist, not a redirect — every mutant's write target is resolved with
`os.path.realpath` and must satisfy `under(target, work)`, where `work` is the counter's `--work` (already `realpath`-gated
and already required to be outside `/tmp`, cf. `w2/SentScratch` F1/F2). Redirecting `HOME`/`XDG_*` into `work` is the second
layer, and the before/after digest (G5) is the third.

---

## Guard specification (what the counters and seat prompts should carry)

### G1 — compile (fixture keymaps)

```
env -i PATH=/usr/bin \
  /usr/lib/xkbcommon/xkbcli-compile-keymap \
    --include=/usr/share/xkeyboard-config-2 \
    --rules evdev --model "$MODEL" --layout "$LAYOUT" --variant "$VARIANT" --options "$OPTIONS"
```
- `--include=` replaces the default path list (H3); never add `--include-defaults`, never set `XKB_CONFIG_ROOT`,
  `XKB_CONFIG_EXTRA_PATH`, `XKB_DEFAULT_*`.
- `env -i` is mandatory even with `--include`: it also clears `XKB_LOG_LEVEL`/`XKB_LOG_VERBOSITY` (stderr noise a counter
  might mistake for a tool failure) and `XCOMPOSEFILE`.
- Both-ways check: also compile with the default path in a pristine scratch home and `cmp` (H3). Equal digests, or `Setup`.
- Create the scratch home fresh per run (`mktemp -d -p "$WORK"`), never reuse one across cases.
- Pin the fixture digests; a moved digest is a host change → `Setup` error, not a scoring event (H5).

### G2 — judge (the oracle)

```
env -i PATH=/usr/bin /usr/lib/xkbcommon/xkbcli-how-to-type \
  --keymap="$k.xkb" --disable-compose --keysym "$ARG"
```
- Assert on the built argv: `--keymap` present; none of `--rules --model --layout --variant --options
  --enable-environment-names` (H4).
- Assert on the judge's stdout: no `=== Access via Compose sequences ===` (H1); at least one data row, else `Setup` (H4).
- `--keymap` also makes `XKB_CONFIG_ROOT` provably inert (`r5-judge-contract.txt:8-9`), which is why the two flags together
  are the whole isolation story for the oracle.

### G3 — bwrap, judge run

As H6, plus: `--clearenv`, then `--setenv` only `PATH=/usr/bin`. No `/home`, no `/run/user`, no `/etc` beyond
`ld.so.cache`, no `/usr/include`, no `/usr/share`. `--unshare-all` (net included). `--die-with-parent --new-session`.

### G4 — bwrap + tripwire, tool run

Judge set, plus:

```
--ro-bind "$PYTHON" /usr/bin/python3        # PYTHON = os.path.realpath(sys.executable)
--ro-bind "$TOOL"   /oracle/tool.py         # read-only: a tool cannot rewrite itself
--ro-bind "$KEYMAP" /k.xkb                  # never rw
[--ro-bind /usr/include/xkbcommon/xkbcommon-keysyms.h <same path>]   # only if the contract keeps the header
--chdir /oracle
/usr/bin/python3 -I -B /oracle/tool.py how-to-type --keymap /k.xkb --disable-compose --keysym ARG
```
wrapped outside by `strace -f -qq -e trace=execve,execveat,socket,socketpair,connect,fork,vfork,clone,clone3,openat,open,… -o
"$WORK/trace-XXX"` — trace file under `--work`, never `/tmp`, never the lane.

Tripwire reading rules (extending the round-48 v2 reader, which is the right base):
- start after the payload's `execve("/usr/bin/python3"` and treat `<... … resumed>` lines as continuations (M48-12's
  `???(<detached` flake class);
- a write trip is an `openat` whose flag word contains `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND` **or** any of
  `mkdir/mkdirat/rename/unlink/symlink/link/truncate` — and it must fire for `__pycache__` too, which is why G4 forces `-B`
  (H7);
- run the *judge* through the same trace with `writes_ok=False` as an invariant check (round 48 traced only the tool): the
  judge is pinned and must never write (`r1`, `r4` show 0);
- `python-execve-not-seen` is a trip, never a skip.

Optional stronger guard for "starts no process": `bwrap --seccomp` with a profile denying `fork/vfork/clone/clone3/execve`
after the initial exec. Not exercised here (no profile builder in stdlib); the strace reader is the working guard.

### G5 — host-state digest (the `M48-10`/N2 pair)

`receipts/r9-operator-state.txt` is the executable shape: `stat -c '%F %s %Y'` + `sha256sum`, `~` for the home prefix,
**no directory listings**, every row labelled `operator-owned` or `package-file`.

```
~/.XCompose                      regular file 240 1791060272 09f65e20…7f05a   present
~/.config/xkb                    absent
~/.xkb                           absent
~/.cache/xdg-terminal-exec       regular file 190 1793069967 ddd94f6b…a1b3d5 present
/etc/xkb                         absent
/usr/share/xkeyboard-config-2.d  absent
/usr/share/xkeyboard-config.d    absent
```
Counters run this **before and after** their own work and fail (exit 3) on any delta; the mutants run it around every
mutant with the fake home substituted (ExecMutantSandbox's `hostguard.py` is the same shape — it should take the path list
as an argument so counters and seats share one implementation).

### G6 — clauses to paste into the C1/C2 counter drafts and the w2 seat prompts

1. "The compile runs `env -i PATH=/usr/bin` with `--include=/usr/share/xkeyboard-config-2`; the keymap each fixture is
   judged on is the one whose digest `meta` prints, and it must equal the default-path compile in a pristine scratch home."
2. "The judge and the tool are invoked with `--keymap=… --disable-compose --keysym …`; the counter asserts both flags on
   the argv it built, and rejects any judge stdout containing `=== Access via Compose sequences ===` or zero data rows."
3. "The tool runs under `python3 -I -B` with `/oracle` read-only; it is a single file and imports no sibling module."
4. "Every sandbox is `--unshare-all --clearenv` with the bind set in G3/G4; the loader is bound at
   `/lib64/ld-linux-x86-64.so.2`."
5. "Mutant write targets are `realpath`-checked against `--work`; `HOME`/`XDG_*` are redirected into `--work`, and the G5
   digest pair brackets every run."
6. "No seat commits `hyprctl devices -j` content, any `/run/user/<uid>/hypr/<sig>` substring, or a directory listing of
   `~`."
7. "`/tmp`, `/var/tmp`, `/dev/shm` as `--work`/`TMPDIR` are a `Setup` refusal (SentScratch F1/F2), and the strace file lives
   under `--work`."

---

## What an attacker gains, ranked

| # | shape | guard that stops it | residual |
|---|---|---|---|
| 1 | judge silently re-derives a keymap from host state, both sides agree on an empty table | G2 argv+stdout assertions; 0-row = `Setup` | needs the assertion to be written |
| 2 | a control/mutant plants `xkb/symbols/br` in the counter's own work dir and rewrites the fixture | G1 `--include` + both-ways `cmp` + pinned digests | none observed |
| 3 | operator compose table read into the verdict | G2 `--disable-compose` + stdout assertion | none observed |
| 4 | a mutant writes the operator's real cache (M48-10 replay) | G5 digest pair + `HOME` redirect + bwrap | digest list is finite |
| 5 | Python bytecode write trips or lands in a rw dir | G4 `-B`, `/oracle` ro | none observed |
| 6 | sandbox that "fails" because the loader is bound at the wrong path | G3/G4 loader path | none observed |

## Residual risk / not tested

- The C1/C2 counters do not exist yet this wave; the guards above are specifications against the round-48 v2 reader, not a
  verification of round-49 code.
- `bwrap --seccomp` as a hard no-process guard: not exercised.
- Keymap format 1 input, and keymaps whose layout names vary per group: not exercised (outside this seat's surface).
- `xkbcli dump-keymap*` / `interactive-*`: forbidden by the guard, therefore not traced.
- Everything ran as this user; I did not test whether user namespaces could be disabled on the host (they work:
  `bwrap --unshare-user` succeeded in every probe).
- No host service was signalled, no compositor verb other than the four allowed reads was called, no package transaction
  ran (versions were read from `/var/lib/pacman/local/*/desc`).

## Tools installed / updated by this seat

None. Every binary used (`xkbcli*`, `hyprctl`, `bwrap 0.13.1`, `strace 7.2`, `python3 3.14.8`) was already present.
