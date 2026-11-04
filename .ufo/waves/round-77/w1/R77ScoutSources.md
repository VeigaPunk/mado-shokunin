# R77ScoutSources — per-surface source reconnaissance (round 77)

Scope: the rules `tools/mado-barfoot.py` (`VERSION r77-v1`) models, checked line by line
against the pinned trees. Read-only.

Trees and revisions
- Hyprland `v0.56.2 @ efb5099` — `/fast/scratch/hyaku/mado-r77/l1-src/Hyprland`
- Waybar `tag 0.15.0` — `/fast/scratch/hyaku/mado-r77/l1-src/Waybar`
- gtk-layer-shell `0.10.1` — not pinned; source tarball `codeload.github.com/wmww/gtk-layer-shell`
  tag `v0.10.1`, matching the installed `/usr/lib/libgtk-layer-shell.so.0.10.1`. Cited below as
  `gls:`; every `gls:` anchor is upstream, not from the pinned trees.
- Host: `hyprctl monitors -j` → `DP-1 3440x1440 scale=1 reserved=[0,26,0,0]`; `hyprctl layers -j`
  → one surface, level `2`, namespace `waybar`, box `0,0,3440,26`. The live chain agrees with
  `tools/mado-barfoot.py` on the declared host config (`layer: top`, `position: top`,
  `height: 26`, no `width`, no `margin`, no `name`).

Method note (evidence class): no LSP server answers these C++ trees in this seat, so every anchor
below is a literal `grep -n` line citation, not a semantic reference. Treat cross-file links
(e.g. `desiredSize`) as traced-by-hand, not by definition lookup.

---

## 1. Anchor table

`claim` = the sentence the tool implements. Quotes are trimmed to <=25 words; `…` marks elision.

| # | claim | file:line | quote | licenses | does not license |
|---|---|---|---|---|---|
| A1 | four level slots exist, indexed 0–3 | `Hyprland/src/output/Monitor.hpp:195` | `std::array<std::vector<PHLLSREF>, 4> m_layerSurfaceLayers;` | the tool's four-entry `LEVEL` map shape | nothing about ordering — the array size alone does not fix which index is which |
| A2 | index order is background,bottom,top,overlay = 0,1,2,3 | `Hyprland/protocols/wlr-layer-shell-unstable-v1.xml:86-89` | `<entry name="background" value="0"/>` … `<entry name="overlay" value="3"/>` | `LEVEL = {"background":0,"bottom":1,"top":2,"overlay":3}` and the `level-top-swap` mutant's target | that waybar ever uses a level other than its configured `layer` (see F3) |
| A3 | a surface lands in the slot named by the client's `set_layer` | `Hyprland/src/desktop/view/LayerSurface.cpp:55` | `pMonitor->m_layerSurfaceLayers[resource->m_current.layer].emplace_back(pLS);` | that `layers[mon].levels["2"]` means *top* | that duplicates cannot occur — multiple surfaces may share one slot (tool raises `Unmodelled`, correct but a policy, not a source rule) |
| A4 | the JSON key is the array index | `Hyprland/src/debug/HyprCtl.cpp:660-661,690` | `int layerLevel = 0; for (auto const& level : mon->m_layerSurfaceLayers) {` … `layerLevel++;` | `find_layer`'s `levels[str(level)]` lookup | nothing about emptiness: all four keys are always emitted, empty arrays included |
| B1 | the box is sized from the client's requested size | `Hyprland/src/render/Renderer.cpp:2607` (`:87` in `LayerShell.cpp`) | `CBox box = {{}, PSTATE->desiredSize};` / `m_pending.desiredSize = {sc<int>(x), sc<int>(y)};` | `declared_box` starting from `height`/`width` | that `desiredSize` equals the *config* value (F2) |
| B2 | zero desired width spans with margins; both horizontal anchors centre without margins; a single anchor pins | `Hyprland/src/render/Renderer.cpp:2610-2619` | `if (box.width == 0) box.x = bounds.x; else if ((PSTATE->anchor & both_horiz) == both_horiz) box.x = bounds.x + ((bounds.width / 2) - (box.width / 2));` | `declared_box`'s three horizontal branches | the anchor values themselves — those come from waybar (H1/H2) |
| B3 | same three branches on the vertical axis | `Hyprland/src/render/Renderer.cpp:2622-2632` | `if (box.height == 0) box.y = bounds.y; else if ((PSTATE->anchor & both_vert) == both_vert) box.y = bounds.y + ((bounds.height / 2) - (box.height / 2));` | `declared_box`'s vertical branches | reachability for a horizontal bar (F2) |
| B4 | margins apply only on axes that are not double-anchored | `Hyprland/src/render/Renderer.cpp:2635-2653` | `if (box.width == 0) { box.x += margin.left; box.width = bounds.width - (margin.left + margin.right); }` … `else if ((anchor & both_horiz) == both_horiz) ; // don't apply margins` | `parse_margins` + `declared_box` composing as the tool does | that margins also move the *reserved band* (see I2) |
| C1 | non-positive exclusive zones do not reserve | `Hyprland/src/render/Renderer.cpp:2531` | `if (exclusive <= 0) { return; }` | `exclusive: false` → `reserved=NOT_APPLIED` | — |
| C2 | the edge is chosen by singular anchor, or by the anchor triplet, and the margin is added | `Hyprland/src/render/Renderer.cpp:2575` | `if ((exclusiveEdge == edges[i].singular_anchor \|\| anchor == edges[i].singular_anchor \|\| anchor == edges[i].anchor_triplet) && exclusive + edges[i].margin > 0)` | `edge_extent`'s per-side band and the `exclusive + margin` arithmetic | that the client's `exclusive` already contains a margin (I2) |
| C3 | edge table order is top, bottom, left, right, each with its own singular + triplet | `Hyprland/src/render/Renderer.cpp:2540-2583` | `.singular_anchor = ZWLR_LAYER_SURFACE_V1_ANCHOR_TOP, .anchor_triplet = LEFT \| RIGHT \| TOP, .margin = marginTop` | that a top bar's triplet (LEFT\|RIGHT\|TOP = 13) selects the top edge | the first-match `break` — ambiguous anchor sets resolve to whichever edge comes first (tool never constructs one) |
| D1 | the LS contribution is recomputed from scratch each arrange | `Hyprland/src/render/Renderer.cpp:2680` | `PMONITOR->m_reservedArea.resetType(Desktop::RESERVED_DYNAMIC_TYPE_LS);` | that `reserved` is a snapshot of the current tree, not a monotone accumulator | that the whole band is dynamic — static monitor reserve survives (F5) |
| D2 | the band is the delta between the pre-arrange usable box and the post-arrange one | `Hyprland/src/render/Renderer.cpp:2682,2696` (`ReservedArea.cpp:33-34,53-59`) | `const CBox ORIGINAL_USABLE_AREA = PMONITOR->logicalBoxMinusReserved();` … `addType(RESERVED_DYNAMIC_TYPE_LS, CReservedArea{ORIGINAL_USABLE_AREA, usableArea});` | `band == extent` for one bar with zero margins; `band > extent` → `GT` | that `ORIGINAL_USABLE_AREA` starts at the monitor origin (F5) |
| D3 | `reserved` is static + dynamic, clamped at 0 per side | `Hyprland/src/desktop/reserved/ReservedArea.cpp:43-51,104-112` | `m_bottomRight += e.bottomRight; m_topLeft += e.topLeft;` / `ref.topLeft = ref.topLeft.clamp({0, 0});` | `band` being a small non-negative int | that a negative margin can pull the band inside the extent (clamp hides it; the tool says NOT_MODELLED anyway) |
| E1 | the `layers` reply carries exactly the fields the tool reads | `Hyprland/src/debug/HyprCtl.cpp:671-682` | `"x": {}, "y": {}, "w": {}, "h": {}, "alpha": {}, "namespace": "{}", "pid": {}` | `find_layer` + the live-box comparison | that the reply exposes the exclusive zone — it does not, which is why the band must be inferred from `monitors` |
| E2 | `monitors[].reserved` is `[left, top, right, bottom]` | `Hyprland/src/debug/HyprCtl.cpp:253,281-282` | `"reserved": [{}, {}, {}, {}],` … `m_reservedArea.left(), …top(), …right(), …bottom()` | `RESERVED_INDEX` and the `reserved-wrong-edge` mutant's target | that the numbers are logical units (F1) |
| F1 | per-side margin keys win, absent sides are 0 | `Waybar/src/bar.cpp:178-184` | `if (config["margin-top"].isInt() \|\| … ) { margins_ = { … ? … .asInt() : 0,` | `parse_margins` branch 1 (including the zero-fill of absent sides) | that a non-int side is an error — it silently becomes 0 on both sides |
| F2 | CSS-string margins are 1/2/3/4 integer tokens, other counts ignored | `Waybar/src/bar.cpp:186-217` | `} else if (config["margin"].isString()) { std::istringstream iss(…); … std::stoi(margins[0], nullptr, 10);` | `parse_margins` branch 2 and the `margin 2` / `margin 3` selftests | that a 0-token or 5-token string keeps the previous value — it keeps the *initial* zeros (tool returns zeros too) |
| F3 | an integer `margin` fills all four sides | `Waybar/src/bar.cpp:218-221` | `} else if (config["margin"].isInt()) { auto gaps = config["margin"].asInt();` | `parse_margins` branch 3 | — |
| G1 | the requested size is the config size, defaulting to 0 | `Waybar/src/bar.cpp:175-176,240` | `height_ = config["height"].isUInt() ? config["height"].asUInt() : 0;` … `window.set_size_request(width_, height_);` | `as_uint` (UInt, bool and negatives rejected) | that 0 reaches the compositor as 0 (M1) |
| H1 | position clears exactly one anchor | `Waybar/src/bar.cpp:392-413` | `anchors.fill(TRUE); … default: /* Gtk::POS_TOP */ anchors[GTK_LAYER_SHELL_EDGE_BOTTOM] = FALSE;` | the tool's assumption that a top bar is anchored LEFT\|RIGHT\|TOP | — |
| H2 | a configured cross size > 1 clears the remaining pair | `Waybar/src/bar.cpp:414-425` | `} else if (orientation == Gtk::ORIENTATION_HORIZONTAL && configured_width > 1) { anchors[LEFT] = FALSE; anchors[RIGHT] = FALSE; }` | `declared_box`'s `width > 1` threshold — the `> 1` (not `> 0`) is waybar's, not Hyprland's | — |
| I1 | exclusive mode picks auto-zone, non-exclusive pins zone 0 | `Waybar/src/bar.cpp:357-361` | `if (mode.exclusive) { gtk_layer_auto_exclusive_zone_enable(gtk_window); } else { gtk_layer_set_exclusive_zone(gtk_window, 0); }` | `exclusive` being a boolean gate on reserve at all | that auto-zone equals the bar's extent (I2) |
| I2 | auto zone = allocation + the margins on *unanchored* edges | `gls:src/layer-surface.c:264-288` | `new_exclusive_zone = self->current_allocation.height; if (!anchors[TOP]) += margins[TOP]; if (!anchors[BOTTOM]) += margins[BOTTOM];` | `NOT_MODELLED` whenever any margin is non-zero — and it is *necessary*, see below | that the extra term is the *same* margin the compositor adds (it is the opposite one) |
| J1 | `name` is the layer namespace, default `waybar` | `Waybar/src/bar.cpp:232-233` | `gtk_layer_set_namespace(gtk_window, config["name"].isString() ? config["name"].asCString() : "waybar");` | `declared_bar`'s `namespace = config.get("name") or "waybar"` | the manual's account of `name` (F7) |
| K1 | exclusive reserve is level-agnostic | `Hyprland/src/render/Renderer.cpp:2690-2694` | `for (auto const& la : PMONITOR->m_layerSurfaceLayers) arrangeLayerArray(PMONITOR, la, true, &usableArea);` | `layer: bottom` + `exclusive: true` still reserving | that any frozen case exercises it — none does (all 15 declare `layer: top`) |
| K2 | waybar's shipped default is bottom + exclusive | `Waybar/src/bar.cpp:27-33` | `{"default", {.layer = bar_layer::BOTTOM, .exclusive = true, .passthrough = false, .visible = true}},` | the tool's defaults (`layer` → bottom, `exclusive` → true) | — |

**I2 in full.** For a top bar (`LEFT == RIGHT == TRUE`, `TOP == TRUE`, `BOTTOM == FALSE`), the
client sends `zone = allocation.height + margins[BOTTOM]`; Hyprland then computes
`band = zone + margins[TOP]` (`Renderer.cpp:2575`). The surface's own extent is
`margins[TOP] + allocation.height`. So `band - extent == margins[BOTTOM]`: a margin on the edge
*opposite* the bar inflates the band without moving the box. `css-margins` and `per-side-margin`
expect `box=MATCH, reserved=NOT_MODELLED` for exactly this reason, and the tool's
"any margin non-zero ⇒ NOT_MODELLED" is the only safe reading. The declaration's limit text
("the gtk-layer-shell auto exclusive-zone composition when the bar's edge margin is non-zero")
is correct but understates it: the trigger is any margin, not only the edge one.

---

## 2. Rules the source does not support as modelled

### F1 — `monitors[].width/height` are physical pixels; the tool treats them as the logical box
`HyprCtl.cpp:278` fills `"width"`/`"height"` from `sc<int>(m->m_pixelSize.x), …y`; Hyprland's
layout box is `m_size = (xfmd / m_scale).round()` (`Monitor.cpp:699-700`, `996`) and every
`m_geometry` in the `layers` reply is in that logical space. `parse_monitors` accepts
`width`/`height` and never reads the `scale` field sitting in the same object. On the host
(`scale=1`, all 15 fixtures `scale=1.0`) the two spaces coincide, so nothing fails today; on any
scaled output the declared box is over-sized by the scale factor and the tool reports a false
`box=DIFFER`. Confidence: high (both sides are literal source). Exposure: none of the 15 cases.

### F2 — the auto branch is evaluated on axes where it cannot fire
`gls:src/layer-surface.c:31-46` zeroes a requested dimension **only** when both anchors on that
axis are set. Waybar clears `BOTTOM` for a top bar (`bar.cpp:410-411`), so the surface always
sends a concrete height — the allocation, which is the module floor when `height` is absent
(`bar.cpp:639-649`). Hyprland's `box.height == 0` branch (`Renderer.cpp:2623,2645`) is therefore
unreachable for a horizontal waybar bar, and `LayerShell.cpp:57-66` would reject such a commit
outright ("y == 0 but anchor doesn't have top and bottom"). `declared_box` nonetheless evaluates
that branch and returns `h = mon_h - margins` for a height-less top bar, and `w = mon_w - margins`
for a width-less left/right bar.
- Not a case failure: `height: 0` occurs only in `left-vertical`, where height *is* the
  double-anchored axis, and `width: 0` occurs only in horizontal cases, where width is. The two
  reachable auto branches are modelled correctly.
- But it does contradict the declaration's own posture — "the tool refuses or names them, never
  guesses" (Named limits) — for the opposite-axis case. Confidence: high.

### F3 — `mode` presets are invisible to the model
`bar.cpp:326-345` resolves `config["mode"]` against `PRESET_MODES` and `setMode` then rewrites
layer and exclusive zone (`:346-361`); `setVisible` re-enters it (`:455-462`). A config with
`"mode": "hide"` is overlay + non-exclusive at runtime, while `declared_bar` reads the raw
`layer`/`exclusive` keys and predicts top + reserved. Not in the declaration's named limits.
Exposure: no case. Confidence: high.

### F4 — centring rounding
`declared_box` uses floor division (`(mon_w - w) // 2`), Hyprland centres in double and rounds
the box afterwards (`Renderer.cpp:2613`, `2660`). Odd deltas differ by 1 px. Every case's
delta is even (3440−800, 1080−30, …), so the boundary is unexercised. Confidence: medium-high
(the rounding mode of `CBox::round` lives in hyprutils, not in the pinned tree).

### F5 — static reserved (monitor rules) shifts the origin
`logicalBoxMinusReserved()` (`Monitor.cpp:1772-1774`, `Renderer.cpp:2682`) starts the usable box
inside any `monitor … addreserved` band, and `calculate()` keeps that static part in the reported
`reserved` (`ReservedArea.cpp:43-51`). The tool places the declared box at the monitor origin and
compares `band == extent`, so a host with a static top reserve yields `box=DIFFER` (false drift)
and `reserved=GT`. Not named in the declaration's limits. Host and fixtures: zero. Confidence: high.

### F6 — "declared size" is a request, not the realized size
`bar.cpp:630-652` warns when GTK allocates more than requested and then **stores the allocated
size**. A declared `height: 26` with taller modules produces a 30 px bar. This is the legitimate
`DIFFER` channel the tool's `drift-box` case represents; it is not a tool contradiction, but it
does mean `box=MATCH` is evidence about the *request*, never about whether the bar fits.

### F7 — the manual does not document the namespace effect
`waybar.5.scd.in:95-97` says only "Optional name added as a CSS class, for styling multiple
waybars." The namespace use is code-only (`bar.cpp:232-233`). The C1 declaration cites "the
installed waybar 0.15.0 manual (… `exclusive`)" as ground; the namespace rule is not in it.

### F8 — the `layers` reply carries no exclusive-zone field
`HyprCtl.cpp:671-682` emits address/x/y/w/h/alpha/namespace/pid only. So "did the bar reserve?"
cannot be answered from the layer entry; it must be inferred from the monitor band, which is what
the tool does. This is a structural constraint on the claim, not a defect — but it means the C1
join is really *three* observations (config → geometry → band), never config → zone.

---

## 3. Case coverage vs. the anchors

Frozen set (15): `layers` values `{top}` only; `positions` `{top, bottom, left}`; `widths`
`{0, 40, 800}`; `heights` `{0, 24, 26, 30}`; all monitors `scale=1.0`.

| anchor | exercised by | gap |
|---|---|---|
| A1–A4 level map | every case (level `2`) | `bottom`/`background`/`overlay` levels have no case; only the `level-top-swap` mutant touches the map |
| B2/B3 centred | `centred-width` (800) | no vertical centring case (would need a left bar with `height > 1`) |
| B4 margins | `css-margins`, `per-side-margin` | only as `NOT_MODELLED`; the margin *composition* is never scored |
| C1 | `exclusive-false` | — |
| C2 band arithmetic | `host-top`, `bottom-bar`, `left-vertical` | no non-zero-band-without-margin case beyond these three |
| D2/D3 | `drift-reserved`, `wrong-edge-band` | — |
| E1 | `malformed-layers`, `declared-level-miss` | — |
| E2 order | `wrong-edge-band` (the mutant `reserved-wrong-edge` is killed by it) | trust in the order rests on `HyprCtl.cpp:281-282`, not on a case |
| F1–F3 margins | `css-margins` (2-value), `per-side-margin` (per-side) | no 3-value and no 1-value string case (selftest covers them) |
| H2 threshold | `centred-width` (width 800 > 1), all auto cases (width 0) | `width: 1` is the crack between waybar's `> 1` and Hyprland's `== 0`; unreachable in practice because gtk zeroes the request whenever both anchors are set (`gls:31-46`) |
| K1 bottom reserve | **none** | the claim "`layer: bottom` + `exclusive: true` still reserves" is source-licensed (K1/K2) and case-unexercised |

---

## 4. Answers to the two pointed questions

1. **Does `name` change the namespace?** Yes — `bar.cpp:232-233`; `name` is the layer namespace
   string and `waybar` is the fallback. It also stays a CSS class (`:150`). The manual mentions
   only the CSS class (F7).
2. **Does `layer: bottom` with `exclusive: true` still reserve?** Yes — `arrangeLayersForMonitor`
   runs the exclusive pass over all four level arrays with no level filter (`Renderer.cpp:2690-2694`),
   and waybar's own default preset is bottom + exclusive (`bar.cpp:27-33`). The level only decides
   stacking; the reserve comes from the client's exclusive zone.

---

## 5. Remaining unknowns

- `CBox::round`'s exact tie-breaking (hyprutils, not in the pinned tree) — affects F4 only.
- Whether gtk-layer-shell 0.10.1's allocation for an unset cross size is exactly waybar's module
  floor on the host (the `MIN_HEIGHT` path is host-dependent; not exercised here).
- The `edges[]` first-match `break` under anchor sets that fit two triplets (e.g. all four
  anchors) — Hyprland would pick top; no waybar configuration produces it (H1 clears one edge).
