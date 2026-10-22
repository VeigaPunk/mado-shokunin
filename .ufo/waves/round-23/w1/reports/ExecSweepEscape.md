# ExecSweepEscape — C1 item: remove the redundant callback sweep only where it is provably safe

Seat: `MadoR23.ExecSweepEscape` (executor, leaf). Lane tip `a28e4815aabfa85f55274884000fb2608355f8cf`,
base classifier `tools/mado-tripwire.py` SHA256
`cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`.

Deliverables (all under `.ufo/waves/round-23/w1/out/ExecSweepEscape/`):

| file | what it is |
|---|---|
| `candidate.patch` | `git diff a28e4815aabfa85f55274884000fb2608355f8cf -- tools/` (198 lines, 164 insertions, 2 deletions, one file) |
| `candidate-tool.py` | the candidate classifier bytes, sha256 `3daf01e34467942f71ff8c5fb9547e0fa797c5a6a7cedf2a7a5501b965ecae8d` |
| `base-tool.py` | the base classifier bytes (`git show a28e481…:tools/mado-tripwire.py`), sha256 `cd9da20c…` |
| `guards.json` | every guard command, its exact argv, its exit and its raw result |
| `design-note.md` | the rule, its implementation and its limits |

Clone: `/fast/scratch/hyaku/mado-r23/ExecSweepEscape`, branch `round-23/exec-sweep-escape`, commit
`f860c1e8834397bcf42309c121d7630ef32cb7dc` ("round-23: skip a callback sweep only when the consumer
cannot let it escape"). Nothing was pushed; the lane's git index, jj state and working copy were not
touched.

## Verdict

**The item is implemented and every no-harm guard holds.** The escape-gated rule replaces round 22's
withdrawn v3 suppression: a callable argument is no longer swept when the followed consumer's body
provably cannot let it escape, and it is still swept for every escape form. The four repair cases this
item owns (`ForwarderPassesCallerArgument`, `ForwarderInvokesFactoryClosure`,
`ReturnedGlobalCallableShadow`, `ForwardExistingClosureWithoutFrameContamination`) go from red to green,
and the two recall guards (`CallbackStoredInDict`, `CallbackStoredOnAttribute`) keep their rows.

**The round-23 repair counter is 10/12 for this candidate, not 12/12.** The two remaining failures,
`ForwarderInvokesCallback` and `CallerLocalShadowsHelperGlobal`, are the caller-frame leak (H4): they
report a false `observed` host mutation (`pacman -S r23-forward-foreign`,
`pacman -S r23-local-foreign`) that the follow produces because `follow_helper` starts the callee
body from the caller's environment snapshot instead of the callee's defining frame. That is the
frame-environment item, not this one; this change removed the *redundant sweep* from
`ForwarderInvokesCallback` (its unparsed count is now 0), but it cannot remove a false `observed` row
that a follow produces. I did not touch the frame logic: it is another seat's item and the two patches
would overlap.

## The rule, in one paragraph

For a consumer call of a visible helper that the scan **followed** with **no unparsed row** and whose
body contains no opaque statement, each argument of that call is classified by how the consumer's
body uses the receiving parameter:

* **never read** in the body (nested defs and lambdas included, shadowing respected) → the consumer
  cannot reach the value → the later sweep is **skipped**;
* **read only as the direct call target `param(...)`** of calls that were themselves followed with
  zero unparsed → the callback's execution is already accounted for → the sweep is **skipped**;
* **read only as a returned value** → the sweep is skipped **only when the body it was bound to was
  itself followed with zero unparsed** (the returned-callback case; the return is *shown* to be
  followed, not assumed);
* **anything else** — a store into a subscript or an attribute, a `global`/`nonlocal` declaration, a
  container literal, a `return`, a `yield`, an alias assignment, a pass-on as an argument, a
  `*args`/`**kwargs` capture, a `locals()`/`vars()`/`globals()` read → the sweep is **kept**.

A nested scope that binds the name itself (its own parameter, an assignment, a `global`/`nonlocal`
statement) shadows it and is not counted as a use of the consumer's parameter. A starred argument,
an unknown `**kwargs`, a consumer that was not followed, a consumer whose follow produced an unparsed
row and a body with an opaque statement all leave the sweep in place.

Implementation: four helpers (`consumer_body`, `bound_param_names`, `scope_binds_name`,
`parameter_escape`) plus `note_consumer_args`, called from `spawn_scan` right after a consumer is
followed; `new_scan_context()` gained `clean_calls`, `clean_bodies`, `safe_args`, `returned_args`.
The reference loop in `spawn_scan` skips `sweep_body` for an argument node in `safe_args`, and for an
argument whose returned body is in `clean_bodies`. Full detail in `design-note.md`.

## What the four owned repair cases measured

`python3 -I .ufo/waves/round-23/repair/measure.py --tool <candidate>` (one child per case, 384 MiB,
15 s, via the unchanged round-21 oracle scan helper):

| case | base | candidate |
|---|---|---|
| `ForwarderPassesCallerArgument` | red (`unparsed_spawns 1`, row correct) | **pass** — `package_query pacman -Q r23-forwarded-argument observed`, unparsed 0 |
| `ForwarderInvokesFactoryClosure` | red (`unparsed_spawns 1`, row correct) | **pass** — `package_query pacman -Q r23-closure-captured observed`, unparsed 0 |
| `ReturnedGlobalCallableShadow` | red (foreign lead `pacman -S r22-foreign-callable`) | **pass** — only `package_query pacman -Q r22-global-callable observed` |
| `ForwardExistingClosureWithoutFrameContamination` | red (`unparsed_spawns 1`) | **pass** — `package_query pacman -Q r22-forward-global observed`, unparsed 0 |
| `CallbackStoredInDict` | pass (lead) | **pass** (lead kept) |
| `CallbackStoredOnAttribute` | pass (lead) | **pass** (lead kept) |
| `ForwarderInvokesCallback` | red (false observed + unparsed 1) | still red — false observed only, **unparsed now 0** |
| `CallerLocalShadowsHelperGlobal` | red (false observed) | still red — false observed only |

Base counter 6/12 → candidate 10/12.

The returned-callback case is the one the assignment asked me to handle only if the return can be
*shown* to be followed. It can: `forward` returns its `callback` parameter, `job = forward(...)` binds
the result, `job()` resolves to the same body and the scan follows it with zero unparsed
(`FOLLOW run depth=0 -> ([('package_query', 'pacman:-Q', 'pacman', 'pacman -Q r22-forward-global')], 0)`
in the traced run). The sweep is therefore skipped and the case passes. Where the returned body is
never followed the sweep is kept — probe M below shows `pacman -S pM` still reported as a lead.

## Discrimination, measured

Thirteen probe fixtures (scratch only, not committed; source below) run through the candidate with
`follow_helper`/`sweep_body` traced, to show the rule separates the escape forms instead of
suppressing sweeps wholesale:

```python
A_store_dict       def consumer(cb): hooks["k"] = cb          -> sweep KEPT   -> lead pacman -S pA
B_pass_on          def consumer(cb): sink(cb)                  -> sweep KEPT   -> lead pacman -S pB
C_unbindable_arg   def consumer(cb): cb(makeup())              -> sweep KEPT   -> unparsed 2, no row
D_never_read       def consumer(cb): return 1                  -> sweep SKIPPED-> no row (body never runs)
E_clean_call       def consumer(cb): cb(["pacman","-Q","pE"])  -> sweep SKIPPED-> observed pacman -Q pE
F_yield            def consumer(cb): yield cb                  -> sweep KEPT   -> lead pacman -S pF
G_alias            def consumer(cb): alias = cb                -> sweep KEPT   -> observed pacman -S pG
H_locals           def consumer(cb): print(locals())           -> sweep KEPT   -> lead pacman -S pH
I_container        def consumer(cb): box = [cb]                -> sweep KEPT   -> lead pacman -S pI
J_attr_store       def consumer(cb): box.cb = cb               -> sweep KEPT   -> lead pacman -S pJ
K_nested_def_call  def consumer(cb): def inner(): cb(); inner()-> sweep SKIPPED-> observed pacman -S pK
L_return_then_call def consumer(cb): return cb  (+ job())      -> sweep SKIPPED-> observed pacman -S pL
M_return_uncalled  def consumer(cb): return cb  (never called)  -> sweep KEPT   -> lead pacman -S pM
```

Each probe body is a `def run(): subprocess.run([...])` (or `run(actual)`) handed to `consumer(run)`
in a module that imports only `subprocess`; the literal argv is the only difference between the
probes. The probe files are in `/fast/scratch/hyaku/mado-r23/probe/`, the tracer in
`/fast/scratch/hyaku/mado-r23/dbg.py` (it loads the candidate as a module and wraps `sweep_body` and
`follow_helper`; it never executes fixture content).

## Guards — every command, sequentially, one child at a time

All of these ran from `/home/vgpnk/Projects/shokunin/mado-shokunin` (the lane) with `--tool` pointing
at `.ufo/waves/round-23/w1/out/ExecSweepEscape/candidate-tool.py`, whose bytes are identical to the
clone's `tools/mado-tripwire.py` (sha256 `3daf01e3…`). The lane's harnesses
(`round-22/replay.py`, `round-22/resource-closure-measure.py`) refuse a `--tool` outside the
repository, so the in-repo copy was used for every guard that goes through them; the eleven selftest
suites were run with the same in-repo copy (they only need the suite directory, which is in the
clone), and the precision counter ran inside the clone, reading the tool bytes from the clone's own
commit `f860c1e…`. Raw results are in `guards.json`.

| # | guard | command | result |
|---|---|---|---|
| 1 | round-23 repair set | `python3 -I .ufo/waves/round-23/repair/measure.py --tool <candidate>` | **10/12** (base 6/12); the two reds are the caller-frame leak, see above |
| 2 | round-22 residual truth | `python3 -I .ufo/waves/round-22/residual-truth/measure.py --tool <candidate>` | **4/4** (base 2/4) — the H3 harm is gone: `ReturnedGlobalCallableShadow` loses its foreign lead, `ForwardExistingClosureWithoutFrameContamination` loses its unparsed row |
| 3 | round-22 primary oracle | `python3 -I .ufo/waves/round-22/oracle/measure.py --tool <candidate>` | **57/57** |
| 4 | round-21 oracle replay | `python3 -I .ufo/waves/round-22/replay.py --tool <candidate> --mode oracle` | **primary 35/35, supplemental 17/17** |
| 5 | eleven legacy selftest suites | `prlimit --as=402653184 --cpu=15 python3 -I <candidate> --selftest .ufo/waves/<suite>` for the eleven suites of `round-22/evidence/resume/legacy-selftests-summary.json` | **247/247**, every suite exit 0 (`9,16,33,30,1,31,45,34,17,13,18`) |
| 6 | whole-corpus comparator | `python3 -I .ufo/waves/round-22/replay.py --tool <candidate> --mode corpus --before-tool <base-tool.py>` | **1356 files, 1356 runs before and after, byte-identical run records; `added_or_relabelled` = [], `removed_or_relabelled` = [], error flips = 0** (107 pre-existing `CouldNotEvaluate` entries, identical before and after) |
| 7 | resource populations | `python3 -I .ufo/waves/round-22/resource-closure-measure.py --tool <candidate> --mode module-main` and `--mode cli`; `python3 -I .ufo/waves/round-21/resource/measure.py --tool <candidate> --mode module-main` and `--mode cli` | every case exit 0, no timeout, empty stderr, verdict `clean` under 384 MiB / 15 s (round-22 closure: stored-closures 512/1024/2048, 0.079–0.254 s, max RSS 20824–32132 KiB module-main and 30384–42500 KiB cli; round-21: assignments 1000/2000/4000, 0.038–0.098 s, max RSS 19044–29724 KiB module-main and 29540–38380 KiB cli) |
| 8 | precision | `python3 -I <clone>/.ufo/waves/round-20/tw-precision.py f860c1e8834397bcf42309c121d7630ef32cb7dc` (run from the clone) | **166/175** (P 66/66, S 17/17, W 21/22, H 47/52, L 15/18) with the **identical failing-name set** as the base commit `a28e481…` (also 166/175, same nine names): no passing case lost, none gained |

Guard 6 lists every added/removed finding group and error flip explicitly because there are none:
`added_or_relabelled: []`, `removed_or_relabelled: []`, and the 107 `errors` entries compare equal
before and after (the same `CouldNotEvaluate` inputs: an invalid JSON line, refused file names, and
the like). The per-file run records for all 1356 files are identical before and after.

## Critic neighbour cases (L1's extra input)

`CritEscapeNeighbour/run.py` was copied (byte-identical, `runner_sha256`
`28f4055042800d8c03d53c83c5c36b67479450f041e92ee4e407132e6c6c73aa`) to a scratch tree at the same
depth below a repository root so that its own `LANE = ROOT.parents[5]` still resolves, with the
round-21 helper symlinked in; the copy writes its `cases.json` there, so the critic's own file was
not touched.

| case | base | candidate | why |
|---|---|---|---|
| `EscapeListAppendThenCalled` | unparsed 1, no rows | **unchanged** (unparsed 1, no rows) | `hooks.append(callback)` is a container store, an escape, so the sweep is kept; the sweep still cannot resolve the module-global `argv`, and `list.append` is a pure consumer, so the callback is not otherwise reachable |
| `EscapeSecondForwarder` | false observed `pacman -S r23x-chain-inner-foreign` + unparsed 1 | **unchanged** | the false observed row is the frame leak; the unparsed comes from the redundant sweep of `run`, which survives because `outer` passes the callback on as an argument — an escape under the assigned rule |
| `EscapeTupleNestedClosureLater` | silent miss (no rows, unparsed 0) | **unchanged** | needs a tuple-returning factory to be resolved and unpacked (`callback, _ = pair`); no part of this rule touches factory/tuple resolution |

So this candidate is a **no-op on all three neighbour cases**; it neither fixes nor breaks them.

Two consequences worth the L1's attention:

1. `EscapeSecondForwarder` can only pass if the frame fix also gives the *sweep* its own defining
   frame. Under the assigned rule the redundant sweep of `run` survives (`outer` passes the callback
   on as an argument). With a defining-frame fix, that surviving sweep resolves `argv` to the module
   global and yields a duplicate `pacman -Q r23x-chain-global` **lead**, which the same-command dedup
   (`mado-tripwire.py:2883`, "a same-command `lead` is dropped when the same tool call already has it
   `observed`") drops against the observed row — leaving the case exact-rule clean. Without that, the
   unparsed count stays 1 and the case stays red. A compositional refinement of the rule (treating a
   pass-on to a *visible, cleanly followed* consumer as non-escape) would remove the sweep outright,
   but that goes beyond the assigned rule, so I did not take it.
2. `EscapeListAppendThenCalled` and `EscapeTupleNestedClosureLater` are pre-existing recall gaps (the
   sweep's environment does not carry module globals; a tuple-returning factory is not resolved).
   Fixing them is not safe inside this item: giving the sweep the module environment would add
   `lead` rows all over the corpus, and resolving tuple factories changes factory semantics. I left
   both alone.

## Risks

* **The `unused` class drops a `lead` row** that the old sweep produced for a callback the consumer
  ignores. That is correct when the consumer is the only reference: the body cannot run. It would be
  wrong only if the callback is reached by a path the scan does not model (a `globals()` lookup, a
  C-level registration). The corpus comparator found no such instance in 1356 files, and the
  `locals()`/`vars()`/`globals()` escape keeps the sweep for a consumer that uses them.
* **The `call` class trusts the follow.** When the consumer calls the callback and the scan followed
  that call with no unparsed row, the follow's rows stand in for the body. This matches the tool's
  established semantics (a followed body is not swept) but it does mean a row on a branch the follow
  did not take is not reported. The rule refuses to fire whenever the follow had any unparsed row.
* **Ordering.** The `returned` class is decided in the reference loop, after every call of the cell is
  known, so a returned body followed later in the same cell is recognised; a returned body followed in
  a later cell is not, and the sweep is kept (conservative).
* **Overlap with the frame-environment seat.** Both patches touch `spawn_scan`/`follow_helper`
  territory. My patch adds four helpers and touches two call sites (the follow in `spawn_scan` and
  the reference loop); it does not change `follow_helper`, the environment construction or the sweep
  environment. A merge should be straightforward, but the L1 should re-run guard 6 after combining.
* The candidate is a single-file change to `tools/mado-tripwire.py`; nothing else in the repository
  was modified, and no harness, fixture, expectation or document was touched.

## Commands actually run (exact)

```bash
# clone and candidate
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r23/ExecSweepEscape
cd /fast/scratch/hyaku/mado-r23/ExecSweepEscape && git checkout -b round-23/exec-sweep-escape
#   (edit tools/mado-tripwire.py, then)
git add tools/mado-tripwire.py && git -c user.name=mado-shokunin -c user.email=mado@shokunin.local \
    commit -m "round-23: skip a callback sweep only when the consumer cannot let it escape"
git -C /fast/scratch/hyaku/mado-r23/ExecSweepEscape diff a28e4815aabfa85f55274884000fb2608355f8cf -- tools/ \
    > .ufo/waves/round-23/w1/out/ExecSweepEscape/candidate.patch

# guards (all sequential, one child at a time; raw results in guards.json)
python3 -I .ufo/waves/round-23/repair/measure.py --tool .ufo/waves/round-23/w1/out/ExecSweepEscape/candidate-tool.py
python3 -I .ufo/waves/round-22/residual-truth/measure.py --tool .ufo/waves/round-23/w1/out/ExecSweepEscape/candidate-tool.py
python3 -I .ufo/waves/round-22/oracle/measure.py --tool .ufo/waves/round-23/w1/out/ExecSweepEscape/candidate-tool.py
python3 -I .ufo/waves/round-22/replay.py --tool .ufo/waves/round-23/w1/out/ExecSweepEscape/candidate-tool.py --mode oracle
python3 -I .ufo/waves/round-22/replay.py --tool .ufo/waves/round-23/w1/out/ExecSweepEscape/candidate-tool.py \
    --mode corpus --before-tool .ufo/waves/round-23/w1/out/ExecSweepEscape/base-tool.py
prlimit --as=402653184 --cpu=15 python3 -I .ufo/waves/round-23/w1/out/ExecSweepEscape/candidate-tool.py \
    --selftest .ufo/waves/round-17/tripwire/core            # …and the other ten suites
python3 -I .ufo/waves/round-22/resource-closure-measure.py --tool .ufo/waves/round-23/w1/out/ExecSweepEscape/candidate-tool.py --mode module-main
python3 -I .ufo/waves/round-22/resource-closure-measure.py --tool .ufo/waves/round-23/w1/out/ExecSweepEscape/candidate-tool.py --mode cli
python3 -I .ufo/waves/round-21/resource/measure.py --tool .ufo/waves/round-23/w1/out/ExecSweepEscape/candidate-tool.py --mode module-main
python3 -I .ufo/waves/round-21/resource/measure.py --tool .ufo/waves/round-23/w1/out/ExecSweepEscape/candidate-tool.py --mode cli
cd /fast/scratch/hyaku/mado-r23/ExecSweepEscape && python3 -I .ufo/waves/round-20/tw-precision.py f860c1e8834397bcf42309c121d7630ef32cb7dc
cd /fast/scratch/hyaku/mado-r23/ExecSweepEscape && python3 -I .ufo/waves/round-20/tw-precision.py a28e4815aabfa85f55274884000fb2608355f8cf
```

No package was installed, upgraded or removed; no host state was changed (the only host reads were
the repository and the scratch tree). Every scanner invocation was `python3 -I` over committed fixture
data, one child at a time, inside the existing 384 MiB / 15 s caps; no fixture content was executed.

Patch check: a fresh clone of the lane at `a28e4815aabfa85f55274884000fb2608355f8cf` accepts
`candidate.patch` with `git apply --check` (clean), and the patched tree's `tools/mado-tripwire.py`
hashes to `3daf01e34467942f71ff8c5fb9547e0fa797c5a6a7cedf2a7a5501b965ecae8d` and measures 10/12 on
the round-23 repair counter. The lane's own `tools/mado-tripwire.py` is untouched (still
`cd9da20c…`), and no tracked file in the lane changed.

**Verdict: the assigned item is implemented, the four owned repair cases pass, the two recall guards
keep their rows, every no-harm guard holds (57/57, 35/35 + 17/17, 247/247, 166/175 with the base's
identical passing set, 1356-file corpus with zero added/removed groups and zero error flips, both
resource populations clean), and the round-23 repair counter stands at 10/12 for this candidate — the
remaining two cases need the caller-frame fix that belongs to another seat.**
