# Held citations for `hyprland-dispatcher-dispatch-r51.md`

Every citation below resolves at the round base `6ca8c559a4a3d6d361101592116eea2bc7452437`
(`git show 6ca8c559:corpus/knowledge/<file>`), the tokens on the `held:` line appear verbatim and
case-sensitively on that line, and the entry cites no held fact that is not listed here. The `held:`
lines are also in the entry itself, so the freeze can read them from either file.

| # | held citation | key tokens | verification line text (verbatim, at base) |
|---|---|---|---|
| 1 | `corpus/knowledge/bind-table-r25.md:38` | `DISPATCHER`, `ARG`, `numbArgs` | A regular bind uses `MOD, KEY, DISPATCHER, ARG`; `d` inserts a description before the dispatcher, `k` adds a device field, and the parser sets its field count from those flags. [S162, pinned `ConfigManager.cpp:1554-1558,1580-1586`, quotes: “const int numbArgs = (hasDescription ? 5 : 4) + sc<int>(isPerDevice);”; “const auto DESCRIPTION = hasDescription ? ARGS[2 + DEVICE_OFFSET] : "";”] |
| 2 | `corpus/knowledge/bind-table-r25.md:52` | `dispatcher` | Too few or too many fields, an unknown dispatcher, an invalid nonempty modifier string, and `catchall` outside a submap are rejected before a bind is added. [S162, pinned `ConfigManager.cpp:1559-1562,1594-1604,1616-1624`, quotes: “return "bind: too few args";”; “return "bind: too many args";”; “Invalid dispatcher, requested”; “Invalid mod, requested mod”; “Catchall not allowed outside of submap!”; “g_pKeybindManager->addKeybind”] |
| 3 | `corpus/knowledge/keybind-rule-semantics.md:73` | `params`, `comma-separated` | - Comma rule: the fixed fields are comma-separated, but a dispatcher's `params` may itself |
| 4 | `corpus/knowledge/keybind-rule-semantics.md:55` | `submap` | m 2, r 1). `submap` is `""` on all 192 (no submaps in the plane). `catch_all` 0. |
| 5 | `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md:48` | `submap`, `pass`, `send_shortcut` | `exec_cmd`, `exec_raw`, `focus`, `exit`, `submap`, `pass`, `send_shortcut`, |
| 6 | `corpus/knowledge/hyprland-bind-key-match-r50.md:57` | `CVarList`, `numbArgs` | 1. **The handler.** `bind` and its flag variants land in one handler registered as `"bind"` … the value is split into at most four (five with `d`, plus one with `k`) comma arguments `const auto ARGS     = CVarList(value, numbArgs);`(Hyprland-legacy-ConfigManager.cpp:1555) … |
| 7 | `corpus/knowledge/hyprland-config-era-r12.md:41` | `hyprland.lua`, `hyprland.conf` | \| `hyprland.lua` exists \| `hyprland.lua` instead of `hyprland.conf` \| `[INF-docs]` S024, “Lua configs” \| |

## What each citation is used for in the entry

1. **bind-table-r25:38** - the fixed fields of a bind line and the field count the parser derives
   from flags. Used in step 2 (the dispatcher field is taken by position) and step 7 (the last
   field is the rest of the line).
2. **bind-table-r25:52** - an unknown dispatcher is refused before a bind is added. Used in step 2
   as the reason a name is a config-time commitment.
3. **keybind-rule-semantics:73** - a dispatcher's params may itself contain commas. Used in step 7
   for `exec` keeping `foo, bar` intact versus `sendshortcut` rejecting a fourth field.
4. **keybind-rule-semantics:55** - this host's bind plane carries no submap on any of its 192
   binds. Used in Limits (no host observation of a submap switch exists).
5. **dispatcher-surface-and-request-grammar-r26:48** - `submap`, `pass` and `send_shortcut` are in
   the documented dispatcher vocabulary of the 0.56 line. Used to justify naming those three as the
   special handlers a reader will meet, without claiming anything about their hyprlang spelling.
6. **hyprland-bind-key-match-r50:57** - the round-50 parse account, including `CVarList(value,
   numbArgs)`. Used as the boundary sentence: the match chain and the parser are that entry's
   ground, and this one starts after them.
6. **hyprland-config-era-r12:41** - the presence of `hyprland.lua` selects the Lua manager and its
   absence leaves `hyprland.conf`. Used in step 9 to decide which branch the socket verb takes on a
   directory that holds only the `.conf` file.

## Checks run

- `git show 6ca8c559:corpus/knowledge/<file> | sed -n '<line>p'` for all six, 2026-10-27.
- Each token list was matched against that printed line by eye and by the C2 counter's own
  `clause_d` (see `counter-fit-receipt.txt`: `d ok=1 held=7/3 lines=8 untargeted=1 tokens=14`).
- No held citation names a file that is absent at base, and no two citations name the same
  `file:line`.
