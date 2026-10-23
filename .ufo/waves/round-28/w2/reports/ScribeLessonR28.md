# ScribeLessonR28 — scoped report

## Behavior and axes
- Wrote the round-28 lesson with one mined M27-3 mistake, the S183 gate row, and one sentence each relating C1 and C2 to the lesson.
- Axis: the lesson bounds interpretation of C1's finite mutation evidence; it adds no new C1 counter measurement. C2 calibration is explicitly outside the lesson's measurements and repairs. No coverage claim or score moved.
- S183 is used only as a title-level research question. No article result or method detail is attributed.

## Gates and findings
- The DOI reader for `https://doi.org/10.1145/2635868.2635929` returned CrossRef metadata; the `title` field was “Are mutants a valid substitute for real faults in software testing?” (11 words), and no abstract was available.
- Cross-check: `corpus/SOURCES.md:195` identifies the DOI metadata title and frames the empirical question; `corpus/knowledge/mutation-testing-r28.md:31-34` records the same URL, date, title-field quote, and no-result decision. No disagreement found.
- M27-3 evidence resolves at the lane tip: `CritC1Counter.md:118-143` records prefix-keyed, GlobalOnce, and FileScope shortcuts meeting earlier counters at 41/41; the round-27 v4 pilot receipts have `TARGET_MISSED`, exit 1 at lines 49-50 (GlobalOnce 18/41, FileScope 24/41, PrefixKeyed 16/41). This shows the cited fix can reject those controls only, not all shortcuts.
- No test, build, counter, or scorer was run for this scribe item. No check failed. SOURCES.md, QUALITY.md, registration, and counters were not edited. No tools were installed; no scratch files were written.

## Commands and checks
Commands below were read-only; exit codes are the observed successful command status.

```text
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse master
exit 0
4f610066efd90804b055c42ae20c41a7f44404f9

test ! -e /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-28.md && printf 'absent\n'
exit 0
absent

test ! -e /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/w2/reports/ScribeLessonR28.md && printf 'absent\n'
exit 0
absent
```

- Opened the DOI with the static reader: method `crossref`; title as above; output says `No abstract available.`
- Line-numbered repository grep checks (the specialized grep tool; it does not expose a shell exit code): lesson anchors at `round-28.md:7,11,13,19,23,25,27`; S183 cross-check at `SOURCES.md:195`, `mutation-testing-r28.md:31-34`, and new lesson `round-28.md:19,21`.
- Evidence reads confirmed `CritC1Counter.md:118-143`, `registration.md:156-168`, and pilot receipt lines `49-50` for each of K1GlobalOnce, K1FileScope, and K1PrefixKeyed. Their printed verdict/exit lines are respectively `18/41 TARGET_MISSED`/`exit=1`, `24/41 TARGET_MISSED`/`exit=1`, and `16/41 TARGET_MISSED`/`exit=1`.
- The lesson write tool reported `Successfully wrote 1894 bytes` to `corpus/lessons/round-28.md`.

## Touched surfaces and artifacts
- Wrote `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-28.md` (1,894 bytes).
- Wrote `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/w2/reports/ScribeLessonR28.md`.
- No other files changed by this seat. No builds/tests were run, so none are claimed as passed.
