# ExecRefCacheA — C1 reference A: the warm-cache path of `tools/mado-terminal.py` (round 48, w1 BUILD)

Seat: `.ufo/waves/round-48/w1/ExecRefCacheA/`. Base revision `579f694`. The tracked path
`tools/mado-terminal.py` is **not** touched (L1 integrates). Nothing is committed; nothing outside the seat dir
and `/fast/scratch/hyaku/mado-r48/ExecRefCacheA` (deleted at the end) was written.

## Deliverables

| path (under the seat dir) | sha256 | what |
|---|---|---|
| `mado-terminal.py` | `c4ed769e…` (`receipts/SHA256SUMS`) | copy of `tools/mado-terminal.py` @ `b84d5c4f…` plus the warm-cache model (1705 lines; selftest **71/71**, also 71/71 inside the sandbox with `TMPDIR=/tmp`) |
| `receipts/agree.txt` | | 72 warm-cache cases: case, ours, theirs, cold, cache state |
| `receipts/lsdiff.txt` | | `ls -LRl` emulation differential (120 + 120 trees) and `gen_hash` composition (24×6 desktops) |
| `receipts/r47-replay.txt` | | all 190 round-47 fixtures replayed against the draft |
| `receipts/explain-states.txt` | | the five `cache=` states from real primed trees |
| `receipts/isolation.txt` | | strace: no process, no socket |
| `harness/{harness,warm,replay47,demo,make_agree}.py` | | the differential harness (runs from a scratch dir with `import harness`) |
| `pins/{ls.c,ls12.c,human.c,PINS.txt}` | | fetched sources + URLs + sha256, host binary hashes |

Run: `python3 -I mado-terminal.py --selftest`, `print …`, `explain [--observed FILE]`. Python 3 stdlib only.

## The contract implemented (all line numbers are `/usr/bin/xdg-terminal-exec` v0.14.3, sha256 `89f2be9a…`)

Cache file `$XDG_CACHE_HOME/xdg-terminal-exec` (`XDG_CACHE_HOME` default `$HOME/.cache`), computed in
`Resolver.make_paths` (:785) exactly where x:172 assigns it. `Resolver.select` (:1161) asks
`check_bool($XTE_CACHE_ENABLED)` (unset = true, x:1174) and then `read_cache` (:1100) — **before** any list or entry
is read, so `/enable_cache` and `/disable_cache` are cold-path-only, exactly as x:1179-1184 orders it.

`read_cache` models x:217-298: `[ -f ]` first (a directory or FIFO at that path is *absent*), then the
`while IFS= read -r` parse — lines 1-10 into hash/cmd/path/id/action/execarg/appidarg/titlearg/dirarg/holdarg, the
`"$xte__line_limit")` arm at line 50 rejected **before** the accumulate arm (so a terminator on line 49 parses and on
line 50 does not, x:223-254), line 11+ accumulated with `\n` joins until a line *ending* in `\x1eEND_OF_EXEC_USEP`.
A last line without a trailing newline is not seen by `while read`, so such a terminator counts as missing. Verdicts:
`hit` = hash equal and `command -v <line 2>`; `stale` = parsed but hash differs, cmd gone, or `gen_hash` failed;
`invalid` = parse failed; `absent` = no regular file; `disabled` = the gate is off/unparseable.

`gen_hash` (:715) is `md5("4\n" + $XDG_CURRENT_DESKTOP + "\n" + ls -LRl <colon-split XTE__CONFIGS:XTE__APPLICATIONS_DIRS>)`
— no process, no socket: `ls_lrl` (:621) computes the bytes from stat data.

Warm-path state assignment: `entry_path/id/action`, the `\x1f`-joined Exec words, `execarg` (which also drives the
`-e | "$XTE__EXECARG"` option arm and the "prepend execarg if args remain" rule), `appidarg/titlearg/dirarg/holdarg`.
Every `print` mode then composes from the cached values, `--print-path` folding `/./`, `--print-content` reading the
*cached path* (a failed read is `shcat`'s failed redirection under errexit: partial stdout, exit 1). No cache is ever
written, unlinked or renamed on these paths (all writes in the file are inside the selftest block at :1334+).

`explain` prints the round-47 line shape with five markers in order and a value that is always one of
`absent|hit|stale|invalid|disabled` (:1305-1330). HOME (or the XDG default) unset: `Exit(1)` from `make_paths` (:785)
models bash's `set -u` death — `print` exits 1 with empty stdout, `explain` reports `cache=absent … verdict=NO_TERMINAL`
exit 3 (convention agreed with `ExecCounterC1-2`, who scores that shape).

## `ls -LRl` emulation: the edge classes it had to handle

Computed (grep -n) locators in the draft; the GNU source is `pins/ls12.c` (host coreutils **9.12**, `ls` sha256
`29abfee0…`), with `pins/ls.c` (9.7) for the parts 9.12 kept.

1. **Per-block column widths**, not global: `nlink`, owner, group, size maxima over the *stat-ok* entries of one
   listing (`_ls_columns` :533); a stat failure contributes no width (ls12.c gobble_file early return). Owner/group
   `format_user_or_group` pads `width-name+1`, and a zero width still prints one space (the `do … while`).
2. **Unknown fields** (`_ls_line` :554): letter + 9 `?` (10 with an ACL column), `?` right-aligned per width, owner and
   group `?`+width spaces, size `?` right-aligned to the size width, date `?` right-aligned to
   `long_time_expected_width` (=12 in C locale). The type letter survives from readdir d_type: `l` for a dangling
   symlink or an ELOOP pair, `p` for a FIFO, `d`/`-` likewise (`_ls_dtype` :607, `os.lstat` first).
3. **Names are literal bytes** (non-tty default quoting is `literal`), and **coreutils 9.12 replaces every `\n` inside a
   printed name and inside a `dir:` header with `?`** (`qmark_newline`, ls12.c:2341 + 4499-4535; `-l` always qualifies).
   That is the single 9.12-specific rendering difference from 9.7, and it is what made two fixture-style trees hash
   differently until I modelled it. Non-UTF-8 and multi-byte names are emitted byte-exact (no locale re-encoding).
4. **Headers and separators** (ls.c:3068-3090, 1852-1855): with `-R` every directory gets a `name:` header, the header
   is dropped for a directory that cannot be opened, a blank line separates directory blocks, and the command-line
   file block is followed by a blank line only when directories follow.
5. **Operand order**: command-line args are stat'd (followed, `-L`), directories are queued and popped in ascending
   byte order; a failed operand is stderr only (ls.c:3345-3351). `dir/sub` is joined without doubling a trailing `/`.
6. **Recursion** (ls.c:3040-3062, extract_dirs_from_files): subdirectories are listed in the parent *and* recursed, a
   directory already on the active stack is reported and skipped (its header is not printed), and a marker pop makes a
   *sibling* symlink to the same directory legal.
7. **`total`** = `sum(st_blocks)` of stat-ok entries, `human_readable(n, opts=0, from=512, to=1024)` → `n//2` (exact
   divisor path, ls.c:210-221 + human.c:196-202); `POSIXLY_CORRECT` selects 512 and `LS_BLOCK_SIZE`/`BLOCK_SIZE` a
   spec, both modelled.
8. **Dates** (`_ls_date` :602): mtime, `recent = now-15778476 < when < now` (ls.c six_months), C-locale
   `%b %e %H:%M` vs `%b %e  %Y`, in the modelled `TZ`; `TIME_STYLE` `locale|iso|long-iso|full-iso|+FMT` supported,
   including `%N` (which Python's strftime lacks) and the `posix-` prefix dropped in the C locale.
9. **Special files**: `c`/`b` print `major, minor` with `major_width + max(0, size_width-(major+2+minor))` padding
   (ls.c:4417-4432); FIFOs and sockets print size 0.
10. **ACL column**: `any_has_acl` is per block; the flag column is `' '`/`+`/`.`/`?`. Probed: a mode-000 file does *not*
    set it here (EACCES goes to `ACL_T_UNKNOWN` only on NFS-like errors), so the sandbox shows 10-char modes.

## Evidence (each receipt is a run, not a claim)

- `receipts/lsdiff.txt`: **120/120** random trees agree byte-for-byte with the real `/usr/bin/ls -LRl` inside the
  counter-style bwrap sandbox (no /etc → numeric ids; LC_ALL=C LANG=C; TZ unset/UTC/Asia-Tokyo; trees with dangling
  and ELOOP symlinks, dir loops, 000/444/500 dirs, 000/4755/1777 files, FIFOs, odd names, old and recent mtimes);
  with FIFOs included, **115/120 + 5 declared residuals** (the FIFO letter of an entry inside an *unsearchable*
  directory: readdir d_type is unreachable through Python's `DirEntry`, which exposes only is_dir/is_file/is_symlink).
  `gen_hash` composition vs `{ printf '4\n%s\n' "$XDG_CURRENT_DESKTOP"; ls -LRl …; } | md5sum`: **24/24**.
- `receipts/agree.txt`: **72/72** warm-cache cases. Every case primes *both* twin trees with the pin (cold
  `--print-cmd`, bounded wait for the background save), mutates them identically, then runs the pin warm on one tree and
  the draft on the other. **18 cases** are ones where the warm answer provably differs from the same tree with the cache
  removed. States asserted per case and **all 72 match**: state histogram hit 38, stale 19, invalid 6, absent 5,
  disabled 4 (by class: hit 19, hit-differs 18, stale 19, invalid 6, absent 2, disabled 4, nohome 4 — the nohome
  cases have no state expectation; three model the `set -u` death, one runs with `XDG_CACHE_HOME` set).
  Covered: same-size+same-minute list swaps, TryExec stub removed, Exec/TerminalArg names edited same-size, multiline
  Exec, actions, cached appid/title/dir/hold, cached empty execarg, cached broken path, `/disable_cache` present at
  prime with the gate forced on, list/desktop/dir size+mtime+added+removed invalidation, `XDG_CURRENT_DESKTOP`
  changed/unset/empty/`:GNOME`, exec gone / exec not executable, hash wrong/uppercase, cmd empty/builtin/gone,
  no terminator / terminator at 5 / at 49 / at 50 / 10 lines / empty file / cache-is-a-directory / unterminated last
  line, gate false/0/garbage/empty-string, HOME unset (4 shapes), `XDG_CACHE_HOME` unset via `$HOME/.cache`.
- `receipts/r47-replay.txt`: **190/190** round-47 fixtures agree with the live pin, **0 recorded drift** — the cold
  path did not regress, and the recorded `expect` still describes this host's resolver.
- `receipts/explain-states.txt`: the five `MADO_TERM:` lines from real primed trees (`hit`, `stale`, `invalid`,
  `absent`, `disabled`) next to the pin's warm stdout.
- `receipts/isolation.txt`: `strace -f -e trace=execve,execveat,socket,socketpair,connect` around `print` and `explain`
  in the sandbox: python execve seen once, **0 traced events after it** (no process, no socket).
- `python3 -I mado-terminal.py --selftest` → `MADO_TERMINAL_SELFTEST: 71/71 passed` (43 round-47 + 23 warm + 5
  explain-state), hermetic under `$TMPDIR`.

### Independent score by the round-48 counter seat (not my own claim)

`ExecCounterC1-2` scored this draft with its own instrument
(`.ufo/waves/round-48/w1/ExecCounterC1/c1-r48-terminal-cache.py`, sha256 `8db736a7…`, 32 fixtures) in its own sandbox:
final draft `c4ed769e…` nonce 48 → `cold=190/190 warm=32/32 explained=222/222 generated=230/230 selftest=ok (71/71)
readonly=ok verdict=TARGET_MET` (also TARGET_MET on nonce 424242 for the previous draft `2894f7f8…`). The round-47 tool
at `579f694` scores `warm=22/32 … verdict=TARGET_MISSED` on the same instrument, missing on the warm-differs fixtures
plus the HOME-unset one. Their independent findings match mine: a plain sandboxed run of the pin leaves no cache
(`save_cache &` dies with the sandbox), so priming needs a waiter; and a 2020-pinned mtime makes a +7200 s change
invisible to `ls` (a date change needs a day boundary).

## Disagreements found while building this (all were mine; each is a trap for the counter)

1. A name containing `\n` prints as `nl?line` in coreutils 9.12, not raw and not `nl?line`-by-`-q` across the board.
2. Field padding for unknown entries is `max(0, width-len)+1` spaces, so a zero width still leaves one space.
3. A FIFO in an unsearchable directory is `p?????????` for ls and `??????????` for the model (declared residual).
4. `--print-content` on a cached path that has vanished exits **1** with whatever was printed before it (errexit on the
   redirection), not 0.
5. The pin at `.ufo/waves/round-47/fetch/xdg-terminal-exec` is mode 644: a sandbox that `--ro-bind`s it directly gets
   `Permission denied`. Copy it and `chmod 755` (the round-47 counter does; my harness initially did not).
6. The cache hash covers **absolute paths** (ls prints `dir:` headers), so a cache primed in tree A is stale in tree B.
   Twin-tree judging must prime each tree with the pin — which `ExecCounterC1-2` already does (its clause w).

## Notes for the freeze (fixture schema v2 as exercised here)

I used exactly the draft v2 shape and it is sufficient: `mtime` (every file and dir pinned, so dates are deterministic),
`prime: {args}` (a cold run, bounded wait for the background save), `after: {files, exec_add, exec_remove, modes, env,
mtime}`, and `cache: "<literal>"` (malformed caches, `$ROOT` substituted, no priming). Two additions that made cases
precise and that I recommend freezing: a per-case **`prime_env`** (prime with `XTE_CACHE_ENABLED=true` or a different
`XDG_CURRENT_DESKTOP`, score with the case's own env — without it the `disabled` and desktop-change cases cannot have a
cache to ignore), and an explicit **`primed: false`** (no cache file at all, distinct from an empty one).

## Risks / declared residuals

- FIFO/socket/device letter inside an unsearchable directory (d_type not exposed by Python's `DirEntry`): the model
  prints `?` where ls prints `p`/`s`/`b`/`c`. Only reachable if a fixture puts such an entry in a mode-444/000
  directory under a hashed path.
- Out of contract (unchanged from round 47 plus): `-h/--help`; a FIFO named like a desktop file in a later application
  dir; symlink loops on a *command line*; an empty-string argument; `:`/glob/quote in a default XDG dir or HOME; non-ASCII
  `\u`/`\U` delimiters; `QUOTING_STYLE` or any ls switch other than `-LRl` (the resolver passes exactly that); a
  `TIME_STYLE` with a second newline; `LS_BLOCK_SIZE` specs that are not a number with B/K/M/G; a modelled `TZ` that
  differs from the process `TZ` (rendered as UTC); a cache file that exists but cannot be opened (bash kills the
  resolver with 1 — modelled as `Exit(1)`, not exercised by a fixture here).
- The draft models stdout and exit status only; it never performs the resolver's background rewrite (so a repeated run
  after a stale/invalid state must be judged against a freshly primed tree, which is how the counter works).

## Cleanup

`/fast/scratch/hyaku/mado-r48/ExecRefCacheA` (trees, sandboxes, fetched sources) deleted; every receipt above was copied
into the seat dir first. `/tmp` was not used for fixtures. No pacman, no host service, no compositor, no terminal launch:
`xdg-terminal-exec` ran only with `--print-cmd` and only with `XDG_CACHE_HOME` inside the sandbox scratch; the host's
`~/.cache/xdg-terminal-exec` was never read or written.
