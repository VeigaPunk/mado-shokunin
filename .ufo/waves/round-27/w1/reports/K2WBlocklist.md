# K2WBlocklist — C2 source-only control

## Verdict
CONTROL K2WBlocklist best: PRED-C2-r27 green=3/8 w_killed=15/15 h_killed=0/0 h_need=0 h_valid=0 h_invalid=0 verdict=TARGET_MISSED — not met

Both fresh seeds produced that exact PRED line and `exit=1`. This W-only control fails the green requirement independently of the absent held-out set. No held-out files were read or scored. No exit-2 run occurred.

## What was implemented

Axes: shape fidelity, green/W discrimination, and reproducible host-safe execution.

Created only the two assigned control suites, their two receipts, and this report:

- `.ufo/waves/round-27/controls/K2WBlocklist-suite-a.py`
- `.ufo/waves/round-27/controls/K2WBlocklist-suite-b.py`
- `.ufo/waves/round-27/controls/K2WBlocklist-seed1.txt`
- `.ufo/waves/round-27/controls/K2WBlocklist-seed2.txt`

The single-file Python-stdlib suites embed the complete relevant W patterns from the frozen JSON, scoped to each mutant's subject. Suite A accepts `--c1`, `--c2`, and `--rev`; suite B accepts `--checker`. They read subject bytes without importing or executing the subjects. Each exits 1 on literal containment of any nonempty `new` pattern, or absence of the complete `old` pattern for a deletion mutant; otherwise it exits 0. There is no behavioral check, AST comparison, pristine hash gate, or held-out knowledge. `--rev` is accepted but does not affect the decision.

The literal substring rule has an unavoidable false positive for suite A: W mutant `c1-drop-bezier` has `new = "ok = gn == en"`, already contained in the pristine line `ok = gn == en and gb == eb` at `.ufo/waves/round-26/c1/count-v2.py:359`. Consequently all five A green cases fail with `W-BLOCKLIST reject c1 c1-drop-bezier`. No old-text exception or statement-boundary matching was added, because either would change the assigned containment rule.

## Observed detector output

The detector was the unchanged frozen round-27 C2 counter, with both suites injected into its disposable scratch clones.

| Seed | Green | Counter W tally | Held-out | Counter exit |
| --- | --- | --- | --- | --- |
| `79f9325e2291869b` | 3/8 | 15/15 | 0 valid, not supplied | 1 |
| `4cb85bb3d3352a21` | 3/8 | 15/15 | 0 valid, not supplied | 1 |

Both complete stdout streams, including `exit=1`, are saved verbatim in the receipt paths above. The counter reports no W survivors. Suite B's pristine and two benign cases pass, and each of its six W cases exits 1 with the corresponding blocklist ID, including the deletion mutant.

The nine A cases labeled `KILLED` by the frozen counter are **inconclusive as mutation-discrimination evidence**, because A also fails pristine. They are reported as the counter's actual tally, not as nine demonstrated behavioral kills. B's six W detections are source-signature detections, not behavioral validation.

## Exact scoring commands

Both commands ran with working directory `/home/vgpnk/Projects/shokunin/mado-shokunin`. Seeds were freshly selected using Python `secrets.token_hex(8)` twice. The two scores ran concurrently; each counter used six workers.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2WBlocklist-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2WBlocklist-suite-b.py --seed 79f9325e2291869b --jobs 6
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2WBlocklist-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2WBlocklist-suite-b.py --seed 4cb85bb3d3352a21 --jobs 6
```

Both resolved revision `5ddc5885188a1de8606464526d636c9e2fc433e6`.

## Byte preservation and restoration evidence

No lane subject, counter, harness, or W-set bytes were edited. Mutations were applied only by the frozen counter in its disposable scratch clones. Its `run_suite` cleanup removes each clone in `finally`; no manual source restoration was needed. Both scoring runs independently loaded identical pristine subject hashes and repeated identical pristine results. Separate before/after SHA-256 commands also observed the following unchanged lane bytes:

| Path | Before SHA-256 = after SHA-256 |
| --- | --- |
| `.ufo/waves/round-27/c2/count.py` | `2e180ed29c31abcb3421d7e57a147d05ac9d2982ebe4dbc555747b287e754dc7` |
| `.ufo/waves/round-27/c2/mutants-w.json` | `0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608` |
| `.ufo/waves/round-26/c1/count-v2.py` | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` |
| `.ufo/waves/round-26/c2/count.py` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` |
| `.ufo/waves/round-26/quality/check-population.py` | `803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64` |

Both receipts' suite hashes agree with the final SHA-256 command:

- A: `dbc34f3ae7f19bfe10cc9923b63883b115aaf8b4e35f461e1245b1351b477d6c`
- B: `ae38ee85014933d80ae87482512f0f9f39a7ede992f43325da4d24d4af0382b1`

The before command was:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c2/count.py .ufo/waves/round-27/c2/mutants-w.json .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/c2/count.py .ufo/waves/round-26/quality/check-population.py
```

The after command was:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c2/count.py .ufo/waves/round-27/c2/mutants-w.json .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/c2/count.py .ufo/waves/round-26/quality/check-population.py .ufo/waves/round-27/controls/K2WBlocklist-suite-a.py .ufo/waves/round-27/controls/K2WBlocklist-suite-b.py
```

## Host safety

No Hyprland, hyprctl, oracle, subject program, additional runtime, host service, or package installation was invoked by these suites. No git/jj write command was issued in the lane; the counter performed its own sandbox clone operations. All started commands completed. The source-only suites start no child processes.

Before scoring:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 -- df -h /fast
```

Output:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  690G  114G  86% /fast
```

Coredump baseline command:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 -- coredumpctl list --no-pager --no-legend
```

Its complete captured output (`artifact://30381`, read with bounded selector `:raw:1-2000`) contained 1338 lines including `/usr/bin/Hyprland`, counted in Python without rerunning the baseline command. The final equivalent executable-filtered count was:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 -- coredumpctl list --no-pager --no-legend /usr/bin/Hyprland | env -i PATH=/usr/bin HOME=/home/vgpnk timeout 30 prlimit --as=4000000000 -- wc -l
```

Output: `1338`.

`HOST_SAFETY Hyprland_coredumps_before=1338 after=1338 delta=0; Hyprland_processes_started_by_this_control=0`.

Tool installs or updates: none. No additional build, lint, formatter, or behavioral test was run.

## L1 follow-up — K2WBlocklistExact

### Verdict
CONTROL K2WBlocklistExact best: PRED-C2-r27 green=8/8 w_killed=15/15 h_killed=0/0 h_need=0 h_valid=0 h_invalid=0 verdict=TARGET_MISSED — not met

**Both seeds satisfy every green and W criterion. TARGET_MISSED is solely because `h_valid=0`, below the required minimum of 6.** No held-out directory was supplied, read, or scored. This is the strongest tested W-blocklist variant and supersedes the original substring variant's 3/8 green result; the original evidence above is retained unchanged.

### Exact-byte implementation and detector

Created the requested second pair:

- `.ufo/waves/round-27/controls/K2WBlocklistExact-suite-a.py`
- `.ufo/waves/round-27/controls/K2WBlocklistExact-suite-b.py`

Both load `.ufo/waves/round-27/c2/mutants-w.json` from their clone at runtime. They obtain pristine committed subject bytes using read-only `git show`: suite A uses its supplied `--rev`; suite B uses the fresh clone's `HEAD`, because its CLI has no revision argument. For every W entry belonging to the given subject, they require exactly one occurrence of `old`, compute `pristine.replace(old, new, 1)`, and reject only when the subject's full bytes equal that complete mutant. Deletion mutants use the same replacement operation. Otherwise they accept.

They neither execute nor import a subject and perform no behavioral check. The Git source-read subprocesses use a cleared environment, 30-second timeout, 4 GB address-space cap, and core limit 0. Unlike the original variant, these suites do start bounded read-only Git subprocesses.

The unchanged frozen C2 detector observed:

| Seed | Green | W killed | Held-out valid | Verdict | Exit |
| --- | --- | --- | --- | --- | --- |
| `23baf5da57b126d2` | 8/8 | 15/15 | 0 | TARGET_MISSED | 1 |
| `ba39bbf3e8ae73d5` | 8/8 | 15/15 | 0 | TARGET_MISSED | 1 |

Each pristine and benign case prints `W-BLOCKLIST-EXACT accept` and exits 0. Each W case prints its corresponding mutant ID and exits 1. All 15 counter-reported kills therefore have passing pristine baselines in this variant; there are no W survivors or baseline-failure ambiguities. These remain exact source-identity detections, not behavioral tests. No exit-2 run occurred.

Complete counter stdout, including `exit=1`, is preserved verbatim at:

- `.ufo/waves/round-27/controls/K2WBlocklistExact-seed1.txt`
- `.ufo/waves/round-27/controls/K2WBlocklistExact-seed2.txt`

### Exact scoring commands

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Both fresh seeds were generated with `secrets.token_hex(8)`. The scores ran concurrently.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2WBlocklistExact-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2WBlocklistExact-suite-b.py --seed 23baf5da57b126d2 --jobs 6
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2WBlocklistExact-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2WBlocklistExact-suite-b.py --seed ba39bbf3e8ae73d5 --jobs 6
```

The runtime W source's existence in the scored commit was established before implementation with:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 -- git cat-file -e 5ddc5885:.ufo/waves/round-27/c2/mutants-w.json
```

It exited successfully without output.

### Preservation and safety

Before the follow-up, the same five-input SHA-256 command recorded under “Byte preservation and restoration evidence” was run again. After scoring, this command recorded the same five protected-input hashes plus the new suite hashes:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 -- sha256sum .ufo/waves/round-27/c2/count.py .ufo/waves/round-27/c2/mutants-w.json .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/c2/count.py .ufo/waves/round-26/quality/check-population.py .ufo/waves/round-27/controls/K2WBlocklistExact-suite-a.py .ufo/waves/round-27/controls/K2WBlocklistExact-suite-b.py
```

All five before/after hashes exactly equal the earlier table. Both receipts and the final command agree on the exact-suite hashes:

- A: `422880dd574e90556c8ab21f9b753378cd44037a69f84fec7173e23c07c7915b`
- B: `a59744733e0684d19983914bce83518764932edcf009e06d19779f38bb2adf13`

No lane subject, counter, harness, or W-set bytes were changed. Mutation application and disposal remained the frozen counter's responsibility in per-case scratch clones; no in-place restoration or restored-clone rerun was performed. The suites only read subject and repository bytes. No git/jj write command was issued in the lane.

The same bounded `df -h /fast` command shown above was rerun before scoring and again reported 114 GB available. The executable-filtered coredump-count command shown above was run before and after the follow-up; both outputs were `1338`.

`HOST_SAFETY exact_followup_Hyprland_coredumps_before=1338 after=1338 delta=0; Hyprland_processes_started_by_this_control=0`.

All started commands completed; the suites' bounded Git children were waited for. No Hyprland, hyprctl, oracle, subject program, host service, additional runtime, tool installation, or tool update was invoked. No build, lint, formatter, or extra behavioral test was run.
