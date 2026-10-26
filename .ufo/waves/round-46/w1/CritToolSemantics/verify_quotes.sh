#!/bin/sh
# Verifies every quote used in the report against the pinned sources / host headers.
F=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/fetch
H=/usr/include/hyprland/src/macros.hpp
chk() { f=$1; n=$2; line=$(grep -nF -- "$n" "$f" | head -1 | cut -d: -f1); if [ -n "$line" ]; then echo "OK   $(basename $f):$line  $n"; else echo "MISS $(basename $f)  $n"; fi }
chk $F/Hyprland-IKeyboard.cpp 'if (m_keymapOverridden) {'
chk $F/Hyprland-IKeyboard.cpp 'm_currentRules          = rules;'
chk $F/Hyprland-IKeyboard.cpp 'if (!m_xkbFilePath.empty()) {'
chk $F/Hyprland-IKeyboard.cpp 'm_currentRules.layout  = "us";'
chk $F/Hyprland-InputManager.cpp 'applyConfigToKeyboard(keeb);'
chk $F/Hyprland-InputManager.cpp 'pKeyboard->setKeymap(IKeyboard::SStringRuleNames{LAYOUT, MODEL, VARIANT, OPTIONS, RULES});'
chk $F/Hyprland-InputManager.cpp 'Not applying config to keyboard, it did not change.'
chk $F/Hyprland-InputManager.cpp 'if (Config::mgr()->deviceConfigExplicitlySet(devname, "scroll_factor"))'
chk $F/Hyprland-InputManager.cpp '0.F, 100.F'
chk $F/Hyprland-InputManager.cpp 'pKeyboard->m_enabled           = ENABLED;'
chk $F/Hyprland-HyprCtl.cpp 'for (auto const& k : g_pInputManager->m_keyboards) {'
chk $F/Hyprland-HyprCtl.cpp '"scrollFactor": {:.2f}'
chk $F/Hyprland-HyprCtl.cpp 'm->m_scrollFactor.value_or(-1)'
chk $F/Hyprland-ConfigManager.cpp 'if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())'
chk $F/Hyprland-ConfigManager.cpp 'm_config->addSpecialConfigValue("device", "kb_layout", {"us"});'
chk $F/Hyprland-ConfigManager.cpp 'm_config->addSpecialConfigValue("device", "scroll_factor", Hyprlang::FLOAT{-1});'
chk $F/Hyprland-ConfigManager.cpp 'g_pInputManager->setKeyboardLayout();'
chk $F/Hyprland-MiscFunctions.cpp "case ',': return '-';"
chk $F/Hyprland-VirtualKeyboard.cpp 'm_keymapOverridden = true;'
chk $F/Hyprland-protocols-VirtualKeyboard.cpp 'std::string name = "hl-virtual-keyboard";'
chk $F/hyprlang-config.cpp 'if (!COMMENT.starts_with("hyprlang"))'
chk $F/hyprlang-config.cpp "special category's first value must be the key"
chk $F/hyprlang-config.cpp 'VALUEIT->second.m_bSetByUser = true;'
chk $F/hyprlang-config.cpp 'impl->categories.clear();'
chk $F/hyprlang-config.cpp 'if (!impl->currentFlags.ifDatas.empty() && impl->currentFlags.ifDatas.back().failed)'
chk $F/hyprlang-config.cpp 'impl->currentSpecialCategory = nullptr;'
chk $F/hyprlang-config.cpp 'const auto COMMENT = trim(comment);'
chk $F/hyprlang-config.cpp 'impl->currentSpecialKey = value;'
chk $H '#define STRVAL_EMPTY "[[EMPTY]]"'
