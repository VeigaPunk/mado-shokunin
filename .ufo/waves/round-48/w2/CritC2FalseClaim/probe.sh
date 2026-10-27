#!/bin/bash
# CritC2FalseClaim - read-only xkbcli classification probes. No writes outside $S.
ulimit -f 2048
S=/fast/scratch/hyaku/mado-r48/CritC2FalseClaim
X=/usr/bin/xkbcli
export TMPDIR=$S/tmp
mkdir -p "$TMPDIR"
unset XKB_DEFAULT_RULES XKB_DEFAULT_MODEL XKB_DEFAULT_LAYOUT XKB_DEFAULT_VARIANT XKB_DEFAULT_OPTIONS
unset XKB_CONFIG_EXTRA_PATH XKB_CONFIG_ROOT XKB_CONFIG_VERSIONED_EXTENSIONS_PATH XKB_CONFIG_UNVERSIONED_EXTENSIONS_PATH

run() {  # run <label> <env...> -- <args...>
    local label=$1; shift
    echo "### $label"
    echo "\$ env $* | $X"
    local out err rc
    out=$(mktemp -p "$S/tmp"; ) 2>/dev/null
    # simpler: capture via temp files
    local o=$S/tmp/o.txt e=$S/tmp/e.txt
    env "$@" >"$o" 2>"$e"; rc=$?
    echo "--- rc=$rc"
    echo "--- stdout bytes=$(wc -c <"$o") lines=$(wc -l <"$o")"
    sed -n '1,12p' "$o"
    echo "--- stderr"
    cat "$e"
    echo
}

echo "== versions"
$X --version; echo "rc=$?"
echo
echo "== package db (read-only)"
ls -d /var/lib/pacman/local/libxkbcommon-[0-9]* /var/lib/pacman/local/xkeyboard-config-[0-9]* 2>&1
echo
echo "== root symlink"
readlink -f /usr/share/X11/xkb
echo
echo "== user include paths present on host (boolean only)"
for p in "$HOME/.config/xkb" "$HOME/.xkb" /etc/xkb /usr/share/xkeyboard-config-2.d /usr/share/xkeyboard-config.d; do
  if [ -d "$p" ]; then echo "dir-present"; else echo "dir-absent"; fi
done
echo

# isolated env for every probe
export HOME=$S/home
export XDG_CONFIG_HOME=$S/xdg
export XDG_CACHE_HOME=$S/cache
mkdir -p "$HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"
echo "== positive replay (clause r shape)"
$X compile-keymap --layout br --options compose:caps >"$S/tmp/positive.keymap" 2>"$S/tmp/positive.err"; echo "rc=$?"
sha256sum "$S/tmp/positive.keymap"; wc -lc "$S/tmp/positive.keymap"; wc -c <"$S/tmp/positive.err"
echo

echo "== unknown layout"
$X compile-keymap --test --layout zz >"$S/tmp/lo.out" 2>"$S/tmp/lo.err"; echo "rc=$?"
echo "-- stdout:"; cat "$S/tmp/lo.out"; echo "-- stderr:"; cat "$S/tmp/lo.err"
echo
echo "== unknown variant nope"
$X compile-keymap --test --layout br --variant nope >"$S/tmp/vn.out" 2>"$S/tmp/vn.err"; echo "rc=$?"
echo "-- stderr:"; cat "$S/tmp/vn.err"
echo
echo "== variant caps (not a br map)"
$X compile-keymap --test --layout br --variant caps >"$S/tmp/vc.out" 2>"$S/tmp/vc.err"; echo "rc=$?"
echo "-- stderr:"; cat "$S/tmp/vc.err"
echo
echo "== unknown rules nope"
$X compile-keymap --test --rules nope --layout br >"$S/tmp/rn.out" 2>"$S/tmp/rn.err"; echo "rc=$?"
echo "-- stderr:"; cat "$S/tmp/rn.err"
echo
echo "== rules xfree98"
$X compile-keymap --test --rules xfree98 --layout br >"$S/tmp/rx.out" 2>"$S/tmp/rx.err"; echo "rc=$?"
echo "-- stderr:"; cat "$S/tmp/rx.err"
echo
echo "== rules base kccgst"
$X compile-keymap --kccgst --rules base --layout br; echo "rc=$?"
echo
echo "== rules xorg kccgst"
$X compile-keymap --kccgst --rules xorg --layout br; echo "rc=$?"
echo
echo "== unknown option, default log level (no XKB_LOG_LEVEL)"
$X compile-keymap --test --layout br --options nope:nope >"$S/tmp/on.out" 2>"$S/tmp/on.err"; echo "rc=$?"
echo "-- stderr:"; cat "$S/tmp/on.err"
echo
echo "== unknown model, default level"
$X compile-keymap --kccgst --layout br --model nope >"$S/tmp/m0.out" 2>"$S/tmp/m0.err"; echo "rc=$?"
cat "$S/tmp/m0.out"; echo "-- stderr bytes=$(wc -c <"$S/tmp/m0.err")"
echo
echo "== unknown model, XKB_LOG_LEVEL=warn"
XKB_LOG_LEVEL=warn $X compile-keymap --kccgst --layout br --model nope >"$S/tmp/m1.out" 2>"$S/tmp/m1.err"; echo "rc=$?"
cat "$S/tmp/m1.out"; echo "-- stderr:"; cat "$S/tmp/m1.err"
echo
echo "== unknown model, XKB_LOG_LEVEL=debug (entry says 'silent at every level')"
XKB_LOG_LEVEL=debug $X compile-keymap --kccgst --layout br --model nope >"$S/tmp/m2.out" 2>"$S/tmp/m2.err"; echo "rc=$?"
cat "$S/tmp/m2.out"; echo "-- stderr:"; cat "$S/tmp/m2.err"
echo
echo "== no names (defaults)"
$X compile-keymap --kccgst; echo "rc=$?"
echo
echo "== empty layout + variant intl, default level"
$X compile-keymap --kccgst --layout '' --variant intl 2>"$S/tmp/el.err"; echo "rc=$?"
echo "-- stderr bytes=$(wc -c <"$S/tmp/el.err")"; cat "$S/tmp/el.err"
echo
echo "== empty layout + variant intl, warn level"
XKB_LOG_LEVEL=warn $X compile-keymap --kccgst --layout '' --variant intl 2>&1 | sed -n '1,10p'
echo
echo "== two layouts one variant, kccgst"
$X compile-keymap --kccgst --layout br,us --variant nodeadkeys 2>"$S/tmp/tl.err"; echo "rc=$?"
echo "-- stderr bytes=$(wc -c <"$S/tmp/tl.err")"; cat "$S/tmp/tl.err"
echo
echo "== two layouts one variant, warn"
XKB_LOG_LEVEL=warn $X compile-keymap --test --layout br,us --variant nodeadkeys 2>&1 | sed -n '1,10p'; echo "rc=${PIPESTATUS[0]}"
echo
echo "== one layout two variants, default level"
$X compile-keymap --kccgst --layout br --variant nodeadkeys,intl 2>"$S/tmp/ov.err"; echo "rc=$?"
echo "-- stderr:"; cat "$S/tmp/ov.err"
echo
echo "== one layout two variants, warn"
XKB_LOG_LEVEL=warn $X compile-keymap --test --layout br --variant nodeadkeys,intl 2>&1 | sed -n '1,10p'
echo
echo "== two layouts two variants (empty first), kccgst"
$X compile-keymap --kccgst --layout br,us --variant ,dvorak 2>"$S/tmp/tv.err"; echo "rc=$?"
echo "-- stderr:"; cat "$S/tmp/tv.err"
echo
echo "== multi-layout misalignment: 3 layouts 2 variants"
$X compile-keymap --kccgst --layout br,us,de --variant nodeadkeys,dvorak 2>"$S/tmp/t3.err"; echo "rc=$?"
echo "-- stderr:"; cat "$S/tmp/t3.err"
echo
echo "== variant on second layout only, first layout known"
$X compile-keymap --kccgst --layout br,us --variant ,nope 2>"$S/tmp/t4.err"; echo "rc=$?"
echo "-- stderr:"; cat "$S/tmp/t4.err"
echo

# ---- include path probes ----
mkprobe() {  # mkprobe <dir> <name>
    mkdir -p "$1/symbols"
    cat >"$1/symbols/mado48" <<EOF
default partial alphanumeric_keys
xkb_symbols "basic" {
    name[Group1]= "$2";
    key <AE01> { [ 1 ] };
};
EOF
}
mkprobe "$S/xdg/xkb" "MADO48-XDG"
mkprobe "$S/h2/.config/xkb" "MADO48-HOMECONFIG"
mkprobe "$S/h3/.xkb" "MADO48-DOTXKB"
mkprobe "$S/h4/.xkb" "MADO48-DOTXKB-H4"
mkprobe "$S/extra" "MADO48-EXTRA"
mkdir -p "$S/emptyroot"

echo "== include probe A: XDG_CONFIG_HOME/xkb"
env -u XKB_CONFIG_EXTRA_PATH HOME=$S/h2 XDG_CONFIG_HOME=$S/xdg $X compile-keymap --layout mado48 >"$S/tmp/ia.out" 2>"$S/tmp/ia.err"; echo "rc=$?"
grep -o 'MADO48-[A-Z0-9-]*' "$S/tmp/ia.out" | sort -u; sed -n '1,4p' "$S/tmp/ia.err"
echo
echo "== include probe B: XDG unset, HOME/.config/xkb fallback"
env -u XDG_CONFIG_HOME -u XKB_CONFIG_EXTRA_PATH HOME=$S/h2 $X compile-keymap --layout mado48 >"$S/tmp/ib.out" 2>"$S/tmp/ib.err"; echo "rc=$?"
grep -o 'MADO48-[A-Z0-9-]*' "$S/tmp/ib.out" | sort -u; sed -n '1,8p' "$S/tmp/ib.err"
echo
echo "== include probe B2: XDG set to a nonexistent dir, HOME/.config/xkb present (fallback must NOT apply)"
env HOME=$S/h2 XDG_CONFIG_HOME=$S/xdg-does-not-exist $X compile-keymap --layout mado48 >"$S/tmp/ib2.out" 2>"$S/tmp/ib2.err"; echo "rc=$?"
grep -o 'MADO48-[A-Z0-9-]*' "$S/tmp/ib2.out" | sort -u; sed -n '1,8p' "$S/tmp/ib2.err"
echo
echo "== include probe C: HOME/.xkb"
env -u XDG_CONFIG_HOME -u XKB_CONFIG_EXTRA_PATH HOME=$S/h3 $X compile-keymap --layout mado48 >"$S/tmp/ic.out" 2>"$S/tmp/ic.err"; echo "rc=$?"
grep -o 'MADO48-[A-Z0-9-]*' "$S/tmp/ic.out" | sort -u; sed -n '1,4p' "$S/tmp/ic.err"
echo
echo "== include probe D: precedence XDG vs HOME/.xkb"
env -u XKB_CONFIG_EXTRA_PATH HOME=$S/h4 XDG_CONFIG_HOME=$S/xdg $X compile-keymap --layout mado48 >"$S/tmp/id.out" 2>"$S/tmp/id.err"; echo "rc=$?"
grep -o 'MADO48-[A-Z0-9-]*' "$S/tmp/id.out" | sort -u
echo
echo "== include probe E: XKB_CONFIG_EXTRA_PATH"
env -u XDG_CONFIG_HOME HOME=$S/h5 XKB_CONFIG_EXTRA_PATH=$S/extra $X compile-keymap --layout mado48 >"$S/tmp/ie.out" 2>"$S/tmp/ie.err"; echo "rc=$?"
grep -o 'MADO48-[A-Z0-9-]*' "$S/tmp/ie.out" | sort -u; sed -n '1,8p' "$S/tmp/ie.err"
echo
echo "== include probe F: HOME=/nonexistent-home, XDG unset"
env -u XDG_CONFIG_HOME HOME=/nonexistent-home $X compile-keymap --layout mado48 >"$S/tmp/if.out" 2>"$S/tmp/if.err"; echo "rc=$?"
grep -o 'MADO48-[A-Z0-9-]*' "$S/tmp/if.out" | sort -u; sed -n '1,12p' "$S/tmp/if.err"
echo
echo "== include probe G: XKB_CONFIG_ROOT overridden to an empty dir"
env XKB_CONFIG_ROOT=$S/emptyroot XKB_LOG_LEVEL=warn $X compile-keymap --test --layout br >"$S/tmp/ig.out" 2>"$S/tmp/ig.err"; echo "rc=$?"
sed -n '1,14p' "$S/tmp/ig.err"
echo
echo "== include probe H: verbose include path order under the isolated env"
env XKB_LOG_LEVEL=info $X compile-keymap --test --layout mado48 2>&1 | grep -E "Include path|Include extensions" | sed -n '1,10p'
echo
echo "== host config file digests (read-only)"
sha256sum "$HOME" 2>/dev/null >/dev/null
sha256sum /home/vgpnk/.config/hypr/input.conf /home/vgpnk/.local/share/omarchy/default/hypr/input.conf 2>&1
echo
echo "== largest files written"
find "$S" -maxdepth 2 -type f -printf '%s %p\n' 2>/dev/null | sort -nr | head -5
