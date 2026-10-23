# K1NoMerge — fresh-seed v4 re-score

RESCORE K1NoMerge best: PRED-C1-r27-v4 cases_pass=8/41 verdict=TARGET_MISSED — not met

## Control and detector

Read `registration.md` first. Re-scored the unchanged committed `.ufo/waves/round-27/controls/K1NoMerge.py`, SHA-256 `918501eb066d36b811a6ac0ec759e2b510c2285261c58d5f9058291ead785947`.

The deliberate defect is append-only insertion: every successfully parsed workspace line appends an object, without selector lookup, deduplication, update, or merge (`K1NoMerge.py:206–243`). The expected detector is counter v4's exact ordered, type-strict JSON comparison against the pinned Hyprland oracle. Repeated selectors should produce excess entries and reject the control.

## Exact scoring command and outputs

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Ran this command twice, without `--seed`:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K1NoMerge.py --jobs 6
```

Each invocation was wrapped with `set -o pipefail` and piped to `env -i PATH=/usr/bin tee RECEIPT`, using the respective absolute receipt path below. Initial asynchronous submissions were rejected by the tool's full background-job table before launch; the two subsequent synchronous invocations below completed and are the measurements.

| Run | Fresh seed | Actual PRED line | Process exit | Wall time | Receipt |
| --- | --- | --- | --- | --- | --- |
| 1 | `417ad309ae7d8eee` | `PRED-C1-r27-v4 cases_pass=6/41 verdict=TARGET_MISSED` | 1 | 180.82 s | `/fast/scratch/hyaku/mado-r27/rescore/K1NoMerge-fresh-seed1.txt` |
| 2 | `712f207b95621aef` | `PRED-C1-r27-v4 cases_pass=8/41 verdict=TARGET_MISSED` | 1 | 140.93 s | `/fast/scratch/hyaku/mado-r27/rescore/K1NoMerge-fresh-seed2.txt` |

Both passed BASE and the repeated-base stability guard, confirmed oracle commit `efb50993780079460b0cbed1363e2166a2de1d9f`, and measured the same 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`. Neither run exited 2.

## Comparison with committed receipts

The requested `controls/v4/K1NoMerge-seed*.txt` paths contain **v4**, not v3, receipts. Compared both those requested files and the actual v3 files:

| Historical counter | Seed 1 | Seed 2 | Best |
| --- | --- | --- | --- |
| v4, requested paths | `ae05fa9a659a346f`: 7/41 | `538061af089eeeab`: 9/41 | 9/41 |
| v3, `controls/v3/` | `4f300834ca94c475`: 14/41 | `53cc409ac3e29827`: 8/41 | 14/41 |
| v4, this re-score | `417ad309ae7d8eee`: 6/41 | `712f207b95621aef`: 8/41 | 8/41 |

Every historical and fresh receipt reports `TARGET_MISSED` and `exit=1`. The historical best is not a fresh-run result; fresh-seed populations differ, so score differences do not establish a regression. The kill-rule conclusion is unchanged: this control does not meet 41/41.

## Strongest version within the shape

**For both newly measured populations, the committed control already attains the strict append-only shape's score ceiling.** No stronger within-shape variant was identified or scored.

To distinguish a parser weakness from the intended missing merge, regenerated the two exact seeded populations using the frozen counter's builder, verified the snapshot digest against each receipt, and ran only the control parser in temporary scratch trees. This did not launch Hyprland or change the detector. For every case, the number of distinct parsed selector strings equalled the oracle's recorded rule count. Every duplicate-free case already passed the complete JSON comparison; every rejected case contained repeated selector strings and emitted excess entries.

```text
COUNT_CEILING seed=417ad309ae7d8eee cases=41 unique_selector_counts_equal_oracle=41/41 duplicate_free=6 repeated_selector=35 observed_pass=6
DUPLICATE_FREE BASE,C02,C16,C19,C26,C39
COUNT_CEILING seed=712f207b95621aef cases=41 unique_selector_counts_equal_oracle=41/41 duplicate_free=8 repeated_selector=33 observed_pass=8
DUPLICATE_FREE BASE,C05,C06,C09,C11,C17,C22,C26
```

The analysis exited 0 with empty stderr. Exact executed command, including the full Python analysis, is retained at `/fast/scratch/hyaku/mado-r27/rescore/K1NoMerge-count-ceiling-command.txt`; output is `/fast/scratch/hyaku/mado-r27/rescore/K1NoMerge-count-ceiling.txt`. Temporary trees were removed by `TemporaryDirectory`.

Improving either measured score would require reducing entries for repeated valid selectors—deduplication, replacement, or merging—which leaves the assigned one-entry-per-line shape. This is an evidenced ceiling for these populations, not a claim that the parser implements every possible Hyprlang input.

## Integrity, restoration, and safety

This assignment re-scored an existing retained control; it did not mutate a pristine production implementation. No pristine/mutated/restored causal-kill experiment is claimed. Both valid detector runs rejected the control. No source bytes were changed, so no restoration was necessary.

The following before/after hashes matched exactly:

| File | Before = after SHA-256 |
| --- | --- |
| `controls/K1NoMerge.py` | `918501eb066d36b811a6ac0ec759e2b510c2285261c58d5f9058291ead785947` |
| `c1/count-v4.py` | `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1` |
| `harness/oracle.py` | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |

Paths in this table are under `.ufo/waves/round-27/`. Before/after receipts are `/fast/scratch/hyaku/mado-r27/rescore/K1NoMerge-inputs-before.txt` and `K1NoMerge-inputs-after.txt`.

| New receipt | Bytes | SHA-256 |
| --- | --- | --- |
| `K1NoMerge-fresh-seed1.txt` | 6,030 | `8d90d0b78a1ee0bc5db18b6ebb6225e9be452db9633771b4a156d4ae581afb91` |
| `K1NoMerge-fresh-seed2.txt` | 6,094 | `3ed395a7412cbce3a2b1e0760d21c01b18911a0703e7f548c533d9c66c34af95` |
| `K1NoMerge-count-ceiling.txt` | 731 | `cd34f53fd94124326a1cdfe0635ae0368dbc3b381920979e83943c0339edad66` |

`df -h /fast` reported 74G available before writes. Independent host Hyprland coredump count: **1338 before, 1338 after, delta 0**, measured with bounded, cleared-environment `coredumpctl list --no-pager --no-legend` and a count of lines containing `/usr/bin/Hyprland`. Each counter receipt also reports:

```text
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
```

Only the frozen counter/oracle launched nested Hyprland; it uses host-wide slot locks and cleans each process group in `finally`. Both counter process trees completed. No live compositor commands, DRM card nodes, held-out reads, git/jj write commands, subagent dispatch, host-service changes, or tool installations/updates were used. No background process or temporary analysis tree was retained. The only lane write is this scoped report.
