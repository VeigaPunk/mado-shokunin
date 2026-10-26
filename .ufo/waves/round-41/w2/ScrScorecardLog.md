# Seat Report: ScrScorecardLog (wave w2)

Draft deliverables (both written in the seat dir `w2/ScrScorecardLog/`):
- `scorecard.md` — SCORECARD.md `## Round 41` section draft (claims table with v2/v1 split disclosed, Capabilities row for `tools/mado-globals.py`, Sources/saturation, axis placeholder, Planned round 42).
- `log.md` — LOG.md `## Round 41` block draft (freeze/data/measurements/motivating evidence/wave facts).

## Sources read (all at the DATA commit 07f2641 unless noted)
- `git show 07f2641`: SCORECARD.md (full), LOG.md (full), corpus/lessons/round-41.md, corpus/knowledge/hyprland-focus-grab-r41.md, corpus/README.md, corpus/SOURCES.md, tools/mado-globals.py, .ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt, fetch/xdph-installed-version.txt.
- `.ufo/waves/round-41/registration-v2.md`, `registration.md` shape line, `w1-results.json` (outputs lost to kernel restart), `w2-spec.json`.
- w1 seat reports (headlines + findings): CritC1Cheat, RevC1Counter, CritC2Cheat, RevC2Counter, ExecC1ExtraMutants, ExecC2ExtraMutants, ExecDiffFuzz, ExecJournalFormat (via registration), RevRefTool, MutSelftestFixtures, MutC1CounterGates, ExecHarmChecks, ConnCrossClaim, ScrEntryA/B/C, ScrRowsDraft, ScoutPackageFocus, ScoutHeldOverlap, ScoutMergeRest, ExecQuarantineSlice, ExecLiveHost, ExecSrcProtocols, ScrQualityCriteria, ScrConsiderthese.

## Verification runs (all executed; read-only)
- `sha256sum` tools/mado-globals.py vs c1/ctl-ref-tool-v2.py.txt at 07f2641: both `286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e`, BYTE-IDENTICAL.
- `python3 -I quality/counters/c1-r41-globals-v2.py --repo . --rev 07f2641` → `fixtures=39/39 tool=present verdict=TARGET_MET`, exit 0 (matches `receipts/c1-v2-after-data.txt` at HEAD 9919e16).
- `python3 -I quality/counters/c2-r41-focus-entry-v2.py --repo . --rev 07f2641` → `admitted=1/1 verdict=TARGET_MET`, exit 0 (matches `receipts/c2-v2-after-data.txt`).
- v1 counters at 07f2641 for the disclosed split: C1 → `fixtures=6/24 tool=present verdict=TARGET_MISSED` (clause g:0), exit 1; C2 → `admitted=1/1 verdict=TARGET_MET`, exit 0 (matches `receipts/c1-v1-after-data.txt` / `c2-v1-after-data.txt`).
- Counts at base vs DATA: knowledge entries 58 → 59; registry rows 219 → 226 (S283–S289, +S037 used-by) — used in the Sources line.

## Findings
- No defect found in the drafted content: every numeric claim in the drafts is grounded in a run above or in committed receipts; the v1/v2 split at the data tip is verified exactly as disclosed (v1 C1 6/24, v1 C2 1/1).
- Note for the L1: the after-data receipts live at HEAD `9919e16` ("data measurements, wave w2 spec and dispatch"), not at 07f2641; both drafts cite them as `receipts/*-after-data.txt`.
- Axis-sentence numbers left as placeholders (`<rev>` / A/B, C/D, E/F) per assignment; the L1 re-derives.
- Tooling: nothing installed (host python3 3.14.8 and git used); no pacman, no journal verb, no mutating git/jj.
