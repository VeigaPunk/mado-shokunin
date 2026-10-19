# L2 seat R12Portal-3 — final output (verbatim, 2026-10-19)

**Files written**

- `corpus/knowledge/xdg-portal-routing-r12.md` — 123 lines; `5c71579f826a4588`
- `.ufo/evidence/round-12/portal-host.txt` — 142 lines; `6b3049668f615ef1`
- `.ufo/round-12/sources/portal.md` — 31 lines; `e2309a06f35cbf7a`

Line counts: `123 — wc -l /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/mado-shokunin/corpus/knowledge/xdg-portal-routing-r12.md 2026-10-19`; `142 — wc -l /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/mado-shokunin/.ufo/evidence/round-12/portal-host.txt 2026-10-19`; `31 — wc -l /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/mado-shokunin/.ufo/round-12/sources/portal.md 2026-10-19`.

**Behavior and retained evidence**

- The entry maps interfaces to configured backend candidates using the observed Hyprland profile and installed `.portal` declarations. It documents the ScreenCast v6 lifecycle and distinguishes each stage’s evidence from end-to-end capture.
- Host observations: `pacman -Q xdg-desktop-portal xdg-desktop-portal-hyprland xdg-desktop-portal-gtk` reported `1.22.1-2`, `1.4.1-2`, and `1.15.3-1`. `XDG_CURRENT_DESKTOP=Hyprland`; `hyprland-portals.conf` declares `default=hyprland;gtk`. All three queried portal units were active. Read-only ScreenCast property reads returned `version=u 6` and `AvailableSourceTypes=u 7`.
- Retained evidence is `E-PT-PORTAL-HOST` in `portal-host.txt`; the source fragment records opened-source quotes and identifies six sources cited by the entry. No portal request or method was issued.

**Risks / blockers**

- No runtime request, dialog, consent, session, or stream was tested. Active units and config do not prove capture success; the `Secret` provider and actual request routing remain unknown. Profile selection is conditional on the daemon using the observed desktop environment.
- No blockers to the scoped implementation. Build, lint, and tests were not run; the parent owns post-integration verification.
