#!/bin/bash
ulimit -f 2048
S=/fast/scratch/hyaku/mado-r48/CritC2FalseClaim
X=/usr/bin/xkbcli
export TMPDIR=$S/tmp
unset XKB_DEFAULT_RULES XKB_DEFAULT_MODEL XKB_DEFAULT_LAYOUT XKB_DEFAULT_VARIANT XKB_DEFAULT_OPTIONS
unset XKB_CONFIG_EXTRA_PATH XKB_CONFIG_ROOT XKB_CONFIG_VERSIONED_EXTENSIONS_PATH XKB_CONFIG_UNVERSIONED_EXTENSIONS_PATH
export XDG_CACHE_HOME=$S/cache
mkdir -p "$S/tmp" "$S/cache"

mkprobe() { mkdir -p "$1/symbols"; cat >"$1/symbols/mado48" <<EOF
default partial alphanumeric_keys
xkb_symbols "basic" {
    name[Group1]= "$2";
    key <AE01> { [ 1 ] };
};
EOF
}

# extension-dir fixtures: add_direct_subdirectories -> <extpath>/<subdir>/symbols/mado48
mkprobe "$S/extv/subv" "MADO48-EXT-VERSIONED"
mkprobe "$S/extu/subu" "MADO48-EXT-UNVERSIONED"
mkprobe "$S/extra" "MADO48-EXTRA"
mkprobe "$S/h6/.xkb" "MADO48-DOTXKB-H6"

echo "== K1: HOME/.xkb vs XKB_CONFIG_EXTRA_PATH (claimed order: HOME/.xkb first)"
env -u XDG_CONFIG_HOME HOME=$S/h6 XKB_CONFIG_EXTRA_PATH=$S/extra $X compile-keymap --layout mado48 2>"$S/tmp/k1.err" | grep -o 'MADO48-[A-Z0-9-]*' | sort -u
echo "rc=${PIPESTATUS[0]}"; sed -n '1,6p' "$S/tmp/k1.err"
echo
echo "== K2: extra path vs versioned extensions dir (claimed order: extra first)"
env -u XDG_CONFIG_HOME HOME=$S/h6 XKB_CONFIG_EXTRA_PATH=$S/extra XKB_CONFIG_VERSIONED_EXTENSIONS_PATH=$S/extv XKB_CONFIG_UNVERSIONED_EXTENSIONS_PATH=$S/extu $X compile-keymap --layout mado48 2>"$S/tmp/k2.err" | grep -o 'MADO48-[A-Z0-9-]*' | sort -u
echo "rc=${PIPESTATUS[0]}"; sed -n '1,8p' "$S/tmp/k2.err"
echo
echo "== K3: versioned vs unversioned extensions dir (claimed order: versioned first)"
env -u XDG_CONFIG_HOME HOME=$S/h6 -u XKB_CONFIG_EXTRA_PATH XKB_CONFIG_VERSIONED_EXTENSIONS_PATH=$S/extv XKB_CONFIG_UNVERSIONED_EXTENSIONS_PATH=$S/extu $X compile-keymap --layout mado48 2>"$S/tmp/k3.err" | grep -o 'MADO48-[A-Z0-9-]*' | sort -u
echo "rc=${PIPESTATUS[0]}"; sed -n '1,8p' "$S/tmp/k3.err"
echo
echo "== K4: verbose path order with extensions set"
env -u XDG_CONFIG_HOME HOME=$S/h6 XKB_CONFIG_EXTRA_PATH=$S/extra XKB_CONFIG_VERSIONED_EXTENSIONS_PATH=$S/extv XKB_CONFIG_UNVERSIONED_EXTENSIONS_PATH=$S/extu XKB_LOG_LEVEL=debug $X compile-keymap --test --layout mado48 2>&1 | grep -E "Include path added|Include extensions" | sed -n '1,12p'
echo
echo "== N-fixed: user rules file at the real include path wins (empty rules/evdev shadow)"
mkdir -p "$S/xdg/xkb/rules"
: > "$S/xdg/xkb/rules/evdev"
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg $X compile-keymap --test --layout br >"$S/tmp/nf.out" 2>"$S/tmp/nf.err"; echo "rc=$?"
sed -n '1,12p' "$S/tmp/nf.err"
rm -f "$S/xdg/xkb/rules/evdev"
echo
echo "== N2-fixed: user rules/custom used when --rules custom"
cp /usr/share/xkeyboard-config-2/rules/evdev "$S/xdg/xkb/rules/custom"
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg $X compile-keymap --kccgst --rules custom --layout br >"$S/tmp/n2f.out" 2>"$S/tmp/n2f.err"; echo "rc=$?"
grep -o 'include "[^"]*"' "$S/tmp/n2f.out"; sed -n '1,4p' "$S/tmp/n2f.err"
echo
echo "== N3: rules/custom.post is read (option section added by post file)"
cat > "$S/xdg/xkb/rules/custom.post" <<'EOF'
! option = symbols
  mado:post = +mado48
EOF
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg $X compile-keymap --kccgst --rules custom --options mado:post --layout br >"$S/tmp/n3.out" 2>"$S/tmp/n3.err"; echo "rc=$?"
grep -o 'xkb_symbols { include "[^"]*" }' "$S/tmp/n3.out"; sed -n '1,4p' "$S/tmp/n3.err"
echo
echo "== N4: same with custom.pre instead of custom.post (pre is read before the main file)"
rm -f "$S/xdg/xkb/rules/custom.post"
cp "$S/xdg/xkb/rules/custom" "$S/xdg/xkb/rules/custom.pre"
cat >> "$S/xdg/xkb/rules/custom.pre" <<'EOF'

! option = symbols
  mado:pre = +mado48
EOF
env HOME=$S/home XDG_CONFIG_HOME=$S/xdg $X compile-keymap --kccgst --rules custom --options mado:pre --layout br >"$S/tmp/n4.out" 2>"$S/tmp/n4.err"; echo "rc=$?"
grep -o 'xkb_symbols { include "[^"]*" }' "$S/tmp/n4.out"; sed -n '1,4p' "$S/tmp/n4.err"
rm -f "$S/xdg/xkb/rules/custom.pre" "$S/xdg/xkb/rules/custom"
echo
echo "== R1: real host env (no scratch HOME) - positive digest and stderr"
env -u XDG_CONFIG_HOME HOME=/home/vgpnk $X compile-keymap --layout br --options compose:caps >"$S/tmp/r1.keymap" 2>"$S/tmp/r1.err"; echo "rc=$?"
sha256sum "$S/tmp/r1.keymap"; wc -c <"$S/tmp/r1.err"
echo
echo "== R2: real host env, unknown layout stderr census (host paths)"
env -u XDG_CONFIG_HOME HOME=/home/vgpnk $X compile-keymap --test --layout zz 2>&1 | sed -n '1,8p'
echo
echo "== R3: real host env, unknown model at drill level, with --test (RMLVO debug line)"
env -u XDG_CONFIG_HOME HOME=/home/vgpnk XKB_LOG_LEVEL=debug $X compile-keymap --test --layout br --model nope 2>&1 | grep -E "RMLVO|model|WARNING|ERROR" | sed -n '1,8p'
echo
echo "== largest files"
find "$S" -maxdepth 2 -type f -printf '%s %p\n' 2>/dev/null | sort -nr | head -3
