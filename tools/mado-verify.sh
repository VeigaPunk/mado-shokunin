#!/usr/bin/env bash
# =============================================================================
# mado-verify.sh — mado-shokunin config-plane verdict gate (v1, round 5 / M5-2)
#
# Verifies the DECLARED config planes (hypr core, waybar, walker, terminals)
# against live bytes and, where available, live hyprctl reads, then emits one
# verdict line:
#
#     MADO_VERIFY: CLEAN    (...)
#     MADO_VERIFY: DIVERGED (...)
#
# Exit map: 0 = CLEAN · 1 = DIVERGED (a check FAILed, or a required check was
# UNVERIFIABLE) · 2 = tool/usage error (bad args; a failing --selftest).
#
# Usage:
#   mado-verify.sh                 # live run against $HOME (read-only)
#   mado-verify.sh --no-live       # file plane only; verdict names the scope
#   mado-verify.sh --root DIR      # file plane against DIR (used by selftest)
#   mado-verify.sh --selftest      # hermetic fixture tests, no substrate reads
#
# Discipline (PROVINCE.md:10-12, :16; SKILL.md "Safe-probe discipline"):
#   * READ-ONLY on every substrate: hyprctl read verbs only (version,
#     instances, configerrors, getoption, binds, monitors, layers); no file is
#     written; scratch lives under /tmp/w5-mado-m52-* and only --selftest makes it.
#   * Anti-claim: a plane that cannot be verified reads UNKNOWN and blocks
#     CLEAN — never a fake CLEAN (SKILL safety rule 5).
#   * Session material stays shape-only: no window titles, no compositor log,
#     no instance signature printed in full.
#   * NOTEs are record-level rows (S3-class or open findings); they never
#     flip the verdict, but they stay visible in the report.
#
# Invariants encoded (measured anchors in corpus/knowledge/):
#   hypr    — hyprland.conf is a pure orchestrator: 17 source statements in the
#             exact include order (MADO-1 §1/§3); 12 active local confs
#             (MADO-1 §2); local envs.conf is an orphan (MADO-1 §2,
#             MADO-R2-1 §6/F3); the no-gaps toggle declares 0s (MADO-1 §7).
#   hypr-live — configerrors empty; gaps_out "0 0 0 0"; kb_layout br;
#             border_size 0; rounding 0; animations on; binds 192; DP-1
#             3440x1440@~100; touchpad scroll_factor 0.4; GDK_SCALE=1;
#             NVD_BACKEND unset (MADO-1 §4/§7/§10, MADO-R2-1 §3/§7).
#   waybar  — config.jsonc JSONC-parses; reload_style_on_change true; bar
#             globals layer/position top + height 26 (MADO-2 §2.1); style.css
#             imports the theme css (MADO-2 §2.5); live: process, layer
#             surface pid agreement, tray watcher (MADO-R3-1 §1/§2.3).
#   walker  — config.toml TOML-parses; force_keyboard_focus/selection_wrap/
#             hide_action_hints true, theme omarchy-default (MADO-2 §3); live:
#             app-walker@autostart.service + elephant.service active,
#             version pin 2.17.0 (MADO-R3-1 §1/§6).
#   terms   — alacritty.toml TOML-parses and imports the theme (MADO-3 §1-3);
#             font 12.5 + padding 14 uniform across the four configs
#             (MADO-3 §3); install state: alacritty only (MADO-3 §5).
#   pins    — Hyprland 0.56.2 commit efb5099…, waybar v0.15.0, walker 2.17.0
#             (SKILL.md "Version pins"): a changed pin is a FAIL — the claims
#             must be re-verified, not silently reused.
#
# Explicitly NOT verified here (no read surface; stays UNKNOWN, never guessed):
# window-rule effects, dispatcher behaviour, module text, idle/lock
# transitions, per-window rules (SKILL "claim-first routing").
# =============================================================================
set -u
export LC_ALL=C

VERSION_STR="mado-verify.sh v1 (mado-shokunin round 5 / M5-2)"
ROOT="${MADO_VERIFY_ROOT:-$HOME}"
LIVE_REQ="${MADO_VERIFY_LIVE:-auto}"
MODE="verify"

PASS=0; FAIL=0; UNKNOWN=0; SKIP=0; NOTE=0
declare -a ROWS=()

usage() {
  cat <<'EOF'
usage: mado-verify.sh [--no-live] [--live] [--root DIR] [--selftest] [--help]

  (default)     live read-only run against $HOME (or MADO_VERIFY_ROOT)
  --no-live     file plane only; the verdict names the skipped live layer
  --root DIR    verify DIR as the config root (default $HOME)
  --selftest    hermetic fixture tests under /tmp/w5-mado-m52-* (no substrate)
  --help        this text

verdict: MADO_VERIFY: CLEAN|DIVERGED (...)   exit 0 / 1  (usage error: 2)
env: MADO_VERIFY_ROOT (config root), MADO_VERIFY_LIVE=auto|yes|no
EOF
}

row() { # plane id status detail
  local plane="$1" id="$2" st="$3" detail="$4"
  ROWS+=("$plane|$id|$st|$detail")
  case "$st" in
    PASS) PASS=$((PASS + 1)) ;;
    FAIL) FAIL=$((FAIL + 1)) ;;
    UNKNOWN) UNKNOWN=$((UNKNOWN + 1)) ;;
    SKIP) SKIP=$((SKIP + 1)) ;;
    NOTE) NOTE=$((NOTE + 1)) ;;
  esac
}

have() { command -v "$1" >/dev/null 2>&1; }
tmo() { if have timeout; then timeout 5 "$@"; else "$@"; fi; }

# rc → row mapper for python check blocks: 0 PASS, 6 UNKNOWN, else FAIL
row_from_rc() { # plane id detail rc
  case "$4" in
    0) row "$1" "$2" PASS "$3" ;;
    6) row "$1" "$2" UNKNOWN "$3" ;;
    *) row "$1" "$2" FAIL "$3" ;;
  esac
}

# ---------------------------------------------------------------------------
# python availability (all JSON/TOML parsing runs through python3; its absence
# is an UNKNOWN, never a silent pass)
# ---------------------------------------------------------------------------
PY_OK=0; have python3 && python3 -c 'pass' >/dev/null 2>&1 && PY_OK=1
PY_TOML=0
if [ "$PY_OK" = 1 ] && python3 -c 'import tomllib' >/dev/null 2>&1; then PY_TOML=1; fi

# JSONC → JSON (comments + trailing commas stripped, string-aware).
# prints compact JSON on stdout; parse/read errors go to stderr with rc 4/3.
jsonc_parse() {
  python3 - "$1" <<'PY'
import json, re, sys
try:
    s = open(sys.argv[1], encoding='utf-8', errors='replace').read()
except OSError as e:
    print("read error: %s" % e, file=sys.stderr); sys.exit(3)
out = []; i = 0; n = len(s); instr = False; esc = False
while i < n:
    c = s[i]
    if instr:
        out.append(c)
        if esc: esc = False
        elif c == '\\': esc = True
        elif c == '"': instr = False
        i += 1; continue
    if c == '"':
        instr = True; out.append(c); i += 1; continue
    if c == '/' and i + 1 < n and s[i + 1] == '/':
        j = s.find('\n', i); i = n if j < 0 else j; continue
    if c == '/' and i + 1 < n and s[i + 1] == '*':
        j = s.find('*/', i + 2); i = n if j < 0 else j + 2; continue
    out.append(c); i += 1
t = ''.join(out)
prev = None
while prev != t:
    prev = t
    t = re.sub(r',(\s*[}\]])', r'\1', t)
try:
    d = json.loads(t)
except Exception as e:
    print("parse error: %s" % e, file=sys.stderr); sys.exit(4)
print(json.dumps(d))
PY
}

# JSON pointer check: args = <json-string> <dotted-path> <expected-json>
# prints "ok" or "got=X want=Y"; rc 0 ok / 5 mismatch / 4 error
json_expect() {
  python3 - "$1" "$2" "$3" <<'PY'
import json, sys
try:
    cur = json.loads(sys.argv[1])
except Exception as e:
    print("json error: %s" % e); sys.exit(4)
for k in sys.argv[2].split('.'):
    if isinstance(cur, dict) and k in cur:
        cur = cur[k]
    else:
        cur = None; break
try:
    exp = json.loads(sys.argv[3])
except Exception:
    exp = sys.argv[3]
if cur == exp:
    print("ok"); sys.exit(0)
print("got=%s want=%s" % (json.dumps(cur), json.dumps(exp))); sys.exit(5)
PY
}

# walker config check: parse + 4 key invariants (MADO-2 §3).
# rc 0 pass (prints detail) / 4 parse error / 5 mismatch
walker_check() {
  python3 - "$1" <<'PY'
import sys, tomllib
try:
    d = tomllib.load(open(sys.argv[1], 'rb'))
except Exception as e:
    print("parse error: %s" % e, file=sys.stderr); sys.exit(4)
bad = []
if d.get('force_keyboard_focus') is not True: bad.append("force_keyboard_focus=%r" % d.get('force_keyboard_focus'))
if d.get('selection_wrap') is not True: bad.append("selection_wrap=%r" % d.get('selection_wrap'))
if d.get('theme') != "omarchy-default": bad.append("theme=%r" % d.get('theme'))
if d.get('hide_action_hints') is not True: bad.append("hide_action_hints=%r" % d.get('hide_action_hints'))
if bad:
    print("mismatch: " + ", ".join(bad)); sys.exit(5)
print("4/4 keys match (focus/wrap/theme/hints)")
PY
}

# ---------------------------------------------------------------------------
# boundary proof — hash the config plane before/after; the gate itself must
# not touch it (SKILL safety rule 3). Skipped when the root has no .config.
# ---------------------------------------------------------------------------
boundary_hash() {
  local base="$1"
  [ -d "$base" ] || { echo "-"; return 0; }
  find "$base" -type f \
    \( -name '*.conf' -o -name '*.jsonc' -o -name '*.css' -o -name '*.toml' \
       -o -name '*.ini' -o -name 'config' \) 2>/dev/null | sort | while read -r f; do
    sha256sum "$f"
  done | sha256sum | cut -d' ' -f1
}

# ===========================================================================
# SELFTEST — hermetic fixtures under /tmp/w5-mado-m52-* (no substrate reads)
# ===========================================================================
build_fixture() { # $1 = root
  local R="$1"
  mkdir -p "$R/.config/hypr" "$R/.config/waybar" "$R/.config/walker" \
           "$R/.config/alacritty" "$R/.config/foot" "$R/.config/kitty" \
           "$R/.config/ghostty" "$R/.config/omarchy/current/theme" \
           "$R/.local/share/omarchy/default/hypr/bindings" \
           "$R/.local/share/omarchy/default/walker/themes" \
           "$R/.local/state/omarchy/toggles/hypr"

  cat >"$R/.config/hypr/hyprland.conf" <<'EOF'
# fixture — pure orchestrator, mirrors MADO-1 §3 include order
source = ~/.local/share/omarchy/default/hypr/autostart.conf
source = ~/.local/share/omarchy/default/hypr/bindings/media.conf
source = ~/.local/share/omarchy/default/hypr/bindings/clipboard.conf
source = ~/.local/share/omarchy/default/hypr/bindings/tiling-v2.conf
source = ~/.local/share/omarchy/default/hypr/bindings/utilities.conf
source = ~/.local/share/omarchy/default/hypr/envs.conf
source = ~/.local/share/omarchy/default/hypr/looknfeel.conf
source = ~/.local/share/omarchy/default/hypr/input.conf
source = ~/.local/share/omarchy/default/hypr/windows.conf
source = ~/.config/omarchy/current/theme/hyprland.conf
source = ~/.config/hypr/monitors.conf
source = ~/.config/hypr/input.conf
source = ~/.config/hypr/bindings.conf
source = ~/.config/hypr/looknfeel.conf
source = ~/.config/hypr/autostart.conf
source = ~/.local/state/omarchy/toggles/hypr/*.conf
source = ~/.config/hypr/ai-usage.conf
EOF

  local f
  for f in bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph; do
    printf '# fixture %s\n' "$f" >"$R/.config/hypr/$f.conf"
  done
  cat >"$R/.config/hypr/ai-usage.conf" <<'EOF'
windowrule = tag +floating-window, match:class ^(org.omarchy.ai-usage)$
windowrule = float on, match:class ^(org.omarchy.ai-usage)$
windowrule = center on, match:class ^(org.omarchy.ai-usage)$
windowrule = size 875 600, match:class ^(org.omarchy.ai-usage)$
EOF
  cat >"$R/.config/hypr/envs.conf" <<'EOF'
env = NVD_BACKEND,opengl
env = LIBVA_DRIVER_NAME,nvidia
env = __GLX_VENDOR_LIBRARY_NAME,nvidia
EOF
  cat >"$R/.local/state/omarchy/toggles/hypr/window-no-gaps.conf" <<'EOF'
general {
    gaps_out = 0
    gaps_in = 0
    border_size = 0
}
EOF

  for f in autostart.conf bindings/media.conf bindings/clipboard.conf \
           bindings/tiling-v2.conf bindings/utilities.conf envs.conf \
           looknfeel.conf input.conf windows.conf; do
    printf '# fixture default\n' >"$R/.local/share/omarchy/default/hypr/$f"
  done
  printf '# fixture theme include\n' >"$R/.config/omarchy/current/theme/hyprland.conf"
  printf 'matte-black\n' >"$R/.config/omarchy/current/theme.name"
  printf '# fixture theme bar css\n' >"$R/.config/omarchy/current/theme/waybar.css"

  cat >"$R/.config/waybar/config.jsonc" <<'EOF'
{
  // fixture comment: url-in-string must survive // stripping
  "reload_style_on_change": true,
  "layer": "top",
  "position": "top",
  "height": 26,
  "custom/fixture": { "exec": "echo http://example.invalid//x" },
}
EOF
  cat >"$R/.config/waybar/style.css" <<'EOF'
@import "../omarchy/current/theme/waybar.css";
* { background: @background; }
EOF

  cat >"$R/.config/walker/config.toml" <<'EOF'
force_keyboard_focus = true
selection_wrap = true
theme = "omarchy-default"
additional_theme_location = "~/.local/share/omarchy/default/walker/themes/"
hide_action_hints = true

[columns]
symbols = 1

[providers]
max_results = 256
EOF

  cat >"$R/.config/alacritty/alacritty.toml" <<'EOF'
general.import = [ "~/.config/omarchy/current/theme/alacritty.toml" ]

[font]
normal = { family = "JetBrainsMono Nerd Font", style = "Regular" }
size = 12.5

[window]
padding.x = 14
padding.y = 14
EOF
  cat >"$R/.config/foot/foot.ini" <<'EOF'
[main]
include=~/.config/omarchy/current/theme/foot.ini
font=JetBrainsMono Nerd Font:size=12.5
pad=14x14
EOF
  cat >"$R/.config/kitty/kitty.conf" <<'EOF'
include ~/.config/omarchy/current/theme/kitty.conf
font_size        12.5
window_padding_width 14
EOF
  cat >"$R/.config/ghostty/config" <<'EOF'
config-file = ?"~/.config/omarchy/current/theme/ghostty.conf"
font-size = 12.5
window-padding-x = 14
window-padding-y = 14
EOF
}

selftest() {
  local T BASH_BIN
  T=$(mktemp -d /tmp/w5-mado-m52-selftest.XXXXXX) || { echo "cannot mktemp" >&2; exit 2; }
  BASH_BIN="${BASH:-/bin/bash}"
  local A="$T/clean" B="$T/broken" SANDBOX="$T/nobin"
  local n_pass=0 n_fail=0
  declare -a failed=()
  st_ok() { n_pass=$((n_pass + 1)); }
  st_bad() { n_fail=$((n_fail + 1)); failed+=("$1"); }
  st_eq() { if [ "$2" = "$3" ]; then st_ok; else st_bad "$1 (got '$3' want '$2')"; fi; }
  st_has() { case "$2" in *"$3"*) st_ok ;; *) st_bad "$1 (missing: $3)" ;; esac; }
  st_not_has() { case "$2" in *"$3"*) st_bad "$1 (unexpected: $3)" ;; *) st_ok ;; esac; }
  st_rows() { # desc out status expected-count
    local n
    n=$(printf '%s\n' "$2" | awk -v s="$3" '/^(hypr|hypr-live|waybar|walker|terms|gate) / && $3==s {c++} END {print c+0}')
    st_eq "$1" "$4" "$n"
  }
  st_row_has() { # out id status
    if printf '%s\n' "$1" | awk -v i="$2" -v s="$3" '/^(hypr|hypr-live|waybar|walker|terms|gate) / && $2==i && $3==s {c++} END {exit (c+0>0)?0:1}'; then
      st_ok
    else
      st_bad "$4 (want row $2 $3)"
    fi
  }

  build_fixture "$A"

  # --- scenario A: clean fixture → CLEAN, exit 0, substrate untouched ------
  local before after out rc
  before=$(find "$A" -type f | sort | xargs sha256sum | sha256sum)
  out=$("$BASH_BIN" "$0" --root "$A" --no-live 2>&1); rc=$?
  after=$(find "$A" -type f | sort | xargs sha256sum | sha256sum)
  st_eq   "A: exit 0" 0 "$rc"
  st_has  "A: CLEAN verdict" "$out" "MADO_VERIFY: CLEAN"
  st_rows "A: zero FAIL rows" "$out" FAIL 0
  st_rows "A: zero UNKNOWN rows" "$out" UNKNOWN 0
  st_row_has "$out" hypr.root.include_graph PASS "A"
  st_row_has "$out" walker.config PASS "A"
  st_row_has "$out" waybar.config.reload_style PASS "A"
  st_row_has "$out" term.cross.font_size PASS "A"
  st_row_has "$out" boundary.readonly PASS "A"
  st_has  "A: scope names skipped live layer" "$out" "live layer skipped"
  st_eq   "A: fixture unchanged (read-only proof)" "$before" "$after"

  # --- scenario B: broken fixture → DIVERGED, exit 1, named FAIL rows ------
  mkdir -p "$B"
  cp -a "$A/." "$B/"
  printf 'exec-once = fixture-drift\n' >>"$B/.config/hypr/hyprland.conf"
  rm -f "$B/.config/hypr/xdph.conf"
  printf '{ "reload_style_on_change": ' >"$B/.config/waybar/config.jsonc"
  sed -i 's/force_keyboard_focus = true/force_keyboard_focus = false/' "$B/.config/walker/config.toml"
  out=$("$BASH_BIN" "$0" --root "$B" --no-live 2>&1); rc=$?
  st_eq   "B: exit 1" 1 "$rc"
  st_has  "B: DIVERGED verdict" "$out" "MADO_VERIFY: DIVERGED"
  st_row_has "$out" hypr.root.orchestrator FAIL "B"
  st_row_has "$out" hypr.local.inventory FAIL "B"
  st_row_has "$out" waybar.config.parse FAIL "B"
  st_row_has "$out" walker.config FAIL "B"
  st_row_has "$out" hypr.root.include_graph PASS "B (isolation)"
  st_not_has "B: no fake CLEAN" "$out" "MADO_VERIFY: CLEAN"

  # --- scenario C: live requested, no hyprctl → UNKNOWN blocks CLEAN -------
  mkdir -p "$SANDBOX"
  local c
  for c in bash grep sed awk cut head tail tr sort uniq wc find mktemp sha256sum \
           python3 ls cat rm cp mv mkdir printf dirname basename; do
    if have "$c"; then ln -sf "$(command -v "$c")" "$SANDBOX/$c"; fi
  done
  out=$(env PATH="$SANDBOX" MADO_VERIFY_LIVE=yes "$BASH_BIN" "$0" --root "$A" 2>&1); rc=$?
  st_eq   "C: exit 1" 1 "$rc"
  st_has  "C: DIVERGED verdict" "$out" "MADO_VERIFY: DIVERGED"
  st_row_has "$out" live.plane UNKNOWN "C (anti-claim)"
  st_has  "C: reason names unverifiable" "$out" "unverified"
  st_not_has "C: no fake CLEAN" "$out" "MADO_VERIFY: CLEAN"
  st_row_has "$out" hypr.root.include_graph PASS "C (file plane still judged)"

  # --- scenario D: usage contract ------------------------------------------
  out=$("$BASH_BIN" "$0" --help 2>&1); rc=$?
  st_eq  "D: --help exit 0" 0 "$rc"
  st_has "D: --help prints usage" "$out" "usage: mado-verify.sh"
  out=$("$BASH_BIN" "$0" --bogus 2>&1); rc=$?
  st_eq  "D: bad arg exit 2" 2 "$rc"

  if [ "$n_fail" = 0 ]; then
    rm -rf "$T"
    echo "MADO_SELFTEST: $n_pass/$n_pass assertions passed"
    return 0
  fi
  echo "MADO_SELFTEST: FAILED — $n_pass passed, $n_fail failed"
  for f in "${failed[@]}"; do echo "  - $f"; done
  echo "fixtures kept: $T"
  return 2
}

# ===========================================================================
# VERIFY — file plane + live plane
# (C/H are assigned in main, after argument parsing, so --root is honoured)
# ===========================================================================
live_skipped_reason=""

verify() {
  local before=""
  [ -d "$C" ] && before=$(boundary_hash "$C")

  # -------------------------------------------------------------------------
  # plane: hypr (file) — MADO-1 §1-§3, §7
  # -------------------------------------------------------------------------
  local f="$H/hyprland.conf"
  if [ -f "$f" ]; then
    local lc
    lc=$(wc -l <"$f")
    row hypr hypr.file.root PASS "hyprland.conf present ($lc L)"
  else
    row hypr hypr.file.root FAIL "missing: $H/hyprland.conf"
  fi

  if [ -f "$f" ]; then
    local off
    off=$(grep -nEv '^[[:space:]]*(#|$)|^[[:space:]]*source[[:space:]]*=' "$f" | head -3)
    if [ -z "$off" ]; then
      row hypr hypr.root.orchestrator PASS "0 settings lines (pure orchestrator)"
    else
      row hypr hypr.root.orchestrator FAIL "non-source lines: $(printf '%s' "$off" | tr '\n' ' ')"
    fi

    declare -a EXPECT=( \
      '~/.local/share/omarchy/default/hypr/autostart.conf' \
      '~/.local/share/omarchy/default/hypr/bindings/media.conf' \
      '~/.local/share/omarchy/default/hypr/bindings/clipboard.conf' \
      '~/.local/share/omarchy/default/hypr/bindings/tiling-v2.conf' \
      '~/.local/share/omarchy/default/hypr/bindings/utilities.conf' \
      '~/.local/share/omarchy/default/hypr/envs.conf' \
      '~/.local/share/omarchy/default/hypr/looknfeel.conf' \
      '~/.local/share/omarchy/default/hypr/input.conf' \
      '~/.local/share/omarchy/default/hypr/windows.conf' \
      '~/.config/omarchy/current/theme/hyprland.conf' \
      '~/.config/hypr/monitors.conf' \
      '~/.config/hypr/input.conf' \
      '~/.config/hypr/bindings.conf' \
      '~/.config/hypr/looknfeel.conf' \
      '~/.config/hypr/autostart.conf' \
      '~/.local/state/omarchy/toggles/hypr/*.conf' \
      '~/.config/hypr/ai-usage.conf' )
    local -a got=() miss=""
    mapfile -t got < <(awk '/^[[:space:]]*source[[:space:]]*=/{sub(/^[^=]*=[[:space:]]*/, ""); sub(/[[:space:]]+$/, ""); print}' "$f")
    local i
    if [ "${#got[@]}" -ne "${#EXPECT[@]}" ]; then
      row hypr hypr.root.include_graph FAIL "${#got[@]} source lines (expected ${#EXPECT[@]})"
    else
      for i in "${!EXPECT[@]}"; do
        if [ "${got[$i]}" != "${EXPECT[$i]}" ]; then
          miss="line $((i + 1)): got '${got[$i]}' want '${EXPECT[$i]}'"
          break
        fi
      done
      if [ -n "$miss" ]; then
        row hypr hypr.root.include_graph FAIL "$miss"
      else
        row hypr hypr.root.include_graph PASS "${#got[@]}/${#EXPECT[@]} sources, order exact"
      fi
    fi

    # every source target must resolve under $ROOT (~ expanded; globs ≥1 match)
    local t x tmiss=""
    for t in "${EXPECT[@]}"; do
      x="${t/#\~/$ROOT}"
      if [ -e "$x" ]; then continue; fi
      case "$x" in
        *'*'*) if compgen -G "$x" >/dev/null 2>&1; then continue; fi ;;
      esac
      tmiss="$tmiss $t"
    done
    if [ -z "$tmiss" ]; then
      row hypr hypr.root.sources_resolve PASS "${#EXPECT[@]}/${#EXPECT[@]} targets exist"
    else
      row hypr hypr.root.sources_resolve FAIL "unresolved:$tmiss"
    fi
  else
    row hypr hypr.root.orchestrator UNKNOWN "hyprland.conf missing"
    row hypr hypr.root.include_graph UNKNOWN "hyprland.conf missing"
    row hypr hypr.root.sources_resolve UNKNOWN "hyprland.conf missing"
  fi

  # 12 active local confs (MADO-1 §2)
  local -a LOCAL=(hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph)
  local n x lmiss=""
  n=0
  for x in "${LOCAL[@]}"; do
    if [ -f "$H/$x.conf" ]; then n=$((n + 1)); else lmiss="$lmiss $x.conf"; fi
  done
  if [ -z "$lmiss" ]; then
    row hypr hypr.local.inventory PASS "$n/${#LOCAL[@]} active local confs"
  else
    row hypr hypr.local.inventory FAIL "missing:$lmiss"
  fi

  # orphan invariant: local envs.conf sourced by nothing (MADO-1 §2; F3)
  if [ -f "$H/envs.conf" ]; then
    local src bad="" line
    src=$(grep -rnE '^[[:space:]]*source[[:space:]]*=' "$H" 2>/dev/null | grep 'envs\.conf' || true)
    while IFS= read -r line; do
      [ -z "$line" ] && continue
      case "$line" in
        *'default/hypr/envs.conf'*) : ;;
        *) bad="$bad $line" ;;
      esac
    done <<<"$src"
    local nenv
    nenv=$(grep -cE '^[[:space:]]*env[[:space:]]*=' "$H/envs.conf" || true)
    if [ -n "$bad" ]; then
      row hypr hypr.local.envs_orphan FAIL "local envs.conf is now sourced:$bad"
    else
      row hypr hypr.local.envs_orphan PASS "sourced by nothing; declares $nenv env vars (F3 stays open)"
    fi
  else
    row hypr hypr.local.envs_orphan UNKNOWN "envs.conf missing"
  fi

  # no-gaps toggle declares 0s (MADO-1 §7)
  local tog="$ROOT/.local/state/omarchy/toggles/hypr/window-no-gaps.conf"
  if [ -f "$tog" ]; then
    if grep -qE '^[[:space:]]*gaps_out[[:space:]]*=[[:space:]]*0' "$tog" \
       && grep -qE '^[[:space:]]*gaps_in[[:space:]]*=[[:space:]]*0' "$tog" \
       && grep -qE '^[[:space:]]*border_size[[:space:]]*=[[:space:]]*0' "$tog"; then
      row hypr hypr.toggle.no_gaps PASS "toggle declares gaps_in/gaps_out/border_size = 0"
    else
      row hypr hypr.toggle.no_gaps FAIL "toggle present but 0-invariants not all found"
    fi
  else
    row hypr hypr.toggle.no_gaps NOTE "toggle absent — gaps fall back to default looknfeel; live check judges"
  fi

  # record-level pins
  if [ -f "$f" ] && have sha256sum; then
    local sha
    sha=$(sha256sum "$f" | cut -c1-12)
    if [ "$sha" = "4f52854a3c14" ]; then
      row hypr hypr.file.sha_pin NOTE "hyprland.conf sha256 ${sha}… matches round-1 pin"
    else
      row hypr hypr.file.sha_pin NOTE "hyprland.conf sha256 ${sha}… drifted from round-1 pin 4f52854a3c14…; re-verify anchors"
    fi
  fi
  local nbak
  nbak=$(find "$H" -maxdepth 1 -name '*.bak*' 2>/dev/null | wc -l)
  row hypr hypr.backups NOTE "$nbak backup file(s) under ~/.config/hypr (S3 litter class)"

  # -------------------------------------------------------------------------
  # plane: hypr-live — hyprctl read verbs only (MADO-R2-1 §3/§5/§8)
  # -------------------------------------------------------------------------
  if [ "$LIVE" = 0 ]; then
    row hypr-live live.plane SKIP "live layer skipped ($live_skipped_reason) — file plane only"
  else
    live_plane
  fi

  # -------------------------------------------------------------------------
  # plane: waybar (file) — MADO-2 §2.1/§2.5
  # -------------------------------------------------------------------------
  local wb="$C/waybar/config.jsonc" wbjson=""
  if [ ! -f "$wb" ]; then
    row waybar waybar.config.parse FAIL "missing: $wb"
    row waybar waybar.config.reload_style UNKNOWN "config.jsonc missing"
    row waybar waybar.config.bar_globals UNKNOWN "config.jsonc missing"
  elif [ "$PY_OK" = 0 ]; then
    row waybar waybar.config.parse UNKNOWN "python3 not on PATH — cannot parse JSONC"
    row waybar waybar.config.reload_style UNKNOWN "python3 not on PATH"
    row waybar waybar.config.bar_globals UNKNOWN "python3 not on PATH"
  else
    wbjson=$(jsonc_parse "$wb" 2>/dev/null) || wbjson=""
    if [ -z "$wbjson" ]; then
      row waybar waybar.config.parse FAIL "JSONC parse failed: $(jsonc_parse "$wb" 2>&1 >/dev/null | head -1)"
      row waybar waybar.config.reload_style UNKNOWN "config.jsonc unparseable"
      row waybar waybar.config.bar_globals UNKNOWN "config.jsonc unparseable"
    else
      local wl wc
      wl=$(wc -l <"$wb"); wc=$(wc -c <"$wb")
      row waybar waybar.config.parse PASS "JSONC parses ($wl L, $wc B)"
      local det rc2
      det=$(json_expect "$wbjson" "reload_style_on_change" "true"); rc2=$?
      if [ "$rc2" = 0 ]; then
        row waybar waybar.config.reload_style PASS "reload_style_on_change = true (style reloads; modules need restart)"
      else
        row waybar waybar.config.reload_style FAIL "reload_style_on_change $det"
      fi
      local gbad=""
      det=$(json_expect "$wbjson" "layer" '"top"'); [ "$?" != 0 ] && gbad="$gbad layer($det)"
      det=$(json_expect "$wbjson" "position" '"top"'); [ "$?" != 0 ] && gbad="$gbad position($det)"
      det=$(json_expect "$wbjson" "height" "26"); [ "$?" != 0 ] && gbad="$gbad height($det)"
      if [ -z "$gbad" ]; then
        row waybar waybar.config.bar_globals PASS "layer=top, position=top, height=26"
      else
        row waybar waybar.config.bar_globals FAIL "globals drifted:$gbad"
      fi
    fi
  fi
  local wbs="$C/waybar/style.css"
  if [ -f "$wbs" ]; then
    if grep -q 'omarchy/current/theme/waybar.css' "$wbs"; then
      row waybar waybar.style PASS "style.css imports the theme css"
    else
      row waybar waybar.style FAIL "style.css does not import omarchy/current/theme/waybar.css"
    fi
  else
    row waybar waybar.style FAIL "missing: $wbs"
  fi

  # -------------------------------------------------------------------------
  # plane: walker (file) — MADO-2 §3
  # -------------------------------------------------------------------------
  local wk="$C/walker/config.toml"
  if [ ! -f "$wk" ]; then
    row walker walker.config FAIL "missing: $wk"
  elif [ "$PY_TOML" = 0 ]; then
    row walker walker.config UNKNOWN "python3 tomllib unavailable — cannot parse TOML"
  else
    local wdet wrc
    wdet=$(walker_check "$wk"); wrc=$?
    case "$wrc" in
      0) row walker walker.config PASS "TOML parses; $wdet" ;;
      4) row walker walker.config FAIL "TOML parse failed: $(walker_check "$wk" 2>&1 | head -1)" ;;
      *) row walker walker.config FAIL "TOML parses; $wdet" ;;
    esac
  fi

  # -------------------------------------------------------------------------
  # plane: terminals (file) — MADO-3 §1-§3, §5
  # -------------------------------------------------------------------------
  local al="$C/alacritty/alacritty.toml"
  if [ ! -f "$al" ]; then
    row terms term.alacritty.toml FAIL "missing: $al"
  elif [ "$PY_TOML" = 0 ]; then
    row terms term.alacritty.toml UNKNOWN "python3 tomllib unavailable — cannot parse TOML"
  else
    if python3 -c 'import tomllib,sys; tomllib.load(open(sys.argv[1],"rb"))' "$al" 2>/dev/null; then
      row terms term.alacritty.toml PASS "TOML parses"
    else
      row terms term.alacritty.toml FAIL "TOML parse failed"
    fi
  fi
  if [ -f "$al" ] && grep -q 'omarchy/current/theme/alacritty.toml' "$al"; then
    row terms term.alacritty.theme_import PASS "imports omarchy/current/theme/alacritty.toml"
  else
    row terms term.alacritty.theme_import FAIL "theme import missing"
  fi

  local tmiss="" tcount=0 tname tfile
  for tname in alacritty foot kitty ghostty; do
    case "$tname" in
      alacritty) tfile="$C/alacritty/alacritty.toml" ;;
      foot) tfile="$C/foot/foot.ini" ;;
      kitty) tfile="$C/kitty/kitty.conf" ;;
      ghostty) tfile="$C/ghostty/config" ;;
    esac
    [ -f "$tfile" ] && tcount=$((tcount + 1))
  done
  local term_size_ok=1 term_pad_ok=1
  [ -f "$C/alacritty/alacritty.toml" ] || term_size_ok=0
  local tf
  for tf in "alacritty:$C/alacritty/alacritty.toml" "foot:$C/foot/foot.ini" \
            "kitty:$C/kitty/kitty.conf" "ghostty:$C/ghostty/config"; do
    tname="${tf%%:*}"; tfile="${tf#*:}"
    [ -f "$tfile" ] || continue
    case "$tname" in
      alacritty)
        grep -qE '^[[:space:]]*size[[:space:]]*=[[:space:]]*12\.5' "$tfile" || { term_size_ok=0; tmiss="$tmiss alacritty"; }
        grep -qE '^[[:space:]]*padding\.x[[:space:]]*=[[:space:]]*14' "$tfile" \
          && grep -qE '^[[:space:]]*padding\.y[[:space:]]*=[[:space:]]*14' "$tfile" || { term_pad_ok=0; }
        ;;
      foot)
        grep -qE 'size=12\.5' "$tfile" || { term_size_ok=0; tmiss="$tmiss foot"; }
        grep -qE 'pad=14x14' "$tfile" || { term_pad_ok=0; }
        ;;
      kitty)
        grep -qE 'font_size[[:space:]]+12\.5' "$tfile" || { term_size_ok=0; tmiss="$tmiss kitty"; }
        grep -qE 'window_padding_width[[:space:]]+14' "$tfile" || { term_pad_ok=0; }
        ;;
      ghostty)
        grep -qE '^[[:space:]]*font-size[[:space:]]*=[[:space:]]*12\.5' "$tfile" || { term_size_ok=0; tmiss="$tmiss ghostty"; }
        grep -qE '^[[:space:]]*window-padding-x[[:space:]]*=[[:space:]]*14' "$tfile" \
          && grep -qE '^[[:space:]]*window-padding-y[[:space:]]*=[[:space:]]*14' "$tfile" || { term_pad_ok=0; }
        ;;
    esac
  done
  if [ "$term_size_ok" = 1 ]; then
    row terms term.cross.font_size PASS "12.5 in all $tcount present configs (MADO-3 §3)"
  else
    row terms term.cross.font_size FAIL "size 12.5 not found:$tmiss${tcount:+ }"
  fi
  if [ "$term_pad_ok" = 1 ]; then
    row terms term.cross.padding PASS "padding 14 on both axes in all $tcount present configs"
  else
    row terms term.cross.padding FAIL "padding 14 pattern missing in at least one present config"
  fi

  # -------------------------------------------------------------------------
  # boundary proof row (SKILL safety rule 3)
  # -------------------------------------------------------------------------
  if [ -d "$C" ] && [ -n "$before" ]; then
    local after
    after=$(boundary_hash "$C")
    if [ "$after" = "$before" ]; then
      row gate boundary.readonly PASS "config plane byte-identical before/after (combined sha ${before:0:12}…)"
    else
      row gate boundary.readonly FAIL "config plane changed during the run — investigate immediately"
    fi
  else
    row gate boundary.readonly SKIP "no $C tree to hash"
  fi
}

# ---------------------------------------------------------------------------
# live plane (read verbs only; every unverifiable surface reads UNKNOWN)
# ---------------------------------------------------------------------------
live_plane() {
  local reason=""
  if ! have hyprctl; then reason="hyprctl not on PATH"; fi
  if [ -z "$reason" ] && [ -z "${HYPRLAND_INSTANCE_SIGNATURE:-}" ]; then
    reason="HYPRLAND_INSTANCE_SIGNATURE unset — session target unknown (no guessing, MADO-R2-1 §8)"
  fi
  if [ -z "$reason" ]; then
    local v rc
    v=$(tmo hyprctl version 2>&1); rc=$?
    [ "$rc" != 0 ] && reason="hyprctl cannot reach the compositor (rc=$rc)"
  fi
  if [ -n "$reason" ]; then
    row hypr-live live.plane UNKNOWN "$reason; live checks unverified — verdict cannot be CLEAN"
    return
  fi

  # version pin: Hyprland 0.56.2 / commit efb5099… (SKILL "Version pins")
  local v
  v=$(tmo hyprctl version 2>/dev/null | head -1)
  if printf '%s' "$v" | grep -q 'Hyprland 0\.56\.2' && printf '%s' "$v" | grep -q 'efb50993780079460b0cbed1363e2166a2de1d9f'; then
    row hypr-live live.hypr.version PASS "Hyprland 0.56.2 efb5099… (pin matches)"
  else
    row hypr-live live.hypr.version FAIL "pin changed: $(printf '%s' "$v" | cut -c1-80); re-verify claim anchors"
  fi

  # instance target unambiguous
  local inst n
  inst=$(tmo hyprctl -j instances 2>/dev/null)
  if [ "$PY_OK" = 0 ]; then
    row hypr-live live.hypr.instances UNKNOWN "python3 not on PATH"
  else
    n=$(printf '%s' "$inst" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null) || n=""
    case "$n" in
      '') row hypr-live live.hypr.instances UNKNOWN "cannot parse hyprctl -j instances" ;;
      *[!0-9]*) row hypr-live live.hypr.instances UNKNOWN "cannot parse hyprctl -j instances (got '$n')" ;;
      *)
        if [ "$n" = 1 ]; then
          row hypr-live live.hypr.instances PASS "1 instance (target unambiguous)"
        elif [ "$n" -gt 1 ]; then
          row hypr-live live.hypr.instances PASS "$n instances; targeting the session's own signature (no guessing)"
        else
          row hypr-live live.hypr.instances FAIL "0 instances"
        fi
        ;;
    esac
  fi

  # load health
  local ce crc
  ce=$(tmo hyprctl configerrors 2>&1); crc=$?
  if [ "$crc" != 0 ]; then
    row hypr-live live.hypr.configerrors FAIL "rc=$crc: $(printf '%s' "$ce" | head -1)"
  elif [ -n "$ce" ]; then
    row hypr-live live.hypr.configerrors FAIL "non-empty: $(printf '%s' "$ce" | head -1)"
  else
    row hypr-live live.hypr.configerrors PASS "empty (config loads clean)"
  fi

  local j det

  # gaps_out = 0 0 0 0 (toggle owns; MADO-1 §7)
  j=$(tmo hyprctl -j getoption general:gaps_out 2>/dev/null)
  if [ "$PY_OK" = 0 ]; then
    row hypr-live live.hypr.gaps_out UNKNOWN "python3 not on PATH"
  else
    det=$(printf '%s' "$j" | python3 -c "import json,sys; d=json.load(sys.stdin); print('custom=%r set=%s' % (d.get('custom'), d.get('set'))); sys.exit(0 if (d.get('custom')=='0 0 0 0' and d.get('set') is True) else 5)" 2>/dev/null); rc=$?
    row_from_rc hypr-live live.hypr.gaps_out "$det" "$rc"
  fi

  # kb_layout = br (local input.conf owns)
  j=$(tmo hyprctl -j getoption input:kb_layout 2>/dev/null)
  if [ "$PY_OK" = 0 ]; then
    row hypr-live live.hypr.kb_layout UNKNOWN "python3 not on PATH"
  else
    det=$(printf '%s' "$j" | python3 -c "import json,sys; d=json.load(sys.stdin); print('str=%r set=%s' % (d.get('str'), d.get('set'))); sys.exit(0 if d.get('str')=='br' else 5)" 2>/dev/null); rc=$?
    row_from_rc hypr-live live.hypr.kb_layout "$det" "$rc"
  fi

  # zero chrome: border_size 0 + rounding 0
  if [ "$PY_OK" = 0 ]; then
    row hypr-live live.hypr.zero_chrome UNKNOWN "python3 not on PATH"
  else
    local bsz rd
    j=$(tmo hyprctl -j getoption general:border_size 2>/dev/null)
    bsz=$(printf '%s' "$j" | python3 -c "import json,sys; print(json.load(sys.stdin).get('int'))" 2>/dev/null)
    j=$(tmo hyprctl -j getoption decoration:rounding 2>/dev/null)
    rd=$(printf '%s' "$j" | python3 -c "import json,sys; print(json.load(sys.stdin).get('int'))" 2>/dev/null)
    if [ "$bsz" = 0 ] && [ "$rd" = 0 ]; then
      row hypr-live live.hypr.zero_chrome PASS "border_size=0, rounding=0 (toggle/style owns)"
    else
      row hypr-live live.hypr.zero_chrome FAIL "border_size=$bsz rounding=$rd (want 0/0)"
    fi
  fi

  # animations on
  j=$(tmo hyprctl -j getoption animations:enabled 2>/dev/null)
  if [ "$PY_OK" = 0 ]; then
    row hypr-live live.hypr.animations UNKNOWN "python3 not on PATH"
  else
    det=$(printf '%s' "$j" | python3 -c "import json,sys; d=json.load(sys.stdin); print('enabled=%s' % d.get('int')); sys.exit(0 if d.get('int')==1 else 5)" 2>/dev/null); rc=$?
    row_from_rc hypr-live live.hypr.animations "$det" "$rc"
  fi

  # binds count = 192 (arithmetic closes per MADO-1 §4)
  local binds
  binds=$(tmo hyprctl -j binds 2>/dev/null)
  if [ "$PY_OK" = 0 ]; then
    row hypr-live live.hypr.binds_count UNKNOWN "python3 not on PATH"
  else
    n=$(printf '%s' "$binds" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null) || n=""
    if [ -z "$n" ]; then
      row hypr-live live.hypr.binds_count UNKNOWN "cannot parse hyprctl -j binds"
    elif [ "$n" = 192 ]; then
      row hypr-live live.hypr.binds_count PASS "192 binds (file arithmetic closes)"
    else
      row hypr-live live.hypr.binds_count FAIL "$n binds (expected 192 — re-run the per-file arithmetic)"
    fi
  fi

  # DP-1 3440x1440@~100
  local mon
  mon=$(tmo hyprctl -j monitors 2>/dev/null)
  if [ "$PY_OK" = 0 ]; then
    row hypr-live live.hypr.monitor_dp1 UNKNOWN "python3 not on PATH"
  else
    det=$(printf '%s' "$mon" | python3 -c "
import json, sys
d = json.load(sys.stdin)
m = [x for x in d if x.get('name') == 'DP-1']
if not m:
    print('DP-1 absent'); sys.exit(5)
x = m[0]
ok = (x.get('width') == 3440 and x.get('height') == 1440 and abs(float(x.get('refreshRate', 0)) - 100) < 0.5)
print('DP-1 %sx%s@%s' % (x.get('width'), x.get('height'), x.get('refreshRate')))
sys.exit(0 if ok else 5)
" 2>/dev/null); rc=$?
    row_from_rc hypr-live live.hypr.monitor_dp1 "$det" "$rc"
  fi

  # touchpad scroll_factor 0.4 (MADO-1 §7)
  j=$(tmo hyprctl -j getoption input:touchpad:scroll_factor 2>/dev/null)
  if [ "$PY_OK" = 0 ]; then
    row hypr-live live.hypr.scroll_factor UNKNOWN "python3 not on PATH"
  else
    det=$(printf '%s' "$j" | python3 -c "import json,sys; d=json.load(sys.stdin); v=float(d.get('float', -1)); print('scroll_factor=%s' % d.get('float')); sys.exit(0 if abs(v-0.4)<0.0001 else 5)" 2>/dev/null); rc=$?
    row_from_rc hypr-live live.hypr.scroll_factor "$det" "$rc"
  fi

  # idle consumer (F1/S1 open finding; record-level row)
  if ! have pgrep; then
    row hypr-live live.consumer.hypridle UNKNOWN "pgrep not on PATH"
  elif pgrep -x hypridle >/dev/null 2>&1; then
    row hypr-live live.consumer.hypridle PASS "hypridle running (idle chain has a consumer)"
  else
    row hypr-live live.consumer.hypridle NOTE "hypridle absent — declared 150s/152s idle chain has no consumer (F1, S1; operator-owned)"
  fi

  # env probes — GDK_SCALE=1 (sourced default envs.conf path chain) / orphan NVD unset
  if ! have printenv; then
    row hypr-live live.env.gdk_scale UNKNOWN "printenv not on PATH"
    row hypr-live live.env.nvd_backend UNKNOWN "printenv not on PATH"
  else
    local gdk grc nvd nrc
    gdk=$(printenv GDK_SCALE 2>/dev/null); grc=$?
    if [ "$grc" = 0 ] && [ "$gdk" = 1 ]; then
      row hypr-live live.env.gdk_scale PASS "GDK_SCALE=1"
    else
      row hypr-live live.env.gdk_scale FAIL "GDK_SCALE='${gdk:-<unset>}' (rc=$grc; want 1)"
    fi
    nvd=$(printenv NVD_BACKEND 2>/dev/null); nrc=$?
    if [ "$nrc" != 0 ]; then
      row hypr-live live.env.nvd_backend PASS "NVD_BACKEND unset (orphan envs.conf effect provably absent, F3)"
    else
      row hypr-live live.env.nvd_backend FAIL "NVD_BACKEND is set ('$nvd') — re-check the envs.conf routing"
    fi
  fi

  # waybar version pin / process / layer surface / tray watcher
  if ! have waybar; then
    row hypr-live live.waybar.version FAIL "waybar not on PATH (declared bar consumer absent)"
  else
    local wv
    wv=$(tmo waybar --version 2>/dev/null | head -1)
    if [ "$wv" = "Waybar v0.15.0" ]; then
      row hypr-live live.waybar.version PASS "Waybar v0.15.0 (pin matches)"
    else
      row hypr-live live.waybar.version FAIL "pin changed: '$wv'; re-verify claim anchors"
    fi
  fi
  local wpid=""
  if ! have pgrep; then
    row hypr-live live.waybar.process UNKNOWN "pgrep not on PATH"
  else
    wpid=$(pgrep -x waybar 2>/dev/null | head -1)
    if [ -n "$wpid" ]; then
      row hypr-live live.waybar.process PASS "waybar pid $wpid"
    else
      row hypr-live live.waybar.process FAIL "no waybar process"
    fi
  fi
  local layers
  layers=$(tmo hyprctl -j layers 2>/dev/null)
  if [ "$PY_OK" = 0 ]; then
    row hypr-live live.waybar.layer UNKNOWN "python3 not on PATH"
  elif [ -z "$layers" ]; then
    row hypr-live live.waybar.layer UNKNOWN "hyprctl -j layers returned nothing"
  else
    det=$(printf '%s' "$layers" | python3 -c "
import json, sys
d = json.load(sys.stdin)
want = sys.argv[1] if len(sys.argv) > 1 else ''
found = []
for mon, mm in (d.items() if isinstance(d, dict) else []):
    for lvl, surfs in ((mm.get('levels') or {}).items()):
        for s in (surfs or []):
            if s.get('namespace') == 'waybar':
                found.append((mon, lvl, s.get('pid'), s.get('w'), s.get('h')))
if not found:
    print('no waybar layer surface'); sys.exit(5)
mon, lvl, pid, w, h = found[0]
if want and str(pid) != str(want):
    print('layer pid %s != waybar process %s' % (pid, want)); sys.exit(5)
print('%s level %s pid %s %sx%s' % (mon, lvl, pid, w, h)); sys.exit(0)
" "$wpid" 2>/dev/null); rc=$?
    row_from_rc hypr-live live.waybar.layer "$det" "$rc"
  fi
  if ! have busctl; then
    row hypr-live live.waybar.tray UNKNOWN "busctl not on PATH"
  else
    local tray trc
    tray=$(tmo busctl --user get-property fr.arouillard.waybar /StatusNotifierWatcher org.kde.StatusNotifierWatcher RegisteredStatusNotifierItems 2>/dev/null); trc=$?
    if [ "$trc" = 0 ]; then
      row hypr-live live.waybar.tray PASS "tray watcher answers: $tray"
    else
      row hypr-live live.waybar.tray FAIL "tray watcher query failed (rc=$trc)"
    fi
  fi

  # walker: version pin + services (MADO-R3-1 §1/§6)
  if ! have walker; then
    row hypr-live live.walker.version FAIL "walker not on PATH (declared launcher absent)"
  else
    local kv
    kv=$(tmo walker --version 2>/dev/null | head -1)
    if [ "$kv" = "2.17.0" ]; then
      row hypr-live live.walker.version PASS "2.17.0 (pin matches)"
    else
      row hypr-live live.walker.version FAIL "pin changed: '$kv'; re-verify claim anchors"
    fi
  fi
  if ! have systemctl; then
    row hypr-live live.walker.services UNKNOWN "systemctl not on PATH"
  else
    local wa el
    wa=$(tmo systemctl --user is-active app-walker@autostart.service 2>/dev/null || true)
    el=$(tmo systemctl --user is-active elephant.service 2>/dev/null || true)
    if [ "$wa" = active ] && [ "$el" = active ]; then
      row hypr-live live.walker.services PASS "app-walker@autostart + elephant active"
    else
      row hypr-live live.walker.services FAIL "app-walker='$wa' elephant='$el' (want active/active)"
    fi
  fi

  # theme: record-level only (operator-owned)
  if ! have omarchy; then
    row hypr-live live.theme.current NOTE "omarchy not on PATH — theme not read"
  else
    local tc
    tc=$(tmo omarchy theme current 2>/dev/null | head -1)
    row hypr-live live.theme.current NOTE "omarchy theme current → '${tc:-<empty>}' (operator-owned; not a verdict input)"
  fi
}

# ===========================================================================
# main
# ===========================================================================
while [ "$#" -gt 0 ]; do
  case "$1" in
    --selftest) MODE=selftest ;;
    --no-live) LIVE_REQ=no ;;
    --live) LIVE_REQ=yes ;;
    --root) shift; [ "$#" -gt 0 ] || { echo "usage error: --root needs a directory" >&2; exit 2; }; ROOT="$1" ;;
    --root=*) ROOT="${1#--root=}" ;;
    -h | --help) usage; exit 0 ;;
    *) echo "usage error: unknown argument '$1'" >&2; usage >&2; exit 2 ;;
  esac
  shift
done
ROOT="${ROOT%/}"; [ -n "$ROOT" ] || ROOT=/

if [ "$MODE" = selftest ]; then
  selftest
  exit $?
fi

case "$LIVE_REQ" in
  auto)
    if [ "$ROOT" = "$HOME" ]; then LIVE=1; live_skipped_reason=""; else LIVE=0; live_skipped_reason="non-home root"; fi
    ;;
  yes) LIVE=1 ;;
  no) LIVE=0; live_skipped_reason="--no-live" ;;
  *) echo "usage error: MADO_VERIFY_LIVE must be auto|yes|no" >&2; exit 2 ;;
esac

C="$ROOT/.config"
H="$C/hypr"

verify

# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------
printf '%s\n' "$VERSION_STR"
if [ "$LIVE" = 1 ]; then
  printf 'mode: live (read-only) | root: %s | hyprctl: %s\n' "$ROOT" "$(have hyprctl && echo yes || echo no)"
else
  printf 'mode: file-plane only | root: %s | live layer: skipped (%s)\n' "$ROOT" "$live_skipped_reason"
fi
printf '%-9s %-31s %-7s %s\n' "plane" "check" "status" "detail"
local_ifs_save="$IFS"
for r in "${ROWS[@]}"; do
  IFS='|' read -r p i s d <<<"$r"
  printf '%-9s %-31s %-7s %s\n' "$p" "$i" "$s" "$d"
done
IFS="$local_ifs_save"

first_fail=""; first_unk=""
for r in "${ROWS[@]}"; do
  IFS='|' read -r p i s d <<<"$r"
  if [ "$s" = FAIL ] && [ -z "$first_fail" ]; then first_fail="$i ($d)"; fi
  if [ "$s" = UNKNOWN ] && [ -z "$first_unk" ]; then first_unk="$i ($d)"; fi
done

printf 'counts: pass=%s fail=%s unknown=%s skip=%s note=%s\n' "$PASS" "$FAIL" "$UNKNOWN" "$SKIP" "$NOTE"

if [ "$FAIL" = 0 ] && [ "$UNKNOWN" = 0 ]; then
  if [ "$LIVE" = 0 ]; then
    printf 'MADO_VERIFY: CLEAN (%s pass, %s notes; file plane only — live layer skipped: %s)\n' "$PASS" "$NOTE" "$live_skipped_reason"
  else
    printf 'MADO_VERIFY: CLEAN (%s pass, %s notes; file + live planes verified read-only)\n' "$PASS" "$NOTE"
  fi
  exit 0
fi

reason=""
[ "$FAIL" != 0 ] && reason="first fail: $first_fail"
[ -z "$reason" ] && reason="unverifiable: $first_unk"
printf 'MADO_VERIFY: DIVERGED (%s fail, %s unknown, %s pass) — %s\n' "$FAIL" "$UNKNOWN" "$PASS" "$reason"
exit 1