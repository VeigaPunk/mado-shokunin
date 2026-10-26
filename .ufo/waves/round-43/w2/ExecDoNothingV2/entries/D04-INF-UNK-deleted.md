# What sets the size of the host's gkeep window: the rule text, an anchored match, the floating first-map branch, and the GOAL that `hyprctl clients -j` prints

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
recheck: 90d - re-pull the seven Hyprland files at efb5099, re-copy the three own-work receipts and re-run the counter; a Hyprland tag after v0.56.2 or an edit of ~/.config/hypr/gkeep.conf is the earlier trigger
ground: why a gkeep window on this host should open floating at 420x500, which link of the chain decides it, and what `hyprctl clients -j` can and cannot tell about it
Lane: mado-shokunin. Round: 43.
assimilated-from: merge/mado/knowledge/corpus/knowledge/gkeep-size-to-real-size-r11.md (its four-link chain, re-derived at the host's own commit; the refused staged files and their flip conditions are in corpus/lessons/round-43.md)

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| Does the host's rule text ask for a floating, centred 420x500 gkeep window? | the config copy: one `size`, one `float on`, one `center on` line, one class regex | OBS |
| Does the rule's regex match the app's own id? | the anchored match function, the regex, the app's `application_id` | OBS (source) + INF (the join) |
| What box does a first-mapped floating gkeep window get? | the floating algorithm's first-map branch, which evaluates the stored size expression | OBS (source); OBS in an isolated oracle, not on the host session |
| What does `hyprctl clients -j` put in `size`? | the JSON builder, which reads the GOAL of the animated size | OBS |
| Is the GOAL the size drawn on screen? | the animated type keeps GOAL apart from CURRENT; no read verb exposes CURRENT | UNK on the host |

## §1 The rule as text, and the match

**OBS** S295 - the host declares exactly one size for the class: `windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$` (host-gkeep.conf:4); the same file holds one `float on` line (line 2) and one `center on` line (line 3) for the same regex, and its comment says it avoids the floating-window tag on purpose.

**OBS** S290 - the class test is anchored on the whole string: `return re2::RE2::FullMatch(other, *m_regex) != m_negative;` (Hyprland-RegexMatchEngine.cpp:16); a regex that starts with `negative:` is stripped of that prefix and the result is inverted (constructor, lines 7-8).


## §2 What the rule becomes and who reads it

**OBS** S155 - the size effect is kept as an unevaluated expression: `static_.size = expr;` (Hyprland-WindowRuleApplicator.cpp:426), in the arm that reads a `Math::SExpressionVec2` and resets the slot when the expression is empty.

**OBS** S291 - the default floating algorithm evaluates that expression only inside its first-map branch: `const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);` (Hyprland-DefaultFloatingAlgorithm.cpp:56), and writes the result into the new window's geometry width and height.

**OBS** S292 - the computed box is stored on the layout target: `void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) {` (Hyprland-Target.cpp:10) assigns the box and rounds its logical and visual parts.

**OBS** S293 - for a floating, non-fullscreen window the stored box is handed to the window itself: `if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) { m_window->setBox(m_box.logicalBox);` (Hyprland-WindowTarget.cpp:70-71).


## §3 What the compositor prints

**OBS** S294 - a size read asks for one of two values of the animated size, and the goal is its own accessor: `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` (Hyprland-GeometricMovableAnimated.cpp:19); GEOMETRIC_CURRENT returns the current value instead (line 20).

**OBS** S158 - `hyprctl clients -j` fills `size` from that goal: `sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), w->m_workspace ? w->workspaceID() : WORKSPACE_INVALID, escapeJSONStrings(!w->m_workspace ? "" : w->m_workspace->m_name),` (Hyprland-HyprCtl.cpp:428-429), the width coming from the same call one line earlier; the plain-text formatter reads the same goal at line 448.


## §4 The client's half

**OBS** S297 - the app asks for the same size the rule asks for: `window.set_default_size(420, 500) self.board = Board(window)` (gkeep-ui-excerpt.py:33-34), on a `Gtk.ApplicationWindow` of the application whose id is `org.omarchy.gkeep` (line 6).


## §5 Today's census on the host

**OBS** S296 - the pinned dump holds four mapped clients and none is floating, for example `"class": "chromium", "floating": false,` (host-clients-r43.json:50-51); no object has the class `org.omarchy.gkeep`.


Census (recomputed by the C2 counter from the three own-work receipts):

host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$
host clients total=4 floating=0 gkeep=0
gkeep request default_size=420x500 application_id=org.omarchy.gkeep

## What this entry does not establish


