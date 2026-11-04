---
source: S443 (https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/expressions.rst, § Calls, :1415-1417 @ tag v3.14.8) and S438 (the exported environment is what acts on the git child)
verified-at: 3868bc659621fd1ffeb46d8a2040b1f327ae3444
recheck: `python3 -I quality/counters/c2-r71-shapes.py --repo . --rev HEAD --base-rev c354f4d410b829d985b31560af9202d98655dad0 --controls .ufo/waves/round-71/controls/c2-controls-r71.json --scratch-root <scratch>` prints `TARGET_MET`
---

# Guard carrier shapes r71 (dict-call splat, splat alias, store alias, attribute edge)

Claim: the guard census's carrier rule counts four more Python constructions of the
environment key `GIT_NO_REPLACE_OBJECTS`, each still subject to the held dominance test, and
discriminates them from two negatives on a frozen 23-case set (the round-70 seventeen carried
forward byte-identically).

## The four shapes

| shape | frozen case | construction | dominance requirement |
|---|---|---|---|
| dict-call splat | `dict-call-splat` | `env = dict(os.environ, **GUARD)` with module mapping `GUARD` carrying the key | the mapping bound once at module level; the env name not rebound unguarded before the launch |
| splat through an alias | `dict-call-splat-object-alias` | `m = GUARD; env = {**os.environ, **m}` | `m` bound exactly once and **not rebound between its binding and the splat line** (R71RevC2 F1 repair); a rebinding after the splat is harmless — the contents were already copied |
| store through an alias | `store-through-alias-two-hop` | `e = {"PATH": …}; staging = e; staging[KEY] = "1"; … env=e` | the handed name bound exactly once to a mapping expression; the store strictly between the alias binding and the call; **no rebinding of either name in between, whatever its spelling** |
| attribute through a second object | `attribute-second-object` | `runner.env[KEY] = "1"; cfg.runner = runner; … env=cfg.runner.env` | store-before-use, no plain replacement of the dotted attribute in between (also under edge resolution), and **the edge itself bound strictly before the call** (R71RevC2 F2 repair) |

Negatives frozen in the same set: `unguarded-dict-splat-negative` (a `**` splat of a module
mapping without the key) and `env-call-no-key-negative` (`dict(os.environ)`).

Counting command (frozen):
`python3 -I quality/counters/c2-r71-shapes.py --repo . --rev 3868bc659621fd1ffeb46d8a2040b1f327ae3444 --base-rev c354f4d410b829d985b31560af9202d98655dad0 --controls .ufo/waves/round-71/controls/c2-controls-r71.json --scratch-root <scratch>`
→ `MADO_R71_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=23/23 base_controls=19/23 verdict=TARGET_MET`, rc 0
(`.ufo/waves/round-71/measurement-r71.txt` § C2, first at `8e78a4ee`, re-run at the repair
commit `3868bc65` — the frozen 23 score identically before and after the repair). The
do-nothing control — the held round-70 classifier — scores 19/23, missing exactly the four
carriers and accepting both negatives (pre-freeze receipt `control-baseline-c2-r71.txt`). The
widened classifier reclassifies no production file: the per-file census over the twenty
population files is sort-identical to the round-70 classifier's (review-verified,
`w1/R71RevC2.md`).

## Review-driven repair

The round's reviewer falsified the first widening: two dominance bypasses inside the declared
envelope (straight-line code, one hop, exact dotted names) that flip no frozen case but
violate the frozen sentence's "each still subject to the dominance test":
(a) *splat-alias rebind* — `m = GUARD; m = {"LABEL": "x"}; env = {**os.environ, **m}` credits
the alias although the module mapping's contents never reach the launch;
(b) *edge-after-use* — a genuinely executing launch through a pre-bound `cfg.runner.env`
credited when the `cfg.runner = runner` edge was bound only after the call.
Both are repaired in `3868bc65` with red-before/green-after receipts
(`.ufo/waves/round-71/c2-dominance-repair-r71.txt`; the pre-fix blob credits both, the
repaired counter refuses both) and pinned as counter regressions
(`r71-splat-alias-rebound-before-splat`, `r71-attribute-edge-after-use`; selftest 63/63).

## Sourced ground

S443 supersedes S439 for this scope (CORPUS rule 2: a new row whose `teaches` opens
`supersedes S439 —`; S439 keeps its dictionary-display scope and its cells). Fetched
2026-11-04 three times, byte-identical, sha256
`e19de4fead912abcb323f3a6ab42b20595bf6b8ae302e04f257b844b3ce7582a` (92,034 bytes — the digest
S439 already records). Located quote, 25 words, expressions.rst:1415-1417: "If the syntax
`**expression` appears in the function call, `expression` must evaluate to a mapping, the
contents of which are treated as additional keyword arguments." — a `**` operand inside a call
is a real carrier of the mapping's contents, not a mention, which is what makes the dict-call
splat and its alias forms count.

## Limits

One module, one alias hop, one object-alias edge, exact dotted names, no container flow, no
path-sensitivity beyond a literal-false branch; key presence is value-agnostic (a later
keyword/splat/value can neutralize the setting); method-call mutations (`.clear()`, `.pop()`)
and non-Assign replacements are untracked; a function-scoped `global GUARD` rebinding executed
before the splat escapes both splat carriers (inherited r70 bound, disclosed by the reviewer
F3); stores spelled through the edge (`cfg.runner.env[KEY] = "1"` used as plain `runner.env`)
do not resolve — the sentence's spelled direction (reviewer F4, within the declared bound);
`alias_store_guard` is conservative (any second binding of the handed name disqualifies — may
under-credit); cross-method attribute order is source-line order. A guarded environment does
not authenticate objects and does not protect an already-rewritten repository.
