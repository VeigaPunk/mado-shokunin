# L2 seat R12Scribe-3 — final output (verbatim, 2026-10-19)

**Files written** (only one; nothing outside my set):
- `W/.ufo/round-12/sources/local.md` — 47 lines — sha256 `818d4f637b29ae12…` (untracked: `git status` shows `?? .ufo/round-12/sources/` — L2 does not commit). No writes in fleet root, /tmp, or any sibling.

**Content**: 12 rows (`rows=12`), namespace `S@LOC1`–`S@LOC12`; 4 `mined` (round-10.md lessons :63-123; arc-synthesis §6 :290-307; PROTOCOL.md §Evidence :328-358 + §Gate :360-408; kaika SOURCES contract), 6 `queued` (wayland-protocols README phases, freedesktop extras, libinput tools, wayland-book high-level design, freedesktop architecture page, wayland.app tier C), 2 `rejected` (fleet MANIFEST verdicts; version-unanchored Filip Mikina blog).

**Acceptance checks** (re-runnable, 2026-10-19):
- `awk -F'|' '/^\|[[:space:]]*S@/ && NF!=13'` → no output (all 11-column, NF=13).
- `grep -cE '\| rejected \|'` → 2; `grep -cE '^- S@LOC[0-9]+ — '` → 12 (one Gate bullet per row, each with a verbatim ≤25-word quote + location).
- Anchors verified by brace/direct reads: fleet HEAD `31baf5c`, PROTOCOL.md sha `b1d4f4c094052298…`; ledger HEAD `959b746`, contract committed at `5b471e4` sha `6c674a2281afb75b…`; W HEAD `a6528e6`, round-10.md `d7b4708e864fca29…` (226 L), arc-synthesis `a5b4833141461810…` (387 L).

**Key measured values**:
- `jq '[.rounds[]|select(.lane=="mado")|.verdicts|to_entries[]|select(.value=="improved")]|length' fleet-ledger/MANIFEST.json` → **45**; manifest-only **28** re-derived against `SCORECARD.md:11-26` axis rows (2+3+1+3+5+3+3+3+3+2) — matches dossier §2.2 exactly. Grounds the S@LOC11 rejection.
- wayland-protocols README revision pinned via GitLab API (`path=README.md&per_page=1`) → `3dac056d`, 2026-01-16.
- Blog rejection grounded on full 335-line read: no Hyprland version named anywhere; quote "This works if the window class/title is known at creation time."

**Search log**: 4 bounded notes (rejection sweep 8→1 opened→1 rejected / frontier opens 7 opened→6 rows / chapter-location 10→1 / MANIFEST re-measure unit-exact), each with counts, exclusion reasons, stop rationale.

**Open risks** (integrator): (1) used-by for LOC1/3/4 cites `corpus/lessons/round-12.md` (C1 seat, in flight) and LOC2 cites `corpus/knowledge/window-rule-effects-getprop.md` (R12RuleEffects-3, in flight) — both must exist before the merged SOURCES census or the "mined used-by path exists" check flags them; (2) `S@LOCn` ids need renumbering on merge; (3) my 28-count re-derivation used the SCORECARD axis rows directly, not the dossier's python script — agreement was unit-exact, but a differing reading of "lane axis move" rows would move it.
