# ExecCounterC1 — C1 counter draft for round 48 (warm-cache clause)

Seat target: `.ufo/waves/round-48/w1/ExecCounterC1/c1-r48-terminal-cache.py` (copy of
`quality/counters/c1-r47-terminal.py`, extended) plus the fixture set it pins
(`.ufo/waves/round-48/w1/ExecCounterC1/c1-r48-fixtures.json`) and its builder
(`.ufo/waves/round-48/w1/ExecCounterC1/gen-fixtures-v2.py`). Base: `579f694b45c797a9c39761fdb4f9e0a1b71b3585`.
Nothing outside this seat directory was written.

STATUS: complete. Draft built, fixtures measured from the pin (3 identical runs each), scored against the round-47
tool at the round start (TARGET_MISSED on exactly the warm cases) and against ExecRefCacheA's warm-cache draft
(TARGET_MET), at two nonces each — section 5. No tool was installed, upgraded or run outside the counter's sandbox;
no host service, compositor, terminal or GUI was touched; `xdg-terminal-exec` ran only with `--print-*` and with
`XDG_CACHE_HOME` inside this seat's scratch (now deleted).

## 1. What changed against the round-47 counter

| round-47 | round-48 | why |
|---|---|---|
| one fixture file (cold), 190 cases | two: the round-47 file byte-identical (`SHA256_COLD`, clause f = the r47 cold clause verbatim) and a new 32-case file (`SHA256_WARM`, clause w) | harm watch: the r47 cold clause keeps its records and its verdict |
| fixture schema: id/class/env/files/exec/args/expect | plus `mtime`, `prime{args}`, `after{files,exec_add,exec_remove,env,unset,mtime}`, `cache`, `default_cache`, `unset`, `state`, `cold` | warm path needs a deterministic listing and a cache; `state`/`cold` are measured, never typed |
| the oracle's cache file never existed (a plain sandbox run left none) | each tree is primed by the pin itself, in a waiter that reaps the resolver's forked `save_cache` | `save_cache "$1" &` (pin :1455-1457) dies with the sandbox's pid 1, so the cache cannot be produced any other way |
| clause x compared selected= and path= | also cmd=, and cache= against the oracle's own decision; three captures (AGREE, first `.desktop` renamed, **first two items only**) | `w2/CritC1Explain.md`: a tool that drops or ignores the command line scored TARGET_MET |
| clause i said "without /fast", "only", and the `.rw` bind was writable for the tool | clause i is the enumerated mount set; the tool tree's `.rw` is READ-ONLY; `default_cache` adds one documented alias mount | `w2/SentC1Sandbox.md` F1, F2, F3, F4 |
| `explain_case` did `os.makedirs(<tool tree>/.rw/obs)` after the tool ran | `tempfile.mkdtemp(dir=<tool tree>/.rw)` + `O_EXCL|O_NOFOLLOW` captures, any OSError is a clause-x failure, never an abort | F4: a tool write could abort the count with a traceback and no verdict line |
| clause g: 150 cold generated cases | 150 cold (same generator) + 80 warm generated (kind hit/stale/invalid/disabled, premise measured) | the generated arm must reach the warm path too |
| `MADO_TERM:` parsed by splitting on whitespace | parsed by its five literal markers, in contract order | found while building: the r47 parser truncated `cmd=my term` to `my` (cold fixture `t6-exec-quoted-binary-with-space`), so cmd= could never have been compared |

## 2. The warm clause, as scored

Per fixture, per variant (A `LANG=C.UTF-8`, B `LANG=en_US.UTF-8`), on **three independent trees** (oracle, tool,
cold twin), prepared identically: materialize → pin `mtime` (files, then dirs deepest-first, `.rw` excluded) →
cache (`cache` literal, or `prime` = the pin run on that tree through a waiter that returns only when the cache ends
with `\x1eEND_OF_EXEC_USEP`) → `after` mutations → re-pin `mtime` → one scored run. Each tree's cache is its own
(the hash covers absolute paths, so a cache is only valid for the tree it was primed in). The oracle runs with
`XTE_DEBUG=1`; its debug stream is stderr only, so stdout and exit status stay the judge's, and `cache_state()` reads
the decision off the stream (`cache is actual` / `cache is out-of-date` / `invalid cache data` /
`reached cache line limit` / `no cache data` / none-but-`paths:` → disabled / none-and-no-`paths:` → absent).

The 32 warm fixtures, by class (each `expect`, `state` and `cold` measured, 3 identical runs, builder refuses to
write otherwise):

| class | ids | what it establishes |
|---|---|---|
| WARM-SAME | W-01, W-02, W-09, W-12 | primed cache, answer identical to the cold twin; W-02/W-14 use the resolver's default cache location (`XDG_CACHE_HOME` unset → `$HOME/.cache`); W-09 adds `/disable_cache` to a list after priming (same byte count) and the state stays **hit** — the resolver reads the cache before any list (:1179 before :1184) |
| WARM-DIFFERS | W-03..W-08, W-10, W-11, W-14 | the warm answer is measurably different from the cold twin's: same-size/same-date `Exec` edit (cold rejects, warm prints the cached command); `TryExec` stub removed while exec[0] resolves; `Categories` edited; `TerminalArgDir`/`TerminalArgTitle` names edited under `--dir=`/`--title=`; `Exec=foot --a`→`--b`; list reordered (cold picks kitty, warm foot); `Exec=foot`→`foou` plus a `bin/foou` stub (both valid, different commands) |
| MALFORMED-* | M-01..M-06, M-11, M-12, M-16..M-18 | a cache that exists and is not trusted: mtime date moved (M-01), size moved (M-02), entry renamed (M-03), a new entry appears (M-04), `XDG_CURRENT_DESKTOP` changed (M-05), exec[0] stub gone while the listing is unchanged (M-06), fake hash (M-11), applications dir gone (M-12), terminator on line 49 parses/stale vs line 50 invalid (M-16/M-17), terminator on an unterminated last line invalid (M-18) |
| MALFORMED-DISABLED | M-13, M-14 | cache never consulted: `XTE_CACHE_ENABLED=false` after priming, and `=garbage` (check_bool says no) |
| EDGE-HOMEUNSET | E-01 | round-47 D1 / `w2/ExecC1Diff` H3: HOME and the XDG bases unset → the resolver exits 1 with empty stdout; `state=absent` (it dies before the cache gate) |
| WARM-ABSENT | E-02 | nothing selectable, so the prime saves no cache: a plain cold run, cache=absent |

Warm states are 13 hit / 9 stale / 6 invalid / 2 disabled / 2 absent; 31 fixtures carry a measured cold twin and 9 of
them answer differently (the WARM-DIFFERS set, each asserted at count time).

## 3. Clause x (explain) after the two routed findings

* `cmd=` compared, from a **second** prepared tree and a `--print-cmd=\036 --print-delimiter=\036` oracle run, so a
  command word may contain a newline (splitting the default capture on `\n` would truncate it).
* `cache=` compared to the oracle's derived state, so `explain` must name the warm verdict, not just file existence.
* the third capture is the oracle's own capture **cut to its first two items**: a tool that compares only id+path
  (or that drops its last output line) now reports AGREE and fails. That is the `w2/CritC1Explain.md` hole, closed by
  measurement rather than by wording.
* F4 closed: the captures are written into a fresh `mkdtemp` inside the tool tree's `.rw`, each file opened
  `O_EXCL|O_NOFOLLOW`, and every OSError there becomes a clause-x failure for that fixture.
* a `MADO_TERM:` line whose values carry spaces is parsed by marker order (see the table in section 1).

## 4. Clause i after `w2/SentC1Sandbox.md` F1-F3

Clause i is now the **enumerated mount set** (`/` tmpfs; `/usr/lib` host read-only plus the `/lib`,`/lib64`
symlinks; `/bin/sh` and `/bin/bash`; `/oracle/bin` = the seven externals; `/dev` with host devtmpfs nodes and a
fresh devpts; `/proc`; `/tmp` tmpfs; the case root read-only; its `.rw` rw for an oracle run and **read-only for a
tool run**; the `default_cache` alias; the pin, or python3 + the tool), followed by the statement that "no host path
outside that set is BOUND" and by the declared residuals F1/F2/F3 named in the probe: bwrap's empty stub
directories for mountpoints (the `/fast` chain of `--work`, `/usr/bin`), the whole host `/usr/lib`, the inherited
UTS name, the `PWD` bwrap injects, `/proc/1/cmdline` carrying the bwrap argv. F1's "path X is absent" test is
explicitly rejected as the criterion.

## 5. Measurements (this host, 2026-10-26)

Final line for the round-47 tool at the round start (`--nonce 48`):

```
PRED-C1-r48: cold=190/190 warm=22/32 explained=193/222 generated=210/230 selftest=ok readonly=ok tool=present verdict=TARGET_MISSED
```

READ THIS AS THE DRAFT'S OWN NUMBERS, NOT A SCORE. The round-47 tool models the cold path only, so the warm clause
is expected to miss — and it misses on exactly the cases where the warm answer differs from the cold one (the ten
WARM-DIFFERS failures plus E-01, which the r47 tool answers with exit 2 where the pin exits 1), while the 22 warm
passes are exactly the four WARM-SAME controls, the seventeen MALFORMED cases and WARM-ABSENT - every
fixture whose warm answer equals its cold one. Clause x fails where `cache=` is `hit`/`stale`/
`invalid`/`disabled` (the r47 tool prints `present`) and on E-01 (no `MADO_TERM` line at all: exit 2). Clause f is
190/190 on the unchanged round-47 file — the harm watch holds. `trips=0` over every tool run.

Two nonces, so the generated arm is not one draw:

| tool | nonce | final line |
|---|---|---|
| round-47 tool @ `579f694` | 48 | `cold=190/190 warm=22/32 explained=193/222 generated=210/230 selftest=ok readonly=ok tool=present verdict=TARGET_MISSED` |
| round-47 tool @ `579f694` | 424242 | `cold=190/190 warm=22/32 explained=193/222 generated=210/230 selftest=ok readonly=ok tool=present verdict=TARGET_MISSED` |
| ExecRefCacheA's warm-cache draft (sha256 `2894f7f8dc5dcc2eeb9199670032db794b118f3acb7667eda3fc843f83fd6196`, committed as `8e1eeeab` in a scratch clone) | 48 | `cold=190/190 warm=32/32 explained=222/222 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET` |
| same draft | 424242 | `cold=190/190 warm=32/32 explained=222/222 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET` |
| ExecRefCacheA's FINAL draft (sha256 `c4ed769eea9c1c88da8fe9c222cca79035faac0224639e45c98a7d0f44a93bdd`, committed as `9340fcf6` in a scratch clone) | 48 | `cold=190/190 warm=32/32 explained=222/222 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET` (`MADO_TERMINAL_SELFTEST: 71/71 passed`) |

Same nonce, same numbers, both tools: the instrument is reproducible. Different tools, different verdict: it
discriminates. The MET is a measurement of a peer's **draft**, not a claim about the tracked `tools/mado-terminal.py`
(that one is scored above, at the round start, and misses).

Exact invocations:

```
python3 -I .ufo/waves/round-48/w1/ExecCounterC1/c1-r48-terminal-cache.py \
        --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 579f694b45c797a9c39761fdb4f9e0a1b71b3585 \
        --work /fast/scratch/hyaku/mado-r48/ExecCounterC1/run48  --nonce 48
D=$(mktemp -d -p /fast/scratch/hyaku/mado-r48/ExecCounterC1); git clone -q --shared --no-checkout <lane> $D; \
git -C $D rev-parse --show-toplevel   # == $D; then checkout 579f694, copy the draft over tools/mado-terminal.py,
git -C $D -c user.name=seat -c user.email=seat@scratch.invalid commit  # then --repo $D --rev HEAD
```

Runtime: 88 s (r47 tool) and 109 s (draft) per count on this host; `trips=0` in every run; the sandbox mounts
nothing of the host outside clause i's set.

## 5b. Artifacts in this seat directory

| file | what |
|---|---|
| `c1-r48-terminal-cache.py` | the counter draft (sha256 `8db736a7...`), drop-in beside `c1-r47-fixtures.json` in `quality/counters/` |
| `c1-r48-fixtures.json` | the 32 warm/malformed fixtures, sha256 `23932fd3...` = the counter's `SHA256_WARM` |
| `gen-fixtures-v2.py` | the builder that measured them (imports the counter's `prepare`/`oracle_side`; 3 identical runs or it writes nothing) |
| `counter-r47tool.txt`, `counter-r47-nonce424242.txt` | r47 tool receipts (nonce 48 / 424242) |
| `counter-draft-cacheA.txt`, `counter-draft-nonce424242.txt`, `counter-draft-final.txt` | ExecRefCacheA draft receipts (draft `2894f7f8` nonces 48 / 424242, final draft `c4ed769e` nonce 48) |
| `counter-r47tool-prefixparse.txt` | the same r47-tool count before the `MADO_TERM:` parse fix (shows the `t6` truncation) |
| `probe-prime.py`, `probe-warm.py`, `probe-receipts.txt` | the two emulation probes the clause design rests on, kept verbatim as run (their `WORK` names the scratch root, deleted since; the receipt is `probe-receipts.txt`): 8/8 primed runs leave a complete 191-byte cache; a pinned 2020 mtime gives a stable hash, a same-size edit stays `hit`, a size change goes `stale` |

### What clause f does NOT change about the round-47 cold clause

Same file, same `SHA256_COLD`, same 190 records, same two variants, same two trees per variant, same comparison
(exit status + `$ROOT`-normalized stdout; stderr not compared). Two harness differences, both inert for a cold
answer and both measured: (i) the oracle of every clause now runs with `XTE_DEBUG=1`, whose `debug()` writes to
**stderr only** (pin :61-75), so stdout and exit status cannot move; (ii) a tool run's `.rw` is mounted read-only,
and no cold fixture's tool run writes there - a tool that did would fail, which is the point. Evidence: 190/190 with
the round-47 tool at two nonces, i.e. exactly the number the round-47 counter reported at its freeze.

## 6. Defects found in the round-47 instrument while extending it

1. **`MADO_TERM:` was parsed by whitespace**, so any value with a space was truncated: cold fixture
   `t6-exec-quoted-binary-with-space` (`Exec="my term" --flag`) reads `cmd=my`. The r47 counter never compared cmd=,
   so the defect was invisible; comparing cmd= exposed it. Fixed by parsing by marker order; receipt
   `counter-r47tool-prefixparse.txt` (before) vs `counter-r47tool.txt` (after).
2. **A plain sandbox run of the pin leaves no cache at all** (`save_cache "$1" &` is killed with the sandbox's pid
   1), so any claim that a warm cache "can be produced by running the resolver once" is false under the r47 clause-i
   sandbox. Clause w primes through a waiter that reaps the fork (`.ufo/.../ExecCounterC1/probe-prime.py` receipt:
   8/8 primed runs complete, 191-byte cache with the terminator).
3. **A pinned 2020 mtime prints the old `Mon dd  YYYY` form**, so a mtime mutation must move the *date*: +7200 s is
   invisible to `ls` and left the cache a hit (M-01 first draft, measured). The fixtures use +86400.

## 7. What the freeze must record

1. `SHA256_COLD = 4836cc1d...` (round-47 file, unchanged) and `SHA256_WARM = 23932fd3...` (this seat's 32-case
   file); the counter refuses another byte, and fewer than 100 / 20 cases is a setup error.
2. The five `cache=` tokens (`absent|hit|stale|invalid|disabled`), the derivation rule in clause w, and E-01's
   `explain` answer (`NO_TERMINAL`/exit 3/`cache=absent`) - the only contract choices in this draft that are not
   forced by the pin.
3. Clause i as the enumerated mount set, including the read-only `.rw` for tool runs and the `default_cache` alias.
4. `GEN = 150`, `GEN_W = 80`, `SELFTEST_MIN = 30`, `PINNED_MTIME = 1600000000`, and the final-line shape
   `PRED-C1-r48: cold=K/F warm=W/V explained=X/T generated=G/N selftest=.. readonly=.. tool=.. verdict=..`.

## 8. Risks / open items for the freeze

* The five `cache=` tokens and the `explain` verdict for the HOME-unset edge are a contract decision, not a
  measurement. ExecRefCacheA agreed to both (message of 2026-10-26); the counter scores `NO_TERMINAL`/exit 3 for the
  edge, so if the freeze picks another verdict the counter must be re-pinned with it.
* The prime waiter is the counter's own shell; the resolver's *timing* is not scored, only its result. A pin that
  stopped forking the save would make every `prime` fixture absent and clause w would report the drift (the fixtures
  record `state`, and a mismatch is a setup error).
* `gen_warm_case`'s four kinds are structural (same-size edit / size or date change / no terminator / gate off), so
  the premise cannot depend on the clock; the premise is still measured at count time and a mismatch is a setup
  error, not a silent pass.
* Not modelled, declared: a cache path that is a directory or FIFO (`[ -f ]` false → absent), an unreadable cache
  file, a cache whose path lies outside the writable `.rw`, non-ASCII `\u` delimiter escapes, `-h/--help`.
* `explain`'s `MADO_TERM:` line cannot carry a value containing a later field's marker (`" path="`); no fixture
  builds one, and the residual is declared in `term_line()`.
