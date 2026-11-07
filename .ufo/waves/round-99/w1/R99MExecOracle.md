# R99MExecOracle — w1 report (mado round 99, C1 oracle)

Seat: R99MExecOracle (executor, leaf). Base `2cbaa141f42df9dfeee4d207cae6558a4dd59863`.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Scratch
`/fast/scratch/hyaku/mado-r99/R99MExecOracle` (deleted before this report was finalised; the
measurement receipt is reproduced below).

## Artifacts (all committed this wave, ASCII, stdlib only)

| file | sha256 | role |
|---|---|---|
| `.ufo/waves/round-99/controls/launchenv-probe-r99.py` | `cbfff7a4b64e63f3e6861d29d1c5639de2c25abe2f6875088918abb45d129199` | instrument: case materialiser + `/usr/bin/gio` driver + record parser + cause deriver; also the ONE desktop-file renderer (M98-8). `--selftest`: `checks=15 failed=0`. |
| `.ufo/waves/round-99/controls/launchenv-cases-r99.json` | `14b4cc571a35bb5b4c6996a4a3fde19ff71ce9f26dabe3dd4142eec162f82acd` | the frozen case set (67 cases / 31 classes), every label measured twice with agreeing results. |
| `.ufo/waves/round-99/controls/launchenv-fresh-r99.py` | `5012642324f61bc6ee63d295b1cdb2cc91d35561442cc136e63f632257fe6dbf` | instrument: seeded fresh-case generator (`--seed HEX --dir D --out F --count N`), labels at measurement time through the oracle module. Selftest `checks=2 failed=0`; smoke `--count 6` = `FRESH_GEN: cases=6 ok=2 refused=4` + `FRESH_GEN_PIN`. |

Instrument/candidate split (QUALITY 162/165): the probe module and the generator spawn
`/usr/bin/gio` (subprocess) — they are instruments. Neither is a candidate; the C1 candidate is
`tools/mado-launchenv.py` (R99MExecTool's seat), which this set scores. No other tools were
installed or upgraded (none needed; pacman paused per host guard).

## Method

Per case: materialise a fresh root from the case dict (files b64 at 0755 unless `modes` overrides,
`dirs`, default probe at `probe.sh` 0755, desktop rendered 0644), then run

```
cwd=<root>  env -i LC_ALL=C HOME=<root>/h PROBE_OUT=<root>/out PATH=<case path entries>
            /usr/bin/gio launch <root>/case.desktop <root>/<arg>...
```

10 s gio timeout; after gio exits, a 1.5 s quiet wait on the out file (a refusal never spawns a
child, so "gio exited + 1.5 s + no file" concludes the empty record set; the whole wait caps at 20 s).
The probe appends ONE record line per spawn with ONE printf (`REC ARGV0=… ARGC=… CWD=… GDF=… A1=…`),
flock-free; a single short write to an O_APPEND fd cannot interleave, which retires M98-7's
line-tearing without a lock. Multi-spawn argv lists are frozen SORTED — completion order is not
observable (M98-10). Every case ran twice; disagreeing pairs are dropped, never guessed: **0
dropped** across the final freeze.

Cause derivation is construction-first (candidate taxonomy, per R99MExecCounter's addendum):
`no-exec` / `desktop-file` (GKeyFile refusal incl. a bad Exec escape, M98-3) / `exec-parse`
(shell-level, unbalanced quote) from the case shape; `load` / `no-terminal` / `cwd-failed` /
`program-not-found` from gio's exit status + stderr. All seven tokens are frozen.

Header pins, re-hashed at every run: `/usr/bin/gio` sha256
`d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` (matches the L1's receipt),
glib2 2.90.1-1. No host PATH ever reached a probe env; `Terminal=true` cases place their terminal
scripts under the case root only (the L1's trap (a)).

## The frozen set: 67 cases, 31 classes, 0 dropped

| class | n | observes |
|---|---|---|
| term-xte | 3 | xdg-terminal-exec, NULL exec_arg -> `[xte, prog…]`, no option |
| term-kgx | 2 | kgx `-e` inserted after the terminal |
| term-order | 2 | table order decides (kgx beats gnome-terminal; gnome-terminal `--` beats xterm) |
| term-none | 2 | Terminal=true with no known terminal -> `no-terminal` |
| term-path | 2 | terminal reachable only via a RELATIVE PATH entry joined to `Path=` |
| term-mate/xfce4/tilix/konsole/nxterm/color-xterm/rxvt/dtterm/xterm-row | 1 each | the nine remaining `known_terminals` rows with their exec_args (all twelve rows covered) |
| cwd-path | 2 | `Path=` becomes the child cwd |
| cwd-empty | 3 | absent key and empty `Path=` inherit the launcher cwd (= `<root>`); absolute argv[0] kept verbatim |
| cwd-missing | 2 | `Path=` nonexistent (ENOENT) and a FILE (ENOTDIR) -> `cwd-failed` |
| prog-abs | 2 | absolute argv[0] kept, executable+not-dir test only |
| prog-bare | 2 | bare argv[0] absolutised via the PATH walk; first dir wins |
| prog-missing | 2 | load-gate refusal (`load`), bare and slash forms |
| prog-dir | 2 | `!IS_DIR` half of the lookup: directory named as the program -> `load` |
| prog-rel | 2 | `./x` and `sub/x` resolved through `Path=`; argv[0] keeps the `/./` |
| multi-term | 3 | 2 and 3 spawns per launch, each prepended; frozen sorted |
| path-empty-entry | 5 | leading/trailing/double colon; `PATH=""` -> `{root}/probe`; `PATH="."` -> `{root}/./probe` (the `./` is kept — a normpath mutant mismatches) |
| path-unset | 2 | gio runs with NO PATH (absolute Exec, model answer PATH-independent) |
| tryexec | 5 | R1b: ok, reachable only via `Path=`, missing -> `load`, empty ignored, 0644 -> `load` |
| exec-test | 4 | 0644 program -> `load` (g_file_test IS_EXECUTABLE); 0644 terminal skipped (kgx wins) / alone -> `no-terminal` |
| prog-notfound | 1 | Exec=`%k`: load gate passes on `%k`, expansion swaps argv[0] to the 0644 desktop path -> `program-not-found` |
| refuse-shape | 4 | `no-exec`, `desktop-file` (raw + bad escape), `exec-parse` (unbalanced quote) |
| arg-conv | 3 | `g_file_new_for_commandline_arg` before the macro; relative and `./`-prefixed args arrive canonical (`{root}/args/a.txt`, `./` stripped) |
| env-gdf | 3 | GDF for an absolute arg, a RELATIVE arg (canonicalised -> `{root}/case.desktop`, not the literal), and under a terminal prepend |

Cause distribution: `launch` 49, `load` 8, `no-terminal` 3, `cwd-failed` 2, `desktop-file` 2,
`exec-parse` 1, `no-exec` 1, `program-not-found` 1.

Envelope: `version/round/oracle/probe_module/oracle_sha256/renderer_sha256/gio_path/gio_sha256/
glib2/schema_notes/classes/cases`. `oracle_sha256 == renderer_sha256` (one file is the one
renderer, M98-8); the counter is told to importlib-load `render_desktop`/`build_root` from the
committed module and to SETUP_ERROR on any pin mismatch (gio, module, cases). Contract pinned to
R99MExecCounter by message: `{root}`/`{probe}` tokens; `path` entries verbatim (`""`, `"."`,
relative, `{root}/bin`; `null` = PATH unset); `modes` map (adopted — without it the
executable-test class is unobservable); `rel_desktop`/`args_rel` flags; launch cwd `<root>` on
both sides; r98 generator CLI; construction-first causes.

## Corrections absorbed during the wave (all pre-freeze; none guessed)

1. **Instrument defect (found by wrong labels, fixed, re-frozen).** My first `build_root` wrote
   case files at 0644 (open() default) — 26 terminal cases froze as spurious `no-terminal`/`load`.
   The contract's "probe programs (mode 0755)" was not implemented. Fixed (chmod 0755 before the
   `modes` override) and the set re-frozen. Class: an instrument default defeating the surface
   (M98-9's family: frozen bytes must carry the intended mode).
2. **Instrument defect (quiet-wait).** `quiet_read` timed out at its 20 s cap on every refusal
   (no child ever writes the out file) and labelled it `setup-error`, crashing the builder.
   Fixed: "gio exited + 1.5 s + file absent/empty" concludes the empty record set.
3. **Label/input inconsistency (M98-9 family).** `pe-empty-str`/`pe-dot` declared `Exec=probe`
   with no file named `probe` (only the default `probe.sh`), so both measured `load` while the
   class point was the empty/`./` entry answer. Fixed by adding `files={"probe": …}`; now
   `{root}/probe` and `{root}/./probe` as the mutator measured.
4. **Cause taxonomy.** A bad GKeyFile escape in Exec is `desktop-file` (M98-3), not `exec-parse`;
   relabeled after R99MMutC1's cross-read; selftest asserts the mapping.
5. **gdf-rel canonicalisation.** `GIO_LAUNCHED_DESKTOP_FILE` for a relative desktop argument is
   the canonicalised absolute path (gio-tool-launch.c:78), not the literal argument —
   R99MMutC1's measurement, confirmed by my freeze; the schema note states it.
6. **Measured (not modelled) details frozen as-is.** `argv[0]` keeps `/./` (`{root}/./probe.sh`);
   `g_file_new_for_commandline_arg` strips `./` from arguments; after a terminal prepend a BARE
   non-zero argv entry stays bare (fresh smoke `fresh-05`: `[xfce4-terminal, -x, probe]`) — only
   argv[0] gets the R3 lookup.

## Named limits (declared, not silently dropped)

- `program-not-found` is frozen only through the `Exec=%k` construction; under a fully controlled
  `env -i` the R3 lookup duplicates the load gate with the same effective PATH, so without the %k
  argv[0]-swap the cause is unreachable. A mutant confined to the R3 failure branch's message
  string is an equivalent under this set.
- The unset-PATH DEFAULT STRING (`/bin:/usr/bin:.`) is not observable without host programs
  (the `Exec=sh` route launches a host binary — forbidden); the frozen `path-unset` cases use an
  absolute Exec and observe end-to-end unset-PATH behaviour with a PATH-independent answer.
- `load-gate-launch-path` (mutant checklist 14): my labels are frozen with the probe env PATH ==
  the case `path` list; the counter pins the candidate side by running it with process PATH=""
  and `--path` = the case PATH, which keeps the class counted on their side.
- Spawn order within a multi-spawn launch is not modelled (M98-10 carries); sorted multisets only.
- `dbus`, portals, `gio-launch-desktop` env scrubbing, process survival: not modelled (declaration).
- The desktop file is rendered 0644 — load-bearing for `pnf-k` (the swapped-in argv[0] must be
  non-executable).

## Measurement receipt (condensed; full per-case lines were in the scratch receipt)

```
gio_sha256=d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462 glib2=2.90.1-1
probe_module=cbfff7a4…29199  runs_per_case=2 quiet_s=1.5 gio_timeout_s=10.0 launch_cwd=root
frozen_cases=67 classes=31 dropped=0
cause_distribution={"cwd-failed":2,"desktop-file":2,"exec-parse":1,"launch":49,"load":8,
 "no-exec":1,"no-terminal":3,"program-not-found":1}
class_distribution={"arg-conv":3,"cwd-empty":3,"cwd-missing":2,"cwd-path":2,"env-gdf":3,
 "exec-test":4,"multi-term":3,"path-empty-entry":5,"path-unset":2,"prog-abs":2,"prog-bare":2,
 "prog-dir":2,"prog-missing":2,"prog-notfound":1,"prog-rel":2,"refuse-shape":4,
 "term-color-xterm":1,"term-dtterm":1,"term-kgx":2,"term-konsole":1,"term-mate":1,
 "term-none":2,"term-nxterm":1,"term-order":2,"term-path":2,"term-rxvt":1,"term-tilix":1,
 "term-xfce4":1,"term-xte":3,"term-xterm-row":1,"tryexec":5}
DROP lines: none
```

Cross-checks against independent measurements: R99MMutC1's 15-row measured-expect table agrees
with the frozen labels on every shared shape (order, exec_arg, ./ retention, empty/`./` PATH
entries, 0644 refusals, `%k` program-not-found); the L1's 18:15Z probe facts agree (terminal
prepend, cwd inheritance, `cwd-failed`, the two refusal messages).

## Coordination

- R99MExecCounter: full schema/CLI contract pinned (message on file); counter reuses
  `render_desktop`/`build_root` from the committed module by path and cross-checks three pins.
- R99MMutC1: 21-class checklist mapped to frozen case ids (message on file); two of its
  constructions adopted into the set (`modes`-style 0644 via the adopted `modes` map; the `Exec=%k`
  program-not-found route); its `unset-default` and `load-gate-launch-path` classes carry my
  equivalence arguments for its not_observable/equivalent report.

## Risks / blockers

None open. The cases file is frozen at the pins above; any later edit to the probe module must
re-run the freeze (the envelope pins the module bytes). If the C1 candidate's CLI cannot express
`--path ""` or a relative/`{root}`-less entry, the `path-empty-entry` class will mismatch — the
schema note warns the counter to pass the verbatim joined string.
