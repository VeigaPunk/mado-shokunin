# R79ScoutModel — the static-reserve composition: source reconnaissance

Seat: scout (read-only). Round 79, wave 1. No repo write, no git/jj mutation, no host write.
Every "observed" line below is a command output or pinned file byte; every "source-derived"
line is an arithmetic consequence of the cited code, not a live compositor observation.

## 0. State of the lane while this seat ran (facts)

- Frozen tool in the declaration: `sha256 c9aa139152643020acf27b5aef8026ae5b8a5f70372e86abb4a032c82bed86de`,
  blob of `tools/mado-barfoot.py` at rev `5eb8f20fe291603c74973fa94cc55723ac8089a4` (verified with
  `git show 5eb8f20:tools/mado-barfoot.py | sha256sum`).
- The tool changed under this seat. Lane HEAD at close: `8696c4ddf35223d69c0558603e110bc0f6263c4b`
  (2026-11-04 07:37:02, "scorecard and log at the repaired measurement"); HEAD's blob is
  `673ac44d176ce2dd63701c6db6f3f1116ed059cc62d9000c6e57423341c60f99`, introduced by
  `d6be05ef` ("repair R1: an addreserved with no prior rule drops its area"). The diff touches
  only `parse_static_reserve`'s `addreserved` slot, the docstring and the selftest. The four
  attack sites in §4 are byte-unchanged by that repair, and every probe below was re-run at
  `673ac44d`.
- C1 re-run at HEAD with the declared counting command (read-only; scratch only):
  `cases=23 correct=23 mutants=12 killed=12 base_correct=18/23 carried=18/18
  tool_selftest=44/44 verdict=TARGET_MET rev=8696c4dd tool_sha256=673ac44d`. Control-set sha
  `108bde32…` (the declaration's `5f7ebb3c…` belongs to the pre-repair set at `5eb8f20`).
- `fetch/S466.bin` is byte-identical to `fetch/S459.bin` (`0a52e145…`, 3339 B): the same
  `src/desktop/reserved/ReservedArea.cpp` at the same commit. S466's new evidence is its
  anchors (`calculate`/`setStatic`/`addType`), not new bytes.
- The legacy ConfigManager bytes are not in `fetch/`. S303 pins the anchors
  (`Hyprland-legacy-ConfigManager.cpp:1293-1387`). This seat re-fetched the same URL at
  `efb5099…` (`sha256 9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`,
  90963 B); every line number below matches S303's range.

## 1. Anchor table

| # | Operation | Exact line | What it proves about `expected = static + bar` |
|---|---|---|---|
| 1 | The applied rule's area becomes the monitor's static band | `S465` (=`src/output/Monitor.cpp`) :652-655, `m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea)` at :654; hard path `applyMonitorRule` :719 ends at :1069 with `applyMonitorRuleSoft` | Both apply paths (soft compare and full apply) install the rule's reserved area as the monitor's static initial band. |
| 2 | The band is applied to a box that starts at the monitor's layout origin | `S465` :1768-1770 `return {m_position, m_size};`, :1772-1774 `m_reservedArea.apply(logicalBox())` | `usable.x/y` are `m_position + static.left/top`, not `static.left/top`. The tool omits `m_position` (§4A). |
| 3 | Static and dynamic are summed | `S459`/`S466` :43-51 `calculate()` resets to `m_initial*` then adds every `m_dynamicReserved`; :101-108 `addType` accumulates per type | SUM, not replace. A dynamic band never overwrites the static one. |
| 4 | The layer band is measured against the static-reduced box | `S457` :2682 `ORIGINAL_USABLE_AREA = logicalBoxMinusReserved()`, :2683 `usableArea = ORIGINAL_USABLE_AREA`, :2696 `addType(LS, CReservedArea{ORIGINAL_USABLE_AREA, usableArea})` | The layer delta is relative to the already-reduced box, so it adds to the static exactly once (no double count). |
| 5 | The layer box is arranged inside the static-reduced box | `S457` :2588 `full_area = {m_position, m_size}`; :2599-2603 `bounds = *usableArea` unless `exclusive == -1` | For an exclusive surface (`exclusive >= 0`) the placement box is the static-reduced usable box. `full_area` is used only for `exclusive == -1`. |
| 6 | One edge consumes `exclusive + anchored margin` | `S457` :2529 signature; :2535-2572 edge table (top/bottom/left/right, axis, per-edge margin); :2574-2585 first match applies once and breaks | A surface consumes one band on its anchored edge; the band is the client's zone plus that edge's margin. |
| 7 | The client's zone already includes the *unanchored* margin | `S464` (=gtk-layer-shell `layer-surface.c`) :264-292: horizontal branch `allocation.height` + margins of whichever of TOP/BOTTOM is unanchored; vertical branch transposed; waybar enables the auto zone at `S462` :357-361 | This is the "opposite margin" term: band = `anchored margin + allocation + unanchored margin`. |
| 8 | Waybar's anchor set | `S462` :398-429: `top` clears BOTTOM; `width > 1` clears LEFT and RIGHT (transposed for vertical) | Which edge `applyExclusive` matches, and why cross-axis margins never enter a horizontal bar's vertical band. |
| 9 | The placed box and the negative/zero skip | `S457` :2605-2662 (placement, margins, `box.round()` at :2660); :2655-2658 `if (box.width <= 0 || box.height <= 0) continue;` | The box the layer reply prints is this box; a non-positive box is skipped before `applyExclusive`. |
| 10 | `reserved` print order | `S458` :281-282 JSON `left(), top(), right(), bottom()`; :302 text | `[left, top, right, bottom]`, the tool's index. |
| 11 | Legacy rule grammar | `S303` anchors `LegacyConfigManager.cpp:1293-1387`: `addreserved` :1319-1334 (mapping :1322-1323, mutate-existing :1329-1331, fall-through :1333-1341), positional key loop :1351-1379, `transform` :1304-1317, `disable` :1299-1303 | The rule walk the tool reproduces, and the first-`addreserved` drop (repair R1). |
| 12 | One rule per exact name; last match wins | `MonitorRuleManager.cpp` :37-42 `add()` = `erase_if(m_name == …)` then append; :96-99 reverse iteration + `matchesStaticSelector`; :103-106 empty-name fallback | Exact-name rules are unique, so "the newest rule for the selector" is well defined; `desc:` and empty-name rules are *first-class* selectors (see §4C). |
| 13 | Selector predicate | `S465` :1201-1211: `desc:` matches `m_description`/`m_shortDescription` prefix; otherwise exact `m_name == selector` | A `desc:` rule is not "another selector"; it matches the joined monitor. |
| 14 | `addreserved` argument order and clamping | `LegacyConfigManager.cpp` :1322-1323 `{stoi(ARGS[2]), stoi(ARGS[5]), stoi(ARGS[3]), stoi(ARGS[4])}` into `CReservedArea(top, right, bottom, left)` (`S459` :14); clamps at `S459` :15 `std::max(x, 0.0)` | Line order TOP, BOTTOM, LEFT, RIGHT (matches the tool); negative values become 0 (the tool does not, §4B). |
| 15 | Parent/child delta and refusal | `S459` :19-35 (start/end points must lie in the parent); `tests/desktop/Reserved.cpp` :32-37 (`left=20-10`, `top=30-10`, `right=1010-920`, `bottom=1010-930`), :39-55 (empty or non-contained child → all zero), :23-30 (static + dynamic add) | The delta model the tool's `edge_extent` reproduces, and the refusal→zero rule that §4D exploits. |
| 16 | `CBox` semantics | hyprutils `Box.cpp` @ `5a7b8cf…` :43-45 `containsPoint` (inclusive), :47-49 `empty()` = `fabs(w) < EPSILON || fabs(h) < EPSILON`, :51-61 `round()` | A *negative* size is not "empty"; the refusal then comes from the start/end point test. Both paths end at zero contribution. |

## 2. The three decisions the claim depends on

### 2.1 Does the dynamic layer band sum with the static one, or replace it?
**Sum.** `CReservedArea::calculate()` (`S459` :43-51) discards the computed `m_topLeft/m_bottomRight`,
restores `m_initial*` (the static) and adds every dynamic type; `addType` (:101-108) accumulates per
type. The repo's own test asserts the sum: static `(20,30)/(40,50)` plus dynamic LS `(10,20)/(30,40)`
gives `x += 30`, `w -= 100` (`tests/desktop/Reserved.cpp` :23-30). Because the layer delta is
constructed from `ORIGINAL_USABLE_AREA` (already static-reduced, `S457` :2682-2696), the sum is
exact: no static term is counted twice.

### 2.2 Is the layer box arranged inside the static-reduced usable box?
**Yes.** `bounds` is `*usableArea` for every surface with `exclusive >= 0` (`S457` :2599-2603), and
`usableArea` starts as `logicalBoxMinusReserved()` (:2682-2683). The static reserve therefore
translates (and shrinks) the placement box before the bar's own anchors and margins apply. This is
why the tool's `box = local + {static.left, static.top}` is right and why `expected = static[edge] +
extent + opposite margin` needs no cross-term.

### 2.3 What happens when the static reserve leaves no usable box?
Hyprland does **not** refuse. `arrangeLayersForMonitor` has no usable-box guard: with a non-positive
box the surface's computed width/height are non-positive, so `arrangeLayerArray` hits
`if (box.width <= 0 || box.height <= 0) continue;` (`S457` :2655-2658) *before* `applyExclusive`, the
aggregate `usableArea` stays as it was, and `CReservedArea{ORIGINAL_USABLE_AREA, usableArea}`
(:2696) either sees an empty parent/child (`empty()` is `|w| < EPSILON || |h| < EPSILON`,
hyprutils `Box.cpp` :47-49) or fails the start/end-point test (`S459` :19-35) and yields zeros. The
printed band is therefore the static reserve alone, with no layer contribution.
The tool instead refuses the join (`Unmodelled`, `stage=model`, exit 3) as soon as
`usable.w <= 0 || usable.h <= 0`. That is fail-closed, not the observed behaviour, and it is
**not** the same boundary as §4D (where the static box is positive but the bar's *band* overflows).

## 3. The positive path is exact (observed)

The tool's expectation matches a hand derivation from §1 rows 1-8 on all four edges, with the static
on the same edge and both margins non-zero:

```
top     static top 26    bar h 26  margin 4  -> band 60 expected 60  box MATCH  CLEAN
bottom  static bottom 20 bar h 30  margin 4  -> band 58 expected 58  box MATCH  CLEAN
left    static left 10   bar w 40  margin 6  -> band 62 expected 62  box MATCH  CLEAN
right   static right 10  bar w 40  margin 6  -> band 62 expected 62  box MATCH  CLEAN
```
(the `MADO_BARFOOT_RESULT` rows of four `evaluate()` calls; fixtures are the same shape as §4 but
with a same-edge static). So: a bottom bar with a static bottom reserve, a left bar with a static
left reserve, and a margined bottom bar are all modelled correctly. `transform` and `disable` are
also modelled correctly *when the selector already has a rule*: `transform` copies the slot
(`LegacyConfigManager.cpp` :1304-1317) and `disable`/a positional rule replace it with zero
(:1299-1303, `MonitorRuleManager.cpp` :37-42).

## 4. Attacks: reachable declarations where the recorded composition is wrong

All probes are in `.ufo/waves/round-79/w1/R79ScoutModel/probe/<case>/` and are run as:

```sh
python3 -I tools/mado-barfoot.py --config  .ufo/waves/round-79/w1/R79ScoutModel/probe/<case>/config.json \
  --layers   .ufo/waves/round-79/w1/R79ScoutModel/probe/<case>/layers.json \
  --monitors .ufo/waves/round-79/w1/R79ScoutModel/probe/<case>/monitors.json \
  --rules    .ufo/waves/round-79/w1/R79ScoutModel/probe/<case>/rules.conf
```

### A. The monitor's layout origin is ignored (false `box=DIFFER`, rc 1)
Declaration: `M2` at layout `(1920,0)`, `1920x1080`, top bar 26, margin 4, static top 26, live
`reserved [0,60,0,0]`; rules carry a prior positional rule so the static is applied.

Observed (`A-origin`):
```
STATIC: monitor=M2 top=26 right=0 bottom=0 left=0 source=rules
DECL:   monitor=M2 box=4,30,1912,26 edge=top
LIVE:   monitor=M2 level=2 ns=waybar box=1924,30,1912,26 entries=1
RESULT: monitor=M2 box=DIFFER reserved=EQ band=60 expected=60 verdict=DIFFER
rc=1
```
Source-derived: `logicalBox()` is `{m_position, m_size}` (`S465` :1768-1770), so
`logicalBoxMinusReserved()` starts at `(1920, 26)` and the margin-4 box is
`(1924, 30, 1912, 26)` — exactly the LIVE row. `hyprctl monitors -j` already carries `x`/`y`
(`S458` :243-244) and the tool ignores them. The band column is right; only the box join is off.
Coverage: every frozen C1 case has `monitors[x] = monitors[y] = 0` (scanned all 23), so the set
cannot see this. Any bar on a monitor that is not the layout origin yields a spurious rc 1.

### B. A negative `addreserved` value is not clamped (wrong expected, wrong box)
Declaration: `monitor = M1, addreserved, 0, -30, 0, 0` (with a prior positional rule), bottom bar 30,
live `reserved [0,0,0,30]`.

Observed (`B-negative`):
```
STATIC: monitor=M1 top=0 right=0 bottom=-30 left=0 source=rules
DECL:   monitor=M1 box=0,1080,1920,30 edge=bottom
LIVE:   monitor=M1 level=2 ns=waybar box=0,1050,1920,30 entries=1
RESULT: monitor=M1 box=DIFFER reserved=GT band=30 expected=0 verdict=DIFFER
```
Source-derived: `std::stoi("-30")` succeeds (`LegacyConfigManager.cpp` :1323) and the four-arg
`CReservedArea` clamps with `std::max(x, 0.0)` (`S459` :14-15), so Hyprland's static bottom is 0,
its usable box is the full 1080, and the bar is at `y=1050` with band 30. The tool accepts
`INT_FIELD_RE = -?[0-9]{1,6}` and never clamps: `usable.h` becomes 1110, `DECL y=1080`, and the
printed expected becomes `-30 + 30 = 0`. This is the one case seen where the *expected column*
itself is wrong (GT hides it), because the box is also shifted. No frozen case uses a negative
`addreserved`.

### C. `desc:` (and empty-name) selectors are silently skipped
Declaration: `monitor = desc:Dell U2720Q, 1920x1080@100, 0x0, 1` then
`monitor = desc:Dell U2720Q, addreserved, 26, 0, 0, 0`; join monitor `M1` whose description matches;
top bar 26; live `reserved [0,52,0,0]`.

Observed (`C-desc`):
```
STATIC: monitor=M1 top=0 right=0 bottom=0 left=0 source=rules
DECL:   monitor=M1 box=0,0,1920,26 edge=top
LIVE:   monitor=M1 level=2 ns=waybar box=0,26,1920,26 entries=1
RESULT: monitor=M1 box=DIFFER reserved=GT band=52 expected=26 verdict=DIFFER
```
Source-derived: `matchesStaticSelector` matches a `desc:` selector against the description prefix
(`S465` :1201-1211), and `get()` iterates the rule vector in reverse (`MonitorRuleManager.cpp`
:96-99), so the desc rule is the applied one: static 26, box `y=26`, band 52. The tool's
`if selector != monitor: continue` treats it as another selector. The tool's docstring promises
"a selector outside the literal subset" is refused; the code does not refuse — it skips.
Related silent hole: the tool asserts only the joined edge, so a missed static on the *opposite*
edge is invisible. Observed with `monitor = desc:…, addreserved, 0, 26, 0, 0` and live
`reserved [0,26,0,26]`: the tool prints `STATIC … bottom=0` and `verdict=CLEAN`, rc 0.
Empty-name rules (`monitor = , …`, selected by the fallback loop at :103-106) are skipped the same
way.

### D. When the bar's *band* overflows the usable box, Hyprland reserves 0 and the tool expects the band
Declaration: 100-px-high monitor, top bar 26, `margin-top 4`, `margin-bottom 80` (band
`C = 26 + 4 + 80 = 110 > 100`); live `reserved [0,0,0,0]`, live box `(0,4,1920,26)`.

Observed (`D-overflow`):
```
DECL:   monitor=M1 box=0,4,1920,26 edge=top
LIVE:   monitor=M1 level=2 ns=waybar box=0,4,1920,26 entries=1
RESULT: monitor=M1 box=MATCH reserved=DIFFER band=0 expected=110 verdict=DIFFER
```
Source-derived: gtk-layer-shell's auto zone is `allocation.height + margin.bottom = 106`
(`S464` :276-286); `applyExclusive` adds the anchored margin and shrinks the usable box by
`106 + 4` (`S457` :2575-2580, top edge), leaving `y=110, h=-10`. The parent/child constructor then
fails its start-point test (`110 > 100`) and returns zeros (`S459` :19-30; `empty()` does not catch
a negative height, hyprutils `Box.cpp` :47-49), so the derived layer band is 0 and the monitor
reserves nothing. The tool's containment proxy is the *bar box* (`mt + h = 30 <= 100`), not the
*band*; it therefore expects 110. Boundary confirmed at `C = 100`: tool expects 100, source-derived
0; at `C = 99`: both 99 (EQ). The tool's selftest has "an overflowing bar reserves nothing" for the
box-oversize case only (bar taller than the monitor), not this band-overflow case. A static reserve
shrinks `U` first, so a plausible `addreserved` + large margin reaches this without exotic output
sizes.

### E. `transform` with no prior rule creates a phantom slot (post-repair)
Observed (`parse_static_reserve`):
```
monitor = M1, transform, 1
monitor = M1, addreserved, 26, 0, 0, 0
-> {'top': 26, ...}
```
Source-derived: the `transform` branch loops over the rules; with no same-name rule it reaches
`return {};` **without adding anything** (`LegacyConfigManager.cpp` :1304-1317). The following
`addreserved` therefore has no rule to mutate and falls through to `add(parser.rule())` with the area
never handed to the parser (:1329-1341) — the same drop that repair R1 models for the plain case.
The repaired tool's `slot = dict(slot) if slot is not None else dict(ZERO_STATIC)` makes `transform`
look like an existing rule, so the area is wrongly applied. Reachable with a config that sets a
transform before the monitor's mode/position line (legal order, upstream also loses the transform).

## 5. What the model cannot cover, and why

- **A second layer-surface consumer.** `arrangeLayersForMonitor` folds every exclusive surface into
  one aggregate and adds one `CReservedArea` (`S457` :2696). The reply prints the sum
  (`calculate`), so a second consumer is indistinguishable from the joined bar. The tool's `GT`
  is printed and accepted as `CLEAN` (its own `second-consumer` case: band 60, expected 34, GT).
- **A second, non-layer dynamic type.** `RESERVED_DYNAMIC_TYPE_ERROR_BAR` (`ReservedArea.hpp` :7-11)
  is added by `src/errorOverlay/Overlay.cpp` :167-172 as `(m_lastHeight + m_outerPad) / scale` on
  the top or bottom, and `calculate()` sums it. The tool's docstring names only a second layer
  surface; an error overlay is a second GT source it cannot attribute.
- **Scaled outputs.** `hyprctl monitors -j` prints `m_pixelSize` as width/height (`S458` :281),
  while `logicalBox()` is `m_size = (pixel / scale).round()` (`S465` :1059, and `m_pixelSize` is
  only copied to `m_size` at scale 1, :978) and layer boxes are logical. The tool refuses
  `scale != 1`; that refusal is justified.
- **`desc:` / empty-name selectors** (see §4C) and **`monitorv2`** `addreserved`
  (`LegacyConfigManager.cpp` :802-809, same TOP/BOTTOM/LEFT/RIGHT value order but a separate config
  shape): the tool reads only legacy `monitor =` lines, so a host using either form is
  under-modelled (or silently wrong, for `desc:`).
- **Sourced config files.** The legacy manager follows `source`; the tool refuses any `source =`
  line, even when the sourced file carries no monitor rules. Fail-closed, coarse.
- **`std::stoi` prefix forms** (`26px`, `+26`) and `$` variables: Hyprland accepts the prefix /
  expands the variable; the tool refuses. Fail-closed.
- **Negative margins.** Refused (justified: the band can be voided or extend past the box). Note the
  source's `exclusive + margin > 0` condition (`S457` :2575) also makes a zero-zone surface consume
  its anchored margin; the tool's `exclusive: false` path prints an `expected` that is not the
  physical band (its `static-exclusive-false` case prints `expected=52` where the source-derived
  contribution is 0).
- **Aggregate refusal.** One uncontained surface zeroes the *entire* LS aggregate (the ctor refuses
  as a whole, `S459` :19-35), not just its own band; the tool's per-bar containment is a different
  predicate (see §4D).

## 6. Residual unknowns

- `CVarList2`'s exact trimming/iteration is not executed here; the tool's `split(",")` + `strip()`
  reproduces every tested line, including trailing comments and the drop-on-unknown-key cases, but
  exotic whitespace/quoting is [INFERENCE].
- `monitorv2` and legacy rules can coexist in one config; the relative `add()` order across both is
  not modelled (the tool never reads `monitorv2`).
- Host posture (read-only): one monitor at layout `(0,0)`, scale 1, transform 0,
  `reserved [0,26,0,0]`, and no `addreserved`, `desc:` or `monitorv2` in `~/.config/hypr`. The
  host's own band therefore exercises only the single-consumer r78 path; all C1 static cases are
  synthetic and, per §4A, all sit at the origin.
- `CBox::empty()`/`containsPoint()` are pinned from hyprutils `5a7b8cf221914ce4714407950e4ffbdddcd8b66f`
  (the `flake.lock` pin), not from `fetch/`.

## 7. Method, fetches, housekeeping

- Pins read: `fetch/S457.bin … S466.bin` (sha256 per `fetch/sha256-r79.txt`).
- Unpinned corroborating fetches at `efb50993780079460b0cbed1363e2166a2de1d9f` (same commit as the
  pins): `src/config/legacy/ConfigManager.cpp` `9db68cf4…`; `src/config/shared/monitor/MonitorRuleManager.cpp`
  `17d46685…`; `.../Parser.cpp` `616468fd…`; `tests/desktop/Reserved.cpp` `37988cca…`;
  `src/errorOverlay/Overlay.cpp` `ec6ca667…`; `src/desktop/view/LayerSurface.cpp` `63b24015…`;
  `src/protocols/LayerShell.cpp` `ad9314da…`; `src/desktop/reserved/ReservedArea.hpp` `6222d114…`;
  `src/output/Monitor.cpp` is the S465 pin. hyprutils `Box.hpp` `39962242…`, `Box.cpp` `2d04de99…`
  at rev `5a7b8cf…` (`flake.lock` `ba52e623…`).
- Commands of record: the four probe CLI runs (§4), the four-edge matrix (`evaluate()` calls), the
  selftest (`python3 -I tools/mado-barfoot.py --selftest` → `44/44` at HEAD), and the C1 counter at
  HEAD (§0). No tool installs; no pacman; no repo or host writes; read-only git only.
- Scratch `/fast/scratch/hyaku/mado-r79/R79ScoutModel/` is deleted at seat close; the probe fixtures
  remain in this seat's write directory only.
