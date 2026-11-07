# mado round 99 — claims declaration (hyaku run 15, attempt 2)

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`, base
`2cbaa141f42df9dfeee4d207cae6558a4dd59863` (= the round-98 closure tip; `jj-lane.sh state` ahead=0
behind=0, tracked=0 untracked=0 at declaration time). This file is the round's contract. The L1
(`MadoR99a2`) holds the canonical planner seat; wave `w1` builds and falsifies against this text.
The `## Freeze block` at the end is filled only after the wave returns and the controls are scored;
nothing above it is widened after any seat has scored.

Axis posture: SCORECARD saturation 9.0 / stagnation window N=3; the round-98 section records every
owned axis at 10, so the lowest-axis duty is a tie and either axis may carry the round. Two claims,
two distinct axes, causally separable (each counter runs at the base with the other's artifact
absent). No exploratory claim. `Assimilation: none` (the staged `merge/mado/` package holds no entry
on the launch-environment plane; checked this round).

## C1 — coverage (capability, new surface): the launch spawn environment

**Claim.** At the base revision no lane tool answers what surrounds the argv vectors: the load-time
program gate, the `Terminal=true` terminal selection and prepend, the `Path=` working directory, the
post-prepend `argv[0]` program lookup, and the `GIO_LAUNCHED_DESKTOP_FILE` environment value. After
this round `tools/mado-launchenv.py` answers all five, read-only, for one desktop file, a list of
arguments and a `PATH` string, scored against the installed `/usr/bin/gio` on a frozen case set.

**Surface (glib 2.90.1, `/usr/bin/gio` sha256 `d2164260…c462`).** Sources opened this round:
`gdesktopappinfo.c` (r98 pin, re-opened), `gutils.c` (new: `g_find_program_for_path`),
`gio-tool-launch.c` (new), the Desktop Entry Specification's `Terminal`/`Path` keys (new row).

**Rules the candidate must model** (each cites its line; the seat verifies, the L1 freezes):

- R1 load gate: after `g_shell_parse_argv(Exec)`, `g_find_program_for_path(argv[0], NULL, Path=)`
  (`gdesktopappinfo.c:1976-2004`); NULL → the file does not load (`gio` prints `Unable to load
  application information for ‘<path>’`, exit 1). The PATH here is the *process* PATH, and the
  working dir is the entry's `Path=` value.
- R1b `TryExec`: when present and non-empty, `g_find_program_for_path(TryExec, NULL, Path=)`
  (`gdesktopappinfo.c:1946-1960`) runs *before* the Exec check and its failure is the same load
  refusal. Order: `Path` read, `TryExec` check, `Exec` check.
- R2 terminal: `Terminal=true` → walk the twelve `known_terminals` in table order
  (`gdesktopappinfo.c:2765-2778`), each through `g_find_program_for_path(name, PATH, Path=)`
  (`:2797-2806`); first hit wins; prepend `[found]`, plus the row's `exec_arg` when non-NULL
  (`:2814-2830`). No hit → `Unable to find terminal required for application`
  (`:3027-3032`), `gio` exit 1.
- R3 `argv[0]` after the prepend: keep it when absolute, executable and not a directory; else
  `g_find_program_for_path(argv[0], PATH, Path=)` and replace (`:3053-3084`); NULL →
  `Program ‘<x>’ not found in $PATH`, `gio` exit 1.
- R4 cwd: `g_spawn_async_with_fds(info->path, …)` (`:3116-3126`) — the child's cwd is `Path=`; an
  empty `Path=` inherits the launcher's cwd (measured); a `Path=` that cannot be entered fails the
  spawn (`gio` prints `Failed to change to directory “<path>” (No such file or directory)`, exit 1)
  — the refusal cause `cwd-failed` (measured this round).
- R5 env: `GIO_LAUNCHED_DESKTOP_FILE` = `info->filename` (`:3036-3040`).
- R7 the load gate also refuses an `Exec` whose `argv[0]` names a directory (the `!IS_DIR` half of
  `gutils.c:352-356`), measured: `Exec=<a directory>` prints `Unable to load application information`
  and exits 1.
- R6 `g_find_program_for_path` semantics (`gutils.c:300-500`): `working_dir` + a non-absolute
  program → `working_dir/program`; absolute program or a `/` in the original → executable and not a
  directory test only; otherwise walk PATH (unset PATH → `/bin:/usr/bin:.`), an empty PATH entry
  means the current directory, a relative candidate is joined to `working_dir`, and a relative hit
  is returned absolute against the process cwd.

**Before → after (frozen predicate).**

```
PRED-C1-r99-v1:
  TARGET_MET iff  cases_correct == cases_total
              AND classes_covered == classes_total
              AND mutants_killed == mutants_counted
              AND fresh_correct == fresh_total
              AND control_naive_correct  < cases_total
              AND control_held_r98_correct < cases_total
```

- `cases_total` = the frozen case count; `classes_total` = the frozen class list length; every case
  label is measured twice against `/usr/bin/gio` with agreeing results before freezing.
- `mutants_counted` = the frozen counted-mutant list; each `find` occurs exactly once in the
  non-selftest code and the mutant must make at least one frozen case mismatch.
- `fresh` = a generator seeded at measurement time, labels written outside the candidate's reach.
- `control_naive` = `Exec.split()` + no environment model, scored by the same counter.
- `control_held_r98` = the committed round-98 `tools/mado-execargv.py` (argv only, no environment),
  scored by the same counter over the same cases.
- Counting command (full pinned argv in the freeze block):
  `python3 -I quality/counters/c1-r99-launchenv.py --repo . --rev <rev> --base-rev 2cbaa141… --cases … --mutants … --genseed … --expect-… --scratch-root DIR`
- Separability at base: the counter prints `SETUP_ERROR … tools/mado-launchenv.py absent at
  2cbaa141` (exit 2).

**Named limits (declared now).** The spawn *order* of multi-spawn launches is not modelled (the r98
limit carries). `DBusActivable`, the `gio-launch-desktop` wrapper's own environment scrubbing, the
portal path and whether the process survives are not modelled. The model answers the argv, the cwd
and the one env value; it does not start anything.

## C2 — operability: the harm watch as an instrument

**Claim.** At the base revision no instrument enumerates the lane's harm-watch legs: the round-98
watch was an ad-hoc shell list whose first run had 28 legs and whose final run had 26, and the two
dropped legs (`r97c1_filetype`, `r97c2_counter_selftest`) were noticed only by the outside
spot-check (defect 5). After this round `quality/harm-watch.py` replays a frozen panel of legs, each
with a frozen expectation (`rc` + a stdout marker), and its census fails closed on a leg the panel
declares but does not carry.

**Rules.**

- The panel (`.ufo/waves/round-99/controls/harm-panel-r99.json`) declares `expect_legs` (an integer),
  `rounds` (round → the leg ids that round contributes) and `legs` (rows: `id`, `round`, `argv` with
  a `REV` placeholder, `expect_rc`, `expect_marker`, `note`).
- Census before running anything: `PANEL_LEG_COUNT` (row count ≠ `expect_legs`), `PANEL_DUPLICATE`
  (an id twice), `PANEL_ROUND_MISSING` (a declared round with no row), `PANEL_LEG_UNKNOWN` (a row
  whose id is not in `rounds`), `PANEL_LEG_MISSING` (a declared id with no row). Any census finding
  exits 2 without running a leg. **Net-of-findings rule (frozen here, derived before any data):**
  `PANEL_LEG_COUNT` fires only when the row-count delta is not fully explained by the other findings
  (explained = unknown rows + duplicate surplus − missing ids), so a dropped leg reports exactly one
  `PANEL_LEG_MISSING <id>` and an extra row reports exactly one `PANEL_LEG_UNKNOWN <id>`. The rule is
  stated in the gate's docstring and in the panel's top-level `census_rule` key, so a reader
  re-deriving the census gets the observed answer.
- Then every leg runs with a timeout under `--scratch-root`; `HARM_WATCH: legs=N ok=M mismatch=K`
  plus one `LEG <id> rc=<n> expect=<n> marker=<ok|MISS>` line. Exit 0 iff `K == 0`, 1 on a mismatch,
  2 on setup/census.
- Controls: a planted panel with one row removed must exit 2 with exactly one `PANEL_LEG_MISSING`
  naming the removed id; a planted panel with an undeclared extra row must exit 2 with exactly one
  `PANEL_LEG_UNKNOWN`; a planted panel with a wrong `expect_rc` must exit 1 with exactly one `LEG …`
  mismatch; a planted panel with the SAME rc and an impossible marker must also exit 1 with exactly
  one `LEG …` mismatch (this separates the marker test from the rc test, added before data on the
  round-99 critic's counterexample); a marker-blind copy of the gate must score TARGET_MISSED on the
  real panel; an always-OK stub must be flagged (it reports `ok=N` while a planted panel is red).

**Before → after (frozen predicate).**

```
PRED-C2-r99-v1:
  TARGET_MET iff  panel_legs == declared_legs
              AND panel_legs >= 20
              AND legs_run == panel_legs
              AND mismatches == 0
              AND planted_dropped_leg_flagged == 1
              AND planted_wrong_expect_flagged == 1
              AND planted_wrong_marker_flagged == 1
              AND marker_blind_flagged == 1
              AND stub_flagged == 1
              AND selftest_checks >= 12 AND selftest_failed == 0
```

- Counting command:
  `python3 -I quality/counters/c2-r99-harm-watch.py --repo . --rev <rev> --base-rev 2cbaa141… --panel .ufo/waves/round-99/controls/harm-panel-r99.json --expect-panel-sha256 160763ce… --planted-dir .ufo/waves/round-99/controls/harm-planted --expect-gate-sha256 … --scratch-root DIR`
- Separability at base: `SETUP_ERROR … quality/harm-watch.py absent at 2cbaa141` (exit 2).
- The before is the r98 receipts: `receipts/harm-base-r98.txt` has 28 `LEG` lines,
  `receipts/harm-final-r98.txt` has 26, and no committed instrument reads either count.

**Named limits.** The panel freezes the expectations measured at this round's tip; a later tree that
legitimately changes a leg's rc must re-freeze the panel in that round (the tool reports the
mismatch, it does not decide which side is right). Legs that declare `SETUP_ERROR` keep that rc and
are labelled in the row's `note`. The tool does not repair anything and does not run the round's own
new counters (a round cannot harm-watch itself).

## Record repairs riding this round (not claims)

The round-98 outside spot-check routed eight defects; each is fixed here or answered in the report:
D1 the S532 registry row, D2 the registry gate re-run at the records tip, D3 the `SKILL.md` r98 rows'
stale pins, D4 the `LOG.md` round-98 entry (seed and mistake count), D5 the two dropped harm legs
(this is C2's panel), D6 a `QUALITY.md` criterion for M98-1's class, D7 report ordering (process),
D8 the C2 commit attribution (erratum).

## Freeze block

(filled after the wave returns and the controls are scored)
