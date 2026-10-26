#!/bin/bash
# SentC1Host hostile-case driver. Every case gets its own root; env -i; timeout per case.
set -u
S=/fast/scratch/hyaku/mado-r47/SentC1Host
TOOL=$S/tool.py
OUT=$S/results.tsv
: >"$OUT"

mkcase() {  # $1 = case dir
  local C=$1
  mkdir -p "$C/home/.config" "$C/home/.local/share/applications" "$C/cache" "$C/bin" "$C/share" "$C/etcxdg"
  printf '[Desktop Entry]\nType=Application\nName=Foot\nExec=foot\nCategories=System;TerminalEmulator;\n' \
    >"$C/home/.local/share/applications/good.desktop"
  printf '#!/bin/sh\n' >"$C/bin/foot"; chmod +x "$C/bin/foot"
}

baseenv() {  # $1 = case dir; prints env assignments
  local C=$1
  printf 'HOME=%s PATH=%s TMPDIR=%s XDG_CONFIG_HOME=%s XDG_DATA_HOME=%s XDG_DATA_DIRS=%s XDG_CONFIG_DIRS=%s XDG_CURRENT_DESKTOP=Hyprland XDG_CACHE_HOME=%s' \
    "$C/home" "$C/bin" "$S/tmp" "$C/home/.config" "$C/home/.local/share" "$C/share" "$C/etcxdg" "$C/cache"
}

runcase() {  # $1 name, $2 timeout, $3 casedir, rest: extra args after "explain"
  local name=$1 tmo=$2 C=$3; shift 3
  local so=$C.out se=$C.err t0 t1 rc
  t0=$(date +%s.%N)
  timeout -k 2 "$tmo" env -i $(baseenv "$C") /usr/bin/python3 -I "$TOOL" explain "$@" >"$so" 2>"$se"
  rc=$?
  t1=$(date +%s.%N)
  printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$rc" "$(echo "$t1 - $t0" | bc)" \
    "$(tail -c 300 "$so" | tr '\n' '|' | tr -d '\t')" \
    "$(tail -c 300 "$se" | tr '\n' '|' | tr -d '\t')" >>"$OUT"
  printf '%-22s rc=%-4s t=%-7s %s\n' "$name" "$rc" "$(echo "$t1 - $t0" | bc)" "$(tail -c 200 "$so" | tr '\n' ' ')"
}

mkdir -p "$S/tmp"

# ---- C0 clean baseline
C=$S/c/C0; mkcase "$C"; runcase C0-clean 40 "$C"

# ---- C1 FIFO as the config list file (list path is not a regular file -> must be skipped)
C=$S/c/C1; mkcase "$C"; rm -f "$C/home/.config/xdg-terminals.list"
mkfifo "$C/home/.config/xdg-terminals.list"
runcase C1-fifo-list 20 "$C"

# ---- C2 FIFO as a .desktop entry
C=$S/c/C2; mkcase "$C"; mkfifo "$C/home/.local/share/applications/pipe.desktop"
runcase C2-fifo-desktop 20 "$C"

# ---- C3 FIFO handed to --observed (operator arg; main read_file opens it)
C=$S/c/C3; mkcase "$C"; mkfifo "$C/observed.fifo"
runcase C3-fifo-observed 10 "$C" --observed "$C/observed.fifo"

# ---- C4 /dev/zero handed to --observed (unbounded read), memory capped so the host survives
C=$S/c/C4; mkcase "$C"
( ulimit -v 1500000; timeout -k 2 10 env -i $(baseenv "$C") /usr/bin/python3 -I "$TOOL" explain --observed /dev/zero >"$C.out" 2>"$C.err"; echo "rc=$?" >"$C.rc" )
printf 'C4-devzero-observed\t%s\t-\t%s\t%s\n' "$(cat "$C.rc")" \
  "$(tail -c 200 "$C.out" | tr '\n' '|')" "$(tail -c 300 "$C.err" | tr '\n' '|')" >>"$OUT"

# ---- C5 symlink self-loop in the applications dir
C=$S/c/C5; mkcase "$C"; ln -s . "$C/home/.local/share/applications/loop"
runcase C5-symlink-selfloop 20 "$C"

# ---- C6 symlink out of the applications dir to a real, wider tree (measures escape)
C=$S/c/C6; mkcase "$C"; ln -s /usr/share/doc "$C/home/.local/share/applications/out"
runcase C6-symlink-out 30 "$C"

# ---- C7 deep nesting (find -L has no depth cap; python recursion has one)
C=$S/c/C7; mkcase "$C"
p="$C/home/.local/share/applications"
for i in $(seq 1 1400); do p="$p/d"; done
mkdir -p "$p" && printf '[Desktop Entry]\nType=Application\nName=Deep\nExec=foot\nCategories=System;TerminalEmulator;\n' >"$p/deep.desktop"
runcase C7-deep-nest 60 "$C"

# ---- C8 huge list file (64 MiB of entry lines)
C=$S/c/C8; mkcase "$C"
/usr/bin/python3 - "$C/home/.config/xdg-terminals.list" <<'PY'
import sys
with open(sys.argv[1], "w") as f:
    for i in range(2000000):
        f.write("entry%07d.desktop\n" % i)
PY
ls -l "$C/home/.config/xdg-terminals.list" | awk '{print "C8 list size:", $5}'
runcase C8-huge-list 60 "$C"

# ---- C9 /proc inside the XDG vars
C=$S/c/C9; mkcase "$C"
( C=$S/c/C9
  timeout -k 2 20 env -i HOME="$C/home" PATH="$C/bin" TMPDIR="$S/tmp" XDG_CONFIG_HOME=/proc/self XDG_DATA_HOME=/proc/self XDG_DATA_DIRS=/proc/self XDG_CONFIG_DIRS=/proc/self XDG_CURRENT_DESKTOP=Hyprland XDG_CACHE_HOME=/proc/self \
    /usr/bin/python3 -I "$TOOL" explain >"$C.p.out" 2>"$C.p.err"; echo "rc=$?" >"$C.p.rc" )
printf 'C9b-proc-xdg\t%s\t-\t%s\t%s\n' "$(cat "$C.p.rc")" \
  "$(tail -c 300 "$C.p.out" | tr '\n' '|')" "$(tail -c 300 "$C.p.err" | tr '\n' '|')" >>"$OUT"

# ---- C10 list file symlinked to /proc/self/mem (regular file, read raises)
C=$S/c/C10; mkcase "$C"; ln -s /proc/self/mem "$C/home/.config/xdg-terminals.list"
runcase C10-proc-mem-list 20 "$C"

# ---- C11 list file symlinked to /dev/zero (char device -> non-regular, must be skipped)
C=$S/c/C11; mkcase "$C"; ln -s /dev/zero "$C/home/.config/xdg-terminals.list"
runcase C11-devzero-list 10 "$C"

# ---- C12 device file as an entry
C=$S/c/C12; mkcase "$C"; ln -s /dev/zero "$C/home/.local/share/applications/zero.desktop"
runcase C12-devzero-desktop 10 "$C"

# ---- C13 permission errors: list file 000, entry 000, applications dir 000
C=$S/c/C13; mkcase "$C"
printf 'good.desktop\n' >"$C/home/.config/xdg-terminals.list"; chmod 000 "$C/home/.config/xdg-terminals.list"
runcase C13a-list-000 20 "$C"
C=$S/c/C13b; mkcase "$C"; chmod 000 "$C/home/.local/share/applications/good.desktop"
runcase C13b-entry-000 20 "$C"
C=$S/c/C13c; mkcase "$C"; chmod 000 "$C/home/.local/share/applications"
runcase C13c-appdir-000 20 "$C"

# ---- C14 XDG var holding a glob character (declared out of contract -> rc 2)
C=$S/c/C14; mkcase "$C"
( C=$S/c/C14
  timeout -k 2 20 env -i HOME="$C/home" PATH="$C/bin" TMPDIR="$S/tmp" XDG_CONFIG_HOME="$C/home/.config" XDG_DATA_HOME="$C/home/.l*" XDG_CURRENT_DESKTOP=Hyprland \
    /usr/bin/python3 -I "$TOOL" explain >"$C.g.out" 2>"$C.g.err"; echo "rc=$?" >"$C.g.rc" )
printf 'C14-glob-xdg\t%s\t-\t%s\t%s\n' "$(cat "$C.g.rc")" \
  "$(tail -c 200 "$C.g.out" | tr '\n' '|')" "$(tail -c 300 "$C.g.err" | tr '\n' '|')" >>"$OUT"

# ---- C15 --observed pointing at a directory
C=$S/c/C15; mkcase "$C"
runcase C15-observed-dir 10 "$C" --observed "$C/home"

# ---- C16 sparse 4 GiB .desktop entry, memory capped
C=$S/c/C16; mkcase "$C"
truncate -s 4G "$C/home/.local/share/applications/huge.desktop"
( ulimit -v 1500000
  timeout -k 2 30 env -i $(baseenv "$C") /usr/bin/python3 -I "$TOOL" explain >"$C.out" 2>"$C.err"; echo "rc=$?" >"$C.rc" )
printf 'C16-huge-entry\t%s\t-\t%s\t%s\n' "$(cat "$C.rc")" \
  "$(tail -c 200 "$C.out" | tr '\n' '|')" "$(tail -c 300 "$C.err" | tr '\n' '|')" >>"$OUT"

# ---- C17 a socket file in the applications dir, and a socket as the list file
C=$S/c/C17; mkcase "$C"
/usr/bin/python3 - "$C" <<'PY'
import socket, sys, os
c = sys.argv[1]
for p in (c + "/home/.local/share/applications/sock.desktop",):
    s = socket.socket(socket.AF_UNIX); s.bind(p); s.close()
PY
runcase C17-socket-entry 15 "$C"

echo "---- $OUT"
cat "$OUT"
