#!/bin/bash
# Round 50, seat ExecFetchR50: re-fetch every source pinned by round-49 rows S352-S363 and every pin in
# .ufo/waves/round-49/fetch/, and compare each byte-for-byte with the round-49 pin.
#
# Usage: WORKDIR=<dir outside /tmp /var/tmp /dev/shm> LANE=<lane root> ./fetch-all.sh
# Writes: $LANE/.ufo/waves/round-50/w1/ExecFetchR50/fetch/<basename> and fetch-manifest.tsv
# Every fetch is a commit or tag URL on raw.githubusercontent.com (never a branch).
set -uo pipefail
ulimit -f 65536
S=${WORKDIR:?set WORKDIR to a scratch dir outside /tmp, /var/tmp, /dev/shm}
case "$S" in /tmp/*|/var/tmp/*|/dev/shm/*) echo "refusing work dir under $S" >&2; exit 2;; esac
LANE=${LANE:-/home/vgpnk/Projects/shokunin/mado-shokunin}
SEAT=$LANE/.ufo/waves/round-50/w1/ExecFetchR50
R49=$LANE/.ufo/waves/round-49/fetch
mkdir -p "$S/tmp" "$SEAT/fetch"
export TMPDIR="$S/tmp"
MAN="$SEAT/fetch-manifest.tsv"
printf 'basename\turl\thttp_status\tbytes\tlines\tsha256\tpin_r49_sha256\tequal\taccessed_utc\n' > "$MAN"
fail=0
while IFS=$'\t' read -r base url; do
  [ -z "${base:-}" ] && continue
  out="$S/dl-$base"
  code=$(curl -sS --max-time 180 -o "$out" -w '%{http_code}' "$url") || code="curl-error"
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  if [ "$code" != "200" ]; then
    printf '%s\t%s\t%s\t-\t-\t-\t-\tNO-FETCH\t%s\n' "$base" "$url" "$code" "$ts" >> "$MAN"
    fail=$((fail+1)); continue
  fi
  cp -- "$out" "$SEAT/fetch/$base"
  bytes=$(stat -c %s "$SEAT/fetch/$base")
  lines=$(wc -l < "$SEAT/fetch/$base")
  sha=$(sha256sum "$SEAT/fetch/$base" | cut -d' ' -f1)
  pin=$(sha256sum "$R49/$base" | cut -d' ' -f1)
  eq=no; [ "$sha" = "$pin" ] && eq=yes || fail=$((fail+1))
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$base" "$url" "$code" "$bytes" "$lines" "$sha" "$pin" "$eq" "$ts" >> "$MAN"
done <<'EOF'
Hyprland-KeybindManager.cpp	https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp
Hyprland-legacy-ConfigManager.cpp	https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp
Hyprland-InputManager.cpp	https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/input/InputManager.cpp
xkbcommon-keysym.c	https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/keysym.c
xkbcommon-keysym.h	https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/keysym.h
xkbcommon-ks_tables.h	https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/ks_tables.h
xkbcommon-tools-how-to-type.c	https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/tools/how-to-type.c
xkbcommon-xkbcommon-keysyms.h	https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/include/xkbcommon/xkbcommon-keysyms.h
wiki-Binds.md	https://raw.githubusercontent.com/hyprwm/hyprland-wiki/d5f07c60e16fe03744aabb76e492117b7f7c4679/content/Configuring/Basics/Binds.md
wiki-Variables.md	https://raw.githubusercontent.com/hyprwm/hyprland-wiki/d5f07c60e16fe03744aabb76e492117b7f7c4679/content/Configuring/Basics/Variables.md
xkbcommon-state.c	https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/state.c
Hyprland-IKeyboard.hpp	https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/IKeyboard.hpp
Hyprland-IKeyboard.cpp	https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/devices/IKeyboard.cpp
Hyprland-ConfigValues.cpp	https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/values/ConfigValues.cpp
EOF
echo "manifest_rows=$(( $(wc -l < "$MAN") - 1 )) failures=$fail"
[ "$fail" -eq 0 ]
