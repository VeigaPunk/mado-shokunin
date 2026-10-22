# RevTruthC — falsification review of frozen truth: ForwarderInvokesCallback, CallerLocalShadowsHelperGlobal

Seat: MadoR23.RevTruthC (leaf reviewer, no subagents). Scope: the two named repair cases only.
2026-10-22.

## What I did (exact commands, from /home/vgpnk/Projects/shokunin)

1. Read `.ufo/waves/round-23/registration.md`, `repair/expected.json`, `repair/truth.py`,
   `repair/measure.py`, and the two fixture files.
2. Verified frozen-set integrity myself:
   `cd /home/vgpnk/Projects/shokunin/mado-shokunin && sha256sum .ufo/waves/round-23/repair/expected.json .ufo/waves/round-23/repair/fixtures/ForwarderInvokesCallback.jsonl .ufo/waves/round-23/repair/fixtures/CallerLocalShadowsHelperGlobal.jsonl tools/mado-tripwire.py && git rev-parse HEAD`
   - expected.json `53e34d2691f1a456ce6a4387795c84e5a55d3449b94245d68de516023187c6b9` (matches truth.py/measure.py pin),
     ForwarderInvokesCallback `9325530c…f5ff`, CallerLocalShadowsHelperGlobal `442d9956…57a9` (both match their
     case `sha256` fields), base classifier `cd9da20c…ea84` (matches registration), HEAD `a28e4815aabfa85f55274884000fb2608355f8cf`
     (working tree classifier bytes still equal the e33ea304 base sha — no production edit has landed).
3. Ran the truth oracle once:
   `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/truth.py`
   → `passed 12, total 12` (python 3.14.8). My two cases executed exactly:
   - ForwarderInvokesCallback: `["pacman -Q r23-forward-global"]`
   - CallerLocalShadowsHelperGlobal: `["pacman -Q r23-local-global"]`
   Identical to the frozen `evidence/repair-truth.json` rows for these ids.
4. Ran the counter once at base:
   `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py`
   → exit 1, `passed 6, total 12` (matches registration's before 6/12). For my two cases:
   - ForwarderInvokesCallback: passed=false, unparsed=1, exit=1, rows `[(host_mutation, "pacman -S r23-forward-foreign", observed)]`
   - CallerLocalShadowsHelperGlobal: passed=false, unparsed=0, exit=1, rows `[(host_mutation, "pacman -S r23-local-foreign", observed)]`
   Byte-for-byte the same id/kind/passed/unparsed/exit/rows as
   `evidence/repair-before-e33ea304.json` (file rows for these ids). Base result confirmed.

## Case 1 — ForwarderInvokesCallback (exact)

Fixture code (from the frozen jsonl `eval` payload):

```python
import subprocess
argv = ["pacman", "-Q", "r23-forward-global"]
def run():
    subprocess.run(argv)
def forward(argv, callback):
    callback()
forward(["pacman", "-S", "r23-forward-foreign"], run)
```

Semantics: `run` and `forward` are both module-level defs; `run.__globals__` is the module dict.
`argv` inside `run` is a free name resolved late (LOAD_GLOBAL) in `run`'s defining namespace.
`forward`'s first parameter `argv` shadows the global *only inside `forward`'s frame*; binding a
parameter never mutates the module global, and name resolution in `run` never consults the caller's
frame (no cell sharing — `run` is not nested in `forward`). So `callback()` → `run()` executes
`subprocess.run(["pacman","-Q","r23-forward-global"])` exactly once; the foreign
`pacman -S r23-forward-foreign` list is constructed and passed as an argument but never executed.

Truth check: want is exactly one row `(package_query, "pacman -Q r23-forward-global", observed)`;
forbid_any `pacman -S r23-forward-foreign`. Recorded execution matches the want command set exactly,
forbidden command never executes. No Python behavior contradicts the want (the -Q list is a
literal-derived module global, never rebound, so "observed" is statically knowable).

Base failure anatomy (confirmed): the base classifier reports the foreign `-S` argv as *observed*
host_mutation — the exact caller-frame leak H4 describes — and additionally leaves `unparsed=1` on
this payload. Both are real base defects, and the exact rule fails it on rows-mismatch, forbid-tier,
and unparsed independently; a repair fixing only one would still fail.

**Verdict: truth-correct. Rule neither too loose nor too strict for this case.**

## Case 2 — CallerLocalShadowsHelperGlobal (exact)

Fixture code:

```python
import subprocess
argv = ["pacman", "-Q", "r23-local-global"]
def helper():
    subprocess.run(argv)
def caller():
    argv = ["pacman", "-S", "r23-local-foreign"]
    helper()
caller()
```

Semantics: `caller`'s `argv = [...]` is a plain local binding (no `global` statement), local to
`caller`'s frame. `helper` resolves `argv` late in the module globals → the `-Q` list. The local
assignment cannot and does not touch the global. Executed argv: `pacman -Q r23-local-global`, once;
`pacman -S r23-local-foreign` is constructed but never executed.

Truth check: want exactly one row `(package_query, "pacman -Q r23-local-global", observed)`; forbid
`pacman -S r23-local-foreign`. Recorded execution matches; forbidden never executes.

Base failure anatomy (confirmed): base (fully parsed here, unparsed=0) reports the forbidden
`pacman -S r23-local-foreign` as *observed* host_mutation and misses the `-Q` entirely — it
propagates the caller local into the helper's frame. Same H4 leak through an assigned local instead
of a parameter, as the case `why` states.

**Verdict: truth-correct. Rule neither too loose nor too strict for this case.**

## Pass-rule analysis (exact kind, as applied to these two cases)

- Not too strict: the wants equal the executed argv sets exactly (truth-verified); class
  `package_query` for `pacman -Q` matches the set's own convention on its passing cases; demanding
  `evidence: observed` demands nothing Python does not permit a correct static analysis to claim
  here, since the executed values are module-global literal lists with no intervening rebinding.
- Not too loose: rows must equal the want set exactly (no extra findings, no other class/tier,
  no missing row), `eval_unparsed + unparsed_spawns` must be 0 (a tool cannot pass by failing to
  parse and staying silent), and the forbid command may not appear at *any* evidence tier. The
  forbid check is redundant for exact cases (an extra row already breaks sorted equality) but
  harmless. The only residual channel to "pass while wrong" is a tool that is right on these two
  fixtures and wrong elsewhere (e.g. hardcoded answers, or correct only for module-global literals
  but leaking on rebound globals) — that is cross-fixture, and the set's other eight cases
  (LateGlobalRebinding, ForwarderPassesCallerArgument, NestedDefReadsDefiningFrame, …) plus the
  no-harm corpus comparator are the designed counterweight, not this pair's job.
- Present-kind contrast (not my cases): `want_present ⊆ {observed|lead}` accepts any class and any
  evidence tier and ignores extra rows, so it is deliberately a recall-only bar. Correct as
  registered for the two callback-store cases; noted only as context.

## Residual risks / verification gaps

- truth.py's fake `subprocess` records `" ".join(argv)`; a fixture passing non-string argv elements
  would crash the child — not reachable for these two cases (string lists only).
- My truth and measure runs each happened once, as mandated; conclusions rest on those single runs
  plus the pinned hashes (all verified above). I did not re-run to confirm determinism.
- The `safe()` gate bans `globals`/`getattr`/etc., so truth cannot be fooled by dynamic attribute
  tricks in these fixtures; the fixtures use none.

## Verdict line

ForwarderInvokesCallback: **truth-correct** (executed argv `pacman -Q r23-forward-global`; want and
forbid match Python semantics; base fails it with the H4 frame leak + unparsed, before-receipt
confirmed). CallerLocalShadowsHelperGlobal: **truth-correct** (executed argv
`pacman -Q r23-local-global`; want and forbid match Python semantics; base fails it with the same
leak through an assigned local, before-receipt confirmed). Pass rule for both exact cases: neither
too loose nor too strict.
