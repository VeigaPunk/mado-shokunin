# RevQuoteS206 — scratch findings (raw)

Worktree: /home/vgpnk/Projects/shokunin/mado-shokunin (lane, read-only)
Scratch log with exit codes: .ufo/waves/round-35/scratch/RevQuoteS206/verify.log

## Axes
- A1 anchor integrity: receipt sha256 == SOURCES.md S206 anchor cell
- A2 receipt fidelity: receipt's recorded file sha256/size and quoted lines == live host bytes
- A3 quote legality: entry gate-quote is a contiguous, unique substring of receipt bytes
- A4 statement truth: the two facts the gate-quote asserts hold on the live host now
- A5 liveliness (beyond the seat): the on-click target is a present, wired command

## Raw values
live  /home/vgpnk/.config/waybar/config.jsonc
  sha256 a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829
  wc -c 6354   wc -l 260   mtime 2026-10-17T17:02:56-03:00
receipt .ufo/waves/round-35/fetch/S206.receipt.txt
  sha256 1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5
  wc -c 929
SOURCES.md row S206 cell 7: 6354 B, file sha256 a408a33d...aae829, receipt sha256 1d30e4a9...a938d5
=> A1, A2 pass, byte for byte, no tolerance needed.

gate-quote contiguity: quote of 111 bytes found at byte offset 817, count=1, file has no CRLF,
quote terminates the file (quote + single LF). The entry's rendered line additionally prefixes
"S206 " (seat label); that prefix is absent from receipt bytes and byte offset is -1 for the
prefixed form. Same convention on all six seats S205-S210 (each receipt line starts "located: ",
each entry line starts "gate-quote: S20x "). Convention, not divergence.

live lines 207-212 (verbatim, cat -n):
   207	  "custom/idle-indicator": {
   208	    "on-click": "omarchy-toggle-idle",
   209	    "exec": "$OMARCHY_PATH/default/waybar/indicators/idle.sh",
   210	    "signal": 9,
   211	    "return-type": "json"
   212	  },
line 18 sits inside "modules-center" (header at line 11), not modules-left:
    11	  "modules-center": [
    12	    "clock",
    ...
    18	    "custom/idle-indicator",
    19	    "custom/notification-silencing-indicator"
    20	  ],
    21	  "modules-right": [

receipt numbered-segment diff vs live: 14 numbered lines (range 18..213), 0 content
mismatches. (Naive parser flagged line 24 only because the excerpt's closing "---" marker
is unnumbered; line 24 text equals live line 24 exactly.)

on-click counts: block 207-212 => 1; file-wide => 15. Receipt's "--- on-click handler count
--- 1" is block-scoped; readable as file-wide it would understate by 14.

liveliness: /home/vgpnk/.local/share/omarchy/bin/omarchy-toggle-idle exists, -rwxr-xr-x, 316 B,
resolves on PATH; its line 13 is `pkill -RTMIN+9 waybar`, matching config line 210 `"signal": 9`.
Running bar: pgrep -a waybar -> "935660 /usr/bin/waybar", started Sun Oct 25 02:06:20 2026,
no -c override; only config.jsonc is live in ~/.config/waybar (rest are .bak copies) so the
running bar loads the hashed file.

No installs performed (pacman paused; nothing needed).
