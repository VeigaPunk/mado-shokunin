# ScoutHeldOverlap — report (round 41 w1)

Full findings: `.ufo/waves/round-41/w1/ScoutHeldOverlap/overlap.md` (file:line per held statement, §0-§6).

## Findings

1. Prose hold of focus-grab: none (grep over corpus/SOURCES/lessons/SKILL/PROVINCE/plans). Datum hold: YES. S041
   (`.ufo/waves/round-13/w1/globals.json`, SOURCES.md:53, wayland-info 2026-10-20T04:10:03Z) already lists
   `hyprland_focus_grab_manager_v1` v1 (also input_capture v1, layer_shell v5, xdg_activation v1, security_context v1,
   foreign_toplevel ×3, lock_notifier v1). The entry must cite S041 as a held second-client advertisement.
2. Held prose on the other terms: xdph = xdg-portal-routing-r12.md (descriptor-level routing; pacman/unit state; S037 v1.4.1 SOURCES.md:49;
   S031 :43); no xdph runtime-log reading, no "Got interface" anywhere. Protocol-boundary rules = wayland-protocol-boundaries-r13.md
   (:6-16 phase/advert/behavior split, :14/:29/:33 Hyprland-specific protocols need their own owning-repo authority, :37-43 advertise ≠ bind,
   :104 no per-extension XML inventory), SKILL.md:419-436/470-475. Rule level: keybind-rule-semantics.md:189,210,225,229-232
   (`no_focus` dynamic, `no_initial_focus` static, `focus_on_activate off`, `no_follow_mouse`), hyprctl-verification-layer.md:107,125
   (option values). Nothing held on layer-shell focus, input-capture global, xdg_activation, foreign-toplevel, security_context (prose).
3. No held statement contradicts `fetch/Hyprland-FocusGrab.cpp`. Near-misses: (A) `no_focus` is a window-focus gate: pinned
   FocusState.cpp (efb5099, sha256 9b971362…) checks `noFocus()` in `rawWindowFocus` :150 but not in `rawSurfaceFocus` :223-, which
   the grab's `refocusKeyboard` calls (Hyprland-FocusGrab.cpp:108); the entry must not write an unscoped "no_focus blocks focus".
   (B) idle-lock-route-r17.md:130 holds an UNK on whether `hyprland-lock-notify-v1` is exposed, while S041 and the journal both list
   `hyprland_lock_notifier_v1` v1: stale UNK, answerable at advertisement level.
4. Population caveat: journal session 1952 (63 distinct) ⊂ S041 (71 unique), same versions; S041's 8 absent names (wl_output,
   zwp_linux_dmabuf_v1, wl_drm, wp_color_manager_v1, wp_drm_lease_device_v1, wp_linux_drm_syncobj_manager_v1,
   ext_image_copy_capture_manager_v1, ext_foreign_toplevel_image_capture_source_manager_v1) appear only in the old session 1918 of the
   journal; cause UNK. Never equate "63 in this log session" with "the compositor's globals".
5. `Got interface` = xdph `onGlobal` registry-global log before any bind (xdph-PortalManager.cpp:85-88): advertisement only.
6. Source semantics the lane lacks (new ground): `cleared` is sent only via `finish(true)` (compositor-side cancel); explicit destroy/client death
   → destructor `finish(false)`, no `cleared` (INF from :24-25,:31,:58-71); how a second grab displaces the first depends on SeatManager
   `setGrab`, NOT in the fetched bytes (UNK).
7. Held rows to cite not re-open: S041, S043, S052, S037, S031, S162/S163 (same commit efb5099). lessons/round-35.md:138 notes the staged
   package's S3xx ids name quickshell/hyprland-protocols/Japanese-article rows, so staged ids must not be reused.

## Evidence / state
Read-only greps and python parses of the two data files; one raw-GitHub fetch to /tmp (deleted). No counter run, no lane file edited,
no tool installed, no mutating git/jj. Written: this file and `overlap.md` only.
