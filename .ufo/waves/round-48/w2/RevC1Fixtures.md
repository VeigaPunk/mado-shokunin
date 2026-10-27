# RevC1Fixtures — round 48 w2 (FALSIFY): the 204 frozen warm fixtures and their class premises

Seat `RevC1Fixtures` (leaf). Target: the frozen C1 warm fixture set and the class premises it claims, attacked
against the real pinned resolver before any data commit. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, freeze
`3e6c848a0e1bbc9c7058226b86d0faefc5351c9d`, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`.

Frozen instruments used read-only, hashes observed at count time:

| artifact | sha256 |
|---|---|
| `quality/counters/c1-r48-fixtures.json` | `4d946bd7934d4afc40d16676a300a7a10ee077404a2d51e289d9db871cb311aa` (= `SHA256_WARM`) |
| `quality/counters/c1-r48-terminal-cache.py` | `2a7d03d96d6ea5489fecc110de8d29b83d6c3d2d6abd4e5d4138096d01ccddd4` |
| `.ufo/waves/round-47/fetch/xdg-terminal-exec` (v0.14.3) | `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (= `PIN_SHA256`) |

`git status --short --` on the fixture file, the counter and the pin prints nothing (unmodified working bytes). No
lane file, registry, counter, entry, report, fleet repo, sibling lane or shokuknow byte was written; no commit/push/jj;
no install; no pacman; no compositor/input/GUI mutation. No subagent and no background job — the single labrat was
unused; every run was a direct child of the seat's own shell.

## Verdict

**No drift and no false premise in the frozen set on this host.** All 204 warm records re-derive from the pin:
`expect` 204/204 in variant A **and** 204/204 in variant B (deeper root, `LANG=en_US.UTF-8`), `state` 204/204,
recorded `cold` 160/160, my extended class-premise checks 204/204, and the frozen `check_premise` raises no `Setup`
for any row. `state` is equal in both variants for all 204 (no variant-B-only state drift).

What the wave does find is **instrument coverage**, not a fixture defect: clause `w` premise-checks only
`WARM-DIFFERS`/`WARM-SAME` (74 rows); the other 130 rows are held only by their recorded `state`/`cold`. Four
fabricated false class labels in those classes are accepted by the frozen `check_premise` (F5). Three labelling /
normalisation notes (F6-F8) and one unmeasurable residual (F9) follow. None of them narrows or changes a predicate;
none is a scored miss, because every label those rows claim is true under measurement here.

## Method — commands and scratch

Scratch `S=/fast/scratch/hyaku/mado-r48/RevC1Fixtures` (removed at the end, see Cleanup). Every script imports the
frozen counter by path (never modified) and drives the **pin** through `Box`/`prepare`/`oracle_side`, so the oracle is
the resolver, not an implementation of ours. Evidence scripts live in
`.ufo/waves/round-48/w2/RevC1Fixtures/`.

| script | command | measures |
|---|---|---|
| `verify-fixtures.py` | `python3 -I verify-fixtures.py $S/work $S/full` | per row: variant-A oracle vs `expect`, variant-B oracle vs `expect`, `state`, cold twin vs `cold`, class premise, frozen `check_premise` |
| `boundary-49-50.py` | `python3 -I boundary-49-50.py $S/work $S/boundary.json` | a **real primed** cache with its terminator walked over lines 47-51, then `M-16`/`M-17` shifted ±2 lines |
| `root-subst.py` | `python3 -I root-subst.py $S/work $S/rootsubst.json` | every `$ROOT` in the frozen file, plus five dynamic substitution shapes in both variants and the `norm()` identity |
| `readdir-fs.py` | `python3 -I readdir-fs.py $S/work $S/readdir.json` | filesystems, the counter's materialization vs every recorded `readdir_order`, creation-order vs readdir for 2…1024 entries, load-bearing flip |
| `order-sensitivity.py` | `python3 -I order-sensitivity.py $S/work $S/order.json` | every multi-entry fixture re-measured with ascending and descending `files_order` |
| `checks.py` | `python3 -I checks.py $S/checks.json` | `load_fixtures` (pin SHA + `check_case`), counts, cold/prime consistency, and four false-label probes through the frozen rule |

Receipts: `fixtures-verify.log`/`.jsonl`, `boundary.json`, `rootsubst.json`, `readdir.json`, `order.json`,
`checks.json` beside this report.

## Counts

```
SUMMARY {"cold": 160, "counterpremise": 204, "expectA": 204, "expectB": 204, "n": 204, "premise": 204, "state": 204}
FAILS 0
```

- 204 rows, 204 unique ids, `load_fixtures` accepts the file against `SHA256_WARM` with `MIN_FIXTURES_WARM=20`;
  `check_case` accepts all 204 (no cache+prime collision, every `args`/`prime.args` carries a print option, every
  `XDG_CACHE_HOME` under `$ROOT/.rw`, every `default_cache` row free of `XDG_CACHE_HOME`/`HOME` unset).
- 44 rows carry no cache by design: READDIR 10, H1 12, H2 11, HOME-UNSET 8 (`v2-hu-01..06,09,10`), EDGE-HOMEUNSET 1
  (`E-01`), CACHE-DEFAULT 1 (`v2-wd-38`), MALFORMED 1 (`v2-mf-17-no-cache-path`); 160 rows carry a `cold` record, and
  **0** rows disagree with that rule (a `cold` record exactly on the rows that have a cache to remove).
- Class table as measured (state → n):

| class | n | derived states |
|---|---|---|
| WARM-DIFFERS | 48 | hit 48 (warm ≠ cold 48/48) |
| WARM-SAME | 26 | hit 26 (warm = cold 26/26) |
| WARM-INVALID | 34 | stale 30, disabled 3, invalid 1 (cache rejected, warm = cold 34/34) |
| MALFORMED | 31 | invalid 10, hit 12, stale 8, absent 1 |
| MALFORMED-`MTIME/SIZE/NAME/DIRADD/DIRGONE/DESK/EXECGONE` | 7 | stale 7 (mutation classes) |
| MALFORMED-`TERM/EARLY/LIMIT/EMPTY/NONL` | 5 | invalid 5 |
| MALFORMED-`BADHASH/LINE49` | 2 | stale 2 |
| MALFORMED-`LINE50/DISABLED/DISABLED-GARBAGE` | 3 | invalid 1, disabled 2 |
| HOME-UNSET | 10 | absent 4, `-` 4, hit 2 |
| H1 | 12 | absent 12 |
| H2 | 13 | absent 11, hit 2 |
| READDIR | 10 | absent 10 |
| WARM-ABSENT, CACHE-DEFAULT, EDGE-HOMEUNSET | 1+1+1 | absent, absent, `-` |

Class totals reconcile with the w1 tables (36 `WARM-HIT-DIFFERS` + 9 `W-*` + 3 `L1-*` = 48 `WARM-DIFFERS`;
18 + 4 + 4 = 26 `WARM-SAME`; 34 `WARM-INVALID` unchanged; prefix totals 162 `v2-*` + 13 `W-*` + 17 `M-*` +
2 `E-*` + 10 `L1-*` = 204).

## Findings

### F1 (holds) — every record re-derives from the pin, in both variants
204/204 variant-A oracle `(rc, stdout)` equal the recorded `expect`; 204/204 variant-B oracle (root
`<work>/job-<hex>/deep/<hex>/r`, `LANG=en_US.UTF-8`) equal the same record, so no record is root-depth- or
locale-dependent; 204/204 derived `state` equal the recorded `state`; 160/160 recorded `cold` twins re-derive; the
frozen `check_premise` accepts all 204 (`counterpremise` 204). The counter's own drift list would therefore be empty.

### F2 (holds) — the 49/50 cache line boundary is exact, and both fixtures sit on it
`read_cache` (`:217-298`) returns `reached cache line limit` when line 50 is reached; line 49 is still parsed. On a
**real primed** cache (11 lines, terminator on line 11) with the primed — i.e. *valid* — hash:

```
term_line_47  lines=47 rc=0 state=hit      debug=['got cache:','cache is actual']
term_line_48  lines=48 rc=0 state=hit      debug=['got cache:','cache is actual']
term_line_49  lines=49 rc=0 state=hit      debug=['got cache:','cache is actual']
term_line_50  lines=50 rc=0 state=invalid  debug=['reached cache line limit (50)']
term_line_49_no_terminator lines=49 rc=0 state=invalid debug=['invalid cache data']
term_line_50_no_terminator lines=50 rc=0 state=invalid debug=['reached cache line limit (50)']
term_line_51_no_terminator lines=51 rc=0 state=invalid debug=['reached cache line limit (50)']
```

So a *valid* cache is discarded the moment its terminator reaches line 50 — the limit precedes the hash comparison.
Shifting the two frozen boundary fixtures one line each way:

```
M-16 delta=-1 term_line=48 state=stale    (recorded stale)
M-16 delta=+0 term_line=49 state=stale    (recorded stale)
M-16 delta=+1 term_line=50 state=invalid  -> 'reached cache line limit (50)'
M-17 delta=-1 term_line=49 state=stale    -> 'cache is out-of-date'
M-17 delta=+0 term_line=50 state=invalid  (recorded invalid)
```

`M-16` (terminator line 49) and `M-17` (line 50) are exactly on the boundary and flip into each other's verdict on a
one-line shift; their recorded `state` (`stale`, `invalid`) and their recorded `expect` (cold answer both times) hold.
`v2-mf-10-50-lines` (50 lines, no terminator) and `v2-mf-11-51-lines` (terminator line 51) are consistent with the
same rule (`invalid`).

### F3 (holds) — `$ROOT` is a total, path-only substitution; the mask exists but no fixture can reach it
Static scan of all 204 rows: **859** `$ROOT` occurrences in 204/204 fixtures, **859/859** immediately followed by `/`
(no mid-token use), and **0** baked absolute paths (`/fast/`, the lane path) anywhere in the set. The only other
`$`-token in the file is a literal `$HOME` inside `v2-wd-38`'s prose `meta.note`.

Dynamic, both variants (`root_tokens` = occurrences in the normalized output, `abs` = un-normalized absolute path
left in stdout):

```
colon-list-two-roots     A/B rc=0 state=hit   roots=1 abs=False '$ROOT/home/.local/share/applications/foot.desktop'
exec-word-with-root      A/B rc=0 state=hit   roots=1 abs=False 'foot\n--$ROOT/x\n'
root-as-whole-cache-line A/B rc=0 state=stale roots=1 abs=False '$ROOT/home/.local/share/applications/foot.desktop'
escaped-double-root      A/B rc=0 state=hit   roots=0 abs=False 'foot\n--\n'
```

`encode()` replaces every occurrence (file bodies, cache literals, `after.*` values, env values) and `norm()` replaces
the case root back on stdout, so `$ROOT` appearing in *content* (not a path) is re-tokenised: `Exec=foot --$ROOT/x`
prints `--$ROOT/x`, which **is** the absolute path. The mask is exactly that identity —

```
masking: {"identical": true,
          "oracle_prints_literal": "$ROOT/foot.desktop\n",
          "tool_prints_root": "$ROOT/foot.desktop\n"}
```

i.e. a literal `$ROOT` in stdout and the real root normalise to the same string. No frozen fixture is exposed: schema
v2 has no way to emit a literal `$ROOT` (every write path goes through `encode`; `$$ROOT` does not yield one — measured
`foot\n--\n`), and no record needs one. Residual for the freeze: `$ROOT` is unescapable, so a future fixture that wants
the literal text would be silently conflated with the root; there is no fixture of that kind today.

### F4 (holds) — the readdir premise is load-bearing, and every order-sensitive case is pinned
Filesystems at count time: `/fast` = **xfs**, my work root = xfs, `/home` (lane) = **btrfs**.

- The frozen counters' own materialization reproduces the recorded `readdir_order` for **186/186** recorded
  `(directory, order)` pairs across 161 fixtures — zero mismatches once the fixture's `after` mutations are applied
  before the listing (four rows — `v2-wi-03/04/05/10` — record the *post-mutation* order; they also reproduce).
- On this host, xfs readdir order **is** creation order for the fixture sizes and well beyond: `n = 2, 3, 4, 10, 16,
  32, 64, 128, 256, 512, 1024` entries created in reverse name order all list in creation order
  (`readdir==creation:True`, `readdir==sorted:False` at every n). The counter's docstring claim ("readdir order is
  reproducible on the same filesystem") therefore holds for every directory the set materializes.
- Load-bearing: `v2-rd-06-reverse-create` frozen `(0,'ghostty.desktop\n')` vs sorted materialization
  `(0,'konsole.desktop\n')` — `drifts=True`.
- Coverage: 18 fixtures materialize a directory with ≥2 entries. **8 change answer** under an ascending or descending
  `files_order` (`v2-rd-01`…`v2-rd-08`), and **all 8 ship `meta.files_order`**; `sensitive_without_files_order=0`.
  The other ten (W-10, M-05, the seven `v2-wd-*` list/entry rows, `v2-h1-12`) do not change answer under either probe,
  and neither do the twelve recorded multi-entry directory orders that ship no `files_order` (7 `v2-wd-*`,
  `v2-wi-05/10/11`, `v2-h1-08/12`). No order-dependent answer is left to filesystem luck. `v2-rd-09` (duplicate id, later operand wins) and `v2-rd-10`
  (nested id, one entry) are order-insensitive by construction; `v2-rd-10`'s recorded order covers only the parent
  directory — see F7.

### F5 (advisory) — clause `w` premise-checks 74 of 204 rows; the other 130 rest on `state`/`cold` records only
`check_premise` premises only `WARM-DIFFERS`/`WARM-SAME` (74 rows). 26 classes / 130 rows have no warm-vs-cold
premise; their label is only as good as the recorded `state` (enforced for every row) and `cold` (enforced where
recorded). Measured with the frozen function itself:

```
WARM-INVALID with a warm answer that differs from cold    -> accepted (not enforced)
READDIR with an invented winner                           -> accepted (not enforced)
H1 with no shadowing directory                            -> accepted (not enforced)
HOME-UNSET that never unset HOME                          -> accepted (not enforced)
WARM-SAME with a differing cold twin                      -> rejected: warm answer differs from the cold one
WARM-DIFFERS with no cold twin                            -> rejected: WARM-DIFFERS without a cold twin
WARM-INVALID whose state is a hit                         -> rejected: cache state is 'hit', recorded 'stale'
```

A future row in one of those classes could carry a false label and still score. **Today it cannot pass unnoticed by
this wave**: my own premise checks for exactly those classes pass 204/204 (WARM-INVALID 34/34 rejected-cache **and**
warm = cold; READDIR 10/10 winner = last *file* entry of the recorded order, nested row excepted; H1 12/12 has a
directory shadowing an entry; H2 13/13 has an option-like `Exec`/`TryExec`; HOME-UNSET 10/10 dies before the cache gate
iff `state` is `-`; CACHE-DEFAULT 1/1 has `default_cache` and no `XDG_CACHE_HOME`). This is an instrument-coverage
note for the freeze, not a predicate change and not a miss.

### F6 (advisory) — `WARM-INVALID` names a rejected-cache group, not the `invalid` state
30 of the 34 derive `stale`, 3 `disabled`, 1 `invalid`. The row premise that matters (the cache is rejected, so the
warm answer equals the cold one) holds 34/34. A reader who takes the class name for the derived state would be wrong;
the counter never compares the two, and does not need to.

### F7 (advisory) — two naming nits, both with correct records
`MALFORMED-DIRADD` (`M-04`) adds a *file* (`usr/share/applications/extra.desktop`) inside a hashed directory, not a
directory; its mechanism (listing change) and its `stale` record hold. `v2-rd-10-subdir-ids` records `readdir_order`
only for `home/.local/share/applications` (`['a.desktop']`), not for the nested `a.desktop/` that actually decides the
winner; the row is order-insensitive (one nested entry), so the record is incomplete rather than false. `M-14`'s
`disabled` verdict comes from a garbage `XTE_CACHE_ENABLED` in the scored env, verified from its `env`/`cache` pair.

### F8 (residual) — the readdir premise is same-filesystem, and the counter admits any `--work`
`--work` is rejected only inside the repo, the lane or the lane's parent (`main()`), so a count with `--work` on
another filesystem is legal. All fixture expects were produced on xfs (`meta.fs: xfs`) and this seat re-derived them on
xfs. `/home` is btrfs here; I did **not** materialize fixtures there (seat write scope: everything under
`/fast/scratch/hyaku/mado-r48/RevC1Fixtures`), so on-xfs behaviour is measured and non-xfs readdir ordering is
`[INFERENCE: filesystem-specific; not measured]`. The consequence is bounded: a differing order changes the oracle
answer, which the drift check turns into a loud `SETUP` ("oracle drifted from ..."), never a silent pass — and F4
shows no order-sensitive row is unpinned anyway.

### F9 (residual) — variant-B `state` is not compared by clause `w`
Clause `w` premises the derived state on variant A only. Measured: variant-B state equals variant-A state for all 204
rows, so nothing is hiding there today.

## Risks and blockers

- **Seat bound vs the instrument's own copy:** `ulimit -f 2048` (1 MiB) makes the frozen `Box` fail —
  `shutil.copy('/usr/bin/gawk')` → `OSError: [Errno 27] File too large`, gawk is 1 274 872 B. Each writer shell
  therefore started with `ulimit -f 2048` and then raised to `ulimit -f 8192` (4 MiB) for the run; every artifact this
  seat produced is ≤ 43 937 B (`readdir.json`), the seat evidence directory totals 154 971 B, and scratch totalled
  1.5 MB (`du`), far inside the 2 GB / 1 MiB-per-file budget. No other package, service or host state was touched.
- Non-xfs readdir ordering is not measurable under this seat's write scope (F8). No blocker for the frozen set.
- No blocker reachable: the fixtures, the counter and the pin are byte-unchanged and every claim above is a measured
  output of the pinned resolver under the frozen sandbox.

## Cleanup

Scratch `/fast/scratch/hyaku/mado-r48/RevC1Fixtures` (work trees, primed caches, sandbox bins) was removed after the
receipts were copied; no `/tmp` use, no fixture edited, no lane write, no commit. Evidence retained in this directory:
six scripts, `fixtures-verify.log`/`.jsonl`, `boundary.json`, `rootsubst.json`, `readdir.json`, `order.json`,
`checks.json` and the matching run logs.
