#!/usr/bin/env bash
# mado round-48 w1 / seat ExecXkbLive — C2 live receipt: read-only xkbcli compile matrix.
#
# Read-only by construction: every xkbcli verb here is compile-keymap/list; hyprctl is used only
# with `version` and `devices -j`. No compositor mutation, no launch, no package transaction,
# no write to any host path. All fixture material lives in a scratch dir under
# /fast/scratch/hyaku/mado-r48/ExecXkbLive and is removed on exit; the only persistent write
# is receipts/xkb-live.txt inside the seat dir.
#
# Environment pinning: every xkbcli call runs under `env -i` with PATH, LC_ALL=C, a scratch HOME
# and a scratch XDG_CONFIG_HOME, so XKB_CONFIG_ROOT, XKB_CONFIG_EXTRA_PATH, XKB_LOG_LEVEL,
# XKB_DEFAULT_* and the caller's user xkb dirs cannot change what is measured. Section 8 then
# varies those variables deliberately, one at a time, to show what each one does.
#
# Usage: ./probe.sh        (regenerates receipts/xkb-live.txt; exits 0 when every section ran)
set -u

SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-48/w1/ExecXkbLive
SCRATCH_ROOT=/fast/scratch/hyaku/mado-r48/ExecXkbLive
mkdir -p "$SEAT/receipts" "$SCRATCH_ROOT" || exit 1
S=$(mktemp -d -p "$SCRATCH_ROOT" probe.XXXXXX) || exit 1
trap 'rm -rf -- "$S"' EXIT
OUT=$SEAT/receipts/xkb-live.txt
export XDG_CACHE_HOME=$S/cache          # nothing may reach the host cache during the probe
umask 022

PINHOME=$S/pinhome
PINCFG=$PINHOME/.config
mkdir -p "$PINCFG"

# Pinned environment: the caller's environment does not reach the compiler.
xc() { env -i PATH=/usr/bin:/bin LC_ALL=C HOME="$PINHOME" XDG_CONFIG_HOME="$PINCFG" /usr/bin/xkbcli "$@"; }
# Same, with a chosen HOME/XDG_CONFIG_HOME (include-path experiments).
xw() { local home=$1 cfg=$2; shift 2; env -i PATH=/usr/bin:/bin LC_ALL=C HOME="$home" XDG_CONFIG_HOME="$cfg" /usr/bin/xkbcli "$@"; }
# Same, with extra VAR=VAL pairs before a `--` (environment-sensitivity experiments).
xx() { local -a ev=(); while [ "$1" != "--" ]; do ev+=("$1"); shift; done; shift
       env -i PATH=/usr/bin:/bin LC_ALL=C HOME="$PINHOME" XDG_CONFIG_HOME="$PINCFG" "${ev[@]}" /usr/bin/xkbcli "$@"; }

# $HOME is shown as a literal token so the receipt carries no absolute user path.
hide() { sed -e "s|${HOME}|\\\$HOME|g" -e "s|${S}|\\\$S|g"; }

say() { printf '%s\n' "$*" >>"$OUT"; }
sec() { printf '\n===== %s =====\n' "$*" >>"$OUT"; }
# One bounded line per command: everything truncated.
clip() { cut -c1-200; }

: >"$OUT"

sec "0. host guard / tool identity (read-only)"
say "date        : $(date -u +%Y-%m-%dT%H:%M:%SZ)"
say "shell       : bash $BASH_VERSION"
say "xkbcli      : $(command -v xkbcli)"
say "sha256 xkbcli                  : $(sha256sum /usr/bin/xkbcli | cut -d' ' -f1)"
say "sha256 xkbcli-compile-keymap   : $(sha256sum /usr/lib/xkbcommon/xkbcli-compile-keymap | cut -d' ' -f1)"
say "xkbcli --version               : $(xc --version 2>&1 | clip)"
say "libxkbcommon.pc Version        : $(grep -m1 '^Version:' /usr/lib/pkgconfig/xkbcommon.pc | clip)"
say "xkeyboard-config.pc Version    : $(grep -m1 '^Version:' /usr/share/pkgconfig/xkeyboard-config.pc | clip)"
say "xkeyboard-config.pc xkb_root   : $(grep -m1 '^xkb_root=' /usr/share/pkgconfig/xkeyboard-config.pc | clip)"
say "hyprctl version (line 1)       : $(hyprctl version 2>&1 | head -1 | clip)"
say "ambient XKB_* vars             : $(env | grep -cE '^XKB_[A-Z_]+=') (0 = this host sets none); every xkbcli call below runs under env -i (PATH, LC_ALL=C, scratch HOME/XDG_CONFIG_HOME)"
say "host cache untouched           : XDG_CACHE_HOME=\$S/cache, created? $(test -e "$S/cache" && echo yes || echo no)"

sec "1. host names from ~/.config/hypr/input.conf (kb_* values only)"
CONF=$HOME/.config/hypr/input.conf
say "source: ~/.config/hypr/input.conf"
say "active kb_* assignments (verbatim lines):"
grep -nE '^[[:space:]]*kb_[a-z]+[[:space:]]*=' "$CONF" | hide | clip >>"$OUT"
say "commented kb_* lines (the us,dk,eu + intl case):"
grep -nE '^[[:space:]]*#[[:space:]]*kb_' "$CONF" | hide | clip >>"$OUT"
HOST_LAYOUT=$(awk -F= '/^[[:space:]]*kb_layout[[:space:]]*=/{v=$2; sub(/#.*/,"",v); gsub(/[[:space:]]/,"",v); print v; exit}' "$CONF")
HOST_OPTIONS=$(awk -F= '/^[[:space:]]*kb_options[[:space:]]*=/{v=$2; sub(/#.*/,"",v); gsub(/[[:space:]]/,"",v); print v; exit}' "$CONF")
HOST_VARIANT=$(awk -F= '/^[[:space:]]*kb_variant[[:space:]]*=/{v=$2; sub(/#.*/,"",v); gsub(/[[:space:]]/,"",v); print v; exit}' "$CONF")
say "derived RMLVO: kb_layout='${HOST_LAYOUT}' kb_variant='${HOST_VARIANT}' kb_options='${HOST_OPTIONS}' (absent lines -> empty)"
say "commented grp option on the kb_options line: $(awk '/^[[:space:]]*kb_options/{print $0}' "$CONF" | grep -o '#[^#]*grp:[a-z_]*' | clip)"

sec "2. positive: host RMLVO compiles (layout=$HOST_LAYOUT options=$HOST_OPTIONS)"
xc compile-keymap --layout "$HOST_LAYOUT" --options "$HOST_OPTIONS" >"$S/host.keymap" 2>"$S/host.err"
RC=$?
SHA_HOST=$(sha256sum "$S/host.keymap" | cut -d' ' -f1)
say "cmd         : xkbcli compile-keymap --layout $HOST_LAYOUT --options $HOST_OPTIONS"
say "rc          : $RC"
say "stdout lines: $(wc -l <"$S/host.keymap")"
say "stdout bytes: $(wc -c <"$S/host.keymap")"
say "sha256 out  : $SHA_HOST"
say "stderr (no --verbose)   : $(grep -c . "$S/host.err") lines, XKB codes: $(grep -o 'XKB-[0-9]*' "$S/host.err" | sort -u | tr '\n' ' ' | clip)"
xc compile-keymap --layout "$HOST_LAYOUT" --options "$HOST_OPTIONS" --verbose >/dev/null 2>"$S/host.verbose"
say "stderr with --verbose   : $(grep -c . "$S/host.verbose") lines (warnings surface only at --verbose, and only while XKB_LOG_LEVEL is unset or symbolic — section 8)"
say "verbose XKB census (code, count, first message):"
for c in $(grep -o 'XKB-[0-9]*' "$S/host.verbose" | sort -u); do
  printf '  %-8s n=%-3s %s\n' "$c" "$(grep -c "$c" "$S/host.verbose")" \
    "$(grep -m1 "$c" "$S/host.verbose" | hide | clip)" >>"$OUT"
done
say "--kccgst (rules -> KcCGST):"
xc compile-keymap --layout "$HOST_LAYOUT" --options "$HOST_OPTIONS" --kccgst 2>/dev/null | hide | clip >>"$OUT"
say "--rmlvo (defaults filled in):"
xc compile-keymap --layout "$HOST_LAYOUT" --options "$HOST_OPTIONS" --rmlvo 2>/dev/null | hide | clip >>"$OUT"

sec "3. negative matrix (rc, stdout sha, first XKB-### of stderr; pinned environment)"
neg() {
  local label=$1; shift
  local rc code line sha lines
  xc compile-keymap "$@" >"$S/n.out" 2>"$S/n.err"; rc=$?
  code=$(grep -o -m1 'XKB-[0-9]*' "$S/n.err" || true); [ -n "$code" ] || code='-'
  line=$(grep -m1 . "$S/n.err" || true)
  sha=$(sha256sum "$S/n.out" | cut -d' ' -f1); lines=$(wc -l <"$S/n.out")
  printf '%-30s rc=%d lines=%-5s sha=%s code=%s | %s\n' \
    "$label" "$rc" "$lines" "${sha:0:16}" "$code" "$(printf '%s' "$line" | hide | clip)" >>"$OUT"
  printf '    args: %s\n' "$*" >>"$OUT"
}
neg unknown-layout          --layout zz
neg unknown-variant         --layout br --variant nope
neg unknown-option          --layout br --options nope:nope
neg unknown-model           --layout br --model nope
neg unknown-rules           --rules nope --layout br
neg two-layouts-one-variant --layout us,br --variant ,abnt2
neg variant-on-first-layout-fails --layout us,br --variant abnt2
neg variant-on-first-valid --layout br,us --variant abnt2
neg more-variants-than-layouts --layout br --variant abnt2,intl
neg variant-valid-elsewhere --layout br --variant intl
neg option-group-exists     --layout br --options grp:alts_toggle
neg host-options-plus-grp   --layout br --options "$HOST_OPTIONS,grp:alts_toggle"
neg commented-us-dk-eu-intl --layout us,dk,eu --variant intl
say "component mapping for the accepted cases:"
say "  two-layouts-one-variant: $(xc compile-keymap --layout us,br --variant ,abnt2 --kccgst 2>/dev/null | grep -o 'symbols { include "[^"]*"' | clip)"
say "  commented-us-dk-eu-intl: $(xc compile-keymap --layout us,dk,eu --variant intl --kccgst 2>/dev/null | grep -o 'symbols { include "[^"]*"' | clip)"
say "  option-group-exists    : $(xc compile-keymap --layout br --options grp:alts_toggle --kccgst 2>/dev/null | grep -o 'symbols { include "[^"]*"' | clip)"
say "equivalence checks (sha256 of stdout; identical stdout = the name was silently dropped):"
SHA_BR=$(xc compile-keymap --layout br 2>/dev/null | sha256sum | cut -d' ' -f1)
SHA_OPT=$(xc compile-keymap --layout br --options nope:nope 2>/dev/null | sha256sum | cut -d' ' -f1)
SHA_ABNT=$(xc compile-keymap --layout br --variant abnt2 2>/dev/null | sha256sum | cut -d' ' -f1)
SHA_OVER=$(xc compile-keymap --layout br --variant abnt2,intl 2>/dev/null | sha256sum | cut -d' ' -f1)
say "  baseline --layout br               : $SHA_BR"
say "  unknown option dropped (nope:nope) : $SHA_OPT  identical_to_baseline=$([ "$SHA_OPT" = "$SHA_BR" ] && echo yes || echo no)"
say "  --variant abnt2 (single)           : $SHA_ABNT"
say "  --variant abnt2,intl (overflow)    : $SHA_OVER  identical_to_abnt2=$([ "$SHA_OVER" = "$SHA_ABNT" ] && echo yes || echo no) (extra variants dropped, first still applied)"
say "  overflow kccgst                    : $(xc compile-keymap --layout br --variant abnt2,intl --kccgst 2>/dev/null | grep -o 'symbols { include "[^"]*"' | clip)"
say "3b. drop shapes (unknown name kept in RMLVO, no effect on the keymap):"
say "  --model nope --rmlvo : $(xc compile-keymap --layout br --model nope --rmlvo 2>/dev/null | tr '\n' ' ' | clip)"
say "  --model nope stderr  : $(xc compile-keymap --layout br --model nope 2>&1 >/dev/null | grep -c .) lines at default verbosity"
for o in nope:caps grp:nope grp:alts_toggle:nope; do
  xc compile-keymap --layout br --options "$o" >"$S/d.out" 2>"$S/d.err"; rc=$?
  printf '  option %-22s rc=%d sha16=%s code=%s msg=%s\n' "$o" "$rc" \
    "$(sha256sum "$S/d.out" | cut -c1-16)" "$(grep -o -m1 'XKB-[0-9]*' "$S/d.err")" \
    "$(grep -m1 . "$S/d.err" | hide | clip)" >>"$OUT"
done

sec "4. include-path search order and user paths"
say "verbose include-path lines (stderr, --verbose; pinned HOME/XDG under \$S, \$HOME hidden):"
xc compile-keymap --layout br --options compose:caps --verbose 2>&1 >/dev/null \
  | grep -E 'Include (path|extensions path)' | head -8 | hide | clip >>"$OUT"
say "host user paths (the ambient \$HOME/XDG_CONFIG_HOME of this workstation):"
for p in "${XDG_CONFIG_HOME:-$HOME/.config}/xkb" "$HOME/.xkb" /etc/xkb /usr/share/xkeyboard-config-2; do
  say "  $(printf '%s' "$p" | hide) : $([ -d "$p" ] && echo present || echo absent)"
done

# Tiny valid symbols file used to prove which include path supplies a layout.
mkdir -p "$S/cfg/xkb/symbols" "$S/home/.xkb/symbols" "$S/empty" "$S/home2" "$S/empty2" "$S/oa/xkb/symbols" "$S/ob/xkb/symbols"
SYM='default partial alphanumeric_keys
xkb_symbols "basic" {
    include "us(basic)"
    key <AD11> { [ KEYSYM ] };
};'
printf '%s\n' "${SYM/KEYSYM/dead_acute}"  >"$S/cfg/xkb/symbols/mado48"
printf '%s\n' "${SYM/KEYSYM/dead_greek}"  >"$S/home/.xkb/symbols/mado48"
printf '%s\n' "${SYM/KEYSYM/dead_acute}"  >"$S/oa/xkb/symbols/mado48"
printf '%s\n' "${SYM/KEYSYM/dead_greek}"  >"$S/ob/xkb/symbols/mado48"
say "fixture symbols/mado48 body (shared, KEYSYM varied):"
printf '%s\n' "$SYM" | sed 's/^/    /' >>"$OUT"

inc() {
  local label=$1 home=$2 cfg=$3; shift 3
  local rc code line
  xw "$home" "$cfg" compile-keymap "${INC_ARGS[@]}" --layout mado48 >"$S/i.out" 2>"$S/i.err"; rc=$?
  code=$(grep -o -m1 'XKB-[0-9]*' "$S/i.err" || true); [ -n "$code" ] || code='-'
  line=$(grep -m1 . "$S/i.err" || true)
  printf '%-38s rc=%d lines=%-5s AD11=%-20s code=%s | %s\n' \
    "$label" "$rc" "$(wc -l <"$S/i.out")" \
    "$(grep -o 'dead_[a-z]*' "$S/i.out" | head -1)" "$code" \
    "$(printf '%s' "$line" | hide | clip)" >>"$OUT"
}
INC_ARGS=()
inc "XDG_CONFIG_HOME dir only"      "$S/home2" "$S/cfg"
inc "HOME/.xkb dir only"            "$S/home"  "$S/empty"
inc "no user path (host default)"   "$S/home2" "$S/empty2"
INC_ARGS=(--include "$S/cfg/xkb")
inc "--include dir, defaults dropped" "$S/home2" "$S/empty2"
INC_ARGS=(--include "$S/cfg/xkb" --include-defaults)
inc "--include dir + --include-defaults" "$S/home2" "$S/empty2"
INC_ARGS=(--include "$S/oa/xkb" --include "$S/ob/xkb" --include-defaults)
inc "order: oa first (dead_acute wins)" "$S/home2" "$S/empty2"
INC_ARGS=(--include "$S/ob/xkb" --include "$S/oa/xkb" --include-defaults)
inc "order: ob first (dead_greek wins)" "$S/home2" "$S/empty2"

sec "5. compositor state read (hyprctl devices -j; keyboard names replaced kbd1..n)"
hyprctl devices -j >"$S/dev.json" 2>"$S/dev.err"
say "hyprctl devices -j rc=$? err=$(grep -m1 . "$S/dev.err" | hide | clip) (hyprctl runs in the ambient session env by design: it needs the compositor socket)"
python3 - "$S/dev.json" >>"$OUT" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as fh:
    data = json.load(fh)
kbs = data.get("keyboards", [])
print(f"keyboards: {len(kbs)} (names replaced)")
for i, kb in enumerate(kbs, 1):
    print("  kbd%d layout=%r variant=%r options=%r active_layout_index=%s active_keymap=%r"
          % (i, kb.get("layout"), kb.get("variant"), kb.get("options"),
             kb.get("active_layout_index"), kb.get("active_keymap")))
print("distinct (layout,variant,options,active_keymap) tuples: %d"
      % len({(k.get("layout"), k.get("variant"), k.get("options"), k.get("active_keymap")) for k in kbs}))
PY

sec "6. name inventories on this host (xkeyboard-config 2.48 data under /usr/share/xkeyboard-config-2)"
XK=/usr/share/xkeyboard-config-2
xc list >"$S/list.txt" 2>"$S/list.err"
say "registry (xkbcli list): rc=$? lines=$(wc -l <"$S/list.txt") stderr=$(grep -c . "$S/list.err") | models=$(sed -n '1,/^layouts:/p' "$S/list.txt" | grep -c '^- name:') layout-entries=$(grep -c '^- layout:' "$S/list.txt") variant-entries=$(grep -c "^  variant: '[^']" "$S/list.txt")"
say "registry layout set includes br/us/dk/eu: $(for l in br us dk eu; do grep -qx -- "- layout: '$l'" "$S/list.txt" && printf '%s:Y ' "$l" || printf '%s:N ' "$l"; done)"
say "registry br variants   : $(awk "/^- layout: 'br'/{f=1;next} /^- layout:/{f=0} f&&/^  variant:/{gsub(/.*variant: '|'.*/,\"\"); printf \"%s \", \$0}" "$S/list.txt")"
say "symbols/br declarations: $(grep -o 'xkb_symbols "[^"]*"' "$XK/symbols/br" | sed 's/xkb_symbols "//;s/"//' | grep -v '^$' | tr '\n' ' ')"
say "  -> divergence: br(abnt2) compiles (section 3) although the registry does not list it as a br variant"
BRV=$(grep -o 'xkb_symbols "[^"]*"' "$XK/symbols/br" | sed 's/xkb_symbols "//;s/"//' | grep -v '^$')
say "  declared-variant compile check (every name above), rc:"
for v in $BRV; do
  printf '    br(%-20s) rc=%d\n' "$v" "$(xc compile-keymap --layout br --variant "$v" >/dev/null 2>&1; echo $?)" >>"$OUT"
done
say "  layout names resolve against symbols/ files, not the registry XML:"
say "    symbols/eu file present=$([ -f "$XK/symbols/eu" ] && echo yes || echo no); registry layout 'eu'=$(grep -qx -- "- layout: 'eu'" "$S/list.txt" && echo yes || echo no); --layout eu rc=$(xc compile-keymap --layout eu >/dev/null 2>&1; echo $?) lines=$(xc compile-keymap --layout eu 2>/dev/null | wc -l)"
say "registry model count   : $(sed -n '1,/^layouts:/p' "$S/list.txt" | grep -c '^- name:'), pc105 present=$([ "$(sed -n '1,/^layouts:/p' "$S/list.txt" | grep -cx -- '- name: pc105')" -gt 0 ] && echo yes || echo no), nope present=$([ "$(sed -n '1,/^layouts:/p' "$S/list.txt" | grep -cx -- '- name: nope')" -gt 0 ] && echo yes || echo no)"
say "options inventory (rules/evdev.lst): option names total=$(grep -cE '^  [a-z0-9_]+:' "$XK/rules/evdev.lst")"
say "  grp:* options=$(grep -cE '^  grp:' "$XK/rules/evdev.lst") compose:* options=$(grep -cE '^  compose:' "$XK/rules/evdev.lst")"
say "  alts_toggle   : $(grep -m1 -E '^  (grp:)?alts_toggle' "$XK/rules/evdev.lst" | clip)"
say "  compose:caps  : $(grep -m1 -E '^  compose:caps ' "$XK/rules/evdev.lst" | clip)"
say "data pins (sha256):"
for f in symbols/br symbols/group symbols/pc symbols/us rules/evdev rules/evdev.xml rules/evdev.lst; do
  say "  $(sha256sum "$XK/$f" | cut -d' ' -f1)  $f"
done

sec "7. environment sensitivity of the compile (one variable at a time; pinned base in sections 2-4)"
mkdir -p "$S/root-empty" "$S/poison-xdg/xkb/symbols" "$S/poison-home/.xkb/symbols" "$S/poison-extra/symbols"
PD='default partial alphanumeric_keys
xkb_symbols "basic" {
    include "us(basic)"
    key <AD11> { [ KEYSYM ] };
};'
printf '%s\n' "${PD/KEYSYM/dead_acute}"      >"$S/poison-xdg/xkb/symbols/zz"
printf '%s\n' "${PD/KEYSYM/dead_greek}"      >"$S/poison-home/.xkb/symbols/zz"
printf '%s\n' "${PD/KEYSYM/dead_circumflex}" >"$S/poison-extra/symbols/zz"
ad11() { grep -o 'dead_[a-z]*' "$1" | head -1; }

/usr/bin/xkbcli compile-keymap --layout br --options compose:caps >"$S/ambient.keymap" 2>/dev/null
SHA_AMB=$(sha256sum "$S/ambient.keymap" | cut -d' ' -f1)
say "ambient-env run vs pinned-env run of the host RMLVO: ambient sha=$SHA_AMB pinned sha=$SHA_HOST equal=$([ "$SHA_AMB" = "$SHA_HOST" ] && echo yes || echo no) (they differ only if the caller's user xkb dirs or XKB_* env supply something)"

say "7a. XKB_LOG_LEVEL controls the message, not the drop (unknown option nope:nope, rc stays 0):"
for lvl in UNSET 0 3 5 10 20 30 critical error warning none bogus debug; do
  if [ "$lvl" = UNSET ]; then
    xc compile-keymap --layout br --options nope:nope >"$S/e.out" 2>"$S/e.err"
  else
    xx XKB_LOG_LEVEL="$lvl" -- compile-keymap --layout br --options nope:nope >"$S/e.out" 2>"$S/e.err"
  fi
  printf '  XKB_LOG_LEVEL=%-8s rc=%d stderr_lines=%-2d XKB=%s sha16=%s\n' "$lvl" "$?" \
    "$(grep -c . "$S/e.err")" "$(grep -o -m1 'XKB-[0-9]*' "$S/e.err" || echo -)" \
    "$(sha256sum "$S/e.out" | cut -c1-16)" >>"$OUT"
done

say "7b. XKB_CONFIG_ROOT changes the root string the compiler starts from:"
say "  unset          -> $(xc compile-keymap --layout br --verbose 2>&1 >/dev/null | grep -o 'Include path added: .*' | head -1 | hide | clip)"
say "  /nonexistent   -> $(xx XKB_CONFIG_ROOT=/nonexistent -- compile-keymap --layout zz 2>&1 >/dev/null | grep -A1 'include paths searched' | tail -1 | sed 's/^[[:space:]]*//' | clip)"
say "  empty dir      -> $(xx XKB_CONFIG_ROOT="$S/root-empty" -- compile-keymap --layout zz 2>&1 >/dev/null | grep -A1 'include paths searched' | tail -1 | sed 's/^[[:space:]]*//' | hide | clip)"
xx XKB_CONFIG_ROOT="$S/root-empty" -- compile-keymap --layout br >/dev/null 2>"$S/r.err"; RC=$?
say "  empty dir, valid br: rc=$RC code=$(grep -o -m1 'XKB-[0-9]*' "$S/r.err" || echo -) msg=$(grep -m1 . "$S/r.err" | hide | clip)"

say "7c. user and extra xkb dirs are searched before the root; a poisoned symbols/zz proves precedence:"
xw "$S/home2" "$S/poison-xdg" compile-keymap --layout zz >"$S/p1" 2>"$S/p1e"
say "  \$XDG_CONFIG_HOME/xkb only: rc=$? AD11=$(ad11 "$S/p1") (baseline for zz in the pinned tree: rc 1 XKB-338, section 3)"
xw "$S/poison-home" "$S/poison-xdg" compile-keymap --layout zz >"$S/p2" 2>"$S/p2e"
say "  XDG_CONFIG_HOME/xkb + \$HOME/.xkb: rc=$? AD11=$(ad11 "$S/p2") (first user path wins)"
xw "$S/poison-home" "$S/empty2" compile-keymap --layout zz >"$S/p2b" 2>"$S/p2be"
say "  \$HOME/.xkb only (XDG empty): rc=$? AD11=$(ad11 "$S/p2b")"
xx XKB_CONFIG_EXTRA_PATH="$S/poison-extra" -- compile-keymap --layout zz >"$S/p3" 2>"$S/p3e"
say "  XKB_CONFIG_EXTRA_PATH only: rc=$? AD11=$(ad11 "$S/p3")"
env -i PATH=/usr/bin:/bin LC_ALL=C HOME="$S/poison-home" XDG_CONFIG_HOME="$S/empty2" XKB_CONFIG_EXTRA_PATH="$S/poison-extra" /usr/bin/xkbcli compile-keymap --layout zz >"$S/p3b" 2>/dev/null
say "  \$HOME/.xkb + XKB_CONFIG_EXTRA_PATH: AD11=$(ad11 "$S/p3b") (orders HOME against extra)"
env -i PATH=/usr/bin:/bin LC_ALL=C HOME="$S/poison-home" XDG_CONFIG_HOME="$S/poison-xdg" XKB_CONFIG_EXTRA_PATH="$S/poison-extra" /usr/bin/xkbcli compile-keymap --layout zz >"$S/p4" 2>/dev/null
say "  XDG + HOME + extra together: AD11=$(ad11 "$S/p4") (which vector reaches first)"

say "7d. XKB_DEFAULT_* are inert for xkbcli (unlike the compositor, which is not exercised here):"
xx XKB_DEFAULT_LAYOUT=zz XKB_DEFAULT_RULES=nope XKB_DEFAULT_OPTIONS=nope:nope -- compile-keymap --layout br >"$S/def.keymap" 2>"$S/def.err"
say "  XKB_DEFAULT_{LAYOUT=zz,RULES=nope,OPTIONS=nope:nope} with --layout br: rc=$? sha16=$(sha256sum "$S/def.keymap" | cut -c1-16) identical_to_baseline=$([ "$(sha256sum "$S/def.keymap" | cut -d' ' -f1)" = "$SHA_BR" ] && echo yes || echo no) stderr_lines=$(grep -c . "$S/def.err")"

sec "8. probe hygiene"
say "commands used: xkbcli compile-keymap/list (read: stdout), xkbcli --version, hyprctl version, hyprctl devices -j, coreutils"
say "writes inside scratch only: $(find "$S" -type f | wc -l) files under \$S (removed by trap on exit)"
say "host cache written: $(test -e "$S/cache" && echo yes || echo no)"

printf '\nreceipt written to %s (%s bytes)\n' "$OUT" "$(wc -c <"$OUT")"
