# The layer-surface composition under the bar's reserved band (round 80)

source: S470, S471, S472, S473, S474; held S457, S459, S465, S466 (re-opened byte-identical this round)
verified-at: 6c302a53eb8f577e83fbcadc01e05a286778df8e (lanes tip at the round-80 freeze)
recheck: `python3 -I quality/counters/c1-r80-multisurface.py --repo . --rev REV --base-rev e10f7e9f528b13195a1cdde28a68a702af3045c4 --controls .ufo/waves/round-80/controls/c1-cases-r80.json --carried .ufo/waves/round-79/controls/c1-cases-r79.json --scratch-root DIR` — 33 frozen cases, 22 mutants, exit 0 on `TARGET_MET`

## 0. What this entry is, and what it is not

The round-78 entry (`bar-footprint-margins-r78.md`) modelled one exclusive layer surface; the
round-79 entry (`bar-footprint-reserve-r79.md`) composed the static `addreserved` reserve with it.
Both left the second *dynamic* consumer `NOT_MODELLED`. This entry states how Hyprland 0.56.2
arranges **any number** of declared layer surfaces against a shrinking usable box, which edge each
one's reserved band lands on, and why the compositor's `reserved` array is a total with no
attribution. Every proposition below is read from the host's own version at commit `efb5099…`
(`hyprctl version` → `Hyprland 0.56.2 … commit efb50993780079460b0cbed1363e2166a2de1d9f`) and
reproduced by the lane's join in `.ufo/waves/round-80/receipts/measurement-c1-r80.txt`.

It is a **model over captured bytes**, not a runtime probe: no layer surface is created, no
compositor verb is run, and nothing about a *particular* host consumer is claimed beyond the
captures named in a receipt.

## 1. The order: level first, then the declared rule order

`arrangeLayersForMonitor` walks `m_layerSurfaceLayers` — one vector per layer level, background
(0) to overlay (3) — twice (S470 :2690-2694). Before the walk it resets the layer dynamic type
(:2680) and snapshots `logicalBoxMinusReserved()` as `ORIGINAL_USABLE_AREA` (:2682); after it, it
adds one `CReservedArea{ORIGINAL_USABLE_AREA, usableArea}` (:2696). Within a level the vector is
sorted by the surface's rule `order()` descending (:2686-2688), so a higher `order` is arranged
first. The join models that order as a declared integer per surface (`order`, default 0) and sorts
`(level, -order, declaration index)` — the index only breaks ties the compositor would break by
container order.

## 2. Each surface's box is placed against the *running* usable box

`arrangeLayerArray` takes `bounds = *usableArea` for every surface whose `exclusive != -1`, and
`bounds = full_area` (the monitor's own box) only for `exclusive == -1` (S470 :2599-2603). The box
is then the desired size against `bounds`, with anchors choosing the side (both horizontal anchors
centre, one anchor pins, none centres), and margins applied only on an anchored side; a zero-size
axis spans the bounds less that axis's margins (:2605-2652). `box.round()` follows (:2653).

Because `applyExclusive` mutates `usableArea` in the same loop, the *next* surface — and any later
level — is placed inside the already-reduced box. Two consequences the frozen cases pin:

| Effect | Case | Observation |
|---|---|---|
| A later level starts below the earlier one | `overlay-compose-top` | bar `0,0,1000,26` then panel `0,26,1000,40`; reserve 66 |
| An earlier level moves the bar itself | `bottom-level-first` | panel at level 1 `0,0,1000,40`, bar at `0,40,1000,26`; reserve still 66 |
| A higher `order` wins inside one level | `same-level-order` | panel (order 10) `0,6,1000,30` then bar `0,36,1000,26` |
| `exclusive == -1` ignores the shrink | `overlay-unexclusive-full`, `full-box-vs-usable` | the panel lands at full-box `y=700`, not the shrunk `y=660` |

An **empty arranged box** is skipped before anything else: `if (box.width <= 0 || box.height <= 0)
{ log; continue; }` (S470 :2655-2658). A skipped surface contributes no zone and gets no live box
(`empty-box-skip`).

## 3. `applyExclusive`: four rules, first match, one guard

`applyExclusive` returns immediately when `exclusive <= 0` (:2532-2534) and then walks four rules in
the fixed order **top, bottom, left, right** (:2536-2573). A rule matches when

```c
if ((exclusiveEdge == edges[i].singular_anchor || anchor == edges[i].singular_anchor
     || anchor == edges[i].anchor_triplet) && exclusive + edges[i].margin > 0) {
```

(S470 :2575-2576) — that is: the declared exclusive edge is this edge, *or* the anchor is exactly
this edge, *or* the anchor is the three-edge triplet that contains it. The first match wins and
`break`s (:2583). Top and left move the positive axis (`usable.y`, `usable.x`) and shrink the size;
bottom and right only shrink it (:2577-2582). Two consequences that a "sum of sizes" model gets
wrong:

- **An unmatched mask reserves nothing at all.** A surface anchored `top|right` (two edges, not a
  triplet) matches no rule: not the top singular, not the top triplet (left|right|top), not any
  other. Its zone is positive and its box is real, yet the usable box is untouched
  (`anchor-unmatched`). Declaring `exclusiveEdge = top` — which the protocol accepts because the
  edge is inside the anchor (S471 :162-164) — makes the first rule match and the zone applies
  (`exclusive-edge-matched`).
- **The guard is on the sum, not the zone.** `exclusive + margin(edge) > 0` means a positive zone
  cancelled by a negative margin on the matched edge does nothing at all (`negative-margin-skip`:
  zone 12, margin top −12 → no shrink).

The margin that joins the zone is the **matched edge's** margin — the anchored edge's — not the
opposite edge's. gtk-layer-shell's auto zone already contains the unanchored edge's margin
(S464 :264-292), which is why the round-78 expression `extent + opposite margin` and this
expression `zone + anchored margin` agree for an auto-zone bar.

## 4. One total, no attribution

The compositor stores exactly one dynamic entry for the whole layer plane:
`resetType(RESERVED_DYNAMIC_TYPE_LS)` (:2680) then `addType(..., CReservedArea{ORIGINAL, usable})`
(:2696). `CReservedArea` keeps a static initial box plus an array of dynamic deltas
(`ReservedArea.cpp:11-15, 37-48, 88-99`, held S466) and `calculate()` sums them; the monitor reply
prints only the sum (`HyprCtl.cpp` `reserved`, held S458). **There is no per-surface band in any
reply.** Any per-surface number is a model prediction — which is exactly why the round's join
prints `MADO_BARFOOT_ATTR:` per surface and `attr=`/`gt=` vectors beside the total: ATTRIBUTED is
the join's model, GT is the compositor's reply, and the claim is that the two agree.

## 5. The area guard: an invalid area zeroes the *whole* layer reserve

`CReservedArea(const CBox& parent, const CBox& child)` (S466 / S459 :19-31, pinned by S472
`tests/desktop/Reserved.cpp:32-54`) returns with a zeroed area when either box is empty, and sets
`m_ok = false` with a zeroed area when the child is not contained in the parent. So a zone larger
than the axis does not make a huge band: it empties the usable box, the constructor bails, and the
monitor reserves **only the static reserve**. `ls-area-invalid` pins that shape: a 2000 zone on an
800-high monitor with a 26-high bar gives `band=0 expected=0 attributed=2026 ls=INVALID` — the
attribution the model computed is printed, and the GT it must match is zero.

## 6. What the join prints (and what a caller may read)

`tools/mado-barfoot.py` (`r80-v1`) with `--surfaces`:

| Line | Reads |
|---|---|
| `MADO_BARFOOT_DECL:` | per surface: level, namespace, the box the model arranged, the anchor set, the requested zone |
| `MADO_BARFOOT_LIVE:` | per surface: the box the captured `hyprctl layers -j` reply carries for that namespace+level |
| `MADO_BARFOOT_ATTR:` | per surface: the edge its zone landed on and the amount (`edge=none contribution=0` when no rule matched) |
| `MADO_BARFOOT_RESULT:` | `box=`, `boxes=` (one verdict per surface in arrangement order), `reserved=` (EQ/GT/DIFFER for the bar's edge), `band=`/`expected=`/`attributed=` for that edge, `gt=`/`attr=` as four-value vectors in the reply's left,top,right,bottom order, `ls=VALID|INVALID`, `verdict=` |

`GT` (band > expected) stays admissible: an undeclared consumer can reserve more than the model
accounts for, and the r78 `second-consumer` case keeps that honest. `DIFFER` (band < expected)
means the model over-attributes, which is a model error, not a host state.

## 7. Limits (named, not smoothed over)

1. **No host attribution.** A host with a second exclusive surface would let one compare the model's
   `attr=` against nothing — the compositor prints no per-surface band. Today's host has one
   exclusive surface (`waybar`) plus `wallpaper` at level 0; the live join with both declared
   (`.ufo/waves/round-80/receipts/live-join-r80.txt`) reads `boxes=MATCH,MATCH … attributed=26
   gt=0,26,0,0 CLEAN`, which exercises the composition path but not a second exclusive band.
2. **Rule `order()` is a declared integer.** The compositor sorts by the surface's rule
   (`m_ruleApplicator->order()`); the join cannot read it from the layers reply, so a caller must
   declare it. A wrong `order` changes the attribution, not the total.
3. **`preview_scale` and fractional scaling are unmodelled**; the join refuses a monitor whose
   `scale`/`transform` is not 1/0 and says so.
4. **Cross-axis overflow with a valid area is unmodelled**: a box wider than the bounds is arranged
   by the compositor but the join's centring arithmetic is integer-only.
5. **`exclusive == 0` versus `-1`** are modelled as "arrange against the final usable box" and
   "arrange against the full monitor box"; a client that changes its zone at runtime re-arranges,
   which the join cannot observe.
6. The static reserve path is unchanged from round 79 and keeps its own limits (`source =` refused,
   `desc:`/empty selector refused, one monitor rule per selector).

## 8. Recheck

Run the counting command in the provenance line against any revision that carries the r80
instrument. It re-derives all 33 expectations from the frozen set, kills the 22 named mutants, and
prints `verdict=TARGET_MET` only when the tool's own selftest is green. A model change that moves a
case, a mutant or a target is a new round, never an edit to this entry (CORPUS.md rule 2).

## 9. Limit addendum (append-only; written after the round-80 wave's live recon)

Three limits the round's own seats surfaced, recorded rather than smoothed:

1. **The empty declaration is refused, not treated as "no extras".** `--surfaces` with an empty list
   exits `stage=setup` (`the surfaces declaration is empty`); the no-extras case is the *omitted*
   flag, which selects the single-surface branch. A caller that wants to say "the bar is the only
   surface" must omit the flag. (Seat `R80ScoutLive` §3.)
2. **`hyprctl layers -j` carries neither an anchor nor an exclusive-zone field.** A declaration can
   be *pinned* only where the box moves with the field: on this host `wallpaper`'s observed
   `0,0,3440,1440` pins `exclusive: -1` (the `exclusive: 0` probe arranges it at `0,26,3440,1414`
   and reads `DIFFER`), while its anchor set cannot be recovered from the reply at all. (Seat
   `R80ScoutLive` §6.)
3. **`RESERVED_DYNAMIC_TYPE_ERROR_BAR` is not modelled.** The compositor's reserved area sums two
   dynamic types (`ReservedArea.hpp:5-8`); the join models only the layer-surface type, so a host
   running the debug error bar reserves more than the model accounts for and reads `GT` — which the
   verdict already treats as admissible (band > expected), never as agreement.

## 10. Anchor corrections (append-only; the wave's source seat re-read the pinned bytes)

Two registry anchors written earlier in this round were off, and CORPUS.md rule 2 makes the
correction a new row, never an in-place rewrite:

- **S476 supersedes S473.** The mask table is `:100-115`, **sixteen** `s/^N,/` rules (`^0,` strips
  the mask, then fifteen modifier sets through `^77,`), not "twelve" over `:100-120`. The number
  twelve is the count of *distinct rendered tuples this host's binds produce*, not the table's rule
  count — a distinction the entry's §6 grammar depends on, since the grammar validates the rendered
  words, not the mask arithmetic.
- **S477 supersedes S472.** The empty-box cases are `:39-52` (`c` at `:39`, `d` at `:46`), and the
  not-contained assertion at `:53-54` proves `ok() == false`; it does not read the zeroed area —
  that zeroing is the constructor's (`ReservedArea.cpp:20-31`, S459/S466). §5 above relies on the
  constructor, not on this test, for the zeroing.

The propositions in §§1–8 are unaffected: both corrections are about where a claim lives, not about
what the compositor does. The entry's `source:` line keeps the original ids for that reason, and
these two rows carry this path in `used-by`.
