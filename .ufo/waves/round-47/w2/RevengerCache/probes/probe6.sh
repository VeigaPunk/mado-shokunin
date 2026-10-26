#!/bin/bash
# Appends the remaining warm/cold comparisons (hotkey shapes, command shape, truncated cache) to
# w2-warm-vs-cold.txt. Print modes only; XDG_CACHE_HOME always inside scratch.
set -u
S=/fast/scratch/hyaku/mado-r47/RevengerCache
R=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w2/RevengerCache
cd "$S" || exit 1
ENVARGS=()
while IFS='=' read -r k v; do case "$k" in HOME|PATH|XDG_*) ENVARGS+=("$k=$v") ;; esac; done < "$S/hyprland.env"
go() { timeout 120 env -i "${ENVARGS[@]}" XDG_CACHE_HOME="$1" "${@:2}"; }

{
echo
echo "## appended by probes/probe6.sh — the remaining argument shapes and a truncated cache file"
echo
echo "### cold with the hotkey's --dir request, this seat's own run"
rm -rf "$S/cJ"; mkdir -p "$S/cJ"
echo "\$ XDG_CACHE_HOME=scratch/empty xdg-terminal-exec --dir=/home/vgpnk --print-id --print-path --print-cmd"
echo "  $(go "$S/cJ" "$S/xte" --dir=/home/vgpnk --print-id --print-path --print-cmd 2>/dev/null | tr '\n' '|')"
echo
echo "### warm cache + a command (Alacritty.desktop has -e in X-TerminalArgExec)"
rm -rf "$S/cK"; mkdir -p "$S/cK"; cp "$HOME/.cache/xdg-terminal-exec" "$S/cK/xdg-terminal-exec"
echo "\$ warm   xdg-terminal-exec --print-cmd -- htop : $(go "$S/cK" "$S/xte" --print-cmd -- htop 2>/dev/null | tr '\n' '|')"
rm -rf "$S/cL"; mkdir -p "$S/cL"
echo "\$ cold   xdg-terminal-exec --print-cmd -- htop : $(go "$S/cL" "$S/xte" --print-cmd -- htop 2>/dev/null | tr '\n' '|')"
echo
echo "### truncated cache (first 3 lines of the host cache, no END_OF_EXEC_USEP terminator)"
rm -rf "$S/cM"; mkdir -p "$S/cM"
head -3 "$HOME/.cache/xdg-terminal-exec" > "$S/cM/xdg-terminal-exec"
echo "\$ sed -n l scratch-cache/xdg-terminal-exec"; sed -n l "$S/cM/xdg-terminal-exec" | sed 's/^/  /'
echo "\$ XTE_DEBUG=1 xdg-terminal-exec --print-id --print-cmd"
echo "  decision: $(go "$S/cM" env XTE_DEBUG=1 "$S/xte" --print-id --print-cmd 2>&1 >/dev/null | grep -E 'invalid cache data|cache is actual|no cache data' | tr '\n' '|')"
echo "  stdout:   $(go "$S/cM" "$S/xte" --print-id --print-cmd 2>/dev/null | tr '\n' '|')"
echo "  cache after the run has the terminator again: $(grep -c 'END_OF_EXEC_USEP' "$S/cM/xdg-terminal-exec" 2>/dev/null)"
} >> "$R/w2-warm-vs-cold.txt"
tail -26 "$R/w2-warm-vs-cold.txt"