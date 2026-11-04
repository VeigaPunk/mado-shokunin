# R73CriticClaims — frozen-claim review

## Axes and scope

Axes: C1 calibration (four-mutation discrimination), C2 operability (28-case carrier classification), provenance/freeze integrity, score identity, and unchanged finite harm-watch axes. This is an adversarial review, not admission or a canonical judgment. No production files changed; no counters, builds, selftests, alternate runtimes or host probes were run. Sweep: source inspection of both counters and control sets, all three receipts, the baseline prototype, SCORECARD's current ending, read-only commit ordering/blob identities, and artifact filesystem timestamps. Counterexamples below are static call-graph proofs or explicitly marked inferences, not invented run results.

## Four required questions, by claim

### C1

1. **Receipt entailment:** measurement-c1-r73.txt lines 6–9 name four killed mutants; the held column names exactly two. Lines 10–11 follow arithmetically. In the actual counter, lines 266–290 construct each substituted module, call its `outcome_verdict` on both sets, accumulate mismatches, and render the totals. The mutant table contains source substitutions, not stored kill answers. Pristine correctness is checked at lines 259–264. Thus the receipt is internally consistent and the implementation computes, rather than merely asserts, those totals; the text receipt alone cannot authenticate execution.
2. **Control timing:** baseline receipt existed before the freeze commit and before the instrument commit (details below). It is not demonstrated to be a retrospective instrument receipt. Importantly, the baseline already reports `new_set=4/4`: the changed object is the ten-case control set, not the production outcome rule. Doing nothing to the rule can reach the new-set target, intentionally; doing nothing to the held eight-case set cannot. Any claim of newly repaired production outcome behavior would be false.
3. **Score identity:** declared bounded score is 10×4/4 = 10.0000 versus held 10×2/4 = 5.0000. This measures mutation separation, not pristine case accuracy (which is already 10/10 at base). SCORECARD currently ends with round-72 material around lines 3992–4052; no round-73 score is recorded yet. Future agreement is unobserved. A round-73 row must explicitly use killed/4, not correct/10 or the old resolved-active criterion ratio.
4. **Do-nothing/cheat:** unchanged held set misses, but a fake measurement implementation can retain the selftest helpers and print a perfect contract without executing any production mutation. See counterexample A. Also the literal frozen command is not runnable as specified: see B.

### C2

1. **Receipt entailment:** measurement-c2-r73.txt lines 3–22 enumerate 20 files, 13 readers, all guarded; lines 23–50 contain 28 correct candidate cases. Lines 52–79 contain exactly three failures: global-rebind-guard, environ-splat-guard, environ-call-guard. Hence 28/28 and 25/28, and the final counts, follow from the displayed cases. Source lines 1095–1106 and 1138–1169 compute these counts. These are classification outputs, not execution of the fixture subprocesses.
2. **Control timing:** same pre-instrument/pre-freeze baseline evidence as C1. Its held-classifier hash and three miss names agree with the later receipt. The held classifier is genuinely a prior committed generation; exact production-time authenticity has the timestamp limitations below.
3. **Score identity:** declared bounded score is 10×28/28 = 10.0000 versus 10×25/28 = 8.9286. This is classification accuracy on the frozen cases, not 13/13 reader coverage (which the older classifier may already achieve on current production files). No round-73 SCORECARD row yet establishes that future publication uses this quantity.
4. **Do-nothing/cheat:** the held classifier scores 25/28, so cannot reach the declared target unchanged. However, the measurement plumbing can be replaced by a canned target without affecting the classifier selftests, as in A. A further selftest-preserving semantic hole is C.

## Counterexamples and smallest corrections

### A — selftests do not cover either measurement implementation (fixable instrument weakness)

**Concrete counterexample:** replace only C1's `measure(args)` with `emit(contract_line(4, 2, "a" * 40)); return 0`, or C2's with `emit(contract_line(20, 13, 13, 0, 28, 25, "a" * 40)); return 0`. Leave every other definition unchanged. Both selftest call graphs remain exactly unchanged: C1 lines 340–437 and C2 lines 1338–1448 never invoke `measure`. Therefore these substitutions introduce zero selftest failures relative to the originals, while skipping all real mutation scoring/census work. This is a static dependency proof, not a reported mutant run. It does not show the shipped counters are canned; their inspected loops are substantive.

**Impacted axes:** calibration of the counters; evidentiary linkage for both claims. **Smallest safe correction:** have an independent counter/harness mutation check kill these two measure-only substitutions, exercising the CLI/measurement path against controlled read-only extraction. Keep frozen claim predicates unchanged. Merely testing more embedded truth tables does not close this hole.

### B — frozen C1 command omits required `--controls` (fixable interface defect)

The declaration committed at freeze `87e4c61a` specifies `--repo`, `--rev`, `--base-rev`, and `--scratch-root`, without `--controls`. C1 parser gives controls no default (line 446); main explicitly raises UsageError when it is absent (lines 458–459). The documented invocation therefore reaches exit 2 with no contract, not the promised exit 0. This conclusion follows directly from parsing and control flow; no rerun was performed. The existing receipt proves a run using some valid arguments, not that this literal invocation works.

**Impacted axes:** operability/reproducibility and freeze-command fidelity. **Smallest safe correction:** an explicit append-only invocation erratum naming `--controls .ufo/waves/round-73/controls/c1-outcomes-r73.json`; do not silently rewrite the frozen declaration or reinterpret the predicate. A default matching that immutable path is another implementation repair, subject to the lane's freeze policy.

### C — C2 whole-mapping global rebinding is asserted but not discriminated (fixable coverage gap)

The frozen sentence includes both a key store and rebinding a global to a guarded mapping. The case named `global-rebind-guard` actually executes `ENV["GIT_NO_REPLACE_OBJECTS"] = "1"`, not `ENV = {"GIT_NO_REPLACE_OBJECTS": "1"}` (controls lines 144–147). Candidate support for the latter exists separately in global_guard lines 923–925. Removing only that `elif` branch leaves all 28 frozen cases untouched and none of the listed selftest regressions specifically exercises a guarded whole-name global rebind. [INFERENCE] Such a mutant can retain the target while violating this clause; the classifier has other flows, so its exact rejection output is not asserted without execution.

**Impacted axes:** C2 claim entailment and calibration. **Smallest safe correction:** independently probe a real whole-name rebind fixture and its branch-removal mutant; record it as auxiliary clause evidence, not a silent expansion of the frozen 28-case denominator. Alternatively limit publication to the actually discriminated subscript-store spelling, with canonical authority deciding whether that is an acceptable scope change.

## Provenance evidence and limits

Read-only git log establishes the parent chain:

- base `d3f6c9f5…`: author/committer 2026-11-04 01:54:53 -03:00;
- freeze `87e4c61a…`: parent base; author 01:54:53, committer 02:00:09;
- instruments `1459cca1…`: parent freeze; author/committer 02:04:18.

`git show --stat` puts baseline, prototype, declaration and both control sets together in the freeze commit, preceding instrument addition. Filesystem stat: baseline birth 01:59:36.281 / mtime 01:59:36.341; declaration birth 02:00:05.513; measurement files born 02:03:45.465 (C1), 02:03:02.132 (C2). This supports pre-freeze baseline creation. The baseline has no embedded execution timestamp or control-file digests despite declaration lines 13–14 saying digests are in the receipt. Commit order proves persistence order, not an unforgeable execution history; timestamps can be manipulated. No concrete retrofit evidence found. The declaration's current mtime is later, so this review separately read the declaration directly from the freeze commit rather than assuming current bytes were authoritative.

C1 production harness blob identity is identical at base and instrument revisions: `484c5d7ea738668ad1773b97d7c5ceaf3f2dc3d6`. Thus the current C1 improvement is control-set discrimination with unchanged subject. Its `--base-rev` is only printed, not used to extract an independently scored base harness; this does not change the observed round's result given the identical subject blobs, but must not be described as independent baseline execution.

## Disposition boundary

No false arithmetic or encoded mutant-answer table found. At least two concrete counterexamples are established statically (A and B); C identifies a clause-evidence gap. Whether C1's control-set-only improvement counts as an admissible capability, and whether these residuals invalidate admission/no-harm, belongs to the canonical judge. No saturation, promotion, or universal classifier-soundness conclusion follows from these finite maxima. No tools installed or updated.

Self-evaluation: accuracy 4/5 (semantic mutant C not executed, clearly marked inference); completeness 4/5 (future SCORECARD publication unavailable); clarity 4/5 (source line references support each distinction); actionability 4/5 (specific minimal corrections, not applied by critic); conciseness 4/5 (provenance detail retained for the assigned audit). Overall 4.0/5. Improvement priority: independent measurement-path mutant evidence, then whole-name-rebind clause evidence; neither changes the frozen scoring denominator.
