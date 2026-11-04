# QUALITY criteria — two candidates from round-72's own defects

Drafted by wave seat R72ScribeLesson 2026-11-04. A rule counts only when the round's own
fail lines back it — both candidates below cite exactly such lines, all committed.
Numbering (116)/(117) is a draft placeholder; the L1 assigns. Style follows criteria
112–115.

**116. A summary-derived credit counts only when the run's own failure detail backs the
summary line.**
(a) A rule that credits a kill from a parsed `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n>
assertions passed` summary must additionally require the run's own `SELFTEST FAIL` lines
to number exactly `n − p`: a summary line that no assertion of the run produced (a bare
echo), and a summary whose failure count is not backed by the run's fail lines, earn no
credit. (b) Both captured streams are read — the credit rule is stream-agnostic but not
stream-forgetting.
Lesson that produced it: `corpus/lessons/round-72.md` § Outcome, C1 — the held round-71
rule `mz_killed = summary_shows_failure(out)` scored the round's own frozen control set
6/8, crediting `bare-failing` and `mismatch-detail` where the truth is no credit.
Shown able to fail: `grep 'correct_for_held=NO' .ufo/waves/round-72/control-baseline-c1-r72.txt`
prints exactly the two modes `bare-failing` and `mismatch-detail` (committed at
`5601e526`), while the successor scores `correct=8` (`.ufo/waves/round-72/measurement-c1-r72.txt`,
committed at `fd9ea03b`).
Limits: the eight modes are a finite control set, not fault coverage; the rule reads the
child's report, it does not authenticate it — a summary replayed with its own matching
detail lines stays byte-indistinguishable from a genuine run; the fixture lane is the
counter's own instrument.

**117. A run's outcome verdict is read from the subject's own last parsed summary, not
from its exit status.**
(a) A contract verdict of `TARGET_MET` requires the kill count to be complete **and** the
extracted instrument's **last** parsed `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n>
assertions passed` summary to have `n > 0` and `p == n`; a missing or garbled summary
earns no green. (b) The exit status is recorded for the reader but does not gate the
outcome: one status bit is derived from the result object (held ground S445, with
S441/S435), so a fully green summary with exit 2 passes and a failing summary with exit 0
fails.
Lesson that produced it: `corpus/lessons/round-72.md` § Outcome, C2 — the held round-71
`outcome_verdict(gate_rc, killed)` scored the round's own frozen case set 4/8.
Shown able to fail: `grep 'base_correct=no' .ufo/waves/round-72/measurement-c2-r72.txt`
prints exactly `failing-summary-exit0`, `green-summary-exit2`, `no-summary-exit0`,
`garbled-summary-exit0` (committed at `fd9ea03b`), matching the pre-freeze held-leg
baseline `control-baseline-c2-r72.txt` (committed at `5601e526`, `held_correct=NO` on the
same four).
Limits: the eight cases are a finite set over the summary grammar the production
instrument prints; the counter scores the committed functions, not the whole harness
execution; a case where the summary and the exit status contradict is scored by the
summary by design.
