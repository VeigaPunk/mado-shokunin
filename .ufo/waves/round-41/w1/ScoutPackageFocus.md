# ScoutPackageFocus — report (round 41 w1)

Full table: `.ufo/waves/round-41/w1/ScoutPackageFocus/survey.md`. Read-only; no repo file edited, no tool installed, no network, no socket.

## Verdicts (13 theme files)

- **Admit (re-grounded, folded into the one C2 entry):** `focus-grab-protocol-live-on-host-r14` (spine); `focus-control-surfaces-r28` §1-§2 only.
  Content-only fold-ins from `focus-grab-seat-semantics-r8` (S273/S274 facts).
- **Hold (needs a fetch of SeatManager.cpp/.hpp, not in `fetch/`):** `focus-grab-mouse-target-r11`, `focus-grab-whitelist-admission-r12`,
  `upstream-input-holds-and-the-lock-screen-r16` (different claim: bind flags).
- **Refuse:** `focus-grab-observed-semantics-r9` (private log, superseded), `focus-grab-focus-selection-r10` (self-refuted by r11),
  `focus-grab-keyboard-routing-r13` (JP source + generic security), `focus-grab-has-no-client-here-r15` (single private receipt, would be a 2nd own-work row),
  `compositor-focus-manipulation-literature-r26`, `privileged-client-surface-r29`, `wayland-input-security-literature-r8` (generic security; r29 is the registered refuse),
  `focus-control-surfaces-r28` §3 (Japanese, `amgsk.dev`).

## Depends on private `lanes/mado/roundN/fetch/...` receipts (cannot be admitted as written)

r8 (S275 round8), r9 (S293 round9), r14 (S328 round14), r15 (S338 round15, sole source). S328's "2 adverts at both boots (2026-10-23)" is not
reproducible: the journal now starts 2026-10-25T13:16:45 (`fetch/xdph-journal.txt:1`), one focus-grab advert (line 117).

## Findings that change the plan (each checked against a file or command)

1. **Id-space collision.** Staged ids S203-S349 vs lane S203-S282 (219 rows): staged S218 = arXiv, lane S218 = hyprlang wiki (`SOURCES.append.md:22`, `corpus/SOURCES.md:224`);
   MERGE-REPORT says the lane holds 192 rows. Every staged `source:` id is wrong here; re-issue from S283.
2. **`issue-565.html` was closed as completed 2022-08-25** (maintainer: "should be fixed hastily"; "done and working"), on a 2022 build. Staged r28 §2's
   "`silent` is not a focus guarantee" is unsupported for 0.56.2; the locator "Expected behaviour" is "Expected behavior:" in the page.
3. **Counter `norm()` strips `<...>`:** quotes made of XML attributes (`<interface name=...>`, `summary="..."`) or C++ templates (`std::unordered_map<...>`) can never satisfy
   clause d. Quote element text instead (`focus-grab-v1.xml:62`, `input-capture-v1.xml:68`; `Hyprland-FocusGrab.hpp:7` `#include <unordered_map>` text/`m_surfaces;`). Verified by script over `fetch/`: all other staged quotes for S273/S295/S296/S308/S314/S329/S330/S331/S227 found.
4. **Own-work re-run today:** `hyprctl version` 0.56.2 efb5099; focus-grab strings in `/usr/bin/Hyprland` = 89 (= S275); xdph binary 0 (supports "portal never binds it"); Quickshell not on PATH.
5. **Journal session 1** (pid 1918, 15 adverts, no `Initializing xdph`) vs session 2 (pid 1952, 63 adverts, focus_grab=1): don't read session 1's absence as "not advertised".

## Best single admit set (one entry, all receipts already in `fetch/`)

Nine rows from S283: focus-grab-v1.xml, Hyprland-FocusGrab.cpp, Hyprland-FocusGrab.hpp, xdph-PortalManager.cpp (v1.4.1), quickshell-grab.cpp (@9b0f339),
protocols-README.md, input-capture-v1.xml, issue-565.html (stated as closed 2022), and the single own-work row `xdph-journal.txt`
(`journal sessions=2 adverts=78 interfaces=63 focus_grab=1`). Successor of r14 + r28 §1-§2; refuse r29 and r28 §3 per the registration.

## Unknowns

SeatManager.cpp/.hpp @v0.56.2/efb5099 not read (r11/r12/r13 rules unverified here). Why session 1 is shorter: not established.

Tools installed: none.
