# RescoreK2EmbedReplay

RESCORE K2EmbedReplay not met (best 23/51)

## Scope and frozen inputs

Axes: fresh-seed behavioral coverage, literal embedding detection, preservation of the permitted replay shape, payload footprint, host safety, and exact restoration.

Re-scored the committed control twice without modifying it, then scored one scratch-only strengthening attempt once. All three runs used revision `1b0b91e9889cbf984b052f5de564db78330a72aa`, the frozen C2 counter, fresh counter-generated seeds, and `--jobs 2`. None returned a setup/guard exit 2.

Before and after hashes were identical for these lane files:

| File | SHA-256 |
| --- | --- |
| `.ufo/waves/round-26/controls/K2EmbedReplay.py` | `a4d6d115fb74294dce44824c38b2e9b049e68face6afc30071c001d1d263a30c` |
| `.ufo/waves/round-26/c2/count.py` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` |
| `.ufo/waves/round-26/harness/oracle.py` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` |

All receipts reported the same snapshot: 79 files, SHA-256 `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, and two agreeing BASE oracle tables containing 192 binds.

## Fresh re-score receipts

### Committed control, run 1

```text
seed=3a9926d62b5fb1e0
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=23/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Subprocess return code: 1. BASE and all 20 V3 cases passed. The two passing ARITH cases were A18 (`escaped+unclosed`) and A29 (`unclosed+unclosed`); the remaining 28 ARITH cases failed.

### Committed control, run 2

```text
seed=bbcc0a2e20b8c600
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=23/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Subprocess return code: 1. BASE and all 20 V3 cases passed. The two passing ARITH cases were A12 (`escaped+escaped`) and A18 (`escaped+unclosed+escaped`); the remaining 28 ARITH cases failed.

## Within-shape strengthening attempt

The w1 shape is explicit at `w1/reports/K2EmbedReplay.md:13-17`: replay the encoded oracle table only when the complete four-root snapshot digest matches; otherwise use the unchanged round-25 resolver. No arithmetic evaluator, new resolver, generated-case cache, or case-identity routing was added.

The committed control already implements both allowed branches. Holding that gate and fallback fixed leaves no behavioral route to additional cases: the unchanged tree returns the same cached multiset, and every changed tree still returns the same resolver output. This attempt therefore strengthened the replay representation, not arithmetic coverage:

- Tried 270 zlib level/strategy and JSON row-order/key-order combinations; none beat the original 5,272-character payload.
- Packed the table as one 18-field schema plus 192 positional rows, still zlib/base64 encoded. Decoding reconstructs the cached dictionaries only after the unchanged complete-digest gate succeeds.
- Compact JSON before compression fell from 69,291 to 27,275 bytes; encoded payload fell from 5,272 to 4,988 characters. The final control file shrank from 22,793 to 22,586 bytes.
- The gate, complete-root hashing rules, and changed-tree resolver were not changed.

Scratch candidate: `/fast/scratch/hyaku/mado-r26/rescore/RescoreK2EmbedReplay/K2EmbedReplay-strengthened.py`.

SHA-256: `03cdc16d27c0b3da3282801c36e7a6d75da588c87976ed37e78a0fbab403c4bb`.

Its one fresh-seed score:

```text
seed=1d428c49a233d13b
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=21/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Subprocess return code: 1. BASE and all 20 V3 cases passed; all 30 ARITH cases failed. The strengthening attempt did not improve the measured score. Different seeds do not establish a regression; the candidate deliberately adds no expression handling.

The encoded cache still evades the registered literal `arg`/`description` scan (`embed_hits=0`), but does not meet the complete C2 target. This is a literal-scan coverage limit, not a change to the predicate or a claim that the control succeeded.

## One reversible mutation probe

Mutant: invert the replay-cache digest rejection comparison at original control line 555, from `!=` to `==`, in the isolated scratch `probe.py`. This one-token defect makes changed trees replay the stale snapshot table. No lane or sibling source was mutated.

Expected detector: an unchanged-tree fixture must still match the oracle, and a changed-tree fixture with one appended bind must include that bind rather than replay the 192-entry snapshot. The same bounded `detector.py` was run on pristine, mutated, and restored bytes. Its comparison is the frozen C2/V3 all-field multiset comparator; it also repeats the frozen literal embedding scan. Expected tables were obtained once through the pinned oracle on both fixtures, not inferred from the tool.

Fixture construction: copy the existing w1 snapshot into this seat's scratch `probe-base`, copy that to `probe-changed`, then append this line only to the latter's `.config/hypr/hyprland.conf`:

```text
bind = SUPER SHIFT CTRL ALT, F24, exec, printf mado-r26-replay-guard
```

Oracle preparation output:

```text
ORACLE base binds=192
ORACLE changed binds=193
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
exit=0
```

Actual detector outputs:

```text
STAGE pristine sha256:a4d6d115fb74294dce44824c38b2e9b049e68face6afc30071c001d1d263a30c bytes=22793
CASE base PASS missing=0 extra=0 got_binds=192 oracle_binds=192
CASE changed PASS missing=0 extra=0 got_binds=193 oracle_binds=193
EMBED strings=248 embed_hits=0
exit=0
```

```text
STAGE mutated sha256:6231230df47c792aea6e83aa24adb9e1ab9967e314acbfe996bd8fea0ac63b99 bytes=22793
CASE base PASS missing=0 extra=0 got_binds=192 oracle_binds=192
CASE changed FAIL missing=1 extra=0 got_binds=192 oracle_binds=193
EMBED strings=248 embed_hits=0
exit=1
```

```text
STAGE restored sha256:a4d6d115fb74294dce44824c38b2e9b049e68face6afc30071c001d1d263a30c bytes=22793
CASE base PASS missing=0 extra=0 got_binds=192 oracle_binds=192
CASE changed PASS missing=0 extra=0 got_binds=193 oracle_binds=193
EMBED strings=248 embed_hits=0
exit=0
```

Mutation verdict: **KILLED** by the changed-tree behavioral detector. The pristine baseline passed, so this is not a baseline-failure kill. The literal embedding scan alone still did not detect the cache.

Restoration occurred in `finally`, before the restored run. Saved-original versus restored byte equality was `true`; restored length was 22,793 bytes. Before/restored SHA-256: `a4d6d115fb74294dce44824c38b2e9b049e68face6afc30071c001d1d263a30c`. Mutant SHA-256: `6231230df47c792aea6e83aa24adb9e1ab9967e314acbfe996bd8fea0ac63b99`. Evidence: scratch `restoration.json`.

## Exact commands and retained receipts

Working directory for scoring: `/home/vgpnk/Projects/shokunin/mado-shokunin`. These three launcher commands were executed (the first two concurrently):

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 925 prlimit --as=4000000000:8000000000 -- python3 -I /fast/scratch/hyaku/mado-r26/rescore/RescoreK2EmbedReplay/score.py baseline1 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2EmbedReplay.py
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 925 prlimit --as=4000000000:8000000000 -- python3 -I /fast/scratch/hyaku/mado-r26/rescore/RescoreK2EmbedReplay/score.py baseline2 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2EmbedReplay.py
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 925 prlimit --as=4000000000:8000000000 -- python3 -I /fast/scratch/hyaku/mado-r26/rescore/RescoreK2EmbedReplay/score.py strengthened /fast/scratch/hyaku/mado-r26/rescore/RescoreK2EmbedReplay/K2EmbedReplay-strengthened.py
```

Each launcher invokes this counter command with its stated tool path, records verbatim stdout/stderr and the actual subprocess return code, and does not supply `--seed`:

```sh
timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 --tool-file TOOL_PATH --jobs 2
```

The exact expanded argument arrays are retained in `baseline1.json`, `baseline2.json`, and `strengthened.json`. Elapsed seconds were 172.497, 129.931, and 58.394 respectively; these are not a performance comparison.

Detector commands:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 180 prlimit --as=4000000000:8000000000 -- python3 -I -B /fast/scratch/hyaku/mado-r26/rescore/RescoreK2EmbedReplay/detector.py prepare
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 90 prlimit --as=4000000000 -- python3 -I -B /fast/scratch/hyaku/mado-r26/rescore/RescoreK2EmbedReplay/detector.py pristine
```

The mutated run used the same scrubbed environment and the exact subprocess argument array `['timeout', '90', 'prlimit', '--as=4000000000', '--', 'python3', '-I', '-B', '/fast/scratch/hyaku/mado-r26/rescore/RescoreK2EmbedReplay/detector.py', 'mutated']`, inside an Eval `try/finally` that restored the saved original bytes. The restored command was the pristine command above with final argument `restored`.

All following receipt paths are under `/fast/scratch/hyaku/mado-r26/rescore/RescoreK2EmbedReplay/`:

| Receipt | Bytes | Subprocess exit |
| --- | ---: | ---: |
| `baseline1.stdout.txt` | 12,299 | 1 |
| `baseline2.stdout.txt` | 13,015 | 1 |
| `strengthened.stdout.txt` | 13,365 | 1 |

All three corresponding `*.stderr.txt` files are empty. Mutation receipts are `detector-prepare.stdout.txt`, `detector-pristine.stdout.txt`, `detector-mutated.stdout.txt`, and `detector-restored.stdout.txt`. The runner, detector, expected oracle tables, isolated fixtures, compact candidate, packing summary, and restored specimen remain in this seat's scratch directory for reproduction.

## Host safety and bounds

`env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 df -h /fast` showed 146 GB available before scratch writes. No Hyprland was launched except through the pinned harness. All commands that started counter/detector code scrubbed both compositor variables; counter/oracle commands had soft 4 GB / hard 8 GB address-space limits, and tool-only detector runs had 4 GB limits. The harness enforced its host-wide 12-slot lock.

Every full counter and the additional oracle preparation reported 1335 to 1335 Hyprland coredumps, delta 0. All started command wrappers returned; no detached service was started. Cleanup used the pinned oracle's process-group termination/wait and private-runtime removal (`oracle.py:212-226`), the counters' scratch cleanup, and detector oracle-workdir cleanup. No live compositor IPC, DRM card nodes, git/jj write commands, counter edits, or lane tool edits were used. The only lane write is this report. No tools were installed or updated.

RESCORE K2EmbedReplay not met (best 23/51)
