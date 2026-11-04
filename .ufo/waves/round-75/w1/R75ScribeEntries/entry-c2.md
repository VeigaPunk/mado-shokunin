---
source: own-work — `.ufo/waves/round-75/{claims-declaration-r75.md,controls/c2-cases-r75.json,measurement-c2-r75.txt}`; `quality/counters/c2-r75-shapes.py`; held `quality/counters/c2-r74-shapes.py`; external S-row citations reserved for the L1
verified-at: `def73656c94f0e88bd671cfb4a65124338261722` (freeze and instruments; the supplied measurement names this revision, not a commit containing the receipt)
recheck: `python3 -I quality/counters/c2-r75-shapes.py --repo . --rev <rev> --base-rev b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6 --controls .ufo/waves/round-75/controls/c2-cases-r75.json --scratch-root DIR` — `population=20 readers=13 guarded=13 unguarded=0 controls=47/47 base_controls=41/47 verdict=TARGET_MET`
---

# Name-neutral guard copies and literal-key deletion (round 75, C2)

## 1. Two rule deltas

The guard census asks whether git-object readers among tracked `quality/check-*.py` hand the
child an environment carrying `GIT_NO_REPLACE_OBJECTS`. The successor retains the round-74
classifier's carried shapes and adds two bounded syntactic rules.

**A. Name-neutral mapping construction.** A simple name bound to a mapping carrying the guard
key in **key position** can guard a launch whatever the name. Both
`child = dict(env, GIT_NO_REPLACE_OBJECTS="1")` and
`child = {**env, "GIT_NO_REPLACE_OBJECTS": "1"}` count when passed as `env=child`.
The guard binding must be strictly before the launch, with no intervening plain rebinding
that loses the guard. A keyless copy, a mention only in value position, or a rebound copy does
not establish this guard. The delta removes the env-named restriction for these mapping
constructions; it does not promise arbitrary alias or mutation analysis.

**B. Literal-key cancellation.** Within the same scope, `del env["GIT_NO_REPLACE_OBJECTS"]`
strictly between construction/store and launch cancels that guard. Deleting another key or
deleting before the later store does not cancel it. The round-74 generic env-named flow's
unmodelled deletion is the gap closed here; no dynamic-key interpretation is claimed.

## 2. Eleven appended cases, grouped by shape

The frozen forty-seven-case set is `.ufo/waves/round-75/controls/c2-cases-r75.json`, SHA-256
`d99502ba23e969a981a856a06742d8da14e1684850c7ca0e0900cd2dc7767897`. Its first thirty-six
cases carry the round-74 set byte-identically, checked against SHA-256
`4db4cc70d1a8e86876f20a9527cfc7f0c7a344eb6d2655b398443b907b3a73d0`. Every appended case
is labelled a git reader; the guard expectations below are the rule separators.

| shape | appended case | expected guard | separator |
|---|---|---|---|
| keyed copy positive | copy-dict-kw-bound | yes | `dict(env, KEY="1")` bound to `child` |
| keyed copy positive | copy-splat-bound | yes | `{**env, KEY: "1"}` bound to `child` |
| keyed copy positive | copy-dict-builtin-bound | yes | `dict(os.environ, KEY="1")` bound to `child` |
| keyed copy positive | copy-dict-literal-base | yes | `dict(base, KEY="1")`, base is a literal mapping |
| copy negative | copy-dict-no-key | no | `dict(env)` supplies no guard |
| copy negative | copy-dict-value-position | no | guard text is only `LABEL`'s value |
| copy negative | copy-rebound | no | keyless rebinding before launch |
| deletion cancellation | del-env-store-cancel | no | literal-key delete after subscript store |
| deletion cancellation | del-env-literal-cancel | no | literal-key delete after keyed literal construction |
| deletion boundary | del-other-key | yes | deletes `PATH`, not the guard key |
| deletion boundary | del-before-store | yes | deletion precedes the guard store |

`KEY` in the table abbreviates the literal `GIT_NO_REPLACE_OBJECTS` spelling in the frozen
sources, not an extra promise to resolve arbitrary key variables.

## 3. Population and control separation

The supplied `.ufo/waves/round-75/measurement-c2-r75.txt`, measured revision
`def73656c94f0e88bd671cfb4a65124338261722`, ends:

```
MADO_R75_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=47/47 base_controls=41/47 verdict=TARGET_MET rev=def73656c94f0e88bd671cfb4a65124338261722
```

The census is unchanged: twenty tracked check scripts, thirteen readers, thirteen guarded,
zero unguarded. The successor's expanded rules therefore do not newly classify a production
check script in this measured population. The held round-74 classifier at base
`b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6` scores `41/47`, missing the four keyed-copy
positives and the two deletion cancellations; all forty-seven successor labels match.

`TARGET_MET` requires all frozen population and control counts, not merely a larger correct
count. The exit map is 0 for met, 1 for measured misses, and 2 for usage/setup errors with no
contract line. This scribe did not rerun the measurement.

## 4. Declared limits

- Line order is not execution order: the inherited cross-method attribute-flow approximation
  compares source line numbers, not all possible executions.
- One object-alias edge and one `os.environ` alias, without chains or cross-module producer
  interpretation.
- The name-neutral rule recognises a keyed mapping passed as `env=`, not the truth of its
  values. Key presence is syntactic evidence, not proof of effective replacement protection.
- The new delete cancellation recognises a literal key in the same scope only. It does not
  establish interprocedural cancellation or dynamic-key flow.
- These forty-seven cases are a frozen separator set, not general Python semantic coverage.
  In particular, `del-before-store` is a syntactic ordering case, not a promise its keyless
  mapping deletion would execute without raising.

## Receipt provenance

The measurement names the freeze/instrument revision above; the receipt is committed with this
round's landing, rather than being part of that measured revision (landing status supplied by
the L1, not independently observed by this scribe). The L1 supplies the external S-row citations.
