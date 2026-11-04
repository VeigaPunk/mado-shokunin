---
source: S451 (CPython v3.14.8 assignment statements, attribute-reference targets), S452 (CPython v3.14.8 os.environ mapping modification); own-work — `.ufo/waves/round-74/{claims-declaration-r74.md,controls/c2-cases-r74.json,control-baseline-r74.txt,measurement-c2-r74.txt}` and `quality/counters/c2-r74-shapes.py:{twohop_guard,environ_alias_guard}`
verified-at: `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4` (committed census receipt; not a fresh run by this scribe)
recheck: `python3 -I quality/counters/c2-r74-shapes.py --repo . --rev b73db773aaf67c9b26c8cf1a4cd567dec3af11f4 --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 --controls .ufo/waves/round-74/controls/c2-cases-r74.json --scratch-root DIR`
---

# Guard carriers: the two-hop object spelling and the environment alias (round 74, C2)

## Ground and command provenance

The axes are operability (the C2 guard census) and calibration (accurate separation of recorded evidence from a new execution). This entry changes neither instrument nor frozen expectations.

Below, **M** means the exact `recheck:` command above, with `DIR` an existing explicitly supplied scratch directory. Every empirical count and case result below comes from M's committed output, `.ufo/waves/round-74/measurement-c2-r74.txt`, not a rerun. The separate pre-freeze receipt `.ufo/waves/round-74/control-baseline-r74.txt` corroborates the held misses; its original invocation is not present in that receipt and is not reconstructed here.

The census asks whether a tracked `quality/check-*.py` reader hands a guard-bearing environment to its git child. The carrier is the mapping, not a mention of `GIT_NO_REPLACE_OBJECTS` in a value.

| source | located quotation | scope |
|---|---|---|
| S451 | “The primary expression in the reference is evaluated.” (`.ufo/waves/round-74/fetch/simple_stmts.rst.1:160-165`) | Attribute assignment evaluates the object expression; an alias may name the object whose attribute is assigned. |
| S452 | “This mapping may be used to modify the environment as well as query the environment.” (`.ufo/waves/round-74/fetch/os.rst.1:196-198`) | The environment mapping is mutable; the following source sentence states that modifying it automatically calls `putenv`. |

Sources ground Python semantics, not the classifier's completeness or runtime dominance.

## Carrier A — an object alias crosses the dotted spelling

```python
r = cfg.runner
r.env["GIT_NO_REPLACE_OBJECTS"] = "1"
subprocess.run(["git", "show", "HEAD:a"], env=cfg.runner.env)
```

The reverse spelling also counts: store into `cfg.runner.env[KEY]`, then hand `env=r.env`.
`twohop_guard` uses the existing alias map to canonicalise the dotted expressions. The plain alias name must be assigned exactly once by the syntactic alias-map rule. At least the store or the call must cross the alias edge; a same-spelling store is already the held attribute-flow carrier.

Dominance bounds: the guard-key store must be strictly earlier in line order than the git launch; no recorded replacement of that canonical dotted path may occur between them. Dead-line assignments and calls are excluded. Keys may be the guard literal or a recognised module constant. This is an object-alias edge, not arbitrary alias-chain resolution.

## Carrier B — an alias of the process environment

```python
env = os.environ
env["GIT_NO_REPLACE_OBJECTS"] = "1"
subprocess.run(["git", "show", "HEAD:a"], env=dict(env))
```

`environ_alias_guard` recognises the alias itself (`env=env`), the copy `env=dict(env)`, and the copy `env={**env}`. The alias is a plain name assigned exactly once to `os.environ`; another counted assignment removes it from the alias set. The `dict` copy has a sole positional alias argument and no keywords; the splat copy contains only that alias.

Dominance bounds: the store must be strictly before the launch. This helper explicitly cancels a store if `del alias[KEY]` occurs between store and launch. A store after the launch does not count. Neither this helper nor the object helper establishes actual execution order.

## Frozen additions and measurement

The following eight new cases and all their expected/observed classifications are from **M**, candidate receipt lines 51–58 and held lines 88–95. Every case expects `reader=yes`; both legs report that reader result.

| frozen case | expected guard | candidate guard (M) | held guard (M) |
|---|---|---|---|
| `twohop-attr-store-dotted-call` | yes | yes | no |
| `twohop-attr-store-alias-call` | yes | yes | no |
| `environ-alias-call-guard` | yes | yes | no |
| `environ-alias-splat-guard` | yes | yes | no |
| `twohop-attr-store-after-call` | no | no | no |
| `twohop-attr-store-replaced` | no | no | no |
| `environ-alias-no-store` | no | no | no |
| `environ-alias-rebound` | no | no | no |

The call-guard positive uses `dict(env)`; the splat positive uses `{**env}`. The rebound negative contains a rebinding but no guard-key store, so it is not an isolated demonstration of rebinding cancelling a previously stored guard.

| quantity | result | command and receipt |
|---|---|---|
| population / readers / guarded / unguarded | 20 / 13 / 13 / 0 | M; final `MADO_R74_GUARD_SHAPES` line |
| candidate controls | 36/36 | M; final line |
| held controls | 32/36 | M; `MADO_R74_BASE` and final lines |
| held misses | four new positives, exactly the first four rows above | M; held detail lines 88–91; corroborated by `control-baseline-r74.txt:13-17` |
| carried cases | 28, byte-identical round-73 cases | M; `MADO_R74_HELD_CONTROLS ... carried=yes` line |
| verdict | `TARGET_MET` | M; final line |

The frozen declaration requires those exact population and control counts for `TARGET_MET`. It specifies exit 0 for met, exit 1 for measured-and-missed, and exit 2 for setup/usage errors without a contract line. The supplied assignment reports committed M exit 0; the receipt text itself contains no exit-code field. This scribe did not execute M or any no-harm gate.

## Declared limits

- **Line order is not execution order.** The cross-method approximation inherited from attribute flow remains; a lexically earlier store is not proof that the launch actually executes it.
- **One edge, no chains.** Only the declared object-alias edge and the one-hop `os.environ` alias are followed; do not infer arbitrary alias closure.
- **Generic deletion remains unmodelled.** The generic env-named flow still does not cancel `del env[KEY]`. The specialised environment-alias helper's local cancellation does not repair or override that generic path; do not claim an end-to-end deletion guarantee.
- **Syntax, not values.** The detector does not interpret whether a stored value enables the guard, and the finite cases are not general program correctness evidence.

The improved control classification does not add census population members and does not establish host configuration, live process behaviour, or execution-order correctness.
