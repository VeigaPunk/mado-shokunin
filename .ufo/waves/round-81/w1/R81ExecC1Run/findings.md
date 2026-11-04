# R81ExecC1Run — C1 run at the freeze + hand re-derivation of two cases

Seat: R81ExecC1Run (round 81, wave 1). Lane root: /home/vgpnk/Projects/shokunin/mado-shokunin.
Freeze `0e2ccd2a8692825cac534f57246053b276be9f13`, base `c702094ace5dd9b2b5e152951b4b2f4dd578f8b6`.
Constraint honored: `tools/mado-barfoot.py` was never read; the hand model is built only from the
pinned upstream sources (S478.bin, S470.bin, S464.bin) and the frozen control set / counter.

## 1. Counter run, verbatim, at the freeze

Command (cwd = lane root), argv exactly as specified:

```
python3 -I quality/counters/c1-r81-overflow-auto.py --repo . --rev 0e2ccd2a8692825cac534f57246053b276be9f13 --base-rev c702094ace5dd9b2b5e152951b4b2f4dd578f8b6 --controls .ufo/waves/round-81/controls/c1-cases-r81.json --carried .ufo/waves/round-80/controls/c1-cases-r80.json --scratch-root /fast/scratch/hyaku/mado-r81/R81ExecC1Run
```

Full output saved as `c1-run.txt` (this dir). Final line and exit code:

```
MADO_R81_BARFOOT: cases=39 correct=39 mutants=28 killed=28 base_correct=33/39 carried=33/33 tool_selftest=121/121 verdict=TARGET_MET rev=0e2ccd2a8692825cac534f57246053b276be9f13 tool_sha256=a129a435572805c3ae7730714f0dafdea2b9a7e420f53f0d109dc2d5f57d1230
EXIT_CODE=0
```

Corroborating lines from the same run:

```
MADO_R81_CASE: name=overflow-tie-negative rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R81_CASE: name=auto-left-dock rc=0 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN correct=yes
MADO_R81_BASE: correct=33/39 rule=held-r79-model(no-multi-surface-arrangement) base_rev=c702094ace5dd9b2b5e152951b4b2f4dd578f8b6 base_sha256=5b9e2930005e1081454f46b8ba32deba4ba4ba81851482f90ce561926b42f0d9
MADO_R81_CONTROL: sha256=ab8154a1d4bc5d2a0f58bef8aeb675605e50ecfe932406b39b0a0c2df0533d52 carried=33/33
```

All 28 mutants report `killed=yes` (28/28). Fresh output is byte-identical to the pinned receipt:

```
$ diff .ufo/waves/round-81/receipts/measurement-c1-r81.txt <(grep -v '^EXIT_CODE=' .ufo/waves/round-81/w1/R81ExecC1Run/c1-run.txt) && echo 'DIFF: identical (receipt == fresh run)'
DIFF: identical (receipt == fresh run)
```

Frozen-instrument hashes re-verified on disk this seat:

```
ab8154a1d4bc5d2a0f58bef8aeb675605e50ecfe932406b39b0a0c2df0533d52  .ufo/waves/round-81/controls/c1-cases-r81.json
17c27157a9b0c293dbd07d56d67673cb061e808b6abcd1bb31f16ff6c15fd6ed  .ufo/waves/round-80/controls/c1-cases-r80.json
```

`git -C <lane> show 0e2ccd2a…:tools/mado-barfoot.py | sha256` = `a129a435572805c3ae7730714f0dafdea2b9a7e420f53f0d109dc2d5f57d1230` — matches the
declared frozen prefix `a129a435…` and equals the working-tree bytes (`worktree==frozen: True`).

## 2. Hand re-derivation (no reading of tools/mado-barfoot.py)

### overflow-tie-negative

Sources: hyprutils v0.14.0 `CBox::round` (S478.bin :51-63) and Hyprland `arrangeLayerArray`
(S470.bin :2609-2663; horizontal axis :2615-2624, `box.round()` at :2660).

Fixture facts: monitor M1 1000×800 scale 1.0, reserved [0,26,0,0]; waybar level 2, 1000×26 at
(0,0) with zone 26 on top; panel level 3, surface anchor [left,right], desired 1001×100,
exclusive 0, margins 0. Layers reply (ground truth): panel x=-1 y=363 w=1002 h=100.

Arithmetic:
- Usable area after waybar: x=0, y=26, w=1000, h=774.
- Horizontal (both_horiz branch, S470.bin :2619-2620): box.x = bounds.x + (bounds.width/2 − box.width/2) = 0 + (1000/2 − 1001/2) = 500 − 500.5 = −0.5.
- Vertical (no vertical anchor → else-center, :2634-2635): box.y = 26 + (774/2 − 100/2) = 26 + 337 = 363.
- Margins: both_horiz → `; // don't apply margins` (:2643); no vertical anchor and h≠0 → no vertical margin (:2650-2655 fall through). Margins are 0 regardless.
- `box.round()` (S478.bin :51-63, std::round = half away from zero):
  roundedX = round(−0.5) = −1  (the negative tie: trunc/banker's would give 0)
  newW     = x + w − roundedX = −0.5 + 1001 − (−1) = 1001.5 → w = round(1001.5) = 1002
  roundedY = 363; newH = 363 + 100 − 363 = 100 → h = 100
  ⇒ box (−1, 363, 1002, 100) — exactly the layers reply.
- `applyExclusive` (S470.bin :2568): panel exclusive=0 → gate `exclusive + margin > 0` is 0+0 > 0 = false ⇒ panel contributes no zone.

Expected RESULT line (hand-derived):

```
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN
```

with a single ATTR line `ns=waybar edge=top contribution=26`; band=expected=attributed=26 (waybar's
top 26 only), gt=attr=0,26,0,0, usable area after the band is 1000×774 > 0 ⇒ ls=VALID.

### auto-left-dock

Sources: gtk-layer-shell `layer_surface_update_auto_exclusive_zone` (S464.bin :264-292) and
Hyprland `applyExclusive` (S470.bin :2544-2573).

Fixture facts: monitor M1 1000×800, reserved [0,26,0,0]; dock level 1, anchor [left], width 40,
height 0, exclusive "auto"; waybar level 2, 960×26 at (40,0). Layers reply: dock 40×800 at (0,0).

Arithmetic:
- dock arrange (S470.bin): width≠0, not both_horiz, anchor&LEFT ⇒ box.x = bounds.x = 0 (:2620-2621); height==0 ⇒ box.y = bounds.y = 0 and box.height = bounds.height − (margin.top + margin.bottom) = 800 (:2646-2648) ⇒ box (0,0,40,800) — matches reply.
- gtk auto zone (S464.bin :267-289): horiz = (anchors[L]==anchors[R]) = false; vert = (anchors[T]==anchors[B]) = true; `vert && !horiz` ⇒ new_exclusive_zone = current_allocation.width = 40; anchors[L] true so no left margin added; anchors[R] false so += margins[R] = 0 ⇒ zone 40 sent to the compositor.
- `applyExclusive` (S470.bin :2568-2577): Left edge row — anchor == ZWLR_LAYER_SURFACE_V1_ANCHOR_LEFT matches the singular anchor, and exclusive(40) + marginLeft(0) > 0 ⇒ usableArea.x += 40, usableArea.width −= 40 ⇒ usable (40,0,960,800).
- waybar then arranges at (40,0,960,26) — matches reply — and takes its own 26 on top. The monitor's reserved vector keeps only waybar's 26: gt = 0,26,0,0; the dock's 40 lands on the left edge of the attr vector only.

Expected RESULT line (hand-derived):

```
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=40,26,0,0 ls=VALID verdict=CLEAN
```

with ATTR lines `ns=dock edge=left contribution=40` and `ns=waybar edge=top contribution=26`.

## 3. Fixture replay vs hand derivation

Fixtures written byte-faithfully from the frozen control set (config/layers/monitors/surfaces +
expect) into the scratch dir, tool = the freeze-rev bytes
(`git show 0e2ccd2a…:tools/mado-barfoot.py`, sha256 a129a435…57d1230). Command shape per case:

```
python3 -I mado-barfoot-frozen.py --config fixture-<name>/config.json --layers fixture-<name>/layers.json --monitors fixture-<name>/monitors.json --surfaces fixture-<name>/surfaces.json
```

Full outputs saved as `fixture-overflow-tie-negative.txt` / `fixture-auto-left-dock.txt` (this dir).

overflow-tie-negative — tool RESULT (rc=0):
`box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN`; ATTR `ns=waybar edge=top contribution=26` (sole ATTR).
Field-by-field vs §2 hand values: box ✓ boxes ✓ band 26 ✓ expected 26 ✓ attributed 26 ✓ gt ✓ attr ✓ ls VALID ✓ verdict CLEAN ✓ rc 0 ✓ attr_ns {waybar: top:26} ✓. Also DECL/LIVE box −1,363,1002,100 ✓ (negative tie realized). ⇒ AGREE, every field.

auto-left-dock — tool RESULT (rc=0):
`box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=40,26,0,0 ls=VALID verdict=CLEAN`; ATTR `ns=dock edge=left contribution=40` + `ns=waybar edge=top contribution=26`.
Field-by-field vs §2 hand values: box ✓ boxes ✓ band 26 ✓ expected 26 ✓ attributed 26 ✓ gt ✓ attr ✓ ls VALID ✓ verdict CLEAN ✓ rc 0 ✓ attr_ns {dock: left:40, waybar: top:26} ✓. DECL dock box 0,0,40,800 zone=40 ✓; waybar box 40,0,960,26 ✓. ⇒ AGREE, every field.

Both RESULT lines also equal the frozen `expect` blocks of the two control cases field-for-field.

## 4. Tool selftest

Command:

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py --selftest
```

Output (saved as `c1-selftest.txt`):

```
MADO_BARFOOT_SELFTEST: 121/121
rc=0
```

## Commands run (exact argv)

1. `mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/w1/R81ExecC1Run /fast/scratch/hyaku/mado-r81/R81ExecC1Run`
2. `python3 -I quality/counters/c1-r81-overflow-auto.py --repo . --rev 0e2ccd2a8692825cac534f57246053b276be9f13 --base-rev c702094ace5dd9b2b5e152951b4b2f4dd578f8b6 --controls .ufo/waves/round-81/controls/c1-cases-r81.json --carried .ufo/waves/round-80/controls/c1-cases-r80.json --scratch-root /fast/scratch/hyaku/mado-r81/R81ExecC1Run` (cwd = lane root; stdout+stderr → c1-run.txt)
3. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0e2ccd2a8692825cac534f57246053b276be9f13:tools/mado-barfoot.py` (read-only; piped to sha256 → a129a435…57d1230)
4. python3 heredoc: extract the two control cases → fixture-*/{config,layers,monitors,surfaces,expect}.json under the scratch dir (byte-faithful json.dump of the frozen case dicts)
5. `python3 -I mado-barfoot-frozen.py --config fixture-overflow-tie-negative/config.json --layers fixture-overflow-tie-negative/layers.json --monitors fixture-overflow-tie-negative/monitors.json --surfaces fixture-overflow-tie-negative/surfaces.json` (cwd = scratch dir; → fixture-overflow-tie-negative.txt)
6. same argv with `fixture-auto-left-dock` (→ fixture-auto-left-dock.txt)
7. `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py --selftest` (→ c1-selftest.txt)
8. `diff .ufo/waves/round-81/receipts/measurement-c1-r81.txt <(grep -v '^EXIT_CODE=' .ufo/waves/round-81/w1/R81ExecC1Run/c1-run.txt)` → identical
9. `sha256sum .ufo/waves/round-81/controls/c1-cases-r81.json .ufo/waves/round-80/controls/c1-cases-r80.json`

No tools installed or upgraded (none needed). Scratch dir removed after receipts were copied into
this seat dir.

STATUS: ok
