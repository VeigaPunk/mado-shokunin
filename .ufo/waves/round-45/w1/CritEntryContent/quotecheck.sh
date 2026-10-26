#!/bin/bash
# literal single-line grep of each draft quote against its cited pin
F=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/fetch
chk() { local file="$1" line="$2" q="$3"; if grep -qF -- "$q" "$F/$file"; then echo "FOUND-anywhere $file :: $q"; else echo "MISSING-as-line $file:$line :: $q"; fi; }
chk Hyprland-legacy-ConfigManager.cpp 1345 'parser.parseMode(std::string(ARGS[1])); parser.parsePosition(std::string(ARGS[2])); parser.parseScale(std::string(ARGS[3]));'
chk Hyprland-legacy-ConfigManager.cpp 1345 'parser.parseMode(std::string(ARGS[1]));'
chk hyprutils-String.cpp 59 "if (i == 0 && str.at(i) == '-') {"
chk Hyprland-MonitorRuleManager.cpp 38 'std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });'
chk Hyprland-Monitor.cpp 1001 'float searchScale = std::round(m_scale * 120.0);'
chk Hyprland-MonitorPositionController.cpp 27 'm->moveTo(*POS); arranged.push_back(m); it = toArrange.erase(it);'
chk Hyprland-HyprCtl.cpp 241 '"physicalHeight": {}, "refreshRate": {:.5f},'
chk Hyprland-HyprCtl.cpp 242 '"refreshRate": {:.5f},'
echo '--- line-number truth for each ---'
grep -n 'parser.parseMode(std::string(ARGS\[1\]));' $F/Hyprland-legacy-ConfigManager.cpp
grep -n "if (i == 0 && str.at(i) == '-') {" $F/hyprutils-String.cpp
grep -n 'float    searchScale' $F/Hyprland-Monitor.cpp
grep -n 'm->moveTo(\*POS);' $F/Hyprland-MonitorPositionController.cpp
grep -n '"refreshRate": {:.5f},' $F/Hyprland-HyprCtl.cpp
