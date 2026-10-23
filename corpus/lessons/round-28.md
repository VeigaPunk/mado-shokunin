author: mado

# Round 28 — finite mutation evidence and the S183 gate

Base: lane tip `4f610066efd90804b055c42ae20c41a7f44404f9` (`master`).

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M27-3 | premature-saturation | `.ufo/waves/round-27/w1/reports/CritC1Counter.md:118-143` records shortcut readers meeting v2/v3 at 41/41; the v4 pilots reject GlobalOnce, FileScope, and PrefixKeyed at `.ufo/waves/round-27/controls/v4/K1GlobalOnce-L1pilot.txt:49-50` (18/41), `K1FileScope-L1pilot.txt:49-50` (24/41), and `K1PrefixKeyed-L1pilot.txt:49-50` (16/41). | Round-27 pre-data kill rule (`.ufo/waves/round-27/registration.md:81-87,156-172`), applied by w1 `CritC1Counter`. | Retire a counter when a critic-derived control meets target before data, expand its predicate for the demonstrated shortcut shapes, and re-score. Counter v4 rejects these three cited controls (all `TARGET_MISSED`, exit 1); this demonstrates rejection of these controls, not every shortcut. |

## Gate

S183 was opened this round on 2026-10-23; the DOI reader returned CrossRef metadata with no abstract.

| id | source path | URL | access date | located quote (≤25 words, verbatim) |
|---|---|---|---|---|
| S183 | DOI reader, CrossRef `title` field | https://doi.org/10.1145/2635868.2635929 | 2026-10-23 | `Are mutants a valid substitute for real faults in software testing?` |

**Decision:** the title frames the research question only; no article result or method detail is attributed. The S183 row (`corpus/SOURCES.md:195`) and the gate note (`corpus/knowledge/mutation-testing-r28.md:31-34`) agree; no discrepancy.

## Notes

**C1:** This lesson informs C1's operability claim only by bounding the interpretation of its finite mutation gate; it does not establish real-fault detection.

**C2:** C2 is the calibration claim and is not measured or repaired by this lesson.
