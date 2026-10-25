# Focus as a protocol surface on this host: the grab manager the compositor advertises to its portal, the protocol's promise, a client's lifecycle, and the rule-level counterpart

source: S283 - hyprland-protocols focus-grab-v1.xml (hyprland_focus_grab_v1) - protocol description, manager and grab interfaces, the cleared event - cd1aba6bd78775825eb230b3a4274c48b6705eb7
source: S284 - Hyprland src/protocols/FocusGrab.cpp - CFocusGrab: seat grab, start, finish, commit, refocusKeyboard - efb50993780079460b0cbed1363e2166a2de1d9f
source: S285 - quickshell src/wayland/hyprland/focus_grab/grab.cpp - the client FocusGrab: addWindow, sync, cleared - 9b0f339b19057f4731bf3b48293307d7ef241671
source: S286 - xdg-desktop-portal-hyprland src/core/PortalManager.cpp - CPortalManager::onGlobal, the Got interface log, the bind branches - v1.4.1
source: S287 - github.com/hyprwm/Hyprland/issues/565 - issue body, workaround rule, closure - html snapshot 2026-10-25
source: S288 - hyprland-protocols README - Finished protocols list - cd1aba6bd78775825eb230b3a4274c48b6705eb7
source: S289 - own-work: user journal of xdg-desktop-portal-hyprland - journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso - .ufo/waves/round-41/fetch/xdph-journal.txt, captured 2026-10-25
source: S290 - hyprland-protocols input-capture-v1.xml (hyprland_input_capture_manager_v1) - the input-capture bridge, for contrast with the grab - cd1aba6bd78775825eb230b3a4274c48b6705eb7
verified-at: 2026-10-25
recheck: 90d - re-pull the three protocol files at cd1aba6, FocusGrab.cpp at efb5099, quickshell grab.cpp at 9b0f339 and the issue snapshot, then re-capture the xdph journal
ground: focus as a protocol surface on this host, in four layers - the advertisement the portal logged, the protocol's promise, the compositor's implementation, one client's lifecycle - plus the rule-level counterpart; held ground not restated: wayland-protocol-boundaries-r13.md §1 (advertise, bind, behaviour are three claims), keybind-rule-semantics.md §4.3-§4.4 (rule vocabulary and the plane's declared values), xdg-portal-routing-r12.md §2 (XDPH role, descriptor level)

Lane: mado-shokunin. Round: 41.

## §1 The host first: what this compositor advertised to its portal

**OBS** S289 (own work, 2026-10-25; 153 lines, sha256 `bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7`): the unit's journal holds two portal sessions; the later one (pid 1952, from `2026-10-25T13:36:24-03:00`) logs 63 adverts over 63 distinct names, one of them `Got interface: hyprland_focus_grab_manager_v1 (ver 1)`.

journal sessions=2 adverts=78 interfaces=63 focus_grab=1

**OBS** S286 (`src/core/PortalManager.cpp:85-88`, `CPortalManager::onGlobal`): the log line `Got interface: {} (ver {})` is the first statement of the registry-global handler, before every `if (INTERFACE == ...)` bind branch. An advert therefore records a `wl_registry.global` event that reached the portal - not a bind and not a use.

**INF** Classifying those 63 names with the round-41 class table (`quality/counters/c1-r41-globals.py` docstring) gives focus-grab 1 (`hyprland_focus_grab_manager_v1` v1), input-synthesis 3 (`zwlr_virtual_pointer_manager_v1` v2, `zwp_virtual_keyboard_manager_v1` v1, `zwp_input_method_manager_v2` v1), input-capture 3 (`hyprland_input_capture_manager_v1` v1, `zwp_keyboard_shortcuts_inhibit_manager_v1` v1, `hyprland_global_shortcuts_manager_v1` v1), session-lock 2 (`ext_session_lock_manager_v1`, `hyprland_lock_notifier_v1`), idle 2, clipboard 3, capture 2, toplevel-control 4, output-control 4, sandbox 1, other 38. This is a classification of names, not capability proof: it says which surface a name belongs to, never that the portal or any other client exercised it. The four classes a reader is likely to conflate are separated here on purpose - a grab restricts focus, input-synthesis injects events, input-capture reads them, session-lock owns the screen.

**OBS** S290 (`input-capture-v1.xml:68`, the capture session's barrier request): the neighbouring class is a different protocol with a different mechanism - its session takes barriers, `Add one barrier to the current session`, a straight line on the screen edge; the file calls itself a bridge of XDG input capture (`:35`) and sends the inputs over an EIS socket (`:56`). The XML declares `hyprland_input_capture_manager_v1` at version 2 (`:38`) while this host advertises version 1 (§1), so the advertised version is what the compositor implements, not what the protocol file tops out at.

**OBS** held prior (S041, `.ufo/waves/round-13/w1/globals.json`, captured `2026-10-20T04:10:03Z` by wayland-info 1.3.0-1 against Hyprland `efb5099`): 72 records over 71 distinct names, `hyprland_focus_grab_manager_v1` among them at version 1. Re-derived this seat: every name of the journal's latest session is in that capture at the same version, and eight names are in the capture that the latest session does not hold (`wl_output`, `wl_drm`, `zwp_linux_dmabuf_v1`, `wp_color_manager_v1`, `wp_drm_lease_device_v1`, `wp_linux_drm_syncobj_manager_v1`, `ext_image_copy_capture_manager_v1`, `ext_foreign_toplevel_image_capture_source_manager_v1`); all eight appear in the journal's *earlier* session (pid 1918, 15 adverts over 8 distinct names).

**INF** `interfaces=63` is what the portal logged in that one session, not the compositor's global set. Two independent populations (S041's 71 names, the earlier session's 8) hold names this session's lines do not, and the earlier session is visibly a fragment: its 15 adverts carry neither `wl_compositor` nor `wl_seat`, which the latest session and the capture both hold, so the retained window cut it. The latest session has the same shape at its other end - its last line is an advert and it holds no `wl_output` at all, while both other populations do - so 63 is a lower bound for that session too. The grab manager is in the latest session and in the capture, so its absence from the 8-name fragment says nothing about earlier availability.

**UNK** Why the latest session's log holds 63 names and not the 71 of the capture: a cut at the end of the retained window, globals still arriving when the portal's enumeration ended (outputs may be created after the first roundtrip), or a real per-boot difference - the receipts cannot decide between them, and no further host read was made this round.

## §2 What the protocol promises

**OBS** S283 (`focus-grab-v1.xml:34`, protocol description): the protocol lets a client limit input focus to a set of surfaces and be told when the limiter is removed.

**OBS** S288 (README, Finished protocols): the grab is listed among the finished protocols as `for grabbing input focus, primarily for complex context menus` - the upstream statement of purpose, with no mechanism attached.

**OBS** S283 (`:62-76`, `hyprland_focus_grab_v1`): `This interface restricts input focus to a specified whitelist of surfaces` while the grab object exists and holds at least one committed surface; mouse and touch input inside the whitelist is delivered normally, input outside it clears the grab; a compositor-picked whitelisted surface receives `wl_keyboard::enter`; and another grab or similar action started later clears it too, at the compositor's discretion. The clearing is compositor-side and implementation-defined, not a client decision.

**OBS** S283 (`:105-112`, request `commit`): a commit that turns an empty list non-empty starts the grab and one that empties it makes it inert; `add_surface`/`remove_surface` take effect only at commit (`:85`, `:99`), and duplicate additions are ignored (`:82`). The whitelist is a committed set, not a sequence of calls.

**OBS** S283 (`:121-124`, event `cleared`): the event is sent when the compositor cancels an active grab, regardless of cause - a compositor-initiated end, not a general "grab ended" signal.

## §3 The compositor's implementation

**OBS** S284 (`Hyprland-FocusGrab.cpp:20-22`, constructor): a grab is a seat grab with both devices claimed - `m_grab->m_keyboard = true;`, `m_grab->m_pointer = true;` - and a callback `m_grab->setCallback([this]() { finish(true); });`. **INF** The whitelist is carried as the seat grab's own surface set: `commit` calls `m_grab->add` for an admitted surface (`:126`) and `m_grab->remove` for a withdrawn one (`:119`), so membership is a seat-level fact rather than a per-surface filter in the protocol code.

**OBS** S284 (`:45-56`, `start`): starting sets the grab, then `g_pInputManager->simulateMouseMovement();` and `refocusKeyboard();`. `refocusKeyboard` (`:94-111`) keeps the current keyboard surface if it is a committed member, else focuses the first committed surface through `Desktop::focusState()->rawSurfaceFocus(surface);` (`:108`), and logs an error if no committed surface exists. So a grab start can move keyboard focus and simulate a pointer motion by itself.

**OBS** S284 (`:113-142`, `commit`): pending additions become `Committed` and are added to the seat grab, pending removals are removed and erased; if the set changed, a non-empty set starts the grab and an empty one calls `finish(true)`. `finish(sendCleared)` (`:58-71`) clears the grab and the surface map and sends `cleared` only when `sendCleared` is true.

**INF** From those paths: `cleared` reaches the client on a compositor-side cancel (the seat-grab callback, `:22`) and on a commit that leaves no committed surface (`:141`), but not on explicit `destroy` or client death, because the destructor calls `finish(false)` (`:32`). A client that waits for `cleared` after destroying its own grab waits forever; one that waits for it after losing focus does not.

**UNK** How a second grab displaces an active one: the protocol leaves it to the compositor (`S283:75`), and the seat manager that would decide it (`setGrab` semantics) is not in the fetched bytes, so nothing here says which grab wins or whether the displaced one gets `cleared`.

## §4 A real client's lifecycle

**OBS** S285 (`quickshell grab.cpp:67-86`, `addWindow`/`sync`): a window's surface is added with `add_surface` and queued in `pendingAdditions`; `sync` calls `this->commit()`, and only if `pendingAdditions` was non-empty does the client set `this->active = true;` and `emit this->activated();`. The client treats "commit accepted, something was pending" as "the grab is active" - it does not wait for a compositor confirmation, because the protocol has none.

**OBS** S285 (`:78-79`, comment in `sync`): `the protocol will always send cleared() when the grab is deactivated,` even when the cause is window destruction, so the client keeps no separate bookkeeping.

**OBS** S285 (`:98-100`, `hyprland_focus_grab_v1_cleared`): the handler is exactly `this->active = false;` plus an emitted `cleared` - the client's whole deactivation path.

**INF** The client's assumption is narrower than it reads: it holds for compositor-side deactivation (the paths of §3), and it is vacuous for the client's own destroy, where the client is the actor and already knows. A second consumer that relied on `cleared` after tearing down a grab would be relying on something the compositor does not send.

## §5 The rule-level counterpart

**OBS** S287 (issue #565, opened 2022-08-23, closed as completed 2022-08-25): a new window on an inactive workspace stole focus - a notification window opened on another workspace un-fullscreened the active window. The reporter's workaround is a rule, not a protocol: a `windowrule` pinning the browser to workspace 1 with the `silent` flag. Their debug log carries the compositor's own line `Tried to set workspace silent rule to a nofocus window!`, and the rule trace above it shows a silent workspace rule matching a window by class, so the collision between a silent workspace rule and a nofocus window is something the compositor detects and logs. The maintainer said it should be fixed hastily, that a more robust solution would probably be needed, and closed it as completed.

**OBS** held (`corpus/knowledge/keybind-rule-semantics.md:189,210,225,229-232`; `corpus/knowledge/hyprctl-verification-layer.md:107`): the config plane already carries the counterpart on this host - `no_focus on` is a window-rule *dynamic* effect (`windows.conf:9`), `no_initial_focus` a static one (`webcam-overlay.conf:4`), `focus_on_activate off` (`telegram.conf:2`), `stay_focused` (davinci orphan, unsourced), and the live option `misc:focus_on_activate` reads 1. The plane also holds the silent notion the issue's workaround uses (`keybind-rule-semantics.md:145`: `movetoworkspacesilent` does not follow the window).

**INF** The two layers point in opposite directions. A rule decides, per window and from outside it, whether a new surface may take focus and where it lands (`silent`, `no_initial_focus`, `focus_on_activate off`); the grab lets a client restrict focus to its own surfaces while it is open and be told when the restriction ends. A rule is applied by the compositor at map/activation time and is invisible to the client; a grab is requested by the client and its end is reported to it.

**UNK** Which internal focus path each rule gates. The fetched bytes contain no rule applicator, so nothing here says whether `no_focus` gates window focus only or every focus assignment; a source-level answer would need the focus-state and rule-applicator files, neither of which is a receipt of this round.

## §6 What this does not license

- No capability claim: an advert is a registry event received by one portal (§1), and nothing here says the portal, quickshell or any other client created a grab on this host. The class table classifies names.
- `interfaces=63` is one session's log, not the compositor's global set, and the eight names of §1 must not be reported as withdrawn.
- Nothing about a second grab, about what the simulated pointer motion does to a real pointer, or about session-lock interaction with a grab.
- The issue (#565) is a 2022 report against a then-current build; its workaround is quoted as the reporter's rule, not as today's semantics, and its closure does not establish today's behaviour.
- One host, one date, one portal session, one protocol pin: re-capture the journal and re-pull the pins rather than reuse these counts.
- No localized documentation channel was used (PROVINCE.md's channel rule); the staged package's Japanese-channel section is not cited here.
