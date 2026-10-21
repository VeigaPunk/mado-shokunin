# FalsifyC225 — C2 AuditRawPathEscape (round 22, author-lane advisory)

Seat: `FalsifyC225` (leaf, advisory only — this is NOT non-author admission).
Target fixture: `.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathEscape`
Expected entry: `.ufo/waves/round-22/audit/fixtures/expected.json:1163-1205`; that file's sha256 is `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09`, matching the fixed audit-expected identity.
Receipt: `.ufo/waves/round-22/w2/receipts/FalsifyC225/result.json` (raw stdout/stderr/exit alongside).

## Tool identity

| item | value |
|---|---|
| tool | `tools/mado-evidence-audit.py` |
| fixed identity | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| sha256 before | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| sha256 after | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` |
| drift | none |

Selected-tool hash checked before and after the single measurement; no moving target.

## Fixture facts (raw bytes, read directly)

| item | value |
|---|---|
| `bundle.json` | 219 B, sha256 `6be0ed408c2e8b61be065538a3f4f35a64512a7cf2755eb607d2a3d4e58da97c` (matches `bundle_sha256` in expected.json) |
| bundle `snapshot` | `"../outside.json"` |
| bundle `sha256` | `3972b1f5d92cb5a2ff347d11cbe2861765e10e0954764a87931195e17eeae99c` (64 lowercase hex) |
| bundle `claim` | `{clean: true, total: 0, observed: 0, lead: 0, errors: 0}` |
| ROOT | `.../AuditRawPathEscape/root`, **empty** (0 entries), not a symlink, no symlinked ancestor (`readlink -f` == logical abspath) |
| escape target | `.../AuditRawPathEscape/outside.json`, regular 104 B file, sha256 `3972b1f5…`, exactly one level above ROOT |
| escape target shape | `findings: []`; `files: [{eval_unparsed: 0, unparsed_spawns: 0}]` — i.e. digest-valid **and** claim-consistent |
| expected | `{"code": 2, "finding_ids": ["evidence_audit_input_invalid"]}` (identical `original_expected`) |

## Independent derivation (not from old classifier output)

Basis: raw bundle bytes, raw `outside.json` bytes, declared counts, strict schema in `.ufo/waves/round-22/audit-contract.json` rules 1–8, the path rule in `.ufo/waves/round-22/audit-clarifications.md:5` ("snapshot path resolves relative to explicit ROOT, never bundle parent. Reject absolute, empty, dot/dotdot, backslash paths and every symlink component"), and the candidate relevant check in the tool.

Chain:

1. `check()` (`tools/mado-evidence-audit.py:121`) → `bounded(bundle)` reads 219 B ≤ 2 MiB; `parse()` succeeds (no duplicate keys, no nonfinite numbers); `snapshot` is a `str`; `sha256` is a valid 64-lowercase-hex digest.
2. Next statement `raw = bounded(rooted(root_path(root), name))` (line 127). `root_path` (line 88) passes: abspath, no symlink in root/ancestors, root is a directory.
3. `rooted` (line 97) first calls `relative(name)` (line 80). `"../outside.json".split('/')` = `['..', 'outside.json']`; the `'..'` member hits the dotdot predicate at line 84 → `Invalid('invalid relative path')` **before any join, stat, open or digest**.
4. `evaluate` (line 165) catches `Invalid` (a `ValueError` subclass) at line 169 → `result(2, ['evidence_audit_input_invalid'], error='Invalid')`.
5. `main` prints `json.dumps(..., sort_keys=True)` and returns `code` → process exit 2, stderr untouched.

Derived: **exit 2**, `code 2`, `result could-not-evaluate`, `finding_ids ["evidence_audit_input_invalid"]`, `error Invalid`, stderr empty.
The derivation consumes **no** row counting and **no** claim comparison: the snapshot is refused before it is opened, so the declared all-zero claim is inert on this path.

## Execution (one authorized measurement)

```
prlimit --as=402653184 --cpu=15 -- timeout 15 \
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py \
  --check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathEscape/bundle.json \
  --root  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/audit/fixtures/cases/AuditRawPathEscape/root
```

Caps: 384 MiB address space (402653184 B), 15 s CPU and wall, one child.

- exit `2`, not timed out, no signal
- stdout (240 B, sha256 `9956a6a70be430b8f2c1692fc4425dd06c0c33c92be6937ab6303ca099eb4756`):
  `{"authority": "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion", "code": 2, "error": "Invalid", "finding_ids": ["evidence_audit_input_invalid"], "result": "could-not-evaluate"}`
- stderr: 0 bytes (`e3b0c442…`, empty-hash)

**Observed match:** code 2 ✔, finding id ✔, exit ✔, empty stderr ✔ — the delivered bytes match the independently derived expectation exactly. No expectation was edited.

## Independent semantic verdict

Accept `2 / evidence_audit_input_invalid` as the truthful label for these bytes.

- **Not 0.** `0/evidence_audit_clean` would assert the escaped snapshot satisfied the declared claim. Reaching it requires the artifact-input gate to fail first; the rules forbid path escape.
- **Not 1.** `1` asserts a contradicted artifact assertion. Nothing was evaluated here — no digest comparison, no row count, no claim comparison. Calling a refusal "failed" would claim a contradiction that never occurred.
- **Counterfactual discriminator.** An unchecked join (`root / '..' / 'outside.json'`) reaches `outside.json`: its 104 bytes match the declared `3972b1f5…` digest, `findings` is empty, and its sole files row is `0/0`. Declared claim is all-zero with `clean: true`, so a bypass yields `failures = []` → `0/evidence_audit_clean`, exit 0. The fixture therefore separates the escaped-join class from compliant behaviour exactly — and tamper detection cannot rescue the escape, because the escaped bytes are digest-valid by construction.

**Credit ceiling (do not inflate):** this green evidences only that the delivered bytes refuse this dotdot snapshot name at the CLI boundary with the contract authority string intact. It is not arithmetic correctness, not row-grain precision, not digest-ordering evidence, not symlink or size-boundary evidence, and not semantic precision or admission.

## Attack surfaces relevant to THIS case

| surface | exercised? | finding |
|---|---|---|
| row/line grain | no | The snapshot is never parsed; `findings`/`files` loops and the claim comparison (`check()` lines 137-160) are unreachable here. This case supplies zero evidence about row-grain counting. |
| digest-before-decode | no | No bytes are read, so no digest is computed. Contract rule "snapshot digest is checked before verdict comparison" is untested by this case. Its only relevant contribution is negative: digest validity of the escaped file means the discriminator is path admissibility alone. |
| signed / bool / nonfinite counts | no | `claim` is required only after the snapshot read, so `require(claim,'clean',bool)` and `count()` are never reached. A tool that accepted `true` as `1` or negative counts would still pass this case. |
| path boundary | yes | Lexical dotdot component rejection, pre-filesystem. |
| symlink boundary | no | ROOT and ancestors are real directories; `outside.json` is a regular file. The symlink-component guard is not exercised. |
| 2 MiB size boundary | no | 219 B and 104 B inputs, far from the cap; `bounded()`'s oversize branch is untested. |
| truthful authority | yes | Output carries the contract authority verbatim and labels the outcome `could-not-evaluate`; it claims no arithmetic verification. |

## Falsification findings (retained, not normalized)

1. **The green does not localize the guard.** `relative()`'s dotdot rejection and `rooted()`'s final `path.resolve().is_relative_to(root)` containment check (line 103) both reject this name and both raise the same `Invalid` class, so `error: "Invalid"` cannot tell an observer which fired. Localization comes from ordered source, not from the process output. The same label also covers absolute/backslash/empty paths, symlink inputs, missing root and symlinked root ancestors.
2. **Proposed mutant recipe is a multi-guard defeat, not a one-line kill.** Deleting only the `'..'` member from `relative()`'s tuple leaves the containment check (still 2). Deleting only the containment predicate leaves the lexical check (still 2). The rationale's "joins paths without checks" flips only by defeating both at once — e.g. replacing the call at line 127 with a plain join `bounded(root / name)`, after which `bounded()`'s `root_path(parent)` sees the FIX directory and passes. A private mutation run must not expect a kill from a single-site edit inside either guard alone, and must not read such a survivor as expectation failure. **No mutant was built or run by this seat**; this is a recipe and prediction only, and no mutant is claimed killed.
3. **`--check` does not bind the bundle digest.** `bundle_sha256` is verified only inside `selftest`. The single authorized `--check` run therefore does not by itself prove the bundle is the manifest-bound bytes; that bind here rests on the external sha256 comparison against the expected.json entry (`6be0ed40…`, matches).
4. **Environment alternative ruled out, but as an observation.** `root_path()` refuses any symlinked ancestor, so an environment symlink above ROOT could produce the identical 2 for the wrong reason. `readlink -f(root)` equals the logical abspath, which excludes that here; this is an environment check, not tool evidence.

## Not run / scope held

- 46-case selftest: **not run**. Measurement driver: **not run**. No other case measured. No extra source-shaped probes (0).
- No production/fixture/expected/tool edits; no clones of fixtures; no delegation, background jobs, installs, or live probes. One child, one command, both caps applied.
- No expectations changed; no dead replacements. C1 verdicts, prior r19/r20/r21 red receipts and the streak were left untouched.
