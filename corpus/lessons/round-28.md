author: mado

# Round 28 — finite mutation evidence and the S183 gate

Base: lane tip `4f610066efd90804b055c42ae20c41a7f44404f9` (`master`).

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M27-3 | premature-saturation | `.ufo/waves/round-27/w1/reports/CritC1Counter.md:118-143` records shortcut readers meeting v2/v3 at 41/41; the v4 pilots reject GlobalOnce, FileScope, and PrefixKeyed at `.ufo/waves/round-27/controls/v4/K1GlobalOnce-L1pilot.txt:49-50` (18/41), `K1FileScope-L1pilot.txt:49-50` (24/41), and `K1PrefixKeyed-L1pilot.txt:49-50` (16/41). | Round-27 pre-data kill rule (`.ufo/waves/round-27/registration.md:81-87,156-172`), applied by w1 `CritC1Counter`. | Retire a counter when a critic-derived control meets target before data, expand its predicate for the demonstrated shortcut shapes, and re-score. Counter v4 rejects these three cited controls (all `TARGET_MISSED`, exit 1); this demonstrates rejection of these controls, not every short… |
| M28-1 | vacuous | Composite `count.py:100` pins count-v4.py at `3d7d301f…`; committed bytes are `635ae788…` at freeze 5198cc8 and r27 tip 20022a65, so the boolword leg could never print inside the composite (`evidence/c1-after-77cdda86.txt` shows `normal=missing mutant=missing` while the leg's declared commands pass standalone: 41/41, 2/2; mutant 0/2). | `none` — pre-data kill rules scored controls against counters, never required one composite smoke run at freeze. | Run the composite once at freeze before declaring its predicate; the defect is shown able to fail by the composite's own TARGET_MISSED output at 77cdda86 while both declared leg commands exit as frozen. |
| M28-2 | stale-premise | Registration declares "Leg 1 alone depends on the inherited ephemeral H1 directory"; `/fast/scratch/hyaku/mado-r27/heldout` was cleaned before closure, so h1-rotation re-runs `rc=2 no-tally` at 77cdda86; w1 `CritCalibration.md` §5 had explicitly advised preserving the H1 input at its registered path through adjudication. | `none` as a QUALITY criterion (named only in the w1 critic advisory) — now QUALITY criterion below. | A claim leg depending on ephemeral bytes names its committed receipt as the verification basis at data time; this round demonstrates the fix: leg 1 verifies from the committed `ReviewerSuiteMonotone.md` receipt (h=18/18, monotone) with H1 absent. |
| M28-3 | survivor | First refpub draft carried comment-only benign rows (AST-identical → invalid) and `ref-chk-no-anchor`, which shares M2's class but not suite B's discriminator, so it SURVIVED first scoring. | `none` — the frozen counter itself caught both (invalid rows printed; `SURVIVED` row). | Read the suite's probe list before authoring mutants (second draft: 12/12 killed, `h_min_per_subject=4`, `evidence/c1-after-77cdda86.txt`). |

## Attempt-completion addendum (2026-10-24)

The completing attempt inherited this lesson plus committed counters, controls, H2, q36 fixtures, suites and
wave evidence through tip `317ff19` (seven watchdog `lane-dead-no-report mado round=28` lines; attempt 1 of
2026-10-23 OOM-killed mid-work). It restored the oracle byte-identically (tinywl `227a74af…`, libwlroots
`1f3d7036…`, via `.ufo/waves/round-26/harness/build-tinywl.sh`), authored and sealed the public reference
set `c1/refpub/` (12 mutants + 6 benign rows; frozen counter 12/12), regenerated the q36 witness receipts,
re-ran both frozen counters at tip `77cdda86`, and wrote the round records. No leg rule was changed after data.

## Gate

S183 was opened this round on 2026-10-23; the DOI reader returned CrossRef metadata with no abstract.

| id | source path | URL | access date | located quote (≤25 words, verbatim) |
|---|---|---|---|---|
| S183 | DOI reader, CrossRef `title` field | https://doi.org/10.1145/2635868.2635929 | 2026-10-23 | `Are mutants a valid substitute for real faults in software testing?` |

**Decision:** the title frames the research question only; no article result or method detail is attributed. The S183 row (`corpus/SOURCES.md:195`) and the gate note (`corpus/knowledge/mutation-testing-r28.md:31-34`) agree; no discrepancy.

## Notes

**C1:** This lesson informs C1's operability claim only by bounding the interpretation of its finite mutation gate; it does not establish real-fault detection.

**C2:** C2 is the calibration claim and is not measured or repaired by this lesson.
