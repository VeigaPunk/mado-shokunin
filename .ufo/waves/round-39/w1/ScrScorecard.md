# ScrScorecard — round-39 scorecard draft report (w1)

Seat: `ScrScorecard` (leaf scribe). Scope: draft the round-39 SCORECARD.md
update. Wrote ONLY `.ufo/waves/round-39/w1/ScrScorecard/scorecard.md` (the draft)
and this report. No other files written; no tool installs (stdlib + read-only git
only); no pacman/uv/npx; no mutating git/jj; no subagents.

## Measured facts used (commands, outputs, exit codes)

- Freeze commit == tip at write time: `457d1b125932c1e0d797061a2156b917bcd7edaa`
  (`git rev-parse HEAD`; `git log --oneline -1`). Base: `08be4eb7fd13358ed29b096e8924005d46ac409c`.
- C1 before: `receipts/c1-redbefore.txt` → `MADO_R38_DISCRIMINATION: controls=19
  correct=18/19 verdict=TARGET_MISSED`; sole failure `c1-duprow` (ok=0).
- C1 after @ freeze and @ tip: `w1/ExecC1After/after-freeze.txt` /
  `after-tip.txt` → `controls=19 correct=19/19 verdict=TARGET_MET`, exit 0 (both
  files 1672 B, identical; all 19 controls ok=1). Manifest byte-copy: sha256
  `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8`, `cmp` exit 0;
  freeze rev `git show` streams identical (ExecC1After.md).
- C2/C3 before verified at freeze commit: `git ls-tree -r --name-only HEAD` has no
  `mado-options` / `r39-options` / `config-option-table-r39` path (grep exit 1);
  `git show HEAD:corpus/SOURCES.md | grep -cE '^\| S21[89] '` → 0; S219 own-work
  receipt unverifiable (ExecAssimFetches.md: `ls tools/mado-options.py` exit 2,
  `git log --all -- tools/mado-options.py` empty).
- Harm watch @ freeze: `w1/ExecGateHealth/gate1-check-index.out` → `indexed=55/55
  missing=0 dangling=0 duplicates=0`; `gate2-discrimination.out` → `MADO_R38_DISCRIMINATION:
  controls=19 correct=19/19`; `w1/ExecEventqSnapshot/eventq-after.txt` → `PRED-C2-r38-v3
  fixtures=14/14 readonly=1 live=1 tool=present verdict=TARGET_MET`; census before/after
  both `EXIT_CODE=0` with identical W-warning sets (`receipts/census-before.txt`,
  `w1/ExecCensusAfter/census-after.txt`); `receipts/selftest-base.txt` → `460/460`;
  `receipts/nav-base.txt` → 55/55 @ base.
- Axis re-derivation @ freeze (ran read-only): `python3 -I quality/check-axis-scores.py
  --repo . --rev master` → `MADO_AXIS: checked=3 mismatched=0 rev=457d1b125932c1e0d797061a2156b917bcd7edaa`,
  exit 0 (navigation 55/55, calibration 50/50, operability 12/12, all MATCH); byte-identical
  to `receipts/axis-base.txt` @ `08be4eb…`.
- Refusal-count correction grounded in `corpus/lessons/round-38.md` ## Mistakes ("three
  refusals explicitly (r28, r29 journal, r29 socket-client) - earlier LOG wording said
  'two' and is corrected") and LOG round-38 entry ("three refusals stand"); the scorecard
  round-38 paragraph at `SCORECARD.md:2420` still reads "2 refused" → corrected to 3 in
  this draft's records-update note.

## Deliverable

`.ufo/waves/round-39/w1/ScrScorecard/scorecard.md` (6771 B): three claim rows
(C1/C2/C3 with before→after, counting commands, measured commits), capabilities row
(config-option ownership resolver, first-working round 39), saturation 9.0/N=3
unchanged, retired none, "2 refused"→3 refused records-update note + published-axis
staleness gate unchanged, sources/harm-watch/frontier paragraph, `Planned (round 40)`
intent block.

## Limits

C2/C3 after-measurements cannot exist yet: the round-39 data commit has not landed
(HEAD == freeze commit; tool, counters, entry, S218/S219 rows all absent). The draft
marks those cells pending and records the targets verbatim from the frozen
registration — no numbers invented.

## Final answer (≤6 lines)

1. Scorecard draft written to `.ufo/waves/round-39/w1/ScrScorecard/scorecard.md` (only file besides this report).
2. C1 measured: before 18/19 (red-before receipt) → after 19/19 TARGET_MET @ freeze & tip `457d1b12`, exit 0, manifest sha 96965518….
3. C2/C3 before-state verified absent at freeze (ls exit 2; S218/S219 count 0); after-cells pending data commit — targets recorded, no numbers invented.
4. Harm watch @ freeze: nav 55/55, discrimination 19/19, eventq fixtures=14/14 tool=present, axis checked=3 mismatched=0, census before/after exit 0.
5. Records update: round-38 "2 refused" → 3 refused correction included; staleness gate unchanged.
6. No installs; read-only git/python only; no writes beyond the two seat files.
