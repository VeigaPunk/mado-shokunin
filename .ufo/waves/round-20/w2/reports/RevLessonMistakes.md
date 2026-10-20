# RevLessonMistakes — partly falsified: M4 misstates who caught the marker defect; M2/M8 evidence is not fully reproducible or integrated

## Findings

### Medium — M2’s round-19 red control is not runnable from the clean reviewed checkout

The source incident pointer resolves, and its red receipt is genuinely red: `.ufo/waves/round-20/evidence/crit29-inns-r19-shape.txt:3-10` records `FAIL_OPEN` after a forced mount failure, with the canary present; the receipt ends `exit=1` (`SHA-256 6b2baa25e082a751da2680980176125d7234babdbcc8cbf5dae6479876030c8c`). But the control fixture is not executable in the canonical `a4046a8` tree: `git -C /tmp/mado-r20w2-RevLessonMistakes ls-tree a4046a8216080d4004de3f268c62cf142095ac07 .ufo/waves/round-20/evidence/inns-r19-shape.sh` returned `100644 blob 26f037748f7b37012bec56579bb9ecad258edca6`. The checker rejects non-executable harnesses (`isolation-check.sh:11-13`).

In my clean `/tmp` clone, `bash /tmp/mado-r20w2-RevLessonMistakes/.ufo/waves/round-20/isolation-check.sh /tmp/mado-r20w2-RevLessonMistakes/.ufo/waves/round-20/evidence/inns-r19-shape.sh` printed `COULD_NOT_EVALUATE inns-r19-shape.sh (not executable)` and exited 2 (`/tmp/mado-r20w2-RevLessonMistakes/isolation-r19-shape.out`, SHA-256 `db8c8ac2d22da81a54d2f1895d89b08053e21a5e038f260b9778076a90da99df`). After adding execute permission to that clone copy only, the same checker returned `FAIL_OPEN` for `mount-nonzero`, `mount-noop`, `partial-arm`, `missing-target`, and `missing-stub`, `FAIL_CLOSED` for `unshare-refused`, positive control passed, exit 1 (`.../isolation-r19-shape-after-chmod.out`, SHA-256 `d1430d40641bb9cfe4c21bb28feca1dc280c537043652fb03eefb1ec7bec86db`). The stored receipt is valid for its measured `28c6837` commit (where the file was executable), but the documented check is not reproducible at the reviewed tip without an unrecorded mode change. The independent rerun report records the same issue at lines 5-8 (`w2/reports/RerunIsolation.md`, SHA-256 `162843f4eddda0724a34953b6822594ad6cbc0c85da2dd3e59e4acb7803dd691`).

### Medium — M8’s no-harm evidence is still pending in the committed result and the current diff summaries do not list every added finding

M8’s evidence pointers resolve, and the capture attribution is plausible: `CaseWrapperCrossCell.md:133` records the author telling TwRuleB the expected behavior; `CasePureCallables.md:181-193` records the corresponding discussion. Those reports support the row’s statement that the communication occurred.

The fix’s stated out-of-suite evidence is not yet a complete, committed acceptance record. `SCORECARD.md:1330` still says `whole-corpus diff vs 9c54c56: pending (wave 2)`. A W2 worktree artifact has since appeared: `CorpusDiffV2/9c54c56-vs-28c6837.json` (SHA-256 `598d5b709c1d514413380578625bac793c07360c8b71d48c139d8ade40e70fc0`) reports 6,207 added findings and zero lost rows, but its `added_rows` are grouped by class/rule/evidence with counts and sample examples (for example, `live_probe/journalctl` count 16 with 8 examples), not a row-by-row listing. The independent summary `CorpusDiffIndependent/corpus-diff-results.json` (SHA-256 `75ad0213d4044397c3415315593ea2dfc64a53c0aa648ce66dab360f645c7697`) reports `lost_row_count=0`, `repaired_rows=7938`, and no scan/hash errors, but only stores counts for repaired rows. Thus the existence of a diff is now corroborated, while the committed “pending” status and the lack of an exhaustive added-row listing mean the full out-of-suite gate is not yet evidenced as written.

The held-out result is also not a green validation: `precision-heldout-final.txt:1-3` (SHA-256 `2868c3c9c5aca8a63ab38c4077a518ef1b49048cf11d1cea3218028f2336d9cb) reports 0/12, and my `--heldout` reruns at `1f7f995` and `28c6837` each found 0 passed / 12 failed. This matches the scorecard’s explicit `0/12 → 0/12`; it shows no change, not that held-out cases pass. Keep M8’s out-of-suite claim conditional until L1 integrates a revision-bound, exhaustive diff result and judges the held-out failures in their declared outside-contract scope.

### Low — M4’s `captured-by: none` contradicts the cited prior review

`corpus/lessons/round-20.md:18` says the missing-marker defect was captured by `none`. However, `round-19/w2/reports/CriticC3W2.md:150-155` explicitly says the finding row had no lead marker and that the JSON did not match the docstring; round-19 lesson M14 also attributes the unmarked leads to `CriticC3W2` (`corpus/lessons/round-19.md:89`). The evidence pointer is sound, but “none” is not. M1 already uses the accurate nuance: “none at landing” while disclosing that CriticC3W2 saw it but it was filed as a limit. M4 should similarly distinguish “noticed/filed as a limit” from “no formal gate or correction at that landing.” CriticC3W2 report SHA-256: `5a8b756f63d13289c1ee93447e495338ac051def7b7892d056fb1d9eb0b64ed3`.

## Row-by-row checks

| Row | Pointer resolution / captured-by | Red-before evidence and result |
|---|---|---|
| M1 | Closure and both W1 scout reports resolve. “None at landing” is qualified by the fact CriticC3W2 saw the issue and it was filed as a limit. | `precision-1f7f995.txt:1-3` exists (SHA-256 `9fbef2c79dfbb9f29b9fd36d70661973fdcded3372ac0e99666c74127bdf50ff`). Re-run in the `/tmp` clone: `tw-precision.py 1f7f995` → 29/175, P 7/66, L 1/18, 146 case mismatches; counter exit 0 means it evaluated, not that all cases passed. At `28c6837`: 172/175, P 66/66, L 17/18. The receipt’s case-level `pass:false` rows supply the red. |
| M2 | `SentinelGatePath.md:75-79` resolves; “none (seat self-report)” matches the closure’s account that the scanner cannot see a written-then-run script. | `crit29-inns-r19-shape.txt` is red as above; clean-checkout reproduction gap is Finding 1. `crit29-isolate.txt:3-58` is green, six setup failures fail closed and the positive control passes (SHA-256 `812155500cc2f68b512fa271631251331e338f15c19101c69ebaa71d53ad0d8f`). Four mutant runs in the clone each exited 1 on the mode they break. |
| M3 | All named lesson/SCORECARD/LOG pointers resolve. “No checker read the sentences” is accurate as the process gap; it does not deny that the later closure caught them manually. | Clone run of `tally-check.py … --set red` produced five `MISMATCH` rows and `TALLY_SUMMARY: set=red n=5 match=0 mismatch=5 error=0`, `EXPECT_SUMMARY: 5/5`, exit 1 (`/tmp/mado-r20w2-RevLessonMistakes/tally-red.out`, SHA-256 `e9a0d76115249243c270fd2867ac8b8ddd9834b5808fabd2665a12c6979b645e`). The green set produced 4/4 matches, exit 0. Independent retained rerun: `w2/reports/RerunTally.md:22-25`, SHA-256 `61e5a89afb1df0e0243e95857d29726c88e07f49a815a43f5cabf870c8a98665`. |
| M4 | The docstring/row-builder and W1 report pointers resolve; capture attribution is the finding above. | Same precision red as M1; the scorecard’s final precision receipt reports P 66/66 and L 17/18, so the final fix is not all-green. |
| M5 | QUALITY 10 and all three named W1 reviewer reports resolve; captured-by names match the reports. The scorecard withdraws original criterion 30 before after-measurement (`SCORECARD.md:1285-1297`). | The original duplicate was explicitly identified by the W1 reviews, but the “screen all numbered criteria” is a human-review rule, not an executable check with its own red receipt. Later `w2/reports/CriticC2Final.md:25` says the replacement 30′ had a possible criterion-25 overlap that was not independently screened; keep the rule’s general effectiveness [UNK] until closure resolves that question. |
| M6 | Both named suite cases resolve; “L1 integration” is supported by the claimed integration change, and the original failure is independently reproducible below. | Rebuilt the broken v2 patch only in `/tmp` from the `f3da504` tool plus the committed `TwRuleB-v2.patch` (patch SHA-256 `be214cfcc7574f524470ff394aeb2629adc70fe0070fcf3f0866906e0d992277`). Pre-fix `--selftest` gives `eval-js-unparsed-clean FAIL want=(0, []) got=(2, [])`, 32/33, exit 1 (`/tmp/.../m6-bad-r17-selftest.out`, SHA-256 `58fc3c51549fda78c364a7b267923c94cab2d3c68ae6bba5f791d24a1f0188fe`); the r19 suite gives `js-cell-separate-kernel-clean FAIL want=(0, []) got=(2, [])`, 44/45, exit 1 (`.../m6-bad-r19-selftest.out`, SHA-256 `cd2f346beae67aa35ecbfa6f21f24aa31728c35deeee45677bfb8a240243f29c`). Final tool SHA-256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` passes the corresponding suites 33/33 and 45/45. |
| M7 | `SentinelPause20.md` H2 resolves and is the named capture. | Its `/tmp` replica records `git push origin master` rc 0 moving master `c101cc3 → 0107e84` (`SentinelPause20.md:45-60`, SHA-256 `cf52d8c1d9642db2d04a41c82266294485fb9ef63fa825bb0ec08fe566eff8b2`). This is the red hazard; I did not run a VCS write experiment. |
| M8 | The two W1 case reports substantiate the communication; L1’s “reading of seat reports” is a reasonable capture attribution. | The suite/case result pointers resolve. Held-out 0/12 → 0/12 and the current diff evidence are discussed in Finding 2; there is no separate red receipt showing the overfit-control itself distinguishes a contaminated suite. |

## Residual risk

- M5’s restatement-screen correction is evidenced by a human review of the original 30, not a reusable test; M5’s broad rule should not be treated as a fully validated detector of future restatements.
- M8’s data-only corpus-diff summaries and the still-pending committed SCORECARD claim should remain separate: zero lost rows is useful evidence, but the artifact needs a complete, revision-bound row listing and an explicit final disposition before the C1 no-harm guard is called closed.
- The round-20 held-out set is 0/12 at both tool revisions. It is accurately disclosed as outside-contract, but it does not contribute a green generalization check.

## Verification gaps

- Checks run in the own `/tmp` clone after removing `origin`: `tw-precision.py` at `1f7f995`, `9c54c56`, and `28c6837`; held-out precision at `1f7f995` and `28c6837`; tally red and green; isolation check on the legacy control, fixed harness, and all four named mutants; final `--selftest` on round-17 hardening and round-19 bashcvar; reconstructed pre-fix v2 `--selftest` on those two suites. All payloads were parser fixtures or `/tmp` canaries; no host binary, package command, live gate, or VCS write was run.
- Corpus-diff JSONs and peer reports were read as artifacts, not rerun. The committed `SCORECARD.md:1330` still records the whole-corpus diff as pending.
- No LSP caller/definition/diagnostic conclusion is claimed; this assignment checked Markdown pointers, reports, and receipts rather than callsites.

## Limits

Read-only review of the lane at the stated `a4046a8` tip plus the currently present W2 artifacts. The only permission change was on a copied `/tmp` legacy-control script. No source or lane file was edited except this report.

## Installs

None.

Report: .ufo/waves/round-20/w2/reports/RevLessonMistakes.md
