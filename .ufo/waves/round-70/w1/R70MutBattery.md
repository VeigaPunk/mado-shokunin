# R70MutBattery — mutation battery over the round-70 instruments

seat: `R70MutBattery` (mado round 70, wave w1) · axes: **C1 calibration**, **C2 operability**
lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` · date 2026-11-04 (America/Sao_Paulo)
scratch: `/fast/scratch/hyaku/mado-r70/R70MutBattery/` (removed; §7)

No production path was written, no lane file was modified, no tool was installed, no git
state was mutated in the lane or the fleet repo. Every mutant is a copy under scratch; the
lane instruments are only ever read (and read through the frozen commands below).

## 1. Byte set measured

The seat names `5144a6b5f43225d8021a469f4d24c19558026b9e` as the scored-instrument revision.
The lane **advanced during this seat** (HEAD `5144a6b` → `3aea1e10`, commit
`round-70: harm-watch battery …`, 2026-11-03 23:35:34 -0300), with three pre-data commits
`9508e878`, `5adba5a9`, `71caa8b7`. Both revisions were therefore measured; the three contract
lines are identical modulo `rev=`.

| instrument | sha256 @5144a6b | sha256 @3aea1e10 = disk |
|---|---|---|
| `quality/counters/c1-r70-landing-controls.py` | `71a7b6c45b904a734f194be9a8de6cc2eeb5f5ea1922760f908f5637f1d4db58` | same |
| `quality/counters/c1-r70-real-children.py` | `b1785f388724c8f0a21dda016da2e212105354221767eaa128fa73c3ddaaebb4` | `b3a6f131abf371ecf64273b65a143478c4b23eaa7acf974ec80e5efebf6e6a7b` |
| `quality/counters/c2-r70-carriers.py` | `87ca466432302feaabf2c504dc131184178afe199d8b84fa492ad3b5211af9f7` | `d868ae334b794f99544bd41b1265a9ee6bb5a380278755c6d1223630abd21363` |

Deltas, neither of which touches a mutated expression:
`c1-r70-real-children.py` + 1 line (`os.makedirs(scratch, exist_ok=True)` in `run_harness`);
`c2-r70-carriers.py` `score_cases(..., leg=…)` + `leg=` in the emitted `MADO_R70_CONTROL` line
(observability only). Mutants were built from the **disk (HEAD) bytes**; the driver asserts the
target substring occurs exactly once before replacing.

Frozen inputs used unchanged: `.ufo/waves/round-70/controls/c2-controls-r70.json`
(`29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff`, 17 cases),
`.ufo/waves/round-70/control-baseline-r70.txt`, `.ufo/waves/round-70/claims-declaration-r70.md`.

## 2. Baselines (committed instruments, run normally)

Self-tests (hermetic):

| command | rc | last line |
|---|---|---|
| `c1-r70-landing-controls.py --selftest` | 0 | `MADO_R70_LANDING_CONTROLS_SELFTEST: 68/68 assertions passed` |
| `c1-r70-real-children.py --selftest` | 0 | `MADO_R70_REAL_CHILDREN_SELFTEST: 26/26 assertions passed` |
| `c2-r70-carriers.py --selftest` (no `--controls`) | 0 | `MADO_R70_GUARD_CARRIERS_SELFTEST: 47/47 assertions passed` |
| `c2-r70-carriers.py --selftest --controls …` | 0 | `MADO_R70_GUARD_CARRIERS_SELFTEST: 49/49 assertions passed` |

The C2 mutants were run **with** `--controls` (the frozen file), so their like-for-like
baseline is **49/49**, not 47/47.

Full measurements, `--rev` pinned at each revision:

```
c1h  rc=0  MADO_R70_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET rev=<rev>
c1c  rc=0  MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET rev=<rev>
c2   rc=0  MADO_R70_GUARD_CARRIERS: population=20 readers=13 guarded=13 unguarded=0 controls=17/17 base_controls=13/17 verdict=TARGET_MET rev=<rev>
```

Both `rev=5144a6b5f43225d8021a469f4d24c19558026b9e` and
`rev=3aea1e10aad3365ca1b648ddfba7e6b1818970fc` produced the same three lines. Independent C2
evidence lines at the pristine run: `MADO_R70_CONTROLS cases=17 sha256=29947b4c…`,
`MADO_R70_HELD_CONTROLS path=.ufo/waves/round-69/controls/c2-controls-r69.json cases=11
sha256=975ca3ba… carried=yes`, `MADO_R70_BASE controls=13/17`.

## 3. Method

Per mutant: copy the instrument into `mut/<id>/`, apply one exact substring replacement
(`count(find) == 1`, asserted), record the mutant sha256, run
`python3 <mutant> --selftest --scratch-root <S>/st/<id> [--controls <frozen>]`, and capture
`SELFTEST FAIL` lines plus the summary. Survivors were then run as the **full measurement**
against the lane repo (the real fixture) at pinned revs; where the real input cannot expose
the defect, the flip was demonstrated on a scratch fixture repo (`fixture-c1`, `fixture-c2`,
built with `git init`, explicit `-c user.name/user.email`, `-C` on every git call, toplevel
asserted equal to the fixture dir).

## 4. Kill matrix

20 single-point mutants: 7 on the C1 harness, 5 on the C1 counter, 8 on the C2 counter.
**14 killed by `--selftest`; 1 selftest-survivor killed by the measurement; 5 survivors.**

| id | instrument | mutation | selftest | first failing assertion(s) | real/fixture printed-line effect |
|---|---|---|---|---|---|
| c1h-a | harness | `mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))` → `bool(mz_rc != 0)` | **KILLED** 66/68 | `a crashing M-Z child is not a kill (a parsed failed assertion is required)`; `an M-Z run whose summary reports no failure is not a kill` | – |
| c1h-b | harness | `summary_shows_failure` → `return True` | **KILLED** 62/68 | the two above + `summary 2/2 shows no failure`; `garbled summary shows no failure`; `absent summary shows no failure`; `zero-total summary shows no failure` | – |
| c1h-c | harness | `summary_shows_failure` → `return False` | **KILLED** 64/68 | `scripted both-killed prints the met line`; `scripted both-killed exits 0`; `a crashing M-R child is not a kill (decision + oracle pair)`; `summary 1/2 shows failure` | – |
| c1h-d | harness | `passed < total` → `passed <= total` | **KILLED** 66/68 | `an M-Z run whose summary reports no failure is not a kill`; `summary 2/2 shows no failure` | – |
| c1h-e | harness | summary regex `re.fullmatch` → `re.search` (l. 323) | survived 68/68 | – | contract line byte-identical, rc 0 → **R1** |
| c1h-f | harness | sha guard `re.fullmatch` → `re.search` (l. 213) | survived 68/68 | – | contract line byte-identical, rc 0 → **R2** |
| c1h-g | harness | fixture-rev guard `re.fullmatch` → `re.search` (l. 389) | survived 68/68 | – | contract line byte-identical, rc 0 → **R3** |
| c1c-a | counter | `score()` → `return got is not None` (answer compared with itself) | **KILLED** 24/26 | `crash pass is a false credit`; `garbage pass is a false credit` | – |
| c1c-b | counter | `base_ok = score(…)` → `mode == MODES[0]` (base_correct forced to 1) | survived 26/26 | – | real line byte-identical, rc 0 → **R4** |
| c1c-b2 | counter | `base_ok = score(…)` → `True` (base_correct forced to 3) | survived 26/26 | – | **measurement-killed**: `base_correct=3 verdict=TARGET_MISSED`, rc 1 (see §6.2) |
| c1c-c | counter | `verdict_met` → `correct >= 2` | **KILLED** (crash) | no printed FAIL: uncaught `TypeError: '>=' not supported between NoneType and int` at the `absent line parses` check (`contract_line(None, 0, …)`) | – |
| c1c-d | counter | `EXPECT["crash"]` → `"pass"` | **KILLED** 25/26 | `expectations` | – |
| c2-a | counter | `carrier_guard` → `return True` | **KILLED** 32/49 | six of 17: `classify value-position-only is (True, False)`, `dead-branch-only`, `uncalled-helper`, `overwritten-env`, `mention-only`, `guarded-env-for-a-non-git-call` (each `is (True, False)`) | – |
| c2-b | counter | `carrier_guard` → `return False` | **KILLED** 45/49 | `classify alias-carried is (True, True)`; `attribute-carried`; `splat-carried`; `constant-key` | – |
| c2-c | counter | alias detector removed (`alias_guard_lines` → `{}`) | **KILLED** 48/49 | `classify alias-carried is (True, True)` | – |
| c2-d | counter | attribute detector removed (`attribute_guard` → `False`) | **KILLED** 48/49 | `classify attribute-carried is (True, True)` | – |
| c2-e | counter | splat detector removed (`splat_guard_lines` → `{}`) | **KILLED** 48/49 | `classify splat-carried is (True, True)` | – |
| c2-f | counter | constant-key detector removed (`const_key_names` → `set()`) | **KILLED** 48/49 | `classify constant-key is (True, True)` | – |
| c2-g | counter | `held_check` → `return 0` (guard dropped) | survived 49/49 | – | contract line byte-identical, rc 0; the `MADO_R70_HELD_CONTROLS … carried=yes` evidence line **disappears** → **R5** |
| c2-h | counter | `verdict_met` drops `and base_controls == FROZEN_BASE_CONTROLS` | **KILLED** 48/49 | `verdict requires the frozen base-control score` | – |

Mutant/diff digests (full 64-hex in `R70MutBattery/mutants.json`):

| id | mutant sha256 | diff sha256 |
|---|---|---|
| c1h-a | `4c3e9021a17c56afc3eea8fad2cd8f09cc24eef6bf53d960fb9b42bdb7b178bc` | `bc98a68921a868698341fe68dfcf1eab9d08d7e0d874eef95f7f09fcab6e693a` |
| c1h-b | `b864642a62bba71eca3dc225a02041daaa21cf1694618217f179a90bc2ba5fbe` | `fc8918dec68ba6e0bf23a162ba595d22a35c4489fea8849decac0fd8272986c1` |
| c1h-c | `795c1bc2e0b8ffccf8657195891c993701e740269b6f617dadb9881cd476a4a1` | `32a8e707b3a5f0d8b5d061f6308507e0538584dae9cfaaa4f575cfcbc20cccc2` |
| c1h-d | `c77bb3a3ea45397f0e20d9f83685224adb9bf79206942f27105651bc9207e695` | `a6e10d7108e927c30bc815ccbcc5f42aca1760556e4e17246f07a1f9015691bf` |
| c1h-e | `2ff8224964ae3e47490ae998c2854d9688c4ee2581c57e81349c73b8db398288` | `cae2e70e00387819c1b73be55ef373bbe501a69d0d74b4dbd582648951b82349` |
| c1h-f | `ffb1b61ba4d5bcb29755d76b5f51ea0d4831e0e29f5511d19fb0a82e3289f7b1` | `0eb88e9aca1663411fca0f49cc7db2308f181bb68405784a0fa4376211fb32a8` |
| c1h-g | `094a3666148b3c66277e45dc2b6f39949506c6836ad1e6ad81aa98af723410e6` | `b7b05fc50d2c2f893680633934ec1f903896d8e83fae37c5ad1af945c90ce325` |
| c1c-a | `e10e84361ec0b9c29fe1644ff15eb8a1f5dc7e41f0bedf23e73f153711b1dc96` | `110ee013f407683a8ba1ace6d9b7e23d9a03ca5151016314e75eebefee864e42` |
| c1c-b | `f581f03145eec6526a28903bfa344f2ab8e44c1b81d3b0a570258b5167ead907` | `2d0ba42b81eed89dce656a9b6580851fd39fbea92cec66aa44da8fc5cbc4ad0d` |
| c1c-b2 | `32af200a2067bdaa94dd9292b09e23089aade71f04b8c764fab731cd8b940c7e` | `34564cfcbbb5b95628058f84cd991e10075678930a2be871d87825e255800bd2` |
| c1c-c | `8d4c3627bfa6233afdab26c1f1ddc8550064219ff6ad13c7156f5cf7d50c4a39` | `e069e611ec76f586cabfec351d5ec6254195bf7282191a623bbd4f072300eb69` |
| c1c-d | `9bc7240617706750b95b1904e12145068f202a2697ed97bdc8354d31f1a25ac4` | `94cc0e575335d40f62bbfa23ff564887e63914fcc976cbd1e38d094ef3ac3dc4` |
| c2-a | `7fb049d1428fe9e583ae0f3fbc73595dcf3dd02372630ae98d2bbaf005d02009` | `84138ff48c99c9fd0ab6608b30caf3101bafe37ff9ce2daa9d02693907430f1a` |
| c2-b | `b5804ae2ef44b078cd43f2b0306ac160b760ff5653911096d77a260f9813884b` | `bdc19f550bbf67517664a93ba2abc95e9b673824bea2ec9a0ce4d52dcfa7eab1` |
| c2-c | `5c2540fdebbef2828092c5d8908449b0e067e04e75ab2dc17989e6305c3bad7e` | `b6bf6f6d71a6e1fea164a2736dcc029b22b7f09e445eb5cae40264ccf0fec273` |
| c2-d | `f760d074490294956da364bcb533952c01338b3689901b519cf32f09cf0dcf50` | `9b0714e91d45d1691913907c1ef840f16d2d38f99f2b596850d8a0cc5bc78547` |
| c2-e | `ae3dfc835431a303247a0c76e4642f48590261b0e600e10924695a343ca34d41` | `453b596cb4fe44798170ea809a158e7481cc4883b9021a30936660223050b3b3` |
| c2-f | `5bf1424b75a1ec10a9865d7788bdba7da5a9267df2cde5e3e9618623eb7906a9` | `4832527989fb61884b1aead7d8b3ae24496fb73cc05d5403118ff160e8d19c0d` |
| c2-g | `c5d1322484fa005c7ce173f275803be82f7be4357c4f243724b3896a8f81ae0e` | `e5cd4e0ecdc1866d0befb35abcb467f0f91a3e15ca2d1923a7d571ab52db927c` |
| c2-h | `eb852370d04b9fcba577f372790c031c2bf3c08ffe2c285d3410e5efa4c4ec97` | `26ce54fb970f9a38b4d48e349f963118abc829a9d5b556c3cc289eb57c0fb848` |

## 5. Residuals (survivors)

Each residual names the input at which the mutated predicate and the frozen predicate disagree;
none of them is exercised by the committed detectors on the committed inputs.

**R1 — `c1h-e`, summary regex `fullmatch` → `search`** (mutant `2ff82249…`, diff `cae2e70e…`).
The M-Z child's own summary must *end* at `assertions passed` for the parse to differ. Flip
condition: a summary line with a trailing suffix, e.g.
`MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed (interrupted)`.
Probe (imported both modules, called the predicate): pristine `summary_shows_failure(line)`
= `False` (no kill credit), mutant = `True` (kill credit). The committed fixture lane never
emits a suffix, so the full measurement is unchanged (`mz=pass`, rc 0).

**R2 — `c1h-f`, `--rev` sha guard `fullmatch` → `search`** (mutant `ffb1b61b…`, diff `0eb88e9a…`).
Flip condition: `git rev-parse --verify` output that is not a bare object id but *contains* a
40–64 hex substring, e.g. `zz` + 40×`a` + `zz`. Probe (`resolve_rev` with `run` stubbed to emit
that string and the real toplevel): pristine raises
`SetupError: --rev resolved to an unexpected object name`; mutant returns
`zzaaaa…aaaaaz` and proceeds to the toplevel check. Unreachable on a well-behaved git.

**R3 — `c1h-g`, fixture-rev guard `fullmatch` → `search`** (mutant `094a3666…`, diff `b7b05fc5…`).
Same predicate, second call site (`build_r_fixture`, l. 389). Flip condition: the fixture's own
`rev-parse HEAD` output carries a 40-hex substring inside a longer malformed string; the harness
computes that id itself, so the flip needs corrupted git plumbing output. Not separately probed
— identical expression and identical failure mode as R2.

**R4 — `c1c-b`, base leg hardcoded to 1** (mutant `f581f031…`, diff `2d0ba42b…`).
`base_ok = score(EXPECT[mode], base_got)` → `mode == MODES[0]`; the `base_correct` column is no
longer measured. On the real fixture the true base score *is* 1, so the printed line is
byte-identical (`base_correct=1 verdict=TARGET_MET`, rc 0) — invisible.
Flip condition: a `--base-rev` harness that scores 3/3. Demonstrated on scratch `fixture-c1`
(base `142ff4f750917f43dda820c33f6307976a39e546` = a repaired, `MADO_R69_`-prefixed harness
that is correct on all three scenarios; rev `e9aba639c5f1923fae749385fc46240d91ee5bca`):

```
pristine  rc=1  MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=3 verdict=TARGET_MISSED rev=e9aba639…
mutant    rc=0  MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET rev=e9aba639…
```

The mutant turns a rejected base into a false green. Internal tell, not enforced: its
`MADO_R70_SCENARIO` lines report `base_correct=no` for `crash` and `garbage` while the aggregate
prints `base_correct=1`.

**R5 — `c2-g`, `held_check` guard dropped** (mutant `c5d13224…`, diff `e5cd4e0e…`).
Flip condition: the `.ufo/waves/round-69/controls/c2-controls-r69.json` at `--rev` has any digest
other than `975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9` (or is absent, or
carries ≠ 11 cases). Demonstrated on scratch `fixture-c2` (base
`cd75fd9af65a6e468e91c33646802907776ee496`; pristine rev
`bd0a4a1a8ad940386cca81867a2c8b9960a5a62b`; tampered commit
`601b105b944ff841604063ce2a2212136c8019ee` = the held file plus one trailing space, digest
`0ae1e02754cf2108d2827f598dfe2896e49f4f7a3748b922ac7b37a594fc5fad`, still 11 parseable cases):

```
pristine  rc=2  c2-r70-carriers.py: held controls sha256 0ae1e027… does not match the frozen digest
mutant    rc=0  MADO_R70_GUARD_CARRIERS: population=20 readers=13 guarded=13 unguarded=0 controls=17/17 base_controls=13/17 verdict=TARGET_MET rev=601b105b…
```

On the pristine fixture (`rev=bd0a4a1a…`) the mutant's contract line is identical to the
pristine's and rc stays 0; the only visible delta is the missing
`MADO_R70_HELD_CONTROLS … carried=yes` line.

## 6. Mechanics worth recording

1. **c1c-c is a crash kill, not an assertion kill.** `verdict_met` with `correct >= 2` raises
   `TypeError` when the selftest builds `contract_line(None, 0, …)` (the `absent line parses`
   check) before any FAIL can print. rc=1 is a kill, but the detector's evidence is a traceback.
2. **c1c-b2 is selftest-blind but measurement-visible.** Forcing `base_ok = True` yields
   `base_correct=3`; the real fixture rejects it (`verdict=TARGET_MISSED`, rc 1). So the selftest
   alone cannot see base-leg loss, while the full measurement can — except for the R4 shape,
   which is calibrated to the expected value.
3. **The four carrier detectors are each individually load-bearing.** Removing any one drops
   exactly its one frozen case (48/49); removing all (`carrier_guard → False`) drops all four.
   No overlap was observed between the four detectors on the frozen cases.
4. **`carrier_guard → True`** is caught by the seven negative cases, not by the four carriers —
   the census is guarded in both directions.
5. The C1 harness selftest drives the real measurement body through `_scripted_run`, which is
   why the mz/mr decision mutants (a–d) are visible without spawning.

## 7. Reproduction and cleanup

Exact commands (all from the lane root unless stated):

```
python3 quality/counters/c1-r70-landing-controls.py --selftest --scratch-root "$S/st-c1h"
python3 quality/counters/c1-r70-real-children.py --selftest --scratch-root "$S/st-c1c"
python3 quality/counters/c2-r70-carriers.py --selftest --scratch-root "$S/st-c2" \
        --controls .ufo/waves/round-70/controls/c2-controls-r70.json

python3 quality/counters/c1-r70-landing-controls.py --repo . --rev <REV> --scratch-root "$S/bl-<rev>-c1h"
python3 quality/counters/c1-r70-real-children.py   --repo . --rev <REV> \
        --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 --scratch-root "$S/bl-<rev>-c1c"
python3 quality/counters/c2-r70-carriers.py        --repo . --rev <REV> \
        --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 \
        --controls .ufo/waves/round-70/controls/c2-controls-r70.json --scratch-root "$S/bl-<rev>-c2"

# per mutant (cwd = <S>/mut/<id>)
python3 <instrument> --selftest --scratch-root "$S/st/<id>" [--controls <frozen>]
# survivors, full measurement: same three commands, with <instrument> = <S>/mut/<id>/<basename>
```

Scratch fixtures: `fixture-c2` (2 commits pristine + 1 tampered held-controls commit) and
`fixture-c1` (repaired-base commit + r70-instrument commit); every git call used `-C <fixture>`
and an explicit `-c user.name=r70-mut -c user.email=r70-mut@example.invalid -c commit.gpgsign=false`,
with `git rev-parse --show-toplevel` asserted equal to the fixture directory before the first
commit.

Lane integrity after the battery: the three instruments re-hash to
`71a7b6c4…` / `b3a6f131…` / `d868ae33…`, `git diff` shows no tracked change under `quality/`,
`quality/counters/`, `.ufo/waves/round-70/`; `c2-controls-r70.json` and
`control-baseline-r70.txt` still hash to `29947b4c…` / `675b18df…`. The working-tree
modifications present at seat end (`SCORECARD.md`, `corpus/SOURCES.md`) appeared during the
seat from outside it and were not written by me.

Seat artifacts (in `.ufo/waves/round-70/w1/R70MutBattery/`):

| file | sha256 |
|---|---|
| `mutants.json` (20 mutant records: pristine/mutant/diff sha256, rc, FAIL lines) | `e831bf78d4ac80e6e669843479b974551fd771f8f664a270ea184bf1a4dcc898` |
| `probes.json` (R1/R2 differential probes) | `7e6602d998ed9e61cd15de4434f3fab000c31c653c0eb7cc1dbd4b4e3568dff1` |
| `mutate.py` (battery driver) | `78264fce3b6aeb5e23f878c32ada789dcf3b7043efef4426fcad1c18ac9e25b8` |
| `probe.py` | `529df14e1bf7c735de644f51195c12cf5d36cf1cd302d68d9851d7f82467e3d4` |

No production draft was produced by this seat (mutants live only in scratch); no tool was
installed or upgraded.

**Scratch-cleanup receipt.** `/fast/scratch/hyaku/mado-r70/R70MutBattery` was removed with
`rm -rf --` at seat end; `test ! -e` confirms absence. No file was written to `/tmp`,
`/var/tmp` or `/dev/shm`; `TMPDIR` was never relied on.

## 8. Not claimed

Universal fault coverage; that these 20 mutants bound the defect space of the three instruments;
that a survivor is a bug (it is a detection blind spot at the named input, and the instrument
still scores the committed targets); any behaviour of the instruments outside the invocation
forms above; any claim about the round-70 verdict, promotion or axis retirement.
