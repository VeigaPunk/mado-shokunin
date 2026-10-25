#!/usr/bin/env python3
"""Writes corpus/lessons/round-40.md with digests computed from the committed
receipts (the Gate lines are what PRED-C2-r40-v2 clause d reads)."""
import hashlib
import os

L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
F = ".ufo/waves/round-40/fetch/"
GATE = [
    ("S158", "hyprctl-efb5099.bin",
     'R"({{"option": "{}", "vec2": [{},{}], "set": {} }})"'),
    ("S162", "config-manager-efb5099.bin",
     'DATA->m_angle = std::stoi(std::string(var.substr(0, var.find("deg")))) * (std::numbers::pi / 180.0); // radians'),
    ("S173", "hyprlang-config-v0.6.8.bin",
     "a = std::round(std::stof(trim(rolling.substr(0, rolling.find(',')))) * 255.f);"),
    ("S180", "complex-data-types-efb5099.bin",
     'return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);'),
    ("S181", "parser-utils-efb5099.bin", "std::floor(*a * 255.F)"),
    ("S215", "config-values-efb5099.bin",
     '"shadow\'s rendering offset.", Config::VEC2{},'),
    ("S278", "wiki-0.54.0-using-hyprctl.html",
     "getoption [option] - gets the config option status (values)"),
    ("S279", "census-receipt.txt",
     "census: 70 declared keys queried once each with hyprctl getoption -j"),
    ("S280", "omarchy-v3.8.4-screen-recording.bin",
     'if pgrep -f "^gpu-screen-recorder" >/dev/null; then'),
    ("S281", "omarchy-v3.8.4-notification-silencing.bin",
     "if makoctl mode | grep -q 'do-not-disturb'; then"),
    ("S282", "host-k2-reads.txt", '"exec": "~/.local/bin/gkeep waybar",'),
]
lines = []
for i, fn, q in GATE:
    blob = open(os.path.join(L, F, fn), "rb").read()
    lines.append('GATE %s receipt=%s%s sha256=%s quote="%s"'
                 % (i, F, fn, hashlib.sha256(blob).hexdigest(), q))
tmpl = open(os.path.join(L, ".ufo/waves/round-40/data/lesson-template.md")).read()
out = tmpl.replace("@@GATE@@", "\n".join(lines))
open(os.path.join(L, "corpus/lessons/round-40.md"), "w").write(out)
print(len(lines), len(out))
