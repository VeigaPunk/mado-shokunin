# RescoreK1SnapshotCache — C1 counter v2

RESCORE K1SnapshotCache not met (best 2/41)

Best means this assignment's fresh runs, not the pre-existing L1 receipt. The committed reference `controls/v2/K1SnapshotCache.txt` recorded 4/41 with seed `72d13a4e7200c4dd`; that receipt is unchanged. Neither the two requested re-scores nor the one strengthened attempt met 41/41.

## Scope and expected detector

Axes: exact C1-v2 score, cache-only shape, immutable lane programs, host isolation, reproducible receipts.

Ran the unchanged `.ufo/waves/round-26/c1/count-v2.py` at revision `1b0b91e9889cbf984b052f5de564db78330a72aa`. The detector compares both complete animation-node and bezier sets against isolated Hyprland for BASE, 20 APPEND, 10 EDIT and 10 SYNTH cases; only 41/41 meets the target. The two requested re-scores used the committed control directly, without edits. All four executions below omitted `--seed` and printed distinct fresh seeds.

## Actual outputs

Full stdout receipts are under `/fast/scratch/hyaku/mado-r26/rescore/RescoreK1SnapshotCache/`.

| Execution | Receipt | Seed | Passes | Counter exit |
| --- | --- | --- | --- | --- |
| Requested re-score 1, pristine committed bytes | `rescore-1.txt` | `2776b79fd6075ba1` | 2/41 | 1 |
| Requested re-score 2, pristine committed bytes | `rescore-2.txt` | `df7b7cb681b1b579` | 1/41 | 1 |
| Strengthened cache-only attempt | `strengthened.txt` | `ba821ec565ab4232` | 1/41 | 1 |
| Additional restored-byte detector run | `restored.txt` | `a1bd4dd60bfd81cf` | 2/41 | 1 |

Requested re-score 1, verbatim predicate and exit:

```text
PRED-C1-r26-v2 cases_pass=2/41 verdict=TARGET_MISSED
exit=1
```

Requested re-score 2:

```text
PRED-C1-r26-v2 cases_pass=1/41 verdict=TARGET_MISSED
exit=1
```

Strengthened attempt:

```text
PRED-C1-r26-v2 cases_pass=1/41 verdict=TARGET_MISSED
exit=1
```

Restored-byte run:

```text
PRED-C1-r26-v2 cases_pass=2/41 verdict=TARGET_MISSED
exit=1
```

Every run printed these identical guard/safety observations:

```text
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
```

Re-score 1 passed BASE and C07 (`APPEND:DISABLE+INVALID`, `changed=no`). Re-score 2 passed only BASE. Both failed every EDIT and SYNTH case. The strengthened attempt passed only BASE. The restoration run passed BASE and C24 (`EDIT:rewrite-animation+UNSOURCED`, `changed=no`). No measured run returned a setup/guard failure. Counter exits above are the counter's own `exit=` lines; the surrounding `tee` pipelines do not propagate the Python exit status.

## Strengthening attempt / mutant

The committed shape is unconditional snapshot-table replay (`w1/reports/K1SnapshotCache.md:25`). The same report explicitly allows a hash-gated static-default fallback (`:26-29`). I tried that documented variant under v2, not a config interpreter:

- Hash every regular file under `--home`, with sorted traversal, using relative path + NUL + SHA-256(content) + newline.
- Exact match to the recorded snapshot digest selects the snapshot table; any mismatch or read error selects the static-default table.
- Tables were copied from the committed `controls/K1SnapshotCache.py:5` and `controls/K1StaticDefault.py:7`. The digest was already recorded in `w1/reports/K1SnapshotCache.md:27` and matched every fresh counter snapshot.
- No parsing of directives, sources, variables, validation rules or expressions; no environment, mountinfo, case labels or runtime oracle access in the candidate. The behavior-bearing change is the final cached-table selection.

This is an attempted strengthening, not an observed improvement: it scored 1/41. Fresh seeds differ, so the scores are not a paired causal comparison. The candidate remained entirely within the previously documented cache-only/hash-fallback shape.

The scored 8,279-byte source is retained at:

`/fast/scratch/hyaku/mado-r26/rescore/RescoreK1SnapshotCache/K1SnapshotCache-hash-fallback-scored.py`

SHA-256: `e6a83a4f5bd70df889df8840b7cbd53491f8025449d4da33a908b506a17f6ad0`.

**Mutation-test verdict: inconclusive as a kill test.** The pristine control already misses the target, so the strengthened variant's miss is not counted as a killed mutant. The requested control re-score verdict is nevertheless unambiguously **not met**. No contract change is proposed.

## Exact scoring commands

Working directory for every command: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

The two original-byte runs were independent concurrent commands. Each command used two oracle workers; the unchanged harness also enforces its host-wide 12-slot lock.

```sh
timeout 900 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file .ufo/waves/round-26/controls/K1SnapshotCache.py --jobs 2 | tee /fast/scratch/hyaku/mado-r26/rescore/RescoreK1SnapshotCache/rescore-1.txt

timeout 900 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file .ufo/waves/round-26/controls/K1SnapshotCache.py --jobs 2 | tee /fast/scratch/hyaku/mado-r26/rescore/RescoreK1SnapshotCache/rescore-2.txt

timeout 900 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK1SnapshotCache/K1SnapshotCache-hash-fallback.py --jobs 2 | tee /fast/scratch/hyaku/mado-r26/rescore/RescoreK1SnapshotCache/strengthened.txt
```

After that third command completed, retained its source as `K1SnapshotCache-hash-fallback-scored.py`, restored `K1SnapshotCache-hash-fallback.py` to the exact 4,101-byte committed control, and ran the same bounded detector on the restored bytes:

```sh
timeout 900 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/rescore/RescoreK1SnapshotCache/K1SnapshotCache-hash-fallback.py --jobs 2 | tee /fast/scratch/hyaku/mado-r26/rescore/RescoreK1SnapshotCache/restored.txt
```

## Preservation and restoration evidence

No lane program was edited. Only this assigned report was written in the lane. The scratch candidate was archived and its execution path restored to the original bytes after the attempt.

| Bytes | Before / pristine SHA-256 | After / restored SHA-256 |
| --- | --- | --- |
| `controls/K1SnapshotCache.py` | `0c5672f9b4a5ca66697e7f5b8dd4b21da7dd020ae65dff00734030319daa6528` | same |
| `c1/count-v2.py` | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` | same |
| `harness/oracle.py` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` | same |
| Scratch execution path | mutant: `e6a83a4f5bd70df889df8840b7cbd53491f8025449d4da33a908b506a17f6ad0` | restored: `0c5672f9b4a5ca66697e7f5b8dd4b21da7dd020ae65dff00734030319daa6528` |

SHA-256 was recorded with `sha256sum` before and after the probe; each counter receipt independently prints its input source hash. The restored receipt reports the same original-control hash and successfully reaches the predicate.

Receipt SHA-256 values:

```text
955adfcc5d6e314004f4ece975eaa95a480429c26aeb4b4446f8b812d8677386  rescore-1.txt
25dd0d69fa81c105b34d7c46801d0a33563439fa01554a59e0f0064222d11058  rescore-2.txt
b355f4f6e414f53cfaed7b35d05c37e8adb799b23ac675a318a0e04da528dd18  strengthened.txt
cfa3dc15624e4514a4d11f99bb578e9d2d42c3ac97b0e7cd26f41bee23d795c5  restored.txt
```

Final hash command:

```sh
timeout 15 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE sha256sum .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/harness/oracle.py .ufo/waves/round-26/controls/K1SnapshotCache.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK1SnapshotCache/K1SnapshotCache-hash-fallback.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK1SnapshotCache/K1SnapshotCache-hash-fallback-scored.py /fast/scratch/hyaku/mado-r26/rescore/RescoreK1SnapshotCache/restored.txt
```

## Host safety and tooling

Before scratch writes:

```sh
timeout 10 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE df -h /fast
timeout 10 env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE mkdir -p /fast/scratch/hyaku/mado-r26/rescore/RescoreK1SnapshotCache
```

`df` reported `/dev/nvme1n1p2`, 804G total, 658G used, 146G available, 82% used. Scratch source and receipts are small bounded files.

Hyprland was started only through the pinned counter/oracle, with the two live-session environment variables removed from every started shell command. No live compositor command, package transaction, service restart, git/jj write, sibling edit or subagent dispatch was performed. All four bounded process jobs completed. Oracle process-group termination and wait occur in `harness/oracle.py:212-224` before each oracle call returns; counter scratch removal occurs in `c1/count-v2.py:375-376`. Every receipt recorded coredump delta zero. No tools were installed or updated.
