#!/bin/sh
# Repro 1 (round 47 w2, ExecC1Determinism): the resolver's fallback order is the reverse of
# `LC_ALL=C find -L` output (pin x:790 prepend, x:795 find), i.e. readdir order; the selected id
# can therefore flip with the filesystem. The reference tool mirrors the real order (os.scandir,
# l1-draft/mado-terminal.py:506), so it agrees with the pin on both filesystems.
# usage: repro-readdir-order.sh <xfs-base> <tmpfs-base>
#   both bases must be writable directories outside the lane (e.g. /fast/scratch/... and /dev/shm/...)
set -eu
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
X=${1:?xfs base}; T=${2:?tmpfs base}
PIN=$X/pin
cp "$LANE/.ufo/waves/round-47/fetch/xdg-terminal-exec" "$PIN"
chmod 755 "$PIN"
TOOL=$LANE/.ufo/waves/round-47/l1-draft/mado-terminal.py
sha256sum "$PIN" "$TOOL"

mk() { # mk <root>: two entries whose Exec[0] both resolve; created zeta first, alpha second
  R=$1; rm -rf "$R"
  mkdir -p "$R/home/.local/share/applications" "$R/home/.config" "$R/.rw/cache" "$R/bin"
  for n in zeta alpha; do
    printf '[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=%s\nName=%s\n' "$n" "$n" \
      > "$R/home/.local/share/applications/$n.desktop"
    printf '#!/bin/sh\nexit 1\n' > "$R/bin/$n"; chmod 755 "$R/bin/$n"
  done
}

for base in "$X/order" "$T/order"; do
  R=$base/r; mk "$R"
  echo "== $base fstype=$(stat -f -c %T "$base")"
  echo "-- find -L order (pin x:795):"; find -L "$R/home/.local/share/applications/." -type f | sed 's#.*/\./##'
  E="env -i HOME=$R/home PATH=$R/bin:/usr/bin:/bin XDG_CONFIG_HOME=$R/home/.config XDG_CONFIG_DIRS=$R/etc/xdg"
  E="$E XDG_DATA_HOME=$R/home/.local/share XDG_DATA_DIRS=$R/usr/share XDG_CURRENT_DESKTOP=Hyprland"
  E="$E XDG_CACHE_HOME=$R/.rw/cache"
  for L in C.UTF-8 en_US.UTF-8; do
    printf -- '-- pin  LANG=%s: ' "$L"; $E LANG=$L "$PIN" --print-id 2>/dev/null; echo "   rc=$?"
  done
  printf -- '-- tool LANG=C.UTF-8: '; $E LANG=C.UTF-8 python3 -I "$TOOL" print --print-id 2>/dev/null; echo "   rc=$?"
done
