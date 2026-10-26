#!/usr/bin/env bash
# ScrRowsDraft anchor verifier (round 44, w1). Read-only against the lane pins.
# Parts: (1) file:line needle checks on the pinned bytes; (2) cited-locator checks on the row cell
# (every cited number inside the file, every cited first number needle-checked); (3) clause-e
# containment (location's last path component vs receipt file name). No scratch dir needed.
set -u
L=/home/vgpnk/Projects/shokunin/mado-shokunin
F="$L/.ufo/waves/round-44/fetch"
D="$L/.ufo/waves/round-44/w1/ScrRowsDraft"
R="${ROWS_BLOCK:-$D/rows-block.txt}"
fail=0
TMPV=$(mktemp -p "$D") || { echo 'SETUP FAIL mktemp TMPV'; exit 2; }
trap 'rm -f -- "$TMPV"' EXIT
: > "$TMPV" || { echo 'SETUP FAIL TMPV unwritable'; exit 2; }
[ -r "$R" ] || { echo "SETUP FAIL rows block unreadable: $R"; exit 2; }

chk() { # chk <file> <line> <needle> <label>
  local got; got=$(awk -v n="$2" 'NR==n' "$1")
  printf '%s:%s\n' "$(basename "$1")" "$2" >> "$TMPV" || { echo 'SETUP FAIL TMPV write'; exit 2; }
  if printf '%s' "$got" | grep -qF -- "$3"; then printf 'PASS %s:%s holds [%s]\n' "$(basename "$1")" "$2" "$4"
  else printf 'FAIL %s:%s lacks [%s] :: %s\n' "$(basename "$1")" "$2" "$4" "$got"; fail=$((fail+1)); fi
}

echo '== S298 fetch/Hyprland-XDGShell.cpp'
chk "$F/Hyprland-XDGShell.cpp" 354 'CXDGToplevelResource::setSize' 'setSize definition'
chk "$F/Hyprland-XDGShell.cpp" 443 'scheduleStateApplication' 'scheduleStateApplication definition'
chk "$F/Hyprland-XDGShell.cpp" 455 'sendConfigure(m_pendingApply.size.x' 'the pending size leaves in one sendConfigure'
chk "$F/Hyprland-XDGShell.cpp" 601 'setAckConfigure' 'the ack hook'
chk "$F/Hyprland-XDGShell.cpp" 629 'CXDGSurfaceResource::scheduleConfigure' 'scheduleConfigure definition'
chk "$F/Hyprland-XDGShell.cpp" 635 'wl_display_next_serial' 'the serial is minted here'
chk "$F/Hyprland-XDGShell.cpp" 640 'CXDGSurfaceResource::configure' 'configure definition'
chk "$F/Hyprland-XDGShell.cpp" 642 'sendConfigure(m_scheduledSerial)' 'configure performs the send'

echo '== S299 fetch/xdg-shell.xml'
chk "$F/xdg-shell.xml" 560 'name="ack_configure"' 'ack_configure request'
chk "$F/xdg-shell.xml" 598 '<event name="configure">' 'xdg_surface configure event'
chk "$F/xdg-shell.xml" 615 'discard all but the last' 'may discard all but the last'
chk "$F/xdg-shell.xml" 1144 '<event name="configure">' 'xdg_toplevel configure event'
chk "$F/xdg-shell.xml" 1150 'specify a hint to the window' 'width and height are a hint'
chk "$F/xdg-shell.xml" 1154 'are zero' 'zero means the client decides'
chk "$F/xdg-shell.xml" 1166 'must send an ack_configure' 'clients must ack'
chk "$F/xdg-shell.xml" 1169 '<arg name="width"' 'width argument'
chk "$F/xdg-shell.xml" 1170 '<arg name="height"' 'height argument'
chk "$F/xdg-shell.xml" 409 '<interface name="xdg_surface" version="7">' 'xdg_surface version 7'
chk "$F/xdg-shell.xml" 622 '<interface name="xdg_toplevel" version="7">' 'xdg_toplevel version 7'

echo '== S300 fetch/gdktoplevel-wayland.c'
chk "$F/gdktoplevel-wayland.c" 606 'gdk_wayland_toplevel_handle_configure' 'configure handler'
chk "$F/gdktoplevel-wayland.c" 633 'fixed_size =' 'fixed_size assignment'
chk "$F/gdktoplevel-wayland.c" 635 'GDK_TOPLEVEL_STATE_FULLSCREEN' 'fullscreen in fixed_size'
chk "$F/gdktoplevel-wayland.c" 636 'GDK_TOPLEVEL_STATE_TILED' 'tiled in fixed_size'
chk "$F/gdktoplevel-wayland.c" 639 'was_fixed_size =' 'was_fixed_size assignment'
chk "$F/gdktoplevel-wayland.c" 644 'pending.width' 'pending width'
chk "$F/gdktoplevel-wayland.c" 645 'pending.height' 'pending height'
chk "$F/gdktoplevel-wayland.c" 647 'saved_size = (width == 0 && height == 0)' 'zero as saved_size'
chk "$F/gdktoplevel-wayland.c" 656 'if (saved_size && !fixed_size && was_fixed_size)' 'restore branch'
chk "$F/gdktoplevel-wayland.c" 658 'saved_width' 'restored width'
chk "$F/gdktoplevel-wayland.c" 662 'if (width > 0 && height > 0)' 'positive-size branch'
chk "$F/gdktoplevel-wayland.c" 680 'size_is_fixed = fixed_size' 'size_is_fixed'
chk "$F/gdktoplevel-wayland.c" 681 'configured_width = width' 'configured_width'
chk "$F/gdktoplevel-wayland.c" 683 '}' 'branch closes'
chk "$F/gdktoplevel-wayland.c" 382 'gdk_wayland_toplevel_update_size' 'update_size definition'
chk "$F/gdktoplevel-wayland.c" 441 'gdk_wayland_surface_update_size' 'update_size applies the size'

echo '== S301 fetch/gkeep-ui.py'
chk "$F/gkeep-ui.py" 446 'class GkeepApp' 'GkeepApp'
chk "$F/gkeep-ui.py" 449 'application_id="org.omarchy.gkeep"' 'application id'
chk "$F/gkeep-ui.py" 472 'def do_activate' 'do_activate'
chk "$F/gkeep-ui.py" 475 'set_decorated(False)' 'undecorated'
chk "$F/gkeep-ui.py" 476 'set_default_size(420, 500)' 'the default size'
n=$(grep -c 'set_size_request(' "$F/gkeep-ui.py" || true)
[ "$n" = 0 ] && echo 'PASS gkeep-ui.py set_size_request( occurrences = 0' || { echo "FAIL set_size_request count=$n"; fail=$((fail+1)); }

echo '== sizes and hashes against receipts/fetch-sha256.txt'
for f in Hyprland-XDGShell.cpp xdg-shell.xml gdktoplevel-wayland.c gkeep-ui.py; do
  got=$(sha256sum "$F/$f" | cut -d' ' -f1)
  want=$(grep -E "^[0-9a-f]{64} [0-9]+ fetch/$f\$" "$L/.ufo/waves/round-44/receipts/fetch-sha256.txt" | cut -d' ' -f1)
  byt=$(wc -c < "$F/$f")
  wby=$(grep -E "^[0-9a-f]{64} [0-9]+ fetch/$f\$" "$L/.ufo/waves/round-44/receipts/fetch-sha256.txt" | cut -d' ' -f2)
  if [ "$got" = "$want" ] && [ "$byt" = "$wby" ]; then echo "PASS $f sha256 $got bytes $byt";
  else echo "FAIL $f sha256 $got (pin $want) bytes $byt (pin $wby)"; fail=$((fail+1)); fi
done

echo '== clause-e containment: location last path component vs receipt file name'
while IFS=$'\t' read -r id src anch; do
  id=$(printf '%s' "$id" | tr -d '[:space:]')
  case "$id" in S164) echo "SKIP S164 clause e applies to new ids only; the held row keeps its BASE anchor"; continue;; esac
  loc=$(printf '%s\n' "$src" | awk '{print $NF}')
  comp=$(printf '%s' "${loc%%\#*}" | awk -F/ '{print $NF}' | tr 'A-Z' 'a-z')
  rec=$(printf '%s\n' "$anch" | grep -oE '\.ufo/waves/round-44/fetch/[A-Za-z0-9._-]+' | head -1 | awk -F/ '{print $NF}' | tr 'A-Z' 'a-z')
  if [ -z "$rec" ]; then echo "FAIL $id no receipt path in the anchor cell"; fail=$((fail+1)); continue; fi
  case "$rec" in *"$comp"*) ok=1;; *) case "$comp" in *"$rec"*) ok=1;; *) ok=0;; esac;; esac
  if [ "$ok" = 1 ]; then echo "PASS $id location=$comp receipt=$rec (one contains the other)"
  else echo "FAIL $id location=$comp receipt=$rec"; fail=$((fail+1)); fi
done < <(awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ {print $2 "\t" $3 "\t" $7}' "$R")

echo '== cited locators: range check and echo of the cited line (new rows)'
while IFS=$'\t' read -r id anch; do
  id=$(printf '%s' "$id" | tr -d '[:space:]')
  f=$(printf '%s\n' "$anch" | grep -oE '\.ufo/waves/round-44/fetch/[A-Za-z0-9._-]+' | head -1 | awk -F/ '{print $NF}')
  if [ -z "$f" ]; then echo "FAIL $id no receipt path"; fail=$((fail+1)); continue; fi
  nlines=$(wc -l < "$F/$f")
  toks=$(printf '%s' "$anch" | grep -oE '([A-Za-z0-9._/-]+)?:[0-9]+(-[0-9]+)?' | grep -v 'sha256:')
  if [ -z "$toks" ]; then echo "FAIL $id anchor cell cites no locator"; fail=$((fail+1)); continue; fi
  while read -r r; do
    [ -n "$r" ] || continue
    if [ "$r" -le 0 ] || [ "$r" -gt "$nlines" ]; then echo "FAIL $id cites $f:$r beyond the file's $nlines lines"; fail=$((fail+1)); fi
  done < <(printf '%s\n' "$toks" | awk -F: '{print $NF}' | tr '-' '\n')
  while IFS= read -r tok; do
    seg=${tok##*:}; first=${seg%%-*}
    grep -qxF "$f:$first" "$TMPV" || { echo "FAIL $id cites $f:$first with no semantic needle check"; fail=$((fail+1)); }
    printf 'ECHO %s %s:%s | %s\n' "$id" "$f" "$first" "$(awk -v k="$first" 'NR==k' "$F/$f" | cut -c1-110)"
  done < <(printf '%s\n' "$toks")
done < <(awk -F'|' '/^\|[[:space:]]*S(298|299|300|301)[[:space:]]*\|/ {print $2 "\t" $7}' "$R")

echo "SUMMARY failures=$fail"
[ "$fail" = 0 ] && exit 0 || exit 1
