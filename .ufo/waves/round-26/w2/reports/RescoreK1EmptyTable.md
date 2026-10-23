# RescoreK1EmptyTable — C1 counter v2

Seat: `MadoR26.RescoreK1EmptyTable`, round 26 wave w2, leaf member.

RESCORE K1EmptyTable not met (best 0/41)

## Scope and method

Axes: detector evidence, fidelity to the registered control shape, reproducibility, and host safety.

Re-scored the unchanged committed `controls/K1EmptyTable.py` twice, with fresh seeds, using the frozen C1 v2 counter at REV `1b0b91e9889cbf984b052f5de564db78330a72aa`. Then scored one scratch-only strengthening with another fresh seed. The L1's previous v2 receipt (`controls/v2/K1EmptyTable.txt:49-51`) was 0/41, exit 1; both new re-scores agree.

The detector requires exact equality of both animation-node and bezier sets across BASE, 20 APPEND, 10 EDIT, and 10 SYNTH cases; target 41/41 (`registration.md:137-144`, `c1/count-v2.py:22-24,308-322,358-374`). No counter or oracle bytes were changed. No seed was supplied; the counter generated each from `os.urandom(8)` (`c1/count-v2.py:301`).

## Actual receipts

Full command-plus-stdout transcripts, including every CASE line and `exit=`, are retained under:

`/fast/scratch/hyaku/mado-r26/rescore/RescoreK1EmptyTable/`

| Run | File | Fresh seed | PRED line | Printed exit / command exit |
|---|---|---|---|---|
| Unchanged A, first | `baseline-1.txt` | `9878f79081923a2b` | `PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED` | 1 / 1 |
| Unchanged A, second | `baseline-2.txt` | `7f198a6797f97fec` | `PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED` | 1 / 1 |
| Strengthened B | `strengthened.txt` | `8f73a5676d98e628` | `PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED` | 1 / 1 |

All three runs printed:

```text
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26-v2 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

No exit-2 guard or counter timeout occurred. An initial asynchronous request for the second run was rejected by the tool's 100-background-job limit before execution; the subsequent launch completed and produced `baseline-2.txt`. Exactly three counter executions completed for this assignment.

## Strengthening within the shape

Scratch file:

`/fast/scratch/hyaku/mado-r26/rescore/RescoreK1EmptyTable/K1EmptyTableZeroNodes.py`

SHA-256: `1a29b08a151c42818442b346d2d7cb318843dc213cf641707effae0ee410dde3`.

Behavioral change relative to A: replace the empty node list with 35 named zero/default-value nodes; retain the empty bezier list. Each node has `overridden=false`, `bezier=""`, `enabled=true`, `speed=0.0`, and `style=""`. This deliberately reuses w1's already-explored variant B, not a new shortcut or a change to the shape (`w1/reports/K1EmptyTable.md:13-26`; constants and construction from `controls/K1EmptyTableZeroNodes.py:18-34`). The scratch script opens no config files, reads no environment, and copies no nonzero oracle table values. Its only CLI input is the required, ignored `--home` argument.

Expected detector: C1 v2 should still reject the answer because neither the config-derived overrides nor any bezier entries are produced. Actual BASE diagnostic:

```text
CASE BASE  FAIL nodes missing=19 extra=19 beziers missing=6 extra=0 changed=base (unperturbed)
```

The strengthened run's node mismatches were 8–22 missing and equally many extra; its bezier misses were 3–8 with zero extras. All 41 cases failed. The two unchanged-A runs each missed all 35 nodes in every case; bezier misses were respectively 3–7 and 3–8. Adding the zero nodes reduces some missing tuples but does not improve the case score.

This is a negative-control re-score, not a checker-mutant kill. If interpreted as an invariant-mutation probe, a kill verdict would be inconclusive because the original baseline already returns TARGET_MISSED; no killed-mutant claim is made. The supported re-score verdict is that neither the unchanged control nor this within-shape strengthening met the frozen target.

## Exact commands

Working directory for every command below:

`/home/vgpnk/Projects/shokunin/mado-shokunin`

The following scoring command ran twice; the two executions overlapped, each with one oracle worker:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I -B .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file .ufo/waves/round-26/controls/K1EmptyTable.py --jobs 1
```

After both completed, the strengthening ran once:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I -B .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK1EmptyTable/K1EmptyTableZeroNodes.py --jobs 1
```

Capacity and hash commands:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 df -h /fast
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 sha256sum .ufo/waves/round-26/controls/K1EmptyTable.py .ufo/waves/round-26/controls/K1EmptyTableZeroNodes.py .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/harness/oracle.py
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 sha256sum /fast/scratch/hyaku/mado-r26/rescore/RescoreK1EmptyTable/K1EmptyTableZeroNodes.py
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 sha256sum .ufo/waves/round-26/controls/K1EmptyTable.py .ufo/waves/round-26/controls/K1EmptyTableZeroNodes.py .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/harness/oracle.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK1EmptyTable/K1EmptyTableZeroNodes.py
```

The capacity check reported `/fast`: 804G total, 658G used, 146G available, 82% used. The scratch script and receipts were created with the file-write tool, not by changing lane controls.

## Byte preservation and host safety

SHA-256 before and after all scoring was identical for every original input:

| Original file, relative to `.ufo/waves/round-26/` | Before = after SHA-256 |
|---|---|
| `controls/K1EmptyTable.py` | `1dd7006992e8d5d0d3a98832c408fb28d1590d5440f7a8af2033caa41009d4b5` |
| `controls/K1EmptyTableZeroNodes.py` | `3ce6d3240c3d6c31e837859f7a8dfb49f8c569c0282c6f46373ceec1f22fa0ba` |
| `c1/count-v2.py` | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` |
| `harness/oracle.py` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` |

Restoration evidence is byte preservation: no original file was mutated, so no restore was necessary. The strengthening exists only as a separate new scratch file; its pre-score and post-score hashes also match the hash above.

Only this assigned report was written in the lane. No git/jj write command, subagent dispatch, runtime invocation, tool installation, or host-service operation was performed. Hyprland was started only by the frozen counter's oracle, with inherited desktop identifiers removed from the counter launches. The oracle uses shared slot locks and cleans up each sandbox process group in `finally` (`harness/oracle.py:109-125,212-226`); all three counter commands have returned. No independent live-compositor command was issued. The observed coredump delta was zero in every receipt.

These three scores do not establish anything about untested control shapes or data-seat tools. No blockers remain for this scoped re-score.
