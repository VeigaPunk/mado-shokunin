# RescoreK1PrefixKeyed — C1 v4 fresh-seed rescore and one-point shortcut probe

RESCORE K1PrefixKeyed.py best: PRED-C1-r27-v4 cases_pass=20/41 verdict=TARGET_MISSED
RESCORE K1GlobalOnce.py best: PRED-C1-r27-v4 cases_pass=19/41 verdict=TARGET_MISSED
RESCORE K1FileScope.py best: PRED-C1-r27-v4 cases_pass=31/41 verdict=TARGET_MISSED
SHORTCUT best: PRED-C1-r27-v4 cases_pass=41/41 verdict=TARGET_MET — met

## Scope and receipts

Read the frozen registration before acting. No subagents, integration, contract changes, lane-source edits, git/jj writes, or tool installations. The only lane write is this assigned report. Axes: fresh-seed score, omitted source/variable semantics, exact restoration, and host safety.

Receipt root `R=/fast/scratch/hyaku/mado-r27/rescore/RescoreK1PrefixKeyed/`. Full commands, return codes, seeds and output are in `R/rescore-record.json`, individual `.txt` receipts, and the shortcut `.json`/`.txt` pairs. All scores use revision `2fdca5caaab6859386effbb8fa6acc5250c90633` and the unchanged frozen counter/harness.

## Six required control runs

| Committed control | Fresh seed 1 | Score | Fresh seed 2 | Score | Exit codes |
|---|---|---|---|---|---|
| K1PrefixKeyed | `99e745b409f01eb1` | 20/41 | `076cad3863da8bd0` | 15/41 | 1, 1 |
| K1GlobalOnce | `b903890fa67d666e` | 19/41 | `7fd383483f5b0d69` | 18/41 | 1, 1 |
| K1FileScope | `22c39a659b314c16` | 27/41 | `593776486b87d067` | 31/41 | 1, 1 |

Each full receipt is `R/<control>-seed{1,2}.txt`. None of these committed controls met v4. Every run reported `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0`.

Exact command, executed twice for each of the three listed control paths (no `--seed`, so the counter chose fresh seeds):

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count-v4.py 2fdca5ca --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/controls/<control>.py --jobs 4
```

Orchestrator command: `env -i PATH=/usr/bin HOME=/home/vgpnk timeout 3000 python3 -I /fast/scratch/hyaku/mado-r27/rescore/RescoreK1PrefixKeyed/rescore.py`. Its first asynchronous launch was rejected by the host background-job cap; the synchronous retry completed all six measurements. Rescoring finished `2026-10-23T11:43:40.298974+00:00`.

## Shortcut: omit variable expansion in source paths

**Mutant:** preserve all other behavior of the scratch streaming reader, but replace exactly line 59:

```python
# pristine / restored
                target = expand(rhs, env)
# mutant
                target = rhs
```

The baseline starts from the small FileScope reader with child calls sharing the variable environment, rather than copying it. It follows nested/glob sources in order, expands workspace variables in position, and replays repeated sources. The single mutation leaves `$name` references literal only in `source =` paths. This is a genuine omitted hyprlang source/variable semantic, not label sniffing, a source/AST hash pin, or an oracle call by the reader.

**Generator regularity:** all generated source operands are literal `~/` paths, including GLOB, NESTED, TWICE and SRCDEF. See frozen `c1/count-v4.py:240,245,248,254,268,272,304,306,314`. Randomized variable names, embedded workspace values, use-before-definition and child definitions do not exercise a variable in a source operand. The snapshot's measured base table was `[]`.

**Expected detector:** if this semantic were covered, the frozen counter would find a source-variable case whose table differs and return `TARGET_MISSED`. Actual v4 results:

| Phase | Seed | Score | Exit | Receipt |
|---|---|---|---|---|
| Pristine | `34335be5d092ee3c` | 41/41 TARGET_MET | 0 | `R/shortcut-pristine.txt` |
| Mutant, paired | `34335be5d092ee3c` | 41/41 TARGET_MET | 0 | `R/shortcut-mutant-paired.txt` |
| Mutant, second fresh seed | `75c285743e83f12d` | 41/41 TARGET_MET | 0 | `R/shortcut-mutant-fresh.txt` |
| Exact restoration | `34335be5d092ee3c` | 41/41 TARGET_MET | 0 | `R/shortcut-restored.txt` |

The paired three phases used identical snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727` (79 files), the same seed and the same frozen bounded detector. There was no failed baseline to misclassify as a kill. Every phase reported coredump delta 0.

Each shortcut measurement used the same control command above, substituting `--tool-file R/K1SourcePathLiteral.py` and adding the table's `--seed`. Exact expanded argv arrays are in `R/shortcut-<phase>.json`. Driver commands:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 940 python3 -I /fast/scratch/hyaku/mado-r27/rescore/RescoreK1PrefixKeyed/measure-shortcut.py pristine
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 940 python3 -I /fast/scratch/hyaku/mado-r27/rescore/RescoreK1PrefixKeyed/measure-shortcut.py mutant-paired --seed 34335be5d092ee3c
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 940 python3 -I /fast/scratch/hyaku/mado-r27/rescore/RescoreK1PrefixKeyed/measure-shortcut.py mutant-fresh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 940 python3 -I /fast/scratch/hyaku/mado-r27/rescore/RescoreK1PrefixKeyed/measure-shortcut.py restored --seed 34335be5d092ee3c
```

**Verdict: SURVIVED.** This is a coverage finding. No counter, contract or candidate was integrated or changed in response.

## Independent safe semantic witness

Tree retained under `R/witness/home/`:

```ini
# .config/hypr/hyprland.conf
$folder = ~/.config/hypr
source = $folder/child.conf
# .config/hypr/child.conf
workspace = name:sourcevar, bordersize:2, rounding:false
```

The registered `oracle()` returned:

```json
[{"workspaceString":"name:sourcevar","enabled":true,"borderSize":2,"rounding":false}]
```

The mutant returned `[]`, with no tool error. After exact restoration the reader returned the oracle's table. Receipts: `R/witness-mutant.json` and `R/witness-restored.json`. One nested oracle call supplied the truth; the restored witness compared with that saved truth, not a claimed second oracle invocation. Both phases recorded host count 1338 → 1338, delta 0.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 180 prlimit --core=0 --as=4000000000:8000000000 -- python3 -I /fast/scratch/hyaku/mado-r27/rescore/RescoreK1PrefixKeyed/witness.py mutant --oracle
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 90 prlimit --core=0 --as=4000000000 -- python3 -I /fast/scratch/hyaku/mado-r27/rescore/RescoreK1PrefixKeyed/witness.py restored
```

## Byte restoration and host safety

The scratch probe file `R/K1SourcePathLiteral.py` was restored before continuing any supplemental measurements. Exact before/restored SHA-256: `bb2faf4efdf2f68f97c895f3733807341dc7bdcb70660c49e90d5fcdb788386f`. Mutated SHA-256: `3d6c10cde7bbe295489405fd27dbbe669a6fb71c548e81bffd00617109183061`. The unchanged mutant is retained separately as `R/K1SourcePathLiteral-mutant.py` for reproduction; the working probe path holds the pristine bytes.

Committed inputs were never edited; `R/rescore-record.json` records equal before/after hashes:

| Input | SHA-256 before = after |
|---|---|
| Frozen v4 counter | `635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1` |
| Frozen oracle | `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601` |
| K1PrefixKeyed | `6fb88339190ad63e3549231281d6068ff4f09d31542e8568e62dccd3fe9b05fa` |
| K1GlobalOnce | `5fe54d4992578bb69f7ceabe4af166c894e5a80a16bda43e7e811d9ba8c4ca39` |
| K1FileScope | `f56e20a77dc511b10963cf70a69c2971499244ee035d309f224525c1cd553bcb` |

`df -h /fast` before scratch writes reported 74G available. All subprocess commands use cleared environments and timeouts. Nested compositors were launched only by the pinned registered harness; its host-wide 12-slot flock cap applies. Counters use four workers. The witness used a 4 GB soft / 8 GB hard address-space limit so the pinned harness could apply its own nested 8 GB cap. No live-compositor mutation, card-node access, source cycles or overflowing numeric inputs were used. No tools were installed or updated.

## Completed 20-minute search window

After the six control runs, the single source-path mutation was built and confirmed. The rest of the assigned search window exercised that same mutant, without introducing another defect: 14 additional fresh seeds, with pristine / mutant / restored measurements for each seed. All 42 supplemental measurements returned exit 0 and `PRED-C1-r27-v4 cases_pass=41/41 verdict=TARGET_MET`. Combined with the two initial mutant seeds, the one-point shortcut met v4 on **16 distinct fresh seeds**. No baseline or restoration measurement failed.

Search window: `2026-10-23T11:43:40.298974+00:00` through `2026-10-23T12:04:16.075527+00:00`, elapsed **1235.776565 seconds**. The final already-started paired set completed 35.8 seconds after the 20-minute deadline; no further set was started. Full per-phase commands, outputs and all 14 supplemental seeds are in `R/search-window-record.json`; full receipts are `R/shortcut-window-<01..14>-<pristine|mutant|restored>.txt`.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 2700 python3 -I /fast/scratch/hyaku/mado-r27/rescore/RescoreK1PrefixKeyed/search-window.py
```

The supplemental runner reported `SEARCH_WINDOW_FINISHED elapsed_seconds=1235.776565 paired_seeds=14 baseline_restored_exactly=True`. Final SHA-256 measurements again matched every committed input and the pristine scratch hash above. `R/final-safety.json` records host Hyprland coredumps **1338 → 1338, delta 0** and no remaining process whose argv contains an absolute path under this probe's scratch directory. All bounded detector commands returned; the pinned oracle's `finally` cleanup waits for and kills its own sandbox groups.

Final disposition: **one surviving semantic mutant, exact restoration complete; no integration or contract change.**
