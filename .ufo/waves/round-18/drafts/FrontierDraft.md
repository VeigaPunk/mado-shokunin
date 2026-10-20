# FrontierDraft — round 18 (README `## Frontier` bullet and index rows)

Draft for L1 integration. Not applied to `corpus/README.md`. The two linked
notes are being drafted by NoteWalker and NoteTheme; the bullet and rows
below claim only what those notes are scoped to establish and must be
re-checked against the landed notes before integration.

## 1. Frontier bullet (insert after the round-17 bullet, README line 125)

```
- Round 18 moves P3 Walker and P5 themes/wallpapers onto **documentary** sourced
  ground: [Walker route](knowledge/walker-route-r18.md) and
  [theme route](knowledge/theme-route-r18.md), upstream contracts joined to host
  file bytes. Still open: runtime theme application and wallpaper reload, Walker
  provider behaviour, the elephant service, and rendered UI for both surfaces.
  Host binaries stay `[UNK]`; no theme, wallpaper, walker or elephant command runs.
```

## 2. Index rows (insert after the `terminal-route-r17.md` row, README line 43)

```
| `knowledge/walker-route-r18.md` (round 18; surface P3) | Documentary upstream contract for Walker and elephant, joined to declared host config by sha256 and line anchor. Declared configuration is not observed launcher behaviour; provider resolution at runtime, the elephant service, socket protocol and rendered UI stay `[UNK]`. | `source:` S0xx-pending in [SOURCES](SOURCES.md); tag-pinned fetch receipts under `.ufo/waves/round-18/fetch/NoteWalker/`. No walker or elephant process is started or queried. |
| `knowledge/theme-route-r18.md` (round 18; surface P5) | Documentary upstream contract for the omarchy theme-set and wallpaper path and for swaybg, joined to `current/theme`, the current background link and consumer imports by sha256 and line anchor. Declared chain is not runtime theme application; reload effects and rendered wallpaper stay `[UNK]`. | `source:` S0xx-pending in [SOURCES](SOURCES.md); tag-pinned fetch receipts under `.ufo/waves/round-18/fetch/NoteTheme/`. No theme, wallpaper or swaybg command is run. |
```

## 3. Open dependencies for L1

- Replace every `S0xx-pending` with the ids L1 assigns in `corpus/SOURCES.md` (reserved S072-S099).
- Confirm both notes exist, carry `surface: P3` / `surface: P5` in their first 15 lines, and their section headings match the descriptions above before the rows land.
- Confirm the bullet's "Still open" list still matches the landed notes' `## Unexercised behavior` sections.
