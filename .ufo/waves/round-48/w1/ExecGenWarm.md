# ExecGenWarm — C1 clause g v2: a nonce generator of warm-cache cases, judged by the pin at count time

Round 48, wave w1 (BUILD). Seat output for the L1's instrument freeze. Base rev `579f694b45c797a9c39761fdb4f9e0a1b71b3585`;
judge = the pinned resolver `.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256 `89f2be9a…3127ac` (= the host's
`/usr/bin/xdg-terminal-exec`, `receipts/env.txt`). No frozen predicate is scored here.

## 1. Deliverable (all under `.ufo/waves/round-48/w1/ExecGenWarm/`)

| file | role | sha256 |
|---|---|---|
| `gen_warm.py` | **the generator**: `gen_warm_case(rng, k)` -> one fixture-schema-v2 case | `ca0b2d7e0466f09e3da1576e8705db3d870dda97f82a48cf4f237134ad518062` |
| `warm_judge.py` | seat-local driver: materialize/prime/mutate/judge the pin 3x, the cold answer, and the round-47 tool | `113708e9…68f6ca` |
| `strict_probe.py` | seat-local probe: two prerequisites a case must satisfy before a prime can write a cache | `56f73a14…81f8a9` |
| `receipts/env.txt` | base rev, pin/tool sha256, python 3.14.8, bwrap/strace, generator sha | `113a053f…60fa71` |
| `receipts/determinism.txt` | 300 cases x 3 fresh-tree runs | `1f2ef6e8…e2a76e` |
| `receipts/mix.txt` | measured cache verdicts + per-family table | `a78e7699…660043` |
| `receipts/base-tool-miss.txt` | the round-47 tool (cold-only) vs the warm pin | `2b39bd3c…72ba6d` |
| `receipts/cases.txt` | one line per case: family, measured verdict, warm-vs-cold, tool match, prime state | `6cbafd95…13fa68` |
| `receipts/cases-sample.json` | the first 12 generated cases verbatim | `0434a644…ba762a` |
| `receipts/prime-mechanism.txt` | why a warm judge needs a prime wrapper (3 + 3 runs) | `ee940048…cf8c5d` |
| `receipts/prime-requirements.txt` | why entries carry `TerminalArgExec=-e` and why cache directives are stripped | `22aea433…3a0d3` |

Reproduce (scratch under `/fast`, receipts beside the seat):

```
python3 gen_warm.py --n 300 --seed 4801                       # print the cases (self-checked)
python3 warm_judge.py --n 300 --seed 4801 --work <fast/scratch>/w --receipts receipts
python3 strict_probe.py <fast/scratch>/strict receipts
```

## 2. The generator

`gen_warm_case(rng, k)` is a pure function of `(rng, k)`: it draws a round-47 `gen_case(rng, k)` base
(`quality/counters/c1-r47-terminal.py:349`, imported by path from beside the generator or an ancestor's
`quality/counters/`), so all the cold-path variety round-47's clause g bought is kept, and then adds the cache layer.

**Schema v2 produced** (round-47 fields unchanged, plus):

```
mtime: <epoch>                 pinned on every materialized file AND dir; only dates older than six months are used,
                               so `ls -l` always prints "Mon dd  YYYY" and nothing depends on when the counter runs
prime: {"args": [...], "env": {...}}   a cold oracle run before the scored run; env overlays the case env for the
                               prime only; after it the harness must wait until the cache file is complete and re-pin
                               `mtime`
after: {"files": {rel: text|null}, "exec_add": [...], "exec_remove": [...], "env": {...}, "mtime": <epoch>,
        "cache": [{"op": "set", "line": N, "text": T} | {"op": "append", "lines": [...]} |
                  {"op": "truncate", "keep": N} | {"op": "write", "text": T}, ...]}
                               mutations after priming, then `after.mtime` (default: the case mtime) re-pins the tree.
                               Tokens in any text: $ROOT, $CACHE_HASH (line 1 of the primed cache), $USEP (0x1f),
                               $RS (0x1e)
cache: "<literal text>"        a cache file written INSTEAD of priming (malformed / unusable caches)
```

Two schema additions were **required by the subject matter**, not stylistic:

- `prime.env` — a cache can only exist if the cold run saves one, so "cache disabled at prime time" is only
  expressible through the prime's environment (`XTE_CACHE_ENABLED=false`, pin `:1172`).
- `after.cache` with `$CACHE_HASH` — a literal cache text cannot contain the right hash: the hash is an md5 over
  `ls -LRl` output that embeds the case root's absolute paths (pin `:179-215`), so it is knowable only after priming.
  Without these ops, "the cache is trusted but its content is wrong" (the sharpest warm-cache case) is inexpressible.

`check_case()` enforces: exactly one of `prime`/`cache`; every `args`/`prime.args` vector contains a print option or
`--test` (the judge never launches a terminal); no absolute path and no `..` in any path the case writes; only
2024-epoch mtimes.

Three construction rules the receipts justify:

1. **A guaranteed selectable entry.** One injected entry `<n>.desktop` in `usr/share/applications/` with
   `Categories=TerminalEmulator`, `TerminalArgExec=-e`, `TerminalArgTitle=-T=`, `Exec=<n>`, `TryExec=<t3>`, and stubs
   `bin/<n>`, `bin/<twin>`, `bin/<t3>` present. Without `TerminalArgExec` a list line `/execarg_strict` (pin `:394`)
   makes the resolver skip it (pin `:1091`), nothing is selected, and **no cache is written** — measured 3/3 primes
   fail (`receipts/prime-requirements.txt`).
2. **`<n>.desktop` is the first line of every list file** (a list file is created when the base has none), so the
   prime selects the injected entry and the warm answer is a function of that entry; the base's list noise stays
   behind it. Without this, the prime usually selected an unrelated base entry and the mutations never bit.
3. **`/disable_cache` and `/enable_cache` are stripped from base list files**: such a line makes the cold run remove
   the cache (`save_cache` `:300`, `:380`), so the tree cannot be primed at all (measured 3/3,
   `receipts/prime-requirements.txt`). The directive families are generated explicitly instead (a same-size content
   swap while the cache is valid, and `XTE_CACHE_ENABLED` in the environment).

Family draw (top split 20 % literal / 5 % disabled / 37.5 % keep-the-hash / 37.5 % break-the-hash):

- **keep the md5** (content edits of equal byte length + re-pinned mtime, a same-day mtime shift, a stub removed from
  a directory that is not a hashed operand, cache line edits): `exec-swap`, `cache-tamper` (7 sub-variants),
  `titlearg-swap`, `disable-cache-same-size`, `tryexec-stub-gone`, `categories-corrupt`, `mtime-same-day`,
  `unrelated-stub-gone`.
- **break the md5** (added / removed / renamed / resized files, a mode change, a new directory, a changed mtime DAY,
  a changed `XDG_CURRENT_DESKTOP`): `shadowing-list`, `exec-size-change`, `new-subdir`, `mtime-next-day`,
  `desktop-env-change`, `inert-desktop-added`, `higher-pref-desktop`, `entry-renamed`, `mode-change`,
  `cache-removed`, `list-removed`.
- **disabled**: `XTE_CACHE_ENABLED=false` after priming, `=0`, and at prime time.
- **literal cache**: empty, no terminator, 49-line no-terminator, 50 lines (line limit, pin `:240`), garbage hash,
  sentinel on line 10 (never seen).

## 3. What the judge must do (obligations for the freeze)

- **Prime through a wrapper that keeps the sandbox alive.** The round-47 bwrap argv (`--unshare-all`, so the resolver
  is PID 1 of a new PID namespace; `quality/counters/c1-r47-terminal.py:139`) kills the resolver's background
  `save_cache "$1" &` (pin `:1457`): the cache file **never appears** (3/3 runs). Priming with
  `--ro-bind <work>/prime.sh /oracle/prime.sh` + `sleep` in `/oracle/bin`, running
  `/bin/bash /oracle/prime.sh <prime args>`, keeps PID 1 alive until the cache is complete (3/3). Everything else in
  the argv is the round-47 one byte for byte; the deployed command is still the pin
  (`receipts/prime-mechanism.txt`).
- **Wait for completeness, not existence**: non-empty and the last line ends with `\x1eEND_OF_EXEC_USEP`.
- **Two trees** (oracle / tool), primed and mutated identically, as in round-47 clause f; the tool must never see the
  oracle's cache. A third, never-primed tree gives the cold answer.
- **Classify with `XTE_DEBUG=1`** on the scored oracle run: `cache is actual` (pin `:275`), `cache is out-of-date`
  (`:287`), `invalid cache data` (`:291`), `no cache data` (`:295`), `reached cache line limit` (`:240`); "disabled"
  comes from a false `XTE_CACHE_ENABLED`. Debug output is stderr only and does not enter the hash.
- **Compare** the tool's `print` rc + root-normalized stdout with the oracle's; the measured verdict is reported, not
  required. A `prime` case that writes no cache is a setup error unless `prime.env` disables the cache.

## 4. Measured (300 cases, seed 4801; `receipts/determinism.txt`, `receipts/mix.txt`)

- **Determinism: 300/300 identical over 3 runs** on fresh trees, comparing `(rc, root-normalized stdout, measured
  verdict, root+hash-normalized cache bytes)`. Cache hashes are normalized because they are root-path dependent by
  construction (pin `:179-215`). Prime failures: 0/247; 3 primes ran with the cache disabled (no cache by design).
- **Mix:** `hit 112`, `stale 123`, `invalid 45`, `absent 9`, `disabled 11`. Among the 247 primed cases: 112 keep the
  hash (45 %), 115 break it (47 %), 6 delete the cache, 3 prime with it disabled, 11 read it disabled. The label ->
  verdict table in `receipts/mix.txt` has no surprise: every `keep:` family measures `hit`, every `break:` family
  `stale` (or `absent` for `cache-removed`), the literal ones `invalid`/`stale` (a garbage hash is a hash mismatch,
  not a parse error).
- **Warm answer differs from the cold one in 82/300** — exactly the 82 cache hits whose cached values (command,
  entry, arg names) are no longer what a cold run computes.
- **The round-47 tool (cold-only, `tools/mado-terminal.py` at the base rev, sha256 `b84d5c4f…de2222`) misses
  82/300** and equals the cold answer on 300/300 (`receipts/base-tool-miss.txt`): the misses are all
  `keep-exec-swap 28`, `keep-cache-tamper 18`, `keep-titlearg-swap 17`, `keep-tryexec-stub-gone 11`,
  `keep-categories-corrupt 8`. So clause g v2 at `GEN_W = 300` scores the base tool 218/300 and separates the warm
  path cleanly; it is not satisfiable by a cold model.

## 5. Findings that gate the freeze

- **F1 — the round-47 sandbox cannot produce a cache** (attacks: the round-47 argv as a v2 judge). Evidence:
  `receipts/prime-mechanism.txt` (direct 3/3 `cache=absent`, wrapper 3/3 `cache=complete`); mechanism: PID-namespace
  teardown vs. the background save at pin `:1457`. A v2 counter that primes with the round-47 argv verbatim would
  judge every "warm" fixture against a cold oracle.
- **F2 — a prime needs a selectable entry** (supports the generator's `TerminalArgExec=-e`): `receipts/prime-requirements.txt`
  variant 1 vs 2, 3 runs each.
- **F3 — a cache directive in a list file prevents priming entirely** (supports the strip rule): same receipt,
  variant 3 (stdout `foot`, rc 0, `cache=absent` 3/3).
- **F4 — the warm path is decided before any list is read** (supports the keep families): pin `:1179` gates the
  cache read ahead of `read_config_paths`; measured `keep-disable-cache-same-size` = `hit 13/13` even though the
  list file says `/disable_cache`, because a hit never reads it.

## 6. Proposed clause g v2 (text for `registration.md`, to be frozen by the L1)

> **g** `GEN_W = 300` cases drawn from NONCE by `gen_warm_case()` (`quality/counters/gen_warm.py`, which imports
> `gen_case()` from this counter). Each case is materialized twice (oracle, tool) exactly as clause f, with the case
> env, `files`, `exec` and `mtime` (pinned on every file and dir); a case with `prime` runs `prime.args` (overlaid by
> `prime.env`) through `/bin/bash /oracle/prime.sh`, waits until `$XDG_CACHE_HOME/xdg-terminal-exec` is non-empty and
> its last line ends with `\x1eEND_OF_EXEC_USEP`, and re-pins `mtime`; a case with `cache` writes that text instead.
> Then `after` is applied in order (`files`, `exec_add`, `exec_remove`, `env`, `cache` ops with `$ROOT`,
> `$CACHE_HASH`, `$USEP`, `$RS` substituted) and `after.mtime` (default: the case `mtime`) re-pins the tree. The
> oracle runs `args` with `XTE_DEBUG=1`, the tool runs `print args`; the case passes when the tool's exit status and
> its root-normalized stdout equal the oracle's. A `prime` case that leaves no complete cache is a setup error unless
> `prime.env` sets `XTE_CACHE_ENABLED` false. Clause g v2 prints the measured verdict mix
> (`hit/stale/invalid/absent/disabled`) and `generated=GEN_W/GEN_W` is required. The sandbox must leave `TZ` unset
> (the round-47 argv does: `--clearenv`, no `/etc`), so the pinned dates are read in UTC.

## 7. Limits, risks, owed

- `gen_warm.py` imports `c1-r47-terminal.py` by path (beside it, or an ancestor's `quality/counters/`). Freezing it
  beside the new counter is enough; if the L1 renames or moves the round-47 counter, the import path must follow.
- The keep families rely on GNU `ls` printing day-granular dates for old files and on the sandbox running in UTC
  (no `/etc/localtime` is bound). `keep-mtime-same-day` shifts by +3 h around a 12:00 UTC anchor: safe for any
  offset in [-12 h, +9 h); the round-47 argv sets no `TZ`.
- `warm_judge.py` and `strict_probe.py` are **seat-local instruments**, not the frozen contract: the counter must
  carry the prime wrapper, the completion wait, the two-tree order and the `XTE_DEBUG` classifier itself. They are
  the executable definition of §3.
- The generator draws from the counter's NONCE at count time; seed 4801 here is only for reproduction. The case set
  is therefore not precomputable, but the *families* are fixed, so `expect` must be computed by the pin at count time
  (never typed) — as this seat did.
- Out of scope and untouched: `explain`'s `cache=` vocabulary (the v2 tool's clause x would use the same five
  verdicts this judge measures), the launch half of the resolver, and `-h/--help`.

## 8. Evidence index

Pin locators (computing `grep -n` over `.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256 `89f2be9a…`):
`:179` `gen_hash()`, `:217` `read_cache()`, `:223` `xte__line_limit=50`, `:240` line-limit rejection, `:274` hash +
`command -v` trust test, `:275/:287/:291/:295` the four verdicts, `:300` `save_cache()`, `:321` the cache `printf`,
`:374/:380` `/enable_cache` `/disable_cache`, `:394` `/execarg_strict`, `:885/:891` `TerminalArgExec` read,
`:1091` "if entry lacks TerminalArgExec", `:1113` `get_default_execarg`, `:1129` the `-e` default, `:1172`
`XTE__CACHE_ENABLED`, `:1179` the read gate, `:1180` `XTE__CACHE_USED=true`, `:1457` `save_cache "$1" &`.
Counter locators: `quality/counters/c1-r47-terminal.py:139` (`--unshare-all` argv), `:198` `materialize`, `:220`
`case_env`, `:349` `gen_case`. Tool: `tools/mado-terminal.py:82` ("Cache (out of contract)"). Surface:
`corpus/README.md:110` ("the warm-cache path" still open at base).

Every number above is produced by a receipt in `receipts/`; nothing is typed from expectation. Scratch
`/fast/scratch/hyaku/mado-r48/ExecGenWarm` was removed after the receipts were written; no file was written outside
this seat directory and the report, no process, socket or compositor call was made, and the pin ran only with
`--print-cmd`/`--print-*`/`--test` options and `XDG_CACHE_HOME` inside the scratch tree.
