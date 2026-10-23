# ReopenRuleManager — re-open of SrcWsRuleCode.md

Re-open target: `.ufo/waves/round-27/w1/reports/SrcWsRuleCode.md` (source-row report S178 proposal + S162 used-by extension).
Re-fetched both raw URLs with curl into `/fast/scratch/hyaku/mado-r27/reopen/`, compared sha256 and byte count against
the w1 report's rows, and re-located every quote by whitespace-collapsed substring test (python3 stdlib). No source
file edited; no counter/harness run; no Hyprland process started.

## Fetch fidelity

| Row | URL | Report sha256 | Fetched sha256 | Report bytes | Fetched bytes |
|---|---|---|---|---|---|
| S178 (proposed) | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/workspace/WorkspaceRuleManager.cpp` | `06e8dcbaea83e51710bd372a8f264ad3d07bbe061b9720bbe456811451c02d10` | `06e8dcbaea83e51710bd372a8f264ad3d07bbe061b9720bbe456811451c02d10` | 2672 | 2672 |
| S162 (existing, used-by ext.) | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp` | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` | 90963 | 90963 |

`file` identifies both as `C source, ASCII text`. Fetched bytes stored at
`/fast/scratch/hyaku/mado-r27/reopen/ReopenRuleManager.bin` (S178) and
`/fast/scratch/hyaku/mado-r27/reopen/ReopenRuleManager-s162.bin` (S162).

## Quote re-location (whitespace-collapsed substring test, path:line)

File: `src/config/shared/workspace/WorkspaceRuleManager.cpp` (fetched, 91 lines). All 4/4 located at exactly the
reported lines:

- Line 26: `r->m_workspaceString == x.m_workspaceString` — located at line 26 (exact-match search in `replaceOrAdd`, requires `r->isEnabled()`).
- Line 30: `(*it)->mergeLeft(x);` — located at line 30 (duplicate selector merges into existing rule).
- Line 42: `workspace->matchesStaticSelector(rule->m_workspaceString)` — located at line 42 (lookup tests each enabled rule).
- Line 45: `mergedRule.mergeLeft(*rule);` — located at line 45 (each matching rule contributes to aggregate).

Semantic eyeball of the fetched file confirms the report's structural claims: `replaceOrAdd` (25–32) finds the first
enabled rule with exact `m_workspaceString` equality and `mergeLeft`s into it, else `add`s; `getWorkspaceRuleFor`
(34–51) walks enabled rules, skips non-matching via `matchesStaticSelector`, and merges matches into one result. No
discrepancy.

## S162 used-by extension claims (ConfigManager.cpp)

All three cited ranges verified in the fetched file:

- Lines 608–610: `m_config->registerHandler(&::handleWorkspaceRules, "workspace", {false});` at line 609. ✓
- Lines 335–342: `static Hyprlang::CParseResult handleWorkspaceRules(...)` delegates to
  `Config::Legacy::mgr()->handleWorkspaceRules(COMMAND, VALUE)` at line 339. ✓
- Lines 1676–1792: handler at 1676 takes first comma-delimited field (`value.find_first_of(',')` at 1678 →
  `first_ident` at 1680), assigns `wsRule.m_workspaceString = first_ident` (1686), parses rule fields via the
  `assignRule` lambda over the comma split (1781–1786), then calls
  `Config::workspaceRuleMgr()->replaceOrAdd(std::move(wsRule))` at line 1791. ✓

Correction for the proposal: the report asks that `335-342,608-610,1676-1792` be added to S162's anchor, but the
existing S162 row in `corpus/SOURCES.md` already anchors `src/config/legacy/ConfigManager.cpp:419-451,590-623,893-968,2016-2093` —
lines 608–610 (the `workspace` registerHandler call) already fall inside the existing `590-623` anchor. Only
`335-342` and `1676-1792` are genuinely new ranges for the used-by extension.

## Ledger checks

- `corpus/SOURCES.md` has no row for the `WorkspaceRuleManager.cpp` raw URL and no S178 row (grep for
  `S178|WorkspaceRuleManager` → no matches) — the proposed new row is not a duplicate.
- S162 exists exactly as the report states (sha256 `9db68cf…62b`, 90,963 bytes).

## Verdict lines

```
REOPEN S178 https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/workspace/WorkspaceRuleManager.cpp sha=match quotes=4/4 located — agree
REOPEN S162 https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp sha=match quotes=0/0 cited (range claims all verified) — agree
```

## Host safety

`coredumpctl list --no-pager --no-legend | grep -c /usr/bin/Hyprland` was 1338 before and 1338 after (delta 0).
No Hyprland process started, no live compositor queried, no tool installed. Only writes: the two re-fetch files under
`/fast/scratch/hyaku/mado-r27/reopen/` and this report.
