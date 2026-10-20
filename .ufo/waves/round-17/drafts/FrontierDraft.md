# FrontierDraft — round 17 (draft for L1 integration; not landed)

Target: `corpus/README.md` `## Frontier` (append after the round-16 bullet, line 116) and `## Coverage map` table (new rows after line 41). Source ids are `S0xx-pending`; L1 assigns S056–S069 on integration. Link targets exist only after NoteIdle/NoteTerminal land.

## Frontier bullet (append to `## Frontier`)

- Round 17 moves P6 screen/idle (hypridle/hyprlock) and P4 terminal-emulator configs onto **documentary** sourced ground: [idle/lock route](knowledge/idle-lock-route-r17.md) (upstream listener/lock contract joined to host file bytes) and [terminal route](knowledge/terminal-route-r17.md) (`bindings.conf:2` → `xdg-terminal-exec` → `xdg-terminals.list` naming `Alacritty.desktop`, then the Alacritty config contract). Sources are `S0xx-pending` until integration.
  Still open: idle/lock transitions, listener firing, lock success and stop-cause; which terminal actually launches (the list's first valid entry is a documented rule, not an observed launch) and Alacritty reload effects; P3 Walker sourced routes; P5 theme/wallpaper sourced routes (chain existence is not rendering).
  No lock, suspend, DPMS, idle interval, terminal launch or screenshot is claimed; host versions stay `[UNK]`.

## Coverage map rows (insert after the `waybar-observation-boundaries-r16.md` row)

| `knowledge/idle-lock-route-r17.md` (round 17; covers P6) | Documentary upstream contract for hypridle and hyprlock (listener timeouts, lock/sleep hooks, inhibit) joined to the host's declared files by sha256 and line anchor. Declared timings are not observed behaviour; transitions and lock success stay `[UNK]`. | `source:` S0xx-pending (hypridle/hyprlock wiki and tag-pinned upstream) in [SOURCES](SOURCES.md); host bytes `~/.config/hypr/hypridle.conf` and `hyprlock.conf` by sha256; link [idle-lock-plane.md](knowledge/idle-lock-plane.md) §11 for open unknowns. No lock, suspend or listener is triggered. |
| `knowledge/terminal-route-r17.md` (round 17; covers P4) | Documentary route from the Hyprland launch binding through `xdg-terminal-exec` and `xdg-terminals.list` (first entry `Alacritty.desktop`) to the Alacritty config-import contract. Which terminal actually launches and reload effects stay `[UNK]`. | `source:` S0xx-pending (xdg-terminal-exec upstream, Alacritty tagged manual) in [SOURCES](SOURCES.md); host bytes `~/.config/hypr/bindings.conf` and `~/.config/xdg-terminals.list` by sha256. No terminal is launched. |

## Host bytes read for this draft (file reads only; no omarchy/hypr/terminal commands)

- `~/.config/xdg-terminals.list` — sha256 `d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b`; comment lines 1–2 state "The first found and valid terminal will be used"; line 3 `Alacritty.desktop`. Size 127 B is carried from terminals-and-omarchy.md §1 and was not re-measured here.
- `~/.config/hypr/bindings.conf` — sha256 `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581`; line 2 `bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir=...`.
- `~/.config/hypr/hypridle.conf` — sha256 `e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41` (matches idle-lock-plane.md §2 pin).
- `~/.config/hypr/hyprlock.conf` — sha256 `b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1` (matches idle-lock-plane.md §2 pin).

## Caveats

- The two note paths and their `source:` ids are not yet on disk; L1 must confirm the links resolve after integration.
- The Coverage map and Province routes tables already route P4 and P6 to inherited 2026-10-14 notes; the new rows add sourced documentary routes beside them, not a replacement for those rows.
