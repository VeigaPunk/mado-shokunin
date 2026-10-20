# AttackSeparable — round 16 causal-independence attack

Seat: `MadoR16.AttackSeparable` (leaf reviewer, read-only). Root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Scope: attack whether C1 (coverage, U7 join), C2 (static action-plan gate), and C3 (literal calibration counter) move independently when the others are removed or altered.

Method and limits:
- Read only: `tools/mado-action-plan.py`, `.ufo/waves/round-16/{safety-policy.json,safety-cases.json,measure.py}`, `corpus/QUALITY.md`, `corpus/SOURCES.md` rows S053–S055, `corpus/knowledge/waybar-observation-boundaries-r16.md`, `.ufo/waves/round-16/adjudication.json`, the round-15 spot-check, and the baseline `corpus/QUALITY.md` at `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea` via one read-only `git show`.
- No gate, `measure.py`, selftest, frozen replay, probe, or package/service operation was executed. Counts below are arithmetic over the bytes read.
- Working-tree bytes were read for the integrated artifacts. L1 must rederive the counts at the committed revision.
- Installs: none. Tools used: read, grep, one read-only `git show`.

## 1. Verdicts

| Claim | Verdict | Basis (anchors) |
|---|---|---|
| C1 unchanged with the C2 gate removed | HOLDS for C2 artifacts. One hard coupling to the older lane gate, not to C2. | `measure.py:74-79` `try_source` swallows missing revision bytes. `measure.py:362-376` safety artifacts are presence/sha only (`scored: False`). `measure.py:415-428` the coverage dict never reads them. Counterexample C-5 below. |
| C2 unchanged with QUALITY 21/22 altered or removed | HOLDS for 22 (no coupling). Criterion 21 is a normative source of C2 scope, and it also feeds C3. | Grep of `mado-action-plan.py`, `safety-policy.json`, `safety-cases.json` for `QUALITY|criterion|22|lesson` returns no hit. C2 has no numeric score in `measure.py`. |
| C3 unchanged with Waybar/U7 removed | HOLDS. | C3 reads only `corpus/QUALITY.md` (`measure.py:338-358`). No Waybar/U7 token appears in QUALITY. The only `module` hit is generic criterion 14 ("module membership"). |
| C3 still improves without 21 | HOLDS, but only because 22 alone is grounded. Removing both 21 and 22 gives no improvement. | Arithmetic in §2. |

## 2. C3 arithmetic (literal rule `^[0-9]+\. .*lessons/` over `^[0-9]+\. `)

Baseline `32c4fda`, criteria 1–20: lesson-grounded on the numbered line = 6–17 (12 items). Fraction 12/20 = 0.6000, score 6.0000.

Working tree, criteria 1–22: grounded = 6–17, plus 21 (`QUALITY.md:82`), plus 22 (`QUALITY.md:102`). Fraction 14/22 = 0.6364, score 6.3636.

Not literal-grounded: 1–5 (no citation); 18, 19, 20. Their citations sit on continuation lines `QUALITY.md:49`, `:55`, `:77`, which the published rule excludes.

| Scenario | Grounded / total | Fraction | vs baseline 0.6000 |
|---|---|---|---|
| As integrated | 14/22 | 0.6364 | improves |
| Without 21 (Waybar irrelevant to C3) | 13/21 | 0.6190 | improves |
| Without 22 | 13/21 | 0.6190 | improves |
| Without 21 and 22 | 12/20 | 0.6000 | no change |
| Rewrap-only 22 so `lessons/` falls on a continuation line | 13/22 | 0.5909 | regresses |
| Rewrap-only 18/19/20 onto first line | 17/22 | 0.7727 | improves, no content change |

## 3. Counterexamples (bounded)

- **C-1 (C3 is line-break-sensitive).** Moving criterion 22's `lessons/` onto a continuation line takes C3 below baseline (0.5909 < 0.6000) with no semantic change. Moving 18/19/20's citations up to their first lines lifts C3 to 0.7727 with no semantic change. The literal counter measures wrapping as much as calibration.

- **C-2 (C3 is monotone in any grounded addition).** Any appended numbered criterion whose first line contains `lessons/` raises the fraction whenever the fraction is below 1. Example, arithmetic only: a 23rd criterion `(lesson: lessons/round-1.md)` gives 15/23 = 0.6522. C3 therefore cannot distinguish calibration from rubric growth. This bears directly on "C3 improves" as evidence.

- **C-3 (criterion 22 is not fully implemented in the instrument).** Criterion 22 (`QUALITY.md:102-106`) requires literal and semantic citation counters reported separately. `measure.py:343-358` emits only the literal counter. A semantic counter (any `lessons/` in a criterion, wrapped or not) gives 17/22 = 0.7727. The gap is in the instrument, not the prose.

- **C-4 (criterion 21 has a double role).** Criterion 21 (`QUALITY.md:82-104`) is both C2's normative boundary and a numerator item for C3. The measurement is causally separate: removing the C2 gate does not change C3. The ledger is not separate: `adjudication.json` accepts "criterion21 first-line citation" in the same accepted line as the C3 addition. [INFERENCE] The first-line placement of 21's citation looks deliberate given the literal rule, which 18–20 do not satisfy. This should be disclosed alongside the C3 claim.

- **C-5 (C1 has a hard dependency on the older lane gate).** `measure.py:325` calls `source('tools/mado-verify.sh')` without `try_source`. Removing that pre-existing file, not the C2 artifacts, raises an uncaught `CalledProcessError` and produces no C1 output. "C1 no gate" must therefore be read as "C2 artifacts removed". Removing the lane gate is a different and fatal case.

- **C-6 (stale path in the C2 case file).** `safety-cases.json:257` and `:274` name `corpus/knowledge/waybar-module-text-boundary-r16.md`. That file does not exist; the U7 note is `corpus/knowledge/waybar-observation-boundaries-r16.md`. The verdict is inert: argv is never resolved, so C2 stays independent of U7. It is still a dangling reference a reader could mistake for a join.

- **C-7 (the pause is hard-wired into the gate code).** `_validate_policy` forces `paused` to `True` and pins the kind dispositions (`mado-action-plan.py:233-235`, return `:276-281`). No policy file can express a lifted pause. An authorized post-lift install plan, the flow criterion 21 points to and criterion 20 governs, is refused `blocked_action_kind:package-install` until the gate code is edited. C2's verdict is therefore fixed to the operator-pause decision by code, not by policy. This is fail-closed by design. L1 must not describe the gate as policy-driven for the lift.

- **C-8 (frozen mode attests inputs, not gate code).** `run_frozen` (`mado-action-plan.py:380-430`) pins `plan.json` and `policy.json` digests only. A coordinated edit of gate code, policy, and `expected.json` passes `frozen_match`. The module docstring (`:65-66`) does not claim gate-code pinning. L1 must not present `frozen_match` as gate integrity.

## 4. Classifier residuals (declared scope vs promised behaviour)

The module docstring (`mado-action-plan.py:4-13`) declares a lexical, kind-label and `argv[0]`-basename classifier. These are declared limits, not broken promises. They matter only where criterion 21's wording ("disguised forbidden executable") is broader than the pinned cases.

- **R-1 whitespace-joined argv[0].** `_basename` (`:311-316`) splits only on `/`. Under `kind: read-source`, `argv: ["sudo pacman -S libinput"]` yields basename `sudo pacman -S libinput`, not in the deny list, so `plan_safe`. The cases (`safety-cases.json:148-198`, `:289-299`) cover only split-argv forms.
- **R-2 kind label is trusted.** `_classify` (`:319-349`) inspects only `argv[0]` for allowed kinds. Under `repo-write`, `argv: ["rm","-rf","corpus"]` yields `plan_safe`. This is the declared label-trust model and is not a promise violation. Do not let the SKILL text imply repo confinement.
- **R-3 same shape under `read-source`.** For example `argv: ["tee","x"]` yields `plan_safe`. Same declared limit as R-2.

## 5. Gaps for L1 (no edits made by this seat)

1. Rederive C3 at the committed revision. Report literal and semantic counters separately, per criterion 22 and C-3.
2. Disclose the criterion-21 double role (C-4) next to any C3 claim.
3. Do not present C2 as independent of the operator pause (C-7). Do not present `frozen_match` as gate-code integrity (C-8).
4. Correct or flag the stale case path (C-6) in the case-file owner's lane; it is not a C2 verdict change.
5. C1 "no gate" holds for C2 artifacts only. Record C-5 as a measurement-script hardening item, not a C2 claim.
