# R56W3RevTrendAudit — attempt-2 trend evidence

Attacked: attempt-1 trend-verdict evidence, exclusively at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`, compared with base `13f0acbe3a15da2d9c08357a576d91dcadc85273`. Axes: expansion, quality, discernment. These findings check evidence, not operator/closure judgments or admission.

## Findings by severity

### Cosmetic — quality correction count is eight E rows, not seven

`corpus/lessons/round-56.md:30-31` says “seven E rows (E01-E07, E09)”. That enumerates eight. Comparing proposition cells in the originally audited `28fc86ac` entry with the assigned tip independently yields:

```text
changed_propositions K count=9 K01,K05,K07,K08,K14,K16,K18,K21,K27
changed_propositions E count=8 E01,E02,E03,E04,E05,E06,E07,E09
rc=0
```

Input: the entry blobs at those two revisions, not working-tree content. The exact `python3 -I -c` command and complete entry diff are in the receipt. The 9-K count holds; the 7-E count does not. Recommendation: correct the bookkeeping in a permitted integration, not the frozen predicates. No change made here.

## Evidence verdicts

| Evidence axis | Stability | Decisive observations |
|---|---|---|
| Expansion improved | **HOLD**, scoped | Base-specific autoreload-chain keyword search in `corpus/knowledge` returns no matches, rc 1. Broad registered search does find old unrelated inotify mentions, general reload instructions and option fixtures; “0 citations” is not “0 keyword hits”. Current entry holds the new chain. Registry is 319→332, new ids S383–S395, removed=0. `git diff BASE TIP --stat -- corpus/knowledge` returns only the new entry, 167 insertions, rc 0. Tool exists as regular executable blob `089c2a697f7eb6e6d120b16a8831876d177eebfe`. |
| Quality unprovable-but-better | **DRIFTED**, numeric evidence only | All six w2 audit reports A–F exist at tip, rc 0; their verdict and counter-forgery lines remain present. Actual changes are 9 K + **8 E**. Entailment remains explicitly outside the counter in registration-v2:82–84. The qualitative judgment is not re-scored. |
| Discernment unchanged at filing | **HOLD**, pinned filing record | Lesson:51 says outside spot-check pending; :55 explicitly says lane-dispatched seats are not independent verifiers. LOG:2630 says no non-author admit/reject sample at filing. Direct `git cat-file -e TIP:corpus/lessons/round-56-verifier-spotcheck.md` returns absent, rc 128. This is consistency with filing evidence, not a universal assertion about external records. |

Representative audit lines: AuditA:40/44 calls K01/K05 OVERREACH; AuditB:12–13 calls K07/K08 SUPPORTED (narrow), so not all nine changes were corrections of false propositions; AuditF:24–26 calls E02–E04 OVERREACH; AuditA:50–53 records false propositions still passing TARGET_MET. Reports score the earlier `28fc86ac` content, not a fresh entailment audit of the assigned corrected tip. Their persistence proves historical evidence exists, not that all corrected sentences are now independently verified.

Pinned LOG:2630 actually phrases quality as “improved with a trade disclosed”; the assignment's “unprovable-but-better” is not a verbatim quotation of that LOG line. No policy verdict is inferred from that wording difference.

## Commands and deliverables

Full exact commands, stdout/stderr and return codes, organized per verdict:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevTrendAudit/receipts/trends-a2.txt`
- This report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevTrendAudit.md`

Decisive command families: `git -C LANE grep -n -i -E ... BASE/TIP -- corpus tools SKILL.md PROVINCE.md`; narrower chain keyword query against `corpus/knowledge`; requested `git diff BASE TIP --stat -- corpus/knowledge`; `git ls-tree` for each named audit and the capability; pinned report-verdict `git grep`; isolated Python registry/proposition counting over `git show` blobs. All commands include absolute lane paths in the receipt. Broad grep has rc 0 at both revisions; the narrow base null query has rc 1. A wildcard `ls-tree` query returned empty and was explicitly discarded as absence evidence; full listing and direct sidecar lookup replaced it.

## Residual risk and verification gaps

- No C1/C2/C3 counters, control harnesses, selftests or live compositor commands were run: this seat re-derived trend evidence, not frozen claim scores or fresh source truth. Runtime/caller/resume-continuity checks are not touched by this documentation-only assignment.
- `read xd://lsp` returned “No such tool”; no LSP status/references/definitions/diagnostics route exists in this tool inventory. Read-only git-object/text fallback is not semantic caller proof.
- No universal external non-author-sample census was possible within this lane-only scope. The filing's own explicit pending status and absent named closure sidecar are the bounded evidence.
- No scratch files, clones, fixture repos, installs or updates were created; no cleanup was required. No tracked files, host state, fleet files or frozen contracts were changed. No delegation/background jobs.

Self-evaluation: accuracy 4/5 (external sample absence remains bounded); completeness 4/5 (historical evidence re-derived, no new entailment judgment by design); clarity 4/5 (full receipt is lengthy, report isolates decisive outputs); actionability 5/5 (exact E-row correction and source location); conciseness 4/5 (receipt retains full grep/diff output for reproduction). Overall 4.2/5. Main improvement: preserve the bounded absence wording when summarizing; user agreement expected only within that scope.
