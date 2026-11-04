# Seat R81ExecMutants — independent mutation census of the six new C1 mutants

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (HEAD detached; frozen tool rev `0e2ccd2a8692825cac534f57246053b276be9f13`, tool sha256 `a129a435…` verified locally).
Scope: the six new mutants from the frozen counter's `MUTATIONS` — `tie-round-trunc`, `round-width-spec`, `auto-gate-open`, `auto-gate-and`, `auto-axis-swapped`, `auto-dynamic-kept` — scored by hand against the six new case fixtures (`overflow-tie-negative`, `auto-dynamic-band-refused`, `auto-corner-edge`, `auto-all-four-edge`, `auto-parallel-edge`, `auto-left-dock`). The counter's own mutant loop was NOT used; the counter module was imported only for its `expected_ok`/`parse_result`/`parse_attr` scoring functions so expectations are bit-identical to the frozen instrument.

## Method

1. Copied `tools/mado-barfoot.py` to scratch (`/fast/scratch/hyaku/mado-r81/R81ExecMutants/mado-barfoot.py`), applied each mutation by hand with the exact `(anchor, replacement)` pair from `quality/counters/c1-r81-overflow-auto.py` `MUTATIONS` (asserted `source.count(anchor) == 1` per mutant, same guard as the counter's `apply_mutation`).
2. Wrote each case's fixture files (`config.json`, `layers.json`, `monitors.json`, `surfaces.json` where present) from `.ufo/waves/round-81/controls/c1-cases-r81.json` and ran the tool per case with the counter's exact argv (`python3 -I <tool> --config … --layers … --monitors … --surfaces …`) and its sandboxed env (`TMPDIR=<case dir>`, `LC_ALL=C`, …).
3. Scored each run with the counter's `expected_ok`; for failures, diffed every expected field (`parse_result` fields, `attr_ns` via `parse_attr`, rc, error line) to name the separating field.

Driver: `/fast/scratch/hyaku/mado-r81/R81ExecMutants/census.py` (evidence copy: `evidence/census.log`, `evidence/census.json`); literal RESULT lines: `evidence/separators.log`.

## Census result (six new cases only)

| variant | score | separating case(s) |
|---|---|---|
| base | 6/6 | — |
| tie-round-trunc | 5/6 | overflow-tie-negative |
| round-width-spec | 5/6 | overflow-tie-negative |
| auto-gate-open | 3/6 | auto-corner-edge, auto-all-four-edge, auto-parallel-edge |
| auto-gate-and | 3/6 | auto-all-four-edge, auto-parallel-edge, auto-left-dock |
| auto-axis-swapped | 5/6 | auto-left-dock |
| auto-dynamic-kept | 5/6 | auto-dynamic-band-refused |

Literal score lines (`evidence/census.log`):

```
VARIANT base score=6/6
VARIANT tie-round-trunc score=5/6
VARIANT round-width-spec score=5/6
VARIANT auto-gate-open score=3/6
VARIANT auto-gate-and score=3/6
VARIANT auto-axis-swapped score=5/6
VARIANT auto-dynamic-kept score=5/6
```

Cross-check against the frozen all-39 receipt (`.ufo/waves/round-81/receipts/measurement-c1-r81.txt`): the counter scores these mutants `38/39, 38/39, 36/39, 36/39, 38/39, 38/39`. My six-case losses are `1, 1, 3, 3, 1, 1`, so each mutant loses exactly the same number over the new six and — assuming the carried 33 behave as the receipt's `base_correct=33/39` composition implies — the carried set contributes zero losses for all six. The independent census and the frozen instrument agree.

## Per-mutant separating case and differing field

### tie-round-trunc — killed by `overflow-tie-negative`
Anchor: `    return math.floor(value + 0.5) if value >= 0 else math.ceil(value - 0.5)` → `    return math.trunc(value)` (`std_round`, tool line 495).
Differing fields: `boxes` (want `MATCH,MATCH`, got `MATCH,DIFFER`), `rc` (0→1), `verdict` (`CLEAN`→`DIFFER`).
Literal (`evidence/separators.log`): the panel arranged at `x=-0.5, w=1001` (anchors left+right on a 1000-wide monitor) rounds to `DECL … box=-1,363,1000,100` under the mutant vs live `box=-1,363,1002,100`; base `std_round` (half away from zero) reproduces the compositor's `-1,…,1002`. Result line: `MADO_BARFOOT_RESULT: … boxes=MATCH,DIFFER reserved=EQ band=26 expected=26 attributed=26 … verdict=DIFFER`.

### round-width-spec — killed by `overflow-tie-negative`
Anchor: `    nw = box["x"] + box["w"] - rx` → `    nw = box["w"]` (`cbox_round`, tool line 504).
Differing fields: `boxes` (want `MATCH,MATCH`, got `MATCH,DIFFER`), `rc`, `verdict`.
Literal: mutant emits `DECL … box=-1,363,1001,100` (width taken from the spec, not re-based on the rounded origin) vs live `box=-1,363,1002,100` → `boxes=MATCH,DIFFER … verdict=DIFFER`.

### auto-gate-open — killed by `auto-corner-edge` (also `auto-all-four-edge`, `auto-parallel-edge`)
Anchor: `    # gtk-layer-shell sends no zone for a corner, a parallel pair or all four anchors\n    return 0` → `    return spec["height"] + spec["margins"]["bottom"]` (`surface_zone`, tool lines 591–592).
Differing fields on the corner case: `attributed` (26→126), `expected` (26→126), `attr` (`0,26,0,0`→`0,126,0,0`), `attr_ns` (gains `panel: top:100`), `reserved` (`EQ`→`DIFFER`), `rc`, `verdict`.
Literal: `MADO_BARFOOT_DECL: … level=3 ns=panel … anchor=top+left zone=100` (base: zone 0 — gtk-layer-shell sends no zone for a corner) and `MADO_BARFOOT_RESULT: … reserved=DIFFER band=26 expected=126 attributed=126 gt=0,26,0,0 attr=0,126,0,0 … verdict=DIFFER`. All three gate cases (corner, all-four, parallel) fail identically; `auto-left-dock` and the other two new cases survive.

### auto-gate-and — killed by `auto-left-dock` (also `auto-all-four-edge`, `auto-parallel-edge`)
Anchor: `    if vert and not horiz:` → `    if vert and horiz:` (`surface_zone`, tool line 581).
On `auto-left-dock` (anchor `left`, the vertical-only branch) the mutant falls through to the corner `return 0`: dock zone 40→0. Differing fields: `box` (`MATCH`→`DIFFER`), `boxes` (`MATCH,MATCH`→`DIFFER,DIFFER`), `attr` (`40,26,0,0`→`0,26,0,0`), `attr_ns` (loses `dock: left:40`), `rc`, `verdict`.
Literal: `MADO_BARFOOT_DECL: … level=1 ns=dock box=0,26,40,774 anchor=left zone=0` (base zone=40) and `MADO_BARFOOT_RESULT: … box=DIFFER boxes=DIFFER,DIFFER … attr=0,26,0,0 … verdict=DIFFER` with no `MADO_BARFOOT_ATTR … ns=dock` line.
On `auto-all-four-edge`/`auto-parallel-edge` the mutated condition `vert and horiz` fires the vertical branch for balanced anchor sets: zone becomes `width=200` instead of 0, `attributed` 26→226, `attr` `0,26,0,0`→`0,226,0,0`, `attr_ns` gains `panel: top:200`. `auto-corner-edge` survives (vert=false → falls to `return 0` under both base and mutant).

### auto-axis-swapped — killed by `auto-left-dock`
Anchor: `        zone = spec["width"]` → `        zone = spec["height"]` (vertical branch of `surface_zone`, tool line 585).
Differing fields: `box`, `boxes`, `attr` (`40,26,0,0`→`0,26,0,0`), `attr_ns` (loses `dock: left:40`), `rc`, `verdict`.
Literal: dock surface has `width=40, height=0` → swapped zone = 0 → `DECL … ns=dock box=0,26,40,774 anchor=left zone=0` vs base zone=40; `RESULT … box=DIFFER boxes=DIFFER,DIFFER … attr=0,26,0,0 … verdict=DIFFER`. (The `spec["width"] == 0` guard is untouched, so no refusal fires — this is a silent zero-zone defect, exactly the class the case exists to catch.)

### auto-dynamic-kept — killed by `auto-dynamic-band-refused`
Anchor: `        if spec["height"] == 0:` → `        if False:` (`surface_zone` horizontal branch, tool line 572).
Differing fields: `rc` (want 3, got 0) and the error line (case demands `ERROR (stage=model …)`; mutant prints none) — the tool instead models the dynamic band as zone 0 and reports `MADO_BARFOOT_RESULT: … band=26 expected=26 attributed=26 … verdict=CLEAN` / `MADO_BARFOOT: verdict=CLEAN`, rc=0.

**No mutant lacks a separating case: all six are killed within the six new fixtures.** None is a real defect of the counter.

## Anchor uniqueness and anchor-absent behavior

`grep -c -F` on the pristine tool bytes, one count per anchor:

```
'    return math.floor(value + 0.5) if value >= 0 else math.ceil(value - 0.5)' => 1
'    nw = box["x"] + box["w"] - rx' => 1
'    if vert and not horiz:' => 1
'        zone = spec["width"]' => 1
'        if spec["height"] == 0:' => 1
'    # gtk-layer-shell sends no zone for a corner, a parallel pair or all four anchors' => 1
```

`auto-gate-open`'s anchor is the two-line sequence (comment line 591 + `    return 0` line 592, per `grep -n -F -A1`); the full two-line byte count is 1 (verified by exact string count).

Anchor-absent run: fixture git repo at `/fast/scratch/hyaku/mado-r81/R81ExecMutants/absent-repo` (scratch; `git rev-parse --show-toplevel` asserted to print the fixture dir before the single commit), whose `tools/mado-barfoot.py` has all six anchors deleted verbatim, then:

```
python3 -I quality/counters/c1-r81-overflow-auto.py --repo <absent-repo> --rev HEAD --base-rev HEAD \
  --controls .ufo/waves/round-81/controls/c1-cases-r81.json --carried <carried-r80.json> --scratch-root <scratch>/absent-work
```

(counter rc=1, i.e. verdict printed, no crash; `evidence/absent-run.log`):

```
MADO_R81_MUTANT: name=tie-round-trunc correct=0/39 killed=no reason=anchor-absent
MADO_R81_MUTANT: name=round-width-spec correct=0/39 killed=no reason=anchor-absent
MADO_R81_MUTANT: name=auto-gate-open correct=0/39 killed=no reason=anchor-absent
MADO_R81_MUTANT: name=auto-gate-and correct=0/39 killed=no reason=anchor-absent
MADO_R81_MUTANT: name=auto-axis-swapped correct=0/39 killed=no reason=anchor-absent
MADO_R81_MUTANT: name=auto-dynamic-kept correct=0/39 killed=no reason=anchor-absent
```

All six deleted anchors produce `reason=anchor-absent` (not a traceback): `grep -c 'reason=anchor-absent' absent-run.log` = 6, `grep -c Traceback` = 0. The remaining 22 mutants still applied and were scored (`killed=22` in the final verdict line). Counter selftest: `MADO_R81_BARFOOT_SELFTEST: 72/72` rc=0. Frozen tool selftest: `MADO_BARFOOT_SELFTEST: 121/121` rc=0.

## Risks / notes

- The two rounding mutants share one separating case (`overflow-tie-negative`) and one visible symptom (`boxes=MATCH,DIFFER`); they are distinguished by mechanism (`std_round` vs the `nw` re-base), visible in the differing `DECL` widths (1000 vs 1001) — not a collision problem, but if the suite ever wanted one case per mutant, `overflow-tie-negative` would need a sibling. Within the frozen set both are killed, which is what the contract scores.
- `auto-gate-and` and `auto-axis-swapped` both surface on `auto-left-dock` with identical RESULT fields; again both mutants are independently killed elsewhere (`auto-gate-and` also on the two balanced-anchor cases), so the census is unambiguous.
- No installs/upgrades were needed (system python 3 + git only); nothing was written outside the seat dir, the scratch dir, and the two report files named above.

STATUS: ok
