---
source: S453, S454 in [SOURCES](../SOURCES.md) plus own-work receipts `.ufo/waves/round-75/{claims-declaration-r75.md,controls/c2-cases-r75.json,control-baseline-r75.txt,measurement-c2-r75-final.txt}`; `quality/counters/{c2-r75-shapes.py,c2-r74-shapes.py}`
verified-at: `4527fcae6a8619e890172ca0a616ae8a3e20fd87` (the final measured content; freeze body `def73656c94f0e88bd671cfb4a65124338261722`)
recheck: `python3 -I quality/counters/c2-r75-shapes.py --repo . --rev <rev> --base-rev b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6 --controls .ufo/waves/round-75/controls/c2-cases-r75.json --scratch-root DIR` — `population=20 readers=13 guarded=13 unguarded=0 controls=47/47 base_controls=41/47 verdict=TARGET_MET`
---

# Name-neutral guard copies and literal-key deletion (round 75, C2)

## 1. Two rule deltas on the guard census

The census asks whether git-object readers among tracked `quality/check-*.py` hand the child an
environment carrying `GIT_NO_REPLACE_OBJECTS`. The successor keeps every round-74 shape and adds
two bounded syntactic rules.

**A. Name-neutral keyed mapping.** A simple name bound to a mapping that carries the guard key in
**key position** guards a launch whatever the binding's name: `child = dict(env,
GIT_NO_REPLACE_OBJECTS="1")` and `child = {**env, "GIT_NO_REPLACE_OBJECTS": "1"}` both count when
handed as `env=child`. The binding must sit strictly before the launch with no plain rebinding of
the name in between; a keyless copy, a key in value position and a rebound copy do not count. The
runtime ground is S454: the keyword pairs are added to the dictionary created from the positional
mapping, so the copy itself holds the guard key. The hand-off is `env=` only — a positional
argument to a git launch is argv-adjacent metadata, never the child environment (repaired after
the round's reviewer found the positional false positive; commit `e3e29bb4`).

**B. Literal-key cancellation.** In the same scope, `del env["GIT_NO_REPLACE_OBJECTS"]` strictly
between the guard construction and the launch cancels that guard. The runtime ground is S453:
deletion of a subscription is passed to the primary object, so the key is removed from the mapping
the child would receive. Deleting another key, or deleting before the later store, cancels
nothing; a delete inside a dead branch does not cancel either (repaired after the round's
reviewer; commit `e3e29bb4`).

## 2. The eleven appended cases

The frozen set is `.ufo/waves/round-75/controls/c2-cases-r75.json` (sha256 `d99502ba…`); its
first thirty-six cases carry the round-74 set byte-identically (sha256 `4db4cc70…`).

| shape | case | expect guard | held r74 | successor |
|---|---|---|---|---|
| keyed copy bound to a name | `copy-dict-kw-bound` | yes | no | yes |
| keyed copy bound to a name | `copy-splat-bound` | yes | no | yes |
| keyed copy of `os.environ` | `copy-dict-builtin-bound` | yes | no | yes |
| keyed copy of a literal base | `copy-dict-literal-base` | yes | no | yes |
| copy negative | `copy-dict-no-key` | no | no | no |
| copy negative (value position) | `copy-dict-value-position` | no | no | no |
| copy negative (rebound) | `copy-rebound` | no | no | no |
| delete cancellation | `del-env-store-cancel` | no | yes (false accept) | no |
| delete cancellation | `del-env-literal-cancel` | no | yes (false accept) | no |
| delete boundary | `del-other-key` | yes | yes | yes |
| delete boundary | `del-before-store` | yes | yes | yes |

Measured at `4527fcae`: `population=20 readers=13 guarded=13 unguarded=0 controls=47/47
base_controls=41/47`. The held classifier misses exactly the four copy positives and the two
deletion cancellations. The expanded rules classify no new production check script in this
population.

## 3. Declared limits

- Line order is not execution order: the inherited cross-method approximation compares line
  numbers.
- One object-alias edge and one `os.environ` alias, no chains; a syntactic approximation that does
  not interpret values.
- The name-neutral rule recognises a keyed mapping handed as `env=`; key presence is syntactic
  evidence, not proof the value disables replacement at runtime.
- The delete cancellation is a literal key in the same scope only; no interprocedural or dynamic
  key flow. `del-before-store` is an ordering case whose source would raise `KeyError` before any
  launch (the key is absent when deleted) — the label pins the ordering rule, not a reachable
  runtime state; a successor fixture should initialise the key first.
