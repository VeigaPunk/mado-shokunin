# AtkWindowObject — attack on "value + rule-property mask + priority class, not rule identity" (rows A5–A8)

**Seat:** MadoR24.AtkWindowObject (critic, leaf). **Item attacked:** the round-24 note's
per-property-origin row, `corpus/knowledge/rule-attribution-r24.md:24`:

> `| per-property origin | applicator stores a value plus a **rule-property mask** and a priority class (A5–A8) | which *match properties* a setting came through, and that it was a window rule | the rule's identity; neither is exported by hyprctl, Lua or socket2 |`

and the question it must answer: **is any rule pointer, name or index retained per applied property
(`m_otherProps`, `SCustomPropContainer::idx`, …)?**

**Pin:** lane master `39c59630` (note text), sources at Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f`
(= v0.56.2; `git rev-parse HEAD` in the read-only clone returns exactly that, clean tree). Files read at the
pin: `src/desktop/rule/windowRule/WindowRuleApplicator.{hpp,cpp}`, `src/desktop/types/OverridableVar.hpp`,
`src/desktop/view/Window.hpp`, plus `Rule.hpp`, `RuleWithEffects.hpp`, `WindowRule.hpp`,
`WindowRuleEffectContainer.{hpp,cpp}`, `EffectContainer.hpp`, `TagKeeper.hpp`, `Rule.cpp`.

## 1. Byte check of the four cited rows

Fresh fetch to `/tmp` (ordinary curl on the pinned raw URLs), hashes, and byte-compare against the committed
round-24 fetch:

```text
$ curl -sSfL -o r24-S155.bin …/efb50993…/src/desktop/rule/windowRule/WindowRuleApplicator.cpp
$ curl -sSfL -o r24-S156.bin …/efb50993…/src/desktop/rule/windowRule/WindowRuleApplicator.hpp
fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b  r24-S155.bin
334e1254a66e2df8ef243544e3ff99db398ed5ec6e48996d496d05ff7bf50f44  r24-S156.bin
$ cmp r24-S155.bin .ufo/waves/round-24/fetch/S155.bin && cmp r24-S156.bin .ufo/waves/round-24/fetch/S156.bin
BYTES_IDENTICAL
```

These equal the `sha256:` values recorded for S155/S156 in `corpus/SOURCES.md`, so the committed bytes are the
pinned upstream bytes. Quote presence in those bytes:

| row | quote | present |
|---|---|---|
| A5 | `m_allowsInput.first.set(std::get<bool>(value), Types.PRIORITY_WINDOW_RULE);` | 1 hit, S155.bin (cpp:234) |
| A6 | `m_alpha.second = rule->getPropertiesMask();` | 0 raw / 1 whitespace-collapsed, S155.bin (source has an 11-space run at cpp:156) |
| A7 | `std::pair<Types::COverridableVar<type>, std::underlying_type_t<eRuleProperty>> m_##name = {def, RULE_PROP_NONE};` | 1 hit, S156.bin (hpp:77) |
| A8 | `std::vector<std::pair<std::string, std::underlying_type_t<eRuleProperty>>> m_dynamicTags;` | 1 hit, S156.bin (hpp:140) |

A6 only matches after whitespace collapse, which is exactly the frozen predicate's quote rule; not a defect.
**The four count rows themselves are accurate as written.**

## 2. What the applicator actually retains

Per-property slots (the 42 `DEFINE_PROP` fields, hpp:75-88 macro):

```cpp
private:
  std::pair<Types::COverridableVar<type>, std::underlying_type_t<eRuleProperty>> m_##name = {def, RULE_PROP_NONE};
public:
  Types::COverridableVar<type>& name() { return m_##name.first; }   // mask has no accessor
```

`COverridableVar` (OverridableVar.hpp:72 `set`, :121 `getPriority`, :153
`std::array<std::optional<T>, PRIORITY_END> m_values`) stores per-priority optionals only. Every single write the
applicator makes from a rule is enumerable: over the whole cpp, `rule->` appears only as `rule->effects()` (×2)
and `rule->getPropertiesMask()` (×44). There is no `rule->name()`, no stored `CWindowRule*`/`SP<CWindowRule>` per
property, and no index of the rule in the engine vector. `m_otherProps.props` is keyed by the **effect** id
(`windowEffects()` is a process-global name-vector singleton, `WindowRuleEffectContainer.cpp:8-11`;
`EffectContainer::registerEffect` returns the position in that vector), and `SCustomPropContainer::idx = key` is
that same effect index, `effect` is the effect's raw value string (cpp:97-107). `idx` has no in-tree reader at
all (grep: only the two writes, window and layer applicators). `m_dynamicTags` holds `(tag string, mask)` pairs
(hpp:140, cpp:162). `CTagKeeper` holds a `std::set<std::string>` (TagKeeper.hpp).

**Answer to the assigned question: no rule pointer, name or rule index is retained per applied property.**
`m_otherProps`' `idx` is an effect index, not a rule index.

## 3. Counterexamples and where the printed sentence breaks

### 3.1 `m_execRules` is rule identity kept on the applicator (the strongest counterexample)

`WindowRuleApplicator.hpp:146-148`:

```cpp
private:
    PHLWINDOWREF                          m_window;
    std::vector<SP<CWindowRule>>          m_execRules;
```

Populated at cpp:502 (`m_execRules.emplace_back(wr)`) for every matching exec rule, applied at cpp:517-521, and
the engine registration is dropped while the `SP` keeps the object alive (`ruleEngine()->unregisterRule(wr)`,
cpp:521). So the applicator does hold rule objects, and for exec rules it is the only place the rule survives.
This does **not** restore attribution: the vector is not linked to any property slot (the property slots hold
only `getPropertiesMask()`), it is `private` with no accessor and no `friend`, and the public path
(`CWindow::m_ruleApplicator` is public, `Window.hpp:126-463` region, line 236; `m_otherProps` is public,
hpp:63-72, annotated "Plugins may read this") cannot reach it. But the sentence's absolute clause
"**not rule identity**" is false as a description of applicator state: identity *is* held, just never associated
with a value and never exported. The wave-1 source report
(`.ufo/waves/round-24/w1/reports/SrcWindowRuleApplicator.md`) said so explicitly ("The applicator separately has
an `m_execRules` vector of `SP<CWindowRule>` objects…"); S156's own annotation mentions "a separate exec-rule
collection"; the integrated note never mentions `m_execRules` anywhere.

### 3.2 "value plus a mask and a priority class" is not uniform

- `static_` (hpp:41-61) holds **bare** `std::string` / `std::optional<T>` / `std::vector<std::string>` for
  float, tile, fullscreen, maximize, fullscreenstate, move, size, center, pseudo, monitor, workspace,
  noinitialfocus, pin, group, suppressevent, content, noclosefor, scrollingwidth. No `eRuleProperty` mask, no
  `eOverridePriority`. For these effects the row's "which match properties a setting came through" is not merely
  coarse — nothing is recorded.
- `m_dynamicTags` (hpp:140) and `m_otherProps` (hpp:63-72) carry a mask but **no priority class** (they are not
  `COverridableVar`s).
- The priority class exists only inside the `COverridableVar` of the generated dynamic props.

So the formula holds for exactly the `DEFINE_PROP` fields (42 of them), not for the applicator's state as a
whole, and the table row does not say "dynamic".

### 3.3 A generated property whose mask is never its own: `tonemap`

`WindowRuleApplicator.cpp:348-351`:

```cpp
case WINDOW_RULE_EFFECT_TONEMAP: {
    m_tonemap.first.set(std::get<int64_t>(value), Types::PRIORITY_WINDOW_RULE);
    m_noAutoHDR.second |= rule->getPropertiesMask();     // wrong mask slot
    break;
}
```

A sweep of all 42 generated props shows `tonemap` is the only one with no `m_tonemap.second` write: its mask stays
`RULE_PROP_NONE`, and `m_tonemap` is absent from the `resetProps` tuple (cpp:41-63), so `resetProps` never clears
it either. For the tonemap effect the row's "which match properties a setting came through" returns nothing.
This is an upstream quirk, but it is inside the exact mechanism the row cites, so the sentence is not
exception-free even for generated props.

## 4. Verdict on the note sentence

- The attribution-relevant core — **no per-property rule identity, and no per-property mask/priority exported by
  hyprctl, Lua or socket2** — is confirmed at the pin.
- The sentence as printed overstates in three ways: it implies a uniform value+mask+priority layout (static
  effects have none of the tracking; tags/custom props lack the priority class), it denies rule identity
  absolutely while `m_execRules` retains `SP<CWindowRule>` (private, non-attributing), and its "which match
  properties" clause fails for `tonemap`.
- Rows A5–A8 and their anchors are correct; the defect is the summary row and the missing `m_execRules`
  sentence, not the counted quotes.

**Impacted axes:** C1 coverage (note accuracy only; PASS_ROW accounting is unchanged — the predicate counts A-rows
against bytes, and those pass). C2 calibration untouched. No `tools/` file, SOURCES row, SCORECARD, LOG or
PROVINCE line is affected by the correction.

**Smallest safe correction** (wording-only, no new claims, no counter change):

1. Scope row 24's route cell to dynamic props and add the exceptions: "each `DEFINE_PROP` dynamic property stores
   a `COverridableVar` value (per-priority slot) beside an `eRuleProperty` mask; static effects keep a bare
   value; tags and plugin-registered effects keep a mask without a priority class."
2. Replace "not rule identity" with "no rule identity **tied to a property**" and add one Limits line: the
   applicator keeps `m_execRules` (`std::vector<SP<CWindowRule>>`, private, no accessor) for exec rules; it is
   rule identity, but it is not linked to any value and cannot be read through hyprctl, Lua, socket2 or a plugin.
3. If the row keeps the "which match properties" wording, exclude `tonemap` (mask written to
   `m_noAutoHDR.second`, cpp:350) or drop the claim to "for most dynamic properties".

No git/jj writes, no lane edits outside this report, no host commands, no installs. I did not run the counted C1
counter (other lane); the bytes above are an independent re-fetch and compare.

VERDICT: partial
