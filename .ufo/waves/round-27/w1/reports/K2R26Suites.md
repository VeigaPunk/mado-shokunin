# K2R26Suites — round-26 suites control

## Verdict
CONTROL K2R26Suites best: PRED-C2-r27 green=3/8 w_killed=12/15 h_killed=0/0 h_need=0 h_valid=0 h_invalid=0 verdict=TARGET_MISSED — not met

Both fresh seeds produced the same PRED line and process exit 1. Neither run exited 2, so no guard rerun was required. No held-out directory was supplied or read; these are the required pre-data W-only scores, not a held-out measurement.

## Scope and detector

Axes: preserve the registered control shape, measure green compatibility, and distinguish meaningful mutant detection from baseline failure.

Read the godspeed skill, round-27 registration, operator tooling rules, unchanged round-26 self-test, round-26 population red/green receipt, and frozen C2 counter before running.

- Suite A was the unchanged `.ufo/waves/round-26/quality/counter-selftest.py`, injected at that exact repo-relative path with `--suite-a-rel`. No suite-A copy or replacement was authored.
- Created only `controls/K2R26Suites-suite-b.py` under the round-27 control directory. It accepts `--checker PATH`, invokes exactly the five synthetic round-26 fixture commands listed at `q37-population-red-green.txt:4-42`, and exits 0 iff all five observed exits equal their expected exits. Each checker invocation has a 30-second timeout and a cleared, explicitly constructed environment. No additional checker assertions or fixtures were added.
- Expected fixture exits, in order: green receipt 0; removed CASE 1; changed denominator 1; changed registration total 1; self-consistent 40-case shrink 1. The real base receipts and unreadable-receipt example later in that receipt were intentionally not included: the assigned shape is exactly five population fixtures.
- Detector: the frozen round-27 C2 counter at REV `5ddc5885188a1de8606464526d636c9e2fc433e6`, with its 15 existing W mutants. No mutant, counter, harness, or lane subject was edited. The counter applies its mutations only in disposable clones and removes those clones in its `finally` blocks.
- Suite B: 1,607 bytes, SHA-256 `d8ef4aa74516ff0e443942e1ffdceff3a050864180d80bd5e20a8a271ea7aaff`.

## Exact scoring commands

Commands ran concurrently from `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/quality/counter-selftest.py --suite-a-rel .ufo/waves/round-26/quality/counter-selftest.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2R26Suites-suite-b.py --seed cc9ffcd4d34c067b --jobs 6
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 python3 -I .ufo/waves/round-27/c2/count.py 5ddc5885 --suite-a-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/quality/counter-selftest.py --suite-a-rel .ufo/waves/round-26/quality/counter-selftest.py --suite-b-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/K2R26Suites-suite-b.py --seed de233aeaac46f498 --jobs 6
```

Both stdout streams were saved verbatim, including the final `exit=1`; both stderr streams were empty. Saved bytes were compared with the captured stdout bytes and matched exactly.

| Seed | Receipt relative to lane root | Bytes | Receipt SHA-256 |
| --- | --- | ---: | --- |
| `cc9ffcd4d34c067b` | `.ufo/waves/round-27/controls/K2R26Suites-seed1.txt` | 3295 | `2e680ccafb560541c98c9eba7854d5392659c5552b22d1e45125b766d384cc36` |
| `de233aeaac46f498` | `.ufo/waves/round-27/controls/K2R26Suites-seed2.txt` | 3295 | `40e4fd595df1eac8c04c1ee3b0cd3a2d5f1b23369ef9915203fa45ad26ed28bb` |

Each receipt ends:

```text
PRED-C2-r27 green=3/8 w_killed=12/15 h_killed=0/0 h_need=0 h_valid=0 h_invalid=0 verdict=TARGET_MISSED
exit=1
```

## Actual outputs and mutation interpretation

Both seeds agreed on every case:

- Suite A: pristine and all four benign variants exited 1, so green was 0/5. All nine A-subject W mutants also exited 1 and were labelled KILLED by the counter's registered nonzero-exit rule. These nine labels are **inconclusive as discriminating mutation evidence**, because the pristine A baseline already failed. They are not claimed as nine demonstrated behavioral kills.
- Suite B: pristine and both benign checker variants exited 0 with `POPULATION_SUITE pass=5/5`, so green was 3/3.
- Suite B killed `q37-M1-ignore-registered` (3/5), `q37-M3-drop-denominator` (4/5), and `q37-M5-case-plus-one` (3/5), all with exit 1 against a passing pristine baseline.
- Suite B survivors were `q37-M2-case-anywhere`, `q37-M4-first-pred-only`, and `q37-M6-unreadable-exit-0`, each exit 0 with 5/5. These are coverage findings within the five-fixture shape, not grounds to add fixtures or change the contract.

Thus the raw registered score is 12/15 W labels, but the sound behavioral interpretation is three killed B mutants, three surviving B mutants, and nine baseline-inconclusive A mutants. The control does not meet the target independently of the absent held-out set.

## Preservation and safety evidence

The following SHA-256 values were independently computed before and after both runs; every before hash equalled its after hash. No lane restoration was necessary because no lane subject bytes were changed. No separate restored-state detector run was claimed; this was the assigned two-seed control score using disposable clone mutations.

| Lane-relative input | Before SHA-256 = after SHA-256 |
| --- | --- |
| `.ufo/waves/round-27/c2/count.py` | `2e180ed29c31abcb3421d7e57a147d05ac9d2982ebe4dbc555747b287e754dc7` |
| `.ufo/waves/round-27/c2/mutants-w.json` | `0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608` |
| `.ufo/waves/round-26/quality/counter-selftest.py` | `0754f5013800a1f61a04259b1a4bbbbee389788b251a1b831fd82994385b642a` |
| `.ufo/waves/round-26/c1/count-v2.py` | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` |
| `.ufo/waves/round-26/c2/count.py` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` |
| `.ufo/waves/round-26/quality/check-population.py` | `803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64` |

Safety commands ran with environment `{PATH=/usr/bin, HOME=/home/vgpnk}`:

```sh
timeout 20 prlimit --as=4000000000 --core=0 -- df -h /fast
timeout 20 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
```

`df` reported `/fast`: 804G total, 689G used, 115G available, 86% used. The coredump command was run before and after; Python counted stdout lines containing `/usr/bin/Hyprland` (the equivalent of the required grep count): before 1338, after 1338, delta 0. Both coredump commands exited 0 with empty stderr.

All started child environments omitted WAYLAND_DISPLAY, HYPRLAND_INSTANCE_SIGNATURE, and git override variables. The self-test uses its existing offline oracle replacements; no Hyprland instance, live-compositor command, host service, network request, or device access was started. Both counter process groups were isolated; direct children were reaped, and each group received final cleanup if still present. The counter itself imposes the registered 300-second, 4-GB, core-disabled suite bounds. No git/jj write command was run in the lane or fleet repo. No tools were installed or updated.
