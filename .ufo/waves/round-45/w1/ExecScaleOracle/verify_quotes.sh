#!/bin/sh
# verify_quotes.sh - every quote in report.md comes from this receipt: fixed-string
# grep over the frozen pins / draft, so the locators are computed, never typed.
set -eu
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/w1/ExecScaleOracle
W=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45
{
  q() { echo "--- $1"; shift; grep -nF -- "$1" "$2"; }
  q "MON-1001"   'searchScale = std::round(m_scale * 120.0);'          "$W/fetch/Hyprland-Monitor.cpp"
  q "MON-997"    'logicalSize.x != std::round(logicalSize.x)'           "$W/fetch/Hyprland-Monitor.cpp"
  q "MON-1035"   'm_scale = getDefaultScale();'                          "$W/fetch/Hyprland-Monitor.cpp"
  q "MON-1408"   'if (PPI > 200'                                         "$W/fetch/Hyprland-Monitor.cpp"
  q "MON-1413"   'return 1.5;'                                           "$W/fetch/Hyprland-Monitor.cpp"
  q "RULE-45"    'float                        m_scale         = -1;'    "$W/fetch/Hyprland-MonitorRule.hpp"
  q "PARSER-203" 'if (m_rule.m_scale < 0.25F) {'                         "$W/fetch/Hyprland-Parser.cpp"
  q "DRAFT-327"  'def expected_scale(s, w, h):'                          "$W/l1-draft/mado-monitors.py"
  q "DRAFT-323"  'def whole(x):'                                         "$W/l1-draft/mado-monitors.py"
  q "DRAFT-DOC"  'none found means the scale is not compared'            "$W/l1-draft/mado-monitors.py"
  q "DRAFT-385"  'if e is not None and abs(sc - e) >= 0.0001:'            "$W/l1-draft/mado-monitors.py"
  q "HYPRCTL-282" '"scale": {},'                                         "$W/fetch/Hyprland-HyprCtl.cpp"
} > "$SEAT/receipts/quotes.txt" 2>&1
cat "$SEAT/receipts/quotes.txt"
