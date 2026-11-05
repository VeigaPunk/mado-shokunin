author: hyaku closure (non-author integrator, @m_zfl)

# mado round 86 — verifier spot-check (non-author)

Round report `.ufo/reports/round-86/mado.md`; lane repo `mado-shokunin`; round tip (the commit closed)
`500bef3c8782788b1e3b327845a3a0694b8594fe`; round base `a722c60493f24f83429112e9123058835b2cdd82`;
declaration/instrument freeze `237ecf4e69a4986108f719f3beeafe111adaa033`. I did not author this round.
Every command below was run by me against committed bytes. This file supersedes the first landing of
the same path (`landed 5e78674f…`): its quality grade was self-contradictory and is corrected here as a
new commit, not an amend.

## 1. Conformance (step 1)

| item | command | observed | result |
|---|---|---|---|
| report committed by the lane identity | `git log --format='%an %ae %H %ci' -- .ufo/reports/round-86/mado.md` | `mado-shokunin mado@shokunin.local 932d6067… 2026-11-05 00:40:16`; earlier filing `78b3faab… 00:38:37` | pass |
| `SHONEN` heading, one line per box | `grep -n '^## SHONEN' .ufo/reports/round-86/mado.md`; `grep -c '^- \[' SHONEN.md` | heading present; four `[~]` lines; `SHONEN.md` has 4 boxes; no `[x]` written | pass |
| cited lane commits exist and are ancestors of the branch | `git cat-file -e $h^{commit}` and `git merge-base --is-ancestor $h master` over every cited hash | all cited hashes exist and are ancestors of `master`, including `d7ffa762` (cited in receipts, absent from the report's Landed-changes table) | pass |
| no uncommitted round work; pushed | `scripts/hyaku/jj-lane.sh state mado-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 tracked=0 untracked=0`; status empty; remote `500bef3c…` | pass |
| prompt carries the template contract | `.ufo/prompts/mado-round-86.md` | §1 mission/axes, §3 L2 floor and route deferral, §4 report path and sections incl. `SHONEN`, §5 commit-then-push and push scope and L0 channel, §6 addendum (write scope, report-lands-last, hash-citation rule) | pass |
| wave shape | `w1-results.json`; `w1/` | `seats=14`, 14 result rows, 0 empty outputs, 14 seat reports; executor 3, scribe 3, scout 2, reviewer 2, critic 1, mutation-tester 1, sentinel 1, connector 1; no dead seat | pass |

**Conformance defects (status-neutral, routed in §6):** the report was rewritten in a second commit
(`932d6067`: 228 insertions, 149 deletions over the same file) instead of an erratum appended after the
filed bytes; the first filing (`78b3faab`) preceded the lane commit it cites; the Landed-changes table
omits `d7ffa762`.

## 2. Per-claim re-check

Both claims rest on lane-owned counters. Per `PROTOCOL.md` §Gate standard (Closure consequence) I
verified their committed evidence and did not execute either counter. What I re-derived myself is the
population arithmetic, the carried-set equality and the tool bytes.

### C1 — calibration: refusal records

| re-check | command | observed |
|---|---|---|
| case population | `len(json.load(open('.ufo/waves/round-86/controls/c1-cases-r86.json'))['cases'])` | `75` (counter `CASES = 75`) |
| carried set | compare `cases[:72]` of the r86 control with the r85 control `cases` | `True` (`carried=72/72` holds as population equality) |
| flood ceiling | count refusal and non-refusal cases | `27` refusal, `48` non-refusal: the flooding tool's maximum is exactly the printed `flooding=48/75` |
| vocabulary and mutants | AST literal count | `CAUSE_VOCAB 10`; `MUTATIONS 51` (= `mutants=51`) |
| tool bytes | `sha256sum tools/mado-barfoot.py`; `git show master:tools/mado-barfoot.py \| sha256sum` | both `62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5` = receipt `tool_sha256` |
| counter and tool unchanged since the measured revision | `git diff --stat 3afdb713 500bef3c -- quality/counters/c1-r86-refusal-records.py tools/mado-barfoot.py` | empty |
| verdict receipt | `.ufo/waves/round-86/receipts/final-c1-r86.txt` | `cases=75 correct=75 mutants=51 killed=51 base_correct=75/75 carried=72/72 tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=TARGET_MET rev=3afdb713…`, rc 0 |
| self-test | `receipts/selftest-c1-r86.txt` | `127/127`, rc 0 |

The held-rule control is faithful to its source: `c1-r86.held_ok()` reproduces
`quality/counters/c1-r85-identity-causes.py::expected_ok` for refusal cases (`"ERROR (stage=%s " in stdout`
and `" cause=%s " in stdout`, rc pinned). **C1: re-measured at population level, evidence-verified at
the verdict level. Claim verifies.**

### C2 — operability: clause observation

| re-check | command | observed |
|---|---|---|
| case population | r86 control list | `37`; first 36 equal the r85 list (`True`); new case `border-size-int` |
| mutant population | AST literal count | `MUTATIONS 37` (= `mutants=37 killed=37`) |
| verdict receipt | `receipts/final-c2-r86.txt` | `cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37 clauses_observed=37/37 mutants=37 killed=37 verdict=TARGET_MET rev=8528dfa6… tree=bound`, rc 0 |
| before-state | `receipts/control-held-rule-r86.txt` (the r85 instrument run over the 36-case set) | `matched=36/36 mutants=37 killed=33 verdict=TARGET_MISSED`; survivors `regex-anchor-dropped`, `line-anchor-prefix`, `negatives-skipped`, `samples-skipped` |
| self-test | `receipts/selftest-c2-r86.txt` | `114/114`, rc 0 |
| witness row, read from bytes | `border-size-int`: `kind=regex`, `value="[0-9]+"`, `anchor: line`; negatives `0 extra`, `-1`, `0`(rc 127) | as stated |
| **the held rule on that witness** | import `quality/counters/c2-r85-status-classes.py` and call its own `case_correct()` on the case | frozen output `True`; negatives `0 extra`, `-1`, `0` all **refused**; samples `1`, `2` **accepted**: the held rule scores the witness **1/1** |

**Refutation (routed as R1).** The report's before/after table and `SCORECARD.md` §Round86 C2 cite
`held rule on the new witness = 0/1`. That figure is produced by the lane's *model*,
`c2-r86-clause-observations.py::held_case_correct()` (`:574-593`), which passes `anchor` nowhere, not by
running the held round-85 counter. The real round-85 counter routes `anchor == "line"` through
`line_anchored()` (`c2-r85-status-classes.py:369-380`, `case_correct` at `:509-513`) and scores the
witness 1/1. The lane's own selftest asserts the false model (`c2-r86-clause-observations.py:736-737`).
The lesson `corpus/lessons/round-86.md` does not mention the figure, so nothing in the lane marks it.

The refutation does not touch the frozen C2 predicate: the declared kill rule (`matched`, `shapes`,
`clauses_observed`, `kills`, `tree=bound`) is measured by the mutant machinery, not by
`held_case_correct`, and the 33/37 → 37/37 delta is measured by running the frozen instruments. So
**C2 verifies as declared.** The defect is a false control figure presented as measured evidence in an
admitted knowledge entry (§5, quality).

### Harm watch (no axis harmed inside the exercised scope)

`receipts/final-gate-r86.txt` `MADO_SELFTEST: 460/460`; `final-index-r86.txt` `107/107 missing=0
dangling=0 duplicates=0`; `final-ledger-r86.txt` `population=158 ledger_rows=158 uncovered=0
bad_pointer=0`; `final-axis-r86.txt` `checked=3 mismatched=0`. Independent counts:
`git ls-tree 237ecf4e~1 corpus/knowledge/ | wc -l` → `106`, at tip → `107`;
`git show <rev>:corpus/SOURCES.md | grep -c '^| S[0-9]'` → `425` at base and at `237ecf4e~1`, `427` at tip.
The census command (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`)
exits `0`, with the standing `W04` duplicate-URL warnings unfiltered.

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | improved | C1 is the declared calibration claim; refusal-record rule refuses the all-cause flood (`flooding 75/75 → 48/75`) while the honest tool stays `75/75`. Named limits stand (four forgery classes at `75/75`, own-cause echo). The lane's instrumented calibration sub-score (`86/86`) does not move; the critic's label dissent is on record |
| operability | improved | C2 is the declared operability claim; clause observation `37/37`; mutants killed `33/37 → 37/37`; standing gate `460/460` unchanged |
| coverage | unchanged | no coverage claim was declared; the new entry is lane-internal instrument ground (the report's own domain-share line: 0 new tools, 0 new surfaces). Corpus growth is graded under expansion |
| depth | unchanged | no depth claim |
| freshness | unchanged | no freshness claim; the quote correction (`e2d7f63a`) is inside the round's own evidence |
| adjacency | unchanged | connector seat found no kumitate/tameshi acquisition; `PROVINCE.md` unchanged |

## 4. Discernment spot-check

Sources re-opened live at 2026-11-05. Both pins reproduce the live bytes exactly (sha256 equal), so no
Gitiles decoding was needed.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S491 — RFC 7493 §2.3, line 159, 12,849 B, sha256 `a44ccf14…` | admit | `https://www.rfc-editor.org/rfc/rfc7493.txt` (live: 12,849 B, sha256 `a44ccf1451a7bf4f4bbb78b39e10ed0e9a27ff2ee5b639c6458042b5a7197062`, identical); pin bytes 6364–6437 | **agree** | line 159 is "Objects in I-JSON messages MUST NOT have members with duplicate names." under the §2.3 heading at line 157; a MUST NOT, which is what the refusal ground needs |
| S492 — CPython v3.14.8 `re.rst` `fullmatch`, line 957, 78,262 B, sha256 `d252cc18…` | admit | `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/re.rst` (live: 78,262 B, sha256 `d252cc185dfc1014e1b4a8087b2515b71c76527f0f2f6dfddba9a880537e6a48`, identical); directive at line 955 | **agree** | line 957 is "If the whole *string* matches the regular expression *pattern*, return a corresponding :class:`~re.Match`." (13 words, within the 25-word bound); whole-string semantics is the `anchor: line` claim |
| "RFC 8259 alone grounds a duplicate-name refusal as a specification constraint" | reject | `https://www.rfc-editor.org/rfc/rfc8259.txt` line 322 (§4): "The names within an object SHOULD be unique." | **agree** | a SHOULD; a refusal citing only RFC 8259 over-claims. The reject's flip (an I-JSON-mandated surface) is exactly S491 |
| "the two anchor survivors were killed by the anchor branch" | reject | `corpus/lessons/round-85-verifier-spotcheck.md` R1; `c2-r85-status-classes.py` `version` / `omarchy-version` values `^[0-9]+\.[0-9]+\.[0-9]+$` | **agree** | the frozen patterns already carry `^`/`$`, so dropping the branch changed nothing on them; the flip (an unanchored pattern bound to an `anchor: line` row, with a negative proving the difference) is the `border-size-int` row that landed |

Score: 2 admits and 2 rejects sampled, **4/4 agreement**. The agreement covers the admit/reject
decisions the trend measures. It does not cover the lane's control figure (R1), which is a separate
defect of the gate's own measurement and is routed as such.

## 5. Trend verdicts

- **expansion — improved.** `SOURCES.md` 425 → 427 rows (both new rows `mined`, tier A, opened
  2026-11-04, located quotes verified live); `corpus/knowledge/` 106 → 107 files; index gate `107/107`.
  The growth is lane-internal instrument ground, not new desktop surface, and is graded as such.
- **quality — harmed.** LEARNING.md's harmed condition is "an entry is found false or stale and left
  unmarked". `corpus/knowledge/refusal-records-clause-observations-r86.md` §3 and `SCORECARD.md` §Round86
  present `held_rule_new_case=0/1` as a measured control on the new witness; re-running the held rule
  gives `1/1` (§2). The entry is admitted, the false figure is unmarked in the lane's repo at closure,
  and the lesson's routed table does not carry it. The lane's measured quality gains (the record rule,
  the clause observation) are real and re-verified; the trend is graded on the false entry because the
  learning path makes that the harmed condition. Cure: a named correction appended in the lane's next
  round (R1).
- **discernment — improved.** The outside spot-check agrees with the gate on 2 admits and 2 rejects
  (4/4), the source rows re-derive from live bytes, and the round closed two r85 routed defects
  (population; substring test) with measured controls. The R1 control error is a measurement defect of
  the gate, routed; it is recorded here, not counted as a discernment agreement.

Because expansion is improved and quality is harmed, LEARNING.md's trade rule applies: the round is
reported as a trade and is not admitted. No axis is harmed, so the verdict is an honest stop, not a
harm rejection. The operator may rule otherwise; the rule is the protocol's.

## 6. Routed defects — mado owns the correction (next round)

1. **R1, medium — the false control.** Replace `held_case_correct()` with a call into the held
   round-85 counter's own `case_correct()` (or print the figure as a labelled model, never as
   measured), add a selftest that pins the held model against that counter over the held set and the
   new witness, and append a correction to `SCORECARD.md` §Round86 and
   `corpus/knowledge/refusal-records-clause-observations-r86.md` §3 naming the superseded sentence.
   Once the correction lands, this quality grade is re-graded by a closure-correction.
2. **R2, medium — no stored baselines.** Neither `c1-r86-refusal-records.py` nor
   `c2-r86-clause-observations.py` compares its control JSON against a stored digest: both print
   `sha256` of the control file and assert nothing about it. A frozen instrument needs an
   `expected.json` digest pin (PROTOCOL §Gate standard, *Two evidences*). The r87 plan covers the
   counter's own bytes (`counter_sha256`) only.
3. **R3, low.** `.ufo/waves/round-86/controls/c2-cases-r86.json` carries `"round": 85`, and its metadata
   says `superseded: 15`, while the scored run prints 16 superseded names.
4. **R4, low — report filing.** The report was rewritten in place (`932d6067`) where the protocol
   requires an erratum appended after the filed bytes; the first filing (`78b3faab`) preceded the commit
   it cites.
5. **R5, low — attack-count definition.** LOG.md's settlement line counts the policy set
   (reviewer 2, critic 1, mutation-tester 1 = `4/14`, 28.6 %); the report counts five (adds sentinel,
   `5/14`, 35.7 %). Both clear ≥25 %; the definition should be one.
6. **R6, low.** `c1-r86-refusal-records.py` docstring still reads `mutants=53 killed=53` against
   `MUTANTS = 51` (self-named M86-6; correctly left frozen and routed).
7. **R7, medium (carried, lane-routed).** The record rule still scores four forgery classes `75/75`
   (stderr flood, one-leading-space duplicate, result-path flood, homoglyph flood); the own-cause echo
   exempts the record's own cause by identity, not position (`w1/R86ReviewerC1.md`,
   `w1/R86CriticClaims.md` §(a)).
8. **R8, medium (carried, lane-routed).** A count-preserving stub still passes case-level clause
   observation (`w1/R86ReviewerC2.md` F1/F2): the observation counts calls, not evaluations.

## 7. Notes for the operator

`SHONEN.md` boxes 1–4 look checkable by a non-author from the pointers the report cites (the
SKILL.md runbook tables at `:231` and `:301`, registry rows `SKILL.md:859-860`, `LOG.md:4273-4280`, the
declaration's counting commands, `PROVINCE.md` unchanged). Promotion stays operator-owned; nothing here
writes `[x]`.
