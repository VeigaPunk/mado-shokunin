## Criterion from the round-70 record-order and commit-enumeration defects (round 70)

**112. An append-only insertion is anchored to the round whose heading encloses it, and a round's
landed-commit list is complete only when it is co-extensive with `git rev-list base..tip`.**
(a) A block appended to an append-only log belongs to the round whose heading encloses it: a block
that sits under another round's heading misattributes its facts even when no prior byte was deleted,
and the repair is an erratum in the current round's entry that names the misplaced copies — never a
deletion or a rewrite of the filed bytes. (b) A round's Landed-changes table is complete iff its
enumerated revisions are co-extensive with the revision range: `git rev-list --count base..tip` equal
to the table's data-row count is necessary, and an empty set difference between `git rev-list
base..tip` and the revisions the table names is the check. A table that is one row short is a defect
even when every enumerated row is correct.
Shown able to fail: round 69 — the ten-line `Critic closures … / Final measurement … / Wave
settlement …` block appears at `LOG.md:3257-3266` (inside `### Round 67`, `LOG.md:3220`) and
`LOG.md:3314-3323` (inside `## Round 68`, `LOG.md:3273`) as well as at its own `LOG.md:3396-3405`
(`### Round 69`, `LOG.md:3339`), all three copies from `139f4801`; the report's table enumerates 18
rows (`.ufo/reports/round-69/mado.md:69-86`) while `git rev-list --count
04093b83f73a841117d3b31dbb2a6063f4f2a454..9d91f7f6f5c603bdc19cf455ce6f413c5990d744` is 19, and
`b9b70a09` is in neither `LOG.md` nor `SCORECARD.md` (`grep -c` = 0 and 0). Both are re-derivable with
one command each: `awk '/^#+ Round/{r=$0} /Wave settlement: 12 seats dispatched/{print NR, r}' LOG.md`
and `comm -3 <(git rev-list BASE..TIP | cut -c1-12 | sort) <(grep -oE '[0-9a-f]{12}' REPORT | sort -u)`.
Receipt: `corpus/lessons/round-69-verifier-spotcheck.md` § Conformance defects 1–2.
Ground: `corpus/lessons/round-70.md` M70-1 and M70-2.
Limits: the heading sweep reads one log file with one block pattern, so a block split across two
headings, or a second log, is not covered; set equality proves the commit list is enumerated, not that
any row's description is accurate or that the commit did what its message says; and neither clause
detects an insertion that is anchored correctly but factually wrong.

## Criterion from the round-70 real-child kill-credit repair (round 70)

**113. A kill credit is a parsed failed assertion, not a nonzero exit status, and the credit is
evidenced with real children.**
A harness that reports a mutant killed must credit it from the child's own contract marker, parsed and
showing fewer passes than assertions; a crashed child (no summary), a garbled summary and a missing
executable earn no credit and are reported as setup failures, not as kills. The claim is evidenced by
running the harness over at least one scenario per failure mode with real child processes, and by
scoring the pre-change harness on the same scenarios so the before-leg is visible in the same contract
line.
Shown able to fail: at the round-70 base the held harness carries `mz_killed = mz_rc != 0`
(`quality/counters/c1-r69-landing-controls.py:452`) and credits both the crashed and the garbled
child: `.ufo/waves/round-70/measurement-r70.txt` prints `MADO_R70_SCENARIO mode=crash …
base_mz=pass correct=yes base_correct=no` and the same for `garbage`, with
`MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET
rev=5adba5a92a8d58eb76533b39a9216d8e85d48fbc`. The round-70 harness's credit is
`mz_killed = bool(mz_rc != 0 and summary_shows_failure(mz_out))`
(`quality/counters/c1-r70-landing-controls.py:478`), whose predicate parses
`MADO_LANDING_COUNTERS_SELFTEST: (\d+)/(\d+) assertions passed` and requires the fraction to be below
one (`:315-327`). The three scenarios are built as real `bash` children in a scratch git repository
with one commit per mode.
Ground: `corpus/lessons/round-70.md` § Outcome and boundaries (C1) and
`.ufo/waves/round-70/claims-declaration-r70.md` § C1.
Limits: three scenarios do not exhaust the kill-credit hazards; the fixture lane is a stand-in for the
lane's landing instrument, not that instrument; the credit is still a syntactic read of one summary
line, so a child that prints a plausible failing summary without running its assertions earns a kill;
and no clause here covers a harness whose measurement is wrong for reasons outside the marker.
