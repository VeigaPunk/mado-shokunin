# C2 AuditRawSymlinkFile — independent falsification (author-lane advisory)

**Verdict: observed match; independent semantic verdict agree (high confidence).** Exit 2, stdout `code:2`, `result:"could-not-evaluate"`, `finding_ids` exactly `["evidence_audit_input_invalid"]`, empty stderr. No expectation was changed, normalized, or reinterpreted. This establishes bounded admissibility behavior on one case only: no semantic-precision, authentication, admission, or promotion credit.

## 1. Frozen case identity

- Case record: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/expected.json:1335-1378`. `expected` `{code:2, finding_ids:["evidence_audit_input_invalid"]}` at `:1347-1352`; `original_expected` identical at `:1356-1361`; `normalizations: []` at `:1355`; eligibility `included: proposal declared frozen` at `:3354-3360`.
- `bundle` `cases/AuditRawSymlinkFile/bundle.json` with sha256 `0b6edd115aadfa273bd849baf567fad9151c33cba19e48e1e57fbbf92bdd17e7` (`:1336-1337`), `bundle_snapshot_path` `link.json` (`:1338`), declared claim `{total:0, observed:0, lead:0, errors:0, clean:true}` (`:1339-1345`), `root` `cases/AuditRawSymlinkFile/root` (`:1372`), `snapshot_files` `cases/AuditRawSymlinkFile/root/real.json` with sha256 `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c` (`:1373-1376`).
- Raw inventory entries at `:4009-4033`: bundle is a regular file, 213 bytes; `root/link.json` is a symlink with target `real.json`; `root/real.json` is a regular file, 104 bytes, sha256 `3972b1f5...`.
- Proposal sha256 `914877c2410ee3b2d075d90101413e419763a3684e016fd91b0a413801ffeb34`, size 966 (`:1362-1369`); the W1 proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/audit-proposals/AuditRawSymlinkFile.json` has that same digest and the same claim plus `expected` as the frozen record.
- Normative text: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/inputs/audit-contract.json:7` ("No path escape or symlink is accepted; all snapshot bytes are bounded to 2MiB") and `:8` (`2` = could-not-evaluate for invalid or unavailable input); `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit-clarifications.md:5` (pre-implementation, frozen: "Reject absolute, empty, dot/dotdot, backslash paths and every symlink component"). `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w1/reports/AuditSchema.md:117` classifies the leaf in-ROOT symlink as `2 input_invalid`.
- Identity checks: selected tool `tools/mado-evidence-audit.py` sha256 `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` before and after (matches the fixed identity); `expected.json` sha256 `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` (matches the fixed auditexpected). No drift.

## 2. Independent derivation from raw bytes (not from old classifier output)

1. `bundle.json` is 213 bytes and hashes to the frozen `bundle_sha256`. Parsed strictly it yields `snapshot:"link.json"`, `sha256:"3972b1f5..."` (64 lowercase hex), and the declared claim with exact `int` counters and an exact `bool` `clean:true`.
2. `root` and every ancestor up to `/` were checked: all are directories, none is a symlink (`precheck.txt`). So `root_path()` at `tools/mado-evidence-audit.py:88-94` cannot be the rejection site for this input; attribution to the leaf path is unambiguous.
3. `lstat(root/link.json)` is a symlink; `readlink` = `real.json`; `realpath` = `root/real.json`, a regular 104-byte file whose sha256 `3972b1f5...` equals the declared snapshot digest. `sha256sum link.json` follows the link and reports the same target digest (a followed digest, not an lstat hash).
4. The snapshot name is lexically admissible: relative, nonempty, one component, no backslash, no `.`/`..`. The only admissibility failure is the symlink component itself. `rooted()` at `:97-105` tests `path.is_symlink()` at `:101` before any read or digest.
5. The contract and clarification require rejecting every symlink component, even one that stays inside ROOT and resolves to valid bytes. Invalid input maps to verdict 2. Therefore the correct result is `2` / `could-not-evaluate` with exactly `["evidence_audit_input_invalid"]` — not `1` (no declared count is contradicted) and not `0` (the input is inadmissible).
6. Counterfactual arithmetic if the path were admissible: `findings:[]` gives total 0, the marker loop adds nothing, one `files` row with `eval_unparsed:0` and `unparsed_spawns:0` gives errors 0; all four declared counts equal the actual counts and `clean:true` is consistent, so the failure list is empty and the result would be `0` / `["evidence_audit_clean"]`. This is why the case discriminates exactly the resolve-then-contain mutant class named in the frozen rationale (`expected.json:1371`) and nothing about arithmetic.

## 3. Measurement receipt

Command actually run (single `--check`, absolute paths):

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py \
  --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawSymlinkFile/bundle.json \
  --root /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawSymlinkFile/root
```

Caps: `ulimit -v 393216` (384 MiB address space), `timeout 15s`, one child, no concurrency. Full stdout (240 bytes, sha256 `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`):

```
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

stderr: empty (0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). Process exit: `2`. `error` is the exception class name `Invalid`; no `actual_snapshot_sha256` field appears.

Observed vs derived: process exit = expected code = stdout code = 2; finding IDs equal; result name matches the contract's verdict 2; stderr empty. **Match.**

Raw receipt directory: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC229/` (`result.json`, `stdout.txt`, `stderr.txt`, `exit.txt`, `precheck.txt`, `postcheck.txt`). The `result.json` `stdout` field was byte-compared to `stdout.txt`; length and both stream digests were re-derived.

## 4. Attack surfaces relevant to this case

- **Row/line grain.** `findings` is empty, so there are zero rows and no `observed|lead` marker or class/command decision to make. The declared `total/observed/lead` of 0 equals the actual population. The registered raw-r19 projection counterfactuals (11 markerless findings on 6 lines; a derived 5-observed/1-lead or 10-observed/1-lead population) are not present here and are not credited, inflated, or used to justify this verdict.
- **Digest-before-decode.** Not exercised by this case: path rejection at `:101` precedes the bounded read and hash at `check():127-128`. The absence of `actual_snapshot_sha256` in stdout is consistent with a pre-digest refusal but does not prove the ordering, and no digest-ordering credit is taken.
- **Signed/bool/nonfinite counts.** The claim counters are exact `int` 0 (the `require`/`count` type and sign checks at `tools/mado-evidence-audit.py:67-77` would reject `bool`, `float`, and negative values), and `clean` is an exact `bool`. No negative, boolean-as-count, or nonfinite value is present, so those invalid paths remain unmeasured here.
- **Path/symlink/size boundary.** The path is relative with a single component but its leaf is a symlink; the target stays inside ROOT and its bytes are a valid, digest-matching clean receipt. The 2 MiB bound (`MAX_BYTES`, `:20`) is irrelevant at 213/104 bytes. The ancestor scan rules out an accidental rejection from `root_path()`, so the observed code 2 is attributable to the designed symlink boundary rather than to an unrelated invalid input.
- **Truthful authority.** The emitted `authority` string is exactly the contract authority ("artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion"), and `could-not-evaluate` truthfully reports that no assertion was evaluated. No claim of semantic correctness is made or supported by this measurement.

**Code 2 discipline and the r19 boundary.** The observed `2` is could-not-evaluate; it must never be reported as a false clean `0` or as a failed `1`. This case contributes nothing to the literal registered C2 r19 target: the actual raw r19 receipt remains code 2 with markerless rows (11 markerless findings on 6 incident lines). The later markerful population (10 observed / 1 lead) and any 5-observed/1-lead projection are derived audit inputs that require explicit derivation provenance; they are not actual r19 output. An all-observed or 11-observed reading would be a new counterfactual, not an actual r19 claim, and no such reading is credited here.

## 5. Remaining uncertainties and contradictions (retained)

- The stdout records only `error:"Invalid"`; it does not record the raising site or message. Attribution to `rooted():101` rests on the verified symlink-free ancestry plus the `check()` ordering, not on logged evidence.
- Single-ID refusal is cause-blind: an unconditional-invalid implementation, or one that rejects every non-regular target, produces this identical output. This case's kill power is limited to implementations that accept the symlink and then evaluate the claim (they would emit `0`/`evidence_audit_clean`); constraining the other mutants requires sibling cases (for example the intermediate-directory symlink case and valid controls), which I did not run.
- The explicit in-ROOT rejection depends on the pre-implementation clarification (`audit-clarifications.md:5`); the contract line alone (`audit-contract.json:7`) says "no path escape or symlink is accepted" without the words "every component". Both texts are frozen and consistent, but the expectation is only determinate with the clarification.
- The digest equality belongs to the link target bytes; it is not evidence that this tool verified a digest for this input (it did not reach the digest step).
- Scope is one case, one `--check` invocation. No selftest, no measurement driver, no whole-population comparison, no mutant execution, no rerun of the older tools.

## 6. Non-actions and provenance

No production, fixture, expected, tool, proposal, gate, registry, or documentation bytes were modified; the tool, bundle, snapshot, and expected digests are unchanged before/after. No install or update was performed (none was needed). No package query or transaction, service action, compositor action, network access, build, or live-target probe was performed, and no fixture payload was executed; the only executed code was file stat/read/digest and JSON-parsing shell helpers plus the single bounded audit child. This seat exposes no `lsp` device, so definitions and line numbers were pinned by direct source reads plus `grep -n`/`awk`; the conclusions above are grounded in those read source sections and the measured bytes, not in semantic LSP proof.

Report: `.ufo/waves/round-22/w2/reports/FalsifyC229.md`
