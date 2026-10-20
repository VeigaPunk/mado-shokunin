# ScribeLog — round-20 LOG draft written; numbers and hashes left as «» for L1; one dispatch-accounting item routed

Scope: one file, `.ufo/waves/round-20/w1/drafts/ScribeLog.md`, drafted from the round-19 entry (`LOG.md:1312-1338`) and the round-19 draft skeleton (`.ufo/waves/round-19/drafts/LogDraft.md`). No wave result, receipt or measurement was rerun; every number round 20 must produce is `«»`.

## Findings

1. **Append point and baseline (read-only git).** `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 1f7f995:LOG.md | wc -l` = 1338; the same at `e629f73`. The entry is appended after line 1338. `e629f73` (`round-20: pre-registration …`, 2026-10-20T16:23:13-03:00) is an ancestor of `refs/heads/master` (`e629f731172b8238caffe50f152217ce56535fb4`); `1f7f995` is the round-19 closure commit; `b435568` is the round-19 tip; `9c54c56` is the pre-harm baseline. Subjects read with `git log -1 --format=…`.

2. **Tool identity (sha256 prefixes, `git show REV:tools/mado-tripwire.py | sha256sum`).** `1f7f995` 367be94773d8fec5, `e629f73` 367be94773d8fec5, `b435568` 367be94773d8fec5, `9c54c56` c1ae45a7573e536b. Matches the spec and the SCORECARD declared claims; the draft quotes these as the before/pre-harm tool values.

3. **Measured before-state exists and agrees with the pre-registration.** `.ufo/waves/round-20/evidence/measure-before.txt`: `RECEIPT tool=.ufo/waves/round-17/measure.py tool_sha256=de4c422b…cfcdc measured_commit=1f7f995caa…`, `"criteria": 28, "lesson_cited": 20, "score": 7.1429`. The draft cites 20/28 = 7.1429 and the 22/30 target as declared, and leaves after values as `«»`.

4. **Stale round-19 statements the draft corrects (append-only, per R19-V2 and R19-V5).**
   - `LOG.md:1324` "5/13 name S096 on the crediting line". The closure lesson gives 8/13 (any matching line) and 6/13 (first matching line) at `b435568`. The draft carries those as `«»` for L1 to re-verify rather than copying them as measured.
   - `SCORECARD.md:1167` repeats the 5/13 wording; `SCORECARD.md:1270-1271` already names the correction as a red for criterion 30.
   - "ten OM10 assertions" appears in `SCORECARD.md:1271` as a declared red; the correct figure is nine labeled occurrences / eight distinct, which the draft records as `«»`.
   - `LOG.md:1334` (round-19 "Harm watch PASS at `01b8094`") covers gate, classifier, suites and census only. The closure (`corpus/lessons/round-19-verifier-spotcheck.md` §C3) shows the precision no-harm condition was not covered; the draft adds a closure-scope correction. (`LOG.md:1309` is the round-18 entry and is not corrected here.)

5. **Counterexample reference used in the draft (sourced, not re-executed).** The closure's data-only fixture result (`9c54c56` exit 0 clean; `b435568` exit 1 `package_query/pacman:-Q`) is quoted from `corpus/lessons/round-19-verifier-spotcheck.md` §C3. I did not run `--scan` myself; the fixture is a committed round-19 file and was never executed by this seat.

6. **Dispatch accounting anomaly (routed to L1, unresolved).** `.ufo/waves/round-20/w1/task-result.json` lists `attempts: [[1,"16:36",85],[2,"16:39:52",85],[3,"16:42:57",0]]`, while `w1/dispatch.json` gives `counts: {spawn: 85, resume: 0, total: 85}` and its note says to issue exactly one batched taskCall. Two attempts each report 85 spawns about three minutes apart. Whether a duplicate spawn occurred is `[UNK]`; the draft leaves the wave count as `«»` with a reconciliation instruction. `w1/reports/swarm-registry.json` (mode 0600) was not used for counts.

7. **Ids.** The draft leaves source ids `S1xx` and lesson numbers `«»` (L1 assigns, reserved range S099–S110) and names no new source row.

## Limits

- Ran no gate, selftest, counter (`tw-precision.py`, `measure.py`, `tw-recall.py`), fetch or host command. Nothing in the draft is a new measurement; numbers are placeholders or quotations of prior receipts.
- Did not check that the round-20 precision suite, `tw-precision.py`, the QUALITY 29/30 text or the new SOURCES rows exist yet; the draft refers to them as declared and leaves their state `«»`.
- Did not read the w1 seat reports (in progress at drafting time); the wave and dead-seat accounting in the draft is incomplete by design.
- Did not verify the round-19 `inns.sh` shape or the "155 transcripts" receipt; the draft cites them only as the SCORECARD declares them.
- The host-pause sentence in the draft is a statement L1 must verify from seat reports before integration; this seat does not claim it as observed.
- Lane files were read only; no git or jj write was made in the lane. Files written: the draft and this report.
- A mistaken in-place edit during drafting truncated this report; it was rewritten in full. The draft file was not affected.

## Installs

none
