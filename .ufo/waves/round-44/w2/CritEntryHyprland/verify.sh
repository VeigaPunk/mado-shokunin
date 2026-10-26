#!/usr/bin/env bash
# CritEntryHyprland verifier (round 44 w2).
# Every located quote used in w2/CritEntryHyprland.md must occur at the cited line of the pinned file.
# Usage: bash verify.sh [output-file]   (default: stdout)
set -u

LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
F="$LANE/.ufo/waves/round-44/fetch"
R="$LANE/.ufo/waves/round-44/receipts"
W="$F/Hyprland-Window.cpp"
X="$F/Hyprland-XDGShell.cpp"
OUT="${1:-/dev/stdout}"

n=0; fail=0
chk() { # $1 file, $2 line, $3 fixed-string needle
  local f="$1" ln="$2" needle="$3" got
  got=$(sed -n "${ln}p" "$f")
  n=$((n+1))
  if printf '%s' "$got" | grep -qF -- "$needle"; then
    printf 'OK   %02d %s:%s  %s\n' "$n" "${f##*/}" "$ln" "$needle" >>"$OUT"
  else
    printf 'FAIL %02d %s:%s  want[%s] got[%s]\n' "$n" "${f##*/}" "$ln" "$needle" "$got" >>"$OUT"
    fail=$((fail+1))
  fi
}

printf '# pins\n' >>"$OUT"
hs=$(sha256sum "$W" "$X")
printf '%s\n' "$hs" >>"$OUT"
for spec in "Hyprland-Window.cpp d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded" \
            "Hyprland-XDGShell.cpp d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0"; do
  set -- $spec
  n=$((n+1))
  if grep -qxF "$2  124226 fetch/$1" "$R/fetch-sha256.txt" || grep -q "^$2 .*fetch/$1\$" "$R/fetch-sha256.txt"; then
    printf 'OK   %02d receipt hash %s\n' "$n" "$1" >>"$OUT"
  else
    printf 'FAIL %02d receipt hash %s\n' "$n" "$1" >>"$OUT"; fail=$((fail+1))
  fi
done

printf '\n# Window.cpp\n' >>"$OUT"
chk "$W" 184  'm_listeners.ack'
chk "$W" 1514 'void CWindow::onAck(uint32_t serial) {'
chk "$W" 1515 'return e.first <= serial; });'
chk "$W" 1517 'if (SERIAL == m_pendingSizeAcks.rend())'
chk "$W" 1520 'm_pendingSizeAck = *SERIAL;'
chk "$W" 1521 'std::erase_if(m_pendingSizeAcks, [&](const auto& el) { return el.first <= SERIAL->first; });'
chk "$W" 1523 'if (m_isX11)'
chk "$W" 1526 'm_pending.ackedSize'
chk "$W" 1526 '= m_pendingSizeAck->second;'
chk "$W" 1527 'm_pending.updated.bits.acked = true;'
chk "$W" 1685 'Vector2D CWindow::realToReportSize() {'
chk "$W" 1687 'm_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);'
chk "$W" 1691 'clamp(Vector2D{1, 1}, Math::VECTOR2D_MAX);'
chk "$W" 1694 'if (*PXWLFORCESCALEZERO && PMONITOR)'
chk "$W" 1696 'return (REPORTSIZE * PMONITOR->m_scale).round();'
chk "$W" 1698 'return REPORTSIZE;'
chk "$W" 1699 '}'
chk "$W" 1732 'void CWindow::sendWindowSize(bool force) {'
chk "$W" 1741 'const auto REPORTSIZE = realToReportSize();'
chk "$W" 1743 'if (!force && m_pendingReportedSize == REPORTSIZE && (m_reportedPosition == REPORTPOS || !m_isX11))'
chk "$W" 1744 'return;'
chk "$W" 1751 'm_xwaylandSurface->configure({REPORTPOS, REPORTSIZE});'
chk "$W" 1753 'm_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());'
chk "$W" 1861 'Vector2D CWindow::getReportedSize() {'
chk "$W" 1863 'return m_reportedSize;'
chk "$W" 1865 'return m_wlSurface->resource()->m_current.ackedSize;'

printf '\n# XDGShell.cpp\n' >>"$OUT"
chk "$X" 130 'm_resource->sendConfigure(box.x, box.y, box.w, box.h);'
chk "$X" 132 'm_surface->scheduleConfigure();'
chk "$X" 354 'uint32_t CXDGToplevelResource::setSize(const Vector2D& size) {'
chk "$X" 355 'm_pendingApply.size = size;'
chk "$X" 356 'scheduleStateApplication();'
chk "$X" 357 'return m_owner->scheduleConfigure();'
chk "$X" 443 'void CXDGToplevelResource::scheduleStateApplication() {'
chk "$X" 445 'if (m_stateUpdate)'
chk "$X" 455 'm_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);'
chk "$X" 601 'm_resource->setAckConfigure([this](CXdgSurface* r, uint32_t serial) {'
chk "$X" 602 'if (serial < m_lastConfigureSerial)'
chk "$X" 603 'return;'
chk "$X" 604 'm_lastConfigureSerial = serial;'
chk "$X" 605 'm_events.ack.emit(serial);'
chk "$X" 629 'uint32_t CXDGSurfaceResource::scheduleConfigure() {'
chk "$X" 630 'if (m_stateUpdate)'
chk "$X" 631 'return m_scheduledSerial;'
chk "$X" 635 'm_scheduledSerial = wl_display_next_serial(g_pCompositor->m_wlDisplay);'
chk "$X" 637 'return m_scheduledSerial;'
chk "$X" 640 'void CXDGSurfaceResource::configure() {'
chk "$X" 641 'm_stateUpdate.reset();'
chk "$X" 642 'm_resource->sendConfigure(m_scheduledSerial);'

printf '\n# structural counts\n' >>"$OUT"
body=$(sed -n '1732,1754p' "$W")
cfg=$(printf '%s\n' "$body" | grep -c 'configure(')
siz=$(printf '%s\n' "$body" | grep -c 'setSize(')
n=$((n+1))
if [ "$cfg" = 1 ] && [ "$siz" = 1 ]; then
  printf 'OK   %02d witness hyprland sendWindowSize xdg_setSize=%s x11_configure=%s (Window.cpp:1732-1754)\n' "$n" "$siz" "$cfg" >>"$OUT"
else
  printf 'FAIL %02d witness counts configure=%s setSize=%s\n' "$n" "$cfg" "$siz" >>"$OUT"; fail=$((fail+1))
fi
n=$((n+1))
acked=$(grep -c 'ackedSize' "$W")
if [ "$acked" = 2 ]; then
  printf 'OK   %02d ackedSize in Window.cpp = %s lines (1526 write, 1865 read)\n' "$n" "$acked" >>"$OUT"
else
  printf 'FAIL %02d ackedSize in Window.cpp = %s, want 2\n' "$n" "$acked" >>"$OUT"; fail=$((fail+1))
fi
n=$((n+1))
ackedx=$(grep -c 'ackedSize' "$X")
if [ "$ackedx" = 0 ]; then
  printf 'OK   %02d ackedSize in XDGShell.cpp = %s\n' "$n" "$ackedx" >>"$OUT"
else
  printf 'FAIL %02d ackedSize in XDGShell.cpp = %s, want 0\n' "$n" "$ackedx" >>"$OUT"; fail=$((fail+1))
fi
n=$((n+1))
acksend=$(sed -n '1514,1529p' "$W" | grep -c 'send\|emit')
if [ "$acksend" = 0 ]; then
  printf 'OK   %02d onAck body (Window.cpp:1514-1529) sends/emits nothing to the client = %s\n' "$n" "$acksend" >>"$OUT"
else
  printf 'FAIL %02d onAck body send/emit hits = %s, want 0\n' "$n" "$acksend" >>"$OUT"; fail=$((fail+1))
fi

printf '\n# C2 declared residuals\n' >>"$OUT"
chk "$LANE/quality/counters/c2-r44-gkeep-size-request-v2.py" 65 'a true quote at a true locator can stand beside a claim it does'
chk "$LANE/quality/counters/c2-r44-gkeep-size-request-v2.py" 66 'not support'
chk "$LANE/quality/counters/c2-r44-gkeep-size-request-v2.py" 67 'clause j binds a locator and a'
chk "$LANE/quality/counters/c2-r44-gkeep-size-request-v2.py" 68 'not the truth of the sentence around them'

printf '\nCHECKS=%d FAILURES=%d\n' "$n" "$fail" >>"$OUT"
printf 'CHECKS=%d FAILURES=%d\n' "$n" "$fail"
[ "$fail" -eq 0 ]
