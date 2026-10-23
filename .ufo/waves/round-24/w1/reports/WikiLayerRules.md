# Wiki layer/workspace rules — source-opener report

## Verdict

Source opener complete for the two assigned wiki pages. Six proposed claim rows passed the source-quote and anchor checks. This is not a C1 target verdict: the rows retain `S?` pending integration, cover only two source files, and the C1 counter was not run.

## Behavior and findings

At pinned wiki commit `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`, the layer-rules page documents `hl.layer_rule()`, says layer-rule syntax matches `hl.window_rule()`, gives `namespace` as a layer prop (with `hyprctl layers` as the place to check it), lists effects, and says layer rules return a handle with `set_enabled()`/`is_enabled()`.

The workspace-rules page documents `hl.workspace_rule()` syntax with a workspace selector and rule fields, describes workspace-specific behavior and rule options, and directs readers to layout pages for layout-specific rules. It says workspace rules can set per-workspace layouts.

Neither of these two pages explains how to determine which matched layer/workspace rule produced an observed applied effect. The layer handle methods document enablement controls, not attribution of an effect to a particular rule. This is limited to these two pages; it does not establish that no attribution mechanism exists elsewhere. Host behavior remains [UNK].

## Proposed SOURCES rows

| S? | Layer rules — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/layer-rules.md | docs | A | layer-rule API, match property, effects, and handles | content/configuring/core/rules/layer-rules.md:18-22, 26-43, 68-76 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:a513798fec803eed723678a2acf24c6e8bdb896fbc7358b01d3201aea2e19836, 2129 B | documents separate layer rules, shared window-rule syntax, namespace matching, effects, and enablement handles | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S? | Workspace Rules — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/workspace-rules.md | docs | A | workspace-rule syntax, options, and per-workspace layouts | content/configuring/core/rules/workspace-rules.md:6-19, 22-42, 59-66 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:0d6fd4ab4477082d4681aacc7639b1f1c22fac4e3582dc049b19385660721074, 2954 B | documents workspace selector and rule fields, workspace options, and layout-specific rules | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |

## Proposed claim rows

| A1 | This page documents `hl.layer_rule()` for separate rules on layers that are not windows. | S? | "These have separate rules using `hl.layer_rule()`." |
| A2 | The page describes layer-rule syntax as the same as `hl.window_rule()` syntax. | S? | "The syntax is the same as `hl.window_rule()`." |
| A3 | The page says layer rules return a handle exposing `set_enabled()` and `is_enabled()` controls. | S? | "Layer rules also return a handle with `set_enabled()`/`is_enabled()`:" |
| A4 | This page says, "You can set workspace rules to achieve workspace-specific behaviors." | S? | "You can set workspace rules to achieve workspace-specific behaviors." |
| A5 | The page states, "Some layouts have their own specific rules, which can be found on the corresponding layout page." | S? | "Some layouts have their own specific rules, which can be found on the corresponding layout page." |
| A6 | The page says to use workspace rules to set per-workspace layouts. | S? | "Use workspace rules to set per-workspace layouts:" |

## Gates, commands, and outcomes

Both sources were fetched from their pinned raw URLs on 2026-10-23. Exact fetch commands and receipts:

```sh
timeout 60 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/layer-rules.md' -o '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-1.bin' && sha256sum '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-1.bin' && wc -c '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-1.bin'
```
Output: `a513798fec803eed723678a2acf24c6e8bdb896fbc7358b01d3201aea2e19836  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-1.bin`; `2129 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-1.bin`.

```sh
timeout 60 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/workspace-rules.md' -o '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-2.bin' && sha256sum '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-2.bin' && wc -c '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-2.bin'
```
Output: `0d6fd4ab4477082d4681aacc7639b1f1c22fac4e3582dc049b19385660721074  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-2.bin`; `2954 /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-2.bin`.

Quote check: a Python check over the six proposed `(file, quote, claim)` tuples whitespace-collapsed each decoded fetched file and quote, then checked quote presence, at most 25 quote words, at least 8 claim words, a rule-topic substring, and the 4-word-run-or-backticked-identifier anchor. All six passed. Output, in row order:

```text
WikiLayerRules-1.bin: quote_present=True quote_words=7 claim_words=14 topic=True anchor=True row_predicate=True
WikiLayerRules-1.bin: quote_present=True quote_words=8 claim_words=12 topic=True anchor=True row_predicate=True
WikiLayerRules-1.bin: quote_present=True quote_words=9 claim_words=13 topic=True anchor=True row_predicate=True
WikiLayerRules-2.bin: quote_present=True quote_words=9 claim_words=12 topic=True anchor=True row_predicate=True
WikiLayerRules-2.bin: quote_present=True quote_words=16 claim_words=19 topic=True anchor=True row_predicate=True
WikiLayerRules-2.bin: quote_present=True quote_words=7 claim_words=11 topic=True anchor=True row_predicate=True
```

Narrow attribution-term sweep command:

```sh
timeout 20 grep -niE 'attribut|which[[:space:]].*rule|matched|getprop|prop|tag|set_enabled|is_enabled' '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-1.bin' '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-2.bin'
```
Output (only layer page hits):

```text
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-1.bin:12:        prop = some_prop_value,
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-1.bin:24:### Props
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-1.bin:26:| Prop | Description | Type |
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-1.bin:68:Layer rules also return a handle with `set_enabled()`/`is_enabled()`:
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/fetch/w1/WikiLayerRules-1.bin:76:myLayerRule:set_enabled(false)
```

The sweep is lexical and limited to the two fetched pages; it is not proof of system-wide absence. No package/tool installation, host query, build, C1 counter, or C2 counter was run.

## Touched surfaces and artifacts

Created the two fetched source receipts and this assigned report only; no product code, corpus entry, README, or SOURCES file was edited.

- `.ufo/waves/round-24/fetch/w1/WikiLayerRules-1.bin`
- `.ufo/waves/round-24/fetch/w1/WikiLayerRules-2.bin`
- `.ufo/waves/round-24/w1/reports/WikiLayerRules.md`

## Out of scope and limits

No host compositor behavior was queried; it remains [UNK]. No source-code pages, Hyprland APIs outside these two wiki pages, or other documentation routes were inspected. C1 integration, source-ID assignment, the third distinct C1 source, the corpus note, and both round counters remain outside this scoped source-opening item and are not claimed complete.
