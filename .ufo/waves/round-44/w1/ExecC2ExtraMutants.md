# ExecC2ExtraMutants — C2 clause-mutation population (round 44, w1)

Lane `mado-shokunin`, base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`, data-freeze `e2289516a9a857f55cda7be635933e89b931c3da`. Assignment: build a
positive fixture for `PRED-C2-r44`, then a population of single-defect clause mutants of it, and report every mutant the counter still admits.

**Result: the positive fixture is admitted (1/1); 51 single-defect mutants were built, 48 score 0/1 and 3 score 1/1 — two of those three are
predicate defects/gaps, the third is the declared quote-to-claim residual.**

Nothing tracked in the lane was edited: the work is a scratch clone at the frozen revision plus this seat directory. No counter, control,
registration or reference file was touched.

## Positive fixture

The same shape the C2 counter docstring prescribes (`quality/counters/c2-r44-gkeep-size-request.py:1-44`), built from the five frozen pins:

- entry `corpus/knowledge/hyprland-gkeep-size-request-r44.md` (`entry.md`), citing held `S164` (Hyprland-Window.cpp) and four new rows
  `S298` XDGShell.cpp, `S299` xdg-shell.xml, `S300` gdktoplevel-wayland.c, `S301` gkeep-ui.py — i.e. one cited id per pin, so clause i's
  "every PIN is a Gate receipt" is discharged by the real bytes;
- registry rows appended to `corpus/SOURCES.md` (`S164` used-by extended, cells 1-9 untouched), README index row, and `corpus/lessons/round-44.md`
  with the five `GATE` lines (sha256 = the PINS values) plus `ADMIT gkeep-client-size-request-r12.md` and `REFUSE
  gkeep-geometry-never-recorded-r15.md … flip once …`;
- the two clause-h census lines recomputed from the pins by the counter's own functions:
  `gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep` and
  `hyprland sendWindowSize xdg_setSize=1 x11_configure=1` (`Window.cpp` sendWindowSize body = lines 1732-1754; `setSize` once, `configure` once).

Evidence (fixture commit `99ad0ddb9d7c4bee400f193ecb8cb22d9f51d377`):

    python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo <fixture> --rev HEAD --base 6a1a90528fe533cadee506a9fa3e9d13d15cc41f
    -> PRED-C2-r44 hyprland-gkeep-size-request-r44.md clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1
    -> PRED-C2-r44: admitted=1/1 verdict=TARGET_MET rev=99ad0ddb9d7c4bee400f193ecb8cb22d9f51d377    (rc=0)

`positive-score.txt` is the full run; `positive.patch` is the whole diff against `e2289516`. Applying `positive.patch` alone to a second clone at
the same revision scores the same (`rev=f73972e357e08ffaa301995acadd9d4e21e31a2b`), so the fixture is reproducible without the seat's scripts.

Every quote used was computed, never typed: `quote_at` / `occurrences` / `quote_in_code` were imported read-only from the frozen counter and run
over the pinned bytes; the chosen quotes are `const auto REPORTSIZE = realToReportSize();` (Window.cpp:1741), `m_stateUpdate =
g_pEventLoopManager->doLaterLock([this] { configure(); });` (XDGShell.cpp:633), `This configure event asks the client to resize its toplevel
surface or to change its state.` (xdg-shell.xml:1146), `if (saved_size && !fixed_size && was_fixed_size)` (gdktoplevel-wayland.c:656) and
`window.set_default_size(420, 500) self.board = Board(window)` (gkeep-ui.py:476, a two-line join) — each occurs exactly once, word-bounded, and
outside comments.

## Mutation population

51 mutants, each ONE defect applied to the positive commit, committed, scored, saved as `mutants/<name>.patch`, then the tree reset to the
positive commit. `scores.tsv` holds name, one-line defect, verdict, final counter line and the full `clauses=` vector for all 51.

The assigned classes are all present: header window (01), `source:` outside the window (02), ghost `S###` (03), row cell edits (06-09, 11-13,
40, 45, 47), used-by missing/renamed (07, 47), held `S164` cells 1-9 (11, 12), Gate sha wrong (14), quote in a comment (15), quote twice (16),
locator off by one (19), census numbers (21, 22), census inside a fence (23), census duplicated (24), README row missing/doubled (25, 26),
`ADMIT gkeep-size-to-real-size-r11.md` (27), REFUSE without a flip word (29), a pin left uncited (36, 37, 35) — plus quote length/word-boundary
(17, 18), cross-receipt quote (48), Gate placement (32-34), and clause-i REFUSE shapes (28, 30, 31, 44). 48 mutants score
`admitted=0/1 verdict=TARGET_MISSED`.

Kill attribution (`scores.tsv`): b 5 isolated, c 10, d 1, e 1, f 2, g 5, h 5, i 7; the rest are coupled — a quote that is unusable makes d and g
fail together, and usually i as well, because the id drops out of `receipts` and the PINS coverage test then misses that receipt.

## Survivors (full detail in `survivors.md`)

1. **`51-census-prefix-hides-claim` — admitted, predicate defect.** The clause-g line filter is
   `not l.startswith("gkeep client ")` / `not l.startswith("hyprland sendWindowSize ")` (counter:560-563). Exact-line exclusion
   (`l not in census_lines`, counter:561) already removes the two census lines, so the prefix tests only create an exemption channel: the line
   `hyprland sendWindowSize S299 is the document that licenses this whole section` names a cited id with no quote and no locator, is skipped by
   `all_body_lines_bound` (counter:354-367), and the entry is admitted (`admitted=1/1`).
   Measured fix in a seat copy (`fix-counter.py`, NOT applied to the lane): drop the two `startswith` clauses → mutant 51 goes to
   `admitted=0/1` (g:0) and the positive fixture stays `admitted=1/1` (a..i all 1). The clause's stated goal — "neither line is a clause-g claim
   line" (counter:24-25) — is already met by exact equality.
2. **`50-row-kind-ownwork` — admitted, predicate gap.** Setting S300's registry `kind` cell to `own-work` for an upstream file changes nothing:
   clause c tests status, opened, recheck, used-by and the location token (counter:453-472), clause e the location, clause i `BAD_LOC` only, and
   the round-44 clause h (`host_census`, counter:382) never reads a row's kind — its `new_ids` argument is unused. The r43 "three new rows have
   kind own-work" test survives only in the inherited text (counter:107). Counter is faithful to its own docstring, so this is a coverage gap to
   register, not a counter bug.
3. **`49-misread-quote` — admitted, declared residual.** The S300 claim keeps its true quote at the true locator and the prose around it asserts
   the opposite. Every syntactic clause holds because every syntactic fact holds; this is the residual the registration already declares ("a real
   quote at a true locator can be cited for a claim it does not support"). Listed because the counter admits it, not because a clause should fire.

Method note (disclosed): the first form of mutant 33 inserted the moved Gate line just *above* the next `## ` heading — i.e. still inside
`## Gate` — and "survived"; its patch showed the mutant had not been applied as intended. It was re-formed (insert below the next `## ` heading)
and is killed (d+e+g+h+i). Every surviving mutant was re-checked by reading its patch, not only its score.

## Files (all under `.ufo/waves/round-44/w1/`)

- `ExecC2ExtraMutants.md` — this report.
- `ExecC2ExtraMutants/entry.md`, `lesson.md` — the positive entry and lesson Gate section (source of truth for the fixture text).
- `ExecC2ExtraMutants/positive.patch`, `positive-score.txt` — the fixture diff and its full counter run.
- `ExecC2ExtraMutants/mutants.py`, `fixture.py` — the builders (mutant table with one defect line per mutant).
- `ExecC2ExtraMutants/mutants/*.patch` (51), `scores.tsv` (51 rows).
- `ExecC2ExtraMutants/survivors.md` — the survivor analysis, kill attribution and the measured fix.
- `ExecC2ExtraMutants/fix-counter.py` — seat copy of the counter with the clause-g prefix exemption removed (experiment only).

## Limits

- The fixture is synthetic: its entry text is this seat's, so a 1/1 proves the predicate is satisfiable with a real citation set, not that the
  round-44 data entry is good.
- The census lines are bookkeeping over pinned bytes (declared residual); mutant 21/22/23/24/46 show they are exact-line tests, so any
  *plausible-looking* line that differs in a digit or sits in a fence is caught only because the recomputation is exact.
- The two predicate defects above were found by probing exclusions and unchecked cells; no attempt was made to enumerate every unchecked field
  (e.g. the `tier` cell is likewise untested — not built as a mutant, stated as the same class as 50).
- No tool was installed, no pacman transaction was run, no compositor verb beyond none at all, and the scratch tree was deleted; the fixture is
  the patch in this seat directory.
