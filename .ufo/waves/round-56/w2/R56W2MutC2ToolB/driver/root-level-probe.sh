#!/usr/bin/env bash
# R56W2MutC2ToolB: root-level config probe for mutants m75 / m76 (cannot be staged in the C2 layout).
# usage: root-level-probe.sh PRISTINE_TOOL MUTANT_TOOL...   (needs bwrap; writes only under a mktemp dir it removes)
set -eu
D=$(mktemp -d)
trap 'rm -rf "$D"' EXIT
mkdir -p "$D/sub"
printf 'source = sub/x.conf\n' > "$D/hyprland.conf"      # cur=/hyprland.conf: curdir "" (m75 bound)
printf 'source = ../a.conf\n' > "$D/sub/x.conf"          # cur=/sub/x.conf: one-level curdir (m76 bound)
printf 'a = 1\n' > "$D/a.conf"
run() {
  bwrap --unshare-all --die-with-parent --tmpfs / --ro-bind /usr /usr --symlink usr/lib /lib \
    --symlink usr/lib64 /lib64 --symlink usr/bin /bin --dev /dev --proc /proc \
    --ro-bind "$D/hyprland.conf" /hyprland.conf --ro-bind "$D/sub" /sub --ro-bind "$D/a.conf" /a.conf \
    --ro-bind "$1" /tool.py --chdir / /usr/bin/python3 -I /tool.py --config /hyprland.conf
}
for t in "$@"; do
  echo "== $(basename "$t")"
  run "$t" || echo "rc=$?"
done
