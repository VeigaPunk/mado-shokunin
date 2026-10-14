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
  st_row_detail() { # out id status substr desc
    if printf '%s\n' "$1" | awk -v i="$2" -v s="$3" -v t="$4" '$2==i && $3==s && index($0,t) {c++} END {exit (c+0>0)?0:1}'; then
      st_ok
    else
      st_bad "$5 (want row $2 $3 containing '$4')"
    fi
  }
  st_counts_agree() { # out desc — the report counts must equal the row table
    local np nf nu ns nn
    np=$(printf '%s\n' "$1" | awk '/^(hypr|hypr-live|waybar|walker|terms|gate) / && $3=="PASS" {c++} END {print c+0}')
    nf=$(printf '%s\n' "$1" | awk '/^(hypr|hypr-live|waybar|walker|terms|gate) / && $3=="FAIL" {c++} END {print c+0}')
    nu=$(printf '%s\n' "$1" | awk '/^(hypr|hypr-live|waybar|walker|terms|gate) / && $3=="UNKNOWN" {c++} END {print c+0}')
    ns=$(printf '%s\n' "$1" | awk '/^(hypr|hypr-live|waybar|walker|terms|gate) / && $3=="SKIP" {c++} END {print c+0}')
    nn=$(printf '%s\n' "$1" | awk '/^(hypr|hypr-live|waybar|walker|terms|gate) / && $3=="NOTE" {c++} END {print c+0}')
    st_has "$2" "$1" "counts: pass=$np fail=$nf unknown=$nu skip=$ns note=$nn"
  }

  # >>> MADO-R7-SELFTEST-BLOCK >>>
  # --- scenario R: the --regression engine ---------------------------------
  # Hermetic: every case below runs against a stub runner honouring tameshi's
  # evidence contract (results.tsv + sweep.log verdict lines) written into the
  # fixture, so no sibling-repo tool and no substrate is read. The real harness
  # integration is a separate, measured step (the mode's own end-to-end run).
  local RF="$T/regression" RG="$T/regression/cases" st_rg o1 dsha
  local RTGT="$T/regression/target.sh" RSPEC="$T/regression/spec.spec"
  mkdir -p "$RF" "$RG"
  printf '#!/bin/bash\nexit 0\n' >"$RTGT"
  printf '@defect K1 | fixture\n@old exit 0\n@new exit 1\n' >"$RSPEC"
  cat >"$RF/runner-stub.sh" <<'MADO_R7_STUB_EOF'
#!/bin/bash
# stub of tameshi's mutate-and-run.sh: same evidence contract, fixture verdicts
wd=''
while [ "$#" -gt 0 ]; do
  case "$1" in
    --workdir) shift; wd="$1" ;;
    --label | --target | --defects | --suite) shift ;;
  esac
  shift
done
[ -n "$wd" ] || exit 64
mkdir -p "$wd" || exit 2
rows="${STUB_ROWS:-}"
k=0; s=0; i=0
printf 'CONTROL: %s (exit=0 duration-ms=1 pristine-sha256=stub)\n' "${STUB_CONTROL:-GREEN}"
printf 'MUTATE_RESTORE: %s (target-sha256 before=stub after=stub pristine-sha256=stub)\n' "${STUB_RESTORE:-OK}"
printf 'id\tverdict\texit\tduration-ms\tmutant-sha256\tdesc\n' >"$wd/results.tsv"
if [ -n "$rows" ] && [ -f "$rows" ]; then
  while IFS="$(printf '\t')" read -r id v; do
    [ -n "$id" ] || continue
    printf '%s\t%s\t1\t1\tstub\tstub\n' "$id" "$v" >>"$wd/results.tsv"
    case "$v" in KILLED) k=$((k + 1)) ;; SURVIVED) s=$((s + 1)) ;; *) i=$((i + 1)) ;; esac
  done <"$rows"
fi
printf 'MUTATE: DONE (target=stub defects=%s killed=%s survived=%s inconclusive=%s kill-rate=0%%)\n' \
  "$((k + s + i))" "$k" "$s" "$i"
exit "${STUB_EXIT:-0}"
MADO_R7_STUB_EOF
  chmod +x "$RF/runner-stub.sh"
  printf 'D1\tKILLED\nD2\tKILLED\n' >"$RF/all-killed.tsv"
  printf 'D1\tSURVIVED\nD2\tKILLED\n' >"$RF/one-survivor.tsv"
  printf 'D1\tKILLED\nD2\tKILLED\nD3\tKILLED\n' >"$RF/extra-id.tsv"
  printf 'D1\tKILLED\n' >"$RF/missing-id.tsv"
  printf 'D1\tKILLED\nD2\tINCONCLUSIVE\n' >"$RF/inconclusive.tsv"
  local RTABLE='D1:KILLED,D2:KILLED' RSUITE='bash "$MUTANT" --selftest'
  REGRESSION_RUNNER="$RF/runner-stub.sh"
  export STUB_CONTROL=GREEN STUB_RESTORE=OK STUB_EXIT=0 STUB_ROWS="$RF/all-killed.tsv"

  regression_case fixture "$RTGT" "$(mado_r7_sha "$RTGT")" "$RSPEC" "$RSUITE" "$RTABLE" \
    "$RG/pass" >"$RF/out1" 2>&1
  st_rg=$?
  o1=$(cat "$RF/out1")
  st_eq  "R1: in-band fixture PASSes (exit 0)" 0 "$st_rg"
  st_has "R1: PASS line names the reproduced table" "$o1" \
    "REGRESSION_CASE fixture: PASS (recorded table reproduced: killed=2/2 flips=0 inconclusive=0 control=green restore=ok)"
  st_has "R1: table line" "$o1" \
    "REGRESSION_TABLE fixture: match=2/2 recorded-killed=2 measured-killed=2 survived=0 inconclusive=0 flips=0"

  export STUB_ROWS="$RF/one-survivor.tsv"
  regression_case fixture "$RTGT" "$(mado_r7_sha "$RTGT")" "$RSPEC" "$RSUITE" "$RTABLE" \
    "$RG/doctored" >"$RF/out2" 2>&1
  st_rg=$?
  o1=$(cat "$RF/out2")
  st_eq  "R2: a lost kill FAILs the fixture (exit 1)" 1 "$st_rg"
  st_has "R2: differing row named with both verdicts" "$o1" \
    "REGRESSION_DEFECT fixture D1: measured=SURVIVED recorded=KILLED"
  st_has "R2: FAIL line" "$o1" "REGRESSION_CASE fixture: FAIL (out of band:"
  st_has "R2: measured flips reported" "$o1" "flips=1"

  regression_case fixture "$RTGT" \
    0000000000000000000000000000000000000000000000000000000000000000 \
    "$RSPEC" "$RSUITE" "$RTABLE" "$RG/pinmismatch" >"$RF/out3" 2>&1
  st_rg=$?
  o1=$(cat "$RF/out3")
  st_eq  "R3: pin mismatch is SETUP (exit 2)" 2 "$st_rg"
  st_has "R3: SETUP names recorded and live sha" "$o1" \
    "REGRESSION_CASE fixture: SETUP (pin mismatch: recorded=000000000000"
  if [ ! -e "$RG/pinmismatch" ]; then
    st_ok
  else
    st_bad "R3: refused before any sweep run (case workdir was created)"
  fi

  regression_case fixture "$RF/no-such-target" \
    0000000000000000000000000000000000000000000000000000000000000000 \
    "$RSPEC" "$RSUITE" "$RTABLE" "$RG/notarget" >"$RF/out4" 2>&1
  st_rg=$?
  o1=$(cat "$RF/out4")
  st_eq  "R4: missing target is SETUP (exit 2)" 2 "$st_rg"
  st_has "R4: SETUP names the missing target" "$o1" "SETUP (target missing:"

  export STUB_ROWS="$RF/extra-id.tsv"
  regression_case fixture "$RTGT" "$(mado_r7_sha "$RTGT")" "$RSPEC" "$RSUITE" "$RTABLE" \
    "$RG/extra" >"$RF/out5" 2>&1
  st_rg=$?
  o1=$(cat "$RF/out5")
  st_eq  "R5: an unrecorded measured row FAILs (exit 1)" 1 "$st_rg"
  st_has "R5: unrecorded row named" "$o1" "REGRESSION_DEFECT fixture D3: measured=KILLED recorded=ABSENT"
  st_has "R5: FAIL line carries the defect count" "$o1" "defects=3-recorded=2"

  export STUB_ROWS="$RF/missing-id.tsv"
  regression_case fixture "$RTGT" "$(mado_r7_sha "$RTGT")" "$RSPEC" "$RSUITE" "$RTABLE" \
    "$RG/missing" >"$RF/out6" 2>&1
  st_rg=$?
  o1=$(cat "$RF/out6")
  st_eq  "R6: a missing recorded row FAILs (exit 1)" 1 "$st_rg"
  st_has "R6: absent row named" "$o1" "REGRESSION_DEFECT fixture D2: measured=ABSENT recorded=KILLED"

  export STUB_ROWS="$RF/all-killed.tsv" STUB_CONTROL=RED
  regression_case fixture "$RTGT" "$(mado_r7_sha "$RTGT")" "$RSPEC" "$RSUITE" "$RTABLE" \
    "$RG/ctlred" >"$RF/out7" 2>&1
  st_rg=$?
  o1=$(cat "$RF/out7")
  st_eq  "R7: a red control FAILs (exit 1)" 1 "$st_rg"
  st_has "R7: reason names the control" "$o1" "control-not-green"
  export STUB_CONTROL=GREEN

  export STUB_RESTORE=DRIFT
  regression_case fixture "$RTGT" "$(mado_r7_sha "$RTGT")" "$RSPEC" "$RSUITE" "$RTABLE" \
    "$RG/drift" >"$RF/out8" 2>&1
  st_rg=$?
  o1=$(cat "$RF/out8")
  st_eq  "R8: a restore drift FAILs (exit 1)" 1 "$st_rg"
  st_has "R8: reason names the restore proof" "$o1" "restore-not-ok"
  export STUB_RESTORE=OK

  export STUB_ROWS="$RF/inconclusive.tsv" STUB_EXIT=1
  regression_case fixture "$RTGT" "$(mado_r7_sha "$RTGT")" "$RSPEC" "$RSUITE" "$RTABLE" \
    "$RG/inconcl" >"$RF/out9" 2>&1
  st_rg=$?
  o1=$(cat "$RF/out9")
  st_eq  "R9: an inconclusive row FAILs (exit 1)" 1 "$st_rg"
  st_has "R9: reason names the inconclusive count" "$o1" "inconclusive=1"
  export STUB_EXIT=0

  if mado_r7_target_build "$0" "$RF/derived.sh"; then
    dsha=$(mado_r7_sha "$RF/derived.sh")
  else
    dsha='build-failed'
  fi
  if [ "${DEFECT_ID:-}" = '' ] || [ "${DEFECT_ID:-}" = CONTROL ]; then
    st_eq "R10: derived target equals the recorded gate revision" "$PIN_MADO" "$dsha"
  else
    if [ "$dsha" != "$PIN_MADO" ]; then
      st_ok
    else
      st_bad "R10: a defected gate must not equal the recorded revision"
    fi
  fi

  mado_r7_spec_write "$RF/spec.written"
  st_eq "R11: the embedded spec is byte-identical to the recorded case" "$SPEC_SHA" \
    "$(mado_r7_sha "$RF/spec.written")"
  st_eq "R11: the embedded spec carries the ten recorded defects" 10 \
    "$(grep -c '^@defect ' "$RF/spec.written")"

  o1=$(env MADO_VERIFY_HARNESS="$T/no-harness" "$BASH_BIN" "$0" --regression --target "$RTGT" 2>&1)
  st_rg=$?
  st_eq  "R12: --regression --target is a usage error (exit 2)" 2 "$st_rg"
  st_has "R12: the refusal names the flag" "$o1" "usage error: --regression takes no --target"
  o1=$(env MADO_VERIFY_HARNESS="$T/no-harness" "$BASH_BIN" "$0" --regression --defects=x 2>&1)
  st_rg=$?
  st_eq  "R12: --regression --defects= is a usage error (exit 2)" 2 "$st_rg"
  o1=$(env MADO_VERIFY_HARNESS="$T/no-harness" "$BASH_BIN" "$0" --regression --bogus 2>&1)
  st_rg=$?
  st_eq  "R12: an unknown argument with --regression is refused (exit 2)" 2 "$st_rg"
  o1=$(env MADO_VERIFY_HARNESS="$T/no-harness" "$BASH_BIN" "$0" --regression --help 2>&1)
  st_rg=$?
  st_eq  "R12: --regression --help exits 0" 0 "$st_rg"
  st_has "R12: --regression --help prints the usage" "$o1" "usage: mado-verify.sh"
  st_has "R12: --regression --help documents the mode" "$o1" "--regression  replay the recorded mutation case"

  o1=$(env MADO_VERIFY_HARNESS="$T/no-harness" "$BASH_BIN" "$0" --regression 2>&1)
  st_rg=$?
  st_eq  "R13: a missing harness is SETUP (exit 2)" 2 "$st_rg"
  st_has "R13: the SETUP names the harness" "$o1" "MADO_REGRESSION: SETUP (mutation harness not found:"
  st_not_has "R13: regression mode never prints a MADO_VERIFY verdict" "$o1" "MADO_VERIFY:"
  # <<< MADO-R7-SELFTEST-BLOCK <<<
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
  st_row_has "$out" live.plane SKIP "A (live layer not executed)"
  local shaf
  shaf=$(sha256sum "$A/.config/hypr/hyprland.conf" | cut -c1-12)
  st_row_detail "$out" hypr.file.sha_pin NOTE "sha256 ${shaf}…" "A: sha pin reports the measured prefix"
  st_row_detail "$out" hypr.file.sha_pin NOTE "drifted from round-1 pin 4f52854a3c14" "A: sha pin names the round-1 pin (fixture cannot match it)"
  st_counts_agree "$out" "A: counts agree with rows"

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
  st_counts_agree "$out" "B: counts agree with rows"

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
  st_counts_agree "$out" "C: counts agree with rows"

  # --- scenario D: usage contract ------------------------------------------
  out=$("$BASH_BIN" "$0" --help 2>&1); rc=$?
  st_eq  "D: --help exit 0" 0 "$rc"
  st_has "D: --help prints usage" "$out" "usage: mado-verify.sh"
  out=$("$BASH_BIN" "$0" --bogus 2>&1); rc=$?
  st_eq  "D: bad arg exit 2" 2 "$rc"

  # --- scenario E: python3 absent → degradation arms must read UNKNOWN ------
  local SANDBOX_NPY="$T/nopy"
  mkdir -p "$SANDBOX_NPY"
  for c in bash grep sed awk cut head tail tr sort uniq wc find mktemp sha256sum \
           ls cat rm cp mv mkdir printf dirname basename; do
    if have "$c"; then ln -sf "$(command -v "$c")" "$SANDBOX_NPY/$c"; fi
  done
  out=$(env PATH="$SANDBOX_NPY" "$BASH_BIN" "$0" --root "$A" --no-live 2>&1); rc=$?
  st_eq  "E: exit 1 (UNKNOWN blocks CLEAN)" 1 "$rc"
  st_has "E: DIVERGED verdict" "$out" "MADO_VERIFY: DIVERGED"
  st_row_has "$out" waybar.config.parse UNKNOWN "E (reader fallback)"
  st_row_has "$out" walker.config UNKNOWN "E (reader fallback)"
  st_row_has "$out" term.alacritty.toml UNKNOWN "E (reader fallback)"
  st_not_has "E: no fake CLEAN" "$out" "MADO_VERIFY: CLEAN"
  st_counts_agree "$out" "E: counts agree with rows"

  # --- scenario F: a failing suite must exit 2 (failing-selftest exit map) --
  # the child carries the marker so this probe cannot recurse.
  if [ "${MADO_SELFTEST_NESTED:-0}" != 1 ]; then
    local SANDBOX_NOSHA="$T/nosha" cs csr csp
    mkdir -p "$SANDBOX_NOSHA"
    for c in bash env grep sed awk cut head tail tr sort uniq wc find mktemp \
             ls cat rm cp mv mkdir printf dirname basename ln chmod; do
      if have "$c"; then ln -sf "$(command -v "$c")" "$SANDBOX_NOSHA/$c"; fi
    done
    cs=$(env MADO_SELFTEST_NESTED=1 PATH="$SANDBOX_NOSHA" "$BASH_BIN" "$0" --selftest 2>&1); csr=$?
    st_eq  "F: failing selftest exits 2" 2 "$csr"
    st_has "F: failing selftest reports FAILED" "$cs" "MADO_SELFTEST: FAILED"
    csp=$(printf '%s\n' "$cs" | sed -n 's/^fixtures kept: //p' | tail -1)
    [ -n "$csp" ] && rm -rf "$csp"
  fi

  # --- scenario H: an undeclared extra source flips the census to FAIL ------
  local EXTRA="$T/extra"
  mkdir -p "$EXTRA"
  cp -a "$A/." "$EXTRA/"
  printf 'source = ~/.config/hypr/extra.conf\n' >>"$EXTRA/.config/hypr/hyprland.conf"
  out=$("$BASH_BIN" "$0" --root "$EXTRA" --no-live 2>&1); rc=$?
  st_eq  "H: exit 1 (undeclared source)" 1 "$rc"
  st_has "H: DIVERGED verdict" "$out" "MADO_VERIFY: DIVERGED"
  st_row_has "$out" hypr.root.include_graph FAIL "H (exact census, no tolerance)"
  st_not_has "H: no fake CLEAN" "$out" "MADO_VERIFY: CLEAN"
  st_counts_agree "$out" "H: counts agree with rows"

  # --- scenario I: a plane change mid-run must FAIL the boundary proof ------
  local MID="$T/midrun" REAL_SHA
  REAL_SHA=$(command -v sha256sum)
  mkdir -p "$MID"
  cat >"$MID/sha256sum" <<IEOF
#!/bin/sh
if [ "\$#" -gt 0 ]; then exec "$REAL_SHA" "\$@"; fi
n=\$(cat "$MID/sha-calls" 2>/dev/null || echo 0)
n=\$((n + 1)); printf '%s' "\$n" >"$MID/sha-calls"
h=\$("$REAL_SHA" | cut -d' ' -f1)
printf '%s %s\\n' "\${h}\${n}" stdin-counter
IEOF
  chmod +x "$MID/sha256sum"
  out=$(env PATH="$MID:$PATH" "$BASH_BIN" "$0" --root "$A" --no-live 2>&1); rc=$?
  st_eq  "I: exit 1 (boundary drift detected)" 1 "$rc"
  st_has "I: DIVERGED verdict" "$out" "MADO_VERIFY: DIVERGED"
  st_row_has "$out" boundary.readonly FAIL "I (safety row, FAIL direction)"
  st_not_has "I: no fake CLEAN" "$out" "MADO_VERIFY: CLEAN"
  st_counts_agree "$out" "I: counts agree with rows"

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
# >>> MADO-R7-REGRESSION-BLOCK >>>
# ===========================================================================
# REGRESSION — replay the recorded mutation case (M7-1, round 7)
#
# Case (recorded, not re-derived): tameshi's T6-1 sweep of this gate — round-6
# record corpus/knowledge/gate-mutation-proof.md §1: the ten-defect spec byte
# copy (sha256 c7ee75b9…) applied to gate revision c4c1afb7… (1,186 L, suite
# 53) measured 10 killed / 0 survived / 0 inconclusive. This mode re-runs it:
#
#   target   THIS file with the two MADO-R7 blocks excised = the recorded
#            revision; byte-identity to PIN_MADO is asserted before any run
#            (a mismatch refuses with SETUP, exit 2: the table is revision-
#            tied, re-cut it — the gate moved outside the blocks)
#   defects  the recorded spec, written verbatim from the heredoc below and
#            re-checked against SPEC_SHA on the written bytes before the sweep
#   suite    bash "$MUTANT" --selftest — fresh fixture trees per run, no
#            substrate read (discipline of selftest(), above)
#
# PASS requires the measured table to equal TABLE_MADO exactly: all ten ids
# present, every verdict KILLED, flips 0, inconclusive 0, control GREEN,
# MUTATE_RESTORE OK, target bytes unchanged. The round-7 plan §(a) sketched a
# |killed − recorded| ≤ 1 / ≤ 1 flip tolerance (tameshi's report shape); it is
# deliberately NOT applied — the target is byte-frozen by excision, so slack
# would only hide a lost kill. The measured numbers print either way.
#
# Re-cut (required after any edit to the gate outside these blocks, e.g. a
# plane widening): run the printed REGRESSION_RECUT command, then update
# PIN_MADO and TABLE_MADO here from the measured table. selftest() asserts the
# derived target equals PIN_MADO on pristine runs, so a stale pin is visible.
#
# Discipline: the harness (tameshi-shokunin/tools/mutate-and-run.sh) is
# consumed read-only — a needed change is a recommendation to tameshi, never a
# patch; its revision is printed as provenance, not gated (the kill table is
# the check). Scratch only under /tmp/mado-verify-regression.*; the gate never
# touches the config plane. Kept fixture dirs from THIS run's failing suite
# runs are removed by exact path (prefix-guarded); foreign /tmp dirs are left
# untouched. No compositor/session state is read or written.
#
# Usage: mado-verify.sh --regression [--keep]
#   --target/--defects/--suite/--label/--workdir/--timeout/--tail and the
#   gate's --no-live/--live/--root/--selftest are refused (usage error, exit 2);
#   --keep retains the scratch root also on PASS.
# Lines: REGRESSION_TOOL · REGRESSION_DATE · REGRESSION_HARNESS · REGRESSION_SPEC
#   · REGRESSION_TARGET · REGRESSION_RECUT · REGRESSION_BAND · REGRESSION_SWEEP
#   · REGRESSION_TABLE · REGRESSION_WORKDIR · REGRESSION_CLEANUP ·
#   REGRESSION_DEFECT (one per differing row) · REGRESSION_CASE ·
#   MADO_REGRESSION: PASS|FAIL|SETUP   (never MADO_VERIFY:)
# Exit map: 0 PASS · 1 FAIL (measured table differs) · 2 SETUP (cannot verify:
#   missing tool/harness, spec or pin mismatch, sweep refusal) · 2 usage error.
# ===========================================================================
PIN_MADO='c4c1afb75dd1c8aa4d8ff9b808ddbeb2a05ac0e3ab1095dd7d067cff1a625171'
SPEC_SHA='c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8'
HARNESS_SHA_RECORDED='b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb'
TABLE_MADO='D1:KILLED,D2:KILLED,D3:KILLED,D4:KILLED,D5:KILLED,D6:KILLED,D7:KILLED,D8:KILLED,D9:KILLED,R1:KILLED'
MADO_R7_SELF=$(readlink -f "$0" 2>/dev/null || printf '%s' "$0")
MADO_R7_FLEET=$(dirname "$(dirname "$(dirname "$MADO_R7_SELF")")")
REGRESSION_RUNNER=''

mado_r7_sha() { sha256sum -- "$1" 2>/dev/null | cut -d' ' -f1; }

mado_r7_table_lookup() { # <table> <id> -> verdict, '-' when the id is absent
  local pair
  for pair in ${1//,/ }; do
    if [ "${pair%%:*}" = "$2" ]; then printf '%s' "${pair#*:}"; return 0; fi
  done
  printf '%s' '-'
}

mado_r7_table_count() { # <table> <verdict> -> entries carrying that verdict
  local pair n=0
  for pair in ${1//,/ }; do
    if [ "${pair#*:}" = "$2" ]; then n=$((n + 1)); fi
  done
  printf '%s' "$n"
}

mado_r7_table_total() { # <table> -> number of entries
  local pair n=0
  for pair in ${1//,/ }; do n=$((n + 1)); done
  printf '%s' "$n"
}

mado_r7_spec_write() { # <dest-file> — the recorded defect spec, verbatim (no trailing LF)
  local body
  body=$(cat <<'MADO_R7_SPEC_EOF'
# defect spec v1 — T6-1 service sweep, target mado-shokunin/tools/mado-verify.sh
# pin: sha256 d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13
# clause map: A verdict token · B UNKNOWN-never-CLEAN · C exit map · D declared-plane census
#             E sha comparison · F reader fallback

@defect D1 | clause A: file-plane CLEAN verdict token renamed (CLEAN -> OK)
@old MADO_VERIFY: CLEAN (%s pass, %s notes; file plane only
@new MADO_VERIFY: OK (%s pass, %s notes; file plane only

@defect D2 | clause B: UNKNOWN guard dropped from the CLEAN test
@old if [ "$FAIL" = 0 ] && [ "$UNKNOWN" = 0 ]; then
@new if [ "$FAIL" = 0 ]; then

@defect D3 | clause B: skipped live layer row reports PASS instead of SKIP
@old     row hypr-live live.plane SKIP "live layer skipped ($live_skipped_reason) — file plane only"
@new     row hypr-live live.plane PASS "live layer skipped ($live_skipped_reason) — file plane only"

@defect D4 | clause C: DIVERGED path exits 0
@old "$reason"\nexit 1
@new "$reason"\nexit 0

@defect D5 | clause C: failing --selftest returns 1 not 2
@old   return 2
@new   return 1

@defect D6 | clause D: xdph dropped from the 12-conf local inventory
@old (hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph)
@new (hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs)

@defect D7 | clause D: include-graph count test -ne -> -lt (extra source lines tolerated)
@old if [ "${#got[@]}" -ne "${#EXPECT[@]}" ]; then
@new if [ "${#got[@]}" -lt "${#EXPECT[@]}" ]; then

@defect D8 | clause E: hyprland.conf sha pin comparison always "matches"
@old if [ "$sha" = "4f52854a3c14" ]; then
@new if [ -n "$sha" ]; then

@defect D9 | clause E: read-only boundary comparison always reads byte-identical
@old if [ "$after" = "$before" ]; then
@new if [ -n "$after" ]; then

@defect R1 | clause F: tomllib-unavailable arm reads PASS not UNKNOWN
@old     row walker walker.config UNKNOWN "python3 tomllib unavailable — cannot parse TOML"
@new     row walker walker.config PASS "python3 tomllib unavailable — cannot parse TOML"
MADO_R7_SPEC_EOF
)
  printf '%s' "$body" >"$1"
}

mado_r7_target_build() { # <src-file> <dest-file> — excise the two MADO-R7 blocks
  sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-REGRESSION-BLOCK <<<$/d' \
      -e '/^[[:space:]]*# >>> MADO-R7-SELFTEST-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-SELFTEST-BLOCK <<<$/d' \
      "$1" >"$2" || return 1
  [ -s "$2" ]
}

regression_case() {
  # <name> <target> <pin-sha> <spec> <suite> <recorded-table> <case-workdir>
  # Fresh sweep of <spec> against <target> through $REGRESSION_RUNNER, then a
  # comparison of the measured verdict table against the recorded table.
  # Writes <case-workdir>/sweep.log. Returns 0 PASS · 1 FAIL · 2 SETUP.
  local name="$1" target="$2" pin="$3" spec="$4" suite="$5" table="$6" cwd="$7"
  local tsha
  if [ ! -f "$target" ]; then
    printf 'REGRESSION_CASE %s: SETUP (target missing: %s)\n' "$name" "$target"
    return 2
  fi
  tsha=$(mado_r7_sha "$target")
  if [ "$tsha" != "$pin" ]; then
    printf 'REGRESSION_CASE %s: SETUP (pin mismatch: recorded=%s live=%s target=%s)\n' \
      "$name" "$pin" "$tsha" "$target"
    return 2
  fi
  mkdir -p "$cwd" || {
    printf 'REGRESSION_CASE %s: SETUP (cannot create case workdir: %s)\n' "$name" "$cwd"
    return 2
  }

  local rc
  bash "$REGRESSION_RUNNER" --target "$target" --defects "$spec" --suite "$suite" \
    --workdir "$cwd/sweep" --label "$name" >"$cwd/sweep.log" 2>&1
  rc=$?
  printf 'REGRESSION_SWEEP %s: %s\n' "$name" \
    "$(grep -m1 '^MUTATE: ' "$cwd/sweep.log" 2>/dev/null || printf 'no MUTATE line (sweep exit=%s)' "$rc")"
  if [ "$rc" = 2 ]; then
    printf 'REGRESSION_CASE %s: SETUP (sweep refused; log: %s)\n' "$name" "$cwd/sweep.log"
    return 2
  fi
  if [ "$rc" != 0 ] && [ "$rc" != 1 ]; then
    printf 'REGRESSION_CASE %s: FAIL (sweep exit=%s, expected 0 or 1; log: %s)\n' \
      "$name" "$rc" "$cwd/sweep.log"
    return 1
  fi
  local rtsv="$cwd/sweep/results.tsv"
  if [ ! -f "$rtsv" ]; then
    printf 'REGRESSION_CASE %s: FAIL (no results table; sweep exit=%s; log: %s)\n' \
      "$name" "$rc" "$cwd/sweep.log"
    return 1
  fi

  local id v rest want total=0 killed=0 survived=0 inconcl=0 flips=0 matches=0 seen='' diffs=''
  while IFS=$'\t' read -r id v rest; do
    [ -n "$id" ] || continue
    [ "$id" = id ] && [ "$v" = verdict ] && continue
    total=$((total + 1)); seen="$seen $id"
    case "$v" in
      KILLED) killed=$((killed + 1)) ;;
      SURVIVED) survived=$((survived + 1)) ;;
      *) inconcl=$((inconcl + 1)) ;;
    esac
    want=$(mado_r7_table_lookup "$table" "$id")
    if [ "$want" = '-' ]; then
      flips=$((flips + 1))
      diffs="$diffs$(printf 'REGRESSION_DEFECT %s %s: measured=%s recorded=ABSENT\n' "$name" "$id" "$v")"$'\n'
    elif [ "$want" != "$v" ]; then
      flips=$((flips + 1))
      diffs="$diffs$(printf 'REGRESSION_DEFECT %s %s: measured=%s recorded=%s\n' "$name" "$id" "$v" "$want")"$'\n'
    else
      matches=$((matches + 1))
    fi
  done <"$rtsv"
  local pair eid
  for pair in ${table//,/ }; do
    eid="${pair%%:*}"
    case " $seen " in
      *" $eid "*) ;;
      *)
        flips=$((flips + 1))
        diffs="$diffs$(printf 'REGRESSION_DEFECT %s %s: measured=ABSENT recorded=%s\n' "$name" "$eid" "${pair#*:}")"$'\n'
        ;;
    esac
  done

  local exp_total exp_killed ctl=0 restore=0 after delta=0
  exp_total=$(mado_r7_table_total "$table")
  exp_killed=$(mado_r7_table_count "$table" KILLED)
  grep -q '^CONTROL: GREEN ' "$cwd/sweep.log" && ctl=1
  grep -q '^MUTATE_RESTORE: OK ' "$cwd/sweep.log" && restore=1
  after=$(mado_r7_sha "$target")

  local reasons=''
  delta=$((killed - exp_killed)); [ "$delta" -lt 0 ] && delta=$((0 - delta))
  [ "$killed" = "$exp_killed" ] || reasons="$reasons killed=$killed-recorded=$exp_killed"
  [ "$flips" = 0 ] || reasons="$reasons flips=$flips"
  [ "$inconcl" = 0 ] || reasons="$reasons inconclusive=$inconcl"
  [ "$total" = "$exp_total" ] || reasons="$reasons defects=$total-recorded=$exp_total"
  [ "$ctl" = 1 ] || reasons="$reasons control-not-green"
  [ "$restore" = 1 ] || reasons="$reasons restore-not-ok"
  [ "$after" = "$pin" ] || reasons="$reasons target-sha-changed"

  [ -z "$diffs" ] || printf '%s' "$diffs"
  printf 'REGRESSION_TABLE %s: match=%s/%s recorded-killed=%s measured-killed=%s survived=%s inconclusive=%s flips=%s\n' \
    "$name" "$matches" "$exp_total" "$exp_killed" "$killed" "$survived" "$inconcl" "$flips"
  printf 'REGRESSION_WORKDIR %s: %s\n' "$name" "$cwd"
  if [ -z "$reasons" ]; then
    printf 'REGRESSION_CASE %s: PASS (recorded table reproduced: killed=%s/%s flips=0 inconclusive=0 control=green restore=ok)\n' \
      "$name" "$killed" "$exp_total"
    return 0
  fi
  printf 'REGRESSION_CASE %s: FAIL (out of band:%s; delta=%s; log: %s)\n' \
    "$name" "$reasons" "$delta" "$cwd/sweep.log"
  return 1
}

run_regression() { # <keep 0|1>
  local keep="$1" root harness spec target ssha tsha rc removed=0 p
  local missing=''
  for p in sed grep cut sha256sum mktemp python3; do
    have "$p" || missing="$missing $p"
  done
  if [ -n "$missing" ]; then
    printf 'MADO_REGRESSION: SETUP (tool(s) missing:%s)\n' "$missing"
    return 2
  fi
  harness="${MADO_VERIFY_HARNESS:-$MADO_R7_FLEET/tameshi-shokunin/tools/mutate-and-run.sh}"
  if [ ! -f "$harness" ]; then
    printf 'MADO_REGRESSION: SETUP (mutation harness not found: %s; set MADO_VERIFY_HARNESS)\n' "$harness"
    return 2
  fi
  REGRESSION_RUNNER="$harness"
  root=$(mktemp -d /tmp/mado-verify-regression.XXXXXX) || {
    printf 'MADO_REGRESSION: SETUP (mktemp -d /tmp/mado-verify-regression.* failed)\n'
    return 2
  }
  printf 'REGRESSION_TOOL: %s sha256=%s\n' "$MADO_R7_SELF" "$(mado_r7_sha "$MADO_R7_SELF")"
  printf 'REGRESSION_DATE: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'REGRESSION_HARNESS: %s sha256=%s (recorded revision %s — provenance, not gated)\n' \
    "$harness" "$(mado_r7_sha "$harness")" "$HARNESS_SHA_RECORDED"

  spec="$root/mado-verify.defects.spec"
  if ! mado_r7_spec_write "$spec"; then
    printf 'MADO_REGRESSION: SETUP (cannot write the embedded spec under %s)\n' "$root"
    return 2
  fi
  ssha=$(mado_r7_sha "$spec")
  if [ "$ssha" != "$SPEC_SHA" ]; then
    printf 'MADO_REGRESSION: SETUP (embedded spec sha256 %s != recorded %s)\n' "$ssha" "$SPEC_SHA"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    return 2
  fi
  printf 'REGRESSION_SPEC: %s sha256=%s (recorded pin matches)\n' "$spec" "$ssha"

  target="$root/target.mado-verify.sh"
  if ! mado_r7_target_build "$MADO_R7_SELF" "$target"; then
    printf 'MADO_REGRESSION: SETUP (cannot derive the recorded target from %s)\n' "$MADO_R7_SELF"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    return 2
  fi
  tsha=$(mado_r7_sha "$target")
  printf 'REGRESSION_TARGET: %s sha256=%s (recorded pin %s; match=%s)\n' \
    "$target" "$tsha" "$PIN_MADO" "$([ "$tsha" = "$PIN_MADO" ] && printf yes || printf no)"
  if [ "$tsha" != "$PIN_MADO" ]; then
    printf 'REGRESSION_RECUT: bash %s --target %s --defects %s --suite %s --workdir %s/recut --label mado-verify.sh\n' \
      "$harness" "$target" "$spec" "'bash \"\$MUTANT\" --selftest'" "$root"
    printf 'MADO_REGRESSION: SETUP (target pin mismatch — the gate moved outside the MADO-R7 blocks; re-cut, then update PIN_MADO/TABLE_MADO)\n'
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    return 2
  fi

  printf 'REGRESSION_BAND: all recorded kills required (recorded %s/%s KILLED; flips=0; inconclusive=0; control GREEN; MUTATE_RESTORE OK; target sha unchanged) — plan §(a) killed-delta<=1 tolerance not applied\n' \
    "$(mado_r7_table_count "$TABLE_MADO" KILLED)" "$(mado_r7_table_total "$TABLE_MADO")"
  regression_case mado-verify-hardened "$target" "$PIN_MADO" "$spec" \
    'bash "$MUTANT" --selftest' "$TABLE_MADO" "$root/case"
  rc=$?

  for p in $(grep -rhoE '^fixtures kept: /tmp/w5-mado-m52-selftest\.[A-Za-z0-9.]+' \
             "$root/case/sweep/evidence" 2>/dev/null | sed 's/^fixtures kept: //' | sort -u); do
    case "$p" in
      /tmp/w5-mado-m52-selftest.*)
        if [ -d "$p" ]; then rm -rf "$p"; removed=$((removed + 1)); fi
        ;;
    esac
  done
  printf 'REGRESSION_CLEANUP: removed=%s kept-fixture dir(s) named by this run (paths read from this run; /tmp/w5-mado-m52-selftest.* prefix-guarded)\n' "$removed"

  case "$rc" in
    0)
      printf 'MADO_REGRESSION: PASS (case=mado-verify-hardened; target=%s)\n' "$PIN_MADO"
      if [ "$keep" = 1 ]; then
        printf 'REGRESSION_WORKDIR: %s (kept; --keep)\n' "$root"
      else
        printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\n' "$root"
        rm -rf "$root"
      fi
      return 0
      ;;
    1)
      printf 'MADO_REGRESSION: FAIL (case=mado-verify-hardened; the recorded table did not reproduce)\n'
      printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
      return 1
      ;;
    *)
      printf 'MADO_REGRESSION: SETUP (case=mado-verify-hardened could not be verified)\n'
      printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
      return 2
      ;;
  esac
}

mado_r7_regression_requested() { # "$@" → 0 when --regression is present
  local a
  for a in "$@"; do [ "$a" = '--regression' ] && return 0; done
  return 1
}

mado_r7_cli() { # regression-mode argument contract (the gate's own flags are refused)
  local keep=0
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --regression) : ;;
      --keep) keep=1 ;;
      -h | --help)
        usage
        printf '\n  --regression  replay the recorded mutation case (tameshi T6-1 spec at\n'
        printf '                pinned bytes over the recorded gate revision); --keep\n'
        printf '                retains the scratch root also on PASS. No substrate read.\n'
        return 0
        ;;
      --target | --defects | --suite | --label | --workdir | --timeout | --tail)
        printf 'usage error: --regression takes no %s\n' "$1" >&2; usage >&2; return 2
        ;;
      --target=* | --defects=* | --suite=* | --label=* | --workdir=* | --timeout=* | --tail=*)
        printf 'usage error: --regression takes no %s\n' "${1%%=*}" >&2; usage >&2; return 2
        ;;
      --no-live | --live | --selftest | --root | --root=*)
        printf 'usage error: %s is not valid with --regression (the case reads no substrate)\n' \
          "${1%%=*}" >&2
        usage >&2
        return 2
        ;;
      *)
        printf 'usage error: unknown argument %s\n' "$1" >&2; usage >&2; return 2
        ;;
    esac
    shift
  done
  run_regression "$keep"
}

if mado_r7_regression_requested "$@"; then
  mado_r7_cli "$@"
  exit $?
fi
# <<< MADO-R7-REGRESSION-BLOCK <<<

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