# K1NaiveGrep — C1 NAIVE-GREP control

## Verdict
CONTROL K1NaiveGrep best: PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED — not met

Both fresh-seed runs exited 1. Each passed only BASE (the unperturbed table was empty), with all 25 APPEND and 15 SYNTH cases failing ordered JSON equality. The detector rejected this control in both runs; neither run was inconclusive or exited 2. This control therefore does not trigger the registration's target-meeting-control redesign rule.

## Control and expected detector

Created only the assigned stdlib implementation, `.ufo/waves/round-27/controls/K1NaiveGrep.py`, plus its two requested receipts and this report. Axes: shape fidelity, strongest line-local key mapping, reproducible detector evidence, and host safety.

The CLI is `python3 -I K1NaiveGrep.py --home DIR`. It opens only `DIR/.config/hypr/hyprland.conf`, processes each physical line independently with regexes, and appends one object per matching `workspace =` line in encounter order. It never follows `source =`, expands `$variables`, or merges repeated workspace selectors. Boolean fields accept only literal `true` and `false`; other boolean spellings are ignored. Line-local mapping includes the printed camel-case keys, integer border sizes, CSS gap expansion, comments, and best-effort on-created-empty workspace-command formatting. Layout/layoutopt/animation fields are not printed because the pinned JSON formatter omits them.

The expected detector is the frozen round-27 C1 counter: Hyprland v0.56.2 oracle output versus exact ordered JSON-list equality over BASE + 25 APPEND + 15 SYNTH, target 41/41. This was a separately retained control, not a mutation of a pristine implementation; no pristine/mutated/restored subject cycle was applicable.

Mapping references read from the pinned Hyprland commit:

- [HyprCtl.cpp:523–550](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp): output keys and omitted optional fields.
- [ConfigManager.cpp:1676–1792](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp): workspace key mappings.
- [ComplexDataTypes.hpp:82–128](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp): gap expansion.
- [MiscFunctions.cpp:478–510](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp): command workspace-prefix formatting.

## Exact scoring command

Working directory for both invocations: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Ran this identical command twice, concurrently; omitting `--seed` made the frozen counter draw a fresh seed independently for each run:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count.py 5ddc5885 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NaiveGrep.py --jobs 6
```

| Receipt | Fresh seed | Result | Process exit |
| --- | --- | --- | --- |
| `.ufo/waves/round-27/controls/K1NaiveGrep-seed1.txt` | `e6329cb4f0c249d5` | `PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |
| `.ufo/waves/round-27/controls/K1NaiveGrep-seed2.txt` | `22a04c1ec6f06d33` | `PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |

Receipts contain stdout verbatim through `exit=1`. Both resolved REV to `5ddc5885188a1de8606464526d636c9e2fc433e6`, observed 79 snapshot files with digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, confirmed duplicate BASE oracle output equality, and reported oracle commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`.

Representative direct outputs:

```text
# seed e6329cb4f0c249d5
CASE C27   FAIL rules got=3 want=2 first_diff=0 oracle_rules=2 (SYNTH:MERGE)
CASE C32   FAIL rules got=1 want=2 first_diff=1 oracle_rules=2 (SYNTH:COMMENT+NEWSRC)
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED
exit=1

# seed 22a04c1ec6f06d33
CASE C26   FAIL rules got=0 want=3 first_diff=0 oracle_rules=3 (SYNTH:BOOLWORD+NEWSRC+ONEMPTY)
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED
exit=1
```

## Hashes and restoration evidence

The assigned control output did not exist before creation. Its SHA-256 was identical in both counter receipts and in the final hash command:

`f26dfb60602b57297fba5c4e5b1153dd22964f2b1cb7fee33a2539f77550e611`.

Frozen inputs were hashed before scoring and again afterward, with identical results:

| Path | Before and after SHA-256 |
| --- | --- |
| `.ufo/waves/round-27/c1/count.py` | `3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136` |
| `.ufo/waves/round-27/harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

Receipt SHA-256 values:

- seed1: `e734a7ee51d3c77c1af549dbdf61faed3a85d4c1e3f6d6c938c681e68d53d2b1`
- seed2: `4b8430eb281c890c963955b4ee55194d15a2bdcb96096cc50f5f777836b1f256`

Hash commands, run in the same working directory:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 10 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c1/count.py .ufo/waves/round-27/harness/oracle.py
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 10 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c1/count.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/controls/K1NaiveGrep.py .ufo/waves/round-27/controls/K1NaiveGrep-seed1.txt .ufo/waves/round-27/controls/K1NaiveGrep-seed2.txt
```

No existing lane subject, counter, oracle, W set, sibling file, or host config was edited. The new control and receipts are intentionally retained under the control contract, so no original subject bytes required restoration. Both bounded counter processes completed, using the oracle's process-group cleanup and temporary-tree cleanup paths; no independent compositor was started.

## Host safety and tooling

Before scoring, this command reported `/fast` at 86% used, 115G available:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 prlimit --as=4000000000 -- df -h /fast
```

This exact independent coredump command was run before and after scoring; both outputs were `1338` (delta 0), agreeing with each receipt:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 -- coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland
```

All Hyprland execution was through the frozen counter/oracle, with cleared environments, private headless isolation, and the shared oracle slot cap. No live-compositor commands, host service changes, package transactions, or git/jj writes were performed. No tools were installed or updated. No checks beyond the assigned two scoring runs and safety/hash evidence were run.
