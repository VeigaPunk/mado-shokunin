# ShonenSubjects — advisory review

Date: 2026-10-21  
Verdict: **No current wording mismatch or concrete C2 topic-classification defect found.** The matcher correctly distinguishes the preserved round-20 wrong-topic transcription from the canonical four-box fixture in the recorded candidate run. This is a narrow artifact-topic check, not a semantic review or promotion decision.

## Reviewed identity and scope

- Candidate under review: `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.
- Current `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py` SHA-256: `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/SHONEN.md` SHA-256: `c723b7413170aa9952bd071941a3e6376527f1e2cc6ab48fa2a85c489b3b3e99`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-20-verifier-spotcheck.md` SHA-256: `d3941b28f84d0bf05e0d4cf610b05be6b65b7bd8b5502ff34b783f3907c066f6`.

## Four canonical subjects versus C2

`SHONEN.md:5,7,9,11` contains four `[~]` assertions. `tools/mado-assessment.py:20-25` hardcodes the same four subject strings, respectively; no text mismatch was found.

| Box | Exact subject in `SHONEN.md` | Required substance for the future report |
|---|---|---|
| 1 | `SKILL.md contains real decision tables, error patterns, checklists, cited sources` | Assess the actual tables, error patterns, checklists, and cited sources—not merely source curation or the existence of a round artifact. |
| 2 | `At least one end-to-end domain task executed and logged in LOG.md` | Assess an executed end-to-end domain task and its LOG record—not a file-plane change or a generic no-harm claim. |
| 3 | `Instructions executable by an agent without oral context` | Assess whether the instructions are executable without oral context—not the existence or count of dispatched advisers/reports. |
| 4 | `No cross-domain bleed (PROVINCE.md still accurate)` | Assess cross-domain bleed and PROVINCE accuracy—not an adjacency/no-harm verdict alone. |

At `tools/mado-assessment.py:128-145`, the checker requires four distinct valid box numbers, nonempty evidence, a `~` or `x` mark, and the corresponding hardcoded subject phrase as a case-insensitive substring of that row's evidence. An `x` additionally needs the literal named-non-author-verifier form. The code explicitly says this checks the declared subject, not whether evidence proves it (`:142-145`).

## Historical wrong-topic case

The lane's sealed assessment oracle preserves the historical four rows as inert text at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json:50-58`; the fixture rows are also at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/round20_wrong_topic_shonen.json:7-13`. They substitute “claims measured with receipts,” “no axis harmed,” “sources curated,” and “mistake mined” for the four canonical subjects. This agrees with the recorded independent finding at `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-20-verifier-spotcheck.md:24,79` and round-21 M6 at `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-21.md:16`.

The recorded candidate receipt `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/evidence/assessment-candidate.json` reports `round20_wrong_topic_shonen`: `pass=true`, observed exit `1`, `finding_ids=["wrong_topic_shonen"]`; `round20_canonical_shonen_corrected`: `pass=true`, observed exit `0`, `assessment_clean`; overall `20/20`, exit `0`. The corrected fixture at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/round20_canonical_shonen_corrected.json:7-13` uses the exact four SHONEN subjects and keeps each mark `~`.

## Findings by severity

### No actionable implementation finding

The current C2 topic strings match the current canonical SHONEN subjects, the fixed four-box shape is enforced, and the recorded wrong-topic/corrected controls have the expected classifications.

### Medium — same-revision verification gap (not a demonstrated matcher failure)

The recorded assessment run is bound to commit `843d301d1b17af78427918f7845af336b2218de0`; its embedded self-test tool hash is `9d976face474379119da630f2963f6da1a482073327e6f3d4876fa8114937a98`. Comparing that version with candidate `f499a8db7171b7476fe9f204ab9edbac5a956fa9` shows a self-test-only change: the current code adds expected-finding-ID assertions in `selftest()` (`tools/mado-assessment.py:175-197`). The `check()` topic matcher at `:91-155` is unchanged, so the old receipt is relevant to the matcher but does **not** establish that the current `5101c317…` file passes its strengthened 20-case self-test. No current-version replay was run in this review; L1's final verification should bind the self-test result to the current code hash before describing it as a current pass.

## Residual risk and future report requirement

- The matcher is a phrase-presence filter over JSON evidence. Quoting a canonical subject can satisfy it without substantively assessing the box; the artifact result also disclaims authenticated chronology, authorship, semantic proof, and promotion authority (`tools/mado-assessment.py:152-155`). It must not be treated as the non-author assessment required by SHONEN.
- `SUBJECTS` duplicates wording from `SHONEN.md` rather than deriving from it. They match now, but a future wording change could make the checker stale without a source-linked test.
- Round-21 M6 explicitly requires the report to assess the actual four boxes, not claims/no-harm/sources/mistakes, and keeps author rows `[~]`; no dispatched adviser supplies non-author promotion authority (`corpus/lessons/round-21.md:16`). A future report should therefore contain one evidence-backed row for each exact subject above and retain `[~]` absent a named, genuinely non-author verifier. This review does not assess or clear the underlying promotion claims.
- The original historical report is outside this lane. I did not open it; review of that transcription uses only the lane-preserved inert fixture and the cited lane lesson.

## Verification limits

No tests, scanner probes, or other runtime were run; the observed output above is from the committed receipt, not a fresh execution. No tools were installed. LSP is not mounted here (`read xd://lsp` returned “No such tool”), so no LSP status/references/definition/diagnostics were available; literal search was used only for navigation, not as semantic proof. Source lines, the fixture, recorded output, file hashes, and the candidate diff are the review basis.

Report: .ufo/waves/round-21/w2/reports/ShonenSubjects.md
