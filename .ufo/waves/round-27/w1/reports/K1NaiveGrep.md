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

## v2 re-score
CONTROL K1NaiveGrep v2 best: PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED — not met

L1 retired C1 counter v1 before data after a separate source-blind control met its target. The original v1 results above remain historical evidence, not the active claim. As requested, re-scored this control without changing any of its bytes under the amended frozen v2 counter, which adds decoys, nested/glob sources, interleaved source order, variable redefinition, and type-strict canonical-JSON comparison.

Ran this exact command twice concurrently from `/home/vgpnk/Projects/shokunin/mado-shokunin`; the counter independently generated two fresh seeds:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v2.py a4dc0da0 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NaiveGrep.py --jobs 6
```

| Verbatim stdout receipt | Fresh seed | Result | Exit |
| --- | --- | --- | --- |
| `.ufo/waves/round-27/controls/v2/K1NaiveGrep-seed1.txt` | `1e38009652d8ff46` | `PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |
| `.ufo/waves/round-27/controls/v2/K1NaiveGrep-seed2.txt` | `7d0a534e821b6298` | `PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |

Both runs resolved REV to `a4dc0da0394a71badf506e9c72144cd1b8ca7281`, confirmed duplicate BASE oracle equality with zero rules, and confirmed oracle commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`. Both used the same 79-file snapshot digest recorded above. BASE passed and every generated case failed in each run. Both receipts finish:

```text
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED
exit=1
```

Thus v2 rejected the unchanged NAIVE-GREP control on both seeds; neither run was inconclusive or exited 2, so no guard retry was needed. No target-meeting-control redesign rule was triggered by this control.

Before-and-after SHA-256 evidence for the re-score:

| Path | SHA-256 before and after |
| --- | --- |
| `.ufo/waves/round-27/c1/count-v2.py` | `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87` |
| `.ufo/waves/round-27/harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |
| `.ufo/waves/round-27/controls/K1NaiveGrep.py` | `f26dfb60602b57297fba5c4e5b1153dd22964f2b1cb7fee33a2539f77550e611` |

Receipt hashes:

- v2 seed1: `c772fb9d7417521d9c05f0d1be35ee17f62186bab063bb4cbd3e65f3f22c25e5`
- v2 seed2: `482d64343fb0404330d14b68c3237452a9516a95c39035fce6d79f0229d50739`

Exact re-score hash commands:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 10 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c1/count-v2.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/controls/K1NaiveGrep.py
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 10 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c1/count-v2.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/controls/K1NaiveGrep.py .ufo/waves/round-27/controls/v2/K1NaiveGrep-seed1.txt .ufo/waves/round-27/controls/v2/K1NaiveGrep-seed2.txt
```

The same bounded `df -h /fast` command recorded above reported 86% used and 113G available before this re-score. The same independent bounded coredump-count command reported `1338` before and after (delta 0), matching both v2 receipts. Both counter processes completed; all nested compositor execution and cleanup remained in the pinned oracle. The control, counter, and oracle were unchanged, so restoration was unnecessary. Only the two authorized v2 receipt files and this appended report section were written for the follow-up. No tools were installed or updated.

## v3 re-score
CONTROL K1NaiveGrep v3 best: PRED-C1-r27-v3 cases_pass=2/41 verdict=TARGET_MISSED — not met

L1 retired v2 before data after a separate `$wsr`-prefix-keyed reader met its target. The v2 receipts above remain historical evidence. As requested, re-scored the unchanged NAIVE-GREP control under v3, which replaces fixed variable-name prefixes with random names while retaining v2's other behavior.

Ran this exact command twice concurrently from `/home/vgpnk/Projects/shokunin/mado-shokunin`, allowing the counter to draw two fresh seeds:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v3.py 9f5fc28b --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NaiveGrep.py --jobs 6
```

| Verbatim stdout receipt | Fresh seed | PRED line | Exit |
| --- | --- | --- | --- |
| `.ufo/waves/round-27/controls/v3/K1NaiveGrep-seed1.txt` | `30688c62b8e855e5` | `PRED-C1-r27-v3 cases_pass=2/41 verdict=TARGET_MISSED` | 1 |
| `.ufo/waves/round-27/controls/v3/K1NaiveGrep-seed2.txt` | `8f384c40777b4ea2` | `PRED-C1-r27-v3 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |

Both runs resolved REV to `9f5fc28b3db8d06870d0314818ffbe5e43bb5937`, confirmed duplicate BASE oracle equality with zero rules, and confirmed oracle commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`. The 79-file snapshot digest was unchanged. Seed1 passed BASE and this generated case:

```text
CASE C22   PASS rules=3 oracle_rules=3 (APPEND:DECOY+GAPSHORT)
```

Its remaining 39 generated cases failed. Seed2 passed only BASE, with all 40 generated cases failing. Neither run exited 2 or was inconclusive; no guard retry was needed. Both rejected this control against the 41/41 target, so it did not trigger the target-meeting-control redesign rule.

Before-and-after SHA-256 evidence:

| Path | SHA-256 before and after |
| --- | --- |
| `.ufo/waves/round-27/c1/count-v3.py` | `ee4cea19c11a1a8160115f4754e88c11c58aac9a3bff40ccfd16920cd1d691bd` |
| `.ufo/waves/round-27/harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |
| `.ufo/waves/round-27/controls/K1NaiveGrep.py` | `f26dfb60602b57297fba5c4e5b1153dd22964f2b1cb7fee33a2539f77550e611` |

Receipt SHA-256 values:

- v3 seed1: `603c41088a3e6bc49b6b4f10e77f46ce7cf857a176f3c3306a477cb267b0f95e`
- v3 seed2: `4cb1850e7a3d7628307e2925c8d5ebdc91d8c4e5ef27a4494d659181211828c3`

Exact hash commands:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 10 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c1/count-v3.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/controls/K1NaiveGrep.py
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 10 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c1/count-v3.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/controls/K1NaiveGrep.py .ufo/waves/round-27/controls/v3/K1NaiveGrep-seed1.txt .ufo/waves/round-27/controls/v3/K1NaiveGrep-seed2.txt
```

The bounded scratch-capacity command recorded above reported `/fast` 89% used, 94G available before the v3 runs. The independent bounded coredump-count command recorded above reported `1338` both before and after (delta 0). Both receipts independently contain `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0` and end in `exit=1`.

Both bounded counter processes completed using the pinned oracle for compositor isolation and cleanup. The control and frozen inputs were unchanged; no restoration was necessary. Only the two authorized v3 receipts and this report append were written for this follow-up. No tools were installed or updated.

## v4 re-score
CONTROL K1NaiveGrep v4 best: PRED-C1-r27-v4 cases_pass=2/41 verdict=TARGET_MISSED — not met

L1 retired v3 before data after separate GlobalOnce and FileScope partial readers met its target. The earlier receipts remain historical evidence. Re-scored this control without changing its bytes under frozen v4, which adds value-embedded variables, definitions in sourced files, use before definition, and repeated sourcing with a conflicting rule between visits.

Ran this exact command twice concurrently from `/home/vgpnk/Projects/shokunin/mado-shokunin`, using the requested reduced `--jobs 4` and independent fresh seeds drawn by the counter:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NaiveGrep.py --jobs 4
```

| Verbatim stdout receipt | Fresh seed | PRED line | Exit |
| --- | --- | --- | --- |
| `.ufo/waves/round-27/controls/v4/K1NaiveGrep-seed1.txt` | `8181b2b3d7e653d2` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |
| `.ufo/waves/round-27/controls/v4/K1NaiveGrep-seed2.txt` | `43e44544cc382be0` | `PRED-C1-r27-v4 cases_pass=2/41 verdict=TARGET_MISSED` | 1 |

Both resolved REV to `2fdca5caaab6859386effbb8fa6acc5250c90633`, confirmed duplicate BASE oracle equality with zero rules, and confirmed oracle commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`. Both used the unchanged 79-file snapshot digest recorded above. Seed1 passed only BASE and failed all 40 generated cases. Seed2 passed BASE and this generated case, failing the remaining 39:

```text
CASE C16   PASS rules=3 oracle_rules=3 (APPEND:GAPSHORT+ONEMPTY)
```

Both runs rejected the unchanged NAIVE-GREP control against the 41/41 target. Neither was inconclusive or exited 2, so no guard retry was required. This control did not trigger the target-meeting-control redesign rule.

Before-and-after SHA-256 evidence:

| Path | SHA-256 before and after |
| --- | --- |
| `.ufo/waves/round-27/c1/count-v4.py` | `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1` |
| `.ufo/waves/round-27/harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |
| `.ufo/waves/round-27/controls/K1NaiveGrep.py` | `f26dfb60602b57297fba5c4e5b1153dd22964f2b1cb7fee33a2539f77550e611` |

Receipt SHA-256 values:

- v4 seed1: `d91a32e8643f1154e97ffc8c3a997f0f62a5f30a449af300dcab825af6b31b8a`
- v4 seed2: `5922aae35cfba03c77fb6a953ed59cfc6ec38b06b92e468ef14590bdd3434f36`

Exact hash commands:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 10 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c1/count-v4.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/controls/K1NaiveGrep.py
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 10 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c1/count-v4.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/controls/K1NaiveGrep.py .ufo/waves/round-27/controls/v4/K1NaiveGrep-seed1.txt .ufo/waves/round-27/controls/v4/K1NaiveGrep-seed2.txt
```

The same bounded scratch-capacity command recorded above reported `/fast` 90% used, 84G available before the v4 runs. The same independent bounded coredump-count command recorded above reported `1338` before and after (delta 0). Both v4 receipts contain `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0` and end in `exit=1`.

Both bounded counter processes completed using the pinned oracle's compositor isolation and cleanup. The control and frozen inputs remained unchanged, so restoration was unnecessary. Only the authorized v4 receipts and this report append were written for this follow-up. No tools were installed or updated.

