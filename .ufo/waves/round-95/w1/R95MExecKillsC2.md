# R95MExecKillsC2 — C2 kill-sets for mado-mimeglob.py and mado-portals.py (round 95, wave w1)

Status: COMPLETE. All DRAFT runs are labelled DRAFT; no measurement is claimed (measured scoring happens only after the L1 freezes).

## Deliverables (files written)

- `.ufo/waves/round-95/build/mado-mimeglob-kills.c2.json` — 17 kills, `selftest_checks: 19`
- `.ufo/waves/round-95/build/mado-portals-kills.c2.json` — 27 kills, `selftest_checks: 28`
- `.ufo/waves/round-95/w1/R95MExecKillsC2.md` — this report

No other lane file was touched. No installs were performed (none needed; nothing added to PATH dirs). No pacman transactions.

## Input verification

- `sha256sum` of the two tools matched the declared hashes:
  - `tools/mado-mimeglob.py` = `65f80a6cb1551bb722ae7608df04fb17deba1b5cd05bef6f7fdd79bed76e2453`
  - `tools/mado-portals.py` = `e46a861e6a8ab62e26671169e201b953ca629a3861c6dddc74fd89b73b2ac021`
- First text occurrence of `def selftest(` (the gate's `non_selftest_prefix` cut): mado-mimeglob.py line 585, mado-portals.py line 575. Every `find` in both kill-sets lies before that line and occurs exactly once in the whole tool (asserted by the driver; the gate independently asserts prefix-count == 1).
- Unmutated baselines (DRAFT): mado-mimeglob `MADO_MIMEGLOB_SELFTEST: checks=19 failed=0` rc 0; mado-portals `MADO_PORTALS_SELFTEST: checks=28 failed=0` rc 0.

## Method

For each kill: copy the tool to `$S/mut*/<id>.py` with the single find→replace applied, run `python3 -I <copy> --selftest` (TMPDIR set to the scratch dir), and record rc + the exact `*_SELFTEST_FAIL:` label lines. `must_fail` is verbatim that measured label set; the gate compares it as an unordered set (`sorted(fails) != sorted(must_fail)` → WRONG_CHECK), which all kills satisfy. Every kill was held by an actual run; nothing is predicted-only.

## Gate control runs (DRAFT, unmodified tools, rc recorded)

```
python3 -I quality/check-selftest-strength.py --tool tools/mado-mimeglob.py \
  --kills .ufo/waves/round-95/build/mado-mimeglob-kills.c2.json --scratch-root $S/gate-mimeglob
SELFTEST_STRENGTH: OK tool=tools/mado-mimeglob.py kills=17 held=17 survived=0 wrong_check=0   # rc 0

python3 -I quality/check-selftest-strength.py --tool tools/mado-portals.py \
  --kills .ufo/waves/round-95/build/mado-portals-kills.c2.json --scratch-root $S/gate-portals
SELFTEST_STRENGTH: OK tool=tools/mado-portals.py kills=27 held=27 survived=0 wrong_check=0   # rc 0
```

## Label coverage — mado-mimeglob (19/19)

Singletons: t02←g01, t03←g02, t04←g03, t05←g04, t06←g13, t07←g05b, t08←g06, t09←g07, t11←g08, t12←g09, t14←g10, t15←g11b, t16←g12, t18←g16.
Multi-label kills: g14 [t01, t04, t11, t16, t17] (filter_out_dupes disabled), g15 [t07, t10, t13] (no-match return made certain), g17b [t18, t19] (HOME fallback to `~`).
Labels without a singleton: **t01, t10, t13, t17**. Reasoning: t01/t17 cannot be broken without either crashing the selftest (bare `*` insertion paths raise/crash → gate counts a crash as SURVIVED) or duplicating a type via the second lookup pass, which the dedupe kill g14 already covers; t10/t13 share the single `if not types: return … uncertain=1` return with t07, and no production branch distinguishes "no candidate at all" from "literal folded away" there.

## Label coverage — mado-portals (28/28)

Singletons: 5←p05, 7←p07, 8←p08b, 9←p09, 11←p11, 12←p12, 13←p13c, 14←p14b, 15←p15, 16←p16, 17←p17c, 18←p18, 19←p19, 20←p20, 21←p21, 22←p22, 23←p23, 24←p24b, 25←p25, 26←p26b, 27←p27b, 28←p28.
Multi-label kills: p01 [1, 8], p02 [1, 2, 6, 7, 12, 21, 23, 25, 26, 27] (default-branch reason string flipped — the only measured mutation that reaches label 2), p03 [3, 4], p06b [6, 7], p10 [8, 10, 14, 15, 20, 24] (GTK DBus comparison flipped).
Labels without a singleton: **1, 2, 3, 4, 6, 10**. Reasoning: 1 and 8 exercise the identical `_by_list` walk (unsupported-then-next); 2's distinguishing feature (first list item wins) is inseparable from the shared walk and reason string; 3/4 share the interface-key branch; 6's expected pick (`hyprland` for Screenshot) is also the name-order pick among supporters, so only a star-branch mutation reaches it, and any such mutation also moves label 7; 10's gtk-last-resort path is shared with 8/14/15/20/24, whose conf-voiding runs fall through to the same `_gtk` scan.

## Dead steps (replaced before freezing; none remain open)

- g05, g11, g17 (round 1, mimeglob): g05 survived (`d == lower` never matches `Makefile` because the stored glob keeps its capital); g11 and g17 produced non-zero rc with no FAIL lines (IndexError in `xdg_utf8_to_ucs4`; TypeError on `None + str`) — the gate counts a crash as SURVIVED. Replaced by g05b/g11b/g17b, all measured held.
- p06, p08, p13, p17, p24, p26, p27 (round 1, portals): p06/p08/p24/p26 survived for modelled-input reasons (label 6's `SS` is Screenshot, whose supporters `hyprland` also wins by name order; the trailing ` gtk` piece is appended by the trailing-empty branch, not the `;` branch; the `\x0b` line contains `=` so the junk-line raise never fires; the NUL in label 26 sits after `]`, outside the `rindex` slice); p17/p27 had wrong-indentation finds (count 0); round-1 p13 matched an unrelated 20-space `out.append(i)` — the real `_all_by_list` append is at 16 spaces (confirmed by a mutated-source dump + direct `resolve(Settings)` probe). All replaced by the measured pNNb/p13c/p17c variants in the frozen file.

## Reproducing evidence (commands + exit codes)

- Round-1 mutant sweep: `python3 -I $S/driver.py` → rc 0 (17+26 mutants, baselines included); results in `$S/results.json` (scratch, since deleted).
- Round-2 sweep: `python3 -I $S/driver2.py` → rc 0 (3+9 mutants + p13 probe); `$S/results2.json`.
- Round-3 sweep: `python3 -I $S/driver3.py` → rc 0 (p13c, p17c); `$S/results3.json`.
- JSON validity of both frozen kill-sets: `python3 -c json.load(...)` → `JSON_OK`.
- Gate runs quoted above → rc 0 / rc 0.

## Hygiene

- Scratch `$HYAKU_SCRATCH/mado-r95/R95MExecKillsC2` (default root `/fast/scratch/hyaku`) holds all mutants, drivers, and gate scratch; deleted after this report was written. Nothing cited lives only in scratch: the kill-sets are the frozen build files, and the gate outputs are quoted here.
- Nothing written outside the two build files, this report, and scratch. No host mime databases touched; no git/jj mutations; no peers messaged; no subagents.
