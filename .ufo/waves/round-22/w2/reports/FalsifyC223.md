# FalsifyC223 — C2 AuditRawPathDotDotInternal (fresh falsification, revision 71228fd582d6d9338d7916cc64e69bd4c2e928b5)

Date: 2026-10-21. Lane: author-lane advisory, leaf seat, no subagent dispatch. Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC223/result.json`.

## Findings by severity

### Critical
None.

### Major
None.

### Minor
None.

### Informational
- **Observed match, independent derivation.** I derived the verdict **before** running the probe, from raw bytes/declared counts/strict schema, not from any prior classifier output:
  1. `bundle.json` (sha256 `5533101c5e37464787e0f671af9495357433c3bbed0caa66ae5cbc8b58e58c02`, 224 bytes — recomputed, matches `expected.json` `bundle_sha256`) declares `snapshot = "sub/../snapshot.json"`, `sha256 = 3972b1f5…99c`, and claim `{clean:true, total:0, observed:0, lead:0, errors:0}` (all counts exact ints, `clean` exact bool — schema-valid, so arithmetic alone would not reject).
  2. `root/snapshot.json` (sha256 `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c`, 104 bytes — recomputed, matches both the declared digest and `expected.json`) is `{files:[{eval_unparsed:0, unparsed_spawns:0}], findings:[]}`: a genuinely clean, nonempty-files snapshot.
  3. Presealed lexical rule: `.ufo/waves/round-22/audit-clarifications.md` line 5 — "Reject absolute, empty, **dot/dotdot**, backslash paths and every symlink component." `'sub/../snapshot.json'.split('/')` contains `'..'`, so the input is invalid **lexically, independent of resolution**. Since the resolved path (`root/snapshot.json`) is a regular in-root file with the correct digest and consistent all-zero clean claim, the only correct verdict is `code 2 / ["evidence_audit_input_invalid"]` — could-not-evaluate, never false-clean `0/evidence_audit_clean`, never `failed 1`. This is exactly the mutant-kill the case was designed for (a containment-only check would answer 0/clean).
- **Authorized probe result (the ONE assigned measurement, only run performed).** Command: `python3 -I tools/mado-evidence-audit.py --check <case>/bundle.json --root <case>/root` under `ulimit -v 393216` (384 MiB) + `timeout 15`, one child, no selftest, no measurement driver.
  - exit **2**; stdout exactly: `{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}`; stderr empty.
  - **Observed == independently derived == expected.json (code 2, `["evidence_audit_input_invalid"]`). MATCH.**
- **Candidate check site (read-only, source as data).** `tools/mado-evidence-audit.py` `relative()` (lines 77–85) raises `Invalid('invalid relative path')` for any part in `('', '.', '..')`; `Invalid(ValueError)` propagates from `check()` via `rooted()` **before** snapshot bytes are read or hashed (lexical rejection precedes digest/decode — consistent with the digest-before-decode ordering; on this path the tool never computes the snapshot digest at all). `evaluate()` (lines 163–169) catches `ValueError` → `result(2, ['evidence_audit_input_invalid'], error='Invalid')`; `main` returns `output['code']` → exit 2.
- **No drift / fixed identities hold.** Tool sha256 `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` identical before and after the run (matches C2 fixed identity); bundle and snapshot hashes unchanged. No production/fixture mutation; only my own receipt and report were written.
- **Axes not exercised by this case (confirmed irrelevant here, not evidence of absence elsewhere).** Bool/int-signed/nonfinite count handling (`type()`-exact int, bool rejected) is schema-satisfied and never reached; no symlink or 2 MiB boundary present. The output authority string matches the contract authority verbatim; no semantic precision or admission is claimed or creditable from this case.

## Truth/expectation contradictions retained
None observed for this case. Note retained per registration: this `code 2` input-invalid verdict is the presealed truth for the raw lexical rule; it says nothing about the r19 markerless 11-finding/6-line receipt, which remains code2 could-not-evaluate under the strict schema, and any 5/1 or 10/1 row population claims stay derived/new-counterfactual territory outside this case's scope.

## Residual risk and verification gaps
- Single case, single probe by design; no whole-corpus or 46-case selftest rerun (out of lane). Sibling dotdot-adjacent cases (`AuditRawPathEscape`, `AuditRawSymlinkEscape`) were read only as corroborating rationale context and were **not** probed.
- Mutant-killing property (containment-only check → 0/clean) is established by static reasoning on the check path, not by running a mutant; per contract, actual mutant execution belongs to L1's private sandbox.

**Independent semantic verdict: the delivered candidate agrees with the presealed truth for this case (2 / evidence_audit_input_invalid, could-not-evaluate). No actionable defect found in scope.**
