# R81 scout — live recon on today's host (read-only)

Seat: `R81ScoutLive` · round 81 · lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`
Everything below is a reading of the live compositor or of committed bytes in the lane. No
compositor verb that changes state was issued (only `hyprctl monitors|layers|version|getoption`).

## 0. Provenance and instrument identity

Live compositor is the frozen commit itself, so today's boxes come from the same code the round
freezes:

```
$ hyprctl version
Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).
Date: Wed Aug 5 14:13:21 2026
$ echo "$HYPRLAND_INSTANCE_SIGNATURE"
efb50993780079460b0cbed1363e2166a2de1d9f_1793632040_1005787507
```

`efb50993…` is the pin of `.ufo/waves/round-80/fetch/S470.bin` (Hyprland `src/render/Renderer.cpp`)
and of `.ufo/waves/round-81/fetch/S479.bin` (Hyprland `CMakeLists.txt`).

```
$ pacman -Q hyprutils hyprland
hyprutils 0.14.2-1
hyprland 0.56.2-4
$ grep -n HYPRUTILS_MINIMUM_VERSION .ufo/waves/round-81/fetch/S479.bin
150:set(HYPRUTILS_MINIMUM_VERSION 0.14.0)
```

`S478.bin` is hyprutils **v0.14.0** `src/math/Box.cpp`; the host carries **0.14.2**. The
`CBox::round` body quoted in §4 is the v0.14.0 file. **[GAP]** the 0.14.2 `Box.cpp` bytes were not
opened, so "the host's `round()` is byte-identical to S478" is *not* claimed here — only
`0.14.2 ≥ 0.14.0`, which is the constraint S479:150 imposes.

Instrument identity (frozen tool, not rewritten):

```
$ sha256sum tools/mado-barfoot.py
a129a435572805c3ae7730714f0dafdea2b9a7e420f53f0d109dc2d5f57d1230  tools/mado-barfoot.py
$ python3 -I tools/mado-barfoot.py --selftest
MADO_BARFOOT_SELFTEST: 121/121
```

`a129a435…` is the frozen `r81-v1` digest, and the selftest count matches the declared 121/121.

## 1. Capture, redaction, and the join

### 1.1 Capture and redaction

```
$ hyprctl monitors -j > monitors.raw.json   # rc=0
$ hyprctl layers  -j > layers.raw.json      # rc=0
```

`monitors.raw.json` was rewritten field-by-field, preserving key order, with
`description`, `serial`, `make`, `model` replaced by `<redacted: <field>>`; nothing else was
touched. Saved, byte-stable, in the seat directory:

| file | bytes | sha256 |
|---|---|---|
| `monitors.redacted.json` | 1343 | `82c01435afb9ab98e77d37f19ef3698f0cb671aea571cfde5c3871bb4026d013` |
| `layers.raw.json` | 748 | `46eb2481ed664862c53c93f76e52cee31753519c4e0587af5d5928c73fd6f53c` |

```
$ grep -n -E '508AZFMF7323|LG Electronics|ULTRAWIDE' monitors.redacted.json
leak_grep_rc=1
$ grep -n -E 'redacted|description|serial|"make"|"model"' monitors.redacted.json
5:  "description": "<redacted: description>",
6:  "make": "<redacted: make>",
7:  "model": "<redacted: model>",
8:  "serial": "<redacted: serial>",
```

No vendor string survives the redaction (grep rc=1), and `layers.raw.json` carries no identity
field at all (its key set is listed in §5.1).

### 1.2 Flag set used — and why

**`--config --layers --monitors` only. No `--surfaces`. No `--rules` in the primary run.**
`--monitor` was omitted because the capture carries exactly one monitor, which the tool
auto-selects (`tools/mado-barfoot.py:1454-1459`).

`--surfaces` was **not** added: the `hyprctl layers -j` reply carries the *arranged* box only —
`address, alpha, h, namespace, pid, w, x, y`, with `level` present only as the enclosing dict key
(§5.1). `parse_surfaces` (`tools/mado-barfoot.py:604-663`) requires a *declared* `anchor`,
`exclusive`, `margins` and `order` per surface; none of those is observable in the reply, and the
live stack has no extra panel surface to declare (level 1 and level 3 are both `entries 0`,
§2). Building a surfaces file from this capture would have meant inventing the very declaration
the composition model is supposed to check against. So the single-surface path was used, and the
composition path (auto-zone gate, overflow rounding of extras) is exercised only by the frozen
cases, not by today's host.

### 1.3 The join

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py \
    --monitors /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/w1/R81ScoutLive/monitors.redacted.json \
    --layers   /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/w1/R81ScoutLive/layers.raw.json \
    --config   /home/vgpnk/.config/waybar/config.jsonc
MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=26 width=0 margins=0,0,0,0 exclusive=true
MADO_BARFOOT_STATIC: monitor=DP-1 top=0 right=0 bottom=0 left=0 source=none
MADO_BARFOOT_DECL: monitor=DP-1 box=0,0,3440,26 edge=top
MADO_BARFOOT_LIVE: monitor=DP-1 level=2 ns=waybar box=0,0,3440,26 entries=1
MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
rc=0
```

(The single-surface path emits one `DECL` row — the composition path would emit one per declared
surface.)

Cross-check with the host's monitor rules handed to the tool explicitly:

```
$ python3 -I …/tools/mado-barfoot.py --monitors …/monitors.redacted.json --layers …/layers.raw.json \
    --config /home/vgpnk/.config/waybar/config.jsonc --rules /home/vgpnk/.config/hypr/monitors.conf
MADO_BARFOOT_STATIC: monitor=DP-1 top=0 right=0 bottom=0 left=0 source=rules
MADO_BARFOOT_DECL: monitor=DP-1 box=0,0,3440,26 edge=top
MADO_BARFOOT_LIVE: monitor=DP-1 level=2 ns=waybar box=0,0,3440,26 entries=1
MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
rc=0
```

Both receipts are kept in the seat directory (`join-live-receipt.txt`,
`join-live-rules-receipt.txt`).

The declaration the join read, verbatim from the config:

```
$ grep -n -E '^  "(layer|position|height)"' /home/vgpnk/.config/waybar/config.jsonc
3:  "layer": "top",
4:  "position": "top",
6:  "height": 26,
$ grep -n '"width"' /home/vgpnk/.config/waybar/config.jsonc
rc=1
```

No bar-level `width` key at all → `width=0` in the `CONFIG` row, i.e. the auto/full-width branch.

## 2. Live layer census

`hyprctl layers -j`, monitor `DP-1` (3440×1440 at 0,0, scale 1, transform 0 — so the join's
scale/transform precondition holds):

| level | namespace | box (x,y,w,h) | alpha | pid | pid count |
|---|---|---|---|---|---|
| 0 | `wallpaper` | `0,0,3440,1440` | 1 | 1722 | 1 |
| 1 | — | `entries 0` | — | — | 0 |
| 2 | `waybar` | `0,0,3440,26` | 1 | 1720 | 1 |
| 3 | — | `entries 0` | — | — | 0 |

```
monitor DP-1 level 0 entries 1
   ns=wallpaper box=0,0,3440,1440 alpha=1 pid=1722
monitor DP-1 level 1 entries 0
monitor DP-1 level 2 entries 1
   ns=waybar box=0,0,3440,26 alpha=1 pid=1720
monitor DP-1 level 3 entries 0
```

Two surfaces, one pid each, two distinct pids. Ownership confirmed against `/proc`:

```
$ for p in 1720 1722; do echo -n "pid $p: "; cat /proc/$p/comm; done
pid 1720: waybar
pid 1722: swaybg
$ pgrep -x waybar | wc -l
count=1
```

So the bar is a single waybar process (pid 1720) at the `top` layer (level 2), and the level-0
full-monitor surface is the wallpaper daemon, not a bar.

## 3. Does the bar's box match the declared `height`/`position`?

**Yes — `box=MATCH`.** Declared `position=top`, `height=26`, no margins, no width →
`DECL box=0,0,3440,26`; live `box=0,0,3440,26`. The whole monitor width, flush to `y=0`, 26 px
tall: exactly the declared edge and the declared height, with no residual offset.

The exclusive zone agrees too: the monitor's `reserved` is `[0,26,0,0]`, and the join maps
`top` to index 1 (`RESERVED_INDEX = {"left": 0, "top": 1, "right": 2, "bottom": 3}`,
`tools/mado-barfoot.py:116`), reading `band=26` against `expected=26` → `reserved=EQ`. The bar's
declared height is *also* the band it reserves, so the top 26 px of the 1440-px monitor are
excluded from the usable area and the composition is self-consistent on this host.

## 4. Can today's live boxes reach the negative-tie class?

### 4.1 The two frozen bodies

`CBox::round`, `.ufo/waves/round-81/fetch/S478.bin:51-63` (hyprutils v0.14.0):

```cpp
51| CBox& Hyprutils::Math::CBox::round() {
52|     double roundedX = std::round(x);
53|     double roundedY = std::round(y);
54|     double newW     = x + w - roundedX;
55|     double newH     = y + h - roundedY;
56| 
57|     x = roundedX;
58|     y = roundedY;
59|     w = std::round(newW);
60|     h = std::round(newH);
61| 
62|     return *this;
63| }
```

`IHyprRenderer::arrangeLayerArray`, `.ufo/waves/round-80/fetch/S470.bin:2587-2671`, the horizontal
placement and the round call:

```cpp
2610|         if (box.width == 0)
2611|             box.x = bounds.x;
2612|         else if ((PSTATE->anchor & both_horiz) == both_horiz)
2613|             box.x = bounds.x + ((bounds.width / 2) - (box.width / 2));
...
2635|         if (box.width == 0) {
2636|             box.x += PSTATE->margin.left;
2637|             box.width = bounds.width - (PSTATE->margin.left + PSTATE->margin.right);
...
2660|         box.round(); // fix rounding errors
```

The class needs a **half-integer, negative** `x` before line 2660: `std::round(-0.5)` is `-1`
(away from zero), and the width was already re-derived from the un-rounded right edge at line 54,
so `w` grows by one. Frozen case replayed through the tool's own model:

```
frozen class replay: {'x': -1, 'y': 363, 'w': 1002, 'h': 100}
```

### 4.2 Today's geometry

`bounds` for a top bar is the usable box: `bounds.x = 0`, `bounds.width = 3440`, margins all 0.
With the host's declaration (`width=0`, i.e. absent) the **first** branch is taken and the
centring branch is unreachable:

- `box.width == 0` → `box.x = bounds.x = 0`; then `box.width = 3440 − 0 = 3440`. Both integers;
  `round()` is the identity. Live box `0,0,3440,26` is that identity.
- The centring branch is only reached with a declared width, and then
  `box.x = (3440 − w)/2`. It is **negative and half-integral** only when `w > 3440` *and*
  `(3440 − w)` is odd, i.e. `w ∈ {3441, 3443, 3445, …}`.

Evaluated through `cbox_round` at `MON_W=3440` (`tools/mado-barfoot.py:498`):

```
  decl_w=   0 width==0 branch    pre=(x=0.0 w=3440.0) -> post=(x=0 w=3440) right_edge=3440
  decl_w=3439 both_horiz centre  pre=(x=0.5 w=3439.0) -> post=(x=1 w=3439) right_edge=3440
  decl_w=3440 both_horiz centre  pre=(x=0.0 w=3440.0) -> post=(x=0 w=3440) right_edge=3440
  decl_w=3441 both_horiz centre  pre=(x=-0.5 w=3441.0) -> post=(x=-1 w=3442) right_edge=3441  OVERFLOW
  decl_w=3443 both_horiz centre  pre=(x=-1.5 w=3443.0) -> post=(x=-2 w=3444) right_edge=3442  OVERFLOW
  decl_w=3445 both_horiz centre  pre=(x=-2.5 w=3445.0) -> post=(x=-3 w=3446) right_edge=3443  OVERFLOW
```

**Answer: no — today's live boxes cannot reach the negative-tie class.** The host's bar width is
the monitor width: the config declares no `width` key at all (grep rc=1), so the compositor takes
the `box.width == 0` branch and `box.x` is the integer `bounds.x = 0`; and the live reply confirms
`w=3440` against a `3440`-px monitor, a difference of exactly 0. The negative tie is only produced
by the centring branch with `w` odd and **greater** than the monitor width (`3441`, `3443`, …), a
declaration this host never makes. The odd-width *under*-monitor case (`w=3439`) lands in the
positive-half class instead and keeps `right_edge=3440` — no overflow.

Two further facts constrain it in practice:

- `hyprctl layers -j` prints post-`round()` integers: `fractional coords: []`. Even if a
  half-integer were computed, a live capture could only show its **shadow** (`x=-1, w=3442`), never
  the pre-round value — so the class is unobservable live by construction, and its frozen cases
  stay the only direct witnesses.
- The vertical axis is equally integral here (`y=0`, `h=26`; `box.height ≠ 0` and the top anchor
  takes `box.y = bounds.y`), so no half-integer can arise from the other axis either.

## 5. Two limits of the live join

### 5.1 Limit 1 — `--surfaces` is underivable from live bytes, so the composition half of the claim cannot be exercised on this host

```
$ python3 -c "import json; d=json.load(open('…/layers.raw.json')); print(sorted({k for m in d.values() for lv in m['levels'].values() for s in lv for k in s}))"
union of keys: ['address', 'alpha', 'h', 'namespace', 'pid', 'w', 'x', 'y']
```

There is no `anchor`, no `exclusive`, no `margins`, no `exclusiveEdge`, no `order`, and no
per-surface `level` — only the final box, alpha, namespace, pid. `parse_surfaces`
(`tools/mado-barfoot.py:604-663`) demands exactly those declared fields, and `surface_zone`
(`:559`) exists to model the `auto` gate on them. Consequently a `--surfaces` file for this
capture can only be *written by hand*, i.e. the auto-zone gate (`auto-dynamic-band-refused`,
`auto-corner-edge`, `auto-all-four-edge`, `auto-parallel-edge`, `auto-left-dock`) and the overflow
rounding of extra surfaces are checked against frozen declarations, never against today's
compositor. The live stack also offers nothing to declare: levels 1 and 3 are `entries 0`.

### 5.2 Limit 2 — the `reserved` check is an aggregate, and its static term is an assumption in the default invocation

```
$ python3 -I …/mado-barfoot.py --monitors … --layers … --config /home/vgpnk/.config/waybar/config.jsonc
MADO_BARFOOT_STATIC: monitor=DP-1 top=0 right=0 bottom=0 left=0 source=none
MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN
$ python3 -I …/mado-barfoot.py … --rules /home/vgpnk/.config/hypr/monitors.conf
MADO_BARFOOT_STATIC: monitor=DP-1 top=0 right=0 bottom=0 left=0 source=rules
MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN
$ grep -rn 'addreserved' /home/vgpnk/.config/hypr/
grep_rc=1
```

`expected` is `static[edge] + contribution` (`:985-986`), and unless `--rules` is passed `static` is
`ZERO_STATIC` with `static_source="none"` (`:1460-1462`). On this host that assumption happens to
be right — `grep` finds no `addreserved` anywhere under `~/.config/hypr/` (rc=1) and the host's
`monitors.conf` only carries `monitor = DP-1, 3440x1440@100, 0x0, 1`, which the rules parser
reduces to a zero static reserve — so the two runs agree. But the default run *never read the
host rules*: it asserted zero. And `band` is a single integer per edge that sums the static area
with **every** exclusive surface on that edge, so the join can prove "26 px are reserved on top",
not "26 px are reserved *because of waybar*". A second top-exclusive surface would surface as
`reserved=GT`, i.e. as a mismatch, not as an attribution.

### 5.3 Additional observed limit — the reply is already rounded

`fractional coords: []` on every `x/y/w/h` in the capture. The join can therefore never observe
the pre-`round()` box that §4 is about; it verifies the post-round result only. This is not a
defect of the instrument (it models `CBox::round` from source instead), but it is a hard ceiling
on what *live* evidence can say about rounding.

## 6. Remaining unknowns

- **[GAP]** hyprutils `0.14.2`'s `src/math/Box.cpp` was not opened; the `round()` body quoted is
  v0.14.0's. The host runs 0.14.2, which satisfies S479:150's `>= 0.14.0`, but byte-identity with
  S478 is unverified.
- **[GAP]** one capture instant. Nothing here says the arrangement is stable across a workspace
  switch, a bar reload, or a scale/transform change; the join would refuse the latter two anyway
  (`evaluate`, `:921-924`: scale/transform must be `1`/`0`).
- **[INFERENCE]** `swaybg`'s level-0 surface has no exclusive zone (it does not appear in the
  26 px band and the band matches the bar's height exactly); the reply carries no `exclusive`
  field, so this is inferred from the band arithmetic, not read.

STATUS: ok
