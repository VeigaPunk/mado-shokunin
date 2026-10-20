# SrcHypridleSrc — hypridle v0.1.8 source anchors (P6 idle/lock route)

Seat: MadoR17.SrcHypridleSrc (leaf source-evidence scout). Report only; no lane, ledger or
knowledge edits. No subagent dispatch. Host package/compositor commands: none issued
(host-wide pause respected; no pacman/yay/paru/sudo/systemctl/hyprctl/live probes).

## Provenance

- Repository: `hyprwm/hypridle`. Latest release per `https://github.com/hyprwm/hypridle/releases/latest`
  → HTTP 302 → `releases/tag/v0.1.8`; release page `relative-time datetime="2026-07-26T14:45:24Z"`.
- Highest tag by `git ls-remote --tags`: `v0.1.8` = `e5c01af0842bd66617f7004568df9406111d6e80`
  (lightweight tag: no `refs/tags/v0.1.8^{}` entry; `refs/heads/main` =
  `aa958ed7ad4863860b93ecd7189419e193bfae2c`). Tags seen: v0.1.0–v0.1.8.
- Access date: 2026-10-20. Fetched with `curl` from
  `https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/<path>`
  (HTTP 200 each). A second fetch of `src/core/Hypridle.cpp` was byte-identical (`cmp` clean).

| File | Bytes | Lines | SHA-256 of raw bytes |
|---|---|---|---|
| `src/core/Hypridle.cpp` | 29880 | 735 | `2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75` |
| `src/core/Hypridle.hpp` | 3611 | 105 | `f9e4e5587075fe34ae3279c4225b00661c686468035c4ad6cbe71e098fc0a2b8` |
| `src/config/ConfigManager.cpp` | 7613 | 188 | `396f1f99ad0795f37d6e63f717eea9c8d67f776f7ce02333c3fca2a699f2cb11` |
| `src/config/ConfigManager.hpp` | 1127 | — | `b9e3e90b7a562bc2202328dfbf140430800736260ad5fe4648cb14f7de4b19a5` |
| `CMakeLists.txt` (dependency pin) | — | — | `84c0fd3ce2b2a19c8f22471d2931fd394b7c9dc889b4b34d37a7f11e92919aeb` |
| support: `hyprwm/hyprutils` `src/os/Process.cpp` @v0.9.0 | 7377 | — | `f7decbc2ccebac1ec2900dfafabea66d274417d8ce1feacb78c3a7b875ed5d14` |

Host binary/version: **[UNK]** — no package queries were run (paused), and a tag's source never
establishes the installed binary. `CMakeLists.txt:47` requires only `hyprutils>=0.2.0`; the
reviewed `Process.cpp` is at hyprutils v0.9.0, so process semantics below carry that version
qualifier. hyprlock is **out of scope** of this report (not fetched).

## 1. Where timeout listeners are created and where on-timeout / on-resume fire

All in `src/core/Hypridle.cpp`. Pipes inside quoted spans are escaped as `\|` only to keep
GFM table structure; the source text is otherwise unmodified.

| Role | Lines | Anchors (verbatim, each ≤25 words) |
|---|---|---|
| Rules → listener array; notification created per rule at `timeout * 1000` ms | 60–85 | L65–79: `if (*IGNOREWAYLANDINHIBIT \|\| r.ignoreInhibit)` selects `sendGetInputIdleNotification(r.timeout * 1000 /* ms */, m_sWaylandState.seat->resource())` else `sendGetIdleNotification(r.timeout * 1000 /* ms */, m_sWaylandState.seat->resource())`; L61 `m_sWaylandIdleState.listeners.resize(RULES.size());` |
| Timeout callback wiring | 81–84 | L83 `l.notification->setIdled([this](CCExtIdleNotificationV1* n) { onIdled((CHypridle::SIdleListener*)n->data()); });`; L84 the same shape with `setResumed` → `onResumed` |
| **on-timeout fires (primary)** | 298–328 (`onIdled` 298; gate 301–309; condition gate 311–323; spawn 325–327) | L325–327 `Debug::log(LOG, "Running {}", pListener->onTimeout);` / `pListener->onTimeoutFired = true;` / `spawn(pListener->onTimeout);` |
| **on-timeout fires (condition-retry path)** | 264–280 inside `enterEventLoop`, spawn at 274–275 | L274–275 `Debug::log(LOG, "Condition met, running {}", l.onTimeout);` / `spawn(l.onTimeout);` |
| Inhibit gate on on-timeout | 301–304 | `if (g_pHypridle->m_iInhibitLocks > 0 && !pListener->ignoreInhibit) {` |
| **on-resume fires** | 330–361 (`onResumed` 330; gate 343–350; empty check 354–357; spawn 359–360) | L346 `// If on-timeout never actually executed (was inhibited), skip on-resume too`; L352 `pListener->onTimeoutFired = false;`; L360 `spawn(pListener->onRestore);` — note `onRestore` is loaded from `r.onResume` at L68 |
| Inhibit-count drop while idled: destroy + recreate every notification and re-wire callbacks | 363–396 (core 371–393) | L371 `if (m_iInhibitLocks == 0 && isIdled) {`; L379 `l.notification->sendDestroy();`; L381–391 re-create + `setIdled`/`setResumed` |
| Wayland lock notification wiring (hyprland-lock-notify-v1) | 89–93 | L91 `m_sWaylandState.lockNotification->setLocked([this](CCHyprlandLockNotificationV1* n) { onLocked(); });`; L92 same with `setUnlocked` → `onUnlocked` |
| Wayland lock/unlock handlers | 398–416 (`onLocked`), 418–436 (`onUnlocked`) | L402–404 `g_pConfigManager->getValue<Hyprlang::STRING>("general:on_lock_cmd")` / `spawn(*LOCKCMD);`; L414–415 `if (m_inhibitSleepBehavior == SLEEP_INHIBIT_LOCK_NOTIFY)` / `uninhibitSleep();`; L430–431 mirror with `inhibitSleep();`; L433–435 `general:on_unlock_cmd` spawn |
| Missing lock-notify protocol warning | 104–107 | `general:inhibit_sleep=3, general:on_lock_cmd and general:on_unlock_cmd will not work.` |
| `spawn` helper (async, no explicit wait in this file) | 286–296 | L289 `Hyprutils::OS::CProcess proc("/bin/sh", {"-c", args});`; L290 `if (!proc.runAsync()) {`; L295 `Debug::log(LOG, "Process Created with pid {}", proc.pid());` |
| `condition_cmd` helper (sync, exit-code checked) | 151–162 | L155 `if (!proc.runSync()) {`; L161 `return exitCode == 0;` |

Observed gates a documentary note must carry:

- on-resume is suppressed when the rule's on-timeout never ran (inhibited or empty command):
  `onTimeoutFired` is set only at line 326 or 273 and cleared at 352.
- on-timeout is suppressed entirely while `m_iInhibitLocks > 0`, unless the rule sets
  `ignore_inhibit` (line 301).
- `ignore_wayland_inhibit` / per-rule `ignore_inhibit` choose a different ext-idle-notify
  request (`sendGetInputIdleNotification`), not just a different callback.

## 2. D-Bus surfaces: inhibit, systemd, ScreenSaver, logind Lock/Unlock/PrepareForSleep

All in `src/core/Hypridle.cpp` unless stated.

| Surface | Lines | Anchors (verbatim, each ≤25 words) |
|---|---|---|
| System bus connection | 97–102 | L98 `m_sDBUSState.connection = sdbus::createSystemBusConnection();` |
| logind session path + matches | 603–615; registration 610–611 | L608 `proxy->callMethod("GetSession").onInterface("org.freedesktop.login1.Manager").withArguments(std::string{"auto"}).storeResultsTo(path);`; L610 `m_sDBUSState.connection->addMatch("type='signal',path='" + path + "',interface='org.freedesktop.login1.Session'", ::handleDbusLogin);`; L611 `m_sDBUSState.connection->addMatch("type='signal',path='/org/freedesktop/login1',interface='org.freedesktop.login1.Manager'", ::handleDbusSleep);` |
| **logind Lock / Unlock** handler | 465–488 | L467–468 `g_pConfigManager->getValue<Hyprlang::STRING>("general:lock_cmd")` / `g_pConfigManager->getValue<Hyprlang::STRING>("general:unlock_cmd")`; L473 `if (MEMBER == "Lock") {`; L478 `spawn(*LOCKCMD);`; L480 `} else if (MEMBER == "Unlock") {`; L485 `spawn(*UNLOCKCMD);` |
| **systemd BlockInhibited** parsing | 516–531; property-changed wrapper 533–540; match 617–618; initial snapshot 620–623 | L520 `if (inhibits_.contains(":idle:")) {`; L524 `g_pHypridle->onInhibit(true);`; L529 `g_pHypridle->onInhibit(false);`; L618 `m_sDBUSState.connection->addMatch("type='signal',path='/org/freedesktop/login1',interface='org.freedesktop.DBus.Properties'", ::handleDbusBlockInhibitsPropertyChanged);` |
| **ScreenSaver service** (session bus) | 626–666; service name 634; vtable 640–651; paths 628–631 | L634 `m_sDBUSState.screenSaverServiceConnection = sdbus::createSessionBusConnection(sdbus::ServiceName{"org.freedesktop.ScreenSaver"});`; L640 `obj->addVTable(sdbus::registerMethod("Inhibit").implementedAs([object = obj.get()](std::string s1, std::string s2) {`; L643 `sdbus::registerMethod("UnInhibit").implementedAs([object = obj.get()](uint32_t c) {` |
| ScreenSaver inhibit handler + cookie registry | 542–582 | L564–567 `if (inhibit)` / `g_pHypridle->onInhibit(true);` / `else if (cookieFound)` / `g_pHypridle->onInhibit(false);`; L572 `auto cookie = CHypridle::SDbusInhibitCookie{.cookie = cookieID, .app = app, .reason = reason, .ownerID = ownerID};` |
| Cookie cleanup on bus-name vanish | 584–597; match 657–658 | L591 `size_t removed = g_pHypridle->unregisterDbusInhibitCookies(oldOwner);`; L594–595 `for (size_t i = 0; i < removed; i++)` / `g_pHypridle->onInhibit(false);` |
| Inhibit counter core | 363–396 | L364 `m_iInhibitLocks += lock ? 1 : -1;`; L371–372 `if (m_iInhibitLocks == 0 && isIdled) {` + `general:ignore_wayland_inhibit` |
| **PrepareForSleep** handler + ordering | 490–514 | L493–494 `if (MEMBER != "PrepareForSleep")` / `return;`; L496–497 `bool toSleep = true;` / `msg >> toSleep;`; L504 `std::string cmd = toSleep ? *SLEEPCMD : *AFTERSLEEPCMD;`; L506–507 `if (!toSleep)` / `g_pHypridle->handleInhibitOnDbusSleep(toSleep);`; L512–513 `if (toSleep)` / `g_pHypridle->handleInhibitOnDbusSleep(toSleep);` |
| Sleep-inhibit mode selection | 109–143 | L113 `switch (*INHIBIT) {`; L120 comment `// auto (enable, but wait until locked if before_sleep_cmd contains hyprlock, or loginctl lock-session and lock_cmd contains hyprlock.)`; L128 `case 3: // wait until locked`; L142–143 `if (m_inhibitSleepBehavior != SLEEP_INHIBIT_NONE)` / `inhibitSleep();` |
| Sleep-inhibit toggling | 671–681 | L677–680 `if (!toSleep)` / `inhibitSleep();` / `else` / `uninhibitSleep();` |
| logind `Inhibit` call (type `sleep`, mode `delay`) | 683–725 | L694–698 `createMethodCall(sdbus::InterfaceName{"org.freedesktop.login1.Manager"}, sdbus::MethodName{"Inhibit"})`; `method << "sleep";`; `method << "hypridle";`; `method << "Hypridle wants to delay sleep until it's before_sleep handling is done.";`; `method << "delay";` |
| Inhibitor release | 727–735 | L733–734 `Debug::log(LOG, "Releasing the sleep inhibitor!");` / `m_sDBUSState.sleepInhibitFd.reset();` |
| Event-loop dispatch (system dbus, wayland, ScreenSaver session dbus) | 215–256 | L234 `while (m_sDBUSState.connection->processPendingEvent()) {`; L252 `while (m_sDBUSState.screenSaverServiceConnection->processPendingEvent()) {` |

## 3. ConfigManager facts (src/config/ConfigManager.cpp)

| Fact | Lines | Anchors (verbatim, each ≤25 words) |
|---|---|---|
| Config discovery | 10–26 | L20 `static const auto paths = Hyprutils::Path::findConfig("hypridle");` |
| `listener` special category (anonymous, per-entry) | 58 | `m_config.addSpecialCategory("listener", Hyprlang::SSpecialCategoryOptions{.key = nullptr, .anonymousKeyBased = true});` |
| Listener keys + defaults | 59–64 | `timeout` INT −1; `on-timeout` `""`; `on-resume` `""`; `ignore_inhibit` INT 0; `condition_cmd` `""`; `condition_retry` INT 0 |
| `general:` keys + defaults | 66–75 | `lock_cmd`, `unlock_cmd`, `on_lock_cmd`, `on_unlock_cmd`, `before_sleep_cmd`, `after_sleep_cmd` all STRING `""`; `ignore_dbus_inhibit`/`ignore_systemd_inhibit`/`ignore_wayland_inhibit` INT 0; L75 `m_config.addConfigValue("general:inhibit_sleep", Hyprlang::INT{2});` |
| Rule construction from special-category keys | 95–131 | L107 read `timeout`; L110–111 read `on-timeout`/`on-resume`; L113–115 read `ignore_inhibit`/`condition_cmd`/`condition_retry` |
| Missing timeout is an error but other rules still parse | 117–120 | `if (timeout == -1) {` / `result.setError("Category has a missing timeout setting");` / `continue;` |
| Parse errors logged, parsing continues | 84–92 (init) | L86–87 `if (result.error)` / `Debug::log(ERR, "Config has errors:\n{}\nProceeding ignoring faulty entries", result.getError());` |
| `source=` include with glob + circular-include guard | 137–188 | L146 `glob(absolutePath(rawpath, CURRENTDIR).c_str(), GLOB_TILDE, nullptr, glob_buf.get())`; L160–161 `source= skipping already included source file {} to prevent circular dependency` |

Key-name consequence for any P6 route note: **two distinct lock-command families** exist.
`general:lock_cmd`/`general:unlock_cmd` are spawned by the **logind Session Lock/Unlock**
signal (`handleDbusLogin`, 465–488). `general:on_lock_cmd`/`general:on_unlock_cmd` are spawned
by the **Wayland hyprland-lock-notify-v1** events (`onLocked`/`onUnlocked`, 398–436). They are
not aliases.

## 4. Observed ordering facts (cite only with the caveats attached)

1. `PrepareForSleep(true)`: the code spawns `before_sleep_cmd`, then releases the logind delay
   inhibitor (lines 509–513 → 671–680 → 727–734). In hypridle's own `spawn()`, the process is
   started with `runAsync()` and the function returns after logging the pid (286–296). At
   hyprutils v0.9.0, `runAsync()` double-forks and the parent `waitpid`s only the intermediate
   child (`Process.cpp:197–256`), and `~CProcess()` only deletes its impl (`Process.cpp:30–32`).
   So at this source pair the delay inhibitor is released **without awaiting the command's
   completion**; the logind reason string at line 697 states the opposite intent. This is a
   code-reading fact, not observed host behavior, and the host hyprutils version is [UNK].
2. `PrepareForSleep(false)`: hypridle re-acquires the sleep inhibitor **before** spawning
   `after_sleep_cmd` (506–507 precede 509–510).
3. `onUnlocked` re-acquires sleep inhibition before spawning `on_unlock_cmd` (430–435);
   `onLocked` releases it after spawning `on_lock_cmd` and emitting `ActiveChanged(true)`
   (402–415).
4. `onInhibit` destroys and recreates every ext-idle-notify object when the lock count reaches
   zero while idled (371–393). A rule's pending `condition_cmd` retry is orphaned by that
   recreation; `onResumed` compensates by clearing `conditionPending` for **all** rules
   (343–344; comment 334–342).
5. The 5-second event-loop wakeup exists for `condition_cmd` retries (221, 264–280).
6. If `hyprland-lock-notify-v1` is absent, `general:inhibit_sleep=3` assigns nothing
   (128–131) and an invalid value falls through `default` (132); the enum member has no
   default initializer (`Hypridle.hpp:67–71`), so the mode later compared at 135–142 is not
   defined by that path. The 104–107 warning only states that mode 3 and the two
   lock-command keys "will not work". Source-level observation; not executed here.

## 5. What this evidence supports for the P6 documentary route (and what it cannot)

Supported (documentary, tag-pinned):

- hypridle v0.1.8 has exactly these trigger families: ext-idle-notify-v1 timeouts with
  `on-timeout`/`on-resume`, hyprland-lock-notify-v1 lock/unlock, logind `Session.Lock`/
  `Session.Unlock`, logind `Manager.PrepareForSleep`, systemd `BlockInhibited` (`:idle:`),
  and the `org.freedesktop.ScreenSaver` `Inhibit`/`UnInhibit` service with `NameOwnerChanged`
  cleanup.
- The config surface is the `listener` special category (`timeout`, `on-timeout`, `on-resume`,
  `ignore_inhibit`, `condition_cmd`, `condition_retry`) plus `general:` keys listed in §3,
  with `inhibit_sleep` defaulting to 2 and `source=` includes supported.
- `inhibit_sleep=2` auto-detection inspects `before_sleep_cmd` for `hyprlock` and
  `lock_cmd` for `hyprlock` together with `before_sleep_cmd` containing `lock-session`
  (120–124) — this is the only in-tree link from hypridle to hyprlock semantics.

Not supported (must stay [UNK] in any note):

- Which hypridle version, if any, is installed on this host, and whether its packaged build
  matches tag v0.1.8.
- Any claim about actual timeout values, lock integration, or inhibitor behavior on the host.
- Any claim that `before_sleep_cmd` completes before sleep proceeds (see §4.1).
- Anything about hyprlock's own config/behavior — not fetched by this seat.

## 6. Remaining unknowns

- Host hypridle/hyprutils versions and packaged config contents: [UNK] (no queries permitted).
- Whether the host compositor exposes `hyprland-lock-notify-v1`. Without it, v0.1.8 warns that
  `general:inhibit_sleep=3`, `on_lock_cmd` and `on_unlock_cmd` "will not work" (104–107), and
  mode 3 leaves the sleep-inhibit mode unassigned (§4.6).
- Runtime effect of that unassigned mode on a host lacking the protocol: [UNK] (no execution,
  no host queries).
- `runAsync()` semantics at hyprutils versions other than v0.9.0: [UNK]; `CMakeLists.txt:47`
  only sets `hyprutils>=0.2.0`.
- hyprlock v0.1.8-parallel sources: not inspected (outside this assignment).

Tools installed/updated: none (directive satisfied by using `curl`, `git ls-remote`, `cmp`,
`sha256sum`, `awk`, `sed`, `grep` only; no package manager, no sudo).
