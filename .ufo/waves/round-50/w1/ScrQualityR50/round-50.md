# mado round 50 — mistakes (draft of the M50-1 row, seat ScrQualityR50)

Draft only: `corpus/lessons/round-50.md` does not exist yet (`test -f` → absent at the round-50 base).
This file carries the one row criterion 102 cites, in `corpus/lessons/round-49.md`'s row format, so the
row has a location to cite before the L1 lands the lesson. Line numbers are this file's, computed by `receipts/locators.txt`; the
criterion's `(lesson:)` line names `corpus/lessons/round-50.md#mistakes M50-1` and must be re-anchored
when the L1 lands this row there.

## Mistakes

**M50-1** · class `ordering` (the round report was committed before the wave's results existed) · evidence: round 49's report
(`.ufo/reports/round-49/mado.md`, fleet commit `b0184c43`) was filed with 7 w1 seats unsettled and no WAVE-DONE, while
`.ufo/waves/round-49/w1-results.json` is not in the lane's closure commit — `git cat-file -e
8a370cd4:.ufo/waves/round-49/w1-results.json` → `fatal: path '.ufo/waves/round-49/w1-results.json' exists on disk, but not in
'8a370cd4'` — and the file present in the worktree now (227 903 B, mtime 2026-10-27 02:58, untracked `??`) was written while
round 50 w1 was running; the dispatcher writes that file only at wave finalize (`scripts/hyaku/inline-dispatcher.py:295`), and
round 49's wave never finalized. 2 of the 7 unsettled seats (`ExecSessionTriage`, `SentPrivacy`) have no report file at the
closure commit (`git cat-file -e` → absent for both). · captured-by: none (no criterion required a wave's results before the
report commit). · fix: criterion 102 + `quality/check-wave-done.py`, run at integration with its receipt committed beside the
report; its audit form reads the results file at the report's revision, so a file written after closure cannot green the run
(this seat's prototype `w1/ScrQualityR50/check102-wave-done.py` reproduces the round-49 verdict: `RESULTS_NOT_AT_REV`, rc 1).
