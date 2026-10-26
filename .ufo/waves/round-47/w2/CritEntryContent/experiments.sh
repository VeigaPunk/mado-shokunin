#!/bin/sh
set -u
S=/fast/scratch/hyaku/mado-r47/CritEntryContent/exp
P=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/fetch/xdg-terminal-exec
mkdir -p "$S"
mkenv() { R=$1; mkdir -p "$R/home/.config" "$R/etc/xdg" "$R/usr/share/applications" "$R/home/.local/share/applications" "$R/bin" "$R/home/.cache"
  for t in find awk tr ls md5sum mkdir rm; do ln -sf /usr/bin/$t "$R/bin/$t"; done; }
run() { R=$1; shift
  env HOME="$R/home" PATH="$R/bin" XDG_CONFIG_HOME="$R/home/.config" XDG_CONFIG_DIRS="$R/etc/xdg" \
      XDG_DATA_HOME="$R/home/.local/share" XDG_DATA_DIRS="$R/usr/share" XDG_CACHE_HOME="$R/home/.cache" \
      XDG_CURRENT_DESKTOP=Hyprland /usr/bin/timeout 20 /bin/sh "$P" "$@" 2>"$R/stderr"
  echo "rc=$?"; }
term() { printf '[Desktop Entry]\nType=Application\nName=%s\nExec=%s\nCategories=System;TerminalEmulator;\n%s' "$1" "$1" "$2"; }

echo "[EXP-B1] carryover a1(cats-only)+b2(exec-only)"; R=$S/b1; mkenv $R
printf 'a1.desktop\nb2.desktop\n' > "$R/home/.config/xdg-terminals.list"
printf '[Desktop Entry]\nCategories=TerminalEmulator;\n' > "$R/usr/share/applications/a1.desktop"
printf '[Desktop Entry]\nExec=foot\n' > "$R/usr/share/applications/b2.desktop"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
run $R --print-id
echo "[EXP-B2] b2 alone"; R=$S/b2; mkenv $R
printf 'b2.desktop\n' > "$R/home/.config/xdg-terminals.list"
printf '[Desktop Entry]\nExec=foot\n' > "$R/usr/share/applications/b2.desktop"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
run $R --print-id
echo "[EXP-C] tryexec builtin printf"; R=$S/c1; mkenv $R
term foot 'TryExec=printf\n' > "$R/usr/share/applications/foot.desktop"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
run $R --print-id
echo "[EXP-D] loop-status entry-header-last"; R=$S/d1; mkenv $R
printf 'Actions=act;\n[Desktop Action act]\nExec=foot\nCategories=TerminalEmulator;\n[Desktop Entry]\n' > "$R/usr/share/applications/b.desktop"
printf 'b.desktop:act\n' > "$R/home/.config/xdg-terminals.list"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
run $R --print-id
echo "[EXP-E] loop-status other-group-last"; R=$S/e1; mkenv $R
printf 'Categories=TerminalEmulator;\n[Other]\n' > "$R/usr/share/applications/b.desktop"
printf '[Desktop Entry]\nExec=foot\n' > "$R/usr/share/applications/a.desktop"
printf 'a.desktop\nb.desktop\n' > "$R/home/.config/xdg-terminals.list"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
run $R --print-id
echo "[EXP-F] no final newline"; R=$S/f1; mkenv $R
printf '[Desktop Entry]\nExec=foot\nCategories=TerminalEmulator;' > "$R/usr/share/applications/foot.desktop"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
run $R --print-id
echo "[EXP-G] dup data-dirs -> data-home path wins"; R=$S/g1; mkenv $R
term foot '' > "$R/usr/share/applications/foot.desktop"
term foot '' > "$R/home/.local/share/applications/foot.desktop"
printf 'foot.desktop\n' > "$R/home/.config/xdg-terminals.list"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
run $R --print-path
echo "[EXP-H] delimiters"; R=$S/h1; mkenv $R
term foot '' > "$R/usr/share/applications/foot.desktop"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
run $R --print-id --print-path --print-delimiter='|'
run $R --print-cmd=, -- htop -d 5
echo "[EXP-I] cache newline + print-id cache"
R=$S/i1; mkenv $R
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
printf '[Desktop Entry]\nType=Application\nName=foot\nExec=foot\nCategories=System;TerminalEmulator;\nTerminalArgExec=\\n\n' > "$R/usr/share/applications/foot.desktop"
run --print-cmd -- sh -c 'echo hi' 2>/dev/null || true
env HOME="$R/home" PATH="$R/bin" XDG_CONFIG_HOME="$R/home/.config" XDG_CONFIG_DIRS="$R/etc/xdg" \
    XDG_DATA_HOME="$R/home/.local/share" XDG_DATA_DIRS="$R/usr/share" XDG_CACHE_HOME="$R/home/.cache" \
    XDG_CURRENT_DESKTOP=Hyprland /usr/bin/timeout 20 /bin/sh "$P" --print-cmd -- sh -c 'echo hi' >/dev/null 2>&1
[ -f "$R/home/.cache/xdg-terminal-exec" ] && echo "cache-file: EXISTS size=$(wc -c < "$R/home/.cache/xdg-terminal-exec")" || echo "cache-file: ABSENT"
echo "-- cache byte lines (cat -A head):"; head -c 300 "$R/home/.cache/xdg-terminal-exec" | cat -A
R2=$S/i2; mkenv $R2
printf '#!/bin/sh\nexit 0\n' > "$R2/bin/foot"; chmod +x "$R2/bin/foot"
term foot '' > "$R2/usr/share/applications/foot.desktop"
env HOME="$R2/home" PATH="$R2/bin" XDG_CONFIG_HOME="$R2/home/.config" XDG_CONFIG_DIRS="$R2/etc/xdg" \
    XDG_DATA_HOME="$R2/home/.local/share" XDG_DATA_DIRS="$R2/usr/share" XDG_CACHE_HOME="$R2/home/.cache" \
    XDG_CURRENT_DESKTOP=Hyprland /usr/bin/timeout 20 /bin/sh "$P" --print-id
[ -f "$R2/home/.cache/xdg-terminal-exec" ] && echo "print-id cache: EXISTS" || echo "print-id cache: ABSENT"
echo "[EXP-K] -id then +id -> still excluded"
R=$S/k1; mkenv $R
term alacritty '' > "$R/home/.local/share/applications/alacritty.desktop"
term foot '' > "$R/d1/applications/foot.desktop"
mkdir -p "$R/d1/applications"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/alacritty"; chmod +x "$R/bin/alacritty"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/foot"; chmod +x "$R/bin/foot"
env XDG_CONFIG_HOME="$R/home/.config" XDG_CONFIG_DIRS="$R/etc/xdg" XDG_DATA_HOME="$R/home/.local/share" \
    XDG_DATA_DIRS="$R/d1" XDG_CACHE_HOME="$R/home/.cache" XDG_CURRENT_DESKTOP=Hyprland \
    HOME="$R/home" PATH="$R/bin" /usr/bin/timeout 20 /bin/sh "$P" --print-id <<'L' 2>/dev/null
L
printf '#!/bin/sh\nexit 0\n' > "$R/bin/nothing"; chmod +x "$R/bin/nothing"
printf -- '-alacritty.desktop\n+alacritty.desktop\n' > "$R/home/.config/xdg-terminals.list"
env HOME="$R/home" PATH="$R/bin" XDG_CONFIG_HOME="$R/home/.config" XDG_CONFIG_DIRS="$R/etc/xdg" \
    XDG_DATA_HOME="$R/home/.local/share" XDG_DATA_DIRS="$R/d1" XDG_CACHE_HOME="$R/home/.cache" \
    XDG_CURRENT_DESKTOP=Hyprland /usr/bin/timeout 20 /bin/sh "$P" --print-id 2>"$R/stderr"; echo "rc=$?"
echo "[EXP-L] +id then -id -> keeps"
R=$S/l1; mkenv $R
term alacritty '' > "$R/home/.local/share/applications/alacritty.desktop"
printf '#!/bin/sh\nexit 0\n' > "$R/bin/alacritty"; chmod +x "$R/bin/alacritty"
printf -- '+alacritty.desktop\n-alacritty.desktop\n' > "$R/home/.config/xdg-terminals.list"
env HOME="$R/home" PATH="$R/bin" XDG_CONFIG_HOME="$R/home/.config" XDG_CONFIG_DIRS="$R/etc/xdg" \
    XDG_DATA_HOME="$R/home/.local/share" XDG_DATA_DIRS="$R/d1" XDG_CACHE_HOME="$R/home/.cache" \
    XDG_CURRENT_DESKTOP=Hyprland /usr/bin/timeout 20 /bin/sh "$P" --print-id 2>"$R/stderr"; echo "rc=$?"
