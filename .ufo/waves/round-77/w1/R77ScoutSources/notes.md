# R77ScoutSources — working notes

## Environment / tooling
- No tool install or upgrade. No pacman. `curl` used once to fetch
  `codeload.github.com/wmww/gtk-layer-shell/tar.gz/refs/tags/v0.10.1` into scratch to anchor the
  auto-exclusive-zone formula; the installed library on the host is
  `/usr/lib/libgtk-layer-shell.so.0.10.1`, so the fetched tree matches the running ABI. Scratch dir
  removed before finish.
- No LSP server answers the pinned C++ trees; all anchors are `grep -n` line citations.
- Host probes used (read verbs only): `hyprctl monitors -j`, `hyprctl layers -j`. Output reduced to
  name/width/height/scale/reserved/transform and namespace/box; no instance signature, no titles.

## Anchor extraction commands
- `grep -n "m_layerSurfaceLayers" Hyprland/src` → Monitor.hpp:195, LayerSurface.cpp:33/55/315-322,
  HyprCtl.cpp:660-690.
- `grep -n "arrangeLayerArray\|arrangeLayersForMonitor\|applyExclusive" Hyprland/src`
  → Renderer.cpp:2529 (applyExclusive), 2587 (arrangeLayerArray), 2673 (arrangeLayersForMonitor).
- Numbered slices read: Renderer.cpp 2520-2715, 2584-2660; HyprCtl.cpp 215-310, 629-763;
  ReservedArea.cpp/.hpp; Monitor.cpp 694-706, 996-1045, 1772-1774; LayerShell.cpp 39-113;
  LayerSurface.cpp 33/55.
- Waybar: bar.cpp 18-132, 150-423, 423-500, 620-700; config.cpp 168-215; man/waybar.5.scd.in 37-138.
- gtk-layer-shell (fetched): src/layer-surface.c 24-105, 255-345.

## Decisions
- Treated `layer: bottom` + `exclusive: true` as reserving: source has no level filter in the
  exclusive pass. No frozen case declares `layer: bottom`, so this is source-only ground.
- Reported the auto-branch gap (F2) as a declaration-posture contradiction rather than a case
  failure: the two reachable auto branches (width on horizontal bars, height on vertical bars) are
  modelled correctly.
- Did not touch any lane file; report is the only file written outside this dir.

## Cross-checks that came back clean
- `LEVEL` map order ↔ wlr-layer-shell enum ↔ array index ↔ JSON key: 4-way consistent.
- `RESERVED_INDEX` ↔ monitors reply argument order (left, top, right, bottom): consistent.
- Margin precedence (per-side > CSS string > int) matches bar.cpp branch-for-branch, including the
  zero-fill of absent per-side keys and the initial-zeros fallback on a stoi failure.
- `setPosition`'s `configured_width > 1` threshold is the tool's `width > 1`, and gtk-layer-shell
  zeroes the request whenever both horizontal anchors survive, so `width: 1` cannot diverge.
