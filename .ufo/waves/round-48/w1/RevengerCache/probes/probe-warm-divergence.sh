#!/bin/sh
# R48 RevengerCache probe 2: warm-vs-cold divergence classes, against the real pinned resolver.
# Runs /usr/bin/xdg-terminal-exec with --print-cmd ONLY (never a launch), XDG_CACHE_HOME inside $S.
set -eu
S=${1:-/fast/scratch/hyaku/mado-r48/RevengerCache/probe-warm}
rm -rf -- "$S"
mkdir -p "$S/config" "$S/cfgdir" "$S/data/applications" "$S/data2/applications" "$S/bin" "$S/cache"
export XDG_CONFIG_HOME="$S/config" XDG_CONFIG_DIRS="$S/cfgdir"
export XDG_DATA_HOME="$S/data" XDG_DATA_DIRS="$S/data2"
export XDG_CACHE_HOME="$S/cache"
export PATH="$S/bin:/usr/bin:/bin"
unset XDG_CURRENT_DESKTOP 2>/dev/null || true
unset XTE_CACHE_ENABLED 2>/dev/null || true
X=/usr/bin/xdg-terminal-exec
C="$S/cache/xdg-terminal-exec"

mk() { # name exec
	printf '[Desktop Entry]\nType=Application\nName=%s\nTerminal=true\nCategories=System;TerminalEmulator;\nX-TerminalArgExec=-e\nExec=%s --flag\n' "$1" "$2"
}
wait_cache() { i=0; while [ ! -f "$C" ] && [ "$i" -lt 100 ]; do sleep 0.05; i=$((i+1)); done; }

printf 'termA.desktop\n' > "$S/config/xdg-terminals.list"
mk A termA > "$S/data/applications/termA.desktop"
mk B termB > "$S/data/applications/termB.desktop"
for t in termA termB termC; do printf '#!/bin/sh\nexit 0\n' > "$S/bin/$t"; chmod +x "$S/bin/$t"; done

echo "== prime (cold, --print-cmd)"; "$X" --print-cmd; wait_cache
echo "-- cache header, lines 1-5:"; sed -n '1,5p' "$C"

echo
echo "== class 1: entry edited, size and mtime minute unchanged"
cp -a "$S/data/applications/termA.desktop" "$S/x.snap"
mk A termC > "$S/data/applications/termA.desktop"
touch -r "$S/x.snap" "$S/data/applications/termA.desktop"
echo "   sizes: $(wc -c < "$S/x.snap") -> $(wc -c < "$S/data/applications/termA.desktop")"
printf '   warm: '; "$X" --print-cmd | tr '\n' ' '; echo
mv "$C" "$S/held"; printf '   cold: '; "$X" --print-cmd | tr '\n' ' '; echo; mv "$S/held" "$C"

echo
echo "== class 2: TryExec stub removed; entries and PATH (not hashed) diverge"
mk A termA > "$S/data/applications/termA.desktop"
printf 'TryExec=stubXYZ\n' >> "$S/data/applications/termA.desktop"
printf '#!/bin/sh\nexit 0\n' > "$S/bin/stubXYZ"; chmod +x "$S/bin/stubXYZ"
rm -f "$C"; "$X" --print-cmd > /dev/null; wait_cache
rm -f "$S/bin/stubXYZ"
printf '   warm (stub gone): '; "$X" --print-cmd | tr '\n' ' '; echo
mv "$C" "$S/held"; printf '   cold (stub gone): '; "$X" --print-cmd | tr '\n' ' '; echo; mv "$S/held" "$C"

echo
echo "== class 3: a warm hit never rewrites the cache"
m1=$(stat -c %Y "$C"); sleep 1.1; "$X" --print-cmd > /dev/null; m2=$(stat -c %Y "$C")
echo "   mtime ${m1} -> ${m2}  identical=$([ "$m1" = "$m2" ] && echo yes || echo no)"

echo
echo "== class 4: XTE_CACHE_ENABLED=false deletes the cache file"
"$X" --print-cmd > /dev/null; printf '   before: %s\n' "$([ -f "$C" ] && echo present || echo absent)"
XTE_CACHE_ENABLED=false "$X" --print-cmd | tr '\n' ' '; echo
printf '   after : %s\n' "$([ -f "$C" ] && echo present || echo absent)"

echo
echo "== class 5: issue #47 - /disable_cache in the list is ignored while a valid cache exists"
printf '/disable_cache\ntermA.desktop\n' > "$S/config/xdg-terminals.list"
XTE_CACHE_ENABLED=1 "$X" --print-cmd > /dev/null; wait_cache
printf '   primed with XTE_CACHE_ENABLED=1: %s\n' "$([ -f "$C" ] && echo present || echo absent)"
printf '   run with the env unset, config still /disable_cache: '; "$X" --print-cmd | tr '\n' ' '; echo
printf '   cache after: %s\n' "$([ -f "$C" ] && echo present || echo absent)"
printf '   verdict: '; DEBUG=1 "$X" --print-cmd 2>&1 >/dev/null | grep -m1 -E 'cache is (actual|out-of-date)|no cache data|invalid cache data'
printf 'termA.desktop\n' > "$S/config/xdg-terminals.list"

echo
echo "== class 6: HOME unset"
env -u HOME -u XDG_CONFIG_HOME -u XDG_CONFIG_DIRS -u XDG_DATA_HOME -u XDG_DATA_DIRS -u XDG_CACHE_HOME \
	"$X" --print-cmd > "$S/o" 2> "$S/e" && rc=0 || rc=$?
printf '   HOME+XDG unset: rc=%s stdout=%sB stderr=%s\n' "$rc" "$(wc -c < "$S/o")" "$(head -c 90 "$S/e")"
env -u HOME "$X" --print-cmd > "$S/o2" 2> "$S/e2" && rc=0 || rc=$?
printf '   HOME unset, XDG set: rc=%s stdout=%sB\n' "$rc" "$(wc -c < "$S/o2")"

echo
echo "== class 7: PATH identity is not in the key (same name, different binary)"
mkdir -p "$S/bin1" "$S/bin2"
mk A termP > "$S/data/applications/termA.desktop"
printf '#!/bin/sh\necho ONE\n' > "$S/bin1/termP"; chmod +x "$S/bin1/termP"
printf '#!/bin/sh\necho TWO\n' > "$S/bin2/termP"; chmod +x "$S/bin2/termP"
rm -f "$C"
printf '   prime under bin1: '; PATH="$S/bin1:/usr/bin:/bin" "$X" --print-cmd | tr '\n' ' '; echo
wait_cache
printf '   warm under bin2 : '; PATH="$S/bin2:/usr/bin:/bin" "$X" --print-cmd | tr '\n' ' '; echo
printf '   verdict         : '; PATH="$S/bin2:/usr/bin:/bin" DEBUG=1 "$X" --print-cmd 2>&1 >/dev/null | grep -m1 -E 'cache is (actual|out-of-date)|no cache data'

echo
echo "== class 8: the cached command name disappears from PATH"
rm -f "$C"; PATH="$S/bin2:/usr/bin:/bin" "$X" --print-cmd > /dev/null; wait_cache
mv "$S/bin2/termP" "$S/bin2/termP.off"
printf '   warm (name gone): '; PATH="$S/bin2:/usr/bin:/bin" "$X" --print-cmd | tr '\n' ' '; echo
printf '   verdict         : '; PATH="$S/bin2:/usr/bin:/bin" DEBUG=1 "$X" --print-cmd 2>&1 >/dev/null | grep -m1 -E 'cache is (actual|out-of-date)|no cache data'
mv "$S/bin2/termP.off" "$S/bin2/termP"
PATH="$S/bin1:/usr/bin:/bin"
mk A termA > "$S/data/applications/termA.desktop"
