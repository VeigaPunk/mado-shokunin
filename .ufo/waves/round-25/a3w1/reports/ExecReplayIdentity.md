# ExecReplayIdentity — v4 replays v3's case trees for a seed (a3w1)

Seat: `MadoR25A3.ExecReplayIdentity` (leaf executor). Assignment: verify the registration claim that
counter v4 (`c1/count.py`) replays v3's (`c1/count-v3.py`) case trees for a seed, via a read-only harness
in `/fast/scratch/hyaku/mado-r25a3/replay/`, comparing per-case tree digests, expected-model lists, and
rng consumption. No oracle, no counter edit, no tool run, no wave data.

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (tip `1ed41fa8`).
Counter bytes measured, before and after the runs (unchanged):

```
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
```

v4's internal pin `V3_SHA` equals the v3 sha above; the harness rejects the run otherwise.

## Verdict

`REPLAY v4==v3 trees: 41/41 per seed 0123456789abcdef (models 41/41 rng_state 41/41 rng_draws 41/41 total_draws=35059) ; 41/41 per seed 00000000deadbeef (models 41/41 rng_state 41/41 rng_draws 41/41 total_draws=34102) ; 41/41 per seed dade6dca3676b06e (models 41/41 rng_state 41/41 rng_draws 41/41 total_draws=33619)`

Claim verified, under the counter's own input model: for the same config snapshot and the same live
`hyprctl binds -j` table, v4's step 1 generates byte-identical case trees, identical expected-model
lists, and the identical rng draw sequence/state as v3's loop, case by case, in the same order, for
both fixed seeds and a fresh seed (123/123 case comparisons). v4 makes no rng draw outside its step-1
block. Two negative controls show the harness would have caught a one-draw difference and a one-byte
tree difference, so the 41/41 result is not vacuous.

## What was run

Harness (my only implementation file, single stdlib python3 file):
`/fast/scratch/hyaku/mado-r25a3/replay/replay_identity.py` (22513 B, sha256
`421f82d759e507ea74d066901b621a55bddf0d7d9838723d7f5166bf0ff42702`). It imports both counters with
`importlib` only (neither `main()` runs), reads both files as bytes, and executes each counter's
generation statements **extracted verbatim from its own source** with `ast` line slices:

* v3: `cases = ...` / `rng = random.Random(int(seed, 16))` / `gen = Gen(rng, live)` (3 lines), then the
  loop-body statements 0–4 (`home = os.path.join(tmp, "case")`, the `rmtree` guard,
  `shutil.copytree(snap0, home, symlinks=False)`, the `BASE`/`perturb` branch, the label).
* v4: main's step-1 block from `cases = ...` through the end of `for kind, i in cases:` (13 lines),
  including `home = os.path.join(tmp, "cases", label, "home")` and `v3.perturb(kind, rng, home, live, gen)`.

Instrumentation only (no semantic change): both blocks execute against a `random.Random` subclass that
logs `random`/`choice`/`shuffle`/`randint` calls and results; v4's `v3` name is a pass-through proxy that
records the post-`Gen` state and every `perturb` call. Case trees come from one shared snapshot copy
(`v3.copy_roots(~, snap0)`, 79 files); `live` is one `hyprctl binds -j` read verb (sha256
`9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`, 192 binds) deep-copied per side.
Per case it computes the digest over `sorted(relpath + "\0" + sha256(bytes))` for every regular file.

Commands (all in `/fast/scratch/hyaku/mado-r25a3/replay/`; all exited 0):

```
timeout 900  prlimit --as=4000000000 python3 -I replay_identity.py --seeds 0123456789abcdef > single-seed.out 2> single-seed.err
timeout 1800 prlimit --as=4000000000 python3 -I replay_identity.py > replay-run.out 2> replay-run.err
timeout 1800 prlimit --as=4000000000 python3 -I replay_identity.py --selftest > replay-run-selftest.out 2> replay-run-selftest.err
timeout 1800 prlimit --as=4000000000 python3 -I replay_identity.py --selftest > replay-run-selftest2.out 2> replay-run-selftest2.err
timeout 1800 prlimit --as=4000000000 python3 -I replay_identity.py --selftest > replay-final.out 2> replay-final.err   # canonical receipt
```

Canonical receipt: `replay-final.out` (337 lines, sha256
`383d4a8138fee7e1c4361f64457df129a00f29a1a00d7d538b5f2f6e56f5c585`; `replay-final.err` empty).
Wall time 9.8 s. `work/` is empty after the run (case trees deleted); no lane file was written; the
counters' shas were re-checked afterwards and are unchanged.

## Static checks (from `replay-final.out`)

```
count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375 bytes=38921
count.py    sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 bytes=14537
v4 pin V3_SHA=8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375 pin_matches=True
static v3-import-vs-v4-loaded-v3 code fingerprints: 29/29 equal, mismatch=none
static TYPES equal=True (AUVSGUCSRH) PER_TYPE v3=4 v4=4 equal=True
static v3 pre-block (3 lines): cases/rng/gen from source; rng uses in loop body after the extracted slice: none
static cases construction identical: True  'cases = [("BASE", None)] + [(t, i) for t in TYPES for i in range(PER_TYPE)]'
static v3 block has copytree-from-snap0 + perturb-per-case: missing=none
static v4 block has copytree-from-snap0 + perturb-per-case: missing=none
static v4 rng names outside step-1 block: none ; random.* outside block: none ; random.* in block: [52]
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
```

`29/29` is the recursive code fingerprint (byte code, names, consts, nested comprehensions/lambdas) of
every function/method defined in `count-v3.py`, compared between the harness's import and the module
object v4 itself loads — same code, not just the same sha. The only `random.*` use in v4 is the single
`random.Random(int(seed, 16))` inside step 1; `rng` appears nowhere else in v4's source.

## Dynamic result per seed

41 cases per seed (`BASE`, then 4 each of `ADD UNBIND VARIABLE SOURCE GLOB UNSOURCED COMMENT SYNTH
REWRITE HARD`), same labels and same `(kind, index)` list on both sides (asserted, not assumed). All
five columns matched 41/41 for every seed; `v3_total_draws == v4_total_draws` in each run:

```
TOTALS seed=0123456789abcdef trees=41/41 models=41/41 rng_state=41/41 rng_draws=41/41 descs=41/41 v3_total_draws=35059 v4_total_draws=35059 final_state_same=True gen_state_same=True
TOTALS seed=00000000deadbeef trees=41/41 models=41/41 rng_state=41/41 rng_draws=41/41 descs=41/41 v3_total_draws=34102 v4_total_draws=34102 final_state_same=True gen_state_same=True
TOTALS seed=dade6dca3676b06e trees=41/41 models=41/41 rng_state=41/41 rng_draws=41/41 descs=41/41 v3_total_draws=33619 v4_total_draws=33619 final_state_same=True gen_state_same=True
```

Columns: `tree` = per-case digest of sorted relpath + file sha256; `model` = v3's expected entry list
(v4's `model_exp`) compared field-for-field; `rng_state` = `getstate()` after each case; `rng_draws` =
per-case logged draw sequence (method, arity/index, values); `descs` = perturb descriptions. The
unperturbed `BASE` tree digest was the same (`2eec8a6a09234800…`) in all runs and seeds, i.e. one stable
snapshot. Per-case draw counts are non-trivial (e.g. `REWRITE-0` 4234 draws, `HARD-0 3122`), so the
comparison is not dominated by empty cases.

## Negative controls (`--selftest`, same seed, same snapshot/live)

```
TOTALS seed=0123456789abcdef [selftest M1: one extra rng draw in v4 block] trees=13/41 models=17/41 rng_state=15/41 rng_draws=12/41 descs=21/41 v3_total_draws=35059 v4_total_draws=34920 final_state_same=False gen_state_same=True
SELFTEST M1 extra_rng_draw detected=yes trees=13/41 states=15/41 draws=12/41
TOTALS seed=0123456789abcdef [selftest M2: one byte changed in ADD-0's v4 tree] trees=40/41 models=41/41 rng_state=41/41 rng_draws=41/41 descs=41/41 v3_total_draws=35059 v4_total_draws=35059 final_state_same=True gen_state_same=True
SELFTEST M2 tree_byte detected=yes trees=40/41 models=41/41 states=41/41 draws=41/41
SELFTEST LIVE reversed_live replay_holds=yes trees=41/41 models=41/41 states=41/41 draws=41/41 digests_differ_from_base=23/41
SELFTEST overall=harness detects divergence and content drift
```

* M1 inserts one `rng.random()` after `gen = v3.Gen(rng, live)` in the extracted v4 block (in-memory
  string edit of the slice; the counter file is untouched). The harness immediately reports mismatches
  (trees 13/41, states 15/41, draws 12/41, v4 total draws 34920 vs v3 35059). Partial matches come from
  later re-synchronization windows where the diverged runs happen to consume the same number of words
  again; `Gen.used` then still blocks exact equivalence. This is the failure mode the assignment names.
* M2 appends one comment byte to `ADD-0`'s v4 case tree after the block. Exactly one tree digest flips
  (40/41) while models, rng states and draws stay 41/41 — the digest check detects content drift the rng
  checks cannot see.
* LIVE reruns both literal loops with `list(reversed(live))`. Replay still holds 41/41 on every axis,
  yet 23/41 tree digests differ from the base-live run: the loops track each other for a different live
  input, and the trees demonstrably depend on that input.

## Findings and limits of the claim

1. **The registration claim is true as stated in its own frame.** "v4 keeps v3's case generator
   unchanged (count-v3.py, imported and sha256-pinned) and v4's step 1 is the same loop in v3's order
   with the same rng" is verified mechanically: same literal statements, same code (29/29 fingerprints),
   same case list, identical per-case trees/models/states/draw logs, and no rng use anywhere else in v4.
2. **Replay identity is conditional on two live inputs, not on the seed alone.** The snapshot copy and
   the `hyprctl binds -j` table feed `perturb` (candidate selection, copied dispatcher/arg/description).
   With a reversed live list the identical loops still replay each other 41/41 but 23/41 tree digests
   change. So "seed X replays the case trees of receipt Y" also needs the same live table and snapshot;
   a v4 run at a later time on a changed table can legitimately differ for the same seed. This is v3's
   own property (v3 captures live the same way), not a v4 replay defect; it does not weaken v4's
   predicate, because v4 takes expected values from the oracle on whatever trees v4 generates.
3. **`model_exp` is diagnostic only.** v4 computes v3's expected list per case but uses it solely for
   `V3_MODEL_AGREE`; scoring uses the oracle table. Identical model lists therefore prove generator
   replay, not oracle agreement (that is out of scope here; no oracle was run).

## Risks

* Fidelity rests on `inspect.getsource` + `ast` line slices of `main`; an edit to v4 outside the extracted
  step-1 lines would not be executed by the harness. Mitigations: the exact block content is asserted
  (`v3.Gen`, `v3.perturb`, `copytree(snap0, …)`, `random.Random(int(seed, 16))`), the whole-file sha is
  printed, and a source-wide AST scan shows no `rng`/`random.*` use outside the block. Both counters are
  frozen and were re-hashed after the runs.
* One `hyprctl binds -j` read verb per invocation; a live change *during* an invocation is invisible
  (both loops share one capture). This affects interpretation of other receipts, not these comparisons.
* The harness executes v4's step-1 block without the oracle/thread pool around it; nothing in step 1
  reads the oracle's results, and the block was run verbatim, so this is not expected to mask a
  difference. The negative controls bound the risk of a false "match".

## Host and scope compliance

* No nested Hyprland, no bubblewrap, no oracle call, no tool execution; only `hyprctl binds -j` (read
  verb) and read-only reads of the four config roots (79 files) into `/fast/scratch/hyaku/mado-r25a3/`.
* No writes in the lane; the counter and generator bytes are unchanged (shas above). No packages
  installed or upgraded. Nothing committed.
* Leftover scratch: harness + `single-seed.out`, `replay-run.out`, `replay-run-selftest*.out`,
  `replay-final.out` (all under `/fast/scratch/hyaku/mado-r25a3/replay/`); `work/` empty.

## Blockers

None. No exit-2 or setup error occurred; every harness invocation exited 0.
