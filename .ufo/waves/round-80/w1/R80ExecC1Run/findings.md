# R80ExecC1Run — C1 re-count + independent re-derivation (round 80, w1)

Seat: R80ExecC1Run (leaf executor). Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
No frozen instrument, control set, or lane file was modified. All writes are under
`.ufo/waves/round-80/w1/R80ExecC1Run/` plus this seat's scratch (removed at the end).

## 1. C1 counting command (verbatim) — exit code

Run from the lane root:

```
python3 -I quality/counters/c1-r80-multisurface.py --repo . \
  --rev 6c302a53eb8f577e83fbcadc01e05a286778df8e \
  --base-rev e10f7e9f528b13195a1cdde28a68a702af3045c4 \
  --controls .ufo/waves/round-80/controls/c1-cases-r80.json \
  --carried .ufo/waves/round-79/controls/c1-cases-r79.json \
  --scratch-root /fast/scratch/hyaku/mado-r80/R80ExecC1Run
```

- Full output saved to `.ufo/waves/round-80/w1/R80ExecC1Run/c1-after.txt` (58 lines).
- **Exit code: 0** (`EXIT_CODE:0` under `set -o pipefail`; job exit 0).
- Tail of the output:

```
MADO_R80_BASE: correct=23/33 rule=held-r79-model(no-multi-surface-arrangement) base_rev=e10f7e9f528b13195a1cdde28a68a702af3045c4 base_sha256=9e2741577189424741e4294cfc22e8cd3acd95a1353bb7744c01a1b27eadcc85
MADO_R80_CONTROL: sha256=17c27157a9b0c293dbd07d56d67673cb061e808b6abcd1bb31f16ff6c15fd6ed carried=23/23
MADO_R80_BARFOOT: cases=33 correct=33 mutants=22 killed=22 base_correct=23/33 carried=23/23 tool_selftest=111/111 verdict=TARGET_MET rev=6c302a53eb8f577e83fbcadc01e05a286778df8e tool_sha256=c3eb5fbef794c92ba45adc85ed1dcd18c505a2776a3fb1db34742a6eed27fa99
```

All five predicate numbers of the frozen C1 claim reproduce: `correct=33`, `killed=22`,
`base_correct=23/33`, `carried=23/23`, tool selftest 111/111, `verdict=TARGET_MET`, exit 0.
The 22 named mutants each printed `killed=yes`; the three target cases printed
`overlay-compose-top ... band=66 expected=66 correct=yes`, `same-level-order ... band=62
expected=62 correct=yes`, `ls-area-invalid ... band=0 expected=0 correct=yes`.

## 2. Selftests

| Command | Output | Exit |
|---|---|---|
| `python3 -I tools/mado-barfoot.py --selftest` | `MADO_BARFOOT_SELFTEST: 111/111` | 0 |
| `python3 -I quality/counters/c1-r80-multisurface.py --selftest` | `MADO_R80_BARFOOT_SELFTEST: 60/60` | 0 |

## 3. Compositor ground used (no tool code read for the derivation)

Source: `.ufo/waves/round-80/fetch/S470.bin` — `src/render/Renderer.cpp`
(sha256 `9af8a74e…`, byte-identical to the r79 `S457.bin` and r78 pin, as declared).
Line numbers below are exact (grep-pinned against the file).

- `arrangeLayersForMonitor` :2673-2700 — `ORIGINAL_USABLE_AREA = logicalBoxMinusReserved()`
  (:2682-2683); per-level `stable_sort` by rule `order()` **descending** (:2685-2688);
  exclusive pass over `m_layerSurfaceLayers` in array order (:2690-2691), then the
  non-exclusive pass (:2693-2694); the whole layer reserve is committed with
  `addType(RESERVED_DYNAMIC_TYPE_LS, CReservedArea{ORIGINAL_USABLE_AREA, usableArea})` (:2696).
- `arrangeLayerArray` :2587-2671 — surfaces with `exclusive > 0` are arranged only in the
  exclusive pass (:2596-2597 `if (exclusiveZone != (PSTATE->exclusive > 0)) continue;`);
  `bounds = full_area` iff `exclusive == -1`, else `bounds = *usableArea` — the **running**
  box earlier surfaces already shrank (:2599-2603); top-anchored `box.y = bounds.y`, and the
  anchored-top margin is added to the box (`box.y += margin.top`, :2651); an arranged box with
  `width <= 0 || height <= 0` is skipped entirely (:2655-2658); after placement,
  `applyExclusive(...)` (:2664) runs per surface; the box itself is committed regardless
  (`ls->setBox`, :2669).
- `applyExclusive` :2529-2585 — returns without reserving when `exclusive <= 0` (:2531-2533);
  the edge table matches `exclusiveEdge == singular || anchor == singular || anchor == triplet`
  **and** `exclusive + margin > 0` (:2574-2575); the matched edge shifts
  `usableArea.y += exclusive + margin` and `usableArea.height -= exclusive + margin`
  (:2576-2581); `break` (:2582) — only the **first** matching edge reserves.
- Reserve drop: `ReservedArea.cpp:19-31` per the frozen declaration — the layer reserve is
  dropped when the surviving box is empty or not contained in the static-reduced box. The
  `.cpp` itself is **not** among the fetched bytes; the semantics are pinned behaviorally by
  the fetched unit test S472 (`tests/desktop/Reserved.cpp`): `CReservedArea d{orig, CBox{}}`
  yields all-zero sides (:46-51) and `CReservedArea e{orig, CBox{0,0,100,100}}` (not
  contained) has `ok() == false` (:53-54).
- Attribution convention (from the control set, not the tool): `attr` is
  `top,bottom,left,right`; per-surface contribution = the zone `applyExclusive` charged to
  that surface's first matching edge (`zone = exclusive + margin`, margins of anchored edges
  ride the zone); `band` = the compositor's own GT top (the case's `monitors[].reserved`);
  `attributed` = sum of per-surface top contributions; `expected` = hand-derived band.

Level iteration order (level 2 "top" before level 3 "overlay") is not visible inside S470
(it is the `m_layerSurfaceLayers` array order in Monitor state); it is pinned here by the
frozen fixtures' own geometry (waybar@y0 level 2, panel@y26 level 3 in `overlay-compose-top`,
control :1294).

## 4. Derivations (hand arithmetic, straight from S470.bin + control fixtures)

### 4.1 `overlay-compose-top` (control `name` at :1294; fixture in `fixtures/overlay-compose-top/`)

Monitor M1 1000×800, static reserve 0 → `ORIGINAL_USABLE_AREA = [0,0,1000,800]`.
Declared surface: panel {level 3, height 40}; bar: waybar {top, level 2, height 26}.

1. Exclusive pass in level order → waybar (level 2) first: bounds y=0;
   top-anchored box `[0,0,1000,26]` (fixture level-2 waybar y=0 ✓).
   `applyExclusive`: zone `26 + 0 = 26 > 0` (:2575) → `usable.y = 0+26 = 26`,
   `usable.height = 800-26 = 774`. Contribution waybar = top:26.
2. Panel (level 3) next: `exclusive != -1` → bounds = running usable `[y26 h774]` (:2600-2603);
   box `[0,26,1000,40]` (fixture level-3 panel y=26 ✓).
   `applyExclusive`: zone `40` → `usable.y = 26+40 = 66`, `height = 734`. Contribution panel = top:40.
3. `addType{orig, usable y66 h734}` (:2696): non-empty, contained → reserve kept.

Arithmetic: `band = 0 + 26 + 40 = 66`; `attributed = 26 + 40 = 66`; `attr = "0,66,0,0"`;
`expected = band = 66`.

### 4.2 `same-level-order` (control `name` at :1449; fixture in `fixtures/same-level-order/`)

Both surfaces in level 2: panel {exclusive 30, margins.top 6, order 10, h30}; waybar {top, h26}.

1. Intra-level sort by order desc (:2686-2687): panel (10) before waybar (default 0).
2. Panel: bounds y=0; top-anchored box y=0, then anchored-top margin `box.y += 6` (:2651)
   → box `[0,6,1000,30]` (fixture panel y=6 ✓).
   `applyExclusive`: Top edge; `30 + 6 = 36 > 0` (:2575) → `usable.y = 36`, `height = 764`.
   Contribution panel = top:**36** (the margin rides the zone).
3. Waybar: bounds y=36 → box `[0,36,1000,26]` (fixture waybar y=36 ✓); zone `26` →
   `usable.y = 36+26 = 62`, `height = 738`. Contribution waybar = top:26.
4. `addType{orig, usable y62 h738}`: kept.

Arithmetic: `band = 36 + 26 = 62`; `attributed = 36 + 26 = 62`; `attr = "0,62,0,0"`;
`expected = 62`.

### 4.3 `ls-area-invalid` (control `name` at :1777; fixture in `fixtures/ls-area-invalid/`)

Monitor M1 1000×800. Declared surface: panel {level 3, exclusive 2000, h100}; bar waybar {top, h26}.

1. Waybar (level 2) first: box `[0,0,1000,26]`; zone `26` → `usable.y = 26`, `height = 774`.
   Contribution waybar = top:26.
2. Panel (level 3): bounds = running usable `[y26 h774]` → box `[0,26,1000,100]` (fixture y=26 ✓);
   `applyExclusive`: `2000 + 0 > 0` (:2575) → `usable.y = 26+2000 = 2026`,
   `usable.height = 774-2000 = -1226`. Contribution panel = top:2000.
3. `addType{orig [0,0,1000,800], usable y2026 h-1226}` (:2696): surviving box has negative
   height → empty, and `[y2026 …]` is not contained in `[0,0,1000,800]` → per
   `ReservedArea.cpp:19-31` (behavior pinned by S472 :46-51, :53-54) the **whole** dynamic LS
   reserve is dropped → monitor reserved stays `[0,0,0,0]`.
4. Geometry was already committed per surface (setBox :2669) → boxes still MATCH; only the
   reserve is void → `ls = INVALID`.

Arithmetic: `band = 0` (GT dropped); `attributed = 2000 + 26 = 2026`; `attr = "0,2026,0,0"`;
`expected = 0`.

## 5. Tool runs on the three cases (my fixtures, built from the control set)

Fixtures: `fixtures/<case>/{config,layers,monitors,surfaces}.json` extracted field-for-field
from `.ufo/waves/round-80/controls/c1-cases-r80.json`. Invocation per case:

```
python3 -I tools/mado-barfoot.py --config <dir>/config.json --layers <dir>/layers.json \
  --monitors <dir>/monitors.json --surfaces <dir>/surfaces.json --monitor M1
```

Full stdout saved as `tool-overlay-compose-top.txt`, `tool-same-level-order.txt`,
`tool-ls-area-invalid.txt`. All three exit 0.

### overlay-compose-top (exit 0)

```
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=0,0,1000,26 anchor=top+left+right zone=26
MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=waybar edge=top contribution=26 box=0,0,1000,26
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=0,26,1000,40 anchor=top+left+right zone=40
MADO_BARFOOT_ATTR: monitor=M1 level=3 ns=panel edge=top contribution=40 box=0,26,1000,40
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=66 expected=66 attributed=66 gt=0,66,0,0 attr=0,66,0,0 ls=VALID verdict=CLEAN
```

### same-level-order (exit 0)

```
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=panel box=0,6,1000,30 anchor=top+left+right zone=30
MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=panel edge=top contribution=36 box=0,6,1000,30
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=0,36,1000,26 anchor=top+left+right zone=26
MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=waybar edge=top contribution=26 box=0,36,1000,26
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=62 expected=62 attributed=62 gt=0,62,0,0 attr=0,62,0,0 ls=VALID verdict=CLEAN
```

### ls-area-invalid (exit 0)

```
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=0,0,1000,26 anchor=top+left+right zone=26
MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=waybar edge=top contribution=26 box=0,0,1000,26
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=0,26,1000,100 anchor=top+left+right zone=2000
MADO_BARFOOT_ATTR: monitor=M1 level=3 ns=panel edge=top contribution=2000 box=0,26,1000,100
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=0 expected=0 attributed=2026 gt=0,0,0,0 attr=0,2026,0,0 ls=INVALID verdict=CLEAN
```

## 6. Verdicts

| Case | Field | My derivation | Control expect | Tool run | Verdict |
|---|---|---|---|---|---|
| overlay-compose-top | band | 66 | 66 | 66 | AGREE |
| overlay-compose-top | expected | 66 | 66 | 66 | AGREE |
| overlay-compose-top | attributed | 66 | 66 | 66 | AGREE |
| overlay-compose-top | attr | 0,66,0,0 | 0,66,0,0 | 0,66,0,0 | AGREE |
| same-level-order | band | 62 | 62 | 62 | AGREE |
| same-level-order | expected | 62 | 62 | 62 | AGREE |
| same-level-order | attributed | 62 | 62 | 62 | AGREE |
| same-level-order | attr | 0,62,0,0 | 0,62,0,0 | 0,62,0,0 | AGREE |
| ls-area-invalid | band | 0 | 0 | 0 | AGREE |
| ls-area-invalid | expected | 0 | 0 | 0 | AGREE |
| ls-area-invalid | attributed | 2026 | 2026 | 2026 | AGREE |
| ls-area-invalid | attr | 0,2026,0,0 | 0,2026,0,0 | 0,2026,0,0 | AGREE |

No DISAGREE on any field; no differing field to name.

## 7. Notes / caveats

- `ReservedArea.cpp:19-31` is cited from the frozen declaration; that file is not among the
  round's fetched bytes. The drop semantics are pinned behaviorally by fetched S472
  (:46-51 empty → zeros; :53-54 non-contained → `ok() == false`) and by the call site
  S470 :2696.
- Level iteration order (top before overlay) is inferred from the frozen fixtures' geometry
  and the r80 claim text; the array order itself lives in monitor state, not in S470.
- The counter's scratch under `/fast/scratch/hyaku/mado-r80/R80ExecC1Run/` was removed at
  the end of the seat; nothing a report points at lives there (all artifacts are in this
  directory).
- Host discipline held: read-only probes only, no pacman, no service restart, no git/jj
  mutation anywhere.

STATUS: ok — nothing missing; all three re-derivations AGREE with control and tool on every field.
