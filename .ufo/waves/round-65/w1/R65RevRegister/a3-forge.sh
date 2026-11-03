#!/usr/bin/env bash
# seat R65RevRegister — A3: cheapest forged input that passes c1-r65-register.py.
# Fixture git repo lives ONLY in scratch; toplevel asserted before every mutation.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
SEAT=$LANE/.ufo/waves/round-65/w1/R65RevRegister
COUNTER=$LANE/.ufo/waves/round-65/w1/R65ExecC1Counter/c1-r65-register.py
HEADREV=cb63ab13ccaf85191318701d5db5ace050bd5bd4
BASE=524fa1f90b1f2de44b3019bacf833d54e0af13a0
S=/fast/scratch/hyaku/mado-r65/w1/R65RevRegister/forge-a3
OUT=$SEAT/a3-forge-r65.txt
: > "$OUT"
say(){ printf '%s\n' "$*" | tee -a "$OUT"; }

say "== A3 forged-input demonstration — seat R65RevRegister — $(date -u +%Y-%m-%dT%H:%M:%SZ) =="
say "== counter bytes sha256: $(sha256sum "$COUNTER" | cut -c1-16) =="

# --- lane control re-runs (read-only, no mutation) ---
say "-- lane control re-run at base (expect TARGET_MISSED rc=1) --"
python3 -I "$COUNTER" --repo "$LANE" --rev "$BASE" >> "$OUT" 2>&1; say "LANE_BASE_RC=$?"
say "-- lane control re-run at HEAD cb63ab13 (expect TARGET_MISSED rc=1) --"
python3 -I "$COUNTER" --repo "$LANE" --rev "$HEADREV" >> "$OUT" 2>&1; say "LANE_HEAD_RC=$?"

# --- fixture 1: base PROVINCE.md + forged block with FALSE state cells ---
rm -rf "$S"; mkdir -p "$S"
git -C "$LANE" show "$BASE":PROVINCE.md > "$S/PROVINCE.md" || { say "FATAL: base PROVINCE.md unreadable"; exit 8; }
cat >> "$S/PROVINCE.md" <<'EOF'

### Surface state register (2026-11-03, forged A3 fixture — every state cell below is FALSE)

| surface group | state (observed 2026-11-03) | probe (read-only) | receipt |
| --- | --- | --- | --- |
| hypr plane | absent (2026-11-03) | `command -v hyprctl` → not found | `.ufo/waves/round-65/receipts/gate-fileplane-r65.txt` |
| waybar | absent (2026-11-03) | `command -v waybar` → not found | `.ufo/waves/round-65/receipts/gate-fileplane-r65.txt` |
| walker | absent (2026-11-03) | `command -v walker` → not found | `.ufo/waves/round-65/receipts/gate-fileplane-r65.txt` |
| terminal configs | absent (2026-11-03) | `test -e ~/.config/{alacritty,foot,kitty,ghostty}` → all missing | `.ufo/waves/round-65/receipts/gate-fileplane-r65.txt` |
| theme/wallpaper omarchy plane | absent (2026-11-03) | `test -e ~/.config/omarchy` → missing | `.ufo/waves/round-65/receipts/gate-fileplane-r65.txt` |
| idle/lock plane | absent (2026-11-03) | `command -v hypridle hyprlock hyprsunset` → not found (3/3) | `.ufo/waves/round-65/receipts/gate-fileplane-r65.txt` |
| omarchy skill docs | absent (2026-11-03) | `test -d ~/.agents/skills/omarchy` → missing | `.ufo/waves/round-65/receipts/gate-fileplane-r65.txt` |
| windows desktop plane | absent (2026-11-03) | `python tools/mado-win-desk.py` → rc=2 | `.ufo/waves/round-65/receipts/gate-fileplane-r65.txt` |

<!-- r65 register end -->
EOF
mkdir -p "$S/.ufo/waves/round-65/receipts"
git -C "$LANE" show "$HEADREV:.ufo/waves/round-65/receipts/gate-fileplane-r65.txt" > "$S/.ufo/waves/round-65/receipts/gate-fileplane-r65.txt" || { say "FATAL: receipt not committed at HEAD"; exit 8; }

cd "$S" || exit 8
git init -q .
TOP=$(git rev-parse --show-toplevel)
[ "$TOP" = "$S" ] || { say "FATAL: toplevel $TOP != fixture $S"; exit 9; }
git add PROVINCE.md .ufo
git -c user.name=a3forge -c user.email=a3forge@fixture commit -qm "A3 forged register fixture (all state cells false)"
FORGEREV=$(git rev-parse HEAD)
say "-- forged fixture rev: $FORGEREV --"
say "-- forged fixture tree receipt present: $(git ls-tree -r --name-only HEAD | grep -c gate-fileplane) --"
say "-- run counter on FORGED fixture (design question: does it accept?) --"
python3 -I "$COUNTER" --repo "$S" --rev HEAD >> "$OUT" 2>&1
say "FORGED_RC=$? (0 = counter ACCEPTS forged state cells)"

# --- fixture 2: negative control, base PROVINCE.md only (no block) ---
S2=/fast/scratch/hyaku/mado-r65/w1/R65RevRegister/forge-base
rm -rf "$S2"; mkdir -p "$S2"
git -C "$LANE" show "$BASE":PROVINCE.md > "$S2/PROVINCE.md"
cd "$S2" || exit 8
git init -q .
TOP2=$(git rev-parse --show-toplevel)
[ "$TOP2" = "$S2" ] || { say "FATAL: toplevel $TOP2 != fixture $S2"; exit 9; }
git add PROVINCE.md
git -c user.name=a3forge -c user.email=a3forge@fixture commit -qm "A3 base-only negative control"
say "-- run counter on BASE-ONLY fixture (expect TARGET_MISSED rc=1) --"
python3 -I "$COUNTER" --repo "$S2" --rev HEAD >> "$OUT" 2>&1
say "BASEONLY_RC=$?"

say "== A3 end =="
