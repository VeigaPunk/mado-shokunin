# R99MMutC1 - C1 mutant population (mutation tester)

Round 99, wave w1, seat R99MMutC1. Read-only mutation probe against the C1 candidate
draft. This report is the seat output; the mutant population is the lane draft
`controls/launchenv-mutants-r99.json` (the L1 lands it).

## Measured objects

- Candidate: `build/mado-launchenv.py` sha256
  `a63c20c886a2bd840d80966d531e055e9c4f5d3accb431e4b0e317e04523eb16` (954 lines; the draft at
  sweep time - every anchor below was re-verified against these bytes).
- Frozen cases: `controls/launchenv-cases-r99.json` sha256
  `14b4cc571a35bb5b4c6996a4a3fde19ff71ce9f26dabe3dd4142eec162f82acd` (67 cases, 31 classes).
- Mutant file: `controls/launchenv-mutants-r99.json` sha256
  `57b11e14ad5aeab2878aaa95379949c043825ab29561057823f2b3195bf85e36`
  (69 counted, 13 `not_observable`, 3 `equivalents`, 31-case-class envelope).
- Oracle: `/usr/bin/gio` sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`;
  glib2 2.90.1-1.
- Candidate selftest at this sha, run by this seat: `MADO_LAUNCHENV_SELFTEST: checks=90 failed=0`
  (rc 0).

## Detector and kill definition

The candidate is a model, not a process; the detector is an instrument, not a candidate. The kill
leg is the counter's case leg, reproduced verbatim from the convention R99MExecCounter pinned in
flight:

- the candidate runs as a child: `python3 -I <tool> <root>/case.desktop <root>/<arg>...
  --path <PATHSTR> --json`, `cwd` = the materialised case root,
  `env = {PATH:"", LC_ALL:"C", HOME:"<root>/h"}`;
- `PATHSTR` = the frozen `path` list with `{root}`/`{probe}` substituted per entry, joined with
  `":"`, an empty entry kept empty, a literal `"."` kept as `"."`;
- compare: `launches`, `argv` as a sorted multiset of vectors, `cwd` and
  `env.GIO_LAUNCHED_DESKTOP_FILE` exact; a refusal needs rc 2 and the exact `error` cause
  (`detail` ignored).

A kill is a **parsed wrong answer on a case the pristine candidate answers correctly**. A crash, a
timeout or an unparsable output is never a kill.

Baseline on the frozen set with these bytes: **67/67 correct, 0 wrong, 0 crash**. The mutant sweep
only scores cases the baseline answered correctly, so a baseline defect can never be counted as a
kill.

Every mutant is applied to a disposable copy under `S=$HYAKU_SCRATCH/mado-r99/R99MMutC1`; the
candidate bytes are never modified (sha256 before and after: `a63c20c8...`). The scratch tree is
removed before the seat yields.

## Mutant population

- **69 counted mutants**, each `{"id","find","replace","class","defect","expect":"kill"}`.
- Every `find` occurs exactly once in the WHOLE tool text and exactly once in the non-selftest
  prefix (cut at the first literal `def selftest(`, line 451).
- `find` strings are unique across the counted list, the `not_observable` list and the
  `equivalents` list.
- **Schema note.** The counter's `validate_mutants` requires each mutant's `class` to be one of the
  FROZEN CASE classes (`mutant class not in the frozen class list`), and requires the file's
  `classes` list to equal the case file's list exactly. The seat's 21-class defect vocabulary is
  therefore carried in a separate `defect` field, and `class` is the case class of the case the
  mutant first breaks. Verified with the counter's own validator
  (`c1-r99-launchenv.py:validate_mutants` over the current prefix): **0 errors**.
- 13 `not_observable` and 3 `equivalents` entries, each with a written argument (below).
- **Class coverage of the 21 declared defect classes: 20/21 counted.** The missing one is
  `unset-PATH-default`: the counter always passes `--path` (set, possibly empty) and the probe
  always sets `PATH`, so the `/bin:/usr/bin:.` default branch is unreachable on the frozen plane.
  Both directions are recorded as non-killers with their arguments. This is a routed finding, not a
  silent omission.

## Kill table

All 69 counted mutants are killed. One row per mutant: the first frozen case that produced a parsed
wrong answer, and the observed wrong answer.

### Kill table

| mutant | defect class | case class of first kill | first kill case | observed wrong answer |
|---|---|---|---|---|
| order-01-swap-kgx-gnome | term-order | term-order | order-kgx-gnome | launches=1 argv0=["<root>/bin/gnome-terminal", "--"] |
| order-03-xterm-first | term-order | term-xte | xte-plain | ERROR no-terminal |
| order-04-walk-reversed | term-order | term-order | order-kgx-gnome | launches=1 argv0=["<root>/bin/gnome-terminal", "--"] |
| order-06-drop-xterm-row | term-order | term-xterm-row | tx-xterm | ERROR no-terminal |
| order-07-drop-xte-row | term-order | term-xte | xte-plain | ERROR no-terminal |
| order-08-drop-kgx-row | term-order | term-kgx | kgx-plain | ERROR no-terminal |
| term-01-always-false | term-order | term-xte | xte-plain | launches=1 argv0=["<root>/probe.sh"] |
| term-02-inverted | term-order | term-xte | xte-plain | ERROR no-terminal |
| term-03-no-refusal | term-order | term-none | none-plain | launches=1 argv0=["<root>/probe.sh"] |
| term-04-no-wd | term-order | term-path | tpath-xte | ERROR no-terminal |
| term-05-null-path | term-order | term-xte | xte-plain | launches=1 argv0=["/bin/xdg-terminal-exec", "<root>/probe.sh"] |
| execarg-01-drop-prepend | exec-arg-dropped | term-kgx | kgx-plain | launches=1 argv0=["<root>/bin/kgx", "<root> |
| execarg-02-drop-resolve | exec-arg-dropped | term-kgx | kgx-plain | launches=1 argv0=["<root>/bin/kgx", "<root> |
| execarg-03-add-prepend | exec-arg-added | term-xte | xte-plain | launches=1 argv0=["<root>/bin/xdg-terminal-exec", "-e"] |
| execarg-04-add-resolve | exec-arg-added | term-xte | xte-plain | launches=1 argv0=["<root>/bin/xdg-terminal-exec", "-e"] |
| execarg-05-kgx-dashdash | exec-arg-dropped | term-kgx | kgx-plain | launches=1 argv0=["<root>/bin/kgx", "--"] |
| execarg-06-gnome-dash-e | exec-arg-added | term-order | order-gnome-xterm | launches=1 argv0=["<root>/bin/gnome-terminal", "-e"] |
| xgterm-01-option | xgterm-null-arg | term-xte | xte-plain | launches=1 argv0=["<root>/bin/xdg-terminal-exec", "-e"] |
| xgterm-02-empty-string | xgterm-null-arg | term-xte | xte-plain | launches=1 argv0=["<root>/bin/xdg-terminal-exec", ""] |
| xgterm-03-dashdash | xgterm-null-arg | term-xte | xte-plain | launches=1 argv0=["<root>/bin/xdg-terminal-exec", "--"] |
| wdjoin-01-drop | working-dir-join-dropped | tryexec | tx-viawd | ERROR load |
| wdjoin-03-noop | working-dir-join-dropped | tryexec | tx-viawd | ERROR load |
| absbranch-02-drop-abs | absolute-or-slash-branch-dropped | tryexec | tx-viawd | ERROR load |
| absbranch-03-abs-original | absolute-or-slash-branch-dropped | prog-rel | pr-dot | ERROR load |
| empty-01-absolute | empty-entry-rule | path-empty-entry | pe-empty-str | ERROR load |
| empty-02-dot | empty-entry-rule | path-empty-entry | pe-empty-str | launches=1 argv0=["<root>/./probe"] |
| empty-03-empty-startp | empty-entry-rule | path-empty-entry | pe-empty-str | ERROR load |
| reljoin-01-drop | relative-candidate-join | term-path | tpath-xte | ERROR no-terminal |
| join-01-no-sep | relative-candidate-join | term-path | tpath-xte | ERROR no-terminal |
| absol-01-return-relative | relative-hit-absolutisation | path-empty-entry | pe-empty-str | launches=1 argv0=["probe"] |
| exectest-01-drop | executable-test-dropped | term-xte | xte-work | launches=1 argv0=["<root>/work/xdg-terminal-exec", "<root> |
| exectest-02-exists | executable-test-dropped | tryexec | tx-644 | launches=1 argv0=["<root>/probe.sh"] |
| exectest-03-readable | executable-test-dropped | tryexec | tx-644 | launches=1 argv0=["<root>/probe.sh"] |
| isdir-01-drop | is-dir-test-dropped | prog-dir | pd-abs | ERROR program-not-found |
| isdir-03-symlink | is-dir-test-dropped | prog-dir | pd-abs | ERROR program-not-found |
| load-01-drop-exec | load-gate-dropped | prog-missing | pm-bare | ERROR program-not-found |
| load-02-drop-tryexec | load-gate-dropped | tryexec | tx-missing | launches=1 argv0=["<root>/probe.sh"] |
| load-03-wrong-cause | load-gate-dropped | prog-missing | pm-bare | ERROR program-not-found |
| load-06-tryexec-ignored | load-gate-dropped | tryexec | tx-missing | launches=1 argv0=["<root>/probe.sh"] |
| load-07-no-wd | load-gate-dropped | path-empty-entry | pe-trailing | ERROR load |
| load-08-tryexec-no-wd | load-gate-dropped | tryexec | tx-viawd | ERROR load |
| loadpath-01-exec | load-gate-launch-path | prog-bare | pb-plain | ERROR load |
| loadpath-02-tryexec | load-gate-launch-path | tryexec | tx-ok | ERROR load |
| prepend-01-tail | prepend-order-reversed | term-xte | xte-plain | launches=1 argv0=["<root>/probe.sh", "<root> |
| prepend-02-arg-first | prepend-order-reversed | term-kgx | kgx-plain | ERROR program-not-found |
| argv0-01-drop-r3 | argv0-lookup-dropped | prog-bare | pb-plain | launches=1 argv0=["probe"] |
| argv0-02-no-lookup | argv0-lookup-dropped | prog-bare | pb-plain | ERROR program-not-found |
| argv0-03-no-replace | argv0-lookup-dropped | prog-bare | pb-plain | launches=1 argv0=["probe"] |
| r3-06-no-wd | argv0-lookup-dropped | path-empty-entry | pe-trailing | ERROR program-not-found |
| cwd-01-process | cwd-from-process | term-xte | xte-work | launches=1 argv0=["<root>/bin/xdg-terminal-exec", "<root> |
| cwd-02-child-process | cwd-from-process | term-xte | xte-work | launches=1 argv0=["<root>/bin/xdg-terminal-exec", "<root> |
| r4-01-drop-enterable | cwd-from-process | cwd-missing | cm-gone | launches=1 argv0=["<root>/probe.sh"] |
| r4-02-empty-only | cwd-from-process | term-xte | xte-plain | ERROR cwd-failed |
| r4-03-no-isdir | cwd-from-process | cwd-missing | cm-file | launches=1 argv0=["<root>/probe.sh"] |
| empty-path-01-empty-cwd | empty-path-inheritance | term-xte | xte-plain | launches=1 argv0=["<root>/bin/xdg-terminal-exec", "<root> |
| empty-path-02-enterable | empty-path-inheritance | cwd-empty | ce-empty | ERROR cwd-failed |
| gdf-01-empty-env | gdf-dropped | term-xte | xte-plain | launches=1 argv0=["<root>/bin/xdg-terminal-exec", "<root> |
| gdf-02-none | gdf-dropped | term-xte | xte-plain | launches=1 argv0=["<root>/bin/xdg-terminal-exec", "<root> |
| gdf-03-result-none | gdf-dropped | term-xte | xte-plain | launches=1 argv0=["<root>/bin/xdg-terminal-exec", "<root> |
| gdf-04-basename | gdf-desktop-id | term-xte | xte-plain | launches=1 argv0=["<root>/bin/xdg-terminal-exec", "<root> |
| gdf-05-id | gdf-desktop-id | term-xte | xte-plain | launches=1 argv0=["<root>/bin/xdg-terminal-exec", "<root> |
| gdf-06-no-canon | gdf-desktop-id | env-gdf | gdf-rel | launches=1 argv0=["<root>/probe.sh"] |
| cause-01-load | refusal-cause-token | prog-missing | pm-bare | ERROR load-refused |
| cause-02-noterm | refusal-cause-token | term-none | none-plain | ERROR no-term |
| cause-03-pnf | refusal-cause-token | prog-notfound | pnf-k | ERROR not-found |
| cause-04-cwd | refusal-cause-token | cwd-missing | cm-gone | ERROR cwd |
| cause-05-noexec | refusal-cause-token | refuse-shape | rf-noexec | ERROR missing-exec |
| cause-07-execparse | refusal-cause-token | refuse-shape | rf-quote | ERROR parse |
| cause-08-tryexec | refusal-cause-token | tryexec | tx-missing | ERROR try-exec |

### Class coverage (frozen case classes)

| case class | mutants that break it |
|---|---|
| term-xte | 55 |
| term-kgx | 34 |
| term-order | 37 |
| term-none | 10 |
| term-path | 42 |
| cwd-path | 14 |
| cwd-empty | 23 |
| cwd-missing | 7 |
| prog-abs | 14 |
| prog-bare | 22 |
| prog-missing | 8 |
| prog-dir | 10 |
| prog-rel | 20 |
| multi-term | 53 |
| path-empty-entry | 63 |
| path-unset | 14 |
| tryexec | 47 |
| exec-test | 38 |
| prog-notfound | 6 |
| refuse-shape | 2 |
| arg-conv | 23 |
| env-gdf | 33 |
| term-mate | 15 |
| term-xfce4 | 15 |
| term-tilix | 15 |
| term-konsole | 15 |
| term-nxterm | 15 |
| term-color-xterm | 15 |
| term-rxvt | 15 |
| term-dtterm | 15 |
| term-xterm-row | 16 |

### Non-killers

#### not_observable (13)

- `no-direct-relative-return` (relative-hit-absolutisation): the direct branch returns a RELATIVE program only when the program contains '/' and the working_dir join does not make it absolute; every frozen slash-program case (pr-sub, pr-dot) carries Path= so the join yields an absolute path and the call is never reached with a relative value
- `no-group-token` (refusal-cause-token): no frozen case reaches the group check: rf-notkeyfile's raw bytes (the five characters `hello` and a newline) hit the earlier key-before-group refusal, so the token at this site is unobservable (the observable sibling is cause-14-early-key)
- `no-swap-xte-kgx` (term-order): no frozen case has BOTH xdg-terminal-exec and kgx on the case PATH: xte-plain carries only xte, kgx-plain and order-kgx-gnome only kgx (plus gnome-terminal). With one of the two rows present the swap cannot change which row is found, so the answer is identical on every frozen case
- `no-slash-branch` (absolute-or-slash-branch-dropped): the slash half is load-bearing only when the program contains '/' and the working_dir join does not make it absolute; every frozen slash-program case (pr-sub, pm-slash) either carries Path= (join -> absolute, branch entered anyway) or refuses for another reason, so dropping the half changes no answer
- `no-empty-exec` (load-gate-dropped): no frozen case carries an EMPTY Exec= (rf-noexec is a MISSING key, tx-empty is TryExec=''), so the guard that skips the static parse for an empty Exec is never exercised
- `no-realpath-cwd` (cwd-from-process): realpath differs from the joined value only for a trailing-slash Path=, a '.'/'..' component or a symlinked Path=; every frozen Path= is an absolute normalised directory (cp-work, pa-work, xte-work, tpath-*, pe-trailing, cm-gone, cm-file), so the two answers are identical
- `no-type-token` (refusal-cause-token): no frozen case carries a non-Application Type= (rf-notkeyfile has no group at all and refuses earlier at the group check), so the type-refusal token is unobservable
- `no-join-always-sep` (relative-candidate-join): the extra separator appears only when the first element ends with '/', i.e. a trailing-slash Path=; no frozen case has one, so the two joins agree
- `no-execparse-launch-site` (refusal-cause-token): the second exec-parse site (build_launches returned None after a successful static parse) has no frozen case: every frozen exec-parse case fails at the static parse, which returns earlier
- `no-unset-default` (unset-PATH-default): the default is entered only when the model PATH is unset; the counter always passes --path (set, possibly empty) and the probe always sets PATH, so the branch is unreachable on the frozen plane (R99MExecCounter and R99MExecOracle both pinned that an unset PATH is not expressible)
- `no-empty-path-takes-default` (unset-PATH-default): the only frozen case with --path '' is pe-empty-str, whose program does not exist in the cwd: the empty-entry walk and the default's '.' entry both miss, so both answers are `load`
- `no-terminal-field` (gdf-dropped): the counter compares launches, argv, cwd and env only; the --json terminal field is never read, so a wrong terminal name cannot be observed
- `no-detail-token` (refusal-cause-token): the counter compares the error cause and ignores detail (pinned by R99MExecCounter), so any detail-only change is unobservable

#### equivalents (3)

- `eq-r3-isdir-dead` (is-dir-test-dropped): _exec_file already returns False for a directory (access X_OK and not isdir), so 'not _exec_file(a0)' fires before the isdir conjunct; the conjunct is dead code and removing it cannot change any answer. The load-bearing is-dir test is _exec_file's, covered by isdir-01-drop
- `eq-absol-normpath` (relative-hit-absolutisation): this call is reached only for a relative hit, and a relative hit on the frozen plane arises only from an EMPTY path entry, where startp is the bare program (no './' or '//'); the './' preservation is observed through pr-dot's absolute Path= join, which returns before this call, so normpath here is a no-op
- `eq-reljoin-reversed` (relative-candidate-join): the walk's working_dir join is reached only when working_dir+program is NOT executable; the reversed join yields program/working_dir, which cannot be executable in any frozen case, so both directions miss and the answer is identical

## Class coverage

Every one of the 31 frozen case classes is broken by at least one killed mutant, so the counter's
`class_kills == classes_total` conjunct is satisfied by this population (31/31).

## Independent cross-check

A second instrument (a scratch reference model of the declaration's R1-R6, `refmodel.py`, delegating
the argv expansion to the same committed `tools/mado-execargv.py` the candidate loads) was measured
against `/usr/bin/gio` on a 32-case self-built suite covering every class shape: **24/26 exact** on
the first run, and 32/32 after the two taxonomy cases were relabelled to the tool's own cause
vocabulary (a bad `Type=` prints the same `Unable to load application information` stderr as the
load gate; an empty `Exec=` fails at launch with `Text was empty`, outside the cause taxonomy) and
after the reference model adopted the physical-cwd rule (`realpath` after `chdir`). The candidate
answers that 32-case suite **32/32**.

Measured shapes (all reproduced twice, `env -i`, PATH = the case bin dirs only, cwd = the case
root):

| shape | measured answer |
|---|---|
| `Exec=prog`, prog in `<root>/bin`, PATH `<root>/bin` | `[<root>/bin/prog]`, cwd `<root>` |
| `Path=<root>/work`, prog in work | `[<root>/work/prog]`, cwd `<root>/work` |
| `Path=` (empty) | cwd `<root>` (inherits) |
| `Terminal=true`, xdg-terminal-exec on PATH | `[<root>/bin/xdg-terminal-exec, prog]` |
| `Terminal=true`, kgx on PATH | `[<root>/bin/kgx, -e, prog]` |
| `Terminal=true`, kgx AND gnome-terminal | kgx wins (table order) |
| `Terminal=true`, no known terminal | `no-terminal` |
| `Exec=bin/prog`, `Path=<root>/work`, work/bin/prog | `[<root>/work/bin/prog]` |
| PATH `"<root>/bin:"`, prog in `<root>` | `[<root>/prog]` (empty entry = cwd) |
| PATH `"<root>/bin:"`, `Path=<root>/work`, prog in work | `[<root>/work/prog]` |
| PATH `"."`, prog in `<root>` | `[<root>/./prog]` (no normalisation) |
| PATH `""` (set-empty), prog in `<root>` | `[<root>/prog]` |
| `TryExec=nope` | `load` |
| `TryExec=prog` (present) | launch |
| `Exec=%k` with an executable `%k` on PATH | `program-not-found` |
| `Path=/nonexistent` | `cwd-failed` |
| `Path=<a regular file>` | `cwd-failed` |
| prog mode 0644 on PATH | `load` |
| a DIRECTORY named prog on PATH | `load` |
| `Exec=prog %f` + two args + `Terminal=true` | two launches, each `[xte, prog, <arg>]` |
| relative arg `./args/a.txt` | `<root>/args/a.txt` (GFile canonicalisation) |
| relative desktop arg `case.desktop` | `GIO_LAUNCHED_DESKTOP_FILE=<root>/case.desktop` |

Two structural facts this cross-check established and the population uses:

1. `g_file_test(IS_EXECUTABLE)` on UNIX is `access(X_OK)` only (gfileutils.c:428, fetched 200 this
   round), so a 0755 DIRECTORY passes it and the `!IS_DIR` half is load-bearing - the is-dir class
   is observable through a directory, and the executable class needs a non-0755 file (the `modes`
   map the oracle adopted).
2. In the candidate's R3 the conjunct `or os.path.isdir(a0)` is dead code: `_exec_file` already
   returns False for a directory, so `not _exec_file(a0)` fires first. Recorded as an equivalent,
   not counted.

## Findings routed before the freeze

1. **`gdf-rel` label (relative desktop argument).** The oracle's first freeze measured
   `env_gdf = "case.desktop"` (the literal argument). `gio launch` canonicalises argv[1]
   (`gio-tool-launch.c:78`), so the child sees `<root>/case.desktop`; measured twice. Routed and
   fixed in the frozen file.
2. **`rf-badescape` taxonomy.** A bad GKeyFile escape in `Exec` dies in GKeyFile, before
   `g_shell_parse_argv`, so its cause is `desktop-file`, not `exec-parse`. Routed; the oracle
   relabelled it and added a structural-cause check.
3. **The `modes` gap.** The contract writes every `files` entry at 0755, so a non-executable
   program could not be expressed and the executable-test class had no observing case. Routed to
   the oracle and the counter; both adopted an optional `modes` map (`{"bin/prog": "644"}`), and
   the frozen set now carries five `modes` cases.
4. **Relative file arguments were not canonicalised (candidate defect).** `ac-rel` and `ac-dot`
   failed 2/67: the candidate passed `args/a.txt` / `./args/a.txt` through, while
   `g_file_new_for_commandline_arg` resolves them to `<root>/args/a.txt`. Routed to R99MExecTool
   with the reproduction; fixed at draft `a63c20c8` (the candidate now canonicalises every non-URI
   argument and the desktop argument lexically), and the frozen set is 67/67.
5. **`PATHSTR` placeholder blocker.** The frozen `path` entries carry `{root}` placeholders
   (`["{root}/bin"]`), so a counter that root-prefixed them would build `<root>/{root}/bin` and
   every expect would mismatch. Routed; the counter loads the probe's `path_string` by sha-pinned
   path, so its string is byte-identical by construction.
6. **The unset-PATH default is unobservable on this plane.** `--path` is always passed and the
   probe always sets `PATH`; the two `path: null` cases carry an absolute `Exec`, so their answer
   is PATH-independent. Both mutant directions are non-killers with that argument; the class is a
   named limit of the frozen plane, not of the model.
7. **`def selftest(` sits before `main()` (QUALITY 167).** The counter cuts the non-selftest prefix
   at the first literal `def selftest(` (line 451), which leaves `main()` (line 805) outside the
   prefix, so any mutant of `main` would be a SETUP_ERROR. No mutant in this population targets
   `main`, so the leg is unaffected; the tool should move the selftest after `main()` before the
   freeze.

## Limits

- The mutant leg is frozen-case-only. Shapes that only the fresh generator can produce (an empty
  `Exec=`, a non-Application `Type=`, a trailing-slash `Path=`, a relative `PATH` entry, a
  non-searchable directory) are listed in `not_observable` with their arguments; they are not
  counted kills.
- The kill evidence is this seat's reproduction of the counter's leg over the frozen bytes; the
  counter re-scores the same file with the same comparator, and a divergence between the two legs
  would show up as a baseline MISMATCH in the counter's run.
- The mutant `class` field is the frozen case class (counter schema); the seat's defect taxonomy is
  in `defect`. A reader counting "defect classes covered" should read `defect`.
- The anchors are pinned to the candidate sha `a63c20c8...`; a later candidate edit that moves a
  line invalidates a `find` and the counter reports `setup-mutants-anchor`, never a silent pass.

## Tooling

No tool was installed or upgraded; no pacman transaction, no sudo, no host service change. The
probes used `/usr/bin/python3` (stdlib only), `/usr/bin/gio` and the existing shell. One source file
was fetched this round with the required command and counts at HTTP 200:
`curl -sSL -o gfileutils.c -w '%{http_code} %{url_effective}'` on
`https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gfileutils.c` -> `200`, 88544 bytes, sha256
`edbfc1dbf286c1538779590e18f7fe03faa6e7230a2e72ff00b57274f296f546`; the located quote is
`gfileutils.c:428` (`if ((test & G_FILE_TEST_IS_EXECUTABLE) && (access (filename, X_OK) == 0))`).
Scratch: `S=$HYAKU_SCRATCH/mado-r99/R99MMutC1`; it is removed before the seat yields (the lane files
above are the only writes).
