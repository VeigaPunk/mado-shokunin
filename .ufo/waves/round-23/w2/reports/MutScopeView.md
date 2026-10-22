# MutScopeView — wave-2 mutation probe of the round-23 C1 scope logic

Seat: `MadoR23.MutScopeView` (leaf mutation-tester). Item: **C1 operability** — attack
what landed, do not change it. Wave 2, falsify pass.

Target under test: the **landed lane tip** `2f1134f38930fc8b067d2d7f5bba126338faabdd`
(`tools/mado-tripwire.py`, sha256 `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009`),
i.e. the C1 tool change from wave-1 candidate `ExecFullB`.

Nothing in the lane repo was modified by this seat: no tool, corpus, fixture, expected
file, PROVINCE/SKILL/LOG/SCORECARD file, and no other seat's `w1/out/*` directory. The
only file written inside the lane is this report. All mutation work happened in a scratch
copy under `/fast/scratch/hyaku/mado-r23/w2/MutScopeView/`.

---

## 1. What was mutated

The five single-point mutants were built by `make_mutants.py`, which copies the pristine
tip bytes and applies exactly one anchored replacement each (each pattern was asserted to
occur exactly once). Diff hunks (`diff -u tool.py mutants/<name>/tool.py`):

**M1 — `m1_caller_frame_in_scope_view` (include the calling frame in `scope_view`)**
sha256 `9b3e010fd246a5c08422df365eed9181fca8dcf744e8771260cc1ecf0a5a2f68`
```diff
@@ -2451,6 +2451,10 @@ scope_view()
     env, bindings = {}, {}
+    for name, value in fallback_env.items():
+        env[name] = value
+    for name, info in fallback_bindings.items():
+        bindings[name] = info
     for view in views:
```
The caller's frame (`fallback_env` / `fallback_bindings`) now takes part in the view and
takes precedence over the scope chain — the H4 "caller-frame leak" defect.

**M2 — `m2_chain_outermost_first` (merge the chain outermost-first)**
sha256 `d5c66f81f14e254720ba0a212aa92b4f490836d95cf8088c8cb3773bd65ccef0`
```diff
@@ -2451,7 +2451,7 @@ scope_view()
-    for view in views:
+    for view in reversed(views):
```

**M3 — `m3_all_parameters_escape` (every parameter escapes)**
sha256 `12d3d706e07282f3a8d72bb369c056668cd627da57b965c1cca80a9bf3a129cd`
```diff
@@ -2510,7 +2510,7 @@ parameter_escapes()
-    return bool(reaches & escaping)
+    return True  # MUTANT: every parameter escapes
```

**M4 — `m4_no_parameter_escapes` (no parameter escapes)**
sha256 `14f736a4c4ca64ca79f2180bd10df0aa0a87f318c00a97c789ef3dcab25cb058`
```diff
@@ -2488,7 +2488,7 @@ parameter_escapes()
         if reaches & escaping:
-            return True
+            return False  # MUTANT: no parameter escapes
@@ -2510,7 +2510,7 @@ parameter_escapes()
-    return bool(reaches & escaping)
+    return False  # MUTANT: no parameter escapes
```

**M5 — `m5_drop_module_scope_view` (drop the MODULE_SCOPE late-global view)**
sha256 `b40ac6e34f97fd8482d1473b02ba84869a055d069efae863f19822601cd40dcd`
```diff
@@ -2446,6 +2446,8 @@ scope_view()
         view = ctx["scopes"].get(key)
         if view is None:
             break
+        if key == MODULE_SCOPE:
+            break  # MUTANT: the module-scope late-global view is dropped
         views.append(view)
```

## 2. Detectors run on pristine bytes and on every mutant

| id | command |
|---|---|
| repair (12-case frozen set) | `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/measure.py --tool <TOOL>` |
| round-22 oracle (57) | `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-22/oracle/measure.py --tool <TOOL>` |
| round-21 oracle (35+17) | `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/oracle/measure.py --tool <TOOL>` |
| `CritFrameNeighbour` | `python3 -I <scratch>/lane/.ufo/waves/round-23/w1/out/CritFrameNeighbour/measure.py --tool <TOOL>` |
| `CritEscapeNeighbour` | `python3 -I <scratch>/lane/.ufo/waves/round-23/w1/out/CritEscapeNeighbour/run.py --tool <TOOL>` |
| `CritClosureNeighbour` | `python3 -I <scratch>/lane/.ufo/waves/round-23/w1/out/CritClosureNeighbour/probe.py --tool <TOOL>` |
| `CritScheduledNeighbour` | `python3 -I <scratch>/sched_run.py --tool <TOOL>` |

The three neighbours that take `--tool` write `cases.json` next to themselves, so they were
run from **byte-exact copies** of the wave-1 neighbour directories placed under
`<scratch>/lane/.ufo/waves/round-23/w1/out/` (their `parents[5]` then resolves to
`<scratch>/lane`, whose `.ufo/waves/round-21/oracle/measure.py` is a symlink to the real
helper). The lane's own `w1/out/Crit*Neighbour/` files are byte- and mtime-unchanged.

`CritScheduledNeighbour/cases.py` can only rebuild its cases against the fixed **base**
classifier, so it cannot score an arbitrary tool. `<scratch>/sched_run.py` is an equivalent
runner written for this probe: it reuses the neighbour's own frozen `cases.json`
expectations and its `truth.py` (recording fake `subprocess`, no real subprocess spawned)
with the unchanged round-21 oracle `scan` helper and the round-23 `repair/measure.py`
`judge()`, i.e. exactly the rule the neighbour's own builder applies.

Baselines were taken on the **pristine tip bytes** before any mutant was scored; a detector
that already fails at baseline is reported as *inconclusive*, never as a kill.

## 3. Baseline (pristine tip bytes, sha256 `41489991…`)

| detector | result |
|---|---|
| repair set | **12/12** |
| round-22 oracle | **57/57** (`status: complete`, exit 0) |
| round-21 oracle | **35/35 primary + 17/17 supplemental** |
| `CritFrameNeighbour` | 3/3 `base-correct` |
| `CritEscapeNeighbour` | 2/3 `base-correct`; `EscapeTupleNestedClosureLater` = `base-silent-miss` (known pre-existing gap, also recorded in the ExecFullB design note) |
| `CritClosureNeighbour` | 1/3 `base-correct`; `LoopClosuresLateBinding` = `base-silent-miss`, `NonlocalReboundAfterFactory` = `base-unparsed` (pre-existing gaps at the tip) |
| `CritScheduledNeighbour` | 3/3 pass |

Those three neighbour cases are baseline-failing and therefore **inconclusive** as
kill signals; every other case is attributable.

## 4. Per-mutant results

| mutant | repair | r22 oracle | r21 oracle | frame | escape | closure | scheduled | verdict |
|---|---|---|---|---|---|---|---|---|
| M1 caller frame in scope_view | **10/12** | 57/57 | 35+17 | 0/3 | 1 regress. | = base | **0/3** | **KILLED** |
| M2 chain outermost-first | **11/12** | 57/57 | 35+17 | 3/3 | = base | = base | 3/3 | **KILLED** |
| M3 every parameter escapes | **10/12** | 57/57 | 35+17 | 3/3 | = base | 1 regress. | 3/3 | **KILLED** |
| M4 no parameter escapes | **10/12** | 57/57 | 35+17 | 3/3 | = base | = base | 3/3 | **KILLED** |
| M5 drop MODULE_SCOPE view | **9/12** | **56/57** | 35+17 | **0/3** | **2 regress.** | 1 regress. | **0/3** | **KILLED** |

Detail per mutant (failing repair cases and their rows):

* **M1** — repair `ForwarderInvokesCallback`, `CallerLocalShadowsHelperGlobal`: the
  classifier reports the *foreign* `pacman -S r23-forward-foreign` /
  `pacman -S r23-local-foreign` as `observed` (a caller's local shadowing the callee's
  global). `CritScheduledNeighbour` 0/3: all three cases report the foreign
  `pacman -S r23w1-*-foreign` argv as `observed`. `CritFrameNeighbour` 0/3
  `base-false-observed`; `CritEscapeNeighbour/EscapeSecondForwarder` →
  `base-false-observed`.
* **M2** — repair `NestedDefReadsDefiningFrame`: the outermost (module) view now wins the
  merge, so a nested `def`'s free name resolves to the module global instead of the
  defining frame's local → foreign `pacman -S r23-nested-foreign` observed. Killed by the
  repair counter alone: the round-22 oracle, the round-21 oracle and all four neighbours
  are insensitive to it.
* **M3** — repair `ReturnedGlobalCallableShadow` (an extra `lead` row
  `pacman -S r22-foreign-callable`) and `ForwarderPassesCallerArgument`
  (`unparsed_spawns = 1`). `CritClosureNeighbour/TwoFactoryClosureReadsReboundGlobal`
  regresses `base-correct` → `base-false-observed`.
* **M4** — repair `CallbackStoredInDict` and `CallbackStoredOnAttribute`: both produce
  **no rows at all** (the stored callback is never swept, so the recall the repair set
  demands is lost). This is a silent-miss direction, not a false-positive one.
* **M5** — repair `ForwardExistingClosureWithoutFrameContamination` (now
  `unparsed_spawns = 2`, no rows), `ForwarderInvokesCallback` and
  `CallerLocalShadowsHelperGlobal` (foreign argv observed). The round-22 oracle fails
  `CaptureGlobalLate` ("complete class/command/evidence multiset or zero-error condition
  differs") — the late-global invariant. `CritFrameNeighbour` 0/3
  `base-false-observed`; `CritScheduledNeighbour` 0/3; `CritEscapeNeighbour`:
  `EscapeSecondForwarder` → `base-false-observed`, `EscapeListAppendThenCalled` →
  `base-unparsed`; `CritClosureNeighbour/TwoFactoryClosureReadsReboundGlobal` →
  `base-unparsed`.

## 5. Coverage findings (advice, not contract changes)

1. **All five mutants are killed**, so the landed scope logic is not merely
   plausibility-covered: each of the five plausible single-point defects in the new scope
   logic is caught by at least one committed detector.
2. **The repair set carries nearly all the discriminating power.** M2, M3 and M4 are
   invisible to the round-22 oracle (57/57), to the round-21 oracle (35/35 + 17/17) and to
   the four neighbours. If the round-23 repair set were weakened, the merge-order and
   escape-polarity defects would ship silently.
3. **The neighbours add real signal on the frame/closure axis**: `CritFrameNeighbour` and
   `CritScheduledNeighbour` kill M1 and M5 (caller-frame leak / dropped module view) even
   though the repair set alone would also kill them; `CritClosureNeighbour` contributes a
   second kill for M3.
4. **The round-22 oracle's unique contribution is `CaptureGlobalLate`** — only M5 breaks
   it, so the S121 "late global" invariant is guarded by exactly one committed case.
5. **Round-21 oracle blind spot**: it passed all five mutants (35/35 + 17/17 in every
   run). It cannot see any of the round-23 scope changes; it is a no-harm guard for older
   populations only, and should not be read as evidence that the scope logic is correct.
6. **Baseline gaps that remain open at the tip** (not caused by any mutant, unchanged from
   the ExecFullB design note): `CritEscapeNeighbour/EscapeTupleNestedClosureLater`
   (`base-silent-miss`), `CritClosureNeighbour/LoopClosuresLateBinding`
   (`base-silent-miss`), `CritClosureNeighbour/NonlocalReboundAfterFactory`
   (`base-unparsed`). These three are the cases that cannot distinguish anything, and they
   are where a future mutation probe would have the most room.

## 6. Restoration evidence

* The pristine tip bytes were never edited: `sha256sum tool.py` =
  `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009` **before and after**
  all mutant runs (identical to `git show 2f1134f3…:tools/mado-tripwire.py`).
* Every mutant lives in its own directory (`mutants/<name>/tool.py`); the five mutant
  hashes are listed in §1 and differ from the pristine hash.
* Lane repo untouched by this seat: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain`
  shows only `M SKILL.md`, `M corpus/README.md`, `M tools/mado-tripwire.py` and untracked
  wave files. **These are another seat's in-flight work, not mine**: the working-copy
  `tools/mado-tripwire.py` had mtime `09:01:03` (sha256 `8975a4da948c8102872804bf3cbc0d8f618027301cb68ee4900adab865b67198`,
  51 insertions / 17 deletions vs the tip — a reworked `parameter_escapes` with
  `DYNAMIC_SCOPE_CALLS`), i.e. it was being edited concurrently with my probe. My probe
  never wrote to it and always read the classifier from `git show 2f1134f3…` as instructed;
  the M3/M4 mutants therefore target the **committed tip's** `parameter_escapes`, not the
  working copy's reworked one.
* The wave-1 neighbour directories in the lane are unmodified (mtimes still 08:02–08:08,
  e.g. `CritFrameNeighbour/measure.py` 08:03:07); the probe ran against copies.
* No host change: no package install, no `pacman` transaction, no service/display/config
  edit. **Tooling: none installed or updated** (no `uv tool install`, no pacman, no
  release binary) — the probe needed only the interpreter and the committed harnesses.

## 7. Receipts

* scratch tree: `/fast/scratch/hyaku/mado-r23/w2/MutScopeView/`
  (`tool.py` pristine, `mutants/<name>/tool.py` ×5, `make_mutants.py`, `run_detectors.sh`,
  `sched_run.py`, `compare.py`, `results/<label>/{repair,oracle22,oracle21,frame,escape,closure,scheduled}.json` + `.err`)
* all stderr files of all detector runs are 0 bytes (no harness errors); every kill above is
  a genuine detector verdict, not a crash.

## 8. Verdict

**KILLED — 5/5 mutants killed.** The landed C1 scope logic survives a targeted mutation
probe: the caller-frame leak (M1), the outermost-first chain merge (M2), the
every-parameter-escapes polarity (M3), the no-parameter-escapes polarity (M4) and the
dropped MODULE_SCOPE late-global view (M5) are each detected by the committed repair
counter; M5 additionally breaks the round-22 oracle (`CaptureGlobalLate`) and all four
neighbours. No mutant survived; no detector result was inconclusive except the three
neighbour cases that already fail at the tip. No lane file was modified.
