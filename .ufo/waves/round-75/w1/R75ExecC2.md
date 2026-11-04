# R75ExecC2 — independent frozen C2 measurement

## Axes and scope
Operability: census correctness, frozen-control classification, and runtime fidelity of labels. No-harm: preserve frozen instruments/cases and repository/host state. Calibration C1 is context only, not re-measured by this seat.
Read the declaration and committed baseline/C1/C2 receipts; none was rewritten. No production changes, installs, fixture git mutations, LSP-supported refactors, or external-state operations were needed. No LSP tool is exposed in this seat; symbol work was unnecessary.

## Frozen command and retained receipts
Executed from `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
python3 -I quality/counters/c2-r75-shapes.py --repo . --rev def73656c94f0e88bd671cfb4a65124338261722 --base-rev b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6 --controls .ufo/waves/round-75/controls/c2-cases-r75.json --scratch-root /fast/scratch/hyaku/mado-r75/R75ExecC2/run
```

Exit 0; full stdout, empty stderr, and exit code retained under `.ufo/waves/round-75/w1/R75ExecC2/main-run.{stdout,stderr,rc}`.

```text
MADO_R75_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=47/47 base_controls=41/47 verdict=TARGET_MET rev=def73656c94f0e88bd671cfb4a65124338261722
```

Candidate 47/47; held base 41/47. The base misses precisely four copy positives (`copy-dict-kw-bound`, `copy-splat-bound`, `copy-dict-builtin-bound`, `copy-dict-literal-base`) and two cancellation negatives (`del-env-store-cancel`, `del-env-literal-cancel`). This independently reproduces the committed C2 receipt.

### Full per-file census
```text
MADO_R75_READER file=quality/check-anchor-cover.py reader=yes guard=yes
MADO_R75_READER file=quality/check-axis-scores.py reader=yes guard=yes
MADO_R75_READER file=quality/check-control-receipts.py reader=yes guard=yes
MADO_R75_READER file=quality/check-counter-discrimination.py reader=no guard=no
MADO_R75_READER file=quality/check-deliverables.py reader=yes guard=yes
MADO_R75_READER file=quality/check-evidence-pointers.py reader=yes guard=yes
MADO_R75_READER file=quality/check-freeze-order.py reader=yes guard=yes
MADO_R75_READER file=quality/check-index-rows.py reader=yes guard=yes
MADO_R75_READER file=quality/check-index.py reader=yes guard=yes
MADO_R75_READER file=quality/check-landed-contract.py reader=yes guard=yes
MADO_R75_READER file=quality/check-locators.py reader=no guard=no
MADO_R75_READER file=quality/check-population.py reader=no guard=no
MADO_R75_READER file=quality/check-r38-discrimination.py reader=no guard=no
MADO_R75_READER file=quality/check-r55-controls.py reader=no guard=no
MADO_R75_READER file=quality/check-r56-controls.py reader=no guard=no
MADO_R75_READER file=quality/check-round-outcome-first.py reader=yes guard=yes
MADO_R75_READER file=quality/check-session-material.py reader=yes guard=yes
MADO_R75_READER file=quality/check-state-cite.py reader=no guard=no
MADO_R75_READER file=quality/check-tool-ledger.py reader=yes guard=yes
MADO_R75_READER file=quality/check-wave-done.py reader=yes guard=yes
```

## Selftests
Both use the same executable, `--repo`, `--rev`, and `--base-rev` as above; replace the scratch root and add `--selftest`:

| Variant | Scratch root suffix | Result | Exit |
|---|---|---|---|
| Without `--controls` | `st-noctl` | `MADO_R75_GUARD_SHAPES_SELFTEST: 95/95 assertions passed` | 0 |
| With `--controls .ufo/waves/round-75/controls/c2-cases-r75.json` | `st-ctl` | `MADO_R75_GUARD_SHAPES_SELFTEST: 97/97 assertions passed` | 0 |

Full outputs and exit codes: `selftest-noctl-retry.{stdout,stderr,rc}` and `selftest-ctl-retry.{stdout,stderr,rc}` in the evidence directory. Both stderr files are empty.
Initial attempts mistakenly supplied nonexistent selftest scratch directories; both exited 2 with `--scratch-root is not a directory`, producing no tally. Their full stdout/stderr and rc are retained as `selftest-noctl.{stdout,stderr,rc}` and `selftest-ctl.{stdout,stderr,rc}`. Creating those directories resolved setup; the instrument was not changed.

## Hand-check: eleven appended cases
All eleven are git readers syntactically. Below, “right” means the declared syntactic guard predicate; runtime fidelity is stated separately where material.

| Case | Frozen guard | Hand-check |
|---|---|---|
| `copy-dict-kw-bound` | true | Right: `dict(env, GIT_NO_REPLACE_OBJECTS="1")` adds/overrides the actual key, and that `child` is passed unchanged. |
| `copy-splat-bound` | true | Right: the explicit key after `**env` wins, and the copied `child` reaches `env=`. |
| `copy-dict-builtin-bound` | true | Right: keyword insertion into `dict(os.environ, ...)` carries the guard key into the launched mapping. |
| `copy-dict-literal-base` | true | Right: copying the literal base and inserting the keyword produces a guarded `child`, regardless of its non-env name. |
| `copy-dict-no-key` | false | Right syntactically: `dict(env)` adds no guard; runtime absence is conditional because inherited `os.environ` could already contain it. |
| `copy-dict-value-position` | false | Right syntactically: the string is the value of `LABEL`, not an inserted guard key; inherited ambient guard is not excluded. |
| `copy-rebound` | false | Right syntactically: the guarded first copy is discarded; the second copy adds no guard, though ambient inheritance remains possible. |
| `del-env-store-cancel` | false | Right: the key was stored, so deletion succeeds and removes it from the exact mapping later passed to the child. |
| `del-env-literal-cancel` | false | Right: the literal contains the key, then deletion genuinely removes it before launch. |
| `del-other-key` | true | Right: deleting existing `PATH` succeeds and leaves the guard key intact in the child mapping. |
| `del-before-store` | true | Right only for the declared syntactic ordering rule; runtime fixture defect: the literal has no guard key, so deletion raises `KeyError` and neither the subsequent store nor launch executes. |

**Flagged source/label mismatch:** `del-before-store` cannot demonstrate a genuinely guarded child at runtime: no child exists. Its label is consistent with the frozen syntactic approximation (earlier delete does not cancel a later store), not execution semantics. Reported to L1; L1 explicitly retained the frozen case and requested the defect be documented. No frozen edits. A successor could initialise the key before deleting it, but this wave did not do so. The three ambient-copy negatives are conditional runtime examples, not unconditional proof of absence; their labels remain correct under the stated syntactic predicate.

## Frozen carry proof
Compared ordered first 36 r75 cases to all 36 r74 cases on `name`, `src`, `expect_reader`, `expect_guard`: **0 mismatched cases**, and complete parsed case dictionaries are equal. Exact JSON comparison result is retained in `carry-comparison.json`.

Observed SHA-256 values:
- r75 controls: `d99502ba23e969a981a856a06742d8da14e1684850c7ca0e0900cd2dc7767897`.
- r74 controls: `4db4cc70d1a8e86876f20a9527cfc7f0c7a344eb6d2655b398443b907b3a73d0`.

These match the frozen declaration and the counting command's `carried=yes` receipt. Equality above is exact source-string/field equality, not a claim that the surrounding JSON serialization is identical.

## Disposition, risks, and handoff
Measured C2 target met exactly; no production move proposed. Retained the successful measurement alongside the runtime-fidelity defect rather than recutting the corpus. All assigned measurements were exercised; no broader gate/build/lint/formatting was run. No blockers. L1 owns any integration gates and successor fixture correction. Scratch was removed after retaining receipts; only this requested report and exclusive evidence directory were written.

Self-evaluation: accuracy 4/5 (runtime behavior hand-reasoned, not executed); completeness 5/5 (all four assignment items and original failed setup attempts retained); clarity 4/5 (long full census is required); actionability 4/5 (frozen-case repair intentionally deferred to a successor); conciseness 4/5 (full evidence increases length). Mean 4.2/5. Highest-impact future improvement: exercise corrected successor fixture semantics without changing this frozen corpus. User agreement expected because static success and runtime defect are explicitly separated.
