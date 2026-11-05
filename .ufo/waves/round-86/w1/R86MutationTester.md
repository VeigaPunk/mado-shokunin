# R86MutationTester — independent mutation battery over the two r86 counters

Seat: R86MutationTester (mutation-tester, leaf; no subagent dispatch). Wave: round-86 w1, hyaku run 15.
Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`. Tasking rev
`237ecf4e69a4986108f719f3beeafe111adaa033`. Frozen declaration read first
(`.ufo/waves/round-86/claims-declaration-r86.md`).

Verdict in one line: **17 counter mutants beyond the declared populations — 5 killed, 12 survived.
Every survivor has a named hole and an executed doctored input that the pristine instrument refuses
and the mutant accepts.** The declared populations (51 tool mutants for C1, 37 self-mutants for C2)
are *not* what this battery measures; it measures the instruments' own rules.

## 0. Identity of the bytes measured

| item | sha256 |
|---|---|
| `quality/counters/c1-r86-refusal-records.py` at 237ecf4e (copied to scratch as `frozen-c1.py`) | `d651c6aab255826301954782beba0e5b145a9fc37ae24e0b2571393383ce4df4` |
| `quality/counters/c2-r86-clause-observations.py` at 237ecf4e (`frozen-c2.py`) | `1283df22a1bf2ca53b70c290ea7c0d4e5821e69f380c6daa95708af0a0f7faf5` |
| `tools/mado-barfoot.py` at 237ecf4e (the `tool_sha256` every C1 run prints) | `62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5` |
| `.ufo/waves/round-86/controls/c1-cases-r86.json` (counter-reported `MADO_R86_CONTROL: sha256=`) | `f6dd9cdef7daa2e6b51c95f27cf8ebe8509188c551ff18ed42a176a08d8620bf` |
| `.ufo/waves/round-86/controls/c2-cases-r86.json` (`MADO_R86_CONTROLS: sha256=`) | `a87f0ea480b36a8eec8592ccdffb6b1e3d60b183c343af2cc5c4563c23bd57d8` |

The c1 counter's working-tree bytes changed under this seat during the wave (a docstring-only edit,
`mutants=53` → `mutants=51`, present at 00:16 and reverted by ~00:50; `git status` is clean for that
path now). Every measurement below used the rev-237ecf4e bytes copied with `git show`, never the
working tree. No lane file other than this report was written by this seat; the counters, control
sets, carried sets, declaration and sibling reports were opened read-only.

Scratch: `/fast/scratch/hyaku/mado-r86/R86MutationTester/` (removed before yield).

## 1. Baselines actually run (pristine frozen instruments)

```
$ python3 -I $S/c1/frozen-c1.py --repo $R --rev 237ecf4e69a4986108f719f3beeafe111adaa033 \
    --base-rev 2b6dd76b65de4dfe701db87db13b7e448b3538ee \
    --controls $R/.ufo/waves/round-86/controls/c1-cases-r86.json \
    --carried $R/.ufo/waves/round-85/controls/c1-cases-r85.json --scratch-root $S/c1/base
MADO_R86_REFUSALS_SELFTEST: 127/127                          # --selftest, rc 0
MADO_R86_REFUSALS: cases=75 correct=75 mutants=51 killed=51 base_correct=75/75 carried=72/72 \
  tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=TARGET_MET \
  rev=237ecf4e69a4986108f719f3beeafe111adaa033 tool_sha256=62626fce...   rc=0  wall=378.30s

$ python3 -I $S/c2/frozen-c2.py --repo $R --rev b33afc089fad2fcc5f6684f3b3a9d2260cf2e915 \
    --controls $R/.ufo/waves/round-86/controls/c2-cases-r86.json \
    --carried $R/.ufo/waves/round-85/controls/c2-cases-r85.json --scratch-root $S/c2/base
MADO_R86_RUNBOOK_SELFTEST: 114/114                           # --selftest, rc 0
MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37 \
  clauses_observed=37/37 mutants=37 killed=37 verdict=TARGET_MET \
  rev=b33afc089fad2fcc5f6684f3b3a9d2260cf2e915 tree=bound               rc=0  wall=74.02s
```

Both claims reproduce at their scoreable revs under my independent run. `$S` is the scratch root
above, `$R` the lane root.

## 2. Finding (not a mutant): C2 cannot be scored at the tasking rev

```
$ python3 -I $S/c2/frozen-c2.py --repo $R --rev 237ecf4e69a4986108f719f3beeafe111adaa033 \
    --controls $R/.ufo/waves/round-86/controls/c2-cases-r86.json \
    --carried $R/.ufo/waves/round-85/controls/c2-cases-r85.json --scratch-root $S/c2/basefreeze
MADO_R86_RUNBOOK: ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)
rc=2
```

`git -C $R diff 237ecf4e..HEAD -- SKILL.md` is `+2` rows (`b33afc08` registered the two r86 counters in
the SKILL.md **counter-registry** table, not in either `### Executable runbook rows` section). C2 binds
the working tree byte-equal to `--rev`, so at the freeze rev the instrument fails closed and no C2
verdict exists there. The lane's own control receipt `.ufo/waves/round-86/receipts/control-c2-r86.txt`
also used `rev=b33afc089...`, so the lane is self-consistent and the tasking text (and the
declaration's `rev=<freeze>` placeholder) is what diverges from what the instrument can measure.

Battery consequence: **C1 mutants are scored at 237ecf4e; C2 mutants at b33afc08** — the only rev at
which the C2 baseline reaches a verdict. Scoring C2 at 237ecf4e would have made every C2 mutant
"inconclusive" (baseline setup failure), not "killed".

## 3. Method

Each mutant is a scratch copy of the frozen instrument with one expression replaced (anchors asserted
to occur exactly once). For each copy: (a) the copy's own `--selftest`; (b) one full scoring pass with
the same arguments as the baseline. **Killed** = selftest exits nonzero, or the full pass exits nonzero
/ a declared-population mutant survives. **Survived** = selftest green *and* `verdict=TARGET_MET`.
Survivors were then probed with a doctored input (§4) — a surviving mutant is a coverage hole and the
hole is named with the exact input.

Reproduction: `specs.py` (the table below verbatim as `(name, anchor, replacement)`) + a driver that
writes `$S/c1/mut/<name>.py` / `$S/c2/mut/<name>.py` and runs the two baseline commands of §1 once per
copy. The battery ran in a 9-worker pool (32 cores); the 9 C1 passes (~378 s each at that contention)
and the 8 C2 passes (~74 s each) overlapped as slots freed, 17 full passes in ~35 min.

## 4. Battery — 17 mutants

### 4.1 C1 — `quality/counters/c1-r86-refusal-records.py` (scored at 237ecf4e)

| # | mutant | mutation (before → after) | selftest | full pass | verdict |
|---|---|---|---|---|---|
| m01 | `record-any-count` | `if len(records) != 1:` → `if not records:` | 127/127 rc0 | rc0 `TARGET_MET` correct=75 killed=51 flooding=48/75 held=75/75 | **SURVIVED** |
| m02 | `record-search-anywhere` | `REFUSAL_RE` loses `^` and `re.M` (record may match anywhere) | 127/127 rc0 | rc0 `TARGET_MET` correct=75 killed=51 flooding=48/75 held=75/75 | **SURVIVED** |
| m03 | `negative-one-class` | `CAUSE_VOCAB` loses `"alloc-negative"` | 127/127 rc0 | rc0 `TARGET_MET` correct=75 killed=51 flooding=48/75 held=75/75 | **SURVIVED** |
| m04 | `cause-any-of-ten` | `if want is not None and cause != want:` → `… cause not in CAUSE_VOCAB:` | **126/127 rc1** (`another cause is refused`) | rc1 `TARGET_MISSED` correct=75 **killed=48**; survivors `alloc-dup-cause-collapsed`, `ns-dup-cause-collapsed`, `ns-dup-level-blind` (all 75/75) | **KILLED** |
| m05 | `carried-check-skipped` | `carried_ok = cases[:CARRIED] == carried` → `carried_ok = True` | 127/127 rc0 | rc0 `TARGET_MET` carried=72/72 (printed from the same constant that was just faked) | **SURVIVED** |
| m06 | `rc-ignored-result-cases` | result-case field loop also skips `"rc"` | 127/127 rc0 | rc0 `TARGET_MET` correct=75 killed=51 | **SURVIVED** |
| m07 | `tool-selftest-rc-free` | `selftest_ok = (rc == 0 and m is not None …` → `(m is not None …` | 127/127 rc0 | rc0 `TARGET_MET` tool_selftest=152/152 | **SURVIVED** |
| m08 | `stage-unchecked` | `if stage != exp.get("stage", "model"):` → `if False:` | 127/127 rc0 | rc0 `TARGET_MET` correct=75 killed=51 | **SURVIVED** |
| m09 | `negative-observation-dropped` | `foreign = {token … if token in stdout} - {cause}` → `foreign = set()` | **126/127 rc1** (`a foreign cause token is refused`) | rc1 `TARGET_MISSED` **flooding=75/75** | **KILLED** |

### 4.2 C2 — `quality/counters/c2-r86-clause-observations.py` (scored at b33afc08, §2)

| # | mutant | mutation (before → after) | selftest | full pass | verdict |
|---|---|---|---|---|---|
| m01 | `live-snapshot-dropped` | `ran = (LIVE["anchors"], …)` → `ran = (clauses["anchors"], …)` | 114/114 rc0 | rc1 `TARGET_MISSED` **clauses_observed=34/37** (the three `anchor: line` cases: `version`, `omarchy-version`, `border-size-int`), killed=37 | **KILLED** |
| m02 | `clause-equality-dropped` | `if OBS["samples"] != len(samples) or OBS["negatives"] != len(negatives):` → `if False:` | 114/114 rc0 | rc1 `TARGET_MISSED` **killed=35**; `negatives-skipped` and `samples-skipped` both 37/37 alive — exactly the r85 survivors | **KILLED** |
| m03 | `observed-all-constant` | `observed_all += 1 if ran == declared else 0` → `observed_all += 1` | 114/114 rc0 | rc0 `TARGET_MET` clauses_observed=37/37 | **SURVIVED** |
| m04 | `tree-bound-dropped` | working-tree sha256 loop → `pass` | 114/114 rc0 | rc0 `TARGET_MET` … `tree=bound` | **SURVIVED** |
| m05 | `carried-field-drift` | carried `allowed` gains `{"value", "argv", "anchor"}` | 114/114 rc0 | rc0 `TARGET_MET` matched=37 | **SURVIVED** |
| m06 | `shapes-count-every-case` | `shapes += 1 if case["kind"] in SHAPE_KINDS and good else 0` → `shapes += 1 if good else 0` | 114/114 rc0 | rc1 `TARGET_MISSED` **shapes=37/27** | **KILLED** |
| m07 | `live-anchor-clause-dropped` | `if case.get("anchor") == "line" and LIVE["anchors"] != 1:` → `if False:` | 114/114 rc0 | rc0 `TARGET_MET` matched=37 | **SURVIVED** |
| m08 | `live-anchor-declared` | `LIVE["anchors"] = OBS["anchors"]` → `LIVE["anchors"] = 1 if case.get("anchor") == "line" else 0` | 114/114 rc0 | rc0 `TARGET_MET` clauses_observed=37/37 | **SURVIVED** |

Totals: **5 killed / 12 survived** of 17. Notes on the three kills that matter most:

* m02 is the load-bearing kill: deleting the samples/negatives equality is the *only* thing that
  leaves `negatives-skipped` and `samples-skipped` alive, i.e. the r85 C2 defect is cured by that
  single equality and by nothing else in the rule.
* m01 dies through `observed_all` alone (matched stays 37/37) — the printed clause count is the only
  detector of the live-snapshot defect.
* m06 dies through the constant 27, not through any behaviour: `shapes=37/27` is a comparison to a
  frozen population size.

## 5. Survivors — the holes, each with an executed witness

All of these are "pristine instrument refuses, mutant accepts", run on the same bytes.

| hole | mutant | doctored input | pristine | mutant |
|---|---|---|---|---|
| the record need not be unique, only the *cause* need be unique: a tool printing the identical refusal twice (same stage, same cause) is accepted, because the foreign-token set subtracts the cause and the second record adds no new token | m01 | `expected_ok({"expect":{"error":True,"rc":2,"stage":"setup","cause":"alloc-negative"}}, 2, record + record)` | `False` | `True` |
| `^`/`re.M` are not load-bearing: a record found mid-line satisfies the rule, so any log prefix defeats "the record is a line" | m02 | stdout `"LOG: MADO_BARFOOT: ERROR (stage=setup cause=alloc-negative …)\n"` | `False` | `True` |
| the negative observation is only as wide as the ten-token literal: drop one token and a one-token flood is invisible — the flood control cannot see it either, because it builds its flood *from* `CAUSE_VOCAB` | m03 | record with `cause=alloc-unknown-namespace` + `MADO_BARFOOT: FLOOD: alloc-negative` | `False` | `True` |
| the carried parsed-equal clause is untested: no case, mutant or control moves when it is faked | m05 | carried set with `cases[5].expect.band = 47` | `rc=2 MADO_R86_REFUSALS: ERROR (stage=setup the successor set does not carry the frozen round-84 cases unchanged)` | `rc=0 … carried=72/72 … verdict=MUTANTS_SKIPPED` |
| a result case's exit status is not exercised: the honest tool never exits nonzero, so `rc` can be dropped from the compared fields | m06 | `expected_ok({"expect":{"rc":0,"box":"MATCH","reserved":"EQ","band":34,"expected":34,"verdict":"CLEAN"}}, 7, <correct RESULT line>)` | `False` | `True` |
| the tool-selftest `rc == 0` clause is never exercised: the honest tool exits 0, so `tool_selftest=152/152` can be printed by a tool whose selftest exits 1 | m07 | fixture git repo (§5.1) whose tool prints `MADO_BARFOOT_SELFTEST: 152/152` and returns 1 | `rc=1 TARGET_MISSED` (all other clauses green: correct=75 killed=51 flooding=48/75 held=75/75) | `rc=0 TARGET_MET` |
| the stage equality is redundant against the population: no selftest check holds `rc` fixed while varying the stage | m08 | `expected_ok({"expect":{"error":True,"rc":2,"stage":"setup","cause":"alloc-negative"}}, 2, "…(stage=model cause=alloc-negative …)")` | `False` | `True` |
| `clauses_observed` is not independent evidence: `case_correct` already refuses a case whose declared clause did not run, so `matched == 37` implies `observed_all == 37`; the printed field can be constant-folded | m03 (C2) | controls copy with `border-size-int` kind→`exact`, value→`[0-9]+` (a declared `anchor: line` case whose live judgement never takes the anchor branch) | `matched=36 … clauses_observed=36/37` | `matched=36 … clauses_observed=37/37` |
| `tree=bound` is printed unconditionally: with the binding deleted the instrument still claims the working tree is the measured rev | m04 (C2) | run at `--rev 237ecf4e` with the tree at `b33afc08` (§2) | `rc=2 ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)` | `rc=0 … rev=237ecf4e… tree=bound` |
| the carried-set comparison is untested: a drifted carried expectation is accepted | m05 (C2) | carried copy with `cases[7].value = "drifted"` | `rc=2 ERROR (stage=setup carried case 'layers-namespaces' changes field 'value')` | `rc=0 … matched=37/37 … TARGET_MET` |
| there are two independent anchor guards and neither is self-tested: the `LIVE["anchors"] != 1` clause in `case_correct`, and the snapshot's honesty | m07/m08 (C2) | `case_correct({"kind":"exact","value":"5","anchor":"line"}, 0, "5")` (matches exactly, but the live judgement never takes the line branch) | `False` | `False→True` (m07 `True`; m08 `True`, and m08 also reports `LIVE=1` for a case whose `OBS["anchors"]` is 0) |

### 5.1 The m07 fixture (only place a git write happened, in scratch)

```sh
S=/fast/scratch/hyaku/mado-r86/R86MutationTester ; R=/home/vgpnk/Projects/shokunin/mado-shokunin
F=$S/fixture/toolrepo ; mkdir -p $F/tools
git -C $R show 237ecf4e69a4986108f719f3beeafe111adaa033:tools/mado-barfoot.py > $F/tools/mado-barfoot.py
git -C $R show 237ecf4e69a4986108f719f3beeafe111adaa033:SKILL.md > $F/SKILL.md
# edit: selftest's `return 0 if checks == total else 1`  ->  `return 1  # FIXTURE`
git -C $F init -q
test "$(git -C $F rev-parse --show-toplevel)" = "$F"        # asserted before the first commit
git -C $F config user.name  "$(git -C $R config user.name)"     # mado-shokunin (the lane's own identity)
git -C $F config user.email "$(git -C $R config user.email)"    # mado@shokunin.local
git -C $F add -A && git -C $F commit -q -m "fixture: frozen r86 tool with a nonzero selftest exit"
$F commit = eea9d2f39051faf0f7e0f530e9d71655241a75bf ; tool sha256 = 0ef2b99e98e60bf0955e59035970d77fd20102f6ea8efb634346bed2233960a7
python3 -I $F/tools/mado-barfoot.py --selftest   # MADO_BARFOOT_SELFTEST: 152/152 ; rc=1
```

Then both counters run with `--repo $F --rev HEAD --base-rev HEAD` and the lane's control/carried
files: pristine → `verdict=TARGET_MISSED` (rc 1), m07 → `verdict=TARGET_MET` (rc 0), same
`tool_sha256=0ef2b99e…` in both. No mutating git command touched the lane; the fixture is a throwaway
directory under scratch and was removed with it.

## 6. Other findings (reported, not fixed)

1. **Frozen docstring contradicts the frozen constant.** `git -C $R show
   237ecf4e:quality/counters/c1-r86-refusal-records.py | grep -n "Contract:"` →
   `15:Contract: … mutants=53 killed=53 …`, while `MUTANTS = 51` in the same file, the measured kill
   count is 51, and the declaration says 51. The working tree briefly carried an uncommitted repair of
   this line during the wave (`git diff` showed `-53 … +51` at 00:16) which was reverted by ~00:50; at
   report time `sha256sum quality/counters/c1-r86-refusal-records.py` equals the frozen
   `d651c6aa…`. The instrument therefore ships a contract line no run can satisfy by reading.
2. **The C1 diagnostic path returns 0 without evaluating the target.**
   `python3 -I quality/counters/c1-r86-refusal-records.py --repo . --rev 237ecf4e… --base-rev
   2b6dd76b… --controls … --carried … --scratch-root … --no-mutants` →
   `… mutants=0 killed=0 … verdict=MUTANTS_SKIPPED …`, `rc=0`. The `target` expression is never
   evaluated on that branch, so an operator keying on the exit status reads a skip as success. C2's
   `--no-mutants` branch does evaluate the other clauses and returns 1 on `matched < 37` (observed:
   `rc=1 TARGET_MISSED` in the §5 probe), so the two instruments disagree on what a skip means.
3. **Stale label in a user-facing error.** The carried-set failure at C1 says "the successor set does
   not carry the **frozen round-84** cases unchanged" while it compares the r85 carried set (round-86
   instrument). Cosmetic, but it is the message an operator sees when the carried set is doctored.
4. **C1 records are bound by `len(records) == 1` but not by *which* line.** No case in the 75 prints a
   second record, so the exactly-once clause has exactly one detector in the whole instrument: the
   foreign-token set (§5, m01). Any future tool that repeats its own refusal silently widens the gate.
5. **C2 docstring rendering artifacts** at lines 20/24/38: `The36`, `of37`, `Target:cases37/…` — the
   numeric templating dropped spaces. Cosmetic; the numbers agree with the code (`CASES=37`,
   `MUTANTS=37`, `SHAPES=27`).

## 7. What I did not run, and what would be inconclusive

* No C2 mutant was scored at 237ecf4e — the baseline itself fails there (§2), so any such run would be
  a setup failure, not a verdict.
* I did not mutate the control sets, the carried sets, the declaration, `SKILL.md`, the tool, or any
  sibling report. The doctored inputs of §5 live only in scratch copies.
* The 51 declared C1 tool-mutants and the 37 declared C2 self-mutants were exercised only as part of a
  full pass; I did not extend either declared population.
* Not measured here: whether the *claims* hold (that is the executors' and reviewers' remit), and
  whether the C2 runbook rows are the right rows (operability judgement, not mutation coverage).
* Reproducibility caveat: C2 shells out to live `hyprctl`/`systemctl`/`busctl` rows, so a C2 score is
  only reproducible on this desktop at the same tree bytes; the C1 score is fully self-contained apart
  from `python3`.
