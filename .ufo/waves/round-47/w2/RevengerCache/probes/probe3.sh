#!/bin/bash
# RevengerCache probe 3 — three tests of the cache's semantics, all inside scratch, print modes only.
#  T1 metadata-only coverage: a same-size, mtime-restored edit of the list file leaves the hash valid
#     -> warm cache returns the OLD terminal while a cold resolve returns the NEW one.
#  T2 trust-free input: a cache whose command/entry lines are swapped for arbitrary values is accepted
#     (only the hash and `command -v` of the cached cmd are checked); entry path is never validated.
#  T3 writer-shape witness: which print-mode combination writes the entry-path line with the '/./' marker.
set -u
S=/fast/scratch/hyaku/mado-r47/RevengerCache
F=$S/fx
XTE=$S/xte
rm -rf "$F"; mkdir -p "$F"/{home/.config,home/.local/share/applications,etc,usr/share,bin,cache}

mk_home() {
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
	printf '%s\n' 'TermA.desktop' > "$F/home/.config/xdg-terminals.list"
	for t in term-a term-b term-c; do printf '#!/bin/sh\nexit 1\n' > "$F/bin/$t"; chmod 755 "$F/bin/$t"; done
}
E=(
	HOME="$F/home"
	PATH="$F/bin:/usr/bin:/bin"
	XDG_CONFIG_HOME="$F/home/.config"
	XDG_CONFIG_DIRS="$F/etc"
	XDG_DATA_HOME="$F/home/.local/share"
	XDG_DATA_DIRS="$F/usr/share"
	XDG_CURRENT_DESKTOP=Hyprland
	LANG=C
)
res() { # tag cachedir args...
	local tag=$1 cache=$2; shift 2
	timeout 90 env -i "${E[@]}" XDG_CACHE_HOME="$cache" XTE_DEBUG=1 "$XTE" "$@" > "$S/$tag.out" 2> "$S/$tag.err"
	echo "  [$tag] rc=$? out=$(tr '\n' '|' < "$S/$tag.out")"
}
hashof() {
	local paths="$F/etc/hyprland-xdg-terminals.list:$F/etc/xdg-terminals.list"
	paths=$paths":$F/home/.config/hyprland-xdg-terminals.list:$F/home/.config/xdg-terminals.list"
	paths=$paths":$F/usr/share/xdg-terminal-exec/hyprland-xdg-terminals.list:$F/usr/share/xdg-terminal-exec/xdg-terminals.list"
	paths=$paths":$F/usr/share/applications/:$F/home/.local/share/applications/"
	{
		echo 4; echo Hyprland
		IFS=':'
		# shellcheck disable=SC2086
		LANG=C LC_ALL=C ls -LRl ${paths} 2> /dev/null
	} | md5sum | cut -d' ' -f1
}

mk_home
echo "== T0. seed a cache with a cold run; confirm hash reproducibility =="
res seed1 "$F/cache/seed1" --print-id --print-path --print-cmd
echo "  recomputed_hash=$(hashof)"
echo "  cache_line1    =$(head -1 "$F/cache/seed1/xdg-terminal-exec" 2>/dev/null)"

echo
echo "== T1. same-size, mtime-restored list edit -> warm cache vs cold resolve =="
L="$F/home/.config/xdg-terminals.list"
MT=$(stat -c '%y' "$L"); SZ=$(stat -c '%s' "$L")
printf '%s\n' 'TermC.desktop' > "$L"          # TermA->TermC: identical length, no other change
touch -d "$MT" "$L"
echo "  list size before=$SZ after=$(stat -c '%s' "$L"); mtime restored=$(stat -c '%y' "$L" | cut -c1-19)"
echo "  hash now=$(hashof)  (cache line1=$(head -1 "$F/cache/seed1/xdg-terminal-exec"))"
res warmT1 "$F/cache/seed1" --print-id --print-path --print-cmd
res coldT1 "$F/cache/coldT1" --print-id --print-path --print-cmd
grep -E 'cache is actual|cache is out-of-date|no cache data' "$S/warmT1.err" "$S/coldT1.err" | sed 's/^/  /'

echo
echo "== T2. forged command/entry lines under a valid hash =="
C="$F/cache/seed1/xdg-terminal-exec"
mkdir -p "$F/cache/forged"
printf '%s\n' "$(head -1 "$C")" 'term-b' '/nonexistent/Evil.desktop' 'Evil.desktop' '' '-e' '' '' '' '' \
	'term-b'"$(printf '\036')"'END_OF_EXEC_USEP' > "$F/cache/forged/xdg-terminal-exec"
res forged "$F/cache/forged" --print-id --print-path --print-cmd
grep -E 'cache is actual|cache is out-of-date' "$S/forged.err" | sed 's/^/  /'

echo
echo "== T3. writer-shape witness: does the saved entry-path line carry '/./'? =="
mk_home   # pristine tree again
res w_idcmd "$F/cache/w_idcmd" --print-id --print-cmd
res w_full  "$F/cache/w_full"  --print-id --print-path --print-cmd
for t in w_idcmd w_full; do
	printf '  %-7s line3=%s\n' "$t" "$(sed -n 3p "$F/cache/$t/xdg-terminal-exec" 2>/dev/null)"
done
echo "  code: the ONLY place XTE__ENTRY_PATH loses '/./' is the --print-path branch (:1342);"
echo "  save_cache (:1455) runs later, so a run without --print-path (a launch) saves the '/./' form."
