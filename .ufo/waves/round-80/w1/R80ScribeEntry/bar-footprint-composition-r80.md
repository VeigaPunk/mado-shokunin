# The composition under the bar's band: N layer surfaces, one running usable box, one total

source: S470 Hyprland v0.56.2 `src/render/Renderer.cpp` @ efb5099 (`applyExclusive` :2529-2585; `arrangeLayerArray` :2587-2671; `arrangeLayersForMonitor` :2673-2702, `resetType` :2680, `ORIGINAL_USABLE_AREA` :2682, sort :2685-2688, passes :2690-2694, `addType` :2696; sha256 `9af8a74e7dc42ba3c5532303b9bb4ee7c350d4cef2f2c8984e41f2a01b3bdd22` — byte-identical to the held S457); S471 `src/protocols/LayerShell.cpp` @ efb5099 (`setSetExclusiveZone` :100-102, `setSetExclusiveEdge` :156-169, alignment error :162-164; sha256 `ad9314dafda63278aaaa4241e969544560f01fb00983d7754e35fae2567a8961`); S472 `tests/desktop/Reserved.cpp` @ efb5099 (parent/child :32-38, empty parent and empty child :40-52, not contained :53-54; sha256 `37988cca6d024a1481cc419c3bb06cf8c5929e91297514cda11475931a330402`); held and re-read: S457 `src/render/Renderer.cpp` @ efb5099 (sha256 `9af8a74e…`), S459 and S466 `src/desktop/reserved/ReservedArea.cpp` @ efb5099 (both sha256 `0a52e145…`: parent/child constructor :19-31 and :33-34, `calculate` :43-51, `apply` :53-60, `setStatic` :69-74, `addType` :101-112), S465 `src/output/Monitor.cpp` @ efb5099 (sha256 `9cf88e15…`: `m_reservedArea.setStatic` :654, `logicalBox` :1768-1770, `logicalBoxMinusReserved` :1772-1774).
verified-at: 2026-11-04 (UTC), round 80; the thirty-three cases are measured at `6c302a53eb8f577e83fbcadc01e05a286778df8e` with tool `r80-v1` (sha256 `c3eb5fbef794c92ba45adc85ed1dcd18c505a2776a3fb1db34742a6eed27fa99`, selftest 111/111), receipt `.ufo/waves/round-80/receipts/measurement-c1-r80.txt`; the do-nothing control at base `e10f7e9f528b13195a1cdde28a68a702af3045c4` is `receipts/control-c1-r80-at-base.txt`; the read-only host join is `receipts/live-join-r80.txt`.
recheck: on-release (Hyprland after v0.56.2); 180d otherwise — re-open S470/S471/S472, re-verify the pins with `sha256sum -c .ufo/waves/round-80/fetch/sha256-r80.txt`, then re-run `python3 -I quality/counters/c1-r80-multisurface.py --repo . --rev <tip> --base-rev e10f7e9f528b13195a1cdde28a68a702af3045c4 --controls .ufo/waves/round-80/controls/c1-cases-r80.json --carried .ufo/waves/round-79/controls/c1-cases-r79.json --scratch-root DIR` (33 cases, 22 mutants, exit 0 only on `TARGET_MET`), and re-capture `hyprctl monitors -j` / `hyprctl layers -j` for the live join.
Lane: mado-shokunin. Round: 80. Extends the `GT`-only limit of `bar-footprint-margins-r78.md` and the second-consumer limit of `bar-footprint-reserve-r79.md`; those bodies stay the record of their instruments.

## What this entry holds

| question | where the answer lives | state |
|---|---|---|
| Does a second layer surface compose under the bar, or overlap it? | it is arranged in level/order sequence against the running usable box: it can start inside the box the bar made, or move the bar's own box if it comes first (S470 :2685-2696) | OBS (source) |
| Which box is a surface arranged in? | the running usable box; the monitor's own full box only for `exclusive == -1` (S470 :2599-2603) | OBS (source) |
| Which edge does its zone land on? | the first matching rule of top, bottom, left, right (S470 :2534-2583) | OBS (source) |
| When does a positive zone land nowhere? | an anchor mask that is neither one edge nor one of the four triplets and no `exclusiveEdge`; a non-positive `zone + margin`; an empty arranged box (S470 :2575, :2655-2658) | OBS (source) |
| What does the monitor reserve for the whole plane? | one area: the static reserve plus the `ORIGINAL_USABLE_AREA → usableArea` delta; zero for the layer type when that delta is refused (S470 :2696; S466 :19-51) | OBS (source) |
| Can any reply name one surface's band? | no: one dynamic type, one summed `reserved` array (S470 :2696, S472 :26-30) | OBS (source) |
| Is the composition scored on a frozen set? | 33/33 cases, 22/22 mutants at `6c302a53` (receipt `measurement-c1-r80.txt`) | OBS (receipt) |
| What does the held round-79 model score on the same set? | 23/33; the ten composition cases exit 2 because `r79-v1` has no `--surfaces` (receipt `control-c1-r80-at-base.txt`) | OBS (receipt) |
| Does the host agree today? | one exclusive surface (`waybar`); a declared `exclusive: -1` wallpaper composes with it, both boxes match, `attributed=26 gt=0,26,0,0` (receipt `live-join-r80.txt`) | OBS (host, read-only) |

## §1 The order: level, then declared rule order, against a running box

`arrangeLayersForMonitor` drops the layer dynamic type (:2680) and snapshots
`ORIGINAL_USABLE_AREA = logicalBoxMinusReserved()` (:2682) — the monitor's logical box
(`{m_position, m_size}`, S465 :1768-1770) after the static reserve (`m_reservedArea.apply`,
S466 :53-60) — then copies it into `usableArea` (:2683). `m_layerSurfaceLayers` is one vector
per level: the renderer indexes it with a level constant (S470 :1234, :1239), and both
arrangement walks iterate it in level order (:2690, :2693). Inside a level the vector is
`stable_sort`ed by the surface's rule `order()` descending (:2685-2688). Every arranged surface
ends its turn with `applyExclusive(*usableArea, …)` (:2664), so the next surface — same level or
later — is placed inside the box the earlier ones already shrank.

The join reproduces the sort as `(level, -order, declaration index)` and stands the declaration
index in for the container's insertion order on an `order` tie. Because the usable box is the
only box that moves, the composition is a *sequence*, not a sum of independent footprints: a
surface's box depends on which surfaces were arranged before it.

| effect | case | receipt line (`.ufo/waves/round-80/receipts/measurement-c1-r80.txt`) |
|---|---|---|
| a later level starts below the earlier one | `overlay-compose-top` | `band=66 expected=66` (26 + 40) |
| an earlier level moves the bar's own box | `bottom-level-first` | panel level 1 at `0,0,1000,40`, bar at `0,40,1000,26`; `band=66 expected=66` |
| a higher `order` wins inside one level | `same-level-order` | panel (`order` 10) at `y=6`, zone 30 + top margin 6 = 36; bar at `y=36`; `band=62 expected=62` |

## §2 The two passes, and the one bounds exception

`arrangeLayerArray` runs over the whole level array twice: first with `exclusiveZone = true`,
then with `false` (:2690-2694). A surface is skipped unless
`exclusiveZone == (PSTATE->exclusive > 0)` (:2596-2597), so the first pass takes every
`exclusive > 0` surface and the second takes every `exclusive <= 0` surface, including `-1`.
The passes are global, not per level: every exclusive surface on every level is arranged before
any non-exclusive one, so a non-exclusive surface at level 0 is placed against a box an exclusive
surface at level 3 has already shrunk. `applyExclusive` returns immediately for `exclusive <= 0`
(:2531-2533), so the second pass never moves the usable box.

`bounds` is the monitor's own full box for `exclusive == -1` (:2600-2601) and the running usable
box otherwise (:2603). `full_area` is `{m_position, m_size}` (:2588): not the usable box, and not
the static-reduced box either. The join takes `full` for `zone == -1` and `usable` otherwise, and
walks the same two passes over its ordered list.

| case | declaration | receipt |
|---|---|---|
| `overlay-unexclusive-full` | panel `exclusive: -1`, anchor bottom+right | box at full-box `y=700` on an 800-high monitor; `band=26 expected=26` |
| `full-box-vs-usable` | bottom dock (40) + top bar (26) + the same `-1` panel | panel `y=700`, not the post-arrangement usable `y=660`; `band=26 expected=26`, attr `0,26,0,40` |

## §3 `applyExclusive`: four rules in order, first match

`applyExclusive` walks a fixed four-row table in the order top, bottom, left, right
(:2534-2573) and `break`s at the first match (:2583). A row matches when any of three
equalities holds and the guard holds (:2575):

```c
if ((exclusiveEdge == edges[i].singular_anchor || anchor == edges[i].singular_anchor
     || anchor == edges[i].anchor_triplet) && exclusive + edges[i].margin > 0)
```

The triplets are the three-edge sets that leave the opposite edge free: top+left+right,
bottom+left+right, left+top+bottom, right+top+bottom (:2544, :2552, :2560, :2568). Top and left
move the positive axis and shrink the size; bottom and right only shrink (:2577-2582). One
surface moves at most one edge.

Three consequences the model encodes:

- **Equality, not containment.** A mask that is neither exactly one edge nor exactly one of the
  four triplets matches no row. `anchor-unmatched` pins a two-edge mask (top+right): the zone is
  30 and the box is real, yet the usable box is untouched (`band=26 expected=26`). A mask of all
  four edges is the same class.
- **`exclusiveEdge` is a second way in.** The same mask with `exclusiveEdge: top` matches the top
  row and reserves (`exclusive-edge-matched`: `band=56 expected=56`). The protocol rejects an edge
  that is not one of the anchor's bits (S471 :162-164), so the join refuses such a declaration at
  `stage=model` rather than modelling it. The check reads the *pending* anchor at request time, so
  a client that sets the edge before the anchor is refused on the wire while the join, which
  compares the final declared set, would accept it.
- **An unmatched positive zone is not an error.** It is a surface whose zone the compositor
  simply cannot place; the request is accepted and nothing is reserved.

## §4 The guard is on `zone + margin`, not on the zone

The second conjunct at :2575 is `exclusive + margin(edge) > 0`, and `margin(edge)` is the row's
own margin — `marginTop`, `marginBottom`, `marginLeft`, `marginRight` (:2547, :2555, :2563,
:2571) — not the opposite edge's. The amount added or subtracted is that same sum (:2577-2582).
So a positive zone cancelled by a negative margin on the matched edge does nothing at all:
`negative-margin-skip` declares zone 12 with `margin-top: -12`, the guard is `0`, no row matches,
and the band stays the bar's 26.

`exclusive <= 0` returns before the walk (:2531-2533), so a negative zone never reaches the guard
and never shrinks; `-1` is the arrange-in-the-full-box marker, not a negative reserve.

## §5 An empty arranged box is skipped before anything else

After the box is built and its margins applied, `if (box.width <= 0 || box.height <= 0)` logs and
`continue`s (:2655-2658) — before `box.round()` (:2660), before `m_geometry` (:2662), before
`applyExclusive` (:2664), and before `configure` (:2666-2667). A surface with an empty arranged
box therefore reserves nothing, has no live geometry, and does not move the usable box. The join
prints `SKIP … reason=empty`, records `SKIP` in the per-surface verdict list, and does not call
its exclusive helper. `empty-box-skip` is the case: `height: 0` with `margin-top: 1000` yields a
negative height, and the band stays 26.

## §6 One dynamic area, one early return

The compositor keeps exactly one dynamic contribution for the whole layer plane:
`resetType(RESERVED_DYNAMIC_TYPE_LS)` (:2680), then a single
`addType(RESERVED_DYNAMIC_TYPE_LS, CReservedArea{ORIGINAL_USABLE_AREA, usableArea})` (:2696). The
area is the two boxes' difference: `child.pos - parent.pos` and
`(parent.pos + parent.size) - (child.pos + child.size)` (S466 :33-34), which is what
`left/top/right/bottom` return (:80-94). `calculate()` sums the static initial box and every
dynamic delta (S466 :43-51); `addType` clamps each contribution at zero (:101-112), a no-op for
an inward shrink. S472 writes the same arithmetic out: the parent/child case expects
`left=20-10`, `top=30-10`, `right=1010-920`, `bottom=1010-930` (:32-38), and the `addType` case
expects the static and dynamic terms summed (:26-30).

The parent/child constructor bails before computing when either box is empty (S466 :19-21), and
sets `m_ok = false` without computing when the child is not contained in the parent (:23-31).
S472 pins both branches: the empty-parent and empty-child cases expect zeros (:40-52), the
not-contained case expects `ok() == false` (:53-54). A refused area contributes nothing to the
totals, because `addType` sums `left/top/right/bottom` (S466 :110-112).

Consequence: an exclusive zone that empties the usable box does not create a huge band. The layer
type adds zero, the monitor keeps only the static reserve, and with a zero static reserve the
band is zero. `ls-area-invalid` pins the shape: a 2000 zone on an 800-high monitor with the
26-high bar prints `band=0 expected=0`, and the case's frozen expectation is `attributed=2026`,
`attr=0,2026,0,0`, `ls=INVALID`. The join tests
`usable.w > 0 and usable.h > 0 and contains(original, usable)`; in the modelled subset the
not-contained branch is reached through the same overflow, because every applied amount is
positive and only shrinks the box inward.

## §7 The reply is a total; the attribution is the model

The compositor's state holds no per-surface band: the only layer-plane value is the single area
of §6, and the monitor's `reserved` is that area summed with the static one (S466 :43-51). The
monitors reply carries one four-integer `reserved` array — the join refuses any other shape
(`parse_monitors`) and the live capture prints `gt=0,26,0,0` — while the layers capture is read
for a box only (`find_layer` reads `x/y/w/h`). Anchor, zone and order are therefore *declared*
inputs, not captured ones.

The join prints two different things on purpose:

- `MADO_BARFOOT_ATTR:` one line per arranged surface: `edge=<name or none>
  contribution=<amount>`; `edge=none contribution=0` when no rule matched.
- In `MADO_BARFOOT_RESULT`: `attributed=` and `attr=` are the model's values for the bar's
  anchored edge and the full four-value vector; `gt=` is the reply's four-value vector;
  `ls=VALID|INVALID` says whether the layer area exists at all.

**ATTRIBUTED is a prediction; GT is the observation.** `reserved=EQ` compares the bar's anchored
edge only; the four-value vectors are printed for inspection, not compared. `GT` (band greater
than expected) is admissible and does not fail — an undeclared consumer can reserve more.
`DIFFER` (band less than expected) is a model or host disagreement and fails with rc 1. Two
different per-surface attributions can produce the same total; the frozen cases separate them
only because the case set pins `attr_ns` per surface, and the counter refuses a mismatched `attr`
or `attributed` (its selftest exercises both refusals).

## §8 The ten composition cases

Every row's `band` / `expected` / `reserved` values are one `MADO_R80_CASE` line of
`.ufo/waves/round-80/receipts/measurement-c1-r80.txt` at revision
`6c302a53eb8f577e83fbcadc01e05a286778df8e`, produced by the C1 command of §9 against
`.ufo/waves/round-80/controls/c1-cases-r80.json` (sha256 `17c27157…`). The ten are the tail of
the thirty-three; the first twenty-three are the round-79 cases, asserted parsed-equal
(`carried=23/23`).

| case | what decides it | `band` / `expected` / `reserved` |
|---|---|---|
| `overlay-compose-top` | level 2 bar h26, then level 3 panel h40 | 66 / 66 / EQ (26 + 40) |
| `bottom-level-first` | level 1 panel h40 first; the bar's box starts at `y=40` | 66 / 66 / EQ |
| `same-level-order` | panel `order` 10, zone 30 + top margin 6 = 36, then the bar | 62 / 62 / EQ |
| `exclusive-edge-matched` | anchor top+right, `exclusiveEdge: top`, zone 30 | 56 / 56 / EQ (26 + 30) |
| `anchor-unmatched` | the same mask without the edge; no rule matches | 26 / 26 / EQ |
| `overlay-unexclusive-full` | `exclusive: -1`, anchor bottom+right; box in the full monitor | 26 / 26 / EQ |
| `ls-area-invalid` | zone 2000 on an 800-high monitor voids the whole layer area | 0 / 0 / EQ |
| `negative-margin-skip` | zone 12, `margin-top: -12`; the guard is zero | 26 / 26 / EQ |
| `empty-box-skip` | `height: 0`, `margin-top: 1000`; the arranged box is empty | 26 / 26 / EQ |
| `full-box-vs-usable` | bottom dock 40, top bar 26, `-1` panel at full-box `y=700` | 26 / 26 / EQ, attr `0,26,0,40` |

The CASE line prints `band`, `expected` and `reserved`; the counter also compares `attributed`,
`attr`, `attr_ns`, `boxes` and `ls` against the case file, so `correct=yes` means every field
matched, not only the three shown.

## §9 The measured set, the mutants, and the before state

Counting command, at both ends of the claim (run from the lane root):

```sh
python3 -I quality/counters/c1-r80-multisurface.py --repo . \
  --rev 6c302a53eb8f577e83fbcadc01e05a286778df8e \
  --base-rev e10f7e9f528b13195a1cdde28a68a702af3045c4 \
  --controls .ufo/waves/round-80/controls/c1-cases-r80.json \
  --carried .ufo/waves/round-79/controls/c1-cases-r79.json \
  --scratch-root DIR
```

The receipt's summary line at the freeze is

```
MADO_R80_BARFOOT: cases=33 correct=33 mutants=22 killed=22 base_correct=23/33
carried=23/23 tool_selftest=111/111 verdict=TARGET_MET rev=6c302a53eb8f577e83fbcadc01e05a286778df8e
tool_sha256=c3eb5fbef794c92ba45adc85ed1dcd18c505a2776a3fb1db34742a6eed27fa99
```

The held model's line, from the same counter at `--rev e10f7e9f` (the tree that still carries
`r79-v1`), is `MADO_R80_BASE: correct=23/33 … base_sha256=9e274157…`; the ten composition cases
exit 2 because `r79-v1` has no `--surfaces` option, and the ten composition mutants are printed
`reason=anchor-absent`. Twelve round-79 mutants still die at that revision (`killed=12`).

Twenty-two single-anchor mutants, each killed iff it scores below 33 (`MADO_R80_MUTANT` lines,
same receipt; the ten new ones are the last ten):

| mutant | score | rule it falsifies |
|---|---|---|
| `opposite-margin-dropped` | 23/33 | the r78 auto-zone identity |
| `horizontal-margin-leak` | 23/33 | only the band-axis margins enter |
| `level-bottom-swap` | 32/33 | level ordering |
| `right-extent-flip` | 31/33 | the anchored-edge extent |
| `per-side-margin-dropped` | 32/33 | per-side margins |
| `negative-margin-accepted` | 32/33 | the bar's negative-margin refusal |
| `opposite-edge-wrong` | 32/33 | the opposite-edge map |
| `static-dropped` | 30/33 | the static term |
| `static-order-swapped` | 30/33 | `addreserved` field order |
| `static-first-wins` | 29/33 | newest rule wins |
| `static-box-unoffset` | 29/33 | the static origin |
| `static-selector-ignored` | 32/33 | selector matching |
| `attr-edge-order` | 23/33 | top/bottom row order |
| `running-bounds-ignored` | 26/33 | `bounds` is the running usable box |
| `exclusive-edge-ignored` | 32/33 | the `exclusiveEdge` disjunct |
| `edge-guard-dropped` | 32/33 | the `zone + margin > 0` guard |
| `invalid-area-kept` | 32/33 | the invalid-area zeroing |
| `full-box-uses-usable` | 32/33 | `exclusive == -1` uses the full box |
| `empty-box-contributes` | 32/33 | the empty-box skip |
| `same-level-order-ignored` | 32/33 | the `order` tie-break |
| `zone-margin-not-added` | 32/33 | `amount = zone + margin` |
| `attribution-not-summed` | 23/33 | per-edge attribution summing |

### Numbers and where they come from

| number | value | command | revision |
|---|---|---|---|
| frozen cases | 33 | `python3 -c 'import json;print(len(json.load(open(".ufo/waves/round-80/controls/c1-cases-r80.json"))["cases"]))'` | content at `6c302a53`; sha256 `17c27157…` |
| carried cases, parsed-equal | 23/23 | `MADO_R80_CONTROL: … carried=23/23` from the C1 command | `6c302a53` |
| cases correct | 33/33 | C1 command above | `6c302a53` |
| mutants killed | 22/22 | C1 command above | `6c302a53` |
| tool selftest | 111/111 | C1 command above (`--selftest` of the extracted tool) | `6c302a53` |
| tool sha256 | `c3eb5fbe…` | `git show 6c302a53:tools/mado-barfoot.py \| sha256sum` | `6c302a53` |
| held-model base score | 23/33 | C1 command at `--rev e10f7e9f` | `e10f7e9f` |
| base mutants killed | 12/22 | same run (`reason=anchor-absent` × 10) | `e10f7e9f` |
| base tool selftest | 50/50 | same run | `e10f7e9f` |
| base tool sha256 | `9e274157…` | `git show e10f7e9f:tools/mado-barfoot.py \| sha256sum` | `e10f7e9f` |
| live join | `band=26 expected=26 attributed=26` | `python3 -I tools/mado-barfoot.py --config <copy> --layers … --monitors … --monitor DP-1 --surfaces <wallpaper>` | captured 2026-11-04 (UTC), `r80-v1` |
| pinned sources | 5/5 OK | `sha256sum -c .ufo/waves/round-80/fetch/sha256-r80.txt` | pins @ `efb5099` |

## §10 What this entry does not claim

1. **No per-surface attribution on the host.** The monitors reply carries one total, and the
   layers capture is read for a box only. `ATTR:`/`attr=` are the join's model; only the bar's
   anchored edge is compared, and only against the total. Today's host has one exclusive surface
   (the live receipt's `attributed=26 gt=0,26,0,0`), so no second exclusive band has been
   observed — the composition is exercised, the attribution is not confirmed by any reply.
2. **`order()` is only a declared integer.** The compositor sorts by the surface's rule; no
   capture carries it, so a caller declares it. A wrong `order` moves boxes and attribution; an
   edge total is a sum, so it can stay unchanged.
3. **`preview_scale` is unmodelled.** The join has no field for it and makes no claim about a
   layer surface whose box is scaled before arrangement; every box in this entry is the declared
   size.
4. **Cross-axis overflow with a valid area is unmodelled.** A box wider (or taller) than the
   bounds, whose exclusive band still leaves a valid usable box, is arranged by the arithmetic
   here and its band is predicted; what the compositor renders for the overflowing box, and
   whether the client accepts the resulting configure, is outside this entry.
5. **No runtime probe.** No layer surface was created, no exclusive zone was set, no compositor
   verb was run. The model is source plus captured bytes; the live join is a read-only capture.
6. **The declaration index stands in for insertion order** on an `order` tie inside a level; the
   compositor's tie is the container's insertion order, which no capture exposes.
7. **`m_noProcess` surfaces are not modelled.** `arrangeLayerArray` skips a surface with
   `m_noProcess` (S470 :2591-2592); the declaration has no such field and the join would arrange
   it.
8. **Two surfaces of one namespace on one level are refused** by the join
   (`find_layer` raises `Unmodelled`), while the compositor arranges both.
9. **`exclusive: "auto"` is the round-78 waybar identity** (`size + unanchored margin`) keyed on
   the declared `position`, not a general gtk-layer-shell auto-zone computation for an arbitrary
   anchor mask; a custom mask should declare the integer.
10. **The static reserve path is unchanged from round 79** and keeps its limits: a `source =`
    line, a `desc:` or empty selector, and one rule per selector are refused, never guessed.

## §11 Evidence

- `.ufo/waves/round-80/fetch/S470.bin`–`S472.bin`, `sha256-r80.txt` (5/5 OK) — the three pins,
  `S470` byte-identical to the held `S457` (`9af8a74e…`).
- `.ufo/waves/round-79/fetch/S457.bin`, `S459.bin`, `S465.bin`, `S466.bin`, `sha256-r79.txt` —
  the held pins; `S459` and `S466` are the same `ReservedArea.cpp` bytes (`0a52e145…`).
- `.ufo/waves/round-80/receipts/measurement-c1-r80.txt` — 33 cases, 22/22 mutants,
  `base_correct=23/33`, `carried=23/23`, `tool_selftest=111/111`, `TARGET_MET`.
- `.ufo/waves/round-80/receipts/control-c1-r80-at-base.txt` — the held `r79-v1` at `e10f7e9f`:
  23/33, 12/22 mutants, `tool_selftest=50/50`, `TARGET_MISSED`.
- `.ufo/waves/round-80/receipts/live-join-r80.txt` — the read-only host join: `CLEAN`, then the
  `--surfaces` run with `boxes=MATCH,MATCH … attributed=26 gt=0,26,0,0`.
- `.ufo/waves/round-80/controls/c1-cases-r80.json` — sha256 `17c27157…`, 33 cases; generator
  `controls/make-cases-r80.py`.
- `tools/mado-barfoot.py` — `r80-v1`, sha256 `c3eb5fbe…`;
  `quality/counters/c1-r80-multisurface.py` — the counter, selftest 60/60.

## Sources

S470, S471, S472, S457, S459, S465, S466 in [SOURCES](../SOURCES.md).
