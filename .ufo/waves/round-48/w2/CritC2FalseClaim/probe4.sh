#!/bin/bash
ulimit -f 2048
S=/fast/scratch/hyaku/mado-r48/CritC2FalseClaim
X=/usr/bin/xkbcli
export TMPDIR=$S/tmp XDG_CACHE_HOME=$S/cache
unset XKB_DEFAULT_RULES XKB_DEFAULT_MODEL XKB_DEFAULT_LAYOUT XKB_DEFAULT_VARIANT XKB_DEFAULT_OPTIONS
unset XKB_CONFIG_EXTRA_PATH XKB_CONFIG_ROOT XKB_CONFIG_VERSIONED_EXTENSIONS_PATH XKB_CONFIG_UNVERSIONED_EXTENSIONS_PATH
mkdir -p "$S/tmp" "$S/home" "$S/xdg"

echo "== T1: 3 variants for 2 layouts (truncation class)"
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg $X compile-keymap --kccgst --layout br,us --variant nodeadkeys,intl,dvorak >"$S/tmp/t1.out" 2>"$S/tmp/t1.err"; echo "rc=$?"
grep -o 'xkb_symbols { include "[^"]*" }' "$S/tmp/t1.out"; cat "$S/tmp/t1.err"
echo
echo "== T2: 5 layouts (beyond XKB_MAX_GROUPS=4)"
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg $X compile-keymap --kccgst --layout br,us,de,fr,gb >"$S/tmp/t2.out" 2>"$S/tmp/t2.err"; echo "rc=$?"
grep -o 'xkb_symbols { include "[^"]*" }' "$S/tmp/t2.out"; cat "$S/tmp/t2.err"
echo
echo "== T3: 4 layouts, 1 variant"
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg $X compile-keymap --kccgst --layout br,us,de,fr --variant nodeadkeys >"$S/tmp/t3.out" 2>"$S/tmp/t3.err"; echo "rc=$?"
grep -o 'xkb_symbols { include "[^"]*" }' "$S/tmp/t3.out"; cat "$S/tmp/t3.err"
echo
echo "== T4: --options '' with XKB_DEFAULT_OPTIONS set (+--enable-environment-names)"
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg XKB_DEFAULT_OPTIONS=nope:nope $X compile-keymap --kccgst --enable-environment-names --layout br --options '' >"$S/tmp/t4.out" 2>"$S/tmp/t4.err"; echo "rc=$?"
grep -o 'xkb_symbols { include "[^"]*" }' "$S/tmp/t4.out"; cat "$S/tmp/t4.err"
echo
echo "== T5: same but --options omitted (default should be used)"
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg XKB_DEFAULT_OPTIONS=nope:nope $X compile-keymap --kccgst --enable-environment-names --layout br >"$S/tmp/t5.out" 2>"$S/tmp/t5.err"; echo "rc=$?"
grep -o 'xkb_symbols { include "[^"]*" }' "$S/tmp/t5.out"; cat "$S/tmp/t5.err"
echo
echo "== T6: layouts with an empty entry in the middle"
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg $X compile-keymap --kccgst --layout 'br,,us' --variant nodeadkeys >"$S/tmp/t6.out" 2>"$S/tmp/t6.err"; echo "rc=$?"
grep -o 'xkb_symbols { include "[^"]*" }' "$S/tmp/t6.out"; cat "$S/tmp/t6.err"
echo
echo "== T7: .pre/.post read from EVERY include path (XDG post + extra post)"
mkdir -p "$S/xdg/xkb/rules" "$S/extra/rules"
printf '\n! option = symbols\n  mado:aaa = +compose(caps)\n' > "$S/xdg/xkb/rules/evdev.post"
printf '\n! option = symbols\n  mado:bbb = +compose(rwin)\n' > "$S/extra/rules/evdev.post"
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg XKB_CONFIG_EXTRA_PATH=$S/extra $X compile-keymap --kccgst --options mado:aaa,mado:bbb --layout br >"$S/tmp/t7.out" 2>"$S/tmp/t7.err"; echo "rc=$?"
grep -o 'xkb_symbols { include "[^"]*" }' "$S/tmp/t7.out"; cat "$S/tmp/t7.err"
echo
echo "== T8: same, but post files at BOTH paths with the SAME option name (order/path check)"
printf '\n! option = symbols\n  mado:dup = +compose(caps)\n' > "$S/xdg/xkb/rules/evdev.post"
printf '\n! option = symbols\n  mado:dup = +compose(rwin)\n' > "$S/extra/rules/evdev.post"
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg XKB_CONFIG_EXTRA_PATH=$S/extra $X compile-keymap --kccgst --options mado:dup --layout br >"$S/tmp/t8.out" 2>"$S/tmp/t8.err"; echo "rc=$?"
grep -o 'xkb_symbols { include "[^"]*" }' "$S/tmp/t8.out"; cat "$S/tmp/t8.err"
rm -f "$S/xdg/xkb/rules/evdev.post" "$S/extra/rules/evdev.post"; rmdir "$S/xdg/xkb/rules" "$S/extra/rules" 2>/dev/null
echo
echo "== T9: rules alias identity - base vs xorg byte compare"
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg $X compile-keymap --kccgst --rules base --layout br 2>/dev/null >"$S/tmp/base.k"; env HOME=$S/home XDG_CONFIG_HOME=$S/xdg $X compile-keymap --kccgst --rules xorg --layout br 2>/dev/null >"$S/tmp/xorg.k"
cmp -s "$S/tmp/base.k" "$S/tmp/xorg.k" && echo "identical=yes" || echo "identical=no"
stat -c '%F %n' /usr/share/xkeyboard-config-2/rules/xorg /usr/share/xkeyboard-config-2/rules/base
echo
echo "== T10: --rules xfree98 report (file exists, maps nothing) and README size"
cat /usr/share/xkeyboard-config-2/rules/xfree98 | sed -n '1,12p'
echo
echo "== largest"
find "$S" -maxdepth 2 -type f -printf '%s %p\n' | sort -nr | head -3
