# round 99 w1 - SOURCES rows for `corpus/knowledge/gio-launch-env-r99.md` (R99MScribe draft)

Target: the L1 appends these three rows to `corpus/SOURCES.md` after row S531 (the registry holds 466
rows at the base revision `2cbaa141`; S532-S534 are free - `grep -n '^| S53[234] ' corpus/SOURCES.md`
returns nothing). Shape: the 11-column fleet schema of the last ten rows (id | source | kind | tier |
scope | anchor | teaches | status | opened | recheck | used-by).

## 1. Rows

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S532 | GLib 2.90.1 `gio launch` CLI - https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gio-tool-launch.c (sha256 16b4c8683b00407670f600eda0e65e9d929a59daac499cbe8f3d1fd532f6595a, 3991 B, 134 L, HTTP 200 at the recorded URL); host package glib2 2.90.1-1, `/usr/bin/gio` sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462 | code | A | the installed `gio launch` CLI's own pre-processing and its two refusal lines: the canonicalized desktop argument, the key-file pre-check, the constructor, the per-argument `g_file_new_for_commandline_arg`, and the exit status | gio-tool-launch.c:91 (`g_canonicalize_filename (argv[1], NULL)`), :97-104 (key-file pre-check), :106 (constructor), :109 (load refusal), :116 (the argument append), :119-121 (launch and launch refusal) | the CLI canonicalizes the desktop path before the app info is built, so the child's `GIO_LAUNCHED_DESKTOP_FILE` is absolute even when the argument was relative; each FILE-ARG becomes a `GFile` through `g_file_new_for_commandline_arg`; and the CLI prints exactly two refusal lines, one without a cause and one carrying the error's message | mined | 2026-11-07 | 180d | corpus/knowledge/gio-launch-env-r99.md |
| S533 | GLib 2.90.1 `g_find_program_for_path` - https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c (sha256 65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771, 100534 B, 3245 L, HTTP 200 at the recorded URL; the same file S506 holds, new scope, census W04 expected); host package glib2 2.90.1-1 | code | A | the single program lookup all four launch searches call: the working-directory join, the absolute-or-slash branch, the PATH source and its default, the empty PATH entry, and the absolute return | gutils.c:274-276 (the doc sentence), :322-327 (the working-dir join), :331-357 (the absolute/slash branch and the executable-and-not-a-directory test), :359-368 (an absolute miss returns NULL), :370-389 (the PATH source and the `/bin:/usr/bin:.` default), :462-487 (the entry walk, the empty entry, the per-entry join), :488-497 (the absolute return) | a bare program is joined to `working_dir` before the PATH walk and each PATH candidate is joined to `working_dir` too; a relative hit comes back absolute against the process cwd; an unset PATH is `/bin:/usr/bin:.` while an empty PATH entry is the current directory; a directory is never a program | mined | 2026-11-07 | 180d | corpus/knowledge/gio-launch-env-r99.md |
| S534 | Desktop Entry Specification, recognized keys - https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html (sha256 7bc0b6401cda9c019d5b89a2fab053d216eb937c83602df838a6c0a1175c03d9, 24174 B, HTTP 200 at the recorded URL; fetched twice this round - the L1's `spec-recognized-keys.html` and this seat's `spec-terminal-path.html` - byte-identical) | spec | A | the documented contract for the three keys the launch environment reads: `TryExec`, `Path` and `Terminal`, with their declared types and optionality | recognized-keys.html rendered lines 114-119 (`TryExec`), 127-128 (`Path`), 129-130 (`Terminal`) | `Path` is documented as the working directory to run the program in and `Terminal` as whether the program runs in a terminal window; `TryExec` is documented as a soft signal ("the entry may be ignored") where GLib 2.90.1 refuses the load - the three deltas the entry's section 11 records | mined | 2026-11-07 | 180d | corpus/knowledge/gio-launch-env-r99.md |

## 2. Held rows that gain the entry in `used-by` (append only, no other cell moves)

| id | cell to append | why |
|---|---|---|
| S528 | `corpus/knowledge/gio-launch-env-r99.md` | the entry cites gdesktopappinfo.c's load gate (`:1894-2005`), `known_terminals` (`:2765-2778`), the prepend (`:2748-2836`) and the spawn tail (`:3027-3144`) |
| S529 | `corpus/knowledge/gio-launch-env-r99.md` | the entry cites the `g_shell_parse_argv` call the load gate makes (`gdesktopappinfo.c:1978`) |
| S531 | `corpus/knowledge/gio-launch-env-r99.md` | the entry cites `gio.1:218` for the `launch` synopsis |

## 3. Census expectation

- Rows: 466 -> 469. New ids S532, S533, S534; all tier A, all status `mined`.
- W04 duplicate-URL: **one** new warning, S533 against S506 (both `gutils.c` at the same URL, separate
  scopes). S532's `gio-tool-launch.c` and S534's `recognized-keys.html` are new URLs
  (`grep -c 'gio-tool-launch' corpus/SOURCES.md` = 0, `grep -c 'recognized-keys' corpus/SOURCES.md` = 0
  at the base revision), so no W04 for either.
- Read-back (round-98's R4): the three new rows name the entry in `used-by` from birth, and the entry's
  frontmatter names S528 S529 S531 S532 S533 S534 - the pair is symmetric in both directions.

## 4. Gate table (for `corpus/lessons/round-99.md`)

| row | locator | access | located quote | decision |
|---|---|---|---|---|
| S532 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gio-tool-launch.c (HTTP 200, 3991 B, sha256 `16b4c868...f6595a`); host package glib2 2.90.1-1 | 2026-11-07 | `args = g_list_append (args, g_file_new_for_commandline_arg (argv[i]));` (10 words, `:116`) | **admit** - the CLI's argument step is the source of the round-98 URI pre-processing and of the two refusal lines; tier A for the implementation source |
| S533 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c (HTTP 200, 100534 B, sha256 `65086c29...5e3771`); host package glib2 2.90.1-1 | 2026-11-07 | `Locates the first executable named @program in @path, in the same way that execvp() would locate it.` (17 words, `:274-276`) | **admit** - the one lookup the load gate, the terminal search and the post-prepend check all call; tier A |
| S534 | https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html (HTTP 200, 24174 B, sha256 `7bc0b640...5c03d9`) | 2026-11-07 | `If entry is of type Application, the working directory to run the program in.` (15 words, rendered `:128`) | **admit** - the documented `Path`/`Terminal`/`TryExec` contract the entry's section 11 measures the implementation against; tier A |

Every quote is a whitespace-collapsed line of the fetched bytes and is <= 25 words. S534's fetch is
this seat's own (`curl -sSL -o .ufo/waves/round-99/fetch/spec-terminal-path.html -w '%{http_code} %{url_effective}'`
printed `200 https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html`), and its
sha256 equals the L1's `spec-recognized-keys.html`, so the digest is confirmed by two independent fetches.

## 5. Candidates considered

| candidate | decision | reason | flip |
|---|---|---|---|
| the twelve-row `known_terminals` table as a model fact | **admit** | source at `gdesktopappinfo.c:2765-2778` and measured order/exec_arg (P01-P04) | a GLib tag or distribution patch that adds or reorders a row |
| `$TERMINAL` / `$COLORTERM` as an input to the terminal choice | **reject as a model fact** | `grep -c 'getenv ("TERMINAL")' gdesktopappinfo.c` = 0; the table is the whole choice (`:2797-2806`) | a GLib tag that consults the environment |
| `Program '<x>' not found in $PATH` as unreachable through `gio launch` | **reject** | reachable when `Exec` is empty (the load gate skips it at `:1974`) and the argument is not executable: P23 prints it, exit 1 | a load gate that checks an empty `Exec` |
| the empty-`Path=` inheritance as a source rule | **admit as a measurement only** | P07/P14/P15 measure it; the empty-vs-NULL decision is in `gspawn.c`, which this round did not open | a `gspawn.c` read that locates the test |
| the spec's `TryExec` "may be ignored" as the implementation's behaviour | **reject as a model fact** | `gdesktopappinfo.c:1947-1959` refuses the load; P12 measures the refusal | an implementation that ignores the entry |
| `Terminal=true` resolving the `Exec` program before the prepend | **reject as a model fact** | the prepend runs first (`:3027-3029`) and the post-prepend lookup only rewrites `argv[0]`; P19 records `TA1=probe.sh`, P22 shows the terminal's `exec` failing | a GLib tag that reorders the two steps |
| the spec's `Terminal` sentence as "runs in a terminal window" | **admit the observation, reject the mechanism** | the implementation prepends one of twelve names found on PATH; there is no terminal-window protocol in this path | a spec revision that names the table |

## 6. Entry frontmatter `source:` line (for the L1 to paste)

```
source: S532 (GLib 2.90.1 gio-tool-launch.c 16b4c8683b00407670f600eda0e65e9d929a59daac499cbe8f3d1fd532f6595a, 3991 B, 134 L), S533 (GLib 2.90.1 gutils.c 65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771, 100534 B, 3245 L), S534 (Desktop Entry Specification, recognized keys, https://specifications.freedesktop.org/desktop-entry/latest/recognized-keys.html 7bc0b6401cda9c019d5b89a2fab053d216eb937c83602df838a6c0a1175c03d9, 24174 B, HTTP 200), S528, S529, S531 (held rows, new scope)
```

The full frontmatter is already written in `drafts/gio-launch-env-r99.md`; it names all six rows with
their digests and locators.
