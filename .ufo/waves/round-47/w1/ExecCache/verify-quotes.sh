#!/bin/sh
# verify-quotes.sh — check every quote used in ExecCache.md against the pinned resolver.
# Each entry: <line-number> <fixed string taken verbatim from that line>.
# A quote passes only if the exact string appears on the exact cited line.
set -u
SRC=${1:-/usr/bin/xdg-terminal-exec}
fails=0
chk() {
	line=$1
	shift
	want=$*
	have=$(sed -n "${line}p" "$SRC")
	case "$have" in
	*"$want"*) printf 'OK   %s: %s\n' "$line" "$want" ;;
	*)
		printf 'FAIL %s: wanted <%s>\n' "$line" "$want"
		printf '     have   <%s>\n' "$have"
		fails=$((fails + 1))
		;;
	esac
}

chk 172 'XDG_CACHE_HOME=${XDG_CACHE_HOME:-"${HOME}/.cache"}'
chk 173 'XTE__CACHE_FILE=${XDG_CACHE_HOME}/xdg-terminal-exec'
chk 180 'return md5 of custom string, XDG_CURRENT_DESKTOP and ls -LRl output'
chk 194 'echo 4'
chk 200 'LANG=C ls -LRl ${xte__hash_paths} 2> /dev/null'
chk 223 'xte__line_limit=50'
chk 240 'reached cache line limit ($xte__line_limit)'
chk 274 'if [ "$XTE__HASH" = "$xte__cached_hash" ] && command -v "$xte__cached_cmd"'
chk 275 'debug "cache is actual"'
chk 287 'debug "cache is out-of-date"'
chk 291 'debug "invalid cache data"'
chk 314 "One or more of terminal's arguments contains a newline"
chk 320 'umask 0077'
chk 332 '"${XTE__EXEC_USEP}${XTE__RSEP}END_OF_EXEC_USEP" > "${XTE__CACHE_FILE}"'
chk 336 "cache is disabled, removing"
chk 380 '/disable_cache)'
chk 1169 'no way of telling if cache is enabled or not'
chk 1179 'if check_bool "${XTE__CACHE_ENABLED}" && read_cache; then'
chk 1340 'remove /./ delimiter'
chk 1342 "*'/./'*) XTE__ENTRY_PATH=\${XTE__ENTRY_PATH%%/./*}/\${XTE__ENTRY_PATH##*/./}"
chk 1368 'early bail out in some print modes'
chk 1370 "'  ' | *' cmd '*)"
chk 1456 'saves or removes cache, forked out of the way'
chk 1457 'save_cache "$1" &'
chk 1499 'exec "$@"'
chk 363 "reading config '\$xte__config_path'"

printf '\nverified against %s (sha256 %s)\n' "$SRC" "$(sha256sum "$SRC" | cut -d' ' -f1)"
printf 'MADO_CACHE_QUOTES: %s failed\n' "$fails"
[ "$fails" -eq 0 ]
