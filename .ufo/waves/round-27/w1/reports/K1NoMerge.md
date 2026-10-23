# K1NoMerge — C1 NO-MERGE control

## Verdict
CONTROL K1NoMerge best: PRED-C1-r27 cases_pass=18/41 verdict=TARGET_MISSED — not met

The bounded detector distinguished this control on both fresh seeds. Neither run met 41/41; neither exited 2.

## Defect and permitted behavior

Created only `.ufo/waves/round-27/controls/K1NoMerge.py`, its two receipts, and this report. No data-seat tool or suite was built or changed.

The plausible defect is replacing `WorkspaceRuleManager::replaceOrAdd` with append-only insertion: every successfully parsed `workspace =` line creates a fresh object, including repeated selectors. There is no selector lookup, deduplication, cross-line update, or merge. Expected detector: the frozen C1 counter's exact ordered JSON-array comparison rejects the excess entries where Hyprland combines repeated selectors.

The control otherwise follows sorted source globs depth-first, expands config variables longest-name-first, handles comments and escaped hashes, joins continued lines, respects hyprlang conditional comments, parses CSS gap shorthand and boolean words, and renders the workspace-rule JSON fields including cleaned `on-created-empty` commands. It reuses the traversal pattern in `tools/mado-anims.py`. It reads config bytes only, uses Python's standard library only, and does not inspect case labels, receipts, environment metadata, or a live compositor. No expected tables are embedded.

Godspeed axes: shape fidelity; permitted parsing coverage; exact oracle equality; host safety and reproducible evidence. Independent source fetches and the two mandated measurements ran concurrently; the control bytes were identical for both measurements.

## Exact detector command

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Executed this command twice, without supplying `--seed`, so each invocation generated a fresh random seed:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count.py 5ddc5885 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NoMerge.py --jobs 6
```

| Run | Fresh seed | Actual PRED output | Process exit | Elapsed | Verbatim stdout receipt |
| --- | --- | --- | --- | --- | --- |
| 1 | `3e1018b3f675bb25` | `PRED-C1-r27 cases_pass=18/41 verdict=TARGET_MISSED` | 1 | 12.979 s | `.ufo/waves/round-27/controls/K1NoMerge-seed1.txt` |
| 2 | `c5e8246b8e68d97d` | `PRED-C1-r27 cases_pass=13/41 verdict=TARGET_MISSED` | 1 | 22.493 s | `.ufo/waves/round-27/controls/K1NoMerge-seed2.txt` |

Both receipts end in `exit=1`; both stderr captures were empty. Saved receipt bytes were compared with the captured stdout and matched exactly.

Both runs reported `ORACLE_CHECK base_twice equal rules=0`, passed BASE, and confirmed the oracle commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`. Both measured the same 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`.

All 23 failed cases in run 1 and all 28 failed cases in run 2 had more output entries than the oracle. All run-1 failures and 27 run-2 failures were explicitly marked MERGE. Run-2 C20 also had `rules got=3 want=2` despite lacking that feature label; no claim is made that the feature label exhaustively identifies selector collisions. Examples:

```text
CASE C23   FAIL rules got=2 want=1 first_diff=0 oracle_rules=1 (APPEND:BOOLWORD+MERGE)
CASE C39   FAIL rules got=2 want=1 first_diff=0 oracle_rules=1 (SYNTH:BOOLWORD+MERGE+NEWSRC)
```

The first example is run 1; the second is run 2. Non-merge examples with sources, variables, gap shorthand, boolean words, and creation commands passed, as recorded in the receipts.

## Source grounding

Read registration first. Opened the pinned raw sources in memory with this bounded, cleared-environment command form, using the URL as the final argument:

```sh
env -i PATH=/usr/bin timeout 35 prlimit --as=4000000000 -- curl -fsSL --max-time 30 --max-filesize 2000000 URL
```

Key sources, all at Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f`:

- [ConfigManager.cpp](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp):1676–1854 — workspace-field parsing and source traversal.
- [HyprCtl.cpp](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp):522–550 — JSON fields and optional-field emission.
- [WorkspaceRuleManager.cpp](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/workspace/WorkspaceRuleManager.cpp):25–31 — the deliberately omitted selector lookup and merge.
- [ComplexDataTypes.hpp](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp):80–120 — CSS gap expansion.
- [MiscFunctions.cpp](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/MiscFunctions.cpp):125–475,478–512 — workspace names and creation-command cleaning.

The attempted `src/config/shared/complex/ComplexDataTypes.cpp` URL returned HTTP 404; the available header contains the implementation. No downloaded source files or helper scripts were retained.

## Byte integrity and restoration evidence

No pre-existing subject bytes were mutated, so a pristine/mutated/restored production-tool experiment was not performed or claimed. This assignment created a retained, shape-constrained control and scored it twice. Before and after those runs, the following SHA-256 hashes were identical:

| File | Before = after SHA-256 |
| --- | --- |
| `.ufo/waves/round-27/controls/K1NoMerge.py` | `918501eb066d36b811a6ac0ec759e2b510c2285261c58d5f9058291ead785947` |
| `.ufo/waves/round-27/c1/count.py` | `3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136` |
| `.ufo/waves/round-27/harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

Receipt integrity:

- Seed 1: 4,796 bytes; SHA-256 `2a2ef9e28796341fa5a4dfafaec4fa05d949477897f66738b5438531225ab8c0`.
- Seed 2: 4,954 bytes; SHA-256 `3680b105b86eee7d751f675044f5a29dfa7491eba598914965913c2998043170`.

## Host safety and tooling

`env -i PATH=/usr/bin timeout 10 df -h /fast` reported 115G available before counter writes. No Hyprland process was started outside the frozen counter/oracle path; no live-session commands or DRM card nodes were used. Each counter completed normally, with its harness responsible for stopping its nested process trees. No background job or service was retained.

Both receipts contain:

```text
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
```

Independent before/after coredump measurements used `env -i PATH=/usr/bin timeout 15 prlimit --as=4000000000 -- coredumpctl list --no-pager --no-legend`, counting output lines containing `/usr/bin/Hyprland`: 1,338 before, 1,338 after, delta 0; both commands exited 0 with empty stderr.

No tools were installed or updated. No git/jj write commands, host-service changes, held-out reads, or additional behavioral probes were performed.

## v2 rescore — unchanged control

CONTROL K1NoMerge v2 best: PRED-C1-r27-v2 cases_pass=20/41 verdict=TARGET_MISSED — not met

L1 retired v1 before data and requested this follow-up under the redesigned, type-strict v2 detector. The control was not edited. This section adds exactly two v2 measurements; the v1 receipts and findings above remain historical evidence.

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Executed twice concurrently, allowing each invocation to generate its own fresh seed:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v2.py a4dc0da0 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NoMerge.py --jobs 6
```

| Run | Fresh seed | Actual PRED output | Process exit | Elapsed | Verbatim stdout receipt |
| --- | --- | --- | --- | --- | --- |
| 1 | `4c5cad49891a6850` | `PRED-C1-r27-v2 cases_pass=20/41 verdict=TARGET_MISSED` | 1 | 116.010 s | `.ufo/waves/round-27/controls/v2/K1NoMerge-seed1.txt` |
| 2 | `0727a9cfecf66ae2` | `PRED-C1-r27-v2 cases_pass=7/41 verdict=TARGET_MISSED` | 1 | 87.106 s | `.ufo/waves/round-27/controls/v2/K1NoMerge-seed2.txt` |

Both stderr captures were empty, and both receipts end in `exit=1`. Neither run exited 2, so no guard retry was required. Saved receipt bytes matched captured stdout exactly:

- Seed 1: 5,296 bytes; SHA-256 `42aaa8fa8dfbd4936c709312594b833e2ac31b5856677259041cf5e6301add6b`.
- Seed 2: 5,648 bytes; SHA-256 `f89e85464e30e6476bae7ce0ff1648aaa3f65d5356d6448bd846359be669bc8f`.

Both runs passed BASE, reported `ORACLE_CHECK base_twice equal rules=0`, and confirmed Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`. They used revision `a4dc0da0394a71badf506e9c72144cd1b8ca7281` and the same 79-file snapshot digest recorded above.

The detector distinguished the NO-MERGE defect on both seeds: all 21 failures in run 1 and all 34 failures in run 2 had excess entries. All run-1 failures and 32 run-2 failures carried MERGE labels. Run-2 C02 and C37 had excess entries without MERGE labels; feature-label completeness is not assumed. A glob-source case passed in run 2 (`C06`), a nested-source case passed in run 1 (`C02`), and variable-redefinition and interleaved-source cases also passed, as recorded in the receipts.

Before and after the v2 measurements, all measured hashes were identical:

| File | Before = after SHA-256 |
| --- | --- |
| Control | `918501eb066d36b811a6ac0ec759e2b510c2285261c58d5f9058291ead785947` |
| C1 counter v2 | `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87` |
| Retired C1 counter v1 | `3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136` |
| Oracle | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

Thus no restoration was necessary: the retained control is byte-identical to the originally scored file, and neither detector nor harness was mutated.

The pre-write disk command reported 114G available on `/fast`. Both v2 receipts reported `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`. Independent coredump measurements using the bounded command recorded above also gave 1,338 before and after, delta 0; both commands exited 0 with empty stderr. Both counter processes completed normally. No background service, source edit, git/jj write, or tool installation was added by this follow-up.


## v3 rescore — unchanged control

CONTROL K1NoMerge v3 best: PRED-C1-r27-v3 cases_pass=14/41 verdict=TARGET_MISSED — not met

L1 retired v2 before data after a fixed-variable-prefix reader met it. Per the follow-up assignment, scored the original, unchanged NO-MERGE control twice against v3, whose variable names have no fixed prefix. No control implementation changes or additional probes were made.

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Exact command, executed twice concurrently with automatically generated fresh seeds:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v3.py 9f5fc28b --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NoMerge.py --jobs 6
```

| Run | Fresh seed | Actual PRED output | Process exit | Elapsed | Verbatim stdout receipt |
| --- | --- | --- | --- | --- | --- |
| 1 | `4f300834ca94c475` | `PRED-C1-r27-v3 cases_pass=14/41 verdict=TARGET_MISSED` | 1 | 100.571 s | `.ufo/waves/round-27/controls/v3/K1NoMerge-seed1.txt` |
| 2 | `53cc409ac3e29827` | `PRED-C1-r27-v3 cases_pass=8/41 verdict=TARGET_MISSED` | 1 | 106.613 s | `.ufo/waves/round-27/controls/v3/K1NoMerge-seed2.txt` |

Both receipts end in `exit=1`; both stderr captures were empty. Neither run exited 2, so no guard retry was needed. Each receipt was byte-compared with captured stdout and matched exactly:

- Seed 1: 5,314 bytes; SHA-256 `605cf2f290bc2d06784a3653280325663518e8fee0ef4d75aaae42155d127948`.
- Seed 2: 5,715 bytes; SHA-256 `77f7fedf1368475000a12903e9120c28114c6929d6932af51d976c6199634842`.

Both runs passed BASE and reported `ORACLE_CHECK base_twice equal rules=0`. Both confirmed Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`, and measured the same 79-file snapshot digest recorded above. The measured revision was `9f5fc28b3db8d06870d0314818ffbe5e43bb5937`.

The expected NO-MERGE defect was distinguished in both runs: all 27 run-1 failures and all 33 run-2 failures had more entries than the oracle. MERGE labels appeared on 23 and 28 of those failures respectively; the label is not treated as exhaustive. Run-1 C01 passed with NESTED, NEWSRC, and VARIABLE features; multiple ORDER and VARREDEF cases also passed.

Restoration/immutability evidence: no pre-existing bytes were mutated, and these SHA-256 hashes were equal before and after both v3 measurements:

| File | Before = after SHA-256 |
| --- | --- |
| Original control | `918501eb066d36b811a6ac0ec759e2b510c2285261c58d5f9058291ead785947` |
| C1 counter v3 | `ee4cea19c11a1a8160115f4754e88c11c58aac9a3bff40ccfd16920cd1d691bd` |
| Oracle | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

The bounded disk-capacity command reported 94G available on `/fast` before these runs. Both receipts reported `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`. Independent bounded coredump measurements also returned 1,338 before and after, delta 0, with exit 0 and empty stderr. Both counter processes completed normally; no background service, host-service change, git/jj write, or tool installation was introduced.


## v4 rescore — NO-MERGE and supplied FileScope controls unchanged

CONTROL K1NoMerge v4 best: PRED-C1-r27-v4 cases_pass=9/41 verdict=TARGET_MISSED — not met

CONTROL K1FileScope v4 best: PRED-C1-r27-v4 cases_pass=32/41 verdict=TARGET_MISSED — not met

L1 retired v3 before data and requested two fresh-seed v4 measurements of each unchanged control. The supplied FileScope control was measured, not authored or edited, by this seat. This follow-up changed only the four requested receipt paths and this report.

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Each exact command below ran twice; the four independent invocations ran concurrently, using the harness's host-wide oracle-slot locks:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NoMerge.py --jobs 4
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1FileScope.py --jobs 4
```

| Control / run | Fresh seed | Actual PRED output | Process exit | Elapsed | Verbatim stdout receipt |
| --- | --- | --- | --- | --- | --- |
| K1NoMerge / 1 | `ae05fa9a659a346f` | `PRED-C1-r27-v4 cases_pass=7/41 verdict=TARGET_MISSED` | 1 | 201.129 s | `.ufo/waves/round-27/controls/v4/K1NoMerge-seed1.txt` |
| K1NoMerge / 2 | `538061af089eeeab` | `PRED-C1-r27-v4 cases_pass=9/41 verdict=TARGET_MISSED` | 1 | 199.076 s | `.ufo/waves/round-27/controls/v4/K1NoMerge-seed2.txt` |
| K1FileScope / 1 | `73c12a6b620017e9` | `PRED-C1-r27-v4 cases_pass=29/41 verdict=TARGET_MISSED` | 1 | 180.674 s | `.ufo/waves/round-27/controls/v4/K1FileScope-seed1.txt` |
| K1FileScope / 2 | `5ec3ce7e2621b702` | `PRED-C1-r27-v4 cases_pass=32/41 verdict=TARGET_MISSED` | 1 | 192.884 s | `.ufo/waves/round-27/controls/v4/K1FileScope-seed2.txt` |

All four counter stderr captures were empty. All receipts end in `exit=1`; no run exited 2 and no guard retry was necessary. Receipt bytes were saved directly from captured stdout through the write tool and compared equal:

| Receipt | Bytes | SHA-256 |
| --- | --- | --- |
| K1NoMerge-seed1 | 5,992 | `7bf103c0c3f7873abdd2bfaa1cc1912d2f35fbb2c5029e7e643c53ba0c4ff33b` |
| K1NoMerge-seed2 | 5,994 | `0daea933a8d64bc9b211cd7c56e0cb53f4fc06f9d34606d8d9c9c7ac993b47a9` |
| K1FileScope-seed1 | 5,840 | `5e383a4817ca50adc10108e0c94a06c9e6e844267243830a0762679ce4d39ddb` |
| K1FileScope-seed2 | 5,721 | `5789d0eb5ab0990903741611f66c39ac813d3e55993ce79e39b5ef0b2bb0a815` |

Every run passed BASE, reported `ORACLE_CHECK base_twice equal rules=0`, confirmed the pinned Hyprland commit/tag, and used the same 79-file snapshot digest recorded above. The measured revision was `2fdca5caaab6859386effbb8fa6acc5250c90633`.

Expected detector and observed defect evidence:

- NO-MERGE: all 34 seed-1 failures and all 32 seed-2 failures had excess entries; there were no tool-process failures. The exact-array detector distinguished append-only insertion from Hyprland's selector merge.
- FileScope: all 12 seed-1 failures and all 9 seed-2 failures carried SRCDEF labels. Seed 1 included two tool exits with unresolved-variable integer-conversion errors; seed 2 included one. Other failures were JSON mismatches. These tool-error excerpts are preserved inside the counter's stdout receipts; empty counter stderr does not mean those case tools emitted no stderr.

Restoration/immutability evidence: neither control, the counter, nor the oracle was modified. These before/after SHA-256 values matched exactly:

| File | Before = after SHA-256 |
| --- | --- |
| K1NoMerge.py | `918501eb066d36b811a6ac0ec759e2b510c2285261c58d5f9058291ead785947` |
| K1FileScope.py | `f56e20a77dc511b10963cf70a69c2971499244ee035d309f224525c1cd553bcb` |
| C1 counter v4 | `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1` |
| Oracle | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

The bounded disk command reported 84G available on `/fast` before the measurements. All four receipts recorded `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`. Independent bounded coredump measurements also gave 1,338 before and after, delta 0, exit 0, empty stderr. All counter processes completed normally; no background service, host-service change, git/jj write, or tool installation was introduced.

