# SentHost — host safety of the round-48 probes

Seat `SentHost`, round 48 w1 (BUILD), base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Read-only review; no
tracked file edited, no compositor/config/binary touched, no package transaction, no subagent. Scratch lived in
`/fast/scratch/hyaku/mado-r48/SentHost/` (removed; `probe.sh` carries `trap 'rm -rf -- "$S"' EXIT`).
Receipts in `SentHost/receipts/` are produced by `SentHost/probe.sh` (re-runnable, ~2 s, bounded).

**Host state at the end of this seat: unchanged.** `/home/vgpnk/.cache/xdg-terminal-exec` is 190 B, mode 600,
inode 143468605, mtime 1793047345, sha256 `f497ed057f8aaba24bea21ba652b810c6c2ab754b0b8fe9d9b1645e072a10cac`
before and after every probe in this seat (mtime 2026-10-26 17:42:25 -0300) — and that hash is the one round 47 recorded, so the file has not moved
since round 47 (`receipts/01-host-cache-before.txt`, `receipts/07-host-cache-after.txt`).

Guards in copy-paste form: `SentHost/guards.md` (G1-G6). Findings below.

---

## F1 (high — evidence integrity) the prime race makes a warm fixture pass while never warming

**Attacks:** the C1 contract clause that scores a primed, warm cache (`claims.md` C1; fixture schema v2 `prime`).

The pin writes its cache in a background child, `save_cache "$1" &` (pin :1457). Inside the counter's sandbox
the launched process is not pid 1; bwrap's own init is, and it exits when the command exits, taking every
remaining process of the pid namespace with it. Measured in the round-47 sandbox shape
(`receipts/02-prime-race.txt`):

| prime shaper | cache after the run |
|---|---|
| A `sh -c 'pin --print-cmd'` (sandbox exits with the pin) | **ABSENT** |
| B `bwrap --as-pid-1 … sh -c 'pin; wait'` | **ABSENT** |
| C `default init`, busy poll with no sleep (~1 ms) | **ABSENT** |
| D `default init`, bounded `sleep 0.01` poll, 3/3 runs | present, 168 B, 20-25 ms |

**Exploit path (silent, no error anywhere):** the counter primes a case, the cache never appears, the scored
"warm" run is a cold run, the oracle (pin) and the tool (Python) are both cold, they agree, the clause passes.
The fixture that exists to prove *the warm answer differs from the cold one* proves nothing, and the counter's
final line still says `TARGET_MET`. This is the fabricated-readiness class: the instrument reports the property
it never exercised.

**Impact:** the new C1 claim (warm-cache path) would be scored by an instrument that cannot fail on it; w2 would
inherit a blind spot and the freeze would publish it.

Independently reproduced in this round by ExecCounterC1 (its own primer: a fixed `sleep 0.15` after the pin;
75 of 128 placeholder fixtures primed, exactly the ones whose args reach the save site) and, stronger than
anything in this seat, proved with a forged cache the pin then answered from (`forge_live=ok`). That proof is
the better warm-path witness; the `XTE_DEBUG` assertion below is the cheap per-run version.

**Smallest remediation:** G1 — prime through `/bin/sh -c '<pin> "$@"; while [ ! -s <cache> ] && [ $i -lt 500 ]; do
sleep 0.01; …'`, treat "no complete cache after priming" as a **setup error** (exit 2, not a scored miss), and
assert on the *scored* run that the oracle itself took the warm path (`XTE_DEBUG=1` → stderr contains
`D: cache is actual`, pin :275; measured `receipts/03-cache-mutation.txt` §5, cold control `D: no cache data`).

## F2 (high — host state) the host cache is one inherited variable away, and two ordinary flags delete it

**Attacks:** every seat that runs the resolver by hand; the counter only if it ever runs the pin outside bwrap.

The cache target is `${XDG_CACHE_HOME:-$HOME/.cache}/xdg-terminal-exec` (pin :172-173). This session's ambient
environment already carries `XDG_CACHE_HOME=/home/vgpnk/.cache` (`receipts/06-host-tooling.txt`,
`receipts/08-cache-path-resolution.txt`), so the *default* target of a hand-run `xdg-terminal-exec --print-cmd`
is the live host file. Resolved without running anything:

```
ambient env                          -> /home/vgpnk/.cache/xdg-terminal-exec
ambient, XDG_CACHE_HOME unset        -> /home/vgpnk/.cache/xdg-terminal-exec
guard env (XDG_CACHE_HOME=<work>)    -> <work>/cache/xdg-terminal-exec
```

And the *mode* decides whether the cache is touched at all: the print modes `id`, `path` and `content` bail out
early (`# early bail out in some print modes`, pin :1368-1385, the `exit 0` at :1376/:1383) before the save site
at :1457, while `cmd` and the launch case continue. So a cold `--print-cmd` wrote a 168 B cache in every measured
run, and `--print-id`/`--print-path` never wrote or deleted it even with the cache disabled
(`receipts/03-cache-mutation.txt` §6). Measured deletions, reproduced in a scratch cache and never on the host
file (`receipts/03-cache-mutation.txt` §2-§4):

| trigger (modes that reach :1455: `--print-cmd`, `--test-mode`, a launch) | effect |
|---|---|
| cold run | writes the file (mode 0600, `umask 0077`, pin :319-321) |
| `XTE_CACHE_ENABLED=false … --print-cmd` | **cache file deleted** (pin :1172-1179 skip the read; :336-337 `rm -f`) |
| a `/disable_cache` line in the list file (pin :383) | **cache file deleted** on the same run (:337) |
| warm run | no write (:1456 gates the save) |
| `--print-id` / `--print-path` / `--print-content` | nothing at all: exit at :1376/:1383, before the save site |

Consequence for the fixture set: a case whose `args` are `--print-id`/`--print-path` has no cache to warm and
must not be primed (ExecCounterC1 measured the same split: 75 of 128 placeholders primed). A `prime` on such a
case is a schema error, not a test of the tool.

**Scope (corrected by ExecCounterC1):** its draft cannot reach the host cache by construction — every pin and tool
run goes through its `sandbox()`, `case_env()` forces `XDG_CACHE_HOME=<case root>/.cache` materialized empty per
run, `HOME` is always set and validated, and fixture `env` naming HOME/PATH/XDG_CACHE_HOME (or pointing into the
operator's home) is a setup error. F2 therefore does not describe that instrument's normal path; it describes the
ad-hoc seat probe and any future harness mistake, which is exactly what the tripwire (G2) would notice — the draft
has no equivalent, so the guard stands on its own merit.

**Impact:** one stray `XTE_CACHE_ENABLED=false xdg-terminal-exec --print-cmd` in a seat probe deletes the
operator's real cache; a stray cold `--print-cmd` run silently *overwrites* it. (`--print-id`/`--print-path`
probes are safe on this axis, which makes `--print-cmd` the only mode seats need to police.) Either way the host's next SUPER+RETURN
recomputes or misses a cache the round never intended to touch — and, because the file is now a fixture input
for C1, a changed host cache also means a changed environment for anything that later runs unredirected. It is
also a correctness hazard in the other direction: while the host cache is valid, an unredirected "cold" run
takes the warm path (pin :274-284) and a seat's cold expectation is silently wrong.

**Smallest remediation:** G2/G3 — `XDG_CACHE_HOME` into scratch before any resolver call (a refusal guard if it
resolves under `/home`), the six `XDG_*`/`HOME` inputs pinned, plus the counter-level tripwire on the host
cache signature (size, mtime_ns, inode, sha256) that raises a setup error if it moves. The r47 counter's own
shape is already safe (bwrap `--clearenv` :139, bwrap process run with `env={"PATH": "/usr/bin"}` :166,
`XDG_CACHE_HOME=<root>/.rw/cache` :224) — the risk is in the ad-hoc seat probes and in any new code path that
runs the pin without the wrapper; freeze that property with a self-check that every pin invocation starts with
`box.bwrap`.

## F3 (medium — fixture validity) `HOME` is the fallback cache root, and the r47 root is read-only

With `XDG_CACHE_HOME` unset the cache goes to `$HOME/.cache`, and with `HOME` unset too the pin resolves
`/.cache/xdg-terminal-exec` (`receipts/08-cache-path-resolution.txt`). Measured inside the r47 sandbox shape
(`receipts/09-home-fallback.txt`):

- `HOME=<root>/home` (the r47 shape, root read-only), `XDG_CACHE_HOME` unset → `mkdir: cannot create directory
  …: Read-only file system`, **no cache**, and the pin still prints its answer with rc 0;
- `HOME=<root>/.rw/home` (writable) → cache written, 184 B.

The D1 HOME-unset cases (`ExecHomeUnset/run.py:45,51,58`) do unset it, but they are all `--print-id` runs, which
never reach the save site, so they are unaffected; the hazard appears the moment such an env is combined with
`prime` and a `cmd` run. ExecCounterC1's draft cannot hit it either (`HOME` is always set to `<case root>/home`),
which leaves F3 a constraint on the schema and on seat probes.

**Impact:** a warm fixture whose `env` unsets `XDG_CACHE_HOME` can never be primed in the current root shape, and
the failure is an stderr
line nobody compares — the same silent cold-vs-cold pass as F1. The `HOME`-unset path also leaves the sandbox
conceptually: `/.cache` is neither scratch nor the case root.

**Smallest remediation:** in schema v2, a case that carries `prime` must either set `XDG_CACHE_HOME` under
`<root>/.rw` or have its `HOME` writable (bind `<root>/.rw/home` as `$HOME`), and the prime check of G1 must
read the file at the path the case env actually resolves, not a hard-coded one.

## F4 (medium — evidence integrity) `xkbcli compile-keymap` is read-only but its *inputs* are environment-controlled

**Attacks:** the C2 receipt (`xkbcli compile-keymap … --layout br --options compose:caps`) and any claim about
which names compile.

Read-only confirmed: `strace` over the compile shows 0 write-ish file ops, 0 sockets, 2 execve
(`/usr/bin/xkbcli` → `/usr/lib/xkbcommon/xkbcli-compile-keymap`) — `receipts/04-xkbcli-env.txt` §1. But:

1. **Include paths are user-writable and are searched first.** A `symbols/zz` placed in `$XDG_CONFIG_HOME/xkb`,
   `$HOME/.xkb` or under `XKB_CONFIG_EXTRA_PATH` **compiled** (`name[Group1]="POISON"` in the output) — §3. So
   the answer to "does `zz` compile" depends on three directories in `$HOME` and one env var, and the receipt's
   own `env -i`-less run inherits them.
2. **`XKB_CONFIG_ROOT` silently changes which tree is searched, and its failure mode differs from unset**:
   `XKB_CONFIG_ROOT=<empty dir>` → that dir; `=/nonexistent` → falls back to `/usr/share/X11/xkb`; unset →
   `/usr/share/xkeyboard-config-2`. Three different "searched root" strings for the same host — a receipt that
   quotes the line without pinning the env is quoting a state that a later run need not reproduce.
3. **`XKB_LOG_LEVEL` decides whether the XKB-595 warning exists.** Ten rows measured (§4): numeric `0`, `5`, `10`
   and the symbolic `critical` suppress it entirely with rc still 0; `20`, `30`, `error`, `warning`, `none` and an
   unknown token show it; `info`/`debug` show it plus chatter. The C2 claim "unknown option is dropped with a
   warning, rc 0" is *half* an environment claim. (My first sweep missed `critical`; ExecXkbLive measured the
   symbolic side independently and is right — the receipt now carries the full matrix.)
4. `XKB_DEFAULT_{RULES,MODEL,LAYOUT,VARIANT,OPTIONS}` are **inert** for this tool (§2: `XKB_DEFAULT_LAYOUT=zz`
   and `XKB_DEFAULT_RULES=nope` leave the keymap identical, rc 0) — unlike the compositor, which reads them
   (`ScoutHyprKeymap` item 1-2). A receipt generated with `xkbcli` therefore cannot exercise the compositor's
   defaults; the entry must not imply that it does.

Bonus, for the freeze: the same run settles `ScoutHyprKeymap`'s open `[INFERENCE]` ("whether the Arch build
keeps the meson defaults") — an all-empty compile fails with
`Couldn't look up rules 'evdev', model 'pc105', layout 'zz', variant '(null)', options '(null)'`
(`receipts/04-xkbcli-env.txt:45`), i.e. the host binary carries evdev/pc105 defaults.

**Impact:** a C2 receipt taken with the ambient environment is not reproducible; a poisoned `~/.config/xkb` (the
operator's own, or a seat's mistake) would change or break the compile with no trace in the receipt, and a
suppressed `XKB-595` would make the "warning" row unsupported by its own receipt.

**Smallest remediation:** G4 — `env -i` with `PATH`, a scratch `HOME`/`XDG_CONFIG_HOME`, `XKB_CONFIG_ROOT`/
`XKB_CONFIG_EXTRA_PATH` unset, `XKB_LOG_LEVEL` unset, plus the assertion that the `include paths searched` line
names `/usr/share/xkeyboard-config-2` and that none of the three user paths exist on the host (measured absent
today: `/home/vgpnk/.config/xkb`, `/home/vgpnk/.xkb`, `/etc/xkb`).

## F5 (medium — session material) `hyprctl devices -j` carries hardware names and device addresses

Measured shape only, no values (`receipts/05-devices-shape.txt`): `keyboards[10]` with
`name,address,active_keymap,layout,variant,options,model,rules,main,capsLock,numLock,active_layout_index`;
`mice[4]` with `name,address,scrollFactor,defaultSpeed`. `name` is the kernel product string and `address` the
device node id — a hardware fingerprint. `active_keymap` is a locale label ("Portuguese (Brazil)"), not personal
but not needed either. Nothing in C1 or C2 needs this verb.

**Already at base (cannot be fixed here, must not be repeated):** `.ufo/waves/round-46/receipts/live-devices-host-r46.txt`
carries **14** `name="…"` values (first at line 7), i.e. the committed corpus holds device model names against
the round rule "input-device names beyond what a task asks". `hyprctl monitors -j` is the same class
(descriptions, serials) and must be treated as off-limits even though it is a "-j read verb".

**Smallest remediation:** G5 — shape-only filter (counts + key names), no raw dump in any seat dir, no
`monitors -j`; if a claim ever needs a name, it needs exactly one, redacted to its class (`keyboard #3`).

## F6 (low — sandbox preconditions) bwrap needs the loader symlinks; the tree must be bound as-is

bubblewrap 0.13.1, strace 7.2, unprivileged userns available and not AppArmor-restricted
(`receipts/06-host-tooling.txt`). Two operational facts the counters depend on:

- without `--symlink usr/lib /lib --symlink usr/lib64 /lib64`, every exec inside the sandbox fails
  `execvp … No such file or directory` (measured);
- with no `/etc` inside, `ls -l` prints numeric ids: a root-owned host binary shows `65534 65534` (root unmapped
  in the user namespace), a counter-created file shows `1000 1000`. The C1 `ls -LRl` emulation must produce
  exactly these numbers — a model that prints `root`/`vgpnk` or `0` misses the md5 by construction.

**Smallest remediation:** G6 — keep the r47 bind shape, bind the case root as it is (a tmpfs copy changes
`total` lines and the hash), keep `strace -o` outside the sandbox and under `--work`.

---

## Not a finding (checked, clear)

- `xdg-terminal-exec`'s pin bytes equal the host binary (sha256 `89f2be9a…` both, re-verified this seat), so the
  oracle is the host's resolver and the sandbox does not need `/usr/bin`.
- The r47 counter runs every tool under `strace -f … execve,execveat,socket,socketpair,connect` and the sandbox
  binds no `/usr/bin`, `/usr/share`, `/etc`, `/home`, `/fast`, `/run`, `/var` (allowlist :39-45, argv :139-148) — the resolver
  cannot reach the host cache from inside it.
- `xkbcli` has no `interactive-*` path in this seat's use; no compositor verb except `devices -j` was issued, and
  it was piped straight into the shape filter.
- No `.ufo`/fleet file, no lane index, no PATH directory was written; nothing outside `SentHost`'s seat dir and
  scratch.
- One guard shape that *looks* protective and is not: an `openat`-path check for "/home" inside the sandbox.
  Measured: `/home`, `/home/vgpnk` and `/etc/xkb` are all absent inside the r47 sandbox, so such a clause can
  never fire; if a counter adds one, its predicate must be the literal host prefix and never `$HOME` (inside the
  sandbox `$HOME` is the case home fixtures legitimately read, so a `$HOME` predicate trips every correct run).
  The `/fast` direction fails too: bwrap creates the bind target's missing parents as empty stubs, one level
  each, so a `/fast`-prefix check matches the legitimate case root (stub test in `receipts/06-host-tooling.txt`;
  no sibling seat directory is reachable). `guards.md` G2 carries the same caveat. ExecCounterC1 measured the
  `/fast` stub on its own builder and demoted the clause to regression-tripwire material.
