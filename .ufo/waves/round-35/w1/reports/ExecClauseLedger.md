# ExecClauseLedger — clause ledger verification (round-35, c1)

## Scope

Verify `.ufo/waves/round-35/c1/clauses.json` (`CLAUSES-r35-v1`) against committed control
receipts:

1. Every live clause with a `control.receipt` → receipt file exists, is non-empty, contains
   `verdict=TARGET_MISSED`, and is committed to the repo (jj-colocated; checked via
   `git ls-files --error-unmatch`).
2. Every live clause has either a `control` or a `not-load-bearing` reason.
3. Exactly one clause carries a `not-load-bearing` declaration, and it is `o-nofollow-open`.

## Verdict: PASS — all 10 live clauses covered; zero uncovered.

## Method (machine check, re-run at write time)

Python 3 stdlib script parsed the ledger, then per live clause: stat receipt → read bytes →
substring scan for `verdict=TARGET_MISSED` → `git ls-files --error-unmatch <receipt>` for
committed status. Counted clauses with `control` vs `not-load-bearing`; enforced XOR and the
exactly-one rule.

Full machine output: `.ufo/waves/round-35/scratch/ExecClauseLedger/summary.txt`

## Findings

- 10 live clauses: 9 with `control`, 1 with `not-load-bearing` (`o-nofollow-open`, 384-char
  reason naming the r35 split: S_ISLNK component walk is load-bearing via
  `controls/c1-entry-symlink`; the O_NOFOLLOW open-time flag is TOCTOU-only defence in depth).
- All 9 receipts exist, are non-empty (308–326 bytes), contain `verdict=TARGET_MISSED`, and
  are git-tracked.
- Sample receipt `controls/c1-digest.txt` shows command transcript ending
  `PRED-C1-r35-v1 closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED` +
  `exit=1`; last commit touching it: `19e4ab3171c1540c40d6b12097745af98053b07d` (ancestor of
  HEAD).
- No clause carries both `control` and `not-load-bearing`; no clause carries neither.
- `retired[]` holds one entry (`r34-word-bound-1-25`) — retired clauses are out of scope for
  the coverage check per the ledger note.

## Uncovered clauses

None.
