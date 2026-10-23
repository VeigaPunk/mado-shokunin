# AtkLogChannel — round 24 wave 2 attack: the note's log claim

## What I attacked

One sentence, `corpus/knowledge/rule-attribution-r24.md:25` (Answer table, `logs` row):

> `| logs | none name a rule; the one matched-by log line is the workspace-rule path (A18) | — | window/layer rule identity |`

Two testable propositions, attacked against the whole pinned tree (not only `src/desktop/rule/`):

- **P1** — no log names a window or layer rule (prints its name, an index that identifies it, or its match
  string).
- **P2** — the one matched-by log line is the workspace-rule path; i.e. window rules leave no rule-application
  log.

The assignment's operational criterion for P1: "log lines that print a rule name, rule index or match string
for window or layer rules", including Window.cpp lines that say a rule matched.

## Pin check (bytes are the pinned commit, not a local edit)

Clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`, `git log -1` = `efb50993780079460b0cbed1363e2166a2de1d9f`
(`[gha] Nix: update inputs`), i.e. tag v0.56.2. `sha256sum` of the four files I cite equals the sha256 recorded
in the lane's own SOURCES rows:

| file | sha256 | SOURCES row |
|---|---|---|
| `src/desktop/view/Window.cpp` | `sha256:d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded` | S164 |
| `src/desktop/rule/windowRule/WindowRuleApplicator.cpp` | `sha256:fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b` | S155 |
| `src/desktop/rule/windowRule/WindowRuleApplicator.hpp` | `sha256:334e1254a66e2df8ef243544e3ff99db398ed5ec6e48996d496d05ff7bf50f44` | S156 |
| `src/debug/HyprCtl.cpp` | `sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` | S158 |

## Method

1. Whole-`src/` sweep, not just `src/desktop/rule/`: every file under `src/` (`*.cpp`, `*.hpp`, `*.h`), regex
   `Log::logger->log\((.*?)\);` with DOTALL, bodies filtered on `rule` (case-insensitive). Hit count: **59** call
   sites in the whole tree, of which the rule-directory ones are exactly the 15 the note's sweep names.
2. Distinct rule-bearing message literals: `grep -rhoE 'Log::logger->log\(Log::[A-Z]+, "[^"]*"' src/ | grep -i rule
   | sort -u | wc -l` → 37 literals, enumerated below by kind. Plus checks for alternate print paths
   (`Debug::log`, `LOG(`, `std::println`, `fprintf`/`printf`): none carries rule content (`std::println` hits are
   startup/bail-out text only).
3. Targeted greps: `grep -rn 'matched by' src/` → exactly `src/desktop/view/Window.cpp:2187` plus an unrelated
   comment in `src/xwayland/Server.cpp:65`. `→name()` / `.name()` passed to a log: 6 hits, none a rule object.
4. Manual read of the rule application paths: `CWindow::mapWindow`, `CWindow::updateWindowData`,
   `CWindowRuleApplicator::applyStaticRule`, `CLayerRuleApplicator`, `CRuleEngine`, legacy `handleWindowrule`,
   `dispatchKeyword`.

Result classes:

| kind of rule log | where | identity printed? |
|---|---|---|
| monitor rule | `MonitorRuleManager.cpp:51-172`, `Monitor.cpp:222,723,966`, `Window.cpp:2167,2170` | no |
| workspace rule (`workspace =`) | `ConfigManager.cpp:1760` (invalid-rule error), `WorkspacePlacementController.cpp:76-105` | no; the manager logs nothing (`grep -c 'Log::' src/config/shared/workspace/WorkspaceRuleManager.cpp` → 0) |
| window/layer rule | 15 sites under `src/desktop/rule/` + `Window.cpp:2187,2218,2263,2405` + `DefaultFloatingAlgorithm.cpp:58,71` | no rule name/index; enum ints on skip/BUG paths, or effect text on parse errors |
| exec rule, permission rule, xkb "rules" | unrelated | n/a |

## Findings

### F1 — P2 is false: the matched-by line is the **window-rule** path, not the workspace-rule path

False on the path as well as on the count. The evidence chain:

- `Window.cpp:2187` fires inside `if (!m_ruleApplicator->static_.workspace.empty())` (`:2174`) and prints
  `m_ruleApplicator->static_.workspace`.
- Both log lines sit in the `setStaticProps` lambda (`:2143`) of `void CWindow::mapWindow()` (`:2052`; it is the
  only `CWindow::` definition head between 2052 and 2143), invoked at `:2278`/`:2281`.
- `static_.workspace` is written from a rule effect in exactly one place in the tree —
  `src/desktop/rule/windowRule/WindowRuleApplicator.cpp:443`, `case WINDOW_RULE_EFFECT_WORKSPACE` (the only other
  write is the whole-struct `static_ = {}` reset in `readStaticRules`); `static_.monitor`
  at `:439`, `case WINDOW_RULE_EFFECT_MONITOR`. Both are **window-rule effects**: `"monitor"` and `"workspace"`
  are registered in `WindowRuleEffectContainer.cpp:23-24`, and `handleWindowrule` (`ConfigManager.cpp:2016`)
  parses them out of a `windowrule` value.
- The config `workspace =` path is a different type applied elsewhere: `CWindow::updateWindowData(const
  Config::CWorkspaceRule&)` (`:1123-1135`) applies border/decorate/rounding/shadow with
  `PRIORITY_WORKSPACE_RULE` and contains **no log call**; `CWorkspaceRuleManager` logs nothing.

So `"Rule workspace matched by {}, {} applied."` is a **window-rule application log** (the effect named
`workspace`, applied to a window). The note's sentence inverts the categories: it tells a reader that the sole
match log belongs to workspace rules and that window rules are silent, when the cited line is precisely a window
rule matching and applying.

### F2 — "the one" undercounts: there are two window-rule application lines

`Window.cpp:2167` logs `"Rule monitor, applying to {:mw}"` when a window-rule `monitor` effect applies, in the
same lambda. Neither line names the rule, but both announce that *a window rule applied* to a named window. The
singular "the one matched-by log line" survives only as a literal-string observation (`matched by` occurs once
tree-wide); as a statement about rule-application logging it is false.

### F3 — P1 fails under the assignment's own criterion: a log prints a window/layer rule's match string

`src/debug/HyprCtl.cpp:1252`, inside `dispatchKeyword` (`:1160`):

```cpp
Log::logger->log(Log::DEBUG, "Hyprctl: keyword {} : {}", COMMAND, VALUE);
```

`COMMAND`/`VALUE` are the two tokens of the `hyprctl keyword` request (`:1176-1182`). `windowrule` and
`layerrule` are registered config handlers (`ConfigManager.cpp:610-611`), and `CConfigManager::handleWindowrule`
(`:2016`) / `handleLayerrule` (`:2057`) parse `VALUE` as the rule body — match props and effects. A dynamic
`hyprctl keyword windowrule 'opacity 0.8, match:class:kitty'` therefore logs the rule's own text, match string
included; named forms are special-cased by HyprCtl itself (`:1237-1240` test `COMMAND.contains("windowrule[")` /
`"layerrule["`), so the logged COMMAND can carry a rule key. [INFERENCE] on the exact named-key spelling; the
inline match-string case is grounded in the bytes above.

This is a **declaration-time** echo, not an attribution channel: it contains no window/layer and no match event,
and it fires only when the user applies the keyword dynamically. It does not overturn the note's thesis. It does
break the literal universal "none name a rule" — a log line outside `src/desktop/rule/` can print a window or
layer rule's match string.

### F4 — What holds

- No log pairs a rule **identity** with an applied effect on a window or layer. The 15 rule-dir calls carry
  property/effect enum ints on skip or BUG paths, or effect text on parse errors; `Rule.cpp:93`'s "rule idx {}"
  prints an `eRuleProperty` enum index, not a rule id; 5 of the 15 are TRACE-gated (`HYPRLAND_TRACE`,
  `src/helpers/env/Env.cpp:11`), matching the note's count exactly. `LayerSurface.cpp` has no rule log at all.
  `hyprctl`/Lua/socket2 attribution remains absent.
- So the note's headline ("No upstream channel maps an applied property back to the rule that set it") is not
  harmed; and A18's counted row is verbatim-true and still passes the frozen C1 predicate. This is a prose
  defect in a non-counted table, not a counted-row failure.

## Verdict

- "no log names a window/layer rule" — **holds in the attribution sense; fails as written** (match-string echo at
  `HyprCtl.cpp:1252`; and two Window.cpp lines log that a *window* rule applied).
- "the one matched-by log line is the workspace-rule path" — **fails**: it is the window-rule static effect path,
  and it is not the only rule-application line.

VERDICT: partial

## Impacted axes

- **C1 coverage** (the note is the deliverable): counted predicate unaffected — A18 passes, `PASS_ROW` unchanged.
  The answer table (non-counted prose) carries a false statement about the tree.
- C2 calibration, `tools/`, SOURCES: untouched by this finding.

## Smallest safe correction

Rewrite one cell (note line 25) and add one clause to the Logs sweep bullet; no counted row, SOURCES cell, or
counter changes:

```
| logs | no log identifies a window or layer rule; two `CWindow::mapWindow` DEBUG lines report a window-rule
`monitor`/`workspace` effect being applied (`:2167`, `:2187`, no rule name), and `hyprctl keyword` echoes the
text of a dynamically applied `windowrule`/`layerrule` (`HyprCtl.cpp:1252`) | — | window/layer rule identity |
```

and, in the "Logs" sweep bullet, one sentence: *the two rule-application lines are window-rule static effects,
not the config `workspace =` path (which logs nothing)*.

Cross-check for the integrator: `.ufo/waves/round-24/w2/reports/ReopenS164.md:78` proposes a replacement that
repeats the mislabel ("emitted on the workspace-rule path"); that wording should not be adopted.

## Reproduce

Run in `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2` (all read-only):

```sh
grep -rn 'matched by' src/                                        # -> Window.cpp:2187 only (log)
awk 'NR<2145 && /^[A-Za-z_].*CWindow::/ {last=NR": "$0} END{print last}' src/desktop/view/Window.cpp
                                                                  # -> 2052: void CWindow::mapWindow() {
grep -rn 'static_.workspace\|static_.monitor' src/                # -> WindowRuleApplicator.cpp:439,443 ; Window.cpp:2144-2187
grep -rn 'WINDOW_RULE_EFFECT_WORKSPACE\|WINDOW_RULE_EFFECT_MONITOR' src/desktop/rule/windowRule/WindowRuleApplicator.cpp
grep -n 'Hyprctl: keyword' src/debug/HyprCtl.cpp                  # -> 1252
grep -n 'registerHandler(&::handleWindowrule\|registerHandler(&::handleLayerrule' src/config/legacy/ConfigManager.cpp
grep -rn 'Log::logger->log' src/desktop/rule | wc -l               # -> 15
grep -c 'Log::' src/config/shared/workspace/WorkspaceRuleManager.cpp  # -> 0
```

No install or update was performed; no host verb, compositor action, or lane write occurred beyond this report.
Every `Report:` path above is relative to the lane root.

Report: .ufo/waves/round-24/w2/reports/AtkLogChannel.md
