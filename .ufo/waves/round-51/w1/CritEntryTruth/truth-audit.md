# Dispatcher-adjacent truth audit (fallback: round 50)

The round-51 `w1/ScrDispatchEntry/` directory was empty when checked, so this audits dispatcher-adjacent statements in `corpus/knowledge/hyprland-bind-key-match-r50.md`. Scope is only dispatcher execution/argument parsing/submap claims; it does not audit unrelated key matching assertions.

## Unsupported or overbroad claims

1. **Line 57: “The value is split into at most four (five with `d`, plus one with `k`) comma arguments.”**
   - Pin cited: `Hyprland-legacy-ConfigManager.cpp:1555`, `CVarList(value, numbArgs)`.
   - Evidence: that cited line only shows the invocation and argument-count variable. It does not establish the value of `numbArgs`, the effects of `d`/`k`, or the maximum count. The neighboring line 1567 about `multiKey` does not prove the split bound either.
   - Corrected sentence: “The handler calls `CVarList(value, numbArgs)` to split the value into comma arguments; the split limit is not established by this cited line.”
   - Impact: sourced-claim truth / C2 coverage.

2. **Line 59: “the catch-all is refused outside a submap.”**
   - Pin cited: `Hyprland-legacy-ConfigManager.cpp:1620`, quoted diagnostic `Catchall not allowed outside of submap!`.
   - Evidence: diagnostic supports a refusal path, but this single line does not establish its condition, whether it is specifically outside a submap, or whether it is the only refusal condition. The claim's qualifier is not supplied by the cited text.
   - Corrected sentence: “The parser contains the diagnostic `Catchall not allowed outside of submap!` at line 1620; this citation alone does not establish the condition that reaches it.”
   - Impact: sourced-claim truth / C2 coverage.

3. **Line 72: “Binds are appended in parse order” with citations at `KeybindManager.cpp:189` and `:634`.**
   - Pin cited: `:189` `m_keybinds.emplace_back(KEYBIND);`; `:634` loop over `m_keybinds`.
   - Evidence: the append operation and vector scan support append order and scan order, respectively, but do not show that `KEYBIND` is appended in configuration parse order. The cited manager lines do not connect the append call to parser/config order.
   - Corrected sentence: “`addKeybind` appends each received bind to `m_keybinds` (line 189), and `handleKeybinds` scans that vector (line 634); these citations do not establish the order in which configuration binds are received.”
   - Impact: sourced-claim truth / C2 coverage.

4. **Line 73: “multiple eligible binds can be dispatched in vector order.”**
   - Pin cited: `KeybindManager.cpp:773`, `bindsHit.emplace_back(k)`.
   - Evidence: this line supports adding a bind to the hit collection, not dispatching the collection, the order of dispatch, or whether all eligible entries survive later control flow. The wording leaps from collection to execution.
   - Corrected sentence: “A passing bind is appended to `bindsHit` at line 773; this citation alone does not establish which collected binds are ultimately dispatched or their dispatch order.”
   - Impact: sourced-claim truth / C2 coverage.

5. **Line 73: “`nonConsuming` and `autoConsuming` affect the `found`/continue path as well as suppression.”**
   - Pin cited: `KeybindManager.cpp:728` and `:747`, which quote `release` gates only.
   - Evidence: the cited lines contain no `nonConsuming`, `autoConsuming`, `found`, or `continue` logic. Thus the cited evidence does not support this specific causal assertion.
   - Corrected sentence: “The cited lines show press/release eligibility checks; they do not establish the effects of `nonConsuming` or `autoConsuming`.”
   - Impact: sourced-claim truth / C2 coverage.

## Dispatcher subject not covered by fallback

The fallback entry has no supported detailed account of `handleKeybind` dispatch-string parsing, `m_mDispatchers`, dispatcher argument splitting, special submap dispatch behavior, or the `hyprctl dispatch` route. The few mentions of submap/catch-all above are not a substitute for those claims. No additional dispatcher-mechanism statement in the audited lines can be validated as a description of that requested surface.
