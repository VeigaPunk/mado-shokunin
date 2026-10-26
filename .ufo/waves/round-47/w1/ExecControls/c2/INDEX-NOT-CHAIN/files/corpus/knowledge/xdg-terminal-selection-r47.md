source: S326 (https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/xdg-terminal-exec @ tag v0.14.3, sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac, pin .ufo/waves/round-47/fetch/xdg-terminal-exec)
source: S327 (https://raw.githubusercontent.com/Vladimir-csp/xdg-terminal-exec/v0.14.3/README.md @ tag v0.14.3, sha256 c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40, pin .ufo/waves/round-47/fetch/README-v0.14.3.md)
verified-at: 2026-10-26
recheck: 90d
surface: P4
scope: the print-mode selection chain of one resolver version on this host; the launch itself, rendered windows and reload effects stay out of scope

# Terminal selection by xdg-terminal-exec 0.14.3 - the executed chain

The selection order below is read from the pinned script bytes, and the host's own selection is confirmed by a live read-only receipt (`.ufo/waves/round-47/receipts/xdg-terminal-live.txt`).

## Chain (citation index)

| surface | locator | quote | reading |
|---|---|---|---|
| List files are built from the config hierarchy first | xdg-terminal-exec:143-178 | `for xte__dir in ${XDG_CONFIG_HOME:-"${HOME}/.config"}${IFS}${XDG_CONFIG_DIRS:-/etc/xdg}; do` | each hierarchy directory adds its desktop-prefixed list before its plain list, so the first readable file wins the tail of the preference order |
| The desktop token is the lowercased XDG_CURRENT_DESKTOP | xdg-terminal-exec:143-178 | `for xte__desktop in ${XTE__LOWERCASE_XDG_CURRENT_DESKTOP}; do` | a colon-separated desktop list contributes one prefixed list per item, in that order |
| Every list line becomes a preference in file order | xdg-terminal-exec:351-476 | `debug "added entry ID with action ID '$xte__line'"` | read_config_paths appends a validated entry id as it reads, and discards the rest with a message, so a line is a preference and not a guarantee |
| Duplicate desktop-file ids resolve to the last found | xdg-terminal-exec:754-801 | `# Entries are checked in ascending order of preference, so use last found if duplicate` | find_entry_paths registers the ids it finds in ascending preference and keeps the last, which is how a user-local entry shadows the system copy |
| The explicit list is walked, then the fallback | xdg-terminal-exec:1055-1112 | `for xte__entry_id in ${XTE__ENTRY_IDS}${XTE__LF}//fallback_start//${XTE__LF}$XTE__FALLBACK_ENTRY_IDS; do` | find_entry tries the listed ids first with the desktop show-in checks off, then flips them on at the marker and walks the fallback ids |
| An entry must parse and declare the terminal category | xdg-terminal-exec:1055-1112 | `[ -z "${XTE__IS_TERMINAL}" ] && continue` | check_entry_key sets the terminal flag only for a TerminalEmulator category, and find_entry skips any candidate that has no parsed Exec or no terminal category |
| The printed path is the file path, not the find start path | xdg-terminal-exec:1340-1344 | `*'/./'*) XTE__ENTRY_PATH=${XTE__ENTRY_PATH%%/./*}/${XTE__ENTRY_PATH##*/./} ;;` | print-path compacts the /./ separator find leaves in the start path, so the printed path is the desktop file itself |

The rows above list where each surface lives; the order they imply is the reader's, not the resolver's.
## The documented contract

- **Configuration files are named.** "Configuration files are named `${desktop}-xdg-terminals.list` or `xdg-terminals.list`" (README-v0.14.3.md:100-101) - the two file names the script builds.
- **The list format.** "The format is a simple newline-separated list with decreasing priority." (README-v0.14.3.md:131-131) - one id per line, decreasing priority downwards.
- **Applicability is checked per entry.** "Each entry from the explicit selection list is checked for applicability:" (README-v0.14.3.md:166-166) - a listed id is a candidate, not a promise.

The documented route names the option surface, including the `--print-delimiter=seq` separator and the `--print-cmd` command renderer; the script's `print-delimiter` handling and its print blocks are the executed side of the same contract.

## The round-17 unknown, answered for the selection stage

Round 17 left `[UNK]` whether the resolver actually picks the user-local entry over the system one (`corpus/knowledge/terminal-route-r17.md:144`). The live receipt `.ufo/waves/round-47/receipts/xdg-terminal-live.txt` answers the selection stage: the `--print-id --print-path --print-cmd` capture names the user override entry, and re-running the landed tool over that capture reports `verdict=AGREE`. The launch of a window is not observed and is not claimed.

## Held ground

The documentary route stays with its own note and rows; nothing here restates the README-level contract as host behaviour, and no terminal tree note is reopened.

Pins: `.ufo/waves/round-47/fetch/xdg-terminal-exec`, `.ufo/waves/round-47/fetch/README-v0.14.3.md`. Receipt: `.ufo/waves/round-47/receipts/xdg-terminal-live.txt`.
