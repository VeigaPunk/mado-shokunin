#!/usr/bin/env python3
"""Verify every quote in this seat's report: each fragment must occur on the cited line of the pinned file.

Locators are computed (the fragment is looked up in the pinned file and the line number compared), never typed
into the report without this check. Quote length is checked against the 25-word cap.
"""
import sys

FETCH = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/fetch"

# (file, line, quoted fragment)
QUOTES = [
    ("Hyprland-IKeyboard.cpp", 61, "if (m_keymapOverridden) {"),
    ("Hyprland-IKeyboard.cpp", 62, "Ignoring setKeymap: keymap is overridden"),
    ("Hyprland-IKeyboard.cpp", 66, "m_currentRules          = rules;"),
    ("Hyprland-IKeyboard.cpp", 87, "if (!m_xkbFilePath.empty()) {"),
    ("Hyprland-IKeyboard.cpp", 88, "auto path = absolutePath(m_xkbFilePath, Config::mgr()->currentConfigPath());"),
    ("Hyprland-IKeyboard.cpp", 91, "Cannot open input:kb_file= file for reading"),
    ("Hyprland-IKeyboard.cpp", 98, "if (!m_xkbKeymap)"),
    ("Hyprland-IKeyboard.cpp", 99, "m_xkbKeymap = xkb_keymap_new_from_names2(CONTEXT, &XKBRULES"),
    ("Hyprland-IKeyboard.cpp", 107, "memset(&XKBRULES, 0, sizeof(XKBRULES));"),
    ("Hyprland-IKeyboard.cpp", 113, 'm_currentRules.layout  = "us";'),
    ("Hyprland-IKeyboard.cpp", 214, "if (keymap) {"),
    ("Hyprland-InputManager.cpp", 1273, "FILEPATH == pKeyboard->m_xkbFilePath) {"),
    ("Hyprland-InputManager.cpp", 1274, "Not applying config to keyboard, it did not change."),
    ("Hyprland-InputManager.cpp", 1285, "pKeyboard->m_xkbFilePath = FILEPATH;"),
    ("Hyprland-InputManager.cpp", 1286, "pKeyboard->setKeymap(IKeyboard::SStringRuleNames{LAYOUT, MODEL, VARIANT, OPTIONS, RULES});"),
    ("Hyprland-HyprCtl.cpp", 794, '"active_keymap": "{}"'),
    ("Hyprland-HyprCtl.cpp", 799, "escapeJSONStrings(k->m_currentRules.rules)"),
    ("Hyprland-HyprCtl.cpp", 800, "escapeJSONStrings(k->m_currentRules.layout)"),
    ("Hyprland-ConfigManager.cpp", 736, "m_configCurrentPath = m_mainConfigPath;"),
    ("Hyprland-ConfigManager.cpp", 977, "g_pInputManager->setKeyboardLayout();"),
    ("Hyprland-ConfigManager.cpp", 1119, "if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())"),
    ("Hyprland-ConfigManager.cpp", 1120, 'return m_config->getConfigValuePtr(fallback.c_str());'),
    ("Hyprland-ConfigManager.cpp", 1838, "m_configCurrentPath          = value;"),
    ("Hyprland-ConfigManager.cpp", 1840, "= configCurrentPathBackup;"),
    ("Hyprland-MiscFunctions.cpp", 61, "std::string absolutePath(const std::string& rawpath, const std::string& currentPath) {"),
    ("Hyprland-MiscFunctions.cpp", 68, "auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));"),
    ("Hyprland-ConfigValues.cpp", 272, '"us"'),
    ("Hyprland-ConfigValues.cpp", 276, "STRVAL_EMPTY"),
    ("Hyprland-VirtualKeyboard.cpp", 41, "m_keymapOverridden = true;"),
    ("Hyprland-IKeyboard.cpp", 306, "std::string IKeyboard::getActiveLayout() {"),
    ("Hyprland-IKeyboard.cpp", 313, "const auto LAYOUTNAME = xkb_keymap_layout_get_name(KEYMAP, i);"),
    ("Hyprland-ConfigManager.cpp", 522, 'addSpecialConfigValue("device", "kb_file", {STRVAL_EMPTY})'),
    ("Hyprland-ConfigManager.cpp", 1163, "if (VAL == STRVAL_EMPTY)"),
    ("Hyprland-ConfigManager.cpp", 2146, "return m_configCurrentPath;"),
    ("Hyprland-InputManager.cpp", 1195, "applyConfigToKeyboard(keeb);"),
    ("Hyprland-InputManager.cpp", 1278, "can be libc errors for null std::string"),
    ("Hyprland-InputManager.cpp", 1206, "void CInputManager::setKeyboardLayout() {"),
]

REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/l1-draft/mado-devices.py"
REF_QUOTES = [
    (15, "its printed rules do not witness its keymap"),
    (73, "the compositor's fallback after a keymap that does not compile"),
    (107, 'EMPTY = "[[EMPTY]]"'),
    (346, 'if k in blk:'),
]

bad = 0
for fname, lineno, frag in QUOTES:
    path = "%s/%s" % (FETCH, fname)
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    hit = [i + 1 for i, t in enumerate(lines) if frag in t]
    words = len(frag.split())
    ok = lineno in hit and words <= 25
    if not ok:
        bad += 1
    print("%s %s:%d words=%d hit=%s :: %s" % ("OK  " if ok else "FAIL", fname, lineno, words,
                                              hit if hit else "none", frag))
for lineno, frag in REF_QUOTES:
    with open(REF, encoding="utf-8") as f:
        lines = f.readlines()
    hit = [i + 1 for i, t in enumerate(lines) if frag in t]
    words = len(frag.split())
    ok = lineno in hit and words <= 25
    if not ok:
        bad += 1
    print("%s mado-devices.py:%d words=%d hit=%s :: %s" % ("OK  " if ok else "FAIL", lineno, words, hit if hit else "none", frag))
print("MADO_QUOTES: total=%d failed=%d" % (len(QUOTES) + len(REF_QUOTES), bad))
sys.exit(1 if bad else 0)
