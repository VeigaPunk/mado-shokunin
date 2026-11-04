# R84MutationTester — independent mutation probe

Frozen revision: `3f9eec3906ddd1492e8bc08325e83064f00111ea`.
Axes: coverage, operability, false-kill resistance, exact restoration.
No production changes, commits, delegation, installations, compositor/service mutations, screenshots, or input capture. Scratch clones and generated mutation fixtures only. Tooling rules read; pacman not used. Python 3.14.8; existing jq route reports jaq 3.1.1.

## Principal findings

1. **C2's full frozen predicate does not complete.** Actual child exit **2**, after 33 executed / 33 matched live rows and 28 printed mutant kills:

   ```text
   MADO_R84_RUNBOOK: ERROR (stage=setup mutant pipeline-guard-stripped anchor occurs 2 times, not once)
   ```

   The anchor `        executed_argv = list(argv)` occurs both in the quoted MUTATIONS entry and in executable `run()` code. Its full-source count is two. This is a baseline setup failure, **not a killed mutant**; no TARGET_MET was printed. The enclosing receipt shell exited zero after printing `rc=2`; the counter's actual exit is the latter. The initial parallel launch failed before counter execution because its output directory did not yet exist; the recorded baseline is the subsequent completed launch.

2. **Surviving C1 wrong rules:** permitting equal-valued repeated allocation keys; case-insensitive namespace identity. Each scores **61 → 61 → 61** on pristine / mutated / restored bytes.
3. **Surviving C2 wrong rules in the two contained cases:** accepting any nonzero producer status; accepting a stdout prefix instead of exact text. Each scores **2 → 2 → 2**. These are bounded relevant-case findings, **not full-counter passes**: the full C2 baseline remains inconclusive as above.
4. Removing the allocation duplicate-preserving hook and excluding the bar from namespace identity are behaviorally killed. Removing only the failing-producer fixture's execution guard is behaviorally killed. An equivalent guard-semicolon-to-newline rewrite survives; **no false kill observed in the bounded detector**. Do not count the full-counter setup failure as a behavioral kill.

## Detector and actual results

C1 detector: import the frozen `quality/counters/c1-r84-namespaces.py`; call its unchanged `run_cases(tool_path, all_61_frozen_cases, own_scratch, phase)`. A kill requires fewer than 61 correct. Each mutation changes one unique behavior-bearing point; every variant runs the identical detector on pristine, mutated and exactly restored bytes. No missing-anchor or parse-error kill substituted for scoring.

C2 bounded detector: import each scratch counter variant; execute the actual frozen argv for `pipefail-demonstration` and `producer-failure-propagated` through its `run()`; score using its `case_correct()` including all committed churn and negative samples. Baseline and restoration must both match 2/2. Replacements are anchored to the complete executable line, excluding the quoted mutation-list entry.

| Mutant | Smallest change | Pristine → mutated → restored | Actual result |
|---|---|---|---|
| C1 equal-duplicate-accepted | `if key in out:` becomes `if key in out and out[key] != value:` | 61 → 61 → 61 | Survived; frozen duplicate case uses differing values 24 and 40, so it cannot distinguish equal-key/equal-value acceptance |
| C1 namespace-casefold | `set(names)` becomes `set(name.lower() for name in names)` | 61 → 61 → 61 | Survived; over-refuses case-distinct identities |
| C1 allocation-hook-removed | `load_json(raw, "allocation", pairs_hook=allocation_pairs)` becomes `load_json(raw, "allocation")` | 61 → 60 → 61 | Killed by `duplicate-allocation-keys` only |
| C1 namespace-bar-excluded | names list excludes `bar["namespace"]` | 61 → 60 → 61 | Killed by `duplicate-bar-namespace` only |
| C2 producer-any-nonzero | producer matcher changes `rc == value["rc"]` to `rc != 0` | 2 → 2 → 2 | Survived bounded detector; accepts rc141 with the plausible text |
| C2 producer-prefix-text | exact stdout comparison becomes `.startswith(value["text"])` | 2 → 2 → 2 | Survived bounded detector; accepts appended junk |
| C2 fixture-guard-stripped | execution strips `set -o pipefail; ` only from argv containing `failing-producer.sh` | 2 → 1 → 2 | Killed: producer row returns rc0 with `b true`, rather than required rc7 |
| C2 equivalent-guard-newline | execution replaces guard's `; ` separator with newline | 2 → 2 → 2 | Equivalent survivor, not a coverage defect or false kill |

The full pristine C1 invocation from the declaration completed with child rc0:

```text
cases=61 correct=61 mutants=41 killed=41 base_correct=58/61 carried=58/58 tool_selftest=139/139 verdict=TARGET_MET
```

The independent probes above do not claim to rerun the full enumerated populations for each new mutant. Their specified bounded behavioral detector is the case-scoring function, run identically in all three phases.

## Authentic shell status and wrong-rule witnesses

Contained shell commands only; `/bin/sh` resolves to `/usr/bin/bash` on this host. Each actual stdout below was `b true` after newline removal.

| Command shape | Actual pipeline rc |
|---|---:|
| failing-producer fixture `\| cat`, no guard | 0 |
| same fixture `\| cat`, with pipefail | 7 |
| failing producer `\|` tail that consumes input then exits 9, with pipefail | 9 |
| same failing tail without pipefail | 9 |
| `yes 'b true' \| head -n 1`, with pipefail | 141 |

Thus pipefail supplies the **rightmost nonzero pipeline status**, not necessarily the producer's own status. In the frozen tiny-output fixture, successful `cat` makes rc7 genuine propagation of that particular producer's exit7. In general, SIGPIPE can instead give 141 and a failing final stage can supersede the producer with rc9. No claim of authentic producer-status attribution follows from a pipeline rc alone.

Direct matcher witnesses (pristine vs changed behavior):

- `(rc141, "b true\n")`: pristine producer matcher **False**, any-nonzero mutant **True**. The actual SIGPIPE command above demonstrates that this pair is attainable.
- `(rc7, "b true EXTRA\n")`: pristine **False**, prefix mutant **True**.
- Equal duplicate allocation `{"panel":40,"panel":40}`: pristine `parse_allocation` gives **setup-refusal**, equal-duplicate mutant **accepted**.
- Case-distinct identity expression `['waybar', 'Waybar']`: pristine duplicate test **False**, casefold mutant **True**. This is an expression-level over-refusal witness, not an additional full join measurement.

## Hashes and exact restoration

C1 pristine/restored tool SHA-256:
`72456666a31927dfc46f955f41b3aa57b2215a8fcd8dc736fc302d7b58830c7f`.

C2 pristine/restored counter SHA-256:
`53f47372a2d44cd07120815835c3cb3ec4e4dca8cb31954bf869292952598839`.

| Mutant | Mutated SHA-256 |
|---|---|
| equal-duplicate-accepted | `adc1fc0be4ae6e77314b895b5cf4796fb7a26345bd32bd9b2689a41599abd816` |
| namespace-casefold | `fa0df1f30971e6cf7b1aac2b0d1e7f68e94e60829213428c898fe3ac8240ccc1` |
| allocation-hook-removed | `6b0ea4dcd4a7d78bb61e6c4f64df0cf0ab8fcda4b930a808f56cb49810c53b1c` |
| namespace-bar-excluded | `5c33f9c7c3d947410bd74b96083e2b12a04c9476265ee6ad6f3042757d094277` |
| producer-any-nonzero | `809c59828b1cb9247a55d457ddd58b12b25dc4f5954d672a164283061edcf953` |
| producer-prefix-text | `bf8b0b75df79e479b8d7ec5bb4418ced9436833030d37d5cb16bd00c571d5bf6` |
| fixture-guard-stripped | `c167b0ee3417c97c27ee7088672667b50992531904f79648d44ee6f0a01df6eb` |
| equivalent-guard-newline | `15d48b2ef49f0503cdede3376ae75fcfe0ecd1b569850d1743f94d10dbed69f4` |

Every restored-phase hash equals its pristine hash; all eight exact-byte comparisons returned True. Restoration occurred in `finally` blocks. Detector results were persisted before a terminal printing-only `KeyError: 'claim'`; all eight three-phase probes and direct witnesses had already completed. The retained results were subsequently read, not fabricated from that formatting failure.

Scratch location: `/fast/scratch/hyaku/mado-r84/R84MutationTester`; explicitly created, receipts summarized here, then removed before yielding. The prepared scratch commit-driver was never executed; no mutant commits were made. Only this report is delivered.

## Limitations and handoff

No integration, contract change, or broad mastery claim. C2 full-predicate evidence is inconclusive because of its pristine anchor-count setup error. The surviving wrong rules are coverage findings, not permission to narrow the frozen contract. Planner can address the anchor collision and, if the frozen contract permits a later instrument revision, add equal-valued duplicate, case-distinct identity, rc141, and stdout-suffix discrimination cases. Those changes were not made here.

Self-evaluation: accuracy 4 (C2 full predicate blocked, clearly separated); completeness 4 (all assigned behavior points probed; C2 bounded subset explicitly labeled); clarity 4 (full-vs-bounded evidence separated); actionability 4 (exact anchors, witnesses and hashes); conciseness 3 (detailed receipt needed). Average 3.8. Main should retain the baseline setup failure and coverage gaps rather than crediting a full C2 pass.
