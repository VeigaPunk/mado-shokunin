# K1NoVariables — fresh-seed v4 re-score

RESCORE K1NoVariables best: PRED-C1-r27-v4 cases_pass=6/41 verdict=TARGET_MISSED — not met

## Assignment and detector

Re-scored the committed NO-VARIABLES control twice, unchanged, at revision `2fdca5caaab6859386effbb8fa6acc5250c90633`. Its deliberate defect is to ignore variable assignments and leave `$name` references literal, while following sources and merging selectors. The expected detector is counter v4's type-strict, ordered JSON comparison with the isolated Hyprland v0.56.2 oracle. This assignment was a re-score, not a new pristine/mutated/restored implementation experiment.

Axes: fidelity to the registered shape, non-variable behavior, fresh-seed reproducibility, and host safety.

## Actual fresh-seed outputs

| Run | Seed | PRED line | Exit | Complete stdout receipt |
| --- | --- | --- | --- | --- |
| 1 | `dd2f9c3debeec693` | `PRED-C1-r27-v4 cases_pass=6/41 verdict=TARGET_MISSED` | 1 | `/fast/scratch/hyaku/mado-r27/rescore/K1NoVariables-fresh-seed1.txt` |
| 2 | `ba03e01d8d5cb1ab` | `PRED-C1-r27-v4 cases_pass=6/41 verdict=TARGET_MISSED` | 1 | `/fast/scratch/hyaku/mado-r27/rescore/K1NoVariables-fresh-seed2.txt` |

Verbatim PRED output, in run order:

```text
PRED-C1-r27-v4 cases_pass=6/41 verdict=TARGET_MISSED
PRED-C1-r27-v4 cases_pass=6/41 verdict=TARGET_MISSED
```

Both runs passed the two-run BASE oracle stability check, verified nested Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`, and passed the control's BASE case. Both used the same 79-file snapshot, SHA-256 `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`. Neither returned guard exit 2. Each rejected 35 cases; the control did not meet the registered target or trigger the target-meeting kill rule. These are control rejections, not a claimed causal mutation kill backed by an unrun pristine implementation.

## Comparison with committed receipts

The request calls the supplied `controls/v4/` files “v3 receipts,” but their own headers and PRED lines identify counter **v4**. Compared both those files and the actual `controls/v3/` receipts, without changing them:

| Receipt | Seed | Actual PRED line |
| --- | --- | --- |
| `controls/v3/K1NoVariables-seed1.txt` | `32b6552f33f29d4d` | `PRED-C1-r27-v3 cases_pass=8/41 verdict=TARGET_MISSED` |
| `controls/v3/K1NoVariables-seed2.txt` | `9cbc9111ba1de2aa` | `PRED-C1-r27-v3 cases_pass=10/41 verdict=TARGET_MISSED` |
| `controls/v4/K1NoVariables-seed1.txt` | `a925bfbf44d81d7a` | `PRED-C1-r27-v4 cases_pass=7/41 verdict=TARGET_MISSED` |
| `controls/v4/K1NoVariables-seed2.txt` | `5488cc34a3a8e0be` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` |

All four historical receipts identify the same control hash as the fresh runs. The two fresh v4 results, 6/41 and 6/41, fall between the committed v4 scores of 1/41 and 7/41. Every recorded measurement misses 41/41. Different seeds and the v3-to-v4 population redesign prevent treating score differences as a paired causal estimate.

## Strength within the shape

**Assessment: no stronger same-shape variant identified; retain the existing control as the strongest evidenced candidate, not a proved global maximum.**

Reviewed the complete control, the v4 generator, both supplied v4 receipts, and both fresh outputs. Across all four v4 receipts, every case with none of `VARIABLE`, `VARREDEF`, or `USEBEFOREDEF` passes. A negative-lookahead search for a FAIL line lacking all three tags returned no matches. The existing implementation already follows nested and glob sources at their encounter position, revisits a file after a completed include, preserves selector insertion order while merging, and handles the generated non-variable fields and shorthand.

Fresh run 1's six passes are BASE and C02/C06/C13/C17/C35; fresh run 2 passes BASE and C16/C18/C23/C32/C39. Run 2 C39 carries `VARIABLE` yet passes, so a variable feature tag alone is not proof that omission must affect the final table.

[INFERENCE] The measured shortfall is consistent with the defining variable omission, rather than an exposed independent non-variable weakness. Adding a variable table, recovering assignment values, or expanding references would leave the registered shape. No concrete behavior-preserving-within-shape strengthening was found, so no speculative stronger variant was written or scored. The feature-tag evidence does not establish parser completeness or global optimality outside this population.

## Exact measurement commands

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Before measurement, cleared host display/signature variables, checked scratch capacity, created the receipt directory, and hashed the control and counter. Executed the assigned counter command twice without `--seed`, preserving stdout through `tee` with pipeline exit propagation:

```sh
unset WAYLAND_DISPLAY HYPRLAND_INSTANCE_SIGNATURE
set -o pipefail
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NoVariables.py --jobs 6 | tee /fast/scratch/hyaku/mado-r27/rescore/K1NoVariables-fresh-seed1.txt
```

```sh
unset WAYLAND_DISPLAY HYPRLAND_INSTANCE_SIGNATURE
set -o pipefail
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NoVariables.py --jobs 6 | tee /fast/scratch/hyaku/mado-r27/rescore/K1NoVariables-fresh-seed2.txt
```

The initial asynchronous launch request was rejected by the tool with `Background job limit reached (100). Wait for running jobs to finish or cancel one.` Retrying through a non-asynchronous tool call produced the first completed measurement. This tool rejection was not a detector run or a counter guard failure. The two completed commands exited 1 after approximately 32 and 154 seconds respectively; runs were sequential.

## Hashes and preservation evidence

Control and counter hashes were captured before the first run and again after both runs; both remained identical:

```text
65672716b17daf24f7a4f7d69ab4b922cc47066c2d02e5cdd0586423e3cc0b44  .ufo/waves/round-27/controls/K1NoVariables.py
635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1  .ufo/waves/round-27/c1/count-v4.py
```

Both counter receipts identify and enforce the pinned oracle hash; the final hash command also returned:

```text
0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601  .ufo/waves/round-27/harness/oracle.py
```

Fresh receipt SHA-256 values:

```text
db8ab654cd6c991594194628b179dcea4b8fb43115430ed4cf2e156ce762d164  /fast/scratch/hyaku/mado-r27/rescore/K1NoVariables-fresh-seed1.txt
1b924b2e504974be8191d322cab8da63b02c863638b6177851ab5439d923330a  /fast/scratch/hyaku/mado-r27/rescore/K1NoVariables-fresh-seed2.txt
```

Hash command, after clearing display/signature variables:

```sh
timeout 20 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/controls/K1NoVariables.py .ufo/waves/round-27/c1/count-v4.py .ufo/waves/round-27/harness/oracle.py /fast/scratch/hyaku/mado-r27/rescore/K1NoVariables-fresh-seed1.txt /fast/scratch/hyaku/mado-r27/rescore/K1NoVariables-fresh-seed2.txt
```

No control, counter, harness, sibling source, or historical receipt was edited. Exact control preservation therefore required no restoration; no pristine/mutated/restored cycle is claimed. Only the two fresh stdout receipts and this scoped report were retained.

## Host safety and scope

Before scratch writes:

```sh
unset WAYLAND_DISPLAY HYPRLAND_INSTANCE_SIGNATURE
timeout 20 prlimit --as=4000000000 -- df -h /fast
```

Actual output:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  731G   73G  91% /fast
```

Before the first run and after both completed runs, executed:

```sh
unset WAYLAND_DISPLAY HYPRLAND_INSTANCE_SIGNATURE
timeout 20 prlimit --as=4000000000 -- coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland
```

Both outputs were `1338`: seat-observed delta **0**. Each counter receipt independently prints:

```text
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
```

All nested compositor startup and teardown stayed within the frozen oracle, whose shared file locks cap host-wide oracle instances at twelve. Both counter processes completed; no independent long-lived process was started. No live compositor command, unsafe config input, network request, git/jj write, subagent dispatch, other runtime, installation, build, test suite, lint, or formatter was invoked. The only behavioral checks were the two explicitly assigned counter measurements.
