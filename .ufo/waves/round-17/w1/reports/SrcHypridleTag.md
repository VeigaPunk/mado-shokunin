# SrcHypridleTag — hypridle latest release, tag-pinned README and example config

Seat: `MadoR17.SrcHypridleTag` (scout, leaf, no dispatch). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, baseline `27cd06f`, pre-registration `0175f13`.
Access date for every URL below: **2026-10-20**. Report only; no lane file was edited
outside this report. No tool was installed or upgraded; all work was `curl` + `read` +
`tar -O` into `/tmp` scratch. No package, service, compositor or device command was run
(no sudo/pacman/systemctl/hyprctl), per the host pause.

Assignment: find the latest hypridle release tag, fetch the tag-pinned raw `README.md`
and the example/assets config at that tag, and record tag, commit, raw SHA-256, line
anchors and ≤25-word quotes. This is documentary material for the round-17 P6
(idle/lock) route note only — never observed host behaviour.

## 1. Latest release identification

| Fact | Observation | How observed |
|---|---|---|
| Latest release tag | `v0.1.8` | releases atom feed first `<entry>`; `git ls-remote --tags` max tag |
| Release timestamp | `2026-07-26T14:45:24Z` | atom `<updated>`; release page `<relative-time datetime="2026-07-26T14:45:24Z">` |
| Previous release | `v0.1.7`, `2025-08-27T10:40:30Z` | atom `<entry>` 2 |
| Tag → commit | `e5c01af0842bd66617f7004568df9406111d6e80` | release page links `/hyprwm/hypridle/commit/e5c01af0842bd66617f7004568df9406111d6e80`; `git ls-remote` `refs/tags/v0.1.8` = same OID |
| Tag kind | lightweight (no `^{}` peeled ref returned for `refs/tags/v0.1.8^{}`) | `git ls-remote` |
| Default branch | `main` → `aa958ed7ad4863860b93ecd7189419e193bfae2c` | `git ls-remote --symref` |
| Tag vs main | differs; release page carries `compare/v0.1.8...main` | release page HTML |

Release body (atom `<content>`, whitespace-normalised; 7 items):

```text
A small update as usual.
Changes
core: fix dbus inhibit lock counting by @slowsage in #175
nix: remove sdbus-cpp overlay by @PointerDilemma in #182
core: don't skip on-resume when on-timeout already fired by @spheenik in #192
fix: allow hypridle -c to run without default conf by @thursdaddy in #191
config: update dpms commands to lua syntax by @davc0n in #205
core: implement GetActive and ActiveChanged on dbus service by @caguiclajmg in #207
core: add per-listener condition_cmd with retry by @spheenik in #193
Full Changelog : v0.1.7...v0.1.8
```

Note for recheck policy: `v0.1.8` is newer than any hypridle tag cited in the corpus so far;
any earlier-tag hypridle claim is stale against this row.

## 2. Tag-pinned artifacts fetched

Raw URLs are tag-pinned (`/v0.1.8/`), so they cannot drift to a later commit.

| Artifact | URL | bytes | lines | raw SHA-256 |
|---|---|---|---|---|
| README | `https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md` | 2598 | 76 | `f5b852eefe3c6d21ede9cef8b9b2dbf55d2e9423f1224b82592aa1b4759781f6` |
| Example config | `https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/assets/example.conf` | 1665 | 37 | `ef385d88e8c99820ed910eadd62cd14c16bc948317d4f78e93453e24c70d13d1` |
| Tag tarball | `https://codeload.github.com/hyprwm/hypridle/tar.gz/refs/tags/v0.1.8` | 19972 | — | `08703613cc33cc796c2179bcaa6076e8618113f67b938daaf7535f90c7d39595` |
| `VERSION` | in tarball | — | 1 | content `0.1.8` |
| `CMakeLists.txt` | in tarball | 3568 | — | `84c0fd3ce2b2a19c8f22471d2931fd394b7c9dc889b4b34d37a7f11e92919aeb` |
| `src/config/ConfigManager.cpp` | in tarball | 7613 | — | `396f1f99ad0795f37d6e63f717eea9c8d67f776f7ce02333c3fca2a699f2cb11` |
| Releases atom feed | `https://github.com/hyprwm/hypridle/releases.atom` | 67676 | — | `affa06f7f36dae57e168929f97642d489ec14d935b1879a528bb12f53f58c827` |
| Release page HTML | `https://github.com/hyprwm/hypridle/releases/tag/v0.1.8` | 203035 | — | `0f59aa137c3a7b2bda9c484f00e8bca7298428f083838df427df93cfff86eaa8` |

Byte-identity cross-check (raw vs tarball, `tar xzf … -O … | sha256sum`):
README `f5b852ee…` = tarball copy; `assets/example.conf` `ef385d88…` = tarball copy. Both
match, so the raw bytes are the tag's bytes, not a rendered or post-edited view.

The GitHub REST API (`/repos/hyprwm/hypridle/releases`, `/tags`) returned HTTP 200 with
`{"message":"API rate limit exceeded …"}` for this host IP; it was not used as evidence.
Tag identification therefore rests on the atom feed + `git ls-remote` + the release page
HTML, which agree.

## 3. README.md anchors and quotes (tag v0.1.8, commit `e5c01af…`)

| Lines | Content | Verbatim quote (≤25 words) |
|---|---|---|
| 1-2 | Name/purpose | `Hyprland's idle daemon` (4 words) |
| 5 | Protocol basis | `based on the ext-idle-notify-v1 wayland protocol` (6 words) |
| 6-7 | dbus surfaces | loginctl lock/unlock/before-sleep; dbus inhibit used by firefox/steam |
| 11-12 | Config path | `Configuration is done via ~/.config/hypr/hypridle.conf in the standard hyprland syntax.` (10 words) |
| 14-22 | `general {}` example | lock_cmd, unlock_cmd, before_sleep_cmd, after_sleep_cmd, ignore_dbus_inhibit, ignore_systemd_inhibit |
| 24-30 | `listener {}` example | timeout, on-timeout, on-resume, condition_cmd, condition_retry |
| 28-29 | Condition gate semantics | `if set, run this command before on-timeout. Exit 0 = proceed, non-zero = defer` (14 words) |
| 33-35 | Listener multiplicity | `You can add as many listeners as you please.` then: omitting on-timeout/on-resume makes those events ignored (full sentence 22 words) |
| 57-63 | Launch route (compositor) | `exec-once = hypridle` (3 words, fenced `hyprlang`) |
| 64-67 | Launch route (systemd) | `systemctl --user enable --now hypridle.service` (4 words) |
| 69-76 | CLI flags | `-c/--config` defaults to `${XDG_CONFIG_HOME}/hypr/hypridle.conf`; `-q`, `-v` |

Quote discipline note: backticks in the source were removed above only where the markdown
would otherwise nest; no word was changed. For exact-byte quoting cite the raw file line,
not this table.

## 4. assets/example.conf anchors and quotes (tag v0.1.8)

This is the only config file in the tag tarball besides README's inline block
(`tar tzf` shows `assets/example.conf`; no `hypridle.conf` at root, no `example/` dir —
root `hypridle.conf`, `example/hypridle.conf`, `assets/hypridle.conf` all returned HTTP 404
from raw).

| Lines | Content | Verbatim quote (≤25 words) |
|---|---|---|
| 1-2 | Provenance | `# sample hypridle.conf` / points to `wiki.hyprland.org/Hypr-Ecosystem/hypridle` |
| 4-8 | `general` block | `lock_cmd = pidof hyprlock \|\| hyprlock` (13 words incl. comment) |
| 6 | Pre-suspend lock | `before_sleep_cmd = loginctl lock-session` (5 words) |
| 7 | Post-resume dpms | `after_sleep_cmd = hyprctl dispatch 'hl.dsp.dpms({action = "on"})'` (8 words) |
| 10-14 | Backlight listener, 150 s | `brightnessctl -s set 10` on timeout, `brightnessctl -r` on resume |
| 17-21 | Keyboard-backlight listener, 150 s | `brightnessctl -sd rgb:kbd_backlight set 0` |
| 23-26 | Lock listener, 300 s | `on-timeout = loginctl lock-session` (5 words) |
| 28-32 | Screen-off listener, 330 s | `on-timeout = hyprctl dispatch 'hl.dsp.dpms({action = "off"})'` (8 words) |
| 34-37 | Suspend listener, 1800 s | `on-timeout = systemctl suspend` (4 words) |

Observed shape: the sample routes *lock* through `loginctl lock-session` (line 25), and
mentions `hyprlock` only as an idempotence guard inside `lock_cmd` (line 5); dpms on/off
uses the `hl.dsp.dpms({…})` string form that release note #205 calls "lua syntax".

## 5. Secondary tag evidence that fixes the documentary chain

`CMakeLists.txt` (tag `e5c01af…`):

- `:94` `protocolnew("staging/ext-idle-notify" "ext-idle-notify-v1" false)`
- `:95` `protocolnew("${HYPRLAND_PROTOCOLS}/protocols" "hyprland-lock-notify-v1" true)`
- `:98` `install(TARGETS hypridle)`
- `:99-100` systemd unit installed to `lib/systemd/user`
- `:102-105` the sample config is installed:

```text
install(
  FILES ${CMAKE_SOURCE_DIR}/assets/example.conf
  DESTINATION ${CMAKE_INSTALL_FULL_DATAROOTDIR}/hypr
  RENAME hypridle.conf)
```

`systemd/hypridle.service.in`:

```text
:5  After=graphical-session.target
:6  ConditionEnvironment=WAYLAND_DISPLAY
:10 ExecStart=@CMAKE_INSTALL_PREFIX@/bin/hypridle
:11 Restart=on-failure
:14 WantedBy=graphical-session.target
```

`src/config/ConfigManager.cpp` (registered keys, exact lines):

- `:58` `addSpecialCategory("listener", … .anonymousKeyBased = true)`
- `:59-64` listener keys `timeout`, `on-timeout`, `on-resume`, `ignore_inhibit`,
  `condition_cmd`, `condition_retry`
- `:66-75` general keys `lock_cmd`, `unlock_cmd`, `on_lock_cmd`, `on_unlock_cmd`,
  `before_sleep_cmd`, `after_sleep_cmd`, `ignore_dbus_inhibit`,
  `ignore_systemd_inhibit`, `ignore_wayland_inhibit`, `inhibit_sleep`
- `:107-115` values read back with `getSpecialConfigValue("listener", …)`

Observed asymmetry: the README example block (`:14-22`) names **6** general keys while
this tag registers **10** — `on_lock_cmd`, `on_unlock_cmd`, `ignore_wayland_inhibit` and
`inhibit_sleep` are code-registered but absent from the README example. A P6 note citing
the README must not present its key list as exhaustive.

## 6. Observed facts / inference / unresolved

**Observed (reproducible from this report):** latest release `v0.1.8` at
`2026-07-26T14:45:24Z`, lightweight tag on commit `e5c01af0842bd66617f7004568df9406111d6e80`;
the two raw digests in §2, each equal to its tarball copy; every line anchor and quote
above; the install rule that renames `assets/example.conf` to `hypridle.conf` under
`${DATAROOTDIR}/hypr`; the 10 registered general keys and 6 listener keys; the seven
release-note changes.

**[INFERENCE]** The sample's `hl.dsp.dpms({…})` strings assume a Hyprland generation whose
dispatch parser accepts that lua-style form (release note #205 is titled "update dpms
commands to lua syntax"). That is a statement about the sample's intended companion
version, not about any host.

**[UNK]** Host installed hypridle version, host `~/.config/hypr/hypridle.conf` contents,
whether a hypridle process or user unit is present, and whether idle→lock actually fires.
All are unobservable here: package queries are paused and live probes are barred. This
seat did not read any host config file under `~/.config`; the assignment was the tag only.
Tag source also never proves the packaged binary — the tarball is one commit (`e5c01af…`),
and `main` had already moved to `aa958ed…` when read.

## 7. What the P6 route note may and may not claim (documentary only)

A P6 knowledge entry may state, with the anchors of §3-§5:

1. hypridle's README declares its configuration at `~/.config/hypr/hypridle.conf`
   (README:11-12) with a `-c/--config` override (README:71-73).
2. The tag ships one sample config, installed as `<datadir>/hypr/hypridle.conf`
   (CMakeLists:102-105), which pairs a 300 s listener with `loginctl lock-session`
   (example.conf:23-26), a 150/330 s backlight/dpms ladder (example.conf:10-14,28-32),
   and a 1800 s `systemctl suspend` (example.conf:34-37), with `hyprlock` named only as
   the `lock_cmd` guard (example.conf:5).
3. Per-listener gating exists: `condition_cmd` with `condition_retry`
   (README:28-29; ConfigManager.cpp:63-64; release note #193).
4. The shipped unit runs the binary as a `graphical-session.target` user unit
   (hypridle.service.in:5,10,14), and README offers `exec-once = hypridle` as the
   compositor route (README:57-63).

It may **not** claim: that the host has v0.1.8, that the host config resembles the sample,
that any listener fired, that a lock or suspend occurred, or that hypridle was running.
Those are behaviour claims needing a live observation this lane may not take. The note
should also say the sample's command strings are quoted as data and were not executed:
`hyprctl dispatch`, `loginctl lock-session` and `systemctl suspend` appear verbatim in it.

Prior-corpus constraint the note must respect (read this pass, not re-measured):
`corpus/knowledge/arc-synthesis.md:233` records hypridle/hyprlock/hyprsunset **absent**
in the then-current session with the 150 s/152 s chain having "no consumer", and
`corpus/knowledge/closeout-r11.md:47` plus `corpus/knowledge/config-health-report-r3.md:175-177`
repeat that absence (`pgrep -x` no match, user unit inactive/disabled, journal empty).
`corpus/knowledge/config-drift-r12.md:31` also lists `hypridle.conf`/`hyprlock.conf` as
present config files, so the corpus already distinguishes *config on disk* from *daemon
running*. A P6 documentary note therefore documents the configuration surface only and
must not imply presence; whether the absence still holds is `[UNK]` this round, since no
`pgrep`/`systemctl`/`journalctl` read is permitted. Grep of `corpus/SOURCES.md` for
`hypridle|hyprlock` returns nothing, so the §9 rows would be the corpus's first hypridle
sources — there is no earlier hypridle row to supersede.

## 8. Routed observations for L1 (not my gate)

1. **Spec gap for the C3 tripwire (declared class lists, §"Classes").** `systemctl` is
   enumerated only for `start|stop|restart|reload|try-restart|enable|disable|mask|unmask|
   kill|daemon-reload|isolate|set-property|edit|link|preset` (host_mutation) and
   `status|show|is-active|is-enabled|is-failed|list-units|list-unit-files|cat`
   (live_probe). `systemctl suspend` — exactly the command at example.conf:36 — plus
   `hibernate|hybrid-sleep|suspend-then-hibernate|poweroff|reboot|halt|kexec|rescue|
   emergency|default` match neither list, so a transcript containing them would yield no
   finding under the declared rules. `loginctl lock-session` (example.conf:25) *is* caught
   (loginctl is listed unconditionally) but only as `live_probe`, not host_mutation,
   although it acts on the session. `tools/mado-tripwire.py` does not exist yet
   (`ls tools/` → `mado-action-plan.py`, `mado-verify.sh`), so this is a spec-level
   observation, [INFERENCE] as to implementation.
2. **Recheck policy** for any row built from this: `on-release` (a v0.1.9
   would supersede it; `v0.1.8` already supersedes earlier-tag claims).
3. **Install-script caution:** README:54 tells readers to `sudo cmake --install build`.
   That is documented upstream text, not a lane instruction and not admissible as a route
   to run anything on this host during the pause.

## 9. Candidate SOURCES rows (ids pending — reserved block S056-S069 is L1's)

Drafted in `corpus/SOURCES.md` column order; `S0xx-pending` per lane convention.

```text
| S0xx-pending | Tagged hypridle README — https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md | docs | A | Declared idle-daemon config path, general/listener option names, condition gating and CLI override; not host version, config file or behaviour | tag v0.1.8, commit e5c01af0842bd66617f7004568df9406111d6e80; README:5,11-12,14-31,33-35,57-76; raw sha256 f5b852eefe3c6d21ede9cef8b9b2dbf55d2e9423f1224b82592aa1b4759781f6 | hypridle documents ~/.config/hypr/hypridle.conf with one listener block per timeout and optional condition_cmd gating; documentation cannot establish that a host runs it | mined | 2026-10-20 | on-release | corpus/knowledge/<P6 note>.md |
| S0xx-pending | Tagged hypridle shipped example config — https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/assets/example.conf | config | A | Shipped sample route from idle timeouts to lock/dpms/suspend command strings; not executed and not host-matching | tag v0.1.8; example.conf:5-7,10-14,23-32,34-37; raw sha256 ef385d88e8c99820ed910eadd62cd14c16bc948317d4f78e93453e24c70d13d1; installed as ${DATAROOTDIR}/hypr/hypridle.conf by CMakeLists.txt:102-105 | the sample expresses lock via loginctl lock-session with a hyprlock guard, screen power via hyprctl dispatch lua-syntax strings, suspend via systemctl; sample text is not behaviour | mined | 2026-10-20 | on-release | corpus/knowledge/<P6 note>.md |
```

Optional third row if L1 wants the key inventory anchored in code: `src/config/ConfigManager.cpp`
at `e5c01af…` (kind `code`, tier A, anchor `:58-64,66-75,107-115`, raw sha256
`396f1f99ad0795f37d6e63f717eea9c8d67f776f7ce02333c3fca2a699f2cb11`), teaches that the tag
registers 10 general keys while the README example shows 6.

## 10. Reproduction (all read-only; /tmp scratch)

```sh
cd /tmp
curl -sS https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/README.md -o r.md
curl -sS https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/assets/example.conf -o e.conf
curl -sSL https://codeload.github.com/hyprwm/hypridle/tar.gz/refs/tags/v0.1.8 -o t.tgz
sha256sum r.md e.conf t.tgz
tar xzf t.tgz -O hypridle-0.1.8/README.md | sha256sum          # f5b852ee…  (matches r.md)
tar xzf t.tgz -O hypridle-0.1.8/assets/example.conf | sha256sum # ef385d88…  (matches e.conf)
curl -sS https://github.com/hyprwm/hypridle/releases.atom | sha256sum  # affa06f7…
GIT_TERMINAL_PROMPT=0 git ls-remote https://github.com/hyprwm/hypridle 'refs/tags/v0.1.8'
```

Expected: the two tag refs above, and digests identical to §2. No network fetch in this
report is a live probe; every command reads remote file bytes only.

## 11. Tooling

None installed, none upgraded, no channel touched. `curl`, `git ls-remote`, `tar`,
`sha256sum`, `python3 -I` and `read` were already present; all outputs went to `/tmp`.

## Gaps this seat leaves to others

- hyprlock's own tag/README/example (sibling `SrcHyprlockTag`) — the P6 route needs a
  second, independently anchored documentary leg for the lock client; this report supplies
  only the hypridle side plus the `hyprlock` guard reference at example.conf:5.
- Host-side reality (`[UNK]` by design): installed version, config contents, running unit,
  observed idle→lock. Not evidence this round may produce.
