# RevC2Matrix — PRED-C2-r34-v1 calibration counter re-run (round 34)

Re-ran the frozen counter `.ufo/waves/round-34/c2/count.py` (unedited) against five
scorecard inputs on 2026-10-24. Command shape per row:

```
python3 -I .ufo/waves/round-34/c2/count.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --scorecard <CARD> --frozen .ufo/waves/round-34/c2/frozen.json
```

Preconditions verified at run time:
- `frozen.json` predicate matched the script's embedded `PREDICATE` (no `predicate-drift` exit-2 on any run).
- Pinned fetch `.ufo/waves/round-32/fetch/S189.bin`: regular file, nlink=1, sha256 `eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d` (matches pin). Every run reported `measured=169`.

## Results — every stdout line + exit code

| # | Card | stdout (verbatim) | exit |
|---|------|-------------------|------|
| 1 | `SCORECARD.md` | `PRED-C2-r34-v1 published=169 measured=169 mismatch=0 verdict=TARGET_MET` | 0 |
| 2 | `.ufo/waves/round-34/controls/c2-junk-card.md` | `PRED-C2-r34-v1 published=128 measured=169 mismatch=1 verdict=TARGET_MISSED` | 1 |
| 3 | `.ufo/waves/round-34/controls/c2-reachable-card.md` | `PRED-C2-r34-v1 published=169 measured=169 mismatch=0 verdict=TARGET_MET` | 0 |
| 4 | `.ufo/waves/round-34/controls/c2-junk.txt` | `PRED-C2-r34-v1 published=absent measured=169 mismatch=1 verdict=TARGET_MISSED` | 1 |
| 5 | `.ufo/waves/round-34/scratch/RevC2Matrix/absent-card.md` | `PRED-C2-r34-v1 published=absent measured=169 mismatch=1 verdict=TARGET_MISSED` | 1 |

No run produced stderr output; no run exited 2.

## Row notes

- **Row 1 — lane SCORECARD.md.** Last `r34-s189-line:` marker is line 2108:
  `r34-s189-line: line=169`. Published claim equals measured line 169 → `TARGET_MET`, exit 0.
- **Row 2 — c2-junk-card.md.** Card body is `r34-s189-line: line=128` → `published=128`,
  mismatch → `TARGET_MISSED`, exit 1. Reproduces the recorded transcript in
  `controls/c2-junk.txt` (`exit=1`, same output line modulo measured).
- **Row 3 — c2-reachable-card.md.** 198,289-byte card; single marker `r34-s189-line: line=169`
  → `TARGET_MET`, exit 0. Reproduces `controls/c2-reachable.txt` (`exit=0`, same line).
- **Row 4 — c2-junk.txt.** Not a card: it is a transcript (`exit=1` + a prior counter line)
  and carries no `r34-s189-line:` marker. Run anyway for completeness — the counter accepts
  any regular file as `--scorecard` and classifies it `published=absent` → exit 1.
- **Row 5 — absent-card.md.** Written for this run at
  `.ufo/waves/round-34/scratch/RevC2Matrix/absent-card.md`; contains no `r34-s189-line`
  marker at all → `published=absent`, mismatch, exit 1.

## Calibration read

Four distinct verdict paths exercised in one sweep: matching publication (169/169 → 0),
contradicting publication (128 vs measured 169 → 1), absent marker on a real card
(→ 1), and absent marker on a non-card regular file (→ 1). `measured=169` was invariant
across all five runs — the pinned fetch, not the card, drives the measured side.
Counter unmodified; frozen predicate unchanged.
