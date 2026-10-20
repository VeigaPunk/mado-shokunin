# RevNoHarmPlan — Current guards do not yet justify an unqualified “operability not harmed” verdict

## Findings

### High — The precision gate can accept a candidate that violates the new evidence-output contract

The round-20 contract requires an explicit `evidence` marker on every finding, plus integer `observed_findings` and `lead_findings` counts. The precision counter does not enforce those requirements for candidate output:

- `.ufo/waves/round-20/tw-precision.py:71-89` normalizes a missing `evidence` field to `observed`; it applies the same normalization to actual rows and baseline rows. Thus an actual `observed` finding with no marker can still match its expectation. Its synthetic proof explicitly confirms that an unmarked row matches expected `observed` (`.ufo/waves/round-20/w1/reports/PrecisionCounter.md:12-14`).
- `tw-precision.py:170-184` checks only that the output has the `MADO_TRIPWIRE: ` prefix, schema string `mado-tripwire-verdict-v1`, matching exit, and a `findings` list. It does not assert the required marker is present, validate the two new top-level counts, check that those counts sum to the number of rows, or require the exact `findings` label for a lead-only result.
- The split reporter is also not a rejecting guard: `.ufo/waves/round-20/tw-recall-split.py:81-91,110-132` buckets missing markers as `unmarked`, prints the tally, then returns 0. Its report records the pre-repair `e629f73` result as 6/6 incident lines detected but 6 detected-unmarked lines and 11 unmarked findings (`.ufo/waves/round-20/w1/reports/RecallSplit.md:119-141`). A 6/6 result or successful reporter exit is therefore not evidence that the split is valid.

**Required closure evidence:** preserve missing-as-`observed` only while reading the old baseline; validate the candidate strictly (marker present and exactly `observed|lead`, exact first-line label, integer counts equal to independently recomputed row totals, and zero unmarked findings). Include at least one observed-positive case as well as lead-positive cases.

### High — “Added rows are classed” does not prove additions are harmless

The registered whole-corpus guard at `SCORECARD.md:1255-1260` requires zero lost findings and that every added row be “classed.” A class such as `package_query` does not establish that the transcript states an executed command. The prior harm is a direct counterexample: the closure records a pure `frozenset` data expression becoming an ordinary `package_query` finding at `corpus/lessons/round-19-verifier-spotcheck.md:67-81`. It was classed, but false.

**Required closure evidence:** for every added whole-corpus row, compare the full `(file, line, class, rule, evidence)` identity and adjudicate its evidence under E1: `observed` only where the transcript shows the command and execution path, otherwise an allowed opaque-callee `lead`; reject any pure-data addition. Report the new rows by evidence type, not just class. The 20 control lines and selected P cases are useful controls, but do not substitute for adjudicating all additions.

### High — The baseline comparison does not yet account for observable CLI/schema compatibility or intentional exit flips

The target intentionally changes output and behavior: E1 adds per-row markers and verdict counts; a lead-only finding must remain a `findings` verdict with exit 1. A formerly clean input containing only such an opaque-helper argv can therefore change from exit 0/`clean` at 9c54c56 to exit 1/`findings`. That is an intentional contract change, not evidence of unchanged behavior; the plan needs to state how callers may interpret it.

The existing compatibility checks are insufficient for that distinction:

- The old output shape is explicitly enumerated as `mado-tripwire-verdict-v1` without these fields in `.ufo/waves/round-17/gen_w1.py:28-30`; current `tools/mado-tripwire.py:1630-1643` still emits the `mado-tripwire-verdict-v1` name. No compatibility test or schema-version policy is registered for the added keys. Additive keys may be safe for tolerant readers, but whether all consumers tolerate them is **[UNK]**.
- Existing scan selftests compare `(class, rule, line[, file])` and do not compare `evidence` (`tools/mado-tripwire.py:2051-2062`). Frozen replay compares only `(file, line, class, rule)` plus exit/label (`tools/mado-tripwire.py:1960-1975`), so the required `observed`/`lead` distinction can change or be absent while the old replay still matches. The precision counter also does not test the exact header label.
- The public use guidance says “A finding is an issued command to disclose” (`SKILL.md:527-531`), while E1 permits a `lead` whose callee body is not visible. The registry describes exit 1 as unpermitted host/package/probe findings (`SKILL.md:563`) and does not define the new lead semantics. This documentation must not imply that a lead proves issuance or execution.

**Required closure evidence:** inventory and exercise in-tree output readers against candidate JSON; choose and document whether this is a compatible additive extension or a schema-version change; update the registry/use guidance. On the whole-corpus diff, publish per-input old/new exit and exact label, explicitly count expected 0→1 lead-only flips, and show there are no unexplained flips or `exit=2` regressions. The new lead behavior can be admitted as an explicit change, but cannot be called “no behavior change.”

### Medium — Runtime non-regression is not bounded by the registered proof

The precision runner does execute each tool revision through one interpreter identity (`sys.executable -I`) and gives each fixture scan a 120-second timeout (`tw-precision.py:155-168`); timeout is converted to could-not-evaluate/exit 2 by its exception path (`:229-231`). This is a useful fail-closed bound, not a measured runtime comparison. The registered whole-corpus guard has no stated aggregate timeout or resource ceiling, and the proof does not request candidate-vs-baseline elapsed-time/output-size evidence. If “operability not harmed” includes responsiveness, record a bounded whole-corpus run on identical committed inputs and fail closed on timeout; otherwise scope the verdict to classification/API behavior and name performance as unmeasured.

## Residual risk and verification gaps

The supplied guard list can support a bounded statement about selected precision cases, preserved historical findings, controls, and suite outcomes, once those results are bound to the final tool revision. It does not by itself prove unchanged output consumers, correct evidence labels/counts, or absence of semantically false additions. A defensible closure should separate (1) no lost baseline detections, (2) reviewed new leads/observations, and (3) the explicit v1 CLI/output extension. Do not collapse those into a blanket “not harmed” claim until the gaps above are closed.

I did not run the suite, whole-corpus scan, or candidate runtime. These are source/report review observations only. The requested `lsp` device is not mounted (`read xd://lsp` returned “No such tool”); targeted text search was used only to locate code, and the findings above rely on direct source reads rather than grep as semantic proof. No routing or saturation subsystem is part of this tripwire scope; the counter uses the same `sys.executable -I` path for each revision and I found no fallback/reroute claim in that path.

## Limits

I did not inspect external consumers or prove their tolerance for extra JSON keys (**[UNK]**), measure aggregate runtime or memory, run the final integrated revision, execute any fixture payload, or independently reproduce the reports cited above. No host, package, device, service, or compositor operation was performed.

## Installs

none
