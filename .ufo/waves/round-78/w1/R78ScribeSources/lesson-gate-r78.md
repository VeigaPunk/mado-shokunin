# round 78 — lesson `## Gate` draft (R78ScribeSources, prose only; the L1 integrates)

Paste target: `corpus/lessons/round-78.md` § Gate. No committed lane file is edited by this seat.

## Gate (sources re-opened this round)

Seven held rows were re-opened 2026-11-04 before the round's entry was written — no new row, no
reused id: the registry stays at **401 rows** (S001–S464; A 386 + B 7 + C 8). The round's bytes
are re-pinned under `.ufo/waves/round-78/fetch/`; `sha256sum -c sha256-r78.txt` prints six `OK`
(S457, S458, S459, S460, S462, S464), and `cmp` against the round-77 copies prints identical for
all seven fetched artifacts including `S461.txt` (`d59c4651…`). Census at `corpus/SOURCES.md` blob `33c02802` (unchanged from `93a10a13` to `d27c5ff4`): exit 0,
0 malformed rows, 0 duplicate ids, 0 enum violations, 0 missing `used-by` paths; the only output
is the standing W01/W04 warning set (48 W04, 1 W01).

Quote cells carry one or two **verbatim** source fragments, each with its own line locator; a
fragment is never reflowed or stitched across a line break. Line numbers are in the round-78
fetch bytes, `wc -l` unchanged from round 77.

| row | URL | locator | accessed | status | quote (≤25 words, located) | what it licenses / does not license |
|---|---|---|---|---|---|---|
| S457 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/render/Renderer.cpp | `Renderer.cpp` @ efb5099, `applyExclusive :2529-2585`, `arrangeLayerArray :2587-2670`, `arrangeLayersForMonitor :2673-2700` | 2026-11-04 | mined (unchanged) | `*edges[i].positive_axis += exclusive + edges[i].margin;` (:2577, 5 tokens) | Licenses the **compositor-side contributor** of this round's join: the edge selected at :2575 by `exclusiveEdge` or by the singular/triplet anchor receives `exclusive + edges[i].margin`, and the loop then `break`s (:2581) so exactly one margin is added; the guard also requires a positive sum. It does **not** license the client-side zone (S464), which margin an ambiguous multi-anchor surface should use, or that the guard's positivity test is a margin refusal — the tool's refusal of a negative margin is the tool's rule, not this function's. |
| S458 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp | `HyprCtl.cpp` @ efb5099, `layersRequest :647-700`, reserved template `:253`, print `:281-282`, command `:2010` | 2026-11-04 | mined (unchanged) | `sc<int>(m->m_reservedArea.left()), sc<int>(m->m_reservedArea.top())` (:281, 2 tokens) | Licenses the reply shape and the reserved print order — left, top, right, bottom (:281-282) — which the join parses. It does **not** say which surface set the zone, and it does **not** license a unit conversion: the round-78 tool refuses a monitor whose `scale` is not 1 or whose `transform` is not 0. |
| S459 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/reserved/ReservedArea.cpp | `ReservedArea.cpp` @ efb5099, parent/child constructor `:19-35`, `apply`/`applyip` `:53-60` | 2026-11-04 | mined (unchanged) | `m_initialBottomRight = (parent.pos() + parent.size()) - (child.pos() + child.size());` (:34, 9 tokens) | Licenses the parent/child reserved band the reply's four integers carry. It does **not** license a per-consumer attribution (which namespace produced the band). |
| S460 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/protocols/wlr-layer-shell-unstable-v1.xml | protocol XML @ efb5099, enum `layer :86-90`, request `set_exclusive_zone :152-190` | 2026-11-04 | mined (unchanged) | `The exclusive zone includes the margin.` (:196, 6 tokens) | Licenses the layer levels and the exclusive-zone contract: the client submits a zone that already includes its margin. It is a **contract, not host behaviour** — it does not say how Hyprland composes the band (that is S457). |
| S461 | host file `/usr/share/man/man5/waybar.5.gz` (`man -w waybar`) | installed `waybar(5)` 0.15.0, `BAR CONFIGURATION` (:38), quote at decompressed line 91 | 2026-11-04 | mined (unchanged) | `Bar position, can be \fBtop\fR, \fBbottom\fR, \fBleft\fR, \fBright\fR.\&` (:91, 8 tokens) | Licenses the declared placement keys and defaults (`position`, `layer`, `height`, `width`, `margin`, `margin-<side>`, `exclusive`). It does **not** license what gtk-layer-shell or the compositor does with them. |
| S462 | https://raw.githubusercontent.com/Alexays/Waybar/90b209add8937514d0a987aa842e701bd8f1232e/src/bar.cpp | `bar.cpp` @ 90b209ad, margin precedence `:178-222`, namespace `:232-233`, size request `:240`, `setMode` `:355-361` | 2026-11-04 | mined (unchanged) | `gtk_layer_auto_exclusive_zone_enable(gtk_window);` (:358, 1 token) | Licenses that exclusive mode reaches the auto-zone API (guarded by `if (mode.exclusive)` at :357) while the non-exclusive branch sets the zone to 0 (:360), so S464's arithmetic is what the host actually submits, and that the margins it sums come from the precedence chain at `:178-222`. It does **not** license the zone arithmetic itself or any band value. |
| S464 | https://raw.githubusercontent.com/wmww/gtk-layer-shell/v0.10.1/src/layer-surface.c | `layer-surface.c` @ v0.10.1, `layer_surface_update_auto_exclusive_zone :264-292` | 2026-11-04 | mined (unchanged) | `new_exclusive_zone = self->current_allocation.height;` (:276, 3 tokens) + `new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_BOTTOM];` (:280, 3 tokens; 6 total) | Licenses the **client-side contributor**: the auto zone starts at the allocation on the band axis (:276 horizontal, :282 vertical) and adds the margin of each *unanchored* edge of that axis (guards :277 and :279; transposed twins :283 and :285), then submits it via `zwlr_layer_surface_v1_set_exclusive_zone` (:289-291). It does **not** license the compositor side (S457) and does **not** license the cross-axis margins. |

Not re-opened, unchanged: **S463** (`https://wayland.app/protocols/wlr-layer-shell-unstable-v1`)
stays `rejected` at tier C — it renders the protocol without a revision pin, so the pinned XML
(S460) remains the authoritative copy. Its `used-by` gains the round-78 entry, which cites the
rejection at `corpus/knowledge/bar-footprint-margins-r78.md:154`.

### What these seven license together (and what they do not)

Taken as one join, the three load-bearing rows compose the band the round models: S464 gives
`allocation + margin(unanchored edges of the band axis)`, S457 adds `exclusive + margin(anchored
edge)`, and S462 establishes that the host's own bar submits the first and Waybar's margin chain
feeds both. The composition is a **derivation from the two source rules**, not a reading of a
reserved-area value: S458/S459 report the result, and this round's cases are fixtures. Nothing
here licenses a static `monitor … addreserved` band, a scaled or transformed output, a dynamic
cross size, centring rounding, a negative margin, or which process set a zone.
