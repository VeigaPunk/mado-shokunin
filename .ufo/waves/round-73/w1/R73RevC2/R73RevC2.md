# R73RevC2 — C2 adversarial review

Axes: frozen-claim fidelity; lexical/environment soundness; carry-forward integrity; reproducibility; scope/no-harm.

Reviewed instrument commit `1459cca11fb5d3956a6e9a128217852dd0c28cb9`, base `d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce`. Recommendation only, not an admission. No production edits or tool installations.

## Findings (severity first)

### F1 — Medium: global carrier accepts a shadowed launch binding

`quality/counters/c2-r73-shapes.py:936–945` matches `env=NAME` by spelling, without establishing that this use resolves to the module binding. `false-global-parameter-shadow.py` has `global ENV` in setup, but `run(repo, ENV=None)` receives a distinct empty dictionary. `classify()` returns `(True, True)`; executing `run('repo', {})` with a capture-only subprocess object observes `env={}`, without the guard. This is lexical scope confusion, not cross-function execution-order uncertainty. The early success at lines 443–444 bypasses held scope checks.

Repro: classify the adjacent fixture with the preserved reviewed instrument (command below). Expected guard false; observed true. Resolve the launch binding before crediting the global carrier, and add a parameter-shadow negative control in any future, separately frozen corpus.

### F2 — Medium: unrelated local assignment cancels a genuine global guard

`quality/counters/c2-r73-shapes.py:928–935` gathers replacement assignments from every scope, although the documented cancellation at lines 18–20 is module-level or another global-declaring function. `true-global-unrelated-local-rebind.py` declares/stores global ENV in setup, then defines an unrelated, uncalled function with local `ENV = {}`. `run()` calls setup and launches with the module ENV. `classify()` returns `(True, False)`; capture observes `{'GIT_NO_REPLACE_OBJECTS': '1'}`. The unrelated local cannot replace that module binding.

Repro: adjacent fixture; expected guard true, observed false. Restrict cancellation to assignments resolving to that global binding. This counterexample uses one global declaration and the required source-line ordering, so the declared line-order limit does not explain it.

### F3 — Medium: environment-key deletion is accepted as guarded

`quality/counters/c2-r73-shapes.py:968–987` tracks Assign stores and whole `os.environ` replacement only. It ignores `del os.environ[KEY]`. `false-environ-key-deleted.py` stores the guard, deletes it, then launches with exactly `dict(os.environ)`. `classify()` returns `(True, True)`; capture observes `{}`. This is a same-function, straight-line invalidation, independent of values or alias-chain limits.

Repro: adjacent fixture; expected guard false, observed true. Credit requires a surviving key at copy time; a future corpus should explicitly specify deletion handling rather than treating 28/28 as semantic soundness.

### F4 — Informational: declared line-order approximation is observable in both directions

- `true-global-reverse-definition-order.py`: run calls setup before launch, but setup's definition is textually later. `classify() == (True, False)`; captured child environment contains the guard.
- `false-environ-uncalled-store.py`: an uncalled earlier helper stores into `os.environ`; run copies the actual empty environment without calling it. `classify() == (True, True)`; captured child environment is empty.

These are demonstrated residual limits, not grounds to reject the frozen finite target. Both new detectors use whole-tree AST traversal and compare source line numbers, not dynamic dominance. Do not describe this census as proof that every git reader executes with the guard.

## Reproduction and evidence

All five programs are original for this review: each was checked unequal to every frozen control source and every embedded regression source. Their complete source files, `attack-results.json`, `carry-forward.json`, `population.json`, `reviewed-c2-r73-shapes.py`, and `reviewed-c2-cases-r73.json` are adjacent to this report. Attacks were executed only with fresh in-memory fake `os.environ` dictionaries and a capture-only `subprocess.run`; no actual child git command was launched by an attack.

From this report's directory, classification can be reproduced without importing fixtures as executable modules:

```sh
python3 -I -c 'import pathlib,runpy; m=runpy.run_path("reviewed-c2-r73-shapes.py"); [(print(p.name,m["classify"](p.read_text()))) for p in sorted(pathlib.Path(".").glob("true-*.py")) + sorted(pathlib.Path(".").glob("false-*.py"))]'
```

Frozen command was executed using the script and controls extracted directly from the instrument commit, with absolute repo/controls paths and explicit scratch `/fast/scratch/hyaku/mado-r73/R73RevC2`. Observed exit 0 and exact last line:

```text
MADO_R73_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=28/28 base_controls=25/28 verdict=TARGET_MET rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9
```

Its `--selftest --controls <extracted-controls> --scratch-root <seat-scratch>` also exited 0:

```text
MADO_R73_GUARD_SHAPES_SELFTEST: 75/75 assertions passed
```

The committed measurement and pre-freeze baseline receipts were reread, not rewritten. Re-execution agrees with their finite measurements; F1–F3 do not falsify 28/28 on the frozen set.

## Carry-forward and population

Independent committed-object extraction found round-71 controls SHA-256 `d7814de8815bb0d4146ceed612ddd3e03029763b7cbf769d868a96ce5cefe7df`, 23 cases. Every whole case object equals the corresponding first 23 entries of the new set, including exact source strings and expected booleans. New-set SHA-256 is `65e9464450d58f803ca626f7b7ce6bc4712f46710ac5707602601cee9ecf230d`.

Loaded the held classifier from the base commit, not the working tree. It scores 25/28; its complete miss list is exactly `global-rebind-guard`, `environ-splat-guard`, `environ-call-guard`. The candidate scores all 28. Thus the two new negative controls remain refused by both classifiers; frozen bypass cases also remain refused.

Independently enumerated all committed tree paths via read-only `git ls-tree`, selected `quality/check-[^/]+\.py`, extracted and classified every member: **population=20, readers=13, guarded=13, unguarded=0**. `population.json` records all 20 paths and classifications. Canonical `measure()` logic is at lines 1138–1169: counts are classification results, and TARGET_MET is the finite conjunction at lines 1002–1005, not universal soundness.

## Residual risk and verification gaps

LSP device unavailable: reading `xd://lsp` returned “No such tool”; no semantic references/definition/diagnostics service was available. Evidence here is committed-source inspection and concrete Python execution, not grep presented as semantic proof. This seat reviewed C2 only; no general repository verification or unrelated runtime/rerouting/resume claims were exercised. No universal saturation claim is justified by this finite grammar and set. Scratch was removed after preserving cited artifacts in this directory.

The requested flat trailer path conflicts with the explicit only-write-directory bound; this report is intentionally inside the allowed seat directory.

## Self-evaluation

Accuracy 4/5: concrete captured environments and pinned objects; child Git itself was deliberately not executed for attack programs. Completeness 5/5: frozen command/selftest, five unseen attacks, carry-forward, held misses, and full population re-derivation covered. Clarity 4/5: findings separate finite claim from semantic soundness, though reproduction is split across adjacent files. Actionability 4/5: exact loci and repro sources supplied; no fixes authorized. Conciseness 4/5: evidence artifacts prevent duplicating five source listings. Mean 4.2/5. Highest-impact improvement for subsequent authorized work: separately freeze scope-shadow, scope-cancellation, and key-deletion controls. Would the user agree? The finite target is confirmed without concealing three actionable soundness defects.
