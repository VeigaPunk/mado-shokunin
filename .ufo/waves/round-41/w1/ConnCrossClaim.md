# Seat ConnCrossClaim — Wave 1 Report

- **Seat:** `ConnCrossClaim`
- **Role:** UFO-FSD Connector
- **Round:** 41 (hyaku run 7, 2026-10-25), Wave `w1`
- **Lane Repo:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Base Commit:** `ab2bfaab661c846d1de9d58c01651cd156a13949`
- **Freeze Commit:** `60c3914154333180450d5da27ba222d5763cc56a`
- **Status:** Complete. Artifact written to `.ufo/waves/round-41/w1/ConnCrossClaim/cross.md`.

---

## 1. Executive Summary & Assigned Objectives

ConnCrossClaim was assigned three core tasks:
1. **Check Separability:** Formally verify mechanical and semantic separability between Claim C1 (`tools/mado-globals.py`) and Claim C2 (`corpus/knowledge/hyprland-focus-grab-r41.md`) under the frozen registration and counter predicates.
2. **Cross-Source Pattern Analysis:** Map `hyprland_focus_grab_manager_v1` across the host journal (own work), protocol XML, compositor source, and client source. Identify consensus, implicit semantics, and the critical pitfall where an advert is mistaken for use.
3. **Audit Staged Claims vs Grounded Receipts:** Audit entries in `/home/vgpnk/Projects/shokuknow/merge/mado` against fetched receipts in `.ufo/waves/round-41/fetch/` and list explicit contradictions.
4. **UFO-FSD Connector Synthesis:** Synthesize a single non-obvious move improving round axes without harming any.

Deliverable artifact: `.ufo/waves/round-41/w1/ConnCrossClaim/cross.md` (claims-vs-sources matrix with 17 verified quotes $\le 25$ words).

---

## 2. Separability Verification (C1 vs C2)

We audited both counter sources (`quality/counters/c1-r41-globals.py` and `quality/counters/c2-r41-focus-entry.py`) and confirm complete separability:
- **No Shared Deliverables:** C1 touches only `tools/mado-globals.py` and its receipts. C2 touches only `corpus/knowledge/hyprland-focus-grab-r41.md`, `corpus/SOURCES.md`, `corpus/lessons/round-41.md`, `corpus/README.md`, and fetch receipts.
- **No Cross-File Reads:**
  - `c1-r41-globals.py` executes `mado-globals.py` inside a bubblewrap sandbox (`bwrap --unshare-all --cap-drop ALL`, tmpfs `/tmp`, read-only interpreter). It evaluates synthetic nonce-based fixtures; it never accesses git or reads any C2 markdown file.
  - `c2-r41-focus-entry.py` evaluates git show blobs of knowledge, lessons, and receipts. In Clause `h`, it parses the own-work journal receipt using its **own built-in parser** (`ADV_RE` and `BOOT_RE`, lines 84-88, 155-179). It does **not** import, call, or inspect `tools/mado-globals.py`.
- **AST/Grep Check:**
  - `grep -i 'hyprland-focus-grab\|SOURCES\.md\|round-41\.md' quality/counters/c1-r41-globals.py` $\rightarrow 0$ matches.
  - `grep -i 'mado-globals\|ctl-c1\|c1-r41' quality/counters/c2-r41-focus-entry.py` $\rightarrow 0$ matches.
- Either claim can land, mutate, fail, or be verified independently of the other.

---

## 3. Cross-Source Patterns of `hyprland_focus_grab_manager_v1`

We cross-referenced `hyprland_focus_grab_manager_v1` across four local source layers:
1. **Host Journal (`fetch/xdph-journal.txt:117`):**
   - Quote: `Got interface: hyprland_focus_grab_manager_v1 (ver 1)` (5 words).
   - Broadcast in Session 2 (PID 1952) at `2026-10-25T13:36:24-03:00`.
   - In Session 1 (PID 1918), the global was **absent** (only 8 distinct globals advertised).
2. **Protocol XML (`fetch/focus-grab-v1.xml` & `fetch/protocols-README.md`):**
   - Quote (`focus-grab-v1.xml:34-36`, 24 words): `This protocol allows clients to limit input focus to a specific set of surfaces and receive a notification when the limiter is removed as`
   - Quote (`focus-grab-v1.xml:62-64`, 25 words): `This interface restricts input focus to a specified whitelist of surfaces as long as the focus grab object exists and has at least one comitted`
   - Quote (`protocols-README.md:17`, 12 words): `- hyprland_focus_grab -> for grabbing input focus, primarily for complex context menus.`
   - Protocol defines manager (`create_grab`, `destroy`) and grab object (`add_surface`, `remove_surface`, `commit`, `destroy`, `cleared`).
3. **Compositor Implementation (`fetch/Hyprland-FocusGrab.cpp`):**
   - Quote (`Hyprland-FocusGrab.cpp:149`, 9 words): `void CFocusGrabProtocol::bindManager(wl_client* client, void* data, uint32_t ver, uint32_t id)`
   - Quote (`Hyprland-FocusGrab.cpp:19-21`, 9 words): `m_grab = makeShared<CSeatGrab>(); m_grab->m_keyboard = true; m_grab->m_pointer = true;`
   - Implements `bindManager` with no privilege checks or security contexts.
4. **Client Observer vs Consumer (`fetch/xdph-PortalManager.cpp` vs `fetch/quickshell-grab.cpp`):**
   - Quote (`xdph-PortalManager.cpp:88`, 10 words): `Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);`
   - Quote (`quickshell-grab.cpp:78`, 11 words): `the protocol will always send cleared() when the grab is deactivated,`
   - Quote (`quickshell-grab.cpp:98-100`, 9 words): `void FocusGrab::hyprland_focus_grab_v1_cleared() { this->active = false; emit this->cleared(); }`

### Pitfall: Mistaking Advert for Use
`xdg-desktop-portal-hyprland`'s registry listener (`CPortalManager::onGlobal`) logs *every* global broadcast by the compositor. It binds `hyprland_input_capture_manager_v1` and `hyprland_global_shortcuts_manager_v1`, but contains **zero** binds or handlers for `hyprland_focus_grab_manager_v1`. A reader seeing the journal line could mistake an advert for portal usage. Furthermore, host binary sweeps confirm no program on this host besides `/usr/bin/Hyprland` carries the string.

---

## 4. Contradictions in Staged Package vs Fetched Sources

1. **`privileged-client-surface-r29.md` (Major False Claim):**
   - Staged claim: Asserts that focus-grab is a "privileged client" surface granted only to compositor-spawned clients via `WAYLAND_SOCKET` descriptor handoff.
   - Grounded truth: `Hyprland-FocusGrab.cpp:149` (`bindManager`) exposes the interface to *all* connecting clients without credential or privilege checks. `protocols-README.md:17` specifies its purpose is "for complex context menus" (ordinary UI). Registration rightly marks r29 as `REFUSE`.
2. **`focus-control-surfaces-r28.md` (Province & Conflation Contradictions):**
   - Staged claim: Relies on `amgsk.dev` (Japanese practitioner blog) and pairs issue #565 (`silent` rule bug) with focus-grab.
   - Grounded truth: `amgsk.dev` is out of province under PROVINCE.md:68-80. `issue-565.html:659` reveals issue #565 was a 2022 window-rule bug where a window opened in another workspace momentarily stole focus, completely unrelated to the 2024 `hyprland_focus_grab_v1` protocol.
3. **`focus-grab-protocol-live-on-host-r14.md` (Count Drift):**
   - Staged claim: Cites an older journal (2026-10-23) claiming 2 focus-grab adverts across two boots.
   - Grounded truth: The live receipt `xdph-journal.txt` (`bf8fa91a...`) has Session 1 with 0 focus-grab adverts (8 globals total) and Session 2 with 1 advert.

---

## 5. UFO-FSD Connector Move

### 5.1 Evidence
- C1 delivers `tools/mado-globals.py` with class `focus-grab` and `--expect NAME`.
- C2 delivers knowledge entry `corpus/knowledge/hyprland-focus-grab-r41.md` and cites `xdph-journal.txt`.
- `xdph-PortalManager.cpp` logs every interface but never binds `hyprland_focus_grab_manager_v1`.
- `focus-grab-has-no-client-here-r15.md` shows no installed client binds focus grab.

### 5.2 Affected Axes
- **operability** (C1, diagnostic tool validity).
- **coverage** (C2, grounded focus-grab knowledge entry).

### 5.3 Proposed Move: The "Advertisement-to-Binding Gap" Contract Bridge
Formally synthesize the **Advertisement-to-Binding Gap** across C1 documentation and C2 entry drafting:
1. **For C1 (`mado-globals.py`):** Explicitly document in SKILL.md and PROVINCE.md that `mado-globals.py` is an *advertisement census tool* (measuring compositor announcements via `wl_registry::global`), not a *client-capability or client-binding tool*. `--expect NAME` verifies server advertisement, not portal or client binding.
2. **For C2 (`hyprland-focus-grab-r41.md`):** Ground the entry around the four-source chain (`xdph-journal.txt` [advertisement], `xdph-PortalManager.cpp` [portal non-binding], `focus-grab-v1.xml` / `protocols-README.md` [unprivileged context menu purpose], and `quickshell-grab.cpp` [real client lifecycle]). This directly resolves the draft tension (Draft A vs B vs C) by establishing that the focus-grab surface on this host is **advertised-but-unbound**.
3. **Net Benefit:**
   - Improves **operability** by eliminating false operational assumptions from `--expect` verdicts.
   - Improves **coverage** by giving C2 a cohesive, contradiction-free foundation grounded in 4 verified receipts.
   - Harms neither axis: 100% compliant with frozen counter predicates (`PRED-C1-r41-v1` and `PRED-C2-r41-v1`).

### 5.4 Risks & Second-Order Effects
- **Runtime Surface:** Zero impact; tool CLI and output formatting remain byte-for-byte compliant.
- **Contract Surface:** Eliminates operational confusion in SKILL.md.
- **Substrate Surface:** Read-only; zero host or compositor mutation.
- **Verification Surface:** Counters continue to evaluate and pass without modification.

### 5.5 Verification Script
All 17 quotes in `.ufo/waves/round-41/w1/ConnCrossClaim/cross.md` were mechanically verified against receipts in `.ufo/waves/round-41/fetch/` using Python eval:
```python
# Result: 17/17 quotes verified, all <= 25 words, PASS.
```
