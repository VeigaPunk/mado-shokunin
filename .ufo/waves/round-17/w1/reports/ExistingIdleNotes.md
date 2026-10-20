# Existing idle/lock and terminal notes — non-contradiction, staleness, narrowable unknowns

Seat `MadoR17.ExistingIdleNotes` (scout, leaf). 2026-10-20. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. **Report only** — no lane file edited, no
erratum appended, no commit.

**Question answered:** for the two new documentary entries (P6 screen/idle =
hypridle+hyprlock; P4 terminal-emulator configs), (a) which existing claims they must not
contradict, (b) which existing claims are stale present-tense statements dated to the
2026-10-14 probes, (c) which recorded unknowns a documentary source route can narrow
(never resolve).

**Read (file bytes):** `corpus/knowledge/idle-lock-plane.md` (382 L),
`corpus/knowledge/terminals-and-omarchy.md` (206 L),
`corpus/knowledge/closeout-r11.md` §§1/5/7 (1–30, 144–240).
**Cross-read:** `corpus/README.md:48-80`, `PROVINCE.md:1-12`,
`SCORECARD.md` (round-17 declared claims), `corpus/knowledge/config-health-report-r3.md:283-296`,
`corpus/knowledge/remaining-planes-census.md:186-198,236-247`,
`corpus/knowledge/hyprland-config-plane.md:150-166`, `corpus/SOURCES.md` (row census).

Tags: `[OBS]` read directly in the named file this pass · `[INF]` inference ·
`[UNK]` unresolved. This report deliberately carries no rubric-V metadata; it is not a
knowledge entry and must not be counted as one.

**Host-pause compliance [OBS]:** no `sudo`, `pacman`/`yay`/`paru` (not even `-Q`/`-Si`),
`systemctl`, `hyprctl`, `loginctl`, `pgrep`/`pkill`, `libinput`/`evtest`/`wayland-info`,
`hypridle`/`hyprlock`/`alacritty`/`waybar`/`walker`/`omarchy-*`, notify, screenshot or
input probe was run. No web fetch. No separate omp CLI. Only `sed`/`grep`/`awk`/`cat`/
`wc`/`sha256sum` on file bytes. Nothing installed or updated, so there is no tooling
directive entry to record. Only write: this report.

---

## 0. Five headline constraints (read these before drafting)

1. **Documentary means documentary.** Both entries may describe upstream contracts and
   the host's *declared* files (read as bytes); they may not adopt any 2026-10-14 point
   sample as current host state, and they cannot re-measure it: every live channel used
   by those notes (hyprctl, loginctl, pgrep, systemctl, package queries) is paused.
2. **"hypridle is not running" is not a present-tense fact.** It is a 16:00–16:08 UTC
   point sample (`idle-lock-plane.md:51-56`), superseded later the same day by the
   recorded turnover (`:365-380`), and "never started" is already ruled out by journal
   evidence (`config-health-report-r3.md:283-296`). The new P6 entry must keep the three
   states distinct: *absent at probe* / *started at boot* / *stop cause unknown*.
3. **Unit state ≠ process state on this host.** The `hypridle.service` unit is
   `disabled` in every sample, while the daemon ran as a Hyprland autostart child; only
   `pgrep` discriminates (`idle-lock-plane.md:111-114`, `:371-375`). Any doc-derived
   sentence equating "unit disabled" with "no idle daemon" contradicts E2.
4. **Installed ≠ declared preference ≠ resolved launcher (P4).** "Only Alacritty was on
   PATH" (2026-10-14 `command -v`), "`~/.config/xdg-terminals.list` names
   `Alacritty.desktop` first" (file bytes) and "what `xdg-terminal-exec` actually
   launches" (resolver never executed, `idle-lock-plane.md:309-310`) are three different
   claims. A documentary route may explain the list format/precedence; it may not promote
   the declared preference into the resolved default.
5. **README's binding sentence governs both entries:** "These routes lead to inherited
   2026-10-14 evidence and its limitations, not present-tense health claims. Read appended
   errata before reusing the original body. Source commands that apply changes are
   operator handoffs, never permission to run them." (`corpus/README.md:50-53`).

---

## 1. Rubric-V interface the two new entries must satisfy

Facts `[OBS]`:

- `SCORECARD.md` round-17 C2 defines coverage as: an admitted `corpus/knowledge/` entry
  whose **first 15 lines** carry a `source` field citing a **mined tier-A** `SOURCES.md`
  row whose **used-by names that entry**, plus the entry declaring `surface: P<n>`; the
  legacy map is fixed to U1/U2→P1 and U7→P2 and is "never widened in this round".
- `idle-lock-plane.md` and `terminals-and-omarchy.md` contain **neither** a `source`
  field **nor** a `covers`/`surface` line in their first 15 lines (verified by
  `sed -n '1,15p' … | grep -c '^source:'` → 0/0; `grep -n '^covers:'` → no match for
  either file). They therefore **cannot count under rubric V**, before or after any
  wording edit that leaves them as-is; only new entries can carry P6/P4.
- `SOURCES.md` at `27cd06f`: 55 rows (`grep -cE '^\| *S[0-9]{3}'` → 55), and **zero**
  rows mention the four surfaces (`grep -ci` → alacritty 0, hypridle 0, hyprlock 0,
  xdg-terminal 0). Nearest adjacent rows are S020 (`apps/terminals.conf`, window-rule
  opacity effects) and S053/S054 (Waybar custom-module producer/renderer boundary).
  Those rows' used-by lists name other entries and their claims are about other
  surfaces, so citing them as the P4/P6 source cannot satisfy C2.

Consequences `[INF]`:

- The two drafts must cite new mined rows. Per the round contract, drafts write
  `S0xx-pending`; **L1** assigns ids from the reserved S056–S069 block on integration and
  must add the new entry's filename to each cited row's used-by cell.
- One `source` line may list several pending rows, but every cited row must end up
  `mined` + tier A and must name the entry; a tier-B or `lead` row is not countable.
- The entries must not re-use `covers:` — the legacy map is closed; a new `covers: U8`
  would be an undeclared widening, not coverage.

---

## 2. P6 (screen/idle) — claims the new entry must not contradict

Anchors are `idle-lock-plane.md` unless stated. "Must not contradict" means: quote it as a
dated record, never invert it, and never silently resolve an `[UNK]`.

| id | anchor | claim as recorded | drafting obligation |
|---|---|---|---|
| P6-C01 | 43-49 | Both configs are byte-identical to the shipped Omarchy payload (`diff` exit 0); declared chain = 150 s screensaver, 152 s lock via `omarchy-system-lock`, DPMS off ~3 s later unless `OMARCHY_LOCK_ONLY=true`, wake restores DPMS/backlight. | Cite as 2026-10-14 byte fact + declaration. Do not write "the daemon locks at 152 s". |
| P6-C02 | 60-77 | Pins: `hypridle.conf` 765 B/19 L `e7d3b8dd…`; `hyprlock.conf` 742 B/43 L `b8d173dc…`; theme `hyprlock.conf` 176 B/5 L `3ef010e7…`; no `.bak` for either idle file. | Historical pins; if reused, mark them dated. No fresh hash may be presented as the note's own measurement. |
| P6-C03 | 87-105 | Actuator inventory: 11 scripts + `idle.sh` + `default/hypr/autostart.conf`, sizes/line counts/first-12 digests, all payload mtime 2026-10-03 17:42:32. | Do not collapse script-defined effects into "hypridle does X". |
| P6-C04 | 109-114 | `hypridle.conf` has no `source` in any Hyprland config; startup declared as `exec-once = uwsm-app -- hypridle` (no `-c`); systemd unit exists, `disabled`, `ExecStart=/usr/bin/hypridle`; recorded package `hypridle 0.1.8-2`. | Version is a dated package pin, from a now-paused channel. Unit enabled/disabled says nothing about the running process (P6-C17). |
| P6-C05 | 116-131 | hypridle keys: `lock_cmd` = lock script; `before_sleep_cmd` = lock-only variant; `after_sleep_cmd` = `sleep 1 && wake`; `inhibit_sleep = 3`; listener 150 → `pidof hyprlock \|\| omarchy-launch-screensaver`; listener 152 → lock, `on-resume` wake. | Quote as file bytes. A doc may explain a key; it must not import upstream keys the file does not use as if they were host config. |
| P6-C06 | 133-135, 194-200, 212-214 | The ≈302 s lock is `[INF]` from the L14 comment ("screensaver resets idle timer"); "5 minutes" comment vs `timeout = 152` is reconciled only by that comment; no transition observed. | Keep both the reset assumption and the 302 s arithmetic as inference/`[UNK]`. A doc route may not be used to assert either happened. |
| P6-C07 | 142-146 | `inhibit_sleep = 3` numeric semantics beyond the comment were never verified against the binary. | A documented mapping narrows the question; the host value's effect stays unproven (P6-U6). |
| P6-C08 | 148-174 | hyprlock structure: theme `source`; `ignore_empty_input = true`; background `monitor` empty (all), path = current background symlink, `blur_passes = 3`; animations disabled; input-field 650x100 centered, JetBrainsMono, placeholder/fail_text, rounding 0, no shadow, `fade_on_empty = false`; fingerprint auth disabled at L41-43. Theme file defines exactly five colour vars (matte-black values). | Do not infer PAM/credential behaviour: the PAM surface is explicitly unread and out of province (`:174`). |
| P6-C09 | 177-192 | Declared 10-step chain incl. screensaver preconditions (`tte` required, `screensaver-off` flag, walker quit, per-monitor focus dance), lock side-effects (`switchxkblayout all 0`, `1password --lock`, `pkill` screensaver class, DPMS off after `sleep 3`), wake (`brightness-display on`, `brightness-keyboard restore`), suspend path (lock-only + inhibit 3). | These are script-declared effects, not executed behaviours. No step may be reported as observed. |
| P6-C10 | 202-210 | Host no-ops recorded: no keyboard backlight device (off/restore exit 1); `switchxkblayout all 0` is a no-op today (only `br` configured); lock kills the screensaver class, so the declared order ends with the screensaver removed. | "No-op today" is that probe's keyboard config, not a guarantee; the kill-on-lock ordering claim is script bytes and may be restated as such. |
| P6-C11 | 216-239 | Division of labour: Hyprland has no idle timer and no "panel off after N"; it supplies the wake half (`key_press`/`mouse_move` enable dpms) and the session-lock protocol; DPMS-off is delegated to the script chain. The `getoption` table values are live-probe samples. | The protocol/contract half may be cited from a spec; the option values are dated and their channel is paused. |
| P6-C12 | 241-267 | Point sample: no hypridle/hyprlock/hyprsunset/swayidle process; unit `inactive (dead)`, `disabled`; DP-1 `dpmsStatus: 1`; logind `IdleHint=no`, `LockedHint=no`; layers only wallpaper+waybar; live transitions UNKNOWN; stop cause UNK. | Every item must keep "at probe". Do not add a current-state reading. |
| P6-C13 | 269-294 | Toggle surface: `omarchy-toggle-idle` is a stateless `pgrep`/`pkill` toggle (no flag file); screensaver toggle uses `~/.local/state/omarchy/toggles/screensaver-off` (absent at probe); waybar `custom/idle-indicator` + `idle.sh` prints the disabled glyph when hypridle is absent; rendered bar state UNK. | Do not claim the bar currently renders either state; file-level behaviour only. |
| P6-C14 | 296-317 | Hardware/route deps: `/sys/class/backlight/` empty; no `*kbd_backlight*`; `tte` present; the operative screensaver branch is the Alacritty one; single monitor DP-1; `dpms off` carries no monitor argument. | Multi-monitor behaviour stays UNK (P6-U8). |
| P6-C15 | 318-325 | E1: the `hyprland-config-plane.md` §10 claim ("hypridle is not running … cause `[UNK]`") was re-measured and **held**; file counts/hashes agree. | Preserve the cross-note agreement; do not "correct" it. |
| P6-C16 | 327-345 | Eight named unknowns (see §6 below). | Every narrowing must cite its number; none may be silently closed. |
| P6-C17 | 347-356, 365-380 | §12 lists spot-check commands with 2026-10-14 outputs; E2 records the 16:11:06–07 UTC session turnover (Hyprland 1671 → 1203316), hypridle child 1203349 present 16:21:49 then **absent by 16:23:19**, unit inactive/disabled throughout, "only the `pgrep` half discriminates", configs re-hashed equal. | §12 is not a runbook now (`pgrep`/`systemctl`/`hyprctl`/`loginctl` are prohibited); E2 is dated evidence, not a current "hypridle absent". |

Additional P6-adjacent pin `[OBS]`: the recorded `hyprlock 0.9.6-3` lives **outside** the
idle note (`hyprland-config-plane.md:162`; `remaining-planes-census.md:244-245`). If the P6
entry binds a hyprlock doc tag to the host, that is the version to cite, and it is a
2026-10-14 package pin that cannot be refreshed under the pause. The idle note records no
hyprlock version itself.

---

## 3. P4 (terminal) — claims the new entry must not contradict

Anchors are `terminals-and-omarchy.md` unless stated.

| id | anchor | claim as recorded | drafting obligation |
|---|---|---|---|
| P4-C01 | 8-24 | Four terminal config trees exist; each has a `.bak.20261003-190229` sibling from the same second; sizes/lines/mtime: alacritty 876 B/28 L, foot 516/25, kitty 954/34, ghostty 1325/41, all mtime 2026-10-03 19:02. | Byte facts of that date; do not present as current file state. |
| P4-C02 | 29-40 | Alacritty: theme import `general.import`; `TERM=xterm-256color`; OSC 52 clipboard; JetBrainsMono 12.5; padding 14; `decorations = "None"`; Shift/Ctrl+Insert clipboard pair; Shift+Return and Alt+Shift+Return forced to CSI-u (comments explain TUI/mux reasons). | Anchors are byte positions in the file; a doc may explain the syntax, not re-measure the file. |
| P4-C03 | 41-51 | foot: theme `include`; `term=xterm-256color`; windowed; font 12.5; pad 14x14; `workers=0`; scrollback 10000; block cursor, blink off; clipboard bindings incl. `primary-paste=none`; CSI-u text bindings. | Same. |
| P4-C04 | 52-61 | kitty: theme include; font 12.5; padding 14; hidden decorations; `confirm_os_window_close 0`; clipboard pair; CSI-u `send_text`; `allow_remote_control yes`; cursor block/no blink; shell-integration no-cursor; audio bell off; tab bar bottom/powerline/slanted. | Same. |
| P4-C05 | 62-72 | ghostty: **optional** theme include (`?"…"`); font; `window-theme`; padding 14; close/resize/gtk options; cursor; `shell-integration-features` comment; CSI-u binds; split-resize binds; scroll multiplier; `async-backend = epoll` with cited link. | Do not upgrade the optional include to mandatory or resolve the linked discussion. |
| P4-C06 | 73-81 | Cross-terminal invariants: same font family, size 12.5, padding 14, Insert clipboard pair, CSI-u escapes in all four; block cursor with no blink in foot/kitty/ghostty; **Alacritty sets no cursor style here, default not measured**. | The alacritty cursor default is an explicit gap; a doc route may narrow it (P4-U5) but must stay documented-default, not host rendering. |
| P4-C07 | 83-89 | Theme plane: active theme `matte-black`; theme dir holds per-app colour files (`alacritty.toml`, `foot.ini`, `kitty.conf`, `ghostty.conf`, …); measured palette (`#121212`, `#bebebe`, cursor `#eaeaea`, selection `#515151`, color0 `#333333`, color1 `#D35F5F`, color4-family `#e68e0d`); templating sample with `{{ … }}` vars and user-template priority; colour edits belong to the theme layer. | Palette is a 2026-10-14 byte read of theme files; do not claim it is the rendered palette. |
| P4-C08 | 91-98 | Install/serving: only Alacritty was on PATH (`command -v`, 2026-10-14); `~/.config/xdg-terminals.list` 127 B lists `Alacritty.desktop` first; `/etc/xdg/xdg-terminals.list` absent (`stat`); `SUPER,RETURN` → `uwsm-app -- xdg-terminal-exec`; foot `.desktop` stubs are 28 B `Hidden=true`; omarchy install/default/restart routes were **read, not executed**; only Alacritty installed and referenced, the other three configs inert. | These are four separable claims (installed / list bytes / launcher binding / route text). No sentence may merge them into "Alacritty is the default terminal that launches". |
| P4-C09 | 100-113 | Backup delta: exactly one changed line per file, font size 9 → 12.5 (`size`, `size=`, `font_size`, `font-size`); no other diff. | Inference (one coordinated operator bump) stays inference. |
| P4-C10 | 115-151 | omarchy skill anatomy: single `SKILL.md` 392 L / 14,908 B; frontmatter covers the four terminal paths; section map incl. restart discipline `:172,204`, `unbind` rule `:272-284`, window-rules wiki re-fetch `:300-305`; claimed flat hooks (`:219-223`) vs observed five `*.d` dirs + one active hook — skill text older than shipped layout; documentation surface is read-only. | Skill stats are dated; do not restate the hook drift as repaired, and do not edit the skill. |
| P4-C11 | 153-166 | Summary: four trees exist; all delegate colour to matte-black; invariants; only Alacritty installed; `xdg-terminals.list` prefers Alacritty; backup delta 9→12.5; skill 392 L. Inferences: one operator bump; colour layer regenerated by theme changes; kitty/foot/ghostty inert because packages absent. | Summary drops the date; the new entry must re-date every sentence it reuses. |
| P4-C12 | 168-176 | Six unknowns: binaries outside PATH; whether `omarchy restart terminal` restarts the other three; operator's day-to-day terminal; backup provenance (hand vs tool); alacritty cursor default; exact `omarchy theme set` regeneration. | See §6. Unknowns 1 and 3 are not source-narrowable. |
| P4-C13 | 182-205 | R2-E1: round-1 body is 179 lines by `wc -l` (180 editor view, no trailing newline). R2-E2: §1/§4/§5/§6/§7 numbers re-measured and held, incl. `command -v` → only `/usr/bin/alacritty`, list 127 B first entry `Alacritty.desktop`, `/etc/xdg` list absent, both foot stubs 28 B, skill 392 L/14,908 B. | These re-measurements are still 2026-10-14; they do not extend the claim's date. |
| P4-C14 | census 186-198 | Same-day corroboration: package `alacritty 0.17.0-1`; three live Alacritty windows (PIDs/ppid/times); the other three terminal packages absent; theme import chain file-level unchanged; whether the live windows render today's theme bytes is `[UNK]`. | The version pin is dated and cannot be re-queried. Live windows are session weather, not a current census. |
| P4-C15 | README:60 | Limit sentence: "Only Alacritty was installed in the recorded sweep; the other configs are declarations, not tested consumers." | This is the canonical wording for the P4 limit; reuse it rather than a stronger claim. |

---

## 4. Cross-record claims (closeout §5, README, health register) that bind both entries

| id | anchor | claim | obligation |
|---|---|---|---|
| X-C01 | closeout:163-164 | "Final-round rule: 'carried' does not exist — every item is named with its state and where it lands." | New entries must name each disposition (narrowed / still unknown / out of province), not say "carried". |
| X-C02 | closeout:166-171 | Closed items bind to `f7bfc9f`; the round-1 `corpus/scripts/` path is superseded by `tools/mado-verify.sh`; the gate's ladder 28→268 is closed evidence there. | Do not quote gate counts or old paths as current. |
| X-C03 | closeout:173-179 | Operator-owned: theme choice and every config edit; the omarchy checkout's cleanliness (`git status`/`fetch` never run from this lane); the promotion decision (never self-declared); the live waybar absence in that window is session weather, and "a live FAIL that survives re-run is a finding about the session". | P4 must not describe any config edit as applied; neither entry may claim promotion or "health". |
| X-C04 | closeout:181-193 | Unknown with named owner: record-family debt (README rows, SCORECARD stubs, lessons, ⟨PENDING⟩ blocks, walker-deep errata, theme covering mutant, assertion-floor residue); each lands with the settlement or the failure is recorded. | Do not restate these as new discoveries or as resolved. |
| X-C05 | closeout:195-205 | Five open findings, append-only correction owed: F1 corrupted pin tail `…a5171`; F2 `snapshot-diff-receipt-r9.md:33` tail; F3 "2,837 L" that reproduces nowhere; F4 stale `ten-round-synthesis.md` pointer; F5 `SKILL.md:1314` stale citation. | New entries must not quote the corrupted/stale strings, and must not silently "fix" F1–F5 (write scope). |
| X-C06 | closeout:227-229, 234-235 (§7) | "If the gate moves: re-derive §2 whole — never quote this note's counts for a revision it does not name"; every correction is an appended erratum. | Any reused count carries its revision and date. |
| X-C07 | README:50-53 | Province routes "lead to inherited 2026-10-14 evidence and its limitations, not present-tense health claims. Read appended errata before reusing the original body. Source commands that apply changes are operator handoffs, never permission to run them." | The single strongest constraint on both entries. |
| X-C08 | README:60, 62, 74-83 | Limit rows: terminal — "only Alacritty was installed in the recorded sweep; the other configs are declarations, not tested consumers"; idle — "no idle/lock transition was exercised; consumer presence and stop-cause are dated observations/unknowns, not a new live verdict". Frontier list keeps idle/lock transitions and daemon stop-cause unresolved. | Reuse these sentences; do not retire them by adjacency. |
| X-C09 | health:283-296 | F1: consumer absent at probe; `journalctl` for the unit says "No entries", but the session journal shows hypridle started at boot Oct 13 11:02:09 via a `systemd-run` scope, now collected, no stop line; stop time/cause `[UNK]`; the only in-repo stopper is the stateless `omarchy-toggle-idle`. | "Never started" is ruled out; "started at boot" is not "runs now"; neither may be dropped. |
| X-C10 | SCORECARD round-17 C2 | Coverage here is "documentary routes, not observed behaviour"; U stays 7/7; "no exploratory claim". | No sentence in either entry may be justified by "the source implies the host behaves so". |
| X-C11 | SOURCES census | 55 rows at baseline; zero idle/terminal rows; reserved ids S056–S069 for L1. | Drafts use `S0xx-pending`; L1 assigns ids and writes used-by. |

---

## 5. Stale present-tense claims (measured 2026-10-14; six days before round 17)

Staleness here is **positional/grammatical**, not necessarily factual. I re-read the
pinned file bytes on 2026-10-20 `[OBS]`:

- `hypridle.conf` → `e7d3b8dd…` 765 B; `hyprlock.conf` → `b8d173dc…` 742 B; theme
  `hyprlock.conf` → `3ef010e7…` 176 B; both idle files still byte-identical to
  `~/.local/share/omarchy/config/hypr/` payload copies.
- Terminal trees: 876/28, 516/25, 954/34, 1325/41 bytes/lines — all match the recorded
  table; `~/.config/xdg-terminals.list` 127 B with comment lines plus
  `Alacritty.desktop`; `theme.name` = `matte-black`.
- The terminal note published no digests, so for those four only size/line-count identity
  is shown, not content identity against a recorded hash.

**Therefore:** the *file plane* has not drifted in anything I can check; the stale items
are the **live/process/version** claims, which cannot be re-measured under the pause. A
new entry that reuses a file fact should still date it, because dating is what makes the
claim falsifiable if the bytes change later.

### 5a. P6 stale claims

| id | anchor | text as it stands | why stale / risk | allowed phrasing |
|---|---|---|---|---|
| P6-S01 | 51-56 | "At probe time **hypridle is not running** … so `[INF]` the two timers cannot fire in this session as it stands." | E2 (same file) records the session replaced at 16:11:07 and the daemon present→absent later; F1 rules out "never started". A reader drops "at probe time". | "absent in the 16:00–16:08 UTC sample; later same-day present→absent; current status unmeasured." |
| P6-S02 | 111-114 | unit "exists … but is `disabled`. Binary `hypridle 0.1.8-2` (`pacman -Q`)." | Presents unit state beside a version as if diagnostic; E2 proves unit state never tracks the process; the query channel is paused. | "recorded unit disabled; recorded package 0.1.8-2 (2026-10-14); process presence independent." |
| P6-S03 | 241-246 | "no match" process; `inactive (dead)`, `disabled; preset: enabled`. | Point sample; `systemctl` now prohibited. | date it; do not restate as a check. |
| P6-S04 | 248-249 | DP-1 `dpmsStatus: 1`, `disabled: false` (panel on). | Live sample; `hyprctl` prohibited. | "at probe". |
| P6-S05 | 250-253 | logind `Type=wayland Active=yes State=active IdleHint=no IdleSinceHint=0 LockedHint=no`. | Live sample; `loginctl` prohibited; F1 shows idle state history is not inferable. | "at probe". |
| P6-S06 | 254-257 | layers = wallpaper (pid 1710) + waybar (pid 1707), no lock layer. | PIDs belong to the **pre-turnover** session (Hyprland 1671); E2 replaced it. Factually wrong today even as a sample of "the session". | cite as pre-turnover sample; never as current pids. |
| P6-S07 | 259-263 | "Live idle-state transitions: UNKNOWN … at the sample instant." | Boundary is correct; the risk is dropping "at the sample instant". | keep. |
| P6-S08 | 264-267 | cause of absence "still `[UNK]` (open since round 1, re-measured in rounds 2/3 and **now**)". | "now" is 2026-10-14; E2 narrows (fresh session launches via autostart, then exits). | "open through the 2026-10-14 probes". |
| P6-S09 | 216-230 | `getoption` table values (`misc:key_press_enables_dpms` 1, `cursor:inactive_timeout` 0, etc.). | Live probe values; channel prohibited; table's `set` column reads as current settings. | label table "2026-10-14 `getoption` sample"; keep `set=false` = engine default distinction. |
| P6-S10 | 236-239 | "cursor:invisible reads `0` now (screensaver not running)". | Live sample; also depends on the absent screensaver claim. | "at probe". |
| P6-S11 | 273-290 | flag "absent at probe"; `idle.sh` prints disabled glyph "exactly when hypridle is absent"; rendered state `[UNK]`. | Mixed: flag absence is a filesystem sample (not re-measured here), `idle.sh` is file bytes, rendering is UNK. | keep the three classes separate. |
| P6-S12 | 347-356 | "§12 Spot-checks (reproducible)" with four commands and outputs. | Heading invites re-execution of `pgrep`/`systemctl`/`hyprctl`/`loginctl`, all prohibited; outputs are 2026-10-14. | "historical spot-checks"; do not reproduce as recheck steps. |
| P6-S13 | 14-19 | Method block lists `hyprctl` verbs, `pgrep`/`pidof`, `systemctl --user status`, `loginctl`, `pacman -Q`. | Copying this as "method available" breaches the pause and the round's documentary scope. | method of the **2026-10-14** pass only. |
| P6-S14 | 43-49 | "Both config files are byte-identical … The declared chain is two hypridle listeners…" | Present tense over a byte fact plus a declaration. Value still reproduces (my 2026-10-20 hash), but it is dated. | "bytes at 2026-10-14 (and unchanged 2026-10-20); declared chain as follows." |
| P6-S15 | 365-380 | E2: "absent **again by 16:23:19** UTC"; "§1/§7's 'not running' remains true as a point sample of the probe window, not of the session after the turnover". | E2 is itself dated; a reader can lift "absent again" into the present. | cite E2 with its date; do not extend it. |

### 5b. P4 stale claims

| id | anchor | text as it stands | why stale / risk | allowed phrasing |
|---|---|---|---|---|
| P4-S01 | 93 | "Only Alacritty is on PATH: `command -v alacritty` → `/usr/bin/alacritty`; `command -v foot`, `kitty`, `ghostty` → no output (not found), 2026-10-14." | Date is present but sentence is present-tense; no re-check is permitted (a `command -v` is harmless but would be a new claim). | "recorded 2026-10-14: only Alacritty resolved on PATH." |
| P4-S02 | 94 | "`~/.config/xdg-terminals.list` (127 B, 2026-10-03) lists `Alacritty.desktop` as first choice; `/etc/xdg/xdg-terminals.list` does not exist (stat)." | Mixes a current-looking preference with a dated stat; bytes reproduce 2026-10-20 (127 B, content confirmed) but "first choice" is a declaration, not a resolution. | "list bytes name `Alacritty.desktop` (unchanged 2026-10-20); declared preference, resolver not run." |
| P4-S03 | 96 | foot launcher entries "are hidden stubs: … 28-byte files". | 2026-10-14 `cat`; still a file claim, must be dated. | "recorded 2026-10-14". |
| P4-S04 | 97 | omarchy routes "exist and were read (not executed)"; route summaries quoted. | Route text is 2026-10-14 help output; `omarchy` is prohibited now and the checkout may have moved. | "routes as recorded 2026-10-14, not executed". |
| P4-S05 | 98 | "only Alacritty is installed and referenced. kitty/foot/ghostty configs are inert on this host until their packages are installed." | Present-tense conclusion from a dated sweep; package queries prohibited. | README:60 wording + date. |
| P4-S06 | 155-159 | §8 observations: "only Alacritty installed; `xdg-terminals.list` prefers Alacritty". | Summary drops the date and compresses installed vs preference (headline constraint 4). | keep the two claims separate and dated. |
| P4-S07 | 119, 140-146 | skill `SKILL.md` 392 L / 14,908 B; hooks listing observed `*.d` dirs. | Dated file stats; a drift-watch note exists precisely because the skill/checkout moves. | "recorded 2026-10-14". |
| P4-S08 | census 195-198 | "Package `alacritty 0.17.0-1`; the other three terminal packages are absent"; three live windows. | Same-day package query and process census; channel paused; windows are session weather. | "recorded 2026-10-14". |
| P4-S09 | 161-166 | Inferences: colour layer "would be regenerated"; configs "are inert here because their packages are absent". | Inferences are fine, but the second reads as a current state. | keep `[INF]` and date the premise. |
| P4-S10 | idle:309-310 (cross) | "`xdg-terminal-exec --print-id` … resolves the default terminal — the resolver itself was not executed this pass." | The P4 entry's list claim must not silently inherit a resolver result that was never run. | "resolver not executed"; doc route explains format only. |

---

## 6. Unknowns a sourced documentary route could narrow

"narrow" = reduce the question to a documented contract or a smaller candidate set.
No source can convert any of these into observed host behaviour, and none may be marked
resolved. The named source families are route candidates, not evidence; the source seats
own the actual rows. `[INF]` judgments about document scope are mine and unverified here.

### 6a. P6

| UNK (idle note) | route candidate | what it can establish | what it must never be used to claim | verdict |
|---|---|---|---|---|
| 1. why hypridle is not running | none | at most that the toggle is stateless and the autostart route exists — both already in the note | any cause, or that it is absent now | **not narrowable** |
| 2. live transitions, reset assumption, ≈302 s | ext-idle-notify-v1 protocol spec; hypridle listener docs at the pinned tag | the protocol's idle/notify/resume contract and what "listener fires" means | that 150/152/302 s occurred, or that the screensaver resets the timer on this host | **partial (contract only)** |
| 3. which component writes logind `IdleHint`/`LockedHint`; whether hyprlock participates | logind D-Bus interface docs (`SetIdleHint`, `LockedHint`); ext-session-lock-v1 spec | eligible writers and the lock/unlock events a session-lock client produces | the host's current values, or that hyprlock set them | **partial (contract: candidate writers)** |
| 4. whether hypridle/hyprlock configs parse cleanly | upstream key reference at `hypridle 0.1.8` / `hyprlock 0.9.6` | whether each key used in the host files is a documented key at that version | that the files parse; no read-only validator exists and loading mutates the session | **partial (unknown-key risk only)** |
| 5. cursor restore if hyprlock is killed while `cursor:invisible` is true | hyprlock docs / Hyprland cursor docs at the pinned versions | documented ownership of cursor visibility during lock/unlock | that a killed locker restores the cursor; the reset is only in the screensaver trap | **partial (ownership, not kill behaviour)** |
| 6. `inhibit_sleep = 3` semantics | hypridle config reference at 0.1.8 | the documented numeric mapping, if the reference defines it | that the host's sleep inhibition behaves that way | **partial/strong (documented mapping)** |
| 7. whether the waybar idle indicator's rendering matches `idle.sh` | none new | S053/S054 already bound producer vs rendered text; the boundary is settled | any rendered-state claim | **already bounded; do not reopen** |
| 8. multi-monitor behaviour | hyprlock `background.monitor` reference; Hyprland `dpms` dispatch docs | that an empty/absent monitor means all monitors and that a no-argument dpms dispatch targets all | behaviour on this host (single DP-1) or any multi-monitor observation | **partial (declared semantics)** |
| (side) PAM service/data used by hyprlock | — | nothing admissible | any credential-surface claim | **out of province; exclude** |

### 6b. P4

| UNK (terminal note) | route candidate | what it can establish | what it must never be used to claim | verdict |
|---|---|---|---|---|
| 1. binaries outside PATH | xdg-terminal-exec spec (resolution by desktop entry `Exec`, not PATH) | what "installed" must mean for the list to resolve; where else entries could come from | that foot/kitty/ghostty exist anywhere | **partial (definition only)** |
| 2. whether `omarchy restart terminal` restarts the other three | omarchy checkout script bytes for the restart route (read-only) | the declared target set and mechanism of that command | that running it works or that it was executed | **strong-ish (declared targets)** |
| 3. operator's day-to-day terminal | none | nothing | any usage claim | **not narrowable** |
| 4. backup provenance (hand vs tool) | omarchy refresh/backup code path; naming convention it produces | the timestamped `.bak` convention and which tool would produce it | that the tool produced these backups; name match is consistent, not proof | **partial** |
| 5. alacritty cursor default | Alacritty man page / config reference at `0.17.0` | the documented default cursor style/blink for that version | host rendering, or a version other than the recorded 0.17.0-1 | **strong (documented default)** |
| 6. exact `omarchy theme set` regeneration for terminal colour files | omarchy theme-set script bytes + `themed/` template docs | the regeneration mechanism, template priority, and which files it rewrites | that a theme set occurred or that the host files were regenerated | **partial/strong (mechanism)** |
| (new) what the xdg-terminals list means | xdg-terminal-exec spec/repo | path precedence (`~/.config` before `/etc/xdg`), file format, first-valid-entry rule | which entry is valid *now* or what launches | **strong (format/precedence)** |
| (new) foot/kitty/ghostty config validity | upstream references at matching tags | documented key validity — but the host versions are unrecorded, so no tag can be bound | any version-bound claim, any "config is valid" claim | **weak/partial (unbound tag)** |

---

## 7. Hard must-nots checklist for the two drafts

1. No sentence in either entry may assert a live/process/compositor/package state as
   current; every such sentence is either absent or explicitly a 2026-10-14 record.
2. P6 must keep UNK-1 through UNK-6 and UNK-8 open (UNK-4 and UNK-6 may be narrowed to a
   documented key set or numeric mapping, never resolved); UNK-7 stays the already-bounded
   producer/renderer boundary and must not be reopened. P4 must keep UNK-1, UNK-3, UNK-4,
   UNK-5 and UNK-6 open (UNK-2 and UNK-6 may be narrowed to declared targets/mechanism).
3. P6 must never say "never started" (F1) or equate `disabled` unit with no daemon (E2).
4. P6 must never present the ≈302 s chain or the reset assumption as measured; script
   effects are declared, not observed.
5. P4 must never merge installed, listed preference, and resolved launcher.
6. Neither entry may cite a tag as proof of the host binary, and P4's Alacritty tag must
   be 0.17.0 (recorded); P6's hypridle tag 0.1.8 and hyprlock tag 0.9.6 come from dated
   cross-note pins, not from the idle note.
7. Neither entry may quote F1–F5 corrupted/stale strings, repair them, or cite
   `ten-round-synthesis.md`.
8. Neither entry may describe a config edit, service action, or probe as performed; the
   pause holds and the operator owns edits.
9. No `covers:` token; `surface:` P6/P4 plus a first-15-lines `source` line citing pending
   tier-A rows, with L1 assigning ids and used-by.
10. README limit sentences (X-C08) are reused, not retired.

---

## 8. Remaining unknowns of this report

- **U-A** `[UNK]` Whether the upstream references at the pinned tags actually enumerate
  every key used by the host files (the hypridle general/listener keys and the hyprlock
  blocks). The Src* seats own that check; my "narrowable" verdicts are `[INF]` about
  document scope, not readings.
- **U-B** `[UNK]` The host `hyprlock` version is not in the idle note; it is only in
  `hyprland-config-plane.md:162` and `remaining-planes-census.md:244-245` (`0.9.6-3`). Whether
  the P6 entry should cite that cross-note pin is an L1 interface decision.
- **U-C** `[UNK]` The reserved SOURCES ids (S056–S069) and the exact row set the P6/P4
  drafts will cite; drafts must say `S0xx-pending` and L1 assigns.
- **U-D** `[UNK]` Live/process state at round-17 time. Not measured, not measurable here;
  my 2026-10-20 checks are file bytes only and do not constitute a health claim.
- **U-E** `[INF]` My staleness classification treats "present tense over a 2026-10-14
  measurement" as stale even where the value still reproduces. If L1 prefers a stricter
  definition (only values that no longer reproduce), then the count collapses to the
  process/PID/version items (P6-S01, S02, S03, S06, S09, S10, S12; P4-S05, S06, S08) —
  the rest are dated-but-holding.
- **U-F** `[UNK]` Whether `hyprlock.conf`'s theme include resolves today; the symlink
  target was not re-read (only the file and theme pin hashes were).

---

## 9. Reproduction (all read-only)

```text
sed -n '1,15p' corpus/knowledge/idle-lock-plane.md
sed -n '1,15p' corpus/knowledge/terminals-and-omarchy.md
grep -n '^## ' corpus/knowledge/idle-lock-plane.md
grep -n '^## ' corpus/knowledge/terminals-and-omarchy.md
grep -nE '^## (4|5|7|9|10|11|12)\.' corpus/knowledge/idle-lock-plane.md
grep -n '^covers:' corpus/knowledge/*.md
for f in corpus/knowledge/*.md; do echo "$(sed -n '1,15p' "$f" | grep -c '^source:') $(basename "$f")"; done
grep -cE '^\| *S[0-9]{3}' corpus/SOURCES.md            # 55 at 27cd06f
grep -ci 'alacritty' corpus/SOURCES.md                 # 0
grep -ci 'hypridle'  corpus/SOURCES.md                 # 0
grep -ci 'hyprlock'  corpus/SOURCES.md                 # 0
grep -ci 'xdg-terminal' corpus/SOURCES.md              # 0
sed -n '48,86p' corpus/README.md
sed -n '144,240p' corpus/knowledge/closeout-r11.md
sed -n '283,296p' corpus/knowledge/config-health-report-r3.md
sed -n '186,198p;236,247p' corpus/knowledge/remaining-planes-census.md
sed -n '150,166p' corpus/knowledge/hyprland-config-plane.md

# file-byte pins (2026-10-20; no execution, no package query)
sha256sum ~/.config/hypr/hypridle.conf ~/.config/hypr/hyprlock.conf \
          ~/.config/omarchy/current/theme/hyprlock.conf \
          ~/.local/share/omarchy/config/hypr/hypridle.conf \
          ~/.local/share/omarchy/config/hypr/hyprlock.conf
wc -c -l ~/.config/alacritty/alacritty.toml ~/.config/foot/foot.ini \
         ~/.config/kitty/kitty.conf ~/.config/ghostty/config \
         ~/.config/hypr/hypridle.conf ~/.config/hypr/hyprlock.conf \
         ~/.config/omarchy/current/theme/hyprlock.conf
cat ~/.config/omarchy/current/theme.name ~/.config/xdg-terminals.list
```

Byte-check result `[OBS]`: idle/lock and theme pins reproduce exactly
(`e7d3b8dd…`, `b8d173dc…`, `3ef010e7…`; 765/742/176 B; 19/43/5 L) and both idle files
still equal their payload copies; terminal files match the recorded
876/516/954/1325 B and 28/25/34/41 L; `xdg-terminals.list` is 127 B and its only
uncommented entry is `Alacritty.desktop`; `theme.name` is `matte-black`. **This is a
byte-stability observation, not a live or health claim**, and it does not upgrade any
2026-10-14 sentence.

No tool was installed or updated; no fleet or sibling-lane file was touched; no commit,
no git mutation, no jj command.
