# NoteIdle — round 17 P6 documentary route (idle/lock)

## Behaviour
Drafted the P6 sourced documentary route note for hypridle and hyprlock (surface P6, route for the idle/lock plane). The note records the upstream contract with source anchors, the host declaration as file bytes with sha256, a safe-observation list, and an explicit unexercised list. Nothing was executed on the host. No listener, lock or inhibit was triggered.

## Files written (only these two)
- `corpus/knowledge/idle-lock-route-r17.md` — route note. Head lines 1-4 are `source:` / `verified-at:` / `recheck:` / `surface: P6`. Links `corpus/knowledge/idle-lock-plane.md` §11 and narrows its items 1, 2, 5, 6 and 8.
- `.ufo/waves/round-17/drafts/NoteIdle-rows.md` — seven SOURCES rows (ids `S0xx-pending`, 11-column shape), each with a gate line: URL, access date 2026-10-20, ≤25-word verbatim quote with line anchor, raw SHA-256.
- `.ufo/waves/round-17/w1/reports/NoteIdle.md` — this report.

## Gates and evidence
- Tag resolution: `releases/latest` redirect → hypridle `v0.1.8`, hyprlock `v0.9.6`. The GitHub REST API returned rate-limit 403 and was not used.
- Raw sources fetched with curl and hashed (sha256 in the drafts file). All 24 quotes and key line anchors were re-checked with `grep -nF` against the fetched bytes before writing; two anchors (HC:97, HC:480-484) were wrong on first pass and were corrected to HC:601/617 and HC:480-485.
- Host bytes read with `cat -n` / `sha256sum` only: `~/.config/hypr/hypridle.conf` (e7d3b8dd…de41), `hyprlock.conf` (b8d173dc…68fc1), omarchy theme `hyprlock.conf` (3ef010e7…ad0b), omarchy `omarchy-system-lock` (c1dd3881…ce1), `omarchy-system-wake` (09ad52b0…d3bd4), `omarchy-launch-screensaver` (ba783a3a…fa12), omarchy default `hypr/autostart.conf` (acb6a668…441). User `~/.config/hypr/autostart.conf` (5ace1701…c46) read too; it does not start hypridle.
- No validation or build was run. Per the lane contract only L1 verifies.

## Findings
1. hypridle is started by the omarchy default autostart (`exec-once = uwsm-app -- hypridle`, default autostart.conf:1), not by the user `autostart.conf`. Whether the default file is sourced on this host is `[UNK]` (hyprland.conf not read for this note). This narrows `idle-lock-plane.md` §11 item 1 without resolving it.
2. Host `inhibit_sleep = 3` depends on the compositor exposing `hyprland-lock-notify-v1`; upstream warns that without it `inhibit_sleep=3`, `on_lock_cmd` and `on_unlock_cmd` do not work ([HC:104-107]). Host support is `[UNK]`. This is the same gap as `idle-lock-plane.md` §11 item 6.
3. The host "screensaver resets idle timer" comment (hypridle.conf:14) is a runtime claim, not documented upstream; it remains `[UNK]`.
4. The upstream `example/` configs return 404 at both tags; the wiki's example-config link target was not extracted. Recorded as `[UNK]`.
5. hyprlock README points at `wiki.hyprland.org`; the live wiki is `wiki.hypr.land`. Documentary drift, not a defect in the host.
6. The wiki is "Latest git" (last updated 2026-08-26), not pinned to v0.1.8 / v0.9.6. Recorded as a recheck item.

## Out of scope / not done
- No host observation of idle timing, listener firing, lock success, or inhibit state. Those stay `[UNK]` in the note.
- hyprlock source (grace, fail_timeout, faillock) not opened; documentary wiki and README only.
- Host binary versions of hypridle and hyprlock: `[UNK]`. No package query ran.
- No edits to SOURCES.md, SKILL.md, SCORECARD.md, LOG.md, PROVINCE.md or other L1-owned files.

## Pause compliance
Host pacman transactions are paused. Nothing from the pacman/yay/paru, sudo, systemctl, hyprctl, libinput, evtest, hypridle, hyprlock, loginctl, journalctl, pidof or omarchy-* families was run. No tools were installed or updated (curl and sha256sum were already present). The operator tooling directive's `sudo pacman` channel was not used.

## Artifact paths
- /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/idle-lock-route-r17.md
- /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/drafts/NoteIdle-rows.md
- /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/w1/reports/NoteIdle.md
- Scratch fetches (not deliverables): /tmp/noteidle/

## Checks for L1 to run once after integration
- Recompute sha256 of the six host files and the three omarchy scripts against the note's table.
- Re-fetch the two wiki URLs and four tag-pinned raw URLs; compare with the rows file digests (wiki digests may differ on markup, text anchors should hold).
- Assign S056–S069 ids to the seven `S0xx-pending` rows and replace the `source:` line placeholders in the note's line 1.
- Confirm `covers`/`surface: P6` is read by the coverage check (note head line 4 carries `surface: P6`; the `source:` line is line 1).
