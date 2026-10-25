# ScoutGetoptionHandler — HyprCtl.cpp getoption handler (Hyprland efb5099)

Scope: locate the `getoption` handler in Hyprland v0.56.2 (commit
`efb50993780079460b0cbed1363e2166a2de1d9f`), report exact output format strings, the
`no such option` path and its exit status, the `set` field's meaning, and how complex types
print. Quotes <= 25 words, with line numbers.

## Provenance of the source read (re-derived, not taken from the brief)

- Read-only git checkout present at `/tmp/mado40-probe/Hyprland`; `git rev-parse HEAD` =
  `efb50993780079460b0cbed1363e2166a2de1d9f`; `git describe --tags` = `v0.56.2`;
  `cat VERSION` = `0.56.2`.
- Host binary agrees: `hyprctl version` prints
  `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean`.
- The same handler file exists as a bare copy at `/tmp/r40src/HyprCtl.cpp` (2346 lines) — byte
  identical size to the checkout copy; I read the checkout (line numbers below are from it).
- Hyprlang side: installed header `/usr/include/hyprlang.hpp` (hyprlang 0.6.8) plus the
  source copies `/tmp/r40src/hyprlang-config.cpp`, `/tmp/r40src/hl-config.cpp`,
  `/tmp/r40src/hl-common.cpp` (hyprlang rev pinned by the checkout's `flake.lock`:
  `090117506ddc3d7f26e650ff344d378c2ec329cc`).
- Verbs run against the host: `hyprctl version`, `hyprctl getoption [-j] <key>` only
  (read-only). No mutating verb, no pacman, no config write.

## 1. Where the handler lives

- `src/debug/HyprCtl.cpp:1647` — `static std::string dispatchGetOption(eHyprCtlOutputFormat format, std::string request) {`
- `src/debug/HyprCtl.cpp:2039` — `registerCommand(SHyprCtlCommand{"getoption", false, dispatchGetOption});`
  (`exact = false`, so the command is matched by prefix — see §6.)
- Dispatch entry: `src/debug/HyprCtl.cpp:2062` `std::string CHyprCtl::getReply(std::string request) {`
  strips the flag prefix, then matches the command and calls `cmd->fn(format, request)`.

### Request → key

The handler receives the request **including the command word**, and consumes two tokens:

- `src/debug/HyprCtl.cpp:1650-1662` — `nextItem()` lambda: splits on the first space, `curitem = trim(curitem);`
- `src/debug/HyprCtl.cpp:1664-1665` — `nextItem();` / `nextItem();` (twice: token 1 = command, token 2 = key)
- `src/debug/HyprCtl.cpp:1667` — `const auto VAR = Config::mgr()->getConfigValue(curitem);`

The echoed `"option"` value in the JSON reply is exactly `curitem`, i.e. the key as the user
typed it (trimmed). Live: `hyprctl getoption -j general:col.active_border` →
`{"option": "general:col.active_border", ... }`.

Key lookup is exact-match, no normalisation:
- `src/config/legacy/ConfigManager.cpp:1169-1184` — `SConfigOptionReply CConfigManager::getConfigValue(const std::string& val)`
  returns `{}` (null `dataptr`) when absent; a `plugin:` prefix is special-cased.
- hyprlang `hl-config.cpp:1082-1086` — `CConfigValue* CConfig::getConfigValuePtr(const char* name)` does a plain map lookup.
Live: `hyprctl getoption gaps_in` → `no such option` (the category prefix is mandatory).

## 2. The `no such option` path and its exit status

Server side (one guard, **before** the format split):

- `src/debug/HyprCtl.cpp:1669-1670` —
  `if (!VAR.dataptr)` / `return "no such option";`

Consequences that matter for a client:

1. The reply is the bare string `no such option` — **not** a JSON object, in `-j` mode too.
   It is emitted before `if (format == FORMAT_NORMAL)`, so both formats get the same text.
2. The client prints the reply and exits **0**:

   - `hyprctl/src/main.cpp:275` — `log(reply);`
   - `hyprctl/src/main.cpp:277-278` — `if (reply.starts_with("error:"))` / `return 7;`
   - `hyprctl/src/main.cpp:280` — `return 0;`

   So the only non-zero exit the IPC layer produces from a *reply* is 7, and only for a reply
   literally starting with `error:`. `no such option` does not, hence exit 0.

Live verification (host, read-only):

```
$ hyprctl getoption -j no:such:option ; echo "exit=$?"
no such option
exit=0
$ hyprctl getoption -j no:such:option 1>/dev/null ; echo "(stderr above)"
(stderr above)          <- nothing on stderr; the text goes to stdout
$ hyprctl getoption no:such:option ; echo "exit=$?"
no such option
exit=0
```

Other failure paths of the *client* (not of getoption), `hyprctl/src/main.cpp`:

| line | condition | exit |
|---|---|---|
| 206 | `SERVERSOCKET < 0` (socket open) | 1 |
| 212 | `setsockopt` timeout | 2 |
| 219 | not enough args (`minArgs`) | -1 |
| 224 | `HYPRLAND_INSTANCE_SIGNATURE` empty inside `request()` | 3 |
| 236 | `connect()` failed | 4 |
| 241 | `writeAll` failed | 5 |
| 262 | read failed / timeout | 6 |
| 277-278 | reply starts with `error:` | 7 |
| 490, 516 | instance signature missing before the request | 1 |

Live: `env -u HYPRLAND_INSTANCE_SIGNATURE hyprctl getoption -j general:layout` →
`HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)`, exit 1 (main.cpp:515-516).

**Reading for the C1 claim:** the compositor never signals "unknown key" by exit status; it
signals it by the *text* `no such option` with exit 0. A tool that treats non-zero exit as
failure and zero exit as success will read the text to distinguish "no such option" from a
value — matching the claim's wording ("native replies … or the text `no such option`").
Also note the **name collision**: hyprctl's own exit 5 means "couldn't write to socket"
(main.cpp:241), unrelated to a `getoption` key.

An unknown *command* (not key) is a different string:
`src/debug/HyprCtl.cpp:2124` — `return "unknown request";` (also exit 0).

## 3. The `set` field's meaning

The field is `VAR.setByUser`, threaded from the config manager into the reply:

- `src/config/ConfigManager.hpp:24` — `bool setByUser = false;` (member of `SConfigOptionReply`)
- `src/config/legacy/ConfigManager.cpp:1176` and `:1183` —
  `return {.dataptr = VAL->getDataStaticPtr(), .type = &VAL->getValue().type(), .setByUser = VAL->m_bSetByUser};`
- hyprlang `hl-config.hpp` / installed header `/usr/include/hyprlang.hpp:275-278` —
  "a flag to notify whether this value has been set explicitly by the user, or not." / `bool m_bSetByUser = false;`
- hyprlang `hyprlang-config.cpp:513` — `VALUEIT->second.m_bSetByUser = true;` (end of
  `configSetValueSafe`, i.e. set when a config **line** assigns the value)
- hyprlang `hl-common.cpp:122` — `m_bSetByUser = false;` (end of `defaultFrom`, i.e. reset when
  the built-in default is re-applied)

Semantics: `set` = "some parsed config line assigned this key", **not** "differs from the
default" and **not** "the key exists in a user file". Defaults applied by the compositor keep
`set: false`; a key assigned by any sourced file (including the compositor's own defaults
tree, which is `source`d from `hyprland.conf`) becomes `set: true`.

Live discriminating evidence:

```
$ hyprctl getoption -j cursor:no_hardware_cursors
{"option": "cursor:no_hardware_cursors", "int": 2, "set": false }   # untouched default
$ hyprctl getoption -j general:border_size
{"option": "general:border_size", "int": 0, "set": true }          # assigned by a sourced file
$ hyprctl getoption -j debug:overlay
{"option": "debug:overlay", "int": 0, "set": false }
```

and the frozen capture agrees for every declared key:
`quality` receipt `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/c1/native-capture.jsonl`
— 70/70 lines carry `"set": true`, and every one of those 70 keys is declared in a file the
static table names (e.g. `cursor:warp_on_change_workspace` → owner
`.local/share/omarchy/default/hypr/looknfeel.conf` line 137).

Caveat for the tool: because the compositor's own defaults tree is *sourced* into
`hyprland.conf`, its assignments also read `set: true`. `set` therefore does **not** separate
"omarchy default" from "user override"; it separates "assigned by a config line" from
"never assigned".

## 4. Exact output format strings

### JSON branch (`-j`), `src/debug/HyprCtl.cpp:1701-1729`

Every line is one `std::format` with a raw-string literal; the literal contains `{{`/`}}`
(escaped braces). Exact formats:

| line | format literal (verbatim) |
|---|---|
| 1702 | `R"({{"option": "{}", "int": {}, "set": {} }})"` |
| 1704 | `R"({{"option": "{}", "bool": {}, "set": {} }})"` — bool as literal `true`/`false` |
| 1706 | `R"({{"option": "{}", "float": {:2f}, "set": {} }})"` |
| 1708-1709 | `R"({{"option": "{}", "vec2": [{},{}], "set": {} }})"` |
| 1711-1712 | `R"({{"option": "{}", "vec2": [{},{}], "set": {} }})"` (Hyprlang::VEC2) |
| 1714 | `R"({{"option": "{}", "str": "{}", "set": {} }})"` — value via `escapeJSONStrings(...)` |
| 1716 | `R"({{"option": "{}", "str": "{}", "set": {} }})"` (Config::STRING, **no** escaping) |
| 1718-1719 | `R"({{"option": "{}", "custom": "{}", "set": {} }})"` |
| 1721 | `R"({{"option": "{}", "custom": "{}", "set": {} }})"` |
| 1723 | `R"({{"option": "{}", "css": "{}", "set": {} }})"` |
| 1725 | `R"({{"option": "{}", "gradient": "{}", "set": {} }})"` |
| 1727-1728 | `R"({{"option": "{}", "font_weight": "{}", "set": {} }})"` |

Shape facts that a parser must know:

- There is a **space before the closing brace**: the reply is `{"option": "K", "int": 1, "set": true }`
  (byte-exact: `cat -A` on the capture shows `"set": true }$`, and live
  `hyprctl getoption -j general:layout | cat -A` → `{"option": "general:layout", "str": "dwindle", "set": true }$`).
- `{:2f}` is std::format's *width* 2, not precision — the default float presentation of type
  `f` is 6 decimals (printf-like). Live: `"float": 0.600000`, `"float": 0.000000`,
  `"float": 0.490000`. The capture preserves the same text (`"float": 0.600000`).
- Exactly one value key per reply, besides `option` and `set`.
- The `str` value is escaped **only** on the `Hyprlang::STRING` branch (line 1714,
  `escapeJSONStrings`, `src/helpers/MiscFunctions.cpp:85`); the `Config::STRING` branch (1716)
  is unescaped, and the `custom` values (1718/1721) are unescaped too.

### Text branch (no `-j`), `src/debug/HyprCtl.cpp:1676-1699`

| line | format literal |
|---|---|
| 1677 | `"int: {}\nset: {}"` |
| 1679 | `"bool: {}\nset: {}"` |
| 1681 | `"float: {:2f}\nset: {}"` |
| 1683 | `"vec2: [{}, {}]\nset: {}"` |
| 1685 | `"vec2: [{}, {}]\nset: {}"` |
| 1687 | `"str: {}\nset: {}"` |
| 1689 | `"str: {}\nset: {}"` |
| 1691 | `"custom type: {}\nset: {}"` |
| 1693 | `"custom type: {}\nset: {}"` |
| 1695 | `"css gap data: {}\nset: {}"` |
| 1697 | `"gradient data: {}\nset: {}"` |
| 1699 | `"font weight data: {}\nset: {}"` |

Fallback when no type matches: `src/debug/HyprCtl.cpp:1731` — `return "invalid type (internal error)";`

Live text replies: `hyprctl getoption general:col.active_border` →
`custom type: ffe68e0d 45deg` + `set: true`.

## 5. How complex types print

### Which branch the host actually takes

`TYPE` is `std::type_index(*VAR.type)` (`src/debug/HyprCtl.cpp:1673`), and in the legacy
(hyprlang) manager `VAR.type = &VAL->getValue().type()` (`src/config/legacy/ConfigManager.cpp:1176`).
For a **custom** value hyprlang's `getValue()` returns
`std::any(reinterpret_cast<CUSTOMTYPE*>(m_pData)->data)` — a `void*` — so `TYPE == typeid(void*)`
and the reply takes the `void*` branch:

- `src/debug/HyprCtl.cpp:1718-1719` — `rc<Config::IComplexConfigValue*>((*rc<Hyprlang::CUSTOMTYPE* const*>(VAL))->getData())->toString()`

Consequence (host is the legacy manager: `src/config/ConfigManager.cpp:31-45` selects the Lua
manager only when the config file extension is `.lua`; the host uses `hyprland.conf`):
**gradients, CSS gaps and font weights all arrive under the JSON key `custom`**, never under
`gradient` / `css` / `font_weight`. The `css`/`gradient`/`font_weight` keys (1723/1725/1727) and
the `bool` key (1704) are reachable only under the **Lua** manager, whose `underlying()` returns
the concrete typeid (`src/config/lua/types/LuaConfigGradient.cpp:88-90`,
`LuaConfigCssGap.cpp:70-72`, `LuaConfigBool.cpp:30-32`, `LuaConfigFontWeight.cpp:47-49`).

Live confirmation that the host is legacy-shaped:

```
$ hyprctl getoption -j general:gaps_in
{"option": "general:gaps_in", "custom": "0 0 0 0", "set": true }
$ hyprctl getoption -j group:groupbar:font_weight_active
{"option": "group:groupbar:font_weight_active", "custom": "1000", "set": true }
```

Host capture shape agrees: `int` 44, `float` 5, `custom` 13, `str` 8 = 70 keys, no `bool`,
no `vec2`, no `css`/`gradient`/`font_weight`
(`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/c1/native-capture.jsonl`).

### The `toString()` implementations (what the complex value prints)

`src/config/shared/complex/ComplexDataTypes.hpp`:

- Gradient, `:69-77`:
  `result += std::format("{:x} ", c.getAsHex());` (per colour, trailing space) and
  `result += std::format("{}deg", sc<int>(m_angle * 180.0 / M_PI));`
- CSS gap, `:133-135`: `return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);`
- Font weight, `:154-156`: `return std::format("{}", m_value);`

So the gradient form is `<argb-hex> <argb-hex> … <N>deg`: each colour is lowercase, **unpadded**
hex of the ARGB-packed `uint32` (hence 8 digits only when the value ≥ 0x10000000), each followed
by a space, and the angle last as an integer number of degrees.
`src/helpers/Color.cpp:27-30` —
`uint32_t CHyprColor::getAsHex() const { return sc<uint32_t>(a * 255.f) * 0x1000000 + ... }`
→ channel order is **A,R,G,B** (alpha in the top byte).

Live/captured gradient strings, matching the source rule:

- `general:col.active_border` → `ffe68e0d 45deg` (one colour `rgb(e68e0d)` = alpha ff, then angle)
- `group:col.border_locked_active` → `ee33ccff ee00ff99 45deg` (two colours, one space each)
- `group:groupbar:col.active` → `40000000 0deg`; `general:col.inactive_border` → `aa595959 0deg`
- `decoration:shadow:color` → `ee1a1a1a 0deg`

CSS gap always prints **four** numbers (top right bottom left) even when the config declared a
single value: `general:gaps_in` → `0 0 0 0` while the toggles file declares `gaps_in = 0`
(`/home/vgpnk/.local/state/omarchy/toggles/hypr/window-no-gaps.conf:4`). The 1→4 expansion is
`CCssGapData::parseGapData` (`ComplexDataTypes.hpp:96-120`).

Font weight prints the numeric weight, not the name: `group:groupbar:font_weight_active` →
`1000`, `…font_weight_inactive` → `400`; the name→number map is
`CFontWeightConfigValueData::WEIGHTS` (`ComplexDataTypes.hpp:157-160`, e.g. `ultraheavy`→1000).

### Why `45deg` appears on a single-colour declaration (angle inheritance, at source level)

- `src/config/legacy/ConfigManager.cpp:103` — `static Hyprlang::CParseResult configHandleGradientSet(const char* VALUE, void** data) {`
- `src/config/legacy/ConfigManager.cpp:112` — `DATA->m_colors.clear();` (colours are cleared)
- `src/config/legacy/ConfigManager.cpp:120` — `DATA->m_angle = std::stoi(...) * (std::numbers::pi / 180.0);`
  (the angle is written **only** inside the branch that saw a `deg` token)

The handler clears the colour list but never resets `m_angle`; a redeclaration without a `deg`
token therefore keeps the previous declarer's angle. Host evidence:

- defaults tree `/home/vgpnk/.local/share/omarchy/default/hypr/looknfeel.conf:4` —
  `$activeBorderColor = rgba(33ccffee) rgba(00ff99ee) 45deg`; `:15` `col.active_border = $activeBorderColor`
- theme `/home/vgpnk/.config/omarchy/current/theme/hyprland.conf:1` —
  `$activeBorderColor = rgb(e68e0d)`; `:4` `col.active_border = $activeBorderColor`
- source order: `/home/vgpnk/.config/hypr/hyprland.conf:10` sources the defaults tree,
  `:13` sources the theme → the theme's single colour lands last, the angle survives.

Live read: `hyprctl getoption -j general:col.active_border` →
`{"option": "general:col.active_border", "custom": "ffe68e0d 45deg", "set": true }`.

This is the mechanism behind the C2 "angle inheritance" rule; it is a property of the
**gradient handler** (`ConfigManager.cpp`), surfaced through the `custom` string that
`HyprCtl.cpp` prints.

## 6. Two more handler behaviours a client can trip on

- **Prefix matching.** `getoption` is registered with `exact = false`
  (`src/debug/HyprCtl.cpp:2039`), and non-exact commands are matched by
  `request.starts_with(cmd->name)` (`src/debug/HyprCtl.cpp:2113-2122`). Live:
  `hyprctl getoptionx -j foo` → `no such option` (it is dispatched as a getoption whose key
  token is `foo`), not `unknown request`.
- **Keys with spaces are truncated.** `nextItem()` splits on the first space only
  (`src/debug/HyprCtl.cpp:1651`), so a key containing a space can never be addressed.
  Live: `hyprctl getoption -j "general:col.active border"` → `no such option`.

## 7. Confidence and remaining unknowns

High confidence (source + host agreement, both re-derived here):
format strings, `no such option` text/exit 0, the `set` semantics, complex-type printing
(`custom` under the legacy manager), gradient hex/degree rendering, angle inheritance.

Open / not established by me:
- The Lua-manager variants (`bool`, `vec2`, `css`, `gradient`, `font_weight` keys) are read
  from source only; the host runs the legacy manager, so no live confirmation was possible
  (no host mutation was performed or attempted).
- The `std::format` `{:2f}` width-vs-precision reading is confirmed empirically (6 decimals
  in live output) rather than by a std::format standard citation.
- `escapeJSONStrings` (`src/helpers/MiscFunctions.cpp:85`) escapes `"`, `\`, and control chars;
  no host key exercised a non-trivial escape case, so its effect on a `str` reply is
  source-derived only.

Tools installed: none (no package manager used, no new binaries).
Report: `.ufo/waves/round-40/w1/ScoutGetoptionHandler.md`
