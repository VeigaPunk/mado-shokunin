# R72ExecC1 — independent frozen C1 execution

## Axes and scope
C1 calibration: require matching failure-detail counts for kill credit. C2 operability: summary-based outcome (held prototype observations only; no independent C2 candidate run). No implementation changes. Report is inside the exclusive seat directory; the conflicting shorter trailer suggestion would write outside that directory and was not used.

## Commands, exit codes, and retained evidence
All three requested processes ran concurrently, once, with cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`. Both C1 executions share the requested scratch root but use separate internal work directories. The unmodified drivers assert fixture Git toplevel before their add/commit operations; all fixture writes were under the explicit scratch roots. Each stderr stream was empty. Full stdout is retained below, before scratch deletion.

### measurement

```sh
python3 -I quality/counters/c1-r72-summary-credit.py --repo . --rev 9bcb4fd5b598844f168230dc05e441721d95b272 --base-rev 976684a27e99c2508037a60eec415f550f53d70e --scratch-root /fast/scratch/hyaku/mado-r72/R72ExecC1/run
```

Observed process rc: `0`. Last stdout line:

```text
MADO_R72_SUMMARY_CREDIT: cases=8 correct=8 base_correct=6 verdict=TARGET_MET rev=9bcb4fd5b598844f168230dc05e441721d95b272
```

Full stdout:

```text
MADO_R72_REVS rev=9bcb4fd5b598844f168230dc05e441721d95b272 base=976684a27e99c2508037a60eec415f550f53d70e
MADO_R72_HARNESS role=candidate path=quality/counters/c1-r72-landing-controls.py present=yes sha256=d0d3bfd2b8306062e7ea7323377dea1371df93c4a9447a7a28c4927becfe7c62
MADO_R72_HARNESS role=base path=quality/counters/c1-r71-landing-controls.py sha256=f836499594fb4fa8898336b1a47241614bb2b9ddb6f93c369a9e00ece0f185f1
MADO_R72_FIXTURE mode=liar-success rev=c5cc58bfd84ba0bb140f4d80cdf5ca171b1a834d lane_sha256=817f313249e932077667dd11f739fbe0d1eda228e984c2393ab1598e2f5425f2
MADO_R72_FIXTURE mode=stderr-genuine rev=3ff58791c30ecc88fd706aba4155555d073dc036 lane_sha256=f219cc8a5d39c6404e253599ae3b99a3092b0ec7ada0910445712564783695db
MADO_R72_FIXTURE mode=liar-kill rev=492e056f417a1b2717634787271cdb387580c3af lane_sha256=e3ffaa941c1bf3d7126d98f60a4847ce26905d7ea41e0f0c750ffd9ba9bae2ec
MADO_R72_FIXTURE mode=crash-stderr rev=78aeaf2b463f39550a6939e8bd5df325e782cbc5 lane_sha256=2e0215ab80ac41ed82bc2fd2fd7c0a479bed8bb4aa547128a66f0ca912895ab0
MADO_R72_FIXTURE mode=bare-failing rev=fa1235f95a5f6be2ac59069a836784b05144f0fc lane_sha256=4872102952c2300ee5ae670e1eec30eec2aae64163a3cc935f0733350826d49f
MADO_R72_FIXTURE mode=mismatch-detail rev=3a04e92a4e4468bbd2f05a48a3ab7ab4804a14ac lane_sha256=a30d47040bc3bdf9289306528db44682d1afe64240a4a5053e3c68325ddd84fc
MADO_R72_FIXTURE mode=last-wins-pass rev=befa9af42ad574a7ad0ea9d17404d36ed30a891b lane_sha256=540a191b01c31b06e060ce8b3593196cc6cb73b596108c7bf13182493b18cce9
MADO_R72_FIXTURE mode=last-wins-fail rev=557246aab5a0d980ef012ddf838d598cbde2d84e lane_sha256=1804c47797cfce51ce21a2c2f9bf27b47253f2dacf80c1367801d7e7c79b587a
MADO_R72_SCENARIO mode=liar-success expect_mz=pass candidate_mz=pass base_mz=pass correct=yes base_correct=yes rev=c5cc58bfd84ba0bb140f4d80cdf5ca171b1a834d
MADO_R72_SCENARIO mode=stderr-genuine expect_mz=pass candidate_mz=pass base_mz=pass correct=yes base_correct=yes rev=3ff58791c30ecc88fd706aba4155555d073dc036
MADO_R72_SCENARIO mode=liar-kill expect_mz=fail candidate_mz=fail base_mz=fail correct=yes base_correct=yes rev=492e056f417a1b2717634787271cdb387580c3af
MADO_R72_SCENARIO mode=crash-stderr expect_mz=fail candidate_mz=fail base_mz=fail correct=yes base_correct=yes rev=78aeaf2b463f39550a6939e8bd5df325e782cbc5
MADO_R72_SCENARIO mode=bare-failing expect_mz=fail candidate_mz=fail base_mz=pass correct=yes base_correct=no rev=fa1235f95a5f6be2ac59069a836784b05144f0fc
MADO_R72_SCENARIO mode=mismatch-detail expect_mz=fail candidate_mz=fail base_mz=pass correct=yes base_correct=no rev=3a04e92a4e4468bbd2f05a48a3ab7ab4804a14ac
MADO_R72_SCENARIO mode=last-wins-pass expect_mz=fail candidate_mz=fail base_mz=fail correct=yes base_correct=yes rev=befa9af42ad574a7ad0ea9d17404d36ed30a891b
MADO_R72_SCENARIO mode=last-wins-fail expect_mz=pass candidate_mz=pass base_mz=pass correct=yes base_correct=yes rev=557246aab5a0d980ef012ddf838d598cbde2d84e
MADO_R72_SUMMARY_CREDIT: cases=8 correct=8 base_correct=6 verdict=TARGET_MET rev=9bcb4fd5b598844f168230dc05e441721d95b272
```

Stderr: empty.

### selftest

```sh
python3 -I quality/counters/c1-r72-summary-credit.py --selftest --scratch-root /fast/scratch/hyaku/mado-r72/R72ExecC1/run
```

Observed process rc: `0`. Last stdout line:

```text
MADO_R72_SUMMARY_CREDIT_SELFTEST: 33/33 assertions passed
```

Full stdout:

```text
MADO_R72_SUMMARY_CREDIT_SELFTEST: 33/33 assertions passed
```

Stderr: empty.

### prototype

```sh
python3 -I .ufo/waves/round-72/proto/held-lanes-r72.py --repo . --rev 976684a27e99c2508037a60eec415f550f53d70e --scratch-root /fast/scratch/hyaku/mado-r72/R72ExecC1/proto
```

Observed process rc: `0`. Last stdout line:

```text
PROTO_R72_SUMMARY c1_modes=8 c2_cases=8 c2_held_correct=4
```

Full stdout:

```text
PROTO_R72_REV rev=976684a27e99c2508037a60eec415f550f53d70e harness=quality/counters/c1-r71-landing-controls.py harness_sha256=f836499594fb4fa8898336b1a47241614bb2b9ddb6f93c369a9e00ece0f185f1
PROTO_R72_C1 mode=liar-success expect_mz=pass held_mz=pass correct_for_held=yes rev=af46382c4f8b315d52c5bb0cf52252ccf8e01ce0
PROTO_R72_C1 mode=stderr-genuine expect_mz=pass held_mz=pass correct_for_held=yes rev=de084537aef4e0c2cf9af1f60a577f2ba59202b1
PROTO_R72_C1 mode=liar-kill expect_mz=fail held_mz=fail correct_for_held=yes rev=e39f27a2207ac8ad3e918c78c1c7718313ee9c11
PROTO_R72_C1 mode=crash-stderr expect_mz=fail held_mz=fail correct_for_held=yes rev=a0f5562a89c4333d068da2476615c8ae4ffa71cd
PROTO_R72_C1 mode=bare-failing expect_mz=fail held_mz=pass correct_for_held=NO rev=28e355ba5d53198f176a2d300d48996e17f26979
PROTO_R72_C1 mode=mismatch-detail expect_mz=fail held_mz=pass correct_for_held=NO rev=0a865cb1bdadb7624f01d6458efcc45a079fb143
PROTO_R72_C1 mode=last-wins-pass expect_mz=fail held_mz=fail correct_for_held=yes rev=10adfaf5d1a52a3d8346da4d95dc1c53799e634e
PROTO_R72_C1 mode=last-wins-fail expect_mz=pass held_mz=pass correct_for_held=yes rev=47cda207c0c76b13be6f314346859b33811603f6
PROTO_R72_C2 case=green-summary-exit0 expect=TARGET_MET held=TARGET_MET held_correct=yes
PROTO_R72_C2 case=failing-summary-exit0 expect=TARGET_MISSED held=TARGET_MET held_correct=NO
PROTO_R72_C2 case=green-summary-exit2 expect=TARGET_MET held=TARGET_MISSED held_correct=NO
PROTO_R72_C2 case=no-summary-exit0 expect=TARGET_MISSED held=TARGET_MET held_correct=NO
PROTO_R72_C2 case=garbled-summary-exit0 expect=TARGET_MISSED held=TARGET_MET held_correct=NO
PROTO_R72_C2 case=failing-summary-exit2 expect=TARGET_MISSED held=TARGET_MISSED held_correct=yes
PROTO_R72_C2 case=no-summary-exit2 expect=TARGET_MISSED held=TARGET_MISSED held_correct=yes
PROTO_R72_C2 case=green-summary-killed1 expect=TARGET_MISSED held=TARGET_MISSED held_correct=yes
PROTO_R72_SUMMARY c1_modes=8 c2_cases=8 c2_held_correct=4
```

Stderr: empty.

## Reconciliation with frozen receipts
Re-read `measurement-c1-r72.txt`, `control-baseline-c1-r72.txt`, and the two C2 receipts, without rewriting them. The eight C1 modes, truth labels, candidate decisions, and held decisions agree exactly with the committed receipts:

| Mode | Expected M-Z | Candidate | Held (both runs) | Held correct |
|---|---|---|---|---|
| liar-success | pass | pass | pass | yes |
| stderr-genuine | pass | pass | pass | yes |
| liar-kill | fail | fail | fail | yes |
| crash-stderr | fail | fail | fail | yes |
| bare-failing | fail | fail | pass | no |
| mismatch-detail | fail | fail | pass | no |
| last-wins-pass | fail | fail | fail | yes |
| last-wins-fail | pass | pass | pass | yes |

Candidate 8/8; same-run base 6/8; held-only prototype C1 6/8. Only `bare-failing` and `mismatch-detail` distinguish candidate from held. M-Z `pass` in these output fields denotes credited kill, not a passing child assertion suite.

Differences and reporting distinctions:
- All eight ephemeral fixture `rev=` values changed from the measurement receipt, in both its fixture rows and corresponding scenario rows. All eight prototype C1 fixture `rev=` values likewise changed from the baseline receipt. The complete new values are retained above. These scratch commit identities are not the scored revision. [INFERENCE] New fixture commit timestamps explain their changing identities; the drivers generate commits rather than fixing commit dates.
- Every measurement fixture `lane_sha256` matches the committed measurement receipt. Candidate and base harness SHA256 values also match, as do scored revision and base revision. No other measurement stdout fields differ.
- The committed measurement receipt adds `C1_RC=0` after the program's contract line. The actual program's last line is the frozen `MADO_R72_SUMMARY_CREDIT` contract, and the observed process rc is 0. There is no rc/contract disagreement.
- `control-baseline-c1-r72.txt` contains only the prototype header and eight C1 rows, no process rc or prototype final summary. The full independently captured prototype also emits eight C2 rows and `PROTO_R72_SUMMARY c1_modes=8 c2_cases=8 c2_held_correct=4`. Its C2 rows agree with `control-baseline-c2-r72.txt`: held 4/8, with the same four incorrect cases. Prototype rc 0 means successful diagnostic execution, not all controls correct; its source unconditionally returns 0 after reporting. No target-verdict contract is emitted by this prototype. The original baseline process rc is not evidenced by either split baseline receipt.
- Counter selftest reports 33/33 and rc 0. Neither of the two C1 frozen receipts contains a selftest result, so this is additional observed evidence, not a claim of byte-for-byte selftest receipt reproduction.

## What credit() does and does not authenticate
`quality/counters/c1-r72-landing-controls.py:298–344` takes the last line beginning exactly `MADO_LANDING_COUNTERS_SELFTEST:`, strips its surrounding whitespace, requires the complete summary grammar with nonnegative decimal integers, requires `n > 0` and `p < n`, then requires exactly `n-p` lines whose text begins `SELFTEST FAIL` anywhere in the supplied output. Thus it checks report syntax and arithmetic consistency, not authenticity: it does not verify assertion identities, detail grammar, unique failures, execution provenance, timestamps, or that reported assertions actually ran. Replaying or fabricating both a failing summary and matching prefix-counted detail lines still earns credit. The caller at lines 500–507 supplies decoded stdout followed by decoded stderr, so both streams count but their original temporal interleaving is not retained; the function itself receives only one string and does not inspect exit status. It selects the last prefix-bearing summary line, not the last valid parsed summary: a later malformed prefix-bearing summary prevents credit even if an earlier valid one fails. Failure lines are counted over the whole combined capture, not scoped to the segment associated with the selected summary.

## Risks, blockers, and posture
No blocker to the assigned executions; no production edits or tool installs. This is finite fixture evidence, not whole-system fault coverage or authentication. Original split-baseline rc is unavailable in those receipts; current prototype rc is directly observed. LSP definitions/references were unavailable: no LSP route is exposed in this seat, so source inspection used the read tool. No additional build, lint, formatter, or integration gate was run. Scratch is deleted after retaining this report.

## Self-evaluation
Accuracy 4/5: raw outputs and rc retained; original split-baseline rc remains unevidenced. Completeness 5/5: three requested runs, receipt reconciliation, and credit limits included. Clarity 4/5: full receipts lengthen the report but keep evidence local. Actionability 5/5: exact commands and discrepancies are explicit. Conciseness 4/5: full stdout is deliberately retained for reproducibility. Overall 4.4/5. Improvements: future receipt producers should retain prototype rc with the unsplit final summary; preserve a selftest receipt alongside measurement evidence. Self-check: the report distinguishes observed results from inference and should support the L1's reconciliation without another run.
