#!/bin/bash
# RevengerCache probe 5 — a metadata-preserving config edit also bypasses the cache-control directives,
# because read_cache() (:1179) runs before read_config_paths() (the else branch at :1181+).
set -u
S=/fast/scratch/hyaku/mado-r47/RevengerCache
F=$S/fx5
XTE=$S/xte
rm -rf "$F"; mkdir -p "$F"/{home/.config,home/.local/share/applications,etc,usr/share,bin}
cat > "$F/home/.local/share/applications/TermA.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Term A
Exec=term-a
Terminal=false
X-TerminalArgExec=-e
Categories=System;TerminalEmulator;
EOF
cat > "$F/home/.local/share/applications/TermC.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Term C
Exec=term-c
Terminal=false
X-TerminalArgExec=-e
Categories=System;TerminalEmulator;
EOF
for t in term-a term-c; do printf '#!/bin/sh\nexit 1\n' > "$F/bin/$t"; chmod 755 "$F/bin/$t"; done
L="$F/home/.config/xdg-terminals.list"
E=(HOME="$F/home" PATH="$F/bin:/usr/bin:/bin" XDG_CONFIG_HOME="$F/home/.config" XDG_CONFIG_DIRS="$F/etc"
   XDG_DATA_HOME="$F/home/.local/share" XDG_DATA_DIRS="$F/usr/share" XDG_CURRENT_DESKTOP=Hyprland LANG=C)
hashof() {
	local paths="$F/etc/hyprland-xdg-terminals.list:$F/etc/xdg-terminals.list"
	paths=$paths":$F/home/.config/hyprland-xdg-terminals.list:$F/home/.config/xdg-terminals.list"
	paths=$paths":$F/usr/share/xdg-terminal-exec/hyprland-xdg-terminals.list:$F/usr/share/xdg-terminal-exec/xdg-terminals.list"
	paths=$paths":$F/usr/share/applications/:$F/home/.local/share/applications/"
	{ echo 4; echo Hyprland; IFS=':'; LANG=C LC_ALL=C ls -LRl ${paths} 2> /dev/null; } | md5sum | cut -d' ' -f1
}
run() { local tag=$1 cache=$2; shift 2
	timeout 90 env -i "${E[@]}" XDG_CACHE_HOME="$cache" XTE_DEBUG=1 "$XTE" "$@" > "$S/p5-$tag.out" 2> "$S/p5-$tag.err"
	echo "  [$tag] rc=$? out=$(tr '\n' '|' < "$S/p5-$tag.out")"
}

echo "== T4. config now says /disable_cache and names TermC; a hash-valid cache for the SAME metadata says TermA =="
printf '/disable_cache\nTermC.desktop\n' > "$L"
H=$(hashof); echo "  hash for the new list = $H"
mkdir -p "$F/cache"
printf '%s\n' "$H" 'term-a' "$F/home/.local/share/applications/./TermA.desktop" 'TermA.desktop' '' '-e' '' '' '' '' \
	'term-a'"$(printf '\036')"'END_OF_EXEC_USEP' > "$F/cache/xdg-terminal-exec"
run warm "$F/cache" --print-id --print-path --print-cmd
grep -E 'cache is actual|disable_cache|reading config' "$S/p5-warm.err" | sed 's/^/    /'
echo "  cold control (cache removed):"
rm -f "$F/cache/xdg-terminal-exec"
run cold "$F/cache" --print-id --print-path --print-cmd
grep -E 'no cache data|disable_cache' "$S/p5-cold.err" | sed 's/^/    /'
echo "  cache re-created by the cold run? $(test -f "$F/cache/xdg-terminal-exec" && echo yes || echo no)"
