#!/usr/bin/env python3
"""Verify every fragment quoted in w1/ExecLiveHost.md: each must appear verbatim in the receipts or in a pinned fetch file.

    python3 -I qcheck.py     (run from this directory)

Prints PASS/FAIL per fragment and a total; exit 0 only when all PASS.
"""
import sys

HERE = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/ExecLiveHost"
F = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/fetch/"
RUN = HERE + "/runs.txt"

run = open(RUN, encoding="utf-8").read()


def pin(n):
    return open(F + n, encoding="utf-8").read()


checks = [
    (RUN, run, '"option": "input:kb_layout", "str": "br", "set": true'),
    (RUN, run, '"option": "input:kb_options", "str": "compose:caps", "set": true'),
    (RUN, run, '"option": "input:scroll_factor", "float": 1.000000, "set": false'),
    (RUN, run, '# hyprlang noerror true'),
    (RUN, run, '# hyprlang noerror false'),
    (RUN, run, 'name="hl-virtual-keyboard-fcitx5" block=no layout="br" variant="" options="compose:caps" model="" rules="" kb_file=- differ=- verdict=VIRTUAL'),
    (RUN, run, 'keyboards=10 agree=9 differ=0 fallback=0 virtual=1 mice=4 mice_differ=0 blocks=0 stale=0 unsupported=2 verdict=NOT_COMPARED'),
    (RUN, run, 'keyboards=10 agree=9 differ=0 fallback=0 virtual=1 mice=4 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK'),
    (RUN, run, 'keyboards=9 agree=0 differ=9 fallback=0 virtual=0 mice=4 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=DIFFER'),
    (RUN, run, 'keyboards=9 agree=0 differ=0 fallback=9 virtual=0'),
    (RUN, run, 'mice_differ=0 blocks=2 stale=1'),
    (RUN, run, 'active_keymap'),
    (RUN, run, "{'mice': 4, 'keyboards': 10, 'tablets': 0, 'touch': 0, 'switches': 0}"),
    (RUN, run, "mouse scrollFactors: [('razer-razer-deathadder-v2', -1.0)"),
    (RUN, run, "main: ['power-button-1']"),
    (RUN, run, "main: ['hl-virtual-keyboard-fcitx5']"),
    (F + "Hyprland-InputManager.cpp", pin("Hyprland-InputManager.cpp"), 'getDeviceString(devname, "kb_layout", "input:kb_layout")'),
    (F + "Hyprland-InputManager.cpp", pin("Hyprland-InputManager.cpp"), 'if (Config::mgr()->deviceConfigExplicitlySet(devname, "scroll_factor"))'),
    (F + "Hyprland-InputManager.cpp", pin("Hyprland-InputManager.cpp"), 'std::clamp(Config::mgr()->getDeviceFloat(devname, "scroll_factor", "input:scroll_factor"), 0.F, 100.F)'),
    (F + "Hyprland-InputManager.cpp", pin("Hyprland-InputManager.cpp"), 'm->m_scrollFactor = std::nullopt;'),
    (F + "Hyprland-InputManager.cpp", pin("Hyprland-InputManager.cpp"), 'getNameForNewDevice'),
    (F + "Hyprland-ConfigManager.cpp", pin("Hyprland-ConfigManager.cpp"), 'if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())'),
    (F + "Hyprland-ConfigValues.cpp", pin("Hyprland-ConfigValues.cpp"), 'MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us"'),
    (F + "Hyprland-IKeyboard.cpp", pin("Hyprland-IKeyboard.cpp"), 'm_currentRules.layout  = "us";'),
    (F + "Hyprland-IKeyboard.cpp", pin("Hyprland-IKeyboard.cpp"), 'm_currentRules.options = "";'),
    (F + "Hyprland-HyprCtl.cpp", pin("Hyprland-HyprCtl.cpp"), '"scrollFactor": {:.2f}'),
    (F + "Hyprland-HyprCtl.cpp", pin("Hyprland-HyprCtl.cpp"), '(k->m_active ? "true" : "false")'),
    (F + "Hyprland-MiscFunctions.cpp", pin("Hyprland-MiscFunctions.cpp"), 'std::string deviceNameToInternalString(const std::string& in)'),
]

bad = 0
for path, text, needle in checks:
    ok = needle in text
    if not ok:
        bad += 1
    print(("PASS" if ok else "FAIL"), path.rsplit("/", 1)[-1], "::", needle[:90])
print("total", len(checks), "fail", bad)
sys.exit(0 if bad == 0 else 1)
