# R78MutC1 — mutation probe of the r78 reserved-band rule (round 78, wave v1)

Seat: R78MutC1 (mutation-tester, leaf member, no subagents). Probe: 27 single-anchor mutants of
`tools/mado-barfoot.py` (r78-v1) run against a byte-verified copy of the frozen 18-case set
`.ufo/waves/round-78/controls/c1-cases-r78.json`. None of the 27 (anchor, replacement) pairs
equals any of the seven frozen `MUTATIONS` in `quality/counters/c1-r78-margins.py:26-49`; three
share an anchor with a frozen mutant but replace it differently (flagged per row below).

## Command and baseline

- Driver: `/fast/scratch/hyaku/mado-r78/R78MutC1/mutate.py` — preserved at
  `.ufo/waves/round-78/w1/R78MutC1/mutate.py`; raw machine result at
  `.ufo/waves/round-78/w1/R78MutC1/results.json`; run log at
  `.ufo/waves/round-78/w1/R78MutC1/receipt-run.txt`.
- Per case the driver mirrors PRED-C1-r78-v1's scoring:
  `python3 -I <tool-copy> --config config.json --layers layers.json --monitors monitors.json`
  (`--monitor` where the case names one), files written per case from the frozen JSON, exit map
  and RESULT line parsed exactly as `expected_ok`/`parse_result` in the counter.
- Baseline (pristine copy): **correct=18/18**, selftest rc 0 `MADO_BARFOOT_SELFTEST: 22/22`.
  A baseline failure would have made every mutant inconclusive; it did not.
- Case-set sha256 verified `99f1d82f…56ae` before scoring.

## Results — mutant | verdict | killing case(s)

All verdicts are grounded in per-case observed stdout; `file:line` is the mutated anchor in the
pristine `tools/mado-barfoot.py`.

| # | mutant | axis | file:line | verdict | killing case(s) |
|---|--------|------|-----------|---------|-----------------|
| 1 | band-edge-top-right-swap | band edge selection | :65 | KILLED | host-top, +10 (top-margin-int, top-margin-css-2, top-margin-asym, right-margin, right-zero-margin, layer-bottom, output-exclusion, width-with-margins, second-consumer, reserved-differ) |
| 2 | band-edge-opposite-read | band edge selection | :410 | KILLED | host-top, +13 |
| 3 | margin-sign-flip *(≠ frozen #1: subtracts, not drops)* | margin sign | :411 | KILLED | top-margin-int, +8 (top-margin-css-2, top-margin-asym, bottom-margin, left-margin, right-margin, width-with-margins, second-consumer, reserved-differ) |
| 4 | margin-sign-absorbed | margin sign | :193 | KILLED | negative-margin-refused |
| 5 | per-side-branch-skipped *(≠ frozen #5: skips the branch, falls to margin-key forms)* | per-side precedence order | :184 | KILLED | top-margin-asym |
| 6 | css-2-order-scramble | per-side precedence order | :199 | KILLED | top-margin-css-2 |
| 7 | css-3-order-scramble | per-side precedence order | :201 | SURVIVED | — (gap S1) |
| 8 | centre-shift-left-margin | centring with margins | :278 | KILLED | width-with-margins |
| 9 | centre-vertical-shift | centring with margins | :292 | SURVIVED | — (gap S2) |
| 10 | centre-round-half-up | rounding | :278 | SURVIVED | — (gap S3, **model gap**) |
| 11 | centre-float-division | rounding | :278 | SURVIVED | — (gap S3, **model gap**) |
| 12 | level-top-demoted *(≠ frozen #3: demotes top, not bottom)* | level order | :60 | KILLED | host-top, +13 |
| 13 | level-overlay-demoted | level order | :60 | SURVIVED | — (gap S4) |
| 14 | output-exclusion-dropped | output include/exclude precedence | :231 | KILLED | output-excluded |
| 15 | output-include-first | output include/exclude precedence | :231 | SURVIVED | — (gap S5) |
| 16 | extent-bottom-flip | extent bottom | :312 | KILLED | bottom-bar, bottom-margin |
| 17 | extent-left-flip | extent left | :314 | KILLED | left-margin |
| 18 | extent-right-double-margin *(≠ frozen #4: double-subtracts anchored margin)* | extent right | :315 | KILLED | right-margin |
| 19 | extent-top-margin-sub | extent top (control) | :309 | KILLED | top-margin-int, +5 |
| 20 | gt-differ-swap | exclusivity branch | :416 | KILLED | second-consumer, reserved-differ |
| 21 | eq-ge-merge | exclusivity branch | :414 | KILLED | second-consumer |
| 22 | exclusivity-inverted | exclusivity branch | :412 | KILLED | host-top, +13 |
| 23 | empty-box-refusal-relaxed | refusal conditions | :302 | SURVIVED | — (gap S6) |
| 24 | scale-transform-refusal-relaxed | refusal conditions | :371 | SURVIVED | — (gap S7) |
| 25 | mode-refusal-relaxed | refusal conditions | :248 | SURVIVED | — (gap S8) |
| 26 | background-refusal-relaxed | refusal conditions | :245 | SURVIVED | — (gap S9) |
| 27 | star-output-refusal-relaxed | refusal conditions | :225 | SURVIVED | — (gap S10) |

**Totals: 27 probes — 16 killed, 11 survived, 0 inconclusive.** Baseline 18/18 held before and
the frozen tool bytes were re-hashed identical after (see Restoration).

Representative observed outputs (full 5-line stdout preserved in `gen/<mutant>/case-NN.fail.txt`,
copied per-mutant into results.json):

```
# margin-sign-flip / top-margin-int      (expect reserved=EQ band=38 expected=38 rc 0)
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH reserved=GT band=38 expected=30 verdict=CLEAN
# eq-ge-merge / second-consumer          (expect reserved=GT band=60 expected=34)
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH reserved=EQ band=60 expected=34 verdict=CLEAN
# output-exclusion-dropped / output-excluded (expect rc 3 NO_BAR)
MADO_BARFOOT: verdict=CLEAN            # full CLEAN run, rc 0
```

## Survivors (11) — classification

Every survivor's stdout is **sha1-identical to pristine on all 18 cases**
(`results.json: stdout_identical_on_all_18=true` for each) — equivalence on the frozen set is
proven byte-for-byte, not inferred. Every survivor also diverges from pristine on a plausible
input, so **all 11 are type (a) findings (real coverage/model gaps with a named discriminating
case); zero are type (b) algebraic equivalents.** Per the seat contract these are coverage
findings, not contract changes; the frozen predicate `mutants=7 killed=7` is untouched.

- **S3 centre-round-half-up + centre-float-division (:278) — the sharp one: a real MODEL gap.**
  The pinned sources do not floor. `CBox` members are double (`fetch/S468-Box.hpp:164-167`);
  arrangeLayerArray centres as `box.x = bounds.x + ((bounds.width / 2) - (box.width / 2))`
  (`fetch/S457.bin:2613`, vertical `:2626`), then `box.round()` at `fetch/S457.bin:2660`, and
  `CBox::round()` is `std::round` — half away from zero — (`fetch/S469-Box.cpp:51-60`). So for an
  odd positive `mon − size` remainder the source puts the bar at `(mon − w + 1) // 2` (e.g. 1920/801
  → 960 − 400.5 = 559.5 → 560), while the model's `(mon_w - w) // 2` (`tools/mado-barfoot.py:278`)
  floors to 559. The frozen set cannot see this: its only centring case (width-with-margins) has
  even remainder 2640. Discriminating case: **A** below. Honest scope: neither pristine nor the
  round-half-up mutant is fully source-true (negative odd remainders round away from zero, i.e.
  down = floor); a successor model line should be `round(mon_w/2 - w/2)` with half-away-from-zero
  semantics. The frozen declaration already lists "centring rounding" among what the model does
  not claim — this names the exact case and the required semantics.
- **S2 centre-vertical-shift (:292)** — no case reaches vertical centring: all four left/right
  cases leave `height` undeclared (0 → auto-height branch). Discriminating case: **B** below.
- **S1 css-3-order-scramble (:201)** — no 3-token margin string in any case (the 18 use `0`,
  `4`, `8`, `"4 8"`, `"-2 0"`, per-side ints). Discriminating: `{position top, height 30,
  margin "1 2 3"}` on 1920×1080, live `x=2 y=1 w=1916 h=30` → pristine band 34 EQ; mutant swaps
  top/bottom → `y=3` → box DIFFER rc 1 → killed.
- **S4 level-overlay-demoted (:60)** — all 18 configs declare layer `top` (17) or `bottom` (1);
  `overlay` is never declared. Discriminating: `{layer "overlay", position top, height 26}` with
  the live entry on level 3 → pristine CLEAN; mutant finds nothing on level 1 → NO_LAYER rc 3.
- **S5 output-include-first (:231)** — both output cases are exclusion-only (`"!M2"`, `"!M1"`),
  so `include` is empty whenever the precedence code runs; no positive-include case exists at all.
  Discriminating: `{output ["M1","!M1"]}` joined on M1 → pristine NO_BAR rc 3 (exclusion wins);
  mutant CLEAN rc 0.
- **S6 empty-box-refusal-relaxed (:302)** — reachable only when the computed box is exactly 0
  wide/high; the set's one zero-size case (dynamic-cross) exits at the earlier dynamic-cross-size
  guard, never reaching `:302`. Discriminating: `{position top, height 26, margin "0 960"}` on
  1920 → pristine rc 3 `declared box is empty (0x26)`; mutant proceeds → rc 0/1 → error-clause
  expectation fails.
- **S7 scale-transform-refusal-relaxed (:371)** — all 18 monitors carry scale 1.0 / transform 0.
  Discriminating case: **C** below.
- **S8 mode-refusal-relaxed (:248)** — no case sets `mode`. Discriminating: `{"mode":"dock",
  position top, height 26}` → pristine rc 3 model error; mutant runs → rc 0/1.
- **S9 background-refusal-relaxed (:245)** — no background case. Discriminating: `{layer
  "background"}` with a live level-0 waybar entry → pristine rc 3 `ERROR (stage=model …)`;
  mutant matches on level 0 → CLEAN rc 0.
- **S10 star-output-refusal-relaxed (:225)** — no `*`/space output case. Discriminating:
  `{"output":"*"}` → pristine rc 3 `ERROR (stage=model …)`; mutant treats `*` as an include name,
  falls through to NO_BAR rc 3 without the `ERROR (` marker → error-clause expectation fails.

## Coverage bound the eighteen cases impose

The set kills any mutant that changes an observable on: the band composition of a top/bottom bar
under the exercised margin forms (int, 2-token CSS, per-side pair), the four reserved verdict
classes (EQ/GT/DIFFER/NOT_APPLIED are all pinned by host-top/second-consumer/reserved-differ/
exclusive-false), the four edge extents at the exercised bar shapes, level lookup for 1 and 2,
exclusion matching, and the two pinned refusals (dynamic cross size, negative margin). It
**cannot** distinguish pristine from any mutant whose differing input requires one of:

1. an odd `mon − size` centring remainder (only one centring case, even remainder, horizontal);
2. a vertical bar with explicit height (vertical centring branch never executes);
3. layer `overlay` or `background`, or a `mode` key;
4. scale ≠ 1 or transform ≠ 0 on the joined monitor;
5. a 3- or 4-token CSS margin string;
6. a positive output include (all output specs are exclusions; a name in both lists is
   unreachable too);
7. a `*`/space output pattern;
8. a computed box of exactly zero extent.

11 of 27 independent mutants live entirely in that blind spot — every one byte-identical to
pristine on all 18 cases. Positions are also top-heavy (13 top / 2 bottom / 1 left / 2 right), so
single-case edges (left) carry no redundancy.

## Three strongest successor cases (expectations derived from the pinned sources, not from tool runs)

- **A — odd-remainder centring (kills 11's class, demonstrates the model gap):** config
  `{position top, layer top, height 26, width 801}`; M1 1920×1080 scale 1 transform 0, reserved
  `[0,26,0,0]`; live level-2 waybar `x=560 y=0 w=801 h=26` (S457.bin:2613 halves in double →
  559.5; S469-Box.cpp:51-53 `std::round` → 560). Expect box=MATCH, reserved=EQ, band=26,
  expected=26, rc 0. Pristine today scores this case red (declared x=559 → box DIFFER rc 1) —
  case A is simultaneously the kill of centre-float-division and the demonstration that the
  `:278` floor deviates from S457+S469 on odd remainders.
- **B — vertical explicit-height centring with margins (kills 9):** config
  `{position left, layer top, width 40, height 200, margin 6}`; M1 3440×1440, reserved
  `[52,0,0,0]`; live `x=6 y=620 w=40 h=200` (both vertical anchors cleared by the declared
  height → centred `1440/2 − 200/2 = 620`, margins not applied on that axis, S457.bin:2625-2626
  and the `// don't apply margins` branch; anchored left + margin.left → x=6; band = extent 46 +
  opposite right margin 6 = 52). Expect MATCH / EQ 52 / rc 0. Kills centre-vertical-shift (626 ≠
  620) and pins the transposed no-margin centring.
- **C — scaled-monitor refusal (kills 24):** host-top's fixtures with the monitor at
  `scale 1.25` → expect rc 3 with `ERROR (stage=model` (the refusal at `tools/mado-barfoot.py:371`
  that the declaration names as unmodelled ground).

Runners-up, one case each: `mode` preset refusal (kills 25), `layer background` refusal (26),
`output "*"` refusal (27), 3-token CSS margin (7), positive include + `["M1","!M1"]` precedence
(15), `margin "0 960"` empty-box refusal (23).

## Restoration evidence

- The repo copy of `tools/mado-barfoot.py` was never opened for writing by this seat; mutants
  were written only under scratch. sha256 **before** `aac5d41b923711e174c6d62bb24da5a2b53abf7c938bfc5b68816929a12009c0`
  = **after** (driver prints `RESTORATION: … identical=True`).
- Case set sha256 `99f1c75a…`/`99f1d82f…` verified (`99f1d82fd3476b151be2951549645ce71fd47b6d8a9e96f90a5f891bda5a56ae`);
  counter files untouched.
- `git status --porcelain -- tools quality .ufo/waves/round-78/controls` shows only
  ` M quality/tool-ledger.md`, which this seat did not create or modify (concurrent wave
  traffic; seat wrote only its scratch and its two w1 artifacts).
- No git/jj write command was run anywhere; no host probe beyond file reads; scratch deleted
  after evidence was copied out.
