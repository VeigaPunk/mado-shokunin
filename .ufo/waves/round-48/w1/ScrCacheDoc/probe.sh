#!/bin/sh
# Regenerates the warm-cache receipts for the ScrCacheDoc seat (round 48 w1).
# Read-only with respect to the host: every xdg-terminal-exec run uses --print-cmd and an XDG_CACHE_HOME under
# $WORK; nothing under ~/.cache, ~/.config or the lane is written.
set -eu
WORK=${WORK:-/fast/scratch/hyaku/mado-r48/ScrCacheDoc}
R=$(cd "$(dirname "$0")" && pwd)/receipts
PIN=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/fetch/xdg-terminal-exec
X=/usr/bin/xdg-terminal-exec
T=$WORK/t
rm -rf "$T" "$WORK/dates" "$WORK/links" "$WORK/loop"
mkdir -p "$R" "$T/home/.config" "$T/etc" "$T/data/applications" "$T/usr/share" "$T/bin" "$T/cache"

mk_stub() { printf '#!/bin/sh\nexit 0\n' > "$T/bin/$1"; chmod 755 "$T/bin/$1"; }
mk_stub foo
mk_stub bar

entry() { printf '[Desktop Entry]\nType=Application\nName=Foo\nExec=%s\nCategories=System;TerminalEmulator;\n' "$1" > "$T/data/applications/foo.desktop"; }

# fixed, recent epoch: ls prints "Mon dd HH:MM" for it, and two seconds inside the same minute hash the same
NOW=$(date +%s)
PINNED=$((NOW - 3600))

run() { # run <cache-home> <extra env...> -- args...
	ch=$1; shift
	env -i HOME="$T/home" XDG_CONFIG_HOME="$T/home/.config" XDG_CONFIG_DIRS="$T/etc" \
		XDG_DATA_HOME="$T/data" XDG_DATA_DIRS="$T/usr/share" XDG_CACHE_HOME="$ch" \
		XDG_CURRENT_DESKTOP=Hyprland PATH="$T/bin:/usr/bin:/bin" LC_ALL=C "$@" \
		timeout 10 "$X" --print-cmd
}

{
	echo "== pin and host binary"
	sha256sum "$PIN" "$X"
	echo
	echo "== prime (cold, --print-cmd) writes the cache in the background"
	entry foo
	printf 'foo.desktop\n' > "$T/home/.config/xdg-terminals.list"
	touch -d "@$PINNED" "$T/data/applications/foo.desktop" "$T/home/.config/xdg-terminals.list"
	rm -rf "$T/cache"; mkdir "$T/cache"
	echo -n 'stdout: '; run "$T/cache"
	sleep 1
	echo -n 'cache line count: '; wc -l < "$T/cache/xdg-terminal-exec"
	echo -n 'cache line 1: '; sed -n 1p "$T/cache/xdg-terminal-exec"
	echo 'cache bytes:'; od -c "$T/cache/xdg-terminal-exec"
	echo
	echo "== gen_hash reproduced byte-exactly from the tree (x:191-201)"
	HP="$T/home/.config/hyprland-xdg-terminals.list:$T/home/.config/xdg-terminals.list:$T/etc/hyprland-xdg-terminals.list:$T/etc/xdg-terminals.list:$T/usr/share/xdg-terminal-exec/hyprland-xdg-terminals.list:$T/usr/share/xdg-terminal-exec/xdg-terminals.list:$T/usr/share/applications/:$T/data/applications/"
	( echo 4; echo Hyprland; set -f; IFS=':'; LANG=C ls -LRl $HP 2>/dev/null ) | md5sum | awk '{print "recomputed: "$1}'
	echo 'ls stdout that is hashed:'; set -f; IFS=':'; LANG=C ls -LRl $HP 2>/dev/null | cat -A
	echo
	echo "== same-size, same-minute Exec edit: warm answer differs from cold"
	entry bar
	touch -d "@$((PINNED + 20))" "$T/data/applications/foo.desktop"
	echo -n 'warm stdout: '; run "$T/cache" XTE_DEBUG=1 2>"$WORK/warm.err"
	grep -E 'cache is (actual|out-of-date)|invalid cache data' "$WORK/warm.err" || true
	rm -rf "$T/cache2"; mkdir "$T/cache2"
	echo -n 'cold stdout: '; run "$T/cache2"
	sleep 1
	echo
	echo "== /disable_cache reaches the cold path only (it changes the list, hence the hash)"
	printf '/disable_cache\nfoo.desktop\n' > "$T/home/.config/xdg-terminals.list"
	touch -d "@$((PINNED + 40))" "$T/home/.config/xdg-terminals.list"
	echo -n 'stdout: '; run "$T/cache" XTE_DEBUG=1 2>"$WORK/disable.err"
	grep -E 'cache is (actual|out-of-date)|directive|cache is disabled' "$WORK/disable.err" || true
	sleep 1
	echo -n 'cache file after the run: '; ( ls "$T/cache" || true ) | tr '\n' ' '; echo
	echo
	echo "== XTE_CACHE_ENABLED=false ignores a valid cache and removes it"
	rm -rf "$T/cache3"; mkdir "$T/cache3"
	entry foo; printf 'foo.desktop\n' > "$T/home/.config/xdg-terminals.list"
	touch -d "@$PINNED" "$T/data/applications/foo.desktop" "$T/home/.config/xdg-terminals.list"
	run "$T/cache3" > /dev/null; sleep 1
	echo -n 'primed: '; sed -n 1p "$T/cache3/xdg-terminal-exec"
	entry bar; touch -d "@$((PINNED + 20))" "$T/data/applications/foo.desktop"
	echo -n 'stdout with XTE_CACHE_ENABLED=false: '; run "$T/cache3" XTE_CACHE_ENABLED=false 2>"$WORK/enabled.err"
	grep -E 'Assuming|no cache data|cache is disabled' "$WORK/enabled.err" || true
	sleep 1
	echo -n 'cache file after: '; ( ls "$T/cache3" || true ) | tr '\n' ' '; echo
	echo
	echo "== an unreadable cache file is a failed read, not a fatal error"
	rm -rf "$T/cache4"; mkdir "$T/cache4"; entry foo
	touch -d "@$PINNED" "$T/data/applications/foo.desktop"
	run "$T/cache4" > /dev/null; sleep 1
	chmod 000 "$T/cache4/xdg-terminal-exec"
	echo -n 'rc/stdout: '; run "$T/cache4" > "$WORK/u.out" 2> "$WORK/u.err" && echo -n "rc=0 " || echo -n "rc=$? "
	cat "$WORK/u.out"; grep -c 'Permission denied' "$WORK/u.err" | sed 's/^/permission-denied-lines: /'
	chmod 644 "$T/cache4/xdg-terminal-exec"
	echo
	echo "== HOME unset: fatal only where a default must expand (set -u x:23; x:148, x:166, x:172)"
	nohome() { env -i "$@" PATH="$T/bin:/usr/bin:/bin" LC_ALL=C XDG_CURRENT_DESKTOP=Hyprland timeout 10 "$X" --print-cmd; }
	rm -rf "$T/cache5"; mkdir "$T/cache5"; entry foo
	touch -d "@$PINNED" "$T/data/applications/foo.desktop"
	echo -n '(a) all three XDG base vars set: rc='
	nohome XDG_CONFIG_HOME="$T/home/.config" XDG_CONFIG_DIRS="$T/etc" XDG_DATA_HOME="$T/data" XDG_DATA_DIRS="$T/usr/share" XDG_CACHE_HOME="$T/cache5" > "$WORK/h1.out" 2> "$WORK/h1.err" && echo -n '0' || echo -n "$?"
	echo " stdout=[$(cat "$WORK/h1.out")] stderr=[$(cat "$WORK/h1.err")]"
	echo -n '(b) XDG_CONFIG_HOME unset: rc='
	nohome XDG_CONFIG_DIRS="$T/etc" XDG_DATA_HOME="$T/data" XDG_DATA_DIRS="$T/usr/share" XDG_CACHE_HOME="$T/cache5" > "$WORK/h2.out" 2> "$WORK/h2.err" && echo -n '0' || echo -n "$?"
	echo " stdout=[$(cat "$WORK/h2.out")] stderr=[$(cat "$WORK/h2.err")]"
	echo -n '(c) XDG_DATA_HOME unset: rc='
	nohome XDG_CONFIG_HOME="$T/home/.config" XDG_CONFIG_DIRS="$T/etc" XDG_DATA_DIRS="$T/usr/share" XDG_CACHE_HOME="$T/cache5" > "$WORK/h3.out" 2> "$WORK/h3.err" && echo -n '0' || echo -n "$?"
	echo " stdout=[$(cat "$WORK/h3.out")] stderr=[$(cat "$WORK/h3.err")]"
	echo -n '(d) XDG_CACHE_HOME unset: rc='
	nohome XDG_CONFIG_HOME="$T/home/.config" XDG_CONFIG_DIRS="$T/etc" XDG_DATA_HOME="$T/data" XDG_DATA_DIRS="$T/usr/share" > "$WORK/h4.out" 2> "$WORK/h4.err" && echo -n '0' || echo -n "$?"
	echo " stdout=[$(cat "$WORK/h4.out")] stderr=[$(cat "$WORK/h4.err")]"
} > "$R/warm-cache.txt" 2>&1

{
	echo "== ls -LRl in the C locale, non-tty: the bytes that go into the md5"
	mkdir -p "$WORK/links/sub"
	cd "$WORK/links"
	printf 'abc' > real.txt
	ln -sfn real.txt good.link
	ln -sfn missing.txt broken.link
	ln -sfn sub dirlink
	LANG=C ls -LRl . 2>/dev/null | cat -A
	echo '--- stderr:'; LANG=C ls -LRl . 2>&1 >/dev/null | cat -A
	echo
	echo "== symlink loop"
	mkdir -p "$WORK/loop"; cd "$WORK/loop"; rm -f loop; ln -s loop loop
	LANG=C ls -LRl . 2>/dev/null | cat -A
	LANG=C ls -LRl . 2>&1 >/dev/null | cat -A
	echo
	echo "== date form: any future mtime takes the year form; six-month boundary bracketed"
	mkdir -p "$WORK/dates"; cd "$WORK/dates"; rm -f f*
	N=$(date +%s)
	for off in 1 3599 3600 $((15778476-7200)) $((15778476+7200)); do : > "p$off"; touch -d "@$((N-off))" "p$off"; done
	for off in 1 3600; do : > "fut$off"; touch -d "@$((N+off))" "fut$off"; done
	LANG=C ls -l | cat -A
	echo
	echo "== numeric uid/gid when no passwd entry resolves (bwrap, /etc hidden)"
	bwrap --dev-bind / / --tmpfs /etc -- /bin/ls -l "$T/data/applications" | cat -A
} > "$R/ls-listing.txt" 2>&1

rm -f "$WORK/warm.err" "$WORK/disable.err" "$WORK/enabled.err" "$WORK/u.out" "$WORK/u.err"
echo "receipts written under $R"
