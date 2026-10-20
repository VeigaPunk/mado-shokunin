# SrcLogindLock — systemd logind D-Bus: Lock/Unlock signals, PrepareForSleep, delay inhibitors

Seat: `MadoR17.SrcLogindLock` (scout, round 17 / hyaku phase 2).
Scope of this report only: what the *documentation* says, quoted, for the
logind side of the P6 idle/lock route — `Lock`/`Unlock` signals,
`PrepareForSleep`, and the `delay` inhibitor mode that hypridle's
`inhibit_sleep` / `before_sleep_cmd` / `after_sleep_cmd` sit on.
No host behaviour is claimed. No live command was run (see § Method audit).
Write scope honoured: this file only; no commit, no git/jj mutation, no
fleet/sibling-lane edit, no delegation.

Status of each statement below: **[OBS-doc]** = read verbatim in the cited
documentation; **[INFERENCE]** = my reasoning across sources, flagged;
**[UNK]** = not observable under this round's pause.

## 1. Sources opened

| ref | URL | kind / version marker | raw digest and size | access |
|---|---|---|---|---|
| S1 (`S0xx-pending`) | https://raw.githubusercontent.com/systemd/systemd/v260.4/man/org.freedesktop.login1.xml | tag `v260.4` of systemd/systemd; this file's bytes are also the current `main` bytes (same digest) | sha256 `ce9838f0b762142b8a5f33a7c81bcd1384bf747e88901b12dab675d01769e781`, 89983 bytes, 1707 lines | 2026-10-20 |
| S1-render | https://www.freedesktop.org/software/systemd/man/260/org.freedesktop.login1.html | rendered release page; footer marker `systemd 260.4` | sha256 `4f3175179d4af4be0eb3ca54848c4cf33b940e77d1fd03afda3445b3ba3f2afa`, 90354 bytes; `Last-Modified: Thu, 23 Jul 2026 22:21:43 GMT` | 2026-10-20 |
| S2 (`S0xx-pending`) | https://systemd.io/INHIBITOR_LOCKS/ (no-slash URL 301s here) | **unversioned** upstream prose doc, linked from S1; self-describes only "systemd 183 and newer" — no tag exists to pin | sha256 `bcc8630a9f839c450212b46b5f6fa4ccb3b60080a4d9006c3886e6bbbb74054b`, 16722 bytes, 285 lines; `Last-Modified: Sat, 17 Oct 2026 01:26:08 GMT` | 2026-10-20 |
| S3 (consumer, cross-check only) | https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp | tag `v0.1.8` | sha256 `2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75`, 29880 bytes, 735 lines | 2026-10-20 |

Version-marker discipline: the release page `/260/` renders `systemd 260.4`,
matching tag `v260.4`. The `/latest/` page today renders `systemd 262`
(sha256 `4db07079022fed290311ad8d1d853710f4069d91ee3fb86b0b614399a4413684`,
90352 bytes) but its `login1` content is unchanged from `v260.4` — the
`main` copy of the XML is byte-identical to `v260.4` (same sha256), and the
four sampled sentences (Q1, Q3, Q5, Q12) verify verbatim in the `/latest/`
render too. v258, v259 and v260 carry the same Q1/Q2/Q7 sentences. A tag's
text is **not** evidence of the host's installed logind version: host
version stays **[UNK]** (no package queries under the pause).

Method: fetched with `curl`; quotes verified by stripping XML/HTML tags,
unescaping entities, collapsing whitespace to single spaces, then substring
matching; anchors computed by mapping the matched span back to line numbers
of the raw carrier. Word counts are whitespace-split counts, and every quote
below is ≤25 words.

## 2. The reported request, corrected precisely

The task names "Lock/Unlock signals". The documents support a narrower and
exact statement, and one negative:

1. **[OBS-doc]** There is **no** `Lock`/`Unlock` signal on the Manager
   interface. The Manager signals listed in the introspection block are
   `SecureAttentionKey`, `SessionNew`, `SessionRemoved`, `UserNew`,
   `UserRemoved`, `SeatNew`, `SeatRemoved`, `PrepareForShutdown`,
   `PrepareForShutdownWithMetadata`, `PrepareForSleep`
   (S1 `:441-459`; signatures `:180-189`). Manager *methods*
   `LockSession()`, `UnlockSession()`, `LockSessions()`, `UnlockSessions()`
   exist at `:347-353`.
2. **[OBS-doc]** `Lock()`/`Unlock()` are signals on
   `org.freedesktop.login1.Session`, with no arguments
   (introspection block S1 `:1236-1237`; methods `Lock(); Unlock();` at
   `:1206-1207`).
3. **[OBS-doc]** The Manager methods are the trigger; §3 Q6 is the sentence
   that joins the two layers.
4. **[INFERENCE]** `loginctl lock-session` / `lock-sessions` are the usual
   clients of those Manager methods. I did not open the `loginctl(1)` page,
   so this mapping is the round's existing vocabulary, not a claim of this
   seat. The hypridle wiki quoted by the P6 note uses the same phrase
   ("e.g. loginctl lock-session").

## 3. Quotes (carrier = S1 raw XML `v260.4` unless marked S2)

Every row: id, verbatim quote, word count, raw line anchor, and whether the
identical byte sequence also occurs in the S1-render page.

| id | quote (verbatim, ≤25 words) | w | anchor | in render |
|---|---|---|---|---|
| Q1 | "Lock()/Unlock() is sent when the session is asked to be screen-locked/unlocked. A session manager of the session should listen to this signal and act accordingly." | 25 | :1515-1517 | yes |
| Q2 | "signals are sent right before (with the argument true) or after (with the argument false) the system goes down for reboot/poweroff and suspend/hibernate, respectively." | 24 | :788-790 | no — render inserts typographic quotes around `true`/`false` (render :438-439) |
| Q2b | (render-safe fragment of Q2) "the system goes down for reboot/poweroff and suspend/hibernate, respectively." | 9 | :789-790 | yes |
| Q3 | "After completion of this work they should release their inhibition locks in order to not delay the operation any further." | 20 | :791-793 | yes |
| Q4 | "whether it should just delay the operation to a certain maximum time" | 12 | :762-763 | yes |
| Q5 | "The method returns a file descriptor. The lock is released the moment this file descriptor and all its duplicates are closed." | 21 | :764-765 | yes |
| Q6 | "This is implemented by sending out the Lock() and Unlock() signals from the respective session object which session managers are supposed to listen on." | 24 | :609-610 | yes |
| Q7 | "Signals are only emitted on objects referencing a specific session ID, not on the /org/freedesktop/login1/session/self or /org/freedesktop/login1/session/auto convenience objects" | 19 | :1520-1522 | no — render inserts quotes around the two paths (render :810-812) |
| Q8 | "what is one or more of shutdown, sleep, idle, handle-power-key, handle-suspend-key, handle-hibernate-key, handle-lid-switch, separated by colons" | 16 | :754-757 | no — render quotes each literal (render :416-419) |
| Q9 | "It returns an array of structures consisting of what, who, why, mode, uid (user ID), and pid (process ID)." | 19 | :593-595 | yes |
| Q10 | "may be used to set the \"locked hint\" to locked, i.e. information whether the session is locked." | 17 | :1468-1469 | yes |
| Q11 | "This is intended to be used by the desktop environment to tell systemd-logind when the session is locked and unlocked." | 20 | :1469-1471 | yes |
| Q12 | "boolean properties are true during the interval between the two PrepareForShutdown() and PrepareForSleep() signals respectively" | 15 | :842-844 | yes |

Signatures carried verbatim by the introspection blocks: `PrepareForSleep(b start);`
(S1 `:189`), `Inhibit(in s what, in s who, in s why, in s mode, out h fd);`
(S1 `:156`), `SetLockedHint(in b locked);` (S1 `:1209`).

Carrier S2 (raw HTML, anchors are raw-file line numbers; "render" column not
applicable because S2 *is* the raw HTML):

| id | quote (verbatim, ≤25 words) | w | anchor |
|---|---|---|---|
| H1 | "delay inhibits operations only temporarily, either until the lock is released or up to a certain amount of time." | 19 | :88 |
| H2 | "This is intended to be used by applications which need a synchronous way to execute actions before system suspend" | 19 | :89 |
| H3 | "This mode is only available for sleep and shutdown locks." | 10 | :90 |
| H4 | "The signal with False is generally delivered only after the system comes back from suspend" | 15 | :152 |
| H5 | "watching PrepareForShutdown(true)/PrepareForSleep(true) without taking a delay lock is racy and should not be done" | 14 | :156 |
| H6 | "quickly execute the operations they wanted to execute before suspend/shutdown and then release any delay lock taken" | 17 | :149 |
| H7 | "ensure the lock screen for the eventual resume is on the screen before the system enters suspend state" | 18 | :243 |
| H8 | "InhibitDelayMaxUSec contains the delay timeout value as configured in logind.conf(5)." | 10 | :164 |
| H9 | "As soon as you see PrepareForSleep(true), save your data, then release the lock" | 13 | :194 |
| H10 | "These locks need to be taken in the “block” mode, “delay” is not supported for them." | 16 | :241 |
| H11 | "each consisting of What, Who, Why, Mode as above, plus the PID and UID of the process" | 17 | :142 |
| H12 | "this will only be sent out for suspend/resume cycles done via logind" | 12 | :160 |
| H13 | "If the client dies while the lock is taken the kernel automatically closes the file descriptor so that the lock is automatically released." | 23 | :138 |
| H14 | "A delay lock taken this way should be released ASAP on reception of PrepareForShutdown(true)" | 14 | :140 |
| H15 | "As soon as the file descriptor is closed (and all its duplicates) the lock is automatically released." | 17 | :137 |

## 4. What that composes to (documentary facts, no host claim)

1. **[OBS-doc]** Screen-lock request flow: a client calls a Manager method
   (`LockSession(session_id)` / `LockSessions()`) or the Session method
   (`Lock()`), and logind emits the no-argument `Lock` signal on the
   *session object*; `Unlock` mirrors it (Q1, Q6, Q7). A session manager is
   the intended listener (Q1). No signal is ever emitted on the
   `session/self` or `session/auto` convenience objects, so a listener must
   resolve a concrete session path first (Q7).
2. **[OBS-doc]** Reverse direction: a desktop can tell logind that the
   session is locked/unlocked via `Session.SetLockedHint(b locked)`
   (Q10, Q11) — this does not emit `Lock`/`Unlock`; it records state.
3. **[OBS-doc]** Sleep flow: `PrepareForSleep(b start)` is one signal for
   both edges — `true` before suspend/hibernate begins, `false` after it
   completes or fails (Q2; S2 `:146-147`). The `PreparingForSleep` property
   is true between the two edges (Q12). S2 adds the boundary: the signal is
   only sent for suspend/resume cycles done via logind, not low-level
   kernel-induced suspend (H12).
4. **[OBS-doc]** Delay inhibitor: `Manager.Inhibit(what, who, why, mode)`
   returns one fd; `mode="delay"` means "delay the operation to a certain
   maximum time" rather than block it (Q4, Q5); `what="sleep"` is the sleep
   lock (Q8); the fd is the lock — closing it (or all duplicates) releases
   it, and the kernel closes it if the client dies (Q5, H13, H15).
5. **[OBS-doc]** Delay is bounded, not indefinite: bounded by
   `InhibitDelayMaxSec=` in `logind.conf(5)`, exposed as the
   `InhibitDelayMaxUSec` property (H2, H8). `delay` is valid only for
   `sleep` and `shutdown`; the `handle-*` locks must be `block` (H3, H10).
6. **[OBS-doc]** Intended delay-lock protocol: hold the lock, run the
   pre-sleep actions on `PrepareForSleep(true)`, release the lock as soon as
   those actions are done (H6, H14, H9), then re-take the lock on
   `PrepareForSleep(false)` so the next cycle is again synchronous (H4,
   S2 `:154`). Watching `true` without holding a delay lock is explicitly
   called racy (H5).
7. **[OBS-doc]** Observability surface for a documentary note:
   `ListInhibitors()` returns `what, who, why, mode, uid, pid` (Q9) — i.e.
   a held delay lock is enumerable *if* one is allowed to query; the
   `BlockInhibited` / `DelayInhibited` properties encode the active lock
   types (S2 `:162`).
8. **[OBS-doc]** S2 line `:140` (H14) says "on reception of
   PrepareForShutdown(true)" in the general delay-lock paragraph; for a
   `sleep` lock the operative edge is `PrepareForSleep(true)` (H6, H9). Do
   not lift H14 as sleep semantics without that correction — it is the one
   wording trap in this material.

## 5. Consumer mapping that the P6 note can now cite (S3, cross-check)

These are source-read facts about hypridle `v0.1.8`, not host behaviour;
they are recorded here only to bind the documented contract to the consumer
the P6 note already describes.

- **[OBS-src]** hypridle resolves its session and subscribes on the
  *concrete* path — `GetSession("auto")`, then
  `addMatch("type='signal',path='<resolved>',interface='org.freedesktop.login1.Session'")`
  (S3 `:604-610`). This is exactly what Q7 requires.
- **[OBS-src]** It subscribes to the Manager path
  `/org/freedesktop/login1` for `PrepareForSleep`, requires
  `MEMBER == "PrepareForSleep"`, and reads the boolean (S3 `:611`, `:490-497`).
- **[OBS-src]** It selects `before_sleep_cmd` on `toSleep` and
  `after_sleep_cmd` otherwise (S3 `:504`), then drives the inhibitor
  (`:506-513`, `:671-681`).
- **[OBS-src]** It takes the lock exactly as Q4/Q5/Q8 describe:
  `Inhibit("sleep", "hypridle", "…before_sleep handling is done.", "delay")`,
  holds the returned fd (dup'd `F_DUPFD_CLOEXEC`) and releases it by closing
  (S3 `:694-723`, `:727-735`).
- **[OBS-src]** Its `handleDbusLogin` matches members `"Lock"` and
  `"Unlock"` (S3 `:465-485`), i.e. the Q1/Q6 signals on the session object.
- **[INFERENCE]** Therefore `inhibit_sleep`'s "normal" path is the
  documented delay-lock protocol of §4.6, and `before_sleep_cmd` executes in
  the `PrepareForSleep(true)` window with the delay held. Whether the host
  ever enters that window is live behaviour and stays **[UNK]**.

## 6. Draft SOURCES.md rows (ids reserved to L1; `S0xx-pending`)

Both rows are `mined`, tier A, `used-by` = the P6 note that already exists
in the tree. If L1 prefers one row only, keep the S1 row: it is the
tag-pinned carrier for every signal/method claim, and S2 is linked from it.

```text
| S0xx-pending | systemd logind D-Bus interface manual — https://raw.githubusercontent.com/systemd/systemd/v260.4/man/org.freedesktop.login1.xml | docs | A | Documented Manager/Session lock and sleep signal contract, Inhibit delay mode and fd lifetime; not host logind version or behaviour | tag v260.4; raw sha256 ce9838f0b762142b8a5f33a7c81bcd1384bf747e88901b12dab675d01769e781 (89983 B, 1707 lines), bytes equal current main; rendered /260/ page carries "systemd 260.4"; Session Lock/Unlock signals :1236-1237, docs :1515-1522; PrepareForSleep :189, :788-793; Inhibit :156, :754-765; ListInhibitors :593-595; SetLockedHint :1468-1471 | Manager Lock/Unlock are methods that emit session-object Lock/Unlock signals; PrepareForSleep carries true-before/false-after; delay mode releases on fd close; signals never on self/auto objects | mined | 2026-10-20 | on-release | corpus/knowledge/idle-lock-route-r17.md |
| S0xx-pending | Inhibitor Locks — https://systemd.io/INHIBITOR_LOCKS/ | docs | A | Documented delay-lock protocol (release on the true edge, re-take on false), its time bound and its logind-only delivery boundary; unversioned upstream prose | final URL after 301; raw sha256 bcc8630a9f839c450212b46b5f6fa4ccb3b60080a4d9006c3886e6bbbb74054b (16722 B, 285 lines); delay mode :88-90; release/re-take :140-156; logind-only :160; delay-lock scheme :188-196; handle-* block-only :241 | delay is bounded by InhibitDelayMaxSec and only for sleep/shutdown; watching the true edge without a delay lock is racy; PrepareForSleep is not sent for kernel-initiated suspend | mined | 2026-10-20 | on-release | corpus/knowledge/idle-lock-route-r17.md |
```

Note for L1: `used-by` must name the entry exactly as it lands. If the P6
note is renamed or split, move this value with it; the row's `status` should
only become `mined` once the note's `source:` line actually names the row id.

## 7. Ready front matter for the P6 note (L1 applies)

`corpus/knowledge/idle-lock-route-r17.md` already carries `surface: P6` and
six `S0xx-pending` sources, and already cites hypridle's `PrepareForSleep`
handler and `inhibit_sleep` modes. It has **no** logind-side source. Two
additive edits make the note's logind claims sourced rather than inferred:

1. Append to the `source:` line:

```text
; S0xx-pending https://raw.githubusercontent.com/systemd/systemd/v260.4/man/org.freedesktop.login1.xml (Session signals, Signals, Inhibit, ListInhibitors, SetLockedHint, Properties); S0xx-pending https://systemd.io/INHIBITOR_LOCKS/ (delay, signals, delay-lock scheme, miscellanea)
```

2. Add to the note's anchor-key table:

```text
| LD | https://raw.githubusercontent.com/systemd/systemd/v260.4/man/org.freedesktop.login1.xml | systemd 260.4 (tag) | `[LD:n]` = file line |
| IL | https://systemd.io/INHIBITOR_LOCKS/ | unversioned upstream doc, no tag | `[IL:n]` = raw HTML line |
```

Citation lines the note may then use, each already true of the quoted text:

- "A lock request reaches the session as a `Lock` signal, not a Manager
  signal: `LockSession()`/`LockSessions()` are implemented by sending the
  session object's `Lock()`/`Unlock()` signals [LD:609-610, LD:1515-1517]."
- "Listeners must bind a concrete session path: signals are not emitted on
  `/session/self` or `/session/auto` [LD:1520-1522]; hypridle resolves
  `GetSession("auto")` before subscribing [HC:604-610]."
- "`PrepareForSleep` is one signal with a boolean, true before and false
  after suspend [LD:788-790, IL:146-147]; hypridle selects
  `before_sleep_cmd` on true [HC:493-504]."
- "hypridle holds a `delay` lock on `what="sleep"` for exactly that window
  [HC:694-698, IL:88-90]; the wait is bounded, so the command cannot hold
  sleep indefinitely [IL:89, IL:164, LD:806-810]."
- "The lock dies with its fd — including if the client dies [LD:764-765,
  IL:137-138]."
- "logind emits the signal only for suspend/resume it performs, not for
  kernel-initiated suspend [IL:160] — the presence of the edge is a
  measurement, not an assumption."
- "`delay` is not accepted for `handle-*` locks [IL:90, IL:241]; those are
  `block` locks and are a different route from `before_sleep_cmd`."

Line anchors for the `[LD:805-809]` citation above: the properties paragraph
that names `InhibitDelayMaxUSec` sits at S1 `:805-809` in `v260.4` (six lines
later than in `v260`; the whole shift is one added `ScheduleShutdown` `usec`
paragraph, the only diff between the two tags).

## 8. Remaining unknowns (do not let a note imply otherwise)

- `[UNK]` **Host systemd/logind version.** No `pacman -Q`, `systemctl`, or
  binary read was performed (host-wide pause). Tag text never establishes
  the installed version.
- `[UNK]` **Host `InhibitDelayMaxSec=` value.** `/etc/systemd/logind.conf*`
  is outside this round's authorized read scope and was not read; the doc
  only fixes the property name and that it reflects configuration (H8).
- `[UNK]` **The host's session object path / manager bus address.** Needs
  `loginctl`-class tooling; paused.
- `[UNK]` **Whether anything on this host listens to `Session.Lock`.** The
  doc assigns that duty to "a session manager" (Q1); whether one exists
  here, and whether it is the compositor, `uwsm`, or nothing, is a live
  question. `[INFERENCE]` hypridle listens for its own `lock_cmd`; that is a
  consumer, not the manager.
- `[UNK]` **Whether this host's suspend actually goes through logind** (the
  precondition for H12's signal at all). Live.
- `[UNK]` **Whether `hyprland-lock-notify-v1` is exposed** (decides
  `inhibit_sleep=3`), already carried as `[UNK]` by the P6 note; unchanged
  by this seat.

## 9. Method audit

- Commands issued: `curl` (docs and one source file), `sha256sum`, `wc`,
  `grep`/`awk`/`sed` on `/tmp` copies, `python3 -I` for quote/anchor
  verification (read-only, stdin scripts, no file writes outside `/tmp`).
- Not issued, per pause: no `sudo`, `pacman`/`yay`/`paru` (not even `-Q`),
  `systemctl`, `loginctl`, `hyprctl`, `hypridle`, `hyprlock`, `waybar`,
  `walker`, `omarchy-*`, `dbus-*`, `notify-send`, screenshots, or device
  probes. No OMP session transcript was read (not named by this item).
- No tool installed or updated; nothing to record under the tooling
  directive.
- Carrier honesty: Q2, Q7 and Q8 are marked `no` in the render column only
  because the XSLT render wraps `<literal>` values in typographic quotes;
  the sentences are present at the cited render lines and the underlying
  XML is tag-pinned. Q2b is the render-exact fragment.
