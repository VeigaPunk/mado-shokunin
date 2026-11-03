#!/usr/bin/env bash
# seat R65RevRegister — A1: independent re-derivation of the 8-group surface register (2026-10-31 family)
# READ-ONLY probes only. No env dumps, no service starts, no config writes.
set -u
OUT="$1"
: > "$OUT"
say(){ printf '%s\n' "$*" | tee -a "$OUT"; }

say "== A1 independent register probes — seat R65RevRegister — $(date -u +%Y-%m-%dT%H:%M:%SZ) — host $(hostname) =="

say "-- G1 hypr plane (~/.config/hypr, hyprctl) --"
o=$(command -v hyprctl); rc=$?; say "G1 command -v hyprctl rc=$rc -> ${o:-<none>}"
if [ -d "$HOME/.config/hypr" ]; then say "G1 ~/.config/hypr=present"; else say "G1 ~/.config/hypr=missing"; fi
o=$(hyprctl version 2>&1); rc=$?; say "G1 hyprctl version rc=$rc"; printf '%s\n' "$o" | sed -n '1,2p' | tee -a "$OUT"

say "-- G2 waybar (~/.config/waybar, process) --"
o=$(command -v waybar); rc=$?; say "G2 command -v waybar rc=$rc -> ${o:-<none>}"
if [ -d "$HOME/.config/waybar" ]; then say "G2 ~/.config/waybar=present"; else say "G2 ~/.config/waybar=missing"; fi
pgrep -x waybar >/dev/null 2>&1; say "G2 waybar process pgrep rc=$? (0=running)"

say "-- G3 walker (~/.config/walker) --"
o=$(command -v walker); rc=$?; say "G3 command -v walker rc=$rc -> ${o:-<none>}"
if [ -d "$HOME/.config/walker" ]; then say "G3 ~/.config/walker=present"; else say "G3 ~/.config/walker=missing"; fi

say "-- G4 terminal configs (alacritty/foot/kitty/ghostty) --"
for t in alacritty foot kitty ghostty; do
  if [ -e "$HOME/.config/$t" ]; then say "G4 ~/.config/$t=present"; else say "G4 ~/.config/$t=missing"; fi
done

say "-- G5 theme/wallpaper omarchy plane --"
if [ -e "$HOME/.config/omarchy" ]; then say "G5 ~/.config/omarchy=present"; else say "G5 ~/.config/omarchy=missing"; fi
if [ -e "$HOME/.local/share/omarchy" ]; then say "G5 ~/.local/share/omarchy=present"; else say "G5 ~/.local/share/omarchy=missing"; fi
o=$(command -v omarchy); rc=$?; say "G5 command -v omarchy rc=$rc -> ${o:-<none>}"

say "-- G6 idle/lock plane (hypridle/hyprlock/hyprsunset) --"
for b in hypridle hyprlock hyprsunset; do
  o=$(command -v "$b"); rc=$?; say "G6 command -v $b rc=$rc -> ${o:-<none>}"
done

say "-- G7 omarchy skill docs (~/.agents/skills/omarchy/) --"
if [ -d "$HOME/.agents/skills/omarchy" ]; then
  n=$(find "$HOME/.agents/skills/omarchy" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l)
  say "G7 ~/.agents/skills/omarchy=present md-files=$n"
else
  say "G7 ~/.agents/skills/omarchy=missing"
fi

say "-- G8 windows desktop plane (WM state, DPI, DWM) --"
for b in powershell pwsh powershell.exe; do
  o=$(command -v "$b"); rc=$?; say "G8 command -v $b rc=$rc -> ${o:-<none>}"
done
if [ -f tools/mado-win-desk.py ]; then
  o=$(python3 tools/mado-win-desk.py 2>&1); rc=$?
  say "G8 python3 tools/mado-win-desk.py rc=$rc"
  printf '%s\n' "$o" | sed -n '1,3p' | tee -a "$OUT"
else
  say "G8 tools/mado-win-desk.py absent in cwd"
fi

say "-- extras cross-check (receipt lines beyond the 8 groups) --"
for b in mako swayosd grim slurp; do
  o=$(command -v "$b"); rc=$?; say "X command -v $b rc=$rc -> ${o:-<none>}"
done

say "-- package versions (pacman -Q, read-only local db) --"
o=$(pacman -Q hyprland waybar walker hypridle hyprlock hyprsunset 2>&1); rc=$?
say "pacman -Q rc=$rc"; printf '%s\n' "$o" | tee -a "$OUT"
say "== A1 end =="
