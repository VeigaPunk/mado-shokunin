# Reopen S163 — LayerRuleApplicator.cpp (round 24 wave 2)

Seat: `MadoR24.ReopenS163` (leaf; no subagents). Lane HEAD verified: `39c596307333b8ca0a1e42b3f3b9a748bb8b208b` (matches assignment). No tools installed (nothing needed; `curl`, `git` read-only, `python3` all present).

## S163 row (SOURCES.md at HEAD, line 175)

- URL: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/layerRule/LayerRuleApplicator.cpp`
- Row pin: commit `efb50993780079460b0cbed1363e2166a2de1d9f`, sha256 `9321999ac030e8da73abab53f6a0d6f0cf82ddc3c8c63befa845ade8716568ba`, 6193 B, lines 40-149.

## Pin resolution and byte integrity

1. **Refetch**: `curl -fsSL` on the pinned raw URL -> `/fast/scratch/hyaku/mado-r24/w2/S163.fetch.bin`.
2. **sha256/bytes**: `9321999ac030e8da73abab53f6a0d6f0cf82ddc3c8c63befa845ade8716568ba`, 6193 B — identical to the row-recorded values.
3. **Committed fetch bytes**: `cmp` of refetched bytes vs `.ufo/waves/round-24/fetch/S163.bin` -> identical (`CMP_IDENTICAL`); committed bin itself hashes to the same sha256 and 6193 B.
4. **Pin resolves**: read-only local clone (Hyprland v0.56.2, `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`) — `git cat-file -t efb50993780079460b0cbed1363e2166a2de1d9f` -> `commit`; `git show efb509…:src/desktop/rule/layerRule/LayerRuleApplicator.cpp` -> sha256 `9321999a…` and 6193 B, matching the refetch and row.

**Source/pin verdict: holds.**

## Claim A17 (rule-attribution-r24.md line 51)

> | A17 | A layer rule is applied dynamically only after the associated surface passes `wr->matches`. | S163 | "if (!wr->matches(m_ls.lock())) continue; applyDynamicRule(wr);" |

### (a) Quote occurs verbatim — HOLDS (whitespace-collapsed canon); not a literal contiguous substring

The exact single-line byte string `if (!wr->matches(m_ls.lock())) continue; applyDynamicRule(wr);` does **not** appear contiguously: the file has it split (LayerRuleApplicator.cpp lines 146-149):

```
146:        if (!wr->matches(m_ls.lock()))
147:            continue;
149:        applyDynamicRule(wr);
```

Collapsing all whitespace runs (the frozen predicate's definition of verbatim, c1/count.py `collapse()`) yields exactly the quoted text: `if (!wr->matches(m_ls.lock())) continue; applyDynamicRule(wr);`. The claim is also anchored per the predicate: backticked `wr->matches` (9 chars, in quote), and contains a rule-topic word. Frozen counter confirms `A17 S163 PASS_ROW` at HEAD (`39c596…`, mode=refetch, PASS_ROW=23/26, TARGET_MET, counter_sha256 b2f37c57…) and at the wave-1 receipt commit `cf86f9e0` (same counter sha, A17 PASS_ROW).

### (b) Claim TRUE of the quoted bytes; no overreach — HOLDS

- `CLayerRuleApplicator::applyDynamicRule` has exactly one call site in the whole v0.56.2 tree: `LayerRuleApplicator.cpp:149`, inside `propertiesChanged`, immediately after `if (!wr->matches(m_ls.lock())) continue;` (grep over `src/` for `applyDynamicRule` shows the remaining hits are `CWindowRuleApplicator::applyDynamicRule`, a different class).
- All layer-rule application funnels through `propertiesChanged`: `Engine.cpp:46` (`updateAllRules` → `ls->m_ruleApplicator->propertiesChanged(RULE_PROP_ALL)`) and `LayerSurface.cpp:169` (on layer map). No path reaches `applyDynamicRule` without the matches gate.
- The claim asserts a *necessary* condition ("applied dynamically only after … passes matches") and does not assert sufficiency; the additional preconditions in the loop (rule type == `RULE_TYPE_LAYER`, property-mask intersection, non-null `m_ls`) don't contradict it. No overreach.

### (c) Rule-attribution content — FAILS (generic rule mechanics)

The row states a gate on *when* a layer rule's dynamic effects are applied (match → apply). It identifies neither which rule produced an effect nor any channel that exposes rule identity; it is application mechanics of the same kind as A3/A4 (static pass calls `matches` before applying), not attribution. At most it contributes indirectly to attribution-by-reasoning (only a matching rule can have produced the effect) — but by the rubric ("which rule produced an effect / what exposes rule identity") it does not carry attribution content.

## VERDICT: partial

- Source/pin integrity: holds (refetch sha256 + byte count == row == committed `S163.bin`; pin resolves in the local clone).
- A17 (a) quote: holds (canonical whitespace-collapsed verbatim; not literal contiguous text).
- A17 (b) truth: holds (sole dynamic-application path is gated by `wr->matches`; no bypass, no overreach).
- A17 (c) attribution relevance: fails — generic rule mechanics, not rule attribution.

**A17 row verdict: partial** (mechanics row passes both counter criteria but adds no attribution content to the note's answer table).

## Residual risk / verification gaps

- Attribution relevance judged against the rubric in the assignment; the note itself places A17 outside its "Answer" table's routes, consistent with the mechanics classification.
- No claim row in scope beyond A17 cites S163 (grep of rule-attribution-r24.md for `S163` returns only A17).
- All checks run read-only; no git/jj writes, no hyprctl mutation, no installs.
