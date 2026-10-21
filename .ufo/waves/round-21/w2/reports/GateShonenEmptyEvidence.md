# GateShonenEmptyEvidence

## Verdict

The frozen `shonen_empty_evidence` expectation is robust for the reported defect. Both the frozen empty string and a nearby whitespace-only evidence value produce the same invalid-input verdict: exit/code `2`, result `could-not-evaluate`, finding ID `assessment_input_invalid`. Empty or whitespace-only evidence leaves a required row unevaluable; it should not be accepted as clean or treated as a claim whose truth was evaluated.

## Exact artifacts

SHA-256 values below were computed from the actual file bytes. The tested production source was `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-assessment.py` (`5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7`).

- Frozen input `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/cases/shonen_empty_evidence.json`: `7e63401aa4a03a70faad901c15a03061bfe55b319b1f4e50bb343e2c712ccee2`. This matches its entry in `seal.json`.
- Frozen expectation `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/expected.json`: `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e`.
- Seal `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/seal.json`: `99516c349637f2aefaef5c106ec7973c8af638bd4a22c79c835a49e0559fe686`.
- Population bytes `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/assessment-fixtures/snapshots/population-baseline.txt`: `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`.
- One inert nearby variant, `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/GateShonenEmptyEvidence-2/empty-evidence-whitespace.json`: `0f3bf17c46e53b3e65e6961980b6661f00cfa084e175d1e30084fd35ef98dcb0`. It changes only box 2's evidence value to whitespace (space, tab, newline, space); the other assessment fields remain as in the frozen case.

The frozen expected row in `expected.json:122-125` specifies code `2` and `could-not-evaluate`. It does not enumerate a finding ID. The gate's selftest mapping at `mado-assessment.py:193-197` defaults an expected code-2 case without a special mapping to `assessment_input_invalid`, which is the observed stable ID.

## Bounded observations

Each probe was one synchronous `/usr/bin/python -I -B` child with a 15-second timeout; the shell set the virtual-memory limit to 393216 KiB (384 MiB) before both children. No selftest or corpus was run.

| Input | Observed stdout | Exit |
|---|---|---:|
| Frozen case | `{"code": 2, "error": "empty assessment evidence", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}` | 2 |
| Whitespace-only variant | `{"code": 2, "error": "empty assessment evidence", "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}` | 2 |

The predicate at `mado-assessment.py:136-139` rejects `not evidence.strip()` by raising `Invalid`; `evaluate()` at `158-163` turns that into the observed code-2 result. This catches both the exact frozen empty string and whitespace-only near variant. The behavior is consistent with an invalid required assessment row, rather than a substantive assessment failure (`code 1`).

## C1 independence and evidence limits

The `--check` route is `main()` → `evaluate()` → `check()` (`mado-assessment.py:206-226, 158-163, 91-155`). The inspected imports (`8-15`) are Python standard-library modules only. The check path reads the supplied bundle, rooted population file(s), and `expected.json`; it computes the relevant file digests from bytes. It does not import/call a C1 classifier or look up/consume a C1 result. `subprocess.run` occurs in the separate selftest path (`166-203`), not this `--check` path; the fixed `history.c2_independent == false` comparison is an artifact assertion, not a current C1 result lookup. No C1 code was run.

No `lsp` device is mounted (`read xd://lsp` reported “No such tool”), so definition/call tracing used direct reads of the selected source ranges; text search was navigational only.

This gate establishes only that the artifact contains nonempty evidence and passes its configured structural checks. Its timestamps, oracle-author string, verifier names, and assessment text are assertions, not independently authenticated chronology, authorship, reviewer identity, or semantic proof. In particular, the empty-evidence result does not independently establish whether the underlying box-2 claim is true. No tools were installed.