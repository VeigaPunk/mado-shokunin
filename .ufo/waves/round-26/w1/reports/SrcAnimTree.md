# SrcAnimTree — round-26 w1 source opening

## Behavior and findings

This is a static source opening, not a control implementation or runtime measurement. The animation node inventory is built by `Config::CAnimationTreeController::reset()` in Hyprland v0.56.2 at `src/config/shared/animation/AnimationTree.cpp:14-66`. In this pin, the tree builder is under `config/shared/animation`, not `src/managers/animation/*`.

The node hierarchy created there is:

- Roots: `__internal_fadeCTM`, `global`.
- `global`: `windows`, `layers`, `fade`, `border`, `borderangle`, `shadowangle`, `glowangle`, `workspaces`, `zoomFactor`, `monitorAdded`.
- `layers`: `layersIn`, `layersOut`.
- `windows`: `windowsIn`, `windowsOut`, `windowsMove`.
- `fade`: `fadeIn`, `fadeOut`, `fadeSwitch`, `fadeShadow`, `fadeGlow`, `fadeDim`, `fadeLayers`, `fadePopups`, `fadeDpms`.
- `fadeLayers`: `fadeLayersIn`, `fadeLayersOut`.
- `fadePopups`: `fadePopupsIn`, `fadePopupsOut`.
- `workspaces`: `workspacesIn`, `workspacesOut`, `specialWorkspace`.
- `specialWorkspace`: `specialWorkspaceIn`, `specialWorkspaceOut`.

That is 34 named nodes plus `__internal_fadeCTM`. `reset()` then assigns `global` enabled/speed 8/default, `__internal_fadeCTM` enabled/speed 5/linear, and `borderangle`, `shadowangle`, and `glowangle` disabled/speed 1/default (lines 61-66).

Hyprland's controller delegates to hyprutils `CAnimationConfigTree`. In the pinned `AnimationConfig.cpp`, `createNode()` initializes a node with `overridden=false`; if a parent name resolves, `pParentAnimation` refers to that parent and `pValues` points to its value source, otherwise both fall back to the node itself (lines 9-28). `setConfigForNode()` sets `overridden=true`, makes that node its own value source, and preserves its existing parent link (lines 35-50). Parent-value propagation visits children with the matching direct parent link and updates only children whose `overridden` flag is false (lines 61-68). Thus `overridden` means the node has an explicit `setConfigForNode()` assignment that should not be replaced by later parent-value propagation; it does not necessarily mean a user-authored setting, since `reset()` itself sets defaults on five nodes.

The literal `addAnimationConfig` was not found in the inspected config-manager, animation-manager, or tree-builder candidate sources. The node list and parent assignments in this pin are directly in `CAnimationTreeController::reset()`.

## Located quotes

1. `src/config/shared/animation/AnimationTree.cpp:15-16`:
   ```cpp
   m_animationTree.createNode("__internal_fadeCTM");
   m_animationTree.createNode("global");
   ```
   This shows the special internal node and `global` are created without an explicit parent argument.

2. `src/config/shared/animation/AnimationTree.cpp:35`:
   ```cpp
   m_animationTree.createNode("windowsIn", "windows");
   ```
   This gives the direct parent link for `windowsIn`.

3. `hyprutils/src/animation/AnimationConfig.cpp:24-25`:
   ```cpp
   .pValues          = (parentRef) ? parentRef->pValues : pConfig,
   .pParentAnimation = (parentRef) ? parentRef : pConfig,
   ```
   This distinguishes inherited values from the direct parent-animation reference, with self-reference as the fallback.

4. `hyprutils/src/animation/AnimationConfig.cpp:63-64`:
   ```cpp
   if (anim->pParentAnimation == PANIM && !anim->overridden) {
       // if a child isnt overridden, set the values of the parent
   ```
   This states that descendants receive parent values only when they are not overridden.

The four quotes were checked in Python by testing that each whitespace-collapsed quote is a substring of the whitespace-collapsed decoded source bytes; all four checks returned `collapsed_substring=True`, and all quotes are under 25 whitespace-separated words.

## Source capture and provenance

The URLs below were checked against the `SOURCES.md` header and tail for row shape; an exact-URL search returned no existing row. `S?` IDs are intentionally left for the registry integrator. No row was inserted into `corpus/SOURCES.md`.

- Hyprland v0.56.2 source: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/animation/AnimationTree.cpp` — pin commit `efb50993780079460b0cbed1363e2166a2de1d9f`; 3,483 bytes; SHA-256 `313ed20167618dfe163fceee8753e9a49d8ef356bc3f580963e07039839e7bae`; anchors `src/config/shared/animation/AnimationTree.cpp:14-66`; capture `.ufo/waves/round-26/fetch/SrcAnimTree.bin`.
- hyprutils v0.14.2 source: `https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/animation/AnimationConfig.cpp` — pin tag `v0.14.2`; 2,354 bytes; SHA-256 `dbb5d50a27f80ea947db92050af40ee87e0e9e0718add0520cbc96e32abe268e`; anchors `src/animation/AnimationConfig.cpp:9-70`; capture `.ufo/waves/round-26/fetch/SrcAnimTreeHyprutils.bin`.

Draft SOURCES rows (not inserted):

| S? | Hyprland v0.56.2 animation tree — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/animation/AnimationTree.cpp | code | A | Static animation node inventory, hierarchy, and initial values | `src/config/shared/animation/AnimationTree.cpp:14-66 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:313ed20167618dfe163fceee8753e9a49d8ef356bc3f580963e07039839e7bae, 3483 B` | Enumerates the fixed nodes and their parents, then sets the initial global, internal, and angle-node values | mined | 2026-10-23 | on-release | corpus/knowledge/animation-table-r26.md |
| S? | hyprutils v0.14.2 animation config tree — https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/animation/AnimationConfig.cpp | code | A | Parent/value links and override propagation for the animation tree used by Hyprland v0.56.2 | `src/animation/AnimationConfig.cpp:9-70 @ tag v0.14.2, sha256:dbb5d50a27f80ea947db92050af40ee87e0e9e0718add0520cbc96e32abe268e, 2354 B` | Shows how node creation links parents, explicit configs set `overridden`, and unoverridden descendants inherit parent values | mined | 2026-10-23 | on-release | corpus/knowledge/animation-table-r26.md |

## Commands and gates

Executed from `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
mkdir -p .ufo/waves/round-26/fetch && timeout 120 prlimit --as=4000000000 curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/animation/AnimationTree.cpp -o .ufo/waves/round-26/fetch/SrcAnimTree.bin && timeout 120 prlimit --as=4000000000 curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/animation/AnimationConfig.cpp -o .ufo/waves/round-26/fetch/SrcAnimTreeHyprutils.bin
```

Outcome: completed successfully with no stdout. Both fetched text files are under the 2 MB source bound.

```sh
timeout 30 prlimit --as=4000000000 sha256sum .ufo/waves/round-26/fetch/SrcAnimTree.bin .ufo/waves/round-26/fetch/SrcAnimTreeHyprutils.bin && timeout 30 prlimit --as=4000000000 wc -lc .ufo/waves/round-26/fetch/SrcAnimTree.bin .ufo/waves/round-26/fetch/SrcAnimTreeHyprutils.bin
```

Outcome: SHA-256 and line/byte counts match the source-capture entries above: 83 lines/3,483 bytes and 70 lines/2,354 bytes. Exact-URL search in `corpus/SOURCES.md` returned no matches.

## Gates, touched surfaces, and limits

- Source-opening gate: passed for both pinned raw sources; quote-substring checks passed; no existing exact-URL SOURCES row was found.
- No C1/C2 counter, control score, Hyprland oracle, compositor, build, or test was run. This report does not claim runtime behavior or a counter verdict.
- Touched only `.ufo/waves/round-26/fetch/SrcAnimTree.bin`, `.ufo/waves/round-26/fetch/SrcAnimTreeHyprutils.bin`, and this report. No product code or registry file was edited; no tool was installed.
- The hyprutils anchor uses the pinned `v0.14.2` tag because that is the version pin provided for this lane; no commit hash is asserted for it.

Report: `.ufo/waves/round-26/w1/reports/SrcAnimTree.md`
