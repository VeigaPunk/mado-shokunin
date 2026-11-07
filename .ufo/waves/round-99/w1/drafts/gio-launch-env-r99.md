---
source: S532 (GLib 2.90.1 gio-tool-launch.c 16b4c8683b00407670f600eda0e65e9d929a59daac499cbe8f3d1fd532f6595a, 3991 B, 134 L - the `gio launch` CLI: the canonicalized desktop argument at :91, the key-file pre-check at :97-104, the constructor at :106, the two print_error shapes at :109 and :121, and the per-argument `g_file_new_for_commandline_arg` at :116), S533 (GLib 2.90.1 gutils.c 65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771, 100534 B, 3245 L - new scope on the file S506 holds: `g_find_program_for_path` at :300-500, the working-dir join at :322-327, the absolute/slash branch at :331-357, the PATH source and default at :370-389, and the entry walk at :462-500), S534 (Desktop Entry Specification, recognized keys, https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html 7bc0b6401cda9c019d5b89a2fab053d216eb937c83602df838a6c0a1175c03d9, 24174 B, HTTP 200 at the recorded URL; the `TryExec` sentence at rendered lines 114-119, `Path` at :127-128, `Terminal` at :129-130), S528 (GLib 2.90.1 gdesktopappinfo.c 8e9ce1a8327a2daf6bc16e8dcfb653c482afde7bebc2ca2621747626b5495b0d, 163369 B, 5356 L - new scope on the file S504/S528 hold: `is_invalid_key_error` at :1885-1891, the load gate at :1894-2005, `info->path`/`info->terminal` at :2018-2019, `known_terminals` at :2765-2778, `prepend_terminal_to_vector` at :2748-2836, and the spawn tail at :3027-3144), S529 (GLib 2.90.1 gshell.c 640a0d0fbc9c50d0c70eb8f9ff2c4994392515c6174f76ade9292d7500e60442, 21464 B, 730 L - the `g_shell_parse_argv` call the load gate makes at gdesktopappinfo.c:1978), S531 (`gio(1)` GLib 2.90.1 manual, `/usr/share/man/man1/gio.1.gz`, container sha256 810077be12cf2df5006db1e1b9b967f6c505930033c68aa9cfc964281906a565, decompressed 84b3cdad868feecd69f113b789d7009113e16531b67d750cd0e424ba2bcb8bc5, 781 lines; `launch` at :218-221)
verified-at: 2026-11-07 - `glib2 2.90.1-1`; the oracle `/usr/bin/gio` sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462. The three GLib files were re-hashed in this seat's scratch against the L1 receipt (`.ufo/waves/round-99/receipts/sources-open-r99.txt`) and match byte for byte; the spec page was fetched by this seat at the recorded URL (`curl -sSL -o ... -w '%{http_code} %{url_effective}'` -> `200 https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html`) and its sha256 equals the L1's row, so the digest is confirmed by a second fetch. The 24 rows of section 13 are this seat's read-only runs of that binary over case roots built under `/fast/scratch/hyaku/mado-r99/R99MScribe`; every `gio launch` call ran under `env -i` with a PATH holding only the case's own bin directories, no host application was started, and no host file was read by any probe.
recheck: 180d - re-pull `gdesktopappinfo.c`, `gutils.c` and `gio-tool-launch.c` at the next GLib tag that changes any of them (2.90.1 is the pin) and re-open the recognized-keys page at its current locator; also when `glib2` leaves 2.90.1-1 or the `gio` CLI's `launch` spelling moves. A change to the twelve-row `known_terminals` table, the load gate's two `g_find_program_for_path` calls, the `working_dir` argument of any of the four searches, the `GIO_LAUNCHED_DESKTOP_FILE` setenv or the `g_spawn_async_with_fds` working-directory argument flips this entry.
covers: the **spawn environment** GIO 2.90.1 builds around a launch argv - the load gate that decides whether a desktop file is launchable at all (both the `TryExec` check and the `Exec` argv[0] check, and the directory half of the executable test); the twelve-row known-terminals table with its order and its `exec_arg` column; `g_find_program_for_path`'s decision tree as a table; the terminal prepend; the post-prepend `argv[0]` lookup and what it does **not** resolve; `Path=` as the child's working directory and as the working directory of four program searches; the empty-`Path=` inheritance; `GIO_LAUNCHED_DESKTOP_FILE`; the two refusal shapes with their exact messages; the `Terminal`/`Path`/`TryExec` spec-vs-implementation deltas; and the named limits.
---

# The launch spawn environment GIO 2.90.1 builds

Rounds 91-97 answered *which* MIME type and *which* application; round 98 answered *which argv
vectors* a launch spawns. This entry answers what surrounds those vectors: whether the desktop file
loads at all, which program the argv is handed to when `Terminal=true`, what the child's working
directory is, what one environment value it carries, and which program lookup runs **after** the
terminal has been prepended. The surface is the five rules a model of `gio launch` must add to the
round-98 argv model, plus the lookup those rules sit on.

Every behavioural sentence below carries a located line of one of the fetched files or a probe row
of section 13. Where a sentence is a measurement whose mechanism lives in a file this round did not
open, it says so and names the file (section 12).

## 1. Question and scope

### 1.1 The surface

- **What is read.** `gio launch DESKTOP-FILE [FILE-ARG ...]` (`gio.1:218`) canonicalizes the desktop
  argument (`gio-tool-launch.c:91`), pre-checks the key file (`:97-104`), constructs the app info
  (`:106`), turns each remaining argument into a `GFile` (`:116`), and calls `g_app_info_launch`
  (`:119`). A refusal prints one of two lines (`:109`, `:121`) and exits 1.
- **What is modelled.** Five rules and the lookup they sit on:
  - **R1/R1b/R7 the load gate** - the `TryExec` check, the `Exec` argv[0] check, and the directory
    half of the executable test (section 2).
  - **R2 the terminal prepend** - the twelve-row table, its order, its `exec_arg` column, and the
    prepend itself (sections 3 and 5).
  - **R6 `g_find_program_for_path`** - the decision tree all four searches share (section 4).
  - **R3 the post-prepend `argv[0]` lookup** (section 6).
  - **R4 `Path=`** - the child's cwd and the searches' working directory (sections 7 and 8).
  - **R5 `GIO_LAUNCHED_DESKTOP_FILE`** (section 9).
- **What is out of scope.** The spawn *order* of a multi-spawn launch (the round-98 limit carries:
  `do { } while (dup_uris != NULL)` at `gdesktopappinfo.c:3007-3186`); `DBusActivatable`; the
  `gio-launch-desktop` wrapper's own environment scrubbing (`:3105-3121`); the portal path; whether
  the process survives. The model answers the argv, the cwd and one env value; it starts nothing.

### 1.2 Evidence class

Sections 2-11 carry located source lines. Section 13 carries the oracle's answers on fixtures this
seat built and ran read-only; each row names the class it labels. The frozen case file for the round
(`.ufo/waves/round-99/controls/launchenv-cases-r99.json`, the oracle seat's artifact) must carry at
least one row per class named here; a class this entry names and that file does not carry is
unproved, not proved.

### 1.3 Conventions

- `gdesktopappinfo.c`, `gutils.c` and `gio-tool-launch.c` line numbers are those of the fetched
  bytes at the digests in the front matter. `spec:<n>` is the rendered line of the recognized-keys
  page (the page is one long line per table row, so a key's sentence is one or two rendered lines).
- The C source and the CLI print typographic quotation marks (U+2018/U+2019 around a path and
  U+201C/U+201D around a directory). This entry writes them as ASCII `'...'` and `"..."` and says so
  once here; the bytes on the wire are the typographic ones.
- A probe row is `P01`-`P24` (section 13). `<root>` stands for the case root.

## 2. The load gate (R1, R1b, R7)

### 2.1 The read order

`g_desktop_app_info_load_from_keyfile` (`gdesktopappinfo.c:1894-2005`) reads, in this order:

| step | read | line | refusal on |
|---|---|---|---|
| 1 | start group must be `[Desktop Entry]` | `:1905-1911` | any other start group |
| 2 | `Type=` must be `Application` | `:1913-1922` | absent or another type |
| 3 | `Path=` (the working directory) | `:1924-1933` | a key-file error other than "not found" |
| 4 | `TryExec=` and its program lookup | `:1935-1959` | a non-empty value that is not found |
| 5 | `Exec=` parse and its argv[0] lookup | `:1961-2004` | a parse error or a missing program |

Step 3 cannot refuse an absent or empty `Path`: `is_invalid_key_error` (`:1885-1891`) returns FALSE
for `G_KEY_FILE_ERROR_KEY_NOT_FOUND` and `G_KEY_FILE_ERROR_GROUP_NOT_FOUND`, so a missing `Path=`
leaves `path` NULL and the load continues (measured P15). The same helper guards the `TryExec` and
`Exec` reads (`:1939`, `:1965`), so an absent `Exec` is not a read error either - it is skipped by
the non-empty test at `:1974`.

### 2.2 The two program checks

Both checks pass the **same** two arguments: the program name, a NULL `path`, and the entry's
`Path=` value as `working_dir`.

- `TryExec`: `if (try_exec && try_exec[0] != '\0')` (`:1947`) then
  `g_find_program_for_path (try_exec, NULL, path)` (`:1951`).
- `Exec`: `g_shell_parse_argv (exec, &argc, &argv, NULL)` (`:1978`), then
  `g_find_program_for_path (argv[0], NULL, path)` (`:1993`), with the comment
  `Use the desktop file path (if any) as working dir to search program` (`:1992`).

A NULL return from either call returns FALSE from the loader (`:1952-1957`, `:1996-2002`), the
constructor returns NULL (`:1054-1062`), and the CLI prints the load refusal (`gio-tool-launch.c:109`).

The NULL `path` argument is what makes the search use the **process** `PATH`: inside
`g_find_program_for_path`, `if G_LIKELY (original_path == NULL) path = g_getenv ("PATH")`
(`gutils.c:370-371`). The `working_dir` argument is `Path=`, so a bare `Exec=` name is first joined
to `Path=` and found there even when it is on no `PATH` entry. P21 isolates that join: with
`Exec=probe.sh`, `Path=<root>/bin21` and `PATH=<root>/empty21` (which holds nothing), the file
loads, and the child's `argv[0]` is the absolute `<root>/bin21/probe.sh`. P10 shows the same
pass-through with the directory also on `PATH`. With no `Path=` and no `PATH` entry holding the
name, the same file refuses (P11).

### 2.3 R7: the directory half of the executable test

The executable test is a conjunction everywhere it appears:

```
if (g_file_test (program, G_FILE_TEST_IS_EXECUTABLE) &&
    !g_file_test (program, G_FILE_TEST_IS_DIR))
```

(`gutils.c:339-340` for the absolute/slash branch, `:486-487` for the PATH walk). A directory is
executable to `access(2)` and is excluded by the second half, so `Exec=<a directory>` is a load
refusal (measured P13), not a spawn failure.

### 2.4 The load refusal table

| condition | line | message | exit | probe |
|---|---|---|---|---|
| `TryExec` non-empty and not found | `:1947-1957` | `Unable to load application information for '<desktop>'` | 1 | P12 |
| `Exec` argv[0] not found | `:1978-2002` | same | 1 | P09, P11 |
| `Exec` argv[0] is a directory | `:1993` + `gutils.c:339-340` | same | 1 | P13 |
| `Exec` fails `g_shell_parse_argv` | `:1978-1984` | same | 1 | (round-98 `exec-parse` class) |
| start group or `Type` wrong | `:1905-1922` | same | 1 | (round-98 `desktop-file` class) |

The load refusal prints **only** the outer sentence (`gio-tool-launch.c:109`); the cause is not
printed. A malformed or missing key file is a *different* shape, caught before the constructor
(`gio-tool-launch.c:97-104`): `Unable to load '<file>': <key-file error>`.

## 3. The known-terminals table

`known_terminals` (`gdesktopappinfo.c:2765-2778`) is a static array of twelve rows, each an
executable name and an optional argument:

| # | exec | exec_arg | line |
|---|---|---|---|
| 1 | `xdg-terminal-exec` | NULL | `:2766` |
| 2 | `kgx` | `-e` | `:2767` |
| 3 | `gnome-terminal` | `--` | `:2768` |
| 4 | `mate-terminal` | `-x` | `:2769` |
| 5 | `xfce4-terminal` | `-x` | `:2770` |
| 6 | `tilix` | `-e` | `:2771` |
| 7 | `konsole` | `-e` | `:2772` |
| 8 | `nxterm` | `-e` | `:2773` |
| 9 | `color-xterm` | `-e` | `:2774` |
| 10 | `rxvt` | `-e` | `:2775` |
| 11 | `dtterm` | `-e` | `:2776` |
| 12 | `xterm` | `-e` | `:2777` |

The table is searched in array order and the **first** hit wins (`:2797-2806`); the loop stops at
the first non-NULL lookup (`:2801-2805`). Each row is looked up with
`g_find_program_for_path (known_terminals[i].exec, path, working_dir)` (`:2799-2800`) where `path`
is the launch environment's `PATH` and `working_dir` is `Path=` (section 5). No hit returns FALSE
(`:2808-2812`) and the caller turns that into the terminal refusal (section 10).

Order is observable: with both `xdg-terminal-exec` and `kgx` on the case PATH, row 1 wins and the
child's `argv[0]` is the `xdg-terminal-exec` fixture (P01). With only `kgx` present the row-2
`exec_arg` appears as a separate argv element (`TA1=-e`, P02); with only `xterm`, `-e` (P03); with
only `gnome-terminal`, `--` (P04). A terminal that is not one of these twelve names is never used,
whatever the environment says: the file contains no `getenv` of `TERMINAL` or `COLORTERM`
(`grep -c 'getenv ("TERMINAL")' gdesktopappinfo.c` = 0).

## 4. `g_find_program_for_path`'s decision tree

`g_find_program_for_path (program, path, working_dir)` (`gutils.c:300-500`) is the single lookup all
four searches call. Its doc sentence is
`Locates the first executable named @program in @path, in the same way that execvp() would locate it.`
(`gutils.c:274-276`). As a table:

| step | condition | action | line |
|---|---|---|---|
| 1 | `working_dir != NULL` and `program` is not absolute | `program = working_dir/program` | `:322-327` |
| 2 | `program` is absolute, or the **original** program contains `/` | test it: executable and not a directory; return it absolute (joining the process cwd when the test path is relative) | `:331-357` |
| 2b | step 2's test failed and the original program was absolute | return NULL (never walk PATH) | `:359-368` |
| 3 | otherwise | restore the original program; `path` = the caller's `path`, else `getenv("PATH")`, else `/bin:/usr/bin:.` | `:370-389` |
| 4 | for each `:`-separated entry | an empty entry (leading, trailing or doubled colon) means the current directory; a relative candidate is joined to `working_dir`; test executable and not a directory | `:462-487` |
| 5 | a hit | return it absolute: as-is when absolute, else joined to the process cwd | `:488-497` |
| 6 | no entry hit | return NULL | `:500` |

Three consequences a model must carry:

- **The `working_dir` join happens twice**: once on the program (`:322-327`) and once per PATH
  candidate (`:479-484`). The second join is what lets a `Path=`-relative `Exec` be found through a
  relative PATH entry.
- **The default PATH is `/bin:/usr/bin:.`** when the environment has no `PATH` at all
  (`:376-389`), with the comment `In GLib we put . last, for security` (`:383-384`). An empty `PATH`
  string is *not* unset: it is one empty entry, which means the current directory (`:471-475`).
- **A relative hit is returned absolute against the process cwd** (`:490-497`), so the value the
  caller receives is always absolute when it is non-NULL. That is why the terminal prepend's
  `argv[0]` survives the post-prepend test (section 6).

The empty-`working_dir` question is answered by the `working_dir &&` test itself: an empty string is
non-NULL, so the join runs, but `g_build_filename ("", "probe.sh")` yields a **relative**
`probe.sh`, which step 2 then discards (not absolute, no `/` in the original) and step 4 re-tests
against each PATH entry. Measured: `Exec=./probe.sh` with `Path=` present-but-empty and the program
in the launcher's cwd launches with `argv[0] = <root>/./probe.sh` (P14), exactly as with no `Path=`
key at all (P15) - so an empty `Path=` is a no-op for the searches, not an absolute working
directory.

## 5. The prepend (R2)

The call site is the only one:

```
if (info->terminal && !prepend_terminal_to_vector (&argc, &argv,
                                                   g_environ_getenv (envp, "PATH"),
                                                   info->path))
```

(`gdesktopappinfo.c:3027-3029`). Note the two arguments: the search PATH is the **launch
environment's** `PATH` (`envp`, a copy of the process environment), and the working directory is
`Path=`. The search is therefore the same string the load gate used, but the working directory is
applied to the terminal names too - measured P19: with `Path=<root>/bin19` holding both
`xdg-terminal-exec` and `probe.sh`, and `PATH` holding neither, the terminal is found through the
working-dir join and the child's cwd is `bin19`.

`prepend_terminal_to_vector` (`:2748-2836`) then builds the new vector:

- `term_argc = term_arg ? 2 : 1` (`:2814-2815`, comment `check if the terminal require an option`);
- `real_argv[0] = found_terminal` (`:2821`);
- `real_argv[1] = exec_arg` when the row has one (`:2823-2824`);
- the old vector follows (`:2827-2828`), and `*argc` grows by `term_argc` (`:2834`).

The found terminal is absolute (section 4, step 5), so the prepended `argv[0]` always passes the
post-prepend test of section 6.

## 6. The post-prepend `argv[0]` lookup (R3)

After the prepend and after `GIO_LAUNCHED_DESKTOP_FILE` is set, the code tests `argv[0]` again:

```
if (!g_path_is_absolute (argv[0]) ||
    !g_file_test (argv[0], G_FILE_TEST_IS_EXECUTABLE) ||
    g_file_test (argv[0], G_FILE_TEST_IS_DIR))
```

(`gdesktopappinfo.c:3066-3068`). When the test fires and `argv[0]` is not absolute, the lookup is
`g_find_program_for_path (program, g_environ_getenv (envp, "PATH"), info->path)` (`:3070-3077`);
a hit replaces `argv[0]` (`:3082-3086`), a miss raises
`Program '<x>' not found in $PATH` (`:3092-3094`). An absolute `argv[0]` that failed the
executable-or-directory half skips the lookup (`:3072`) and goes straight to the same refusal.

**What this lookup does and does not do.** It rewrites `argv[0]` only. Two consequences:

- With `Terminal=false`, a bare `Exec=` name found through `Path=` is replaced by its absolute path
  even when it is on no PATH entry (P21: `Exec=probe.sh`, `Path=<root>/bin21`, `PATH=<root>/empty21`,
  child `argv[0] = <root>/bin21/probe.sh`).
- With `Terminal=true`, `argv[0]` is the **terminal**, so the terminal is kept and the `Exec`
  program name at index 1 is passed on **unresolved**. Measured P19: the terminal fixture receives
  `TA1=probe.sh` (the literal `Exec` name), not an absolute path. P22 makes the consequence
  visible: the program exists only in `Path=`, the terminal's own `exec` cannot find it, the terminal
  prints `exec: probe.sh: not found`, and `gio launch` still exits **0** - the spawn succeeded, the
  child failed.

**When the refusal is reachable.** The load gate (`:1974`) skips its check when `Exec` is empty, so
`Exec=` plus one argument reaches this lookup with the argument as `argv[0]`. A non-executable
argument refuses with `Program '<arg>' not found in $PATH` (P23, exit 1); an executable argument is
spawned as the program (P24). That is the only shape this seat found where the load gate passes and
this lookup refuses.

The spawn itself passes `G_SPAWN_SEARCH_PATH` (`#define _SPAWN_FLAGS_DEFAULT (G_SPAWN_SEARCH_PATH)`,
`:2944`), so a slashless `argv[0]` would also be searched by the spawn; the lookup above makes that
moot by handing the spawn an absolute path whenever it can.

## 7. `Path=` as cwd and as the searches' working dir (R4)

`Path=` is read once (`gdesktopappinfo.c:1924-1933`), stored as `info->path` (`:2018`), and then
used in **five** places:

| use | line | measured |
|---|---|---|
| the child's working directory, as the first argument of `g_spawn_async_with_fds` | `:3134-3135` | P06 (`CWD=<root>/work`) |
| `TryExec`'s `working_dir` | `:1951` | source only (not probed) |
| `Exec` argv[0]'s `working_dir` | `:1993` | P21 (isolates the join), P10 |
| the terminal search's `working_dir` | `:2799-2800` | P19 |
| the post-prepend lookup's `working_dir` | `:3075-3076` | P21 |

A relative `Path=` is passed through verbatim: `Path=work` with the launcher's cwd at `<root>` gives
the child `CWD=<root>/work` (P17). The value is not canonicalized and not checked at load time, so a
`Path=` that cannot be entered refuses nothing until the spawn, where it becomes a **launch**
refusal, not a load refusal:

```
gio: Unable to launch application '<desktop>': Failed to change to directory "<path>" (No such file or directory)
```

(P08, exit 1). The `chdir` and that message live in `gspawn.c`, which this round did not open; the
shape is measured, not source-located (section 12).

## 8. The empty-`Path=` inheritance

`Path=` present with an empty value is not the same *value* as an absent key, but it behaves the
same in both places:

- **As the cwd.** `g_key_file_get_string` returns `""` for a present-empty key and NULL for an
  absent one; `info->path` is `""` in the first case (`:1924-1933`, `:2018`) and NULL in the second.
  Both inherit the launcher's cwd: P07 (`Path=`) and P15 (no `Path=`) both record `CWD=<root>`, the
  launcher's cwd. The spawn call passes the value verbatim (`:3134`), so the empty-vs-NULL decision
  is taken inside `gspawn.c`, which this round did not open.
- **As the searches' working directory.** The join is a no-op for a relative program (section 4,
  last paragraph): `Exec=./probe.sh` with `Path=` empty launches with
  `argv[0] = <root>/./probe.sh` (P14), the same record as with no `Path=` key (P15). The terminal
  search likewise finds its terminal on `PATH` (P20).

## 9. `GIO_LAUNCHED_DESKTOP_FILE` (R5)

```
if (info->filename)
  envp = g_environ_setenv (envp,
                           "GIO_LAUNCHED_DESKTOP_FILE",
                           info->filename,
                           TRUE);
```

(`gdesktopappinfo.c:3036-3040`). Three facts a model must carry:

- The value is `info->filename`, which for `gio launch` is the **canonicalized** desktop path: the
  CLI calls `g_canonicalize_filename (argv[1], NULL)` (`gio-tool-launch.c:91`) and constructs the
  app info from that string (`:106`). A relative desktop argument therefore reaches the child
  absolute: P18 passes `work/x.desktop` from cwd `<root>` and the child records
  `GDF=<root>/work/x.desktop`.
- The setenv happens **after** the terminal prepend and **before** the spawn (`:3027-3040`,
  `:3134`), so the terminal process and the program it execs both see it.
- The `TRUE` overwrite flag replaces any inherited value. The child's environment otherwise carries
  no other key this surface adds: in all 16 spawns that produced a record, `DESKTOP_STARTUP_ID` and
  `XDG_ACTIVATION_TOKEN` were unset (section 13, `DSI=<unset>`/`XAT=<unset>`). Those two are set
  only when a launch context yields a startup id (`:3048-3056`), which the CLI's plain
  `g_app_launch_context_new ()` (`gio-tool-launch.c:118`) does not.

`info->filename` is NULL only for an app info built from a key file rather than a file path
(`:2115-2135`); `gio launch` always builds from a path, so the "not set" branch is unreachable
through the CLI (section 12).

## 10. The two refusal shapes

`gio launch` has exactly two refusal lines, both exit 1:

| shape | message | line | cause carried in the message? |
|---|---|---|---|
| **load** | `Unable to load application information for '<desktop>'` | `gio-tool-launch.c:109` | no |
| **launch** | `Unable to launch application '<desktop>': <error>` | `gio-tool-launch.c:121` | yes, `<error>` |

The `<error>` of the launch shape is one of:

| cause | message | line | probe |
|---|---|---|---|
| no known terminal | `Unable to find terminal required for application` | `gdesktopappinfo.c:3031-3032` | P05 |
| program not found after the prepend | `Program '<x>' not found in $PATH` | `:3092-3094` | P23 |
| the cwd cannot be entered | `Failed to change to directory "<path>" (No such file or directory)` | `gspawn.c` (not opened) | P08 |

Two further shapes exist before either: the CLI's key-file pre-check
`Unable to load '<file>': <key-file error>` (`gio-tool-launch.c:97-104`) and the option/arity
refusals (`:62-82`). They are the round-98 `desktop-file`/`no-exec` causes and are not re-derived
here.

The exit status is the CLI's, not the child's: a spawn that succeeds exits 0 even when the child
then fails (P22: the terminal's `exec` failed, `gio` exited 0).

## 11. Spec-vs-implementation deltas

| key | the spec says | the implementation does | line | flip |
|---|---|---|---|---|
| `Path` | `If entry is of type Application, the working directory to run the program in.` (`spec:127-128`) | the child's cwd **and** the working directory of four program searches (section 7) | `:1951`, `:1993`, `:2799`, `:3075`, `:3134` | a `Path=` that does not exist refuses nothing at load and fails the spawn (P08) |
| `Terminal` | `Whether the program runs in a terminal window.` (`spec:129-130`) | a fixed twelve-name table searched on the launch PATH; a name not in the table is never used; no hit is a hard refusal | `:2765-2778`, `:2797-2812`, `:3027-3033` | a terminal emulator the spec would allow but the table does not name |
| `TryExec` | `If the file is not present or if it is not executable, the entry may be ignored (not be used in menus, for example).` (`spec:114-119`) | a hard load refusal with the same message as a missing `Exec` | `:1947-1959` | an implementation that ignores the entry instead of refusing the launch |
| `Terminal` + `Exec` | the spec says nothing about who resolves the program | the prepend happens before the argv[0] lookup, so the `Exec` name is passed to the terminal **unresolved** | `:3027-3029`, `:3066-3086` | a terminal that resolves its argument differently from `execvp` |
| `Terminal` + `exec_arg` | the spec says nothing | the row's `exec_arg` is inserted as a separate argv element before the old vector | `:2814-2824` | a table row whose argument form changes |
| empty `Path` | the spec does not distinguish absent from empty | empty inherits the cwd and is a no-op for the searches | `:1924-1933`, `:3134` | a `gspawn.c` that treats `""` as a directory |

## 12. Named limits

- **Spawn order of a multi-spawn launch** is not modelled (round-98 limit; `:3007-3186`).
- **`DBusActivatable`**, the `gio-launch-desktop` wrapper's environment scrubbing (`:3105-3121`), the
  portal path, and whether the process survives are not modelled.
- **`gspawn.c` was not opened this round.** The empty-`Path=` inheritance (section 8) and the
  `Failed to change to directory` text (section 7) are measured, not source-located.
- **The terminal fixtures are stand-ins.** The real `xdg-terminal-exec` on this host has its own
  configuration and argument handling; the model answers which name is prepended and with which
  `exec_arg`, not what that program does next.
- **The search PATH is the launch environment's PATH** (`envp`), which the oracle sets to the case's
  own bin directories. A launch context that rewrites `PATH` is not modelled.
- **`GIO_LAUNCHED_DESKTOP_FILE` is not set when `info->filename` is NULL** (`:3036`); unreachable
  through `gio launch` (section 9).
- **The twelve-name table is a 2.90.1 constant**; a distribution patch that adds or reorders a row
  flips section 3 and every case that depends on order.
- **`TERMINAL`/`COLORTERM` are never read** (`grep -c` = 0 in `gdesktopappinfo.c`); a model that
  consults them is wrong on this pin.
- **The load gate's cause is not printed** (`gio-tool-launch.c:109`), so a case can label the
  refusal but not which of the five conditions produced it; the oracle's `load` cause is one label
  for five conditions.

## 13. Probe rows

This seat's read-only runs, 2026-11-07, `/usr/bin/gio` sha256 `d2164260...c462`, `env -i` with a
PATH of the case's own bin directories only. `<root>` is the case root; `T0/TC/TA1` are the terminal
fixture's `$0`/`$#`/`$1`; `P0/PC/PA1` are the probe's; `CWD` is the child's `$PWD`; `GDF` is
`GIO_LAUNCHED_DESKTOP_FILE`. Full transcript: `.ufo/waves/round-99/w1/R99MScribe-probes.txt`.

| row | class | fixture | observed | labels |
|---|---|---|---|---|
| P01 | terminal-order | `Terminal=true`, `xdg-terminal-exec` and `kgx` both on PATH, `Path=<root>/work` | rc 0; `T0=<root>/bin1/xdg-terminal-exec`, `TC=2`, `TA1=<root>/bin1/probe.sh`; `CWD=<root>/work` | row 1 wins over row 2 |
| P02 | terminal-execarg | only `kgx` present | rc 0; `T0=<root>/bin2/kgx`, `TC=3`, `TA1=-e` | `kgx`'s `exec_arg` is a separate element |
| P03 | terminal-execarg | only `xterm` present | rc 0; `T0=<root>/bin3/xterm`, `TC=3`, `TA1=-e` | `xterm`'s `exec_arg` |
| P04 | terminal-execarg | only `gnome-terminal` present | rc 0; `T0=<root>/bin4/gnome-terminal`, `TC=3`, `TA1=--` | `gnome-terminal`'s `exec_arg` |
| P05 | no-terminal | `Terminal=true`, no known terminal on PATH | rc 1; `Unable to launch application '<desktop>': Unable to find terminal required for application` | the terminal refusal |
| P06 | path-cwd | `Path=<root>/work` | rc 0; `CWD=<root>/work` | `Path=` is the cwd |
| P07 | path-empty | `Path=` (present, empty) | rc 0; `CWD=<root>` | empty `Path=` inherits |
| P08 | cwd-failed | `Path=<root>/nope` | rc 1; `Failed to change to directory "<root>/nope" (No such file or directory)` | an unenterable `Path=` fails the spawn |
| P09 | load-gate | `Exec=nosuchprog-xyz %f` | rc 1; `Unable to load application information for '<desktop>'` | the load refusal |
| P10 | load-gate-workdir | `Exec=probe.sh`, `Path=<root>/bin10`, PATH also holds `bin10` | rc 0; `P0=<root>/bin10/probe.sh`, `CWD=<root>/bin10` | `Path=` set and the child's cwd is it (the join is isolated by P21) |
| P11 | load-gate | `Exec=probe.sh`, no `Path=`, not on PATH | rc 1; load refusal | the same name without the join |
| P12 | load-gate-tryexec | `TryExec=nosuch-tryexec`, valid `Exec` | rc 1; load refusal | `TryExec` refuses before `Exec` |
| P13 | load-gate-dir | `Exec=<root>/bin13/adir` (a directory) | rc 1; load refusal | the `!IS_DIR` half |
| P14 | path-empty-search | `Path=`, `Exec=./probe.sh`, program in cwd | rc 0; `P0=<root>/./probe.sh`, `CWD=<root>` | the empty-join is relative |
| P15 | path-empty-search | no `Path=` key, same program | rc 0; `P0=<root>/./probe.sh`, `CWD=<root>` | absent == empty for the search |
| P16 | argv0-lookup | `Exec=probe.sh`, `PATH=<root>/bin16` | rc 0; `P0=<root>/bin16/probe.sh` | the PATH hit is returned absolute |
| P17 | path-relative | `Path=work` (relative), absolute `Exec` | rc 0; `CWD=<root>/work` | a relative `Path=` resolves against the launcher cwd |
| P18 | gdf | desktop passed as `work/x.desktop` from cwd `<root>` | rc 0; `GDF=<root>/work/x.desktop` | `GIO_LAUNCHED_DESKTOP_FILE` is canonical |
| P19 | terminal-workdir | `Terminal=true`, `Exec=probe.sh`, `Path=<root>/bin19`, PATH without it | rc 0; `T0=<root>/bin19/xdg-terminal-exec`, `TC=2`, `TA1=probe.sh`; `CWD=<root>/bin19` | the terminal search uses `Path=`; the `Exec` name is passed unresolved |
| P20 | terminal-empty-path | `Terminal=true`, `Path=`, terminal on PATH | rc 0; `T0=<root>/bin20/xdg-terminal-exec`, `TC=1`, `TA1=<root>/bin20/probe.sh`; `CWD=<root>` | empty `Path=` is a no-op for the terminal search |
| P21 | argv0-lookup | `Exec=probe.sh`, `Path=<root>/bin21`, PATH without it | rc 0; `P0=<root>/bin21/probe.sh` | the post-prepend lookup rewrites `argv[0]` |
| P22 | terminal-program | `Terminal=true`, `Exec=probe.sh` only in `Path=`, PATH without it | rc 0; `TA1=probe.sh`; terminal stderr `exec: probe.sh: not found`; no probe record | the lookup does not resolve index 1 |
| P23 | program-not-found | `Exec=` (empty), argument a non-executable file | rc 1; `Program '<root>/bin23/x.txt' not found in $PATH` | the post-prepend refusal is reachable |
| P24 | program-not-found | `Exec=` (empty), argument an executable file | rc 0; `P0=<root>/bin24/probe.sh` | the same shape launches |

In all 16 rows that produced a probe record, `DSI=<unset>` and `XAT=<unset>` (section 9).
