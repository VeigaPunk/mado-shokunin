#!/bin/sh
# Verifies every literal quote and line locator used by docstring.md against the pinned script.
# usage: verify-quotes.sh [PIN]
set -eu
PIN=${1:-/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/fetch/xdg-terminal-exec}
fail=0
check() { # check <line> <fixed string>
	line=$1; shift
	if sed -n "${line}p" "$PIN" | grep -Fq -- "$1"; then
		printf 'OK   %4s  %s\n' "$line" "$1"
	else
		printf 'FAIL %4s  %s\n' "$line" "$1"
		fail=1
	fi
}
check 23 'set -euf'
check 148 '${XDG_CONFIG_HOME:-"${HOME}/.config"}'
check 166 '${XDG_DATA_HOME:-${HOME}/.local/share}'
check 172 'XDG_CACHE_HOME=${XDG_CACHE_HOME:-"${HOME}/.cache"}'
check 173 'XTE__CACHE_FILE=${XDG_CACHE_HOME}/xdg-terminal-exec'
check 191 'xte__hash_paths=${XTE__CONFIGS}:${XTE__APPLICATIONS_DIRS}'
check 194 'echo 4'
check 195 'echo "${XDG_CURRENT_DESKTOP-}"'
check 200 'LANG=C ls -LRl'
check 221 'if [ -f "${XTE__CACHE_FILE}" ]; then'
check 226 'while IFS= read -r xte__line; do'
check 239 '"$xte__line_limit")'
check 240 'reached cache line limit'
check 250 'END_OF_EXEC_USEP'
check 258 'done < "${XTE__CACHE_FILE}"'
check 274 'command -v "$xte__cached_cmd"'
check 275 'cache is actual'
check 287 'cache is out-of-date'
check 291 'invalid cache data'
check 295 'no cache data'
check 302 'if check_bool "$XTE__CACHE_ENABLED"; then'
check 312 'case "${XTE__HASH}${1}'
check 320 'umask 0077'
check 332 'END_OF_EXEC_USEP" > "${XTE__CACHE_FILE}"'
check 336 'cache is disabled, removing'
check 376 '[ -z "$XTE__CACHE_CONFIGURED" ] || continue'
check 380 '/disable_cache)'
check 782 'alias "$xte__entry_id"'
check 1172 'XTE__CACHE_ENABLED=${XTE_CACHE_ENABLED-true}'
check 1174 'XTE__CACHE_CONFIGURED=${XTE_CACHE_ENABLED-}'
check 1179 'if check_bool "${XTE__CACHE_ENABLED}" && read_cache; then'
check 1342 'XTE__ENTRY_PATH=${XTE__ENTRY_PATH%%/./*}'
check 1362 'shcat < "${XTE__ENTRY_PATH}"'
check 1450 'set -- $XTE__EXEC_USEP "$@"'
check 1455 'if [ "$XTE__CACHE_USED" = "false" ]; then'
check 1457 'save_cache "$1" &'
check 1460 'case "$XTE__TEST_MODE" in'

TOOL=/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-terminal.py
checkt() { # checkt <line> <fixed string> - quotes taken from the tool's own docstring
	line=$1; shift
	if sed -n "${line}p" "$TOOL" | grep -Fq -- "$1"; then
		printf 'OK   tool:%s  %s\n' "$line" "$1"
	else
		printf 'FAIL tool:%s  %s\n' "$line" "$1"
		fail=1
	fi
}
checkt 14 'for a cold cache (see "Cache" below)'
checkt 19 'cache=<absent|present|disabled>'
checkt 42 'set in the environment win'
checkt 43 'over any directive)'
checkt 82 'Cache (out of contract)'
checkt 82 'xdg-terminal-exec (default $HOME/.cache)'
checkt 85 'HOME unset'

CLAIMS=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/claims.md
checkc() { # checkc <line> <fixed string> - quotes taken from the round-48 claims
	line=$1; shift
	if sed -n "${line}p" "$CLAIMS" | grep -Fq -- "$1"; then
		printf 'OK   claims:%s  %s\n' "$line" "$1"
	else
		printf 'FAIL claims:%s  %s\n' "$line" "$1"
		fail=1
	fi
}
checkc 20 'HOME unset modelled as the pin (round-47 D1)'
exit "$fail"
