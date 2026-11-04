# R83ExecC1Cases — C1 case replay and independent arithmetic

STATUS: ok

## Scope and axes
Coverage: score all 58 frozen controls and independently derive the six new surface cases. Evidence fidelity: retain exact replay results and bind them to bytes. Isolation: no instrument changes, no host changes, no git/jj mutations, no extra verification.

Imported `quality/counters/c1-r83-surface-band.py` with `importlib.util.spec_from_file_location`, disabled bytecode, and called:

```python
correct, rows = counter.run_cases(
    '/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py',
    cases,
    '/fast/scratch/hyaku/mado-r83/R83ExecC1Cases',
    'current',
)
```

`cases` was loaded from `.ufo/waves/round-83/controls/c1-cases-r83.json["cases"]`. The run helper was wrapped in memory only to retain its returned stdout/stderr without executing cases twice. Python 3.14.8; existing installation, no installs or updates. All child fixture directories and TMPDIR were under the seat scratch. No full counter, mutant suite, base replay, selftest, build, lint or formatter was run.

## Result and byte binding

`cases=58 correct=58 mismatches=0`. Counter MUTANTS and mutation-entry length were both already 39 at import; the earlier reported constant mismatch was not present in these measured bytes. No instrument was edited by this seat. The declaration read at task start still said 38; reconciliation belongs to L1 and is not evidence of a case mismatch.

SHA-256 before and after replay were equal:

- `quality/counters/c1-r83-surface-band.py`: `0d85c11bea2b0313e73caaac86c6bc0ed5614bd5a0f9968bec6a23a93034050f`
- `tools/mado-barfoot.py`: `8b17706014e6708a11413f0bd6c3398ca4e1b95b40b9c2d51f80f5064c677207`
- `.ufo/waves/round-83/controls/c1-cases-r83.json`: `e4409dabcf74f32307f14b31afb85091bca7d584771076bdb9a3b336bc9512c4`

These identify the current working files actually executed, not a claimed replay of a specific commit.

## Independent six-case derivation

Arithmetic is independent of the tool output: start with full usable `(x,y,w,h)=(0,0,3440,1440)`; all six have zero margins. Read source excerpts `.ufo/waves/round-80/fetch/S470.bin:2529-2665,2690-2696` and `.ufo/waves/round-79/fetch/S464.bin:264-292`. The former applies positive-exclusive passes before nonpositive passes, places each surface against the running usable box, and then subtracts its exclusive extent from that box. Top/left shift the origin; bottom/right only reduce size. The latter takes horizontal auto zone from allocation.height and vertical auto zone from allocation.width. Allocation resolution is the frozen declaration's input contract, not a number inferred from observed live geometry. Layer levels in these fixtures establish dock level 1 before bar level 2 before panel level 3; geometric position `bottom` does not make a level-3 surface run at layer level 1.

| Case | Ordered geometry and arithmetic | Expected reserve (left,top,right,bottom) / result |
|---|---|---|
| extra-dyn-band-top | Bar `(0,0,3440,26)` first leaves `(0,26,3440,1414)`; allocated panel height 40 yields `(0,26,3440,40)`, then top reserve 26+40. | `(0,66,0,0)`; band/expected/attributed 66; both boxes MATCH, CLEAN rc 0 |
| extra-dyn-band-dock | Level-1 dock width 60 fills height 1440 at `(0,0,60,1440)`, leaving `(60,0,3380,1440)`; level-2 bar is therefore `(60,0,3380,26)`. Reversing order would incorrectly leave the bar full-width and shorten/shift the dock. | `(60,26,0,0)`; top-axis band/expected/attributed 26 (not 86); both MATCH, CLEAN rc 0 |
| extra-dyn-band-explicit | Bar first leaves y=26. Allocation sets panel box height 40; explicit zone 40 independently reserves 40. Box `(0,26,3440,40)` is not the remaining usable height 1414. | `(0,66,0,0)`; band/expected/attributed 66; both MATCH, CLEAN rc 0 |
| extra-dyn-band-bottom | Level-2 top bar runs before level-3 bottom-position panel. Remaining y=26,h=1414 gives bottom y=26+1414-30=1410, hence `(0,1410,3440,30)`. Bottom reservation changes height, not y; final usable `(0,26,3440,1384)`. | `(0,26,0,30)`; top-axis band/expected/attributed 26 (not 56); both MATCH, CLEAN rc 0 |
| extra-dyn-band-zero-alloc | Dynamic panel height with explicit allocation 0 cannot provide its own band. Explicit exclusive=40 is not a substitute box height. | Model refusal rc 3, exact zero-height error below |
| alloc-two-namespaces | Allocation makes bar height 34 at `(0,0,3440,34)`, then panel height 40 at `(0,34,3440,40)`; remaining usable y=74,h=1366. Both namespace entries must resolve separately. | `(0,74,0,0)`; band/expected/attributed 74; both MATCH, CLEAN rc 0 |

All derived boxes, vectors, stages and return codes agree with frozen controls and observed output. Ordering caveat: the bottom case alone cannot distinguish reversing these two orthogonal horizontal-edge reservations, because their boxes and final reserve commute here; the dock case does distinguish ordering through cross-axis box changes. No additional ordering claim is inferred from bottom's pass alone.

## Exact retained six-case stdout

### extra-dyn-band-top (rc 0)

```text
MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=26 width=0 margins=0,0,0,0 exclusive=true surfaces=2
MADO_BARFOOT_STATIC: monitor=M1 top=0 right=0 bottom=0 left=0 source=none
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=0,0,3440,26 anchor=top+left+right zone=26
MADO_BARFOOT_LIVE: monitor=M1 level=2 ns=waybar box=0,0,3440,26 entries=1
MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=waybar edge=top contribution=26 box=0,0,3440,26
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=0,26,3440,40 anchor=top+left+right zone=40
MADO_BARFOOT_LIVE: monitor=M1 level=3 ns=panel box=0,26,3440,40 entries=1
MADO_BARFOOT_ATTR: monitor=M1 level=3 ns=panel edge=top contribution=40 box=0,26,3440,40
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=66 expected=66 attributed=66 gt=0,66,0,0 attr=0,66,0,0 ls=VALID verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
```

stderr: ""

### extra-dyn-band-dock (rc 0)

```text
MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=26 width=0 margins=0,0,0,0 exclusive=true surfaces=2
MADO_BARFOOT_STATIC: monitor=M1 top=0 right=0 bottom=0 left=0 source=none
MADO_BARFOOT_DECL: monitor=M1 level=1 ns=dock box=0,0,60,1440 anchor=left+top+bottom zone=60
MADO_BARFOOT_LIVE: monitor=M1 level=1 ns=dock box=0,0,60,1440 entries=1
MADO_BARFOOT_ATTR: monitor=M1 level=1 ns=dock edge=left contribution=60 box=0,0,60,1440
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=60,0,3380,26 anchor=top+left+right zone=26
MADO_BARFOOT_LIVE: monitor=M1 level=2 ns=waybar box=60,0,3380,26 entries=1
MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=waybar edge=top contribution=26 box=60,0,3380,26
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=60,26,0,0 attr=60,26,0,0 ls=VALID verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
```

stderr: ""

### extra-dyn-band-explicit (rc 0)

```text
MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=26 width=0 margins=0,0,0,0 exclusive=true surfaces=2
MADO_BARFOOT_STATIC: monitor=M1 top=0 right=0 bottom=0 left=0 source=none
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=0,0,3440,26 anchor=top+left+right zone=26
MADO_BARFOOT_LIVE: monitor=M1 level=2 ns=waybar box=0,0,3440,26 entries=1
MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=waybar edge=top contribution=26 box=0,0,3440,26
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=0,26,3440,40 anchor=top+left+right zone=40
MADO_BARFOOT_LIVE: monitor=M1 level=3 ns=panel box=0,26,3440,40 entries=1
MADO_BARFOOT_ATTR: monitor=M1 level=3 ns=panel edge=top contribution=40 box=0,26,3440,40
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=66 expected=66 attributed=66 gt=0,66,0,0 attr=0,66,0,0 ls=VALID verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
```

stderr: ""

### extra-dyn-band-bottom (rc 0)

```text
MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=26 width=0 margins=0,0,0,0 exclusive=true surfaces=2
MADO_BARFOOT_STATIC: monitor=M1 top=0 right=0 bottom=0 left=0 source=none
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=0,0,3440,26 anchor=top+left+right zone=26
MADO_BARFOOT_LIVE: monitor=M1 level=2 ns=waybar box=0,0,3440,26 entries=1
MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=waybar edge=top contribution=26 box=0,0,3440,26
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=0,1410,3440,30 anchor=bottom+left+right zone=30
MADO_BARFOOT_LIVE: monitor=M1 level=3 ns=panel box=0,1410,3440,30 entries=1
MADO_BARFOOT_ATTR: monitor=M1 level=3 ns=panel edge=bottom contribution=30 box=0,1410,3440,30
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,30 attr=0,26,0,30 ls=VALID verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
```

stderr: ""

### extra-dyn-band-zero-alloc (rc 3)

```text
MADO_BARFOOT: ERROR (stage=model panel 'top' was allocated a 0 height band; a zero band reserves nothing)
```

stderr: ""

### alloc-two-namespaces (rc 0)

```text
MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=0 width=0 margins=0,0,0,0 exclusive=true surfaces=2
MADO_BARFOOT_STATIC: monitor=M1 top=0 right=0 bottom=0 left=0 source=none
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=0,0,3440,34 anchor=top+left+right zone=34
MADO_BARFOOT_LIVE: monitor=M1 level=2 ns=waybar box=0,0,3440,34 entries=1
MADO_BARFOOT_ATTR: monitor=M1 level=2 ns=waybar edge=top contribution=34 box=0,0,3440,34
MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=0,34,3440,40 anchor=top+left+right zone=40
MADO_BARFOOT_LIVE: monitor=M1 level=3 ns=panel box=0,34,3440,40 entries=1
MADO_BARFOOT_ATTR: monitor=M1 level=3 ns=panel edge=top contribution=40 box=0,34,3440,40
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=74 expected=74 attributed=74 gt=0,74,0,0 attr=0,74,0,0 ls=VALID verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
```

stderr: ""

## Exact 58-case runner rows

Tuple columns: name, rc, box, reserved, band, expected, verdict, correct. Refusal rows carry null parsed RESULT fields; `correct=true` is the runner's stage/rc check.

```jsonl
["host-top", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["bottom-bar", 0, "MATCH", "EQ", 30, 30, "CLEAN", true]
["top-margin-int", 0, "MATCH", "EQ", 38, 38, "CLEAN", true]
["top-margin-css-2", 0, "MATCH", "EQ", 38, 38, "CLEAN", true]
["top-margin-asym", 0, "MATCH", "EQ", 42, 42, "CLEAN", true]
["bottom-margin", 0, "MATCH", "EQ", 46, 46, "CLEAN", true]
["left-margin", 0, "MATCH", "EQ", 52, 52, "CLEAN", true]
["right-margin", 0, "MATCH", "EQ", 46, 46, "CLEAN", true]
["right-zero-margin", 0, "MATCH", "EQ", 40, 40, "CLEAN", true]
["layer-bottom", 0, "MATCH", "EQ", 28, 28, "CLEAN", true]
["output-exclusion", 0, "MATCH", "EQ", 24, 24, "CLEAN", true]
["output-excluded", 3, "NOT_ON_MONITOR", "NOT_APPLIED", null, null, "NO_BAR", true]
["width-with-margins", 0, "MATCH", "EQ", 34, 34, "CLEAN", true]
["exclusive-false", 0, "MATCH", "NOT_APPLIED", 0, 26, "CLEAN", true]
["second-consumer", 0, "MATCH", "GT", 60, 34, "CLEAN", true]
["reserved-differ", 1, "MATCH", "DIFFER", 26, 34, "DIFFER", true]
["dynamic-cross", 3, null, null, null, null, null, true]
["negative-margin-refused", 3, null, null, null, null, null, true]
["static-composed", 0, "MATCH", "EQ", 60, 60, "CLEAN", true]
["static-other-edge", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["static-exclusive-false", 0, "MATCH", "NOT_APPLIED", 26, 52, "CLEAN", true]
["static-last-wins", 0, "MATCH", "EQ", 52, 52, "CLEAN", true]
["static-source-refused", 3, null, null, null, null, null, true]
["overlay-compose-top", 0, "MATCH", "EQ", 66, 66, "CLEAN", true]
["bottom-level-first", 0, "MATCH", "EQ", 66, 66, "CLEAN", true]
["same-level-order", 0, "MATCH", "EQ", 62, 62, "CLEAN", true]
["exclusive-edge-matched", 0, "MATCH", "EQ", 56, 56, "CLEAN", true]
["anchor-unmatched", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["overlay-unexclusive-full", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["ls-area-invalid", 0, "MATCH", "EQ", 0, 0, "CLEAN", true]
["negative-margin-skip", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["empty-box-skip", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["full-box-vs-usable", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["overflow-tie-negative", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["auto-dynamic-band-refused", 3, null, null, null, null, null, true]
["auto-corner-edge", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["auto-all-four-edge", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["auto-parallel-edge", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["auto-left-dock", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["alloc-dyn-height-top", 0, "MATCH", "EQ", 34, 34, "CLEAN", true]
["alloc-dyn-height-margin", 0, "MATCH", "EQ", 38, 38, "CLEAN", true]
["alloc-dyn-width-dock", 0, "MATCH", "EQ", 60, 60, "CLEAN", true]
["alloc-zero-refused", 3, null, null, null, null, null, true]
["alloc-negative-refused", 2, null, null, null, null, null, true]
["alloc-unknown-namespace", 2, null, null, null, null, null, true]
["alloc-explicit-ignored", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["alloc-composition-dyn-bar", 0, "MATCH", "EQ", 46, 46, "CLEAN", true]
["extra-dyn-band-top", 0, "MATCH", "EQ", 66, 66, "CLEAN", true]
["extra-dyn-band-dock", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["extra-dyn-band-explicit", 0, "MATCH", "EQ", 66, 66, "CLEAN", true]
["extra-dyn-band-bottom", 0, "MATCH", "EQ", 26, 26, "CLEAN", true]
["extra-dyn-band-zero-alloc", 3, null, null, null, null, null, true]
["alloc-live-band-differs", 1, "DIFFER", "EQ", 34, 34, "DIFFER", true]
["alloc-bool-refused", 2, null, null, null, null, null, true]
["alloc-two-namespaces", 0, "MATCH", "EQ", 74, 74, "CLEAN", true]
["bar-dyn-band-no-alloc", 3, null, null, null, null, null, true]
["alloc-live-box-differs-composed", 1, "DIFFER", "EQ", 34, 34, "DIFFER", true]
["bar-dyn-band-exclusive-false", 3, null, null, null, null, null, true]
```

## Boundaries, risks and cleanup

Only this report is a retained write. Scratch was removed before report publication; no driver/scaffold retained. LSP is unavailable in this seat's exposed tool inventory; no symbol refactor or implementation edit was performed. No blockers or case mismatches. This is not a lane-admission vote or a full predicate/mutation assessment; parent retains integration gates.

Self-evaluation: accuracy 4/5 (58 exact observations, but no full predicate replay); completeness 5/5 (58 cases plus six independent derivations); clarity 4/5 (full raw output deliberately lengthens report); actionability 5/5 (zero mismatches and exact byte bindings); conciseness 4/5 (raw retention costs space). Overall 4.4/5. Improvement: parent should reconcile the known declaration count against its chosen final instrument revision; do not substitute this case-only receipt for mutant/base/selftest evidence. User-agreement self-check: scope and limits are explicit.

Report: .ufo/waves/round-83/w1/R83ExecC1Cases.md
