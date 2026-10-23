# K1RootOnly — C1 ROOT-ONLY control

## Verdict
CONTROL K1RootOnly best: PRED-C1-r27 cases_pass=10/41 verdict=TARGET_MISSED — not met

The source-omission control did not meet the frozen 41/41 target under either fresh seed. This is a rejected control, not a claim that a pristine full-parser implementation passed a mutation test.

## Work and boundary

Axes: root-local semantic fidelity, strict source omission, reproducible measurement, and host safety.

Created only the authorized stdlib control `.ufo/waves/round-27/controls/K1RootOnly.py`, its two stdout receipts, and this report. The control reads `.config/hypr/hyprland.conf` once beneath `--home`; it never opens, resolves, globs, traverses or otherwise reads a `source =` target. No snapshot table, case labels, fixture-specific values, subprocesses, or oracle access are embedded in the control.

Implemented ordered, field-wise merges by exact selector; one-to-four-value CSS gaps; boolean words and integer forms; root variable definitions/redefinitions and longest-name-first expansion; comments and escaped hashes; line continuation; `defaultName`; and `on-created-empty` workspace-command rewriting for numeric, named, special and static-pattern selectors. Layout options are parsed but not serialized, matching the exposed JSON shape. Root conditionals and simple variable arithmetic are also handled. The implementation does not claim complete hyprlang parity outside the exercised counter surface.

The deliberate defect is omission of sourced rules and definitions. Every generated case without a `NEWSRC` or `SOURCED` receipt tag passed: 2/2 in seed 1 and 8/8 in seed 2. Both BASE cases passed with the oracle's empty table. One source-bearing case also passed (seed 2 C35); equality there does not imply source traversal. The remaining 69 source-bearing cases failed exact table equality. These are observations from receipt tags, not an assertion that each failure's individual field difference was separately diagnosed.

## Detector and commands

Read the frozen registration and `skill://godspeed` before implementation, and `/home/vgpnk/.omp/agent/RULES.md` before any potential installation. No installation or upgrade was necessary; the control uses only Python's standard library.

Primary implementation references were read from pinned raw sources:

- `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp`, workspace handler at lines 1682–1793.
- `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp`, JSON fields at lines 528–554 and ordered table at lines 619–636.
- `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/workspace/WorkspaceRuleManager.cpp` and `WorkspaceRule.cpp`, lookup and merge behavior.
- `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp`, CSS gap expansion.
- `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/parserUtils/ParserUtils.cpp`, integer and boolean parsing.
- `https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp`, variable and line parsing, particularly lines 675–832.

Also inspected the existing cached helper source `/fast/scratch/hyaku/mado-r26/data/ExecAnimToolB/src/MiscFunctions.cpp:478-512` for command rewriting and the pinned hyprutils 0.14.2 `VarList2.cpp` for delimiter escaping. An attempted raw `src/config/shared/complex/ComplexDataTypes.cpp` fetch returned HTTP 404; the implementation is in the successfully opened header, not that unopened path.

The bounded behavioral detector was the unmodified frozen C1 counter, exact ordered-list equality against isolated Hyprland v0.56.2. From `/home/vgpnk/Projects/shokunin/mado-shokunin`, executed this exact command twice concurrently through `asyncio.create_subprocess_exec`, each with a clean parent environment containing only `PATH=/usr/bin`:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count.py 5ddc5885 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1RootOnly.py --jobs 6
```

The counter supplied the two fresh random seeds and enforced its own memory and oracle-slot limits. Each stdout byte stream was saved without modification through the write tool; stderr was empty for both runs. Both processes completed normally with return code 1; neither returned guard code 2, so no guard retry was required.

| Run | Fresh seed | Actual predicate output | Exit | Receipt | Elapsed |
| --- | --- | --- | --- | --- | --- |
| 1 | `31293effa2aa1684` | `PRED-C1-r27 cases_pass=3/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/K1RootOnly-seed1.txt` | 25.238 s |
| 2 | `81f4f8c207fc37cd` | `PRED-C1-r27 cases_pass=10/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/K1RootOnly-seed2.txt` | 23.658 s |

Both receipts confirm stable repeated BASE results, the exact pinned Hyprland commit and tag, and identical snapshot inputs: 79 files, digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`.

## Byte integrity and restoration evidence

No frozen subject, counter, harness, W set, or sibling file was modified. The control is an authorized persistent output, not an in-place mutation requiring restoration. SHA-256 was recorded before and after both detector runs:

| File | Before and after SHA-256 |
| --- | --- |
| `.ufo/waves/round-27/controls/K1RootOnly.py` (11,101 bytes) | `bf9a86af4f5f34679d77a47d19ba67614a1715c2b6d74df175469fee20b3544a` |
| `.ufo/waves/round-27/c1/count.py` | `3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136` |
| `.ufo/waves/round-27/harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

Receipt SHA-256:

- Seed 1: `9279fa6977ea9da6be32dca2555b20a2311babb2ffdf3506a761a737da756ab7`.
- Seed 2: `84da8341721b121795e6f37b483a63d2352ddcbebb0c3ec175702358be994ff6`.

Hash commands were bounded, clean-environment `sha256sum` invocations over the named files; no git/jj write commands were invoked.

## Host safety

Before scoring, bounded `df -h /fast` reported 115G available (86% used). Before and after the runs, the prescribed `coredumpctl list --no-pager --no-legend` count of `/usr/bin/Hyprland` entries was 1338: delta 0. Each counter independently printed:

```text
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
```

Only the frozen counter launched nested compositors, through its pinned isolated oracle. No live-compositor command, card node, service restart, package transaction, inherited compositor environment, or independent Hyprland launch was used. The two awaited counter processes exited; their oracle calls ran the harness's process-group cleanup. No persistent service was started.

No additional build, lint, test suite, mutation probe, or integration run was performed. No lane production parser or next-wave suite was created.
