#!/bin/bash
# SentHost receipt generator: every experiment runs on scratch fixtures only.
# Nothing here touches the real HOME, ~/.cache, the compositor, or the network.
set -u
S=${1:?usage: gen-receipts.sh <scratch-dir>}
R=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w1/SentHost/receipts
XTE=/usr/bin/xdg-terminal-exec
mkdir -p "$R"
export TMPDIR="$S/tmp"; mkdir -p "$TMPDIR"

mkcase() { # $1 = dir
  mkdir -p "$1/home/.local/share/applications" "$1/x" "$1/cfg" "$1/bin" "$1/cache" "$1/cache-run"
  cat > "$1/env.sh" <<EOF
export HOME=$1/home
# F2b: the agent shell exports XDG_CACHE_HOME, so HOME alone redirects nothing.
export XDG_CACHE_HOME=$1/cache-run
export XDG_DATA_HOME=$1/home/.local/share
export XDG_DATA_DIRS=$1/x
export XDG_CONFIG_HOME=$1/home/.config
export XDG_CONFIG_DIRS=$1/cfg
export XDG_CURRENT_DESKTOP=Hyprland
export PATH=$1/bin:/usr/bin:/bin
EOF
  cat > "$1/home/.local/share/applications/Term.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Term
Exec=fake-term
Categories=System;TerminalEmulator;
EOF
  printf '#!/bin/sh\nexit 0\n' > "$1/bin/fake-term"; chmod +x "$1/bin/fake-term"
}

{
echo "# cache-write.txt - which print mode writes the resolver cache, and where"
echo "# fixture: scratch XDG tree, HOME=<scratch case>/home, PATH=<scratch>/bin:/usr/bin:/bin"
echo "# date: $(date -Is)"
echo "# xdg-terminal-exec sha256: $(sha256sum $XTE | cut -d' ' -f1)"
echo
C=$S/cw; rm -rf "$C"; mkcase "$C"
echo "## 1. --print-id only, XDG_CACHE_HOME=<empty scratch dir>"
( . "$C/env.sh"; XDG_CACHE_HOME=$C/cache "$XTE" --print-id; echo "rc=$?"; sleep 0.6
  echo "cache_files=$(find "$C/cache" -type f | wc -l)" )
echo
echo "## 2. --print-id --print-path --print-cmd (the wave's capture shape), XDG_CACHE_HOME=<scratch>"
( . "$C/env.sh"; XDG_CACHE_HOME=$C/cache "$XTE" --print-id --print-path --print-cmd; echo "rc=$?"; sleep 0.6
  find "$C/cache" -type f -printf 'cache_file=%p bytes=%s\n' )
echo
echo "## 3. --print-cmd with XDG_CACHE_HOME UNSET (HOME points into scratch)"
rm -rf "$C/home/.cache"
( . "$C/env.sh"; unset XDG_CACHE_HOME; "$XTE" --print-cmd >/dev/null; echo "rc=$?"; sleep 0.6
  find "$C/home/.cache" -type f -printf 'wrote_below_HOME=%p bytes=%s\n' 2>/dev/null || echo "no file" )
echo
echo "## 4. --print-cmd with XDG_CACHE_HOME='' (empty VALUE, not empty dir)"
rm -rf "$C/home/.cache"
( . "$C/env.sh"; XDG_CACHE_HOME= "$XTE" --print-cmd >/dev/null; echo "rc=$?"; sleep 0.6
  find "$C/home/.cache" -type f -printf 'wrote_below_HOME=%p bytes=%s\n' 2>/dev/null || echo "no file" )
} > "$R/cache-write.txt" 2>&1

{
echo "# stale-cache.txt - a warm cache can make --print-cmd differ from a cold run"
echo "# fixture: same tree, one desktop file edited with identical byte size and identical mtime"
S=$S; C=$S/sc; rm -rf "$C"; mkcase "$C"
F="$C/home/.local/share/applications/Term.desktop"
cp -p "$F" "$C/ref.desktop"
# cache is written by the pre-edit run
( . "$C/env.sh"; XDG_CACHE_HOME=$C/cache "$XTE" --print-cmd; echo "rc=$?" ); sleep 0.7
sed -i 's/^Exec=fake-term$/Exec=fake-trmX/' "$F"; touch -r "$C/ref.desktop" "$F"
printf '#!/bin/sh\nexit 0\n' > "$C/bin/fake-trmX"; chmod +x "$C/bin/fake-trmX"
echo "size_before=$(stat -c%s "$C/ref.desktop") size_after=$(stat -c%s "$F") mtime_identical=$([ "$(stat -c%Y "$C/ref.desktop")" = "$(stat -c%Y "$F")" ] && echo yes || echo no)"
echo -n "warm_cache_prints="; ( . "$C/env.sh"; XDG_CACHE_HOME=$C/cache "$XTE" --print-cmd ) ; echo " rc=$?"
mkdir -p "$C/cache2"
echo -n "cold_cache_prints="; ( . "$C/env.sh"; XDG_CACHE_HOME=$C/cache2 "$XTE" --print-cmd ) ; echo " rc=$?"
echo
echo "# cause: the cache key is md5 over 'ls -LRl' of config+data paths (size+mtime only),"
echo "# so a content change preserving both keeps the hash and the cache is applied."
} > "$R/stale-cache.txt" 2>&1

{
echo "# hostile-files.txt - what the resolver does with a hostile applications directory"
echo "# fixture: scratch XDG tree with a valid Term.desktop plus hostile siblings"
C=$S/hf; rm -rf "$C"; mkcase "$C"
A="$C/home/.local/share/applications"
ln -s /proc/self/environ "$A/Proc.desktop"
ln -s . "$A/Loop.desktop"
mkfifo "$A/Fifo.desktop"
ln -s /nonexistent/target.desktop "$A/Dangling.desktop"
python3 - "$A/Huge.desktop" <<'PY'
import sys
with open(sys.argv[1],'w') as f:
    f.write("[Desktop Entry]\nType=Application\nName=Huge\nExec=fake-term\nCategories=System;TerminalEmulator;\n")
    f.write("Comment=" + "x"*(50*1024*1024) + "\n")
PY
echo "## entries present:"
ls -la "$A" | awk 'NR>3 {printf "  %s %s %s\n", $1, $9, $10}'
echo
echo "## --print-id with the valid entry present (find order decides the last found):"
( . "$C/env.sh"; /usr/bin/timeout 60 "$XTE" --print-id; echo "rc=$?" )
echo
echo "## --print-id with only hostile entries (valid and huge entries moved away):"
mv "$A/Term.desktop" "$A/Term.off"; mv "$A/Huge.desktop" "$A/Huge.off"
( . "$C/env.sh"; t0=$(date +%s%N); /usr/bin/timeout 60 "$XTE" --print-id; rc=$?; t1=$(date +%s%N)
  echo "rc=$rc wall_ms=$(( (t1-t0)/1000000 ))" )
mv "$A/Term.off" "$A/Term.desktop"
echo
echo "## symlink escape: applications/Escape.desktop -> <outside>/Evil.desktop"
mkdir -p "$C/outside"
cat > "$C/outside/Evil.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Evil
Exec=fake-term
Categories=System;TerminalEmulator;
EOF
mv "$A/Term.desktop" "$A/Term.off"; ln -sf "$C/outside/Evil.desktop" "$A/Escape.desktop"
( . "$C/env.sh"; /usr/bin/timeout 60 "$XTE" --print-id --print-path --print-content; echo "rc=$?" )
mv "$A/Term.off" "$A/Term.desktop"; rm -f "$A/Escape.desktop"
} > "$R/hostile-files.txt" 2>&1

{
echo "# exec-argv.txt - what a print run spawns, writes, and opens"
C=$S/tr; rm -rf "$C"; mkcase "$C"
( . "$C/env.sh"; XDG_CACHE_HOME=$C/cache strace -f -qq -e trace=execve,openat,mkdir,socket,connect \
    -o "$S/tr.txt" "$XTE" --print-id --print-path --print-cmd >/dev/null; echo "rc=$?" )
echo "## execve (basename, count)"
grep -h 'execve(' "$S/tr.txt" | sed -E 's/.*execve\("([^"]+)".*/\1/' | sed 's#.*/##' | sort | uniq -c
echo "## openat with write intent (deduplicated)"
grep -h 'openat(' "$S/tr.txt" | grep -E 'O_WRONLY|O_RDWR|O_CREAT' | sed -E 's/^[0-9]+ +//' | sed "s#$S#\$S#g" | sort -u
echo "## sockets/connects"
grep -hE 'socket\(|connect\(' "$S/tr.txt" | sed -E 's/^[0-9]+ +//' | sort | uniq -c
echo
echo "## pure-Python baseline for the C1 tripwire form (tool side must be 1/0/0)"
printf 'print("x")\n' > "$S/pure.py"
strace -f -qq -e trace=execve,socket,connect -o "$S/p.txt" python3 -I "$S/pure.py" >/dev/null || echo "STRACE_FAILED (nested ptrace?)"
n=$(grep -c 'execve(' "$S/p.txt" 2>/dev/null || echo 0)
echo "python3_I_script execve=$n socket=$(grep -c 'socket(' "$S/p.txt") connect=$(grep -c 'connect(' "$S/p.txt")"
[ "${n:-0}" -ge 1 ] || echo "TRIPWIRE_UNMEASURED: the baseline above is not evidence"
} > "$R/exec-argv.txt" 2>&1

{
echo "# builtin-exec.txt - Exec=cd is accepted (command -v sees shell builtins); metacharacters are not executed"
C=$S/bu; rm -rf "$C"; mkcase "$C"
A="$C/home/.local/share/applications"; rm -f "$A/Term.desktop"
mk(){ printf '[Desktop Entry]\nType=Application\nName=%s\nExec=%s\nCategories=System;TerminalEmulator;\n' "$1" "$2" > "$A/$1.desktop"; }
mk OnlyCD 'cd'
mk Meta "foo; touch $S/BUILTIN-CANARY"
mk Subst '$(touch '$S'/SUBST-CANARY)'
for id in OnlyCD Meta Subst; do
  echo -n "[$id] "; ( . "$C/env.sh"; "$XTE" --print-id --print-cmd; echo " rc=$?" )
done
echo -n "canary_files_present="; ls "$S/BUILTIN-CANARY" "$S/SUBST-CANARY" 2>/dev/null | wc -l
} > "$R/builtin-exec.txt" 2>&1

echo "receipts:"; ls -la "$R"
