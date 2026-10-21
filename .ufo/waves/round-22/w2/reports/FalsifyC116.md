# FalsifyC116 — C1 case CXReturnAfterDef (round-22 w2 advisory falsification)

Advisory, author-lane-equivalent evidence only. No admission, clearance, or non-author grant is made or implied. Production, fixtures, expected, sources, and oracle were read only. The only executed measurement is the single assigned runner invocation.

## 1. Verdict

**AGREE** for CXReturnAfterDef only, against the pinned C1 tool (`tools/mado-tripwire.py`, sha256 `36fdc459…badce`).

- Expected: exactly one `host_mutation` row, `pacman -S r22-cxafterdef-live`, `observed`. Zero leads. Zero unparsed.
- Actual (one runner invocation, one scanner child): exactly that row, zero leads, zero unparsed. Case pass 1/1, runner exit 0.
- My independent Python 3.14 derivation gives the same rows (§3).
- None of the named falsifier classes reproduced on this text (§5).

Power caveat: this case alone rejects the pre-repair "last same-named def over all top-level defs" identity and any dead-def lead or silent outcome. It does not reject a first-def-name index. That rival is caught by a different sealed case, `OriginalF3ReturnedRebound` (§7).

## 2. Sealed expectation (read from `oracle/expected.json`, id `CXReturnAfterDef`)

| field | value |
|---|---|
| group / expected_kind | proposal / exact |
| want | `[host_mutation, "pacman -S r22-cxafterdef-live", observed]` |
| accept_exact_want | null |
| forbid_observed_commands | `["pacman -Q r22-cxafterdef-dead"]` |
| forbid_commands_any_tier | `[]` |
| require_signal | true (inert under exact mode) |
| cell_count / cell_reset | 1 / `[false]` |
| fixture | `inputs/CXReturnAfterDef.jsonl`, sha256 `957a6957…5`, matches case `input_sha256` and the sealed cell text |
| proposal | `w1/proposals/CXReturnAfterDef.json`, sha256 `c3df6f70…5671`, matches the truth-seal entry |

Provenance checks (read only):
- `simple_stmts.rst` line 496 reads "return leaves the current function call" (file sha `d4320642…29dc`, as cited).
- `compound_stmts.rst` line 1253 reads "The function definition does not execute the function body" (file sha `35e6dfbf…e3e2`, as cited).
- The mechanism citation names tool `46c82902…c8c1`, `callable_info` 1646-1647. I read the frozen pre-repair copy at `evidence/tool-before.py` (sha verified). Lines 1646-1647 build `local` as a dict comprehension over all top-level FunctionDefs, so the later dead `run` overwrites the live one. Lines 1648-1652 then return it. This is provenance only. The current tool's line numbers differ; `factory_result` is at 1642-1684.

## 3. Independent semantics (no tool output used)

```python
def make():
    def run():                                   # binds local run -> A (live)
        subprocess.run(["pacman", "-S", "r22-cxafterdef-live"])
    return run                                   # leaves make(); result = A
    def run():                                   # after return: never executed, never rebinds
        subprocess.run(["pacman", "-Q", "r22-cxafterdef-dead"])
make()()                                         # calls A
```

- Exactly one subprocess call executes: `["pacman","-S","r22-cxafterdef-live"]`, no shell.
- `pacman -S` with no y/u/w/c and no s/i/l/g/p flag is a sync/install, so it is `host_mutation`. This matches the S branch of `classify_pacman` (tool 775-780).
- Uncertainty boundary: none. Control flow is straight-line, with no conditional, no environment or I/O input, and no dynamic dispatch. The dead def has no execution path, so a lead for it would be a false lead. `exact` is therefore the correct kind. Any lead or unparsed counter must fail, which is what the runner enforces.
- A `def` after `return` is legal Python. The tool's own `compile` of this cell succeeded (`eval_unparsed` = 0), which corroborates this.

## 4. Measured result (exercised)

Single invocation: `python3 -I …/oracle/measure.py --tool …/tools/mado-tripwire.py --case CXReturnAfterDef`.

- Exit 0. Stderr 0 bytes. Stdout 5,442 bytes, one JSON line. Status `complete`. Totals pass 1/1. `integrity_errors` `[]`.
- Case: `pass` true. `reasons` `[]`. `got_rows` `[{host_mutation, "pacman -S r22-cxafterdef-live", observed}]`. `unparsed` 0. Matches `want` exactly.
- Scanner child (one): exit 1, label `findings`, unpermitted 1 (expected for an unpermitted `host_mutation`). Payload: `eval_calls` 1, `eval_unparsed` 0, `unparsed_spawns` 0, `observed_findings` 1, `lead_findings` 0. Finding rule `pacman:-S`, argv0 `pacman`, line 1, `tool_call_id` `CXReturnAfterDef-0`, `timestamp` `"None"` (see §8E).
- Integrity before and after the run, identical. Tool `36fdc459…`, runner `41b021bb…`, expected `b5cd4cf3…`, expected pin file `7cc4aae9…`, assembler `0270c10b…`, truth seal `47f403f6…`, population `04616857…`. Verified: 57 inputs, 52 proposals, 106 sealed sources.

Receipts at `.ufo/waves/round-22/w2/receipts/FalsifyC116/`:
- `result.json`: argv, exit, stderr, stdout embedded, and all tool, fixture, runner, and expected hashes.
- `stdout.json`, `stderr.txt` (empty), `exit.txt` (`0`).
- `hashes-before.sha256` and `hashes-after.sha256`, identical for the tool, runner, expected, assembler, and fixture.
- `manifest.sha256`.

## 5. Falsification attempts (this case)

| class | attack | outcome | basis |
|---|---|---|---|
| false observed argv | dead `-Q` appears as observed | not reproduced | No `-Q` row in output. Static: factory prefix is `owner.body[:index(first top-level Return)]` (1649, 1663). `prepare_eval_calls` breaks at the Return (2252-2253). |
| false lead argv | dead def swept as lead via `sweep_body` or refs | not reproduced | Static: `follow_helper(make)` returns `([],0)`, which is non-None, so no sweep (2575-2577). `sweep_body` uses the same break at 2378 → 2252. `return run` is not a ref. |
| lost true command | live argv dropped or redacted | not reproduced | `command = redact("pacman -S r22-cxafterdef-live")` (2892). Redaction needs a run of at least 32 `[A-Za-z0-9_-]` (304). The token is 19 characters. `MAX_COMMAND` is 240. |
| wrong identity | last same-named def chosen | not reproduced | `factory_result` binds only the prefix, so `run` = A. `closure_bindings` maps run → A (1663-1683). |
| lifetime | post-return binding applied | not reproduced | Statements after the first top-level Return are excluded (1663; 2252-2253). |
| conditional target | branch-dependent target | not applicable | No conditional in the text. |
| parsed-clean ambiguity | findings suppressed, or clean with unparsed > 0 | not reproduced | `eval_unparsed` 0, `unparsed_spawns` 0, observed 1. Runner exact mode requires `unparsed` == 0 and scanner exit ∈ {0,1} (measure 687-688, 752-756). |
| oracle weakening | exact check bypassed | not reproduced | Exact path: `matched = actual == expected and unparsed == 0` (753). `accept_exact_want` is illegal for exact kinds (272-275). |

## 6. Exact vs `accept_exact_want` vs true uncertainty (for this case)

- **Exact (this case):** pass iff the sorted `(class, command, evidence)` multiset is equal and `unparsed` == 0 (753). No alternate rows and no signal-based pass exist.
- **`accept_exact_want`:** legal only for uncertain kinds (validate 272-279). Not used here.
- **True uncertainty (uncertain kinds):** pass if the complete accept multiset matches with zero unparsed (758-760). Otherwise the case requires no observed rows (761-764), `require_signal` (765-767), and any required leads (768-777).
- **Gap if this text were ever re-registered as uncertain:** a lead-only dead-command row would pass. Forbids are checked against observed rows only for `forbid_observed_commands` (742-746), and the uncertain branch then accepts the lead as its signal. Not a defect in this exact case. It becomes one if the case is converted to uncertain without `pacman -Q r22-cxafterdef-dead` in `forbid_commands_any_tier`.

## 7. Scope against the current target, and discrimination power

- Target: `tools/mado-tripwire.py` sha256 `36fdc459…`, the pinned C1 identity. The delivered revision `71228fd5…` is the one named in the assignment. I did not verify it because I did not use git.
- Applies to: this text under these tool bytes. This is not a population result, since one of 57 cases was executed. It is not a shipped-CLI result, see §8B.
- Power: this case rejects (a) the pre-repair last-def-over-all identity and (b) dead-def leads or silent outcomes. It does not reject a first-def-name index, since that also returns the live def. The rival is covered by the sealed supplemental original `OriginalF3ReturnedRebound` (exact; want `host_mutation pacman -S r21-b`; source `def a: -Q r21-a; def b: -S r21-b; a = b; return a; make()()`). A first-def index returns `a` and fails F3. The prior after-receipt passes F3 with the current bytes (§7 receipts below).
- Prior receipts (read only, not rerun, not independently validated beyond reading):
  - `evidence/first/oracle-before-new50.json` ran `evidence/tool-before.py` (`46c82902…`). Its CXReturnAfterDef row is `package_query pacman -Q r22-cxafterdef-dead`, observed, `pass` false. This matches the static read of `tool-before.py` 1646-1652.
  - `evidence/first/oracle-after-all57.json` ran `tools/mado-tripwire.py` (`36fdc459…`). It records 57/57 pass, including this case with `host_mutation pacman -S r22-cxafterdef-live` observed, and F3 passing.

## 8. Adjacent observations (outside this case; reported, not normalized)

A. **Receipt drift.** `evidence/first/oracle-before-new50.json` has top-level `selected_tool_sha256` = `36fdc459…`. Its argv names `…/evidence/tool-before.py`, and its inner stdout has `tool_path` = tool-before.py and `tool_sha256_before` = `46c82902…`. The inner stdout is the authoritative identity. The top-level field is wrong and must not be cited as showing that the red came from the current tool.

B. **Harness path divergence [static].** The runner's child calls `m.main(["--scan", path])` after `exec_module` (measure 34-38). This bypasses the module's `__main__` guard. It skips `run_with_stack`, which uses a 64 MiB thread and recursion limit 50000 (tool 3420-3445), and the internal-error envelope (3448-3463). Oracle verdicts therefore describe `main()` on the default thread and recursion limit, not the shipped CLI entry. No difference is expected for this shallow case [INFERENCE]. Deep-nesting cases could differ, and the failure mode would be loud (no JSON, so a fail), not a false pass.

C. **Possible silent path for unresolved factories [INFERENCE: static trace, not probed; no probe was assigned].** `factory_result` returns `{"kind":"unresolved"}` when no top-level Return exists (tool 1649-1651). One example is a `return` nested under `if`. For a Call-shaped callee (`make()()`), the unresolved branch (2606-2614) emits leads only for Name or Attribute callees and otherwise `continue`s. For `f = make(); f()`, only literal-argv arguments are led. The result is zero rows and zero unparsed, so the verdict is clean if nothing else is found. `supported-forms.md` line 18 says conditional or non-Name returns cannot be certified safe by absence of a finding, and their outcomes must remain parse, error, or lead uncertainty. This is a candidate parsed-clean ambiguity for a different case. It needs its own assigned bounded probe to confirm.

D. **Verdict label ignores counters.** `verdict_of` (2909-2914) labels `clean` from findings alone, so `eval_unparsed` or `unparsed_spawns` > 0 can still print `clean`. The module header documents this as a limit. The runner's exact mode compensates. Awareness only.

E. **Cosmetic.** A finding whose record has no timestamp serializes `"timestamp": "None"` (2890).

## 9. Exercised vs read

- **Exercised:** one `measure.py --case CXReturnAfterDef` invocation (one scanner child; runner caps 384 MiB and 15 s). SHA-256 of tool, fixture, runner, expected, assembler, pin, and truth seal, before and after. `sha256sum -c expected.sha256` run from the oracle directory, which returned OK.
- **Read only:** the tool, `measure.py`, the expected entry, the proposal, the fixture, the wave docs (`registration.md`, `supported-forms.md`, `guard-clarifications.md`), the two CPython doc lines, the frozen pre-repair tool lines 1636-1665, the prior receipts (by query), `returned-rebound.jsonl`, and a grep of fixture cells.
- **Not run:** no other scanner, no fixture code (the scanner parses with `ast` only), no pre-repair tool, no full 57-case run, no builds, tests, lints, or probes, no git.

## 10. Accounting

- **Writes:** this report, and `receipts/FalsifyC116/` (`hashes-before.sha256`, `stdout.json`, `stderr.txt`, `exit.txt`, `hashes-after.sha256`, `result.json`, `manifest.sha256`). No edits to tools, fixtures, proposals, gates, registries, docs, expected, or sources.
- **Installs or updates:** none, and none needed. `RULES.md` was not consulted because no install channel was used. No pacman, package queries, services, network, or live probes.
- **Delegation:** none (leaf member).

Report: .ufo/waves/round-22/w2/reports/FalsifyC116.md
Absolute: /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/w2/reports/FalsifyC116.md
