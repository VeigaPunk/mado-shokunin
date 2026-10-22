# CritClosureNeighbour — closure-lifetime neighbour fixtures (C1 discovery, outside the counter)

Seat: `MadoR23.CritClosureNeighbour` (critic, leaf). Lane base `a28e4815aabfa85f55274884000fb2608355f8cf`,
classifier `tools/mado-tripwire.py` SHA256 `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`
(same bytes as the registration base `e33ea304`).

## Headline

One of the three new fixtures makes the base classifier fail open. `LoopClosuresLateBinding` executes
`pacman -Q r23cc-loop-last`. The base returns exit 0 with a clean verdict, no rows and zero
unparsed, so nothing tells the reader that a command ran. The other two are disclosed misses
(unparsed > 0), not silent ones. None of the three is in the frozen 12-case counter or in any
no-harm guard population.

## Cases (receipt: `.ufo/waves/round-23/w1/out/CritClosureNeighbour/cases.json`)

| Case | Fixture sha256 | Executed (truth) | Never executed | Base exit / unparsed / rows | Label |
|---|---|---|---|---|---|
| NonlocalReboundAfterFactory | `faccb16b407e9a6a1c1f70b19242829e4693443bb3884cefc3a4da09f7472286` | `pacman -Q r23cc-nonlocal-rebound` | `pacman -S r23cc-nonlocal-initial` | 0 / 1 / none | base-unparsed (miss disclosed) |
| LoopClosuresLateBinding | `cf12f9d97e8cd4f8a6c10e3fe52728561e5eba9d4394834b613d88fa78c3ec9f` | `pacman -Q r23cc-loop-last` | `pacman -S r23cc-loop-first` | 0 / 0 / none | **base-silent-miss** |
| TwoFactoryClosureReadsReboundGlobal | `6b84af674ca45f26e7db31a7a765895c19aab0fa7029bc5b1a705118ec347804` | `pacman -Q r23cc-global-at-call` | `pacman -S r23cc-global-at-definition` | 1 / 1 / `package_query pacman -Q r23cc-global-at-call observed` | base-unparsed (right row, residue 1) |

What each fixture tests (all import only `subprocess`, and every spawn is `subprocess.run(<name>)`):

- **NonlocalReboundAfterFactory** covers a factory-captured variable that is rebound after the
  closure is created. `make()` binds `argv` to the `-S` list, defines `run` to read `argv`, then calls
  `rebind()`, which does `nonlocal argv` and sets it to the `-Q` list. `make()` returns `run`, and the
  module calls it.
- **LoopClosuresLateBinding** covers loop-created closures. `make_all()` loops over two list
  literals, defines `run` in the loop body and appends it. It returns the list, and the module calls
  `jobs[0]()`. Because of late binding, the first closure reads the last loop value.
- **TwoFactoryClosureReadsReboundGlobal** combines a closure passed through two factories with a
  module global rebound between definition and call. `make()` returns `run`, which reads the module
  global `argv`. `wrap(callback)` returns `wrapped`, which calls `callback()`. The module runs
  `job = wrap(make())`, rebinds the global `argv` from `-S` to `-Q`, then calls `job()`.

Proposed wave-2 expectations are in `cases.json` under `proposed_expectation`, in the repair-set
schema: `kind: exact`, the want row taken from the executed argv, and `forbid_any` set to the
never-executed literal. Each want row's class is assigned by prefix (`-Q` → package_query,
`-S` → host_mutation), matching the classes in the repair set.

## Counterexample: functions defined under a branch or loop are dropped without disclosure

Narrowing with scratch variants (`diag.json` holds the code, sha256 and base rows; these are
diagnostics, not attack inputs):

- A: loop-defined closure called directly inside the factory → exit 0, unparsed 0, no rows.
- C: module-level `for` that defines `run`, then `run()` → exit 0, unparsed 0, no rows.
- F, G, H: `if True:`, `try:` or `while` containing `def run(): subprocess.run(["pacman","-Q","d-only"])`
  with a **literal** argv, then `run()` → exit 0, unparsed 0, no rows each.
- B, a factory with no loop called through a list subscript → unparsed 1. The subscript call is
  disclosed.
- D, a spawn directly in a loop body using the loop variable → unparsed 1. Also disclosed.
- E, the same factory without the nonlocal rebind → `pacman -Q d-only observed`. Correct.

Cause in the code: in `update_bindings` (`tools/mado-tripwire.py:1953-1959`), any statement that is a
branch or loop hits `visit()`. That rebinds every nested `def`/`class` name to `{"kind": "unknown"}`
and returns without keeping the node. A later zero-argument call to that name has no call-site argv
for `helper_argv_leads` to report, so nothing is emitted and nothing is counted.

This breaks the tool's own stated contract at `tools/mado-tripwire.py:47-50`: "A visible body this
path does not follow but the executed text still reaches is swept, and every row in it is a `lead`."
The body is visible and the executed text reaches it by name, yet it is never swept.

Why earlier rounds missed it: round-20 `AdvLeadMarks` B4, B5 and B10 (`lead-if-true-def`,
`lead-try-def`, `lead-while-false-def`) exercise the same `visit()` path but always pass the argv as a
call-site literal (`run(['pacman','-Q','hyprland'])`). The base reports `lead` on those through
`helper_argv_leads`, which hides the fact that the body is never read. Corpus exposure: across the
1356-file round-21 snapshot (1102 eval cells), five definitions sit under a compound statement. Two
have spawn text, and both are those round-20 call-site-argv files. **No file in any guard population
has the zero-argument shape**, so the corpus comparator cannot see a change on this path in either
direction.

## Impacted axes

- **Operability / honesty of `clean`.** A transcript that ran a finding-class command gets exit 0.
  Swapping the two loop literals gives the same silence for `pacman -S` (host_mutation). This is a
  pre-existing base defect, not a candidate harm. Round-23 claims are frozen, so it should be routed
  as a new defect rather than added to C1 after the fact.
- **Wave-2 attack value against the candidate.** Each fixture has a definition-time decoy. A
  candidate that "repairs" closure resolution by reading the value at definition time, or by
  treating a loop or branch `def` as a straight-line `helper`, would produce a false `observed` row
  for `-S r23cc-nonlocal-initial`, `-S r23cc-loop-first` or `-S r23cc-global-at-definition`. Any
  `forbid_any` command at any tier is a regression relative to base, because base emits none of them.
  TwoFactory is in the same family as the repair case `ForwarderInvokesFactoryClosure` (unparsed 1
  at base). If the candidate clears that residue, it must keep `-Q r23cc-global-at-call`.
- **Tradeoff, not a defect.** NonlocalReboundAfterFactory's unparsed 1 with no row follows the
  documented rule that any non-straight-line binding forgets the name (lines 75-82). The judge
  should accept that and reject only a foreign row.

## Smallest safe correction (advice; not patched or tested here)

In `visit()`, keep the node for a `FunctionDef`/`AsyncFunctionDef`/`ClassDef` nested under a branch
or loop, and give it a binding kind that a later call or reference **sweeps** with `sweep_body`
(rows become `lead`; free names unknown, so free-variable argv counts as unparsed_spawns). Do not
give it the `helper` kind: following it with straight-line literals is exactly what would turn
`LoopClosuresLateBinding` into a false observed `-S r23cc-loop-first`. [INFERENCE] With that change,
F/G/H would give `lead pacman -Q d-only` and A/C/LoopClosures would give unparsed 1. Re-check
round-20 B4/B5/B10 and the precision set, because a swept body adds a body-literal lead next to the
existing call-site lead.

## What I did and exact commands

1. Read `registration.md`, `repair/truth.py`, `repair/measure.py`, the round-21 scan helper
   `.ufo/waves/round-21/oracle/measure.py`, sample repair fixtures and the base before receipt.
   `/home/vgpnk/.omp/agent/RULES.md` read. Skill `godspeed`: no file found under `~/.omp`, the fleet
   root, or by `find / -xdev -path '*godspeed*' -name '*.md'`. Recorded as unopened.
2. Wrote the three fixtures by hand in the repair JSONL shape under `out/CritClosureNeighbour/fixtures/`.
3. Wrote `out/CritClosureNeighbour/probe.py` (sha256 `abf3e40b…d7cd`). Its `CHILD` and `safe()`
   are copied from `repair/truth.py`. Truth comes from a child `python3 -I -S` running under the
   recording fake `subprocess`; no real subprocess is reachable from fixture code. The scan uses
   `runpy` on the round-21 helper's `scan` (one child, 384 MiB, 15 s), and the probe checks that
   tool and helper hashes are unchanged after the run.
4. `git show a28e4815aabfa85f55274884000fb2608355f8cf:tools/mado-tripwire.py > /tmp/mado-r23-critclosure/base-tripwire.py`
   (sha256 `cd9da20c…ea84`, verified), then
   `python3 -I .ufo/waves/round-23/w1/out/CritClosureNeighbour/probe.py --tool /tmp/mado-r23-critclosure/base-tripwire.py`
   writes `cases.json` (sha256 `97cfb287ad7eb223456e72fb52bb704c5ccbbf916258d5ff934ae37a293bb235`).
   Helper sha256 `4eb893d2337a4aa758d14c064a855032737c6e2b2b1239d7ca3502042c6c82da`, Python 3.14.8.
5. Diagnostics: variant JSONL generated in `/tmp/mado-r23-critclosure/diag/`, scanned with the same
   helper and base bytes, plus the three round-20 files. Receipt
   `out/CritClosureNeighbour/diag.json` (sha256 `1506cbcc60876c3e573b1780009daccb450cec0a4dd1536ff2b5a236b5b4da87`).
6. Corpus exposure: `python3 -I /tmp/mado-r23-critclosure/count_nested_defs.py .ufo/waves/round-21/corpus/snapshot/files`,
   a static AST count only with no execution. Output:
   `{"files": 1356, "eval_cells": 1102, "defs_under_compound": 5, "defs_under_compound_with_spawn_text": 2, ...}`.

The lane was written only in `out/CritClosureNeighbour/` and in this report. No installs or updates.
No jj commands. No git writes.

**Verdict:** three new closure-lifetime fixtures with mechanical truth. Base results: one
base-silent-miss (LoopClosuresLateBinding, a fail-open clean verdict caused by
`update_bindings`/`visit()` dropping branch- and loop-scoped defs, contrary to docstring
lines 47-50) and two base-unparsed (disclosed). There are no base-false-observed cases, so any
forbidden `-S` row a candidate produces on these inputs in wave 2 is a regression.
