# R76RevC2 — C2 adversarial review

Axes: mapping-identity correctness; lexical-scope correctness; frozen-control discrimination; bounded, reproducible evidence.

Reviewed frozen `quality/counters/c2-r76-shapes.py` at `cb713254ee9926e036e594312fdc61b57825526b`, its diff against the held round-75 counter at `c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf`, all twelve appended cases, and the committed measurement receipt. No repair or admission recommendation is made.

## Findings, by severity

### P2 — D3 loses which parameter receives the deleted mapping

Paths: `quality/counters/c2-r76-shapes.py:402-450`, consumers at `609-610` and `1022-1023` (frozen revision).

`cancelling_functions` accepts a deletion from **any** parameter, then retains only `fn.name`. `call_cancellations` cancels the caller's **first** argument regardless of the deleted parameter's position. This violates mapping identity even with a direct local function call and no aliases.

```python
def drop(m, other):
    del other["GIT_NO_REPLACE_OBJECTS"]
def run(repo):
    env = {"GIT_NO_REPLACE_OBJECTS": "1", "PATH": "/usr/bin"}
    other = dict(env)
    drop(env, other)
    subprocess.run(["git", "show", "HEAD:a"], env=env)
```

Expected `(reader=True, guard=True)`; observed `(True, False)`; held `(True, True)`. The original environment remains guarded; only its copy is mutated. Receipt case: `b-second-parameter`.

The inverse, `drop(other, env)` with `def drop(other, m): del m[KEY_LITERAL]`, actually deletes from the launched mapping, yet returns `(True, True)` instead of `(True, False)` (`b-second-parameter-inverse`). The inverse is a retained blind spot, not a regression relative to held. Together these demonstrate that D3 does not preserve the same-mapping invariant.

### P2 — D3 resolves function names across unrelated lexical scopes

Paths: `quality/counters/c2-r76-shapes.py:402-450`; whole-tree cancellation injection into each scope at `609-610`, `985-987`, `1022-1023`.

```python
def unrelated():
    def drop(m):
        del m["GIT_NO_REPLACE_OBJECTS"]
def drop(m):
    pass
def run(repo):
    env = {"GIT_NO_REPLACE_OBJECTS": "1", "PATH": "/usr/bin"}
    drop(env)
    subprocess.run(["git", "show", "HEAD:a"], env=env)
```

Expected `(True, True)`; observed `(True, False)`; held `(True, True)` (`d-nested-name-collision`). The nested deleting function is unreachable from `run`; Python resolves the call to the module's no-op function. The new rule indexes every nested function by bare name and treats a different function's call as cancellation. This is not the declared function-alias/call-chain limitation: the executed call is a direct `Name` call.

### P2 — D4 and D3 treat shadowed module key constants as live guard keys

Paths: `quality/counters/c2-r76-shapes.py:382-399`, `402-435`, `479-490`, `574-575`, `608-610`, `1018-1023`; `key_is_guard:717-721` consults module constant names without lexical parameter exclusion.

```python
k = "GIT_NO_REPLACE_OBJECTS"
def run(repo, k="PATH"):
    env = {"GIT_NO_REPLACE_OBJECTS": "1", "PATH": "/usr/bin"}
    del env[k]
    subprocess.run(["git", "show", "HEAD:a"], env=env)
```

Expected `(True, True)` for `run(repo)`; observed `(True, False)`; held `(True, True)` (`e-parameter-shadow`). The parameter shadows the once-bound module name, so this invocation deletes PATH, not the guard key. The same issue affects callee keys: module `K=KEY_LITERAL`, `def drop(m, K="PATH"): del m[K]`, and `drop(env)` produce the same wrong cancellation (`e-callee-parameter-shadow`). Neither case needs dynamic value interpretation: both defaults and the call are explicit. The new rules conflate a module binding with a distinct lexical binding.

### P2 — Producer shortcut bypasses D3 cancellation

Paths: `quality/counters/c2-r76-shapes.py:523-546`, `584-587`, `597-600`. `guard_producers` checks direct rebindings/deletes but not D3 call cancellations; an accepted producer then becomes a fresh guard construction.

```python
def drop(m):
    del m["GIT_NO_REPLACE_OBJECTS"]
def git_env():
    env = {"GIT_NO_REPLACE_OBJECTS": "1", "PATH": "/usr/bin"}
    drop(env)
    return env
def run(repo):
    env = git_env()
    subprocess.run(["git", "show", "HEAD:a"], env=env)
```

Expected `(True, False)`; observed `(True, True)` (`producer-callee-delete`). This is a retained false guarded classification, not a held-to-candidate regression. It bounds the new D3 coverage: the same direct cancellation recognized in the frozen caller cases is ignored inside an already-supported guard producer. No attribute carrier or function alias is involved.

## Required adversarial verdict matrix

All rows are readers. `yes`/`no` below denotes guarded. Full sources and exact tuples are preserved in the evidence files.

| Case | Expected | Observed | Right? |
|---|---|---|---|
| a-copy-rebound: callee rebinds parameter to `dict(m)` | yes | yes | yes |
| a-copy-argument: caller passes `dict(env)` | yes | yes | yes |
| b-other-mapping: caller passes separate `other` | yes | yes | yes |
| b-second-parameter: callee deletes second argument's copy | yes | no | **no** |
| c-dynamic-dead: once-bound key, delete in `if False` | yes | yes | yes |
| d-nested-name-collision: unrelated nested delete, live no-op | yes | no | **no** |
| d-nested-local-copy: nested callee deletes parameter copy | yes | yes | yes |
| d-attribute-copy: method deletes parameter copy | yes | yes | yes |
| e-parameter-shadow: dynamic module key shadowed by caller parameter | yes | no | **no** |
| e-callee-parameter-shadow: module key shadowed in callee | yes | no | **no** |

The attribute-copy result alone is not evidence of method analysis: `d-attribute-real-delete` removes the guard through `Cleaner().drop(env)`, yet is also classified guarded. Attribute dispatch is outside the frozen simple-call limitation, so this is a disclosed residual limitation, not an additional defect finding.

## Frozen positives really require delete handling

Executed the frozen classifier on all twelve appended controls: 12/12 match their labels. For each of the four positive cancellation cases, replaced AST `Delete` nodes with `Pass` in memory, preserving every other statement. This is an ablation, not a production edit.

| Case | Expected guarded | Candidate | Held | Candidate with delete ignored |
|---|---|---|---|---|
| callee-del-literal | no | no | yes | yes |
| callee-del-store | no | no | yes | yes |
| dynamic-key-del | no | no | yes | yes |
| dynamic-key-module-const | no | no | yes | yes |

Thus the four labels are genuine separators against the held/delete-ignoring behavior, not incidental failures from another source shape. This ablation does not exclude arbitrary name-based overfitting; it demonstrates dependence on deletion semantics for the actual classifier.

## Evidence and verification gaps

- Evidence directory: `.ufo/waves/round-76/w1/R76RevC2/`.
- `adversarial-receipt.json`: frozen revision, classifier digest, controls digest, all 13 adversarial sources/results and held comparisons, all twelve frozen results, and the four delete ablations.
- `adversarial-fixtures.json`: standalone source corpus, copied before scratch removal.
- `classifier-diff.txt`: actual frozen successor versus held classifier diff, obtained read-only from Git blobs.
- Execution: retrieved blobs with `git show`; compiled them in isolated Python namespaces with non-main `__name__`; invoked their actual `classify(source)` functions. Fixture programs themselves were not launched, and no Git fixture repository or other swarm runtime was created. Expected labels follow Python binding/mapping semantics; these are classifier probes, not production subprocess tests.
- Frozen controls SHA256 independently derived: `df9e89841ed560613d7a05ad50f345b2d6bbf0d8e40a98f51e8b8134492b3948`.
- Re-read committed `measurement-c2-r76.txt`: its final line reports `population=20 readers=13 guarded=13 unguarded=0 controls=59/59 base_controls=55/59 verdict=TARGET_MET`, revision `755b339f1f6ec18f45b494d40515aecdbe9ceb73`. That full census was **not** rerun here. The observed counterexamples do not falsify its finite 59-case arithmetic or prove an error in those 13 production readers.
- LSP unavailable: `read xd://lsp` returned `No such tool`. Definitions/callers were inspected through Python AST/source snapshots instead; no text search is presented as semantic reference proof.
- No resume, rerouting, saturation, or canonical-run implementation changed in this scoped counter review; those runtime contracts were not exercised.
- No tools installed/updated; no committed files repaired; scratch removed after preserving receipts.

## Self-evaluation

Accuracy 4/5: exact classifier outputs preserved; expected behavior inferred from explicit Python semantics, not fixture execution. Completeness 4/5: all five requested attack families, twelve controls, and four ablations covered; production census not re-executed. Clarity 4/5: concrete snippets and tuples, with retained versus regressed behavior separated; evidence JSON is verbose. Actionability 4/5: frozen line anchors and reproductions supplied, but no repair by assignment. Conciseness 4/5: findings require multiple snippets to distinguish independent causes. Overall 4.0/5. Highest-impact improvement for a future implementation assignment: retain lexical function/parameter identity and add these counterexamples to regression coverage. Would the user agree? The report provides falsification evidence without recasting finite target success as general correctness.
