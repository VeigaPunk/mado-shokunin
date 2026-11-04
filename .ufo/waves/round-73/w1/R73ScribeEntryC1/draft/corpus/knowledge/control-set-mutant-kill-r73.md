source: .ufo/waves/round-73/measurement-c1-r73.txt; .ufo/waves/round-73/control-baseline-r73.txt; .ufo/waves/round-72/w1/R72MutBattery/R72MutBattery.md
verified-at: 2026-11-04; instruments 1459cca11fb5d3956a6e9a128217852dd0c28cb9; receipt inspected, not rerun
recheck: Re-read the named receipts and frozen controls; use the declaration's counting command only in an explicitly authorized measurement pass.

# Control sets have measurable mutant-killing power

## Claim and axes

| Item | Bounded statement |
|---|---|
| Primary axis | C1 calibration: distinguish named broken outcome rules from the correct rule. |
| Preservation axis | No change to the held eight cases, frozen rule, or historical scores. |
| Provenance axis | Separate committed source, inspected receipt, and new execution. |
| Principle | A control set is an instrument, not merely a list of examples. |
| Measurement | Mutate the rule the set is supposed to certify; count separated mutations. |
| Negative lesson | A set that passes a broken rule certifies nothing about that defect. |
| Positive bound | Four named mutations of one rule family are not fault coverage. |

## Evidence map

All paths below are relative to `mado-shokunin`.

| Key | Source path | Locator |
|---|---|---|
| D73 | `.ufo/waves/round-73/claims-declaration-r73.md` | C1 target, frozen sentence, named mutations, limits |
| R73 | `.ufo/waves/round-73/measurement-c1-r73.txt` | Lines 1–11 |
| B73 | `.ufo/waves/round-73/control-baseline-r73.txt` | Lines 1–7, pre-freeze C1 legs |
| J73 | `.ufo/waves/round-73/controls/c1-outcomes-r73.json` | First eight carried; final two added |
| M72 | `.ufo/waves/round-72/w1/R72MutBattery/R72MutBattery.md` | Battery M3 row; GAP-1, lines 56–75 |
| D72 | `.ufo/waves/round-72/claims-declaration-r72.md` | C2 predicate; erratum items 1 and 4 |
| F72 | `.ufo/waves/round-72/receipts/c1-r72-repair.txt` | Red-before and green-after lines 1–10 |
| H72 | `quality/counters/c1-r72-landing-controls.py` | `summary_green`, parsed-summary selection, outcome verdict |

## Revision and digest anchors

| Anchor | Exact value |
|---|---|
| Round-73 base | `d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce` |
| Declaration/control freeze | `87e4c61ac90e9ac587c9f65ac7844ded268d9046` |
| Round-73 instruments | `1459cca11fb5d3956a6e9a128217852dd0c28cb9` |
| Round-72 repair | `4f598cfd142e1bfcf4d63341e0b5ea11348c5c4c` |
| Earlier round-72 instruments | `9bcb4fd5b598844f168230dc05e441721d95b272` |
| J73 SHA-256, R73 line 1 | `263b3c5a288c45a59587890a7e4c2e6dc3389630e5dd4a5cd1731976b5d2832b` |
| Held eight SHA-256, R73 line 3 | `640fb44fdb1f31b4706b381c905fde4b5dae769bfd3e5b656bdb374bad58a793` |
| H72 SHA-256, R73 line 4 | `b6108c86e8e03befce50256e2381ec08f199a1ab7fe192aeedef70459c45857d` |

R73 was present on disk when inspected, but was not yet committed at the observed HEAD.
Its `rev=` identifies the measured instrument revision, not the receipt's containing commit.
B73 was read from the freeze commit; M72 was read from the base commit.
No measurement or selftest was executed to compose this entry.

## What the round-72 eight-case set missed

| Defect | Historical evidence | What the frozen set could not distinguish |
|---|---|---|
| Zero total accepted | M72 M3, GAP-1 | `return passed == total` versus `return total > 0 and passed == total` |
| Malformed later marker hides valid summary | D72 erratum §1 | Last prefix-matching marker versus last fully parsed summary |
| Why this matters | D72 erratum §4 | Neither `0/0` nor valid-then-garbled existed in the frozen eight. |
| Repair scope | Commit `4f598cfd` | Production parser repaired; regressions added in selftests, not frozen controls. |

The pre-repair helper selected the last prefix-matching marker before attempting a full parse.
The repair introduces `last_parsed_summary` and scans backward for a fully parsed summary.
Thus the defect is the predecessor behavior, not a claim that the repaired helper is broken.

| M72 GAP-1 receipt excerpt | Recorded result |
|---|---|
| Pristine `summary_green(0/0)` | `False` |
| Mutant-M3 `summary_green(0/0)` | `True` |
| Pristine outcome, `0/0`, kills 2 | `TARGET_MISSED` |
| Mutant-M3 outcome, `0/0`, kills 2 | `TARGET_MET` |
| M3 frozen outcome counter | `cases=8 correct=8 base_correct=4 verdict=TARGET_MET`, rc 0 |
| Consequence | Frozen success did not certify the positive-denominator guard. |

| F72 repair receipt | Before | After |
|---|---|---|
| `credit(valid-then-garbled)` | `False` | `True` |
| `summary_green(green-then-garbled)` | `False` | `True` |
| What this establishes | A real semantic defect existed. | The repair changes the relevant answer. |
| What it does not establish | Complete defect coverage. | Frozen eight-case discrimination of that defect. |

The repair commit also tightens failure-line grammar; that separate change is not C1's target.
D72 erratum §1 records the parser repros as harness selftest regressions (87/87).
D72 erratum §4 explicitly leaves both missing outcome controls for a later denominator.

## Frozen ten-case truth table

`MET` abbreviates `TARGET_MET`; `MISSED` abbreviates `TARGET_MISSED`.

| Case ID | Summary/input feature | rc | kills | Truth | Origin |
|---|---|---:|---:|---|---|
| `green-summary-exit0` | `12/12` | 0 | 2 | MET | Held |
| `failing-summary-exit0` | `3/12` | 0 | 2 | MISSED | Held |
| `green-summary-exit2` | `12/12` | 2 | 2 | MET | Held |
| `no-summary-exit0` | No summary | 0 | 2 | MISSED | Held |
| `garbled-summary-exit0` | `twelve/twelve` | 0 | 2 | MISSED | Held |
| `failing-summary-exit2` | `11/12` | 2 | 2 | MISSED | Held |
| `no-summary-exit2` | No summary | 2 | 2 | MISSED | Held |
| `green-summary-killed1` | `12/12` | 0 | 1 | MISSED | Held |
| `zero-denominator` | `0/0` | 0 | 2 | MISSED | New |
| `valid-then-garbled` | `12/12`, then cleanup marker | 0 | 2 | MET | New |

The cleanup marker is `MADO_LANDING_COUNTERS_SELFTEST: runner cleanup complete`.
It is not a parsed summary and therefore cannot suppress the earlier valid `12/12`.
R73 line 3 reports `cases=8 ... carried=yes`; D73 freezes byte-identical carry-forward.

## Named mutation discrimination

| Mutation | Named rule change | Held correct | Ten-case correct | Killed held/new | R73 line |
|---|---|---:|---:|---|---:|
| N1 | Drop `total > 0` | 8/8 | 9/10 | no / yes | 6 |
| N2 | Select last prefix match | 8/8 | 9/10 | no / yes | 7 |
| N3 | Accept `passed <= total` with positive total | 6/8 | 8/10 | yes / yes | 8 |
| N4 | Decide on kill count alone | 3/8 | 4/10 | yes / yes | 9 |

| Mutation | Exact separating cases reported in R73 |
|---|---|
| N1 | `zero-denominator` |
| N2 | `valid-then-garbled` |
| N3 | `failing-summary-exit0`, `failing-summary-exit2` |
| N4 | `failing-summary-exit0`, `no-summary-exit0`, `garbled-summary-exit0`, `failing-summary-exit2`, `no-summary-exit2`, `zero-denominator` |

Each of N1/N2 is separated by exactly one case, and that case is new.
`zero-denominator` also separates N4; it is not exclusive to N1.
N4's additional miss adds no marginal kill because the held set already separates N4.
This is marginal discrimination, not a one-case-to-one-mutant partition.

## Receipt outcome and gate

| Receipt locator | Exact observation |
|---|---|
| R73 line 5 | `MADO_R73_PRISTINE correct=10/10 misses=-` |
| R73 line 10 | `MADO_R73_KILLED killed=4/4 base_killed=2/4 (the held eight-case set must separate only two)` |
| R73 line 11 | `MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=4 base_killed=2 verdict=TARGET_MET rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9` |
| B73 line 7 | `PROTO_R73_C1 killed: new_set=4/4 held_set=2/4` |
| Frozen gate | `cases == 10`, `mutants == 4`, `killed == 4`, `base_killed == 2` |
| Score under D73 | `10 × killed / 4`: held 5.0000, new 10.0000 |
| Exit status | Assignment reports rc 0; bare R73 text itself has no rc field. |

## Recheck boundary

The declaration names this counting command; it is reproduced as a reference, not run here:

```sh
python3 -I quality/counters/c1-r73-summary-mutants.py --repo . --rev REV --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce --scratch-root DIR
```

| Boundary | What must not be inferred |
|---|---|
| Four named mutations | Not arbitrary program mutation or fault coverage. |
| Ten cases | No guarantee for behavior outside their inputs. |
| Committed decision functions | Not an end-to-end execution of the landing harness. |
| Syntactic substitutions | Not a claim that all semantically broken rules were enumerated. |
| Historical M5/GAP-2 | Counter `None`-acceptance mutation is outside this four-member family. |
| Selftest repair | Does not retroactively widen the frozen eight-case denominator. |
| Existing green baseline | Necessary context, not proof of adequate discrimination. |

Keep the controls, mutation definitions, held comparison, and receipt together.
A surviving named mutation is a measured limitation, never permission to rewrite frozen truth.
