# RevC1Counter — attack on `quality/counters/c1-r40-live.py` (PRED-C1-r40-v1, frozen 5e7e8852)

Counter read at freeze `5e7e88525cc539563de7746361b2650802e81809`. All scored runs used the declared
counting command with `--rev HEAD` (HEAD = `e2b51d3b3f79768282914d57c1fa32cc85dcb06a`, capture present
there: 70 lines, clause k=1; base tool has no `--live`, clause-a precondition holds). Baseline sanity:
the throwaway reference tool scores `fixtures=13/13 clauses=a:1 b:0 g:1 k:1 verdict=TARGET_MISSED`
(selftest 71/71) — matches the registration's declared control behavior, so the run recipe is good.

Exploit tools (this seat dir): `rev-replay.py` (clean), `rev-replay-variants.py` (switchable defects,
env-gated), evidence logs `ev-*.log`. No tools were installed (system python 3.14.8 + git only).

## Findings by severity

### S1 CRITICAL — the docstring's anti-replay claim is false: a tool that never converts passes TARGET_MET
`run_tool` (:451-457) spawns the scored tool **without `cwd`** — the tool inherits the counter's cwd,
the lane root (only the `--selftest` call :649-651 sets `cwd=tmp`). The fixtures are seeded
`sha256(REV:i)`, and REV is ambient-readable: at both declared scoring points ("the data commit and
the tip", run as `cd lane && python3 -I … --rev <rev>`) REV == `git rev-parse HEAD`. `rev-replay.py`
therefore rebuilds all 13 fixtures (generator copied verbatim from the frozen counter), identifies the
fixture by config bytes, and prints `Fixture.want()` labels. It converts **nothing**:

    PRED-C1-r40-v1 clauses=a:1 b:1 g:1 k:1
    PRED-C1-r40-v1: fixtures=13/13 tool=present verdict=TARGET_MET rev=e2b51d3… EXIT=0

The docstring asserts "a tool that replays recorded output cannot pass; it has to convert and
compare" — falsified. Two amplifier details:
- `random` is deliberately absent from `STDLIB_ALLOW`, which blocks an honest `import random` — the
  anti-replay measure — but `imports_ok` (:584) is a pure AST scan, so `exec("import random as _rd")`
  walks through. The clause-g blindspot is load-bearing for the block's defeat.
- Hardening `cwd=tmp` does NOT close it: the tool can read the frozen counter at its known absolute
  path (or embed the generator) and locate the lane by absolute path. Any fixture set derivable from
  public, ambient state is replayable by construction. Durable fix: mix a per-run nonce into the seeds
  (log it for triage); otherwise widen the declared residual to name generator replay explicitly.

### S2 HIGH — clause b (selftest) is pure stdout attestation, satisfiable by a hardcoded line
The counter regexes `MADO_OPTIONS_SELFTEST: (\d+)/(\d+) passed` + rc 0 + k==n≥79 (:649-656). Both
exploit tools print `MADO_OPTIONS_SELFTEST: 79/79 passed` unconditionally and run no selftest logic;
every scored run shows `clause=b rc=0 selftest=79/79` → b:1. The predicate's clause b cannot
distinguish a real 79-assertion selftest from an echo.

### S3 HIGH — the row `live` payload is presence-checked only; fabricated evidence passes
`check_live` only tests `r.get("live") is None` (:519-522) — it never compares the live value against
what the stub actually answered, although the counter knows `fx.table()`. Variant `FABLIVE` labels
every row from `want` with `live:"FABRICATED"`, never reading reply values
(`ev-fablive.log`: "reply value never read" on every key):

    fixtures=13/13 … clauses=a:1 b:1 g:1 k:1 → TARGET_MET EXIT=0

This is the round-39 D2 over-label class: the counter's own output cannot detect declared-echo.

### S4 MEDIUM — hostile-probe enforcement is argparse's accident; the `-`-prefix rule is untested
`score_hostile` (:570-580) sends space-syntax `--probe -x|--version|""`. argparse rejects the dash
values before any tool code runs: `error: argument --probe: expected one argument`, rc=2, message
contains "probe" — exactly the asserted condition, with zero stub calls. A tool with **no refusal
logic at all** passes two of the three legs; the M10 control mutant (`if False:` replacing the
refusal, ctl/run-c1-controls.py:45-46) can only bite via the `""` leg. The rule "empty **or starts
with `-`**" is thus only tool-exercised for `""`; dash keys that argparse accepts as values
(negative numbers) are never sent. Demonstrated: with equals-syntax the `HOSTILEHARD` variant
(refusal hardcoded to exactly `{"-x","--version",""}`) forwarded `getoption -j -rf` and
`getoption -j -1` into compositor argv (stub log shows both lines) while scoring `13/13 → TARGET_MET`.

### S5 MEDIUM — no-write / no-extra-program verified only on valid runs; failure paths unchecked
`tree_listing(home)` comparison (:497) exists only in `check_live`; `score_fail`, `score_missing` and
`score_hostile` re-check neither tree nor argv on the negative legs. Variant `NEGWRITE` wrote
`<home>/.config/hypr/.pwned-failure` during the fail0/bad0/missing0 runs and `.pwned-hostile` on the
hostile refusal (`ev-negwrite.log` names all four paths under `/tmp/mado-c1-r40-72b8gq52/`) —
`fixtures=13/13 … TARGET_MET EXIT=0`. Separately, "runs no other program" is unenforceable: the
replay tool ran `git rev-parse HEAD` throughout scoring, invisible to the stub's calls.log.

### S6 MEDIUM — clause g AST scan is string-blind (exec-import bypass)
`MADO_EXPLOIT_EXEC=1` run: `exec("import socket as _sk")` executed at module level in all 20 scored
invocations (`ev-exec.log`), `clauses=… g:1 … TARGET_MET`. No static check can fully close this; a
cheap heuristic (reject string-literal `import` inside top-level `exec(`/`eval(` calls) plus an
honest residual is the practical hardening.

### S7 LOW — failure naming checked by substring, not precision
`score_fail`: `named = victim in err` (:556). `ALLKEYS` variant exits 5 with **all 15 keys** on
stderr (`ev-allkeys.log`: "failing key was ['optfail13:ginh13']" while stderr listed all) → named=1,
13/13, TARGET_MET.

### S8 LOW — duplicate rows collapse silently
`got = {r.get("key"): …}` (:507) last-wins. `DUP` variant emitted 30 rows for 15 keys
(`ev-dup.log`), TARGET_MET.

### S9 INFO — universal docstring clauses no fixture enumerates (static; input unreachable in fixture space)
- "an answer with **no known form** … exits 5": `Fixture.table()` and `expect_extra` always emit a
  known form; no stub mode produces a form-less record. A tool that crashes or exits 0 on such
  replies is untested.
- Float "stof" edges, str "exact trimmed equality" (no whitespace generated), uppercase hex,
  comment-suffix handling beyond "on # note": stated as the conversion contract, outside the
  generator's value space (adjacent to the declared hardcoding residual, but the docstring presents
  them as enforced).
- Transient write-then-delete during a *valid* run evades the `tree_listing` diff.
- A probe answered with malformed JSON is unspecified and untested.

### Determinism
Generation is hash-seeded (`sha256(REV:i)` / `REV:tag`), wall-clock-free, `sorted()`-normalized —
stable across re-runs at a fixed rev (observed: identical fixtures/labels across all 9 scored runs).
Residual wall-clock risks: `run_tool` timeout=60 and selftest timeout=300 are environmental flake
points under this machine's load; no minimum-runtime or retry logic. The REV-seeding itself is the
S1 weakness: deterministic public seeds are exactly what makes replay possible.

## Recommended hardening (next-round predicate; counters are frozen this round)
1. Per-run nonce mixed into fixture seeds (echo the seed in diagnostics) — kills S1 and recorded-output caching simultaneously; `cwd=tmp` in `run_tool` is still worth adding but is not sufficient.
2. Cross-check every row's `live` against the stub's emitted value; require exactly one row per expected key (kills S3, S8).
3. Negative legs: re-check tree listing + argv after fail/bad/missing/hostile runs (kills S5).
4. Hostile fixture: add equals-syntax probes (e.g. `--probe=-1`) so tool logic, not argparse, is exercised (kills S4).
5. Failure naming: require stderr to name exactly one fixture key equal to the victim (kills S7).
6. Either give the selftest observable teeth or demote clause b to attestation in the docstring (S2).
7. Add a no-known-form stub mode (S9); ban `exec(`/`eval(` string-imports as a heuristic with a declared residual (S6).

## Residual risk / verification gaps
- I did not re-run the 16 C1 mutants; M10 was read statically (ctl/run-c1-controls.py:45-46). The registration's `CTL_C1 controls=18 correct=18/18` is taken as declared, not re-verified.
- The replay exploit is conditioned on REV==HEAD at scoring time (true at both declared scoring points); I did not test a non-HEAD `--rev`.
- No lsp device is mounted in this session; all checks are text + runtime evidence (grep/read of the frozen source, executed exploits).
- Claim unchanged as declared: TARGET_MET is reachable by a tool that resolves/converts nothing, so this round's C1 verdict measures tool presence + fixture mechanics, not conversion fidelity. The out-of-distribution live host receipt (70/70) remains the only fidelity evidence, as the registration already flags for the hardcoding residual — it now also carries the replay residual.
