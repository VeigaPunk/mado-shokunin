# K2DoNothing — C2 pre-data control

## Verdict
CONTROL K2DoNothing best: PRED-C2-r27 green=0/8 w_killed=0/15 h_killed=0/0 h_need=0 h_valid=0 h_invalid=0 verdict=TARGET_MISSED — not met

Both fresh-seed runs returned this same PRED line and `exit=1`. Neither run returned exit 2, so no guard-error rerun was required. This control did not trigger the redesign rule.

## Shape and detector

The assigned DO-NOTHING shape was preserved: no suite file was created or supplied. The frozen C2 counter ran at `5ddc5885188a1de8606464526d636c9e2fc433e6` without suite overrides or a held-out directory. Both receipts report:

```text
SUITE A quality/counter-selftest.py MISSING at REV
SUITE B quality/population-suite.py MISSING at REV
```

Axes: fidelity to the missing-suite shape, reproducibility across fresh seeds, and host safety. No subject implementation, counter, harness, W set, or sibling-owned file was edited. Only the two assigned receipts and this report were written in the lane.

Expected detector: the frozen counter documents that absent suites fail every green run and kill nothing (`c2/count.py:18-20`). Actual output matched: all 8 green cases were `rc=None FAIL`, and all 15 valid W cases were `rc=None SURVIVED`, each identifying the missing suite. No suite process ran. H was not supplied or read; these measurements do not assess held-out detection.

There is no claimed killed mutant. Since the pristine green cases also fail, these results cannot establish a behavioral mutant kill; they establish the prescribed negative-control result.

## Exact scoring commands and receipts

Both commands used working directory `/home/vgpnk/Projects/shokunin/mado-shokunin`. Seeds were independently generated with Python's `secrets.token_hex(8)`. The two invocations ran concurrently, each with six counter jobs.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --seed 86dac744665f6659 --jobs 6
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --seed bb3ebe735ba8aae3 --jobs 6
```

| Run | Verbatim stdout receipt, including `exit=1` | Command exit | Wall time |
| --- | --- | --- | --- |
| Seed 1 | `.ufo/waves/round-27/controls/K2DoNothing-seed1.txt` | 1 | 9.26 s |
| Seed 2 | `.ufo/waves/round-27/controls/K2DoNothing-seed2.txt` | 1 | 9.17 s |

Each receipt is 3675 bytes and contains the counter, W-set and pristine-subject hashes, missing-suite declarations, every case result, and the complete PRED line.

## Input hashes and restoration evidence

Before and after scoring, this exact command produced identical output:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/c2/count.py .ufo/waves/round-27/c2/mutants-w.json
```

```text
2e180ed29c31abcb3421d7e57a147d05ac9d2982ebe4dbc555747b287e754dc7  .ufo/waves/round-27/c2/count.py
0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608  .ufo/waves/round-27/c2/mutants-w.json
```

Both receipts also report identical pristine subject hashes:

- `.ufo/waves/round-26/c1/count-v2.py`: `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428`
- `.ufo/waves/round-26/c2/count.py`: `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8`
- `.ufo/waves/round-26/quality/check-population.py`: `803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64`

Restoration is not applicable: no suite bytes existed at the measured revision, and no manual mutation was made. The counter's missing-suite return precedes applying scratch-subject edits (`c2/count.py:78-81`); it cleans its temporary clones in `finally`. No additional pristine/mutated/restored probe was substituted for the assigned two-run control.

## Host safety and tooling

Scratch capacity was checked before the counter runs:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 -- df -h /fast
```

Output: `/fast` had 115G available, 86% used. No large persistent scratch artifact was created by this seat.

Coredump listing commands, before and after respectively:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 -- coredumpctl list --no-pager --no-legend
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
```

Both commands exited 0. Counts of captured output lines containing `/usr/bin/Hyprland` were computed in Python:

```text
HOST_SAFETY Hyprland_coredumps before=1338 after=1338 delta=0
```

No Hyprland, oracle, live-compositor command, or long-lived service was started by this seat. Both bounded counter process trees finished; counter-owned git children are synchronous. All launched commands used cleared environments without WAYLAND_DISPLAY or HYPRLAND_INSTANCE_SIGNATURE. No lane/fleet git or jj write command was issued; only counter-owned sandbox clones were used. No tool was installed or updated. No build, lint, formatter, or unrelated verification was run.
