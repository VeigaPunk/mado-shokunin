# RevengerCache — the resolver cache: what the hotkey run actually uses on this host

Seat: RevengerCache (round 47, w2 FALSIFY). Target: `xdg-terminal-exec`'s cache — does the hotkey run read
`~/.cache/xdg-terminal-exec` or resolve cold, and is the cold capture equal to what the hotkey uses today?

**Verdict: the hotkey run reads the cache, not a cold resolution — and today the cache agrees with a cold
resolve.** The md5 that the resolver derives right now, recomputed independently under the compositor's own
environment, equals line 1 of the host cache (`d27b6b707781b8106c7b00390bdf2822`), the resolver accepts that
cache (`cache is actual`), and the warm run's stdout is byte-identical to a cold run's for the hotkey's
argument shapes. That agreement is *contingent*, not structural: the key is metadata-only and the cache file's
content is unvalidated, so a warm cache and a cold resolve can diverge with the hash unchanged (H1, H2 below).

Nothing was launched, no host file was written, `xdg-terminal-exec` was only ever invoked with a `--print-*`
option and with `XDG_CACHE_HOME` inside scratch. Host cache digest before and after all probes:
`sha256 f497ed057f8aaba24bea21ba652b810c6c2ab754b0b8fe9d9b1645e072a10cac`, size 190, mode 600,
mtime `2026-10-26 17:42:25 -0300` (`RevengerCache/host-cache.txt`).

## 1. The chain, as coded

| rung | evidence |
|---|---|
| cache path is `$XDG_CACHE_HOME/xdg-terminal-exec` | `XTE__CACHE_FILE=${XDG_CACHE_HOME}/xdg-terminal-exec` (xdg-terminal-exec:173); compositor env sets `XDG_CACHE_HOME=~/.cache` |
| cache is on unless disabled | `XTE__CACHE_ENABLED=${XTE_CACHE_ENABLED-true}` (xdg-terminal-exec:1172); the compositor env carries **no** `XTE_*` at all (`grep -c '^XTE' /proc/<Hyprland>/environ` = 0) |
| it is read **before** any config file | `if check_bool "${XTE__CACHE_ENABLED}" && read_cache; then` (xdg-terminal-exec:1179); `read_config_paths` sits in the `else` branch (xdg-terminal-exec:1198; branch opens at :1181) |
| both existing list files carry **no** cache directive | `grep -nE '^/(disable_cache\|enable_cache)' ~/.config/xdg-terminals.list /usr/share/xdg-terminal-exec/xdg-terminals.list` → none |
| re-use gate = hash + the cached command resolving | `command -v "$xte__cached_cmd" > /dev/null` (xdg-terminal-exec:274) |
| key = md5 over a literal version, `$XDG_CURRENT_DESKTOP`, and `ls -LRl` of the config + applications paths | `echo 4` (xdg-terminal-exec:194) and `LANG=C ls -LRl ${xte__hash_paths} 2> /dev/null` (xdg-terminal-exec:200) |
| any run that reaches argument composition saves the cache from a background child | `if [ "$XTE__CACHE_USED" = "false" ]; then` (xdg-terminal-exec:1455) then `save_cache "$1" &` (xdg-terminal-exec:1457) |

The hotkey path itself was fixed in w1: `uwsm-app -- xdg-terminal-exec --dir=<cwd>` runs as a transient user
scope that inherits the compositor's environment unchanged (w1/RevengerUwsm/report.md, rungs 1-7). So the
hotkey's hash inputs are exactly the compositor's `XDG_*` values — which is what §2 uses.

## 2. Independent recomputation of the key, and the comparison with line 1

Path lists rebuilt exactly as `make_paths` builds them (xdg-terminal-exec:143-171), from the compositor's own
environment read out of `/proc/<Hyprland>/environ` (20 keys: HOME, PATH, 18 `XDG_*`; `RevengerCache/w1-hash-recompute.txt`):

```
CONFIGS=~/.config/hyprland-xdg-terminals.list:~/.config/xdg-terminals.list:/etc/xdg/hyprland-xdg-terminals.list:/etc/xdg/xdg-terminals.list:/usr/local/share/xdg-terminal-exec/hyprland-xdg-terminals.list:/usr/local/share/xdg-terminal-exec/xdg-terminals.list:/usr/share/xdg-terminal-exec/hyprland-xdg-terminals.list:/usr/share/xdg-terminal-exec/xdg-terminals.list
APPS=/usr/share/applications/:/usr/local/share/applications/:~/.local/share/applications/
```

```
$ { echo 4; echo Hyprland; LANG=C LC_ALL=C ls -LRl <CONFIGS> <APPS> ; } | md5sum
d27b6b707781b8106c7b00390bdf2822      # == head -1 ~/.cache/xdg-terminal-exec
```

Two independent confirmations of the same number: my pipe (above, 13938 bytes / 224 lines of input, kept as
`RevengerCache/hash-input.txt`), and the resolver's own `gen_hash` reporting `got fresh hash
'd27b6b707781b8106c7b00390bdf2822'` in a cold run under that environment (`RevengerCache/w1-hash-recompute.txt`).
Only two `xdg-terminals.list` files exist in the eight config slots, so the listing is 2 file lines followed by
the three applications directories — the order matters and was reproduced, not guessed.

## 3. Warm run vs cold run, under the compositor's environment

Cache = a byte copy of the host file in a scratch `XDG_CACHE_HOME`; cold = an empty scratch `XDG_CACHE_HOME`
(`RevengerCache/w2-warm-vs-cold.txt`):

| run | cache decision | stdout |
|---|---|---|
| warm, no args | `cache is actual` | `Alacritty.desktop`, `~/.local/share/applications/Alacritty.desktop`, `alacritty` |
| cold, no args | `no cache data` | identical bytes |
| warm, `--dir=/home/vgpnk` (hotkey shape) | `cache is actual` | same + `--working-directory=/home/vgpnk` |
| cold, `--dir=/home/vgpnk` | `no cache data` | same + `--working-directory=/home/vgpnk` (the w1 capture showed `--working-directory=/tmp` for `--dir=/tmp`) |
| warm, `--print-cmd -- htop` | `cache is actual` | `alacritty`, `-e`, `htop` |
| cold, `--print-cmd -- htop` | cold | identical |

So the cache does not change the printed selection today, and `/usr/bin/xdg-terminal-exec` (mode 644 in the
lane pin; the installed copy, sha256 `89f2be9a…3127ac`, identical) behaves exactly like the pin.

**Provenance witness — the cache on disk was written by a launch, not by a capture.** The only code that strips
the `/./` marker from the entry path is the `--print-path` branch, `XTE__ENTRY_PATH=${XTE__ENTRY_PATH%%/./*}/${XTE__ENTRY_PATH##*/./}`
(xdg-terminal-exec:1342), and `save_cache` runs *later* (:1455). The host cache's line 3 is
`/home/vgpnk/.local/share/applications/./Alacritty.desktop` — with the marker. Reproduced both ways in a fixture:
a run with `--print-cmd` only saves `…/applications/./TermA.desktop`, a run with `--print-path --print-cmd` saves
`…/applications/TermA.desktop` (`RevengerCache/w3-cache-semantics.txt`, T3). [INFERENCE, high]: the last writer of
`~/.cache/xdg-terminal-exec` was a hotkey launch (or an equivalent run without `--print-path`), not any of the
round-47 captures, which all use `--print-id --print-path --print-cmd`.

## 4. Holes — where warm and cold can disagree, reproducible

**H1 — the key is metadata-only, so a content edit is invisible.** `ls -LRl` (xdg-terminal-exec:200) contributes
name, size and mtime; the *bytes* of the list file and of every `.desktop` entry do not enter the md5. Fixture:
seed a cache, rewrite `xdg-terminals.list` from `TermA.desktop` to `TermC.desktop` (same 14 bytes, mtime restored),
and the hash is unchanged — `cache is actual`, warm prints **TermA**, cold prints **TermC**. Worse, the same trick
hides cache-control: with a hash-valid cache present, a list file that now says `/disable_cache` plus `TermC.desktop`
is never read at all (`cache is actual`, TermA printed; the cold control prints `found '/disable_cache' directive`,
TermC). `RevengerCache/w3-cache-semantics.txt` T1, `RevengerCache/w4-directive-bypass.txt` T4.

**H2 — the cache's content is trusted beyond the hash, and the validated field is not the executed field.**
Re-validation is `command -v` of line 2 only (:274); the command that actually runs is line 11 (`XTE__EXEC_USEP`).
With the host's real hash line verbatim, a scratch cache whose lines 2/3/4/11 read `bash`,
`/nonexistent/Whatever.desktop`, `Whatever.desktop`, `bash` is accepted and prints all of it; and a cache whose
line 2 is the legitimate `alacritty` but whose line 11 is `bash` also passes and prints `bash`
(`RevengerCache/w6-forgery.txt` A, B). The entry path is never checked for existence. Any process running as the
user can therefore redirect what the hotkey launches without touching config — no hash recomputation needed.
(w1/ExecCache found the same acceptance for its own fixture; this seat confirms it against the host's live hash.)

**H3 — `PATH` is not in the key.** Two environments with the same `XDG_*` and the same listings share a cache even
if they can resolve different terminals; the cached command is re-checked (:274) but the *ordering* is not. Today
harmless: the single applicable candidate resolves to `/usr/bin/alacritty` under both the compositor's and the
shell's `PATH` (w1/RevengerUwsm, condition 1).

**H4 — the resolver's own identity is not in the key.** Only the literal `4` (xdg-terminal-exec:194) versions the
format. [INFERENCE] An upgrade that changes selection rules but ships the same `xdg-terminals.list` files (pacman
restores packaged mtimes) leaves the old cache looking current. Not observable today: installed and pinned copies
are `cmp`-identical at sha256 `89f2be9a…3127ac`.

**H5 — the cache write is non-atomic and forked.** `save_cache "$1" &` (:1457) opens `O_WRONLY|O_CREAT|O_TRUNC`
and writes the 190 bytes in 11 syscalls (`RevengerCache/w6-forgery.txt` C, `strace -y`). The failure mode of a
concurrent reader is benign, and was measured rather than assumed: a cache truncated to its first 3 lines is
rejected (`invalid cache data`) and the run falls back to a cold resolve with unchanged stdout, re-writing a complete
file (`RevengerCache/w2-warm-vs-cold.txt`, truncated-cache section). Low severity, recorded because C1 forbids host
cache writes.

**H6 — C1's frozen contract deliberately excludes the path the hotkey takes.** The counter's own words:
"resolver (a warm cache) and -h/--help are outside the contract" (quality/counters/c1-r47-terminal.py:56). Its
190 fixtures never seed a cache and never set `XDG_CACHE_HOME`/`XTE_CACHE_ENABLED` (only `XDG_CONFIG_*`,
`XDG_DATA_*`, `XDG_CURRENT_DESKTOP` appear; `case_env` forces a per-case `.rw/cache`, c1-r47-terminal.py:224), so
every oracle run is cold — measured, `RevengerCache/c1-fixtures.txt`: `cases: 190`,
`any case seeding a cache file: False`, `any case setting XDG_CACHE_HOME/XTE_CACHE_ENABLED: False`. Given H1/H2 that is a real coverage gap: a candidate can be TARGET_MET while differing
from the host's warm behaviour. It also means C1 cannot catch a candidate that reads `XDG_CACHE_HOME` itself.
(The two fixtures that never reach argument composition are safe: `l1-test-mode` passes `--test`, which exits
before `exec` (xdg-terminal-exec:1460-1464); `u5-print-content` exits at :1376.)

**H7 — C2 clause f cannot tell a capture from a fabrication, and does not check cache state.** Clause f demands
`resolver_sha256=<digest>`, ">= 3 XDG_* lines, and `observed=<path>`" (quality/counters/c2-r47-terminal-entry.py:69)
— all strings. Feeding the frozen function a hand-written receipt (public sha256 + three `XDG_*` lines) and a
hand-written three-line capture naming `PhantomTerm.desktop`, an entry this host does not select, returns **True**:

```
$ python3 -I probes/callf.py <throwaway-repo> <rev> <base>
PRED-C2-r47 … clause=f receipt=…/fab.md observed=…/fab-capture.txt selected=PhantomTerm.desktop …
clause_f returned: True
```

Neither provenance nor `--print-id --print-path --print-cmd` being the producer nor cache-coldness is checkable, so
a capture taken with a warm/stale/forged cache (H1, H2) is admitted identically to a cold one. Receipt:
`RevengerCache/w5-clause-f-fabrication.txt`; the fixture lives outside the lane and was never committed. Scope of
the hole: clause f alone — the same tree is still `TARGET_MISSED` on clauses b/c (no sources, no pins), so C2 as a
whole is not forgeable by this route (`RevengerCache/w5-clause-f-counter-run.txt`); what is unprotected is the
provenance of the capture that f promises to verify.

## 5. Answer to the assigned question, and its limits

- **Does the hotkey read the cache?** Yes. Cache enabled by default (:1172), no `XTE_*` in the compositor env, no
  cache directive in either list file, host cache present and its line 1 equal to the hash recomputed under the
  compositor's environment → `read_cache` returns 0 and the selection chain (steps 1-5) is skipped.
- **Is the cold capture equal to what the hotkey uses today?** Yes, byte-for-byte on stdout for every argument
  shape the hotkey uses (no args, `--dir=<cwd>`), and both resolve to `Alacritty.desktop` at
  `~/.local/share/applications/Alacritty.desktop` running `alacritty` plus `--class=`/`--title=`/
  `--working-directory=` slots.
- **Why that is an observation and not an invariant:** H1 makes the equality breakable by a metadata-preserving
  edit, H2 makes it breakable by anyone who can write the cache file, H3/H4 by `PATH` or a resolver upgrade. Any
  C1/C2 evidence about selection should therefore state *which* cache state it was taken in; the w1 ExecLive
  capture is cold (fresh `XDG_CACHE_HOME` per run), so it is the trustworthy side of the comparison.

Evidence limits: the `/./` provenance reading is inference from code plus a two-way fixture, not from the writing
process; the host cache's mtime moved during w1 (w1/RevengerUwsm observed 17:42→18:49), so only its content
(sha256 above) is used as evidence, never its timestamp.

## 6. Reproduce

```
# 1. cache state, read-only
stat -c '%n mode=%a owner=%U:%G size=%s mtime=%y' ~/.cache/xdg-terminal-exec; sha256sum ~/.cache/xdg-terminal-exec
# 2. key recomputation + warm/cold comparison (writes only under /fast/scratch/hyaku/mado-r47/RevengerCache)
bash probes/probe.sh ; bash probes/probe2.sh
# 3. cache semantics (metadata-only, forgery, writer shape, directive bypass)
bash probes/probe3.sh ; bash probes/probe5.sh ; bash probes/probe6.sh
# 4. clause-f fabrication proof (throwaway repo under scratch; never the lane)
bash probes/probe4.sh ; python3 -I probes/callf.py <that repo> <rev> <base-rev>
```

`probes/*.sh` are the exact scripts that produced the receipts (`w1-hash-recompute.txt`, `w2-warm-vs-cold.txt`,
`w3-cache-semantics.txt`, `w4-directive-bypass.txt`, `w5-*`, `w6-forgery.txt`, `c1-fixtures.txt`, `host-cache.txt`,
`hash-input.txt`, `quotes.txt`, `verify-quotes.txt`). Every quote above is re-checked by
`probes/verify-quotes.py`, which greps `quotes.txt` and re-reads the cited line from the source.

Safety: no terminal, gui, compositor verb, pacman or input injection; `/usr/bin/xdg-terminal-exec` runs were
`--print-id/--print-path/--print-cmd` only, each with `XDG_CACHE_HOME` in scratch; host cache and config trees
read-only; no git/jj mutation anywhere (the C2 fixture is a fresh `git init` in scratch with its toplevel asserted);
no tool installed or upgraded (nothing was needed); scratch removed after copies.
