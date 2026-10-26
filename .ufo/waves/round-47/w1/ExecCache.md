# ExecCache — cache semantics of xdg-terminal-exec 0.14.3 (round 47, w1)

Scope: the resolver cache of `/usr/bin/xdg-terminal-exec` — what it stores, when it is read,
what invalidates it, and whether a stale cache can make it print a different entry than a cold run.
Feeds C2 (`corpus/knowledge/xdg-terminal-selection-r47.md`) and constrains the C1 contract, which
models a cold cache only.

Target pin: `/usr/bin/xdg-terminal-exec`, 1499 lines, sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (matches the L1 host fact;
byte-equal to upstream v0.14.3 per the L1 registration). All probes below ran this script only in
`--print-*` mode, with `XDG_CACHE_HOME` inside `/fast/scratch/hyaku/mado-r47/ExecCache`.

Method: `cache-probe.sh` (this seat dir) builds hermetic case roots (`$ROOT/{bin,home/.config,
home/.local/share/applications,usr/share/applications,etc/xdg,cache}`, stub binaries `term-a`,
`term-b`, two `TerminalEmulator` desktop entries, a two-line config list), runs the resolver under
`env -i` with the full XDG environment, and asserts output equality/divergence. **41/41 checks
passed** (`receipts/probe.log`, section E0–E8, `PROBE_RESULT: all checks passed`).

## Code map (line numbers in the pinned script)

| Range | What |
|---|---|
| 143–178 | `make_paths`: builds `XTE__CONFIGS` (config list files), `XTE__APPLICATIONS_DIRS`, and the cache path (171–173) |
| 179–215 | `gen_hash`: md5 of version constant + `XDG_CURRENT_DESKTOP` + `ls -LRl` of the two path sets |
| 217–298 | `read_cache`: parse, field mapping, validity test |
| 300–340 | `save_cache`: format, umask, newline guard, disable removal |
| 1169–1184 | bootstrap: cache-enable default and the read gate (`check_bool … && read_cache`) |
| 1325–1385 | print blocks; early bail-out that skips `save_cache` for id/path/content |
| 1455–1458 | `save_cache "$1" &` — only reached when `cmd` is in the print data (or a real launch) |
| 371–386 | `/enable_cache`, `/disable_cache` config directives (cold path only) |

## F1 — What is stored

One file, one slot: `${XDG_CACHE_HOME:-$HOME/.cache}/xdg-terminal-exec` (172–173). No argv/mode key;
one cache serves every invocation. Written with `umask 0077` → mode 0600 (319–320; observed
`mode=600` in `receipts/probe.log` E0/E8).

Layout (save printf at 321–332; sample from E0):

```
<hash>                     md5 from gen_hash
<exec[0]>                  first token of the expanded Exec (also the `command -v` check target)
<entry path>               XTE__ENTRY_PATH as it was at save time (may still contain "/./")
<entry id>                 e.g. TermA.desktop
<entry action>             empty when no "id:action" was requested
<execarg>                line 6 (e.g. -e)
<appidarg> <titlearg> <dirarg> <holdarg>   lines 7-10, often empty
<XTE__EXEC_USEP> RS "END_OF_EXEC_USEP"     line 11; RS = 0x1e; USEP-separated, LF records
```

Reader accepts at most 50 lines (223, 240); the command field runs from line 11 to the RS
terminator. Line 2 (the first Exec token) is only the `command -v` probe and the value handed to
`save_cache`; the command that is assembled, printed and exec'd comes from line 11. Sample valid
cache (E0, 175 bytes) in `receipts/probe.log`; a cache with a `X-TerminalArgTitle` entry in E6.
Parsing stops at the RS terminator (`break`, 250–253), so bytes after it are never read and the
50-line limit only bites when no terminator appears by line 50 (E3b). [INFERENCE for the
trailing-bytes half: code 250–253; only the limit case was run.]

## F2 — When it is read

The read gate is line 1179, after `make_paths` and **before** `read_config_paths` (351) and
`find_entry_paths` (754). Every mode passes it; print handling only starts at 1325. On a hit
(274–284) it restores `XTE__EXEC_USEP`, entry path/id/action and the five terminal-side arg values,
so list files and desktop entries are never opened. Evidence: a cold run's debug contains
`reading config …`; the warm run with `cache is actual` contains none (E0 checks).

On a miss it returns 1 and the cold path re-derives the whole selection, then (if the run reaches
line 1455) saves a fresh cache.

## F3 — Validity test: exactly two conditions

1. `gen_hash` equality (274). The hashed string is:

```
4 \n XDG_CURRENT_DESKTOP \n  $(LC_ALL=C LANG=C ls -LRl ${XTE__CONFIGS}:${XTE__APPLICATIONS_DIRS})
```

hashed with `md5sum` (180–200). Reproduced bit-exactly (`receipts/hash-formula.txt`:
`reproduced=6099b212… MATCH`). Notes:

- the config entries are the list-file *paths*; the application entries are the directories, each
  ending in `/` (143–178), so `ls -lR` headers and recursion cover the whole desktop-file tree;
- covered: file names, sizes, modes, **displayed** mtimes, symlink targets, directory contents,
  `XDG_CURRENT_DESKTOP`, and the hash version constant `4` (194);
- **not** covered: file contents, `PATH` composition, CLI arguments, print mode, and any env var
  not reachable through those two path sets;
- `ls -l` shows recent mtimes only to the minute, so a sub-minute mtime change is invisible (E5);
- timestamps are rendered in the ambient `TZ`, so a `TZ` change alone invalidates (E5, below).

2. `command -v "$xte__cached_cmd"` (same line 274) — only *presence* of the cached first Exec token
   on `PATH`, not its identity.

`receipts/verify-quotes.txt`: all 26 quoted locators verified on the exact cited lines.

## F4 — What invalidates (and what does not)

Invalidating, each observed:

| Trigger | Evidence |
|---|---|
| any metadata change in the listed tree, including displayed mtime (`touch -t 200001010000`) | E5 `displayed-minute mtime change invalidates cache` |
| `XDG_CURRENT_DESKTOP` change | E5 (`GNOME` → `cache is out-of-date`) |
| `TZ` change (hash renders timestamps differently) | E5 (`UTC` cache, `Asia/Tokyo` read) |
| cached cmd no longer on `PATH` | E3f (`cache is out-of-date`, re-resolves TermA→TermB) |
| truncated file, missing RS terminator, >50 lines, non-matching hash | E3a–E3d |
| cache version constant bump (code: `echo 4`) | code 193–194 |
| `XTE_CACHE_ENABLED=false` → file removed; `/disable_cache` on a cold path → removed | E4 |

Not invalidating, each observed:

| Non-trigger | Evidence |
|---|---|
| file **contents** edited with size and displayed mtime preserved | E2: `ls -LRl` byte-identical, `cache is actual`, output stale |
| `PATH` gaining/losing a binary other than the cached cmd (including one earlier in preference) | E1: hash identical before/after, `cache is actual` |
| CLI args (`--title`, `--dir`, command args) | E6: cached arg replayed, fresh value recomposed, same cache |
| which print mode is requested | one slot, no mode key (E0/E6) |

## F5 — Can a stale cache print a different entry than a cold run? **Yes — three proven cases**

(a) PATH-only change (realistic: installing a terminal). List order TermA, TermB; `bin/term-a`
absent → cold picks TermB. Create `bin/term-a` (not hashed) → warm run reports `cache is actual`
and prints TermB; remove the cache → cold prints TermA. Hash line is identical
`deb7da7aa64f974cf3aa8f135b6544dd` both times (E1). The stale cache also answers `--print-id`
alone (E1).

(b) Content-only edit with metadata restored. Rewrite the higher-preference entry's
`Categories=…` line as a same-length comment (`#ategories=…`), restore mtime with `touch -r`:
file is 93 bytes before and after, `ls -LRl` listing is byte-identical, warm run reports
`cache is actual` and prints TermA/term-a; cold run prints TermB/term-b (E2). This is the
corollary that `ls -l` hashes metadata, not content.

(c) Tampered cache. Keep line 1, replace line 2 (cmd), line 3 (path), line 4 (id) and line 11
(expanded Exec) → read_cache reports `cache is actual` and the run prints
`Evil.desktop`, `$WORK/…/Evil.desktop`, `term-evil`; cold prints `TermA.desktop`, its real path,
`term-a` (`receipts/forge-cache.txt`). In launch mode the cached `XTE__EXEC_USEP` is what gets
`exec`'d (code: 276 restore, 1447–1457 command assembly, 1499 `exec "$@"`; **not** executed in the probe).

So: whenever the world changes in a way the metadata hash cannot see, or the cache file is edited,
the warm path keeps printing (and would launch) the old selection until the hash moves.

## F6 — Corruption is safe for output, not for integrity

All corrupt forms fall back to the cold path and produce the cold stdout/exit status:
(a) 5-line truncation → `invalid cache data`; (b) 55 lines with no terminator →
`reached cache line limit (50)`; (c) wrong 32-hex hash → `cache is out-of-date`; (d) missing RS
terminator → `invalid cache data`; (f) cached cmd missing → `cache is out-of-date` (E3). If the run
reaches `save_cache`, a valid file is rewritten (or removed when disabled). Note that "valid" here
means only F3's two conditions — a well-formed forgery is accepted (F5c).

## F7 — Not every print mode writes the cache

The early bail-out at 1368–1385 exits for `--print-id`, `--print-path`, `--print-content` (and their
combinations) **before** line 1455, so no cache write. Only runs whose print data contains `cmd`
(or no print mode at all → launch / `--test`) reach `save_cache "$1" &` (1457). Observed: id / path /
content alone → no file; `--print-cmd` → file (E7). Consequence for capture workflows: a capture that
includes `--print-cmd` warms the cache it wrote; redirect `XDG_CACHE_HOME` (L1 host fact).

## F8 — The write is asynchronous and races

`save_cache "$1" &` (1457) forks; the parent continues and exits. Measured over 30 cold
`--print-cmd` runs: cache present immediately after exit **0/30**, present 50 ms after exit
**30/30** (E8). No lock, no fsync, direct `>` truncate+write. A second invocation in that window
either sees no cache (cold path) or, when replacing a stale one, the old content; concurrent
invocations race on the same file.

## F9 — Replay semantics

A hit replays the entry-derived state (entry id/path/action, the five terminal-side `X-TerminalArg*`
values, and the expanded Exec) while CLI values are recomposed on every run. E6: cache warmed with
`--title=First`, then run with `--title=Second` → `--title`, `Second` in the printed command; the
cache's `<titlearg>` line stays `--title`. Because the cache is not keyed on argv, `--dir/--title`
never invalidate it.

## F10 — Quirks worth recording in C2

- `--print-path` strips the `/./` find delimiter **in place** (1340–1342) before `save_cache` runs
  (1455). A cache warmed by a run that included `--print-path` stores the normalized path; a cache
  warmed by `--print-cmd` alone stores the raw `…/applications/./TermA.desktop` form. Printed
  `--print-path` output is normalized either way (E0 cache line 3 vs E6 cache line 3). Harmless for
  output, but the stored bytes differ by warming mode.
- Cache read precedes config parsing, so `/enable_cache` and `/disable_cache` (371–386) are only
  honoured on a cold path; the code comment (1169–1171) relies on config edits invalidating through
  the hash. By F3/E2, a config edit that preserves size and displayed mtime would never be re-read
  while the cache stays valid. [INFERENCE: composed from code 1169–1184 plus E2; not separately run.]
- Disabled cache is removed only when a run reaches `save_cache` (E4: removal after `--print-cmd`;
  no file is created by id/path/content-only runs).
- Default location when `XDG_CACHE_HOME` is unset: `$HOME/.cache/xdg-terminal-exec` (E4).
- The hash is md5, but the practical staleness vector is metadata blindness, not collision.

## Risks / hand-off

- **C1 (cold-cache contract)**: fixtures and the counter must give every case a fresh, empty
  `XDG_CACHE_HOME`. A `--print-cmd` case writes a cache ~50 ms after exit (F8); reusing one cache
  dir across cases whose stub `PATH` or desktop bytes differ can leak a stale selection into a later
  case (F5a/F5b). The Python re-implementation should refuse to model a warm cache and say so in
  `explain`; it must never read `$XDG_CACHE_HOME`.
- **C2 entry**: document the cache as an out-of-contract acceleration layer keyed on `ls -l`
  metadata, not contents; list the three divergence classes (PATH composition, content edit,
  tampering) and the minute-granular `ls -l` mtime.
- **Integrity**: the cache trusts lines 3/4/11 completely and validates line 2 only by presence on
  `PATH`. File mode 0600 limits other-user tampering; an attacker-controlled `XDG_CACHE_HOME` (or
  same-user write) can change the printed entry and the binary a real launch would exec.
  Code-read (276, 1447–1457, 1499) plus E3e; launch was **not** executed (host guard).

## Receipts (relative to this directory)

- `receipts/probe.log` — sanitized full run, 41/41 PASS, sections E0–E8 (`$WORK` = case root).
- `receipts/hash-formula.txt` — reproduced md5 equals cache line 1.
- `receipts/forge-cache.txt` — valid cache, forged cache, warm vs cold outputs.
- `receipts/verify-quotes.txt` — 26/26 cited lines verified by `verify-quotes.sh`.
- `cache-probe.sh`, `verify-quotes.sh` — probes and quote checker (take a work dir; honour `$WORK`).

Scratch: `/fast/scratch/hyaku/mado-r47/ExecCache` (deleted after the receipts were copied here).

Report: .ufo/waves/round-47/w1/ExecCache.md
