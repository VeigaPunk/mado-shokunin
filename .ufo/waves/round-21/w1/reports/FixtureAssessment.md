# Round 21 C2 artifact fixture assessment

## Scope and result

Authored an independent artifact-only expectation set for the new registration-integrity capability. No classifier or gate was implemented or run, and no tool measurements, build, lint, test, formatter, or host probe was performed. The expected bundle is fixed before gate implementation; this seat claims no gate outcome or historical capability.

The registration clarification states the pre-change capability is absent and disallows a fabricated permissive historical baseline. Accordingly, this set does not model a green historical gate: it pairs the real rejected round-20 wrong-topic SHONEN artifact with a corrected canonical assessment, and specifies the frozen valid/invalid cases for the future gate.

## Files authored

All fixture files are within `/tmp/mado-r21-assessment-external/.ufo/waves/round-21/assessment-fixtures/`:

- `expected.json` — independent stable IDs, case rationales, explicit numeric result mapping, schema rules, and historical transcription.
- `expectations-changed.json` — a separate deliberately altered expectations source for the digest-mismatch case.
- `snapshots/population-baseline.txt` and `snapshots/population-mutated.txt` — real local population bytes, not caller-supplied stand-ins.
- `cases/` — 20 standalone input JSON files:
  `baseline_valid.json`, `late_registration_after_measurement.json`, `late_registration_after_implementation.json`, `population_file_mutated.json`, `missing_registered_input_sha256.json`, `oracle_tool_generated_not_independent.json`, `expectation_digest_changed.json`, `shonen_missing_box.json`, `shonen_duplicate_box.json`, `shonen_x_without_nonauthor.json`, `shonen_empty_evidence.json`, `history_suppresses_old_three_misses.json`, `history_round20_admitted_true.json`, `history_c2_independent_true.json`, `malformed_timestamp.json`, `population_empty.json`, `oracle_author_missing.json`, `shonen_x_with_named_nonauthor.json`, `round20_wrong_topic_shonen.json`, and `round20_canonical_shonen_corrected.json`.

`expected.json` maps `0` to `clean`, `1` to `failed`, and `2` to `could-not-evaluate`, with each case's code and result recorded explicitly. Expected partition: clean = baseline, named-non-author positive control, corrected canonical SHONEN; failed = both late-registration cases, changed population, tool-generated oracle, changed expectations, unsupported `[x]`, suppressed old misses, changed old admission, claimed old C2 independence, and historical wrong-topic SHONEN; could-not-evaluate = missing frozen digest, missing/duplicate SHONEN box, empty evidence, malformed timestamp, empty population, and missing oracle author.

The per-input population `path` fields are fixture-root-relative (`snapshots/...`), resolved by the future gate's `--root`. The mutated case points at bytes whose digest differs from the frozen `sha256`; its `actual_sha256` is advisory and must not be trusted instead of hashing the pointed-to file. The missing-input-digest case removes the frozen `sha256` while leaving the advisory field present.

Timestamps are deliberately synthetic RFC3339 ordering values. They test only the artifact-level ordering assertion and do not authenticate wall-clock events or commit ancestry. The positive `[x]` case uses `FixtureVerifier-Q7` as a synthetic test identity only; it is not a real verification claim.

## Independent semantic anchors retained

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/registration.md:7-9,21` defines the registered target, the artifact-only C2 scope, absence of a historical gate, the no-fake-baseline rule, actual snapshot hashing requirement, and timestamp evidence limit.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-20-verifier-spotcheck.md:5,24,40,50-52` records rejected-harmed/admitted-false, the three misses at 172/175 against unchanged 175, the four-row SHONEN subject error, and C2's lack of independent calibration.
- `/home/vgpnk/Projects/shokunin/.ufo/reports/round-20/mado.md:65-68` was read directly. The wrong-topic case retains the original four rows verbatim as inert `evidence` strings: claims measured with receipts; no axis harmed; sources curated; mistake mined. These are deliberately not converted into canonical box claims.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/SHONEN.md:5-12` supplies the corrected canonical four subjects used by the positive corrected fixture: skill decision tables/sources, logged end-to-end domain task, oral-context-free instructions, and no cross-domain bleed. The corrected fixture preserves honest `~` marks; the schema-positive `x` fixture is separate and synthetic.

## Retained content digests

SHA-256 values were obtained from the written local bytes (no gate was invoked):

- Baseline population bytes `/tmp/mado-r21-assessment-external/.ufo/waves/round-21/assessment-fixtures/snapshots/population-baseline.txt`: `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed` (registered and observed digest).
- Mutated population bytes `/tmp/mado-r21-assessment-external/.ufo/waves/round-21/assessment-fixtures/snapshots/population-mutated.txt`: `c02069a203b8c1306e61b8470c8fe916e08fd5db23fd433c95b6f87ed82e84fc` (registered digest remains the baseline digest above).
- Pre-normalization raw source receipt for `/tmp/mado-r21-assessment-external/.ufo/waves/round-21/assessment-fixtures/expected.json`: `047a37a14107593a808f415d64678a3fe3e59ba962ab7e51bfb828fd8d3d81b0` (captured before fixture data-reference normalization; retained as provenance, not the current input digest).
- Normalized `/tmp/mado-r21-assessment-external/.ufo/waves/round-21/assessment-fixtures/expected.json`: `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e` (current and registered expectation digest in normal inputs after fixture-root-relative data-reference normalization).
- Altered expectations source `/tmp/mado-r21-assessment-external/.ufo/waves/round-21/assessment-fixtures/expectations-changed.json`: `c084335adf5c2191e2561c5207faaaf565e3cfe69f0e9e04ee6a94e6adf1a266` (used only as the changed current digest; the registered digest stays bound to `expected.json`).

## Limitations

This is an oracle specification and fixture population, not a measured result. Fixture data references resolve relative to the assessment-fixture root supplied via `--root`; report and tool read/write paths remain absolute. Historical report path fragments inside the wrong-topic evidence strings are preserved as quoted source text only. No tools were installed or updated.
