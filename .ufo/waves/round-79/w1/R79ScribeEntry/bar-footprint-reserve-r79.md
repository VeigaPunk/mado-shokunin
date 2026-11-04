# The static reserve under the bar's band: `addreserved` composes with a layer surface

source: S465 Hyprland v0.56.2 `src/output/Monitor.cpp` @ efb5099 (`applyMonitorRuleSoft` `:652-655`, `m_reservedArea.setStatic(...)` `:654`; `logicalBoxMinusReserved` `:1772-1774`; `m_size = (xfmd / m_scale).round()` `:699-700`); S466 `src/desktop/reserved/ReservedArea.cpp` @ efb5099 (parent/child ctor `:19-37`, `calculate` `:43-51`, `apply` `:53-60`, `setStatic` `:69-74`, `addType` `:101-112`; byte-identical to S459, sha256 `0a52e145…`); S457 `src/render/Renderer.cpp` @ efb5099 (`arrangeLayersForMonitor` `:2673-2700`: reset `:2680`, `ORIGINAL_USABLE_AREA` `:2682`, LS add `:2696`; `applyExclusive` `:2529-2585`, guard `:2575`, add `:2577`); S458 `src/debug/HyprCtl.cpp` @ efb5099 (monitors `reserved` print `:281-282`; layers `namespace`/`pid` `:676-677`); S303 `src/config/legacy/ConfigManager.cpp` @ efb5099 (`handleMonitor` `:1293-1386`: `addreserved` `:1319-1327`, in-place set `:1331`, fall-through add `:1341`, positional add `:1384`; `CMonitorRuleManager::add` `MonitorRuleManager.cpp:37-38`).
verified-at: 2026-11-04, round 79; 23 cases at `5eb8f20fe291603c74973fa94cc55723ac8089a4` (tool `r79-v1`, sha256 `c9aa1391…86de`): `correct=23 killed=12 base_correct=18/23 carried=18/18 tool_selftest=43/43 verdict=TARGET_MET` (`receipts/measurement-c1-r79.txt`); the held round-78 tool is the control (`correct=18/23 killed=4`, `receipts/control-c1-r79-at-base.txt`)
recheck: on-release (Hyprland after v0.56.2); 180d otherwise — re-open S465/S466/S457/S458/S459/S303, `sha256sum -c .ufo/waves/round-79/fetch/sha256-r79.txt`, re-run `python3 -I quality/counters/c1-r79-reserve.py --repo . --rev <tip> --base-rev e4b153dfa4a67ca56f7ec65cb6639082451626a7 --controls .ufo/waves/round-79/controls/c1-cases-r79.json --carried .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root DIR`
Lane: mado-shokunin. Round: 79. Supersedes the static-`addreserved` limit of `bar-footprint-margins-r78.md` §What is not claimed; that body stays the record of the r78 instrument and of the two margins the bar contributes.

## What this entry holds

| question | where the answer lives | state |
|---|---|---|
| Does a static reserve replace the bar's band or add? | `calculate` sums the static initial box with every dynamic entry (S466 `:43-51`); the layer type is the delta between the static-reduced box and the arranged box (S457 `:2682`, `:2696`) | OBS (source) |
| Where does the static part come from? | the active rule's area, copied by `setStatic` on application (S465 `:654`; S466 `:69-74`) | OBS (source) |
| Which `addreserved` wins? | the selector's existing rule is mutated in place (S303 `:1331`); a positional line erases it first (`:1384`, `MonitorRuleManager.cpp:37-38`) | OBS (source) |
| What does the join expect? | `static[edge] + extent_inside_usable + margins[opposite]`, box moved by the static origin; scored 23/23 at `5eb8f20f` (`tools/mado-barfoot.py:554-555`, `:503-505`, `:524`; `measurement-c1-r79.txt`) | OBS (tool, receipt) |

## §1 The composition: one sum, two contributors

The printed band is not a maximum over overlapping rectangles. `calculate()` starts from the static initial box and
adds every dynamic type's contribution (S466 `:44-51`); the static part is the active rule's area, copied by
`m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea)` (S465 `:654`), and `setStatic` copies the corners and
the validity flag, then recomputes (S466 `:69-74`). The layer part arrives as a parent/child pair: `ORIGINAL_USABLE_AREA`
is `logicalBoxMinusReserved()` — the box already shrunk by the static reserve (S457 `:2682`, S465 `:1772-1774`, S466
`:53-60`) — and after `arrangeLayerArray`, `CReservedArea{ORIGINAL_USABLE_AREA, usableArea}` is added as the single
layer type (S457 `:2696`, cleared at `:2680`); its constructor stores the four deltas (S466 `:19-37`).

The bar's extent is therefore measured **inside** the static-reduced box: a 26 px static top reserve puts the usable
origin at `y=26`, so a top bar with `height 26, margin 4` realises at `y=30`, contributes `4+26+4 = 34`, and the
band is `26+34 = 60`. Contributions sum rather than saturate, so a reserve on another edge moves the box without
entering the joined edge's band.

## §2 The rule walk that produces the static area

`handleMonitor` treats field 1 as a modifier when it is `disable`/`disabled`/`addreserved`/`transform` (S303
`:1293-1299`). For `addreserved` the four fields are `std::stoi`-read into `CReservedArea(top=ARGS[2], right=ARGS[5],
bottom=ARGS[3], left=ARGS[4])` (S303 `:1319-1327`) — written order **TOP, BOTTOM, LEFT, RIGHT** — and assigned to the
selector's existing rule in place (S303 `:1331`). A positional rule appends through `CMonitorRuleManager::add`, which
erases every same-name rule first (`MonitorRuleManager.cpp:37-38`, called at S303 `:1384`), so a selector never keeps
two rules: a later `addreserved` overwrites, and a positional line resets the area to zero. `transform` copies the
rule and keeps the area (S303 `:1303-1313`).

One anchor is a limit, not a rule: when the selector has no rule yet, `addreserved` falls through to
`add(parser.rule())` (S303 `:1341`) with a default zero area, so the parsed area is dropped; the join applies it and
assumes the rule slot exists, as the frozen cases do. The tool also refuses (`stage=model`) a `source =` line, a rule
line carrying `$`, `\` or `##`, a non-integer `addreserved` field, and a reserve leaving no usable box
(`tools/mado-barfoot.py:356-375`, `:506-508`).

## §3 Decision table: reachable declaration → expected band

| declaration (modelled subset) | usable box → bar box | `expected` on the joined edge | published `reserved` |
|---|---|---|---|
| static top 26, top bar h26 m4 | `y=30`, `h=26` | `26 + (4+26+4) = 60` | `EQ` 60 (`static-composed`) |
| static left 40, top bar h26 (another axis) | `x=40`, `w=mon_w−40`, `y=0` | `26`; the 40 prints as `reserved[0]` | `EQ` 26 (`static-other-edge`) |
| static top 26 **or** none, `exclusive: false` | `y=26` / `y=0` | 52 / 26 printed, `NOT_APPLIED`; the band reads the monitor's value | `NOT_APPLIED` (`static-exclusive-false`, `exclusive-false`) |
| two `addreserved` for M1 (10 then 26), one for M2 (5) | `y=26` | `26+26 = 52` (M1's last line; M2's selector is never consulted) | `EQ` 52 (`static-last-wins`) |
| no static reserve (eighteen carried cases) | `y=m.top` | `extent + margins[opposite]` — this rule at `static=0` | `EQ`/`GT`/`DIFFER` |
| `source = …`; non-integer `addreserved` field; a reserve leaving no usable box | — | — | refused `stage=model` rc 3 (`static-source-refused`) |
| dynamic cross, negative margin, `mode`, `layer: background`, list config, spaced output, scale/transform | — | — | refused rc 3 / rc 2 (carried cases) |

## §4 The five new cases, worked

Each row is one `MADO_R79_CASE` line of `.ufo/waves/round-79/receipts/measurement-c1-r79.txt` (cited, not re-run).

| case | rules line | bar | expected | receipt |
|---|---|---|---|---|
| `static-composed` | `addreserved, 26, 0, 0, 0` | top h26 m4 | 26+34=60 | `band=60 expected=60 reserved=EQ` |
| `static-other-edge` | `addreserved, 0, 0, 40, 0` | top h26 | 26, box `x=40` | `band=26 expected=26 reserved=EQ` |
| `static-exclusive-false` | `addreserved, 26, 0, 0, 0` | top h26, `exclusive: false` | 52 printed, not applied | `band=26 expected=52 reserved=NOT_APPLIED` |
| `static-last-wins` | M1 10, M1 26, M2 5 | top h26 | 26+26=52 | `band=52 expected=52 reserved=EQ` |
| `static-source-refused` | `source = ~/.config/hypr/other.conf` | top h26 | refused | `rc=3 box=None … correct=yes` |

`static-composed` realises at `4,30,3432,26` — the margin places the bar 4 px below a usable origin already 26 px
down. `static-other-edge` keeps the top band at 26 while the monitor reports `reserved=[40,26,0,0]`: only the joined
edge's index is read (`tools/mado-barfoot.py:548`; order left, top, right, bottom, S458 `:281-282`).

## §5 Mutants and the do-nothing control

Twelve single-anchor mutations (`quality/counters/c1-r79-reserve.py:45-88`), killed iff below 23: the seven r78
ones score 13,13,22,21,22,22,22 and the five new ones 20,20,22,19,22 (`static-dropped`, `static-order-swapped`,
`static-first-wins`, `static-box-unoffset`, `static-selector-ignored`; counters `:71-73`–`:85-87`) — all killed. The
control (`1bceb514…`) scores `18/23`, `killed=4`, five new cases `rc=2`, eight anchors `anchor-absent`, no `--rules`.

## What is not claimed

- **A second layer-surface consumer** that reserves at runtime is still not attributed: the join reports `GT` and
  no model. Only a statically declared reserve composes.
- **Scaled or transformed outputs** stay refused (S465 `:699-700`: the logical size is the pixel size over the
  scale); the monitors reply carries pixel size, the layer box is logical.
- **`desc:` selectors, an empty selector, a sourced config file** are outside the walk; the tool refuses rather
  than guesses, so such a config reads `stage=model`, never `DIFFER`.
- **The rule slot is assumed.** An `addreserved` that opens a selector's config loses its area at the handler's
  fall-through (S303 `:1341`); the model applies it.
- **The host is one read-only sample.** No `addreserved` was applied to the running compositor; `grep -rl addreserved ~/.config/hypr/` exits 1, so the host join stays a zero-static prediction.
- **Four exported ints, not a rectangle.** Only the integer at `RESERVED_INDEX[edge]` is compared, so a reserve
  distributed around the monitor is checked on one edge; the layers reply carries `namespace`/`pid`, not the
  exclusive request (S458 `:676-677`).

## Evidence

- `.ufo/waves/round-79/fetch/S465.bin`, `S466.bin` (+ S457–S462, S464), `sha256-r79.txt` — `sha256sum -c` OK for
  every source row; the manifest's own self-row cannot verify (it lists its own digest).
- `.ufo/waves/round-79/receipts/measurement-c1-r79.txt` — 23 cases, 12/12 mutants, base 18/23, `carried=18/18`,
  `tool_selftest=43/43`, tool sha `c9aa1391…`; `control-c1-r79-at-base.txt` — base `e4b153df`, sha `1bceb514…`;
  `.ufo/waves/round-79/controls/c1-cases-r79.json` sha `5f7ebb3c…`.

## Sources

S465 and S466 in [SOURCES](../SOURCES.md), opened this round; S457/S458/S459 mined from rounds 77–78, with S303,
S460, S461, S462, S464 re-read. S463 stays rejected (renders the protocol without a revision pin); S467 stays
rejected (documents the line syntax, not the summation).
