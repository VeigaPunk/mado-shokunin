# Animation grammar, Hyprland v0.56.2

Pin `efb50993780079460b0cbed1363e2166a2de1d9f`. This is the legacy hyprlang front end, which is what a `.conf` tree uses. A path whose extension is `.lua` selects the Lua manager; anything else, including a missing extension rewritten to `.conf`, selects `Config::Legacy::CConfigManager` (`src/config/ConfigManager.cpp:29-50`). The Lua manager file at this pin only resets the shared tree (`src/config/lua/ConfigManager.cpp:699`). It has no `animation` or `bezier` keyword parser. Beside Hyprland: hyprutils v0.14.2, hyprlang v0.6.8.

`hyprctl animations -j` dumps that shared tree plus the bezier map. It does not dump resolved inherited values. Read section 3 before treating a child's speed or bezier as the parent's.

## 1. Node list and parents

Built only in `CAnimationTreeController::reset` (`src/config/shared/animation/AnimationTree.cpp:14-67`). `createNode(name)` is a root. `createNode(name, parent)` requires the parent to exist already (`hyprutils v0.14.2 src/animation/AnimationConfig.cpp:9-29`). The keyword handler never inserts an unknown name (section 5). The set is 35 nodes: the 34 names in `c1/count.py:37-41`, plus `__internal_fadeCTM`, which that generator does not target but the dump always includes.

| Node | Parent | Default after the creates |
|---|---|---|
| `__internal_fadeCTM` | root | enabled 1, speed 5, bezier `linear`, style empty (`AnimationTree.cpp:63`) |
| `global` | root | enabled 1, speed 8, bezier `default`, style empty (`:62`) |
| `windows`, `layers`, `fade`, `border`, `borderangle`, `shadowangle`, `glowangle`, `workspaces`, `zoomFactor`, `monitorAdded` | `global` | only the three angle nodes are set: enabled 0, speed 1, bezier `default`, style empty (`:64-66`) |
| `layersIn`, `layersOut` | `layers` | none |
| `windowsIn`, `windowsOut`, `windowsMove` | `windows` | none |
| `fadeIn`, `fadeOut`, `fadeSwitch`, `fadeShadow`, `fadeGlow`, `fadeDim`, `fadeLayers`, `fadePopups`, `fadeDpms` | `fade` | none |
| `fadeLayersIn`, `fadeLayersOut` | `fadeLayers` | none |
| `fadePopupsIn`, `fadePopupsOut` | `fadePopups` | none |
| `workspacesIn`, `workspacesOut`, `specialWorkspace` | `workspaces` | none |
| `specialWorkspaceIn`, `specialWorkspaceOut` | `specialWorkspace` | none |

`reset()` runs at the start of every legacy reload and again inside `resetHLConfig` before parse (`src/config/legacy/ConfigManager.cpp:726-731`, `:753-754`, `:764-770`). One parse replaces the tree; it is not a patch of the previous reload.

## 2. What a node stores

`SAnimationPropertyConfig` (`hyprutils include/hyprutils/animation/AnimationConfig.hpp:13-23`):

- `overridden` starts false.
- `internalBezier` and `internalStyle` start empty, `internalSpeed` starts `0`, `internalEnabled` starts `-1`.
- `pValues` is the node whose `internal*` fields the animator reads. A new root points `pValues` at itself. A new child points `pValues` at its parent's current `pValues`.
- `pParentAnimation` is the parent, or itself for a root.

`setConfigForNode` (`hyprutils src/animation/AnimationConfig.cpp:35-51`) sets `overridden` true, copies enabled, speed, bezier, and style into the `internal*` fields, points `pValues` at this node, and keeps `pParentAnimation`. It then calls `setAnimForChildren` (`:61-70`). Every node whose parent pointer is this node and whose `overridden` is still false gets `pValues = parent->pValues`, and the walk repeats. Overridden descendants are skipped, so their children are not re-pointed. The walk does not copy `internal*` onto children. The comment at `:64` is only that `pValues` assignment.

Hyprland's wrapper takes `bool enabled` and forwards it (`src/config/shared/animation/AnimationTree.cpp:77-79`). A keyword therefore stores enabled as `0` or `1`. `-1` remains only on nodes that have never been passed to `setConfigForNode`. A missing name returns without inserting (`AnimationConfig.cpp:36-38`). The legacy handler does not call it for a missing name.

## 3. The dump is not the inherited value

`animationsRequest` reads `overridden`, `internalBezier`, `internalEnabled`, `internalSpeed`, and `internalStyle` on the node itself (`src/debug/HyprCtl.cpp:947-959`). It does not follow `pValues`.

A node that has never been `setConfigForNode`'d dumps as `overridden` false, `bezier` `""`, `style` `""`, `speed` `0.00`, and enabled from the integer `-1`. The JSON writer turns any non-zero integer into `true` (`:958`). Text mode prints the raw integer (`:933-934`), so the same unset node is `-1` in text and `true` in JSON.

Only the five defaults in section 1, plus nodes a keyword actually wrote, have a real speed, bezier, or style in the dump. Setting `windows` does not change the dumped fields of `windowsIn`. It only repoints `windowsIn.pValues` for the animator. The frozen counter compares this dump (`c1/count.py:13-15`, `:35-36`, `:185-190`). Emit the raw fields, not the inherited ones.

## 4. How a line reaches the handler

Legacy config sets `throwAllErrors = true` (`ConfigManager.cpp:486`). The handlers are unscoped: `registerHandler(..., "bezier", {false})` and `"animation"` (`:612-613`). `{false}` is `allowFlags`, so the left-hand side must be exactly `bezier` or `animation`, not a flagged prefix (`hyprlang v0.6.8 src/config.cpp:844-870`).

Before the handler, hyprlang:

1. Joins a trailing `\` to the next line, after dropping trailing spaces and tabs in front of the slash (`hyprlang src/config.cpp:32`, `:44-64`). A file that ends on `\` is an error (`:1022-1027`).
2. Trims, strips a `#` comment, and turns `##` into one `#` (`:672-706`).
3. Splits on the first `=` and trims both sides (`:719-723`).
4. Expands `$variables` (at most 100 rounds) and `{{...}}` on the right-hand side, then removes `\` before `{` and `}` (`:732-827`). The handler sees the expanded text. The expression grammar is hyprlang's, not this note.
5. Looks up a config value named by the open category stack joined with `:`, plus the left-hand side (`:277-285`, `:337`). `animation` and `bezier` are not config values. Inside `animations { }`, the lookup name is `animations:animation`, the lookup fails, and it returns found=false (`:446-448`). `parseLine` then still tries handlers, and an unscoped handler matches the bare left-hand side (`:838-874`). The "does not exist" error is dropped when a handler matches. So both keywords fire at top level and at any category depth, including a category that is not named `animations`.
6. On a handler error, `parseFile` records it and keeps reading (`:1016-1039`). It does not roll back side effects. An unclosed `{` at end of file is another error and the category stack is cleared (`:1044-1052`). Lines already applied stay applied.

`source =` parses each glob match immediately, inline (`ConfigManager.cpp:1822-1854`). Lines after `source` in the parent file run after the sourced file. `resetHLConfig` has already cleared the tree and the bezier map.

The handler splits the right-hand side with `CVarList` defaults: comma delimiter, no last-argument collapse, empty tokens kept (`hyprutils src/string/VarList.cpp:8-26`). Each token is trimmed. There is no quote syntax. A comma always starts a new argument. An out-of-range index reads as `""` (`include/hyprutils/string/VarList.hpp:33-36`).

## 5. `animation =`

`CConfigManager::handleAnimation` (`ConfigManager.cpp:1426-1479`). The wrapper turns a returned string into a parse error (`:299-308`). No string means success.

Fields: `[0]` name, `[1]` enabled, `[2]` speed, `[3]` bezier name, `[4]` style. There is no "too many arguments" check. Field 5 and later are ignored. A comma inside the style splits it, and only the first piece is kept.

1. Name. `nodeExists` is exact and case-sensitive (`AnimationConfig.cpp:31-33`). Unknown or empty: `"no such animation"` (`ConfigManager.cpp:1432-1435`). No write.

2. Enabled is `ParserUtils::parseInt(ARGS[1]).value_or(0) == 1` (`:1438`). That is only 0 or 1, so the later rejection of any other integer (`:1440-1442`, message `"invalid animation on/off state"`) never runs. `parseInt` (`src/config/shared/parserUtils/ParserUtils.cpp:134-149`):
   - a prefix `true`, `on`, or `yes` yields 1 (case-sensitive, not the whole token: `online` and `yesterday` are 1)
   - a prefix `false`, `off`, or `no` yields 0 (`none` and `nope` are 0)
   - `0x` or `0X` hex through `strToNumber` (`hyprutils include/hyprutils/string/Numeric.hpp:31-45`) yields that integer when the rest of the token is hex
   - otherwise the whole token must be a base-10 integer (`from_chars`, no trailing junk). Failure, including empty, `1.0`, `TRUE`, and `maybe`, becomes `value_or(0)`

   If the value is not exactly 1, the off path (`:1444-1447`) writes the node with enabled 0, speed 1, bezier `default`, style empty, and returns success. Later fields are not read. So `0`, `2`, `false`, `no`, `1.0`, `maybe`, a missing second field, and `0x2` all disable the node and succeed. Only a parse of exactly 1 continues: `1`, a `true` / `on` / `yes` prefix, or `0x1`.

3. Speed, only on the on path (`:1452-1461`). `isNumber(token, true)` then `std::stof`. `isNumber` (`hyprutils src/string/String.cpp:50-84`): non-empty; an optional `-` only in position 0; digits; at most one `.`; the `.` not first; the last character a digit. Rejected: empty, `+1`, `.5`, `5.`, `1e2`, `inf`, `0x10`. There is no upper bound. `speed <= 0`, including `0` and `-0` (`stof("-0")` is `-0.0`, and `-0.0 <= 0`), returns `"invalid speed"`. A non-number also returns `"invalid speed"`. Both returns happen before `setConfigForNode`. The local stores `speed = 1.f` and `speed = 10.f` (`:1456`, `:1460`) never reach the tree. `stof` is not caught. A token that passes `isNumber` but overflows `stof` throws `std::out_of_range` out of `parseLine`, which does not catch (`hyprlang src/config.cpp:669`), and `reload` does not catch the `parse()` call either (`ConfigManager.cpp:743`).

4. The bezier name is field 3, or `""` if omitted. `bezierExists` is an exact key test (`hyprutils src/animation/AnimationManager.cpp:88-95`). Missing: `"no such bezier"` (`ConfigManager.cpp:1464-1467`) and no write. At the start of a parse the existing names are `default` and `linear` (section 7). A user curve exists only if its line succeeded earlier in this same parse.

5. The write is `setConfigForNode(name, 1, speed, field3, field4)` and it runs before the style check (`:1469-1475`). An empty style skips the check and succeeds. A non-empty style goes to `styleValidInConfigVar` (`src/animation/AnimationManager.cpp:388-457`). On failure the handler returns the error, but the write, including the child `pValues` walk, has already happened.

Style rules, first match (`AnimationManager.cpp:388-457`). A percent is parsed only to see whether `std::stoi` accepts it. The stored style is the whole token. The number is discarded.

- Name starts with `window` (`windows`, `windowsIn`, `windowsOut`, `windowsMove`):
  - `slide` plus any suffix, including `slide`, `slidefade`, `slide top`, `slide 80%`: valid, and the percent is not parsed (`:390-391`)
  - exactly `gnome` or `gnomed`: valid
  - `popin` plus any suffix: if the token contains `%`, take it from the last space and keep that space (`:397`, there is no `+ 1`), drop the last character, and `stoi`. Failure, including no space (`substr` of `npos` throws), returns `"invalid minperc"`. No `%` at all is valid and unchecked. `popin 80%` passes. `popin%` fails. `popin 80` passes. A negative number passes. There is no range check.
  - anything else: `"unknown style"`
- Name starts with `workspaces` or `specialWorkspace`, which includes the `In` and `Out` children:
  - exactly `slide`, `slidevert`, or `fade`: valid (`:411-412`)
  - otherwise `slide` plus a suffix: if `%` is present, the piece after the last space (`:418`, this one does `+ 1`; no space means the whole token) loses its last character and is `stoi`'d. Failure returns `"invalid movePerc"`. No `%` is valid. So `slidefade` and `slide top` are valid, and `slidefade 20%` is valid when the last word passes `stoi`.
  - anything else: `"unknown style"`
- Name ends with `angle` (`borderangle`, `shadowangle`, `glowangle`): exactly `loop` or `once`, otherwise `"unknown style"` (`:431-434`)
- Name starts with `layers` (`layers`, `layersIn`, `layersOut`): exactly `fade`, or `slide` plus any suffix with no percent parse, or `popin` plus a suffix under the same percent rule as windows (`"invalid minperc"`). The empty-style arm in this function is unreachable from the handler, which only calls it for a non-empty token. Anything else is `"unknown style"` (`:435-454`)
- Every other name (`global`, `border`, the whole `fade` subtree, `zoomFactor`, `monitorAdded`, `__internal_fadeCTM`): `"animation has no styles"` (`:455-456`)

The last `setConfigForNode` for a name wins. A style-invalid line is still a write. A later line can overwrite it. An off-path write replaces a previous on-path write and clears the style, forcing bezier `default` and speed 1.

## 6. What an error does

| Failure | Tree or bezier map | Parse afterwards |
|---|---|---|
| Unknown animation name | unchanged | error `"no such animation"`, later lines still run |
| Enabled token is not exactly 1 | written off: speed 1, bezier `default`, style empty | not an error |
| Bad or non-positive speed | unchanged | error `"invalid speed"`, later lines still run |
| Unknown bezier on an on-path line | unchanged | error `"no such bezier"` |
| Bad style | already written, including the bad style | error text is `unknown style`, `invalid minperc`, `invalid movePerc`, or `animation has no styles` |
| Bad bezier line | unchanged | error, later lines still run |
| Good bezier line | that key replaced or inserted | not an error |

Reload does not restore the previous tree after a bad line. The next reload starts from `reset()` again.

## 7. `bezier =`

`handleBezier` (`ConfigManager.cpp:1389-1424`). Five fields, all required: name, X0, Y0, X1, Y1. A sixth non-empty token is `"too many arguments"` (`:1418-1419`). A missing point is `"too few arguments"`. A point that fails `isNumber(..., true)` is `"invalid point"`. Each check returns before `addBezierWithName`, so a bad line stores nothing. A trailing comma is an empty sixth token and is allowed. There is no range clamp. Negatives and values outside 0 to 1 are stored. Point tokens use the same `isNumber` rules as speed. `stof` is again uncaught.

`addBezierWithName` replaces `m_mBezierCurves[name]` (`hyprutils src/animation/AnimationManager.cpp:54-58`). Redefining `default`, `linear`, or a user name overwrites that key. An empty name is a legal key when the points parse (`bezier = , 0, 0, 1, 1`).

The curve stores four points: `(0,0)`, the first user point, the second user point, `(1,1)` (`hyprutils src/animation/BezierCurve.cpp:11-16`). The JSON writer prints control points `[1]` and `[2]`, not the endpoints (`HyprCtl.cpp:966-976`).

Builtins, restored on every `resetHLConfig`:

- `removeAllBeziers` clears the map and puts `default` back (`hyprutils AnimationManager.cpp:40-46`). Its points are `(0.0, 0.75)` and `(0.15, 1.0)` (`:13`, `:16-20`).
- Legacy reset then adds `linear` at `(0,0)` and `(1,1)` (`ConfigManager.cpp:766-767`). The same add is in `CHyprAnimationManager`'s constructor (`src/animation/AnimationManager.cpp:39`).

`getBezier` of an unknown name returns `default` (`hyprutils AnimationManager.cpp:106-109`). The keyword handler does not use that fallback. It errors.

## 8. Category `animations { }`

This is not a special category. `addSpecialCategory` is used for `device`, `monitorv2`, `windowrule`, `layerrule`, and `plugin` (`ConfigManager.cpp:518-626`), not for `animations`. `animations {` is an ordinary category push (`hyprlang src/config.cpp:899-909`).

Inside it, a config left-hand side is prefixed:

- `enabled` becomes `animations:enabled`. That is a bool registered as a hyprlang `INT`, default true (`src/config/values/ConfigValues.cpp:264`; registered at `ConfigManager.cpp:495-496`). `configStringToInt` (`hyprlang src/config.cpp:185-271`) uses the same `true` / `on` / `yes` and `false` / `off` / `no` prefixes, otherwise `isNumber(..., false)` and `stoll`. A bad value errors and does not call `setFrom` (`:455-461`).
- `workspace_wraparound` becomes `animations:workspace_wraparound`, bool, default false (`ConfigValues.cpp:265`).

`animations:enabled` is read by the tick loop (`src/animation/AnimationManager.cpp:167`, `:284`). `animationsRequest` does not read it. Neither flag changes `hyprctl animations -j`.

`animation =` and `bezier =` inside the block are the unscoped handlers from section 4, not category values. Nesting does not stop them. An unknown left-hand side such as `foo = 1` is a config error, not an animation line.

Top-level `animations:enabled = 0` is the same value, because the category stack is empty and the left-hand side already contains the colon.

## 9. JSON writer

`animationsRequest` (`src/debug/HyprCtl.cpp:927-985`) is the `animations` command (`:2018`). The JSON branch (`:944-981`):

- It starts with `[[`, writes one object per node, replaces the final comma with `]` (`:962`), appends `,\n[`, writes one object per bezier, then `trimTrailingComma` (`:106-109`) drops a final comma, then appends `]]`.
- Node fields, in this order, four-space indent, comma and newline between objects: `name`, `overridden`, `bezier`, `enabled`, `speed`, `style`.
- `name` is inserted raw, not through `escapeJSONStrings`. `bezier` and `style` are escaped (`:958-959`). A bezier `name` is escaped (`:976`). The fixed node names contain no quotes, so the raw insert still parses.
- `overridden` and `enabled` are the bare tokens `true` and `false`. Enabled uses C++ truthiness of the int, so `-1` becomes `true` and `0` becomes `false` (section 3).
- `speed`, `X0`, `Y0`, `X1`, and `Y1` use `std::format` `{:.2f}`.
- Bezier objects are `name`, `X0`, `Y0`, `X1`, `Y1` from `getControlPoints()[1]` and `[2]`.
- Both containers are `std::unordered_map` (`AnimationConfig.cpp:57-58`, `AnimationManager.cpp:118-119`). The writer does not sort. Order is not alphabetical and not tree order. The frozen counter ignores order and compares sets of parsed field tuples (`c1/count.py:13-15`, `:185-190`).

`escapeJSONStrings` (`src/helpers/MiscFunctions.cpp:85-105`) maps `"` to `\"`, `\` to `\\`, and backspace, form feed, newline, CR, and tab to `\b` `\f` `\n` `\r` `\t`. Other bytes from `0x00` through `0x1f` become `\u` plus four hex digits. `/`, DEL, and non-ASCII pass through. `std::hex` and `setfill('0')` stay set on that stream. `setw` does not.

Speed is a `float` from `stof`, stored in `internalSpeed`. User bezier points are `stof` floats promoted into `Vector2D`, whose components are `double` (`hyprutils include/hyprutils/math/Vector2D.hpp:12-22`). `{:.2f}` is fixed two digits. Measured with this host's `g++ -std=c++23` `std::format`, which is the call the writer makes: the binary value rounds, not the decimal token. `8` prints `8.00`, `0.1` prints `0.10`, `0.15` prints `0.15`, `0.75` prints `0.75`, `0.125` prints `0.12`, `stof("1.005")` prints `1.00`, `stof("0.135")` prints `0.14`, `stof("3.14159")` prints `3.14`. Negative zero prints `-0.00`. A stored animation speed is never negative zero, because `<= 0` returns before the write. A bezier coordinate can be `-0.00`. Builtin `default` prints `0.00`, `0.75`, `0.15`, `1.00`. Builtin `linear` prints `0.00`, `0.00`, `1.00`, `1.00`.

The counter parses with `json.loads` and compares `json.dumps` of each field (`c1/count.py:185-190`). `8.00` and `8.0` therefore match. `true` and `false` must be JSON booleans, not `0` and `1`.

## 10. Not in the dump

- `animations:enabled` and `animations:workspace_wraparound` (section 8).
- A window-rule `animation:` value, and window or layer `no_anim` (`ConfigManager.cpp:1771-1773`, `src/config/shared/actions/ConfigActions.cpp:809-862`). Those change per-surface state, not the tree.
- Springs. The animation manager has a spring map (`hyprutils src/animation/AnimationManager.cpp:49-52`). `animations -j` does not print it, and `ConfigManager.cpp` has no legacy `spring` handler.
