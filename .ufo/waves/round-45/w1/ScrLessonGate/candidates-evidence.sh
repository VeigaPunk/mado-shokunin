#!/bin/sh
# ScrLessonGate: evidence for the rejected Gate candidates. Read-only network GETs
# and lane reads only; nothing is written outside this seat dir.
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
F=$LANE/.ufo/waves/round-45/fetch
T=$(mktemp -d -p /fast/scratch/hyaku/mado-r45/ScrLessonGate)

echo "== A. wiki at main vs the pin"
echo '$ curl -sS -o r1 -w "http=%{http_code} bytes=%{size_download}" https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605e453c0ad533d979fccbefff788ef/content/Configuring/Monitors.md'
curl -sS -o "$T/r1" -w "http=%{http_code} bytes=%{size_download}\n" https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605e453c0ad533d979fccbefff788ef/content/Configuring/Monitors.md
echo '$ sha256sum r1'
sha256sum "$T/r1" | cut -c1-64
echo '$ local pin .ufo/waves/round-45/fetch/wiki-Monitors.md'
sha256sum "$F/wiki-Monitors.md" | cut -c1-64
echo '$ curl -sS -o r2 -w "http=%{http_code} bytes=%{size_download}" https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/Monitors.md'
curl -sS -o "$T/r2" -w "http=%{http_code} bytes=%{size_download}\n" https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/Configuring/Monitors.md
echo '$ cat r2'
cat "$T/r2"; echo

echo "== B. the parser's number test is hyprutils, reached through isNumber"
echo '$ grep -n "isNumber" fetch/Hyprland-Parser.cpp'
grep -n "isNumber" "$F/Hyprland-Parser.cpp"
echo '$ sed -n 46,47p fetch/hyprutils-String.cpp'
sed -n 46,47p "$F/hyprutils-String.cpp"

echo "== C. host version pin for S309 (hyprctl version, read-only)"
echo '$ hyprctl version | grep -E "^(Hyprland|Hyprutils|Hyprlang)"'
hyprctl version | grep -E "^(Hyprland|Hyprutils|Hyprlang)"

echo "== D. held rows S158/S162 cannot carry the monitor lines"
echo '$ (coverage from verify_gate.py, counter range semantics)'
python3 -I "$LANE/.ufo/waves/round-45/w1/ScrLessonGate/verify_gate.py" | grep -E "S158 anchor covers|S162 anchor covers"

rm -rf -- "$T"
