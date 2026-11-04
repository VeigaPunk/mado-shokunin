# R82ScoutModel — round-82 model reconnaissance

Read-only seat. Base `6ea2386d49318a5f223097c78b5fe79c31b064f8`, freeze
`780c30fcae12d74ce8ab3b871a0888696c2415d9`. The bytes read are the freeze's: the working
tree `tools/mado-barfoot.py` and `git show 780c30fc:tools/mado-barfoot.py` both hash to
`380075284d7d5c6f56a82600935d512def617223be27f33241ff5dbcb0bcab59`; the counter hashes to
`1e9f394d…`, the C1 control to `e404bb3f…`. Diffstat: one file, +119/−22. Lane `HEAD` at read
time was `b6146ee` (later than the freeze); the tool blob at the freeze is `93cd54a8`, the same
blob the working tree carries.

## 1. Exact diff inventory

### 1.1 Contract docstring (tools/mado-barfoot.py:52-60)
The unconditional refusal of a dynamic band is replaced by a conditional one: a horizontal
`height = 0` / vertical `width = 0` is refused unless `--allocation` declares the client's own
band for that namespace; then the allocation is the band for both the arranged box and
gtk-layer-shell's auto zone (`layer-surface.c:276/282`), and a zero or absent allocation is
still refused, never guessed. Only the list-valued-config sentence is re-wrapped.

### 1.2 VERSION (tools/mado-barfoot.py:89)
`r81-v1` → `r82-v1`.

### 1.3 `parse_allocation` (tools/mado-barfoot.py:436-453)
Grammar, in order:

- the input is strict JSON via `load_json` (:441), not JSONC. The config path uses
  `load_jsonc` (:1543), so comments and trailing commas are accepted in the config file but
  are a setup refusal in the allocation file. UTF-8 and ≤1 MiB come from `read_bytes`.
- top level must be a JSON object (:442-443): `the allocation declaration is not an object of
  namespace -> band`.
- each key must be a non-empty string (:446-447): `the allocation declaration carries an
  empty namespace` (JSON object keys are strings already; the empty key is what is refused).
- each value must be an `int`, with `bool` explicitly rejected (:448-449): `the allocation for
  %r is not an integer`.
- each value must be ≥ 0 (:450-451): `the allocation for %r is negative`. Zero parses; the
  zero refusal is deferred to `band_of` so it fires only when a dynamic band actually consumes
  the entry.
- returns `{namespace: band}`; no other key is interpreted here — unknown namespaces are a
  later setup refusal (1.6/1.7).
- `-` (stdin) is accepted because main calls `read_bytes(..., stdin_ok=True)` (:1566).

### 1.4 `band_of` (tools/mado-barfoot.py:456-471)
- axis = `height` for `top`/`bottom`, `width` for `left`/`right` (:460).
- a positive declared value wins and the allocation is not consulted (:461-462).
- otherwise `allocation.get(namespace)` (:463); key absent → `Unmodelled` "has a dynamic %s
  (0) and no --allocation entry" (:464-467); present but ≤ 0 → `Unmodelled` "was allocated a
  %d %s band; a zero band reserves nothing" (:468-470).
- no inference and no fallback; distinct absent vs zero, both refused.

### 1.5 `declared_box` (tools/mado-barfoot.py:474-510)
- signature gains `allocation=None` (:474), defaulted to `{}` (:478).
- only the band axis resolves: `height = band_of(bar, allocation)` for `top`/`bottom` else the
  config `height`; `width = band_of(...)` for `left`/`right` else the config `width`
  (:481-482).
- every later branch reads the resolved locals rather than `bar[...]` (:484-508). A dynamic
  band with an allocation therefore takes the explicit-band branch (`height > 0`, :490;
  `width > 0`, :504), and the auto-span branch (:493-496 / :507-509) is skipped. Centring,
  margins and the final non-positive refusal are unchanged.
- thresholds unchanged: cross axis is explicit when `> 1` (:484, :498), band when `> 0`
  (:490, :504). This is a carried threshold, not introduced here (see §5.2).

### 1.6 Composition band resolution (`evaluate_composition`, tools/mado-barfoot.py:748-…)
- signature gains `allocation` (:748-749).
- the declaration is copied and checked against the namespaces the composition carries: bar
  namespace plus every `--surfaces` namespace (:768-770); any other key → setup refusal
  "the allocation declaration names …, which the composition does not carry" (:771-773).
- `bar_spec` is seeded with the config `height`/`width` (:795-796); then `band_axis` is chosen
  by position and `bar_spec[band_axis] = band_of(bar_spec, allocation)` (:802-803), before the
  surface list and the level/order sort (:804-806). Both the bar's arranged box and its
  `surface_zone` (auto) therefore see the resolved band.
- only the bar spec is patched. Extras keep their declared sizes (:804); the known set at
  :769 includes extra namespaces, so an allocation for an extra passes this gate but is never
  consumed (verified in §3 and §5.1).

### 1.7 `evaluate` simple path (tools/mado-barfoot.py:956-1004)
- signature gains `allocation` (:956-957); the composition delegation forwards it (:959-960).
- unknown-namespace check against the bar namespace alone (:961-965).
- `declared_box(bar, usable["w"], usable["h"], allocation)` (:1004).

### 1.8 `--allocation` CLI (tools/mado-barfoot.py:1534, :1540, :1564-1568)
- `ap.add_argument("--allocation")` (:1534); the usage line becomes
  `… [--surfaces PATH] [--allocation PATH|-]` (:1540).
- main parses it after `--surfaces` (:1564-1566) with `read_bytes(..., stdin_ok=True)`;
  absent → `None`. An empty-string argument is falsy and is skipped (:1565).
- `evaluate(..., surfaces, allocation)` (:1567-1568).

### 1.9 Selftest additions (tools/mado-barfoot.py:1485-1520)
Twelve new checks: four `declared_box` allocation boxes for top/bottom/left/right
(:1488-1495), "a declared band is not overridden by the allocation" (:1496-1499), absent
allocation refused (:1500-1504), zero allocation refused (:1505-1509), the vertical band axis
is the width (:1510-1511), `parse_allocation` accepts a valid object (:1512), and negative /
non-integer / non-object are refused (:1513-1520). Base tool tally 121/121 → 133/133.

## 2. The eight new cases, recomputed by hand

Sources used for the arithmetic:

- **Arrange (S470.bin `src/render/Renderer.cpp`, Hyprland 0.56.2).** Desired size starts the
  box (:2607); `width == 0` → `x = bounds.x` (:2610-2611); two horizontal anchors centre in
  doubles (:2612-2613); singular left → `x = bounds.x` (:2614-2615); right → far edge
  (:2616-2617); vertical is symmetric (:2622-2632). Margins: `width == 0` → `x += left`,
  `w = bounds.w − left − right` (:2635-2637); both horizontal anchors → no margins
  (:2638-2639); left → `+left`, right → `−right` (:2640-2643); vertical symmetric
  (:2645-2653); non-positive box is skipped (:2655-2658); `box.round()` (:2660).
- **Auto zone (S464.bin `src/layer-surface.c`, gtk-layer-shell 0.10.1).** `horiz` = left
  anchor == right anchor, `vert` = top == bottom (:269-272); `horiz && !vert` → zone =
  `current_allocation.height` + top margin if top unanchored + bottom margin if bottom
  unanchored (:275-280); `vert && !horiz` → zone = `current_allocation.width` + left/right
  unanchored margins (:281-286); corner/parallel/all-four leaves `-1` and sends nothing
  (:287-292).
- **Exclusive application (S470 `applyExclusive`, :2529-2586).** First edge whose singular
  anchor or triplet matches (or `exclusiveEdge`) and `zone + margin > 0` (:2575); top adds
  `zone + marginTop` to y (:2576-2577); bottom subtracts from h (:2580); left adds to x,
  right subtracts from w. The case's `band` is the monitor's reserved value for the bar's
  edge; order is `[left, top, right, bottom]` (tool :119).

Case-by-case (`band` = `expect.band` = monitor reserved on the bar edge):

| case | allocation | band resolution | hand box | auto zone → reserved | verdict |
|---|---|---|---|---|---|
| `alloc-dyn-height-top` | waybar 34 | height 0 → 34 (:460-467) | w 0 → x 0, w 3440 (:2610-2611, :2635-2637); h 34, top → y 0 (:2627-2628, :2650-2651) = **0,0,3440,34** | 34 + 0 + 0 = 34 (:275-280); exclusive top 34 + 0 (:2575-2578) → **34** | DERIVED |
| `alloc-dyn-height-margin` | waybar 30 | height 0 → 30 | w 0 → x 4, w 3432 (:2635-2637); h 30, top → y 4 = **4,4,3432,30** | 30 + 0 (top anchored) + 4 (bottom unanchored) = 34 (:276-280); exclusive top 34 + marginTop 4 = **38** (:2575-2578) | DERIVED |
| `alloc-dyn-width-dock` | waybar 60 | width 0 → 60 (:axis width) | w 60, left → x 0 (:2614-2615, :2640-2641); h 0 → y 0, h 1440 (:2623-2624, :2645-2647) = **0,0,60,1440** | 60 + left 0 + right 0 = 60 (:281-286); exclusive left 60 + 0 (:2575-2577) → **60** | DERIVED |
| `alloc-zero-refused` | waybar 0 | height 0, allocation 0 → `band <= 0` → Unmodelled (:468-470) | none | none; stage=model, rc 3 | DERIVED |
| `alloc-negative-refused` | waybar −4 | `parse_allocation` negative → Setup (:450-451) | none | none; stage=setup, rc 2 | DERIVED |
| `alloc-unknown-namespace` | panel 40 | bar namespace defaults to `waybar` (:336); simple-path unknown check (:961-965) → Setup | none | none; stage=setup, rc 2 | DERIVED |
| `alloc-explicit-ignored` | waybar 40 | height 26 > 0 wins (:461-462); allocation unused | w 0 → x 0, w 3440; h 26, top → y 0 = **0,0,3440,26** | 26 (:276-280); exclusive top 26 (:2575-2578) → **26** | DERIVED |
| `alloc-composition-dyn-bar` | waybar 34 | bar height 0 → 34 via :802-803 | bar **0,0,3440,34**; panel bounds y 34, h 100 top → y 34, w 0 → w 3440 = **0,34,3440,100** (:2610-2611, :2627-2628, :2635-2637) | bar zone 34 (:276) + panel explicit zone 12 (:604-606) = **46** (:2575-2578); usable y 46; expected 46; attributed 34+12 = 46; `ls` top 46 = VALID | DERIVED |

All eight are **DERIVED**: every box and every reserved value follows from the cited lines,
including the margin double-count in `alloc-dyn-height-margin` (gtk's auto zone adds the
unanchored bottom margin at S464:279-280, then Hyprland adds the anchored top margin at
S470:2575-2578). No case is NOT-DERIVABLE.

Secondary cross-check (not the C1 counter): running the tool directly on the eight case files
in scratch produced the exact `expect` fields — the three CLEAN RESULT lines
(`band=34 expected=34`, `band=38 expected=38`, `band=60 expected=60`, `band=26 expected=26`,
`band=46 expected=46 attributed=46 attr=0,46,0,0 ls=VALID`) and the three staged refusals
(`stage=model` rc 3, `stage=setup` rc 2, `stage=setup` rc 2). The hand arithmetic above was
written first and stands independently.

## 3. Classes that remain REFUSED after this round

### 3.1 Per-axis dynamic extra surface
The composition resolves the band only for the bar (`bar_spec[band_axis] = band_of(...)`,
tools/mado-barfoot.py:802-803); extras are appended unresolved (:804). For an extra whose
band is 0:

- `exclusive` `"auto"`: `surface_zone` refuses inside the `horiz && !vert` branch at
  tools/mado-barfoot.py:613-616 (raise :615), and inside `vert && !horiz` at :623-626
  (raise :625). Verified probe: `panel` height 0, `exclusive`: `"auto"`, allocation
  `{"waybar":34,"panel":40}` → `stage=model`, rc 3, "auto zone on a dynamic height (0)…".
- `exclusive` an explicit integer: **not refused**. The allocation is accepted by the known
  set (:769-770) but never applied; the box auto-spans the usable axis (S470:2623-2624,
  2645-2647). Verified probe: the same panel with `exclusive`: 12 and allocation `panel`: 40
  yields `DECL … box=0,34,3440,1406` (the full usable height, not 40). This is the one place
  where the new input is accepted and then silently ignored.

### 3.2 Fractional-scale monitor
`scale` must be 1/1.0 and `transform` 0/0.0, in both paths:
`evaluate_composition` tools/mado-barfoot.py:762-766 (raise :764) and `evaluate`
:977-981 (raise :979), message "the reply carries pixel size and the layer box is logical,
so this join is not modelled". Verified probes with scale 1.5 and transform 1 → `stage=model`,
rc 3 in the modelled composition.

### 3.3 The allocation bypass (what the declaration cannot bypass)
A dynamic band is modelled only by a positive allocation that names a carried surface. The
remaining refusal gates:

- absent entry for a dynamic band: tools/mado-barfoot.py:463-467 (raise :465), stage=model;
- present zero: :468-470 (raise :469), stage=model;
- negative: `parse_allocation` :449-451 (raise :451), stage=setup;
- unknown namespace: composition :769-773 (raise :772), simple path :961-965 (raise :964),
  stage=setup;
- malformed declaration: non-object :442-443, empty key :446-447, non-integer :448-449,
  all stage=setup;
- a positive declared band cannot be overridden: `band_of` :461-462 returns the declared value
  and ignores the allocation (`alloc-explicit-ignored`), so an allocation is not a bypass of
  the declaration either.

## 4. Version and selftest

- `VERSION = "r82-v1"` (tools/mado-barfoot.py:89).
- `TMPDIR=/fast/scratch/hyaku/mado-r82/R82ScoutModel/tmp python3 -I tools/mado-barfoot.py
  --selftest` → `MADO_BARFOOT_SELFTEST: 133/133`, rc 0.
- The base tool (`6ea2386d`) is `r81-v1` and tallies `121/121`; the diff adds 12 checks.
- No tools were installed or upgraded for this seat (none needed).

## 5. Residual observations (read-only; for the L1 to weigh)

1. **Extra-surface allocation is accepted but inert** — see §3.1. `evaluate_composition`'s
   known set includes extras (:769), but only the bar is patched (:803). With an explicit
   `exclusive` the declared extra allocation changes nothing and the box auto-spans; with
   `auto` the same declaration is refused at :615/:625. If `--allocation` is intended to be
   per-surface, this is a modelling hole; C1's frozen claim only asserts the bar's band
   (:802-803), so it is not a scored defect against the claim.
2. **Carried cross-axis threshold `> 1` vs Hyprland `== 0`** — tools/mado-barfoot.py:484/498
   treat cross sizes 0 and 1 as auto-span, while S470 tests `box.width == 0` (:2610),
   `box.height == 0` (:2623), and the margin branches (:2635, :2645): a 1-px explicit cross
   size would be placed at its anchor by Hyprland but spans here. Pre-existing (the diff only
   swaps `bar[...]` for the resolved locals); not exercised by the 47 frozen cases.
3. **Allocation file is strict JSON, config is JSONC** — :441 vs :1543. A commented
   allocation file is a setup refusal; the contract docstring does not state this asymmetry.
4. **Empty `--allocation` argument is skipped** — :1565 tests truthiness, so `--allocation ""`
   behaves as if absent (`None`), not as a parse error. Only a non-empty path (or `-`) reaches
   `parse_allocation`.

STATUS: ok
