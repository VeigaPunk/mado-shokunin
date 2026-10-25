# ConnR34 — round-34 routed defects × round-35 repairs

Connector seat. Sources: `corpus/lessons/round-34-verifier-spotcheck.md` §"Routed
defects" (L299–324) against `.ufo/waves/round-35/registration.md` and the frozen
r35 artifacts it names. Wave w1 was in flight at read time (`w1/exit-codes.tsv`
empty); verdicts are on what is frozen/committed so far.

## Defect 1 — dead `1–25` word-bound clause in `PRED-C1-r34-v1` → **REPAIRED**

Repaired by retirement plus a live replacement, exactly the defect's own "retired
or given a failing case" fork.

- `registration.md:104–110` — declares the repair.
- `c1/clauses.json` — `retired` holds `r34-word-bound-1-25` with the reason; the
  live list holds `gate-quote-word-bound` bound to control `c1-quote-long`; the
  entry's quote is now a free variable (`c1/count.py:17`).
- `controls/c1-quote-long.txt` — committed receipt prints `TARGET_MISSED`,
  exit 1: the replacement clause has a failing case.

## Defect 2 — `S_ISLNK`/`O_NOFOLLOW` pair was TOCTOU-only → **REPAIRED**

Repaired by split: the component walk stays load-bearing with a failing control;
the open-time flag is declared non-load-bearing with a reason — which is also
the defect's alternative fork, "justified as TOCTOU protection in the counter's
own header."

- `registration.md:111–116` — declares the split.
- `c1/clauses.json` — `o-nofollow-open` carries `not-load-bearing` + reason;
  `entry-regular` (the S_ISLNK walk) names control `c1-entry-symlink`, whose
  receipt prints `TARGET_MISSED`, exit 1.
- `c1/count.py:18–20,59–60` — the counter's own docstrings name the pair
  "TOCTOU-only defence in depth … NOT a load-bearing clause."
- `c2/count.py:16–18,99–100` + `c2/frozen.json` — `toctou_declared=1` is enforced
  by the frozen C2 predicate, so the declaration cannot silently revert.

## Defect 3 — `RevFrozenBlobs.md` labelled `fa7ba113` as lane tip → **REPAIRED**

Repaired by re-issue, not rewrite — matching the defect's "should be re-issued
with the real tip."

- `registration.md:117–120` — declares the re-issue.
- `ledger/RevFrozenBlobs-r35.md` exists; names the real r34 tip
  `dff394109f3cc3d851309ad7c67dd3b35b46adf2` (L5, L13, L19), re-measures the
  same seven paths, and explicitly leaves the r34 artifact in place (L56–57).
- `c2/count.py:19–21` — `ledger_tip_ok` re-verifies every listed blob id at that
  revision, so the re-issue is itself checked by the frozen predicate.

## Defect 4 — merge-package id remap is stale (campaign-side) → **PARTIALLY REPAIRED**

- Campaign half handled: `registration.md:121–122` files it under L0 `ae2c52b8`
  and does not duplicate the question — correct disposition.
- Lane half declared but not yet landed: `registration.md:123–126` says the
  lane's id handling (registry rows S203–S210 vs the package's S309…S336) is
  "recorded in the round lesson." `corpus/lessons/round-35.md` does not exist
  yet (glob of `corpus/lessons/` shows no round-35 file); the wave is still
  running, so this is pending, not refused.

## Defect 5 — three L0 questions remain open → **NOT REPAIRED** (operator-owned by design)

The r34 closure routed all three to the operator and required they not be
answered, corrected or duplicated by the lane. Registration acknowledges only
the id-remap question (`registration.md:121–122`); the other two — the r33
routed defect 2 on the S189 line number, and the inherited working-tree debt —
are unmentioned. Leaving them untouched is conformant; the only gap is that the
registration does not name them as still-routed.

## Missed defects

None of the five routed defects is wholly ignored. Two flags:

1. **Coverage regression adjacent to the defect-2 repair (new observation, not
   routed).** The r34 counter's `st_nlink != 1` check had a committed hardlink
   control that the closure re-proved load-bearing both ways. In r35 the check
   survives (`c1/count.py:87`) but no `c1-hardlink` control exists in the
   kill-rule table (`registration.md:49–61`), and `clauses.json`'s
   `entry-regular` clause does not mention `nlink`. The clause still counts as
   covered because the symlink control kills the clause as a whole — but the
   hardlink sub-condition lost its failing case.
2. **Cosmetic.** The registration heading "The two routed r34 defects this
   round repairs" (`registration.md:102`) undercounts — it repairs three (1–3)
   and dispositions a fourth.
