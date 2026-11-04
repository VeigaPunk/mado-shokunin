# The static reserve under the bar's band: how `addreserved` composes with a layer surface

source: S465 Hyprland v0.56.2 `src/output/Monitor.cpp` @ efb5099 (`applyMonitorRuleSoft` `:652-655`, quote `:654`, `logicalBoxMinusReserved` `:1772-1774`); S466 `src/desktop/reserved/ReservedArea.cpp` @ efb5099 (`calculate` `:43-51`, `setStatic` `:69-74`, `addType` `:101-112`); S457 `src/render/Renderer.cpp` @ efb5099 (`arrangeLayersForMonitor` `:2673-2700`, reset `:2680`, parent box `:2682`, add `:2696`); S458 `src/debug/HyprCtl.cpp` @ efb5099 (monitors `reserved` print `:281-282`); S459 `src/desktop/reserved/ReservedArea.cpp` @ efb5099 (parent/child constructor `:19-35`, `apply` `:53-60`); S303 `src/config/legacy/ConfigManager.cpp` @ efb5099 (`handleMonitor` modifier forms `:1299`, `addreserved` fields `:1319-1341`).
verified-at: 2026-11-04, round 79; the twenty-three cases are measured at `5eb8f20fe291603c74973fa94cc55723ac8089a4` (tool `r79-v1`, sha256 `c9aa1391…`, 23/23); the held round-78 tool is the control (`base_correct=18/23`). Receipts `.ufo/waves/round-79/receipts/measurement-c1-r79.txt` and `control-c1-r79-at-base.txt`; pinned bytes `.ufo/waves/round-79/fetch/S465.bin`–`S466.bin` (`sha256-r79.txt`).
recheck: on-release (Hyprland after v0.56.2); 180d otherwise — re-open S465/S466/S457/S458/S459/S303, re-fetch the three files, re-run `python3 -I quality/counters/c1-r79-reserve.py --repo . --rev <tip> --base-rev e4b153df … --controls .ufo/waves/round-79/controls/c1-cases-r79.json --carried .ufo/waves/round-78/controls/c1-cases-r78.json --scratch-root DIR`
Lane: mado-shokunin. Round: 79. Supersedes the `NOT_MODELLED` static-`addreserved` limit of `bar-footprint-margins-r78.md` §limits; the r78 body stays the record of the r78 instrument.

## What this entry holds

| question | where the answer lives | state |
|---|---|---|
| Does a static reserve add to the layer's own band, or replace it? | `CReservedArea::calculate` sums the static initial box with every dynamic type's contribution (S466 `:43-51`); the layer type is added as the delta between the static-reduced box and the box after arranging (S457 `:2682`,`:2696`) | OBS (source) |
| Where does the static reserve come from? | the active monitor rule's `m_reservedArea`, copied by `setStatic` when the rule is applied (S465 `:654`; S466 `:69-74`) | OBS (source) |
| How does an `addreserved` line set it? | field 1 `addreserved`; fields 2–5 are TOP, BOTTOM, LEFT, RIGHT, assigned as `CReservedArea(top, right, bottom, left)` (S303 `:1319-1326`): TOP=ARGS[2], RIGHT=ARGS[5], BOTTOM=ARGS[3], LEFT=ARGS[4] | OBS (source) |
| Which rule's reserve wins? | `addreserved` changes the same-selector rule in place (`:1331`), or adds a default rule when none exists (`:1341`); a positional rule replaces the selector's rule (the manager erases same-selector rules before appending); the newest matching rule is the one applied | OBS (source) |
| Where is the layer box placed? | inside `logicalBoxMinusReserved()` — the monitor box minus the static reserve (S457 `:2682`; S465 `:1773`), not inside the full monitor box | OBS (source) |
| What does the join expect now? | `expected = static[edge] + extent_inside_usable + margins[opposite]`, the box translated by the static origin (`tools/mado-barfoot.py`) | OBS (tool) |
| Is that scored on a frozen set? | 23/23 at `5eb8f20f`, twelve named mutants killed (`receipts/measurement-c1-r79.txt`) | OBS (receipt) |
| Does the host declare a static reserve? | no `addreserved` line in `~/.config/hypr/**` (2026-11-04); the live join with `--rules ~/.config/hypr/monitors.conf` reports `STATIC … source=rules` all-zero and stays `CLEAN band=26 expected=26` | OBS (host, read-only) |

## §1 Two contributors, summed once each

The reported `reserved` band is not a maximum of overlapping rectangles; it is a sum.
`CReservedArea::calculate` starts from the static initial box (`m_initialTopLeft`,
`m_initialBottomRight`) and adds every dynamic type's contribution (S466 `:44-51`). The static
part is the active monitor rule's reserved area, copied at rule application
(`m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea)`, S465 `:654`). The layer part is
registered by the renderer as a parent/child box: `ORIGINAL_USABLE_AREA` is
`logicalBoxMinusReserved()` — the monitor box minus the static reserve (S457 `:2682`, S465
`:1773`) — and after `arrangeLayerArray` has consumed the layer's exclusive zones, the delta
between the two boxes is added as the single dynamic type `RESERVED_DYNAMIC_TYPE_LS` (S457
`:2680`, `:2696`). So a static top reserve of 26 px and a top bar that consumes 34 px yield a
reported top band of 60 px, and the bar's own extent is measured *inside* the 26-px-reduced
box, not from the monitor edge.

## §2 The rule walk that produces the static reserve

`handleMonitor` splits the line on commas (S303 `:1295`) and treats field 1 as a modifier when
it is `disable`/`disabled`/`addreserved`/`transform` (S303 `:1299`):

- `addreserved`: fields 2–5 are read with `std::stoi` and handed to
  `CReservedArea(top, right, bottom, left)` as `ARGS[2], ARGS[5], ARGS[3], ARGS[4]` (S303
  `:1323`), i.e. the written order is **TOP, BOTTOM, LEFT, RIGHT**. The area is written into
  the first rule with the same selector (`:1331`); if none exists, a default rule for that
  selector is added (`:1341`) — and that rule never received the area, so its reserve is zero
  and the written area is dropped. An `addreserved` line is therefore only effective after a
  same-selector rule (typically the positional `monitor = NAME, WxH@R, x, y` line).
- `transform`: copies the same-selector rule, so its reserved area survives the copy.
- `disable`/`disabled`: adds a disabled rule, reserved zero.
- A positional rule replaces the selector's rule (the manager erases same-selector rules
  before appending), so it resets the reserve unless the line itself is dropped: an unknown
  key never reaches the add (S303 `:1351-1379`).

The tool models exactly this walk for the joined monitor's exact selector, ignores other
selectors, and refuses (`stage=model`) a `source =` line, a `$`-bearing rule or a non-integer
field — because a sourced file is not followed and a guessed reserve is worse than no join.

## §3 Decision table: reachable declaration → expected band

| declaration | box | `expected` | published `reserved` |
|---|---|---|---|
| static top 26 + top bar h26 m4 | `y = 26 + 4` | `26 + (4+26+4) = 60` | `EQ` when the monitor reports 60 |
| static left 40 + top bar h26 | `x = 40`, width `mon_w − 40` | top band `26` (the left reserve is not on this axis) | `EQ` 26 |
| static top 26 + `exclusive: false` | `y = 26` | `26 + 26 = 52` printed, `NOT_APPLIED` | `NOT_APPLIED` |
| two `addreserved` for M1 (10 then 26) + one for M2 (5) | `y = 26` | `26 + 26 = 52` (newest M1 rule; M2's selector never applies) | `EQ` 52 |
| `addreserved` with no same-selector rule ahead of it | unchanged | `0` + bar (the area is dropped) | as the bar alone (the written area is not applied) |
| a negative `addreserved` field | unchanged | the field clamps at 0 (`std::max(x, 0.0)`) | as the clamped reserve |
| a monitor whose layout position is not `0,0` | origin `+ position` | the static term plus the bar band | `EQ` at the new origin |
| a band that does not fit the usable axis | matches | the static term alone (the layer contributes 0) | `EQ` when the monitor reserves only the static band |
| static reserve leaves no usable box | — | — | refused `stage=model` |
| `source =` line in the rules file | — | — | refused `stage=model` |

## §4 The measured set and its limits

The five new cases (`static-composed`, `static-other-edge`, `static-exclusive-false`,
`static-last-wins`, `static-source-refused`) join the eighteen r78 cases carried
byte-identically; the twelve mutants are the seven r78 ones plus `static-dropped`,
`static-order-swapped`, `static-first-wins`, `static-box-unoffset`, `static-selector-ignored`.
Each new mutant is separated by at least one of the five cases; the receipt prints the
per-mutant score.

## §5 Repairs the wave forced (R1, R2)

**R1 (wave seat R79ScribeEntry F1).** The rule walk credited an `addreserved` area with no
same-selector rule ahead of it; the handler drops it (above). Repaired; the four static fixtures
now carry the positional rule their expectation presupposes. Receipts
`repair-r79-c1-fallthrough.txt` (frozen tool `expected=52 DIFFER` vs repaired `expected=26
CLEAN` on a rules file whose only line is `addreserved`) and `repair-r79-c1-oldfixtures.txt` (the
pre-repair fixtures score 20/23 against the repaired tool).

**R2 (wave seat R79ScoutModel §4 A–E).** Five more reachable classes were wrong: the monitor's
layout origin was ignored (`logicalBox()` is `{position, size}`, S465 `:1772-1774`); a negative
`addreserved` field was not clamped (S466 `:14-15`); a `desc:`/empty selector was silently
skipped instead of refused (a `desc:` rule matches by description, S465-monitor `:1201-1211`);
a band that overflows the usable axis was still expected (the parent/child short-circuit returns
zeros, S459 `:19-30`); and a `transform` with no same-selector rule created a phantom slot.
All five repaired with a selftest assertion each (44 → 50) and one red/green pair per class in
`repair-r79-c1-model-r2.txt`; no frozen case, expectation, mutant or target moved.

## What is not claimed

- A second *layer-surface* consumer whose band is declared only at runtime is still not
  attributed: the join reports `GT` and no model. Only a statically declared reserve composes.
- Scaled or transformed outputs (`scale != 1`, `transform != 0`) stay refused: the monitors
  reply carries pixel size while the layer box is logical.
- `desc:` selectors, an empty selector and a sourced config file are outside the walk; the tool
  refuses rather than guesses.
- The composition is a model over source-read semantics. No `addreserved` line was applied to
  the running compositor in this round; the host join is a read-only prediction against a
  zero static reserve.
- The fall-through (an `addreserved` with no same-selector rule drops its area) is asserted in
  the tool's selftest, not in a frozen case: the twenty-three cases all declare a prior rule, so
  a mutation that credits the fall-through would survive the case set. The wave found and
  repaired this rule (`receipts/repair-r79-c1-fallthrough.txt`, `repair-r79-c1-oldfixtures.txt`).
