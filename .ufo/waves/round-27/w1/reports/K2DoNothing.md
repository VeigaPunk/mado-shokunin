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

## C2 v2 rescore — L1 follow-up

CONTROL K2DoNothing v2 best: PRED-C2-r27-v2 green=0/8 b_valid=0 w_killed=0/15 h_killed=0/0 h_need=0 h_valid=0 h_min_per_subject=0 invalid=0 verdict=TARGET_MISSED — not met

The L1 retired C2 v1 before data and requested this rescore under the hardened counter. The earlier receipts above remain historical evidence. The DO-NOTHING control was unchanged: no suite file was authored, copied, or supplied. Both suites were missing at the newly assigned revision `a4dc0da0394a71badf506e9c72144cd1b8ca7281`.

### Commands and actual output

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Two fresh seeds were independently generated with `secrets.token_hex(8)`. The bounded commands ran concurrently:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count-v2.py a4dc0da0 --seed 812fc7f54b78da35 --jobs 6
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count-v2.py a4dc0da0 --seed ce5da8b869d87d78 --jobs 6
```

| Run | Verbatim stdout receipt, including `exit=1` | Command exit | Wall time |
| --- | --- | --- | --- |
| V2 seed 1 | `.ufo/waves/round-27/controls/v2/K2DoNothing-seed1.txt` | 1 | 270.99 s |
| V2 seed 2 | `.ufo/waves/round-27/controls/v2/K2DoNothing-seed2.txt` | 1 | 271.05 s |

Each receipt is 3709 bytes. Both report the PRED line above, both suites `MISSING at REV`, all 8 green cases `rc=None FAIL`, and all 15 W cases `rc=None SURVIVED`. Neither invocation returned exit 2; no guard-error rerun was required. No held-out directory or seal was supplied or read, so `b_valid=0` and `h_valid=0` do not assess the sealed population.

Expected detector: the v2 missing-suite contract fails every green and kills nothing (`c2/count-v2.py:27-30`). The observed result matches it. Because the missing-suite guard returns before scratch-subject edits and the bubblewrap invocation (`:88-105`), this control exercises the missing-suite path, not the suite sandbox. No behavioral mutant kill is claimed: pristine green cases also fail.

### V2 hashes, restoration and safety

This command was run before and after both scores, with identical output:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/c2/count-v2.py .ufo/waves/round-27/c2/mutants-w.json
```

```text
4dfb34b5551a908aa7fd56e75526417b43659018c47fa5993ad39a72b6b109d3  .ufo/waves/round-27/c2/count-v2.py
0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608  .ufo/waves/round-27/c2/mutants-w.json
```

The pristine subject hashes in both v2 receipts match those listed in the v1 section. No counter, W set, harness, subject, or control bytes were modified. Suite hashes and byte restoration are not applicable because the control consists of absent suites; no manual mutation was performed.

Capacity check before scoring:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 --core=0 -- df -h /fast
```

Output: `/fast` had 112G available, 87% used. Coredump counts were collected before and after using:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
```

Both listings exited 0 with empty stderr. Python counted lines containing `/usr/bin/Hyprland`:

```text
HOST_SAFETY v2 Hyprland_coredumps before=1338 after=1338 delta=0
```

Both bounded counter invocations finished. No suite process, Hyprland, oracle, live-compositor command, or long-lived service was started by this seat. All command environments were cleared. No lane/fleet git or jj write command was issued; git writes were counter-owned no-local scratch clones. No tools were installed or updated, and no unrelated checks were run.
