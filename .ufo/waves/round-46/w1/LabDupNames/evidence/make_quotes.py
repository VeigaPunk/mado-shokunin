#!/usr/bin/env python3
"""Generate and verify the quoted-locator receipt for seat LabDupNames.

Every quoted line in report.md must be <= 25 words, located by a computed line number
(grep -n on the pinned fetch tree), and reproduced byte-for-byte in evidence/quotes.txt.
Run: python3 evidence/make_quotes.py   (writes quotes.txt, exits nonzero on any mismatch)
"""
import pathlib
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/mado-shokunin")
FETCH = LANE / ".ufo/waves/round-46/fetch"
HERE = pathlib.Path(__file__).resolve().parent

# (file, line, substring that must be on that line, and is the quoted text)
SPEC = [
    ("Hyprland-ConfigManager.cpp", 518, 'addSpecialCategory("device", {"name"});'),
    ("Hyprland-ConfigManager.cpp", 1117, 'getSpecialConfigValuePtr("device", val.c_str(), dev.c_str());'),
    ("Hyprland-ConfigManager.cpp", 1198, "std::ranges::replace(copy, ' ', '-');"),
    ("Hyprland-InputManager.cpp", 1138, "m_hids.emplace_back(keeb);"),
    ("Hyprland-InputManager.cpp", 1141, "keeb->m_hlName = getNameForNewDevice(keeb->m_deviceName);"),
    ("Hyprland-InputManager.cpp", 1322, "m_hids.emplace_back(mauz);"),
    ("Hyprland-InputManager.cpp", 1532, "std::erase_if(g_pInputManager->m_hids"),
    ("Hyprland-InputManager.cpp", 1946, "m_hids.emplace_back(PNEWDEV);"),
    ("Hyprland-InputManager.cpp", 2119, "std::string CInputManager::getNameForNewDevice(std::string internalName) {"),
    ("Hyprland-InputManager.cpp", 2124, '"-" + std::to_string(dupeno)'),
    ("Hyprland-InputManager.cpp", 2126, "while (std::ranges::find_if(m_hids"),
    ("Hyprland-MiscFunctions.cpp", 777, "std::string deviceNameToInternalString(const std::string& in) {"),
    ("Hyprland-HyprCtl.cpp", 772, "escapeJSONStrings(m->m_hlName)"),
    ("Hyprland-HyprCtl.cpp", 799, "escapeJSONStrings(k->m_hlName)"),
    ("hyprlang-config.cpp", 1089, "sc->name != CAT"),
    ("hyprlang-config.cpp", 1089, "!= KEY"),
    ("hyprlang-config.cpp", 1117, "sc->name != category"),
    ("hyprlang-config.cpp", 1117, "!= key"),
    ("wiki-Keywords.md", 79, "hyprctl devices"),
    ("quality/counters/c1-r46-devices.py", 116, 'SUFFIX = ["", "", "-keyboard"'),
    ("quality/counters/c1-r46-devices.py", 124, "if all(n not in p and p not in n for p in picked):"),
]


def main() -> int:
    bad = 0
    out = []
    for name, line, sub in SPEC:
        path = LANE / name if name.startswith("quality/") else FETCH / name
        text = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if line < 1 or line > len(text):
            print(f"FAIL {name}:{line} out of range (file has {len(text)} lines)")
            bad += 1
            continue
        actual = text[line - 1]
        if sub not in actual:
            print(f"FAIL {name}:{line} does not contain {sub!r}; line is {actual!r}")
            bad += 1
            continue
        if len(sub.split()) > 25:
            print(f"FAIL {name}:{line} quote over 25 words: {sub!r}")
            bad += 1
            continue
        out.append(f"{name}:{line}\t{sub}")
    (HERE / "quotes.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"quotes={len(out)} verified, failures={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
