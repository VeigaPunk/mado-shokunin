---
source:
  - S183
verified-at: 2026-10-23 (S183 DOI metadata opened; prior-gate references checked)
recheck: on-source-or-gate-change
---

# Finite mutation suites: evidence and limits

## Scope

This note uses “mutation score” only as a summary of how a test suite treats a selected, finite mutant population. A score or pass verdict is conditional on the chosen mutants, subject/input population, oracle, harness, and frozen scoring rule. It is not a direct measure of real-fault detection.

The opened S183 source is Just et al.'s paper identity and title. The DOI reader returned CrossRef metadata with no abstract, so this note attributes no empirical result, method detail, or conclusion to the inaccessible paper text. Its title frames mutant-to-real-fault substitution as a question, not an answer. [S183]

## What a finite mutation gate claims

The round-28 C1 claim is deliberately bounded: its six registered legs test the frozen suite/counter behavior against named round-27 survivors, a rotated held-out set, a public reference set, specified boolean-word inputs, Q36 witness fixtures, and the Q37 population checker. Meeting those predicates at a revision is evidence about those artifacts and that enumerated challenge surface, not a claim that arbitrary real faults will be found. [`.ufo/waves/round-28/registration.md:17-55`]

A surviving mutant is evidence that the tested suite did not distinguish that mutant under the gate's observations; it is not, by itself, proof of a real defect. A behaviorally equivalent mutant cannot be distinguished by any test that observes the same behavior. If equivalent mutants remain in the counted population, they can appear as survivors; if they are excluded, equivalence classification affects the denominator. Neither mutation score nor a target-met verdict establishes that the selected mutants represent the distribution of real faults.

## Limits inherited by C1

- **Finite population:** conclusions stay within the mutants, subjects, and input cases actually named by the frozen legs; H2 rotation is evidence about H2, not every possible future mutant. The registration separately discloses that leg 1 depends on inherited ephemeral H1 data. [`.ufo/waves/round-28/registration.md:31-55,94-107`]
- **A passing finite suite can miss bypasses:** M26-8 records 6/10 self-test mutants and 3/6 Q37 mutants surviving, alongside Q36's receipt-format failure. This is evidence that initial mutation/fixture sets left concrete paths uncovered, not a population-wide fault-detection estimate. [`corpus/lessons/round-26.md:32`]
- **A counter can reward shortcuts:** M27-3 records flat-scan/shortcut readers meeting earlier counters, followed by v4 pilots missing target. A target must therefore be read with the mutant set and gate revision that produced it; passing a finite rule does not prove general implementation adequacy. [`corpus/lessons/round-27.md:15`]
- **No real-fault substitution result:** S183's opened metadata contains no abstract or article findings. It cannot support a claim that mutation scores predict real-fault detection, nor a quantitative transfer rate. [`corpus/SOURCES.md:195`; DOI reader output, 2026-10-23]

## Gate

- **S183 URL:** https://doi.org/10.1145/2635868.2635929
- **Access date:** 2026-10-23 (opened with the reader; CrossRef metadata, no abstract).
- **Located quote (11 words):** “Are mutants a valid substitute for real faults in software testing?” — DOI reader, CrossRef `title` field. This is title metadata, not a quotation from the paper body.
- **Source decision:** use S183 to identify and frame the paper's research question only. No article result or method detail is attributed to it.
- **Prior-gate evidence:** M26-8, [`corpus/lessons/round-26.md:32`]; M27-3, [`corpus/lessons/round-27.md:15`]. These lane records show concrete finite-suite survivors and shortcuts, and bound the lesson to observed gate behavior.
