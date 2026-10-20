# PtrWaybarWalkerSemantics — R18-V3 freshness pointer appended to waybar-walker-semantics.md (append-only, verified)

## Scope
Target: /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/waybar-walker-semantics.md (sole writer this wave). Only edit: one appended block at file tail. No other file in the lane was written. No fetch performed (no web source opened). No git/jj command run. Host paused: no pacman, systemctl, walker, waybar or live-gate command run; host files read as bytes only (none needed beyond the note itself).

## Line list (grep -n '2\.17\.0' on the note, before the edit)
- `23:| walker | `walker --version` → `2.17.0`; pkg `2.17.0-1` | ...` — the only line containing `2.17.0`.
- Note measurement date: line 4 ("Measured 2026-10-14 on host plazir27").
- Line 387 (`3.8.3`) and line 190 (procps) are not walker version claims; not in the list.

## Byte evidence
- Before: sha256 `b92bee2cc69c95b921da8172b2bf15bca7248c40ef72f7b4acb12d9ab179e263`, 38083 bytes; last byte `.` (no trailing newline).
- After: sha256 `8412646f40b660f161ec1080e03c467d186b5573b947261bae79ef4179f860d6`, 39539 bytes.
- Prefix check: `head -c 38083` of the new file → sha256 `b92bee2cc69c95b921da8172b2bf15bca7248c40ef72f7b4acb12d9ab179e263`, identical to the pre-edit hash. Old bytes unchanged; the appended block begins with one newline after the old final `.`.
- Appended block: lines 464–472 (blank, heading at 465, five bullets at 467–471 and 472). Bullet 467 contains both `2.17.2` and `S090`. Block is 9 lines (<20).

## Findings
1. The version pin is dated: line 23 describes walker 2.17.0 measured 2026-10-14; host moved to 2.17.2 per `/var/log/pacman.log:2929` (S090 row).
2. Version-bound families (dated, not re-checked against 2.17.2): packaged default `/etc/xdg/walker/config.toml` line count and values (§6.1, §6.2); `strings /usr/bin/walker` claims (§6.2, §6.3, §6.4); walker socket/protocol ledger (§6.8, §9 item 7).
3. Elephant pin (line 24) is also version-bound; S090 row records elephant 2.21.0-1 → 2.22.1-1 at `/var/log/pacman.log:3095`.
4. Host-file bytes (`~/.config/walker/config.toml`, sha256 `fecf71fa…` in §10) are dated 2026-10-14 and not re-hashed this round; the meaning of its keys is version-bound.
5. Version-independent of the walker package [INFERENCE]: omarchy-owned theme, launch/restart scripts, keybinds, omarchy-menu path (§6.6, §6.7). Not re-measured this round.
6. Behaviour of the 2.17.2 binary: [UNK].

## Deviations from the brief
- The brief's template named `S096` (host walker bytes) in the first bullet. S096 is reserved but has no row in corpus/SOURCES.md yet (grep of `^| S09[5-7]` shows only S095), so the block cites only S090 and does not claim a file-bytes read of the 2.17.2 binary. L1 may add S096 once the row exists.
- Only one line contains the literal `2.17.0`; the other version-bound statements (config line counts, binary-string claims) are covered by family bullets, not by line list.

## Limits
- No live check of walker 2.17.2 behaviour or of its binary bytes (host pause). Did not open /usr/bin/walker, /etc/xdg/walker/config.toml, or ~/.config/walker/config.toml this round.
- Did not read walker-route-r18.md content; pointer is cited as the routing target only.
- Did not verify SOURCES.md S090 row beyond the grep line shown.

## Installs
none
