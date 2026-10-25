# RevAssimilUsedBy — S201/S202 used-by audit

Scope: rows appended to `corpus/SOURCES.md` at `fa7ba11346116672352b5d41494141c5c4d738d0`
("round-34: admit the waybar event-socket entry after the frozen counter").
Checked: column count, used-by cell verbatim, knowledge-file citations of each id, set equality.

## S201 (Waybar 0.15.0 Hyprland IPC backend)

- **Columns:** 11 (matches header: id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by).
- **used-by cell verbatim:** `corpus/knowledge/waybar-module-text-route-r25.md`
- **Knowledge files citing `S201` (`grep -rnE 'S201' corpus/knowledge/`):**
  - `corpus/knowledge/waybar-module-text-route-r25.md` — 3 matches (lines 7, 12, 18)
- **used-by == citing set?** Yes — exactly one file, exactly the one listed.
- **Discrepancies:** none. No extra, missing, malformed, or whole-token-partial tokens.

## S202 (Waybar 0.15.0 Hyprland window module)

- **Columns:** 11 (matches header).
- **used-by cell verbatim:** `corpus/knowledge/waybar-module-text-route-r25.md`
- **Knowledge files citing `S202` (`grep -rnE 'S202' corpus/knowledge/`):**
  - `corpus/knowledge/waybar-module-text-route-r25.md` — 3 matches (lines 8, 13, 21)
- **used-by == citing set?** Yes — exactly one file, exactly the one listed.
- **Discrepancies:** none. No extra, missing, malformed, or whole-token-partial tokens.

## Verdict

Both rows are well-formed. Each used-by cell contains exactly one token
(`corpus/knowledge/waybar-module-text-route-r25.md`), and the set of knowledge files citing
each id equals that set. No anomalies found.
