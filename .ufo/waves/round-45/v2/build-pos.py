#!/usr/bin/env python3
"""Apply the v2 draft (entry, rows S302-S315, lesson Gate, README row) to a lane checkout at DIR (positive control
for PRED-C2-r45-v2; never run against the lane itself)."""
import hashlib
import os
import re
import sys

D = sys.argv[1]
L1 = os.environ.get("L1DRAFT", "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/v2")
F = ".ufo/waves/round-45/fetch/"
ENTRY = "corpus/knowledge/hyprland-monitor-rule-r45.md"
C = "efb50993780079460b0cbed1363e2166a2de1d9f"
HY = "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/" % C


def sha(p):
    return hashlib.sha256(open(os.path.join(D, F + p), "rb").read()).hexdigest()


def size(p):
    return os.path.getsize(os.path.join(D, F + p))


def anchor(rname, ranges, rev):
    return "%s (receipt %s) @ %s, %d B sha256:%s; receipt %s%s" % (
        ranges, rname, rev, size(rname), sha(rname), F, rname)


ROWS = [
    ("S302", "Hyprland v0.56.2 monitor rule parser - " + HY + "config/shared/monitor/Parser.cpp", "code", "A",
     "How a monitor line's mode, position, scale and transform fields are parsed (host Hyprland 0.56.2)",
     anchor("Hyprland-Parser.cpp", "Hyprland-Parser.cpp:110-143 parseMode, Hyprland-Parser.cpp:145-191 parsePosition, Hyprland-Parser.cpp:193-227 parseScale and parseTransform", "commit " + C),
     "A rate is read only after @, positions and scales starting auto stay unset, and a scale below 0.25 becomes 1"),
    ("S303", "Hyprland v0.56.2 legacy config manager - the monitor keyword handler - " + HY + "config/legacy/ConfigManager.cpp", "code", "A",
     "The monitor line grammar of the hyprlang-era config: modifiers, positional fields and the key loop",
     anchor("Hyprland-legacy-ConfigManager.cpp", "Hyprland-legacy-ConfigManager.cpp:1293-1387 handleMonitor, Hyprland-legacy-ConfigManager.cpp:788-880 handleMonitorv2", "commit " + C),
     "Eight keys follow the scale; any other key rejects the whole line before the rule is added"),
    ("S304", "Hyprland v0.56.2 monitor rule manager - " + HY + "config/shared/monitor/MonitorRuleManager.cpp", "code", "A",
     "Which stored monitor rule an output receives",
     anchor("Hyprland-MonitorRuleManager.cpp", "Hyprland-MonitorRuleManager.cpp:37-42 add, Hyprland-MonitorRuleManager.cpp:44-117 get", "commit " + C),
     "One rule per selector string; the newest matching rule wins, else the first empty-selector rule, else a built-in default"),
    ("S305", "Hyprland v0.56.2 monitor rule fields - " + HY + "config/shared/monitor/MonitorRule.hpp", "code", "A",
     "Default values of a parsed monitor rule",
     anchor("Hyprland-MonitorRule.hpp", "Hyprland-MonitorRule.hpp:41-69 class CMonitorRule fields", "commit " + C),
     "A rule without an explicit rate carries 60 Hz; scale -1 means auto; the offset sentinel means auto position"),
    ("S306", "Hyprland v0.56.2 output - applying a monitor rule - " + HY + "output/Monitor.cpp", "code", "A",
     "How a rule's mode and scale become the running mode and scale, and how selectors match",
     anchor("Hyprland-Monitor.cpp", "Hyprland-Monitor.cpp:719-1082 applyMonitorRule, Hyprland-Monitor.cpp:1201-1211 matchesStaticSelector, Hyprland-Monitor.cpp:250-256 descriptions", "commit " + C),
     "The closest available mode is chosen within 1 px and 1 Hz, and a scale leaving fractional pixels is corrected to a 1/120 step"),
    ("S307", "Hyprland v0.56.2 hyprctl - the monitors request - " + HY + "debug/HyprCtl.cpp", "code", "A",
     "The monitors request and the JSON fields it prints for each output",
     anchor("Hyprland-HyprCtl.cpp", "Hyprland-HyprCtl.cpp:224-288 getMonitorData JSON, Hyprland-HyprCtl.cpp:313-345 monitorsRequest", "commit " + C),
     "monitors all lists disabled outputs too; refreshRate has five decimals and description is the short make-model-serial form"),
    ("S308", "Hyprland v0.56.2 monitor arrangement - " + HY + "state/MonitorPositionController.cpp", "code", "A",
     "Where explicit and auto monitor positions are placed",
     anchor("Hyprland-MonitorPositionController.cpp", "Hyprland-MonitorPositionController.cpp:16-38 explicit positions, Hyprland-MonitorPositionController.cpp:61-101 auto directions", "commit " + C),
     "An explicit offset is placed exactly as written before any auto placement"),
    ("S309", "hyprutils v0.14.2 string helpers - https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/string/String.cpp", "code", "A",
     "The number test Hyprland's scale and transform parsers call (host hyprutils 0.14.2-1)",
     anchor("hyprutils-String.cpp", "hyprutils-String.cpp:46-84 isNumber and isNumber2", "tag v0.14.2"),
     "A leading minus and one inner dot are allowed; the last character must be a digit"),
    ("S310", "Hyprland wiki Monitors page (hyprlang era) - https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605e453c0ad533d979fccbefff788ef/content/Configuring/Monitors.md", "docs", "A",
     "The documented monitor line format and options for the hyprlang config",
     anchor("wiki-Monitors.md", "wiki-Monitors.md:5-30 General, wiki-Monitors.md:240-260 colour keys, wiki-Monitors.md:290-310 Monitor v2", "commit ecc06f3b6605e453c0ad533d979fccbefff788ef (2026-04-20)"),
     "Documents name, resolution, position, scale plus option keys, including an sdr_eotf key the 0.56.2 line handler does not accept"),
    ("S311", "Hyprland v0.56.2 monitor state tracker - " + HY + "state/MonitorState.cpp", "code", "A",
     "Which outputs the full and the active monitor lists hold",
     anchor("Hyprland-MonitorState.cpp", "Hyprland-MonitorState.cpp:24-46 active list, Hyprland-MonitorState.cpp:49-55 allMonitors and monitors, Hyprland-MonitorState.cpp:109-125 add", "commit " + C),
     "Every real output joins the full list before the enabled check; the active list holds enabled outputs that mirror nothing"),
    ("S312", "Hyprland v0.56.2 macros header - " + HY + "macros.hpp", "code", "A",
     "The DELTALESSTHAN comparison used by the mode closeness test",
     anchor("Hyprland-macros.hpp", "Hyprland-macros.hpp:40 DELTALESSTHAN", "commit " + C),
     "The closeness test is a strict less-than on the absolute difference"),
    ("S313", "hyprutils v0.14.2 vector type - https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/math/Vector2D.hpp", "code", "A",
     "The arithmetic precision of Hyprland's logical-size division",
     anchor("hyprutils-Vector2D.hpp", "hyprutils-Vector2D.hpp:12-22 fields, hyprutils-Vector2D.hpp:36-41 scalar operators", "tag v0.14.2"),
     "Vector2D holds doubles and divides by a double, so the scale-integrality test runs in double precision"),
    ("S314", "hyprutils v0.14.2 CVarList2 splitter - https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/string/VarList2.hpp", "code", "A",
     "How a monitor line's value is split into fields",
     anchor("hyprutils-VarList2.hpp", "hyprutils-VarList2.hpp:9-18 constructor and defaults", "tag v0.14.2"),
     "The default delimiter is a comma and empty fields are kept"),
    ("S315", "aquamarine v0.15.1 DRM backend - https://raw.githubusercontent.com/hyprwm/aquamarine/v0.15.1/src/backend/drm/DRM.cpp", "code", "A",
     "How a DRM output's description string is built (host aquamarine 0.15.1-1)",
     anchor("aquamarine-DRM.cpp", "aquamarine-DRM.cpp:1915-1940 EDID make model serial, aquamarine-DRM.cpp:2096-2104 output fields and description", "tag v0.15.1"),
     "A DRM output's description is make, model, serial and the connector name in parentheses"),
]
QUOTES = {
    "S302": ("Hyprland-Parser.cpp", "m_rule.m_refreshRate = stof(value.substr(value.find_first_of('@') + 1));"),
    "S303": ("Hyprland-legacy-ConfigManager.cpp", 'if (ARGS[1] == "disable" || ARGS[1] == "disabled" || ARGS[1] == "addreserved" || ARGS[1] == "transform") {'),
    "S304": ("Hyprland-MonitorRuleManager.cpp", "std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });"),
    "S305": ("Hyprland-MonitorRule.hpp", "float m_refreshRate = 60;"),
    "S306": ("Hyprland-Monitor.cpp", "float searchScale = std::round(m_scale * 120.0);"),
    "S307": ("Hyprland-HyprCtl.cpp", '"physicalHeight": {}, "refreshRate": {:.5f},'),
    "S308": ("Hyprland-MonitorPositionController.cpp", "m->moveTo(*POS); arranged.push_back(m); it = toArrange.erase(it);"),
    "S309": ("hyprutils-String.cpp", "if (i == 0 && str.at(i) == '-') {"),
    "S310": ("wiki-Monitors.md", "monitor = name, resolution, position, scale"),
    "S311": ("Hyprland-MonitorState.cpp", "mon->m_self = mon; m_realMonitors.emplace_back(mon);"),
    "S312": ("Hyprland-macros.hpp", "#define DELTALESSTHAN(a, b, delta) (abs((a) - (b)) < (delta))"),
    "S313": ("hyprutils-Vector2D.hpp", "constexpr Vector2D operator/(const double& a) const { return Vector2D(this->x / a, this->y / a);"),
    "S314": ("hyprutils-VarList2.hpp", "explicit CVarList2(std::string&& in, const size_t lastArgNo = 0, const char delim = ',',"),
    "S315": ("aquamarine-DRM.cpp", 'output->description = std::format("{} {} {} ({})", make, model, serial, szName);'),
}

src = open(os.path.join(D, "corpus/SOURCES.md")).read()
lines = src.split("\n")
last = max(k for k, l in enumerate(lines) if re.match(r"^\| S\d{3,} \|", l))
new = ["| %s | %s | %s | %s | %s | %s | %s | mined | 2026-10-26 | 90d | %s |" % (i, s, kd, t, sc, an, te, ENTRY)
       for (i, s, kd, t, sc, an, te) in ROWS]
for r in new:
    assert r.count("|") == 12, r
lines[last + 1:last + 1] = new
open(os.path.join(D, "corpus/SOURCES.md"), "w").write("\n".join(lines))
gate = ["## Gate", ""]
for i, (f, q) in QUOTES.items():
    gate.append('GATE %s receipt=%s%s sha256=%s quote="%s"' % (i, F, f, sha(f), q))
os.makedirs(os.path.join(D, "corpus/lessons"), exist_ok=True)
open(os.path.join(D, "corpus/lessons/round-45.md"), "w").write("# round 45 (positive control draft)\n\n" + "\n".join(gate) + "\n")
os.makedirs(os.path.join(D, "corpus/knowledge"), exist_ok=True)
open(os.path.join(D, ENTRY), "w").write(open(os.path.join(L1, "entry.md")).read())
rd = open(os.path.join(D, "corpus/README.md")).read().split("\n")
k = max(i for i, l in enumerate(rd) if l.startswith("| `knowledge/hyprland-gkeep-size-request-r44.md`"))
rd.insert(k + 1, "| `knowledge/hyprland-monitor-rule-r45.md` (MADO-R45-1, round 45) | draft | S302-S315 |")
open(os.path.join(D, "corpus/README.md"), "w").write("\n".join(rd))
print("applied")
