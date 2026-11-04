---
source: S447 (CPython 3.14.8 language reference, the `global` statement), S448 (`os.environ`), S449 (`subprocess.run` `env`); own-work — `.ufo/waves/round-73/{claims-declaration-r73.md,controls/c2-cases-r73.json,control-baseline-r73.txt,measurement-c2-r73.txt}`
verified-at: `1459cca11fb5d3956a6e9a128217852dd0c28cb9` (round-73 census; measurement in `.ufo/waves/round-73/measurement-c2-r73.txt`)
recheck: `python3 -I quality/counters/c2-r73-shapes.py --repo . --rev <rev> --base-rev d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce --controls .ufo/waves/round-73/controls/c2-cases-r73.json --scratch-root DIR` — `controls=28/28 base_controls=25/28 verdict=TARGET_MET`
---

# Two guard carriers the census did not count: the global-declared store and the mutated process environment (round 73, C2)

## 1. The ground

The lane's guard census asks one question of every `quality/check-*.py` file that reads git
objects: does the environment handed to the child carry `GIT_NO_REPLACE_OBJECTS`? Its answer is
what makes the object reads replacement-proof, so a carrier it does not count is a real check
script that looks guarded and is not.

Three sourced sentences define the two carriers this round adds:

| row | sentence (located) | what it grounds |
|---|---|---|
| S447 | "The global statement causes the listed identifiers to be interpreted as globals." (simple_stmts.rst:972-973) | a store inside a function that declares the name `global` binds the **module** mapping, so the guard it writes is the guard a later `env=NAME` hands over |
| S448 | "Changes to the environment made after this time are not reflected in os.environ, except for changes made by modifying os.environ directly." (os.rst:193-194) | only a store **into** `os.environ` updates the mapping — an inherited environment or a `putenv` is not the same object, so the store is the guard |
| S449 | "a mapping that defines the environment variables for the new process" (subprocess.rst:88-90) | a non-None `env` mapping is the child's whole environment, so a copy of `os.environ` carries the stored key to the child |

## 2. Carrier A — the global-declared guard

```python
ENV = {"PATH": "/usr/bin"}

def setup():
    global ENV
    ENV["GIT_NO_REPLACE_OBJECTS"] = "1"

def run(repo):
    setup()
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env=ENV)
```

The round-71 classifier scores this **unguarded**: its name flow is scope-local, the module
binding carries no key, and the store lives in a different function. The round-73 detector
requires three facts: the store sits in a function that declares the name `global`; the key is a
literal or a module constant; the git launch's `env=` is that same name at a **later line**. A
plain replacement of the name between store and launch (`ENV = {}` at module level or in another
global-declaring function) cancels the store.

## 3. Carrier B — the mutated process environment

```python
def run(repo):
    os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"
    subprocess.run(["git", "-C", repo, "show", "HEAD:a"], env={**os.environ})
```

and its `env=dict(os.environ)` spelling. The store is an attribute subscript on `os.environ`
(key literal or module constant); the launch's `env=` is one of exactly two copy forms — a
single-key dict-splat of `os.environ`, or a `dict(os.environ)` call with no keyword — at a later
line. A store after the call, a `dict(os.environ, EXTRA="1")` call, and a dead-branch store are
all refused (frozen negatives).

The held classifier already counted `env=os.environ` directly (the attribute flow matches the
dotted name) and refused the copy forms: the copy is a different expression, and `mapping_has_key`
does not follow an attribute into a dict-splat.

## 4. Measurement

| quantity | held round-71 classifier | round-73 classifier |
|---|---|---|
| frozen cases | 25/28 | 28/28 |
| population / readers / guarded / unguarded | 20 / 13 / 13 / 0 | 20 / 13 / 13 / 0 |

The three held misses are exactly the three new positives (`global-rebind-guard`,
`environ-splat-guard`, `environ-call-guard`); the two new negatives and the twenty-three carried
cases score the same on both. The census population is unchanged — the new shapes are carriers a
script may use, not new scripts.

## 5. Bounds (declare them, do not footnote them)

- **Line order, not execution order.** A store in a function that the launch never calls, or
  calls later, still counts if its line precedes the launch. This is the attribute-flow
  approximation the lane already carries; the `r73-global-rebind-replaced-between` regression pins
  the replacement half only.
- **One declaration hop.** The name must be declared `global` in the storing function itself;
  a module-level store or a closure over a mutable default is not followed.
- **One `os.environ` store, two copy spellings.** `{**os.environ}` and `dict(os.environ)`; a
  `**` of a module mapping together with `os.environ` is the held splat carrier, not this one.
  An alias of `os.environ` (`e = os.environ; e[KEY] = "1"`) is not followed.
- **No value interpretation.** The census reads syntax; a store whose value is "0" counts the
  same as "1".

## 6. Why it matters

A check script that mutates `os.environ` and copies it, or that centralises its env setup behind
`global`, is guarded in fact. Counting it unguarded is a false negative that would push a real
guard toward a mechanical rewrite; refusing the copy forms also keeps the census from accepting
`env=dict(os.environ, EXTRA="1")`, which is not a copy. Both directions are pinned as frozen
negatives.
