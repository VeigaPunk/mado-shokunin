# AttackPriorRubric — round 16 measure.py U1–U6 semantic comparison

Scope: compare `.ufo/waves/round-15/measure.py` (committed at `5f13870`) with `.ufo/waves/round-16/measure.py` (working copy, untracked) for silent changes to U1–U6 counting, inverse, reserved-pair, and denominator semantics. Source reading and `diff` only. `measure.py`, gates, tests and probes were not executed. No installs. No commits. No edits outside this report.

## Verdict

No silent broader inverse or denominator change to U1–U6 was found. Every U1–U6 branch, the generic `covered` join, the `10 * n / 7` denominator, the registry parse and the navigation check are logically unchanged. Two binding gaps are real (F2, F3); they concern revision binding and do not change any count.

## Method and anchors

`diff -u` of the two files was read in full (artifact `artifact://21000`). The hunks are: header and docstring (1–48), new `try_source` helper (71–78), new `u7_facets` (168–189), registry comment (196–205), `u7_candidates` init (216–217), new U7 branch (277–295), U7 `joined` entry (307–310), a removed blank line before the SHA256 block (324), C3 calibration block (328–358), safety block (360–376), additive result keys (385–390, 403–412, 425–427, 430–431), and a rewritten tail comment (434–435).

Unchanged between r15 and r16, byte for byte in logic:

| Element | r15 anchor | r16 anchor |
|---|---|---|
| `body_facets` (U5 sections) | 70–102 | 93–125 |
| `level2_sections` | 105–121 | 128–144 |
| `u6_facets` | 124–142 | 147–165 |
| U4 facets and gate | 181–191 | 234–244 |
| U5 branch, `inverse`, reserved `S047/S048` | 192–204 | 245–257 |
| U6 branch, `inverse`, reserved `S051/S052` (`U6_SOURCES`) | 205–223 | 258–276 |
| Generic `covered` join (`mined and any A/B`) | 224–235 | 296–311 |
| Denominator `round(10*len(covered)/7, 4)` | 282 | 418 |
| `used_by` and `mined_ab` | 59–67 | 82–90 |
| Registry parse (`len(cells)==13`) | 147–150 | 194–197 |
| Navigation (`nav`) | 241–247 | 317–323 |

The U5 `inverse` expression is identical in both files (`all(s in cited for s, row in registry.items() if row[8]=='mined' and used_by(row, path))`). U6 uses the same expression. U7 copies it (r16 284–285), which is the only new inverse logic and it applies only to U7 notes.

Corpus inputs were checked so that identical code is also identical in effect:

- `git diff --stat 5f13870 -- corpus/knowledge` is empty. The only new knowledge file is untracked `waybar-observation-boundaries-r16.md`, which covers U7.
- `corpus/SOURCES.md`, `corpus/README.md` and `corpus/QUALITY.md` have insertions only, no deletions (54 insertions total). Existing rows and criteria 1–20 are unchanged.
- The 13-cell registry parse yields 52 rows at `5f13870` and 55 in the working tree. Mined rows go 40 → 43 (S053–S055 added). No malformed S-rows exist.
- S053 and S054 `used-by` name only `corpus/knowledge/waybar-observation-boundaries-r16.md`. S055 `used-by` names only `corpus/lessons/round-16.md`. None of these changes the `inverse` result for an existing U1–U6 knowledge note.

Therefore r16 U1–U6 counting over the current corpus should reproduce r15 exactly: 6/7 with U1–U6 covered, 8.5714. [INFERENCE — derived from code identity and input identity; not executed.] The only new fields are additive JSON keys.

## Findings

### F1 — none (no U1–U6 semantic drift)
As above. The U1–U6 branches have no changed predicate, reserved pair, facet, denominator or `covered` condition. The diff's only edits to the U1–U6 path are comment and docstring rewording (r16 lines 19–24 and 199–204) and the new `try_source` helper, which is used only for optional artifacts and QUALITY.md. All U1–U6 inputs still use strict `source()`.

### F2 — medium (revision binding): round-16 `measure.py` is untracked
`git status --porcelain` shows `?? .ufo/waves/round-16/`. `git ls-files .ufo/waves/round-16/measure.py` is empty. The r16 counter therefore has no committed revision. Its own docstring says it is revision-bound (r16 lines 26–37), but the code that does the binding is not in any commit.

By contrast, `.ufo/waves/round-15/measure.py` at `5f13870` is byte-identical to its working copy (`diff -q` silent). Citing an r15-vs-r16 comparison requires committing the r16 probe first. Commit is L1's action; I did not commit.

### F3 — medium (revision binding): round-16 safety artifacts are untracked
`tools/mado-action-plan.py`, `.ufo/waves/round-16/safety-policy.json` and `.ufo/waves/round-16/safety-cases.json` are all untracked (`git ls-files` empty). The probe reads them only with `git show <rev>:<path>` (`try_source`, r16 74–79 and 360–376). At any committed revision that does not yet include them, the probe will report `present: false` and `sha256: null`.

The safety observation is therefore only meaningful after the artifacts are committed. The probe's "presence/bytes only" claim is accurate as written, but its outcome depends entirely on commit order.

Related observation, not a counter defect: `tools/__pycache__/mado-action-plan.cpython-314.pyc` exists (mtime 05:46:56), and it predates the last edit of `tools/mado-action-plan.py` (05:52:57). A `.pyc` for this tool implies the file was byte-compiled or imported at least once in this lane. Importing runs top-level code. I did not determine which process produced it. L1 should confirm that it was not an import or execution of the gate tool, and should remove the untracked `__pycache__` before commit.

### F4 — low (calibration semantics, not U1–U6)
- Literal C3 numbers, from `grep` on the working copy and on `5f13870`:
  - `5f13870`: numbered lines 20, same-line `lessons/` 12 (criteria 6–17), fraction 0.6, score 6.0.
  - Working copy: numbered lines 22, same-line `lessons/` 14 (criteria 6–17, 21, 22), fraction 0.6364, score 6.3636.
  - Ungrounded literal ids: {1, 2, 3, 4, 5, 18, 19, 20}. Criteria 18–20 cite lessons only on continuation lines (QUALITY lines 49, 55, 76–77), which the literal rule correctly excludes.
- The improvement 0.6 → 0.6364 is arithmetic from two new grounded criteria (21, 22). Existing criteria 1–20 are unchanged. It is not evidence that the existing criteria improved. Criterion 22 requires literal and semantic counters to be reported separately; the report should say so.
- The denominator regex `^[0-9]+\. ` runs over the whole of `QUALITY.md`, not over a criterion section. Today every match is a criterion, so there is no false inflation. A future numbered prose line at column 0 would silently raise the denominator.

### F5 — low (additive output keys)
Whole-JSON comparisons will show a diff even though no r15 field changed value. New keys: `measure_inputs.{safety_artifacts,safety_executed,quality}`, `source_registry.round16_required`, `coverage.{u7_present,u7_facets,u7_candidates}`, top-level `safety_artifacts` and `calibration`. Field-level r15 consumers are unaffected.

### F6 — informational (declared-policy limit; pre-existing, not introduced in r16)
S055 is `mined`, tier A, `own-work`. The generic U1–U4 join (`covered`, r16 296–311) credits any mined A/B row, with no reserved-pair requirement. The r16 claim that "own-work receipts cannot credit a documented-route item" is enforced only for U7, through `U7_SOURCES` (r16 203–206) and the reserved-pair gate. It is not enforced for U1–U4, where existing own-work rows (S019, S041, S044) are already credited.

Bounded hypothetical [INFERENCE, not present today]: a knowledge note with `covers: U1`, `source:` citing S055, and the note's path added to S055 `used-by`, would pass the generic `covered` join for U1. The corpus does not do this now, and the probe would not block it. This is a declared-policy classifier limit, not a counter defect.

## Residual risk
- The r16 U1–U6 counts are inferred identical to r15, not measured. A single probe run against the committed revision will confirm or refute this (L1 action).
- Until F2 and F3 are committed, the r16 probe's binding and safety observations cannot be reproduced from a revision.
- F6 is a policy-scope gap for future own-work rows; it has no present counterexample.

## Verification gaps
- `measure.py` was not executed. Output equality is by code and input identity only.
- `tools/mado-action-plan.py` and the safety JSON were not read for semantics. Only their presence and git tracking state were checked. They are outside this assignment.
- The U7 note's own header, facets and reciprocal rows were not checked. Other seats own that scope.
- Installs: none. Tooling: none. Commits: none. Edits outside this report: none.
