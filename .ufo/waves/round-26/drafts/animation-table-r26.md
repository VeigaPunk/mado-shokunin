---
author: mado
source:
  - S175
  - S176
  - S177
  - S158
  - S162
---

# Hyprland v0.56.2 animation table

## Scope and directive shape

The opened legacy wiki documents `animation = NAME, ONOFF, SPEED, CURVE [,STYLE]`, with `0` disabling, `1` enabling, and optional trailing fields when disabled; it says unset nodes inherit their parent's values. This is hyprlang-era documentation, while the implementation details below are pinned to Hyprland v0.56.2. [S175, `content/Configuring/Animations.md:8-12,14-24`]

The v0.56.2 legacy config manager registers `bezier` and `animation` as separate handlers. [S162, `src/config/legacy/ConfigManager.cpp:612-613 @ efb50993780079460b0cbed1363e2166a2de1d9f`]

## Fixed node tree and inheritance

Hyprland creates the animation nodes in its tree constructor; an `animation =` handler first requires the name to exist and then sets that node's config, rather than creating a new node. [S176, `src/config/shared/animation/AnimationTree.cpp:14-60`; S162, `src/config/legacy/ConfigManager.cpp:1432-1435,1469`]

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

The tree constructor initializes `global` enabled at speed 8 with `default`, `__internal_fadeCTM` enabled at speed 5 with `linear`, and `borderangle`, `shadowangle`, and `glowangle` disabled at speed 1 with `default`. [S176, `src/config/shared/animation/AnimationTree.cpp:61-66`]

On node creation, hyprutils starts `overridden` false and links `pParentAnimation` to the named parent when present; the node's `pValues` points at the parent's values, or at itself for a root. An explicit `setConfigForNode` sets `overridden` true, stores the node's internal config values, and preserves its parent link. [S177, `src/animation/AnimationConfig.cpp:9-28,35-48 @ v0.14.2`]

After an explicit config change, the tree recursively points each unoverridden descendant's `pValues` at the parent's values; overridden descendants are skipped. Thus `overridden` records whether the node received an explicit config, while the parent/value links implement inheritance. [S177, `src/animation/AnimationConfig.cpp:61-70 @ v0.14.2`]

## Directive validation and error path

For `bezier =`, the handler reads the name from argument 0 and four coordinate arguments from 1–4. Each coordinate must be present and pass `isNumber`; otherwise it returns `too few arguments` or `invalid point`. It converts accepted values with `std::stof`, rejects a nonempty argument 5 as `too many arguments`, and calls `addBezierWithName` with the two points. The handler code has no explicit nonempty-name or coordinate-range check. [S162, `src/config/legacy/ConfigManager.cpp:1389-1423 @ efb50993780079460b0cbed1363e2166a2de1d9f`]

For `animation =`, an unknown node returns `no such animation`. The enabled expression is `parseInt(ARGS[1]).value_or(0) == 1`, so the subsequent 0/1 range check is applied after conversion to a boolean and cannot reject another integer value. If that expression is false, the handler sets the node disabled with speed 1 and bezier `default`, returns success, and skips speed, bezier-existence, and style checks. [S162, `src/config/legacy/ConfigManager.cpp:1432-1447 @ efb50993780079460b0cbed1363e2166a2de1d9f`]

For an enabled animation, speed must be numeric and greater than zero or the handler returns `invalid speed`; the named bezier must exist or it returns `no such bezier`. The handler then calls `setConfigForNode` and only afterward validates a nonempty style with `styleValidInConfigVar`; a style error is returned from that point. [S162, `src/config/legacy/ConfigManager.cpp:1449-1478 @ efb50993780079460b0cbed1363e2166a2de1d9f`]

The registered callbacks turn a handler's returned optional error string into `CParseResult::setError`; these source lines establish the callback error conversion, not whole-file rollback or the eventual user-visible diagnostic. [S162, `src/config/legacy/ConfigManager.cpp:287-309 @ efb50993780079460b0cbed1363e2166a2de1d9f`]

## `hyprctl animations -j` table shape

The `animations` command is registered to `animationsRequest`. Its JSON branch emits a top-level two-element array: animation-node objects first, bezier objects second. The node objects contain `name`, `overridden`, `bezier`, `enabled`, `speed`, and `style`; `enabled` is serialized from the truth value of `internalEnabled`, and speed uses fixed two-decimal formatting. The formatter reads node internal fields, while inheritance is represented by the separate `pValues` links above. [S158, `src/debug/HyprCtl.cpp:947-964,2018 @ efb50993780079460b0cbed1363e2166a2de1d9f`; S177, `src/animation/AnimationConfig.cpp:18-26,40-48 @ v0.14.2`]

Each bezier object contains `name`, `X0`, `Y0`, `X1`, and `Y1`. The coordinates come from control points 1 and 2, and all four are formatted to two decimal places. The JSON formatter applies `escapeJSONStrings` to node bezier/style strings and bezier names. [S158, `src/debug/HyprCtl.cpp:951-976 @ efb50993780079460b0cbed1363e2166a2de1d9f`]

The animation array iterates the full animation config map; the bezier array iterates `Animation::mgr()->getAllBeziers()`. The emitted node inventory therefore follows the fixed tree, while the second array is the manager's bezier inventory; the JSON objects do not include a parent field. [S158, `src/debug/HyprCtl.cpp:948-976 @ efb50993780079460b0cbed1363e2166a2de1d9f`; S176, `src/config/shared/animation/AnimationTree.cpp:14-60`]

## Local tool and counter

[INF — local round-26 tool contract, not an upstream Hyprland-source claim] The tool interface is `python3 -I tools/mado-anims.py --home DIR`. The frozen C1 checker is `.ufo/waves/round-26/c1/count-v2.py`; its contract compares both node and bezier field sets with the nested Hyprland oracle and targets `cases_pass=41/41`. The assigned counter invocation is:

```sh
timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file <file>
```

[INF] This note is a static-source explanation, not a new live-compositor capture. The handler source does not establish whether a style-validation error is rolled back later in config processing; it also does not establish the complete runtime/user-facing diagnostic path. The formatter iterates its source containers without an explicit sort, so this note does not claim stable entry ordering. [S162, `src/config/legacy/ConfigManager.cpp:1469-1478,287-309`; S158, `src/debug/HyprCtl.cpp:948-976`]
