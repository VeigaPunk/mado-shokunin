# K1Echo — PRE-DATA C1 control

## Verdict
CONTROL K1Echo best: PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED — not met

Both fresh-seed runs returned exit 1. Each passed only BASE, whose oracle table was empty, and failed all 25 APPEND and 15 SYNTH cases. No exit-2 guard occurred; no retry was needed. This is a control result, not a killed-mutant claim from a pristine/mutated/restored probe.

## Control and expected detector

Axes: ECHO shape fidelity, exact-oracle discrimination, host safety.

Created `.ufo/waves/round-27/controls/K1Echo.py`, a single Python stdlib file accepting `--home DIR`. It opens only `DIR/.config/hypr/hyprland.conf`, matches an assignment whose stripped key is exactly `workspace`, and emits one object per matching line in encounter order: `workspaceString` is the first comma field after `=`, stripped; `enabled` is always true. These are its only output fields. It does not merge selectors, follow sources, expand variables, or interpret rule fields. Whitespace around the assignment is accepted.

The frozen C1 detector compares complete ordered JSON arrays against the pinned isolated Hyprland oracle, requiring 41/41. The deliberate shortcut is omission of all rule semantics beyond the root selector echo.

## Commands and observed output

Working directory for commands: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Executed this exact scoring command twice concurrently; the counter selected two fresh seeds:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count.py 5ddc5885 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1Echo.py --jobs 6
```

Both subprocesses also received only PATH and HOME in their initial environment. Each ran in a separate process group, with a 925-second parent deadline; the wrapper's `finally` attempted `os.killpg(pid, signal.SIGKILL)`, ignoring an already-absent group.

| Run | Seed | BASE | APPEND | SYNTH | Process exit | Verbatim stdout receipt |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `1907c6a1d9f5e040` | 1/1 | 0/25 | 0/15 | 1 | `.ufo/waves/round-27/controls/K1Echo-seed1.txt` |
| 2 | `beebd329dfade698` | 1/1 | 0/25 | 0/15 | 1 | `.ufo/waves/round-27/controls/K1Echo-seed2.txt` |

Both receipts end verbatim:

```text
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED
exit=1
```

Both runs had empty stderr. Both confirmed equal duplicate BASE oracle results (`rules=0`), Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`, and snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727` over 79 files. Resolved revision: `5ddc5885188a1de8606464526d636c9e2fc433e6`.

Before execution:

```sh
env -i PATH=/usr/bin timeout 15 prlimit --as=4000000000 -- df -h /fast
```

Reported 804G total, 689G used, 115G available, 86% used.

Before and after execution:

```sh
env -i PATH=/usr/bin timeout 20 prlimit --as=4000000000 -- coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland
```

Both counts were `1338`; observed delta was zero. Hyprland was started only by the frozen counter through its pinned oracle; no live compositor commands were issued.

## Hashes and restoration evidence

Before scoring:

```sh
env -i PATH=/usr/bin timeout 15 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/controls/K1Echo.py .ufo/waves/round-27/c1/count.py .ufo/waves/round-27/harness/oracle.py
```

After scoring:

```sh
env -i PATH=/usr/bin timeout 15 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/controls/K1Echo.py .ufo/waves/round-27/c1/count.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/controls/K1Echo-seed1.txt .ufo/waves/round-27/controls/K1Echo-seed2.txt
```

Before and after SHA-256 values were identical for:

- Control: `093aa876dca8081acd1c3a88a0d17475f8510cfaa105d9be57ab12f6a8b9fedd`.
- Frozen C1 counter: `3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136`.
- Oracle: `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`.

Receipt SHA-256 values:

- Seed 1: `f261156f9593be06284316a9994e0b3005631619c6f5701623773b5d58d27e0a`.
- Seed 2: `0754e44135334ff5c960e0034689a79e6d0c90a985b20ac4b8e091bde45f6cdc`.

No pristine subject bytes were mutated, so no source restoration was necessary. Only this seat's control, two receipts, and this report were written; the control remains as the required deliverable. No git/jj writes, subagents, tool installations, or upgrades were performed.

## C1 v2 re-score
CONTROL K1Echo v2 best: PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED — not met

At L1's request, re-scored the unchanged ECHO control after retirement of v1. No control bytes were edited. The v2 detector retains the 41/41 target and adds source-order/glob/nesting/decoy and variable-redefinition cases plus type-strict JSON equality.

Working directory remained `/home/vgpnk/Projects/shokunin/mado-shokunin`. Executed this exact command twice concurrently with fresh counter-selected seeds:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v2.py a4dc0da0 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1Echo.py --jobs 6
```

| Run | Seed | BASE | APPEND | SYNTH | Process exit | Verbatim stdout receipt |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `ef8547bc424a0772` | 1/1 | 0/25 | 0/15 | 1 | `.ufo/waves/round-27/controls/v2/K1Echo-seed1.txt` |
| 2 | `eff4ef7fdcf80a37` | 1/1 | 0/25 | 0/15 | 1 | `.ufo/waves/round-27/controls/v2/K1Echo-seed2.txt` |

Both runs had empty stderr, no exit-2 guard, and these verbatim final lines:

```text
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED
exit=1
```

Resolved revision: `a4dc0da0394a71badf506e9c72144cd1b8ca7281`. Both runs confirmed equal duplicate BASE oracle results (`rules=0`), the pinned Hyprland v0.56.2 commit, and the same 79-file snapshot digest as v1. No retry was necessary.

Repeated the storage and coredump commands documented above. Before re-scoring, `/fast` had 113G available (691G used, 86%). Independent before/after Hyprland coredump counts were both `1338`, delta zero. Both processes used a cleared initial environment, separate process groups, a 925-second parent deadline, and the same process-group cleanup in `finally`. No live compositor commands were issued.

Before re-scoring:

```sh
env -i PATH=/usr/bin timeout 15 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/controls/K1Echo.py .ufo/waves/round-27/c1/count-v2.py .ufo/waves/round-27/harness/oracle.py
```

After re-scoring:

```sh
env -i PATH=/usr/bin timeout 15 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/controls/K1Echo.py .ufo/waves/round-27/c1/count-v2.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/controls/v2/K1Echo-seed1.txt .ufo/waves/round-27/controls/v2/K1Echo-seed2.txt
```

Before/after SHA-256 values were identical:

- Unchanged ECHO control: `093aa876dca8081acd1c3a88a0d17475f8510cfaa105d9be57ab12f6a8b9fedd`.
- Frozen v2 counter: `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87`.
- Oracle: `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`.

New receipt SHA-256 values:

- v2 seed 1: `319b31eb0f803478ac012fc0aa234dbfe2f7ba62368e8eb91883e411bbeee824`.
- v2 seed 2: `11928ff2385c8af6839e9777732b19c9acdc029e63bcea5822c29149ff61557f`.

Restoration was unnecessary: no control, subject, counter, or oracle bytes were modified. This follow-up wrote only the two requested v2 receipts and appended this section. No tools were installed or upgraded, no subagents were dispatched, and no git/jj write commands were run.
