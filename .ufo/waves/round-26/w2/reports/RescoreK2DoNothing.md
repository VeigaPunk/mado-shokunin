# RescoreK2DoNothing — round 26, w2

RESCORE K2DoNothing not met (best 0/51)

## Scope and method

Axes: measured score, fidelity to the frozen control shape, host isolation, exact-byte restoration.

Re-scored the committed `controls/K2DoNothing.py` twice without changing its bytes, then scored one within-shape simplification once. Finally restored the scratch file and ran the same detector on restored bytes. The first two runs are the required re-scores; the fourth is restoration evidence, not a replacement receipt.

All paths below beginning `controls/`, `c2/`, `harness/`, or `w1/` are relative to `.ufo/waves/round-26/`. Scratch and complete stdout receipts are under:

`/fast/scratch/hyaku/mado-r26/rescore/RescoreK2DoNothing/`

The w1 shape is an empty bind table or no output, never reading the config tree (`w1/reports/K2DoNothing.md:7-23`; `controls/K2DoNothing.py:2-9`). A 247-byte exact copy of the named committed control was used in scratch. No committed control, tool, counter, harness, or sibling source was edited. The only lane write is this report.

Measurement revision: `1b0b91e9889cbf984b052f5de564db78330a72aa`.

Frozen inputs, unchanged before/after:

- C2 counter: `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8`.
- Oracle: `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441`.
- The counter reported its pinned count-v3 dependency: `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`.

## Actual results

No `--seed` was supplied. Each run generated its own fresh seed.

| Run | Seed | Cases passed | Embed hits | Actual process exit | Receipt filename |
|---|---|---|---|---|---|
| Unchanged re-score 1 | `9bb151b58be27073` | 0/51 | 0 | 1 | `pristine-1.txt` |
| Unchanged re-score 2 | `734c844a7888b39e` | 0/51 | 0 | 1 | `pristine-2.txt` |
| Literal-output candidate | `633d7d165910766d` | 0/51 | 0 | 1 | `literal-candidate.txt` |
| Exact-byte restored | `217ea8cf7b1a1cc4` | 0/51 | 0 | 1 | `restored.txt` |

Unchanged re-score 1, verbatim prediction and exit:

```text
PRED-C2-r26 cases_pass=0/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Unchanged re-score 2, verbatim prediction and exit:

```text
PRED-C2-r26 cases_pass=0/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Candidate, verbatim prediction and exit:

```text
PRED-C2-r26 cases_pass=0/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Restored bytes, verbatim prediction and exit:

```text
PRED-C2-r26 cases_pass=0/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Every run reported `ORACLE_CHECK base_twice equal binds=192`, the same 79-file snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, and all 51 cases failing with `missing=oracle_binds`, `extra=0`. These were complete scored runs, not exit-2 guards or timeouts.

## Within-shape strengthening attempt

Small scratch-only change: remove `import json` and replace `print(json.dumps([]))` with `print("[]")`. This removes the serialization dependency/call while retaining the required CLI and the identical empty-table output. Neither version reads `--home` or evaluates any expressions.

Expected detector: the same frozen C2 counter, exact 18-field multiset equality, target 51/51 and no embedded strings. Expected tool output for valid CLI input remains `[]` followed by a newline. Actual detector output above confirms the candidate produced a valid empty table, not a JSON error, and still scored 0/51.

No score-improving strengthening was found within this shape. All measured expected tables were nonempty. The equality comparison subtracts complete multisets (`.ufo/waves/round-25/c1/count-v3.py:746-751`), so changing empty-table serialization cannot supply missing bindings. Returning config-derived or cached nonempty bindings would leave the w1 do-nothing shape.

Mutation-kill interpretation: **inconclusive, not killed**. The pristine program already fails the target, and this candidate is deliberately output-equivalent rather than a behavioral fault injection. These results support the requested control re-score; they do not establish checker mutation coverage.

## Restoration evidence

| Bytes | SHA-256 |
|---|---|
| Committed control before and after | `5b51bd4fb0f7d6e6b40013554ca3c94e7964820df18dea0b9875a5e5e3c6e747` |
| Scratch pristine, both required re-scores | `5b51bd4fb0f7d6e6b40013554ca3c94e7964820df18dea0b9875a5e5e3c6e747` |
| Scratch candidate | `edc9882e8808064d58d5eb3e58b510581ff3cbedf008ddb7a54448ca81643fc8` |
| Scratch restored, independently hashed and reported by final counter run | `5b51bd4fb0f7d6e6b40013554ca3c94e7964820df18dea0b9875a5e5e3c6e747` |

The scratch file was restored immediately after the candidate run returned exit 1. The final detector used the same scratch path and confirmed the original tool hash.

Complete stdout receipt hashes:

```text
2ef0b96ded17145663cbb058cd567df8ebcb94622a0d88e12000b0097ed78784  pristine-1.txt
9a179dd4bf2bd287bd9615ee2e6ea6759054c97be7dbb59fd7e3253339e4c823  pristine-2.txt
d4ce50d7ba61860ddbaef753b15d33f79e6b5139546baea9d82e1f6385b39076  literal-candidate.txt
6e6457dacb5048f96332811563567e6b391cff96c8c978c57d29f18e427f4a8b  restored.txt
```

## Host safety

The two required re-scores and candidate each printed:

```text
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
```

The additional restoration run printed a host-wide increment, retained without alteration:

```text
HOST_SAFETY hyprland_coredumps_before=1336 after=1337 delta=1
```

Read-only `coredumpctl` inspection found two recent Hyprland SIGABRT records, both naming another seat's development trees:

```text
PID 2245463, Fri 2026-10-23 06:32:14 -03
Command Line: Hyprland -c /fast/scratch/hyaku/mado-r26/data/ExecAnimToolA/devO-pmv1gx6g/tmpnpun2ha4/home/.config/hypr/hyprland.conf
PID 2367290, Fri 2026-10-23 06:32:54 -03
Command Line: Hyprland -c /fast/scratch/hyaku/mado-r26/data/ExecAnimToolA/devO-pmv1gx6g/tmppqc7gw7o/home/.config/hypr/hyprland.conf
```

Both records report `Storage: none`, terminated abnormally without generating a coredump. The later record overlaps the restoration run. This attributes the observed new records to `ExecAnimToolA` paths, not this control's counter trees; it does not make the fourth receipt's raw host-wide delta zero. Sent that seat the two PIDs, times, and paths for its safety accounting.

`MadoR26.ExecAnimToolA` subsequently confirmed both PIDs were its `dev_overflow.py` probe, using 60-digit animation-speed and bezier-coordinate inputs. It reports uncaught `std::out_of_range` from `std::stof` in nested Hyprland and no live-compositor interaction. This is peer-provided cause attribution, not an additional probe by this seat.

Only the frozen oracle started nested compositors. Counter commands explicitly removed `WAYLAND_DISPLAY` and `HYPRLAND_INSTANCE_SIGNATURE`, used the prescribed 4 GB soft / 8 GB hard limit, 900-second timeout, and `--jobs 1`; the oracle retains its host-wide 12-slot lock. No live-compositor command or DRM card access was issued by this seat. All four counter commands completed normally with exit 1; no service was started or left running. The oracle's normal-return cleanup kills/waits for each sandbox process group (`harness/oracle.py:212-226`).

`df -h /fast` before writes reported 145 GB available. No git/jj write commands, package installations, upgrades, or service restarts were performed.

## Exact detector commands

Working directory for all commands: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

```sh
set -o pipefail && env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout --kill-after=30 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK2DoNothing/K2DoNothing.py --jobs 1 | tee /fast/scratch/hyaku/mado-r26/rescore/RescoreK2DoNothing/pristine-1.txt
set -o pipefail && env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout --kill-after=30 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK2DoNothing/K2DoNothing.py --jobs 1 | tee /fast/scratch/hyaku/mado-r26/rescore/RescoreK2DoNothing/pristine-2.txt
# Scratch-only change described above.
set -o pipefail && env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout --kill-after=30 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK2DoNothing/K2DoNothing.py --jobs 1 | tee /fast/scratch/hyaku/mado-r26/rescore/RescoreK2DoNothing/literal-candidate.txt
# Restored exact scratch bytes.
set -o pipefail && env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout --kill-after=30 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK2DoNothing/K2DoNothing.py --jobs 1 | tee /fast/scratch/hyaku/mado-r26/rescore/RescoreK2DoNothing/restored.txt
```

Additional read-only crash-attribution commands:

```sh
timeout 15 coredumpctl list --since '15 minutes ago' --no-pager --no-legend
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 15 coredumpctl info 2245463 --no-pager
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 15 coredumpctl info 2367290 --no-pager
```

No blocker. Both fresh-seed re-scores agree with w1's 0/51 result; the within-shape candidate also misses the target. No contract change or integration is proposed.
