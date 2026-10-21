# LessonDraft — proposal-only findings

## Axes

- **Operability / binding correctness:** mine r21 FinalBindingReview F1–F5 under QUALITY criterion 32.
- **Calibration / precision and no-harm:** retain the r19 C3 precision gap under criterion 30, without treating six-line recall as a no-harm result.

## Behavior and findings

Authored six proposed mistake rows in `w1/notes/LessonDraft.json`: five distinct r21 F1–F5 cases and one r19 C3 precision/no-harm case. Each row names the source evidence, what the cited review reports, a bounded correction/limit, and its criterion pointer. R21's report describes six inert variants (five defect variants plus a control); this draft does not claim a repair. The C3 row preserves the rejected-harmed historical disposition and distinguishes recall, positive-side precision, and removal-side evidence.

The JSON records only existing report claims as historical evidence, not as measurements performed by this seat. Its count policy makes no round-22 or historical count changes: revise counts only after actual applicable red and green receipts, with their revision and producer/input provenance.

## Gates and provenance

- Read the round-22 registration and audit contract, the r21/r19 lessons and residual/closure evidence, the criterion 30/32 text, and this wave's seat contract.
- No build, test, selftest, detector measurement, fixture execution, new probe, package/live/service query, network access, Git mutation, or tool installation was performed. No new round-22 red/green evidence was available or consumed by this work.
- The r21 FinalBindingReview reports its one bounded probe as `python3 -c` invoking `runpy.run_path(oracle/measure.py)` and `scan(tool, fixture_dir)`, whose child was `sys.executable -I -c WRAPPER tool dir`; the report specifies 402653184-byte RLIMIT_AS and 15-second timeout. This is cited provenance only; I did not reproduce it.
- The r19 closure records copied-tool scans with `python3 -I tool.py --scan data-only.jsonl`, explicitly states the fixture code was never executed, and reports base clean versus changed-tool unmarked package_query. This is cited closure evidence only; I did not rerun it.

## Touched surfaces

- `.ufo/waves/round-22/w1/notes/LessonDraft.json` — new proposal.
- `.ufo/waves/round-22/w1/reports/LessonDraft.md` — this scoped report.

No canonical lesson, `QUALITY.md`, `SOURCES.md`, `LOG.md`, source code, or shared artifact was changed. No installations or updates.

## Limits and out of scope

This is an author-lane draft, not sealed truth, a round closure, a non-author judgment, or proof of repair. The r21 reports characterize `Timer.run()` as sharing a source path but the cited fixture tests `Thread.run()` only. The r19 numbers remain historical and criterion 30 does not by itself supply independent calibration or prove absence of recall loss. Counts and repair status require the named future receipts; this seat made no such measurements.

## Artifacts

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/notes/LessonDraft.json`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/reports/LessonDraft.md`
