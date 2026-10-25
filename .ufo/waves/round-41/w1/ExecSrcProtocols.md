# ExecSrcProtocols — C1 class-table names verified against real protocol definitions (round 41, w1)

STATUS: complete. Seat dir: `.ufo/waves/round-41/w1/ExecSrcProtocols/` (`facts.md`, `verify.py`, `receipt/`).

## Verdict

- **No defect in the frozen class table's name set.** All 27 names it uses are real Wayland interface names; 0 missing,
  0 misspelled. Each resolves to the XML that declares `<interface name="…">` (table below).
- The table names **27** distinct interfaces in 10 classes, not 33 as the assignment text said. The docstring table and the
  in-code `CLASSES` dict are byte-for-byte the same name list (`verify.py` step 1), so the count is 27 either way.
- Independent support: all 27 names are advertised to `xdg-desktop-portal-hyprland` on this host
  (`fetch/xdph-journal.txt`: 78 ADVERT lines, 71 distinct names, 27/27 table names present).
- Two names are not defined in wayland-protocols / wlr-protocols / hyprland-protocols / plasma-wayland-protocols: they live
  in wlroots' bundled `protocol/` XMLs, which Hyprland vendors at the host's commit (Notes 1–2). Location fact, not a defect.

## Method (all read-only)

1. Parsed the class table from `quality/counters/c1-r41-globals.py` twice — from the docstring and from the `CLASSES`
   literal — and required equality (27 names, 10 classes, no duplicates).
2. Pinned every candidate repository with `git ls-remote` (2026-10-25), cloned into `/tmp/srcproto-r41`, and indexed every
   `<interface name=…>` declaration across all XMLs (116 files in the four protocol repos, plus Hyprland's `protocols/`).
3. For each name recorded `repo@commit:path:line` and the exact definition line; copied the 27 source files into
   `receipt/sources/` with a sha256 manifest.
4. Searched full histories where a name was absent: `git log --all -S <name>` in wayland-protocols (564 commits, all tags),
   canonical wlr-protocols, and the github.com/swaywm mirror; listed wayland-protocols trees at tags 1.30/1.36/1.40/1.44/1.48.
5. Wrote `verify.py`: names vs. counter, receipts vs. table line-by-line + sha256, pins-table consistency, journal
   advertisement of every name, quotes located/verbatim/<=25 words; `--refetch` re-clones the 4 repos at the cited commits
   and re-hashes the 27 files. Teeth: 6 mutants of `facts.md` (off-by-one line, interface-version typo, edited quote, table
   name typo, wrong pin in a row, wrong pin in the Pins table) — 6/6 killed, baseline PASS, file restored byte-identically.

## Table — `name | defined in (repo@commit:path:line) | interface line`

| name | class | defined in | interface line |
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

Pins: hyprland-protocols `cd1aba6bd78775825eb230b3a4274c48b6705eb7` (the wave's pin), wayland-protocols `b9edf66597586c914b5b1ff3d964d7ed201adab9`,
wlr-protocols `1106a4a1c57562ddd438c547da4c0d6dc150d624` (canonical gitlab — the github mirror is stale, see Risks), plasma-wayland-protocols
`1db07441870d54157e937674b99380a7dcc0fb32` (0/27 names, so KDE defines none of them), wlroots `f9d2520f90e1026152ecb3178a7d390621fcee03`,
Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f`.

## Findings that are not name defects

1. **`zwp_virtual_keyboard_manager_v1`** — `virtual-keyboard-unstable-v1.xml` is in neither wlr-protocols (both mirrors, full
   history) nor wayland-protocols (all refs). It is defined in `wlroots` `protocol/virtual-keyboard-unstable-v1.xml:90`
   (`wlroots@f9d2520f90e1026152ecb3178a7d390621fcee03`, added 2018-05-28 `5334ee8b`) and vendored at
   `Hyprland@efb50993780079460b0cbed1363e2166a2de1d9f:protocols/virtual-keyboard-unstable-v1.xml:91`; name/version identical in both.
2. **`zwp_input_method_manager_v2`** — same shape: `wlroots` `protocol/input-method-unstable-v2.xml:468` (added 2018-10-09
   `cec74711`), vendored at `Hyprland@efb50993780079460b0cbed1363e2166a2de1d9f:protocols/input-method-unstable-v2.xml:468`. wayland-protocols held
   this `zwp_` name only transiently: `4da0453` (2025-05-22) added it at
   `experimental/xx-input-method/input-method-unstable-v2.xml:464`, and the same day `8d1ccbd` renamed the namespace to
   `xx_`. Every release tag checked has only v1 under `unstable/input-method/`. So `zwp_` is correct for the host.
3. **README label ≠ interface name** — `protocols-README.md:16` calls the protocol `hyprland_global_keybindings`; the
   interface is `hyprland_global_shortcuts_manager_v1` (`hyprland-global-shortcuts-v1.xml:38`). The table uses the interface
   name, which is what the journal advertises.
4. **Version drift (one name)** — 26/27 XML interface versions equal the host's advertised version. The exception is
   `hyprland_input_capture_manager_v1`: version 2 in hyprland-protocols@cd1aba6bd78775825eb230b3a4274c48b6705eb7, advertised as ver 1 by
   pid 1952 (the compositor binds the older revision). Not a name defect; recorded for the L1.

## Quotes (<= 25 words, located, machine-checked)

What the hyprland-protocols README says the repository is:

- `protocols-README.md:3` — "Wayland protocol extensions for Hyprland." (5 words)
- `protocols-README.md:5` — "This repository exists in an effort to bridge the gap between Hyprland and KDE/Gnome's functionality," (15 words)
- `protocols-README.md:11` — "Some of the protocols here also do not belong in w-p, as they are specific to Hyprland." (17 words)

What `input-capture-v1.xml` grants (the file the C1 class `input-capture` rests on):

- `input-capture-v1.xml:35` — "This protocol is a bridge of the XDG input capture to the compositor." (13 words)
- `input-capture-v1.xml:40` — "This interface allows to create an input capture session." (9 words)
- `input-capture-v1.xml:56` — "The inputs are sent through an EIS socket, when the cursor hit a barrier." (14 words)
- definition line, `input-capture-v1.xml:38` — `<interface name="hyprland_input_capture_manager_v1" version="2">`

## Evidence retained

- `.ufo/waves/round-41/w1/ExecSrcProtocols/facts.md` — full table, notes, quotes, integrity section.
- `receipt/sources/<repo>/<path>` — byte copies of the 27 defining XMLs (27 files); `receipt/sources.sha256` — their hashes.
- `verify.py` — offline PASS (names 27/27, receipts 27/27, journal 27/27, quotes 8/8) and `--refetch` PASS
  (4 repos, 27 sources byte-identical at the cited commits). 6/6 mutants killed.
- Fetch receipts re-hashed against the pinned clone: `protocols-README.md` `3c700763…`, `focus-grab-v1.xml` `0bc60c14…`,
  `input-capture-v1.xml` `fff89f6f…` — all byte-identical to `hyprland-protocols@cd1aba6…`.

## Risks / caveats

- `wlr-protocols`: the github.com/swaywm mirror (`b010a03…`) is **stale** — it declares `zwlr_output_manager_v1` version 2
  while canonical gitlab (`1106a4a1…`) declares version 4, which is what the host advertises. All wlr rows cite the canonical
  gitlab pin. Anyone re-checking against the mirror will see different line numbers and versions.
- wayland-protocols is pinned at `ls-remote HEAD` on 2026-10-25, not at the release Hyprland 0.56.2 was built against; every
  cited path also exists in the releases checked, but a future HEAD could move `ext_*` files (as it did for `xx_*`).
- The two wlroots-bundled protocols are cited from Hyprland's vendored copies (the compositor's own bytes). Hyprland's copies
  differ in prose from wlroots' (two description edits, one dropped error entry); name and version agree.
- Scope: this seat verified names → definitions only. It did not score C1/C2, did not run the counters, and did not judge
  whether the class *assignments* are the right classes.

## Tooling / cleanup

- No installs (system `git`, `python3` 3.14 stdlib only). No pacman, no journalctl run (the journal receipt was pre-fetched
  by the L1 and only read). No compositor/Wayland connection.
- Scratch `/tmp/srcproto-r41` (clones) removed after the final verification; the lane keeps only the seat artifacts above.
