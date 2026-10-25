# ExecSrcFocusGrab — compositor-side facts: Hyprland focus-grab

Scope: what the compositor's implementation and the protocol XML actually say. Every quote below is a verbatim
fragment of the named line (leading indentation trimmed), verified by `verify.py` in this directory, which prints
the line number, the word count and the file sha256 for each row.

Files (staged receipts, re-fetched 2026-10-25 and compared byte-for-byte):

| file | sha256 | source |
|---|---|---|
| `focus-grab-v1.xml` | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` | `https://raw.githubusercontent.com/hyprwm/hyprland-protocols/cd1aba6bd78775825eb230b3a4274c48b6705eb7/protocols/hyprland-focus-grab-v1.xml` |
| `Hyprland-FocusGrab.cpp` | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/FocusGrab.cpp` |
| `Hyprland-FocusGrab.hpp` | `dce47251853f8d95eeec0eb357665efdceccd52b111e633c56412e5c55103421` | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/FocusGrab.hpp` |

## Facts

| fact | quote | file:line | sha256 of file |
|---|---|---|---|
| protocol purpose: a client can limit input focus to a set of surfaces | `This protocol allows clients to limit input focus to a specific set` | focus-grab-v1.xml:34 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| the limiter's removal is reported back to the client | `of surfaces and receive a notification when the limiter is removed as` | focus-grab-v1.xml:35 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| manager interface exists at version 1 (one interface, one version) | `<interface name="hyprland_focus_grab_manager_v1" version="1">` | focus-grab-v1.xml:39 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| manager request `create_grab` creates a grab object | `Create a surface grab object.` | focus-grab-v1.xml:46 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| destroying the manager leaves existing grabs alive | `This doesn't destroy existing focus grab objects.` | focus-grab-v1.xml:55 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| grab interface exists at version 1 | `<interface name="hyprland_focus_grab_v1" version="1">` | focus-grab-v1.xml:60 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| the grab is a whitelist of surfaces | `This interface restricts input focus to a specified whitelist of` | focus-grab-v1.xml:62 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| the restriction holds while the object exists and has at least one committed surface | `surfaces as long as the focus grab object exists and has at least` | focus-grab-v1.xml:63 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| (verbatim typo in the source) committed surfaces | `one comitted surface.` | focus-grab-v1.xml:64 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| mouse and touch inside a whitelisted surface are passed normally | `Mouse and touch events inside a whitelisted surface will be passed` | focus-grab-v1.xml:66 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| mouse/touch outside any whitelisted surface clears the grab | `to the surface normally, while events outside of a whitelisted surface` | focus-grab-v1.xml:67 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| the clearing event is a grab clear; keyboard events still go to the client | `will clear the grab object. Keyboard events will be passed to the client` | focus-grab-v1.xml:68 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| keyboard enters a compositor-picked whitelisted surface | `wl_keyboard::enter event if a whitelisted surface is not already entered.` | focus-grab-v1.xml:70 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| the clearing criteria are implementation-defined | `Upon meeting implementation-defined criteria usually meaning a mouse or` | focus-grab-v1.xml:72 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| the usual criterion is mouse/touch input outside any whitelisted surface | `touch input outside of any whitelisted surfaces, the compositor will` | focus-grab-v1.xml:73 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| clearing = whitelist emptied, grab inert, `cleared` sent | `clear the whitelist, rendering the grab inert and sending the cleared` | focus-grab-v1.xml:74 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| another focus grab or similar action also clears | `event. The same will happen if another focus grab or similar action` | focus-grab-v1.xml:75 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| the compositor decides when | `is started at the compositor's discretion.` | focus-grab-v1.xml:76 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| `add_surface`: destroying the surface equals `remove_surface` | `Add a surface to the whitelist. Destroying the surface is treated the` | focus-grab-v1.xml:81 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| `add_surface`: duplicate additions are ignored | `same as an explicit call to remove_surface and duplicate additions are` | focus-grab-v1.xml:82 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| `add_surface` takes effect only at `commit` | `Does not take effect until commit is called.` | focus-grab-v1.xml:85 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| `remove_surface`: destroying the surface equals an explicit call | `the same as an explicit call to this function.` | focus-grab-v1.xml:94 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| removing the keyboard-entered surface re-enters another on commit | `keyboard, another surface will be entered on commit.` | focus-grab-v1.xml:97 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| `remove_surface` takes effect only at `commit` | `Does not take effect until commit is called.` | focus-grab-v1.xml:99 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| `commit` applies pending whitelist changes | `Commit pending changes to the surface whitelist.` | focus-grab-v1.xml:107 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| empty → non-empty starts the grab | `If the list previously had no entries and now has at least one, the grab` | focus-grab-v1.xml:109 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| non-empty → empty makes the grab inert | `will start. If it previously had entries and now has none, the grab will` | focus-grab-v1.xml:110 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| inert, not destroyed | `become inert.` | focus-grab-v1.xml:111 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| `destroy` removes the grab if active | `Destroy the grab object and remove the grab if active.` | focus-grab-v1.xml:117 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| `cleared` is sent when the compositor cancels an active grab | `Sent when an active grab is cancelled by the compositor,` | focus-grab-v1.xml:123 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| `cleared` is sent regardless of cause | `regardless of cause.` | focus-grab-v1.xml:124 | `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` |
| the grab redirects keyboard input | `m_grab->m_keyboard = true;` | Hyprland-FocusGrab.cpp:20 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| the grab redirects pointer input | `m_grab->m_pointer  = true;` | Hyprland-FocusGrab.cpp:21 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| when the compositor ends the seat grab, the focus grab finishes and sends `cleared` | `m_grab->setCallback([this]() { finish(true); });` | Hyprland-FocusGrab.cpp:22 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| `destroy` request and resource destruction both drop the grab object | `m_resource->setDestroy([this](CHyprlandFocusGrabV1* pMgr) { PROTO::focusGrab->destroyGrab(this); });` | Hyprland-FocusGrab.cpp:24 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| `add_surface` request handler | `m_resource->setAddSurface([this](CHyprlandFocusGrabV1* pMgr, wl_resource* surface) { addSurface(CWLSurfaceResource::fromResource(surface)); });` | Hyprland-FocusGrab.cpp:26 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| `commit` request handler | `m_resource->setCommit([this](CHyprlandFocusGrabV1* pMgr) { commit(); });` | Hyprland-FocusGrab.cpp:28 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| the grab destructor finishes without sending `cleared` | `finish(false);` | Hyprland-FocusGrab.cpp:32 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| the seat grab is installed once, only on the inactive→active edge | `if (!m_grabActive) {` | Hyprland-FocusGrab.cpp:48 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| the focus grab becomes the seat's grab | `g_pSeatManager->setGrab(m_grab);` | Hyprland-FocusGrab.cpp:50 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| start re-runs pointer motion so surfaces under the cursor are focused | `g_pInputManager->simulateMouseMovement();` | Hyprland-FocusGrab.cpp:54 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| start refocuses the keyboard | `refocusKeyboard();` | Hyprland-FocusGrab.cpp:55 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| finish is a no-op unless the grab is active (so `cleared` is only ever sent for an active grab) | `if (m_grabActive) {` | Hyprland-FocusGrab.cpp:59 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| finish releases the seat grab only if it is still ours (a replacement grab is left installed) | `if (g_pSeatManager->m_seatGrab == m_grab)` | Hyprland-FocusGrab.cpp:62 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| finish empties the seat grab's surface list | `m_grab->clear();` | Hyprland-FocusGrab.cpp:65 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| finish discards the whitelist map | `m_surfaces.clear();` | Hyprland-FocusGrab.cpp:66 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| the `cleared` event is sent only when finish was asked to | `if (sendCleared)` | Hyprland-FocusGrab.cpp:68 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| the event itself | `m_resource->sendCleared();` | Hyprland-FocusGrab.cpp:69 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| `add_surface` of an already-listed surface is dropped (duplicate ignored) | `if (iter == m_surfaces.end())` | Hyprland-FocusGrab.cpp:75 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| a new whitelist entry is created in the pending-addition state | `m_surfaces.emplace(surface, makeUnique<CFocusGrabSurfaceState>(this, surface));` | Hyprland-FocusGrab.cpp:76 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| `remove_surface` on a still-pending surface erases it immediately | `if (iter->second->m_state == CFocusGrabSurfaceState::PendingAddition)` | Hyprland-FocusGrab.cpp:82 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| `remove_surface` on a committed surface only marks it pending-removal | `iter->second->m_state = CFocusGrabSurfaceState::PendingRemoval;` | Hyprland-FocusGrab.cpp:85 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| surface destruction removes it and commits with `removeOnly` | `commit(true);` | Hyprland-FocusGrab.cpp:91 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| keyboard focus stays put if it is already on a committed surface | `if (keyboardSurface && isSurfaceCommitted(keyboardSurface.lock()))` | Hyprland-FocusGrab.cpp:96 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| otherwise the first committed surface in `unordered_map` iteration order (unspecified) is chosen | `if (state->m_state == CFocusGrabSurfaceState::Committed) {` | Hyprland-FocusGrab.cpp:101 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| focus is moved directly, bypassing normal focus rules | `Desktop::focusState()->rawSurfaceFocus(surface);` | Hyprland-FocusGrab.cpp:108 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| refocus with no committed surface is logged as an error | `LOGM(Log::ERR, "CFocusGrab::refocusKeyboard called with no committed surfaces. This should never happen.");` | Hyprland-FocusGrab.cpp:110 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| commit drops pending removals from the seat grab | `m_grab->remove(iter->first.lock());` | Hyprland-FocusGrab.cpp:119 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| commit promotes pending additions into the seat grab | `m_grab->add(iter->first.lock());` | Hyprland-FocusGrab.cpp:126 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| commit acts only when the whitelist actually changed | `if (surfacesChanged) {` | Hyprland-FocusGrab.cpp:137 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| changed with at least one committed surface → grab starts | `start();` | Hyprland-FocusGrab.cpp:139 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| changed with none committed → finish with `cleared` (this is the empty-whitelist commit) | `finish(true);` | Hyprland-FocusGrab.cpp:141 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| destroying the manager only drops the manager object | `std::erase_if(m_managers, [&](const auto& other) { return other->resource() == res; });` | Hyprland-FocusGrab.cpp:158 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| destroying a grab drops it from the protocol's grab list | `std::erase_if(m_grabs, [&](const auto& other) { return other.get() == grab; });` | Hyprland-FocusGrab.cpp:162 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| `create_grab` allocates one grab object per request, at the manager's version | `m_grabs.push_back(makeUnique<CFocusGrab>(makeShared<CHyprlandFocusGrabV1>(pMgr->client(), pMgr->version(), id)));` | Hyprland-FocusGrab.cpp:166 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| allocation failure is reported as `noMemory` | `pMgr->noMemory();` | Hyprland-FocusGrab.cpp:170 | `53b762f7149bf1c3105ec1da2137d02cc7bece90043d9a2ce253a784b092aff1` |
| the whitelist is a map from surface to per-surface state | `std::unordered_map<WP<CWLSurfaceResource>, UP<CFocusGrabSurfaceState>> m_surfaces;` | Hyprland-FocusGrab.hpp:51 | `dce47251853f8d95eeec0eb357665efdceccd52b111e633c56412e5c55103421` |
| three per-surface states, new entries default to pending addition | `} m_state = PendingAddition;` | Hyprland-FocusGrab.hpp:24 | `dce47251853f8d95eeec0eb357665efdceccd52b111e633c56412e5c55103421` |
| each focus grab owns exactly one seat grab | `SP<CSeatGrab>                                                          m_grab;` | Hyprland-FocusGrab.hpp:52 | `dce47251853f8d95eeec0eb357665efdceccd52b111e633c56412e5c55103421` |
| grab objects are held in a vector: several may exist at once | `std::vector<UP<CFocusGrab>>                  m_grabs;` | Hyprland-FocusGrab.hpp:71 | `dce47251853f8d95eeec0eb357665efdceccd52b111e633c56412e5c55103421` |
| managers are held in a vector | `std::vector<UP<CHyprlandFocusGrabManagerV1>> m_managers;` | Hyprland-FocusGrab.hpp:70 | `dce47251853f8d95eeec0eb357665efdceccd52b111e633c56412e5c55103421` |
| the active flag gates installation and `cleared` | `bool                                                                   m_grabActive = false;` | Hyprland-FocusGrab.hpp:54 | `dce47251853f8d95eeec0eb357665efdceccd52b111e633c56412e5c55103421` |

## Behaviour summary (what the rows above compose)

- Interfaces and versions: `hyprland_focus_grab_manager_v1` v1 (`create_grab`, `destroy`) and `hyprland_focus_grab_v1`
  v1 (`add_surface`, `remove_surface`, `commit`, `destroy`) plus the single event `cleared`. No other request or event exists.
- Whitelist storage: a `std::unordered_map` keyed by weak surface pointer, each value carrying one of
  `PendingAddition` / `PendingRemoval` / `Committed` (hpp:21-24, :51). The seat grab keeps its own list, changed only
  from `commit` (cpp:119, :126).
- `create_grab` allocates one grab per request; failure yields `noMemory` (cpp:166, :170). Destroying the manager
  does not destroy grabs (xml:55, cpp:158).
- `add_surface` ignores duplicates (cpp:75) and only queues (xml:85). `remove_surface` erases a still-pending surface
  at once, but a committed surface only becomes `PendingRemoval` until the next `commit` (cpp:82, :85, xml:99).
- `commit` is the only transition point: it applies removals and promotions, then if anything changed it either
  starts the grab (≥1 committed surface) or finishes it with `cleared` (0 committed surfaces) (cpp:113-143).
- Empty-whitelist `commit`: the "changed and nothing committed" path calls `finish(true)` (cpp:141), which is
  guarded by `m_grabActive` (cpp:59) — so `cleared` is emitted only if the grab had actually started.
- `cleared` timing: the focus grab finishes with `cleared` when its seat-grab callback fires (cpp:22 → `finish(true)`;
  what invokes that callback is `CSeatGrab`'s business and is not in this receipt [INFERENCE: the callback marks the
  compositor ending/replacing the grab]), when a commit empties the whitelist (cpp:141), or when a surface destroy
  commits a remove-only change that leaves nothing committed (cpp:91). Explicit `destroy` does NOT send it
  (destructor → `finish(false)`, cpp:32).
- Input redirected: keyboard and pointer are set on the seat grab (cpp:20-21). Touch is never mentioned in either
  file (`grep -c touch` = 0/0). The XML promises mouse *and* touch handling (xml:66-68); that promise is not
  implemented in this file.
- Focus of surfaces outside the whitelist: this file never unfocuses a surface; it only moves keyboard focus into the
  whitelist via `rawSurfaceFocus` on start (cpp:108) and leaves focus alone if it is already on a committed surface
  (cpp:96). What happens to the previously focused surface is not visible here.
- Interaction with other grabs: exactly one `CSeatGrab` is installed per focus grab (`g_pSeatManager->setGrab`,
  cpp:50); the seat grab's callback ends the focus grab with `cleared` (cpp:22) [INFERENCE: the callback marks the
  compositor replacing or ending the grab; the trigger is in `CSeatGrab`, not this receipt]. `finish` clears the
  seat grab only if it is still this grab's (cpp:62), so a successor grab is not uninstalled by the predecessor's
  teardown.

## What the source does NOT say

1. **Touch.** Neither file contains the token `touch` (verified: `grep -c touch` → 0 and 0). The XML says mouse and
   touch outside the whitelist clear the grab (xml:66-68); the implementation only sets keyboard and pointer on the
   seat grab (cpp:20-21). Nothing here says touch input is redirected or that a touch clears the grab.
2. **Where the "outside click" detection lives.** No code in `FocusGrab.cpp` inspects pointer or touch events. The
   only clear paths are the seat-grab callback (cpp:22) and the commit/empty path (cpp:141); the outside-input rule
   is delegated to `CSeatGrab` / the input manager, which are not in this receipt.
3. **What happens to focus of non-whitelisted surfaces.** There is no per-surface unfocus, no "restore previous
   focus" on clear (`finish` just clears the map, cpp:65-66), and no statement about clients that lose keyboard
   focus. The XML only says keyboard goes to the client and a whitelisted surface is entered (xml:68-70).
4. **The never-started case.** The XML does not say what `commit` on an empty list does when the grab never started;
   the code answers it only implicitly through the `m_grabActive` guard (cpp:59): no `cleared` is sent.
5. **No-op commits.** Neither source says whether a `commit` with no pending changes is observable; the code makes it
   silent (`if (surfacesChanged)`, cpp:137).
6. **Multiple simultaneous grabs.** `m_grabs` is a vector and several grab objects may exist, but the file does not
   define precedence between them: `start()` simply installs the seat grab (cpp:50), and the loser learns only via
   the callback (cpp:22). No ordering, no queuing, no error.
7. **Rule-level / config counterpart.** Nothing in either file mentions Hyprland rules, window rules, dispatchers,
   `hyprctl`, or any user-facing configuration. That counterpart must come from elsewhere (not this receipt).
8. **Advertisement and host state.** The XML declares version 1 only; neither file says what the compositor
   advertises on the registry, which clients bind it, or which portal/desktop is running. (The host census is a
   different receipt: `xdph-journal.txt`.)
9. **Client obligations.** Neither source states what a client must do with `cleared` (re-acquire, release surfaces,
   ignore), nor whether a grab can be re-armed on the same object after `cleared`.
10. **Error cases.** The XML declares no protocol error for `add_surface` with a foreign/unknown surface or for a
    second `commit` after `cleared`; the code has no such check either (`addSurface` accepts any surface, cpp:73-77).
11. **Surface destruction during `PendingAddition`.** The XML says destroying a surface equals `remove_surface`
    (xml:81, :93-94); the code routes it through `eraseSurface` → `commit(true)` (cpp:89-92), but nothing states what
    a `cleared` is when the destroyed surface was the only committed one beyond the generic commit path.
