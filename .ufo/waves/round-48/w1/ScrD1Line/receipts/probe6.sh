#!/bin/bash
# Does the landed tool register a NON-regular path in a later application dir (the code comment at :489-491
# and ExecC1Diff H1), while the landed docstring step 4 still says `-type f` over every dir?
set -u
S=/fast/scratch/hyaku/mado-r48/ScrD1Line
L=/home/vgpnk/Projects/shokunin/mado-shokunin
PIN=$S/xdg-terminal-exec
D=$S/dirshadow
rm -rf -- "$D"; mkdir -p "$D"/{home,data1/applications,data2/applications/x.desktop,cfg,cfgdirs,cache}
printf '[Desktop Entry]\nType=Application\nName=t\nCategories=TerminalEmulator;\nExec=ls\nTryExec=ls\n' > "$D/data1/applications/x.desktop"
E=(XDG_CONFIG_HOME="$D/cfg" XDG_CONFIG_DIRS="$D/cfgdirs" XDG_DATA_HOME="$D/data2" XDG_DATA_DIRS="$D/data1" XDG_CACHE_HOME="$D/cache" HOME="$D/home" PATH=/usr/bin:/bin)
cd "$D" || exit 1
echo "tree: data1/applications/x.desktop = regular entry; data2/applications/x.desktop = DIRECTORY"
echo "--- tool ---"; env "${E[@]}" timeout 10 python3 -I "$L/tools/mado-terminal.py" print --print-id; echo "tool rc=$?"
echo "--- tool explain (candidate lines) ---"; env "${E[@]}" timeout 10 python3 -I "$L/tools/mado-terminal.py" explain 2>&1 | grep -iE 'candidate|MADO_TERM:|shadow' ; echo "explain rc=${PIPESTATUS[0]}"
echo "--- pin ---"; env "${E[@]}" timeout 10 "$PIN" --print-id; echo "pin rc=$?"
echo
echo "tree B: FIFO in the FIRST-walked dir (docstring excludes only a later dir)"
F=$S/fifofirst
rm -rf -- "$F"; mkdir -p "$F"/{home,data1/applications,data2/applications,cfg,cfgdirs,cache}
printf '[Desktop Entry]\nType=Application\nName=t\nCategories=TerminalEmulator;\nExec=ls\nTryExec=ls\n' > "$F/data1/applications/term.desktop"
mkfifo "$F/data1/applications/pipe.desktop"
cd "$F" || exit 1
G=(XDG_CONFIG_HOME="$F/cfg" XDG_CONFIG_DIRS="$F/cfgdirs" XDG_DATA_HOME="$F/data2" XDG_DATA_DIRS="$F/data1" XDG_CACHE_HOME="$F/cache" HOME="$F/home" PATH=/usr/bin:/bin)
echo "--- tool ---"; env "${G[@]}" timeout 10 python3 -I "$L/tools/mado-terminal.py" print --print-id; echo "tool rc=$?"
echo "--- pin ---"; env "${G[@]}" timeout 10 "$PIN" --print-id; echo "pin rc=$?"
