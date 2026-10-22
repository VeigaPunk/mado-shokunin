# BaseResource — C1 no-harm baseline: resource guards re-measured at base

Seat: MadoR23.BaseResource (leaf reviewer) · 2026-10-22 · Base commit `a28e4815aabfa85f55274884000fb2608355f8cf` (lane HEAD, `git status --porcelain tools/` empty at measurement time).

## Scope

Independent re-measurement, at the base classifier, of the round-21 and round-22 resource-guard populations in both `module-main` and `cli` modes. Expectation per assignment: all clean. All raw outputs saved under `.ufo/waves/round-23/w1/out/BaseResource/` (sha256 list at the end).

## Preparation

1. Extracted the base classifier copy (assignment-literal TOOL):

   ```
   git -C /home/vgpnk/Projects/shokunin/mado-shokunin show a28e4815aabfa85f55274884000fb2608355f8cf:tools/mado-tripwire.py \
     > /fast/scratch/hyaku/mado-r23/BaseResource/base-tool.py
   sha256sum /fast/scratch/hyaku/mado-r23/BaseResource/base-tool.py \
     /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py
   ```

   Both files: `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` — matches the registration value; lane working copy is byte-identical to the base blob.

2. `--help` screens checked before any measurement (both `EXIT=0`):
   - `.ufo/waves/round-21/resource/measure.py`: `--tool` (required), `--mode {module-main,cli}` (required), `--python` (default `sys.executable`).
   - `.ufo/waves/round-22/resource-closure-measure.py`: `--tool` (required), `--mode {module-main,cli}` (required).

3. Path constraint discovered by reading both sources before running: the round-22 harness's `selected_tool()` enforces `path.is_relative_to(REPO_ROOT)` (lines 212–213). `/fast/scratch/...` cannot be used there. Demonstrated live (see finding F1). The round-21 harness only requires a regular file, so the extracted scratch copy was used for both round-21 runs.

## Measurements (sequential, one harness process at a time; each harness runs its children one at a time; cwd = lane root)

| # | Command | Exit | Output |
|---|---|---|---|
| 1 | `python3 -I .ufo/waves/round-21/resource/measure.py --tool /fast/scratch/hyaku/mado-r23/BaseResource/base-tool.py --mode module-main` | 0 | 3 JSONL rows, stderr empty |
| 2 | `python3 -I .ufo/waves/round-21/resource/measure.py --tool /fast/scratch/hyaku/mado-r23/BaseResource/base-tool.py --mode cli` | 0 | 3 JSONL rows, stderr empty |
| 3 | `python3 -I .ufo/waves/round-22/resource-closure-measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --mode module-main` | 0 | 1 receipt: `driver_exit=0`, `receipt_complete=true`, `integrity_errors=[]` |
| 4 | `python3 -I .ufo/waves/round-22/resource-closure-measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --mode cli` | 0 | 1 receipt: `driver_exit=0`, `receipt_complete=true`, `integrity_errors=[]` |

## Per-case results — 12/12 child scans clean

Every row: child `exit=0`, `timed_out=false`, `spawn_error=null`, `process_reaped=true`, `reap_timeout=false`, RLIMIT_AS `402653184` (384 MiB), scanner stdout `MADO_TRIPWIRE: clean` with verdict JSON `mado-tripwire-verdict-v1`, `observed_findings=0`, `unpermitted=0`, all five `counts` fields 0, `unparsed_total=0`; fixture and tool sha256 identical before/after each scan.

| Population | Mode | Case (statements/closures) | exit | RSS KiB | elapsed s |
|---|---|---|---|---|---|
| r21 | module-main | 1000 | 0 | 26 580 | 0.054 |
| r21 | module-main | 2000 | 0 | 23 316 | 0.048 |
| r21 | module-main | 4000 | 0 | 29 508 | 0.081 |
| r21 | cli | 1000 | 0 | 29 692 | 0.052 |
| r21 | cli | 2000 | 0 | 32 804 | 0.071 |
| r21 | cli | 4000 | 0 | 37 648 | 0.098 |
| r22 | module-main | 512 | 0 | 21 852 | 0.071 |
| r22 | module-main | 1024 | 0 | 25 156 | 0.122 |
| r22 | module-main | 2048 | 0 | 32 292 | 0.230 |
| r22 | cli | 512 | 0 | 29 744 | 0.092 |
| r22 | cli | 1024 | 0 | 33 824 | 0.141 |
| r22 | cli | 2048 | 0 | 41 004 | 0.259 |

Peak RSS 41 004 KiB ≈ 40.0 MiB → ~9.4× headroom under the 384 MiB cap. Slowest case 0.259 s → ~58× headroom under the 15 s deadline. Growth with workload size is linear-ish and small (23→29 MiB across 1000→4000 statements; 22→32 MiB across 512→2048 closures); no retained-memory blowup at base.

A post-hoc sweep re-parsed all 12 saved rows and both receipts against those criteria: 0 violations.

## Findings

No defect blocks the guard. Findings by severity:

- **F1 — [info, by design, observed] round-22 harness rejects out-of-repo `--tool`.** Run with the scratch copy printed a receipt with `driver_exit=2` and `driver_error: "ValueError: --tool must resolve inside the repository"` (no child spawned; saved as `r22-reject-scratch-path.*`). Consequence: round-22 re-measurement necessarily runs the lane working-copy path. Legitimate here because identity was proven by sha256 equality with the extracted base blob (`cd9da20c…`), lane HEAD equals the base commit, and `tools/` had no local modifications. Anyone re-running this guard later should re-do that identity proof first; the harness itself also pins the tool digest across the whole workload (`tool_sha256_before==after==cd9da20c…` in both receipts).
- **F2 — [info, stale-doc risk] round-21 help/docstring warns CLI mode "can fail" under the 384 MiB cap** (512 MiB worker-thread stack reservation). At this base the failure mode did not manifest: CLI rows ran clean with peak RSS 29.7–37.6 MiB in both populations. The statement is conditional and the harness policy ("preserve that failure as observed") is intact, but note for post-repair interpretation: the registration's no-harm guard says these populations must stay **clean** under 384 MiB / 15 s, and this baseline shows clean including CLI mode — a post-repair CLI failure here would be a regression against this baseline, not a pre-existing condition to preserve.
- **F3 — [info] determinism.** Verdicts, exits, digest pins and manifest/runner hashes are identical across all four independent harness runs (both r22 receipts: manifest `6a357933…` matching the harness's `EXPECTED_MANIFEST_SHA256`, runner `6d0362e1…`). Only `elapsed_seconds` and `ru_maxrss` vary slightly between runs — normal scheduler noise, ~5–15%, no effect on any threshold.

## Environment

Python 3.14.8 (`/usr/bin/python3.14`, resolved via `sys.executable` for children). **No tools installed or updated** (tooling directive: none needed). Host untouched; no jj commands; read-only git only (`show`, `rev-parse`, `status`).

## Residual risk and verification gaps

- Baseline only: this seat measured the base classifier; the post-repair re-measurement at the landed tip is the integration owner's check (same commands, TOOL = landed `tools/mado-tripwire.py`).
- One run per (harness × mode); exits were uniform, but per-case RSS/elapsed were not re-sampled. Cap headroom is ~9×, so single-sample noise cannot flip the guard.
- Round-22 numbers come from the lane working-copy path (F1), not the scratch copy; identity to base is sha256-proven, and the harness re-verifies the digest per case, so this is equivalence by construction rather than a second scratch-path run.

## Artifacts (all sha256-verified, under `.ufo/waves/round-23/w1/out/BaseResource/`)

| File | sha256 |
|---|---|
| `r21-module-main.stdout.jsonl` | `ffc345d3c4068b06e297db405e5a17aab03c469823f72e90265440164929915e` |
| `r21-module-main.stderr.txt` | `e3b0c442…b855` (empty) |
| `r21-module-main.exit` | `9a271f2a…86aa` ("0") |
| `r21-cli.stdout.jsonl` | `9dae7919409766c548a12041618220b35faf4aa1094b23789c2d24ad1db0e2bd` |
| `r21-cli.stderr.txt` | `e3b0c442…b855` (empty) |
| `r21-cli.exit` | `9a271f2a…86aa` |
| `r22-module-main.stdout.json` | `cf7115b812022da01b0d94815a650cad60b020f06cf362c28923268e48e89385` |
| `r22-module-main.stderr.txt` | `e3b0c442…b855` (empty) |
| `r22-module-main.exit` | `9a271f2a…86aa` |
| `r22-cli.stdout.json` | `cf19d442523608a5746b13c2d6d55d9de39e8d02fb58e296dba2cf02e7247055` |
| `r22-cli.stderr.txt` | `e3b0c442…b855` (empty) |
| `r22-cli.exit` | `9a271f2a…86aa` |
| `r22-reject-scratch-path.stdout.json` | (demo of F1, exit 2) |
| `r22-reject-scratch-path.stderr.txt` / `.exit` | (empty / "2") |

Extracted tool copy kept at `/fast/scratch/hyaku/mado-r23/BaseResource/base-tool.py` (`cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`).

## Verdict

**PASS — all four resource-guard measurements at base are clean: 12/12 child scans exit 0, zero findings, zero timeouts, zero spawn/reap failures, peak RSS 40.0 MiB vs 384 MiB cap, slowest case 0.259 s vs 15 s. The C1 no-harm resource baseline is re-confirmed at `a28e4815` / classifier `cd9da20c…`; no harness defect found (F1 is a by-design path guard, worked around via sha256-proven identity).**
