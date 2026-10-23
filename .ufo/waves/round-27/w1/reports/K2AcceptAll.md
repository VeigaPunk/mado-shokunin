# K2AcceptAll — C2 ACCEPT-ALL control

## Verdict
CONTROL K2AcceptAll best: PRED-C2-r27 green=8/8 w_killed=0/15 h_killed=0/0 h_need=0 h_valid=0 h_invalid=0 verdict=TARGET_MISSED — not met

Both fresh-seed runs produced that exact PRED line and `exit=1`. All 8 green cases passed; all 15 W mutants survived in each run. Neither run was inconclusive or exit 2. No held-out set was supplied or inspected; this is the required W-first control measurement, not a held-out result.

## Control and expected detector

Axes: shape fidelity, detector discrimination, reproducibility, host safety.

Read the round-27 registration before acting, the godspeed skill, and the workstation tooling rules. Created only the assigned two control suites, the two receipts, and this report. No data-seat tool or suite was implemented.

- `.ufo/waves/round-27/controls/K2AcceptAll-suite-a.py`
- `.ufo/waves/round-27/controls/K2AcceptAll-suite-b.py`

Both files contain exactly these 43 bytes, including the final newline:

```python
#!/usr/bin/env python3
raise SystemExit(0)
```

The control always accepts, ignores all supplied arguments, and never opens or executes a subject. The expected detector is the frozen round-27 C2 counter: green runs pass, no mutant is killed, and the target is missed. Observed output matches that expectation. Mutant survival describes this deliberately empty control's coverage only; it does not change the contract.

## Exact scoring commands

The independent runs were launched concurrently; each used six jobs and a newly generated hexadecimal seed. Environment variables were cleared, including compositor and Git override variables.

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2AcceptAll-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2AcceptAll-suite-b.py --seed 4a9dd77647d9133a --jobs 6
cd /home/vgpnk/Projects/shokunin/mado-shokunin && env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2AcceptAll-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2AcceptAll-suite-b.py --seed a653807c814780e3 --jobs 6
```

Both resolved REV to `5ddc5885188a1de8606464526d636c9e2fc433e6`. Every case returned suite `rc=0`; the counter returned 1, with empty stderr. There was no exit-2 run requiring repetition.

Verbatim stdout, including `exit=1`, is saved at:

| Receipt | Bytes | SHA-256 |
| --- | ---: | --- |
| `.ufo/waves/round-27/controls/K2AcceptAll-seed1.txt` | 2993 | `e75cea2370a9bf6aea88f575c542404766c2b0211b7d9ab75d533473c721620b` |
| `.ufo/waves/round-27/controls/K2AcceptAll-seed2.txt` | 2993 | `3a12e2e89872995d17639a4b05b8cf2645de05703e8889cfc7d59b170cfc4106` |

Both receipt byte strings were compared with the captured subprocess stdout and matched exactly.

## Preservation and restoration evidence

The frozen detector applies its W edits only in disposable fresh clones under `/fast/scratch/hyaku/mado-r27/c2`. Its `finally` blocks remove each clone and the run parent (`c2/count.py:93-94,189-190`). Both counter processes completed. No subject was edited in the lane; no lane restoration was necessary.

Python `hashlib.sha256(path.read_bytes()).hexdigest()` recorded the following identical before/after hashes:

| Path | SHA-256 before = after |
| --- | --- |
| `.ufo/waves/round-27/c2/count.py` | `2e180ed29c31abcb3421d7e57a147d05ac9d2982ebe4dbc555747b287e754dc7` |
| `.ufo/waves/round-27/c2/mutants-w.json` | `0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608` |
| `.ufo/waves/round-26/c1/count-v2.py` | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` |
| `.ufo/waves/round-26/c2/count.py` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` |
| `.ufo/waves/round-26/quality/check-population.py` | `803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64` |
| `.ufo/waves/round-27/harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |
| `.ufo/waves/round-27/controls/K2AcceptAll-suite-a.py` | `29453a6f2fb8c3e5f0e6fefb688ae00cbc5d2d36d2eb762112a1553e33167ae0` |
| `.ufo/waves/round-27/controls/K2AcceptAll-suite-b.py` | `29453a6f2fb8c3e5f0e6fefb688ae00cbc5d2d36d2eb762112a1553e33167ae0` |

The counter and oracle hashes match their frozen pins. No counter, harness, W-set, subject, or sibling file was changed. Git writes were confined to the counter's scratch clones.

## Host safety and tooling

Before scoring:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 --core=0 -- df -h /fast
```

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  689G  115G  86% /fast
```

Before and after scoring:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
```

Both calls returned 0 with empty stderr. Counting stdout lines containing `/usr/bin/Hyprland` gave:

```text
HOST_SAFETY Hyprland_before=1338 Hyprland_after=1338 delta=0 launched_by_control=0
```

No compositor, subject runtime, host service, network fetch, or live-compositor command was invoked by either suite. All started counter processes returned; there are no retained background jobs. No tools were installed or updated. No additional tests or builds were run.
