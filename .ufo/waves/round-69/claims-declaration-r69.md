# mado round 69 — frozen claims, predicates, controls and recipes

author: mado L1 (planner seat held by the L1; no planner seat is dispatched — validator rejects it)
date: 2026-11-03/04 (America/Sao_Paulo)
base: `04093b83f73a841117d3b31dbb2a6063f4f2a454` (lane tip at round start; round 68 closed there)
round: mado lane round 69, hyaku run 15, ONE v1 wave (12 seats)
status: **FROZEN before any candidate data.** Nothing below may be re-scoped, narrowed or
re-worded after a seat has scored it. Two claims, distinct axes, causally separable.

## Axis posture

Every published finite sub-axis sits at its measured maximum at round start — navigation
`indexed=80/80`, calibration resolved-active `86/86`, operability selftest `12/12` at the
round-68 measured content, hermetic gate `MADO_SELFTEST: 460/460` — so no axis is distinctly
lowest; this is the rounds 56–68 posture. The stagnation nudge does **not** apply: the last
capability row entered at round 68 and the stagnation window is `N = 3`
(`SCORECARD.md` § Saturation), gap 0 < 3. Both claims therefore take **new finite
denominators** declared here before data: C1 a new three-recipe set, C2 a new eleven-case
control set. Neither is a re-scoring of a rule the lane already holds (the do-nothing control
scores are 0/3 and 7/11 below, not published base sub-axis values).

## C1 — calibration: the hardened control harness kills paired (decision + oracle) forgeries

**Surface changed.** `quality/counters/c1-r69-landing-controls.py` — the successor of the
round-68 harness `quality/counters/c1-r68-landing-controls.py`. Same measurement body; the
selftest now drives decision **and** oracle together: a crashing M-R child is not a kill, an
M-Z run with no assertion summary is not a kill, and the hermetic spawn guard is itself
asserted live (an attempted spawn under the guard must raise).

**Frozen predicate (one sentence, the counter's code and the receipt label are this sentence).**
At `REV`, `quality/counters/c1-r69-paired-recipes.py` extracts
`quality/counters/c1-r69-landing-controls.py`, runs its `--selftest` (rc must be 0), applies
each of the three frozen recipes R1/R2/R3 exactly once to a scratch copy (`applicable=no` if a
recipe's text does not occur exactly once), and counts a mutant **killed** iff its own
`--selftest` exits nonzero; the same three recipes are applied at `--base-rev` to the
round-68 harness, which must survive all three (`base=0/3`).

**Counting command.**

```sh
python3 quality/counters/c1-r69-paired-recipes.py --repo . \
  --rev <measured-content> --base-rev 04093b83f73a841117d3b31dbb2a6063f4f2a454 \
  --scratch-root <scratch>
```

**Contract line (exact).**

```
MADO_R69_PAIRED_RECIPES: selftest=<rc|absent> killed=<n>/3 applied=<k>/3 base=<m>/3 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>
```

**Frozen recipes (each text must occur exactly once in the candidate and once in the r68 base
harness; both counts are asserted before scoring).**

- **R1 — crash credited as a kill (M-R decision loses its oracle term).**
  old (two lines, 12 + 29 spaces of indentation):
  `mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker)` newline
  `and forged_credit(mr_rc, mr_marker))`
  → new: `mr_killed = bool(u_ok and not control_ok(mr_rc, mr_marker))`
- **R2 — unparseable mutant run credited as a kill (M-Z decision loses its summary oracle).**
  old: `mz_killed = mz_rc != 0`
  → new: `mz_killed = mz_rc != 0 or mz_summary == "none"`
- **R3 — hermeticity oracle removed (the selftest's own spawn guard is dropped).**
  old: `subprocess.run = _no_spawn`
  → new: `pass  # spawn guard removed by recipe`

The exact byte strings, with their real indentation, are the ones recorded in
`.ufo/waves/round-69/control-baseline-r69.txt` (each `RECIPE <name> occurrences=1` line); the
counter embeds them literally.

**Target.** `selftest=0 killed=3/3 applied=3/3 base=0/3` → `verdict=TARGET_MET`, rc 0.
Bounded score `10 × killed / 3`. Before at base: the harness is absent at `04093b83`
(`selftest=absent killed=0/3 applied=0/3 base=0/3`) → 0.0000.

**Do-nothing control (committed before freeze).** Keep the round-68 harness and apply the same
three recipes: `killed=0/3 applied=3/3` — all three survive its green 52/52 selftest
(`.ufo/waves/round-69/control-baseline-r69.txt` § C1 base). The claimed work is therefore
required by the counter, not by the recipe text.

**Not claimed.** Universal fault coverage; that the three recipes are the only forgeries; that
an outside attacker cannot reforge the printed line; runtime behaviour of the extracted
instruments (the harness's real-children leg stays the harm-watch leg); that `R1`/`R2`/`R3` are
equivalent to any historical round-68 recipe (they are not — `RevC1`'s recipe **L**
`mz_killed = mz_rc != 0 or mz_rc is None` is an *equivalent* mutant: the frozen text sits
inside `try:` after `mz_rc = r.returncode`, so `mz_rc` is always an int there; the baseline
receipt's § L probe shows the mutant keeps a green 59/59 selftest, and it is **excluded** from
the frozen set — it is mined as this round's mistake).

## C2 — operability: the guard census requires key position and dominance, not a mention

**Surface changed.** `quality/counters/c2-r69-guard-dominance.py` — the successor of
`quality/counters/c2-r68-reader-guard.py` over the same frozen population (the tracked
`quality/check-[^/]+\.py` files). Two rule changes, both new predicates rather than edits of the
round-68 rule:

1. **Key position.** The guard key `GIT_NO_REPLACE_OBJECTS` counts only where it is a *key* of
   an environment mapping — a dict-literal key, a subscript store `env[KEY] = …`, an
   `update`/`setdefault` keyword, or a `dict(KEY=…)` keyword. A string with the same value in
   value position is not a guard (`{ "LABEL": "GIT_NO_REPLACE_OBJECTS" }`).
2. **Dominance.** The guarded environment must reach a process launch of `git` (a call whose
   argv literal, or a name bound to an argv literal, contains `git`), by one of three flows
   confined to one module: (a) inline `env=<guarded mapping>` at that call; (b) an env-named
   name bound to a guarded mapping (or to a local *producer* function that returns one), used
   as `env=` or as an argument at that call, with no intervening rebinding of the name to a
   mapping without the key; (c) the guarded name passed as an argument to a locally defined
   function whose env-named parameter is passed as `env=` at that call. Constructions inside a
   literal-false branch (`if False:` / `while False:`) do not count.

**Counting command.**

```sh
python3 quality/counters/c2-r69-guard-dominance.py --repo . --rev <measured-content> \
  --base-rev 04093b83f73a841117d3b31dbb2a6063f4f2a454 \
  --controls .ufo/waves/round-69/controls/c2-controls-r69.json --scratch-root <scratch>
```

**Contract line (exact).**

```
MADO_R69_GUARD_DOMINANCE: population=20 readers=13 guarded=13 unguarded=0 controls=<n>/11 base_controls=<m>/11 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>
```

**Frozen control set.** `.ufo/waves/round-69/controls/c2-controls-r69.json`, 11 cases, sha256
`975ca3ba37341b5a058dec4fa76278d548996738e8b517616181824a841f90b9`:
`guarded-inline`, `value-position-only`, `dead-branch-only`, `uncalled-helper`,
`overwritten-env`, `update-guard`, `subscript-guard`, `module-constant`, `producer-helper`,
`argv-name-flow`, `mention-only`. Every case carries `expect_reader` and `expect_guard`; the
counter scores a case correct only when both match, and refuses a control file whose case count
is not 11 or whose sha256 differs from the frozen digest.

**Target.** `population=20 readers=13 guarded=13 unguarded=0 controls=11/11 base_controls=7/11`
→ `TARGET_MET`, rc 0. Bounded score `10 × guarded / readers` = 10.0000 (12 → 13 at the base of
the round-68 work; the population is 13/13 already at `04093b83` — this claim moves
**discrimination**, not the count, and says so). Before at base: the r69 counter does not exist
→ missing counter, rc 1; its *rule* (the r68 classifier) scores `controls=7/11` on the same
frozen set.

**Do-nothing control (committed before freeze).** The round-68 classifier on the frozen 11
cases: `7/11` — it accepts `value-position-only`, `dead-branch-only`, `uncalled-helper` and
`overwritten-env` (`.ufo/waves/round-69/control-baseline-r69.txt` § C2). The r69 prototype
scores `11/11` and reads `population=20 readers=13 guarded=13 unguarded=0` at the base
revision.

**Sourced ground.** This claim lands `corpus/knowledge/gate-guard-dominance-r69.md` and a new
registry row **S438** (`git v2.56.0 Documentation/git.adoc`: `--no-replace-objects` "is
equivalent to exporting the `GIT_NO_REPLACE_OBJECTS` environment variable", and the variable
acts only when "setting and exporting" it). The documented fact is the dominance ground: a
guard that is merely *constructed* is not in effect for any child; only the environment handed
to the process carries it. The row is drafted by a scribe, opened independently by the scout,
and admitted only through the lane's Gate.

**Not claimed.** That the dominance rule is sound for arbitrary Python (it is a bounded
syntactic approximation: one module, one hop, no alias/attribute/container flow, no
path-sensitivity beyond a literal-false branch, no cross-module producer); that a guarded
environment makes the guard effective at runtime (value not interpreted; `GIT_NO_REPLACE_OBJECTS=0`
also disables); that the 20-file population is the lane's whole reader set (r67's wider lexical
set stays outside); that the register of `quality/` is exhaustive; state truth of any
`PROVINCE.md` cell.

## Causal separability

C1 changes `quality/counters/c1-r69-landing-controls.py` and adds
`quality/counters/c1-r69-paired-recipes.py`; C2 changes a different file
(`quality/counters/c2-r69-guard-dominance.py`) with its own frozen control JSON. Each counter
is extracted from the same `REV` but reads only its own artifacts, and each can be run alone;
neither touches the other's target. The two claims share only the wave and the lesson.

## Harm watch (every claim)

- Standing landing instrument at the measured content: `MADO_LANDING_COUNTERS: GREEN`
  (`nav`, `usedby`, `ledger`, `citecheck` all rc 0), navigation `indexed=80/80`.
- Hermetic suites: gate `MADO_SELFTEST: 460/460`; landing selftest; C1 counter and harness
  selftests; C2 counter selftest; the unchanged r68 counters at their pinned revisions.
- Axis table: `python3 quality/check-axis-scores.py` reports no mismatch at the measured
  content (the round-68 publication cadence item rides this round).
- No desktop probe, compositor/socket/service write, package-manager transaction,
  `MANIFEST.json` edit or sibling-lane write. r68 files stay at their revisions; no alias or
  compatibility shim is added for any predecessor counter.

## Exploration, assimilation, frontier

- **Exploratory claim:** none. Both claims are measured.
- **Assimilation:** `none` this round (declared; the shokuknow package work is not taken).
  `considerthese/2026-10-28.md` proposal 4 (a live-tool table: question answered, last live
  run, verdict, who ran it) is mined at most as one QUALITY criterion/lesson pointer if it
  fits C2; it adds no claim slot.
- **Frontier step (§2b):** `corpus/SOURCES.md` census at round start is exit 0 (374 rows,
  existing W04/W01 warnings); C2's entry cites the new row S438 opened this round; one
  mistake (the equivalent-mutant misclassification above) is mined into
  `corpus/lessons/round-69.md` § Mistakes with class, evidence, captured-by and fix.
