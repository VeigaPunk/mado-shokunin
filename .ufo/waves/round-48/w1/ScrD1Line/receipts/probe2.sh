#!/bin/bash
# Bounded probes, take 2: application dirs are <XDG_DATA_DIRS entry>/applications and <XDG_DATA_HOME>/applications.
set -u
S=/fast/scratch/hyaku/mado-r48/ScrD1Line
L=/home/vgpnk/Projects/shokunin/mado-shokunin
PIN=$S/xdg-terminal-exec
ENTRY='[Desktop Entry]
Type=Application
Name=t
Categories=TerminalEmulator;
Exec=ls
TryExec=ls
'

mk_tree() {   # $1 = case dir; valid entry in the FIRST-walked dir (XDG_DATA_DIRS), empty data home
  local t=$1
  rm -rf -- "$t"; mkdir -p "$t"/{home,data1/applications,data2/applications,cfg,cfgdirs,cache}
  printf '%s' "$ENTRY" > "$t/data1/applications/term.desktop"
}
envs() {  # $1 = tree
  XDG_CONFIG_HOME="$1/cfg" XDG_CONFIG_DIRS="$1/cfgdirs" XDG_DATA_HOME="$1/data2" \
  XDG_DATA_DIRS="$1/data1" XDG_CACHE_HOME="$1/cache" HOME="$1/home" PATH=/usr/bin:/bin
  export XDG_CONFIG_HOME XDG_CONFIG_DIRS XDG_DATA_HOME XDG_DATA_DIRS XDG_CACHE_HOME HOME PATH
}

echo "== A: HOME unset (valid entry present) =="
A=$S/a2; mk_tree "$A"
( envs "$A"; cd "$A" || exit 1
  echo "--- pin ---"; env -u HOME timeout 10 "$PIN" --print-id; echo "pin rc=$?"
  echo "--- tool ---"; env -u HOME python3 -I "$L/tools/mado-terminal.py" print --print-id; echo "tool rc=$?"
  echo "--- tool explain ---"; env -u HOME python3 -I "$L/tools/mado-terminal.py" explain >/dev/null 2>"$A/err"; echo "tool explain rc=$?"; cat "$A/err"
)
echo

echo "== B: FIFO named pipe.desktop in XDG_DATA_HOME (the later-walked dir) =="
B=$S/b2; mk_tree "$B"; mkfifo "$B/data2/applications/pipe.desktop"
( envs "$B"; cd "$B" || exit 1
  echo "--- tool ---"; timeout 10 python3 -I "$L/tools/mado-terminal.py" print --print-id; echo "tool rc=$?"
  echo "--- pin (timeout 5; a block is expected) ---"; timeout 5 "$PIN" --print-id; echo "pin rc=$?"
)
echo

echo "== B2: same FIFO, control: no FIFO, both dirs have the valid entry =="
B2=$S/b2c; mk_tree "$B2"; cp "$B2/data1/applications/term.desktop" "$B2/data2/applications/term.desktop"
( envs "$B2"; cd "$B2" || exit 1
  echo "--- tool ---"; timeout 10 python3 -I "$L/tools/mado-terminal.py" print --print-id; echo "tool rc=$?"
  echo "--- pin ---"; timeout 10 "$PIN" --print-id; echo "pin rc=$?"
)
echo

echo "== C: symlink loop in the first-walked application dir =="
C=$S/c2; mk_tree "$C"
ln -s . "$C/data1/applications/self"
ln -s .. "$C/data1/applications/up"
( envs "$C"; cd "$C" || exit 1
  echo "--- tool ---"; timeout 10 python3 -I "$L/tools/mado-terminal.py" print --print-id; echo "tool rc=$?"
  echo "--- tool explain ---"; timeout 10 python3 -I "$L/tools/mado-terminal.py" explain 2>&1 | grep -E '^MADO_TERM:|OUT_OF_CONTRACT'; echo "explain rc=${PIPESTATUS[0]}"
  echo "--- pin ---"; timeout 10 "$PIN" --print-id; echo "pin rc=$?"
)
echo

echo "== C3: symlink loop but the entry lives in a deeper real subdir =="
C3=$S/c3; rm -rf -- "$C3"; mkdir -p "$C3"/{home,data1/applications/sub,data2/applications,cfg,cfgdirs,cache}
printf '%s' "$ENTRY" > "$C3/data1/applications/sub/deep.desktop"
ln -s ../.. "$C3/data1/applications/sub/root"
( envs "$C3"; cd "$C3" || exit 1
  echo "--- tool ---"; timeout 10 python3 -I "$L/tools/mado-terminal.py" print --print-id 2>&1; echo "tool rc=$?"
  echo "--- pin ---"; timeout 10 "$PIN" --print-id 2>&1; echo "pin rc=$?"
)
