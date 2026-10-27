# ExecFixturesV2 — C1 fixture set v2 (round 48 w1, BUILD)

Seat `ExecFixturesV2`. Deliverable: `.ufo/waves/round-48/w1/ExecFixturesV2/fixtures-v2.json` — **162 NEW cases**
(ids `v2-*`, none reused from `quality/counters/c1-r47-fixtures.json`) for the warm-cache path of
`xdg-terminal-exec` v0.14.3, every `expect` produced by **3 identical runs** of the pinned resolver plus an
independent **2-run verification pass** in a second work root (162/162 agree), and the **COLD answer** recorded for all
119 primed/pre-seeded cases.

| artifact | sha256 |
|---|---|
| `fixtures-v2.json` (201 284 B) | `faf5141d54c913df7f5175de927c871a25a6f2a364d423e45485712e4862f3f3` |
| `gen.py` (generator + verifier) | `8863d6e5b84c50e77e99aa2f17ba034e7f2ac06e04cea810f5a42b7de9aa612a` |
| pin (`.ufo/waves/round-47/fetch/xdg-terminal-exec`) | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` |

Lane base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. Nothing outside
`.ufo/waves/round-48/w1/ExecFixturesV2/` and this file was written; scratch
`/fast/scratch/hyaku/mado-r48/ExecFixturesV2/` was deleted at the end; no tool install, no pacman, no compositor
write, no terminal launch (every resolver run carried a `--print-*` option — asserted over the set: 0 cases without
one, 0 primes without one).

## 1. Class counts, resolver cache verdicts, and the differ count

The verdict column is the **resolver's own** `D:` line from a scored run with `XTE_DEBUG=1`
(`cache is actual` / `out-of-date` / `invalid cache data` / `no cache data` / `cache is disabled, removing` /
`reached cache line limit`; `error` = the script died on an unbound variable before the cache logic).

| class | n | verdicts | warm ≠ cold |
|---|---|---|---|
| WARM-HIT-DIFFERS | 36 | hit 36 | **36** |
| WARM-HIT-SAME | 18 | hit 18 | 0 |
| WARM-INVALID | 34 | stale 30, disabled 3, invalid 1 | 0 |
| MALFORMED | 28 | invalid 10, stale 8, hit 9, absent 1 | 6 |
| HOME-UNSET | 10 | absent 4, error 4, hit 2 | 1 |
| CACHE-DEFAULT | 1 | absent 1 | 0 |
| READDIR | 10 | absent 10 | 0 |
| H1 | 12 | absent 12 | 0 |
| H2 | 13 | absent 11, hit 2 | 2 |
| **total** | **162** | hit 67, absent 39, stale 38, invalid 11, error 4, disabled 3 | **45** |

`warm_differs_from_cold` is computed, not typed: the fixture's scored `expect` is compared with a fresh cold run of
the same tree and environment (`XDG_CACHE_HOME` pointed at an empty dir, no priming). **45 of the 45 warm-differ
candidates differ; the 36 WARM-HIT-DIFFERS members are exactly the same-size/same-minute edits where the cached answer
wins**, e.g.

```
v2-wd-01-exec-firstword    hit  out='foot\n--a\n'                 cold='feot\n--a\n'
v2-wd-06-argdir            hit  out='…--chdir=/srv\n'             cold='…--chdor=/srv\n'
v2-wd-16-tryexec-stub-removed hit out='foot\n--a\n'               cold=rc 1, empty
v2-wd-23-compat-strict     hit  out='…-e\nhtop\n'                 cold=rc 1, empty
v2-wi-04-entry-deleted     stale rc 1, empty                      cold=rc 1, empty   (deletion ⇒ listing change ⇒ invalid)
v2-h2-12-cached-option-cmd hit  out='-p\n'                        cold=rc 1, empty
v2-hu-08-home-unset-warm-differs hit out='foot\n--a\n'            cold='feot\n--a\n'
```

The per-case table (all 162 rows, expect + cold + verdict) is `fixtures-v2.summary.txt`; machine counts are
`fixtures-v2.receipt.json`.

## 2. Schema v2 as shipped (the freeze candidate)

Base = the round-47 schema (`id`, `class`, `env` with `$ROOT`, `files`, `exec`, `args`, `expect{rc,stdout}`), plus:

| key | type | meaning |
|---|---|---|
| `mtime` | int (epoch s) | pins `st_mtime` of **every** materialized file and directory (the hash is an md5 over `LANG=C ls -LRl` of the config/list and applications paths, pin `:179-215`) |
| `prime` | `{"args":[…]}` | one **warm-up** run before the scored run; the resolver's background `save_cache "$1" &` (`:1457`) must be waited for (see §3) |
| `after.files` | `{path: text|null}` | post-prime rewrite (`$ROOT` substituted) / `null` = delete; a path ending `/` creates a directory |
| `after.exec_add` / `after.exec_remove` | `[path]` | stub binaries added/removed after priming (nothing outside the hashed paths) |
| `after.env` | `{name: text|null}` | environment overrides applied to the scored run only (`null` = unset) |
| `after.mtime` | int | re-pin every file/dir after the mutations (same value as `mtime` keeps the hash valid) |
| `after.cache_lines` | `{"<1-based line>": text}` | replace a line of the **primed** cache file |
| `after.cache_sub` | `[[find,replace],…]` | exact substring edits of the primed cache |
| `after.cache_append` | `[line,…]` | append lines after the primed cache's terminator |
| `after.modes` | `{path: int}` | `chmod` after priming (`ls -l` mode column) |
| `cache` | text | pre-seeded cache file, **no priming**; `$ROOT` substituted. Used only where the hash is *meant* to be wrong (parse-shape cases): `read_cache` rejects bad shapes before it ever calls `gen_hash` (`:217-298`) |
| `unset` | `[name,…]` | removed **after** the harness sets `HOME`/`PATH`/`XDG_CACHE_HOME`/`LANG` |
| `cold` | `{rc,stdout}` or `null` | recorded cold answer (same tree + env, empty `XDG_CACHE_HOME`, no prime) |
| `meta.files_order` | `[path,…]` | **materialization order** (see §5, READDIR); absent = object order |
| `meta.readdir_order` | `{dir:[names]}` | observed directory order on the materialized tree |
| `meta.cache_state` | enum | the resolver's own verdict (`hit/stale/invalid/absent/disabled/error`) |
| `meta.warm_differs_from_cold` | bool | computed |
| `meta.fs`, `meta.probe`, `meta.note`, `meta.cache_dir` | | filesystem (`xfs`), how the cache arose (`prime`/`cache`/`cold`), one-line purpose, `cache_dir:"home"` for the one default-path case |

`expect` is always the scored run's `(rc, stdout)` with the case root replaced by `$ROOT`; stderr is not part of the
contract (as in r47). No `$HASH` token is needed anywhere: warm hits come from real priming, and the only synthetic
caches are shape cases whose hash is deliberately wrong, or edits of a primed cache that keep the real hash.

## 3. How the warm answers were produced (own harness) — and the instrument fact it exposes

I built my own harness (`gen.py`); ExecOracleV2's seat held only a placeholder note when I checked it
(`.ufo/waves/round-48/w1/ExecOracleV2.md`, 20:43), so nothing was reused. The sandbox is copied byte-for-byte from
`quality/counters/c1-r47-terminal.py` `Box.argv` (same 7 externals at `/oracle/bin`, `/usr/lib` ro, host bash as
`/bin/sh`+`/bin/bash`, `/dev`, `/proc`, tmpfs `/tmp`, case root ro with only `<root>/.rw` rw, no `/etc` ⇒ numeric ids,
`PATH=<root>/bin:/oracle/bin`, `HOME=<root>/home`, `XDG_CACHE_HOME=<root>/.rw/cache`, `LANG=C.UTF-8`).

**F1 — the background save cannot land if the resolver is PID 1.** `save_cache "$1" &` (`:1457`) is killed when the
PID-namespace init exits. Measured (`probe-prime.py` → `prime-receipt.txt`): pin as PID 1 **0/6** cache files; pin
under a `/bin/bash -c` parent that outlives it and polls for the terminator **6/6**. The priming recipe is shipped as
`prime-wrap.sh` (bash builtins only — the sandbox PATH has no `sleep`, `wc`, `seq`; poll with `$(<file)` and
`EPOCHREALTIME`). Scored runs still use the pin as PID 1, exactly like the counter.

**Determinism.** Each `expect` was produced by 3 independent trials (fresh tree each, own root, own prime), all three
`(rc, stdout)` identical and all three `readdir_order` observations identical, else the case is dropped (0 dropped).
Then `gen.py --verify` re-resolved the whole file in a **second work root** with 2 more trials → `VERIFY: 162/162
agree`. The final set was generated twice, byte-identical (`faf5141d…` both times), and the earlier 161-case revision was
likewise byte-identical across its two runs, so `expect` depends only on the pin and the fixtures file.

## 4. Findings that constrain the freeze (each with its evidence row)

**F2 — an mtime bump inside the same day is invisible to the hash.** `ls -l` prints "Mon dd  YYYY" for files older
than six months, so with the seed epoch `1577836800` a delta of 59 s … 86340 s leaves the listing byte-identical and
the cache stays a **hit**; +86400 s makes it **stale**. Receipt: `mtime-receipt.txt` (probe `probe-mtime.py`):
`delta=0..86340 state=hit`, `delta=86400 state=stale`. Consequence for the freeze: an `mtime` invalidation fixture must
cross a day boundary (or use a recent epoch, which would make `expect` time-dependent); `v2-wi-01/06/11` move by
86400 s. It also means the same-size/same-minute edits used by WARM-HIT-DIFFERS are stable by construction.

**F3 — a cache whose terminator line has no trailing newline is rejected.** bash's `while read` never runs the body
for an unterminated last line, so `:217-298` never sees the terminator: `v2-mf-12-no-final-newline` → `invalid cache
data` (not "accepted"). Conversely a terminator on line 10 is not parsed (`v2-mf-02`, invalid), line 11 is the minimal
accepted shape (`v2-mf-03`), and the line-50 limit trips before any hash work (`v2-mf-10/11` → `reached cache line
limit`).

**F4 — under clause i's mounts the default cache path is unwritable.** `<root>` is bound read-only except `.rw`, so a
prime that wants `$HOME/.cache/xdg-terminal-exec` fails (`mkdir … Read-only file system`, observed while building
`v2-wd-37`, which was therefore not shipped). The default-path answer is observable only with an empty `$HOME/.cache`
→ `v2-wd-38-default-cache-absent` (class `CACHE-DEFAULT`, `no cache data`). If the C1 contract promises the default
path, the counter cannot observe a *warm* default-path answer without widening clause i's writable set.

**F5 — the hash is blind to some environment edits.** Adding a **nonexistent** path to `XDG_DATA_DIRS` adds no `ls`
output, so the cache stays a hit (`v2-ws-18`, hit, output equal to cold); adding an **existing** applications dir does
invalidate (`v2-wi-14`, stale). Likewise the list files' *contents* are not hashed at all — only their names, sizes
and dates — which is what every `v2-wd-1x-list-*` case exploits.

**F6 — `/disable_cache` in the list is invisible to a warm hit.** The directive is only read on the cold path
(`:374-398`); a warm run never calls `read_config_paths`. `v2-wd-25` primes with `/enable_cache ` (trailing space is
trimmed by `read`, same byte length as `/disable_cache`), rewrites the directive *and* the entry's Exec in one
same-size edit: warm prints the cached `foot --a`, cold prints `feot --a`.

**F7 — `HOME` unset requires three XDG vars.** With `HOME` unset the script still dies on the first *unset* XDG
default because bash expands `${X:-${HOME}/…}` only when `X` is unset: `:148` (config), `:166` (data), `:172` (cache).
So `v2-hu-01` (all three set) resolves; `v2-hu-02/03/04/05` exit 1 with empty stdout and stderr `<NAME>: unbound
variable` (`meta.cache_state=error`, verdict line never printed). That is the exact shape of the round-47 D1 closure,
and it is narrower than "HOME unset ⇒ rc 1": HOME unset **with** the three XDG vars set behaves normally, including a
warm hit (`v2-hu-07/08`).

**F8 — H1 and H2 reproduce the round-47 w2 shapes inside the current sandbox.** H1: a *directory* named
`foot.desktop` in a higher-preference applications dir shadows the valid file in the first operand; `find -L … -type f
( -path d1 ) -o ( -path d2 )` applies the type test only to the first dir → `read: 0: read error: Is a directory` →
rc 1, empty stdout (`v2-h1-01..04, 07, 11`); a shadow in the *first* dir is filtered and the home file wins
(`v2-h1-06`); a nested entry becomes id `foot.desktop-x.desktop` and can win the fallback order (`v2-h1-05, 09`).
H2: `command -v` parses an option-like operand as its own option, so `Exec=-p`, `-pv`, `-pV`, `--`, `-v x` and
`TryExec=-pv/-v` are **accepted** (rc 0, the word printed verbatim), while `-q`, `-`, `--foo` are rejected
(`v2-h2-01..11`); with a cache, a cached cmd `-p` keeps the hit while a cold run with `-q` fails
(`v2-h2-12/13`).

**F9 — cache line 2 is only a gate; it is not the command.** `read_cache` uses the cached `exec[0]` solely for
`command -v` (`:274`); the printed command comes from the cached `EXEC_USE P` line. Rows `v2-ws-10`, `v2-ws-17`,
`v2-mf-29` change line 2 (`printf`, `ls`, `-p`) and the stdout is **unchanged**, so a counter that compares only
stdout cannot see it — this is exactly the `CritC1Explain` hole: `explain` must keep comparing `cmd=` (and the
`--observed` capture's third item).

**F10 — other parse/verdict rows worth freezing as-is.** Junk before the terminator is accepted and becomes part of
the command (`v2-mf-19` → prints `JUNK`); bytes *after* the terminator mean no terminator is ever seen (`v2-mf-20`
invalid); lines after the terminator are never read (`v2-mf-26/27`); a cached cmd that is a shell builtin or an
option-like cluster keeps the hit (`v2-mf-21`→removed as duplicate of `v2-ws-10`, `v2-mf-29`); an empty line 2 makes
`command -v ""` fail (`v2-wi-29`); a lying cached path is printed verbatim by `--print-path` (`v2-mf-22`); an empty
cached id prints just the delimiter newline (`v2-mf-23`); a cached action suffix is appended to the printed id
(`v2-mf-24`); CRLF breaks the terminator (`v2-wi-31`, `v2-mf-25`) but a CR *inside* a cached arg is delivered into the
command (`v2-mf-28`).

## 5. READDIR (D3) — recorded order and filesystem

Ten cases put two or more valid candidates in one applications dir with **no list file**; the winner is the *last*
entry of that directory's readdir order, because `find` emits readdir order and each id is prepended to
`XTE__FALLBACK_ENTRY_IDS`. Recorded per case in `meta.readdir_order`, e.g.

```
v2-rd-01-foot-kitty   {'home/.local/share/applications': ['foot.desktop','kitty.desktop']}      → kitty.desktop
v2-rd-06-reverse-create ['konsole.desktop','ghostty.desktop'] (created konsole first)          → ghostty.desktop
v2-rd-05-three        ['foot.desktop','kitty.desktop','aaaa.desktop']                          → aaaa.desktop
v2-rd-09-two-dirs-both duplicate id in usr/share and home → home (later operand) wins          → …/foot --home
v2-rd-10-subdir-ids   nested a.desktop/b.desktop → id 'a.desktop-b.desktop'
```

Filesystem: **xfs** (`/fast`, `meta.fs` for every case) and the order is **creation order**; it was identical across
all trials, across two work roots and across the three generations. To keep this stable a checker must materialize in
`meta.files_order` (shipped for the nine multi-entry READDIR cases), not in sorted key order — sorting would flip the
winner and the `expect` drift check would fire. If the counter sorts, these ten cases are a setup error, not a pass.

## 6. Wiring checklist for the C1 counter (what the freeze has to say)

1. **Prime both trees.** Clause f's two-tree rule must extend to warm fixtures: materialize bytes, mtimes and
   creation order identically in the oracle tree and the tool tree, prime **each** with `prime-wrap.sh`, apply the
   same `after` mutations, then run. Priming only the oracle would compare a warm oracle against a cold tool.
2. **Re-pin mtimes** after `after.files` (the `after.mtime` value), else the ≥1 s write gap makes the hash stale.
3. **`cache` literals carry a deliberately wrong hash** (parse-shape cases). `expect` for those is the cold answer;
   that is the point, and the drift check passes because the pin re-derives the same verdict.
4. **`unset` is applied last** (after `HOME`/`PATH`/`XDG_CACHE_HOME`/`LANG` are set by the harness).
5. **Compare stdout+rc only** (r47 contract), and keep `explain`'s `cmd=`/observed third item (F9).
6. **The tool must not write**: `XDG_CACHE_HOME` in the tool tree is writable in clause i, and the F4 finding of
   `SentC1Sandbox` shows a tool write can leak into a later counter run — one tree per run, as r47 already does.
7. New cases are additive: the r47 `expect` records are untouched; this set is a separate file for the r48 counter,
   not a replacement of `c1-r47-fixtures.json`.

## 7. Routed round-47 items touched

| item | where |
|---|---|
| D1 (HOME unset modelled as the pin) | `v2-hu-01..10`, with the `:148/:166/:172` mechanism in §4 F7 |
| D3 (readdir-order blind spot) | `v2-rd-01..10` + `meta.files_order` / `meta.readdir_order` (§5) |
| M47-10 (fixture schema v2, H1/H2) | schema in §2; `v2-h1-01..12`, `v2-h2-01..13` |
| `CritC1Explain` (explain `cmd=` not compared) | `v2-ws-10`, `v2-ws-17`, `v2-mf-29` (line 2 changed, stdout unchanged) |
| `SentC1Sandbox` F1-F4 | §6.6 (one tree per run, tool must not write); F1/F2 also shaped my `prime-wrap.sh` choice |

## 8. Reproduction

```sh
S=/fast/scratch/hyaku/mado-r48/ExecFixturesV2
L=/home/vgpnk/Projects/shokunin/mado-shokunin
G=$L/.ufo/waves/round-48/w1/ExecFixturesV2
mkdir -p $S/work $S/work2
cd "$G" && python3 gen.py --work $S/work --out fixtures-v2.json --receipt fixtures-v2.receipt.json
cd "$G" && python3 gen.py --work $S/work2 --verify fixtures-v2.json --trials 2     # VERIFY: 162/162 agree
cd "$G" && python3 probe-prime.py     # prime-receipt.txt  (direct 0/6, wrapped 6/6)
cd "$G" && python3 probe-mtime.py     # mtime-receipt.txt  (same day = hit, +1 day = stale)
```

`gen.py` refuses a `--work` outside `/fast`, drops any case whose trials disagree, and writes the counts/hashes receipt
next to the set.

## 9. Risks and open questions for the freeze

1. **The priming wrapper is part of the instrument**, not of the tool contract: a counter that primes without it gets
   0/6 caches (F1) and every warm fixture becomes a drift error. `prime-wrap.sh` is shipped; W2 should attack it
   (e.g. a wrapper that returns before the save, or a resolver run whose cache is removed by `/disable_cache`).
2. **Clause i makes `$HOME` read-only**, so the default `$HOME/.cache` *warm* answer is unobservable (F4). Either the
   contract says the default path is modelled but not judged, or clause i must bind a writable `$HOME/.cache`.
3. **READDIR expects depend on creation order** (§5). Freeze `meta.files_order` as normative or drop the ten cases.
4. **`mtime` semantics** (§4 F2): fixtures pin an old epoch; a counter that seeds "now" instead would turn every
   WARM-HIT case into a stale-cache case. The `mtime` field must be honoured exactly.
5. **No `explain` expectations are embedded** in this file. `expect` is the print-mode answer; the explain clause must
   be generated by the counter itself from the same primed trees (and must keep the `cmd=` comparison, F9).
6. **Dropped for cause, recorded here**: `v2-wd-37` (default-cache-path warm prime) — impossible under clause i (F4);
   `v2-mf-16` (duplicate of `v2-mf-03`); an early `Type=` key edit that the resolver does not read (replaced by the
   key-degradation rows `v2-wd-20`, `v2-wd-36`).
