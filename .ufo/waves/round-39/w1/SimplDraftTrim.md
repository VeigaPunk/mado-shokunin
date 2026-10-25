# SimplDraftTrim — scoped findings (round-39 w1, 2026-10-25)

Reviewed every assembled draft under `.ufo/waves/round-39/w1/` (report `ScrReportMain/report-main.md`, scorecard `ScrScorecard/scorecard.md`, lesson `ScrLesson/round-39.md`, SHONEN, erratum, SOURCES rows, knowledge entry, amendment, and all executor/scout reports). No file edited; precise edit list + replacements at `.ufo/waves/round-39/w1/SimplDraftTrim/trim-notes.md` (only file written besides this report).

Trims recommended (all preserve evidence pointers and required sections):
1. report-main.md — remove the verbatim duplication of the C1 counting command (line 5, duplicated at line 24 → keep canonical instance in measurement table); replace the placeholder "Stale-lane: [PENDING ...]" line with the grounded state (HEAD==freeze `457d1b12…`; `git status --porcelain` = w1 artifacts + the two expected uncommitted C2 deliverables).
2. scorecard.md — compress the 8-line preamble to 2 lines (keeps the no-invented-numbers caveat); trim the capability cell to a distinctive summary + `registration.md:57-71` pointer (it restated §C2 verbatim).
3. lesson round-39.md — compress the round-intent restatement (registration.md:35-99 pointer); dedupe "Row facts" bullets vs the GATE code fence (quotes/hashes already in fence; keep only page revisions/grounding); CORRECT stale S219 hash — lesson states `9787b53b…` but current worktree `tools/mado-options.py` hashes `cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e` (file uncommitted; `git log --all -- tools/mado-options.py` empty) — re-hash at data tip, keep as draft-time value until bound.
4. config-option-table-r39.md — fill the two provisional `**OBS**` lines with the now-available verbatim located Gate quotes (S218: "You are allowed multiple hl.config() invocations, each one will update just what you pass into it."; S219: "mado-options.py - static resolver of the config-tree option table." @ `tools/mado-options.py:2`).
5. ExecAssimFetches.md and ScrScorecard.md — remove the duplicated "Final answer (≤6 lines)" boilerplate blocks (pure repetition of the report bodies).

Not trimmed (by design): cross-document repetition (each artifact must stand alone), the `[PENDING]` cells for C2/C3/LOG/data-commit (true pending state), the refused-package table and spot-check table in the lesson (continuity/verification records), the three tool-install evidence pointers.

Log: no LOG draft exists yet in w1 (ScrLog seat produced no file) — nothing to trim; final LOG entry should cite the trimmed report/scorecard/lesson.

Verification performed: read-only `git rev-parse HEAD` = `457d1b125932c1e0d797061a2156b917bcd7edaa` (freeze; data commit not landed); `sha256sum tools/mado-options.py` = `cee78d99…`; `gi status --porcelain` = 10 untracked (8 wave artifacts + `quality/counters/c3-r39-options.py` + `tools/mado-options.py`).

Final answer:
1. Trimmed drafts via edit list in trim-notes.md; no draft file edited, no evidence pointer removed.
2. Biggest wins: report-main command dedup + stale-lane placeholder; scorecard preamble/capability; lesson intro + Row-facts dedup.
3. Stale S219 receipt hash found in lesson (9787b53b… vs actual cee78d99…) — must be re-derived at data tip.
4. Knowledge-entry OBS lines remain placeholder until filled with verbatim Gate quotes (now available).
5. Duplicated Final-answer boilerplate in ExecAssimFetches.md/ScrScorecard.md removable; no LOG draft exists yet.
6. No installs, no mutations, no other files written.
