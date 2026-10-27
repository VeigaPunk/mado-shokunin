#!/bin/bash
# Bounded probes for the three out-of-contract items added to the docstring after the round-47 freeze.
# All trees and caches live under $S; the pin is run only with --print-id; nothing writes outside $S.
set -u
S=/fast/scratch/hyaku/mado-r48/ScrD1Line
L=/home/vgpnk/Projects/shokunin/mado-shokunin
PIN=$S/xdg-terminal-exec
cp -f "$L/.ufo/waves/round-47/fetch/xdg-terminal-exec" "$PIN" && chmod 700 "$PIN"
echo "pin sha256: $(sha256sum "$PIN" | cut -d' ' -f1)"
echo "tool sha256: $(sha256sum "$L/tools/mado-terminal.py" | cut -d' ' -f1)"
echo

mk_tree() {   # $1 = case dir
  local t=$1
  rm -rf -- "$t"; mkdir -p "$t"/{home,data1,data2,cfg,cfgdirs,cache}
  printf '[Desktop Entry]\nType=Application\nName=t\nCategories=TerminalEmulator;\nExec=myterm\nTryExec=ls\n' > "$t/data1/term.desktop"
}

run_tool() {  # $1 = tree, $2 = env spec marker
  python3 -I "$L/tools/mado-terminal.py" print --print-id
}

echo "== A: HOME unset =="
A=$S/a; mk_tree "$A"
env -u HOME XDG_CONFIG_HOME="$A/cfg" XDG_CONFIG_DIRS="$A/cfgdirs" XDG_DATA_HOME="$A/data2" \
    XDG_DATA_DIRS="$A/data1" XDG_CACHE_HOME="$A/cache" PATH=/usr/bin:/bin \
    bash -c 'echo "--- pin ---"; timeout 10 "'"$PIN"'" --print-id; echo "pin rc=$?"'
env -u HOME XDG_CONFIG_HOME="$A/cfg" XDG_CONFIG_DIRS="$A/cfgdirs" XDG_DATA_HOME="$A/data2" \
    XDG_DATA_DIRS="$A/data1" XDG_CACHE_HOME="$A/cache" PATH=/usr/bin:/bin \
    bash -c 'echo "--- tool ---"; python3 -I "'"$L"'/tools/mado-terminal.py" print --print-id; echo "tool rc=$?"'
echo

echo "== B: FIFO named like a desktop file in a LATER application dir (XDG_DATA_HOME) =="
B=$S/b; mk_tree "$B"
mkfifo "$B/data2/pipe.desktop"
env XDG_CONFIG_HOME="$B/cfg" XDG_CONFIG_DIRS="$B/cfgdirs" XDG_DATA_HOME="$B/data2" \
    XDG_DATA_DIRS="$B/data1" XDG_CACHE_HOME="$B/cache" HOME="$B/home" PATH=/usr/bin:/bin \
    bash -c 'echo "--- tool ---"; python3 -I "'"$L"'/tools/mado-terminal.py" print --print-id; echo "tool rc=$?"; echo "--- pin (timeout 5; a block is expected) ---"; timeout 5 "'"$PIN"'" --print-id; echo "pin rc=$?"'
echo

echo "== C: symlink loop inside an application dir =="
C=$S/c; mk_tree "$C"
ln -s . "$C/data1/self"          # self-referential directory symlink
ln -s ../data1 "$C/data1/up"     # symlink to the containing dir
env XDG_CONFIG_HOME="$C/cfg" XDG_CONFIG_DIRS="$C/cfgdirs" XDG_DATA_HOME="$C/data2" \
    XDG_DATA_DIRS="$C/data1" XDG_CACHE_HOME="$C/cache" HOME="$C/home" PATH=/usr/bin:/bin \
    bash -c 'echo "--- tool ---"; python3 -I "'"$L"'/tools/mado-terminal.py" print --print-id; echo "tool rc=$?"; echo "--- pin ---"; timeout 10 "'"$PIN"'" --print-id; echo "pin rc=$?"'
echo "== C2: same loop, explain MADO_TERM line =="
env XDG_CONFIG_HOME="$C/cfg" XDG_CONFIG_DIRS="$C/cfgdirs" XDG_DATA_HOME="$C/data2" \
    XDG_DATA_DIRS="$C/data1" XDG_CACHE_HOME="$C/cache" HOME="$C/home" PATH=/usr/bin:/bin \
    bash -c 'python3 -I "'"$L"'/tools/mado-terminal.py" explain 2>&1 | grep -E "^MADO_TERM|OUT_OF_CONTRACT"; echo "explain rc=${PIPESTATUS[0]}"'
echo

echo "== host cache untouched =="
stat -c '%y %n' "$HOME/.cache/xdg-terminal-exec" 2>/dev/null || echo "no host cache"
