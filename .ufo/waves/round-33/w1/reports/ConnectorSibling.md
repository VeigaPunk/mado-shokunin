# ConnectorSibling — round 33, wave 1

Question: does a sibling lane's `PROVINCE.md` already own Waybar module text, or Hyprland event-queue removal?

Verdict: **none**.

## Scan

Read-only. Twenty sibling `PROVINCE.md` files under `/home/vgpnk/Projects/shokunin/*-shokunin/` (mado excluded as self). No sibling file edited.

- audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mori, revenger, souji, tabi, tameshi, tsukuroi.

Searched each for Waybar / waybar, Hyprland / hypr, module text, event-queue / event queue, compositor, status bar, and a second pass for module / queue / waybar / hyprctl / socket2.

No sibling `Owns` / `Domain` clause names Waybar module text or Hyprland event-queue removal.

## Near misses (attribution, not ownership)

These name the surface and give it to mado, or use "queue" / "removal" for a different object:

- `tsukuroi-shokunin/PROVINCE.md:124` — OUT-004: "Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and screen/idle behavior." Tsukuroi does not take it. Its own owns clause (`:8-14`) is pacman, systemd, journal/boot, driver/firmware.
- `game-dev-3d-shokunin/PROVINCE.md:75` — "Desktop/compositor display behavior belongs to `mado-shokunin` (`../mado-shokunin/PROVINCE.md:3-12`)."
- `kotoba-shokunin/PROVINCE.md:61` — census row `mado | none | … | desktop and compositor craft`; split recorded as `none`. Kotoba owns prompt and skill craft (`:3-5`), not bar text.
- `souji-shokunin/PROVINCE.md:3-4` — owns "receipt-gated removal of stale, duplicate, and already-preserved artifacts" on fleet hygiene surfaces (`:8-16`). Not a Hyprland event queue.
- `kaidoku-shokunin/PROVINCE.md:104` — "it does not run a triage queue". RE of shipped artifacts, not compositor event-manager removal.
- `kumitate-shokunin` and `mori-shokunin` queue hits are broker/workflow queues and OMP job `queued` state (`kumitate` province bands; `mori-shokunin/PROVINCE.md:325-336`). Not Hyprland `EventManager` removal.

## Self, not a sibling

The only ownership claim for this surface is mado's own file: `mado-shokunin/PROVINCE.md:3` (domain: Hyprland/waybar/walker configuration plane and display behavior) and `:6-7` (`~/.config/hypr/`, `~/.config/waybar/`). That is the asking lane, not a sibling.
