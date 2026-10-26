# Located-quote fact table — source chain of the host gkeep window size (round 43, seat ExecSrcChain)

Scope: only the seven code receipts pinned for round 43 (S290–S296). No new source was opened for this table.
Provenance of every receipt: `https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/<path>`,
tag `v0.56.2`, commit `efb50993780079460b0cbed1363e2166a2de1d9f` (per the round-43 fetch set).

| id | receipt (Sid) | file |
|---|---|---|
| S290 | `Hyprland-RegexMatchEngine.cpp` | `src/desktop/rule/matchEngine/RegexMatchEngine.cpp` |
| S291 | `Hyprland-WindowRuleApplicator.cpp` | `src/desktop/rule/WindowRuleApplicator.cpp` |
| S292 | `Hyprland-DefaultFloatingAlgorithm.cpp` | `src/layout/algorithm/floating/DefaultFloatingAlgorithm.cpp` |
| S293 | `Hyprland-Target.cpp` | `src/layout/target/Target.cpp` |
| S294 | `Hyprland-WindowTarget.cpp` | `src/layout/target/WindowTarget.cpp` |
| S295 | `Hyprland-GeometricMovableAnimated.cpp` | `src/desktop/view/GeometricMovableAnimated.cpp` |
| S296 | `Hyprland-HyprCtl.cpp` | `src/debug/HyprCtl.cpp` |

Method. Each quote below is the text of the cited line with leading indentation removed, verified as an
exact substring of that 1-based line by `verify-facts.py` (fixed-string, per line), which also re-checks the
receipt sha256 and that no quote exceeds 25 words. Script output: `verify-output.txt` (this directory),
final line `rows=65 failures=0 distinct_receipts=7`. Quotes are therefore located, not paraphrased.
One spelling note: inside the table a C++ `||` is written `\|\|` because a bare pipe ends a table cell; the
checker compares the unescaped text, so `\|\|` in the table means the literal `||` on the line.

## Chain in one line

rule text (not in this seat's receipts) → S290 match (anchor/negation) → S291 `static_.floating` / `static_.size`
→ S292 `newTarget` size override of the desired geometry → S293 `ITarget::setPositionGlobal` stores+rounds the box
→ S294 `CWindowTarget::updatePos` floating branch writes `setBox` and sends a configure → S295 `setBox`/`resize`
write `m_realSize` → S296 `clients -j` prints `w->size(GEOMETRIC_GOAL)`, i.e. `m_realSize->goal()`.

## Table

| id | claim the quote supports | quote | file:line | sha256 |
|---|---|---|---|---|
| F1 | S290/B — the match engine treats a `negative:` prefix as an instruction at construction time | `if (regex.starts_with("negative:")) {` | Hyprland-RegexMatchEngine.cpp:7 | 8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282 |
| F2 | S290/B — the prefix is stripped (9 chars) and the remainder compiled into `re2::RE2` | `m_regex    = makeUnique<re2::RE2>(regex.substr(9));` | Hyprland-RegexMatchEngine.cpp:9 | 8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282 |
| F3 | S290/B — `match()` is `RE2::FullMatch` on the whole string, and `!= m_negative` flips the result when `negative:` was present | `return re2::RE2::FullMatch(other, *m_regex) != m_negative;` | Hyprland-RegexMatchEngine.cpp:16 | 8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282 |
| F4 | S291/C — the `float` effect writes a plain `bool` into `static_.floating` | `static_.floating = std::get<bool>(value);` | Hyprland-WindowRuleApplicator.cpp:390 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F5 | S291/C — the `tile` effect writes the negation of its bool into the same field | `static_.floating = !std::get<bool>(value);` | Hyprland-WindowRuleApplicator.cpp:394 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F6 | S291/C — the `size` effect has its own case in the static-rule switch | `case WINDOW_RULE_EFFECT_SIZE: {` | Hyprland-WindowRuleApplicator.cpp:421 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F7 | S291/C — the only value form the applicator accepts for `size` is `Math::SExpressionVec2`; it does no string parsing itself | `const auto& expr = std::get<Math::SExpressionVec2>(value);` | Hyprland-WindowRuleApplicator.cpp:422 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F8 | S291/C — an empty expression clears the stored rule size | `static_.size.reset();` | Hyprland-WindowRuleApplicator.cpp:424 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F9 | S291/C — a non-empty expression is stored verbatim in `static_.size` (no clamp, no evaluation here) | `static_.size = expr;` | Hyprland-WindowRuleApplicator.cpp:426 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F10 | S291/C — the *maxsize* case evaluates the expression and rejects a component `< 1` | `if (VEC->x < 1 \|\| VEC->y < 1) {` | Hyprland-WindowRuleApplicator.cpp:183 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F11 | S291/C — `maxsize` becomes a window-rule-priority overridable value | `m_maxSize.first = Types::COverridableVar(*VEC, Types::PRIORITY_WINDOW_RULE);` | Hyprland-WindowRuleApplicator.cpp:188 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F12 | S291/C — the max clamp is applied when tiled-size limits are on **or** the window is floating (the gkeep case) | `if (*PCLAMP_TILED \|\| m_window->m_isFloating)` | Hyprland-WindowRuleApplicator.cpp:190 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F13 | S291/C — that max clamp call, `clampWindowSize(min=nullopt, max=m_maxSize)` | `m_window->clampWindowSize(std::nullopt, m_maxSize.first.value());` | Hyprland-WindowRuleApplicator.cpp:191 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F14 | S291/C — `minsize` becomes a window-rule-priority overridable value | `m_minSize.first = Types::COverridableVar(*VEC, Types::PRIORITY_WINDOW_RULE);` | Hyprland-WindowRuleApplicator.cpp:218 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F15 | S291/C — the min clamp uses the same tiled-or-floating gate | `if (*PCLAMP_TILED \|\| m_window->m_isFloating)` | Hyprland-WindowRuleApplicator.cpp:219 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F16 | S291/C — that min clamp call, `clampWindowSize(min=m_minSize, max=nullopt)` | `m_window->clampWindowSize(m_minSize.first.value(), std::nullopt);` | Hyprland-WindowRuleApplicator.cpp:220 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F61 | S291/C — the *minsize* case logs the string "Invalid size for maxsize" (copy-paste artefact; do not read this log line as a maxsize report) | `Log::logger->log(Log::ERR, "Invalid size for maxsize");` | Hyprland-WindowRuleApplicator.cpp:214 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F62 | S291/C — enclosing function of that switch is `applyStaticRule` (the `try`/`catch` in the file sits only in `applyDynamicRule`, lines 168/192/197/221) | `CWindowRuleApplicator::SRuleResult CWindowRuleApplicator::applyStaticRule(const SP<CWindowRule>& rule) {` | Hyprland-WindowRuleApplicator.cpp:378 | fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b |
| F17 | S292/D — built-in fallback size when nothing else applies | `constexpr const Vector2D DEFAULT_SIZE = {640, 400};` | Hyprland-DefaultFloatingAlgorithm.cpp:16 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F56 | S292/D — `newTarget` first asks the target for its desired geometry (that path clamps min/max, F39–F42) | `const auto DESIRED_GEOM = target->desiredGeometry();` | Hyprland-DefaultFloatingAlgorithm.cpp:21 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F57 | S292/D — the rule-size branch is gated on the window's first map | `if (target->window() && target->window()->m_firstMap) {` | Hyprland-DefaultFloatingAlgorithm.cpp:49 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F18 | S292/D — before the rule is applied the size animation is warped to the desired/default size so expressions can read it | `WINDOW->sizeAnimation()->setValueAndWarp(DESIRED_GEOM ? DESIRED_GEOM->size : DEFAULT_SIZE);` | Hyprland-DefaultFloatingAlgorithm.cpp:53 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F19 | S292/D — presence test for a rule-set size | `if (WINDOW->m_ruleApplicator->static_.size) {` | Hyprland-DefaultFloatingAlgorithm.cpp:55 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F20 | S292/D — the stored expression is evaluated by the window, and a parse failure only logs an error (the desired size survives) | `const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);` | Hyprland-DefaultFloatingAlgorithm.cpp:56 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F21 | S292/D — first component of the expression becomes the box width | `windowGeometry.w = COMPUTED->x;` | Hyprland-DefaultFloatingAlgorithm.cpp:60 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F22 | S292/D — second component becomes the box height | `windowGeometry.h = COMPUTED->y;` | Hyprland-DefaultFloatingAlgorithm.cpp:61 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F23 | S292/D — quirk: the same (w,h) pair is also warped into the **position** animation ("update for pos to work with size") | `WINDOW->positionAnimation()->setValueAndWarp(*COMPUTED);` | Hyprland-DefaultFloatingAlgorithm.cpp:64 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F24 | S292/D — the `center` rule recenters the box, using whatever size the box now has | `if (WINDOW->m_ruleApplicator->static_.center.value_or(false)) {` | Hyprland-DefaultFloatingAlgorithm.cpp:79 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F25 | S292/D — when no rule placed the window, the box is recentred | `if (!posOverridden && (!DESIRED_GEOM \|\| !DESIRED_GEOM->pos))` | Hyprland-DefaultFloatingAlgorithm.cpp:90 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F26 | S292/D — that recentring keeps `windowGeometry.size()` untouched: only x/y change | `windowGeometry = CBox{WORK_AREA.middle() - windowGeometry.size() / 2.F, windowGeometry.size()};` | Hyprland-DefaultFloatingAlgorithm.cpp:91 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F27 | S292/D — the work-area test is on the box **middle point** only | `WORK_AREA.containsPoint(windowGeometry.middle()))` | Hyprland-DefaultFloatingAlgorithm.cpp:95 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F28 | S292/D — the finished box (size untouched) is handed to the target | `target->setPositionGlobal(windowGeometry);` | Hyprland-DefaultFloatingAlgorithm.cpp:96 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F58 | S292/D — on a later map (not `m_firstMap`) the rule size is not re-read; the remembered floating size is used if it is > 5 px | `} else if (target->lastFloatingSize().x > 5 && target->lastFloatingSize().y > 5) {` | Hyprland-DefaultFloatingAlgorithm.cpp:85 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F59 | S292/D — the remembered size supplies the width (height on the next line) | `windowGeometry.w = target->lastFloatingSize().x;` | Hyprland-DefaultFloatingAlgorithm.cpp:86 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F64 | S292/D — `lastFloatingSize` is filled on target removal from the target's current box size | `target->rememberFloatingSize(target->position().size());` | Hyprland-DefaultFloatingAlgorithm.cpp:194 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F65 | S292/D — a work-area fitting helper exists (`fitBoxInWorkArea`), but `newTarget` never calls it; the only calls are in `movedTarget` (lines 160, 170) | `CBox CDefaultFloatingAlgorithm::fitBoxInWorkArea(const CBox& box, SP<ITarget> t) {` | Hyprland-DefaultFloatingAlgorithm.cpp:176 | f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91 |
| F29 | S293/E — the `STargetBox` overload is the real one; its `uint8_t` parameter is unnamed, i.e. the base class ignores the flags | `void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) {` | Hyprland-Target.cpp:10 | 49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06 |
| F30 | S293/E — the whole box (position and size) is stored in `m_box` | `m_box = box;` | Hyprland-Target.cpp:11 | 49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06 |
| F31 | S293/E — the stored logical box is rounded, so the size that survives is the rounded one | `m_box.logicalBox.round();` | Hyprland-Target.cpp:12 | 49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06 |
| F32 | S293/E — the `CBox` overload routes into the logical box and forwards the flags | `setPositionGlobal({.logicalBox = box}, flags);` | Hyprland-Target.cpp:17 | 49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06 |
| F63 | S293/E — the accessor the floating algorithm reads back is the logical box | `return m_box.logicalBox;` | Hyprland-Target.cpp:65 | 49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06 |
| F33 | S294/F — the window target overrides the setter and then runs the client-facing update | `void CWindowTarget::setPositionGlobal(const STargetBox& box, uint8_t flags) {` | Hyprland-WindowTarget.cpp:36 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F34 | S294/F — that update, `updatePos(flags)` | `updatePos(flags);` | Hyprland-WindowTarget.cpp:39 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F35 | S294/F — whether the client is configured is a flag, not unconditional | `const bool  CONFIGURECLIENT = !(flags & TARGET_UPDATE_NO_CLIENT_CONFIGURE);` | Hyprland-WindowTarget.cpp:50 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F36 | S294/F — the floating, non-fullscreen branch that a gkeep window takes | `if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) {` | Hyprland-WindowTarget.cpp:70 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F37 | S294/F — the logical box from the target is pushed into the window (`CWindow::setBox`, body not in these receipts) | `m_window->setBox(m_box.logicalBox);` | Hyprland-WindowTarget.cpp:71 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F38 | S294/F — then a size configure is sent to the client, unless the flag suppressed it | `m_window->sendWindowSize();` | Hyprland-WindowTarget.cpp:74 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F60 | S294/F — the floating branch returns before the tiled path, so the tiled clamps below (F43/F44) never run for a floating window | `return;` | Hyprland-WindowTarget.cpp:77 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F39 | S294/F — the min/max clamp function that *is* in the file, applied to desired geometry only | `Vector2D CWindowTarget::clampSizeForDesired(const Vector2D& size) const {` | Hyprland-WindowTarget.cpp:297 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F40 | S294/F — min clamp of a desired size | `newSize = newSize.clamp(*m);` | Hyprland-WindowTarget.cpp:300 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F41 | S294/F — max clamp, with `MIN_WINDOW_SIZE` as the lower bound of the clamp call | `newSize = newSize.clamp(Vector2D{MIN_WINDOW_SIZE, MIN_WINDOW_SIZE}, *m);` | Hyprland-WindowTarget.cpp:302 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F42 | S294/F — the client's desired size is put through that clamp inside `desiredGeometry()` | `requested.size = clampSizeForDesired(DESIRED_GEOM.size());` | Hyprland-WindowTarget.cpp:313 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F43 | S294/F — the tiled branch clamps size only behind `misc:size_limits_tiled` | `if (*PCLAMP_TILED) {` | Hyprland-WindowTarget.cpp:227 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F44 | S294/F — that tiled clamp of the computed size | `calcSize = calcSize.clamp(minSize, maxSize);` | Hyprland-WindowTarget.cpp:231 | 8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d |
| F45 | S295/G — `size(GEOMETRIC_GOAL)` returns the animation variable's **goal**, not its current value | `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` | Hyprland-GeometricMovableAnimated.cpp:19 | 649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d |
| F46 | S295/G — `GEOMETRIC_CURRENT` is the other accessor and is not what `clients -j` prints | `case IGeometric::GEOMETRIC_CURRENT: return m_realSize->value();` | Hyprland-GeometricMovableAnimated.cpp:20 | 649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d |
| F47 | S295/G — `resize()` writes the animation variable (via its `operator=`), it does not touch the surface | `*m_realSize = x;` | Hyprland-GeometricMovableAnimated.cpp:40 | 649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d |
| F48 | S295/G — `setBox()` writes position and size together; this is the call S294:F37 arrives at | `*m_realSize     = x.size();` | Hyprland-GeometricMovableAnimated.cpp:45 | 649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d |
| F49 | S295/G — `finishAnimation()` warps the size variable, i.e. jumps goal and current together | `m_realSize->warp();` | Hyprland-GeometricMovableAnimated.cpp:50 | 649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d |
| F50 | S295/G — the size animation variable is the same member that S292:F18 and S292:F53 warp | `return m_realSize;` | Hyprland-GeometricMovableAnimated.cpp:58 | 649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d |
| F51 | S296/H — in the JSON template `size` is a two-element array | `"size": [{}, {}],` | Hyprland-HyprCtl.cpp:395 | 798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa |
| F52 | S296/H — `floating` is emitted as a single JSON scalar next to it | `"floating": {},` | Hyprland-HyprCtl.cpp:400 | 798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa |
| F53 | S296/H — the two numbers filled into `size` are the window's `GEOMETRIC_GOAL` size, cast with `sc<int>` | `sc<int>(w->position(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x),` | Hyprland-HyprCtl.cpp:427 | 798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa |
| F54 | S296/H — the second size component, i.e. the height, followed by the workspace id | `sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), w->m_workspace ? w->workspaceID() : WORKSPACE_INVALID,` | Hyprland-HyprCtl.cpp:428 | 798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa |
| F55 | S296/H — the plain-text (`clients`, non-JSON) format prints the same GOAL-based pair | `sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x), sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y),` | Hyprland-HyprCtl.cpp:448 | 798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa |

## What the source does NOT say

Each item below is an *absence in the pinned receipts*, checked by reading the whole file, not a claim about
Hyprland as a whole. Do not let the entry assert these as sourced.

1. **Whether the client may decline the configure.** `sendWindowSize()` is called (S294:F38) but its body is
   not in any pinned receipt; nothing in S293–S296 observes the client's commit, a `xdg_surface.configure` ack,
   or a re-request. The chain stops at "the compositor asks" — "the client obeys" is not sourced here.
2. **What `CWindow::setBox` does.** The chain S294:F37 → a `CWindow` method is a gap: the pinned `setBox` is
   `CGeometricMovableAnimated::setBox` (S295:F48), an animation-variable write. `CWindow` itself (surface size,
   `m_pendingReportedSize`, damage) is not pinned.
3. **`PHLANIMVAR` semantics.** `goal()`, `value()`, `operator=`, `warp()`, animation duration and curve all
   live in hyprutils; the receipts only show that the two accessors differ (S295:F45/F46) and that
   `*m_realSize = x` (S295:F47) and `warp()` (S295:F49) are distinct operations.
4. **How `size 420 500` in the config file becomes a `Math::SExpressionVec2`.** The rule parser is not pinned;
   S291 only shows the applicator receiving an already-built `SExpressionVec2`. Accepted value *forms*
   therefore cannot be enumerated from these receipts — only that the applicator takes exactly that variant,
   that empty means "no size" (S291:F8), and that a non-empty one is stored unevaluated (S291:F9).
5. **`calculateExpression`.** Not pinned. The mapping `expr → (w,h)` (S292:F20–F22) is shown, but nothing here
   says that a literal `420 500` yields `(420,500)`.
6. **Whether the rule size is clamped by min/max or by the work area.** No clamp call appears anywhere in
   `newTarget`; `clampSizeForDesired` (S294:F39–F42) is only applied to the *desired* geometry the rule then
   overwrites, and `fitBoxInWorkArea` is not called from `newTarget` (S292:F65). A 420×500 rule size on a
   smaller or partially covered work area is not shown to be reduced. Only the *position* is adjusted
   (S292:F25–F28), and only when the box's middle point leaves the work area (S292:F27).
7. **Later user resize / float toggle.** `movedTarget` re-applies `lastFloatingSize` through `fitBoxInWorkArea`
   (S292 file lines 160 and 170); `resizeTarget` instead adds the delta to the *current* box and calls
   `setPositionGlobal(pos)` (same file, lines 198–203), so it never consults `static_.size`;
   `rememberFloatingSize` is written on target removal (S292:F64). The interactive-resize entry points, the drag
   controller, and any "user resize beats the rule" policy are outside these receipts, so permanence cannot be
   asserted from them.
8. **Monitor change.** `movedTarget` re-homes a box using `State::monitorState()->query().vec(OLD_POS)` (same
   file, lines 162–170); nothing in the pinned files re-reads `static_.size` on monitor or workspace migration —
   the only read is inside the `m_firstMap` branch (S292:F57). Whether re-mapping triggers `newTarget` again is
   not shown.
9. **Scaling / coordinate space.** `sc<int>` (S296:F53–F55) is used without showing its rounding rule, and
   nothing in S296 shows logical-vs-pixel scaling; the `toLogical` lambda (XWayland `force_zero_scaling`,
   `Hyprland-WindowTarget.cpp:334-337`) divides only the *desired* geometry by the monitor scale and has no
   counterpart on the `hyprctl` output path.
10. **Which of the four rule effects the host file actually uses.** This seat's receipts contain no host config;
    the `float`/`center`/`size`/class text is S297's (host-gkeep.conf), not mine to quote.
11. **Rule ordering / precedence between `float` and a later `tile` rule.** S291:F4/F5 both write
    `static_.floating`; the enclosing loop is `for (const auto& effectData : rule->effects())`
    (`Hyprland-WindowRuleApplicator.cpp:379`), and no receipt shows what happens when one rule carries both
    effects, or which of two matching rules is applied last.
12. **`MIN_WINDOW_SIZE` value** (S294:F41) and the body of `clampWindowSize` (S291:F13/F16) are not in the
    receipts.

## Retained evidence in this seat directory

- `facts.md` (this file)
- `verify-facts.py` — the grep-style checker (fixed-string per line, sha256 re-check, ≤25-word check)
- `verify-output.txt` — its output for all 65 rows (`rows=65 failures=0 distinct_receipts=7`)

No file outside this seat directory was written. No scratch tree was needed (`/fast/scratch/hyaku/mado-r43/ExecSrcChain/`
was never created). No compositor verb was issued; only file reads.
