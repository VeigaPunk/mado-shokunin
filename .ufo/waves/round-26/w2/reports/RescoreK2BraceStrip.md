# RescoreK2BraceStrip — frozen C2 control re-score

RESCORE K2BraceStrip not met (best 21/51)

## Scope and expected detector

Axes: preserve the brace-stripper shape; retain inherited round-25 behavior; discriminate with the frozen counter; maintain host isolation and reproducible evidence.

Re-scored the unmodified committed `controls/K2BraceStrip.py` twice at `1b0b91e9889cbf984b052f5de564db78330a72aa`, with two fresh random seeds. Then scored one within-shape strengthening once with a third fresh seed. Finally restored its exact pre-mutation bytes and replayed the same bounded detector with the first seed for restoration evidence. This last replay is not counted as a fresh-seed re-score.

Shape comes from `w1/reports/K2BraceStrip.md:12-21` and `registration.md:93-95`: the round-25 base resolver with `{{` and `}}` deleted from every root/sourced file before logical-line handling; no arithmetic evaluation, expression grammar, oracle lookup, cached table, or extra resolver.

Expected detector: unmodified `.ufo/waves/round-26/c2/count.py`, requiring exact equality of all 18 bind fields on BASE + 30 ARITH + 20 V3 cases, plus `embed_hits=0`; target 51/51. It checks the nested oracle's base result twice before scoring. All four runs measured cases (counter process exit 1), rather than setup/guard exit 2.

## Observed receipts

Each run passed BASE and all 20 V3 cases and failed all 30 ARITH cases. The within-shape attempt produced no score gain.

### rescore-1

```text
seed=e1763d48904361f2
PRED-C2-r26 cases_pass=21/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Actual counter process return code: `1`.

### rescore-2

```text
seed=b6207fa620dfcffe
PRED-C2-r26 cases_pass=21/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Actual counter process return code: `1`.

### strengthened

```text
seed=84b6084dc029ea68
PRED-C2-r26 cases_pass=21/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Actual counter process return code: `1`.

### restored

```text
seed=e1763d48904361f2
PRED-C2-r26 cases_pass=21/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Actual counter process return code: `1`.

All snapshots contained 79 files with digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`; every base-twice oracle check reported equality at 192 binds. The restored run's complete CASE PASS and CASE FAIL lines exactly equal those of `rescore-1` (recorded in `restoration-comparison.json`).

Examples from the unmodified re-scores:

- `rescore-1.stdout.txt:7`: Hyprland reported resize argument `188.41101 68`; the control emitted `11.083 * 17*0   33 + 35`.
- `rescore-1.stdout.txt:11`: Hyprland preserved unclosed `echo {{2 + 8`; the control emitted `echo 2 + 8`.
- `rescore-2.stdout.txt:7`: Hyprland preserved escaped literal `echo {{(15.4*21 + 4) + 1}}`; the control emitted a backslash followed by `(15.4*21 + 4) + 1`, without the brace pairs.

## Single strengthening / mutation

Only file preprocessing in `parse_file` was changed, at the original line 445, in the isolated scratch copy `K2BraceStrip.fixedpoint.py`:

```python
# Pristine
lines = data.decode("utf-8", "replace").replace("{{", "").replace("}}", "").split("\n")

# Strengthened attempt
text = data.decode("utf-8", "replace")
while "{{" in text or "}}" in text:
    text = text.replace("{{", "").replace("}}", "")
lines = text.split("\n")
```

The intended improvement was fixed-point stripping: a deletion can expose another pair, so the pass repeats until neither pair remains. It still only deletes the same two brace-pair spellings before logical-line handling, preserves all other base-resolver bytes, and adds no arithmetic or expression grammar. This is a strengthening attempt within the shortcut's shape, not a repair of the real C2 contract.

Mutation-probe verdict: **INCONCLUSIVE as a regression kill**, because the pristine control already failed the target. The mutant also missed at 21/51; it is not claimed killed or survived on the strength of an already-failing baseline. The re-score verdict above is conclusive for these measured seeds: none met the target. No universal claim over unmeasured seeds is made.

## Exact commands and receipt files

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Executed the receipt-capture wrapper with these exact commands; `rescore` launched its two independent counters concurrently, and the other modes each launched one:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=20 950 prlimit --as=4000000000:8000000000 -- python3 -I /fast/scratch/hyaku/mado-r26/rescore/RescoreK2BraceStrip/run_probe.py rescore
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=20 950 prlimit --as=4000000000:8000000000 -- python3 -I /fast/scratch/hyaku/mado-r26/rescore/RescoreK2BraceStrip/run_probe.py strengthened
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --kill-after=20 950 prlimit --as=4000000000:8000000000 -- python3 -I /fast/scratch/hyaku/mado-r26/rescore/RescoreK2BraceStrip/run_probe.py restored
```

The wrapper launched these exact detector argv, with the five environment variables above removed:

```sh
timeout --kill-after=15 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK2BraceStrip/K2BraceStrip.py --seed e1763d48904361f2 --jobs 4
timeout --kill-after=15 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK2BraceStrip/K2BraceStrip.py --seed b6207fa620dfcffe --jobs 4
timeout --kill-after=15 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK2BraceStrip/K2BraceStrip.fixedpoint.py --seed 84b6084dc029ea68 --jobs 4
timeout --kill-after=15 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK2BraceStrip/K2BraceStrip.fixedpoint.py --seed e1763d48904361f2 --jobs 4
```

Full stdout, empty stderr, command/environment/exit metadata, receipt hashes, and before/after source hashes are retained under:

`/fast/scratch/hyaku/mado-r26/rescore/RescoreK2BraceStrip/`

| Run | Full stdout | Metadata | Stdout SHA-256 |
| --- | --- | --- | --- |
| `rescore-1` | `rescore-1.stdout.txt` | `rescore-1.summary.json` | `446c0dc8171d83176a7718f9727ab26d7c7ba9c55276aab03e71b3990bca974f` |
| `rescore-2` | `rescore-2.stdout.txt` | `rescore-2.summary.json` | `84bed0c72709dfe8650382d04bb0f354a057cd680dca761c281633e0bcf8a842` |
| `strengthened` | `strengthened.stdout.txt` | `strengthened.summary.json` | `d52d4614069d04608a2c6c49849366c39d527e71706d15772f1e0c3c3152b3a7` |
| `restored` | `restored.stdout.txt` | `restored.summary.json` | `b764201478ff8f8df3cfeb77b0ab2454a73c020e38e90e3b6429cabf921a9d1f` |

Corresponding `*.stderr.txt` files are all zero bytes. `run_probe.py` is the exact capture wrapper. Capacity check was `env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 df -h /fast`: 804G total, 658G used, 146G available, 82% used.

## Hashes and restoration evidence

The committed control and pristine scratch copy were both 15,619 bytes, SHA-256 `6e8efe633f2b8e987e647b8a7726a64a445953cd0fe17ea041c3671b0aa6d625`. The strengthened copy scored at 15,695 bytes, SHA-256 `8e111f089e9d7e745d7186441358d5fe38896f53b5cb1bc6fb710a38d30fa899`. It was then restored to 15,619 bytes and the original SHA-256 before the restored detector run. The formerly strengthened filename now contains pristine bytes, not the mutant.

`restoration-evidence.json` records direct byte equality between the restored copy and the original pre-mutation bytes, and confirms both the committed control and pristine scratch copy are exactly unchanged. All three equality checks were true. Every run's before/after hash records were equal, including the restored run.

| Frozen lane file | SHA-256 before = after, all four runs |
| --- | --- |
| `.ufo/waves/round-26/controls/K2BraceStrip.py` | `6e8efe633f2b8e987e647b8a7726a64a445953cd0fe17ea041c3671b0aa6d625` |
| `.ufo/waves/round-26/c2/count.py` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` |
| `.ufo/waves/round-26/harness/oracle.py` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` |
| `.ufo/waves/round-25/c1/count-v3.py` | `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375` |

No lane file was edited except this assigned report; all control work and receipts stayed in the seat's isolated scratch directory. No git/jj write commands were run.

## Host safety and bounds

Every Hyprland launch was through the frozen counter and its pinned oracle; no direct compositor launch or live-session hyprctl command was issued. The oracle's unchanged host-wide 12-slot locking remained active (`oracle.py:109-125`). No WAYLAND_DISPLAY or HYPRLAND_INSTANCE_SIGNATURE was inherited by the commands launched here. Counter memory limits were 4 GB soft / 8 GB hard so that the oracle could raise its own limit to 8 GB; no lower hard limit was imposed.

All four receipts printed exactly:

```text
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
```

No outer timeout occurred. The wrapper bounded communication, reaped each counter, unconditionally cleaned its process group, and recorded `counter_process_group_remaining=false` after every run. Sandbox process-group cleanup is the oracle's unchanged `finally` block (`oracle.py:212-226`). The three wrapper invocations have completed. No service was started or restarted; no tool was installed or updated. No build, lint, formatter, or unrelated verification was run.

RESCORE K2BraceStrip not met (best 21/51)
