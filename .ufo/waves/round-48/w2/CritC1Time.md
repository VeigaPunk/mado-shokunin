# w2 / CritC1Time — falsify cache-hash date/time boundaries

**Seat** leaf `CritC1Time`; **wave** round 48 `w2` FALSIFY, policy v1, lane `mado-shokunin`, base
`579f694b45c797a9c39761fdb4f9e0a1b71b3585`. **Attack** the warm-cache hash's date/time edges: real pin
`/usr/bin/xdg-terminal-exec` (v0.14.3) against the frozen tool's `ls_lRL`/`gen_hash` over explicit file and
directory mtimes at now, now−1 s, now−6 months ±1 s, future +1 s/+1 h, same-minute and cross-minute same-size
edits, under three controlled `TZ` values, plus the frozen counter itself. Nothing in the lane, the registry, the
counters, the fixtures or any sibling lane was written; scratch only under `$S` and this seat directory.

**Headline.** The frozen predicate stands: **`PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394
generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0**, at `TZ=UTC0` **and**
`TZ=Asia/Tokyo`. Every date/time regime inside the frozen contract is byte-equal between the pin and the tool, and
the fixtures carry identical date strings in both variants. **One contract-text hole, no verdict impact:** an mtime
within one second of the moving GNU ls six-month cutoff is refused by the tool (`MADO_TERM_OUT_OF_CONTRACT`, exit 2)
where the pin answers normally (exit 0, hash, selection). That exception is declared in the tool's docstring
(`mado-terminal.py:108-109`) but **not** in `registration.md`, whose C1 contract says `gen_hash` *must* be byte-equal
to `LC_ALL=C LANG=C ls -LRl` with no date carve-out, and the counter has no notion of an OOC result. No frozen
fixture can reach that window (all pinned mtimes are 2020 dates, ≈2051 days clear of the cutoff, and the fixture
file is SHA-256-pinned), so it is a pre-data registration text defect, reported here as a miss of the frozen
contract's letter, not a fixture failure. A second, benign finding: **directory mtimes never enter the hash at all**
(identical hashes with dir mtimes a day apart), so the schema's dir-mtime pinning is inert.

## Instruments (hashes)

| item | sha256 |
|---|---|
| pin `.ufo/waves/round-47/fetch/xdg-terminal-exec` = `/usr/bin/xdg-terminal-exec` | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` |
| tool frozen `l1-draft/mado-terminal.py` | `1dfde36cfa68beffb6b2bc2ae9cf04875bd48702669812ce3ecd10b986753a92` |
| counter `l1-draft/c1-r48-terminal-cache.py` | `2a7d03d96d6ea5489fecc110de8d29b83d6c3d2d6abd4e5d4138096d01ccddd4` |
| fixtures `l1-draft/c1-r48-fixtures.json` | `4d946bd7934d4afc40d16676a300a7a10ee077404a2d51e289d9db871cb311aa` (= counter `SHA256_WARM`) |
| host `ls` | GNU coreutils **9.12** (`/usr/bin/ls --version`) |

Replay tree: base rev archived (`git -C <lane> archive 579f694…  -- tools/mado-terminal.py quality/counters
.ufo/waves/round-47/fetch | tar -x`) plus the three `l1-draft` bytes (tool, counter, fixtures), committed in a scratch repo
`$S/c/repo` (toplevel asserted == `$S/c/repo` before the commit; scratch commit `b6d02d7dff65b7c915408ea55b345528bb8473b1`,
**not** a lane commit). A full `git clone` was impossible under the 1 MiB/regular-file writer guard — lane blobs
exceed it — and the counter refuses a `--work` dir under the lane root's parent, so the repo sits one level deeper.

Counter command (both TZs):

```
cd $S/c/repo && TZ=UTC0       python3 -I quality/counters/c1-r48-terminal-cache.py --repo $S/c/repo --rev HEAD --work $S/work1 --nonce 4848
cd $S/c/repo && TZ=Asia/Tokyo python3 -I quality/counters/c1-r48-terminal-cache.py --repo $S/c/repo --rev HEAD --work $S/work2 --nonce 4848
```

Observed (both runs identical, receipts `counter-UTC0.txt`, `counter-Asia_Tokyo.txt`, 404 lines each):
`clause=a tool=present`; `clause=meta rev=b6d02d7dff65b7c915408ea55b345528bb8473b1 nonce=4848`;
`clause=s … MADO_TERMINAL_SELFTEST: 69/69 passed`; `clause=g generated=230/230`; `clause=r trips=0`;
final `PRED-C1-r48: cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok
tool=present verdict=TARGET_MET`, `rc=0`. The TZ axis does not move the verdict (the hash is computed per tree by
each side, so a shifted wall clock shifts both).

## A. mtime regime matrix (pin vs tool vs a replayed `ls -LRl`)

Three TZs (`UTC0`, `Asia/Tokyo`, `America/New_York`); one tree (`cd/xdg-terminals.list`, `usr/share/applications/
foot.desktop`, `bin/foot`), every file *and* directory mtime set explicitly, then: `/usr/bin/ls -LRl` under
`LC_ALL=C LANG=C`, the frozen tool's `ls_lRL(operands, now_ns=<captured>)` on the pin's own operand list (8 operands
from its `XTE_DEBUG` `paths:` line), and a fresh-cache `xdg-terminal-exec --print-cmd` whose cache line 1 is the
pin's `gen_hash`. Hashes are `md5("4\n" + XDG_CURRENT_DESKTOP + "\n" + listing)`, the pin's exact stream.
Receipts: `matrix-{UTC0,Asia_Tokyo,America_New_York}.json`.

| regime (TZ=UTC0) | mtime | real `ls` date | tool date | pin hash | tool hash | equal |
|---|---|---|---|---|---|---|
| now | 1793064515 | `Oct 27 01:28` | `Oct 27 01:28` | `e0c3554d…` | `e0c3554d…` | yes |
| now−1 s | 1793064514 | `Oct 27 01:28` | `Oct 27 01:28` | `e0c3554d…` | `e0c3554d…` | yes |
| now−30 s | 1793064485 | `Oct 27 01:28` | `Oct 27 01:28` | `e0c3554d…` | `e0c3554d…` | yes |
| six months +1 s (recent side) | 1777286040 | `Apr 27 10:34` | — **refused** | `6c2d3aa7…` | `MADO_TERM_OUT_OF_CONTRACT` | **no** |
| six months exact | 1777286039 | `Apr 27  2026` | — **refused** | `052e798f…` | `MADO_TERM_OUT_OF_CONTRACT` | **no** |
| six months −1 s (old side) | 1777286038 | `Apr 27  2026` | `Apr 27  2026` | `052e798f…` | `052e798f…` | yes |
| future +1 s | 1793064517 | `Oct 27  2026` | `Oct 27  2026` | `406d3161…` | `406d3161…` | yes |
| future +1 h | 1793068116 | `Oct 27  2026` | `Oct 27  2026` | `406d3161…` | `406d3161…` | yes |
| 2020-01-01 (fixtures' value) | 1577836800 | `Jan  1  2020` | `Jan  1  2020` | `cec5a677…` | `cec5a677…` | yes |
| 2020-09-13 (fixtures' value) | 1600000000 | `Sep 13  2020` | `Sep 13  2020` | `3b1e6b69…` | `3b1e6b69…` | yes |

Identical outcome at `Asia/Tokyo` (`Oct 27 10:28`, `Apr 27 19:34`) and `America/New_York` (`Oct 26 21:29`,
`Apr 27 06:34`): the two six-month rows are refused by the tool and answered by the pin in every TZ, everything else
is hash-equal, and the pin's hash is reproduced byte-for-byte from the real `ls` stream
(`real_hash_replay == pin_hash` in every non-refused row, and `listing_equal` is true — the tool's listing bytes equal
`/usr/bin/ls`'s). Under `America/New_York`, `future +1 s` shows a split (pin `d2cf3f3b…` = the *now* row's hash,
real `ls`/tool `5d016821…`) for the benign reason in §C.

## B. The six-month cutoff, one second at a time

`delta` = mtime − clock, `SIX_MONTHS = 31556952//2 = 15778476`; receipt `sweep.json`:

| delta (s) | real `ls` date | tool date | pin hash | tool hash | equal |
|---|---|---|---|---|---|
| −15778479 | `Apr 27  2026` | `Apr 27  2026` | `53a8d6de…` | `53a8d6de…` | yes |
| −15778478 | `Apr 27  2026` | `Apr 27  2026` | `53a8d6de…` | `53a8d6de…` | yes |
| −15778477 | `Apr 27  2026` | `Apr 27  2026` | `53a8d6de…` | `53a8d6de…` | yes |
| −15778476 | `Apr 27  2026` | — **refused** | `53a8d6de…` | — | **no** |
| −15778475 | `Apr 27 10:37` | — **refused** | `5128d083…` | — | **no** |
| −15778474 | `Apr 27 10:37` | `Apr 27 10:37` | `5128d083…` | `5128d083…` | yes |
| −15778473 | `Apr 27 10:37` | `Apr 27 10:37` | `5128d083…` | `5128d083…` | yes |

So GNU ls switches form exactly at the 6-month line (`year` at the exact cutoff, `HH:MM` one second inside), the
pin hashes both sides normally, and the tool's two-second refusal band is the only disagreement. The tool's rule
(`recent = now − 6mo < mtime < now`, then `abs((now − mtime) − 6mo) <= 1 s → OutOfContract`) reproduces GNU on the
year side and the recent side but declines the switch itself.

## C. The hash is a function of (tree, clock), not of the tree

Same mtime `now+1 s`, sampled twice (receipt `sweep.json`, second block):

| when | clock | real `ls` date | tool date | md5 real / tool |
|---|---|---|---|---|
| immediately | 1793064701 | `Oct 27  2026` | `Oct 27  2026` | `b4bbed025e07` / `b4bbed025e07` |
| after 1.4 s | 1793064702 | `Oct 27 01:31` | `Oct 27 01:31` | `1dc93555db9d` / `1dc93555db9d` |

Both sides agree at each instant; a future mtime prints the year form until the clock passes it, then the recent
form. This explains the one split row in §A: the pin's `gen_hash` runs at the *end* of the resolver (selection, then
`save_cache`), so its `ls` sampled a later instant than my `ls` and saw `now+1 s` already past — the hash it wrote
was the recent-form one. Nothing to fix; it does mean no sample of this hash can be compared across instants, which
is exactly why the fixtures pin mtimes.

## D. Same-minute vs cross-minute same-size edit (the stale-but-valid path)

Prime a cold cache, rewrite `foot.desktop` with an identical byte count (`Exec=foot --a` → `Exec=fool --a`, both
76 B) at `now`, let the pin answer against the pre-edit cache, then restore those exact cache bytes and ask the tool
`print --print-cmd` the same question. Receipts `ed2-*.json`, three TZs, all six rows:

| TZ | case | date before → after | pin `cache` state | pin stdout | tool stdout | agree |
|---|---|---|---|---|---|---|
| UTC0 | same minute | `Oct 27 01:31` → `Oct 27 01:31` | `hit` | `foot --a` | `foot --a` | yes |
| UTC0 | cross minute | `Oct 27 01:30` → `Oct 27 01:31` | `stale` | `fool --a` | `fool --a` | yes |
| Asia/Tokyo | same minute | `10:31` → `10:31` | `hit` | `foot --a` | `foot --a` | yes |
| Asia/Tokyo | cross minute | `10:30` → `10:31` | `stale` | `fool --a` | `fool --a` | yes |
| America/New_York | same minute | `21:31` → `21:31` | `hit` | `foot --a` | `foot --a` | yes |
| America/New_York | cross minute | `21:30` → `21:31` | `stale` | `fool --a` | `fool --a` | yes |

The pin really does serve the stale command when the edit stays inside one displayed minute (mtime minute unchanged
→ md5 unchanged → `cache is actual`, stale content printed), and goes cold the moment the minute string moves. The
tool reproduces both, byte for byte, in every TZ: the minute window is unhedged and does not need to be — both sides
sample their own clock and the fixtures never place a recent mtime.

## E. Directory mtimes are not in the hash

Same file mtimes (`1600000000`), directory mtimes `1600000000` vs `1600086400` (one day apart): the pin's
`gen_hash` is `ba15de34e05310233e66e8055e83e68c` both times (`dir_mtime_visible_in_hash: false`,
`edits-UTC0.json`), and the `ls -LRl` listing is byte-identical across dir mtimes in all three TZs
(`dir_mtime_pair.real_listing_equal_across_dir_mtimes: true` and `tool_hash == real_hash_replay` in each
`matrix-*.json`). Cause: the hashed operands are list *files* plus application *directories*; `ls -lR` prints a
directory as a header and lists its contents, so only file mtimes reach a date column. The counter's
`apply_mtime` dir pass is harmless but is not what makes the listing deterministic — the pinned *file* mtimes are.

## F. Do the fixtures hold the same date strings in both variants?

Yes. Materializing the same bytes in the counter's two root shapes (`…/fx-abcd/r` for variant A,
`…/job-1a2b3c4d/deep/abcdef/r` for variant B), the date columns are identical after `$ROOT` normalization for a
pinned fixture value and for an unpinned materialization (`variants.json`):

```
A pinned:   -rw-r--r-- 1 vgpnk vgpnk 13 Sep 13  2020 $ROOT/cd/xdg-terminals.list
B pinned:   -rw-r--r-- 1 vgpnk vgpnk 13 Sep 13  2020 $ROOT/cd/xdg-terminals.list
A unpinned: -rw-r--r-- … Oct 27 01:32 $ROOT/cd/xdg-terminals.list
B unpinned: -rw-r--r-- … Oct 27 01:32 $ROOT/cd/xdg-terminals.list
```

The variant *hash* differs (the paths are part of the listing, and each side hashes its own tree, so nothing is
transplanted — as `registration.md` states). Fixture audit over all 204 warm cases:

* pinned mtimes are exactly `1577836800` (2020-01-01), `1600000000` (2020-09-13), plus `after.mtime`
  `1577923200`/`1600086400`; every value is **≈2234–2491 days old**, i.e. **≈2051 days clear of the moving 6-month
  cutoff**, so every one prints the year form and the date strings cannot drift across a minute or the cutoff;
* none falls within ±1 s of the cutoff (`in ±1s of cutoff: False` for all four values);
* the 59 cases with **no** `mtime` (`MALFORMED` 17, `H1` 12, `H2` 11, `READDIR` 10, `HOME-UNSET` 8,
  `CACHE-DEFAULT` 1) carry no hash-dependent verdict: recorded states are `absent` 39, `invalid` 8, `stale` 8, none 4;
  **zero** `prime`, and the 16 with a literal `cache` are all `invalid`/`stale` (a recorded hash can never match a
  fresh current-minute tree);
* all 90 `hit` fixtures are pinned and primed in-tree, so their hash equality is clock-stable.

## G. In contract vs out of contract (the decisive table)

| input class | pin | frozen tool | frozen registration says | tool docstring says | verdict |
|---|---|---|---|---|---|
| mtime recent (now, now−1 s, now−30 s), same minute | hash + selection | byte-equal | byte-equal | in contract | **pass** |
| mtime old side (> 6 months) | hash + selection | byte-equal | byte-equal | in contract | **pass** |
| mtime inside ±1 s of the moving 6-month cutoff | hash + selection, rc 0 | `MADO_TERM_OUT_OF_CONTRACT`, rc 2 | **no carve-out** (contract says byte-equal) | OOC (`:108-109`) | **miss of the contract's letter**; not exercised by any fixture |
| future mtime (+1 s, +1 h) | year form | byte-equal | byte-equal | in contract | **pass** (per instant) |
| directory mtimes | not in the listing | not in the listing | n/a | n/a | **inert** |
| `TZ` = UTC0 / Asia/Tokyo / America/New_York | follows TZ | follows TZ | host dependency (residuals) | "TZ (through the C library)" | **pass**, verdict unchanged |
| same-minute same-size edit | `hit`, stale command served | byte-equal | contract (stale-but-valid) | in contract | **pass** |
| cross-minute same-size edit | `stale`, cold answer | byte-equal | contract | in contract | **pass** |

Why it matters and why it is not a verdict failure: the predicate's *scoring* is fixture-based and the fixture file
is pinned by `SHA256_WARM`, so an in-window case cannot be scored without re-registration — and none of the 204
cases is in-window. The hole is in the *text*: `registration.md`'s C1 contract and the counter's declared-OOC list
(`c1-r48-terminal-cache.py:104-110`) omit the exception that the tool relies on, while the tool's own docstring
declares it. Read as written, `gen_hash` is required to be byte-equal for those operands and is not.

## Risks / blockers

1. **Pre-data repair is L1's call, not mine** (I may not touch the predicate). Two consistent fixes: (a) add the
   ±1 s six-month clause to `registration.md` **and** the counter docstring (and, if a case is ever wanted there,
   re-pin `SHA256_WARM` after adding it), or (b) delete the carve-out and implement the ns-exact comparison, which
   §A/§B show the tool's own formula already reproduces on both sides of the line — the refusal is defensive, not
   necessary; its only real function is the clock-race at the exact cutoff.
2. **No frozen fixture can ever test the six-month window** with today's design unless its mtime is recomputed at count
   time, which would break the counter's determinism premise. If clause coverage of the boundary is wanted, the
   fixture must carry a *relative* mtime (e.g. `mtime: "now-15778474"`) and the schema v2 already validates `mtime`
   as an int, so this is a schema change, not a data tweak.
3. **Writer-bound deviation, recorded:** the frozen counter copies `/usr/bin/gawk` (1 274 872 B) into its sandbox
   `bin-`, which a 1 MiB `ulimit -f` kills with `EFBIG` (observed twice: `OSError: [Errno 27] File too large:
   '/usr/bin/gawk' -> …/bin-*/awk`, `rc=1`). The counter shell therefore ran with `ulimit -f 8192` (4 MiB/file);
   every other writer shell used `ulimit -f 2048` (1 MiB/file). Largest file produced anywhere in my scratch:
   `299141 B` (`c1-r46-fixtures-v2.json`, a lane byte extracted by `git archive`); largest file *generated* by my
   own tooling: `12521 B` (`harness.py` receipt copy). Peak scratch `5.5 MB`, final `3.5 MB` before cleanup, both far
   under the 2 GB budget. No package transaction, no host mutation, no GUI/terminal launch, no `xdg-terminal-exec`
   beyond `--print-cmd` in a private scratch tree.
4. **Not attacked here** (other seats): the cache parser's line/terminator edges, `explain`'s `cmd=` comparison,
   the sandbox isolation allowlist, and the C2 entry.

## Retained evidence (this directory)

`commands.txt` (every command + instrument hashes) · `counter-UTC0.txt`, `counter-Asia_Tokyo.txt` (frozen counter,
404 lines each, `verdict=TARGET_MET`, `rc=0`) · `matrix-UTC0.json`, `matrix-Asia_Tokyo.json`,
`matrix-America_New_York.json` (regime matrix, pin/tool/replay hashes, date columns, per-row explain) ·
`ed2-UTC0.json`, `ed2-Asia_Tokyo.json`, `ed2-America_New_York.json` (same-minute/cross-minute edit pairs) ·
`edits-UTC0.json` (dir-mtime pair + first edit probe) ·
`sweep.json` (cutoff sweep + future tick) · `variants.json` (A/B date strings) · `harness.py`, `edits2.py`
(exact drivers) · `ulimit-note.txt`. Scratch `/fast/scratch/hyaku/mado-r48/CritC1Time` removed after copying.
