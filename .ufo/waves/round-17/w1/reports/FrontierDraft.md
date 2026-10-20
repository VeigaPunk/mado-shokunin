# FrontierDraft — round 17 report (seat MadoR17.FrontierDraft)

## Behavior
Drafted the README `## Frontier` bullet and two `## Coverage map` index rows for round 17, covering the P6 idle/lock route and the P4 terminal route as documentary, sourced ground. Each entry names what remains open: transitions, actual lock behaviour, which terminal launches, reload effects, P3 Walker, and P5 themes/wallpapers.

## Gates
- No pacman, yay, paru, sudo, systemctl, hyprctl, omarchy-*, hypridle, hyprlock, alacritty, waybar, walker, notify-send, screenshot or device/input probe was run, in any form.
- Host bytes were read with `cat` and `sha256sum` only: `~/.config/xdg-terminals.list`, `~/.config/hypr/bindings.conf`, `~/.config/hypr/hypridle.conf`, `~/.config/hypr/hyprlock.conf`.
- No jj or git commands were run in the lane.
- The two new note files do not exist yet (`corpus/knowledge/idle-lock-route-r17.md`, `corpus/knowledge/terminal-route-r17.md`); the draft links to them as pending, and L1 must verify the links after integration.

## Touched surfaces
- Written: `.ufo/waves/round-17/drafts/FrontierDraft.md` (the draft, assigned).
- Written: `.ufo/waves/round-17/w1/reports/FrontierDraft.md` (this report).
- Not touched: `corpus/README.md`, `corpus/SOURCES.md` and all other L1-owned files. Integration is L1's job.

## Host-byte observations (file reads only)
- `~/.config/xdg-terminals.list`: sha256 `d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b`. Comment lines 1–2 read "The first found and valid terminal will be used"; line 3 is `Alacritty.desktop`. The 127 B size is carried from `terminals-and-omarchy.md` §1 and was not re-measured here.
- `~/.config/hypr/bindings.conf`: sha256 `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581`; line 2 binds `SUPER, RETURN` to `uwsm-app -- xdg-terminal-exec`.
- `~/.config/hypr/hypridle.conf`: sha256 `e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41`, matching the `idle-lock-plane.md` §2 pin.
- `~/.config/hypr/hyprlock.conf`: sha256 `b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1`, matching the `idle-lock-plane.md` §2 pin.

## Findings
1. The spec asks for the two new sourced routes to be recorded in the Frontier and index. The source ids for both notes are still `S0xx-pending`, pending the sibling NoteIdle and NoteTerminal seats and L1's SOURCES integration.
2. The existing Province routes table already sends P4 and P6 to inherited notes. The new index rows add sourced documentary routes beside those rows and do not replace them.
3. The terminal bullet records that the list is a documented first-valid-entry rule. Which terminal actually launches is not observed and stays `[UNK]`.
4. The draft does not claim a lock, suspend, DPMS change, idle interval, terminal launch or screenshot.

## Out of scope
- Source-row authoring for either note, and the two note bodies (sibling seats).
- Any edit to `corpus/README.md`; L1 integrates the draft.
- P3 Walker and P5 themes sourced routes, which are named as open in the Frontier.

## Tool installs or updates
None. No tool was installed or upgraded in this seat.

## Checks for the main agent after integration
- Confirm `corpus/knowledge/idle-lock-route-r17.md` and `corpus/knowledge/terminal-route-r17.md` exist and that the README links resolve.
- Replace every `S0xx-pending` with the assigned S056–S069 ids, in the notes' `source:` lines and in the index rows.
- Confirm the index rows' `(round 17; covers P4/P6)` tags match each note's `surface:` line.

## Artifacts
- `.ufo/waves/round-17/drafts/FrontierDraft.md`
- `.ufo/waves/round-17/w1/reports/FrontierDraft.md`
