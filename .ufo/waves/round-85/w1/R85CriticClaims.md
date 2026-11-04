# R85CriticClaims — declaration review

Reviewed frozen revision `3905311c75a39c5710413105865c0a1a7dd0116a`, not subsequent working-tree repairs. All counter line numbers below refer to blobs at that revision. No admission, scoring verdict, edits to controls/counters/declaration, git mutations, or other runtime invocation. Axes: coverage (C1), operability (C2); inaccurate declarations additionally affect calibration.

Path key (all absolute):
- D: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/claims-declaration-r85.md`
- C1: `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r85-identity-causes.py`
- C2: `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r85-status-classes.py`
- A: `/home/vgpnk/Projects/shokunin/AXES.md`
- P: `/home/vgpnk/Projects/shokunin/PROTOCOL.md`

## Fixable defects

### 1. Frozen C2 rejects its own declared carried population before measuring
Evidence: D:128-130 allows status/negatives additions; frozen C2:729-737 excludes neither field from its carried comparison. Executed the frozen counter source with the supplied absolute control/carried paths, freeze revision, own scratch root, and `--no-mutants`. Observed exit 2:

`MADO_R85_RUNBOOK: ERROR (stage=setup carried case 'version' changes field 'negatives')`

The working-tree counter now includes STATUS_FIELDS in this comparison, but those bytes are not the frozen counter. Impact: operability/calibration. Smallest correction: carry the explicitly declared status/negative additions in the comparison; identify the corrected counter revision rather than attributing the repair to the frozen blob.

### 2. Carried-field exemption is wider than the declaration
Evidence: frozen C2:730 unconditionally exempts `skill_anchor` for every carried case; C2:66 exempts `argv` for `omarchy-version`. D:128-130 permits argv/skill_anchor supersession only for the fifteen round-84 names; omarchy-version is not one of them. Pure allowlist checks observed `configerrors.skill_anchor` and `omarchy-version.argv` both allowed. These holes persist even after adding STATUS_FIELDS. Impact: operability/calibration; an unchanged carried-case identity can acquire an undeclared command/anchor intervention. Smallest correction: remove global skill_anchor exemption and grant omarchy-version only value/anchor changes, retaining the fifteen named command exceptions.

### 3. Junk runbook status/outcome cells are invisible to the counter
Evidence: C2:287-308 extracts only command cells; C2:761-782 binds those cells to case argv, not the row's status/outcome. A pure parser exercise constructed 36 rows with the frozen commands but `nonsense` status and `FALSE` outcome cells: all 36 command anchors still bound uniquely. Thus, conditional on the genuine command/sample results, replacing every documented status/outcome with junk leaves all measured predicates unchanged. This directly contradicts D:80-83's row-declared outcome/status claim. Impact: operability/calibration; duplicate authorities exist between prose table and control JSON. Smallest correction: bind the documented status and outcome cells to a frozen per-row representation, including a negative control that alters only a status/outcome cell. Merely counting commands does not measure the claimed surface.

### 4. Seven rows bypass their declared `ok` status
Evidence: C2:481-508 handles refusal, producer_failure, is_active and pid_state before the common status_ok check. Frozen controls declare `status: {class: ok}` for all seven affected rows (four refusals, hypridle-is-active, waybar-pgrep, producer-failure-propagated). A pure matcher call accepted rc 3 with a model-refusal message and explicit class ok. D:85-91 defines ok as exit 0 and D:93-95 assigns it to every carried row; these statements cannot both describe the actual predicate. Impact: operability/calibration. Smallest correction: explicitly declare the legacy state/refusal status semantics and the affected supersessions, or represent those states as separate exact-status rows; do not label nonzero-accepting rows ok or hide them behind a bypass.

### 5. C1 accepts conflicting causes instead of one identity cause
Evidence: C1:306-319 checks only substring membership. Pure expected_ok call with expected alloc-not-object accepted:

`MADO_BARFOOT: ERROR (stage=setup cause=alloc-negative cause=alloc-not-object junk)`

A tool can append all vocabulary tokens to every same-stage refusal, defeating the intended right-reason distinction in D:15-24. This demonstrates the scorer weakness, not a full 51-mutant run of that forged implementation. Impact: coverage/calibration. Smallest correction: parse one refusal record, require exactly one cause field, and compare it exactly; add a contradictory/multiple-cause negative witness.

### 6. Mutant totals match, but the C2 ancestry explanation is false
AST enumeration at the freeze found C1 exactly 51 unique names (41 carried names identical and in the same order, plus ten); C2 exactly 37 unique names (28 carried plus nine new). However the frozen round-84 C2 counter enumerates 29 mutants, not 37: the sole omitted name is `rc-blind`. D:107-109 says nine round-84 mutants were dropped. Impact: calibration/provenance. Smallest correction: name the one omitted mutant and why; do not imply nine historical removals.

### 7. C2 declared kill rule differs from implemented rule
Evidence: D:103 says a mutant dies on nonzero exit OR fewer than 36 matches. Frozen C2:818 uses `mrc != 0 and (mm is None or mmatched < CASES)`. A nonzero mutant still reporting matched=36 is declared dead by the prose but alive by the implementation; a zero-exit mutant reporting fewer matches also differs. Impact: calibration/operability. Smallest correction: choose and freeze one rule consistently; the stronger nonzero-plus-measured-loss rule is not equivalent to the current declaration.

### 8. Stale counter contracts misdescribe the frozen metrics
Evidence: C1:14-15 advertises 61 cases/41 mutants and base 58/61; C2:33-35 advertises 33 cases/29 mutants, its opening section/command references round 84. Actual constants/populations are 72/51 and 36/37. Impact: calibration/operability. Smallest correction: update the contract documentation to match the executable output, without rewriting historical evidence.

## Requested checks that do not establish a defect

- **Shape arithmetic is consistent.** Exactly 26 of the 36 frozen C2 cases have kinds in SHAPE_KINDS (C2:185-187); C2:793 counts successful cases in that subset. The ten excluded rows are eight exact, one empty, and one producer_failure. This is not a count of distinct grammars. `shapes=26/26` is arithmetically correct if all rows match; define that meaning explicitly rather than interpreting it as 36 distinct shapes.
- **Causal separability:** C2 consumes the held tool for four stage/rc refusal rows but does not consume C1's cause tokens or counter. Therefore no C1-specific causal prerequisite was found: C2 can in principle verify with the held tool plus its independent runbook work. The current frozen C2 setup failure above prevents an actual successful replay; no end-to-end separability pass is claimed. Binding the tool's revision bytes is not itself a requirement that C1 land.
- **C1 axis naming:** D:9,15-40 names declaration-identity edge classes, not merely 72/72. A:coverage explicitly includes edge classes, so the naming is defensible. Nevertheless cause-message specificity alone is not proof of newly governed domain classes; do not turn extra assertions/mutants into automatic coverage credit. The canonical judge must resolve substantive axis movement, not this critic.
- **Do-nothing controls:** Unchanged C1 cannot meet declared correct=72 if its declared 62/72 baseline is reproduced. The C1 target also checks base_correct=62, so simply deleting its cause check would raise the baseline and fail that clause. No full C1 battery was run here. C2's unchanged unguarded producer rows cannot meet exact 7/signal 141 if they return 0, but its target only prints a receipt description (C2:823-830), rather than executing a before-state control. Treat that control as external evidence, not as an exercised counter clause. The junk-row and multiple-cause counterexamples above are the stronger demonstrated loopholes.

## Evidence boundaries and handoff

Read A's distinct-axis/causal-separability requirements and P:343-417 evidence/gate requirements. The available P does not contain a numbered heading `§9`; this review does not invent its contents. Frozen sources were obtained by read-only `git show <freeze>:<path>` and parsed with Python AST; no files were patched. Exercised only pure parser/matcher/allowlist checks and the short frozen C2 setup-refusal reproduction, not full live/mutation batteries. No tool installation or update. Own scratch removed before yielding.

Self-evaluation: accuracy 4 (pure counterexamples, no full battery); completeness 4 (all named checks covered; §9 numbering unresolved); clarity 4 (frozen/worktree distinction explicit); actionability 4 (minimal repairs per defect); conciseness 4 (multiple contract defects require separate evidence). Overall 4.0. Improvement priority: pin corrected counter bytes, then bind the actual documented status/outcome surface.
