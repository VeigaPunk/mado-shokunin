#!/usr/bin/env python3
"""Apply the L1 draft (entry, rows S316-S325, lesson Gate, README row) to a lane checkout at DIR (positive control
for PRED-C2-r46; never run against the lane itself)."""
import hashlib
import os
import re
import sys

D = sys.argv[1]
L1 = os.environ.get("L1DRAFT", "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/l1-draft")
F = ".ufo/waves/round-46/fetch/"
ENTRY = "corpus/knowledge/hyprland-input-devices-r46.md"
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
    ("S316", "Hyprland v0.56.2 input manager - per-device config application - " + HY + "managers/input/InputManager.cpp", "code", "A",
     "How a keyboard's XKB names and a pointer's scroll factor are chosen per device (host Hyprland 0.56.2)",
     anchor("Hyprland-InputManager.cpp", "Hyprland-InputManager.cpp:1213-1295 applyConfigToKeyboard, Hyprland-InputManager.cpp:1350-1383 setPointerConfigs scroll factor, Hyprland-InputManager.cpp:2119-2131 getNameForNewDevice", "commit " + C),
     "Each kb_ name is read from the device block first and the global input option second; a pointer prints a scroll factor only when its block sets one"),
    ("S317", "Hyprland v0.56.2 legacy config manager - the device special category - " + HY + "config/legacy/ConfigManager.cpp", "code", "A",
     "Per-device config storage and the per-device to global fallback rule",
     anchor("Hyprland-ConfigManager.cpp", "Hyprland-ConfigManager.cpp:518-565 device category values, Hyprland-ConfigManager.cpp:1115-1201 getConfigValueSafeDevice getDeviceString deviceConfigExists", "commit " + C),
     "A device value counts only when the user set it, else the global option applies; the empty marker reads as an empty string"),
    ("S318", "Hyprland v0.56.2 config value table - " + HY + "config/values/ConfigValues.cpp", "code", "A",
     "Defaults of the global keyboard names and of the global scroll factor",
     anchor("Hyprland-ConfigValues.cpp", "Hyprland-ConfigValues.cpp:271-279 input kb options, Hyprland-ConfigValues.cpp:296 input scroll_factor", "commit " + C),
     "The global layout defaults to us and the other keymap names to empty"),
    ("S319", "Hyprland v0.56.2 keyboard base - " + HY + "devices/IKeyboard.cpp", "code", "A",
     "What a keyboard stores as its current rules and what happens when they do not compile",
     anchor("Hyprland-IKeyboard.cpp", "Hyprland-IKeyboard.cpp:60-145 setKeymap", "commit " + C),
     "Stored rules are the names asked for; on a compile failure they reset to layout us with the rest empty; an overridden keymap ignores new names"),
    ("S320", "Hyprland v0.56.2 hyprctl - the devices request - " + HY + "debug/HyprCtl.cpp", "code", "A",
     "The devices request and the JSON fields it prints per keyboard and pointer",
     anchor("Hyprland-HyprCtl.cpp", "Hyprland-HyprCtl.cpp:748-805 devicesRequest mice and keyboards", "commit " + C),
     "Keyboards print their stored rules; pointers print scrollFactor with two decimals"),
    ("S321", "Hyprland v0.56.2 helper functions - device name normalizer - " + HY + "helpers/MiscFunctions.cpp", "code", "A",
     "How a device's name is derived from its kernel name",
     anchor("Hyprland-MiscFunctions.cpp", "Hyprland-MiscFunctions.cpp:777-789 deviceNameToInternalString", "commit " + C),
     "Names are lower-cased and space, newline and comma become a dash"),
    ("S322", "Hyprland v0.56.2 virtual keyboard device - " + HY + "devices/VirtualKeyboard.cpp", "code", "A",
     "How a virtual keyboard takes its client's keymap",
     anchor("Hyprland-VirtualKeyboard.cpp", "Hyprland-VirtualKeyboard.cpp:36-44 keymap listener", "commit " + C),
     "A client keymap marks the keyboard's keymap overridden"),
    ("S323", "Hyprland v0.56.2 virtual keyboard protocol - " + HY + "protocols/VirtualKeyboard.cpp", "code", "A",
     "The name a virtual keyboard device receives",
     anchor("Hyprland-protocols-VirtualKeyboard.cpp", "Hyprland-protocols-VirtualKeyboard.cpp:11-30 virtualKeyboardNameForWlClient", "commit " + C),
     "Virtual keyboards are named hl-virtual-keyboard plus the normalized client binary name when name_vk_after_proc is on"),
    ("S324", "hyprlang v0.6.8 config parser - https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp", "code", "A",
     "How the config language reads comments, continuations and keyed special categories (host hyprlang 0.6.8-5)",
     anchor("hyprlang-config.cpp", "hyprlang-config.cpp:44-66 getNextLine, hyprlang-config.cpp:291-440 special category keys, hyprlang-config.cpp:669-705 comments, hyprlang-config.cpp:885-912 category close", "tag v0.6.8"),
     "A doubled hash is a literal hash; a bracketed name addresses a keyed category; a block must start with its key"),
    ("S325", "Hyprland wiki Keywords page (hyprlang era) - per-device input configs - https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605e453c0ad533d979fccbefff788ef/content/Configuring/Keywords.md", "docs", "A",
     "The documented per-device input block",
     anchor("wiki-Keywords.md", "wiki-Keywords.md:64-94 Per-device input configs", "commit ecc06f3b6605e453c0ad533d979fccbefff788ef (2026-04-20)"),
     "Per-device options overwrite input options only where explicitly set; the name comes from hyprctl devices"),
]
QUOTES = {
    "S316": ("Hyprland-InputManager.cpp", 'const auto LAYOUT = Config::mgr()->getDeviceString(devname, "kb_layout", "input:kb_layout");'),
    "S317": ("Hyprland-ConfigManager.cpp", "if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())"),
    "S318": ("Hyprland-ConfigValues.cpp", 'MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",'),
    "S319": ("Hyprland-IKeyboard.cpp", 'm_currentRules.layout = "us";'),
    "S320": ("Hyprland-HyprCtl.cpp", '"defaultSpeed": {:.5f}, "scrollFactor": {:.2f}'),
    "S321": ("Hyprland-MiscFunctions.cpp", "case ',': return '-';"),
    "S322": ("Hyprland-VirtualKeyboard.cpp", "m_keymapOverridden = true;"),
    "S323": ("Hyprland-protocols-VirtualKeyboard.cpp", 'std::string name = "hl-virtual-keyboard";'),
    "S324": ("hyprlang-config.cpp", "special category's first value must be the key."),
    "S325": ("wiki-Keywords.md", "It's worth noting that ONLY values explicitly changed will be overwritten."),
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
open(os.path.join(D, "corpus/lessons/round-46.md"), "w").write("# round 46 (positive control draft)\n\n" + "\n".join(gate) + "\n")
os.makedirs(os.path.join(D, "corpus/knowledge"), exist_ok=True)
open(os.path.join(D, ENTRY), "w").write(open(os.path.join(L1, "entry.md")).read())
rd = open(os.path.join(D, "corpus/README.md")).read().split("\n")
k = max(i for i, l in enumerate(rd) if l.startswith("| `knowledge/hyprland-monitor-rule-r45.md`"))
rd.insert(k + 1, "| `knowledge/hyprland-input-devices-r46.md` (MADO-R46-1, round 46) | draft | S316-S325 |")
open(os.path.join(D, "corpus/README.md"), "w").write("\n".join(rd))
print("applied")
