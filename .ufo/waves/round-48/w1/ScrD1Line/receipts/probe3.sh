#!/bin/bash
# HOME-unset variants: where the pin actually fails, and what the tool does in each.
set -u
S=/fast/scratch/hyaku/mado-r48/ScrD1Line
L=/home/vgpnk/Projects/shokunin/mado-shokunin
PIN=$S/xdg-terminal-exec
A=$S/h
rm -rf -- "$A"; mkdir -p "$A"/{data1/applications,data2/applications,cfg,cfgdirs,cache,home}
printf '[Desktop Entry]\nType=Application\nName=t\nCategories=TerminalEmulator;\nExec=ls\nTryExec=ls\n' > "$A/data1/applications/term.desktop"

v() {  # $1 label, rest: env assignments (may include "HOME" => unset)
  local label=$1; shift
  echo "== $label =="
  ( cd "$A" || exit 1
    if printf '%s\n' "$@" | grep -qx 'HOME=UNSET'; then
      envargs=(env -u HOME)
      for a in "$@"; do [ "$a" = "HOME=UNSET" ] && continue; envargs+=("$a"); done
    else
      envargs=(env); for a in "$@"; do envargs+=("$a"); done
    fi
    echo "--- pin ---"
    "${envargs[@]}" timeout 10 "$PIN" --print-id; echo "pin rc=$?"
    echo "--- tool ---"
    "${envargs[@]}" timeout 10 python3 -I "$L/tools/mado-terminal.py" print --print-id; echo "tool rc=$?"
  )
  echo
}

v "V1 HOME unset, every XDG_* set (incl. XDG_CACHE_HOME)" HOME=UNSET \
  XDG_CONFIG_HOME="$A/cfg" XDG_CONFIG_DIRS="$A/cfgdirs" XDG_DATA_HOME="$A/data2" XDG_DATA_DIRS="$A/data1" \
  XDG_CACHE_HOME="$A/cache" PATH=/usr/bin:/bin
v "V2 HOME unset, XDG_CACHE_HOME unset, the rest set" HOME=UNSET \
  XDG_CONFIG_HOME="$A/cfg" XDG_CONFIG_DIRS="$A/cfgdirs" XDG_DATA_HOME="$A/data2" XDG_DATA_DIRS="$A/data1" \
  PATH=/usr/bin:/bin
v "V3 HOME unset, XDG_CONFIG_HOME and XDG_DATA_HOME unset, dirs+cache set" HOME=UNSET \
  XDG_CONFIG_DIRS="$A/cfgdirs" XDG_DATA_DIRS="$A/data1" XDG_CACHE_HOME="$A/cache" PATH=/usr/bin:/bin
v "V4 HOME unset, no XDG_* at all" HOME=UNSET PATH=/usr/bin:/bin
