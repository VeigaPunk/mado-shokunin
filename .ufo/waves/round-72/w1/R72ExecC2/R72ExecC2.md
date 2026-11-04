# R72ExecC2 — independent C2 execution

Axis: C2 operability (C1 calibration held out of scope). No production changes.

## Executed results

From the lane root, ran the assigned command unchanged:

```sh
python3 -I quality/counters/c2-r72-outcome.py --repo . --rev 9bcb4fd5b598844f168230dc05e441721d95b272 --base-rev 976684a27e99c2508037a60eec415f550f53d70e --controls .ufo/waves/round-72/controls/c2-controls-r72.json --scratch-root /fast/scratch/hyaku/mado-r72/R72ExecC2/run
```

Observed final contract and command status:

```text
MADO_R72_OUTCOME: cases=8 correct=8 base_correct=4 verdict=TARGET_MET rev=9bcb4fd5b598844f168230dc05e441721d95b272
RC=0
```

Ran `python3 -B -I quality/counters/c2-r72-outcome.py --selftest --scratch-root /fast/scratch/hyaku/mado-r72/R72ExecC2/run`: `MADO_R72_OUTCOME_SELFTEST: 24/24 assertions passed`, RC=0. `-B` prevents imported working-tree modules from creating bytecode files.

Independently extracted both harnesses with read-only `git show`, imported using importlib, and called held `outcome_verdict(gate_rc, killed)` and successor `outcome_verdict(gate_out, killed)` over the frozen JSON. Retained driver: `rederive-baseline.py`. Result: `INDEPENDENT_BASELINE: cases=8 correct=4`; `RECONCILIATION: differences=0`; RC=0.

## Same eight cases, same verdicts

| Case | Expected | Candidate | Held |
|---|---|---|---|
| green-summary-exit0 | TARGET_MET | TARGET_MET | TARGET_MET |
| failing-summary-exit0 | TARGET_MISSED | TARGET_MISSED | TARGET_MET |
| green-summary-exit2 | TARGET_MET | TARGET_MET | TARGET_MISSED |
| no-summary-exit0 | TARGET_MISSED | TARGET_MISSED | TARGET_MET |
| garbled-summary-exit0 | TARGET_MISSED | TARGET_MISSED | TARGET_MET |
| failing-summary-exit2 | TARGET_MISSED | TARGET_MISSED | TARGET_MISSED |
| no-summary-exit2 | TARGET_MISSED | TARGET_MISSED | TARGET_MISSED |
| green-summary-killed1 | TARGET_MISSED | TARGET_MISSED | TARGET_MISSED |

Differences from committed `measurement-c2-r72.txt`: none in cases, verdicts, correctness flags, contract, controls digest, revisions or harness digests. Its `C2_RC=0` and this run's `RC=0` are only different wrapper labels for the same exit status. Differences from `control-baseline-c2-r72.txt`: none; all eight PROTO rows matched exactly. Held failures remain exactly failing-summary-exit0, green-summary-exit2, no-summary-exit0 and garbled-summary-exit0.

## Exact decision surface

Read pinned successor `quality/counters/c1-r72-landing-controls.py` at the scored revision (SHA256 below):

- Lines 298–302: `last_summary` scans lines backward for the first line beginning exactly `MADO_LANDING_COUNTERS_SELFTEST:` and returns its stripped text; absent returns `none`. Thus a later prefixed but malformed summary blocks an earlier valid one: it does not skip malformed summary lines searching for a valid parse. Indented prefixes are not selected.
- Lines 347–354: `summary_green` requires a full match of `MADO_LANDING_COUNTERS_SELFTEST: (\d+)/(\d+) assertions passed`, converts both groups to integers, then requires `total > 0` and `passed == total`.
- Lines 371–376: outcome exit 0 / verdict TARGET_MET additionally require `killed == 2`. Every other combination is exit 1 / TARGET_MISSED.
- Lines 472–478: gate text is decoded stdout concatenated with decoded stderr, not chronological stream interleaving; therefore matching summary lines in stderr follow those in stdout. Gate return code is recorded in `MADO_R72_SELFTEST ... rc=...`; it is not passed to either outcome function.
- Lines 379–382 and 575–578: summary fraction, M-Z/M-R labels, baseline and revision are recorded in the contract. Killed is computed from M-Z/M-R booleans and is a deciding input. Labels, revision and baseline fields do not independently gate verdict. `SELFTEST FAIL` detail is not checked by `summary_green` (C1's separate credit function checks failure details).
- Counter lines 223–224 explicitly feed candidate only `(gate_out, killed)` and held only `(gate_rc, killed)`. Frozen `gate_rc` cannot influence candidate scoring.

## Retained evidence and limits

All retained files are beside this report:

- `frozen-command-receipt.txt`: original process tool response containing all eight case rows, digests, final contract and RC=0.
- `selftest.txt`: exact selftest output and RC.
- `independent-baseline.txt`: imported source hashes, eight exact held rows, baseline total and reconciliation result.
- `rederive-baseline.py`: independent reproducible driver; requires recreating the explicitly named seat scratch directory before rerun.

Controls SHA256: `640fb44fdb1f31b4706b381c905fde4b5dae769bfd3e5b656bdb374bad58a793`.
Candidate SHA256: `d0d3bfd2b8306062e7ea7323377dea1371df93c4a9447a7a28c4927becfe7c62`.
Held SHA256: `f836499594fb4fa8898336b1a47241614bb2b9ddb6f93c369a9e00ece0f185f1`.

No discrepancy or blocker. These are eight finite decision-function controls, not an end-to-end landing-harness execution or general fault-coverage claim. The selftest imports working-tree harnesses; revision-pinned counting and independent extraction establish the frozen-revision result separately. No build/lint/formatter or unrelated test ran. No tools installed or updated. LSP is not exposed in this seat's tool inventory; symbol inspection used bounded source reads and grep, not an empty LSP response.

Only this exclusive report directory was written, plus assigned scratch. Scratch is removed after receipt retention. No committed lane file changed. The frozen invocation was accidentally launched with a service name by the tool wrapper; it completed in 52 ms and exited 0; no continuing job remains.

Self-evaluation: accuracy 4/5 (finite controls only); completeness 5/5 (command, selftest, independent baseline, reconciliation and input semantics retained); clarity 4/5 (detailed stream-order caveat adds length); actionability 5/5 (driver plus exact receipts); conciseness 4/5 (full case table retained for audit). Overall 4.4/5. Highest-value improvement: retain the same finite-scope wording when integrating these findings. User agreement: expected, subject to the declared scope limits.
