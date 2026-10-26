#!/bin/sh
# ScrLessonGate: locate each Gate quote's start line in the frozen pins with grep -n.
# Whitespace-flexible where the upstream file aligns declarations or splits the
# statement; the START line is what the lesson cites. Read-only.
F=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/fetch
set -x
grep -nF "m_rule.m_refreshRate = stof(value.substr(value.find_first_of('@') + 1));" "$F/Hyprland-Parser.cpp"
grep -nF "parser.parseMode(std::string(ARGS[1]));" "$F/Hyprland-legacy-ConfigManager.cpp"
grep -nF "std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });" "$F/Hyprland-MonitorRuleManager.cpp"
grep -nE "float[[:space:]]+m_refreshRate[[:space:]]+= 60;" "$F/Hyprland-MonitorRule.hpp"
grep -nE "float[[:space:]]+searchScale = std::round\(m_scale \* 120\.0\);" "$F/Hyprland-Monitor.cpp"
grep -nF '"refreshRate": {:.5f},' "$F/Hyprland-HyprCtl.cpp"
grep -nF "m->moveTo(*POS);" "$F/Hyprland-MonitorPositionController.cpp"
grep -nF "if (i == 0 && str.at(i) == '-') {" "$F/hyprutils-String.cpp"
grep -nF "monitor = name, resolution, position, scale" "$F/wiki-Monitors.md"
