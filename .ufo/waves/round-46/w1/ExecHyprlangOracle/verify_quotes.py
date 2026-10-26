#!/usr/bin/env python3
"""Verify every quote used by the report: assert the cited line contains the quoted text (grep by line number,
computed from the file, never typed). Writes a receipt line per quote.
"""
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = os.path.join(LANE, ".ufo/waves/round-46/fetch")

QUOTES = [
    (os.path.join(FETCH, "hyprlang-config.cpp"), 376, "if (existingKeyValue != impl->currentSpecialKey)"),
    (os.path.join(FETCH, "hyprlang-config.cpp"), 438, "impl->currentSpecialKey = value;"),
    (os.path.join(FETCH, "hyprlang-config.cpp"), 896, 'impl->currentSpecialKey      = "";'),
    (os.path.join(FETCH, "hyprlang-config.cpp"), 467, "VALUEIT->second.setFrom(std::stof(value));"),
    (os.path.join(FETCH, "hyprlang-config.cpp"), 297, "impl->currentSpecialKey = CATKEY;"),
    (os.path.join(FETCH, "hyprlang-config.cpp"), 348, "if (impl->currentSpecialCategory && valueName.starts_with(impl->currentSpecialCategory->name))"),
    (os.path.join(FETCH, "hyprlang-config.cpp"), 1044, "if (!impl->categories.empty())"),
    (os.path.join(FETCH, "Hyprland-HyprCtl.cpp"), 770, '"scrollFactor": {:.2f}'),
    (os.path.join(FETCH, "Hyprland-InputManager.cpp"), 1380, "std::clamp(Config::mgr()->getDeviceFloat(devname, \"scroll_factor\", \"input:scroll_factor\"), 0.F, 100.F)"),
    (os.path.join(FETCH, "Hyprland-ConfigManager.cpp"), 1117, 'getSpecialConfigValuePtr("device", val.c_str(), dev.c_str())'),
    (os.path.join(FETCH, "Hyprland-ConfigManager.cpp"), 1128, "return VAL && VAL->m_bSetByUser;"),
    (os.path.join(FETCH, "Hyprland-ConfigManager.cpp"), 518, 'addSpecialCategory("device", {"name"})'),
    (os.path.join(FETCH, "Hyprland-ConfigValues.cpp"), 272, '"input:kb_layout", "Appropriate XKB keymap parameter", "us"'),
    ("/usr/include/hyprland/src/macros.hpp", 24, '#define STRVAL_EMPTY "[[EMPTY]]"'),
    (os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py"), 58, "with no current device: adds one to `unsupported`"),
    (os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py"), 64, "no such prefix leaves the key unset; a prefix that is inf/nan/hex"),
    (os.path.join(LANE, ".ufo/waves/round-46/l1-draft/mado-devices.py"), 62, "A `scroll_factor`"),
]


def main():
    bad = 0
    for path, lineno, quote in QUOTES:
        lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
        actual = lines[lineno - 1] if lineno - 1 < len(lines) else ""
        ok = quote in actual
        bad += 0 if ok else 1
        print("%s %s:%d %r" % ("OK  " if ok else "FAIL", os.path.basename(path), lineno, quote))
        if not ok:
            print("      actual: %r" % actual.strip()[:160])
    print("QUOTES: %d/%d verified" % (len(QUOTES) - bad, len(QUOTES)))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
