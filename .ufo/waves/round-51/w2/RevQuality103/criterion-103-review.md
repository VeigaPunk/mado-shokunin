# QUALITY criterion 103 / M51-1 review

Axes: coverage and operability. This reviews the fixed criterion and its evidence chronology; it does not edit QUALITY or reinterpret the frozen claims.

## Verdicts

- **Grounded: PASS, with a citation precision defect.** Criterion 103 cites the actual round-50 verifier spot-check §2 D1, and lesson M51-1 records the same incident and identifies the missing integration-tip receipt as the failure mechanism. The spot-check says the report and LOG claimed `waves=2 settled=2` at `74782d39`, whereas the committed `receipts/wave-done-r50.txt` was measured at `8dbbf61a` and showed one wave; the w2 results arrived later at `c12b588e` (`corpus/lessons/round-50-verifier-spotcheck.md:56,91`). This directly motivates the rule. However, the current wording's phrase “the recorded final state in that spot-check says `74782d39` has two waves” is imprecise: §2 D1 distinguishes the report's assertion from its separately reported measurement. The assertion is not itself a committed final receipt. The same section documents the asserted two-wave result and the missing receipt, so the causal grounding remains sound.
- **Falsifiable: PASS.** The rule fixes a target revision and round, requires exact checker output plus exit status committed under that round's wave directory, and gives a reproducible audit: run the checker at the report revision, match recorded revision/round/outcome to report, and resolve receipt using `git cat-file -e REV:path` (`corpus/QUALITY.md:572`). A missing, stale, mismatched, or unresolvable receipt is a concrete failure. It is falsifiable as a receipt-provenance requirement, not as a proof of checker soundness; that declared limitation is appropriate.
- **Distinct from 102: PASS (separate observable), but adjacent.** Criterion 102 checks results-file presence and seat settlement at the scored report revision; 103 checks whether the final WAVE-DONE assertion is backed by the checker transcript at the integration revision (`corpus/QUALITY.md:569-572`). In D1, the checker had a truthful one-wave receipt, but the later report's two-wave claim had no matching final-tip transcript. Thus 102's state audit and 103's receipt-provenance audit can differ. The text also explicitly confines 103 to evidence provenance and defers wave-discovery/terminal semantics to the existing checker. Not a duplicate, though both rely on the same checker and round evidence.

## Round-50 D1 reproduction from committed evidence

Commands/evidence reviewed:

- `read corpus/lessons/round-50-verifier-spotcheck.md:56` — reports D1: assertion of two waves at `74782d39`; only committed receipt was measured at `8dbbf61a`, says one; w2 results came later at `c12b588e`.
- `read .ufo/waves/round-50/w2/ExecFreezeReplay/receipts/10-wave-done-r50-at-receipted-rev.txt` — exact command uses `--rev 8dbbf61a... --round 50`; output is `waves=1 settled=1 verdict=OK`, exit 0.
- `read .ufo/waves/round-50/w2/ExecFreezeReplay/receipts/08-wave-done-r50-at-tip.txt` — a later replay against `b4a79843...` reports one wave as well. This corroborates that the recorded old receipt cannot support a two-wave claim, but it is not the specified `74782d39` final revision.

The D1 evidence is internally coherent: a committed earlier receipt records one wave; the missing fact is not that the checker falsely reported one, but that the integration/report claim advanced to two without committing the corresponding re-run. The historical spot-check itself is the evidence for the two-wave state at `74782d39`; the supplied receipt is evidence of the mismatch, not the desired final result.

## Round-51 procedure / final receipt

At inspection, the lane was at `58f4d4fcf5f6e35b0c8103294849f94839c6cdc3`; `git status --short` showed untracked `w1.ready.dispatched`, `w2.ready.dispatched`, and `w2/`. `SCORECARD.md:2776-2781` still says w2 falsification is pending. The available `w2/RevReportEvidence/report-evidence.md:3,23-25` likewise explicitly says aggregate results and final receipt do not yet exist in inspected committed evidence. The currently visible round-51 wave directory has `w1-results.json` and W2 per-seat reports, but no W2 results/round-level final WAVE-DONE receipt in the committed tree listing. `corpus/lessons/round-51.md:32` describes the intended post-results, final-tip run-and-commit procedure, not proof that it has occurred.

Therefore, the requested final arm is **MISS / NOT YET EVIDENCED** at the inspected tip: no final integration receipt was available to validate or resolve with `git cat-file -e`. This is a temporal status, not a claim that eventual L1 integration cannot satisfy it. A later integration must use its actual report/integration revision, commit the exact `quality/check-wave-done.py --repo . --rev <that revision> --round 51` output and exit status under the round-51 wave directory, and demonstrate path existence at that same revision. A receipt measured against an earlier partial tip does not suffice. No checker was run for this review, because the assignment is to assess the eventual receipt and it was not yet present.

## Residual risk and verification gap

Criterion 103's audit is evidence-presence and revision-match, not an enforced transactional ordering: its own declared limit says it cannot prove the report was committed after the check unless integration preserves that order. It also delegates correctness of wave discovery and settlement to `check-wave-done.py`. The eventual integration revision/receipt and final report are absent from this inspected state, so the final green arm remains unverified.

## Deliverables

- `criterion-103-review.md` — this detailed criterion review.

Report: `.ufo/waves/round-51/w2/RevQuality103/criterion-103-review.md`
