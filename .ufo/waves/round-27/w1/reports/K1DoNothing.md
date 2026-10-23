# K1DoNothing — C1 DO-NOTHING control

## Verdict

CONTROL K1DoNothing best: PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED — not met

Both fresh-seed DO-NOTHING runs passed only BASE and failed all 40 generated cases. The requested empty, 0-byte comparison passed 0/41. None met the 41/41 target; none exited 2.

## Scope and shape

Read the frozen registration first, then the godspeed skill, operator rules, and relevant counter/harness sections. Axes: shape fidelity, detector discrimination, exact restoration, and host safety.

Created only the assigned control, its three receipts, and this report. The complete final control is 12 bytes:

```python
print("[]")
```

It accepts the `--home DIR` invocation by ignoring arguments and always prints the JSON array `[]`; it performs no tree reads or workspace-rule derivation. No lane subject, counter, harness, W set, or sibling source was changed. No subagents or package installations were used.

## Detector and exact scoring command

All three invocations used the same bounded command below, with the working directory set to the lane. The outer subprocess environment was also limited to `PATH=/usr/bin` and `HOME=/home/vgpnk`. No seed override was supplied: the counter generated and printed a fresh seed on every run.

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count.py 5ddc5885 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1DoNothing.py --jobs 6
```

Expected detector: exact ordered JSON-array equality against the pinned isolated Hyprland oracle, 41 cases. For an empty file, the tool exits without printing JSON, so every case should fail JSON decoding, including an empty-oracle BASE.

Run order was pristine DO-NOTHING, empty bytes, exact restored DO-NOTHING. Full stdout, including `exit=`, is preserved verbatim at these lane-relative paths:

| State | Fresh seed | Exact PRED output | Process exit | Receipt |
| --- | --- | --- | --- | --- |
| Pristine, 12 bytes | `1814c0708653f7d2` | `PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/K1DoNothing-seed1.txt` |
| Empty, 0 bytes | `569a1651082a1846` | `PRED-C1-r27 cases_pass=0/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/K1DoNothing-empty.txt` |
| Restored, 12 bytes | `df7f64b0b4b6107b` | `PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/K1DoNothing-seed2.txt` |

Stderr was empty for all three commands. Each receipt identifies revision `5ddc5885188a1de8606464526d636c9e2fc433e6`, snapshot `files=79`, snapshot SHA-256 `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, and oracle commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`. Both oracle BASE repetitions agreed on zero rules in each run.

Actual pristine/restored BASE output:

```text
CASE BASE  PASS rules=0 oracle_rules=0 (unperturbed)
```

The 40 generated cases each failed with `rules got=0 want=N first_diff=0`, where every observed N was positive. The empty run instead reported `stdout is not JSON` for all 41 cases:

```text
CASE BASE  FAIL stdout is not JSON oracle_rules=0 (unperturbed)
PRED-C1-r27 cases_pass=0/41 verdict=TARGET_MISSED
exit=1
```

## Empty-file mutation and restoration evidence

The sole comparison mutation removed the control's entire print statement, producing exactly zero bytes at the same assigned control path. The counter's override hash independently records those empty bytes. Restoration ran in a `finally` block immediately after the empty-file score, before the second DO-NOTHING seed.

| Bytes/state | SHA-256 |
| --- | --- |
| Before, 12 bytes | `a3381e95441354d833917bdaf481a5b210edf2b8cda6419b5e1805dfe143fd3b` |
| Empty, 0 bytes | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Immediately restored, 12 bytes | `a3381e95441354d833917bdaf481a5b210edf2b8cda6419b5e1805dfe143fd3b` |
| After restored scoring, 12 bytes | `a3381e95441354d833917bdaf481a5b210edf2b8cda6419b5e1805dfe143fd3b` |

Mutation-probe verdict: **inconclusive at the whole-suite kill-rule level**, not a killed mutant, because the pristine control already misses the whole-suite target. Separately, the requested empty control was unambiguously rejected on all cases, and BASE changed from PASS to invalid-JSON FAIL and back to PASS after restoration. The control verdict remains **not met**; no contract change is proposed.

Before/after `sha256sum` also matched the frozen counter and harness pins:

- Counter: `3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136`.
- Harness: `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`.

Receipt SHA-256 values:

- `K1DoNothing-seed1.txt` (5,161 bytes): `d5137e82a5d7a25dddf3b4efb74bc374d55f776f4c4ee570fdf7008035920aa6`.
- `K1DoNothing-empty.txt` (4,744 bytes): `92c564cfd9436108bcb4a8ad2097ec022b0c9048e1fd3b5340fbaf65affa1fd2`.
- `K1DoNothing-seed2.txt` (5,388 bytes): `19e008e56547ff66574e2d2550703561f83c575b75e9c1c4e5ff7211ce40d557`.

## Host safety and commands

Before writes, ran:

```sh
timeout 15 env -i PATH=/usr/bin HOME=/home/vgpnk prlimit --as=4000000000 --core=0 -- df -h /fast
```

Output: `/dev/nvme1n1p2`, size `804G`, used `689G`, available `115G`, use `86%`.

Before the first score and after the final score, ran the following with subprocess environment `PATH=/usr/bin, HOME=/home/vgpnk`, counting output lines containing `/usr/bin/Hyprland` in Python:

```sh
timeout 30 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
```

Both commands exited 0 with empty stderr. Counts were **1338 before, 1338 after, delta 0**. Every counter receipt independently contains:

```text
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
```

SHA-256 fact commands used `timeout 30`, a clean environment, and `prlimit --as=4000000000 --core=0 -- sha256sum` on the paths named above. The counter runs used the contract's memory-limit exception. Hyprland was started only through the frozen counter/oracle; no live-compositor commands or DRM card nodes were used. All subprocess calls completed; the oracle's `finally` cleanup terminates and waits for its nested process groups. No persistent processes were started. No other checks were run.

## v2 re-score — unchanged control

CONTROL K1DoNothing v2 best: PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED — not met

L1 retired v1 before data and assigned this re-score under `count-v2.py`. The historical v1 receipts above remain unchanged. This follow-up made no control mutation: both v2 runs used the original 12-byte file, SHA-256 `a3381e95441354d833917bdaf481a5b210edf2b8cda6419b5e1805dfe143fd3b`, confirmed before and after both scores. No empty-file rerun was requested or performed under v2.

The v2 detector still requires 41/41 exact ordered arrays, now using type-strict canonical JSON comparison and cases with unsourced decoys, nested/glob sources, interleaved source lines, and variable redefinition. The two independent scores ran concurrently, each with six jobs, through the frozen oracle's host-wide slot controls. Both invocations used this exact command with the lane as their working directory and a clean outer environment:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v2.py a4dc0da0 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1DoNothing.py --jobs 6
```

| Run | Fresh seed | Exact PRED output | Process exit | Verbatim stdout receipt |
| --- | --- | --- | --- | --- |
| v2 seed 1 | `cb4c12390d0e37b7` | `PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/v2/K1DoNothing-seed1.txt` |
| v2 seed 2 | `85d747e99df79cb3` | `PRED-C1-r27-v2 cases_pass=1/41 verdict=TARGET_MISSED` | 1 | `.ufo/waves/round-27/controls/v2/K1DoNothing-seed2.txt` |

Both runs passed only BASE (`rules=0`) and failed all 40 generated cases (`rules got=0 want=N first_diff=0`, with positive N). Both printed `exit=1`; stderr was empty. Neither exited 2, so no guard retry was needed. Each receipt identifies revision `a4dc0da0394a71badf506e9c72144cd1b8ca7281`, the same 79-file snapshot and oracle commit recorded above, and two agreeing BASE oracle runs.

Before/after hashes matched:

- Unchanged control: `a3381e95441354d833917bdaf481a5b210edf2b8cda6419b5e1805dfe143fd3b`.
- Frozen v2 counter: `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87`.
- Frozen harness: `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`.

Receipt SHA-256 values:

- `controls/v2/K1DoNothing-seed1.txt` (5,790 bytes): `9114508f636013131077a982b6b5d82e47b52683edd82f05cae15e502e9eb94d`.
- `controls/v2/K1DoNothing-seed2.txt` (5,737 bytes): `6bfb13cc61b4754313e041563749cb3821f8bd38c548d5bb12a910f9b6b0f454`.

Repeated the bounded clean-environment coredump listing command from the host-safety section immediately before and after these two scores. Both listings exited 0 with empty stderr: **1338 before, 1338 after, delta 0**. Each v2 receipt also prints `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`. All score subprocesses completed, and oracle cleanup handles its nested process groups. No persistent processes, installations, additional mutations, or unrelated checks were introduced.
