# R87Connector — mako sibling-overlap sweep (read-only)

Seat: R87Connector (connector, leaf). Scope: fleet artifacts that claim the mako configuration plane or the omarchy mako defaults, and overlap with the C1 surface (effective-settings resolver over `~/.config/mako/config`, its `include=` chain, and criteria sections). Read-only. Files written: this report only. No scratch created. No installs.

## 1. Sweep commands and output

S1 — lane PROVINCE / SKILL / corpus lessons+knowledge, all `*-shokunin`, mado excluded:
`_grep pattern=(?i)\bmako\b|makoctl|notification-daemon|notifications / OSD path=/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md;…/SKILL.md;…/corpus/lessons;…/corpus/knowledge;!**/mado-shokunin/**`
→ `No matches found`.

S2 — same token set over other lanes' `tools`, `quality`, `scripts`, `templates`, mado excluded:
`_grep pattern=makoctl|\.config/mako|mako\.ini|default/mako|\bmako\b path=/home/vgpnk/Projects/shokunin/*-shokunin/{tools,quality,scripts,templates};!**/mado-shokunin/**`
→ `No matches found`.

S3 — omarchy surfaces: `_grep pattern=(?i)\bmako\b|makoctl path=/home/vgpnk/.agents/skills/omarchy/SKILL.md` → lines 6, 26, 82 (below). `_glob` of `~/.local/share/omarchy/default/mako` → `core.ini`; of `~/.config/mako` → `config`. `_read` of both (below).

S4 — mado scope, PROVINCE alone: `_grep pattern=(?i)\bmako\b|makoctl|notifications / OSD path=mado-shokunin/PROVINCE.md` → lines 18, 131 only.

S5 — mado scope, tools + counters: `_grep pattern=makoctl|\.config/mako|mako\.ini|default/mako|\bmako\b path=mado-shokunin/tools;mado-shokunin/quality/counters` → tools/mado-tripwire.py:270; tools/mado-verify.sh:86-88, 342-353, 1146-1153, 4109-4110.

Superseded noise: an earlier loose run (`mako` as substring, case-insensitive) matched only person-name false positives in `kotodama-shokunin` (`corpus/knowledge/civilizations/japan-heian.md:18` "Makoto"; `corpus/knowledge/zimbabwe-shona.md:32`, `:170` "Makondo"). That run was truncated (402 of 587 lines); S1/S2 with the word-bounded token supersede it.

Live surface read (bytes only):
- `~/.config/mako/config` (symlink to `current/theme/mako.ini`), 5 lines: `1: include=~/.local/share/omarchy/default/mako/core.ini`; `3-5: text-color=#bebebe`, `border-color=#e68e0d`, `background-color=#121212`.
- `~/.local/share/omarchy/default/mako/core.ini`, 38 lines: global keys `:1-9`; criteria sections `[app-name=Spotify]` `:11`, `[mode=do-not-disturb]` `:14`, `[mode=do-not-disturb app-name=notify-send]` `:17`, `[urgency=critical]` `:20`, `[summary~=…]` `:24-37`. This is the file C1 must resolve through.

## 2. Overlaps, owner, verdict

Verdict key: CONTESTED = two sources claim the same surface or a claim disclaims what C1 would resolve; ADJACENT = same bytes or tool, different claim; NONE = no lane claim.

### CONTESTED

| hit | owner | overlap with C1 | verdict |
|---|---|---|---|
| `mado-shokunin/PROVINCE.md:18` (round-19 refinement) | mado, theme plane | Says `mako.ini` is "chain evidence only, their consumer configs not owned". C1 resolves the consumer config `~/.config/mako/config` and `core.ini` through that same symlink. | CONTESTED — PROVINCE disclaims the surface C1 would own. Needs a PROVINCE carve-out or the C1 claim must be scoped to read-only effective-settings semantics. |
| `mado-shokunin/SKILL.md:115` (notifications / OSD row) | mado SKILL surface table | Lists `~/.config/mako/config` as a surface of mado, with the verify path `makoctl mode` / `busctl`. | CONTESTED with PROVINCE.md:18 — mado's two surface documents disagree on whether the mako config is in scope. |
| `mado-shokunin/SKILL.md:89` (Notification silencing (DND) row) | mado SKILL | Cites `~/.config/mako/config:1-5` as the config for DND. Lines 1-5 are exactly C1's first hop (include + colours). The DND claim itself is `makoctl mode` only. | CONTESTED (same as :115). |

### ADJACENT

| hit | owner | overlap with C1 | verdict |
|---|---|---|---|
| `mado-shokunin/corpus/knowledge/waybar-walker-plane.md:24, 203-206, 211-220, 328, 331, 359, 375-377, 446` | mado MADO-2 (bar / launcher / notification plane) | Already holds the file-level `include=` line, the three overrides (`:203-206`), stock `core.ini` behaviour (`:211-219`), the `mako.ini` / config sha pin `95bf0c86…` (`:446`). No effective-settings semantics. | ADJACENT. C1 must cite it, not restate it. The declaration's "Not held … waybar-walker-plane.md covers only DND" is inaccurate. |
| `mado-shokunin/corpus/knowledge/waybar-walker-semantics.md:35, 140, 359` | mado | D-Bus owner `org.freedesktop.Notifications` (mako 1706); mako-mode indicator script. | ADJACENT (daemon ownership and DND, not config). |
| `mado-shokunin/corpus/knowledge/config-health-report-r3.md:8, 44, 74, 77, 85, 185, 209-213, 215-227, 272-273, 302, 419-421` | mado R3 record | Byte cell of `~/.config/mako/config` resolved as a symlink: "50 B" is the link's size, 119 B is the target (`:217-223`); `mako --version` misuse (F10, `:419-421`). | ADJACENT. C1 fixtures must follow the symlink; the "50 B vs 119 B" trap is already recorded here. |
| `mado-shokunin/corpus/knowledge/remaining-planes-census.md:17-18, 82, 98-106, 131, 161, 170, 245, 253-254, 305-308, 322-341` | mado census | Same symlink and pin (`95bf0c86…`); mako layer-surface mapping is transient (E2, `:326-333`). | ADJACENT. |
| `mado-shokunin/corpus/knowledge/theme-wallpaper-plane.md:14, 105, 117-118, 136, 192, 232, 292, 321-324` | mado theme plane (P5) | Carries the `theme.chain.mako_link` row (`:292`) and the target pin (`:136`). Same bytes C1 reads. | ADJACENT — but this is where the PROVINCE.md:18 contest bites. |
| `mado-shokunin/SKILL.md:1656, 1674-1681, 2503-2504` and `tools/mado-verify.sh:86-88, 342-353, 1146-1153, 4109-4110` | mado freshness gate | Existing gate row `theme.chain.mako_link` (existence + in-theme resolution), T4 negative fixture (copy in place of link), fixture `mako.ini` with `[main]` only. | ADJACENT. C1 must not duplicate or contradict the gate's hop checks. |
| `mado-shokunin/tools/mado-tripwire.py:270` | mado | `makoctl` listed in a tool-name allowlist. | ADJACENT (name only). |
| `mado-shokunin/corpus/knowledge/theme-route-r18.md:44-45, 86, 91-92, 105-108, 120-121, 139, 142` | mado theme route | `omarchy theme set` restarts mako `[OT:53-62]`; mako config is a symlink into the theme. A theme switch changes C1's input. | ADJACENT. |
| `mado-shokunin/corpus/knowledge/terminals-and-omarchy.md:86, 122, 128` | mado | Theme listing; SKILL path list including `mako`. | ADJACENT. |
| `mado-shokunin/corpus/knowledge/snapshot-diff-receipt-r9.md:72-75, 143-148` | mado | Receipt rows for `theme.chain.mako_link`. | ADJACENT. |
| `mado-shokunin/corpus/knowledge/province-accuracy-selfaudit.md:52, 84-85, 102-103, 224, 302, 328` | mado | Byte pin `95bf0c86…`; "adjacent, not declared" marker at `:84`. | ADJACENT. |
| `mado-shokunin/corpus/knowledge/host-bar-producer-census-r40.md:24-32` | mado | `notification-silencing.sh` (`makoctl mode | grep -q 'do-not-disturb'`). | ADJACENT (DND). |
| `mado-shokunin/corpus/knowledge/closeout-r11.md:48`, `arc-synthesis.md:231, 234, 282, 318` | mado summaries | Summary rows restating mako symlink / owner. | ADJACENT. |
| `mado-shokunin/corpus/lessons/round-12.md:19` (M7), `round-40.md:20-21` (S281), `round-77-verifier-spotcheck.md:122`, `round-78.md:88` | mado lessons | Count pin (`wc -c` mako config = 119), S281 script bytes, `makoctl mode` read verb, `mako-mode` frozen row. | ADJACENT. |
| `mado-shokunin/SKILL.md:218-221, 273, 482, 506, 554, 934, 1197, 1204, 1325` | mado SKILL | `makoctl mode` / `busctl` probes; mako layer transient. | ADJACENT (DND and owner probes). |
| `~/.agents/skills/omarchy/SKILL.md:6, 26, 82` | omarchy skill (upstream doc; read-only for mado, PROVINCE.md:10-11) | Names `~/.config/mako/` as an editable path and mako in the architecture table. | ADJACENT (documentation invites editing; C1 is read-only). |

### NONE

| hit | owner | verdict |
|---|---|---|
| `~/.local/share/omarchy/default/mako/core.ini` (38 L) | omarchy upstream defaults | NONE for lane ownership. It is C1's include target. Mado reads it only as chain evidence (waybar-walker-plane.md:203-206). |
| All other `*-shokunin` lanes (PROVINCE, SKILL, corpus, tools, quality, scripts, templates) | — | NONE. S1 and S2 returned no matches. |

## 3. Declaration and PROVINCE checks (line numbers verified)

- **PROVINCE.md has no "notifications / OSD" row.** Its "Owns (surfaces)" paragraph (`:6-10`) lists hypr, waybar, walker, terminal configs, themes/wallpapers, screen/idle, and the omarchy skill. Notifications are not owned. The "notifications / OSD" row exists only in `mado-shokunin/SKILL.md:115` (and DND at `:89`).
- **PROVINCE.md terminal rows:** `:7-8` (owns terminal configs, `~/.config/alacritty|foot|kitty|ghostty/`); `:154` (absent 2026-10-31, `test -e ~/.config/{alacritty,foot,kitty,ghostty}` → missing); `:268` (present 2026-11-03; alacritty the only installed consumer).
- **PROVINCE.md:130-132** (2026-10-31 absence block) lists `mako` in `command -v … → ABSENT (11/11)`. No later PROVINCE row re-measures mako's presence. [OBS from file; not re-measured live here.]
- **r86 entry:** `mado-shokunin/corpus/knowledge/refusal-records-clause-observations-r86.md:112` reads "against the held rule's `held_rule_new_case=0/1` on the same witness …". Confirmed as the sentence C2 corrects.
- **Declaration wording (`claims-declaration-r87.md:22-27`):** "Not held: no note owns it; `waybar-walker-plane.md` covers only DND". Inaccurate on the second clause (see ADJACENT row 1). Accurate form: no note holds effective-settings semantics; several notes hold the file bytes, symlink resolution, and the sha pin.

## 4. Summary

- CONTESTED: 3 (PROVINCE.md:18; SKILL.md:89; SKILL.md:115). The central question for L1: whether mado's PROVINCE.md treats the mako consumer config as in scope for C1.
- ADJACENT: 20+ rows across mado notes, lessons, tools, and the omarchy skill. All same-bytes or same-daemon, none claim effective-settings semantics.
- NONE: other lanes (0 hits); `core.ini` as lane-owned (not claimed).
- Recommended for L1 (not edited here): correct the declaration's "Not held" wording, and decide the PROVINCE.md:18 / SKILL.md:89,115 contest before C1 is claimed.
