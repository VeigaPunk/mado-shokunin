# AttackCodeBinding — round 16 w2 (C2 gate receipt vs frozen pins)

Seat: `MadoR16.AttackCodeBinding` (leaf reviewer, read-only, no subagent dispatch).
Baseline: `32c4fda873c9cb47a84c549b24b80ead2bcaa1ea`. Target root:
`/home/vgpnk/Projects/shokunin/mado-shokunin`.

Scope: whether the round-16 receipt can bind a **committed gate digest** to the
**frozen input pins** of `tools/mado-action-plan.py --frozen`. No historical
executable equivalence is claimed. Only the current working-tree bytes are
described, each with its observation time.

## 0. Execution and tool record

- Gate, selftest, `--frozen` replay, `--plan`, `measure.py`, `mado-verify.sh`,
  pacman, services, probes: **not run**. Gate bytes were read as text only.
- Read-only commands used: `sha256sum`, `ls`, `wc`, `grep -c`, `find`,
  `git status --porcelain`, `git cat-file -e`, `git log --all -- <paths>`,
  `git check-ignore`, `git show HEAD:...` (none of these execute the gate).
- One `python3 -c` one-liner parsed `safety-cases.json` as JSON data for the case
  table. It did not import or run the gate.
- No installs, updates, or package operations. None were needed.

## 1. Verdict

**Receipt requirement NOT MET.** Frozen input pins match the current bytes, but no
committed gate digest exists, and nothing ties the gate's own bytes to the frozen
pins.

| Requirement | Observed state | Result |
|---|---|---|
| R1 committed gate digest (`git show <rev>:tools/mado-action-plan.py \| sha256sum`) | `tools/mado-action-plan.py` is `??` untracked at HEAD `32c4fda`. `git cat-file -e HEAD:tools/mado-action-plan.py` fails. `git log --all -- tools/mado-action-plan.py .ufo/waves/round-16` prints nothing. | **absent** |
| R2 receipt file that records a gate digest | No round-16 receipt or bindings file exists. `find .ufo/waves/round-16 -iname '*receipt*' -o -iname '*binding*'` returns only `w1/reports/SafetyReceipt.md`, a draft that says "the receipt cannot bind a gate digest yet", and `evidence/source-bindings.json` (S053/S054 only). | **absent** |
| R3 frozen plan pin matches live plan bytes | `sha256sum frozen/plan.json` = `82bc76520ee23804f20efb106df61023c30c2b74447ade39953a493a035febc3`; `expected.json` `plan_sha256` is the same. | **match** (working tree) |
| R4 frozen policy pin matches live policy bytes | `sha256sum frozen/policy.json` = `fb134d8f90d1bb4afbe11df874b5605024aeb2da64b393ed2c7536c15b18b7fc`; `expected.json` `policy_sha256` is the same. `safety-policy.json` is byte-identical. | **match** (working tree) |
| R5 pins bound to a committed revision | `frozen/` and all round-16 artifacts are `??` untracked. `expected.json` sha256 `e76090a3c0079582c090a441de12e2eb1d190da981b556ac13d78944f6bbe535`, itself unpinned. | **absent** |
| R6 gate digest recordable inside `expected.json` | `_EXPECTED_KEYS` (`tools/mado-action-plan.py:127`) excludes any gate key. `run_frozen` (`:415-418`) returns `frozen_error` (exit 2) on an unknown key. The gate digest cannot be added as provenance without a code change, which would move the digest. | **blocked by design** |
| R7 measure binds the gate at a committed revision | `SAFETY_ARTIFACTS` (`measure.py:362-366`) lists the gate, policy, and cases, read via `git show REV:path`. An untracked path yields `CalledProcessError`, then `present: False` (`measure.py:74-79`, `:368-376`). Inference from source, not executed. | **inert until committed** |

The gate's current working-tree SHA-256 is
`14bfa57b75b52f0b80147c0cb5d25f7272eac627905e830a8c8de09e6d869a0d`
(mtime 05:53:11). This is **not** a committed digest and is **not** equivalent to
any historical bytes. An earlier observation, `e506bc23…` at 05:46, is superseded
(see §2).

## 2. Stale-read correction (gate moved mid-review)

The gate changed between my first read (05:46, 752 lines, sha `e506bc23…`) and a
later check (05:53, sha `14bfa57b…`). I re-read the changed regions. Findings on
the 05:46 bytes are superseded:

- **Superseded (fixed at 05:53):** the 05:46 `run_frozen` hashed `plan.json` and
  `policy.json`, then re-opened them through `_evaluate`. A writer could swap bytes
  between the digest check and classification (TOCTOU). Current `run_frozen`
  (`:437-451`) reads each file once, hashes those bytes, and classifies the same
  buffers via `_evaluate_raw`. `_read_regular` (`:150-181`) now uses `O_NOFOLLOW`.
- **Still valid:** the other findings below are about the 05:53 bytes.

## 3. Counterexamples and bounded findings (05:53 bytes; source reading only)

**F1 — Frozen pins are self-referential (binding gap).** `expected.json`,
`plan.json`, and `policy.json` are all untracked. An editor who rewrites all three
together gets a self-consistent `frozen_match` with no trace in git. Nothing outside
the directory anchors these bytes. This is the core reason R1 is unmet.

**F2 — Frozen replay checks one verdict, not classifier behaviour.** The only pinned
expectation is `denied_executable:sudo` / exit 1 for the sudo-wrapped libinput plan
(`expected.json`). A classifier edit that still returns that verdict for this plan
(e.g. changing `_basename` for other inputs, or the `_classify` ordering of unrelated
kinds) keeps `frozen_match` exit 0 [INFERENCE from `run_frozen` `:452-457` and
`_classify` `:327-357`]. The frozen row is a one-case tamper and digest check, not a
gate-equivalence check.

**F3 — Two unbound copies of the policy.** The gate's default policy is
`.ufo/waves/round-16/safety-policy.json`, which `measure.py` hashes at a committed
revision. The frozen replay uses `frozen/policy.json`, which nothing hashes at a
committed revision. Both are `fb134d8f…` today. No check ties them. Drift between
them is undetected.

**F4 — The policy file is a mirror, not the authority.** `_validate_policy`
(`:232-289`) returns the code constants `PINNED_*` regardless of file content. A
policy file that deviates from the pinned semantics yields `policy_malformed`
(exit 2). The authority is the classifier source, not `safety-policy.json`. A
constant-only edit (e.g. removing `sudo` from `PINNED_DENY_EXECUTABLES`) makes the
policy file invalid. The frozen check then reports `frozen_verdict_mismatch`
(`got policy_malformed`). That is detected. A logic-only edit is not detected by F2.

**F5 — Wrapper bypass (declared classifier limit, not a binding defect).** `_basename`
(`:319-324`) and `_classify` (`:327-357`) test only `argv[0]`'s basename against
the 12-name list. Wrappers outside that list pass as `plan_safe` [INFERENCE from
source]. Examples: `["nice","pacman","-S","libinput"]`, `["timeout","5","pacman",…]`,
`["doas","pacman",…]`, `["pkexec",…]`, `["xargs","pacman",…]`, `["setsid","pacman",…]`,
`["su","-c","pacman …"]`, `["run0", …]`, `["busybox","sh"]`. `SKILL.md` row
`mado-action-plan` and the cases-file `scope_limit` state that unlisted argv[0]
values pass. The cases file pins only `omarchy-pkg-add` and `python3 -c` as
residual controls. These extra examples are unpinned. They are declared residuals,
not a promise of enforcement.

**F6 — Cases file has no consumer; selftest does not read it.** `safety-cases.json`
(31 cases) is referenced only by SKILL and the cases header. No gate, selftest,
`measure.py`, or frozen path reads it. The gate's selftest has 35 in-file cases plus
5 frozen fixtures (`run_selftest`, `:518-745`), with no cross-reference. A static
trace of all 31 cases against `_validate_plan`/`_validate_policy`/`_classify` agrees
with each `expected_code` and `expected_finding` [INFERENCE from source; not executed].
Nothing enforces that agreement going forward.

**F7 — SKILL overclaims a receipt that does not exist.** `SKILL.md:530` says the
frozen row's "receipt separately binds executable and expectation digests to measured
commit". `SKILL.md:540-542` says "committed digest [is] harm-watch evidence". There is
no receipt and no committed digest (R1, R2). `git diff --stat HEAD -- SKILL.md` shows
43 uncommitted insertions, so the claim is also not committed. The w1 draft
`SafetyReceipt.md` correctly says the receipt "cannot bind a gate digest yet". SKILL is
L1-owned; this seat does not edit it.

**F8 — `tools/__pycache__/` is not ignored and holds a bytecode artefact.**
`git check-ignore tools/__pycache__/mado-action-plan.cpython-314.pyc` exits 1.
`.gitignore` contains only `.ufo/interactive-sessions/`. A
`mado-action-plan.cpython-314.pyc` (36,541 B, 05:46) is present, which means some
process imported the gate module at 05:46. Its cause is not recorded here. A
commit using `git add -A` would sweep the `__pycache__` in.

**F9 — Symlink rejection is leaf-only and untested.** `_read_regular` uses
`O_NOFOLLOW` (`:155`), which protects only the final path component. A symlinked
parent directory is still followed. No selftest fixture covers a symlink input. The
docstring (`:151-154`) does not overstate this, but a SKILL reader might.

**F10 — Documentation drift in the gate.** `tools/mado-action-plan.py:22` refers to
`PINNED_POLICY`, which does not exist. The constants are `PINNED_PAUSED_SCOPE`,
`PINNED_DENY_EXECUTABLES`, `PINNED_KINDS`. Also, `--selftest` exit 1 equals the
denial exit code. SKILL documents this, but the gate docstring's exit map (`:41-57`)
omits selftest.

**F11 — Non-ASCII in gate and cases (measure hashing).** `measure.py` hashes
`git show` text re-encoded to UTF-8 (`:64`, `:70-71`, `:372`). The gate has 2
non-ASCII lines and `safety-cases.json` has 1. No CR bytes are present, so the
re-encoded hash equals the raw SHA-256 under a UTF-8 locale [INFERENCE]. This would
not hold under a non-UTF-8 decode. Minor, noted for any future committed-digest
receipt.

## 4. What L1 must decide (not implemented here)

1. Commit the gate, policy, cases, and `frozen/` as one revision. Record the gate's
   `git show <rev>:tools/mado-action-plan.py | sha256sum` in a committed bindings
   file, written by a process other than the verifier (FrozenDesign rec 2). Include
   `expected.json`, `plan.json`, `policy.json` digests at that revision.
2. Decide between enforcing the gate digest (a gate edit then becomes
   `snapshot_tampered`) or recording it as provenance (L1 decision, per GateRegistry
   §3). Either way `_EXPECTED_KEYS` must change, which moves the gate digest. Re-measure
   after that change.
3. Correct SKILL `:530` and `:540-542` to match what exists, or land the receipt
   first.
4. Add `tools/__pycache__/` to `.gitignore` or exclude it from commits.
5. Optional: add frozen cases for classifier-logic regressions, or explicitly state
   that the frozen row is single-verdict.

## 5. Limits

- Source reading only. No gate run, no frozen replay, no selftest, no measure run,
  so every behavioural statement above is `[INFERENCE from source]` and needs L1's
  verification run.
- Digests are working-tree observations at the times stated, not committed
  identities.
- F5 is a declared classifier limit under the round's scope, not a claim of
  enforcement. The policy file's own text disclaims host, privacy and probe safety.
