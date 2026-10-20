# FrozenDesign — round 16 w1 (mado): snapshot digest and expected-verdict design

Seat: `MadoR16.FrozenDesign` (reviewer, leaf). Scope: review the snapshot digest and expected-verdict design; advise immutable snapshot inputs.
Method: source reading of `tools/mado-verify.sh`, round-14 `frozen/` precedent, round-15 committed bindings, and `corpus/knowledge/gate-standing-use.md`. Two read-only `sha256sum` calls. No gate, selftest, regression, harness, build, package, or host probe was run. No installs. No files written except this report.

## Axes

- **A1 digest binding:** which bytes are pinned, and by what anchor.
- **A2 expected-verdict binding:** which outcome tuple is pinned, and to which gate revision.
- **A3 fail-closed ordering:** tamper, missing, or malformed input yields exit 2 before any verdict is produced.
- **A4 no-harm:** no execution of supplied inputs, no host reads.

## Observed state (this round)

| Item | Observation | Anchor |
|---|---|---|
| Gate `tools/mado-verify.sh` | sha256 `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`, 3711 lines, 177849 B. Equals the round-15 measured-content digest. This is a working-tree read, not a git blob. | `.ufo/waves/round-15/evidence/committed-bindings.json:6` |
| Harness `tameshi-shokunin/tools/mutate-and-run.sh` | sha256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`. Equals the round-14 frozen pin and the frozen run's `REGRESSION_HARNESS`. It does **not** equal the gate's `HARNESS_SHA_RECORDED` `b56c6e57…`, nor the standing-use note's `cf41efaa…`. | `mado-verify.sh:1641`; `.ufo/waves/round-14/frozen/expected.json:4`; `.ufo/waves/round-14/evidence/frozen-regression.txt:11`; `corpus/knowledge/gate-standing-use.md` §5 rule 5 |
| C2 inputs | `tools/mado-action-plan.py` and `.ufo/waves/round-16/safety-policy.json` do not exist yet. No C2 digest exists. | `ls` on both paths, this round |
| SafetyGate spec | `--frozen DIR` verifies `expected.json` digests for **`plan.json` and `policy.json` only**. The classifier is not pinned. | `spec.json` item `SafetyGate`, prompt line 10 |
| Round-14 precedent | `frozen/verify.py` pins `gate.sh` and `harness.sh`. `expected.json` and `verify.py` are not pinned. Its self-test covers clean, verdict-mismatch, tampered, missing, and malformed. It does not cover symlink escape, duplicate keys, or verify-to-run ordering. | `.ufo/waves/round-14/frozen/verify.py:4-16,24,79-96,136-177` |

## Findings

### F1 — High: frozen pins are self-attesting

`frozen/expected.json` sits next to the inputs it pins. `verify.py` is not in its own pin set (`FILES = ("gate.sh","harness.sh")`, `verify.py:24`). Whoever can write the directory can rewrite the inputs, the digests, the expected exit, and the verifier together. The docstring calls `expected.json` "the committed input snapshot" (`verify.py:4`), but nothing ties it to a commit. The planned `--frozen DIR` inherits the same shape.

**Advice:** the anchor must live outside the frozen directory. Use the round-15 pattern: `git show <rev>:<path> | sha256sum`, recorded in a committed bindings file written by a process other than the verifier. Pin `expected.json` and the verifier too.

### F2 — High: verify-then-execute TOCTOU

`check()` hashes `target.read_bytes()` (`verify.py:91`). `evaluate()` then runs `bash <path>` (`verify.py:110-117`) and the gate re-reads the harness by path at use (`mado-verify.sh:1759`, `bash "$REGRESSION_RUNNER"`). A file swapped between hash and exec runs unverified bytes under a passing verdict.

**Advice:** copy verified bytes into a private `0700` temp directory and run or parse those copies. Alternatively, re-hash after the run and refuse on any change. For C2 the classifier never executes argv, so only "read once, parse the same buffer" applies to `plan.json` and `policy.json`.

### F3 — High: the regression verdict depends on an ungated, unrecorded harness

The regression mode prints the harness digest as "provenance, not gated" (`mado-verify.sh:1866-1867`). The verdict is decided by the harness's own `results.tsv` compared to `TABLE_MADO` (`regression_case`, `:1759-1828`). A substituted harness that emits the recorded table yields `MADO_REGRESSION: PASS`. The harness bytes (`75ed934d`) match neither the in-gate recorded constant (`b56c6e57`) nor the standing-use note (`cf41efaa`). The only current pin is the round-14 frozen `expected.json`. The move from `cf41efaa` to `75ed934d` is not recorded in the reviewed files [U].

**Advice:** gate the harness sha in the in-gate regression. The `--regression` block is excised from `PIN_MADO` (standing-use §5.6), so a harness pin there does not move `PIN_MADO`. Record the harness revision history explicitly.

### F4 — Medium: snapshot gate identity is sampled after the run

`mado_r8_snapshot_cli` runs the child at `:2115` and computes `gate_sha` afterwards at `:2215-2217`. If the gate changes during the run, the receipt binds the new code to the old rows.

**Advice:** hash before the child runs, re-hash after, and refuse with `MADO_SNAPSHOT: REFUSED` on mismatch.

### F5 — Medium: `unavailable` identity fallbacks still write receipts

`gate_sha=unavailable` (`:2217`) and `created=unavailable` (`:2219`) are written into a `WRITTEN` receipt. A receipt with no code identity should not be a receipt.

**Advice:** refuse when the gate sha cannot be computed. Do not substitute a placeholder.

### F6 — Medium: exists-check then write is not exclusive

`[ -e "$dest" ]` (`:2110`) is followed by `printf '%s' "$content" >"$dest"` (`:2230`). Two writers can race past the check. A symlink created in the gap is followed.

**Advice:** create exclusively (`set -o noclobber` with `>`, or write a temp file and `ln` it into place). Keep the existing refusal text.

### F7 — Medium: file digest conflates receipt time with verdict identity; no body integrity

The header includes `# created:`, so any file-sha changes on every write. The loader reconciles counts against the rows it reads (`:2323-2326`), so a consistently edited snapshot loads clean. The snapshot is not tamper-evident on its own.

**Advice:** define two digests.
- `file-sha256`: receipt identity, printed by `--snapshot-diff` for OLD and NEW.
- `verdict-sha256`: canonical rows, counts, and scope, excluding `created:`.

Pin expected verdicts by `verdict-sha256` against a committed copy. Never pin scratch receipts.

### F8 — Medium: input-plane identity lives in a detail string; DETAIL-CHANGED exits 0

The plane digest is computed at `mado-verify.sh:242-244`. Per standing-use §2, it appears in the `boundary.readonly` row detail. A changed detail with unchanged status produces `DETAIL-CHANGED` at exit 0 (`:2488-2490`, `:2493-2494`). So an input-byte change can exit 0.

**Advice:** add `# plane-sha256:` as a header field and make a change in it a scope change (`DIFF_SCOPE`, exit 1), like `gate-sha256`. For any frozen comparison, treat `DETAIL-CHANGED` as not-SAME.

### F9 — Medium: frozen verdict match is a substring test

`if marker not in output` (`verify.py:127`) matches the marker anywhere, including inside other lines. The expected marker `MADO_REGRESSION: PASS` omits the pinned target that the PASS line actually carries (`mado-verify.sh:1917`).

**Advice:** require exactly one anchored verdict line (`^MADO_REGRESSION: PASS \(case=…; target=<pin>\)$`). Zero or multiple verdict tokens are mismatch. For C2, match exactly one `plan_safe` or stable-reason token, and compare the full tuple.

### F10 — Low: receipts are uncommitted scratch; immutability needs a committed anchor

Standing-use §4 and §6 say receipts are never committed and are quoted in records. `/tmp` is not immutable. Frozen expected verdicts need a durable anchor. This conflicts with the "never commit the file" rule.

**Advice:** L1 to decide. Commit the expected pins and the `verdict-sha256` values, not the receipt bodies. Keep the standing-use rule for bodies.

### F11 — Low: snapshot writer and diff sit outside `PIN_MADO`

The `MADO-R8-BLOCK` pairs are excised from the derived target (standing-use §5.6). Edits to the snapshot writer or diff do not move `PIN_MADO`. Their only guard is selftest scenario S. This is designed, but it means the receipt path has no regression anchor.

**Advice:** pin the snapshot writer and diff by sha in the frozen expected pins, or treat their selftest counts as pinned constants.

## Advice: immutable snapshot inputs

1. **Pin the full input set for C2.** The verdict is a function of the classifier bytes, `plan.json`, and `policy.json`. The spec pins only the last two. Add `tools/mado-action-plan.py`. This mirrors the round-14 precedent, which pins the gate under test.
2. **Anchor out-of-band.** Record each pinned digest as `git show <rev>:<path> | sha256sum`, with the revision, in a committed bindings file. Include `expected.json` and the verifier in that file. Write the pins by a process other than the verifier.
3. **Pin the expected outcome tuple,** not a single code: `{expected_exit, expected_stable_id, expected_findings (sorted)}`, plus the classifier sha.
4. **Load rules.** Read each input once, hash the bytes, parse from the same buffer. Reject duplicate JSON keys (`object_pairs_hook`), `NaN`/`Infinity` (`parse_constant`), non-object roots, and unknown keys at every level. Open with `O_NOFOLLOW` and require regular files.
5. **Ordering.** Verify every digest before classification. A tampered or missing input yields exit 2 with `snapshot_tampered` and prints no observed verdict. A missing input counts as tampered, per the round-14 precedent.
6. **Output.** Emit exactly one anchored verdict line. A zero or multiple verdict token is a mismatch.
7. **Mado receipts.** Add `# verdict-sha256` (excluding `created:`) and `# plane-sha256` headers. Print `file-sha256` for OLD and NEW in `--snapshot-diff`. Refuse on `unavailable`. Hash the gate before and after the child run.
8. **Proposed C2 `expected.json` shape** (bytes pinned out-of-band):
   ```json
   {"inputs": {"tools/mado-action-plan.py": "<sha256>", "plan.json": "<sha256>", "policy.json": "<sha256>"},
    "expected_exit": 1, "expected_stable_id": "<reason>", "expected_findings": ["<sorted>"]}
   ```

## Residual risk and verification gaps

- Not run: gate, selftest, `--regression`, frozen `verify.py`, derived-target recompute. The round-14 frozen receipt (`target cd1d73d7…`, match=yes) is cited as historical, not re-measured.
- `SPEC_SHA` (`c7ee75b9…`) was not recomputed. It is cited from the gate constant and the round-14 receipt.
- Working-tree hash only. Committed-blob equality was not checked this round.
- Harness history between round 10 and round 14 is [U]; the reviewed files do not record the change.
- C2 classifier and policy do not exist yet. Every C2 finding is design-level until SafetyGate lands them; re-check the pins against committed bytes then.

## Tooling

No tools installed or updated. No pacman or service operations.
