# ConnCalibration — round 43 w2 report (calibration)

Seat: `ConnCalibration` (connector, leaf). Lane tip at run time:
`2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa` (jj-lane.sh state: local=remote=2a3707c…,
ahead=0 behind=0, head=detached, untracked=19 = w2 seat files). Data commit
`1959770657f1f8665097c1aed4be6c1cbb07139f` (parent 496340dd, the C2 v2 freeze), base
`a35cfdf…`.

## Scope

Attacks the calibration axis (AXES.md: `SHONEN.md`/`SCORECARD.md` entries match observed repo
state). Listed every round-43 statement in `SCORECARD.md`, `LOG.md` and `SHONEN.md` and checked
each against repo bytes at the tip (read-only git; lane tools). Ran the calibration gate
`python3 -I quality/check-axis-scores.py --rev 2a3707c83d55eb1333e1bf6ff1c5c38001c11eaa --repo .`
and re-ran both round counters at the tip.

## Result: 0 mismatches

- **25 round-43 statements checked** (SCORECARD.md:2531,2535,2536,2544,2548,2550; LOG.md:
  2487-2494; SHONEN.md contributes none — `grep -nE '43|40|41|42' SHONEN.md` has no hits).
- **Mismatches: 0**. Every statement matched repo bytes at the tip:
  - C1/C2 counts and verdicts at base and data commit match the committed receipts
    (c1-before-base.txt, c1-after-data.txt, c2-v2-before-base.txt, c2-after-data.txt,
    c2-v1-after-data.txt); tool byte-identical to the round-42 reference (`cmp` IDENTICAL,
    sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`).
  - Controls: `CTL_C1 controls=46`, `0 of 47` non-reference MET, reference met 1; `CTL_C2
    controls=74 correct=74/74` (v2 receipt same tally).
  - Source registry 226→234 rows; S290-S297 all tier A/mined/opened 2026-10-26; S155/S158
    used-by extended by one item each; knowledge entries 59→60; QUALITY 77-81 present;
    lesson round-43.md has Gate (10 GATE rows), ADMIT + 4 REFUSE, M43-1..8;
    `quality/check-locators.py` present.
  - w1 spec committed at `5add5b45…`, items=38, roles 14/7/4/3/3/3/2/1/1.
  - v2 forgery harness: admits A1/A2/D1/E2/H1/X1, rejects B1/B2/C1/C2/E1/F1/F2/G1/G2/X2/X3
    (forge-v2.log, more-v2.log).
  - Oracle observation reproduced in `w1/ExecOracleGkeep/20-observation.txt` (`"size": [420,
    500]`, floating true; floatonly → 200x200; size300 → 300x300; nofloat → tiled).
  - Locator correction verified by grep on the fetch pins (HyprCtl.cpp size at 427/428/448;
    RegexMatchEngine.cpp `negative:` at 7, FullMatch at 16); round-43 pins byte-identical to
    round-42 (7 Hyprland files + host-gkeep.conf, via fetch-sha256.txt sets).
- **Calibration gate**: `MADO_AXIS: checked=3 mismatched=0 rev=2a3707c…`, exit 0 (navigation
  60/60, calibration 68/68, operability 12/12 — all MATCH).
- **Tip re-runs**: C1 `fixtures=37/37 … verdict=TARGET_MET` exit 0; C2 v2 `admitted=1/1 …
  verdict=TARGET_MET` exit 0 at the tip (registration target includes "and at the tip").

## Observations (not counted — lesson-internal pointers, outside the three assessed files)

- `corpus/lessons/round-43.md:93` cites `receipts/census-after.txt`; the committed receipt is
  `census-after-data.txt`.
- `corpus/lessons/round-43.md:205-208` cites `receipts/c1-after-tip.txt` / `c2-after-tip.txt`;
  no after-tip receipts are committed (tip verdicts re-measured here, hold).

## Evidence

Full statement-by-statement ledger with observed bytes: `w2/ConnCalibration/mismatches.md`.

## Tooling

No tools installed (system python3/git/cmp/sha256sum/grep/sed/diff). Counter re-runs used
scratch `$S=/fast/scratch/hyaku/mado-r43/ConnCalibration` as TMPDIR; scratch deleted on exit.
