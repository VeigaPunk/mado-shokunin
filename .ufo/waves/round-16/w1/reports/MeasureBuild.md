# MeasureBuild — round-16 w1 report

## Files changed

- Created `.ufo/waves/round-16/measure.py` (only assigned implementation
  file; executable bit set). No other files touched; no commits.

## Behavior

Round-16 revision-bound structural counter, `measure.py <revision>`:

- **U1–U6 semantics reused unchanged** from
  `.ufo/waves/round-15/measure.py`: head-15 provenance trio
  (`source:` + `verified-at:` + `recheck:`), exactly one `covers: U<N>`
  line, mined `used-by` reciprocity, tier A/B join gate, U4 three body
  facets, U5 decision sections + reciprocal S047/S048 + inverse rule,
  U6 exact level-2 headings (`Layer ladder`, `Safe boundary`,
  `Unexercised delivery` with `[UNK]`) + reciprocal S051/S052 + inverse.
- **C3 calibration observation** (added on L1 request): literal published
  rubric on revision `corpus/QUALITY.md` bytes — numerator = lines
  matching `^[0-9]+\. .*lessons/`, denominator = all `^[0-9]+\. ` numbered
  criterion lines. Emits `criteria_total`, `lesson_grounded`,
  `criterion_ids`, `lesson_grounded_ids`, `ungrounded_ids`, `fraction`,
  and `score = 10 * fraction` under top-level `calibration`. Multiline
  semantics deliberately not broadened: a `lessons/` citation on a
  wrapped continuation line does not count. Causally separate from C1
  coverage and C2 gate evidence; never folded into either score. Working
  tree currently shows 14/22 grounded (ungrounded ids 1–5, 18–20); the
  probe measures whichever revision bytes it is handed.
- **U7 extension** (new): a `covers: U7` note must additionally pass
  `u7_facets` — exact level-2 headings `## Producer contract`,
  `## Renderer boundary`, `## Safe observation`, `## Unexercised
  rendering`, with `[UNK]` inside the rendering section body — plus
  reciprocal mined A/B rows **S053/S054** (both mined, tier A/B, naming
  the note in `used-by`, and cited on its source line) and the same
  inverse rule as U5/U6: any mined row naming the note must be cited.
  S055 (reserved for closure own-work safety evidence) is deliberately
  excluded from `U7_SOURCES`; own-work receipts cannot credit a
  documented-route item, though the inverse rule still forces it to be
  cited if it names the note.
- **Revision binding preserved**: revision resolved to commit SHA first;
  every input read via `git show <sha>:<path>` (SOURCES.md, README.md,
  knowledge notes, gate bytes, safety artifacts).
- **No gate execution, no score conflation**: `tools/mado-verify.sh` is
  SHA-256 hashed only (`gate_executed: false`). New round-16 safety
  artifacts — `tools/mado-action-plan.py`,
  `.ufo/waves/round-16/safety-policy.json`,
  `.ufo/waves/round-16/safety-cases.json` — are observed for
  presence/SHA-256 with `executed: false` and `scored: false`; they are
  never run and never folded into the C1 score. There is no C2 score.
- **Navigation/registry counts preserved**: README index
  missing/extra/duplicates; registry rows/tiers/statuses; required-row
  presence reported as `round15_required` (S051/S052, established key
  kept for consumer continuity) and new `round16_required` (S053/S054).
- **Exit-0 probe semantics preserved**: missing U7 note, failed facets,
  absent reserved rows, or absent safety artifacts are reported as
  measured results; `sys.exit(0)` unconditionally.

New output fields: `coverage.u7_present`, `coverage.u7_facets`,
`coverage.u7_candidates`, `source_registry.round16_required`,
`measure_inputs.safety_artifacts`, `measure_inputs.safety_executed`,
top-level `safety_artifacts` map, `measure_inputs.quality`, top-level
`calibration` (criteria_total, lesson_grounded, criterion_ids,
lesson_grounded_ids, ungrounded_ids, fraction, score, rule). All prior
fields retained.

## Exact retained evidence

- `round-15-verifier-spotcheck.md` read at
  `corpus/lessons/round-15-verifier-spotcheck.md`: confirmed U6 = 6/7
  delivered at `9ebd737a…`, U7 absent, and the provenance-trio +
  level-2-heading + `[UNK]` boundary pattern U7 now mirrors.
- `round-15/measure.py` (295 lines) was the semantic baseline; U1–U6
  logic copied verbatim, U7 added in the same pattern.
- `round-16/w1/spec.json` confirms S053 = tagged Waybar custom man,
  S054 = tagged custom.cpp, S055 = closure own-work safety (reserved,
  not a U7 source).
- `corpus/QUALITY.md` (working tree): 22 numbered criterion lines,
  14 with same-line `lessons/` citations; ungrounded literal ids
  1–5, 18–20 (18–20 carry any citation on wrapped continuation lines,
  which the literal rule intentionally excludes).

## Incident during edit

An `edit` call applied against stale line numbers briefly corrupted the
navigation block; it was repaired in the same session and the final
`edit` reported no syntax error. The file now contains exactly one
`nav` definition, one `round15_required`/`round16_required` pair, and
one `u7_facets` definition.

## Risks

- **Not executed**: per contract, seats run no checks; syntax/behavior
  verified only by the edit tool's parse check and code review. L1's
  post-integration run is the first real execution.
- **`git show` of absent safety artifacts** relies on `CalledProcessError`
  catch in `try_source`; at a pre-integration revision all three report
  `present: false` and exit remains 0.
- **Inverse rule breadth**: any mined row naming the U7 note (including
  a mined S055) must appear on the note's source line or the join
  fails — intentional, same as U5/U6.
- **Heading exactness**: level-2 text is whitespace-normalized lowercase;
  `## Producer Contract` matches, `### Producer contract` or a bolded
  paragraph does not. WaybarDraft's note must use literal `##`
  headings as named above.

## Blockers

None. No installs performed; pacman pause honored; no live probes, no
gate/test execution, no sibling files touched.

Checks for L1 after integration: run
`python3 .ufo/waves/round-16/measure.py <delivered-sha>` and confirm
`coverage.count == 7`, `u7_candidates[].reserved` all true,
`navigation.missing/extra/duplicates == []`, and
`safety_artifacts.*.present == true` with `scored/executed == false`.
