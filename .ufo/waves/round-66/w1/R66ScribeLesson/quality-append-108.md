# QUALITY.md append — criterion 108 (round 66)

Insertion: append at the end of `corpus/QUALITY.md`, after criterion 107. Numbering continues from
107; the text below is a draft for L1 integration and is not itself an admission or a promotion.

---

## Criterion from the round-65 landing-instrument residue (round 66; lesson `lessons/round-66.md` M66-3 and M66-5, routed `lessons/round-65-verifier-spotcheck.md:135`)

**108. A leg-scored instrument's verdict comes from the child's contract marker and its exit status
together; a crash, a skipped child, or an absent marker is a distinct ERROR, never RED and never
GREEN (extends 23's outcome-token rule from a cited receipt to instrument aggregation).**

Scope. An instrument that runs child checks and prints an aggregate verdict — a standing landing
check, a suite driver, a counter harness. For every leg it must capture the child's combined output
and actual exit status, and bind them to a marker the child actually emits at the checked revision.
The marker spelling is read from the child's committed output or source, never from a remembered
literal; a declaration that names a marker the child does not print is a premise defect, corrected by
an erratum, not by renaming the child's output.

Verdict rule.

- GREEN leg: rc=0 AND the leg's own marker carries its green token — navigation
  `revision=… indexed=A/B missing=… dangling=… duplicates=…` with `A == B` and all three counts zero;
  used-by `MADO_USED_BY: … verdict=TARGET_MET`; ledger `LEDGER: … verdict=TARGET_MET`; citecheck
  `MADO_CITECHECK: … citations=<n> resolved=<n> missing=0 … verdict=TARGET_MET` with `citations` greater
  than zero (the citecheck leg keeps its non-empty evidence precondition).
- RED leg: rc=1 AND the marker carries the matching red token (`verdict=TARGET_MISSED`, or the
  named missing/dangling/duplicate list). A red result is an evidenced finding.
- ERROR leg: rc≥2; or rc=0 with no marker, an unparseable marker, or a marker whose token
  contradicts rc; or a required sibling that is absent or unreadable. ERROR is not a red finding.
- Aggregate: GREEN and exit 0 only when every leg is GREEN; RED and exit 1 only when at least one
  leg is RED and none is ERROR; otherwise ERROR and exit 2. ERROR dominates RED. A missing or
  inconsistent marker is ERROR even when the child exits 0.

Check. The instance instrument is `quality/landing-counters.sh` with `--round N` (default scope
`.ufo/waves/round-N/receipts`, explicit `--citecheck-paths` allowed, dirty guard applied to both).
Its hermetic `--selftest` must exercise real child-execution witnesses per leg, a skipped child with
rc forced to zero, a crash versus a genuine red, a missing used-by sibling, a dirty decoy round and a
dirty selected round, required `--round`/`--rev`, tmp-family scratch refusal and symlink-escape
refusal. The frozen control harness
`python3 .ufo/waves/round-66/check-controls.py --repo . --rev REV --claim c2 --scratch-root DIR`
must print `correct=4/4` for the four frozen conditions: genuine red child with its marker → RED/1;
child crash rc=2 → ERROR/2; child skipped or rc forced zero with no child marker → ERROR/2; missing
used-by sibling → ERROR/2. Four-case agreement is necessary, not sufficient: the frozen target also
requires the candidate's hermetic selftest green and a real four-leg landing GREEN, and a count
harness that prints `TARGET_MET` from the four discrimination cases alone over-credits the claim
(round-66 critic F1).

Shown able to fail, on the round-65 bytes: three legs rc=2 produced `MADO_LANDING_COUNTERS: RED …`
exit 1, identical to a genuine red, and selftest a9 passed on crashes
(`.ufo/waves/round-65/w1/R65CriticInstrument/report.md` §S5); a citecheck leg skipped with rc forced
0 read `GREEN` at a revision whose pristine run is RED
(`.ufo/waves/round-65/w1/R65MutCounters/evidence/probe-I1.log`); the default receipts tree
redirected to round 64 read `GREEN` (`…/probe-I7.log`); a missing used-by sibling read as red, not as
a crash (`…/probe-I9.log`), and the location-blind selftest read 19/19 with all three siblings
absent (`…/probe-location-blind.log`). The round-66 instrument's green arm is its committed
control receipt, not this text; at this seat's reads the candidate selftest was 56/56 on
`f0c8d74f…` and 58/58 on the later `1671cebc…` with an `empty population summary RED` case, but no
final count is pinned, the selftest used shimmed children, and the committed four-leg run was not
observed.

Declared limits.

- The marker check is bounded structural consistency, not authentication and not truth binding. A
  child that prints a correct marker over wrong data passes, and a malicious child that forges its
  own marker is out of scope.
- A green marker does not prove the underlying evidence is true: the ledger leg's
  `TARGET_MET` does not bind register state cells, and the used-by leg's `TARGET_MET` does not prove
  a source row's semantics.
- The ledger leg's marker spelling is the child's actual `LEDGER:` line; the round-66 declaration's
  `MADO_TOOL_LEDGER` literal is a recorded premise error
  (`.ufo/waves/round-66/marker-premise-erratum.md`), not the gate.
- The criterion does not make a child hermetic: criterion 29's fail-closed isolation and criterion
  95's write scope still carry child containment, and GIT-environment isolation is the instrument's
  own preflight, not protection against a concurrently hostile filesystem actor.
- The instance is credited only by a committed receipt at the integrated revision; the round-66
  evidence must land before the criterion is used to score a round.
