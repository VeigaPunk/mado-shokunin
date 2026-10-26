#!/usr/bin/env python3
"""Verify every quote the ExecC2Census report lifts from a pin is verbatim on the
named line. Each entry is (receipt, line, snippet); the snippet must be a substring
of that line (or, for fragments that wrap, of the line joined with the next one).
"""
import os
import sys

F = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/fetch"

CASES = [
    ("Hyprland-InputManager.cpp", 1213, "void CInputManager::applyConfigToKeyboard(SP<IKeyboard> pKeyboard) {"),
    ("Hyprland-InputManager.cpp", 1229, 'const auto LAYOUT   = Config::mgr()->getDeviceString(devname, "kb_layout", "input:kb_layout");'),
    ("Hyprland-InputManager.cpp", 1286, "pKeyboard->setKeymap(IKeyboard::SStringRuleNames{LAYOUT, MODEL, VARIANT, OPTIONS, RULES});"),
    ("Hyprland-InputManager.cpp", 1274, 'Log::logger->log(Log::DEBUG, "Not applying config to keyboard, it did not change.");'),
    ("Hyprland-InputManager.cpp", 1379, 'if (Config::mgr()->deviceConfigExplicitlySet(devname, "scroll_factor"))'),
    ("Hyprland-InputManager.cpp", 1382, "m->m_scrollFactor = std::nullopt;"),
    ("Hyprland-InputManager.cpp", 2119, "std::string CInputManager::getNameForNewDevice(std::string internalName) {"),
    ("Hyprland-ConfigManager.cpp", 518, 'm_config->addSpecialCategory("device", {"name"});'),
    ("Hyprland-ConfigManager.cpp", 1119, "if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())"),
    ("Hyprland-ConfigManager.cpp", 1196, "bool CConfigManager::deviceConfigExists(const std::string& dev) {"),
    ("Hyprland-ConfigManager.cpp", 1163, "if (VAL == STRVAL_EMPTY)"),
    ("Hyprland-ConfigValues.cpp", 272, 'MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",'),
    ("Hyprland-ConfigValues.cpp", 296, 'MS<Float>("input:scroll_factor", "Multiplier added to scroll movement for external mice.", 1, {.min = 0, .max = 2,'),
    ("Hyprland-IKeyboard.cpp", 113, 'm_currentRules.layout  = "us";'),
    ("Hyprland-IKeyboard.cpp", 107, "memset(&XKBRULES, 0, sizeof(XKBRULES));"),
    ("Hyprland-IKeyboard.cpp", 61, "if (m_keymapOverridden) {"),
    ("Hyprland-IKeyboard.cpp", 87, "if (!m_xkbFilePath.empty()) {"),
    ("Hyprland-IKeyboard.cpp", 258, 'rules.layout = "us";'),
    ("Hyprland-HyprCtl.cpp", 770, '"scrollFactor": {:.2f}'),
    ("Hyprland-HyprCtl.cpp", 769, '"defaultSpeed": {:.5f},'),
    ("Hyprland-HyprCtl.cpp", 800, "escapeJSONStrings(k->m_currentRules.layout)"),
    ("Hyprland-VirtualKeyboard.cpp", 41, "m_keymapOverridden = true;"),
    ("Hyprland-protocols-VirtualKeyboard.cpp", 12, 'std::string name = "hl-virtual-keyboard";'),
    ("Hyprland-MiscFunctions.cpp", 777, "std::string deviceNameToInternalString(const std::string& in) {"),
    ("Hyprland-MiscFunctions.cpp", 782, "case ',': return '-';"),
    ("Hyprland-MiscFunctions.cpp", 784, "default: return sc<char>(std::tolower(ch));"),
    ("Hyprland-MiscFunctions.cpp", 780, "case ' ':"),
    ("Hyprland-MiscFunctions.cpp", 781, "case '\\n':"),
    ("hyprlang-config.cpp", 291, "if (valueName.contains('[') && valueName.contains(']')) {"),
    ("hyprlang-config.cpp", 435, 'result.setError(std::format("special category\'s first value must be the key. Key for <{}> is <{}>", PCAT->name, PCAT->key));'),
    ("hyprlang-config.cpp", 434, "if (VALUEIT == PCAT->values.end() || VALUEIT->first != sc->key) {"),
    ("hyprlang-config.cpp", 691, "if (line[commentPos + 1] == '#') {"),
    ("hyprlang-config.cpp", 676, "if (commentPos == 0) {"),
    ("hyprlang-config.cpp", 677, "const auto COMMENT_RESULT = impl->parseComment(line.substr(1));"),
    ("hyprlang-config.cpp", 53, "while (line.length() > 0 && line.at(line.length() - 1) == '\\\\') {"),
    ("hyprlang-config.cpp", 896, 'impl->currentSpecialKey      = "";'),
    ("hyprlang-config.cpp", 893, "impl->categories.pop_back();"),
    ("wiki-Keywords.md", 66, "Per-device config options will overwrite your options set in the `input`"),
    ("wiki-Keywords.md", 79, "The `name` can be easily obtained by checking the output of `hyprctl devices`."),
    ("Hyprland-ConfigManager.cpp", 519, 'm_config->addSpecialConfigValue("device", "sensitivity", {0.F});'),
    ("Hyprland-ConfigManager.cpp", 565, 'm_config->addSpecialConfigValue("device", "pressure_range_max", Hyprlang::FLOAT{-1.0});'),
    ("Hyprland-InputManager.cpp", 972, 'static auto PTOUCHPADSCROLLFACTOR = CConfigValue<Config::FLOAT>("input:touchpad:scroll_factor");'),
    ("Hyprland-protocols-VirtualKeyboard.cpp", 14, 'static auto PVKNAMEPROC = CConfigValue<Config::INTEGER>("misc:name_vk_after_proc");'),
    ("Hyprland-ConfigManager.cpp", 1198, "std::ranges::replace(copy, ' ', '-');"),
]

bad = 0
for rname, ln, snippet in CASES:
    lines = open(os.path.join(F, rname), encoding="utf-8", errors="replace").read().split("\n")
    joined = lines[ln - 1] + " " + (lines[ln] if ln < len(lines) else "")
    ok = snippet in lines[ln - 1] or snippet in joined
    bad += 0 if ok else 1
    print("%-4s %-38s:%d  %s" % ("OK" if ok else "FAIL", rname, ln, snippet[:70]))
print("quotes_verified=%d/%d bad=%d" % (len(CASES) - bad, len(CASES), bad))
sys.exit(1 if bad else 0)
