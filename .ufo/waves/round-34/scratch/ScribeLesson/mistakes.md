## Mistakes

- class: ledger. evidence: `corpus/lessons/round-33-verifier-spotcheck.md` item 1;
  the row still reads target met at `cited_entries=3` while the independent
  r32 counter prints `cited_entries=7` on `d9ed38166cc3be8ef4c52b41d66ad94010feb047`.
  captured-by: none at write time; found post-hoc by the r32 spot-check's
  counter re-run. fix: appended line `r33-claim-verdict: r32-C1 cited_entries=7
  verdict=honest-stop rev=d9ed38166cc3be8ef4c52b41d66ad94010feb047`
  (`SCORECARD.md:2097`, commit `d40b35f90ad8bf630ad9404d25aeee1d9737f300`);
  the false row stays visible and is not the last matching line, so only
  last-match tooling sees the correction.
- class: instrument. evidence: `corpus/lessons/round-33-verifier-spotcheck.md`
  §Claims and `.ufo/waves/round-33/controls/c1-symlink-fix-demo.txt`: the frozen
  r33 `c1/count.py` prints `TARGET_MET` on `scratch/CriticC1Junk`, a crib of
  absolute symlinks into the real fetch blobs. captured-by: none of the
  pre-data control fixtures contained a symlink crib; the CriticC1Junk seat
  killed the predicate before data. fix: the frozen counter was not replaced;
  `.ufo/waves/round-34/controls/r33-counter-on-its-crib.txt` still shows
  `verdict=TARGET_MET` on the same crib while `c1-symlink-crib.txt` shows the
  new frozen r34 counter `TARGET_MISSED` (`closed_entries=0 closed_rows=0
  open_cites=2`), and the entries were admitted at
  `fa7ba11346116672352b5d41494141c5c4d738d0`.
- class: reference-drift. evidence: `corpus/lessons/round-33.md` §Gate calls the
  S189 queue-cap quote "line 128 of the pinned EventManager.cpp" two bullets
  after citing it at line 169 of the same file; line 169 of
  `.ufo/waves/round-32/fetch/S189.bin` is `const size_t MAX_QUEUED_EVENTS = 64;`
  and line 128 is `formatEvent`'s `eventString` assignment.
  captured-by: none in the lane; the closure's hand-check re-opened the fetch
  (`corpus/lessons/round-33-verifier-spotcheck.md` item 11, disagree-on-the-line
  row). fix: appended correction marker `r34-s189-line: line=169`
  (`SCORECARD.md:2108`, commit `fa7ba11346116672352b5d41494141c5c4d738d0`);
  this lesson; the filed round-33 lesson is not edited.
- class: disclosure. evidence: `corpus/lessons/round-33-verifier-spotcheck.md`
  §Uncommitted paths: 19 untracked directories; the report names 7 and does
  not name the 12 seat scratch trees `scratch/{CriticC1FalseNeg,ExecAppendDraft,
  ExecCollision,MutC1Counter,ReviewC2Predicate,ReviewRound30,ScoutConsider,
  ScoutQuarantine,ScoutS189Quote,ScoutS190,ScoutS191,ScoutS197}/`; it also
  says `ExecK2Receipts` is 547 MB where `du -sb` prints 495961904 bytes
  (473.0 MiB). captured-by: none at write time; the report's own
  untracked-leftovers disclosure missed them and `git status --porcelain`
  caught them. fix: spotcheck routed defect 4 — dispose the 12 trees with a
  named disposition, not a silent sweep; the r34 report corrects the size.
- class: overclaim. evidence: fleet `.ufo/reports/round-33/mado.md` §Trend
  verdicts says quality **improved** on the strength of the appended
  correction and the locator repair; `corpus/lessons/round-33-verifier-spotcheck.md`
  §Trend verdicts records unchanged — no weaker knowledge entry was superseded,
  no admitted entry was re-verified, and the locator edit is an instrument
  change without a committed re-run. captured-by: none; trend verdicts are
  self-scored and the disagreement only surfaced in the outside spot-check.
  fix: this lesson records the disagreement and restates quality as
  unchanged; a claimed trend move now needs a resolvable evidence pointer
  per verdict, same bar as SHONEN promotion boxes.
