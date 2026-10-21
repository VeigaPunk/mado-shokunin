# GatePopulationFileMutated — independent C2 artifact probe

## Scope and verdict

- Seat: `MadoR21-2.GatePopulationFileMutated-2`; advisory only, no promotion or round-admission authority.
- Axes: correct negative verdict; actual-byte digest authority; C1 independence; bounded execution and exact restoration.
- Stable probe ID: `R21-W2-C2-POPULATION-FILE-MUTATED-ADVISORY-SPOOF`.
- Stable gate finding: `population_digest_changed`.
- **Verdict: the single nearby false-negative/bypass attempt was rejected (artifact mutant killed).** The pristine, altered and restored artifacts all passed the behavioral detector: process exit `1`, output code `1`, result `failed`, exactly the expected finding, and the independently measured on-disk population digest in `actual_inputs`.
- This is an artifact mutation probe, not a production-code mutation or a claim of broad mutation coverage. The pristine gate's `failed` verdict is the expected result for this negative fixture, not a failing baseline detector.

## Exact tested source and inputs

Production source: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`.

Measured SHA-256 before and after all three executions:

```text
5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7
```

The parent identified current candidate `f499a8db7171b7476fe9f204ab9edbac5a956fa9`, superseding the original task's `2ac0f9ba69051aea22cab3b6cfebe4d906b72d17`. That commit association is parent-supplied provenance, not an independent VCS check; the measured source digest above identifies the exercised code. No Git/jj command was run.

Frozen case: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/population_file_mutated.json`.

Scratch artifact: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/GatePopulationFileMutated-2/population_file_mutated.probe.json`.

Fixture root passed to the gate: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures`.

Actual-byte hashes, measured using `sha256sum`, were unchanged before/after except for the deliberate scratch-artifact transition:

| Object | SHA-256 |
| --- | --- |
| Frozen case | `22f490b81c272fd1c37cc2797811c77b5621d32331c7ddb600b4285c83bf5ddb` |
| Scratch pristine | `22f490b81c272fd1c37cc2797811c77b5621d32331c7ddb600b4285c83bf5ddb` |
| Scratch altered | `23318a2f91f18902ac14574b6e64cb769348a8749013a5bb1f9dc1b2709d55a4` |
| Scratch restored | `22f490b81c272fd1c37cc2797811c77b5621d32331c7ddb600b4285c83bf5ddb` |
| Frozen expectations | `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e` |
| Actual mutated population file | `c02069a203b8c1306e61b8470c8fe916e08fd5db23fd433c95b6f87ed82e84fc` |
| Baseline population file | `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed` |

The population paths hashed were `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/snapshots/population-mutated.txt` and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/snapshots/population-baseline.txt`. The expectations path hashed was `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json`. These are measured file bytes, not acceptance of their embedded digest assertions.

## Mutant and expected detector

Only the scratch artifact's `population[0].actual_sha256` was changed:

```text
before: c02069a203b8c1306e61b8470c8fe916e08fd5db23fd433c95b6f87ed82e84fc
mutant: 16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed
```

The mutant falsely makes advisory `actual_sha256` agree with registered `sha256`, while `population.path` still names the unchanged mutated population file. Every other artifact field and every referenced file stayed unchanged. This is the nearby false-negative risk of trusting caller-supplied observed-hash metadata instead of hashing the file.

The expected detector required all of the following on pristine, mutant and restored bytes:

1. Real child process exit = emitted `code` = gate `SystemExit` = `1`.
2. `result == "failed"`.
3. `finding_ids == ["population_digest_changed"]`.
4. `actual_inputs[0]` names `snapshots/population-mutated.txt` and contains measured digest `c02069a203b8c1306e61b8470c8fe916e08fd5db23fd433c95b6f87ed82e84fc`, not the spoofed advisory value.
5. `actual_expectations_sha256` equals the separately measured expectations-file digest.

This matches the frozen case's code/result and its written population digest rule. It does not alter the frozen contract.

## Bounded executions and actual outputs

Three sequential executions of the same detector were run: pristine, single mutation, exact restoration. Each execution used one Python `3.14.8` child, isolated mode and bytecode writing disabled (`-I -B`), a parent-enforced 15-second timeout, `RLIMIT_AS = 402653184` bytes (384 MiB), and `RLIMIT_CPU = 12` seconds. No detector child launched another process.

The unchanged wrapper set the equivalent gate arguments:

```text
/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/GatePopulationFileMutated-2/population_file_mutated.probe.json
```

It invoked that trusted source with `runpy.run_path(..., run_name="__main__")`, recorded `SystemExit`, and exited with the same value. A Python audit hook recorded lane file opens and rejected any unexpected lane dependency or nested process/network launch. No source text from a fixture or transcript was executed.

| Stage | Process exit | JSON code | Result | Finding | Detector | Elapsed seconds |
| --- | --- | --- | --- | --- | --- | --- |
| Pristine scratch, byte-identical to frozen case | 1 | 1 | failed | population_digest_changed | passed | 0.029318 |
| Advisory-hash spoof mutant | 1 | 1 | failed | population_digest_changed | passed; bypass rejected | 0.029614 |
| Exact restored scratch | 1 | 1 | failed | population_digest_changed | passed | 0.028273 |

All three gate stdout byte strings were identical. Their complete JSON output was:

```json
{
  "actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e",
  "actual_inputs": [
    {
      "path": "snapshots/population-mutated.txt",
      "sha256": "c02069a203b8c1306e61b8470c8fe916e08fd5db23fd433c95b6f87ed82e84fc"
    }
  ],
  "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority",
  "code": 1,
  "finding_ids": ["population_digest_changed"],
  "result": "failed"
}
```

The following audit JSON was emitted by the wrapper on stderr for each execution, not by the gate:

```json
{
  "gate_system_exit": 1,
  "lane_open_paths": [
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json",
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/snapshots/population-mutated.txt",
    "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/GatePopulationFileMutated-2/population_file_mutated.probe.json",
    "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py"
  ],
  "process_or_network_events": [],
  "python": "3.14.8",
  "rlimit_as": [402653184, 402653184],
  "rlimit_cpu": [12, 12],
  "unexpected_lane_reads": []
}
```

## Explicit C1 independence review

Static review of `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py` found:

- Lines 8–15 import only standard-library modules. No C1 classifier or result module is imported.
- The `--check` path at lines 206–230 calls `evaluate`, then `check`; it does not call `selftest`.
- Lines 107–116 validate the registered digest, resolve `population.path` beneath the explicit root, hash its actual bytes and compare the result to `sha256`. Advisory `actual_sha256` is not read.
- Lines 123–127 independently hash the actual expectations file. They do not consume a C1 verdict or receipt.
- The only `subprocess.run` site is in the unexecuted `selftest` function at lines 166–203. No C1 code is invoked there either.

Runtime evidence corroborates independence for this probe: the lane-open allowlist permitted exactly the gate source, isolated case artifact, C2 expectations and mutated population bytes. All three runs completed with no unexpected lane open and no process/network event. In particular, no C1 classifier source, transcript, classifier output, result receipt, Git/jj metadata, or evidence-string target such as `/home/vgpnk/Projects/shokunin/mado-shokunin/SHONEN.md` was opened. This establishes the tested gate execution's separation from C1; it is not a general sandbox or authentication proof.

## Restoration, limits and authority

- The scratch mutation was reversed before the final run. Restored SHA-256 equals the original frozen-case SHA-256, and `cmp` of frozen case versus restored scratch exited `0`, establishing exact byte equality, not merely JSON equivalence.
- The production gate, frozen case, frozen expectations and both population files had identical measured before/after hashes. Only the assigned scratch artifact and this report were written. No production, frozen fixture, sibling source, index, remote or host configuration was edited.
- No full selftest, suite, corpus, C1 scanner, live compositor, service or package command was run. No historical unsafe resource failure was rerun.
- **No tools installed or updated.** Existing Python and coreutils were sufficient.
- Scope is one negative fixture and one advisory-hash spoof variant. Other malformed-input classes and unrelated gate behavior were not dynamically tested.
- Timestamp strings are ordering assertions, not authenticated event times. Oracle-author/independence fields and named non-author-verifier strings are assertions, not independently authenticated identities or proof. The gate's regex/string checks do not establish verifier independence or semantic sufficiency. This probe grants neither C2 promotion/admission nor a claim that the historical `c2_independent` assertion has become true.

Report: .ufo/waves/round-21/w2/reports/GatePopulationFileMutated.md
