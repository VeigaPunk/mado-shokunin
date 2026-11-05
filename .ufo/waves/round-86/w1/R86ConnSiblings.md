# R86ConnSiblings — cross-instrument overlap scan

Axes: **calibration (C1)** and **operability (C2)**. This is evidence and one bounded successor proposal, not an admission decision. No instrument, control, declaration, application file or sibling report was changed.

## Scope and method

All counter paths below are absolute. Function spans count physical lines inclusively from `def` through the AST node's last statement; comments/blank lines inside that span count. “Carried” means AST-identical, ignoring source locations; changed docstrings count as changes. `Setup` is a class, listed separately for completeness. Nested functions are included. File totals: C1 584→674 (+90), C2 857→962 (+105). No function/class was removed.

Read-only `git show` comparison against 237ecf4e69a4986108f719f3beeafe111adaa033: both r85 files and the r86 C2 file are byte-identical to the freeze. The observed r86 C1 file differs **only** in module-docstring line 15: frozen `mutants=53 killed=53`, observed `mutants=51 killed=51`. All function bodies/spans are unchanged. This is a real frozen-prose discrepancy, not an executable change; disclosed repair pointer: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/receipts/instrument-repair-r86.md:47–58. The runs below use the observed instrument paths and extract tool content at the named freeze; do not call the C1 instrument byte-identical to the freeze.

## 1. Complete function inventory

### /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r86-refusal-records.py

Compared with /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r85-identity-causes.py.

| Function/class | Classification | r85 span (lines) | r86 span (lines) |
|---|---|---|---|
| `Setup` | carried | 201–202 (2) | 220–221 (2) |
| `sha256` | carried | 205–206 (2) | 224–225 (2) |
| `run` | carried | 209–226 (18) | 228–245 (18) |
| `parse_result` | carried | 244–261 (18) | 263–280 (18) |
| `parse_attr` | carried | 264–266 (3) | 283–285 (3) |
| `case_files` | carried | 269–303 (35) | 288–322 (35) |
| `parse_refusal_records` | added | — | 325–327 (3) |
| `expected_ok` | changed | 306–332 (27) | 330–364 (35) |
| `held_ok` | added | — | 367–379 (13) |
| `run_cases` | changed | 335–357 (23) | 382–404 (23) |
| `apply_mutation` | carried | 360–364 (5) | 407–411 (5) |
| `selftest` | changed | 367–442 (76) | 414–507 (94) |
| `selftest.ok` | changed | 370–376 (7) | 417–423 (7) |
| `extract` | carried | 445–449 (5) | 510–514 (5) |
| `resolve` | carried | 452–457 (6) | 517–522 (6) |
| `main` | changed | 460–580 (121) | 525–670 (146) |

### /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r86-clause-observations.py

Compared with /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r85-status-classes.py.

| Function/class | Classification | r85 span (lines) | r86 span (lines) |
|---|---|---|---|
| `Setup` | carried | 191–192 (2) | 212–213 (2) |
| `sha256` | carried | 195–196 (2) | 216–217 (2) |
| `run` | carried | 199–248 (50) | 220–269 (50) |
| `git_bytes` | carried | 251–258 (8) | 272–279 (8) |
| `git_show` | carried | 261–262 (2) | 282–283 (2) |
| `split_cells` | carried | 265–282 (18) | 286–303 (18) |
| `command_rows` | changed | 285–306 (22) | 306–311 (6) |
| `section_rows` | added | — | 314–334 (21) |
| `type_ok` | carried | 309–324 (16) | 337–352 (16) |
| `fields_ok` | carried | 327–333 (7) | 355–361 (7) |
| `json_text` | carried | 336–340 (5) | 364–368 (5) |
| `status_ok` | carried | 343–356 (14) | 371–384 (14) |
| `line_anchored` | carried | 359–366 (8) | 387–394 (8) |
| `matches` | changed | 369–476 (108) | 397–507 (111) |
| `special_matches` | carried | 479–506 (28) | 510–537 (28) |
| `case_correct` | changed | 509–523 (15) | 540–571 (32) |
| `case_correct.okay` | carried | 510–513 (4) | 550–553 (4) |
| `held_case_correct` | added | — | 574–593 (20) |
| `held_case_correct.okay` | added | — | 577–583 (7) |
| `observed` | carried | 526–528 (3) | 596–598 (3) |
| `selftest` | changed | 531–679 (149) | 601–769 (169) |
| `selftest.ok` | changed | 534–540 (7) | 604–610 (7) |
| `main` | changed | 682–853 (172) | 772–958 (187) |

C1 changes: parsed-record/foreign-vocabulary refusal rule; explicit held-rule control; injectable scoring callback; added selftest witnesses; flooding/held controls and revised final predicate in main. New globals: `CAUSE_VOCAB`, `REFUSAL_RE`.
C2 changes: union of two runbook sections; observed sample/negative/live-anchor clauses; explicit held-rule witness; expanded selftest and final observation accounting. New globals include `SECTIONS`, `NEW_CASE`, `OBS`, `LIVE`. `SUPERSEDED`/`STATUS_FIELDS` remain permissive carry-forward policy, not byte-equality checks of each case.

## 2. Dead, duplicated and case-unreachable logic

Method: Python AST Name-load references plus call-graph inspection, JSON case/field-type census, one concurrent `python3 -I -m trace --count --summary` run per counter, and a pure in-memory refusal diagnostic. No absent call is inferred merely from a missing live desktop response. Trace does **not** cover spawned interpreters, and without `--missing` its displayed 100.0% is not total branch coverage. C2's run exited during setup, so its matcher reachability conclusions below are explicitly static, not dynamic coverage claims.

- **No unreferenced top-level function/class** in either r86 module. `main` is called by the script guard; `selftest` is reachable only with its flag. Closures are invoked locally. Control-only `held_ok` and `held_case_correct` are not dead: main calls them for the flooding/new-witness comparisons.
- **New dead constant:** /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r86-refusal-records.py:37 `BASE_EXPECT = 62` has zero Name-load references. r85 read it in its predicate; r86 deliberately changed the base to a printed observation but retained the stale constant.
- **Inherited dead constant:** /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r86-clause-observations.py:198 `EXACT_KINDS` has zero Name-load references (also unused at r85 line 182). `SHAPE_KINDS` is read for counting; do not confuse the two.
- **Case-unreachable shape branch:** C2 `matches`, lines 407–408, `kind == "contains"` has no member in the 37-case control set. The 17 actual kind populations are regex6, empty1, int4=1, exact8, int_range5, sorted_unique1, json_object_fields1, levels_dump1, array_fields1, refusal4, lines_shape2, chord_shape1, is_active1, action_column1, pid_state1, bool_property1, producer_failure1. This is dormant under the frozen population, not proof it is globally impossible.
- **Case-unreachable type branch:** C2 `type_ok`, lines 344–345, `nonneg_int` is not requested by any frozen schema or the direct `int4` call; schema types are int1, str2, positive_int2, int4=1, number1. Unknown-kind/type exceptions are input-validation paths, not dead code merely because valid controls never request them.
- Normal scoring never enters CLI `--selftest`, `--no-mutants`, malformed-population/scratch/anchor failure paths; these remain intentional alternate/error paths. C2 did enter its working-tree mismatch branch in this seat's run. No exhaustive branch-coverage or untested-timeout claim is made.
- **Duplicated infrastructure:** `sha256` is identical in both r86 modules (2 physical lines each). Both `run` functions implement byte decoding, timeout→124 and OSError→Setup, but their environment contracts differ materially: C1 isolates environment; C2 forwards desktop/session variables and discovers Hyprland/Omarchy. Consolidating those runners naively would harm runtime isolation or live operability.
- **Intentional duplicated historical judgement:** C1 `held_ok` reproduces r85 stage/cause substring scoring as a control; C2 `held_case_correct` duplicates sample/negative loops while deliberately using unobserved substring regex matching. Their different rules are declared controls, not accidental second production conventions. Repair history documents why mutation anchors must not hit those control-only loops: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/receipts/instrument-repair-r86.md:37–42.

## 3. Routed r85 defects R1–R7

| Defect | Disposition and exact boundary | Code/receipt pointer |
|---|---|---|
| R1 | **Closed for the declared 37-mutant population on cached evidence**, not independently re-scored by this seat: clause observations and the unanchored new witness discriminate the four prior survivors. | /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r86-clause-observations.py:409–413,540–571; /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/receipts/c2-repaired-r86.txt; /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/receipts/instrument-repair-r86.md:9–42 |
| R2 | **Closed for the declared C1 flood/cause witnesses**, independently observed 75/75, 51/51, flood48/75 vs held75/75; not universal cause authentication: 14/27 refusal cases still omit cause expectations, while the new alloc-negative-cause witness binds the previously missing token. | /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r86-refusal-records.py:325–379,623–656; /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/controls/c1-cases-r86.json |
| R3 | **Open**, with honest declared limits: numeric exact/signal status does not authenticate termination cause, and Markdown prose cells remain unbound. | /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r86-clause-observations.py:371–384; /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/claims-declaration-r86.md:139–140 |
| R4 | **Open**: QUALITY145 is a criterion, not an instrument binding claim publication to non-null telemetry. | /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-86.md:47–48,110–113; /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/claims-declaration-r86.md:137–138 |
| R5 | **Closed as correction-pointer retention**, not a fresh runtime fix; preserve the already-landed supersession, never repeat the obsolete sentence. | /home/vgpnk/Projects/shokunin/mado-shokunin/LOG.md:4191–4196; /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-86.md:49 |
| R6 | **Partially closed**: new declaration uses pinned S491 §2.3/line159 and S492 fullmatch/line957; source seat corroborates locators. This does not establish recovery of the old unreachable GNU endpoint. | /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/claims-declaration-r86.md:122–129; /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/w1/R86ScribeSources.md:38–51 |
| R7 | **Partially closed/evidence pending**: this seat used and removed its lane/seat subtree; lesson asserts L1 uses its own subtree but the promised cleanup-r86.json was absent in this seat's receipt listing. Do not infer whole-wave cleanup from this seat. | /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-86.md:51; seat commands below |

## 4. Second convention and ONE bounded proposal

**Contradiction, not a scalar score:** the same `MADO_BARFOOT` refusal stream is judged as exactly one prefixed record by C1 (/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r86-refusal-records.py:325–350), but as arbitrary stage-substring membership by C2 (/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r86-clause-observations.py:537). C2's four refusal cases have only rc/stage declarations, no record-count/prefix/foreign-cause observation. C1's calibration improvement therefore does not transfer to the runbook's interpretation of the same tool. This is a maintainability defect for L1, **not a failure of C2's narrower frozen claim**.

Observed pure-function outputs (rc3, model, stage-only expectation):

```text
REFUSAL_DIAGNOSTIC embedded C1= False C2= True
REFUSAL_DIAGNOSTIC duplicate C1= False C2= True
REFUSAL_DIAGNOSTIC flood C1= False C2= True
```

**Proposed move (successor only):** declare one versioned refusal-record contract used by both successor counters, with independent expectations for optional cause binding. Keep historical held-rule controls explicitly historical and frozen. The production parser should have one owner rather than copying C1 into C2. Do not modify this round's frozen instruments or use a successor result retroactively.

**Affected axes:** calibration improves by rejecting embedded/duplicate/flooded refusals at the runbook surface; operability is preserved only if every existing honest refusal sample and live row still passes. These are acceptance conditions, not a measured Pareto win yet. No other-axis improvement is claimed.

**Second-order effects / risks:** runtime gets one small in-memory parse per refusal, no new live command or dependency; contract retains rc/stage and optional-cause boundaries (C2's honest stage-only samples must remain valid); substrate must pin/hash the shared parser to the measured revision and resolve it under `python3 -I` without caller-PYTHONPATH dependence; verification must retain distinct C1 tool mutants and C2 clause mutants so shared parser reuse does not become circular evidence. Both entry points require independent embedded/duplicate/flood fixtures. A shared parser is otherwise a common-mode failure risk. The existing C1 foreign-token set subtracts the permitted token globally (line347), rather than tracking its field span; reuse must not be advertised as exact field-span exclusion without a separate declaration/witness.

**Verification for that proposal (not executed implementation):** unchanged current controls must preserve honest C1=75/75, carried72/72, tool selftest152/152 and all51 kills; honest C2=37/37, shapes27, clause counts37 and all37 kills; C2's four refusal rows must reject all three diagnostic classes while accepting current stage-only samples; independently test parser import and byte binding in a freeze snapshot. Hold old rule controls unchanged and separately scored. No source edits are proposed for this frozen wave.

## 5. Executed commands and bounded results

The two trace commands were launched concurrently. Both child scratch trees were removed by EXIT traps; the parent seat directory was removed before handoff. Full C1 stdout contained all75 correct=yes and all51 killed=yes; final output below is the substantive result. C2 did not execute a case because the evolving working tree differs from the measured freeze. No retry was made to reinterpret that observation as a score; cached snapshot evidence is labelled separately above.

```sh
S=/fast/scratch/hyaku/mado-r86/R86ConnSiblings/c1; mkdir -p "$S" && trap 'rm -rf -- "$S"' EXIT && TMPDIR="$S" python3 -I -m trace --count --summary --coverdir "$S/coverage" /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r86-refusal-records.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 237ecf4e69a4986108f719f3beeafe111adaa033 --base-rev 2b6dd76b65de4dfe701db87db13b7e448b3538ee --controls /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/controls/c1-cases-r86.json --carried /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/controls/c1-cases-r85.json --scratch-root "$S"
```

rc0, final stdout:

```text
MADO_R86_REFUSALS: cases=75 correct=75 mutants=51 killed=51 base_correct=75/75 carried=72/72 tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=TARGET_MET rev=237ecf4e69a4986108f719f3beeafe111adaa033 tool_sha256=62626fce852bc5bef263a26ddee78b12c6fc9b2883e41ef55c015becf3a76fb5
```

```sh
S=/fast/scratch/hyaku/mado-r86/R86ConnSiblings/c2; mkdir -p "$S" && trap 'rm -rf -- "$S"' EXIT && TMPDIR="$S" python3 -I -m trace --count --summary --coverdir "$S/coverage" /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r86-clause-observations.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 237ecf4e69a4986108f719f3beeafe111adaa033 --controls /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-86/controls/c2-cases-r86.json --carried /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/controls/c2-cases-r85.json --scratch-root "$S"
```

rc2, exact error stdout before trace's module summary:

```text
MADO_R86_RUNBOOK: ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)
```

Reproduce the pure-function contradiction without editing/importing either module on disk:

```sh
python3 -I - <<'PY'
from pathlib import Path
root = Path('/home/vgpnk/Projects/shokunin/mado-shokunin')
modules = []
for filename in ('c1-r86-refusal-records.py', 'c2-r86-clause-observations.py'):
    path = root / 'quality/counters' / filename
    ns = {'__name__': 'seat_diagnostic', '__file__': str(path)}
    exec(compile(path.read_text(), str(path), 'exec'), ns)
    modules.append(ns)
c1, c2 = modules
case = {'expect': {'error': True, 'rc': 3, 'stage': 'model'}}
outputs = [
    ('embedded', 'prefix ERROR (stage=model fake)\n'),
    ('duplicate', 'MADO_BARFOOT: ERROR (stage=model fake)\n' * 2),
    ('flood', 'MADO_BARFOOT: FLOOD: ' + ' '.join(c1['CAUSE_VOCAB']) +
     '\nMADO_BARFOOT: ERROR (stage=model fake)\n')]
for label, out in outputs:
    print('REFUSAL_DIAGNOSTIC', label,
          'C1=', c1['expected_ok'](case, 3, out),
          'C2=', c2['special_matches']('refusal', {'rc': 3, 'stage': 'model'}, 3, out))
PY
```

No tool was installed or updated. AST and JSON analysis used the existing Python interpreter; no source imports/pycache writes were needed. No git mutation, foreign runtime, subagent dispatch or broad gate was used.

Self-evaluation: accuracy4/5 (C1 frozen docstring differs; disclosed), completeness4/5 (C2 dynamic scoring blocked by tree binding; static scope explicit), clarity4/5 (full inventory makes report long), actionability4/5 (proposal acceptance criteria concrete but implementation intentionally prohibited), conciseness4/5 (commands retained for reproducibility). Mean4.0. Highest-impact improvement is the explicit shared-tool refusal contradiction rather than indiscriminate helper deduplication. User-agreement check: all four assigned scan items are answered, with no frozen repair or admission claim.

Report: .ufo/waves/round-86/w1/R86ConnSiblings.md
