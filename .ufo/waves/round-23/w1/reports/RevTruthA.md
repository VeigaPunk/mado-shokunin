# RevTruthA — falsification attack on the frozen truth of `ReturnedGlobalHelper` and `CallerArgumentBeforeClosureOverlay`

Seat: MadoR23.RevTruthA (leaf, no subagents). Scope: C1 attack item — try to falsify the
frozen truth of two `exact` cases in `.ufo/waves/round-23/repair/expected.json`, then judge
the pass rule for each. All paths below relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`.

## What I did

1. Read `registration.md`, `expected.json`, `repair/truth.py`, `repair/measure.py`, both
   fixtures, and `.ufo/waves/round-23/evidence/repair-before-e33ea304.json`.
2. Verified the snapshot is the registered one (sha256sum):
   - `fixtures/ReturnedGlobalHelper.jsonl` = `bba513187e957d79032e76c9c7e549414c8e7452968ed67f3115c86715e80ede` (matches expected.json and registration's r22 byte-exact claim)
   - `fixtures/CallerArgumentBeforeClosureOverlay.jsonl` = `799315302691759b727ed9bf9c98e2846903a0a1743ead698240862bb7723525` (matches)
   - `expected.json` = `53e34d2691f1a456ce6a4387795c84e5a55d3449b94245d68de516023187c6b9` (matches EXPECTED_SHA pinned in truth.py and measure.py)
   - `tools/mado-tripwire.py` = `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84` (matches registration base)
3. Reasoned each fixture from Python name-resolution semantics (below), then ran the two
   sanctioned scripts once each, from the repair directory, sequential children enforced by
   the scripts themselves (truth.py: one `python3 -I -S` child per case, 15 s cap;
   measure.py: one scan child per case via the round-21 helper). Python 3.14.8. No tool
   installs were needed or performed. No `lsp` device exists in this leaf's tool inventory;
   semantic ground truth here is the actual interpreter run, which is stronger than LSP
   answers anyway.
   - `python3 -I .ufo/waves/round-23/repair/truth.py` → exit 0, `passed: 12, total: 12`.
   - `python3 -I .ufo/waves/round-23/repair/measure.py --tool tools/mado-tripwire.py` →
     exit 1, `passed: 6, total: 12` (6/12 is the registered before value; exit 1 is the
     counter correctly reporting a failing population, not a run failure).

## Case 1 — `ReturnedGlobalHelper` (exact)

Fixture code (from the single eval toolCall in the JSONL transcript):

```python
import subprocess

argv = ["pacman", "-Q", "r22-nhb-module"]

def helper():
    subprocess.run(argv)

def make(argv):
    return helper

job = make(["pacman", "-S", "r22-nhb-factory-local"])
job()
```

Reasoning: `helper` is defined at module level, so `make`'s scope is not an enclosing scope
of `helper`; inside `helper` the free name `argv` has no local binding and resolves straight
to the module global `["pacman", "-Q", "r22-nhb-module"]`. `make` returns the function
object `helper` itself — no cell is shared, the parameter `argv` is bound and never read
inside `make`. `job()` therefore executes exactly `pacman -Q r22-nhb-module`. The factory
argv `pacman -S r22-nhb-factory-local` is dead data. The classic wrong reading — treating
the returned function as a closure over the caller's frame and reporting the factory argv —
is precisely what `forbid_any` pins.

Truth run: `executed = ["pacman -Q r22-nhb-module"]`, no forbidden command. Equals `want`
(`package_query` / `pacman -Q r22-nhb-module` / `observed`; truth.py exact branch compares
executed commands, class/evidence are scanner-taxonomy demands applied by measure.py).

Base counter: `passed: true`, rows exactly `[(package_query, pacman -Q r22-nhb-module,
observed)]`, `unparsed: 0`, `exit: 1`, no error — byte-identical to the
`repair-before-e33ea304.json` entry for this id (read back and compared field by field).

**Verdict: truth-correct. Rule neither too loose nor too strict.**
- Too loose? No. Exact equality of the sorted (class, command, evidence) row set excludes
  every wrong shape: a wrong extra lead (as the base tool actually produces on sibling case
  `ReturnedGlobalCallableShadow`) fails equality; a right command reported as `lead` fails
  the evidence tuple; the misreading is additionally blocked at any tier by `forbid_any`.
- Too strict? No. The command is unconditionally executed at module level, so demanding
  exactly one `observed` row demands nothing Python does not do; no other executable spawn
  exists in the fixture, so a zero-extra-rows demand forbids nothing legitimate;
  `unparsed 0` is achieved by the base scanner on this fixture.

## Case 2 — `CallerArgumentBeforeClosureOverlay` (exact)

Fixture code:

```python
import subprocess
argv = ["pacman", "-Q", "r22-callsite-argument"]
def make(argv):
    def run(actual):
        subprocess.run(actual)
    return run
job = make(["pacman", "-S", "r22-unused-closed-argument"])
job(argv)
```

Reasoning: `run`'s body references only its parameter `actual` and the global `subprocess`;
it never reads `argv`, so `make`'s parameter is an unused local, not a free variable of
`run` — no closure cell overlays anything. At the module-level call site, `job(argv)`
evaluates the global `argv` (`pacman -Q r22-callsite-argument`) and passes it as `actual`;
`subprocess.run(actual)` executes exactly that. The closed value
`pacman -S r22-unused-closed-argument` is dead; `forbid_any` names exactly the overlay
misreading (substituting make's argv for the caller's argument).

Truth run: `executed = ["pacman -Q r22-callsite-argument"]`, no forbidden command. Equals
`want` (`package_query` / `pacman -Q r22-callsite-argument` / `observed`).

Base counter: `passed: true`, rows exactly `[(package_query, pacman -Q r22-callsite-argument,
observed)]`, `unparsed: 0`, `exit: 1`, no error — byte-identical to the
`repair-before-e33ea304.json` entry for this id.

**Verdict: truth-correct. Rule neither too loose nor too strict.**
- Too loose? No. Any tool that performs the overlay misreading emits
  `pacman -S r22-unused-closed-argument` at some tier and is killed by `forbid_any`; any
  other deviation (dropping the call, misclassifying, lead-instead-of-observed) fails exact
  row equality. A tool passes only by emitting exactly what Python executes.
- Too strict? No. The executed command is unconditional; `observed` is honest; there is no
  second executable spawn, so exactness forbids nothing real; base reaches `unparsed 0`.

## Cross-checks

- truth.py and measure.py agree on both cases: executed argv set == want commands == base
  scanner's observed rows.
- truth.py's `safe()` gate and recording fake are sound for these fixtures: only `subprocess`
  is imported, only `subprocess.run` is touched, both argv lists are single-space-token
  strings so the `" ".join(argv)` recording is unambiguous, and `exec` uses a fresh globals
  dict with `__name__ == "__main__"` — module-level semantics, exactly what the fixtures'
  S121 (lexical vs late-global) point exercises.

## Residual risk / verification gaps

- truth.py's exact branch truth-checks command strings only; class and evidence fields rest
  on scanner-taxonomy consistency and are enforced only by measure.py. Coherent design, but
  a repair that renamed a class would pass truth and fail measure — the pair, not either
  alone, is the contract.
- The rule is output-based: it cannot distinguish right answer via wrong reasoning from
  right answer via right reasoning. Inherent, not a defect.
- `forbid_any` matches exact joined strings. In an `exact` case a quoting/spacing variant of
  a forbidden command would also fail row equality, so it is not exploitable here. In
  `present` cases (not in my scope) a quoting variant of a forbidden command could in
  principle evade `forbid_any` while the wanted command passes presence — one-line residual
  note for the planner; I did not construct an attack fixture for it.
- Each sanctioned script was run exactly once as instructed; no reruns, no edits to any
  lane file. No installs performed, so nothing to record under the tooling directive.
