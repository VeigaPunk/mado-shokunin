# FalsifyC231 — C2 case AuditTotalMismatch (author-lane advisory, NOT admission)

**Verdict: agree.** The delivered `tools/mado-evidence-audit.py` (sha256 `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca`, identical before and after the run) produced exactly the sealed truth for this one case: exit 1, `result: failed`, `finding_ids: ["finding_count_mismatch"]`, `actual_counts {total 2, observed 1, lead 1, errors 0}`. No counterexample was found within this case. This is one bounded artifact-arithmetic agreement; it grants no admission, no semantic-precision credit, and does not touch the r19/r20/r21 rejected-harmed receipts or the streak.

## Sealed truth (expected.json case `AuditTotalMismatch`, `kind: proposal`)

- `expected {code: 1, finding_ids: ["finding_count_mismatch"]}`; `original_expected.code` was the string `"1"`, normalized to integer `1` with that reason recorded in `normalizations`. The normalization is pre-existing and observation-independent; my derivation below arrives at integer 1 independently.
- Provenance: proposal `.ufo/waves/round-22/w1/audit-proposals/AuditTotalMismatch.json` sha256 `ba6c93e986897086966204d3e12848eaf13c5609e201c01ea8921854507507b7`; bundle sha256 `15422fc47e710c1d5e40bf1d0aa04567158cacfa6b47814849791538fed6a5b1`; snapshot sha256 `ba9279096a0ed653ccde520267202ad07a86d5c14570d371c4dd9cd921217808`.
- Contract: `inputs/audit-contract.json` sha256 `e65d165a1599c2d8743509bfb09ef46df9b8cc9038246b80cdef1780b5fdf23f` (read directly; normative rules quoted below). `audit/fixtures/expected.json` sha256 `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09`; `expected.sha256` content matches it. Oracle expected sha `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` was checked, not used for this case.
- The case is a `proposal`, not `raw` and not `historical-derived`. The markerless-r19-is-2, derived-5/1-lines-or-10/1-rows and all-observed-inflation-counterfactual rules do not apply to it, and I make no claim about those here.

## Independent derivation (raw bytes + declared counts + strict schema; no old classifier output)

I re-read the raw bytes and applied the contract rules directly. The artifact snapshot is a normal receipt, not inert payload to execute.

Input validity first — this case must be evaluated, not code 2:

1. Bundle bytes (218 B) and snapshot bytes (1940 B) both parse under the strict reader: no duplicate JSON keys anywhere, no `NaN`/`Infinity`/`1e400` tokens, UTF-8 clean. Both are far under the 2 MiB bound.
2. `snapshot` is `"snapshot.json"`: relative, nonempty, no backslash, no absolute root, no `.`/`..`/empty component. The resolved target is a regular non-symlink file inside the real (non-symlink) ROOT; the resolved path stays under ROOT.
3. Bundle `sha256` is 64 lowercase hex and equals `sha256(snapshot bytes)` = `ba927909…7808`. Digest verification therefore passes and the snapshot decodes; no `snapshot_tampered`, and the digest-before-decode ordering is satisfied trivially here.
4. Claim: `total 1`, `observed 1`, `lead 1`, `errors 0` are exact nonnegative ints; `clean` is the exact bool `false`. No boolean-as-count, negative or nonfinite value. `files` is a nonempty list of two members, each `eval_unparsed 0` and `unparsed_spawns 0` (exact ints), so actual errors = 0 + 0 + 0 + 0 = 0.
5. `findings` has two rows; each carries an explicit legal marker (`observed`, then `lead`) and nonempty `class`/`command` strings. No missing-marker uncertainty applies, so the case is valid input rather than code 2.

Actual counts, derived from row membership and the tier split:

| quantity | actual | declared | contract comparison |
|---|---|---|---|
| total | 2 | 1 | **1 ≠ 2 → `finding_count_mismatch`** |
| observed | 1 | 1 | equal |
| lead | 1 | 1 | equal |
| errors | 0 | 0 | equal |

- Exactly one contradiction exists, so the verdict is code 1 (`failed`), not clean 0 and not could-not-evaluate 2.
- `clean` is `false`, so neither `uncertain_scan_claimed_clean` (which would also need nonzero errors) nor `findings_claimed_clean` applies.
- Grain check: the two rows are on distinct `(file, line)` pairs — line 9 of `MadoR22.AuditTotalMismatch.jsonl` and line 22 of `MadoR22.AuditTotalMismatchHelper.jsonl`. Row grain, distinct-line grain and distinct-file grain all give 2. No line-vs-row reinterpretation rescues the declared total of 1.
- Independent internal cross-check from the same snapshot: `unpermitted: 2`, `permitted: []`, and `counts {package_query: 1, live_probe: 1}` all agree with two unpermitted finding rows across two classes. That corroborates the count but is not itself a contract rule; the verdict rests on the declared-versus-actual comparison above.
- Second, contract-independent basis: the claim is internally inconsistent on its own arithmetic — `observed 1 + lead 1 = 2 ≠ total 1` — so the contradiction stands even without adopting `len(findings)` as the total's definition.

**Derived independently: code 1, `finding_ids ["finding_count_mismatch"]`.** This matches the sealed expectation exactly.

## Actual run (single authorized measurement)

Command, exactly as assigned, with one child under a 384 MiB address-space cap and a 15 s timeout:

```
bash -c 'ulimit -v 393216; timeout 15 python3 -I \
  /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py \
  --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditTotalMismatch/bundle.json \
  --root  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditTotalMismatch/root'
```

- Process exit: **1** (not 124; the cap was not hit). Empty stderr (0 B).
- Full stdout (366 B, sha256 `8e264770f6424dad983d8db097164df2d34595747fa30d2f6a50b5bf35065cb1`):

```json
{"actual_counts": {"errors": 0, "lead": 1, "observed": 1, "total": 2}, "actual_snapshot_sha256": "ba9279096a0ed653ccde520267202ad07a86d5c14570d371c4dd9cd921217808", "authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 1, "finding_ids": ["finding_count_mismatch"], "result": "failed"}
```

- The output authority string matches the contract's declared authority exactly. It does not claim semantic correctness, authentication, admission or promotion.
- `actual_snapshot_sha256` equals both the bundle-declared digest and the frozen snapshot digest, so the run audited the intended bytes.

Observed equals the frozen expectation on code, result, finding IDs, actual counts and digest; there is no drift in tool, bundle, snapshot or expected-file bytes (before/after hashes all identical).

## What this case does NOT exercise (retained as uncertainty, not green)

- Digest-before-decode ordering under tamper or malformed snapshot bytes: the digest matches and the snapshot is well formed, so ordering is only satisfied, never stressed.
- Signed/bool/nonfinite counts: all counters are exact nonnegative ints; `clean` is a genuine bool. Mutants that merely accept booleans or floats as counts would not be killed by this case.
- Path/symlink/size boundaries: clean relative name, regular file, 218/1940 B — far below 2 MiB. No escape, dot/dotdot, backslash, symlink or oversized-input behavior is measured.
- Missing/invalid evidence markers, empty class/command, empty `files`, claimed-clean-with-findings, claimed-clean-with-errors.
- Line-grain amplification of a markerless historical receipt, derived 5/1 or 10/1 projections, and all-observed inflation counterfactuals. This case is row-grain with explicit markers throughout, and it is a `proposal`; none of the historical r19 restrictions are being tested or relaxed here.
- One case cannot establish that other C2 cases or the 46-case population behave correctly. Agreement is bounded to `AuditTotalMismatch` at these exact bytes.

## Smallest safe correction

None required for this case. The delivered check computed `total = len(findings) = 2`, summed both file error counters to 0, compared each declared count, and emitted exactly the one mismatching stable ID with code 1.

## Authority

Author-lane advisory falsification only. Code 2 elsewhere remains could-not-evaluate and is never read as false clean or failed 1. No semantic precision, admission, retirement, waiver or streak disposition is granted here; L1/Main own closure and admission. No production, fixture, expected, proposal, gate or registry files were modified; no installs were needed; only the one authorized capped child and read-only byte inspection were performed.

## Hashes and receipts

- Tool `tools/mado-evidence-audit.py` before/after: `277eced2…58fca` / `277eced2…58fca` (matches the fixed identity; tripwire `36fdc459…badce` was not used).
- Bundle before/after: `15422fc4…a5b1` / `15422fc4…a5b1`. Snapshot before/after: `ba927909…7808` / `ba927909…7808`.
- `audit/fixtures/expected.json`: `b5df74b5…fd09`; `expected.sha256`: `25955456…ebc60` with content matching; oracle `expected.json`: `b5cd4cf3…4357`.
- Raw receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC231/result.json`, with `exit.txt`, `stdout.txt`, `stderr.txt`, `tool-sha-before.txt`, `tool-sha-after.txt`, `bundle-sha-before.txt`, `bundle-sha-after.txt`, `snapshot-sha-before.txt`, `snapshot-sha-after.txt`.
- No whole-46-case selftest, measurement driver, whole-corpus or full-oracle rerun was executed; no original r19/r20/r21 failure was rerun.

Report: .ufo/waves/round-22/w2/reports/FalsifyC231.md
