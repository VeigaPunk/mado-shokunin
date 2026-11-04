#!/bin/sh
# R81ConnSiblings — second sweep: instrument-directory census and fleet-wide attribution counts.
set -u
F=/home/vgpnk/Projects/shokunin
S=$F/mado-shokunin/.ufo/waves/round-81/w1/R81ConnSiblings
cd "$F" || exit 1

# ---- L1: which lane keeps tools/, scripts/, verifiers/ (the seat names "each sibling's tools/") ----
{
  printf '$ for d in *-shokunin; do printf "%%-24s" "$d"; for k in tools scripts verifiers plans; do if test -d "$d/$k"; then printf " %%s=%%s" "$k" "$(ls -1 "$d/$k" 2>/dev/null | wc -l)"; else printf " %%s=-" "$k"; fi; done; echo; done\n'
  for d in *-shokunin; do
    printf '%-24s' "$d"
    for k in tools scripts verifiers plans; do
      if test -d "$d/$k"; then printf ' %s=%s' "$k" "$(ls -1 "$d/$k" 2>/dev/null | wc -l)"; else printf ' %s=-' "$k"; fi
    done
    echo
  done
} > "$S/sweep-l1-instrument-dirs.txt" 2>&1

# ---- L2: the four families restricted to each sibling's tools/ (and scripts/, verifiers/) ----
{
  printf '$ grep -rniE "<four families>" */tools */scripts */verifiers | grep -v ^mado-shokunin/\n'
  grep -rniE 'layer[-_]?shell|exclusive[ _-]?zone|reserved[ _-]?band|arrangeLayerArray|zwlr_layer|gtk-layer|omarchy-menu-keybindings|cut -c36-|pgrep +-x' \
    */tools */scripts */verifiers 2>/dev/null | grep -v '^mado-shokunin/'
  printf 'rc=%s (1 = no hits)\n' "$?"
} > "$S/sweep-l2-instrument-families.txt" 2>&1

# ---- L3: the stray lane-name directory ----
{
  printf '$ ls -la kumitate-shokinin/ ; find kumitate-shokinin -maxdepth 3\n'
  ls -la kumitate-shokinin/
  find kumitate-shokinin -maxdepth 3
  printf '\n$ ls -d *kumitate*\n'
  ls -d *kumitate*
} > "$S/sweep-l3-stray-lane-name.txt" 2>&1

# ---- L4: fleet-wide attribution counts for the C2 token family, outside mado ----
{
  printf '$ grep -rn "omarchy-menu-keybindings" --include=*.md --include=*.py --include=*.sh --include=*.json . | grep -v ^./mado-shokunin/ | cut -d: -f1 | sort | uniq -c\n'
  grep -rn 'omarchy-menu-keybindings' --include=*.md --include=*.py --include=*.sh --include=*.json . 2>/dev/null \
    | grep -v '^\./mado-shokunin/' | cut -d: -f1 | sort | uniq -c
  printf '\n$ grep -rn "omarchy menu keybindings\|cut -c36-" --include=* . | grep -v ^./mado-shokunin/\n'
  grep -rn 'omarchy menu keybindings\|cut -c36-' --include=* . 2>/dev/null | grep -v '^\./mado-shokunin/'
  printf 'rc=%s (1 = no hits)\n' "$?"
} > "$S/sweep-l4-c2-attribution.txt" 2>&1

# ---- L5: fleet-wide counts for the C1 API family, outside mado ----
{
  printf '$ grep -rlE "applyExclusive|arrangeLayerArray|arrangeLayersForMonitor|CReservedArea|addreserved" --include=* . | grep -v ^./mado-shokunin/\n'
  grep -rlE 'applyExclusive|arrangeLayerArray|arrangeLayersForMonitor|CReservedArea|addreserved' --include=* . 2>/dev/null \
    | grep -v '^\./mado-shokunin/'
  printf 'rc=%s (1 = no hits)\n' "$?"
  printf '\n$ grep -rl "gtk-layer-shell\|LayerShell.cpp" --include=* . | grep -v ^./mado-shokunin/\n'
  grep -rl 'gtk-layer-shell\|LayerShell\.cpp' --include=* . 2>/dev/null | grep -v '^\./mado-shokunin/'
  printf 'rc=%s\n' "$?"
} > "$S/sweep-l5-c1-attribution.txt" 2>&1

printf 'second sweep written\n'
