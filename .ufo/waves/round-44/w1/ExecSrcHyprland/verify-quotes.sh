#!/usr/bin/env bash
# ExecSrcHyprland, round-44 w1: verify every quote in facts.md against the pins.
# Each check: the quote must literally occur in the pin file, and the cited line
# number must be among the `grep -n` hits for that quote.
set -u
F=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/fetch
L=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/w1/ExecSrcHyprland/facts.md
fail=0; n=0

chk() { # id file line quote
  local id=$1 file=$2 line=$3 quote=$4 hits
  n=$((n+1))
  hits=$(grep -nF -- "$quote" "$F/$file" | cut -d: -f1 | tr '\n' ' ')
  if [ -z "$hits" ]; then
    printf 'FAIL %-4s %-22s %5s  QUOTE ABSENT: %s\n' "$id" "$file" "$line" "$quote"; fail=$((fail+1)); return
  fi
  if ! printf '%s\n' $hits | grep -qx "$line"; then
    printf 'FAIL %-4s %-22s %5s  quote lives at [%s], not %s\n' "$id" "$file" "$line" "$hits" "$line"; fail=$((fail+1)); return
  fi
  if ! grep -qF -- "$(printf '%s' "$quote" | sed 's/|/\\|/g')" "$L" && ! grep -qF -- "$quote" "$L"; then
    printf 'FAIL %-4s %-22s %5s  quote not present in facts.md\n' "$id" "$file" "$line"; fail=$((fail+1)); return
  fi
  printf 'PASS %-4s %-22s %5s  [%s]\n' "$id" "$file" "$line" "$hits"
}

W=Hyprland-Window.cpp
X=Hyprland-XDGShell.cpp

chk F1  $W 1687 'return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);'
chk F2  $W 1691 'const auto  REPORTSIZE = m_realSize->goal().clamp(Vector2D{1, 1}, Math::VECTOR2D_MAX);'
chk F3  $W 1732 'void CWindow::sendWindowSize(bool force) {'
chk F4  $W 1743 'if (!force && m_pendingReportedSize == REPORTSIZE && (m_reportedPosition == REPORTPOS || !m_isX11))'
chk F5  $W 1751 'm_xwaylandSurface->configure({REPORTPOS, REPORTSIZE});'
chk F6  $W 1753 'm_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());'
chk F7  $W 1515 'const auto SERIAL = std::ranges::find_if(m_pendingSizeAcks | std::views::reverse, [serial](const auto& e) { return e.first <= serial; });'
chk F8  $W 1517 'if (SERIAL == m_pendingSizeAcks.rend())'
chk F9  $W 1521 'std::erase_if(m_pendingSizeAcks, [&](const auto& el) { return el.first <= SERIAL->first; });'
chk F10 $W 1523 'if (m_isX11)'
chk F11 $W 1526 'm_pending.ackedSize'
chk F12 $W 1528 'm_pendingSizeAck.reset();'
chk F13 $W 1865 'return m_wlSurface->resource()->m_current.ackedSize;'
chk F14 $W 184  'm_listeners.ack              = m_xdgSurface->m_events.ack.listen([this](uint32_t d) { onAck(d); });'
chk F15 $W 809  'sendWindowSize();'
chk F16 $W 1559 'sendWindowSize(true);'
chk F17 $W 2852 'sendWindowSize(true);'
chk F18 $X 355  'm_pendingApply.size = size;'
chk F19 $X 357  'return m_owner->scheduleConfigure();'
chk F20 $X 445  'if (m_stateUpdate)'
chk F21 $X 455  'm_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);'
chk F22 $X 635  'm_scheduledSerial = wl_display_next_serial(g_pCompositor->m_wlDisplay);'
chk F23 $X 642  'm_resource->sendConfigure(m_scheduledSerial);'
chk F24 $X 602  'if (serial < m_lastConfigureSerial)'
chk F25 $X 605  'm_events.ack.emit(serial);'
chk F26 $X 519  'm_current = m_pending;'
chk F26b $W 1527 'm_wlSurface->resource()->m_pending.updated.bits.acked = true;'
chk F27 $X 610  'm_pending.geometry = {x, y, w, h};'
chk F28 $W 2732 'm_xdgSurface->m_toplevel->setSize(predSize);'
chk F29 $W 1280 'const Vector2D NEWSIZE  = REALSIZE.clamp(minSize.value_or(Vector2D{MIN_WINDOW_SIZE, MIN_WINDOW_SIZE}), MAX);'

echo "--- function locators ---"
loc() { local q=$1 file=$2 want=$3 got; n=$((n+1))
  got=$(grep -nF -- "$q" "$F/$file" | cut -d: -f1 | tr '\n' ' ')
  if printf '%s\n' $got | grep -qx "$want"; then printf 'PASS %-44s %s\n' "$q" "$want"
  else printf 'FAIL %-44s want %s got [%s]\n' "$q" "$want" "$got"; fail=$((fail+1)); fi; }

loc 'Vector2D CWindow::realToReportSize() {'            $W 1685
loc 'void CWindow::onAck(uint32_t serial) {'             $W 1514
loc 'void CWindow::onMap() {'                            $W 759
loc 'void CWindow::onX11ConfigureRequest(CBox box) {'    $W 1544
loc 'void CWindow::unmanagedSetGeometry() {'             $W 2839
loc 'bool CWindow::clampWindowSize'                      $W 1277
loc 'Vector2D CWindow::getReportedSize() {'              $W 1861
loc 'uint32_t CXDGToplevelResource::setSize(const Vector2D& size) {'  $X 354
loc 'void CXDGToplevelResource::scheduleStateApplication() {'         $X 443
loc 'uint32_t CXDGSurfaceResource::scheduleConfigure() {'             $X 629
loc 'void CXDGSurfaceResource::configure() {'                         $X 640

echo "--- pin hashes ---"
sha256sum -c <<'EOF' || fail=$((fail+1))
d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/fetch/Hyprland-Window.cpp
d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/fetch/Hyprland-XDGShell.cpp
EOF

echo "--- negative-fact checks (must be EMPTY / must match the stated count) ---"
printf 'N1 m_realSize hits in W: %s\n' "$(grep -c 'm_realSize' "$F/$W")"
printf 'N2 ackedSize hits across pins: %s ->\n' "$(grep -rn 'ackedSize' "$F"/*.cpp | wc -l)"
grep -rn 'ackedSize' "$F"/*.cpp
printf 'N3 geometry() hits in W: %s (expect 0)\n' "$(grep -c 'geometry()' "$F/$W")"
printf 'N4 m_pendingSizeAcks hits in W: %s ->\n' "$(grep -c 'm_pendingSizeAcks' "$F/$W")"
grep -n 'm_pendingSizeAcks' "$F/$W"
printf 'N5 reportedSize hits in W: %s\n' "$(grep -c 'reportedSize' "$F/$W")"
printf 'N6 m_pendingApply in X (no initializer line): %s\n' "$(grep -c 'm_pendingApply' "$F/$X")"
printf 'N7 gtk/gkeep/default_size hits: %s (expect 0)\n' "$(grep -ic 'gtk\|gkeep\|default_size' "$F/$W" "$F/$X" | paste -sd' ')"
printf 'N8 error( calls in X: %s ->\n' "$(grep -c 'error(' "$F/$X")"
grep -n 'error(' "$F/$X"
printf 'N11 updated.bits.acked hits W/X: %s ->\n' "$(grep -c 'updated.bits.acked' "$F/$W")"
grep -n 'updated.bits.acked' "$F/$W"
printf 'N11 updated.bits.acked hits in X: %s (expect 0)\n' "$(grep -c 'updated.bits.acked' "$F/$X")"
printf 'site-count sendWindowSize W/X: %s / %s (expect 5 / 0)\n' "$(grep -c 'sendWindowSize' "$F/$W")" "$(grep -c 'sendWindowSize' "$F/$X")"
printf 'site-count setSize in W: %s (expect 2 -> W:1753, W:2732)\n' "$(grep -c 'setSize(' "$F/$W")"
printf 'N10 doLaterLock hits: %s\n' "$(grep -c 'doLaterLock' "$F/$X")"
grep -n 'doLaterLock' "$F/$X"

echo "CHECKS=$n FAILURES=$fail"
[ "$fail" -eq 0 ]
