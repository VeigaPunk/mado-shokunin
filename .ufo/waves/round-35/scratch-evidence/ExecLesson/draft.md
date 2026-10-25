## Mistakes

- class: instrument. evidence: the round-34 closure's routed defect 1
  (`corpus/lessons/round-34-verifier-spotcheck.md` §"Routed defects"): the
  `1 <= len(words) <= 25` clause in `PRED-C1-r34-v1`
  (`.ufo/waves/round-34/c1/count.py`) was checked against `found`, which
  `found == quote` pinned to a frozen short quote, so the clause was provably
  dead code under its own frozen spec. captured-by: the round-34 clause-drop
  mutation suite — `.ufo/waves/round-34/w1/reports/MutC1Drop.md` M5 could not
  flip any verdict. fix: retired, not silently kept — `c1/clauses.json`
  records `r34-word-bound-1-25` under `retired` with the reason, and the r35
  counter makes the entry's quote a free variable so the replacement clause
  `gate-quote-word-bound` is live and has a failing case
  (`controls/c1-quote-long.txt`, `verdict=TARGET_MISSED`, `open_cites=1`).
- class: instrument. evidence: routed defect 2 — the `S_ISLNK`/`O_NOFOLLOW`
  pair in `PRED-C1-r34-v1` was presented as load-bearing, but M2 of
  `MutC1Drop.md` is identical to baseline on every tree: no static tree can
  kill it; it is TOCTOU protection only. captured-by: the same mutation
  suite. fix: split, not dropped — in `PRED-C1-r35-v1` the `S_ISLNK`
  component walk is load-bearing (`controls/c1-entry-symlink.txt` prints
  `TARGET_MISSED` through it) while `o-nofollow-open` carries the ledger's
  single `not-load-bearing` declaration with its reason recorded
  (`c1/clauses.json`, and `c1/count.py:59-61`); `PRED-C2-r35-v1`'s
  `toctou_declared=1` leg counts the declaration, so a clause can no longer
  claim load-bearing status by assertion alone.
- class: ledger. evidence: routed defect 3 — the round-34 seat artifact
  `.ufo/waves/round-34/w1/reports/RevFrozenBlobs.md` measured its table at
  `fa7ba11346116672352b5d41494141c5c4d738d0` and labelled that commit the lane
  tip; the real round-34 tip is `dff394109f3cc3d851309ad7c67dd3b35b46adf2`,
  so the artifact's own label was stale by one commit. captured-by: the
  round-34 closure's re-verification of all seven frozen blobs at `dff3941` —
  the conclusion (PROVEN) stood; only the label was wrong. fix: re-issue, not
  rewrite — `.ufo/waves/round-35/ledger/RevFrozenBlobs-r35.md` names the real
  tip and re-measures the same seven paths there, and `PRED-C2-r35-v1`'s
  `ledger_tip_ok` leg re-verifies every listed blob id at that revision; the
  round-34 artifact stays in place as the record of what it measured.
- class: id-space. evidence: routed defect 4 — the shokuknow merge package's
  `merge/mado/ID-REMAP.md` computes its remap against "registry ends at S196"
  while the lane registry ends at S202, and repeats the lane's S186–S189 URLs
  as S199/S200/S260. captured-by: none lane-side — the id-collision guard
  only compares the registry against the staged ids and cannot see the
  package's remap base; the closure filed it as L0 in commit
  `ae2c52b82018904ad891c304ba023c846a19bd8e` (fleet `.ufo/l0-questions.md`,
  `mado | round-34` row) and routed it to the operator. fix: not duplicated —
  the lane renumbers nothing. The adopted rows continue the lane's own
  registry at S203–S210 re-pointed by document, and the package's ids for the
  same documents (S309, S310, S321, S329, S330, S331, S334, S336) are named in
  `.ufo/waves/round-35/registration.md:123-125` for the campaign to
  reconcile. The question stays open and operator-owned.
- class: instrument. evidence: this round's own clause audit — the
  `PRED-C1-r35-v1` spec text requires that a row's "cells contain no literal
  or escaped pipe", but `c1/count.py`'s `cells()` splits on `|` and honours
  no escape, so either pipe case adds a field and is already killed by
  `nf_ok = len(cs) == 11` (`c1/count.py:109-115,180`). The explicit pipe
  clause is redundant — subsumed by the field count. captured-by: the
  round-35 clause ledger itself — `c1/clauses.json` `row-well-formed`
  records the subsumption in its `why`, and the literal-pipe failing case is
  committed as `controls/c1-row-extra-field.txt` (`verdict=TARGET_MISSED`).
  fix: recorded rather than hidden — the field count is the load-bearing
  clause and the ledger names the pipe clause's dependence on it, so no
  clause is presented as carrying an independent kill it does not have; the
  spec wording stands because the field count implies it.
