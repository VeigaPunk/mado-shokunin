# R84ReviewerC1 — frozen C1 review

Axes: coverage, carried-outcome preservation, refusal-stage integrity. Recommendation only; no admission or integration action.

Reviewed frozen `3f9eec3906ddd1492e8bc08325e83064f00111ea` against base `7fd43921294116299dfce1443d56a951b9c81493`. Production and frozen controls were not edited. All executions used extracted revision bytes and synthetic offline fixtures in this seat's scratch. No live compositor reads, other runtime routing, credential material, screenshots, git/jj mutations, tool installations, or host-service changes.

## Findings by severity

### Medium — three anchor-preserving cheats satisfy every exercised C1 clause

`quality/counters/c1-r84-namespaces.py:163-168,278-297,499-533` scores a finite case set and two blanket identity-guard mutations. The three new controls exercise two same-level extra declarations, a bar/extra collision, and two adjacent allocation keys with differing values. They do not distinguish the following incorrect implementations. Each scratch candidate preserved **all 41 mutation anchors exactly once**, scored **61/61**, passed tool selftest **139/139 (rc0)**, and killed **41/41 canonical mutants**. Shared baseline and carried-equality clauses were independently exercised by the canonical run below. Thus this is not an absent-anchor shortcut. The scratch candidate full mutation loops were invoked through the frozen counter's `apply_mutation`, `run_cases`, and `run` functions; they were not represented as git revisions or as literal `main()` TARGET_MET runs.

1. **Equal-valued duplicates silently collapse.** At `tools/mado-barfoot.py:443`, insert before the existing guard:
   ```python
   if key in out and out[key] == value:
       continue
   ```
   Leave the existing `if key in out:` block intact. Allocation entries `panel=40, panel=40` then return rc0/CLEAN, rather than the frozen production tool's rc2/setup. The frozen differing-value duplicate and enumerated guard-removal mutant still detect their own narrower cases.
2. **Nonadjacent duplicates silently collapse.** Before that same unchanged guard insert:
   ```python
   if key in out and key != next(reversed(out)):
       del out[key]
   ```
   Allocation entries in order `panel=24, waybar=26, panel=40` return rc0/CLEAN instead of rc2/setup. The allocation names are declared, so this witness is not masked by an unknown-name refusal.
3. **Extra declaration identity incorrectly includes level.** Immediately before the unchanged guard at `tools/mado-barfoot.py:783`, replace the working names list through a second assignment:
   ```python
   names = [bar["namespace"]] + [s["namespace"] if s["namespace"] == bar["namespace"] else (s["namespace"], s["level"]) for s in extras]
   ```
   Starting with frozen `duplicate-extra-namespaces`, change only the first extra's level from 3 to 1. Frozen production returns rc2/setup. This candidate reaches prediction and returns rc1/DIFFER, not any setup refusal. A geometric mismatch is not an acceptable replacement for declaration rejection. The candidate still rejects same-level extras and bar collisions, so all frozen checks and tool selftests pass.

Consequence: the declared 41/41 population is honestly killed, but cannot establish general rejection of the named declaration classes beyond its witnesses. Preserve the freeze and report this as a coverage limitation; a later predicate can separately cover equal-valued, interleaved, escaped-key and cross-level witnesses. No score alteration is recommended for this frozen wave solely because additional mutants survive.

### Medium — invalid-type inputs escape refusal handling (pre-existing, not r84 regressions)

`tools/mado-barfoot.py:683` tests anchor members against a dict before requiring strings; `anchor=[{}]` raises TypeError. At `:693`, `exclusiveEdge=[]` likewise raises TypeError. `parse_layers` at `:932-936` accepts any monitor value; `find_layer` at `:965` calls `.get` on it, so a monitor value that is an array raises AttributeError. The CLI catches only Setup and Unmodelled (`:1633-1638`); all three witnesses exit **rc1 with a traceback**, no refusal stage and no RESULT. rc1 is also the normal DIFFER exit, so callers cannot rely on the documented structured refusal path for these malformed inputs.

These three outcomes were reproduced against both frozen tool and held base. They are carried production limitations, not caused by the new guards. Direct allocation null/bool/float/string/object/array values instead correctly returned rc2/setup.

### Low — counter header describes obsolete contract

`quality/counters/c1-r84-namespaces.py:4-18` still describes 47 carried cases, eight later cases, 58 cases, 38 mutants and baseline 52/58; executable constants at `:35-38` and actual output are 61/41/58/58. The executable predicate is consistent with the claims declaration, but this header is misleading audit documentation.

## Actual canonical receipt / carried outcomes

Executed the exact counting command from the claims declaration, substituting the frozen revision, base, absolute repo/control paths and seat-local scratch root; counter script itself was extracted from the frozen revision. Observed completion rc0, 81.90 seconds:

```text
MADO_R84_BASE: correct=58/61
MADO_R84_CONTROL: sha256=5c9ce3891e1ec4be1820d229bbcfddfa5b61cfbd0d02cc93252ac38c6dd9e883 carried=58/58
MADO_R84_BARFOOT: cases=61 correct=61 mutants=41 killed=41 base_correct=58/61 carried=58/58 tool_selftest=139/139 verdict=TARGET_MET rev=3f9eec3906ddd1492e8bc08325e83064f00111ea tool_sha256=72456666a31927dfc46f955f41b3aa57b2215a8fcd8dc736fc302d7b58830c7f
```

All first 58 cases scored correct, including NO_BAR, model/setup refusals, DIFFER, explicit allocations, dynamic bands and composition. No carried-outcome regression observed. All three new cases returned rc2/setup. No generalized saturation or domain-mastery conclusion follows.

Additional scratch mutant receipts, each independently running all frozen cases, tool selftest and all canonical mutations:

| Candidate | Correct | Selftest | Killed | Anchors |
|---|---:|---:|---:|---:|
| equal-duplicates-kept | 61/61 | 139/139 rc0 | 41/41 | 41/41 unique |
| adjacent-only | 61/61 | 139/139 rc0 | 41/41 | 41/41 unique |
| extras-dedup-by-level | 61/61 | 139/139 rc0 | 41/41 | 41/41 unique |

## Positive boundary checks and residual risk

- Escaped allocation spelling `pan` + Unicode escape for `e` + `l` colliding with literal `panel` correctly returns rc2/setup: object-pairs handling compares decoded keys.
- Equal-valued allocation duplicates, interleaved duplicates, extra duplicates across levels, and bar duplicates at the same level all return rc2/setup in unmodified frozen production.
- A second synthetic live hit at the same monitor/level/namespace returns rc3/model via `find_layer:971-974`. A second live surface sharing the namespace at a different level returns rc0/CLEAN because selection includes level. This is not conflated with declaration uniqueness and is not claimed a protocol violation.
- A surface object with two escaped-equivalent namespace member keys is last-wins and rc0/CLEAN in both base and frozen production (`parse_surfaces:661`, ordinary `load_json:225`). This is a residual raw-declaration ambiguity, outside the specifically promised duplicate allocation-key refusal; no global JSON uniqueness policy is claimed.
- LSP device was unavailable (`xd://lsp`: no such mounted tool). Definition/caller/error-path checks therefore used literal search plus direct source inspection and executable probes, not semantic LSP proof.
- C2, full-repository checks, live compositor behavior, canonical runtime/same-identity rerouting and resume_continuity_v1 are outside this C1 seat's affected scope; none were claimed verified.
- No installs or updates. Only this report is retained; synthetic scratch fixtures and mutants are removed before yielding.

## Self-evaluation

Accuracy 4/5: executable receipts distinguish production from scratch candidates and main predicate from function-level clause exercise; no git-revision admission of mutants was attempted. Completeness 4/5: all assigned boundary families probed, but finite probes cannot exhaust malformed JSON schemas. Clarity 4/5: findings include exact guard changes and stages; synthetic recipes rather than a retained fixture bundle keep output compact. Actionability 5/5: three reproducible surviving implementations and precise source locations identify later counter improvements. Conciseness 4/5: retained evidence is summarized instead of raw child output. Overall 4.2/5. User should agree with the distinction between a passing frozen predicate and broader coverage gaps. Highest-impact improvement is a future, separately frozen counter revision adding the three witnesses; no in-wave predicate edits were made.
