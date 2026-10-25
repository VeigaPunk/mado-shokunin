# RevReportContract — pre-file contract check of the round-39 report draft

Scope: the four draft pieces — `w1/ScrReportMain/report-main.md`, ScrReportFrontier (Sources & frontier + Trend verdicts), `w1/ScrReportShonen/shonen.md`, `w1/ScrErratum/erratum.md`. All commands read-only (git rev-parse/show/log/status; file reads). No other file written. No tool installs.

## Verdict

**NOT READY TO FILE — one blocking contract gap:** the required sections **`## Sources & frontier`** and **`## Trend verdicts`** do not exist anywhere in the wave tree. The ScrReportFrontier seat errored out and produced no output (no `w1/ScrReportFrontier/` dir, no `frontier.md`; its recorded yield is an error: "The requested draft and report files are missing from the assigned seat directory…", `history://ScrReportFrontier`). The other three pieces are contract-sound; their evidence pointers and hashes all verify.

## 1. Required sections, in order

Required order: Work performed / Landed changes / Before → after measurements / Sources & frontier / Trend verdicts / SHONEN.

| Section | Status | Location |
|---|---|---|
| Work performed | PRESENT | `report-main.md:3` |
| Landed changes | PRESENT | `report-main.md:9` |
| Before → after measurements | PRESENT | `report-main.md:20` (order 1→2→3 correct) |
| Sources & frontier | **MISSING** | no file in `.ufo/waves/round-39/**` contains the heading (case-sensitive grep `^## (Sources & frontier|Trend verdicts|…)` over the wave tree: only report-main's three + shonen's SHONEN matched; `glob .ufo/waves/round-39/**/*rontier*` → no files) |
| Trend verdicts | **MISSING** | same evidence |
| SHONEN | PRESENT, last | `shonen.md:1` — exactly one `## SHONEN` heading in the whole draft set, exactly four `[~]` box lines (`shonen.md:2-5`); no other draft piece contains the heading |

report-main.md carries no stray headings: `^#` matches only line 1 (`# Round 39 — fleet report main sections`) plus the three required `##`.

## 2. `[PENDING]` placeholders — 16 occurrences, all in report-main.md

True-pending (data commit not landed; measured: `git rev-parse HEAD` = `457d1b125932c1e0d797061a2156b917bcd7edaa` == freeze; `git status --porcelain` = 10 entries: 8 round-39 wave/orchestration artifacts + `?? quality/counters/c3-r39-options.py` + `?? tools/mado-options.py`):
- L6 C2 measured counter result; L7 C3 measured counter result; L15 "data commit [PENDING]"; L16/L17/L18 data-commit cells; L25 C2 after-cell + measured commit; L26 C3 after-cell + measured commit. (12 occurrences — legitimate pending, must be resolved before filing.)

Fillable now, no reason to stay pending:
- **L28 `Stale-lane: [PENDING — …]`** — grounded fact exists (HEAD == freeze `457d1b1…`; porcelain listing above); `w1/SimplDraftTrim/trim-notes.md:54-57` already drafts the replacement text (its "only w1 wave artifacts plus the two expected uncommitted C2 deliverables" matches the measured 10 entries, modulo the 7 round-level `w1-*` orchestration files).
- **L15-18 `[PENDING: LOG entry]` cells (4)** — a LOG entry draft now exists at `w1/ScrLog/log-entry.md` (records C1 19/19 with commit/receipts, C2/C3 honestly pending); the cells can cite it once appended.
- **L7 "…`w1/ScrKnowledgeEntry.md` [PENDING line]"** — dangling anchor: file exists, line number never filled.

## 3. Evidence pointers — all resolvable

report-main.md:
- `registration.md:35-55 / :57-71 / :73-84` — C1/C2/C3 sections start at lines 35/57/73 ✓ (grep-verified heading lines; C1 Before bullet at 44-47, C2 Before at 67-69, C3 Before ends 82, so `:44-47`, `:68-69`, `:81-82` all land on the registered before-state text) ✓
- `w1/ExecC1After/after-freeze.txt:20` = `MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET` ✓ (read :16-20)
- `receipts/c1-redbefore.txt` — 19 control lines, sole `ok=0` is `c1-duprow` (expected MISSED, observed MET), final `…correct=18/19 verdict=TARGET_MISSED` ✓
- `w1/ExecC1After.md:3` (no tool installs), `:8-9` (tip==freeze, base), `:13-18` (freeze measurement block) ✓
- `w1/ExecOptionsCounter.md:3-17` and `:17` — 18-line file; line 17 is the Risk line ending "No tools installed." ✓
- `w1/ExecGateHealth.md:10` = "No installs. Risks/blockers: none observed…" ✓
- `w1/ScrKnowledgeEntry.md` exists ✓ (anchor pending, see above)

shonen.md:
- `corpus/knowledge/executor-test-sufficiency.md` exists; `MADO-R3-4` is its title/marker ✓
- `corpus/knowledge/config-health-report-r3.md` exists ✓
- `LOG.md` (VER-M3) — VER-M3 found, but the closing entry is labeled "round 4 (training r3)" (`LOG.md:294`: "box-3 CLOSED (VER-M3: config-health report reproduces)"); shonen's "LOG.md round 3 (VER-M3)" matches "training r3" only loosely → wording nit, see findings.
- `corpus/knowledge/province-accuracy-selfaudit.md` — "Round-5 addendum — §8 re-run receipt (M5-1, box-4 close evidence)" at :267 ✓; corroborated by `LOG.md:295` "SHONEN box 4 CLOSED by VER-M4B — PROBATION COMPLETE".

erratum.md: commits verified below; the quoted cross-pair triple is verbatim in f551b70's LOG.md diff (lines "+ frozen counter × frozen manifest = 18/19; frozen counter × landed manifest = 19/19; landed counter × frozen manifest = 18/19; landed pair = / 19/19. The `859d0cf` counter patch was a verdict no-op"). ✓

## 4. Cited hashes — all exist

`git rev-parse --verify <h>^{commit}` (all exit 0):
- `457d1b125932c1e0d797061a2156b917bcd7edaa` — freeze commit; `git show --name-only` confirms its content matches report-main's description: registration.md, `.ufo/waves/round-39/c1/manifest.json`, all 7 `receipts/` files, inherited `round-38/w1/reports/{RevEntryBound,RevRegistry,ScoutS253}.md` ✓
- `08be4eb7fd13358ed29b096e8924005d46ac409c` — base (parent of freeze) ✓
- `c46f868` — "record dispute between RevFrozenClaims and RevCensusBefore…", touches LOG.md ✓ (erratum's "dispute record")
- `f551b70` — "freeze-pair resolution (frozen counter x frozen manifest = 18/19; 859d0cf verdict no-op)…", touches LOG.md + SCORECARD.md ✓
- `859d0cf` — resolves ✓

## Findings by severity

**HIGH (blocking)**
1. `## Sources & frontier` and `## Trend verdicts` absent — ScrReportFrontier seat yielded an error and wrote nothing. The draft cannot satisfy the section contract until that seat is re-run (its input needs exist now: `receipts/census-before.txt`, `w1/ExecCensusAfter/census-after.txt`, `corpus/SOURCES.md`, `w1/ScrSourcesRows/rows.md` are all present and readable).

**MEDIUM**
2. Sixteen `[PENDING]` cells in report-main.md; two are fillable now with measured facts (stale-lane line; LOG-entry cells → `w1/ScrLog/log-entry.md`), twelve are gated on the still-missing data commit (HEAD == freeze; C2 tool + counter untracked).
3. `report-main.md:7` — "`w1/ScrKnowledgeEntry.md` [PENDING line]" is a pointer with no anchor.

**LOW**
4. shonen box 2 says "LOG.md round 3 (VER-M3)"; the LOG entry closing box 3 is labeled "round 4 (training r3)" (`LOG.md:294`). Suggest "training r3 (LOG round-4 entry)".
5. Duplication: the C1 counting command appears verbatim at `report-main.md:5` and again in the L24 table row (already flagged by `SimplDraftTrim/trim-notes.md:6`); not a contract breach.

## Residual risk / verification gaps

- C2/C3 after-values and all data-commit cells are unverifiable until the round-39 data commit lands; the pending cells correctly record targets, not invented numbers (cross-checked against `w1/ScrScorecard/scorecard.md:9-18`, which states the same).
- ScrReportFrontier's error message blames missing draft/report files in its seat dir; the inputs it needs (census receipts, SOURCES.md) exist — its failure looks like a sequencing/assumption issue, not missing data. Not further diagnosable from my seat.
- I did not re-execute any counter or gate (verification is the main agent's job); pointer checks are content-level reads, `lsp` not applicable to markdown-only contract.
