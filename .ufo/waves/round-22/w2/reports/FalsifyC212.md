# C2 falsification: AuditRawDupBundleClaim (FalsifyC212)

Seat: MadoR22.FalsifyC212. Lane: leaf member, artifact-only C2 attack on one fixed case. Advisory author-lane output: not non-author admission, no semantic-precision credit, no admission.

## Verdict

- **Observed match: YES.** Exit 2. `code` 2, `finding_ids` `["evidence_audit_input_invalid"]`, `result` `could-not-evaluate`. Matches the fixed expected entry (expected.json lines 599-604). `normalizations` is `[]` and `original_expected` equals `expected`, so no expectation was changed.
- **Independent semantic verdict: AGREES.** The bundle's `claim` object repeats the key `clean` (false, then true). The pinned contract declares duplicate JSON keys invalid input, and verdict 2 is could-not-evaluate. Declared and actual counts are both 0/0/0/0 for either `clean` value, so input validity is the only verdict-determining fact. Code 0 would be a false clean and code 1 is unsupported.
- **No falsification found for this case.** Residual uncertainty is listed below.

## Identities (unchanged before and after the single run)

| artifact | sha256 | size |
|---|---|---|
| tools/mado-evidence-audit.py (C2 pin) | 277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca | |
| fixtures/expected.json (audit expected pin) | b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09 | |
| cases/AuditRawDupBundleClaim/bundle.json (= expected bundle_sha256) | f131852a9bb7ab13574602031d645a6a612a3982ad96baf83a8ed785a7b2cbbf | 184 B |
| cases/AuditRawDupBundleClaim/root/snapshot.json (= bundle `sha256` field) | 3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c | 104 B |
| fixtures/inputs/audit-contract.json (second copy at round-22 top level, same digest) | e65d165a1599c2d8743509bfb09ef46df9b8cc9038246b80cdef1780b5fdf23f | 2129 B |
| w1 and inputs proposal copies of AuditRawDupBundleClaim.json | c763ffa577530070c45079144aa09bb295d62bd70322b169c8a26bb097dfd798 | 1111 B |

## Run

One child, capped by `prlimit --as=402653184` (384 MiB) and `timeout 15`:

```
python3 -I tools/mado-evidence-audit.py --check .../AuditRawDupBundleClaim/bundle.json --root .../AuditRawDupBundleClaim/root
```

- Exit: 2 (tool verdict, not a timeout or signal).
- stderr: empty (sha256 e3b0c442…b855).
- stdout (sha256 9956a6a7…4756):

```
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

- Receipts: `.ufo/waves/round-22/w2/receipts/FalsifyC212/` holds `result.json` (full stdout, stderr, digests, derivation), `stdout.txt`, `stderr.txt`, `exit_code.txt`, `pre_run_sha256.txt`, `post_run_sha256.txt`.

## Independent derivation (not taken from tool output)

1. **Raw bytes.** 184-byte single-line JSON. The `claim` object is `{total:0, observed:0, lead:0, errors:0, clean:false, clean:true}`. My hand count of the literal text is 184 only with both `clean` members present, matching the measured size.
2. **Strict-schema authority.** Contract rules: "Duplicate JSON keys, malformed JSON, booleans-as-counts, negative counts and nonfinite numbers are invalid." Verdict 2 is could-not-evaluate (invalid or unavailable input). The stable ID for invalid input is `evidence_audit_input_invalid`.
3. **Counts.** Declared 0/0/0/0. Actual from snapshot bytes: `findings` is empty and `files` has one row with `eval_unparsed` 0 and `unparsed_spawns` 0, giving 0/0/0/0. Count arithmetic cannot yield 1, and either `clean` value is consistent with the counts.
4. **Derived verdict:** code 2, could-not-evaluate, `["evidence_audit_input_invalid"]`. This agrees with the fixed expectation.
5. **Counterfactual (new, static only, not executed, not an r19 claim).** A duplicate-ignoring parser would reach count comparison and return code 0 `evidence_audit_clean`. That is the false-clean hazard this case exists to block.

## Causal check of the observed code 2

The only reachable `Invalid` is the duplicate-key raise from `pairs()` on the claim object. `evaluate()` catches it (`Invalid` subclasses `ValueError`) and returns `result(2, ['evidence_audit_input_invalid'], error='Invalid')`. The other `Invalid` sources were ruled out with measured inputs:

- symlink or missing root: no symlinks in the ancestor chain (`namei -l`);
- nonregular input: both files are regular;
- size: 184 B and 104 B, far below 2 MiB;
- JSON syntax: valid apart from the duplicate, and no JSONDecodeError class appears;
- snapshot digest: never reached, consistent with no `actual_snapshot_sha256` key in the output.

## Attack dimensions (relevant to this case only)

| dimension | relevant here | result |
|---|---|---|
| row/line grain | marginal (single line, no finding rows) | not triggered; output carries no locus |
| digest-before-decode | ordering only; snapshot digest is correct and never reached | non-discriminating for this case |
| signed/bool/nonfinite counts | not reached (counts are 0 ints; no negative, bool or NaN/Infinity token) | no evidence on count typing |
| path/symlink/size | checked | boundaries pass; not the cause |
| truthful authority | yes | output authority equals contract string exactly; `could-not-evaluate`; no clean or failed wording |

## Uncertainty and contradictions retained (no expectation change)

1. The output names only the exception class `Invalid`, not the reason. Attribution to the duplicate key is static reasoning over tool source plus measured inputs; no further probe was assigned.
2. `expected.json` claim block (lines 591-597) renders `clean: true` alone, while the bytes carry `clean:false` then `clean:true`. The rationale marks it as documentation and the tool does not read it. This is a lossy rendering; reported, not normalized.
3. The rationale cites "the clarifications" for the duplicate rule and "raw_bundle" for the bundle bytes. No `raw_bundle` key exists in the case entry (lines 587-630); binding is via `bundle` and `bundle_sha256`, which match. The rule was verified in the pinned contract text; the clarifications file was not located.
4. The observed output has an extra `error` key the expected entry does not constrain. Compared on `code` and `finding_ids` only.
5. An incidental grep over `audit/fixtures/inputs` surfaced excerpts of sibling proposal rationales. They were not used as derivation or expectation.
6. A third glob hit under `provenance/.ufo/waves/round-22` does not resolve as a path. The two existing contract copies both match the pin.

## Not credited

Semantic precision, admission, r19 receipt claims, derived 5/1 or 10/1 projections, and all-observed inflation counterfactuals. Authority remains artifact arithmetic and evidence labels only.

## Installs and scope

No installs or updates. No selftest, measurement driver, builds, lints, or sibling/production writes. One scanner child was run and nothing else was executed through the tool.
