# ReviewCounterCode — correctness review of the round-27 C1 counter's generator

Scope: `.ufo/waves/round-27/c1/count.py` (frozen, sha256 `3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136`, verified in-run) — the generator (`selector`, `rule_items`, `rule_lines`, `gaps`, `boolv`, `write`, `sourced_existing`, `build_case`) and its selector/rule/variable/source placement. Review question: does Hyprland v0.56.2 reject any generated line (config error or silent drop) so a case becomes vacuous? Read-only on lane files; all work products under `/fast/scratch/hyaku/mado-r27/revc1/`.

## What I did (exact commands)

1. Throwaway tool that prints `[]`: `/fast/scratch/hyaku/mado-r27/revc1/empty-tool.py` (sha256 `cddf5be155ae03b2ab943f2ff0e51b58da7f0ab93532c35d8ea6c862059b6275`).
2. One counter run with it, fixed seed:
   ```
   cd /home/vgpnk/Projects/shokunin/mado-shokunin && env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- \
     python3 -I .ufo/waves/round-27/c1/count.py 5ddc5885 \
     --tool-file /fast/scratch/hyaku/mado-r27/revc1/empty-tool.py --seed 7e5717e5 --jobs 6
   ```
   Receipt: `/fast/scratch/hyaku/mado-r27/revc1/counter-empty-tool-run.txt`. Result: `PRED-C1-r27 cases_pass=1/41 verdict=TARGET_MISSED`, `exit=1`; `ORACLE_CHECK base_twice equal rules=0`; `ORACLE_VERSION commit=efb50993… tag=v0.56.2`; `HOST_SAFETY … delta=0`. Every generated case FAILs against `[]`; `oracle_rules` per case is 1–5 (never 0), so no case passes an empty prediction.
3. Same-seed rebuild of the generated trees by importing the counter's own `build_case` (script `/fast/scratch/hyaku/mado-r27/revc1/rebuild.py`), same rng consumption order as `count.py main`:
   ```
   env -i PATH=/usr/bin HOME=/home/vgpnk timeout 600 prlimit --core=0 --as=8000000000 -- \
     python3 -I /fast/scratch/hyaku/mado-r27/revc1/rebuild.py 7e5717e5 C00 C07 C19 C25 C39
   ```
   Receipt: `rebuild-probe.txt`. Identity check: snapshot `files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727` — byte-identical to the counter run's printed digest, and all 40 case descriptors match the counter's printout character-for-character. The rebuilt trees are the same trees the counter scored.
4. Probe of ALL 41 trees (BASE + 40 cases, not a sample) plus one positive-control tree, with `['workspacerules','configerrors']` (script `probe_all.py`):
   ```
   env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 --as=8000000000 -- \
     python3 -I /fast/scratch/hyaku/mado-r27/revc1/probe_all.py 7e5717e5
   ```
   Receipt: `probe-all.txt`. For each case the script also compares `len(workspacerules)` against the number of distinct generated selectors after variable expansion (a rejected/dropped line would show as a shortfall).
5. Static scan of all 40 trees (distinct selectors, rule keys, bool words, gap-vector lengths, variable-name collisions, snapshot `$ws*` variables) and a pin-exact source check (shallow fetch of Hyprland `efb50993` into scratch, read-only greps).

Note: `prlimit --as=8000000000` on my own scripts mirrors what the harness itself raises for bwrap (oracle.py runs `prlimit --as=8000000000` inside its sandbox); capping at 4G would break that in-sandbox raise, so no lower cap was used, matching the registration's counter-run pattern (`--core=0` only).

## Findings (by severity)

**F1 — No vacuous cases (the review question).** All 40 generated cases load with **zero config errors**: `configerrors -j` returns `[""]` in every case, byte-identical to the unperturbed BASE shape (BASE: `[""]`, `rules=0`). Independently, in every case the number of table entries equals the number of distinct generated selectors (`mismatches=0`), so no line was rejected, skipped, or silently dropped — including the exotic selectors (`w[tv1]`, `w[1-3]`, `f[-1]`, `f[0]`, `m[HEADLESS-1]`, `r[a-b]`, `special:*`, bare ints) and the trap values. With the `[]` throwaway tool the counter scores 1/41 (only the unperturbed BASE passes), so no case is answerable by a do-nothing tool.

**F2 — The `configerrors` probe is a live sensor, not a dead one.** BASE calibration shows `[""]` is the no-error shape. A positive control (copy of the snapshot plus `workspace = 9, bogusrule:xyz` and `workspace = 9, gapsin:banana 2`) produced `["Config error in file …/.config/hypr/hyprland.conf at line 35: banana 2"]` — `configerrors -j` does report real value-parse failures, i.e. exactly the trap class the generator draws from (bool words, gap integers). Asymmetry worth recording: an unknown rule *key* (`bogusrule`) is silently ignored (no error, no field), so key-validity claims rest on the pin, not on the sensor. All 13 generated keys are valid in the pin (each appears in the verb output except layoutopt, see F3).

**F3 — Informational coverage soft spot: `layoutopt` is accepted but invisible.** 28 `layoutopt:orientation:*` items occur across the 40 cases. The key is real in the pin (`src/config/legacy/ConfigManager.cpp:1756` parses `layoutopt:` into `m_layoutopts`, consumed e.g. by `src/layout/algorithm/tiled/master/MasterAlgorithm.cpp:940`), but `workspacerules -j` never serializes it (`src/debug/HyprCtl.cpp` has no `m_layoutopts` reference; observed absent from every probed entry while sibling keys on the same lines all appear). Consequence: no config error can ever come from a layoutopt item, and a predictor that ignores layoutopt entirely is indistinguishable from one that models it. This does **not** make cases vacuous — every layoutopt-bearing line also carries observable keys (monitor, decorate, gapsin, bordersize, on-created-empty, defaultName, persistent).

**F4 — Placement is correct where it could silently break.** Verified empirically and by reading the generator:
- VARIABLE: defs are pinned to the top of the root; uses expand correctly in root lines (C00 `r[3-6]`), in new sourced files (C19 `roysjd.conf` line `workspace = f[0] , $wsupz , …` → entry `default:false` from `$wsupz = default:0`; the `source = ~/sub.conf` line is emitted after the defs, and hyprlang parses the root sequentially), and the EX path is guarded by `"$ws" not in ln` — correctly, because pre-existing sourced files are parsed before the appended defs (the snapshot root's `source` lines 4–19 precede the appended block). No intra-case variable-name collisions (0 across 40 trees) and the snapshot defines no `$ws*` variables (no shadowing).
- SOURCE: EX lines landed in genuinely sourced snapshot files (C00 → `~/.local/share/omarchy/default/hypr/bindings/tiling-v2.conf`, root line 7; C07 → `~/.config/hypr/looknfeel.conf`, root line 19) and their selectors appear in the table, proving Hyprland parsed them. NEWSRC `source = ~/...` resolves under the oracle's HOME (C19/C39 sub-file rules present in output).
- MERGE: exercised across root/sourced/new files (C07: `workspace = 2` in root merged with `persistent:no , decorate:false , on-created-empty:… , default:true` in `looknfeel.conf` into one entry; C19: two `f[0]` lines merged, later `gapsin` wins). The no-trap fallback forces a merge with a comma-free selector, so the `split(",")` extraction there is safe.
- VALUES: all bool-trap words are accepted and serialized (`persistent:no→false`, `shadow:on→true`, `border:1→true`, `default:yes→true`); gap vectors of length 1–4 accepted with CSS-like expansion (`gapsin:4 0 → [4,0,4,0]`); `on-created-empty` values with spaces/`--` preserved verbatim.

**F5 — Counter mechanics behaved as designed during the run.** Twice-equal base oracle (rules=0 — the unperturbed snapshot has no workspace rules, so the 40 generated cases carry 100% of the signal), version pin verified, `HOST_SAFETY … delta=0`, `exit=1` with the `[]` tool.

## Bottom line

No generated line is rejected by Hyprland v0.56.2, no case in the probed seed is vacuous, and the counter's case generation is faithful (same-seed rebuild reproduces the scored trees byte-for-byte). The only substantive observation is F3: `layoutopt` contributes no observable signal in `hyprctl workspacerules -j`, a coverage (not correctness) nuance for whoever reads case descriptors as feature claims.

## Residual risk and verification gaps

- Single seed reviewed (7e5717e5). All selector families and all 13 rule keys of the generator's grammar were drawn and accepted in this seed, so structural rejection risk is low, but other seeds could draw value combinations not exercised here (e.g. `f[1]`, other `special:` words — same grammar shapes already proven).
- The probe script mapped tree dirs to labels by mtime; under mtime ties the label↔dir pairing can permute. Each of the 41 dirs was probed exactly once and all per-dir results were identical in kind, so no finding depends on the mapping; the rebuild receipt (`rebuild-probe.txt`) carries the authoritative dir↔label assignment.
- Unknown keys being silently ignored (F2) means a key renamed in a future pin would go unnoticed by both sensor and verb — irrelevant for the frozen pin, noted for future rounds.
- No LSP server device exists in this seat's tool inventory, so caller/definition checks were text- and runtime-evidence-based (oracle behavior + pin-exact source greps), not semantic LSP output.

## Host safety

Coredump delta across everything I started: 1338 → 1338 (`delta=0`; counter's own HOST_SAFETY lines agree). Nested Hyprland only via `harness/oracle.py` as reached by the frozen counter; no `WAYLAND_DISPLAY`/`HYPRLAND_INSTANCE_SIGNATURE` set; no card node touched; read verbs only (`instances`, `version`, `workspacerules`, `configerrors`, plus the harness's own `dispatch exit` on the nested instance). All spawned process trees terminated (oracle self-terminates; verified). The single live Hyprland process is the operator's desktop session, untouched.

## Receipts and work products (all under /fast/scratch/hyaku/mado-r27/revc1/)

- `counter-empty-tool-run.txt` — counter run with the `[]` tool (1/41 TARGET_MISSED, exit=1)
- `rebuild-probe.txt` — same-seed rebuild, snapshot digest match, 5-case probe detail with per-line JSON
- `probe-all.txt` — all-41-tree `configerrors`/rules probe + positive control, `mismatches=0`
- `per_case_sels.json`, `empty-tool.py`, `rebuild.py`, `probe_all.py` — scan output and scripts
- `hypr-src/` — shallow read-only fetch of Hyprland `efb50993…` used for the F2/F3 source checks (tooling note: no tool installs or upgrades were needed for this item)
