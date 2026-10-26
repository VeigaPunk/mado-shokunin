# A quotation record

source: S295 - receipt
source: S290 - receipt
source: S155 - receipt
source: S291 - receipt
source: S292 - receipt
source: S293 - receipt
source: S294 - receipt
source: S158 - receipt
source: S297 - receipt
source: S296 - receipt
verified-at: 2026-10-26
recheck: 90d

S295 `windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$` (host-gkeep.conf:4).
S290 `return re2::RE2::FullMatch(other, *m_regex) != m_negative;` (Hyprland-RegexMatchEngine.cpp:16).
S155 `static_.size = expr;` (Hyprland-WindowRuleApplicator.cpp:426).
S291 `const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);` (Hyprland-DefaultFloatingAlgorithm.cpp:56).
S292 `void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) {` (Hyprland-Target.cpp:10).
S293 `if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) { m_window->setBox(m_box.logicalBox);` (Hyprland-WindowTarget.cpp:70).
S294 `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` (Hyprland-GeometricMovableAnimated.cpp:19).
S158 `sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), w->m_workspace ? w->workspaceID() : WORKSPACE_INVALID, escapeJSONStrings(!w->m_workspace ? "" : w->m_workspace->m_name),` (Hyprland-HyprCtl.cpp:428).
S297 `window.set_default_size(420, 500) self.board = Board(window)` (gkeep-ui-excerpt.py:33).
S296 `"class": "chromium", "floating": false,` (host-clients-r43.json:50).

host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$
host clients total=4 floating=0 gkeep=0
gkeep request default_size=420x500 application_id=org.omarchy.gkeep


## §6 An observation that is not in this lane

In the isolated oracle run recorded at
`.ufo/waves/round-43/w2/ExecDoNothingV2/oracle-absent.txt` the same client reported
`size 420 500` with the size line removed from the config, which shows the client is
the origin of the size; the file is kept outside the lane by the oracle seat.

