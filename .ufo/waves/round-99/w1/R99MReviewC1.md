# R99MReviewC1 -- C1 review: the launch spawn environment

Seat: reviewer, wave w1, round 99 (hyaku run 15, attempt 2). Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`2cbaa141f42df9dfeee4d207cae6558a4dd59863`. Contract read:
`.ufo/waves/round-99/claims-declaration-r99.md` (C1 and the frozen predicate
`PRED-C1-r99-v1`). I edited nothing in the candidate, the oracle, the counter or the case file;
every measurement below is from my own scratch instruments, and the receipt is
`.ufo/waves/round-99/receipts/review-c1-r99.txt`.

## 0. What I ran

- My own case plane: **92 cases / 41 classes**, built and labelled by me (the seat item asks for
  >= 20 cases over >= 10 classes). Two runs on fresh roots for the first four batches: **zero
  semantic disagreements**; the fifth batch (argument resolution) was measured once, its labels
  being deterministic.
- The frozen case file (67 cases / 31 classes), re-derived independently: roots built by my
  runner from the frozen bytes, the envelope's probe bytes, the `env -i` command from contract 2.
- The candidate on both planes, at two revisions (70fe43d0 and the fixed a63c20c8), scored with
  my comparator and with the counter's own `score_case`.
- The two controls from the declaration, scored on the frozen cases with my comparator.
- The candidate source, read for spawn and IO.

## 1. Independent re-derivation of the frozen labels

The frozen file is behaviourally sound: **67/67 labels reproduce**. Every frozen refusal refuses
(rc 1, no child), every frozen launch launches with the frozen count, argv multiset, cwd and
`env_gdf`. Three rows differ only in the *cause name* when the cause is derived from gio's
stderr alone (`rf-badescape`, `rf-quote`, `rf-notkeyfile`); all three refuse, and the candidate
agrees with the frozen label in all three. So this is a vocabulary observation, not a label
defect -- see F2.

The 49 launch expects all carry `cwd` and `env_gdf` (0 missing), which the counter's strict
comparator needs (F6).

## 2. The candidate on the same cases

Scored with the counter's own scorer (`score_case(..., mode="candidate")`, the oracle module
loaded as its builder; the counter's `--selftest` is green, `checks=18 failed=0`):

| candidate sha256 | frozen cases | misses |
|---|---|---|
| `70fe43d0...7979` | 65/67 | `ac-rel`, `ac-dot` |
| `a63c20c8...eb16` | **67/67** | none |

The two misses at 70fe43d0 were the `arg-conv` class: the model passed a relative file argument
through verbatim (`args/a.txt`, `./args/a.txt`) where gio builds every argument with
`g_file_new_for_commandline_arg` (`gio-tool-launch.c:116`) and the child receives the lexical
canonical absolute path. Measured on `/usr/bin/gio` (cwd = case root): `args/a.txt`,
`./args/a.txt` and `args/../args/a.txt` all reach the child as `<root>/args/a.txt`;
`args/../a.txt` as `<root>/a.txt`. That was predicate-failing and is fixed at a63c20c8; I
re-scored the fixed bytes myself (67/67) and re-ran my own 92-case plane against them.

My own plane at a63c20c8: 86/92 with six rows, none of them candidate behaviour:
`at3-bad-escape` and `at3-unbalanced-quote` are the cause-name vocabulary question (F2);
`at2-exec-absent` and `at3-no-exec-key` are my stderr-only classifier's missing `no-exec`
mapping (the candidate's `no-exec` is the frozen construction label, and gio's line is
"Desktop file didn't specify Exec field"); `at2-unset-path-bare-exec` is my runner omitting
`--path` while inheriting a host PATH (re-run under `env -i` with PATH truly unset the candidate
answers `<root>/./probe` byte for byte); `ar-dotdot-up` is my case carrying a literal `{root}`
token inside the argument. Behaviourally the candidate is clean on the whole plane.

## 3. The two controls (declaration conjuncts)

| control | frozen score | which cases |
|---|---|---|
| `control_naive` (`Exec.split()`, no env) | **1/67** | `rf-noexec` only |
| `control_held_r98` (`tools/mado-execargv.py`, argv only) | **4/67** | the four refusal shapes |

Both are strictly below 67, so both conjuncts hold. See F5 for what the r98 control does and
does not prove.

## 4. Attack surface (the seat item's seven probes)

All seven were measured; the full table is in the receipt. The sharp ones:

- `Terminal=true` + `%f` + two arguments: two launches, each `[term, exec_arg?, prog, arg]`.
- A terminal found only through a **relative** PATH entry is returned **absolute** against the
  process cwd; with a relative `Path=` the walk joins the working dir *again*
  (`<Path>/<entry>/<name>`), and a case built that way is `no-terminal`.
- `Path=` empty and absent both inherit the launcher's cwd; nonexistent, a file, mode 000 and a
  dangling symlink are all `cwd-failed`; a symlink to a directory answers the **physical** target
  (`pwd -P`); trailing slash, `..` and `.` answer the canonical directory.
- `Exec` naming a directory -> load refusal. A bare `Exec` found only after the `Path=` join
  launches with `argv[0] = <Path>/prog` -- but only when `Path=` is **absolute**: with a relative
  `Path=` the join does not survive the reset to the original program before the PATH walk, and
  the gate refuses. `Exec="bin/probe"` with `Path=<root>/work` tests `<root>/work/bin/probe`;
  `Exec="./probe"` answers `<root>/work/./probe` (the `./` is kept).
- Absolute vs relative desktop argument: `GIO_LAUNCHED_DESKTOP_FILE` and `%k` are the same
  lexical canonical path in both (and for `./` and `../<id>/`).
- A PATH with a leading colon searches the cwd first and answers `<root>/probe`; the unset-PATH
  default `/bin:/usr/bin:.` answers `<root>/./probe` (the `./` is **not** normalised).
- Two edges the seat item did not list but the frozen set now holds: the gate parses the **raw**
  `Exec` value, so `Exec=%f`/`%k`/`%F`/`%u`/`%c`/`%i` as `argv[0]` are load refusals; and an
  **empty** `Exec` is not gated at all -- it launches with `argv[0]` = the argument when the
  argument is executable, and refuses `program-not-found` when it is not.

No false green and no false red survived at a63c20c8: every probe above is answered as gio
answers it. The false reds I found at 70fe43d0 (the two `arg-conv` cases) are fixed.

## 5. Does the tool spawn anything or read outside its inputs?

No. `mado-launchenv.py` imports `importlib.util, json, os, shutil, sys, tempfile`; there is no
`subprocess`, `socket`, `ctypes`, `os.system`, `exec*` or `eval`. It reads the desktop bytes
named on the command line, the execargv sibling by path, and -- through the
`g_find_program_for_path` port -- `os.access(X_OK)` / `os.path.isdir` on candidate paths named by
the desktop entry or the PATH string, plus the `Path=` enterability test. It reads its own
`getcwd()`, its own `PATH` when `--path` is absent, and the locale variables. It starts nothing.

## 6. Findings

### F1 (critical; fixed in a63c20c8) -- relative file arguments were not resolved

At 70fe43d0 the model echoed a relative argument; gio resolves it lexically against the process
cwd before the expansion. Frozen `ac-rel` and `ac-dot` fail, so `cases_correct == cases_total`
was false. Fixed at a63c20c8 (67/67 re-scored by me). A re-freeze that adds an argument with a
scheme (`http://...`) or a `file://` URI would need the other branch of
`g_file_new_for_commandline_arg`; the frozen set has none, and the builder records it as a named
limit.

### F2 (high; record) -- the frozen cause vocabulary is construction-first, contract 2's is stderr-first

Contract 2 says the cause is "derived from gio's exit status and stderr text" with three
mappings; the frozen file's labels for `rf-badescape`, `rf-quote` and `rf-notkeyfile` cannot be
derived that way, because gio prints one generic `Unable to load application information` line
for every load-time refusal (and a different `Unable to load '<path>': Key file contains line ...`
for the not-a-key-file case). The labels are reproducible from the case's *construction*, which
is what the oracle implements and what the candidate models; the contract text should say so, or
the three rows should be re-labelled `load`. The predicate is unaffected (candidate and frozen
file agree), but a reader re-deriving from stderr gets a different name.

### F3 (high; record) -- contract 1's cause enumeration omits `cwd-failed`

R4 names `cwd-failed` as the refusal cause for a `Path=` that cannot be entered, the oracle
implements it, the frozen set carries two `cwd-missing` cases, and the candidate emits it -- but
contract 1's list of causes (`load`, `no-terminal`, `program-not-found`, plus the r98 trio) does
not include it. A reader implementing contract 1 alone would have no cause for those two cases.

### F4 (medium) -- the cwd answer depends on process state the contract does not name

For an absent or empty `Path=` the model answers its own `getcwd()`; with no `--path` it reads
its own `PATH`. The counter pins `cwd = <case root>` and always passes `--path`, so the scored
answer is well defined, but the documented CLI run from another directory answers a different
cwd for the same desktop file. The candidate's docstring states this; the contract's input list
("one desktop file, a list of arguments and a `PATH` string") does not. Either the contract
names the launcher cwd as an input or the tool grows a `--cwd`.

### F5 (medium) -- `control_held_r98` cannot discriminate on the launch plane

It scores 4/67 and all four hits are refusals: it answers neither `cwd` nor `env`, so on a
frozen set where every launch expect carries both it can never pass a launch case. The conjunct
`control_held_r98_correct < cases_total` is true but vacuous for the work C1 claims. A
discriminating held control would be the r98 tool plus a constant cwd/env, or the r98 tool
scored on argv alone with the cwd/env conjuncts reported separately.

### F6 (medium; gate note) -- `normalise_expect` silently defaults a missing cwd/env to None

The counter compares `cwd`/`env_gdf` exactly, and defaults them to `None` when the expect omits
them. Every frozen launch case carries both today (checked), so the scored set is sound; a
re-freeze that drops either would make every launch case unpassable against a real answer, with
no setup error. A census line (`expect-cwd-missing`) would fail closed.

### F7 (low) -- `terminal=` is unmeasured

The text and JSON outputs carry `terminal=<table name>`, but the oracle records the resolved
`argv[0]`, not the table name, and the counter does not compare a terminal field. It is a
diagnostic, not a scored claim; the declaration should not read it as verified.

### F8 (low; instrument note) -- the frozen probe appends one line per spawn to a shared file

Contract 2's design, and I measured no torn records over 67 cases x 2 runs. The atomicity is a
property of the line length and the filesystem, not a lock; QUALITY 170's stronger form (one
file per spawn) is what my own plane used. Worth keeping in the instrument's named limits.

### F9 (low; named limit) -- an empty `Exec` with no arguments has no cause name

Measured: `Exec=` (or `Exec= `) with **no** file arguments refuses with gio's
`Text was empty (or contained only whitespace)`; with an executable argument the same desktop
launches (`argv[0]` = the argument), and with a non-executable argument it refuses
`program-not-found`. The candidate answers `exec-parse` for the no-argument form. The frozen set
carries only a *missing* `Exec` (`rf-noexec`), so no scored case is affected; a future case would
need a fourth name (or the `exec-parse` label redefined to cover it). My plane's `at6-*` rows
carry the measurement.

## 7. Residual risk and verification gaps

- I did not run the counter's full CLI (mutants, fresh leg, controls): the tool is not committed
  at a revision and the mutant file is the counter seat's. I ran its `score_case` directly on
  all 67 frozen cases and its `--selftest` (18/0).
- I did not re-run the fresh generator; its labels are generated at measurement time and are the
  counter's leg.
- The candidate answers the **physical** cwd (`realpath`) while the counter rewrites `{root}` by
  string substitution: the two agree only when the case root path is symlink-free. My runs used
  `/fast/scratch` (not a symlink). A symlinked `--scratch-root` would produce a spurious cwd
  mismatch for every launch case.
- My plane's `at3-*` rows are vocabulary and classifier questions (F2 and the missing `no-exec`
  mapping), not behaviour; I did not treat them as candidate defects.
- The `%u`/NoFuse URI path with a relative argument is unmeasured on both planes.
- The mutant leg is not mine: R99MMutC1 independently found the same `arg-conv` defect (their
  finding 4) and reports the candidate's `def selftest(` sitting before `main()`, which leaves
  `main()` outside the counter's non-selftest prefix (QUALITY 167). I did not re-run the mutant
  leg; the candidate's selftest is at 90 checks / 0 failed on the reviewed bytes.

## 8. Verdict

At the reviewed tip `a63c20c8...eb16` the C1 candidate answers the frozen surface 67/67 under the
counter's own scorer, the frozen labels reproduce 67/67 behaviourally under my independent
re-derivation, both controls are strictly below the total, and the tool neither spawns nor reads
outside its inputs. The findings above are record and contract-text defects (F2, F3, F6), one
process-state coupling (F4), one weak control (F5) and two instrument notes (F7, F8); F1 was
real and is fixed. Nothing in this report edits the candidate, the oracle, the counter or the
case file.
