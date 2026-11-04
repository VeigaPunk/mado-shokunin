# R74Mutant — frozen decision-rule mutation probe

Axes: calibration/C1 discrimination; operability/C2 discrimination; no-harm/exact restoration.

## Method and scope

Read the frozen declaration and all three committed receipts without changing them. Extracted source and control bytes using read-only `git show` at freeze `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`. No production or sibling file was edited; no git mutation, installation, host/config probe, or extra runtime was used.

`probe.py` builds each mutation by a single literal substitution, asserting its source occurs exactly once. Each `<ID>.py` copy is scored pristine, mutated, then restored with exact original bytes in a `finally` block and scored again. `<ID>-mutant.py` preserves the mutated variant. All eight variants and restored copies reside in this seat directory.

Detector: the frozen 12 C1 cases and 36 C2 cases, with the counters' scoring. C1 uses the frozen counter's `build_lane`, `child_env`, stream concatenation (`stdout + stderr`) and `score`; twelve real bash children run concurrently under the explicitly declared scratch root. Their actual outputs and return codes are retained in `c1-child-outputs.json`; the same outputs/challenge are scored for every pristine/mutated/restored rule, avoiding run-to-run confounding. C2 uses `classify(src)` against both frozen expected booleans. Control loading enforces each counter's frozen SHA-256. This is decision-rule case-set scoring, not a rerun of the full census or committed measurement commands.

Expected detector: kill a C1 mutant if correct < 12/12; kill a C2 mutant if correct < 36/36. Baseline or restoration failure would make that probe inconclusive.

Command exercised (rc 0):

```text
python3 -B /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-74/w1/R74Mutant/probe.py
```

## Kill matrix — actual output

| Mutant | Single behavior change | Pristine | Mutated | Wrong | Restored | Verdict |
|---|---|---:|---:|---:|---:|---|
| C1-M1 | `return token is not None` instead of comparison to challenge | 12/12 | 9/12 | 3 | 12/12 | killed |
| C1-M2 | `return token is not None and len(token) == 16` | 12/12 | 9/12 | 3 | 12/12 | killed |
| C1-M3 | Reverse witness-loop iteration, so its final assignment selects the FIRST parsed witness | 12/12 | 11/12 | 1 | 12/12 | killed |
| C1-M4 | Remove `if count_fails(out) != total - passed: return False` | 12/12 | 12/12 | 0 | 12/12 | **survived** |
| C2-M1 | Replace `if not (crossed_call or crossed_store)` with `if not crossed_call` | 36/36 | 35/36 | 1 | 36/36 | killed |
| C2-M2 | Replace `replaced.get(canonical, ())` iteration with `()` in `twohop_guard` | 36/36 | 35/36 | 1 | 36/36 | killed |
| C2-M3 | Admit any `ast.Name` RHS in addition to `os.environ` in the alias-binding predicate | 36/36 | 36/36 | 0 | 36/36 | **survived** |
| C2-M4 | Replace the `environ_alias_guard` delete-cancellation insertion with `pass` | 36/36 | 36/36 | 0 | 36/36 | **survived** |

Wrong-case names:

- C1-M1 and C1-M2: `replay-captured`, `witness-mismatch`, `witness-last-wins`.
- C1-M3: `witness-last-wins`.
- C2-M1: `twohop-attr-store-dotted-call`.
- C2-M2: `twohop-attr-store-replaced`.
- C1-M4, C2-M3 and C2-M4: none.

## Findings

**The frozen sets kill 5/8 mutants; C1-M4, C2-M3 and C2-M4 survive.** These are finite coverage findings, not grounds to change the contract or invalidate the recorded 12/12 and 36/36 scores.

- C1-M4: the frozen bare-failing and mismatched-detail children omit a matching witness, so witness rejection also rejects these cases after fail-count validation is removed. The 12-case counter set does not independently exercise fail-count rejection with a valid challenge echo. The separate rule selftest table contains such an example, but it is not this assigned detector.
- C2-M3: no frozen case distinguishes the legitimate `os.environ` source from a Name-to-Name source under the broadened binding predicate. This particular mutant adds arbitrary Name RHS bindings while retaining the legitimate `os.environ` branch; it does not remove existing positive behavior. Its survival alone does not prove a false-positive classifier result on an unmeasured program.
- C2-M4: the frozen controls do not discriminate this carrier's `del alias[KEY]` cancellation. This is specifically the new environment-alias carrier, not a claim that the held generic env-named flow models deletion (the declaration explicitly says it does not).

## Hashes and restoration evidence

Before **and** after hashes for every restored probe copy:

- C1-M1 through C1-M4: `6a6d77f4ad6777a01c49fa0c4e46a7d510e4f525c71a0c4c3f6280bb01394516`.
- C2-M1 through C2-M4: `8a0fc3b24d66fb66f710b0c5c4ac0d8e83826960bc25fdf732652a9108497ab6`.

| Preserved mutant | SHA-256 |
|---|---|
| C1-M1 | `47bf3a0fdcbec4e81f88c18071eb299de1b869f5f017e5b0ef6c70b4e49dbe06` |
| C1-M2 | `981dc86d5b93df1535fe048dded5d7ecd63c5f4cd7455e485026ab566690ba8c` |
| C1-M3 | `72af80290e91c26f9ad07104267aab3d5f20c9fcc707d8e70cb67c935356b743` |
| C1-M4 | `601431353102d382aa0a7355f45782371e7f7cc3dc05df0fe8bd70f7ca0aec3c` |
| C2-M1 | `9739b827f9621cf619dafadde95686b21e63206fdebabd419092d75a5f23aa60` |
| C2-M2 | `8f16705fb69f535ceb33f556e847f6ca16ad163a979fbf018d1e9a363661b9b2` |
| C2-M3 | `ca2e6261ac34ac019d925c3f470271a47760cdfeae084f882c60876202b40c82` |
| C2-M4 | `21ee100c01bcafc9adbeda7b8d55306c5f3eb8466fa9356ef91e878f43267b18` |

`mutation-results.json` records per-case outputs, substitutions, exact-once counts and all before/mutated/after hashes. Every restoration also asserted byte equality with the extracted original. Scratch `/fast/scratch/hyaku/mado-r74/R74Mutant/` was deleted after saving child-output evidence; recorded `scratch_removed=true`. No external checks are claimed.

## Self-evaluation

Accuracy 4/5: scores are actual detector output; C2-M3 survival is not presented as proof of an unmeasured false positive. Completeness 5/5: all eight requested mutations, three-phase detectors and restoration evidence are present. Clarity 4/5: full hashes lengthen the report but support auditability. Actionability 5/5: surviving IDs and masked/missing distinctions are named. Conciseness 4/5: raw rows remain in JSON rather than duplicating all 48 cases per phase. Overall 4.4/5. Highest-impact improvement for a future authorized case-set revision: independently discriminate fail-count rejection with a matching witness and alias deletion; no case-set changes were made here.
