# Pins used by ExecFsSemantics (round 44, w1)

Base URL for every Hyprland pin: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/<path>`
(tag v0.56.2, the running compositor: `hyprctl version` in `receipts/host-read.txt`). Hashes: `SHA256SUMS.txt`.
Repo tree listing: `tree.json` = `https://api.github.com/repos/hyprwm/Hyprland/git/trees/efb50993780079460b0cbed1363e2166a2de1d9f?recursive=1`
(1028 blobs; used only to locate paths).

| pin | repo path | used for |
|---|---|---|
| `Hyprland-FullscreenController.cpp` | `src/managers/fullscreen/FullscreenController.cpp` | clamp of modes, handler selection, exit re-centre |
| `Hyprland-FullscreenHandler.hpp` | `src/managers/fullscreen/handler/FullscreenHandler.hpp` | consulted (interface) |
| `Hyprland-LayoutTarget.cpp` | `src/layout/target/Target.cpp` | `ITarget::setPositionGlobal`, `remember/lastFloatingSize` |
| `Hyprland-LayoutTarget.hpp` | `src/layout/target/Target.hpp` | consulted (declarations) |
| `Hyprland-WindowTarget.cpp` | `src/layout/target/WindowTarget.cpp` | `setBox` on FS branches, floating guard, queued guard |
| `Hyprland-WindowGroupTarget.cpp` | `src/layout/target/WindowGroupTarget.cpp` | group box pushed to members |
| `Hyprland-Space.cpp` | `src/layout/space/Space.cpp` | work area = monitor box − reserved − gaps |
| `Hyprland-LayoutManager.cpp` | `src/layout/LayoutManager.cpp` | `newTarget` (only caller of the floating algorithm's) |
| `Hyprland-FloatingAlgorithm.cpp` | `src/layout/algorithm/FloatingAlgorithm.cpp` | `recenter` uses the remembered size |
| `Hyprland-DefaultFloatingAlgorithm.cpp` | `src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp` | first-map geometry, remembered size |
| `Hyprland-ScrollingFullscreenHandler.cpp` | `src/layout/algorithm/tiled/scrolling/ScrollingFullscreenHandler.cpp` | layout-managed FS: no-op pos/size, column widths |
| `Hyprland-ScrollingAlgorithm.cpp` | `src/layout/algorithm/tiled/scrolling/ScrollingAlgorithm.cpp` | consulted, not quoted |
| `Hyprland-GeometricMovableAnimated.cpp` | `src/desktop/view/types/GeometricMovableAnimated.cpp` | `setBox` writes `m_realSize` |
| `Hyprland-Geometric.hpp/.cpp`, `Hyprland-GeometricAnimated.cpp` | `src/desktop/view/types/` | consulted (`GEOMETRIC_GOAL` mapping) |
| `Hyprland-Window.hpp` | `src/desktop/view/Window.hpp` | consulted (`m_isFloating`, `sendWindowSize`) |
| `Hyprland-Group.cpp` | `src/desktop/view/Group.cpp` | the only other `setFloating` caller |
| `Hyprland-ConfigActions.cpp` | `src/config/shared/actions/ConfigActions.cpp` | `fullscreenWindow` clamp of raw ints |
| `Hyprland-DispatcherTranslator.cpp` | `src/config/legacy/DispatcherTranslator.cpp` | `fullscreen` / `fullscreenstate` argument parsing |
| `Hyprland-KeybindManager.cpp` | `src/managers/KeybindManager.cpp` | consulted (dispatcher registry) |
| `Hyprland-ConfigManager.cpp` | `src/config/ConfigManager.cpp` | consulted (no fullscreen dispatcher here) |
| `Hyprland-WindowRuleApplicator.cpp` | `src/desktop/rule/windowRule/WindowRuleApplicator.cpp` | consulted (rules stored as ints/bools) |
| `Hyprland-XDGShell.cpp` | `src/protocols/XDGShell.cpp` | consulted (client-side fullscreen request) |
| `Hyprland-CMakeLists.txt` | `CMakeLists.txt` | `HYPRUTILS_MINIMUM_VERSION` |
| `hyprutils-0.14.2-AnimatedVariable.hpp` | host `/usr/include/hyprutils/animation/AnimatedVariable.hpp`, `pkg-config --modversion hyprutils` = 0.14.2 | `operator=` sets `m_Goal` |

Frozen round-44 inputs read (hashes in `receipts/frozen-inputs-sha256.txt`): `fetch-c1/Hyprland-FullscreenHandler.cpp`,
`fetch-c1/Hyprland-HyprCtl.cpp`, `fetch-c1/Hyprland-FullscreenController.hpp`, `fetch/Hyprland-Window.cpp`.
