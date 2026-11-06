# R91MExecShell — round 91, wave w1 seat report

Seat: attack the C1 candidate's **program-lookup** and **desktop-file load** rules
(`shell_argv0` ≈ `g_shell_parse_argv`, `find_program` ≈ `g_find_program_for_path`, hand-parsed `Hidden`).
Base revision `cc0381db585cc44c3dfc13ced807409c32c45bb0`. All runs below are **DRAFT** (no measurement, nothing
written under `receipts/`).

## Result

- Wrote the seat's case set: **65 cases, ids `sh-01`…`sh-65`**, schema `mime-cases-r91-v1`, **unlabelled**,
  `controls/mime-cases-r91-sh.json` (sha256 `5ef70365e3412464c02b2a833d7806ee89aa96cb056a3a25dcf206e0e53e061b`).
  Families: `#`-comments 9, backslash/quoting 13, program/PATH lookup 13, Hidden booleans 8, keyfile structure 15,
  extra 7.
- **The DRAFT candidate disagrees with GLib on 15 of the 65 cases**, in **7 distinct root causes**, all inside
  `build/mado-mime.c1.py`: `shell_argv0` (:396-405), `find_program` (:381-394), `_is_exec_file` (:373-379),
  `_validate`'s Hidden line (:572). 50 cases agree (those are the loader rules the candidate does model correctly:
  duplicate-key last-wins, locale-suffixed keys, empty `Exec` skipped, empty argv[0], trailing-backslash error,
  invalid keyfile escape in `Path`/`TryExec`/`Exec` ⇒ the whole load fails, directory named like the program,
  non-executable file, dangling symlink, relative `Path` with relative PATH entries, absolute program).
- One further divergence (**F8**) cannot be expressed by the case schema (no FIFO node type); it is proven below by
  a hand-built fixture and is a schema/coverage gap for the L1.

## DRAFT runs (command → exit code)

| run | command | rc | output |
|---|---|---|---|
| oracle label | `controls/mime-oracle-r91.py --cases <sh-cases> --scratch-root … --label <copy>` | 0 | `MIME_ORACLE: cases=65 types=65 gio_sha256=d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462 libgio_sha256=b38001cca69b2890a22fd3f6590bea7392bf489009de7ddfb6dbf296a133685e changed=0` |
| oracle re-check | `… --check` on the labelled copy | 0 | `changed=0` (labels stable) |
| candidate self-test | `python3 build/mado-mime.c1.py --selftest` | 0 | `MADO_MIME_SELFTEST: checks=17 failed=0` |
| candidate vs GLib | counter-equivalent invocation (`python3 -I <copy> --json --config-home … --path … --desktop-unset -- <type>`, `cwd=<fixture>`, `env LC_ALL=C HOME=<fixture> PATH=/nonexistent`, under the counter's bwrap sandbox, tool bytes copied outside the lane) | 0 | `CASES=65 DISAGREE=15` |

`gio`/`libgio` sha256 are the declaration's pinned values, so the labels come from the pinned binaries.

## Findings

Reproducing input for every finding is a case in `controls/mime-cases-r91-sh.json` (materialise `files`, then
`env -i HOME=<root> XDG_CONFIG_HOME=<root>/cfg XDG_CONFIG_DIRS=<root>/etc XDG_DATA_HOME=<root>/home
XDG_DATA_DIRS=<root>/sys PATH=<root>/bin LC_ALL=C /usr/bin/gio mime text/x-sh-case`, `cwd=<root>`; the program
lookup uses `PATH=<root>/bin`, i.e. the case's `path` list).

### F1 `#` is a comment only after a space or a newline — shlex cuts at every unquoted `#`
GLib `glib/gshell.c:534-552`: `#` becomes a comment only if it is the first byte of the command line or the
**previous byte is `' '` or `'\n'`**; otherwise it is appended to the current token. The candidate
(`build/mado-mime.c1.py:401`, `lex.commenters = "#"`) makes shlex end the token at any `#` outside quotes.

- `sh-01-hash-midword-glib-token`: `Exec=sh#x`, `bin/sh#x` executable, `bin/sh` absent.
  gio: `Default application for “text/x-sh-case”: a.desktop` (+ both lists `a.desktop`);
  tool: `MADO_MIME: text/x-sh-case default=none registered=- recommended=-`.
- `sh-02-hash-midword-shlex-cuts`: same `Exec=sh#x`, `bin/sh` executable, `bin/sh#x` absent.
  gio: `No default applications for “text/x-sh-case”`; tool: `default=a.desktop registered=a.desktop recommended=a.desktop`.
- `sh-03-hash-after-quote`: `Exec='sh'#x` (previous byte is `'`), `bin/sh#x`.
  gio: default `a.desktop`; tool: `default=none`.

### F2 a tab before `#` does not comment in GLib
Same lines (`gshell.c:540-551`, the previous-byte set is `' '`, `'\n'`, `'\0'` — no tab). shlex treats a tab as
word-start, so it comments.

- `sh-04-hash-after-tab`: `Exec=\t#prog` (keyfile `\t` = a real tab), `bin/#prog` executable.
  gio: `Default application … : a.desktop`; tool: `default=none`.

### F3 backslash-newline outside quotes is deleted by GLib, kept by shlex
`glib/gshell.c:449-454` — `\<newline>` outside quotes appends nothing (line joining); shlex turns it into a literal
newline inside the token.

- `sh-10-backslash-newline-glue`: `Exec=sh\<LF>foo` (file text `Exec=sh\\\nfoo`), `bin/shfoo`.
  gio: `Default application … : a.desktop`; tool: `default=none`.
- `sh-11-backslash-newline-kept`: same `Exec`, `bin/sh<LF>foo`.
  gio: `No default applications …`; tool: `default=a.desktop`.

### F4 inside double quotes GLib unescapes `\$` and `` \` ``; shlex keeps the backslash
`glib/gshell.c:108-121` — in double quotes the escaped set is `"`, `\`, `` ` ``, `$`, newline.
Python shlex only unescapes `"` (and `\`), keeping `\$` / `` \` `` verbatim.

- `sh-12-dquote-dollar`: `Exec="\$x"` (file text `Exec="\\$x"`), `bin/$x`.
  gio: `Default application … : a.desktop`; tool: `default=none`.
- `sh-13-dquote-backtick`: `Exec="a\`b"` (file text `Exec="a\\`b"`), ``bin/a`b``.
  gio: default `a.desktop`; tool: `default=none`.

### F5 CR does not delimit a token for GLib
`glib/gshell.c:499-512` — the token delimiters are `'\n'`, `' '`, `'\t'` only; a CR (reached through the keyfile
escape `\r`) stays inside the token. shlex's whitespace set is `' \t\r\n'`, so it splits there.

- `sh-15-cr-in-exec`: `Exec=sh\r` (a real CR), `bin/sh`.
  gio: `No default applications for “text/x-sh-case”`; tool: `default=a.desktop registered=a.desktop recommended=a.desktop`.

### F6 `g_find_program_for_path` falls back to the PATH search when a name containing `/` is not found
`glib/gutils.c:329-378` (the "don't look in PATH" branch) falls through to `program = original_program;`
(`gutils.c:368`) and the PATH loop (`gutils.c:462-520`) if the direct check fails for a **relative** name; the loop
prefixes each PATH element with the original name, so `PATH=bin`, `program=tools/prog` probes `bin/tools/prog`.
The candidate (`build/mado-mime.c1.py:383-385`) returns `False` immediately and never searches PATH.

- `sh-23-relative-slash-path-fallback`: `Exec=tools/prog`, `bin/tools/prog` executable.
  gio: `Default application … : a.desktop`; tool: `default=none`.
- `sh-24-dot-slash-path-fallback`: `Exec=./prog`, `bin/prog`, nothing at `<cwd>/./prog`.
  gio: default `a.desktop`; tool: `default=none`.
- `sh-31-tryexec-relative-slash`: `TryExec=tools/prog`, `Exec=sh`, `bin/tools/prog`, `bin/sh`.
  gio: default `a.desktop`; tool: `default=none`. (Same call site: `gio/gdesktopappinfo.c:1951`.)

### F7 `Hidden` trims GLib's G_ASCII_SPACE set, not Python whitespace
`glib/gkeyfile.c:4979-5004` (`g_key_file_parse_value_as_boolean`): the compared length ends at the last character
that is **not** `g_ascii_isspace`, and `g_ascii_isspace` uses `glib/gstrfuncs.c:262-279` (`ascii_table_data`), where
`0x0b` (\v) carries `0x004` — **no** space bit — while `0x0c` (\f) carries `0x104` (space bit). Non-ASCII bytes
never match. The candidate (`build/mado-mime.c1.py:572`) uses `str.strip()`, which also removes \v, \x1c-\x1f and
Unicode spaces. Every such value is a boolean error in GLib ⇒ *not hidden*; the candidate makes the app hidden and
drops it from the printed lists (the default is still accepted, as both agree).

- `sh-36-hidden-fs-char`: `Hidden=true\x1c`. gio: registered/recommended `["a.desktop"]`;
  tool: `default=a.desktop registered=- recommended=-`.
- `sh-37-hidden-nbsp`: `Hidden=true\u00a0`. gio: lists `["a.desktop"]`; tool: `registered=- recommended=-`.
- `sh-38-hidden-vt`: `Hidden=true\x0b`. gio: lists `["a.desktop"]`; tool: `registered=- recommended=-`.
- Control `sh-65-hidden-formfeed`: `Hidden=true\x0c` → both hidden (agree), which pins the boundary to the
  ASCII table row rather than "non-ASCII".

### F8 (out of schema) a non-regular executable file is a program for GLib
`glib/gfileutils.c:428` — `G_FILE_TEST_IS_EXECUTABLE` is `access(filename, X_OK) == 0`; `glib/gutils.c:339-340` and
`:486-487` add only `!G_FILE_TEST_IS_DIR`. A FIFO with mode 0755 therefore matches. The candidate
(`build/mado-mime.c1.py:373-379`) requires `S_ISREG`.
Hand-built fixture (no schema node type can express a FIFO — the oracle only writes regular files, dirs and
symlinks): `bin/prog` = `mkfifo` + `chmod 755`, `Exec=prog`, `mimeinfo.cache` addition.

```
$ env -i HOME=$R XDG_CONFIG_HOME=$R/cfg XDG_CONFIG_DIRS=$R/etc XDG_DATA_HOME=$R/home \
    XDG_DATA_DIRS=$R/sys PATH=$R/bin LC_ALL=C /usr/bin/gio mime text/x-sh-fifo      # cwd=$R
Default application for “text/x-sh-fifo”: a.desktop
Registered applications:
	a.desktop
Recommended applications:
	a.desktop
$ python3 -I <candidate> … --path $R/bin --desktop-unset -- text/x-sh-fifo
MADO_MIME: text/x-sh-fifo default=none registered=- recommended=-
```
Recommendation for the L1: add a `{"fifo": true}` (or `{"mode": …}`) node type to `mime-cases-r91-v1`, otherwise
this class stays unlabelled; alternatively accept it as a named limit of the candidate.

## Suggested candidate fixes (not applied — outside this seat's write scope)

1. Port `tokenize_command_line` + `g_shell_unquote` (gshell.c:434-620 and 65-180) instead of shlex: `#` by previous
   byte, delimiters `\n`/space/tab only, `\`+newline dropped, double-quote escapes `" \ ` $` + newline.
2. `find_program`: after a `/`-bearing relative name fails the direct check, continue into the PATH search with the
   original name instead of returning `False`.
3. `_is_exec_file`: `os.access(p, os.X_OK) and not os.path.isdir(p)` (drop `S_ISREG`).
4. `Hidden`: strip only `" \t\n\f\r"` from the right of the raw value, compare to `true`/`1` exactly.

## Dead steps and limits

- First oracle run died: `MIME_ORACLE: SETUP_ERROR 'text'` (rc 2) — a `files` value of `{"exec": true}` alone is
  invalid; the schema needs `{"text": …, "exec": true}` (oracle docstring). Fixed in the generator; no case uses
  the bare form.
- An **unset** `PATH` cannot be labelled: the oracle always sets `PATH` from the case's `path` list (empty list ⇒
  `PATH=""` ⇒ current directory), so the `g_getenv("PATH") == NULL` default `"/bin:/usr/bin:."`
  (`glib/gutils.c:388`) is out of reach of this case set.
- A truly **empty** PATH element is not expressible either: `abspaths` rewrites `""` to `<root>/`
  (`controls/mime-oracle-r91.py`, `abspaths`), which happens to be equivalent only because the oracle runs with
  `cwd=<root>`; `sh-29-empty-path-element` therefore tests the root-directory element, not `"."`.
- The counter was not run: my cases are not merged into the frozen set and the counter needs the frozen
  cases/mutants pins. No receipt written.
- Installed: nothing.

## Files written

- `.ufo/waves/round-91/controls/mime-cases-r91-sh.json` (65 unlabelled `sh-` cases; L1 relabels).
- `.ufo/waves/round-91/w1/R91MExecShell.md` (this report).

Scratch `$HYAKU_SCRATCH/mado-r91/R91MExecShell` (default `/fast/scratch/hyaku/...`) is removed on exit; nothing
cited above depends on it (fixtures are reproducible from the case file).
