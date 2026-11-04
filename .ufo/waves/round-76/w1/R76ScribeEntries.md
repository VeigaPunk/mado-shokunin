# R76ScribeEntries — scoped scribe report

## Behavior and axes

Drafted the two admitted knowledge entries from supplied committed evidence only. Axes: calibration (separate outcome-field scoring), operability (bounded delete-flow classification), and no-harm/provenance (no production edits or new measurement). Both drafts use evidence tables, exact path:line locators through explicit aliases, and `[INF]` for deductions. Neither draft exceeds 200 lines (written bodies are under 100 lines each; no separate counting check run).

## Artifacts and touched surfaces

- `.ufo/waves/round-76/w1/R76ScribeEntries/entry-outcome-field.md`: contract field, redundant-echo negative result, four observable mutations/separators/scores, sixteen labels, deterministic case-change challenge, limits, denominator conflict.
- `.ufo/waves/round-76/w1/R76ScribeEntries/entry-interprocedural-del.md`: D3/D4, twelve appended labels and held/candidate classifications, negative boundaries, population interpretation, limits and provenance conflicts.
- `.ufo/waves/round-76/w1/R76ScribeEntries.md`: this report, at the explicitly assigned report path outside the per-seat draft directory.
- Created then removed empty `/fast/scratch/hyaku/mado-r76/R76ScribeEntries/`; no receipt generated there.

The L1 owns integration. No committed corpus, production instrument, label set, registry, ledger, judge, state, fleet-root tracked file or sibling directory was modified.

## Exact shell commands and observed outcomes

Only these shell commands were executed; all returned normally without error:

```sh
mkdir -p /fast/scratch/hyaku/mado-r76/R76ScribeEntries
git -C /home/vgpnk/Projects/shokunin/mado-shokunin log -1 --format='%H %s' -- .ufo/waves/round-76/measurement-c1-r76.txt .ufo/waves/round-76/measurement-c2-r76.txt .ufo/waves/round-76/receipts/label-derivation-r76.txt
rmdir /fast/scratch/hyaku/mado-r76/R76ScribeEntries
```

The log command returned:

```text
cb713254ee9926e036e594312fdc61b57825526b round-76: freeze v2 - label set v3 with its evidence derivation, the named outcome rule and the four observable outcome mutants; echo-dropping class recorded unobservable
```

This is the latest matching path-history commit, not proof that all three paths originated at that commit. File reads/searches used the dedicated read/glob/grep tools; writes used the dedicated write tool. Read the frozen declaration first, both measurements, label derivation, both predecessor entries, baseline, harness rule/challenge source, counter mutation/scoring anchors and all twelve appended fixture sources. Skills read: godspeed and agent-self-evaluation. No tool installation/update occurred.

## Gates and execution evidence

No counter, fixture, selftest, build, lint, verifier, mutation test or other runtime was invoked. No git/jj mutation, publish, deploy, desktop/session/service/network probe or credential access occurred. This is a scribe-only handoff, not an independent certification or judge result.

| Recorded evidence | Observed receipt result | Revision in receipt |
|---|---|---|
| `.ufo/waves/round-76/measurement-c1-r76.txt:19-23` | Four mutants killed; held mz-only scores all 16/16; `cases=16 correct=16 mutants=4 killed=4 base_killed=0 verdict=TARGET_MET` | `cb713254ee9926e036e594312fdc61b57825526b` |
| `.ufo/waves/round-76/measurement-c2-r76.txt:130-143` | Four held misses; `population=20 readers=13 guarded=13 unguarded=0 controls=59/59 base_controls=55/59 verdict=TARGET_MET` | `755b339f1f6ec18f45b494d40515aecdbe9ceb73` |
| `.ufo/waves/round-76/receipts/label-derivation-r76.txt:1-18` | Sixteen table rows agree; `DERIVATION: all labels re-derived` | Not printed |

The supplied assignment says measurement rc 0, but the two measurement files read contain stdout without a command/rc trailer. This seat does not claim to have independently observed those process exit codes. The label receipt contains derived labels, not the raw SELFTEST/M-Z/M-R transcripts; the declaration supplies that derivation provenance.

## Findings and verbatim conflicts for canonical judgment

No severity grade assigned; these are provenance observations, not a re-grade or verdict.

1. Declaration `.ufo/waves/round-76/claims-declaration-r76.md:67-69`:
   - “A mutant is killed iff its two-field score is below fifteen.”
   - “a mutant is base-killed iff its mz-only score is below fifteen.”
   Final target at lines 71-73 uses sixteen; `quality/counters/c1-r76-outcome-field.py:393-394` implements `score < len(cases)` / `base_score < len(cases)`. Receipt lines 19-21 classify 15/16 mutants as killed. Draft preserves rather than repairs this conflict. Counter header also retains “Fifteen REAL `bash` fixture lanes” (line 10), while constants at lines 68-69 are sixteen.
2. Frozen C2 controls `.ufo/waves/round-76/controls/c2-cases-r76.json:3` includes “thirteen appended” and “name bound after the delete”. Declaration lines 108-127 enumerates twelve appended cases, and receipt lines 1-2 records 59 total / 47 carried. The twelve actual entries are at controls lines 288-359.
3. C2 receipt `.ufo/waves/round-76/measurement-c2-r76.txt:142` says `(the held round-74 rule must miss the target)`; line 82 identifies `quality/counters/c2-r75-shapes.py` as the held counter.
4. Pre-freeze `.ufo/waves/round-76/control-baseline-r76.txt:4-7` names `outcome-term-dropped`, `prefix-match`, `first-witness-wins`, `case-insensitive`; the final measurement lines 19-22 names `outcome-summary-only`, `outcome-killed-only`, `outcome-killed-any`, `outcome-killed-or`. Both record 0/4 held kills, but these are not the same named mutation set. The entry grounds the final named comparison in the final measurement, not in an assertion that the baseline used identical final mutants.
5. Assignment summary says “20 readers / 13 guarded / 0 unguarded”; actual C2 contract is `population=20 readers=13 guarded=13 unguarded=0`. Draft explicitly uses the receipt's population/reader distinction.
6. `callee-del-param-rebound` source replaces the parameter with a keyless dictionary before deletion (controls line 338). `[INF]` Executing that delete raises `KeyError`; its guard=yes label is syntactic carrier identity, not successful runtime execution. The live-copy rebinding negative is separately represented at lines 301-304.

## Out of scope and known limits

No integration, new measurement, doc correction, source registry extension, instrument last-change analysis, command/rc reconstruction or canonical judgment. Existing frozen evidence remains unchanged. The echo-dropping outcome class remains unobservable under its declared kill-path premise. D3/D4 remain syntactic, line-order-bounded, simple-call/env-named-flow approximations; no general Python execution guarantee is claimed.

## Self-evaluation (not an execution gate)

| Axis | Score / 5 | Evidence and improvement |
|---|---|---|
| Accuracy | 4 | Exact receipts and conflicting denominators retained; raw derivation transcripts and rc are unavailable in the supplied receipt bodies, so claims stay qualified. |
| Completeness | 5 | Both requested entries include every named mutation, separator, case, negative and declared limit. |
| Clarity | 4 | Tables separate candidate/held and expected/observed; alias citations require consulting the locator table. |
| Actionability | 4 | Two integration-ready drafts provided; L1 still must resolve frozen-text contradictions through canonical judgment, not silent edits. |
| Conciseness | 4 | Each draft is under 100 lines; this audit report deliberately repeats conflicts to keep the handoff self-contained. |

Overall 4.2/5. Highest-impact improvements belong to canonical reconciliation of the frozen denominator and baseline-mutant provenance, not to invented execution evidence. Self-check: the user can integrate the two bounded entries without mistaking this seat for an executor.
