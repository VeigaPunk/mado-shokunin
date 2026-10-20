# RevLog — partly falsified: most measurements match, but the VCS summary and wave-attempt account overstate the evidence

## Findings

### Medium — the “git/jj help and dry-run forms are not writes” summary is too broad

`LOG.md:1350-1351` presents git/jj help and dry-run forms as non-writes without naming the recognized cases or exceptions. The committed round-20 E4 correction explicitly records contrary forms: plain `jj git push --dry-run` snapshots the working copy and stays a `vcs_write`; `git commit -n` means `--no-verify`, and `pull -n`, `merge -n`, `cherry-pick -n`, `add -N`, and `commit -n` are writes (`SCORECARD.md:1311-1316`; `corpus/lessons/round-20.md:41,86-90`). This is a safety-relevant overgeneralization in the summary, not a problem with the underlying measured exceptions. Recommend narrowing it to the tested, recognized non-write segments and keeping the write exceptions explicit.

Evidence: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show --format= --unified=15 4362219 -- LOG.md` adds the blanket sentence; the cited SCORECARD/lesson lines list the counterexamples. `sha256sum`: `LOG.md` `a70427423e39d2f84bc0aff0ae9a3647ef8eb630b8003f40afb33e2eb8fdaa94`; `SCORECARD.md` `0b03337880a502b9984ae7b606000a398df536cdb71faced901fecdc9e647ed0`; `corpus/lessons/round-20.md` `bf55c34db05e47a1499e67567df0d2a8841a4337da26c25a46a10c03e1e324e0`.

### Medium — wave-1 refusal/retry chronology is not reconciled

`LOG.md:1360-1361` states that all 85 seats were refused twice by the 100-job cap and then spawned on the third attempt. The committed artifacts do establish 85 members and 85 reports with zero dead seats, but do not establish that chronology: `w1/task-result.json:1` records attempts `[[1,"16:36",85],[2,"16:39:52",85],[3,"16:42:57",0]]`; `w1/dispatch.json:16-20` records one batch with `{spawn:85,resume:0,total:85}`; and `w1/record.json:5` timestamps registry creation at `19:36:34Z`, matching the first attempt minute under the report’s local-time mapping. The separate wave-accounting review explicitly leaves whether the repeated 85 represents a duplicate spawn or a re-record as `[UNK]` (`w2/reports/ScribeWaveAccounting.md:13,20-22`). Keep the 85/0 seat totals, but mark the two refusals, cap attribution, and “third try” as unresolved until reconciled.

Evidence: the artifact values above and `w2/reports/ScribeWaveAccounting.md:13` (“two attempts each recorded 85 spawns”; duplicate-spawn question `[UNK]`). `sha256sum`: `w1/task-result.json` `5bb18e899b6adb47d500dc96e946dce70c29319875a3c9f616fda918b0e64513`; `w1/dispatch.json` `8f26ea67dd4f98afdcc724886132b0139cb9f2a6371057ca38f43fab231eb689`; `w1/record.json` `5483f5d22af5c5ba720bc453bc93532d64247405b6cbf31c39dbc30907d4b821`; `w2/reports/ScribeWaveAccounting.md` `847fec6f3c77a26cf164adccdec13186f018e9d8442f043630f3c620eee8b172`.

### Low — the tally-check attribution exceeds its registered scope

`LOG.md:1357-1358` attaches `tally-check.py (red 5/5)` to the grouped R19-V2/V4/V5/V6 corrections. The red registry has five stale-claim checks: the 155→154 file count, three stale S096 claims, and ten→nine OM10 occurrences; the green registry has four corrected claims for file count, S096 any-/first-line counts, and OM10 occurrences. It has no R19-V6/25-dead-seats claim, and the R19-V4 fail-open/self-report facts are not checked by that count-only entry. The wave-2 claim list from `jq '{red_ids:[.red[].id],green_ids:[.green[].id]}' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/tally-claims.json` returned those five red IDs and four green IDs, with no V6 entry; `w1/reports/TallyCheck.md:28-35` shows `TALLY_SUMMARY: set=all n=5 match=0 mismatch=5 error=0` / `EXPECT_SUMMARY: 5/5`. The 25 count is documented from the round-19 registry/report join in `corpus/lessons/round-20.md:76-78`, not from this checker. Split the checker-verified numeric claims from the independently sourced V4/V6 corrections.

Hashes: `tally-claims.json` `81eed3ebe33ec0bd2a7adbb5077c51a2624e00bccd945df83477f21674b3a48d`; `w1/reports/TallyCheck.md` `999d561f4784a09ccc7c67c5bd65fa97ad9bfdbc75ead82bc6ca6fa696d5135a`.

### Low — the C2 result omits the scorecard’s explicit qualification

The numeric transition `20/28 → 22/30` in `LOG.md:1354-1356` reproduces: the wave-2 `RerunMeasure` report records `20/28, 7.1429` at `1f7f995` and `e629f73`, then `22/30, 7.3333` at `a4046a8` (`w2/reports/RerunMeasure.md:10-16`). However, the committed SCORECARD states that criterion 30′’s green is **not independent of C1**, and that if closure rules it a target-preserving swap the honest reading is `21/29` (`SCORECARD.md:1307-1309,1331`). The log gives the unqualified headline only. Keep the number, but carry that bounded verdict beside it.

Hash: `w2/reports/RerunMeasure.md` `f45095eb90708e48362f26da7877d6321db8e0a59a9a3dac5846e59623476132`.

## Cross-checks that hold

- Commit labels and sequencing in `LOG.md:1344-1345` resolve correctly: `e629f73` = `e629f731172b8238caffe50f152217ce56535fb4`; `f3da504` = `f3da50488661509ce5d144c90f7780f8088e0903`; `28c6837` = `28c68378eccbd5f227cdc28a62406ff390e3540a`. `4362219e0aaf56601486bdad1df64311e75e12f6` adds the LOG entry; `a4046a8216080d4004de3f268c62cf142095ac07` changes only the round-20 lesson, so the LOG wording is unchanged at tip. `git diff --exit-code f3da504^ f3da504 -- tools/mado-tripwire.py` returned exit 0 (no suite-commit tool change). The current `tools/mado-tripwire.py` SHA-256 is `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`, matching the final recall-split receipt’s tool hash.
- C1 precision values match the committed receipts. Parsing the receipts with `jq -R 'fromjson? | select(.cases != null) | {commit,rev,total:(.cases|length),passed:(.cases|map(select(.pass))|length),families}'` returned `1f7f995`: 29/175; final `28c6837`: 172/175 (P 66/66, S 17/17, W 21/22, H 51/52, L 17/18); pre-harm `9c54c56`: 110/175 and P 66/66. The final precision receipt is pinned to measured commit `28c68378eccbd5f227cdc28a62406ff390e3540a`; its file SHA-256 is `629724dce770aad74a4e268fc36a2061d93fcf5f3c8bd77beee777d61f80e98c`.
- The recall-split final receipt reports 6 incident lines, 5 detected observed + 1 detected lead, and 20 control lines with 0 findings (`recall-split-final.txt:8-21`); its measured commit and tool hash match `28c6837` and the tripwire SHA above. Receipt SHA-256: `5165b72878feec8c67e20a0ab079db0aaaea358258b8a62fbb965dd91a6df0a2`.
- `w2/reports/RerunSuites.md:5-13` records 11 suite runs, 247/247 at the repaired tool, and the eight `r20_edit` cases as the only old-tool expectation changes. This is the peer’s recorded run, not a test run by this reviewer. Report SHA-256: `de7ac9be61bf71cd66f1ca4d7533194df1b0549c7307eefb1c94963609caa3fd`.
- C2’s raw measure result holds numerically (qualified above). The criterion-29 receipts also support the logged fail-closed contrast: the round-19 shape has five fail-open modes and the repaired harness aborts before canary payloads on the six forced setup failures, with the positive control succeeding (`evidence/crit29-inns-r19-shape.txt:3-58`; `evidence/crit29-isolate.txt:3-58`).
- R19-V2’s corrected `8/13` any-line and `6/13` first-line values, R19-V4’s `154`, and R19-V5’s `9/8` are present in the round-20 lesson; the 25-dead-seat value is sourced there separately. SentinelPause20’s wave-1 audit says the inspected seat reports declared no installs; `RevengeRuleBIntent.md:23` also says “No installs.” No contradictory install evidence was found in the sources checked.

## Limits

- This was a read-only LOG/commit/receipt audit. I did not run `tw-precision.py`, `measure.py`, `tally-check.py`, the suites, or the isolation harness; cited rerun outputs are from committed receipts or peer reports.
- The SCORECARD still marks the whole-corpus diff against `9c54c56` as pending (`SCORECARD.md:1330`), so this report does not establish whole-corpus no-harm.
- I did not independently audit L1’s complete command history or every wave-1 report body. The host-command assertion is not disproved by the material checked here; its independent scope remains limited to the cited wave-1 audit.
- No LSP device was mounted; this assignment was a content/history check and required no caller, definition, or diagnostics queries.

## Installs

none