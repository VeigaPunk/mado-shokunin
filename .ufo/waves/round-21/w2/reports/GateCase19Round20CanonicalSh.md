# Round-20 canonical SHONEN corrected case — C2 review

**Verdict: no actionable finding in the scoped artifact-only assessment.** The frozen corrected case produces the expected clean result, and one nearby negative-control variant is rejected with the expected stable finding ID and exit code. This is not an independent SHONEN approval or evidence-authenticity finding.

## Tested bytes and observations

- Production gate: `tools/mado-assessment.py`, SHA-256 `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7`. The observed repository HEAD was `f499a8db7171b7476fe9f204ab9edbac5a956fa9`; the file was clean in the working tree and last changed in `2ac0f9ba69051aea22cab3b6cfebe4d906b72d17`.
- Frozen case: `assessment-fixtures/cases/round20_canonical_shonen_corrected.json`, SHA-256 `72db0d2afd4f74ee176f7fb5c532f494bee59039e9f87641e1c8048656ddff7d`. Its one-per-box subjects match the four `SUBJECTS` constants (source lines 20–25); all four marks are `~`. The frozen oracle row expects code `0`, result `clean` (`assessment-fixtures/expected.json`, case `round20_canonical_shonen_corrected`).
- Inputs were copied byte-for-byte into private workspace `/tmp/round20-c2-seat19-fbkBfd` for execution; the copied case hash matches the frozen case. Direct SHA-256 of the copied `expected.json` was `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e`; direct SHA-256 of `snapshots/population-baseline.txt` was `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`. These match the case assertions and gate output's `actual_expectations_sha256` / `actual_inputs` values.
- Baseline command used isolated Python and an empty environment apart from `PATH`: `env -i PATH=/usr/bin:/bin /usr/bin/python3 -I …/tools/mado-assessment.py --root /tmp/round20-c2-seat19-fbkBfd --check …/cases/round20_canonical_shonen_corrected.json`. Observed JSON: `code: 0`, `result: clean`, `finding_ids: ["assessment_clean"]`, and shell exit `0`.
- One altered artifact, SHA-256 `c45590467d96a4cea5cc98c6fa1f1737f027225e431becc01761d73bb36eb211`, changed only box 1's mark from `~` to `x`, retaining its evidence without an explicit `non-author verifier:` name. Under the same isolated invocation it returned `code: 1`, `result: failed`, `finding_ids: ["unnamed_nonauthor_verifier"]`, and shell exit `1`. The result/ID mapping is consistent with the gate's `x` verifier check (source lines 140–146).

## C1 independence and limits

The C2 `--check` path is artifact-only: the source imports only Python standard-library modules (lines 8–15); its check reads the supplied bundle, asserted population files, and `expected.json` (lines 91–127), then validates the four declared boxes/history (lines 128–155). The CLI's `--check` branch calls `evaluate` directly (lines 216–220). The only subprocess call is in `--selftest`, which launches this same gate for frozen fixtures (lines 166–203); no selftest was run. No C1 classifier, counter, or result is imported, invoked, or supplied in the tested path. The isolated baseline and variant runs further show those results do not depend on user environment variables. This establishes no observed C1 dependency, not oracle independence/authenticity.

The gate itself explicitly limits its authority: its comment says the topic check does not establish whether evidence proves the subject (lines 142–144), and its output says chronology, authorship, semantic proof, and promotion authority are unauthenticated (line 155). The timestamps, `independent` boolean, author label, and any verifier name remain artifact assertions, not verified provenance. Therefore `clean` means this artifact passes the declared structural checks; it must not be reported as proof that the four SHONEN claims are true. A contradictory evidence string retaining the canonical subject phrase could still satisfy this subject check; that is a declared scope limitation, not a semantic certification.

## Verification gaps

- LSP was unavailable: reading `xd://lsp` returned “No such tool” and the mounted-device list had no LSP device. No LSP references/definition/diagnostics or grep-based semantic claim is reported; source citations above are direct file reads.
- Per assignment, no `--selftest`, full suite, corpus, or C1 classifier was run. Only the one frozen case and one private altered artifact were exercised.
- No tools were installed or updated.
