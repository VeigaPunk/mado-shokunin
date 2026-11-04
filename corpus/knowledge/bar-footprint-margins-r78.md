# The margined bar's band: the client's auto zone plus the compositor's edge margin

source: S457 Hyprland v0.56.2 src/render/Renderer.cpp @ efb5099 (applyExclusive `:2529-2585`, add `:2577`, edge guard `:2575`; arrangeLayerArray `:2587-2670`, margin block `:2634-2657`, apply call `:2664`; arrangeLayersForMonitor `:2673-2700`, addType `:2696`); S458 src/debug/HyprCtl.cpp @ efb5099 (layers reply `:647-700`, monitors `reserved` print `:281-282`); S459 src/desktop/reserved/ReservedArea.cpp @ efb5099 (parent/child band `:19-35`, apply `:53-60`); S460 wlr-layer-shell-unstable-v1 XML @ efb5099 (levels `:86-90`, exclusive `:152-190`); S461 waybar(5) 0.15.0; S462 Waybar v0.15.0 src/bar.cpp @ 90b209ad (margin precedence `:178-222`, anchors `:390-424`, auto-zone call `:357-361`); S464 gtk-layer-shell v0.10.1 src/layer-surface.c (auto zone `:264-292`). All re-opened 2026-11-04 with fresh pinned fetches under `.ufo/waves/round-78/fetch/` (`sha256-r78.txt`, seven files; the six `.bin`/man renders are byte-identical to the round-77 copies).
verified-at: 2026-11-04, round 78; the eighteen cases are measured at `44a36b64117812af7cc23a1815430d8320642455` (tool `r78-v1`, sha256 `aac5d41b…`, 18/18); the landing tip carries `r78-v2`, whose wave-driven repairs (output branches, `std::stoi` margins, centring rounding, an overflowing bar) leave every case unchanged (receipt `receipts/repair-r78-tool.txt`); host join receipt `receipts/live-join-r78.txt`
recheck: on-release (Hyprland after v0.56.2, Waybar after 0.15.0, gtk-layer-shell after v0.10.1); 180d otherwise — re-open the seven files, re-capture `hyprctl layers -j` / `hyprctl monitors -j` (reduce the monitors reply to the fields the join reads), and re-run `tools/mado-barfoot.py`
Lane: mado-shokunin. Round: 78. Supersedes the `NOT_MODELLED` margin limit of `bar-footprint-r77.md` §3/§4 (the r77 body stays the record of the r77 instrument).

## What this entry holds

| question | where the answer lives | state |
|---|---|---|
| Why does a margined top bar reserve more than its height? | the client adds the unanchored edge's margin (S464 `:276-280`); the compositor adds the anchored edge's margin (S457 `:2577`) | OBS (source) |
| Which margins enter a horizontal bar's vertical band? | the vertical pair only; horizontal margins move or narrow the box (`Renderer.cpp:2634-2641`) | OBS (source) |
| What band does the join expect? | `extent + margins[OPPOSITE_EDGE[edge]]` (`tools/mado-barfoot.py:411`, extent `:307-315`, map `:69`) | OBS (tool) |
| Is that sum scored on a frozen set? | 18/18 at rev `44a36b64`, receipt `receipts/measurement-c1-r78.txt` | OBS (receipt) |
| Do single-anchor misreadings die? | seven named mutants, all killed (same receipt) | OBS (receipt) |
| What does the held r77 model score on the same set? | 8/18 (`MADO_R78_BASE` line) | OBS (receipt) |
| Does the host agree? | the host's zero-margin bar joins CLEAN (26/26); a margin-4 declaration predicts band 34 against the live 26 and reports DIFFER — the model now forms the expectation where the r77 tool refused | OBS (host capture, reduced) |

## §1 The two contributors, added once each

**1. The client's auto zone.** When the bar is exclusive, Waybar enables gtk-layer-shell's
auto exclusive zone (`bar.cpp:357-358`; the `else` branch sets zone 0 at `:360`).
gtk-layer-shell 0.10.1 computes it in `layer_surface_update_auto_exclusive_zone`
(`layer-surface.c:264-288`): when the left and right anchors agree and the top and bottom
anchors do not (a horizontal bar), the zone is the allocation height (`:276`) plus the
margin of each *unanchored* vertical edge (`:278` top, `:280` bottom); the transposed
branch is the allocation width plus the unanchored horizontal margins (`:282-286`). A top
bar is anchored at top, so it adds only the bottom margin; a bottom bar adds only the top
margin.

**2. The compositor's addition.** `applyExclusive` returns early for `exclusive <= 0`
(`Renderer.cpp:2531-2533`), selects exactly one edge — exclusive edge, singular anchor, or
the anchor triplet at that edge — under `exclusive + margin > 0` (`:2575`), then adds the
zone plus that edge's margin to the usable box (`:2577`, subtract on the negative axis
`:2580`). `arrangeLayerArray` has already placed the box at the anchored edge's margin
(`:2646-2651`), so for a top bar the client's `h + bottom` and the compositor's `top` add
up to `h + top + bottom`; the band starts at the usable origin and ends at the box's far
side plus the opposite margin. The transposed rule gives `w + left + right`.

**3. The identity the tool encodes.** `expected = extent + margins[OPPOSITE_EDGE[edge]]`
(`tools/mado-barfoot.py:411`), where `extent` is the anchored-edge extent of the realised
box (`:307-315`: top `y+h`, bottom `mon_h−y`, left `x+w`, right `mon_w−x`) and `x`/`y`
already include the anchored margin. A negative margin is refused (`:253-254`): the
compositor's guard can void the band and this model does not compose that.

## §2 Decision table: reachable declaration → expected band

| declaration (modelled subset) | box | `expected` band | published `reserved` |
|---|---|---|---|
| `position: top`, `height h>0`, all margins ≥0 | `x=m.left`, `y=m.top`, `w=mon_w−m.left−m.right` (width ≤1) | `h + m.top + m.bottom` | `EQ` when the monitor reports it; `GT` when another surface adds more; `DIFFER` when short |
| `position: bottom` | same widths, `y=mon_h−h−m.bottom` | `h + m.top + m.bottom` | as above |
| `position: left` / `right`, `width w>0` | `x=m.left` / `mon_w−w−m.right`; `height ≤1` spans `mon_h−m.top−m.bottom` | `w + m.left + m.right` | as above |
| `layer: bottom` / `top` / `overlay` | unchanged | unchanged — the level moves the lookup only | `layer-bottom` |
| `exclusive: false` | modelled | computed and printed, but `reserved=NOT_APPLIED` | `exclusive-false` |
| `output: "!M"` excluding the joined monitor | none | none | rc 3 `NO_BAR` |
| `output: "!M2"` on M1 (string) | normal | normal | `output-exclusion` |
| `output: ["!M2"]` (array) | none: the array branch falls through to false | none | r78-v2 repair, `receipts/repair-r78-tool.txt` F1a |
| `output: ["M1","!M1"]` on M1 | the first positive entry wins | normal | r78-v2 repair F1b |
| `output: ""` | every output | normal | r78-v2 repair F1c |
| `margin: "4px 0"` | `std::stoi` prefix-parses `4px` → top/bottom 4 | `h + 8` | r78-v2 repair F3 |
| an odd centred cross size (e.g. width 801 on 3440) | Hyprland rounds the double centre once (`Renderer.cpp:2660`) | modelled | r78-v2 repair F2 |
| a bar whose box is not contained in the monitor | `CReservedArea` is empty → no reserve | 0 | r78-v2 repair F4 |
| any margin < 0 | refused (`mado-barfoot.py:253-254`) | — | rc 3 model error |
| dynamic cross (`height 0` horizontal, `width 0` vertical) | refused (`:271-274`) | — | rc 3 |
| `layer: background`, `mode:` key, list config, `*`/space output | refused (`:246`, `:249`, `:595`, `:226`) | — | rc 3 model / rc 2 setup |
| monitor `scale != 1` or `transform != 0` | refused (`:370-374`) | — | rc 3 |

## §3 The frozen case set, worked

Counting command as the declaration fixes it (the score below is cited from the round's
receipt, not re-run by this entry):
`python3 -I quality/counters/c1-r78-margins.py --repo . --rev 44a36b64 --base-rev f597eccb… --controls .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root …`
— receipt summary: `MADO_R78_BARFOOT: cases=18 correct=18 mutants=7 killed=7 base_correct=8/18 tool_selftest=22/22 verdict=TARGET_MET rev=44a36b64117812af7cc23a1815430d8320642455 tool_sha256=aac5d41b…`.
Each row below is one `MADO_R78_CASE` line of that receipt.

| case | declaration | expected band | receipt |
|---|---|---|---|
| `host-top` | h26, no margin | 26 | `band=26 expected=26` |
| `bottom-bar` | h30, bottom | 30 | `band=30 expected=30` |
| `top-margin-int` | h30, `margin: 4` | 30+4+4=38 | `band=38 expected=38` |
| `top-margin-css-2` | h30, `margin: "4 8"` | 30+4+4=38 (the 8 is cross-axis) | `band=38 expected=38` |
| `top-margin-asym` | h30, `margin-top 10`, `margin-bottom 2` | 30+10+2=42 | `band=42 expected=42` |
| `bottom-margin` | h30, `margin: 8`, bottom | 30+8+8=46 | `band=46 expected=46` |
| `left-margin` | w40, `margin: 6`, left | 40+6+6=52 | `band=52 expected=52` |
| `right-margin` | w36, `margin: 5`, right | 36+5+5=46 | `band=46 expected=46` |
| `right-zero-margin` | w40, right | 40 | `band=40 expected=40` |
| `layer-bottom` | h28, `layer: bottom`, top | 28 | `band=28 expected=28` |
| `output-exclusion` | h24, `output: "!M2"` on M1 | 24 | `band=24 expected=24` |
| `output-excluded` | `output: "!M1"` on M1 | — | rc 3 `box=NOT_ON_MONITOR reserved=NOT_APPLIED` |
| `width-with-margins` | h26, `margin: 4`, `width: 800` | 26+4+4=34 | `band=34 expected=34` |
| `exclusive-false` | h26, `exclusive: false` | printed 26, not applied | `band=0 expected=26 reserved=NOT_APPLIED verdict=CLEAN` |
| `second-consumer` | h26, `margin: 4`, another surface also reserves | 34 | `band=60 expected=34 reserved=GT verdict=CLEAN` |
| `reserved-differ` | h26, `margin: 4`, monitor reports 26 | 34 | `band=26 expected=34 reserved=DIFFER rc=1` |
| `dynamic-cross` | `height: 0` | — | rc 3 model error |
| `negative-margin-refused` | `margin: "-2 0"` | — | rc 3 model error |

## §4 Mutants, the held control, and the host join

Seven single-anchor replacements of the extracted source
(`quality/counters/c1-r78-margins.py:35-57`; each anchor must occur exactly once,
`apply_mutation`). Scores are `MADO_R78_MUTANT` lines of the same receipt:
`opposite-margin-dropped` 9/18, `horizontal-margin-leak` 9/18, `level-bottom-swap` 17/18,
`right-extent-flip` 16/18, `per-side-margin-dropped` 17/18, `negative-margin-accepted`
17/18, `opposite-edge-wrong` 17/18 — all seven killed. The held r77 model
(`base_sha256=e54787b7…`) scores 8/18: it loses every margined case, e.g.
`top-margin-int rc=1 box=DIFFER reserved=NOT_MODELLED band=38 expected=34`,
`top-margin-css-2 rc=3 … band=38 expected=34`, `right-margin rc=3 … band=46 expected=41`
(the 41 is the extent alone).

The host join (`receipts/live-join-r78.txt`, read-only captures): the declared bar
(`layer top`, `position top`, `height 26`, no margins) joins CLEAN, `band=26 expected=26`.
A fixture declaration that adds `margin: 4` predicts `box=4,4,3432,26` and `band=34` while
the live band is 26, so the join reports `box=DIFFER reserved=DIFFER verdict=DIFFER` rc 1 —
the model forms the expectation where the r77 tool returned `UNMODELLED`. The monitors
capture committed beside it is a derived reduction (name, size, reserved, scale,
transform, refresh rate, position), not the raw reply, which carries the output's serial.

## What is not claimed

- **The host join is one point sample, not a frame.** The zero-margin bar matches at 26 px;
  the margin-4 prediction is checked against that same capture and is expected to differ.
  No rendered pixel, animation or GTK allocation was observed.
- **The eighteen-case score is against declared expectations.** Expectations were derived
  from the two source rules, never from a tool run; `host-top` reproduces the round-77 host
  shape but the set is a fixture.
- **Static `monitor … addreserved` bands** are still mixed into `reserved`; the model
  assumes a zero static reserve (`mado-barfoot.py:42-43`).
- **Scaled or transformed monitors** are refused, not modelled (logical box vs pixel size,
  `:370-374`).
- **Centring rounding is modelled, not cased.** The tool now rounds the double centre once
  (`(extent + 1) // 2`), matching `Renderer.cpp:2660`; no frozen case exercises an odd delta, so
  the rule is pinned by a selftest assertion and the repair receipt F2, not by a scored case.
- **Which process set a zone** is not read: the layers entry carries `namespace`/`pid`, not
  the exclusive request (S458 `HyprCtl.cpp:671-682`).
- **An output entry naming the xdg-output identifier** (which waybar derives from the
  description) is not matched; only the monitor `name` is. A config that lists identifiers can
  therefore read `NO_BAR` where waybar would draw.
- **A bar taller than its module minimum** gets a larger allocation than the declared height
  (waybar adopts the realised size, `bar.cpp:639-649`); the model predicts from the declaration
  and reports the difference as drift.
- **`GT` is admissible, not attribution.** A second exclusive surface yields
  `band > expected` and `CLEAN` (`second-consumer`, 60 vs 34); the join cannot apportion
  the band among surfaces.
- **Negative margins** are refused rather than composed; what the stack would compute for
  them is unmodelled.
- **`layer: background`** is refused even though the protocol defines level 0; Waybar's
  presets never select it.

## Evidence

- `.ufo/waves/round-78/fetch/S457.bin`–`S464.bin` and `S461.txt`, sha256 in
  `sha256-r78.txt` — seven pinned sources, `sha256sum -c` all OK.
- `.ufo/waves/round-78/receipts/measurement-c1-r78.txt` — 18 cases, 7/7 mutants, base
  8/18, tool sha `aac5d41b…`.
- `.ufo/waves/round-78/receipts/control-baseline-c1-r78.txt` — base `f597eccb`,
  `TARGET_MISSED`, tool sha `e54787b7…`.
- `.ufo/waves/round-78/receipts/live-join-r78.txt` and `fetch/live-{layers,monitors}-r78.json`
  — the read-only host join (the monitors reply reduced to the fields the join reads).
- `.ufo/waves/round-78/controls/c1-cases-r78.json` — frozen cases, sha `99f1d82f…`;
  generator `.ufo/waves/round-78/controls/make-cases-r78.py`.
- `tools/mado-barfoot.py` — `r78-v1`, sha `aac5d41b…`;
  `quality/counters/c1-r78-margins.py` — `PRED-C1-r78-v1`, sha `1c39a53c…`.

## Sources

S457, S458, S459, S460, S461, S462, S464 in [SOURCES](../SOURCES.md). S463 stays rejected
(renders the protocol without a revision pin).
