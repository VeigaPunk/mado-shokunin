# R81ScoutModel — source recon on the six frozen C1 cases

Round 81, wave w1. Read-only: no code, instrument, control set, declaration, SKILL.md or LOG.md was
edited. The six cases were replayed with the frozen tool from my scratch root
(`/fast/scratch/hyaku/mado-r81/R81ScoutModel`, deleted before yield); the verbatim replay is kept as
`R81ScoutModel/run-output.txt`.

Instruments at the freeze (re-hashed, read-only):

| instrument | sha256 (first 16) |
|---|---|
| `tools/mado-barfoot.py` | `a129a435572805c3` |
| `quality/counters/c1-r81-overflow-auto.py` | `224051330291fdf4` |
| `.ufo/waves/round-81/controls/c1-cases-r81.json` | `ab8154a1d4bc5d2a` |

Replay command shape (the counter's own argv, reproduced; `sys.executable -I`, clean env, cwd inside
scratch):

```
/usr/bin/python3 -I .../tools/mado-barfoot.py --config <case>/config.json \
  --layers <case>/layers.json --monitors <case>/monitors.json \
  [--surfaces <case>/surfaces.json] [--monitor M1]
```

Every one of the six reproduces the frozen `expect` exactly (rc, DECL/ATTR/RESULT, `attr_ns`). The
frozen measurement receipt agrees: `cases=39 correct=39 mutants=28 killed=28 base_correct=33/39
carried=33/33 tool_selftest=121/121 verdict=TARGET_MET`.

## 1. The six new cases and their frozen `expect`

Names taken from `.ufo/waves/round-81/controls/c1-cases-r81.json`; values verbatim.

1. `overflow-tie-negative`
   `{"attr":"0,26,0,0","attr_ns":{"waybar":"top:26"},"attributed":26,"band":26,"box":"MATCH",
   "boxes":"MATCH,MATCH","expected":26,"gt":"0,26,0,0","ls":"VALID","rc":0,"reserved":"EQ",
   "verdict":"CLEAN"}`
2. `auto-dynamic-band-refused` — `{"error":true,"rc":3,"stage":"model"}`
3. `auto-corner-edge`
   `{"attr":"0,26,0,0","attr_ns":{"waybar":"top:26"},"attributed":26,"band":26,"box":"MATCH",
   "boxes":"MATCH,MATCH","expected":26,"gt":"0,26,0,0","ls":"VALID","rc":0,"reserved":"EQ",
   "verdict":"CLEAN"}`
4. `auto-all-four-edge` — same expect object as `auto-corner-edge`.
5. `auto-parallel-edge` — same expect object as `auto-corner-edge`.
6. `auto-left-dock`
   `{"attr":"40,26,0,0","attr_ns":{"dock":"left:40","waybar":"top:26"},"attributed":26,"band":26,
   "box":"MATCH","boxes":"MATCH,MATCH","expected":26,"gt":"0,26,0,0","ls":"VALID","rc":0,
   "reserved":"EQ","verdict":"CLEAN"}`

## 2. Hand derivation, with arithmetic

Shared prelude. The bar (`config {"height":26,"layer":"top","position":"top"}`, no margins) is
anchor `top+left+right`, desired `26` high, `width==0`; over `bounds {0,0,1000,800}` it stretches to
`{0,0,1000,26}` and requests gtk-layer-shell's auto zone. `S464:270-276`:

```
gboolean horiz = (anchors[LEFT] == anchors[RIGHT]);      // true == false -> false
gboolean vert  = (anchors[TOP]  == anchors[BOTTOM]);     // true == false -> false at top
int new_exclusive_zone = -1;
if (horiz && !vert) { new_exclusive_zone = current_allocation.height; ...
```

The bar is horizontal-only, so `horiz` must be true — at `position: top` the anchor is
`top+left+right`, hence `anchors[LEFT]==anchors[RIGHT]` is `true==true` → `horiz=true`;
`anchors[TOP]==anchors[BOTTOM]` is `true==false` → `vert=false`; branch 1 →
`zone = current_allocation.height = 26` (anchors[TOP] set → no top margin; anchors[BOTTOM] clear →
`+margins[BOTTOM]=0`). `S470:2575-2578` then hits the top edge (`S470:2606-2621` box is `{0,0,1000,26}`,
anchor `13 ==` the top triplet `13`): `*positive_axis += 26; *negative_axis -= 26` → usable
`{0,26,1000,774}`. This prelude is common to all four non-refused `auto-*` cases and to
`overflow-tie-negative`.

### 2.1 `overflow-tie-negative`

Source: `S478:51-63` (hyprutils v0.14.0, `CBox::round`):

```cpp
CBox& Hyprutils::Math::CBox::round() {
    double roundedX = std::round(x);
    double roundedY = std::round(y);
    double newW     = x + w - roundedX;
    double newH     = y + h - roundedY;

    x = roundedX;
    y = roundedY;
    w = std::round(newW);
    h = std::round(newH);
```

Source: `S470:2610-2621` (horizontal, then vertical placement; the panel declares
`anchor ["left","right"]`, `width 1001`, `height 100`):

```
box.x = bounds.x + ((bounds.width / 2) - (box.width / 2));   // :2613
box.y = bounds.y + ((bounds.height / 2) - (box.height / 2)); // :2619, no top/bottom anchor
```

Arithmetic (panel is level 3, processed after the bar; `bounds = usable {0,26,1000,774}`):

- `x = 0 + (1000/2 - 1001/2) = 500 - 500.5 = -0.5`
- `y = 26 + (774/2 - 100/2) = 26 + 387 - 50 = 363`
- unrounded `{-0.5, 363, 1001, 100}`
- `rx = std::round(-0.5) = -1` (half away from zero, not Python's `round(-0.5) == 0`)
- `newW = x + w - rx = -0.5 + 1001 - (-1) = 1001.5` → `std::round(1001.5) = 1002`
- `ry = 363`; `newH = 363 + 100 - 363 = 100` → `100`
- rounded box `(-1, 363, 1002, 100)`; the case's layers reply is exactly `x=-1,y=363,w=1002,h=100`
- zone `0` (explicit) → no shrink; final usable `{0,26,1000,774}`; `ls = 0,26,0,0`, `expected.top = 26`,
  reserved band `26` → `EQ`; `attributed` = `0,26,0,0` (the bar's 26 only).

The tie is load-bearing twice: the negative origin rounds away from zero to `-1`, and the far-edge
distance `1001.5` rounds away from zero to `1002` (rounding the width on its own, `round(1001)=1001`,
lands the far edge at `1000` and loses the compositor's width). Literal tool lines:

```
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=-1,363,1002,100 anchor=left+right zone=0
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN
```

### 2.2 `auto-dynamic-band-refused`

The surface is `{"exclusive":"auto","height":0,"level":3,"namespace":"panel"}`; with no `anchor` and no
`position`, the model's declaration default is the top anchor set `top+left+right` (the same set the
bar uses). `S464:270-277`:

- `horiz = true` (LEFT == RIGHT), `vert = false` (TOP != BOTTOM) → branch 1
- `new_exclusive_zone = self->current_allocation.height` — and `current_allocation` is not a declared
  value: it is filled from GTK's allocation in `layer_surface_on_size_allocate` (`S464:307-310`),
  starting life at `{0,0}` (`S464:339-342`). With `height: 0` the declaration says nothing about it.
- `if (new_exclusive_zone >= 0 && …)` (`S464:289`) would only send a zone once an allocation exists.

So the declared bytes do not determine the zone. The case's expectation is a refusal
(`{"error":true,"rc":3,"stage":"model"}`), which the tool emits as
`MADO_BARFOOT: ERROR (stage=model auto zone on a dynamic height (0) is the client's allocation, not a
declared value)`.

Consistency check that the refusal is forced, not a dodge: the case's own monitors reply is
`reserved [0,26,0,0]`, and the panel's layer box is 774 tall. If a model read the zone off that box
(`774`), the panel would add 774 on top → reserved top `800`, `ls` invalid, band `26 != expected 0` →
`DIFFER`. The fixture is only satisfiable by *not* computing the zone, i.e. by refusing.

### 2.3 `auto-corner-edge`

Surface `anchor ["top","left"]`, `exclusive "auto"`, `exclusiveEdge "top"`, `height 100`, `width 200`.
`S464:270-273`:

- `horiz = (anchors[LEFT] == anchors[RIGHT]) = (true == false) = false`
- `vert  = (anchors[TOP]  == anchors[BOTTOM]) = (true == false) = false`
- neither `horiz && !vert` nor `vert && !horiz` → `new_exclusive_zone` stays `-1`; the
  `>= 0` guard (`S464:289`) skips the set call. gtk-layer-shell's initial `self->exclusive_zone = 0`
  (`S464:348`) was already sent when the layer surface was created (`S464:195`), so the compositor's
  zone is `0`. (`exclusiveEdge "top"` cannot change this: the gate returns before any edge is read.)

Box (bounds `{0,26,1000,774}`): `x = bounds.x = 0` (left anchored, width > 0), `y = bounds.y = 26`
(top anchored, height > 0) → `(0,26,200,100)`. No zone → no ATTR; `ls = 0,26,0,0`, band 26 → `EQ`.

```
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=0,26,200,100 anchor=top+left zone=0
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN
```

### 2.4 `auto-all-four-edge`

Anchor `top+bottom+left+right`:

- `horiz = (true == true) = true`, `vert = (true == true) = true`
- `horiz && !vert` is false, `vert && !horiz` is false → `new_exclusive_zone = -1` → no set → zone `0`.

Box: both pairs anchored → `x = 0 + (1000/2 - 200/2) = 400`;
`y = 26 + (774/2 - 100/2) = 26 + 337 = 363` → `(400,363,200,100)`, matching the layers reply.

```
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=400,363,200,100 anchor=top+bottom+left+right zone=0
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN
```

### 2.5 `auto-parallel-edge`

Anchor `top+bottom` (the "parallel" pair):

- `horiz = (anchors[LEFT] == anchors[RIGHT]) = (false == false) = true` — note this is true precisely
  because *neither* horizontal edge is anchored;
- `vert = (anchors[TOP] == anchors[BOTTOM]) = (true == true) = true`;
- both branches fail → `-1` → zone `0`. The vertical pair therefore gets no zone, and the reason is
  `vert` being true, not `horiz` being false.

Box: no horizontal anchor → `x = 0 + (1000/2 - 200/2) = 400`; both vertical → `y = 26 + 337 = 363` →
`(400,363,200,100)`.

```
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=400,363,200,100 anchor=top+bottom zone=0
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN
```

### 2.6 `auto-left-dock`

Surface `{"namespace":"dock","level":1,"anchor":["left"],"exclusive":"auto","width":40}` (`height` 0).
`S464:270-287`:

- `horiz = (true == false) = false`; `vert = (false == false) = true` → `vert && !horiz` branch:
- `new_exclusive_zone = current_allocation.width` = `40` (the case declares `width: 40` and its layers
  reply is a 40-wide dock — see §3 for the one inference this step carries);
- `anchors[LEFT]` is true → do **not** add `margins[LEFT]`; `anchors[RIGHT]` is false →
  `+ margins[RIGHT] = 0` → zone `40`.

Hyprland side, `S470:2529-2586` (`applyExclusive`):

- `if (exclusive <= 0) return;` (`S470:2531`) does not fire (`40 > 0`).
- Edge table order is top, bottom, left, right (`S470:2534-2573`). Dock anchor mask is `left` (`4`):
  top rule needs `anchor == 1` or `anchor == 13` → no; bottom → no; left rule `singular_anchor = 4` →
  `anchor == singular` matches, and `exclusive + marginLeft = 40 + 0 > 0` (`S470:2575`) → hit:
  `usableArea.x += 40; usableArea.width -= 40` (`S470:2577-2578`) → usable `{40,0,960,800}`.
- Bar is next (level 2 > level 1): bounds `{40,0,960,800}` → stretch `x=40,w=960`, `y=0,h=26`;
  zone `26` hits top → usable `{40,26,960,774}`.

Attribution: `(dock,left)=40`, `(waybar,top)=26`. `ls` vector from
`CReservedArea(ORIGINAL_USABLE_AREA, usableArea)` (`S459:19-36`): `left = 40`, `top = 26`, right 0,
bottom 0 → `ls = 40,26,0,0`, `ls=VALID`. `expected.top = 26`, reserved band top `26` → `EQ`;
`attributed.top = 26`; the whole vector is `40,26,0,0`.

```
MADO_BARFOOT_DECL: monitor=M1 level=1 ns=dock box=0,0,40,800 anchor=left zone=40
MADO_BARFOOT_ATTR: monitor=M1 level=1 ns=dock edge=left contribution=40 box=0,0,40,800
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=40,0,960,26 anchor=top+left+right zone=26
MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=waybar edge=top contribution=26 box=40,0,960,26
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=40,26,0,0 ls=VALID verdict=CLEAN
```

## 3. What the bytes do not yield

Five of the six derive end to end. One case's expectation does not, and it *contradicts* the pinned
source rather than merely being underdetermined:

**`auto-left-dock` — its `gt` (and the monitors fixture behind it) contradicts `S470` + `S459`.**
`arrangeLayersForMonitor` ends with (`S470:2696`):

```
PMONITOR->m_reservedArea.addType(Desktop::RESERVED_DYNAMIC_TYPE_LS, Desktop::CReservedArea{ORIGINAL_USABLE_AREA, usableArea});
```

and `CReservedArea(parent, child)` takes the whole-box inset (`S459:33-34`):

```
m_initialTopLeft     = child.pos() - parent.pos();
m_initialBottomRight = (parent.pos() + parent.size()) - (child.pos() + child.size());
```

`ORIGINAL_USABLE_AREA` is `{0,0,1000,800}` and the final `usableArea` is `{40,26,960,774}`, so the
monitor's reserved area is `left 40, top 26, right 0, bottom 0` — `[40,26,0,0]`. The frozen fixture
says `"reserved": [0, 26, 0, 0]` (left 0) while its own layers reply puts the bar at `x=40`, which only
a 40-left reserve can produce. The case passes because the counter compares only the *bar's* edge band
(`band = reserved[1] = 26`, `expected.top = 26`); the left entry is never asserted, and `gt` merely
echoes the impossible fixture. **What is missing:** a monitor reply whose left entry is `40`
(`[40,26,0,0]`), i.e. a fixture consistent with its own layers reply — or a case that asserts the left
band, which would force that reply. As stated, `attr=40,26,0,0` and `gt=0,26,0,0` cannot both describe
one monitor.

Two smaller boundaries, both stated as such and not as case errors:

- **`auto-left-dock`'s zone value.** `S464:282` reads `current_allocation.width`, which S464 fills from
  GTK's `GdkRectangle` at size-allocate (`S464:307-310`), not from the declared `width`. The case's 40
  is the declared width *and* the live dock width, so the value is right, but "declared 40 ⇒ allocation
  40" is an inference corroborated by the layers reply, not a derivation from the pinned bytes.
- **`auto-dynamic-band-refused`.** Nothing is missing from the source: the refusal is exactly "the
  value is the client's allocation", which the declaration cannot carry. The reply does carry the
  realized 774-tall box, so the case is underdetermined only under the tool's declaration-only posture
  — and §2.2 shows that reading 774 back would make the case's own band unsatisfiable, so the refusal
  is the only self-consistent expectation.

For the record, the non-obvious derivations that *are* fully pinned: the negative half-way tie
(`std::round` away from zero, `S478:52`), the auto gate's three refusals (corner, parallel pair, all
four; `S464:275-288` + the `0` default at `S464:348` and the create-time send at `S464:195`), and the
left-dock attribution (edge order + the left singular match, `S470:2534-2578`).

## 4. Probes of unpinned reachable classes (≤4, exact lines)

Each probe is a fresh fixture under scratch, run with the same argv shape as the six. None is proposed
as a round-82 target; these are the measured behaviours of the successor tool on classes the frozen 39
do not pin (verified by enumerating every `surfaces[]` entry of all 39: no auto surface carries a
margin, no `exclusiveEdge` differs from the first matching edge, no negative margin is followed by a
second matching edge, and the only empty-box case is on the height axis).

### P1 `probe-auto-left-margins` — auto zone, vertical axis, margins on both edges — **right**

Dock `anchor ["left"], exclusive "auto", width 40, margins {left:3, right:5}`, height 0.
`S464:282-287`: zone `= allocation.width(40) + margins[RIGHT](5) = 45` (left anchored → no left margin,
right unanchored → added). `S470:2575-2578`: left edge, `amount = 45 + margins[LEFT](3) = 48`.
Box: `x = bounds.x + margin.left = 3`, `w = 40`, `y = 0`, `h = 800`.

```
MADO_BARFOOT_DECL: monitor=M1 level=1 ns=dock box=3,0,40,800 anchor=left zone=45
MADO_BARFOOT_ATTR: monitor=M1 level=1 ns=dock edge=left contribution=48 box=3,0,40,800
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=48,0,952,26 anchor=top+left+right zone=26
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=48,26,0,0 ls=VALID verdict=CLEAN
```

The tool adds the unanchored margin in the client's zone *and* the anchored margin in the compositor's
shrink, and offsets the box by its own anchored margin — all three match the source. `right`.

### P2 `probe-triplet-preempts-edge` — explicit `exclusiveEdge` preempted by the top triplet — **right**

Panel `anchor ["top","left","right"], exclusive 30, exclusiveEdge "left", height 100`.
`S470:2575` iterates top first: `exclusiveEdge(4) == 1`? no; `anchor(13) == 1`? no;
`anchor(13) == top triplet(13)`? **yes** → top wins; the declared edge `left` is never reached.
So `contribution = 30`, not 30 on left.

```
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=0,26,1000,100 anchor=top+left+right zone=30
MADO_BARFOOT_ATTR: monitor=M1 level=3 ns=panel edge=top contribution=30 box=0,26,1000,100
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=56 expected=56 attributed=56 gt=0,56,0,0 attr=0,56,0,0 ls=VALID verdict=CLEAN
```

This combination is protocol-legal (left *is* anchored) and the source silently prefers the triplet.
`right`.

### P3 `probe-edge-fallthrough` — first matching edge fails the `zone+margin` guard, loop falls through — **right**

Panel `anchor ["top","left","bottom"], exclusive 12, exclusiveEdge "top", margins {top:-12, left:5}`,
height 0, width 0. `S470:2575`: top matches by `exclusiveEdge`, but `12 + (-12) = 0` is not `> 0`
(`S470:2575` second conjunct) → **no break**, the loop continues; bottom matches nothing; left matches
by `anchor == left triplet (L|T|B = 7)` and `12 + 5 = 17 > 0` → left, `amount 17`.
Box: `x = 0 + 5 = 5`; `w = 1000 - 5 - 0 = 995`; `y = 26 + (-12) = 14`; `h = 774 - (-12) - 0 = 786`.

```
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=5,14,995,786 anchor=top+left+bottom zone=12
MADO_BARFOOT_ATTR: monitor=M1 level=3 ns=panel edge=left contribution=17 box=5,14,995,786
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=17,26,0,0 ls=VALID verdict=CLEAN
```

The frozen `negative-margin-skip` only pins the *failing* first match with no second candidate; this
probe pins the fall-through. `right`.

### P4 `probe-width-axis-skip` — the empty-box skip on the width axis — **right**

Panel `anchor ["left","right"], exclusive 0, height 100, width 0, margins {left:600, right:600}`.
Stretch width `= 1000 - 600 - 600 = -200`; the guard at `S470:2655`
(`if (box.width <= 0 || box.height <= 0)`) logs and `continue`s before `box.round()`/`applyExclusive`.
The frozen `empty-box-skip` pins the height axis only.

```
MADO_BARFOOT_SKIP: monitor=M1 level=3 ns=panel box=600,363,-200,100 reason=empty
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,SKIP reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN
```

Box `x = 0 + 600 = 600`, `y = 26 + (774/2 - 100/2) = 363`; no zone, no ATTR, no LIVE check. `right`.

## 5. Limits of this seat

- No code, instrument, control set, declaration, SKILL.md or LOG.md was edited; the lane git tree was
  not touched.
- The report proposes no round-82 target (per the seat).
- The one contradiction found (`auto-left-dock`'s monitor vector) is a fixture/expectation issue, not a
  tool failure: the tool's `attr=40,26,0,0` is the source-correct vector and its `gt` is the fixture's.
