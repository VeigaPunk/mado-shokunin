# AttackPause — policy validation, exact `paused` true, strict JSON, fail-open search

Seat: `MadoR16.AttackPause` (sentinel, leaf). Scope: whether the integrated
`tools/mado-action-plan.py` policy path can be made to accept a non-pinned
policy, or to classify a plan more permissively, via `paused`, duplicate keys,
non-finite numbers or unknown fields. Source reading only. No gate run, no
selftest, no frozen replay, no probe, nothing installed or updated (record:
none). The only code I executed was a stdlib `json.loads` check in an isolated
Python session that did not import the gate (§F2). I wrote this file and
nothing else.

## Snapshot binding (the gate was edited while I reviewed it)

The working-tree gate changed four times during this review:
`e506bc23…` → `eee51dda…` → `c78bfcff…` → `ed921141…` → **`6c8c714b086b9a886570b9ac3e298dcd08c176579b63cee92a41ef755a63780b`**
(828 lines, mtime 05:55:57-03:00). The verdicts below apply to `6c8c714b`, and
line numbers refer to that file.
The other files did not change during the review:

- `safety-policy.json` `fb134d8f…`, byte-identical to `frozen/policy.json`.
- `safety-cases.json` `9d0fac4e…`.
- `frozen/expected.json` `e76090a3…`.
- `frozen/plan.json` `82bc7652…`, which equals its pin.

Every file is untracked at HEAD `32c4fda`. These are working-tree reads, not
committed blobs. If the gate changes again, L1 must recheck §F1.

## Axes

A1: no policy-side fail-open. A2: claimed strictness matches the code.
A3: the fixtures can tell a correct validator from a broken one.
A4: frozen-mode provenance.

## Headline: zero policy-side fail-open paths in `6c8c714b`

- **Exact pause check** (`_validate_policy` `:245-247`):
  `type(paused) is bool and paused is True`.
  - Rejected: absent (`None`), `false`, `"true"`, `1`, `1.0` and `null`.
  - Duplicate `paused` keys are rejected before validation runs
    (`_strict_pairs` `:188-195`, applied to every nested object through
    `_parse_json_bytes` `:201-213`).
  - My stdlib check confirmed that `"pa\u0075sed"` is unescaped first, so it
    collides with `paused` as a duplicate.
- **Unknown fields are rejected at every object level:**
  - policy top level `:241-242`
  - each kind rule `:275-276`
  - plan top level `:301-302`
  - each action `:312-313`
  - `expected.json` (unknown-key check right before `:423`)

  The only non-object containers are `paused_scope` and `deny_executables`,
  which must be string lists with no duplicates and must equal the pinned
  sets (`:248-262`).
- **The supplied policy never drives classification.**
  - On success, `_validate_policy` returns code constants: `"paused": True`,
    `PINNED_*` and `dict(pinned_rule)` (`:288-293`, built at `:287`).
  - `_classify` (`:331-363`) reads only that normalized object.
  - So even a broken validator could not make any plan verdict more
    permissive. A validator bug could only accept a dishonest policy file,
    never change a plan verdict. This is why A1 is empty.
- **Policy is checked before the plan**, in both modes (`_evaluate_raw`
  `:366-386`).
- **Read-once (frozen):** `run_frozen` now hashes and classifies the same
  bytes (`:451`, `:454-455`). This closes the hash-then-reopen TOCTOU that
  `e506bc23` had: `_sha256(path)` followed by `_evaluate(path)`.
- **Leftover exceptions:** they now go to the `main` guard
  (`except Exception` at roughly `:816-825`), which exits 2.
  - `parser.error` raises `SystemExit`, a `BaseException`, so it bypasses the
    guard and still exits 2.
  - `RecursionError` from deep nesting and int-digit `ValueError` are caught
    inside `_parse_json_bytes`.

## Findings

### F1 — Medium (A3, evidence strength): two strictness promises lack discriminating fixtures, and all five `safety-cases.json` policy rows are vacuous

**Evidence**

- The docstring (`:31-33`) promises: "duplicate keys, non-finite numbers
  (NaN/Infinity) … fail closed".
- QUALITY 21 and SCORECARD `:703-707` credit a "persisted paused policy".
- On the policy side, the selftest has discriminating rows for:
  - `paused` false, `"true"`, `1` and `null` (`:606-611`, `:645-650`; the
    `1` and `null` rows were added during this review)
  - missing `paused` (`:600`)
  - unknown top-level key (`:630`)
  - allow, remove, add and shrink edits (`:612-640`)
- But the duplicate-key fixture is plan-only (`:586`), and so is the
  non-finite fixture (`:589`).
- There is **no** fixture for:
  - a policy with a duplicate key
  - a policy with NaN/Infinity
  - an unknown key inside a kind rule (`kinds.read-source.note`)
  - a wrong policy `schema`

**Mutations that survive** (my reasoning from reading the fixtures; I did not
run them). All selftest policy fixtures are produced by `json.dump`, which
never emits duplicate keys or NaN.

- **M-a.** In `_evaluate_raw` `:369`, parse the policy with plain
  `json.loads(policy_raw.decode())` instead of `_parse_json_bytes`. Every
  fixture still passes. Inputs this mutant then accepts, though the promise
  says they fail closed:
  - the canonical policy bytes with `"paused": false,` inserted before
    `"paused": true` (last value wins)
  - `"paused": true` preceded by `"paused": NaN`

  This is exactly the edge that `FindingStability.md` F2/E2 called the most
  important fail-open edge.
- **M-b.** Deleting `:274-276` (the kind-rule unknown-key check) survives.
- **M-c.** Deleting `:243-244` (the policy schema check) survives.

**`safety-cases.json` rows 332–410:** `policy_paused_boolean_false`,
`policy_paused_string_false`, `policy_paused_numeric_one`,
`policy_paused_missing` and `policy_extra_allow_key`.

- Each embeds a *partial* policy, such as `{"paused": false}` or
  `{"paused": true, "allow": [...]}`.
- Their own `policy_field` assumption (line 16) says the embedded object
  *replaces* the whole policy. Those objects lack `paused_scope`,
  `deny_executables` and `kinds`.
- So they are rejected at `:249-250` whether or not the `paused` check
  (`:246`) or the unknown-key check (`:241`) exists. They cannot detect
  either check being deleted.
- Expected codes and findings are still correct; the rows are just vacuous.

**Impact:** no plan verdict changes (see headline). What is lost is mutation
evidence for the literal claim that duplicate and non-finite *policy* bytes
fail closed.

**Smallest remediation (gate/cases owner):**

- Add four selftest rows, each built from the canonical policy with one
  change and expecting `2/policy_malformed`:
  - raw bytes with `"paused": false,` inserted before the existing
    `"paused": true`
  - raw bytes with `"paused": NaN`
  - `kinds.read-source` given an extra key
  - `schema: "x"`
- In `safety-cases.json`, state that the embedded policies replace the
  canonical policy with one key changed, or label the five rows as
  "any-malformed" controls, not paused-check discriminators.

### F2 — Low (A2, wording): `parse_constant` does not catch overflow literals

**Evidence**

- `parse_constant` (`:197-198`, `:208`) fires only on the tokens `NaN`,
  `Infinity` and `-Infinity`.
- In a stdlib-only session (the gate was not imported), with the same hooks:
  - `json.loads('{"paused": 1e400}', object_pairs_hook=…, parse_constant=…)`
    returned `{'paused': inf}`.
  - `-1e400` returned `-inf`.
  - `NaN` and `-Infinity` raised errors.

**Exploit path: none.** No schema slot accepts a number:

- `paused` must be a bool.
- Every list must contain strings.
- `disposition` is compared to a string.
- `argv_nonempty` must be a bool.
- `schema` is compared to a string.
- `expected_exit` must satisfy `type(...) is int`.

So `inf` is always rejected with exit 2. The only problem is the reason text:
`{"paused":1e400}` produces "policy.paused must be exactly the boolean true",
not "non-finite".

**Remediation:** either word the promise as "NaN/Infinity tokens; overflow
literals are rejected by the schema", or add a `parse_float` hook that rejects
non-finite results via `math.isfinite`.

### F3 — Info (A2): `paused` is a validated precondition, not a switch; one branch is unreachable

**Evidence**

- In `_classify`, `paused` (`:333`) is always the constant `True` from
  `:289`.
- The deny kinds equal `PINNED_PAUSED_SCOPE` exactly, so the
  `rule["disposition"] != "allow"` branch (`:347-349`) can never run.

**Consequences**

- No policy file can express an unpaused state.
- Lifting the pause needs a code change. That matches SKILL `:483-487`
  (future operator lift).
- This settles `GateRegistry.md`'s [BIND] note: the gate does not ignore
  `paused`. It refuses any policy without exact `true`, and has no runtime
  pause toggle.

**Remediation:** wording only, e.g. "paused=true is a required pinned
precondition". Optionally delete the dead branch. Neither is safety-relevant.

### F4 — Info (A4): frozen `expected.json` is self-attesting in the directory

`expected.json` is not pinned by anything inside `frozen/`.

**Counterexample:**

1. Rewrite `policy.json` with `paused: false`.
2. Update `policy_sha256` in `expected.json` to match.
3. Set `expected_finding: "policy_malformed"` and `expected_exit: 2`.

The result is `frozen_match`, exit 0 (`:456-457`). The directory now records
an unpaused policy under a green comparison.

The SKILL frozen row (`:530`) already limits what this means ("never that a
red plan is safe") and promises that a receipt will separately bind the
executable and expectation digests to the measured commit.

**Observed state:** no such receipt exists yet. `.ufo/waves/round-16/evidence/`
holds only `source-bindings.json` and `census-before.txt`; a grep for
`e76090a3` / `fb134d8f` / `82bc7652` outside `frozen/` finds nothing.

**Condition for L1:** the post-integration frozen receipt must record:

- `expected.json` = `e76090a3…`
- the gate digest that actually ran (not `6c8c714b` if it changes again)
- the measured commit

### F5 — Info (usage hygiene, not fail-open)

- **`--frozen DIR --policy X`:** the `--policy` value is silently ignored
  (`main`, `:812-813` area). The frozen run uses `DIR/policy.json`, which is
  still fully validated, so nothing fails open.
- **Selftest crash label:** an internal exception during `--selftest` exits 2
  but carries the finding `plan_malformed` (the `finding = …` line at
  `:821`). SKILL `:529` describes the selftest outcomes as "0 clean, 1
  failed". Exit 2 is not 0, so this is still fail-closed, but the label is
  misleading.

## Out of my scope (pointer only, not a defect claim against the declared limit)

- An argv[0] of `"pacman\u0000"`: `_basename` (`:323-329`) strips whitespace
  but not NUL, so the name is not in the deny set and the plan gets
  `plan_safe`.
- Similarly `"/usr/bin/pacman/."` gives basename `.`.
- Neither name runs pacman through a normal `execve`. Both fall under the
  declared lexical argv[0] limit (SKILL `:533+`). They belong to the argv
  seat, not to the pause and policy surface.

## Not done / limits

- I ran no gate, selftest, frozen run, mutation harness or census. The
  surviving mutants in F1 come from reading the fixture list at
  `:523-672`, `:741-764`, not from execution.
- The selftest count is not restated, because the file was still growing
  (35 → 46 plan/policy rows, plus 5 frozen rows, as of `6c8c714b`).
- I did not check the committed-blob digest.
- No tools were installed or updated.
