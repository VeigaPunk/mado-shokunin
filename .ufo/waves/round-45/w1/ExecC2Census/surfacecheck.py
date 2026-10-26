#!/usr/bin/env python3
"""ExecC2Census: independent re-derivation of the 17 SURFACES (anchor line + entry
locator <= 30 lines on a keyword line), plus the clause-h census tokens."""
import re
import sys

L1 = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft"
F = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/fetch/"

# (receipt, anchor, keyword, label)  -- transcribed from the counter's SURFACES,
# verified below by an exact occurrence count of 1 in the pinned bytes
SURFACES = [
    ("Hyprland-Parser.cpp", "bool CMonitorRuleParser::parseMode(const std::string& value) {", r"mode|resolution", "parse-mode"),
    ("Hyprland-Parser.cpp", "bool CMonitorRuleParser::parsePosition(const std::string& value, bool isFirst) {", r"position|auto", "parse-position"),
    ("Hyprland-Parser.cpp", "bool CMonitorRuleParser::parseScale(const std::string& value) {", r"scale", "parse-scale"),
    ("Hyprland-legacy-ConfigManager.cpp", "std::optional<std::string> CConfigManager::handleMonitor(const std::string& command, const std::string& args) {", r"handleMonitor|monitor line", "handle-monitor"),
    ("Hyprland-legacy-ConfigManager.cpp", 'return "invalid syntax at \\"" + std::string(ARGS[argno]) + "\\"";', r"invalid syntax|unknown key|dropped", "invalid-syntax"),
    ("Hyprland-MonitorRuleManager.cpp", "std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });", r"erase|same selector", "add-erase"),
    ("Hyprland-MonitorRuleManager.cpp", "for (auto const& r : m_rules | std::views::reverse) {", r"last|reverse", "get-reverse"),
    ("Hyprland-MonitorRule.hpp", "m_refreshRate   = 60; // Hz", r"\b60\b", "default-60"),
    ("Hyprland-Monitor.cpp", "bool CMonitor::matchesStaticSelector(std::string_view selector) const {", r"desc:|selector", "selector"),
    ("Hyprland-Monitor.cpp", "!DELTALESSTHAN(bestMode->refreshRate / 1000.f, RULE->m_refreshRate, 1))", r"refresh|Hz", "closeness"),
    ("Hyprland-Monitor.cpp", "float    searchScale = std::round(m_scale * 120.0);", r"120|scale", "scale-search"),
    ("Hyprland-HyprCtl.cpp", '"refreshRate": {:.5f},', r"refreshRate", "json-refresh"),
    ("Hyprland-HyprCtl.cpp", 'if (vars.size() == 2 && vars[1] == "all")', r"\ball\b", "monitors-all"),
    ("Hyprland-MonitorPositionController.cpp", "m->moveTo(*POS);", r"explicit|position", "explicit-position"),
    ("hyprutils-String.cpp", "bool Hyprutils::String::isNumber2(const std::string_view& str, bool allowfloat) {", r"isNumber|number", "is-number"),
    ("wiki-Monitors.md", "monitor = name, resolution, position, scale", r"wiki|document", "wiki-format"),
    ("wiki-Monitors.md", "The default transfer function assumed to be in use on an SDR display", r"sdr_eotf", "wiki-sdr-eotf"),
]
JWIDTH = 30

text = open(L1 + "/entry.md").read()
raw_lines = text.splitlines()
body, fenced = [], False
for k, l in enumerate(raw_lines):
    if re.match(r"^\s{0,3}(```|~~~)", l):
        fenced = not fenced
        continue
    if not fenced and k >= 20:
        body.append((k + 1, l))

bad = 0
print("label               receipt                               anchor@  cited  entry line:locator (width)")
for rname, anchor, kw, label in SURFACES:
    rl = open(F + rname, encoding="utf-8").read().split("\n")
    hits = [n for n, l in enumerate(rl, 1) if anchor in l]
    if len(hits) != 1:
        print("%-19s %-35s anchor_count=%d" % (label, rname, len(hits)))
        bad += 1
        continue
    L = hits[0]
    pat = re.compile(r"(?<![\w.-])%s:(\d+)(?:-(\d+))?(?!\d)" % re.escape(rname))
    found = []
    for no, l in body:
        if not re.search(kw, l, re.I):
            continue
        for a, b in pat.findall(l):
            a, b = int(a), int(b or a)
            if a <= L <= b and b - a <= JWIDTH:
                found.append((no, a, b))
    ok = bool(found)
    bad += 0 if ok else 1
    print("%-19s %-35s %-7d %-6s %s" % (
        label, rname, L, ok,
        ", ".join("L%d:%d-%d(w=%d)" % (no, a, b, b - a) for no, a, b in found) or "NOT CITED"))

print("uncovered=%d/17" % bad)

# clause h: exactly one entry line carries the census line; no other line carries
# one of the six name= tokens with a different value
CENSUS = ("hyprland monitor-rule default_refresh=60 refresh_tolerance=1 scale_step=1/120 "
          "scale_search=89 json_refresh_decimals=5 line_keys=8")
six = ("default_refresh", "refresh_tolerance", "scale_step", "scale_search",
       "json_refresh_decimals", "line_keys")
exact = [n for n, l in body if l == CENSUS]
print("\ncensus exact lines:", [n for n, _ in [(k + 1, l) for k, l in enumerate(raw_lines) if l == CENSUS]])
for key in six:
    rows = [(k + 1, l) for k, l in enumerate(raw_lines)
            if re.search(r"\b%s=" % key, l)]
    vals = {re.search(r"\b%s=(\S+?)(?=[\s,;]|$)" % key, l).group(1) if re.search(r"\b%s=(\S+?)(?=[\s,;]|$)" % key, l) else "?" for _, l in rows}
    print("%-22s lines=%s values=%s" % (key, [n for n, _ in rows], sorted(vals)))
sys.exit(1 if bad else 0)
