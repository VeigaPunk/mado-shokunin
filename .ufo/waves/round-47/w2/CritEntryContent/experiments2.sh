#!/bin/sh
set -u
S=/fast/scratch/hyaku/mado-r47/CritEntryContent/exp
P=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/fetch/xdg-terminal-exec
mkenv() { R=$1; mkdir -p "$R/home/.config" "$R/etc/xdg" "$R/usr/share/applications" "$R/home/.local/share/applications" "$R/bin" "$R/home/.cache"
  for t in find awk tr ls md5sum mkdir rm; do ln -sf /usr/bin/$t "$R/bin/$t"; done; }
run() { R=$1; shift
  env HOME="$R/home" PATH="$R/bin" XDG_CONFIG_HOME="$R/home/.config" XDG_CONFIG_DIRS="$R/etc/xdg" \
      XDG_DATA_HOME="$R/home/.local/share" XDG_DATA_DIRS="$R/usr/share" XDG_CACHE_HOME="$R/home/.cache" \
      XDG_CURRENT_DESKTOP=Hyprland /usr/bin/timeout 20 /bin/sh "$P" "$@" 2>"$R/stderr"
  echo "rc=$?"; }
term() { printf '[Desktop Entry]\nType=Application\nName=%s\nExec=%s\nCategories=System;TerminalEmulator;\n%s' "$1" "$1" "$2"; }

echo "[EXP-I] newline-in-arg cache write (entry TerminalArgExec=\\n)"
R=$S/i1; rm -rf "$R"; mkenv $R
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
printf '[Desktop Entry]\nType=Application\nName=foot\nExec=foot\nCategories=System;TerminalEmulator;\nTerminalArgExec=\\n\n' > "$R/usr/share/applications/foot.desktop"
run $R --print-cmd -- sh -c 'echo hi' | head -c 200; echo
if [ -f "$R/home/.cache/xdg-terminal-exec" ]; then
  echo "cache-file: EXISTS size=$(wc -c < "$R/home/.cache/xdg-terminal-exec")"
  echo "-- cache lines (cat -A):"; head -c 300 "$R/home/.cache/xdg-terminal-exec" | cat -A
else echo "cache-file: ABSENT"; fi
echo "[EXP-I2] warm rerun same root"
run $R --print-cmd -- sh -c 'echo hi' | head -c 120; echo
echo "[EXP-I3] print-id cold leaves no cache"
R=$S/i3; rm -rf "$R"; mkenv $R
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
term foot '' > "$R/usr/share/applications/foot.desktop"
run $R --print-id
[ -f "$R/home/.cache/xdg-terminal-exec" ] && echo "print-id cache: EXISTS" || echo "print-id cache: ABSENT"
echo "[EXP-I4] print-content cold leaves no cache"
run $R --print-content >/dev/null
[ -f "$R/home/.cache/xdg-terminal-exec" ] && echo "print-content cache: EXISTS" || echo "print-content cache: ABSENT"
echo "[EXP-K] -id then +id -> still excluded (foot selected)"
R=$S/k1; rm -rf "$R"; mkenv $R
mkdir -p "$R/d1/applications"
term alacritty '' > "$R/home/.local/share/applications/alacritty.desktop"
term foot '' > "$R/d1/applications/foot.desktop"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/alacritty"; chmod +x "$R/bin/alacritty"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
printf -- '-alacritty.desktop\n+alacritty.desktop\n' > "$R/home/.config/xdg-terminals.list"
env HOME="$R/home" PATH="$R/bin" XDG_CONFIG_HOME="$R/home/.config" XDG_CONFIG_DIRS="$R/etc/xdg" \
    XDG_DATA_HOME="$R/home/.local/share" XDG_DATA_DIRS="$R/d1" XDG_CACHE_HOME="$R/home/.cache" \
    XDG_CURRENT_DESKTOP=Hyprland /usr/bin/timeout 20 /bin/sh "$P" --print-id 2>"$R/stderr"; echo "rc=$?"
echo "[EXP-L] +id then -id -> keeps (alacritty selected)"
R=$S/l1; rm -rf "$R"; mkenv $R
term alacritty '' > "$R/home/.local/share/applications/alacritty.desktop"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/alacritty"; chmod +x "$R/bin/alacritty"
printf -- '+alacritty.desktop\n-alacritty.desktop\n' > "$R/home/.config/xdg-terminals.list"
env HOME="$R/home" PATH="$R/bin" XDG_CONFIG_HOME="$R/home/.config" XDG_CONFIG_DIRS="$R/etc/xdg" \
    XDG_DATA_HOME="$R/home/.local/share" XDG_DATA_DIRS="$R/d1" XDG_CACHE_HOME="$R/home/.cache" \
    XDG_CURRENT_DESKTOP=Hyprland /usr/bin/timeout 20 /bin/sh "$P" --print-id 2>"$R/stderr"; echo "rc=$?"
