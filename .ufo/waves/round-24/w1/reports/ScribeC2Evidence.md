# Round 24 wave 1 — C2 evidence (draft)

## Behavior and findings

C2 is calibration: align the SCORECARD capability assessment with observations from the frozen counter. The do-nothing control already exists, so I read its receipt rather than rerunning `c2/count.py`. The frozen baseline has one mismatch, `tripwire evidence marker` (stated `works`, observed `fails`), at both the base and control tip. This is a valid C2 experiment under registration: the do-nothing control does not meet the zero-mismatch target. This report's capability table is only a draft; it was not scored, and it does not claim C2's target was met.

The control receipt's exact base run command was:

```sh
timeout --kill-after=30s 900s prlimit --as=4294967296 --core=0 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE MADO_LANE=/fast/scratch/hyaku/mado-r24/ctl/CtlC2DoNothing python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c2/count.py 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122
```

The control receipt records `mismatches=1/12 revision=8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`, counter exit 1, and the sole mismatch as `tripwire evidence marker`. It also records the same 1/12 mismatch at unchanged control tip `4f21d9956e8c7a5d9f824ff24b9a4426a3f51949`. The frozen counter and manifest hashes in that receipt are respectively `sha256:a280950195d647b0be992122a14cc96535e6de24a8bc40d92683351af7ffe4e8` and `sha256:e02c76d1adb4f523fccf11e1e5ad4cd40f6d0da460b75c7f811b66306e188a02`.

### Capability status (round 24 re-demonstration)

Draft from the do-nothing base run's observed values. Each evidence cell gives the recorded summary line and revision; status reflects `observed`, not the prior `stated` assessment.

| capability | status | observed evidence |
|---|---|---|
| sources registry | observed=works | `sources registry stated=works observed=works OK exit=0`; revision `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` |
| verdict gate (live + file plane) | observed=works | `verdict gate (live + file plane) stated=works observed=works OK exit=0`; revision `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` |
| hermetic self-test | observed=works | `hermetic self-test stated=works observed=works OK exit=0`; revision `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` |
| mutation regression with re-cut | observed=works | `mutation regression with re-cut stated=works observed=works OK exit=0`; revision `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` |
| post-hoc transcript tripwire | observed=works | `post-hoc transcript tripwire stated=works observed=works OK exit=0`; revision `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` |
| tripwire frozen replay (gate entry) | observed=works | `tripwire frozen replay (gate entry) stated=works observed=works OK exit=1`; revision `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` |
| landedness check | observed=works | `landedness check stated=works observed=works OK exit=1`; revision `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` |
| tripwire evidence marker | observed=fails | `tripwire evidence marker stated=works observed=fails MISMATCH exit=0`; revision `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` |
| harness fail-closed check | observed=works | `harness fail-closed check stated=works observed=works OK exit=0`; revision `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` |
| tripwire reached-body sweep | observed=works | `tripwire reached-body sweep stated=works observed=works OK exit=0`; revision `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` |
| detector removal-side guard | observed=works | `detector removal-side guard stated=works observed=works OK exit=0`; revision `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` |
| artifact-only assessment integrity | observed=works | `artifact-only assessment integrity stated=works observed=works OK exit=0`; revision `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122` |

## H2 precision comparison

I ran these requested commands from the lane working tree; both returned the counter's JSON result:

```sh
timeout 600 python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/tw-precision.py 8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122
timeout 600 python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/tw-precision.py 28c6837
```

- Base `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`: 166/175; P 66/66, S 17/17, W 21/22, H 47/52, L 15/18; score 9.4857.
- Dated `28c6837` (counter identifies commit `28c68378eccbd5f227cdc28a62406ff390e3540a`): 172/175; P 66/66, S 17/17, W 21/22, H 51/52, L 17/18; score 9.8286.

The two L cases that pass in the dated run but fail at the base are:

- `L-CasePureCrossCell-reset-clears-helper`: dated pass, with `package_query` / `lead` at line 3; base fail, no findings.
- `L-CaseLeadsInvisible-reset-cleared-helper`: dated pass, with `package_query` / `lead` at line 2; base fail, no findings.

`L-AdoptW2-AdvHelperFn-b14` fails in both runs, so it is not one of the two changed cases. The SCORECARD round-21 history attributes the added H2 disagreements to reset-invalidated helper leads and the strict commit/index-write boundary; the round-23 registration says H2 was not repaired and identifies reset-cleared lead adjudication plus the round-21 strict index-write boundary. The observed L cases above are the reset-cleared-helper part of that history; the strict index-write boundary describes the separate H cases. Round 24's base retains this round-21 H2 state.

## Gates, touched surfaces, and limits

- C2 target: `mismatches=0`. Recorded do-nothing result: `1/12`; target not met by the control, so C2 remains valid. No round-24 data table run is claimed here.
- Commands run by me were the two read-only precision-counter commands above. I did not rerun C2 because `CtlC2DoNothing.md` already contains the base and tip runs and their complete outputs.
- Only this scoped report is written; no product code, SCORECARD, control, or counter files were edited. No package/tool installation, lane or fleet git/jj write, host mutation, compositor action, service operation, or `hyprctl` command was performed.
- No unresolved conflict between the scoped counter outputs and the cited SCORECARD/registration H2 account was observed. The case-level causal attribution is limited to the documented reset-cleared lead adjudication; no broader repair or admission is claimed.

## Artifact paths

- Report: `.ufo/waves/round-24/w1/reports/ScribeC2Evidence.md`
- Frozen C2 control receipt: `.ufo/waves/round-24/controls/CtlC2DoNothing.md`
- Precision counter output for base: `artifact://20619`
- Precision counter output for `28c6837`: `artifact://20620`
- Context read: `.ufo/waves/round-24/registration.md`; `.ufo/waves/round-23/registration.md:15-24`; `SCORECARD.md:1340-1343,1454-1458,1532-1535`

**Verdict:** C2's recorded do-nothing baseline is 1/12, with `tripwire evidence marker` the sole mismatch; the 12-row table above is a draft based on observed values only. H2 remains at 166/175 on the base; relative to `28c6837`, two reset-cleared L cases changed from passing to failing, consistent with the documented round-21 H2 history.
