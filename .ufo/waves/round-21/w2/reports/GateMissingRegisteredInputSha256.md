# GateMissingRegisteredInputSha256 — bounded C2 assessment

- **Case:** `missing_registered_input_sha256`
- **Verdict:** **Supported for the frozen case and one nearby control; no defect found.** The frozen artifact correctly yields `could-not-evaluate` because the required registered `population[].sha256` is absent. A nearby valid-digest control becomes clean when that one missing field is supplied from the actual population bytes.
- **Axes:** required-field rejection; nearby valid-input false-negative control; finding-ID/JSON-code/process-exit agreement; actual-byte hash authority; C2 independence from C1 execution/results.
- **Candidate:** current checkout candidate `f499a8db7171b7476fe9f204ab9edbac5a956fa9` (observed `HEAD`).

## Exact bytes and scope

Production assessed without modification:

`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`

Its actual SHA-256 was `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7` before the probes and again after them.

Frozen case:

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/missing_registered_input_sha256.json`

The frozen case SHA-256 was `2e039dc4e8ee7d02a1b7fa194ae8b6f436dc7c600ea8ede6e4d605f71c5f72a6` before and after. Its frozen expectation states code `2`, result `could-not-evaluate`, and the missing-registered-digest reason.

Actual dependency bytes, independently hashed from the files:

| Input | SHA-256 |
| --- | --- |
| `assessment-fixtures/expected.json` | `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e` |
| `assessment-fixtures/snapshots/population-baseline.txt` | `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed` |

The population bytes hash matches the case's `actual_sha256` assertion. It does **not** supply the absent registered `sha256` field.

## Nearby variant and bounded results

I wrote one inert scratch variant at:

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/GateMissingRegisteredInputSha256-2/missing_registered_input_sha256-restored.json`

It preserves the case fields and adds the omitted `population[0].sha256` with `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`, independently obtained by hashing the referenced population file's bytes. The scratch variant SHA-256 is `72db0d2afd4f74ee176f7fb5c532f494bee59039e9f87641e1c8048656ddff7d`.

Each of the two `--check` invocations ran as one Python gate process, with `ulimit -v 393216` (393216 KiB = 402653184 bytes, 384 MiB), a 15-second tool timeout, and `python -I -B`. Both used the frozen assessment root read-only; no selftest, suite, corpus, or C1 code ran.

| Input | Process exit | JSON `code` | JSON `result` | Finding IDs |
| --- | ---: | ---: | --- | --- |
| Frozen missing-digest case | 2 | 2 | `could-not-evaluate` | `assessment_input_invalid` |
| Scratch with registered digest restored | 0 | 0 | `clean` | `assessment_clean` |

Frozen-case stdout:

```json
{"code": 2, "error": "missing or invalid sha256", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}
```

Nearby-control stdout:

```json
{"actual_expectations_sha256": "aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e", "actual_inputs": [{"path": "snapshots/population-baseline.txt", "sha256": "16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed"}], "authority": "artifact assertions only; no authenticated chronology, authorship, semantic proof or promotion authority", "code": 0, "finding_ids": ["assessment_clean"], "result": "clean"}
```

The frozen code/result and the default code-2 finding mapping agree with the observed exit, JSON code, result, and finding ID. The valid-digest neighbor also returns a coherent clean tuple; this rules out the nearby false-negative where the gate would reject the same otherwise-valid artifact after its registered digest is restored. Source lines 107–116 require and validate `sha256`, hash the file's actual bytes, and compare those bytes to the registered value; `actual_sha256` is not used as a fallback.

Two initial shell-wrapper attempts failed before starting the gate (`exec` was not dispatched as a shell builtin). The reported results above are from the subsequent explicit `/usr/bin/bash -c` bounded invocations; no extra gate evaluation occurred in the failed wrapper attempts.

## Explicit C1-dependency review

The exercised source path is `main` → `evaluate` → `check` (`mado-assessment.py:91–163,206–230`). It reads the supplied JSON, each listed population file, and root `expected.json`; helper reads and hashes are local file operations (`:41–67,112–126`). The `--check` branch has no classifier call/import, transcript evaluation, C1-result lookup, external-verifier execution, Git operation, or network operation. The only `subprocess.run` is in the separate `selftest` branch (`:166–203`); `--check` and `--selftest` are mutually exclusive. No C1 code was executed.

No LSP device/server was available in the mounted tools for this seat. Symbol discovery used literal search, while the dependency conclusion above comes from direct source reads of the entry point, helper path, complete `check`/`evaluate` path, and separate selftest branch; this is not an LSP-indexed semantic proof.

## Limits and authority

The artifact timestamp strings are syntax/order assertions, not independently authenticated chronology. Oracle author/independence fields, SHONEN evidence, and any named-verifier strings are assertions, not authenticated identities or independent proof; the probe establishes no real-world verifier independence, semantic truth, C1 independence, promotion authority, or round admission. This result covers the frozen case and one nearby valid-digest control only, not the entire assessment corpus.

Production, frozen case, expected file, and population bytes retained the same hashes across the probe. No production or frozen file was edited. No tool was installed or updated; existing Bash, Python, and coreutils were used. No full selftest was run.

Report: `.ufo/waves/round-21/w2/reports/GateMissingRegisteredInputSha256.md`
