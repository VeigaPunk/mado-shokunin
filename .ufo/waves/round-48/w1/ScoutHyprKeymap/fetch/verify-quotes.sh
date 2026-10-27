#!/bin/sh
# each line: file<TAB>quote ; asserts fixed-string presence and prints computed line
cd "$(dirname "$0")" || exit 1
while IFS='	' read -r f q; do l=$(grep -n -F -- "$q" "$f" | head -1 | cut -d: -f1); [ -n "$l" ] && echo "OK $f:$l" || { echo "MISSING $f :: $q"; rc=1; }; done <<'Q'
Hyprland-IKeyboard.cpp	const auto CONTEXT = xkb_context_new(XKB_CONTEXT_NO_FLAGS);
Hyprland-IKeyboard.cpp	m_xkbKeymap = xkb_keymap_new_from_names2(CONTEXT, &XKBRULES, XKB_KEYMAP_FORMAT_TEXT_V2, XKB_KEYMAP_COMPILE_NO_FLAGS);
Hyprland-IKeyboard.cpp	memset(&XKBRULES, 0, sizeof(XKBRULES));
Hyprland-IKeyboard.cpp	updateXKBTranslationState: keymap failed 2, fallback to us
Hyprland-KeybindManager.cpp	const auto        PCONTEXT   = xkb_context_new(XKB_CONTEXT_NO_FLAGS);
Hyprland-InputManager.cpp	pKeyboard->setKeymap(IKeyboard::SStringRuleNames{LAYOUT, MODEL, VARIANT, OPTIONS, RULES});
Hyprland-ConfigManager.cpp	setenv(ARGS[0].c_str(), ARGS[1].c_str(), 1);
xkbcommon-context.c	ctx->use_environment_names = !(flags & XKB_CONTEXT_NO_ENVIRONMENT_NAMES);
xkbcommon-context.c	ctx->pending_default_includes = !(flags & XKB_CONTEXT_NO_DEFAULT_INCLUDES);
xkbcommon-context.c	user_path = asprintf_safe("%s/.config/xkb", home);
xkbcommon-context.c	user_path = asprintf_safe("%s/.xkb", home);
xkbcommon-context.c	/* XDG_CONFIG_HOME fallback is $HOME/.config/ */
xkbcommon-context-priv.c	return secure_getenv(name);
xkbcommon-context-priv.c	if (rmlvo->options == NULL) {
xkbcommon-xkbcomp.c	"Couldn't look up rules '%s', model '%s', layout '%s', "
xkbcommon-keymap.c	xkb_context_sanitize_rule_names(ctx, &rmlvo);
xkbcommon-xkbcommon.h	Don’t take RMLVO names from the environment.
Q
exit ${rc:-0}
