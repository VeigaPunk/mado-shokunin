# GateCase11HistorySuppressesO — historical rewrite probe

- **Seat:** `MadoR21-2.GateCase11HistorySuppressesO-2`; advisory only, no promotion or round-admission authority.
- **Axes:** correct historical-rewrite verdict; nearby corrected-value false-positive control; stable finding/exit/result agreement; actual-byte identity; C1 independence; bounded execution and containment.
- **Verdict:** **No actionable defect found for this case.** The gate rejects the frozen claim of 175 passes out of 175 and accepts a one-field corrected control reporting the preserved 172/175. This is one artifact-level probe, not a production mutation or an independent historical-authentication claim.

## Exact tested source and fixture bytes

The tested production source was `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py`. `git rev-parse HEAD` observed candidate `f499a8db7171b7476fe9f204ab9edbac5a956fa9`.

Measured source SHA-256 before and after the two checks:

```text
5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7
```

Frozen case: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/history_suppresses_old_three_misses.json`.

Actual-byte hashes measured with `sha256sum`:

| Input | SHA-256 |
| --- | --- |
| Frozen case | `ff5a803b67a15c6ad8b5d7090611e93aee8518c705001d1dc7ba152dd785d708` |
| Frozen `expected.json` | `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e` |
| Frozen `snapshots/population-baseline.txt` | `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed` |
| Frozen `seal.json` | `99516c349637f2aefaef5c106ec7973c8af638bd4a22c79c835a49e0559fe686` |

The frozen oracle entry expects process code `1` and result `failed`; its reason is that the artifact rewrites 172/175 to 175/175. Production's case-ID mapping identifies `historical_target_rewritten` for this fixture (`mado-assessment.py:175-184`), and the check reports that ID when a history field differs from its fixed expected value (`:147-151`). The expected file and population snapshot were copied byte-for-byte into a private `/tmp/mado-gate-history.o2HGu3` root; their copied hashes matched the frozen files above.

## Nearby control and bounded executions

The single altered artifact was made from the frozen case in that private temporary root by changing only `history.round20_pass` from `175` to `172`; its SHA-256 was `58b0aa2d839d96e4243b36c021e08748ab0be8b94e400a9b535bd94d930bf10b`. All other fields and copied support files were unchanged. This is a one-field corrected-value control for the false-positive risk.

Each `--check` ran sequentially as its own isolated Python process, with `RLIMIT_AS=402653184` bytes (384 MiB), CPU limit 15 seconds, and an outer 15-second timeout. The process used `python3 -I`; no snippet or fixture text was executed. No selftest, full suite, corpus, or C1 scanner was run. The temporary root was removed by the probe's exit trap.

| Artifact | Process exit | JSON code | JSON result | Finding IDs |
| --- | ---: | ---: | --- | --- |
| Frozen historical rewrite | 1 | 1 | `failed` | `["historical_target_rewritten"]` |
| Corrected `round20_pass=172` control | 0 | 0 | `clean` | `["assessment_clean"]` |

Both outputs reported actual expectation digest `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e` and actual population input digest `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`. Thus the frozen code/result expectation and the production case-ID finding mapping agree with the observed original output, while the sole corrected history value clears the finding. The full selftest was not run.

## C1 dependency review

The source-only path is `main` → `evaluate` → `check` (`mado-assessment.py:206-226`, `:158-163`, `:91-155`). Imports are Python standard-library modules (`:8-15`). In `--check`, `check` loads the supplied JSON, hashes declared population-file bytes and the actual `expected.json` bytes, and compares the history values to fixed literals (`:107-127`, `:147-151`). It neither imports nor reads a C1 classifier, scanner output, counter, transcript, or result receipt. `history.c2_independent` is compared to the preserved `false` assertion; it is not obtained from current C1 results. The only `subprocess.run` is in the separate `selftest` branch (`:166-203`), which was not invoked. No C1 code was executed.

No LSP device/server was available in this seat's tool inventory, so no semantic reference query was possible; the C1 review is based on the directly read production call path, with literal search used only as corroboration. This is a source-level dependency review, not a runtime file-access audit.

## Residual risk and authority

The gate's output explicitly limits its authority to artifact assertions (`mado-assessment.py:152-155`). Timestamp syntax/order is not authenticated chronology. Oracle author/independence and named-verifier strings are assertions, not authenticated identities or proof; this fixture uses only `~` SHONEN marks, so it makes no named-verifier claim (the `x` check is only a string-pattern check at `:145-146`). Neither this probe nor its clean corrected control proves historical provenance, semantic evidence, verifier independence, promotion, or admission.

No tools were installed or updated. Existing Python 3.14.8, core utilities, and the existing `jq` command were used. No production or frozen input was edited; measured post-probe hashes for the production source, frozen case, expectations, and population snapshot matched their pre-probe hashes.

Report: .ufo/waves/round-21/w2/reports/GateCase11HistorySuppressesO.md
