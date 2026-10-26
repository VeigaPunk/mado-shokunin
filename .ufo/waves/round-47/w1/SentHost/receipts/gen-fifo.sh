#!/bin/bash
# fifo-hang receipt: the resolver's find expression matches non-regular files in
# the LAST applications dir, and opening the FIFO blocks forever.
set -u
S=${1:?usage: gen-fifo.sh <scratch-dir>}
R=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w1/SentHost/receipts
C=$S/fh; rm -rf "$C"; mkdir -p "$C/home/.local/share/applications" "$C/x/applications" "$C/cfg" "$C/bin" "$C/cache"
printf '#!/bin/sh\nexit 0\n' > "$C/bin/fake-term"; chmod +x "$C/bin/fake-term"
printf '[Desktop Entry]\nType=Application\nName=T\nExec=fake-term\nCategories=System;TerminalEmulator;\n' > "$C/home/.local/share/applications/AAA.desktop"
A="$C/home/.local/share/applications"
X="$C/x/applications"
{
echo "# fifo-hang.txt - a FIFO named *.desktop in the LAST applications dir hangs the resolver"
echo "# fixture: scratch XDG tree; AAA.desktop is a valid terminal entry"
echo "# resolver: /usr/bin/xdg-terminal-exec sha256 $(sha256sum /usr/bin/xdg-terminal-exec | cut -d' ' -f1)"
echo "# date: $(date -Is)"
echo
echo "## 1. find argv the resolver builds (captured with a PATH shim) - note: no -o before the FIRST group"
echo '  find -L <dir1>/. <dir2>/. -type f ( -path <dir1>/./[a-zA-Z0-9_]*.desktop ! -path <dir1>/./*[^a-zA-Z0-9_./-]* ) -o ( -path <dir2>/./[a-zA-Z0-9_]*.desktop ! -path <dir2>/./*[^a-zA-Z0-9_./-]* )'
echo "  => (-type f AND group1) OR group2 : group2 has no type constraint"
echo
echo "## 2. the same expression, run verbatim, with a FIFO in the second dir"
mkfifo "$A/Fifo.desktop"
LC_ALL=C /usr/bin/find -L "$X/." "$A/." -type f \( -path "$X/./[a-zA-Z0-9_]*.desktop" ! -path "$X/./*[^a-zA-Z0-9_./-]*" \) -o \( -path "$A/./[a-zA-Z0-9_]*.desktop" ! -path "$A/./*[^a-zA-Z0-9_./-]*" \) 2>&1 | sed "s#$C#<CASE>#g"
echo
echo "## 3. same expression with the dirs swapped (FIFO dir first): FIFO is excluded"
LC_ALL=C /usr/bin/find -L "$A/." "$X/." -type f \( -path "$A/./[a-zA-Z0-9_]*.desktop" ! -path "$A/./*[^a-zA-Z0-9_./-]*" \) -o \( -path "$X/./[a-zA-Z0-9_]*.desktop" ! -path "$X/./*[^a-zA-Z0-9_./-]*" \) 2>&1 | sed "s#$C#<CASE>#g"
echo
echo "## 4. resolver runs (timeout 3s each)"
go(){ ( export HOME=$C/home XDG_CURRENT_DESKTOP=Hyprland XDG_CONFIG_HOME=$C/home/.config XDG_CONFIG_DIRS=$C/cfg \
        PATH=$C/bin:/usr/bin:/bin XDG_CACHE_HOME=$C/cache XDG_DATA_HOME=$C/home/.local/share "$@"
        t0=$(date +%s%N); /usr/bin/timeout 3 /usr/bin/xdg-terminal-exec --print-id >/dev/null 2>&1; rc=$?
        t1=$(date +%s%N); echo "rc=$rc wall_ms=$(( (t1-t0)/1000000 ))" ); }
echo -n "A) FIFO in XDG_DATA_HOME/applications, XDG_DATA_DIRS=<dir without applications subdir>: "; go env XDG_DATA_DIRS=$C/noapps
rm -f "$A/Fifo.desktop"
echo -n "B) FIFO in XDG_DATA_DIRS/applications, XDG_DATA_DIRS=$C/x:                                 "; mkfifo "$X/Fifo.desktop"; go env XDG_DATA_DIRS=$C/x; rm -f "$X/Fifo.desktop"
echo -n "C) FIFO in XDG_DATA_HOME/applications, XDG_DATA_DIRS=$C/x:                                "; mkfifo "$A/Fifo.desktop"; go env XDG_DATA_DIRS=$C/x
echo -n "D) directory named Dir.desktop in XDG_DATA_HOME/applications:                             "; rm -f "$A/Fifo.desktop"; mkdir "$A/Dir.desktop"; go env XDG_DATA_DIRS=$C/x; rmdir "$A/Dir.desktop"
echo
echo "# rc=124 = /usr/bin/timeout killed an invocation that never finished."
echo "# ordering: XTE__APPLICATIONS_DIRS is filled by prefixing, so the XDG_DATA_HOME dir is LAST"
echo "# and is therefore the one matched by the unconstrained OR group."
} > "$R/fifo-hang.txt" 2>&1
cat "$R/fifo-hang.txt"
