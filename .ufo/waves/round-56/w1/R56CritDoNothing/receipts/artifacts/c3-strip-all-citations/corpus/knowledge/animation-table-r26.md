---
author: mado
source:
  - [ref]
  - [ref]
  - [ref]
  - [ref]
  - [ref]
---

# Hyprland v0.56.2 animation table

## Scope and directive shape

The opened legacy wiki documents `animation = NAME, ONOFF, SPEED, CURVE [,STYLE]`, with `0` disabling, `1` enabling, and optional trailing fields when disabled; it says unset nodes inherit their parent's values. This is hyprlang-era documentation, while the implementation details below are pinned to Hyprland v0.56.2. [[ref], `content/Configuring/Animations.md:8-12,14-24`]

The v0.56.2 legacy config manager registers `bezier` and `animation` as separate handlers. [[ref], `src/config/legacy/ConfigManager.cpp:612-613 @ efb50993780079460b0cbed1363e2166a2de1d9f`]

## Fixed node tree and inheritance

Hyprland creates the animation nodes in its tree constructor; an `animation =` handler first requires the name to exist and then sets that node's config, rather than creating a new node. [[ref], `src/config/shared/animation/AnimationTree.cpp:14-60`; [ref], `src/config/legacy/ConfigManager.cpp:1432-1435,1469`]

The pinned tree is:

```text
__internal_fadeCTM
 global
 ├─ windows
 │  ├─ windowsIn
 │  ├─ windowsOut
 │  └─ windowsMove
 ├─ layers
 │  ├─ layersIn
 │  └─ layersOut
 ├─ fade
 │  ├─ fadeIn
 │  ├─ fadeOut
 │  ├─ fadeSwitch
 │  ├─ fadeShadow
 │  ├─ fadeGlow
 │  ├─ fadeDim
 │  ├─ fadeLayers
 │  │  ├─ fadeLayersIn
 │  │  └─ fadeLayersOut
 │  ├─ fadePopups
 │  │  ├─ fadePopupsIn
 │  │  └─ fadePopupsOut
 │  └─ fadeDpms
 ├─ border
 ├─ borderangle
 ├─ shadowangle
 ├─ glowangle
 ├─ workspaces
 │  ├─ workspacesIn
 │  ├─ workspacesOut
 │  └─ specialWorkspace
 │     ├─ specialWorkspaceIn
 │     └─ specialWorkspaceOut
 ├─ zoomFactor
 └─ monitorAdded
```

The tree constructor initializes `global` enabled at speed 8 with `default`, `__internal_fadeCTM` enabled at speed 5 with `linear`, and `borderangle`, `shadowangle`, and `glowangle` disabled at speed 1 with `default`. [[ref], `src/config/shared/animation/AnimationTree.cpp:61-66`]

On node creation, hyprutils starts `overridden` false and links `pParentAnimation` to the named parent when present; the node's `pValues` points at the parent's values, or at itself for a root. An explicit `setConfigForNode` sets `overridden` true, stores the node's internal config values, and preserves its parent link. [[ref], `src/animation/AnimationConfig.cpp:9-28,35-48 @ v0.14.2`]

After an explicit config change, the tree recursively points each unoverridden descendant's `pValues` at the parent's values; overridden descendants are skipped. Thus `overridden` records whether the node received an explicit config, while the parent/value links implement inheritance. [[ref], `src/animation/AnimationConfig.cpp:61-70 @ v0.14.2`]

## Directive validation and error path

For `bezier =`, the handler reads the name from argument 0 and four coordinate arguments from 1–4. Each coordinate must be present and pass `isNumber`; otherwise it returns `too few arguments` or `invalid point`. It converts accepted values with `std::stof`, rejects a nonempty argument 5 as `too many arguments`, and calls `addBezierWithName` with the two points. The handler code has no explicit nonempty-name or coordinate-range check. [[ref], `src/config/legacy/ConfigManager.cpp:1389-1423 @ efb50993780079460b0cbed1363e2166a2de1d9f`]

For `animation =`, an unknown node returns `no such animation`. The enabled expression is `parseInt(ARGS[1]).value_or(0) == 1`, so the subsequent 0/1 range check is applied after conversion to a boolean and cannot reject another integer value. If that expression is false, the handler sets the node disabled with speed 1 and bezier `default`, returns success, and skips speed, bezier-existence, and style checks. [[ref], `src/config/legacy/ConfigManager.cpp:1432-1447 @ efb50993780079460b0cbed1363e2166a2de1d9f`]

For an enabled animation, speed must be numeric and greater than zero or the handler returns `invalid speed`; the named bezier must exist or it returns `no such bezier`. The handler then calls `setConfigForNode` and only afterward validates a nonempty style with `styleValidInConfigVar`; a style error is returned from that point. [[ref], `src/config/legacy/ConfigManager.cpp:1449-1478 @ efb50993780079460b0cbed1363e2166a2de1d9f`]

The registered callbacks turn a handler's returned optional error string into `CParseResult::setError`; these source lines establish the callback error conversion, not whole-file rollback or the eventual user-visible diagnostic. [[ref], `src/config/legacy/ConfigManager.cpp:287-309 @ efb50993780079460b0cbed1363e2166a2de1d9f`]

## `hyprctl animations -j` table shape

The `animations` command is registered to `animationsRequest`. Its JSON branch emits a top-level two-element array: animation-node objects first, bezier objects second. The node objects contain `name`, `overridden`, `bezier`, `enabled`, `speed`, and `style`; `enabled` is serialized from the truth value of `internalEnabled`, and speed uses fixed two-decimal formatting. The formatter reads node internal fields, while inheritance is represented by the separate `pValues` links above. [[ref], `src/debug/HyprCtl.cpp:947-964,2018 @ efb50993780079460b0cbed1363e2166a2de1d9f`; [ref], `src/animation/AnimationConfig.cpp:18-26,40-48 @ v0.14.2`]

Each bezier object contains `name`, `X0`, `Y0`, `X1`, and `Y1`. The coordinates come from control points 1 and 2, and all four are formatted to two decimal places. The JSON formatter applies `escapeJSONStrings` to node bezier/style strings and bezier names. [[ref], `src/debug/HyprCtl.cpp:951-976 @ efb50993780079460b0cbed1363e2166a2de1d9f`]

The animation array iterates the full animation config map; the bezier array iterates `Animation::mgr()->getAllBeziers()`. The emitted node inventory therefore follows the fixed tree, while the second array is the manager's bezier inventory; the JSON objects do not include a parent field. [[ref], `src/debug/HyprCtl.cpp:948-976 @ efb50993780079460b0cbed1363e2166a2de1d9f`; [ref], `src/config/shared/animation/AnimationTree.cpp:14-60`]

## Local tool and counter (round 26, C1)

`python3 -I tools/mado-anims.py --home DIR` (landed `2b3487f7`, sha256 `2beda3f7…cab7d`, written by round-26 data seat
ExecAnimToolA) prints the two arrays above from config bytes only. Checked by
`python3 -I .ufo/waves/round-26/c1/count-v2.py REV` (counter v2, sha256 `4ed70b54…6428`): Hyprland v0.56.2 itself, in a
headless session-isolated nested instance, answers `hyprctl animations -j` for the operator snapshot and 40 generated
trees (20 append, 10 edit/delete, 10 independent); measured once at `2b3487f7`: `PRED-C1-r26-v2 cases_pass=41/41
verdict=TARGET_MET`, exit 0 (`.ufo/waves/round-26/evidence/c1-after-v2-2b3487f7.txt`).

Limits (from the data seat's report, not measured by the counter): `{{…}}` expressions in animation lines, environment
variables (`$VAR` seeded from the environment by hyprlang) and a `std::stof` overflow (Hyprland aborts on it) are not
reproduced; output order is fixed, Hyprland's is its map order (the counter compares sets).

[INF] This note is a static-source explanation, not a new live-compositor capture. The handler source does not establish whether a style-validation error is rolled back later in config processing; it also does not establish the complete runtime/user-facing diagnostic path. The formatter iterates its source containers without an explicit sort, so this note does not claim stable entry ordering. [[ref], `src/config/legacy/ConfigManager.cpp:1469-1478,287-309`; [ref], `src/debug/HyprCtl.cpp:948-976`]
