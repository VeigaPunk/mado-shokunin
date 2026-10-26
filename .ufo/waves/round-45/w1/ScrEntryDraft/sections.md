# C2 entry — alternative prose for three weak sections (ScrEntryDraft, w1 round 45)

For the L1 to merge into `corpus/knowledge/hyprland-monitor-rule-r45.md`. No new S### ids; the pins are named by file, and every locator is
`<pin>:<line>` or `<pin>:<a>-<b>` with `b-a+1 <= 30`. Proof that each locator resolves: `locators.txt` in this directory (produced by
`verify-locators.py`, which runs `grep -n` on every anchor and refuses any range wider than 30 lines or any anchor outside it).

Pins (read-only copies under `.ufo/waves/round-45/fetch/`, sha256 in `.ufo/waves/round-45/receipts/fetch-sha256.txt`):
`Hyprland-Parser.cpp`, `Hyprland-legacy-ConfigManager.cpp`, `Hyprland-MonitorRuleManager.cpp`, `Hyprland-MonitorRule.hpp`,
`Hyprland-Monitor.cpp`, `Hyprland-HyprCtl.cpp`, `Hyprland-MonitorPositionController.cpp`, `hyprutils-String.cpp`, `wiki-Monitors.md`.
Host receipts in this directory: `live-modes-host.txt` (projected: name + `availableModes` only), `monitors-conf-lines.txt` (`grep -n` of
`~/.config/hypr/monitors.conf`; config text, no session material).

---

## §3.5 How to read a DIFFER (new section, sits after §3)

**OBS** A DIFFER is a field disagreement, not proof of a wrong config: the pins hold three mechanisms that produce a running state departing
from every written rule while each file is still honoured as written (Hyprland-HyprCtl.cpp:1188-1190, Hyprland-MonitorRuleManager.cpp:44-46,
Hyprland-Monitor.cpp:836-839).

**OBS** (a) A runtime `keyword monitor` rule lives in no file. The `keyword` request — registered to `dispatchKeyword`
(Hyprland-HyprCtl.cpp:2037) — marks the parse dynamic and hands the text to `parseKeyword` on the legacy config manager
(Hyprland-HyprCtl.cpp:1188-1190); `parseKeyword` is one `parseDynamic`
call on the Hyprlang config object that also registers the `monitor` handler (Hyprland-legacy-ConfigManager.cpp:1089-1090,
Hyprland-legacy-ConfigManager.cpp:606) [INF: the hop from `parseDynamic` to the registered handler is Hyprlang's and is not in the pins].
`handleMonitor` then ends in the same `monitorRuleMgr()->add(...)` a file line reaches (Hyprland-legacy-ConfigManager.cpp:1384), and
`dispatchKeyword` schedules a monitor reload for any command containing `monitor` (Hyprland-HyprCtl.cpp:1200-1202).

**OBS** Because `add` erases every same-selector rule before appending (Hyprland-MonitorRuleManager.cpp:37-42) and the lookup returns the
newest match (Hyprland-MonitorRuleManager.cpp:96-100), a rule typed at runtime shadows the file's rule for that output, and the file still
says what it always said.

**OBS** Reading rule (a): when the dump disagrees with every line of every config file, look for a keyword before a typo — the text on disk
cannot show a keyword (Hyprland-HyprCtl.cpp:1200-1202).

**OBS** (b) An output-management client rewrites the chosen rule before it is applied. `get()` wraps the matched rule in
`applyWlrOutputConfig`, which asks the wlr-output-management protocol for a committed state (Hyprland-MonitorRuleManager.cpp:44-46) and,
when one exists, replaces mode and rate, position, transform and scale with it (Hyprland-MonitorRuleManager.cpp:56-75).

**OBS** Reading rule (b): a DIFFER confined to the fields a display-configuration client manages — mode, position, transform, scale — is the
client's doing, not the line's (Hyprland-MonitorRuleManager.cpp:56-75).

**OBS** (c) The requested mode may not be one the output offers. For `WxH@R` Hyprland sorts the advertised modes by closeness
(Hyprland-Monitor.cpp:822-834) and, when the best is outside 1 px and 1 Hz, appends the request itself as a custom mode
(Hyprland-Monitor.cpp:836-839); if no candidate passes, it takes the first advertised mode that does and raises a warning notification
(Hyprland-Monitor.cpp:942-957).

**OBS** Reading rule (c): the running mode can be a mode the panel never advertised, or a mode nobody asked for — and the second leaves no
trace in `monitors all -j` beyond the applied fields (Hyprland-HyprCtl.cpp:276-289, Hyprland-Monitor.cpp:942-957).

**OBS** (d) The inverse catches more readers than the three causes: a comparison that reuses Hyprland's own 1 px / 1 Hz bound
(Hyprland-Monitor.cpp:836-837) reports AGREE for a rule asking 60 Hz against a mode running 59.99 Hz — see §1.5 below.

**OBS** Which of (a)-(c) applies is decidable from what the dump cannot show: the rule itself (Hyprland-HyprCtl.cpp:230-259), the client's
commit, and the custom-mode attempt are all off-dump, so a DIFFER is resolved by reading the rules and, if they match, by asking who else can
write the state (Hyprland-MonitorRuleManager.cpp:44-46).

---

## §1.5 The 60 Hz default, and what it does to a commented omarchy line (new subsection, sits inside §1)

**OBS** A `WxH` field with no `@` keeps the rule's default rate of 60 (Hyprland-MonitorRule.hpp:46): the parser assigns a rate only when the
field contains `@` (Hyprland-Parser.cpp:132-136). `monitor = DP-1, 3440x1440, 0x0, 1` therefore asks 3440x1440@60, not the output's fastest
mode.

**OBS** Keyword modes never consult that rate. `preferred` discards the request and takes the output's first three modes plus its preferred
mode (Hyprland-Monitor.cpp:773-783); `highrr` and the two keywords after it sort by rate or size instead
(Hyprland-Monitor.cpp:784-794, Hyprland-Monitor.cpp:807-817).

**OBS** In `~/.config/hypr/monitors.conf` every commented example either uses `preferred` (lines 7, 14, 19, 22) or carries an explicit `@`
rate (lines 25, 26) (receipt monitors-conf-lines.txt:7,14,19,22,25,26), so uncommenting any of them whole requests no implicit 60 Hz.

**OBS** The hazard is an edit, not the template: deleting `@100` from the active line 10 leaves `monitor = DP-1, 3440x1440, 0x0, 1`
(receipt monitors-conf-lines.txt:10), a 60 Hz request (Hyprland-MonitorRule.hpp:46).

**OBS** On this host that edit would be quiet. DP-1 advertises `3440x1440@59.99Hz` among its eleven modes (receipt live-modes-host.txt), which
sits inside the 1 Hz bound, so the 60 Hz request would resolve to that mode (Hyprland-Monitor.cpp:822-834, Hyprland-Monitor.cpp:878-887) and every compared field
would agree: the desktop at 59.99 Hz, the verdict AGREE (Hyprland-Monitor.cpp:836-837).

**UNK** The switch itself is not exercised: the config change is the operator's, so the 59.99 Hz landing is read from the advertised list and
the candidate order, not observed (Hyprland-Monitor.cpp:878-887).

---

## §4 additions — what `monitors all -j` omits (replaces the single ¶ after the JSON field list)

**OBS** No rule echo. The JSON format carries applied values only: no selector, no requested mode, no requested rate
(Hyprland-HyprCtl.cpp:230-259, Hyprland-HyprCtl.cpp:260-289), while the applied rule is kept in `m_activeMonitorRule` and never printed
(Hyprland-Monitor.cpp:653) — a grep of the dump builder for it returns nothing (locators.txt, negative check N2).

**OBS** No long description. `description` is the short form, `make model serial` with commas erased (Hyprland-HyprCtl.cpp:277,
Hyprland-Monitor.cpp:250-256), so a `desc:` selector that matched only the long description cannot be reproduced from the dump
(Hyprland-Monitor.cpp:1201-1211).

**OBS** Advertised modes only, at two decimals. `availableModes` is built from the output's own mode list with `{:.2f}`
(Hyprland-HyprCtl.cpp:123-134), while the running rate is printed with five (Hyprland-HyprCtl.cpp:241-242); reading `59.99` in the list
against `59.99400` in `refreshRate` is a formatting gap, not a DIFFER.

**OBS** Disabled outputs only with `all`. `monitors -j` prints `monitors()` and `monitors all -j` prints `allMonitors()`
(Hyprland-HyprCtl.cpp:313-321), and the wiki calls `hyprctl monitors all` the list of "all available monitors (active and inactive)"
(wiki-Monitors.md:23-26); without `all`, DISABLED and absent look the same.

**OBS** The written scale is absent. `scale` is the applied value after the 1/120 search (Hyprland-HyprCtl.cpp:282,
Hyprland-Monitor.cpp:996-1010), so a rule asking a scale with no clean divisor shows the corrected step while the file keeps the number
nobody compared.

**OBS** Positions have no provenance. An `auto*` field writes a direction and a sentinel offset, not a number (Hyprland-Parser.cpp:145-149),
and `x`/`y` are the applied layout position (Hyprland-HyprCtl.cpp:282), so a position comparison is only meaningful against an explicit
offset.

**OBS** Mirroring is an id or `none` (Hyprland-HyprCtl.cpp:286), so a rule's `mirror = NAME` has to be resolved through the `id` field before
anything can be compared.

---

## Locator inventory (each ≤ 30 lines; resolved by grep -n in locators.txt)

| locator | lines | anchor |
|---|---|---|
| Hyprland-HyprCtl.cpp:1188-1190 | 3 | dynamic keyword flag, `parseKeyword` |
| Hyprland-HyprCtl.cpp:1200-1202 | 3 | `contains("monitor")` → `scheduleReload()` |
| Hyprland-HyprCtl.cpp:123-134 | 12 | `availableModes` from `m_output->modes`, `{:.2f}` |
| Hyprland-HyprCtl.cpp:230-259 | 30 | JSON format string, first half (no rule field) |
| Hyprland-HyprCtl.cpp:260-289 | 30 | JSON format string, second half |
| Hyprland-HyprCtl.cpp:241-242 | 2 | `"refreshRate": {:.5f}` |
| Hyprland-HyprCtl.cpp:276-289 | 14 | applied fields: scale, transform, disabled, mirrorOf |
| Hyprland-HyprCtl.cpp:277 | 1 | `description` fed `m_shortDescription` |
| Hyprland-HyprCtl.cpp:282 | 1 | `m_scale`, `m_transform` arguments |
| Hyprland-HyprCtl.cpp:286 | 1 | `mirrorOf` = id or `none` |
| Hyprland-HyprCtl.cpp:313-321 | 9 | `monitors all` switch |
| Hyprland-HyprCtl.cpp:2037 | 1 | `keyword` command → `dispatchKeyword` |
| Hyprland-legacy-ConfigManager.cpp:606 | 1 | `registerHandler(&::handleMonitor, "monitor", ...)` |
| Hyprland-legacy-ConfigManager.cpp:1089-1090 | 2 | `parseKeyword` → `parseDynamic` |
| Hyprland-legacy-ConfigManager.cpp:1384 | 1 | `monitorRuleMgr()->add(...)` at handler end |
| Hyprland-Monitor.cpp:250-256 | 7 | long vs short description construction |
| Hyprland-Monitor.cpp:653 | 1 | `m_activeMonitorRule = std::move(pMonitorRule)` |
| Hyprland-Monitor.cpp:773-783 | 11 | `preferred` branch (rate unused) |
| Hyprland-Monitor.cpp:784-794 | 11 | `highrr` sort |
| Hyprland-Monitor.cpp:807-817 | 11 | `maxwidth` sort |
| Hyprland-Monitor.cpp:822-834 | 13 | closeness sort for `WxH@R` |
| Hyprland-Monitor.cpp:836-839 | 4 | 1 px / 1 Hz bound → custom mode push |
| Hyprland-Monitor.cpp:878-887 | 10 | candidate loop, `requestedModes` in reverse |
| Hyprland-Monitor.cpp:942-957 | 16 | fallback to first working mode + notification |
| Hyprland-Monitor.cpp:996-1010 | 15 | 1/120 scale search start |
| Hyprland-Monitor.cpp:1201-1211 | 11 | `matchesStaticSelector`, `desc:` on long or short |
| Hyprland-MonitorRule.hpp:46 | 1 | default `m_refreshRate = 60` |
| Hyprland-MonitorRuleManager.cpp:37-42 | 6 | `add`: erase same selector, append |
| Hyprland-MonitorRuleManager.cpp:44-46 | 3 | `applyWlrOutputConfig` hook |
| Hyprland-MonitorRuleManager.cpp:56-75 | 20 | client overrides mode/pos/transform/scale |
| Hyprland-MonitorRuleManager.cpp:96-100 | 5 | reverse lookup, newest match |
| Hyprland-Parser.cpp:132-136 | 5 | rate read only when `@` present |
| Hyprland-Parser.cpp:145-149 | 5 | `auto*` position → sentinel + direction |
| wiki-Monitors.md:23-26 | 4 | `hyprctl monitors all` = active and inactive |

---

## Appendix — four over-width locators in the L1 draft, and narrower replacements

`entry-locator-widths.txt` (this directory) extracts every locator from `l1-draft/entry.md` and measures it: four exceed the 30-line bound
(draft lines 34, 54, 60, 62). Each splits into ranges inside the bound without losing an anchor, and every replacement below is grep-verified
in `locators.txt` (the four draft locators are quoted with a space, not a colon, so this checker does not count them as
mine):

| draft locator (width) | narrow replacement (width) | what it keeps |
|---|---|---|
| draft entry.md:34 — legacy-ConfigManager 1299-1343 (45) | Hyprland-legacy-ConfigManager.cpp:1299-1320 (22) + Hyprland-legacy-ConfigManager.cpp:1321-1343 (23) | branch head and transform copy; addreserved and fall-through add |
| draft entry.md:54 — MonitorRuleManager 45-84 (40) | Hyprland-MonitorRuleManager.cpp:44-46 (3) + Hyprland-MonitorRuleManager.cpp:56-75 (20) + Hyprland-MonitorRuleManager.cpp:77-84 (8) | protocol hook; mode/position/transform/scale overrides; vrr override and return |
| draft entry.md:60 — Monitor 784-817 (34) | Hyprland-Monitor.cpp:784-794 (11) + Hyprland-Monitor.cpp:807-817 (11) | `highrr` sort; `maxwidth` sort |
| draft entry.md:62 — Monitor 997-1027 (31) | Hyprland-Monitor.cpp:996-1010 (15) + Hyprland-Monitor.cpp:1011-1027 (17) | 1/120 search start; the up/down loop body |

Two more draft locators are inside the bound but point at a range that does not carry the sentence's subject, and the narrow fix is free:
`Hyprland-legacy-ConfigManager.cpp` 1345 cites the three positional parses, while the comma split the same sentence describes is one line
higher at `Hyprland-legacy-ConfigManager.cpp:1295`; and `Hyprland-HyprCtl.cpp:313-321` supports the `all` switch but not the claim that
disabled outputs are the ones it adds, which the wiki states at `wiki-Monitors.md:23-26`.
