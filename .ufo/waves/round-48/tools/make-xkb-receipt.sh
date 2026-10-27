#!/usr/bin/env bash
# mado round 48 (C2; drafted by w1 seat ScrEntry, run by the L1) - read-only receipt generator for the XKB-compile knowledge entry.
# Writes receipts/xkbcli-compile-keymap-r48.txt next to this script.
# Every xkbcli call is a compile/test/kccgst verb: no compositor, no input device, no host
# write. Probe fixtures live in a mktemp dir under the seat scratch root and are removed.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
OUT="$HERE/xkbcli-compile-keymap-r48.txt"
K=/usr/bin/xkbcli
S=${XKB_R48_SCRATCH:-/fast/scratch/hyaku/mado-r48/L1receipt}
mkdir -p "$S"
T=$(mktemp -d -p "$S" probe.XXXXXX) || exit 1
trap 'rm -rf -- "$T"' EXIT INT TERM

say() { printf '%s\n' "$*" >>"$OUT"; }
cmd() { printf '$ %s\n' "$*" >>"$OUT"; }
run() {  # run "<label>" <command...> : stdout+stderr+rc into the receipt
    local label=$1; shift
    say "--- $label"
    cmd "$@"
    local out rc
    out=$("$@" 2>&1); rc=$?
    printf '%s\n' "$out" | head -c 200000 >>"$OUT"
    say "rc=$rc"
    say ""
}

: >"$OUT"
say "# mado round 48 - read-only xkbcli compile-keymap receipt (C2), generator .ufo/waves/round-48/receipts/make-xkb-receipt.sh"
say "# taken: $(date -u +%Y-%m-%dT%H:%M:%SZ) (UTC)"
say "# host: $(uname -srm)"
say "# xkbcli: $K (no wrapper); compile/test/kccgst verbs only, stdout+stderr captured"
say ""

say "== versions, paths, defaults"
run "xkbcli version" "$K" --version
say '$ ls -d /var/lib/pacman/local/libxkbcommon-[0-9]* /var/lib/pacman/local/xkeyboard-config-[0-9]*   (package database read, no pacman run)'
ls -d /var/lib/pacman/local/libxkbcommon-[0-9]* /var/lib/pacman/local/xkeyboard-config-[0-9]* >>"$OUT" 2>&1
say "rc=$?"
say ""
run "canonical root" readlink -f /usr/share/X11/xkb
say '$ ls -ld /usr/share/X11/xkb'
ls -ld /usr/share/X11/xkb >>"$OUT" 2>&1
say '$ ls /usr/share/xkeyboard-config-2/rules/'
ls /usr/share/xkeyboard-config-2/rules/ >>"$OUT" 2>&1
say ""

say "== the host's names (read-only reads of the two input files the compositor loads)"
say '$ grep -n "kb_" ~/.config/hypr/input.conf ~/.local/share/omarchy/default/hypr/input.conf'
grep -n 'kb_' "$HOME/.config/hypr/input.conf" "$HOME/.local/share/omarchy/default/hypr/input.conf" >>"$OUT" 2>&1
say '$ sha256sum the two files'
sha256sum "$HOME/.config/hypr/input.conf" "$HOME/.local/share/omarchy/default/hypr/input.conf" >>"$OUT" 2>&1
say ""

say "== the names compile: full keymap digest (the keymap itself is ~73 KB and not kept)"
say "\$ $K compile-keymap --layout br --options compose:caps > host.keymap"
"$K" compile-keymap --layout br --options compose:caps >"$T/host.keymap" 2>"$T/host.err"
say "rc=$?"
say '$ sha256sum host.keymap'
sha256sum "$T/host.keymap" | sed "s#$T/##" >>"$OUT"
say '$ wc -lc host.keymap'
wc -l <"$T/host.keymap" | awk '{print $1" lines"}' >>"$OUT"
wc -c <"$T/host.keymap" | awk '{print $1" bytes"}' >>"$OUT"
say '$ head -3 host.keymap'
head -3 "$T/host.keymap" >>"$OUT"
say '$ cat host.keymap.stderr (empty means no diagnostic at the default log level)'
head -c 4000 "$T/host.err" >>"$OUT"
say ""

run "KcCGST for the host's names" "$K" compile-keymap --kccgst --layout br --options compose:caps
run "host names, test mode (compiles, prints nothing)" "$K" compile-keymap --test --layout br --options compose:caps
say "--- the include path list in order (verbose log, filtered to the path and KcCGST lines)"
say '$ /usr/bin/xkbcli compile-keymap --test --verbose --layout br 2>&1 | grep -E "Include path|Include extensions|Compiling from"'
"$K" compile-keymap --test --verbose --layout br 2>&1 \
    | grep -E 'Include path|Include extensions|Compiling from' >>"$OUT"
say "rc=${PIPESTATUS[0]}"
say ""
run "no names at all: the built-in defaults" "$K" compile-keymap --kccgst
run "empty layout with a variant set" env XKB_LOG_LEVEL=warn "$K" compile-keymap --kccgst --layout '' --variant intl

say "== unknown names: which hard-fail and which do not"
run "unknown layout" "$K" compile-keymap --test --layout zz
run "unknown variant on a known layout" "$K" compile-keymap --test --layout br --variant nope
run "variant the br map does not define" "$K" compile-keymap --test --layout br --variant caps
run "variant the br map defines" "$K" compile-keymap --test --layout br --variant nodeadkeys
run "unknown option" "$K" compile-keymap --test --layout br --options nope:nope
run "unknown model, KcCGST" "$K" compile-keymap --kccgst --layout br --model nope
run "unknown model at XKB_LOG_LEVEL=warn (still silent: the model wildcard matched)" env XKB_LOG_LEVEL=warn "$K" compile-keymap --kccgst --layout br --model nope
run "model pc105, KcCGST" "$K" compile-keymap --kccgst --layout br --model pc105
run "unknown rules" "$K" compile-keymap --test --rules nope --layout br

say "== rulesets that exist in the package"
run "rules base" "$K" compile-keymap --kccgst --rules base --layout br
run "rules xorg" "$K" compile-keymap --kccgst --rules xorg --layout br
run "rules xfree98 (file exists, returns no components)" "$K" compile-keymap --test --rules xfree98 --layout br

say "== multi-layout / variant alignment"
run "two layouts, one variant (warning is below the default log level)" "$K" compile-keymap --kccgst --layout br,us --variant nodeadkeys
run "the same run at XKB_LOG_LEVEL=warn" env XKB_LOG_LEVEL=warn "$K" compile-keymap --test --layout br,us --variant nodeadkeys
run "one layout, two variants" "$K" compile-keymap --kccgst --layout br --variant nodeadkeys,intl
run "two layouts, two variants (empty first)" "$K" compile-keymap --kccgst --layout br,us --variant ,dvorak

say "== log level: the default prints ERROR-level lines only"
run "unknown option at XKB_LOG_LEVEL=warn" env XKB_LOG_LEVEL=warn "$K" compile-keymap --test --layout br --options nope:nope
say ""

say "== include-path precedence (ephemeral probes; recreate with the recipe below)"
say "# recipe: mkdir -p \$T/xdg/xkb/symbols and \$T/home/.xkb/symbols; write the 5-line symbols/mado48 below;"
say "#   XDG_CONFIG_HOME=\$T/xdg xkbcli compile-keymap --layout mado48                 -> rc 0"
say "#   XDG_CONFIG_HOME unset, HOME=\$T/home (file at \$HOME/.xkb/symbols/mado48)     -> rc 0"
say "#   HOME=/nonexistent-home, XDG_CONFIG_HOME unset                            -> rc 1 (XKB-338)"
say "# The adjudicating values are the exit status and the XKB-338 stderr block."
cat >"$T/mado48.symbols" <<'EOF'
default partial alphanumeric_keys
xkb_symbols "basic" {
    name[Group1]= "Precedence probe";
    key <AE01> { [ 1 ] };
};
EOF
say '$ cat symbols/mado48'
cat "$T/mado48.symbols" >>"$OUT"
mkdir -p "$T/xdg/xkb/symbols" "$T/home/.xkb/symbols"
cp "$T/mado48.symbols" "$T/xdg/xkb/symbols/mado48"
cp "$T/mado48.symbols" "$T/home/.xkb/symbols/mado48"
XDG_CONFIG_HOME="$T/xdg" "$K" compile-keymap --layout mado48 >"$T/xdg-mado48.keymap" 2>"$T/xdg-mado48.err"
say "XDG_CONFIG_HOME/xkb/symbols/mado48 present: rc=$?"
say '$ sha256sum XDG-mado48.keymap'
sha256sum "$T/xdg-mado48.keymap" | sed "s#$T/##" >>"$OUT"
env -u XDG_CONFIG_HOME HOME="$T/home" "$K" compile-keymap --layout mado48 >"$T/home-mado48.keymap" 2>"$T/home-mado48.err"
say "HOME/.xkb/symbols/mado48 present, XDG_CONFIG_HOME unset: rc=$?"
say '$ cmp the two keymaps'
if cmp -s "$T/xdg-mado48.keymap" "$T/home-mado48.keymap"; then say "byte-identical"; else say "differ"; fi
env -u XDG_CONFIG_HOME HOME=/nonexistent-home "$K" compile-keymap --test --layout mado48 2>"$T/none-mado48.err"
say "neither user path present: rc=$?"
head -9 "$T/none-mado48.err" >>"$OUT"
say ""
run "root override falls back to the legacy root" env XKB_CONFIG_ROOT=/nonexistent-root XKB_LOG_LEVEL=warn "$K" compile-keymap --test --layout br
run "extra-path override is only a failed include" env XKB_CONFIG_EXTRA_PATH=/nonexistent-extra "$K" compile-keymap --test --layout br
say ""

say "== xkbcli ignores the environment names unless the flag is given (compile-keymap.c:585-595)"
run "XKB_DEFAULT_LAYOUT=zz, no flag" env XKB_DEFAULT_LAYOUT=zz "$K" compile-keymap --kccgst
run "XKB_DEFAULT_LAYOUT=zz with --enable-environment-names" env XKB_DEFAULT_LAYOUT=zz "$K" compile-keymap --kccgst --enable-environment-names
say "END OF RECEIPT"
printf 'receipt written: %s\n' "$OUT"
sha256sum "$OUT"
printf 'bytes: %s\n' "$(wc -c <"$OUT")"
