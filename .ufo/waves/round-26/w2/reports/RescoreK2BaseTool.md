# RescoreK2BaseTool — round 26 w2

RESCORE K2BaseTool not met (best 23/51)

## Scope and shape

Re-scored the committed `.ufo/waves/round-26/controls/K2BaseTool.py` twice under the frozen C2 counter with independently generated fresh seeds. No control, counter, harness, or production-tool bytes were edited.

Axes: exact 51-case behavior, strict control-shape fidelity, fresh-seed independence, host isolation, and reproducible receipts.

The w1 shape is unusually strict: `w1/reports/K2BaseTool.md:8-10` requires the round-25 resolver **byte for byte**, with nothing added, wrapped, or edited. Consequently there is no admissible behavior-changing strengthening. Adding expression evaluation, rejecting expression-bearing lines, or wrapping the resolver would change that shape. Rather than silently widening it, I copied the exact original bytes into my isolated scratch directory and scored that strongest admissible candidate once with a third fresh seed. This third score is an unchanged-candidate score, **not an implemented strengthening**.

## Exact execution

Working directory for every counter process:

`/home/vgpnk/Projects/shokunin/mado-shokunin`

Runs 1 and 2 used this identical argument vector, concurrently:

```sh
timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2BaseTool.py --jobs 2
```

Run 3 used:

```sh
timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK2BaseTool/K2BaseTool.shape-constrained.py --jobs 2
```

Each command was started using Python `subprocess.Popen(..., cwd=lane, env=clean_env, stdout=receipt, stderr=error_receipt, start_new_session=True)`. `clean_env` was a copy of the environment with `WAYLAND_DISPLAY` and `HYPRLAND_INSTANCE_SIGNATURE` removed before process creation. No `--seed` was passed. Full resolved revision in every receipt: `1b0b91e9889cbf984b052f5de564db78330a72aa`.

## Observed results

| Run | Seed | Cases | Embed hits | Counter/process exit |
|---|---|---|---|---|
| 1, committed control | `2c2c1e17a8c6370c` | 21/51 | 0 | 1 / 1 |
| 2, committed control | `1e159385d612d8fd` | 23/51 | 0 | 1 / 1 |
| 3, byte-identical scratch candidate | `d50b73d818385c89` | 21/51 | 0 | 1 / 1 |

Run 1, verbatim:

```text
PRED-C2-r26 cases_pass=21/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Run 2, verbatim:

```text
PRED-C2-r26 cases_pass=23/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Run 3, verbatim:

```text
PRED-C2-r26 cases_pass=21/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

BASE and all twenty V3 cases passed in every run. ARITH passed 0/30, 2/30, and 0/30 respectively. Run 2's only ARITH passes were A07 (`unclosed+unclosed`) and A29 (`unclosed+escaped+escaped+escaped`). The control still leaves evaluable expressions literal; run 3 A01, for example, had oracle workspace argument `26` missing and the literal `{{ 26 * 1 }}` as extra. This agrees with the negative-control mechanism described in w1; the new best 23/51 is not the 51/51 target.

All receipts printed:

```text
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal binds=192
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
```

## Complete receipt files

Directory: `/fast/scratch/hyaku/mado-r26/rescore/RescoreK2BaseTool/`.

| File | Bytes | SHA-256 |
|---|---|---|
| `run-1.stdout` | 13582 | `d2478bed55e299cb934bffc97406eac61b35142f8131077c85203aa0f71664c3` |
| `run-2.stdout` | 12176 | `5d64acda873de116faf3258af926207aa1f346f80010a773cbd158577b7dc161` |
| `run-3-shape-constrained.stdout` | 13614 | `e0c436399d41e6d3ea610220be9863977ef91e39bf66f4f7b3016ffeaae455f8` |

The corresponding `run-1.stderr`, `run-2.stderr`, and `run-3-shape-constrained.stderr` files are all zero bytes. Stdout receipts are unmodified, including their `exit=` lines; actual subprocess return codes independently equaled 1.

## Integrity, preservation, and safety

Before execution, measured input SHA-256 values were:

- Control: `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950`.
- C2 counter: `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8`.
- Oracle harness: `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441`.
- Round-25 V3 counter: `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`.

The frozen counter printed those same counter/harness/V3 pins in all three receipts. After all runs, the committed control and the 15,583-byte scratch candidate both had SHA-256 `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950`; direct comparison against the original saved control bytes returned `control_exactly_preserved=True`. No restoration was necessary because no original bytes were changed.

This assignment was a re-score, not a mutation probe. No mutant was introduced and no killed/survived verdict is claimed; an already-missing baseline target would not establish a killed mutant.

Only the pinned counter invoked Hyprland, through its host-wide 12-slot oracle. The 4 GB soft / 8 GB hard address-space limit permits the oracle's own 8 GB limit. Every counter process exited and was reaped; checking its owned process group after exit returned absent for all three. The harness's `finally` cleanup terminates and reaps its sandbox processes (`harness/oracle.py:212-226`). No live-compositor commands or device-card access were performed by this seat. Before scratch writes, `df -h /fast` reported 146 GB available. No tools were installed or updated. No subagents were dispatched.

RESCORE K2BaseTool not met (best 23/51)
