# R55W2RevC3Index — report (C3 landing surface, leaf seat, no subagents)

Full write-up: `.ufo/waves/round-55/w2/R55W2RevC3Index/c3-surface.md`. Receipts: `.ufo/waves/round-55/w2/R55W2RevC3Index/receipts/`.

## What I attacked
C3 landing surface only: the errata index row, the Round-55 Frontier bullet, residual P19 wording across the corpus, the index-completeness gate, and the frozen C3 counter's README leg as a landing check. I did not audit P23's proposition-to-quote entailment (the bullet itself lists that as open).

## Commands that ran (all `python3 -I`, read-only against the lane)
- `git -C <lane> rev-parse HEAD` → `721ba9c…`; `merge-base --is-ancestor 57584ed HEAD` → ancestor; `git diff --stat 57584ed HEAD -- corpus SKILL.md PROVINCE.md quality` → empty.
- `git show 57584ed:corpus/README.md | grep -n 'errata-r53\|P19\|P23'` → lines 81, 118.
- `grep -rn 'only when' corpus SKILL.md PROVINCE.md` → 79 + 3 + 0 hits (`receipts/only-when-hits.txt`).
- `grep -rn 'm_passPressed == 1' corpus SKILL.md PROVINCE.md` → 13 hits (`receipts/passpressed-hits.txt`).
- `python3 -I quality/check-index.py --rev 57584ed… --repo <lane>` → `indexed=70/70 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, exit 0.
- `python3 -I quality/check-index.py --selftest` (TMPDIR in scratch) → `12/12 assertions passed`.
- `sha256sum .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp` → `a83abeb5…` (same as round-51 fetch); `sed -n 1552,1578p` of that pin → confirms `} else {` at 1566, PRESSED at 1568, RELEASED at 1569.
- `python3 -I quality/counters/c3-r55-p19.py --repo . --rev 57584ed… --work <scratch>` → `readme=ok verdict=TARGET_MET`, exit 0.
- Scratch-only mutants (below) and their checks.

## Mutation statement
All mutants live in scratch under `/fast/scratch/hyaku/mado-r55/R55W2RevC3Index/`: two `git archive` copies of the rev (`root_b`, `root_c`) and a scratch `git clone --no-hardlinks` of the lane (branch on top of 57584ed, README-only commits). The lane was never edited; nothing was restored in the lane because nothing in it was changed. Lane `git diff --name-only` is empty.

## Verdicts
| Target | Verdict | Evidence |
|---|---|---|
| T1 errata index row holds errata file, P23, "supersedes P19" | **SURVIVES** | `corpus/README.md:81` at rev |
| T2 Frontier bullet about the correction | **SURVIVES** (its pin line numbers 1554–1571 and the sha match the pin; the bullet's own open sentence-to-pin audit is not done here) | `corpus/README.md:118`; `c3-surface.md` T2 |
| T3a errata table row P19 (`...errata-r53.md:17`) is still a live row with "direct" support and no superseded marker; withdrawal is prose only (:26–:30) | **BROKEN (minor)** | `c3-surface.md` T3 table |
| T3b other corpus presentations of P19's sentence as current | **NOT-REPRODUCED** — `dispatcher-dispatch-r51.md:185-187` (zero-arg `pass` overload, "sends both edges in one call" is imprecise wording, not the P19 claim); lessons are dated records; SKILL.md and PROVINCE.md have no P19 text | `receipts/passpressed-hits.txt`, `receipts/only-when-hits.txt` |
| T4 `check-index --rev 57584ed` still reports complete | **SURVIVES** as a completeness claim (70/70, exit 0; re-counted 70 blobs and 70 rows). **BROKEN as landing evidence**: mutant A (supersession words removed from row 81) still exits 0; control with row 81 deleted exits 1 | `receipts/check-index.txt` |
| T5 frozen C3 counter README leg vs. seat requirement "say it supersedes P19" | **BROKEN as a landing guard**: mutant A (`2e19ebec`) and mutant C (`254f4bdb`, row says "P19 remains the current proposition") both print `readme=ok verdict=TARGET_MET`. The frozen `registration.md:123` leg is exactly "README line naming the errata with P23", so the predicate is as written; the gap is between it and the seat requirement | `receipts/c3-counter-mutants.txt`; `registration.md:123`; `quality/counters/c3-r55-p19.py:234-241` |

## Not verified / not run
- P23 sentence-to-quote entailment (open per the bullet itself).
- `c3-r55-p19.py` self-tests and other C3 legs (`prefix`, `pin`, `p23`); only the rev and two readme mutants were run.
- check-index at HEAD `721ba9c` (not run; the diff over the checked paths is empty, so the result should carry).
- Did not run any hyprctl command, did not touch `~/.local/bin`, no installs (no tool authorised or needed), no pacman.

## Tools installed
None. Commands were `git`, `python3 -I` on the repo's own scripts, `sed`, `sha256sum`, `grep`.

## Cleanup
Receipts copied into the deliverable directory first; scratch under `/fast/scratch/hyaku/mado-r55/R55W2RevC3Index/` removed before yield.
