#!/bin/bash
# Regenerates w6-forgery.txt in the seat dir from the scratch artifacts.
set -u
S=/fast/scratch/hyaku/mado-r47/RevengerCache
R=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w2/RevengerCache
cd "$S" || exit 1
ENVARGS=()
while IFS='=' read -r k v; do case "$k" in HOME|PATH|XDG_*) ENVARGS+=("$k=$v") ;; esac; done < "$S/hyprland.env"
runs() { timeout 120 env -i "${ENVARGS[@]}" XDG_CACHE_HOME="$1" "${@:2}"; }

{
echo "# Forgery / check-vs-use split / write atomicity. Env = the compositor's (/proc/<Hyprland>/environ),"
echo "# XDG_CACHE_HOME in scratch, --print-* only; the host cache was copied by hand, never written."
echo
echo "## A. host hash line verbatim; lines 2/3/4/11 replaced (entry path deliberately nonexistent)"
echo "\$ sed -n '1,4p;11p' cache/xdg-terminal-exec   (XTE__RSEP printed as ^^)"
sed -n '1,4p;11p' "$S/cF/xdg-terminal-exec" | cat -v
echo "\$ xdg-terminal-exec --print-id --print-path --print-cmd"
echo "  stdout: $(runs "$S/cF" "$S/xte" --print-id --print-path --print-cmd 2>/dev/null | tr '\n' '|')"
echo "\$ XTE_DEBUG=1 ... | grep cache/cmd/entry   (stderr)"
runs "$S/cF" env XTE_DEBUG=1 "$S/xte" --print-id --print-path --print-cmd 2>&1 >/dev/null |
	grep -E 'cache is actual|^D: (cmd|entry_path|entry_id|exec_usep)=' | sed 's/^/  /'
echo
echo "## B. check-vs-use split: line2 (validated by command -v) = alacritty, line11 (exec'd) = bash"
echo "\$ xdg-terminal-exec --print-cmd"
echo "  stdout: $(runs "$S/cG" "$S/xte" --print-cmd 2>/dev/null | tr '\n' '|')"
echo
echo "## C. the cache write is a truncating open + separate writes from a forked child (non-atomic)"
grep 'cI/xdg-terminal-exec' "$S/strace2.txt" | grep openat | cut -c1-210 | sed 's/^/  /'
grep 'cI/xdg-terminal-exec' "$S/strace2.txt" | grep 'write(' | cut -c1-132 | sed 's/^/  /'
printf '  sum of bytes in those writes: %s (file size %s)\n' \
	"$(grep 'cI/xdg-terminal-exec' "$S/strace2.txt" | grep 'write(' |
		sed -E 's/.*, ([0-9]+)\) = [0-9]+$/\1/' | paste -sd+ | awk -F+ '{s=0; for(i=1;i<=NF;i++) s+=$i; print s}')" \
	"$(stat -c %s "$S/cI/xdg-terminal-exec")"
} > "$R/w6-forgery.txt" 2>&1
wc -l "$R/w6-forgery.txt"; cat "$R/w6-forgery.txt"