# R53Four33 — cross-claim/source connector

Axes: **operability** (C1) and **coverage** (C2).

## Evidence

- [OBS] Frozen C1 requires a newly committed scratch-aware counter that reports `TARGET_MET` on production ledger, `TARGET_MISSED` on no-work and every frozen forgery, with exact population coverage and non-self pointers; explicitly structural, not semantic (`.ufo/waves/round-53/claims-frozen.md:5-7`). C2 separately requires append-only P16–P18 correction, rejection of old/acceptance of corrected entry by a bound counter, and independent source-truth review; expansion credit additionally requires a source row opened this round and uncovered ground (`:9-13`).
- [OBS] Existing indexed r52 entry still has the recorded P16/P17/P18 defects; the r52 lesson details splice, misattribution, and mislocalization (`corpus/knowledge/hyprland-synthetic-dispatch-r52.md:28-30`; `corpus/lessons/round-52-verifier-spotcheck.md:36-40`). This is routed evidence, not a fresh reproduction.
- [OBS] The sources registry contains the r52 tagged source rows and hashes (`corpus/SOURCES.md:320-323`), but existing rows do not satisfy the frozen requirement for a source row opened this round. Registry identity/pin binding is provenance, not proposition entailment.
- [INFERENCE] A non-obvious compatible move is an evidence handoff ledger with disjoint C1/C2 namespaces: one record per frozen predicate/control, recording input revision and digest, exact command/output, and the specific artifact/source row. C1 records structural population/cardinality and pointer checks; C2 records each proposition's exact pinned quote and location plus independent reviewer outcome. This shares a compact audit format while preventing one predicate's pass from standing in for the other. It improves operability (repeatable, attributable evidence) and coverage (proposition-specific traceability) without collapsing their independent acceptance criteria.

## Risks and verification

- A shared record format can create false confidence if the C1 structural pointer is treated as semantic support or if a C2 quote match is treated as entailment. Preserve separate predicates and the independent review requirement.
- This proposal does not prove a round-53 counter exists, any control passes, corrected source text is true, or expansion credit is available.
- Verify only on the registered final revision: C1 production ledger met and no-work/every forgery missed, with exact population and non-self pointers; C2 old bytes rejected/corrected bytes accepted, proposition-by-proposition pin/quote binding checked against source bytes opened this round, and independent non-author review. Check coverage-map novelty before any expansion claim.

## Evidence boundary

Source-only local reads; no live probes, producer execution, package queries, external fetch, or repository mutation. Disk-guard executable was not located at the attempted lane/tools path; `df` showed `/home` with 589G available. Scratch path `/fast/scratch/hyaku/mado-r53/R53Four33` did not exist; no scratch artifacts were created. No tools installed.

## Trailer

Attacked predicate: C1 frozen structural accountability controls and C2 frozen proposition-grounded correction/provenance; cross-claim risk of confusing structural pointer validity with source entailment.

Exact command/output: Specialized reads of lane `SKILL.md`, claims freeze, SOURCES registry, and r52 report/entry. `df -h /fast/scratch/hyaku/mado-r53/R53Four33 /home/vgpnk/Projects/shokunin/mado-shokunin` → `df: /fast/scratch/hyaku/mado-r53/R53Four33: No such file or directory`; `/dev/mapper/root 930G 307G 589G 35% /home`. No test/counter command run.

Newly opened external sources: none; no URL/date/quote applies.

Report path (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`): `.ufo/waves/round-53/w1/R53Four33.md`
