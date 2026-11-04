# R80ScribeEntry — round-80 knowledge entry: the layer-surface composition under the band

Seat: scribe (leaf member; no subagent dispatch). Lane: mado-shokunin. Round: 80, ONE v1 wave.
Freeze `6c302a53eb8f577e83fbcadc01e05a286778df8e`; base `e10f7e9f528b13195a1cdde28a68a702af3045c4`.

## Deliverable

- Draft: `.ufo/waves/round-80/w1/R80ScribeEntry/bar-footprint-composition-r80.md` — 320 lines,
  sha256 `732e5deabbb6c300b4395bd024528ce4e11c8c1e553eaa2ec66da0827a9b9485`.
- Intended adoption path: `corpus/knowledge/bar-footprint-composition-r80.md`. **Not written by
  this seat**: corpus is read-only under the round's bounds. The path is already occupied — see F3.
- Coverage of the seat's requirements: the provenance trio comes first (`source:` S470/S471/S472
  plus held S457/S459/S466/S465; `verified-at:` the freeze commit; `recheck:` a runnable
  command); §1–§7 are one section per model rule (level order and the running usable box; the
  exclusive/non-exclusive pass split and `bounds` for `exclusive == -1`; the four-rule match order
  and the `exclusiveEdge`/anchor/triplet condition; the `zone + margin > 0` guard; the empty-box
  skip; the single `CReservedArea{ORIGINAL, usable}` total and its early return; no per-surface
  attribution); §8 is the ten-case table; §9 the measurement, the 22 mutants and a
  number/command/revision table; §10 the limits (the five required non-claims plus five more);
  §11 evidence. No credential material, no `op://`, no clock time without a UTC mark.

## Verified before writing (read-only)

| check | command | result |
|---|---|---|
| pins | `cd .ufo/waves/round-80/fetch && sha256sum -c sha256-r80.txt` | `S470.bin`–`S472.bin`, `S473.txt`, `S474.txt`: `OK` (5/5) |
| freeze tool | `git show 6c302a53:tools/mado-barfoot.py \| sha256sum` | `c3eb5fbef794c92ba45adc85ed1dcd18c505a2776a3fb1db34742a6eed27fa99` (matches the receipt) |
| base tool | `git show e10f7e9f:tools/mado-barfoot.py \| sha256sum` | `9e274157…`; `VERSION = "r79-v1"`; zero occurrences of `surfaces` (no `--surfaces` option) |
| control set | `sha256sum …/controls/c1-cases-r80.json`; `python3 -c '…len(…["cases"])'` | `17c27157…` (matches `MADO_R80_CONTROL`), 33 cases, first 23 parsed-equal to the r79 set |
| counter | `sha256sum quality/counters/c1-r80-multisurface.py`; `--selftest` | `6268667c…`; `MADO_R80_BARFOOT_SELFTEST: 60/60`, rc 0 |
| held pins | `sha256-r79.txt` | `S470.bin` bytes == `S457.bin` (`9af8a74e…`); `S459.bin` == `S466.bin` (`0a52e145…`) |
| source anchors | line-numbered reads of S470/S471/S472/S465/S466 | `applyExclusive` :2529-2585, table :2534-2573, condition :2575, axes :2577-2582, break :2583; `arrangeLayerArray` :2587-2671, bounds :2588/:2599-2603, empty skip :2655-2658, round :2660, apply :2664; `arrangeLayersForMonitor` :2673-2702, reset :2680, ORIGINAL :2682, sort :2685-2688, passes :2690-2694, addType :2696; S466 :19-31/:33-34/:43-51/:53-60/:69-74/:80-94/:101-112; S472 :26-30/:32-38/:40-52/:53-54; S465 :654/:1768-1770/:1772-1774 |
| lane state | `git rev-parse HEAD`; `git log -1 -- corpus/knowledge/bar-footprint-composition-r80.md` | `b65f3227…` (parent `6c302a53`); the corpus entry was committed at `b65f3227` |

I did **not** run the C1 counting command: every published score is copied from
`.ufo/waves/round-80/receipts/measurement-c1-r80.txt` (after) and
`receipts/control-c1-r80-at-base.txt` (before) at the revisions they name. My only executions were
the counter selftest above and the F1 probe below.

## Findings

### F1 — instrument defect (unexercised): `box=` can name another surface's verdict

`tools/mado-barfoot.py` (`r80-v1`), `evaluate_composition`, line 785:

```python
    bar_box = boxes[order.index(0)] if 0 in order else "NO_LAYER"
```

`boxes` is appended in **arrangement-sequence** order (the exclusive pass, then the non-exclusive
pass, line 715), but `order` is the **level/order-sorted** list. The two positions coincide only in
two narrow cases (an exclusive bar with no non-exclusive surface before it in `order`; a
non-exclusive bar with no exclusive surface after it). Whenever they differ — a non-exclusive
surface sorting before an exclusive bar, or a non-exclusive bar with an exclusive surface sorting
after it — `order.index(0)` indexes the wrong entry of `boxes`, so the printed `box=` field
reports another surface's verdict.

Probe (scratch only; bar `exclusive: false`, live bar box altered to make its verdict `DIFFER`,
panel exclusive and matching):

```
$ python3 -I tool-r80.py --config probe/config.json --layers probe/layers.json \
    --monitors probe/monitors.json --monitor M1 --surfaces probe/surfaces.json
MADO_BARFOOT_DECL: monitor=M1 level=2 ns=waybar box=0,40,1000,26 anchor=top+left+right zone=0
MADO_BARFOOT_LIVE: monitor=M1 level=2 ns=waybar box=0,0,1000,30 entries=1
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,DIFFER reserved=EQ band=40 expected=40 \
  attributed=40 gt=0,40,0,0 attr=0,40,0,0 ls=VALID verdict=DIFFER
```

`boxes=MATCH,DIFFER` shows the bar's own box verdict is `DIFFER`; `box=MATCH` is the panel's.
Impact: the `box=` field only. The `verdict` is computed from any `DIFFER`/`NO_LAYER` and stays
correct, and no frozen case reaches the configuration: the composition path runs only for the ten
cases that pass `--surfaces`, all ten use an exclusive bar, and in none of them does the bar's
position in the level/order list differ from its position in the arrangement sequence. Fix (not
applied; the instrument is frozen): record the bar's index when `boxes` is appended, or look it up
in `sequence`. Reported for the L1 to fix or name.

### F2 — counter docstring drift (documentation only)

`quality/counters/c1-r80-multisurface.py:12-14` prints a contract of `cases=30 correct=30 …
base_correct=23/30`; the executable constants are `CASES = 33`, `CARRIED = 23`,
`BASE_EXPECT = 23`, and the receipt prints `cases=33 … base_correct=23/33`. A reader quoting the
docstring would misstate the claim. Same class as the round-80 lesson's M80-1 (a quoted line that
does not match the artifact), though it does not move any score.

### F3 — the target path is already occupied by a committed entry

`corpus/knowledge/bar-footprint-composition-r80.md` exists in the lane at HEAD (`b65f3227…`, the
round-80 landing commit; blob `327f5400139700874b19819be505ce6032049230`, 147 lines). It was added
by that landing commit itself, not by a seat directory, and the round's lesson records only two
seats settled (`R80ScoutLive`, `R80ConnSiblings`). It is not mine and this seat did not touch it.
Verified defects in it, each checked against the pinned bytes:

1. Line 39: "`box.round()` follows (:2653)" — `box.round()` is at S470 :2660; :2653 is the
   closing brace of the margin block.
2. Line 91: "`ReservedArea.cpp:11-15, 37-48, 88-99`" — the constructors are :10-17, `calculate`
   :43-51, the accessors :80-94 (S466 pin).
3. Line 3 `source:` names `S473, S474` — the two C2 rows — in the C1 entry, and the body cites
   `S464` (line 83) and `S458` (line 92) without listing either.
4. Line 65: "(S470 :2575-2576)" for the match condition; the condition is the single line :2575.
5. §7 item 4 conflates a cross-axis overflow with the join's integer centring ("a box wider than
   the bounds is arranged by the compositor but the join's centring arithmetic is integer-only").

The draft in this seat's directory is a complete replacement for that file; whether to replace it
is the L1's decision.

### F4 — `preview_scale` has no pin in this round

`grep -rl preview_scale .ufo` returns only the wave machinery
(`make-spec-r80.py`, `w1-spec.json`, `w1-dispatch.json`); no fetch pin in round 78, 79 or 80
mentions it, and neither tool nor counter has a field for it. The draft therefore names it as
unmodelled without asserting a mechanism (required by the seat spec). If the entry is to explain
*what* `preview_scale` does, a new row is needed first.

### F5 — the host cannot confirm the attribution

Today's host has one exclusive surface (`waybar`) plus the non-exclusive `wallpaper`
(`live-join-r80.txt`, `attributed=26 gt=0,26,0,0`). The composition path is exercised; a second
*exclusive* band has never been observed. This is already §10 item 1 of the draft, not a new
defect.

## Conflicts reported verbatim

1. Counter contract vs constants (`quality/counters/c1-r80-multisurface.py:12-13`):
   `Contract: MADO_R80_BARFOOT: cases=30 correct=30 mutants=22 killed=22 base_correct=23/30`
   / `carried=23/23 tool_selftest=p/n verdict=TARGET_MET rev=<hash> tool_sha256=<sha>`
   vs the receipt: `MADO_R80_BARFOOT: cases=33 correct=33 mutants=22 killed=22 base_correct=23/33`.
2. Committed entry vs pinned source (`corpus/knowledge/bar-footprint-composition-r80.md:39`):
   "`box.round()` follows (:2653)." vs S470 :2660 `box.round(); // fix rounding errors`.
3. Committed entry vs pinned source (`:91`):
   "(`ReservedArea.cpp:11-15, 37-48, 88-99`, held S466)" vs S466 :10-17, :43-51, :80-94.
4. Declaration paraphrase vs r79 entry (`claims-declaration-r80.md`, C1 section):
   the round-79 entry named this ground `NOT_MODELLED` "(…§limits: "a band overflow on the cross
   axis" and no second consumer)" — `grep -c cross corpus/knowledge/bar-footprint-reserve-r79.md`
   → `0`; the closest sentence is r79 `:95`, in §5 R2, not §limits: "a band that overflows the
   usable axis was still expected (the parent/child short-circuit returns zeros, S459 :19-30)".
   The draft does not quote the missing phrase.

## Out of scope / not done

- No C2 content (the runbook entry is another seat's ground); no SOURCES row drafting
  (`R80ScribeSources`).
- No edit to `corpus/`, the frozen instruments, the control sets, `SKILL.md`, `SCORECARD.md`,
  `LOG.md`, `corpus/`, the fleet repo or a sibling lane. No mutating git/jj command; the git calls
  above are `show`/`rev-parse`/`log`/`status` only.
- The C1 counting command was not re-run; the draft cites the committed receipts and names them.
- No host probe beyond reading the committed capture.

## Scratch

`/fast/scratch/hyaku/mado-r80/R80ScribeEntry/` (freeze tool copy, `probe/` fixtures) — removed
before finishing; the probe output is quoted above.

STATUS: ok — the draft is complete and self-contained; the L1 must decide whether to replace the
already-committed 147-line entry at the adoption path (F3) and whether to fix the `box=` index
(F1) before any documentation of that field relies on it.
