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

## C1 v2 rescore — unchanged control

CONTROL K1RootOnly v2 best: PRED-C1-r27-v2 cases_pass=6/41 verdict=TARGET_MISSED — not met

The L1 retired counter v1 before data after a different source-blind control met its target. The preceding v1 results are historical; these v2 results are the requested replacement measurement. The control was not changed.

Executed twice concurrently from the lane directory, with two fresh counter-generated seeds and clean parent environments containing only `PATH=/usr/bin`:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v2.py a4dc0da0 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1RootOnly.py --jobs 6
```

Both runs used resolved revision `a4dc0da0394a71badf506e9c72144cd1b8ca7281`. Complete stdout, including `exit=1`, was saved verbatim; stderr was empty for each run. Neither run returned guard code 2, so no retry was needed.

| Run | Fresh seed | Actual predicate output | Exit | Receipt | Elapsed |
| --- | --- | --- | --- | --- | --- |
| 1 | `9df3af3bfd5be2b4` | `PRED-C1-r27-v2 cases_pass=3/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/v2/K1RootOnly-seed1.txt` | 112.303 s |
| 2 | `adfc3f6d1b155195` | `PRED-C1-r27-v2 cases_pass=6/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/v2/K1RootOnly-seed2.txt` | 100.509 s |

Passing cases were BASE, C07 and C26 in run 1; BASE, C01, C05, C14, C16 and C19 in run 2. Both receipts confirm stable repeated BASE results, the pinned Hyprland commit, and the same 79-file snapshot digest as v1. The source-omission control remains rejected; no full-parser pristine/mutated/restored experiment is implied.

Before and after rescore SHA-256 values were identical:

- Control: `bf9a86af4f5f34679d77a47d19ba67614a1715c2b6d74df175469fee20b3544a` — also identical to both v1 runs.
- Counter v2: `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87`, matching the L1 follow-up pin.
- Oracle: `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`.

Receipt SHA-256:

- v2 seed 1: `8a5f27b041deface21f1776ff4357edf1c5a2fbf0470df79ec9ec89a97875b04`.
- v2 seed 2: `a410e9ce772aaa5d05b54f80fbae66d5a1f74a93064c3aadc63163c4f491af92`.

At inspection, registration.md's redesign paragraph still printed an earlier v2 counter hash (`f7f86d75…`); the measured bytes and both receipts use the exact newer pin supplied by the L1. Registration was not edited.

Bounded `df -h /fast` reported 113G available before rescore. Independent before/after Hyprland coredump counts were both 1338, delta 0; both counters also printed `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`. Only the frozen counter/oracle launched nested compositors. Both awaited counter processes exited with code 1 and their oracle calls executed harness process-group cleanup. No persistent service, additional test, install, production parser change, or restoration was required.

## C1 v3 rescore — unchanged control

CONTROL K1RootOnly v3 best: PRED-C1-r27-v3 cases_pass=3/41 verdict=TARGET_MISSED — not met

The L1 retired counter v2 before data after a different variable-prefix-keyed reader met its target. The preceding v1/v2 results remain historical. This rescore uses v3, which randomizes variable names without a fixed prefix. The ROOT-ONLY control was not changed.

Executed twice concurrently from the lane directory with clean parent environments containing only `PATH=/usr/bin`, retaining verbatim stdout in the requested receipts:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v3.py 9f5fc28b --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1RootOnly.py --jobs 6
```

| Run | Fresh seed | Actual predicate output | Exit | Receipt | Elapsed |
| --- | --- | --- | --- | --- | --- |
| 1 | `d251182b055cf307` | `PRED-C1-r27-v3 cases_pass=3/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/v3/K1RootOnly-seed1.txt` | 108.464 s |
| 2 | `3baf9ef184c7bf09` | `PRED-C1-r27-v3 cases_pass=3/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/v3/K1RootOnly-seed2.txt` | 113.022 s |

Both receipts resolve the revision to `9f5fc28b3db8d06870d0314818ffbe5e43bb5937`, confirm repeated BASE equality, pinned Hyprland v0.56.2, and the unchanged 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`. Stderr was empty for both runs. Neither returned guard code 2; no retry was required.

Before/after SHA-256 values were identical:

- Control: `bf9a86af4f5f34679d77a47d19ba67614a1715c2b6d74df175469fee20b3544a`, unchanged from v1/v2.
- Counter v3: `ee4cea19c11a1a8160115f4754e88c11c58aac9a3bff40ccfd16920cd1d691bd`, matching the L1 pin and registration.
- Oracle: `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`.

Receipt SHA-256:

- v3 seed 1: `585c4789c40ab4ae12313c05662224687bb19da33f4eb1b1dd42cf35040b638d`.
- v3 seed 2: `b7c3d5bd785df50a7bb95e9e77dbe3d5f21952c352242ea009ec696e182aa8a5`.

Before rescore, bounded `df -h /fast` reported 94G available. Independent Hyprland coredump counts before and after were both 1338, delta 0; both receipts independently print `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`. Only the frozen counter/oracle launched nested compositors. Both awaited counter processes exited with code 1 and their oracle calls executed harness process-group cleanup. No persistent service or tool install was started. No control, frozen counter, oracle, production code, or sibling file was modified; no restoration was necessary. The source-omission control is rejected under v3.

## C1 v4 rescore — unchanged RootOnly and GlobalOnce controls

CONTROL K1RootOnly v4 best: PRED-C1-r27-v4 cases_pass=4/41 verdict=TARGET_MISSED — not met

CONTROL K1GlobalOnce v4 best: PRED-C1-r27-v4 cases_pass=17/41 verdict=TARGET_MISSED — not met

The L1 retired counter v3 before data after two partial-variable readers met it. These are the replacement v4 measurements, including the additionally assigned GlobalOnce control. Neither control was edited. Counter v4 adds embedded-value variables, sourced definitions, use-before-definition and repeated-source cases; the preceding counter-version measurements remain historical.

From the lane directory, executed each of these exact commands twice with fresh counter-generated seeds, four concurrent processes total, each with a clean parent environment containing only `PATH=/usr/bin`:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1RootOnly.py --jobs 4
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1GlobalOnce.py --jobs 4
```

All four runs resolved revision `2fdca5caaab6859386effbb8fa6acc5250c90633`. Complete stdout, including the terminal `exit=1`, was saved verbatim to the following receipts; stderr was empty in every run. No run returned guard code 2 and no retry was required.

| Control/run | Fresh seed | Actual predicate output | Exit | Receipt | Elapsed |
| --- | --- | --- | --- | --- | --- |
| RootOnly 1 | `e825b5546cbce3dc` | `PRED-C1-r27-v4 cases_pass=2/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/v4/K1RootOnly-seed1.txt` | 210.630 s |
| RootOnly 2 | `46b396d0210888e4` | `PRED-C1-r27-v4 cases_pass=4/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/v4/K1RootOnly-seed2.txt` | 199.779 s |
| GlobalOnce 1 | `3ef4f2738806c3b3` | `PRED-C1-r27-v4 cases_pass=17/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/v4/K1GlobalOnce-seed1.txt` | 197.787 s |
| GlobalOnce 2 | `62a8d764b772bd03` | `PRED-C1-r27-v4 cases_pass=17/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/v4/K1GlobalOnce-seed2.txt` | 211.784 s |

Every receipt confirms repeated BASE equality, pinned Hyprland v0.56.2 at `efb50993780079460b0cbed1363e2166a2de1d9f`, and the same 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`.

Before/after SHA-256 values were identical:

- RootOnly: `bf9a86af4f5f34679d77a47d19ba67614a1715c2b6d74df175469fee20b3544a`, unchanged from all earlier measurements.
- GlobalOnce: `5fe54d4992578bb69f7ceabe4af166c894e5a80a16bda43e7e811d9ba8c4ca39`.
- Counter v4: `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1`, matching the L1 pin and registration.
- Oracle: `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`.

Receipt SHA-256:

- RootOnly seed 1: `f1696cf0107658088be5bbc3e04c949de93656f8aac080de2f7f018ad6535deb`.
- RootOnly seed 2: `8c8d64f86770266f6782619ec93c881b235e1ca63208ef0569153ef746d858c0`.
- GlobalOnce seed 1: `cc3bb9f938d254f4a92dd7fb4bbdbf26770a3fa91077dda275cfb324c099643d`.
- GlobalOnce seed 2: `a2b0bc34669009dbf57af0b1a874db6aa3880472f890e28ed0b3ba71a1eb5cc4`.

Bounded `df -h /fast` reported 84G available before these runs. Independent before/after Hyprland coredump counts were both 1338, delta 0. All four receipts also print `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`. Only the frozen counter/oracle launched nested compositors; its host-wide slot locks enforced the 12-instance bound. All four awaited counter processes exited with code 1, and their oracle calls executed harness process-group cleanup. No persistent service or installation was started. Neither control, the counter, the oracle nor any sibling source was modified, so restoration was unnecessary. Both controls are rejected under v4.
