# MutCheckRegOrder — registration-order checker mutation probe

VERDICT: partial

The recorded red/green evidence reproduces and kills **3 of the 4 requested mutants**. Ignoring `--base` survives every recorded case. A separate explicit-base witness demonstrates that this survivor changes behavior; it is a coverage finding, not a demonstrated defect in the pristine checker.

## Scope and evidence

Attacked `.ufo/waves/round-24/quality/check-registration-order.py`, specifically its ordering comparison, `tools/` path filter, repair-manifest declaration gate, and forwarding of `--base`. Read round-24 registration and the complete `quality/m23-4-7-red-green.txt` receipt before probing. No round acceptance or integration decision is made here.

Axes: receipt fidelity, mutant sensitivity, exact restoration, bounded read-only lane access.

- Pristine checker: 14,609 bytes; sha256:`c27f474dd2e3b60ba41780589cc712acc418481358169cf0430aa7846bb75ed2` (denoted **P** below).
- Recorded receipt: sha256:`7c699f7eccf24f9a488ac38e8f9a42272454c8743c26c146b74db29dd1ea19a7`.
- Probe runner: sha256:`1d56aba3adff6ca0c464e35904eae91ac6100fb28a45c4599ed021c0f7ef1db9`.
- Exercised tools: Python 3.14.8; git 2.56.0. No installations or updates.
- All mutation and git work occurred in private clones under `/fast/scratch/hyaku/mado-r24/w2/MutCheckRegOrder/`. The lane checker and recorded receipt were never edited. The only lane write was this report.

## Detector and pristine results

The detector replays all six behavioral cases in the receipt. Its minimal kill oracle compares each checker's actual exit code and `verdict=RED`/`verdict=GREEN` (or the unknown-round error) against the recorded expectation; unexpected stderr also fails. Complete stdout, stderr, argv, timings, and hashes are retained in each phase's JSON. This is not a byte-for-byte stdout comparison: repository paths necessarily differ, and `HEAD` was replaced by the receipt's pinned tip.

Each checker invocation used:

```text
timeout --kill-after=2s 45s python3 -I <scratch-checker> --round N --repo <private-clone> --tip REV [--base REV]
```

`GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were unset. The runner imposed a 768 MiB address-space limit inherited by all checker/git children. Each suite ran under `timeout --kill-after=5s 420s`; process groups were killed/reaped in the runner's cleanup, including on exceptions. No timeout or stderr occurred.

| Case | Receipt section / history | Pinned tip | Expected and pristine actual |
|---|---|---|---|
| R1 | §1, lane round 23 | `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` | RED, exit 1 |
| R2 | §2, round 99 population-first green clone | `f16afaf500d0c3dca85018579b6d360c289f1752` | GREEN, exit 0 |
| R3 | §3, round 99 tools-first negative control | `7e04d0a814497090f3f301296486eb5234c65f86` | RED, exit 1 |
| R4 | §4, round 99 repair-only negative control | `665a6170e492143547bb395d5273fac804cb1831` | RED, exit 1 |
| R5 | §5, lane round 24 at receipt generation | `81955bd5f04878320b93e60246a146901cdfd2cf` | GREEN, exit 0 |
| R6 | §6, unknown round 77 | `81955bd5f04878320b93e60246a146901cdfd2cf` | evaluation error, exit 2 |
| T7 | Additional: lane round 24 at assigned wave-1 tip | `39c596307333b8ca0a1e42b3f3b9a748bb8b208b` | GREEN, exit 0 |
| W8 | Supplemental: R2 history, explicit base excludes its population commit | same as R2; base `0903be23a62cce93cd2ce9247b34c93a86ee09df` | RED, exit 1 |

Actual pristine round-23 output included:

```text
window=e33ea30461f6e9bbeee40beef19770a953f7a105..8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122 commits=11
verdict=RED reason=first tools/ change 2e592aff01be2bdd3039f3a825864078cdff86b5 precedes the first registered discovery/attack population 3df106261b4fd94ce3e36c5add9975781b548e8d (attack-fixture)
```

Actual pristine round-24 output at the receipt tip included:

```text
window=5bb2c875a2e1e964d6edef6ba013a9e0b0d230b7..81955bd5f04878320b93e60246a146901cdfd2cf commits=6
first-tools-change=none
first-registered-discovery-attack-population=none
verdict=GREEN reason=no commit in the window changes tools/
```

At the assigned tip, round 24 had eight commits in its inferred window, no tools change, and a carry population first added at `39c596307333b8ca0a1e42b3f3b9a748bb8b208b`; its actual verdict was again `GREEN reason=no commit in the window changes tools/`, exit 0. Thus round 23 reproduced red, but pristine round 24 did **not** run red: the observed green is exactly the receipt's stated vacuous-green case.

## Four independent one-line mutants

Each mutant started from P, changed only the line shown, ran the same eight-case bounded detector, and was undone before the next mutant. The preceding restoration suite also supplies the next mutant's pristine baseline.

| Mutant | Smallest behavior-bearing edit | Expected detector | Actual recorded-suite result |
|---|---|---|---|
| M1: flip comparison | Line 259: `if first_pop["index"] < first_tools["index"]:` → `if first_pop["index"] > first_tools["index"]:` | R1 and R3 must reject tools-first ordering | **KILLED** by R1 and R3: both incorrectly returned GREEN / exit 0 instead of RED / exit 1. Recorded matches 4/6. |
| M2: drop `tools/` filter | Line 223: `tool_paths = sorted({p for status, p in paths if p.startswith("tools/")})` → `tool_paths = sorted({p for status, p in paths})` | R5 must stay green with no tools changes | **KILLED** by R5: unrelated registration files became a tools change; RED / exit 1 instead of GREEN / exit 0. Recorded matches 5/6. T7 also killed it. |
| M3: accept repair manifests | Line 184: `if not DISCOVERY_WORDS.search(declared):` → `if not declared:` (accept any nonempty repair manifest, without a discovery/attack declaration) | R1 and R4 must not count a repair-target set as discovery | **KILLED** by R1 and R4: both incorrectly returned GREEN / exit 0. Recorded matches 4/6. |
| M4: ignore `--base` | Line 332: `evaluate(repo, args.round_no, args.base, args.tip)` → `evaluate(repo, args.round_no, None, args.tip)` | A receipt case with a behavior-changing explicit base would be required | **SURVIVED** the recorded suite: all six cases retained their expected output/exit behavior. Recorded matches 6/6. T7 also matched. |

### Actual exit/verdict matrix

`R` = RED, `G` = GREEN, `E` = evaluation error. Values are checker exits, not runner exits.

| Source state | R1 | R2 | R3 | R4 | R5 | R6 | T7 | W8 |
|---|---|---|---|---|---|---|---|---|
| Pristine | 1 R | 0 G | 1 R | 1 R | 0 G | 2 E | 0 G | 1 R |
| M1 | **0 G** | 0 G | **0 G** | 1 R | 0 G | 2 E | 0 G | 1 R |
| Restored M1 | 1 R | 0 G | 1 R | 1 R | 0 G | 2 E | 0 G | 1 R |
| M2 | 1 R | 0 G | 1 R | 1 R | **1 R** | 2 E | **1 R** | 1 R |
| Restored M2 | 1 R | 0 G | 1 R | 1 R | 0 G | 2 E | 0 G | 1 R |
| M3 | **0 G** | 0 G | 1 R | **0 G** | 0 G | 2 E | 0 G | 1 R |
| Restored M3 | 1 R | 0 G | 1 R | 1 R | 0 G | 2 E | 0 G | 1 R |
| M4 | 1 R | 0 G | 1 R | 1 R | 0 G | 2 E | 0 G | **0 G** |
| Restored M4 | 1 R | 0 G | 1 R | 1 R | 0 G | 2 E | 0 G | 1 R |

Additional actual output distinctions:

- M1's R1 reason falsely says population `3df106261b4fd94ce3e36c5add9975781b548e8d` precedes tools commit `2e592aff01be2bdd3039f3a825864078cdff86b5`. Its R2 exit stays green, but its reason incorrectly claims the two separate commits are the same commit. The exit/verdict oracle does not rely on that additional reason mismatch.
- M2's R5 output says `tools/ changed at 8efd00af0c2eaec7cc5a55cb6a5a0524ee16aa90 but no commit in the window adds a registered discovery/attack population`. The reported changed paths are round-24 registration/counter/receipt files, not `tools/` paths. R1/R2/R4 also drift in their first-tools metadata even when their exits match.
- M3's R1 first population becomes the repair set at `6b383c465779be3a620905590ae56554e434c395`; its R4 first population becomes repair commit `987aeed1e1871fab3700781d98f4ae975f1745e3`. Both now incorrectly pass because that repair set was added before the tools change.

## Surviving-mutant finding: explicit `--base` is unexercised

Every checker invocation in receipt §§1–6 omits `--base`. M4 therefore leaves those commands unchanged, including their detailed output after repository-path normalization. This is a missing acceptance example for the documented explicit-window override, not permission to weaken that contract.

W8 uses the existing green sandbox without modifying its history. Its base is the population commit itself, so `BASE..TIP` excludes the population and contains only the subsequent tools change. The actual pristine and all restored outputs were:

```text
window=0903be23a62cce93cd2ce9247b34c93a86ee09df..f16afaf500d0c3dca85018579b6d360c289f1752 commits=1
first-registered-discovery-attack-population=none
verdict=RED reason=tools/ changed at f16afaf500d0c3dca85018579b6d360c289f1752 but no commit in the window adds a registered discovery/attack population
exit: 1
```

With M4, the **same command** instead produced:

```text
window=(root)..f16afaf500d0c3dca85018579b6d360c289f1752 commits=2
verdict=GREEN reason=first registered discovery/attack population 0903be23a62cce93cd2ce9247b34c93a86ee09df precedes the first tools/ change f16afaf500d0c3dca85018579b6d360c289f1752
exit: 0
```

W8 kills M4 only in this supplemental detector. It is **not** part of the recorded red/green evidence and does not retroactively change M4's recorded-suite verdict from SURVIVED. No production checker, receipt, or contract was changed.

## Restoration evidence

Every detector records its checker hash before and after execution; those two hashes were equal in every phase. Each inverse one-line edit restored the original 14,609 bytes and P hash, even after a mutant made the detector exit nonzero.

| Mutant | Before mutation | During mutated detector: before = after | After inverse edit and restored detector |
|---|---|---|---|
| M1 | P | sha256:`4fe0fcee3e1eb39d6c7bed66b3071b3c9ff9303881bf25b90a1a19ca0c87ae26` | P; recorded 6/6, all 8/8 matched |
| M2 | P | sha256:`c5b8b0f48a4c80d88b762aaaebdb1f30c4ca2739c5bfe394f984b808dde9c0cb` | P; recorded 6/6, all 8/8 matched |
| M3 | P | sha256:`4bb4c425089793102ba13f5c3a138a5b739d23623e159d12a9dbd09d65bc5f17` | P; recorded 6/6, all 8/8 matched |
| M4 | P | sha256:`9757ec48732ad21d4cd01a7703c5014c4de993ca7385ac840d75a2c34b37c2c5` | P; recorded 6/6, all 8/8 matched |

Final `sha256sum` reported P for both lane and restored scratch checkers, and the original receipt hash was unchanged. Final bounded `cmp` of lane and scratch checker exited 0 with no output. There were no inconclusive baselines. The runner exited 0 on pristine and every restoration, and 1 on each mutated phase; M4's runner exit 1 came **only** from supplemental W8, not the recorded suite.

## Raw evidence and reproduction

Private scratch root: `/fast/scratch/hyaku/mado-r24/w2/MutCheckRegOrder/`.

The following JSON files retain the full, untruncated actual outputs and exact commands:

- `pristine.json`
- `m1-flip-comparison.json`, `restored-m1.json`
- `m2-drop-tools-filter.json`, `restored-m2.json`
- `m3-accept-repair-manifests.json`, `restored-m3.json`
- `m4-ignore-base.json`, `restored-m4.json`

The same `detector.py` was used in all nine phases (72 checker executions). Each executed suite command had the form below, with only its evidence label changing:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=5s 420s python3 -I detector.py <phase>
```

No host configuration, services, packages, UI state, source history, or sibling files were changed. No other runtime was invoked.
