# K2ShaPin — C2 SHA-PIN control

## Verdict
CONTROL K2ShaPin best: PRED-C2-r27 green=2/8 w_killed=15/15 h_killed=0/0 h_need=0 h_valid=0 h_invalid=0 verdict=TARGET_MISSED — not met

Both fresh-seed runs returned `exit=1` and the identical PRED line above. The pristine A and B runs passed (`rc=0`); all six behaviour-preserving comment/unused-assignment runs failed (`rc=1`). All 15 W mutants were KILLED (`rc=1`). No held-out set was supplied or read: H is unmeasured, not passed. Independently of H, rejecting six green cases prevents this control from meeting C2.

## Implementation and expected detector

Axes: shape fidelity, frozen-counter discrimination, exact source preservation, desktop safety.

Wrote only the assigned control suites, two receipts, and this report:

- `.ufo/waves/round-27/controls/K2ShaPin-suite-a.py`, SHA-256 `3f41b8c6cbeb3c9017ac05684120b41895144f0c5606ba8bb8e512938e65453c`.
- `.ufo/waves/round-27/controls/K2ShaPin-suite-b.py`, SHA-256 `4478cdb9a5b814edb98451719e0cde5c57db9e33f8d142f4166a9c3f202b6381`.

Suite A accepts `--c1`, `--c2`, and `--rev`; suite B accepts `--checker`. Each hashes only its supplied subject file(s), prints `SHA_PIN PASS` and exits 0 exactly when all subject bytes match their pristine pins; mismatches/unreadable files print `SHA_PIN FAIL` and exit 1. Neither suite imports or executes a subject, invokes a process, or runs a behavioural check. `--rev` is accepted but does not change the pins.

Pins came from the counter's `SUBJECT` lines in `.ufo/waves/round-27/evidence/c2-before-543f0445.txt:2-4`. Read-only `git show` hash commands established that the three subjects at `5ddc5885` have the same pins; both new receipts independently print those same `SUBJECT` lines for full revision `5ddc5885188a1de8606464526d636c9e2fc433e6`.

Expected detector: the frozen C2 counter must reject SHA-PIN despite killing every changed-byte W mutant, because it must also accept the six byte-changing, behaviour-preserving green edits. The observed outputs match that expectation; no behavioural coverage is claimed from the W kills.

## Exact scoring commands and receipts

Working directory for every command below: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ShaPin-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ShaPin-suite-b.py --seed b08b085dae235fb7 --jobs 6
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ShaPin-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ShaPin-suite-b.py --seed 387432d12cba988a --jobs 6
```

Executed concurrently, with independent fresh random seeds and cleared subprocess environments. Captured merged stdout/stderr without modification and saved the full receipts, including `exit=1`, to:

- `.ufo/waves/round-27/controls/K2ShaPin-seed1.txt`
- `.ufo/waves/round-27/controls/K2ShaPin-seed2.txt`

Each receipt records the counter hash, full revision, W-set hash, subject hashes, suite hashes, every individual case outcome, PRED line, and exit line. Both OS process return codes were also 1. Neither run exited 2; no retry was needed.

## Preservation and restoration evidence

No lane subject, counter, harness, W-set, or production suite was edited. The counter applied its W/benign edits only in its disposable fresh scratch clones, not in the lane. The control assignment required no additional persistent subject mutation or restoration. Before and after both runs, the following exact hash command produced the identical output shown:

```sh
env -i PATH=/usr/bin timeout 15 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/c2/count.py .ufo/waves/round-27/c2/mutants-w.json .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/c2/count.py .ufo/waves/round-26/quality/check-population.py
```

```text
2e180ed29c31abcb3421d7e57a147d05ac9d2982ebe4dbc555747b287e754dc7  .ufo/waves/round-27/c2/count.py
0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608  .ufo/waves/round-27/c2/mutants-w.json
4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428  .ufo/waves/round-26/c1/count-v2.py
b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8  .ufo/waves/round-26/c2/count.py
803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64  .ufo/waves/round-26/quality/check-population.py
```

Additional read-only pin commands, with the matching outputs above:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- git show 5ddc5885:.ufo/waves/round-26/c1/count-v2.py | sha256sum
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- git show 5ddc5885:.ufo/waves/round-26/c2/count.py | sha256sum
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- git show 5ddc5885:.ufo/waves/round-26/quality/check-population.py | sha256sum
```

## Host safety and tooling

Before writing the controls:

```sh
env -i PATH=/usr/bin timeout 15 prlimit --as=4000000000 --core=0 -- df -h /fast
```

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  689G  115G  86% /fast
```

Before and after the two scores:

```sh
env -i PATH=/usr/bin timeout 20 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend | /usr/bin/grep -c /usr/bin/Hyprland
```

Both outputs were `1338`; Hyprland coredump delta = **0**. The SHA-only suites never started Hyprland or hyprctl. No compositor/environment identifiers were supplied. Counter-run limits are the frozen counter's own; ancillary commands used the 4 GB/core-0 cap. Scorers ran in separate process groups with a final SIGKILL group sweep after completion. No host service was started/restarted. No git/jj write commands were issued in the lane or fleet repository. No other held-out files were read, no subagents were dispatched, and no tools were installed or updated.

## C2 counter v2 re-score

CONTROL K2ShaPin v2 best: PRED-C2-r27-v2 green=2/8 b_valid=0 w_killed=15/15 h_killed=0/0 h_need=0 h_valid=0 h_min_per_subject=0 invalid=0 verdict=TARGET_MISSED — not met

At L1's direction, re-scored the **unchanged** suites against the replacement frozen counter, SHA-256 `4dfb34b5551a908aa7fd56e75526417b43659018c47fa5993ad39a72b6b109d3`, at full revision `a4dc0da0394a71badf506e9c72144cd1b8ca7281`. The preceding v1 results remain historical, not the current counter result.

Both v2 runs again passed the two pristine cases, rejected all six public benign edits, and killed all 15 W mutants. All failures/kills reported `rc=1 | SHA_PIN FAIL`; pristine cases reported `rc=0 | SHA_PIN PASS`. Both PRED lines are identical to the line above. Each process returned 1 and printed `exit=1`; there were no exit-2 runs or retries. The expected detector still rejects this byte-identity control because of the six benign false rejections. No behavioural checks were added.

Exact commands, run concurrently from the same lane directory with two new random seeds:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count-v2.py a4dc0da0 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ShaPin-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ShaPin-suite-b.py --seed ae15ca7921d6ab90 --jobs 6
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count-v2.py a4dc0da0 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ShaPin-suite-a.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2ShaPin-suite-b.py --seed b9be4979deaddd09 --jobs 6
```

Verbatim full receipts, including the PRED and exit lines:

- `.ufo/waves/round-27/controls/v2/K2ShaPin-seed1.txt`
- `.ufo/waves/round-27/controls/v2/K2ShaPin-seed2.txt`

As instructed, neither command passed `--heldout`; no sealed files were read. Thus `b_valid=0`, `h_valid=0`, and held-out/sealed-benign performance is unmeasured. The failed public green cases already prevent the target independently of those absent sets.

Before and after the v2 scores, this command produced identical output:

```sh
env -i PATH=/usr/bin timeout 15 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/c2/count-v2.py .ufo/waves/round-27/c2/count.py .ufo/waves/round-27/c2/mutants-w.json .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/c2/count.py .ufo/waves/round-26/quality/check-population.py .ufo/waves/round-27/controls/K2ShaPin-suite-a.py .ufo/waves/round-27/controls/K2ShaPin-suite-b.py
```

```text
4dfb34b5551a908aa7fd56e75526417b43659018c47fa5993ad39a72b6b109d3  .ufo/waves/round-27/c2/count-v2.py
2e180ed29c31abcb3421d7e57a147d05ac9d2982ebe4dbc555747b287e754dc7  .ufo/waves/round-27/c2/count.py
0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608  .ufo/waves/round-27/c2/mutants-w.json
4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428  .ufo/waves/round-26/c1/count-v2.py
b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8  .ufo/waves/round-26/c2/count.py
803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64  .ufo/waves/round-26/quality/check-population.py
3f41b8c6cbeb3c9017ac05684120b41895144f0c5606ba8bb8e512938e65453c  .ufo/waves/round-27/controls/K2ShaPin-suite-a.py
4478cdb9a5b814edb98451719e0cde5c57db9e33f8d142f4166a9c3f202b6381  .ufo/waves/round-27/controls/K2ShaPin-suite-b.py
```

No lane subject or control needed restoration: the control bytes were unchanged and mutations remained in the counter's disposable clones. The original bounded `df -h /fast` command reported 113G available before v2 scoring (`804G` size, `691G` used, `86%`). Repeating the original bounded coredump-count command before and after gave `1338` both times: Hyprland coredump delta **0**. Subprocess environments were cleared, no compositor was started, and both scorer process groups received the same final SIGKILL sweep. No tooling was installed/updated.
