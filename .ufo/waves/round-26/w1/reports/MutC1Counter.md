# MutC1Counter — frozen C1 counter mutation probe

## Verdict

**12 mutants KILLED; 0 SURVIVED; 0 INCONCLUSIVE.** The pristine detector passed, every mutant changed at least one required outcome, and every individually restored copy passed the same detector. No lane counter, lane harness, or tool implementation was changed or executed as a mutant.

Surviving mutants: **none** in the complete detector. This is a scratch counter-sensitivity probe, not a C1 control receipt or an implementation of the animation-table resolver.

## Scope and method

Axes: comparison sensitivity, the complete 41-case population, the BASE stability guard, actual-oracle provenance, exact restoration, and host isolation.

Scratch root, abbreviated `S` below:

`/fast/scratch/hyaku/mado-r26/mut/MutC1Counter`

Copied the counter to `S/c1/count.py` and the complete harness directory to `S/harness/`, preserving their relative layout. The only baseline adaptation was `count.py:30`: `LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"`. `ORACLE_PATH` remained relative and resolved to the scratch harness; the oracle pin was not changed. `LANE` was used for the counter's read-only revision lookup. No git/jj write commands were run.

Created two privileged Python adapters, `S/PERFECT.py` and `S/NEAR_MISS.py`, and monkeypatched only the imported scratch counter's `O.run_tool` to use them. These adapters receive actual oracle tables; they do not resolve config files and do not demonstrate a real tool meeting C1.

First, the pristine copy generated all cases with seed `c12620261023` and REV `05319e0f` (resolved `05319e0fed2ce25cf0a883380af2763a85fd4936`). Its copied, pinned `oracle()` made **42 actual nested-oracle calls**: BASE, 40 generated cases, and the independent second BASE. The 79-file home snapshot was frozen in `S/fixture-home`. Every subsequent detector run regenerated cases from that snapshot and replayed only actual oracle outputs indexed by a SHA-256 digest of each case's relative paths and exact file bytes. An unknown case digest fails instead of inventing an expectation. The real oracle was not restarted for each mutant.

Actual capture output, from `S/evidence/capture/P.txt`:

```text
seed=c12620261023
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26 cases_pass=41/41 verdict=TARGET_MET
exit=0
```

The capture command also printed:

```text
CAPTURE actual_oracle_calls=42 unique_trees=41 corpus_sha256=fe3a5d5ab6454ae4d836c616a5b9f6a1bd7f3e018096f97dc03ab90e3afed316
```

Raw oracle outputs and both BASE observations are retained in `S/evidence/oracle-corpus.json`.

### Detector and tool variants

`S/probe.py` executes the scratch counter's complete `main()`, captures stdout including `exit=`, and checks exit status, verdict, exact passed count, and exact population. One shared pristine suite covers the 12 byte-identical initial mutation copies; their hashes were recorded before mutation. The mutated suite and restored suite each ran all 12 variants separately on each of the 12 files: **12 pristine + 144 mutated + 144 restored detector invocations**, in addition to the real-oracle capture.

| Column | Adapter / injected condition | Required pristine and restored outcome |
| --- | --- | --- |
| P | PERFECT: the case's unmodified oracle table | `41/41 TARGET_MET`, exit 0 |
| NN | NEAR_MISS: change one node's `name` | `0/41 TARGET_MISSED`, exit 1 |
| NO | Change one node's `overridden` | `0/41 TARGET_MISSED`, exit 1 |
| NB | Change one node's `bezier` reference | `0/41 TARGET_MISSED`, exit 1 |
| NE | Change one node's `enabled` | `0/41 TARGET_MISSED`, exit 1 |
| NS | Change one node's `speed` by 0.00001, choosing the sign to preserve integer rounding | `0/41 TARGET_MISSED`, exit 1 |
| NT | Change one node's `style` | `0/41 TARGET_MISSED`, exit 1 |
| BD | Drop exactly one bezier; leave all nodes unchanged | `0/41 TARGET_MISSED`, exit 1 |
| XN | Add exactly one complete node with a new name | `0/41 TARGET_MISSED`, exit 1 |
| LS | Change one node's style only in C04–C39 | `5/41 TARGET_MISSED`, exit 1 |
| SS | Change one node's style only in C39 | `40/41 TARGET_MISSED`, exit 1 |
| DR | PERFECT, but synthetically change one node name only in the replayed second BASE oracle response | `ORACLE_UNSTABLE`, exit 2, no measured verdict |

Each affected NEAR_MISS case has one node field changed, one bezier removed, or one extra node; the expected table is never modified. DR is an explicit injected oracle-drift fixture, **not** an assertion that the actual oracle drifted. Its expected exit 2 is a passing guard test, not a failed measurement baseline.

## Mutants and kill table

Every mutant changes one behavior-bearing source line. Exact before/after text and line numbers are in `S/evidence/mutations.json`; file stems match these IDs.

| ID | Defect |
| --- | --- |
| M01_drop_beziers | Line 276: drop `and gb == eb` |
| M02_ignore_overridden | Line 35: omit `overridden` from NODE_FIELDS |
| M03_ignore_style | Line 35: omit `style` |
| M04_names_only | Line 35: reduce NODE_FIELDS to `("name",)` |
| M05_round_speed | Line 186: compare `round(speed)` instead of exact speed |
| M06_skip_base_guard | Line 255: disable the BASE disagreement condition |
| M07_cases_four | Line 34: NCASES 40 → 4 |
| M08_ninety_percent | Line 286: accept `npass >= 0.9 * len(built)` |
| M09_allow_extra_nodes | Line 276: replace node equality with `en <= gn` |
| M10_ignore_enabled | Line 35: omit `enabled` |
| M11_ignore_node_bezier | Line 35: omit the node's `bezier` reference |
| M12_ignore_speed | Line 35: omit `speed` |

Cell codes preserve actual outputs: `A41` = `41/41 TARGET_MET`, exit 0; `A40` = `40/41 TARGET_MET`, exit 0; `R0`, `R5`, `R40` = respectively `0/41`, `5/41`, `40/41 TARGET_MISSED`, exit 1; `G` = `ORACLE_UNSTABLE`, exit 2, no measurement. Explicit `/5` codes use a five-case population. **K:** marks a detector-killing deviation; unprefixed cells match the required outcome. A mutant is killed only because its pristine baseline and exact-byte restored suite both pass.

| Counter | P | NN | NO | NB | NE | NS | NT | BD | XN | LS | SS | DR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pristine / every restored copy | A41 | R0 | R0 | R0 | R0 | R0 | R0 | R0 | R0 | R5 | R40 | G |
| M01 | A41 | R0 | R0 | R0 | R0 | R0 | R0 | **K:A41** | R0 | R5 | R40 | G |
| M02 | A41 | R0 | **K:A41** | R0 | R0 | R0 | R0 | R0 | R0 | R5 | R40 | G |
| M03 | A41 | R0 | R0 | R0 | R0 | R0 | **K:A41** | R0 | R0 | **K:A41** | **K:A41** | G |
| M04 | A41 | R0 | **K:A41** | **K:A41** | **K:A41** | **K:A41** | **K:A41** | R0 | R0 | **K:A41** | **K:A41** | G |
| M05 | A41 | R0 | R0 | R0 | R0 | **K:A41** | R0 | R0 | R0 | R5 | R40 | G |
| M06 | A41 | R0 | R0 | R0 | R0 | R0 | R0 | R0 | R0 | R5 | R40 | **K:A41** |
| M07 | **K:A5/5** | **K:R0/5** | **K:R0/5** | **K:R0/5** | **K:R0/5** | **K:R0/5** | **K:R0/5** | **K:R0/5** | **K:R0/5** | **K:A5/5** | **K:A5/5** | G |
| M08 | A41 | R0 | R0 | R0 | R0 | R0 | R0 | R0 | R0 | R5 | **K:A40** | G |
| M09 | A41 | R0 | R0 | R0 | R0 | R0 | R0 | R0 | **K:A41** | R5 | R40 | G |
| M10 | A41 | R0 | R0 | R0 | **K:A41** | R0 | R0 | R0 | R0 | R5 | R40 | G |
| M11 | A41 | R0 | R0 | **K:A41** | R0 | R0 | R0 | R0 | R0 | R5 | R40 | G |
| M12 | A41 | R0 | R0 | R0 | R0 | **K:A41** | R0 | R0 | R0 | R5 | R40 | G |

M07's `R0/5` cells are population failures, not false acceptance of a bad table. LS additionally gives a behavioral bypass witness: all omitted cases contain an error, yet the reduced counter declares `5/5 TARGET_MET`.

### Located output witnesses

- `S/evidence/mutated/M01_drop_beziers/BD.txt:6`: `CASE BASE  PASS nodes missing=0 extra=0 beziers missing=1 extra=0 (unperturbed)`.
- `S/evidence/pristine/count/DR.txt:5–6`: `SETUP_ERROR ORACLE_UNSTABLE two oracle runs of the unperturbed snapshot disagree`, then `exit=2`.
- `S/evidence/mutated/M06_skip_base_guard/DR.txt:48–49`: `PRED-C1-r26 cases_pass=41/41 verdict=TARGET_MET`, then `exit=0` for that same injected drift.
- `S/evidence/mutated/M07_cases_four/LS.txt:12–13`: `PRED-C1-r26 cases_pass=5/5 verdict=TARGET_MET`, then `exit=0`.
- `S/evidence/mutated/M08_ninety_percent/SS.txt:46,48–49`: C39 is `FAIL nodes missing=1 extra=1 beziers missing=0 extra=0`, but the verdict is `cases_pass=40/41 verdict=TARGET_MET`, `exit=0`.

Final survivors: none. Coverage sensitivities demonstrated by the matrix: stable-oracle PERFECT and ordinary all-case near misses alone leave M06 unexercised; DR is necessary. All-case failures alone also cannot distinguish the 90% threshold mutant; SS is necessary. No contract was weakened to obtain these kills.

## Restoration and hashes

The shared adapted pristine hash, **B**, is:

`06d2086236c7d5250962d412b41b43a45ead1d95aca16627fc0a1f1199ceee02`

For **each** of the 12 mutation files: before hash = B, after restoration hash = B, and all 12 restored detector scenarios passed. Restoration reversed the exact one-line mutation, not the permitted LANE adaptation.

| Mutant | Mutated SHA-256 | Before / restored |
| --- | --- | --- |
| M01 | `f6cc5a24cb8b8cef2231056ce3a36ce32909bf1c4007762fcfcadcd3a67d86ff` | B / B |
| M02 | `5962a54aa4ab9cb438b07bfc17a2eeaacb14432f84500c6084e63fd2a358be29` | B / B |
| M03 | `03058f71dcfaa3fabf8c3ed135dfffbc9783f4f2c29a49dac2d848c16a5d65e1` | B / B |
| M04 | `fd0d0f3d231994498e792969619655c248f466498c4baef127793a37b189886a` | B / B |
| M05 | `5ddeee7b05c59731f2eb035ad38f1a17b14e6b73918e7298e77f84635f2529b2` | B / B |
| M06 | `c6de3290cacbfe212d0e87ae6c6dcdd708322613e28d36b9e6d88d5d019bda6f` | B / B |
| M07 | `23d2f497f9b1a827250379a53e860cbcf54193301f7734d05663a5fad438cf20` | B / B |
| M08 | `6df90188589221584025a5f92aa56d4ba3fb08420dbb68761a475dcaed49014d` | B / B |
| M09 | `b5c6d454a445a3587821498c1511d7f83c3b62934cd457d2020993f01c1bbb13` | B / B |
| M10 | `2cf7c2353e71ef64cef7ba38f31817313eabc199eea09e61073467e5020384c0` | B / B |
| M11 | `1b6ca1ac07694c711569ddb52043ca835c1d4e6b0132bdaf8161fc745a3dbd68` | B / B |
| M12 | `41d1a4488372406ee9476861a2da86ba2140fbbdeeec0c691c96e94ff2e4a100` | B / B |

The lane counter remained `f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd`; lane and scratch `harness/oracle.py` remained `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441`. These hashes were checked in the capture, pristine, mutated, restored, and summary phases.

Machine-readable evidence:

- `S/evidence/initial-hashes.json`: all pre-mutation copy hashes and frozen lane pins.
- `S/evidence/pristine.json`, `mutated.json`, `restored.json`: scenario outcomes, receipt paths, counter hashes, and phase hash maps.
- `S/evidence/summary.json`: per-mutant KILLED verdict, killing columns, full before/mutated/after hashes, and `restored_exactly: true`.
- Complete stdout receipts, including `exit=`, at `S/evidence/pristine/count/<column>.txt`, `S/evidence/mutated/<mutant>/<column>.txt`, and `S/evidence/restored/<mutant>/<column>.txt`.
- `S/evidence/mutations.json`: all exact mutation definitions, retained after restoring the executable copies.

## Exact detector commands and safety

All commands below used working directory `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 python3 -I /fast/scratch/hyaku/mado-r26/mut/MutC1Counter/probe.py --phase capture
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 python3 -I /fast/scratch/hyaku/mado-r26/mut/MutC1Counter/probe.py --phase pristine
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 python3 -I /fast/scratch/hyaku/mado-r26/mut/MutC1Counter/probe.py --phase mutated
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 python3 -I /fast/scratch/hyaku/mado-r26/mut/MutC1Counter/probe.py --phase restored
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 30 prlimit --as=4000000000:8000000000 python3 -I /fast/scratch/hyaku/mado-r26/mut/MutC1Counter/probe.py --phase summarize
```

Between pristine and mutated phases, the editor applied the 12 single-line changes recorded in `mutations.json`; between mutated and restored phases, it reversed those exact changes. All files were restored before any restored detector run. The summary command printed KILLED and `restored_exactly=True` for all 12 IDs.

Before copying or capturing, the bounded `df -h /fast` check reported 186G available. Commands cleared the two display variables and had timeouts and memory caps. Per L1's safety correction, the detector's address-space limit was soft 4 GB / hard 8 GB, allowing the pinned oracle to set its required 8 GB limit. All 42 actual compositor launches went through the copied, byte-identical `harness/oracle.py`, with its private headless tinywl/bubblewrap setup and render node only. Each call completed through the harness's process-group cleanup (`oracle.py:212–226`); replay phases launched no compositor. All started detector commands completed. Tool installs/updates: none.

Report: .ufo/waves/round-26/w1/reports/MutC1Counter.md
