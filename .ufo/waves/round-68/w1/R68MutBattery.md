# R68MutBattery — independent mutation test of the two round-68 counters

Seat: mutation-tester (leaf). Scratch: `/fast/scratch/hyaku/mado-r68/R68MutBattery/` (removed at
the end; receipt in §8). No lane file, sibling lane, fleet file, MANIFEST, state directory or
package manager was written. No commits, pushes, stages or git/jj mutations in the lane.

## 1. Instruments under test (exact bytes)

| instrument | rev | sha256 |
|---|---|---|
| C1 counter `quality/counters/c1-r68-selfmutants.py` | `425d4b2f` (= `40d2bef8`, unchanged) | `bdea8dc6b4455f45c59896a44f0bd4ede21c26b82c67e0618a05ac069ef50a85` |
| C2 counter `quality/counters/c2-r68-reader-guard.py` (landed) | `425d4b2f` (= `686d6345`) | `5a6b386545889e3b072740d1d5fa39b3a4c523661d4a788993d48d4607410faa` |
| C2 counter frozen bytes (declaration's instrument) | `e0727cda` | `8eb99a63e324fce18eda824d7aefa48d72650ff6abb7c4afa45def9191ce880e` |
| C1 scored harness at candidate | `425d4b2f` | `25470bc432ad3b612f08869052915f331d9a930149b3af6a9bf0e3eb87cf5527` |
| C1 do-nothing harness at base | `510100c8` | `a4376fa739405a213ccd59847620be02bec5fd2a70584aa59dfbc916022d9b58` |

The lane advanced while this seat ran (`40d2bef8` → `2a39e741` → `686d6345` → `425d4b2f` →
`18d692f3`). Every number below is pinned to the sha in the table, not to a moving HEAD; the two
instrument blobs are byte-identical at `425d4b2f` and `18d692f3` (`git cat-file blob` comparison).

## 2. Frozen-target verification (independent, not copied from the baseline receipt)

C1, base rev — `python3 -I quality/counters/c1-r68-selfmutants.py --repo . --rev 510100c8… --base-rev 510100c8… --scratch-root DIR` → rc 1, last line:

```
MADO_R68_SELFMUTANTS: selftest=absent killed=0/3 applied=0/3 base=0/3 verdict=TARGET_MISSED rev=510100c8…
```

C1, candidate rev `425d4b2f` → rc 0, last line:

```
MADO_R68_SELFMUTANTS: selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET rev=425d4b2f…
```

with `MADO_R68_SELF_MUTANT … recipe_sha256=7bacfa10…/867b4894…/dd284ac4… rc=1 assertions=51/52`,
`51/52`, `50/52` — the three harness mutants are really killed, and all three survive (rc 0,
47/47) on the base harness. The frozen target is real.

C2, base rev `510100c8` → rc 1:

```
MADO_R68_READER_GUARD: population=20 readers=13 guarded=1 unguarded=12 controls=11/11 verdict=TARGET_MISSED rev=510100c8…
```

C2, real repaired candidate `425d4b2f` (the twelve gates are committed there) → rc 0:

```
MADO_R68_READER_GUARD: population=20 readers=13 guarded=13 unguarded=0 controls=11/11 verdict=TARGET_MET rev=425d4b2f…
```

C2 on an independently built scratch candidate (`c0bb9e7a`, base blobs + a guard at each reader's
env construction, compile-checked) → the same line with `rev=c0bb9e7a…`, rc 0. So the target is
reachable from the base bytes by the declared repair, not only at the lane's candidate commit.

C2 frozen bytes reject the frozen command's `--scratch-root` (rc 2, `unrecognized arguments`) —
this seat independently reproduced the erratum already recorded at
`.ufo/waves/round-68/c2-command-erratum-r68.txt`; landed bytes accept it. Pristine selftest:
frozen bytes 17/17, landed bytes 25/25 (the baseline receipt's `17/17` matches frozen bytes only).

## 3. Method

* Mutants are single exact-string substitutions on the pristine counter bytes, asserted to occur
  exactly once, compile-checked, and stored as files. Selftest verdict = mutant `--selftest` rc.
* C1 measure probes use four scratch git repos built from the pristine blobs (toplevel asserted
  per repo): `c1-good` (base harness + candidate harness), `c1-dup` (S3 target duplicated),
  `c1-broken` (candidate `selftest()` forced to return 1), `c1-fake` (base harness copied to the
  candidate path, so no recipe changes its selftest), plus `c1-nobase` (candidate only, base
  harness absent at `--base-rev`).
* C2 measure probes use the scratch candidate above, the real candidate `425d4b2f`, and the lane
  base `510100c8`, each with the frozen `c2-controls.json`
  (`b7a1c939e5a715792d2969eb4ca86d8119cd5a72ef930d00d57338c62faf6a91`, never edited). One
  separate scratch probe `controls-probe-fail.json` flips `non-reader.expect_reader` to `true`
  only to exercise the verdict's control term; it is a detector probe, not the frozen set.
* No mutant ever touched the lane: counters were read, blobs extracted, and all writes stayed in
  `/fast/scratch/hyaku/mado-r68/R68MutBattery/`.

## 4. Kill matrix — C1 counter (`bdea8dc6`)

| # | mutant (one point) | selftest | target run (`c1-good`) | flip probe | verdict |
|---|---|---|---|---|---|
| a | `if args.base_rev:` → `if False and args.base_rev:` | rc 0, 26/26 — **survived** | line identical, rc 0, `MADO_R68_BASE_CONTROL` lines 0 (pristine 1) | `c1-nobase`: pristine rc 2 setup error vs mutant rc 0 TARGET_MET | **survived** |
| b | `recipe=none` counted as killed | rc 0, 26/26 — **survived** | line identical, rc 0 | `c1-dup`: pristine `killed=2/3 applied=2/3 … MISSED` rc 1 vs mutant `killed=3/3 applied=3/3 … TARGET_MET` rc 0 | **survived** |
| c | `died = rc != 0` → `died = rc == 0` | rc 0, 26/26 — **survived** | `killed=0/3 … base=3/3 … TARGET_MISSED` rc 1 (target line catches the inversion) | `c1-fake`: pristine `killed=0/3 … MISSED` rc 1 vs mutant `killed=3/3 … TARGET_MET` rc 0 | **survived** |
| d | `met` drops `result["rc"] == 0` | rc 0, 26/26 — **survived** | line identical, rc 0 | `c1-broken`: pristine `selftest=1 killed=3/3 … MISSED` rc 1 vs mutant `selftest=1 killed=3/3 … TARGET_MET` rc 0 | **survived** |
| e | `applied=` removed from the printed line | rc 0, 26/26 — **survived** | line lacks `applied=`, rc 0; frozen `CONTRACT_RE.fullmatch` False (pristine True) | exact-line comparator rejects the receipt | **survived** |

The counter's own `--selftest` exercises only `apply_recipe`, `CONTRACT_RE` and
`absolute_scratch`; it never calls `measure()` or `score_harness()`, so **0/5** scoring-body
mutants are killed by it.

## 5. Kill matrix — C2 counter (`5a6b3865`, landed)

| # | mutant (one point) | selftest | candidate `425d4b2f` | base `510100c8` | verdict |
|---|---|---|---|---|---|
| a | guard accepts any dict key (`n.value == KEY` dropped) | rc 1, 23/25 — killed (`unguarded dict is reader without guard`, `comprehension env is reader without guard`) | `guarded=13 unguarded=0 controls=9/11 MISSED` rc 1 | `guarded=9 unguarded=4 controls=9/11 MISSED` rc 1 | **killed** |
| b | comment/prose mention counts as guard (`if KEY in src`) | rc 1, 21/25 — killed (`comment mention is not a guard`, `docstring mention…`, `unrelated dict handed to env…`, `guard inside a non-env call keyword…`) | `controls=8/11 MISSED` rc 1 | `guarded=1 unguarded=12 controls=8/11 MISSED` rc 1 | **killed** |
| c | reader rule drops the verb requirement | rc 1, 23/25 — killed (`git init/add only is not a reader`, `git token without a verb is not a reader`) | `readers=15 guarded=13 unguarded=2 controls=10/11 MISSED` rc 1 | `readers=15 guarded=1 unguarded=14 MISSED` rc 1 | **killed** |
| d | population regex widened to `^quality/.*\.py$` | rc 0, 25/25 — **survived** | `population=88 readers=78 guarded=19 unguarded=59 … MISSED` rc 1 (base: 85/75/4/71) | line changes | **survived selftest; caught by the verdict only because population ≠ 20** |
| e | `unguarded = readers - guarded` → `unguarded = 0` | rc 0, 25/25 — **survived** | exact frozen line, rc 0 (indistinguishable from pristine) | forged `guarded=1 unguarded=0 … TARGET_MET` rc 0 (pristine `guarded=1 unguarded=12 … MISSED` rc 1) | **survived** |
| f | `verdict_met` drops `correct == controls_total` | rc 1, 24/25 — killed (`verdict requires every control correct`) | unchanged (all controls correct) | unchanged | **killed** |

## 6. Kill matrix — C2 counter frozen bytes (`8eb99a63`, the declaration's instrument)

Pristine selftest 17/17. a/b/c are killed (15/17, 13/17, 15/17). d/e/f **survive** 17/17.
`fz-f` is the notable delta: on the failing-controls probe the frozen counter prints
`controls=10/11 … TARGET_MISSED` rc 1 while `fz-f` prints `controls=10/11 … TARGET_MET` rc 0 —
the control score was outside the verdict in the frozen bytes. Commit `686d6345` moved the
verdict into `verdict_met()` with that term and a selftest case, which is why the landed bytes
kill f. d and e survive in both revisions.

## 7. Named residuals (survivors only; diff digest = sha256 of `diff -u pristine mutant`)

| id | mutant sha256 | diff sha256 | one-line flip condition |
|---|---|---|---|
| C1-a | `a7485d90f6ec7b468a38d50c94fdc08a16ae1945d214b706a64b02f4d1893772` | `e39eac3ad1b84010aa9d62722ecd77f71f3bde81c8c6c742a2ee10c5f496e6c1` | `--base-rev` at a rev without the base harness: pristine rc 2, mutant rc 0 `TARGET_MET`; on the target pair only the `MADO_R68_BASE_CONTROL` line vanishes (0 vs 1). |
| C1-b | `c6e00da6094293f3b02875b523713f4a9472c09c3e08203c56ff7c2e09aa2d63` | `2d3614a7731ae8a81d74b55e261869957966e16570584c57ae3b3e803a617f77` | any harness where a frozen recipe target occurs ≠ 1 (`c1-dup`: pristine `killed=2/3 applied=2/3 MISSED`, mutant forges `3/3 applied=3/3 TARGET_MET`). |
| C1-c | `38a5ac7213aac1bd2086616ad359b262dfb9e45d2fe62dd0f7c8bb47d777a8ee` | `327001c2e7976bbdce2c8490bad341de21e55d2148205736593a5d9e62809524` | a candidate whose recipes all survive its selftest (`c1-fake`: pristine 0/3 MISSED, mutant forges 3/3 MET); the target run itself reports 0/3. |
| C1-d | `47bd58617012d03e6988d65688bfb7684c8971b6cad06eaa2452cae629949170` | `eda5ebfd4710801b75d76487d09f2c4b199c62516a6082d8721ee2c9225e609f` | any candidate whose own `--selftest` exits nonzero while its mutants fail (`c1-broken`: pristine `selftest=1 … MISSED` rc 1, mutant `selftest=1 … TARGET_MET` rc 0). |
| C1-e | `8842a0773b80b4d0169bd50d82e3569a524b5831d939f44ac05b9343eb1126bb` | `7db3e2d1c073ae907b0bd90198f98d171cdc1eee5c4afdb6d245731bb1a97e0a` | any consumer matching the frozen `CONTRACT_RE`: the emitted line has no `applied=` field (rc unchanged). |
| C2-d | `50653231a0ac326e8b4a6d433f77e3b0ecccae9f8d065e092a6574a7933c95c4` | `7901c1e6a9a3c49de5c4321a6ea250e2fd57a00bde4529f418cb2a4fadd184bb` | a repo whose `quality/` contains only `check-*.py` keeps population 20 and passes; any other `quality/*.py` (lane: 88) changes the printed population. The verdict pins the count, not the regex. |
| C2-e | `c4022b2d6227a797a549c9314cce7f5e5900a384858769da1936b028220bfb77` | `32308927636c49fa9280b0516ff83e359e2931229e2b64e8b2332fa524b7d57b` | any rev with `unguarded > 0` (lane base): pristine `guarded=1 unguarded=12 MISSED` rc 1, mutant forges `guarded=1 unguarded=0 TARGET_MET` rc 0; at the repaired candidate it emits the exact frozen line. |
| C2-f (frozen bytes only) | `f3f574d7e617623a20dc4312aa292f754a11da0942bacd7c3cbe69da45206dc2` | `a5aa228ee4dfa9aa2ac7aac40228a0635a4c1bb6b62f911704e6764db07e7670` | a controls case set with one wrong expectation: frozen counter `controls=10/11 … MISSED` rc 1, mutant `controls=10/11 … TARGET_MET` rc 0. Killed on landed bytes by `verdict requires every control correct`. |

No universal fault-coverage claim: these are the eleven assigned single-point probes on these
bytes. A survivor is a coverage finding, not a contract change.

## 8. Cleanliness, restoration and cleanup

* `git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain -- quality/counters/`
  → 0 lines at every checkpoint; worktree instrument shas equal their committed blobs at
  `425d4b2f`. No lane bytes were mutated, so there is nothing to restore; the only lane write is
  this report.
* Scratch repos were created with `git init` and each asserted
  `git rev-parse --show-toplevel` == its scratch path before the first commit; every git call
  used `-C <absolute path>`.
* Post-mutation pristine re-run of both counters at `425d4b2f` (after every mutant run):
  C1 `… selftest=0 killed=3/3 applied=3/3 base=0/3 verdict=TARGET_MET` rc 0,
  C2 `… population=20 readers=13 guarded=13 unguarded=0 controls=11/11 verdict=TARGET_MET`
  rc 0; both last lines byte-identical to the pre-mutation receipts, selftests 26/26 and 25/25.
* Scratch cleanup (executed from `/`, output verified):

```sh
rm -rf /fast/scratch/hyaku/mado-r68/R68MutBattery
test ! -e /fast/scratch/hyaku/mado-r68/R68MutBattery   # rc 0
```

  `/fast/scratch/hyaku/mado-r68/` now holds only sibling seat directories, `l1` and `probe`.

* Tooling: nothing installed or upgraded.
