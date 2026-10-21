# GateCase1LateRegistrationAf — late registration after measurement

- **Finding ID:** `late_registration`
- **Verdict:** **SUPPORTED (artifact assertion only).** The frozen case produces the expected failing verdict, and a one-second-before-measurement neighbor is clean. This confirms the gate's classification for these supplied timestamp strings; it does not authenticate their truth or establish promotion/round-admission authority.
- **Axes:** frozen-case verdict; nearby false-positive discrimination; stable finding ID / process exit / JSON code and result; actual-byte hashes; absence of C1 classifier/result dependency; authority limits.

## Tested bytes and fixture

The tested production path was `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`.

- Actual source-byte SHA-256: `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7`.
- The parent-supplied candidate commit `f499a8db7171b7476fe9f204ab9edbac5a956fa9` exists locally; its `tools/mado-assessment.py` byte hash matched the tested working-tree file. The current checkout `HEAD` observed by `git rev-parse` was `a8da015624c92f4cb7a4de92adbf6643a3f8b38a`; conclusions are tied to the matching source hash, not a claim that these commit identifiers are equal.
- Frozen case: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/late_registration_after_measurement.json`, actual SHA-256 `1528c4ea88c3f46ae7cfcc4f0e4e22759c99a69fe9fa9aff8a0cfe35b4b15ee3`.
- Frozen expected file: actual SHA-256 `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e`; its `.cases[]` entry selected by `id == "late_registration_after_measurement"` expects code `1`, result `failed`.
- Population input bytes: `snapshots/population-baseline.txt`, actual SHA-256 `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`. The gate output's recomputed `actual_inputs` hash and expectations hash matched those actual-byte hashes.

The frozen case declares registration `2026-01-01T02:00:00Z`, measurement `2026-01-01T01:00:00Z`, and implementation `2026-01-01T03:00:00Z` (`late_registration_after_measurement.json:2-4`). The gate marks `late_registration` if registration is greater than or equal to implementation or any measurement (`tools/mado-assessment.py:91-105`), so the supplied ordering triggers that finding. The fixture's finding-ID mapping is `late_registration_after_measurement` → `late_registration` (`tools/mado-assessment.py:174-178`).

## Bounded execution and neighbor

Both invocations were synchronous, isolated Python `-I`, with `RLIMIT_AS` set by `ulimit -v 393216` (384 MiB) and a 15-second `timeout`; no selftest or suite was run.

Frozen gate command:

```text
ulimit -v 393216 && timeout 15s python3 -I tools/mado-assessment.py --root .ufo/waves/round-21/assessment-fixtures --check .ufo/waves/round-21/assessment-fixtures/cases/late_registration_after_measurement.json
```

Observed JSON stdout: `code=1`, `result=failed`, `finding_ids=["late_registration"]`, with the recomputed expectations/population hashes above. Process exit was `1`. These agree with the frozen expected code/result and the frozen case's mapped finding ID.

For the single nearby false-positive check, I copied the case to the private temporary directory `/tmp/mado-r21-late-registration-UqUfyU/registration_one_second_before_measurement.json` and changed only `registration_time` from `02:00:00Z` to `00:59:59Z` (one second before the unchanged `01:00:00Z` measurement). Actual altered-file SHA-256: `44410e3924d3c5174939ea48f077858bf49f707f89e79ff0449e0a9ee4453393`.

The same bounded command against that private artifact returned JSON `code=0`, `result=clean`, `finding_ids=["assessment_clean"]`, and process exit `0`. Thus the neighboring pre-measurement timestamp is not falsely labeled `late_registration`; all other checks still passed. The frozen fixture and production file were not edited.

## C1 dependency and authority review

The production imports are Python standard-library modules only (`tools/mado-assessment.py:8-15`). The invoked `--check` branch is `main` → `evaluate` → `check` (`:206-226`, `:158-163`); it parses the supplied assessment and reads/re-hashes the declared population and `expected.json` bytes (`:91-127`). It does not import, call, or look up a C1 classifier or C1 result. The only `subprocess.run` is in the separate `selftest` function (`:166-203`, call at `:190`), which was not invoked. No C1 code was run. The tool docstring also explicitly disclaims classifier, transcript evaluation, Git, host-state, and network consultation (`:2-7`).

**Limitations:** This validates only the gate's artifact-level rule over these bytes. Registration, measurement, and implementation timestamps are supplied assertions, not authenticated chronology. Oracle author/independence declarations and any named-verifier text are likewise not independently authenticated; the gate itself returns authority limited to artifact assertions, with no authenticated chronology, authorship, semantic proof, or promotion authority (`:152-155`). No independent judgment about actual preregistration or verifier identity is made.

No LSP device/server was exposed in this session, so `lsp` status, references, definition, and diagnostics could not be requested. Static observations above come from direct source reads and the two exact CLI outputs, not grep presented as semantic proof. No tools were installed or updated.

Report: .ufo/waves/round-21/w2/reports/GateCase1LateRegistrationAf.md
