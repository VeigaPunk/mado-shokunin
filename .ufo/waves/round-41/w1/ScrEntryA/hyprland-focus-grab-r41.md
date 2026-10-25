# The focus grab: a client's own focus whitelist, how Hyprland 0.56.2 enforces it, and what this host advertises

source: S283 - hyprwm/hyprland-protocols focus-grab-v1.xml @ cd1aba6bd78775825eb230b3a4274c48b6705eb7 - both interfaces, every request, the `cleared` event
source: S284 - hyprwm/Hyprland src/protocols/FocusGrab.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f - the compositor-side grab object and the seat grab it installs
source: S285 - quickshell-mirror/quickshell src/wayland/hyprland/focus_grab/grab.cpp @ 9b0f339b19057f4731bf3b48293307d7ef241671 - one real client's grab lifecycle
source: S286 - hyprwm/xdg-desktop-portal-hyprland v1.4.1 src/core/PortalManager.cpp - the registry listener that logs every global and binds ten of them
source: S287 - github.com/hyprwm/Hyprland/issues/565 - the rule-level counterpart, as a closed 2022 tracker record
source: S288 - hyprwm/hyprland-protocols README.md @ cd1aba6bd78775825eb230b3a4274c48b6705eb7 - what upstream says the protocol is for
source: S289 - own-work: `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`, saved at .ufo/waves/round-41/fetch/xdph-journal.txt (sha256 bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7) - the host advertisement census
source: S037 - xdg-desktop-portal-hyprland v1.4.1 release (held row; installed package 1.4.1-2) - the identity of the portal whose journal this is
verified-at: 2026-10-25
recheck: 90d - re-pull the four pinned files, re-read the installed package record, re-run the journal census; a Hyprland tag after v0.56.2 is the earlier trigger
ground: what a client-side focus limiter is on this compositor - the protocol surface, the enforcement point, the host's advertisement of it, one client's lifecycle, and the rule layer it is not
Lane: mado-shokunin. Round: 41.
assimilated-from: merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md and merge/mado/knowledge/corpus/knowledge/focus-control-surfaces-r28.md (sections 1, 2 and 4; its section 3 is the localized documentation channel, outside PROVINCE.md, and is not cited here)

## §1 The protocol: a manager, a grab, and a whitelist

**OBS** S283 (`hyprland_focus_grab_v1`, the grab interface's description): "This interface restricts input focus to a specified whitelist of surfaces" - and at protocol level the same file says "This protocol allows clients to limit input focus to a specific set of surfaces", so the surface is a *limiter over the client's own surfaces*, not a way to focus anyone else's.

**OBS** S283 (`hyprland_focus_grab_manager_v1`, version 1): the manager has exactly two requests - `create_grab`, taking a `new_id` of `hyprland_focus_grab_v1`, and the destructor `destroy`, whose description says it "doesn't destroy existing focus grab objects". The grab has `add_surface` and `remove_surface` (each taking a `wl_surface`), `commit`, its own destructor, and one event, `cleared`.

| interface | member | kind | what it does |
|---|---|---|---|
| `hyprland_focus_grab_manager_v1` (v1) | `create_grab(grab: new_id hyprland_focus_grab_v1)` | request | makes one grab object |
| | `destroy` | destructor request | destroys the manager only; existing grabs survive |
| `hyprland_focus_grab_v1` (v1) | `add_surface(surface: wl_surface)` | request | whitelists a surface; duplicate additions ignored; takes effect on `commit` |
| | `remove_surface(surface: wl_surface)` | request | un-whitelists; a destroyed surface is treated as this call; takes effect on `commit` |
| | `commit` | request | applies the pending list: empty -> non-empty starts the grab, non-empty -> empty makes it inert |
| | `destroy` | destructor request | destroys the grab and removes it if active |
| | `cleared` | event | the compositor cancelled an active grab |

**OBS** S283 (`commit`, the transition rule): "If the list previously had no entries and now has at least one, the grab will start." The start/stop condition is in the request text, not left to the compositor.

**OBS** S283 (`hyprland_focus_grab_v1`, routing and the trigger): the keyboard goes to one surface the compositor picks from the set - "a compositor-picked surface in the whitelist will receive a wl_keyboard::enter event" - pointer and touch inside a whitelisted surface pass normally, and "Upon meeting implementation-defined criteria usually meaning a mouse or touch input outside of any whitelisted surfaces" the compositor clears the whitelist, renders the grab inert and sends `cleared`; the same happens if another focus grab or similar action starts, at the compositor's discretion.

**INF** The protocol cannot move focus outside the set: the keyboard lands on a *compositor-picked* whitelisted surface and the client controls only membership. `Basis:` S283's interface description and the `commit` request text.

**UNK** What "implementation-defined criteria" and "similar action" cover beyond pointer/touch-outside and a competing grab. The XML enumerates neither, and S284 is read below for the branches it contains, not as an enumeration.

## §2 The compositor side: a seat grab carrying a surface set

**OBS** S284 (`src/protocols/FocusGrab.cpp`, `CFocusGrab::CFocusGrab`): "m_grab->m_keyboard = true;" - the grab object allocates a `CSeatGrab` with keyboard and pointer both enabled, and "m_grab->setCallback([this]() { finish(true); });" makes the grab finish *itself*, with the `cleared` event, when the seat grab is cancelled.

**OBS** S284 (`CFocusGrab::start`): "m_grabActive = true; g_pSeatManager->setGrab(m_grab);" - starting means installing this object as the seat's grab; the same method then calls `simulateMouseMovement()` and `refocusKeyboard()`.

**OBS** S284 (`CFocusGrab::finish`): "if (sendCleared) m_resource->sendCleared();" - the event is conditional on the flag, the destructor calls `finish(false)`, and the seat grab is dropped only if it is still the current one ("if (g_pSeatManager->m_seatGrab == m_grab) g_pSeatManager->setGrab(nullptr);"), so a grab object destroyed while another grab owns the seat does not unseat it.

**OBS** S284 (`CFocusGrab::commit`): "if (anyCommitted) start(); else finish(true);" - each surface carries a three-valued state (`PendingAddition`, `PendingRemoval`, `Committed`); a commit promotes additions into the seat grab and erases removals, and only a change of the set triggers start or finish. A surface's destroy signal routes to `eraseSurface`, which removes it and commits with `removeOnly = true`, so destruction can never re-add a surface.

**OBS** S284 (`CFocusGrab::refocusKeyboard`): the keyboard is moved to the first committed surface through `Desktop::focusState()->rawSurfaceFocus(surface)`, and the no-surface branch logs "called with no committed surfaces. This should never happen." - the compositor treats "grab active, nothing committed" as a bug rather than a state.

**OBS** S284 (`CFocusGrabProtocol::onCreateGrab`): a grab whose resource fails `good()` gets `pMgr->noMemory()` and is popped from the protocol's list, so a failed allocation is a protocol error, not a silent no-op.

**INF** The whitelist is enforced at the seat, not at the rule layer: nothing in this file consults a window or workspace rule, and the object's effect is the `CSeatGrab` it installs and removes. `Basis:` S284's constructor, `start` and `finish`.

**UNK** How `CSeatGrab` routes an event that falls outside the set - the receipt holds the grab object, not the seat manager. The XML states the effect (outside input clears the grab; keyboard goes to a whitelisted surface); the seat's own code was not read this round.

## §3 What this host advertises, and who is listening

**OBS** S289 (saved journal, latest session, `2026-10-25T13:36:24-03:00`, pid 1952): "Got interface: hyprland_focus_grab_manager_v1 (ver 1)" - one advert, version 1, in a session that opens with "Gathering exported interfaces" after "XDG_CURRENT_DESKTOP set to Hyprland".

journal sessions=2 adverts=78 interfaces=63 focus_grab=1

**OBS** S289 (session structure): the file holds two portal sessions - pid 1918, whose slice opens mid-stream at 13:16:45 with 15 adverts and closes at "Stopped Portal service (Hyprland implementation).", and pid 1952, which opens at "Starting Portal service (Hyprland implementation)" and carries the other 63. The `-- Boot` marker sits between them.

**INF** Only the second session is a whole advertisement: the first is a journal slice that begins after that portal was already running, so its 15 adverts are a lower bound. The census line above therefore reports the latest session - 63 distinct names, no name advertised twice - which is the only session that can be compared with the compositor's registry as a whole.

**OBS** S286 (`src/core/PortalManager.cpp`, `CPortalManager::onGlobal`, lines 85-261): every global is logged before any branch, with 'Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);', and what follows is a fixed set of ten named branches - screencopy, global shortcuts, input capture ("if (INTERFACE == hyprland_input_capture_manager_v1_interface.name)"), xdg-output, toplevel export, `wl_output`, dmabuf, `wl_shm`, foreign toplevel, toplevel mapping. The focus-grab manager is not one of them.

**OBS** S286 and S289 (measured this round, read-only): `grep -in focus` over `PortalManager.cpp` exits 1 - the string does not occur in the file at all - and in the whole journal the string `focus` occurs exactly once, on the advert line itself, while the same session logs `[input-capture] init successful` and `[globalshortcuts] registered`. The portal logs the global and does not use it.

**OBS** S037 (installed package record, read-only file read of `/var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc`): "%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2" - the portal that wrote this journal is upstream v1.4.1 at pkgrel 2, so S286's `v1.4.1` pin and the running unit are the same upstream release. This receipt grounds the *installed* version, not the release page: the tag anchor `v1.4.1` and its commit `cc8e5ef` are S037's own row, not re-fetched this round.

**INF** The advertisement is a *compositor* fact, not a portal capability: the line exists because the portal dumps the registry it was handed, and the portal's own bind list excludes the manager. A client that wants the protocol binds it itself; the `wl_registry` is the only gate the receipts show, and the XML names no app-id, sandbox or permission condition. `Basis:` S283, S286, S289.

**INF** The compositor that logged this is the one S284 is pinned at: `hyprctl version` this round printed `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f`, the same commit as the source pin. That version read is a dated measurement, not a registry row; the pin is what this entry cites.

**UNK** Which process on this host binds `hyprland_focus_grab_manager_v1` today, and whether any does. The journal shows the advert, not a bind, and this round ran no Wayland client of its own.

## §4 A real client's lifecycle: quickshell

**OBS** S285 (`src/wayland/hyprland/focus_grab/grab.cpp`, `FocusGrab::sync`): "the protocol will always send cleared() when the grab is deactivated," - the client's own comment states the invariant it relies on, which is exactly S284's `finish(true)` path, and why the destructor's `finish(false)` matters for a client that is being torn down anyway.

**OBS** S285 (`FocusGrab::addWaylandWindow`): "this->pendingAdditions.append(window); this->commitRequired = true;" - adding a window records it and *defers* the protocol call; `sync()` is the only place that commits.

**OBS** S285 (`FocusGrab::sync`): "if (!this->active) { this->active = true; emit this->activated(); }" - the client's `active` flips only after a commit that left pending additions, and `hyprland_focus_grab_v1_cleared()` sets it back to false and emits `cleared`.

**OBS** S285 (`FocusGrab::addWindow` and `removeWindow`): a `QWindow` that is not yet a `QWaylandWindow` is added on `surfaceCreated`, or on `visibleChanged` after `window->create()`; removal disconnects the window, drops it from `pendingAdditions`, calls `remove_surface` and sets `commitRequired`.

**INF** The client treats the protocol as a two-phase set operation with a transaction boundary: `startTransaction()` and `completeTransaction()` suspend `sync()`, so a batch of windows becomes one `commit` and at most one `activated`. `Basis:` S285's `sync`, `startTransaction`, `completeTransaction`.

**UNK** Whether one Qt transaction is one frame in practice, and whether a `cleared` arriving between `add_surface` and `commit` is observable to this client. Neither is measured here.

## §5 The rule-level counterpart: focus the compositor decides

**OBS** S287 (issue 565, body): the reporter's rule is `windowrule = workspace 4 silent,^(pavucontrol)$` and the expectation is "If a workspace windowrule contains silent then matching windows should not get focus", while the observed behaviour is that "When the new window opens in a different workspace, it seems to steal it momentarily" and then hands focus back to the previous window.

**OBS** S287 (log excerpt in the issue): the compositor prints "Tried to set workspace silent rule to a nofocus window!" - both the rule and the focus decision are the compositor's, and their disagreement is visible only in its log.

**OBS** S287 (maintainer reply, Aug 2022): "fixed in b09f157" - the issue is closed, and it predates the 0.56 line by years.

**OBS** S288 (hyprland-protocols README, finished protocols): the protocol is listed as "for grabbing input focus, primarily for complex context menus", and the README gives the reason the set exists at all - "we have to maintain a set of protocols Hyprland uses" - because wayland-protocols is slow to change and does not admit Hyprland-specific work.

**INF** Two layers, two owners. The protocol lets a *client* narrow focus over surfaces it already owns and hands the pick back to the compositor; the rule layer lets the *config* constrain the compositor's choice over windows the client never names. Issue 565 is the rule layer failing on its own terms, and it shows why a client cannot get a grab through rules: the rule's subject is a window, the grab's subject is a set of surfaces. `Basis:` S283, S284, S287.

**UNK** Whether 0.56.2 still exhibits the momentary steal of #565. The record is from 2022 against an unnamed revision, and this round measured no focus transition (no input was injected).

**INF** The lane holds no focus-rule knowledge either. `grep -rli 'focus_grab\|focus-grab\|focus grab' corpus PROVINCE.md SKILL.md tools` exits 1 at base; `window-rule-effects-getprop.md` and `workspace-rules-r27.md` contain no `focus` line, and `rule-attribution-r24.md`'s only hit is a block rule named `jetbrains-focus`. This section is a pointer to the tracker record, not a restatement of held rule semantics.

## §6 The decision table

| question | where the answer lives | state |
|---|---|---|
| What can a client ask for? | S283: two interfaces, five requests, one event (§1) | OBS |
| When does a grab start, and when does it end? | S283 `commit` text; S284 `commit`, `start`, `finish` (§1-§2) | OBS |
| What ends an active grab? | S284's seat-grab callback into `finish(true)`; S283's "implementation-defined criteria" (§2) | OBS for the branches, UNK for the criteria |
| Is the whitelist a rule or a seat grab? | S284: a `CSeatGrab` with keyboard and pointer, installed on the seat (§2) | INF |
| Does this host advertise it? | S289: one advert, version 1, latest session (§3) | OBS |
| Does the portal use it? | S286 and S289: logged, not bound, no other line (§3) | OBS |
| Who binds it on this host? | nowhere in the receipts | UNK |
| What must a client do between `add_surface` and `commit`? | S285: batch in `pendingAdditions`, then `sync()` commits (§4) | OBS |
| What does a client do on `cleared`? | S285: `active = false`, emit `cleared` (§4) | OBS |
| How is ordinary window focus decided instead? | S287 plus the held rule entries (§5) | INF, and UNK for the current release |
| Is the protocol part of wayland-protocols? | S288: Hyprland maintains its own set (§5) | OBS |
| Is there a version above 1? | S283: both interfaces declare `version="1"` (§1) | OBS |

## §7 What this does not license

- No live grab was exercised: no client was run and no input was injected, so "a grab works on this host" is not a measured claim. The advert (§3) and the code (§2) are.
- The census is one host, one day, two portal sessions, and the first of them is a slice (§3). Re-run the census; never reuse the counts.
- Issue #565 is a 2022 record. It supports "the rule layer decides focus and can be wrong", not any 0.56.2 behaviour.
- `CSeatGrab`'s routing is unread here (§2 UNK): the entry states what the protocol promises an outside event does, not how the seat implements it.
- Nothing here says the protocol is a security boundary. No receipt gates it by client identity, and no malicious or racing client was tested.
- The portal's non-use (§3) is a statement about v1.4.1's `PortalManager.cpp` and this journal, not about later releases.
- The staged `focus-control-surfaces-r28` section 3 (localized documentation channel) is outside PROVINCE.md and is not a source here; the entry rests only on the rows above.
