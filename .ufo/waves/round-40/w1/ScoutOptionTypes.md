# ScoutOptionTypes — option types in the host's ConfigValues.cpp

Seat: ScoutOptionTypes · wave w1 · round 40 · 2026-10-25
Scope: `src/config/values/ConfigValues.cpp` at `efb50993780079460b0cbed1363e2166a2de1d9f`,
and the JSON form each registered type produces in `src/debug/HyprCtl.cpp`'s `getoption`
handler, at the same commit.

## Status (read this first)

**One registered type produces a reply form outside `int|float|str|custom`: `MS<Vec2>`
(6 keys) → JSON key `"vec2"`, an array `[x,y]`.** It is live on this host today, and the
frozen C1/C2 tooling rejects it as an error. Details and reproduction below.

Everything else is confirmed. No gaps in the type list itself.

## Sources (bytes + receipts)

| file | bytes | sha256 (prefix) | receipt |
|---|---|---|---|
| `fetch/config-values-efb5099.bin` | 59222 | `a76f05079454e1f6` | `fetch/config-values-efb5099.http.txt` |
| `fetch/hyprctl-efb5099.bin` | 97582 | `798b7c6c4c168455` | `fetch/hyprctl-efb5099.http.txt` |

Both fetched from
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/<path>`.
They are byte-identical to the pinned local checkout at `/tmp/mado40-probe/Hyprland`
(`git -C /tmp/mado40-probe/Hyprland rev-parse HEAD` = `efb50993780079460b0cbed1363e2166a2de1d9f`,
clean tree; `diff -q` on both files reported no differences).

Host: Hyprland 0.56.2, commit `efb50993780079460b0cbed1363e2166a2de1d9f`
(`hyprctl version`). Compositor verbs run: `hyprctl version`, `hyprctl getoption -j <key>`
(read-only). No other verb, no mutation.

## 1. The registered types and their counts

`ConfigValues.cpp:159-160` opens the registry:

```cpp
std::vector<SP<IValue>> Values::getConfigValues() {
#define MS makeConfigValue
```

All 353 registrations are `MS<TYPE>("key", "description", default, {...})` entries in that
one function. Counting `MS<...>(` with comments stripped (`/…/` and `//` removed):

| registered type | alias (ConfigValues.hpp:52-60) | count | live JSON form | form key |
|---|---|---|---|---|
| `Bool` | `CBoolValue` | **174** | int | `"int"` |
| `Int` | `CIntValue` | **84** | int | `"int"` |
| `Float` | `CFloatValue` | **34** | float | `"float"` |
| `String` | `CStringValue` | **28** | str | `"str"` |
| `Gradient` | `CGradientValueData` | **16** | custom | `"custom"` |
| `Vec2` | `CVec2Value` | **6** | **vec2** | **`"vec2"`** |
| `Color` | `CColorValue` | **6** | int | `"int"` |
| `CssGap` | `CCssGapValue` | **3** | custom | `"custom"` |
| `FontWeight` | `CFontWeightConfigValueData` | **2** | custom | `"custom"` |
| | | **353** | | |

Two points the type list makes that the four-form model hides:

- **`Bool` is not `"bool"`.** In the legacy manager a bool is registered as
  `Hyprlang::INT{defaultVal ? 1 : 0}` (`src/config/legacy/ConfigManager.cpp:495-496`), so
  it reads back as `"int"` (`general:allow_tearing` → `{"int": 0}`). The `"bool"` JSON key
  exists in `HyprCtl.cpp` but is not reachable on the legacy path.
- **`Color` is not `"custom"`.** `CColorValue` is registered as `Hyprlang::INT` (colour as
  an int), so it reads back as `"int"`
  (`group:groupbar:text_color` → `{"int": 4294967295}`).

## 2. The `getoption` handler and the line numbers

`src/debug/HyprCtl.cpp:1647` — `static std::string dispatchGetOption(eHyprCtlOutputFormat, std::string)`,
registered at `HyprCtl.cpp:2039` as `SHyprCtlCommand{"getoption", false, dispatchGetOption}`.

- `HyprCtl.cpp:1669-1670` — unknown key → the plain text `no such option` (not JSON).
  Verified: `hyprctl getoption -j no:such:key` → `no such option`, exit 0.
- `HyprCtl.cpp:1700` — the JSON branch (`else` of `format == FORMAT_NORMAL`).
- `HyprCtl.cpp:1701-1728` — one `else if` per type; each `return` writes
  `{"option": "<key>", "<form>": <value>, "set": <bool> }`.
- `HyprCtl.cpp:1731` — `return "invalid type (internal error)";` — the fallthrough when no
  branch matches. **Not JSON.** Not reachable on the host (see §4).

The JSON-branch form keys and their emitting lines:

| line | type test | JSON key |
|---|---|---|
| 1701-1702 | `typeid(Config::INTEGER)` | `"int"` |
| 1703-1704 | `typeid(Config::BOOL)` | `"bool"` |
| 1705-1706 | `typeid(Config::FLOAT)` | `"float"` |
| 1707-1709 | `typeid(Config::VEC2)` | `"vec2"` |
| 1710-1712 | `typeid(Hyprlang::VEC2)` | `"vec2"` |
| 1713-1714 | `typeid(Hyprlang::STRING)` | `"str"` |
| 1715-1716 | `typeid(Config::STRING)` | `"str"` |
| 1717-1719 | `typeid(void*)` | `"custom"` |
| 1720-1721 | `typeid(Config::IComplexConfigValue)` | `"custom"` |
| 1722-1723 | `typeid(Config::CCssGapData)` | `"css"` |
| 1724-1725 | `typeid(Config::CGradientValueData)` | `"gradient"` |
| 1726-1728 | `typeid(Config::CFontWeightConfigValueData)` | `"font_weight"` |

So `HyprCtl.cpp` can emit **nine** distinct JSON form keys: `int, bool, float, vec2, str,
custom, css, gradient, font_weight` — plus the `no such option` text and the
`invalid type (internal error)` text.

## 3. The finding: `Vec2` → `"vec2"`, outside the four forms

`MS<Vec2>` (6 keys) is registered as `Hyprlang::VEC2` in the legacy manager
(`src/config/legacy/ConfigManager.cpp:501-502`), i.e. `Hyprlang::SVector2D`
(`include/hyprlang.hpp:45`, `struct SVector2D { float x = 0, y = 0; }`). The reply is
therefore produced by `HyprCtl.cpp:1710-1712`:

```cpp
else if (TYPE == typeid(Hyprlang::VEC2))
    return std::format(R"({{"option": "{}", "vec2": [{},{}], "set": {} }})", curitem, …);
```

All six registered Vec2 keys, live on the host right now:

```
decoration:shadow:offset              {"option": "decoration:shadow:offset", "vec2": [0,0], "set": false }
input:tablet:region_position          {"option": "input:tablet:region_position", "vec2": [0,0], "set": false }
input:tablet:region_size              {"option": "input:tablet:region_size", "vec2": [0,0], "set": false }
input:tablet:active_area_size         {"option": "input:tablet:active_area_size", "vec2": [0,0], "set": false }
input:tablet:active_area_position     {"option": "input:tablet:active_area_position", "vec2": [0,0], "set": false }
layout:single_window_aspect_ratio     {"option": "layout:single_window_aspect_ratio", "vec2": [0,0], "set": false }
```

### Full-registry census (all 353 registered keys, live)

```
FORM CENSUS over ALL registered keys
  int              264
  float             34
  str               28
  custom            21
  vec2               6     <-- fifth form
```

Type → live form, one-to-one and exhaustive:

```
  Bool         {'int': 174}
  Color        {'int': 6}
  CssGap       {'custom': 3}
  Float        {'float': 34}
  FontWeight   {'custom': 2}
  Gradient     {'custom': 16}
  Int          {'int': 84}
  String       {'str': 28}
  Vec2         {'vec2': 6}
```

The host's own tree census (`c1/native-capture.jsonl`, 70 keys) shows only `int 44,
float 5, custom 13, str 8` — **no `vec2`** — because the 70 keys that the capture walked
are the keys the host's *config trees* declare, and the host's trees declare no Vec2 key
(`.config/hypr/looknfeel.conf:33` has `# single_window_aspect_ratio = 1 1`, commented
out). The 70-key capture therefore cannot see the fifth form. The registry-wide census
above does.

### Why this breaks the frozen tooling

`c1/ctl-ref-tool.py.txt:638-640` (the reference tool, a CONTROL):

```python
forms = [f for f in ("int", "float", "str", "custom") if f in rec]
if not isinstance(rec, dict) or len(forms) != 1 or "set" not in rec:
    raise CtlError("%s: unknown reply form from %s" % (key, hyprctl))
```

`quality/counters/c1-r40-live.py:99` — `FORMS = ("int", "float", "str", "custom")`.

Reproduced against the live host, using the frozen control:

```
$ python3 -I ref.py --live --home "$HOME" --probe layout:single_window_aspect_ratio
exit=5
mado-options.py: layout:single_window_aspect_ratio: unknown reply form from hyprctl
```

and with a config tree that *declares* the real Vec2 key:

```
$ cat $T/.config/hypr/hyprland.conf
layout { single_window_aspect_ratio = 1.6 1.0 }
$ python3 -I ref.py --live --home "$T"
exit=5
mado-options.py: layout:single_window_aspect_ratio: unknown reply form from hyprctl
```

Note the second case: the exit-5 is reported as a *compositor failure* naming the key,
which is the wrong diagnosis — the compositor answered correctly, in a fifth form the tool
does not model. The counter's stub (`c1-r40-live.py:410-429`) can only emit `int|float|
str|custom` or `no such option` (the stub writes back a fixed `table.json` whose records
are built from `form` ∈ {int,float,str,custom}), so **no C1 fixture can reach this case**:
`grep -c vec2 quality/counters/c1-r40-live.py` → `0`.

The same four-form assumption is written into the C2 deliverable's scope
(`registration.md`: "Native replies are compared in their native forms (`int`, `float`,
`str`, `custom`)") and into the provisional facts this seat was handed ("native
`hyprctl getoption -j KEY` replies are one JSON object … form in int|float|str|custom").

### What the tool must do instead

A `vec2` reply must be recognised as a valid native form and compared as a two-number
tuple, matching how the legacy manager stores it: `Hyprlang::VEC2` = `SVector2D{float x,
float y}`, printed as `[{},{}]` — no space after the comma (`HyprCtl.cpp:1708`/`:1711`),
values are floats formatted by `std::format` (e.g. `[0,0]`). The declared side is a
space-separated pair in the config tree (`1.6 1.0`); the same whitespace-separated-tuple
rule the tool already applies to CSS gaps is the natural comparison.

## 4. Forms that exist in `HyprCtl.cpp` but are unreachable on this host

The legacy (hyprlang) manager is the one in force on this host — `.config/hypr/hyprland.conf`,
not a `.lua` config, so `src/config/ConfigManager.cpp:37-41` selects
`Legacy::CConfigManager`. Under it, the legacy manager registers every `Values::` type
into hyprlang's `INT / FLOAT / VEC2 / STRING / CConfigCustomValueType`
(`src/config/legacy/ConfigManager.cpp:488-511`), and `CConfigManager::getConfigValue`
(`src/config/legacy/ConfigManager.cpp:1169-1184`) returns hyprlang's own
`CConfigValue::getValue().type()` — i.e. `int64_t`, `float`, `const char*`,
`SVector2D`, or `void*` for a custom type (`include/hyprlang.hpp:260-270`). So the
reachable branches on this host are exactly:

- `int` (from `Config::INTEGER` = `int64_t`) — `HyprCtl.cpp:1701`
- `float` — `HyprCtl.cpp:1705`
- `str` (from `Hyprlang::STRING` = `const char*`) — `HyprCtl.cpp:1713`
- `vec2` (from `Hyprlang::VEC2`) — `HyprCtl.cpp:1710`
- `custom` (from `void*`) — `HyprCtl.cpp:1717`

Therefore these four JSON keys are **unreachable on this host** and must not be claimed as
host-observed: `"bool"` (1703), `"css"` (1722), `"gradient"` (1724), `"font_weight"`
(1726), and the `"invalid type (internal error)"` fallthrough (1731). They belong to the
**Lua** config manager path, whose `underlying()` returns the native C++ type directly
(`src/config/lua/types/LuaConfigBool.cpp:30-31` → `typeid(bool)`,
`LuaConfigCssGap.cpp:70-71` → `typeid(CCssGapData)`,
`LuaConfigGradient.cpp:88-89` → `typeid(CGradientValueData)`,
`LuaConfigFontWeight.cpp:47-48` → `typeid(IComplexConfigValue*)`,
`LuaConfigVec2.cpp:66-67` → `typeid(Config::VEC2)`).

One nuance worth recording: `CssGap`, `Gradient` and `FontWeight` are registered as
hyprlang **custom** types on the legacy path, so they answer `"custom"` — the `"css"`,
`"gradient"` and `"font_weight"` keys only fire under the Lua manager. On the host the
three of them are indistinguishable from each other by form; they are told apart by the
*value's shape*, which is exactly what the reference tool's `native_equal` already does
(`c1/ctl-ref-tool.py.txt:608` for gradients, `:196` `gap_text` for gaps). Confirmed live:

```
general:gaps_in                     {"custom": "0 0 0 0"}
group:groupbar:font_weight_active   {"custom": "1000"}
general:col.active_border           {"custom": "ffe68e0d 45deg"}
```

## 5. Other measured facts

- `device:*` category values are **not** reachable by `getoption`:
  `hyprctl getoption -j device:sensitivity` → `no such option` (exit 0). The
  device-*parent* names from `ConfigValues.hpp:139-160` (`input:sensitivity` etc.) are
  reachable and answer `int 9 / float 2 / str 9` — all within the four forms.
- `autogenerated` → `{"int": 0, "set": false}` (registered at
  `src/config/legacy/ConfigManager.cpp:513`).
- `plugin:<name>` keys answer `no such option` when no plugin is loaded
  (`legacy/ConfigManager.cpp:1170-1178`).
- `hyprctl getoption -j <unknown>` → `no such option`, **exit 0** (not a non-zero exit).

## 6. Confidence

| claim | confidence | basis |
|---|---|---|
| 353 registered options, 9 types, counts in §1 | **certain** | parsed from the pinned bytes; comment-stripped count reconciles with the raw count (353 = 353) |
| `Vec2` → `"vec2"`, 6 keys | **certain** | source lines 1710-1712 + live reply for all 6 keys + full 353-key live census |
| `Bool`/`Color` → `"int"`; `CssGap`/`Gradient`/`FontWeight` → `"custom"` on this host | **certain** | source mapping `legacy/ConfigManager.cpp:488-511` + live replies |
| `"bool"`/`"css"`/`"gradient"`/`"font_weight"`/`invalid type` unreachable on this host | **high** | source: legacy manager returns hyprlang's value type; host runs the legacy manager (`ConfigManager.cpp:37-41`, `.conf` not `.lua`) |
| the reference tool exits 5 on a live `vec2` reply | **certain** | reproduced twice against the live host (probe and tree-declared), exit 5 both times |
| no C1 fixture can reach the `vec2` case | **certain** | `grep -c vec2 quality/counters/c1-r40-live.py` → 0; the stub's table records are built only from `form` ∈ {int,float,str,custom} |

Remaining unknown (out of my seat's scope, flagged not resolved): whether the C1/C2
deliverables will be amended to model `vec2`, or whether the `vec2` case is deliberately
excluded and declared as a residual. The registration's declared residual for C1 covers
only "a tool that hardcodes the reference model's conversion tables for this generator's
value space" — it does not cover "the compositor has a fifth reply form".

## 7. Commands run (all read-only)

```
git -C /tmp/mado40-probe/Hyprland rev-parse HEAD
git -C /tmp/mado40-probe/Hyprland status --porcelain
curl -sSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099.../src/config/values/ConfigValues.cpp
curl -sSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099.../src/debug/HyprCtl.cpp
diff -q <fetched> <local tree>
hyprctl version
hyprctl getoption -j <key>          # 353 registry keys + 20 device parents + edge cases
python3 -I ref.py --live --home "$HOME" [--probe layout:single_window_aspect_ratio]
```

No `hyprctl` verb other than `getoption -j` and `version` was run. No config tree,
compositor state, service or sibling path was modified. Scratch dirs
`/tmp/scout-opt-*` created under `mktemp -d` and removed.

## Tooling

No tool installed. `curl`, `python3`, `git` and `hyprctl` (host) already present; the
Hyprland source tree was already fetched at `/tmp/mado40-probe/Hyprland` by another seat
at the pinned commit — I read it and independently re-fetched both files over HTTPS,
confirming byte equality rather than trusting the local copy.
