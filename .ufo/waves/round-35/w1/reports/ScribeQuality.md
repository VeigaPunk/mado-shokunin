# ScribeQuality — two criteria drafted (55 indirection cribs, 56 per-clause accounting), each extending an existing criterion

Scope: draft text only, at `.ufo/waves/round-35/scratch/ScribeQuality/draft.md`
(3412 B). No lane tracked file was written; no counter or gate was run by this
seat. Lane working copy read-only. Lane tip `dff394109f3cc3d851309ad7c67dd3b35b46adf2`
(per `corpus/lessons/round-34-verifier-spotcheck.md:6`).

## What the round's mistakes produce

The mistakes digested are `corpus/lessons/round-34.md#mistakes` (the round
behind this wave; criteria in round N cite the round-N−1 lesson). Round-34
records mistakes by `class:` (instrument ×2, ledger, id-space, hygiene), not
M-id, so draft citations name the class. The outside source is
`corpus/lessons/round-34-verifier-spotcheck.md` routed defects 1–3.

Two mistakes produce criteria; the other three are applications of existing
criteria or scope outside the bar, and produce none:

**Drafted (extends, never rewrites):**

- **55 — indirection cribs, extends criterion 36.** Produced by the round-34
  instrument mistake: the round-33 frozen counter printed `TARGET_MET` on a
  symlink crib because criterion 36's required shapes (do-nothing,
  all-false/empty, junk, server echo, label- or fixture-keyed, no-reader) all
  *skip* the claimed work — none *fakes* it by reaching the claimed bytes
  through indirection. The fix is the named crib list: symlink at the claimed
  path, symlinked parent, hardlinked claimed file, fetch-tree crib,
  overlay — with committed TARGET_MISSED receipts beside a regular-file
  TARGET_MET control. Precedent receipts: `controls/c1-entry-symlink.txt`
  (`verdict=TARGET_MISSED`, exit 1, read this seat),
  `controls/golden.txt` (`TARGET_MET`, exit 0). Limit recorded: the list
  names known modes; an unexercised admitted mode is a `captured-by: none`
  hole and must be recorded as one.

- **56 — per-clause accounting, extends criterion 25.** Produced by the
  round-34 instrument mistake on clause-drop mutants: the 1–25 word bound was
  dead under `found == quote` and the `S_ISLNK`/`O_NOFOLLOW` pair was
  TOCTOU-only, both presented as load-bearing. The fix is the clause ledger:
  every live clause is either controlled (names a control with a committed
  TARGET_MISSED receipt) or declared `not-load-bearing` with a reason; a
  clause that cannot fail under its own frozen spec is retired or declared,
  never silently counted. Criterion 25 credits a *tightening* shown to bite;
  this requires the accounting for every clause before first data.
  Round-35's `c1/clauses.json` (read this seat) already implements the shape:
  nine controlled clauses, one declared (`o-nofollow-open`,
  reason TOCTOU-only), one retired (`r34-word-bound-1-25`); the do-nothing
  receipt `controls/c2-donothing.txt` reads `uncovered=1 TARGET_MISSED`.

**Not drafted (applications of existing criteria / outside scope):**

- `class: ledger` (round-32 SCORECARD row citing `cited_entries=3` against a
  frozen 7; the S189 "line 128" cited without naming which quote): a
  line-number quote locator that names no span is already covered by
  criterion 23's token-level receipt binding and criterion 10's re-derived
  counts. Round-34 repaired it by the C2 counter (`line=169` vs the
  `line=128` card, both run) and the appended correction in
  `corpus/lessons/round-33.md`. Application, no new criterion.
- `class: id-space` (the register's `S201` is the campaign's pre-remap
  staging id, not the lane's): a collision guard's clearance names the two
  id spaces it compared. This is a candidate criterion for a future round if
  the gap recurs; one mistake does not outrank the two above under the
  at-most-two bound. Recorded here, not drafted.
- `class: hygiene` (19 untracked paths at the round-33 closure; receipts
  whose fixture inputs were never committed): criterion 50 already requires
  a claim leg's ephemeral bytes to be committed or the verification-basis
  receipt named, and the round-34 disposition (18 trees committed, one moved
  to `/fast/scratch/mado-r33-k2-receipts/` with `ORIGIN.md`) was verified by
  the outside spotcheck (`round-34-verifier-spotcheck.md` §The inherited 19
  paths). Application, no new criterion.

## Style check (draft conforms to the lane's numbered-criterion form)

- Numbering continues 55, 56 after criterion 54; both carry a `lessons/`
  citation on the numbered line (satisfies the resolved-active rubric the
  round-30 grounding repair installed).
- Each criterion names the existing criterion it extends (36, 25) and
  states it does not rewrite it; the "append, never rewrite" rule of
  `corpus/QUALITY.md` is followed.
- Round-35 application evidence inside each draft cites only committed
  receipts this seat read: `controls/c1-entry-symlink.txt`,
  `controls/golden.txt`, `controls/c2-donothing.txt`, `c1/clauses.json`.
- Both draft criteria end with an explicit `Limit:` clause, matching the
  style of criteria 27–31.

## Limits

- The draft is text only; no criterion checker was written or run. Whether 55
  and 56 land is the round's closure decision; the draft supplies the
  numbered text, the citations and the supersedes/extends mapping only.
- [INF] Criterion 36's "indirectly-fake" shapes (server echo, fixture-keyed)
  arguably already gesture at indirection; the draft still extends it because
  none of 36's named shapes is a filesystem indirection that *holds the real
  bytes* — the exact hole the round-33 crib exploited.
- [UNK] Whether the id-space gap (register vs lane S-ids) deserves its own
  criterion later depends on whether it recurs; this seat records it as a
  candidate, drafted nothing for it.

## Installs

none
