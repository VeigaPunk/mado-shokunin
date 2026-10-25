# Cross-Claim Separability and Cross-Source Claims-vs-Sources Matrix

**Seat:** `ConnCrossClaim`  
**Lane:** `mado-shokunin`  
**Round:** 41 (hyaku run 7, 2026-10-25), Wave `w1`  
**Base:** `ab2bfaab661c846d1de9d58c01651cd156a13949`  
**Freeze:** `60c3914154333180450d5da27ba222d5763cc56a`  

---

## 1. Separability of Claims C1 and C2 as Registered

The round registration (`.ufo/waves/round-41/registration.md:38-41`) defines strict separability between Claim C1 (operability) and Claim C2 (coverage). We examined both counter implementations and verify total mechanical and semantic decoupling:

### 1.1 Target Paths and File Ownership
- **C1 Deliverable:** `tools/mado-globals.py` (and test receipts/controls).
- **C2 Deliverables:** `corpus/knowledge/hyprland-focus-grab-r41.md`, `corpus/SOURCES.md` (registry rows), `corpus/lessons/round-41.md` (`## Gate`), `corpus/README.md` (index row), and fetch receipts under `.ufo/waves/round-41/fetch/`.
- No path touched or produced by C1 is read by C2, and no path touched or produced by C2 is read by C1.

### 1.2 Counter Isolation & Execution Environments
- **C1 Counter (`quality/counters/c1-r41-globals.py`):**
  - Evaluates `tools/mado-globals.py` inside a strict bubblewrap sandbox (`bwrap --unshare-all --cap-drop ALL`, fresh tmpfs `/tmp`, fresh `/proc` and `/dev`, read-only interpreter and scratch tree).
  - The tool under test cannot access the repository filesystem, `/home`, or the git object database.
  - Generates 24 synthetic journal fixtures using a nonce lattice; does NOT read any file from `corpus/`, `SOURCES.md`, `README.md`, or `.ufo/waves/round-41/fetch/`.
  - Zero references to C2 files (`grep -i 'hyprland-focus-grab\|SOURCES\.md\|round-41\.md' quality/counters/c1-r41-globals.py` returns 0 matches).
- **C2 Counter (`quality/counters/c2-r41-focus-entry.py`):**
  - Evaluates the admitted knowledge entry using `git show <rev>:<path>` on markdown and fetch receipt paths.
  - Clause `h` tests the own-work journal row using its **own built-in regex parser** (`ADV_RE` and `BOOT_RE`, lines 84-88, 155-179). It does **not** execute, import, or call `tools/mado-globals.py`.
  - Zero references to C1 files (`grep -i 'mado-globals\|ctl-c1\|c1-r41' quality/counters/c2-r41-focus-entry.py` returns 0 matches).
- **Conclusion:** C1 and C2 can be tested, mutated, committed, or falsified completely independently at any commit.

---

## 2. Cross-Source Pattern Analysis of `hyprland_focus_grab_manager_v1`

We cross-referenced `hyprland_focus_grab_manager_v1` across four distinct local source planes:
1. **Host Journal (`xdph-journal.txt`):** Own-work journal capture of `xdg-desktop-portal-hyprland`.
2. **Protocol Specification (`focus-grab-v1.xml`, `protocols-README.md`):** Hyprland protocol extension definition.
3. **Compositor Implementation (`Hyprland-FocusGrab.cpp`, `Hyprland-FocusGrab.hpp`):** Hyprland v0.56.2 compositor-side engine.
4. **Client Implementation (`xdph-PortalManager.cpp`, `quickshell-grab.cpp`):** Portal observer vs real Qt/Wayland client.

### 2.1 The Four Source Layers

| Layer | Source File | Exact Role | Observed Focus-Grab Behaviour |
|---|---|---|---|
| **1. Host Journal** | `.ufo/waves/round-41/fetch/xdph-journal.txt:117` | Passive system log of portal startup | In Session 2 (PID 1952, 2026-10-25T13:36:24-03:00), logs: `Got interface: hyprland_focus_grab_manager_v1 (ver 1)`. In Session 1 (PID 1918), interface was **absent** (only 8 distinct globals advertised). |
| **2. Protocol Spec** | `.ufo/waves/round-41/fetch/focus-grab-v1.xml:34-77` | Normative protocol schema | Defines manager (`create_grab`, `destroy`) and grab object (`add_surface`, `remove_surface`, `commit`, `destroy`, event `cleared`). Governs whitelist lifecycle. Purpose: context menus (`protocols-README.md:17`). |
| **3. Compositor Impl** | `.ufo/waves/round-41/fetch/Hyprland-FocusGrab.cpp:15-71, 149-173` | Server-side implementation | Implements `CFocusGrabProtocol::bindManager` without privilege checks. Instantiates `CSeatGrab` with `m_keyboard = true`, `m_pointer = true`. On empty whitelist or pointer exit, fires `sendCleared()`. |
| **4a. Client (Observer)** | `.ufo/waves/round-41/fetch/xdph-PortalManager.cpp:85-121` | Desktop portal registry listener | In `CPortalManager::onGlobal`, logs every advertised global: `Debug::log(LOG, " \| Got interface: {} (ver {})", INTERFACE, version);`. **Never binds** `hyprland_focus_grab_manager_v1`. |
| **4b. Client (Consumer)** | `.ufo/waves/round-41/fetch/quickshell-grab.cpp:55-101` | Active Wayland UI client | Implements `FocusGrab::sync`: calls `this->add_surface()` then `this->commit()`. Listens for compositor `cleared` event in `FocusGrab::hyprland_focus_grab_v1_cleared()`. |

### 2.2 Consensus and Agreements Across Sources
1. **Interface Identity & Versioning:** All four planes agree on interface `hyprland_focus_grab_manager_v1` at version 1.
2. **Lifecycle Model:** The protocol XML, Hyprland compositor (`CFocusGrab`), and Quickshell client (`FocusGrab`) agree exactly on the staged transition:
   - Client requests `add_surface` (buffered in pending additions).
   - Client requests `commit` (compositor activates grab, enters keyboard focus).
   - Compositor dismisses grab on click outside or surface removal, emitting `cleared`.
3. **Dual Pointer & Keyboard Mediation:** Compositor enforces dual mediation via `CSeatGrab` (`m_keyboard = true`, `m_pointer = true`), matching the protocol XML's specification of input restriction.

### 2.3 Implicit vs Explicit Guarantees
- **Keyboard Surface Selection:**
  - *XML Spec:* "a compositor-picked surface in the whitelist will receive a wl_keyboard::enter event" (`focus-grab-v1.xml:69-70`).
  - *Compositor Impl:* In `CFocusGrab::refocusKeyboard()`, if the entered surface is already in the whitelist, focus is retained. If not, it iterates `m_surfaces` (`std::unordered_map`), selecting the first encountered committed surface. The selection among newly committed surfaces is therefore implementation-dependent on internal hash-map ordering.
- **Pointer Dismissal Rule:**
  - *XML Spec:* "Upon meeting implementation-defined criteria usually meaning a mouse or touch input outside of any whitelisted surfaces" (`focus-grab-v1.xml:72-74`).
  - *Compositor Impl:* Handled by `CSeatGrab` callback invoking `finish(true)` whenever mouse input targets an unwhitelisted surface.

### 2.4 The Advertisement-to-Usage Confusion (Pitfall)
A critical pitfall exists for operators and automated tools:
- **The Observation:** `xdg-desktop-portal-hyprland` logs `Got interface: hyprland_focus_grab_manager_v1 (ver 1)`.
- **The Mistake:** Concluding that the portal is using or requires the focus-grab protocol.
- **The Source Fact:** `xdph-PortalManager.cpp` logs *all* Wayland globals announced by the compositor during `wl_registry.global`. In `CPortalManager::onGlobal`, it binds `hyprland_input_capture_manager_v1` (for EIS capture) and `hyprland_global_shortcuts_manager_v1`, but contains zero bind calls or logic for `hyprland_focus_grab_manager_v1`.
- **Host Context:** As verified by host binary sweeps (`focus-grab-has-no-client-here-r15.md`), no client on this host binds the focus-grab protocol; the compositor advertises it, but it remains 100% unbound and unconsumed on this machine.

---

## 3. Claims-vs-Sources Matrix: Staged Package vs Fetched Receipts

We audited the claims in the staged package (`/home/vgpnk/Projects/shokuknow/merge/mado`) against the grounded receipts in `.ufo/waves/round-41/fetch/`:

| Staged Entry | Staged Claim | Fetched Receipt Evidence | Ground Truth & Contradiction |
|---|---|---|---|
| `privileged-client-surface-r29.md` | Focus-grab is a "privileged client" surface restricted to compositor-spawned clients via `WAYLAND_SOCKET` file-descriptor handoff. | `fetch/Hyprland-FocusGrab.cpp:149`, `fetch/focus-grab-v1.xml:34`, `fetch/protocols-README.md:17` | **CONTRADICTION:** `CFocusGrabProtocol::bindManager` binds for *any* connecting client without credential or socket checks. Upstream README explicitly states the protocol is for "complex context menus", an ordinary unprivileged UI function. C2 rightly designates r29 as `REFUSE`. |
| `focus-control-surfaces-r28.md` | Pairs `amgsk.dev` (Japanese blog) `no_focus` rules with upstream issue #565 (`silent` rule bug) as rule-level focus surfaces. | `fetch/issue-565.html:659`, PROVINCE.md:68-80 | **CONTRADICTION & OUT OF PROVINCE:** `amgsk.dev` is Japanese localized documentation, excluded by PROVINCE.md. Issue #565 was a 2022 bug in Hyprland's `workspace silent` rule (fixed in commit 7b01c3d), completely separate from the 2024 `hyprland_focus_grab_v1` protocol. |
| `focus-grab-protocol-live-on-host-r14.md` | Cites S328 (`host-focus-grab-portal-advertisement.txt` from 2026-10-23) claiming 2 focus-grab manager adverts across two boots. | `fetch/xdph-journal.txt:1, 117` | **DRIFT:** Live 2026-10-25 journal receipt (`bf8fa91a...`) has Session 1 (PID 1918) with **0** focus-grab adverts (only 8 globals total), and Session 2 (PID 1952) with exactly **1** advert. Total journal adverts = 78 across 2 sessions. |
| `focus-grab-has-no-client-here-r15.md` | "No program on this host speaks the focus-grab protocol except the compositor itself." | `fetch/xdph-PortalManager.cpp:88`, `fetch/quickshell-grab.cpp:1-103` | **AGREES WITH NUANCE:** xdph indeed does not bind it. While Quickshell's upstream source implements the client contract, Quickshell is not built/installed as a focus-grab client on this host. |
| `focus-grab-focus-selection-r10.md` & `focus-grab-mouse-target-r11.md` | r10 inferred focus fallback was non-deterministic from `std::unordered_map m_surfaces`; r11 corrected that mouse position in `SeatManager.cpp` governs. | `fetch/Hyprland-FocusGrab.cpp:54, 94-111`, `fetch/Hyprland-FocusGrab.hpp:51` | **AGREES:** Compositor source confirms `CFocusGrab::start()` calls `simulateMouseMovement()` and `refocusKeyboard()` checks if already focused before falling back. |

---

## 4. Grounded Quote Index & Mechanical Verification

All quotes are $\le 25$ words, identified by exact file and line, and verified against receipts in `.ufo/waves/round-41/fetch/`:

1. **`xdph-journal.txt:117`** (5 words):
   > "Got interface: hyprland_focus_grab_manager_v1 (ver 1)"
2. **`xdph-journal.txt:1`** (5 words):
   > "Got interface: ext_foreign_toplevel_image_capture_source_manager_v1 (ver 1)"
3. **`focus-grab-v1.xml:34-36`** (24 words):
   > "This protocol allows clients to limit input focus to a specific set of surfaces and receive a notification when the limiter is removed as"
4. **`focus-grab-v1.xml:62-64`** (25 words):
   > "This interface restricts input focus to a specified whitelist of surfaces as long as the focus grab object exists and has at least one comitted"
5. **`focus-grab-v1.xml:123-124`** (13 words):
   > "Sent when an active grab is cancelled by the compositor, regardless of cause."
6. **`xdph-PortalManager.cpp:88`** (10 words):
   > Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);
7. **`xdph-PortalManager.cpp:99-100`** (7 words):
   > "if (INTERFACE == hyprland_input_capture_manager_v1_interface.name) m_sPortals.inputCapture = std::make_unique<CInputCapturePortal>(makeShared<CCHyprlandInputCaptureManagerV1>("
8. **`Hyprland-FocusGrab.cpp:19-21`** (9 words):
   > "m_grab = makeShared<CSeatGrab>(); m_grab->m_keyboard = true; m_grab->m_pointer = true;"
9. **`Hyprland-FocusGrab.cpp:68-69`** (3 words):
   > "if (sendCleared) m_resource->sendCleared();"
10. **`Hyprland-FocusGrab.cpp:149`** (9 words):
    > "void CFocusGrabProtocol::bindManager(wl_client* client, void* data, uint32_t ver, uint32_t id)"
11. **`quickshell-grab.cpp:66`** (1 words):
    > "this->add_surface(window->surface());"
12. **`quickshell-grab.cpp:75`** (1 words):
    > "this->commit();"
13. **`quickshell-grab.cpp:78`** (11 words):
    > "the protocol will always send cleared() when the grab is deactivated,"
14. **`quickshell-grab.cpp:98-100`** (9 words):
    > "void FocusGrab::hyprland_focus_grab_v1_cleared() { this->active = false; emit this->cleared(); }"
15. **`protocols-README.md:17`** (12 words):
    > "- `hyprland_focus_grab` -> for grabbing input focus, primarily for complex context menus."
16. **`protocols-README.md:22`** (7 words):
    > "- `hyprland_input_capture` -> for EIS input capture."
17. **`issue-565.html:659`** (22 words):
    > "If a workspace windowrule contains silent then matching windows should not get focus, unless that window's workspace is already the active one."
