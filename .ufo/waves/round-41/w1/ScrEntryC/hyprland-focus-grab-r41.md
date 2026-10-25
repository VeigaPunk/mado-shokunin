# Focus grab: the protocol surface, its advertisement on this host, one client, the rule-level counterpart

source: S283 - hyprland-protocols `hyprland_focus_grab_v1.xml` (receipt .ufo/waves/round-41/fetch/focus-grab-v1.xml) - both interfaces, their requests and the `cleared` event - hyprland-protocols @ cd1aba6bd78775825eb230b3a4274c48b6705eb7
source: S284 - Hyprland v0.56.2 `src/protocols/FocusGrab.cpp` (receipt .ufo/waves/round-41/fetch/Hyprland-FocusGrab.cpp) - `CFocusGrab` construction, `start`, `finish`, `commit` - Hyprland @ efb50993780079460b0cbed1363e2166a2de1d9f
source: S285 - quickshell `src/wayland/hyprland/focus_grab/grab.cpp` (receipt .ufo/waves/round-41/fetch/quickshell-grab.cpp) - `addWindow`, `sync`, the `cleared` handler - quickshell @ 9b0f339b19057f4731bf3b48293307d7ef241671
source: S286 - xdg-desktop-portal-hyprland v1.4.1 `src/core/PortalManager.cpp` (receipt .ufo/waves/round-41/fetch/xdph-PortalManager.cpp) - `CPortalManager::onGlobal`, the registry handler - tag v1.4.1 (the installed release)
source: S287 - hyprwm/Hyprland issue #565 (receipt .ufo/waves/round-41/fetch/issue-565.html) - issue body: the rule, its expected behaviour, the reporter's log - createdAt 2022-08-23, state CLOSED reason COMPLETED, replies dated 2022-08-25
source: S288 - hyprland-protocols `README.md` (receipt .ufo/waves/round-41/fetch/protocols-README.md) - the finished-protocols list - hyprland-protocols @ cd1aba6bd78775825eb230b3a4274c48b6705eb7
source: S289 - own-work: saved user journal of `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` (receipt .ufo/waves/round-41/fetch/xdph-journal.txt, 153 lines) - the advert lines - captured 2026-10-25
verified-at: 2026-10-25
recheck: 90d - re-pull the XML and README at the pinned hyprland-protocols commit, the portal source at the installed tag, and re-run the journal verb (counts are one host, one date)

Lane: mado-shokunin. Round: 41 (C2 coverage). Host Hyprland 0.56.2 at `efb5099…`, xdg-desktop-portal-hyprland v1.4.1 installed. Read-only: source bytes read, one saved journal parsed; this seat ran no compositor, portal or Wayland verb.

ground: the focus layer as a protocol surface - what a client can ask this compositor for, what this host advertises, how one client uses it, and the rule-level counterpart; what none of them licenses is the last section.

## §1 The protocol surface

**OBS** S283 (`focus-grab-v1.xml:39-124`): the manager is v1 with `create_grab` and `destroy`; the grab object is v1, reached through `add_surface`, `remove_surface`, `commit` and `destroy`, reports one event `cleared`, and states its job as "This interface restricts input focus to a specified whitelist of surfaces".

**OBS** S288 (`protocols-README.md:17`): the protocols repository lists the protocol among its finished ones with the purpose "for grabbing input focus, primarily for complex context menus".

**INF** Basis: S283 `:60-77` (the grab restricts focus to a whitelist and is cleared on criteria the XML calls implementation-defined and does not name): the protocol is a client's ask with a server-chosen ending, so a client can request a whitelist but cannot name the condition under which it ends.

## §2 The compositor side

**OBS** S284 (`Hyprland-FocusGrab.cpp:18-21`): the compositor backs the grab with a seat grab, enabling keyboard capture with `m_grab->m_keyboard = true;` and pointer capture on the line after it.

**INF** Basis: S284 `:58` (`finish(bool sendCleared)`), `:31` (the destructor passes `false`), `:22` and `:141` (the seat-grab callback and a commit leaving no committed surface pass `true`): `cleared` is not sent when the client destroys the grab object, and is sent when the seat-grab callback or an emptying commit ends an active grab.

## §3 The advertisement on this host

**OBS** S286 (`xdph-PortalManager.cpp:88`, `:90-122`): `onGlobal` logs every advertised global with `Got interface: {} (ver {})` and then binds a fixed name set - screencopy, global shortcuts, input capture, xdg output, toplevel export, `wl_output`, dmabuf; `grep -ci focus` over the receipt is 0.

**OBS** S289 (`xdph-journal.txt:117`): the latest session holds one advert of the manager, `Got interface: hyprland_focus_grab_manager_v1 (ver 1)`, at 2026-10-25T13:36:24-03:00 under pid 1952.

journal sessions=2 adverts=78 interfaces=63 focus_grab=1

**INF** Basis: S286 (`grep -ci focus` = 0) and S289 (one advert, no bind line in the receipt): the advert says the compositor offers this global to this connection; it says nothing about the portal or any other program using it.

## §4 One real client

**OBS** S285 (`quickshell-grab.cpp:78`, `:74-90`, `:98`): the client adds a surface, commits, and keeps its own `active` flag on the server's promise - "the protocol will always send cleared() when the grab is deactivated," - its `cleared` handler setting `active = false`.

**INF** Basis: S285 `:74-90` (commit only when `commitRequired`, activation keyed on pending additions) and S284 `:137-142` (the compositor acts on commit only when a surface changed): a client that commits an empty change set neither starts nor re-activates the grab.

## §5 The rule-level counterpart

**OBS** S287 (`issue-565.html:706`, `:656`, `:659`): the counterpart is a window rule, `windowrule = workspace 4 silent,^(pavucontrol)$`, and the reporter's log of the rule path shows the engine refusing focus with "Tried to set workspace silent rule to a nofocus window!".

**INF** Basis: S287 (a rule decided when the window is mapped, holding no protocol object) against S283 (a client-held object with a surface whitelist): the two are separate mechanisms - the rule decides at window creation, the grab decides while a client holds the object - and nothing in these receipts ties one to the other.

## §6 Unknowns, named

**UNK** Whether any program on this host has bound `hyprland_focus_grab_manager_v1`: the receipt holds adverts only (S289, no bind line), and no client-side log was read this round.

**UNK** The criteria the compositor uses to clear a grab: S283 `:72-76` calls them implementation-defined and names no condition, and S284 shows the seat-grab and commit paths, not the criteria.

**UNK** Whether the 2022 rule behaviour of S287 still holds at 0.56.2: the issue was opened 2022-08-23 and is closed as completed, its replies are dated 2022-08-25, and no rule was exercised on this host.

## §7 What this does not license

- Nothing about whether a grab has ever been active on this host: the receipt is adverts, with no bind and no clear line (S289).
- Nothing about input capture, input synthesis or session lock: those globals are advertised in the same session (S289) and belong to other claims.
- Nothing about 0.56.2 rule behaviour from S287: the issue states a 2022 reporter's log and expectation, not a measurement of this host.
- The census is one host, one date, one boot pair; re-run the journal verb, never reuse the counts.
