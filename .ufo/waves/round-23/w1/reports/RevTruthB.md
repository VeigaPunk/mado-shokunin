# RevTruthB — C1 truth falsification: ReturnedGlobalCallableShadow, ForwardExistingClosureWithoutFrameContamination

Seat: MadoR23.RevTruthB, 2026-10-22. Scope: attack the frozen truth of two repair cases in
`.ufo/waves/round-23/repair/expected.json` (sha256 `53e34d26…187c6b9`, verified by both harnesses
on every run). No files outside this report were written. Lane tip read via read-only git:
`a28e4815aabfa85f55274884000fb2608355f8cf`, `git status --porcelain=v1 -- tools/` empty, working-tree
`tools/mado-tripwire.py` sha256 `cd9da20c…f00ea84` = frozen base.

## Commands run (each once)

1. `python3 -I .ufo/waves/round-23/repair/truth.py` — exit 0, `passed: 12, total: 12` (python 3.14.8).
   Both integrity gates (`expected.json` sha, per-fixture sha) passed; no `snapshot_tampered`.
2. `python3 -I .ufo/waves/round-23/repair/measure.py --tool tools/mado-tripwire.py` — exit 1,
   `passed: 6, total: 12`, `tool_sha256: cd9da20c…`, `helper_sha256: 4eb893d2…` — matches the
   registered before value 6/12.
3. Read-only: `git rev-parse HEAD`, `git status --porcelain -- tools/`, `sha256sum` of the tool and
   both fixtures.

No tools were installed or upgraded (none needed).

## Case A — ReturnedGlobalCallableShadow (kind exact)

Fixture code (de-JSON-escaped):

```python
import subprocess
def module_launch():
    subprocess.run(["pacman", "-Q", "r22-global-callable"])
def helper():
    launch()
def other_launch():
    subprocess.run(["pacman", "-S", "r22-foreign-callable"])
launch = module_launch
def make(launch):
    return helper
job = make(other_launch)
job()
```

Semantic walk (S121, CPython execution model: free-name resolution at runtime, in the defining
module's globals — no dynamic scoping):

- `helper` is defined at module top level, so the `launch` in its body is a LOAD_GLOBAL against the
  module namespace, resolved at call time.
- `make`'s parameter `launch` (bound to `other_launch`) lives only in `make`'s frame; `make`'s body
  never reads it and `helper` is not nested inside `make`, so that binding cannot contaminate
  `helper`'s resolution. `make(other_launch)` returns `helper` untouched.
- `job()` → `helper()` → global `launch` (= `module_launch`, set by the plain assignment) →
  `subprocess.run(["pacman", "-Q", "r22-global-callable"])` exactly once.
- `other_launch` is never called: its only reference dies with `make`'s frame. The foreign
  `pacman -S r22-foreign-callable` is unreachable, not merely unobserved.

Executed argv set (truth.py child, fake `subprocess` recording): `["pacman -Q r22-global-callable"]`.
`want` = one row `(package_query, pacman -Q r22-global-callable, observed)`. **Exact match; forbid
command never executed.**

Base measure result (my run): rows
`[["package_query","pacman -Q r22-global-callable","observed"],
  ["host_mutation","pacman -S r22-foreign-callable","lead"]]`, `unparsed 0`, exit 1, passed=false —
byte-identical to `evidence/repair-before-e33ea304.json` (lines 40–57: same rows, `unparsed 0`,
`passed false`), same `tool_sha256`. So the base failure is precisely the routed H3 "foreign lead":
the classifier emits the install as a *lead* because it apparently lets `make`'s parameter shadow the
global for a function `make` merely returns.

**Verdict A: truth-correct.** Rule assessment: exact rule is tight and correctly scoped — it demands
exactly one row with the right class, command and `observed` evidence, zero unparsed, and no
forbidden command at any tier; there is no pass-while-wrong room (a lead-instead-of-observed claim
or a wrong class both fail). Not too strict either: the forbid-any command is genuinely unreachable
(dead parameter binding), so even a conservative "lead" claim about it is false, and forbidding it at
every tier matches the routed defect (the base failure *is* a lead). Nothing demanded exceeds what
Python does: exactly one argv executes.

## Case B — ForwardExistingClosureWithoutFrameContamination (kind exact)

Fixture code:

```python
import subprocess
argv = ["pacman", "-Q", "r22-forward-global"]
def original():
    def run():
        subprocess.run(argv)
    return run
def forward(argv, callback):
    return callback
saved = original()
job = forward(["pacman", "-S", "r22-forward-foreign"], saved)
job()
```

Semantic walk:

- Inner `run` references `argv`, which is bound in neither `run` nor `original` (no assignment in
  `original`), so it is not a cell/free variable of the factory — it resolves as a module global at
  call time: `["pacman", "-Q", "r22-forward-global"]`.
- `forward`'s parameter `argv` (the foreign install list) shadows the global only inside `forward`;
  `forward` returns `callback` unmodified — no wrapper, no rebinding — so the caller's argv never
  escapes `forward`'s frame. Closures capture defining-scope cells, never caller frames; the
  frame-contamination hypothesis is exactly what this fixture refutes.
- `job()` = `saved()` = `run()` → `subprocess.run(["pacman","-Q","r22-forward-global"])` exactly once.
  The foreign list is used by nothing and dies with `forward`'s frame.

Executed argv set (truth.py): `["pacman -Q r22-forward-global"]`. `want` = one row
`(package_query, pacman -Q r22-forward-global, observed)`. **Exact match; forbid never executed.**

Base measure result (my run): rows
`[["package_query","pacman -Q r22-forward-global","observed"]]`, `unparsed 1`, exit 1, passed=false —
identical to `evidence/repair-before-e33ea304.json` (lines 60–77: same single row, `unparsed 1`,
`passed false`). The base scanner actually gets the executed argv right; it fails on the
`eval_unparsed+unparsed_spawns == 0` requirement (routed H3 "ForwardExistingClosure unparsed 1").

**Verdict B: truth-correct.** Rule assessment: not too loose — a contaminated tool emitting the
foreign row fails on both row mismatch and forbid_any, and one that emits both rows also fails exact
equality; only a tool that reports exactly the true single execution passes. Not too strict — the one
demand beyond the executed set is `unparsed == 0`, which constrains scanner parse coverage (this
fixture is 15 lines of plain `def`/calls; a correct parser has nothing to skip), not Python
behavior; the exactness itself (one executed argv, `observed`, `package_query` for a `-Q` query)
matches what Python does. The base failing here is the intended measurement of routed defect H3.

## Rule-level cross-check (both cases, exact kind)

- `truth.py` judges only the executed command strings (`sorted(executed) == sorted(want commands)`);
  `measure.py` additionally judges class and evidence on the scanner's findings rows. The two layers
  are consistent: truth establishes what runs, the measure rule adds the scanner-claim requirements.
  No gap found: for both cases the executed set is a single command, so command-set equality and
  row-tuple equality are equally strict.
- `measure.judge` implements "no forbid_any at any tier" as: any findings row (any evidence value,
  leads included) whose command is in `forbid_any` fails the case. Confirmed live by case A's base
  failure, where the sole trigger besides nothing was the `lead` row.
- Fake-subprocess recording is faithful for these fixtures: only `subprocess.run(<list>)` is used, no
  kwargs dependence, `-I -S` child with fresh exec globals reproduces module-top-level semantics
  (both fixtures pass truth.py's `safe()` gate: imports only `subprocess`, no banned builtins).
- Fixture integrity: `sha256sum` of both fixtures = `6b3d8382…0caa2` and `d3d8222a…94b1`, equal to
  the per-case `sha256` in expected.json and to the round-22 copied-from origin hashes in `origin`.

## Verdict lines

- `ReturnedGlobalCallableShadow`: **truth-correct** — pass rule neither too loose nor too strict.
- `ForwardExistingClosureWithoutFrameContamination`: **truth-correct** — pass rule neither too loose
  nor too strict (the `unparsed == 0` demand is scanner-coverage, correctly keyed to routed H3).
- Base reproduction: `measure.py` at the untouched base tool (`cd9da20c…`) gives 6/12, exit 1, and
  both of my cases fail exactly as recorded in `evidence/repair-before-e33ea304.json` (case A: extra
  foreign `lead` row; case B: correct row + `unparsed 1`).

## Residual risk / verification gaps

- truth.py's child ignores `subprocess.run` kwargs and return values; a fixture abusing them would be
  under-recorded, but neither of my two fixtures does (verified by reading both fixtures; the other
  ten were not re-audited line-by-line in this seat — out of scope).
- The `exact` rule compares scanner `class` labels, so both wants depend on the classifier's
  `package_query` label for `pacman -Q`; that labeling is round-22-inherited convention (both cases
  are byte-exact copies with unchanged wants) and was not re-derived from the classifier's class
  taxonomy in this seat.
- `python3 -I truth.py` ran under Python 3.14.8 (host python). The fixtures use no
  version-sensitive semantics (plain global/closure resolution), so no version risk for these two
  cases.
