# ReMeasureC1 — C1 calibration numbers, falsification attempt

Scope: C1's claim `literal 14/22 -> 15/23` only. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, lane HEAD
`988b858bd6049bc709807534fd725c05264f7e60`. Read-only; no git mutation, no
installs (install: none), no host probes. Round-16/17 `measure.py` executed
hermetically as permitted.

## Verdict

**The attack failed.** All three asserted quantities reproduce exactly at every
named revision, the QUALITY change is strictly append-only, criterion 23 is the
only criterion added, and both independent instruments plus the committed
receipts agree. No counterexample found. Two Low-severity interpretation
caveats follow that qualify what the number means but do not contradict it.

## 1. Literal counts reproduce (primary command)

`git show REV:corpus/QUALITY.md | grep -cE '^[0-9]+\. '` /
`... | grep -cE '^[0-9]+\. .*lessons/'`, plus blob sha256:

| REV | criteria | lesson-cited | QUALITY.md sha256 |
|---|---|---|---|
| `27cd06f` | 22 | 14 | `88bb068106f2c10e261c84c1f4e1eb5d6d35a4696da3220f14d9c3dafa10c00a` |
| `0175f13` | 22 | 14 | `88bb0681…c00a` (identical) |
| `3722ba4` | 23 | 15 | `fedef5c17021823d4fad88c283ce8a870c34b5fe620f172f9c9dd0c04952d53d` |
| `988b858` | 23 | 15 | `fedef5c1…d53d` (identical) |

So `14/22 -> 15/23` is exact. Fraction: `14/22 = 0.636364` (6.3636),
`15/23 = 0.652174` (6.5217), delta `+0.015810` = **+1.5810 pp**.

## 2. Both instruments agree, at every rev

`python3 .ufo/waves/round-17/measure.py REV`:

| REV | c1.criteria | c1.lesson_cited | c1.score |
|---|---|---|---|
| `27cd06f` | 22 | 14 | 6.3636 |
| `0175f13` | 22 | 14 | 6.3636 |
| `3722ba4` | 23 | 15 | 6.5217 |
| `988b858` | 23 | 15 | 6.5217 |

`python3 .ufo/waves/round-16/measure.py REV` (independent prior-round code)
emits the same pair with explicit id sets:

- `27cd06f`: `criteria_total 22`, `lesson_grounded 14`, `ungrounded_ids [1,2,3,4,5,18,19,20]`
- `3722ba4`, `988b858`: `criteria_total 23`, `lesson_grounded 15`, `ungrounded_ids [1,2,3,4,5,18,19,20]`

Note: the earlier-looking failure of the round-16 script was my own pipe merging
its `SyntaxWarning` (stderr, `measure.py:41`) into stdout; with `2>/dev/null` it
emits valid JSON and exits 0. Not a tool defect.

Committed receipts match the live run byte-for-byte:
`.ufo/waves/round-17/evidence/measure-before.json` (blob
`76f1da1f…`, sha256 `54d3cac3…`, rev `27cd06f`, 22/14) and
`measure-c1.json` (blob `19d475db…`, sha256 `85f45237…`, rev `3722ba4`, 23/15),
both committed at HEAD. The instrument on disk equals HEAD's blob
(`sha256 4023124fa40931f630197920e2534f468dc2b1cacfe010826b32032db846466b`,
matching the `4023124f…` prefix quoted in `lessons/round-17.md` M3), so the
before/after pair is same-instrument.

## 3. Append-only and "only criterion 23" — confirmed

- `git diff --numstat 27cd06f 988b858 -- corpus/QUALITY.md` → `15	0`.
- `git diff 3722ba4^ 3722ba4 -- corpus/QUALITY.md` → `15	0` (parent `245fd11`).
- `git log 27cd06f..988b858 -- corpus/QUALITY.md` lists exactly one commit:
  `3722ba4` ("round-17 C1: QUALITY 23 receipt-label criterion, …"). No
  intermediate rewrite is hidden.
- Byte identity of the preserved prefix: `git show 27cd06f:corpus/QUALITY.md`
  sha256 `88bb0681…c00a` equals `git show 988b858:corpus/QUALITY.md | head -n 107`
  sha256 `88bb0681…c00a`. File grows 107 → 122 lines.
- The 15 added lines are: 2 blank, the section heading
  `## Round 17 — receipt-label precision (outside R16-V1)`, and the 12-line
  block of criterion `23.` — exactly one new `^[0-9]+\. ` line
  (`corpus/QUALITY.md:111`).
- No criterion is struck/retired; no counter-evading numbering exists
  (`grep -nE '^[0-9]+[),:]|^\*\*[0-9]+|^[[:space:]]+[0-9]+\. '` over HEAD's
  QUALITY.md returns nothing). Numbering is 1..23, strictly increasing, no
  duplicates, no gaps.
- Criterion 23's cited lessons resolve at that rev:
  `corpus/lessons/round-17.md` exists at `3722ba4` with heading `## Mistakes`
  and an `M1` row; HEAD additionally carries `round-16-verifier-spotcheck.md`.
  The `#mistakes M1` anchor is real, so the numerator's +1 is a resolvable
  citation, not a bare substring.

## 4. Block-citation counter (requested extra measurement)

Definition: a criterion's block = its `^[0-9]+\. ` line plus following lines up
to the next numbered line; counted if any line in the block contains `lessons/`.

| REV | criteria | literal | block-cited | block fraction | block score |
|---|---|---|---|---|---|
| `27cd06f` | 22 | 14 | 17 | 0.772727 | 7.7273 |
| `0175f13` | 22 | 14 | 17 | 0.772727 | 7.7273 |
| `3722ba4` | 23 | 15 | 18 | 0.782609 | 7.8261 |
| `988b858` | 23 | 15 | 18 | 0.782609 | 7.8261 |

Delta is the same `+1` in both conventions, so the claim is not an artifact of
the narrow literal rule. Block-only credits are exactly criteria 18, 19, 20,
whose citations wrap onto continuation lines at HEAD:
`corpus/QUALITY.md:49` (`lessons/round-14.md#mistakes M4`, crit 18),
`:55` (`lessons/round-14.md#mistakes M1`, crit 19),
`:77` (`lessons/round-15.md#mistakes M2`, crit 20).

## 5. Findings

### Low — L1: the literal counter is a floor, not a grounding estimate
`15/23` under-counts by 3. Eight criteria look ungrounded under the literal rule
(`{1,2,3,4,5,18,19,20}`), but three of them (18–20) do cite lessons, on wrapped
lines (`QUALITY.md:49,55,77`). Anyone reading `15/23` as "65% of the rubric is
lesson-grounded" is reading ~`18/23 = 78.3%`. This does not falsify C1 — the
literal rule is the declared one (`SCORECARD.md:841`, and QUALITY 22 explicitly
requires reporting literal and semantic counters separately rather than
silently changing the rubric).

### Low — L2: the increment is structural, and it is declared as such
The numerator and denominator both rise by exactly 1 because the added
criterion is itself lesson-cited, so the fraction rises only because
`14/22 < 1`; the ungrounded set is unchanged before and after
(`[1,2,3,4,5,18,19,20]`, both instruments). The claim therefore supports
"calibration fraction improved by +1.58 pp" but not "previously ungrounded
criteria became grounded" — none did. The pre-registration
(`SCORECARD.md:836-841`) explicitly declared this shape ("append-only
lesson-cited QUALITY criterion"), so this is honest, not a post-hoc dodge.
Counterfactual worth recording: re-wrapping the three existing citations
(18–20) without adding any criterion would have yielded `17/22 = 0.7727`
(`17/23 = 0.7391` had #23 also landed), strictly above the landed `0.6522`.
The round chose the lower-scoring admissible move — evidence against metric
gaming, at the cost of leaving the axis below what its own instrument could
measure.

## 6. Residual risk / gaps

- I did not re-run `label-check.py` or audit its 7 claims, C2's 4/6, or C3's
  selftests; those have separate owners. The `EXPECT_SUMMARY 7/7` text inside
  criterion 23 is therefore unverified here.
- The block counter is my own ~20-line parser over `git show` bytes, not a
  committed instrument; its only definitional freedom is where a block ends
  (next numbered line / EOF), which does not touch any `lessons/` line.
- `measure-before.json` records `rev` in short form (`27cd06f`) while
  `measure-c1.json` records the full sha; both resolve to the claimed commits.
