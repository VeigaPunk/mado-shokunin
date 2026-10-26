# w1/ScrMistakes — mistakes for `corpus/lessons/round-45.md` `## Mistakes`

Status: **done**. Deliverable: `.ufo/waves/round-45/w1/ScrMistakes/mistakes.md` (paste-ready rows + criteria text).
Nothing in the lane was edited; no commit was made in the lane (write scope: this seat dir only).

## Behaviour

Seven rows, one per routed defect, in CORPUS.md's form (class · evidence · captured-by · fix, fix fail-ability stated):

| row | routed | class | criterion proposed |
|---|---|---|---|
| M45-1 | D1 session material | `scope` | 87 (session material stays shape-only in committed bytes) |
| M45-2 | D2 SCORECARD after-values | `landing` | 88 (a claim row carries its own after value and verdict) |
| M45-3 | D3 tip receipts | `attribution` | 86 (a `*tip*` receipt carries the closing tip) |
| M45-4 | D4 nonce before-share | `number-drift` | 89 (a before/after number is a count only if it reproduces) |
| M45-5 | D5 open predicate defects | `vacuous` + `survivor` | 85 (declared residual is a kill rule), aligned with `ConnLessonsPattern` |
| M45-6 | D6 S290-S297 supersession | `stale-premise` | application of 28 |
| M45-7 | D7 ConnCalibration mismatches | `reference-drift` (+ count half) | application/extension of 83 |

Numbers 85-87 match `w1/ConnLessonsPattern/patterns.md:75-98`; that seat confirmed by message that 88/89 are unclaimed, so
the allocation is agreed, not assumed. Each criterion cites its lesson row.

## Measurements (all on committed bytes; receipts in this seat's `receipts/`)

| check | command | red | green / mutant |
|---|---|---|---|
| 87 | `checks.py 87 --repo . --rev 0c89478a` | `violations=77`, 26 files | control `CLEAN`; +1 title key → `violations=1` |
| 86 | `checks.py 86 --repo . --rev 8ac15c41 --round .ufo/waves/round-44` | `violations=3` (the three `*-tip` receipts name `74c606a`) | control with equivalence line `CLEAN`; mutant `violations=1` |
| 88 | `checks.py 88 --repo . --rev 0c89478a` | `violations=4` (`SCORECARD.md:2480,2481,2570,2571`) | control `CLEAN`; pointer mutant `violations=1` |
| 89 | `checks.py 89 --repo . --rev <freeze> --registration …` | `violations=1` (round-44 v1 counter, `--nonce default=None`) | round-45 registration at `22a8dedd` `CLEAN`; mutant `violations=1` |

Receipts: `receipts/red-before-base.txt` (four reds), `receipts/controls.txt` (control CLEAN then four single-defect
mutants FAIL), `receipts/green-round45-freeze.txt` (89 CLEAN at the freeze). Checkers are revision-addressed and read-only.

## Findings that enlarge the routed items

- **D1 is not two files.** At `0c89478a` the sweep finds 26 tracked JSON files with identity fields: the two the closure
  named, 18 `.ufo/waves/round-43/w1/ExecOracleGkeep/receipts/*.json` (3-5 titles each of that seat's own test windows, not
  the host's), and round 44's own `w1/ScrLessonSkeleton/c1-demo/client1.json`/`client2.json`. 22 of the ExecOracleGkeep
  files carry a non-empty 61-62-char `instance_sig`. No title, serial or signature value appears in this seat's files.
- **D2 is older than round 44.** `SCORECARD.md:2480-2481` (Round 43) also publish "see report" instead of an after value.
- **D7's path half is vacuous under criterion 83.** `check83.py` passes the round-44 lesson at base
  (`verdict=PASS citations=13 violations=0`) although it cites `assimilation/renumber-map.tsv`, which no ref holds, because
  `.tsv` is absent from the checker's `EXT` tuple (`check83.py:25`). Criterion 83 must be widened before it can be cited here.
- **D4's fix is already satisfied** for round 45: `c1-r45-monitors.py` defaults `--seed` to 45; the empirical red is the
  same tool bytes (`e3c2e471…`) printing `11/26` and `15/26` under two nonces with an identical clause vector.

## Gates and limits

- Both claims' counters were **not** run by this seat; no tool selftest was run; no host command was run (no `hyprctl`, no
  `pacman`, no service action, no Wayland client). No tool installed.
- Fixes for D1/D2/D3/D6/D7 are not landed at this read (`ExecProjectTitles`, `ExecPrivacyGate`, `ExecSupersede`,
  `ScrErrata` in flight, read only as status lines). No green is claimed for them; only the checkers' red states are measured.
- Criterion 85's wording is narrowed against `ConnLessonsPattern`'s (a residual unexposable by construction must say why);
  the divergence is recorded in the draft for the L1 to resolve.
- The M45-6 census evidence is a report table, not a committed receipt; the landing owes a `sources-census.sh` run.

## Out of scope / not mined

M44-1's reason-coverage class, M44-5's seat-count recompute beyond the LOG half, any live host claim, and the round-45
claims themselves (other seats). Scratch `/fast/scratch/hyaku/mado-r45/ScrMistakes/` removed by the drivers' `trap`.

## Files

- `.ufo/waves/round-45/w1/ScrMistakes/mistakes.md` — the draft rows and criteria.
- `.ufo/waves/round-45/w1/ScrMistakes/checks.py`, `mutants.sh` — proposal checkers 86-89 and their control driver.
- `.ufo/waves/round-45/w1/ScrMistakes/receipts/` — red-before, controls, and the D1-D7 command receipts.
