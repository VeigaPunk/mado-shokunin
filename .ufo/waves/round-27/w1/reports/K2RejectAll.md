# K2RejectAll — C2 REJECT-ALL control

## Verdict
CONTROL K2RejectAll best: PRED-C2-r27 green=0/8 w_killed=15/15 h_killed=0/0 h_need=0 h_valid=0 h_invalid=0 verdict=TARGET_MISSED — not met

Both seeds produced this exact PRED line and `exit=1`; both subprocess return codes were 1, with empty stderr. No exit-2 retry was needed. The control fails all eight green cases, so rejecting every mutant does not meet C2. No held-out files were read or scored.

## Control and expected detector

Created only the two authorized suite files, each containing:

```python
#!/usr/bin/env python3
raise SystemExit(1)
```

- `.ufo/waves/round-27/controls/K2RejectAll-suite-a.py`
- `.ufo/waves/round-27/controls/K2RejectAll-suite-b.py`

This is unconditional rejection: it ignores arguments and subject contents. The expected frozen-counter result is failure on every pristine/benign green run and a mechanical KILLED label on every W mutant. Observed on both seeds: all 8 GREEN cases had `rc=1 FAIL`; all 15 W cases had `rc=1 KILLED`. Because pristine baselines also fail, those KILLED labels are not evidence of useful mutation detection.

## Exact scoring commands and receipts

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`. The two commands ran concurrently, each with six jobs, a fresh seed, cleared environment, and its own process group. Git environment overrides were absent. The frozen counter bounds each suite to 300 seconds, 4 GB address space and zero core size.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2RejectAll-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2RejectAll-suite-b.py --seed 672c76c3b2c699d6 --jobs 6

env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2RejectAll-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2RejectAll-suite-b.py --seed c72b9393c704d4fc --jobs 6
```

Resolved revision: `5ddc5885188a1de8606464526d636c9e2fc433e6`.

Verbatim stdout, including the counter's final `exit=1`, is saved without wrapper text:

| Receipt | Bytes | SHA-256 |
| --- | ---: | --- |
| `.ufo/waves/round-27/controls/K2RejectAll-seed1.txt` | 2964 | `364d2544af8c8767b28282eb9c01947e689957a0a74e14764ad5d71a02d3d5da` |
| `.ufo/waves/round-27/controls/K2RejectAll-seed2.txt` | 2964 | `7e31ae57a1ae3d293370a67ec358c8cbf9a5e23c8bd893e8a649617aa0c772c7` |

## Byte preservation and restoration evidence

No lane subject, counter, W set or production suite was edited. Suite overrides and subject mutations were applied only by the frozen counter in its disposable clones under `/fast/scratch/hyaku/mado-r27/c2`; the counter's normal-return cleanup removes those clones. There were no original lane bytes to restore. The control files remain as the required artifacts.

The following hashes were measured with `sha256sum` before and after both runs and were identical:

| Path | Before = after SHA-256 |
| --- | --- |
| `.ufo/waves/round-27/controls/K2RejectAll-suite-a.py` | `cfe5ad0a62984338e1526d826a7003217899f7dcd59f7c87a1be30581372ede3` |
| `.ufo/waves/round-27/controls/K2RejectAll-suite-b.py` | `cfe5ad0a62984338e1526d826a7003217899f7dcd59f7c87a1be30581372ede3` |
| `.ufo/waves/round-27/c2/count.py` | `2e180ed29c31abcb3421d7e57a147d05ac9d2982ebe4dbc555747b287e754dc7` |
| `.ufo/waves/round-27/c2/mutants-w.json` | `0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608` |
| `.ufo/waves/round-26/c1/count-v2.py` | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` |
| `.ufo/waves/round-26/c2/count.py` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` |
| `.ufo/waves/round-26/quality/check-population.py` | `803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64` |

## Host safety and tooling

Before scoring:

```sh
env -i PATH=/usr/bin timeout 30 prlimit --as=4000000000 -- df -h /fast
```

Output:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  689G  115G  86% /fast
```

Before and after scoring, ran:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
```

Counted output lines containing `/usr/bin/Hyprland` in Python. Both calls returned 0 with empty stderr.

```text
HOST_SAFETY Hyprland_coredumps_before=1338 after=1338 delta=0
```

The reject-all suites launch no processes and do not start Hyprland or contact the live compositor. Both counter process groups were cleaned in `finally` with SIGKILL if still present. No host services were changed, no git/jj write commands were issued in the lane, and no tools were installed or updated.

## v2 re-score

CONTROL K2RejectAll v2 best: PRED-C2-r27-v2 green=0/8 b_valid=0 w_killed=15/15 h_killed=0/0 h_need=0 h_valid=0 h_min_per_subject=0 invalid=0 verdict=TARGET_MISSED — not met

Re-scored the unchanged control after L1 retired counter v1 before data. The earlier v1 receipts remain historical evidence. Both v2 seeds produced the exact PRED line above and `exit=1`; both subprocess return codes were 1 with empty stderr. No exit-2 retry was needed. All 8 GREEN cases again had `rc=1 FAIL`, while all 15 W cases had `rc=1 KILLED`. Failing pristine subjects makes these mechanical kills inconclusive as evidence of meaningful mutation detection; the control does not meet C2.

No `--heldout` was supplied, as assigned. No sealed files were read; `b_valid=0` and `h_valid=0` are not held-out measurements.

### Exact v2 commands and receipts

Working directory was the lane root. These two commands ran concurrently with fresh seeds and separate process groups:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count-v2.py a4dc0da0 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2RejectAll-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2RejectAll-suite-b.py --seed fca0273ee5f372d1 --jobs 6

env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count-v2.py a4dc0da0 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2RejectAll-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2RejectAll-suite-b.py --seed b8c9a71beaa5e2ee --jobs 6
```

Resolved revision: `a4dc0da0394a71badf506e9c72144cd1b8ca7281`.

Each receipt contains verbatim stdout, including the final `exit=1`, without wrapper text:

| Receipt | Bytes | SHA-256 |
| --- | ---: | --- |
| `.ufo/waves/round-27/controls/v2/K2RejectAll-seed1.txt` | 2998 | `a0bac7c8cb21555ca18a1812dc4474d9670c8f09715cc4913d2a298be4c61095` |
| `.ufo/waves/round-27/controls/v2/K2RejectAll-seed2.txt` | 2998 | `658da5a406f8b133011a55c0743526fa79cc8604c8af1f348ba4777b0fdb5116` |

### v2 preservation and host safety

Pre/post `sha256sum` measurements showed both control suites, the W set and all three round-26 subjects unchanged at the hashes already listed above. Both suite files still have SHA-256 `cfe5ad0a62984338e1526d826a7003217899f7dcd59f7c87a1be30581372ede3`. The v2 counter was also unchanged before/after, matching L1's pin: `4dfb34b5551a908aa7fd56e75526417b43659018c47fa5993ad39a72b6b109d3`.

The frozen v2 counter uses no-local clones under `/fast/scratch/hyaku/mado-r27/c2v2`, per-run directories, shuffled execution and bubblewrap isolation. It removes disposable clones in normal-return cleanup. No lane bytes were overwritten or needed restoration. Counter process groups were cleaned in `finally` with SIGKILL if still present.

The same bounded, cleared-environment `df` command, now also using `--core=0`, reported:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  691G  113G  87% /fast
```

The same bounded coredump command and Python line-count method were run before and after v2 scoring. Both calls returned 0 with empty stderr:

```text
HOST_SAFETY v2 Hyprland_coredumps_before=1338 after=1338 delta=0
```

No Hyprland instance was started, no live compositor commands were used, no host services were changed, and no tools were installed or updated.

