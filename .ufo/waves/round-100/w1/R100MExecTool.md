# R100MExecTool — the C1 unset-PATH default branch, cored

Lane mado, round 100, wave w1, base `43309e6af9a3b57f1bc839a826bef1f8eb7495e4`.
Seat: executor (C1 candidate). Read: `.ufo/waves/round-100/claims-declaration-r100.md`,
`corpus/QUALITY.md` (round-90..99), `corpus/lessons/round-99.md`,
`corpus/lessons/round-99-verifier-spotcheck.md`, `SKILL.md`, `quality/harm-watch.py`.

## Files

| Path | What |
|---|---|
| `.ufo/waves/round-100/build/mado-launchenv.py` | candidate copy of `tools/mado-launchenv.py`, sha256 `3b29dc65111a2f3efdd5aa282f74493ff53eff840a1c88a92054f0df2e9fb228`; base `a63c20c886a2bd840d80966d531e055e9c4f5d3accb431e4b0e317e04523eb16` |
| `.ufo/waves/round-100/receipts/c1-tool-r100.txt` | measurements, selftest line, mutant kills |
| `.ufo/waves/round-100/w1/R100MExecTool.md` | this report |

`tools/`, `quality/`, `corpus/`, `plans/`, controls, git index: untouched by this seat.

## Axes

- **coverage** — the declared C1 surface (unset-PATH default) gains executable, oracle-measured
  cases; the model gains assertions at the load-gate level, not only at `find_program` units.
- **depth** — the modelled branch is now pinned where the failure actually occurs (load-gate
  `Exec`/`TryExec` resolution with `cwd = case root`), including the argv0 string shape.
- **calibration** — the two r99 `path-unset` cases are shown structurally blind (below); they
  agree but cannot witness the branch.
- **freshness / operability / adjacency** — no move (not this seat's surface).

## 1. Ground re-measured (not inherited)

| Fact | Measurement |
|---|---|
| glib2 | `2.90.1-1` |
| `/usr/bin/gio` sha256 | `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` (matches the L1 pin and the r99 case-file pin) |
| `/bin` | symlink to `usr/bin` (so a `/bin/...` hit and a `/usr/bin/...` hit are the same inode; the model's first-entry answer `/bin/x` is the C's answer too) |
| host binaries that could pollute a fixture | `/usr/bin/probe.sh` absent, `/bin/probe.sh` absent, `/usr/bin/loose` absent; `xdg-terminal-exec` present in `/usr/bin` (a `Terminal=true` + unset PATH case finds it, as the C would) |

## 2. Divergence hunt over the frozen r99 set

Ran the base tool (candidate and base differ only inside `--selftest`, so the answers are the
same bytes) over all 67 cases of `.ufo/waves/round-99/controls/launchenv-cases-r99.json`, with
each case root materialised exactly as the round-99 oracle builds it (`launchenv-probe-r99.py`:
same `files`/`dirs`/`modes`, same `render_desktop`, same `{root}`/`{probe}` substitution,
candidate run with `cwd = case root`, `path: null` modelled as `path_env=None`, `args` and
`args_rel` handled as the oracle does) and compared against the frozen `expect` using the
oracle's own `canon()`:

```
mismatches=0/67
```

**No divergence exposed by the frozen set.** Every class agreed: `term-*` (incl. all terminal
table rows), `cwd-*`, `prog-*`, `multi-term`, `path-empty-entry` (`pe-leading`, `pe-trailing`,
`pe-double`, `pe-empty-str`, `pe-dot` — the `.`-entry case `pe-dot` expects `{root}/./probe` and
the model answers exactly that), `tryexec`, `exec-test`, `arg-conv`, `env-gdf`, `refuse-shape`.
The known trap named in the assignment — the argv0 string shape `{root}/./probe` from the `.`
entry — is **not** a live divergence; it is reproduced correctly.

The blind spot is real and is the depth finding:

- `pu-abs-work` and `pu-abs-root` (class `path-unset`) both carry an **absolute** `Exec`
  (`{root}/probe.sh`), which returns at `gutils.c:331-357` before the PATH source is read at
  `gutils.c:370`. They agree with the model, but they cannot witness the unset default. Their
  agreement is not evidence about the branch. This matches the declaration's C1 measurement
  sequence; the new coverage is needed for exactly this reason.

## 3. Fresh oracle measurements of the unset class (the branch itself)

Case-private fixtures only, built and launched by the round-99 oracle entry points
(`build_root` + `measure_case`, two runs each, `agreed=True` unless noted; `cwd = case root`;
`path: null` → child env has no `PATH` key):

| id | fixture | measured (oracle, twice) |
|---|---|---|
| `pd-dot-unset` | `Exec=probe`, program at case root, PATH absent | `launches=1 argv[0]={root}/./probe` |
| `pd-empty` | same fixture, `PATH=""` | `launches=1 argv[0]={root}/probe` |
| `pd-privbin-unset` | program only `<root>/bin/probe`, PATH absent | `error load` |
| `pd-privbin-set` | same fixture, `PATH=[{root}/bin]` | `launches=1 argv[0]={root}/bin/probe` |
| `pd-tryexec-dot-unset` | `TryExec=probe` at case root, `Exec={root}/probe.sh`, PATH absent | `launches=1` (TryExec resolved, exec ran) |
| `pd-tryexec-empty` | same, `PATH=""` | `launches=1` |
| `pd-tryexec-privbin-unset` | `TryExec=probe` only in `<root>/bin`, PATH absent | `error load` |
| `pd-tryexec-privbin-set` | same, `PATH=[{root}/bin]` | `launches=1` |
| `pd-term-empty` | `Terminal=true`, `Exec=probe` at root, `PATH=""` | `error no-terminal` |
| `pd-sh-empty` | `Exec=sh`, `PATH=""` | `error load` |
| `pd-term-unset` | `Terminal=true`, PATH absent | `setup-error` — the terminal walk *does* find `xdg-terminal-exec` via the default and the wrapper then fails without a display; not a model verdict, excluded |
| `pd-sh-unset` | `Exec=sh`, PATH absent | `setup-error` — a real `sh` is spawned and writes no probe record; not a model verdict, excluded |

The candidate was run against these same roots and agrees on all ten cases that produce an
oracle verdict (the two `setup-error` rows are excluded as oracle-side artefacts, stated so they
are not counted as agreement).

C1 clauses 1–3 of the declaration are all witnessed by the rows above: unset ≠ empty
(`pd-dot-unset` vs `pd-empty`; `pd-privbin-unset` vs `pd-privbin-set`), unset ≠ ambient
(`pd-privbin-unset` vs `pd-privbin-set`), and the trailing `.` is real (`pd-dot-unset` vs
`pd-empty` — same cwd, different argv0 shape).

## 4. CLI three-state behaviour through the candidate

`env -i` (no `PATH` key), `cwd = case root`, case-private `probe`:

```
no --path, PATH absent   -> ARGV[1][0]={root}/./probe     (default '/bin:/usr/bin:.')
--path ""                -> ARGV[1][0]={root}/probe        (one empty entry, cwd)
--path "."               -> ARGV[1][0]={root}/./probe      (explicit dot, same shape)
--path {root}            -> ARGV[1][0]={root}/probe
no --path, ambient PATH given -> MADO_LAUNCHENV: ERROR load detail=exec-argv0
                                 (reads the process PATH; does NOT fall back to the default)
```

This is the contract's sentence (`--path` absent + no `PATH` in the model process's environment
= PATH unset → `/bin:/usr/bin:.`; `--path ""` = one empty entry) held end to end, not only at
the unit level.

## 5. Change made to the candidate

Diff against `tools/mado-launchenv.py` touches the `--selftest` body only. Five checks added
(≥4 required), placed with the R6 units and before the load-gate block, all end to end:

| check | pins |
|---|---|
| `st-unset-default-dot-launch` | `run(..., path_env=None)` → argv0 `{root}/./probe` (unset default + trailing `.`) |
| `st-empty-string-no-dot` | `run(..., path_env='')` → argv0 `{root}/probe` (empty string ≠ unset) |
| `st-dot-entry-explicit` | `run(..., path_env='.')` → argv0 `{root}/./probe` (`.`) |
| `st-unset-tryexec-privbin-miss` | `TryExec` under PATH absent with the program only in a private bin → `load try-exec` |
| `st-unset-tryexec-dot-hit` | `TryExec` under PATH absent resolved through the trailing `.` → launch |

Selftest line, candidate run from a copy whose sibling is the committed
`tools/mado-execargv.py`:

```
MADO_LAUNCHENV_SELFTEST: checks=95 failed=0
```

CLI, output lines (`MADO_LAUNCHENV:`, `LAUNCH k:`, `ARGV[k][i]=`, `ENV[k] …`, `ERROR …`), the
`--json` key order and the exit map 0/2/3 are unchanged — the diff shows no non-selftest hunk.
(The candidate alone in `build/` answers `SETUP_ERROR execargv-missing`, exactly as the base tool
does outside `tools/`; the sibling is resolved next to the file by design.)

## 6. Mutation sensitivity (why the branch is now cored, not modelled-only)

Mutants were applied to the candidate copy in scratch and scored with its own `--selftest`
(the case set alone is blind to both, per `R100MMutPath`'s independent matrix on r99):

```
m1  DEFAULT_SEARCH_PATH = '/bin:/usr/bin'      (loses the trailing '.')
    -> checks=95 failed=3
m2  PATH unset treated as empty (path = '')    (unset == empty)
    -> checks=95 failed=3
pristine candidate                             -> checks=95 failed=0
```

Killed checks: `st-unset-default-dot-launch`, `st-unset-tryexec-dot-hit`,
`fp-default-dot-entry-keeps-dot-slash` (m1); `st-unset-default-dot-launch`,
`fp-default-path-has-sh`, `fp-default-dot-entry-keeps-dot-slash` (m2). So the asserted surface
discriminates the two readings the declaration's predicate guards against
(`control_unset_as_empty_correct < cases_total`) at the tool's own gate, independent of how many
frozen cases land.

## 7. Runnable evidence retained

- receipt: `.ufo/waves/round-100/receipts/c1-tool-r100.txt` — gio + candidate hashes, oracle
  measurements with two-run agreement, CLI three-state transcript, mutant kills, selftest line,
  `mismatches=0/67`.
- candidate: `.ufo/waves/round-100/build/mado-launchenv.py` (sha256 `3b29dc65…`).

Instrument classification: the candidate tool is stdlib-only and spawns nothing; my harness in
scratch (case runner and oracle measurements) is an **instrument** — it imports the round-99
oracle module and spawns `/usr/bin/gio` (and the probe shell) exactly as the oracle does. No
candidate change touches subprocess/socket/network/ctypes.

## 8. Risks and routed items

1. **Case parity for `path:null` (counter contract, not candidate).** A `path:null` case must
   drive the candidate with **no `PATH` key in its environment and no `--path`**; with
   `PATH=""` the candidate answers `{root}/probe` where the frozen shape is `{root}/./probe`.
   Independently measured and reported by `R100MMutPath`. The r100 counter's case leg must get
   this right or the new class is scored wrong; nothing in the tool can decide it. Routed to L1.
2. **`pd-term-unset` is not usable as a case.** Under PATH absent the terminal walk legitimately
   finds the host's `xdg-terminal-exec`, and that wrapper fails for lack of a display, so the
   oracle reports `setup-error`. A `Terminal=true` case must be built either with `PATH=""`
   (no-terminal, measurable) or with a case-private terminal row.
3. **`/bin` vs `/usr/bin` shape.** The default's first two entries are distinct strings but the
   same inode on this merged-usr host; a case that asserts an argv0 found in `/usr/bin` under
   PATH absent will see `/bin/...` (the C does the same). Case authors should assert the
   `.`-entry shape (case-private), not a host binary path.
4. **The r100 case file is not this seat's write scope.** It does not exist yet at report time;
   the five selftest checks and the measured table above are the inputs its author can freeze
   against. Re-running my r99 comparison against that file's bytes is one command
   (`runcases2.py` logic) once it lands.
5. No tool installs or upgrades were made; no pacman transaction, no host mutation, no terminal
   launched.
