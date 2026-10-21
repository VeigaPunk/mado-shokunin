# FalsifyC228 — C2 `AuditRawSymlinkEscape` independent falsification

Seat: `MadoR22.FalsifyC228` (leaf, author-lane advisory only; not non-author admission).
Lane: read-only production/fixtures/expected. One bounded `--check` child. No selftest, no
measurement driver, no mutants, no installs, no edits to any production/fixture/expected byte.
Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC228/` (`result.json` + raw stdout/stderr/exit/timing).

## 1. Case under test

| Field | Observed value (this case only) |
|---|---|
| case id | `AuditRawSymlinkEscape` |
| bundle | `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawSymlinkEscape/bundle.json` |
| bundle sha256 / size / type | `0b6edd11…dd17e7` / 213 B / regular file |
| declared snapshot name | `link.json` |
| declared snapshot sha256 | `3972b1f5…ae99c` |
| root | `…/cases/AuditRawSymlinkEscape/root` (real dir; no symlink in root or any ancestor) |
| `root/link.json` | **symbolic link** → `../outside.json` (target is outside ROOT) |
| target bytes | `outside.json`, 104 B, sha256 `3972b1f5…ae99c` — matches the declared digest exactly |
| target content | `findings: []`; `files: [{eval_unparsed: 0, unparsed_spawns: 0}]` — a strict-schema-valid clean receipt |
| declared claim | `{clean: true, errors: 0, lead: 0, observed: 0, total: 0}` |
| manifest expectation | `{code: 2, finding_ids: ["evidence_audit_input_invalid"]}`, `normalizations: []` (expected.json:1291-1333) |
| proposal | `.ufo/waves/round-22/w1/audit-proposals/AuditRawSymlinkEscape.json` (sha `fa9ec1fe…` matches manifest) |

All manifest citations agree with the delivered bytes: bundle digest, snapshot digest, snapshot
path, claim, and symlink target all match what is on disk.

## 2. Identities held fixed before and after measurement

- `tools/mado-evidence-audit.py` = `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca`
  before **and** after (required identity; no drift).
- `.ufo/waves/round-22/audit/fixtures/expected.json` = `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09`
  before **and** after (required audit-expected identity; no drift).

## 3. Observation (exact, not paraphrased)

Invocation (assigned absolute form), run from `mado-shokunin/` under `ulimit -v 393216`
(384 MiB address space) and `timeout 15`:

```
python3 -I tools/mado-evidence-audit.py \
  --check .ufo/waves/round-22/audit/fixtures/cases/AuditRawSymlinkEscape/bundle.json \
  --root  .ufo/waves/round-22/audit/fixtures/cases/AuditRawSymlinkEscape/root
```

- exit: **2**
- stderr: **empty** (sha256 `e3b0c442…b855`, 0 bytes)
- stdout (240-byte file, sha256 `9956a6a7…4756`):

```json
{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}
```

- elapsed 263 ms; no `MemoryError`, no timeout; child cap not approached.
- Cross-check: the same check with relative bundle/root paths produced byte-identical stdout
  and stderr, exit 2. Path form is not a variable in the result.

**Observed vs expected: MATCH** — `code 2`, `finding_ids ["evidence_audit_input_invalid"]`,
empty stderr. No expectation was changed, and no normalization was needed.

## 4. Independent derivation from raw bytes + strict schema + relevant check

Derived from fixture bytes, this case's manifest entry, and the delivered tool source; old
classifier/receipt output was not consulted.

| Step | Site | Outcome |
|---|---|---|
| 1 | `bounded(bundle)` (tool:56-64) | bundle is not a symlink, is a regular file, 213 B ≤ 2 MiB → bytes read |
| 2 | `parse` (tool:51-53) | valid UTF-8 JSON, no duplicate keys, no nonfinite token → accepted; claim values are lexical `0` (int) and `true` (bool) |
| 3 | `check` (tool:123-126) | `snapshot` is `str`; declared sha256 is 64 lowercase hex → accepted |
| 4 | `root_path(root)` (tool:88-94) | abspath; `(root, *root.parents)` contains no symlink (independently observed `[]`); `is_dir()` true → accepted |
| 5 | `relative('link.json')` (tool:80-85) | not absolute, no backslash, parts `('link.json',)` contain no `''`/`.`/`..` → accepted (lexical path is clean) |
| 6 | `rooted` (tool:97-102) | assembled `root/link.json` has lstat type **symlink** → `raise Invalid('symlink input')` |
| 7 | `evaluate` (tool:165-170) | `Invalid ⊂ ValueError` → `result(2, ['evidence_audit_input_invalid'], error='Invalid')` |
| 8 | `main` | prints sorted JSON; returns `output['code'] = 2` → exit 2, stderr untouched |

Derived independently: **code 2, ids `["evidence_audit_input_invalid"]`, result label
`could-not-evaluate`**, first rejecting gate = `rooted()`'s per-component symlink guard.

Why not 1 and not 0: no assertion about the bundle's claim was evaluated or contradicted; the
input was refused. `result()` (tool:116-118) maps 2 to `could-not-evaluate`, and the exception
path emits only `evidence_audit_input_invalid`. The exception output correctly omits
`actual_counts`/`actual_snapshot_sha256`, so the receipt fabricates no counts.

## 5. Discrimination — does this fixture actually test the hazard?

Yes, and it is a false-clean trap, derived statically (no mutant executed):

- `outside.json` parses to `findings = []`, `files = [{eval_unparsed: 0, unparsed_spawns: 0}]`.
- `files` is non-empty, so `empty file population` does not fire; `errors = 0`; `total = observed
  = lead = 0`; declared counts all equal actual; `clean = true` with `errors == 0` and `total == 0`
  appends no failure.
- Therefore a mutant that reads *through* the symlink yields `result(0, ['evidence_audit_clean'])`
  and exit 0. Its digest gate would also pass, because the target's sha256 equals the declared
  `3972b1f5…`.
- Conclusion: the fixture kills exactly the "lexical path string is clean, so read it" mutant that
  its rationale describes, and it kills it for the right reason (out-of-ROOT symlink read), not
  because of a digest or row-arithmetic accident.

## 6. Guard attribution limitation (truthful-authority point)

Three independent gates block this input in the delivered bytes:

- **G1** `rooted()` per-component `is_symlink()` (tool:101-102) — **fires**;
- **G2** `rooted()` `not path.resolve().is_relative_to(root)` (tool:103-104) — masked by G1; on its
  own it would also reject, since `../outside.json` resolves outside `root`;
- **G3** `bounded()` `path.is_symlink() or not path.is_file()` (tool:58-59) — masked by G1/G2.

Removal sensitivity (source-level reasoning): removing G1 alone still yields 2 via G2; removing G2
alone still yields 2 via G1; removing G1+G2 still yields 2 via G3. All three sites raise the same
`Invalid` → same code 2 → same finding id. Consequently **this single observation proves "some
Invalid gate refused the escaping symlink", not "the symlink guard specifically is intact."**
Per-guard attribution requires a within-root symlink case (manifest neighbours
`AuditRawSymlinkFile`/`AuditRawSymlinkDir`; their bytes and expectations were not inspected in
this lane). The rationale's phrasing "rejected both as a symlink and as an escape" is accurate as
source structure, but the observed exit cannot attribute which gate fired. No contradiction with
delivered bytes.

## 7. Axis-by-axis relevance to **this** case only

- **Row/line grain — not exercised.** The snapshot has 0 finding rows and 1 file row. The row is
  never reached (read refused). The file row's only schema role here is satisfying non-empty
  `files`; and even `files: []` would raise `Invalid` with the *same* id, so the output cannot
  discriminate that guard either. This case gives no evidence about count arithmetic.
- **Digest-before-decode — statically true, not exercised.** Source order is
  `bounded → sha256(raw) → compare → parse` (tool:127-131), a genuine digest-before-decode shape,
  but this case computes no digest at all because the read is refused. It cannot kill a
  decode-before-digest mutant, and no such credit is taken.
- **Signed/bool/nonfinite counts — not exercised.** `count()` rejects negatives and requires
  `type(x) is int` (so `true`/`false` are rejected as counts); `require(claim,'clean',bool)`
  demands exact bool; `parse_constant`+`finite` reject nonfinite. Those sites run only after the
  snapshot read, which never happens. Claim values here are well-typed lexical `0`/`true`, so no
  predicate is tested. No credit.
- **Path/symlink/size boundary — partially exercised.** Lexical relative-path *acceptance* is
  exercised (step 5); final-component symlink *rejection* is exercised (step 6). Un-exercised:
  resolve-containment (G2), `bounded()`'s symlink/nonregular guard (G3), intermediate-directory
  symlink rejection, the 2 MiB size boundary (213 B/104 B here), and the root-ancestor symlink
  guard (ancestors verified clean).
- **Truthful authority — satisfied.** Output carries the authority disclaimer and the
  `could-not-evaluate` label; code 2 is neither clean nor failed-1; no counts are emitted; no
  semantic-precision, authentication, admission or promotion credit is derivable from this case.
- **Count-inflation applicability — not applicable.** The exception path emits no count rows, so
  no all-observed inflation, no derived 5/1-line or 10/1-row projection, and no r19-receipt claim
  arises here. The markerless actual-r19 code2 receipt is a different artifact and was not touched
  or reinterpreted.

## 8. Independent semantic verdict

- **Observed vs expectation: MATCH** (exit 2, code 2, `["evidence_audit_input_invalid"]`, empty
  stderr).
- **Expectation is semantically correct: yes.** The path string is lexically clean, so lexical
  rejection would be wrong; the resolved target escapes the declared ROOT, so following it would
  breach the audit's evidence boundary; refusing to evaluate is the truthful disposition — code 2
  (could-not-evaluate), not 1 (contradicted) and not 0 (clean).
- **Confidence: high** for the observed match and the derived code/id/gate order; **medium** for
  the removal-sensitivity statement (source reasoning only, mutants deliberately not executed).

## 9. Residual uncertainty (retained, not normalized)

1. **Check-then-use (inference, unexercised).** `bounded()`/`sha_file()`/inventory test
   `is_symlink()`/`lstat` and then `open()` by path without `O_NOFOLLOW`; a concurrent swap
   between check and open could read a symlink target. Frozen fixture bytes cannot exercise this;
   it is not claimed as a defect of this case.
2. **Environment sensitivity (inference).** `bounded(bundle)` first calls `root_path(bundle.parent)`,
   so a checkout or ancestor symlink would produce the *same* `2/evidence_audit_input_invalid` for
   the wrong reason. Verified symlink-free for both absolute paths at run time; future runs under a
   symlinked mount would match the expectation without testing it.
3. **Attribution.** As in §6, the observed exit does not identify the firing guard; only source
   order does.
4. **Scope.** Only this case's fixture bytes and its manifest entry were read; sibling cases,
   the 46-case selftest, the measurement driver, whole-corpus scans and mutants were deliberately
   not run. No claim is made about any other case or the aggregate C2 axis.

## 10. What this receipt does **not** claim

No admission, no non-author falsification credit, no C1 involvement, no aggregate C2 pass, no
semantic-precision credit, no "proposed fault killed" claim, and no change to any expectation.
