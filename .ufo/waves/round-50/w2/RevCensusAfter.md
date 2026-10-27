# RevCensusAfter — seat report (w2 falsify, round 50 attempt 2)

Seat: RevCensusAfter · Target: census conformance — SOURCES.md registry rows before -> after,
and the validator's own verdict at the lane tip.
Verdict: **SUPPORTS the freeze** on both axes. No defect found. No E-level line; validator exit 0.

## Axis 1 — registry row count before -> after

Command (run in the lane, read-only):
`git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\| *S[0-9]{3,}'`

| rev | rows |
|---|---|
| 8ae47b957034ae21012bbf09173cca2c48be345e (base) | 288 |
| 906178b607f2071af7c2efec5aad976a8bfa5757 (data) | 300 |
| b4a79843cc2545bbe800db9322e58f6e00436629 (attack tip) | 300 |

Exactly **+12 (288 -> 300)** as the freeze declares. ID-set diff (`grep -oE 'S[0-9]{3,}' | sort`)
between base and tip is a pure append: `288a289,300` = S352..S363 and nothing else; no id
reused/renamed (would have tripped validator E02/E03 — none fired). Seat copies: `ids-base.txt`,
`ids-tip.txt`.

On-disk `corpus/SOURCES.md` sha256 = `b3a1a041d4a9ce0c2555f028ce415bac5a4b1a0e38bf782e730cbb24ddf52744`,
byte-equal to both the tip commit (`git show b4a79843:...`) and the frozen artifact table in
registration.md — the working tree does not diverge from the scored bytes (only
`corpus/lessons/round-50.md` is modified in the tree; it is not part of this target).

## Axis 2 — validator verdict at the lane tip

Command:
`TMPDIR=/fast/scratch/hyaku/mado-r50/RevCensusAfter bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`

- **exit=0**, final line `mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`.
- **E-level lines: 0** (grep -cE '\tE[0-9]' = 0). No overdue/missing lines.
- Warning totals: baseline 18 (17 W04 + 1 W01, receipts/census-before.txt) -> after 20 (19 W04 + 1 W01).
- **Delta vs census-before.txt is exactly +2 W04 lines, nothing removed, nothing changed**:
  - `mado W04 S353 duplicate url .../efb50993.../src/config/legacy/ConfigManager.cpp across scopes`
    — the S303/S317-family URL the seat spec names as a legitimate new cross-scope duplicate
    (same URL also held by S162/S303/S317).
  - `mado W04 S354 duplicate url .../efb50993.../src/managers/input/InputManager.cpp across scopes`
    — byte-identical URL to held row S316 (verified by exact URL extraction, lines 265 vs 303).
  Both shifts fall inside the spec's declared allowance ("new rows may legitimately add W04
  cross-scope duplicates of held URLs S303/S317-family"). The lone W01 (S277) is unchanged.
- **Reproducibility**: my re-run is byte-identical (diff exit 0) to the committed
  `.ufo/waves/round-50/receipts/census-after.txt`. Seat copy: `census-after-rerun.txt` (with
  `exit=0` appended to match the baseline receipt format).
- Instrument health: `sources-census.sh selftest` -> exit 0, `selftest ok`
  (seat copy `selftest.txt`) — the validator itself is sound.

## What this attacks / supports

- Supports registration.md data-commit claim "rows S352-S363 appended in ## Registry" (exactly
  12 rows, pure append, ids unique).
- Supports the census-before/after receipts committed at freeze: the after-state reproduces
  deterministically at the attack tip with only the two declared-allowable W04 shifts.
- No falsifying evidence found; nothing here kills C1/C2 — this target is orthogonal to the
  frozen counters and shows the registry/census layer consistent with the freeze.

## Hygiene

- No lane/fleet tracked file edited; only this report and seat-dir receipts written.
- Scratch `/fast/scratch/hyaku/mado-r50/RevCensusAfter` deleted after receipts were copied here.
- No host state touched; validator run with TMPDIR under scratch; no GUI/pacman/git mutation.

## Deliverables

- `.ufo/waves/round-50/w2/RevCensusAfter.md` (this report)
- `.ufo/waves/round-50/w2/RevCensusAfter/census-after-rerun.txt`
- `.ufo/waves/round-50/w2/RevCensusAfter/selftest.txt`
- `.ufo/waves/round-50/w2/RevCensusAfter/ids-base.txt` / `ids-tip.txt`
