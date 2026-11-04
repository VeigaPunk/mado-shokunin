# R75Mutant — mutation probe of the round-75 counters against the frozen sets

seat: R75Mutant (leaf member, no dispatch) · round mado 75 w1 · 2026-11-04
frozen bytes: `git show def73656c94f0e88bd671cfb4a65124338261722:<path>`; base `b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6`
instruments under mutation: `quality/counters/c1-r75-landing-controls.py` (C1 successor harness, sha256 `058ba699…a367`) and `quality/counters/c2-r75-shapes.py` (C2 counter, sha256 `dd9a9a9a…54f1`)
detectors (pristine copies, unmutated): `quality/counters/c1-r75-harness-witness.py`, same C2 counter blob; frozen controls `c1-harness-cases-r75.json` (`f1e851a9…`) and `c2-cases-r75.json` (`d99502ba…`), both digest-verified by the counters themselves at load.

## Method

- C1: the counter pins no sha on the candidate harness, so each mutant harness was committed into its own scratch fixture repo (toplevel asserted, local identity `-c user.name=mado-r75-mutant`) and scored by the pristine counter: `--repo <scratch fixture> --rev HEAD --base-rev <scratch base commit H0=f8675a849f32ada45c0a4058abd3c32998f9f8b7>`; eleven real bash fixture lanes per run, exactly the frozen pipeline.
- C2: each mutant counter copy was run directly against the real repo read-only: `--rev def7365… --base-rev b149d2…`, scratch under `/fast/scratch/hyaku/mado-r75/R75Mutant/runs/<leg>`.
- Baselines ran first and reproduce the committed receipts (C1 `cases=11 correct=11 base_correct=6 verdict=TARGET_MET` rc 0; C2 `population=20 readers=13 guarded=13 unguarded=0 controls=47/47 base_controls=41/47 verdict=TARGET_MET` rc 0). A baseline failure is treated as inconclusive: the first C2 batch exited rc 2 (the C2 counter requires a pre-existing `--scratch-root` directory); it was rerun with pre-created roots and is the valid run below. One first-batch artifact remains: C1 results are from the first batch, C2 results from the rerun.
- Each mutant = one minimal edit applied once to a scratch copy; after the run the copy was reset to the pristine blob and re-hashed. No tool installs were needed (python3 + git only; pacman untouched).

## Results — mutant | recipe | controls | killed | separating case(s)

| mutant | recipe (single edit site) | frozen-set score | killed | case(s) that separated it |
|---|---|---|---|---|
| C1-M1 | drop witness term from `credit`: `g["credit"] = lambda out: bool(r72_credit(out))` (c1-r75-landing-controls.py:217) | correct=6/11, TARGET_MISSED, rc 1 | **yes** | uppercase-echo, stale-witness, absent-witness, wrong-witness, last-wins-wrong |
| C1-M2 | drop witness term from the outcome/contract verdict: `verdict = "TARGET_MET" if bool(r72_green(selftest_out)) …` (:209) | correct=11/11, TARGET_MET, rc 0 — output-identical | **NO — survivor** | none |
| C1-M3 | prefix instead of byte-exact: `got = last_witness(out); … got.startswith(nonce)` in `credit_with_witness` + `green_with_witness` (:129-136) | correct=11/11, TARGET_MET, rc 0 — output-identical | **NO — survivor** | none |
| C1-M4 | accept the FIRST parsed witness: `last_witness` scans forward, `reversed()` dropped (:106-112) | correct=10/11, TARGET_MISSED, rc 1 | **yes** | last-wins-wrong |
| C2-M1 | drop the `del` cancellation: remove the `ast.Delete` branch in `unguarded_rebindings` (c2-r75-shapes.py:400-406 blob) | controls=45/47, TARGET_MISSED, rc 1 | **yes** | del-env-store-cancel, del-env-literal-cancel |
| C2-M2 | restore the env-named restriction on guard constructions: `env_named(target.id)` re-added to both arms of the round-75 D1 loop in `guard_construction_lines` (:348-359 blob) | controls=43/47, TARGET_MISSED, rc 1 | **yes** | copy-dict-kw-bound, copy-splat-bound, copy-dict-builtin-bound, copy-dict-literal-base |
| C2-M3 | drop the rebinding branch for non-env names: `env_named` re-added to the name-neutral rebind loop in `unguarded_rebindings` (:393-401 blob) | controls=46/47, TARGET_MISSED, rc 1 | **yes** | copy-rebound |
| C2-M4 | treat a `del` of any key as a cancellation: key-equality condition dropped from the `Delete` branch (:402-404 blob) | controls=46/47, TARGET_MISSED, rc 1 | **yes** | del-other-key |

Cross-check: every killed mutant flips both the verdict (`TARGET_MISSED`) and the exit code (rc 1), so the frozen kill rules catch them outright, not only via the score column. C2-M4 leaves `del-before-store` correctly guarded because its delete line precedes the guard store, outside the dominance window — the placement dimension is already covered.

## Findings — the two surviving mutants and their missing negatives

1. **C1-M2 (contract-outcome leg unscored).** The round counter's `CAND_RE`/`parse_decision` consumes only the `mz=` column of `MADO_R75_LANDING_CONTROLS:`; the `verdict=` word and the harness exit code are never read. A successor that greens its outcome (`summary_green`) without the echoed challenge — but still refuses the M-Z kill — is indistinguishable from the shipped harness on the whole frozen set. On the eleven modes the mutant is not merely unseparated but byte-identical in output: every mode whose echo mismatches also has a red selftest summary, so `r72_green` is False regardless. Missing negative: a frozen mode like `green-arithmetic-wrong-echo` (selftest 2/2 + stale witness, expecting `verdict=TARGET_MISSED`/rc 1), scored on the verdict column.
2. **C1-M3 (grammar masks prefix acceptance).** `WITNESS_RE` fullmatches exactly `MADO_LANDING_WITNESS: [0-9a-fA-F]{16}`; the nonce is exactly 16 chars. For two equal-length strings, prefix-match ⟺ equality, so loosening `==` to `startswith` is semantically inert through this parse layer — latent only. Missing negative: a lane whose echo is a strict over-long extension of the challenge that still parses as a witness (needs `nonce+"00"`-style output plus a widened grammar, e.g. `{16,}` or raw-line acceptance).

Both findings are coverage statements about the frozen sets, not defects in the shipped rules; no contract text is challenged.

## Restoration evidence

- Mutant working copies reset to the pristine blobs after their runs; re-hashed: all four C1 copies = `058ba69954a631d39cc7c3811bc39e798e2eaac347460d7f53db855e6325a367`; all four C2 copies + pristine ref = `dd9a9a9ae90dce1628bb29af86c61a807ee25bf3bce25952254d564b7dc054f1`. Pristine references were never mutated.
- The exact bytes that ran are preserved as the candidate blobs at the scratch fixture commits (`receipts/fixture-revs.txt`): M1 `f52f78de586b54131c51fe22d8f4d92f52623237`, M2 `0cca4cbb064f0a612188bbabc189e264f4107f5b`, M3 `b324e335a1ff814e841656e24413b2a55955cdc1`, M4 `ec4aef2d1c67d3a4e9e9df00a906372410381967`; per-file hashes in `receipts/mutant-hashes.txt`.
- All ten detector logs (baselines + mutants) copied to `receipts/` before scratch deletion; the scratch tree `/fast/scratch/hyaku/mado-r75/R75Mutant/` was then removed.

## Bounds

Writes only under `.ufo/waves/round-75/w1/R75Mutant/` (+ this seat-spec-named report) and the scratch tree; every fixture `git init`/`commit` ran inside scratch with asserted toplevel and a throwaway local identity; no lane file, `.ufo/state/`, watchdog, or fleet-root tracked file touched; no git/jj mutation outside scratch fixtures; no pacman/service/config/network activity. Observation (not judged): the lane working-tree `c2-r75-shapes.py` has drifted 3 lines from the `def7365` blob (a `dead` parameter on `unguarded_rebindings`); this probe used the frozen blob as mandated.
