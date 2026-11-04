# R75RevC1 — frozen C1 instrument/evidence review

Scope: freeze `def73656c94f0e88bd671cfb4a65124338261722`, base `b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6`. Line citations below refer to the frozen bytes, not subsequent working-tree repairs. Axes: instrument fidelity, echo credit integrity, pin/receipt honesty, environment isolation, fixture-label fidelity. No production/corpus edits, no installations, no subagents.

## Findings by severity

### P2 — uppercase fixture can falsely reject a conforming harness

`quality/counters/c1-r75-harness-witness.py:94-95,304-308`, `quality/counters/c1-r75-landing-controls.py:225`, frozen controls `c1-harness-cases-r75.json:16-19`.

The uppercase mode applies `tr a-f A-F`, while its frozen expectation is always no kill. A valid token_hex(8) output containing only decimal digits is unchanged by this transformation. The correct byte-exact comparator then credits the kill, but the counter would mark that case wrong. This is an instrument/label error, not an echo-rule bypass.

Exact witness: isolated process patched only the scratch-loaded `secrets.token_hex` to return `0123456789012345`, then ran the real frozen harness on the counter-created uppercase fixture. Output: `MADO_R75_LANDING_CONTROLS: selftest=2/2 mz=pass mr=pass killed=2/2 baseline=0/2 witness=ok verdict=TARGET_MET ...`; rc 0. Full command/output: `probes.txt`, `NUMERIC_COMMAND` section; reproducer: `probes.py`.

Probability of this valid input under uniform token_hex: `(10/16)^16 = 0.0005421010862427522` (about 1 in 1,845 uppercase-fixture runs). Thus the frozen 11/11 result is reproduced but is not stable for every allowed challenge. Future separately declared controls should make their negative witness guaranteed unequal; do not rewrite these frozen receipts/cases.

### P2 — absent candidate violates the declared measurement/exit contract

`quality/counters/c1-r75-harness-witness.py:205-209,282,418-420`; declaration C1 kill rule and script docstring lines 32-34.

An absent candidate is promised `correct=absent`, `TARGET_MISSED`, exit 1. Instead, unconditional extraction raises SetupError and exits 2 without the contract line. Probe used the frozen counter with `--rev b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6` and the frozen controls/base. Exact output: `c1-r75-harness-witness.py: quality/counters/c1-r75-landing-controls.py is absent at b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6`; rc 2. Command/output: `absent-candidate.txt`.

This turns a specified measured miss into a setup error. It does not invalidate the observed present-candidate 11/11 run. Restore the promised absent-candidate branch in a successor, preserving setup-error treatment for unrelated extraction failures.

### Advisory — `liar-success` has no distinct fixture behavior

`quality/counters/c1-r75-harness-witness.py:91-92,106-126`.

`right` and `liar-success` enter exactly the same report and echo branches. The standalone original scripts both emit `2/2` plus the exact echo and exit 0. After the same M-Z clause deletion, both emit the same one FAIL line, `1/2`, the exact echo, and still exit 0. `probes.txt` records `MODES_IDENTICAL mutated=False True` and `MODES_IDENTICAL mutated=True True`, including all output and exit codes.

Therefore the case named `liar-success` does not independently distinguish a liar from a genuine child. In fact the purported `right` mutant also exits successfully despite reporting a failed assertion. The arithmetic-only contract deliberately ignores rc, so the labels' expected pass values are compatible with the rule; what is unsupported is calling these two modes separate behavioral separators or using them as independent evidence of truthfulness/exit-status discrimination.

## Hypotheses tested and limits

Receipts are siblings of this report. `counter.txt` records the exact frozen command and all eleven per-case rows: candidate 11/11, base 6/11, TARGET_MET, rc 0, matching the committed receipt. All fixture names other than the duplicated right/liar distinction and the probabilistic uppercase expectation are justified by the template's branch/output shape. Crash emits no summary; zero-denominator is refused; mismatched detail fails arithmetic; green-mutant has no failed summary; stale/wrong/absent/last-wrong alter the echo as named.

`probes.py` and `probes.txt` record each additional hypothesis and output:

- **Credit without echo:** frozen `credit_with_witness` with actual r72 `credit` returns False for absent, wrong, uppercase-letter echo; True for exact echo. No no-echo credit bypass observed. Canonical implementation: successor lines 131-132/217; r72 lines 348-362 and 518-525.
- **Ambient nonce contamination:** with ambient `ffffffffffffffff`, installed child env carries only fresh `deadbeefdeadbeef`; successor git env has no nonce. Canonical constructor: successor lines 202-205 wrapping r72 `_base_env` lines 116-126. The ambient nonce is replaced rather than forwarded.
- **Contract verdict/exit divergence:** with two kills and green arithmetic, missing echo produces witness=absent/TARGET_MISSED/exit 1; correct echo produces witness=ok/TARGET_MET/exit 0. `contract_line` lines 207-219 and the canonical r72 `outcome_exit` lines 389-390 both call the installed same-echo green predicate. The r72 measurement derives killed from its actual M-Z/M-R booleans at lines 593-596. No implementation divergence found. A kill can legitimately coexist with a red overall outcome when the original selftest is red.
- **Can witness= lie?** It summarizes only the original selftest output, not the M-Z or M-R output, because r72 passes `selftest_out` at lines 594-595. M-Z has a separate echo check through installed credit. `witness=ok` alone proves neither overall success nor truthful assertions. That limitation is disclosed. The counter's parser extracts only mz (lines 212-216/304-308), so its 11/11 is not independently an assertion about witness-state or verdict/exit agreement.
- **Pin scope:** intercepting only read-only git-show output and adding one newline to the r72 bytes makes `load_generation` reject the digest. The pin freezes exactly `quality/counters/c1-r72-landing-controls.py`, not candidate wrapper, fixture template, production instrument, three child tools, or interpreter. Those four extracted files are selected by rev and individually hashed by canonical r72 lines 483-487; freezing only the generation is consistent with the declaration. Source of pin rejection: successor lines 180-184.
- **Standing echo:** source review of `quality/landing-counters.sh:15-20,225-227,290` shows absent/malformed challenges print nothing, valid 16-hex is preserved and echoed after summary. The eleven-case counter replaces this file with a test double; it is not a production-instrument integration test. No separate production selftest was run by this seat.

## Residual risk / verification gaps

LSP device unavailable (`read xd://lsp` returned `No such tool`), so references/definitions/diagnostics could not be obtained; text inspection is not semantic LSP proof. The relevant canonical r72 callsites were inspected directly. Review is for the frozen assignment, not later working-tree repairs (the working-tree successor changed while this review was running). Production end-to-end selftest, broader no-harm gate, and other claim/route/resume/saturation contracts are not exercised here and are not inferred from 11/11. No unrelated runtime was invoked.

The same nonce is intentionally shared by the original selftest and its mutant invocation within one harness run; this authenticates echo knowledge, not assertion truth or a distinct challenge per child. Environment evidence logs the nonce via r72 describe_env, so the challenge is not a long-lived secret. Neither is presented here as a contradiction of the frozen declared echo-only guarantee.

Self-evaluation: accuracy 4 (source/probe evidence, no LSP diagnostics); completeness 4 (all requested C1 questions addressed, production execution explicitly unexercised); clarity 4 (frozen line citations distinguished from working tree); actionability 4 (two concrete successor fixes, frozen files untouched); conciseness 4 (full receipts separated from findings). Mean 4.0. Highest-impact improvement: deterministic unequal uppercase control in a newly declared set. User agreement check: findings are instrument defects, not a fabricated no-echo bypass.

C1: survives with defects
