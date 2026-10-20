# NoteIdle — SOURCES rows (draft, round 17, P6)

Ids are `S0xx-pending`; L1 assigns S056-S069 on integration. Rows are in the
11-column shape of `corpus/SOURCES.md`. Each row is followed by its gate line:
URL, access date, verbatim quote (≤25 words) with line anchor, raw SHA-256.
Access date for every row: 2026-10-20. Raw SHA-256 is over the bytes fetched
with curl at the time of access; wiki pages are dynamic HTML, so a re-fetch may
differ in markup while the text anchors still hold.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0xx-pending | hypridle wiki page — https://wiki.hypr.land/Hypr-Ecosystem/hypridle/ | docs | A | hypridle keys (general, listener), inhibit_sleep modes, condition_cmd — wiki "Latest git", page modified 2026-08-26 | raw HTML sha256 b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640; anchors are lines of the tag-stripped `<article>` text (lines 6-120) | documented meaning of lock_cmd, before/after_sleep_cmd, on-timeout/on-resume, inhibit_sleep 0-3; not version-pinned to v0.1.8 | mined | 2026-10-20 | 90d | corpus/knowledge/idle-lock-route-r17.md |
| S0xx-pending | hyprlock wiki page — https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/ | docs | A | hyprlock CLI (--grace), config search path, general/auth keys, Arch faillock note — wiki "Latest git" | raw HTML sha256 f69cff6bad5ee10c6e52fac08aca9a99473d8bbac5379ad1d47a92ba297eabf5; anchors are lines of tag-stripped `<article>` text (lines 6-85) | documented hyprlock defaults (hide_cursor, ignore_empty_input, fail_timeout, pam, fingerprint) and the no-config-no-lock warning | mined | 2026-10-20 | 90d | corpus/knowledge/idle-lock-route-r17.md |
| S0xx-pending | hypridle README @ v0.1.8 — https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md | docs | A | hypridle features, config example, usage, flags at tag v0.1.8 | file lines 5-33, 62; sha256 f5b852eefe3c6d21ede9cef8b9b2dbf55d2e9423f1224b82592aa1b4759781f6 | ext-idle-notify-v1 basis; dbus lock/unlock/before-sleep scope; exec-once usage | mined | 2026-10-20 | on-change | corpus/knowledge/idle-lock-route-r17.md |
| S0xx-pending | hypridle src/core/Hypridle.cpp @ v0.1.8 — https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp | code | A | runtime handling of idle notifications, inhibits, dbus Lock/Unlock, PrepareForSleep, ScreenSaver registration, lock-notify | file lines 58, 70-74, 104-132, 301, 327, 346-352, 372-404, 433-485, 493-510, 600-626; sha256 2dd4d73d4f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75 | order of effects: inhibit gate before on-timeout; on-resume only after fired on-timeout; before/after sleep commands; ignore_dbus_inhibit gates ScreenSaver registration | mined | 2026-10-20 | on-change | corpus/knowledge/idle-lock-route-r17.md |
| S0xx-pending | hypridle src/core/Hypridle.hpp @ v0.1.8 — https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.hpp | code | A | SIdleListener fields | file lines 23, 26; sha256 f9e4e5587075fe34ae3279c4225b00661c686468035c4ad6cbe71e098fc0a2b8 | per-listener ignoreInhibit and conditionRetry state | mined | 2026-10-20 | on-change | corpus/knowledge/idle-lock-route-r17.md |
| S0xx-pending | hypridle src/main.cpp @ v0.1.8 — https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/main.cpp | code | A | config lookup and startup failure when no hypridle.conf exists | file lines 55-63; sha256 379bf321a53edc56bde5f81fe070a2519a53bf17ca3b89937c1a027bad672a38 | a missing config is a fatal CRIT path, not a silent default | mined | 2026-10-20 | on-change | corpus/knowledge/idle-lock-route-r17.md |
| S0xx-pending | hyprlock README @ v0.9.6 — https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/README.md | docs | A | hyprlock features, docs pointer, build deps at tag v0.9.6 | file lines 5, 19; sha256 83096def1a9760088ee6508d550f9498aab959176ae50f90720a57fe838f50f3 | ext-session-lock protocol basis; README points to the older wiki domain (wiki.hyprland.org) | mined | 2026-10-20 | on-change | corpus/knowledge/idle-lock-route-r17.md |

## Gate lines

1. **hypridle wiki** — URL https://wiki.hypr.land/Hypr-Ecosystem/hypridle/ · access 2026-10-20 · quote [HW:6]: "Configuration is done via the config file at ~/.config/hypr/hypridle.conf." · raw SHA-256 b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640
2. **hyprlock wiki** — URL https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/ · access 2026-10-20 · quote [LW:7]: "If no config file is found in any of the searched paths, hyprlock exits with an error and your session will not be locked." · raw SHA-256 f69cff6bad5ee10c6e52fac08aca9a99473d8bbac5379ad1d47a92ba297eabf5
3. **hypridle README v0.1.8** — URL https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md · access 2026-10-20 · quote [HR:6]: "support for dbus' loginctl commands (lock / unlock / before-sleep)" · raw SHA-256 f5b852eefe3c6d21ede9cef8b9b2dbf55d2e9423f1224b82592aa1b4759781f6
4. **Hypridle.cpp v0.1.8** — URL https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp · access 2026-10-20 · quote [HC:473]: `if (MEMBER == "Lock") {` · raw SHA-256 2dd4d73d4f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75
5. **Hypridle.hpp v0.1.8** — URL https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.hpp · access 2026-10-20 · quote [HH:23]: `ignoreInhibit     = false;` · raw SHA-256 f9e4e5587075fe34ae3279c4225b00661c686468035c4ad6cbe71e098fc0a2b8
6. **main.cpp v0.1.8** — URL https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/main.cpp · access 2026-10-20 · quote [HM:61]: "No hypridle.conf file found in:" · raw SHA-256 379bf321a53edc56bde5f81fe070a2519a53bf17ca3b89937c1a027bad672a38
7. **hyprlock README v0.9.6** — URL https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/README.md · access 2026-10-20 · quote [LR:5]: "Uses the ext-session-lock protocol" · raw SHA-256 83096def1a9760088ee6508d550f9498aab959176ae50f90720a57fe838f50f3

Not opened as rows (fetched only to confirm absence): the tag trees for
hypridle v0.1.8 and hyprlock v0.9.6 at `/tree/<tag>` and `/tree/<tag>/src`
(listing HTML, sha256 not recorded), and the upstream `example/hypridle.conf`
and `example/hyprlock.conf` raw paths, which returned HTTP 404 at both tags.
