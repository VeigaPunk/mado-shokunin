# Interprocedural and dynamic-key deletions in the guard census (round 76)

Lane: mado-shokunin. Round 76, claim C2 (operability). Measured instrument:
`quality/counters/c2-r76-shapes.py`; measured at `3588a527eba555a94e497097b0467efc04274c6d` (this instrument's last change: the D3 parameter-binding repair and the allowlisted child
environment / scope-local cancellation repairs), with earlier receipts at `755b339f…`,
`cb713254…` and `5dade9b3…` showing identical counts; base `c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf`.
Receipts: `.ufo/waves/round-76/measurement-c2-r76-final.txt` (re-executed at the repair commit),
`.ufo/waves/round-76/control-baseline-r76-matched.txt` (matched pre-freeze control).

## 1. What the census answers

`quality/check-*.py` read git through subprocesses. A reader is a `quality/check-*.py` whose
bytes carry a git verb; a reader is *guarded* when the child's environment carries
`GIT_NO_REPLACE_OBJECTS=1`, so a forged replace ref cannot change what `git show` returns.
The census classifies the whole population at a revision and prints

```
MADO_R76_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=59/59
                       base_controls=55/59 verdict=TARGET_MET rev=<sha>
```

`controls=` is the frozen case set's score; `base_controls=` is the same set scored by the
held round-75 classifier extracted at `--base-rev`, in the same run.

## 2. D3 — a delete inside a callee cancels the caller's guard

Round 75 modelled `del env[KEY]` only in the scope that holds the binding. The mapping is an
object: a callee that receives it as a parameter deletes the key from the caller's mapping.
CPython v3.14.8 says a subscription deletion "is passed to the primary object involved"
(S453) and that a call places the argument in the parameter's slot (S455), so the callee's
`del m[KEY]` and the caller's `env` are the same mapping.

The rule: a local function `f(m)` whose body contains a live `del m[<guard key>]` with no
rebinding of `m` before the delete is a *cancelling callee*; at a call site `f(env)` a
cancellation line is recorded for `env`, and the dominance test (`guard line < call line <
first launch use`) decides.

| case | label |
|---|---|
| `callee-del-literal` | not guarded: the callee deletes the key from the launched mapping |
| `callee-del-store` | not guarded: store then callee delete before the launch |
| `callee-del-other-key` | guarded: the deleted key is not the guard key |
| `callee-del-dead-branch` | guarded: the delete is in a literal-false branch |
| `callee-never-called` | guarded: no call site |
| `callee-called-after-launch` | guarded: the call is after the launch |
| `callee-del-param-rebound` | guarded: `m = {…}` before the delete targets a fresh dict |
| `callee-del-param-rebound-live` | guarded: `m = dict(m)` before the delete targets a copy |

## 3. D4 — a same-scope constant name as the delete key

`del env[k]` cancels when `k` is bound exactly once in the same scope, before the delete, to
the guard key (a string literal equal to `GIT_NO_REPLACE_OBJECTS`, or a module-level constant
whose value is it). Deleting an unbound name raises `NameError` (S456), so a name bound after
the delete cannot be the key at the delete.

| case | label |
|---|---|
| `dynamic-key-del` | not guarded: `k` bound once to the guard key |
| `dynamic-key-module-const` | not guarded: module constant resolves to the guard key |
| `dynamic-key-other` | guarded: `k` bound to `"PATH"` |
| `dynamic-key-rebound` | guarded: `k` bound twice |

## 4. Result and control

Fifty-nine frozen cases: the forty-seven round-75 cases carried byte-identically (the
instrument refuses a set whose held prefix differs from
`.ufo/waves/round-75/controls/c2-cases-r75.json`, sha256 `d99502ba…`) plus the twelve above.
Candidate 59/59; held round-75 classifier 55/59, missing exactly the four new positives.
Population unchanged — 20 files, 13 readers, 13 guarded, 0 unguarded — the new rules do not
cancel a single real guard.

## 5. Declared limits

- Line order is not execution order; the same cross-method approximation the attribute flow
  already declares.
- The callee is matched by name to a local function and the cancellation follows the argument
  bound to the *deleted parameter* (by position or keyword), never a fixed position; a function
  alias, a method call, a `functools.partial`, or a chain of calls is not followed.
- The callee's delete key is a literal or a module constant, not a dynamic key.
- D3 is modelled in the env-named/subscript carrier flows. The attribute flow
  (`self.env[...]`) and the `os.environ` transport flow keep their own, narrower cancellation
  rules.
- The census is a syntactic approximation; it does not interpret values, so
  `env[KEY] = "0"` counts as a store even though the value is not a guard.

## 6. Recheck

Re-run the C2 command in `.ufo/waves/round-76/claims-declaration-r76.md`; exit 0 and the
contract line above are the pass condition. Control set: `controls/c2-cases-r76.json` sha256
`df9e8984…`.

Sources: S453 (subscription deletion is passed to the primary object), S454 (the copy
constructor carries keyword pairs), S455 (an argument is placed in the parameter slot), S456
(deleting an unbound name raises `NameError`).
