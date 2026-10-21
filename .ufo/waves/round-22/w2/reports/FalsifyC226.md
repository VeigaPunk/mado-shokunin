# C2 falsification — AuditRawSnapshotAtLimit

- Seat: `MadoR22.FalsifyC226` (author-lane advisory attack only; NOT non-author admission)
- Delivered revision: `71228fd582d6d9338d7916cc64e69bd4c2e928b5`
- Case: `.ufo/waves/round-22/audit/fixtures/cases/AuditRawSnapshotAtLimit/`
- Receipt (own dir): `.ufo/waves/round-22/w2/receipts/FalsifyC226/result.json` + `stdout.txt`, `stderr.txt`, `exit.txt`, `timing.txt`
- Installations/updates: none. No fixture/tool/expected/production edits by this seat.

## Fixed identities (checked before and after)

| Artifact | SHA-256 |
|---|---|
| `tools/mado-evidence-audit.py` before | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| `tools/mado-evidence-audit.py` after | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| `.ufo/waves/round-22/audit/fixtures/expected.json` | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| case `bundle.json` | `cb74f4c1988a29d27b1393f3c4202d6a14cdde773e7efd981760a1c44b608367` (equals `expected.bundle_sha256`) |
| case `root/snapshot.json` | `5b87c1dae2b1baac67e1796a91e29130cc6cb892d73034bf1f3c646f13a7f58b` (equals `bundle.sha256` and `expected.snapshot_sha256`) |
| `audit/fixtures/inputs/audit-contract.json` | `e65d165a1599c2d8743509bfb09ef46df9b8cc9038246b80cdef1780b5fdf23f` (equals `expected.contract`) |

No drift; the fixed identity was not moved.

## Executed command (the ONE authorized measurement)

```
cd .ufo/waves/round-22/w2/receipts/FalsifyC226
timeout -s KILL 15 prlimit --as=402653184 --cpu=15 -- \
  python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py \
  --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawSnapshotAtLimit/bundle.json \
  --root  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawSnapshotAtLimit/root
```

Caps: 384 MiB address space (`402653184`), 15 s wall (`timeout -s KILL`) and 15 s CPU, one scanner child. No 46-case selftest, no measurement driver, no oracle/full-corpus run.

## Observed

- exit code `0`; wall elapsed `36,860,959 ns`; stderr empty (0 bytes, `e3b0c44…b855`).
- stdout (`ed2ef3e2b2fe1f6f78b1182392a5b5b9746c9467256afaf02fb543d3097cc4c9`):

```json
{"actual_counts": {"errors": 0, "lead": 0, "observed": 0, "total": 0}, "actual_snapshot_sha256": "5b87c1dae2b1baac67e1796a91e29130cc6cb892d73034bf1f3c646f13a7f58b", "authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 0, "finding_ids": ["evidence_audit_clean"], "result": "clean"}
```

- Observed verdict: `code 0`, `["evidence_audit_clean"]`, actual counts `0/0/0/0`, snapshot digest as declared.
- Frozen expectation (`expected.json`): `code 0`, `["evidence_audit_clean"]`. **Observed match: yes.**

## Independent derivation (raw bytes → verdict, not from classifier output)

Derived before reading the run's stdout, from bytes, tool source and the contract:

1. **Size boundary.** `stat` size is exactly `2097152` = `2*1024*1024` = `MAX_BYTES`. `bounded()` does `stream.read(MAX_BYTES + 1)` and rejects only when `len(raw) > MAX_BYTES`; a regular 2 MiB file yields 2,097,152 bytes, which is not `> 2,097,152`. At-limit is therefore **accepted**; the reject predicate is `>`, not `>=`. Bytes beyond the JSON object are `0x20` spaces only (verified tail via `od`), which `json.loads` accepts as trailing whitespace.
2. **Digest before decode.** `bounded()` returns raw bytes; `check()` computes `hashlib.sha256(raw)` and compares to `bundle.sha256` *before* `parse(raw)`. Recomputed independently with `sha256sum`: `5b87c1…a7f58b`, equal to the declaration. No verdict is produced from undigested bytes.
3. **Strict schema.** Bundle keys exactly `{claim, sha256, snapshot}`; `snapshot` is the simple relative `snapshot.json` (non-empty, no `.`/`..`/backslash/absolute part). Claim `total/observed/lead/errors` are exact `int` zero (`type(v) is int`; `true` would be rejected because `type(True) is bool`), `clean` is exact `bool true`. Snapshot: `findings` is a list (legitimately empty), `files` is a non-empty list of one object with `eval_unparsed: 0`, `unparsed_spawns: 0` exact ints. Duplicate-key, nonfinite and negative-count rejection paths are not triggered.
4. **Arithmetic.** `total = len(findings) = 0`; `observed = 0`, `lead = 0` (no rows to count); `errors = 0 + 0 = 0` (per-file counters summed, no dedup). Declared `0/0/0/0` equals actual, so no `*_count_mismatch`; `clean:true` together with actual `errors == 0` and actual `total == 0` raises neither `uncertain_scan_claimed_clean` nor `findings_claimed_clean`.
5. **Containment.** `root_path()` requires no symlink on `root` or any ancestor; independent scan of `/home`, `/home/vgpnk`, `/home/vgpnk/Projects`, `/home/vgpnk/Projects/shokunin`, `/home/vgpnk/Projects/shokunin/mado-shokunin` and the case root found none. `snapshot.json` is a regular non-symlink file whose resolved path stays under the root.
6. **Result mapping.** Empty failure list yields `failures or ['evidence_audit_clean']`; `result(0, …)`; `main()` returns `output['code']` as the process exit, so exit `0`. Code `2` here would mean could-not-evaluate (invalid/unavailable input), never `clean` or `failed`.

Derived verdict from that walk: `code 0`, `["evidence_audit_clean"]`, actual counts `0/0/0/0`. It matches the observed run and the frozen expectation.

## Boundary semantics (contradiction retained, not normalized)

The contract rule text is ambiguous: `audit-contract.json` says "all snapshot bytes are bounded to 2MiB", and `audit-clarifications.md` says "Inputs are bounded to2MiB"; neither sentence alone decides whether exactly 2,097,152 bytes is allowed. The case proposal marked itself contingent for exactly this reason. `expected.json` `eligibility_log` records `decision: include` with `ruling: "included by Main's preimplementation ruling: 2 MiB is inclusive (<= 2097152 bytes); original contingent text retained"`. So the frozen expectation `0/evidence_audit_clean` is coherent with the recorded inclusive ruling, and the tool implements that reading (`>` reject). Under an exclusive reading the same case would be `2/evidence_audit_input_invalid`. This seat retains the wording ambiguity as a governance-recorded ruling; it did not independently authenticate the ruling's pre-implementation chronology beyond the sealed bytes, and it did not change any expectation.

## Axes relevant to THIS case

| Axis | Finding |
|---|---|
| Row/line grain | PASS. Zero finding rows, exactly one file row; totals come from `len(findings)` and per-row counter sums, so no line-vs-row inflation is possible here. Empty `files` would be invalid (not triggered). |
| Digest before decode | PASS. Source order is digest → compare → parse; this case's digest matched. |
| Signed / bool / nonfinite counts | PASS on shape and source (`type(v) is int`, `< 0` reject, `finite()` + `parse_constant` reject); **not adversarially exercised by this case** (all values are exact int zero / exact bool true). |
| Path / symlink / size boundary | PASS. No symlink on root or ancestors, regular non-symlink snapshot inside root, and exactly-at-limit bytes accepted. This case is the *at-limit accept* discriminator only; oversize rejection is the sibling case. |
| Truthful authority | PASS string-equal to the contract authority line; output reports counts and a byte digest, and claims nothing about semantic correctness, authentication, admission or promotion. |

## What this does NOT establish

- No mutant was executed by this seat. The expectation claims this case discards a `>=`-style reject mutant, but that is a *proposed* mutant property: the observed run only proves the delivered tool accepts exactly 2 MiB. A mutant kill must be run by L1 in its private sandbox, and must not be called killed on this advisory report.
- Nothing about oversize-input refusal, bundle-vs-snapshot bound ordering, markerless/derived-row C3 history, removal/no-harm comparisons, roster or admission.
- No semantic-precision credit. The historical markerless actual r19 receipt remains code `2` could-not-evaluate; derived 5-observed/1-lead-line or 10-observed/1-lead-row populations require explicit derivation provenance; all-observed inflation claims are new counterfactuals, not actual r19 claims. This case is a new at-limit boundary counterfactual and says nothing to the contrary.
- Exit `2` is could-not-evaluate throughout; this run's `0` is an artifact-consistency verdict only.

## Uncertainty / residual gaps

1. Inclusive-vs-exclusive bound rests on the recorded Main ruling, not on unambiguous contract prose (retained above).
2. The case does not discriminate bool/negative/nonfinite count handling; those remain source-read claims of this seat, not measured by this fixture.
3. Exactly 2 MiB acceptance depends on `BufferedReader.read(n)` returning all available bytes for a regular file; observed empirically accepted here, and `is_file()`/`is_symlink()` gate special files, but this was not probed with a short-read producer.
4. Independent corroboration of the same `0/evidence_audit_clean` exists in prior wave output, but it was not used to derive this verdict (per assignment); the derivation above stands on bytes and source.

Report: .ufo/waves/round-22/w2/reports/FalsifyC226.md
