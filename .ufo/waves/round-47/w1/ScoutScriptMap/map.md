# ScoutScriptMap: /usr/bin/xdg-terminal-exec v0.14.3, function and selection-step map

Round 47, wave w1 (BUILD). Scout seat, read-only. Every line number below is a `grep -n` /
`read` line number of `/usr/bin/xdg-terminal-exec` (1499 lines). `verify-anchors.txt` in this
directory is the receipt of a script that re-greps each cited (line, snippet) pair against the file.

## 0. Host file == upstream tag (verified)

| file | sha256 |
|---|---|
| /usr/bin/xdg-terminal-exec | 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac |
| upstream-xdg-terminal-exec (fetched from https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec) | 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac |

Equal (`sha256.txt`, `upstream-xdg-terminal-exec` in this seat dir). Interpreter: `#!/bin/sh` (line 1);
host `/bin/sh -> bash`, GNU bash 5.3.20 (POSIX mode when invoked as sh). Behaviour claims marked
**[PROBED]** were observed by running the real script with a `--print-*`/`--test`/`-h` option only,
`XDG_CACHE_HOME` inside scratch, fixture `$ROOT` trees (harness and outputs in `probes/`; case list in section 9).
Claims without the tag are read from the source.

## 1. Function map (ranges from `awk` over `^name() {` .. `^}`)

Option-dependent reach: "ALL" = every run that gets past `find_entry` (id/path/content/cmd/--test/launch).
`read_cache` is tried in ALL modes when cache enabled; a cold cache (the contract) always returns 1.

| function | lines | reads | decides / writes | reached by |
|---|---|---|---|---|
| error | 45-48 | args | printf to stderr | ALL (stderr only) |
| check_bool | 50-59 | $1 | true/True/TRUE/yes/Yes/YES/1 -> 0; false/False/FALSE/no/No/NO/0 -> 1; anything else: stderr `Assuming '$1' means no`, return 1 | 61, 403, 1094, 1179, 302, 1393, 1396 |
| (top-level) debug definition | 61-75 | XTE_DEBUG, DEBUG | defines `debug` as stderr printer or no-op; never touches stdout | ALL |
| shcat | 77-82 | stdin | builtin cat (`read -r` loop, adds trailing newline to a final line without one) | help (91), --print-content (1362) |
| usage | 84-89 | XTE__SELF_NAME | text | help |
| help | 91-141 | `$0` basename | prints help text | `-h`/`--help` before `--` (1133-1141) -> exit 0 |
| make_paths | 143-177 | XDG_CONFIG_HOME, HOME, XDG_CONFIG_DIRS, XDG_DATA_DIRS, XDG_DATA_HOME, XDG_CACHE_HOME, XTE__LOWERCASE_XDG_CURRENT_DESKTOP | builds XTE__CONFIGS (colon list, preference order) and XTE__APPLICATIONS_DIRS (ASCENDING preference), cache file path | ALL (1167) |
| gen_hash | 179-215 | LC_ALL, XDG_CURRENT_DESKTOP, listing of config+data dirs | md5 of `ls -LRl`; re-calls itself with LC_ALL=C | read_cache (272, only if a cache file parsed), save_cache (305) |
| read_cache | 217-298 | cache file | returns 0 only if hash matches and cached cmd on PATH | ALL when XTE__CACHE_ENABLED true (1179); cold: line 221 false -> 296 |
| save_cache | 300-340 | cache state | writes or removes cache file; forked with `&` | only past 1455: --print-cmd, --test, launch. NOT --print-id/--print-path/--print-content |
| list_contains | 342-349 | LF-list, item | membership | read_config_paths (446-458), find_entry_paths (785) |
| read_config_paths | 351-475 | XTE__CONFIGS files | fills XTE__ENTRY_IDS, XTE__INCLUDED/EXCLUDED_ENTRY_IDS, XTE__EXECARG_DEFAULTS, cache/compat directive flags | ALL cold (1198) |
| replace | 477-499 | $1 $2 $3 | substring replace into XTE__REPLACED_STR | de_strip_fields (722) |
| de_expand_str | 501-559 | $1 | expands `\s \n \t \r \\`; any other `\x` loses the backslash (the unsupported-sequence arm is commented out, 552-556) | check_entry_key: Exec (956), TryExec (934), TerminalArg* (888-930) |
| de_tokenize_exec | 561-692 | $1 | Exec to USEP-joined argv, errors return 1 on unquoted special chars, unescaped `$`/backtick in quotes, dangling backslash, unclosed quote | Exec line (958) |
| de_strip_fields | 694-740 | XTE__EXEC_USEP | drops `%f %F %u %U` (second one -> return 1), `%d %D %n %N %v %m`, `%i %c`; `%%`->`%`; other `%?` -> return 1 | Exec line (960) |
| reset_keys | 742-752 | - | clears IS_TERMINAL, EXEC_USEP, sets EXECARG=-e, EXECARG_DEFINED=false, APPID/TITLE/DIR/HOLD args empty | start (1164) and ONLY on a failed key (999) |
| find_entry_paths | 754-800 | XTE__APPLICATIONS_DIRS, XTE__EXCLUDED_ENTRY_IDS | `find -L` + awk, one `alias <ID>=xte__entry_path='<path>'` per file (later = higher preference overwrites), fills XTE__FALLBACK_ENTRY_IDS | ALL cold (1200) |
| check_entry_key | 802-968 | one `Key=Value` line + action + read_exec + de_checks | per-key accept/reject, see section 5 | read_entry_path (997) |
| read_entry_path | 970-1018 | one desktop file | line walk with group handling, see section 5 | find_entry (1086) |
| validate_entry_id | 1020-1037 | $1 | charset [a-zA-Z0-9_.-], non-empty, not `.desktop`, must end `.desktop` | read_config_paths (410, 439) |
| validate_action_id | 1039-1053 | $1 | empty ok, else [a-zA-Z0-9-]+ | read_config_paths (439) |
| find_entry | 1055-1111 | ENTRY_IDS + `//fallback_start//` + FALLBACK_ENTRY_IDS | first valid entry wins; sets ENTRY_PATH/ID/ACTION | ALL cold (1208) |
| get_default_execarg | 1113-1130 | XTE__EXECARG_DEFAULTS | `/execarg_default` override or `-e` | find_entry (1095) |
| main | 1132-1499 | argv | everything else, see section 2 | - |

## 2. Main flow of `--print-id` (cold cache), in execution order

1. 23 `set -euf` (errexit, nounset, noglob). 26 OIFS, 28 LF, 32 SELF_NAME=`${0##*/}`.
2. 37-43 RSEP/USEP/CR obtained from `printf '%b\n'` in a `$(...)` subshell + three `read -r` (builtins only).
3. 45-141: defines error, check_bool; 61 `check_bool "${XTE_DEBUG-${DEBUG-0}}"` selects real/no-op `debug` (64-71 / 74); defines shcat..help; 143-1130 remaining function definitions. No selection code runs yet.
4. 1133-1141 scans ALL args until a literal `--`: any `-h`/`--help` (even after a command word or after `-e`) prints help, exit 0. `foo -h` -> help [PROBED]; `-- -h` -> not help [PROBED].
5. 1144 `XTE__LOWERCASE_XDG_CURRENT_DESKTOP=$(printf ... | tr '[:upper:]' '[:lower:]')`.
6. 1147-1149 compat vars from XTE_EXECARG_COMPAT (default true; CONFIGURED non-empty if env var set). 1151-1161 empty globals. 1164 `reset_keys`.
7. 1167 `make_paths` (143-177): config list = for each of [XDG_CONFIG_HOME or $HOME/.config] + [XDG_CONFIG_DIRS or /etc/xdg]: for each lowercased desktop word `<dir>/<word>-xdg-terminals.list` then `<dir>/xdg-terminals.list` (148-154); then for each of XDG_DATA_DIRS (default /usr/local/share:/usr/share) the same under `<dir>/xdg-terminal-exec/` (157-163). So order: config home, config dirs, data dirs; within one dir desktop-specific before generic. Applications dirs: each of [XDG_DATA_HOME or $HOME/.local/share] + [XDG_DATA_DIRS] gets `/applications/` and is PREPENDED (166-169), giving ascending preference (last data dir ... data home). Trailing `/` of each base dir is stripped once. Cache path `${XDG_CACHE_HOME:-$HOME/.cache}/xdg-terminal-exec` (172-173).
8. 1172-1177 cache flags (XTE_CACHE_ENABLED, default true), XTE__HASH empty.
9. 1179 `check_bool true && read_cache`: cold = no file (221) -> `return 1` (296) -> else branch 1182.
10. 1183-1195 init XTE__CACHE_USED=false, ENTRY_IDS, FALLBACK_ENTRY_IDS, EXCLUDED, INCLUDED (empty).
11. 1198 `read_config_paths` (351-475): file by file in XTE__CONFIGS order (361), missing file skipped (365), every line trimmed by `read -r` (367), directives and ids per section 4. Entire set of files is read before any entry is looked at.
12. 1200 `find_entry_paths` (754-800): registers every `*.desktop` under all applications dirs (section 6).
13. 1208 `find_entry || exit 1` (1055-1111): iterate `ENTRY_IDS`, `//fallback_start//`, `FALLBACK_ENTRY_IDS` (1060): per id, alias lookup (1081), eval (1083), unalias (1085), `read_entry_path` (1086), then empty Exec -> skip (1088), not terminal -> skip (1090), no TerminalArgExec: compat -> default execarg (1094-1096), strict -> skip (1099); accept sets PATH/ID/ACTION (1103-1106). No candidate -> stderr message and return 1 (1109-1110) -> exit 1.
14. 1216-1223 option variable init. 1224-1322 option loop (section 3).
15. 1327-1335 `--print-id`: `printf '%s' "${ID}${ACTION:+:}${ACTION}"` (1331), no newline yet.
16. 1336-1353 `--print-path` (only if requested), 1354-1366 `--print-content` (only if requested).
17. 1369-1385 early bail: id/path/content only. Content present -> `exit 0` at 1376 with no extra newline; otherwise `\n` appended only if the delimiter text is literally `\n` (1380-1381), `exit 0` at 1383. So `--print-id` alone prints `<id>[:action]\n`, rc 0 and never reaches `save_cache` (1455) [PROBED: no cache file written].
18. Not reached by `--print-id` alone: 1388-1498 (argument composition, save_cache, --test, --print-cmd, cd, exec).

## 3. Option loop (1224-1322), arguments left in `$@`

First matching arm per argument, in this order: `--` (consume, stop, 1226); `-e` or text equal to the ENTRY's execarg (consume, stop, 1231); `--app-id=*` / `--title=*` / `--dir=*` (value = text after the first `=` via `IFS='=' read -r`, so only the FIRST LINE of a multi-line value survives, 1236-1259); `--hold`; `--test`; `--print-path`; `--print-id`; `--print-content`; `--print-cmd` (default cmd delimiter `\n`); `--print-cmd=*` (delimiter = rest after first `=`, may be empty, 1296-1304); `--print-delimiter=*` (1305-1312); `[!-]*` first non-option, stop WITHOUT consuming (1313); `-*` unknown option, discarded (1317). An empty-string argument matches NO arm and is not shifted: infinite loop, no output [PROBED, timeout]. Exception: an entry whose TerminalArgExec is empty matches `"$XTE__EXECARG"` and consumes it. Note the arm `-e | "$XTE__EXECARG"` precedes all `--print-*` arms: an entry TerminalArgExec equal to e.g. `--print-id` would swallow it (inference from arm order).

## 4. Config list files (351-475), exact line grammar

- Per file, per line (after `read -r` trims leading/trailing IFS whitespace: space, tab, newline; a CR is NOT trimmed): `/enable_cache`, `/disable_cache` (first one wins, only affect cache save: 374-385), `/execarg_compat`, `/execarg_strict` (first wins, ignored if XTE_EXECARG_COMPAT is set in env: 388-399), `/execarg_default:<id>:<value>` (only while compat true: 402-415; first mention of an id wins via get_default_execarg 1117-1124), `[a-zA-Z0-9_]*` or `[+-][a-zA-Z0-9_]*` (425), everything else silently ignored (comments, blank, unknown `/x`).
- Id line: optional `+`/`-`, then `IFS=':' read -r id action` (436): split at the first `:`, remainder is the action. `validate_entry_id` AND `validate_action_id` must pass else stderr `Discarded possibly misspelled entry` (467) and the line is ignored [PROBED: `t.desktop:a:b` and `foo` discarded, `  t.desktop  ` accepted].
- No sign: appended to ENTRY_IDS (442), duplicates are NOT removed (the comment at 1186 is wrong; dedup happens by `unalias` at 1085). `-id`: id excluded from the FALLBACK list unless an earlier `+id` (first mention across files wins, 446-463). Excluded ids stay usable as explicit ids [PROBED: `-t` then `t` -> t.desktop].
- Order of reading = XTE__CONFIGS order, so the explicit ids of the highest-preference file come first.

## 5. Entry validation (read_entry_path 970-1018 + check_entry_key 802-968)

Runs under `LC_ALL=C` (972-976). Line walk: `read -r` with default IFS (trim), `[Desktop Entry]*` -> read_exec=true only when no action requested (989); line matching `[a-zA-Z0-9-]*` -> `Key=Value` processing with value = text after the first `=` minus leading spaces (993-995), any non-zero return -> `reset_keys` + return 1 (997-1002) = entry discarded; `[Desktop Action <action>]*` -> read_exec=true if the action was listed by an earlier `Actions=` line else return 1 (1005-1011); any other `[`-group header ends the read if read_exec already true (1014). A final line without trailing newline is never processed [PROBED: Exec last without newline -> entry has no Exec -> no terminal found].

check_entry_key matches on the WHOLE line, `'Name'*=*` prefix globs (so `ExecFoo=x`, `Exec[xx]=x`, `Exec = x` all match the Exec arm), first matching arm wins, order: Categories (816: must contain `TerminalEmulator` in `;`-split, sets IS_TERMINAL, else return 1), Actions (829: ignored without action; action must be listed else return 1), OnlyShowIn (846) and NotShowIn (865) (both skipped, return 0, when de_checks=false i.e. explicit ids; for fallback ids compared with the `:`-split XDG_CURRENT_DESKTOP, case-sensitive), `X-TerminalArgExec`/`TerminalArgExec` (885), `X-ExecArg`/`ExecArg` (893, ignored only when XTE__EXECARG_COMPAT is literally `false`), TerminalArgAppId (905), TerminalArgTitle (912), TerminalArgDir (919), TerminalArgHold (926), TryExec (933: `command -v` after escape expansion, failure -> return 1), Hidden (938: only the exact text `true` rejects; `True` does not), Exec (947: ignored when read_exec=false; else expand, tokenize, strip fields, `command -v` of first token, failure -> return 1). Keys are processed in file order in every group visited until the break. NOT checked anywhere: `Type=`, `NoDisplay`, `Name`, `Terminal`.

Quirks found while mapping (all [PROBED] unless noted) that any re-implementation must reproduce:

- Q1 errexit is suppressed inside `check_entry_key ... && continue` (997) and `read_entry_path ... || continue` (1086), so a `return 1` from `de_tokenize_exec` (958) or `de_strip_fields` (960) is NOT propagated: `Exec=foo --a "$X" bar` is accepted with Exec = `foo --a` (truncated at the error); `Exec=foo -c 'x y'` -> `foo -c`; `Exec=foo %f %f x` (second file field) leaves EXEC_USEP as the tokenized string WITH the fields -> `foo %f %f x`; unknown `%z` -> `foo %z x`. (de_strip_fields assigns EXEC_USEP only at its end, 738.)
- Q2 State leak between candidates: `reset_keys` is called only on a failed key (999), not when `find_entry` skips an entry at 1088/1090/1099. An entry that parses but is not a terminal (or has no Exec) leaves its EXEC_USEP, EXECARG(+DEFINED), APPID/TITLE/DIR/HOLD args and IS_TERMINAL in the globals for the next candidate. Observed: entry A (Exec `foo --leak`, TerminalArgDir `--cwd=`, no Category) then entry B (TerminalEmulator, no Exec, TerminalArgExec `-x`) -> B selected, cmd `foo --leak --cwd=/d -x prog`; and the reverse (A terminal without Exec, B with Exec) inherits A's `TerminalArgExec=--` and Title/Dir args.
- Q3 `while read` drops a last line lacking `\n` (config lists too, line 367).
- Q4 Fallback order within ONE directory is `find` traversal (readdir) order, not sorted: fallback list is built by prepending (790), so the entry found LAST by find is tried FIRST [PROBED: files a,m,b,q,c created in that order -> c.desktop chosen; `os.scandir` order == `find -L` order here, scratch fs xfs]. Across dirs: ascending preference in find order, so data home entries are tried first, then the last XDG_DATA_DIRS entry. Same id in several dirs: highest-preference path wins (alias overwritten, 782) but every occurrence is appended to the fallback list (790); `unalias` (1085) makes later occurrences skip.
- Q5 `Type=Link` accepted, `NoDisplay=true` accepted, `Hidden=True` accepted, CRLF files accepted (a trailing CR is `[[:space:]]` to the tokenizer / category split) [PROBED].
- Q6 OnlyShowIn/NotShowIn apply to fallback ids only; an explicit id bypasses them [PROBED: OnlyShowIn=GNOME entry listed in xdg-terminals.list is selected under XDG_CURRENT_DESKTOP=Hypr; as fallback it is skipped].
- Q7 Action ids: `id:action` uses the Exec of `[Desktop Action <action>]` (the main Exec is ignored); printed id and path get `:<action>` appended [PROBED]. Unlisted action -> entry skipped [PROBED].
- Q8 Empty fields: XDG_CURRENT_DESKTOP is split on `:` with IFS=`:` unquoted (150): `A::B:` -> words `a`, empty, `b` (the empty word yields `<dir>/-xdg-terminals.list`), leading `:` gives an empty first word, a trailing `:` adds nothing [PROBED via XTE_DEBUG path dump]. An empty element in XDG_CONFIG_DIRS yields `/xdg-terminals.list` at filesystem root; `XDG_CONFIG_HOME=` / `XDG_DATA_HOME=` empty behave as unset (`:-`).
- Q9 Path printing (1341-1343): `${P%%/./*}/${P##*/./}` removes the `/./` marker inserted by find; if the data dir text itself contains `/./` the middle (including `applications`) is dropped: `XDG_DATA_HOME=$ROOT/home/./.local/share` printed `$ROOT/home/t.desktop` [PROBED].
- Q10 XTE_EXECARG_COMPAT inconsistency: 403 and 1094 use `check_bool` (0/no/junk = strict; junk also warns on stderr) but 895 treats only literal `false` as strict (inference from source, not probed).

## 6. Entry discovery (find_entry_paths 754-800)

`find -L <dir>/applications/.` (one start point per applications dir, ascending preference order) `-type f` with, per dir, `( -path '<dir>/applications/./[a-zA-Z0-9_]*.desktop' ! -path '<dir>/applications/./*[^a-zA-Z0-9_./-]*' )` OR-ed (773). `-path` patterns are globs and the dir text is NOT escaped. `find -L` follows symlinks (broken symlinks have `-type l`, excluded). `awk '{ print; sub(".*/[.]/", ""); gsub("/", "-"); print }'` prints the path then the ID (text after the LAST `/./`, remaining `/` -> `-`): `sub/x.desktop` has ID `sub-x.desktop` [PROBED]. The loop (779-799) registers `alias <id>=xte__entry_path='<path>'` (782) and appends excluded-filtered ids to the fallback list by prepending (790). Alias expansion inside non-interactive bash needs POSIX mode (`/bin/sh -> bash`); a dash `sh` would behave differently (not applicable to this host).

## 7. Print and exec composition (after option loop)

- Order of outputs is fixed: id (1327-1335), path (1336-1353), content (1354-1366), cmd (1468-1491) regardless of option order. Between items `printf '%b' "$XTE__PRINT_DELIMITER"` (default `\n`); `%b` semantics (bash builtin: `\n \t \0NNN \xHH \c ...`) apply, `\c` stops that single printf only [PROBED: `\t|\x41\cZ` printed `<TAB>|A` then the next item].
- id/path-only trailing newline rule 1380-1381. `--print-cmd` trailing newline rule 1486: newline appended when the cmd delimiter is exactly `\n`, or when something was printed before and the main delimiter is exactly `\n`. `--print-cmd=` (empty) separates args with `\n` (1480 default) but adds NO trailing newline [PROBED: `foo\n-e\na\nb`].
- `--print-content` + `--print-cmd` together: content (ends with newline), then delimiter, then cmd [PROBED].
- Prepend order (each `set --` prepends, so the FINAL argv is): Exec tokens (1450, IFS=USEP split: empty middle fields kept, a trailing empty field dropped), then APPID (1430-1443), TITLE (1415-1428), DIR (1400-1413), HOLD (1393-1398), EXECARG (1388-1391, only when at least one command arg remains and EXECARG non-empty), then the user args. ARG with value ending `=` is glued to the value (one argv word), else two words. Observed: `foo --class a --t=x\ y --wd /d --hold -e p q` [PROBED]. Both the Arg and the option value must be non-empty (1400, 1415, 1430); HOLD needs `--hold` (1393).
- `--test` (1460-1466) prints `Command and arguments:` + `  >arg<` lines, rc 0, even without any `--print-*`; it wins over `--print-cmd` [PROBED]; it passes through 1455 so it spawns `save_cache`.
- No print/test: `cd "$XTE__DIRVAL"` when the entry has no TerminalArgDir (1494-1497), then `exec "$@"` (1499): this launches a terminal: out of scope for every probe.

## 8. Reads, calls, exits

### Environment variables read (all via `${VAR-}`-style or defaults)

| variable | lines | role |
|---|---|---|
| XDG_CURRENT_DESKTOP | 137(help text), 195, 848, 857, 867, 876, 1144 | lowercased desktop words for list names (1144, 150, 159); case-sensitive `:`-split for OnlyShowIn/NotShowIn; hash input |
| XDG_CONFIG_HOME, XDG_CONFIG_DIRS, HOME | 148 | config list dirs (empty = unset; defaults `$HOME/.config`, `/etc/xdg`) |
| XDG_DATA_DIRS | 157, 166 | list dirs and applications dirs (default `/usr/local/share:/usr/share`) |
| XDG_DATA_HOME | 166 | highest-preference applications dir (default `$HOME/.local/share`) |
| XDG_CACHE_HOME | 172-173, 303 | cache file dir; the script assigns it (172) |
| XTE_DEBUG, DEBUG | 61 | debug to stderr only; unrecognised value -> stderr warning only |
| XTE_EXECARG_COMPAT | 1147, 1149 | compat default true; set (even empty) marks directive CONFIGURED |
| XTE_CACHE_ENABLED | 1172, 1174 | cache default true |
| LC_ALL | 183, 355, 972 | re-call-with-C guards (185, 357, 974); find run with LC_ALL=C (795); `LANG=C` for `ls` (200) |
| PATH | implicit | `command -v` (274, 936, 964), tr/find/awk/ls/md5sum/mkdir/rm lookups |
| TMPDIR | implicit | bash heredoc temp files for large here-documents (792-799 holds every entry path); a 450 KB case with TMPDIR=/nonexistent-tmp still printed the right id [PROBED], so not a hard dependency |
| `$0` | 32 | help text name; tool should print `xdg-terminal-exec` when mirroring |

### External commands (everything else is builtin: printf, read, command -v, alias/unalias/eval, cd, umask, echo, exec)

| command | line | when |
|---|---|---|
| tr | 1144 | ALWAYS (past help): lowercases XDG_CURRENT_DESKTOP |
| find | 795 | ALWAYS cold: `find -L ... -type f` |
| awk | 797 | ALWAYS cold |
| ls | 200 | only gen_hash: read_cache with a parsable cache, save_cache (past 1455) |
| md5sum | 201 | same |
| mkdir | 303 | save_cache, only if cache dir missing |
| rm | 307, 315, 337 | save_cache removal branches |
| the terminal | 1499 | launch only |

`$(...)` subshells (42, 190, 688, 793, 1144) and the `save_cache ... &` fork (1457) are shell forks, not execs. A Python port that must start no process cannot call these tools and must model `tr` (ASCII-only lowercase), `find -L` (traversal order = readdir order, regular files after symlink resolution) and `awk` (ID derivation) itself; `ls/md5sum/mkdir/rm` are cache-only and out of contract.

### Exit statuses

| rc | trigger | line |
|---|---|---|
| 0 | `-h`/`--help` before `--` | 1138 |
| 0 | id/path-only or content print | 1376, 1383 |
| 0 | `--test` | 1464 |
| 0 | `--print-cmd` | 1490 |
| 1 | no valid terminal entry (stderr `No valid terminal entry was found in:` + dirs) | 1108-1110, 1208 |
| 1 | errexit abort (set -e): `cd` into a missing dir (1496), unreadable entry on `--print-content` (1362); under nounset an unbound variable [INFERENCE, not triggered] | 23 |
| 126/127 | `exec "$@"` fails (not reachable by print modes) | 1499 |
| (terminal status) | `exec` replaces the shell | 1499 |
| hang (no rc) | an empty-string argument in the option loop | 1224-1322 |

`save_cache` runs in the background and can never change the exit status or stdout of the foreground run.

## 9. Probe cases behind the [PROBED] tags

Run in scratch with `XDG_CACHE_HOME` inside scratch and print-only options: base, id-only (no cache written), tokenizer error x2, field error x2, no-trailing-newline x2, state leak x2, empty argument (timeout), print delimiter `%b`, empty cmd delimiter, `\0` delimiter, help, no-terminal, `$ROOT`-path odd-XDG dumps (`XTE_DEBUG=1` stderr `XTE__CONFIGS` lines), Type=Link, CRLF, Hidden true/True, NoDisplay, TryExec missing, OnlyShowIn/NotShowIn x3, fallback order across dirs and within a dir, subdir id, exclusions, desktop list precedence, action listed/unlisted, strict mode, `/execarg_default`, TerminalArgExec match, misspelled ids, `--print-content` (+cmd), `/./` path, entry arg composition, `--test`, `-h` placement, `-e`, unknown options, duplicate print options, 450 KB heredoc with bad TMPDIR.
