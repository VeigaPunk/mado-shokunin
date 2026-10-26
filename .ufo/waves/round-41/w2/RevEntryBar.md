# Seat Report — RevEntryBar (mado round 41, wave w2)

- **Seat:** `RevEntryBar` (reviewer, leaf — no subagent dispatch)
- **Target:** `07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/knowledge/hyprland-focus-grab-r41.md` (and companion C2 surfaces `corpus/SOURCES.md`, `corpus/README.md`, `corpus/lessons/round-41.md`, `.ufo/waves/round-41/fetch/xdph-installed-version.txt`) against `corpus/QUALITY.md` (all 68 criteria) and `/home/vgpnk/Projects/shokunin/CORPUS.md`.
- **Deliverable:** `.ufo/waves/round-41/w2/RevEntryBar/review.md` (full 68-criterion verdict table, `CORPUS.md` check table, and severity-ranked defects D1–D7 with exact `file:line` and reproduction commands) and `.ufo/waves/round-41/w2/RevEntryBar/verify_quotes.py` (quote verifier over all 31 source quotes in the entry: `ENTRY_QUOTES_SUMMARY checked=31 failed=0`).

## Severity-Ranked Defects Summary

1. **[HIGH] D1 — `corpus/knowledge/hyprland-focus-grab-r41.md:10,73`, `corpus/lessons/round-41.md:32`, `corpus/SOURCES.md:49` (Attacks: `QUALITY.md` criteria 2/42, `CORPUS.md:112-118` Rules 1 & 2):**
   - Held row `S037` (`kind = docs`, `https://github.com/hyprwm/xdg-desktop-portal-hyprland/releases/tag/v1.4.1`, anchor `“v1.4.1”, “Changes”; tag commit cc8e5ef; released 2026-07-29`) is cited and bound in `GATE S037` to `.ufo/waves/round-41/fetch/xdph-installed-version.txt` (a local `/var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc` read), while `entry:73` admits `S037`'s release page was not re-fetched.
   - `corpus/SOURCES.md:49` modifies `S037`'s `used-by` cell in place (`corpus/knowledge/xdg-portal-routing-r12.md` → `corpus/knowledge/xdg-portal-routing-r12.md, corpus/knowledge/hyprland-focus-grab-r41.md`), but `corpus/lessons/round-41.md` never logs the `old -> new` transition as required by `CORPUS.md:116-117` (`grep -c xdg-portal-routing-r12` on `round-41.md` is `0`).

2. **[MEDIUM] D2 — `corpus/knowledge/hyprland-focus-grab-r41.md:85` (Attacks: `QUALITY.md` criteria 1/41 & 2/42, claim stronger than quote):**
   - Line 85 writes: `**OBS** S285 (FocusGrab::addWaylandWindow): "this->pendingAdditions.append(window); this->commitRequired = true;" - adding a window records it and *defers* the protocol call; sync() is the only place that commits.`
   - In `fetch/quickshell-grab.cpp:65-69`, `FocusGrab::addWaylandWindow` calls `this->add_surface(window->surface());` **immediately** on line 66 before `this->pendingAdditions.append(window);` on line 67. Only the `commit` protocol call (`this->commit()` in `sync()`, line 75) is deferred (or `addWaylandWindow` itself when `QWindow` lacks a `QWaylandWindow`/`wl_surface` in `addWindow`, lines 21–53).

3. **[MEDIUM] D3 — `corpus/knowledge/hyprland-focus-grab-r41.md:69,115` vs `corpus/SOURCES.md:232,235` (Attacks: `QUALITY.md` criteria 2/42 & 10):**
   - `entry:69` correctly counts **ten** named branches in `CPortalManager::onGlobal` (`xdph-PortalManager.cpp:85-261`: 9 direct `wl_registry_bind` branches plus `zwlr_foreign_toplevel_manager_v1` at `:249-255` delegated to `CToplevelManager`), whereas `corpus/SOURCES.md:235` (`S286` `scope`, `anchor`, and `teaches`) says **nine** and omits `:249-255`.
   - `entry:115` and `corpus/README.md:70` say **five** requests (counting distinct request member names), `corpus/SOURCES.md:232` (`S283` `scope`) says **four** requests, and `focus-grab-v1.xml` actually contains **six** `<request>` elements (`create_grab`, manager `destroy`, `add_surface`, `remove_surface`, `commit`, grab `destroy`).

4. **[MEDIUM] D4 — `corpus/knowledge/hyprland-focus-grab-r41.md:21,63,65,67,69,71,109` (Attacks: `QUALITY.md` criteria 10, 11, 14; `CORPUS.md:34-41`):**
   - **Criterion 14 (census set comparison) & held datum `S041`:** `entry:67` calls session 2 (`63` distinct globals) *"a whole advertisement ... which is the only session that can be compared with the compositor's registry as a whole"*, without comparing it against held row `S041` (`.ufo/waves/round-13/w1/globals.json`, `71` distinct globals on the same Hyprland `efb5099` build, which already includes `hyprland_focus_grab_manager_v1` v1) or noting that the 8 globals in `S041` absent from session 2 (`wl_output`, `zwp_linux_dmabuf_v1`, `wl_drm`, `wp_color_manager_v1`, `wp_drm_lease_device_v1`, `wp_linux_drm_syncobj_manager_v1`, `ext_image_copy_capture_manager_v1`, `ext_foreign_toplevel_image_capture_source_manager_v1`) are the exact 8 distinct globals in session 1.
   - **Criterion 10:** Prose counts (`2`, `5`, `15`, `63`, `78`, `10`, `1`) are not formatted as `<n> — <command> <date>` (note: line 63 `journal sessions=2 adverts=78 interfaces=63 focus_grab=1` is required verbatim by `PRED-C2-r41-v2` clause h and must not be altered in place).
   - **Criterion 11:** Line 71's `grep -in focus` negative sweep is over `PortalManager.cpp` alone without stating why that file covers the portal's registry handling (`PortalManager.cpp:300` is the single `wl_registry` callback).

5. **[MEDIUM] D5 — `corpus/knowledge/hyprland-focus-grab-r41.md:67,77,109` (Attacks: Task `INF` basis rule & `QUALITY.md` criteria 2/42, 3/43):**
   - 5 of 8 `**INF**` paragraphs (`lines 37, 55, 75, 91, 105`) carry explicit `` `Basis:` ... `` tags; 3 of 8 (`lines 67, 77, 109`) omit `` `Basis:` ``, and line `109` mixes an `[OBS]` command observation (`grep -rli ... exits 1 at base`) into an `**INF**` paragraph.

6. **[LOW] D6 — `corpus/knowledge/hyprland-focus-grab-r41.md:97` (Attacks: quote completeness, `QUALITY.md` criteria 1/41 & 2/42):**
   - Line 97 quotes `"If a workspace windowrule contains silent then matching windows should not get focus"` from `issue-565.html:659`, truncating the trailing conditional `", unless that window's workspace is already the active one."` (full sentence is 22 words, within the 25-word limit).

7. **[LOW] D7 — `corpus/README.md:70` and `corpus/SOURCES.md:286-449` (Attacks: `CORPUS.md:46-48,82,126-128`):**
   - `corpus/README.md:70` has only 2 table columns (`NF=4`, missing the 3rd `Sources` column `S283–S289, S037 |`), whereas all 58 prior rows (`lines 12–69`) have 3 columns (`NF=5`).
   - `corpus/SOURCES.md` `## Search log` (`:286-449`) has no round-41 search-log entry.

## Answers to Specific Prompt Questions

- **Every `QUALITY.md` criterion (1–68) evaluated:** Yes — full 68-row table in `.ufo/waves/round-41/w2/RevEntryBar/review.md` §2 (`24 pass`, `8 fail` [criteria 1/41, 2/42, 3/43, 10, 11, 14], `36 n.a.`).
- **Each `INF` marked with its basis:** 5/8 yes (`:37, :55, :75, :91, :105`), 3/8 missing `` `Basis:` `` (`:67, :77, :109` — D5).
- **Each `UNK` a real unknown:** Yes — all 5 `**UNK**` paragraphs (`:39, :57, :79, :93, :107`) are genuinely unanswerable from the fetched receipts under host safety rules.
- **Any claim stronger than its quote:** Yes — `:85` (D2, `add_surface` is not deferred in `addWaylandWindow`) and `:97` (D6, drops `unless that window's workspace is already the active one`).
- **Any scope creep beyond `PROVINCE.md`:** None (`focus-control-surfaces-r28.md` §3 localized Japanese channel is refused and excluded at `:15, :136`).
- **Any sibling-domain bleed (Wayland security literature):** None (`compositor-focus-manipulation-literature-r26.md`, `wayland-input-security-literature-r8.md`, and `privileged-client-surface-r29.md` are excluded, and `:134` disclaims security-boundary status).
- **Any duplicate of held knowledge:** No prose duplicate in `corpus/knowledge/` at base `ab2bfaab661c846d1de9d58c01651cd156a13949`; datum overlap with `S041` (`.ufo/waves/round-13/w1/globals.json`) noted in D4.

## Tooling

- No tools or packages were installed or updated during this seat.

Report: .ufo/waves/round-41/w2/RevEntryBar.md
