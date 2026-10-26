# round 45 (positive control draft)

## Gate

GATE S302 receipt=.ufo/waves/round-45/fetch/Hyprland-Parser.cpp sha256=616468fd0576d8b201ef00cd69289234f0ffb1c3137ae2a0ac954fabe37dd589 quote="m_rule.m_refreshRate = stof(value.substr(value.find_first_of('@') + 1));"
GATE S303 receipt=.ufo/waves/round-45/fetch/Hyprland-legacy-ConfigManager.cpp sha256=9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b quote="parser.parseMode(std::string(ARGS[1])); parser.parsePosition(std::string(ARGS[2])); parser.parseScale(std::string(ARGS[3]));"
GATE S304 receipt=.ufo/waves/round-45/fetch/Hyprland-MonitorRuleManager.cpp sha256=17d46685c2623657f52e71b22a033c0a798cf3903f7bbeb64ceebce87527f016 quote="std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });"
GATE S305 receipt=.ufo/waves/round-45/fetch/Hyprland-MonitorRule.hpp sha256=b01d31a16d5fb413ead28f46825381f36a70c29b86eceb58cd633dcbf031a2f5 quote="float m_refreshRate = 60;"
GATE S306 receipt=.ufo/waves/round-45/fetch/Hyprland-Monitor.cpp sha256=9cf88e154eb5dae676c79d37b5b055ca6134838857cecdbb89a3b747a6821927 quote="float searchScale = std::round(m_scale * 120.0);"
GATE S307 receipt=.ufo/waves/round-45/fetch/Hyprland-HyprCtl.cpp sha256=798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa quote=""physicalHeight": {}, "refreshRate": {:.5f},"
GATE S308 receipt=.ufo/waves/round-45/fetch/Hyprland-MonitorPositionController.cpp sha256=3b705388fa53aef77c5e8c6f6307c94dab08b5dae9460bab427d648359b5ae49 quote="m->moveTo(*POS); arranged.push_back(m); it = toArrange.erase(it);"
GATE S309 receipt=.ufo/waves/round-45/fetch/hyprutils-String.cpp sha256=a92c131a45f41918388eece78f225dbeab7791bb3cd2d3761d840aefa1527bac quote="if (i == 0 && str.at(i) == '-') {"
GATE S310 receipt=.ufo/waves/round-45/fetch/wiki-Monitors.md sha256=f2ac7025b7d7dd13b467ad52a5ca7b4da39e198f3ae4c6a675f92a38cd0304b9 quote="monitor = name, resolution, position, scale"
