# R76ScoutPopulation — C2 population re-derivation and reachability audit

Scope: seat R76ScoutPopulation, round 76, wave 1. Read-only; no lane gate executed; no
instrument, corpus, or committed lane file edited. Revs: freeze v2
`cb713254ee9926e036e594312fdc61b57825526b`, measurement `755b339f1f6ec18f45b494d40515aecdbe9ceb73`.
Artifacts: `w1/R76ScoutPopulation/population.md`, `w1/R76ScoutPopulation/reachability.md`,
`w1/R76ScoutPopulation/probe-d3-d4.txt`, `w1/R76ScoutPopulation/reachability-observed.json`.

## 1. Population re-derived from the freeze-rev bytes — matches the receipt

`git ls-tree -r --name-only cb713254… -- quality` filtered by `^quality/check-[^/]+\.py$` gives
**20** files; `git show cb713254…:<path>` for each, read byte-for-byte:

- **readers = 13** — exactly the 13 that contain the literal `GIT_NO_REPLACE_OBJECTS`; the same
  13 satisfy the counter's own `is_reader` predicate (`["']git["']` + quoted read verb). The XOR
  set between the two tests is empty, so the count does not depend on which predicate is used.
- **guarded = 13** — in every reader the occurrence is an assignment into an env mapping
  (dict literal, `env[KEY] = "1"`, or `dict(os.environ, KEY="1")`) and that mapping reaches a
  `subprocess.*` call as `env=`; verified at the call site for the three helper-style files
  (`git_env()` in check-freeze-order / check-tool-ledger / check-wave-done, `git_blob` in
  check-anchor-cover, `git()` in check-control-receipts). No reader only mentions the string.
- **unguarded = 0** — no reader's guard fails to reach a git call.

`population=20 readers=13 guarded=13 unguarded=0` reproduces
`.ufo/waves/round-76/measurement-c2-r76.txt` exactly; an independent `classify()` pass over the
same 20 blobs returns the same 20/13/13/0. Carried-set identity also re-checked independently:
47/47 round-75 cases present and field-identical, 12 appended, total 59.

Population-boundary observation (does not move any count): `quality/check-r38-discrimination.py`
invokes git six times (`clone`, `sparse-checkout`, `checkout`, `add`, `commit` at :163–:182) with
`ENV` lacking `GIT_NO_REPLACE_OBJECTS`, but never names the key, so it sits outside the reader
predicate. `unguarded=0` therefore means "no reader lacks a guard", not "no check invokes git
unguarded". `check-counter-discrimination.py` sets `GIT_DIR` only and runs no git argv.

Doc nit (recorded, not edited — the file is frozen at sha256 `df9e8984…`): the control file's
`note` says "thirteen appended", but 12 names are appended (3 interprocedural cancellations + 1
dynamic-key delete + 8 negatives = 12; 47+12=59). The declaration table and counts are consistent
at 12.

## 2. Reachability of the twelve — 11/12 reach a launch; one is an M75-3 recurrence

Each `src` was executed with a stubbed `subprocess` recording `(argv, env)`, then `run("repo")`:

- 11 of 12 reach a single git launch and the guard-key state at that launch matches the frozen
  label. The four `expect_guard=False` positives really do launch without the key; the eight
  negatives really do launch with it.
- **P2 — `callee-del-param-rebound` cannot execute as written.** `drop()` rebinds `m` to a fresh
  `{"PATH": …}` and then deletes `GIT_NO_REPLACE_OBJECTS`, raising `KeyError`; no launch is
  reached (0 observed). Its `guarded` label is a counterfactual about the caller's mapping, i.e.
  the round-75 **M75-3** class ("a fixture whose source cannot execute as written"). The round-75
  closure's repair ("the successor shape initialises the key before the delete") was applied to
  the carried `del-before-store` family but not to this newly appended case. Harm is bounded: the
  held counter also says `guarded`, so this case is not one of the four producing
  `base_controls=55/59`; the 59/59 score is unaffected.
- **P3 — two pins are constant-folds/liveness, not reachability analysis:**
  `callee-del-dead-branch` is proved guarded by folding a literal `if False:` (a non-literal
  `if flag:` is treated as cancelling); `callee-never-called` and `callee-called-after-launch`
  are liveness/ordering facts; `dynamic-key-rebound` agrees with both the "bound exactly once"
  rule and a runtime last-binding reading, so it discriminates neither. None of these labels is
  wrong about the reachable launch.

## 3. D3/D4 false-positive risk — latent channels confirmed, not realised in the scored set

The four `expect_guard=False` positives are true positives: each reaches one launch, the launch's
mapping is the same name the callee/dynamic delete targets, and no copy or rebind intervenes. A
copy at the call site (`drop(env.copy())`) is correctly not credited, and a delete placed before
the store is correctly dominated. But the shipped rule has three confirmed false-positive
channels, none exercised by any of the 59 frozen cases (probes T2/T4b/T4c/T5 in
`probe-d3-d4.txt`):

1. **Callee receives a different argument.** `cancelling_functions` marks a function cancelling
   when *any* parameter is deleted from, while `call_cancellations` credits the *first* positional
   argument. `drop(env, other)` with `def drop(m, extra): del extra[KEY]` cancels `env`, though
   the callee deleted `other` → rule says unguarded, runtime state guarded.
2. **A mapping that is not the one launched.** `alt = dict(env); drop(env); run(env=alt)` — the
   launched copy still carries the key, but the rule records the delete against `env` and reports
   unguarded (`mapping_has_key` does not treat `dict(env)` as carrying the key).
3. **Cross-scope name collision.** `call_cancellations(tree, …)` walks the whole tree and its
   result is merged into every scope's `rebinds` by bare name, so a cancelling call on a
   same-named local in a nested function, landing between another scope's guard and launch lines,
   cancels that scope's guard.

Also over-approximated as designed (declared limit, untreated): a non-literal conditional delete
(`if cond: del env[k]`, or the same inside a callee) cancels unconditionally; "guarded" is a
per-file property, so a guarded first launch plus an unguarded second launch after the cancel
counts guarded. Coverage gaps left open by the twelve appended cases: caller-side copy launched
after the cancel, multi-parameter callee, sibling-scope same name, non-literal conditional
deletes, second launch, and caller-side rebinding to another guarded literal before the launch.

## Confidence

High on counts (bytes and two independent idioms agree) and on the runtime table (executed, not
inferred). High on the three false-positive channels (reproduced through the shipped
`classify()`); medium on their practical reach, since the census is declared a syntactic
approximation and no frozen case or score depends on them. High on the M75-3 recurrence in
`callee-del-param-rebound` (KeyError observed, zero launches recorded).

## Remaining unknowns

- Whether the round-75 closure intended the "initialise the key before the delete" repair to cover
  callee-side rebound mappings; no text states it, and the frozen case cannot be re-cut mid-round.
- Whether any future round wants "unguarded" to mean "any launch unguarded" (per-launch) rather
  than "no guarded launch exists"; the frozen target does not say.
