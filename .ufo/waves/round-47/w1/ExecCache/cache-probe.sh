#!/bin/sh
# cache-probe.sh — hermetic probes of the xdg-terminal-exec 0.14.3 resolver cache.
# usage: cache-probe.sh WORKDIR
# Writes everything to WORKDIR/probe.log. Never launches a terminal: only --print-* modes,
# XDG_CACHE_HOME always inside WORKDIR.
set -u
WORK=${1:?usage: cache-probe.sh WORKDIR}
XTE=/usr/bin/xdg-terminal-exec
ROOT=$WORK/case
CACHE=$ROOT/cache
CF=$CACHE/xdg-terminal-exec
LOG=$WORK/probe.log
: > "$LOG"
exec >>"$LOG" 2>&1

DESKTOP=Hyprland
TZ_OVERRIDE=
XTE_DEBUG=
XTE_CACHE_ENABLED=

say() { printf '\n===== %s =====\n' "$*"; }
cmd() { printf '\n$ %s\n' "$*"; }

setup() {
	rm -rf "$ROOT"
	mkdir -p "$ROOT/home/.config" "$ROOT/home/.local/share/applications" \
		"$ROOT/usr/share/applications" "$ROOT/etc/xdg" "$CACHE" "$ROOT/bin"
	for b in term-a term-b; do
		printf '#!/bin/sh\nexit 0\n' > "$ROOT/bin/$b"
		chmod 755 "$ROOT/bin/$b"
	done
	cat > "$ROOT/home/.local/share/applications/TermA.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Term A
Exec=term-a
Categories=System;TerminalEmulator;
EOF
	cat > "$ROOT/home/.local/share/applications/TermB.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Term B
Exec=term-b
Categories=System;TerminalEmulator;
EOF
	printf 'TermA.desktop\nTermB.desktop\n' > "$ROOT/home/.config/xdg-terminals.list"
}

# run <args...> with a fully controlled environment; honours the override vars above
run() {
	env -i HOME="$ROOT/home" PATH="$ROOT/bin:/usr/bin:/bin" \
		XDG_CURRENT_DESKTOP="$DESKTOP" \
		XDG_CONFIG_HOME="$ROOT/home/.config" XDG_CONFIG_DIRS="$ROOT/etc/xdg" \
		XDG_DATA_HOME="$ROOT/home/.local/share" XDG_DATA_DIRS="$ROOT/usr/share" \
		XDG_CACHE_HOME="$CACHE" \
		${TZ_OVERRIDE:+TZ="$TZ_OVERRIDE"} \
		${XTE_DEBUG:+XTE_DEBUG="$XTE_DEBUG"} \
		${XTE_CACHE_ENABLED:+XTE_CACHE_ENABLED="$XTE_CACHE_ENABLED"} \
		"$XTE" "$@"
}

# cold <outfile> <args...> : drop the cache, run, wait for the forked save_cache
cold() {
	_out=$1; shift
	rm -f "$CF"
	run "$@" > "$_out" 2> "$_out.err"
	_rc=$?
	sleep 0.4
	return $_rc
}

# warm <outfile> <args...> : run with whatever cache exists
warm() {
	_out=$1; shift
	run "$@" > "$_out" 2> "$_out.err"
	return $?
}

# the exact hashed path set, in make_paths order (CONFIGS then APPLICATIONS_DIRS)
hash_paths() {
	printf '%s\n' \
		"$ROOT/home/.config/hyprland-xdg-terminals.list" \
		"$ROOT/home/.config/xdg-terminals.list" \
		"$ROOT/etc/xdg/hyprland-xdg-terminals.list" \
		"$ROOT/etc/xdg/xdg-terminals.list" \
		"$ROOT/usr/share/xdg-terminal-exec/hyprland-xdg-terminals.list" \
		"$ROOT/usr/share/xdg-terminal-exec/xdg-terminals.list" \
		"$ROOT/usr/share/applications/" \
		"$ROOT/home/.local/share/applications/"
}

repro_hash() {
	{ echo 4; echo "$DESKTOP"; env LC_ALL=C LANG=C ls -LRl $(hash_paths) 2> /dev/null; } |
		md5sum | cut -d' ' -f1
}

show_cache() {
	if [ -f "$CF" ]; then
		printf '%s\n' '--- cache file (sed -n l) ---'
		sed -n l "$CF"
		stat -c 'mode=%a size=%s mtime=%Y' "$CF"
	else
		printf '%s\n' '--- cache file absent ---'
	fi
}

show_debug() { grep -E 'cache|hash|got cache' "$1" || true; }

fail=0
ck() { # ck <label> <cmd...>
	_l=$1; shift
	if "$@"; then printf 'PASS: %s\n' "$_l"; else printf 'FAIL: %s\n' "$_l"; fail=$((fail + 1)); fi
}

say "pins"
sha256sum "$XTE"
wc -l "$XTE"
printf 'all resolver runs below use --print-* modes with XDG_CACHE_HOME inside WORKDIR\n'

say "E0 cold run writes cache; warm run is byte-identical"
setup
XTE_DEBUG=1
cold "$WORK/e0.cold" --print-id --print-path --print-cmd
rc_cold=$?
cp "$WORK/e0.cold.err" "$WORK/e0.cold.debug"
XTE_DEBUG=
printf 'cold rc=%s stdout:\n' "$rc_cold"; cat "$WORK/e0.cold"
show_cache
hash1=$(sed -n 1p "$CF")
printf 'cold computed hash (debug): '; grep -o "got fresh hash '[0-9a-f]*'" "$WORK/e0.cold.debug" || true
printf 'reproduced hash:        %s\n' "$(repro_hash)"
printf 'cache line 1:           %s\n' "$hash1"
ck "reproduced hash equals cache hash" [ "$(repro_hash)" = "$hash1" ]
sleep 0.2
warm "$WORK/e0.warm" --print-id --print-path --print-cmd
ck "warm stdout byte-identical to cold" cmp -s "$WORK/e0.cold" "$WORK/e0.warm"
XTE_DEBUG=1 warm "$WORK/e0.warm2" --print-id --print-path --print-cmd
printf '%s\n' '--- warm debug (cache lines) ---'; show_debug "$WORK/e0.warm2.err"
ck "warm run reports cache is actual" grep -q 'cache is actual' "$WORK/e0.warm2.err"
ck "cold run parsed the config list files" grep -q 'reading config' "$WORK/e0.cold.debug"
ck "warm run never parses config list files" sh -c "! grep -q 'reading config' '$WORK/e0.warm2.err'"
XTE_DEBUG=
printf 'stdout: '; cat "$WORK/e0.warm"

say "E1 stale cache vs cold run after PATH-only change (no hashed input changes)"
setup
rm -f "$ROOT/bin/term-a"          # TermA (higher preference) not runnable yet
cold "$WORK/e1.cold1" --print-id --print-path --print-cmd
printf 'cold #1 (term-a absent) rc=%s:\n' "$?"; cat "$WORK/e1.cold1"
h_before=$(sed -n 1p "$CF")
printf '#!/bin/sh\nexit 0\n' > "$ROOT/bin/term-a"; chmod 755 "$ROOT/bin/term-a"  # bin/ is not hashed
XTE_DEBUG=1 warm "$WORK/e1.warm" --print-id --print-path --print-cmd
printf 'warm (term-a now present) stdout:\n'; cat "$WORK/e1.warm"
show_debug "$WORK/e1.warm.err"
ck "warm run reports cache is actual after PATH change" grep -q 'cache is actual' "$WORK/e1.warm.err"
warm "$WORK/e1.idonly" --print-id
printf 'stale --print-id only: '; cat "$WORK/e1.idonly"
ck "stale cache answers --print-id too" grep -qx 'TermB.desktop' "$WORK/e1.idonly"
XTE_DEBUG= cold "$WORK/e1.cold2" --print-id --print-path --print-cmd
h_after=$(sed -n 1p "$CF")
printf 'cold #2 (same files, term-a present) stdout:\n'; cat "$WORK/e1.cold2"
printf 'hash cold#1=%s\nhash cold#2=%s\n' "$h_before" "$h_after"
ck "hash unchanged across PATH change" [ "$h_before" = "$h_after" ]
ck "warm output DIFFERS from cold #2" sh -c "! cmp -s '$WORK/e1.warm' '$WORK/e1.cold2'"

say "E2 stale cache after content-only edit with size+mtime restored"
setup
cold "$WORK/e2.cold1" --print-id --print-path --print-cmd
printf 'cold #1 stdout:\n'; cat "$WORK/e2.cold1"
h_before=$(sed -n 1p "$CF")
env LC_ALL=C LANG=C ls -LRl $(hash_paths) 2> /dev/null > "$WORK/e2.ls.before"
cp -p "$ROOT/home/.local/share/applications/TermA.desktop" "$WORK/e2.ref"
stat -c 'TermA before: size=%s mtime=%Y' "$ROOT/home/.local/share/applications/TermA.desktop"
# same-length content edit: 'Categories=...' -> '#ategories=...' (line becomes a comment)
sed -i 's/^Categories=/#ategories=/' "$ROOT/home/.local/share/applications/TermA.desktop"
touch -r "$WORK/e2.ref" "$ROOT/home/.local/share/applications/TermA.desktop"
stat -c 'TermA after:  size=%s mtime=%Y' "$ROOT/home/.local/share/applications/TermA.desktop"
env LC_ALL=C LANG=C ls -LRl $(hash_paths) 2> /dev/null > "$WORK/e2.ls.after"
ck "ls -LRl listing byte-identical after content edit" cmp -s "$WORK/e2.ls.before" "$WORK/e2.ls.after"
XTE_DEBUG=1 warm "$WORK/e2.warm" --print-id --print-path --print-cmd
printf 'warm (cache from before edit) stdout:\n'; cat "$WORK/e2.warm"
show_debug "$WORK/e2.warm.err"
ck "warm run reports cache is actual after content edit" grep -q 'cache is actual' "$WORK/e2.warm.err"
XTE_DEBUG= cold "$WORK/e2.cold2" --print-id --print-path --print-cmd
h_after=$(sed -n 1p "$CF")
printf 'cold #2 (fresh cache) stdout:\n'; cat "$WORK/e2.cold2"
ck "hash identical before/after content edit" [ "$h_before" = "$h_after" ]
ck "warm output DIFFERS from cold #2" sh -c "! cmp -s '$WORK/e2.warm' '$WORK/e2.cold2'"

say "E3 corrupt cache variants (each starts from a valid cache selecting TermA/term-a)"
fresh_valid() {
	setup
	cold "$WORK/e3.base" --print-id --print-path --print-cmd
}
base_out=$(cat "$WORK/e3.base" 2> /dev/null || true)

fresh_valid
printf '%s\n' '-- (a) truncated to 5 lines'
sed -n '1,5p' "$CF" > "$WORK/t"; mv "$WORK/t" "$CF"
XTE_DEBUG=1 warm "$WORK/e3a.out" --print-id --print-path --print-cmd
show_debug "$WORK/e3a.out.err"
printf 'stdout:\n'; cat "$WORK/e3a.out"
ck "(a) truncated cache yields same output as cold" cmp -s "$WORK/e3a.out" "$WORK/e3.base"
ck "(a) cache rewritten valid after run" [ -s "$CF" ]

fresh_valid
printf '%s\n' '-- (b) 55 lines, no terminator (line limit 50)'
sed -i '$d' "$CF"                              # drop RS terminator line
awk 'BEGIN{for(i=0;i<45;i++) print "junk-line-" i}' >> "$CF"   # 10 + 45 = 55 lines
XTE_DEBUG=1 warm "$WORK/e3b.out" --print-id --print-path --print-cmd
show_debug "$WORK/e3b.out.err"
ck "(b) over-long cache falls back to cold result" cmp -s "$WORK/e3b.out" "$WORK/e3.base"
ck "(b) line-limit debug seen" grep -q 'reached cache line limit' "$WORK/e3b.out.err"

fresh_valid
printf '%s\n' '-- (c) wrong hash (32 hex chars)'
sed -i '1s/.*/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/' "$CF"
XTE_DEBUG=1 warm "$WORK/e3c.out" --print-id --print-path --print-cmd
show_debug "$WORK/e3c.out.err"
ck "(c) hash mismatch falls back to cold result" cmp -s "$WORK/e3c.out" "$WORK/e3.base"
ck "(c) out-of-date debug seen" grep -q 'cache is out-of-date' "$WORK/e3c.out.err"

fresh_valid
printf '%s\n' '-- (d) missing RS terminator on last line'
sed -i '$s/\x1eEND_OF_EXEC_USEP$//' "$CF"
XTE_DEBUG=1 warm "$WORK/e3d.out" --print-id --print-path --print-cmd
show_debug "$WORK/e3d.out.err"
ck "(d) unterminated cache falls back to cold result" cmp -s "$WORK/e3d.out" "$WORK/e3.base"
ck "(d) invalid-cache debug seen" grep -q 'invalid cache data' "$WORK/e3d.out.err"

fresh_valid
printf '%s\n' '-- (e) forged fields, hash kept (id/path/cmd replaced)'
hash_line=$(sed -n 1p "$CF")
printf '#!/bin/sh\nexit 0\n' > "$ROOT/bin/term-zz"; chmod 755 "$ROOT/bin/term-zz"
awk -v h="$hash_line" -v p="$ROOT/home/.local/share/applications/Evil.desktop" '
	NR==1 { print h; next }
	NR==2 { print "term-zz"; next }
	NR==3 { print p; next }
	NR==4 { print "Evil.desktop"; next }
	{ print }' "$CF" > "$WORK/t"; mv "$WORK/t" "$CF"
XTE_DEBUG=1 warm "$WORK/e3e.out" --print-id --print-path --print-cmd
show_debug "$WORK/e3e.out.err"
printf 'stdout:\n'; cat "$WORK/e3e.out"
ck "(e) forged cache accepted (cache is actual)" grep -q 'cache is actual' "$WORK/e3e.out.err"
ck "(e) forged output DIFFERS from cold result" sh -c "! cmp -s '$WORK/e3e.out' '$WORK/e3.base'"

fresh_valid
printf '%s\n' '-- (f) cached cmd no longer on PATH (hash still matches)'
rm -f "$ROOT/bin/term-a"
XTE_DEBUG=1 warm "$WORK/e3f.out" --print-id --print-path --print-cmd
show_debug "$WORK/e3f.out.err"
printf 'stdout:\n'; cat "$WORK/e3f.out"
ck "(f) missing cached cmd invalidates cache" grep -q 'cache is out-of-date' "$WORK/e3f.out.err"
cold "$WORK/e3f.cold" --print-id --print-path --print-cmd
ck "(f) warm output equals what a cold run now yields" cmp -s "$WORK/e3f.out" "$WORK/e3f.cold"
ck "(f) selection moved TermA -> TermB after the PATH change" sh -c "grep -q 'TermB.desktop' '$WORK/e3f.out'"

say "E4 enable/disable and default cache location"
setup
XTE_CACHE_ENABLED=false cold "$WORK/e4a.out" --print-cmd
printf 'cold with XTE_CACHE_ENABLED=false rc=%s stdout:' "$?"; cat "$WORK/e4a.out"
ck "cache file absent when disabled" [ ! -e "$CF" ]
XTE_CACHE_ENABLED=
setup
cold "$WORK/e4b.cold" --print-id --print-path --print-cmd
ck "cache exists before disable" [ -s "$CF" ]
XTE_CACHE_ENABLED=false warm "$WORK/e4b.warm" --print-cmd
sleep 0.4
ck "valid cache + disabled: cache file removed" [ ! -e "$CF" ]
XTE_CACHE_ENABLED=
setup
printf '/disable_cache\nTermA.desktop\nTermB.desktop\n' > "$ROOT/home/.config/xdg-terminals.list"
cold "$WORK/e4c.out" --print-cmd
ck "config /disable_cache on cold path leaves no cache" [ ! -e "$CF" ]
# default location: no XDG_CACHE_HOME
setup
env -i HOME="$ROOT/home" PATH="$ROOT/bin:/usr/bin:/bin" XDG_CURRENT_DESKTOP=Hyprland \
	XDG_CONFIG_HOME="$ROOT/home/.config" XDG_CONFIG_DIRS="$ROOT/etc/xdg" \
	XDG_DATA_HOME="$ROOT/home/.local/share" XDG_DATA_DIRS="$ROOT/usr/share" \
	"$XTE" --print-cmd > "$WORK/e4d.out" 2> /dev/null
sleep 0.4
ck "default cache path is \$HOME/.cache/xdg-terminal-exec" [ -s "$ROOT/home/.cache/xdg-terminal-exec" ]

say "E5 metadata invalidations (mtime, desktop, TZ)"
setup
cold "$WORK/e5.cold" --print-cmd
env LC_ALL=C LANG=C ls -LRl $(hash_paths) 2> /dev/null > "$WORK/e5.ls.1"
mtime=$(stat -c %Y "$ROOT/home/.local/share/applications/TermB.desktop")
touch -d "$(date -d "@$mtime" +%Y-%m-%dT%H:%M:00)" "$ROOT/home/.local/share/applications/TermB.desktop"
env LC_ALL=C LANG=C ls -LRl $(hash_paths) 2> /dev/null > "$WORK/e5.ls.2"
ck "sub-minute mtime change is invisible to ls -l" cmp -s "$WORK/e5.ls.1" "$WORK/e5.ls.2"
XTE_DEBUG=1 warm "$WORK/e5.same" --print-cmd
ck "sub-minute mtime change keeps cache actual" grep -q 'cache is actual' "$WORK/e5.same.err"
XTE_DEBUG=
touch -t 200001010000 "$ROOT/home/.local/share/applications/TermB.desktop"
XTE_DEBUG=1 warm "$WORK/e5.oldmtime" --print-cmd
ck "displayed-minute mtime change invalidates cache" grep -q 'cache is out-of-date' "$WORK/e5.oldmtime.err"
XTE_DEBUG=
cold "$WORK/e5.cold2" --print-cmd
DESKTOP=GNOME XTE_DEBUG=1 warm "$WORK/e5.desk" --print-cmd
ck "XDG_CURRENT_DESKTOP change invalidates cache" grep -q 'cache is out-of-date' "$WORK/e5.desk.err"
DESKTOP=Hyprland
cold "$WORK/e5.cold3" --print-cmd
TZ_OVERRIDE=UTC cold "$WORK/e5.tz1" --print-cmd
TZ_OVERRIDE=Asia/Tokyo XTE_DEBUG=1 warm "$WORK/e5.tz2" --print-cmd
ck "TZ change invalidates cache (ls -l timestamps are hashed)" grep -q 'cache is out-of-date' "$WORK/e5.tz2.err"
printf 'TZ=Asia/Tokyo warm stdout: '; cat "$WORK/e5.tz2"
TZ_OVERRIDE=

say "E6 cached terminal-side args are replayed; CLI args are recomposed"
setup
cat > "$ROOT/home/.local/share/applications/TermA.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Term A
Exec=term-a
Categories=System;TerminalEmulator;
X-TerminalArgTitle=--title
EOF
cold "$WORK/e6.cold" --print-id --print-cmd --title=First
printf 'cold --title=First:\n'; cat "$WORK/e6.cold"
show_cache
warm "$WORK/e6.warm" --print-id --print-cmd --title=Second
printf 'warm --title=Second (cached titlearg, fresh value):\n'; cat "$WORK/e6.warm"
ck "warm titlearg replayed from cache with fresh CLI value" sh -c "grep -qx -- '--title' '$WORK/e6.warm' && grep -qx 'Second' '$WORK/e6.warm'"
printf 'titlearg line in cache: '; sed -n 8p "$CF"

say "E7 which print modes write the cache"
setup
run --print-id > /dev/null 2>&1; sleep 0.3
ck "--print-id alone writes no cache" [ ! -e "$CF" ]
run --print-path > /dev/null 2>&1; sleep 0.3
ck "--print-path alone writes no cache" [ ! -e "$CF" ]
run --print-content > /dev/null 2>&1; sleep 0.3
ck "--print-content alone writes no cache" [ ! -e "$CF" ]
run --print-cmd > /dev/null 2>&1; sleep 0.3
ck "--print-cmd writes the cache" [ -s "$CF" ]

say "E8 background save race + file mode"
setup
seen=0; late=0; partial=0
for i in $(seq 1 30); do
	rm -f "$CF"
	run --print-cmd > /dev/null 2>&1
	if [ -f "$CF" ]; then
		seen=$((seen + 1))
		grep -q 'END_OF_EXEC_USEP' "$CF" || partial=$((partial + 1))
	fi
	sleep 0.05
	[ -f "$CF" ] && late=$((late + 1))
done
printf 'cache present immediately after exit: %s/30 (incomplete: %s)\n' "$seen" "$partial"
printf 'cache present 50ms after exit:        %s/30\n' "$late"
[ -f "$CF" ] && stat -c 'mode=%a size=%s' "$CF"

say "summary"
printf 'checks failed: %s\n' "$fail"
[ "$fail" -eq 0 ] && printf 'PROBE_RESULT: all checks passed\n' || printf 'PROBE_RESULT: %s check(s) failed\n' "$fail"
