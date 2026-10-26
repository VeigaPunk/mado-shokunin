# SKILL.md additions for `tools/mado-monitors.py` — append-ready text

Seat `ScrSkillRows`, round 45 w1. Every block below names the exact line it goes after; nothing rewrites an existing row.
Insertion points are `SKILL.md` line numbers at the round freeze (base `0c89478a`, freeze `22a8dedd`).
Locators are pin positions computed with `grep -n` over `.ufo/waves/round-45/fetch/` (table at the end; re-check with
`w1/ScrSkillRows/verify-locators.py`).

---

## Block A — Claim-first routing row

**Goes after `SKILL.md:158`** (the `mado-geometry.py` routing row; last row of § "Claim-first routing"), matching that
table's four columns `| The claim you must settle | Route to | Run (read-only) | Tag |`:

| Does each connected output run the mode, position, scale and transform its monitor rule declares? | two read-only inputs, no new verb: file bytes (the `monitor =` lines) + hyprctl live (`monitors all -j`, which also lists disabled outputs, `Hyprland-HyprCtl.cpp:313-321`) | `hyprctl monitors all -j \| python3 tools/mado-monitors.py --monitors - --config ~/.config/hypr/monitors.conf`; per-verdict licence and exit map in § "Monitor rule versus running output" | `[OBS]` for both printed sides (the rule fields and the running fields); which rule the output got is `[INF]` — a source re-implementation of the lookup (`Hyprland-MonitorRuleManager.cpp:96-107`), not a compositor answer; what the panel renders stays `[UNK]` |

## Block B — Read-only probes row

**Goes after `SKILL.md:225`** (the `mado-geometry.py` probe row; last row of § "Read-only probes (all executed
2026-10-14 unless cited)"), matching that table's three columns `| Probe | Answers | Sample |`:

| `hyprctl monitors all -j \| python3 tools/mado-monitors.py --monitors - --config ~/.config/hypr/monitors.conf` | whether each output runs what its `monitor = NAME, MODE, POSITION, SCALE[, KEY, VALUE]...` rule declares: a read-only join of config bytes and one `monitors all` dump, per output AGREE / DIFFER / DISABLED / UNRULED with the differing fields named; `--selftest` | host run 2026-10-26, one output DP-1 (received `.ufo/waves/round-45/receipts/live-monitors-host-l1.txt`): `MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false`; `MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE`; `MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK`, rc 0, with the dump's `refreshRate` 99.997 against the rule's `@100`; per-verdict licence in § "Monitor rule versus running output" |

## Block C — the prose section

**Goes after `SKILL.md:313`** (last line of § "Rule size versus reported size", immediately before
`### Mutating commands — operator only, mado never runs` at `:314`):

### Monitor rule versus running output

`python3 tools/mado-monitors.py --monitors <dump|-> --config <file>…` joins two caller-supplied read-only inputs: the
`monitor = NAME, MODE, POSITION, SCALE[, KEY, VALUE]...` lines of one or more Hyprland config files, and one
`hyprctl monitors all -j` dump. It starts no process, opens no socket and reads no config tree of its own — the caller runs
`hyprctl monitors all -j | python3 tools/mado-monitors.py --monitors - --config ~/.config/hypr/monitors.conf`. Output: one
`MADO_MON_RULE:` line per rule (numbered in the final list), one `MADO_MON_OUTPUT:` line per dump output, then a
`MADO_MONITORS:` summary; `--selftest` runs built-in fixtures only, reading no file and no host surface
(`mado-monitors.py:455-510`).

Support ceiling. Only the `monitor =` line form is modelled: the tool reads exactly the files named on the command line
(`mado-monitors.py:22`) and its grammar knows only `monitor` and `monitorv2` lines (`:31-33`), so `source` is not followed —
pass every file yourself; a line carrying `##`, `$`, a backslash or an unknown KEY is counted `unsupported` and not guessed; a `monitorv2`
block is counted (`v2=N`) and not parsed; inputs are one dump of at most 1 MiB (`:98`); a `monitors` dump that is not a JSON list
of objects is a SETUP failure, never an empty result.

What the join models, and where the tolerances come from. A rule is stored per selector string: adding one erases every
earlier rule with the same selector and appends the new one (`Hyprland-MonitorRuleManager.cpp:38`, `add` at `:37`), so the
list holds at most one rule per selector. An output takes the newest rule that matches it (reverse walk, `:96-98`), else
the first rule with an empty selector (`:104-105`), else a built-in default (`:108`). A selector matches by exact name, or
as `desc:TEXT` when the description starts with TEXT (`Hyprland-Monitor.cpp:1201-1211`). The handler parses the first four
fields positionally (`Hyprland-legacy-ConfigManager.cpp:1345-1347`); the KEY/VALUE tail accepts only mirror, bitdepth, cm,
sdrsaturation, sdrbrightness, transform, vrr, icc — any other key returns "invalid syntax" and the rule is never added
(`:1351-1379`). The comparison then uses Hyprland's own bounds, never equality:

- `mode` — a rule without `@RATE` keeps `m_refreshRate = 60` (`Hyprland-MonitorRule.hpp:46`); the dump prints the running
  rate with five decimals (`Hyprland-HyprCtl.cpp:242`); a requested mode counts as met within 1 px and 1 Hz
  (`Hyprland-Monitor.cpp:836-837`). The host's 99.997 against `@100` sits inside that bound and reads AGREE.
- `position` — an explicit offset is applied as written (`Hyprland-MonitorPositionController.cpp:27-29`); `auto*` positions are
  computed after, so an auto position has nothing to compare and is not compared.
- `scale` — a written scale whose logical size would be fractional is replaced: start at `round(S*120)/120`
  (`Hyprland-Monitor.cpp:1001-1008`), else one step up then one down for `i = 1..89` (`:1010-1024`); no clean divisor means
  the default scale plus an error overlay (`:1029-1036`), a divisor means the corrected value plus a notification
  (`:1038-1049`). The tool compares against Hyprland's corrected scale, so written ≠ running is the designed behaviour.
- `transform`, `mirror` — `transform` is compared to the rule's value (default 0); `mirrorOf` prints the mirrored output's
  id or `"none"` (`Hyprland-HyprCtl.cpp:267`, `:286`).
- `disabled` — the dump negates enabled (`Hyprland-HyprCtl.cpp:265`).

Per-verdict licence — a verdict reads two printed sides and one source-modelled lookup; it never calls a fault:

| question | verdict/field | what it proves | what it does not |
|---|---|---|---|
| Does the output run the mode, position, scale, transform and mirror its rule declares? | `AGREE`, per output | the rule's fields, read from the file, match the running fields of the dump under Hyprland's own bounds — 1 px and 1 Hz for a requested mode (`Hyprland-Monitor.cpp:836-837`), 1e-4 for scale, exact for position, transform and mirror | that Hyprland picked this rule: the lookup is a source re-implementation (`Hyprland-MonitorRuleManager.cpp:96-107`), not a compositor answer; that the panel renders at those values; that the rule is the only writer |
| Which field disagrees? | `DIFFER` + `differ=<fields>` | that those running fields differ from the rule's — a join, not a blame | a cause or a defect: a runtime `hyprctl keyword monitor` re-enters the same handler (`Hyprland-HyprCtl.cpp:1160`, `:2037`; `Hyprland-legacy-ConfigManager.cpp:606`), an output-management client's committed state overrides the chosen rule's mode, position, transform and scale before it is applied (`Hyprland-MonitorRuleManager.cpp:45-84`), and a mode the output does not offer produces it too |
| Did the output run the rule's `disable`? | `DISABLED` | the rule is disabled and the dump agrees (`Hyprland-HyprCtl.cpp:265` negates enabled) | why it is off — cable, `dpms`, or a rule from a file you did not pass — and anything about rendering |
| Which rule does this output get? | `rule=<n>`, or `UNRULED` | the tool's model of the lookup found, or did not find, a rule in the files given | that the file set is the whole chain: `source` is not followed; and an UNRULED output's fields go unread, it is counted only |
| Is anything unmodelled present that could change which rule applies? | `NOT_COMPARED` (rc 5) | a `monitorv2` block (`Hyprland-legacy-ConfigManager.cpp:567`, `:788-884`) or an `unsupported` line is present, either of which can reorder or replace rules | AGREE, and it also swallows DIFFER: the rc-5 verdict is tested before DIFFER, so a dump whose output differs still exits 5 with `differ=1` (`w1/ScrSkillRows/receipts/v2-differ-precedence.txt`) — read the per-output `differ=` lines, not the top verdict |
| Did any output match at all? | `NO_MATCHING_MONITOR` (rc 3) | `matched=0`: a null observation over the files given | that the host declares no rule, or that a rule works |
| Does the file set carry any monitor line? | `NO_RULES` (rc 4) | `lines=0` and `v2=0` | anything about a `monitorv2`-only or unsupported-grammar file |
| Does a `desc:` selector point at a live output? | rule printed, output unmatched | the dump's `description` is the short form (`Hyprland-HyprCtl.cpp:234`, `:277`) and it did not start with the selector text | a real miss: the long description is not in the dump and Hyprland tests it too (`Hyprland-Monitor.cpp:1206`) — read `make`/`model`/`serial` from the same dump before blaming the selector |

Exit map: 0 `OK` · 1 `DIFFER` (`differ > 0`) · 2 `SETUP` (usage | unreadable | too_large | bad_json) · 3
`NO_MATCHING_MONITOR` (`matched = 0`) · 4 `NO_RULES` (`lines = 0` and `v2 = 0`) · 5 `NOT_COMPARED` (`v2 > 0` or
`unsupported > 0`), tested in that order — NO_RULES, NOT_COMPARED, DIFFER, NO_MATCHING_MONITOR, OK. stderr is empty on
0/1/3/4/5; a setup failure prints exactly one line, `MADO_MONITORS: SETUP <reason>`, and reads no further.

Licence notes.

- **DIFFER is a join, not a blame.** It reads the bytes of the config files you name and one dump; it never asks the compositor
  which rule it chose and never watches a mode set. The rule list it builds is its own model of
  `Hyprland-MonitorRuleManager.cpp:96-107`, so a `rule=<n>` label is `[INF]` and a DIFFER names the field that differs,
  not the writer that set it.
- **Runtime overrides leave no trace in the file or the dump.** `hyprctl keyword monitor` is mutating (never a mado probe)
  and re-enters the same handler that reads the config line (`Hyprland-HyprCtl.cpp:1160`, `:2037`;
  `Hyprland-legacy-ConfigManager.cpp:606`); a wlr-output-management client's committed mode, position, transform or scale
  replaces the chosen rule's field before it is applied (`Hyprland-MonitorRuleManager.cpp:45-84`). Either can make a
  correct file read DIFFER, and neither is visible in `monitors all -j`.
- **`desc:` has a long form the dump cannot show.** Hyprland matches the long or the short description
  (`Hyprland-Monitor.cpp:1206`); the dump prints the short form only (`Hyprland-HyprCtl.cpp:234`, `:277`). A selector
  matching only the long description is reported unmatched here — a limit of the observation, not a dead rule.
- **`monitorv2` is counted, never modelled.** The blocks are registered as their own special category
  (`Hyprland-legacy-ConfigManager.cpp:567`) and parsed by a separate handler (`:788-884`), and they can reorder the same
  selectors, so their presence makes every comparison provisional: the top verdict is NOT_COMPARED (rc 5), which is neither
  AGREE nor DIFFER — the per-output `verdict=` lines still read AGREE / DIFFER / DISABLED / UNRULED, and `differ=` still names
  the fields, but the run's own answer is "not compared".

Host run 2026-10-26, config `~/.config/hypr/monitors.conf:10` = `monitor = DP-1, 3440x1440@100, 0x0, 1`, one output
(receipt `.ufo/waves/round-45/receipts/live-monitors-host-l1.txt`, Hyprland 0.56.2 at `efb50993`):

    $ hyprctl monitors all -j | python3 tools/mado-monitors.py --monitors - --config ~/.config/hypr/monitors.conf
    MADO_MON_RULE: n=1 sel="DP-1" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false
    MADO_MON_OUTPUT: name="DP-1" rule=1 differ=- verdict=AGREE
    MADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK

The 0.003 Hz gap between the rule's `@100` and the dump's 99.997 is inside the 1 Hz bound (`Hyprland-Monitor.cpp:836-837`),
so AGREE is the correct reading and not a rounded match.

Known limits. This host has one output, so the DISABLED, mirror, transform and fractional-scale branches are exercised
only by the tool's `--selftest` fixtures, not by a live run here. A scale correction is compared, not explained: when a
written scale has no clean divisor Hyprland falls back to its default scale and shows an error overlay
(`Hyprland-Monitor.cpp:1029-1036`), and the tool reads that fallback as a field difference. Nothing here says a rule is
in effect for rendering, and no verdict survives a config change: `hyprctl keyword monitor`, an output-management client
or a replug can move every field after the dump was taken.

## Block D — locator receipt (not SKILL text)

| locator | token found there (grep -n) |
|---|---|
| `Hyprland-HyprCtl.cpp:1160` | `dispatchKeyword` |
| `Hyprland-HyprCtl.cpp:2037` | `registerCommand(SHyprCtlCommand{"keyword"` |
| `Hyprland-HyprCtl.cpp:234` | `"description": "{}"` |
| `Hyprland-HyprCtl.cpp:242` | `"refreshRate": {:.5f}` |
| `Hyprland-HyprCtl.cpp:265` | `"disabled": {}` |
| `Hyprland-HyprCtl.cpp:267` | `"mirrorOf": "{}"` |
| `Hyprland-HyprCtl.cpp:277` | `m_shortDescription` |
| `Hyprland-HyprCtl.cpp:286` | `m_mirrorOf` |
| `Hyprland-HyprCtl.cpp:313-321` | `allMonitors` (`monitorsRequest`) |
| `Hyprland-MonitorRuleManager.cpp:37` | `void CMonitorRuleManager::add` |
| `Hyprland-MonitorRuleManager.cpp:38` | `std::erase_if(m_rules` |
| `Hyprland-MonitorRuleManager.cpp:45-84` | `applyWlrOutputConfig` … `m_scale = CONFIG->scale` |
| `Hyprland-MonitorRuleManager.cpp:96-107` | `std::views::reverse` … `r.m_name.empty()` |
| `Hyprland-MonitorRule.hpp:46` | `m_refreshRate   = 60` |
| `Hyprland-Monitor.cpp:1201-1211` | `matchesStaticSelector` |
| `Hyprland-Monitor.cpp:1206` | `m_description.starts_with` / `m_shortDescription.starts_with` |
| `Hyprland-Monitor.cpp:836-837` | `DELTALESSTHAN` (px and Hz) |
| `Hyprland-Monitor.cpp:1001-1008` | `searchScale = std::round(m_scale * 120.0)` … `m_scale = scaleZero` |
| `Hyprland-Monitor.cpp:1010-1024` | `for (size_t i = 1; i < 90; ++i)` |
| `Hyprland-Monitor.cpp:1029-1036` | `failed to find a clean divisor` |
| `Hyprland-Monitor.cpp:1038-1049` | `found suggestion` … `m_scale = searchScale` |
| `Hyprland-legacy-ConfigManager.cpp:606` | `registerHandler(&::handleMonitor, "monitor"` |
| `Hyprland-legacy-ConfigManager.cpp:567` | `addSpecialCategory("monitorv2"` |
| `Hyprland-legacy-ConfigManager.cpp:788-884` | `handleMonitorv2` |
| `Hyprland-legacy-ConfigManager.cpp:1345-1347` | `parser.parseMode` … `parseScale` |
| `Hyprland-legacy-ConfigManager.cpp:1351-1379` | the KEY/VALUE loop (`mirror`, … `icc`) |
| `Hyprland-MonitorPositionController.cpp:27-29` | `m->moveTo(*POS)` … `arranged.push_back(m)` |
| `mado-monitors.py:22` | `It reads files and standard input only` |
| `mado-monitors.py:31-33` | `Config files are read in argument order` … `monitorv2` |
| `mado-monitors.py:81` | `stderr empty on exit 0/1/3/4/5` |
| `mado-monitors.py:98` | `MAX_BYTES = 1048576` |
| `mado-monitors.py:455-510` | `def selftest` … `MADO_MONITORS_SELFTEST: %d/%d passed` |
| `~/.config/hypr/monitors.conf:10` | `monitor = DP-1, 3440x1440@100, 0x0, 1` |
