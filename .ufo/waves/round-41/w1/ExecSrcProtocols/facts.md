# facts — C1 class-table names vs. real protocol definitions (ExecSrcProtocols, round 41 w1)

Seat `ExecSrcProtocols`, lane `mado-shokunin`, 2026-10-25. Frozen inputs read, never written: `quality/counters/c1-r41-globals.py` (PRED-C1-r41-v1) and `.ufo/waves/round-41/fetch/*`.

## Question

The counter docstring's *class decision table* names the globals it classifies. For each name: which protocol XML defines
that interface, at which `repo@commit:path:line`? A name that is not an interface name would be a defect in the frozen
predicate (reported, not fixed).

## Headline

- The table names **27** distinct interfaces in 10 classes. The docstring table and the in-code `CLASSES` dict are
  identical and both hold 27 (the assignment text said 33; 27 is the measured count — `verify.py` step 1).
- **27/27 names are real interface names; 0 missing, 0 misspelled.** No name-level defect found.
- All 27 are also advertised to `xdg-desktop-portal-hyprland` on this host: `fetch/xdph-journal.txt` holds 78 ADVERT
  lines with 71 distinct names, and every one of the 27 table names is among them (0 absent).
- Two names (`zwp_virtual_keyboard_manager_v1`, `zwp_input_method_manager_v2`) are defined in **wlroots' bundled
  `protocol/`** XMLs, vendored by Hyprland at its own pin — not in wayland-protocols, wlr-protocols,
  hyprland-protocols or plasma-wayland-protocols. A location fact, not a name defect (Notes 1–2).

## Pins (read-only `git ls-remote`, then `git clone`, 2026-10-25)

| repo | commit | note |
|---|---|---|
| hyprland-protocols | `cd1aba6bd78775825eb230b3a4274c48b6705eb7` | the wave's pin; equals `ls-remote HEAD` |
| wayland-protocols | `b9edf66597586c914b5b1ff3d964d7ed201adab9` | `ls-remote HEAD`, gitlab.freedesktop.org/wayland/wayland-protocols |
| wlr-protocols | `1106a4a1c57562ddd438c547da4c0d6dc150d624` | canonical gitlab.freedesktop.org/wlroots/wlr-protocols HEAD. The github.com/swaywm mirror (`b010a03648b88d143236de193bddbfea0c08bc84`) is **stale**: it declares `zwlr_output_manager_v1` version 2 where canonical declares 4 (the host advertises 4) and has older line layout for data-control/screencopy |
| plasma-wayland-protocols | `1db07441870d54157e937674b99380a7dcc0fb32` | checked for KDE definitions: 60 interfaces, none of the 27 names |
| wlroots | `f9d2520f90e1026152ecb3178a7d390621fcee03` | upstream home of the two bundled unstable protocols |
| Hyprland | `efb50993780079460b0cbed1363e2166a2de1d9f` | the host's compositor commit; `protocols/` vendored copies |

## Table

`defined in` is `repo@commit:path:line`; the last column is the exact definition line. Byte copies of all 27 source files
are in `receipt/sources/` with sha256 in `receipt/sources.sha256`; `verify.py --refetch` re-clones the four repos at these
commits and re-hashes them.

| name | class | defined in (repo@commit:path:line) | interface line |
|---|---|---|---|
| `hyprland_focus_grab_manager_v1` | focus-grab | `hyprland-protocols@cd1aba6bd78775825eb230b3a4274c48b6705eb7:protocols/hyprland-focus-grab-v1.xml:39` | `<interface name="hyprland_focus_grab_manager_v1" version="1">` |
| `zwlr_virtual_pointer_manager_v1` | input-synthesis | `wlr-protocols@1106a4a1c57562ddd438c547da4c0d6dc150d624:unstable/wlr-virtual-pointer-unstable-v1.xml:121` | `<interface name="zwlr_virtual_pointer_manager_v1" version="2">` |
| `zwp_virtual_keyboard_manager_v1` | input-synthesis | `Hyprland@efb50993780079460b0cbed1363e2166a2de1d9f:protocols/virtual-keyboard-unstable-v1.xml:91` | `<interface name="zwp_virtual_keyboard_manager_v1" version="1">` |
| `zwp_input_method_manager_v2` | input-synthesis | `Hyprland@efb50993780079460b0cbed1363e2166a2de1d9f:protocols/input-method-unstable-v2.xml:468` | `<interface name="zwp_input_method_manager_v2" version="1">` |
| `hyprland_input_capture_manager_v1` | input-capture | `hyprland-protocols@cd1aba6bd78775825eb230b3a4274c48b6705eb7:protocols/hyprland-input-capture-v1.xml:38` | `<interface name="hyprland_input_capture_manager_v1" version="2">` |
| `zwp_keyboard_shortcuts_inhibit_manager_v1` | input-capture | `wayland-protocols@b9edf66597586c914b5b1ff3d964d7ed201adab9:unstable/keyboard-shortcuts-inhibit/keyboard-shortcuts-inhibit-unstable-v1.xml:44` | `<interface name="zwp_keyboard_shortcuts_inhibit_manager_v1" version="1">` |
| `hyprland_global_shortcuts_manager_v1` | input-capture | `hyprland-protocols@cd1aba6bd78775825eb230b3a4274c48b6705eb7:protocols/hyprland-global-shortcuts-v1.xml:38` | `<interface name="hyprland_global_shortcuts_manager_v1" version="1">` |
| `ext_session_lock_manager_v1` | session-lock | `wayland-protocols@b9edf66597586c914b5b1ff3d964d7ed201adab9:staging/ext-session-lock/ext-session-lock-v1.xml:48` | `<interface name="ext_session_lock_manager_v1" version="1">` |
| `hyprland_lock_notifier_v1` | session-lock | `hyprland-protocols@cd1aba6bd78775825eb230b3a4274c48b6705eb7:protocols/hyprland-lock-notify-v1.xml:33` | `<interface name="hyprland_lock_notifier_v1" version="1">` |
| `ext_idle_notifier_v1` | idle | `wayland-protocols@b9edf66597586c914b5b1ff3d964d7ed201adab9:staging/ext-idle-notify/ext-idle-notify-v1.xml:27` | `<interface name="ext_idle_notifier_v1" version="2">` |
| `zwp_idle_inhibit_manager_v1` | idle | `wayland-protocols@b9edf66597586c914b5b1ff3d964d7ed201adab9:unstable/idle-inhibit/idle-inhibit-unstable-v1.xml:27` | `<interface name="zwp_idle_inhibit_manager_v1" version="1">` |
| `zwlr_data_control_manager_v1` | clipboard | `wlr-protocols@1106a4a1c57562ddd438c547da4c0d6dc150d624:unstable/wlr-data-control-unstable-v1.xml:47` | `<interface name="zwlr_data_control_manager_v1" version="2">` |
| `ext_data_control_manager_v1` | clipboard | `wayland-protocols@b9edf66597586c914b5b1ff3d964d7ed201adab9:staging/ext-data-control/ext-data-control-v1.xml:41` | `<interface name="ext_data_control_manager_v1" version="1">` |
| `zwp_primary_selection_device_manager_v1` | clipboard | `wayland-protocols@b9edf66597586c914b5b1ff3d964d7ed201adab9:unstable/primary-selection/primary-selection-unstable-v1.xml:70` | `<interface name="zwp_primary_selection_device_manager_v1" version="1">` |
| `ext_image_copy_capture_manager_v1` | capture | `wayland-protocols@b9edf66597586c914b5b1ff3d964d7ed201adab9:staging/ext-image-copy-capture/ext-image-copy-capture-v1.xml:37` | `<interface name="ext_image_copy_capture_manager_v1" version="1">` |
| `ext_foreign_toplevel_image_capture_source_manager_v1` | capture | `wayland-protocols@b9edf66597586c914b5b1ff3d964d7ed201adab9:staging/ext-image-capture-source/ext-image-capture-source-v1.xml:86` | `<interface name="ext_foreign_toplevel_image_capture_source_manager_v1" version="1">` |
| `zwlr_screencopy_manager_v1` | capture | `wlr-protocols@1106a4a1c57562ddd438c547da4c0d6dc150d624:unstable/wlr-screencopy-unstable-v1.xml:44` | `<interface name="zwlr_screencopy_manager_v1" version="3">` |
| `hyprland_toplevel_export_manager_v1` | capture | `hyprland-protocols@cd1aba6bd78775825eb230b3a4274c48b6705eb7:protocols/hyprland-toplevel-export-v1.xml:40` | `<interface name="hyprland_toplevel_export_manager_v1" version="2">` |
| `zwlr_foreign_toplevel_manager_v1` | toplevel-control | `wlr-protocols@1106a4a1c57562ddd438c547da4c0d6dc150d624:unstable/wlr-foreign-toplevel-management-unstable-v1.xml:28` | `<interface name="zwlr_foreign_toplevel_manager_v1" version="3">` |
| `ext_foreign_toplevel_list_v1` | toplevel-control | `wayland-protocols@b9edf66597586c914b5b1ff3d964d7ed201adab9:staging/ext-foreign-toplevel-list/ext-foreign-toplevel-list-v1.xml:54` | `<interface name="ext_foreign_toplevel_list_v1" version="1">` |
| `xdg_activation_v1` | toplevel-control | `wayland-protocols@b9edf66597586c914b5b1ff3d964d7ed201adab9:staging/xdg-activation/xdg-activation-v1.xml:69` | `<interface name="xdg_activation_v1" version="1">` |
| `hyprland_toplevel_mapping_manager_v1` | toplevel-control | `hyprland-protocols@cd1aba6bd78775825eb230b3a4274c48b6705eb7:protocols/hyprland-toplevel-mapping-v1.xml:37` | `<interface name="hyprland_toplevel_mapping_manager_v1" version="1">` |
| `zwlr_output_manager_v1` | output-control | `wlr-protocols@1106a4a1c57562ddd438c547da4c0d6dc150d624:unstable/wlr-output-management-unstable-v1.xml:42` | `<interface name="zwlr_output_manager_v1" version="4">` |
| `zwlr_output_power_manager_v1` | output-control | `wlr-protocols@1106a4a1c57562ddd438c547da4c0d6dc150d624:unstable/wlr-output-power-management-unstable-v1.xml:45` | `<interface name="zwlr_output_power_manager_v1" version="1">` |
| `zwlr_gamma_control_manager_v1` | output-control | `wlr-protocols@1106a4a1c57562ddd438c547da4c0d6dc150d624:unstable/wlr-gamma-control-unstable-v1.xml:43` | `<interface name="zwlr_gamma_control_manager_v1" version="1">` |
| `hyprland_ctm_control_manager_v1` | output-control | `hyprland-protocols@cd1aba6bd78775825eb230b3a4274c48b6705eb7:protocols/hyprland-ctm-control-v1.xml:39` | `<interface name="hyprland_ctm_control_manager_v1" version="2">` |
| `wp_security_context_manager_v1` | sandbox | `wayland-protocols@b9edf66597586c914b5b1ff3d964d7ed201adab9:staging/security-context/security-context-v1.xml:26` | `<interface name="wp_security_context_manager_v1" version="1">` |

Class tallies: focus-grab 1, input-synthesis 3, input-capture 3, session-lock 2, idle 2, clipboard 3, capture 4,
toplevel-control 4, output-control 4, sandbox 1 = 27.

## Notes (facts, not defects)

1. **`zwp_virtual_keyboard_manager_v1`** — `virtual-keyboard-unstable-v1.xml` is not in wlr-protocols at any commit (full
   history of both the canonical gitlab repo and the github mirror: `git log --all -S zwp_virtual_keyboard_manager_v1` is
   empty) and never in wayland-protocols (`-S` empty over all refs). It is defined in wlroots
   `protocol/virtual-keyboard-unstable-v1.xml:90` (`wlroots@f9d2520f90e1026152ecb3178a7d390621fcee03`; added 2018-05-28,
   `5334ee8bfd93b2bfdc077f422b87c2509f04d5d4`) and vendored at
   `Hyprland@efb50993780079460b0cbed1363e2166a2de1d9f:protocols/virtual-keyboard-unstable-v1.xml:91`. The Hyprland copy differs from wlroots' by
   two description edits and one dropped error entry (diff of the two receipts); name and version are identical.

2. **`zwp_input_method_manager_v2`** — same shape: wlroots `protocol/input-method-unstable-v2.xml:468`
   (`wlroots@f9d2520f90e1026152ecb3178a7d390621fcee03`; added 2018-10-09, `cec747111946f1d51ae1c9ec14b683aa3d5dcfc4`), vendored at
   `Hyprland@efb50993780079460b0cbed1363e2166a2de1d9f:protocols/input-method-unstable-v2.xml:468`. wayland-protocols carried the `zwp_` name only
   transiently: commit `4da0453` (2025-05-22) added `experimental/xx-input-method/input-method-unstable-v2.xml` defining
   `zwp_input_method_manager_v2` at line 464, and the same day `8d1ccbd` renamed the namespace to `xx_`; every release tag
   checked (1.30, 1.36, 1.40, 1.44, 1.48) has only v1 under `unstable/input-method/`. The table's `zwp_` spelling is correct
   for the protocol the host implements.

3. **README label vs. interface name** — `protocols-README.md:16` lists the protocol as `hyprland_global_keybindings`; the
   interface it defines is `hyprland_global_shortcuts_manager_v1` (`hyprland-global-shortcuts-v1.xml:38`). The table uses the
   interface name, which is what the journal advertises; the README label is not an interface name.

4. **Class placement is not a name question** — e.g. `zwp_input_method_manager_v2` sits under `input-synthesis`. The name
   resolves; whether a text-composition protocol belongs in that class is a classification judgement, out of scope here.

5. **KDE** — no `org_kde_*`/`kde_*`/`qt_*` name is in the table; `plasma-wayland-protocols` defines none of the 27.

6. **Interface version vs. advertised version** — 26 of 27 XML interface versions equal the version the host advertises in
   the journal. The one difference is `hyprland_input_capture_manager_v1`: version 2 in
   `hyprland-protocols@cd1aba6bd78775825eb230b3a4274c48b6705eb7`, advertised as ver 1 by pid 1952 (the compositor binds the older
   revision). Version drift is not a name defect; recorded so the L1 does not have to rediscover it.

## Quotes (<= 25 words, located, machine-checked by `verify.py` step 4)

| source:line | quote | words | what it establishes |
|---|---|---|---|
| `.ufo/waves/round-41/fetch/protocols-README.md:3` | "Wayland protocol extensions for Hyprland." | 5 | what the repository is (title line) |
| `.ufo/waves/round-41/fetch/protocols-README.md:5` | "This repository exists in an effort to bridge the gap between Hyprland and KDE/Gnome's functionality," | 15 | what the repository is (purpose) |
| `.ufo/waves/round-41/fetch/protocols-README.md:11` | "Some of the protocols here also do not belong in w-p, as they are specific to Hyprland." | 17 | why Hyprland-specific protocols live here |
| `.ufo/waves/round-41/fetch/protocols-README.md:16` | "hyprland_global_keybindings` -> for managing global keybinds via D-Bus." | 8 | README's label for the global-shortcuts protocol (interface name differs) |
| `.ufo/waves/round-41/fetch/protocols-README.md:17` | "hyprland_focus_grab` -> for grabbing input focus, primarily for complex context menus." | 11 | README entry for the focus-grab protocol |
| `.ufo/waves/round-41/fetch/input-capture-v1.xml:35` | "This protocol is a bridge of the XDG input capture to the compositor." | 13 | what the input-capture protocol is |
| `.ufo/waves/round-41/fetch/input-capture-v1.xml:40` | "This interface allows to create an input capture session." | 9 | what the manager interface grants |
| `.ufo/waves/round-41/fetch/input-capture-v1.xml:56` | "The inputs are sent through an EIS socket, when the cursor hit a barrier." | 14 | how captured input is delivered to the client |

## Integrity of the pre-fetched receipts

The three fetch files this seat leans on are byte-identical to the pinned `hyprland-protocols` clone (`sha256sum`):

- `protocols-README.md` = `3c7007636e13889860491d0c57f93c29d92122d17838ca1f6559e4aeb7aa6323` = `hyprland-protocols@cd1aba6...:README.md`
- `focus-grab-v1.xml` = `0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4` = `hyprland-protocols@cd1aba6...:protocols/hyprland-focus-grab-v1.xml`
- `input-capture-v1.xml` = `fff89f6f9de622fefa1a62a6e6970f76683b6328454565583046abebcfe2c360` = `hyprland-protocols@cd1aba6...:protocols/hyprland-input-capture-v1.xml`

## Reproduce / verify

```sh
python3 -I .ufo/waves/round-41/w1/ExecSrcProtocols/verify.py            # offline: receipts vs table, names vs counter, journal, quotes
python3 -I .ufo/waves/round-41/w1/ExecSrcProtocols/verify.py --refetch  # re-clones the 4 repos at the pinned commits and re-hashes
```
