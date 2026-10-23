# K1Junk — C1 negative control

## Verdict
CONTROL K1Junk best: PRED-C1-r27 cases_pass=0/41 verdict=TARGET_MISSED — not met

Both fresh-seed runs rejected the JUNK control: 0/41, process exit 1. Neither run hit a setup guard or timeout. This control does not trigger the registration's target-met kill rule. This is a standalone negative-control result, not a pristine-versus-mutated source kill claim.

## Assigned defect and shape

Created only `controls/K1Junk.py` under `.ufo/waves/round-27/`. It accepts the required `--home DIR` interface but ignores the argument and reads no config bytes, paths, case labels, environment labels, or mount metadata. Python stdlib `random.SystemRandom` chooses a uniform array length from 0 through 4 and generates workspace-rule-shaped dictionaries with random selectors, monitors, booleans, four-component gaps, border sizes, and on-created-empty strings. Serialization uses `json.dumps`.

Axes: valid bounded JSON, strict config blindness, and exact-match coverage under two fresh case seeds. No claimed parser implementation or data-seat file was built.

## Detector and exact scoring command

Read `registration.md` and the godspeed skill before implementing the control. The frozen detector compares parsed JSON lists exactly, including order, keys and values, against isolated Hyprland v0.56.2. Target: 41/41 over BASE, 25 APPEND and 15 SYNTH cases.

Executed the following command twice, concurrently, from `/home/vgpnk/Projects/shokunin/mado-shokunin`. Each invocation generated its own fresh counter seed; all child environments were explicitly cleared. No `--seed` override was supplied.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count.py 5ddc5885 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1Junk.py --jobs 6
```

Python subprocess pipes captured stdout and stderr separately. The named receipts contain stdout verbatim, including the counter's final `exit=1`; both stderr streams were empty.

| Run | Fresh case seed | Actual prediction line | Exit | Verbatim stdout receipt |
| --- | --- | --- | --- | --- |
| 1 | `1854373589060703` | `PRED-C1-r27 cases_pass=0/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/K1Junk-seed1.txt` |
| 2 | `518858441b8334cc` | `PRED-C1-r27 cases_pass=0/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/K1Junk-seed2.txt` |

Both receipts report:

```text
ORACLE_CHECK base_twice equal rules=0
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C1-r27 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

The resolved revision was `5ddc5885188a1de8606464526d636c9e2fc433e6`. Both snapshots contained 79 files with digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`. Every case failed exact equality. The random BASE lengths were 3 and 4 respectively, versus the oracle's empty list.

## Hash and restoration evidence

No lane subject was mutated, so no source restoration was needed. The new control remained byte-identical across both runs, and the frozen inputs remained byte-identical before and after. Hashes were measured with `sha256sum`, not inferred.

| Path under `.ufo/waves/round-27/` | SHA-256 before = after |
| --- | --- |
| `controls/K1Junk.py` | `2105846310d5b3e85b707b7e809d171b6a66c1914cde8be89db6f13272645a5a` |
| `c1/count.py` | `3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136` |
| `harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |
| `c2/mutants-w.json` | `0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608` |

Receipt hashes:

- `controls/K1Junk-seed1.txt`: `3e69e15ce2ccd00ae04be95e9e2c695a9615a9d8ba4069ff672f692b61f83466`
- `controls/K1Junk-seed2.txt`: `6c131d9a80f573c0d8a3a70309128e48496e9d0d86ec6cde79fda68d3563977d`

Exact before/after evidence commands, run from the lane root:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/c1/count.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/c2/mutants-w.json
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/controls/K1Junk.py
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/controls/K1Junk.py .ufo/waves/round-27/c1/count.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/c2/mutants-w.json .ufo/waves/round-27/controls/K1Junk-seed1.txt .ufo/waves/round-27/controls/K1Junk-seed2.txt
```

## Host safety and scope

Before scoring, `df -h /fast` reported 115G available. The command was:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 --core=0 -- df -h /fast
```

The explicit coredump count command below returned `1338` before and `1338` after: delta 0, also independently recorded by both counter receipts.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland
```

A final process inspection ran the command below with a cleared environment, then filtered its captured output for the exact absolute control path. It reported `K1Junk remaining process matches=0` and `process_check_exit=0`. Both counter subprocesses had already exited normally.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 --core=0 -- ps -eo pid=,ppid=,args=
```

No live-compositor commands, direct Hyprland launches, git/jj write commands, subagent dispatch, tool installation, or service restart was performed. Writes were limited to this report, the single assigned control, and its two receipts. No additional verification beyond the assigned scoring and safety/hash evidence was run.

## C1 counter v2 re-score
CONTROL K1Junk v2 best: PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED — not met

L1 retired v1 before data after a different source-blind control met its target. Per the follow-up, re-scored the unchanged JUNK control twice against the revised detector, including unsourced decoys, nested/glob sources, interleaved source order, variable redefinition, and type-strict canonical-JSON comparison. Used the follow-up's exact v2 pin `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87`, measured before and after.

Executed this exact command twice concurrently from the lane root, with separate fresh automatically generated case seeds and explicitly cleared subprocess environments:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v2.py a4dc0da0 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1Junk.py --jobs 6
```

| Run | Fresh case seed | Actual prediction line | Process exit | Verbatim stdout receipt |
| --- | --- | --- | --- | --- |
| 1 | `167addaf08663b08` | `PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/v2/K1Junk-seed1.txt` |
| 2 | `754aa02a1f9f539f` | `PRED-C1-r27-v2 cases_pass=0/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/v2/K1Junk-seed2.txt` |

Both receipts preserve stdout verbatim through `exit=1`; both stderr streams were empty. Neither run timed out or hit an exit-2 guard. The resolved revision was `a4dc0da0394a71badf506e9c72144cd1b8ca7281`.

Run 1 passed only BASE because the random output was the oracle's empty list; all 40 generated cases failed. Run 2 emitted two objects for BASE, so all 41 cases failed. Thus neither seed met the 41/41 target.

Both runs reported:

```text
ORACLE_CHECK base_twice equal rules=0
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
```

### V2 unchanged-byte and safety evidence

| Path under `.ufo/waves/round-27/` | SHA-256 before = after |
| --- | --- |
| `controls/K1Junk.py` | `2105846310d5b3e85b707b7e809d171b6a66c1914cde8be89db6f13272645a5a` |
| `c1/count-v2.py` | `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87` |
| `harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

No subject or control bytes were changed, so restoration was unnecessary. These measured hashes also show the control is identical to the v1-tested bytes.

Receipt hashes:

- `controls/v2/K1Junk-seed1.txt`: `c7d9ddc25c898ebb7a60e40b8c476fb43a9b88645e384ca44327df7e3890977f`
- `controls/v2/K1Junk-seed2.txt`: `71b5fdf61a03d14f15064bbac88f8deecc0b5e211503c1afa7271df2abb7e319`

Exact before/after hash commands:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/controls/K1Junk.py .ufo/waves/round-27/c1/count-v2.py .ufo/waves/round-27/harness/oracle.py
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/controls/K1Junk.py .ufo/waves/round-27/c1/count-v2.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/controls/v2/K1Junk-seed1.txt .ufo/waves/round-27/controls/v2/K1Junk-seed2.txt
```

The earlier `df -h /fast` command was repeated before v2 and reported 113G available. The explicit coredump command below returned 1338 before and 1338 after, delta 0:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 --core=0 -- sh -c 'coredumpctl list --no-pager --no-legend | grep -c /usr/bin/Hyprland'
```

Both bounded counter processes exited normally (PIDs 556529 and 556544). Repeated the earlier cleared-environment `ps -eo pid=,ppid=,args=` inspection, filtering captured output for the exact absolute control path: `K1Junk v2 remaining process matches=0`, `process_check_exit=0`.

Follow-up writes were limited to the two assigned `controls/v2/` receipts and this appended report section. No control edit, tool installation, direct Hyprland launch, live-compositor command, git/jj write, or subagent dispatch was performed.
