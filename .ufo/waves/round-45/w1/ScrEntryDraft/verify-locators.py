#!/usr/bin/env python3
"""Verify every locator in sections.md against the pinned fetch copies with grep -n.

- extracts every `<pin>:<line>` / `<pin>:<a>-<b>` locator from sections.md
- refuses a range wider than 30 lines, or one outside the file
- runs `grep -n -F <token> <pin>` and requires a hit inside the range (locators are computed, never typed)
- negative checks: the JSON dump builder has no rule field and never prints m_activeMonitorRule
- host receipts: line numbers and the advertised 59.99 Hz mode
Exit 0 only if every check passes.
"""
import re
import subprocess
import sys
from pathlib import Path

SEAT = Path(__file__).resolve().parent
FETCH = SEAT.parents[1] / "fetch"
DOC = SEAT / "sections.md"

# (pin, start, end, token that must appear inside [start, end])
SPEC = [
    ("Hyprland-HyprCtl.cpp", 1188, 1190, "isDynamicKeyword = true"),
    ("Hyprland-HyprCtl.cpp", 1200, 1202, 'COMMAND.contains("monitor")'),
    ("Hyprland-HyprCtl.cpp", 123, 134, "pMonitor->m_output->modes"),
    ("Hyprland-HyprCtl.cpp", 230, 259, '"refreshRate": {:.5f}'),
    ("Hyprland-HyprCtl.cpp", 260, 289, '"mirrorOf": "{}"'),
    ("Hyprland-HyprCtl.cpp", 241, 242, '"refreshRate": {:.5f}'),
    ("Hyprland-HyprCtl.cpp", 276, 289, "availableModesForOutput(m, format)"),
    ("Hyprland-HyprCtl.cpp", 277, 277, "escapeJSONStrings(m->m_shortDescription)"),
    ("Hyprland-HyprCtl.cpp", 282, 282, "m->m_scale, sc<int>(m->m_transform)"),
    ("Hyprland-HyprCtl.cpp", 286, 286, 'm->m_mirrorOf ? std::format("{}", m->m_mirrorOf->m_id) : "none"'),
    ("Hyprland-HyprCtl.cpp", 313, 321, 'vars[1] == "all"'),
    ("Hyprland-HyprCtl.cpp", 2037, 2037, 'SHyprCtlCommand{"keyword", false, dispatchKeyword}'),
    ("Hyprland-legacy-ConfigManager.cpp", 606, 606, 'registerHandler(&::handleMonitor, "monitor", {false})'),
    ("Hyprland-legacy-ConfigManager.cpp", 1089, 1090, "m_config->parseDynamic(COMMAND.c_str(), VALUE.c_str())"),
    ("Hyprland-legacy-ConfigManager.cpp", 1295, 1295, "CVarList2(std::string(args))"),
    ("Hyprland-legacy-ConfigManager.cpp", 1299, 1320, 'if (ARGS[1] == "disable"'),
    ("Hyprland-legacy-ConfigManager.cpp", 1321, 1343, "Config::monitorRuleMgr()->add(std::move(parser.rule()));"),
    ("Hyprland-legacy-ConfigManager.cpp", 1384, 1384, "Config::monitorRuleMgr()->add(std::move(parser.rule()));"),
    ("Hyprland-Monitor.cpp", 250, 256, "m_shortDescription = trim(std::format"),
    ("Hyprland-Monitor.cpp", 653, 653, "m_activeMonitorRule = std::move(pMonitorRule);"),
    ("Hyprland-Monitor.cpp", 773, 783, 'requestedStr = "preferred"'),
    ("Hyprland-Monitor.cpp", 784, 794, 'requestedStr = "highrr"'),
    ("Hyprland-Monitor.cpp", 807, 817, 'requestedStr = "maxwidth"'),
    ("Hyprland-Monitor.cpp", 822, 834, "sort by closeness to requested"),
    ("Hyprland-Monitor.cpp", 836, 837, "!DELTALESSTHAN(bestMode->pixelSize.x"),
    ("Hyprland-Monitor.cpp", 836, 839, "!DELTALESSTHAN(bestMode->refreshRate / 1000.f"),
    ("Hyprland-Monitor.cpp", 1011, 1027, "scaleDown"),
    ("Hyprland-Monitor.cpp", 878, 887, "requestedModes | std::views::reverse"),
    ("Hyprland-Monitor.cpp", 942, 957, "TXT_KEY_NOTIF_MONITOR_MODE_FAIL"),
    ("Hyprland-Monitor.cpp", 996, 1010, "searchScale = std::round(m_scale * 120.0);"),
    ("Hyprland-Monitor.cpp", 1201, 1211, 'selector.starts_with("desc:")'),
    ("Hyprland-MonitorRule.hpp", 46, 46, "= 60; // Hz"),
    ("Hyprland-MonitorRuleManager.cpp", 37, 42, "std::erase_if(m_rules"),
    ("Hyprland-MonitorRuleManager.cpp", 44, 46, "PROTO::outputManagement->getOutputStateFor(PMONITOR)"),
    ("Hyprland-MonitorRuleManager.cpp", 56, 75, "OUTPUT_HEAD_COMMITTED_SCALE"),
    ("Hyprland-MonitorRuleManager.cpp", 77, 84, "OUTPUT_HEAD_COMMITTED_ADAPTIVE_SYNC"),
    ("Hyprland-MonitorRuleManager.cpp", 96, 100, "m_rules | std::views::reverse"),
    ("Hyprland-Parser.cpp", 132, 136, 'if (value.contains("@"))'),
    ("Hyprland-Parser.cpp", 145, 149, 'value.starts_with("auto")'),
    ("wiki-Monitors.md", 23, 26, "active and inactive"),
]

LOCATOR_RE = re.compile(r"(Hyprland-[A-Za-z-]+\.(?:cpp|hpp)|wiki-Monitors\.md):(\d+)(?:-(\d+))?")
fails = []


def check(ok, line):
    print(("OK   " if ok else "FAIL ") + line)
    if not ok:
        fails.append(line)


print("# verify-locators — every locator in sections.md resolved by grep -n against .ufo/waves/round-45/fetch/")
print(f"# seat {SEAT}")
print()

# 1. every locator written in sections.md is >= 1 pinned spec entry, and is not wider than 30 lines
doc = DOC.read_text()
seen = set()
for m in LOCATOR_RE.finditer(doc):
    pin, a, b = m.group(1), int(m.group(2)), m.group(3)
    end = int(b) if b else a
    seen.add((pin, a, end))
    width = end - a + 1
    n = len((FETCH / pin).read_text().splitlines())
    check(1 <= a <= end <= n and width <= 30,
          f"L0 {pin}:{a}-{end} width={width} file_lines={n}")

spec_keys = {(p, a, b) for p, a, b, _ in SPEC}
check(seen <= spec_keys, f"L1 no unverified locator in sections.md (unverified: {sorted(seen - spec_keys)})")
check(spec_keys <= seen, f"L2 every spec locator is used in sections.md (unused: {sorted(spec_keys - seen)})")
print()

# 2. grep -n each token and require a hit inside the range
for pin, a, b, token in SPEC:
    path = FETCH / pin
    r = subprocess.run(["grep", "-n", "-F", token, str(path)], capture_output=True, text=True)
    hits = []
    for row in r.stdout.splitlines():
        ln = int(row.split(":", 1)[0])
        if a <= ln <= b:
            hits.append(row)
    check(bool(hits), f"L3 {pin}:{a}-{b} token={token!r}" + (f" -> {hits[0][:120]}" if hits else " -> NO HIT"))
print()

# 3. negative checks
blk = "\n".join((FETCH / "Hyprland-HyprCtl.cpp").read_text().splitlines()[229:289])
check("rule" not in blk.lower(), "N1 JSON builder 230-289 has no rule/selector field")
r = subprocess.run(["grep", "-n", "-F", "m_activeMonitorRule", str(FETCH / "Hyprland-HyprCtl.cpp")],
                   capture_output=True, text=True)
check(r.returncode == 1 and r.stdout == "", "N2 HyprCtl.cpp never names m_activeMonitorRule")
print()

# 4. host receipts
conf = (SEAT / "monitors-conf-lines.txt").read_text().splitlines()
def conf_line(n, must):
    row = conf[n - 1]
    check(row.startswith(f"{n}:") and must in row, f"H1 monitors.conf:{n} carries {must!r} -> {row[:90]}")
for n in (7, 14, 19, 22):
    conf_line(n, "preferred")
conf_line(10, "monitor = DP-1, 3440x1440@100, 0x0, 1")
conf_line(25, "@60")
conf_line(26, "@120")
modes = (SEAT / "live-modes-host.txt").read_text()
check("3440x1440@59.99Hz" in modes, "H2 DP-1 advertises 3440x1440@59.99Hz (live-modes-host.txt)")
mode_list = [l.split("|", 1)[1].strip() for l in modes.splitlines() if l.startswith("MADO_MODES:")][0]
check(len(mode_list.split(",")) == 11, f"H2b DP-1 advertises eleven modes (got {len(mode_list.split(chr(44)))})")
data = "\n".join(l for l in modes.splitlines() if l.startswith("MADO_MODES:"))
check('"serial"' not in data and "description" not in data, "H3 live-modes-host.txt is projected (data line has no serial/description)")
print()

print(f"# FAILS={len(fails)}")
if fails:
    for f in fails:
        print("# " + f)
    sys.exit(1)
sys.exit(0)
