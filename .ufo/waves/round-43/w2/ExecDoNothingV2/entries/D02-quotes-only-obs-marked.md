# What sets the size of the host's gkeep window

source: S295 - own-work: byte copy of ~/.config/hypr/gkeep.conf, pinned at .ufo/waves/round-43/fetch/host-gkeep.conf - the host's three rules for the class
source: S290 - hyprwm/Hyprland src/desktop/rule/matchEngine/RegexMatchEngine.cpp @ efb5099 (v0.56.2) - the match function: RE2 FullMatch and the `negative:` prefix
source: S155 - hyprwm/Hyprland src/desktop/rule/windowRule/WindowRuleApplicator.cpp @ efb5099 (held row) - the static arm that stores a size rule as an expression
source: S291 - hyprwm/Hyprland src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp @ efb5099 (v0.56.2) - the first-map branch that evaluates the stored size
source: S292 - hyprwm/Hyprland src/layout/target/Target.cpp @ efb5099 (v0.56.2) - where a target keeps its box
source: S293 - hyprwm/Hyprland src/layout/target/WindowTarget.cpp @ efb5099 (v0.56.2) - the floating branch that hands the box to the window
source: S294 - hyprwm/Hyprland src/desktop/view/types/GeometricMovableAnimated.cpp @ efb5099 (v0.56.2) - GEOMETRIC_GOAL against GEOMETRIC_CURRENT on the animated size
source: S158 - hyprwm/Hyprland src/debug/HyprCtl.cpp @ efb5099 (held row) - the `clients -j` size fields, filled from the GOAL
source: S297 - own-work: lines 446-488 of ~/Projects/gkeep/gkeep/ui.py at gkeep 133b867, pinned at .ufo/waves/round-43/fetch/gkeep-ui-excerpt.py - the app's id and default size
source: S296 - own-work: `hyprctl clients -j` reduced to address/mapped/class/floating/size/at/monitor, pinned at .ufo/waves/round-43/fetch/host-clients-r43.json - today's client census
verified-at: 2026-10-26
recheck: 90d

**OBS** S295 - `windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$` (host-gkeep.conf:4);
**OBS** S290 - `return re2::RE2::FullMatch(other, *m_regex) != m_negative;` (Hyprland-RegexMatchEngine.cpp:16);
**OBS** S155 - `static_.size = expr;` (Hyprland-WindowRuleApplicator.cpp:426);
**OBS** S291 - `const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);` (Hyprland-DefaultFloatingAlgorithm.cpp:56);
**OBS** S292 - `void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) {` (Hyprland-Target.cpp:10);
**OBS** S293 - `if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) { m_window->setBox(m_box.logicalBox);` (Hyprland-WindowTarget.cpp:70);
**OBS** S294 - `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` (Hyprland-GeometricMovableAnimated.cpp:19);
**OBS** S158 - `sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), w->m_workspace ? w->workspaceID() : WORKSPACE_INVALID, escapeJSONStrings(!w->m_workspace ? "" : w->m_workspace->m_name),` (Hyprland-HyprCtl.cpp:428);
**OBS** S297 - `window.set_default_size(420, 500) self.board = Board(window)` (gkeep-ui-excerpt.py:33);
**OBS** S296 - `"class": "chromium", "floating": false,` (host-clients-r43.json:50);

host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$
host clients total=4 floating=0 gkeep=0
gkeep request default_size=420x500 application_id=org.omarchy.gkeep

