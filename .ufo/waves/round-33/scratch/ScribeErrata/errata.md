# round-32 errata — repairs r33 can land without editing the filed report

Source: `corpus/lessons/round-32-verifier-spotcheck.md` (routed defects 1–12). The filed report
`.ufo/reports/round-32/mado.md` stays byte-unchanged; every repair below is an append, a new
file, or a repo-hygiene action. All figures re-executed at write time (see companion report
`.ufo/waves/round-33/w1/reports/ScribeErrata.md`).

1. **D1 — falsified claims row standing.** Append a dated correction entry to `SCORECARD.md`
   (append-only) superseding the round-32 C1 row's "target met … `cited_entries=3`" with the
   verifier-measured tip value `entries=3 rows=5 cited_entries=7` at
   `d9ed38166cc3be8ef4c52b41d66ad94010feb047` and the verdict `unprovable` (honest stop).

2. **D2 — report timeline inaccuracy.** Append an erratum restating the sequence with
   committer timestamps: 20:05:38 belongs to `50e6a8f32bfaf0487b2762eb3b5c9f51ed54b75c`
   (ExecCollisionGuard report), the data commit `f5910876486943d967e6994e21ccddb9aee4f249`
   landed at 20:22:50 — ~14m50s after `CriticC1Predicate.md` (20:08:00) — and the "target met"
   claims row `a551f71c` landed at 20:27:38, ~19 min after the falsification was known.

3. **D3 — "187 MB" unsupported by history.** Append a correction replacing the on-disk figure
   with the committed bytes: the seat scratch was 187 MB **on disk**, but what `f5910876`
   committed under `.ufo/waves/round-32/scratch/` is 11.6 MB / 554 blobs and `48f9fe09`
   deleted 130 files / 2.7 MB of it, so "bytes remain in history" covers 11.6 MB, not 187 MB.

4. **D4 — gate not registered.** Add `quality/check-axis-scores.py` to `SKILL.md`
   `## Gate registry` as a new row (command, verdict map, selftest spelling 17/17, write
   scope, owner mado) so the gate conforms to PROTOCOL §Gate standard.

5. **D5 — K2 control receipts missing.** Commit the C2 do-nothing receipts under
   `.ufo/waves/round-32/c2/controls/` (the dir currently holds only the critic's
   `c1-predicate-attack` trees) or append a registration erratum re-pointing the promised
   reference to their actual committed path.

6. **D6 — CriticC2Predicate DEAD verdicts undisclosed.** Append a disclosure naming attacks 3
   and 5 (CLAIM DEAD: `rfind` locator shadowing by quoted errata, 400-char parse truncation,
   single-axis control coverage) and route the locator and control-coverage repairs to r33,
   noting they do not change the measured before→after.

7. **D7 — five uncommitted round-30 leftovers.** Resolve the five paths `git status
   --porcelain` shows at closure — modified `.ufo/waves/round-30/w1/reports/RevRecordsChain.md`,
   `RevTrendExpansion.md`, `SentScope.md`; untracked `RevTrendDiscernment.md`, `SimplifierC2.md`
   — by committing them under a round-33 entry or reverting them, so landed-means-committed holds.

8. **D8 — budget-overrun claim unreconciled.** Append a budget correction: the watchdog digest
   shows launch 19:56:38 → complete 20:33:30 = **36m52s** wall for attempt 1, well under
   `ROUND_MAXTIME=170m`, so the report's "~35 minutes over its 170-minute budget" is retracted
   unless its accounting is shown.

9. **D9 — unresolvable base hash.** In every appended correction and future table, cite the
   registration base as `256222890d935212874a09751ff9b7869943c2d7` (short form `2562228`);
   `25622288` fails `git cat-file -t` and the existing SCORECARD rows are append-only, so the
   fix is prospective citation, never a rewrite.

10. **D10 — omitted commits in the report's commit order.** Append the corrected order —
    operator `a327cd4`, `57a772b`; lane `b1b740d16875b91ac37546b2958d5b016db97c06` (id-collision
    guard) → `50e6a8f3` (ExecCollisionGuard report) → `f5910876` → `48f9fe09` → `a551f71c` →
    `d9ed3816` — since both omitted commits carry work items the report cites.

11. **D11 — S189 cleared-then-adopted wording.** In the appended corrections, state the actual
    flow: quarantine-slice row S189 was hand-checked PRESENT and then adopted, so the flat
    sentence "No quarantined row was appended" must read "no unverified quarantined row was
    appended; S189 was cleared by hand-check before adoption" (S224 and the 7 UNVERIFIABLE rows
    stayed out).

12. **D12 — pre-freeze junk control.** Fold a §9 cheapest-control rule into the counter repair
    already routed to r33: no predicate freezes without its junk-tree control run **before**
    data lands, so a two-sided junk commit (junk control hit `entries=3 rows=5
    cited_entries=3`) can never pass a frozen target again.
