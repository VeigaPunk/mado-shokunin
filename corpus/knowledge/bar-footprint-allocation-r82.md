# The client's own band — a declared dynamic layer band on Hyprland 0.56.2 (MADO-R82-1, round 82)

**Scope.** What a layer surface's *band* is when the declaration is dynamic — `height = 0` on a
horizontal surface, `width = 0` on a vertical one — and how the round-82 join models it from a
declared `--allocation` map instead of refusing it. The band is the surface's extent on its
anchored axis, the number the compositor reserves for it; every claim below is about that number,
not about the surface's rendered content, its module text or the bar's live health.

**Evidence classes** (the lane's legend): `[OBS]` observed in this lane's own pinned bytes or a live
read; `[INF-src]` follows from a pinned source's code; `[DOC]` a pinned document's sentence;
`[UNK]` not established. Quotes are ≤25 words with a line anchor. Host reads are dated.

Sources: S481 (Hyprland 0.56.2's vendored `wlr-layer-shell-unstable-v1.xml`, fetched 2026-11-04,
`.ufo/waves/round-82/fetch/S481.xml`, sha256 `87e0b9c8…`); S464 (gtk-layer-shell v0.10.1
`src/layer-surface.c`, `.ufo/waves/round-79/fetch/S464.bin`); S470 (Hyprland 0.56.2
`src/render/Renderer.cpp`, `.ufo/waves/round-80/fetch/S470.bin`); S466
(`src/desktop/reserved/ReservedArea.cpp`, `.ufo/waves/round-79/fetch/S466.bin`). Held and cited,
not re-claimed: S459 (the reserved-area constructor's containment) and S473 (the keybindings
payload; unrelated to this ground and not cited below).

## 1. A zero size is the client's own

A layer surface asks for its size with `set_size(serial, width, height)`. The protocol says the size
is only a hint and, for the zero case:

> `If the width or height arguments are zero, it means the client should decide its own window dimension.` (S481:347-348)

`[DOC]` Three consequences the model must respect:

1. **The declaration is not the band.** A `height = 0` in a declaration is a request for the client
   to pick, not a zero-height bar. `[DOC]`
2. **The arranged box is not the band either.** Hyprland's arrange pass treats a zero desired size
   by spanning the bounds (`box.height == 0 → box.y = bounds.y`, then the auto-size branch fills the
   axis, S470:2622-2630), so the box the compositor computes from a zero request is the *available*
   box, not the client's chosen size. `[INF-src]` The two numbers diverge whenever the client picks
   less than the span.
3. **The band is the client's allocation.** gtk-layer-shell reads the GTK allocation it received and
   sends it as the exclusive zone — see §2. `[INF-src]` A join that lacks the allocation cannot know
   the band; it can only refuse.

**Why the round-81 join refused.** `surface_zone` raised on `height == 0` (the auto gate's band
axis) and `declared_box` raised on the bar's dynamic axis, both with stage `model`: the join had no
input for the number, and guessing the declaration would have printed a band the compositor never
reserves. `[OBS]` The refusal was per-axis and named: only the gate-selected band axis can be
dynamic.

## 2. The auto zone is the client's allocation

gtk-layer-shell's auto-exclusive-zone update (`layer_surface_update_auto_exclusive_zone`,
S464:264-292) is the whole rule, and its two arms are transposed:

```c
if (horiz && !vert) {
    new_exclusive_zone = self->current_allocation.height;
    if (!self->anchors[GTK_LAYER_SHELL_EDGE_TOP])
        new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_TOP];
    if (!self->anchors[GTK_LAYER_SHELL_EDGE_BOTTOM])
        new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_BOTTOM];
} else if (vert && !horiz) {
    new_exclusive_zone = self->current_allocation.width;
    …
}
```

`[OBS]` S464:276 is the `horiz` arm's size line, S464:282 the `vert` arm's; both read
`self->current_allocation`, the GTK allocation assigned from the size-allocate callback
(`layer_surface_on_size_allocate`, S464:298-310).

Three properties follow:

- **The gate is the anchor set, not the edge.** A zone is sent only when exactly one of
  `horiz = (LEFT == RIGHT)` and `vert = (TOP == BOTTOM)` holds; a corner, a parallel pair and an
  all-four set send `-1`, and Hyprland then keeps its previous zone (held since round 81).
- **The base is the allocation, not the declaration.** The difference is only visible when the two
  differ — i.e. exactly the dynamic-band case this note models.
- **The unanchored margin is added client-side.** For a top-anchored band the unanchored edge is the
  bottom one, so the client's zone is `allocation + margin.bottom`; Hyprland's `applyExclusive` then
  adds the *anchored* edge's margin (S470:2575-2583, held since round 78), so the reserved amount is
  `allocation + margin.bottom + margin.top`.

## 3. What the round-82 join now does

`tools/mado-barfoot.py` generation `r82-v1` adds one declared input and one resolver:

```
--allocation PATH|-     a JSON object {namespace: band}, the client's own band size
band_of(spec, map)      declaration first (spec[axis] > 0), else map[namespace], else refuse;
                        a zero band is a model refusal, a negative one a setup refusal
```

`[OBS]` The resolver is the single entry point for the band axis in both paths:

- `declared_box` (the single-surface join) resolves `height` for a horizontal surface and `width`
  for a vertical one through `band_of`, then arranges as before;
- `evaluate_composition` resolves the bar's band the same way before building `bar_spec`, so the
  bar's pass reserves the allocated band and later surfaces arrange under it.

The zone needs no separate change: `surface_zone` already reads `spec["height"]`/`spec["width"]` as
the allocation's stand-in (round 81's model, S464:276/282), so a resolved band is the zone.

**Refusals kept, one per class:**

| Input | Stage | Why |
|---|---|---|
| dynamic band, no `--allocation` entry | model (rc 3) | the band is the client's; nothing is guessed |
| `--allocation` band of 0 | model (rc 3) | gtk sends 0; Hyprland's `zone + margin > 0` guard reserves nothing |
| negative band | setup (rc 2) | not a declaration the protocol can carry |
| allocation for a namespace the composition lacks | setup (rc 2) | the join never guesses which surface an entry belongs to |
| per-axis dynamic band on an *extra* surface | model (rc 3) | out of this round's scope: the declaration grammar has no allocation field |
| monitor `scale != 1` or `transform != 0` | model (rc 3) | the reply is pixels and the layer box logical (held) |

## 4. Decision table

| # | Surface | Declaration | `--allocation` | Modelled result | Class |
|---|---|---|---|---|---|
| 1 | top bar | `height: 0` | `{"waybar": 34}` | box `0,0,3440,34`; zone 34; band 34 | modelled (case `alloc-dyn-height-top`) |
| 2 | top bar, margin 4 | `height: 0`, `margin: 4` | `{"waybar": 30}` | box `4,4,3432,30`; zone `30+4=34`; reserved `34+4=38` | modelled (case `alloc-dyn-height-margin`) |
| 3 | left dock | `width: 0` | `{"waybar": 60}` | box `0,0,60,1440`; zone 60; left band 60 | modelled (case `alloc-dyn-width-dock`) |
| 4 | top bar | `height: 0` | `{"waybar": 0}` | refused, model | named refusal |
| 5 | top bar | `height: 0` | `{"waybar": -4}` | refused, setup | named refusal |
| 6 | top bar | `height: 26` | `{"panel": 40}` | refused, setup (unknown namespace) | named refusal |
| 7 | top bar | `height: 26` | `{"waybar": 40}` | declaration wins: band 26 | modelled (case `alloc-explicit-ignored`) |
| 8 | top bar + level-3 panel | `height: 0` | `{"waybar": 34}` | bar 34, panel 12 under it, vector `0,46,0,0` | modelled (case `alloc-composition-dyn-bar`) |

## 5. Limits

1. **The allocation is caller-declared, not observed.** The join prints what the caller says the
   client was allocated; it does not read the surface's size back. A caller that declares 34 for a
   client allocated 40 gets a wrong answer, and the join cannot tell. The live join (round 77's
   mode) is what catches that: `DECL` vs `LIVE` prints DIFFER. `[OBS]`
2. **An extra surface's dynamic band stays refused.** The `--surfaces` grammar has no allocation
   field; only the bar (whose namespace the map keys) is resolved. This is per-axis and named.
3. **The composition path resolves the bar only.** An extra surface with `height: 0` is still
   arranged as a full span and its auto zone is still refused; the round-81 case
   `auto-dynamic-band-refused` is carried unchanged.
4. **Negative margins are still refused**, and the band arithmetic still adds both the client's
   unanchored margin and the compositor's anchored one; a caller that thinks one is included twice
   can check case 2's `38`.
5. **No fractional scale.** `scale != 1` remains a model refusal (round 79's `refuse-scale` row
   binds it), so the allocation is in the monitor's logical pixels only.
6. **The protocol clause is not a host observation.** S481 says what a zero size *means*; it does
   not say what waybar sends on this host today, and the join's `--allocation` is the caller's
   declaration either way.

## 6. Where this sits

Round 77 measured the bar's footprint from the declaration; round 78 composed the margins; round 79
composed the static reserve; round 80 composed more than one exclusive surface; round 81 modelled
the coupled rounding and the auto gate and named the dynamic band `NOT_MODELLED`; this round models
it for the bar through a declared allocation and keeps every other refusal in force. The next finite
ground is the transposed composition (an extra surface whose band is dynamic) or the fractional
scale, both of which need a grammar change before a case can exist.

## sources

`source:` S481, S464, S470, S466.
