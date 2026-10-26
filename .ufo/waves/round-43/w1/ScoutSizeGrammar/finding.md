# ScoutSizeGrammar - what `size`, `float` and `match:class` accept, and what the C1 contract reads of the host

Scope: read-only scout. Nothing implemented, no counter/tool touched. Pins (sha256 in `pins/SHA256SUMS`) are v0.56.2
(commit efb5099...) files fetched from raw.githubusercontent.com 2026-10-26, plus hyprutils v0.14.2 (host `pacman -Q hyprutils` = 0.14.2-1).
Paths below `pins/` unless prefixed `fetch/` (= round-43/fetch/). `[INFERENCE]` = not exercised or not pinned.

## 1. The `windowrule = ...` line to rule object (what Hyprland does before the contract's regexes even apply)
- `windowrule = <v>` is a registered keyword handler (pins/Hyprland-src_config_legacy_ConfigManager.cpp:419-429, 610) -> `handleWindowrule` (:2016). `windowrulev2` is rejected outright (:431-434).
- Fields are split on `,` by `CVarList2` with default `delim=','` and `allowEscape=true` (pins/Hyprutils-VarList2.hpp:18; split logic Hyprutils-VarList2.cpp:20-95), each field trimmed. `\,` is an escaped comma (VarList2.cpp:34-52) - the contract's plain `split(",")` differs, only for lines it already refuses (a comma is outside its regex alphabet).
- Each field is `<name> <value>` split at the FIRST space (ConfigManager.cpp:2024-2028; a field without a space is an error). A field starting `match:` is a match prop, otherwise it must be an effect name (:2030-2046). **The order of fields is free**: effect first or match first both parse; any number of match fields and effect fields per line.
- Block form also exists: `windowrule { name = ...  match:class = RX  size = W H }` (addRuleFromConfigKey, ConfigManager.cpp:894-915).
- Match props (pins/Hyprland-Rule.cpp:27-44): class, title, initial_class, initial_title, float, tag, xwayland, fullscreen, pin, focus, group, modal, fullscreen_state_internal, fullscreen_state_client, workspace, content, xdg_tag, namespace. All present props must match (WindowRule.cpp `matches`, AND loop).
- Class/title match = RE2 `FullMatch` (anchored whole string), prefix `negative:` inverts it (fetch/Hyprland-RegexMatchEngine.cpp:7-16). Tag match is NOT a regex: `CTagKeeper::isTagged(tag, strict=false)` (pins/Hyprland-TagKeeper.hpp:8): a leading `negative` prefix inverts, and a window matches tag T when its tag set holds `T` or `T*` (pins/Hyprland-TagKeeper.cpp:3-8). The `hyprctl clients -j` `tags` list shows the dynamic form, e.g. `terminal*` (live dump 2026-10-26: Alacritty `['default-opacity*', 'terminal*']`; fetch/Hyprland-HyprCtl.cpp:415 emits `"tags"`).

## 2. `size`
- Parsed by `parseWindowRuleEffect`: `size`, `move`, `max_size`, `min_size` share one branch, `Math::parseExpressionVec2(raw)` (pins/Hyprland-WindowRule.cpp:268-274).
- `parseExpressionVec2` (pins/Hyprland-Expression.cpp:31-48): trim; empty -> an empty vec (rule clears size, WindowRuleApplicator.cpp:420-427); else split at the FIRST whitespace (`find_first_of(" \t\n\r\f\v")`, :36) into lhs/rhs; no whitespace -> error "expression vec2 requires two expressions separated by whitespace" (:38). Each half is a **muparser expression string**, evaluated later - so the 2-token shape the contract demands is real, but anything after the first whitespace is ONE expression including further whitespace: `size 1 2 3` parses, then fails at evaluation (probe: `3 4` -> `Unexpected value "4"`), and `size (monitor_w - 40) 100` is split at the space inside the parens and fails (`(monitor_w` -> `Missing parenthesis`).
- Evaluated per half by `CWindow::calculateSingleExpr` (pins/Hyprland-Window.cpp:1999-2016) with a fresh `mu::Parser` and exactly these constants: `window_w window_h window_x window_y monitor_w monitor_h cursor_x cursor_y` (:2005-2014). `window_*` = the window's `m_realSize/m_realPosition` goal at map time; the floating algorithm first does `sizeAnimation()->setValueAndWarp(DESIRED_GEOM ? ... : DEFAULT_SIZE)` "so that expressions can use it" (fetch/Hyprland-DefaultFloatingAlgorithm.cpp:52-53); `monitor_*` = the window's monitor, else the focused one, else literal 1920x1080 (:2001, :2010-2011); `cursor_*` = live pointer position. Result is `double`, written to `windowGeometry.w/h` (DefaultFloatingAlgorithm.cpp:56-61), no integer rounding in the source.
- Real muparser 2.3.5 (host `pacman -Q muparser` = 2.3.5-2) probed with the same constants (pins/mu-probe.cpp, input pins/mu-probe-input.txt, output pins/mu-probe-output.txt; the leading `OK [..] = ERR` tokens in the raw table are a cosmetic echo - the mu-probe-output.txt copy rewrites them to `ERR`):
  - accepted: `420`, `420.7`, `1e3`, `-5`, `+5`, `0.5*monitor_w`, `monitor_w*0.5`, `(monitor_w-40)`, `monitor_w - 40`, `window_w`, `1920/2`, `monitor_w*50/100`, `min(monitor_w,800)`, `abs(window_w)`, `rint(monitor_w*0.333)`, `monitor_w>1000?800:400`, and `1,5` (comma operator = 5).
  - refused: `50%` ("Unexpected token "%""), `monitor_w%2`, `100px`, `0x1A`, `floor(...)`, unknown names (`foo`), empty, unbalanced parens, `1e9999`.
  - So **no percentage syntax** exists; "half the monitor" is `monitor_w*0.5` (an expression), and `size` cannot mean a % of anything except through the 8 constants.
- Host usage today (grep of every `*.conf` under ~/.config/hypr and ~/.local/share/omarchy/default/hypr, pins/../host-classify.txt): all 7 `size` lines are two plain decimal integers (`420 500`, `875 600`, `1100 700`, `600 338`, `460 800`). Expressions appear only in `move` (`(monitor_w-window_w-40) (monitor_h*0.04)`, pip.conf:10, webcam-overlay.conf:6), never in `size`. The host has no `max_size`/`min_size` rule line.
- Deterministic-from-text subset: only expressions with NO constant from the 8 are a pure function of the rule text (`420`, `420.7`, `1e3`, `1920/2`, `min(1,2)`); every expression naming a `monitor_*`/`window_*`/`cursor_*` is state-dependent (monitor, pointer, size-at-map) and cannot be decided from one `hyprctl clients -j` dump.
- The size rule is consumed only at the first map of a FLOATING window (`target->window()->m_firstMap`, DefaultFloatingAlgorithm.cpp:49 and the `static_.size` branch :55-62); tiled windows ignore it (TILED verdict in the contract).

## 3. `float`
- Branch `WINDOW_RULE_EFFECT_FLOAT` ... `return truthy(raw)` (pins/Hyprland-WindowRule.cpp:224-257, boolean group).
- `truthy(str)` (pins/Hyprland-MiscFunctions.cpp:829-843): true iff `str == "1"`, or, case-insensitively, `str` STARTS WITH `true`, `yes` or `on`. Everything else is false - `off`, `0`, `false`, `no`, the empty string, and garbage like `banana`, with no error. Consequences: `float ON`, `float True`, `float yes`, `float 1`, `float onwards` are all ON; `float off|0|false|no|xyz` are OFF. The contract's `on|off` (lower case, exact) is a strict subset on the ON side and on the OFF side only names the explicit spelling.
- A `float` field with no value is a parse error ("missing a value", ConfigManager.cpp:2028) - the rule is not registered.
- Host usage: all 9 float lines are `float on` (0 other spellings).

## 4. `match:class` regex forms the host really uses (class-regexes.txt, 54 `match:class` occurrences over `windowrule =` lines and block rules)
- In the contract alphabet `[A-Za-z0-9_.^$()|*+?-]` (+ escapes): `^(org.omarchy.gkeep)$`, `^(org.omarchy.ai-usage)$`, `(Share|localsend)`, `localsend`, `steam`, `steam.*`, `org.gnome.Calculator`, `org.omarchy.screensaver`, `^Typora$`, `^$`, `.*`, `^(jetbrains-.*)$`, long `(a|b|c|...)` lists (system.conf:6-7, 16-17: up to 15 alternatives), `(Alacritty|kitty|foot)`, `chrome-...-Default`, `qemu`, `com.libretro.RetroArch`.
- Outside it (4 distinct regexes, all `[...]` character classes or `(...)?`): `^(1[p|P]assword)$` (1password.conf:1-2), `([fF]irefox|zen|librewolf)` and `((google-)?[cC]hrom(e|ium)|[bB]rave-browser|[mM]icrosoft-edge|Vivaldi-stable|helium)` (browser.conf:2-3), `.*[Rr]esolve.*` (davinci-resolve.conf:2). **None of the 4 sits on a `size`/`float` line**, so widening the alphabet to `[ ]` buys zero host rules today.
- No `negative:` prefix, no `(?`, no `\d`/`\w` anywhere on the host.

## 5. Host `size`/`float` lines against the C1 contract (script: scout's re-implementation of the docstring contract, output pins/../host-classify.txt; 78 `windowrule =` lines, 62 are `other`, 16 are size/float)
| line | verdict | reason |
|---|---|---|
| gkeep.conf:2 float on, class ^(org.omarchy.gkeep)$ | READ | |
| gkeep.conf:4 size 420 500, same class | READ | |
| ai-usage.conf:3,5 float on / size 875 600 | READ | |
| localsend.conf:2 float on (Share\|localsend); :4 size 1100 700 localsend | READ | |
| steam.conf:2 float on, class steam | READ | |
| system.conf:8 float on, class org.gnome.Calculator; :12 float on, org.omarchy.screensaver | READ | |
| pip.conf:4 float on / :6 size 600 338, `match:tag pip` | REFUSED (unsupported) | field 1 is `match:tag` |
| system.conf:2 float on / :4 size 875 600, `match:tag floating-window` | REFUSED | `match:tag`; the tag is granted by system.conf:6-7 `tag +floating-window` class rules (type `other`) |
| steam.conf:6 size 1100 700 / :7 size 460 800, `match:class steam, match:title ...` | REFUSED | 3 fields (extra `match:title`) |
| webcam-overlay.conf:2 float on, `match:title WebcamOverlay` | REFUSED | `match:title` only |
| **typora.conf:2** `match:class ^Typora$, match:title ^Print$, float on, center on` | **MIS-CLASSIFIED as `other`**, silently | field 0 is `match:class`, so effect token = `match:class` (contract: "first token of field 0"); Hyprland accepts any field order. Counted in `other=`, never in `unsupported=`. It also carries `match:title`, so refusing is right, but the label is wrong. |
| input.conf:45-46 `match:class RX, scroll_touchpad N` | `other` (correct - not size/float) | shows the reversed order IS how this host writes rules |
| geforce/jetbrains/moonlight block rules | not seen at all | `windowrule {` does not fully match `windowrule[ \t]*=(.*)` (contract: ignored and counted nowhere); none holds size/float |
Tally: size 3 read / 4 refused (of 7); float 6 read / 3 refused (of 9). Refused by cause: `match:tag` 4 lines (pip x2, system x2), extra `match:title` 2 (steam size), title-only 1 (webcam float). `[INFERENCE]` The contract refuses everything it cannot evaluate by sending it to `unsupported`, EXCEPT the reversed-field-order shape, which falls into `other`.
Host loading: `windows.conf:12 source = .../apps.conf`, `hyprland.conf:29,32` sources ai-usage.conf and gkeep.conf; the toggles/theme files hold no windowrule (grep, 0 hits). A `--rules` list is the caller's choice; passing a non-sourced file would join rules the compositor never loaded.

## 6. Proposal (NOT implemented): smallest extension that reads the most host size/float lines safely
Ranked by host lines gained per unit of added trust surface:
1. **E1 `match:tag NAME` as field 1 (+4 lines: pip x2, system x2; the system pair is the 875x600 default every `tag +floating-window` class inherits, gkeep.conf:1 comment says so).** Semantics, from the pins: window matches when its dump `tags` list contains `NAME` or `NAME*` (TagKeeper.cpp:3-8); a `negative` prefix inverts; NAME has no regex. Contract: field 1 fully matches `match:tag[ \t]+([A-Za-z0-9_.-]{1,64})`; client element's `tags` = list of strings else none (a client without a usable `tags` list cannot match a tag rule: treat as not matching). Input is the same single dump (`tags` is already in `hyprctl clients -j`, HyprCtl.cpp:415). Safe because the dump reports the tag set the compositor actually holds, so the tool never has to evaluate `tag +x` class rules itself. Caveat: tags can be set/removed at runtime by dispatchers, so "rule would apply at map" and "tag present now" can differ - AGREE/DIFFER is a statement about the current state, and that is the same caveat the contract already has for class and for resized floating windows.
2. **E2 field-order freedom + conjunction of several match fields (+0 new lines on its own, makes typora honest; with `match:title RX` against the dump `title`, +2 steam size lines and +1 webcam float).** Any number of fields; at most one effect field (size/float), others must be `match:class|title|tag` with an accepted pattern; every other effect or match prop => `unsupported` (`other` stays only for lines with no size/float effect field at all). Cost: `title` is dynamic (a tab title changes after map), so a title-matched rule's DIFFER can be produced by the title changing, not the size. I rank this second and would mark verdicts from title-matched rules with a distinct word (or exclude them) - [INFERENCE] needs a fixture decision.
3. **E3 `float` spelling set (0 host lines).** If added at all, exactly the closed set `on|1|true|yes` -> on, `off|0|false|no` -> off, case-insensitive, whole token, NOT Hyprland's prefix rule (`onwards` would be a lie). Host has only `on`; skip unless a rule file elsewhere uses others.
4. **E4 size values (0 host lines).** `[0-9]{1,5}` digits are right for the host: Hyprland also accepts decimals (`420.7`) and constant-only expressions, but the host has neither. How a double goal appears in the dump's integer `size` is NOT established here ([INFERENCE]), so do not extend to decimals without a pinned conversion. Any expression naming `monitor_*|window_*|cursor_*` stays unsupported (state-dependent, section 2).
5. **E5 bracket classes `[A-Za-z]` in the regex alphabet (0 host size/float lines).** 0 gain today; [INFERENCE] simple bracket classes behave the same in Python `re` and RE2, not tested here. Leave out.
Not recommended: percentages (no such syntax), block-form `windowrule {}` (3 host blocks, none with size/float; adds a second parser), `negative:` prefix.
Smallest meaningful change: **E1 alone**. It reads 4 more host lines: size 3->5 of 7, float 6->8 of 9, so 9 -> 13 of 16 size/float lines. E1 plus E2 (title conjunction, field order) reaches 16 of 16, at the title-staleness cost named in item 2. E1 adds one regex, one dump field (`tags`) and one verdict input; the rest of the frozen contract stays. The frozen C1 counter scores the CURRENT contract (round-42 freeze), so E1 is a round-44+ candidate, not a round-43 change.

## 7. Quotes (<= 25 words, located; verified by the script in section 8)
- WindowRule.cpp:270 `auto parsed = Math::parseExpressionVec2(raw);`
- Expression.cpp:36 `const auto spacePos = raw.find_first_of(" \t\n\r\f\v");`
- Expression.cpp:38 `expression vec2 requires two expressions separated by whitespace`
- MiscFunctions.cpp:842 `}("true"sv, "yes"sv, "on"sv);`
- Window.cpp:2010 `expr.addVariable("monitor_w", PMONITOR ? PMONITOR->m_size.x : 1920);`
- DefaultFloatingAlgorithm.cpp:52 `set this here so that expressions can use it. This could be wrong of course.`
- RegexMatchEngine.cpp:16 `return re2::RE2::FullMatch(other, *m_regex) != m_negative;`
- TagKeeper.cpp:6 `const bool TAGGED   = m_tags.contains(MATCH) || (!strict && m_tags.contains(MATCH + "*"));`
- ConfigManager.cpp:2028 `invalid field {}: missing a value`

## 8. Verification
`python3 verify-quotes.py` (in this dir) greps each quote in its pin and prints PASS/FAIL.
