# R99MScoutEnv - reconnaissance of the C1 launch-environment surface

Seat: `R99MScoutEnv` (scout, leaf member - no dispatch). Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`, base
`2cbaa141f42df9dfeee4d207cae6558a4dd59863`. Date 2026-11-07.

**Scope.** Read-only reconnaissance of the surface the C1 candidate
(`tools/mado-launchenv.py`) must model. No candidate file was touched. The
receipt - the L1's ground truth for the case classes - is
`.ufo/waves/round-99/receipts/scout-env-r99.txt` (555 lines, ASCII-only) and
holds every label verbatim; this report carries the findings, the attacks on
the declaration, and the shape list.

**Hygiene.** Every oracle call ran `env -i` with a PATH holding only the
case's own bin directory, so `Terminal=true` could never reach the host's
`/usr/bin/xdg-terminal-exec`; no host application and no real terminal was
started; the only processes started were the fixture probes under the seat
scratch; nothing outside my scratch and my two named files was written; no git
or jj command was run at all.

---

## 1. Source digests - one carry is missing

| file | receipt digest | on disk | verdict |
|---|---|---|---|
| `gutils.c` | `65086c29...e3771` | same, 100534 B | **MATCH** |
| `gio-tool-launch.c` | `16b4c868...f6595a` | same, 3991 B | **MATCH** |
| `spec-recognized-keys.html` | `7bc0b640...c03d9` | same, 24174 B | **MATCH** |
| `gdesktopappinfo.c` | `8e9ce1a8...95b0d` | **absent** | **MISMATCH** |
| `gshell.c` | `640a0d0f...60442` | **absent** | **MISMATCH** |

The round-99 fetch receipt says `gdesktopappinfo.c` and `gshell.c` are
"carried byte-identically from `.ufo/waves/round-98/fetch/` and re-hashed
here", and lists both digests. **The two files are not in
`.ufo/waves/round-99/fetch/`.** The digests themselves are correct: I
re-hashed the round-98 copies and they match the pinned values exactly, so
every line cited below is read from bytes the receipt already pins. The
carry simply did not happen.

**Routed to the L1 as a records item** (the fix is to copy the two files into
the round-99 fetch directory, or to drop the carry claim from the receipt). It
does not touch the C1 predicate: the bytes behind every cited line are the
pinned bytes.

**One new source fetched** (not a registry row, not opened by the L1 this
round), with the mandated command, counted only at HTTP 200:

```
curl -sSL -o gspawn-posix.c -w '%{http_code} %{url_effective}'
https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gspawn-posix.c
-> 200  https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gspawn-posix.c
62824 B  sha256 60d8a2d727fd346d0a2ffb76b6dd1eb1a00f8e1d0c03f0fbbfe1c3c78fbe4ab3
```

It is cited for exactly one line (`:725`, the `chdir` of the working
directory) and **needs a registry row** before any committed artefact may
cite it. The other ten `gspawn-posix.c` facts below come from the same file
but only `:725` is load-bearing.

---

## 2. The rules, with file:line

**R1 - load gate.** `g_desktop_app_info_load_from_keyfile`
(`gdesktopappinfo.c:1893`). The `Path` key is read first (`:1924`), then
**TryExec** (`:1947`, lookup `:1951`), then **Exec** (`:1963`, parse `:1985`,
program lookup `:1993`). Both lookups are
`g_find_program_for_path (token, NULL, path)` - the PATH argument is NULL, so
the **process** PATH is used (`gutils.c:370-373`), and the working-dir
argument is the entry's `Path=` value. A miss is a **load** refusal.

**R1b - TryExec is checked before Exec**, and its failure is the same load
refusal (`:1952`).

**R2 - terminal.** `prepend_terminal_to_vector` (`:2748`). The twelve rows are
at `:2762-2778` in table order; the search loop is `:2797-2806`; the vector is
built at `:2814-2830`. The PATH argument is `g_environ_getenv (envp, "PATH")`
(`:3028`) and the working dir is `info->path` (`:3029`). The refusal text is
`:3031-3032`.

**R3 - argv[0] after the prepend.** `:3064-3101`: the test at `:3066-3068`,
the lookup at `:3073-3080`, the replacement at `:3082-3086`, the refusal text
at `:3092-3094`.

**R4 - cwd.** `g_spawn_async_with_fds (info->path, ...)` at `:3134` (the
declaration cites `:3116-3126`; the call is `:3134-3144`, the wrapped argv
`:3124-3130`). `gspawn-posix.c:725` does
`if (working_directory && chdir (working_directory) < 0)`.

**R5 - env.** `:3036-3040`: `GIO_LAUNCHED_DESKTOP_FILE` = `info->filename`,
which is the **canonicalised** desktop path (`gio-tool-launch.c:91`
`g_canonicalize_filename`).

**R6 - `g_find_program_for_path` (`gutils.c:300-519`).** Numbered decision
tree:

- **G1** `:322-327` - working dir join: `working_dir && !absolute(program)` ->
  `program = g_build_filename (working_dir, program)`. This makes the program
  absolute when the working dir is absolute, which decides G2.
- **G2** `:332-337` - absolute-or-slash branch: `absolute(program) ||
  strchr (original_program, '/')` -> **no PATH walk at all**.
- **G3** `:339-340` - the executable test: `IS_EXECUTABLE && !IS_DIR`.
- **G4** `:344-357` - on a hit: absolute -> as-is; relative -> `cwd + "/" + program`.
- **G5** `:359-365` - on a miss: an **absolute** original -> return NULL (a hard
  refusal); a relative one falls through to the PATH walk.
- **G6** `:368` - `program = original_program` (the working-dir join is undone).
- **G7** `:370-373` - PATH unset -> `g_getenv ("PATH")`.
- **G8** `:376-389` - PATH unset -> the default `"/bin:/usr/bin:."` (GLib puts
  `.` **last**, for security).
- **G9** `:462-477` - the PATH walk; an **empty entry** (leading colon, two
  adjacent colons, trailing colon) means the **current directory**.
- **G10** `:479-484` - a **relative PATH candidate** is joined with the
  working dir.
- **G11** `:486-487` - the same executable-and-not-a-directory test as G3.
- **G12** `:490-497` - on a hit: absolute -> as-is; relative -> **absolutised
  against the process cwd**.
- **G13** `:518` - no entry matched -> NULL.

**R7 - a directory as the Exec program.** The `!IS_DIR` half of
`gutils.c:339-340` (and `:486-487` on the PATH). The declaration cites
`gutils.c:352-356`; that range is the cwd-absolutisation arm of G4, not the
test.

**Empty `Path=`** is normalised to NULL at `:2062-2066`
(`if (info->path && info->path[0] == '\0') { free; info->path = NULL; }`), so
an empty `Path=` inherits the launcher's cwd exactly like an absent `Path=`.
**The two are one case, not two.**

---

## 3. The three findings that decide the model

### (a) Under a terminal the program token is **not** absolutised

The prepend at `:3027` runs **before** the R3 block at `:3066`. With
`Terminal=true`, `argv[0]` is already the terminal's absolute path, so the R3
test is false and **the program token is never looked up**:

```
v8_token_relative_kgx   Exec=probe, Terminal=true
  terminal receives  TERM_ARGV0={root}/bin/kgx  TERM_ARGC=2  TERM_A0=-e  TERM_A1=probe
  program receives   ARGV0=probe              <-- RAW, not {root}/bin/probe
v8_token_absolute_kgx   Exec={root}/bin/probe
  terminal receives  TERM_A1={root}/bin/probe
  program receives   ARGV0={root}/bin/probe
v6 base_ok             no terminal
  program receives   ARGV0={root}/bin/probe   <-- ABSOLUTE
```

A candidate that absolutises the token under a terminal is wrong, and this is
the mutant most likely to survive a naive implementation.

### (b) Table order beats the working dir; the working dir beats the PATH

```
v9_wd_kgx_vs_path_xdg    kgx(row 1) in Path=, xdg-terminal-exec(row 0) on PATH
  -> the terminal is {root}/bin/xdg-terminal-exec        (row 0 wins)
v9_wd_kgx_vs_path_xterm   kgx(row 1) in Path=, xterm(row 11) on PATH
  -> the terminal is {root}/wd/kgx                      (row 1 beats row 11)
v9_wd_xdg_vs_path_kgx    xdg-terminal-exec(row 0) in Path=, kgx(row 1) on PATH
  -> the terminal is {root}/wd/xdg-terminal-exec
```

So: **table order first**, and **within one row** the working dir is tried
before the PATH walk.

### (c) The program lookup prefers the working dir over the PATH

```
v10_load_gate_working_dir_wins   probe in {root}/wd and {root}/bin
  -> ARGV0={root}/wd/probe                     (the working dir wins)
v9_working_dir_only              probe only in {root}/wd
  -> ARGV0={root}/wd/probe                     (the load gate finds it there)
v10_load_gate_path_only          probe only in {root}/bin
  -> the load gate PASSES; the launch then fails on the cwd
```

This follows from G1: the working-dir join makes the program absolute, so G2
takes the absolute branch and the PATH walk is never reached.

---

## 4. The eight named edge shapes - all measured, all twice, all agreeing

1. **Terminal order, two terminals present** - all eleven adjacent pairs
   measured (`v8_order_00`...`v8_order_10`) plus all twelve rows alone
   (`v8_row_00`...`v8_row_11`). Table order is exactly as `:2765-2778` reads.
2. **`kgx -e`** - `TERM_ARGC=2`, `TERM_A0=-e`, `TERM_A1=probe`. The full
   vector GIO builds for `Exec="probe --flag val"` is
   `TERM_ARGC=4, TERM_A0=-e, TERM_A1=probe, TERM_A2=--flag, TERM_A3=val`; the
   program then receives `ARGC=2, A0=--flag, A1=val`. `exec_arg` is NULL for
   `xdg-terminal-exec` only - every other row contributes one extra element.
3. **No terminal** - `gio: Unable to launch application '<desktop>': Unable to
   find terminal required for application`, rc 1. With `Path=` also broken the
   **no-terminal refusal comes first**, ahead of the cwd failure.
4. **`Path=` empty** - rc 0, `CWD={root}/work` (the launcher cwd, inherited).
   **Byte-identical to the absent-`Path=` case** (`:2062-2066`).
5. **`Path=` nonexistent** - `gio: Unable to launch application '<desktop>':
   Failed to change to directory "<root>/nodir" (No such file or directory)`,
   rc 1. A relative `Exec` gives the **same** outcome, because the load gate
   still finds the program on the PATH. A `Path=` naming a regular file gives
   `(Not a directory)`.
6. **`Exec` naming a directory** - `gio: Unable to load application
   information for '<desktop>'`, rc 1, both in the absolute form and as a
   directory on the PATH. The control (the same name as a regular file)
   launches.
7. **A relative PATH entry resolved through `Path=`** - `PATH=relbin`,
   `Path={root}/wd`, probe at `{root}/wd/relbin/probe` ->
   `ARGV0={root}/wd/relbin/probe`. Without a working dir the same shape
   resolves against the process cwd (`ARGV0={root}/work/relbin/probe`) - the
   relative-hit absolutisation of G12. A trailing slash gives
   `{root}/wd/relbin//probe`; an absolute PATH entry ignores `Path=`.
8. **`%f` with two arguments under `Terminal=true`** - **two spawns, in
   argument order**: `TERM_A2={root}/f1.txt` then `TERM_A2={root}/f2.txt`.
   The same launch without a terminal gives two spawns whose programs receive
   `ARGC=1` and `A0={root}/f1.txt` / `{root}/f2.txt`. `%F` gives **one** spawn
   with both files in one vector.

---

## 5. The cause taxonomy, as measured

| cause | text (gio's own, verbatim apart from the quote marks) | rc |
|---|---|---|
| `load` | `Unable to load application information for '<desktop>'` | 1 |
| `desktop-file` | `Unable to load '<desktop>': <reason>` | 1 |
| `no-exec` | `Unable to launch application '<desktop>': Desktop file didn't specify Exec field` | 1 |
| `exec-parse` | `Unable to launch application '<desktop>': Text was empty (or contained only whitespace)` | 1 |
| `no-terminal` | `Unable to launch application '<desktop>': Unable to find terminal required for application` | 1 |
| `program-not-found` | `Unable to launch application '<desktop>': Program '<x>' not found in $PATH` | 1 |
| `cwd-failed` | `Unable to launch application '<desktop>': Failed to change to directory "<path>" (No such file or directory)` | 1 |

`load` and `desktop-file` are **different texts** and must stay different
causes: the first is the app-level refusal (the load gate, a bad `Exec`
escape, a wrong `Type`, a directory `Exec`), the second the keyfile-level one
(the file is missing, or it is not a key file).

`program-not-found` is **reachable** and its text is exact: with `Exec=%f` and
a program literally named `%f` on the PATH, the load gate passes (it looks up
the literal `%f`) and the launch then fails with `Program '<file>' not found
in $PATH`.

**Note for the case file.** gio's messages carry U+2018/U+2019 quotation
marks. Committed artefacts must be ASCII, so the case file should hold the
ASCII apostrophes and the comparison should normalise - a byte-for-byte
comparison against the real stderr will fail on the quote marks.

---

## 6. Shapes I could not make gio answer

Full detail with commands and outputs is in the receipt, section 5. In short:

- A relative PATH entry that does **not** exist under the launcher cwd cannot
  produce a launch - `gutils.c:486-487` tests the candidate relative to the
  process cwd, so the relative-entry shape is only meaningful **with** a
  working dir. Measured refusal: `Unable to load application information`.
- A directory reached through a relative PATH entry carries **no signal**:
  "the directory was rejected" and "the program was not found" produce the
  identical text. The signal is only in the absolute form.
- The order of the R3 lookup relative to the prepend **cannot be isolated by
  a case**: GIO does not change `argv[0]`'s identity between the two blocks.
  The source order settles it and finding (a) is the observable consequence.
- The spawn order of a multi-spawn launch **under a terminal** is sequential
  by construction, so the ordinal of concurrent spawns is not observable; the
  r98 limit carries.
- `GIO_LAUNCHED_DESKTOP_FILE` for a desktop loaded **by id** is not reachable
  from `gio launch` at all (the CLI takes a path, `gio-tool-launch.c:91`).
- The portal / `DBusActivatable` path is not reachable from a plain desktop
  file with no session bus.
- An absolute `Path=` that is a **symlink** to a directory was not measured;
  `chdir` resolves it and the child reports the resolved path, but I make no
  claim.
- The `cwd-failed` errno text for a relative `Path=` that exists but is not
  searchable was not exercised.

---

## 7. What the candidate must code (the five rules)

- **R1** load gate - TryExec first (`:1947-1959`), then Exec's argv[0]
  (`:1974-2006`); both `g_find_program_for_path(token, NULL, Path=)`; a miss
  is the `load` refusal.
- **R2** terminal - twelve rows in table order; per row the working dir is
  tried before the PATH walk; first hit wins; the vector is
  `[terminal_abs, exec_arg?, <original argv>]`; `exec_arg` present for every
  row except `xdg-terminal-exec`.
- **R3** the argv[0] lookup at `:3066-3101` **runs only when there is no
  terminal**. With a terminal, the token is passed through **raw**; without
  one, a relative token becomes the absolute path the lookup returns and a
  miss is `Program '%s' not found in $PATH`.
- **R4** cwd - the child's cwd is `Path=`; an empty `Path=` is normalised to
  NULL (`:2062-2066`) and inherits the launcher's cwd; a `Path=` that cannot
  be entered is `cwd-failed`.
- **R5** env - `GIO_LAUNCHED_DESKTOP_FILE` = the **canonicalised** desktop
  path (measured: a relative argument `app.desktop` arrives as
  `{root}/work/app.desktop`, and `../app.desktop` as `{root}/app.desktop`).
- **R6** the lookup semantics - G1 -> G13 as tabulated in section 2.

**The two mutants most likely to survive a naive implementation:** (i)
absolutising the program token under a terminal (measured wrong: `ARGV0=probe`,
not the absolute path); (ii) resolving the program against the PATH before the
working dir (measured wrong: the working dir wins).

---

## 8. Instrumentation notes (so the L1 can reuse or reject it)

- The probe is a **compiled C program**, not a shell script: a shell script's
  `$0` is the script path as exec'd, **not** the `argv[0]` the program
  received, so a shell probe cannot answer the R3 question at all. My first
  four passes used a shell probe and produced a wrong `ARGV0`; the C probe
  corrected it. A candidate's oracle must not make the same mistake.
- Each spawn writes **one record into its own file**, named with a sequence
  number assigned under an exclusive `fcntl` lock (round-98 lessons M98-1 /
  M98-7: a shared output file races, and a multi-spawn launch then looks like
  "the last argument wins").
- The terminal stand-in is a second compiled C program that records the
  vector it was handed and then `execvp`s the program, so the program's own
  argv0 and cwd are observed under a terminal.
- **Agreement**: the 54-case set was run twice and compared label-by-label -
  `agree=54 disagree=0`. The v8, v9, v10 and v11 sets were re-run the same
  way and agreed. Every label quoted in this report is from an agreeing pair.
- Fixture bugs found and fixed along the way, all of which would have
  produced wrong labels: programs written 0644 (not executable) while the
  fixture assumed 0755; a relative output root (the desktop path was built
  relative to the launch cwd); `flock(1)` unavailable under the restricted
  PATH (replaced with a shell `set -C` claim); the terminal stand-in told
  `-e` for every row although `gnome-terminal` uses `--` and `mate-terminal`
  uses `-x`; and a `Path=`-is-a-file case that had no program on the PATH, so
  it refused for the wrong reason.

---

## 9. Tooling

No package was installed, upgraded or removed by this seat, so there is no
install to record (tool / version / channel / reason). The C probes were built
with the host's existing `/usr/bin/cc`:
`cc -O1 -static -o probe.bin probe.c` and `cc -O1 -static -o termfake.bin
termfake.c`, both local to the seat scratch. No pacman transaction was run
(round-99's host guard pauses all of them). No host service was restarted, no
sysctl was touched, no `~/.config` was written, no credential file was read.

## 10. Artefacts

- receipt: `.ufo/waves/round-99/receipts/scout-env-r99.txt` (555 lines, ASCII)
- report: `.ufo/waves/round-99/w1/R99MScoutEnv.md` (this file)
- scratch (deleted before the yield):
  `/fast/scratch/hyaku/mado-r99/R99MScoutEnv` - `probe.c`, `termfake.c`,
  `probe6.py`, `gen6.py`...`gen11.py`, `compare.py`, `cases6.json`...
  `cases11.json`, `out6/`...`out11/` (the per-case labels), `gspawn-posix.c`.
- the candidate `tools/mado-launchenv.py` was **not** touched.

## 11. Cross-domain evidence

Owning domain: none (the launch-environment surface is not a domain this lane
owns elsewhere). Sweep: the round-98 registry rows `S504`/`S506`/`S528`/
`S529` and the round-98 `tools/mado-execargv.py` were read for the boundary
only; no registry row was added or edited by this seat, and the one new source
(`gspawn-posix.c`) is reported for a registry row rather than written into
`corpus/SOURCES.md`, which this seat may not touch.
