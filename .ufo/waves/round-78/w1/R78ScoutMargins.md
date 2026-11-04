# R78ScoutMargins — source reconnaissance for the C1 margined auto exclusive-zone model

Round 78 · seat R78ScoutMargins · read-only · 2026-11-04
Base revision `f597eccbffefd5fd6bbb01f3511c88bbeaed493c`; measured revision `44a36b64`; model under
attack `tools/mado-barfoot.py` r78-v1, sha256 `aac5d41b923711e174c6d62bb24da5a2b53abf7c938bfc5b68816929a12009c0`
(verified in place). Host: Hyprland `0.56.2-4`, waybar `0.15.0-3`, gtk-layer-shell `0.10.1-1`,
hyprutils `0.14.2-1`; `hyprctl version` reports commit `efb50993780079460b0cbed1363e2166a2de1d9f` — the
pinned compositor commit, so the fetched source is the running binary's source, not a neighbour release.

Everything below is source-derived unless a line says **[OBS]** (an executed command and its output).
No compositor state was mutated; the only host writes are the read-only `hyprctl monitors -j` /
`hyprctl layers -j` captures.

---

## 1. What I opened, and that the bytes are the pinned bytes

Fresh fetches into `.ufo/waves/round-78/fetch/`; manifest `fetch/sha256-r78-scout-margins.txt`.
The six round-77 pins reproduce **byte-for-byte** (same sha256 as `round-77/fetch/sha256-r77.txt`), so
the r77 quotes and the r78 model are read off the same bytes:

| id | file | sha256 (r78 fetch = r77) | lines read |
|---|---|---|---|
| S457 | Hyprland `src/render/Renderer.cpp` @ efb5099 | `9af8a74e…` | `applyExclusive` 2529-2585; `arrangeLayerArray` 2587-2671; `arrangeLayersForMonitor` 2673-2697 |
| S458 | Hyprland `src/debug/HyprCtl.cpp` @ efb5099 | `798b7c6c…` | reserved template 253; reserved print 281-282; `layersRequest` 647-700 |
| S459 | Hyprland `src/desktop/reserved/ReservedArea.cpp` @ efb5099 | `0a52e145…` | parent/child ctor 19-35; `apply`/`applyip` 53-68; accessors 76-92 |
| S460 | `wlr-layer-shell-unstable-v1.xml` @ efb5099 | `87e0b9c8…` | layer enum 76-90; `set_exclusive_zone` 152-188; `set_margin` 190-199 |
| S462 | Waybar `src/bar.cpp` @ 90b209a (0.15.0) | `120eb913…` | margins 178-221; namespace/size 232-244; `setMode` 346-369; `setPosition` 392-431; `onConfigure` 630-653 |
| S464 | gtk-layer-shell `src/layer-surface.c` @ v0.10.1 | `deef9c81…` | auto zone 264-292; size-allocate 296-316; anchor setter 417-427 |

Supporting fetches (new this round, hashed in the same manifest):

| file | why |
|---|---|
| S465 Hyprland `src/desktop/DesktopTypes.hpp` | showed `CBox` is **not** defined there |
| S466 Hyprland `src/helpers/math/Math.hpp` | `using namespace Hyprutils::Math;` — `CBox` comes from hyprutils |
| S467 Hyprland `CMakeLists.txt` | `HYPRUTILS_MINIMUM_VERSION 0.14.0` (:150) |
| S468/S469 hyprutils `v0.14.0` `math/Box.hpp`, `math/Box.cpp` | `CBox::round()` = `std::round` (:51-59) |
| S469-v0142 hyprutils `v0.14.2` `math/Box.cpp` | **byte-identical** to v0.14.0 (host has 0.14.2-1) |
| S470 hyprutils `math/Vector2D.cpp` | `Vector2D::round()` = `std::round` (:23-25) |
| S471-S475 Waybar `factory.cpp`, `main.cpp`, `client.cpp`, `config.cpp`, `bar.hpp` | where `output` is actually matched |
| S476 Hyprland `src/desktop/view/LayerSurface.cpp` | `exclusiveEdge` is never assigned there |
| S477 Hyprland `src/protocols/LayerShell.cpp` | same |
| S478 Hyprland `src/output/Monitor.hpp` | `m_layerSurfaceLayers` is `std::array<…,4>` (:195) |

---

## 2. The two rules, as written

**Client (gtk-layer-shell 0.10.1, `layer_surface_update_auto_exclusive_zone`, S464:264-292).**
`horiz = (anchors[LEFT] == anchors[RIGHT])`, `vert = (anchors[TOP] == anchors[BOTTOM])`
(:269-272). Exactly one of `horiz`/`vert` is true for any waybar bar (§3), so:

* horizontal bar → `zone = current_allocation.height` (:276) `+ margins[TOP] if !anchors[TOP]` (:277-278)
  `+ margins[BOTTOM] if !anchors[BOTTOM]` (:279-280);
* vertical bar → `zone = current_allocation.width` (:282) `+ margins[LEFT] if !anchors[LEFT]` (:283-284)
  `+ margins[RIGHT] if !anchors[RIGHT]` (:285-286);
* a negative computed zone is never sent (`new_exclusive_zone >= 0`, :289).

`current_allocation` is the **GTK allocation**, assigned from the size-allocate rectangle
(:303-307) and re-triggering the zone (:313). It is not the declared `height`/`width`.

**Compositor (Hyprland 0.56.2, `applyExclusive`, S457:2529-2585).** For the first matching edge of
`{top, bottom, left, right}` where
`exclusiveEdge == singular || anchor == singular || anchor == triplet` **and** `exclusive + margin > 0`
(:2575): the anchored edge's margin is added to the zone, `y += zone + marginTop` / `height -= …`
(:2577, :2580) or the transposed pair, then `break` (:2583). The margin used is *that edge's* margin.

**Band (S457:2682-2683, :2691, :2696 + S459:19-35).** `usableArea` starts at
`logicalBoxMinusReserved()` (already minus the static reserve), each exclusive surface is arranged
against it (`bounds = *usableArea`, :2603) and shrinks it, and the reported dynamic band is the
parent-minus-child delta `CReservedArea{ORIGINAL_USABLE_AREA, usableArea}`. `hyprctl monitors -j`
prints `left, top, right, bottom` (S458:281-282). The reply is the **sum** of static + dynamic.

**Protocol contract (S460).** A positive zone is meaningful only for one edge or an edge plus both
perpendicular edges (:159-163); 0 = "move me out of the way", -1 = "stretch under" (:168-174);
"**The exclusive zone includes the margin.**" (:196). Layer values are background 0 / bottom 1 /
top 2 / overlay 3 (:87-90).

---

## 3. Anchor table — every reachable waybar declaration

Waybar's anchor set is `all TRUE` then one band-axis edge cleared by position (S462:400-413) and,
when the **cross** size is explicitly > 1, both cross edges cleared (:419-425). Consequences that
matter for the model: `horiz` is true exactly for top/bottom bars and `vert` exactly for left/right
bars, *independently* of the explicit-size clearing, because the clearing is always on the other
axis. So the auto-zone branch is selected by `position` alone.

`h`/`w` below are the allocation; margins are `top,right,bottom,left`. Observed tool lines are in
`w1/R78ScoutMargins/evidence.txt` (A-rows).

| # | declaration | anchors sent | client auto zone | compositor adds | band | tool (observed) |
|---|---|---|---|---|---|---|
| A1 | top, auto width, no margin (**host**) | L,R,T | `h` | `marginTop=0` | `h` | CLEAN 26/26 |
| A2 | top, auto width, `margin: 4` | L,R,T | `h+4` | `+4` | `h+8` = 38 | CLEAN 38/38 |
| A3 | top, `margin: "4 8"` (t4 r8 b4 l8) | L,R,T | `h+4` | `+4` | 38 (cross 8 never enters) | CLEAN 38/38 |
| A4 | top, `margin-top:10, margin-bottom:2` | L,R,T | `h+2` | `+10` | 42 | CLEAN 42/42 |
| A5 | bottom, `margin: 8` | L,R,B | `h+8` (`!TOP`) | `marginBottom=8` | 46 | CLEAN 46/46 |
| A6 | left, auto height, `margin: 6` | L,T,B | `w+6` (`!RIGHT`) | `marginLeft=6` | 52 | CLEAN 52/52 |
| A6b | left, `height: 1000`, `margin: 6` | L | `w+6` | `+6` | 52 | CLEAN 52/52 |
| A7 | right, auto height, `margin: 5` | R,T,B | `w+5` (`!LEFT`) | `marginRight=5` | 46 | CLEAN 46/46 |
| A7b | right, `height: 1000`, `margin: 5` | R | `w+5` | `+5` | 46 | CLEAN 46/46 |
| A8 | right, `width: 40`, no margin | R,T,B | `w` | `0` | 40 | CLEAN 40/40 |
| A9 | `layer: bottom`, top, `height: 28` | L,R,T | `h` | `0` | 28 | CLEAN 28/28 (level 1) |
| A14 | `layer: overlay`, `margin: 4` | L,R,T | `h+4` | `+4` | 34 | CLEAN 34/34 (level 3) |
| A12 | top, `width: 800`, `margin: 4` | T | `h+4` | `+4` | 34; box centred, cross margins dropped (:2613, :2639) | CLEAN 34/34 |
| A10 | `output: "!M2"` on M1 | L,R,T | as A1 | | 24 | CLEAN 24/24 |
| A11 | `output: "!M1"` on M1 | — | — | — | none | NO_BAR rc 3 |
| A13 | `exclusive: false` | L,R,T | zone 0 (`gtk_layer_set_exclusive_zone(0)`, S462:360) | none (`exclusive <= 0`, S457:2531) | 0 | CLEAN, `reserved=NOT_APPLIED` |

**The recorded formula is right for every row.** For a horizontal bar exactly one band-axis edge is
anchored, so the client adds exactly the *unanchored* edge's margin and the compositor adds exactly
the *anchored* edge's margin: `zone + anchored = h + opposite + anchored = h + top + bottom`. The
transposed argument gives `w + left + right`. `OPPOSITE_EDGE` (tool :69) is the correct pairing for
all four positions. `layer` changes only which array the surface is arranged in (S478:195, four
arrays; loops S457:2690-2694 in index order), never the arithmetic — a bottom-layer bar reserves
before a top-layer one. `exclusiveEdge` is never written anywhere in the fetched tree (only read at
S457:2575 and :2664), so for waybar surfaces the `anchor` branch is the only live path.

---

## 4. Where the tool diverges from the sources — discriminating fixtures

All fixtures were run with
`python3 -I tools/mado-barfoot.py --config … --layers … --monitors …`; full transcripts in
`w1/R78ScoutMargins/evidence.txt`.

### F1 — `output` is not waybar's matcher; three wrong verdicts (highest severity)

Waybar matches `output` in `isValidOutput` (S474:178-212), and the **array and string forms have
different semantics**:

* array (:179-198): iterate entries; `!x` returns false on a match and otherwise `continue`; `x`
  returns true on a match; an entry starting with `*` returns true; **after the loop, return false**.
* string (:201-208): `!x` → exclude; `x` → include; **an empty string falls through to `return true`**
  (:211), i.e. "every output".
* both compare against the monitor **name or the xdg-output identifier** (:184, :190, :205, :207);
  waybar derives the identifier from the monitor description (`client.cpp:110-113`).

The tool (tool :210-235) flattens this into "include list minus exclude list", which is wrong in three
reachable ways:

| fixture | waybar 0.15.0 | tool **[OBS]** |
|---|---|---|
| `"output": ["!M2"]` on M1 | no bar on **any** output (array branch falls through to false) | `verdict=CLEAN` rc 0 — **false CLEAN** |
| `"output": ["M1","!M1"]` on M1 | bar on M1 (first positive match short-circuits) | `verdict=NO_BAR` rc 3 — **false NO_BAR** |
| `"output": ""` | bar on every output | `verdict=NO_BAR` rc 3 — **false NO_BAR** |

Plus: a config listing the monitor **identifier** (which `hyprctl monitors -j` carries only inside
`description`) matches waybar and is reported `NO_BAR` by the tool — a verdict, not a refusal. The
tool refuses `*` (safe), but not these.

### F2 — centring rounding: silently mis-computed, not refused

Hyprland centres with doubles and rounds once: `box.x = bounds.x + (bounds.width/2 - box.width/2)`
(S457:2613 for both anchors, :2619 for neither), then `box.round()` (:2660) = `std::round` on x and
y, and `w = round(x + w - roundedX)` (hyprutils `Box.cpp:51-59`, identical in v0.14.0 and v0.14.2).
The tool uses floor division: `x = (mon_w - w) // 2` (:278), `y = (mon_h - h) // 2` (:292).

Discriminating fixture: 3440×1440 monitor, `width: 801`, `height: 26`, live box `x=1320`.
`std::round(1720 - 400.5) = 1320`; tool computes `1319`. **[OBS]** `box=DIFFER … verdict=DIFFER`
rc 1 on a physically correct capture — a false positive. Any odd cross size against an even monitor
dimension hits it (801/1201-wide bars, 1201-tall vertical bars). The declaration lists "centring
rounding" as *not covered*, but the tool does not refuse it: it emits a verdict.

### F3 — margin string parsing is not `std::stoi`

Waybar parses each CSS token with `std::stoi` (S462:190-214): a prefix parse that accepts `4px`,
`4.0`, `" 4"` as 4 and throws only on out-of-range. The tool uses `int(t, 10)` (:193), which raises
and then returns all-zero margins (:196). **[OBS]** with `margin: "4px 0"` (or `"4.0"`) waybar yields
`top=4, bottom=4` → zone 30, band 34; the tool prints `margins=0,0,0,0` and `expected=26`, then
`DIFFER` against the correct 34. Verified `std::stoi` behaviour with a compiled probe (`4px -> 4`,
`4.0 -> 4`, `99999999999 -> THROW`).

### F4 — an overflowing bar reserves nothing; the tool still expects a band

`CReservedArea(parent, child)` returns a **zero** area when the child is empty or not contained in the
parent (S459:20-31, `m_ok = false` at :29), and `arrangeLayerArray` only rejects `w<=0 || h<=0`
(S457:2655) — it happily subtracts a taller bar and leaves `usableArea.height` negative.
**[OBS]** 1920×100 monitor, `height: 120`: compositor reserves 0, tool prints `expected=120`,
`reserved=DIFFER` rc 1. Same for `margin-top: 80, height: 26` (`expected=106`, band 0). This is a
*model* error, not a capture error, and it is not in the declaration's named-limits list.

### F5 — a second exclusive consumer is tolerated, not composed; the frozen case encodes an order

`arrangeLayerArray` takes `bounds = *usableArea` (:2603) and `applyExclusive` mutates the shared
`usableArea` in the same loop (:2664, loop :2691), so a bar arranged **after** another exclusive
surface is placed against the already-shrunk area and its *box* moves. The frozen `second-consumer`
case keeps the bar at `y=4` with `reserved=60`, which is consistent only with the other consumer
being arranged *after* the bar (bar band 34, other 26, total 60). **[OBS]** the same layout with the
other consumer arranged first puts the bar at `y=30`; the tool then reports
`box=DIFFER reserved=GT verdict=DIFFER` rc 1. So `second-consumer` passes because `band > expected`
is accepted (`GT`, tool :414-417), not because the model composes two consumers.

### F6 — static `addreserved` is not refused, so it surfaces as a false DIFFER

`bounds` starts from `logicalBoxMinusReserved()` (S457:2682-2683), and the reported band mixes static
and dynamic (S458:281-282). **[OBS]** a static top reserve of 14 with a 26-px bar at `y=14` (band 40)
gives `box=DIFFER reserved=GT verdict=DIFFER` rc 1. The tool names the limit in its docstring but
still emits a verdict.

### F7 — the auto zone follows the allocation, the tool uses the declared height

`layer_surface_update_auto_exclusive_zone` reads `current_allocation` (S464:276, :303-307); waybar
itself warns when the requested height is below the module minimum and then **adopts the realised
size** (`height_ = ev->height`, S462:639-649). The tool's `declared_box` uses the config value, so a
bar whose modules force a taller allocation yields a `box=DIFFER` (detected, but attributed to
"drift") and an `expected` computed from the wrong height. Not reachable on the host bar (26 px, no
module overflow observed), but reachable on any bar whose CSS/font exceeds `height`.

---

## 5. What the model cannot cover, and why

1. **Negative margins** — refused (tool :253-254). Correct as a policy and consistent with the claim.
   Precision worth recording: only a negative **anchored-edge** margin can trip `exclusive + margin > 0`
   (S457:2575) and void the reservation; a negative **opposite-edge** margin yields a smaller but
   *valid* zone (26 + (-4) = 22, still ≥ 0 at S464:289) and a well-formed band of 22. The tool refuses
   both, so a legitimate negative-margin bar is unmodellable rather than mis-modelled. **[OBS]** D6 →
   `ERROR (stage=model …)`, rc 3.
2. **Scaled / transformed outputs** — refused (tool :371-374). The monitors reply carries pixel size
   while the layer box is logical; at scale ≠ 1 the two are different spaces. **[OBS]** B2/B3 → rc 3.
3. **Static `monitor … addreserved`** — the reply carries one `reserved` quadruple with no attribution,
   so the static and dynamic contributions cannot be separated from the capture. Not refused (F6).
4. **Dynamic cross size** — `height: 0` on a horizontal bar / `width: 0` on a vertical bar makes the
   realised allocation the module allocation; the declaration no longer predicts the box. Refused.
   **[OBS]** B4 → rc 3.
5. **Centring rounding** — `std::round` on a double centre vs integer floor division (F2). Not
   refused; the correct guard would be to refuse a centred box whose centre lands on `.5`, or to
   reproduce `std::round`.
6. **A second exclusive consumer** — the band is cumulative and the box depends on the arrangement
   order (F5); the tool can only say `GT`. It cannot attribute the extra band to a process.
7. **(not in the declaration) A bar that overflows the usable area** reserves nothing (F4) — the
   `CReservedArea` empty/containment short-circuit. Reachable with `height > monitor height` or a
   margin that pushes the box past the edge.

Also outside the model by construction, and correctly refused: list-valued configs (multiple bars),
`*` output patterns, a `mode` key (it rewrites layer and exclusive zone at runtime), a namespace
collision on one level, and the `background` layer (waybar never selects it — `from_json` only maps
bottom/top/overlay, S462:63-71).

---

## 6. Confidence and remaining unknowns

* **High confidence** in the two rules and the band formula: both functions read in full at the
  pinned commits, and the six pinned hashes reproduce the r77 bytes exactly; the running compositor
  reports the pinned commit. The host capture (3440×1440, scale 1, transform 0,
  `reserved [0,26,0,0]`, waybar at level 2, box `0,0,3440,26`) matches row A1 exactly, and the host
  config is `layer: top, position: top, height: 26` with no margin.
* **High confidence** in F1, F2, F3, F4, F6, F7 — each is a line-level reading plus an executed
  fixture whose output is quoted above.
* **Medium confidence** in the *severity* of F1: waybar's array-branch "no positive match ⇒ false" is
  read from the 0.15.0 commit `90b209a`; the host package is `0.15.0-3` and I did not disassemble the
  installed binary to confirm it was built from that commit.
* **Unresolved:** whether a *live* margined waybar behaves exactly as the source predicts. The host
  posture is read-only, so I did not restart waybar with a margined config; every client-side row is
  source-derived. The one live data point (A1) is margin-free.
* **Unresolved:** `hyprctl monitors -j` carries `description` (from which waybar derives the
  identifier) but no `identifier` field; the tool never reads `description`. Whether to model
  identifier matching is a design decision for the lane, not a source question.
* **Unresolved:** hyprutils on the host is `0.14.2-1`; I read `v0.14.0` and `v0.14.2` `Box.cpp` and
  they are byte-identical, so `CBox::round` is settled for both, but no other hyprutils function was
  audited.

## 7. Evidence

`w1/R78ScoutMargins/evidence.txt` — 30 fixture blocks (A1-A15, D1-D6, B1-B4, C1-C2), each with the
config, the monitors reply, the live layer entry, the exact tool output lines and the exit code.
`fetch/sha256-r78-scout-margins.txt` — sha256 for all 21 files this seat fetched.

Report: .ufo/waves/round-78/w1/R78ScoutMargins.md
