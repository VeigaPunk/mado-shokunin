# K1StaticBase — STATIC-BASE C1 control

## Verdict
CONTROL K1StaticBase best: PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED — not met

Both fresh-seed runs rejected the control (exit 1): BASE passed, all 25 APPEND and all 15 SYNTH cases failed. No exit-2 guard occurred. This control does not trigger the registration kill rule. The captured unperturbed table is empty, so this shape happens to produce the same output as DoNothing, but its value was obtained from the required single live read rather than assumed.

## Control and expected detector

Axes: shape fidelity, generated-case discrimination, reproducibility, host safety.

Created only the assigned control and evidence/report paths. The behavior-bearing point is the constant table in `.ufo/waves/round-27/controls/K1StaticBase.py`: it accepts required `--home DIR`, never inspects the tree, and prints the captured `[]` for every input. It is a single Python stdlib file. No solver, suite, counter, harness, or sibling source was changed.

The expected detector is the frozen round-27 C1 counter: exact ordered JSON-array equality against isolated Hyprland v0.56.2 for 1 BASE + 25 APPEND + 15 SYNTH cases, with target 41/41. A static table should pass the unperturbed case and fail changed rule tables. Both runs observed precisely that. This is rejection of the assigned negative control, not a claim of a restored three-run mutation probe against an implemented solver.

## Exact commands and outputs

Commands below used `/home/vgpnk/Projects/shokunin/mado-shokunin` as the working directory, except the free-space and coredump queries, which used `/home/vgpnk/Projects/shokunin`.

Free-space check before counter scratch writes:

```sh
env -i PATH=/usr/bin timeout 10 prlimit --as=4000000000 --core=0 -- df -h /fast
```

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  689G  115G  86% /fast
```

Single live workspace-table read, performed while creating the control:

```sh
env -i PATH=/usr/bin timeout 20 prlimit --as=4000000000 --core=0 -- hyprctl -i 0 workspacerules -j
```

Verbatim output:

```json
[]
```

Scored twice with the same exact command; the counter generated two fresh seeds. The two runs were concurrent, using six oracle workers each and the harness's host-wide slot locks:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count.py 5ddc5885 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1StaticBase.py --jobs 6
```

| Run | Fresh seed | Result | Process status | Verbatim stdout receipt |
| --- | --- | --- | --- | --- |
| 1 | `bef00eeeec06b45b` | `PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/K1StaticBase-seed1.txt` |
| 2 | `f91785fe482cff10` | `PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/K1StaticBase-seed2.txt` |

Both receipts include `ORACLE_CHECK base_twice equal rules=0` and `ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2`. Both snapshots contained 79 files, digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`. Resolved revision: `5ddc5885188a1de8606464526d636c9e2fc433e6`.

## Preservation and hashes

SHA-256 hashes measured before and after both detector runs were identical:

| File | Before = after SHA-256 |
| --- | --- |
| `.ufo/waves/round-27/controls/K1StaticBase.py` | `857cd2de4de199a99fc48527ae64b17938c72cf9dc6f0b9768271297d0a76873` |
| `.ufo/waves/round-27/c1/count.py` | `3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136` |
| `.ufo/waves/round-27/harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

Exact before-hash command:

```sh
env -i PATH=/usr/bin timeout 10 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/controls/K1StaticBase.py .ufo/waves/round-27/c1/count.py .ufo/waves/round-27/harness/oracle.py
```

The after-hash command was identical with the two receipt paths appended. Receipt SHA-256 values:

- Seed 1: `9577a1cda430b4b4c26faa4eb56e35add7db129c7d3d7723bb15685447ca9857`.
- Seed 2: `c9d3a86d1cb02910c17183e1d6f96ba6dcef4e72b40082d6c7fb49164ba52e10`.

No existing subject bytes were mutated, so no byte restoration was needed. The assigned persistent control retains exactly its pre-score bytes. Counter and harness pins were preserved. No git/jj write commands were run.

## Host safety and cleanup

Before and after the work, ran:

```sh
env -i PATH=/usr/bin timeout 20 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland
```

Both outputs were `1338`: own observed Hyprland coredump delta 0. Each counter independently printed `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`.

The only live compositor operation was the one read-only query above. Every launched command used a cleared environment; no WAYLAND_DISPLAY or HYPRLAND_INSTANCE_SIGNATURE was set or inherited by those commands. Nested compositor launches were exclusively through the frozen counter/oracle, not direct commands. Both bounded counters exited normally with code 1. The oracle's existing finally block terminates its sandbox process groups, waits, escalates if necessary, and removes its temporary runtime directory; the counter removes its scratch tree in finally. No long-lived service was started.

No tools were installed or updated. No additional tests, builds, or unrelated verification were run.

## V2 re-score — unchanged control

CONTROL K1StaticBase v2 best: PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED — not met

The v1 findings above are historical: L1 retired v1 before data after another control met its target. Per the same-item follow-up, re-scored the identical STATIC-BASE bytes against the final amended v2 counter, whose registration pin and observed SHA-256 were `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87`. V2 adds unsourced decoys, nested/glob sources, source placement among rules, variable redefinition, and type-strict JSON comparison. No second live query was made and the embedded table remains `[]`.

Ran the following exact command twice from `/home/vgpnk/Projects/shokunin/mado-shokunin`, concurrently with six workers each:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v2.py a4dc0da0 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1StaticBase.py --jobs 6
```

| Run | Fresh seed | Result | Process status | Verbatim stdout receipt |
| --- | --- | --- | --- | --- |
| 1 | `6a01588c811bc3db` | `PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/v2/K1StaticBase-seed1.txt` |
| 2 | `c2329b28df187b04` | `PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED` | `exit=1` | `.ufo/waves/round-27/controls/v2/K1StaticBase-seed2.txt` |

Each run passed BASE and failed all 25 APPEND and all 15 SYNTH cases. Neither hit an exit-2 guard. Both confirmed the base twice with zero rules and the pinned v0.56.2 commit. Resolved revision: `a4dc0da0394a71badf506e9c72144cd1b8ca7281`. Snapshot files/digest were identical to the earlier runs. The control was rejected under v2; the outcome does not change the STATIC-BASE contract.

Before the runs, the same bounded `df -h /fast` command recorded 113G available (804G total, 691G used, 86%). The same bounded coredump query before and after returned `1338`; delta 0. Both receipts independently print `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`. Both counter processes exited with code 1 and used the frozen oracle's process-group teardown and scratch cleanup. No direct compositor launch, live mutation, long-lived service, installation, or git/jj write occurred.

Preservation evidence: before and after hashes, measured using the same bounded `sha256sum` command pattern above with `count-v2.py` in place of `count.py`, remained:

- Control: `857cd2de4de199a99fc48527ae64b17938c72cf9dc6f0b9768271297d0a76873`.
- V2 counter: `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87`.
- Oracle: `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`.

After-score receipt SHA-256 values:

- V2 seed 1: `c4e039bbb01e3a88f4a3b4def20de3c4ea46be749cb8b9033498c532acf78ea9`.
- V2 seed 2: `a88acbddaa82f8bd37dcafbb90b8f9151a992c3962261e83878aacb1a45c2f89`.

No control or subject bytes changed, so no restoration was needed. Only the two assigned v2 receipt files were created and this report was appended.
