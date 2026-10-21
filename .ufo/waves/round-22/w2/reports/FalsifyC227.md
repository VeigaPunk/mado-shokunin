# FalsifyC227 — C2 `AuditRawSymlinkDir` (author-lane advisory)

Base: `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. Scope: one bounded evidence measurement of the
delivered audit tool on one fixed raw case. No production/fixture/expected/tool/gate mutation, no
selftest, no measurement driver, no installs.

## Observed facts

- Tool `tools/mado-evidence-audit.py` sha256 before **and** after: `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` (fixed identity; no drift).
- Audit fixtures `expected.json` sha256: `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` (fixed identity).
- Case `bundle.json` sha256 `1966aebb64d28c5bb5cd059d0c582aafbef2de44d10c46597b60128c5393af0d` (= `bundle_sha256` in expected.json).
- `root/real/snapshot.json` sha256 `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c` (= digest declared inside `bundle.json`), 104 bytes.
- Case topology: `root/` (directory, no symlink ancestors) contains `dirlink -> real` (lstat `0o120777`) and `real/` with one regular file `snapshot.json`. `bundle.json` declares `snapshot: "dirlink/snapshot.json"`, `claim: {clean:true,total:0,observed:0,lead:0,errors:0}`.
- Command (exact, one child, `ulimit -v 393216` = 384 MiB, `timeout 15s`, `python3 -I` 3.14.8, exit ≠ 124):
  `python3 -I tools/mado-evidence-audit.py --check .../AuditRawSymlinkDir/bundle.json --root .../AuditRawSymlinkDir/root`
  (timeout enforcement sanity-checked separately: `timeout 1s sleep 5` → 124; the assigned run exited 2, not 124, so it finished inside 15 s under the 384 MiB address-space cap.)
- Exit **2**. Stdout (240 B, sha256 `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`):

  ```json
  {"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
  ```

  Stderr empty (0 B, sha256 `e3b0c442…b855`). Raw files: `.ufo/waves/round-22/w2/receipts/FalsifyC227/{stdout.txt,stderr.txt,result.json}`.

## Independent derivation (not from old classifier output)

Using only the raw bundle/snapshot bytes, the observed filesystem topology, the strict schema in
`audit-clarifications.md`, and the candidate relevant check `rooted()` in the auditor:

1. `bundle.json` parses as an object with unique `snapshot`/`sha256`/`claim`; `sha256` is 64 lowercase hex; `claim.clean` is bool, counters are exact nonnegative ints — so the bundle's own claim is admissible.
2. `root_path(root)`: abspath root and every parent are non-symlinks (observed ancestor symlink set is empty) and root is a directory — root guard does not fire, and cannot be the attribution.
3. `relative("dirlink/snapshot.json")` passes (nonempty, no backslash, not absolute, parts contain no `""`/`.`/`..`).
4. `rooted()` walks components left to right. The first component `root/dirlink` is a symlink (`readlink → real`), so it raises `Invalid('symlink input')` **before** any snapshot byte read, 2 MiB bound, or digest comparison.
5. `evaluate()` maps `Invalid` (ValueError) to `result(2, ['evidence_audit_input_invalid'], error='Invalid')`; `main()` prints sorted-key JSON and exits with that code.

Derived: **code 2 / `evidence_audit_input_invalid` / could-not-evaluate**, from the "reject every
symlink component" clarification bullet. This matches the fixed expectation exactly, so
`observed_match: true` and independent semantic verdict **match**.

Why not 1: input validation aborts before any count/clean assertion is evaluated, so no
contradiction set exists. Why not 0: the claim is consistent with the zero-row snapshot, so a
leaf-only (`O_NOFOLLOW`/`is_symlink` on the final component) or resolve-then-read implementation
could return `0/evidence_audit_clean`; the clarification forbids that, so 0 would be a
wrong-semantics green here. The case earns credit only for intermediate-component symlink rejection.

## Boundaries this case does NOT exercise

- Digest-before-decode: unreachable — path rejection precedes opening; the declared snapshot digest
  already equals the actual bytes, so `snapshot_tampered` cannot be probed.
- Row/line-grain arithmetic, observed/lead splitting, duplicate/signed/bool/nonfinite count
  handling, `clean` semantics, and per-file summing: the snapshot is never parsed.
- Path size bound (bundle 225 B, snapshot 104 B vs 2 MiB), absolute/dot/backslash path forms,
  symlink-root, leaf-symlink, escaping-path forms: not present.
- Truthful authority: output repeats the artifact-arithmetic-only authority string; no semantic,
  authentication or admission claim is made or earned.
- No mutants were run. The proposal's leaf-only-check mutant remains a proposal, not a killed mutant;
  nothing here proves it dead.

## Retained uncertainty / contradiction

- The tool's input-invalid result omits `actual_counts`/`actual_snapshot_sha256`, so which guard fired
  is not visible from output; attribution to `dirlink` rests on source reading plus topology (leaf is
  regular with a matching digest, root has no symlink ancestors), and is the only reachable rejection.
- The expected fixture's `claim` block (`clean:true`, all zeros) is not a clean-scan assertion; it is
  never evaluated. Treating it as a clean verdict would be an all-observed inflation claim and is
  explicitly not made.
- r19 markerless raw remains code 2; no derived 5/1 or 10/1 row projection is used or implied here.
- This receipt is author-lane advice only: it is not non-author admission, not semantic-precision
  evidence, and it does not soften or retire the existing r19/r20/r21 red receipts or the streak.

## Changes

None outside this report and `.ufo/waves/round-22/w2/receipts/FalsifyC227/`.
