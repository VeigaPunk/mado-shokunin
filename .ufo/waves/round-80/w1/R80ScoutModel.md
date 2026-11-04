# R80ScoutModel — the C1 composition model: source recon against the frozen 33

Seat: scout (read-only, leaf). Round 80, wave 1. No repo write outside this seat directory, no
git/jj mutation, no host write, no instrument edit. Every "observed" row below is a command output;
every "source-derived" row is an arithmetic consequence of the cited code, not a compositor
observation.

## 0. State of the frozen instruments while this seat ran (observed)

```
c3eb5fbe…  tools/mado-barfoot.py                     (declared c3eb5fbe…, r80-v1)  selftest 111/111
6268667c…  quality/counters/c1-r80-multisurface.py   (declared 6268667c…)
462287fb…  quality/counters/c2-r80-runbook.py        (declared 462287fb…)
17c27157…  .ufo/waves/round-80/controls/c1-cases-r80.json   (declared 17c27157…, 33 cases)
f1dfb5f4…  .ufo/waves/round-80/controls/c2-runbook-cases-r80.json
```

All five match the declaration's prefixes; `python3 -I tools/mado-barfoot.py --selftest` →
`MADO_BARFOOT_SELFTEST: 111/111`. Lane HEAD at read time `a1d5f638…` (later than the freeze
`6c302a53…`; the tool blob is unchanged from the freeze). `fetch/S470.bin` `9af8a74e…`,
`S471.bin` `ad9314da…`, `S472.bin` `37988cca…` match `fetch/sha256-r80.txt`.

## 1. Source anchors (Hyprland 0.56.2, `fetch/S470.bin` = `src/render/Renderer.cpp`)

| Operation | Lines | What it fixes |
|---|---|---|
| `applyExclusive` signature | 2529-2530 | receives `anchor, exclusive, exclusiveEdge`, **all four margins** |
| early return | 2531-2532 | `exclusive <= 0` → nothing; `-1` and `-2` are indistinguishable here |
| edge table | 2533-2573 | top=`marginTop`/`&y`+`&height`, bottom=`marginBottom`/`height` only, left=`marginLeft`/`&x`+`&width`, right=`marginRight`/`width` only |
| match + guard | **2575** | `(exclusiveEdge == singular \|\| anchor == singular \|\| anchor == triplet) && exclusive + margin > 0`, tested **in table order**, `break` at 2582 only on a hit |
| axes | 2576-2581 | top: `y += a, h -= a`; bottom: `h -= a`; left: `x += a, w -= a`; right: `w -= a` (`a = zone + that edge's margin`) |
| `arrangeLayerArray` | 2587 | `full_area = {m_position, m_size}` (2588) — the full monitor box, **not** static-reduced |
| skip / pass filter | 2591, **2596** | `m_noProcess` skip; `exclusiveZone != (exclusive > 0)` → exclusive pass is `> 0`, everything else (`0`, `-1`, `-2`) is the second pass |
| bounds | **2599-2603** | `exclusive == -1` → `full_area`; **every other value** (including `0` and `-2`) → `*usableArea` |
| horizontal placement | 2604-2621 | `w==0`→LEFT; both L+R→centre **in doubles**; L; R; else centre |
| vertical placement | 2623-2634 | same shape on `top/bottom` |
| margins | **2635-2653** | `w==0`: `x += left; w = bounds.w - left - right` (margins applied even with both anchors); both-h: no margin; else L/R only |
| empty box | **2655-2658** | `box.w <= 0 \|\| box.h <= 0` → log + `continue` **before** `applyExclusive` → no zone |
| round | 2660 | `box.round()` (`hyprutils` `Box.cpp:51-63`: `std::round` on x/y, then `w = round(x+w-round(x))`) |
| order on the surface | 2662-2669 | geometry ← rounded box, then `applyExclusive`, then `configure(size)`, then `setBox` |
| `arrangeLayersForMonitor` | 2673 | |
| reset | **2680** | `resetType(RESERVED_DYNAMIC_TYPE_LS)` — the layer band is rebuilt each arrange |
| original usable | 2682-2683 | `ORIGINAL_USABLE_AREA = logicalBoxMinusReserved()`; `usableArea =` that |
| sort | 2686-2688 | per level, **in place**, `stable_sort` on `order()` **descending** |
| passes | **2690-2694** | every exclusive surface (level 0→3) first, then every non-exclusive one |
| one add | **2696** | `addType(LS, CReservedArea{ORIGINAL_USABLE_AREA, usableArea})` — the aggregate delta |

Supporting anchors: `ReservedArea.cpp` `S459.bin` :19-35 (parent/child ctor: `empty()` → zeros and
`m_ok` stays true; not-contained → error, `m_ok=false`, zeros), :43-51 (`calculate` re-adds every
dynamic type, no total clamp), :101-108 (`addType` clamps **per type** at 0);
`ReservedArea.hpp` `S459.hpp.bin` :7-11 (only `LS` and `ERROR_BAR` exist);
`LayerShell.cpp` `S471.bin` :100-102 (`exclusive` stored verbatim, any int), :156-169
(`set_exclusive_edge` accepts when `m_pending.anchor & anchor` is non-zero — intersection, not
containment; checked against the **pending** anchor); `tests/desktop/Reserved.cpp` `S472.bin` :23-30
(static + LS sum), :32-54 (delta formulas; empty/not-contained → zero);
`wlr-layer-shell` XML `S460.bin` :159-163 ("A positive value is only meaningful if the surface is
anchored to one edge or an edge and both perpendicular edges … otherwise treated the same as zero"),
:183 ("The default value is 0"), :393-405 (`set_exclusive_edge`, corner disambiguation);
gtk-layer-shell `S464.bin` :264-296 (`update_auto_exclusive_zone`: `horiz = LEFT==RIGHT`,
`vert = TOP==BOTTOM`, zone only when **exactly one** of them is true, from
`current_allocation` + the unanchored edges' margins).

## 2. Class table — what the frozen 33 do **not** pin

"Tool" = observed behaviour of `tools/mado-barfoot.py` r80-v1 on a synthetic fixture written under
this seat's scratch (fixture + full row set reproducible from `probe*.py`, §6). Tool line numbers are
`tools/mado-barfoot.py`.

| # | Model class | Source anchor | Tool behaviour (observed) | Frozen case? |
|---|---|---|---|---|
| 1 | monitor layout origin `x/y ≠ 0`, composition path | S470:2588, 2682 | **right** — `01b`: DECL=`LIVE` both surfaces, `band=74 expected=74 EQ CLEAN` with the monitor at `(1920,0)` | **no** — all 33 monitors omit `x`/`y` (scanned: only `(None,None)`) |
| 2 | static reserve on the **same** edge as the bar | S470:2682-2696, S459:43 | right, and pinned | **yes** — `static-composed` (static top 26 + bar band 34 = 60) |
| 3 | static on the same edge **plus a second exclusive surface** | S470:2690-2696 | **right** — `02`: `band=100 expected=100`, boxes `MATCH,MATCH` | no |
| 4 | `exclusive == -1` with a static reserve (bounds = full monitor) | S470:2600-2603 | **right** — `22b`: wall box `(800,700)` = full 1000×800 while the bar is at `(4,4)` inside the static-reduced box; `CLEAN` | no |
| 5 | `exclusive == 0` (protocol default) vs `-1` vs `-2` bounds | S470:2596-2603 | **right** — `06` zone 0 → box `y=26` (usable); `07` zone −2 → also usable, no reserve | `-1` only (`overlay-unexclusive-full`, `full-box-vs-usable`); `0`/`-2` no |
| 6 | a zone-0 surface at a **lower** level than an exclusive one (pass split) | S470:2690-2694 | **right** — `12`: level-0 `bg` placed at `y=700` against the post-bar box; `CLEAN` | no (`bottom-level-first` has the lower surface exclusive) |
| 7 | an **exclusive** surface whose box is empty | S470:2655-2658 | **right** — `05`: `SKIP … box=900,363,-800,100 reason=empty`, no reserve, `band=26 EQ CLEAN` | no (`empty-box-skip`'s surface has zone 0) |
| 8 | a band that **exactly** consumes the axis (`usable.h == 0`) | S459:20-21 `empty()` | numbers right — `18`: `band=0 expected=0 EQ CLEAN`, `ls=INVALID`; but `attributed=800` is printed next to a 0 band | no (`ls-area-invalid` is a negative box) |
| 9 | all-four anchors **with** an `exclusiveEdge` (protocol says "treated as zero") | S470:2575; S460:159-163 | follows the **implementation**, not the protocol text: `08` → `ATTR edge=top contribution=30`, `band=56 EQ`, box `(400,363)` | no |
| 10 | all-four anchors **without** an edge | S470:2575 | **right** — `09`: `ATTR edge=none contribution=0`, `band=26 EQ` | no |
| 11 | triplet anchor + a conflicting `exclusiveEdge` | S470:2575 (table order) | **right** — `11`: `exclusiveEdge=left` is ignored, `ATTR edge=top` | no |
| 12 | corner anchor + `exclusiveEdge` on the **other** corner edge | S470:2575, S471:162 | **right** — `10`: `anchor=[top,left] edge=left` → `ATTR edge=left contribution=30`, left band 30, `CLEAN` | corner+**top** only (`exclusive-edge-matched`); no case exercises a **left/right** attribution |
| 13 | any explicit **left/right** attribution in the composition path | S470:2544-2573 | **right** — `24b`: `dock` left 50, bar top 34, `gt=50,34,0,0 attr=50,34,0,0 EQ CLEAN` | **no** — all 10 composition extras land on `top`, or `none`, or `-1` |
| 14 | a **non-top** bar in the composition path | S470:2610-2651 | **right** — `16b`: left bar box `(0,0,40,800)`, zone 40, `ATTR edge=left` | **no** — all 10 composition cases declare a top bar |
| 15 | zone + **negative** anchored margin with a positive sum | S470:2575, 2645-2653 | **right** — `20`: `zone 30 margin-top -10` → box `y=16`, `contribution=20`, `band=46 EQ` | no (`negative-margin-skip` is the sum ≤ 0 branch) |
| 16 | a surface box **wider/taller** than its bounds | S470:2610-2621, S469:51-63 | **wrong by 1** at an odd overflow past a negative tie — see §3.1 | no |
| 17 | `auto` zone on a surface whose band size is **dynamic (0)** | S464:276-286 (allocation), S470:2575 | **wrong** — zone is taken from the declared `0`, not the allocated band; no `ATTR` row is printed, `expected` is short by the whole band, and a *later* surface gets the wrong box — §3.2 | no — `empty-box-skip` is the same shape but is skipped before `applyExclusive`, so the set cannot see its zone |
| 18 | `auto` zone on a **corner / parallel / all-four** anchor pair | S464:269-288 (`horiz`/`vert` gating) | **wrong** — gtk sends **no** zone there; the tool prints `size + margin[opposite]`; with an edge the band moves — §3.3 | no (corner cases use explicit zones) |
| 19 | an extra declared **without** `exclusive` | S460:183 (protocol default 0), tool:579 | **wrong for plain clients** — defaults to auto (`zone=size`), so `expected=66` vs a correct host's 26 → `DIFFER` — §3.4 | no — every auto extra in the set was authored so auto equals the fixture's band |
| 20 | an extra declared **without** `anchor` | S471:5 (`anchor=0`), tool:571-573 | guesses the position **triplet** (`30`: reserves as if anchored top-left-right) | no |
| 21 | same-level **ties**: declaration order vs reply array order | S470:2686-2688, S458:661-685 | the arrangement order comes from the **declaration index**; the reply's array order is the post-`stable_sort` order — §3.5 | no (`same-level-order` gives one surface `order: 10`) |
| 22 | two surfaces of **one namespace on one level** | S458:664 (reply lists both), tool:836-848 | **refused** — `04`: `ERROR (stage=model more than one 'panel' layer on monitor M1 level 3)`, rc 3 | no (safe) |
| 23 | a band on an edge **no declared surface touches** | tool:774-782 | `13b`: `gt=10,66,0,0 attr=0,66,0,0` → **`EQ CLEAN`, rc 0**; the phantom left band is visible only inside the two vectors | no |
| 24 | a declared surface whose live entry is the default `0,0,0,0` | S470:2591 (`m_noProcess`), S458:679 | `25`: `boxes=MATCH,DIFFER`, rc 1 — a skipped/unmapped surface reads as a box mismatch. Reachability of such a reply entry is [INFERENCE] (`m_noProcess` is only *read* at 2591; its writer is not in the fetched bytes) | no |
| 25 | a **second dynamic reserved type** (`ERROR_BAR`) | S459.hpp:7-11, S459:43-51,101-108 | unattributable: any extra band lands as `GT`, and `GT` is admitted as `CLEAN` (tool:775-796) | no (R79 §5 named the same hole for the static path) |
| 26 | a **protocol-invalid** declaration (dynamic band + singleton anchor) | S471:57-64 (`commit` errors) | modelled, not refused — `28`: box `w=1000`, `CLEAN`; unreachable in practice | no |
| 27 | `preview_scale` | **no such symbol** in S470, S471, S472, S458, S460, S462, S464, S465 | not applicable; the only scale inputs are `monitor.scale`/`transform`, which the join **refuses** when ≠ 1/0 (tool:666-672, and 868-874 on the legacy path) | n/a |

## 3. Defects (reachable declarations where the recorded composition is wrong)

Fixtures were written under `/fast/scratch/hyaku/mado-r80/R80ScoutModel/probe*/<label>/`; each is a
`--config/--layers/--monitors/--surfaces` quadruple run from the lane root. Scratch is removed at
close (§6), so the rows are quoted in full here.

### 3.1 Odd overflow past a negative tie: the centring formula is not `CBox::round`

Declaration: 1000×800, top bar 26, panel `anchor=[left,right] width=1001 height=100 exclusive=0`
(one pixel wider than the monitor — legal: an explicit size with both anchors).

```
DECL:   monitor=M1 level=3 ns=panel box=0,363,1001,100 anchor=left+right zone=0
LIVE:   monitor=M1 level=3 ns=panel box=-1,363,1002,100 entries=1
RESULT: monitor=M1 box=MATCH boxes=MATCH,DIFFER reserved=EQ band=26 expected=26 ... verdict=DIFFER
rc=1
```

Source-derived: `x = bounds.x + (bounds.w/2 - w/2) = 0 + (500 - 500.5) = -0.5`; `box.round()`
(`S469:51-63`) does `std::round(-0.5) = -1`, then `newW = -0.5 + 1001 - (-1) = 1001.5`,
`std::round = 1002`. The tool's `(bounds.w - w + 1)//2` (tool:503,509) is floor division on the
**offset**: `(1000-1001+1)//2 = 0`, and it never recomputes `w`. So a host that matches the source
reads `DIFFER`, rc 1.
The tie only diverges when the *absolute* coordinate at the half is negative: `d = -1` with
`bounds.x = 0` gives tool 0, source −1. `03b` is the same 1-pixel overflow on the vertical axis,
where `bounds.y = 26`: the source computes `26 + (387 − 387.5) = 25.5`, `std::round` → 26, and
`newH = 25.5 + 775 − 26 = 774.5` → 775 — exactly the tool's `box=300,26,400,775`; my `03b`
fixture's `LIVE` row was a bad hand-guess and is discarded. So the class needs the tie to fall on a
negative absolute coordinate (a monitor at the layout origin with the box overflowing past its
left/top edge) and is otherwise exact; `d` even, `d > 0`, or `w = bounds.w` all agree. Not covered:
every frozen box fits its bounds; the only oversize shape in the set is the *dynamic* empty-box
skip, a different branch.

### 3.2 `auto` on a dynamic band: the zone is not the allocation

Declaration: 1000×800, top bar 26 (zone 26), panel `height=0 margins={top:100} exclusive="auto"`
(the `empty-box-skip` shape with a margin that leaves a positive box).

```
DECL:   monitor=M1 level=3 ns=panel box=0,126,1000,674 anchor=top+left+right zone=0
LIVE:   monitor=M1 level=3 ns=panel box=0,126,1000,674 entries=1
RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=DIFFER band=0 expected=26 ... verdict=DIFFER
rc=1
```

Source-derived: the panel's own box is `h = 774-100 = 674` (it never depends on its own zone), so
gtk-layer-shell's `current_allocation.height` is 674 and its auto zone is `674 + margin.bottom(0) =
674` (`S464:276-280`). `applyExclusive` then takes `674 + margin.top(100) = 774` off the top
(`S470:2575-2578`), leaving `usable = {0,800,1000,0}`; `CReservedArea{{0,26,1000,774},
{0,800,1000,0}}` hits `child.empty()` (`S459:20-21`, `h == 0`) and returns **zeros**, so the
monitor reserves nothing and the reply's band is 0. The tool's `surface_zone` (tool:541-548) sees
`height == 0` and returns `0 + margin[opposite] = 0`, so it prints no `ATTR` row at all
(`if zone > 0`, tool:750) and keeps `expected = 26`.

The defect propagates: a surface arranged **after** the panel gets its box from the emptied usable
box.

```
DECL:   monitor=M1 level=3 ns=note box=0,26,200,100 anchor=top+left zone=0
LIVE:   monitor=M1 level=3 ns=note box=0,800,200,100 entries=1
RESULT: boxes=MATCH,MATCH,DIFFER reserved=DIFFER band=0 expected=26 ... verdict=DIFFER
```

Same on the other axis (`16b`): a left bar `w=40`, panel `position=left width=0 margins={left:4}`
auto → the tool prints `zone=0`, `expected=40`, while the allocation is 956, the band empties the
width, and the reply's band is 0 → `DIFFER`.

Two sub-shapes matter for the record: (a) for a *lone* auto/dynamic surface the band always
collapses to zero, because `zone + margin[anchored] = bounds` exactly — so the tool's `DIFFER` is
deterministic, not occasional; (b) the frozen `empty-box-skip` case has exactly this declaration
shape and still passes — its `margin.top = 1000` empties the box, so `continue` at `S470:2655`
runs before `applyExclusive` and the zone is never used. The case pins the skip, not the zone.

### 3.3 `auto` on a corner anchor: gtk sends nothing

Declaration: top bar 26, panel `anchor=[top,right] width=200 height=100 exclusive="auto"
exclusiveEdge="top"`.

```
DECL:   monitor=M1 level=3 ns=panel box=800,26,200,100 anchor=top+right zone=100
ATTR:   monitor=M1 level=3 ns=panel edge=top contribution=100
RESULT: reserved=DIFFER band=26 expected=126 ... verdict=DIFFER
rc=1
```

Source-derived: `horiz = (LEFT==RIGHT) = false`, `vert = (TOP==BOTTOM) = false`, so neither branch
of `layer_surface_update_auto_exclusive_zone` runs, `new_exclusive_zone` stays −1 and **no**
`set_exclusive_zone` is sent (`S464:269-288`); the client's zone remains 0, `applyExclusive` returns
at `S470:2531`, and nothing is reserved. The tool applies the position-based formula
(`zone = height + margin[opposite]`) to any anchor set, so it attributes 100 and reads `DIFFER`.
For *parallel* / *all-four* anchors the same formula is also wrong but harmless: no rule matches at
`S470:2575`, so the net band is unchanged and only the printed `zone=` differs.

### 3.4 The declaration defaults are gtk-shaped, the protocol defaults are not

Declaration: top bar 26, panel declared as `{"namespace":"panel","level":3,"height":40}` — i.e. the
caller says nothing about the zone (a plain `zwlr_layer_surface_v1` client that never called
`set_exclusive_zone`).

```
DECL:   monitor=M1 level=3 ns=panel box=0,26,1000,40 anchor=top+left+right zone=40
RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=DIFFER band=26 expected=66 ... verdict=DIFFER
rc=1
```

Source-derived: the protocol's default zone is **0** (`S460:183`; `S471:5` resets it to 0), so the
band stays 26 and the host is correct. `parse_surfaces` defaults `exclusive` to `"auto"`
(tool:579), which is gtk auto, not the protocol default. The same holds for `anchor`
(tool:571-573): the protocol default is no anchor (`S471:5`), the tool assumes the position
triplet, so `30` reserves space for a surface the caller described as unanchored. The bar itself is
unaffected — its anchors and zone come from waybar's own rules (`declared_bar`) — so this is
strictly an *extras* default. Every auto extra in the frozen set was authored so auto equals the
fixture's band (`overlay-compose-top`, `bottom-level-first`, `full-box-vs-usable`), which is why
the set cannot see it.

### 3.5 Same-level ties are taken from the declaration, not from the reply

Two extras at level 3, both `order` defaulted to 0, reply shows `[a(y=26), b(y=56)]` (the
compositor's own post-`stable_sort` order, `S470:2686-2688` in place, `S458:656-676` prints it):

```
14b declaration [a, b]: boxes=MATCH,MATCH,MATCH reserved=EQ band=96 ... verdict=CLEAN rc=0
14c declaration [b, a]: boxes=MATCH,DIFFER,DIFFER reserved=EQ band=96 ... verdict=DIFFER rc=1
```

The same host reads CLEAN or DIFFER purely from the order the caller happened to list the surfaces
in. `evaluate_composition`'s sequence (tool:715-716) sorts by `(level, -order, declaration index)`;
the reply carries the tie order and is not consulted. For equal `order()` the reply's order *is*
the arrangement order (stable sort), so this is a model that ignores its own best evidence.

## 4. Where I contradict the round's own wording

- `corpus/knowledge/bar-footprint-composition-r80.md` §7.4 says "Cross-axis overflow with a valid
  area is unmodelled: a box wider than the bounds is arranged by the compositor but the join's
  centring arithmetic is integer-only." It **is** modelled — the join arranges it and prints a box —
  and the actual defect is narrower: `CBox::round`'s half-away-from-zero on a negative absolute
  coordinate (§3.1), which needs `w > bounds.w` by an **odd** amount **and** a box origin at (or
  near) 0. A box taller/wider than the bounds otherwise matches exactly (`03b`).
- §7.3 names "`preview_scale`". No such symbol exists in the fetched bytes (`S470`, `S471`, `S472`,
  `S458`, `S460`, `S462`, `S464`, `S465`; `grep -in preview` → nothing). The real scale class is
  `monitor.scale`/`transform`, which the join refuses — the entry should say so and drop the term.
- §7.3/§6 present `GT` as "an undeclared consumer … admissible" and `DIFFER` as "the model
  over-attributes". §3.2/§3.4 show `DIFFER` arising from a *model under-attribution* where the
  correct host reserves **less** than the model (an auto/dynamic surface, and a defaulted zone), so
  the `GT`/`DIFFER` reading is not a safe caller rule.

## 5. Remaining unknowns

- `m_noProcess`'s writer (`S470:2591` only reads it): the writer is in
  `src/desktop/view/LayerSurface.cpp`, not in `fetch/`. Row 24's reachability is [INFERENCE].
- `arrangeLayersForMonitor`'s trigger set for the commit path is likewise outside `fetch/`; row 21
  only needs the *in-place stable sort* and the reply's iteration order, both pinned.
- The `auto` model is pinned to gtk-layer-shell `S464`; a wlroots client that computes its own
  "auto" could send any positive value, which the declaration expresses explicitly and the tool
  then models exactly.
- Nothing here is a live compositor observation: all `LIVE` rows are fixtures. The host's own join
  (`receipts/live-join-r80.txt`) has one exclusive surface and cannot distinguish any row above.

## 6. Method, reproduction, housekeeping

- Probes (retained, so the critic can re-run them): `R80ScoutModel/probe/probe.py` `061ecd0a…`,
  `probe2.py` `e6ff064b…`, `probe3.py` `20254070…`, `probe4.py` `edb8c3e4…`, each invoking
  `python3 -I tools/mado-barfoot.py --config … --layers … --monitors … [--rules …] [--surfaces …]`
  from the lane root on fixtures it writes itself under `/fast/scratch/hyaku/mado-r80/R80ScoutModel/`
  (a re-run recreates that scratch and must be cleaned up). 21 + 10 + 6 + 2 fixtures; every row
  quoted above is verbatim stdout.
- `python3 -I tools/mado-barfoot.py --selftest` → `111/111` (also at the start of the seat).
- No tool installs, no pacman, no host write, no repo/jj write, no instrument edit. Scratch removed
  at close (`rm -rf /fast/scratch/hyaku/mado-r80/R80ScoutModel`, verified absent); the generated
  fixtures are not retained because every row needed is quoted in §3 and the four scripts above
  regenerate them.

STATUS: ok — nothing missing; the only non-observed item is `m_noProcess`'s writer (§5), which is
outside the fetched bytes and does not affect any defect above.
