# AttackCoverage — report (MadoR13.AttackCoverage, critic, 2026-10-20)

The full findings, anchors and source-open records are in `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/w1/AttackCoverage.md`.

Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/wayland-protocol-boundaries-r13.md` and the registry rows S005 and S040–S043 (working tree, uncommitted).

Axes: coverage and operability.

## Verdict input

C1 at 4/7 is supportable only after A1 is fixed. A2 (a hand facet check) must be recorded next to the count. Nothing found requires the canonical judge to reject the claim.

## Must fix before admission

**A1 — false observation statement.** The entry's table says "Registry advertisement only" for `wp_color_manager_v1`, and line 42 says `wayland-info` "may bind". In fact `wayland-info` 1.3.0:

- binds 10 interface types (`wayland-info.c:3125-3145` @ tag 1.3.0 `d01edd68`);
- sends get_output/get_image_description/get_information on `wp_color_manager_v1` (`:2744-2750`, `:2626`);
- sends `get_xdg_output` (`:1775`) and `get_default_feedback` (`:2031`);
- filters only its printed output with `-i` (`:3163`), so `-i` does not reduce the interaction.

Fix: rename the column to "Retained in S041" and state the exact bind/request set, either as a new code row or tagged `[INFERENCE]`.

## Should fix (cell changes on rows new this round, before commit)

- **A4 — S041 scope.** Narrow it to "one unsandboxed client, this host's config/DRM". In Hyprland v0.56.2:
  - `ProtocolManager.cpp:134-137,225-263` registers globals conditionally on config and DRM capability;
  - `wp_color_manager_v1` is advertised at version 3 or 1 depending on `experimental:wp_cm_1_2` (`:235`);
  - `Compositor.cpp:262-266,283` filters globals for sandboxed clients.
- **A8 — S041 anchor.** Add `set_sha256 9569d02f…` and the provisional file sha, and commit `globals.json` in the same commit.
- **A6 — S040 anchor.** Note "= tag 1.49 except GOVERNANCE.md:174". I checked that the crosswalk does not change: all 45 phased anchors match the host's 1.49-1 XML.
- **A9 — S042 anchor.** Add "branch main". The served bytes equal `main`; `master` holds a different 2021 blob.

## Coverage gains (optional)

- **A3 — unphased interfaces.** Add a row for interfaces that have no phase. Of the 71 advertised interfaces, 44 are in wayland-protocols, 6 are core `wayland.xml` and 21 come from other repositories.
- **A5 — `xwayland_shell_v1`.** Use it as an observed example: it was advertised to a non-Xwayland client although the spec says the compositor "should hide" it (`xwayland-shell-v1.xml:67-69`).
- **A12 — experimental protocols.** Installed trees never contain `experimental/` (meson @ 1.49, `:157` vs `:167`), so `xx_*` names must be classified against the tag tree.

## Reject if merged

**A7 — SourceRevision draft.** Eight README line anchors do not match blob `e81ad629…`, and it reports the tag object `a8d65d7f` as the tag's commit. It also proposes an in-place edit to the immutable S005 anchor. Use ProtocolPhases' line anchors instead.

## Proven gap in the counter

**A2.** On a scratch copy, an entry holding only the header still scores U4 and passes the join. The counter checks the header join, not the facets.

## In flight

**A11.** The join reports that S017 and S044 name `corpus/lessons/round-13.md`, which does not exist yet. Re-run it after the lesson lands.

## Record

- Installs or upgrades: none by this seat. `wayland-utils 1.3.0-1` was installed by GlobalCapture.
- Host reads were read-only, with no `hyprctl` and no `wayland-info`.
- I disclosed one `grep` of `pacman.log` limited to package-transaction lines.
- Checks for L1 are listed in the full file.
