# ScoutShokuknow report (mado r48 w1) — assimilation scan + considerthese open items
Read-only scan; nothing written outside this seat dir. Base 579f694b.

## 1. merge/mado package vs this round's planes (XKB/keymap, terminal cache)
Package: MERGE-REPORT.md:3-9 — 147 staged rows (S203..S349), 69 knowledge files (`merge/mado/knowledge/corpus/knowledge/`, 69 files incl. amendments), staged against a registry of 192 rows (MERGE-REPORT.md:9).
Keyword sweep (xkb|keymap|kb_layout|keyboard layout|fcitx|ibus|mozc|input method|xdg-terminal|terminal-exec|compose) across the whole package:
- **No staged entry on XKB, keymap compile, RMLVO, kb_*; none on xdg-terminal-exec or its cache.** Theme = IPC/event sockets, idle-lock, focus grab, gkeep geometry, zh/ja wiki coverage (MERGE-REPORT.md:17-87). => nothing for C1 or C2 to admit.
- Near-misses (matched keyword only, none is the plane):
  - `japanese-input-observation-methods-r14.md` (cites staged S333, S334): Japanese article naming wev/evtest + Wayland per-client input isolation. Keyboard *event observation*, not XKB compile. Lane already holds `input-debugging-boundaries-r15.md` (S051/S052, libinput tools) and r46 `hyprland-input-devices-r46.md`. Disposition: **refuse for r48 planes** (out of C2 scope; not an XKB claim); a separate Japanese-tier admit question, not this round's.
  - `focus-grab-keyboard-routing-r13.md` (S317, SeatManager::sendKeyboardKey): keyboard focus routing, not keymaps. Refuse for r48 (held ground: round-43/44 focus-grab theme).
  - S247 (omarchy-voxtype-status, SOURCES.append.md:51, "input-method status" = voice typing chip, not an IME). Not XKB. Refuse for r48.
  - S343 fcitx5-wetypex Hyprland doc (SOURCES.append.md:147, window rules/sizes): gkeep/size theme; fcitx5 appears as app name only. Not keymap.
- Staleness / collision hazard (affects any future admit, relevant to C2's new rows): the package ids S203..S349 are numbered against a 192-row registry; lane registry now tops at S339 (corpus/SOURCES.md:288), and lane S333/S334 are already Hyprland rows (SOURCES.md:282-283) while the staged Japanese entry cites S333/S334 for different pages. C2's new rows S340.. are therefore safe from the registry but a later package merge would collide with staged S340-S349 (e.g. S343 above). The package would need renumbering; round 44 already assimilated the gkeep-size theme (corpus/lessons/round-44.md:57 "Assimilation ledger").
- Verdict: **no admit-candidate for C1/C2; refuse-by-scope for all four near-misses.** C2 must be sourced from primary (libxkbcommon/xkeyboard-config) fetches + the live xkbcli receipt, not from the package.
- PROVINCE.md held ground for C2: r46 refinement (PROVINCE.md:102-114) owns kb_* config keys read-only; `hyprland-input-devices-r46.md:69` is the stated open ground the new entry fills; PROVINCE.md :1-16 'never mutates a running compositor' bounds the xkbcli read.

## 2. considerthese/2026-10-26.md proposals (newest file; 6 proposals, lines 47-52)
| # | proposal | status at 579f694b | evidence |
|---|---|---|---|
| 1 | privacy check on new receipts | **implemented** (r45) | quality/check-session-material.py (rules R1-R4); corpus/lessons/round-45.md:81 -> QUALITY 85. Not open. |
| 2 | ledger of live-state tools | **refused r47** | corpus/lessons/round-47.md:227 (flip: ledger whose rows the check re-derives, 0 wrong). Open-by-refusal. |
| 3 | track routed defects until closed | **landed** r46 as QUALITY 90 | round-46.md:365-367; QUALITY.md:459. |
| 4 | re-run one tool myself read-only | **unimplementable in-lane** | reflection-agent behaviour needing operator OK + machine connection (proposal text itself); no lane artifact exists. Open, not a build target. |
| 5 | report domain-to-meta ratio daily | **implemented as tool** (r44) | quality/ratio-domain-meta.py (docstring provenance cites the 2026-10-25 proposal 1, same idea); QUALITY.md:411 criterion 82; round-44.md:251-254. Residual: the daily number is the reflection's job; the lane only provides the re-runnable count. Treat as done. |
| 6 | lead with round-level outcomes, not counter internals | **unimplementable in-lane** | style of the reflection author; no lane artifact; no check applicable. Open, not buildable. |
Genuinely unimplemented lane-buildable items: **only #2** (refused r47 with a stated flip). #1,#3,#5 done; #4,#6 are reflection-author behaviours.
Latest-dated file is 2026-10-26.md (`ls considerthese/`: 10-22..10-26); nothing newer.
