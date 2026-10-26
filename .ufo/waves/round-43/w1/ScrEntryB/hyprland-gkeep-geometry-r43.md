# What determines the size of the host's gkeep window, end to end: rule text, an anchored match, the floating algorithm, and the GOAL `hyprctl clients -j` prints

Lane: mado-shokunin. Round: 43.
ground: P6 - the host's screen and idle behaviour, through its window-sizing rules
assimilated-from: merge/mado/knowledge/corpus/knowledge/gkeep-size-to-real-size-r11.md (the four-link chain, re-derived here at the host's own commit; the lesson's Gate records the admitted and the refused staged files)
source: S290 - hyprwm/Hyprland src/desktop/rule/matchEngine/RegexMatchEngine.cpp @ efb5099 (v0.56.2) - the whole match function: FullMatch over the whole string, and the `negative:` prefix that inverts it
source: S291 - hyprwm/Hyprland src/desktop/rule/windowRule/WindowRuleApplicator.cpp @ efb5099 (v0.56.2) - the static arm that stores the size effect as an expression
source: S292 - hyprwm/Hyprland src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp @ efb5099 (v0.56.2) - the first-map branch that evaluates the rule's size
source: S293 - hyprwm/Hyprland src/layout/target/Target.cpp @ efb5099 (v0.56.2) - where a target's box is stored
source: S294 - hyprwm/Hyprland src/layout/target/WindowTarget.cpp @ efb5099 (v0.56.2) - the window target: the desired geometry and the box pushed onto the window
source: S295 - hyprwm/Hyprland src/desktop/view/types/GeometricMovableAnimated.cpp @ efb5099 (v0.56.2) - GEOMETRIC_GOAL against GEOMETRIC_CURRENT on the animated size
source: S296 - hyprwm/Hyprland src/debug/HyprCtl.cpp @ efb5099 (v0.56.2) - the `clients -j` size fields, filled from the GOAL
source: S297 - own-work: byte copy of ~/.config/hypr/gkeep.conf, pinned at .ufo/waves/round-43/fetch/host-gkeep.conf - the host's three rules for the class
source: S298 - own-work: `hyprctl clients -j` reduced to address/mapped/class/floating/size/at/monitor, pinned at .ufo/waves/round-43/fetch/host-clients-r43.json - today's client census
source: S299 - own-work: lines 446-488 of ~/Projects/gkeep/gkeep/ui.py at gkeep 133b867, pinned at .ufo/waves/round-43/fetch/gkeep-ui-excerpt.py - the application id and the default size
verified-at: 2026-10-26
recheck: 30d - re-pull the seven pinned files at v0.56.2 and re-copy the three own-work receipts, then re-run the counter; a Hyprland tag after v0.56.2 or a change to the host's gkeep rule file is the earlier trigger

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| Does the host's rule text ask for a 420x500 gkeep window? | the config copy: exactly one `size` rule, one `float on`, one `center on`, same class | OBS |
| Does the rule's class regex match the app's own id? | the anchored match function, the rule's regex, the app's `application_id` | OBS |
| What size does a first-mapped gkeep window get? | the floating algorithm's first-map branch, evaluating the rule's size expression | INF |
| What does `hyprctl clients -j` put in `size`? | the JSON fill, taken from the geometric GOAL of the animated size | OBS |
| Is that the size currently drawn on screen? | the animated type keeps GOAL apart from CURRENT; nothing read compares them live | UNK |
| Has a gkeep window been seen at 420x500 on this host? | today's census: four mapped clients, none gkeep, none floating | UNK |

## §1 The rule as text

**OBS** S297 - the host declares exactly one size for the class: `windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$` (host-gkeep.conf:4), with one `float on` and one `center on` line for the same regex in the same file.

**OBS** S290 - the class test is anchored: `re2::RE2::FullMatch(other, *m_regex) != m_negative` (Hyprland-RegexMatchEngine.cpp:16), so the whole class string must match the regex, and the `negative:` prefix (line 7) strips nine characters and inverts the result.

## §2 What the rule becomes

**OBS** S291 - the size effect is stored as an expression, not as a number: `static_.size = expr;` (Hyprland-WindowRuleApplicator.cpp:426), the arm reading a `Math::SExpressionVec2` and resetting the slot when the expression is empty.

**OBS** S292 - the floating algorithm evaluates that expression only on the window's first map: `const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);` (Hyprland-DefaultFloatingAlgorithm.cpp:56), writing the result into the window geometry.

**OBS** S293 - the resulting box is stored on the target: `m_box = box;` (Hyprland-Target.cpp:11), with the logical and visual boxes rounded in the same call.

**INF** The stored box reaches the window through `m_window->setBox(m_box.logicalBox);` (Hyprland-WindowTarget.cpp:71), so the geometry the algorithm computed becomes the window's geometric size; the animated type then holds it as a goal and as a current value.

## §3 What the compositor prints

**OBS** S295 - the reported number is the goal: `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` (Hyprland-GeometricMovableAnimated.cpp:19), a separate accessor from GEOMETRIC_CURRENT, which returns the current value.

**OBS** S296 - `hyprctl clients -j` fills `size` from that goal: `sc<int>(w->position(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x), sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y),` (Hyprland-HyprCtl.cpp:427), and the text format carries the same two size arguments at :448.

**OBS** S294 - the target's desired geometry is the client's own ask: `std::expected<SGeometryRequested, eGeometryFailure> CWindowTarget::desiredGeometry()` (Hyprland-WindowTarget.cpp:306) seeds `requested.size` from the client's geometry before a stored or persistent size replaces it.

## §4 The client's half

**OBS** S299 - the app asks for the same size the rule asks for: `window.set_decorated(False) window.set_default_size(420, 500)` (gkeep-ui-excerpt.py:32), on a `Gtk.ApplicationWindow` titled gkeep inside the application whose id is org.omarchy.gkeep.

**INF** Two agreeing numbers are not one observation: the client's request bounds what it will accept, the rule's expression decides the box the compositor adopts, and the field the dump prints is the animation's goal - so none of the three alone licenses a claim about the drawn window.

## §5 Today's census

**OBS** S298 - the pinned dump holds four mapped clients, none of them floating: `"floating": false, "size": [ 1720, 1414 ],` (host-clients-r43.json:6), and every entry carries the same tiling box.

**UNK** No gkeep client appears in the dump, so the rendered geometry of a gkeep window stays unobserved: whether it receives 420x500 on this host, and whether its GOAL ever equals its CURRENT value, are not established by any receipt pinned this round.

Census (recomputed by the counter from the three own-work receipts):

host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$
host clients total=4 floating=0 gkeep=0
gkeep request default_size=420x500 application_id=org.omarchy.gkeep
