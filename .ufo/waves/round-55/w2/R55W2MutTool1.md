# R55W2MutTool1 — wave 2 (falsify), mutation test of `tools/mado-kbdopts.py` (C2)

Scope: device-over-global fallback, the D / G / - `from` letters, multi-file merge, same-name device block merge,
global-from-later-file. Full table, survivor configs and repro: `w2/R55W2MutTool1/mutants.md`; files:
`w2/R55W2MutTool1/mutants/` (22 mutant sources `Mxx.py`, diffs `Mxx.diff`, `orig/mado-kbdopts.py`, `harness.py`,
`matrix.py`, `repro.py`, `survivors/Sxx/`, `receipts/`).

## What ran

- Export (read-only): `git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive 57584ed67716340b3d466fa04333ac0bab3fb79e tools/mado-kbdopts.py .ufo/waves/round-55/fixtures .ufo/waves/round-55/fetch | tar -x -C /fast/scratch/hyaku/mado-r55/R55W2MutTool1`.
  Original sha256 `9c69dd62c1737d4842a4a0e73db3f8317eda71ee103e71ad3cda11a19c837c2e`.
- Harness (`mutants/harness.py`, `python3 -I`, cwd = scratch root, argv from `args.json`, stdout bytes and rc vs
  `expected.out` / `expected.rc`) over F01–F18 and H01–H08, plus `--selftest` per tool.
- Baseline: original 26/26 pass; selftest `83/83`, rc 0.
- 22 one-edit mutants (M01–M22) on scratch copies. Lane untouched; nothing restored in the lane because nothing was
  modified there. No git/jj mutation, no hyprctl, no installs, no subagents.
- Survivor configs (11) run against original and mutant: `mutants/receipts/survivor-repro.txt`, matrix
  `mutants/receipts/survivor-matrix.txt`, scores `mutants/receipts/harness-scores.jsonl`.

Not run: the frozen C2 harness itself (`MADO_R55_C2`, `ctl/` controls) — not in my assignment; the hold-out
commitment check — not in scope. The survivor fixtures are not added to the lane's fixture set (I am not an author and
did not write tracked files).

## Findings

1. **Fixture suite misses 11 of 22 one-edit mutants of this logic (BROKEN, coverage).** M07 M09 M10 M11 M12 M13 M16
   M18 M20 M21 M22 pass all 26 fixtures. Five of them (M12 M16 M20 M21 M22) also pass `--selftest`. Survivor
   configs S07 … S22 kill each one (the original's output is spec-derived; the mutant's is not). Notable: M16
   violates the frozen text "a second block with the same name merges, later keys win" and no committed or hold-out
   fixture has the same device key twice; M21 violates "`from` letters D/G/- say which" (device set → `D`) and no
   fixture has a device value equal to the global.
2. **Three mutants are killed only by hold-out fixtures (thin kill, noted).** M04 (device value equal to default must
   still win) → H03 only; M15 (nested `input { touchpad { … } }` keys are global) → H02 only; M17 (device key before its
   `name`) → H01 only. The 18 committed fixtures would pass all three.
3. **Original tool: no counterexample found (SURVIVES, instrument).** For each survivor config, the original's output
   matches the frozen §C2 text (registration.md §C2 and registration-v2.md E7; device lookup exact-match, device-block
   state reset per file, current device forgotten only when the stack empties, device value over global over default,
   letters D/G/-, same-name merge with later keys winning, live compare on the global). The unchanged instrument
   therefore does not reproduce a falsification of PRED-C2-r55 from these inputs. Every survivor input is frozen grammar:
   the survivors are inputs the original accepts and answers as specified; the defect is in the fixture suite.
4. **Empty NAME is a wording gap (UNVERIFIED wording, see S22).** `device { name = }` followed by `--keyboard ""`: the
   original creates device `""` and reports `from=D`. The frozen text does not discuss an empty NAME. The literal
   reading is what the original does; an L1 ruling is needed if an empty NAME should be unsupported.

## Per-target verdicts

| target | verdict | evidence |
|---|---|---|
| device-over-global fallback (priority; default) — original tool | SURVIVES | M01 M04 M14 killed; no spec-violating output of the unchanged tool on S-configs or 26 fixtures; `mutants.md` table |
| D/G/- letters — original tool | SURVIVES | M02 M03 M05 M19 killed by 6/22/2/16 fixtures; S21 shows the one letter gap (M21) |
| multi-file merge (device table and current device across files) — original tool | SURVIVES | M08 killed by F11; M07/M20 are fixture gaps only (S07, S20) |
| same-name device block merge — original tool | SURVIVES | M06 killed by F09; M16 is a coverage gap (S16) |
| global-from-later-file — original tool | SURVIVES | M08 killed by F11 and selftest |
| fixture suite detects one-edit mutants of this logic | BROKEN | 11/22 survive all 26 fixtures (S07 S09 S10 S11 S12 S13 S16 S18 S20 S21 S22) |
| PRED-C2-r55 falsified by the unchanged instrument via these inputs | NOT-REPRODUCED | original output agrees with §C2 text on all 11 survivor configs |

## Reproduce

```
mkdir -p /fast/scratch/hyaku/mado-r55/x && git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive 57584ed67716340b3d466fa04333ac0bab3fb79e tools/mado-kbdopts.py .ufo/waves/round-55/fixtures .ufo/waves/round-55/fetch | tar -x -C /fast/scratch/hyaku/mado-r55/x
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w2/R55W2MutTool1/mutants/harness.py /fast/scratch/hyaku/mado-r55/x /fast/scratch/hyaku/mado-r55/x/tools/mado-kbdopts.py
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w2/R55W2MutTool1/mutants && python3 -I repro.py
```
(`repro.py` reads `orig/` and the `M*.py` mutants and the survivor configs in this directory; it writes nothing.)

## Caveats

- Mutants are my one-line edits; other edit shapes could survive other tests. The table is a sample of the focus area,
  not an exhaustive mutant set.
- Selftest count: 83 on the committed tool; `R55ExecTool4.md` records 82. Not reconciled.
- Scratch `/fast/scratch/hyaku/mado-r55/R55W2MutTool1/` removed before yield.
