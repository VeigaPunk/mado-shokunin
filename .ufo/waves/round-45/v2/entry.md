# From `monitor =` line to running output: how Hyprland 0.56.2 parses, picks and applies a monitor rule, and what `hyprctl monitors all -j` shows of it

source: S302 - hyprwm/Hyprland src/config/shared/monitor/Parser.cpp @ efb5099 (v0.56.2) - mode, position, scale and transform field parsing
source: S303 - hyprwm/Hyprland src/config/legacy/ConfigManager.cpp @ efb5099 - the `monitor` keyword handler: line grammar, modifiers, key loop
source: S304 - hyprwm/Hyprland src/config/shared/monitor/MonitorRuleManager.cpp @ efb5099 - one rule per selector, last match wins, fallbacks
source: S305 - hyprwm/Hyprland src/config/shared/monitor/MonitorRule.hpp @ efb5099 - the rule's field defaults
source: S306 - hyprwm/Hyprland src/output/Monitor.cpp @ efb5099 - mode choice, scale correction, selector matching, descriptions
source: S307 - hyprwm/Hyprland src/debug/HyprCtl.cpp @ efb5099 - the `monitors` request and its JSON fields
source: S308 - hyprwm/Hyprland src/state/MonitorPositionController.cpp @ efb5099 - explicit positions placed as written
source: S309 - hyprwm/hyprutils src/string/String.cpp @ v0.14.2 - the number test the scale and transform parsers use
source: S310 - hyprwm/hyprland-wiki content/Configuring/Monitors.md @ ecc06f3 (2026-04-20) - the documented line format and options
source: S311 - hyprwm/Hyprland src/state/MonitorState.cpp @ efb5099 - the real-output list and the active-output list
source: S312 - hyprwm/Hyprland src/macros.hpp @ efb5099 - the strict DELTALESSTHAN comparison
source: S313 - hyprwm/hyprutils include/hyprutils/math/Vector2D.hpp @ v0.14.2 - double-precision vector division
source: S314 - hyprwm/hyprutils include/hyprutils/string/VarList2.hpp @ v0.14.2 - the comma delimiter of the line splitter
source: S315 - hyprwm/aquamarine src/backend/drm/DRM.cpp @ v0.15.1 (the host's aquamarine 0.15.1-1) - how a DRM output's description is built
verified-at: 2026-10-26
recheck: on-release - when `hyprctl version` leaves efb50993 (or 90d at the latest) re-pull the fourteen pins and re-run the counter; upstream main already drops the legacy hyprlang manager (Hyprland a9902ea, 2026-07-22), so a release past 0.56.x removes the `monitor =` line form this entry and tools/mado-monitors.py describe
ground: U5 output management, runtime state agreement; the monitor-rule chain was absent at base (claim grep exit 1); held neighbours: point observations of DP-1's mode in config-health-report-r3.md and hyprctl-verification-layer.md
Lane: mado-shokunin. Round: 45.

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| Which rule does an output get? | the rule list: one rule per selector string, searched newest first; else the first empty-selector rule; else a built-in default; an output flagged as an unsafe fallback skips the list | OBS (source) |
| What does `WxH` without `@RATE` request? | the rule keeps its 60 Hz default, so the mode closest to 60 Hz at that size is chosen | OBS (source) + INF (mode choice not exercised) |
| When does a requested mode count as close? | strictly less than 1 px and 1 Hz from the request; otherwise the request is tried first as a custom mode | OBS (source) |
| Is the written scale the running scale? | only when it divides the pixel size; otherwise the nearest multiple of 1/120 that does (89 steps up and down), or the default scale when none does - unless `debug:disable_scale_checks` is set | OBS (source) |
| Where do positions come from? | explicit offsets are placed as written; `auto*` positions are computed after them | OBS (source) |
| Which extra keys does the line form accept? | eight keys; any other key rejects the whole line | OBS (source) |
| Does the documented `sdr_eotf` key work on a `monitor =` line? | the wiki documents it; the host's line handler has no such key, only `monitorv2` reads it | OBS (source, docs) + INF (rejection not exercised) |
| Which outputs does `hyprctl monitors -j` list? | without `all`, the active list (enabled, not mirrors); with `all`, every real output, disabled ones included | OBS (source) |
| Does the host's output run what its config declares? | one output, one rule, AGREE on every compared field | OBS (host, 2026-10-26) |

## §1 Parsing the line

**OBS** S314 - the line is split by the hyprutils CVarList2 splitter, whose default delimiter is a comma: `explicit CVarList2(std::string&& in, const size_t lastArgNo = 0, const char delim = ',',` (hyprutils-VarList2.hpp:18). The handleMonitor function builds it from the whole value and takes field 0 as the selector (Hyprland-legacy-ConfigManager.cpp:1293-1297).

**OBS** S303 - field 1 is first tested for the modifier forms: `if (ARGS[1] == "disable" || ARGS[1] == "disabled" || ARGS[1] == "addreserved" || ARGS[1] == "transform") {` (Hyprland-legacy-ConfigManager.cpp:1299). `disable`/`disabled` adds a disabled rule; `transform` copies the first rule with the same selector, sets its transform and adds the copy; `addreserved` changes the same-selector rule's reserved area, or falls through and adds a default rule for the selector (Hyprland-legacy-ConfigManager.cpp:1300-1343).

**OBS** Otherwise the three positional fields are parsed (Hyprland-legacy-ConfigManager.cpp:1345-1347), then KEY, VALUE pairs until an empty field: mirror, bitdepth, cm, sdrsaturation, sdrbrightness, transform, vrr, icc; any other key logs and returns "invalid syntax" before the rule is added, so the whole line is dropped (Hyprland-legacy-ConfigManager.cpp:1351-1379). A parse error inside a known field does not stop the add: the rule is added and the error returned (Hyprland-legacy-ConfigManager.cpp:1384-1386), so a bad mode degrades to preferred, a bad position or scale to auto.

**OBS** In parseMode (Hyprland-Parser.cpp:110-139) the mode field is `preferred` when empty or starting `pref`; `highrr`, `highres` and `maxwidth` are keywords; a `modeline` keyword parses a custom DRM mode (Hyprland-Parser.cpp:14-20 and Hyprland-Parser.cpp:119-121); otherwise the field must hold an `x`, the width and height come from `stoi` and the rate from the text after `@`. A resolution of 0x0 is the preferred sentinel the apply step tests (Hyprland-Monitor.cpp:773).

**OBS** S302 - the rate is read only when an `@` is present: `m_rule.m_refreshRate = stof(value.substr(value.find_first_of('@') + 1));` (Hyprland-Parser.cpp:134).

**OBS** S305 - without `@` the rule keeps its default rate: `float m_refreshRate = 60;` (Hyprland-MonitorRule.hpp:46; whitespace-normalized). A rule `monitor = DP-1, 3440x1440, 0x0, 1` therefore asks for 60 Hz, not for the output's fastest mode.

**OBS** parsePosition (Hyprland-Parser.cpp:145-174): an empty field or one starting `auto` leaves the offset unset and records an auto direction (`auto`, `auto-left`, `auto-right`, `auto-up`, `auto-down`, `auto-center-*`); otherwise the field must hold an `x` and both halves go through `stoi` (Hyprland-Parser.cpp:175-190).

**OBS** parseScale (Hyprland-Parser.cpp:193-211): an empty field or one starting `auto` means auto scale; otherwise the field must pass the float number test and a value below 0.25 is set to 1 with an error.

**OBS** S309 - the number test lets a minus sign stand only first: `if (i == 0 && str.at(i) == '-') {` (hyprutils-String.cpp:59). The isNumber2 function (hyprutils-String.cpp:50-79) also allows one `.` (not first), and its last line requires the final character to be a digit (hyprutils-String.cpp:83), so a scale written `1.` fails the test and the rule keeps auto scale, while a transform written `07` passes it and `stoi` reads 7 (Hyprland-Parser.cpp:213-226).

## §2 Which rule an output gets

**OBS** S304 - adding a rule first erases every rule with the same selector string: `std::erase_if(m_rules, [&x](const auto& e) { return e.m_name == x.m_name; });` (Hyprland-MonitorRuleManager.cpp:38). The add function (Hyprland-MonitorRuleManager.cpp:37-42) then appends, so a re-added selector moves to the end of the list.

**OBS** The lookup walks the list in reverse and returns the first match, so the newest matching rule wins; with none it returns the first rule whose selector is empty (Hyprland-MonitorRuleManager.cpp:96-106), then a built-in default of preferred mode, auto position and auto scale (Hyprland-MonitorRuleManager.cpp:108-116). An output flagged as an unsafe fallback never reaches the list and gets 1920x1080, auto, scale 1 (Hyprland-MonitorRuleManager.cpp:86-94). An output-management client's committed state overrides the chosen rule's fields before it is applied (Hyprland-MonitorRuleManager.cpp:45-84), so a running state that differs from the config can be a client's doing.

**OBS** The matchesStaticSelector function (Hyprland-Monitor.cpp:1201-1211) matches by exact output name, or with `desc:` when the long or the short description starts with the trimmed text. The long description is the backend's description with commas erased (Hyprland-Monitor.cpp:250-252); the short one is make, model and serial with commas erased (Hyprland-Monitor.cpp:255-256), which is what `hyprctl monitors -j` prints as `description` (Hyprland-HyprCtl.cpp:276-277), beside separate make, model and serial fields (Hyprland-HyprCtl.cpp:234-237).

**OBS** S315 - for a DRM output the backend's description is make, model, serial and the connector name: `output->description = std::format("{} {} {} ({})", make, model, serial, szName);` (aquamarine-DRM.cpp:2101). So the long description can be rebuilt from the dump as `make model serial (name)` with commas erased, for DRM outputs only.

## §3 Applying the rule

**OBS** For a requested `WxH@R` the available modes are sorted by closeness in width, then height, then rate, and when the best one is not close to the request the requested mode is pushed as a custom mode (Hyprland-Monitor.cpp:819-840); the list is then tried from the back, so that custom mode is tried first (Hyprland-Monitor.cpp:878-889); `highrr`, `highres` and `maxwidth` sort by rate or size instead (Hyprland-Monitor.cpp:784-817).

**OBS** S312 - "close" is strict: `#define DELTALESSTHAN(a, b, delta) (abs((a) - (b)) < (delta))` (Hyprland-macros.hpp:40), applied with a bound of 1 px and 1 Hz at the closeness test (Hyprland-Monitor.cpp:836-837). The running rate is the applied mode's own rate (Hyprland-Monitor.cpp:903).

**OBS** S313 - the logical size is computed in double precision: `constexpr Vector2D operator/(const double& a) const { return Vector2D(this->x / a, this->y / a);` (hyprutils-Vector2D.hpp:39). The logical size of the written scale is that division (Hyprland-Monitor.cpp:996), and the correction runs only when it is fractional and `debug:disable_scale_checks` is unset (Hyprland-Monitor.cpp:997; the option is read at Hyprland-Monitor.cpp:721).

**OBS** S306 - the search starts from the nearest 1/120 step: `float searchScale = std::round(m_scale * 120.0);` (Hyprland-Monitor.cpp:1001; whitespace-normalized). The correction (Hyprland-Monitor.cpp:997-1027) keeps that step when it divides the pixel size, else tries one step up then one down for up to 89 steps; for a written scale with no clean divisor Hyprland uses its default scale and shows an error (Hyprland-Monitor.cpp:1029-1036), and with one it uses the corrected value and shows a notification unless `misc:disable_scale_notification` is set (Hyprland-Monitor.cpp:1038-1049).

**OBS** S308 - an explicit position is applied as written before any auto placement: `m->moveTo(*POS); arranged.push_back(m); it = toArrange.erase(it);` (Hyprland-MonitorPositionController.cpp:27; whitespace-normalized across lines 27-29). The auto directions are placed afterwards (Hyprland-MonitorPositionController.cpp:61-101).

## §4 What `hyprctl monitors all -j` shows

**OBS** S307 - the JSON prints the running rate with five decimals: `"physicalHeight": {}, "refreshRate": {:.5f},` (Hyprland-HyprCtl.cpp:241-242). Its width and height are the pixel size, `scale` the applied scale, `disabled` the negation of enabled, and `mirrorOf` the id of the mirrored output or `none` (Hyprland-HyprCtl.cpp:276-288).

**OBS** The request takes one optional argument; only the word `all` selects allMonitors instead of monitors (Hyprland-HyprCtl.cpp:313-327).

**OBS** S311 - every real output enters the full list when it is added, before the enabled check: `mon->m_self = mon; m_realMonitors.emplace_back(mon);` (Hyprland-MonitorState.cpp:112-114). The active list is filled by the monitor-added event and drops mirrors on layout changes (Hyprland-MonitorState.cpp:24-46), and that event fires only for an output whose rule enables it (Hyprland-Monitor.cpp:264 and Hyprland-Monitor.cpp:389), so plain `hyprctl monitors -j` omits disabled outputs and only the `all` form can show a `disable` rule taking effect.

hyprland monitor-rule default_refresh=60 refresh_tolerance=1 scale_step=1/120 scale_search=89 json_refresh_decimals=5 line_keys=8

## §5 The documentation

**OBS** S310 - the wiki gives the line as `monitor = name, resolution, position, scale` (wiki-Monitors.md:11).

**INF** The wiki documents (wiki-Monitors.md:7-12) the same positional order the handler parses. It also documents a `, sdr_eotf, X` key on the monitor line (wiki-Monitors.md:253), but the host's line handler key loop has no `sdr_eotf` (Hyprland-legacy-ConfigManager.cpp:1351-1379), so a `monitor =` line carrying it is rejected whole; only a `monitorv2` block reads `sdr_eotf` (Hyprland-legacy-ConfigManager.cpp:819-831), and the wiki's own monitorv2 table lists it too (wiki-Monitors.md:300-320). Not exercised on the host.

## §6 On this host (2026-10-26, read-only)

**OBS** `~/.config/hypr/monitors.conf` declares one rule, DP-1 at 3440x1440@100, position 0x0, scale 1; `hyprctl monitors all -j` reports DP-1 at 3440x1440, 99.99700 Hz, 0x0, scale 1, transform 0, not disabled, mirroring none; tools/mado-monitors.py reports AGREE and verdict OK, exit 0 (.ufo/waves/round-45/receipts/live-monitors-host-l1.txt).

**INF** The 99.997 Hz is the applied mode's own rate; whether the requested 100 Hz counted as close (the 0.003 Hz gap is inside the strict 1 Hz bound) or a custom 100 Hz mode was tried first and rejected, the same native mode would run, so the agreement is the tool's 1 Hz tolerance mirroring Hyprland's bound, not proof of which branch ran. Earlier rounds held this pair as a point observation with an EDID class (config-health-report-r3.md); this entry grounds the selection, not the panel's EDID timing.

**UNK** Whether the output would run 59.99 Hz under a rule without `@100`, and whether a fractional scale would be corrected as computed, are not exercised: both need a config change, which is the operator's.

## Limits

- Code-read facts at efb5099, hyprutils v0.14.2 and aquamarine v0.15.1; nothing here was run against a changed config.
- `monitorv2` blocks are handled after the whole config parse and replace same-selector rules (Hyprland-legacy-ConfigManager.cpp:743-747); this entry does not trace their field parsing beyond `sdr_eotf`.
- The long description is rebuilt only for DRM outputs; a Wayland or headless backend builds its description differently and is not covered.
- Upstream main has removed the hyprlang line form (Hyprland a9902ea); everything about the `monitor =` grammar is true of the 0.56.x line only.
