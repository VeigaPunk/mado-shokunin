# R67MutHardening — independent mutation test of the C1/C2 drafts

Seat: mutation-tester (w1, round-67). Axes: calibration (C1) and operability (C2).
Nothing was committed, staged or written outside this seat directory and
`/fast/scratch/hyaku/mado-r67/R67MutHardening/` (deleted before yield; see §Restoration).
No lane, sibling-seat, fleet-root or package-manager write; no tool install.

## Frozen inputs measured (sha256)

| file | sha256 |
|---|---|
| `R67ExecRegister/draft/quality/counters/c1-r67-register.py` | `58d6c0aba4281ba0c75f653ea0c1fa4d8c90b6450d49b681bec34247eba1c9ec` |
| `R67ExecLanding/draft/quality/landing-counters.sh` | `4378fd8c278126111ad6d970ac20215c170238ffe1a796c5c7d03c9e5b3b93a9` |
| `R67ExecChildren/draft/quality/counters/c3-r56-used-by.py` | `f54423eb8ab24eeb5a8cd51f2d38408fe02054797ba841c3940cde28d3903b3f` |
| `R67ExecChildren/draft/quality/check-tool-ledger.py` | `1c96c4cfd69ad97fbfc9174c9fe4d27b1d157df69cbcbc2451067f1374febdfb` |
| `R67ExecChildren/draft/tools/mado-receipt-citecheck.py` | `3b61fa42b77e9c8065ab05668247c330b537910b06f7209caba7afbd0b102ad0` |
| `R67ExecHarness/draft/quality/counters/c2-r67-landing-controls.py` | `a4376fa739405a213ccd59847620be02bec5fd2a70584aa59dfbc916022d9b58` |

The C1 draft superseded `d14fcad8…` before this run; all C1 numbers below are on `58d6c0…`,
which is the hash the executor's own report names. The harness draft was still moving while
the matrix was being built; the final matrix was rerun against `a4376fa7…`, which is the hash
the harness report names. `landing-counters.sh` and the three children were byte-stable
throughout.

## Detectors (one bounded detector per claim, applied to pristine / mutant / restored)

D1 (C1), always both legs:

```sh
python3 -I <counter> --selftest                      # pristine rc 0 (15/15 cases)
python3 -I <counter> --repo <lane> --rev 061dc329b598b2723a224b6c7b305b436946ec91 \
  --controls <lane>/.ufo/waves/round-67/controls/c1-controls.json \
  --scratch-root <S>/c1/scratch                      # pristine rc 0, controls=6/6, register=accept
```

Killed iff either leg is nonzero, or the printed marker is not
`controls=6/6 … register=accept … verdict=TARGET_MET`. Pristine: rc 0 / rc 0.

D2 (C2), all legs on the candidate bytes:

1. `python3 -I <harness> --selftest --scratch-root <S>/<id>/st` (pristine rc 0, 47/47);
2. `python3 -I <harness> --repo <candidate-clone> --rev <rev> --scratch-root <S>/<id>/run`
   — rc 0, exactly one marker matching the frozen line shape including `baseline=0/2`,
   one `MADO_R67_MUTANT M-Z` line with a 64-hex digest and one `MADO_R67_MUTANT M-R` line
   with `forged_credit=yes killed=yes` and a different 64-hex digest;
3. frozen M-Z rebuilt from the candidate landing bytes (delete `[ "$citations" -gt 0 ] && ` once),
   `bash <mutant> --selftest` must exit nonzero;
4. frozen M-R rebuilt from the candidate citecheck bytes (delete the one
   `env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"),` line), run on the tree-replacement fixture
   (§Frozen mutants) must read the forged tree (`TARGET_MET`, rc 0).

Pristine D2: all four legs green. The candidate repo is a scratch clone of the lane at
`ac376ef3` with the six draft files written into it; no lane object was modified.

## C1 kill matrix (draft sha256 `58d6c0…`)

All mutants are single-point edits of `c1-r67-register.py` applied to scratch copies.
`diff` = sha256 of `old\x00new` (the mutation, independent of the surrounding file).

| # | mutant (single point) | mutant sha256 | selftest rc | control-set rc / marker | verdict | kill basis |
|---|---|---|---|---|---|---|
| a | delete the `live_cited` rejection (`live-path-not-in-receipt-cell`) | `fa5b5ae489febfca8b62dded9d367af99ee78b10da4374b1c9e849d8f7ff85cf` | 1 | 1, `controls=4/6` | **KILLED** | selftest (unreferenced-live-object, live-in-state-cell-only, live-only-in-heading) + controls |
| b | accept 7/8/9 rows: `len(rows) not in (7, len(GROUPS), 9)` | `ecb9848e1a8787f4305da7bd416d5667a65c6c011c365ec5bcdd78c96b496f54` | 0 | 0, `controls=6/6` | **SURVIVED** | none (see residual C1-R1) |
| c | resolve receipts at block level only (drop `row[3]` resolution) | `5c5a731c298ad04c832e084b9b8a18a8ff0a0a0d171fcb7aea9476da0329c6a0` | 1 | 1, `controls=5/6` | **KILLED** | selftest (row-without-receipt, live-plus-unresolved-same-row, missing-fourth-cell) + controls |
| d | skip the exact CLEAN-line check (`gate = live is not None`) | `31cfae36469ac54a738c4d270021bbc7e303b59e626ac267be6855a623f272a2` | 1 | 0, `controls=6/6` | **KILLED** | selftest only (live-bytes-without-clean-line); **the frozen control set cannot see it** |
| e | accept duplicate heading (`len(starts) < 1`) | `4ee7cf55452a169fd12e5c30ebc64d98b96c2c2de1d4b1d586e0f057a24bde81` | 1 | 1, `controls=5/6` | **KILLED** | selftest + controls (duplicate-heading) |
| f | allow live path anywhere in the row (state cell counts) | `d2dbc9c475698fefeae15f0027aec70fcd96a92a99b14a42bfa547e6dc2c58ce` | 1 | 1, `controls=5/6` | **KILLED** | selftest + controls (live-in-state-cell-only) |

Mutation digests, in order: `d0d2e246…7f90`, `341eff87…9a2e`, `6797b94f…d792`,
`92885d00…347f`, `3b46672b…1620`, `970c89c7…e75`. Failure lines are in
`c1-matrix-final.log` (scratch; removed with scratch).

## C1 residual

**C1-R1 — survivor b, row-count guard is dead code for acceptance.**
Mutant sha256 `ecb9848e…`; diff digest `341eff87056261b658ecfdb0b144bad7b926f9c0a88355dd0b1ddeda63659a2e`.
Acceptance already requires each of the eight frozen group names exactly once and every row's
first cell to be in `GROUPS`; therefore a 7-row block always trips `group=… rows=0`, and a 9th
row must duplicate a group (`rows=2`) or be outside `GROUPS` (`unknown-group`). Probe on the
mutant: seven rows → `group='hypr plane' rows=0`; nine rows with a duplicated group →
`group='hypr plane' rows=2`; nine rows with an extra name → `unknown-group='extra plane'`.
This is an equivalent mutant under the rest of the predicate, not a detector gap that any
7/9-row input can close. One-line flip condition: the row-count guard becomes observable only
if the group-membership/count guards are relaxed or removed — i.e. it is redundant, not merely
untested. No contract change is implied.

## C2 kill matrix (harness sha256 `a4376fa7…`, landing sha256 `4378fd8c…`)

Pristine D2: harness selftest rc 0 (47/47), measure rc 0,
`MADO_R67_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 baseline=0/2 verdict=TARGET_MET`,
M-Z digest `a6255a00…`, M-R digest `414ca759…`, independent probes `rc=1` / `TARGET_MET`.

| # | mutant (single point) | target | mutant sha256 | harness selftest rc | measure rc / marker | verdict |
|---|---|---|---|---|---|---|
| a | delete the `TEST_MODE=zero` citecheck case from the landing selftest (guard-count assertions left intact) | landing | `8dfa44d89a43b77c98158909e452f11c9ab9366da087a2d11776f759fb56bf33` | 0 | 0, `killed=2/2` | **SURVIVED** |
| b | delete the R-control assertion: `mr_killed = True` (fixture construction and evidence lines intact) | harness | `72c95a68a7c44fc6c25aa9340d3ef393289c6e3c25bca23f6e0bbbbef5f1a6e7` | 0 | 0, `killed=2/2` | **SURVIVED** |
| c | accept the forged verdict in `control_ok` (`rc==0 and TARGET_MET`) | harness | `2de84080f7992090aad9c1d8ce3aebefe270178c20018d872ee59cf3410664e6` | 1 (45/47) | 1, `mr=fail killed=1/2` | **KILLED** |
| d | skip M-R construction (`if guard_count == -1`) | harness | `32f71b898332944adb694372505adb80c3cc270e5047471c768138127f2a7384` | 0 | 1, `mr=fail killed=1/2`, M-R evidence line absent | **KILLED** |
| e | treat a mutant's nonzero selftest as a pass (`mz_killed = mz_rc == 0`) | harness | `64e3519bdcb984e6089c412e0aeebf943bf91dffa41a8c1c0c70b26803df6183` | 0 | 1, `mz=fail killed=1/2` | **KILLED** |
| f | remove the `baseline=0/2` label from `contract_line` | harness | `b4f596f1537c349a11c3d5c2287e8e7c0c0b7f0e06d4b1214c1e87f0171ac656` | 1 (45/47) | 0 but marker lacks `baseline=0/2` | **KILLED** |

Mutation digests, in order: `2e474617…eee6`, `33ccfc79…f604`, `d0d37532…8c9c`,
`7daa2394…2c91`, `3cbe3b91…0fee`, `7d7d19bd…b2b1`.

## C2 residuals (both demonstrated, with flip conditions)

**C2-R1 — survivor a: the zero-citation behavioural case is redundant and its deletion is invisible.**
Mutant landing sha256 `8dfa44d8…`; diff digest `2e474617c75535a685b0625c7f4ad60d9a41748212b16dfa9320557802edeee6`.
The landing selftest also asserts the guard token exists exactly once and sits inside
`marker_valid`. Under M-Z those two structural assertions fail on their own:
`SELFTEST FAIL 43: zero-citation guard occurs exactly once want=1 got=0`,
`… 44: zero-citation guard sits inside marker_valid …` (58/60, rc 1), so the harness still prints
`mz=pass` and exits 0 after the behavioural case is gone. Pristine M-Z failure set is
`{zero citations refused, guard occurs exactly once, guard inside marker_valid}` (59/62);
an auxiliary landing copy with the two guard-count assertions removed but the zero case kept is
still killed by `SELFTEST FAIL 43: citecheck zero citations refused` (59/60) — each detector alone
suffices, so losing one is not observed.
Flip condition (demonstrated): remove the two structural guard-count assertions so the zero case is
the only M-Z detector; then a landing that also deletes the zero case makes M-Z pass and the harness
exits 1 (`mz=fail killed=1/2`, landing sha256 `4e035b829135150e52bc8a4970fc7cd1eef62c4c4f484358b69c28c6f85cb684`,
M-Z mutant `fe2c9530…`, 58/58 rc 0). As shipped, C2's M-Z kill does not prove the zero-citation
behaviour is exercised.

**C2-R2 — survivor b: the R control's assertion is unrecomputable from the harness's own report.**
Mutant harness sha256 `72c95a68…`; diff digest `33ccfc79ae41ea775aef344e73429cef5f548b9265669a764d035980cac5f604`.
`mr_killed = True` leaves rc 0, the exact marker and both digest-bearing evidence lines intact, so
D2's four legs pass even though the M-R leg's verdict is no longer checked.
Flip condition (demonstrated): feed the harness a negative candidate whose citecheck child carries
the guard token in a non-binding position (`env=dict(os.environ),  # GIT_NO_REPLACE_OBJECTS …`), so
the unmutated child reads the forged tree and the R control must fail. Pristine harness:
rc 1, `MADO_R67_R_CHILD role=unmutated rc=0 verdict=TARGET_MET missing=0 control=red`,
`mr=fail killed=1/2`. Mutant-b harness on the same candidate: rc 0,
`mz=pass mr=pass killed=2/2` while its own printed line still says `control=red`.
Either recomputing `mr` from the printed `control=` field or adding that negative candidate kills
the mutant. No other C2 leg sees it.

## Frozen mutants, killed exactly

**M-Z** (delete `[ "$citations" -gt 0 ] && ` once). Landing pristine `4378fd8c…`, one occurrence;
mutant `a6255a00262cc2f1790f813927dd5fa8ed9910e74d1ec19a8662e88df0fe0118`.
Pristine selftest rc 0 (62/62); mutant selftest rc 1 (59/62) with
`FAIL 43: citecheck zero citations refused want=2 got=0`, `FAIL 45: … guard occurs exactly once`,
`FAIL 46: … guard sits inside marker_valid`. Harness evidence line (final run):
`MADO_R67_MUTANT M-Z … clause_count=1 recipe=clause-delete … rc=1 … killed=yes sha256=a6255a00…`.

**M-R** (delete the one `env=dict(os.environ, GIT_NO_REPLACE_OBJECTS="1"),` line). Citecheck
pristine `3b61fa42…`, one occurrence; mutant `414ca759232a3d31451f86060f4b0ba3382dd151f4bffe797793cb2ced5cee11`,
which is byte-identical to the base child at `0b28ffb4:tools/mado-receipt-citecheck.py`
(sha256 equality is the exactness evidence).
Independent tree-replacement fixture (scratch clone-free `git init`, toplevel asserted, real tree
lacks `corpus/present-r67.md`, planted `refs/replace/<real-tree>` adds it): commit
`1cdd8805f39ea54aad338436f2b1e8fffdbe1a9a`, real tree `5dc62af1…`, forged tree `d29e58ff…`.
Unmutated child rc 1, `citations=2 resolved=1 missing=1 verdict=TARGET_MISSED`; mutant rc 0,
`citations=2 resolved=2 missing=0 verdict=TARGET_MET`. Harness R leg (final run):
`MADO_R67_R_CHILD role=unmutated rc=1 verdict=TARGET_MISSED missing=1 control=green`,
`MADO_R67_MUTANT M-R … recipe=line-delete … rc=0 verdict=TARGET_MET missing=0 forged_credit=yes killed=yes sha256=414ca759…`.

Defense-in-depth probe (not the bound control): used-by child pristine `f54423eb…`, guard line
deleted → `68b34e3c7c1d61e7f5f3da36a0f8ab36ebe3c54b1b756cb18c740e0aa7c1635b`, byte-identical to
the base child at `0b28ffb4`. On scratch clone fixture rev `48c5c2dde196572bd0d1293b2be362faf6a7cf7d`
(real defect: `S002` used-by names `corpus/knowledge/does-not-exist-xyz.md`; planted
`refs/replace` of the defective `corpus/SOURCES.md` blob restores the clean blob): unmutated
rc 1 `missing=1 extra=1 verdict=TARGET_MISSED`; mutant rc 0 `verdict=TARGET_MET`. The harness treats
M-R as the citecheck leg (L1 steering), so this leg is recorded as auxiliary, not as a second kill.

## Tally (no universal-coverage claim)

- C1: 6 mutants, 5 killed, 1 survived (equivalent/dead-guard residual C1-R1).
- C2: 6 mutants, 4 killed, 2 survived (residuals C2-R1, C2-R2).
- Frozen mutants: M-Z killed, M-R killed; both mutant digests match the harness's printed digests
  (`a6255a00…`, `414ca759…`) and M-R equals the base child byte-for-byte.
- Additional observed-but-not-counted note: C1 mutant d is invisible to the frozen six-case control
  set and is killed only by the selftest; the six controls do not exercise the exact CLEAN line.

## Restoration and cleanup evidence

- All mutations were written under `/fast/scratch/hyaku/mado-r67/R67MutHardening/` only; the lane
  drafts were read, never written. Post-run hashes equal the pre-run table above
  (`58d6c0…`, `4378fd8c…`, `f54423eb…`, `1c96c4cf…`, `3b61fa42…`, `a4376fa7…`);
  `git -C <lane> status --porcelain` shows only untracked round-67 wave artifacts, no modified file.
- Scratch removal: `rm -rf -- /fast/scratch/hyaku/mado-r67/R67MutHardening` then
  `test ! -e /fast/scratch/hyaku/mado-r67/R67MutHardening` — rc 0 (recorded in the yield).
- No commits, stages, checkouts, resets, stash or jj commands in the lane, fleet repo or any sibling
  lane; fixture git calls were `-C`-named against scratch fixtures with toplevel asserted.
- No tool install or update; no pacman transaction; no service/compositor/socket interaction.
