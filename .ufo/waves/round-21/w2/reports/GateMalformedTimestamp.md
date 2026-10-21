# GateMalformedTimestamp — bounded C2 assessment

- **Case:** `malformed_timestamp`
- **Verdict:** **Supported for the frozen case and one nearby malformed-date variant; no defect found.** The frozen registration timestamp cannot be parsed as a real date/time, so ordering is not evaluated; the gate returns `could-not-evaluate`. A second calendar-invalid timestamp with an otherwise accepted timestamp shape also fails closed with the same finding ID, JSON code, and process exit.
- **Axes:** calendar-timestamp rejection; nearby malformed-date false-negative control; finding-ID/JSON-code/process-exit agreement; actual-byte identity; absence of C1 classifier/result dependency.
- **Candidate identity:** The initial checkout read returned `HEAD` `f499a8db7171b7476fe9f204ab9edbac5a956fa9` (matching the parent notice). A later read during concurrent integration returned `a8da015624c92f4cb4a7de92adbf6643a3f8b38a`. The tested identity is therefore the exact production-file bytes, not an assertion that `HEAD` remained fixed.

## Exact bytes and scope

Production assessed without modification:

`/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`

Its SHA-256 was `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7` at initial capture and again after the probes. The scoped `git status --short` read showed no worktree changes for the production script or the frozen case/dependency paths listed below.

Frozen case:

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/malformed_timestamp.json`

Its SHA-256 was `e70873dfdf89082204da565ffcfb47b818f1c2fa67b73e5047ea9c316428793e`. The input's `registration_time` is `2026-19-42T29:61:61Z`. The registered expectation at `assessment-fixtures/expected.json:146-149` is code `2`, result `could-not-evaluate`, with reason “registration_time is not a valid timestamp, so ordering cannot be evaluated safely.” The expected file's actual SHA-256 is `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e`; the actual population bytes at `snapshots/population-baseline.txt` hash to `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`. The seal's actual SHA-256 is `99516c349637f2aefaef5c106ec7973c8af638bd4a22c79c835a49e0559fe686`.

## Nearby variant and bounded results

One inert variant was written outside the checkout at:

`/tmp/gate_malformed_ts_seat/variant_2025feb30.json`

Its SHA-256 is `a8c48bd124a2615ed387819ea94b269e348bc3bd47f24787e89443a2c736596a`. A parsed-field comparison confirmed it is identical to the frozen artifact except for `registration_time`, changed to `2025-02-30T00:00:00Z`. This value matches the timestamp-shape regex but is not a valid calendar date, and (if invalid dates were improperly accepted/coerced) its year would make it precede the other fixture timestamps. It therefore probes the nearby false-negative where a shape-only check could incorrectly permit ordering.

Each input was first run directly and then repeated with `ulimit -v 393216` (384 MiB), `/usr/bin/timeout 15s`, and `python3 3.14.8 -I -B`, using one `--check` process per input and the frozen assessment root read-only. The bounded results matched the initial direct results. No selftest, full suite, corpus, or C1 code was run.

| Input | Frozen expected | Process exit | JSON `code` | JSON `result` | Finding IDs |
| --- | --- | ---: | ---: | --- | --- |
| Frozen `malformed_timestamp` | code 2, `could-not-evaluate` | 2 | 2 | `could-not-evaluate` | `assessment_input_invalid` |
| Variant, registration `2025-02-30T00:00:00Z` | nearby probe; invalid date should not be ordered | 2 | 2 | `could-not-evaluate` | `assessment_input_invalid` |

Bounded frozen-case stdout:

```json
{"code": 2, "error": "month must be in 1..12, not 19", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}
```

Bounded variant stdout:

```json
{"code": 2, "error": "day 30 must be in range 1..28 for month 2 in year 2025", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}
```

The frozen `expected.json` records code and result, not a finding ID. The selftest mapping at `mado-assessment.py:193-197` defaults an unmapped nonzero case such as `malformed_timestamp` to `assessment_input_invalid`, and requires process exit, JSON code, result, and that finding to agree. Both observed tuples satisfy those conditions. The implementation at `:76-82` first constrains timestamp shape and then calls `datetime.fromisoformat`; invalid calendar values raise `ValueError`. The `evaluate` path at `:158-163` converts that error to code `2`, `could-not-evaluate`, and `assessment_input_invalid`. Thus the accepted shape alone cannot make either invalid calendar timestamp clean or cause a chronology comparison.

## Explicit C1-dependency review

The exercised source path is CLI `--check` → `evaluate` → `check` (`mado-assessment.py:91-105, 158-163, 206-230`). The timestamp decision consumes only the supplied artifact's timestamp strings; subsequent checks read local population bytes and `expected.json` (`:107-126`). The script's imports are standard-library modules (`:8-15`); there is no C1 classifier import, C1 result lookup, transcript evaluation, or network access in this path. Although `subprocess` is imported, its use is in the separate `--selftest` branch (`:188-191`), which was not invoked. The script docstring (`:2-6`) and seal text (`seal.json:6`) likewise declare a no-classifier/C2-only scope; those declarations are supporting artifact assertions, not independent authentication. No C1 code or result was run or consumed for this assessment.

No LSP device/server was mounted for this seat: attempting to read `xd://lsp` returned “No such tool.” I used literal source search followed by direct relevant source reads and the bounded runtime behavior; source-search output alone is not presented as semantic proof, and no LSP-indexed reference proof is available.

## Limits and authority

The timestamp strings are synthetic syntax/order assertions, not authenticated wall-clock chronology. Oracle author/independence fields, SHONEN evidence, and named-verifier strings are assertions, not authenticated identities or independent proof. These probes establish neither the truth of those assertions nor overall C1 independence, semantic proof, promotion authority, or round admission. Coverage is limited to this frozen case and one altered timestamp variant, not the full fixture corpus.

No production or frozen file was edited. No tool was installed or updated; existing Python, Bash, `timeout`, and coreutils were used. No full selftest was run.

Report: `.ufo/waves/round-21/w2/reports/GateMalformedTimestamp.md`
