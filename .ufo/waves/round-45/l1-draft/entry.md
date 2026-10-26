# From `monitor =` line to running output: how Hyprland 0.56.2 parses, picks and applies a monitor rule, and what `hyprctl monitors all -j` shows of it

source: S302 - hyprwm/Hyprland src/config/shared/monitor/Parser.cpp @ efb5099 (v0.56.2) - mode, position, scale and transform field parsing
source: S303 - hyprwm/Hyprland src/config/legacy/ConfigManager.cpp @ efb5099 - the `monitor` keyword handler: line grammar, modifiers, key loop
source: S304 - hyprwm/Hyprland src/config/shared/monitor/MonitorRuleManager.cpp @ efb5099 - one rule per selector, last match wins, the empty-selector fallback
source: S305 - hyprwm/Hyprland src/config/shared/monitor/MonitorRule.hpp @ efb5099 - the rule's field defaults
source: S306 - hyprwm/Hyprland src/output/Monitor.cpp @ efb5099 - mode choice, scale correction, selector matching
source: S307 - hyprwm/Hyprland src/debug/HyprCtl.cpp @ efb5099 - the `monitors` request and its JSON fields
source: S308 - hyprwm/Hyprland src/state/MonitorPositionController.cpp @ efb5099 - explicit positions placed as written
source: S309 - hyprwm/hyprutils src/string/String.cpp @ v0.14.2 (the host's hyprutils 0.14.2-1) - the number test the scale and transform parsers use
source: S310 - hyprwm/hyprland-wiki content/Configuring/Monitors.md @ ecc06f3 (2026-04-20) - the documented line format and options
verified-at: 2026-10-26
recheck: 90d - re-pull the nine pinned files and re-run the counter; a Hyprland or hyprutils package update on the host is the earlier trigger
ground: U5 output management, runtime state agreement (corpus/knowledge/output-colour-boundaries-r14.md left "runtime state agreement" UNK); the read-only join that measures it is tools/mado-monitors.py
Lane: mado-shokunin. Round: 45.

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| Which rule does an output get? | the rule list: one rule per selector string, searched newest first; else the first empty-selector rule; else a built-in default | OBS (source) |
| What does `WxH` without `@RATE` request? | the rule keeps its 60 Hz default, so the mode closest to 60 Hz at that size is chosen | OBS (source) + INF (mode choice not exercised) |
| When does a requested mode count as met? | Hyprland's own closeness test: within 1 px and 1 Hz of the request | OBS (source) |
| Is the written scale the running scale? | only when it divides the pixel size; otherwise the nearest multiple of 1/120 that does (89 steps up and down) | OBS (source) |
| Where do positions come from? | explicit offsets are placed as written; `auto*` positions are computed after them | OBS (source) |
| Which extra keys does the line form accept? | eight keys; any other key rejects the whole line | OBS (source) |
| Does the documented `sdr_eotf` key work on a `monitor =` line? | the wiki documents it; the host's handler reads it only in `monitorv2` blocks | OBS (source, docs) + INF (rejection not exercised) |
| Does the host's output run what its config declares? | one output, one rule, AGREE on every compared field | OBS (host, 2026-10-26) |

## §1 Parsing the line

**OBS** S303 - the handler splits the line on commas, takes field 0 as the selector and parses the next three fields positionally: `parser.parseMode(std::string(ARGS[1])); parser.parsePosition(std::string(ARGS[2])); parser.parseScale(std::string(ARGS[3]));` (Hyprland-legacy-ConfigManager.cpp:1345).

**OBS** The handleMonitor function (Hyprland-legacy-ConfigManager.cpp:1293-1299) first checks field 1 for `disable`/`disabled` (a disabled rule), `transform` (copy the first rule with the same selector, set its transform, add the copy) and `addreserved` (change the same-selector rule's reserved area, or fall through and add a default rule for the selector) (Hyprland-legacy-ConfigManager.cpp:1299-1343).

**OBS** After the scale field the monitor line takes KEY, VALUE pairs until an empty field: mirror, bitdepth, cm, sdrsaturation, sdrbrightness, transform, vrr, icc; any other key logs and returns "invalid syntax" before the rule is added, so the whole line is dropped (Hyprland-legacy-ConfigManager.cpp:1351-1379). A parse error inside a known field does not stop the add: the rule is added and the error returned (Hyprland-legacy-ConfigManager.cpp:1384-1386).

**OBS** In parseMode (Hyprland-Parser.cpp:110-139) the mode field is `preferred` when empty or starting `pref`; `highrr`, `highres` and `maxwidth` are keywords; a `modeline` keyword parses a custom DRM mode; otherwise the field must hold an `x`, the width and height come from `stoi` and the rate from the text after `@`.

**OBS** S302 - the rate is read only when an `@` is present: `m_rule.m_refreshRate = stof(value.substr(value.find_first_of('@') + 1));` (Hyprland-Parser.cpp:134).

**OBS** S305 - without `@` the rule keeps its default rate: `float m_refreshRate = 60;` (Hyprland-MonitorRule.hpp:46). A rule `monitor = DP-1, 3440x1440, 0x0, 1` therefore asks for 60 Hz, not for the output's fastest mode.

**OBS** parsePosition (Hyprland-Parser.cpp:145-173): an empty field or one starting `auto` leaves the offset unset and records an auto direction (`auto`, `auto-left`, `auto-right`, `auto-up`, `auto-down`, `auto-center-*`); otherwise the field must hold an `x` and both halves go through `stoi`.

**OBS** parseScale (Hyprland-Parser.cpp:193-211): an empty field or one starting `auto` means auto scale; otherwise the field must pass the float number test and a value below 0.25 is replaced by 1 with an error.

**OBS** S309 - the number test lets a minus sign stand only first: `if (i == 0 && str.at(i) == '-') {` (hyprutils-String.cpp:59). The isNumber2 function (hyprutils-String.cpp:50-79) also allows one `.` (not first), and its last line requires the final character to be a digit (hyprutils-String.cpp:83), so a scale written `1.` fails the test and the rule keeps auto scale.

## §2 Which rule an output gets

**OBS** S304 - adding a rule first erases every rule with the same selector string: `std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });` (Hyprland-MonitorRuleManager.cpp:38). The add function (Hyprland-MonitorRuleManager.cpp:37-42) then appends, so a re-added selector moves to the end of the list.

**OBS** The lookup walks the list in reverse and returns the first match, so the newest matching rule wins; with none it returns the first rule whose selector is empty, then a built-in default (preferred, auto, auto) (Hyprland-MonitorRuleManager.cpp:96-106). An output-management client's committed state overrides the chosen rule's fields before it is applied (Hyprland-MonitorRuleManager.cpp:45-84), so a running state that differs from the config can be a client's doing.

**OBS** The selector matches by exact output name, or with `desc:` when the long or the short description starts with the trimmed text (Hyprland-Monitor.cpp:1201-1211). The short description is make, model and serial with commas removed (Hyprland-Monitor.cpp:255-256), and that short form is what `hyprctl monitors -j` prints as `description` (Hyprland-HyprCtl.cpp:277).

## §3 Applying the rule

**OBS** For a requested `WxH@R` the available modes are sorted by closeness in width, then height, then rate, and when the best one is not within 1 px and 1 Hz of the request the requested mode is tried first as a custom mode (Hyprland-Monitor.cpp:819-840); `highrr`, `highres` and `maxwidth` sort by rate or size instead (Hyprland-Monitor.cpp:784-817).

**OBS** S306 - when the written scale would leave a fractional logical size the search starts from the nearest 1/120 step: `float searchScale = std::round(m_scale * 120.0);` (Hyprland-Monitor.cpp:1001). The correction (Hyprland-Monitor.cpp:997-1027) keeps that step when it divides the pixel size, else tries one step up then one down for up to 89 steps; for a written scale with no clean divisor Hyprland falls back to its default scale and shows an error (Hyprland-Monitor.cpp:1029-1036), and with one it shows a notification and uses the corrected value (Hyprland-Monitor.cpp:1038-1049).

**OBS** S308 - an explicit position is applied as written before any auto placement: `m->moveTo(*POS); arranged.push_back(m); it = toArrange.erase(it);` (Hyprland-MonitorPositionController.cpp:27).

## §4 What `hyprctl monitors all -j` shows

**OBS** S307 - the JSON prints the running rate with five decimals: `"physicalHeight": {}, "refreshRate": {:.5f},` (Hyprland-HyprCtl.cpp:241-242). Its width and height are the pixel size, `scale` the applied scale, `disabled` the negation of enabled, and `mirrorOf` the id of the mirrored output or `none` (Hyprland-HyprCtl.cpp:276-288).

**OBS** The request takes one optional argument; only the word `all` lists every output including disabled ones, otherwise only the active list is printed (Hyprland-HyprCtl.cpp:313-321).

hyprland monitor-rule default_refresh=60 refresh_tolerance=1 scale_step=1/120 scale_search=89 json_refresh_decimals=5 line_keys=8

## §5 The documentation

**OBS** S310 - the wiki gives the line as `monitor = name, resolution, position, scale` (wiki-Monitors.md:11).

**INF** The wiki documents (wiki-Monitors.md:7-12) the same positional order the handler parses. It also documents a `, sdr_eotf, X` key on the monitor line (wiki-Monitors.md:253), but the host's handler key loop has no `sdr_eotf` (Hyprland-legacy-ConfigManager.cpp:1351-1379), so a `monitor =` line carrying it is rejected whole; only a `monitorv2` block reads `sdr_eotf` (Hyprland-legacy-ConfigManager.cpp:819-831). Not exercised on the host.

## §6 On this host (2026-10-26, read-only)

**OBS** `~/.config/hypr/monitors.conf` declares one rule, DP-1 at 3440x1440@100, position 0x0, scale 1; `hyprctl monitors all -j` reports DP-1 at 3440x1440, 99.99700 Hz, 0x0, scale 1, transform 0, not disabled, mirroring none; the round's tool reports AGREE and verdict OK, exit 0 (.ufo/waves/round-45/receipts/live-monitors-host-l1.txt). The 0.003 Hz gap is inside the 1 Hz closeness bound.

**UNK** Whether the output would have run 59.99 Hz under a rule without `@100`, and whether a fractional scale would be corrected as computed, are not exercised: both would need a config change, which is the operator's.

## Limits

- Code-read facts at efb5099 and hyprutils v0.14.2; nothing here was run against a changed config.
- `monitorv2` blocks are added after every `monitor =` line and replace same-selector rules; this entry does not trace their field parsing beyond `sdr_eotf`.
- The JSON carries only the short description, so a `desc:` selector that matches only the long description cannot be checked from the dump.
