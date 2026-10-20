# SrcHypridleWiki — round 17 scoped report

## Behavior

Opened `https://wiki.hypr.land/Hypr-Ecosystem/hypridle/` once (2026-10-20, 14:00:43 GMT),
recorded its metadata, section inventory, and verbatim quotes for the five general
options, the three listener keys, and the dbus/loginctl lock surface. Wrote only this
report. Nothing installed or upgraded.

Host-touching work, all permitted read-only: one `curl` GET of the wiki page (and two
404 probes + one rate-limited API probe for upstream provenance), plus reading
`~/.config/hypr/hypridle.conf` as file bytes (`grep`, `wc`, `sha256sum`). No
pacman/yay/paru/sudo/systemctl/hyprctl/`hypridle`/`hyprlock` invocation, no live probe,
no service or compositor operation. Commands that appear in quotes below are page
content and were never executed.

## Source receipt

| Field | Value |
|---|---|
| URL | `https://wiki.hypr.land/Hypr-Ecosystem/hypridle/` |
| canonical | `<link rel=canonical href=https://wiki.hypr.land/Hypr-Ecosystem/hypridle/>` |
| HTTP | 200, `content-length: 254750`, `server: cloudflare`, `date: Tue, 20 Oct 2026 14:00:43 GMT`, `cf-cache-status: DYNAMIC` |
| raw SHA-256 | `b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640` |
| size / lines | 254750 bytes, 624 lines (article body occupies lines 555–624; each is one long line) |
| fetched | 2026-10-20, file kept at `/tmp/hypridle.html` (scratch, outside the lane) |

Upstream pinning was **not** obtained, and the report does not pretend otherwise:

- The page's "edit this page" link resolves to
  `https://github.com/hyprwm/hyprland-wiki/edit/main/content/Hypr%20Ecosystem/hypridle.md`.
- `raw.githubusercontent.com` for that path returned **404** on two URL forms
  (`refs/heads/main/…` and `github.com/…/raw/main/…`).
- `api.github.com/repos/hyprwm/hyprland-wiki` returned **403** (`API rate limit exceeded
  for 179.218.13.209`, unauthenticated) — so no commit SHA or upstream digest is claimed.
- Consequence: the citation anchor is the **fetched HTML bytes** (digest above), not a tag
  or commit. The page is mutable; recheck by re-fetching and comparing the digest.

## Page modified date / version marker

| Marker | Observed | Where |
|---|---|---|
| `article:modified_time` | `2026-08-26T14:50:40+02:00` | `<meta property=…>` line 93 |
| `itemprop=dateModified` | `2026-08-26T14:50:40+02:00` (identical) | line 98 |
| `itemprop=wordCount` | `1008` | line 98 |
| visible footer | "Last updated on August 26, 2026" in `<time datetime=2026-08-26T14:50:40.000Z>` | line 624 |
| edition badge | **"Latest git"** | page header |
| version selector | link `href=/version-selector/` (two renderings); **no numeric version on this page**, no `0.x.y` selector href | header |
| generator meta | absent | — |

Label for any C2 use: **current-wiki "Latest git" edition, modified 2026-08-26**. This is
the same era marker the lane already records for S016 and S017 ("page marked Latest git;
modified 2026-08-26"), so this page is consistent with the post-0.55 Lua-era documentation
set — it is **not** a version-pinned source. The host's `hypridle` binary version is
`[UNK]` this round: package queries are paused, so no `-Q`/`-Si` evidence exists. The lane's
older note records `hypridle v0.1.8` from a prior round
(`corpus/knowledge/hyprland-config-plane.md:157`); that is historical evidence, not
re-verified here, and must not be read as "supports everything this page documents".

## Sections (in page order, with anchors and HTML line)

| Level | Section | Anchor | Line |
|---|---|---|---|
| H1 | hypridle | — | 555 |
| H2 | Configuration | `#configuration` | 555 |
| H3 | General | `#general` | 557 |
| H3 | Listeners | `#listeners` | 558 |
| H4 | Conditional timeouts | `#conditional-timeouts` | 564 |
| H3 | Examples | `#examples` | 580 |
| H3 | Recipes | `#recipes` | 614 |
| H4 | Fading the keyboard backlight | `#fading-the-keyboard-backlight` | 615 |

There is **no dedicated D-Bus, logind, systemd or "lock behaviour" section**. All dbus /
`loginctl` content lives in the General table rows, the General inhibitor note, and the
Examples code block. Page pager: previous `hyprlauncher`, next `hyprlock`. Outbound repo
links: `hyprwm/hypridle`, `hyprwm/Hyprland`, `queueingqt/hypr-kbd-backlight-fade`.

## Quotes — configuration frame

Each quote is a verbatim contiguous string from the tag-stripped page text (curly
apostrophes normalized to `'`); word counts ≤25 by construction and checked.

- "hypridle is Hyprland's idle management daemon." — 6 words
- "Configuration is done via the config file at ~/.config/hypr/hypridle.conf." — 9 words
- "A config file is required; hypridle won't run without one." — 10 words
- "To run hypridle at startup, add hypridle to your autostart commands in your hyprland config." — 15 words
- "If Hyprland is started with uwsm, you can use systemctl --user enable --now hypridle.service." — 14 words

## Quotes — general options (`#general`, table at line 558)

Table columns are `Variable | Description | Type | Default`. Every row below is quoted
from its Description cell; Type/Default are the same row's cells.

| Variable | Verbatim description | Type | Default |
|---|---|---|---|
| `lock_cmd` | "command to run when receiving a dbus lock event (e.g. loginctl lock-session)" (12 w) | string | empty |
| `unlock_cmd` | "command to run when receiving a dbus unlock event (e.g. loginctl unlock-session)" (12 w) | string | empty |
| `on_lock_cmd` | "command to run when the session gets locked by a lock screen app" (13 w) | string | empty |
| `on_unlock_cmd` | "command to run when the session gets unlocked by a lock screen app" (13 w) | string | empty |
| `before_sleep_cmd` | "command to run when receiving a dbus prepare_sleep event" (9 w) | string | empty |
| `after_sleep_cmd` | "command to run when receiving a dbus post prepare_sleep event" (10 w) | string | empty |
| `ignore_dbus_inhibit` | "whether to ignore dbus-sent idle inhibit events (e.g. from firefox)" (10 w) | bool | false |
| `ignore_systemd_inhibit` | "whether to ignore systemd-inhibit --what=idle inhibitors" (6 w) | bool | false |
| `ignore_wayland_inhibit` | "whether to ignore Wayland protocol idle inhibitors" (7 w) | bool | false |
| `inhibit_sleep` | "sleep inhibition mode: 0: disable 1: normal 2: auto 3: lock notify" (12 w) | int | 2 |

`inhibit_sleep`'s meaning is spelled out in the General note block:

- "The general:inhibit_sleep option is used to make sure hypridle can perform certain tasks before the system goes to sleep." — 19 words
- "0 disables sleep inhibition." — 4 words
- "1 makes the system wait until hypridle launched general:before_sleep_cmd." — 9 words
- "2 (auto) selects either 3 or 1 depending on whether hypridle detects if you want to launch hyprlock before sleep." — 20 words
- "3 makes your system wait until the session gets locked by a lock screen app. This works with all wayland session-lock apps." — 22 words

## Quotes — listeners (`#listeners`, table at line 558)

- "Hypridle uses listeners to define actions on idleness." — 8 words
- "Every listener has a timeout (in seconds)." — 7 words
- "When action is resumed after idle, on-resume will fire." — 9 words
- "You can define as many listeners as you want." — 9 words

| Variable | Verbatim description | Type | Default |
|---|---|---|---|
| `timeout` | "Idle time in seconds." (4 w) | int | "none, value must be specified" |
| `on-timeout` | "Command to run when timeout has passed." (7 w) | string | empty |
| `on-resume` | "Command to run when activity is detected after timeout has fired." (11 w) | string | empty |
| `ignore_inhibit` | "Ignore idle inhibitors (of all types) for this rule." (9 w) | bool | false |
| `condition_cmd` | "Command run when the timeout is reached, before on-timeout. Run via /bin/sh -c; exit code 0 lets on-timeout fire, non-zero defers it." (22 w) | string | empty |
| `condition_retry` | "When condition_cmd defers, re-run it every N seconds while the user stays idle" (13 w) + "0 disables retrying (the deferred on-timeout is skipped for this idle cycle)." (12 w) | int | 0 |

Conditions, from the prose (`#conditional-timeouts`, lines 565–572):

- "A listener can gate its on-timeout on external state with condition_cmd." — 11 words
- "condition_cmd runs synchronously on hypridle's event loop, so keep it fast" — 11 words
- "Retry timing is checked on hypridle's ~5s event-loop tick" — 9 words

The inline listener example (lines 560–564) is an `ini` block whose comments are the
contract: `timeout = 500  # in seconds.`, `on-timeout = notify-send "You are idle!"  # command to run when timeout has passed.`,
`on-resume = notify-send "Welcome back!"  # command to run when activity is detected after timeout has fired.`

## Quotes — dbus / loginctl lock behaviour

The page's only dbus statements are the five table rows and one recipe sentence. It never
names a D-Bus service, interface, method or signal — the words are generic events.

- dbus **lock** event → `lock_cmd`; the page's own loginctl example is
  "command to run when receiving a dbus lock event (e.g. loginctl lock-session)" (12 w).
- dbus **unlock** event → `unlock_cmd`, example `loginctl unlock-session` (12 w quote above).
- session locked/unlocked **by a lock screen app** → `on_lock_cmd` / `on_unlock_cmd`
  (13 w each, quoted above). These are the post-lock hooks, distinct from `lock_cmd`.
- dbus **prepare_sleep** event → `before_sleep_cmd`; dbus **post prepare_sleep** event →
  `after_sleep_cmd` (9 w / 10 w, quoted above).
- dbus-sent idle inhibits → `ignore_dbus_inhibit`, "whether to ignore dbus-sent idle inhibit events (e.g. from firefox)" (10 w), default `false`.
- The sleep/lock coupling is `inhibit_sleep`, whose mode `3` "makes your system wait until
  the session gets locked by a lock screen app" and which "works with all wayland
  session-lock apps" (22 w quote above); mode `2` (the default) auto-selects 3 or 1.
- `loginctl lock-session` recurs as the page's canonical lock trigger: in the `lock_cmd`
  description, in the Examples block (`before_sleep_cmd = loginctl lock-session`) and in a
  300 s listener (`on-timeout = loginctl lock-session`).

Explicit `[UNK]` — the page does **not** state: the emitting D-Bus interface or signal
names (no `org.freedesktop.login1` string appears), whether hypridle's own D-Bus service
name is stable, whether `lock_cmd` is awaited, retried or how its exit code is treated,
any ordering guarantee between `lock_cmd` and `on_lock_cmd`, or any behaviour of
`loginctl unlock-session` beyond being the example trigger. A documentary route built on
this page must stop at "the wiki describes an event-triggered command hook".

## What this source can and cannot support (C2 / P6 boundary)

**Can** — a P6 note may say: the current wiki documents option names `lock_cmd`,
`unlock_cmd`, `on_lock_cmd`, `on_unlock_cmd`, `before_sleep_cmd`, `after_sleep_cmd`,
`ignore_dbus_inhibit`, `ignore_systemd_inhibit`, `ignore_wayland_inhibit`,
`inhibit_sleep`; the listener keys `timeout`, `on-timeout`, `on-resume`,
`ignore_inhibit`, `condition_cmd`, `condition_retry`; their documented types/defaults;
that the lock trigger vocabulary is dbus lock/unlock and prepare/post-prepare-sleep; and
that `inhibit_sleep` has a four-value ladder whose `3` waits for a session lock.

**Cannot** — the page is unversioned "Latest git". It supports no claim that the host's
installed `hypridle` accepts `unlock_cmd`, `on_lock_cmd`, `on_unlock_cmd`,
`condition_cmd` or `condition_retry`; no claim that a listener fired, that a lock
occurred, that sleep was inhibited, or that `inhibit_sleep = 3` took effect; and no claim
about the actual timing of any real lock. Documentary reading only — never observed
behaviour.

## Documentary cross-check — host config bytes (read-only, file bytes only)

`~/.config/hypr/hypridle.conf`, `sha256 e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41`,
19 lines (digest prefix matches the lane's recorded 16-hex value at
`corpus/knowledge/waybar-walker-plane.md:22`):

| Line | Bytes as read |
|---|---|
| 1 | `general {` |
| 2 | `lock_cmd = omarchy-system-lock` |
| 3 | `before_sleep_cmd = OMARCHY_LOCK_ONLY=true omarchy-system-lock` |
| 4 | `after_sleep_cmd = sleep 1 && omarchy-system-wake` |
| 5 | `inhibit_sleep = 3` |
| 10–11 | listener `timeout = 150`, `on-timeout = pidof hyprlock \|\| omarchy-launch-screensaver` |
| 16–18 | listener `timeout = 152`, `on-timeout = omarchy-system-lock`, `on-resume = omarchy-system-wake` |

So the host file exercises exactly `lock_cmd`, `before_sleep_cmd`, `after_sleep_cmd`,
`inhibit_sleep` (and `timeout`/`on-timeout`/`on-resume`). It sets **none** of
`unlock_cmd`, `on_lock_cmd`, `on_unlock_cmd`, `ignore_dbus_inhibit`,
`ignore_systemd_inhibit`, `ignore_wayland_inhibit`, `condition_cmd`, `condition_retry` —
all of which the page documents. Absence in the file is not evidence that the installed
binary rejects those keys, and the file's silence on the `ignore_*` keys does not prove
the documented `false` defaults are in force at runtime. A P6 note may record the
present/absent split as a config-byte observation; it may not read it as support or
non-support.

## Verification performed

Every quoted string above was checked programmatically against the fetched bytes: HTML
tags stripped, `<br>`→space, curly quotes/apostrophes normalized, whitespace collapsed,
then substring search. First pass 27/28; the one miss was my own draft spacing guess for
the `inhibit_sleep` cell (the cell is `<br>`-separated), not page text. Re-reading the exact
rendered cell form passed; a second batch passed 10/10, and the replacement
`condition_retry` fragments passed 3/3. Every quote retained in this report is ≤25 words.

## Findings for L1

1. **Candidate SOURCES row (id unassigned; paste shape only).** Column order taken from
   `corpus/SOURCES.md:9`:

   ```text
   | S0xx-pending | Hypridle wiki — https://wiki.hypr.land/Hypr-Ecosystem/hypridle/ | docs | A | current-wiki hypridle general options, listener contract, dbus/loginctl lock vocabulary, inhibit_sleep ladder | `#general`, `#listeners`, `#conditional-timeouts`, `#examples`, `#recipes`; page marked Latest git, modified 2026-08-26; opened 2026-10-20 (raw HTML sha256 b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640, 254750 bytes) | documents lock/unlock/prepare_sleep dbus triggers, before/after sleep hooks, three inhibitor-ignore scopes and the 0–3 inhibit_sleep ladder; unversioned, so it teaches host-agnostic option names, never host support or observed behaviour | mined | 2026-10-20 | 90d | corpus/knowledge/<p6-note>.md |
   ```

   `status: mined` is correct only once the P6 note exists and cites this row; otherwise
   use `queued`. `used-by` must name the note path exactly — the coverage rule matches it.

2. **P6 note seed (must satisfy rubric V within the first 15 lines).** Suggested header,
   mirroring `waybar-observation-boundaries-r16.md:1-4` plus the new surface key:

   ```text
   source: S0xx https://wiki.hypr.land/Hypr-Ecosystem/hypridle/ (#general, #listeners, #conditional-timeouts, #examples, #recipes)
   verified-at: 2026-10-20; current-wiki Latest git, page modified 2026-08-26; raw HTML sha256 b45c03dc…, 254750 bytes; file-bytes config read of ~/.config/hypr/hypridle.conf (sha256 e7d3b8dd…)
   recheck: Re-fetch the wiki URL, compare the recorded digest and the #general table rows, re-read the config file bytes; no package query, unit or compositor operation
   covers: — (documentary route; no U-axis claim)
   surface: P6
   ```

3. **C2 wording caution.** The P6 entry must be labelled "current-wiki Latest git
   (modified 2026-08-26)" and must not imply installed-binary support for `unlock_cmd`,
   `on_lock_cmd`, `on_unlock_cmd`, `condition_cmd`, `condition_retry`. If the round wants
   a stronger route, the missing piece is a version-pinned hypridle source/tag — that is
   the `SrcHypridleTag`/`SrcHypridleSrc` seats' ground, not this page's.

4. **Provenance gap retained.** Upstream markdown is unreachable (2× 404) and the GitHub
   API is rate-limited (403), so this report carries an HTML-bytes digest only, with no
   commit pin. If L1 needs a commit anchor, it must come from an authenticated path or a
   different mirror; this report does not fabricate one.

5. **No tools installed or updated**, so there is nothing to record against the tooling
   directive. The pacman channel was not touched at all — not even a read-only query.
