# R75ScoutChain — what the round-75 instruments actually rest on

Anchors are pinned to `HEAD = 466e130775820e7ab67e06175d81dd47d1fb9b4c` (working tree clean for
tracked files). Line numbers are stable there and checkable with `git show 466e1307:<path>`.

Instrument bytes at that rev:

| path | sha256 |
|---|---|
| `quality/counters/c1-r75-landing-controls.py` | `51652b438665829f06b4178d53c6330420e6fa2ccef08bdb5c5b783196adcef5` |
| `quality/counters/c1-r75-harness-witness.py` | `6d878a0c1a2f5fae0a310b5ed1c2373a4143474c08a07afbd3d0ed72dae4de27` (identical to the freeze copy) |
| `quality/counters/c2-r75-shapes.py` | `0544c0ef9d35e5cd76a0a8090d9f3a89fa0e3bb6acccee6da43bb9a3e864419b` |
| `quality/counters/c2-r74-shapes.py` | `eb43e2b6d0fca9ce4e0de8d67473804bfab7d88dac17ba3351123e85c6506277` (base rev and HEAD) |
| `quality/counters/c1-r72-landing-controls.py` | `b6108c86e8e03befce50256e2381ec08f199a1ab7fe192aeedef70459c45857d` (= `R72_SHA256`, `c1-r75-landing-controls.py:58`) |

Revision map:

| rev | event |
|---|---|
| `def73656` | freeze (declaration, controls, both instruments) |
| `dd237a55` | first receipts: `measurement-c1-r75.txt`, `measurement-c2-r75.txt`, both `rev=def73656`, C1 harness sha `058ba699…` |
| `b545bea9` | repair 1: challenge redaction in the child-env line; gate scratch |
| `e3e29bb4` | repair 2: `env=`-only usage; dead-branch deletes stop cancelling |
| `f75afbf6`, `4527fcae` | repair 3: private no-follow generation dir (C1), pinned held generation + root refusal (C2) |
| `466e1307` | final receipts: `measurement-c1-r75-final.txt`, `measurement-c2-r75-final.txt`, both `rev=4527fcae` |

`claims-declaration-r75.md` and `controls/*.json` are **byte-unchanged since `def73656`**
(`git diff def73656 HEAD --` on both paths is empty). The instruments they describe moved four
times underneath them; the C1 harness-witness counter did not move at all.

---

## 1. C1 — where the challenge is drawn, how it travels, where it is read

### 1.1 Drawn

`c1-r75-landing-controls.py:243` — `nonce = secrets.token_hex(8)` inside `measure()`
(`:240`), after `load_generation` (`:163`) so the frozen generation is sha-pinned first
(`:190`), and before `install_rule` (`:199`). One draw per process. Line `:245` announces the
source and the pin, never the value:
`MADO_R75_CHALLENGE source=secrets.token_hex(8) length=16 generation_sha256=<r72 sha> rev=<sha>`.

### 1.2 Reaches the child

The successor does not re-implement anything: it rebinds the frozen module's **globals** —
`g = mod["measure"].__globals__` (`:201`) — and then calls the frozen body unchanged
(`:247` `mod["measure"](args)`; `:248` is dead `line = None`).

- `child_env` (`:209`) = `dict(base_env(home))` + `env["MADO_LANDING_NONCE"] = nonce` (`:211`),
  installed as `g["child_env"]` (`:233`). Every child the frozen body spawns inherits it,
  because that body resolves the name through its own `__globals__` at call time:
  `c1-r72-landing-controls.py:464` (R-child), `:491` (instrument `--selftest`), `:514`
  (`bash -n`), `:520` (M-Z mutant `--selftest`), `:548` (child-env evidence).
- The lane echoes from the same variable: `quality/landing-counters.sh:15-21` (`landing_witness`;
  silent when the var is absent or not 16 hex), called at `:226` (right after the `--selftest`
  summary, inside the same `[ "$P" -eq "$N" ]` decision) and at `:290` (after the main
  `MADO_LANDING_COUNTERS:` line, before `exit "$exitcode"`).
  `landing_witness` always returns 0, so it cannot flip a green selftest red.
- Only these three files in `quality/`+`tools/` mention `MADO_LANDING_NONCE` (grep); the
  round-74 counterpart `c1-r74-replay-witness.py` keeps its own fixture copy.

### 1.3 Parsed

`last_witness(out)` (`:108`) — reverse line scan, `WITNESS_RE.fullmatch`
(`:60`, `MADO_LANDING_WITNESS: ([0-9a-fA-F]{16})`), so the **last** parsed line wins and a
malformed later marker cannot suppress a real one; `witness_state` (`:117`) compares byte-exactly
to the nonce. Two gates, both installed as frozen-module globals:

- `credit_with_witness` (`:135`) → `g["credit"]` (`:235`) → the frozen body calls it at
  `c1-r72:525` for the **M-Z kill only** (`killed` = mz + mr at `c1-r72:593`).
- `green_with_witness` (`:131`) → `g["summary_green"]` (`:236`). Two frozen callers resolve that
  global: `contract_line` (`c1-r72:397`, verdict) and `outcome_exit` (`c1-r72:389-390`, process
  rc, reached from `c1-r72:595`). Neither function is patched — only the global they read — so
  both the printed verdict and the exit code become witness-gated in one move.

No self-echo hazard: the harness's own `MADO_R75_CHILD_ENV` line starts with a different prefix
and `fullmatch` requires the marker at column 0; `summary_fraction` (`:139`) still finds the
untouched `MADO_LANDING_COUNTERS_SELFTEST:` line before the echo.

### 1.4 Frozen r72 behaviour that still passes through unchanged

| surface | anchor |
|---|---|
| the entire `measure()` body: extraction → selftest → M-Z → M-R → contract | `c1-r72:449-596`, invoked at `c1-r75:247` |
| four-file extraction set `(landing-counters.sh, c3-r56-used-by.py, check-tool-ledger.py, mado-receipt-citecheck.py)` | `c1-r72:84`, `write_tree` `c1-r72:196` |
| extraction evidence lines (bytes + sha per file) | `c1-r72:483-487` |
| instrument selftest child, its `summary=` and `green=` field (arithmetic only, never witness-gated) | `c1-r72:490-494` |
| M-Z recipe: clause count, `mutate_clause`, `bash -n`, mutant `--selftest`, `count_fails`, `summary_fraction` | `c1-r72:508-526` |
| M-R pair: `R_TOKEN` census, `build_r_fixture`, unmutated control, `neutralize_guard`, `forged_credit` (no echo required) | `c1-r72:540-591` |
| `BASELINE = "0/2"` | `c1-r72:90`; re-hardcoded at `c1-r75-landing-controls.py:217` |
| `outcome_exit` body | `c1-r72:389-390` (only its `summary_green` is swapped) |
| every evidence line's text, changed only by the `MADO_R72`→`MADO_R75` prefix move | `c1-r75:206`, `rewrite_prefix` `:124` |
| fixture construction, git env scrubbing, fixture toplevel assertion, commit identity | `c1-r75-harness-witness.py:220-245` |

Two frozen surfaces **are** replaced, both in `install_rule`:

- `contract_line` (`c1-r75:214-220`) — same field order plus `witness=`; the `selftest=` field is
  still arithmetic-only, the echo shows up separately.
- `describe_env` (`c1-r75:224-230`) — wrapper that maps `MADO_LANDING_NONCE` to `<challenge>`
  before delegating to the frozen printer. **Added at `b545bea9`; absent at the freeze rev.**

---

## 2. C2 — delta sites against `c2-r74-shapes.py`

Non-behavioural header deltas: `TOOL`, `BASE_COUNTER` → `c2-r74-shapes.py`, `BASE_COUNTER_SHA256`
(`:55`, added in repair 3), frozen 36/32 → 47/41, `HELD_CONTROLS` → round-74 set/36 cases,
`MADO_R74_`→`MADO_R75_` prefixes, work dir `r73-c2-shapes` → `r75-c2-shapes`.

The two new rule branches:

**Branch A (D1) — name-neutral guard binding** — `c2-r75-shapes.py:349-364`, a second loop
appended to `guard_construction_lines` (`:322`). The first loop (`:325-348`) is untouched and
still requires `env_named`. Any single-target `Assign`/`AnnAssign` to a plain `Name` whose value
satisfies `mapping_has_key` (`:164-188`) is a guard binding whatever the name, `dead_lines`
honoured. `mapping_has_key` accepts a dict literal's own `"GIT_NO_REPLACE_OBJECTS"` key, one
level of `**<mapping literal>` (`:175-177`), a `dict(...)` keyword, and `**<name>` where the name
is a module mapping in `maps` (`:183-186`).

**Branch B (D2) — dominance widening + `del` cancellation** — `c2-r75-shapes.py:392-411`, second
loop of `unguarded_rebindings` (`:380`). (i) Any plain-name assignment whose value does not carry
the key cancels that name (`:398-404`) — required because Branch A made guard names
name-neutral. (ii) `del <Name>[<Constant == KEY>]` cancels `<Name>` (`:405-411`), literal key
only, `Name` target only. `dead` is honoured (`:396-397`; the parameter was added at `b545bea9`
and is passed at `:454` and `:529`). The single arbiter is `has_guard`
(`:529-536`): a guard line credits only if some launch line sits after it and no cancellation
line sits between.

Repairs **inside these two functions** after the freeze (both narrow the predicate):

- `usage_lines` `:415-430` — the positional-`Name` arm was removed at `e3e29bb4`; a git launch
  now matches only `kw.arg == "env"` (`:422-428`). At the freeze rev a guarded mapping passed
  positionally counted as handed over.
- `:396-397` — dead-branch statements stopped cancelling at `e3e29bb4`. At the freeze rev a
  `del env[KEY]` inside `if False:` cancelled a live store.

Already present before this round, unchanged: `environ_alias_guard` (`:1232-1278`) carried
`del alias[KEY]` since round 74; `environ_transport_guard` (`:1054-1088`) carried
`del os.environ[KEY]`. The round-75 `del` model is new only for the plain-name flow.

---

## 3. Declaration sentence vs code

| claim | declaration sentence | code anchor (HEAD) | agree? |
|---|---|---|---|
| C1 | one `secrets.token_hex(8)` challenge per run | `:243` | agree (all revs) |
| C1 | hands it to the child in `MADO_LANDING_NONCE` | `:209-211`, `:233` → `c1-r72:464,491,514,520,548` | agree |
| C1 | M-Z kill iff r72 arithmetic **and** last parsed echo equals the challenge byte-exactly | `:108-115`, `:135`, `:235` → `c1-r72:525,593` | agree |
| C1 | contract outcome green only under the same echo | `:131`, `:236`; verdict `:215-217`; rc via `c1-r72:389-390,595` | agree |
| C1 | `landing-counters.sh` echoes a well-formed challenge "and only then" | `landing-counters.sh:15-21,226,290` | agree |
| C1 | `TARGET_MET` iff `cases==11 && correct==11 && base_correct==6` | `c1-r75-harness-witness.py:316,322-325` | agree |
| C1 | exit map: "an absent candidate harness prints `correct=absent`" | `extract` raises (`harness-witness.py:205-209`) at `:282`; `:316` formats an int; `absent` exists only in `CONTRACT_RE` `:74-76` and one selftest string `:354` | **disagree — unreachable**: an absent candidate exits 2 with no contract line (**D-1**) |
| C1 | eleven fixture lanes, `correct=11/11` as a deterministic predicate | lane `:95` uppercases the nonce with `tr 'a-f' 'A-F'`; `:59`/`:108` compare byte-exactly against one fresh random nonce | **disagree — probabilistic**: a letter-free nonce makes `uppercase-echo` credit, `p = (5/8)^16 = 5.421e-4` (100/200 000 Monte Carlo), i.e. ≈1 miss per 1 845 runs (**D-2**) |
| C1 | docstring: challenge value never printed | freeze rev: `describe_env` unpatched → `MADO_LANDING_NONCE=<value>` inside `MADO_R72_CHILD_ENV` (`c1-r72:548`, printer `c1-r72:375-386`) | **disagree at `def73656`**, agree from `b545bea9` (`:224-230`) (**D-3**). Receipts are clean either way only because the counter discards child stdout (`harness-witness.py:302-304`) |
| C2 | counts any simple name bound to a key-carrying mapping "handed as `env=`" | `:415-430` | agree at HEAD; **disagree at `def73656`** (positional arm) (**D-4**) |
| C2 | `del env[KEY]` strictly between guard construction and launch cancels | `:392-411` + `:529-536` | agree at HEAD; **over-broad at `def73656`** (dead-branch delete cancelled) (**D-5**) |
| C2 | limit: "`del` is modelled for a literal key in the same scope only" | `:405-411` requires `Name` + `Constant`; the store side accepts module constants via `key_is_guard` (`:635-640`) | agree on the limit, but asymmetric: `KEY = "GIT_NO_REPLACE_OBJECTS"; env[KEY]="1"; del env[KEY]` classifies **guarded** (probe) (**D-6**) |
| C2 | census `population=20 readers=13 guarded=13 unguarded=0`, `controls=47/47 base_controls=41/47` | `:1299-1302`, `:1447-1469`; both receipts, identical reader rows | agree at every rev |
| both | round-74 frozen instruments byte-identical; held controls carried byte-identically | shas above; `held_check` `:1325-1352`; `BASE_COUNTER_SHA256` `:55` | agree (the base pin was added in repair 3, strictly tightening) |

D-1 and D-2 are the two findings that survive every repair: they live in
`c1-r75-harness-witness.py`, which is byte-identical to its freeze copy. D-3/D-4/D-5 were
repaired after the freeze; D-6 remains and is disclosed by the declaration's own limit.

---

## 4. What is NOT modelled (so the declared limits stay honest)

1. **The declaration describes instruments that no longer exist, and was never amended.** Four
   repair commits changed the instruments; `claims-declaration-r75.md` and both control sets are
   byte-identical to `def73656`. Its C2 "After" sentence still asserts the *pre-repair* predicate
   (positional usage counted, dead-branch delete cancelling). Both revisions score 47/47, so no
   number moved — but the frozen sentence is no longer the code's sentence, and the round has
   receipts at three revs (`def73656`, `e3e29bb4`, `4527fcae`) with no statement of which one
   the claim rests on.
2. **The C1 counter scores `mz` only.** `CAND_RE` (`harness-witness.py:67-70`) captures
   `mz=(pass|fail)`; `parse_decision` (`:212-217`) returns that group. `witness=`, `killed=`,
   `mr=`, `verdict=` are shape-checked but never scored. No fixture lane demonstrates that a
   *green outcome* is denied without the echo — only the unit selftest does
   (`c1-r75-landing-controls.py:290-292`).
3. **`witness=` is not the gate it appears to be.** `contract_line` computes the printed state
   from the **selftest** child's output (`:215` → `selftest_out`), while the M-Z kill is gated on
   the **mutant** child's output (`c1-r72:525` → `mz_out`). Two different child runs; they agree
   only because the same lane body echoes in both.
4. **`del` has many unmodelled spellings.** Probes against the pinned HEAD classifier:
   `del r.env[KEY]` (attribute target) → **guarded**; `del env[KEY]` via a module constant key →
   guarded (D-6); `child.pop(KEY)` → guarded; `del` in a called helper → guarded. All are outside
   the "literal key, same scope" limit; none occurs in `quality/check-*.py` (census 13/13 unchanged
   in all receipts), so the target is insulated — but the classifier would credit them.
5. **Line order is not execution order.** A `del` under a *live* `if` cancels unconditionally
   (probe: guarded store + `if os.environ.get("X"): del env[KEY]` → unguarded). The dead-branch
   repair only widened the gap between "syntactically reachable" and "live".
6. **No chains, one level only.** `a = dict(env, KEY="1"); b = dict(a)` → unguarded (declared
   "no chains"). `mapping_has_key` follows one `**` level of a module-level single-binding dict
   literal (`splat_mapping_names` `:589-602`); runtime-built mappings are credited only through
   `guard_producers` (`:444-477`).
7. **Values are never interpreted** — by design: `dict(env, LABEL="GIT_NO_REPLACE_OBJECTS")` is
   unguarded, and a guard whose value is `"0"` still counts as a guard.
8. **Two internal inconsistencies with no observable effect** (recorded so they are not mistaken
   for coverage): `unguarded_rebindings` is called without `dead` at `:811` (`attribute_flow`) and
   `:936` (`carrier_guard`), so those carriers still treat dead-branch statements as
   cancellations. A cancellation set can only *suppress* credit and the final arbiter
   (`:529`, `dead` passed) re-decides afterwards, so verdicts are unaffected today.
9. **C1 timeouts are misclassified.** A `subprocess.TimeoutExpired` from the frozen `run`
   (`c1-r72:172-174`) is neither `UsageError` nor `SetupError`, so it escapes the successor's
   `main` (`c1-r75-landing-controls.py:385-395`) as a traceback with exit 1 — the declaration
   reserves exit 1 for "measured and missed". Pre-existing in r72, inherited unchanged.
10. **The fixture lanes are test doubles**, declared: the echo is a pure function of
    `$MADO_LANDING_NONCE` and `MODE`, not of the assertions the lane reports. The real lane
    (`quality/landing-counters.sh`) is exercised on only one fixture producer — the C1 harness's
    own run over the real repo, recorded in `receipts/harness-real-r75.txt`, not in the eleven
    scored cases.
