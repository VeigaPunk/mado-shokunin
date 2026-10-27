#!/usr/bin/env bash
# verify.sh — re-derive every locator in located.md from the pins in this seat dir.
#
#   ./verify.sh            human output, exit 0 = all checks passed
#
# What it does, in order:
#   1. PINS: every file listed in fetch/PINS.txt still has the recorded sha256.
#   2. HOST: the host snapshots in fetch/host/ are byte-identical to the pins the packages ship.
#   3. LOCATORS: for each behaviour row of located.md, line N of the pinned file contains the quoted text
#      (the line number is checked, so a shifted file fails).
#   4. GENERATION: xkeyboard-config 2.48 rules/rules.in + rules/generator reproduce the host's rules/evdev
#      byte-for-byte with --compat, and do NOT reproduce it without --compat.
#   5. RECEIPTS: the live `xkbcli compile-keymap` receipt has its recorded digest and symbol set name;
#      symbols/br contains no "nope" section.
# Reads only. Writes only under $TMPDIR (default: a fresh mktemp dir, removed on exit).

set -u
cd "$(dirname "$0")" || exit 2
ROOT=$PWD
L=fetch/libxkbcommon/xkbcommon-1.13.2
X=fetch/xkeyboard-config/xkeyboard-config-2.48
H=fetch/host

pass=0; fail=0
ok()   { pass=$((pass+1)); printf 'PASS %s\n' "$*"; }
bad()  { fail=$((fail+1)); printf 'FAIL %s\n' "$*"; }

# at FILE LINE PATTERN — line LINE of FILE must contain PATTERN verbatim
at() {
    local f=$1 n=$2 pat=$3 line
    if [ ! -f "$f" ]; then bad "$f:$n (missing file)"; return; fi
    line=$(sed -n "${n}p" "$f")
    case $line in
        *"$pat"*) ok "$f:$n  <<$pat>>" ;;
        *)        bad "$f:$n  expected <<$pat>> got <<$line>>" ;;
    esac
}

# uniq FILE PATTERN LINE — PATTERN must occur on exactly one line of FILE, namely LINE
uniq1() {
    local f=$1 pat=$2 n=$3 hits
    hits=$(grep -n -F -- "$pat" "$f" | cut -d: -f1 | tr '\n' ' ')
    if [ "$hits" = "$n " ]; then ok "$f:$n unique  <<$pat>>"
    else bad "$f:$n expected only line $n, got [$hits] for <<$pat>>"; fi
}

echo "== 1. pins =="
while read -r sum path src; do
    case $sum in \#*|'') continue ;; esac
    got=$(sha256sum "$path" 2>/dev/null | cut -d' ' -f1)
    [ "$got" = "$sum" ] && ok "pin $path" || bad "pin $path: $got != $sum ($src)"
done < fetch/PINS.txt

echo
echo "== 2. host snapshots vs pins =="
cmp -s "$X/symbols/br"    "$H/symbols-br"    && ok "host symbols/br == pin"    || bad "host symbols/br != pin"
cmp -s "$X/rules/base.xml" "$H/rules-base.xml" && ok "host rules/base.xml == pin" || bad "host rules/base.xml != pin"
cmp -s "$H/rules-base.xml" "$H/rules-evdev.xml" && ok "host rules/evdev.xml == host base.xml" || bad "host evdev.xml != base.xml"
cmp -s "$X/rules/base.extras.xml" "$H/rules-base.extras.xml" && ok "host rules/base.extras.xml == pin" || bad "host rules/base.extras.xml != pin"
[ "$(sha256sum <"$H/symbols-br" | cut -d' ' -f1)" = "$(sha256sum <"$X/symbols/br" | cut -d' ' -f1)" ] \
    && ok "symbols/br digest matches" || bad "symbols/br digest"

echo
echo "== 3. locators (located.md) =="
# A. entry point
uniq1 "$L/src/keymap.c"       'xkb_keymap_new_from_names(struct xkb_context *ctx,' 183
uniq1 "$L/src/keymap.c"       'return xkb_keymap_new_from_names2(ctx, rmlvo_in,'  187
uniq1 "$L/src/context-priv.c" 'xkb_context_sanitize_rule_names(struct xkb_context *ctx,' 187
uniq1 "$L/src/context-priv.c" 'rmlvo->rules = xkb_context_get_default_rules(ctx);' 193
uniq1 "$L/src/xkbcomp/xkbcomp.c" 'ok = xkb_components_from_rules_names(keymap->ctx, rmlvo, &kccgst,' 157
at "$L/meson.build" 194 "configh_data.set_quoted('DEFAULT_XKB_RULES', get_option('default-rules'))"

# B. rules matching
uniq1 "$L/src/xkbcomp/rules.c" 'if (m->rule.num_mlvo_values != m->mapping.num_mlvo ||' 1481
uniq1 "$L/src/xkbcomp/rules.c" 'NOTE: Wild card * matches empty values only for model and options, as' 1504
uniq1 "$L/src/xkbcomp/rules.c" 'return wildcard_type == WILDCARD_MATCH_ALL || !!to.len;' 1140
uniq1 "$L/src/xkbcomp/rules.c" 'match_group(struct matcher *m, struct sval group_name, struct sval to)' 1103
uniq1 "$L/src/xkbcomp/rules.c" 'to->matched = true;' 1163
uniq1 "$L/src/xkbcomp/rules.c" '! include <rules>' 2001

# C. warnings vs failures
uniq1 "$L/src/xkbcomp/rules.c"  'Unrecognized RMLVO option' 2063
uniq1 "$L/src/messages-codes.h" 'XKB_ERROR_CANNOT_RESOLVE_RMLVO = 595,' 150
uniq1 "$L/src/xkbcomp/rules.c"  'Unrecognized RMLVO model' 2048
at "$H/rules-evdev" 59 '*		=	evdev'
at "$H/rules-evdev" 175 '*		 *			=	pc+%l%(v)'
at "$H/rules-evdev" 138 '! model		 layout			=	symbols'
uniq1 "$L/src/xkbcomp/include.c" "Couldn't find file" 355
uniq1 "$L/src/messages-codes.h"  'XKB_ERROR_INCLUDED_FILE_NOT_FOUND = 338,' 116
uniq1 "$L/src/xkbcomp/include.c" "Couldn't process include statement for '%s(%s)'" 501
uniq1 "$L/src/messages-codes.h"  'XKB_ERROR_INVALID_INCLUDED_FILE = 661,' 162
uniq1 "$L/src/xkbcomp/xkbcomp.c" 'Failed to compile keymap' 62
at "$L/src/xkbcomp/xkbcomp.c" 105 'log_err(keymap->ctx, XKB_ERROR_KEYMAP_COMPILATION_FAILED,'
at "$L/src/xkbcomp/include.c" 169 'log_err(ctx, XKB_ERROR_INCLUDED_FILE_NOT_FOUND,'
uniq1 "$L/src/messages-codes.h"  'XKB_ERROR_KEYMAP_COMPILATION_FAILED = 822,' 190
at "$L/tools/compile-keymap.c" 521 'ERROR: Couldn'"'"'t create xkb keymap'
uniq1 "$L/tools/compile-keymap.c" 'return xkb_keymap_new_from_names2(ctx, rmlvo, keymap_input_format,' 503
at "$L/src/xkbcomp/xkbcomp.c" 106 "Couldn't look up rules"

# D. include path order
uniq1 "$L/src/context.c" 'xkb_context_include_path_append_default(struct xkb_context *ctx)' 243
uniq1 "$L/src/context.c" 'asprintf_safe("%s/xkb", xdg);' 257
uniq1 "$L/src/context.c" 'asprintf_safe("%s/.config/xkb", home);' 264
uniq1 "$L/src/context.c" 'asprintf_safe("%s/.xkb", home);' 272
uniq1 "$L/src/context.c" 'xkb_context_include_path_get_extra_path(ctx);' 279
uniq1 "$L/src/context.c" 'xkb_context_include_path_get_system_path(ctx);' 317
uniq1 "$L/src/context.c" 'return extra ? extra : DFLT_XKB_CONFIG_EXTRA_PATH;' 97
uniq1 "$L/src/context.c" 'return root ? root : DFLT_XKB_CONFIG_ROOT;' 236
uniq1 "$L/meson.build" 'XKB_CONFIG_ROOT = XKEYBOARD_CONFIG_ROOT' 116
uniq1 "$L/meson.build" "configh_data.set_quoted('DFLT_XKB_CONFIG_ROOT', XKB_CONFIG_ROOT)" 179
uniq1 "$L/meson.build" "configh_data.set_quoted('DFLT_XKB_CONFIG_EXTRA_PATH', XKB_CONFIG_EXTRA_PATH)" 192
uniq1 "$L/src/xkbcomp/include.c" '%u include paths searched:' 170
uniq1 "$L/src/xkbcomp/include.c" '%u include paths could not be added:' 184
uniq1 "$L/doc/custom-configuration.md" '`$XKB_CONFIG_EXTRA_PATH` if set, otherwise `<sysconfdir>/xkb`' 199
# the five levels appear in ascending order in that document
last=0
for pat in '$XDG_CONFIG_HOME/xkb' '$HOME/.xkb' '$XKB_CONFIG_EXTRA_PATH' '$XKB_CONFIG_ROOT'; do
    n=$(grep -n -F -- "$pat" "$L/doc/custom-configuration.md" | head -1 | cut -d: -f1)
    if [ -n "$n" ] && [ "$n" -gt "$last" ]; then ok "doc order $pat at line $n"; last=$n
    else bad "doc order $pat at line ${n:-none} (previous $last)"; fi
done

# E. layout/variant alignment
at "$L/src/xkbcomp/rules.c" 520 'if (darray_size(m->rmlvo.layouts) > darray_size(m->rmlvo.variants)) {'
at "$L/src/xkbcomp/rules.c" 527 'darray_resize0(m->rmlvo.variants, darray_size(m->rmlvo.layouts));'
at "$L/src/xkbcomp/rules.c" 530 'Less layouts than variants'
at "$L/src/xkbcomp/rules.c" 447 'if (darray_size(m->rmlvo.layouts) > darray_size(m->rmlvo.variants)) {'
uniq1 "$L/src/xkbcomp/rules.c" 'xkb_components_from_rules_names(struct xkb_context *ctx,' 2111

# F. xkeyboard-config generation
uniq1 "$X/rules/meson.build" "'rules.generator'," 26
uniq1 "$X/rules/meson.build" "cmd += ['--compat']" 36
uniq1 "$X/rules/meson.build" "ruleset_xml = configure_file(output: f'@ruleset@.xml'," 49
uniq1 "$X/rules/generator/__main__.py" 'add_argument("--compat", action="store_true", help="Compatibility rules")' 53
uniq1 "$X/rules/rules.in" 'This file use the following template format:' 2

# G/H. symbols/br
uniq1 "$X/symbols/br" 'xkb_symbols "abnt2" {' 4
uniq1 "$X/symbols/br" 'xkb_symbols "thinkpad" {' 68
n=$(grep -c 'nope' "$X/symbols/br")
[ "$n" = 0 ] && ok "symbols/br has no 'nope' section" || bad "symbols/br has $n 'nope' occurrences"

# option/keycodes anchors used by the receipt explanation
at "$H/rules-evdev" 529 '! option				=	symbols'
at "$H/rules-evdev" 570 'compose:caps				=	+compose(caps)'
at "$H/rules-evdev" 378 '*		=	+inet(evdev)'

echo
echo "== 4. generation: pinned generator + rules.in -> rules/evdev =="
# The generator needs a tree shaped like the source root: rules/{generator,*,compat}, plus the component
# directories it only *queries* for option->section existence. The pins supply rules/'; the component
# trees come from the installed package (read-only), and the tag's 8 legacy symbol *symlinks* are recreated
# from symbols/legacy-links.txt (the Arch package ships the link targets but not the links).
HOST_TREE=${XKB_HOST_TREE:-/usr/share/xkeyboard-config-2}
TMPD=$(mktemp -d "${TMPDIR:-/tmp}/xkbverify.XXXXXX") || exit 2
trap 'rm -rf -- "$TMPD"' EXIT
if [ ! -d "$HOST_TREE/symbols" ]; then
    printf 'SKIP generation: no component tree at %s (set XKB_HOST_TREE to an xkeyboard-config install)\n' "$HOST_TREE"
elif ! command -v python3 >/dev/null 2>&1; then
    printf 'SKIP generation: no python3\n'
else
    T=$TMPD/tree
    mkdir -p "$T/rules/generator" "$T/rules/compat" "$T/symbols"
    cp "$X"/rules/generator/*.py "$T/rules/generator/"
    cp "$X"/rules/rules.in "$X"/rules/base.xml "$X"/rules/base.extras.xml "$T/rules/"
    cp "$X"/rules/compat/*.lst "$T/rules/compat/"
    for f in "$HOST_TREE"/symbols/*; do ln -s "$f" "$T/symbols/$(basename "$f")"; done
    while IFS=$'\t' read -r name target; do
        [ -n "$name" ] || continue
        [ -e "$T/symbols/$target" ] && ln -sfn "$T/symbols/$target" "$T/symbols/$name" \
            || bad "legacy link target $target absent from $HOST_TREE/symbols"
    done < "$X/symbols/legacy-links.txt"
    for d in keycodes types compat geometry; do ln -s "$HOST_TREE/$d" "$T/$d"; done
    if PYTHONPATH="$T" python3 -m rules.generator rules --ruleset evdev --version v2 --compat \
            --output "$TMPD/evdev" "$T/rules/rules.in" >"$TMPD/gen.log" 2>&1; then
        cmp -s "$TMPD/evdev" "$H/rules-evdev" && ok "regenerated rules/evdev (--compat) == host byte-for-byte" \
            || bad "regenerated rules/evdev (--compat) differs from host"
        if PYTHONPATH="$T" python3 -m rules.generator rules --ruleset evdev --version v2 \
                --output "$TMPD/evdev-nocompat" "$T/rules/rules.in" >"$TMPD/gen2.log" 2>&1; then
            cmp -s "$TMPD/evdev-nocompat" "$H/rules-evdev" \
                && bad "without --compat the output still matched: --compat is not what the host used" \
                || ok "without --compat the output differs (host rules were built with --compat)"
        else
            bad "non-compat run failed (see $TMPD/gen2.log)"; sed 's/^/    /' "$TMPD/gen2.log"
        fi
    else
        bad "rules.generator did not run (see below)"
        sed 's/^/    /' "$TMPD/gen.log"
    fi
fi
# digest chain of the recorded receipts (independent of the tree above)
[ "$(sha256sum <receipts/rules-evdev-regenerated | cut -d' ' -f1)" = \
  "$(sha256sum <"$H/rules-evdev" | cut -d' ' -f1)" ] \
    && ok "receipts/rules-evdev-regenerated has the host digest" || bad "receipt digest != host digest"
[ "$(sha256sum <receipts/rules-evdev-regenerated-nocompat | cut -d' ' -f1)" != \
  "$(sha256sum <"$H/rules-evdev" | cut -d' ' -f1)" ] \
    && ok "receipts/rules-evdev-regenerated-nocompat differs from host (as recorded)" || bad "nocompat receipt equals host"

echo
echo "== 5. live receipts =="
rec=receipts/keymap-br-compose-caps.xkb
[ "$(sha256sum <"$rec" | cut -d' ' -f1)" = efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81 ] \
    && ok "receipt digest (br + compose:caps keymap, 73079 bytes)" || bad "receipt digest"
[ "$(wc -c <"$rec")" = 73079 ] && ok "receipt size 73079" || bad "receipt size $(wc -c <"$rec")"
grep -q 'xkb_symbols "pc_br_inet(evdev)_compose(caps)" {' "$rec" \
    && ok "receipt symbols set name pc_br_inet(evdev)_compose(caps)" || bad "receipt symbols set name"
[ -s receipts/keymap-br-compose-caps.err ] && bad "receipt stderr is not empty" || ok "receipt stderr empty (rc 0 path)"
if command -v xkbcli >/dev/null 2>&1; then
    if xkbcli compile-keymap --layout br --options compose:caps 2>/dev/null | cmp -s - "$rec"; then
        ok "live re-run xkbcli compile-keymap --layout br --options compose:caps reproduces the receipt"
    else
        bad "live re-run differs from the receipt"
    fi
    if xkbcli compile-keymap --layout zz >/dev/null 2>"$TMPD/zz.err"; then
        bad "live --layout zz exited 0"
    else
        grep -q 'XKB-338' "$TMPD/zz.err" && ok "live --layout zz exits nonzero with XKB-338" \
            || bad "live --layout zz nonzero but no XKB-338"
    fi
    # the seven rows of the live table in located.md (args | expected rc | stderr token, '-' = must be empty)
    # args | expected rc | stderr token ('-' = stderr must be empty) | XKB_LOG_LEVEL ('' = default)
    while IFS='|' read -r args want tok lvl; do
        [ -n "$args" ] || continue
        if [ -n "$lvl" ]; then
            if XKB_LOG_LEVEL=$lvl xkbcli compile-keymap $args >/dev/null 2>"$TMPD/c.err"; then rc=0; else rc=$?; fi
        else
            if xkbcli compile-keymap $args >/dev/null 2>"$TMPD/c.err"; then rc=0; else rc=$?; fi
        fi
        label="[$args${lvl:+ log=$lvl}]"
        if [ "$rc" != "$want" ]; then bad "live $label rc=$rc want $want"; continue; fi
        if [ "$tok" = "-" ]; then
            [ -s "$TMPD/c.err" ] && bad "live $label rc=$rc but stderr not empty" \
                || ok "live $label rc=$rc, empty stderr"
        else
            grep -q -- "$tok" "$TMPD/c.err" && ok "live $label rc=$rc with $tok" \
                || bad "live $label rc=$rc without $tok"
        fi
    done <<'CASES'
--layout br --options compose:caps|0|-|
--layout br|0|-|
--layout zz|1|XKB-338|
--layout br --variant nope|1|XKB-661|
--rules nope --layout br|1|XKB-338|
--layout br --options nope:nope|0|XKB-595|
--layout br --model nope|0|-|
--layout br,us|0|-|
--layout us,br --variant nodeadkeys|1|XKB-661|warning
--layout br --variant nodeadkeys,nodeadkeys|0|Less layouts than variants|
--layout us,br --variant abnt2,nodeadkeys|1|XKB-661|
CASES
    # the padding warning is log_warn: absent at default level, present at warning level
    if XKB_LOG_LEVEL=warning xkbcli compile-keymap --layout us,br --variant nodeadkeys >/dev/null 2>"$TMPD/w.err"; then :; fi
    grep -q 'WARNING: More layouts than variants' "$TMPD/w.err" \
        && ok "live padding warning appears at XKB_LOG_LEVEL=warning" || bad "padding warning missing"
    if xkbcli compile-keymap --layout us,br --variant nodeadkeys >/dev/null 2>"$TMPD/w2.err"; then :; fi
    grep -q 'More layouts than variants' "$TMPD/w2.err" \
        && bad "padding warning visible at the default log level" || ok "padding warning hidden at default level"
    # INFO level names the include-path census of D12/D13
    if XKB_LOG_LEVEL=info xkbcli compile-keymap --layout br >/dev/null 2>"$TMPD/i.err"; then :; fi
    for want in 'Include path failed: "/etc/xkb"' 'Include path added: /usr/share/xkeyboard-config-2'; do
        grep -q -- "$want" "$TMPD/i.err" && ok "live info: $want" || bad "live info missing: $want"
    done
else
    printf 'SKIP xkbcli not on PATH (host receipt kept in receipts/)\n'
fi

echo
echo "passed=$pass failed=$fail"
[ "$fail" -eq 0 ]
