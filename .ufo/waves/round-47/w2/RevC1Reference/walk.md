# RevC1Reference — branch walk: xdg-terminal-exec v0.14.3 (1499 lines) vs L1 draft mado-terminal.py (1055 lines)

Reference = `.ufo/waves/round-47/fetch/xdg-terminal-exec` (sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac,
identical to /usr/bin/xdg-terminal-exec). Draft = `.ufo/waves/round-47/l1-draft/mado-terminal.py`.
Verdicts: MODELLED (draft reproduces observable stdout+rc), OOC-DECLARED (draft refuses with
`MADO_TERM_OUT_OF_CONTRACT` and the contract docstring declares it), HOLE (divergence the docstring does NOT declare).

| reference lines | what it does | draft location | verdict |
|---|---|---|---|
| x:1-26 shebang/header comments | no output path | — | MODELLED (no behavior) |
| x:28-29 `set -euf` | errexit + nounset + noglob baseline | Exit(1) paths, glob-free matching | MODELLED (e18 unreadable-list: both rc 1, stdout empty) |
| x:26,31-37 XTE__OIFS / XTE__LF | IFS baseline; bash never imports IFS from env | assumes default IFS | MODELLED |
| x:39-40 SELF_NAME | usage/help text only | — | OOC-DECLARED (-h/--help) |
| x:41-46 RSEP/USEP/CR heredoc `read -r` from `printf '%b\n' '\036' '\037' '\r'` | constants | USEP="\x1f" | MODELLED |
| x:48-51 error() | stderr lines | Resolver.err | MODELLED |
| x:53-63 check_bool | 7 true / 6 false literals, else "Assuming '%s' means no" + rc 1 | check_bool | MODELLED |
| x:65-85 XTE_DEBUG/DEBUG + debug() | reads XTE_DEBUG or DEBUG; D: lines to stderr; x:1203,1205 leak IFS=$XTE__LF before find_entry (which sets IFS explicitly) | not read | MODEL-EQUIVALENT on stdout/rc; env vars absent from docstring env list — minor gap (see report F5) |
| x:77-82 shcat | `IFS= read -r` stdin cat, unterminated last line dropped | read_lines(text, False) | MODELLED (e12 AGREE) |
| x:84-142 usage/help | help text, exit 0 | OutOfContract | OOC-DECLARED |
| x:143-177 make_paths | `${XDG_CONFIG_HOME:-"${HOME}/.config"}` etc.; HOME expanded ONLY inside `:-` defaults (x:148, x:168, x:172); trailing `/` strip; IFS=':' word split (empty middle fields kept, trailing dropped) | make_paths | HOLE F1/F3 — draft raises OOC "HOME unset" unconditionally (mado-terminal.py:406-407); real works with HOME unset when the XDG vars are set (e2: real rc 0 selects, draft rc 2); with defaults needed real dies `line 148: HOME: unbound variable` rc 1 (e2b) vs draft rc 2 |
| x:179-215 gen_hash (md5 of `ls -LRl`) | warm-cache validity | not modelled | OOC-DECLARED (cache) |
| x:217-298 read_cache | warm-cache selection | not modelled | OOC-DECLARED (cache) |
| x:300-340 save_cache (forked at x:1457) | writes cache on EVERY cold run incl. print modes | writes nothing | OOC-DECLARED (cache; tool-writes-no-file is the contract) |
| x:342-349 list_contains | +/- first-wins | included/excluded lists | MODELLED |
| x:351-475 read_config_paths | LC_ALL=C re-call; `[ -f ]` skip; unreadable `done < file` redirect failure = errexit rc 1 (x:361); directives first-one-wins, env wins; `/execarg_default:*:*` 3-field read; `[a-zA-Z0-9_]*|[+-][a-zA-Z0-9_]*` entries; misspelled error at x:467 uses the STRIPPED line (x:431 `xte__line=$_line`) | read_config_paths | MODELLED except stderr text: draft re-adds the +/- marker (mado-terminal.py:479 `excl + line`) — stderr not judged by PRED-C1 (report F5) |
| x:477-499 replace | replaces ALL `%%` with `%` | str.replace in strip_fields | MODELLED |
| x:501-559 de_expand_str | \s \n \t \r \\; trailing backslash dropped (reappend case commented out x:546-549); unknown escape keeps char, drops backslash | expand_str | MODELLED |
| x:561-692 de_tokenize_exec | special set, in_space, quote open/close, unquoted-special fail, quoted `` ` $ `` fail, dangling backslash fail, quoted space/special append, outer-space skip, unterminated-quote fail; final debug splits in a `$()` subshell (IFS isolated) | tokenize | MODELLED |
| x:694-740 de_strip_fields | %dDnNvm drop; %fFuU once-else fail (input UNchanged on failure, XTE__EXEC_USEP keeps tokenized); %i %c; %%→%; `*%?*`/`*[!%]%` fail; NOTE x:700 sets IFS=USEP, restored only at x:740 — early `return 1` paths LEAK IFS | strip_fields returns (input, False) on failure | MODELLED outcome-wise (selftest strip-fields-failure-keeps-tokens); leak benign: every later unquoted expansion sets IFS explicitly (x:920, x:934, x:1203, x:1448) — static analysis, see gaps |
| x:742-752 reset_keys | EXECARG defaults to `-e` | reset_keys | MODELLED |
| x:754-800 find_entry_paths | `find -L <dir>. -type f` + per-dir `-path "$d./[a-zA-Z0-9_]*.desktop" ! -path "$d./*[^a-zA-Z0-9_./-]*"`; awk sub greedy last `/./` + gsub → id; alias last-wins; fallback prepend unless excluded; while reads path+id pairs | _walk/_find paths | MODELLED (e1a/e1b digit-leading ids AGREE — POSIX-mode bash expands those aliases; draft dict keys match) |
| x:802-968 check_entry_key | check order Categories, Actions, OnlyShowIn, NotShowIn, X-TerminalArgExec/TerminalArgExec, X-ExecArg/ExecArg (strict ignores), AppId, Title, Dir, Hold, TryExec (x:936), Hidden (exact lowercase `true` only), Exec (read_exec gate; x:964 EXEC0 via command -v); empty `;`-values skip the loop and leak IFS=';' (benign, explicit IFS at all later split sites) | check_entry_key (same order) | MODELLED (e9 AGREE) |
| x:970-1018 read_entry_path | `[Desktop Entry]` prefix + status semantics; key pattern `[a-zA-Z0-9-]*`; value `${line#*=}` (no `=` → whole line) + leading-SPACE-only strip; `[Desktop Action <a>]` + action_listed; `[` group-end break; comments → status 0; loop status = function status | read_entry_path | MODELLED (selftest loop-status cases; e12 AGREE) |
| x:1020-1053 validate_entry_id / validate_action_id | charset + `.desktop` suffix + not `.desktop` | valid_entry_id/valid_action_id | MODELLED |
| x:1055-1111 find_entry | LF-split `ENTRY_IDS ∥ //fallback_start// ∥ FALLBACK`; `*:*` first-:-action / last-:-id; alias-exists + pop (duplicates skipped); reject → continue; empty EXEC_USEP / not-terminal → skip WITHOUT reset (carry-over); execarg default or strict-skip; exhaust → `IFS=':' error ... ${XTE__APPLICATIONS_DIRS}` rc 1 | find_entry | MODELLED (e3 stderr dir list shape matches) |
| x:1113-1131 get_default_execarg | first per-id default; `IFS=':' read -r id arg` remainder rule | execarg_defaults list + read_split | MODELLED (probes 1-9 + selftest trailing-colon case) |
| x:1133-1142 -h/--help pre-loop (stops at `--`) | help + exit 0 | OutOfContract scan before `--` | OOC-DECLARED |
| x:1144 lowercase XDG_CURRENT_DESKTOP | `tr '[:upper:]' '[:lower:]'` (external! needs PATH; ASCII-only in practice); command substitution drops trailing \n | desktops_lower | MODELLED (s6 AGREE) |
| x:1146-1177 globals | XTE_EXECARG_COMPAT/XTE_CACHE_ENABLED defaults; EMPTY env value = "not configured" | select() init | MODELLED |
| x:1179-1208 cache gate; read_config_paths; find_entry_paths; `find_entry \|\| exit 1` | cold path | select() | MODELLED (cold) |
| x:1224-1322 option loop | case order: `--`, `-e|$XTE__EXECARG`, `--app-id=`, `--title=`, `--dir=`, `--hold`, `--test`, `--print-path`, `--print-id`, `--print-content`, `--print-cmd`, `--print-cmd=*`, `--print-delimiter=*`, `[!-]*` break, `-*` discard; option values read via heredoc `IFS='=' read -r a b` = FIRST LINE of the argv element + bash read-remainder rule; empty argv element matches no pattern → infinite loop | run_print loop (same order; read_split) | MODELLED (s1-s3, e15, e17 AGREE); empty-argv OOC-DECLARED |
| x:1325-1416 print id/path/content | id first, `%s` + `:action`; path `/./` fold (first `%%`/last `##`) + `%b` delimiter when not first; content = shcat verbatim + delimiter; early bail: no data or cmd → continue; content-only → exit 0; else optional final \n when delimiter is literal `\n` | run_print | MODELLED (e8, e12, e14, e17 AGREE) |
| x:1418-1454 option prepend | EXECARG only when remaining args exist; HOLDARG+--hold; DIR/TITLE/APPID trailing-`=` append vs two args, prepend order DIR→TITLE→APPID; `IFS=$XTE__USEP; set -- $XTE__EXEC_USEP "$@"` (x:1448) | run_print | MODELLED (s2, s3 AGREE) |
| x:1460-1465 --test | prints before print-cmd; --test beats --print-cmd | run_print test branch | MODELLED (s1 AGREE) |
| x:1467-1492 print-cmd | `%b` delimiter before block when not first; `%s` per arg; empty pcdelim → `\n` (`${:-}`); trailing \n iff pcdelim='\n' or (not-first and pdelim='\n'); exit 0 | run_print | MODELLED (s3 AGREE) |
| x:1494-1497 `cd "$XTE__DIRVAL"` | errexit rc on failure | not modelled | UNREACHABLE in print modes (every print mode exits before x:1494); launch path only → OOC-DECLARED |
| x:1499 `exec "$@"` | launch | not modelled | OOC-DECLARED (no process) |
| command -v semantics (x:936, x:964, and via TryExec) | bash 5.3: aliases (incl. digit-leading names, POSIX mode), functions, builtins, keywords, slash-paths (non-directory, x-bit, NON-REGULAR allowed), PATH dirs, empty PATH entry = cwd, name starting `-` fails, PATH unset → bash default path | command_v + BASH_BUILTINS/BASH_KEYWORDS/SCRIPT_FUNCTIONS | MODELLED except PATH-unset → HOLE F2 (draft raises OOC, mado-terminal.py:374; real falls back to the default path and can select, e3b). Tables diffed vs host bash 5.3.20: 61/61 builtins, 22/22 keywords, 24/24 script function names |
| printf %b (delimiters) | `\a\b\e\E\f\n\r\t\v\\`, `\c` stops that call, `\0NNN` AND `\NNN` octal, `\xHH`, `\uHHHH`/`\UHHHHHHHH`, unknown → literal | printf_b | MODELLED (probes: `\101`→A, `\0101`→A, `a\x41b`→aAb, `\u0041`→A, `x\cy`→x, `A\zB`→A\zB); non-ASCII `\u00e9` → real prints UTF-8 é, draft OOC — OOC-DECLARED |

e2e matrix (14 AGREE / 4 DIVERGE): see `evidence-e2e.txt` in this dir; divergences e2, e3, e3b, e2b = findings F1-F3 below.
