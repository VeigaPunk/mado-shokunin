# ScribeWsNote — round 27 workspace-rules knowledge draft

## Behavior and findings

Drafted `.ufo/waves/round-27/drafts/workspace-rules-r27.md` with source front matter listing S178–S182 plus S158 and S162, `verified-at: <pending>`, and the requested C1 recheck command. It documents the wiki selector grammar with source-era qualification; v0.56.2 workspace parsing; all rule-key branches located in the handler; gaps shorthand; integer/boolean-like conversion; `on-created-empty` command normalization; enabled-rule manager matching and exact-selector merge behavior; and a `config line → table effect` decision table.

The permitted source reports locate the `onCreatedEmpty` serializer key and workspace-rule iteration under S158, but do not enumerate the full JSON object. The draft marks the exact JSON field set, omission behavior, output `enabled` member/type, and ordering `[INF]` instead of inferring them. It also records Lua-era behavior, runtime `hyprctl keyword workspace`, and dynamic selector behavior as open items. The full table-shape limitation is the principal unresolved finding; `verified-at` remains pending.

Draft provenance: read `w1/reports/SrcWsRuleCode.md`, `SrcBoolAndExec.md`, `SrcWsRuleLegacy.md`, and `SrcWikiWsRules.md`; used the corresponding fetched artifacts under `round-27/fetch/` for manager, config handler, gaps, boolean parser, command normalizer, and wiki line references. Read `corpus/knowledge/animation-table-r26.md` for house shape and `round-27/registration.md` for the wave contract. ScribeSourcesRows supplied the assigned IDs S178 (wiki), S179 (manager), S180 (gap parser), S181 (integer parser), and S182 (command normalizer); the draft also includes existing S158 and S162.

A broad report-directory search incidentally returned snippets from non-Src reports. Those reports were not used as sources for the draft; all factual draft claims are confined to the four Src reports and their fetch artifacts, with unlocated claims marked `[INF]`.

## Gates and host safety

No C1/C2 counter, oracle, build, test, live compositor query, or runtime `hyprctl` command was run. No Hyprland process was started. No tool was installed. No gate passed or failed in this work.

Exact coredump-count command run before and after drafting:

```sh
timeout 20 prlimit --as=4000000000 --core=0 -- bash -c 'coredumpctl list --no-pager --no-legend | grep -c /usr/bin/Hyprland'
```

Before: `1338`. After: `1338`. Delta: `0`.

## Touched surfaces and out of scope

Written only:
- `.ufo/waves/round-27/drafts/workspace-rules-r27.md`
- `.ufo/waves/round-27/w2/reports/ScribeWsNote.md`

Source reports, fetched files, the house-style knowledge entry, registration, source ledger, and product code were not changed. The final corpus path `corpus/knowledge/workspace-rules-r27.md` was not written. No measurement receipt exists for this draft.

Out of scope: C1 scoring or recheck, live capture, full HyprCtl serializer enumeration beyond what the allowed source report locates, source-ledger edits, and runtime/Lua-era/dynamic-selector investigation.

## Artifact paths

- Draft: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/drafts/workspace-rules-r27.md`
- This report: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-27/w2/reports/ScribeWsNote.md`
