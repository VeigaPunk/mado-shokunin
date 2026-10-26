#!/usr/bin/env python3
"""Verify every locator in sections.md against the pinned bytes (seat ScrEntryDraft, round 46).

For each locator: the anchor string must occur exactly once in the receipt, and its computed line
(grep -n equivalent) must fall inside the cited range; the range must be <= 30 lines wide and inside
the file. Every locator that appears in sections.md must appear in the table below, so a typed locator
cannot slip through unverified. Host-config claims (line numbers in ~/.config/hypr/hyprland.conf and the
two input.conf files) are checked separately at the end.
"""
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = LANE + "/.ufo/waves/round-46/fetch/"
L1 = LANE + "/.ufo/waves/round-46/l1-draft/"
SECT = LANE + "/.ufo/waves/round-46/w1/ScrEntryDraft/sections.md"
WIDTH = 30

# (receipt, a, b, anchor that must occur exactly once and inside [a, b])
TABLE = [
    ("Hyprland-IKeyboard.cpp", 101, 116, 'ErrorOverlay::overlay()->queueError("Invalid keyboard layout passed.'),
    ("Hyprland-IKeyboard.cpp", 102, 103, 'ErrorOverlay::overlay()->queueError("Invalid keyboard layout passed.'),
    ("Hyprland-IKeyboard.cpp", 102, 106, 'ErrorOverlay::overlay()->queueError("Invalid keyboard layout passed.'),
    ("Hyprland-IKeyboard.cpp", 98, 116, 'ErrorOverlay::overlay()->queueError("Invalid keyboard layout passed.'),
    ("Hyprland-IKeyboard.cpp", 87, 99, "Cannot open input:kb_file= file for reading"),
    ("Hyprland-IKeyboard.cpp", 87, 96, "Cannot open input:kb_file= file for reading"),
    ("Hyprland-IKeyboard.cpp", 60, 66, "void IKeyboard::setKeymap(const SStringRuleNames& rules) {"),
    ("Hyprland-IKeyboard.cpp", 306, 321, "std::string IKeyboard::getActiveLayout() {"),
    ("Hyprland-HyprCtl.cpp", 1188, 1192, "m_currentRequestParams.isDynamicKeyword = true;"),
    ("Hyprland-HyprCtl.cpp", 1203, 1208, 'if (COMMAND.contains("input") || COMMAND.contains("device") || COMMAND == "source") {'),
    ("Hyprland-HyprCtl.cpp", 785, 798, '"active_keymap": "{}",'),
    ("Hyprland-HyprCtl.cpp", 785, 802, '"active_keymap": "{}",'),
    ("Hyprland-HyprCtl.cpp", 781, 794, '"active_layout_index": {},'),
    ("Hyprland-HyprCtl.cpp", 1368, 1396, "const auto         LAYOUTS      = xkb_keymap_num_layouts(KEEB->m_xkbKeymap);"),
    ("Hyprland-HyprCtl.cpp", 1160, 1163, "if (Config::mgr()->type() != Config::CONFIG_LEGACY)"),
    ("hyprlang-config.cpp", 1064, 1068, "CParseResult CConfig::parseDynamic(const char* command, const char* value) {"),
    ("hyprlang-config.cpp", 915, 926, "CParseResult CConfig::parse() {"),
    ("hyprlang-config.cpp", 1083, 1099, "CConfigValue* CConfig::getSpecialConfigValuePtr(const char* category, const char* name, const char* key) {"),
    ("Hyprland-ConfigManager.cpp", 726, 751, "void CConfigManager::reload() {"),
    ("Hyprland-ConfigManager.cpp", 970, 980, "void CConfigManager::postConfigReload(const Hyprlang::CParseResult& result) {"),
    ("Hyprland-ConfigManager.cpp", 614, 614, 'm_config->registerHandler(&::handleSource, "source", {false});'),
    ("Hyprland-ConfigManager.cpp", 1816, 1841, "if (auto r = glob(absolutePath(rawpath, m_configCurrentPath).c_str()"),
    ("Hyprland-ConfigManager.cpp", 1196, 1201, "bool CConfigManager::deviceConfigExists(const std::string& dev) {"),
    ("Hyprland-MiscFunctions.cpp", 777, 789, "std::string deviceNameToInternalString(const std::string& in) {"),
    ("Hyprland-InputManager.cpp", 2119, 2131, "std::string CInputManager::getNameForNewDevice(std::string internalName) {"),
    ("Hyprland-InputManager.cpp", 1233, 1240, 'const auto ENABLED    = HASCONFIG && Config::mgr()->deviceConfigExplicitlySet(devname, "enabled")'),
    ("Hyprland-InputManager.cpp", 1233, 1238, 'const auto ENABLED    = HASCONFIG && Config::mgr()->deviceConfigExplicitlySet(devname, "enabled")'),
    ("Hyprland-InputManager.cpp", 1619, 1621, "void CInputManager::onKeyboardKey(const IKeyboard::SKeyEvent& event, SP<IKeyboard> pKeyboard) {"),
    ("Hyprland-InputManager.cpp", 1685, 1688, "void CInputManager::onKeyboardMod(SP<IKeyboard> pKeyboard) {"),
    ("Hyprland-InputManager.cpp", 1379, 1382, 'if (Config::mgr()->deviceConfigExplicitlySet(devname, "scroll_factor"))'),
    ("Hyprland-InputManager.cpp", 1270, 1280, "Not applying config to keyboard, it did not change."),
    ("Hyprland-ConfigValues.cpp", 296, 296, 'MS<Float>("input:scroll_factor",'),
    ("Hyprland-ConfigValues.cpp", 324, 324, 'MS<Float>("input:touchpad:scroll_factor",'),
    ("hyprlang-config.cpp", 465, 471, "VALUEIT->second.setFrom(std::stof(value));"),
    ("mado-devices.py", 39, 42, "an if/endif/noerror directive"),
    ("mado-devices.py", 62, 66, "value is read as std::stof does"),
    ("hyprlang-config.cpp", 885, 899, 'impl->currentSpecialKey      = "";'),
    ("mado-devices.py", 71, 73, "Verdict, tested in this order"),
    ("mado-devices.py", 87, 89, "V = NOT_COMPARED (exit 5"),
    ("mado-devices.py", 48, 50, "A key line is RELEVANT when KEY starts with"),
    ("mado-devices.py", 22, 26, "hyprctl devices -j | mado-devices.py"),
    ("mado-devices.py", 36, 36, "Config files are read in argument order"),
]
RECEIPTS = sorted({t[0] for t in TABLE})


def path_of(name):
    return (L1 if name == "mado-devices.py" else FETCH) + name


def lines_of(name):
    with open(path_of(name), "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


bad = 0
print("SCR_ENTRY_DRAFT locator check: %d locators over %d receipts, width <= %d" % (len(TABLE), len(RECEIPTS), WIDTH))
for rname, a, b, anchor in TABLE:
    rl = lines_of(rname)
    hits = [n for n, l in enumerate(rl, 1) if anchor in l]
    width = b - a
    ok = len(hits) == 1 and a <= hits[0] <= b and 0 <= width <= WIDTH and b <= len(rl)
    bad += 0 if ok else 1
    print("%s %-30s %4d-%-4d L=%-5s width=%-3d lines=%-5d %s" % (
        "PASS" if ok else "FAIL", rname, a, b, hits[0] if len(hits) == 1 else "%d hits" % len(hits), width, len(rl),
        "anchor=%r" % anchor[:64]))

# every locator written in sections.md must be in TABLE
text = open(SECT, "r", encoding="utf-8").read()
found = re.findall(r"(?<![\w.-])(Hyprland-[A-Za-z-]+\.cpp|hyprlang-config\.cpp|wiki-Keywords\.md|mado-devices\.py):(\d+)(?:-(\d+))?(?!\d)", text)
table_ranges = {(r, a, b if b is not None else a) for r, a, b, _ in TABLE}
print("\nlocators written in sections.md: %d occurrences, %d distinct" % (len(found), len(set(found))))
for r, a, b in sorted(set(found)):
    b2 = b or a
    hit = (r, int(a), int(b2)) in table_ranges
    bad += 0 if hit else 1
    print("%s %s:%s%s" % ("IN-TABLE" if hit else "MISSING", r, a, "-" + b if b else ""))
for r, a, b, _ in TABLE:
    if not any(f[0] == r and int(f[1]) == a and int(f[2] or f[1]) == b for f in found):
        print("NOTE unused-in-sections %s:%d-%d" % (r, a, b))

# host config claims
HOST = os.path.expanduser("~/.config/hypr/hyprland.conf")
hl = open(HOST, "r", encoding="utf-8", errors="replace").read().split("\n")
print("\nhost %s: %d lines" % ("~/.config/hypr/hyprland.conf", len(hl)))
for n, want in ((11, "~/.local/share/omarchy/default/hypr/input.conf"), (17, "~/.config/hypr/input.conf"), (23, "hypr/*.conf")):
    ok = want in hl[n - 1] and hl[n - 1].lstrip().startswith("source")
    bad += 0 if ok else 1
    print("%s line %d: %s" % ("PASS" if ok else "FAIL", n, hl[n - 1].strip()[:120]))
OM = os.path.expanduser("~/.local/share/omarchy/default/hypr/input.conf")
HO = os.path.expanduser("~/.config/hypr/input.conf")
for label, p in (("omarchy default", OM), ("host file", HO)):
    tl = open(p, "r", encoding="utf-8", errors="replace").read().split("\n")
    keys = [l.split("=")[0].strip() for l in tl if re.match(r"^\s*kb_[a-z_]+\s*=", l)]
    print("%-16s %-52s kb keys=%s" % (label, p.replace(os.path.expanduser("~"), "~"), ",".join(keys)))
print("kb keys in omarchy default: 5 expected; host file: kb_layout,kb_options (2 expected)")
ok = len([l for l in open(OM).read().split("\n") if re.match(r"^\s*kb_[a-z_]+\s*=", l)]) == 5
ok2 = [l.split("=")[0].strip() for l in open(HO).read().split("\n") if re.match(r"^\s*kb_[a-z_]+\s*=", l)] == ["kb_layout", "kb_options"]
bad += 0 if ok and ok2 else 1
print("%s input.conf key sets (omarchy=5, host=kb_layout,kb_options)" % ("PASS" if ok and ok2 else "FAIL"))

print("\nSCR_ENTRY_DRAFT VERDICT: %s (failures=%d)" % ("PASS" if bad == 0 else "FAIL", bad))
sys.exit(0 if bad == 0 else 1)
