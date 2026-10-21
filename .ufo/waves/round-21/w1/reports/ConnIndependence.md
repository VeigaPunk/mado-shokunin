# C1/C2 causal-separability review

## Axes

- **C1 — operability residual repair:** scanner behavior against frozen semantic truth cases and the bounded retained-memory/resource workloads.
- **C2 — calibration / independent artifact integrity:** a standalone artifact-only assessment-bundle gate, not a historical criterion-count increase.

Scope is advisory: this is not an admission judgment. I read the round-21 registration, the round-20 verifier spot-check lesson, and current-round FixtureAssessment, FixtureResource, and CriticRegistration reports. No gate/classifier, fixture code, or scanner was run; no measurements or installations were made.

## Evidence and separability

The registration draws a useful **runtime-output boundary**: C1 compares before/after scanner results against the same independent truth fixtures, resource recipes, and frozen whole-corpus population; C2 is to validate artifact bundles, “reads no tripwire output,” and invokes no classifier (`registration.md:7-9`). C1’s resource fixture proposal separately records three bounded workloads and explicitly says no scanner measurement was run (`w1/reports/FixtureResource.md:5-20,24-30`).

The boundary is not yet a demonstrated **evidence-lineage boundary**. C1 depends on frozen population/oracle artifacts; C2’s registered inputs include frozen population hashes and oracle provenance, while its fixture population includes historical-miss disclosure and round-20 assessment cases (`registration.md:7-9`; `w1/reports/FixtureAssessment.md:16-23`). The evidence inspected does not establish whether those C2 population/oracle references are disjoint from the C1 manifests or only re-describe them. **[INFERENCE]** If a shared manifest or oracle receipt is used both to score C1 and to establish C2’s integrity/provenance pass, a clean C2 result certifies the bytes/claims it consumed, not an independent confirmation of C1 correctness. Keep that distinction explicit even if the current gate has no direct scanner-output dependency.

Round 20 is a concrete warning against recasting shared evidence as another axis: the committed closure measured 172/175 against the unchanged target, retained three misses, and found criterion 30-prime used C1’s P/L counter; it ruled the claimed C2 calibration unprovable rather than independent (`corpus/lessons/round-20-verifier-spotcheck.md:40-52,75-81`). The current C2 fixture list has 20 cases, several testing variants of the same semantic families (history preservation, SHONEN structure/authority, registration/hash integrity). Those are useful case coverage, but neither 20 cases nor multiple variants of one rule should be reported as 20 independent criteria or independent axis gains (`w1/reports/FixtureAssessment.md:16-23`).

There is also a limit on what C2’s chronology checks can establish. Registration calls for checking registration-before-measurement, but the assessment proposal says its timestamps are synthetic artifact-order values, not wall-clock or commit-ancestry authentication. The current-round registration explicitly makes timestamps artifact assertions unless bound to provenance (`registration.md:21`; `w1/reports/FixtureAssessment.md:23`). CriticRegistration notes that round-20 M13 was a real prior sandbox measurement before the later registration, and that hashes/commit ancestry alone cannot rule out such an event; it also says no current-round M13 violation is established (`w1/reports/CriticRegistration.md:10-20,36`). Thus C2 may establish integrity of declared artifacts and declared order, but must not be presented as proof of actual prospective/blind oracle authorship absent stronger event provenance.

## One bounded proposed move

Before gate integration, freeze a **causal evidence-partition contract with a cross-over negative-control pair**:

1. Give C1 truth/resource manifests and scanner observation receipts a C1-owned evidence root; give C2 assessment fixtures, expected outcomes, and gate receipts a separate C2-owned root. Shared registration and historical round-20 facts may be referenced as immutable context, but label them as such and do not treat C1 measurement outcomes as C2 pass criteria.
2. Add two synthetic, pre-authored controls to the C2 fixture contract: (a) vary only a C1 current-measurement result/reference while holding the C2 assessment bundle fixed; the C2 verdict must be invariant; (b) alter a C2 assessment artifact’s bytes while holding C1 fixture and outcome evidence fixed; C2 must return its registered non-clean result while C1’s case verdict remains invariant. This is a specification for later verification, not a request to run measurements in this wave.
3. Report C2 as one capability result with per-family coverage and per-case outcomes. Do not convert the case count or the integrity of shared historical context into an independent criterion count.

This improves **C2 calibration** by testing the claimed non-dependence directly and protects **C1 operability** from borrowing a gate result as behavioral/no-harm evidence, without changing C1’s frozen 175-case history, new oracle target, or bounded resource acceptance rules.

## Risks and verification boundary

- C2 intentionally checks disclosure of historical rejected targets, so its bundle cannot be wholly ignorant of C1 history. Keep that dependency limited to frozen historical context; the cross-over must vary current C1 measurement evidence, not rewrite the registered historical facts.
- The negative controls establish functional dependency separation only for the tested schema and bundle. They do not prove that no unrecorded earlier measurement occurred. C2’s result must remain scoped to artifact integrity/order assertions unless an independently controlled durable event witness is added.
- No implementation or measurements were available in this wave, so the proposed invariance and sensitivity conditions are unverified. Main’s later verification should inspect dependency/input fields and compare the paired C2/C1 case verdicts against the frozen manifests; do not infer success from fixture counts alone.

Tool installations: none.