# FalsifyC232 — C2 AuditUnknownClean (round-22 wave2)

Lane: author-lane advisory falsification. Not non-author admission, not semantic-precision credit.
Scope of evidence: one fixed case (`AuditUnknownClean`), one bounded CLI measurement, static reading of
raw fixture bytes, the sealed contract, and the delivered audit tool's relevant check path.

## Identity (checked before and after)

| Object | SHA-256 |
|---|---|
| `tools/mado-evidence-audit.py` (before = after) | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| `audit/fixtures/expected.json` (fixed audit-expected identity) | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` |
| `audit/fixtures/inputs/audit-contract.json` | `e65d165a1599c2d8743509bfb09ef46df9b8cc9038246b80cdef1780b5fdf23f` |
| `cases/AuditUnknownClean/bundle.json` (217 B, regular) | `47926ed532044bb0c9fced71bf3ea1498ae69b73d6279f026b8a35418075494a` (matches expected.json `bundle_sha256`) |
| `cases/AuditUnknownClean/root/snapshot.json` (136 B, regular) | `c4d6f172b69f18b86382a137469f83425a54cdeb54012eac20f2f24d67f56a57` (matches bundle `sha256`) |
| `inputs/proposals/AuditUnknownClean.json` (2049 B) | `a9f38aa3784a515a6a6d6b1337c883620bad3952502759d6bfd4d31bf328a93e` (hash/size provenance only; content not read) |

`expected.sha256` seals `expected.json` with `b5df74…`; exactly one `AuditUnknownClean` entry exists in
`expected.json`. Tool identity did not drift across the run. Python 3.14.8 (`/usr/bin/python3.14`),
invoked with `-I`.

## Independent derivation (before running the tool)

From raw bytes only (`od -c` + direct reads), not from classifier output and not from the proposal rationale:

- Bundle claim: `clean:true`, `errors:1`, `lead:0`, `observed:0`, `total:0`; snapshot ref `snapshot.json`.
- Snapshot: `files:[{eval_unparsed:1, path:"pkg/handler.py", unparsed_spawns:0}]`, `findings:[]`.
- No duplicate JSON keys, no NaN/Infinity tokens, no floats; `clean` is an exact bool, all counters are
  exact nonnegative ints (bool would be rejected by `type(x) is int` in `count()`).

Strict-schema path (contract rules + `check()` lines ~124–162):

1. Snapshot ref is one safe relative component; root and every parent symlink-free (`namei -l`); snapshot
   is regular and 136 B < 2 MiB.
2. Digest-before-decode: `sha256(snapshot) = c4d6f172…` equals the bundle-declared digest → no
   `snapshot_tampered`.
3. Snapshot schema valid: one-member nonempty `files`, empty `findings` is explicitly allowed.
4. Actual arithmetic: `total=0`, `observed=0`, `lead=0`, `errors=1+0=1`.
5. Declared counts equal actual counts for all four keys → all four `*_count_mismatch` rules stay silent.
6. `clean:true` with nonzero `errors` violates "clean:true only if findings empty and errors zero" →
   `uncertain_scan_claimed_clean`.
7. `clean:true` with `total=0` → `findings_claimed_clean` does not fire.
8. Failures nonempty ⇒ **code 1**, IDs exactly `["uncertain_scan_claimed_clean"]`.

Why not 0: the artifact's own clean assertion contradicts its disclosed nonzero error total.
Why not 2: the input is well-formed, digest-consistent, schema-valid, symlink-free and size-bounded; the
disclosed error is artifact data, not an invalid/unavailable input.

## Authorized measurement (one child, capped)

```
( ulimit -v 393216; timeout 15s python3 -I .../tools/mado-evidence-audit.py \
    --check .../cases/AuditUnknownClean/bundle.json \
    --root  .../cases/AuditUnknownClean/root )
```

384 MiB address space / 15 s / one child; timeout did not expire. Observed:

- **exit = 1**
- stdout (372 B, sha256 `fa55b229e2020f201ec7f741304f8e17066b23e13dc57a1fddfa899d9f1339b3`):
  `{"actual_counts": {"errors": 1, "lead": 0, "observed": 0, "total": 0}, "actual_snapshot_sha256": "c4d6f172…6a57", "authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 1, "finding_ids": ["uncertain_scan_claimed_clean"], "result": "failed"}`
- stderr: empty (0 B, sha256 `e3b0c442…b855`).

## Observed vs derived vs fixed expected

| Facet | Derived | Fixed expected | Observed |
|---|---|---|---|
| code | 1 | 1 (normalized from `"1"`, recorded) | 1 |
| finding_ids | `["uncertain_scan_claimed_clean"]` | same | same |
| actual counts | 0/0/0, errors 1 | claim 0/0/0, errors 1 | 0/0/0, errors 1 |
| stderr | — | — | empty |

Match is exact; no expectation was changed. The `"1" → 1` normalization is the recorded fixture
normalization (verdict string to integer), not a verdict reinterpretation.

## Attack surfaces relevant to this case

- **Row/line grain:** `total = len(findings)` = 0; observed/lead are per-finding-row counts; errors are
  summed per file row over exactly `eval_unparsed + unparsed_spawns` = 1+0. Declared 0/0/0 and 1 match
  the row arithmetic exactly. No line-grain projection, no row double-count, no inflation. Consistent.
- **Digest-before-decode:** raw snapshot bytes are hashed and compared before `parse(snapshot)`; the
  declared digest matches, so decode used authenticated bytes. The bundle is decoded first to obtain the
  expected digest and claim; its authorship is bound externally here by `expected.json` (`bundle_sha256`
  matches), not by the tool. Consistent within the declared scope.
- **Signed / bool / nonfinite counts:** `count()` demands exact int (rejecting bools) and nonnegative
  values; `parse()` rejects NaN/Infinity tokens and nonfinite floats. This fixture's 1/0 are exact
  nonnegative ints and `clean` is an exact bool, so nothing routes to invalid input; code stays 1, not 2.
- **Path / symlink / size boundary:** single safe relative snapshot ref, symlink-free root chain, regular
  files of 136 B and 217 B (both < 2 MiB). Boundaries exercised and passed.
- **Truthful authority:** the emitted authority string matches the contract's bounded authority; code 1
  asserts only the internal clean-vs-errors contradiction, not execution truth.

## Retained uncertainty / scope (not normalized away)

1. `check()` never resolves `files[].path` (`pkg/handler.py` is benign and unused except as row data); the
   contract's no-path-escape rule is enforced on the bundle/snapshot references, not on descriptive paths
   inside the snapshot. This cannot change the code-1 verdict here, but the distinction is recorded.
2. The snapshot digest proves snapshot bytes match the bundle's own declaration; it does not authenticate
   the bundle author. The harness's external binding does (bundle and proposal digests match on disk).
3. Code 1 is artifact-assertion contradiction only — no credit to C1 semantic precision, detector
   agreement, admission or promotion.
4. No historical r19 markerless receipt is replayed: this snapshot has zero finding rows, so the
   markerless code-2 basis does not arise and remains untouched.
5. No 5-observed/1-lead or 10-row derived projection and no all-observed inflation counterfactual is
   used or claimed; the only counts are actual 0 finding rows, 1 file row, 1 error unit.

## Receipt

`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/FalsifyC232/`
- `result.json` (sha256 `b9e303fe48ca25fac49558cca8a695ca4ea1a11c5316e9b730da035aff5e98d7`)
- `stdout.txt` (sha256 `fa55b229e2020f201ec7f741304f8e17066b23e13dc57a1fddfa899d9f1339b3`)
- `stderr.txt` (empty, sha256 `e3b0c442…b855`)

Harness note: a first invocation attempt failed before any Python process started (`exec: command not
found`, exit 127). It is a harness construction error, not evidence, and was followed by the single
authorized measurement above.

Confidence: high on observed/derived/expected agreement and on the case-local rule application; no
contradiction found. Remaining unknowns are the two scope boundaries stated above, neither of which
alters the verdict.
