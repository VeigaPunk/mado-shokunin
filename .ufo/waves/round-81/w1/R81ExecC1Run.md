# R81ExecC1Run — C1 run at the freeze + hand re-derivation (overflow-tie-negative, auto-left-dock)

## Verdict
The C1 claim holds at the freeze, and both named cases reproduce independently: hand arithmetic
from the pinned upstream sources (never reading `tools/mado-barfoot.py`) matches the frozen
expectations and the tool's live output field-for-field. **AGREE on every field for both cases.**

## 1. Counter run at the freeze (verbatim command)
Final line (full output: `w1/R81ExecC1Run/c1-run.txt`):

```
MADO_R81_BARFOOT: cases=39 correct=39 mutants=28 killed=28 base_correct=33/39 carried=33/33 tool_selftest=121/121 verdict=TARGET_MET rev=0e2ccd2a8692825cac534f57246053b276be9f13 tool_sha256=a129a435572805c3ae7730714f0dafdea2b9a7e420f53f0d109dc2d5f57d1230
```
Exit code: **0**. Base tool sha256 `5b9e2930…`, control sha256 `ab8154a1…` (matches declared frozen
prefixes); all 28 mutants `killed=yes`. Fresh output is **byte-identical** to the pinned receipt
`.ufo/waves/round-81/receipts/measurement-c1-r81.txt` (diff clean).

## 2. Hand re-derivation (sources only: S478.bin, S470.bin, S464.bin)

**overflow-tie-negative** — CBox::round (S478.bin :51-63) + arrangeLayerArray (S470.bin
:2615-2660). Panel anchored left+right, desired 1001×100, margins 0, usable after waybar's top-26
= (0,26,1000,774):
- box.x = 0 + (1000/2 − 1001/2) = **−0.5**; box.y = 26 + (774/2 − 100/2) = **363** (both_horiz ⇒ margins not applied).
- round(): round(−0.5) = **−1** (negative tie, half away from zero); newW = −0.5+1001+1 = 1001.5 ⇒ w = **1002**; h = 100. ⇒ box (−1,363,1002,100) == layers reply.
- applyExclusive gate (S470.bin :2568): exclusive 0 + margin 0 > 0 false ⇒ panel contributes nothing.
- Expected: `MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN` (rc 0, sole ATTR waybar top:26).

**auto-left-dock** — gtk-layer-shell auto zone (S464.bin :264-292) + applyExclusive (S470.bin
:2544-2573). Dock anchored left, 40×0, `exclusive: auto`, level 1:
- arrange ⇒ box (0,0,40,800) == layers reply; auto zone: horiz=false, vert=true ⇒ zone = allocation.width = **40** (margins 0).
- applyExclusive Left row: anchor==singular LEFT, 40+0 > 0 ⇒ usable.x += 40, w −= 40 ⇒ (40,0,960,800); waybar then sits at (40,0,960,26), its 26 on top.
- Expected: `MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=40,26,0,0 ls=VALID verdict=CLEAN` (rc 0, ATTR dock left:40 + waybar top:26).

## 3. Fixture replay vs hand derivation
Fixtures written byte-faithfully from the frozen control set into the scratch dir; tool run from
the freeze-rev bytes (sha256 a129a435…57d1230, working tree identical):
- `overflow-tie-negative`: `box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN`, rc=0, ATTR {waybar: top:26} — **AGREE, every field** (box/boxes/band/expected/attributed/gt/attr/ls/verdict/rc/attr_ns).
- `auto-left-dock`: `box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=40,26,0,0 ls=VALID verdict=CLEAN`, rc=0, ATTR {dock: left:40, waybar: top:26} — **AGREE, every field**.

Outputs: `w1/R81ExecC1Run/fixture-overflow-tie-negative.txt`, `w1/R81ExecC1Run/fixture-auto-left-dock.txt`.

## 4. Tool selftest
`python3 -I tools/mado-barfoot.py --selftest` ⇒ `MADO_BARFOOT_SELFTEST: 121/121`, rc=0
(`w1/R81ExecC1Run/c1-selftest.txt`).

## Risks / notes
- None observed. Fresh run == pinned receipt byte-for-byte; frozen hashes re-verified on disk.
- `tools/mado-barfoot.py` was never opened; the derivation and fixture comparison stand independent of the tool's internals.
- Scratch dir `/fast/scratch/hyaku/mado-r81/R81ExecC1Run` removed after receipts were copied into the seat dir. No tools installed.
