#!/bin/bash
# Computes every locator used in the report with grep -n (locators are never typed) and writes quotes.txt.
set -u
L=/home/vgpnk/Projects/shokunin/mado-shokunin
R=$L/.ufo/waves/round-47/w2/RevengerCache
OUT=$R/quotes.txt
: > "$OUT"
fail=0
add() { # <relpath> <quote>
	local f=$1 q=$2 n
	n=$(grep -nF -- "$q" "$L/$f" | head -1 | cut -d: -f1)
	if [ -z "$n" ]; then
		echo "MISSING quote in $f: $q" >&2; fail=1; return 1
	fi
	printf '%s\t%s\t%s\n' "$f" "$n" "$q" >> "$OUT"
	printf '%s:%s  %s\n' "$(basename "$f")" "$n" "$q"
}
add .ufo/waves/round-47/fetch/xdg-terminal-exec 'XTE__CACHE_FILE=${XDG_CACHE_HOME}/xdg-terminal-exec'
add .ufo/waves/round-47/fetch/xdg-terminal-exec 'echo 4'
add .ufo/waves/round-47/fetch/xdg-terminal-exec 'LANG=C ls -LRl ${xte__hash_paths} 2> /dev/null'
add .ufo/waves/round-47/fetch/xdg-terminal-exec 'command -v "$xte__cached_cmd" > /dev/null'
add .ufo/waves/round-47/fetch/xdg-terminal-exec 'XTE__CACHE_ENABLED=${XTE_CACHE_ENABLED-true}'
add .ufo/waves/round-47/fetch/xdg-terminal-exec 'if check_bool "${XTE__CACHE_ENABLED}" && read_cache; then'
add .ufo/waves/round-47/fetch/xdg-terminal-exec 'XTE__ENTRY_PATH=${XTE__ENTRY_PATH%%/./*}/${XTE__ENTRY_PATH##*/./}'
add .ufo/waves/round-47/fetch/xdg-terminal-exec 'if [ "$XTE__CACHE_USED" = "false" ]; then'
add .ufo/waves/round-47/fetch/xdg-terminal-exec 'save_cache "$1" &'
add .ufo/waves/round-47/fetch/xdg-terminal-exec 'make_paths() {'
add .ufo/waves/round-47/fetch/xdg-terminal-exec '	read_config_paths'
add .ufo/waves/round-47/fetch/xdg-terminal-exec 'case "$XTE__TEST_MODE" in'
add quality/counters/c1-r47-terminal.py 'resolver (a warm cache) and -h/--help are outside the contract'
add quality/counters/c1-r47-terminal.py 'env["XDG_CACHE_HOME"] = os.path.join(root, ".rw", "cache")'
add quality/counters/c2-r47-terminal-entry.py 'holds `resolver_sha256=<the v0.14.3 script digest>`, >= 3 XDG_* lines, and `observed=<path>`'
echo "rows=$(wc -l < "$OUT") fail=$fail"
exit "$fail"
