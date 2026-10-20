# RerunSuites — partly falsified: eight revised expectations discriminate; the two evidence markers do not fail under the legacy selftest

## Findings

- **The eight `r20_edit` cases are exactly the cases that change the old-source result.** Ran all 11 requested suites against the 28c6837 tool and the 28c6837 suite files: **247/247 passed**. Then, keeping those exact expected files, ran all 11 again after replacing only the tool with the 1f7f995 version: **239/247 passed**. Its only failures were:
  - `r19-class-body-deferred-clean` (`r19-bashcvar`)
  - `py-helper-nonliteral-arg`, `py-helper-defined-after-call`, `py-helper-redefined`, `py-helper-vararg`, `py-helper-default-nonliteral`, `py-lead-nonliteral-var`, and `py-lead-defined-nonliteral` (`r19-helperfn`)

  These are precisely the eight cases with `r20_edit` explanations: [r19-bashcvar expected.json:412-426](.ufo/waves/round-19/tripwire/r19-bashcvar/expected.json) and [r19-helperfn expected.json:104-165,263-287](.ufo/waves/round-19/tripwire/r19-helperfn/expected.json). The revised expected findings therefore account for every old-source failure; the other nine suites and the remaining cases in these two suites passed against both source versions.

  **Commands and output:** for each directory below, ran `python3 -I /tmp/mado-r20w2-RerunSuites/tools/mado-tripwire.py --selftest /tmp/mado-r20w2-RerunSuites/.ufo/waves/<suite>` once with the 28c6837 source and once with the 1f7f995 source. The 28c6837 runs each printed `SELFTEST_SUMMARY: <all>/<all> passed failed=[]`; the 1f7f995 runs printed `44/45 passed failed=['r19-class-body-deferred-clean']` for `round-19/tripwire/r19-bashcvar` and `27/34 passed failed=['py-helper-nonliteral-arg', 'py-helper-defined-after-call', 'py-helper-redefined', 'py-helper-vararg', 'py-helper-default-nonliteral', 'py-lead-nonliteral-var', 'py-lead-defined-nonliteral']` for `round-19/tripwire/r19-helperfn`; each other legacy suite printed its full pass count. Suite counts were: round-17 `core 9`, `compound 16`, `hardening 33`, `w2-regressions 30`; round-18 `frozen 31`, `r18-failsafe 1`; round-19 `r19-bashcvar 45`, `r19-frozen-f1f2 13`, `r19-helperfn 34`, `r19-installers 18`, `r19-vcs 17` (247 total).

  Tool hashes printed by `--selftest`: 28c6837 `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`; 1f7f995 `367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`. The updated expected-file hashes were `e72a97def0c67617984962c4b3276b6127862daa4d48f9dabd5ae845437abbe5` (`r19-bashcvar/expected.json`) and `91e247912827aa5848a7ce87ef7c59273c6681d737f6456d87180f251ded3644` (`r19-helperfn/expected.json`).

- **Low — legacy comparison gap:** The two added `evidence: "lead"` assertions for `py-lead-cross-cell-literal` and `py-lead-two-calls` ([r19-helperfn expected.json:229-244](.ufo/waves/round-19/tripwire/r19-helperfn/expected.json)) pass on 28c6837, whose direct `--scan` outputs include `"evidence": "lead"`. Direct 1f7f995 scans return findings without an `evidence` field, but its selftest still prints `CASE py-lead-cross-cell-literal ok` and `CASE py-lead-two-calls ok`: the legacy comparator checks only class/rule/line/file (1f7f995 `tools/mado-tripwire.py:2055-2062`). The current comparator checks evidence when expected rows include it ([tools/mado-tripwire.py:2533-2542](tools/mado-tripwire.py)). These markers strengthen the final selftest but do not account for any of the eight legacy failures.

## Limits

- This reran only the 11 named suites, on the cloned 28c6837 expected files; it does not assess the separately claimed precision, recall, or corpus-wide no-harm checks.
- The legacy comparison is intentionally limited: its own `--selftest` silently ignores the added `evidence` fields, so its 239/247 result is not an evidence-field regression test. The final source's selftest does assert them.

## Installs

none