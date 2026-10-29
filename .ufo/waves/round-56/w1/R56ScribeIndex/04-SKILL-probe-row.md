# R56ScribeIndex — SKILL.md integration draft (L1 applies; drafts only)

## 4a. Placement

Insert as a new last row of the table `### Read-only probes (all executed 2026-10-14 unless cited)` (SKILL.md lines 204-225), directly after the `hyprctl clients -j \| python3 tools/mado-geometry.py ...` row (SKILL.md:225), before the blank line and `### Advertised Wayland globals` (SKILL.md:227). Only that table is touched.

## 4b. Row

| `python3 -I tools/mado-watchplan.py --config $HOME/.config/hypr/hyprland.conf --home $HOME --getoption <file>` (capture first with the read verb `hyprctl getoption misc:disable_autoreload -j > <file>`; `<file>` an absolute scratch path) | the inotify watch list Hyprland 0.56.2 registers for the config tree (main config plus its `source =` closure, with symlink canonical watches), `autoreload` on or off, joined to the live `misc:disable_autoreload` value in one `MADO_WATCH_LIVE:` line (AGREE, DIFFER or UNKNOWN); read-only, no filesystem event is generated and no reload is observed; contract in `.ufo/waves/round-56/registration.md` §C2 | `to be filled at integration` |

## 4c. Notes for L1

- The tool `tools/mado-watchplan.py` does not exist at the lane base `3423ae28` (checked: `ls` and `git ls-tree`). The sample is therefore not filled; per the seat brief it is marked `to be filled at integration`. Do not fill it from a capture that did not come from this tool.
- The sample must come from the host run at integration, read-only. At this seat the live read was captured to `receipts/getoption-disable_autoreload.json` (`{"option": "misc:disable_autoreload", "int": 0, "set": false }`, 2026-10-28), which is the input file the probe would take; it is not the probe's output.
- The row has no `|` inside a cell (the SKILL table escapes pipes as `\|` elsewhere; none is needed here).
- The table header says "all executed 2026-10-14 unless cited"; this row is cited to the round-56 contract and is not an executed 2026-10-14 probe, so the header stays accurate.

## 4d. Existing SKILL text this row must not contradict

- `SKILL.md:112` (hypr core row) — "auto-reloads on save (omarchy skill:145)": a documentary claim from the omarchy skill; round 56 sources the mechanism but observes no reload, so this row must not promote it to observed.
- `SKILL.md:197-199` (safe-probe discipline) — "Hyprland auto-reloads on config save" as the reason for read-only strictness. The new row is read-only and says so.
- `SKILL.md:145-148` / `:477` (omarchy's validation pair `hyprctl reload` plus `hyprctl configerrors`) — mado runs only the `configerrors` read leg; the new row never runs `hyprctl reload` or `keyword`.
- `SKILL.md:204` (table header date claim, see 4c).
- `SKILL.md:2107-2134` (round-46 devices section) and the round-45 monitors section — the house pattern for a join-tool section; the probe row follows the same read-only framing.
- `PROVINCE.md:10-16` — config trees read-only, no compositor mutation.
