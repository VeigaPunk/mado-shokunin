# FalsifyC216 — C2 AuditRawNaNCounter

Seat `MadoR22.FalsifyC216`. Leaf member, no delegation. Author-lane advisory only: no admission, no semantic-precision credit, no expectation change.
Revision: assignment-stated `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. Not verified; no git subcommands were run.
Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC216/result.json`, with `pre-run-sha256.txt`, `post-run-sha256.txt`, `stdout.txt`, `stderr.txt`, `exit-code.txt`.

## Result

| Source | code | finding_ids | result |
|---|---|---|---|
| Observed (exit 2) | 2 | `["evidence_audit_input_invalid"]` | could-not-evaluate |
| Independent semantic verdict | 2 | `["evidence_audit_input_invalid"]` | could-not-evaluate |
| Expected (`audit/fixtures/expected.json`, `cases[AuditRawNaNCounter]`; `original_expected` identical; `normalizations` empty) | 2 | `["evidence_audit_input_invalid"]` | — |

Observed matches expected and my independent verdict. No contradiction is retained against the expectation, and I propose no expectation change. The output is code 2, never a false 0 or a 1.

## Independent derivation

Derived from raw bytes, declared counts and the strict schema before I read the tool's check path.

1. Bundle (217 B, sha256 `6f245508…`; matches expected `bundle_sha256` and `input_entries` lines 3737–3739). It is a strict JSON object with keys `claim`, `sha256` and `snapshot` only. `claim` is total 0, observed 0, lead 0, errors 0 (exact nonnegative ints) and clean `true` (exact bool). `sha256` is 64 lowercase hex. `snapshot` is `snapshot.json`: relative, with no `\`, empty, `.`, `..` or absolute segment.
2. Path: `root/snapshot.json` is a regular 67 B file. No ancestor is a symlink (`readlink -f` equals each input path). The size is far below 2 MiB.
3. Digest: sha256 of the 67 raw bytes is `183587487f1dacc2623dfdc185cb60c0789458aa05ee3f57d1da361d44fb144c`. This equals the bundle claim and expected `snapshot_sha256` (line 804). So `snapshot_tampered` does not apply. The snapshot digest is settled before the snapshot is decoded; only the bundle is decoded earlier, because it carries the digest.
4. Snapshot bytes: `{"findings":[],"files":[{"eval_unparsed":NaN,"unparsed_spawns":0}]}`. The bare `NaN` is not an RFC 8259 value. Lenient Python json yields float NaN, which is not an exact int. Both readings are invalid under the contract (nonfinite numbers are invalid; counters are exact ints) and the clarifications (JSON numbers must be finite; invalid shapes give 2 `evidence_audit_input_invalid`).
5. Consequence: no counter sum, claim comparison or clean check may run. NaN is not a valid 0, so `errors:0` and `clean:true` can be neither confirmed nor refuted. Code 0 would be a false clean. Code 1 (`error_count_mismatch`, `uncertain_scan_claimed_clean`) would assert a contradiction the input cannot support. Only 2 with `evidence_audit_input_invalid` is compliant.
6. Cross-check: the proposal `raw_snapshot` text (proposal sha `440036ac…`, same as `input_entries` and the `truth_seal_files` entry at lines 4936–4938) hashes to `183587…`, the same as the on-disk snapshot.

## Observed run (one capped scanner child)

`prlimit --as=402653184 timeout 15 python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py --check …/AuditRawNaNCounter/bundle.json --root …/AuditRawNaNCounter/root`

- Caps: 384 MiB address space. `ulimit -v` under the same prlimit reads 393216 KiB. Wall timeout 15 s, not fired. One child. RSS not measured.
- Exit 2. Stderr is empty (`e3b0c442…`). Stdout is 240 B (`9956a6a7…`):
  `{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}`
- Tool sha256 before and after: `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca`. This is the C2 identity and did not change.
- Expected `expected.json` sha256 before and after: `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09`. Bundle and snapshot hashes are unchanged. The case tree gained no files.

## Attack items (relevance to this case only)

- **Row/line grain: not relevant.** `findings` is empty and there is one `files` row. No 5/1-line, 10/1-row or r19 derivation is used or claimed.
- **Digest-before-decode: exercised in the passing direction only.** The tool hashes raw bytes (line 128) before `parse(raw)` (line 131), and the digest matches. This case cannot falsify the ordering. A decode-first implementation returns the same 2 with `evidence_audit_input_invalid`.
- **Signed/bool/nonfinite counts: nonfinite present.** `eval_unparsed: NaN` is rejected with code 2 and never summed. There is no bool or negative counter here (`clean` is a bool, not a count). Layer isolation is weak. By control-flow inference, only `parse_constant` fires. `finite()` and the exact-int check in `count()` would also reject NaN, so this fixture does not separate those layers.
- **Path/symlink/size boundary: accepted correctly.** The relative name is accepted, the files are regular, no ancestor is a symlink, and the size is 67 B. No rejection path is exercised. The symlink rejection and the 2 MiB boundary are untested by this case.
- **Truthful authority: matches.** The stdout authority string is identical to contract line 3, the audit `scope` and the tool `AUTHORITY`. The label is `could-not-evaluate`. The output makes no admission, authentication or semantic-correctness claim. The extra `error` key carries only the class name `Invalid`. That is permitted metadata and does not override normative fields.

## Uncertainties retained

1. The receipt carries the class name only. NaN attribution rests on control flow [INFERENCE from tool lines 121–131]. No exception message was observed.
2. The ordering, layer-isolation and boundary gaps above are fixture-coverage limits. They are not expectation errors.
3. The revision `71228fd5…` is the assignment-stated value and is not verified. The oracle expected `b5cd4cf3…` was neither consumed nor hashed, since it is outside this single-case scope. The governing identity is audit expected `b5df74b5…`, which did not change.
4. Wall time and RSS were not measured. Exit 2 returned with no timeout.

## Suggested discriminators (not run; L1 discretion)

- Same NaN snapshot with a digest mismatch: expected `snapshot_tampered` (2). A decode-first mutant would return `evidence_audit_input_invalid` (2). The finding IDs differ, so this separates ordering. An existing `AuditRawDigestTamper` proposal may serve; I did not examine it.
- Removing `parse_constant` and `finite()` while loosening `count()` to accept float: this would flip the case to code 1 with `error_count_mismatch` and `uncertain_scan_claimed_clean` [INFERENCE, not run].

## Not claimed

No semantic precision, no C1 result, no admission or re-admission, no r19 or counterfactual claim, and no integration. This is advisory author-lane output only.

## Commands and changes

- Reads: case entry in `expected.json` (lines 763–806, plus grep hits), bundle, snapshot, both proposal copies, `audit-contract.json`, `audit-clarifications.md`, `registration.md`, `supported-forms.md`, `guard-clarifications.md`, and the tool source (header, `parse`/`bounded`/`check`/`evaluate`, `main`). `inventory` and `selftest` were not read.
- Non-scanner probes: hashing, `stat`, `find`, `readlink`, `pwd -P`, `od`, `printf | sha256sum`, `jq` for receipt assembly, and `prlimit … sh -c 'ulimit -v'`. Two `python3 -I -c` version/executable probes ran before the scanner call. None of these ran the scanner or fixture code.
- Scanner: one invocation as specified (exit 2). No `--selftest`, no 46-case run, no measurement driver, no mutant runs, no original-tool reruns.
- Receipt: `result.json` was assembled with `jq` from raw captures. Its line 67 was edited once to mark an inference. No observed field changed.
- Installs: none. `prlimit`, `timeout` and `jq` were already present.
