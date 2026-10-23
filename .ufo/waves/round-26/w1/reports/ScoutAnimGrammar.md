# ScoutAnimGrammar

Recon only. No resolver, no `tools/mado-anims.py`, no counter run, no Hyprland process. Grammar note: `.ufo/waves/round-26/recon/anim-grammar.md`.

## What I read

Pinned raw files, Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` (the running compositor reports that same commit):

- `src/config/ConfigManager.cpp` (which manager)
- `src/config/legacy/ConfigManager.cpp` (`handleAnimation`, `handleBezier`, reset, `source`)
- `src/config/shared/animation/AnimationTree.cpp`
- `src/config/shared/parserUtils/ParserUtils.cpp` (`parseInt`)
- `src/animation/AnimationManager.cpp` (`styleValidInConfigVar`, `linear`, `animations:enabled`)
- `src/debug/HyprCtl.cpp` (`animationsRequest`)
- `src/helpers/MiscFunctions.cpp` (`escapeJSONStrings`)
- `src/config/values/ConfigValues.cpp` (`animations:enabled`, `animations:workspace_wraparound`)
- `src/config/lua/ConfigManager.cpp` (reset only)

hyprutils v0.14.2: `src/animation/AnimationConfig.cpp`, `src/animation/AnimationManager.cpp`, `src/animation/BezierCurve.cpp`, `src/string/String.cpp`, `src/string/VarList.cpp`, `include/hyprutils/string/Numeric.hpp`.

hyprlang v0.6.8: `src/config.cpp` (category stack, handler dispatch, `parseFile` continues after errors).

No language server was attached to that fetched tree. Line numbers are from those files, not from a grep index. `{:.2f}` samples were measured with host `g++ -std=c++23` `std::format`, the same call the writer makes.

No tools installed.

## Findings

Confidence high, from the cited lines. The note has the full rules. The parts that will surprise a data seat:

1. The dump is 35 nodes. `__internal_fadeCTM` is real and is not in `c1/count.py`'s `NODES` list. Parents and the five seeded `setConfigForNode` calls are in `AnimationTree.cpp:14-67`. Unknown names are rejected, not added.

2. `hyprctl animations -j` prints each node's own `internal*` fields, not `pValues`. Unset children stay `overridden: false`, empty bezier, empty style, speed `0.00`, and enabled `true` because the stored `-1` is truthy (`HyprCtl.cpp:958`). Setting a parent does not change the child's dumped speed or bezier. The animator follows `pValues`; the JSON does not (`hyprutils AnimationConfig.cpp:61-70`).

3. Enabled is not a closed set of tokens. `parseInt(...).value_or(0) == 1` (`ConfigManager.cpp:1438`). Anything that is not exactly 1, including `0`, `2`, `maybe`, `1.0`, and a missing field, takes the off path, which **writes** speed 1, bezier `default`, empty style, and returns success. The error string `"invalid animation on/off state"` is unreachable. Prefixes `true`/`on`/`yes` and `0x1` are the on value. The check is case-sensitive and is a prefix, so `online` is on and `none` is off.

4. A bad speed or a missing bezier returns before any write. The `speed = 1` / `speed = 10` assignments in that function are local only. A bad style is checked **after** `setConfigForNode`, so the bad style is stored and an error is still reported. `parseFile` keeps going and does not roll back (`hyprlang src/config.cpp:1016-1039`).

5. Style families are prefix tests, not a table of exact names. `slide*` is legal on `window*`, `workspaces*` / `specialWorkspace*`, and `layers*`, with different percent rules (windows `popin` drops the last char from a slice that still contains the space; workspace `slide` percent uses `+ 1`). `gnome` / `gnomed` are windows-only. `loop` / `once` are `*angle` only. Any other non-empty style, including every `fade*` node and `global`, is `"animation has no styles"`. The parsed percent is discarded.

6. `bezier =` is five fields, points via `isNumber` + `stof`, no range clamp, no partial store. A sixth token errors. Redefinition overwrites, including `default` and `linear`. Builtins after reset: `default` `(0, 0.75)-(0.15, 1)` and `linear` `(0,0)-(1,1)`. JSON prints the two control points, not the `(0,0)` and `(1,1)` endpoints, with `{:.2f}`.

7. `animations { }` is an ordinary category, not a special one. It only prefixes config values (`animations:enabled` default true, `animations:workspace_wraparound` default false). Those flags do not appear in `animations -j`. `animation` and `bezier` inside the block are the same unscoped handlers as at top level. The handler sees the right-hand side after `$var` and `{{...}}` expansion. `source =` is inline, so order is the parse order.

8. The counter compares sets of parsed JSON fields (`c1/count.py:13-15`, `:185-190`). Map order does not matter. `8.00` matches `8.0`. Booleans must be JSON `true`/`false`. On this host, `stof("1.005")` formats as `1.00` and `stof("0.135")` as `0.14`, because the float is rounded, not the decimal token. Negative zero prints `-0.00` and can occur on a bezier coordinate, not on a stored speed.

## Unknowns

- I did not run `hyprctl` or the oracle, so the `-1` → JSON `true` rule is the writer source, not a captured dump.
- `std::stof` overflow is uncaught in `parseLine` and in `CConfigManager::reload`. I did not search every caller above `reload` for an outer try.
- I did not open every Lua binding translation unit. `src/config/lua/ConfigManager.cpp` has no keyword parser. The `.conf` path does not use it.
