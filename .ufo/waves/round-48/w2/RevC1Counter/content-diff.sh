#!/usr/bin/env bash
# Warm HIT whose cached entry differs from the cold selection, on a --print-content case.
# Pin runs are read-only print modes with XDG_CACHE_HOME inside this scratch (host guard satisfied).
set -eu
ulimit -f 2048
S=/fast/scratch/hyaku/mado-r48/RevC1Counter/diff
PIN=/fast/scratch/hyaku/mado-r48/RevC1Counter/pin/xdg-terminal-exec
SRC=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/fetch/xdg-terminal-exec
REF=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/l1-draft/mado-terminal.py
MUT=/fast/scratch/hyaku/mado-r48/RevC1Counter/mut/content-cold.py
test "$(sha256sum "$SRC" | cut -d" " -f1)" = 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac
rm -rf "$S"; mkdir -p "$S/R/home/.config" "$S/R/etc/xdg" "$S/R/home/.local/share" "$S/R/usr/share/applications" "$S/R/cache"
R=$S/R
printf '[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nName=alpha\nExec=alpha\n' > "$R/usr/share/applications/alpha.desktop"
printf '[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nName=bravo\nExec=bravo\n' > "$R/usr/share/applications/bravo.desktop"
printf 'alpha.desktop\n' > "$R/home/.config/xdg-terminals.list"
: > "$R/bin_placeholder"
mkdir -p "$R/bin"; printf '#!/bin/sh\nexit 1\n' > "$R/bin/alpha"; chmod 755 "$R/bin/alpha"
printf '#!/bin/sh\nexit 1\n' > "$R/bin/bravo"; chmod 755 "$R/bin/bravo"
E="HOME=$R/home PATH=$R/bin:/usr/bin:/bin LANG=C.UTF-8 XDG_CONFIG_HOME=$R/home/.config XDG_CONFIG_DIRS=$R/etc/xdg XDG_DATA_HOME=$R/home/.local/share XDG_DATA_DIRS=$R/usr/share XDG_CACHE_HOME=$R/cache XDG_CURRENT_DESKTOP=Hyprland"
rm -f "$R/bin_placeholder"
find "$R" -path "$R/cache" -prune -o -print0 | xargs -0 touch -h -d @1600000000
echo "== prime (pin --print-cmd)"
env -i $E "$PIN" --print-cmd; echo "prime rc=$?"
n=0; while [ $n -lt 400 ]; do if [ -f "$R/cache/xdg-terminal-exec" ] && tail -c 40 "$R/cache/xdg-terminal-exec" | grep -q 'END_OF_EXEC_USEP'; then break; fi; n=$((n+1)); done
echo "== cache lines: $(wc -l < "$R/cache/xdg-terminal-exec")"; sed -n '1,11p' "$R/cache/xdg-terminal-exec" | cat -v | cut -c1-120
echo "== same-size list edit alpha.desktop -> bravo.desktop (13+NL bytes each), mtime re-pinned"
printf 'bravo.desktop\n' > "$R/home/.config/xdg-terminals.list"
touch -d @1600000000 "$R/home/.config/xdg-terminals.list" "$R/home/.config"
echo "== pin --print-content (oracle)"
env -i $E XTE_DEBUG=1 "$PIN" --print-content 2>"$S/pin.err"; echo "pin rc=$?"
grep -E 'cache is' "$S/pin.err" || true
echo "== pin --print-id (what the cold path would select now)"
env -i $E "$PIN" --print-id; echo "cold-id rc=$?"
echo "== pin --print-content with cache disabled (the cold answer)"
env -i $E XTE_CACHE_ENABLED=false "$PIN" --print-content; echo "cold-content rc=$?"
echo "== frozen reference tool"
env -i $E python3 -I "$REF" print --print-content; echo "ref rc=$?"
echo "== content-cold mutant"
env -i $E python3 -I "$MUT" print --print-content; echo "mut rc=$?"
echo "== mutant explain cache="
env -i $E python3 -I "$MUT" explain | grep '^MADO_TERM:'
