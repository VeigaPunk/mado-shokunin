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
#   hypr    — hyprland.conf is a pure orchestrator: 18 source statements in the
#             exact include order (MADO-1 §1/§3; 17→18 erratum, round 12); the
#             13 active local confs are judged as an exact set of regular files
#             — every declared name present and no undeclared *.conf file
#             present, each named on FAIL
#             (MADO-1 §2; round 12 M13); the observed source set is compared to
#             the declared one the same way, order kept (round 13); every
#             declared target must be a regular file — the check follows a
#             symlink, so a link to a file passes while a directory (direct or
#             a glob match) is refused by name under `non-regular:` (round 14);
#             local envs.conf is an orphan (MADO-1 §2, MADO-R2-1 §6/F3); the
#             no-gaps toggle declares 0s (MADO-1 §7).
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
#   omarchy — freshness / version-drift watch (omarchy-drift-watch.md §2/§6):
#             version cmd+file 3.8.3, git tag v3.8.4 at HEAD 8fcc9d60…, skill
#             link into the checkout, skill leaf sha becd149e…, worktree ==
#             HEAD blob, command groups ⊇ the 11 skill groups. MOVED → FAIL
#             naming the pin; theme/counters/docs are record-level NOTEs (D-1).
#   theme   — declared file chain (theme-wallpaper-plane.md §2/§4/§6): the
#             machine name (`current/theme.name`, one line, ^[a-z0-9-]+$) and
#             every installed consumer's import resolve (hyprland.conf:13,
#             hyprlock.conf:1, waybar/style.css:1, alacritty.toml:1, the mako
#             config symlink, the walker theme package css, swayosd/style.css);
#             the background symlink resolves inside current/theme/backgrounds/
#             to a non-empty file. Declared-only parts (consumer binary absent,
#             §4.1) stay NOTEs; the theme *choice* stays operator-owned
#             (live.theme.current) and is never a verdict input.
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

# diagnostic display for a resolved source path: the verified root reads as ~
# so a named target matches the declared form in hyprland.conf. Diagnostics
# only — never used for the filesystem test itself.
src_disp() { # <expanded path>
  local p="$1" r="${ROOT%/}"
  case "$p" in
    "$r"/*) printf '~/%q' "${p#"$r"/}" ;;
    *) printf '%q' "$p" ;;
  esac
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
# fixture line-anchor mirror: three leading lines put the theme include at
# line 13, the measured live anchor (theme-wallpaper-plane.md §4).
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
source = ~/.config/hypr/gkeep.conf
EOF

  local f
  for f in bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage gkeep autostart envs xdph; do
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
  # theme chain fixtures (theme-wallpaper-plane.md §2/§4): the parts every
  # consumer import must resolve to, plus the two declared symlinks. Shapes
  # only — a fixture cannot carry the live payload, and no row reads content
  # beyond "is this part a non-empty regular file".
  printf '# fixture theme hyprlock include\n' >"$R/.config/omarchy/current/theme/hyprlock.conf"
  printf '# fixture theme alacritty palette\n' >"$R/.config/omarchy/current/theme/alacritty.toml"
  printf '[main]\nfont=monospace\n' >"$R/.config/omarchy/current/theme/mako.ini"
  printf '# fixture theme walker css\n' >"$R/.config/omarchy/current/theme/walker.css"
  printf '# fixture theme swayosd css\n' >"$R/.config/omarchy/current/theme/swayosd.css"
  mkdir -p "$R/.config/omarchy/current/theme/backgrounds" "$R/.config/mako" "$R/.config/swayosd"
  printf 'fixture background (non-empty; bytes are not read)\n' \
    >"$R/.config/omarchy/current/theme/backgrounds/0-fixture.jpg"
  ln -s theme/backgrounds/0-fixture.jpg "$R/.config/omarchy/current/background"
  ln -s ../omarchy/current/theme/mako.ini "$R/.config/mako/config"
  printf 'source = ~/.config/omarchy/current/theme/hyprlock.conf\n' >"$R/.config/hypr/hyprlock.conf"
  printf '@import "../omarchy/current/theme/swayosd.css";\n' >"$R/.config/swayosd/style.css"
  mkdir -p "$R/.local/share/omarchy/default/walker/themes/omarchy-default"
  printf '@import "~/.config/omarchy/current/theme/walker.css";\n' \
    >"$R/.local/share/omarchy/default/walker/themes/omarchy-default/style.css"

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
    n=$(printf '%s\n' "$2" | awk -v s="$3" '/^(hypr|hypr-live|waybar|walker|terms|omarchy|theme|gate) / && $3==s {c++} END {print c+0}')
    st_eq "$1" "$4" "$n"
  }
  st_row_has() { # out id status
    if printf '%s\n' "$1" | awk -v i="$2" -v s="$3" '/^(hypr|hypr-live|waybar|walker|terms|omarchy|theme|gate) / && $2==i && $3==s {c++} END {exit (c+0>0)?0:1}'; then
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
  st_row_exact() { # out id status whole-detail desc — equality, not a substring
    local got
    got=$(printf '%s\n' "$1" | awk -v i="$2" -v s="$3" '
      $2==i && $3==s { d=$0; sub(/^[^ ]+ +[^ ]+ +[^ ]+ +/, "", d); print d; exit }')
    st_eq "$5" "$4" "$got"
  }
  st_counts_agree() { # out desc — the report counts must equal the row table
    local np nf nu ns nn
    np=$(printf '%s\n' "$1" | awk '/^(hypr|hypr-live|waybar|walker|terms|omarchy|theme|gate) / && $3=="PASS" {c++} END {print c+0}')
    nf=$(printf '%s\n' "$1" | awk '/^(hypr|hypr-live|waybar|walker|terms|omarchy|theme|gate) / && $3=="FAIL" {c++} END {print c+0}')
    nu=$(printf '%s\n' "$1" | awk '/^(hypr|hypr-live|waybar|walker|terms|omarchy|theme|gate) / && $3=="UNKNOWN" {c++} END {print c+0}')
    ns=$(printf '%s\n' "$1" | awk '/^(hypr|hypr-live|waybar|walker|terms|omarchy|theme|gate) / && $3=="SKIP" {c++} END {print c+0}')
    nn=$(printf '%s\n' "$1" | awk '/^(hypr|hypr-live|waybar|walker|terms|omarchy|theme|gate) / && $3=="NOTE" {c++} END {print c+0}')
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

  # >>> MADO-R8-OMARCHY-BLOCK >>>
  # --- scenarios OM: the omarchy drift watch, hermetic (M6-2 note §2/§6) ---
  # Plane `omarchy` (round 8 / M8-2). No substrate is read here: the fixture
  # root carries the install files and `omarchy` / `git` are PATH stubs
  # answering from canned values, so each row's decision logic is exercised
  # without a real checkout or session. Named limitation: the skill-leaf sha
  # pin is a preimage of the real file, so no fixture can carry it — OM1
  # asserts the FAIL direction of that one row, and its PASS direction is
  # covered by the live run only (reported in the round's evidence).
  local OMB="$T/omarchy/bin" OMB2="$T/omarchy/bin-no-omarchy"
  local OMR="$T/omarchy/root" om_out om_rc om_leafsha
  mkdir -p "$OMB" "$OMR/.agents/skills" "$OMR/.config/omarchy/hooks/battery-low.d" \
           "$OMR/.local/share/omarchy/default/omarchy-skill" "$OMR/.local/share/omarchy/.git"
  printf '3.8.3\n' >"$OMR/.local/share/omarchy/version"
  printf 'fixture skill leaf — deliberately not the pinned file\n' \
    >"$OMR/.local/share/omarchy/default/omarchy-skill/SKILL.md"
  ln -s "$OMR/.local/share/omarchy/default/omarchy-skill" "$OMR/.agents/skills/omarchy"
  cp -a "$A/." "$OMR/" # the clean config plane: only omarchy rows can be red
  om_leafsha=$(sha256sum "$OMR/.local/share/omarchy/default/omarchy-skill/SKILL.md" | cut -c1-12)
  python3 - "$T/omarchy/cmds-ok.json" "$T/omarchy/cmds-missing.json" \
    "$OMARCHY_SKILL_GROUPS" <<'MADO_R8_JSON_PY' 2>/dev/null || true
import json, sys
ok_path, miss_path, groups = sys.argv[1], sys.argv[2], sys.argv[3].split()
rows = [{"route": "omarchy %s" % g, "binary": "omarchy-%s" % g, "group": g,
         "name": g, "hidden": False, "routes": ["omarchy %s" % g]} for g in groups]
json.dump({"ok": True, "commands": rows}, open(ok_path, "w"))
json.dump({"ok": True, "commands": [r for r in rows if r["group"] not in ("pkg", "setup")]},
          open(miss_path, "w"))
MADO_R8_JSON_PY
  cat >"$OMB/omarchy" <<'MADO_R8_OM_STUB'
#!/bin/bash
# scenario-local stub of the omarchy CLI: answers the three read verbs the
# drift rows use from canned values (STUB_OM_*), so no install is touched.
case "${1:-}" in
  version) printf '%s\n' "${STUB_OM_VERSION:-3.8.3}" ;;
  theme) [ "${2:-}" = current ] || exit 64; printf '%s\n' "${STUB_OM_THEME:-Matte Black}" ;;
  commands) cat "${STUB_OM_CMDS:-/dev/null}" ;;
  *) printf 'stub omarchy: unhandled verb: %s\n' "$*" >&2; exit 64 ;;
esac
MADO_R8_OM_STUB
  cat >"$OMB/git" <<'MADO_R8_GIT_STUB'
#!/bin/bash
# scenario-local stub of the three git read verbs the drift rows use. The
# checkout path after -C is deliberately not read: the answers are canned.
while [ "$#" -gt 0 ]; do
  case "$1" in
    describe) printf '%s\n' "${STUB_GIT_TAG:-v3.8.4}"; exit 0 ;;
    rev-parse) printf '%s\n' "${STUB_GIT_HEAD:-8fcc9d6048af4cb0e3af8512c78049857a3b53dd}"; exit 0 ;;
    show) cat "${STUB_GIT_BLOB:-/dev/null}"; exit 0 ;;
  esac
  shift
done
exit 64
MADO_R8_GIT_STUB
  chmod +x "$OMB/omarchy" "$OMB/git"
  for c in bash grep sed awk cut head tail tr sort uniq wc find mktemp sha256sum \
           python3 ls cat rm cp mv mkdir printf dirname basename ln chmod readlink; do
    if have "$c"; then ln -sf "$(command -v "$c")" "$OMB/$c"; fi
  done
  cp -a "$OMB" "$OMB2"; rm -f "$OMB2/omarchy"
  local OM_LEAF="$OMR/.local/share/omarchy/default/omarchy-skill/SKILL.md" OM_CMDS="$T/omarchy/cmds-ok.json"

  # --- OM1: fixture install + stubbed readers, live requested --------------
  om_out=$(env PATH="$OMB" STUB_OM_CMDS="$OM_CMDS" STUB_GIT_BLOB="$OM_LEAF" \
    MADO_VERIFY_LIVE=yes "$BASH_BIN" "$0" --root "$OMR" 2>&1); om_rc=$?
  st_eq  "OM1: exit 1 — only the un-reproducible sha row can be red" 1 "$om_rc"
  st_eq  "OM1: the plane emits all 11 rows" 11 \
    "$(printf '%s\n' "$om_out" | awk '$1=="omarchy" {c++} END {print c+0}')"
  st_row_has "$om_out" omarchy.version.file PASS "OM1 (P2 pin held)"
  st_row_has "$om_out" omarchy.skill.link PASS "OM1 (link into the checkout)"
  st_row_has "$om_out" omarchy.version.cmd PASS "OM1 (P1 pin held, stubbed reader)"
  st_row_has "$om_out" omarchy.git.tag PASS "OM1 (P3 tag held)"
  st_row_has "$om_out" omarchy.git.head PASS "OM1 (P3 HEAD held)"
  st_row_has "$om_out" omarchy.skill.vs_head PASS "OM1 (same bytes both sides)"
  st_row_has "$om_out" omarchy.cmd.groups PASS "OM1 (11 skill groups present)"
  st_row_has "$om_out" omarchy.cmd.surface NOTE "OM1 (counter stays a NOTE)"
  st_row_has "$om_out" omarchy.theme NOTE "OM1 (D-1: operator-owned)"
  st_row_has "$om_out" omarchy.doc.drifts NOTE "OM1"
  st_row_detail "$om_out" omarchy.skill.sha FAIL "$om_leafsha" \
    "OM1: the sha row measures the fixture leaf"
  st_row_detail "$om_out" omarchy.skill.sha FAIL "${OMARCHY_SKILL_SHA_PIN:0:12}" \
    "OM1: ... and names the pin it cannot match"
  st_eq  "OM1: exactly one omarchy FAIL" 1 \
    "$(printf '%s\n' "$om_out" | awk '$1=="omarchy" && $3=="FAIL" {c++} END {print c+0}')"
  st_eq  "OM1: zero omarchy UNKNOWN" 0 \
    "$(printf '%s\n' "$om_out" | awk '$1=="omarchy" && $3=="UNKNOWN" {c++} END {print c+0}')"
  st_has "OM1: the verdict names that one row" "$om_out" "first fail: omarchy.skill.sha"
  st_row_has "$om_out" boundary.readonly PASS "OM1 (read-only proof holds with the plane running)"
  st_row_has "$om_out" hypr.root.orchestrator PASS "OM1 (config plane unaffected)"
  st_counts_agree "$om_out" "OM1: counts agree with rows"

  # --- OM2: the same root, file plane only ---------------------------------
  om_out=$(env PATH="$OMB" "$BASH_BIN" "$0" --root "$OMR" --no-live 2>&1); om_rc=$?
  st_eq  "OM2: exit 1 — the sha row is a file row, live or not" 1 "$om_rc"
  st_row_has "$om_out" omarchy.version.file PASS "OM2"
  st_row_has "$om_out" omarchy.skill.link PASS "OM2"
  st_row_detail "$om_out" omarchy.version.cmd SKIP "live layer skipped" \
    "OM2: live rows name the skipped scope"
  st_row_detail "$om_out" omarchy.git.tag SKIP "live layer skipped" "OM2"
  st_row_detail "$om_out" omarchy.theme SKIP "live layer skipped" "OM2"
  st_row_has "$om_out" omarchy.cmd.groups SKIP "OM2"
  st_eq  "OM2: exactly one omarchy FAIL — the unreproducible sha row" 1 \
    "$(printf '%s\n' "$om_out" | awk '$1=="omarchy" && $3=="FAIL" {c++} END {print c+0}')"
  st_eq  "OM2: zero omarchy UNKNOWN" 0 \
    "$(printf '%s\n' "$om_out" | awk '$1=="omarchy" && $3=="UNKNOWN" {c++} END {print c+0}')"
  st_has "OM2: that FAIL is the sha row" "$om_out" "first fail: omarchy.skill.sha"
  st_counts_agree "$om_out" "OM2: counts agree with rows"

  # --- OM3: version file MOVED → FAIL naming the pin, DIVERGED -------------
  local OMR3="$T/omarchy/root-moved"
  cp -a "$OMR" "$OMR3"
  rm -f "$OMR3/.agents/skills/omarchy"
  ln -s "$OMR3/.local/share/omarchy/default/omarchy-skill" "$OMR3/.agents/skills/omarchy"
  printf '3.8.4\n' >"$OMR3/.local/share/omarchy/version"
  om_out=$(env PATH="$OMB" STUB_OM_CMDS="$OM_CMDS" STUB_GIT_BLOB="$OM_LEAF" \
    MADO_VERIFY_LIVE=yes "$BASH_BIN" "$0" --root "$OMR3" 2>&1); om_rc=$?
  st_eq  "OM3: exit 1" 1 "$om_rc"
  st_has "OM3: DIVERGED verdict" "$om_out" "MADO_VERIFY: DIVERGED"
  st_row_detail "$om_out" omarchy.version.file FAIL "MOVED" "OM3: a moved version file reads MOVED"
  st_row_detail "$om_out" omarchy.version.file FAIL "3.8.3" "OM3: ... naming the pin"
  st_row_has "$om_out" omarchy.skill.link PASS "OM3 (the link is untouched)"
  st_eq  "OM3: two omarchy FAILs (moved file + unreproducible sha)" 2 \
    "$(printf '%s\n' "$om_out" | awk '$1=="omarchy" && $3=="FAIL" {c++} END {print c+0}')"
  st_counts_agree "$om_out" "OM3: counts agree with rows"

  # --- OM4: live verb unavailable → UNKNOWN, never CLEAN -------------------
  om_out=$(env PATH="$OMB2" STUB_GIT_BLOB="$OM_LEAF" \
    MADO_VERIFY_LIVE=yes "$BASH_BIN" "$0" --root "$OMR" 2>&1); om_rc=$?
  st_row_has "$om_out" omarchy.version.cmd UNKNOWN "OM4 (anti-claim: stub absent)"
  st_row_has "$om_out" omarchy.cmd.groups UNKNOWN "OM4 (anti-claim)"
  st_row_has "$om_out" omarchy.git.tag PASS "OM4 (git stub still on PATH)"
  st_row_has "$om_out" omarchy.theme NOTE "OM4 (theme unread, still a NOTE)"
  st_eq  "OM4: two omarchy UNKNOWNs, no silent pass" 2 \
    "$(printf '%s\n' "$om_out" | awk '$1=="omarchy" && $3=="UNKNOWN" {c++} END {print c+0}')"
  st_not_has "OM4: no fake CLEAN" "$om_out" "MADO_VERIFY: CLEAN"
  st_counts_agree "$om_out" "OM4: counts agree with rows"

  # --- OM5: link replaced by a real dir with identical bytes ---------------
  local OMR5="$T/omarchy/root-copy"
  cp -a "$OMR" "$OMR5"
  rm -f "$OMR5/.agents/skills/omarchy"
  mkdir -p "$OMR5/.agents/skills/omarchy"
  cp "$OM_LEAF" "$OMR5/.agents/skills/omarchy/SKILL.md"
  om_out=$(env PATH="$OMB" STUB_OM_CMDS="$OM_CMDS" STUB_GIT_BLOB="$OM_LEAF" \
    MADO_VERIFY_LIVE=yes "$BASH_BIN" "$0" --root "$OMR5" 2>&1); om_rc=$?
  st_row_detail "$om_out" omarchy.skill.link FAIL "MOVED" \
    "OM5: a copy reads MOVED even with identical bytes"
  st_row_detail "$om_out" omarchy.skill.link FAIL "real directory" "OM5: ... named as a copy, not a link"
  st_row_detail "$om_out" omarchy.skill.sha FAIL "$om_leafsha" \
    "OM5: the same bytes are still measured (sha detail unchanged)"
  st_counts_agree "$om_out" "OM5: counts agree with rows"

  # --- OM6: worktree edit vs HEAD blob (index-free dirty check) ------------
  printf 'edited in the worktree\n' >"$T/omarchy/blob-edited"
  om_out=$(env PATH="$OMB" STUB_OM_CMDS="$OM_CMDS" STUB_GIT_BLOB="$T/omarchy/blob-edited" \
    MADO_VERIFY_LIVE=yes "$BASH_BIN" "$0" --root "$OMR" 2>&1); om_rc=$?
  st_row_detail "$om_out" omarchy.skill.vs_head FAIL "local edit" \
    "OM6: a worktree edit is detected without git status"
  st_row_has "$om_out" omarchy.version.cmd PASS "OM6 (the pin itself is held)"

  # --- OM7: moved tag / HEAD / version verb -------------------------------
  om_out=$(env PATH="$OMB" STUB_OM_CMDS="$OM_CMDS" STUB_GIT_BLOB="$OM_LEAF" \
    STUB_GIT_TAG=v3.9.0 STUB_GIT_HEAD=0000000000000000000000000000000000000000 \
    STUB_OM_VERSION=9.9.9 MADO_VERIFY_LIVE=yes "$BASH_BIN" "$0" --root "$OMR" 2>&1); om_rc=$?
  st_row_detail "$om_out" omarchy.git.tag FAIL "v3.8.4" "OM7: a moved tag names the pin"
  st_row_detail "$om_out" omarchy.git.head FAIL "8fcc9d60" "OM7: a moved HEAD names the pin"
  st_row_detail "$om_out" omarchy.version.cmd FAIL "3.8.3" "OM7: a moved version names the pin"
  st_eq  "OM7: four omarchy FAILs (three moved pins + the sha row)" 4 \
    "$(printf '%s\n' "$om_out" | awk '$1=="omarchy" && $3=="FAIL" {c++} END {print c+0}')"

  # --- OM8: a missing command group is named, the counter stays a NOTE -----
  om_out=$(env PATH="$OMB" STUB_OM_CMDS="$T/omarchy/cmds-missing.json" STUB_GIT_BLOB="$OM_LEAF" \
    MADO_VERIFY_LIVE=yes "$BASH_BIN" "$0" --root "$OMR" 2>&1); om_rc=$?
  st_row_detail "$om_out" omarchy.cmd.groups FAIL "pkg,setup" \
    "OM8: the missing groups are named"
  st_row_detail "$om_out" omarchy.cmd.surface NOTE "MOVED" \
    "OM8: the surface counter is a NOTE, never a verdict input"
  st_not_has "OM8: no fake CLEAN" "$om_out" "MADO_VERIFY: CLEAN"
  st_counts_agree "$om_out" "OM8: counts agree with rows"
  # <<< MADO-R8-OMARCHY-BLOCK <<<

  # --- scenarios T: the theme plane, hermetic (theme-wallpaper-plane.md §6) --
  # Landed from the round-7 note's file-row spec. Every case drives the real
  # row code against fixture roots built by build_fixture — the chain parts,
  # the two declared symlinks and the consumer style files are fixture shapes
  # (named in build_fixture); no substrate path is read and no consumer is
  # touched. The assertions cover the verdict direction of every landed row:
  # clean PASS, a MOVED anchor FAILs naming it, an absent consumer reads NOTE
  # (never a silent skip), a missing tree reads UNKNOWN (never CLEAN).
  local TH="$T/theme" th_out th_rc
  mkdir -p "$TH"

  # --- T1: the clean fixture — 10 rows, verdict rows PASS, NOTEs stay NOTE --
  th_out=$("$BASH_BIN" "$0" --root "$A" --no-live 2>&1); th_rc=$?
  st_eq  "T1: exit 0 (the theme rows leave the clean fixture CLEAN)" 0 "$th_rc"
  st_has "T1: CLEAN verdict" "$th_out" "MADO_VERIFY: CLEAN"
  st_eq  "T1: the plane emits 10 rows" 10 \
    "$(printf '%s\n' "$th_out" | awk '$1=="theme" {c++} END {print c+0}')"
  st_row_has "$th_out" theme.name.read PASS "T1"
  st_row_detail "$th_out" theme.name.read PASS "matte-black" "T1: the fixture name is read"
  st_row_has "$th_out" theme.chain.hypr_include PASS "T1"
  st_row_detail "$th_out" theme.chain.hypr_include PASS "line 13" "T1: the declared line anchor (live:13) is held"
  st_row_has "$th_out" theme.chain.hyprlock PASS "T1"
  st_row_has "$th_out" theme.chain.waybar_css PASS "T1"
  st_row_has "$th_out" theme.chain.alacritty PASS "T1"
  st_row_has "$th_out" theme.chain.mako_link PASS "T1 (symlink into current/theme/)"
  st_row_has "$th_out" theme.chain.walker_css PASS "T1 (consumer installed in the fixture)"
  st_row_has "$th_out" theme.chain.swayosd_css PASS "T1"
  st_row_has "$th_out" theme.wallpaper.link PASS "T1 (non-empty target inside backgrounds/)"
  st_row_has "$th_out" theme.parts.declared_only NOTE "T1 (declared-only stays a NOTE)"
  st_eq  "T1: zero theme FAILs" 0 \
    "$(printf '%s\n' "$th_out" | awk '$1=="theme" && $3=="FAIL" {c++} END {print c+0}')"
  st_eq  "T1: zero theme UNKNOWNs" 0 \
    "$(printf '%s\n' "$th_out" | awk '$1=="theme" && $3=="UNKNOWN" {c++} END {print c+0}')"
  st_counts_agree "$th_out" "T1: counts agree with the widened plane set"

  # --- T2: a chain target removed → the named row FAILs, DIVERGED ----------
  local TA="$TH/target-missing"
  mkdir -p "$TA"
  cp -a "$A/." "$TA/"
  rm -f "$TA/.config/omarchy/current/theme/hyprlock.conf"
  th_out=$("$BASH_BIN" "$0" --root "$TA" --no-live 2>&1); th_rc=$?
  st_eq  "T2: exit 1" 1 "$th_rc"
  st_has "T2: DIVERGED verdict" "$th_out" "MADO_VERIFY: DIVERGED"
  st_row_detail "$th_out" theme.chain.hyprlock FAIL "target missing" \
    "T2: the missing part is named"
  st_row_has "$th_out" theme.chain.hypr_include PASS "T2 (isolation: only the broken row moves)"
  st_eq  "T2: exactly one theme FAIL" 1 \
    "$(printf '%s\n' "$th_out" | awk '$1=="theme" && $3=="FAIL" {c++} END {print c+0}')"
  st_not_has "T2: no fake CLEAN" "$th_out" "MADO_VERIFY: CLEAN"
  st_counts_agree "$th_out" "T2: counts agree with rows"

  # --- T3: the include line moved → FAIL naming both line numbers ----------
  local TM="$TH/moved"
  mkdir -p "$TM"
  cp -a "$A/." "$TM/"
  sed -i '12a # fixture drift comment (pushes the theme include one line down)' \
    "$TM/.config/hypr/hyprland.conf"
  th_out=$("$BASH_BIN" "$0" --root "$TM" --no-live 2>&1); th_rc=$?
  st_eq  "T3: exit 1" 1 "$th_rc"
  st_row_detail "$th_out" theme.chain.hypr_include FAIL "import moved: line 14 (declared line 13)" \
    "T3: the move is named with both line numbers"
  st_row_has "$th_out" hypr.root.include_graph PASS \
    "T3: isolation — the source order is untouched, only the line number moved"
  st_counts_agree "$th_out" "T3: counts agree with rows"

  # --- T4: a copy in place of the mako link, and a dangling background -----
  local TL="$TH/links"
  mkdir -p "$TL"
  cp -a "$A/." "$TL/"
  rm -f "$TL/.config/mako/config"
  printf '[main]\nfont=monospace\n' >"$TL/.config/mako/config"
  rm -f "$TL/.config/omarchy/current/background"
  ln -s theme/backgrounds/0-missing.jpg "$TL/.config/omarchy/current/background"
  th_out=$("$BASH_BIN" "$0" --root "$TL" --no-live 2>&1); th_rc=$?
  st_eq  "T4: exit 1" 1 "$th_rc"
  st_row_detail "$th_out" theme.chain.mako_link FAIL "regular file" \
    "T4: a copy may not masquerade as the declared link"
  st_row_detail "$th_out" theme.wallpaper.link FAIL "dangling symlink" \
    "T4: the dangling background link is named"
  st_counts_agree "$th_out" "T4: counts agree with rows"

  # --- T5: the background link must resolve INSIDE backgrounds/ ------------
  local TO="$TH/outside"
  mkdir -p "$TO"
  cp -a "$A/." "$TO/"
  rm -f "$TO/.config/omarchy/current/background"
  ln -s theme/hyprland.conf "$TO/.config/omarchy/current/background"
  th_out=$("$BASH_BIN" "$0" --root "$TO" --no-live 2>&1); th_rc=$?
  st_eq  "T5: exit 1" 1 "$th_rc"
  st_row_detail "$th_out" theme.wallpaper.link FAIL "resolves outside" \
    "T5: a link out of backgrounds/ FAILs, never a silent pass"
  st_row_has "$th_out" theme.chain.hypr_include PASS "T5 (isolation)"

  # --- T6: an empty background target FAILs --------------------------------
  local TZ="$TH/empty-target"
  mkdir -p "$TZ"
  cp -a "$A/." "$TZ/"
  : >"$TZ/.config/omarchy/current/theme/backgrounds/0-fixture.jpg"
  th_out=$("$BASH_BIN" "$0" --root "$TZ" --no-live 2>&1); th_rc=$?
  st_eq  "T6: exit 1" 1 "$th_rc"
  st_row_detail "$th_out" theme.wallpaper.link FAIL "target is empty" \
    "T6: an empty wallpaper target is named"

  # --- T7: a malformed theme.name FAILs (shape, not value) -----------------
  local TN="$TH/name"
  mkdir -p "$TN"
  cp -a "$A/." "$TN/"
  printf 'Matte Black\n' >"$TN/.config/omarchy/current/theme.name"
  th_out=$("$BASH_BIN" "$0" --root "$TN" --no-live 2>&1); th_rc=$?
  st_eq  "T7: exit 1" 1 "$th_rc"
  st_row_detail "$th_out" theme.name.read FAIL "malformed theme.name" \
    "T7: the display form (uppercase, space) is not a machine name"
  st_row_has "$th_out" theme.chain.hypr_include PASS "T7 (isolation: the chain is untouched)"

  # --- T8: an absent consumer reads NOTE — never a FAIL, never a skip ------
  local TC="$TH/consumer"
  mkdir -p "$TC"
  cp -a "$A/." "$TC/"
  rm -rf "$TC/.config/swayosd" "$TC/.local/share/omarchy/default/walker/themes/omarchy-default"
  th_out=$("$BASH_BIN" "$0" --root "$TC" --no-live 2>&1); th_rc=$?
  st_eq  "T8: exit 0 — a NOTE never flips the verdict" 0 "$th_rc"
  st_has "T8: CLEAN verdict" "$th_out" "MADO_VERIFY: CLEAN"
  st_row_has "$th_out" theme.chain.walker_css NOTE "T8 (consumer absent)"
  st_row_has "$th_out" theme.chain.swayosd_css NOTE "T8 (consumer absent)"
  st_eq  "T8: zero theme FAILs" 0 \
    "$(printf '%s\n' "$th_out" | awk '$1=="theme" && $3=="FAIL" {c++} END {print c+0}')"
  st_counts_agree "$th_out" "T8: counts agree with rows"

  # --- T9: a missing theme tree reads UNKNOWN — never CLEAN ----------------
  local TE="$TH/no-tree"
  mkdir -p "$TE"
  th_out=$("$BASH_BIN" "$0" --root "$TE" --no-live 2>&1); th_rc=$?
  st_eq  "T9: exit 1 (an empty root fails closed)" 1 "$th_rc"
  st_row_has "$th_out" theme.name.read UNKNOWN "T9 (missing tree)"
  st_not_has "T9: no fake CLEAN" "$th_out" "MADO_VERIFY: CLEAN"
  st_counts_agree "$th_out" "T9: counts agree with rows"

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
  st_row_detail "$out" hypr.local.inventory PASS "13/13 active local confs, set exact" \
    "A: the local census is exact-set, gkeep included"
  st_row_detail "$out" hypr.root.sources_resolve PASS "declared targets exist, member set exact" \
    "A: the source census is exact-set with every target resolving"
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
  rm -f "$B/.config/hypr/gkeep.conf"   # round 12: a declared source whose target vanished
  printf '{ "reload_style_on_change": ' >"$B/.config/waybar/config.jsonc"
  sed -i 's/force_keyboard_focus = true/force_keyboard_focus = false/' "$B/.config/walker/config.toml"
  out=$("$BASH_BIN" "$0" --root "$B" --no-live 2>&1); rc=$?
  st_eq   "B: exit 1" 1 "$rc"
  st_has  "B: DIVERGED verdict" "$out" "MADO_VERIFY: DIVERGED"
  st_row_has "$out" hypr.root.orchestrator FAIL "B"
  st_row_has "$out" hypr.local.inventory FAIL "B"
  st_row_has "$out" hypr.root.sources_resolve FAIL "B (round 12: removed gkeep.conf)"
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
    case "$csp" in
      /tmp/w5-mado-m52-selftest.*) rm -rf "$csp" ;;
    esac
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

  # --- scenarios N: exact-set censuses, hermetic (round 13 / M13) ----------
  # One case per named-set failure: a stray local conf, a same-count source
  # substitution whose replacement target EXISTS (so target-existence alone
  # cannot see it), a same-count local substitution, and the widened gkeep
  # member removed. Each asserts the row ids, the named members, and that an
  # untouched sibling row keeps its verdict (isolation).
  local NX="$T/census" n_out n_rc
  mkdir -p "$NX"

  # N1: a stray *.conf under ~/.config/hypr → named as the extra member
  local N1R="$NX/local-extra"
  mkdir -p "$N1R"
  cp -a "$A/." "$N1R/"
  printf '# undeclared local conf\n' >"$N1R/.config/hypr/extra.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N1R" --no-live 2>&1); n_rc=$?
  st_eq  "N1: exit 1 (undeclared local conf)" 1 "$n_rc"
  st_has "N1: DIVERGED verdict" "$n_out" "MADO_VERIFY: DIVERGED"
  st_row_detail "$n_out" hypr.local.inventory FAIL "extra: extra.conf" \
    "N1: the stray member is named"
  st_row_has "$n_out" hypr.root.include_graph PASS "N1 (isolation: sources untouched)"
  st_row_has "$n_out" hypr.root.sources_resolve PASS "N1 (isolation: declared targets resolve)"
  st_not_has "N1: no fake CLEAN" "$n_out" "MADO_VERIFY: CLEAN"
  st_counts_agree "$n_out" "N1: counts agree with rows"

  # N2: one declared source line swapped for an undeclared one, count equal,
  # and the replacement target exists — the SET must fail, not existence
  local N2R="$NX/source-swap"
  mkdir -p "$N2R"
  cp -a "$A/." "$N2R/"
  printf '# undeclared source target (exists, so only the set can fail)\n' \
    >"$N2R/.local/share/omarchy/default/hypr/replacement.conf"
  sed -i 's#^source = ~/.config/hypr/ai-usage.conf$#source = ~/.local/share/omarchy/default/hypr/replacement.conf#' \
    "$N2R/.config/hypr/hyprland.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N2R" --no-live 2>&1); n_rc=$?
  st_eq  "N2: exit 1 (same-count source substitution)" 1 "$n_rc"
  st_row_has "$n_out" hypr.root.include_graph FAIL "N2 (count unchanged, set moved)"
  st_row_detail "$n_out" hypr.root.include_graph FAIL "missing: ~/.config/hypr/ai-usage.conf" \
    "N2: the missing source is named"
  st_row_detail "$n_out" hypr.root.include_graph FAIL "extra: ~/.local/share/omarchy/default/hypr/replacement.conf" \
    "N2: the extra source is named"
  st_row_detail "$n_out" hypr.root.sources_resolve FAIL "missing: ~/.config/hypr/ai-usage.conf" \
    "N2: sources_resolve names the missing member (its target exists)"
  st_row_detail "$n_out" hypr.root.sources_resolve FAIL "extra: ~/.local/share/omarchy/default/hypr/replacement.conf" \
    "N2: sources_resolve names the extra member"
  st_not_has "N2: no unresolved target (every declared target exists)" "$n_out" "unresolved:"
  st_row_has "$n_out" hypr.local.inventory PASS "N2 (isolation: the local file set is untouched)"
  st_counts_agree "$n_out" "N2: counts agree with rows"

  # N3: one declared local conf swapped for an undeclared one, count equal
  local N3R="$NX/local-swap"
  mkdir -p "$N3R"
  cp -a "$A/." "$N3R/"
  rm -f "$N3R/.config/hypr/xdph.conf"
  printf '# undeclared local conf\n' >"$N3R/.config/hypr/extra.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N3R" --no-live 2>&1); n_rc=$?
  st_eq  "N3: exit 1 (same-count local substitution)" 1 "$n_rc"
  st_eq  "N3: the *.conf count is unchanged (13) — a tally cannot see it" 13 \
    "$(find "$N3R/.config/hypr" -maxdepth 1 -type f -name '*.conf' | wc -l)"
  st_row_detail "$n_out" hypr.local.inventory FAIL "missing: xdph.conf" \
    "N3: the absent declared member is named"
  st_row_detail "$n_out" hypr.local.inventory FAIL "extra: extra.conf" \
    "N3: the undeclared member is named"
  st_row_has "$n_out" hypr.root.include_graph PASS "N3 (isolation: sources untouched)"
  st_counts_agree "$n_out" "N3: counts agree with rows"

  # N4: the widened gkeep member removed → the census names it, and the source
  # target row still names the vanished target (round-12 behaviour preserved)
  local N4R="$NX/gkeep-gone"
  mkdir -p "$N4R"
  cp -a "$A/." "$N4R/"
  rm -f "$N4R/.config/hypr/gkeep.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N4R" --no-live 2>&1); n_rc=$?
  st_eq  "N4: exit 1 (declared member removed)" 1 "$n_rc"
  st_row_detail "$n_out" hypr.local.inventory FAIL "missing: gkeep.conf" \
    "N4: the local census names gkeep.conf"
  st_row_detail "$n_out" hypr.root.sources_resolve FAIL "~/.config/hypr/gkeep.conf" \
    "N4: the source target row names the vanished target"
  st_row_exact "$n_out" hypr.root.sources_resolve FAIL \
    "unresolved: ~/.config/hypr/gkeep.conf" \
    "N4: the owning-row detail is exactly one unresolved member (no extra token)"
  st_row_has "$n_out" hypr.root.include_graph PASS "N4 (isolation: the source line is untouched)"
  st_counts_agree "$n_out" "N4: counts agree with rows"

  # N7: an empty `source =` line has no member to name — the census must keep
  # the stable FAIL+verdict (never a bad-subscript error and no rows) and name
  # the empty member. Regression guard for the exact-set code (AttackSets K2).
  local N7R="$NX/empty-source"
  mkdir -p "$N7R"
  cp -a "$A/." "$N7R/"
  printf 'source =\n' >>"$N7R/.config/hypr/hyprland.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N7R" --no-live 2>&1); n_rc=$?
  st_eq  "N7: exit 1, a verdict — not a crash" 1 "$n_rc"
  st_has "N7: the report still prints a verdict" "$n_out" "MADO_VERIFY: DIVERGED"
  st_row_detail "$n_out" hypr.root.include_graph FAIL "extra: ''" \
    "N7: the empty member is named as extra"
  st_row_detail "$n_out" hypr.root.sources_resolve FAIL "extra: ''" \
    "N7: sources_resolve names it too"
  st_not_has "N7: no bad-subscript error" "$n_out" "bad array subscript"
  st_counts_agree "$n_out" "N7: counts agree with rows"

  # N8: a hyprlang conditional wraps a source line. The plain source list still
  # reads exact, but Hyprland would skip the line — the gate must fail the
  # orchestrator row by name instead of judging a config it cannot model.
  local N8R="$NX/hyprlang"
  mkdir -p "$N8R"
  cp -a "$A/." "$N8R/"
  sed -i -e '/^source = ~\/.config\/hypr\/gkeep.conf$/i # hyprlang if UNDEFINED' \
         -e '/^source = ~\/.config\/hypr\/gkeep.conf$/a # hyprlang endif' \
         "$N8R/.config/hypr/hyprland.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N8R" --no-live 2>&1); n_rc=$?
  st_eq  "N8: exit 1 (unsupported conditional)" 1 "$n_rc"
  st_has "N8: DIVERGED verdict" "$n_out" "MADO_VERIFY: DIVERGED"
  st_row_detail "$n_out" hypr.root.orchestrator FAIL "unsupported hyprlang directive" \
    "N8: the unsupported directive is named"
  st_row_has "$n_out" hypr.root.include_graph PASS "N8 (isolation: the source list is unchanged)"
  st_not_has "N8: no fake CLEAN" "$n_out" "MADO_VERIFY: CLEAN"
  st_counts_agree "$n_out" "N8: counts agree with rows"

  # N9-N11 (round 14): a source target must be a REGULAR file. `[ -f ]` follows
  # symlinks, so a link to a file is accepted; a directory — declared directly,
  # matched by a glob, or mixed into a glob's match set — is refused by name
  # under `non-regular:` on the stable owner row hypr.root.sources_resolve.
  # A non-existent direct target and a zero-match glob keep `unresolved:`.
  # These fixtures are isolated: the hyprland.conf source lines are untouched,
  # so include_graph stays PASS and the local conf census stays PASS.

  # N9: a direct source target replaced by a directory of the same name
  local N9R="$NX/direct-dir"
  mkdir -p "$N9R"
  cp -a "$A/." "$N9R/"
  rm -f "$N9R/.local/share/omarchy/default/hypr/windows.conf"
  mkdir -p "$N9R/.local/share/omarchy/default/hypr/windows.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N9R" --no-live 2>&1); n_rc=$?
  st_eq  "N9: exit 1 (directory-shaped direct source)" 1 "$n_rc"
  st_has "N9: DIVERGED verdict" "$n_out" "MADO_VERIFY: DIVERGED"
  st_row_detail "$n_out" hypr.root.sources_resolve FAIL \
    "non-regular: ~/.local/share/omarchy/default/hypr/windows.conf" \
    "N9: the directory-shaped direct target is named"
  st_row_exact "$n_out" hypr.root.sources_resolve FAIL \
    "non-regular: ~/.local/share/omarchy/default/hypr/windows.conf" \
    "N9: the owning-row detail is exactly the non-regular target"
  st_not_has "N9: an existing target is never called unresolved" "$n_out" "unresolved:"
  st_row_has "$n_out" hypr.root.include_graph PASS "N9 (isolation: the source line and order are untouched)"
  st_row_has "$n_out" hypr.local.inventory PASS "N9 (isolation: the local census is untouched)"
  st_eq  "N9: exactly one hypr FAIL — the source row" 1 \
    "$(printf '%s\n' "$n_out" | awk '$1=="hypr" && $3=="FAIL" {c++} END {print c+0}')"
  st_counts_agree "$n_out" "N9: counts agree with rows"

  # N10: the toggle glob's only match is a directory (all-directory match set).
  # The toggle content row has its own status path for an absent regular file
  # (NOTE), so it is asserted separately — never assumed clean.
  local N10R="$NX/glob-dirs"
  mkdir -p "$N10R"
  cp -a "$A/." "$N10R/"
  rm -f "$N10R/.local/state/omarchy/toggles/hypr/window-no-gaps.conf"
  mkdir -p "$N10R/.local/state/omarchy/toggles/hypr/window-no-gaps.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N10R" --no-live 2>&1); n_rc=$?
  st_eq  "N10: exit 1 (glob matched, but only a directory)" 1 "$n_rc"
  st_has "N10: DIVERGED verdict" "$n_out" "MADO_VERIFY: DIVERGED"
  st_row_detail "$n_out" hypr.root.sources_resolve FAIL \
    "non-regular: ~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf" \
    "N10: the all-directory glob match is named"
  st_row_exact "$n_out" hypr.root.sources_resolve FAIL \
    "non-regular: ~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf" \
    "N10: the owning-row detail names only that match"
  st_not_has "N10: the glob did match, so it is not unresolved" "$n_out" "unresolved:"
  st_row_has "$n_out" hypr.root.include_graph PASS "N10 (isolation: the glob line and order are untouched)"
  st_row_has "$n_out" hypr.local.inventory PASS "N10 (isolation: the local census is untouched)"
  st_row_has "$n_out" hypr.toggle.no_gaps NOTE "N10 (collateral status: the toggle path is not a regular file)"
  st_eq  "N10: exactly one hypr FAIL — the source row" 1 \
    "$(printf '%s\n' "$n_out" | awk '$1=="hypr" && $3=="FAIL" {c++} END {print c+0}')"
  st_counts_agree "$n_out" "N10: counts agree with rows"

  # N11: mixed glob — one regular member beside one directory-shaped member.
  # Only the non-regular member is refused; the regular one still judges.
  local N11R="$NX/glob-mixed"
  mkdir -p "$N11R"
  cp -a "$A/." "$N11R/"
  mkdir -p "$N11R/.local/state/omarchy/toggles/hypr/dir.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N11R" --no-live 2>&1); n_rc=$?
  st_eq  "N11: exit 1 (mixed regular/directory glob)" 1 "$n_rc"
  st_has "N11: DIVERGED verdict" "$n_out" "MADO_VERIFY: DIVERGED"
  st_row_exact "$n_out" hypr.root.sources_resolve FAIL \
    "non-regular: ~/.local/state/omarchy/toggles/hypr/dir.conf" \
    "N11: the owning-row detail names only the directory member (no regular-member token)"
  st_not_has "N11: the glob matched, so it is not unresolved" "$n_out" "unresolved:"
  st_row_has "$n_out" hypr.root.include_graph PASS "N11 (isolation: the source lines are untouched)"
  st_row_has "$n_out" hypr.toggle.no_gaps PASS "N11 (isolation: the regular member still judges)"
  st_eq  "N11: exactly one hypr FAIL — the source row" 1 \
    "$(printf '%s\n' "$n_out" | awk '$1=="hypr" && $3=="FAIL" {c++} END {print c+0}')"
  st_counts_agree "$n_out" "N11: counts agree with rows"

  # N12: SAME members, order swapped (monitors.conf ↔ input.conf, file lines
  # 14/15 so the theme anchor at line 13 does not move). This is the existing
  # order/set split, recorded as a fixture — NOT new detection: include_graph
  # owns order and FAILs naming line 11, while sources_resolve stays PASS
  # because the set and every regular target are unchanged.
  local N12R="$NX/source-order"
  mkdir -p "$N12R"
  cp -a "$A/." "$N12R/"
  sed -i -e '\#^source = ~/.config/hypr/monitors.conf$#{h;d;}' \
         -e '\#^source = ~/.config/hypr/input.conf$#{G;}' \
         "$N12R/.config/hypr/hyprland.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N12R" --no-live 2>&1); n_rc=$?
  st_eq  "N12: exit 1 (same member set, order moved)" 1 "$n_rc"
  st_has "N12: DIVERGED verdict" "$n_out" "MADO_VERIFY: DIVERGED"
  st_row_detail "$n_out" hypr.root.include_graph FAIL \
    "line 11: got '~/.config/hypr/input.conf' want '~/.config/hypr/monitors.conf'" \
    "N12: the swap is named with the line and both members"
  st_row_detail "$n_out" hypr.root.sources_resolve PASS \
    "declared targets exist, member set exact" \
    "N12: the resolution row stays PASS — order belongs to the graph row"
  st_row_has "$n_out" hypr.root.sources_resolve PASS "N12: stable owner row id"
  st_row_has "$n_out" hypr.local.inventory PASS "N12 (isolation: the local census is untouched)"
  st_row_has "$n_out" theme.chain.hypr_include PASS "N12 (isolation: the line-13 theme anchor is held)"
  st_eq  "N12: exactly one hypr FAIL — the graph row" 1 \
    "$(printf '%s\n' "$n_out" | awk '$1=="hypr" && $3=="FAIL" {c++} END {print c+0}')"
  st_counts_agree "$n_out" "N12: counts agree with rows"

  # N13-N16 (round 14, pass 2): the policy's other arms, each a hermetic shape.
  # N13 is the positive control for the symlink rule; N14/N15 cover the
  # `unresolved:` classes; N16 proves the glob transport does not split a
  # filename containing a newline (the compgen line transport did).

  # N13: a symlink to a regular file is an accepted target (`-f` follows it).
  local N13R="$NX/direct-symlink"
  mkdir -p "$N13R"
  cp -a "$A/." "$N13R/"
  rm -f "$N13R/.local/share/omarchy/default/hypr/windows.conf"
  ln -s envs.conf "$N13R/.local/share/omarchy/default/hypr/windows.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N13R" --no-live 2>&1); n_rc=$?
  st_eq  "N13: exit 0 (a file symlink is a regular target)" 0 "$n_rc"
  st_has "N13: CLEAN verdict" "$n_out" "MADO_VERIFY: CLEAN"
  st_row_exact "$n_out" hypr.root.sources_resolve PASS \
    "declared targets exist, member set exact" \
    "N13: the followed link resolves — no non-regular token"
  st_row_has "$n_out" hypr.root.include_graph PASS "N13 (isolation: the source lines are untouched)"
  st_row_has "$n_out" hypr.local.inventory PASS "N13 (isolation: the local census is untouched)"
  st_counts_agree "$n_out" "N13: counts agree with rows"

  # N14: the toggle glob matches nothing → the pre-existing unresolved class.
  local N14R="$NX/glob-empty"
  mkdir -p "$N14R"
  cp -a "$A/." "$N14R/"
  rm -f "$N14R/.local/state/omarchy/toggles/hypr/window-no-gaps.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N14R" --no-live 2>&1); n_rc=$?
  st_eq  "N14: exit 1 (a zero-match glob does not pass)" 1 "$n_rc"
  st_has "N14: DIVERGED verdict" "$n_out" "MADO_VERIFY: DIVERGED"
  st_row_exact "$n_out" hypr.root.sources_resolve FAIL \
    "unresolved: ~/.local/state/omarchy/toggles/hypr/*.conf" \
    "N14: the declared glob is named once under unresolved"
  st_not_has "N14: no non-regular token for a non-match" "$n_out" "non-regular:"
  st_row_has "$n_out" hypr.toggle.no_gaps NOTE "N14 (collateral status: the toggle file is gone)"
  st_eq  "N14: exactly one hypr FAIL — the source row" 1 \
    "$(printf '%s\n' "$n_out" | awk '$1=="hypr" && $3=="FAIL" {c++} END {print c+0}')"
  st_counts_agree "$n_out" "N14: counts agree with rows"

  # N15: the glob matches a dangling symlink → unresolved, appended once.
  local N15R="$NX/glob-dangling"
  mkdir -p "$N15R"
  cp -a "$A/." "$N15R/"
  rm -f "$N15R/.local/state/omarchy/toggles/hypr/window-no-gaps.conf"
  ln -s gone.conf "$N15R/.local/state/omarchy/toggles/hypr/window-no-gaps.conf"
  n_out=$("$BASH_BIN" "$0" --root "$N15R" --no-live 2>&1); n_rc=$?
  st_eq  "N15: exit 1 (a matched dangling link does not resolve)" 1 "$n_rc"
  st_has "N15: DIVERGED verdict" "$n_out" "MADO_VERIFY: DIVERGED"
  st_row_exact "$n_out" hypr.root.sources_resolve FAIL \
    "unresolved: ~/.local/state/omarchy/toggles/hypr/*.conf" \
    "N15: the declared glob is named exactly once, never as non-regular"
  st_row_has "$n_out" hypr.toggle.no_gaps NOTE "N15 (collateral status: the toggle link is broken)"
  st_eq  "N15: exactly one hypr FAIL — the source row" 1 \
    "$(printf '%s\n' "$n_out" | awk '$1=="hypr" && $3=="FAIL" {c++} END {print c+0}')"
  st_counts_agree "$n_out" "N15: counts agree with rows"

  # N16: a regular glob member whose name contains a newline stays one member.
  # The NUL-delimited transport reads it whole; the old line-oriented compgen
  # transport split it into two phantom non-regular names.
  local N16R="$NX/glob-newline" N16N
  N16N=$'line\nbreak.conf'
  mkdir -p "$N16R"
  cp -a "$A/." "$N16R/"
  printf '# fixture newline-named toggle\n' \
    >"$N16R/.local/state/omarchy/toggles/hypr/$N16N"
  n_out=$("$BASH_BIN" "$0" --root "$N16R" --no-live 2>&1); n_rc=$?
  st_eq  "N16: exit 0 (a newline-named regular member is not split)" 0 "$n_rc"
  st_has "N16: CLEAN verdict" "$n_out" "MADO_VERIFY: CLEAN"
  st_row_exact "$n_out" hypr.root.sources_resolve PASS \
    "declared targets exist, member set exact" \
    "N16: the whole match set is regular — no phantom non-regular member"
  st_row_has "$n_out" hypr.root.include_graph PASS "N16 (isolation: the source lines are untouched)"
  st_row_has "$n_out" hypr.toggle.no_gaps PASS "N16 (isolation: the declared toggle is untouched)"
  st_counts_agree "$n_out" "N16: counts agree with rows"
  # >>> MADO-R8-BLOCK >>>
  # --- scenario S: snapshot + snapshot-diff freshness receipts (M8-3) ------
  # Hermetic: snapshots come from the fixture roots only (the sandboxed live
  # case has no hyprctl, so no substrate is read); the diff reads only files.
  local SNAP="$T/snap" S1 S2 S3 S4 S5 S6 sfix ssha
  mkdir -p "$SNAP"
  S1="$SNAP/clean.snap"; S2="$SNAP/broken.snap"; S3="$SNAP/live.snap"
  S4="$SNAP/created.snap"; S5="$SNAP/resha.snap"; S6="$SNAP/tampered.snap"

  sfix=$(find "$A" -type f | sort | xargs sha256sum | sha256sum)
  out=$("$BASH_BIN" "$0" --root "$A" --no-live --snapshot "$S1" 2>&1); rc=$?
  st_eq   "S1: the receipt run keeps the verdict exit (CLEAN=0)" 0 "$rc"
  st_has  "S1: the child verdict still prints" "$out" "MADO_VERIFY: CLEAN"
  st_has  "S1: the receipt names the file" "$out" "MADO_SNAPSHOT: WRITTEN $S1"
  st_eq   "S1: the verified plane is untouched (read-only proof)" "$sfix" \
    "$(find "$A" -type f | sort | xargs sha256sum | sha256sum)"
  if [ -f "$S1" ]; then st_ok; else st_bad "S1: no snapshot written at $S1"; fi
  st_eq   "S1: v1 magic on the first line" "# mado-verify snapshot v1" "$(head -1 "$S1")"
  st_eq   "S1: scope recorded" "file-plane" "$(sed -n 's/^# scope: //p' "$S1")"
  st_eq   "S1: '# rows:' agrees with the row lines" \
    "$(sed -n 's/^# rows: //p' "$S1")" "$(grep -c '^row|' "$S1")"
  st_has  "S1: rows are stored pipe-delimited" "$(cat "$S1")" \
    "row|hypr|hypr.root.orchestrator|PASS|0 settings lines (pure orchestrator)"
  st_eq   "S1: the stored PASS count equals the stored PASS rows" \
    "$(sed -n 's/^# counts: pass=\([0-9]*\).*/\1/p' "$S1")" "$(grep -c '|PASS|' "$S1")"

  out=$("$BASH_BIN" "$0" --root "$B" --no-live --snapshot "$S2" 2>&1); rc=$?
  st_eq  "S2: a DIVERGED run still exits 1" 1 "$rc"
  st_has "S2: the DIVERGED verdict prints" "$out" "MADO_VERIFY: DIVERGED"
  st_has "S2: the red run also gets a receipt" "$out" "MADO_SNAPSHOT: WRITTEN $S2"

  out=$("$BASH_BIN" "$0" --snapshot-diff "$S1" "$S2" 2>&1); rc=$?
  st_eq   "S3: a row-class move exits 1" 1 "$rc"
  st_has  "S3: verdict is CHANGED" "$out" "MADO_DIFF: CHANGED"
  st_has  "S3: the orchestrator regression is named" "$out" \
    "DIFF_ROW regressed hypr.root.orchestrator: PASS→FAIL"
  st_has  "S3: the walker regression is named" "$out" \
    "DIFF_ROW regressed walker.config: PASS→FAIL"
  st_has  "S3: a same-status detail move is classified detail" "$out" \
    "DIFF_ROW detail hypr.file.sha_pin: NOTE (detail changed)"
  st_has  "S3: the boundary-hash detail move is classified detail" "$out" \
    "DIFF_ROW detail boundary.readonly: PASS (detail changed)"
  st_has  "S3: the different roots are named as a scope move" "$out" \
    "DIFF_SCOPE root: $A → $B"
  st_has  "S3: scope counted" "$out" "scope=1"
  st_not_has "S3: the diff prints no MADO_VERIFY verdict" "$out" "MADO_VERIFY:"
  st_not_has "S3: a changed pair never reads SAME" "$out" "MADO_DIFF: SAME"

  sed 's/^# created:.*/# created: 1999-01-01T00:00:00Z/' "$S1" >"$S4"
  out=$("$BASH_BIN" "$0" --snapshot-diff "$S1" "$S4" 2>&1); rc=$?
  st_eq  "S4: receipt-time is provenance, not verdict data (SAME, exit 0)" 0 "$rc"
  st_has "S4: verdict is SAME" "$out" "MADO_DIFF: SAME"
  st_has "S4: no class noise" "$out" \
    "regressed=0 recovered=0 flipped=0 relaxed=0 relabeled=0 appeared=0 vanished=0"
  out=$("$BASH_BIN" "$0" --snapshot-diff "$S1" "$S1" 2>&1); rc=$?
  st_eq  "S4: a file diffed with itself is SAME (exit 0)" 0 "$rc"

  sed 's/^# gate-sha256:.*/# gate-sha256: 0000000000000000000000000000000000000000000000000000000000000000/' \
    "$S1" >"$S5"
  out=$("$BASH_BIN" "$0" --snapshot-diff "$S1" "$S5" 2>&1); rc=$?
  st_eq   "S5: a gate-revision move is a class change (exit 1)" 1 "$rc"
  st_has  "S5: the scope field is named" "$out" "DIFF_SCOPE gate-sha256:"
  st_has  "S5: scope counted" "$out" "scope=1"
  st_not_has "S5: no row-class noise" "$out" "DIFF_ROW"

  out=$(env PATH="$SANDBOX" MADO_VERIFY_LIVE=yes "$BASH_BIN" "$0" --root "$A" --live --snapshot "$S3" 2>&1); rc=$?
  st_eq  "S6: the sandboxed live run still exits 1 (UNKNOWN blocks CLEAN)" 1 "$rc"
  st_has "S6: a receipt is written under a degraded PATH" "$out" "MADO_SNAPSHOT: WRITTEN $S3"
  out=$("$BASH_BIN" "$0" --snapshot-diff "$S1" "$S3" 2>&1); rc=$?
  st_eq  "S6: a scope move is a class change (exit 1)" 1 "$rc"
  st_has "S6: the scope move is named" "$out" "DIFF_SCOPE scope: file-plane → live"
  st_has "S6: the live-plane row move is named" "$out" "DIFF_ROW regressed live.plane: SKIP→UNKNOWN"

  ssha=$(sha256sum "$S1")
  out=$("$BASH_BIN" "$0" --root "$A" --no-live --snapshot "$S1" 2>&1); rc=$?
  st_eq  "S7: an existing receipt is refused (exit 2)" 2 "$rc"
  st_has "S7: the refusal names the file" "$out" "MADO_SNAPSHOT: REFUSED (destination exists: $S1"
  st_eq  "S7: the existing receipt is byte-unchanged" "$ssha" "$(sha256sum "$S1")"
  out=$("$BASH_BIN" "$0" --snapshot 2>&1); rc=$?
  st_eq  "S7: --snapshot without a file is a usage error (exit 2)" 2 "$rc"
  out=$("$BASH_BIN" "$0" --snapshot "$SNAP/never.snap" --selftest 2>&1); rc=$?
  st_eq  "S7: --snapshot takes no --selftest (exit 2)" 2 "$rc"
  st_has "S7: the refusal names the flag" "$out" "usage error: --snapshot takes no --selftest"
  out=$("$BASH_BIN" "$0" --snapshot "$SNAP/never.snap" --bogus 2>&1); rc=$?
  st_eq  "S7: an unknown argument with --snapshot is refused (exit 2)" 2 "$rc"
  if [ ! -e "$SNAP/never.snap" ]; then st_ok; else st_bad "S7: a refused invocation wrote a file"; fi

  out=$("$BASH_BIN" "$0" --snapshot-diff "$S1" "$SNAP/nope.snap" 2>&1); rc=$?
  st_eq   "S8: a missing snapshot is SETUP (exit 2)" 2 "$rc"
  st_has  "S8: the SETUP names the file" "$out" "MADO_DIFF: SETUP (missing snapshot file:"
  st_not_has "S8: the diff never prints a MADO_VERIFY verdict" "$out" "MADO_VERIFY:"
  printf 'not a snapshot\n' >"$SNAP/junk.txt"
  out=$("$BASH_BIN" "$0" --snapshot-diff "$S1" "$SNAP/junk.txt" 2>&1); rc=$?
  st_eq  "S8: a file without the v1 magic is SETUP (exit 2)" 2 "$rc"
  st_has "S8: the refusal names the magic" "$out" "not a v1 snapshot"
  sed 's/^# counts: pass=[0-9]*/# counts: pass=99/' "$S1" >"$S6"
  out=$("$BASH_BIN" "$0" --snapshot-diff "$S1" "$S6" 2>&1); rc=$?
  st_eq  "S8: a tampered receipt that no longer reconciles is SETUP (exit 2)" 2 "$rc"
  st_has "S8: the refusal names the disagreement" "$out" "does not reconcile"

  out=$("$BASH_BIN" "$0" --snapshot-diff 2>&1); rc=$?
  st_eq  "S9: --snapshot-diff without files is a usage error (exit 2)" 2 "$rc"
  out=$("$BASH_BIN" "$0" --snapshot-diff "$S1" 2>&1); rc=$?
  st_eq  "S9: one snapshot is a usage error (exit 2)" 2 "$rc"
  out=$("$BASH_BIN" "$0" --snapshot-diff "$S1" "$S1" --live 2>&1); rc=$?
  st_eq  "S9: --snapshot-diff takes no --live (exit 2)" 2 "$rc"
  out=$("$BASH_BIN" "$0" --snapshot-diff --help 2>&1); rc=$?
  st_eq  "S9: --snapshot-diff --help exits 0" 0 "$rc"
  st_has "S9: the help documents the diff mode" "$out" "--snapshot-diff OLD NEW"
  st_has "S9: the help documents the diff verdicts" "$out" "MADO_DIFF:"
  out=$("$BASH_BIN" "$0" --snapshot --help 2>&1); rc=$?
  st_eq  "S9: --snapshot --help exits 0" 0 "$rc"
  st_has "S9: the help documents the snapshot mode" "$out" "--snapshot FILE"

  # S10: the class table itself, against a crafted pair (no child process) —
  # every row class is pinned by name, and the unchanged row must stay silent.
  local SCA="$SNAP/classes-a.snap" SCB="$SNAP/classes-b.snap"
  cat >"$SCA" <<'MADO_R8_CRAFT_A'
# mado-verify snapshot v1
# created: crafted
# tool: mado-verify.sh fixture
# gate-sha256: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# root: /fixture
# scope: file-plane
# mode-line: mode: file-plane only | root: /fixture | live layer: skipped (fixture)
# counts: pass=2 fail=2 unknown=1 skip=0 note=1
# rows: 6
row|fix|fix.recovered|FAIL|was red
row|fix|fix.flipped|FAIL|was fail
row|fix|fix.relaxed|UNKNOWN|was unknown
row|fix|fix.relabeled|NOTE|was note
row|fix|fix.vanished|PASS|goes away
row|fix|fix.stable|PASS|unchanged
MADO_R8_CRAFT_A
  cat >"$SCB" <<'MADO_R8_CRAFT_B'
# mado-verify snapshot v1
# created: crafted
# tool: mado-verify.sh fixture
# gate-sha256: ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# root: /fixture
# scope: file-plane
# mode-line: mode: file-plane only | root: /fixture | live layer: skipped (fixture)
# counts: pass=4 fail=0 unknown=1 skip=0 note=1
# rows: 6
row|fix|fix.recovered|PASS|was red
row|fix|fix.flipped|UNKNOWN|was fail
row|fix|fix.relaxed|NOTE|was unknown
row|fix|fix.relabeled|PASS|was note
row|fix|fix.appeared|PASS|new row
row|fix|fix.stable|PASS|unchanged
MADO_R8_CRAFT_B
  out=$("$BASH_BIN" "$0" --snapshot-diff "$SCA" "$SCB" 2>&1); rc=$?
  st_eq   "S10: the crafted pair exits 1 (classes moved)" 1 "$rc"
  st_has  "S10: recovered is named" "$out" "DIFF_ROW recovered fix.recovered: FAIL→PASS"
  st_has  "S10: flipped is named" "$out" "DIFF_ROW flipped fix.flipped: FAIL→UNKNOWN"
  st_has  "S10: relaxed is named" "$out" "DIFF_ROW relaxed fix.relaxed: UNKNOWN→NOTE"
  st_has  "S10: relabeled is named" "$out" "DIFF_ROW relabeled fix.relabeled: NOTE→PASS"
  st_has  "S10: appeared is named" "$out" "DIFF_ROW appeared fix.appeared: -→PASS"
  st_has  "S10: vanished is named" "$out" "DIFF_ROW vanished fix.vanished: PASS→-"
  st_has  "S10: the class tally is complete" "$out" \
    "regressed=0 recovered=1 flipped=1 relaxed=1 relabeled=1 appeared=1 vanished=1"
  st_has  "S10: the counts move is reported" "$out" "DIFF_COUNTS: pass 2→4 fail 2→0"
  st_not_has "S10: the unchanged row stays silent" "$out" "fix.stable"
  # <<< MADO-R8-BLOCK <<<

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
# Re-cut record — round 8 / M8-2 (omarchy plane + scenarios OM): the ten
# recorded defects were re-swept against the widened revision with the recorded
# spec, re-extracted from the heredoc below and checked byte-for-byte against
# SPEC_SHA before the sweep. Measured table identical to TABLE_MADO (10 killed
# / 0 survived / 0 inconclusive; MUTATE_RESTORE OK, target sha unchanged
# before/after). PIN_MADO moves c4c1afb7… → d2bcdb31…; TABLE_MADO is unchanged
# — the widening lost no kill. Evidence: /tmp/w8-mado-m8-2/sweep (scratch).
#
# Re-cut record — round 9 / M9-1 (theme plane: the §6 file rows + scenarios T):
# the note's paste-ready spec landed as theme_plane(), the suite's plane
# alternation widened to `theme` (seven awk sites) and the plane joined
# verify() — all outside the marked families, so the derived target moved and
# the pin was re-cut. The ten recorded defects were re-swept against the
# widened revision with the recorded spec, re-extracted from the heredoc below
# and checked byte-for-byte against SPEC_SHA before the sweep. Measured table
# identical to TABLE_MADO (10 killed / 0 survived / 0 inconclusive, kill-rate
# 100 %; MUTATE_RESTORE OK, target sha before == after). PIN_MADO moves
# d2bcdb31… → dc7c4141… (derived target 1,945 L, re-derived independently and
# cmp-identical); TABLE_MADO is unchanged — the widening lost no kill. The
# derived target's own suite read 163/163 in the control run. Evidence:
# /tmp/w9-mado-m9-1/recut (scratch, this round). The newly landed theme rows
# carry no defect of their own yet: a covering mutant for the theme clauses is
# owed by the sweep lane (round-6 reading rule 2) — recorded, not smoothed.
#
# Discipline: the harness (tameshi-shokunin/tools/mutate-and-run.sh) is
# consumed read-only — a needed change is a recommendation to tameshi, never a
# patch; its revision is printed as provenance, not gated (the kill table is
# the check). Scratch only under /tmp/mado-verify-regression.*; the gate never
# touches the config plane. Kept fixture dirs from THIS run's failing suite
# runs are removed by exact path (prefix-guarded); foreign /tmp dirs are left
# untouched. No compositor/session state is read or written.
#
# Re-cut record — round 13 / M13 (exact-set censuses): sources_resolve and
# hypr.local.inventory became exact-set comparisons with named missing/extra,
# the local expected set widened 12→13 by an append (gkeep), and scenarios N
# landed beside A/B/H — all outside the marked families, so the derived target
# moved and PIN_MADO is owed a measured re-cut by L1 (never edited to match
# reality, corpus/knowledge/gate-standing-use.md §5 rule 4). The embedded spec
# and SPEC_SHA are unchanged: the recorded D6 anchor is the 12-name list, which
# the append leaves byte-verbatim — D6's dropped member now dies on the
# exact-set guard. Until the recut the mode reads SETUP with the printed
# REGRESSION_RECUT command — never a stale PASS.
#
# Re-cut record — round 14 / M14 (regular-file source targets): sources_resolve
# now tests each declared target with `-f` (following file symlinks) and names
# non-regular direct targets and glob matches under `non-regular:`; the PASS
# text, the `unresolved:` class, the exact-set comparison and the order split
# are unchanged. N9-N16 cover directory, order, symlink, zero-match,
# dangling-glob and newline-regular cases outside the marked R7/R8 blocks.
# L1 measured the required re-cut: target cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96,
# historical spec unchanged, 10/10 KILLED, GREEN control, restore OK;
# .ufo/waves/round-14/evidence/regression-recut.txt and historical-results.tsv.
# PIN_MADO moves only from that measured table, never by blessing a mismatch.
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
PIN_MADO='cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96'
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

mado_r7_target_build() { # <src-file> <dest-file> — excise the MADO-R7/R8 marker blocks
  # The MADO-R8 pair wraps round-8's own additions (snapshot receipts + the
  # scenario-S selftest region). Excising it too keeps the derived target
  # byte-identical when that block rides along — a widening inside the pair
  # needs no re-cut; anything new outside every pair still does, as the pin
  # and its re-cut note in the header say.
  sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-REGRESSION-BLOCK <<<$/d' \
      -e '/^[[:space:]]*# >>> MADO-R7-SELFTEST-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-SELFTEST-BLOCK <<<$/d' \
      -e '/^[[:space:]]*# >>> MADO-R8-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R8-BLOCK <<<$/d' \
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
# >>> MADO-R8-BLOCK >>>
# ===========================================================================
# SNAPSHOT + SNAPSHOT-DIFF — freshness receipts (M8-3, round 8)
#
# Why: live verdicts move across a day and no single process can hold two of
# them. The receipt pair substitutes: snapshot one invocation now, snapshot a
# later one, then diff the two snapshots class by class.
#
#   mado-verify.sh --snapshot FILE [--no-live|--live] [--root DIR]
#       runs the gate as an ordinary invocation (the child's report and
#       MADO_VERIFY verdict are printed verbatim; the run's exit code is
#       preserved) and then writes a v1 snapshot of the verdict table to FILE.
#       FILE must not exist — receipts are never overwritten — and must not
#       land inside the verified <root>/.config plane. Refusals (MADO_SNAPSHOT:
#       REFUSED, exit 2, nothing written): FILE exists or sits in the config
#       plane; the run exits outside 0/1; the printed rows do not reconcile
#       with the printed counts (a row whose detail spans lines is refused,
#       never silently truncated); the write or its read-back fails.
#   mado-verify.sh --snapshot-diff OLD NEW
#       reads two snapshots (no substrate, no child process) and prints
#       DIFF_LEFT/DIFF_RIGHT provenance, DIFF_SCOPE per moved scope field
#       (tool / gate-sha256 / root / scope), one DIFF_ROW line per changed row
#       with its class, DIFF_DETAIL old/new for every moved detail, and
#       DIFF_COUNTS when the status tallies move. Classes:
#         regressed PASS|SKIP|NOTE → FAIL|UNKNOWN   recovered  FAIL|UNKNOWN → PASS
#         flipped   FAIL ↔ UNKNOWN                  relaxed    FAIL|UNKNOWN → SKIP|NOTE
#         relabeled any other status move           detail     same status, new detail
#         appeared  row only in NEW                 vanished   row only in OLD
#       Verdicts: MADO_DIFF: SAME (exit 0; nothing moved) ·
#       DETAIL-CHANGED (exit 0; details moved, classes did not) ·
#       CHANGED (exit 1; a row class or a scope field moved, counted) ·
#       SETUP (exit 2; a file is missing/malformed/edited — receipts are
#       self-checking: the stored counts must reconcile with the stored rows).
#       The diff never prints MADO_VERIFY: — that token belongs to the runs
#       being compared, whose output the snapshot mode passes through.
#
# Discipline: the snapshot write is the only write this mode makes, only to
# the named FILE, never into the verified config plane; the child is the
# ordinary gate under its own read-only discipline; the diff reads only the
# two named files. 'created:' is receipt-time provenance and is never
# compared. A refused snapshot writes nothing (a failed write is removed).
#
# Excision: this marker pair also wraps the scenario-S selftest region, and
# mado_r7_target_build excises the pair — the recorded regression target
# stays byte-identical while this block rides along (no re-cut for it). The
# gate's own usage text in usage() stays silent on these modes by the same
# invariant; --snapshot --help / --snapshot-diff --help print the contract.
# ===========================================================================
MADO_R8_SELF=$(readlink -f "$0" 2>/dev/null || printf '%s' "$0")
MADO_R8_ERR=''
MADO_R8_KEYS_L=()
MADO_R8_KEYS_R=()
declare -A MADO_R8_ST=()
declare -A MADO_R8_DT=()
declare -A MADO_R8_HDR=()
declare -A MADO_R8_CNT=()

mado_r8_snapshot_requested() { # "$@" → 0 when --snapshot / --snapshot= is present
  local a
  for a in "$@"; do
    case "$a" in --snapshot | --snapshot=*) return 0 ;; esac
  done
  return 1
}

mado_r8_diff_requested() { # "$@" → 0 when --snapshot-diff / --snapshot-diff= is present
  local a
  for a in "$@"; do
    case "$a" in --snapshot-diff | --snapshot-diff=*) return 0 ;; esac
  done
  return 1
}

mado_r8_usage_note() {
  cat <<'EOF'

  --snapshot FILE   run the gate (honouring --no-live/--live/--root) and write
                a v1 verdict snapshot to FILE (FILE must not exist; receipts
                are never overwritten). Exit = the run's verdict; the write
                adds MADO_SNAPSHOT: WRITTEN|REFUSED (a refusal exits 2).
  --snapshot-diff OLD NEW  diff two snapshots class by class; MADO_DIFF:
                SAME|DETAIL-CHANGED|CHANGED|SETUP (exit 0/0/1/2). Reads only
                the two files; never prints MADO_VERIFY:.
EOF
}

mado_r8_snapshot_cli() {
  local dest='' out='' rc=0 bash_bin line f1 f2 f3 rest
  local version_line mode_line counts_line scope root_f
  local cpass cfail cunk cskip cnote v kv
  local rpass=0 rfail=0 runk=0 rskip=0 rnote=0 total=0 body=''
  local gate_sha created content dd dreal cfg cfgr n_file
  local -a child=()
  bash_bin="${BASH:-/bin/bash}"

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --snapshot)
        shift
        [ "$#" -gt 0 ] || { printf 'usage error: --snapshot needs a file\n' >&2; usage >&2; return 2; }
        case "$1" in
          -h | --help) usage; mado_r8_usage_note; return 0 ;;
          -*) printf 'usage error: --snapshot needs a file (got %s)\n' "$1" >&2; usage >&2; return 2 ;;
        esac
        dest="$1"
        ;;
      --snapshot=*)
        dest="${1#--snapshot=}"
        [ -n "$dest" ] || { printf 'usage error: --snapshot needs a file\n' >&2; usage >&2; return 2; }
        ;;
      --no-live | --live) child+=("$1") ;;
      --root)
        shift
        [ "$#" -gt 0 ] || { printf 'usage error: --root needs a directory\n' >&2; usage >&2; return 2; }
        child+=(--root "$1")
        ;;
      --root=*) child+=("$1") ;;
      -h | --help) usage; mado_r8_usage_note; return 0 ;;
      --snapshot-diff | --snapshot-diff=* | --selftest | --regression)
        printf 'usage error: --snapshot takes no %s\n' "${1%%=*}" >&2; usage >&2; return 2 ;;
      *)
        printf 'usage error: unknown argument %s with --snapshot\n' "$1" >&2; usage >&2; return 2 ;;
    esac
    shift
  done
  [ -n "$dest" ] || { printf 'usage error: --snapshot needs a file\n' >&2; usage >&2; return 2; }
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    printf 'MADO_SNAPSHOT: REFUSED (destination exists: %s — receipts are never overwritten)\n' "$dest"
    return 2
  fi

  out=$("$bash_bin" "$MADO_R8_SELF" ${child[@]+"${child[@]}"} 2>&1)
  rc=$?
  printf '%s\n' "$out"
  case "$rc" in
    0 | 1) : ;;
    *)
      printf 'MADO_SNAPSHOT: REFUSED (the run exited %s — no verdict rows to receipt; nothing written)\n' "$rc"
      return 2
      ;;
  esac

  version_line=$(printf '%s\n' "$out" | head -1)
  mode_line=$(printf '%s\n' "$out" | sed -n '2p')
  counts_line=$(printf '%s\n' "$out" | grep -m1 '^counts: pass=' || true)
  case "$version_line" in
    'mado-verify.sh '*) : ;;
    *)
      printf 'MADO_SNAPSHOT: REFUSED (the run did not print a mado-verify report; first line: %s)\n' "${version_line:-<empty>}"
      return 2
      ;;
  esac
  case "$mode_line" in
    'mode: live (read-only) | root: '*) scope=live ;;
    'mode: file-plane only | root: '*) scope=file-plane ;;
    *)
      printf 'MADO_SNAPSHOT: REFUSED (cannot parse the mode line: %s)\n' "${mode_line:-<empty>}"
      return 2
      ;;
  esac
  root_f=${mode_line#*'| root: '}
  root_f=${root_f%%' | '*}
  if [ -z "$root_f" ] || [ "$root_f" = "$mode_line" ]; then
    printf 'MADO_SNAPSHOT: REFUSED (cannot parse the root from the mode line: %s)\n' "$mode_line"
    return 2
  fi
  if [ -z "$counts_line" ]; then
    printf 'MADO_SNAPSHOT: REFUSED (the run printed no counts line)\n'
    return 2
  fi
  cpass=0; cfail=0; cunk=0; cskip=0; cnote=0
  for kv in ${counts_line#counts: }; do
    case "$kv" in
      pass=*) cpass="${kv#pass=}" ;;
      fail=*) cfail="${kv#fail=}" ;;
      unknown=*) cunk="${kv#unknown=}" ;;
      skip=*) cskip="${kv#skip=}" ;;
      note=*) cnote="${kv#note=}" ;;
    esac
  done
  for v in "$cpass" "$cfail" "$cunk" "$cskip" "$cnote"; do
    case "$v" in
      '' | *[!0-9]*)
        printf 'MADO_SNAPSHOT: REFUSED (counts line unparseable: %s)\n' "$counts_line"
        return 2
        ;;
    esac
  done

  while IFS= read -r line; do
    read -r f1 f2 f3 rest <<<"$line"
    case "$f3" in
      PASS | FAIL | UNKNOWN | SKIP | NOTE)
        if [ -z "$f1" ] || [ -z "$f2" ] || [ -z "$rest" ]; then
          printf 'MADO_SNAPSHOT: REFUSED (row-shaped line without plane/id/detail: %s)\n' "$line"
          return 2
        fi
        case "$f3" in
          PASS) rpass=$((rpass + 1)) ;;
          FAIL) rfail=$((rfail + 1)) ;;
          UNKNOWN) runk=$((runk + 1)) ;;
          SKIP) rskip=$((rskip + 1)) ;;
          NOTE) rnote=$((rnote + 1)) ;;
        esac
        total=$((total + 1))
        printf -v body '%srow|%s|%s|%s|%s\n' "$body" "$f1" "$f2" "$f3" "$rest"
        ;;
    esac
  done <<<"$out"
  if [ "$total" = 0 ] || [ "$rpass" != "$cpass" ] || [ "$rfail" != "$cfail" ] ||
     [ "$runk" != "$cunk" ] || [ "$rskip" != "$cskip" ] || [ "$rnote" != "$cnote" ]; then
    printf 'MADO_SNAPSHOT: REFUSED (row parse does not reconcile with the printed counts: parsed total=%s pass=%s fail=%s unknown=%s skip=%s note=%s; printed pass=%s fail=%s unknown=%s skip=%s note=%s)\n' \
      "$total" "$rpass" "$rfail" "$runk" "$rskip" "$rnote" "$cpass" "$cfail" "$cunk" "$cskip" "$cnote"
    return 2
  fi

  case "$dest" in
    */*) dd="${dest%/*}" ;;
    *) dd='.' ;;
  esac
  dreal=$(cd "$dd" 2>/dev/null && pwd -P) || dreal=''
  if [ -n "$dreal" ] && [ -d "$root_f/.config" ]; then
    cfgr=$(cd "$root_f/.config" && pwd -P)
    case "$dreal/${dest##*/}" in
      "$cfgr"/*)
        printf 'MADO_SNAPSHOT: REFUSED (destination is inside the verified config plane: %s)\n' "$dest"
        return 2
        ;;
    esac
  fi

  gate_sha=$(sha256sum -- "$MADO_R8_SELF" 2>/dev/null || true)
  gate_sha=${gate_sha%% *}
  [ -n "$gate_sha" ] || gate_sha=unavailable
  created=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || true)
  [ -n "$created" ] || created=unavailable
  content="# mado-verify snapshot v1
# created: $created
# tool: $version_line
# gate-sha256: $gate_sha
# root: $root_f
# scope: $scope
# mode-line: $mode_line
# counts: pass=$cpass fail=$cfail unknown=$cunk skip=$cskip note=$cnote
# rows: $total
$body"
  if ! printf '%s' "$content" >"$dest" 2>/dev/null; then
    rm -f "$dest"
    printf 'MADO_SNAPSHOT: REFUSED (cannot write %s)\n' "$dest"
    return 2
  fi
  n_file=0
  while IFS= read -r line; do
    case "$line" in 'row|'*) n_file=$((n_file + 1)) ;; esac
  done <"$dest"
  if [ "$n_file" != "$total" ]; then
    rm -f "$dest"
    printf 'MADO_SNAPSHOT: REFUSED (write verification failed: %s row lines on disk vs %s expected)\n' "$n_file" "$total"
    return 2
  fi
  printf 'MADO_SNAPSHOT: WRITTEN %s (rows=%s pass=%s fail=%s unknown=%s skip=%s note=%s; scope=%s)\n' \
    "$dest" "$total" "$rpass" "$rfail" "$runk" "$rskip" "$rnote" "$scope"
  return "$rc"
}

mado_r8_load() { # <L|R> <file> → 0 loaded; 1 refused (message in MADO_R8_ERR)
  local side="$1" file="$2" line key k tag plane id st dt n=0
  local npass=0 nfail=0 nunk=0 nskip=0 nnote=0 total=0
  local h_created='' h_tool='' h_sha='' h_root='' h_scope='' h_modeline='' h_counts='' h_rows=''
  local kv v p='' f='' u='' s='' nt=''
  MADO_R8_ERR=''
  [ -f "$file" ] || { MADO_R8_ERR="missing snapshot file: $file"; return 1; }
  if [ "$side" = L ]; then MADO_R8_KEYS_L=(); else MADO_R8_KEYS_R=(); fi

  while IFS= read -r line || [ -n "$line" ]; do
    n=$((n + 1))
    if [ "$n" = 1 ]; then
      [ "$line" = '# mado-verify snapshot v1' ] || { MADO_R8_ERR="not a v1 snapshot (line 1): $file"; return 1; }
      continue
    fi
    case "$line" in
      '# created: '*) h_created="${line#'# created: '}" ;;
      '# tool: '*) h_tool="${line#'# tool: '}" ;;
      '# gate-sha256: '*) h_sha="${line#'# gate-sha256: '}" ;;
      '# root: '*) h_root="${line#'# root: '}" ;;
      '# scope: '*) h_scope="${line#'# scope: '}" ;;
      '# mode-line: '*) h_modeline="${line#'# mode-line: '}" ;;
      '# counts: '*) h_counts="${line#'# counts: '}" ;;
      '# rows: '*) h_rows="${line#'# rows: '}" ;;
      'row|'*)
        IFS='|' read -r tag plane id st dt <<<"$line"
        if [ -z "$plane" ] || [ -z "$id" ] || [ -z "$st" ] || [ -z "$dt" ]; then
          MADO_R8_ERR="malformed row at line $n in $file"; return 1
        fi
        key="$plane|$id"
        k="$side|$key"
        if [ -n "${MADO_R8_ST["$k"]+x}" ]; then
          MADO_R8_ERR="duplicate row $key in $file"; return 1
        fi
        MADO_R8_ST["$k"]="$st"
        MADO_R8_DT["$k"]="$dt"
        if [ "$side" = L ]; then MADO_R8_KEYS_L+=("$key"); else MADO_R8_KEYS_R+=("$key"); fi
        case "$st" in
          PASS) npass=$((npass + 1)) ;;
          FAIL) nfail=$((nfail + 1)) ;;
          UNKNOWN) nunk=$((nunk + 1)) ;;
          SKIP) nskip=$((nskip + 1)) ;;
          NOTE) nnote=$((nnote + 1)) ;;
        esac
        total=$((total + 1))
        ;;
      '#'*) : ;;
      *) MADO_R8_ERR="unexpected line $n in $file"; return 1 ;;
    esac
  done <"$file"

  [ -n "$h_tool" ] && [ -n "$h_sha" ] && [ -n "$h_root" ] && [ -n "$h_scope" ] && [ -n "$h_counts" ] || {
    MADO_R8_ERR="missing required header field(s) in $file"
    return 1
  }
  case "$h_scope" in
    live | file-plane) : ;;
    *) MADO_R8_ERR="bad scope '$h_scope' in $file"; return 1 ;;
  esac
  if [ "$total" = 0 ]; then MADO_R8_ERR="no rows in $file"; return 1; fi
  for kv in $h_counts; do
    case "$kv" in
      pass=*) p="${kv#pass=}" ;;
      fail=*) f="${kv#fail=}" ;;
      unknown=*) u="${kv#unknown=}" ;;
      skip=*) s="${kv#skip=}" ;;
      note=*) nt="${kv#note=}" ;;
    esac
  done
  for v in "$p" "$f" "$u" "$s" "$nt"; do
    case "$v" in
      '' | *[!0-9]*) MADO_R8_ERR="counts line unparseable in $file"; return 1 ;;
    esac
  done
  if [ "$p" != "$npass" ] || [ "$f" != "$nfail" ] || [ "$u" != "$nunk" ] || [ "$s" != "$nskip" ] || [ "$nt" != "$nnote" ]; then
    MADO_R8_ERR="receipt does not reconcile (rows pass=$npass fail=$nfail unknown=$nunk skip=$nskip note=$nnote vs counts pass=$p fail=$f unknown=$u skip=$s note=$nt) in $file"
    return 1
  fi
  if [ -n "$h_rows" ]; then
    case "$h_rows" in
      '' | *[!0-9]*) MADO_R8_ERR="bad # rows: field in $file"; return 1 ;;
    esac
    [ "$h_rows" = "$total" ] || { MADO_R8_ERR="# rows: $h_rows disagrees with $total row lines in $file"; return 1; }
  fi
  MADO_R8_HDR["$side|created"]="$h_created"
  MADO_R8_HDR["$side|tool"]="$h_tool"
  MADO_R8_HDR["$side|gate-sha256"]="$h_sha"
  MADO_R8_HDR["$side|root"]="$h_root"
  MADO_R8_HDR["$side|scope"]="$h_scope"
  MADO_R8_HDR["$side|mode-line"]="$h_modeline"
  MADO_R8_CNT["$side|pass"]="$npass"
  MADO_R8_CNT["$side|fail"]="$nfail"
  MADO_R8_CNT["$side|unknown"]="$nunk"
  MADO_R8_CNT["$side|skip"]="$nskip"
  MADO_R8_CNT["$side|note"]="$nnote"
  MADO_R8_CNT["$side|total"]="$total"
  return 0
}

mado_r8_class() { # <old-status> <new-status> → the change class (statuses differ)
  case "$1:$2" in
    PASS:FAIL | PASS:UNKNOWN | SKIP:FAIL | SKIP:UNKNOWN | NOTE:FAIL | NOTE:UNKNOWN)
      printf 'regressed' ;;
    FAIL:PASS | UNKNOWN:PASS)
      printf 'recovered' ;;
    FAIL:UNKNOWN | UNKNOWN:FAIL)
      printf 'flipped' ;;
    FAIL:SKIP | FAIL:NOTE | UNKNOWN:SKIP | UNKNOWN:NOTE)
      printf 'relaxed' ;;
    *)
      printf 'relabeled' ;;
  esac
}

mado_r8_diff_cli() {
  local old='' new='' okey rkey oid os od ns nd cls field l r
  local r_regressed=0 r_recovered=0 r_flipped=0 r_relaxed=0 r_relabeled=0
  local r_detail=0 r_appeared=0 r_vanished=0 scount=0 rowcls class_total
  local verdict rc

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --snapshot-diff)
        shift
        [ "$#" -gt 0 ] || { printf 'usage error: --snapshot-diff needs two snapshot files\n' >&2; usage >&2; return 2; }
        case "$1" in
          -h | --help) usage; mado_r8_usage_note; return 0 ;;
          -*) printf 'usage error: --snapshot-diff takes no %s\n' "$1" >&2; usage >&2; return 2 ;;
        esac
        old="$1"
        shift
        [ "$#" -gt 0 ] || { printf 'usage error: --snapshot-diff needs two snapshot files\n' >&2; usage >&2; return 2; }
        case "$1" in
          -h | --help) usage; mado_r8_usage_note; return 0 ;;
          -*) printf 'usage error: --snapshot-diff takes no %s\n' "$1" >&2; usage >&2; return 2 ;;
        esac
        new="$1"
        ;;
      --snapshot-diff=*)
        old="${1#--snapshot-diff=}"
        [ -n "$old" ] || { printf 'usage error: --snapshot-diff needs two snapshot files\n' >&2; usage >&2; return 2; }
        shift
        [ "$#" -gt 0 ] || { printf 'usage error: --snapshot-diff needs two snapshot files\n' >&2; usage >&2; return 2; }
        case "$1" in
          -h | --help) usage; mado_r8_usage_note; return 0 ;;
          -*) printf 'usage error: --snapshot-diff takes no %s\n' "$1" >&2; usage >&2; return 2 ;;
        esac
        new="$1"
        ;;
      -h | --help) usage; mado_r8_usage_note; return 0 ;;
      *)
        printf 'usage error: unexpected argument %s with --snapshot-diff\n' "$1" >&2; usage >&2; return 2 ;;
    esac
    shift
  done
  if [ -z "$old" ] || [ -z "$new" ]; then
    printf 'usage error: --snapshot-diff needs two snapshot files\n' >&2; usage >&2; return 2
  fi

  mado_r8_load L "$old" || { printf 'MADO_DIFF: SETUP (%s)\n' "$MADO_R8_ERR"; return 2; }
  mado_r8_load R "$new" || { printf 'MADO_DIFF: SETUP (%s)\n' "$MADO_R8_ERR"; return 2; }

  printf 'DIFF_LEFT: %s created=%s scope=%s root=%s gate-sha256=%s tool=%s\n' \
    "$old" "${MADO_R8_HDR['L|created']}" "${MADO_R8_HDR['L|scope']}" "${MADO_R8_HDR['L|root']}" \
    "${MADO_R8_HDR['L|gate-sha256']}" "${MADO_R8_HDR['L|tool']}"
  printf 'DIFF_RIGHT: %s created=%s scope=%s root=%s gate-sha256=%s tool=%s\n' \
    "$new" "${MADO_R8_HDR['R|created']}" "${MADO_R8_HDR['R|scope']}" "${MADO_R8_HDR['R|root']}" \
    "${MADO_R8_HDR['R|gate-sha256']}" "${MADO_R8_HDR['R|tool']}"
  for field in tool gate-sha256 root scope; do
    l="${MADO_R8_HDR["L|$field"]}"
    r="${MADO_R8_HDR["R|$field"]}"
    if [ "$l" != "$r" ]; then
      printf 'DIFF_SCOPE %s: %s → %s\n' "$field" "$l" "$r"
      scount=$((scount + 1))
    fi
  done

  for okey in "${MADO_R8_KEYS_L[@]}"; do
    oid="${okey#*|}"
    os="${MADO_R8_ST["L|$okey"]}"
    od="${MADO_R8_DT["L|$okey"]}"
    if [ -z "${MADO_R8_ST["R|$okey"]+x}" ]; then
      printf 'DIFF_ROW vanished %s: %s→-\n' "$oid" "$os"
      printf 'DIFF_DETAIL %s old: %s\n' "$oid" "$od"
      r_vanished=$((r_vanished + 1))
      continue
    fi
    ns="${MADO_R8_ST["R|$okey"]}"
    nd="${MADO_R8_DT["R|$okey"]}"
    if [ "$os" = "$ns" ]; then
      if [ "$od" = "$nd" ]; then continue; fi
      printf 'DIFF_ROW detail %s: %s (detail changed)\n' "$oid" "$os"
      printf 'DIFF_DETAIL %s old: %s\n' "$oid" "$od"
      printf 'DIFF_DETAIL %s new: %s\n' "$oid" "$nd"
      r_detail=$((r_detail + 1))
      continue
    fi
    cls=$(mado_r8_class "$os" "$ns")
    printf 'DIFF_ROW %s %s: %s→%s\n' "$cls" "$oid" "$os" "$ns"
    case "$cls" in
      regressed) r_regressed=$((r_regressed + 1)) ;;
      recovered) r_recovered=$((r_recovered + 1)) ;;
      flipped) r_flipped=$((r_flipped + 1)) ;;
      relaxed) r_relaxed=$((r_relaxed + 1)) ;;
      relabeled) r_relabeled=$((r_relabeled + 1)) ;;
    esac
    if [ "$od" != "$nd" ]; then
      printf 'DIFF_DETAIL %s old: %s\n' "$oid" "$od"
      printf 'DIFF_DETAIL %s new: %s\n' "$oid" "$nd"
      r_detail=$((r_detail + 1))
    fi
  done
  for rkey in "${MADO_R8_KEYS_R[@]}"; do
    [ -z "${MADO_R8_ST["L|$rkey"]+x}" ] || continue
    printf 'DIFF_ROW appeared %s: -→%s\n' "${rkey#*|}" "${MADO_R8_ST["R|$rkey"]}"
    printf 'DIFF_DETAIL %s new: %s\n' "${rkey#*|}" "${MADO_R8_DT["R|$rkey"]}"
    r_appeared=$((r_appeared + 1))
  done

  if [ "${MADO_R8_CNT['L|pass']}" != "${MADO_R8_CNT['R|pass']}" ] ||
     [ "${MADO_R8_CNT['L|fail']}" != "${MADO_R8_CNT['R|fail']}" ] ||
     [ "${MADO_R8_CNT['L|unknown']}" != "${MADO_R8_CNT['R|unknown']}" ] ||
     [ "${MADO_R8_CNT['L|skip']}" != "${MADO_R8_CNT['R|skip']}" ] ||
     [ "${MADO_R8_CNT['L|note']}" != "${MADO_R8_CNT['R|note']}" ]; then
    printf 'DIFF_COUNTS: pass %s→%s fail %s→%s unknown %s→%s skip %s→%s note %s→%s\n' \
      "${MADO_R8_CNT['L|pass']}" "${MADO_R8_CNT['R|pass']}" \
      "${MADO_R8_CNT['L|fail']}" "${MADO_R8_CNT['R|fail']}" \
      "${MADO_R8_CNT['L|unknown']}" "${MADO_R8_CNT['R|unknown']}" \
      "${MADO_R8_CNT['L|skip']}" "${MADO_R8_CNT['R|skip']}" \
      "${MADO_R8_CNT['L|note']}" "${MADO_R8_CNT['R|note']}"
  fi

  rowcls=$((r_regressed + r_recovered + r_flipped + r_relaxed + r_relabeled + r_appeared + r_vanished))
  class_total=$((rowcls + scount))
  verdict=SAME
  rc=0
  if [ "$class_total" -gt 0 ]; then
    verdict=CHANGED
    rc=1
  elif [ "$r_detail" -gt 0 ]; then
    verdict=DETAIL-CHANGED
  fi
  printf 'MADO_DIFF: %s (rows %s→%s; regressed=%s recovered=%s flipped=%s relaxed=%s relabeled=%s appeared=%s vanished=%s; detail-changed=%s; scope=%s)\n' \
    "$verdict" "${MADO_R8_CNT['L|total']}" "${MADO_R8_CNT['R|total']}" \
    "$r_regressed" "$r_recovered" "$r_flipped" "$r_relaxed" "$r_relabeled" \
    "$r_appeared" "$r_vanished" "$r_detail" "$scount"
  return "$rc"
}

if mado_r8_diff_requested "$@"; then
  mado_r8_diff_cli "$@"
  exit $?
fi
if mado_r8_snapshot_requested "$@"; then
  mado_r8_snapshot_cli "$@"
  exit $?
fi
# <<< MADO-R8-BLOCK <<<

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
    local off hyprd
    hyprd=$(grep -nE '^[[:space:]]*#[[:space:]]*hyprlang' "$f" | head -1)
    off=$(grep -nEv '^[[:space:]]*(#|$)|^[[:space:]]*source[[:space:]]*=' "$f" | head -3)
    if [ -n "$hyprd" ]; then
      row hypr hypr.root.orchestrator FAIL \
        "unsupported hyprlang directive at line ${hyprd%%:*} — conditional source semantics are not modelled"
    elif [ -z "$off" ]; then
      row hypr hypr.root.orchestrator PASS "0 settings lines (pure orchestrator)"
    else
      row hypr hypr.root.orchestrator FAIL "non-source lines: $(printf '%s' "$off" | tr '\n' ' ')"
    fi

    # Erratum (round 12, 2026-10-19): 17→18 source lines (+ ~/.config/hypr/gkeep.conf
    # after ai-usage.conf; root sha 4f52854a3c143dcf… → ce7483f35ab52bc2…) after the
    # operator-applied gkeep installer (~/Projects/gkeep/install.sh:21-36); backup
    # epoch 1792267376 = 2026-10-17T20:02:56Z. Round 12 kept LOCAL at the MADO-1 list
    # of 12 and left the set-blind local census open as M13 (corpus/lessons/round-12.md);
    # that erratum cited the drift note's re-anchor protocol, which does not govern a
    # gate EXPECT — the governing rule is corpus/knowledge/gate-standing-use.md §5
    # rule 4 (a moved anchor reports itself; the response is re-verification plus an
    # appended erratum), as recorded in lessons round-12 R12-b.
    # Round 13 (2026-10-20, M13): LOCAL is the exact 13-name expected set (gkeep
    # appended after the recorded 12-name list, so the recorded spec's D6 anchor
    # stays byte-verbatim) and both censuses are exact-set comparisons with named
    # missing/extra; EXPECT stays 18 and SPEC_SHA is unchanged. The regression
    # PIN is re-cut by L1 from the measured sweep — never edited to match reality
    # (§5 rule 4). Re-measure with:
    # grep -cE '^[[:space:]]*source[[:space:]]*=' ~/.config/hypr/hyprland.conf;
    # sha256sum ~/.config/hypr/hyprland.conf.bak.1792267376 ~/.config/hypr/hyprland.conf;
    # diff -u ~/.config/hypr/hyprland.conf.bak.1792267376 ~/.config/hypr/hyprland.conf
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
      '~/.config/hypr/ai-usage.conf' \
      '~/.config/hypr/gkeep.conf' )
    local -a got=() miss="" sdiff=""
    mapfile -t got < <(awk '/^[[:space:]]*source[[:space:]]*=/{sub(/^[^=]*=[[:space:]]*/, ""); sub(/[[:space:]]+$/, ""); print}' "$f")
    local i
    # exact-set census (round 13, M13): membership is compared first so any
    # FAIL names the substituted members — a count-only or first-position
    # message is set-blind when one undeclared line replaces one declared line.
    # The positional walk below stays the PASS criterion (MADO-1 §3 order).
    local -A seen=() declared=()
    for i in "${EXPECT[@]}"; do declared["$i"]=1; done
    for i in "${got[@]}"; do
      [ -n "$i" ] && seen["$i"]=1
    done
    for i in "${EXPECT[@]}"; do [ -n "${seen["$i"]:-}" ] || sdiff="$sdiff missing: $i"; done
    for i in "${got[@]}"; do
      if [ -z "$i" ]; then sdiff="$sdiff extra: ''"; continue; fi
      [ -n "${declared["$i"]:-}" ] || sdiff="$sdiff extra: $i"
    done
    if [ "${#got[@]}" -ne "${#EXPECT[@]}" ]; then
      miss="${#got[@]} source lines (expected ${#EXPECT[@]})"
    else
      for i in "${!EXPECT[@]}"; do
        if [ "${got[$i]}" != "${EXPECT[$i]}" ]; then
          miss="line $((i + 1)): got '${got[$i]}' want '${EXPECT[$i]}'"
          break
        fi
      done
    fi
    if [ -n "$miss" ]; then
      row hypr hypr.root.include_graph FAIL "$miss$sdiff"
    else
      row hypr hypr.root.include_graph PASS "${#got[@]}/${#EXPECT[@]} sources, order exact, set exact"
    fi

    # every source target must resolve under $ROOT as a REGULAR file (~ expanded;
    # a glob must match ≥1 path and every match must be a regular file), and the
    # observed source set must equal the declared one (round 13, M13): a
    # same-count substitution whose replacement target happens to exist is
    # invisible to target-existence alone, so the members are named as well.
    #
    # Regular-file test (round 14): `[ -f ]` follows symlinks on purpose — a
    # symlink to a regular file is accepted, while a directory, a symlink to a
    # directory, or any other non-regular path is refused by name under
    # `non-regular:` (owner row: hypr.root.sources_resolve). A direct target
    # that does not exist keeps the pre-existing `unresolved:` class, and so
    # does a glob with zero matches; the two name classes are not repurposed.
    # The check reads metadata only — it never opens or writes a target.
    local t x m tmiss="" tnr="" tset=""
    local -A tseen=() tdecl=()
    for t in "${EXPECT[@]}"; do tdecl["$t"]=1; done
    for t in "${got[@]}"; do
      [ -n "$t" ] && tseen["$t"]=1
    done
    for t in "${EXPECT[@]}"; do
      [ -n "${tseen["$t"]:-}" ] || tset="$tset missing: $t"
      case "$t" in
        '~'*) x="$ROOT${t#\~}" ;;
        *) x="$t" ;;
      esac
      case "$x" in
        *'*'*)
          # glob target: ≥1 match required, and every match must be a regular
          # file. A mixed match set names only the non-regular members, so a
          # legitimate *.conf beside a directory-shaped one is never refused.
          # A matched dangling symlink does not resolve (`unresolved:`); any
          # other non-`-f` match — directory, link to a directory, FIFO,
          # socket, device — is named under `non-regular:`.
          #
          # Matches are collected NUL-delimited from a nullglob expansion in a
          # subshell (IFS empty, so no field splitting; nullglob scoped there),
          # not from line-oriented compgen output: a filename containing a
          # space or a newline stays one member. Only `*` is treated as a glob
          # (the pre-existing grammar).
          local -a gmatch=()
          local gdang=0
          mapfile -d '' -t gmatch < <(
            shopt -s nullglob
            IFS=
            gsub=( $x )
            for g in "${gsub[@]}"; do printf '%s\0' "$g"; done
          )
          if [ "${#gmatch[@]}" -eq 0 ]; then
            tmiss="$tmiss $t"
          else
            for m in "${gmatch[@]}"; do
              if [ -f "$m" ]; then continue; fi
              if [ -L "$m" ] && [ ! -e "$m" ]; then gdang=1; else tnr="$tnr $(src_disp "$m")"; fi
            done
            # one declared token, however many matched links are broken: the
            # unresolved class names the source line, not each dangling match.
            [ "$gdang" = 1 ] && tmiss="$tmiss $t"
          fi
          ;;
        *)
          if [ -f "$x" ]; then continue; fi
          if [ -e "$x" ]; then tnr="$tnr $(src_disp "$x")"; else tmiss="$tmiss $t"; fi
          ;;
      esac
    done
    for t in "${got[@]}"; do
      if [ -z "$t" ]; then tset="$tset extra: ''"; continue; fi
      [ -n "${tdecl["$t"]:-}" ] || tset="$tset extra: $t"
    done
    if [ -z "$tmiss" ] && [ -z "$tnr" ] && [ -z "$tset" ]; then
      row hypr hypr.root.sources_resolve PASS "declared targets exist, member set exact"
    else
      local tdetail=""
      [ -n "$tmiss" ] && tdetail="unresolved:$tmiss"
      [ -n "$tnr" ] && tdetail="${tdetail:+$tdetail }non-regular:$tnr"
      [ -n "$tset" ] && tdetail="${tdetail:+$tdetail }$tset"
      row hypr hypr.root.sources_resolve FAIL "$tdetail"
    fi
  else
    row hypr hypr.root.orchestrator UNKNOWN "hyprland.conf missing"
    row hypr hypr.root.include_graph UNKNOWN "hyprland.conf missing"
    row hypr hypr.root.sources_resolve UNKNOWN "hyprland.conf missing"
  fi

  # 13 active local confs, exact set (MADO-1 §2 + gkeep; round 13, M13):
  # a declared regular file may not be absent and no undeclared regular *.conf
  # file may sit in the directory (directories are not loadable confs and stay
  # out of both sides of the census). A presence-only tally cannot see a stray
  # substitution — that silence was M13 (corpus/lessons/round-12.md), so the
  # observed set is compared exactly and each side is named on FAIL.
  local -a LOCAL=(hyprland bindings input monitors looknfeel hypridle hyprlock hyprsunset ai-usage autostart envs xdph)
  # gkeep joins the declared set as an append (round 13, M13). The recorded
  # tameshi spec's D6 anchor is the list above, byte-verbatim, so the append —
  # not an edited list — keeps the recorded case recorded and moves only
  # PIN_MADO at the re-cut. D6's dropped member now dies on the exact-set guard
  # (the observed file becomes an extra), not on a presence tally.
  LOCAL+=(gkeep)
  local n x xq lmiss="" lextra=""
  local -a lobs=()
  for x in "$H"/*.conf; do
    [ -f "$x" ] && lobs+=("${x##*/}")
  done
  local -A lexp=()
  for x in "${LOCAL[@]}"; do lexp["$x.conf"]=1; done
  n=0
  for x in "${LOCAL[@]}"; do
    if [ -f "$H/$x.conf" ]; then
      n=$((n + 1))
    else
      printf -v xq '%q' "$x.conf"
      lmiss="$lmiss $xq"
    fi
  done
  for x in "${lobs[@]}"; do
    if [ -z "${lexp["$x"]:-}" ]; then
      printf -v xq '%q' "$x"
      lextra="$lextra $xq"
    fi
  done
  if [ -z "$lmiss" ] && [ -z "$lextra" ]; then
    row hypr hypr.local.inventory PASS "$n/${#LOCAL[@]} active local confs, set exact"
  else
    local ldetail=""
    [ -n "$lmiss" ] && ldetail="missing:$lmiss"
    [ -n "$lextra" ] && ldetail="${ldetail:+$ldetail }extra:$lextra"
    row hypr hypr.local.inventory FAIL "$ldetail"
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
  # plane: omarchy — freshness / version-drift watch (M6-2 note §2/§6; M8-2)
  # -------------------------------------------------------------------------
  omarchy_plane

  # -------------------------------------------------------------------------
  # plane: theme — declared file chain (theme-wallpaper-plane.md §6; M9-1)
  # -------------------------------------------------------------------------
  theme_plane

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
# plane: omarchy — freshness / version-drift watch (MADO-R6-2, round 8 / M8-2)
#
# Landed from corpus/knowledge/omarchy-drift-watch.md §2/§6. The watch becomes
# a verdict-bearing arm: the note's pins are held as the constants below, in
# line, with the note cited — the gate never *parses* the note. A prose parser
# would tie the verdict to the repo's working tree instead of to the substrate,
# and its own failure would surface as a self-inflicted UNKNOWN. Re-anchoring
# is an appended erratum in the note (old→new + reason + command); the baseline
# is never edited to match reality, and a MOVED pin is reported first.
#
# Verdict-bearing: version cmd (P1) + file (P2), git tag (P3) + HEAD (P3),
# link topology (P5), leaf sha (P4), worktree-vs-HEAD blob (index-free dirty
# check), command groups (derived). Record-level NOTEs: theme (D-1: operator-
# owned mutable state — a routine theme change must not turn the gate
# permanently red; HELD|MOVED is printed in the detail), the surface counter,
# and the docs register (C5/C6/C8). An unavailable probe reads UNKNOWN and
# blocks CLEAN (C7) — never a silent pass (SKILL safety rule 5).
#
# Read-only, §6 guard list only: `omarchy version|theme current|commands
# --json --all`, `git describe|rev-parse|show`, `readlink`, `sha256sum`.
# Never `git status`/`fetch` on the checkout (index stat-cache refresh,
# province-accuracy-selfaudit.md:110-128) and never a mutating omarchy verb
# (`theme set`, `restart *`, `refresh *`, `install *`, `setup *`, `update`).
# Root-splitting per §6: file/link/git rows read $ROOT; PATH probes follow the
# live-skip semantics exactly like the hypr-live plane.
# ===========================================================================
OMARCHY_VERSION_PIN="3.8.3"
OMARCHY_TAG_PIN="v3.8.4"
OMARCHY_HEAD_PIN="8fcc9d6048af4cb0e3af8512c78049857a3b53dd"
OMARCHY_SKILL_SHA_PIN="becd149e4d1c0767a80bcc1eb84e86e509149dc1e4b3d680cf24ab54bea5256d"
OMARCHY_SKILL_LINK_TARGET=".local/share/omarchy/default/omarchy-skill"
OMARCHY_SKILL_REL="default/omarchy-skill/SKILL.md"
OMARCHY_THEME_PIN="Matte Black"
OMARCHY_CMD_SURFACE_PIN=282
OMARCHY_SKILL_GROUPS="refresh restart toggle theme install launch capture reminder pkg setup update"

omarchy_plane() {
  local tree="$ROOT/.local/share/omarchy"
  local link="$ROOT/.agents/skills/omarchy"
  local leaf="$link/SKILL.md"
  local target="$ROOT/$OMARCHY_SKILL_LINK_TARGET"
  local nolive=""
  [ "$LIVE" = 0 ] && nolive="live layer skipped ($live_skipped_reason)"

  # --- file rows (root-scoped; run in both modes) --------------------------
  # The install marker is the `version` file (P2), not the directory: fixture
  # roots carry a partial tree (build_fixture writes default/hypr/*) and must
  # not read as broken installs.
  local vf="$tree/version" got
  if [ ! -f "$vf" ]; then
    if [ "$ROOT" = "$HOME" ]; then
      row omarchy omarchy.version.file FAIL "missing $vf (install broken)"
      row omarchy omarchy.skill.link FAIL "no omarchy install at $tree (link topology unverifiable)"
      row omarchy omarchy.skill.sha FAIL "no omarchy install at $tree (skill sha unverifiable)"
    else
      local why="no omarchy install under non-home root $ROOT (plane anchored to the HOME install)"
      row omarchy omarchy.version.file SKIP "$why"
      row omarchy omarchy.skill.link SKIP "$why"
      row omarchy omarchy.skill.sha SKIP "$why"
    fi
  else
    got=$(head -1 "$vf" 2>/dev/null | tr -d '[:space:]')
    if [ "$got" = "$OMARCHY_VERSION_PIN" ]; then
      row omarchy omarchy.version.file PASS "HELD: version file '$got' (P2 pin; == HEAD:version blob at the pinned HEAD)"
    else
      row omarchy omarchy.version.file FAIL "MOVED: version file '$got' != pin $OMARCHY_VERSION_PIN (re-anchor the note, never the pin)"
    fi

    if [ ! -L "$link" ]; then
      if [ -e "$link" ]; then
        row omarchy omarchy.skill.link FAIL "MOVED: $link is a real directory, not a symlink into the checkout (a copy may not masquerade as the live skill)"
      else
        row omarchy omarchy.skill.link FAIL "MOVED: $link missing (skill not installed)"
      fi
    elif ! have readlink; then
      row omarchy omarchy.skill.link UNKNOWN "readlink not on PATH — link target unresolved"
    else
      local lr
      lr=$(readlink -f "$link" 2>/dev/null || true)
      if [ "$lr" = "$target" ]; then
        row omarchy omarchy.skill.link PASS "HELD: symlink into the checkout (one file; nothing to drift)"
      elif [ -z "$lr" ]; then
        row omarchy omarchy.skill.link FAIL "MOVED: dangling symlink $link"
      else
        row omarchy omarchy.skill.link FAIL "MOVED: retargeted to $lr (want $target)"
      fi
    fi

    if ! have sha256sum; then
      row omarchy omarchy.skill.sha UNKNOWN "sha256sum not on PATH"
    elif [ ! -f "$leaf" ]; then
      row omarchy omarchy.skill.sha FAIL "MOVED: skill leaf unreadable ($leaf)"
    else
      local ss
      ss=$(sha256sum "$leaf" 2>/dev/null | cut -d' ' -f1)
      if [ "$ss" = "$OMARCHY_SKILL_SHA_PIN" ]; then
        row omarchy omarchy.skill.sha PASS "HELD: leaf sha256 ${ss:0:12}… (P4 pin)"
      else
        row omarchy omarchy.skill.sha FAIL "MOVED: leaf sha256 ${ss:0:12}… != pin ${OMARCHY_SKILL_SHA_PIN:0:12}…"
      fi
    fi
  fi

  # --- live rows (PATH/repo probes; SKIP under --no-live, UNKNOWN if absent) -
  local omtree=0
  [ -d "$tree/.git" ] && omtree=1
  if [ -n "$nolive" ]; then
    row omarchy omarchy.version.cmd SKIP "$nolive"
    row omarchy omarchy.git.tag SKIP "$nolive"
    row omarchy omarchy.git.head SKIP "$nolive"
    row omarchy omarchy.skill.vs_head SKIP "$nolive"
    row omarchy omarchy.cmd.groups SKIP "$nolive"
    row omarchy omarchy.cmd.surface SKIP "$nolive"
    row omarchy omarchy.theme SKIP "$nolive"
  else
    if ! have omarchy; then
      row omarchy omarchy.version.cmd UNKNOWN "omarchy not on PATH — version pin unverified (blocks CLEAN)"
    else
      local ov orc
      ov=$(tmo omarchy version 2>/dev/null); orc=$?
      if [ "$orc" != 0 ] || [ -z "$ov" ]; then
        row omarchy omarchy.version.cmd UNKNOWN "'omarchy version' failed (rc=$orc) — pin unverified"
      else
        ov=$(printf '%s' "$ov" | head -1 | tr -d '[:space:]')
        if [ "$ov" = "$OMARCHY_VERSION_PIN" ]; then
          row omarchy omarchy.version.cmd PASS "HELD: 'omarchy version' → $ov (P1 pin)"
        else
          row omarchy omarchy.version.cmd FAIL "MOVED: 'omarchy version' → '${ov:-<empty>}' != pin $OMARCHY_VERSION_PIN"
        fi
      fi
    fi

    if ! have git; then
      row omarchy omarchy.git.tag UNKNOWN "git not on PATH — checkout identity unverified"
      row omarchy omarchy.git.head UNKNOWN "git not on PATH — checkout identity unverified"
    elif [ "$omtree" = 0 ]; then
      row omarchy omarchy.git.tag UNKNOWN "no git checkout at $tree"
      row omarchy omarchy.git.head UNKNOWN "no git checkout at $tree"
    else
      local gt gh grc
      gt=$(tmo git -C "$tree" describe --tags --exact-match 2>/dev/null); grc=$?
      gt=$(printf '%s' "$gt" | head -1)
      if [ "$grc" != 0 ]; then
        row omarchy omarchy.git.tag UNKNOWN "git describe failed (rc=$grc) — tag pin unverified"
      elif [ "$gt" = "$OMARCHY_TAG_PIN" ]; then
        row omarchy omarchy.git.tag PASS "HELD: $gt exactly at HEAD (P3 pin)"
      else
        row omarchy omarchy.git.tag FAIL "MOVED: describe --tags --exact-match → '${gt:-<none>}' != pin $OMARCHY_TAG_PIN"
      fi
      gh=$(tmo git -C "$tree" rev-parse HEAD 2>/dev/null); grc=$?
      gh=$(printf '%s' "$gh" | head -1)
      if [ "$grc" != 0 ]; then
        row omarchy omarchy.git.head UNKNOWN "git rev-parse failed (rc=$grc) — HEAD unverified"
      elif [ "$gh" = "$OMARCHY_HEAD_PIN" ]; then
        row omarchy omarchy.git.head PASS "HELD: ${gh:0:8} (P3 pin)"
      else
        row omarchy omarchy.git.head FAIL "MOVED: rev-parse HEAD → '${gh:-<none>}' != pin ${OMARCHY_HEAD_PIN:0:8}… (every pin held at the old HEAD needs re-verification)"
      fi
    fi

    if ! have git || [ "$omtree" = 0 ] || ! have sha256sum || [ ! -f "$leaf" ]; then
      row omarchy omarchy.skill.vs_head UNKNOWN "checkout or leaf unreadable — worktree/HEAD relation unverified"
    else
      local blob sw
      blob=$(tmo git -C "$tree" show "HEAD:$OMARCHY_SKILL_REL" 2>/dev/null | sha256sum | cut -d' ' -f1)
      sw=$(sha256sum "$leaf" 2>/dev/null | cut -d' ' -f1)
      if [ -z "$blob" ]; then
        row omarchy omarchy.skill.vs_head UNKNOWN "cannot read HEAD:$OMARCHY_SKILL_REL from the checkout"
      elif [ "$blob" = "$sw" ]; then
        row omarchy omarchy.skill.vs_head PASS "worktree == HEAD blob (index-free; no local edit)"
      else
        row omarchy omarchy.skill.vs_head FAIL "MOVED: worktree ${sw:0:12}… != HEAD blob ${blob:0:12}… (local edit; editing the skill edits the checkout)"
      fi
    fi

    if ! have omarchy || [ "$PY_OK" = 0 ]; then
      row omarchy omarchy.cmd.groups UNKNOWN "omarchy or python3 not on PATH — command surface unverified"
      row omarchy omarchy.cmd.surface NOTE "probe unavailable; surface counter not read"
    else
      local cj co crc
      cj=$(tmo omarchy commands --json --all 2>/dev/null)
      co=$(printf '%s' "$cj" | python3 -c '
import json, sys
want = sys.argv[1].split()
try:
    d = json.load(sys.stdin)
except Exception:
    print("parse-error"); raise SystemExit(6)
rows = d.get("commands") if isinstance(d, dict) else None
if not isinstance(rows, list):
    print("shape-error"); raise SystemExit(6)
groups = {c.get("group") for c in rows if isinstance(c, dict)}
missing = [g for g in want if g not in groups]
print("%d %d %s" % (len(rows), len(groups), ",".join(missing) if missing else "-"))
' "$OMARCHY_SKILL_GROUPS" 2>/dev/null); crc=$?
      if [ "$crc" = 6 ] || [ -z "$co" ]; then
        row omarchy omarchy.cmd.groups UNKNOWN "cannot parse 'omarchy commands --json --all'"
        row omarchy omarchy.cmd.surface NOTE "probe unparseable; surface counter not read"
      else
        local nrows rest ngroups miss nwant
        nrows=${co%% *}; rest=${co#* }
        ngroups=${rest%% *}; miss=${rest#* }
        nwant=$(printf '%s' "$OMARCHY_SKILL_GROUPS" | wc -w | tr -d ' ')
        if [ "$miss" = "-" ]; then
          row omarchy omarchy.cmd.groups PASS "HELD: all $nwant skill groups present ($ngroups live groups in --json --all)"
        else
          row omarchy omarchy.cmd.groups FAIL "MOVED: skill groups missing from the command surface: $miss"
        fi
        if [ "$nrows" = "$OMARCHY_CMD_SURFACE_PIN" ]; then
          row omarchy omarchy.cmd.surface NOTE "HELD: $nrows commands in --json --all (counter only, not a verdict input)"
        else
          row omarchy omarchy.cmd.surface NOTE "MOVED: $nrows commands in --json --all (pin $OMARCHY_CMD_SURFACE_PIN; counter only, not a verdict input)"
        fi
      fi
    fi

    if ! have omarchy; then
      row omarchy omarchy.theme NOTE "omarchy not on PATH — theme pin not read (operator-owned; D-1: not a verdict input)"
    else
      local th
      th=$(tmo omarchy theme current 2>/dev/null | head -1)
      if [ "$th" = "$OMARCHY_THEME_PIN" ]; then
        row omarchy omarchy.theme NOTE "HELD: '$th' (operator-owned; D-1: never a verdict input)"
      else
        row omarchy omarchy.theme NOTE "MOVED: '${th:-<empty>}' != pin '$OMARCHY_THEME_PIN' (operator-owned; D-1: never a verdict input)"
      fi
    fi
  fi

  # --- docs register (record-level; C5/C8) ---------------------------------
  local hooks="$ROOT/.config/omarchy/hooks" nd
  if [ -d "$hooks" ]; then
    nd=$(find "$hooks" -mindepth 1 -maxdepth 1 -type d -name '*.d' 2>/dev/null | wc -l | tr -d ' ')
    row omarchy omarchy.doc.drifts NOTE "R2 carried: $nd *.d hook dirs live vs flat files in the skill text (MADO-3 §7); R1 route-table drift declared in the note, not re-derived here"
  else
    row omarchy omarchy.doc.drifts NOTE "no $hooks under this root — docs register carried in omarchy-drift-watch.md §4 (R1/R2)"
  fi
}

# ===========================================================================
# plane: theme — declared file chain (theme-wallpaper-plane.md §2/§4/§6)
#
# Landed from the round-7 note's paste-ready §6 row spec — the FILE rows only
# (the note's live rows, swaybg argv and the theme-name display agreement, are
# not landed here). The note is the input and is never parsed: its measured
# anchors are held in line below with the note cited. Every row reads $ROOT,
# so a fixture root carrying the declared files is judged like the real one;
# a missing tree reads UNKNOWN (never a silent pass) and a broken chain FAILs.
# The theme *choice* stays operator-owned (live.theme.current, unchanged) —
# this plane judges chain integrity, never the name's value.
# ===========================================================================
theme_chain_row() { # <id> <consumer-file> <theme part> <declared line>
  local id="$1" file="$2" part="$3" at="$4" hit lno
  if [ ! -f "$file" ]; then
    row theme "$id" FAIL "missing consumer: ${file#$ROOT/}"
    return
  fi
  hit=$(grep -nE "omarchy/current/theme/${part}([\"' 	]|\$)" "$file" 2>/dev/null | head -1)
  if [ -z "$hit" ]; then
    row theme "$id" FAIL "${file#$ROOT/} does not import omarchy/current/theme/$part (chain broken)"
    return
  fi
  lno="${hit%%:*}"
  if [ -n "$at" ] && [ "$lno" != "$at" ]; then
    row theme "$id" FAIL "import moved: line $lno (declared line $at)"
    return
  fi
  if [ ! -f "$C/omarchy/current/theme/$part" ]; then
    row theme "$id" FAIL "import at line $lno but target missing: current/theme/$part"
    return
  fi
  row theme "$id" PASS "line $lno imports current/theme/$part (target exists)"
}

theme_symlink_row() { # <id> <link> <must-resolve-under> <require-nonempty 0|1>
  local id="$1" link="$2" under="$3" need="$4" res
  if [ ! -e "$link" ] && [ ! -L "$link" ]; then
    row theme "$id" FAIL "missing: ${link#$ROOT/}"
  elif [ ! -L "$link" ]; then
    row theme "$id" FAIL "${link#$ROOT/} is a regular file (want a symlink into ${under#$ROOT/})"
  elif ! have readlink; then
    row theme "$id" UNKNOWN "readlink not on PATH — link target unresolved"
  else
    res=$(readlink -f "$link" 2>/dev/null || true)
    case "$res" in
      "$under"/*)
        if [ ! -f "$res" ]; then
          row theme "$id" FAIL "dangling symlink: ${link#$ROOT/} → ${res#$ROOT/}"
        elif [ "$need" = 1 ] && [ ! -s "$res" ]; then
          row theme "$id" FAIL "target is empty: ${res#$ROOT/}"
        else
          row theme "$id" PASS "symlink → ${res#$ROOT/} (inside ${under#$ROOT/})"
        fi
        ;;
      '' | "$link")
        row theme "$id" FAIL "dangling symlink: ${link#$ROOT/} (target does not exist)"
        ;;
      *)
        row theme "$id" FAIL "resolves outside ${under#$ROOT/}: $res"
        ;;
    esac
  fi
}

theme_walker_css_row() { # consumer: walker's theme package imports the css
  local cfg="$C/walker/config.toml" thme loc style
  if [ ! -f "$cfg" ]; then
    row theme theme.chain.walker_css NOTE "walker not installed under this root (no ${cfg#$ROOT/}) — css chain declared only"
    return
  fi
  # the two keys are quoted TOML strings; a trailing comment (# …) is legal
  # and must not defeat the read (measured on the live config.toml:3)
  thme=$(sed -nE 's/^[[:space:]]*theme[[:space:]]*=[[:space:]]*"([^"]*)".*$/\1/p' "$cfg" | head -1)
  loc=$(sed -nE 's/^[[:space:]]*additional_theme_location[[:space:]]*=[[:space:]]*"([^"]*)".*$/\1/p' "$cfg" | head -1)
  if [ -z "$thme" ] || [ -z "$loc" ]; then
    row theme theme.chain.walker_css UNKNOWN "walker config.toml present but theme/additional_theme_location unreadable — chain unverifiable"
    return
  fi
  style="${loc/#\~/$ROOT}/${thme}/style.css"
  if [ ! -f "$style" ]; then
    row theme theme.chain.walker_css NOTE "theme package '$thme' not present under ${loc#$ROOT/} — css chain declared only"
    return
  fi
  if ! grep -q 'omarchy/current/theme/walker.css' "$style"; then
    row theme theme.chain.walker_css FAIL "${style#$ROOT/} does not import omarchy/current/theme/walker.css"
    return
  fi
  if [ ! -f "$C/omarchy/current/theme/walker.css" ]; then
    row theme theme.chain.walker_css FAIL "import present but target missing: current/theme/walker.css"
    return
  fi
  row theme theme.chain.walker_css PASS "package '$thme' style.css imports current/theme/walker.css (target exists)"
}

theme_swayosd_css_row() { # consumer: swayosd style.css imports the css
  local style="$C/swayosd/style.css"
  if [ ! -f "$style" ]; then
    row theme theme.chain.swayosd_css NOTE "swayosd not installed under this root (no ${style#$ROOT/}) — css chain declared only"
    return
  fi
  if ! grep -q 'omarchy/current/theme/swayosd.css' "$style"; then
    row theme theme.chain.swayosd_css FAIL "${style#$ROOT/} does not import omarchy/current/theme/swayosd.css"
    return
  fi
  if [ ! -f "$C/omarchy/current/theme/swayosd.css" ]; then
    row theme theme.chain.swayosd_css FAIL "import present but target missing: current/theme/swayosd.css"
    return
  fi
  row theme theme.chain.swayosd_css PASS "style.css imports current/theme/swayosd.css (target exists)"
}

theme_plane() {
  local tdir="$C/omarchy/current" thdir="$C/omarchy/current/theme"

  # --- the declared machine name (writer: omarchy-theme-set:45; note §1) ----
  local nf="$tdir/theme.name" nm nl
  if [ ! -f "$nf" ]; then
    row theme theme.name.read UNKNOWN "theme tree absent under this root (${nf#$ROOT/}) — name unreadable"
  else
    nm=$(head -1 "$nf" 2>/dev/null)
    nl=$(awk 'END {print NR+0}' "$nf" 2>/dev/null)
    if [ -z "$nm" ] || [ "$nl" != 1 ] || ! printf '%s' "$nm" | grep -qE '^[a-z0-9-]+$'; then
      row theme theme.name.read FAIL "malformed theme.name ('$nm', $nl line(s); want one line matching ^[a-z0-9-]+$)"
    else
      row theme theme.name.read PASS "theme.name = '$nm' (one line, machine-name shape)"
    fi
  fi

  # --- consumer import chain (note §4): file line → theme part -------------
  theme_chain_row theme.chain.hypr_include "$H/hyprland.conf" hyprland.conf 13
  theme_chain_row theme.chain.hyprlock "$H/hyprlock.conf" hyprlock.conf 1
  theme_chain_row theme.chain.waybar_css "$C/waybar/style.css" waybar.css 1
  theme_chain_row theme.chain.alacritty "$C/alacritty/alacritty.toml" alacritty.toml 1

  # --- mako: the consumer config IS the theme part (symlink) ---------------
  theme_symlink_row theme.chain.mako_link "$C/mako/config" "$thdir" 0

  # --- installed-consumer-gated css chains (NOTE when absent, never a
  #     silent skip — note §4/§6) -------------------------------------------
  theme_walker_css_row
  theme_swayosd_css_row

  # --- the wallpaper's declared pointer (note §1/§3) ----------------------
  theme_symlink_row theme.wallpaper.link "$tdir/background" "$thdir/backgrounds" 1

  # --- §4.1 parts whose consumer is absent: declared-only, never FAILs -----
  local pair bin part missing=""
  for pair in foot:foot.ini kitty:kitty.conf ghostty:ghostty.conf \
              helix:helix.toml code:vscode.json asusctl:keyboard.rgb; do
    bin="${pair%%:*}"; part="${pair#*:}"
    if ! have "$bin" && [ -f "$thdir/$part" ]; then missing="$missing $part($bin)"; fi
  done
  row theme theme.parts.declared_only NOTE "declared-only, consumer absent:${missing:- none}"
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