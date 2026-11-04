# R81ScribeEntry — findings

Seat: R81ScribeEntry (leaf; no subagent dispatch). Lane root:
`/home/vgpnk/Projects/shokunin/mado-shokunin`. All paths absolute or lane-relative from the lane root.
cwd of every shell call was the lane root (the persisted shell reports fleet root; every command
below names its path or `cd`s first). No file outside the lane's round-81 seat dir, my scratch dir,
and the one report path was written.

## 1. Deliverable and what it says

**`entry-draft.md`** (seat dir) — C1 knowledge entry draft in the r80 shape: `source:` / `verified-at:`
/ `recheck:` header, then §1 what it is, §2 `CBox::round` coupled (quote `S478:51-63` line by line,
derive `x=-1, w=1002`, show the floor-divided `0/1001`), §3 hyprutils revision class, §4 the auto-zone
gate and the refusal, §5 the gate's composition consequence (including the left dock), §6 the
DECL/ATTR/RESULT fields, §7 seven limits, §8 the two SOURCES rows (S478, S479).

Behavior claims, each backed in the draft by a file:line:

- `CBox::round` rounds the origin then `round(x + w - roundedX)`; a 1001-wide panel on a 1000-wide
  bounds gives unrounded `x=-0.5`, `round(-0.5)=-1`, `w=round(1001.5)=1002`
  (`fetch/S478.bin:51-63`, `Renderer.cpp:2613`, `:2660`).
- The r80 integer centring `(bounds.size - size + 1) // 2` gives `0//2=0` → `0/1001`
  (`bar-footprint-composition-r80.md:193`, base tool at `c702094a…:503`).
- The auto zone is the client's, from `current_allocation`, gated on
  `anchors[LEFT]==anchors[RIGHT]` / `anchors[TOP]==anchors[BOTTOM]`
  (`fetch/S464.bin:264-292`, allocation assignment `:304-313`).
- Corner/parallel/all-four send no zone; `exclusiveEdge` is only consulted after the positive-zone
  guard (`Renderer.cpp:2531-2533`, `:2575`; protocol repeats it at `S460:159-163`, default 0 at `:183`).
- `auto-left-dock` puts 40 on the left attribution vector; the bar starts at x=40
  (`attr=40,26,0,0`, `reserved=EQ` for the top edge).
- The declaration grammar still defaults `exclusive` to `"auto"` (`tools/mado-barfoot.py:633`) while
  the protocol default is 0 (`S460:183`) — the r80 §11 item-4 defect remains open.

## 2. Evidence runs (exact argv and material output)

All shell rows: `cd /home/vgpnk/Projects/shokunin/mado-shokunin` first (shown once as `[cd]`), and
only lane paths are read. The scratch root was `/fast/scratch/hyaku/mado-r81/R81ScribeEntry`.

### 2.1 Byte pins and hashes

```
[cd] sha256sum .ufo/waves/round-81/fetch/S478.bin .ufo/waves/round-81/fetch/S479.bin
2d04de99ba977e5c3d99546606aede0d3eacc819049e16da5e0fd0d2004d083c  .ufo/waves/round-81/fetch/S478.bin
97b8028aa342cf6ee6f04b5db2e67e6e4fe6adf5d3fd67bad18005193db36516  .ufo/waves/round-81/fetch/S479.bin

[cd] cat .ufo/waves/round-81/fetch/sha256-r81.txt
2d04de99ba977e5c3d99546606aede0d3eacc819049e16da5e0fd0d2004d083c  S478.bin
97b8028aa342cf6ee6f04b5db2e67e6e4fe6adf5d3fd67bad18005193db36516  S479.bin

[cd] sha256sum <(git show 0e2ccd2a8692825cac534f57246053b276be9f13:tools/mado-barfoot.py)
a129a435572805c3ae7730714f0dafdea2b9a7e420f53f0d109dc2d5f57d1230  /dev/fd/63
[cd] sha256sum tools/mado-barfoot.py
a129a435572805c3ae7730714f0dafdea2b9a7e420f53f0d109dc2d5f57d1230  tools/mado-barfoot.py
```
(The first command was actually run as `git show 0e2ccd2a…:tools/mado-barfoot.py | sha256sum`; same
bytes.) Freeze bytes equal the worktree instrument, so the draft's `verified-at` pin is real.

### 2.2 Line pins used by the draft

```
[cd] grep -n "CBox::round\|roundedX\|newW\|newH\|w = std::round\|h = std::round" .ufo/waves/round-81/fetch/S478.bin
51:CBox& Hyprutils::Math::CBox::round() {
52:    double roundedX = std::round(x);
54:    double newW     = x + w - roundedX;
55:    double newH     = y + h - roundedY;
57:    x = roundedX;
59:    w = std::round(newW);
60:    h = std::round(newH);

[cd] grep -n "HYPRUTILS_MINIMUM_VERSION\|hyprutils_dep" .ufo/waves/round-81/fetch/S479.bin
150:set(HYPRUTILS_MINIMUM_VERSION 0.14.0)
156:pkg_check_modules(hyprutils_dep REQUIRED IMPORTED_TARGET hyprutils>=${HYPRUTILS_MINIMUM_VERSION})

[cd] grep -n "auto_exclusive_zone\|gboolean horiz\|gboolean vert\|new_exclusive_zone\|current_allocation\|margins\[GTK_LAYER_SHELL_EDGE" .ufo/waves/round-79/fetch/S464.bin
264:layer_surface_update_auto_exclusive_zone (LayerSurface *self)
269:    gboolean horiz = (self->anchors[GTK_LAYER_SHELL_EDGE_LEFT] ==
271:    gboolean vert = (self->anchors[GTK_LAYER_SHELL_EDGE_TOP] ==
273:    int new_exclusive_zone = -1;
276:        new_exclusive_zone = self->current_allocation.height;
282:        new_exclusive_zone = self->current_allocation.width;
289:    if (new_exclusive_zone >= 0 && self->exclusive_zone != new_exclusive_zone) {
304:    if (self->current_allocation.width != allocation->width ||
313:        layer_surface_update_auto_exclusive_zone (self);
```
The full function body was read with `read .ufo/waves/round-79/fetch/S464.bin:260-296:raw`; every
quoted line in the draft is verbatim from it.

```
[cd] sed -n '263,268p;300,316p' .ufo/waves/round-79/fetch/S464.bin | cat -n
     1  static void
     2  layer_surface_update_auto_exclusive_zone (LayerSurface *self)
     3  {
     4      if (!self->auto_exclusive_zone)
     5          return;
...
     7      if (self->current_allocation.width != allocation->width ||
     8          self->current_allocation.height != allocation->height) {
    10          self->current_allocation = (GtkRequisition) {
    11              .width = allocation->width,
    12              .height = allocation->height,
...
    17          layer_surface_update_auto_exclusive_zone (self);
```

```
[cd] grep -n "if (exclusive <= 0)\|exclusiveEdge == edges\|singular_anchor\|anchor_triplet\|exclusive + edges" .ufo/waves/round-80/fetch/S470.bin
2531:    if (exclusive <= 0) {
2535:        uint32_t singular_anchor;
2536:        uint32_t anchor_triplet;
2575:        if ((exclusiveEdge == edges[i].singular_anchor || anchor == edges[i].singular_anchor || anchor == edges[i].anchor_triplet) && exclusive + edges[i].margin > 0) {

[cd] grep -n "bounds.width / 2\|box.round()\|arrangeLayerArray" .ufo/waves/round-80/fetch/S470.bin
2587:void IHyprRenderer::arrangeLayerArray(...)
2613:            box.x = bounds.x + ((bounds.width / 2) - (box.width / 2));
2660:        box.round(); // fix rounding errors
2682:    const CBox ORIGINAL_USABLE_AREA = PMONITOR->logicalBoxMinusReserved();
2696:    PMONITOR->m_reservedArea.addType(Desktop::RESERVED_DYNAMIC_TYPE_LS, Desktop::CReservedArea{ORIGINAL_USABLE_AREA, usableArea});

[cd] grep -n "bounds.height / 2" .ufo/waves/round-80/fetch/S470.bin
2626:            box.y = bounds.y + ((bounds.height / 2) - (box.height / 2));
2632:            box.y = bounds.y + ((bounds.height / 2) - (box.height / 2));
```
The `:2632` one is the no-vertical-anchor `else` branch, which is the panel's branch (anchors
left|right only); the draft uses it for `y=363`.

```
[cd] grep -n "The default value is 0" .ufo/waves/round-79/fetch/S460.bin
183:        The default value is 0.
[cd] sed -n '159,163p' .ufo/waves/round-79/fetch/S460.bin
        A positive value is only meaningful if the surface is anchored to one
        edge or an edge and both perpendicular edges. If the surface is not
        anchored, anchored to only two perpendicular edges (a corner), anchored
        to only two parallel edges or anchored to all edges, a positive value
        will be treated the same as zero.
```

### 2.3 The instrument's fields and code points

```
[cd] grep -n "MADO_BARFOOT_DECL\|MADO_BARFOOT_ATTR\|MADO_BARFOOT_RESULT" tools/mado-barfoot.py
787:        rows.append(("DECL", "monitor=%s level=%d ns=%s box=%d,%d,%d,%d anchor=%s zone=%d"
807:                rows.append(("ATTR", "monitor=%s level=%d ns=%s edge=none contribution=0"
813:                rows.append(("ATTR", "monitor=%s level=%d ns=%s edge=%s contribution=%d box=%d,%d,%d,%d"
848:    rows.append(("RESULT", "monitor=%s box=%s boxes=%s reserved=%s band=%d expected=%d "

[cd] grep -n "def std_round\|def cbox_round\|def surface_zone\|def zone_for_pass\|exclusive = item.get\|if horiz and not vert\|if vert and not horiz\|gtk-layer-shell sends no zone\|band = mon\[\"reserved\"\]" tools/mado-barfoot.py
493:def std_round(value):
498:def cbox_round(box):
559:def surface_zone(spec):
571:    if horiz and not vert:
581:    if vert and not horiz:
591:    # gtk-layer-shell sends no zone for a corner, a parallel pair or all four anchors
633:        exclusive = item.get("exclusive", "auto")
804:        if zone > 0:
830:    band = mon["reserved"][RESERVED_INDEX[edge]]
```
`sed -n '784,816p'`/`'836,856p'`/`'791,804p'` located the exact rows cited in the draft:
DECL `:787-789`, LIVE `entries=0` `:792-794`, LIVE `entries=1` `:800-802`, ATTR `:804-815`
(`edge=none` `:807-808`), `bar_box`/verdict `:839-845`, vector `:846-847`, RESULT `:848-854`.
`sed -n '620,628p'` located the anchor default `:625-627`; `sed -n '594,604p'` located
`zone_for_pass` `:595-602`; `sed -n '1470,1478p'` located the model error `:1474-1476`.

### 2.4 Frozen cases and receipt

```
[cd] cat .ufo/waves/round-81/receipts/measurement-c1-r81.txt
...
MADO_R81_BASE: correct=33/39 rule=held-r79-model(no-multi-surface-arrangement) base_rev=c702094ace5dd9b2b5e152951b4b2f4dd578f8b6 base_sha256=5b9e2930005e1081454f46b8ba32deba4ba4ba81851482f90ce561926b42f0d9
MADO_R81_CONTROL: sha256=ab8154a1d4bc5d2a0f58bef8aeb675605e50ecfe932406b39b0a0c2df0533d52 carried=33/33
MADO_R81_BARFOOT: cases=39 correct=39 mutants=28 killed=28 base_correct=33/39 carried=33/33 tool_selftest=121/121 verdict=TARGET_MET rev=0e2ccd2a8692825cac534f57246053b276be9f13 tool_sha256=a129a435572805c3ae7730714f0dafdea2b9a7e420f53f0d109dc2d5f57d1230
```

Case-name lines in the frozen control (`grep -n '"name": …'`):
`overflow-tie-negative` 2103, `auto-dynamic-band-refused` 2175, `auto-corner-edge` 2253,
`auto-all-four-edge` 2337, `auto-parallel-edge` 2423, `auto-left-dock` 2508; case blocks
2035–2525, overflow's surface block 2104–2117.

### 2.5 The six new cases through the frozen instrument

Driver argv (one subprocess per case, files written under scratch):

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py \
  --config <scratch>/<case>/config.json --layers <scratch>/<case>/layers.json \
  --monitors <scratch>/<case>/monitors.json --monitor M1 \
  [--surfaces <scratch>/<case>/surfaces.json]
```
(exact tool path was `<lane>/tools/mado-barfoot.py`; surfaces passed as `{"surfaces": [...]}`).
Captured verbatim into `.ufo/waves/round-81/w1/R81ScribeEntry/join-six-cases.txt`; the load-bearing
lines:

```
### case=overflow-tie-negative rc=0
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=-1,363,1002,100 anchor=left+right zone=0
MADO_BARFOOT_LIVE: monitor=M1 level=3 ns=panel box=-1,363,1002,100 entries=1
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN

### case=auto-dynamic-band-refused rc=3
MADO_BARFOOT: ERROR (stage=model auto zone on a dynamic height (0) is the client's allocation, not a declared value)

### case=auto-corner-edge rc=0
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=0,26,200,100 anchor=top+left zone=0
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN

### case=auto-all-four-edge rc=0
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=400,363,200,100 anchor=top+bottom+left+right zone=0

### case=auto-parallel-edge rc=0
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=400,363,200,100 anchor=top+bottom zone=0

### case=auto-left-dock rc=0
MADO_BARFOOT_DECL: monitor=M1 level=1 ns=dock box=0,0,40,800 anchor=left zone=40
MADO_BARFOOT_ATTR: monitor=M1 level=1 ns=dock edge=left contribution=40 box=0,0,40,800
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=40,0,960,26 anchor=top+left+right zone=26
MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=waybar edge=top contribution=26 box=40,0,960,26
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=40,26,0,0 ls=VALID verdict=CLEAN
```
The three no-zone panels produce **no** ATTR row (zone 0 skips the block).

### 2.6 The base instrument over all 39 cases (do-nothing control reproduction)

First attempt (disclosed because it was wrong): the harness omitted `--rules`, so it mis-scored the
five `static-*` cases and printed `BASE_TOTAL: correct=28/39`. The frozen counter's `run_cases`
writes and passes the rules file; with `--rules <case>/rules.conf` added the run reads:

```
BASE_TOTAL: correct=33/39
carried-ok: 33/33 new-ok: 0/6
```
Full matrix: `.ufo/waves/round-81/w1/R81ScribeEntry/base-39-matrix.txt`. Base failure modes, quoted
from the base tool run:

```
overflow-tie-negative:      boxes=MATCH,DIFFER   (rc 1; the 0/1001 panel box)
auto-dynamic-band-refused:  verdict=CLEAN        (rc 0; no refusal)
auto-corner-edge:           ATTR panel edge=top contribution=100 ; expected=126 (rc 1)
auto-left-dock:             boxes=DIFFER,DIFFER  (rc 1)
```
So the receipt's `base_correct=33/39` is exactly "carried 33 / new 0".

### 2.7 Host version read

```
pacman -Q hyprutils hyprland
hyprutils 0.14.2-1
hyprland 0.56.2-4
```
Read-only query; no pacman transaction was run.

## 3. Findings (including two things the L1 should decide)

1. **The counter's base-rule label is not what the bytes are.** The receipt prints
   `rule=held-r79-model(no-multi-surface-arrangement)`, but `git show
   c702094ace5dd9b2b5e152951b4b2f4dd578f8b6:tools/mado-barfoot.py` contains
   `VERSION = "r80-v1"` (line 85) and `def evaluate_composition` (line 652). The base score 33/39 is
   the **r80 composition tool**, not a no-composition r79 model. The draft states the bytes and calls
   the label the counter's; the counter itself is frozen, so this is a note for the L1, not an edit.
2. **A non-bar band is printed but never compared.** `RESULT.reserved` is computed only for the bar's
   edge (`tools/mado-barfoot.py:830-838`). In `auto-left-dock` the join prints
   `gt=0,26,0,0 attr=40,26,0,0` — the left 40 has no compositor counterpart in the fixture, and
   `reserved=EQ` certifies only the top 26. The draft records this as limit 5. If the round wants the
   left edge certified, the fixture's `reserved` must carry `40,26,0,0` and the verdict must compare a
   non-bar edge; neither exists.
3. **The host's hyprutils is 0.14.2-1, not 0.14.0.** The pinned S478 is tag `v0.14.0`, licensed by
   `HYPRUTILS_MINIMUM_VERSION 0.14.0` (a `>=` pin). Whether `CBox::round` changed in the two patch
   releases is `[UNK]`; the draft says so and names what would settle it (the `v0.14.2` `Box.cpp`).
   This supersedes the statement in the pre-existing untracked corpus draft
   `corpus/knowledge/bar-footprint-rounding-auto-r81.md` ("The host's installed hyprutils package
   version was not read this round") — it was read this seat, by package query.
4. **A sibling draft already sits at `corpus/knowledge/bar-footprint-rounding-auto-r81.md`** (untracked;
   not written or edited by this seat). This seat's `entry-draft.md` is the assigned deliverable; it
   differs from that draft by (a) the 0.14.2 host read, (b) the protocol quote at `S460:159-163`,
   (c) the base-label/bytes mismatch at `c702094a…:85`, (d) the §6 declared-field summary and the
   `edge=none`-is-a-different-shape distinction, (e) limit 5 (the left 40 has no GT). The L1 should
   pick one text before integration; the gate rows below name that path as the used-by target.
5. **The overflow case is arithmetic, not a host capture.** The 1000×800 M1 and 1001-wide panel are
   generated fixtures (`make-c1-cases-r81.py:18-28`, `:45-53`); the live monitor is 3440 wide
   (`live-join-r80.txt:5`). The match certifies the model against source-derived expectations, not a
   host surface.
6. **Nothing was refused that should have been reserved.** The three auto-refused anchor classes do
   send no zone at the client (`S464:269-288`) and the protocol treats a positive zone on those sets
   as zero (`S460:159-163`), so the join's `zone=0` is the source's behaviour, not a gap; the gap is
   only the dynamic-band refusal, which is named.

## 4. Out of scope / not run

- The full 39-case counter was **not** re-run by this seat; the freeze receipt
  (`measurement-c1-r81.txt`) is the measured evidence, and this seat re-ran only the six new cases
  through the frozen tool plus the base tool over all 39.
- The 28 mutants were not re-run; the receipt records `mutants=28 killed=28`.
- The tool selftest was not re-run; the receipt records `tool_selftest=121/121`, and the freeze hash
  equality above shows the bytes are the same instrument.
- No network fetch; no `hyprctl`; no layer surface created; no compositor verb.
- No git/jj mutation. `git show`, `git log`, `git status --porcelain` only (read-only).
- No pacman transaction (package query only), no installs.

## 5. Artifact paths

- `.ufo/waves/round-81/w1/R81ScribeEntry/entry-draft.md` — the entry draft (primary deliverable).
- `.ufo/waves/round-81/w1/R81ScribeEntry/join-six-cases.txt` — frozen tool over the six new cases.
- `.ufo/waves/round-81/w1/R81ScribeEntry/base-39-matrix.txt` — base tool over all 39 cases.
- `.ufo/waves/round-81/w1/R81ScribeEntry.md` — this report.
- Scratch `/fast/scratch/hyaku/mado-r81/R81ScribeEntry` — removed after copying the two receipts.

## 6. Cleanup and a scratch observation

```
[cd] rm -rf -- /fast/scratch/hyaku/mado-r81/R81ScribeEntry
[cd] ls /fast/scratch/hyaku/mado-r81/
Box-v0.14.2.cpp
R81ConnSiblings
R81ExecMutants
c2-pre-fix-strip.py
controls.sh
l1
live
sandbox
tip.sh
```
My own scratch directory is gone; the entries listed belong to other seats. `Box-v0.14.2.cpp` is a
sibling's scratch artifact, not this seat's: scratch is never citable, so the draft keeps the
`v0.14.0` versus `0.14.2` question as `[UNK]` (§3 of the draft, limit 7). If that sibling commits a
v0.14.2 pin, the L1 can close the `[UNK]` from the committed bytes; this seat does not use it.

STATUS: ok
