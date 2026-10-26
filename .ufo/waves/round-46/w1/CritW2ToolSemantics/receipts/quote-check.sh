#!/bin/sh
S=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/CritW2ToolSemantics/receipts
# quote check: every citation used in the report -> source:line must contain the needle
P45=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/fetch
P46=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/fetch
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
: # tool-at-tip.py is the blob of tools/mado-monitors.py at 4d22eeb, copied here
chk(){ f="$1"; n="$2"; needle="$3"; got=$(sed -n "${n}p" "$f"); case "$got" in *"$needle"*) echo "PASS $4 $f:$n";; *) echo "FAIL $4 $f:$n want[$needle] got[$got]";; esac; }
chk "$S/tool-at-tip.py" 116 'monitorv2(?:[ \t={]|$)'            "V2_RE misses bracket form"
chk "$S/tool-at-tip.py" 100 'NOT_COMPARED (exit 5, v2 > 0,'      "docstring v2 gate promise"
chk "$S/tool-at-tip.py" 422 'mo == str(ids[0])'                   "mirror compared by dump name"
chk "$S/tool-at-tip.py" 20  'compared: vrr, bitdepth, cm'         "not-compared list"
chk "$S/tool-at-tip.py" 36  'Config files are read in argument order' "no source handling"
chk "$S/tool-at-tip.py" 60  'starting `auto` is auto'             "auto position declared"
chk "$P46/Hyprland-ConfigManager.cpp" 567 'addSpecialCategory("monitorv2"' "special category key output"
chk "$P46/Hyprland-ConfigManager.cpp" 743 'const auto ERR = m_config->parse();' "parse legacy lines first"
chk "$P46/Hyprland-ConfigManager.cpp" 747 'handleMonitorv2();'    "v2 rules added after parse"
chk "$P46/Hyprland-ConfigManager.cpp" 883 'listKeysForSpecialCategory("monitorv2")' "v2 keys iterated"
chk "$P46/Hyprland-ConfigManager.cpp" 876 'monitorRuleMgr()->add'  "v2 rule added to the same manager"
chk "$P46/hyprlang-config.cpp" 291 'valueName.contains' "bracket special-category key"
chk "$P46/wiki-Keywords.md" 121 'device[my-device]' "bracket form documented for device"
chk "$P45/Hyprland-Monitor.cpp" 1204 'trim(selector.substr(5))' "desc: text trimmed"
chk "$P45/Hyprland-Monitor.cpp" 1335 'configString(mirrorOf)' "mirror target via query"
chk "$P45/Hyprland-Monitor.cpp" 1341 'Cannot mirror a mirror!' "mirror-of-mirror refused"
chk "$P45/Hyprland-Monitor.cpp" 1346 'Cannot mirror self!' "self mirror refused"
chk "$P45/Hyprland-Monitor.cpp" 1386 'm_position = PMIRRORMON->m_position;' "mirror position overwritten"
chk "$P45/Hyprland-MonitorPositionController.cpp" 68 'DIR_AUTO_LEFT: newPosition.x = maxXOffsetLeft' "auto-left computable"
chk "$P45/Hyprland-MonitorRule.hpp" 44 'm_offset        = Vector2D(-INT32_MAX, -INT32_MAX)' "default rule pos auto"
chk "$P45/Hyprland-legacy-ConfigManager.cpp" 1323 'std::stoi(std::string{ARGS[2]})' "addreserved stoi fields"
chk "$P45/Hyprland-legacy-ConfigManager.cpp" 1341 'monitorRuleMgr()->add' "addreserved fall-through adds default rule"
chk "$S/tool-at-tip.py" 18 'join, not a blame'                 "differ-cause list"
chk "$P45/Hyprland-MonitorRule.hpp" 41 'm_autoDir       = DIR_AUTO_NONE' "default auto dir"
chk "$P45/Hyprland-MonitorRuleManager.cpp" 38 'e.m_name == x.m_name' "add erases same selector"
chk "$P45/Hyprland-HyprCtl.cpp" 285 '(m->m_enabled ? "false" : "true")' "disabled flag is !m_enabled"
chk "$P45/Hyprland-Monitor.cpp" 752 'm_transform = RULE->m_transform;' "transform applied from rule"
chk "$P46/Hyprland-ConfigManager.cpp" 614 'registerHandler(&::handleSource, "source"' "source handler"
