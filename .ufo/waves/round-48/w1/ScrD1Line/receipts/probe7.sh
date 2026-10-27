#!/bin/bash
# FIFO in a later application dir that is NEVER the candidate read: does the pin answer while the tool refuses?
set -u
S=/fast/scratch/hyaku/mado-r48/ScrD1Line
L=/home/vgpnk/Projects/shokunin/mado-shokunin
PIN=$S/xdg-terminal-exec
D=$S/fifo-listed
rm -rf -- "$D"; mkdir -p "$D"/{home,data1/applications,data2/applications,cfg,cfgdirs,cache}
printf '[Desktop Entry]\nType=Application\nName=t\nCategories=TerminalEmulator;\nExec=ls\nTryExec=ls\n' > "$D/data1/applications/term.desktop"
mkfifo "$D/data2/applications/pipe.desktop"
# a list file names term.desktop, so the list candidate is tried before any fallback id
printf 'term.desktop\n' > "$D/cfg/xdg-terminals.list"
E=(XDG_CONFIG_HOME="$D/cfg" XDG_CONFIG_DIRS="$D/cfgdirs" XDG_DATA_HOME="$D/data2" XDG_DATA_DIRS="$D/data1" XDG_CACHE_HOME="$D/cache" HOME="$D/home" PATH=/usr/bin:/bin)
cd "$D" || exit 1
echo "tree: list file names term.desktop; data2/applications/pipe.desktop is a FIFO that is never read"
echo "--- pin ---"; env "${E[@]}" timeout 10 "$PIN" --print-id; echo "pin rc=$?"
echo "--- tool ---"; env "${E[@]}" timeout 10 python3 -I "$L/tools/mado-terminal.py" print --print-id; echo "tool rc=$?"
echo "--- tool explain ---"; env "${E[@]}" timeout 10 python3 -I "$L/tools/mado-terminal.py" explain 2>&1 | tail -3; echo "explain rc=${PIPESTATUS[0]}"
