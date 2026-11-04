# R78ExecC1Cases — independent re-derivation of the eighteen frozen C1 expectations

Seat: executor, round 78 wave 1. Scope: read-only re-derivation of every case in
`.ufo/waves/round-78/controls/c1-cases-r78.json` (sha256 `99f1d82f…`, verified below) from the
two source rules, then one tool run per case for comparison. No repo file was edited; only
read-only git (`rev-parse`, `show`) was used, `--show-toplevel` asserted the lane repo.

## 1. Frozen-instrument verification (before any use)

```
sha256sum tools/mado-barfoot.py            aac5d41b923711e174c6d62bb24da5a2b53abf7c938bfc5b68816929a12009c0  (brief: match)
           quality/counters/c1-r78-margins.py  1c39a53c9320b3f4c849ceb973e7fb0d42fb115e2f8f7a64bc3338fc4ab85000  (brief: match)
           .ufo/waves/round-78/controls/c1-cases-r78.json  99f1d82fd3476b151be2951549645ce71fd47b6d8a9e96f90a5f891bda5a56ae  (brief: match)
```
`git rev-parse HEAD` = `44a36b64…` (the frozen pre-wave amendment). Pinned fetches: all six
entries of `.ufo/waves/round-78/fetch/sha256-r78.txt` match their files, and r78 `S457.bin`,
`S462.bin`, `S464.bin` are byte-identical to the round-77 copies (`9af8a74e…`, `120eb913…`,
`deef9c81…`). The held r77 control tool was extracted read-only:
`git -C /home/vgpnk/Projects/shokunin/mado-shokunin show f597eccbffefd5fd6bbb01f3511c88bbeaed493c:tools/mado-barfoot.py`
(572 lines, VERSION `r77-v1`, into the seat scratch only).

## 2. The two source rules, as quoted

**Rule A — gtk-layer-shell auto zone** (`.ufo/waves/round-78/fetch/S464.bin:264-295`,
`layer_surface_update_auto_exclusive_zone`): horizontal branch
`:275-280` — `new_exclusive_zone = self->current_allocation.height`, plus
`margins[TOP]` if the top edge is *not* anchored and `margins[BOTTOM]` if the bottom edge is
*not* anchored; vertical branch `:281-286` transposed on width/left/right. So the client-side
auto zone = allocation + margins of the **unanchored** edges of the band axis.

**Rule B — Hyprland `applyExclusive`** (`.ufo/waves/round-78/fetch/S457.bin:2529-2533`,
guard `if (exclusive <= 0) return;`; composition loop `:2574-2584`): on the anchored edge it
advances the usable area by `exclusive + edges[i].margin`, where `edges[i].margin` is that
anchored edge's own margin (`marginTop` `:2547`, `marginBottom` `:2555`, `marginLeft`
`:2563`, `marginRight` `:2571`); call site `IHyprRenderer::arrangeLayerArray` `:2664`, the
result lands in `m_reservedArea` `:2680-2696`. So the compositor adds the **anchored** edge's
margin.

**Composed model under test** (declaration C1): band for top/bottom =
`height + margin.top + margin.bottom`; transposed for left/right =
`width + margin.left + margin.right`; negative margin refused, never composed. Cross-check
with the tool's shape: `expected = extent + bar["margins"][OPPOSITE_EDGE[edge]]`
(`tools/mado-barfoot.py:411`, `OPPOSITE_EDGE` `:69`) with
`extent = box.y + box.h` (top) etc. — the anchored-edge margin rides inside `extent` through
the declared box position, algebraically the same total.

**Box rule** (Hyprland `arrangeLayerArray`; contract at `tools/mado-barfoot.py:46-49`): a zero
desired width spans the usable box minus horizontal margins; `width > 1` clears both
horizontal anchors (waybar `bar.cpp:422-424`) and the box is centred
(`x = (mon_w - w) // 2`); transposed for vertical.

**Verdict mapping** (`tools/mado-barfoot.py:410-426`): `reserved` NOT_APPLIED iff
`exclusive` false, else EQ (`band == expected`) / GT (`band > expected`) / DIFFER;
`box` MATCH iff the live entry at the declared level+namespace equals the declared box
exactly; verdict DIFFER rc 1 if either differs else CLEAN rc 0; excluded output → NO_BAR rc 3;
refusals (dynamic cross size `:289-291`, negative margin `:253-254`) → rc 3 with
`ERROR (stage=model …)`.

## 3. Order of work (as instructed)

Derivation first, tool second. For each case I computed box, extent, expected, band class and
verdict by hand from the rules above and the frozen fixtures, wrote the re-derived row down,
and only then materialized each case's `config/layers/monitors` fixtures in scratch and ran
`python3 -I tools/mado-barfoot.py --config … --layers … --monitors … [--monitor …]` once per
case (driver and its full output preserved at
`.ufo/waves/round-78/w1/R78ExecC1Cases/receipt-c1-cases-tool-run.txt`; the same driver scored
the held r77 tool on the same fixtures).

## 4. Table — case | declared | re-derived | tool | agree?

Encoding: `box/reserved b<band> e<expected> <verdict> rc<n>`; `—` = field not emitted.

| case | declared | re-derived | tool (r78-v1) | agree? |
|---|---|---|---|---|
| host-top | MATCH/EQ b26 e26 CLEAN rc0 | MATCH/EQ b26 e26 CLEAN rc0 | MATCH/EQ b26 e26 CLEAN rc0 | yes |
| bottom-bar | MATCH/EQ b30 e30 CLEAN rc0 | MATCH/EQ b30 e30 CLEAN rc0 | MATCH/EQ b30 e30 CLEAN rc0 | yes |
| top-margin-int | MATCH/EQ b38 e38 CLEAN rc0 | MATCH/EQ b38 e38 CLEAN rc0 | MATCH/EQ b38 e38 CLEAN rc0 | yes |
| top-margin-css-2 | MATCH/EQ b38 e38 CLEAN rc0 | MATCH/EQ b38 e38 CLEAN rc0 | MATCH/EQ b38 e38 CLEAN rc0 | yes |
| top-margin-asym | MATCH/EQ b42 e42 CLEAN rc0 | MATCH/EQ b42 e42 CLEAN rc0 | MATCH/EQ b42 e42 CLEAN rc0 | yes |
| bottom-margin | MATCH/EQ b46 e46 CLEAN rc0 | MATCH/EQ b46 e46 CLEAN rc0 | MATCH/EQ b46 e46 CLEAN rc0 | yes |
| left-margin | MATCH/EQ b52 e52 CLEAN rc0 | MATCH/EQ b52 e52 CLEAN rc0 | MATCH/EQ b52 e52 CLEAN rc0 | yes |
| right-margin | MATCH/EQ b46 e46 CLEAN rc0 | MATCH/EQ b46 e46 CLEAN rc0 | MATCH/EQ b46 e46 CLEAN rc0 | yes |
| right-zero-margin | MATCH/EQ b40 e40 CLEAN rc0 | MATCH/EQ b40 e40 CLEAN rc0 | MATCH/EQ b40 e40 CLEAN rc0 | yes |
| layer-bottom | MATCH/EQ b28 e28 CLEAN rc0 | MATCH/EQ b28 e28 CLEAN rc0 | MATCH/EQ b28 e28 CLEAN rc0 | yes |
| output-exclusion | MATCH/EQ b24 e24 CLEAN rc0 | MATCH/EQ b24 e24 CLEAN rc0 | MATCH/EQ b24 e24 CLEAN rc0 | yes |
| output-excluded | NOT_ON_MONITOR/NOT_APPLIED — NO_BAR rc3 | NOT_ON_MONITOR/NOT_APPLIED — NO_BAR rc3 | NOT_ON_MONITOR/NOT_APPLIED — NO_BAR rc3 | yes |
| width-with-margins | MATCH/EQ b34 e34 CLEAN rc0 | MATCH/EQ b34 e34 CLEAN rc0 | MATCH/EQ b34 e34 CLEAN rc0 | yes |
| exclusive-false | MATCH/NOT_APPLIED b0 CLEAN rc0 | MATCH/NOT_APPLIED b0 (e26, unchecked by expect) CLEAN rc0 | MATCH/NOT_APPLIED b0 e26 CLEAN rc0 | yes |
| second-consumer | MATCH/GT b60 e34 CLEAN rc0 | MATCH/GT b60 e34 CLEAN rc0 | MATCH/GT b60 e34 CLEAN rc0 | yes |
| reserved-differ | MATCH/DIFFER b26 e34 DIFFER rc1 | MATCH/DIFFER b26 e34 DIFFER rc1 | MATCH/DIFFER b26 e34 DIFFER rc1 | yes |
| dynamic-cross | error rc3 | error rc3 (h=0 horizontal refused) | ERROR (stage=model) rc3 | yes |
| negative-margin-refused | error rc3 | error rc3 (margin "-2 0" refused) | ERROR (stage=model) rc3 | yes |

**r78-v1: 18/18 agree. Held r77 tool on the same eighteen cases: 8/18** (passes exactly
host-top, bottom-bar, right-zero-margin, layer-bottom, output-exclusion, output-excluded,
exclusive-false, dynamic-cross; every margined case reports `NOT_MODELLED` rc 3
`UNMODELLED`, and negative-margin-refused fails on the missing `ERROR (` line) — equal to the
frozen `base_correct=8/18` clause. The tool selftest was also run and exited 0
(`--selftest` exits 0 iff checks==total; the frozen clause is `tool_selftest=22/22`; the
literal count line went to the supervised job log, the receipt holds the case table).

### Derivation notes (one line each; box x,y,w,h)

1. host-top: 3440×1440, top h26 m0 → box 0,0,3440,26; extent=26; +mb0 → 26; band r[top]=26 EQ.
2. bottom-bar: 1920×1080, bottom h30 → box 0,1050,1920,30; extent=1080−1050=30; +mt0 → 30 EQ.
3. top-margin-int: m4 → box 4,4,1912,30; extent=34; +mb4 → 38 EQ. (Composed-rule check:
   30 + mb4 unanchored + mt4 anchored = 38 — same total.)
4. top-margin-css-2: "4 8" → t4 r8 b4 l8 → box 8,4,1904,30; extent=34; +4 → 38 EQ.
5. top-margin-asym: margin-top 10, margin-bottom 2 → box 0,10,1920,30; extent=40; +2 → 42 EQ.
6. bottom-margin: m8 → box 8,1042,1904,30; extent=38; +mt8 → 46 EQ.
7. left-margin: 3440×1440, left w40 m6 → box 6,6,40,1428; extent=46; +mr6 → 52 EQ.
8. right-margin: box 3399,5,36,1430; extent=3440−3399=41; +ml5 → 46 EQ.
9. right-zero-margin: 1920×1080 → box 1880,0,40,1080; extent=40; +0 → 40 EQ.
10. layer-bottom: level bottom=1 (`LEVEL` `tools/mado-barfoot.py:60`); box 0,0,1920,28; extent 28 EQ.
11. output-exclusion: `!M2` + `--monitor M1` → bar applies on M1; box 0,0,3440,24; extent 24 EQ.
12. output-excluded: `!M1` on M1 → NO_BAR rc3 before any box/layers consultation.
13. width-with-margins: w800>1 → x=(3440−800)//2=1320, y=4, box 1320,4,800,26; extent=30; +4 → 34 EQ.
14. exclusive-false: NOT_APPLIED; band=measured r[top]=0; expected=26 emitted but the frozen
    expect deliberately omits the `expected` key (counter compares only declared keys,
    `quality/counters/c1-r78-margins.py:124`).
15. second-consumer: box 4,4,3432,26; extent=30; e34; band 60>34 → GT; GT is admissible → CLEAN rc0.
16. reserved-differ: e34; band 26<34 → DIFFER → verdict DIFFER rc1.
17. dynamic-cross: h=0 horizontal → Unmodelled refusal rc3.
18. negative-margin-refused: "-2 0" → top=bottom=−2 → negative check refuses rc3.

## 5. Flags

**F0 — no fixture contradicts its declaration.** Checked per case: (a) live box equals the
hand-derived declared box in all 16 non-error cases; (b) every EQ band equals
allocation + band-axis margins (26, 30, 38, 38, 42, 46, 52, 46, 40, 28, 24, 34, 34); (c) all
18 names distinct, no duplicated case; (d) the GT/DIFFER fixtures are deliberate
(second-consumer band 60 = 34 + 26 from a second consumer; reserved-differ band 26 < 34).

**F1 — eight cases cannot separate the r78 model from the held r77 rule** (base also correct):
host-top, bottom-bar, right-zero-margin, layer-bottom, output-exclusion, output-excluded,
exclusive-false, dynamic-cross. This is consistent with the frozen predicate, which only
requires set-level separation (`base_correct=8/18` < `correct=18`), and each still pins an
independent behavior (plain box, bottom edge, vertical bar, level join, two-monitor join,
exclusion, NOT_APPLIED, refusal). Recorded here because the seat checklist asks for it; no
action implied.

**F2 — four of the seven frozen mutants have a single killer case.** Working the kill map by
hand: `opposite-margin-dropped` and `horizontal-margin-leak` are killed by many cases;
`right-extent-flip` by two (right-margin, right-zero-margin). But:
- `level-bottom-swap` — killed only by `layer-bottom` (the only bottom-layer declaration);
- `per-side-margin-dropped` — killed only by `top-margin-asym` (the only `margin-*` case);
- `negative-margin-accepted` — killed only by `negative-margin-refused` (the only negative
  margin; the mutant lands CLEAN rc0 there: extent 24, expected 22, band 24 → GT);
- `opposite-edge-wrong` — killed only by `top-margin-asym`: for every symmetric-margin case
  the wrong edge still sums to the band (top-margin-int 34+4=38, bottom-margin 38+8=46,
  left-margin 46+6=52, right-margin 41+5=46, width-with-margins 30+4=34), second-consumer
  stays GT (34 vs 60) and reserved-differ stays DIFFER (30 vs 26); asym is the only case where
  band-axis margins differ (40+10=50 ≠ 42).
`top-margin-asym` is therefore the unique killer for two of the seven mutants.

**F3 — error-case fixtures carry plausible but unasserted bands.** dynamic-cross ships
`reserved [0,26,0,0]` against a declared height 0; negative-margin-refused ships `[0,24,0,0]`.
The counter's error contract never reads them (`expected_ok` `:115-118`), so this is
harmless; noted only so a future generator does not treat those bands as modelled values.

**F4 — output-excluded's fixture is not capture-shaped.** The case keeps a live waybar layer
(0,0,3440,26) on M1 although `output: "!M1"` would not map the bar there; the tool returns
NO_BAR before consulting layers, so nothing breaks. A real capture would show no such entry.

**F5 — the tool's decomposition is unobservable through this set.** The tool folds the
anchored-edge margin into `extent` (via the box position) and adds only the opposite margin;
the source rules compose allocation + unanchored margins + anchored margin. Totals are
identical in every reachable configuration, and no frozen mutant separates the two
decompositions. Inherent to the algebra; no action.

## 6. Proposed case upgrades (a later round; the frozen set was not edited)

- **U1** a bottom bar with asymmetric band-axis margins (e.g. `margin-top: 1`,
  `margin-bottom: 7`) — second killer for `opposite-edge-wrong` through the bottom edge.
- **U2** a left/right bar with per-side left/right margins — second killer for
  `per-side-margin-dropped` and a further `opposite-edge-wrong` killer on the vertical axis.
- **U3** a margined `layer: bottom` bar — second killer for `level-bottom-swap` and the first
  margined non-top-level case.
- **U4** a negative margin in per-side integer form (`margin-top: -2`) — second killer for
  `negative-margin-accepted` through a different parse branch than the CSS string.
- **U5** a four-value CSS margin with differing top/bottom (e.g. `"3 4 5 6"`) — string-branch
  asymmetric-band killer.
- **U6** re-shape the output-excluded fixture to a real capture (move the live entry to the
  other monitor or empty the levels on M1).

## 7. Commands actually run (evidence trail)

1. `sha256sum` over the five frozen artifacts → all match the seat brief (§1).
2. `git rev-parse HEAD` / `git rev-parse --show-toplevel` → `44a36b64…`, lane repo asserted.
3. `git show f597eccb…:tools/mado-barfoot.py` → held r77 control extracted to scratch only.
4. `python3 -I tools/mado-barfoot.py --selftest` → exit 0 (passes iff checks==total;
   frozen clause `tool_selftest=22/22`).
5. `python3 -I /fast/scratch/hyaku/mado-r78/R78ExecC1Cases/drive_cases.py` → per-case table
   above; full stdout preserved at
   `.ufo/waves/round-78/w1/R78ExecC1Cases/receipt-c1-cases-tool-run.txt`.
6. Host posture: no hyprctl call at all (none needed); no installs (no tooling
   authorization consumed); no git/jj mutation; no repo edit; scratch directory
   `/fast/scratch/hyaku/mado-r78/R78ExecC1Cases/` deleted at the end of the seat.

Report: .ufo/waves/round-78/w1/R78ExecC1Cases.md
