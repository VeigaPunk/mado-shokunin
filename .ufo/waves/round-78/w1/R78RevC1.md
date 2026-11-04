# R78RevC1 — C1 byte-fidelity review (margined auto exclusive-zone join)

Seat: R78RevC1 · lane: mado-shokunin · round 78 · wave 1 · 2026-11-04
Method: independent re-derivation from a clean scratch (`/fast/scratch/hyaku/mado-r78/R78RevC1/`,
deleted after review). No repo writes; no mutating git/jj. All commands read-only.

## Verdict

The frozen C1 claim **holds on every independently re-derived count**. Tool bytes match the
pinned digests at both revisions; the counter re-run reproduces the committed receipt on every
count line; all seven mutation anchors are byte-unique in the tool and each kill is a
declared-case value/refusal mismatch with zero crashes; all eighteen case expectations are
forced by the two pinned source functions plus two source-backed assumptions I name below.
Two receipt-provenance notes (non-blocking) are recorded in §6.

## 1. Tool byte fidelity

Commands (cwd = reviewer scratch, `REPO=/home/vgpnk/Projects/shokunin/mado-shokunin`):

    git -C $REPO show 44a36b64:tools/mado-barfoot.py            > extract/tool-44a36b64.py
    git -C $REPO show f597eccbffefd5fd6bbb01f3511c88bbeaed493c:tools/mado-barfoot.py > extract/tool-f597eccb.py
    sha256sum extract/tool-44a36b64.py extract/tool-f597eccb.py

Observed:

    aac5d41b923711e174c6d62bb24da5a2b53abf7c938bfc5b68816929a12009c0  tool-44a36b64.py   # == pinned r78-v1
    e54787b75645a97780984aa1e5bf9187b81b400b42ea5b0e04cb46387769b093  tool-f597eccb.py   # == held r77 base (receipt line 27)

`diff -q extract/tool-44a36b64.py $REPO/tools/mado-barfoot.py` → identical (working tree is the
frozen instrument). Pinned supporting bytes also verified in-tree:
`quality/counters/c1-r78-margins.py` = 1c39a53c…85000, `.ufo/waves/round-78/controls/c1-cases-r78.json`
= 99f1d82f…56ae, `S457.bin` = 9af8a74e…, `S464.bin` = deef9c81… (per `.ufo/waves/round-78/fetch/sha256-r78.txt`),
and `S457/S462/S464.bin` are byte-identical to the round-77 pinned copies.

## 2. Counter re-derivation vs committed receipt

Command (clean scratch root, absolute paths):

    python3 -I $REPO/quality/counters/c1-r78-margins.py --repo $REPO --rev 44a36b64 \
      --base-rev f597eccbffefd5fd6bbb01f3511c88bbeaed493c \
      --controls $REPO/.ufo/waves/round-78/controls/c1-cases-r78.json \
      --scratch-root $SCR/c1          # rc=0

`diff` of my stdout against `.ufo/waves/round-78/receipts/measurement-c1-r78.txt`:
**28 lines compared, 27 identical.** Every count matches: cases=18, correct=18,
mutants=7 killed=7 with per-mutant scores 9/18, 9/18, 17/18, 16/18, 17/18, 17/18, 17/18,
base_correct=8/18, tool_selftest=22/22, verdict=TARGET_MET, tool_sha256=aac5d41b…,
control sha256=99f1d82f…. The single differing field is `rev=` on the summary line
(§6 note 1). I additionally scored the extracted base tool per-case on the frozen set:
correct = host-top, bottom-bar, right-zero-margin, layer-bottom, output-exclusion,
output-excluded, exclusive-false, dynamic-cross (8/18) — the same eight the baseline
receipt records.

Generator fidelity: `python3 -I controls/make-cases-r78.py --out regen.json` reproduces the
frozen control set byte-identically (sha256 99f1d82f…56ae on both). Expectations are authored
from the rules, not captured from a tool run.

## 3. Mutation anchors vs tool bytes; kill provenance

Authoritative check: imported `MUTATIONS` from the committed counter
(`quality/counters/c1-r78-margins.py:23-43`) via importlib and counted each anchor in
`tool-44a36b64.py`. All seven anchors occur **exactly once**; each replacement changes the
named rule:

| mutant | tool line (44a36b64) | rule changed |
|---|---|---|
| opposite-margin-dropped | 411 `expected = extent + bar["margins"][OPPOSITE_EDGE[edge]]` | drops the unanchored-edge margin from the composed band |
| horizontal-margin-leak | 411 (same anchor, different replacement) | adds left+right margins on the band axis |
| level-bottom-swap | 60 `LEVEL = {"background":0,"bottom":1,"top":2,"overlay":3}` | bottom layer looked up on level 2 |
| right-extent-flip | 315 `return mon_w - box["x"]` | right-edge extent becomes `x+w` |
| per-side-margin-dropped | 187 `sides[side] = value if isinstance…else 0` | per-side margins forced to 0 |
| negative-margin-accepted | 253 `if any(value < 0 for value in margins.values()):` | negative-margin refusal removed |
| opposite-edge-wrong | 69 `OPPOSITE_EDGE = {…}` | opposite edge mapped to itself |

Kill provenance (my per-case runs of each mutant over the 18 frozen cases; mechanism = parsed
RESULT fields differing vs the case's declared expectation, or a declared refusal path):

- **opposite-margin-dropped** 9/18 — flips exactly the nine margin-carrying cases
  (top-margin-int, top-margin-css-2, top-margin-asym, bottom-margin, left-margin, right-margin,
  width-with-margins → GT on band; second-consumer → GT; reserved-differ → DIFFER). Zero-margin
  cases survive, as designed.
- **horizontal-margin-leak** 9/18 — flips the same nine (top/bottom cases over-add left+right:
  e.g. top-margin-int expected 42 vs band 38 → DIFFER). 
- **level-bottom-swap** 17/18 — flips only `layer-bottom` (lookup moves to level 2 → NO_LAYER,
  rc 3). This is the declaration's named `layer: bottom` gap.
- **right-extent-flip** 16/18 — flips only `right-margin` and `right-zero-margin`
  (expected 3440/1920 vs band 46/40 → DIFFER). Named right-anchored gap.
- **per-side-margin-dropped** 17/18 — flips only `top-margin-asym` (declared box y=0 vs live
  y=10 → box DIFFER).
- **negative-margin-accepted** 17/18 — flips only `negative-margin-refused`: refusal removed,
  mutant composes band 22 vs fixture 24 → GT. Named negative-margin gap.
- **opposite-edge-wrong** 17/18 — flips only `top-margin-asym` (uses margin.top instead of
  margin.bottom: expected 50 vs band 42 → DIFFER). Interesting and correct: it is the one case
  where the two vertical margins differ.

No mutant survives; **no kill is by crash** — every flipped case emitted a parseable
`MADO_BARFOOT_RESULT` line or a declared error line, all rc ∈ {0,1,3} per the tool's exit map,
and no stderr contained a traceback. All kills come from declared cases.

## 4. Model vs the two source functions, line by line

Pinned sources: `.ufo/waves/round-78/fetch/S464.bin` (gtk-layer-shell 0.10.1
`layer-surface.c`) and `S457.bin` (Hyprland v0.56.2 `Renderer.cpp`); both sha-verified.

**gtk auto zone** — `layer_surface_update_auto_exclusive_zone`, S464.bin:264-296: for a
horizontal surface (`anchors[LEFT]==anchors[RIGHT]`, i.e. both-or-neither, and top/bottom
disagreeing) the zone is `allocation.height` plus the margin of each *unanchored* vertical
edge (`if (!anchors[TOP]) += margin.top; if (!anchors[BOTTOM]) += margin.bottom`,
lines 276-280); transposed for vertical (lines 282-286). If neither branch applies the zone
is left unchanged. → matches the tool's `OPPOSITE_EDGE` table (tool:69) and
`expected = extent + margins[OPPOSITE_EDGE[edge]]` (tool:411).

**Hyprland side** — `applyExclusive`, S457.bin:2529-2585: for the anchored singular edge,
`usableArea` shrinks by `exclusive + margin` (e.g. top: `y += exclusive + marginTop`,
lines 2546-2552; guard `exclusive + margin > 0`, line 2575). `arrangeLayerArray`
(S457.bin:2587-2668) places the box (width 0 → full usable width minus left/right margins,
lines 2626-2634; anchored edge gets that edge's margin; both cross anchors cleared → centred,
no margins, lines 2636-2643), then calls `applyExclusive` with the four margins (line 2664).
A centred top bar therefore has extent `margin.top + height` and the join adds
`margin.top` (Hyprland, anchored) + `margin.bottom` (gtk, unanchored) =
`extent + margins[OPPOSITE_EDGE]` — the tool's line 411 reproduces both functions exactly,
including the `exclusive <= 0` early-return (S457.bin:2533-2535 ↔ tool exclusive-false case,
band 0 / NOT_APPLIED).

**Reply order** — `HyprCtl.cpp` print order `m_reservedArea.left(), top(), right(), bottom()`
at `S458.bin:281-282` backs the tool's `RESERVED_INDEX` (tool:65). The declaration cites only
S457/S464; the join's fourth input is pinned anyway.

**Per-case force** (all 18 verified arithmetically against the fixtures):

| case | forced value | by |
|---|---|---|
| host-top | band=extent 26+0 = reserved[1] 26 | gtk h; hypr +0 |
| bottom-bar | 30 = reserved[3] | gtk h; hypr +0 |
| top-margin-int | 38 = 30+4(top extent)+4(bottom) | join |
| top-margin-css-2 | 38 (margin "4 8": top/bottom=4) | join + CSS 2-value rule |
| top-margin-asym | 42 = 40+2 | join with per-side margins |
| bottom-margin | 46 = 38+8 | join |
| left-margin | 52 = 46+6 (reserved[0]) | join transposed |
| right-margin | 46 = 41+5 (reserved[2]) | join transposed |
| right-zero-margin | 40 = 40+0 | join transposed |
| layer-bottom | level 1 fixture; band 28 | LEVEL map = wlroots order |
| output-exclusion | !M2 excludes only M2; band 24 | exact-name/!exclusion subset |
| output-excluded | NO_BAR rc 3 | exclusion match |
| width-with-margins | box (1320,4,800,26); band 34 | centred box + join (see A1) |
| exclusive-false | band 0, NOT_APPLIED | applyExclusive early-return |
| second-consumer | 60 > 34 → GT, rc 0 | reserved area accumulates consumers |
| reserved-differ | 26 < 34 → DIFFER, rc 1 | same |
| dynamic-cross | refusal rc 3 | model boundary (declared) |
| negative-margin-refused | refusal rc 3 | model policy (declared) |

## 5. Assumptions the declaration does not state

- **A1 — waybar anchor selection for narrow bars.** `width-with-margins` requires waybar to
  clear the side anchors when `width` is set (compositor centres the surface; Hyprland
  S457.bin:2636-2643 "don't apply margins" branch). The generator docstring says "Waybar
  anchors a top bar TOP|LEFT|RIGHT", which is literally inconsistent with its own centred
  fixture; the band still composes the same because gtk's zone adds the unanchored vertical
  margins in both branches. Source: waybar 0.15.0 `bar.cpp` — **not pinned this round**.
  Mitigation: the case's box MATCH pins the fixture box to the tool's declared box, so any
  anchor regression is caught; the band formula itself is anchor-insensitive here.
- **A2 — waybar margin precedence** (per-side > CSS 1-4-value string > integer; bools
  rejected). Stated in the tool docstring (tool:170-176) and exercised by cases 3-9, but the
  pinned sources are gtk/Hyprland only; waybar `bar.cpp` is again unpinned.
- **A3 — `exclusiveEdge` never set.** `applyExclusive` also shrinks on
  `exclusiveEdge == singular_anchor` (S457.bin:2575); the model assumes waybar never calls
  `gtk_layer_set_exclusive_edge`. Cases cannot distinguish this; consistent with waybar's
  documented config surface.
- **A4 — layer-name→level map** (`bottom`=1, `top`=2) follows the wlroots layer order both
  sides already share; fixture-verified by `layer-bottom`, but the declaration does not say it.
- A5 (minor): EQ-case fixture `reserved` arrays are authored equal to the composed band. This
  is not circular: the fixture is frozen input and the tool must reproduce 38 against it;
  base-tool rows in the same receipts show the counter separates models (8/18 with
  UNMODELLED/DIFFER verdicts on the margin cases).

None of A1-A4 weakens the claim; all are test-covered by the frozen cases or pinned sources.

## 6. Receipt provenance notes (non-blocking)

1. `measurement-c1-r78.txt` summary line carries `rev=d27c5ff4…`, not `44a36b64` — the receipt
   was rendered when the wave HEAD had already moved. Verified: `git diff 44a36b64 d27c5ff4 --
   tools/mado-barfoot.py quality/counters/c1-r78-margins.py …/c1-cases-r78.json` is empty and
   `git show d27c5ff4:tools/mado-barfoot.py | sha256sum` = aac5d41b… — the measured bytes are
   identical, so every count stands. My re-run at `--rev 44a36b64` met TARGET_MET (rc 0).
2. `control-baseline-c1-r78.txt` records `MADO_R78_CONTROL: sha256=d19c20e2…` — the pre-freeze
   baseline ran against the pre-amendment case set, not the frozen 99f1d82f set. The do-nothing
   separation is nonetheless re-established on the frozen bytes: the current receipt and my
   re-run both score the base tool 8/18 on 99f1d82f, and the passing set is identical
   (§2). The declaration's phrase "same counter and case set" is true of the count, not of the
   control-set bytes frozen in that receipt.

## 7. Residual risk

The only un-pinned inputs to the model are waybar-side behaviors (A1, A2); every other rule is
anchored in sha-verified bytes (S457/S458/S464 this round, byte-identical to round-77). The
seven mutants kill narrowly (five of seven by a single case), which is appropriate for
single-anchor mutations of a well-frozen rule; no equivalent-class mutant was observed to
survive. No actionable defect found.
