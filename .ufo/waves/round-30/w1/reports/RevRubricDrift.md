# RevRubricDrift — rubric-integrity attack on PRED-C2-r30

Seat: reviewer (report only). Scope: criterion 22 (report literal vs semantic
counters separately; never silently change the rubric), the counter's
`active` denominator, and the r24 `26/35` recorded baseline.

Method: the frozen counter `.ufo/waves/round-30/c2/count.py` was executed
read-only at committed revisions (it reads `git show REV:corpus/QUALITY.md`);
the registered literal grep was re-run independently; a `/tmp` analysis script
importing the counter's own regexes decomposed literal/resolved and
active/all counts (no change to the frozen file). No lane or fleet mutation
beyond this report; git read-only; no installs (python3, git pre-existing);
pacman untouched.

## Direct answers

### 1. Does the `active` denominator retroactively inflate earlier recorded scores if re-run?

**Measured: yes for the literal rule by exactly one line; no for the semantic
rule (it slightly deflates); the counter's large historical uplift comes from
the semantic definition, not the denominator.**

| Revision | Recorded score | Counter literal (all lines) | Literal over active denominator | Counter resolved-active |
|---|---|---|---|---|
| r24 base `8e5d9369` | 23/32 = 7.1875 | 23/32 = 7.1875 | 23/31 = **7.4194** (+0.2319) | 26/31 = **8.3871** (+1.1996) |
| r24 tip `39c5963` | **26/35 = 7.4286** (`SCORECARD.md:1619-1620`) | 26/35 = 7.4286 | 26/34 = **7.6471** (+0.2185) | 29/34 = **8.5294** (+1.1008) |
| r26 `ca13523` | not recorded in this receipt | 28/37 = 7.568 | 28/36 = 7.7778 | 31/36 = 8.6111 |
| base `8f51071` | — | 28/40 = 7.000 | 28/39 = 7.1795 | 31/39 = 7.9487 |
| data `446dc39` | — | 40/52 = 7.692 | 40/40 = 10.0 | 40/40 = 10.0 |

Decomposition (frozen counter's own regexes, plus a `/tmp` replica of its
resolution loop):

- The only excluded line at every revision before the data commit is
  criterion 20 (superseded by criterion 21). Criterion 20 is **non-literal**
  but **resolved** at every revision (`c20_resolved=True`;
  `QUALITY.md:72-80`, citations `lessons/round-15.md#mistakes M2` and
  `lessons/round-15-verifier-spotcheck.md R15-V1/V2`).
- Because it is non-literal, dropping it from the literal denominator raises
  the literal fraction: 26/35 → 26/34 at r24. Applying the round's *stated*
  rule ("superseded lines leave both denominators", `LOG.md:1802-1804`;
  `registration.md:54`) to history therefore restates the recorded
  **7.4286 as 7.6471** with no new evidence.
- Because it is resolved, dropping it from the *semantic* denominator
  slightly **lowers** the semantic fraction: 30/35 = 8.5714 (all lines,
  resolved) vs 29/34 = 8.5294 (active). The +1.10 historical uplift from
  7.4286 to 8.5294 is produced by the semantic definition (continuation-line
  citations counted as resolved), not by the active denominator.
- The records have not executed this rewrite: `SCORECARD.md:1619-1620` keeps
  26/35 and `SCORECARD.md:1827` records round-28's decision that the
  lesson-citation rubric is "NOT re-scored". The defect is a live
  re-scoring capability with a measured delta, not an applied rewrite.

### 2. Would the same rubric at r24's QUALITY.md give a different 26/35?

- **Literal rubric: identical.** Both the frozen counter
  (`literal lines=26/35 fraction=0.7429`) and
  `grep -cE '^[0-9]+\. .*lessons/'` over `grep -cE '^[0-9]+\. '` at
  `39c5963` give 26/35. No literal drift.
- **Counter's semantic rubric: different.** 29/34 = 0.8529 (`active=34
  resolved_active=29`). ```
  python3 -I .ufo/waves/round-30/c2/count.py 39c5963
  METRIC literal lines=26/35 fraction=0.7429
  METRIC superseded=[20]
  METRIC active=34 resolved_active=29 fraction=0.8529
  PRED-C2-r30 verdict=TARGET_MISSED  (exit 1)
  ```
- **Round's stated exclusion rule applied to the literal rule: different.**
  26/34 = 0.7647.

So "same rubric ⇒ different 26/35" is true for the semantic reading and for
the record's stated both-denominator rule; false for the literal metric.

### 3. Does the round introduce a rubric-change defect disguised as a measurement?

**No disguise: the rubric change is declared in every layer.** The
registration prints both values at base and target (`registration.md:47-61`),
`QUALITY.md` carries an explicit "Grounding repair (round 30 …)" block with
both readings (`QUALITY.md:338-346`), the receipts print `METRIC literal` and
`METRIC active` side by side, and `SCORECARD.md:1915` repeats both. That
satisfies criterion 22's reporting clause in form. `QUALITY.md` changed by
**22 insertions and 0 deletions** base→data; no old criterion was rewritten,
so no silent in-place rubric edit occurred.

**But the pass condition is achieved by rewriting the population being
measured, in the measured commit, plus one self-referential citation.** The
40/40 saturation is not a measurement of the pre-existing criteria:

- 12 criteria leave the denominator in the same data commit that is scored
  (11 superseded by rows 41-51; #20 by criterion 21 since round 16). The
  eight base-unresolved criteria `{1..5, 38..40}` are not grounded in place;
  they are superseded and replaced.
- 5 of the 40 "resolved" active criteria (41-45, `QUALITY.md:347-351`) resolve
  only through `lessons/round-30.md#mistakes M30-1` — a lesson row created in
  the same data commit whose content is *"criteria 1–5 carry no lesson
  citation"* and whose `captured-by` column is `none`
  (`corpus/lessons/round-30.md:13`). Row 41 itself states: "The
  probation-seed bar's lesson is not a corpus `lessons/` file". The counter
  counts the absence record as the grounding citation.
- The literal fraction's move 28/40 → 40/52 is the ratio of all lines; the 8
  originally ungrounded lines remain ungrounded in the record and the 12 new
  lines are what raise the numerator. It is an honest ratio, but not a
  fixed-population repair.

**The comparable score depends on the rubric.** On the recorded literal rule
the move is 0.7000 → 0.7692; only on the newly introduced semantic rule is it
0.7949 → 1.0000. If the canonical judge scores the calibration axis at 1.0
from `resolved-active 40/40`, the literal value 0.7692 must be carried beside
it; the claim is a rubric extension, not a saturation of the recorded rule.

## Findings by severity

### F1 — Medium — the record's "superseded leaves both denominators" statement is false for the literal metric

`LOG.md:1802-1804` ("Superseded lines leave both denominators (criterion
21→20 precedent)") and `registration.md:54` ("[20] counted out of both
fractions") describe a rule the frozen counter does not implement for the
literal metric: `count.py:168-169` computes `total = len(crits)` and
`lit_n = sum(c["lit"] for c in crits)` over **all** criterion lines;
`count.py:170` builds the active set separately. Verified values:

- base: literal all-lines 28/40 = 0.7000; superseded-excluded 28/39 = 0.7179.
- data: literal all-lines **40/52 = 0.7692**; the 12 superseded lines are in
  that denominator; excluding them gives 40/40 = 1.0.

Consequence: a re-derivation from the record does not reproduce the printed
numbers (0.7000 vs 0.7179; 0.7692 vs 1.0), and the base literal floor
`>= 0.70` (`count.py:189`) sits exactly at 0.7000 under the implemented rule
but has headroom 0.7179 under the stated one. No predicate flip (both pass),
but the record and the code disagree about the rubric. `ScoutAxisScores.md`
repeats the claim and should be corrected in closure.

### F2 — Medium — criterion 20 is conditionally superseded, not retired; the "criterion 21→20 precedent" is mis-cited

`QUALITY.md:82-94` (criterion 21) supersedes only
"criterion 20's prospective install route **while the operator's host-wide
pause holds**" and then states (lines 93-94): "After explicit operator lift,
criterion 20's complete real-plan/installed-name comparison still applies". Criterion 20 is
therefore dormant under the pause, not retired. The counter
(`SUPER_RE` at `count.py:44`; supersession loop at `count.py:102-107`)
matches the number and excludes the criterion unconditionally, with no scope
or condition check, and its docstring nevertheless asserts "full supersedes
only; criterion 21 supersedes criterion 20 by its own text".

Consequence: a still-binding criterion is removed from the `active`
denominator at every revision; this is the one-line source of the literal
retroactive inflation in answer 1. The base semantic value would be
32/40 = 0.8000 if #20 were counted (31/39 = 0.7949 otherwise) — the verdict
at data is unaffected (41/41 either way), but the historical denominator is
misstated.

### F3 — Medium — five active criteria are self-referentially "resolved" by the audit row that records their lack of grounding

Rows 41-45 (`QUALITY.md:347-351`) cite only
`lessons/round-30.md#mistakes M30-1` (plus `MINT.md`, which the counter
ignores). `M30-1` (`corpus/lessons/round-30.md:13`) is the round's own audit
finding — "criteria 1–5 carry no lesson citation" — created in the same data
commit, with `captured-by: none`. The counter's `resolved` test
(`count.py:138-160`) checks only file existence, an anchor substring and M-id
substring presence; it cannot distinguish a grounding lesson from a citation
to the absence record. 5/40 = 12.5% of the claimed saturation is of this
form. The claim's word "lesson-grounded" is therefore broader than what the
counter certifies, although the row text discloses the circularity ("The
probation-seed bar's lesson is not a corpus `lessons/` file").

Distinct from `CritPredicates` B1/B2: those demonstrate the counter is
cheatable with an unrelated lesson or a single line; this is what the actual
committed data does.

### F4 — Low — supersession count/attribution error in the registration

`registration.md:61`: "12 lines superseded by rows 41–51". Rows 41-51 are 11
lines and supersede 11 criteria (`1-5,18,19,32,38,39,40`). The 12th
superseded line, #20, is superseded by criterion 21, as the same registration
notes at line 54. Total 12 is right; the attribution is wrong.

### F5 — Low, latent — frozen-text vs implementation gaps in the counter

- **Order not enforced.** The docstring/registration say "a **later**
  criterion line says `Supersedes criterion N`"; `count.py:102-107` scans
  every criterion with no position check. A synthetic "Supersedes criterion
  50" inside criterion 2 would exclude 50 (verified by the parser shape;
  no committed file exercises it).
- **Combined ranges truncate.** `expand_super` on the `SUPER_RE` match for
  `"Supersedes criteria 1-5 and 38-40"` returns `[1,2,3,4,5,38]` — the
  trailing `-40` is silently dropped (verified against the frozen
  `SUPER_RE`/`expand_super`). Not used by the committed rows (each names one
  number), but the registration advertises this form.
- **Indent asymmetry.** `CRIT_RE` (`count.py:39`) accepts leading whitespace,
  `LIT_RE` (`count.py:40`) does not. No indented numbered lines exist at base,
  data, or r24 (grep verified), so nil effect today.

### F6 — Informational — axis selection is robust; criterion 22's first clause is satisfied

Calibration is the lowest axis under both the recorded literal rule
(0.7000 < coverage 0.9535/operability 1.0) and the new semantic rule
(0.7949 < 0.9535/1.0). The lowest-axis choice is not a defect. Criterion 22's
"re-derive every active, non-retired axis under its recorded counting rule"
is satisfied for selection (literal 28/40 is the recorded rule at base), and
its "report literal versus semantic separately" clause is satisfied in form.
The drift is in the *claim target*, which moves the pass predicate to the new
rule without re-scoring the recorded axis.

## Verified honest (not findings)

- Counter frozen: `git diff 451e8b3..92d3c86 -- .ufo/waves/round-30/c2/count.py`
  is empty; controls (451e8b3) precede data (446dc39).
- Base receipt reproduces exactly (exit 1); data receipt reproduces (exit 0);
  r24 `26/35` reproduces with the registered grep.
- `QUALITY.md` base→data diff is 22 insertions, 0 deletions; append-only
  correction policy honored; no old criterion rewritten.
- No duplicate criterion numbers at data; no indented numbered lists at base,
  data or r24.
- Rows 49-51 cite genuine round-28 `M28-1/2/3`; rows 46-48 are disclosed
  citation relocations; criterion 52 is new and resolves.
- Criterion 22 itself is unchanged at data (`QUALITY.md:107`) and resolves.

## Residual risk

- **Unbounded supersession.** The counter cannot distinguish the committed
  11-row replacement from a single line that supersedes the population
  (`CritPredicates` B2 proves the class). The `active` denominator is
  author-controlled in the same commit that is scored.
- **History re-scoring.** Any later re-derivation with this counter restates
  r24/r26/r28/r29 upward (semantic: +1.0 to +1.2 points) or slightly upward
  (literal-active: +0.18 to +0.23). Unless each use re-declares the rubric,
  the SCORECARD calibration series is no longer comparable across rounds.
- **Dependence on `M30-1`.** If the audit row is corrected or removed, five
  active criteria become unresolved and the data saturation flips; its
  `captured-by` is `none`.
- **Population drift.** Appending grounded rows raises the literal fraction
  without repairing the old ungrounded lines; the literal metric is not
  fixed-population.

## Verification gaps

- No scratch-clone mutation tests (owned by `CritPredicates`); the retroactive
  numbers come from read-only runs at committed revisions.
- I read `M30-1`/`M30-2` and rows 41-52 in full; I did not read all 40 cited
  lesson anchors. The counter's anchor check is substring-level and not
  section-scoped by design, so "resolves" is structural.
- C1/C3 are other seats' scope. No tools installed.

## Reproduce

```
python3 -I .ufo/waves/round-30/c2/count.py 8e5d9369   # literal 23/32, active 26/31
python3 -I .ufo/waves/round-30/c2/count.py 39c5963   # literal 26/35, active 29/34, exit 1
python3 -I .ufo/waves/round-30/c2/count.py ca13523   # literal 28/37, active 31/36
python3 -I .ufo/waves/round-30/c2/count.py 8f51071   # literal 28/40, active 31/39, exit 1
python3 -I .ufo/waves/round-30/c2/count.py 446dc39   # literal 40/52, active 40/40, exit 0
git show 39c5963:corpus/QUALITY.md | grep -cE '^[0-9]+\. .*lessons/'   # 26
git show 39c5963:corpus/QUALITY.md | grep -cE '^[0-9]+\. '             # 35
git diff 8f51071 446dc39 -- corpus/QUALITY.md                          # 22 insertions, 0 deletions
git diff 451e8b3 92d3c86 -- .ufo/waves/round-30/c2/count.py            # empty (frozen)
```
