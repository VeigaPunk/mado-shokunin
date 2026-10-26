# CritEntryContent — sentence-by-sentence pin check of the L1 draft entry

Target: `.ufo/waves/round-45/l1-draft/entry.md` (C2 coverage, round 45 w1, 2026-10-26).
Method: every sentence opened against the pinned source in `.ufo/waves/round-45/fetch/` at Hyprland
`efb50993780079460b0cbed1363e2166a2de1d9f` (v0.56.2) / hyprutils `v0.14.2`, plus the four files this
review had to fetch to answer the assigned questions (pinned below). Every quote in this file is
grep-verified: `quote-verdicts.txt` (70/70 literal) is the receipt.

Verdict vocabulary: **S** supported · **S\*** supported but the locator, the quote or a config gate is
defective · **O** overclaimed · **W** wrong · **U** unsupported (claim with no locator anywhere).

## Pins added by this seat (all under `w1/CritEntryContent/pins/`, sha256 in `PIN-SHA256.txt`)

| file | source | sha256 | why |
|---|---|---|---|
| `MonitorState.cpp` | Hyprland @efb5099 `src/state/MonitorState.cpp` | `b5033be770b95f13b9ca65d9f60daae2446910e946576156c50dae8da89cab1c` | what `monitors()` vs `allMonitors()` hold (the `all` claim) |
| `aquamarine-DRM.cpp` | aquamarine **v0.15.1** (host `pacman -Q aquamarine` = 0.15.1-1) `src/backend/drm/DRM.cpp` | `ff9b19d823a0f2f8b365ba7efd4b09bf9515fcfcdb10f3b1ae505abd6d1977b3` | where `m_description` comes from (line 2101) |
| `aquamarine-Output.cpp` | aquamarine v0.15.1 `src/output/Output.cpp` | `bb9351ba01ae04e2389763c8261ea5ba9ecc5de7f42ab9dff6566323cdc098ea` | control: no `description` assignment here |
| `macros.hpp` | Hyprland @efb5099 `src/macros.hpp` | `b62d51406768f08d3a820c882de77ac47b55c15693b68322180ff2002164d738` | `DELTALESSTHAN` is `abs(a-b) < delta` (line 40) |
| `Math.hpp` | Hyprland @efb5099 `src/helpers/math/Math.hpp` | `26e71b8ba323d68015b6e7c67abab4ec125b9e5f996acce9413af27d9dce2b5b` | negative control: no `DELTALESSTHAN` here |
| `VarList2.hpp` / `VarList2.cpp` | hyprutils v0.14.2 | `0e484df50ec18ef432c319a4d3249dfc3ddf25bb990a836ebcdd597a441f2179` / `b8cacea741b2d6260ad6618be00e37bc01c4d092e655a7557f7cfbadb76cf26d` | the comma split the whole entry rests on |
| `MonitorLayoutController.cpp` | Hyprland @efb5099 `src/state/MonitorLayoutController.cpp` | `0190e7496f1f7b90a4c596ecfe2cb973f65b96d1876a2b3273f360226b41cb0b` | any later clamp/overlap fix after placing positions |

## Tally

| verdict | count |
|---|---|
| S | 24 |
| S\* | 12 |
| O | 3 |
| W | 1 |
| U | 0 |
| total adjudicated | 40 |

No sentence is unsourced. One is **wrong** (Limits ¶3), three **overclaim** (licenses row 4, §3 ¶2, §6 ¶3),
and five **quotes fail a literal grep** — the C2 gate greps quotes, so those five are mechanical defects,
not style.

## Table A — every sentence

| # | sentence (draft locator) | verdict | evidence | corrected text |
|---|---|---|---|---|
| E1 | licenses r1 "one rule per selector string, searched newest first; else the first empty-selector rule; else a built-in default" | S | `Hyprland-MonitorRuleManager.cpp:38` erase-by-name, `:39` append, `:96` reverse walk, `:104` empty-selector, `:108-116` hardcoded default | — |
| E2 | licenses r2 "`WxH` without `@RATE` … keeps its 60 Hz default, so the mode closest to 60 Hz at that size is chosen" | S | `Hyprland-MonitorRule.hpp:46` (`m_refreshRate   = 60; // Hz`), `Hyprland-Monitor.cpp:828` rate tiebreak after width/height | — |
| E3 | licenses r3 "closeness test: within 1 px and 1 Hz" | S | `Hyprland-Monitor.cpp:836-837` + `pins/macros.hpp:40` (`abs(a-b) < (delta)`, strict) | say "strictly less than 1 px and 1 Hz" |
| E4 | licenses r4 "only when it divides the pixel size; otherwise the nearest multiple of 1/120 that does (89 steps up and down)" | **O** | the whole correction sits behind `Hyprland-Monitor.cpp:997` `if (!*PDISABLESCALECHECKS` (`:721` = `debug:disable_scale_checks`) | append "unless `debug:disable_scale_checks` is set (`Hyprland-Monitor.cpp:721,997`), which skips the correction entirely" |
| E5 | licenses r5 "explicit offsets are placed as written; `auto*` positions are computed after them" | S | `Hyprland-MonitorPositionController.cpp:21-38` (explicit loop) then `:52-70` (auto loop) | — |
| E6 | licenses r6 "eight keys; any other key rejects the whole line" | S | `Hyprland-legacy-ConfigManager.cpp:1352-1376` (mirror, bitdepth, cm, sdrsaturation, sdrbrightness, transform, vrr, icc), `:1377-1378` reject, `:1384` add | — |
| E7 | licenses r7 "the wiki documents it; the host's handler reads it only in `monitorv2` blocks" | S | `wiki-Monitors.md:253`; `Hyprland-legacy-ConfigManager.cpp:819-831` reads `monitorv2`/`sdr_eotf` only | — |
| E8 | licenses r8 "one output, one rule, AGREE on every compared field" | S | `receipts/live-monitors-host-l1.txt` (5 lines, incl. `[{"name": "DP-1", … "refreshRate": 99.997 …}]`) | — |
| E9 | §1 ¶1 "splits the line on commas, takes field 0 as the selector and parses the next three fields positionally: `parser.parseMode(…); parser.parsePosition(…); parser.parseScale(…);` (…ConfigManager.cpp:1345)" | S\* | `Hyprland-legacy-ConfigManager.cpp:1295` `CVarList2(std::string(args))`, `:1297` `ARGS[0]`, `:1345-1347` the three calls; comma default is `hyprutils` `VarList2.hpp:18` (`const char delim = ','`) — **not among the pinned set** | quote each call on its own line and cite `:1345-1347`; add `VarList2.hpp:18` to the pin set, because "on commas" is not evidenced by any of S302–S310 |
| E10 | §1 ¶2 "first checks field 1 for `disable`/`disabled` …, `transform` (copy the first rule with the same selector, set its transform, add the copy) and `addreserved` (…or fall through and add a default rule…) (…:1293-1299 / 1299-1343)" | S | `:1299` the four-word guard, `:1302-1318` transform (`:1312` `cpy.m_transform = TRANSFORM;`), `:1319-1341` addreserved (`:1329` find_if on `allMut()`), `:1341` add | — |
| E11 | §1 ¶3 "KEY, VALUE pairs until an empty field: mirror, bitdepth, cm, sdrsaturation, sdrbrightness, transform, vrr, icc; any other key logs and returns "invalid syntax" before the rule is added, so the whole line is dropped (…:1351-1379)"; "a parse error inside a known field does not stop the add … (…:1384-1386)" | S | `:1351` loop, `:1377` log, `:1378` return before `:1384` add, `:1386` `return parser.getError();` | optionally add the degradation the code shows: a bad mode falls back to preferred, a bad scale to auto, a bad position to auto (`Parser.cpp:136-139, 195-199, 176-186`) — an errored rule still applies |
| E12 | §1 ¶4 "`preferred` when empty or starting `pref`; `highrr`, `highres` and `maxwidth` are keywords; a `modeline` keyword parses a custom DRM mode; otherwise … an `x` … `stoi` … rate after `@` (…Parser.cpp:110-139)" | S\* | `Hyprland-Parser.cpp:111` (`starts_with("pref")`), `:119` `parseModeLine`, but the "modeline" keyword test is at `:20` (`if (keyword != "modeline")`), outside the cited range | cite `:14-20,119` for the modeline clause |
| E13 | §1 ¶5 "the rate is read only when an `@` is present: `m_rule.m_refreshRate = stof(value.substr(value.find_first_of('@') + 1));` (Parser.cpp:134)" | S | quote literal at `Hyprland-Parser.cpp:134` (grep-verified) | — |
| E14 | §1 ¶6 "without `@` the rule keeps its default rate: `float m_refreshRate = 60;` (MonitorRule.hpp:46). A rule … therefore asks for 60 Hz, not for the output's fastest mode." | S\* | content right (`Hyprland-MonitorRule.hpp:46` = `float                        m_refreshRate   = 60; // Hz`; `Monitor.cpp:823-831` prefers 60 Hz at the requested size) | quote the line as it stands or drop the quote and cite `:46`: the draft's de-spaced form fails a literal grep |
| E15 | §1 ¶7 "parsePosition (145-173): … otherwise the field must hold an `x` and both halves go through `stoi`" | S\* | auto branch `Hyprland-Parser.cpp:146-180`; but the `x`/`stoi` branch is `:181-182`, **outside 145-173** (function ends `:191`) | cite `:145-191` |
| E16 | §1 ¶8 "parseScale (193-211): … a value below 0.25 is replaced by 1 with an error" | S | `Hyprland-Parser.cpp:195` (`m_rule.m_scale = -1;`), `:203-206` (`0.25F` → error, m_scale = 1), `:210-211` close | — |
| E17 | §1 ¶9 "minus sign only first: `if (i == 0 && str.at(i) == '-') {` (String.cpp:59); isNumber2 (50-79) … one `.` (not first) … last character a digit (String.cpp:83), so a scale written `1.` fails the test and the rule keeps auto scale" | S | `hyprutils-String.cpp:59` (literal), `:71-72`, `:74-77`, `:83` `return isdigit(str.back()) != 0;`; `Parser.cpp:195` keeps `-1` (auto) on failure | — |
| E18 | §2 ¶1 "adding a rule first erases every rule with the same selector: `std::erase_if(…)` (…:38) … appends, so a re-added selector moves to the end (…:37-42)" | S | `Hyprland-MonitorRuleManager.cpp:38-39` (both literal) | — |
| E19 | §2 ¶2 "walks the list in reverse … newest matching rule wins; with none … first rule whose selector is empty, then a built-in default (preferred, auto, auto) (…:96-106)" | S\* | `:96` reverse walk, `:104` empty check; but the hardcoded default is `:108-116`, outside the cited range, and `:86-93` (`if (PMONITOR->m_isUnsafeFallback)`) is an earlier exit the tool needs to know about | cite `:86-116`; add "a monitor flagged `m_isUnsafeFallback` never reaches the rules and is forced to 1920x1080, auto-right, scale 1 (`:86-93`)" |
| E20 | §2 ¶3 "an output-management client's committed state overrides the chosen rule's fields before it is applied (…:45-84) …" | S | `Hyprland-MonitorRuleManager.cpp:45` lambda, `:65` `rule.m_offset = CONFIG->position;` among six overrides | — |
| E21 | §2 ¶4 "the selector matches by exact output name, or with `desc:` when the long or the short description starts with the trimmed text (Monitor.cpp:1201-1211)" | S\* | `Hyprland-Monitor.cpp:1204` (trim of `selector.substr(5)`), `:1206` (`m_description.starts_with(…) \|\| m_shortDescription.starts_with(…)`), `:1209` exact name. The term "long description" is never defined anywhere in the entry | define it: `m_description` = aquamarine `IOutput::description` with commas erased (`Hyprland-Monitor.cpp:250-252`), and on the DRM backend that string is exactly `` `{make} {model} {serial} ({connector})` `` (`pins/aquamarine-DRM.cpp:2015,2101`) |
| E22 | §2 ¶5 "the short description is make, model and serial with commas removed (Monitor.cpp:255-256), and that short form is what `hyprctl monitors -j` prints as `description` (HyprCtl.cpp:277)" | S | `:255` `trim(std::format("{} {} {}", make, model, serial))`, `:256` comma erase, `HyprCtl.cpp:277` `escapeJSONStrings(m->m_shortDescription)` | — |
| E23 | §3 ¶1 "sorted by closeness in width, then height, then rate, and when the best one is not within 1 px and 1 Hz … the requested mode is tried first as a custom mode (Monitor.cpp:819-840)" | S\* | comparator `:823-831` (`:828` the rate leg), custom push `:836-839`; "tried first" comes from the reverse iteration at `:878` (`for (auto const& mode : requestedModes \| std::views::reverse)`), outside the cited range | add `:878` to the locator |
| E24 | §3 ¶1 "`highrr`, `highres` and `maxwidth` sort by rate or size instead (…:784-817)" | S | `Hyprland-Monitor.cpp:785-817`, `:807` is the maxwidth branch | — |
| E25 | §3 ¶2 "when the written scale would leave a fractional logical size the search starts from the nearest 1/120 step: `float searchScale = std::round(m_scale * 120.0);` (…:1001)" | **O** | `:997` gates the whole block on `!*PDISABLESCALECHECKS` (`:721`, `debug:disable_scale_checks`); source line is `float    searchScale = …` so the draft quote fails a literal grep | "unless `debug:disable_scale_checks` (`:721`)"; quote the line with its real spacing or cite `:1001` |
| E26 | §3 ¶3 "keeps that step when it divides … else one step up then one down for up to 89 steps; … no clean divisor falls back to its default scale and shows an error (1029-1036), and with one it shows a notification and uses the corrected value (1038-1049)" | S\* | `:1029` `if (!found) {`, `:1034` queueError, `:1035` `m_scale = getDefaultScale();`, `:1048` `m_scale = searchScale;`; the notification is itself gated on `misc:disable_scale_notification` (`:1040`) | add the second gate: "…shows a notification, unless `misc:disable_scale_notification` is set (`:1040`)" |
| E27 | §3 ¶4 "an explicit position is applied as written before any auto placement: `m->moveTo(*POS); arranged.push_back(m); it = toArrange.erase(it);` (…PositionController.cpp:27)" | S\* | placing loop `Hyprland-MonitorPositionController.cpp:24-38` (`:27` `m->moveTo(*POS);`) before the auto loop `:52-70`; nothing clamps: `Hyprland-Monitor.cpp:1725` `m_position = pos;`, and the only later check is `pins/MonitorLayoutController.cpp:44`, which logs + notifies an overlap and never moves anything | quote `:27-29` per line; add "an overlapping layout is only reported (`MonitorLayoutController.cpp:38-51`), never repaired" — that closes "any later clamp/fix?" |
| E28 | §4 ¶1 "the JSON prints the running rate with five decimals: `"physicalHeight": {}, "refreshRate": {:.5f},` (HyprCtl.cpp:241-242)" | S\* | `Hyprland-HyprCtl.cpp:242` `"refreshRate": {:.5f},` (literal); the value is the chosen mode's rate, `Hyprland-Monitor.cpp:903` `m_refreshRate = mode->refreshRate / 1000.f;` | quote per line; cite `:242` for the quote, `:241-242` only if the field pair is the point |
| E29 | §4 ¶2 "width/height are the pixel size, `scale` the applied scale, `disabled` the negation of enabled, `mirrorOf` the id … or `none` (…:276-288)" | S | `Hyprland-HyprCtl.cpp:279-286`: `m->m_pixelSize`, `m->m_scale`, `:285` `(m->m_enabled ? "false" : "true")`, `:286` `m->m_mirrorOf ? … : "none"` | — |
| E30 | §4 ¶3 "The request takes one optional argument; only the word `all` lists every output including disabled ones, otherwise only the active list is printed (…:313-321)" | S\* | `Hyprland-HyprCtl.cpp:317` "too many args", `:320-321` `vars[1] == "all"`, `:327` selection; the list semantics are elsewhere: `pins/MonitorState.cpp:50` `return m_realMonitors;` (filled at `:114` for **every** output, before the `:122` `if (!mon->m_enabled)`), `:54` `return m_monitors;` (enabled, non-mirror: `:33` drops mirrors, `:22-27` event-driven), and `Hyprland-Monitor.cpp:389` emits `monitor.added` only inside the `:264` `if (m_enabled && !monitorRule.m_disabled)` block, so a disabled output never joins the active list | add the MonitorState pin + `Hyprland-Monitor.cpp:264,389`; note `HyprCtl.cpp:225` blanks an entry whose `m_id == -1`, which cannot happen for a real output because `MonitorState.cpp:111` always assigns an id |
| E31 | §5 ¶1 "the wiki gives the line as `monitor = name, resolution, position, scale` (wiki-Monitors.md:11)" | S | `wiki-Monitors.md:11` (literal) | — |
| E32 | §5 ¶2 "The wiki documents (wiki-Monitors.md:7-12) the same positional order the handler parses." | S | `wiki-Monitors.md:8-12` (lead-in + fence + line) | — |
| E33 | §5 ¶2 "… documents a `, sdr_eotf, X` key on the monitor line (…:253), but the host's handler key loop has no `sdr_eotf` (…:1351-1379), so a `monitor =` line carrying it is rejected whole; only a `monitorv2` block reads `sdr_eotf` (…:819-831)" | S | `wiki-Monitors.md:253` (literal); `Hyprland-legacy-ConfigManager.cpp:1352-1376` has eight keys and none is `sdr_eotf`, `:1378` returns before `:1384` add; `:819-831` reads it from the `monitorv2` category (`:576`) | optionally note the wiki also lists `sdr_eotf` in the v2 table (`wiki-Monitors.md:307,319`), so the divergence is narrower than "the wiki is wrong" |
| E34 | §6 ¶1 "`~/.config/hypr/monitors.conf` declares one rule, DP-1 at 3440x1440@100, position 0x0, scale 1" | S | `receipts/live-monitors-host-l1.txt`: `MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000`, config sha256 `69c9d899…` | — |
| E35 | §6 ¶1 "`hyprctl monitors all -j` reports DP-1 at 3440x1440, 99.99700 Hz, 0x0, scale 1, transform 0, not disabled, mirroring none; the round's tool reports AGREE and verdict OK, exit 0" | S | same receipt: projected dump line + `MADO_MON_OUTPUT … verdict=AGREE` + `MADO_MONITORS … agree=1 differ=0 verdict=OK` + `# exit=0` | — |
| E36 | §6 ¶2 "The 0.003 Hz gap is inside the 1 Hz closeness bound." | **O** | arithmetically true (`|99.997-100| = 0.003 < 1`, `Hyprland-Monitor.cpp:836-837`, `pins/macros.hpp:40`), but the bound is **not what produced the agreement**: had the gap been outside it, a custom 100 Hz mode would be pushed (`:836-839`) and tried first (`:878`), rejected (`:885-886`, `continue`), and the *same* native 99.997 Hz mode applied — so the gap is the panel's own rate (`:903`), and what makes the tool's AGREE legitimate is the tool's own refresh tolerance (census `refresh_tolerance=1`), not Hyprland's | "The 0.003 Hz gap is the display mode's own rate (99997 mHz); it is inside Hyprland's 1 Hz mode-selection tolerance (`Hyprland-Monitor.cpp:836-837`, `abs(a-b) < delta`), so no custom 100 Hz mode is attempted first. A larger gap would have added one rejected custom attempt (`:836-839`, `:878-889`) and landed on the same mode — the tool's agreement rests on the same 1 Hz tolerance, not on Hyprland's." |
| E37 | §6 ¶3 (UNK) "Whether the output would have run 59.99 Hz under a rule without `@100`, and whether a fractional scale would be corrected as computed, are not exercised" | S | consistent with the code: 60 Hz request → closest mode (`:828`), unexercised; scale correction needs a changed config (`:997-1051`) | — |
| E38 | Limits ¶1 "Code-read facts at efb5099 and hyprutils v0.14.2; nothing here was run against a changed config." | S | matches the receipt set (one live read-only run, no config change) | — |
| E39 | Limits ¶2 "`monitorv2` blocks are added after every `monitor =` line and replace same-selector rules; this entry does not trace their field parsing beyond `sdr_eotf`." | S\* | true and adjacent: `Hyprland-legacy-ConfigManager.cpp:743` `m_config->parse()` (the `monitor` handler runs here) then `:747` `handleMonitorv2();`, and replacement is `MonitorRuleManager.cpp:38` erase-by-name. **No locator in the sentence** | cite `Hyprland-legacy-ConfigManager.cpp:743,747` + `Hyprland-MonitorRuleManager.cpp:38`; say "after the whole config parse", not "after every line" |
| E40 | Limits ¶3 "The JSON carries only the short description, so a `desc:` selector that matches only the long description cannot be checked from the dump." | **W** | the dump carries `make`, `model`, `serial` (`Hyprland-HyprCtl.cpp:239-241`) and `name` (`:277`); on the DRM backend the long description is built from exactly those three plus the connector name (`pins/aquamarine-DRM.cpp:2101` `output->description = std::format("{} {} {} ({})", make, model, serial, szName);`, with `szName` the same string the output is constructed from at `:2015`), and Hyprland only erases commas (`Hyprland-Monitor.cpp:250-252`); indeed `Hyprland-Monitor.cpp:254` calls the suffix a "parenthesized DRM node name suffix". So the long form is reconstructible | "The JSON prints only the short description as `description`, but it also prints `make`, `model`, `serial` and `name`, so on the DRM backend the long description is reconstructible as `` `make model serial (name)` `` with commas erased (`aquamarine-DRM.cpp:2015,2101`; `Hyprland-Monitor.cpp:250-252`). A `desc:` selector that matches the long form but not the short is the short form plus a prefix of ``` (CONNECTOR)```, and stays checkable; only a non-DRM output with an empty `description` has no long form to check." |

## Defect detail

**W1 (E40)** — the entry's own Limits paragraph tells the reader a check is impossible that the dump
supports. This is the only wrong statement; it is also the one a C1-style tool would act on (marking a
`desc:`-selected rule unmatched). Fix as E40.

**O1 (E4)**, **O2 (E25)** — the 1/120 scale correction is described as unconditional; it is gated by
`debug:disable_scale_checks` (`Hyprland-Monitor.cpp:721,997`). Both rows/sentences need the gate, not a
rewrite.

**O3 (E36)** — causal attribution of the 99.997 → 100 agreement to Hyprland's 1 Hz bound. The mode applied
is the same either way; the bound only avoids a doomed custom-mode attempt. This matters because the
entry's own census line advertises `refresh_tolerance=1`, and a reader can come away thinking Hyprland
verified the rate against the rule.

**Quote mechanics (5)** — `quotecheck-draft.txt`: `GREP-FAIL` for
`Hyprland-legacy-ConfigManager.cpp:1345`, `Hyprland-MonitorRule.hpp:46`, `Hyprland-Monitor.cpp:1001`,
`Hyprland-MonitorPositionController.cpp:27`, `Hyprland-HyprCtl.cpp:241`; three controls pass
(`hyprutils-String.cpp:59`, `Hyprland-MonitorRuleManager.cpp:38`, `Hyprland-Parser.cpp:134`). Four of the
five join consecutive source lines into one quoted string; the fifth (`MonitorRule.hpp:46`) is a
column-aligned declaration quoted with single spaces. A gate that greps the quote will reject all five.

**Locator defects (5)** — each has the right fact but a range that excludes it:
`ConfigManager.cpp:1345` (should be `:1345-1347`), `Parser.cpp:110-139` for the modeline clause (needs
`:14-20`), `Parser.cpp:145-173` for the `stoi` half (needs `:145-191`), `RuleManager.cpp:96-106` for the
built-in default (needs `:108-116`), `Monitor.cpp:819-840` for "tried first" (needs `:878`).

**Missing pins behind stated facts (4)** — facts the entry asserts that none of S302–S310 evidences:
1. "splits on commas" → hyprutils `VarList2.hpp:18` (`const char delim = ','`) — S309 pins `String.cpp` only.
2. "`all` lists every output including disabled ones" → `MonitorState.cpp:49-55,111-122` + `Hyprland-Monitor.cpp:264,389`.
3. "the long description" → aquamarine `DRM.cpp:2015,2101` at the host's 0.15.1.
4. "within 1 px and 1 Hz" as a strict bound → `macros.hpp:40` (`DELTALESSTHAN`).

## Smallest safe corrections (for the L1)

1. Replace Limits ¶3 with the E40 text (one wrong → supported).
2. Insert the `debug:disable_scale_checks` gate into licenses r4 and §3 ¶2; insert the
   `misc:disable_scale_notification` gate into §3 ¶3.
3. Replace §6 ¶2 with the E36 text.
4. Re-quote the five failing quotes per source line, or drop the quote and keep the locator.
5. Widen/fix the five locators listed above; add the four pins (or cite them) so every asserted fact has a
   source in the S302–S310 set.
6. Optional, one clause each: the errored-rule degradation (E11), the `m_isUnsafeFallback` exit (E19), the
   overlap-only reporting (E27).

## Receipts in this seat

| file | content |
|---|---|
| `quote-verdicts.txt` | 70/70 quotes used in this review, literal-grep-verified against pins with line numbers |
| `quotecheck-draft.txt` | the 5 draft quotes that fail a literal grep + 3 controls that pass |
| `quotecheck.txt` / `quotecheck.sh` | first pass over the draft's own quotes |
| `PIN-SHA256.txt` | sha256 of every file this seat added |
| `QUOTES.tsv` | the quote list the verifier consumes |
