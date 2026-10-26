#!/usr/bin/env python3
"""Round-45 w2 falsification, seat CritW2Entry: locate every quote the landed
entry corpus/knowledge/hyprland-monitor-rule-r45.md lifts, by grep, and print the
computed line next to the line the entry cites.  Locators are computed here, never typed.
Read-only over .ufo/waves/round-45/fetch/ (pins) and the entry at 4d22eeb.
"""
import json, re, subprocess, sys, pathlib

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
FETCH = LANE / ".ufo/waves/round-45/fetch"
REV = "4d22eeb66c2835af8aaa3fac6ad838fa616aa663"
ENTRY = "corpus/knowledge/hyprland-monitor-rule-r45.md"

def pin(name):
    return (FETCH / name).read_text(errors="replace").splitlines()

def find(pinname, needle, want_line=None, nth=0):
    """Return list of 1-based lines containing needle."""
    ls = pin(pinname)
    hits = [i + 1 for i, l in enumerate(ls) if needle in l]
    return hits

CHECKS = [
 # id, pin, needle, lines the entry cites (entry line:locator), what it is
 ("L38a", "hyprutils-VarList2.hpp", "const char delim = ','", 18),
 ("L38b", "Hyprland-legacy-ConfigManager.cpp", "CConfigManager::handleMonitor(const std::string& command", 1293),
 ("L40a", "Hyprland-legacy-ConfigManager.cpp", 'if (ARGS[1] == "disable" || ARGS[1] == "disabled" || ARGS[1] == "addreserved" || ARGS[1] == "transform")', 1299),
 ("L40b", "Hyprland-legacy-ConfigManager.cpp", '} else if (ARGS[1] == "addreserved") {', 1319),
 ("L42a", "Hyprland-legacy-ConfigManager.cpp", "while (!ARGS[argno].empty()) {", 1351),
 ("L42b", "Hyprland-legacy-ConfigManager.cpp", 'Config::monitorRuleMgr()->add(std::move(parser.rule()));', 1384),
 ("L42c", "Hyprland-legacy-ConfigManager.cpp", "return parser.getError();", 1386),
 ("L44a", "Hyprland-Parser.cpp", "bool CMonitorRuleParser::parseMode(const std::string& value)", 110),
 ("L44b", "Hyprland-Parser.cpp", "static bool parseModeLine(const std::string& modeline", 14),
 ("L44c", "Hyprland-Parser.cpp", "else if (parseModeLine(value, m_rule.m_drmMode))", 119),
 ("L44d", "Hyprland-Monitor.cpp", "if (RULE->m_resolution == Vector2D()) {", 773),
 ("L46",  "Hyprland-Parser.cpp", "m_rule.m_refreshRate = stof(value.substr(value.find_first_of('@') + 1));", 134),
 ("L48",  "Hyprland-MonitorRule.hpp", "m_refreshRate   = 60;", 46),
 ("L50a", "Hyprland-Parser.cpp", "bool CMonitorRuleParser::parsePosition(const std::string& value, bool isFirst)", 145),
 ("L50b", "Hyprland-Parser.cpp", "m_rule.m_offset.y = stoi(", 182),
 ("L52",  "Hyprland-Parser.cpp", "if (m_rule.m_scale < 0.25F)", 203),
 ("L54a", "hyprutils-String.cpp", "if (i == 0 && str.at(i) == '-') {", 59),
 ("L54b", "hyprutils-String.cpp", "bool Hyprutils::String::isNumber2(const std::string_view& str", 50),
 ("L54c", "hyprutils-String.cpp", "return isdigit(str.back()) != 0;", 83),
 ("L54d", "Hyprland-Parser.cpp", "const auto TSF = std::stoi(value);", 219),
 ("L58a", "Hyprland-MonitorRuleManager.cpp", "std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });", 38),
 ("L58b", "Hyprland-MonitorRuleManager.cpp", "void CMonitorRuleManager::add(CMonitorRule&& x) {", 37),
 ("L60a", "Hyprland-MonitorRuleManager.cpp", "for (auto const& r : m_rules | std::views::reverse) {", 96),
 ("L60b", "Hyprland-MonitorRuleManager.cpp", "if (r.m_name.empty())", 104),
 ("L60c", "Hyprland-MonitorRuleManager.cpp", "CMonitorRule fallbackRule;", None),  # 87 and 110
 ("L60d", "Hyprland-MonitorRuleManager.cpp", "if (PMONITOR->m_isUnsafeFallback) {", 86),
 ("L60e", "Hyprland-MonitorRuleManager.cpp", "auto applyWlrOutputConfig = [PMONITOR](CMonitorRule rule) -> CMonitorRule {", 45),
 ("L62a", "Hyprland-Monitor.cpp", "bool CMonitor::matchesStaticSelector(std::string_view selector) const {", 1201),
 ("L62b", "Hyprland-Monitor.cpp", "m_description = m_output->description;", 250),
 ("L62c", "Hyprland-Monitor.cpp", "std::erase(m_description, ',');", 252),
 ("L62d", "Hyprland-Monitor.cpp", 'm_shortDescription = trim(std::format("{} {} {}", m_output->make, m_output->model, m_output->serial));', 255),
 ("L62e", "Hyprland-HyprCtl.cpp", '"description": "{}",', 234),
 ("L62f", "Hyprland-HyprCtl.cpp", "escapeJSONStrings(m->m_shortDescription)", 277),
 ("L64a", "aquamarine-DRM.cpp", 'output->description = std::format("{} {} {} ({})", make, model, serial, szName);', 2101),
 ("L68a", "Hyprland-Monitor.cpp", "} else if (RULE->m_resolution != Vector2D()) {", 818),
 ("L68b", "Hyprland-Monitor.cpp", "requestedModes.push_back(", None),  # 838 + 847
 ("L68c", "Hyprland-Monitor.cpp", "for (auto const& mode : requestedModes | std::views::reverse) {", 878),
 ("L70a", "Hyprland-macros.hpp", "#define DELTALESSTHAN(a, b, delta) (abs((a) - (b)) < (delta))", 40),
 ("L70b", "Hyprland-Monitor.cpp", "!DELTALESSTHAN(bestMode->pixelSize.x, RULE->m_resolution.x, 1)", 836),
 ("L70c", "Hyprland-Monitor.cpp", "m_refreshRate = mode->refreshRate / 1000.f;", 903),
 ("L72a", "hyprutils-Vector2D.hpp", "constexpr Vector2D operator/(const double& a) const {", 39),
 ("L72b", "Hyprland-Monitor.cpp", "Vector2D logicalSize = m_pixelSize / m_scale;", 996),
 ("L72c", "Hyprland-Monitor.cpp", "if (!*PDISABLESCALECHECKS &&", 997),
 ("L72d", "Hyprland-Monitor.cpp", 'CConfigValue<Config::INTEGER>("debug:disable_scale_checks")', 721),
 ("L74a", "Hyprland-Monitor.cpp", "float    searchScale = std::round(m_scale * 120.0);", 1001),
 ("L74b", "Hyprland-Monitor.cpp", "for (size_t i = 1; i < 90; ++i) {", 1010),
 ("L74c", "Hyprland-Monitor.cpp", "if (!found) {", 1029),
 ("L74d", "Hyprland-Monitor.cpp", 'CConfigValue<Config::INTEGER>("misc:disable_scale_notification")', 1040),
 ("L76a", "Hyprland-MonitorPositionController.cpp", "m->moveTo(*POS);", 27),
 ("L76b", "Hyprland-MonitorPositionController.cpp", "it = toArrange.erase(it);", 29),
 ("L76c", "Hyprland-MonitorPositionController.cpp", "for (auto const& m : toArrange) {", 61),
 ("L80a", "Hyprland-HyprCtl.cpp", '"physicalHeight": {},', 241),
 ("L80b", "Hyprland-HyprCtl.cpp", '"refreshRate": {:.5f},', 242),
 ("L80c", "Hyprland-HyprCtl.cpp", '(m->m_enabled ? "false" : "true")', 285),
 ("L80d", "Hyprland-HyprCtl.cpp", 'm->m_mirrorOf ? std::format("{}", m->m_mirrorOf->m_id) : "none"', 286),
 ("L82",  "Hyprland-HyprCtl.cpp", 'if (vars.size() == 2 && vars[1] == "all")', 320),
 ("L82b", "Hyprland-HyprCtl.cpp", "allMonitors ? State::monitorState()->allMonitors()", 327),
 ("L84a", "Hyprland-MonitorState.cpp", "m_realMonitors.emplace_back(mon);", 114),
 ("L84b", "Hyprland-MonitorState.cpp", "m_listeners.monitorAdded   = Event::bus()->m_events.monitor.added.listen", 25),
 ("L84c", "Hyprland-MonitorState.cpp", "m_listeners.layoutChanged = Event::bus()->m_events.monitor.layoutChanged.listen", 32),
 ("L84d", "Hyprland-Monitor.cpp", "if (m_enabled && !monitorRule.m_disabled) {", 264),
 ("L84e", "Hyprland-Monitor.cpp", "Event::bus()->m_events.monitor.added.emit(m_self.lock());", 389),
 # the defect probe: the early-return that sits between the two cited lines
 ("L84f", "Hyprland-Monitor.cpp", "        return;", None),
 ("L84g", "Hyprland-Monitor.cpp", "if (monitorRule.m_disabled) {", 275),
 ("L84h", "Hyprland-Monitor.cpp", "m_enabled = false;", 283),
 ("L90",  "wiki-Monitors.md", "monitor = name, resolution, position, scale", 11),
 ("L92a", "wiki-Monitors.md", ", sdr_eotf, X", 253),
 ("L92b", "Hyprland-legacy-ConfigManager.cpp", '"monitorv2", "sdr_eotf"', 819),
 ("L92c", "wiki-Monitors.md", "| sdr_eotf |", 319),
 ("L105", "Hyprland-legacy-ConfigManager.cpp", "const auto ERR = m_config->parse();", 743),
 ("L105b","Hyprland-legacy-ConfigManager.cpp", "const auto monitorError               = handleMonitorv2();", 747),
]

def main():
    out = []
    ok = 0
    miss = 0
    for cid, pinname, needle, cited in CHECKS:
        hits = find(pinname, needle)
        cited_s = "n/a" if cited is None else str(cited)
        if not hits:
            out.append(f"{cid}\t{pinname}\tNOT_FOUND\tcited={cited_s}\t{needle[:60]}")
            miss += 1
            continue
        ok += 1
        within = "" if cited is None else ("MATCH" if cited in hits else "MISMATCH")
        out.append(f"{cid}\t{pinname}\tlines={hits}\tcited={cited_s}\t{within}\t{needle[:60]}")
    print("\n".join(out))

    # census recomputation, each value with its computed locator
    print("\n-- census recompute (entry line 86) --")
    rule = pin("Hyprland-MonitorRule.hpp")
    print("default_refresh=60 ->", [i+1 for i,l in enumerate(rule) if "m_refreshRate" in l and "60" in l])
    mon = pin("Hyprland-Monitor.cpp")
    print("refresh_tolerance=1 ->", [i+1 for i,l in enumerate(mon) if "DELTALESSTHAN(bestMode->pixelSize.x" in l])
    print("scale_step=1/120 ->", [i+1 for i,l in enumerate(mon) if "120.0" in l][:6])
    print("scale_search=89 -> 'i < 90' at", [i+1 for i,l in enumerate(mon) if "i < 90" in l])
    ctl = pin("Hyprland-HyprCtl.cpp")
    print("json_refresh_decimals=5 ->", [i+1 for i,l in enumerate(ctl) if "{:.5f}" in l])
    cm = pin("Hyprland-legacy-ConfigManager.cpp")
    keys = [l for l in cm[1290:1390] if "} else if (ARGS[argno] ==" in l]
    first = [l for l in cm[1290:1390] if 'if (ARGS[argno] == "mirror")' in l]
    print(f"line_keys -> first={len(first)} else_if={len(keys)} total={len(first)+len(keys)}")
    for l in first + keys:
        print("   ", l.strip()[:60])

    # the defect probe: what lies between 264 and 389 in onConnect
    print("\n-- onConnect 262-290 (brace shape of the cited pair 264 & 389) --")
    for i in range(261, 291):
        print(f"{i+1:4d}: {mon[i]}")

    print(f"\nSUMMARY found={ok} not_found={miss} checks={len(CHECKS)}")

if __name__ == "__main__":
    main()
