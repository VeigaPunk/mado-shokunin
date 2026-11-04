# The composition's overflow rounding and its auto-zone gate (round 81)

source: S478, S479, S480; held S460, S464, S470
verified-at: 0e2ccd2a8692825cac534f57246053b276be9f13 (the round-81 freeze named in
`claims-declaration-r81.md`) and f3eb70c744113b4573f1f79b27edbc20ea2e9ba3 (the content tip, where
the same counting command re-ran `TARGET_MET`; `tools/mado-barfoot.py` at that revision is byte-identical to the
worktree, sha256 `a129a435572805c3ae7730714f0dafdea2b9a7e420f53f0d109dc2d5f57d1230`)
recheck: `python3 -I quality/counters/c1-r81-overflow-auto.py --repo . --rev REV --base-rev
c702094ace5dd9b2b5e152951b4b2f4dd578f8b6 --controls .ufo/waves/round-81/controls/c1-cases-r81.json
--carried .ufo/waves/round-80/controls/c1-cases-r80.json --scratch-root DIR` — 39 frozen cases
(33 carried parsed-equal + 6), 28 named mutants, exit 0 only on `MADO_R81_BARFOOT: cases=39
correct=39 mutants=28 killed=28 base_correct=33/39 carried=33/33 tool_selftest=121/121
verdict=TARGET_MET`

## 1. What this entry is and is not

The round-80 entry (`bar-footprint-composition-r80.md`) composed N layer surfaces under one running
usable box and then named four reachable classes where its model was **wrong** (§11 there). This
entry states the two source propositions the round-81 cases stand on — the coupled rounding inside
`CBox::round`, and the client-side auto-zone gate — and fixes each with a frozen case.

It is a **model over captured bytes**. No layer surface is created, no compositor verb is run, and
no claim is made about a live surface beyond the fixtures named below. The instrument read is
`tools/mado-barfoot.py` (`r81-v1`, sha256 `a129a435…`), scored by
`quality/counters/c1-r81-overflow-auto.py`; the round's measured receipt is
`.ufo/waves/round-81/receipts/measurement-c1-r81.txt`:

```
measurement-c1-r81.txt:70  MADO_R81_BARFOOT: cases=39 correct=39 mutants=28 killed=28 base_correct=33/39 carried=33/33 tool_selftest=121/121 verdict=TARGET_MET rev=0e2ccd2a… tool_sha256=a129a435…
measurement-c1-r81.txt:68  MADO_R81_BASE: correct=33/39 rule=held-r79-model(no-multi-surface-arrangement) base_rev=c702094ace5dd9b2b5e152951b4b2f4dd578f8b6 …
measurement-c1-r81.txt:69  MADO_R81_CONTROL: sha256=ab8154a1… carried=33/33
```

The base instrument scores 33/39 on the successor set (`measurement-c1-r81.txt:68`), and a seat-side
re-run of the base bytes confirms the split: 33/33 carried, 0/6 new
(`.ufo/waves/round-81/w1/R81ScribeEntry/base-39-matrix.txt`, last two lines). The counter's printed
rule label says `held-r79-model(no-multi-surface-arrangement)`, but the bytes it extracts at
`base_rev` are `VERSION = "r80-v1"` with `evaluate_composition`
(`c702094ace5dd9b2b5e152951b4b2f4dd578f8b6:tools/mado-barfoot.py:85`, `:652`); the label is the
counter's, not the file's, and the 33 are the carried round-80 cases. The read of each new `LIVE` box
is the case's supplied layers reply, not a compositor capture (the fixtures are 1000×800 with
`pid: 4242`; `.ufo/waves/round-81/controls/make-c1-cases-r81.py:18-33`). No fixture in either set
is a recorded host reply, so every `box=MATCH` below is a model-versus-source check.

## 2. `CBox::round` is coupled

Hyprland centres a box in doubles (`S470` `src/render/Renderer.cpp:2613`):

```c
box.x = bounds.x + ((bounds.width / 2) - (box.width / 2));
```

and rounds once, after the empty-box skip (`S470:2655-2657`, `S470:2660`):

```c
box.round(); // fix rounding errors
```

The rounding is in hyprutils, and it is **not per-field**. `S478` (`hyprutils` v0.14.0
`src/math/Box.cpp`) lines 51-63, verbatim:

| line | text |
|---|---|
| 51 | `CBox& Hyprutils::Math::CBox::round() {` |
| 52 | `    double roundedX = std::round(x);` |
| 53 | `    double roundedY = std::round(y);` |
| 54 | `    double newW     = x + w - roundedX;` |
| 55 | `    double newH     = y + h - roundedY;` |
| 56 | `` |
| 57 | `    x = roundedX;` |
| 58 | `    y = roundedY;` |
| 59 | `    w = std::round(newW);` |
| 60 | `    h = std::round(newH);` |
| 61 | `` |
| 62 | `    return *this;` |
| 63 | `}` |

The width that is rounded is the **unrounded far edge minus the rounded origin** (`:54`), not the
width field itself; `:59` then rounds that distance. So both edges are rounded independently and the
rounded box spans `round(left) .. round(right)`.

Derivation of the frozen overflow (`overflow-tie-negative`,
`.ufo/waves/round-81/controls/c1-cases-r81.json:2103`, surface declaration at `:2104-2116`): a
1001-wide panel with `left|right` anchors against the 1000-wide running usable box
`0,26,1000,774`. The unrounded origin is

```
x = 0 + (1000/2 - 1001/2) = -0.5
```

`std::round` is half **away from zero** (C++11 26.8/9), so `round(-0.5) = -1` (`S478:52`), and the
distance to round is

```
newW = x + w - roundedX = -0.5 + 1001 - (-1) = 1001.5   ->   round(1001.5) = 1002
```

giving `x=-1, w=1002` — the box is two pixels wider than the bounds, with its right edge at
`x+w = 1001`, one pixel past the 1000-wide area. The vertical placement has no tie:
`y = 26 + (774/2 - 100/2) = 363` (`S470:2632`).

The floor-divided reading gives the other answer. The round-80 model centred with the integer form
`(bounds.size - size + 1) // 2` (`corpus/knowledge/bar-footprint-composition-r80.md:193`; the base
tool's `x = bounds["x"] + (bounds["w"] - w + 1) // 2`, `git show
c702094ace5dd9b2b5e152951b4b2f4dd578f8b6:tools/mado-barfoot.py` line 503). With bounds 1000 and size
1001 the numerator is `1000 - 1001 + 1 = 0`, so
`0 // 2 = 0`: the origin stays `0` and the width is never recomputed, `0/1001`. The two models agree
on every box that fits its bounds because the tie is non-negative there; they separate only when the
tie lands at a negative half.

The round-81 join implements the coupled form (`tools/mado-barfoot.py:498-506`: `rx = std_round(...)`,
`nw = box["x"] + box["w"] - rx`, `"w": int(std_round(nw))`) and the frozen case pins the result:

```
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=-1,363,1002,100 anchor=left+right zone=0
MADO_BARFOOT_LIVE: monitor=M1 level=3 ns=panel box=-1,363,1002,100 entries=1
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN
```

(seat receipt `.ufo/waves/round-81/w1/R81ScribeEntry/join-six-cases.txt`). The expected box is
source-derived in the counter, never from a tool run
(`quality/counters/c1-r81-overflow-auto.py:15-18`: "expectations derived from hyprutils
`Box.cpp:51-63` … never from a tool run").

## 3. Which hyprutils revision this is

The rounding lives in hyprutils, not in Hyprland. Hyprland's `CMakeLists.txt` at the host's commit
`efb50993…` declares the dependency pin (`S479:150`):

```
set(HYPRUTILS_MINIMUM_VERSION 0.14.0)
```

and consumes it as a **minimum** (`S479:156`):

```
pkg_check_modules(hyprutils_dep REQUIRED IMPORTED_TARGET hyprutils>=${HYPRUTILS_MINIMUM_VERSION})
```

The inference class of this line is a **version-pin licence**, not a runtime read: `>=0.14.0`
licenses the tag `v0.14.0` whose `Box.cpp` is S478; it does not assert which revision the running
compositor linked (the host runs Hyprland 0.56.2). Separately, the local package database
read this round (`pacman -Q hyprutils hyprland`, 2026-11-04) reports:

```
hyprutils 0.14.2-1
hyprland 0.56.2-4
```

So the host carries hyprutils **0.14.2**, two patch releases above the tag the bytes come from. Whether
`CBox::round` is unchanged between `v0.14.0` and `0.14.2` is `[UNK]`: it would be settled by
opening the `v0.14.2` tarball's `src/math/Box.cpp` (not fetched by this seat, whose instruction is to
read the committed pins rather than re-fetch). The six new cases cannot distinguish the two, since
their layers replies are constructed to the derivation by the frozen case generator, not captured
from the host (§1).

The host compositor version itself is from the round-80 entry's `hyprctl version` read
(`bar-footprint-composition-r80.md:14-15`: `Hyprland 0.56.2 … commit
efb50993780079460b0cbed1363e2166a2de1d9f`); the seat did not re-run `hyprctl` this round.

## 4. The auto zone is the client's

The compositor stores whatever integer the client sends; for `exclusive = auto` that integer is
computed client-side by gtk-layer-shell (`S464` v0.10.1 `src/layer-surface.c:264-292`). The gate and
the size source, verbatim:

```c
    gboolean horiz = (self->anchors[GTK_LAYER_SHELL_EDGE_LEFT] ==
                      self->anchors[GTK_LAYER_SHELL_EDGE_RIGHT]);
    gboolean vert = (self->anchors[GTK_LAYER_SHELL_EDGE_TOP] ==
                     self->anchors[GTK_LAYER_SHELL_EDGE_BOTTOM]);
    int new_exclusive_zone = -1;

    if (horiz && !vert) {
        new_exclusive_zone = self->current_allocation.height;
        if (!self->anchors[GTK_LAYER_SHELL_EDGE_TOP])
            new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_TOP];
        if (!self->anchors[GTK_LAYER_SHELL_EDGE_BOTTOM])
            new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_BOTTOM];
    } else if (vert && !horiz) {
        new_exclusive_zone = self->current_allocation.width;
        if (!self->anchors[GTK_LAYER_SHELL_EDGE_LEFT])
            new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_LEFT];
        if (!self->anchors[GTK_LAYER_SHELL_EDGE_RIGHT])
            new_exclusive_zone += self->margins[GTK_LAYER_SHELL_EDGE_RIGHT];
    }

    if (new_exclusive_zone >= 0 && self->exclusive_zone != new_exclusive_zone) {
        self->exclusive_zone = new_exclusive_zone;
        if (self->layer_surface) {
            zwlr_layer_surface_v1_set_exclusive_zone (self->layer_surface, self->exclusive_zone);
```

(`S464:269-292`.) Four facts follow.

1. **The gate is equality, not "spans".** `horiz` is true when the two horizontal anchors are equal —
   both present **or both absent** (`:269-270`); `vert` likewise (`:271-272`). The branches are
   `horiz && !vert` (`:275`) and `vert && !horiz` (`:281`). A corner pair (`top|left`) puts both
   false; a parallel pair (`top|bottom`) and all four anchors put both true. In both-true and
   both-false cases neither branch runs, `new_exclusive_zone` stays `-1` (`:273`), and nothing is
   sent (`:289`).
2. **The size is the allocation's** (`:276`, `:282` `self->current_allocation.*`), and
   `current_allocation` is assigned from GTK's allocated rectangle in
   `layer_surface_on_size_allocate` (`S464:304-313`, assignment `:307-310`). It is neither the
   requested size nor the declared size.
3. **The unanchored margins are added** on the band's axis (`:277-280`, `:283-286`): for a top bar
   (top anchored) the bottom margin; for a left dock (left anchored) the right margin. The anchored
   edge's own margin is not added.
4. **The value is sent only when it changes** (`:289-292`).

The classes the join refuses are exactly those where the gate selects a band axis but the band size
is the allocation, which the join has no input for. `surface_zone`
(`tools/mado-barfoot.py:559-592`) raises on `auto` with `height == 0` under `horiz && !vert`
(`:571-577`) and on `auto` with `width == 0` under `vert && !horiz` (`:581-587`). The frozen case
`auto-dynamic-band-refused` (`c1-cases-r81.json:2175`) declares `{"height": 0, "exclusive": "auto"}`
with no anchor key, so the parser's position default supplies the top triplet
(`tools/mado-barfoot.py:104-109`, `:625-627`) — the gate is horizontal and the height *is* the band:

```
MADO_BARFOOT: ERROR (stage=model auto zone on a dynamic height (0) is the client's allocation, not a declared value)
```

exit 3 (`make-c1-cases-r81.py:57-69`; `tools/mado-barfoot.py:1474-1476`). A modelled zero would be
wrong in a specific way: gtk-layer-shell would send the *allocation*, a number the join cannot know;
the refusal is the only honest answer. The refusal is raised at the surface's turn, after the
empty-box skip (`tools/mado-barfoot.py:786`); the ordering pass calls the same function through
`zone_for_pass`, which maps the refusal to 0 so the surface still sorts (`:595-602`).

The classes the join does **not** refuse are the gate's no-zone classes: a corner, a parallel pair,
or all four anchors return `0` from `surface_zone` (`tools/mado-barfoot.py:591-593`) without an
error, because the source sends no zone there either.

## 5. The gate's composition consequence

A zone the client never sends cannot reserve anything, and an explicit `exclusiveEdge` cannot
manufacture one. `applyExclusive` returns before its rule table when the zone is non-positive
(`S470:2531-2533`):

```c
    if (exclusive <= 0) {
        return;
    }
```

The declared edge is consulted only inside the match condition (`S470:2575`):

```c
        if ((exclusiveEdge == edges[i].singular_anchor || anchor == edges[i].singular_anchor || anchor == edges[i].anchor_triplet) && exclusive + edges[i].margin > 0) {
```

so `exclusiveEdge = top` with zone 0 is inert. The protocol says the same thing from the other side
(`S460` `set_exclusive_zone` description, `:159-163`): "A positive value is only meaningful if the
surface is anchored to one edge or an edge and both perpendicular edges. If the surface is not
anchored, anchored to only two perpendicular edges (a corner), anchored to only two parallel edges
or anchored to all edges, a positive value will be treated the same as zero."

The three frozen shapes confirm it; each declares an explicit `exclusiveEdge` that changes nothing:

| Case | Anchor set (declaration) | Join result |
|---|---|---|
| `auto-corner-edge` (`c1-cases-r81.json:2253`) | `top,left`, `exclusiveEdge: top` | `DECL … ns=panel box=0,26,200,100 anchor=top+left zone=0`; no `ATTR` row for the panel; `attr=0,26,0,0 attributed=26` |
| `auto-parallel-edge` (`:2423`) | `top,bottom`, `exclusiveEdge: top` | `DECL … ns=panel box=400,363,200,100 anchor=top+bottom zone=0`; `attr=0,26,0,0 attributed=26` |
| `auto-all-four-edge` (`:2337`) | `top,bottom,left,right`, `exclusiveEdge: top` | `DECL … ns=panel box=400,363,200,100 anchor=top+bottom+left+right zone=0`; `attr=0,26,0,0 attributed=26` |

The vertical gate is the positive control. `auto-left-dock` (`c1-cases-r81.json:2508`) declares
`anchor: ["left"]`, `width: 40`, `height: 0`, `exclusive: "auto"`: `horiz` is false
(`left != right`) and `vert` is true (`top == bottom`, both absent), so the source's zone is
`current_allocation.width + unanchored horizontal margins` (`S464:282-286`). The join uses the
declared width as the allocation's stand-in (`tools/mado-barfoot.py:582-586`), and the fixture's
layers entry has `w=40`, so the two agree. The dock at level 1 reserves the left 40, the bar at
level 2 is arranged at `x=40`, and the attribution vector carries the left band:

```
MADO_BARFOOT_DECL: monitor=M1 level=1 ns=dock box=0,0,40,800 anchor=left zone=40
MADO_BARFOOT_ATTR: monitor=M1 level=1 ns=dock edge=left contribution=40 box=0,0,40,800
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=40,0,960,26 anchor=top+left+right zone=26
MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=waybar edge=top contribution=26 box=40,0,960,26
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=40,26,0,0 ls=VALID verdict=CLEAN
```

This is the frozen set's first non-`top` attribution: `attr` is in the monitor reply's
left,top,right,bottom order (`tools/mado-barfoot.py:846-847`), so `40,26,0,0` is left 40 + top 26.
The round-80 entry listed "a left/right attribution vector" among classes probed but unpinned
(`bar-footprint-composition-r80.md:212`), which is what this case now pins.

## 6. What the join prints

`tools/mado-barfoot.py` prints one line per arranged surface plus one result. The six new cases pin
these shapes:

| Line | Fields the six pin | Emitter |
|---|---|---|
| `MADO_BARFOOT_DECL:` | `monitor= level= ns= box=x,y,w,h anchor=a+b zone=n` — the model's arranged box, the declared anchor set, the requested zone (0 for every no-zone gate) | `:787-789` |
| `MADO_BARFOOT_LIVE:` | `monitor= level= ns= box=x,y,w,h entries=1` — the case's layers entry for that namespace+level | `:800-802` |
| `MADO_BARFOOT_LIVE:` (absent) | `entries=0`, `boxes` gains `NO_LAYER` | `:791-794` |
| `MADO_BARFOOT_ATTR:` | `monitor= level= ns= edge=<edge> contribution=<zone+margin> box=<the DECL box>` — emitted only when `zone > 0` | `:804-815` |
| `MADO_BARFOOT_ATTR:` (no rule) | `edge=none contribution=0` — emitted only when `zone > 0` and no edge matches | `:807-808` |
| `MADO_BARFOOT_RESULT:` | `monitor= box= boxes= reserved= band= expected= attributed= gt= attr= ls= verdict=` | `:848-854` |
| refusal | `MADO_BARFOOT: ERROR (stage=model …)`, exit 3; **no** DECL/ATTR/RESULT | `:1474-1476` |

Read as fields: the six pin `DECL.box`, `DECL.anchor`, `DECL.zone`; `ATTR.edge` and
`ATTR.contribution` (of the six declared non-bar surfaces only `auto-left-dock`'s dock produces an
ATTR row — the five panels produce none, and the fixture bar produces its own top 26 in every case);
and `RESULT.box`, `.boxes`, `.reserved`, `.band`, `.expected`, `.attributed`, `.gt`, `.attr`, `.ls`,
`.verdict` (the `expect` objects in the six case blocks at `c1-cases-r81.json:2035-2525`). They do
not pin `LIVE` (a fixture echo) or `SKIP` (none of the six has an empty box).

Two consequences the six pin precisely:

- **Zone 0 emits no `ATTR` row at all.** For the corner/parallel/all-four cases the whole ATTR block
  is skipped by `if zone > 0:` (`:804`); `edge=none contribution=0` belongs to a *different* shape —
  a positive zone whose anchor set matches no rule, the carried `anchor-unmatched` case.
- **`boxes` is one verdict per declared surface in arrangement order**, `box` is the bar's own entry
  (`:839-845`). `reserved` is `EQ|GT|DIFFER|NOT_APPLIED` for the bar's edge only (`:830-838`), and
  the verdict is `DIFFER`/rc 1 if either the bar's box or that one edge differs (`:839-845`).

## 7. Limits

1. **The allocation is not modelled — it is refused.** gtk-layer-shell's auto zone is
   `current_allocation` (`S464:276`, `:282`), a client-rendered number. The join has no input for it,
   so `auto` with a dynamic band exits 3 rather than printing a band (`tools/mado-barfoot.py:571-587`).
   A waybar with `height = 0` would be a caller-side refusal until the join grows an allocation
   input; it is not a prediction.
2. **The refusal is per-axis.** Only the gate-selected band axis can be dynamic: `height == 0` under
   `horiz && !vert`, `width == 0` under `vert && !horiz` (`:571-587`). The other axis is not
   consulted — a `left`-anchored surface with `height = 0` is modelled from its width. And the
   no-zone classes never refuse: corner, parallel and all-four `auto` return 0 (`:591-593`), so
   "auto is modelled" is true only for the two gate branches.
3. **The declaration grammar's `exclusive` default is still `"auto"`** (`tools/mado-barfoot.py:633`:
   `exclusive = item.get("exclusive", "auto")`), while the protocol's default is 0
   (`S460:183`: "The default value is 0."). A plain client declared without the key reserves as if it
   were a bar; it must say `"exclusive": 0` explicitly. The round-80 §11 item-4 defect is therefore
   **still open**: the six new cases all
   declare `exclusive` explicitly (`overflow-tie-negative` `0`;
   `auto-dynamic-band-refused`/`auto-corner-edge`/`auto-all-four-edge`/`auto-parallel-edge`/
   `auto-left-dock` `"auto"`), so none pins the default, and this round changes no grammar.
4. **The overflow case is a synthetic fixture at a size the host does not have.** M1 is 1000×800 with
   a 1001-wide panel (`make-c1-cases-r81.py:18-33`, `:45-53`); the live host monitor is 3440 wide
   (`.ufo/waves/round-80/receipts/live-join-r80.txt:5`, `box=0,0,3440,26`). The case pins the
   arithmetic, not a host surface.
5. **A non-bar band is printed but not compared.** `attr` carries the whole attribution vector, but
   `reserved`/`band`/`expected` are computed for the bar's edge only (`tools/mado-barfoot.py:830-838`,
   `:848-854`). In `auto-left-dock` the fixture's `gt=0,26,0,0` carries no left band while
   `attr=40,26,0,0` does; `reserved=EQ` therefore certifies the top 26 only. The left 40 is a model
   prediction with no compositor counterpart in this case. Pinning the left edge would need a
   fixture whose `reserved` carries `40,26,0,0` and a verdict that compares a non-bar edge — neither
   exists yet.
6. **Zero and refused-by-the-gate are indistinguishable in the print.** Both produce `zone=0` and no
   `ATTR` row; the join does not say "the client sent 0" versus "the client's gate sends nothing"
   (`:591-592` versus an explicit `exclusive: 0` passed through `:566-567`).
7. **`0.14.0` versus the host's `0.14.2` is unverified** (§3). Everything in §2 is bound to the tag
   `v0.14.0`; if the patch release changed `round()`, the frozen case still reproduces the pinned
   source but no longer the host's binary.

## 8. Gate block

Two new registry rows, access date 2026-11-04, quotes verbatim from the committed pins (each ≤25
words). URLs are the upstream raw paths for the pinned tag/commit; this seat read
`fetch/S478.bin` / `fetch/S479.bin`, not the network.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S478 | hyprutils v0.14.0 — `src/math/Box.cpp` — https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.0/src/math/Box.cpp | code | A | mado composition: the coupled rounding of a box's origin and far edge, including an odd overflow past a negative tie (round-81 C1) | `CBox::round` :51-63 @ v0.14.0 (fetched 2026-11-04, sha256 `2d04de99ba977e5c3d99546606aede0d3eacc819049e16da5e0fd0d2004d083c`) | `double newW     = x + w - roundedX;` — the rounded width is the unrounded far edge minus the rounded origin, so both edges round and a negative half widens the box | mined | 2026-11-04 | on-release | `corpus/knowledge/bar-footprint-rounding-auto-r81.md` |
| S479 | Hyprland — `CMakeLists.txt` — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/CMakeLists.txt | code | A | mado composition: the hyprutils revision this Hyprland commit licenses (the pin behind S478's tag) | `set(HYPRUTILS_MINIMUM_VERSION 0.14.0)` :150 @ efb50993 (fetched 2026-11-04, sha256 `97b8028aa342cf6ee6f04b5db2e67e6e4fe6adf5d3fd67bad18005193db36516`) | `set(HYPRUTILS_MINIMUM_VERSION 0.14.0)` — a minimum-version licence (`hyprutils>=0.14.0`, :156), not a runtime equality | mined | 2026-11-04 | on-release | `corpus/knowledge/bar-footprint-rounding-auto-r81.md` |

## 9. Errata and same-round closures (append-only)

1. **§3/§7 item 7 are closed.** The host package is `hyprutils 0.14.2-1` (`pacman -Q hyprutils`), and
   `src/math/Box.cpp` at tag `v0.14.2` is **byte-identical** to the `v0.14.0` pin — sha256
   `2d04de99…`, `cmp` against `fetch/S478.bin` empty (S480, pinned at `fetch/S480.bin`). This does not
   turn S479 into an installed-version read: the pin licenses the tag, S480 shows the installed file's
   bytes are the model's bytes.
2. **§6 gains a limit the wave found.** Without `--rules` the join asserts a **zero** static reserve
   (`static_source=none`) instead of reading the host's `monitors.conf`. On this host the assertion
   happens to be right (no `addreserved` line anywhere under `~/.config/hypr/`; the only `monitor =`
   line carries no reserved field), but a default run is a claim the caller did not measure
   (`R81ScoutLive` §5.2).
3. **§5's live ceiling.** The `hyprctl layers -j` reply is already rounded (`fractional coords: []` on
   every `x/y/w/h`), so no live capture can show the pre-`round()` box; the rounding model is
   source-derived only (`R81ScoutLive` §5.3).
