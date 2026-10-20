# AttackP6General — § Upstream contract, "General keys (hypridle)" bullets, re-anchored against the tag bytes

Seat `MadoR17.AttackP6General`, reviewer, leaf (no subagent dispatch). Lane
`mado-shokunin` @ `988b858bd6049bc709807534fd725c05264f7e60` (read only). Assignment:
attack `corpus/knowledge/idle-lock-route-r17.md` § Upstream contract → "General keys
(hypridle)" against the tagged `Hypridle.cpp` / README / wiki bytes; every
`[HC:n]` / `[HW:n]` / `[HR:n]` anchor must hold; report each wrong anchor or over-read.

**Result: the section largely survives. 28 of 30 citations hold exactly; one quotation is
attributed to a source that does not contain it (F1); one range excludes the condition it
asserts (F2).** Three smaller wording/coverage defects (F3–F5) and one adjacent over-read in
the same claim chain (F6, lands in § Unexercised, not in these bullets) are listed below with
anchors. No factual inversion of a General key was found: every semantic claim about
`lock_cmd`, `unlock_cmd`, `on_lock_cmd`/`on_unlock_cmd`, `before_sleep_cmd`/`after_sleep_cmd`,
`ignore_dbus_inhibit`, `ignore_systemd_inhibit`, `ignore_wayland_inhibit` and `inhibit_sleep`
reproduces from the v0.1.8 bytes. Installs: **none**.

## 1. Fetch and digest identity

Fetched with `curl` (raw bytes). The `HC`/`HR` rows are tag-pinned (`v0.1.8`); the `HW` row
is the live "Latest git" page, and the bytes I received hash to the same digest the note and
SOURCES record, so they are the copy the note read. Every URL below answered HTTP 200
(checked with `curl -o /dev/null -w '%{http_code}'`), so the raw paths are real tag paths, not
branch fallbacks.

| key | URL | lines | bytes | sha256 (fetched) |
|---|---|---|---|---|
| HC | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp | 735 | 29880 | `2dd4d73d4f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75` |
| HR | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md | 76 | 2598 | `f5b852eefe3c6d21ede9cef8b9b2dbf55d2e9423f1224b82592aa1b4759781f6` |
| HW | https://wiki.hypr.land/Hypr-Ecosystem/hypridle/ | 623 (HTML) | 254750 | `b45c03dccab0e7a85bf99d8baa3572a1898f66bb37a030d09b4427a51c83f640` |

Cross-checks fetched but **not** declared sources of this note (used only to test claims the
bullets imply, see F5/F6): `src/core/Hypridle.hpp`
`f9e4e5587075fe34ae3279c4225b00661c686468035c4ad6cbe71e098fc0a2b8`, `src/main.cpp`
`379bf321a53edc56bde5f81fe070a2519a53bf17ca3b89937c1a027bad672a38`,
`src/config/ConfigManager.cpp` `396f1f99ad0795f37d6e63f717eea9c8d67f776f7ce02333c3fca2a699f2cb11`.

Three-way identity for the three declared sources:

| source | fetched | `corpus/SOURCES.md` | `corpus/lessons/round-17.md` § Gate |
|---|---|---|---|
| S063 / HW | `b45c03…f640` | `b45c03…f640` (line 75) | `b45c03…f640` (line 50) |
| S065 / HR | `f5b852…81f6` | `f5b852…81f6` (line 77) | `f5b852…81f6` (line 52) |
| S066 / HC | `2dd4d7…2d75` | `2dd4d7…2d75` (line 78) | `2dd4d7…2d75` (line 53) |

`ALL-THREE-IDENTICAL` for each. The wiki page's `<time datetime=2026-08-26T14:50:40.000Z>`
matches the note's "page modified 2026-08-26"; the article's last line is `Last updated on
August 26, 2026`.

## 2. `[HW:n]` reconstruction — reproducible, and it is the author's

The note defines `[HW:n]` as line *n* of the tag-stripped `<article>` text, "one line per
block (table cells run together in the text)". I rebuilt it independently and got the same
addressing the note uses, so the anchor numbers are not a private convention:

```python
src = open('wiki-hypridle.html', encoding='utf-8').read()
art = src[src.index('<article'):src.index('</article>')]
t = re.sub(r'</(?:h1|h2|h3|h4|p|li|tr|pre|div|table|ul|ol|blockquote|section|main|header|footer|figure)>', '\n', art)
t = re.sub(r'<br\s*/?>', '\n', t); t = re.sub(r'<[^>]+>', '', t); t = html.unescape(t)
HW = [l.strip() for l in t.split('\n') if l.strip()]   # 121 lines
```

Result: 121 blocks; lines 1–3 page header/H1, line 6 the config path, line 13 `lock_cmd`,
line 33 the `inhibit_sleep = 3` sentence, line 120 last-updated, line 121 the footer nav
(`hyprlauncherhyprlock`). That is exactly the note's and SOURCES S063's "lines 6-120".
Had the author broken on `<td>` as well, all ten `[HW:n]` citations below would shift and fail;
they do not, so this reconstruction is the note's.

## 3. Mechanical anchor verification (all 30 citations in the section)

Every citation in the section was extracted and its cited lines printed from the fetched
bytes. Verdicts: `HOLD` = the text the sentence asserts is present at the cited line(s);
`CAVEAT` = anchor present but does not carry the stated qualification; `FAIL` = text absent.

| # | anchor | claim in the note | bytes at the anchor | verdict |
|---|---|---|---|---|
| 1 | [HC:473] | `if (MEMBER == "Lock") {` | identical, char-exact | HOLD |
| 2 | [HC:477-478] | `spawn(*LOCKCMD)` if non-empty | 477 log, 478 `spawn(*LOCKCMD);`; the `if (!…empty())` is **476** | CAVEAT (F2) |
| 3 | [HW:13] | "command to run when receiving a dbus lock event (e.g. loginctl lock-session)" | `lock_cmd` + that description + `string` + `empty` | HOLD |
| 4 | [HR:16] | "dbus/sysd lock command (loginctl lock-session)" | `lock_cmd = notify-send "lock!"  # dbus/sysd lock command (loginctl lock-session)` | HOLD |
| 5 | [HC:480-485] | `Unlock` branch, same pattern | 480 `} else if (MEMBER == "Unlock") {` … 485 `spawn(*UNLOCKCMD);` | HOLD |
| 6 | [HW:14] | documented `unlock_cmd` | `unlock_cmd` + "dbus unlock event (e.g. loginctl unlock-session)" | HOLD |
| 7 | [HC:402] | `onLocked` reads `general:on_lock_cmd` | identical | HOLD |
| 8 | [HC:404] | spawns it | `spawn(*LOCKCMD);` | HOLD |
| 9 | [HC:433] | `onUnlocked` reads `general:on_unlock_cmd` | identical | HOLD |
| 10 | [HC:104-107] | warning text (two fragments) | 104 `if (!m_sWaylandState.lockNotifier)`; 106–107 carry both fragments verbatim | HOLD |
| 11 | [HW:15-16] | documented `on_lock_cmd` / `on_unlock_cmd` | rows present, descriptions match | HOLD |
| 12 | [HC:493] | `handleDbusSleep` matches `PrepareForSleep` | `if (MEMBER != "PrepareForSleep")` | HOLD |
| 13 | [HC:504] | `cmd = toSleep ? before : after` | `std::string cmd = toSleep ? *SLEEPCMD : *AFTERSLEEPCMD;` | HOLD, but see F3 |
| 14 | [HC:509-510] | spawned if non-empty | `if (!cmd.empty())` / `spawn(cmd);` | HOLD |
| 15 | [HW:17-18] | documented before/after sleep | rows present ("dbus prepare_sleep" / "post prepare_sleep") | HOLD |
| 16 | [HC:600] | `ignore_dbus_inhibit` read in `setupDBUS` | inside `setupDBUS` (opens 599), identical key string | HOLD |
| 17 | [HC:626] | block registering `org.freedesktop.ScreenSaver` when false | `if (!*IGNOREDBUSINHIBIT) {` + comment + `ServiceName{"org.freedesktop.ScreenSaver"}` (634) | HOLD |
| 18 | [HR:20] | README inhibit description | exact comment text | HOLD |
| 19 | [HW:19] | documented `ignore_dbus_inhibit` | row present, default `false` | HOLD |
| 20 | [HC:601] | `ignore_systemd_inhibit` read | identical | HOLD |
| 21 | [HC:617] | gated | `if (!*IGNORESYSTEMDINHIBIT) {` | HOLD |
| 22 | [HW:20] | documented | row present, default `false` | HOLD |
| 23 | [HC:58] | `ignore_wayland_inhibit` read | identical (inside `run()`, opens 24) | HOLD (F5) |
| 24 | [HC:74] | selection when true or per-listener `ignore_inhibit` | `if (*IGNOREWAYLANDINHIBIT \|\| r.ignoreInhibit)` | HOLD, wording F4 |
| 25 | [HW:21] | documented | row present, default `false` | HOLD |
| 26 | [HW:22-26] | modes 0 disable / 1 normal / 2 auto / 3 **"wait until locked"** | 23–25 `0: disable`, `1: normal`, `2: auto`; 26 `3: lock notifyint2` | **FAIL** (F1) |
| 27 | [HC:120] | case 2 "auto" | `case 2: { // auto (enable, but wait until locked if before_sleep_cmd contains hyprlock, or …)` | HOLD |
| 28 | [HC:128-129] | case 3 waits only `if (m_sWaylandState.lockNotifier)` | 128 `case 3: // wait until locked`; 129 `if (m_sWaylandState.lockNotifier)` | HOLD (F6) |
| 29 | [HW:33] | "3 makes your system wait until the session gets locked by a lock screen app." | exact substring; sentence continues "This works with all wayland session-lock apps." | HOLD |
| 30 | [HW:26] | default `inhibit_sleep` = 2 | `3: lock notify` + `int` + `2` (description/type/default cells run together) | HOLD |

Positive controls that also passed (claims without an explicit `[HC:n]`, checked because they
are load-bearing): `onLocked`/`onUnlocked` have exactly two call sites, the `setLocked` /
`setUnlocked` callbacks of `CCHyprlandLockNotificationV1` (HC:91–92) — so "fired from the
Wayland session-lock notification, not dbus" holds; the notification is constructed only when
the `hyprland_lock_notifier_v1_interface.name` global was bound (HC:34–36, 89–93); `spawn` is
`/bin/sh -c` (HC:286–296); the tag's own defaults are `ignore_dbus_inhibit = 0`,
`ignore_systemd_inhibit = 0`, `ignore_wayland_inhibit = 0`, `inhibit_sleep = 2`
(ConfigManager.cpp:72–75), so the two "(default)" parentheticals and "Default
`inhibit_sleep` = 2" are true even though the note cites only the wiki for them.

## 4. Findings

### F1 — FAIL (only true anchor violation): the mode-3 quotation is not in the cited source

Note text (line 9 of the section):

> **inhibit_sleep** — modes 0 disable / 1 normal / 2 auto / 3 "wait until locked" [HW:22-26].

The string `wait until locked` occurs **nowhere in the fetched wiki article** (0 hits over all
121 reconstructed lines). [HW:22-26] says `3: lock notify` (HW:26). The quoted phrase is the
**source comment** at `Hypridle.cpp:128` (`case 3: // wait until locked`), and the wiki's prose
equivalent is [HW:33] ("3 makes your system wait until the session gets locked by a lock screen
app."), cited in the very next sentence. So this is a quote moved one source left: `[HW:22-26]` should read
`"lock notify"`, with the "wait until locked" phrasing attributed to `[HC:128]`, or the quotation
marks dropped from the HW-attributed mode list. Substance is unaffected (mode 3 does wait until
locked, [HW:33] + HC:128–131); this is a citation defect, not a claim reversal.

### F2 — CAVEAT: `[HC:477-478]` does not exhibit the "if non-empty" it asserts

> then `spawn(*LOCKCMD)` if non-empty [HC:477-478]

HC:476 is `if (!std::string{*LOCKCMD}.empty()) {`, HC:477 the log line, HC:478 the spawn. The
cited range starts one line too late for the qualification. Cite `[HC:476-478]`. The sibling
`unlock_cmd` citation `[HC:480-485]` does include its test (HC:483), so the two bullets are
internally inconsistent on the same construct.

### F3 — NIT: code-shaped fragment is a paraphrase, not the line

> `cmd = toSleep ? before : after` [HC:504]

HC:504 is `std::string cmd = toSleep ? *SLEEPCMD : *AFTERSLEEPCMD;`. The note's other
backticked fragments in this section are byte-exact (`if (MEMBER == "Lock") {`,
`spawn(*LOCKCMD)`, `if (m_sWaylandState.lockNotifier)`), so this one reads as a quotation and
is not. Either quote the line or mark it as a schematic.

### F4 — LOW: "the inhibit-aware idle notification" inverts the wiki's own term

> selects the inhibit-aware idle notification when true or when the listener sets `ignore_inhibit` [HC:74]

When the condition is true the code calls `sendGetInputIdleNotification` (HC:76); when false,
`sendGetIdleNotification` (HC:79). The wiki uses "inhibit-awareness" for *honouring* inhibitors
and says setting `general:ignore_wayland_inhibit` "would disable inhibit-awareness for every
listener" ([HW:118-119]). Applied to the `ignore_wayland_inhibit = true` branch, "inhibit-aware"
therefore reads backwards. Suggested wording: "selects the input-idle (inhibitor-ignoring)
notification when true or when the listener sets `ignore_inhibit`". Anchor is correct; the
label is the defect.

### F5 — INFO: `ignore_wayland_inhibit` is read (and the selection re-applied) twice

HC:58 is the startup read cited. The same value is read again at HC:372 and the
input-idle/idle choice is rebuilt for every listener at HC:381–386 when the inhibit count drops
to zero while idled. Not false as written ("read at [HC:58]"), but a reader modelling the
host's `ignore_inhibit` behaviour from this bullet would miss the re-registration path. Worth a
half-clause if the note is ever extended.

### F6 — adjacent over-read (lands in § Unexercised, same claim chain): "the protocol decides whether 3 waits" is not entailed

The bullet's sentence is literally true: `case 3` assigns `SLEEP_INHIBIT_LOCK_NOTIFY` only
inside `if (m_sWaylandState.lockNotifier)` (HC:128–131). But there is no defined else:

- the member is an uninitialized anonymous enum — `enum { SLEEP_INHIBIT_NONE,
  SLEEP_INHIBIT_NORMAL, SLEEP_INHIBIT_LOCK_NOTIFY } m_inhibitSleepBehavior;`
  (Hypridle.hpp:67–71), no `= …`;
- `CHypridle` has a user-provided default constructor (Hypridle.cpp:16), so
  `std::make_unique<CHypridle>()` (main.cpp:71) value-initializes **without** zero-initializing
  members; the value is indeterminate (reading it is undefined behaviour);
- `run()` then calls `inhibitSleep()` whenever that value is not `SLEEP_INHIBIT_NONE`
  (HC:142–143) and `handleInhibitOnDbusSleep` branches on the same value (HC:671–681).

Consequence for the note's § Unexercised line — "Whether the compositor exposes
`hyprland-lock-notify-v1` on this host. This decides whether `inhibit_sleep = 3` waits" — the
protocol's absence does **not** decide what happens; it leaves the mode unwritten. In the
`LOCK_NOTIFY` outcome the startup call would take a logind `delay` inhibitor that nothing ever
releases (no notifier ⇒ `onLocked` never runs), i.e. the opposite of "will not work"; in the
`NORMAL` outcome sleep handling would still work; in `NONE` it would be off. The warning at
[HC:104-107] is the program's own claim, not an established postcondition. This does not
falsify any anchor in the General keys bullets; it says the note should either state the
unassigned else or downgrade "decides whether … waits" to "selects the wait-until-locked mode
only if". If this seat's scope is held to the bullets, treat F6 as a note for the
Unexercised/ownership seat.

### Observation, not a defect — the [HW:33] quote stops before the wiki's broader claim

The quoted first sentence is exact. The omitted continuation is "This works with all wayland
session-lock apps." The v0.1.8 source can neither confirm nor deny it: it depends on the
Hyprland-specific `hyprland-lock-notify-v1` (HC:34–36, 89–93), not on a generic session-lock
signal, so the wiki sentence is about lock-screen apps on Hyprland rather than portability.
No action required for anchor correctness; noting it because the sentence sits one line from
the [HC:104-107] warning and a reader may take it as the source-backed scope.

## 5. What the attack failed to break

- Every semantic claim in the seven General-keys bullets reproduces: dbus `Lock`/`Unlock`
  member names and non-empty spawn, on-lock/on-unlock from the Wayland lock notification only,
  `PrepareForSleep` before/after selection, `ignore_dbus_inhibit` gating the ScreenSaver
  registration, `ignore_systemd_inhibit` gating the BlockInhibited path, `ignore_wayland_inhibit`
  selecting the input-idle notification, and `inhibit_sleep` cases 0/1/2/3 including the
  lock-notify precondition.
- Both README anchors ([HR:16], [HR:20]) are char-exact against the v0.1.8 file.
- All three source digests match SOURCES and the lesson gate; the wiki "modified"
  date matches; the tag-pinned URLs serve HTTP 200 from `raw.githubusercontent.com`
  (no branch fallback: the note's own tag, `v0.1.8`, is the path component).
- No install, no package query, no live probe was run; the host was not touched.

## 6. Residual risk and verification gaps

- **Tag vs master.** The wiki is "Latest git" (2026-08-26); the code is v0.1.8. The note says
  this and only claims agreement on `condition_cmd`. My check cannot bound wiki drift beyond
  the keys cited here. A `master`-vs-`v0.1.8` diff of `Hypridle.cpp` was not run (would need a
  second fetch set); the note's "not version-pinned" caveat stands.
- **Config defaults are documentary in the note.** `HW:19-21` default column and `HW:26` say
  false/false/false/2; I confirmed those against `ConfigManager.cpp:72-75`, which is **not** a
  declared source for the note. If the note wants the default asserted from code, that row
  needs adding; today the parentheticals rest on the wiki.
- **`get_idle_notification` vs `get_input_idle_notification` semantics** are taken from the
  wrapper names plus the wiki's own use of "inhibit-awareness" ([HW:115-119]); the
  `ext-idle-notify-v1` XML was not fetched for this seat. F4's suggested rewording does not
  depend on the XML, only on which branch the code calls.
- F6's practical effect depends on compiler/layout luck (indeterminate value), so no runtime
  outcome is claimed — only that the note's "decides whether" is stronger than the source.

## 7. Commands run

```
curl -sS -o … https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp
curl -sS -o … https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md
curl -sS -o … https://wiki.hypr.land/Hypr-Ecosystem/hypridle/
curl -sS -o … https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.hpp
curl -sS -o … https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/main.cpp
curl -sS -o … https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/config/ConfigManager.cpp
python3  (article reconstruction + per-citation dump, §2/§3 above; no lane file written)
sha256sum on the fetched files
```

No lane file was modified. No git mutation. Installs: none.
