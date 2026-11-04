# The bar's footprint: declared waybar config → live layer box → monitor reserved band

source: S457 Hyprland v0.56.2 src/render/Renderer.cpp @ efb5099 (arrangeLayerArray, applyExclusive, arrangeLayersForMonitor); S458 src/debug/HyprCtl.cpp @ efb5099 (layers request, monitors reserved print); S459 src/desktop/reserved/ReservedArea.cpp @ efb5099 (parent/child band); S460 protocols/wlr-layer-shell-unstable-v1.xml @ efb5099 (levels, exclusive zone); S461 waybar(5) 0.15.0 (position, layer, height, width, margin, exclusive); S462 Waybar v0.15.0 src/bar.cpp (margin precedence, namespace, size request, exclusive zone); S464 gtk-layer-shell v0.10.1 src/layer-surface.c (auto exclusive zone)
verified-at: 2026-11-04 (schema and host join re-measured; fetch receipts `.ufo/waves/round-77/fetch/S457.bin` … `S464.bin`, sha256 in `fetch/sha256-r77.txt`)
recheck: on-release (Hyprland after v0.56.2 or Waybar after 0.15.0); 180d otherwise — re-pin the seven files, re-capture `hyprctl layers -j` and `hyprctl monitors -j`, re-run `tools/mado-barfoot.py`
ground: what sets a waybar bar's position and size on this compositor, what the monitor's `reserved` band owes to that surface, and which part of the chain `hyprctl layers` cannot show
Lane: mado-shokunin. Round: 77.

## What this entry holds

| question | where the answer lives | state |
|---|---|---|
| What box does a top-anchored layer surface with a requested height get? | `arrangeLayerArray`: desired size, anchors, margins (`Renderer.cpp:2587-2670`) | OBS (source) |
| What happens when a bar requests an explicit width? | waybar clears both horizontal anchors (`bar.cpp:422-424`); the both-anchors branch then centres the box (`Renderer.cpp:2609-2620`) | OBS (source) |
| How does an exclusive zone become a reserved band? | `applyExclusive` adds `exclusive + margin` to the usable box (`Renderer.cpp:2529-2585`, add line :2577); `arrangeLayersForMonitor` stores the parent-minus-child difference (`Renderer.cpp:2696`) | OBS (source) |
| Which level carries waybar? | level 2 = top in `layers -j` (`HyprCtl.cpp:706`, protocol enum `S460`) | OBS (source) + OBS (host) |
| In what order does `monitors -j` print `reserved`? | left, top, right, bottom (`HyprCtl.cpp:281-282`) | OBS (source) + OBS (host) |
| What does the bar declare, and does the live box agree? | `~/.config/waybar/config.jsonc` + `hyprctl layers -j` | OBS (host, 2026-11-04) |
| Is the reserved band exactly the bar's height? | equal here (26 px, zero margins); with non-zero margins the auto-zone composition is not modelled (`NOT_MODELLED`) | OBS (host) / UNK (margined bars) |

## §1 The chain, link by link

**1. Declaration.** waybar 0.15.0 reads `position` (top/bottom/left/right, default top), `layer` (top or bottom, default bottom), `height`/`width` (requested sizes, blank = dynamic), `margin` (CSS format: 1/2/3/4 integers) or `margin-<side>` (integers), and `exclusive` (bool, default true). Source S461 (`BAR CONFIGURATION`; headings at rendered lines 64/85/93/124/183, their text at 70/91/97/128/189) and S462 (`bar.cpp:178-222`, `:232-233`, `:240`, `:355-361`). The per-side form wins when any `margin-<side>` is an integer; otherwise a `margin` string is read in CSS order; otherwise an integer `margin` sets all four sides (`bar.cpp:178-222`). The layer namespace is the config's `name`, else `waybar` (`bar.cpp:232-233`).

**2. Size request and anchors.** The bar requests `(width, height)` as its desired size (`bar.cpp:240`); a horizontal bar with an explicit width > 1 clears both horizontal anchors, and a vertical bar with an explicit height > 1 clears both vertical anchors (`bar.cpp:419-426`). The compositor then places the surface.

**3. Arrange.** `arrangeLayerArray` computes the box (S457, `Renderer.cpp:2587-2670`): a zero desired width spans the usable box minus horizontal margins, with both horizontal anchors set; a non-zero desired width is centred and the margins are not applied horizontally. The same rule transposed applies to vertical bars. The box is rounded (`:2660`), then `applyExclusive` adds the exclusive zone and the edge margin to the usable area on the anchored edge (`:2664`): `*edges[i].positive_axis += exclusive + edges[i].margin;` (add at `:2577`, rule `:2575-2583`). Only one edge wins per surface: the singular anchor, the anchor triplet at the same edge, or the exclusive edge (`:2575-2583`).

**4. Reserved.** `arrangeLayersForMonitor` resets the dynamic layer-shell contribution, runs the exclusive pass and then the non-exclusive pass, and stores `CReservedArea{ORIGINAL_USABLE_AREA, usableArea}` (`Renderer.cpp:2673-2700`). The parent/child constructor turns the two boxes into a per-side band (S459, `ReservedArea.cpp:19-35`); `apply()` subtracts it from the logical box (`:53-60`). So a top bar of height `h` with no margins shrinks the usable area by `h` and produces `reserved.top = h`.

**5. The reply.** `hyprctl layers -j` is keyed by monitor, then by level `0..3` in background/bottom/top/overlay order; each entry carries `address x y w h alpha namespace pid` (S458, `HyprCtl.cpp:647-700`, level names `:706`). `hyprctl monitors -j` prints `reserved` as left, top, right, bottom (S458, `HyprCtl.cpp:281-282`). The protocol's own contract (S460): a positive exclusive zone is meaningful only for a one-edge or edge-plus-perpendicular anchor, and it is the distance from that edge in surface-local coordinates.

## §2 The host join, measured 2026-11-04

The declared bar (`~/.config/waybar/config.jsonc`): `"layer": "top"`, `"position": "top"`, `"height": 26`, no `margin`/`margin-<side>`, no `exclusive` key (default true). The monitor (`hyprctl monitors -j`, capture `fetch/live-monitors-r77.json`, sha256 `e732af34…`): DP-1 3440x1440 @ 99.997 Hz, scale 1, reserved `[0, 26, 0, 0]`. The layer reply (`fetch/live-layers-r77.json`, sha256 `46eb2481…`): DP-1 level 0 `wallpaper` at 0,0,3440,1440; level 2 `waybar` at 0,0,3440,26; levels 1 and 3 empty.

The join (`tools/mado-barfoot.py`, receipt `.ufo/waves/round-77/receipts/pre-wave-evidence-r77.txt`):

    MADO_BARFOOT_DECL: monitor=DP-1 box=0,0,3440,26 edge=top
    MADO_BARFOOT_LIVE: monitor=DP-1 level=2 ns=waybar box=0,0,3440,26 entries=1
    MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN

INF: the usable area of DP-1 is 3440 x 1414, starting at y = 26 (the band is the bar's own height; the reserved array's other sides are zero). UNK: which process set the top layer's exclusive zone is not read — the layer entry carries `namespace` and `pid`, not the zone; the join names the namespace, not the request. The `wallpaper` surface at level 0 has no reserved contribution because the host's band matches the bar's height exactly; a level-0 surface with a positive exclusive zone would add to the band and the tool would report `reserved=GT` (the exclusive pass is level-agnostic).

## §3 The tool contract

`tools/mado-barfoot.py` (`VERSION r77-v1`) is a read-only join over three caller-supplied artifacts: the waybar JSONC config, a captured `hyprctl layers -j` reply, a captured `hyprctl monitors -j` reply, plus an optional `--monitor`. It derives the declared box (the five links above except the compositor execution), finds the live entry with the declared namespace at the declared level, and prints one `MADO_BARFOOT_RESULT:` line with `box=MATCH|DIFFER|NO_LAYER|NOT_ON_MONITOR` and `reserved=EQ|GT|DIFFER|NOT_APPLIED|NOT_MODELLED|NOT_CHECKED`. Exit map: 0 `CLEAN`, 1 `DIFFER`, 2 setup/parse error, 3 not formed. It writes nothing, opens no socket and starts no process.

## §4 What the model does not cover

- **Margined exclusive bars (any margin, not only the edge one).** gtk-layer-shell 0.10.1's auto zone is the allocation plus the margins on the *unanchored* edges (S464, `layer-surface.c:264-292`: `new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_BOTTOM];`), and Hyprland then adds the anchored edge's margin (S457, `Renderer.cpp:2575`), so `band - extent` is the opposite-edge margin. With any non-zero margin the reserved expectation is `NOT_MODELLED`; the box itself is still modelled.
- **Scaled or transformed monitors.** `hyprctl monitors -j` prints `width`/`height` from `m_pixelSize` (`HyprCtl.cpp:278`) while every layer box is logical (`m_size = pixelSize / scale`), so a scale-2 output would overstate the declared box. The tool refuses a monitor whose `scale` is not 1 or whose `transform` is not 0 (`UNMODELLED`, exit 3).
- **Dynamic cross size.** A horizontal bar with `height` unset (or 0) gets the module allocation, not a declared value; the tool refuses rather than computing the whole usable height (`UNMODELLED`).
- **Static `monitor … addreserved` bands.** The reported band mixes the static reserve with the layer contribution (`logicalBoxMinusReserved()`), and the tool assumes a zero static reserve; a static band is a named, unmodelled case.
- **`mode` presets.** `mode: hide|invisible|overlay` rewrites layer and exclusive zone at runtime (`bar.cpp:326-361`); a `mode` key is refused (exit 3) rather than read past.
- **Centring rounding.** Floor division vs Hyprland's round-after-double differs by 1 px on odd deltas.
- **Frozen-set gaps named by the mutation tester.** No case declares a right-anchored bar (the right edge extent is untested; a `position=right` case with reserved `[0,0,40,0]` would kill the survivor), no case exercises an exclusion-only output spec (`output: "!M2"` on M1), and no case declares `layer: bottom` (the level lookup and the bottom-level reserve are untested). All three are source-licensed and case-unexercised; the frozen set stays as declared and the cases are round-78 candidates.
- **Runtime after the capture:** a layer mapped or destroyed after the dump is outside the join; only a fresh capture sees it.
- **Who set the zone:** the reply has no exclusive-zone field (`HyprCtl.cpp:671-682`); the namespace is evidence of the surface, not of the request.

## Evidence

- `.ufo/waves/round-77/fetch/S457.bin`–`S464.bin` and `sha256-r77.txt` (seven pinned sources, byte receipts).
- `.ufo/waves/round-77/fetch/live-layers-r77.json`, `live-monitors-r77.json` (host captures, sha256 in `receipts/pre-wave-evidence-r77.txt`).
- `.ufo/waves/round-77/receipts/control-baseline-r77.txt` — frozen 15-case score 15/15, five mutants killed, live-echo control 8/15; `MADO_R77_CONTROL` sha256 `7d6e2b1a…`.
- `.ufo/waves/round-77/controls/c1-cases-r77.json` — the frozen case set (generator `controls/make-cases-r77.py`).

## Sources

S457, S458, S459, S460, S461, S462, S464 in [SOURCES](../SOURCES.md). S463 (wayland.app) was opened and rejected: it renders the protocol without a revision pin, so the pinned XML is the authoritative copy.

## Erratum (round 78, append-only)

This entry records the r77 instrument (`tools/mado-barfoot.py`, `VERSION r77-v1`) at the revision it
was measured (`a83e9bee`; later r77 repairs up to `de627316`). From round 78 the tracked tool is
`r78-v1`: it composes the margined band instead of returning `NOT_MODELLED`, refuses a negative
margin, and its selftest is 22/22. The sentences "the reserved expectation is formed only when
`exclusive` is true and every margin side is zero", "a margined exclusive bar reports `NOT_MODELLED`"
(§3) and "with any non-zero margin the reserved expectation is `NOT_MODELLED`" (§4) describe the r77
bytes only and are superseded by [the margined band entry](bar-footprint-margins-r78.md). The r77
frozen set and its counter stay as they were; `mado-r77-barfoot-counter` scores them.
