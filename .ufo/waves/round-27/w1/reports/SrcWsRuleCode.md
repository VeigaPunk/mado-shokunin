# SrcWsRuleCode — workspace-rule source opening

## Behavior and findings

Pinned Hyprland v0.56.2 source at commit `efb50993780079460b0cbed1363e2166a2de1d9f` separates the legacy `workspace =` handler from workspace-rule management. In `src/config/legacy/ConfigManager.cpp`, the legacy config manager registers `handleWorkspaceRules` for the `workspace` keyword (lines 608–610); the callback delegates to that handler (335–342). The handler takes the first comma-delimited field as `m_workspaceString`, parses the following rule fields into a `CWorkspaceRule`, then calls `workspaceRuleMgr()->replaceOrAdd(std::move(wsRule))` (1676–1792).

The manager implementation opened for this item is `src/config/shared/workspace/WorkspaceRuleManager.cpp`. `replaceOrAdd` searches enabled rules for an exact `m_workspaceString` match, adds a new rule if none is found, and otherwise merges into the existing rule. Separately, `getWorkspaceRuleFor` walks enabled rules, tests each with `matchesStaticSelector`, and merges every matching rule into the result. Thus repeated identical selectors are combined at insertion, while distinct selectors that both match a workspace are combined at lookup.

The pinned GitHub tree listing for `src/config/shared/workspace/` contained `WorkspaceRuleManager.cpp` (2,672 bytes), alongside `WorkspaceRule.cpp`, `WorkspaceRule.hpp`, and `WorkspaceRuleManager.hpp`.

## Opened source and located quotes

Fetched raw source:

- URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/workspace/WorkspaceRuleManager.cpp`
- Commit: `efb50993780079460b0cbed1363e2166a2de1d9f`
- SHA-256: `06e8dcbaea83e51710bd372a8f264ad3d07bbe061b9720bbe456811451c02d10`
- Size: 2,672 bytes
- Anchors: `src/config/shared/workspace/WorkspaceRuleManager.cpp:25–32, 34–52`
- Artifact: `.ufo/waves/round-27/fetch/SrcWsRuleCode.bin`

Quotes were checked against the fetched UTF-8 bytes by collapsing whitespace and testing substring membership; all four checks passed.

- Line 26: “r->m_workspaceString == x.m_workspaceString” — this is the exact selector-string equality used by the replace-or-add search (which also requires the stored rule to be enabled).
- Line 30: “(*it)->mergeLeft(x);” — when that search finds a duplicate selector, the new fields are merged into the existing rule.
- Line 42: “workspace->matchesStaticSelector(rule->m_workspaceString)” — lookup tests each enabled rule against the workspace's static selector matcher.
- Line 45: “mergedRule.mergeLeft(*rule);” — each matching rule contributes to the returned aggregate.

## SOURCES ledger proposal

A search for the exact `WorkspaceRuleManager.cpp` raw URL in `corpus/SOURCES.md` found no existing row. Proposed new 11-cell row:

| S178 | Hyprland workspace rule manager — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/workspace/WorkspaceRuleManager.cpp | code | A | Exact-selector replace-or-add and aggregation of static-selector matches in the workspace rule manager | src/config/shared/workspace/WorkspaceRuleManager.cpp:25-32,34-52 @ efb50993780079460b0cbed1363e2166a2de1d9f, sha256:06e8dcbaea83e51710bd372a8f264ad3d07bbe061b9720bbe456811451c02d10, 2672 B | Reuses a rule only for an enabled exact-string selector match and merges it; workspace lookup separately applies every enabled static-selector match into one rule | mined | 2026-10-23 | on-release | corpus/knowledge/workspace-rules-r27.md |

The parser URL, `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp`, already appears as S162 (SHA-256 `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`, 90,963 bytes). Do not add a duplicate row. Propose a `used-by` extension on S162 to include `corpus/knowledge/workspace-rules-r27.md`; the additional workspace-specific anchors are `src/config/legacy/ConfigManager.cpp:335-342,608-610,1676-1792` at the same pinned commit. The existing S162 row's current anchor ranges cover other handlers, so those workspace ranges should be added to its anchor if the registry is updated to substantiate this use.

## Commands, gates, and safety

Fetch command (run from the lane root):

```sh
mkdir -p .ufo/waves/round-27/fetch && env -i PATH=/usr/bin HOME=/home/vgpnk timeout 60 prlimit --as=4000000000 -- curl -fsSL 'https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/workspace/WorkspaceRuleManager.cpp' -o '.ufo/waves/round-27/fetch/SrcWsRuleCode.bin'
```

It completed successfully. `sha256sum` returned the digest above; `wc -c` returned `2672`; `file` identified the artifact as `C source, ASCII text`. The quote-validation check printed `QUOTE_OK` for all four excerpts.

Hyprland coredump count command, run before and after this work:

```sh
timeout 30 prlimit --as=4000000000 -- bash -c 'coredumpctl list --no-pager --no-legend | grep -c /usr/bin/Hyprland'
```

Output was `1338` both times (delta 0). No Hyprland process was started and no live compositor was queried. No tool was installed. C1/C2 counters, builds, and tests were not run; this was a source-opening task, not a gate execution.

## Touched surfaces and scope

Created only the source artifact `.ufo/waves/round-27/fetch/SrcWsRuleCode.bin` and this report, `.ufo/waves/round-27/w1/reports/SrcWsRuleCode.md`. `corpus/SOURCES.md` was read but not edited. Out of scope: product-code changes, edits to the SOURCES ledger, implementation of the workspace-rule tool or C2 suites, and C1/C2 scoring.
