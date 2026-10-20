# AttackQuality23 — falsify QUALITY criterion 23 and its runnable check

Seat `MadoR17.AttackQuality23` (critic, leaf, lane-dispatched; this is not outside review).
Date 2026-10-20. Target lane HEAD `988b858bd6049bc709807534fd725c05264f7e60`.
Read: `corpus/QUALITY.md` (HEAD; diff `27cd06f..HEAD` = +15/−0), `corpus/lessons/round-17.md`
(M1, M2), `corpus/lessons/round-16.md` erratum (+18/−0), `corpus/lessons/round-16-verifier-spotcheck.md`
(R16-V1 routing, :164-172), `corpus/lessons/round-12.md` M6, `.ufo/waves/round-17/label-check.py`,
`label-claims.json`, `label-fixtures/want-only.json`, `evidence/label-check.txt`, round-16/17
receipts named below, `w1/reports/CriticC1.md`, `w1/reports/RevQuality2122.md`, `SKILL.md:558`,
`SCORECARD.md:820-895`.
Ran (read-only/hermetic): `python3 -I .ufo/waves/round-17/label-check.py [claims]` with the
lane claims and with my claims under `/tmp/aq23/`; `python3 .ufo/waves/round-17/measure.py HEAD`;
the round-16 semantic counter command copied from `evidence/calibration-readings.json`; an
in-memory import of the checker source with two mutations (`/tmp/aq23/mut.py`, never a lane file);
`git show/diff/log/rev-parse`; `grep -c`. No commits, no jj, no package/host commands. Installs: none.

## Verdict

Criterion 23 is **a narrow real discernment gain wrapped in a duplicate clause set, and its
runnable check is insufficient for the criterion as written**. The C1 score move
(14/22 → 15/23) is not itself evidence of discernment: any numbered line carrying `lessons/` on
line 1 produces it. What is genuinely new is one clause — the outcome-side token grammar
(`MADO_<NAME>:` verdict / `finding` / got-side; never want-side or `matched_exit`). The revision and
append/supersede clauses restate criteria 9, 4 and 6. The check can fail (R16-V1 red reproduces),
but its 7/7 acceptance is blind to *why* a red fails, its revision clause is author-transcribed and
opt-in, its token sets are not bound to a row/run, it truncates colon-qualified verdicts, and it
cannot evaluate the lane's own text receipts. Ten counterexamples below are fixable defects; D1
is a tradeoff for the judge.

## Axes

calibration (C1 literal/semantic counters; criterion discernment), quality (corpus claim
precision), honesty/provenance (lesson M1 wording), operability (runnable check as a gate).

## What held (attack failed)

- **It can fail on the motivating case.** Lane claims reproduce byte-identically to
  `evidence/label-check.txt`: `R16-V1-red MISMATCH (receipt outcome ['frozen_error'] lacks
  'snapshot_tampered')`, `LABEL_SUMMARY: 4/7`, `EXPECT_SUMMARY: 7/7`, exit 1. The red is
  receipt-stage, on range 131-132 (CriticC1 CE4 closed).
- **It generalises to unseen real text (greens).** My claims A1 `round-16-verifier-spotcheck.md:74`
  ↔ `action-frozen.json` `frozen_error` → ok; A2 `:80` ↔ `tight-red.json` `denied_executable` → ok.
- **The two declared regressions bite.** A substring receipt check would make
  `want-side-only-mutant` ok; dropping the `measured_commit` stage would make
  `superseded-commit-mutant` ok — either drops EXPECT below 7/7 (by construction of the claims).
- **Erratum discipline.** `round-16.md` erratum is append-only, names the superseded text at
  :131-132 `27cd06f`, keeps the true token `frozen_error`, and fixes CriticC1 CE8 ("already in the
  red `action-selftest.json`"). Its "at current content" holds: `git show HEAD:tools/mado-action-plan.py
  | sha256sum` = `226220ae…ba5aea3` = recut `action_gate_sha256`; `git diff --stat 0175f13 HEAD --
  .ufo/waves/round-16/frozen tools/mado-action-plan.py` is empty (recut measured `0175f13`).
- **No candidate 24 numbered** (CriticC1 CE3 closed). Literal counter at HEAD
  `measure.py HEAD` → `c1 {criteria 23, lesson_cited 15, score 6.5217}`; without 23 → 14/22.
- **No live want-side leak today.** Sweep of 42 parseable `.ufo/waves/round-1*/evidence/*.json`
  receipts: 0 nested `finding` keys under expect/want/fixture/case paths (D10 is latent only).

## Counterexamples

### D1 — the score move is count inflation by construction (calibration; tradeoff, judge-owned)
Same regexes as `measure.py:92-93` on `git show HEAD:corpus/QUALITY.md` copies:
HEAD 15/23; append vacuous `24. Be careful with receipts (lesson: lessons/round-17.md#mistakes M1).`
→ 16/24; prefix `lessons/` onto line 1 of criteria 18, 19, 20 (which already cite lessons on
continuation lines) → 18/23 with zero new content. The fraction is < 1, so every appended
line-1-cited criterion raises it. The +0.1581 rewards appending, not discerning; the discernment
evidence is only the checker's red/green behaviour. Not fixable within the literal rubric.

### D2 — three of criterion 23's four clauses duplicate 4/6/9 (calibration, quality)
- "When the receipt records a `measured_commit`, the sentence's revision must match it" = criterion 9
  ("Bind each audit verdict to a commit or frozen-copy sha"), QUALITY.md:15.
- "corrections append and never relabel" = criterion 4 ("Errata are append-only blocks"), :7.
- "A superseded receipt is named as superseded and keeps its true token" = criterion 6
  ("corrections preserving old and new values"), :12.
- Only the outcome-token grammar is new. The lane's own precedent rejects duplicate provenance
  criteria for receipt-application defects (QUALITY.md:57-61 R13-V2/V3, :65-70 R14-V1: "No duplicate
  provenance criterion … is introduced"). Criterion 23 reverses that precedent while asserting only
  about 9 ("did not bite … because 9 binds the commit, not the token", :118-119). Lane seats
  disagree on that assertion: `w1/reports/CriticC1.md` CE7 says 9 passes R16-V1;
  `w1/reports/RevQuality2122.md:11-19` says 9's in-flight clause bites (a pre-fix `frozen_error` run
  cited as settled tamper evidence). CriticC1's requested 7/9/13/19-vs-23 table was not delivered.
  Reading round-12 M6 ("A verdict from a moving tree or truncated harness output was treated as a
  stable judgment"), RevQuality2122's reading is the stronger one: 9 *could* have bitten; it was
  not applied. "Did not bite" is an application fact, not a semantic gap.

### D3 — lesson M1 justifies the design with a premise false for the cited receipt (honesty, quality)
`corpus/lessons/round-17.md:15` captured-by: "A substring check would also have passed (the red
selftest receipt carries `snapshot_tampered` got-side for other rows)". The R16-V1 sentence cites
`frozen-tampered.json`; `grep -c snapshot_tampered .ufo/waves/round-16/evidence/frozen-tampered.json`
→ **0**. A substring check against the cited receipt would have MISMATCHed. The parenthetical
describes a different receipt (`action-selftest.json`, :`SELFTEST PASS frozen-tampered-plan … got
2/snapshot_tampered`). The lesson that introduces criterion 23 attributes receipt Y's content to
receipt X — the defect class the criterion targets. The want-side mutant is the correct (synthetic)
justification; the R16-V1 claim is not.

### D4 — the check regresses the checker, not the corpus (operability, quality)
`label-claims.json` has 7 hand-declared claims: 3 read real docs (all at `27cd06f`), 4 are
`doc: mutant` with inline `doc_text` — including `recut-green`, so even the round-17 erratum's own
recut sentence is never read from `round-16.md`. Zero claims read HEAD text (no erratum line, no
lesson M1 cell, no spot-check line). The checker has no discovery: a new mislabel in any
document passes unless someone hand-writes a claim for it. "Runnable check" for a corpus-wide
admission rule therefore covers 3 historical sentences.

### D5 — red expectations are stage-agnostic; the doc stage has no red control (operability)
- Mutation M1 (`/tmp/aq23/mut.py`): replace `if base not in window or token not in window:` with
  `if False:` → `LABEL_SUMMARY: 4/7`, `EXPECT_SUMMARY: 7/7`. The doc stage can be deleted unnoticed.
- Mutation M2: `window = text` (whole document instead of the line range) → `EXPECT_SUMMARY: 7/7`.
  The line pin is unverified.
- Claim A5 (copy of `R16-V1-red` with `line 1`): `MISMATCH (doc line 1-1 lacks basename
  frozen-tampered.json, token 'snapshot_tampered')` → counts as **met**. A red control with a broken
  anchor still satisfies 7/7. CriticC1 CE4's "red for the wrong reason" is fixed only in today's
  data, not structurally; the stage is prose in the output, not part of acceptance.

### D6 — tokens are a receipt-wide set, not bound to the row/run the sentence names (quality)
- A6: "the untampered control run in `frozen-tampered-recut.json` returns snapshot_tampered" →
  **ok** (the control run's `MADO_PLAN` is `frozen_match`; the token comes from the tampered run).
- A7: "`action-selftest.json` (measured 9dcf248) shows the frozen denied plan returning
  snapshot_tampered", `measured_commit 9dcf248` → **ok**; that row is
  `SELFTEST FAIL frozen-denied-match: want 0/frozen_match got 2/frozen_error`.
Criterion 23 says "the got-side of a selftest row"; the checker unions all rows/runs. This is the
residue of CriticC1 CE5 (multi-row receipts) and the exact shape of R16-V1 (right token, wrong run).

### D7 — the revision clause is opt-in and transcribed, never read from the sentence (quality, calibration)
Criterion text: "When the receipt records a `measured_commit`, the sentence's revision must match it".
- A8: `doc_text` "(measured 1e31681) records frozen_error", claim `measured_commit "9dcf248"` → **ok**
  (sentence's revision wrong; claim author's transcription right).
- A9: same sentence, `measured_commit` omitted → **ok** although the receipt records `9dcf248`.
- A10: `measured_commit ""` → **ok** (`str(got_mc).startswith("")`, `label-check.py:132`).
The lane's own `R16-V1-red` claim omits `measured_commit`, so the criterion's revision half is not
exercised on the motivating case at all; R16-V1's sentence described corrected content (`1e31681`)
while the receipt is `9dcf248`.

### D8 — co-occurrence cannot tell attribution from quotation/negation (operability)
- A3: `round-16.md:163-164` at HEAD (the erratum quoting the superseded sentence) ↔
  `frozen-tampered.json` `snapshot_tampered` → **MISMATCH**.
- A4: `round-16-verifier-spotcheck.md:165-166` (the outside R16-V1 routing: "cite
  `frozen-tampered.json` as showing `snapshot_tampered`, but …") → **MISMATCH**.
The two correct texts that criterion 23 requires ("named as superseded") fail its check. Harmless
while claims are curated (D4), fatal for any future scan use; the criterion/SKILL row does not say
the check is curated-only.

### D9 — colon-qualified verdicts are truncated (quality; hits the lane's own C2 verdict family)
`OUTCOME_LINE = ^MADO_[A-Z_]+: ([a-z_]+)` and `FINDING_JSON … "([a-z_]+)"` stop at `:`.
`tight-red.json` stdout is `MADO_PLAN: denied_executable:sudo`, `"finding": "denied_executable:sudo"`.
- B1: honest `spotcheck:80` ↔ token `denied_executable:sudo` → **MISMATCH** (outcome set
  `['denied_executable']`).
- B2: "`tight-red.json` exit 1 denied_executable:pacman" with token `denied_executable` → **ok**.
The round-16 12-name classifier's verdicts are all `<class>:<executable>`; the checker cannot
distinguish the wrong executable and false-reds the right one.

### D10 — want-side exclusion is by key name/regex, not by side (quality; latent)
In-memory `outcome_tokens`: `{"stdout":"MADO_PLAN: frozen_error\n","expected":{"finding":"snapshot_tampered"}}`
→ `['frozen_error','snapshot_tampered']`; stdout prose `note: would have got 2/snapshot_tampered`
→ counted. Any nested `finding` key and any `got N/x` substring count as outcome. No current
receipt triggers it (sweep above), so latent.

### D11 — the lane's own C1/C3 receipts are outside the check's scope (operability, quality)
A11: `round-17.md:82-83` ↔ `evidence/tripwire-anchor-r15.txt` → `COULD_NOT_EVALUATE (receipt is not
valid JSON)`, whole run exit 2 — although that receipt's first line `MADO_TRIPWIRE: findings` is
exactly criterion 23's outcome grammar. M1's own receipt `evidence/label-check.txt` and all
`tripwire-*.txt` are likewise unevaluable. Grammar gap too: lesson :83 attributes `host_mutation` to
the anchor receipt, but under 23's definition the outcome token is `findings`; `host_mutation` is a
`counts` key — the criterion does not say whether finding classes count.

### D12 — acceptance pin is a mutable count (operability, minor)
QUALITY.md:121-122 pins "`EXPECT_SUMMARY` must be 7/7"; `SKILL.md:558` says "must equal the claim
count". Adding a real claim (D4's fix) forces editing an admitted criterion's text, or the two pins
diverge.

### D13 — QUALITY 22 semantic counter promised, not yet recorded (calibration; pending)
`SCORECARD.md:882-885` says the semantic block counter is "reported beside the literal one"; no
round-17 value appears in SCORECARD or `lessons/round-17.md` at HEAD (`grep -E '18/23|7\.8261'` → only
other w2 reports). Measured with the round-16 command: `27cd06f 22 14 17 6.3636 7.7273`;
`988b858 23 15 18 6.5217 7.8261`, i.e. semantic 17/22 → 18/23. Must land at close or QUALITY 22 is
breached by the round that cites it.

## Impacted axes

calibration: D1 (inflation tradeoff), D2, D7, D13. quality: D3, D4, D6, D7, D9, D10, D11.
operability (check as gate): D4, D5, D8, D11, D12. honesty/provenance: D3.
No axis is *harmed* in the corpus by 23's presence; the risk is false provenance — "shown able to
fail, 7/7" read as broad label coverage.

## Smallest safe corrections (append-only, fixable this round)

1. **Shrink 23 to its new clause** (D2): keep the outcome-token grammar; replace the revision and
   append/supersede sentences with "revision binding per 9; errata per 4/6". Record in M1 that 9's
   in-flight clause applied but was not applied (RevQuality2122), not that it "did not bite".
2. **Lesson M1 erratum** (D3): "a substring check over `frozen-tampered.json` would have failed (0
   occurrences); a substring check passes the synthetic want-side mutant and any sentence citing the
   red `action-selftest.json`."
3. **Checker** (D5-D10), each with one red/green claim:
   - `expect_stage` (`doc` | `receipt` | `measured_commit`); count a red as met only when the
     stage matches; add one doc-stage red.
   - When the receipt has `measured_commit`, require the claim's `measured_commit` (≥7 hex) and require
     that prefix to appear in the doc window (or an explicit `describes_rev`) — A8/A9/A10 must go red.
   - Optional `row`/`run` selector (selftest case name or `runs[].label`) — A6/A7 must go red.
   - Token regex `[a-z_]+(?::[^\s"/]+)?` for `MADO_` and `finding` — B1 ok, B2 red.
   - Count `finding` only at top level, in `runs[]`, or inside stdout verdict JSON; `got` only on
     `SELFTEST (PASS|FAIL)` lines.
   - Accept text receipts by applying the same line grammar to raw text (D11).
4. **Scope statement** (D4/D8/D12): state in QUALITY 23 and `SKILL.md:558` that the check verifies
   curated claims, not a scan; replace the "7/7" pin with "EXPECT_SUMMARY n/n over the declared
   claims"; add at least the HEAD erratum and M1 recut sentences as real-doc claims.
5. **Record the semantic counter** 17/22 → 18/23 (7.7273 → 7.8261) beside the literal one (D13).

Tradeoff for the judge (not fixable here): even fully corrected, C1's +1 criterion is a
placement-sensitive literal move; its value rests on the token-grammar red/green evidence, not on
15/23.
