# RecoveryIndependence — C2 independence, historical label provenance, and the unsubstituted classifier copies

Seat `MadoR22.RecoveryIndependence`, connector, author-lane advisory only. Delivered revision `71228fd582d6d9338d7916cc64e69bd4c2e928b5`. This is **not** non-author admission, semantic precision, execution truth, authentication or promotion. The r19/r20/r21 rejected-harmed receipts and the streak are unchanged.

Mode: source-only static inspection of the delivered C2 tool, the independence driver and the materialized truth. No C1, C2, `measure.py`, `independence.py`, `--selftest`, measurement driver, fixture payload, mutant or original old tool was executed. No builds, lints, formatters or installs. The only writes are this report and `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/receipts/RecoveryIndependence/notes.json`.

Path convention: the fixed repository root is `/home/vgpnk/Projects/shokunin/mado-shokunin`; every cited `tools/…`, `.ufo/…`, `corpus/…` path resolves under that root, and the fully expanded absolute identity paths are in the receipt notes. No citation is relative to the report directory.

## Verdict in one paragraph

Two of the three declared independence properties hold at the source and provenance level: the delivered `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py` has no read/import/run path to C1, and every later derived historical label is exactly the label set of a committed round-20 receipt joined 1:1 to the committed markerless round-19 rows. The third property is incomplete in the delivered independence driver: the staged revision contains **three** in-tree classifier sources, but `independence.py` mutates only `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`. The two `tool-before.py` copies remain byte-identical in every state, so a gate whose only classifier-source read is either copy would produce identical outputs across `base/changed/absent/read_fifo/execution_marker`, and the driver would still report `pass_intervention=true`. The delivered C2 tool shows no such read, so this is a proof-scope gap rather than observed coupling. Separately, the selftest/measurement equality boundary does not assert the tool's own `actual_counts` or `result` label, and `measure.py` accepts any `--selftest` exit 0 without parsing its aggregate.

## Identities checked at HEAD (no drift observed across the static reads)

| Artifact | sha256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` (C1) | `36fdc45950cafe0be8c7698e7ed037772d9eed395a42c12097d75c16479badce` (fixed identity) |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py` (C2) | `277eced250774a5d2a2c1985828de522377839a794a2151ddedd232e11458fca` (fixed identity) |
| `.ufo/waves/round-22/oracle/expected.json` | `b5cd4cf3a54ba3af3808436edecf659fe625aba1a8d3cbfbdd0ac355c59c4357` (fixed identity) |
| `.ufo/waves/round-22/audit/fixtures/expected.json` | `b5df74b5b3ce19e944ebafffd72c1b67c43f5ef39bf3bc1a4cc71f4838c2fd09` (fixed identity) |
| `.ufo/waves/round-22/truth-seal.json` and `audit/fixtures/inputs/truth-seal.json` | `47f403f6d4672639629d014d160530b831720aefb5ed588ab841ca92585b24d4` (also at `9185f1f9` and `71228fd`) |
| `.ufo/waves/round-22/w1/historical-c3.json` | `9ee6144d73342062fc1120afd2e4d4db4a52ec014f8a18744f116ab0dbebed7a` |
| `.ufo/waves/round-22/audit/independence.py` | `002b0d676813ef40b832126759fcc8edeb305fccc298534d0188407e9c7fbefc` |
| `.ufo/waves/round-22/audit/assemble.py` | `9b566e0b957fb4d32b0e703f7b888a5a79f14f5ab6ae42c7b6949d3b48c98845` (equals the retry1 receipt runner) |
| `.ufo/waves/round-22/audit/measure.py` | `7646701aa552019285d2546f215d6f7d5e6fbc318622ef84e2673c9277fd0eed` |

## Evidence 1 — C2 source has no read/import/run path to C1

- Imports at `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:9-18` are `argparse, hashlib, json, math, os, pathlib, re, stat, subprocess, sys`. There is no `tools` import, no `importlib`, no `runpy`, no dynamic import.
- `subprocess` has one call site, `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-evidence-audit.py:244`: it re-invokes `sys.executable -I <its own resolved path> --check` for `--selftest`. It never invokes the classifier.
- The string `classifier` occurs only in the docstring (`:6`); `tripwire` does not occur; `mado` occurs only in the fixture schema name (`:220`).
- `--check` (`:121-162`) reads the bundle, the snapshot named by the bundle under `--root`, and nothing else. `--selftest` (`:212-264`) reads `expected.json`, `expected.sha256`, and the fixture inventory listed in the manifest.
- Fixture inventory: 266 entries, 190 under `cases/` and 76 under `inputs/`; **zero** under `tools/`. The only `tripwire`-named files are historical r19 receipt text under `inputs/provenance/` (`tripwire-frozen-r19.txt`, `tripwire-frozen-scan-classes.txt`), which are C1 **output data**, not C1 source.
- Truth seal: 106 file entries, zero `tools/` paths, zero classifier source paths.

Boundary: `--selftest` hashes the old r19 receipts as part of the fixture inventory. That is the declared historical C3 input, not a read/import/run of the changed detector. The registration's "never imports/runs C1, reads its source or derives its expectations from the changed detector" is satisfied at the source level.

## Evidence 2 — Later derived historical labels come only from old committed blobs

The historical case family is not a new detector run. I verified the chain independently of `check()`:

1. **Original markerless receipt.** `.ufo/waves/round-19/evidence/final/tripwire-frozen-scan-classes.txt`, sha256 `64648ccad1f2c872d62026f530ee535624b03268e454ffd1ab8437ab2d0cf857`, committed in `d642ce524ba01c6212b573e5ad51a2b7ddc84c1c`. It contains exactly 11 finding rows, and **no** row has an `evidence` key.
2. **Original counter receipt.** `.ufo/waves/round-19/evidence/final/tw-recall-after.txt`, sha256 `8ff13d23d3ffeab946a301a3457360edc3abf52ea833611ac2a0d6bda48ec1c1`, committed `d642ce5`. It reports `incident_lines 6, detected 6`.
3. **Split authority.** `.ufo/waves/round-20/evidence/recall-split-final.txt`, sha256 `5165b72878feec8c67e20a0ab079db0aaaea358258b8a62fbb965dd91a6df0a2`, committed `4362219e0aaf56601486bdad1df64311e75e12f6`. It reports `finding_totals {observed: 10, lead: 1, unmarked: 0}` and `totals {detected_observed: 5, detected_lead: 1, detected_unmarked: 0, undetected: 0}`. Its producer `.ufo/waves/round-20/tw-recall-split.py` (sha256 `5c8f1424833de506f8f839164ff284614ed5080b6015cf615b61b31e30bc7956`, committed `f3da504`) recorded the scanned tool as `9613f510…` at commit `28c6837`, not the r22 changed detector `36fdc459…`.
4. **Independent join.** I replayed the join from those committed bytes: the split receipt's markers keyed by `(file, line, class, rule)` apply 1:1 to the 11 markerless rows; D1 is exactly 10 observed + 1 lead; the six-line aggregation is exactly 5 observed lines + 1 lead line. Both derived snapshots equal the fixture snapshots byte-for-byte (`HistoricalC3.r19-c3-derived-six-row-5obs-1lead` = D2; `HistoricalC3.D1.row-claim-matches-derived` = D1).
5. **Canonical digests.** Recomputing `sort_keys, separators=(',', ':')` SHA-256 gives D1 `9507e816a5906194ef7bb41661ed3c9a90995e3ed7c404853b3a0172c1fae94b`, D2 `407f7500330b778f142a6f7e8f4f05d8fea3511b3d381a42d98921483cc976af`, markerless projection `9351abaa5b5dcb00dd75f9a2340bbb50e1446cfbcad8e64ecf3144e700c432df` — all equal to the declared values.
6. **Enforcement.** `assemble.py` requires the 11 markerless rows (`:545-560`), the six-line counter (`:562-574`), D1/D2 canonical digests and the 5/1 claim (`:576-599`), the split totals (`:601-620`), the unique 1:1 join and faithful D1/D2 construction (`:621-684`), and the markerless projection digest (`:687-695`).
7. **Sources.** 14 of 14 `historical-c3.json` sources with a named commit match that commit's blob; the `git show 9c54c56…` denominator pin (`4f3534ae…`) matches both the blob and the worktree copy.

The original markerless fixture correctly expects code 2 (`could-not-evaluate`), not failed 1 or clean 0. The derived 5/1 and 10/1 greens are explicitly labeled derived (`claim_kind` "Derived … not an r19 claim") and do not stand in for the literal registered target.

Nuance, not a contradiction: `sources[15]` (`audit-clarifications.md`) is recorded as `UNCOMMITTED (worktree at eda932e)`; its bytes `db5e5c30…` now equal the blob at both `9185f1f9` and `71228fd`. It is contract text, not a label source. Do not edit the sealed proposal to "fix" the historical status.

## Evidence 3 — The independence driver controls one of three in-tree classifier sources

`independence.py` stages the whole revision with `git archive` (`:151-153`) and then defines exactly one classifier path:

- `:34` `CLASSIFIER = 'tools/mado-tripwire.py'` (repo-relative source literal, resolved under the fixed root)
- `:35` `BASELINE = '741122d177ae8ff68a73768777f20484d5bdcbe4'`
- `:155-157` `classifier = regular(stage, relative(CLASSIFIER))`, then reads its bytes and mode.

The staged revision `71228fd` contains three classifier sources:

| Path in stage | sha256 | Bytes | Provenance |
|---|---|---|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py` | `36fdc459…badce` | 162323 | candidate/current C1; the **only** path substituted |
| `.ufo/waves/round-22/evidence/tool-before.py` | `46c82902…4c8c1` | 153493 | equals `git show 741122d:tools/mado-tripwire.py` (repo-relative git path); unsubstituted |
| `.ufo/waves/round-21/evidence/tool-before.py` | `a57d4fe9…b6458` | 130516 | the r20 a2 scanned tool recorded in `historical-c3.json` sources[10]; unsubstituted |

The state loop at `:238` is `base`, `changed`, `absent`, `read_fifo`, `execution_marker`; `:243-248` and `:276-289` unlink/write/mkfifo only `classifier`. Integrity is checked only for `tree_hash(fixtures)` and `digest(gate.read_bytes())` (`:251-256`); the two `tool-before.py` copies are outside `fixtures` and outside the gate, so they are never hashed, restored or recorded. Positive controls (`:271-292`) hash and execute only `classifier`. The limitations (`:301-306`) name stat-only/nonblocking reads and intentional evasion but not unsubstituted in-tree copies.

Consequences:

- A gate whose only classifier-source access is a read or import of `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/evidence/tool-before.py` or `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/evidence/tool-before.py` is **invariant** across all five states, because those files are byte-identical in every state. `equality` (`:261-262`) remains true, `healthy` remains true, and `pass_intervention` (`:299`) remains true.
- The `absent` state label is an overclaim: two classifier sources still exist in the stage when the receipt says `state: absent`.
- The delivered C2 tool does **not** read either copy (Evidence 1), so this is a proof-scope gap, not an observed C2/C1 coupling. The gap matters because the intervention is the evidence offered for the declared negative; a green receipt would not establish that negative for the copies left in place.
- The gap is cheap to close: the three copies have stable, recorded hashes; a size/hash filter over the staged tree finds them without a corpus scan.

## Evidence 4 — CLI, `--selftest`, and the exact-output equality boundary

Paths are explicit and bounded:

- `--check BUNDLE --root ROOT`: the snapshot path is resolved under `--root`, never the bundle parent; absolute, empty, dot, dot-dot, backslash and symlink-component paths are rejected (`:80-114`); inputs are capped at 2 MiB (`:56-65`); the snapshot digest is checked before decoding (`:121-131`).
- `--selftest FIXTURES`: reads `expected.json` and the exact sidecar, validates the fixture inventory and each case's bundle digest, then re-invokes itself per case with the case's explicit root (`:212-259`). The 2 MiB exact-limit case and the symlink cases are present.
- Minor interface ambiguity: `--check` without `--root` returns code 2 (`:275`) rather than a usage error, and `--selftest` silently ignores a supplied `--root`. Neither changes a valid-case verdict.

The equality boundary is narrower than the tool's evidence output:

- `--selftest` marks a case passed iff `proc.returncode == expected code == observed_code`, `sorted(expected ids) == observed ids`, and stderr is empty (`:252-253`). It does **not** compare `result`, `actual_counts`, `actual_snapshot_sha256` or `authority`.
- `measure.py:446-460` compares exit code, exact `finding_ids`, exact authority string, and only requires `result`/`authority` to be non-empty strings. It never reads `actual_counts` (no occurrence in `measure.py`) and never checks `result` against `clean`/`failed`/`could-not-evaluate`.
- `measure.py:494-541` marks `--selftest` passed solely on exit 0; it stores stdout but does not parse `passed`, `total`, `expected_sha256`, `tool_sha256` or the per-case rows. `:718-722` aggregates that boolean with the per-case results.

Consequence: a fault that only swaps or misreports `actual_counts.observed`/`lead` in the output (after the verdict is computed), or emits a wrong `result` label with the right code and IDs, or short-circuits `--selftest` to exit 0, survives the 46-case population, `measure.py` and `independence.py`. No such fault is claimed to exist in the delivered tool; this bounds what the green demonstrates and matters because downstream reports quote `actual_counts` from receipts. The per-case `--check` runs still demonstrate the verdicts themselves.

## Evidence 5 — No identity or authentication claim

- Docstring `:6` disclaims classifier, host probe, Git, network, authenticated chronology, admission and promotion authority.
- `AUTHORITY` at `:22` is exactly "artifact arithmetic and evidence labels only; not semantic correctness, authentication, admission or promotion"; `result()` attaches it (`:116-118`), and `measure.py:456` requires it verbatim.
- `snapshot_tampered` (`:130`) means only "bytes differ from the caller-supplied bundle digest". It is not authorship or authenticity.
- `--selftest` prints `expected_sha256` and `tool_sha256`, which are self-computed digests, not signatures. A self-consistent forged bundle + snapshot + sidecar passes; this is consistent with the disclaimer and is not a defect.

## Bounded coverage enumeration (secondary; not the proposed move)

From the 46 sealed cases (23 raw, 12 proposal, 11 historical-derived; 35 sealed audit proposals represented; 0 excluded):

- Evidence markers across valid snapshots: 92 `observed`, 14 `lead`, 12 absent. **No other marker value exists.** The contract rule "absence or another marker is invalid" is fixture-covered only for absence (`AuditMissingEvidence`). A fault that maps an unknown present marker (for example `"inferred"`) to `observed` survives all 46 cases. Proposed recipe for L1's private sandbox, not run here: change the membership test at `:136-139` to accept a third value; the suite has no input to kill it.
- Nonzero error counters appear only as `AuditErrorsOmitted` `(eval_unparsed 0, unparsed_spawns 2)` and `AuditUnknownClean` `(1, 0)`. **No valid row has both counters positive**, and no duplicate path carries a nonzero counter. A `max(eval_unparsed, unparsed_spawns)` fault therefore produces the same totals on every fixture. A single-counter-only fault dies on one of the two cases; the additive-vs-max distinction is untested.
- `clean:false` with `total 0` and `errors 0` occurs only in `AuditErrorsOmitted` (actual errors 2, expected code 1) and `AuditRawOverflowCounter` (invalid nonfinite, expected code 2). There is no green conservative non-clearance case with zero findings and zero errors, although the clarification permits it.
- No `clean:true` case has both actual findings and actual errors, so the "collect all applicable contradiction IDs" path is never exercised for the two clean IDs together.
- No case has a non-bool `clean`, a non-string `class`/`command`, or a whitespace-only string. Those declared strict-shape rules are source-correct but not fixture-discriminated.
- Four HistoricalC3 case pairs are byte-identical (cross-referenced to `FalsifyC233.md`): 46 cases are at most 42 distinct inputs, so the case total must not be read as independent coverage.
- One undeclared representation normalization is recorded in `expected.json`: `AuditLeadInflated` sorts/dedups `expected.finding_ids`; the clarification names only `expected.code` normalization. It is semantically neutral because the tool emits sorted unique IDs, and `FalsifyC204.md` already records it. Not re-reported as a defect.

These are falsification-coverage limits, not delivered C2 verdict defects and not grounds to change an expectation.

## Affected axes

| Axis | Direction | Why |
|---|---|---|
| C2 calibration / independence evidence | **improve** | The intervention would cover every known in-tree classifier source, not one of three. |
| Truthful provenance / receipt authority | **improve** | Receipt records substituted and unsubstituted copies; `absent` no longer implies no classifier bytes exist. |
| C2 per-case verdicts | **no change** | No fixture, expected value or audit-tool behavior is touched. |
| C1 operability / C1 evidence | **no change** | C1 bytes are untouched; the substitution occurs only in the temp stage. |
| No-harm / verification surface | **improve (bounded)** | Adds per-copy negative controls and integrity hashes; leaves the delivered gate's expected outputs unchanged because it reads none of the copies. |

## Proposed move (one, bounded)

**Exhaustive staged classifier-copy substitution in `.ufo/waves/round-22/audit/independence.py`.**

1. After staging, enumerate regular non-symlink files under `tools/` and `.ufo/waves/**` whose sha256 is one of the known classifier digests (`36fdc459…`, `46c82902…`, `a57d4fe9…`) or whose basename is `tool-before.py`/`mado-tripwire.py` and whose hash matches an explicit pin. Record path, sha256, bytes, mode.
2. Apply each state to **all** discovered copies: `base` writes baseline bytes everywhere, `changed` writes candidate bytes everywhere, `absent` unlinks all, `read_fifo` makes FIFOs of all, `execution_marker` writes the marker to all.
3. Record `classifier_copy_inventory`, `substituted_paths`, `unsubstituted_candidates` and per-copy pre/post hashes. Replace the bare `absent` label with `known_classifier_copies_absent` or add `state_scope`.
4. Extend `positive_controls` per copy: hasher control on base vs changed must differ, FIFO must time out, marker must execute (exit 83 plus marker). `sensitive = all copies sensitive`.
5. Extend `intact` to require every substituted copy to be at the state's expected hash/absence/FIFO after each run, in addition to the existing fixture and gate checks.
6. Add the limitation: only enumerated copies are controlled; absolute-path reads outside the staged tree, stat-only reads, nonblocking opens and unenumerated copies are not detected.

No fixture, expected value, audit tool or C1 byte changes. L1 owns the edit and integration.

## Risks

- Discovery can miss a future copy with a different size/hash; mitigate with explicit `--classifier-copies` pins and record unmatched `tool-before.py`/`mado-tripwire.py`-named files as `unsubstituted_candidates`.
- Substituting `.ufo/waves/round-21/evidence/tool-before.py` changes staged provenance bytes; do it only in the temp stage and record the original hashes. Never touch the checkout.
- If the gate legitimately reads a historical copy, the extended harness will (correctly) report non-identical output; L1 must inspect that as a coupling finding, not dismiss it as a harness bug.
- Multiple marker copies write one marker path; make the write idempotent and clear the marker between states.
- Use `lstat` and reject symlinks/hardlinks when substituting, matching the existing `regular()` discipline.
- Keep the existing one-child, 384 MiB address-space, 15 s limits; the added hashing is a handful of files.

## Verification (L1, after the wave)

1. Static: every discovered copy is mutated in every state; no write path remains outside the loop; receipt fields present and complete.
2. Run `independence.py --revision 71228fd582d6d9338d7916cc64e69bd4c2e928b5 --fixtures .ufo/waves/round-22/audit/fixtures`. Expect `identical_outputs=true`, `selftest_ok=true`, `expected_exits_match=true`, `fixtures_and_gate_unchanged=true`, `positive_control_sensitive=true`, `pass_intervention=true`, with all three copies enumerated.
3. Negative controls in a private sandbox, not run here: a coupled probe that reads `.ufo/waves/round-22/evidence/tool-before.py` and changes its output must yield `identical_outputs=false` under the extended harness while the current harness passes it; repeat for `.ufo/waves/round-21/evidence/tool-before.py`. Do not call any proposed fault killed before L1 runs it.
4. Hash gates: C1 `36fdc459…`, C2 `277eced2…`, audit expected `b5df74b5…`, seal `47f403f6…` before and after; record the new `independence.py` sha256.

## Contradictions and uncertainties retained (not normalized away)

- **No source-level contradiction** was found between the delivered C2 `check()` semantics and the sealed expectations. This seat did not run the tool or the 46-case suite and does not re-credit the per-case greens.
- `sources[15]` `audit-clarifications.md` is recorded `UNCOMMITTED (worktree at eda932e)` but is byte-identical to blobs at `9185f1f9` and `71228fd`. It is contract text, not a label source; the sealed digest remains correct.
- The HistoricalC3 D1 cases inherit a D2 rationale text false for their own bytes; cross-referenced from `FalsifyC234.md`, `FalsifyC235.md`, `FalsifyC236.md`. Expectations are unaffected.
- Four HistoricalC3 case pairs are byte-identical (`FalsifyC233.md`); 46 cases are not 46 independent inputs.
- The registration's "red on a faithful actual r19 C3 six-incident receipt" is correctly materialized as code 2 for the markerless original, per `guard-clarifications.md`; it is never reinterpreted as failed 1 or clean 0.

## Not credited

No admission, non-author admission, semantic precision, execution truth, authentication, promotion, criterion-count credit or streak reset. No mutant is claimed killed; the recipes above are proposals for L1's private sandbox. No C2 verdict or expectation was changed.

Report: .ufo/waves/round-22/w2/reports/RecoveryIndependence.md
