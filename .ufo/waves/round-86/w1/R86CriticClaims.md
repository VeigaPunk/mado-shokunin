# R86CriticClaims — falsification of the two frozen round-86 predicates

Seat: leaf critic. Scope: read and run the frozen instruments; report defects with command + output.
Nothing here edits an instrument, a control set, the declaration or another seat's report.

Both frozen predicates were **re-executed**, not read:

| run | command target | result | wall |
|---|---|---|---|
| C1 @ freeze | `--rev 237ecf4e…` full (51 mutants) | rc 0, `killed=51`, `flooding=48/75`, `held_flooding=75/75` | 395 s |
| C2 @ freeze rev, lane tree | `--rev 237ecf4e…` | **rc 2**, `ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)` | 2 s |
| C2 @ freeze tree (extracted) | `git archive 237ecf4 \| tar -x`, fixture commit `e6787d6b…` | rc 0, `37/37` matched, `37/37` killed, `tree=bound` | 85 s |
| C2 @ HEAD | `--rev HEAD --no-mutants` | rc 0, `tree=bound` | 37 s |

Fixture: `D=$(mktemp -d -p /fast/scratch/hyaku/mado-r86/R86CriticClaims)`, `git init -q`, `git archive 237ecf4e | tar -x -C "$D"`, committed as `e6787d6b…` with the lane's own identity (`mado-shokunin <mado@shokunin.local>`); `git -C "$D" show HEAD:SKILL.md | sha256sum` = `f6fc19b3ab7c2d8646c4e7591912a4c6388101b1fca9298614de130f2ab14439`, equal to the freeze blob.

**Bottom line.** Both target *numbers* reproduce. Neither *predicate* is what the declaration says it
is: (a) the C1 binding sentence is weaker in code than in prose, the receipts name the wrong revision,
and the freeze-rev C2 receipt is a transcript relabelled in one field; (b) both kill rules miss on a
strict subset of target-misses and `rc 0` does not imply the kill clause; (c) separability holds one
way but the surfaces are not disjoint — C2 executes C1's tool; (d) C1's axis label changed from r85's
`coverage` with no instrumented calibration move; (e) three of the C1 gap's 27 points are appended
witnesses, not the rule.

---

## (a) One sentence, one condition, one label

### C1 — the sentence matches, the **binding** sentence does not

- Sentence: *"a tool that prints every cause token among the honest answer is refused, while the held
  round-85 rule still gives it full marks."*
- Condition: `target = (correct == CASES and killed == MUTANTS and carried_ok and selftest_ok and flood_correct < CASES and held_flood == CASES)`
- Label: `flooding=48/75 held_flooding=75/75`. Same claim. ✔

The declared *binding* is a different claim:

> "no token of the ten-token vocabulary may appear anywhere in stdout outside that record's own cause
> field (the negative observation)."

Code (`quality/counters/c1-r86-refusal-records.py:347`):

```python
foreign = {token for token in CAUSE_VOCAB if token in stdout} - {cause or ""}
```

The exemption is **by token equality, not by position**. The record's own cause token is allowed
*everywhere* in stdout, not only in its field. Counterexample (built in scratch from the freeze tree's
tool; the rule is imported verbatim from the frozen counter):

```python
'        print("MADO_BARFOOT: ERROR (stage=model%s %s)" % (cause_tag(exc), exc))'
# replaced by: a NOTE line that repeats the record's own cause, then the record
'        print("MADO_BARFOOT: NOTE:%s" % cause_tag(exc))\n' + record
```

```
r86 rule on own-cause echo tool: correct=75/75
refused cases: [] ... 0
```

The declared binding refuses this tool; the frozen rule scores it **75/75**. ✔ defect.

*Not* a defect, checked: the target does bind the record semantics elsewhere. The 51 mutants mutate
`tools/mado-barfoot.py`, and their death depends on cause/stage/rc equality:

```
r86-record-rule                  cause-dropped correct=62/75
geometry+keyword-refusal         cause-dropped correct=75/75
```

The second rule keeps `expected_ok`'s whole non-refusal path and replaces **only** the refusal test
with `"FLOOD:" not in stdout`. A degenerately keyword-based rule is therefore rejected by the mutant
population — the hole is confined to the negative observation, and that hole is reachable.

### C1/C2 — the label names the specimen, the declaration names the freeze

The declaration: *"**Freeze revision**: the commit that carries this declaration, the two counters,
their control sets and the new runbook row"*, and the target block prints `rev=<freeze>`. Both seat
receipts print `rev=f72bba01928efe80cfa1a7907fe3aaa9eba1cfd7` — the preserved attempt-1 commit, not the
freeze `237ecf4e…` (`git ls-tree 237ecf4` carries the repaired counters; `f72bba01` 23:08:08, freeze
00:00:51).

The numbers are invariant, because the specimens did not move:

```
$ git diff --stat f72bba01 237ecf4 -- SKILL.md tools/mado-barfoot.py
(empty)
```

My C1 run at the freeze reproduces the receipt character-for-character except `rev=`:

```
MADO_R86_REFUSALS: cases=75 correct=75 mutants=51 killed=51 base_correct=75/75 carried=72/72
tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=TARGET_MET
rev=237ecf4e69a4986108f719f3beeafe111adaa033 tool_sha256=62626fce…
```

and `MADO_R86_CONTROL: sha256=f6dd9cde…` and `flooding_sha256=3c5ec8b2…` are byte-equal to the seat's
receipt. Provenance defect, not a numeric one.

### C1/C2 — neither receipt binds the instrument's own bytes

C1 prints `tool_sha256` (the specimen) and the control-set sha; C2 binds `SKILL.md`,
`tools/mado-barfoot.py` and the fixtures (`c2-r86-clause-observations.py:829-831`). **No receipt prints
a hash of the counter that produced it.** The lane already routed this class at r85 — M85-3/R3: "final
input hashes bind *identity*, not *chronology*, and `tree=bound` is not full counter/control
authentication" (`corpus/lessons/round-85.md`). It is still true at r86, and it is not hypothetical:
`quality/counters/c1-r86-refusal-records.py` was **modified in the working tree relative to the
freeze** for a period — the docstring `Contract:` line read `mutants=53 killed=53` instead of `…51
killed=51` (`git diff 237ecf4` showed 1 insertion / 1 deletion; the repair is disclosed as repair 4 in
`instrument-repair-r86.md`). It was reverted by `3afdb713` (00:26:42): `git diff 237ecf4 HEAD --
quality/counters/c1-r86-refusal-records.py` is now empty. Predicate-neutral either way, and
unverifiable from any receipt while it lasted.

### A receipt labelled `rev=237ecf4` cannot be a lane-tree run at the freeze

`receipts/final-c2-freezerev-r86.txt` (00:27:14) prints
`… mutants=37 killed=37 verdict=TARGET_MET rev=237ecf4e… tree=bound`. That contradicts my run of the
same frozen command in the lane tree, which exits 2 with
`ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)`.

Three facts, no judgement:

```
SKILL.md working tree : 3cd9b17304ca34618d65176c1003891b9a6cc192b84b8b1435c3ac64b0378032
SKILL.md @237ecf4     : f6fc19b3ab7c2d8646c4e7591912a4c6388101b1fca9298614de130f2ab14439
SKILL.md @HEAD        : 3cd9b17304ca34618d65176c1003891b9a6cc192b84b8b1435c3ac64b0378032   (2 rows added at b33afc08)
```

```
$ diff <(tr -d '\000' < receipts/c2-repaired-r86.txt) <(tr -d '\000' < receipts/final-c2-freezerev-r86.txt)
77c77
< … verdict=TARGET_MET rev=f72bba01928efe80cfa1a7907fe3aaa9eba1cfd7 tree=bound
> … verdict=TARGET_MET rev=237ecf4e69a4986108f719f3beeafe111adaa033 tree=bound
```

The two transcripts differ **only** in the `rev=` field; all 37 probe lines, including every live
`stdout-bytes=` value, are byte-identical. And `tree=bound` is a literal in the print statement
(`"… verdict=%s rev=%s tree=bound"`), so the label asserts "no Setup was raised", not a hash derived
at print time.

[INFERENCE] Either the freezerev run was taken on a copy of the lane at the freeze (then the receipt
should say so — the rev alone cannot distinguish it), or the transcript is the `f72bba01` run with the
rev string rewritten. As published, it does not demonstrate that the frozen predicate holds at
`237ecf4` in the lane tree; that state is reachable only from the freeze bytes (my extracted fixture,
`e6787d6b`, does exactly that and passes).

---

## (b) Does the kill rule miss exactly when the target is missed?

**No.** Write `T` for the declared rc conjunction and `M` for the kill-rule sentence.

### b1. `rc 0` does not imply `T`: the `--no-mutants` branch

C1 declaration: *"rc 0 iff `correct == 75` **and** `killed == 51` …"*. C2 declaration: *"rc 0 iff
`matched == 37`, `shapes == 27`, `bindings == 37`, `clauses_observed == 37` … and `killed == 37`."*

```
$ python3 -I quality/counters/c1-r86-refusal-records.py … --no-mutants
MADO_R86_REFUSALS: … mutants=0 killed=0 … verdict=MUTANTS_SKIPPED rev=237ecf4e…
C1 --no-mutants RC=0

$ python3 -I quality/counters/c2-r86-clause-observations.py --repo . --rev HEAD … --no-mutants
MADO_R86_RUNBOOK: … mutants=0 killed=0 verdict=MUTANTS_SKIPPED rev=b33afc08… tree=bound
RC=0
```

`killed` is false in both and both exit 0. The verdict *label* is honest (`MUTANTS_SKIPPED`, never
`TARGET_MET`), so the harm is bounded to scripted callers — and the C2 counter's own mutant driver is
one (`dead = mrc != 0 and (… mmatched < CASES)`), which is why the label, not the exit code, is load
bearing. The biconditional as written is false.

### b2. `¬T` does not imply `M`: both kill rules under-enumerate their own rc clauses

C1 kill rule: *"misses if any clause is false: a candidate rule that leaves the flooding tool at
75/75, that scores the honest tool below 75/75, that loses a carried case, or that lets a declared
mutant survive."* Four clauses. The rc conjunction has six: it also requires the tool selftest green
and `held_flooding == 75`. A run with `tool_selftest=0/0` (or `held_flooding=74/75`, i.e. the control's
own premise failing) prints `verdict=TARGET_MISSED`, rc 1, and **no** kill-rule clause fires.

C2 kill rule: *"misses if any of the four round-85 survivors lives, if any case's declared clause is
not observed, if the new witness is not matched, or if the working tree is not the measured revision's
bytes."* The rc conjunction also requires `shapes == 27` and `bindings == 37`, and `killed == 37`
covers **33 mutants that are not among "the four"**. A survivor among the other 33 → rc 1, kill rule
silent.

So `M ⊊ ¬T` for both. The direction that matters (a survivor is never a footnote) holds; the reverse
direction does not.

### b3. Kill-rule conditions implemented as setup errors, not misses

- C1: `carried_ok` false → `raise Setup(…)` → rc 2, no verdict (`:580-582`). The printed `carried=72/72`
  is therefore tautological whenever the line prints, and the kill clause "loses a carried case" is
  never a *miss* — it is a could-not-evaluate.
- C2: `tree=bound`, `rows == 37`, `bindings == 37` are all `raise Setup` → rc 2. The kill rule calls
  the tree case a miss; the code calls it an error. (The lane's own SKILL.md registry row uses the
  three-valued vocabulary `1 miss; 2 could-not-evaluate`, which the declaration's kill rule does not.)

### b4. C1 has no self-mutation population

C1's 51 mutants mutate **`tools/mado-barfoot.py`** (`apply_mutation(source, …)` where `source` is the
extracted tool). C2's 37 mutate **its own source**. So C1's "51/51 killed" is evidence about the
tool/case-set, and the *rule* is tested by exactly one hand-built control: the flood. The own-cause
echo above is a rule defect that the population structurally cannot see.

---

## (c) Causal separability, from the file dependencies

Verified by reading what each counter opens, not by prose:

| dependency | C1 | C2 |
|---|---|---|
| `SKILL.md` | **not opened** (`grep -c SKILL quality/counters/c1-r86-refusal-records.py` → `0`) | `git_show(repo, rev, "SKILL.md")`, plus hash-bind (`:828-831`) |
| `tools/mado-barfoot.py` | extracted at `--rev` **and** `--base-rev`, then scored | **hash-bind only** — never parsed |
| controls / carried | `args.controls`, `args.carried`, sha printed | same, plus per-case fixture hash-bind |
| own source | not read | read as `__file__` to build mutants |

- "C1 needs no SKILL.md row": **true**.
- "C2 needs no `tools/mado-barfoot.py` change": **true** — it never reads the tool's content.

But the surfaces are **not disjoint**, and the declaration's word "separable" overstates it:

1. Four of C2's rows *execute* the tool C1 scores:
   `refuse-mode`, `refuse-scale`, `refuse-layer-background`, `refuse-output-space`
   (`argv: python3 -I tools/mado-barfoot.py --config .ufo/waves/round-79/fixtures/…`). A C1 move that
   changed a refusal message breaks C2's `refusal` rows, whose negatives bind exact refusal text.
2. C2's `tree=bound` **pins** the C1 surface file. Any C1 landing edit to the tool invalidates C2's
   verdict until `--rev` advances.
3. This round demonstrated the reverse coupling: `b33afc08` ("register the counters at SKILL.md")
   added two registry rows to `SKILL.md` at 00:10:24, and that alone makes the frozen C2 predicate
   exit 2 (see (a)/(b) above). Registering the claim invalidated the claim's own binding.

Separability therefore holds as *"neither needs the other's change"*, and fails as *"either verdict
survives the other's landing"*.

Cross-authority: C2 scores refusals by substring and says so —
`return rc == value["rc"] and ("ERROR (stage=%s " % value.get("stage", "model")) in stdout` — the exact
rule C1's round declares a forgery ("A gate that cannot tell a record from a flood overreaches every
claim it prints"). One round, two definitions of a valid refusal, applied to the same tool. C2's claim
does not cover it, but the lane now holds two authorities on the same judgement.

---

## (d) Axis naming

**AXES.md does not exist in the lane.** `ls AXES.md` fails; `find . -name 'AXES*'` returns only
`.ufo/waves/**` scratch. The contract survives only inside the lane's axis gate,
`quality/check-axis-scores.py`, whose docstring defines it: *"AXES.md defines calibration as
`SHONEN.md/SCORECARD entries match observed repo state`"*, and which re-derives exactly three axes:

```
$ python3 -I quality/check-axis-scores.py --repo . --rev 237ecf4e…
MADO_AXIS_ROW: axis=navigation published=106/106 derived=106/106 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=86/86 derived=86/86 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=237ecf4e…
```

- **C1 = calibration.** The instrumented calibration axis is *resolved-active entries* (86/86), i.e.
  "entries match observed repo state". C1 moves no entry and no derived fraction; it changes a refusal
  gate's judgement. The same instrument family was labelled **coverage** one round earlier —
  `corpus/lessons/round-85.md`: *"C1 (coverage) binds a declaration-identity refusal to its own
  `cause=` token"*. So the axis label for an unchanged surface moved coverage → calibration, with no
  new rubric row and no derived cell. C1's surface does **not** match the calibration axis as the
  lane's own instrument defines it.
- **C2 = operability.** The surface (rows execute; mutants die by clause observation) matches the
  operability *family* — the SCORECARD's operability rubrics are gate selftest and mutation kills. But
  the published operability cell is `selftest 12/12, ledger 158/158`; C2 moves neither. Family match,
  no cell move.
- The lowest-axis obligation rests on prose, not on either axis system: *"coverage/operability tie at
  9.0/10 in `SCORECARD.md`"*. `9.0` is the saturation value (`Axis posture: saturation 9.0 / window
  N=3`), and r56's own text contradicts the tie as a *score*: *"The lowest **scored** non-retired axis
  is freshness (file-plane gate agreement, 28/29 = 9.6552)"*. No committed instrument derives a 9.0
  coverage or operability score; `check-axis-scores.py` compares fractions only. The tie is
  unfalsifiable from local instruments.

---

## (e) Are the r86 additions a capability/depth move disguised as coverage?

Measured decomposition (frozen cases, frozen rule, imported verbatim):

```
carried72 honest 72/72
carried72 flood  48/72
carried72 flood under HELD r85 rule 72/72
all75     honest 75/75
all75     flood  48/75
all75     flood under HELD r85 rule 75/75
```

**C1.** The rule change alone yields a **24/72** gap on the pre-existing population. The headline
**27/75** adds 3/75 from the appended witnesses (`alloc-negative-cause`, `alloc-bool-cause`,
`alloc-float-band`) — new *inputs* over existing causes (`alloc-non-integer`, `alloc-negative`), i.e.
depth on the tool's validation surface. The declaration discloses it ("Three witnesses are appended to
the carried 72") and the control sha covers it, so it is not disguised; but the printed contract has no
`flooding_carried` cell, so the headline cannot be decomposed by a reader without re-running the
counter as I did. The 3 witnesses are capability witnesses carried inside a calibration claim.

**C2.** The new row is depth in the right place, and I verified its necessity rather than taking it:

```
regex-anchor-dropped  rc 1 failing cases: ['border-size-int']
line-anchor-prefix    rc 1 failing cases: ['border-size-int']
```

Both anchor mutants die on exactly one case — the new `border-size-int` — and on nothing else. So
"carries the witness the two round-85 anchor survivors needed" is literally true. The cost is that the
anchor branch is entered by only the 3 `anchor: line` cases (`version`, `omarchy-version`,
`border-size-int`); the first two cannot distinguish a prefix rule because their patterns already carry
`^`/`$`, so **one row, carried by its two negatives (`0 extra`, `-1`), is the entire discriminator**.
That is a single point of failure, not disguised coverage.

Carried defect, re-used: `shapes=27/27` is a clause of C2's rc condition, but `shapes` counts
shape-kind **cases** (27 of 37) across **14 distinct kinds**. This is the r85 routed defect M85-10 —
*"the declared C2 shape count reads as a diversity claim it is not"* — repeated in a frozen target
without a qualifier.

---

## Do-nothing controls and reachability

| target | do-nothing instrument | measured score | verdict on the target |
|---|---|---|---|
| C1 | held r85 rule (`held_ok`) | honest 72/72 (carried) / 75/75 (all); flood **72/72** / **75/75** | gap 0 → `flooding < 75` false → **miss** |
| C2 | r85 instrument (36 rows) at the r86 tree | `cases=36 matched=36 shapes=26/26`; `killed=33`, survivors `regex-anchor-dropped`, `line-anchor-prefix`, `negatives-skipped`, `samples-skipped` (4 × `killed=no`) | **miss** (cannot reach 37/37) |

Both targets are **unreachable without the round's work**, and the reason differs:
C1 needed only the **rule** — `base_correct=75/75` proves the r85 tool already satisfies the r86 case
set, so the increment is the rule and not the tool (declaration control 2, reproduced). C2 needed the
clause observation **and** the new row — the same mutant population dies 33/37 without them.

Declared anti-cribbing clause, checked and false:

> "Do-nothing controls are built and committed **before** the candidate measurements (receipts under
> `.ufo/waves/round-86/receipts/control-*`)"

```
$ git ls-tree --name-only 237ecf4 -- .ufo/waves/round-86/receipts/
c1-r86.txt  c2-anchor-only-r86.txt  c2-live-observation-r86.txt  c2-repaired-r86.txt  instrument-repair-r86.md
     # no control-* receipt at the freeze; the three files are untracked (`??` in git status)

00:00:41 c1-r86.txt      00:11:10 control-c1-r86.txt
23:57:54 c2-repaired     00:11:23 control-c2-r86.txt
                         00:12:18 control-held-rule-r86.txt
```

They are also not do-nothing instruments: `control-c1-r86.txt` and `control-c2-r86.txt` are
`--no-mutants` runs of the **candidate** (`mutants=0 killed=0 verdict=MUTANTS_SKIPPED`, revs
`237ecf4e` and `b33afc08`). Only `control-held-rule-r86.txt` measures a held instrument.

Related: the lane's own chronology gate cannot evaluate this round —

```
$ python3 -I quality/check-freeze-order.py --repo . --rev 237ecf4e… --round 86 --wave w1
MADO_FREEZE_ORDER: round=86 wave=w1 freeze=none freeze_time=none launch=none verdict=FAIL reason=no_freeze
freeze-order RC=1
```

— because it requires `claims-frozen.md` and `registration.md`, which this round does not have.

---

## Findings ledger

| # | class | claim | impacted axes | smallest safe correction |
|---|---|---|---|---|
| F1 | label ≠ freeze | receipts print `rev=f72bba01`, declaration says `rev=<freeze>`; numbers invariant (empty specimen diff) | provenance (both) | print `specimen=<rev>` and `freeze=<rev>` as separate fields |
| F2 | self-invalidating binding | at the freeze rev the frozen C2 command exits 2 (`SKILL.md in the working tree is not the measured revision's bytes`) because `b33afc08` added 2 rows at 00:10:24; it passes at HEAD and on the extracted freeze tree | operability | bind the 37 row *cells* + fixtures, not the `SKILL.md` blob; or state that `tree=bound` is a point-in-time cell |
| F3 | prose > code | `foreign = {…} - {cause or ""}` exempts the record's own cause token everywhere; own-cause echo tool scores 75/75 against a binding that refuses it | calibration | strip the record's own span before scanning: `re.sub(REFUSAL_RE, "", stdout)` then scan |
| F4 | rc contract | `--no-mutants` returns rc 0 with `killed=0` on both counters | calibration + operability | make the skip branch exit 3 (distinct from 0/1/2) |
| F5 | kill rule ⊊ target | C1 kill rule omits selftest/`held_flooding`; C2 kill rule omits `shapes`, `bindings`, 33 non-"four" mutants | both | enumerate the rc conjunction verbatim in the kill rule |
| F6 | no rule-mutation | C1's 51 mutants mutate the tool, not the rule; the rule has one adversarial control | calibration | add a C1 self-mutation population (clone C2's `__file__` approach) |
| F7 | unbound instrument | no receipt prints the counter's own sha; the C1 counter is edited post-freeze | provenance (both) | print `self_sha256` and commit the instrument before measuring |
| F8 | coupling | C2 executes `tools/mado-barfoot.py` in 4 rows and pins its bytes; registering the counters at SKILL.md invalidated C2 | operability | declare the coupling, or move those 4 rows out of the C2 population |
| F9 | duplicate authority | C2's `refusal` kind is the substring rule C1's round declares a forgery, applied to the same tool | calibration | adopt the record rule in C2's `refusal` kind |
| F10 | axis label | C1 was `coverage` at r85, `calibration` at r86; `check-axis-scores.py` re-derives resolved-active 86/86, moved by neither claim; AXES.md absent | calibration | name the instrumented sub-axis and show the cell, or state "no axis cell moves" |
| F11 | composition | headline 27/75 = 24/72 rule + 3/75 appended witnesses; no `flooding_carried` cell | calibration | print the carried-subset flood score |
| F12 | M85-10 repeat | `shapes=27/27` counts shape-kind cases across 14 kinds, and is an rc clause | operability | rename `shape_cases=`; print distinct-kind count separately |
| F13 | single witness | both anchor mutants die on exactly `border-size-int` (36/37 cases do not distinguish them); the witness's discriminating power (`held_rule_new_case`) is a control, not a clause | operability | print the killing case per anchor mutant, or promote `held_new_case == 1` to a clause |
| F14 | thaw (resolved) | `quality/counters/c1-r86-refusal-records.py` differed from the freeze in the working tree (docstring `53`→`51`) from the 00:00:41 measurement until `3afdb713` reverted it; predicate-neutral, unverifiable from receipts while it lasted | provenance | commit or revert before any seat scores |
| F15 | false provenance | `final-c2-freezerev-r86.txt` is byte-identical to `c2-repaired-r86.txt` except `rev=`, and `rev=237ecf4` is unreachable in the lane tree (SKILL.md hashes); `tree=bound` is a print literal, not a derived hash | operability, provenance | print `repo_tree_sha` and `specimen=`/`freeze=` separately; a receipt taken on a copy must say so |

Severity: F2, F3, F4, F7, F15 are defects in the frozen artefacts or in what their receipts prove;
F1, F5, F9, F10, F12 are declaration/label bookkeeping that a reader would otherwise resolve the
wrong way; F6, F8, F11, F13 are tradeoffs of the design that the record should state rather than
repair; F14 is closed (reverted).

## What I could not run

- The frozen C2 command **at the freeze revision against the lane tree** — it fails closed by design
  (F2). Reproduced on an extracted freeze tree instead (`e6787d6b`), which is equivalent for every
  binding the counter makes.
- No re-derivation of the `9.0` coverage/operability tie: no committed instrument produces it.
- `check-freeze-order.py` cannot evaluate the round (missing freeze file names); the chronology of
  `237ecf4` is therefore uncertified by the lane's own gate.

Scratch (`/fast/scratch/hyaku/mado-r86/R86CriticClaims/`) was removed after this report was written.
