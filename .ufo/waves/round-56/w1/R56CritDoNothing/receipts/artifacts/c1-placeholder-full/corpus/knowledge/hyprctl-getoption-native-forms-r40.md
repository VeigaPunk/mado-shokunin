# What `hyprctl getoption -j` answers: five native forms, and how a declared string meets them

source: S158 - Hyprland v0.56.2 HyprCtl.cpp (the getoption handler)
source: S162 - Hyprland ConfigManager.cpp (the gradient handler)
source: S173 - hyprlang v0.6.8 config.cpp (configStringToInt, the vec2 parser)
source: S180 - Hyprland ComplexDataTypes.hpp (gap and font-weight value types)
source: S181 - Hyprland ParserUtils.cpp (parseColor)
source: S215 - Hyprland ConfigValues.cpp (the registered option types)
source: S278 - Hyprland wiki 0.54.0, Using hyprctl
source: S279 - own-work: the live census receipt of `tools/mado-options.py --live`
verified-at: 2026-10-25
recheck: on-change

Lane: mado-shokunin. Round 40 (C2 coverage; the capability is C1, `tools/mado-options.py --live`). Host measured: Hyprland 0.56.2 at `efb50993780079460b0cbed1363e2166a2de1d9f`, hyprlang 0.6.8, `.conf` era. Read-only throughout: the only compositor verbs run were `hyprctl getoption -j`, `version` and `descriptions -j`.

ground: what one option key's own answer from the running compositor looks like (reply shape, the forms, the failure shapes), how a *declared* string is converted before it can equal that answer, and the one rule that makes a declared value and a live value differ without anything being wrong (angle inheritance). Held, not restated: include order and last-declarer ownership (`config-option-table-r39.md` §1-§4), the parser boundary that decides which lines are options (§2 there), the label vocabulary and the 56 claim-to-live pairs (`hyprctl-verification-layer.md` §2-§4). This entry supersedes `config-option-table-r39.md` §4's catch-all comparison with per-form conversions, closes unknown 2 of `hyprctl-verification-layer.md` (why `45deg` survives a single-colour assignment), and extends the held `set` correlation (§3 there) by one reading rule.

## §1 The reply

**OBS** S158 (`src/debug/HyprCtl.cpp`, dispatchGetOption, `:1701-1728`): with `-j` the handler formats one object per key, the field name after `option` being the type's form; the vec2 line reads `R"({{"option": "{}", "vec2": [{},{}], "set": {} }})"` (note the space before the closing brace; floats use `{:2f}`, six decimals). The quoted line: `R"({{"option": "{}", "vec2": [{},{}], "set": {} }})"`.

**OBS** S279 (measured 2026-10-25): over all 353 options of `hyprctl descriptions -j` the host answers five forms, and over the 70 keys its config tree declares four of them. The two count lines are standalone below (§6); a reply holds exactly one form, the field `option` equals the key asked, and `set` is a JSON boolean. The census receipt carries the raw shapes: `census: 70 declared keys queried once each with hyprctl getoption -j`.

**OBS** S279 (measured): an unknown key is not an error - the text `no such option` on stdout, exit 0 - and a missing compositor instance is an error that speaks on **stdout** (`HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)`, exit 1) with stderr empty. A reader that requires JSON must branch on the first, and read stdout before trusting the exit status on the second.

**OBS** S279 (measured, from the 353-line capture): `set` is true for exactly the 70 options some file of the tree declares and false for the other 283 - the set of true keys equals the declared set - so `set` separates "a file says so" from "the engine's default". The held correlation (`hyprctl-verification-layer.md` §3: `set=false` on the four then-undeclared options) was a 56-key sample; this is the whole option set. The receipt line: `set=true options: 70 of 353; equal to the declared set: yes; set=false: 283`.

**OBS** S215 (`src/config/values/ConfigValues.cpp`): every one of the 353 options is registered through `MS<Type>(...)`; counted by this lane, `Bool` 174, `Int` 84 and `Color` 6 answer as `int` (264), `Float` 34 as `float`, `String` 28 as `str`, `Gradient` 16 + `CssGap` 3 + `FontWeight` 2 as `custom` (21), and `Vec2` 6 as `vec2`. The fifth form's registry line, for the key `decoration:shadow:offset`: `"shadow's rendering offset.", Config::VEC2{},`.

**INF** The form follows the option's registered type, not the spelling in the config: `input:sensitivity` is declared `0` and answers `float`; a boolean option declared `yes, please :)` answers `int 1`. The handler also has a `"bool"` branch (`:1704`) that this host never reaches (0 of 353): the legacy config manager registers booleans as integers. A tool that treats an unknown form as an error, as `--live` does, is right to; it must not assume the four forms are the universe (the frozen round-40 v1 predicates did, and the wave caught it).

## §2 How a declared string is converted (per form)

| form | reply field | declared -> answered | rule at |
|---|---|---|---|
| `int` | `"int": N` | `0x` hex; `rgba(rrggbbaa)`; `rgba(r,g,b,a)`; `rgb(rrggbb)`; `rgb(r,g,b)`; prefixes `true`/`on`/`yes` -> 1 and `false`/`off`/`no` -> 0 (`nothing` -> 0); signed decimal | S173 `:185-264` |
| `float` | `"float": 0.600000` | decimal text, compared numerically (the host prints six decimals) | S173 |
| `str` | `"str": "dwindle"` | the trimmed declared text, exactly | S173 |
| `vec2` | `"vec2": [x,y]` | exactly `x y`, one space, `stof` each; `1  2` and `1 2 3` are refused | S173 `:474-486` |
| `custom` gradient | `"<hex> ... <N>deg"` | each colour token through `ParserUtils::parseColor`, printed lowercase unpadded ARGB, then `<N>deg`; `N` is `stoi` of the first `deg` token (`45.5deg` reads 45); no `deg` token keeps the previous angle (§4) | S181, S162 |
| `custom` CSS gap | `"t r b l"` | 1 value -> all four; 2 -> vertical horizontal; 3 -> top horizontal bottom; 4 -> as written | S180 |
| `custom` font weight | `"N"` | a name from a fixed table (`thin` 100 ... `ultraheavy` 1000, case-insensitive) | S180 |

**OBS** S180 (`src/config/shared/complex/ComplexDataTypes.hpp`): the gap type prints its four sides as integers in top/right/bottom/left order, which is why a one-value declaration answers with four: `return std::format("{} {} {} {}", m_top, m_right, m_bottom, m_left);`.

**UNK** The numeric font-weight branch is not exercised on this host (only names are declared). Read in code (S180 `:163-175`), an in-range number absent from the name table is parsed and discarded, so the value keeps whatever it held, and an out-of-range number forces 400; neither outcome is a host fact here, so a numeric weight is never labelled `agreement` by the tool.

## §3 Two colour parsers, two roundings

**OBS** S173 (hyprlang, `configStringToInt`, used by every `Int`/`Color` option): the alpha byte of `rgba(r,g,b,a)` is rounded: `a = std::round(std::stof(trim(rolling.substr(0, rolling.find(',')))) * 255.f);`. With alpha 0.5 that is 128 (`0x80`), with 0.3 it is 77.

**OBS** S181 (Hyprland, `ParserUtils::parseColor`, used by every gradient colour token): the alpha byte is floored and the channels must be 0-255: `std::floor(*a * 255.F)`. With alpha 0.5 that is 127 (`0x7f`), with 0.3 it is 76. The same spelling therefore prints two different bytes depending on whether the option is an int colour or a gradient.

**INF** (source reading, not run against the library): a comparison that parses every colour with one function is right for one family and off by one in the other. The tool keeps two models (`hl_int`, `grad_color`); `parseColor` also accepts `#rgb`, `#rrggbb` and `#rrggbbaa`, which a config *file* cannot carry (`#` starts a comment in hyprlang), so they are modelled and not generated.

## §4 Angle inheritance: why a declared value and a live value differ and both are right

**OBS** S162 (`src/config/legacy/ConfigManager.cpp`, `configHandleGradientSet`, `:103-160`): the handler clears the colour list on every declaration but assigns the angle only when a token holds `deg`: `DATA->m_angle = std::stoi(std::string(var.substr(0, var.find("deg")))) * (std::numbers::pi / 180.0); // radians`.

**OBS** S279 (measured): `general:col.active_border` is declared twice on this host - the defaults tree with `rgba(33ccffee) rgba(00ff99ee) 45deg`, then the theme with the one-colour `rgb(e68e0d)` - and answers `ffe68e0d 45deg`: the angle the theme's line does not contain. `group:col.border_active` is the same. With the rule switched off in a copy of the tool the census reads `agreement*=6 mismatch=2`, flipping exactly those two keys; with it on, `mismatch=0`.

**INF** The angle is state of the option's data object, allocated once and reused across declarations, so a later declaration without `deg` inherits the earlier one's angle; the colour list is not inherited. This closes the carried unknown that `hyprctl-verification-layer.md` left open ("why `45deg` survives a single-colour assignment"). The mechanism was confirmed against the installed hyprlang library by a wave seat (`.ufo/waves/round-40/w1/RevAngleClaim.md`), cited, not re-run here.

## §5 vec2

**OBS** S215 (the type table): six options register as `Vec2`; none is declared on this host, so the census's declared-key forms line has no `vec2`, and the all-options line has six. The compositor answers them as arrays, e.g. `decoration:shadow:offset` -> `[0,0]` with `set` false (the receipt lists the probes).

**INF** A tool that exits with a failure on a form it has not seen reports a healthy compositor as broken the moment a config declares one of the six; `tools/mado-options.py --live` therefore handles `vec2` (declared `x y`, both components within 1e-6) and exits 5 only on a form outside the five.

## §6 The host census

The three lines below are standalone on purpose: the counter reads them from this entry and from the receipt and compares them with the committed captures.

forms int=44 float=5 str=8 custom=13
labels agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0
allforms int=264 float=34 str=28 custom=21 vec2=6

**OBS** S279 (own work, 2026-10-25): the 70 keys of the static table were queried once each; 62 agree with their last declarer after conversion and 8 agree while an earlier declarer is shadowed (`decoration:rounding`, `general:border_size`, `general:col.active_border`, `general:gaps_in`, `general:gaps_out`, `group:col.border_active`, `input:kb_layout`, `input:kb_options`); none disagrees.

**INF** `mismatch=0` under this model means every declared key's live value is explained by its declaration plus the rules above. It does not say the config is what the operator meant, nor that no `hyprctl keyword` override ever ran.

**OBS** S278 (the 0.54.0 wiki page, the last archive on the `.conf` era documented by the lane): the page documents the verb and no reply shape: `getoption [option] - gets the config option status (values)`. The strings `"set"`, `"option"`, `custom type` and `no such option` occur nowhere in its text (a wave seat searched the three pages), so the native forms, the `set` field and the exit status of an unknown key are known here only from the compositor's source (S158) and from measurement (S279), never from documentation.

**UNK** The 0.56.0 wiki spells option names with dots (`general.gaps_in`); on this host that spelling answers `no such option` while the colon spelling works. Which is right for which release was not settled this round.

## §7 What this does NOT license

- Runtime `hyprctl keyword` overrides are outside: nothing here says how an override interacts with a reload or how to attribute a live value no declaration explains.
- Nothing is claimed about options the host never declares: a probe answers the engine's default with `set` false and no owner.
- Plugin-registered options are outside the parser boundary (§2 of the held option table) and outside the census.
- The census is one host, one date, one theme and toggle state: re-run it, never reuse the counts (the receipt is `.ufo/waves/round-40/fetch/census-receipt.txt`; the command is `python3 -I tools/mado-options.py --home "$HOME" --live`).
- A numeric font weight, a Lua-era config and the `bool` form are unmeasured here (§1, §2).
