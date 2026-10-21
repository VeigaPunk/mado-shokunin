# Round 20 — wave-2 dispositions (attempt-2 recovery, L1 MadoR20Recovery, 2026-10-21)

Wave 2 (attempt 1): 78 members, 76 reports, 2 dead without a report (`SentinelPostWaveScan`,
`ConnConsumers`; uncredited, not respawned). Registry `w2/reports/swarm-registry.json`,
spec `w2/spec.json`. Each row: the report's headline verdict, what the round did with it,
and where. "A1" = attempt 1 (`f8576f7`); "A2" = attempt 2; tool v3 = `3610e3e`, v3.1 = `a8960de`.
Re-verification of reused attempt-1 work is listed at the end.

| Report | Verdict (headline) | Disposition | Pointer |
|---|---|---|---|
| AdvCrash | falsified: RecursionError flips at half the old depth | fixed A2 (iterative eager walk, deep-stack thread); parity crashes kept as limit | `a2/evidence/guards-after-a8960de…` `crash_flip` 13→0; lesson M11 |
| AdvDepth | partly falsified: starred/dict-splat/lambda silently drop a spawn | fixed A2 (literal starred binding; unbindable calls and lambdas swept as `lead`) | guards `recall_lost` (silent-only set) |
| AdvLeadMarks | partly falsified: 11 mis-marked shapes; `globals()` reads fabricate leads | partly fixed A2 (namespace reads no longer reset; `miss-*` shapes found); A1/A2 decorator and `global`-in-helper marks kept as limits | note Limits; tool docstring |
| AdvPureShapes | partly falsified: 24 pure stdlib `from`-imports emit leads | fixed A2 (stdlib purity by process denylist, S113–S115) | guards `pure_rows` 24→0 |
| AdvRecallShapes | falsified: 49 certain real-execution shapes silently missed; one signal-contingent shape and one intentional old false-positive correction are excluded | fixed A2 within this frozen population (lead sweeps, `importlib` alias); later residual reviews found additional regressions | guards `recall_lost` 52→0; lesson M9 |
| AdvVcsForms | partly falsified: clusters/abbreviations flagged as writes | partly fixed A2 (short clusters); abbreviations and `=false` kept as limits | guards `vcs_fp` 31→20, `vcs_fn` 0→0 |
| AtkCasesH1 | partly falsified: vacuous case, inert evidence fields | limit: suite pinned at `f3da504`, no post-result edit | SCORECARD A2 results |
| AtkCasesH2 | partly falsified: 3 vacuous H cases, no cluster negative | limit (pinned suite); cluster negatives now in the a2 guard via AdvVcsForms | guards |
| AtkCasesH3 | partly falsified: one AdoptW2 want contradicts the contract | accepted as the stated `jj $c --help` miss (lesson Decisions); no suite edit | SCORECARD |
| AtkCasesL | partly falsified: lead definition finished after measurement | accepted as a claim-scope caveat in SCORECARD | SCORECARD A2 |
| AtkCasesP1 | partly falsified: one P case cannot fail | limit (pinned suite) | SCORECARD |
| AtkCasesP2 | partly falsified: dataclass/decorator P cases do not discriminate | limit (pinned suite); twins now covered by AdvRecallShapes in the guard | guards |
| AtkCasesP3 | partly falsified: 4 P cases certify shapes whose spawning twins went silent | fixed A2 (the twins are swept as `lead`) | guards `recall_lost` |
| AtkCasesS | partly falsified: `del-run` pins a guaranteed NameError as a lead | limit: a lead is "may run"; pinned suite unchanged | note §1 |
| AtkCasesW1 | partly falsified: `class-method-instance` want is wrong | accepted: the tool's detection is true; stays a failing case (lesson Decisions) | SCORECARD |
| AtkCasesW2 | holds | — | — |
| AtkFailingThree | partly falsified: 2 of 3 failures are stale wants; 174/175 corrected reading | reported beside the registered 172/175 (no suite edit) | SCORECARD A2 |
| AtkHeldout | partly falsified: held-out exclusion by a w1 hint; full-suite 172/187 | reported: 172/187 at `28c6837`, 174/187 at `a8960de` | SCORECARD A2 |
| ConnQueueClose | partly falsified: V5 tail off the queue; red harness mode 100644 | mode fixed A1 (`f8576f7`); V5 harm-watch provenance tail kept open in README queue | `a2/evidence/iso/crit29-inns-r19-shape.txt` |
| CorpusAddedAudit | partly falsified: ≥53 vcs false positives on the live corpus | partly fixed A2 (clusters); remainder limit | corpus diffs A2 |
| CorpusDiffIndependent | holds | — | `w2/CorpusDiffIndependent/` |
| CorpusDiffV2 | holds: 0 lost vs `9c54c56` | re-run A2 at `3610e3e` and `a8960de`; the run from `28c6837` found M15 | `a2/evidence/corpus-diff-*` |
| CorpusLeadAudit | partly falsified: 22 of 25 leads are visible helpers | limit: label fidelity, no verdict change | note Limits |
| CorpusRemovedAudit | holds | — | — |
| CorpusRuntime | partly falsified: one 30 s hang; duplicate observed+lead rows | fixed A2 (recursion guard, budget; same-command lead dedup) | lesson M10; guards `dup_rows` 0 |
| CriticC1Final | partly falsified: scope-local repair, corpus diff pending | addressed A2 (out-of-suite guard, corpus diff run) | SCORECARD A2 |
| CriticC2Final | partly falsified: 22/30 conditional; 21/29 conservative | both readings reported | SCORECARD A2 |
| CriticHarmAxes | partly falsified: note `surface:` head MALFORMED | fixed A2 (`scope:`) at `94b6925`, after tool measurement at `a8960de` | ReviewDocsV3 reproduced `measure.py` rejected=[] at `451c7e41`; the rejection still exists at `a8960de` |
| CriticHonestyFinal | partly falsified: receipt/mode defects, wording overclaims | mode fixed A1; wording reviewed in A2 rewrite of note/SKILL | — |
| MutBinding | holds (combined detectors) | — | — |
| MutEvidence | partly falsified: emitted totals unasserted | limit (counter reads rows, not totals) | — |
| MutIsolationCheck | falsified: skipping mount-noop greens a bad harness | fixed A1 (check v3) | `a2/evidence/iso/` |
| MutVcs | partly falsified: r19-vcs alone misses 5 mutants | limit: the H family kills them | — |
| ReopenBash | holds; two bookkeeping defects | Gate rendering kept; digest receipts as committed | — |
| ReopenExecModel | partly falsified: quote count/span | fixed A1 (lesson Gate S111) | lesson Gate |
| ReopenGitDocs | partly falsified: 16 words not 14 | fixed A1 | lesson Gate S099 |
| ReopenGitSource | holds | — | — |
| ReopenJj | partly falsified: `jj help` mechanism | fixed A2 (note §2 split) | note §2 |
| ReopenPyDocs | holds | — | — |
| ReopenPyShlexSub | partly falsified: `json.dumps` uncited | fixed A2 (S114) | SOURCES S114 |
| ReopenUnshare | partly falsified: S112 version wording, `--keep-caps` | recorded A1 (Gate caveats) | lesson Gate |
| RerunCensus | holds | — | — |
| RerunFrozen | partly falsified: frozen keys miss evidence drift | limit | — |
| RerunIsolation | partly falsified: one control not directly runnable | fixed A1 (mode) | — |
| RerunMeasure | holds | re-run A2: 22/30 at `a8960de` | `a2/evidence/harm/harm-measure-round-17.txt` |
| RerunPrecision | holds | re-run A2 | `a2/evidence/precision-a8960de…` |
| RerunRecall | partly falsified: `9c54c56` does not pass | context only (pre-harm tool) | — |
| RerunSuites | partly falsified: legacy selftest ignores two markers | limit | — |
| RerunTally | partly falsified: green accepts a wrong rule | limit (registered statements only) | QUALITY attempt-2 note |
| RevCrit10Application | holds; bare command exits 2 | fixed A2 (runnable form in QUALITY) | QUALITY attempt-2 note |
| RevDocstring | partly falsified: 4 false sentences | fixed A2 (docstring rewrite) | `tools/mado-tripwire.py:1-130` |
| RevKnowledgeNote1 | holds | — | — |
| RevKnowledgeNote2 | holds | — | — |
| RevKnowledgeNote3 | partly falsified: PATH-stub wording, S112 recheck, bash parity | fixed A2 (note head and §3) | note |
| RevLessonCorrections | holds | — | — |
| RevLessonGate | partly falsified: counts lacked command/date | fixed A1 | lesson Gate |
| RevLessonMistakes | partly falsified: M4 captured-by | fixed A1 | lesson M4 |
| RevLog | partly falsified: VCS summary and attempts overstate | LOG A2 entry states attempts and seats from the registries | LOG |
| RevQuality29 | partly falsified: checker leaked controls | fixed A1 (v3) and re-verified A2 | QUALITY attempt-2 note |
| RevQuality30 | partly falsified: corpus leg pending | run A2; M9 recorded against 30′'s scope | QUALITY attempt-2 note |
| RevReadme | partly falsified: coverage row omits Sources cell | fixed A2 | README |
| RevScorecard | partly falsified: rerun break; one count lacks derivation | A2 receipts carry commands | SCORECARD A2 |
| RevSkill | partly falsified: two overclaims | fixed A2 (SKILL section rewrite) | SKILL |
| RevSuiteEdits | partly falsified: py/sh asymmetry for call-before-def | limit | — |
| RevToolDiffEval | partly falsified: dotted rebinding silent drop | fixed A2 (`spawn_attr_leads`) | `a2/fixtures/dotted-rebind-sp` |
| RevToolDiffLeads | partly falsified: `vars()` lead, heapq lead, first-wins dedup | fixed A2 (namespace reads, stdlib purity); dedup by (class, rule) kept | guards `a2_mismatch` 0 |
| RevToolDiffVcs | falsified: `jj -R` collision misses; clusters/prefixes | fixed A2 (index anchor, clusters); ambiguous prefixes limit | `a2/fixtures/jj-R-*` |
| RevengeEnvBug | partly falsified (drafts only) | — (landed tool unaffected) | — |
| RevengeSuiteNegatives | partly falsified: one semantic error among clean pins | limit (pinned suite) | — |
| ScribeShonen | holds | used for SHONEN lines | report |
| ScribeTrendDraft | partly falsified: `json.dumps` citation | fixed A2 (S114) | SOURCES |
| ScribeW1Dispositions | partly falsified: 36 w1 findings not acted on | carried; A2 acted on the C1-relevant ones through the guard | this file |
| ScribeWaveAccounting | partly falsified: two 85-spawn attempts | LOG states the refused attempts | LOG |
| SentinelCommitSet | partly falsified: path/email privacy candidates | limit: lane-local absolute paths and the lane identity are intentional | — |
| SentinelHarnessNote | partly falsified: pass-through reading risk; PATH `cmp` | scope text in `isolate.sh` and the check (A1); note §3 rule 4 | `isolate.sh:1-4` |
| SimplifyFinal | holds | — | — |

Reused from attempt 1 after re-running at `a8960de`: the precision suite and counter
(`f3da504`), `tw-recall.py` and `tw-recall-split.py`, the 11 tripwire suites and frozen
replays (harm-watch PASS, `a2/evidence/harm/`), `measure.py` c1 22/30, `tally-check.py`
(9/9 expected), `isolation-check.sh` and every committed harness and mutant
(`a2/evidence/iso/`), the census, and the wave-2 fixture populations (counted by
`a2-guards.py`). Discarded: attempt-1 SCORECARD after-readings at `28c6837` as C1's final
state (superseded, kept append-only), and the `28c6837` capability-row evidence pointer.
