author: hyaku closure (non-author integrator, @m_zfl)

# mado round 86 — verifier spot-check (non-author)

Round report `.ufo/reports/round-86/mado.md`; lane repo `mado-shokunin`; lane HEAD at closure
`500bef3c8782788b1e3b327845a3a0694b8594fe`; round base `a722c60493f24f83429112e9123058835b2cdd82`;
declaration/instrument freeze `237ecf4e69a4986108f719f3beeafe111adaa033`. I did not author this
round. Every command below was run by me against committed bytes at the tip; the receipts quoted are
the lane's committed files, cited rather than re-typed from the report.

## 1. Conformance (step 1)

| item | command | observed | result |
|---|---|---|---|
| report landed by the lane identity | `git log --format='%an %ae %H %ci' -- .ufo/reports/round-86/mado.md` | `mado-shokunin mado@shokunin.local 932d6067… 2026-11-05 00:40:16 -0300` (earlier filing `78b3faab… 00:38:37`) | pass |
| `SHONEN` heading, one line per box | `grep -n '^## SHONEN' .ufo/reports/round-86/mado.md`; `grep -c '^- \[' SHONEN.md` | heading present; report carries 4 `[~]` lines; `SHONEN.md` has 4 boxes; no `[x]` written | pass |
| cited lane commits exist and are ancestors | `for h in …; do git cat-file -e $h^{commit} && git merge-base --is-ancestor $h master; done` | `f72bba01 237ecf4e 01be4234 b33afc08 3afdb713 8528dfa6 78baa05a e2d7f63a b24b03aa e6b72872 500bef3c 2b6dd76b a722c604` all `exists ancestor-of-master`; `d7ffa762` too (unlisted in the report table) | pass |
| no uncommitted round work, pushed | `scripts/hyaku/jj-lane.sh state mado-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 … tracked=0 untracked=0`; status empty; remote `500bef3c… refs/heads/master` | pass |
| prompt carries the contract | `.ufo/prompts/mado-round-86.md` | §1 mission/axes binding, §3 L2 floor (≥8, one batched call) + route-table deferral, §4 report path and required sections incl. `SHONEN`, §5 commit-then-push, push scope, L0 side channel; addendum §write-scope (`:448`), report-lands-last and hash-citation rule (`:516-519`) | pass |
| L2 route map vs `MISSION.md` bucket | `sed -n '53,66p' MISSION.md` | `MISSION.md` §L2 = ≥8 lanes, one batched call, role-class buckets; the prompt defers to the host route table (§3) and its historical alias lines are dated operator directives | pass |
| wave shape | `w1-results.json`, `w1/` | `seats=14`, 14 result rows, 0 empty outputs, 14 seat reports; roles executor 3 / scribe 3 / scout 2 / reviewer 2 / critic 1 / mutation-tester 1 / sentinel 1 / connector 1; attack 5/14 = 35.7 % ≥ 25 %; connector 1 ≤ 2 | pass |

**Conformance defects (status-neutral, routed below):** the report was rewritten in a second commit
instead of an appended erratum (`git show --stat 932d6067` → 228 insertions / 149 deletions over the
same file); the first filing (`78b3faab`, 00:38:37) preceded the lane commit it now cites
(`500bef3c`, 00:38:55); the `Landed changes` table omits `d7ffa762`.

## 2. Per-claim re-check

Both claims rest on lane-owned counters. Per `PROTOCOL.md` §Gate standard (Closure consequence) I
verified their **committed evidence** and did not execute either counter. What I re-derived myself is
the population arithmetic and the tool bytes behind each verdict.

### C1 — calibration: refusal records

| re-check | command | observed |
|---|---|---|
| case population | `python3 -c '…len(json.load(open(".ufo/waves/round-86/controls/c1-cases-r86.json"))["cases"])'` | `75` (matches `CASES = 75`) |
| carried set | compare `cases[:72]` of the r86 control against the r85 control list | `first 72 of r86 == r85 cases: True` (`carried=72/72`) |
| flood ceiling | count refusal vs non-refusal cases | `refusal cases 27 non-refusal 48` → the flood's maximum under the record rule is exactly the `flooding=48/75` the receipt prints |
| vocabulary | AST count of `CAUSE_VOCAB` / `MUTATIONS` | `CAUSE_VOCAB 10`, `MUTATIONS 51` (matches `mutants=51`) |
| tool bytes | `sha256sum tools/mado-barfoot.py` | `62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5` = the receipt's `tool_sha256` and `base_sha256` |
| re-runnable at the tip | `git diff 3afdb713 500bef3c -- quality/counters/c1-r86-refusal-records.py tools/mado-barfoot.py` | empty |
| verdict receipt | `.ufo/waves/round-86/receipts/final-c1-r86.txt` | `cases=75 correct=75 mutants=51 killed=51 base_correct=75/75 carried=72/72 tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=TARGET_MET rev=3afdb7136904b70b0a01ac31963b6e9b14320f1f` |
| control | `receipts/control-c1-r86.txt` | same numbers with `--no-mutants` (`verdict=MUTANTS_SKIPPED`, kill clause not claimed) |

The held-rule control is faithful: `c1-r86`'s `held_ok()` reproduces
`quality/counters/c1-r85-identity-causes.py::expected_ok` (`"ERROR (stage=%s " in stdout` plus
`" cause=%s " in stdout`, rc pinned). **C1: re-measured (population arithmetic, carried set, flood
ceiling, tool bytes) and evidence-verified (counter run). Claim verifies.**

### C2 — operability: clause observation

| re-check | command | observed |
|---|---|---|
| case population | control list length | `37`; `first 36 of r86 == r85: True`; new case `border-size-int` |
| mutant population | AST count of `MUTATIONS` | `37` (matches `mutants=37 killed=37`) |
| verdict receipt | `receipts/final-c2-r86.txt` | `MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37 clauses_observed=37/37 … mutants=37 killed=37 verdict=TARGET_MET rev=8528dfa665fbf34cf3c671cd683098c95d9b1637 tree=bound` |
| before-state | `receipts/control-held-rule-r86.txt` (the r85 counter, 36-case set) | `cases=36 executed=36 matched=36 … mutants=37 killed=33`, survivors `regex-anchor-dropped`, `line-anchor-prefix`, `negatives-skipped`, `samples-skipped` |
| witness row | `border-size-int` in the r86 control set | `kind=regex`, `value="[0-9]+"`, `anchor: "line"`, negatives `0 extra` / `-1` |
| the held rule on that witness | load `quality/counters/c2-r85-status-classes.py` and call its own `case_correct()` on the case | frozen `True`; negatives `0 extra`, `-1`, `0` all **refused**; samples `1`, `2` correct → **1/1, not 0/1** |

**Refutation (routed as R1 below).** `c2-r86-clause-observations.py::held_case_correct()`
(`:574-593`) models the held rule as "a regex row is a substring search even where it declares
`anchor: line`". The actual round-85 counter does not: `case_correct()` (`:509-513`) passes
`case.get("anchor")` into `special_matches()` → `matches()`, which routes `anchor == "line"` through
`line_anchored()`. Measured, the held rule scores the new witness 1/1. So
`held_rule_new_case=0/1` — repeated in `SCORECARD.md` §Round86 C2 row, in
`corpus/knowledge/refusal-records-clause-observations-r86.md` §3, and asserted as a selftest at
`c2-r86-clause-observations.py:736` — is false. It does not weaken the claim's measured delta
(`33/37 → 37/37` kills, `37/37` clause populations), which the mutant machinery computes without
`held_case_correct`; it overstates how much the witness discriminates the new rule from the held
one. **C2: evidence-verified, with one control cell refuted. Claim verifies as declared; the frozen
declaration's predicate does not include this control.**

### Harm watch (locked axes)

`receipts/final-gate-r86.txt` `MADO_SELFTEST: 460/460`; `final-index-r86.txt` `107/107 missing=0
dangling=0`; `final-ledger-r86.txt` `population=158 ledger_rows=158 uncovered=0 bad_pointer=0`;
`final-axis-r86.txt` `checked=3 mismatched=0`; `selftest-c1/c2` `127/127`, `114/114`. Independent
counts: `git ls-tree 237ecf4e~1 corpus/knowledge/ | wc -l` → `106`, at tip → `107`; `git show
<rev>:corpus/SOURCES.md | grep -c '^| S[0-9]'` → `425` at base and at `237ecf4e~1`, `427` at tip.
No owned axis is harmed inside the exercised scope.

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | improved | `corpus/knowledge/` 106 → 107 files; `SOURCES.md` 425 → 427 rows; the new entry opens on `S491`/`S492` ground the corpus did not hold |
| operability | improved | clause observation `37/37`; mutants killed `33/37 → 37/37`; standing gate `460/460` unchanged |
| calibration | improved (bounded) | the refusal rule now refuses the all-cause flood (`75/75 → 48/75`) while the honest tool and the held tool both stay `75/75`; named limits remain (four forgery classes at `75/75`, own-cause echo). The lane's instrumented calibration sub-axis (`86/86 resolved-active`) does not move; the critic's axis-label dissent is on record |
| depth | unchanged | no depth claim this round; the new entry is graded under coverage/expansion |
| freshness | unchanged | no freshness score claim; the quote correction (`e2d7f63a`) lands inside the round's own evidence |
| adjacency | unchanged | connector seat found no kumitate/tameshi acquisition; `PROVINCE.md` unchanged |

## 4. Discernment spot-check

Sources re-opened live from the network at 2026-11-05; both pins reproduce the live bytes exactly
(`sha256` equal), so no base64/Gitiles decoding was needed.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S491 — RFC 7493 (I-JSON) §2.3, line 159, 12,849 B, sha256 `a44ccf14…` | admit | `https://www.rfc-editor.org/rfc/rfc7493.txt` (live fetch: 12,849 B, sha256 `a44ccf14…`); pin `.ufo/waves/round-86/fetch/S491.bin` bytes 6364–6437 | **agree** | line 159 reads exactly "Objects in I-JSON messages MUST NOT have members with duplicate names."; §2.3 at line 157 as the row says; a MUST NOT, so the refusal ground is stronger than S486's SHOULD |
| S492 — CPython v3.14.8 `Doc/library/re.rst` `fullmatch`, line 957, 78,262 B, sha256 `d252cc18…` | admit | `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/re.rst` (live fetch: 78,262 B, sha256 `d252cc18…`); pin bytes 39792–39901 | **agree** | line 957 is verbatim "If the whole *string* matches the regular expression *pattern*, return a corresponding :class:`~re.Match`." (13 words, ≤25); the `fullmatch` directive sits at line 955; the quote is whole-string semantics, exactly the `anchor: line` claim |
| "RFC 8259 alone grounds a duplicate-name refusal as a specification constraint" | reject | `https://www.rfc-editor.org/rfc/rfc8259.txt` §4, line 322; `SOURCES.md` S486 row | **agree** | RFC 8259 says "The names within an object SHOULD be unique" — a SHOULD; a refusal citing it alone over-claims, and the reject's flip (an I-JSON-mandated surface) is exactly S491 |
| "the two anchor survivors were killed by the anchor branch" | reject | `corpus/lessons/round-85-verifier-spotcheck.md` R1; `c2-r85-status-classes.py::line_anchored`; the `version` / `omarchy-version` control values `^[0-9]+\.[0-9]+\.[0-9]+$` | **agree** | the frozen patterns already carry `^`/`$`, so dropping the branch changes nothing on them; the reject's flip condition (an unanchored pattern bound to an `anchor: line` row) is the `border-size-int` row that landed |

Scored 2 admits + 2 rejects, 4/4 agreement. The lane's own gate did miss the R1 mis-model below —
agreement on the rows sampled does not certify the whole gate.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → `exit=0`,
`mado ok …/mado-shokunin/corpus/SOURCES.md`, warnings only (standing `W04` duplicate-URL set;
`W01 S277 tierC mined`).

## 5. Trend verdicts

- **expansion — improved.** `SOURCES.md` 425 → 427, `corpus/knowledge/` 106 → 107, index gate
  `107/107`; the admitted entry's `source:` cites both new rows, both `mined`, on ground the
  coverage map did not hold.
- **quality — unchanged** (the lane graded `improved`; I disagree, reasons on record). The
  instruments are stronger, but that is graded on operability/calibration; no weaker entry was
  superseded and no stale entry was re-verified, and the round's new entry carries a figure this
  check refuted (R1). Not `harmed` only because the refutation is now marked and routed rather than
  left standing.
- **discernment — improved.** Outside agreement on 2 admits and 2 rejects, both source rows
  re-derivable from live bytes, and the round closed two r85 routed defects (`R1` population, `R2`
  substring) with measured controls. Marked limit: the mis-modelled held rule survived 5 attack
  seats and the lane's own selftest.

## 6. Routed defects — mado owns the correction

1. **R1, medium.** `c2-r86-clause-observations.py::held_case_correct()` omits the anchor handling the
   held r85 counter implements, so `held_rule_new_case=0/1` is false (measured 1/1). Fix: pass
   `case.get("anchor")` through the held model, or relabel it as a strawman and print it as such;
   re-derive the `border-size-int` narrative; add a selftest that pins the held model against
   `c2-r85-status-classes.py::case_correct` over the held 36-case set; correct `SCORECARD.md`
   §Round86 and `corpus/knowledge/refusal-records-clause-observations-r86.md` §3 by appended
   correction.
2. **R2, medium.** Neither new gate ships an `expected.json` digest pin (`PROTOCOL.md` §Gate
   standard, *Two evidences*): the counters print the control-file `sha256` but assert no stored
   baseline, so an edited control set is re-blessed rather than reported `snapshot_tampered`. The
   r87 plan covers `counter_sha256` only; the control-set pin is not covered.
3. **R3, low.** `.ufo/waves/round-86/controls/c2-cases-r86.json` carries `"round": 85`,
   `"cases_added": 3` and `superseded: 15` while it holds 37 cases and the run prints 16 superseded
   names.
4. **R4, low.** The report was rewritten in place (`932d6067`: 228 insertions / 149 deletions) where
   the protocol requires an erratum appended after the filed bytes; the first filing also preceded
   the commit it cites.
5. **R5, low.** `Landed changes` omits `d7ffa762` (battery receipts + cleanup record); `LOG.md`
   wave settlement says "four attack seats (28.6 %)" where the report counts five (35.7 %).
6. **R6, low.** `c1-r86-refusal-records.py` docstring still prints `mutants=53 killed=53` against
   `MUTANTS = 51` (self-named M86-6, correctly left frozen and routed).
7. **R7, medium (carried, lane-routed).** The record rule still scores four forgery classes
   `75/75` (stderr flood, one-leading-space duplicate, result-path flood, homoglyph flood) and an
   own-cause echo exempts the record's cause by identity rather than position; r87 controls exist in
   `w1/R86ReviewerC1.md` and `w1/R86CriticClaims.md`.
8. **R8, medium (carried, lane-routed).** A count-preserving stub still passes case-level clause
   observation (`w1/R86ReviewerC2.md` F1/F2): the observation counts calls, not evaluations.

## 7. Notes for the operator

`SHONEN.md` boxes 1–4 look fully checkable by a non-author from the pointers the report cites
(`SKILL.md:231`/`:301` tables and registry rows at `SKILL.md:859-860`, `LOG.md:4273-4280`, the two
declaration counting commands, `PROVINCE.md` unchanged). Promotion stays operator-owned; nothing here
writes `[x]`.
