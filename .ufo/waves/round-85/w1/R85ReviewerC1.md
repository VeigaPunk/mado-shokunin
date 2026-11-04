# R85ReviewerC1 — frozen C1 falsification

Axes: coverage/discrimination, reproducibility, non-interference. Recommendation only; no admission or integration.

## Findings, by severity

### Medium — negative-allocation cause is not measured

The declaration names ten cause tokens, including `alloc-negative`, but the frozen population binds only nine distinct tokens. Its carried `alloc-negative-refused` case supplies `{"waybar": -4}` and expects only `{error:true, rc:2, stage:"setup"}`; there is no `expect.cause`. Evidence: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/controls/c1-cases-r85.json:2744-2757`. `/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r85-identity-causes.py:304-320` checks a cause only if declared.

Measured wrong-reason tool: replace only

```python
raise Setup("the allocation for %r is negative" % name, "alloc-negative")
```

with

```python
raise Setup("the allocation for %r is negative" % name, "alloc-not-object")
```

The real frozen `run_cases`/`expected_ok` path scores this tool **72/72**, zero failing cases. The direct CLI for `alloc-negative-refused` returns 2 and prints:

```text
MADO_BARFOOT: ERROR (stage=setup cause=alloc-not-object the allocation for 'waybar' is negative)
```

This answers the wrong-reason question affirmatively without multi-token tricks. This was a case-score attack, not a complete target-admission run: the source change breaks the negative-allocation mutant's literal anchor and its own cause selftest. Do not claim it passes the full gate. Scratch variant SHA256: `9f28699ea7e5cacbb3f2fe8e18251357da9977602c49262b5ee15d1c7cdaf28f`.

Recommendation: explicitly delimit the claim to cause-bound witnesses, or add an immutable successor expectation and a wrong-negative-cause mutation. Do not silently alter the carried population.

### Low — cause presence is not unique, nor bound to the error record

`/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r85-identity-causes.py:310-318` independently searches all stdout for the stage fragment and `" cause=<expected> "`. It never requires exactly one cause on the same error line.

A scratch tool preserving all original refusal decisions but flooding every cause-bearing CLI error with `cause=wrong-reason` plus all nine cause-bound tokens scores **72/72**. Example for `alloc-dup-key-equal`, rc 2:

```text
MADO_BARFOOT: ERROR (stage=setup cause=wrong-reason cause=alloc-duplicate-key cause=alloc-empty-namespace cause=alloc-non-integer cause=alloc-not-object cause=alloc-unknown-namespace cause=live-duplicate-surface cause=namespace-duplicate-bar cause=namespace-duplicate-cross-level cause=namespace-duplicate-surface the allocation declaration repeats namespace 'waybar')
```

Reproduction transformation: after `if args.selftest: return selftest()` in `main`, retain `original_cause_tag = cause_tag`; wrap it so an empty original tag stays empty, otherwise return the fixed string above's cause list. All original mutant anchors remain intact. CLI-only installation leaves `--selftest` unchanged. Measured: tool selftest **152/152**, candidate **72/72**, but only **48/51** mutants die. Survivors: `alloc-dup-cause-collapsed`, `ns-dup-cause-collapsed`, `ns-dup-level-blind`, each **72/72**. Thus this survives the case score, **not** the complete gate. Variant SHA256: `49654d739a491b10643f3018f4ac0f93927e328224368743123b650836eff23c`.

Recommendation: parse one canonical error record and require its unique cause token to equal the expectation. The existing mutant clause already catches this demonstrated flood when the full gate is exercised.

## Four requested CHEATS

Counter copies and tool submissions were created only in the seat scratch. For (b)/(c), casefolding namespace identity and accepting duplicate declarations are tool behaviors, so these were submitted to the unmodified frozen scorer rather than silently rewriting expectations.

| Cheat | Case score | Complete gate / discrimination result |
|---|---:|---|
| (a) Counter ignores `expect.cause` (`if False` replaces the cause rejection condition) | 72/72 | **TARGET_MISSED**, rc 1; killed **47/51**, base **72/72**, carried 61/61, selftest 152/152 |
| (b) Tool casefolds namespace identity before comparison | 71/72 | Rejected by `ns-case-distinct-accepted`. Tested both the declared `ns-case-folded` mutation and a consistent implementation that casefolds the initial bar key and every extra key; both fail precisely that case. |
| (c) Tool accepts equal-valued duplicate allocation keys (`if key in out and out[key] != value`) | 71/72 | Rejected by `alloc-dup-key-equal`. |
| (d) Counter accepts any cause token (`re.search(r" cause=\S+ ", stdout)` instead of expected-token search) | 72/72 | **TARGET_MISSED**, rc 1; killed **48/51**, base **62/72**, carried 61/61, selftest 152/152 |

(a) survivors: `alloc-dup-cause-collapsed`, `cause-dropped`, `ns-dup-cause-collapsed`, `ns-dup-level-blind`, all 72/72. (d) survivors: the same except `cause-dropped`. Hence neither weakened counter meets the full declared target despite candidate scores of 72/72.

Additional single-token control: change duplicate-key cause to `alloc-non-integer` using the declared `alloc-dup-cause-collapsed` mutation. The real scorer returns **70/72**, failing exactly `alloc-dup-key-equal` and `alloc-dup-key-interleaved`. It does discriminate specific single causes for the cause-bound witnesses.

## Real measured path

All source/control/counter copies were extracted with read-only `git show` at freeze `3905311c75a39c5710413105865c0a1a7dd0116a`; base was `5f174ca48d4f9cf94abf1a8c58b7d6f88733aced`. The unmodified frozen counter was invoked with the declared flags, absolute repo/control/carried/scratch paths, and no `--no-mutants`.

```text
MADO_R85_IDENTITY: cases=72 correct=72 mutants=51 killed=51 base_correct=62/72 carried=61/61 tool_selftest=152/152 verdict=TARGET_MET rev=3905311c75a39c5710413105865c0a1a7dd0116a tool_sha256=d2eb4547b2e285fb80415e81b70c05e47aa6184eadb863e3cd72dab43e6bfd12
```

Exit 0. Counter SHA256: `ab2306ac59f8744a51ff0d4bc4d719fc669fce03c7fe4d877872efad90d9ae9c`; controls SHA256: `bacae37d29d06e4f9d623262c05f2975bcba338e650dbd38cbbd4039ca6216a1`.

**C1's precise numerical frozen predicate verifies.** It does not establish correct cause discrimination for all ten vocabulary entries or make 72/72 alone sufficient. No demonstrated attack passed the complete gate.

## CLI reachability and accept-case authenticity

**`live-dup-surface` is reachable through the real file-input CLI**, not just an imported function. Materialized the frozen witness with the counter's actual `case_files`, then invoked frozen tool `--config <absolute> --layers <absolute> --monitors <absolute>`. It returned 3:

```text
MADO_BARFOOT: ERROR (stage=model cause=live-duplicate-surface more than one 'waybar' layer on monitor M1 level 2)
```

Canonical path: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py:1693-1715` parses capture and calls `evaluate`; `find_layer` at lines 998-1009 counts exact-namespace entries at the requested level and raises when more than one. No production compositor IPC run was performed.

**`ns-case-distinct-accepted` is a genuine accept case.** Direct CLI returned 0 with `surfaces=2`, separate `ns=waybar contribution=26` and `ns=Waybar contribution=40` attribution records, and:

```text
MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=66 expected=66 attributed=66 gt=0,66,0,0 attr=0,66,0,0 ls=VALID verdict=CLEAN
```

The consistent casefold tool fails exactly this witness. To remove the level difference as a confound, moved `Waybar` declaration/live entry from level 3 to level 2, preserving geometry; the real tool still returned CLEAN, rc 0, score 1/1, band/expected 66. Exact-string identity is deliberate in `evaluate_composition` lines 801-820 and `find_layer` line 1005, not an accidental differing-level acceptance. The frozen accept expectation does not bind `attr_ns`; the direct output supplies independent evidence of the two identities.

## Residual risk and verification gaps

- No `lsp` device is mounted (`xd://lsp` returned “No such tool”). Caller/definition review used source/diff and executable probes, not semantic reference proof; no LSP diagnostics available.
- Reviewed actual frozen tool diff against base. No alternate runtime, resume path, saturation admission, or rerouting implementation is changed by this C1 tool diff; no claims about those systems are inferred.
- Scratch tool score attacks used the frozen scorer's `run_cases`, not fabricated revisions or a replacement canonical runtime. Complete frozen/cheat-counter runs used its actual `main` extraction/mutation path. No fixture git mutation was needed.
- No tracked declaration, tool, counter, controls, or sibling-owned file was edited. No installs or git mutations. Only this report persists; seat scratch is removed before yielding.
- Self-evaluation: accuracy 4/5 (full gate and case-only attacks explicitly separated); completeness 4/5 (no live compositor capture); clarity 4/5 (counter-vs-tool cheat interpretation explicit); actionability 4/5 (exact matching gaps and replacements provided); conciseness 4/5 (preserved necessary reproduction/evidence). Overall 4.0. Most useful next action is a scoped successor negative-cause witness, not a broader claim from the current totals.
