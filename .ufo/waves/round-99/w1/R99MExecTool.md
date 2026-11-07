# R99MExecTool - w1 report (round 99, hyaku run 15 attempt 2)

Seat: C1 candidate builder (`tools/mado-launchenv.py` target; in-wave draft
`.ufo/waves/round-99/build/mado-launchenv.py`). Leaf; no subagents used, no
tool installs (none needed: stock python 3.14 + stdlib only; no pacman touch,
no sudo, no service or sysctl change, no config write; every probe read-only
under `env -i` with case-local PATHs).

## Files changed (write scope respected)

- `.ufo/waves/round-99/build/mado-launchenv.py` - NEW, the C1 candidate draft.
  sha256 `a63c20c886a2bd840d80966d531e055e9c4f5d3accb431e4b0e317e04523eb16`,
  955 lines, ASCII only. Nothing else written outside my scratch and this
  report; `tools/`, `quality/`, `corpus/` untouched; no git/jj command run
  anywhere.
- Final selftest: `MADO_LAUNCHENV_SELFTEST: checks=90 failed=0` (exit 0),
  run from a scratch harness (`S/harness/`, symlinks to the draft and to the
  committed `tools/mado-execargv.py`; the draft itself was never copied into
  the lane and `tools/mado-execargv.py` was never copied or modified).

## Behavior (Shared contract 1 + declaration R1-R6)

- CLI exactly as contracted: `DESKTOP [FILE...] [--path PATH] [--json]` and
  `--selftest`; exit 0 success, 2 refusal (`MADO_LAUNCHENV: ERROR <cause>
  detail=<...>`), 3 SETUP_ERROR (named `execargv-missing` / `execargv-spec` /
  `execargv-import`; the draft in `build/` fails closed there because it has
  no sibling - demonstrated: bare `python3 build/mado-launchenv.py --selftest`
  prints `checks=1 failed=1`, and the landed `tools/` sibling satisfies it).
  JSON: `{"launches","cwd","terminal","argv","env":{"GIO_LAUNCHED_DESKTOP_FILE"}}`
  (terminal `null` when none) or `{"error","detail"}`.
- `--path PATH` is the model of the launching PROCESS's PATH; the load gate
  (path=NULL), the terminal walk (envp PATH) and the R3 lookup (envp PATH) all
  use that one string because for `gio launch` envp IS the process
  environment. Omitted -> the model process's own PATH; unset -> the gutils.c
  default `/bin:/usr/bin:.`; empty string -> one empty entry (cwd).
- R6 `find_program` is a line-faithful port of `g_find_program_for_path`
  (gutils.c:300-500): working_dir join via g_build_filename semantics (empty
  prefix vanishes, no separator doubling), the absolute-or-slash-in-original
  direct-test branch with its fall-through to the walk for a relative
  slash-carrying miss and its early NULL for an absolute miss, the walk's
  empty-entry current-directory rule, the SECOND working_dir join on relative
  walk candidates, relative hits absolutised against the process cwd (the
  `.` entry keeps the literal `./`, measured), directories never candidates.
- R1/R1b load gate in keyfile order (group, Type, Path, TryExec, Exec;
  gdesktopappinfo.c:1907-2004): bad escapes of Type/Path/TryExec/Exec are
  `desktop-file` pass-throughs (r98 details, new `bad-escape-try-exec`); a
  non-empty TryExec is looked up BEFORE Exec (`load`/`try-exec`); the static
  Exec argv[0] lookup is `load`/`exec-argv0` (a directory argv[0] refuses via
  the !IS_DIR half - R7); a relative `Path=` joined to a bare program is NOT
  directly searched (the joined value only gets the direct test when
  absolute), so a bare Exec + relative Path= refuses the gate even when
  `<Path>/<prog>` exists (reviewer-measured, selftest-pinned).
- R2: the twelve `known_terminals` in table order (kgx before
  gnome-terminal; xdg-terminal-exec carries no exec_arg), each through
  `find_program(name, PATH, working_dir)` so a terminal inside an ABSOLUTE
  `Path=` wins before the walk and a relative `Path=` + empty PATH entry
  finds `<wd>/term`; first hit prepends `[found, exec_arg?]` to EVERY launch;
  miss -> `no-terminal`. The table NAME goes to `terminal=`/JSON; argv[0]
  carries the resolved absolute path.
- R3 per launch: argv[0] kept only when absolute+executable+not-dir; else
  (non-absolute only) `find_program` replace or `program-not-found` with
  detail = the unresolved name. argv[1+] are never rewritten (bare Exec stays
  bare after a terminal prepend - reviewer-measured, pinned). Per-launch
  resolution is modeled (Exec=%f with an executable and a non-executable file
  refuses on the second launch).
- R4: refusal `cwd-failed` only for a non-empty `Path=` failing
  isdir+searchable; the reported `cwd=` is the child's physical directory
  (realpath of the join; trailing slash/`..`/`.` collapse, symlinked Path=
  answers its target - reviewer-measured), and an absent/empty `Path=`
  inherits (the model process's cwd, what the probe's `pwd -P` records).
- R5: `GIO_LAUNCHED_DESKTOP_FILE` = the desktop argument CWD-canonicalised
  (same string %k expands to), one `ENV[k]` line per launch.
- Argument conversion (part of the launch-time surface, gio-tool-launch.c:116
  + g_file_new_for_commandline_arg/g_canonicalize_filename): EVERY plain-path
  argument AND the desktop argument are lexically canonicalised before the
  %-expansion sees them - joined to the process cwd when relative, `//`,
  `.` and `..` collapsed, trailing slash stripped, NO symlink resolution and
  NO existence check, applied to absolute arguments too (all measured:
  `./args/a.txt`, `args/../args/a.txt`, `args//a.txt`, `args/` and an
  absolute `.../args/../args/a.txt` all answer the collapsed form; the
  `../<id>/case.desktop` desktop argument answers `<root>/case.desktop`).
  Scheme-carrying arguments stay in the URI plane (arg_model's branch);
  file-URI-derived paths are NOT re-canonicalised (unmeasured, named limit -
  the frozen set carries no such case). Implementation is a pre-conversion in
  run(); the committed mado-execargv.py stays byte-identical.
- Refusal order = the C: load-time (desktop-file, try-exec, exec-argv0), then
  no-exec, exec-parse, no-terminal, program-not-found, cwd-failed last
  (pinned: no-exec before no-terminal; no-terminal before spawn; R3 before
  cwd). Text form escapes values ASCII-safely (`\xNN` per non-printable byte,
  backslash doubled) so raw newlines/surrogates in argv stay line-oriented.

## Exact retained evidence

1. Selftest: 90 checks / 0 failed (rule-by-rule and cause-by-cause coverage;
   every refusal cause incl. `cwd-failed`, every R2 table-order and wd-join
   shape, R6 units for the walk/branch/join edges, the eight-case argument
   conversion family, CLI/JSON/render units, setup-missing named error).
2. Differential probe vs the installed binary (instrument in scratch,
   `diffprobe.py`; it spawns `/usr/bin/gio` and case-local probe children -
   outside the candidate allowlist, this file is NOT a candidate):
   - pin re-hashed at run: `/usr/bin/gio` sha256
     `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`
     (glib2 2.90.1-1).
   - 16 classes x 2 repetitions, `env -i LC_ALL=C HOME=<root>/h PROBE_OUT=...
     PATH=<case bins only> /usr/bin/gio launch <desktop> <arg>`, 1.5 s quiet
     wait, BOTH processes given the same argument bytes from the same cwd;
     the two measurements agreed on all 16 and the candidate matched on all
     16 (stable across its own two runs): term-xterm (`[xterm, -e, probe,
     arg]`, cwd=work, gdf), term-xdg (no exec_arg), term-order
     (gnome-terminal `--` beats konsole), term-none -> no-terminal,
     load-tryexec, load-argv0-dir (Exec=<a dir>), load-no-such (the L1's
     measured bare fact), rel-replace (relative Exec program replaced by the
     absolute found path, cwd=Path=), cwd-failed (Path= missing),
     inherit-empty-path (empty Path= -> cwd = launcher dir), gdf-rel-k
     (relative desktop arg: GDF = %k = the canonicalised path), plain-abs,
     and the four arg-conv rows arg-rel/arg-dot/arg-dotdot/arg-trailslash
     (relative argument conversion, measured twice, agreeing).
   - frozen-set verification: the two frozen `arg-conv` cases (ac-rel,
     ac-dot, reported by R99MMutC1 as the only 2/67 misses on the PRE-fix
     draft sha `70fe43d0...`) were re-run through the candidate CLI with the
     counter's shape (cwd=case root, relative arg verbatim) and now match the
     frozen argv bytes; the six measured conversion edges were re-checked the
     same way.
   - no real terminal could start: every case PATH contained only the case's
     own bin dir (fake pass-through terminals that record their argv and
     `exec "$@"`); the only children spawned were fixtures of case roots
     built in my scratch.
3. Reviewer cross-checks: R99MReviewC1's five stale-draft findings were
   answered (sha `70fe43d0...` already carried the fixes) and their
   independent gio measurements became pinned selftest checks; their
   86-case/42-class private plane scored the PRE-fix draft 86/86 behaviour
   and the counter's run/compare conditions (cwd=case root, env
   `{PATH:"", LC_ALL:"C", HOME:...}`, cause-only refusal compare, cwd/env_gdf
   exact) are folded into the freeze conditions below. R99MMutC1's frozen-set
   baseline found the arg-conv defect (the only 2/67 misses) - fixed this
   round as described above; their `args_rel` counter plumbing means the
   relative argument reaches the candidate verbatim, so the fix is scored,
   not masked.

## Risks / decisions for the L1 (attack surface, nothing widened)

- **cwd= shape.** The header/JSON `cwd` answers the child's concrete absolute
  physical directory; on inherit that is the model process's cwd. So the
  counter must invoke the candidate from the SAME cwd the oracle's `gio`
  measurement ran in (same obligation as %k/GDF), and frozen `expect.cwd`
  values must be the physical resolved directory (my normalization matches
  `pwd -P`; the `-` slot in the contracted format remains only as a defensive
  fallback when getcwd fails). If the oracle instead froze `-` for inherit
  cases, the case set pins it and my output shape must flip - one-line change.
  Caveat kept: `realpath` matches the child's `pwd -P` exactly, which also
  resolves symlinks - clean against the counter's `{root}` string
  substitution only when the case root is symlink-free; the desktop path
  itself (%k/GDF) is NOT resolved, it stays the CWD-canonicalised argument
  (reviewer-measured: `../<id>/case.desktop` answers `<root>/case.desktop`
  lexically).
- **JSON refusal objects carry `detail`; oracle expects are `{"error":cause}`.**
  The counter should compare the cause token (details are free-form and
  root-dependent, e.g. cwd-failed's failed path).
- **Cause-taxonomy boundary (flagged, not decided):** a static `Exec` line
  that `g_shell_parse_argv` rejects keeps the round-98 pass-through
  `exec-parse`/`static`, although the C folds it into the load refusal (same
  "Unable to load application information" message as `load`). Contract 1
  says the r98 causes pass through and defines `load` as the lookup failure,
  and the r98 oracle derived causes structurally, so I follow the structural
  reading; if the round-99 oracle derives purely from stderr text, load-time
  grammar/type/escape/static-parse cases would label `load` and the case set
  must avoid or re-pin that overlap.
- **Measured label tensions (R99MReviewC1; run/compare conditions from the
  counter `.ufo/waves/round-99/build/c1-r99-launchenv.py`, `structural_cause`
  from the ORACLE `.ufo/waves/round-99/controls/launchenv-probe-r99.py` -
  the counter only reads the frozen expect, so the label rows below are
  oracle-seat freeze decisions; reviewer-measured gio bytes exist for each):**
  - the counter runs the candidate with cwd=<case root>, env
    `{PATH:"", LC_ALL:"C", HOME:<root>/h}`, always passes `--path`, and
    compares refusal CAUSE only plus cwd/env_gdf exactly - both hold for my
    CLI, PROVIDED the frozen expect carries real `cwd`/`env_gdf` for every
    launch case (their `normalise_expect` defaults them to None, which a real
    answer then mismatches);
  - `Exec=<... a\z>` (bad escape): gio's stderr says `load`, r98/M98-3
    structural says `desktop-file` (my answer), their `structural_cause`
    reportedly returns `exec-parse` - three labels for one class; the frozen
    label decides;
  - `Exec=` (empty) + executable argument: gio LAUNCHES with argv[0]=the file
    and refuses `program-not-found` when it is not - my model already matches
    gio on BOTH (the key-present/empty case goes to expansion + R3; only a
    MISSING Exec key is `no-exec`), so if the frozen set labels empty-Exec
    `no-exec` structurally (M98-9 class) the label, not the model, is wrong;
    my `exec-parse`/`empty` check covers the no-argument empty Exec, whose
    gio message ("Unable to launch application ...: Text was empty") is
    outside the stderr cause table - another pin-for-freeze row;
  - `Exec=<... 'oops>` (unbalanced quote): gio refuses at LOAD; my model and
    their structural both say `exec-parse`/`static` - a shared false green
    against gio unless the case set pins the stderr label.
- **Locale:** Name/Icon reads go through execargv's `locale_selected`
  (LC_ALL > LC_MESSAGES > LANG of the model process). The counter must run
  the candidate under the same locale env as the oracle call (the harness
  contract already pins LC_ALL=C).
- **Named limits carried:** spawn order of multi-spawn launches is not
  modeled; a first launch that would have spawned before a second launch's
  R3 refusal is not modeled as a side effect (the observable - gio's exit and
  message - is). DBusActivable, gio-launch-desktop env scrubbing, portal
  path, process survival: not modeled. The model never spawns anything.
- **Exit 3 for setup** is my choice (contract lists 0/2 only); the C1
  counter's own base-rev `SETUP_ERROR ... absent` (exit 2) is unaffected
  since that is the counter's message, not the candidate CLI's.

## Cleanup

Scratch `/fast/scratch/hyaku/mado-r99/R99MExecTool` (harness symlinks,
diffprobe, diff roots) removed after this report was written.
