#!/usr/bin/env bash
# ScrRowsDraft quote check: every quote this seat's report uses is <=25 words, occurs verbatim in
# the verifier receipt check-anchors.out, and is cited there next to the file:line it claims.
set -u
D=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/w1/ScrRowsDraft
RCPT=$D/check-anchors.out
fail=0
q() { # q "<quote>" "<echo anchor>" "<label>"
  local w; w=$(printf '%s' "$1" | wc -w)
  if [ "$w" -gt 25 ]; then echo "FAIL words=$w >25 [$3]"; fail=$((fail+1)); return; fi
  if ! grep -F -- "$1" "$RCPT" | grep -Fq -- "$2"; then echo "FAIL quote not found at [$2] in check-anchors.out [$3]"; fail=$((fail+1)); return; fi
  printf 'PASS words=%s at %s [%s] %s\n' "$w" "$2" "$3" "$1"
}
q 'uint32_t CXDGToplevelResource::setSize(const Vector2D& size) {' 'Hyprland-XDGShell.cpp:354' 'S298 setSize'
q 'm_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);' 'Hyprland-XDGShell.cpp:455' 'S298 sendConfigure'
q 'Clients must send an ack_configure in response to this event. See' 'xdg-shell.xml:1166' 'S299 ack duty'
q 'if (saved_size && !fixed_size && was_fixed_size)' 'gdktoplevel-wayland.c:656' 'S300 restore branch'
q 'window.set_default_size(420, 500)' 'gkeep-ui.py:476' 'S301 default size'
echo "SUMMARY quote-failures=$fail"
[ "$fail" = 0 ] || exit 1
