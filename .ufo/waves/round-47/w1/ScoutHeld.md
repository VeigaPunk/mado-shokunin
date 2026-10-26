# ScoutHeld - what the lane already holds on xdg-terminal-exec selection (round 47, w1)

Base: `60edb66e2f1cb90acc6e9442fc93ded0ca42d750` (all `git grep` below name it). Read-only; no host command run.
Script read for the "not held" side: `/usr/bin/xdg-terminal-exec`, sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`
(= S057 / v0.14.3; `wc -l` 1499). Line numbers below are of that script, from `cat -n`.

## 0. Where the lane mentions xdg-terminal-exec (git grep -l at base)
Outside `.ufo/`: `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/{terminal-route-r17,terminals-and-omarchy,hyprland-config-plane,idle-lock-plane,remaining-planes-census,waybar-walker-plane,waybar-walker-semantics}.md`,
`corpus/lessons/{round-17,round-17-verifier-spotcheck}.md`, `tools/mado-tripwire.py` (:272, only a name in a deny list).
`terminal-trees-r23.md` has no literal "xdg-terminal-exec" (only :87 "round-17 resolver honours [Hidden] (S057)", `[UNK]`, "not re-derived here"; :76 `grep -v '^#' ~/.config/xdg-terminals.list`; :94 narrows terminals-and-omarchy §8).
Inside `.ufo/`: 21 wave dirs; only two are source-of-truth-grade for the rule text: `round-18/fetch/FetchBackfillR17/s056-xtd-readme` and `s057-xtd-script` (raw pinned bytes, the whole script) and the r17 scout report `round-17/w1/reports/SrcXdgTerminalExec.md` (a working report, not a corpus entry).

## 1. Rules ALREADY held in the corpus (file:line at base)
| Rule | Held at | Depth |
|---|---|---|
| File names `${desktop}-xdg-terminals.list` / `xdg-terminals.list` | terminal-route-r17.md:24-26 (README:100-101 quote) | name only |
| Lookup order: user file after its desktop sibling, before /etc/xdg; data-dir copies lowest | r17:28-32 (README:115-123, script:148-162) | one sentence; no per-dir order list, no XDG_CONFIG_DIRS/XDG_DATA_DIRS list expansion, no unset defaults |
| List format: newline list, decreasing priority, `#` comment | r17:33-34 (README:131,133) | |
| "each entry is checked for applicability"; failing entries discarded | r17:35-39 (README:153-166) | prose only |
| `--dir=workdir` option documented/parsed | r17:40-42 (script:106,1252) | |
| `TerminalArgDir` key read | r17:42-43 (script:919) | key named, no composition |
| Applicability reads Categories=TerminalEmulator (:816-822), TryExec (:933-937), Hidden (:938-942), enforced :1088-1090; X-TerminalArgExec read :885 | r17:44-46 | line cites only; no behaviour table, no ordering of checks |
| Duplicate IDs: dirs ascending preference, XDG_DATA_HOME last (:165-168), last found wins (:779-781) | r17:47-50 | stated as "documented basis"; no ID derivation, no collision outcome observed |
| Cache default on (`XTE_CACHE_ENABLED`, :1172), read first (:1179), saved after fresh selection (:300-302, :1455-1457) | r17:51-53 | 3 line cites |
| `/execarg_default:` directives (:402-413); upstream example list has no Alacritty entry | r17:58-60; SOURCES.md S057/S060 | one clause |
| Compliance wording README:264 | r17:54-57 | |
| Host: bindings.conf:2-3, `~/.config/xdg-terminals.list:3`=`Alacritty.desktop`, system list sha256 a2b5bf69.. (1053 B), user `Alacritty.desktop` lines 7,14-17 shadows system entry (0 X-Terminal keys) | r17:79-90, 99-101, 103-107 | bytes only |
| No desktop-prefixed list present in `~/.config` or `/etc/xdg` (maxdepth 1) | r17:89-91 | scan 2026-10-20, no `/usr/share`/`/usr/local/share` prefixed copy checked |
| Cache file observed as bytes: 190 B, records `alacritty`, `/home/vgpnk/.local/share/applications/./Alacritty.desktop`, four X-TerminalArg* values | r17:123-127 | `[OBS, bytes]`; the `/./` marker is shown but its removal on `--print-path` (:1341-1343) is not explained |
| Version binding resolver 0.14.3-2, script == tag | r17:131-139 | |
| Hidden=true makes the resolver skip an entry (applied to foot stubs) | terminal-trees-r23.md:86-87, terminals-and-omarchy.md:96 | `[UNK]`, "not re-derived here" |
| Launch binding SUPER+RETURN, SUPER+ALT+RETURN | terminals-and-omarchy.md:95; hyprland-config-plane.md:84; r17:81 | |
| `--app-id=org.omarchy.terminal` used by omarchy-menu:47 | waybar-walker-semantics.md:338 | |
| `xdg-terminal-exec --print-id` as screensaver terminal resolver, "not executed" | idle-lock-plane.md:309 | `[INF]` |
| The open question itself | r17:140-145 `[UNK] whether the resolver actually picks that entry over the system one at launch` | the C2 target |

Source rows held: S056 (README), S057 (script, anchors :106,148-162,402-413,919,1252), S058 (alacritty man), S059/S060 (host files), S071 (user Alacritty.desktop). `corpus/SOURCES.md:72` S060 "teaches" cell says "fallback exclusions and execarg defaults" - the only corpus mention of fallback exclusions, no rule text.

## 2. Rules NOT held in any corpus file (all confirmed by grep, section 4)
Script line numbers from the pinned script. These are the new entry's ground:
1. Desktop-prefixed list order and lowercasing: `XTE__LOWERCASE_XDG_CURRENT_DESKTOP` :1144 (`tr`), per-config-dir `${desktop}-` files for EACH colon item of XDG_CURRENT_DESKTOP, in listed order, before the plain file (:148-154); same for data dirs `xdg-terminal-exec/` (:157-163); defaults `${HOME}/.config`, `/etc/xdg`, `/usr/local/share:/usr/share`.
2. List-file line grammar: `/enable_cache`, `/disable_cache` (:374-385), `/execarg_compat`, `/execarg_strict` (:388-399), `/execarg_default:ID:ARG` (:402-415; ignored in strict mode), entry/`ID:action` lines starting `[a-zA-Z0-9_]` or `[+-]` (:425-469), `+id` protects / `-id` excludes from fallback (:445-464), first directive of a kind wins, env `XTE_CACHE_ENABLED`/`XTE_EXECARG_COMPAT` pre-empt (:1147-1149,1172-1174), misspelled-entry stderr message "Discarded possibly misspelled entry" (:467), validate_entry_id (:1020-1037: must end `.desktop`, charset `[a-zA-Z0-9_.-]`) and validate_action_id (:1039-1053).
3. Entry ID derivation and ID collision across data dirs: `find -L` over `$XDG_DATA_HOME/applications` + each `XDG_DATA_DIRS` item with `.` marker, path filter `[a-zA-Z0-9_]*.desktop` and `[^a-zA-Z0-9_./-]` rejection (:766-775), `awk` turns subdirectory `/` into `-` (:797), last registration wins via `alias` (:779-783), `unalias` after first try so a shadowed duplicate is never tried (:1081-1085), dir order built by prepending so XDG_DATA_HOME ends last (:166-169).
4. Fallback list: all found IDs minus `-` exclusions, reverse-registration order, appended after `//fallback_start//` marker (:785-791,1060-1074); `OnlyShowIn`/`NotShowIn` checks enabled ONLY in the fallback phase (:1058,1072; :846-884); explicit list entries skip them. Error text `No valid terminal entry was found in:` + dirs, exit 1 (:1109-1110,1208). The system list excludes yakuake, kitty-open, foot-server, footclient (host list lines 6-11).
5. Entry validation keys and their order: Categories splits on `;` for exact `TerminalEmulator` (:816-828); Actions only when an action was requested (:829-845); TryExec through `command -v` on the de-escaped value (:933-937); Hidden only `true` discards (:938-946); Exec read only from the main group or from `[Desktop Action <id>]`, action must be listed in Actions (:947-965, 989, 1005-1012, 1014); a failing key discards the entry and resets keys (:997-1002); entry with empty Exec, no TerminalEmulator, or (strict mode) no X-TerminalArgExec is skipped (:1088-1100); `[a-zA-Z0-9-]*` key-line shape (:991); `X-`-prefixed and unprefixed key names (`TerminalArgExec`, `X-ExecArg` legacy, :885-932); EXECARG default `-e`, per-ID default from `/execarg_default` (:1113-1130).
6. Exec parsing: `de_expand_str` (\s \n \t \r \\ , :501-559), `de_tokenize_exec` (unquoted specials fail the entry, :561-692), `de_strip_fields` (%f %F %u %U removed once, %d %D %n %N %v %m removed, %i %c removed, %% -> %, unknown % fails, :694-740), Exec[0] checked with `command -v` (:962-964), the US separator (:34-43, 1448-1451).
7. Exec-arg composition: option parse loop (:1224-1322: `--`, `-e`/EXECARG stop options, `--app-id=`, `--title=`, `--dir=`, `--hold`, `--test`, unknown `-*` dropped, first non-option stops); prepend order EXECARG (only when args remain, :1388) -> hold -> dir -> title -> appid, each `*=`-suffixed arg concatenated else two words (:1393-1443); Exec tokens placed first (:1450); `--dir` without TerminalArgDir -> `cd` only on real launch (:1494-1497).
8. Print modes: `--print-id`/`--print-path`/`--print-content`/`--print-cmd[=seq]`/`--print-delimiter=seq` (:1272-1312), emission order id, path, content, cmd (:1327-1366,1468-1492), `/./` removal in path (:1341-1343), `:action` suffix (:1331,1349), `%b` printing of delimiters, newline-terminate rules (:1380-1383,1486-1488), early exit before cmd for id/path/content (:1369-1385), `-h|--help` handled before everything (:1133-1141).
9. Cache: format (version 4, md5 of `ls -LRl` of config+applications dirs + XDG_CURRENT_DESKTOP, :179-215), 10 header lines + END_OF_EXEC_USEP terminator (:217-298), validity = hash equal AND `command -v` of cached command (:272-289), `save_cache` backgrounded with `&` (:1455-1458), removed when disabled or hash fails (:304-309,335-338), umask 0077 (:319-333). PRECISION NOTE (not in corpus; do not copy r17's wording forward): `--print-id`/`--print-path`/`--print-content` alone `exit 0` at :1376/:1383, BEFORE `save_cache` (:1455); only `--print-cmd`, `--test` and a real launch reach it. r17:129 "(test/print modes also write the cache)" and the round-47 brief "print modes write only the cache" are therefore too broad for id/path/content; this is `[INFERENCE]` from the script until an observation with a scratch XDG_CACHE_HOME confirms it.
10. The fallback chain's final outcome on this host with the user entry removed (live read-only), and which list line selected the entry (`~/.config/xdg-terminals.list:3`, which wins over `/usr/share/xdg-terminal-exec/xdg-terminals.list` that has no entry ID): not stated anywhere.

Outside the corpus, held only as working drafts in `.ufo/waves/round-17/w1/reports/SrcXdgTerminalExec.md` (not promoted to a knowledge entry): `-terminal.desktop` / `+terminal.desktop` semantics, `terminal.desktop:action`, `*ShowIn` fallback-only, the 8-path priority table. The new entry MAY cite README:137-150 afresh; these working-report lines are not citable corpus ground.

## 3. Ground-absent grep terms (>= 6) - all exit 1 over `corpus/` at the base
Command shape: `git grep -q -F -e '<term>' 60edb66e2f1cb90acc6e9442fc93ded0ca42d750 -- corpus; echo $?`. Each run below printed exit 1 (receipt, run 2026-10-26):
| # | term | what the new entry would say with it | script line |
|---|---|---|---|
| 1 | `fallback_start` | the marker separating explicit list from fallback IDs | :1060,1071 |
| 2 | `execarg_compat` (also `execarg_strict`) | the compat/strict directives and `XTE_EXECARG_COMPAT` | :388-399,1147 |
| 3 | `OnlyShowIn` (also `NotShowIn`) | show-in checks apply only to fallback entries | :846,865,1058,1072 |
| 4 | `TerminalArgHold` (also `X-ExecArg`) | key names read by check_entry_key, hold composition | :926,893,1393 |
| 5 | `print-content` (also `print-cmd`, `print-delimiter`) | the print modes and their order | :1272-1312,1327-1492 |
| 6 | `validate_entry_id` (also `validate_action_id`) | list-line validation, misspelled-entry discard | :1020,1039,439 |
| 7 | `gen_hash` (also `ls -LRl`, `END_OF_EXEC_USEP`) | cache hash and format | :179-215,217-298 |
| 8 | `XTE__EXCLUDED_ENTRY_IDS` (also `XTE__FALLBACK_ENTRY_IDS`) | `-id`/`+id` fallback exclusion state | :446-464,785-791 |
| 9 | `No valid terminal entry` | the NO_TERMINAL error text, exit 1 | :1109,1208 |
| 10 | `Discarded possibly misspelled` | invalid list line message | :467 |
| 11 | `de_tokenize_exec` (also `de_strip_fields`, `de_expand_str`) | Exec tokenizer and `%` field handling | :561,694,501 |
| 12 | `unalias` | shadowed duplicate never retried | :1085 |
| 13 | `Desktop Action` | `[Desktop Action <id>]` group read | :1005 |
| 14 | `hyprland-xdg-terminals` | the Hyprland desktop-prefixed list name (host: absent) | :151 |

Scope caveat (important for the L1 predicate): the unscoped `git grep -F <term> 60edb66e..` is NOT exit 1 for these, because `.ufo/waves/round-18/fetch/FetchBackfillR17/s057-xtd-script` is the raw script (e.g. `fallback_start` 2 hits there; `Discarded possibly misspelled` :467; `X-ExecArg` also in `.ufo/waves/round-17/w1/reports/SrcXdgTerminalExec.md:156`; `hyprland-xdg-terminals` once in `.ufo/waves/round-17/w1/reports/HostTerminalFiles.md:44`). The predicate must scope to `corpus/` (or `:!.ufo`). Terms that look absent but are NOT (exit 0, do not use): `XTE_CACHE_ENABLED` (terminal-route-r17.md:51), `TryExec`, `Hidden`, `TerminalArgTitle`, `--app-id`, `--title=`, `execarg_default`, `XDG_CURRENT_DESKTOP`, `xdg-terminal-exec/xdg-terminals`, `lowercased`, `find -L` (theme notes), `command -v`.
Also check the new entry does not trip the held-ground rule: it must not restate r17's documentary route (S056-S060), terminal-trees-r23, terminals-and-omarchy.

## 4. Verification receipts
- `git rev-parse 60edb66e2f1cb90acc6e9442fc93ded0ca42d750` ok; `sha256sum /usr/bin/xdg-terminal-exec` = 89f2be9a..27ac; `wc -l` 1499.
- For every term in section 3, `git grep -q -F -e '<term>' 60edb66e2f1cb90acc6e9442fc93ded0ca42d750 -- corpus` exit 1 (the 23 terms listed incl. the "also" ones; run as a loop, output printed per term).
- Counts at base for the sort: `git grep -l -i xdg-terminal-exec` outside .ufo = 12 files (section 0).
## Unresolved
- Whether `--print-id` alone leaves the cache untouched is derived from script :1369-1385 vs :1455, unobserved (a seat running it needs `XDG_CACHE_HOME` in scratch).
- The lane holds no observation of the resolver at all (r17:128 `[UNK]`); the host fact quoted in the brief (prints Alacritty.desktop, user override path, `alacritty`) is L1-supplied, not corpus.
