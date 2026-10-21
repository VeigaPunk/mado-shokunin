# ReviewRuntimeV3-4 — partly falsified: v3.1 handles 10,001-deep calls without new exit-2s, but per-statement snapshots drive shallow 20k-statement inputs past 1.8 GiB RSS

## Findings

### High — per-statement snapshots cause a quadratic memory blow-up on wide, literal-binding cells

**Reproducer** (one input per child; hard stop when sampled RSS exceeds 1,800 MiB):

```sh
python3 /tmp/mado-r20a2-ReviewRuntimeV3/measure.py \
  --tools 1f7f995=/tmp/mado-r20a2-ReviewRuntimeV3/revs/tw-1f7f995.py \
          28c6837=/tmp/mado-r20a2-ReviewRuntimeV3/revs/tw-28c6837.py \
          a8960de=/tmp/mado-r20a2-ReviewRuntimeV3/revs/tw-a8960de.py \
  --inputs /tmp/mado-r20a2-ReviewRuntimeV3/focused-inputs.txt \
  --out /tmp/mado-r20a2-ReviewRuntimeV3/out/focused.jsonl \
  --timeout 120 --rss-cap-mb 1800
```

The five focused inputs are under `/tmp/mado-r20a2-ReviewRuntimeV3/fixtures/`; list digest: `cefdbae8a8605dabc26d94f83a5f25e8b49d4edf8b233be0d1c843ad5084e01a`. Relevant inputs and SHA-256:
Tool bytes used: `1f7f995` SHA-256 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`; `28c6837` SHA-256 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`; `a8960de655e6ea8c0a3bf74f5542041d9fe25b39` SHA-256 `a57d4fe9277ff06c9b5916fc731e91f05bcd69cf05639cb2090ebcb00b5b6458`.

- `/tmp/mado-r20a2-ReviewRuntimeV3/fixtures/advcrash_huge_many_stmts.jsonl` — `9cf69f6fcd121aa90269ca814ac16ab63e9c8f445a7a2f42ba1177fd9b1d619d` (byte-identical to `.ufo/waves/round-20/w2/AdvCrash/fixtures/huge_many_stmts.jsonl`, 777,987 bytes).
- `/tmp/mado-r20a2-ReviewRuntimeV3/fixtures/per_statement_snapshot_5000.jsonl` — `edbd3eb64c1018f0f18d3b99c83ce2bc8d526df8a84aa189e1e61db6f9b8db5e`.
- `/tmp/mado-r20a2-ReviewRuntimeV3/fixtures/wide_statements_20000.jsonl` — `9c8ca36ef21db114bdad826a9900b17cac7314e180b2b4f5ff81b913382092de`.
- `/tmp/mado-r20a2-ReviewRuntimeV3/fixtures/wide_helpers_2600_mutual.jsonl` — `16547328717d0c0b0064a8e30ec63ec35a95ce29a74a600f85fdf87063e20511`.

[INFERENCE] Large, shallow literal-binding cells should complete without a new multi-GiB allocation or harness cap; `.ufo/waves/round-20/w2/AdvCrash/fixtures/huge_many_stmts.jsonl` is 50,000 assignment-only statements, while the synthetic large cells append a harmless `/bin/echo` call. Expected scanner label for these inputs is `clean`, exit 0.

**Observed:** the earlier revisions completed those inputs cleanly; v3.1 was killed after exceeding the 1,800 MiB RSS cap. The `-9` status below is the harness's SIGKILL, not a `mado-tripwire` exit-2 verdict. The 5,000-binding case completes but uses about 18× the older RSS.

| Input | `1f7f995` exit / wall / peak RSS | `28c6837` exit / wall / peak RSS | `a8960de` exit / wall / peak RSS / verdict |
|---|---:|---:|---:|
| AdvCrash `huge_many_stmts.jsonl` | `0 / 0.758s / 165.3 MiB` | `0 / 0.767s / 166.2 MiB` | `-9 / 1.329s / 1,821.1 MiB / harness-capped` |
| synthetic 20,000 shallow assignments | `0 / 0.305s / 79.1 MiB` | `0 / 0.320s / 80.3 MiB` | `-9 / 0.817s / 1,812.7 MiB / harness-capped` |
| synthetic 5,000 literal bindings | `0 / 0.102s / 36.2 MiB` | `0 / 0.102s / 37.5 MiB` | `0 / 0.362s / 664.3 MiB / clean` |
| 2,600 mutually referencing helpers | `0 / 0.240s / 70.8 MiB` | `0 / 3.520s / 347.5 MiB` | `0 / 1.070s / 786.8 MiB / clean` |

**Cause evidence:** at `a8960de`, `tools/mado-tripwire.py:1870-1902` makes `dict(env)` and `dict(bindings)` for every statement (`1882`) and retains each snapshot through every `Call`, `Name`, `Attribute`, and `Lambda` node in that statement (`1883-1886`). Unique literal assignments grow `env`; their retained snapshots therefore duplicate progressively larger dictionaries. [INFERENCE] This yields quadratic retained snapshot storage in the number of bindings/statements. At `28c6837`, `tools/mado-tripwire.py:1732-1758` copied environments only for `ast.Call` nodes (`1741-1743`), so assignment-only statements did not retain snapshots. The per-cell `DESCENT_BUDGET = 2000` at v3.1 `tools/mado-tripwire.py:1991-1997` does not bound this allocation: these inputs need no helper descents.

### Synthetic runtime cases (all revisions; timings are wall seconds, RSS is MiB)

| Case and input SHA-256 | `1f7f995` | `28c6837` | `a8960de` |
|---|---|---|---|
| 9,500 nested calls; `deep_call_nesting_9500.jsonl`, `244630a533f3bbe2c188d4ad3d371525b09829617e28fda068664a2ec4a56a88` | `0 clean / .031s / 21.7` | `0 clean / .036s / 24.4` | `0 clean / .036s / 24.7` |
| 10,001 nested calls; `deep_call_nesting_10001.jsonl`, `48d12cd04bb65d6ef5d378ba9cd74974146f5aef6219963986a64b3604d791c3` | `0 clean / .031s / 22.1` | `0 clean / .036s / 24.1` | `0 clean / .036s / 24.2` |
| 120 classes × 29 dunders; `many_classes_120x29_dunders.jsonl`, `a1d2e6726aa0c3064b9e9d8cc1efb30516e77a9d57e5552d4fac48a4931cab4c` | `0 clean / .311s / 63.4` | `0 clean / .210s / 64.5` | `0 clean / .550s / 63.7` |
| 2,400 helper calls exhausting the cell budget; echo-only canary `budget_exhaustion_2400_echo_canary.jsonl`, `016a625081339bea5bb551a3dbb5dfb7fc31df74f5389036d96242651afd0de7` | `1 findings / .367s / 54.1` | `1 findings / .536s / 239.8; observed=1, lead=0` | `1 findings / .561s / 243.3; observed=1, lead=1` |

The budget canary uses only `sudo /bin/echo harmless-*` as inert transcript data; it was scanned, never executed. The v3.1 observed+lead split is consistent with following calls until the 2,000-descent budget is spent, then sweeping the remaining bodies. Stack/recursion constants are `512 * 1024 * 1024` and `50000` at `tools/mado-tripwire.py:2890-2911`; both 9,500- and 10,001-level synthetic call expressions scan cleanly at all three revisions.

## Corpus measurements

### AdvCrash

All 172 `.ufo/waves/round-20/w2/AdvCrash/fixtures/*.jsonl` and `fixtures2/*.jsonl` inputs were run one file per process at each revision (516 scans total). Exit distributions include the harness-cap termination separately.

| Revision | exit 0 | exit 1 | exit 2 | harness SIGKILL | total wall | median | p95 | max wall / input | max RSS | files >5s |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| `1f7f995` | 136 | 25 | 11 | 0 | 90.605s | .030887s | .056451s | 82.226s `huge_bash_cmd.jsonl` | 234.0 MiB | 1 |
| `28c6837` | 127 | 21 | 24 | 0 | 91.672s | .030919s | .061606s | 82.987s `huge_bash_cmd.jsonl` | 235.3 MiB | 1 |
| `a8960de` | 137 | 31 | 3 | 1 | 101.476s | .036018s | .064426s | 82.813s `huge_bash_cmd.jsonl` | 1,803.4 MiB | 1 |

There was **no v3.1 exit-2 on an input that had exited 0/1 at both older revisions**. The one v3.1 cap termination was `huge_many_stmts.jsonl` (above). The only >5s AdvCrash input was `huge_bash_cmd.jsonl`: exit 0 at every revision, 82.226/82.987/82.813s respectively (input SHA-256 `0e73ec4cf310e8a0b5c813151614464278333a0ba64a80cbb85df670baf05c2d`; copied to `/tmp/mado-r20a2-ReviewRuntimeV3/fixtures/advcrash_huge_bash_cmd.jsonl`). `deep_binop_50k.jsonl` still produces `internal RecursionError` / exit 2 at all revisions, not a new v3.1 exit-2 (0.082/0.082/0.205s; input SHA-256 `b86476a4057e1d5720ee8d0fb4fd8bf3f5f75c32866207d78e71be02827830ae`).

Complete per-file exits, labels, wall times, RSS, and input hashes: `/tmp/mado-r20a2-ReviewRuntimeV3/advcrash-per-file.tsv` (SHA-256 `5074aa1619767c36e4f91f99185d2eb922d1066806031423edd52a7876d95929`); input manifest `/tmp/mado-r20a2-ReviewRuntimeV3/advcrash-manifest.tsv` (SHA-256 `4095d7c3bed0143ebff8ae60135fd8dfef9cff2e6df3a18b4600dab38b4daa48`). Raw run results: `/tmp/mado-r20a2-ReviewRuntimeV3/out/advcrash.jsonl` (SHA-256 `fa756048f4435b2fa8fd7b0b446b9de1dbd09bdad6e9704eae115d75a4aabbfc`).

### 300 aged session transcripts

The deterministic sample used seed `20261021`: 300 of 7,404 eligible regular `.jsonl` files under `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`, all older than the recorded cutoff `2026-10-21T06:10:24.724Z`. Their SHA-256 values were rechecked after scanning; zero changed. Each file was scanned in a separate child at all three revisions (900 scans).

| Revision | exit 0 | exit 1 | exit 2 / cap / timeout | total wall | median | p95 | max wall / input | max RSS | files >5s |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| `1f7f995` | 215 | 85 | 0 | 12.210s | .040742s | .061194s | .091847s | 45.4 MiB | 0 |
| `28c6837` | 217 | 83 | 0 | 13.485s | .041038s | .071449s | .106801s | 47.2 MiB | 0 |
| `a8960de` | 217 | 83 | 0 | 14.039s | .045863s | .071512s | .112029s | 47.6 MiB | 0 |

Slowest sampled file (still <0.12s): `2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR20/MadoR20.SimplifyRuleB-3.jsonl`, SHA-256 `9bf943e6a2dcd64cc2dd313583c7e551069083fdd1fa24f08e715b9d7d1f5e41`; it exited 0 (`clean`) at all three revisions, with wall times 0.091847/0.106801/0.112029s.

Complete per-file exits, labels, wall times, RSS, and input hashes: `/tmp/mado-r20a2-ReviewRuntimeV3/sessions-300-per-file.tsv` (SHA-256 `c9f44bca6a82d72f8eadbe2c8dcdd9b1f53121beb564bc6e32c6e08d5fd82282`). The exact sample manifest with paths, mtimes, sizes, hashes, and cutoff is `/tmp/mado-r20a2-ReviewRuntimeV3/sessions-sample.tsv` (SHA-256 `e4ffe77dc3ec75e5cd6f8998a5b7a6014bd127d27af8fe09c51d7f2a287739c0`); raw run results: `/tmp/mado-r20a2-ReviewRuntimeV3/out/sessions-300.jsonl` (SHA-256 `9106df656cbb63c3ef18084f5cdb4d2fb604f089abeaff8294b56aa05269f573`).

## Limits

- Python 3.14.8 on Linux x64. Each wall time includes interpreter startup; runs were sequential but not on an otherwise isolated host, so small timing deltas are noisy. Peak RSS is each child’s `wait4` `ru_maxrss`; the harness sampled `/proc/<pid>/status` every 5 ms and killed at 1,800 MiB, so cap-case peaks overshoot the threshold slightly. No unrestricted multi-GiB rerun was attempted.
- No timeouts at the 120s per-input limit. `huge_bash_cmd.jsonl` is an 82–83s common slow case, not a v3.1 regression; the 300-session sample had no >5s file.
- The 50,000-binop AdvCrash case remains an exit-2 `RecursionError` in all three revisions; the requested 10,001-deep call cases succeeded. No new scanner-generated exit-2 was observed; the only new failure mode was harness-capped memory exhaustion.
- No `lsp` device is mounted (`read xd://lsp` returned “No such tool”), so no LSP caller/definition/diagnostics pass was available; this assignment was runtime measurement plus source-line cause evidence, not a caller-graph review. The lane was not edited except for this report. Transcript contents and echo canaries were scanned as data and never executed.
- Full per-file tables and raw JSONL results are under `/tmp/mado-r20a2-ReviewRuntimeV3/`; the report cites their hashes above.

## Installs

none
