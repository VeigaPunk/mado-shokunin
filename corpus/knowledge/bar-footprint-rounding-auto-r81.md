# The composition's rounding and the auto-zone gate (round 81)

source: S478, S479; held S464, S470, S471, S473
verified-at: 0e2ccd2a8692825cac534f57246053b276be9f13 (the round-81 freeze; the landing commit re-runs
the same command)
recheck: `python3 -I quality/counters/c1-r81-overflow-auto.py --repo . --rev REV --base-rev
c702094ace5dd9b2b5e152951b4b2f4dd578f8b6 --controls .ufo/waves/round-81/controls/c1-cases-r81.json
--carried .ufo/waves/round-80/controls/c1-cases-r80.json --scratch-root DIR` — 39 frozen cases, 28
mutants, exit 0 on `TARGET_MET`

## 0. What this entry is, and what it is not

The round-80 entry (`bar-footprint-composition-r80.md`) composed N layer surfaces under the running
usable box and listed four reachable classes where its model was **wrong** (§11). This entry closes
three of them on the source that states each, and records the fourth as a deliberate refusal. Every
proposition is read from the host's own compositor version at commit `efb5099…` (Hyprland 0.56.2) and
from the client library whose zone the compositor stores, and is reproduced by the lane's join in
`.ufo/waves/round-81/receipts/measurement-c1-r81.txt`.

It is a **model over captured bytes**: no layer surface is created, no compositor verb is run, and
nothing about a *particular* host consumer is claimed beyond the captures named in a receipt.

## 1. `CBox::round` is coupled

Hyprland centres a both-anchors box in doubles and rounds once:

```c
box.x = bounds.x + ((bounds.width / 2) - (box.width / 2));
...
box.round(); // fix rounding errors
```

(`Renderer.cpp:2613` and `:2660`, held S470). The rounding is not per-field: hyprutils rounds the
origin first and then the far edge's *distance from that origin* (S478 `src/math/Box.cpp:51-63`):

```cpp
double roundedX = std::round(x);
double newW     = x + w - roundedX;
x = roundedX;
w = std::round(newW);
```

So a panel one pixel wider than its bounds, both horizontal anchors, at the layout origin:

| value | source arithmetic | round-80 model |
|---|---|---|
| `(bounds.width / 2) - (box.width / 2)` | `500 - 500.5 = -0.5` | offset floor-divided: `(1000-1001+1)//2 = 0` |
| `x` after `std::round` | `-1` (half away from zero) | `0` |
| `w` after `std::round(-0.5 + 1001 - (-1))` | `round(1001.5) = 1002` | `1001` (never recomputed) |

Frozen case `overflow-tie-negative` pins `box=-1,363,1002,100`. The two models agree on every box
that fits its bounds (the tie's absolute coordinate is non-negative there), which is why the
round-80 set never saw the divergence: `x` and `w` move together only when the tie is a negative
half.

`std::round` is half **away from zero** (C++11 26.8/9), not Python's banker's rounding:
`std_round(-0.5) = -1`, `std_round(0.5) = 1`. The join implements it explicitly.

## 2. Which hyprutils revision this is

The rounding lives in hyprutils, not in Hyprland. Hyprland's `CMakeLists.txt` at the host's commit
pins the dependency (S479 `:150`):

```
set(HYPRUTILS_MINIMUM_VERSION 0.14.0)
```

The row cites the pinned `v0.14.0` tag as the licence to fetch, and the class is `[INF]` on one
point: the *minimum* version is what Hyprland declares, not what the host has installed. The host's
installed hyprutils package version was not read this round; the function has this shape at
`v0.14.0`, and a later version could change it. A re-check opens the tag the host's package manager
reports.

## 3. The auto zone is the client's

The compositor stores whatever integer a client sends (`LayerShell.cpp:100-102`, held S471). For
`exclusive = auto` that integer is computed by gtk-layer-shell (S464
`layer_surface_update_auto_exclusive_zone`, `:264-292`):

```c
gboolean horiz = (self->anchors[GTK_LAYER_SHELL_EDGE_LEFT] ==
                  self->anchors[GTK_LAYER_SHELL_EDGE_RIGHT]);
gboolean vert = (self->anchors[GTK_LAYER_SHELL_EDGE_TOP] ==
                 self->anchors[GTK_LAYER_SHELL_EDGE_BOTTOM]);
```

Three facts follow, and the join now models all three:

1. **The gate is `horiz XOR vert`** (`:275`, `:281`). Both true (all four anchors, or a parallel
   pair such as `top|bottom`, where both sides of each comparison are equal) and both false (a
   corner pair) send **no** zone at all — the stored value stays `0`/unset.
2. **The size is the allocation's** (`:276` `current_allocation.height`, `:282`
   `current_allocation.width`), not the declared size. For a declared band of `h > 0` the arranged
   box carries that size, so the join can compute it; for `h = 0` the allocation is the client's own
   content and the join has no input for it, so the join **refuses** (`ERROR (stage=model auto zone
   on a dynamic height (0) is the client's allocation, not a declared value)`).
3. **The unanchored margins are added** (`:278-280`, `:284-286`): for a top bar the bottom margin,
   for a left dock the right margin.

The round-80 model computed `size + margin[opposite]` from the *position* for every anchor set, so it
gave a corner or all-four surface a zone the client never sends, and it gave a zero-height surface
`0` instead of refusing.

## 4. The gate in composition

A zone the client never sends cannot reserve anything, and an explicit `exclusiveEdge` does not
manufacture one: the edge only picks *which* rule `applyExclusive` may match (`Renderer.cpp:2575`,
held S470). The frozen cases pin the three shapes:

| Case | Declaration | What the join now does |
|---|---|---|
| `auto-corner-edge` | anchors `top,left`, `exclusiveEdge: top`, auto | zone 0; the box is arranged at the running box's top-left; band unchanged |
| `auto-parallel-edge` | anchors `top,bottom`, `exclusiveEdge: top`, auto | zone 0 (both gates true); no shrink despite the edge |
| `auto-all-four-edge` | all four anchors, `exclusiveEdge: top`, auto | zone 0; the box centres at `400,363,200,100` |
| `auto-left-dock` | anchor `left`, width 40, height 0, auto | zone = allocation width 40 + right margin; the left rule shrinks the usable box, the bar's box starts at `x=40`, and the attribution vector reads `40,26,0,0` |

`auto-left-dock` is also the second pinned **left/right attribution**: the round-80 set only ever
attributed a band on `top` (or none), so the left rule's bookkeeping had no frozen case.

## 5. What the join prints

The six new cases pin these `RESULT` fields (`MADO_BARFOOT_RESULT:`): `box` (the bar's own box
state), `boxes` (one state per declared surface in arrangement order), `band` (the monitor's
`reserved` value for the bar's edge), `expected`/`attributed` (the model's two totals for that
edge), `gt` (the monitor's whole `reserved` vector) and `attr` (the model's whole attributed
vector). A refusal prints `MADO_BARFOOT: ERROR (stage=model …)` and exits 3; a model disagreement
exits 1.

## 6. Limits

- **The allocation is not modelled.** `auto` with a dynamic band is a refusal, not a prediction. A
  waybar with `height = 0` would need waybar's own module measurement; that is out of this join's
  input set.
- **The refusal is per-axis.** A `height = 0` surface whose gate is vertical (a left/right surface)
  is modelled from its width; only the gated axis can be dynamic here.
- **The declaration grammar's `exclusive` default is still `auto`.** A plain client declared without
  the key therefore reserves as if it were a bar; the round-80 §11 item 4 defect stays **open** and
  is named again rather than silently fixed (changing the default would move four carried cases,
  which the frozen contract forbids).
- **The gtk-layer-shell version is pinned, not read.** S464 is `v0.10.1`; the host's installed
  library version was not read this round. The gate's shape is long-standing, but the claim is bound
  to the pinned tag.
- **`CBox::empty()`'s label boundary** (round-80 §13) is unchanged: an exactly empty composed box
  prints `ls=INVALID` where `CReservedArea`'s `empty()` yields a valid zero.
