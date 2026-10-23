# K1RootOnly — fresh-seed counter-v4 rescore

RESCORE K1RootOnly best: PRED-C1-r27-v4 cases_pass=4/41 verdict=TARGET_MISSED — not met

## Scope and detector

Axes: root-local semantic fidelity, strict source omission, reproducible fresh-seed measurement, and host safety. Read `skill://godspeed`, the frozen registration, the committed control, counter-v4 generation/comparison code, oracle slot/cleanup code, and the prior receipts/report. No subagents, production changes, package installs, or other runtime were invoked.

The assigned control's deliberate defect is omission of every `source =` target. Its single config read is the root `HOME/.config/hypr/hyprland.conf`; source directives are skipped before argument expansion. Root-local variables/redefinitions, embedded substitution, ordered field-wise merges, gap shorthand, booleans, comments, continuations, and command rewriting remain implemented. Expected detector: the unchanged pinned counter compares the entire ordered JSON array, type-strictly, against isolated Hyprland v0.56.2; the target is 41/41.

## Exact commands and actual outputs

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Executed the requested command twice concurrently, each without `--seed`, saving stdout verbatim with `tee`:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1RootOnly.py --jobs 6 | /usr/bin/tee /fast/scratch/hyaku/mado-r27/rescore/K1RootOnly-v4-fresh-seed1.txt
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1RootOnly.py --jobs 6 | /usr/bin/tee /fast/scratch/hyaku/mado-r27/rescore/K1RootOnly-v4-fresh-seed2.txt
```

Initial requests to run these as asynchronous bash jobs were refused with `Background job limit reached (100)`; those requests did not execute the detector. Both successful calls used non-asynchronous bash execution. No guard failure or detector retry followed.

| Run | Fresh seed | Exact predicate line | Counter's terminal line | Wall time |
| --- | --- | --- | --- | --- |
| 1 | `70ed61f5b7ee3b1d` | `PRED-C1-r27-v4 cases_pass=3/41 verdict=TARGET_MISSED` | `exit=1` | 167.35 s |
| 2 | `b74791bf503f4d27` | `PRED-C1-r27-v4 cases_pass=4/41 verdict=TARGET_MISSED` | `exit=1` | 151.88 s |

The counter-reported status is recorded above; the outer pipeline ends in `tee` and does not independently preserve the counter's process status. No stderr diagnostics appeared. Both receipts passed repeated-BASE stability and oracle-version guards, resolved revision `2fdca5caaab6859386effbb8fa6acc5250c90633`, and recorded 79 snapshot files with digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`. The oracle reported commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`.

Receipt SHA-256:

- `/fast/scratch/hyaku/mado-r27/rescore/K1RootOnly-v4-fresh-seed1.txt`: `d93094d4537638ac4a18617ea0b64a26c1eaac116d97e8fd58ecb8953ced3afa`.
- `/fast/scratch/hyaku/mado-r27/rescore/K1RootOnly-v4-fresh-seed2.txt`: `1a2605c59a16c41681443b86e3bcbf8e8f02a32a939bb85b4e63b0849a81d2ea`.

## Comparison with committed receipts

The assignment calls the `controls/v4/K1RootOnly-seed*.txt` files “v3 receipts”, but their headers and predicate labels identify counter **v4**. I compared those exact named files and also the actual v3 receipts under `controls/v3/`.

| Receipt set | Seeds | Exact predicate lines |
| --- | --- | --- |
| Actual committed v3 | `d251182b055cf307`, `3baf9ef184c7bf09` | `PRED-C1-r27-v3 cases_pass=3/41 verdict=TARGET_MISSED` (both) |
| Named committed v4 | `e825b5546cbce3dc` | `PRED-C1-r27-v4 cases_pass=2/41 verdict=TARGET_MISSED` |
| Named committed v4 | `46b396d0210888e4` | `PRED-C1-r27-v4 cases_pass=4/41 verdict=TARGET_MISSED` |
| Fresh v4, this seat | `70ed61f5b7ee3b1d` | `PRED-C1-r27-v4 cases_pass=3/41 verdict=TARGET_MISSED` |
| Fresh v4, this seat | `b74791bf503f4d27` | `PRED-C1-r27-v4 cases_pass=4/41 verdict=TARGET_MISSED` |

All six receipts identify the same control SHA-256 and snapshot digest. Fresh v4 results remain in the committed v4 range and tie its best, 4/41. Different seeds and counter versions are not paired measurements of a regression.

## Is this the strongest version of its shape?

For the exercised counter surface, the committed control is the strongest evidenced ROOT-ONLY variant available here: no concrete, honest within-shape strengthening was identified, and no stronger file was created or scored. This is a scoped assessment, not a proof of optimality over every root-only algorithm or full hyprlang parity.

Evidence: in the two fresh receipts, all five generated cases with none of `NEWSRC`, `SOURCED`, `SRCDEF`, or `TWICE` passed, as did both BASE cases. Fresh run 1 passed BASE/C24/C28; run 2 passed BASE/C08/C26/C32. Across the two actual v3, two committed v4, and two fresh v4 receipts, every such generated case passed: 12/12, plus all six BASE runs. Every failing case carries at least one source-dependent feature. One committed-v4 case with `SRCDEF` also passed incidentally. Receipt feature membership is not a separate diagnosis of each differing field.

The root-local code already handles the v4 additions that do not require sourced bytes: value-embedded variables and position-sensitive use-before-definition. Missing sourced workspace records, sourced definitions, and the final repeated-source overwrite cannot be recovered generally from the root bytes without abandoning ROOT-ONLY. Inferring them from counter labels, random-name patterns, or memorized snapshot contents would not be a semantic strengthening. No justified score-improving root-local repair emerged from the bounded strengthening review.

This is rejection of the assigned partial-reader control, not a pristine/mutated/restored full-parser experiment. No pristine passing implementation was supplied or run, so I do **not** claim a killed mutant or a general coverage proof.

## Byte integrity, restoration, and host safety

Before and after both completed detector runs, bounded clean-environment `sha256sum` calls returned identical hashes:

| File | Before = after SHA-256 |
| --- | --- |
| `controls/K1RootOnly.py` | `bf9a86af4f5f34679d77a47d19ba67614a1715c2b6d74df175469fee20b3544a` |
| `c1/count-v4.py` | `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1` |
| `harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

No subject bytes were edited; exact restoration was therefore unnecessary. Lane writes were limited to this assigned report; scratch writes were the two named receipts and the counter's self-removed scratch. No git/jj write command was used.

Before scoring, `df -h /fast` reported 73G available, 91% used. Independent bounded clean-environment counts using `coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland` were 1338 before and 1338 after, delta 0. Both counter receipts independently printed:

```text
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
```

Only the pinned counter/oracle launched nested Hyprland. Its host-wide 12-slot locks bounded concurrency; its process-group cleanup and scratch removal ran before both commands returned. No live-compositor commands, card-node access, inherited compositor environment, persistent service, or separate Hyprland launch was used. No additional build, lint, integration, or behavioral check was run.
