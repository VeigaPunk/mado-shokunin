# SimplDraftTrim — trim notes, round-39 w1 (2026-10-25)

Scope: the assembled w1 drafts (report / scorecard / lesson / seat reports) — filler, dead
prose, repeated receipts, placeholder text. Method: full read of every draft in
`.ufo/waves/round-39/w1/`; dedup judged *within* a document only (cross-document repetition
is inherent to the artifact set — report, scorecard, lesson and SOURCES rows are separate
required deliverables, each must stand alone with its own evidence pointers). No file was
edited; this note is the precise edit list. Verified against working tree / read-only git
(`git rev-parse HEAD` = `457d1b125932c1e0d797061a2156b917bcd7edaa` freeze; data commit not
landed).

## Inventory reviewed

- `ScrReportMain/report-main.md` (report) — 30 lines
- `ScrScorecard/scorecard.md` (scorecard draft) — ~76 lines
- `ScrLesson/round-39.md` (lesson) — ~102 lines
- `ScrReportShonen/shonen.md` (SHONEN section) — 4 rows, compact, no trims
- `ScrErratum/erratum.md`, `ScrErratum.md` — compact; no trims
- `ScrSourcesRows/rows.md`, `ScrSourcesRows.md` — data-dense; no trims
- `ScrKnowledgeEntry/config-option-table-r39.md` — one placeholder-gap (fix below)
- `ScrDispatcherAmendment/dispatcher-amendment-section.md` — dense; no trims
- Executor/scout reports: `ExecC1After.md`, `ExecC1ManifestDiff.md`, `ExecOptionsCounter.md`,
  `ExecGateHealth.md`, `ExecEventqSnapshot.md`, `ExecCensusAfter.md`, `ExecSelftestAfter.md`,
  `ExecAssimFetches.md`, `ExecAssimIdGuard.md`, `ExecQuarantineSlice.md`, `SctHostTree/manifest.sha256`
- `ScrQualityCriterion.md` — no trims

Log: NO draft LOG file exists in w1 yet (`ScrLog` seat registered, no output produced;
report-main's LOG cells are `[PENDING: LOG entry]`). Nothing to trim; when written, the LOG
entry should cite the trimmed report/scorecard/lesson instead of re-stating them.

---

## 1. `ScrReportMain/report-main.md` — 2 edits

### 1a. REMOVE repeated counting command (line 5)
The full C1 counting command appears verbatim twice: line 5 (Work performed) and line 24
(Before → after table). Keep the canonical instance in the measurement table; shrink the
bullet to a pointer.

Old (line 5):
```
- **C1 — calibration:** re-registered the repaired discrimination pair against the re-frozen manifest and unchanged counters; target is 19/19 at freeze. Evidence: `.ufo/waves/round-39/registration.md:35-55`; `python3 -I quality/check-r38-discrimination.py --c1 quality/counters/c1-r38-event-ground.py --c2 quality/counters/c2-r38-eventq.py --manifest .ufo/waves/round-39/c1/manifest.json --rev 457d1b125932c1e0d797061a2156b917bcd7edaa` — `.ufo/waves/round-39/w1/ExecC1After/after-freeze.txt:20`.
```
New:
```
- **C1 — calibration:** re-registered the repaired discrimination pair against the re-frozen manifest and unchanged counters; target is 19/19 at freeze. Evidence: `.ufo/waves/round-39/registration.md:35-55`; measured with `quality/check-r38-discrimination.py` (+ c1/c2 counters, c1 manifest) at freeze rev — `.ufo/waves/round-39/w1/ExecC1After/after-freeze.txt:20` (full counting command in the table below / registration.md:42-43).
```

### 1b. REPLACE placeholder "Stale-lane" line (line 28)
Old:
```
Stale-lane: [PENDING — lane status/state evidence not present in the reviewed receipts].
```
New (grounded, no fabrication):
```
Stale-lane: none observed — HEAD == freeze commit `457d1b125932c1e0d797061a2156b917bcd7edaa`; `git status --porcelain` shows only w1 wave artifacts plus the two expected uncommitted C2 deliverables (`tools/mado-options.py`, `quality/counters/c3-r39-options.py`) pending the data commit.
```

No other changes: the `[PENDING]` cells (C2/C3 after, LOG entries, data commit) are true
pending state, not filler; the three tool-install evidence pointers (line 30) are each
independent evidence and stay.

---

## 2. `ScrScorecard/scorecard.md` — 2 edits

### 2a. COMPRESS preamble (lines 3-10)
Old (8 lines):
```
Round intent frozen in `.ufo/waves/round-39/registration.md`: three claims — C1
(re-registration of the repaired round-38 discrimination pair), C2 (config-option
ownership resolver, capability acquisition), C3 (sourced config-option knowledge
admission). This draft is written during wave w1 at the freeze commit
`457d1b125932c1e0d797061a2156b917bcd7edaa` (HEAD, "round-39: freeze registration +
base receipts + inherited r38 seat reports"; tip == freeze commit at write time).
The round-39 data commit has **not landed** at write time: C2/C3 after-cells are
pending measurement, no numbers are invented below.
```
New:
```
Round intent frozen in `.ufo/waves/round-39/registration.md`: C1 re-registration of the repaired round-38 discrimination pair, C2 config-option ownership resolver (capability acquisition), C3 sourced config-option knowledge admission. Drafted at freeze commit `457d1b125932c1e0d797061a2156b917bcd7edaa` (HEAD; tip == freeze at write time): the round-39 data commit has not landed, so C2/C3 after-cells are pending and no numbers are invented below.
```
(keeps the honesty caveat; drops the authorial staging detail)

### 2b. TRIM capability description (line 24)
The capability cell restates registration §C2 nearly verbatim. Keep the distinctive
vocabulary, point the spec away. Old cell body:
```
static resolver of the config-tree option table (all non-bind/non-animation/non-workspace/non-rule `key = value` settings) through the Hyprland source graph, with last-declarer ownership resolution and an optional `--getoption <json>` live-value merge reproducing the divergence vocabulary (`agreement` / `agreement*` / `live-default` / `mismatch` / `config-only`); strict regular-file policy; no compositor, socket or network; Python stdlib only
```
New:
```
static resolver of the config-tree option table with last-declarer ownership resolution and an optional `--getoption <json>` live-value merge reproducing the divergence vocabulary (`agreement` / `agreement*` / `live-default` / `mismatch` / `config-only`); strict regular-file policy, stdlib only — full spec registration.md:57-71
```
Everything else in the scorecard (claims table before/after cells, harm-watch block,
records-update, planned round-40) carries unique evidence and stays.

---

## 3. `ScrLesson/round-39.md` — 3 edits

### 3a. COMPRESS round-intent restatement (lines 3-12)
Old:
```
Round intent (frozen in `.ufo/waves/round-39/registration.md`, freeze commit
`457d1b125932c1e0d797061a2156b917bcd7edaa`, base `08be4eb7fd13358ed29b096e8924005d46ac409c`):
three claims — **C1** (re-registration of the repaired round-38 discrimination
pair: re-frozen manifest `.ufo/waves/round-39/c1/manifest.json` + unchanged
counters `c1-r38-event-ground.py`/`c2-r38-eventq.py` must score
`controls=19 correct=19/19 verdict=TARGET_MET` at the freeze commit), **C2**
(operability/capability acquisition: `tools/mado-options.py` + counter
`quality/counters/c3-r39-options.py`), **C3** (coverage/sourced:
`corpus/knowledge/config-option-table-r39.md` + SOURCES rows S218/S219 + counter
`quality/counters/c4-r39-options-entry.py`).
```
New:
```
Round intent frozen in `.ufo/waves/round-39/registration.md:35-99` (freeze `457d1b125932c1e0d797061a2156b917bcd7edaa`, base `08be4eb…`): C1 re-registration (re-frozen manifest + unchanged counters must score `controls=19 correct=19/19 verdict=TARGET_MET` at freeze), C2 options tool `tools/mado-options.py` + counter `c3-r39-options.py`, C3 sourced entry `config-option-table-r39.md` + S218/S219 + counter `c4-r39-options-entry.py`.
```

### 3b. DEDUPE "Row facts" vs Gate fence (lines 38-55)
The GATE code fence (lines 33-36) already carries each row's receipt+sha256+quote (required
form). The "Row facts" bullets repeat the same quotes/hashes/URLs; keep only the facts the
fence lacks:
- S218 bullet: drop the repeated quote sentence (`Grounds the last-declarer option-syntax claim: repeated hl.config() invocations merge, each updating only what is passed.` already states the grounding; the quote itself is in the fence). Keep URL, open date, page revision, anchor.
- S219 bullet: drop the repeated hash/quote (`worktree sha256 at draft time ...`; quote is in fence). Keep own-work/no-URL note, quote location `tools/mado-options.py:2`.
- S220 bullet: drop the repeated quote; keep URL, open date, page revision, cited-by.

### 3c. CORRECT stale S219 hash (Gate line 34 + spot-check row)
`GATE S219` states `sha256=9787b53b298216aee93ec1193814e2972d9fef9125656ce9ed0bd03ed7fbcf59`
for `tools/mado-options.py`. The current worktree bytes hash `cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e`
(verified `sha256sum tools/mado-options.py`; file uncommitted — `git log --all -- tools/mado-options.py` empty; HEAD still freeze `457d1b12…`). The stated hash does not match any present byte set and must not be presented as bound. Fix: replace the draft hash with the current worktree hash and keep the existing note "data commit must bind the same bytes (re-hash at data tip)". Same correction applies to the spot-check table's S219 row (`9787b53b…cf59` → `cee78d99…` + note).

No other lesson changes: the refused-package table (continuity record) and the spot-check
table (verification evidence) are required and stay.

---

## 4. `ScrKnowledgeEntry/config-option-table-r39.md` — fill placeholder OBS lines (42-45)

The two `**OBS**` lines are provisional citations ("consult its located Gate quote and bound
receipt") — per ScrKnowledgeEntry's own finding they do not meet quote-grounding. The quotes
now exist in the lesson Gate; replace with verbatim located quotes:
- OBS S218 → `"You are allowed multiple hl.config() invocations, each one will update just what you pass into it."` (§Syntax, Variables page 0.56.0; receipt `.ufo/waves/round-39/w1/ExecAssimFetches/S218.bin` sha256 `400d18195…2801`).
- OBS S219 → `"mado-options.py - static resolver of the config-tree option table."` (`tools/mado-options.py:2`; receipt = tool bytes at data tip, re-hashed at landing).

---

## 5. Template residue — remove duplicated "Final answer (≤6 lines)" blocks

- `ExecAssimFetches.md` lines 76-86: the "Final answer" block repeats the body's six facts verbatim. Remove the section (dead prose; no information lost).
- `ScrScorecard.md` lines 57-64: "Final answer (≤6 lines)" repeats the Measured-facts section. Remove the section.
(These are subagent-report boilerplate; if the harness requires a final-answer trailer, keep one line citing the report file instead of restating facts.)

---

## Preserved contract

- Every evidence pointer in the drafts survives: receipts (`c1-redbefore.txt`, `selftest-base.txt`, `axis-base.txt`, `nav-base.txt`, `census-before.txt`), gate outputs, `ExecC1After/*`, `ExecEventqSnapshot/*`, `ExecCensusAfter/census-after.txt`, `S218.bin`/`S220.bin` hashes, S018/S220 pins, and all `registration.md` section ranges.
- Required sections are untouched in substance: report Work performed/Landed changes/Before→after, scorecard claims/capabilities/saturation/harm-watch/planned, lesson Gate/Mistakes/assimilation/spot-check, sources rows, knowledge entry provenance trio, amendment Gate/UNK clauses.
- No additions change meaning; all replacements are compressions or grounded fill-ins.
- Nothing else was written: only this file (trim-notes.md) and the seat report `SimplDraftTrim.md`.
