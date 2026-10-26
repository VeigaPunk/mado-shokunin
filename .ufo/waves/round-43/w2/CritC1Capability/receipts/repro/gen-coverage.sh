#!/bin/bash
set -u
S=/fast/scratch/hyaku/mado-r43/CritC1Capability
W=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w2/CritC1Capability
cd "$S" || exit 1
OUT="$W/receipts/coverage.txt"
{
  echo "# host rule set vs the tool, at data commit 1959770657f1f8665097c1aed4be6c1cbb07139f (host read-only, 2026-10-26)"
  echo
  echo '## 1. source closure of ~/.config/hypr/hyprland.conf (transitive, globs expanded)'
  python3 srcwalk.py > sources.txt 2> sources.count
  cat sources.count
  echo "\$ wc -l sources.txt"; wc -l < sources.txt
  echo
  echo '## 2. windowrule lines in the closure, by effect'
  python3 classify.py | tee classify.out | tail -5
  echo
  echo '## 3. the tool over every closure file as --rules, and over hyprland.conf alone'
  hyprctl clients -j > clients.json
  echo "\$ hyprctl clients -j > clients.json   # $(wc -c < clients.json) bytes, $(python3 -c 'import json;print(len(json.load(open("clients.json"))))') clients"
  args=(); while read -r f; do args+=(--rules "$f"); done < sources.txt
  echo "\$ python3 mado-geometry.py --clients clients.json --rules <40 closure files>"
  python3 mado-geometry.py --clients clients.json "${args[@]}"; echo "exit=$?"
  echo
  echo "\$ python3 mado-geometry.py --clients clients.json --rules ~/.config/hypr/hyprland.conf"
  python3 mado-geometry.py --clients clients.json --rules /home/vgpnk/.config/hypr/hyprland.conf; echo "exit=$?"
  echo
  echo '## 4. every size/float line in the closure, classified independently of the tool'
  awk '/^SIZE|^FLOAT/ {print}' classify.out
  echo
  echo '## 5. independent counts (python classify.py summary)'
  python3 classify.py --summary
} > "$OUT" 2>&1
cat "$OUT"
