# GateBaselineValid — one artifact mutation probe

- **Finding ID:** `R21-C2-baseline-valid-duplicate-registration-time`
- **Verdict:** **KILLED (artifact mutant)**. The pristine baseline was clean; one duplicated registration key was rejected as malformed; restoring the exact pristine bytes restored the same clean output. No defect was found in this bounded variant. This is not a production-source mutation or an independent promotion/round-admission decision.
- **Axes:** baseline correctness; ambiguous-input rejection; exit/code/result/finding-ID agreement; actual-byte hash authority; C2 independence from C1 execution/results; exact restoration and containment.
- **Candidate:** L1 supplied current commit identifier `f499a8db7171b7476fe9f204ab9edbac5a956fa9`, superseding the initial `2ac0f9ba69051aea22cab3b6cfebe4d906b72d17`. Commit identity was not queried through VCS. The exact tested source bytes, independently hashed before and after the probe, are recorded below.

## Scope and tested bytes

Production was read and executed without modification:

`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`

Tested production SHA-256, unchanged before/after:

`5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7`

Frozen baseline:

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/baseline_valid.json`

Private inert scratch assessment, the only artifact mutated:

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/GateBaselineValid/baseline_valid.json`

The scratch assessment was byte-identical to the frozen baseline before mutation. The gate used the frozen fixture root read-only, so its population and expectations inputs were the actual frozen files rather than reconstructed or self-reported hashes.

| Bytes read | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| Frozen baseline | `98edc77e17d25d4181f12200805c73f7d7bc871df473367e59908e811d47937d` | `98edc77e17d25d4181f12200805c73f7d7bc871df473367e59908e811d47937d` |
| Scratch baseline/restoration | `98edc77e17d25d4181f12200805c73f7d7bc871df473367e59908e811d47937d` | `98edc77e17d25d4181f12200805c73f7d7bc871df473367e59908e811d47937d` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json` | `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e` | `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/snapshots/population-baseline.txt` | `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed` | `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed` |

These are actual `sha256sum` observations. In particular, neither the population digest nor the expectations digest was accepted merely because its string appeared in the assessment.

## Mutant and expected detector

Insert exactly one additional line immediately after the existing registration field in the scratch JSON:

```json
  "registration_time": "2026-01-01T00:00:00Z",
```

This creates two occurrences of the same top-level key, even with the same value. All other bytes remain unchanged. It is a nearby malformed/ambiguous artifact, not a contradictory timestamp claim. A permissive last-key-wins parser could silently report it clean; the registered malformed/ambiguous-input contract instead requires code 2 and `could-not-evaluate`.

Mutated scratch SHA-256:

`df2d9772795c495c3b6f1f7378ea881cd4735ccd8187504d828c580190707701`

Expected detector: production `--check` rejects duplicate JSON identities through `pairs` and returns `assessment_input_invalid`, not `assessment_clean`. Source locations: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py:32-38,49-51,158-163`.

## Bounded execution and actual outputs

The same command was run once on pristine, once on mutated, and once on restored scratch bytes:

```text
/usr/bin/python -I -B /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/GateBaselineValid/baseline_valid.json
```

Each execution was one gate child launched synchronously with `RLIMIT_AS = 402653184` bytes (384 MiB) and a 15-second subprocess timeout. `-I -B` isolated Python module lookup and suppressed bytecode writes. No selftest, suite, corpus, C1 execution, service, compositor, package command, background job, or fixture payload was run. Standard error was empty in all three executions.

| Phase | Process exit | JSON code | JSON result | Exact finding IDs |
| --- | --- | --- | --- | --- |
| Pristine | 0 | 0 | `clean` | `["assessment_clean"]` |
| Mutated | 2 | 2 | `could-not-evaluate` | `["assessment_input_invalid"]` |
| Restored | 0 | 0 | `clean` | `["assessment_clean"]` |

Pristine and restored stdout were identical, including the trailing newline:

```json
{"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 0, "finding_ids": ["assessment_clean"], "result": "clean"}
```

Mutated stdout:

```json
{"code": 2, "error": "duplicate JSON key: registration_time", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}
```

Thus baseline acceptance was established before interpreting rejection as a killed mutant. Every observed process exit matched its JSON code, and each result/finding-ID pair matched the expected detector outcome.

## Explicit C1-dependency review

The complete production source was inspected, including its separate selftest branch. The exercised path is `main` → `evaluate` → `check`. It imports only Python standard-library modules. Its file-content reads on this path are the supplied assessment JSON, each declared population file, and the root's `expected.json`. Population and expectations SHA-256 values are recomputed from those files' bytes at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py:112-126`.

There is no classifier import/call, transcript evaluation, C1 result lookup, external verifier execution, Git command, or network operation in this path. The only `subprocess.run` in the production file is in the unexercised `selftest` function, where it launches this same assessment gate rather than C1. `--check` and `--selftest` are mutually exclusive. The historical `history.c2_independent = false` check is a fixed comparison to the preserved round-20 artifact, not a lookup or use of current C1 classification/results.

**Conclusion:** source/call-path review verifies no C1 classifier/result dependency in this C2 assessment operation; no C1 code was executed by this probe. This conclusion does not authenticate the assessment author's real-world independence.

## Restoration, limitations, and authority

The single inserted line was removed even though it had already produced the expected rejection. The restored scratch hash exactly equals both the pristine scratch hash and frozen baseline hash. Re-running the same bounded detector on restored bytes returned the pristine stdout and exit code. Production, frozen inputs, sibling artifacts, VCS state/index, remotes, and host configuration were not edited. Only this advisory report and the restored inert scratch assessment were written.

This tests one duplicate-key neighbor of `baseline_valid`, not every malformed variant and not production-source mutation coverage. The baseline's timestamps are synthetic ordering assertions, not authenticated chronology. Oracle-author, independence, evidence, and named-verifier strings are declarations, not independently authenticated identities or proof; the baseline has `~` marks and makes no named-verifier claim. Subject-substring checks do not establish semantic truth, and the gate's own authority field explicitly excludes chronology/authorship/semantic-proof/promotion authentication. No promotion or round admission is asserted here.

**Tools installed or updated: none.** Existing Python and coreutils were used. The assigned mutation probe is complete; no full selftest was run.

Report: .ufo/waves/round-21/w2/reports/GateBaselineValid.md
