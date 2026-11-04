# R69RevC2 — adversarial C2 review

Verdict recommendation: **unsound** (bounded predicate violations, not merely arbitrary-Python limits).
Axes: calibration C1; operability C2. This seat reviews C2 only; no production edits, integration, admission or runtime-routing changes.

## Reviewed identities

- Declaration read first, frozen claim C2 lines 89–158; base `04093b83f73a841117d3b31dbb2a6063f4f2a454`.
- Prototype `.ufo/waves/round-69/proto/c2-classify.proto.py`: SHA256 `0a1e1ff609ef562e3ffe3c0566e1bb20e2466b1ba70c7498750d36e6e0f47803`.
- Frozen controls SHA256 independently matched `975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9`.
- Executor draft directory existed but contained no counter when inspected. A concurrently present production candidate was reviewed read-only: `quality/counters/c2-r69-guard-dominance.py`, SHA256 `b6bcec07ffe1849f9ef9a3c1a1e25d94743be6e01e9cae4219ea8045996b673a`. Findings apply to these exact bytes, not later revisions.
- LSP unavailable: reading `xd://lsp` returned `No such tool`. References/definition/diagnostics could not run. Evidence below is direct AST/function execution and source inspection, not semantic grep proof.

## Findings by severity

### High — dead inline construction is accepted

Candidate lines 353–364 (`inline_guarded_call`) walks all calls without excluding dead lines; `has_guard` at 380–381 accepts its result before the guarded-name checks. `dead-inline` is `(True, True)` despite its sole guarded call being inside `if False:`. Explicitly violates declaration 107. Prototype lines 253–266 has the same defect. Exclude dead construction/launch nodes in every path, including inline and producer-return paths.

### High — producer does not return the guard it is credited with

Candidate lines 266–299 collect any guarded local name then accept any return of that spelling, without checking rebinding or ordering. Both `producer-overwrite` (env becomes `{}` before return) and `producer-late` (guard occurs after unconditional return) are `(True, True)`. These are local producer flows inside the stated boundary; they do not return a guarded mapping as required by declaration 103–105. Prototype lines 165–197 agrees. Require guard-before-return and no intervening unguarded binding.

### High — key-position test descends into values

Candidate lines 167–180 use `ast.walk` over an entire mapping value. `nested-key-value`, with `env = {"LABEL": {"GIT_NO_REPLACE_OBJECTS": "1"}}`, is `(True, True)`. The actual environment has only key LABEL; this violates key-position requirement 96–99. Prototype lines 60–73 agrees. Recognize actual mapping keys and supported dictionary expansion, not arbitrary descendant dicts/calls.

### High — same spelling is mistaken for the same flowing environment

Candidate `function_scopes` 202–206, `guarded_names` 302–334 and `usage_lines` 239–262 descend across lexical scopes. `sibling-scope` puts a guard only in uncalled `never()` and uses an unresolved env in separate `run()`; result `(True, True)`. This violates one-module actual-flow rule, not its no-cross-module limitation. Additionally `onehop-wrong-parameter` passes guarded `env` to first parameter while callee launches with unguarded second parameter `other_env`; result `(True, True)`. `callee_passes_env_to_git` 226–235 proves only that some env-named parameter is used; it never matches the caller argument to that parameter. Bind names by lexical identity and match argument position/keyword to the specific parameter. Prototype has both defects.

### Medium — live else branch rejected

`false_guarded_lines` candidate 187–199 marks the entire `if False` AST, including its live else. `dead-else-valid` is `(True, False)` despite constructing the guard in the only executed arm. Prototype 80–93 agrees. Mark false body only, not else.

### Medium — symbolic KEY spelling has undisclosed restriction

Supplementary `constant-key-subscript` and `constant-key-splat` return `(True, False)` when `KEY="GIT_NO_REPLACE_OBJECTS"`. Literal-string equivalents are accepted. Declaration says `env[KEY]` and does not explicitly exclude local constant-key resolution. These are false negatives against that reading; at minimum the report must disclose literal-key-only support without changing the frozen predicate. Attribute variant remains expressly outside supported flow.

## New attack cases

Exact complete source for every case and observed verdict is retained in `w1/R69RevC2/prototype-attacks.txt` and `w1/R69RevC2/candidate-attacks.txt`; named-case construction is executable in `w1/R69RevC2/attacks.py`. Both reviewed classifiers produce the same table. T/F columns are reader/guard.

| Case | Verdict | Assessment against stated bounds |
|---|---|---|
| filtered-conditional | T/T | Bounded TP; runtime FP possible when enabled false, expressly excluded path sensitivity. Filter `k != "GIT_"` does not strip prefixed keys. |
| attribute-env | T/F | Runtime FN, excluded attribute flow; not a bounded defect. |
| alias-env | T/F | Runtime FN, excluded alias flow; not a bounded defect. |
| late-guard | T/F | Correct negative: guard follows launch. |
| except-other-env | T/F | Correct negative: except rebinds to unguarded env; conservative lexical rebinding handles this particular case. |
| closure-env | T/T | TP for this actual closure; does not establish general closure correctness. |
| splat-env | T/T | TP with literal KEY string in expanded mapping. |
| cross-module | T/F | Runtime FN, expressly excluded cross-module producer. Exact second-module source is logged too. |
| dead-inline | T/T | Bounded FP, high finding. |
| producer-overwrite | T/T | Bounded FP, high finding. |
| producer-late | T/T | Bounded FP, high finding. |
| sibling-scope | T/T | Bounded FP, high finding. |
| nested-key-value | T/T | Bounded FP, high finding. |
| onehop-wrong-parameter | T/T | Bounded FP, high finding. |
| dead-else-valid | T/F | Bounded FN, medium finding. |
| producer-direct | T/T | TP. |

Literal-name `KEY` variants and exact source are additionally logged in `w1/R69RevC2/denominators.txt`: subscript T/F, splat T/F, attribute T/F. Thus both literal strings and requested symbolic spellings were exercised.

## Base population — all 20 files

Measured using `git -C <absolute-lane> ls-tree -r --name-only <base> -- quality`, exact declaration regexp, then `git -C <absolute-lane> show <base>:<path>` for each classifier input. Reproduction driver runs these read-only commands explicitly; no git mutation.

| quality file | Reader | Guard | Fragility (ablation-confirmed) |
|---|---|---|---|
| check-anchor-cover.py | yes | yes | one-hop only |
| check-axis-scores.py | yes | yes | neither required |
| check-control-receipts.py | yes | yes | neither required |
| check-counter-discrimination.py | no | no | — |
| check-deliverables.py | yes | yes | neither required |
| check-evidence-pointers.py | yes | yes | neither required |
| check-freeze-order.py | yes | yes | producer only |
| check-index-rows.py | yes | yes | neither required |
| check-index.py | yes | yes | neither required |
| check-landed-contract.py | yes | yes | neither required |
| check-locators.py | no | no | — |
| check-population.py | no | no | — |
| check-r38-discrimination.py | no | no | — |
| check-r55-controls.py | no | no | — |
| check-r56-controls.py | no | no | — |
| check-round-outcome-first.py | yes | yes | neither required |
| check-session-material.py | yes | yes | neither required |
| check-state-cite.py | no | no | — |
| check-tool-ledger.py | yes | yes | producer only |
| check-wave-done.py | yes | yes | producer only |

Total **20 population / 13 readers / 13 guarded / 0 unguarded**, independently reproduced for prototype and candidate. Ablation replaces only `callee_passes_env_to_git` or `guard_producers` with a false/empty result in a separate in-memory namespace; it does not mutate files.

Fragile flow source evidence at base:
- `quality/check-anchor-cover.py:102–106` constructs env and passes it to git_blob; launch `:22–23` uses env parameter. Removing that handoff, renaming parameter away from env, or introducing another intermediary breaks the bounded one-hop acceptance.
- `quality/check-freeze-order.py:44–53` returns guarded env, `:57–61` passes producer result to launch.
- `quality/check-tool-ledger.py:101–111` returns guarded env; `:116` and `:127–128` use producer inline.
- `quality/check-wave-done.py:179–190` returns guarded env; `:195` uses producer inline.
Producer flows break if moved to another module or routed through aliases; changing to a non-env-named return local can also break the approximation. Actual removal/overwrite of the guard should break acceptance but currently may not (high finding).

Behaviour identity: **no production change to any gate is required** to satisfy the frozen dominance census; every base reader already passes. Do not repair the gates merely to accommodate this counter. This is discrimination improvement, not 12→13 reader-coverage improvement; the base is already 13/13.

## Frozen rejected controls / red state

Executed against r68 classifier extracted from base and both reviewed classifiers:

| Frozen case | r68 | Prototype/candidate |
|---|---|---|
| value-position-only | T/T | T/F |
| dead-branch-only | T/T | T/F |
| uncalled-helper | T/T | T/F |
| overwritten-env | T/T | T/F |

All eleven outcomes are logged. Baseline receipt lines 33–46 records **r68 7/11 TARGET_MISSED**, prototype 11/11. Reproduction agrees. Passing these eleven does not rebut the bounded counterexamples above.

## Denominator/verdict attacks

Executed `load_controls`, `verdict_met`, and `contract_line` directly (no fabricated revision measurements). Candidate 416–431 rejects both truncated ten-case JSON and an eleven-case renamed JSON on SHA mismatch. Required assertions: exact SHA and case count 11; population==20; readers==13; guarded==13; unguarded==0; candidate controls==11; base_controls==7. Candidate 410–413 contains all of these; no missing denominator assertion found.

Observed: canonical synthetic tuple => TARGET_MET; base_controls=11 => TARGET_MISSED; population=19 => TARGET_MISSED; controls=10 => TARGET_MISSED. No truncated/renamed control can reach the score through `measure`: it invokes `load_controls` at 508 first. Population identities are selected by the frozen regexp at REV, not by this seat's own subset.

Prototype is classifier feasibility evidence only: it has no frozen-control loader or TARGET_MET contract. Its omission is not mistaken for a production verdict vulnerability.

## Exact reproduction commands and exits

All commands executed from inherited fleet cwd but use absolute paths; driver writes only its authorized scratch and removes it in finally.

```
mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-69/w1/R69RevC2 /fast/scratch/hyaku/mado-r69/R69RevC2
# rc 0
python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-69/w1/R69RevC2/attacks.py
# rc 0; prototype-attacks.txt
python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-69/w1/R69RevC2/attacks.py /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r69-guard-dominance.py
# rc 0; candidate-attacks.txt
python3 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-69/w1/R69RevC2/denominators.py
# rc 0; denominators.txt
```

These commands reproduce every named case; each log includes exact source adjacent to its verdict. The cross-module case feeds the consumer only, correctly reflecting the declared single-module boundary; producer source is recorded but never imported/executed.

## Residual limits / verification gaps

Even after fixes: single module, one hop, no general alias/attribute/container flow, only literal-false path handling, guard value uninterpreted, file-level existential acceptance rather than every launch guarded, lexical reader detection, fixed 20-file population not whole-lane reader completeness. Do not claim runtime effective environment safety, universal Python soundness, whole-axis saturation or additional reader-count progress. No resume-continuity or runtime-rerouting change is in this assigned diff. No desktop probe, package install, screenshot, fixture commit or production write occurred.

No full CLI measurement at a newly committed candidate revision was performed; this seat evaluated pure classifier/verdict boundaries and base census. No final executor draft hash was available during review. Exact attacked candidate hash is above. Any subsequent counter change needs these cases rerun by the main agent.

Scratch `/fast/scratch/hyaku/mado-r69/R69RevC2` **removed**, both drivers print `SCRATCH_REMOVED True`; final existence check returned false. Tool installs: none. Production drafts: none; this is an attack/review seat.

Artifacts SHA256 (all under absolute seat directory given in commands):
- attacks.py `8e7bf3e738d36863bda4bae55311d08703412737e2a8366b2daccc664d296d7b`
- prototype-attacks.txt `a62d5baf64e649d75d56a08b9e00bbb2e96456a72e33c862d9e50cdabc5d3b8c`
- candidate-attacks.txt `1e0a4c53529e771592b1b5932f8e06040b46161d2ae3f4cc3a040d0d057c00b0`
- denominators.py `b9fe045da3d5e2c66680bd4214ee6533d42204e991fc4be0ebef1d2a60acfb1a`
- denominators.txt `2b2daa095c7614e32474dcf730e67960c5849bb0424bb653b178916f2365bfbc`

Self-evaluation: accuracy 4 (symbolic KEY interpretation explicitly qualified); completeness 4 (no final draft available); clarity 4 (source retained in linked logs); actionability 5 (named cases, lines, executable repro); conciseness 4 (full population required). Mean 4.2. Main action: fix bounded false positives without changing frozen targets, then rerun the exact review drivers against integrated bytes.

## Addendum — distinct executor draft now available

The executor subsequently supplied its own draft at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-69/w1/R69ExecDominance/draft/quality/counters/c2-r69-guard-dominance.py`, SHA256 `157104c841127ba6203b963b857c7c40484fefabf948f6832533305f72d877b1`. It is **not** the production-path candidate reviewed above; no attribution of that candidate to this executor is intended.

Independent in-memory execution confirms this draft fixes the original six false-positive shapes and the live-else false negative. All 16 original shapes were rerun; outcomes retained in `w1/R69RevC2/executor-draft-attacks.txt`. The previous findings remain historical evidence against their exact hashes, not claims that this draft retains those exact defects.

Nevertheless, verdict for this exact executor draft remains **unsound**, with three newly reproduced high-severity bounded false positives:

1. **Chained overwrite bypasses rebinding detection**, draft lines 328–345. `rebindings` ignores `ast.Assign` unless it has one target; `env=other={}` therefore fails to invalidate the earlier guard. Declaration 103–105 explicitly disallows intervening unguarded rebinding.
2. **One-hop callee overwrites its env parameter**, draft lines 387–402. Parameter use is credited without checking an assignment `env={}` before the process launch. Matching argument position alone does not establish the guarded mapping reaches that call.
3. **Unreachable guarded producer return is credited**, draft lines 363–383. An unconditional `return env` returning an empty mapping is followed by an unreachable `return {KEYliteral: "1"}`; the latter alone marks the function as a producer. It never returns a guarded mapping. This is straight-line reachability within the supported producer flow, not arbitrary conditional path sensitivity.

Exact additional sources and observed outcomes, each `(True, True)`:

```python
# chained-overwrite
env={"GIT_NO_REPLACE_OBJECTS":"1"}
env=other={}
subprocess.run(["git","show"],env=env)
```

```python
# onehop-param-overwrite
def launch(env):
    env={}
    subprocess.run(["git","show"],env=env)
env={"GIT_NO_REPLACE_OBJECTS":"1"}
launch(env)
```

```python
# dead-producer-return
def git_env():
    env={}
    return env
    return {"GIT_NO_REPLACE_OBJECTS":"1"}
env=git_env()
subprocess.run(["git","show"],env=env)
```

Reproduction: load the exact draft using `ns={"__name__":"review_import"}; exec(compile(path.read_bytes(),str(path),"exec"),ns)` and call `ns["classify"](src)` on each source above; no Python source is executed as an application. Observed tool cell rc 0. Exact outcomes are also retained in `w1/R69RevC2/executor-draft-extra.txt`. The bounded predicate requires rejection of all three without narrowing the frozen declaration. Symbolic-key limitation remains disclosed, but the verdict does not depend on its interpretation.

Draft source inspection confirms its `load_controls` at 558–586 checks frozen SHA, exact count and field types, and `verdict_met` at 617–623 requires exact target counts including denominator 11 and base 7. No denominator omission was found in this distinct draft. Base population evidence above remains the prototype/candidate measurement, not an unperformed independent census of this executor draft. Executor-reported full CLI/selftest success is not promoted to this seat's own exercised evidence.

Scratch remains absent: these additional attacks created no scratch files. Main should rerun original and additional exact cases against the eventual integrated identity.

## Final addendum — revised executor identity

Latest distinct executor draft SHA256 `782b95aa0da0dd263baa2953944478dcce8e90d53c78a98ab887ffb48a7a333c` was independently loaded and all 19 original/additional source shapes rerun (tool cell rc 0). Outcomes: all six original bounded false positives and all three later false positives now return `(True, False)`; live-else returns `(True, True)`; valid producer-direct, closure and literal splat remain `(True, True)`. Full outcome table: `w1/R69RevC2/executor-draft-final-attacks.txt`. The original exact source blocks and reproduction method above remain applicable.

**Latest verdict recommendation: C2 predicate sound as bounded for this revised executor identity and exercised attack set**, with the declared literal-key spelling restriction and other residual limits disclosed above. This supersedes the unsound verdict only for this exact revised identity; it does not certify the concurrently different production-path artifact or universal Python soundness. No actionable reproduced finding remains against these revised bytes in the reviewed cases. Main must measure the integrated identity and confirm its frozen population/control verdict; the executor's reported full CLI results are not this seat's independent measurement. Scratch remains absent; no production writes or installs.
