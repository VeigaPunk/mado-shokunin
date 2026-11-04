source: S439 — CPython v3.14.8 `Doc/reference/expressions.rst` (fetched 2026-11-04 three times, byte-identical, sha256 e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a, 92034 bytes) — "A double asterisk `**` denotes dictionary unpacking. Its operand must be a mapping. Each mapping item is added to the new dictionary." — the ground for counting a `**` expansion of a guarded module mapping as a carrier of the key; and S440 — CPython v3.14.8 `Doc/reference/simple_stmts.rst` (fetched 2026-11-04 three times, byte-identical, sha256 d43206423b327dcf05009b5aa26d1175a516a597367cc4739851d3b299ae29dc, 41375 bytes) — "If the target is a subscription: The primary expression in the reference is evaluated. Next, the subscript expression is evaluated." — the ground for counting a name-valued subscript key as that key's value, not as a mention
verified-at: 2026-11-04
recheck: 90d — re-fetch both pages at the same tag and re-hash; re-run `quality/counters/c2-r70-carriers.py` when the classifier's carrier functions, the frozen 17-case set, or the census population regex change

# Guard carriers: alias, attribute, splat and name-valued key (MADO-R70-1)

## Scope

Lane-tooling scope only. This entry explains round-70 claim C2
(`.ufo/waves/round-70/claims-declaration-r70.md`, C2 §): the four environment-carrier
shapes the round-69 guard census missed, why each is a real carrier under the language's
own documentation, and why each still has to satisfy the round-69 dominance test (the
guarded environment must reach a `git` launch). It is not a claim about any gate's
correctness and not a runtime measurement.

The measured population is unchanged: the same 20 tracked `quality/check-*.py` files,
13 readers, 13 guarded, 0 unguarded at both the base and the measured revision.

## 1. The four shapes

Round 69 counted a key only in key position and only when the environment reached a
launch. Its classifier read *names*: an env-named binding, a local producer, a one-hop
parameter. Four constructions build the same environment through a different carrier and
were counted as unguarded (`.ufo/waves/round-70/control-baseline-r70.txt` § C2: the
round-69 classifier scores 13/17 on the round-70 set).

| shape | construction | why it is a carrier, and the documented ground |
|---|---|---|
| alias | `env = base; alias = env; alias[KEY] = "1"` then `git … env=env` | the alias and `env` are the same object; S440 says a subscription store evaluates the primary and calls `__setitem__` on *it*, so the guarded mapping is the one `env` names |
| attribute | `self.env[KEY] = "1"` then `git … env=self.env` | same store, on an attribute reference; the launch hands the same object |
| splat | `GUARD = {KEY: "1"}` (module) then `env = {**os.environ, **GUARD}` | S439: "Its operand must be a mapping. Each mapping item is added to the new dictionary" — the guarded item is in `env` |
| constant key | `KEY = "GIT_NO_REPLACE_OBJECTS"` (module) then `env[KEY] = "1"` | S440: the *subscript expression is evaluated* — the store is under the key's value, not under the spelling `KEY` |

## 2. The rule in one sentence

Round-69 key position and its three dominance flows stay in force; a construction counts
when the guard key lands in an environment mapping and that mapping reaches the `git`
launch by inline `env=`, an env-named binding (or a local producer) with no intervening
unguarded rebinding, or a one-hop argument bound to the callee's env-named parameter;
the four carriers above are alternative ways to *construct* that environment, never a
substitute for dominance. A module-level constant counts only when the module binds it
once, to a literal; a second module-level binding disqualifies it.

## 3. The frozen seventeen cases

`quality/counters/c2-r70-carriers.py` scores `.ufo/waves/round-70/controls/c2-controls-r70.json`
(sha256 `29947b4ce5890f5c977f3ec74bafd14ba12b0d581dcb03ef1e3b637017a778ff`). The first
eleven are the round-69 set carried forward byte-identically; the counter asserts the
round-69 file still hashes to `975ca3ba…` and carries the same eleven cases. The six new
cases:

| case | reader | guard | what it pins |
|---|---|---|---|
| `alias-carried` | yes | yes | the store through an alias is a store on the env-named object |
| `attribute-carried` | yes | yes | the store on `self.env` and the launch `env=self.env` are the same mapping |
| `splat-carried` | yes | yes | a guarded module mapping expanded with `**` carries the key |
| `constant-key` | yes | yes | a module string constant used as the subscript is the key |
| `guarded-env-for-a-non-git-call` | yes | no | a guard handed to a non-`git` call does not guard the `git` launch |
| `git-called-without-env` | yes | no | a guard built in the same scope but never handed to the launch is not a guard |

Measured: `population=20 readers=13 guarded=13 unguarded=0 controls=17/17
base_controls=13/17 verdict=TARGET_MET` at
`3d28f92a819b84e2004ef1301f9303f81ad497ab` (`.ufo/waves/round-70/measurement-r70.txt`). **After review** (`w1/R70RevC2.md` blockers 1-2) the implementation was repaired against this same rule - the attribute carrier now requires a store line before the call with no plain assignment to the same dotted attribute in between, and a module string constant counts only when the store's scope does not rebind it. The red-before/green-after is `.ufo/waves/round-70/c2-classifier-repair-r70.txt` (prefix `(True, True)` -> postfix `(True, False)` on all three attack cases), the frozen 17 score identically before and after, and the five attack cases are pinned in the counter's selftest (54/54).

## Pins

| id | proposition | source | pin |
|---|---|---|---|
| K01 | A `**` display item's operand must be a mapping and each of its items is added to the new dictionary, so a guarded module mapping expanded into the env mapping carries the key. | S439 | expressions.rst:510 |
| K02 | A subscription target evaluates the primary then the subscript expression, so `env[KEY]` with a module string constant stores under the key's value. | S440 | simple_stmts.rst:191 |

## 4. What stays outside

- Two-hop aliases, aliasing through a second object, and container-held env mappings.
- `dict(**GUARD)` call form: the counter's splat detector reads dict *literals* with a
  `**` item, not call keywords expanded from a mapping.
- The guard *value* is not interpreted: `GIT_NO_REPLACE_OBJECTS="0"` also disables
  replacement and is counted.
- Cross-module producers; non-`check-` instruments; shell scripts (the census population
  is the tracked `quality/check-*.py` set).
- A guarded environment does not authenticate objects and does not protect a repository
  that is already rewritten.

## 5. Verify

```
python3 -I quality/counters/c2-r70-carriers.py --repo . --rev <rev> \
  --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 \
  --controls .ufo/waves/round-70/controls/c2-controls-r70.json --scratch-root <dir>
```

Exit 0 iff `population=20 readers=13 guarded=13 unguarded=0 controls=17 base_controls=13`;
the last line is the contract sentence § 3 quotes. `--selftest` carries the seventeen
cases plus the regression table (49/49 at the measured content).
