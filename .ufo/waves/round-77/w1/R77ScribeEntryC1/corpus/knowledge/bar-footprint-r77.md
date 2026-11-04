# The bar-footprint chain: declared waybar config → live layer box → monitor `reserved` band (round 77, C1)

source: S457, S458, S459, S460, S461, S462 (opened 2026-11-04; byte receipts `.ufo/waves/round-77/fetch/S457.bin`–`S462.bin`, hashes in `.ufo/waves/round-77/fetch/sha256-r77.txt`)
verified-at: 2026-11-04 (pinned sources re-read in the read-only trees at efb5099 / 90b209a; host join taken from the committed live captures and the pre-wave receipt; no host state changed)
recheck: trigger — Hyprland moves past v0.56.2 @ efb5099 or Waybar past 0.15.0 @ 90b209a (on-release), otherwise 180 days after 2026-11-04: re-pin the six sources, re-capture `hyprctl layers -j` and `hyprctl monitors -j`, re-run `tools/mado-barfoot.py` on the fresh captures plus the C1 counting command in `.ufo/waves/round-77/claims-declaration-r77.md`.
ground: which links carry a declared waybar bar's footprint into the monitor's `reserved` band on this compositor, what the `hyprctl` replies can and cannot show of that chain, and where the read-only join tool refuses to guess.
Lane: mado-shokunin. Round: 77.

## Ground statement

On 2026-11-04 the host's single monitor DP-1 (3440x1440 @ 99.997, scale 1, transform 0) carries one waybar surface at level 2 with box 0,0,3440,26, and its `reserved` band [0,26,0,0] is exactly that box's extent on the declared top edge; the declared config (`position` top, `layer` top, `height` 26, no margins, default exclusive) licenses the same box under Hyprland 0.56.2's arrange rule. Everything above the level of "some process set an exclusive zone" is observed in pinned sources or committed captures; the client-side zone composition under margins and the zone's provenance are named UNK / NOT_MODELLED, not guessed.

## The chain, one row per link

| # | link | statement | tag | pointer |
|---|---|---|---|---|
| 1 | waybar declaration | waybar 0.15.0 reads `position` (default top), `layer` (default bottom), `height`/`width` (blank = dynamic), `margin` (CSS string) or `margin-<side>` (int), `exclusive` (default true), `output` (string or array; `!name` excludes; `*` only as a terminal array entry), `name` (else namespace `waybar`). Any integer `margin-<side>` beats a `margin` string, which beats an integer `margin`; a string parse failure leaves all sides zero. | OBS | S461 (`fetch/S461.txt`: layer :64, output :72, position :85, height :93, width :99, margin :124, margin-<side> :130, exclusive :183); S462 (`bar.cpp`: margin precedence :178-222, namespace :232-233, size request :240, position default `Gtk::POS_TOP` :99) |
| 2 | anchors | all four edges are anchored except the far edge of `position`; an explicit width > 1 on a horizontal bar (height > 1 on a vertical bar) additionally clears both anchors on the long axis, so the bar centres | OBS | S462 `bar.cpp:392-431` (fill :393-394, per-position clear :401-412, explicit-size clear :414-425, apply :427-430) |
| 3 | protocol semantics | levels are background=0 / bottom=1 / top=2 / overlay=3; a positive exclusive zone is meaningful only anchored to one edge or an edge plus both perpendicular edges; "The exclusive zone includes the margin." | OBS | S460 (XML :86-90, :152-190, margin sentence :196) |
| 4 | arrange rule → box | desired size + anchors + margins yield the box: zero desired width spans the usable box minus left/right margins at x = margin.left; both horizontal anchors with a non-zero width centre the box; margins are not applied on an axis whose both-anchors branch ran; the result is rounded | OBS | S457 `Renderer.cpp:2587-2670` (horizontal :2609-2620, margin block :2634-2648, round :2660) |
| 5 | exclusive pass → usable area | `arrangeLayersForMonitor` resets the dynamic layer-shell reserve, arranges exclusive-zone surfaces first (every level, exclusive pass), then the rest; `applyExclusive` moves the usable area's edge by `exclusive + edge margin` on one edge per surface | OBS | S457 `Renderer.cpp:2529-2585` (edge table :2545-2572, add/sub :2576-2581), passes :2691/:2694 |
| 6 | band construction | the stored dynamic reserve is `CReservedArea{ORIGINAL_USABLE_AREA, usableArea}`; the parent/child constructor converts the shrinkage into top-left / bottom-right distances, and `apply()` subtracts the band from the logical box — a top bar of height h with zero margins yields reserved.top = h | OBS | S457 `Renderer.cpp:2696`; S459 `ReservedArea.cpp:19-35` (derivation :30-31), apply/applyip :53-69 |
| 7 | reply shapes | `layers -j` is keyed by monitor, then levels "0".."3" (names background/bottom/top/overlay); each entry carries address, x, y, w, h, alpha, namespace, pid — no exclusive-zone field. `monitors -j` prints `reserved` as left, top, right, bottom and takes width/height from `m_pixelSize` | OBS | S458 `HyprCtl.cpp:647-700` (entry fields :679-680), level names :706-708; monitors template :253, reserved args :281-282, pixel size :278. Host: `fetch/live-layers-r77.json`, `fetch/live-monitors-r77.json` (sha256 in `receipts/pre-wave-evidence-r77.txt`) |
| 8 | host join | declared box = live box = 0,0,3440,26 at level 2, namespace waybar; band 26 = box top extent 0+26; the tool prints `box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN` | OBS | `receipts/pre-wave-evidence-r77.txt` (`MADO_BARFOOT_DECL/LIVE/RESULT`, rc 0); captures per row 7; declaration per `~/.config/waybar/config.jsonc` echoed in `MADO_BARFOOT_CONFIG` |
| 9 | usable area | today's usable area is 3440 x 1414 starting at y 26: pixel height 1440 minus the band, shifted by the band — derived, not printed by any reply | INF | monitor height in `fetch/live-monitors-r77.json`; subtraction per S459 `ReservedArea.cpp:53-69` |
| 10 | zone provenance | which process set the zone, and to what value, is not in the replies; the join names the surface (namespace, pid), not the request | UNK | S458 entry field list :679-680 (no zone field) |
| 11 | margined composition | with any non-zero margin the client-side auto-zone composition is outside the model (NOT_MODELLED); only the compositor-side fact that the zone includes the anchored-edge margin is licensed | UNK (client side) / OBS (compositor side) | tool docstring `tools/mado-barfoot.py` ("Contract (v1, round 77)"); declaration named limits; S460 :196; S457 :2577 |

## The host join, measured 2026-11-04

- Declaration (`~/.config/waybar/config.jsonc`, read-only): `"layer": "top"`, `"position": "top"`, `"height": 26`; no `margin`/`margin-<side>` keys, no `exclusive` key (default true), no `name` (namespace `waybar`), no `output`. Echoed by `MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=26 width=0 margins=0,0,0,0 exclusive=true` (receipts/pre-wave-evidence-r77.txt).
- Monitor (`fetch/live-monitors-r77.json`, sha256 `e732af34…`): DP-1 3440x1440 @ 99.997, scale 1, transform 0, `reserved` [0,26,0,0]; the C2 probes `monitors-size` / `monitors-reserved` print the same mode and band (receipts/control-baseline-r77.txt).
- Layer (`fetch/live-layers-r77.json`, sha256 `46eb2481…`): level 0 `wallpaper` at 0,0,3440,1440; level 2 `waybar` at 0,0,3440,26; levels 1 and 3 empty.
- Join (receipts/pre-wave-evidence-r77.txt):

      MADO_BARFOOT_DECL: monitor=DP-1 box=0,0,3440,26 edge=top
      MADO_BARFOOT_LIVE: monitor=DP-1 level=2 ns=waybar box=0,0,3440,26 entries=1
      MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN
      MADO_BARFOOT: verdict=CLEAN   (rc=0)

INF: the wallpaper surface at level 0 contributes nothing to the band today — the band equals the bar's height exactly (row 9); a level-0 surface with a positive zone would add to the band and the tool would print `reserved=GT` (row 5 is level-agnostic). UNK: the zone's value and setter (row 10).

## The tool contract — `tools/mado-barfoot.py` (VERSION r77-v1, sha256 `409e78a4…` per receipts/control-baseline-r77.txt)

- **Inputs.** `--config PATH` (waybar JSONC, object form; a list-valued root, stdin, non-regular paths and files over 1 MiB are refused); `--layers PATH|-` and `--monitors PATH|-` (captured `hyprctl layers -j` / `monitors -j`; 1 MiB cap); `--monitor NAME` (optional only when exactly one monitor answers). The tool writes nothing, opens no socket, starts nothing; stdout carries at most four `MADO_BARFOOT_{CONFIG,DECL,LIVE,RESULT}` rows and one `MADO_BARFOOT: verdict=` row.
- **Auto branches** (`declared_box`, modelling row 4): a horizontal bar with `height` 0, or a vertical bar with `width` 0, is refused (`UNMODELLED` — the realised cross size is the module allocation, not a declared value); otherwise the cross axis spans the monitor minus the two margins. On the long axis, an explicit size > 1 clears both anchors and centres with floor division, margins not applied; size ≤ 1 spans the monitor minus the two margins. A box computed empty is refused. Floor division vs Hyprland's round-after-double can differ by 1 px on odd deltas (`Renderer.cpp:2612-2613` computes in double, `:2660` rounds; the tool uses `//`).
- **Reserved expectation.** Formed only when `exclusive` is true and all four margins are zero: expected = the declared box's extent on the declared edge (top: y+h; bottom: mon_h−y; left: x+w; right: mon_w−x), compared against `reserved` at the edge's index in left, top, right, bottom order (`RESERVED_INDEX`, from S458 :281-282) → `EQ`, `GT` (admissible: other surfaces may reserve too), or `DIFFER`. `exclusive: false` → `NOT_APPLIED`; any non-zero margin → `NOT_MODELLED` (row 11).
- **Output key.** Exact monitor names and `!name` exclusions only; a `*`- or space-containing pattern, a non-string entry, or a non-string/non-array `output` is refused as unmodelled. An excluded monitor yields `NO_BAR` (rc 3, `box=NOT_ON_MONITOR reserved=NOT_APPLIED`).
- **Exit map.** 0 `CLEAN` · 1 `DIFFER` (box or band disagrees) · 2 `SETUP/ERROR` (unreadable, non-regular, oversized or malformed input; missing monitor) · 3 `NOT_FORMED` — `NO_LAYER` (declared level carries no entry with the namespace), `UNMODELLED` (declaration outside the model), `NO_BAR` (output exclusion). Unmodelled declarations are refused, never guessed. Scale ≠ 1 or transform ≠ 0 is refused (`monitors -j` is pixel-sized, the layer box is logical).
- **Named limits** (declaration and tool docstring, not afterthoughts): margined exclusive bands (above); scaled/transformed monitors; dynamic cross sizes; list-valued configs; `*` output patterns; multiple bars per config; static `monitor … addreserved` bands (the reported band mixes static and layer contributions; the tool assumes a zero static reserve); `mode` presets that rewrite layer/exclusive at runtime (S462 `bar.cpp:30-57`, `:355-361`); layer-rule effects; and any runtime change after the capture.

## Frozen measurement (cited, not re-run by this seat)

`quality/counters/c1-r77-barfoot.py` over `.ufo/waves/round-77/controls/c1-cases-r77.json` (15 cases, sha256 `7d6e2b1a…`), receipt `receipts/control-baseline-r77.txt` at rev a83e9bee: 15/15 cases correct; five named single-anchor mutants each killed (`level-top-swap` 3/15, `exclusive-false-ignored` 14/15, `no-centred-width` 14/15, `reserved-wrong-edge` 4/15, `per-side-margin-dropped` 14/15); the live-echo do-nothing control scores 8/15 (it cannot see `css-margins`, `drift-box`, `drift-reserved`, `output-excluded`, `wrong-edge-band`, `malformed-layers`, `per-side-margin`); tool selftest 18/18; contract line `MADO_R77_BARFOOT: … verdict=TARGET_MET`.

## Sources

- S457 — Hyprland v0.56.2 `src/render/Renderer.cpp` @ efb5099 (sha256 `9af8a74e…`): `arrangeLayerArray` :2587-2670, `applyExclusive` :2529-2585, `arrangeLayersForMonitor` :2673-2700.
- S458 — Hyprland v0.56.2 `src/debug/HyprCtl.cpp` @ efb5099 (`798b7c6c…`): `layersRequest` :647-700, monitors template :253, reserved print :281-282, level names :706-708.
- S459 — Hyprland v0.56.2 `src/desktop/reserved/ReservedArea.cpp` @ efb5099 (`0a52e145…`): parent/child constructor :19-35, `apply`/`applyip` :53-69.
- S460 — `protocols/wlr-layer-shell-unstable-v1.xml` @ efb5099 (`87e0b9c8…`): enum layer :86-90, `set_exclusive_zone` :152-190, margin sentence :196.
- S461 — waybar(5) manual, waybar 0.15.0 (`3972caaf…`; committed text rendering `fetch/S461.txt`): layer :64, output :72, position :85, height :93, width :99, margin :124, margin-<side> :130, exclusive :183.
- S462 — Waybar v0.15.0 `src/bar.cpp` @ 90b209a (`120eb913…`): margin precedence :178-222, namespace :232-233, size request :240, anchors :392-431, `setMode` exclusive :355-361.
- S463 (Wayland Explorer rendering of the same protocol) was opened 2026-11-04 and rejected: it pins no protocol or compositor revision, so the pinned XML (S460) is the authoritative copy.
