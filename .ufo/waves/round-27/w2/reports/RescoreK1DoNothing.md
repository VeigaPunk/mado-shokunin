# K1DoNothing — fresh-seed v4 re-score

RESCORE K1DoNothing best: PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED — not met

## Scope and shape

Read registration.md first after loading the requested godspeed skill. Axes: shape fidelity, fresh-seed detector discrimination, byte preservation, and host safety.

The committed control is exactly 12 bytes, `print("[]")\n`. Its defect is to ignore the configuration tree and always emit the empty JSON array. Expected detector: the frozen v4 counter requires type-strict, ordered JSON equality with the pinned isolated Hyprland oracle on all 41 cases; exit 0 means 41/41, exit 1 means target missed, and exit 2 is a guard/setup failure.

**Strongest within its registered shape: yes.** Registration defines DoNothing as “prints `[]`”. This control emits that valid array successfully. Every implementation preserving that behavior produces the same parsed JSON and therefore the same case results. Producing a nonempty table or reading the configuration would leave the assigned shape, not strengthen it. No stronger variant or extra mutation was created or scored.

## Exact command and fresh outputs

Ran the requested command twice concurrently, each with six jobs and a fresh counter-generated seed; no `--seed` was supplied. Both outer subprocess environments contained only `PATH=/usr/bin` and `HOME=/home/vgpnk`. The frozen oracle's shared 12-slot file locks bound host-wide compositor concurrency.

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1DoNothing.py --jobs 6
```

| Run | Fresh seed | Exact PRED line | Process exit | Elapsed |
| --- | --- | --- | --- | --- |
| 1 | `87bd8bc3942a1f4f` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 | 162.050 s |
| 2 | `4fdc85c0e2d265ab` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 | 167.462 s |

Both stderr streams were empty. Both passed only `BASE` (`rules=0 oracle_rules=0`) and failed all 25 APPEND and 15 SYNTH cases with `rules got=0 want=N first_diff=0`, where N was positive. Neither run hit a guard. Both BASE oracle repetitions agreed, and both receipts identify Hyprland commit `efb50993780079460b0cbed1363e2166a2de1d9f`, tag `v0.56.2`.

Verbatim stdout receipts:

- `/fast/scratch/hyaku/mado-r27/rescore/K1DoNothing-seed1.txt` — 6,066 bytes; SHA-256 `ccca1239fc9c5e6a4281b3348829fadd999519f897d1b044cb03617ea5beabe1`.
- `/fast/scratch/hyaku/mado-r27/rescore/K1DoNothing-seed2.txt` — 6,147 bytes; SHA-256 `1b8c024381fbd0c27bab8433a0e545e9d20128054cb05986f4a4a85fa8fb6c3e`.
- `/fast/scratch/hyaku/mado-r27/rescore/K1DoNothing-audit.txt` records the commands, process exits, receipt hashes, before/after source hashes, and coredump counts.

## Comparison with committed receipts

The request calls the supplied `controls/v4/K1DoNothing-seed*.txt` paths “v3 receipts”; their headers and PRED labels actually identify **v4**. Compared those exact files:

| Committed receipt | Seed | PRED line | Exit |
| --- | --- | --- | --- |
| `controls/v4/K1DoNothing-seed1.txt` | `8b1b1caa8415be87` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |
| `controls/v4/K1DoNothing-seed2.txt` | `bf84153533e19bc2` | `PRED-C1-r27-v4 cases_pass=1/41 verdict=TARGET_MISSED` | 1 |

Both new seeds differ from each other and both committed seeds. All four v4 scores agree: only BASE passes, so 1/41. Counter, oracle, control, revision, and snapshot hashes also match the committed v4 receipts. Revision is `2fdca5caaab6859386effbb8fa6acc5250c90633`; the 79-file snapshot SHA-256 is `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`.

Also read the actual historical `controls/v3/K1DoNothing-seed1.txt` and `seed2.txt` PRED lines: both say `PRED-C1-r27-v3 cases_pass=1/41 verdict=TARGET_MISSED`, with exit 1. Thus the outcome agrees with both the specified v4 receipts and the actual v3 scores; this does not treat the retired v3 counter as the current rule.

## Byte preservation and mutation verdict

No source bytes were modified, so no restoration write was needed. Bounded `sha256sum` commands before and after both scores returned identical hashes:

| File | SHA-256 before = after |
| --- | --- |
| `controls/K1DoNothing.py` | `a3381e95441354d833917bdaf481a5b210edf2b8cda6419b5e1805dfe143fd3b` |
| `c1/count-v4.py` | `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1` |
| `harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

This assignment re-scored an already-failing control; it did not introduce a new pristine/mutated/restored comparison. There is no killed-mutant claim: the control's whole-suite baseline misses the target, so any such kill inference would be inconclusive. The observed control verdict is **not met**, not a contract change.

## Host safety and other commands

Before scoring, ran `env -i PATH=/usr/bin HOME=/home/vgpnk timeout 15 prlimit --as=4000000000 -- df -h /fast`: `/dev/nvme1n1p2`, 804G total, 731G used, 73G available, 91% used.

Before and after the pair, ran the following commands with the same clean outer environment, lane working directory, and 35-second subprocess deadline:

```sh
timeout 30 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
timeout 30 prlimit --as=4000000000 --core=0 -- sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1DoNothing.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/c1/count-v4.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/harness/oracle.py
```

Counted coredump-list lines containing `/usr/bin/Hyprland` in Python. Both listings exited 0 with empty stderr: **1338 before, 1338 after, delta 0**. Both counter receipts independently print `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`. Both hash commands exited 0.

Hyprland was started only through the frozen counter/oracle, with no inherited live compositor environment, no live-compositor commands, and no DRM card-node access. Both counter processes completed; the frozen oracle uses `finally` process-group termination and waits. No persistent service, subagent, alternate agent runtime, installation, git/jj write, lane source edit, or unrelated check was performed. Writes were limited to this scoped report and the three assigned rescore receipts.
