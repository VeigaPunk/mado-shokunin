# ExecRefB — C1 reference implementation B: `tools/mado-terminal.py`

Status: DONE. Lane repo `mado-shokunin`, wave w1 (BUILD), round 47.

Seat scope: an independent (B) implementation of the C1 capability tool, written from
`/usr/bin/xdg-terminal-exec` alone (no sibling seat's files were read), plus the comparison
corpus against the pinned script. Deliverables are staged inside the seat directory; the L1 is
the only integrator, so nothing outside
`.ufo/waves/round-47/w1/ExecRefB/` was written.

## 1. Files

| file | role |
|---|---|
| `.ufo/waves/round-47/w1/ExecRefB/mado-terminal.py` | the tool (Python 3 stdlib only, no process, no socket, no writes) |
| `.ufo/waves/round-47/w1/ExecRefB/compare.py` | agreement harness: materialises fixtures, runs the pinned script and the tool side by side, writes `receipts/` |
| `.ufo/waves/round-47/w1/ExecRefB/derive-help.py` | one-shot derivation of the embedded `--help` bytes (provenance for the only non-hand-written constant) |
| `.ufo/waves/round-47/w1/ExecRefB/probe-shell-semantics.sh` | measures the `/bin/sh` semantics the model depends on (re-runnable) |
| `.ufo/waves/round-47/w1/ExecRefB/verify-quotes.py` | checks every §4 quote against both the cited script line and the report |
| `.ufo/waves/round-47/w1/ExecRefB/receipts/agree.txt` | 208-case comparison receipt + tripwire lines |
| `.ufo/waves/round-47/w1/ExecRefB/receipts/cases.json` | the same 208 cases in the frozen fixture schema, `expect` produced by the real script |
| `.ufo/waves/round-47/w1/ExecRefB/receipts/selftest.txt`, `probes.txt`, `host-*.txt`, `quotes.tsv`, `quotes-check.txt`, `digests.txt` | supporting evidence |

Pin under study: `/usr/bin/xdg-terminal-exec`, sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (the harness refuses to run
against any other digest), 1499 lines, `#!/bin/sh` → `/usr/bin/bash 5.3.20(1)-release`.

## 2. Contract as implemented

* `mado-terminal.py print [args]` — resolves the entry exactly as the program does in the
  current environment and reproduces stdout bytes + exit status for
  `--print-id`, `--print-path`, `--print-content`, `--print-cmd[=seq]`,
  `--print-delimiter=seq`, `--test`, `-h`/`--help`, `--app-id=`, `--title=`, `--dir=`,
  `--hold`, `--`, `-e`, unknown options and any command words. Cache is modelled **cold**
  (the contract's `<empty dir>`), so `read_cache`/`save_cache` never influence the answer.
  With no print/`--test` mode the program would `exec` a terminal; the tool refuses
  (`rc=2`, stderr) instead of ever launching one — the launch path is the one case the
  contract cannot compare.
* `mado-terminal.py explain [--observed FILE]` — a trace then a verdict line
  `MADO_TERM: selected=<id> path=<path> verdict=OK|AGREE|DIFFER|NO_TERMINAL`, plus
  `SUMMARY tried= rejected= reasons=<code:count,...>`. Exit 0 for OK/AGREE, 1 for DIFFER,
  3 for NO_TERMINAL, 2 for usage. Rejection codes: `not-found`,
  `not-terminal-emulator`, `no-exec`, `exec-not-on-path`, `tryexec-not-on-path`,
  `hidden`, `show-in-mismatch`, `action-not-listed`, `strict-mode-no-terminalarg-exec`,
  `unreadable-file`, `desktop-file-tail`. `Type=`/`NoDisplay=` are **never** rejection
  reasons (the program does not read them) — when present they are reported as
  `NOTE unread-keys=...`.
* `mado-terminal.py --selftest` — 55 hermetic cases built under `$TMPDIR` (no process, no
  socket, no `/tmp`): `MADO_TERMINAL_SELFTEST: 55/55 passed`.

### Live host answer (read-only, no process, no socket)

`explain` on this host (`receipts/host-explain.txt`): `XDG_CURRENT_DESKTOP='Hyprland'` →
lowercased `hyprland` only for list *filenames*; config chain `/home/vgpnk/.config/
hyprland-xdg-terminals.list` (absent), `/home/vgpnk/.config/xdg-terminals.list` (present),
`/etc/xdg/...` (absent), `/usr/local/share/xdg-terminal-exec/...` (absent),
`/usr/share/xdg-terminal-exec/xdg-terminals.list` (present, contains the exclusions and the
`/execarg_default` table); 184 entries registered, 182 fallback ids; candidate
`Alacritty.desktop` from `/home/vgpnk/.config/xdg-terminals.list:3` accepted; the desktop file
resolved to the **user override** `/home/vgpnk/.local/share/applications/Alacritty.desktop`
(last found wins over `/usr/share/applications`), `command=['alacritty']`, `execarg='-e'`,
`dir='--working-directory='`, `title='--title='`, `app-id='--class='`.
`explain --observed` against a cold-cache capture of
`xdg-terminal-exec --print-id --print-path --print-cmd` prints `verdict=AGREE`
(`receipts/host-explain-observed.txt`). `print --dir=/home/vgpnk` (the hotkey shape, no print
option) exits 2 and launches nothing.

## 3. Evidence (exact)

* `receipts/agree.txt`: `COMPARISON: 208/208 agree on stdout bytes and exit status`
  — 108 pinned + 100 nonce cases (seed 47); every case also passed the explain/observed check
  (`explain=agree/0`) and the no-write check (`nowrite=ok`). The same 208/208 holds for
  nonce seeds 1 and 999 (three seeds × 70 nonce cases, run during development; the receipt is
  the seed-47 run).
* `TRIPWIRE print: rc=0 execve=1 sockets=0 stdout_ok=True` and
  `TRIPWIRE explain: rc=0 execve=1 sockets=0` — under `strace -f -e trace=execve,socket,connect`
  the only `execve` is the interpreter itself; zero socket/connect syscalls. "execve=1" is the
  python3 start, not a child.
* `receipts/selftest.txt`: `MADO_TERMINAL_SELFTEST: 55/55 passed`.
* `receipts/probes.txt`: the measured shell semantics (`/bin/sh` = bash 5.3) that the model
  encodes; each numbered section is cited in §4.
* `receipts/host-observed.txt` (84 bytes, three lines: `Alacritty.desktop`,
  `/home/vgpnk/.local/share/applications/Alacritty.desktop`, `alacritty`) —
  produced with `XDG_CACHE_HOME` pointed at an empty scratch directory, print mode only.
* `/home/vgpnk/.cache/xdg-terminal-exec` was not written by any of these runs (mtime
  17:42 −0300, before this seat started; every child env was built from scratch with
  `XDG_CACHE_HOME=$ROOT/cache`).
* `receipts/quotes-check.txt`: `QUOTES: 32/32 verified (locator and report)` — every
  fragment quoted in §4 is present at the cited line of the pinned script *and* in this
  report (the table is `receipts/quotes.tsv`, the checker `verify-quotes.py`).
* Artifact digests (sha256): tool `0f11b15059c030909dfe734ee565e6e301b4da2992b8ec18fbc659efedfff89d`,
  harness `e0261ac265bc1b946caa8f02a7ba8b90fbde64d98e43b479ca7390d0f4e857fb`,
  `receipts/agree.txt` `9c721ab5568ec9900f5f6cb48a9a3fd32096083d9730ea203cad4ade369c1eb8`,
  `receipts/cases.json` `35400309caacabbaf1ac1b45b3b0a9c526bd77e5c64c2639522a999a3b317f26`.
* No tool installs were needed (`strace`, `bwrap`, `python3` already present); no pacman.

## 4. Surprising behaviour found in v0.14.3 (these are the fixtures)

Each row: what the program really does, where, and the case in `receipts/cases.json` that
pins it. Locators are `grep -n` output on the pinned script and are machine-checked by
`receipts/quotes.tsv` + `verify-quotes.py` (see `receipts/quotes-check.txt`).

1. **A bad `%` field does not reject the entry.** `check_entry_key` calls
   `de_strip_fields` (xdg-terminal-exec:960) and ignores its status; only
   `command -v "$XTE__EXEC0" > /dev/null || return 1` (xdg-terminal-exec:964) can reject.
   So `Exec=term %f %U` (two file fields), `Exec=term %Z` and `Exec=term %` are all
   **accepted with the raw tokens kept**, and `--print-cmd` prints `%f`, `%U`, `%Z`, `%`
   literally. Cases: `exec-two-file-fields`, `exec-unknown-field`, `exec-trailing-percent`.
   (`Encountered more than one %[fFuU] field!` at xdg-terminal-exec:708 and
   `unknown % field in argument` at xdg-terminal-exec:729 are debug-only.)
2. **`-type f` applies to only one data directory.** The find expression is
   `set -- "$@" -type f` (xdg-terminal-exec:766) followed by per-directory
   `( -path "$xte__directory"'./[a-zA-Z0-9_]*.desktop' ... )` groups joined with `-o`
   (xdg-terminal-exec:773); implicit `-a` binds tighter than `-o`, so only the **first**
   (lowest-preference) group keeps the type test. A directory named `X.desktop` under
   `$XDG_DATA_HOME` or `$XDG_DATA_DIRS[1]` is therefore registered as an entry and, being
   found later, overwrites the alias of a real file of the same ID → NO_TERMINAL.
   Cases: `directory-shadows-file` (probe §8/§9 in `receipts/probes.txt`).
3. **Duplicate IDs are won by the user directory, not the system one.** Registration is
   `alias "$xte__entry_id"="xte__entry_path='$xte__entry_path'"` (xdg-terminal-exec:782) in
   find order (lowest preference first), and the fallback list is *prepended*
   (`${XTE__FALLBACK_ENTRY_IDS:+${XTE__LF}${XTE__FALLBACK_ENTRY_IDS}}`,
   xdg-terminal-exec:790), so the last-found (highest-preference) file both wins the alias
   and is tried first. Cases: `duplicate-user-wins`, `duplicate-all-dirs`, `readdir-order`.
4. **Selection state leaks between candidates.** `reset_keys` (xdg-terminal-exec:999) runs
   only when a *key check* fails; the three `continue` paths in `find_entry`
   (`[ -z "${XTE__EXEC_USEP}" ] && continue` xdg-terminal-exec:1088,
   `[ -z "${XTE__IS_TERMINAL}" ] && continue` xdg-terminal-exec:1090, and the strict-mode
   `continue` under `if [ "$XTE__EXECARG_DEFINED" != "true" ]; then`
   xdg-terminal-exec:1092) leave `IS_TERMINAL`, `EXEC_USEP`, `EXECARG` and
   `EXECARG_DEFINED` in place; in compat mode the missing ExecArg is filled from
   `get_default_execarg "$xte__entry_id"` (xdg-terminal-exec:1095). A `Categories`-less
   entry can therefore be selected just because the *previous* candidate was a
   TerminalEmulator. Cases: `state-leak`, `skipped-group-header-tail`.
5. **A desktop file's last line may be silently dropped.** Every reader is `while read`; a
   file whose final line has no `\n` never enters the loop body (probe §2). An entry ending
   `Exec=term` without a newline has no Exec at all. Cases: `no-trailing-newline`.
6. **`read_entry_path` returns the status of the last command its loop ran.** The
   `'[Desktop Entry]'*) [ -z "$xte__entry_action" ] && xte__read_exec=true ;;` arm
   (xdg-terminal-exec:989) and `'['*) [ "$xte__read_exec" = "true" ] && break ;;`
   (xdg-terminal-exec:1014) are non-zero when their test fails, so a file that ends on a
   skipped group header discards the entry (probe §4). Case: `skipped-group-header-tail`.
7. **`command -v` can be satisfied by the script's own shell functions, builtins, keywords
   and its live aliases.** `TryExec=printf`, `TryExec=find_entry` and `TryExec=shcat` all
   pass; a directory or non-executable file on PATH does not (probe §5). Cases:
   `tryexec-present`, `tryexec-dot-path`, and the nonce corpus.
8. **`Hidden` only matches the literal lowercase `true`** (`'Hidden'*=*` xdg-terminal-exec:938);
   `Hidden=True` and `Hidden=1` are accepted. Cases: `hidden-true`, `hidden-True`, `hidden-one`.
9. **Categories are matched as exact `;`-tokens** (`[ "$xte__category" = "TerminalEmulator" ] && {`
   xdg-terminal-exec:821): `TerminalEmulatorX` does not count, `;;` empties are harmless.
   Cases: `categories-substring`, `categories-other-only`.
10. **Show-in rules are skipped for explicitly listed IDs and applied to fallback IDs**
    (`xte__de_checks=false` xdg-terminal-exec:1058, flipped by `xte__de_checks=true` at the
    `//fallback_start//` marker, xdg-terminal-exec:1072). Cases: `onlyshowin-explicit-ignored`,
    `onlyshowin-fallback-mismatch`, `notshowin-fallback-match`, `no-desktop-variable`.
11. **`XDG_CURRENT_DESKTOP` is lowercased only for list filenames**
    (`XTE__LOWERCASE_XDG_CURRENT_DESKTOP=$(printf '%s' "${XDG_CURRENT_DESKTOP-}" | tr ...`,
    xdg-terminal-exec:1144); `OnlyShowIn` compares the raw value, so
    `XDG_CURRENT_DESKTOP=HYPRLAND` + `OnlyShowIn=Hyprland` is a mismatch. And `tr` leaves
    non-ASCII uppercase alone even under `LANG=en_US.UTF-8` (probe §10). Cases:
    `uppercase-desktop-list`, `uppercase-desktop-showin`, `case-differs-showin`.
12. **`--print-cmd`'s default word separator is a newline**, not a space
    (`printf '%b' "${XTE__PRINT_CMD_DELIMITER:-\n}"` xdg-terminal-exec:1480): `--print-cmd`
    alone prints one argument per line. Cases: `print-id-path-cmd`, `print-cmd-args`.
13. **The trailing newline rule is string equality with the two characters `\n`**
    (`'\n') printf '%b' '\n' ;;` xdg-terminal-exec:1381): a literal newline or `\t`
    delimiter does *not* get the extra newline. Cases: `print-delimiters`,
    `print-cmd-comma`, `print-delimiter-tab`, `print-delimiter-raw-newline`.
14. **Print blocks are executed in a fixed order (id, path, content, cmd) regardless of the
    option order**, because each block tests membership in `$XTE__PRINT_DATA`
    (`printf '%s' "${XTE__ENTRY_ID}${XTE__ENTRY_ACTION:+:}${XTE__ENTRY_ACTION}"`,
    xdg-terminal-exec:1331). `--test` is ignored when any print option is present.
    Cases: `print-order-reversed`, `print-cmd-then-test`.
15. **Option values are parsed with `read`**, so a value containing a literal newline is
    truncated at it, and a lone trailing `=` is dropped (`--dir=a=` → `a`, but `--dir=a==` →
    `a==`; probe §7). `--print-delimiter=<LF>` therefore behaves like an empty delimiter.
    Case: `print-delimiter-raw-newline`.
16. **A malformed `Exec` still yields a usable command.** On an unquoted special
    (`Encountered unquoted character` xdg-terminal-exec:623), an unclosed quote
    (`xte__tok_quoted=1` xdg-terminal-exec:617) or a dangling backslash, the tokenizer
    returns what it has; the Exec arm continues with those partial tokens. `Exec=term "open`
    selects the entry and prints `term open`. Cases: `exec-unclosed-quote`,
    `exec-unquoted-semicolon`, `exec-tilde`, `exec-escaped-quote`.
17. **Unsupported backslash escapes lose only the backslash**: the commented-out
    `# unsupported sequence, reappend backslash` branch (xdg-terminal-exec:552) means `\q`
    → `q` and a trailing `\` disappears. `%%` becomes `%` before the unknown-field test.
    Cases: `exec-escapes`, `exec-backslash-unknown`, `exec-percent-literal`.
18. **`--print-cmd` writes the resolver cache (background) and `read_cache` can answer
    instead of the filesystem.** `save_cache "$1" &` (xdg-terminal-exec:1457) forks before
    printing; `read_cache` bails out at `xte__line_limit=50` (xdg-terminal-exec:223). The
    tool models a cold cache, which is what the contract specifies; a warm-cache comparison
    is out of scope and must not be used as evidence.
19. **A config line's trailing `:` yields an action-less entry**, and `--` / unknown options
    are consumed before the first non-option word; `-e` (or the entry's own ExecArg) ends
    option processing (`IFS=':' read -r xte__entry_id xte__action_id`
    xdg-terminal-exec:436; `IFS='=' read -r _opt XTE__TITLEVAL` xdg-terminal-exec:1246).
    Cases: `invalid-action-id`, `exec-dash-e-option`, `print-unknown-option`,
    `print-after-dashdash-help`.

## 5. Model boundary and risks

* **Externals are modelled, not run.** The program's discovery pipeline is
  `while IFS= read -r xte__entry_path && IFS= read -r xte__entry_id; do`
  (xdg-terminal-exec:779) over `LC_ALL=C find -L "$@" 2> /dev/null |` (xdg-terminal-exec:795);
  the model replaces `find -L` with a readdir pre-order walker and `-path`-equivalent globs,
  `awk`'s ID derivation by `rfind('/./')` + `/`→`-`, and `tr`'s lowercasing by an ASCII table. If a fixture shadows `find`/`awk`/`tr` with a stub in
  `$ROOT/bin`, the real script would run the stub and the model would diverge — such fixtures
  are out of scope for the C1 comparison (my harness only ever symlinks the real helpers into
  a tool bin). Absence is modelled: no `tr` → exit 1 before parsing; no `find`/`awk` → no
  entries → exit 1.
* **Cache is modelled cold.** Any fixture that seeds `XDG_CACHE_HOME` makes the real script
  read its own md5 cache; the tool ignores it. The counter must keep `XDG_CACHE_HOME` empty
  and fresh per run (the cache key is `ls -LRl`, i.e. size+mtime only).
* **Special files**: a FIFO named `*.desktop` makes the real resolver block on `open()`
  (reported by another seat; not reproduced here). The model treats it as an unreadable
  entry. No fixture of mine contains one.
* **`printf %b`** is implemented for `\\ \a \b \c \e \f \n \r \t \v \0nnn \xHH` with >0xFF
  masking; a delimiter relying on other GNU extensions is not covered.
* **Exit status of the abort paths**: an unset `HOME` (only when a default is actually
  needed) and a missing `tr` produce exit 1 with no stdout, matching `set -e`; the stderr
  text differs by design (the contract fixes stdout + status only).
* The embedded `--help` bytes are captured from the pinned invocation, so the modelled `$0`
  basename is `xdg-terminal-exec`; renaming the script would change only that word.

## 6. Scratch

All work ran under `/fast/scratch/hyaku/mado-r47/ExecRefB/` (harness trees, strace logs,
intermediate receipts); it was deleted after the receipts were copied here. Nothing was
written outside this seat directory.
