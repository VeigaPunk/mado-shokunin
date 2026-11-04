# The margined bar footprint: client auto zone + compositor band

source: S457 Hyprland v0.56.2 `src/render/Renderer.cpp` @ efb5099 (`applyExclusive`, `arrangeLayerArray`); S458 `src/debug/HyprCtl.cpp` (layers reply, monitors `reserved`); S459 `src/desktop/reserved/ReservedArea.cpp` (parent/child band); S460 wlr-layer-shell-unstable-v1 XML (exclusive-zone contract); S461 waybar(5) 0.15.0 (placement keys); S462 Waybar v0.15.0 `src/bar.cpp` @ 90b209ad (margins, anchors, auto-zone call); S464 gtk-layer-shell v0.10.1 `src/layer-surface.c` (client auto zone). All seven re-opened 2026-11-04 with fresh pinned fetches under `.ufo/waves/round-78/fetch/` (sha256 in `sha256-r78.txt`, byte-identical to the round-77 copies).
verified-at: 2026-11-04, round 78, instrument revision `44a36b64117812af7cc23a1815430d8320642455` (tool sha256 `aac5d41b…`)
recheck: on-release (Hyprland after v0.56.2, Waybar after 0.15.0, gtk-layer-shell after v0.10.1); 180d otherwise — re-open the seven files, re-capture `hyprctl layers -j` / `hyprctl monitors -j`, and re-run `tools/mado-barfoot.py`
Lane: mado-shokunin. Round: 78. Supersedes only the `NOT_MODELLED` limit of `bar-footprint-r77.md` §4; the round-77 chain description stands.

## What this entry holds

| question | where the answer lives | state |
|---|---|---|
| What exclusive zone does the bar's client library submit? | `layer_surface_update_auto_exclusive_zone`: allocation on the band axis plus the margin of each *unanchored* edge of that axis (`S464:264-288`) | OBS (source) |
| What does the compositor add to it? | `applyExclusive`: `exclusive + edges[i].margin` on the anchored edge (`S457:2575-2583`, add `:2577`) | OBS (source) |
| Which edge's margin does each side add? | the client adds the *opposite* (unanchored) edge's margin; the compositor adds the *anchored* edge's margin | OBS (source) |
| So what is the reserved band of a margined bar? | `height + margin.top + margin.bottom` for a top/bottom bar; `width + margin.left + margin.right` for a left/right bar | INF (source composition) |
| Do cross-axis margins enter the band? | no: a horizontal bar's left/right margins only move/resize a zero-width box (`S457:2636-2637`) | OBS (source) |
| Is the band's box arithmetic unchanged? | yes: `arrangeLayerArray` positions the box at the anchored margin and the band ends at the opposite margin (`S457:2646-2651`, `:2664`) | OBS (source) |
| Does the host's live join agree? | `host-top` (no margins, 26 px band) is the round-77 capture; every margined case here is a committed fixture, not a host observation | OBS (fixture) / UNK (host) |

## §1 The composition, link by link

1. **Declaration.** Waybar reads `margin-<side>` integers (per-side wins when any is an integer,
   `S462:178-185`), else a CSS-order `margin` string (`:186-216`), else an integer `margin`
   (`:218-220`). All four sides start at zero; a parse failure leaves zeros.
2. **Anchors.** All four edges are anchored (`S462:393-394`); the configured `position` frees one
   edge — top frees bottom, bottom frees top, left frees right, right frees left (`:398-411`) —
   and a horizontal bar with `width > 1` frees both left and right, a vertical bar with
   `height > 1` frees both top and bottom (`:413-424`).
3. **Client auto zone.** Waybar enables it when the mode is exclusive (`S462:357-361`; when it is
   not, it sets zone 0 explicitly). gtk-layer-shell then computes, when the left and right anchors
   agree and the top and bottom anchors do not (a horizontal bar), the allocation height plus the
   margin of each *unanchored* vertical edge (`S464:266-280`); the transposed branch gives the
   allocation width plus the unanchored horizontal margins (`:281-287`). A top bar is anchored at
   top, so it adds only the bottom margin; a bottom bar adds only the top margin.
4. **Compositor band.** `arrangeLayerArray` places the box at the anchored edge's margin
   (`S457:2646-2651`), then `applyExclusive` adds `exclusive + edges[i].margin` on that edge —
   the anchored edge's margin (`:2575-2583`, add `:2577`; the band grows from the monitor's usable
   origin, so the box offset and the band's start coincide). A top bar therefore reserves
   `height + margin.bottom` (client) `+ margin.top` (compositor); a bottom bar reserves
   `height + margin.top` (client) `+ margin.bottom` (compositor). Both sides are in the band in
   either case.
5. **Reserved.** `arrangeLayersForMonitor` stores the parent-minus-child difference
   (`S457:2696`), which `ReservedArea` turns into the per-side band (`S459:19-35`, `:53-60`) that
   `hyprctl monitors -j` prints as left, top, right, bottom (`S458:281-282`).

## §2 Decision table — reachable declaration → expected band

| declaration (horizontal bar unless stated) | client zone | compositor adds | reserved band | ref |
|---|---|---|---|---|
| top, `height h`, no margins | `h` | 0 | top `h` | `S464:276`, `S457:2577` |
| top, `height h`, `margin 4` (all sides) | `h + 4` | `4` | top `h + 8` | `S464:280`, `S457:2577` |
| top, `height h`, `margin "4 8"` (vertical 4, horizontal 8) | `h + 4` | `4` | top `h + 8` (the 8s are cross-axis) | `S462:190-196`, `S457:2636-2637` |
| top, `height h`, `margin-top 10`, `margin-bottom 2` | `h + 2` | `10` | top `h + 12` | `S462:178-185` |
| bottom, `height h`, `margin 8` | `h + 8` (top margin) | `8` (bottom margin) | bottom `h + 16` | `S464:278`, `S457:2580` |
| left, `width w`, `margin 6` | `w + 6` (right margin) | `6` (left margin) | left `w + 12` | `S464:284`, `S457:2577` |
| right, `width w`, `margin 5` | `w + 5` (left margin) | `5` (right margin) | right `w + 10` | `S464:286`, `S457:2580` |
| top, `width 800`, `margin 4` (explicit width) | `h + 4` | `4` | top `h + 8`; the box is centred and its margins are not applied horizontally | `S462:413-424`, `S457:2639-2640` |
| top, `exclusive: false` | 0 | 0 | no band | `S462:359-360` |
| top, `layer: bottom`, `height h` | `h` | 0 | top `h` (the exclusive pass is level-agnostic) | `S457:2673-2700` |
| `output: "!M2"` on M1 | as declared | as declared | as declared on M1 (no bar on M2) | `S462:232-233`-adjacent route |

A negative margin is **refused**, never composed: `applyExclusive` skips an edge whose
`exclusive + margin` is not positive (`S457:2575`), so the band can vanish or invert and this
model does not cover it.

## §3 The instrument and its frozen evidence

`tools/mado-barfoot.py` (`VERSION r78-v1`, sha256 `aac5d41b…`, `--selftest` 22/22) forms the
reserved expectation as `edge_extent + margin[opposite_edge]`, where `edge_extent` is the
anchored-edge distance to the box's far side. The frozen eighteen-case set
(`.ufo/waves/round-78/controls/c1-cases-r78.json`, sha256 `99f1d82f…`, generated by
`controls/make-cases-r78.py`) covers all four positions, the three margin forms, the three
round-77-named gaps (right-anchored bar, `layer: bottom`, exclusion-only `output`), the refusal
paths, and a second consumer (`reserved=GT`, admissible but not attributed).

Measured at `44a36b64` with
`python3 -I quality/counters/c1-r78-margins.py --repo . --rev 44a36b64 --base-rev f597eccb… --controls …`:

    MADO_R78_BARFOOT: cases=18 correct=18 mutants=7 killed=7 base_correct=8/18
    tool_selftest=22/22 verdict=TARGET_MET rev=44a36b64…

The held round-77 model (no margin composition, no negative-margin refusal) scores `8/18` on the
same cases; the seven named mutants of the r78 rule each lose at least one case
(`opposite-margin-dropped` 9/18, `horizontal-margin-leak` 9/18, `level-bottom-swap` 14/18,
`right-extent-flip` 13/18, `per-side-margin-dropped` 14/18, `negative-margin-accepted` 14/18,
`opposite-edge-wrong` 14/18). Receipt: `.ufo/waves/round-78/receipts/measurement-c1-r78.txt`.

## §4 What the model does not cover

- **Static `monitor … addreserved` bands.** The reply mixes the static reserve with the layer
  contribution; the tool assumes a zero static reserve.
- **Scaled or transformed monitors.** `monitors -j` prints pixel size while layer boxes are
  logical; a scale ≠ 1 or a transform ≠ 0 is refused (`UNMODELLED`).
- **Dynamic cross size.** A horizontal bar with `height` 0 (or a vertical bar with `width` 0)
  gets the module allocation; refused rather than computed.
- **Centring rounding.** Floor division vs Hyprland's round-after-double differs by 1 px on odd
  deltas.
- **Second exclusive consumer.** The band is a sum; a larger band is reported `GT` (admissible)
  and is not attributed to a surface.
- **Negative margins.** Refused; the client and compositor both treat them as arithmetic, not as
  absolute values, and this model does not.
- **Who set the zone.** The layer reply carries no exclusive-zone field; the namespace is
  evidence of the surface, not of the request.
- **Runtime after the capture.** A surface mapped or destroyed after the dump is outside the join.

## Evidence

- `.ufo/waves/round-78/fetch/S457.bin`–`S464.bin` and `S461.txt`, sha256 in `sha256-r78.txt`
  (byte-identical to the round-77 fetches).
- `.ufo/waves/round-78/controls/c1-cases-r78.json` and `controls/make-cases-r78.py`.
- `.ufo/waves/round-78/receipts/measurement-c1-r78.txt` (per-case, per-mutant and contract lines)
  and `receipts/control-baseline-c1-r78.txt` (the base-revision red run, 8/18).

## Sources

S457, S458, S459, S460, S461, S462, S464 in [SOURCES](../SOURCES.md). S463 (wayland.app) stays
rejected: it renders the protocol without a revision pin, so the pinned XML (S460) is the
authoritative copy.
