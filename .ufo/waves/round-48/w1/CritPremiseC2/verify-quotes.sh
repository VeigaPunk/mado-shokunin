#!/bin/bash
# Verifies every quoted locator used in findings.md against its receipt/pin.
# rc 0 = all quotes found. Run from anywhere; paths are absolute.
set -u
D=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w1/CritPremiseC2
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
fail=0
check() { # check <file> <quote> <locator>
  if grep -qF -- "$2" "$1"; then
    printf 'OK   %s\n' "$3"
  else
    printf 'MISS %s\n' "$3"; fail=1
  fi
}
check "$LANE/.ufo/waves/round-46/fetch/Hyprland-IKeyboard.cpp" \
  "xkb_keymap_new_from_names2(CONTEXT, &XKBRULES, XKB_KEYMAP_FORMAT_TEXT_V2, XKB_KEYMAP_COMPILE_NO_FLAGS)" \
  "Hyprland-IKeyboard.cpp:99"
check "$LANE/.ufo/waves/round-46/fetch/Hyprland-IKeyboard.cpp" \
  "xkb_context_new(XKB_CONTEXT_NO_FLAGS)" \
  "Hyprland-IKeyboard.cpp:75"
check "$LANE/.ufo/waves/round-46/fetch/Hyprland-ConfigValues.cpp" \
  'MS<String>("input:kb_layout", "Appropriate XKB keymap parameter", "us",' \
  "Hyprland-ConfigValues.cpp:272"
check "$D/pins/libxkbcommon-context-priv.c" \
  "if (rmlvo->options == NULL) {" \
  "context-priv.c:219"
check "$D/pins/libxkbcommon-context-priv.c" \
  'XKB_DEFAULT_LAYOUT' \
  "context-priv.c:156"
check "$D/pins/libxkbcommon-rules.c" \
  'Unrecognized RMLVO option \"%.*s\" was ignored' \
  "rules.c:2063"
check "$D/pins/libxkbcommon-rules.c" \
  'Unrecognized RMLVO model \"%.*s\" was ignored' \
  "rules.c:2048"
check "$D/pins/libxkbcommon-keymap-formats.h" \
  '#define DEFAULT_INPUT_KEYMAP_FORMAT  XKB_KEYMAP_FORMAT_TEXT_V2' \
  "keymap-formats.h:13"
check "$D/pins/libxkbcommon-compile-keymap.c" \
  "enum xkb_context_flags ctx_flags = XKB_CONTEXT_NO_DEFAULT_INCLUDES;" \
  "compile-keymap.c:585"
check "$D/pins/libxkbcommon-compile-keymap.c" \
  "ctx_flags |= XKB_CONTEXT_NO_ENVIRONMENT_NAMES;" \
  "compile-keymap.c:587"
check "$D/pins/libxkbcommon-compile-keymap.c" \
  "return xkb_keymap_new_from_names2(ctx, rmlvo, keymap_input_format," \
  "compile-keymap.c:503"
check "$D/pins/libxkbcommon-context.c" \
  "xkb_context_include_path_append_default(struct xkb_context *ctx)" \
  "context.c:243"
check "$D/pins/libxkbcommon-meson_options.txt" \
  "value: 'evdev'" \
  "meson_options.txt default-rules"
check "$D/pins/libxkbcommon-meson_options.txt" \
  "value: 'pc105'" \
  "meson_options.txt default-model"
check "$D/pins/libxkbcommon-meson_options.txt" \
  "value: 'us'" \
  "meson_options.txt default-layout"
check "$LANE/corpus/README.md" \
  "Still open: the XKB compile itself" \
  "corpus/README.md:112"
check "$LANE/corpus/knowledge/hyprland-input-devices-r46.md" \
  "The XKB compile itself is not reproduced" \
  "hyprland-input-devices-r46.md:69"
check "$D/receipts-xkbcli-empirical.txt" \
  'rules: "evdev"' \
  "receipt R1"
check "$D/receipts-xkbcli-empirical.txt" \
  'layout: "br"' \
  "receipt R3"
check "$D/receipts-xkbcli-empirical.txt" \
  'symbols/zz' \
  "receipt R6"
check "$D/receipts-xkbcli-empirical.txt" \
  'xyzzy:1:1: syntax error' \
  "receipt R7"
check "$D/receipts-xkbcli-empirical.txt" \
  '/usr/share/xkeyboard-config-2' \
  "receipt R6 root"
check "$D/receipts-xkbcli-empirical.txt" \
  '/usr/share/X11/xkb -> /usr/share/xkeyboard-config-2' \
  "receipt R0 symlink"
exit $fail
