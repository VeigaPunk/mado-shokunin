---
source: S451 (CPython 3.14.8 language reference, assignment statements — attribute-reference targets), S452 (CPython 3.14.8 library reference, `os.environ` mapping modification; supersedes S448's recorded digest); own-work — `.ufo/waves/round-74/{claims-declaration-r74.md,controls/c2-cases-r74.json,control-baseline-r74.txt,measurement-c2-r74.txt}`
verified-at: `b73db773aaf67c9b26c8cf1a4cd567dec3af11f4` (round-74 census; measurement in `.ufo/waves/round-74/measurement-c2-r74.txt`)
recheck: `python3 -I quality/counters/c2-r74-shapes.py --repo . --rev <rev> --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 --controls .ufo/waves/round-74/controls/c2-cases-r74.json --scratch-root DIR` — `controls=36/36 base_controls=32/36 verdict=TARGET_MET`
---

# Two more guard carriers: the two-hop object alias and the one-hop environment alias (round 74, C2)

## 1. The ground

The lane's guard census asks of every `quality/check-*.py` file that reads git objects: does the
environment handed to the child carry `GIT_NO_REPLACE_OBJECTS`? A carrier it does not count is a
real check script that looks guarded and is not.

Two sourced sentences define the carriers this round adds:

| row | sentence (located) | what it grounds |
|---|---|---|
| S451 | "If the target is an attribute reference: The primary expression in the reference is evaluated. It should yield an object with assignable attributes" (`Doc/reference/simple_stmts.rst:160-162`) | `r.env[KEY] = "1"` evaluates `r` first: an alias of the object carries the store at the alias's dotted path, so `r.env` and `cfg.runner.env` name the same mapping when `r = cfg.runner` |
| S452 | "This mapping may be used to modify the environment as well as query the environment." (`Doc/library/os.rst:196-197`) | the environ mapping itself is the mutation surface; a one-hop alias of it (`env = os.environ`) carries the key store into a later copy of that alias |

S452 also corrects the round-73 record: S448's anchor cell recorded
`2d0f2892676e1cf9f0d8e61c63a2e70a86f0e0a5cdb6b06dd7b7d2c9b8b88a4e`; the fetched bytes hash to
`2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5` (208,655 B, three
byte-identical fetches, `.ufo/waves/round-74/fetch/os.rst.{1,2,3}`). Per CORPUS rule 2 the
correction is the new row whose `teaches` opens `supersedes S448 — `, not an edit of S448.

## 2. The two carrier shapes, with their bounds

**A. Two-hop object alias.** A plain name is bound exactly once to a dotted path (`r =
cfg.runner`); the guard key is stored at `r.env[KEY]` and a git launch hands the other spelling
(`env=cfg.runner.env`), or the store is at `cfg.runner.env[KEY]` and the launch hands `env=r.env`.
Both spellings canonicalise to the same dotted path by the longest alias prefix. The store must
sit strictly before the launch; no replacement of that canonical path may sit in between; at
least one side must actually cross the alias edge (the same-spelling store is the held attribute
flow's ground, not this carrier's).

**B. One-hop environment alias.** `env = os.environ` bound exactly once, `env[KEY] = "1"` before
a git launch whose `env=` is the alias itself, `dict(env)` or `{**env}`. A second assignment to
the name leaves no alias at all; a `del env[KEY]` between store and launch cancels the store; a
store after the launch is not a guard.

## 3. The thirty-six-case set

`.ufo/waves/round-74/controls/c2-cases-r74.json` (sha256 `4db4cc70…`): the twenty-eight
round-73 cases carried byte-identically (the counter hash-checks
`.ufo/waves/round-73/controls/c2-cases-r73.json`, sha256 `65e94644…`, and compares every name,
source and expectation) plus eight new cases:

| case | expect | why |
|---|---|---|
| twohop-attr-store-dotted-call | guarded | store on `r.env`, launch on `cfg.runner.env` |
| twohop-attr-store-alias-call | guarded | store on `cfg.runner.env`, launch on `r.env` |
| environ-alias-call-guard | guarded | store through the alias, launch `env=dict(env)` |
| environ-alias-splat-guard | guarded | store through the alias, launch `env={**env}` |
| twohop-attr-store-after-call | not guarded | store after the launch |
| twohop-attr-store-replaced | not guarded | `r.env = {…}` between store and launch |
| environ-alias-no-store | not guarded | alias handed with no key store |
| environ-alias-rebound | not guarded | the name is assigned twice, so it is not an alias |

## 4. Measurement

At `b73db773…` (`quality/counters/c2-r74-shapes.py`):

```
MADO_R74_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0
controls=36/36 base_controls=32/36 verdict=TARGET_MET rev=b73db773aaf67c9b26c8cf1a4cd567dec3af11f4
```

The population is every tracked `quality/check-*.py` at that revision: 20 files, 13 git readers,
13 guarded, 0 unguarded — unchanged from round 73, so the new carriers did not reclassify a
production check script. The do-nothing control (the round-73 classifier at `bd5a9715…`) scores
32/36 and misses exactly the four new positives, named in the receipt's `correct=no` base lines:
`twohop-attr-store-dotted-call`, `twohop-attr-store-alias-call`, `environ-alias-call-guard`,
`environ-alias-splat-guard`.

## 5. Declared limits

- Line order is not execution order: a store in one function and a launch in another are ordered
  by their line numbers, the same cross-method approximation the attribute flow already declares.
- One object-alias edge and one `os.environ` alias; no chains, no cross-module producer.
- The generic env-named flow's `del env[KEY]` cancellation is still unmodelled: a delete of a key
  stored through a plain env-named mapping is not seen by `subscript_guard_lines`. The alias path
  does model its own delete.
- The classifier is a syntactic approximation; it does not interpret values, so a store of a
  non-guard value spelled with the guard key's name is counted (the held value-position cases
  bound the opposite direction).
