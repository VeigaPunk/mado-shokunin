# Guard text — round 48 host-safety (SentHost)

Copy-paste blocks. Every claim here is measured; the receipt that proves each is named.
Nothing in this file may be weakened without a receipt that shows the failure mode is gone.

---

## G1 — the prime must wait for the background save (counter clause)

The pin forks its cache write (`save_cache "$1" &`, pin :1457). Inside the counter's bwrap the sandbox's
pid-namespace init takes that child with it when the sandbox exits, so **a prime that just runs the pin and
returns leaves no cache at all** (`receipts/02-prime-race.txt`, variants A, B, C: cache ABSENT).
A warm fixture then compares cold-against-cold and passes without exercising the warm path.

```python
PRIME_DEADLINE_S = 5.0        # measured: the write lands in 19-25 ms
CACHE_TAIL = b"END_OF_EXEC_USEP\n"

def primed(box, root, env, args):
    """Run the pin cold and keep the sandbox alive until the cache file is complete."""
    rw_cache = env["XDG_CACHE_HOME"] + "/xdg-terminal-exec"
    # keep the sandbox alive after the pin returns: poll with a REAL sleep, bounded
    sh = ('/oracle/xdg-terminal-exec "$@" >/dev/null 2>&1; '
          'i=0; while [ ! -s "' + rw_cache + '" ] && [ $i -lt 500 ]; do sleep 0.01; i=$((i+1)); done')
    # wrap the pin: replace the final ['/oracle/xdg-terminal-exec'] + args of Box.argv() (:137-155) with
    # ['/bin/sh', '-c', sh, '/oracle/xdg-terminal-exec'] + args -- the wrapper is what keeps the sandbox alive
    box.run_wrapped(root, env, sh, args)
    blob = open(rw_cache, "rb").read()                 # host side, after the sandbox is gone
    if not blob.endswith(CACHE_TAIL):                  # truncated or absent -> the prime failed
        raise Setup("prime did not produce a complete cache at %s (%d B)" % (rw_cache, len(blob)))
```

Required consequences in the counter:

- `prime` is **not** optional sugar: a case with `prime` but no cache file after priming is a **setup error**
  (exit 2), never a scored miss.
- the warm clause must also assert that the **scored** oracle run took the warm path, not just that a file exists:

```python
# oracle warm-path assertion (stderr only, stdout untouched)
env_dbg = dict(env, XTE_DEBUG="1")
rc, out, err = box.run(root, env_dbg, tool=False, args=args)
assert "D: cache is actual" in err, "warm clause did not reach the cache (pin :275)"
```

  `XTE_DEBUG=1` is read at pin :61 and writes to stderr only; the measured lines are `D: cache is actual`
  (warm) and `D: no cache data` (cold) — `receipts/03-cache-mutation.txt` §5.
- do **not** compare stderr (debug output is 40 vs 431 lines warm/cold, measured).

## G2 — the host cache tripwire (counter clause, every counter that runs the resolver)

The resolver's cache target is `${XDG_CACHE_HOME:-$HOME/.cache}/xdg-terminal-exec` (pin :172-173).
This seat shell has `XDG_CACHE_HOME=/home/vgpnk/.cache` in its environment, so the *default* target of any
unredirected run is the real host file — which exists (190 B, mode 600, sha256 `f497ed05…`, unchanged since
round 47: `receipts/01-host-cache-before.txt`, `07-host-cache-after.txt`, `08-cache-path-resolution.txt`).

```python
HOST_CACHE = os.path.expanduser("~/.cache/xdg-terminal-exec")

def cache_sig():
    try:
        st = os.stat(HOST_CACHE)
        return (st.st_size, st.st_mtime_ns, st.st_ino,
                hashlib.sha256(open(HOST_CACHE, "rb").read()).hexdigest())
    except FileNotFoundError:
        return None

sig0 = cache_sig()          # first statement of main()
...                          # all work
if cache_sig() != sig0:
    raise Setup("the host xdg-terminal-exec cache changed during this run - a probe escaped its sandbox")
```

Scope: a counter that forces `XDG_CACHE_HOME=<root>/.cache` (materialized empty per run), always sets and
validates `HOME`, and rejects fixture `env` naming HOME/PATH/XDG_CACHE_HOME cannot reach the host cache by
construction — ExecCounterC1's draft does exactly that. The tripwire is not a criticism of that design; it is the
only thing that would notice a future harness mistake or an ad-hoc seat probe, and it costs one stat plus one hash.

Two hard rules that make the tripwire unnecessary to trip:

1. **Every** execution of the pin or of `/usr/bin/xdg-terminal-exec` — including one-off probes, `expect`
   generation, `-h`/`--version` checks and print-mode runs — happens inside the bwrap sandbox with
   `XDG_CACHE_HOME` set to a directory under `--work`. `--print-cmd` is NOT a read-only mode: a cold run wrote a
   168 B cache in every measured case (`receipts/03-cache-mutation.txt` §1), and with the cache disabled it
   deleted the file. `--print-id`/`--print-path`/`--print-content` exit before the save site (pin :1368-1385) and
   neither write nor delete (§6) — which also means a fixture whose args are id/path-only has no cache to warm and
   must not carry `prime`.
2. The Python harness passes only `env={"PATH": "/usr/bin"}` to the bwrap process and the sandbox is
   `--clearenv` (r47 counter :139, :166) — keep both. A static self-check is cheap and worth freezing:
   `assert all(argv[0] == box.bwrap for argv in every_run_argv)`.

One caveat about the *other* shape of this guard: an `openat`-path check for "anything under `/home`" inside
the sandbox is vacuous — the r47 sandbox binds no `/home`, so the path does not exist there and the check can
never fire (`receipts/06-host-tooling.txt`, "absent: /home"). The `/fast` direction is no better: bwrap creates
the missing parents of a bind target as empty stub directories, one level each, so a `/fast`-prefix check matches
the legitimate case root (`receipts/06-host-tooling.txt`, stub test; the stubs hold nothing but the next path
component and no sibling seat directory is reachable). If a counter adds such a check anyway, its
predicate must be the literal host prefix, never `$HOME`: inside the sandbox `$HOME` is the case home that
fixtures legitimately read, and a `$HOME` predicate would trip on every correct run. The tripwire is the check
that has teeth, and it costs one stat plus one hash.

Measured host-state hazards the tripwire covers (`receipts/03-cache-mutation.txt` §2, §3, all reproduced in a
scratch cache, never on the host file):

| trigger | effect on the cache file |
|---|---|
| cold run | writes it (mode 0600, `umask 0077`, pin :319-321) |
| `XTE_CACHE_ENABLED=false` | `rm -f` the cache file (pin :1172-1179 skip the read, :336-337 delete) |
| `/disable_cache` line in the list file | `rm -f` the cache file (pin :383, then :337) |
| warm run | no write (pin :1456 gates on `XTE__CACHE_USED`) |
| `--print-id` / `--print-path` / `--print-content` | nothing: pin :1368-1385 exits before the save site |

## G3 — seat prompt preamble for any probe that runs the resolver

```bash
S=/fast/scratch/hyaku/mado-r48/<Seat>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT
# the resolver writes $XDG_CACHE_HOME/xdg-terminal-exec and deletes it when the cache is disabled
export XDG_CACHE_HOME="$S/cache"          # MUST be set before any xdg-terminal-exec call
export HOME="$S/home"                     # no host ~/.config, ~/.local/share, ~/.cache
export XDG_CONFIG_HOME="$S/home/.config" XDG_DATA_HOME="$S/home/.local/share"
export XDG_CONFIG_DIRS="$S/etc/xdg"       XDG_DATA_DIRS="$S/usr/share"
export XDG_CURRENT_DESKTOP=Hyprland       # pin it: it is one of the six hash inputs
mkdir -p "$HOME" "$XDG_CONFIG_HOME" "$XDG_DATA_HOME" "$XDG_CONFIG_DIRS" "$XDG_DATA_DIRS"
case "$XDG_CACHE_HOME" in /home/*|"") echo "REFUSING: cache would resolve outside scratch"; exit 2;; esac
```

One more trap (hit while writing this seat's own probe): a cold `--print-cmd` run's background writer lands up to
~20 ms after the command returns, so `rm -f` immediately followed by the next measurement can lose the race and
see a cache that belongs to the previous run. After any resolver run, wait for the writer to settle
(`sleep 0.2`, or poll for the file) before interpreting its absence or presence.

`XDG_CURRENT_DESKTOP` matters twice: it is written into the hash (pin :186) and it selects the
`hyprland-xdg-terminals.list` lookup paths (pin :148-162). Leaving it ambient makes a seat's answer depend on
the shell it was started from.

## G4 — `xkbcli compile-keymap` receipt recipe

`xkbcli compile-keymap` is read-only: 0 write-ish syscalls, 0 sockets, 2 execve (`/usr/bin/xkbcli` →
`/usr/lib/xkbcommon/xkbcli-compile-keymap`) — `receipts/04-xkbcli-env.txt` §1. But its **input set** is
environment-controlled, and three of the four controls are user-writable paths:

Search order per libxkbcommon `context.c` (`ScoutHyprKeymap` item 4): `$XDG_CONFIG_HOME/xkb` (else `$HOME/.config/xkb`)
→ `$HOME/.xkb` → `XKB_CONFIG_EXTRA_PATH` (default `/etc/xkb`) → the root. Each member is measured to be honoured
(`receipts/04-xkbcli-env.txt` §3); the order itself is sourced, not re-measured here.

| control | measured effect |
|---|---|
| `$XDG_CONFIG_HOME/xkb`, `$HOME/.xkb` | searched first; a poisoned `symbols/zz` there compiles (§3) |
| `XKB_CONFIG_EXTRA_PATH` | searched; poisoned tree compiles (§3) |
| `XKB_CONFIG_ROOT` | replaces the root; `/nonexistent` silently falls back to `/usr/share/X11/xkb` while unset prints `/usr/share/xkeyboard-config-2` (§3) |
| `XKB_DEFAULT_{RULES,MODEL,LAYOUT,VARIANT,OPTIONS}` | **inert** for this tool (§2) — unlike the compositor, which reads them |
| `XKB_LOG_LEVEL` | numeric 0..10 and the symbolic `critical` suppress `XKB-595` entirely (rc unchanged); `error`, `warning`, `none` and unknown tokens show it; `info`/`debug` show it plus chatter (§4, ten rows) |

```bash
S=/fast/scratch/hyaku/mado-r48/<Seat>; mkdir -p "$S/home" "$S/etc"
env -i PATH=/usr/bin:/bin HOME="$S/home" XDG_CONFIG_HOME="$S/home/.config" LC_ALL=C \
  /usr/bin/xkbcli compile-keymap --layout br --options compose:caps > "$S/keymap.txt" 2> "$S/err.txt"
# assertions that keep the receipt honest
grep -q 'include paths searched' "$S/err.txt" && grep -q '/usr/share/xkeyboard-config-2' "$S/err.txt"
HOST_HOME=$(getent passwd "$(id -un)" | cut -d: -f6)
for p in "$HOST_HOME/.config/xkb" "$HOST_HOME/.xkb" /etc/xkb; do
  [ -e "$p" ] && echo "WARNING: a user xkb path exists, the pinned HOME hides it: $p"
done   # measured 2026-10-26: all three absent, so the pinned HOME cannot change the answer
```

- never `env -u HOME` for this receipt unless the case is the HOME-unset case (it changes the
  "could not be added" list, not the compiled keymap);
- if a receipt must quote the include-path list, the scratch root appears in it — rewrite it to `$HOME` and say
  so, or quote only the `include paths searched` line, which names the host root;
- with an empty root even a valid `--layout br` fails (rules/evdev missing, rc 1 XKB-338) — so "rc 0 for the
  host's names" also asserts that the root was found;
- an all-empty compile is the cheap host confirmation of the build defaults: it fails with
  `Couldn't look up rules 'evdev', model 'pc105', layout 'zz', variant '(null)', options '(null)'`
  (`receipts/04-xkbcli-env.txt` §5).

## G5 — `hyprctl devices -j` (session material)

Measured shape (`receipts/05-devices-shape.txt`): 10 keyboards, 4 mice, keys
`name,address,active_keymap,layout,variant,options,model,rules,main,capsLock,numLock,active_layout_index`
and `name,address,scrollFactor,defaultSpeed`. `name` is the kernel product string, `address` the device node id:
both are host-hardware fingerprints. Round 46's committed receipt carries **14** `name="…"` values
(`.ufo/waves/round-46/receipts/live-devices-host-r46.txt:7` first, count 14) — that exposure is at base and is
not this round's to repeat.

```bash
# shape-only: counts and key names, never values
hyprctl devices -j | python3 -c '
import json,sys
d=json.load(sys.stdin)
KEEP={"layout","variant","options","model","rules","main","capsLock","numLock","active_layout_index","scrollFactor"}
for k,v in sorted(d.items()):
    keys=sorted({x for e in v if isinstance(e,dict) for x in e}) if isinstance(v,list) else []
    print("%s: %d entries; shape keys %s" % (k, len(v), ",".join(sorted(set(keys)&KEEP))))'
```

Rules: no raw dump into a seat dir or receipt; `hyprctl monitors -j` is a read verb but yields monitor
descriptions and serials — treat it as off-limits for the same reason, and `hyprctl output`/`dispatch`/`keyword`
stay forbidden. Nothing in C1 or C2 needs this verb at all.

## G6 — sandbox preconditions (bwrap / strace)

Measured (`receipts/06-host-tooling.txt`): bubblewrap 0.13.1, strace 7.2, `kernel.unprivileged_userns_clone=1`,
`user.max_user_namespaces=122865`, no `apparmor_restrict_unprivileged_userns`. bwrap must be invoked with the
loader symlinks or every exec fails with `execvp … No such file or directory`:

```
bwrap --unshare-all --die-with-parent --new-session --clearenv \
      --ro-bind /usr/lib /usr/lib --symlink usr/lib /lib --symlink usr/lib /lib64 \
      --ro-bind /usr/bin/bash /bin/sh --ro-bind /usr/bin/bash /bin/bash \
      --ro-bind <bin> /oracle/bin --dev /dev --proc /proc --tmpfs /tmp \
      --ro-bind <root> <root> --bind <root>/.rw <root>/.rw ...
```

- bind the case root **as it is** (no tmpfs copy): `ls -lR`'s `total` lines and the `-LRl` hash depend on the
  filesystem the tree really lives on;
- inside the sandbox there is no `/etc`, so `ls -l` prints numeric ids — a root-owned host binary shows
  `65534 65534` (unmapped in the user namespace), a file the counter created shows `1000 1000`;
- `strace -o` writes outside the sandbox; keep that path under `--work` and trace tool runs only.
