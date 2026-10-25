# ScribeScorecard — round-35 scorecard rows drafted, not applied

Seat: ScribeScorecard (w1, round 35, mado). Read-only against the lane plus two
draft files; SCORECARD.md untouched (`git status` clean on it).

## Deliverable

`.ufo/waves/round-35/scratch/ScribeScorecard/draft.md` — apply-ready round-35
section text: one row per claim (before→after, counting command, measured
commit, author verdict), the proposed capabilities-table row with its caveat,
the Sources/saturation/planned block, and a harm-watch fill. `⟨…⟩` marks the
cells that can only be filled when the C1 data commit lands (commit hash,
post-data counter output, navigation 50/50).

## What was measured at write time (all re-run, not copied)

| Command | Result |
|---|---|
| `python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json` at `19e4ab3` | `closed_entries=0 closed_rows=0 open_cites=8 verdict=TARGET_MISSED` exit 1 — C1 data not landed |
| `python3 -I .ufo/waves/round-35/c2/count.py --repo . --frozen .ufo/waves/round-35/c2/frozen.json` at `19e4ab3` | `uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET` exit 0 |
| C2 counter against a scratch `git archive` extraction of r34 tip `dff3941` | `error=clause-ledger-missing` exit 2 — the drafted before-state |
| `git show 6d754bd:corpus/SOURCES.md \| grep -cE '^\| S[0-9]'` | 192 rows; 0 S203–S210; `corpus/knowledge/` 47 files, no `idle-lock-r1*` |
| `python3 -I quality/check-axis-scores.py --rev HEAD --repo .` | `checked=3 mismatched=0` exit 0 (47/47, 41/41, 12/12) |
| `git ls-tree HEAD .ufo/waves/round-35/fetch/` | 8 committed receipts S203–S210 |

## Findings that shape the rows

- **C1 is mid-flight.** The freeze commit `19e4ab3` holds both predicates,
  counters, clause ledger, all 11 committed control receipts, 8 fetch receipts
  and `ledger/RevFrozenBlobs-r35.md`. The three entries + eight rows exist only
  in `controls/golden/` and scratch mirrors (w1 ExecIndex, ExecRows confirm).
- **C2 is already green at the freeze commit.** Its evidence is the predicate
  machinery itself — same commit, same counter. Drafted before-state = exit-2
  `clause-ledger-missing` at the r34 tip (exit 2 = usage/drift surface, quoted
  verbatim in the row rather than invented as a target-miss line).
- **Capability row caveat carried.** w1 RevDoNothing (V1 truncation, V3
  receipt-aliasing) proves the clause ledger is unauthenticated worktree bytes:
  do-nothing TARGET_MET is reachable on a substituted ledger. The draft admits
  the row as a *shape audit* with the limit stated inline; integrator decides.
- **Kill rule evidence is stronger than registered.** Committed: 10 defect
  controls + golden, all reproduced byte-for-byte by w1 RevReceipts. In-round
  additions (w1 ExecSymlink): entry `nlink=2` and receipt-side `S_ISLNK` both
  MISSED — scratch-only, not part of the committed kill set.
- **Planned candidates gathered from landed reports:** RevDoNothing binding
  gap; ExecSymlink commit-or-drop; ExecRows' unenumerated `on-change`/
  `on-request` recheck tokens; ScoutReg's staged-append census (package's
  S197–S336 contiguous collides with lane-allocated S201/S202 — campaign-side,
  operator-owned; the round adopted S203–S210 by document, package ids
  S309/S310/S321/S329/S330/S331/S334/S336 recorded in the lesson).
- Wave shape for the section line: 64 seats — 13 executor, 12 scout,
  11 reviewer, 8 critic, 3 mutation-tester, 2 each simplifier/sentinel/
  revenger, 7 scribe, 4 connector.

## Constraints honored

Leaf member: zero subagent dispatch. No writes to SCORECARD.md, corpus/,
tools/, or any sibling; only the scratch draft and this report. No tool
installs needed (python3 + git suffice).
