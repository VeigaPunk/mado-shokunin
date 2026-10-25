# ScribeQuality draft — round 35 (append-only, never into the lane)

Proposed append to `corpus/QUALITY.md`. Existing criteria are numbered 1–54
(at `dff3941`); these continue at 55 and 56. Neither rewrites an existing
criterion. Each names the criterion it extends and cites the mistake that
produced it. The round-34 lesson records mistakes by `class:` (instrument,
ledger, id-space, hygiene), not by M-id, so the citations name the class.

## Round 35 — indirection cribs and per-clause accounting (round-34 mistakes; outside lessons/round-34-verifier-spotcheck.md routed defects 1–3)

55. A claim whose counter reads tree shape names the indirection cribs its
    control set must miss, in addition to the skip-the-work shapes criterion
    36 already requires: a symlink at the claimed path, a symlinked parent
    component, a hardlinked claimed file, and any further path the tree
    permits for reaching the claimed bytes without holding them at the
    claimed path (a fetch-tree crib, a merged-tree overlay); each crib's
    receipt is committed beside a regular-file control that meets the same
    spec (lesson: lessons/round-34.md#mistakes instrument — the round-33
    counter printing `TARGET_MET` on the symlink crib; outside
    lessons/round-33-verifier-spotcheck.md C1Junk).
    Round-35 application: `controls/c1-entry-symlink.txt` reads
    `verdict=TARGET_MISSED`, `controls/golden.txt` reads `TARGET_MET`; the
    round-34 set (`controls/symlink-crib`, `symlink-entry`,
    `extra/symlink-parent`, `extra/symlink-sources`, plus the
    `c1-hardlink` receipt) is the precedent. Extends criterion 36; 36's
    shapes skip the claimed work, this adds shapes that fake its result.
    Limit: the clause names the indirection modes the lane knows; a mode
    the tree admits that no control exercises stays a `captured-by: none`
    hole and must be recorded as one.
56. Every live clause of a frozen counter is named in a committed clause
    ledger and counts only as controlled or declared: controlled means the
    clause names a control whose committed receipt records a TARGET_MISSED
    verdict for which the clause is the load-bearing check; declared means
    the clause carries an explicit `not-load-bearing` line with a reason
    (TOCTOU-only, dead under its own spec). A clause that cannot fail under
    the counter's own frozen spec is dead code and is recorded retired or
    declared, never silently counted as load-bearing (lesson:
    lessons/round-34.md#mistakes instrument — the clause-drop mutation
    suite showing the 1–25 word bound dead under `found == quote` and the
    `S_ISLNK`/`O_NOFOLLOW` pair TOCTOU-only; outside
    lessons/round-34-verifier-spotcheck.md routed defects 1–2).
    Round-35 application: `c1/clauses.json` names nine controlled live
    clauses, one declared clause (`o-nofollow-open`, reason TOCTOU-only)
    and one retired clause (`r34-word-bound-1-25`, dead code);
    `controls/c2-donothing.txt` reads `uncovered=1 TARGET_MISSED`.
    Extends criterion 25; 25 credits a tightening shown to bite on a
    mutant, this requires per-clause accounting of every clause in a
    counter before its first data, not only tightened ones. Limit: a
    `not-load-bearing` reason is a declared status, not evidence; a clause
    declared TOCTOU-only can still be wrong code, and the ledger's reason
    is reviewable text, not a run.
