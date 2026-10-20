# FrozenInputs — snapshot tamper controls for `mado-action-plan.py --frozen`

Seat: `MadoR16.FrozenInputs` (reviewer, leaf). Baseline `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`.

Basis, stated once: source reading only. `tools/mado-action-plan.py` does not exist at review time (glob of `tools/` returns only `mado-verify.sh`), so every control below is a **design requirement** for SafetyGate and a **case row** for SafetyCases. Nothing here is observed behaviour. No command was executed, no test or gate run, no install, no package/service/pacman operation, no host or input probe, no sibling file edited.

## 1. Verdict on the design as written

The contract (`spec.json:10`, SafetyGate prompt): "`--frozen DIR` verifies expected.json input digests for plan.json and policy.json then compares verdict/code; tampering returns 2 snapshot_tampered." The assignment: tamper must return could-not-evaluate (2), **not** a changed verdict (1).

The sentence is correct in direction but under-specified in three places that matter for this assignment:

1. **expected.json is not pinned.** If only `expected_code` / `expected_finding` is edited, every input digest still matches, the classifier runs, and the comparison fails with the changed-verdict code 1. That is exactly the outcome the assignment forbids for tampering.
2. **Ordering is not stated.** The control must be: digests verified → only then the classifier runs → only then verdict compare. A tampered plan whose computed verdict happens to equal the expectation must still return 2 (no verdict-based rescue).
3. **Byte discipline is not stated.** Hash the bytes that are parsed, once. A path re-read after hashing is a TOCTOU window.

Requirements R-1 to R-10 (§5) and controls T01–T22 / G01–G05 (§6) close these. Exit map: §4.

## 2. Axes named

- **A1 tamper coverage** — every input mutation class returns 2 `snapshot_tampered`.
- **A2 ordering** — no classifier output and no verdict before the digest gate; no verdict-rescue.
- **A3 expectation integrity** — expected.json bytes bound by something outside the directory.
- **A4 fail-closed I/O** — symlink, FIFO, extra entry, duplicate key, subdirectory all refuse; no hang.
- **A5 honest limits** — residuals named, not smoothed (§8).

Iteration: the first draft bound only the input digests (round-14 shape). The T13/T14 case (expectation-only and consistent-rewrite tamper) showed A3 unmet, so a pin was added. Adding `--frozen-pin` improved A3 and left A1, A2, A4 unchanged; cost is one operator-supplied hex string. Kept.

## 3. Precedent read and defects not to copy

Precedent: `.ufo/waves/round-14/frozen/verify.py` (+ `expected.json`), registered at `SKILL.md:515` (`mado-frozen-regression-r14`) with the same exit shape the new gate needs: 0 `frozen_match`, 1 `frozen_verdict_mismatch`, 2 `snapshot_tampered` / `frozen_error`. Round-13 copy: `.ufo/waves/round-13/frozen/verify.py`, `SKILL.md:510`.

Its shape is right; four defects must not be inherited:

- **P1 expected.json unpinned.** `load()` reads `expected.json` (`verify.py:57-59`) and no digest binds those bytes. Editing `expected_exit` (`expected.json:6`) alone reaches `evaluate()` and returns 1 (`:125-131`), the changed-verdict code.
- **P2 duplicate keys accepted.** `json.loads` keeps the last value (`:59`); `{"inputs":{"gate.sh":GOOD,"gate.sh":BAD}}` passes the exact-set check at `:67` with BAD.
- **P3 check-then-use TOCTOU.** Digest taken from `target.read_bytes()` at `:91`; the file is executed later by `bash gate` at `:113-114`. Bytes may change in between. Harness path is likewise pinned by digest and executed by path.
- **P4 selftest coverage gap.** Cases at `:158-177` cover clean, changed verdict, changed input, missing input, malformed JSON. Not covered: expected.json tamper, symlink, extra entry, duplicate key, verdict-rescue, absence of verdict output in tampered runs.

Repo precedents for "could not evaluate, not fail":
- `tools/mado-verify.sh:1891-1896`: pin mismatch → `MADO_REGRESSION: SETUP`, exit 2, "never a stale PASS"; `:1926-1936`: only a non-reproducing table is FAIL (1).
- `corpus/knowledge/gate-standing-use.md` §5.3: "A SETUP is not a gate failure … only FAIL names a non-reproducing table." §5.4: "Pins are never edited to match reality."
- `tools/mado-verify.sh:2300-2326`: snapshot loader refuses malformed, unreconciled or edited receipts with rc 2 and writes nothing.

## 4. Exit and stable-id map (required for the frozen mode)

| Outcome | Exit | Stable id | When |
|---|---|---|---|
| replay match | 0 | `frozen_match` | pin matched; plan/policy digests matched; computed code **and** finding equal expected |
| changed verdict | 1 | `frozen_verdict_mismatch` | pin and input digests matched; computed code **or** finding differs. The only path to 1 under `--frozen`. |
| tampered snapshot | 2 | `snapshot_tampered` | any pin, digest, exact-set, type, symlink, FIFO, directory or device failure on DIR entries or expected bytes; classifier not called |
| could not evaluate | 2 | `frozen_error` | pin ok but expected.json unparseable or schema-invalid; usage conflict; unpinned invocation |

Decision for L1 (recorded, not imposed): under `--frozen`, exit 0 means **replay matched**, not `plan_safe`. A frozen red fixture (expected code 1) exits 0 with `frozen_match`. A naive caller could read that as safe. Required mitigation: a frozen run prints no classifier finding token (e.g. `plan_safe`), and the SKILL row states the replay meaning. The alternative (pass through the computed code) makes exit 1 ambiguous between "blocked" and "mismatch"; not recommended.

## 5. Required operation order (SafetyGate)

- **R-1 argv.** `--frozen DIR` requires `--frozen-pin SHA` (64 lowercase hex). Missing pin → 2 `frozen_error` ("unpinned"). `--frozen` combined with `--plan` or `--policy` → usage, 2.
- **R-2 DIR entries.** Enumerate with `os.scandir` (no follow). The name set must equal exactly `{expected.json, plan.json, policy.json}`. Any extra name (backup, dotfile, editor swap, subdirectory) → 2 `snapshot_tampered`, naming it.
- **R-3 open discipline.** For each of the three files: `os.open(path, O_RDONLY | O_NOFOLLOW | O_NONBLOCK)`, `os.fstat`, require `S_ISREG`. Symlink, FIFO, directory or device → 2 `snapshot_tampered`. `O_NONBLOCK` stops a FIFO from hanging the gate.
- **R-4 single read.** Read each file's bytes once. Hash those bytes (`hashlib.sha256`). The same bytes are parsed and classified. No second path open anywhere after R-3.
- **R-5 pin first.** `sha256(expected.json bytes) == --frozen-pin`, else 2 `snapshot_tampered` naming `expected.json`. Only after this does expected.json get parsed.
- **R-6 expected schema.** `json` parsed with `object_pairs_hook` that rejects duplicate keys. Top-level keys exactly `{inputs, expected_code, expected_finding}`; `inputs` keys exactly `{plan.json, policy.json}`; digests 64 lowercase hex; `expected_code` an int, not bool, in {0,1,2}; `expected_finding` a non-empty string. Failure → 2 `frozen_error`.
- **R-7 input digests.** `sha256(plan bytes)`, `sha256(policy bytes)` vs expected. Mismatch → collect all failures, print them, return 2 `snapshot_tampered`. **The classifier is not called.**
- **R-8 classifier input.** Frozen mode calls `classify(plan_bytes, policy_bytes)` on the bytes already hashed. No classifier-side file reads in frozen mode.
- **R-9 compare.** Code and finding both equal → `frozen_match` 0; either differs → `frozen_verdict_mismatch` 1. Code-only comparison is not enough (SelftestTruth: code + finding).
- **R-10 no execution.** No subprocess, no exec of any argv, no host inspection, no network. Print `GATE_SHA256` (sha256 of the gate's own source) as provenance, not gated.

Ordering property to test: no classifier output and no verdict token is printed before R-7 completes.

## 6. Control matrix

Tamper rows must return **exit 2, `snapshot_tampered`** (or `frozen_error` where marked), with no classifier finding token in stdout. Forbidden outcomes are listed explicitly; any of them is a defect.

| ID | Mutation (DIR fixture; baseline is a red libinput `sudo pacman` plan, expected code 1) | Required | Forbidden |
|---|---|---|---|
| T01 | plan.json one byte changed (`pacman` → `pacmaN`) | 2 snapshot_tampered | 1, 0 |
| T02 | red plan edited to safe (sudo action removed) | 2 snapshot_tampered | 0 plan_safe |
| T03 | plan.json semantically identical reformat (key order / whitespace / trailing newline) | 2 snapshot_tampered (byte-exact by design) | 0, 1 |
| T04 | policy.json `paused: true` → `false` | 2 snapshot_tampered | 0, 1 |
| T05 | policy.json allowed list gains `package-install` | 2 snapshot_tampered | 0 |
| T06 | policy.json whitespace-only edit | 2 snapshot_tampered | 0, 1 |
| T07 | plan.json absent | 2 snapshot_tampered, names plan.json | any |
| T08 | policy.json absent | 2 snapshot_tampered, names policy.json | any |
| T09 | plan.json replaced by symlink to a byte-identical copy (inside and outside DIR) | 2 snapshot_tampered | 0, 1 |
| T10 | plan.json replaced by FIFO | 2 snapshot_tampered within timeout (no hang) | hang |
| T11 | extra entry in DIR (`policy-override.json`, `plan.json.bak`, dotfile) | 2 snapshot_tampered, names entry | 0, 1 |
| T12 | `plan.json` is a subdirectory | 2 snapshot_tampered | any |
| T13 | expected.json `expected_code` (or `expected_finding`) edited; inputs untouched | 2 snapshot_tampered via R-5 pin | **1 frozen_verdict_mismatch** |
| T14 | expected.json input digests rewritten to match a tampered plan | 2 snapshot_tampered via R-5 pin | 0, 1 |
| T15 | expected.json with duplicate key `"plan.json"` (last-wins trap) | 2 snapshot_tampered (pin fails first) or frozen_error if pin set to match the bad bytes | 0, 1 |
| T16 | expected.json malformed: extra key, `expected_code: true`, uppercase digest, `expected_code: 3`, non-string finding; pin set to match these bytes | 2 frozen_error | 0, 1 |
| T17 | expected.json absent | 2 frozen_error | any |
| T18 | `--frozen DIR` without `--frozen-pin` | 2 frozen_error ("unpinned") | any run |
| T19 | `--frozen DIR --plan X` | usage, 2 | any run |
| T20 | verdict-rescue: plan tampered but computed verdict still equals expected | 2 snapshot_tampered | 0 frozen_match |
| T21 | ordering: plan tampered so computed verdict differs from expected | 2 snapshot_tampered | **1 frozen_verdict_mismatch** |
| T22 | every T01–T21 run: stdout contains no classifier finding line or verdict token | asserted | any finding token |

Green and discriminator controls (must **not** return 2):

| ID | Setup | Required |
|---|---|---|
| G01 | intact DIR, safe plan, expected 0 + `plan_safe` | 0 `frozen_match`; FROZEN_INPUT lines for both files |
| G02 | intact DIR, red libinput plan, expected 1 + its finding | 0 `frozen_match`; detail shows computed 1 = expected 1 |
| G03 | G01 DIR copied to another path, mtime touched | identical result to G01 (digest is over bytes, not path or mtime) |
| G04 | intact DIR, valid pin, deliberately wrong expected code | 1 `frozen_verdict_mismatch`. Proves the changed-verdict path stays reachable and is distinct from tamper. Also: same code, different finding → 1. |
| G05 | same command as T02, reason-only delta (one byte in plan restored vs. not) | tampered → 2; restored → 0 or 1. Shows the discriminator is the digest, not the verdict. |

## 7. Selftest contract (SafetyCases / SelftestTruth)

- Each case runs `sys.executable tools/mado-action-plan.py --frozen DIR --frozen-pin PIN` as a **subprocess** and asserts exit code **and** the `FROZEN_ID:` line. Tamper cases also assert that no classifier finding token appears (T22). Helper-only function tests do not exercise argparse, exit paths or ordering; they are insufficient.
- Fixture digests and pins are **literals** written into the selftest, computed by an independent `sha256sum` at authoring time by L1 or SafetyCases, never by the gate's own code path (round-14 pattern `verify.py:26-37`; "hard-coded fixture is not actual package validation", round-15 spotcheck R15-V2).
- The red fixture is the in-memory libinput `sudo pacman` action literal. Fixtures are temp dirs; removed on pass, kept on fail with the path printed (precedent `verify.py:178-185`).
- Nothing in the selftest touches the host, `pacman`, a service or the compositor. Gate never executes fixture argv.

## 8. Residuals — not closed by these controls

- **E1 same-commit substitution.** Gate source, frozen DIR and pin changed together in one commit: undetectable in-band. Controls: git review and `GATE_SHA256` recorded in the receipt.
- **E2 pin provenance.** The pin is only as trustworthy as where it is recorded. A pin copied from inside the DIR is self-certifying. Record it in the round report / LOG, outside the DIR.
- **E3 byte-exact by design.** Benign reformatting of plan or policy returns 2 (T03, T06). No canonical-JSON equivalence is offered.
- **E4 replay ≠ safety.** A frozen match proves the recorded classification reproduces. It does not prove the plan is safe to run. The classifier is bounded and declared-plan only (spec); wrapper and indirection cases (`env`, `sh -c` through an absolute path, aliases) remain classifier limits, owned by ExecBasename / SafetyService.
- **E5 TOCTOU after exit 0.** Frozen mode says nothing about later host state or any live file.
- **E6 precedent debt.** P1–P4 remain in the round-14 runner. This seat did not edit it. Any correction is an appended erratum owned by L1. The round-14 registry row must not be cited as evidence of expectation integrity.
- **E7 no execution.** Nothing above was run. Each control is design-level until SafetyCases / L1 runs the subprocess selftest once after integration.

## 9. Routing

- **SafetyGate:** R-1 to R-10 (§5); exit semantics (§4); `--frozen-pin` flag. The flag is an addition to the literal `--frozen DIR` text in the spec. L1 must confirm it under "Report API exactly".
- **SafetyCases:** T01–T22 and G01–G05 as case rows: name, DIR fixture, pin, expected code, expected finding, expected exit, expected id.
- **GateRegistry / SKILL row:** must state the pin requirement, that exit 0 under `--frozen` is replay match (not `plan_safe`), and E1–E5.
- **L1 decisions:** pin as CLI flag (recommended) vs. source constant in the `PIN_MADO` style; whether to append an erratum on the round-14 runner (P1–P4).

## 10. Tooling and commands

- Installs: none. Contract NoInstalls prevails over the generic tooling directive this round.
- Commands run: none. Read-only tools only (`read`, `glob`, `grep`).
- Peers: one status message to `MadoR16` (planner) only.
