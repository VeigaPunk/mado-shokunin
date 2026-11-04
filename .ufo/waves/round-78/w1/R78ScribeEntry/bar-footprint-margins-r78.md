# The margined bar's band: the client's auto zone plus the compositor's edge margin

source: S457 Hyprland v0.56.2 src/render/Renderer.cpp @ efb5099 (applyExclusive `:2529-2585`, add `:2577`, edge guard `:2575`; arrangeLayerArray `:2587-2670`, margin block `:2634-2657`, apply call `:2664`; arrangeLayersForMonitor `:2673-2700`, addType `:2696`); S458 src/debug/HyprCtl.cpp @ efb5099 (layers reply `:647-700`; monitors reserved print `:281-282`); S459 src/desktop/reserved/ReservedArea.cpp @ efb5099 (`:19-35`, `:53-60`); S460 protocols/wlr-layer-shell-unstable-v1.xml @ efb5099 (level enum `:86-90`, set_exclusive_zone `:152-190`); S461 waybar(5) 0.15.0 (`margin` `S461.txt:124`, `margin-<side>` `:130`, `exclusive` `:183`); S462 Waybar v0.15.0 src/bar.cpp (margin precedence `:178-222`, namespace `:232-233`, size request `:240`, anchors `:422-424`, exclusive guard `:357-361`); S464 gtk-layer-shell v0.10.1 src/layer-surface.c (layer_surface_update_auto_exclusive_zone `:264-292`, adds `:276-286`)
verified-at: 2026-11-04 (six fetched sources re-pinned under `.ufo/waves/round-78/fetch/`, `sha256sum -c sha256-r78.txt` all OK; the band model scored 18/18 at rev `44a36b64`)
recheck: on-release (Hyprland after v0.56.2, Waybar after 0.15.0, gtk-layer-shell after 0.10.1); 180d otherwise — re-pin the fetched sources, re-run `python3 -I quality/counters/c1-r78-margins.py --repo . --rev REV --base-rev f597eccbffefd5fd6bbb01f3511c88bbeaed493c --controls .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root "$HYAKU_SCRATCH/mado-r78/c1"`
ground: what the monitor's `reserved` band owes to a waybar bar that declares margins, which margins enter it, and which declarations the model refuses rather than compose
Lane: mado-shokunin. Round: 78.

## What this entry holds

| question | where the answer lives | state |
|---|---|---|
| Why does a margined top bar reserve more than its height? | the client adds the unanchored edge's margin (S464 `:276-280`); the compositor adds the anchored edge's margin (S457 `:2577`) | OBS (source) |
| Which margins enter a horizontal bar's vertical band? | the vertical pair only; horizontal margins move or narrow the box (`Renderer.cpp:2634-2641`) | OBS (source) |
| What band does the join expect? | `extent + margins[OPPOSITE_EDGE[edge]]` (`tools/mado-barfoot.py:411`, extent `:307-315`, map `:69`) | OBS (tool) |
| Is that sum scored on a frozen set? | 18/18 at rev `44a36b64`, receipt `.ufo/waves/round-78/receipts/measurement-c1-r78.txt` | OBS (receipt) |
| Do single-anchor misreadings die? | seven named mutants, all killed (same receipt) | OBS (receipt) |
| What does the held r77 model score on the same set? | 8/18 (`MADO_R78_BASE` line) | OBS (receipt) |
| Is the host observed this round? | no: every case is a committed fixture, not a live capture | OBS (control set) / UNK (live) |

## §1 The two contributors, added once each

**1. The client's auto zone.** When the bar is exclusive, Waybar enables gtk-layer-shell's auto exclusive zone (`bar.cpp:357-358`; the `else` branch sets zone 0 at `:360`). gtk-layer-shell 0.10.1 computes it in `layer_surface_update_auto_exclusive_zone` (`layer-surface.c:264-292`): for a horizontal surface (left and right anchors equal) it starts at `new_exclusive_zone = self->current_allocation.height` (`:276`), then adds the margin of each vertical edge that is *not* anchored (`:278` top, `:280` bottom). A top-anchored bar leaves the bottom edge unanchored, so the client sends `height + margin.bottom`. The vertical branch transposes the same rule (`:282-286`, left/right margins).

**2. The compositor's addition.** `applyExclusive` returns early for `exclusive <= 0` (`Renderer.cpp:2531-2533`), selects one edge — exclusive edge, singular anchor, or the anchor triplet at that edge — under `exclusive + margin > 0` (`:2575`), then adds the zone *and that edge's margin* to the positive axis and subtracts the same from the size (`:2577`, `:2579-2581`). The top record's margin is `marginTop` (`:2547`), the bottom record's `marginBottom` (`:2555`), then `marginLeft` (`:2563`) and `marginRight` (`:2571`). So a top bar's band is `(height + margin.bottom) + margin.top`. The reservation is stored as original usable minus usable (`:2682`, `:2696`), and S459's parent/child constructor turns that difference into the per-side band (`ReservedArea.cpp:19-35`).

**3. The identity the tool encodes.** `expected = extent + margins[OPPOSITE_EDGE[edge]]` (`tools/mado-barfoot.py:411`), where `extent` is the anchored-edge extent of the realised box (`:307-315`: top `y+h`, bottom `mon_h−y`, left `x+w`, right `mon_w−x`) and `OPPOSITE_EDGE` maps top↔bottom, left↔right (`:69`). The anchored margin already moved the box along the band axis (`:280`, `:287-294`), so `extent` carries one margin and the opposite-edge term adds the other: top → `(m.top + h) + m.bottom`; bottom → `(m.bottom + h) + m.top`; left → `(m.left + w) + m.right`; right → `(m.right + w) + m.left`. Cross-axis margins never enter: the block offsets a zero-size or singly-anchored axis and skips a both-anchored one (`Renderer.cpp:2634-2641`), and Waybar either keeps both horizontal anchors set or clears both when `width > 1` is declared (`bar.cpp:422-424`) — neither branch adds a horizontal margin — hence `width-with-margins` keeps `expected=34` at `width=800`.

## §2 Decision table: reachable declaration → expected band

| declaration (modelled subset) | box | `expected` band | published `reserved` |
|---|---|---|---|
| `position: top`, `height h>0`, all margins ≥0 | `x=m.left`, `y=m.top`, `w=mon_w−m.left−m.right` (width ≤1) | `h + m.top + m.bottom` | `EQ` when the monitor reports it; `GT` when another surface adds more; `DIFFER` when short |
| `position: bottom` | same widths, `y=mon_h−h−m.bottom` | `h + m.top + m.bottom` | as above |
| `position: left` / `right`, `width w>0` | `x=m.left` / `mon_w−w−m.right`; `height ≤1` spans `mon_h−m.top−m.bottom` | `w + m.left + m.right` | as above |
| `layer: bottom` / `top` / `overlay` | unchanged | unchanged — the level moves the lookup only | `layer-bottom` |
| `exclusive: false` | modelled | computed and printed, but `reserved=NOT_APPLIED` | `exclusive-false` |
| `output: "!M"` excluding the joined monitor | none | none | rc 3 `NO_BAR` |
| `output: "!M2"` on M1 | normal | normal | `output-exclusion` |
| any margin < 0 | refused (`mado-barfoot.py:253-254`) | — | rc 3 model error |
| dynamic cross (`height 0` horizontal, `width 0` vertical) | refused (`:271-274`) | — | rc 3 |
| `layer: background`, `mode:` key, list config, `*`/space output | refused (`:246`, `:249`, `:595`, `:226`) | — | rc 3 model / rc 2 setup |
| monitor `scale != 1` or `transform != 0` | refused (`:370-374`) | — | rc 3 |

## §3 The frozen case set, worked

Counting command as the declaration fixes it (the score below is cited from the round's receipt, not re-run by this entry): `python3 -I quality/counters/c1-r78-margins.py --repo . --rev 44a36b64 --base-rev f597eccbffefd5fd6bbb01f3511c88bbeaed493c --controls .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root /fast/scratch/hyaku/mado-r78/c1` — receipt summary: `MADO_R78_BARFOOT: cases=18 correct=18 mutants=7 killed=7 base_correct=8/18 tool_selftest=22/22 verdict=TARGET_MET rev=44a36b64117812af7cc23a1815430d8320642455 tool_sha256=aac5d41b923711e174c6d62bb24da5a2b53abf7c938bfc5b68816929a12009c0`. Each row below is one `MADO_R78_CASE` line of that receipt.

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

## §4 Mutants and the held control

Seven single-anchor replacements of the extracted source (`quality/counters/c1-r78-margins.py:35-57`; each anchor must occur exactly once, `apply_mutation` `:145-149`). Scores are `MADO_R78_MUTANT` lines of the same receipt: `opposite-margin-dropped` 9/18, `horizontal-margin-leak` 9/18, `level-bottom-swap` 17/18, `right-extent-flip` 16/18, `per-side-margin-dropped` 17/18, `negative-margin-accepted` 17/18, `opposite-edge-wrong` 17/18 — all seven killed. The held r77 model (`base_sha256=e54787b7…`) scores 8/18: it loses every margined case, e.g. `top-margin-int rc=1 box=DIFFER reserved=NOT_MODELLED band=38 expected=34`, `top-margin-css-2 rc=3 … band=38 expected=34`, `right-margin rc=3 … band=46 expected=41` (the 41 is the extent alone: the opposite-edge term is the dropped half), and `negative-margin-refused rc=3 box=MATCH reserved=NOT_MODELLED band=24 expected=24 correct=no` (control receipt `control-baseline-c1-r78.txt`).

## What is not claimed

- **No live observation this round.** All eighteen cases are committed fixtures in `c1-cases-r78.json` (protocol `mado-c1-r78-v1`); expectations were derived from the two source rules, never from a tool run. `host-top` reproduces the round-77 host shape (`c1-cases-r78.json` case `host-top`: 3440x1440, reserved `[0,26,0,0]`) but is a fixture, not a capture.
- **The composition is scored against declared expectations, not a frame.** A host join would need fresh `hyprctl layers -j` / `hyprctl monitors -j`; neither exists in this round's receipts.
- **Static `monitor … addreserved` bands** are still mixed into `reserved`; the model assumes a zero static reserve (`mado-barfoot.py:42-43`).
- **Scaled or transformed monitors** are refused, not modelled (logical box vs pixel size, `:370-374`).
- **Centring rounding:** the tool floors (`//`, `:278`, `:292`), Hyprland rounds after doubles (`Renderer.cpp:2660`); a 1 px divergence is possible and no case exercises an odd delta.
- **Which process set a zone** is not read: the layers entry carries `namespace`/`pid`, not the exclusive request (S458 `HyprCtl.cpp:671-682`).
- **`GT` is admissible, not attribution.** A second exclusive surface yields `band > expected` and `CLEAN` (`second-consumer`, 60 vs 34); the join cannot apportion the band among surfaces.
- **Negative margins** are refused rather than composed; what the stack would compute for them is unmodelled.
- **`layer: background`** is refused even though the protocol defines level 0; Waybar's presets never select it.
- The `22/22` selftest was re-run read-only at HEAD (`python3 -I tools/mado-barfoot.py --selftest` → `MADO_BARFOOT_SELFTEST: 22/22`); the 18-case score is cited from the receipt, not re-executed here.

## Evidence

- `.ufo/waves/round-78/fetch/S457.bin`…`S464.bin` and `sha256-r78.txt` — six pinned sources, `sha256sum -c` all OK.
- `.ufo/waves/round-78/receipts/measurement-c1-r78.txt` — 18 cases, 7/7 mutants, base 8/18, tool sha `aac5d41b…`.
- `.ufo/waves/round-78/receipts/control-baseline-c1-r78.txt` — base `f597eccb`, `TARGET_MISSED`, tool sha `e54787b7…`.
- `.ufo/waves/round-78/controls/c1-cases-r78.json` — frozen cases, sha `99f1d82f…`; generator `controls/make-cases-r78.py`.
- `tools/mado-barfoot.py` — `r78-v1`, sha `aac5d41b…`; `quality/counters/c1-r78-margins.py` — `PRED-C1-r78-v1`, sha `1c39a53c…`.

## Sources

S457, S458, S459, S460, S461, S462, S464 in [SOURCES](../SOURCES.md). S463 stays rejected (renders the protocol without a revision pin).
