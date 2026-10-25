#!/bin/bash
# RevQuoteS210 — read-only re-derivation of row S210 (wave 2, round 35).
# Run from anywhere. Writes nothing outside this scratch directory.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
DIR=/home/vgpnk/.local/state/omarchy/toggles/hypr
REC=$LANE/.ufo/waves/round-35/fetch/S210.receipt.txt
ENTRY=$LANE/corpus/knowledge/idle-lock-offered-in-the-bar-r15.md
ROW=$LANE/corpus/SOURCES.md

echo "## live directory: $DIR"
ls -la "$DIR"; echo "ls-rc=$?"
echo "--- regular files (includes dotfiles) ---"
find "$DIR" -maxdepth 1 -type f | sort; echo "find-rc=$?"
echo "--- entry count, hidden included ---"
ls -A "$DIR" | wc -l
echo "--- files whose text names the idle lock (case-insensitive) ---"
grep -ril idle "$DIR"; echo "grep-rc=$? (1 = no match)"
grep -ril idle "$DIR" 2>/dev/null | wc -l
echo "--- per-file keyword counts ---"
for f in "$DIR"/*.conf; do
  printf '%s idle=%s lock=%s hypridle=%s size=%s mtime=%s\n' \
    "$(basename "$f")" "$(grep -ci idle "$f")" "$(grep -ci lock "$f")" \
    "$(grep -ci hypridle "$f")" "$(stat -c %s "$f")" "$(stat -c %y "$f")"
done
echo "--- directory mtime vs window-no-gaps.conf mtime (entry-set stability) ---"
stat -c '%n %y' "$DIR" "$DIR/window-no-gaps.conf"

echo
echo "## receipt bytes and gate-quote contiguity"
python3 -I - "$REC" "$ENTRY" <<'PY'
import sys
rec_path, entry_path = sys.argv[1], sys.argv[2]
rec = open(rec_path, 'rb').read()
quote = b"located: the toggles/hypr directory holds 2 files and 0 of them name the idle lock"
print("receipt bytes:", len(rec))
print("quote bytes:", len(quote))
i = rec.find(quote)
print("first index:", i, "occurrences:", rec.count(quote))
print("contiguous_substring:", i != -1)
print("after-quote bytes:", None if i == -1 else repr(rec[i+len(quote):]))
line = [l for l in open(entry_path, 'rb').read().split(b'\n') if b'gate-quote: S210' in l][0]
prefix = b'gate-quote: S210 '
assert line.startswith(prefix), line
entry_quote = line[len(prefix):]
print("entry_quote_equal_to_receipt_substring:", entry_quote in rec)
print("entry_quote_words:", len(entry_quote.split()))
print("gate_quote_lines_for_S210:", sum(1 for l in open(entry_path, 'rb').read().split(b'\n') if b'gate-quote: S210' in l))
PY
echo "py-rc=$?"

echo
echo "## receipt sha256 vs row anchor"
sha256sum "$REC"; echo "sha-rc=$?"
stat -c '%n type=%F size=%s mtime=%y' "$REC"
grep -c "ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726" "$ROW"
python3 -I - "$ROW" <<'PY'
import sys
rows = [l for l in open(sys.argv[1], encoding='utf-8').read().split('\n') if l.startswith('| S210 ')]
print("S210 row count:", len(rows))
cells = [c.strip() for c in rows[0].strip().strip('|').split('|')]
print("cells:", len(cells))
print("status:", repr(cells[7]), "opened:", repr(cells[8]), "recheck:", repr(cells[9]))
print("used-by tokens:", cells[10].split(','))
print("escaped pipe in row:", '\\|' in rows[0])
print("sha in anchor cell (6):", 'ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726' in cells[5])
PY
echo "py-rc=$?"

echo
echo "## provenance discriminator: score runs on the state dir, not the default dir"
find /home/vgpnk/.local/share/omarchy/default/hypr/toggles -maxdepth 1 -type f | wc -l

echo
echo "## who writes the toggle store / does the idle toggle persist anything"
grep -n "toggles/hypr" /home/vgpnk/.config/hypr/hyprland.conf
sed -n '16,20p' /home/vgpnk/.local/share/omarchy/bin/omarchy-hyprland-toggle
sed -n '17,19p' /home/vgpnk/.local/share/omarchy/bin/omarchy-toggle
sed -n '1,14p' /home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle
echo "--- idle-named state anywhere under omarchy state (depth<=2) ---"
timeout 20 find /home/vgpnk/.local/state/omarchy -maxdepth 2 -iname '*idle*'; echo "find-rc=$?"
