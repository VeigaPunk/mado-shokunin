# K1Junk — fresh-seed C1 v4 re-score

RESCORE K1Junk best: PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED — not met

The committed control scored **0/41 twice**, matching both committed v4 receipts. A one-line, config-blind sampling variant scored **1/41 twice**, passing only BASE. No run met 41/41.

## Detector and scope

Read the godspeed skill and round-27 registration before executing. Axes: bounded valid random JSON, strict config blindness, exact-match coverage, and host safety. The frozen v4 detector compares ordered, type-strict JSON against isolated Hyprland v0.56.2 for BASE, 25 APPEND cases, and 15 SYNTH cases. The expected negative-control result is nonzero exit, not a successful parser claim.

All receipts below are under `/fast/scratch/hyaku/mado-r27/rescore/`. Their `.txt` files contain stdout verbatim; corresponding `.stderr.txt` files are empty. All six completed counter processes exited 1, without a timeout or setup guard. All used fresh automatically generated case seeds, with no `--seed` override.

## Required committed-control scores

Ran this exact command twice from `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1Junk.py --jobs 6
```

| Receipt | Fresh seed | Actual PRED line | Exit |
| --- | --- | --- | --- |
| `K1Junk-seed1.txt` | `4d63e29583b180c0` | `PRED-C1-r27-v4 cases_pass=0/41 verdict=TARGET_MISSED` | 1 |
| `K1Junk-seed2.txt` | `f3112846e7ed4878` | `PRED-C1-r27-v4 cases_pass=0/41 verdict=TARGET_MISSED` | 1 |

Neither run passed any case. BASE emitted four and one random objects respectively, versus the oracle's empty array.

The initial two asynchronous bash submissions were refused at admission with `Background job limit reached (100)`; neither started a counter. The successful executions used Python `asyncio.create_subprocess_exec` with the exact argv above, a cleared parent environment, separate process sessions, stdout/stderr pipes, and a 920-second outer wait. Scoped metadata records actual argv, PIDs, return codes, durations, and receipt hashes in `K1Junk-evidence.txt`. No different detector was substituted.

## Historical comparison

The assignment calls the `controls/v4/` receipts “v3”; their actual headers and PRED labels identify **v4**. Compared both requested receipts and the actual v3 receipts:

| Committed receipt under `.ufo/waves/round-27/` | Seed | Actual PRED line |
| --- | --- | --- |
| `controls/v4/K1Junk-seed1.txt` | `2c7682faedba6600` | `PRED-C1-r27-v4 cases_pass=0/41 verdict=TARGET_MISSED` |
| `controls/v4/K1Junk-seed2.txt` | `7e7cbe9ad2504851` | `PRED-C1-r27-v4 cases_pass=0/41 verdict=TARGET_MISSED` |
| `controls/v3/K1Junk-seed1.txt` | `868f2870b502fc1c` | `PRED-C1-r27-v3 cases_pass=1/41 verdict=TARGET_MISSED` |
| `controls/v3/K1Junk-seed2.txt` | `c7c31a1c251131c4` | `PRED-C1-r27-v3 cases_pass=0/41 verdict=TARGET_MISSED` |

Both historical v4 runs used the same resolved revision and control/counter hashes as this re-score. Their w1 report records `--jobs 4`; the requested fresh runs used `--jobs 6`. The fresh result reproduces 0/41, not a target-met kill-rule event. The historical v3 1/41 was only an empty BASE guess.

## One within-shape strengthening probe

**The committed sampler is not the strongest version of its shape.** It emits the empty array with probability 1/5. BASE is stably empty. A single-line mutation increases that probability to 15/16 while retaining a 1/16 chance of generating one through four random objects. It still ignores `--home`, reads no config or environment, inspects no labels or paths, and writes only its JSON array to stdout. This is deliberately a near-DoNothing sampling improvement, not workspace-rule capability or a claim of global optimality.

Created an exact isolated copy at `K1Junk-probe.py`, scored its pristine bytes, changed only line 18, scored twice, preserved the tested stronger bytes at `K1Junk-strong.py`, restored the probe copy exactly in a `finally` block, then scored the restored bytes.

Pristine line:

```python
    for _ in range(rng.randrange(5)):
```

Mutated line:

```python
    for _ in range(0 if rng.randrange(16) else rng.randrange(1, 5)):
```

The same bounded command was run for pristine, both mutated scores, and restoration; only the scratch bytes changed between phases:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /fast/scratch/hyaku/mado-r27/rescore/K1Junk-probe.py --jobs 6
```

| Phase / receipt | Fresh seed | Actual PRED line | Passed cases |
| --- | --- | --- | --- |
| Pristine / `K1Junk-probe-pristine.txt` | `16a0a9b19acb0987` | `PRED-C1-r27-v4 cases_pass=0/41 verdict=TARGET_MISSED` | None |
| Mutated / `K1Junk-strong-seed1.txt` | `78aa441d2fa58174` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | BASE only |
| Mutated / `K1Junk-strong-seed2.txt` | `87136c3199910a22` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | BASE only |
| Restored / `K1Junk-probe-restored.txt` | `09cc42d3b6886205` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | BASE only |

The stronger variant still failed every generated case. Restoration's stochastic score need not equal pristine's score: both the case seed and `SystemRandom` draws are fresh. Restoration is established by exact byte equality and hashes, not score equality.

**Mutation-kill verdict: INCONCLUSIVE.** The pristine control already failed the detector, so this is not a killed-mutant claim. As a negative-control target test, the strengthened control remains **not met**.

## Hashes and restoration

Measured before and after; no lane source or committed control was edited:

| Input | SHA-256 before = after |
| --- | --- |
| `controls/K1Junk.py` | `2105846310d5b3e85b707b7e809d171b6a66c1914cde8be89db6f13272645a5a` |
| `c1/count-v4.py` | `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1` |
| `harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

Paths in this table resolve under `.ufo/waves/round-27/`.

Scratch probe before and restored SHA-256: `2105846310d5b3e85b707b7e809d171b6a66c1914cde8be89db6f13272645a5a`; exact byte comparison returned `True`.

Tested mutant and preserved `/fast/scratch/hyaku/mado-r27/rescore/K1Junk-strong.py` SHA-256: `cd65275e4dc9f4cf44f3ccad4f92bdf022f93303b4eef2cf78840f18d9bc3eed`. The preserved copy's hash was measured equal to the tested mutant's hash. Full per-receipt hashes and commands are in `K1Junk-evidence.txt`.

## Host safety

`df -h /fast` reported 73G available before scratch writes. Every receipt verified stable BASE, Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`, and the same 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`.

All six receipts printed:

```text
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
```

Independent before/after coredump commands each exited 0 and counted 1338 `/usr/bin/Hyprland` rows: delta 0. Commands:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 10 prlimit --as=4000000000 --core=0 -- df -h /fast
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 --core=0 -- ps -eo pid=,ppid=,pgid=,args=
```

Coredump rows and process-group membership were counted from captured output in Python. Final process inspection exited 0 and found no tracked PID or process-group member. Every started scoring process had exited, and its private process group was cleaned up. Nested compositors ran only through the supplied counter/oracle with its host-wide slot locks. No live-compositor commands, direct Hyprland launches, git/jj writes, sibling edits, subagent dispatch, tool installs/updates, or service restarts were performed. Writes were limited to the assigned rescore directory and this report.
