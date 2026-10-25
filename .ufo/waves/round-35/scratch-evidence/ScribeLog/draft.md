## Round 35 — the dead clause retired, the TOCTOU pair split, and the idle-lock offer measured (2026-10-24, attempt 1)

Motivation: `corpus/lessons/round-34-verifier-spotcheck.md` passed round 34 and
routed four defects into this round: the `1-25` word bound in `PRED-C1-r34-v1`
was dead code under its own frozen spec, the `S_ISLNK`/`O_NOFOLLOW` pair was
presented as load-bearing while protecting only against a TOCTOU race no static
tree can kill, `RevFrozenBlobs.md` labelled `fa7ba113` the lane tip when the
round-34 tip is `dff3941`, and the merge package's id remap is stale on the
campaign side (already filed as L0 `ae2c52b8`, not duplicated here).

Work: two NEW predicates were frozen before any corpus append at
`19e4ab3171c1540c40d6b12097745af98053b07d`. `PRED-C1-r35-v1`
(`c1/frozen.json`, implemented in `c1/count.py`, its predicate sentence
identical in `count.py`, `frozen.json` and `registration.md`) scores the
idle-lock control surface: `TARGET_MET iff closed_entries=3 AND closed_rows=8
AND open_cites=0`, over three knowledge entries and eight registry rows
(S203–S210) whose anchor cells pin the sha256 of the in-round fetch receipts
`.ufo/waves/round-35/fetch/S203–S210.receipt.txt`. Its kill rule discharged
before data: `controls/golden.txt` prints `closed_entries=3 closed_rows=8
open_cites=0 verdict=TARGET_MET` exit 0, and all ten defect trees miss —
`c1-donothing` (`open_cites=8`), `c1-entry-symlink`, `c1-row-duplicate`,
`c1-row-extra-field`, `c1-usedby-extra`, `c1-status-queued`,
`c1-recheck-prose`, `c1-digest`, `c1-quote-absent` and `c1-quote-long` each
printing `closed_entries=2 closed_rows=7 open_cites=1 verdict=TARGET_MISSED`
exit 1 (receipts committed beside each tree under `controls/`). On the lane
root before the append the frozen counter prints `closed_entries=0
closed_rows=0 open_cites=8 verdict=TARGET_MISSED` exit 1 — the claim verdict
flips only when the data lands [<data commit hash here>].

`PRED-C2-r35-v1` (`c2/frozen.json`, implemented in `c2/count.py`) scores the
lane's own evidence ledger: `TARGET_MET iff uncovered=0 AND retired=1 AND
toctou_declared=1 AND ledger_tip_ok=1`. Its do-nothing control — a scratch
clause ledger stripped of its control and declaration — prints `uncovered=1
retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MISSED` exit 1
(`controls/c2-donothing.txt`). On the lane repo the frozen counter prints
`uncovered=0 retired=1 toctou_declared=1 ledger_tip_ok=1 verdict=TARGET_MET`
exit 0: every live clause in `c1/clauses.json` names a control whose committed
receipt records a miss, `r34-word-bound-1-25` is retired — the r35 counter
makes the entry's quote a free variable so the replacement
`gate-quote-word-bound` clause has a real failing case
(`controls/c1-quote-long.txt`) — and the `S_ISLNK`/`O_NOFOLLOW` pair is split:
the `S_ISLNK` component walk stays load-bearing (`c1-entry-symlink` kills it)
while `o-nofollow-open` carries an explicit `not-load-bearing` declaration
with its TOCTOU reason. The stale tip label is repaired by re-issue:
`ledger/RevFrozenBlobs-r35.md` measures the same seven frozen counter paths at
the real round-34 tip `dff394109f3cc3d851309ad7c67dd3b35b46adf2` and the C2
counter re-verifies every blob id there; the round-34 artifact is not
rewritten. One wave ran under `w1-taskcall.json` (spawn 64, one batched call,
policy band 64–128): [<settled counts at closure — dispatched/finished/
reports/dead>].

Honest notes: this entry is drafted while wave 1 is still in flight and before
the corpus append; the C1 post-data verdict line and the settled seat counts
are the only places publication fills in, everything else above is re-executed
output. C2's surface is the frozen ledger itself — the claim is `TARGET_MET`
at the freeze because the clause ledger, the retirement and the re-issued blob
table all landed inside `19e4ab3`; that is the design, not a skipped step.
`o-nofollow-open` is recorded as `not-load-bearing` with its reason rather
than silently counted — no static tree can kill an open-time flag, and the
ledger says so. The staged rows continue the lane's registry at S203–S210 and
re-point by document; the merge package's own ids for the same documents
(S309, S310, S321, S329, S330, S331, S334, S336) are recorded in the round
lesson for the campaign to reconcile, and the lane renumbers nothing. SHONEN
stays `[~]` on all four boxes; nothing was self-promoted.
