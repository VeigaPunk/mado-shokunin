#!/usr/bin/env python3
"""ScrReadme locator + row-shape check (round 45, seat ScrReadme).

Read-only. Re-reads the pinned bytes this seat's draft cites and asserts that every cited line carries the token the
draft says it carries; then checks the two drafted blocks for the shape the frozen C2 predicate and the README's
neighbours require. Line numbers were obtained by grep -n on the pins (see locators.txt), never typed from memory.
"""
import os
import re
import sys

W = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45"
FETCH = os.path.join(W, "fetch")
SEAT = os.path.join(W, "w1", "ScrReadme")

CASES = [
    ("Hyprland-legacy-ConfigManager.cpp", 1345, "parser.parseMode(std::string(ARGS[1]));"),
    ("Hyprland-legacy-ConfigManager.cpp", 1346, "parser.parsePosition(std::string(ARGS[2]));"),
    ("Hyprland-legacy-ConfigManager.cpp", 1347, "parser.parseScale(std::string(ARGS[3]));"),
    ("Hyprland-legacy-ConfigManager.cpp", 1352, 'if (ARGS[argno] == "mirror") {'),
    ("Hyprland-legacy-ConfigManager.cpp", 1355, '} else if (ARGS[argno] == "bitdepth") {'),
    ("Hyprland-legacy-ConfigManager.cpp", 1358, '} else if (ARGS[argno] == "cm") {'),
    ("Hyprland-legacy-ConfigManager.cpp", 1361, '} else if (ARGS[argno] == "sdrsaturation") {'),
    ("Hyprland-legacy-ConfigManager.cpp", 1364, '} else if (ARGS[argno] == "sdrbrightness") {'),
    ("Hyprland-legacy-ConfigManager.cpp", 1367, '} else if (ARGS[argno] == "transform") {'),
    ("Hyprland-legacy-ConfigManager.cpp", 1370, '} else if (ARGS[argno] == "vrr") {'),
    ("Hyprland-legacy-ConfigManager.cpp", 1373, '} else if (ARGS[argno] == "icc") {'),
    ("Hyprland-legacy-ConfigManager.cpp", 1378, 'return "invalid syntax at'),
    ("Hyprland-legacy-ConfigManager.cpp", 576, 'addSpecialConfigValue("monitorv2", "sdr_eotf"'),
    ("Hyprland-legacy-ConfigManager.cpp", 819, 'getSpecialConfigValuePtr("monitorv2", "sdr_eotf"'),
    ("Hyprland-legacy-ConfigManager.cpp", 831, "    }"),
    ("Hyprland-MonitorRule.hpp", 46, "m_refreshRate   = 60;"),
    ("Hyprland-MonitorRuleManager.cpp", 38, "std::erase_if(m_rules"),
    ("Hyprland-MonitorRuleManager.cpp", 45, "applyWlrOutputConfig"),
    ("Hyprland-MonitorRuleManager.cpp", 84, "    };"),
    ("Hyprland-MonitorRuleManager.cpp", 96, "std::views::reverse"),
    ("Hyprland-MonitorRuleManager.cpp", 103, "for (auto const& r : m_rules)"),
    ("Hyprland-Monitor.cpp", 836, "DELTALESSTHAN(bestMode->pixelSize.x"),
    ("Hyprland-Monitor.cpp", 837, "DELTALESSTHAN(bestMode->refreshRate / 1000.f"),
    ("Hyprland-Monitor.cpp", 1001, "std::round(m_scale * 120.0)"),
    ("Hyprland-Monitor.cpp", 1201, "CMonitor::matchesStaticSelector"),
    ("Hyprland-Monitor.cpp", 1202, 'selector.starts_with("desc:")'),
    ("Hyprland-Monitor.cpp", 1211, "}"),
    ("Hyprland-Monitor.cpp", 255, "m_shortDescription = trim"),
    ("Hyprland-MonitorPositionController.cpp", 27, "m->moveTo(*POS);"),
    ("Hyprland-HyprCtl.cpp", 242, '"refreshRate": {:.5f},'),
    ("Hyprland-HyprCtl.cpp", 277, "m->m_shortDescription"),
    ("Hyprland-HyprCtl.cpp", 320, 'vars[1] == "all"'),
    ("hyprutils-String.cpp", 59, "if (i == 0 && str.at(i) == '-') {"),
    ("wiki-Monitors.md", 253, "sdr_eotf"),
]

ROW_PREFIX = "| `knowledge/hyprland-monitor-rule-r45.md`"


def main():
    bad = 0
    for name, lineno, needle in CASES:
        lines = open(os.path.join(FETCH, name), encoding="utf-8", errors="replace").read().split("\n")
        got = lines[lineno - 1] if lineno - 1 < len(lines) else "<EOF>"
        ok = needle in got
        bad += not ok
        print("%s %s:%d %r" % ("PASS" if ok else "FAIL", name, lineno, needle))

    readme = open(os.path.join(SEAT, "readme.md"), encoding="utf-8").read().split("\n")
    rows = [l for l in readme if l.startswith(ROW_PREFIX)]
    print("%s row occurrences in seat draft = %d" % ("PASS" if len(rows) == 1 else "FAIL", len(rows)))
    bad += len(rows) != 1
    row = rows[0]
    cells = row.split("|")
    shape = (cells[0] == "" and cells[-1] == "" and len(cells) == 5)
    print("%s row is one line with 3 cells (split=%d)" % ("PASS" if shape else "FAIL", len(cells) - 2))
    bad += not shape
    inner = cells[2]
    no_pipe = "|" not in inner
    print("%s holds cell carries no inner pipe" % ("PASS" if no_pipe else "FAIL"))
    bad += not no_pipe
    src = cells[3].strip()
    print("%s source cell = %r (entry cites S302-S310)" % ("PASS" if src == "S302-S310" else "FAIL", src))
    bad += src != "S302-S310"
    print("%s clause-f prefix matches: %r" % (
        "PASS" if re.match(r"^\| `knowledge/hyprland-monitor-rule-r45\.md`", row) else "FAIL", row[:60]))
    bad += re.match(r"^\| `knowledge/hyprland-monitor-rule-r45\.md`", row) is None

    sec = readme.count("### Round-45 monitor-rule route")
    print("%s frontier subsection occurrences = %d" % ("PASS" if sec == 1 else "FAIL", sec))
    bad += sec != 1
    tail_ok = rows[0] and "Nothing was applied" in "\n".join(readme)
    print("%s frontier keeps the unexercised-cases sentence" % ("PASS" if tail_ok else "FAIL"))
    bad += not tail_ok
    leaked = [w for w in ("serial", "Serial") if w in row]
    print("%s row names no serial field (%s)" % ("PASS" if not leaked else "FAIL", leaked or "-"))
    bad += bool(leaked)

    print("SUMMARY failures=%d" % bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
