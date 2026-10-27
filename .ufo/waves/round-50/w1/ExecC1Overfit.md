# ExecC1Overfit — clause g (nonce) of the frozen C1 counter: does memorising the fixtures pay?

Seat `ExecC1Overfit`, mado round 50, wave w1 (BUILD + ATTACK of the round-49 instruments, retargeted w2 item
`ExecC1Overfit`, `.ufo/waves/round-49/w2-items.json` entry 9, routed by the round-49 closure D1).

**Verdict: the answer is no.** A tool that answers every frozen fixture from a 24 KiB embedded table and falls back to
a first-level-only algorithm reaches `fixtures=633/633` and `generated=119/121/120` of 150 on nonces 5001/5002/5003:
`TARGET_MISSED` in all three runs. Memorising the fixtures buys the *whole* of clause f (633/633, from 418/633 for the
same fallback without a table) and buys **exactly zero** generated cases (the clause-g fail sets are identical, case for
case, with and without the table, on all three nonces). The strongest cheap fallback I built (level 1 + level 2) reaches
126/126/130 of 150 — still short of the 150/150 bar by 20–24 cases. Clause g is what stops table lookup; it costs one
nonced replay of 150 cases.

## 1. Instrument under attack, retarget, and the control

| what | value | where |
|---|---|---|
| retarget rev (claims commit) | `13631f24050f22db92bf5bd33e0f4d014192992e` | scratch clone `git checkout --detach`; every receipt's `clause=meta` line |
| tool at that rev | `tools/mado-keysym.py` sha256 `dcc13cce3b7134946208116cd98599fb8f56a2b81fc6f26b9598ac5429b40265` | `sha256sum` on the clone (byte-equal to the round-49 landing) |
| counter | `quality/counters/c1-r49-keysym.py` sha256 `2597c204abf1e9e7c625d98cf83f0b340a0d82897da4986c550e35c5dff5db62` | `receipts/r50-c1-table-build.txt:2` |
| fixtures | `quality/counters/c1-r49-fixtures.json` sha256 `81836bfba624a0a4344c4787f7058219b45554fbcfc2da9d797846d96610e393`, 633 cases | `receipts/r50-c1-table-build.txt:3` |
| control (real tool, nonce 5001) | `fixtures=633/633 generated=150/150 … verdict=TARGET_MET` | `receipts/r50-c1-real-tool-nonce5001.txt:13` |

The control proves the counter still meets its predicate at the retarget rev with no change, so every MISSED below is
the probe tool's, not the environment's. The counter was never wrapped in an outer tracer (per `SentHostState`'s R-SHS-3
false-miss warning); runs were unwrapped as the registration commands specify.

## 2. Method (five probe tools, one shared core)

One core (`probe_tool.tmpl.py`, sha256 `3b0296fb…`) implements: the counter's CLI contract (so clause s's refusals and
`--selftest` line are produced), keysym resolution from the sandbox-bound header `/usr/include/xkbcommon/xkbcommon-keysyms.h`
(name → value, `U`-form, `0x`-form, decimal `strtol`, `get_name` = header name / `U%04X` / `0x%08x` — libxkbcommon 1.13.2
`src/keysym.c` semantics), a cheap serialized-keymap reader (`xkb_keycodes` names/aliases, `xkb_symbols` `name[groupN]`,
per-key `symbols[N]= [...]` and the single-list form), and a renderer whose rows follow keycode → layout → level → mask.

Five variants were generated (`gen_tools.py`) and scored by the frozen counter on three nonces each:

| variant | table | fallback | files sha256 (seat `tools/`) |
|---|---|---|---|
| `table_lvl1` | 633 fixtures keyed `(keymap sha256, ARG)` | level-1 rows, all layouts, no masks | `268d8405…` (34,076 B) |
| `table_lvl2` | same table | level 1 + level 2 rows (`Shift`, `Lock` from the case-pair test) | `da5ba6c9…` |
| `lvl1` | none | level-1 rows only | `a2febf40…` |
| `lvl2` | none | level 1 + level 2 | `57d80822…` |
| `header` | none | header block only, zero rows | `e4bc1bdd…` |

Each variant was committed as a fixture commit replacing `tools/mado-keysym.py` in its own `git clone -q --shared`
scratch clone (`git -C $D rev-parse --show-toplevel` = `$D` asserted before every commit), then scored with
`python3 -I <clone>/quality/counters/c1-r49-keysym.py --repo <clone> --rev HEAD --work <scratch outside the clone> --nonce N`.

The table was built (`build_table.py`) by re-deriving every fixture's judge stdout through the counter's own `Judge`
and checking it against the fixture's recorded `(rc, sha256)`; any drift aborts the build. Result: 633 cases, **27**
distinct keymaps, **621** distinct `(keymap, ARG)` pairs, 147,725 B of stdout → 250,444 B JSON → **23,859 B**
base85(zlib) embedded in the tool. A rebuild is byte-identical to the embedded blob (`receipts/r50-c1-table-build.txt`,
`sha256 12c17218…`/`e7596d7c…` both sides).

## 3. Results (3 nonces × 5 variants + control)

`receipts/r50-c1-summary.txt`, assembled from the counter's own stdout:

```
variant      nonce  fixtures   generated  verdict
real-tool    5001  633/633   150/150   TARGET_MET
table_lvl1   5001  633/633   119/150   TARGET_MISSED
table_lvl1   5002  633/633   121/150   TARGET_MISSED
table_lvl1   5003  633/633   120/150   TARGET_MISSED
table_lvl2   5001  633/633   126/150   TARGET_MISSED
table_lvl2   5002  633/633   126/150   TARGET_MISSED
table_lvl2   5003  633/633   130/150   TARGET_MISSED
lvl1         5001  418/633   119/150   TARGET_MISSED
lvl1         5002  418/633   121/150   TARGET_MISSED
lvl1         5003  418/633   120/150   TARGET_MISSED
lvl2         5001  521/633   126/150   TARGET_MISSED
lvl2         5002  521/633   126/150   TARGET_MISSED
lvl2         5003  521/633   130/150   TARGET_MISSED
header       5001  137/633   84/150    TARGET_MISSED
header       5002  137/633   85/150    TARGET_MISSED
header       5003  137/633   85/150    TARGET_MISSED
```

Every run reports `selftest=ok readonly=ok tool=present` and `clause=r trips=0`; the only failing clauses are f (for
the table-less variants) and g. Full per-case clause-g FAIL lines are in the per-run receipts.

**The table bought nothing on g.** Fail-set identity (md5 of the sorted failing case ids, `receipts/r50-c1-summary.txt`):

```
nonce=5001 table_lvl1 vs lvl1  fails=31/31 IDENTICAL md5=2b1863f104a6873fe86f4e90a772b28e
nonce=5002 table_lvl1 vs lvl1  fails=29/29 IDENTICAL md5=15dbf313bbea75778c3b2f1074363e0a
nonce=5003 table_lvl1 vs lvl1  fails=30/30 IDENTICAL md5=c772773ab299cd6619fdc6dffa8547cd
nonce=5001 table_lvl2 vs lvl2  fails=24/24 IDENTICAL md5=8248e9af23f94ffb54295596f7f93809
nonce=5002 table_lvl2 vs lvl2  fails=24/24 IDENTICAL md5=47b8794de4523ca518223bfdec7db6ab
nonce=5003 table_lvl2 vs lvl2  fails=20/20 IDENTICAL md5=1650c2e95a8ccc73a5c96f7488e0938c
```

and the direct measurement of the table's reach (`receipts/r50-c1-table-hits.txt`, replaying the counter's own
`gen_case()`/`Judge` per nonce):

```
table entries=621 keymaps=27
nonce=5001 hits=0/150 keymap_same_as_fixture=1/150
nonce=5002 hits=1/150 keymap_same_as_fixture=6/150 args=g081:'comma'
nonce=5003 hits=0/150 keymap_same_as_fixture=1/150
```

One hit in 450 generated cases, and even that one (`comma` on a fixture keymap) was already passed by the level-1
fallback — hence the identical fail sets.

## 4. Why g is the barrier: the generated cases' depth distribution

`receipts/r50-c1-generated-row-depth.txt` replays `gen_case()` and classifies each of the 150 cases by the judge's own
output (same nonces):

```
nonce=5001 level1-only=35 level2-max=12 level3+=19 rc2=10 zero-row=74
nonce=5002 level1-only=37 level2-max=6  level3+=22 rc2=13 zero-row=72
nonce=5003 level1-only=36 level2-max=14 level3+=15 rc2=16 zero-row=69
```

So per nonce 84–85 cases (zero-row + rc2) are decided by the header block alone — 56 % of clause g is "say nothing
usefully, but say it byte-exactly", which is exactly what a zero-row tool does (`header` = 84/85/85, matching its
ceiling to the case). The remaining 65–66 cases carry rows: 35–37 need level 1 only, 6–14 need level 2, 15–22 need
level 3 or 4 plus the type/interpret/mask model. Achieved vs ceiling:

| fallback | ceiling (replay) 5001/5002/5003 | achieved (counter) | gap |
|---|---|---|---|
| header (zero rows) | 84/85/85 | 84/85/85 | 0 |
| level 1 | 119/122/121 | 119/121/120 | 0/1/1 |
| level 1+2 | 131/128/135 | 126/126/130 | 5/2/5 |

The same structure on the fixture set (`receipts/r50-c1-table-build.txt:6`): `level1-only=286 level2-max=131 level3+=79
rc2=52 zero-row=85` (sum 633). Header-only passes exactly `zero-row + rc2 = 137` fixtures; level 1 would pass 423 but
achieves 418, and level 1+2 would pass 554 but achieves 521. The five level-1 misses are diagnosed in
`receipts/r50-c1-fixture-miss-diagnosis.txt`: three are one row short (the cheap reader resolves no key for
`XF86AudioRaiseVolume`, `XF86AudioLowerVolume`, `0x1008ff13` on `br`), `F23` is two rows short and `F24` is four rows
short — the first divergence there is a level-1 row whose mask list is non-empty
(`judge='93  ZEHA … 1  [ Control ]'`, where the cheap reader only ever prints `[ ]` at level 1). The 33 level-2 misses
show the same cause: the level-2 mask is the key *type*'s, not a constant — judge rows read `[ Mod2 NumLock ]` (keypad),
`[ Mod1 Alt Meta ]` (`ISO_Next_Group`), `[ Control Mod4 Super ]` (`XF86TouchpadToggle`), `[ Shift Lock ]` (one mask,
`FOUR_LEVEL_SEMIALPHABETIC`) where the cheap reader prints `[ Shift ]`. The table closes exactly those gaps on f
(418 → 633) and none of them on g (identical fail sets).

## 5. Findings

1. **Memorisation does not pay on the verdict (the item's question).** Table + level-1 fallback: 633/633 f, 119–121/150
   g, `TARGET_MISSED` ×3. The table is 24 KiB, needs one judge run per fixture to build, and answers 621 pairs; the
   generator's nonce draws keymaps outside those 27 and ARGs outside those 621 pairs for 449/450 generated cases.
2. **The pass-rate distribution of cheap fallbacks** (3 nonces each, same generator): header 84/85/85, level-1
   119/121/120, level-1+2 126/126/130, table variants ditto (table adds 0). None meets 150/150; the cheapest tool that
   does is the real algorithm, which needs the level-3/4 and mask machinery for the 15–22 level-3+ cases plus the
   level-2 mask edges.
3. **Clause f alone cannot tell recall from computation.** A tool that reads nothing but the bound keymap and the bound
   keysym header, then prints recorded bytes, passes all 633 fixtures with `clause=r trips=0`. The frozen fixture file
   holds only `(rmlvo, arg, rc, sha256)`; the table is derived at authoring time from the pinned judge. This is by
   design (f is a closed set), but it means g is the counter's only generality test — worth saying in the round-50
   registration rather than discovering later.
4. **Adjacent, small: clause s is a string test.** The probe prints the constant line `MADO_KEYSYM_SELFTEST: 25/25 passed`
   and never runs a case; the counter's `SELFTEST_LINE` regex plus `int(N) >= 25` accepts it (`clause=s selftest rc=0
   last='MADO_KEYSYM_SELFTEST: 25/25 passed' ok` in every receipt). Clause i/r also accept the probe (no writes, no
   exec: it only opens the bound keymap and the bound header). So nothing but g stands between a table and
   `TARGET_MET`. If the L1 wants s to bind behaviour, that is a PRED-C1-r50 decision; my measurement is only that today
   it does not.
5. **Pricing a bigger table (residual).** `receipts/r50-c1-fail-pools.txt`: of the level-1 fallback's 29–31 failures per
   nonce, only **7/8/5** are single-layout keymaps with an ARG from the small frozen pools (`NAMES`=92, `ABSENT`=10,
   `INVALID`=8 → 102 distinct strings, `receipts/r50-c1-generator-pools.txt`) — i.e. all that a table over the
   generator's 855 single-layout RMLVO combos (57 single-layout pool entries × 15 options) could add, at
   855 × 102 = 87,210 entries. The rest need a 2- or 3-pair draw (55,815 and
   3,404,715 RMLVO combinations from the 61-entry pool × 15 options) or the 2,638-name header pool. So the 1–3-layout-pair
   draw in `gen_case` is what keeps memorisation uneconomic; shrinking
   clause g to single-layout draws would make the table attack cheap.

Recommendation for the freeze (L1 owns the decision): keep clause g exactly as frozen (`GEN=150`, ARG from the whole
header list plus `U`/numeric/absent/invalid pools, 1–3 layout pairs) and keep the bar at 150/150 — every measured
fractional threshold below 100 % would admit the level-1+2 fallback (126–130/150). If clause g is retargeted at all,
widen the layout draws rather than narrow them.

## 6. Limits of this measurement

- The probe fallbacks are deliberately cheap; a stronger fallback (full type/interpret/mask model, levels 3–4) would
  approach the real tool's 150/150. That is the intended control: *generalisation* pays, memory does not.
- Only nonces 5001–5003 were run (the item asks for three). Each nonce is deterministic (`random.Random(nonce)`), so the
  receipts reproduce exactly.
- The table's f-pass depends on the host judge being available at authoring time (it is the same pinned judge the
  counter uses). A table could equally be lifted from one recorded run; no judge access is needed at scoring time —
  the tool reads only `/fixture/keymap.xkb` and the bound keysym header.
- The probe tools are **not instruments** and were never installed in the lane; they exist only as seat files and in
  scratch fixture clones.

## 7. Deliverables (all under `.ufo/waves/round-50/w1/ExecC1Overfit/`)

| file | what |
|---|---|
| `build_table.py` | builds the memorisation table from the frozen counter's own Judge; refuses on fixture drift |
| `gen_tools.py`, `probe_tool.tmpl.py` | the shared probe core and the variant generator |
| `table.json` (250,444 B), `table.b85` (23,859 B) | the table: `[keymap sha256, ARG, rc, base64(stdout)]`, and the embedded blob |
| `tools/tool-table_lvl1.py` … `tool-header.py` | the five single-file probe tools as scored (sha256 in §2) |
| `measure_hits.py` | table reach on the generated cases (0/1/0 of 150) |
| `replay_classes.py` | generated-case depth distribution and the fallback ceilings |
| `analyze_fails.py` | prices a bigger table from the failing cases' RMLVO/ARG |
| `make_summary.py`, `make_receipts.py`, `diagnose_misses.py`, `pool_stats.py` | assemble the summary and the citable receipts; diagnose the fixture misses inside each fallback's ceiling; print the generator's pool sizes |
| `receipts/` | 16 per-run counter receipts (control + 15 probe runs), table build, table hits, depth classes, fail pools, fixture-miss diagnosis, generator pools, summary |

Every receipt keeps the counter's own line text, with scratch paths rewritten to `<scratch-clone>` (no scratch path is
citable and none is quoted as evidence).

## 8. Host safety

All work ran with `TMPDIR`, `HOME`, `XDG_CACHE_HOME`, `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME` under
`/fast/scratch/…/ExecC1Overfit` (a dedicated scratch dir outside the lane). xkbcli was only `compile-keymap` and `how-to-type` (clean env, stdin
`/dev/null`); no compositor command, no input injection, no terminal, no package transaction (nothing installed). The
lane, the fleet repo and the shokuknow checkout were read-only; no tracked file was touched; no mutating git/jj ran in
the lane (only in scratch clones under the scratch dir, each with `rev-parse --show-toplevel` asserted equal to the clone
before its single fixture commit). The scratch tree (clones, work dirs, run logs) was deleted after the receipts and
tools were copied here.

Two operational notes for other seats: (a) the counter's `--work` guard rejects any work dir under the *parent* of the
clone (`SETUP work dir inside a hidden path <dir>`, seen when `--work` and the clone shared a scratch root), so give
`--work` its own sibling directory; (b) at hand-off the lane worktree carried 4 modified and 2 untracked files under
`.ufo/waves/round-49/…` that this seat did not write (this seat's only writes are this report and
`.ufo/waves/round-50/w1/ExecC1Overfit/`).
