#!/bin/bash
ulimit -f 2048
S=/fast/scratch/hyaku/mado-r48/CritC2FalseClaim
X=/usr/bin/xkbcli
export TMPDIR=$S/tmp
unset XKB_DEFAULT_RULES XKB_DEFAULT_MODEL XKB_DEFAULT_LAYOUT XKB_DEFAULT_VARIANT XKB_DEFAULT_OPTIONS
unset XKB_CONFIG_EXTRA_PATH XKB_CONFIG_ROOT XKB_CONFIG_VERSIONED_EXTENSIONS_PATH XKB_CONFIG_UNVERSIONED_EXTENSIONS_PATH
export HOME=$S/home XDG_CONFIG_HOME=$S/xdg XDG_CACHE_HOME=$S/cache
mkdir -p "$HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" "$S/tmp"

echo "== J: two layouts, no variant (does %l expand with several?)"
$X compile-keymap --kccgst --layout br,us 2>"$S/tmp/j.err"; echo "rc=$?"; echo "-- stderr:"; cat "$S/tmp/j.err"
echo
echo "== J2: three layouts, no variant"
$X compile-keymap --kccgst --layout br,us,de 2>"$S/tmp/j2.err"; echo "rc=$?"; echo "-- stderr:"; cat "$S/tmp/j2.err"
echo
echo "== L: unknown layout in the second position (test/compile)"
$X compile-keymap --test --layout br,zz >"$S/tmp/l.out" 2>"$S/tmp/l.err"; echo "rc=$?"; sed -n '1,12p' "$S/tmp/l.err"
echo
echo "== M: unknown variant on second layout (test/compile, not kccgst)"
$X compile-keymap --test --layout br,us --variant ,nope >"$S/tmp/m.out" 2>"$S/tmp/m.err"; echo "rc=$?"; sed -n '1,12p' "$S/tmp/m.err"
echo
echo "== M2: known variant on second layout (test/compile)"
$X compile-keymap --test --layout br,us --variant ,dvorak >"$S/tmp/m2.out" 2>"$S/tmp/m2.err"; echo "rc=$?"; sed -n '1,8p' "$S/tmp/m2.err"
echo
echo "== B: empty rules name replaced by default"
$X compile-keymap --kccgst --rules '' --layout br 2>"$S/tmp/b.err"; echo "rc=$?"; cat "$S/tmp/b.err"
echo
echo "== B2: empty model and empty variant"
$X compile-keymap --kccgst --rules evdev --model '' --layout br --variant '' 2>"$S/tmp/b2.err"; echo "rc=$?"; cat "$S/tmp/b2.err"
echo
echo "== N: user rules file on the first include path wins (rules/evdev shadowed by an empty file)"
mkdir -p "$S/xdg/rules"
: > "$S/xdg/rules/evdev"
$X compile-keymap --test --layout br >"$S/tmp/n.out" 2>"$S/tmp/n.err"; echo "rc=$?"; sed -n '1,12p' "$S/tmp/n.err"
rm -f "$S/xdg/rules/evdev"
echo
echo "== N2: user rules named rules/custom used when --rules custom"
cp /usr/share/xkeyboard-config-2/rules/evdev "$S/xdg/rules/custom" 2>/dev/null
$X compile-keymap --kccgst --rules custom --layout br >"$S/tmp/n2.out" 2>"$S/tmp/n2.err"; echo "rc=$?"; cat "$S/tmp/n2.out"; sed -n '1,4p' "$S/tmp/n2.err"
rm -f "$S/xdg/rules/custom"
echo
echo "== G2: XKB_CONFIG_ROOT nonexistent -> legacy-root fallback (warn level)"
env XKB_CONFIG_ROOT=/nonexistent-root XKB_LOG_LEVEL=warn $X compile-keymap --test --layout br >"$S/tmp/g2.out" 2>"$S/tmp/g2.err"; echo "rc=$?"; sed -n '1,14p' "$S/tmp/g2.err"
echo
echo "== G3: XKB_CONFIG_ROOT empty string -> no fallback"
env XKB_CONFIG_ROOT= XKB_LOG_LEVEL=warn $X compile-keymap --test --layout br >"$S/tmp/g3.out" 2>"$S/tmp/g3.err"; echo "rc=$?"; sed -n '1,14p' "$S/tmp/g3.err"
echo
echo "== G4: XKB_CONFIG_ROOT nonexistent at default level (fallback warning hidden?)"
env XKB_CONFIG_ROOT=/nonexistent-root $X compile-keymap --test --layout br >"$S/tmp/g4.out" 2>"$S/tmp/g4.err"; echo "rc=$?"; echo "-- stderr bytes=$(wc -c <"$S/tmp/g4.err")"; sed -n '1,14p' "$S/tmp/g4.err"
echo
echo "== I: unknown model at debug, full stderr"
env XKB_LOG_LEVEL=debug $X compile-keymap --kccgst --layout br --model nope >"$S/tmp/i.out" 2>"$S/tmp/i.err"; echo "rc=$?"; echo "-- stderr lines=$(wc -l <"$S/tmp/i.err")"; cat "$S/tmp/i.err"
echo
echo "== Q: XKB_DEFAULT_* ignored by xkbcli (S348 claim)"
env XKB_DEFAULT_LAYOUT=zz XKB_DEFAULT_RULES=nope XKB_DEFAULT_MODEL=nope $X compile-keymap --kccgst 2>"$S/tmp/q.err"; echo "rc=$?"; cat "$S/tmp/q.err"
echo
echo "== Q2: same with --enable-environment-names"
env XKB_DEFAULT_LAYOUT=zz $X compile-keymap --kccgst --enable-environment-names >"$S/tmp/q2.out" 2>"$S/tmp/q2.err"; echo "rc=$?"; sed -n '1,10p' "$S/tmp/q2.out"; sed -n '1,10p' "$S/tmp/q2.err"
echo
echo "== largest files"
find "$S" -maxdepth 2 -type f -printf '%s %p\n' 2>/dev/null | sort -nr | head -3
