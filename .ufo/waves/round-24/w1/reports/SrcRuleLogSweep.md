# SrcRuleLogSweep — round 24, wave 1 C1 recon: rule/matcher/effect logging

## Scope and outcome

Swept the pinned Hyprland v0.56.2 sources under `src/desktop/rule` and `src/config` for every log call
(`Log::`, `Debug::log`, logging macros) and classified each hit: does it name a rule, its match, or its effect,
and would it tell a reader **which rule produced an applied effect**. Findings only — this seat wrote no
SOURCES rows, no C1 claim rows, and did not touch the knowledge note.

Outcome in one line: **the rule directory contains 15 log calls in 6 files and none of them names a rule; the
rule-matching and rule-application loops in both applicators and in `Engine.cpp` contain no logging at all; the
only log messages in the pinned tree that carry rule content are workspace-rule (`ConfigManager.cpp:1760`),
monitor-rule (`MonitorRuleManager.cpp:51-172`) and merged-static-state (`Window.cpp:2167,2187`) messages — none
of which identifies which window or layer rule produced an applied effect.** Full detail, commands and counts
below.

## Method and identity

- Local clone (read-only use): `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`.
- Clone identity: `git log -1 --format='%H %s'` printed
  `efb50993780079460b0cbed1363e2166a2de1d9f [gha] Nix: update inputs`, i.e. tag `v0.56.2`.
- Every file cited below was re-fetched byte-for-byte from
  `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/<path>` into
  receipts `SrcRuleLogSweep-1.bin` … `SrcRuleLogSweep-17.bin` in `.ufo/waves/round-24/fetch/w1/`, and each
  receipt was `cmp`-compared against the clone copy: **all 17 identical**. So the line numbers and texts below
  are the pinned bytes, not a local edit.
- Cross-check: receipt 3 (`WindowRule.cpp`, `sha256:7034c332…`, 19588 B) matches the sha256 recorded independently
  by the sibling report `w1/reports/SrcWindowRule.md` for the same path and commit.

Receipt legend (path, sha256, bytes):

| # | path | sha256 | bytes |
|---|---|---|---|
| 1 | src/desktop/rule/Engine.cpp | sha256:1ecb7afa34b341d21984e5c21a35d5901bc43cf0f0fab0db6605ad8596addde6 | 1478 |
| 2 | src/desktop/rule/Rule.cpp | sha256:257687efd814cb714024c14e2952adb26e1e7a1f5907d20aa6aaea1e4c098e2e | 6835 |
| 3 | src/desktop/rule/windowRule/WindowRule.cpp | sha256:7034c3325fee476cb501266af67999534ca36cf2841d83c9940db96d116d1f78 | 19588 |
| 4 | src/desktop/rule/windowRule/WindowRuleApplicator.cpp | sha256:fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b | 27092 |
| 5 | src/desktop/rule/layerRule/LayerRule.cpp | sha256:f3e05eafeed061471fee843842db18127b905d2847faa738e763f4355f3c9bca | 3948 |
| 6 | src/desktop/rule/layerRule/LayerRuleApplicator.cpp | sha256:9321999ac030e8da73abab53f6a0d6f0cf82ddc3c8c63befa845ade8716568ba | 6193 |
| 7 | src/desktop/rule/matchEngine/IntMatchEngine.cpp | sha256:f832b4380766dada25cfadba6f9ef5eead905608d4f772a635051c75c9985bb8 | 368 |
| 8 | src/config/shared/monitor/MonitorRuleManager.cpp | sha256:17d46685c2623657f52e71b22a033c0a798cf3903f7bbeb64ceebce87527f016 | 10962 |
| 9 | src/config/legacy/ConfigManager.cpp | sha256:9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b | 90963 |
| 10 | src/config/supplementary/executor/Executor.cpp | sha256:65eed6c2acb5e21bea6e95bd6f6fc9c6ea3896773795eb0e5ee75923467cc09d | 7395 |
| 11 | src/debug/log/Logger.hpp | sha256:aeb07ba1ba1fd5cfdb75aaf7434910c887096c24952f1a6788f71a4d7dbe78fe | 1767 |
| 12 | src/debug/log/Logger.cpp | sha256:d04e3a2fe5c73ad8684377856ce8301e493929ed9f391e405fde4975eaf6b868 | 1789 |
| 13 | src/helpers/env/Env.cpp | sha256:2976c823023e4a6147946d8678d8fa91963a8f3b585b4d9c9eb9d67760597b16 | 285 |
| 14 | src/desktop/view/Window.cpp | sha256:d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded | 124226 |
| 15 | src/debug/HyprCtl.cpp | sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa | 97582 |
| 16 | src/config/shared/actions/ConfigActions.cpp | sha256:a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637 | 71407 |
| 17 | src/output/Monitor.cpp | sha256:9cf88e154eb5dae676c79d37b5b055ca6134838857cecdbb89a3b747a6821927 | 112738 |

Receipts 11–17 support the gating and error-path findings and are outside the two assigned directories; they are
fetched because the report makes claims about them (trace gate, `hyprctl` keyword path, `getprop`, adjacent
callers).

## Exact sweep commands and counts

Run in `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2` (bytes identical to the pinned receipts):

```sh
# 1. all log-ish tokens in the two assigned directories
grep -rnE 'Log::|Debug::log|Log::logger|LOG\(|RASSERT|ASSERT' src/desktop/rule src/config | wc -l
# -> 119

# 2. per-token counts (fixed-string, so no regex escape effects)
for t in 'Debug::log' 'Log::logger' 'Log::' 'LOG(' 'LOGM(' 'RASSERT' 'ASSERT' 'std::println' 'fprintf' 'printf'; do
  printf '%-14s rule=%s config=%s\n' "$t" "$(grep -rF -- "$t" src/desktop/rule | wc -l)" "$(grep -rF -- "$t" src/config | wc -l)"
done
# Debug::log     rule=0 config=0
# Log::logger    rule=15 config=87
# Log::          rule=15 config=93
# LOG(           rule=0 config=0
# LOGM(          rule=0 config=0
# RASSERT        rule=0 config=11
# ASSERT         rule=0 config=11
# std::println   rule=0 config=0
# fprintf        rule=0 config=0
# printf         rule=0 config=1     <- snprintf in Monitor Parser.cpp:87, not a log

# 3. the 15 rule-directory call sites, sorted
grep -rnE 'Log::logger->log' src/desktop/rule/ | sort -t: -k1,1 -k2,2n
# -> 15 lines (table below)

# 4. per-file counts in the rule directory
grep -rcE 'Log::logger->log' src/desktop/rule/*.cpp src/desktop/rule/*/*.cpp
# WindowRuleApplicator.cpp:9  LayerRuleApplicator.cpp:2  Rule.cpp:1  LayerRule.cpp:1
# WindowRule.cpp:1  IntMatchEngine.cpp:1  (all other files: 0)

# 5. per-file counts in the config directory
grep -rc 'Log::logger->log' src/config/ | grep -v ':0$'
# ConfigManager.cpp:9  legacy/ConfigManager.cpp:24  lua/ConfigManager.cpp:6  lua/LuaEventHandler.cpp:4
# shared/actions/ConfigActions.cpp:4  shared/inotify/ConfigWatcher.cpp:4  shared/monitor/MonitorRuleManager.cpp:15
# shared/monitor/Parser.cpp:5  supplementary/executor/Executor.cpp:5  + 11 single-hit files
# TOTAL 87 occurrences across 20 files
```

Level split of the 15 rule-directory calls: **5 TRACE, 10 ERR, 0 DEBUG, 0 INFO**. Only 3 of the 15 message
literals contain the word `rule` at all:

```sh
grep -rhE 'Log::logger->log' src/desktop/rule | grep -oE '"[^"]+"' | grep -cE 'rule'   # -> 3
# "BUG THIS: IRule: RULE_ENGINES does not contain rule idx {}"
# "maxsize rule \"...  (the literal is "maxsize rule \"{}\" failed with: {}")
# "minsize rule \"...
```

(The naive count `grep -rnE 'Log::logger->log' src/desktop/rule | grep -ic rule` prints 15, but that matches the
**path** `src/desktop/rule/` on every line; it is not evidence about message text.)

## The 15 sites in `src/desktop/rule` — verbatim line and verdict

"Which rule?" = would this line, on its own, tell a reader **which** rule (by name, match pattern, or effect
pairing) produced an applied effect.

| path:line | lvl | exact line (byte-exact from receipt) | what it carries | which rule? |
|---|---|---|---|---|
| Rule.cpp:93 | ERR | `Log::logger->log(Log::ERR, "BUG THIS: IRule: RULE_ENGINES does not contain rule idx {}", sc<std::underlying_type_t<eRuleProperty>>(p));` | integer index of a rule *property*, at `registerMatch` time | **No** — "rule idx" is a property enum index, not a rule identity; no rule name, no match string |
| windowRule/WindowRule.cpp:383 | TRACE | `Log::logger->log(Log::TRACE, "CWindowRule::matches: skipping prop entry {}", sc<std::underlying_type_t<eRuleProperty>>(prop));` | property enum int for an unhandled prop inside the matcher | **No** — printed only when a prop is *unhandled*, not on match success/failure; no rule name |
| windowRule/WindowRuleApplicator.cpp:92 | TRACE | `Log::logger->log(Log::TRACE, "CWindowRuleApplicator::applyDynamicRule: Skipping effect {}, not dynamic", sc<std::underlying_type_t<eWindowRuleEffect>>(key));` | effect enum int being skipped | **No** — skip path only, no rule name |
| windowRule/WindowRuleApplicator.cpp:114 | ERR | `Log::logger->log(Log::ERR, "CWindowRuleApplicator::applyDynamicRule: BUG THIS: WINDOW_RULE_EFFECT_NONE??");` | constant | **No** |
| windowRule/WindowRuleApplicator.cpp:180 | ERR | `Log::logger->log(Log::ERR, "failed to parse {} as an expression", expr.toString());` | the failing maxsize expression text | **No** — during application, so a reader learns *some* rule's maxsize expression failed, never which rule |
| windowRule/WindowRuleApplicator.cpp:184 | ERR | `Log::logger->log(Log::ERR, "Invalid size for maxsize");` | constant | **No** |
| windowRule/WindowRuleApplicator.cpp:192 | ERR | `} catch (std::exception& e) { Log::logger->log(Log::ERR, "maxsize rule \"{}\" failed with: {}", std::get<Math::SExpressionVec2>(value).toString(), e.what()); }` | expression + exception text | **No** — names the *effect kind* only |
| windowRule/WindowRuleApplicator.cpp:209 | ERR | `Log::logger->log(Log::ERR, "failed to parse {} as an expression", expr.toString());` | failing minsize expression text | **No** |
| windowRule/WindowRuleApplicator.cpp:214 | ERR | `Log::logger->log(Log::ERR, "Invalid size for maxsize");` | constant | **No**, and it **misnames the effect**: this line sits in the `WINDOW_RULE_EFFECT_MIN_SIZE` branch (:196-221), so a minsize failure is logged as `maxsize` |
| windowRule/WindowRuleApplicator.cpp:221 | ERR | `} catch (std::exception& e) { Log::logger->log(Log::ERR, "minsize rule \"{}\" failed with: {}", std::get<Math::SExpressionVec2>(value).toString(), e.what()); }` | expression + exception text | **No** |
| windowRule/WindowRuleApplicator.cpp:385 | TRACE | `Log::logger->log(Log::TRACE, "CWindowRuleApplicator::applyStaticRule: Skipping effect {}, not static", sc<std::underlying_type_t<eWindowRuleEffect>>(key));` | effect enum int being skipped | **No** — skip path only |
| layerRule/LayerRule.cpp:103 | TRACE | `Log::logger->log(Log::TRACE, "CLayerRule::matches: skipping prop entry {}", sc<std::underlying_type_t<eRuleProperty>>(prop));` | property enum int for an unhandled prop | **No** |
| layerRule/LayerRuleApplicator.cpp:49 | TRACE | `Log::logger->log(Log::TRACE, "CLayerRuleApplicator::applyDynamicRule: Skipping effect {}, not dynamic", sc<std::underlying_type_t<eLayerRuleEffect>>(key));` | effect enum int being skipped | **No** |
| layerRule/LayerRuleApplicator.cpp:70 | ERR | `Log::logger->log(Log::ERR, "CLayerRuleApplicator::applyDynamicRule: BUG THIS: LAYER_RULE_EFFECT_NONE??");` | constant | **No** |
| matchEngine/IntMatchEngine.cpp:9 | ERR | `} catch (...) { Log::logger->log(Log::ERR, "CIntMatchEngine: invalid input {}", s); }` | the raw match string that failed integer conversion, at matcher construction | **No** — best of the 15: it carries a *match value*, but neither the rule nor which property the value belonged to |

Aggregate: **0 of 15 identify a rule.** 5 are TRACE (invisible unless `HYPRLAND_TRACE` is set, see below).
The other 10 are all `Log::ERR`, and every one of those fires on a *failure* path (unmappable property at
registration, unexpected effect enum, unparsable expression, invalid size) — none on a success path.

## Config-directory sites that mention a rule

The config sweep produced 87 `Log::logger->log` occurrences; only these touch a rule concept, and none is a
window/layer rule attribution:

| path:line | lvl | exact line | which rule? |
|---|---|---|---|
| shared/monitor/MonitorRuleManager.cpp:51 | DEBUG | `Log::logger->log(Log::DEBUG, "CConfigManager::getMonitorRuleFor: found a wlr_output_manager override for {}", PMONITOR->m_name);` | names the **monitor**, not the rule |
| :53, :57, :64, :69, :74, :79 | DEBUG | `" > overriding enabled/mode/offset/transform/scale/vrr: {} -> {}"` (one line each; :57 wraps to the next line) | field-level before/after of the synthesized monitor rule, no rule identity |
| :101 | WARN | `Log::logger->log(Log::WARN, "No rule found for {}, trying to use the first.", PMONITOR->m_name);` | negative: says *no* rule matched |
| :108 | WARN | `Log::logger->log(Log::WARN, "No rules configured. Using the default hardcoded one.");` | negative |
| :172 | ERR | `Log::logger->log(Log::ERR, "[MonitorRuleManager] failed to apply rule to {}!", m->m_name);` | names the **monitor**, not the rule |
| legacy/ConfigManager.cpp:1760 | ERR | `Log::logger->log(Log::ERR, "Invalid workspace rule found: {}", rule);` | prints the offending **workspace-rule text**: the only rule-parse log that carries rule content, and it is workspace rules |
| supplementary/executor/Executor.cpp:71 | DEBUG | `Log::logger->log(Log::DEBUG, "Applied rule arguments for exec, pid {}.", pid);` | names the **pid**, not the rule |
| supplementary/executor/Executor.cpp:121 | ERR | `Log::logger->log(Log::ERR, "Failed to parse exec rule: {}", builtRule.error());` | error text of an exec rule |

The other monitor-rule lines in that file (`:222, :241, :246, :255, :279`) are VRR/output messages. Nothing in
`src/config` logs a window or layer rule's name, its `match:` properties, or the effect a window/layer rule set.

## The matching and application loops are silent

This is the structural reason the 15 lines cannot answer "which rule applied". Counted directly over the
pinned bytes:

```sh
sed -n '483,590p' src/desktop/rule/windowRule/WindowRuleApplicator.cpp | grep -c 'Log::'   # -> 0  (all three loops)
sed -n '127,153p' src/desktop/rule/layerRule/LayerRuleApplicator.cpp | grep -c 'Log::'     # -> 0
grep -c 'Log::\|Debug::log' src/desktop/rule/Engine.cpp                                    # -> 0  (file is 56 lines)
sed -n '893,917p' src/config/legacy/ConfigManager.cpp | grep -c 'Log::'                    # -> 0  (addRuleFromConfigKey)
sed -n '946,976p' src/config/legacy/ConfigManager.cpp | grep -c 'Log::'                    # -> 0  (reloadRules)
```

- `CWindowRuleApplicator::readStaticRules` (WindowRuleApplicator.cpp:483-524), `recheckStaticRules` (:526-545) and
  `propertiesChanged` (:547-590) each iterate `ruleEngine()->rules()`, call `wr->matches(...)`, then
  `applyStaticRule(wr)` / `applyDynamicRule(wr)`. There is no log statement between the loop head and the tail;
  the only logs reachable from inside are the effect-level skips/errors listed above.
- `CLayerRuleApplicator::propertiesChanged` (LayerRuleApplicator.cpp:127-153) is the same shape with no log.
- `CRuleEngine` (`Engine.cpp`, 56 lines) has no logging at all: `registerRule`, `unregisterRule`, `updateAllRules`,
  `clearAllRules` are silent.
- `CConfigManager::addRuleFromConfigKey` (:893-917) and `addLayerRuleFromConfigKey` (:919-944) build the rule
  and only return error strings; `reloadRules` (:946-976) collects them into a `Hyprlang::CParseResult`; no log.

## TRACE gating: 5 of the 15 are off by default

- `src/debug/log/Logger.hpp:24-27`: the variadic `log()` returns early `if (level == Hyprutils::CLI::LOG_TRACE && !m_isTrace)`;
  `m_isTrace` defaults to `false` (`Logger.hpp:43`); `TRACE` is aliased at `Logger.hpp:54`.
- `src/debug/log/Logger.cpp:10-11`: `CLogger::CLogger() : m_isTrace(Env::isTrace())` then sets the underlying
  logger level to `LOG_TRACE` or `LOG_DEBUG`.
- `src/helpers/env/Env.cpp:10-12`: `bool Env::isTrace() { static bool TRACE = envEnabled("HYPRLAND_TRACE"); return TRACE; }`.

So the three "skipping prop entry" / "Skipping effect … not dynamic|not static" sites are only reachable in a
`HYPRLAND_TRACE` session, and even then carry enum integers, not rule identity. Those five calls are the *only*
`Log::TRACE` statements in `src/desktop/rule` (`grep -rc 'Log::TRACE' src/desktop/rule/` sums to 5) and
`src/config` contains none, so trace mode adds nothing about rule attribution anywhere in the assigned scope.

## Where rule parse errors go instead of a log

Observed at the pinned bytes:

- `CConfigManager::reload()` (legacy/ConfigManager.cpp:726-750) computes
  `const auto ruleError = reloadRules();` at :748 and then calls
  `postConfigReload(ERR.error || !monitorError.error ? ERR : monitorError);` at :750 — `ruleError` is **never
  read**. A rule-construction error therefore neither logs nor reaches the error object handed on.
- `src/debug/HyprCtl.cpp:1238` and `:1241` call `mgr->reloadRules();` as discarded-value statements (triggered by
  `keyword` on `windowrule`/`layerrule`).
- The deprecated one-line syntax path `CConfigManager::handleWindowrule` (legacy/ConfigManager.cpp:2016-2055)
  returns `std::format("invalid field …")` style strings and never logs them; the same is true for
  `handleLayerrule` (:2057-2095). Those strings are returned to `parseKeyword`'s caller, i.e. the `hyprctl`
  client — a surface outside the log.
- `hyprctl getprop` (`src/debug/HyprCtl.cpp:2032`; implementation `dispatchGetProp`, :1463-1647) reports
  *values* pulled from `m_ruleApplicator` (`minSize`, `maxSize`, `alpha`, border colours, animation style).
  Nothing in that function reports which rule produced a value.

## Negative claims, with the sweep that produced them

- **N1 — no log line in `src/desktop/rule` prints a rule name or match string.**
  `grep -rnE 'Log::logger->log' src/desktop/rule/ | grep -E 'name\(\)|->name|m_name'` → no output, exit 1.
  Same filter over `src/config/` yields only monitor/pid references (table above), no `rule->name`.
- **N2 — no attribution wording anywhere in the two directories.**
  `grep -rniE 'which rule|rule that|applied by|matched rule|rule name' src/desktop/rule src/config | wc -l` → `0`.
- **N3 — the old logging API and macros are absent from the rule directory.**
  Fixed-string counts: `Debug::log` 0, `LOG(` 0, `LOGM(` 0, `RASSERT` 0, `ASSERT` 0 (command in §Exact sweep).
- **N4 — `Engine.cpp` has no logging.** `grep -c 'Log::\|Debug::log' src/desktop/rule/Engine.cpp` → `0`; file is 56 lines.
- **N5 — no logging inside the window/layer matcher loops.** Range counts in §The matching and application loops
  are silent: all three ranges print `0`.

These are sweeps of the pinned tree only. They do not constrain code outside `src/desktop/rule` and `src/config`
beyond the specific adjacent files I fetched (receipts 14-17).

## Adjacent hits outside the assigned directories (flagged, not part of the sweep verdict)

Found while checking whether any caller logs an applied rule. They are the only lines in the fetched set that
say a rule "matched" or was "applied", and they still do not name a rule:

| path:line | lvl | exact line | reading |
|---|---|---|---|
| src/desktop/view/Window.cpp:2167 | DEBUG | `Log::logger->log(Log::DEBUG, "Rule monitor, applying to {:mw}", m_self.lock());` | prints only the window pointer; the monitor it was assigned came from the merged `static_` field, not from a named rule |
| src/desktop/view/Window.cpp:2170 | ERR | `Log::logger->log(Log::ERR, "No monitor in monitor {} rule", MONITORSTR);` | prints the monitor selector string of a monitor rule, no rule identity |
| src/desktop/view/Window.cpp:2187 | DEBUG | `Log::logger->log(Log::DEBUG, "Rule workspace matched by {}, {} applied.", m_self.lock(), m_ruleApplicator->static_.workspace);` | window pointer + the merged static workspace value, logged unconditionally once `static_.workspace` is non-empty |
| src/desktop/view/Window.cpp:2218 and :2263 | ERR | "Error while parsing suppressevent windowrule: unknown event type {}" and "windowrule group does not support {} always" (text shown de-quoted) | parse-time complaints about effect payloads, no rule identity |
| src/output/Monitor.cpp:723 | DEBUG | `Log::logger->log(Log::DEBUG, "Applying monitor rule for {}", m_name);` | monitor name |

Even the two "matched/applied" lines print the *merged applicator state*, not the rule that contributed it.
Multiple matching rules write the same fields (`m_dynamicTags`, `m_maxSize`, `m_alpha`, …) with no per-rule
provenance retained, so no log line could reconstruct the contributing rule without extra bookkeeping.

## Observation vs inference vs unknown

**Observed (pinned bytes; receipts 1-17, all `cmp`-identical to the clone):**
the 15 rule-directory log sites and their exact texts; 0 DEBUG/0 INFO among them; 5 TRACE gated on
`HYPRLAND_TRACE`; 0 lines carrying a rule name; the three matcher/applicator loops and `Engine.cpp` with zero
logging; `reload()` discarding `ruleError`; `HyprCtl` discarding `reloadRules()` results; `getprop` reading
applicator values only, with no rule field; `handleWindowrule`/`handleLayerrule` returning error strings instead
of logging them.

**Inference ([INFERENCE]):**
- Because rule effects are stored as merged overridable values keyed by `Types::PRIORITY_WINDOW_RULE` with no
  back-pointer to the rule, a reader of the current log cannot recover rule attribution for an applied effect
  even by correlating the existing skipped/error lines — the applying rule object is not printed anywhere.
- A `HYPRLAND_TRACE` session would add per-effect "skipped, not dynamic/static" noise but still no attribution,
  so raising the log level does not answer the frontier question.

**What these bytes do NOT establish:**
- Host behaviour: what the host's installed 0.56.2 binary actually writes at runtime, at which log level, and
  whether any plugin or packaging patch adds attribution — **[UNK]**, not tested here (read-only host, no
  `HYPRLAND_TRACE` session run).
- Whether `hyprlang` itself independently prints a parse error for a bad `keyword windowrule …` line — the
  hyprlang dependency is outside the pinned tree fetched here; the observed discard of `ruleError` bounds only
  Hyprland's own handling.
- Whether `hyprctl clients`/`layers` JSON exposes any rule provenance — not inspected in this sweep.
- No claim is made that adding logging is possible without cost, and no claim about runtime overhead.

## Verdict

`SURFACED`: 15 log calls in `src/desktop/rule` (6 files) and 87 in `src/config` (20 files); **none tells a reader
which window/layer rule produced an applied effect** — 0 of 15 name a rule, 5 of 15 are `HYPRLAND_TRACE`-gated,
10 of 15 fire only on failure paths, and the matching/application loops plus `Engine.cpp` contain no logging at
all. The only rule-content logs in the pinned tree are workspace-rule (`ConfigManager.cpp:1760`) and
monitor-rule (`MonitorRuleManager.cpp:51-172`) messages plus the merged-state lines in `Window.cpp:2167,2187`.
Host runtime behaviour remains [UNK].

No tool was installed or updated; no package, display, compositor or home-directory state was touched; no
git/jj write was issued in the lane or the fleet repo. Files created: this report and the 17 receipts under
`.ufo/waves/round-24/fetch/w1/`.
