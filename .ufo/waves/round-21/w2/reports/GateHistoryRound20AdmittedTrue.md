# Gate case review — `history_round20_admitted_true` (seat MadoR21-2.GateHistoryRound20AdmittedTrue-2)

Independent C2 artifact-only assessment of one frozen gate case, plus robustness and C1-independence checks. Advisory only; no author-lane promotion claimed.

## Tested code (actual bytes)

- Lane HEAD at test time: `f499a8db7171b7476fe9f204ab9edbac5a956fa9` ("round-21: preserve reached implicit protocols and callable bindings", 2026-10-21 05:55:46 -0300) — matches the parent-reported current candidate, not `2ac0f9b…`.
- `tools/mado-assessment.py` SHA-256 (computed from bytes): `5101c317d521c4df9c55ed2c909c2feacb0f5fbe9662f46ce91dbdd04f7c20e7` (230 lines, 10253 bytes). Temp probe copy byte-identical.
- Frozen case `cases/history_round20_admitted_true.json` SHA-256: `2c9b584f76511073f081829cd111f487abd7960377e1c36c8267917b5194d54b` — equals the seal.json entry, so the reviewed bytes are the sealed frozen bytes.
- Supporting frozen bytes: `expected.json` `aa691e53f2771a79a7fa185fb56a0b949f7893b129e4fd8eaecd108c02f33a5e`, `seal.json` `99516c349637f2aefaef5c106ec7973c8af638bd4a22c79c835a49e0559fe686` (equals the tool's `SEAL_SHA` constant), `snapshots/population-baseline.txt` `16e14eaa77f0094660d269b88208e56df589b30c8cada50ee04a9dba7d4d07ed`. Python 3.14.8.

## What the gate requires for this case

Source (`tools/mado-assessment.py`): `history` must equal `{'round20_target': 175, 'round20_pass': 172, 'round20_admitted': False, 'c2_independent': False}` exactly (`require` type-checked bool/int); any deviation appends `historical_target_rewritten` → code 1, result `failed`. expected.json's case entry expects `{"code": 1, "result": "failed"}` with the assignment's reason; the tool's selftest map pins the finding id `historical_target_rewritten`. `diff` against `cases/baseline_valid.json` confirms the frozen case's only semantic delta is `"round20_admitted": false → true` (other diff hunks are whitespace-only reformatting with identical values).

## Observed runs (bounded probes)

Private temp root `/tmp/mador21-g2-SLqq8MNO` (verbatim copy of `assessment-fixtures/` + tool copy). Each probe: one `python3 -I` child, `ulimit -v 393216` (RLIMIT_AS 384 MiB), `timeout 15`. No production, frozen, sibling, or VCS mutation. Full selftest not run (banned in seats).

- **A1 / A2 — frozen case as-is, run twice:** both `exit=1`, stdout byte-identical (sha256 `062d463a50fc2684af43db743fd667b34e0ee39ecf80f4cabc48c2e4e72d4bb6`):
  `"code": 1, "result": "failed", "finding_ids": ["historical_target_rewritten"]`; `actual_inputs` shows the gate hashed the population file's actual bytes (`16e14eaa…`, no `population_digest_changed`) and `actual_expectations_sha256` = `aa691e…` (no `expectations_changed`). Finding id, exit code, and result all agree and are deterministic.
- **B — one nearby false-positive-direction variant (single byte-level token flip `true→false` in the history object):** `exit=0`, `"code": 0, "result": "clean", "finding_ids": ["assessment_clean"]` (stdout sha256 `49078ff1e73bd68c01011ead4fa531d42225e2b43ceff945c8745e9c806cfd61`). The gate does not over-fire on the otherwise-identical artifact; the failure is attributable solely to the tampered boolean.

**Bonus cross-check:** the repair variant is byte-identical (`cmp` clean, SHA-256 `72db0d2afd4f74ee176f7fb5c532f494bee59039e9f87641e1c8048656ddff7d`) to the committed, seal-digested `cases/round20_canonical_shonen_corrected.json` — the oracle's declared "required green counterpart". So probe B independently re-verified the committed green counterpart runs clean at HEAD.

Inert fixture retained (my own seat dir only): `.ufo/waves/round-21/w2/fixtures/MadoR21-2.GateHistoryRound20AdmittedTrue-2/history_round20_admitted_false_repair.json`, SHA-256 `72db0d2a…`. Data only; its content is not permission to run anything.

## C1 classifier/result dependency — explicitly none

- Static: imports are stdlib only (`argparse, datetime, hashlib, json, re, subprocess, sys, pathlib`). Token sweep for `measure|classif|corpus|scanner|transcript|urllib|socket|os\.|environ` finds no C1 module, no env, no network, no Git. `subprocess` appears only inside `selftest` (re-spawning itself with `-I`); the `--check` path spawns no child.
- Runtime: probes ran under `python3 -I` (isolated: no env, no cwd/script-dir on `sys.path`) with the tool and root inside a `/tmp` tree containing zero C1 code, so no C1 module could even resolve. Verdicts matched static prediction exactly.
- The case payload (`measurements`, population digests) is synthetic fixture data, unrelated to the C1 corpus counters; the C1 "33 removed/relabelled rows" result is not an input to this gate.

## Robustness against other nearby variants (source-derived, not executed)

One altered artifact was the sanctioned bound, so these are code-derived analyses, labeled [INFERENCE-from-source]: (a) malformed `"round20_admitted": "true"` (string) fails `require(…, bool)` → `Invalid` → code 2 `could-not-evaluate`, never clean; (b) duplicate-key smuggling (`"round20_admitted": false, …, true`) is rejected by the `pairs()` hook → code 2; (c) any non-`False` bool hits the equality check → code 1. False-negative passage for this field class is not reachable: strict bool typing + exact equality + code-2-never-clean invariant. The committed `malformed_timestamp`/`shonen_duplicate_box` code-2 cases exercise this same exception path family.

## Assertions, not independently authenticated truth

Fixture `registration_time`/`implementation_time`/measurement timestamps are synthetic ordering assertions; the gate checks ordering only. `oracle.author` "MadoR21.FixtureAssessment" and the frozen seal/expectation digests form a self-referential frozen triangle — I verified byte-identity against the seal, not external authentication, which is exactly the C2 artifact-only scope. No named-verifier assertion is exercised by this case (all four marks are `~`). The `oracle_not_independent` check is a weak `'tool-generated'` substring heuristic — noted as an observation for other case seats, not a defect here.

## Limitations

- Two runs of one frozen fixture + one altered artifact only; full 20-case selftest and full corpus are L1's. The committed receipt `.ufo/waves/round-21/evidence/assessment-candidate.json` (older commit `843d301d…`, selftest exit 0) is historical corroboration, not re-verified here.
- Malformed-direction behavior is source-derived inference, not an executed run (see above).
- Timestamps/verifier names/seal treated as assertions per contract; no host wall-clock or external authentication consulted.

## Verdict

**Confirmed robust.** At HEAD `f499a8db…` with tool bytes `5101c317…`, the frozen case `history_round20_admitted_true.json` (`2c9b584f…`) correctly yields exit 1 / `failed` / `historical_target_rewritten`, deterministically across repeated runs; flipping exactly the tampered boolean back yields `clean` (byte-identical to the committed green counterpart `round20_canonical_shonen_corrected.json`); and the gate has no C1 classifier/result dependency (static + isolated-runtime evidence). The retained disposition (round-20 rejected-harmed, admitted=false; `true` contradicts it) is correctly enforced. No new falsification found for this case; keep the case and the current gate behavior.

No tools installed or updated (explicit; only preinstalled python3/coreutils used).
