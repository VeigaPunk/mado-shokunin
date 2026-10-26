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
assimilated-from: merge/mado/knowledge/corpus/knowledge/gkeep-size-to-real-size-r11.md (its chain rule -> floating algorithm -> target box -> window box and animated size, re-derived at the host's own commit; the refused staged files and their flip conditions are in corpus/lessons/round-43.md)

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| Does the host's rule text ask for a floating, centred 420x500 gkeep window? | the config copy: one `size`, one `float on`, one `center on` line, one class regex | OBS |
| Does the rule's regex match the app's own id? | the anchored match function, the regex, the app's `application_id` | OBS (source) + INF (the join) |
| What box does a newly mapped floating gkeep window get? | the floating algorithm's map branch, which evaluates the stored size expression | OBS (source); OBS in an isolated oracle with a stand-in client, not on the host session |
| What does `hyprctl clients -j` put in `size`? | the JSON builder, which reads the GOAL of the animated size | OBS |
| Is the GOAL the size drawn on screen? | the animated type keeps GOAL apart from CURRENT; no geometry read verb exposes CURRENT | UNK on the host |
| Has a gkeep window been seen at 420x500 on this host session? | today's census: four mapped clients, none floating, none of them gkeep | UNK |

## §1 The rule as text, and the match

**OBS** S295 - the host declares exactly one size for the class: `windowrule = size 640 720, match:class ^(org.omarchy.gkeep)$` (host-gkeep.conf:4); the same file holds one `float on` line (line 2) and one `center on` line (line 3) for the same regex, and its comment says it avoids the floating-window tag on purpose.

**OBS** S290 - the class test is anchored on the whole string: `return re2::RE2::FullMatch(other, *m_regex) != m_negative;` (Hyprland-RegexMatchEngine.cpp:16); a regex that starts with `negative:` is detected in the constructor (lines 7-8) and stripped with `substr(9)` (line 9), and the comparison with that flag on line 16 inverts the result.

**INF** With FullMatch, the host regex `^(org.omarchy.gkeep)$` matches the class `org.omarchy.gkeep` and nothing longer (`org.omarchy.gkeep2` does not match; the unescaped dots match any character except a newline under RE2's default options, so a class such as `orgXomarchy.gkeep` would). The `^`/`$` anchors are redundant under FullMatch but harmless.

## §2 What the rule becomes and who reads it

**OBS** S155 - the size effect is kept as an unevaluated expression: `static_.size = expr;` (Hyprland-WindowRuleApplicator.cpp:426), in the arm that reads a `Math::SExpressionVec2` and resets the slot when the expression is empty.

**OBS** S291 - the default floating algorithm evaluates that expression only inside its first-map branch: `const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);` (Hyprland-DefaultFloatingAlgorithm.cpp:56), and writes the result into the new window's geometry width and height.

**OBS** S292 - the computed box is stored on the layout target: `void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) {` (Hyprland-Target.cpp:10) assigns the box and rounds its logical and visual parts.

**OBS** S293 - for a floating, non-fullscreen window the stored box is handed to the window itself: `if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) { m_window->setBox(m_box.logicalBox);` (Hyprland-WindowTarget.cpp:70-71).

**OBS** The box reaches the animated size the dump reads: `setBox` writes `*m_realSize     = x.size();` (Hyprland-GeometricMovableAnimated.cpp:45), the link between the window's box and the goal reported in §3.

**INF** A tiled window never reaches the floating branch above, but the rule is not inert for it: at map, the non-floating arm of `mapWindow` evaluates the same `static_.size` expression and stores it with `m_target->setPseudoSize(*COMPUTED);` (`Window.cpp:2402-2408` at efb5099, pinned at `.ufo/waves/round-43/w1/ExecGoalVsValue/pins/window.cpp`), and that pseudo size decides the box only when the target is pseudo-tiled. Without `float on` and without `pseudo`, the tiler decides the box (the oracle's no-float case reported 918x498, below). Basis: `.ufo/waves/round-43/w2/CritEntryInf/findings.md` F1.

## §3 What the compositor prints

**OBS** S294 - a size read asks for one of two values of the animated size, and the goal is its own accessor: `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` (Hyprland-GeometricMovableAnimated.cpp:19); GEOMETRIC_CURRENT returns the current value instead (line 20).

**OBS** S158 - `hyprctl clients -j` fills `size` from that goal: `sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), w->m_workspace ? w->workspaceID() : WORKSPACE_INVALID, escapeJSONStrings(!w->m_workspace ? "" : w->m_workspace->m_name),` (Hyprland-HyprCtl.cpp:428-429), the width coming from the same call one line earlier; the plain-text formatter reads the same goal at line 448.

**INF** So a `clients -j` size equal to the rule's size says that the compositor's target equals the rule, not that the window is drawn at that size at that moment: while the open animation runs, the current value differs from the goal (the host's `windowsIn` animation uses `popin 87%`, `.ufo/waves/round-43/w1/ExecGoalVsValue/finding.md`), and no geometry read verb of the request socket (`clients`, `activewindow`, `getprop`) exposes the current value.

## §4 The client's half

**OBS** S297 - the app asks for the same size the rule asks for: `window.set_default_size(640, 720) self.board = Board(window)` (gkeep-ui-excerpt.py:33-34), on a `Gtk.ApplicationWindow` (line 31) of the application whose id is `org.omarchy.gkeep` (line 6).

**INF** Two agreeing numbers are not one observation: the client's default size and the rule's size coincide, so a 420x500 report alone cannot say which of the two set it.

**OBS** (isolated oracle, not the host session) In an adaptation of the round-27 bubblewrap oracle (a Hyprland 0.56.2 at efb5099 nested under tinywl, with a headless output added inside the nested instance), a small shm stand-in client (`gkeep-shm.c`, app id `org.omarchy.gkeep`, one 200x200 buffer, no size request) reported `"size": [420, 500]`, `"floating": true` under the host's three rules; with the size line removed a stand-in client reported its own 200x200 buffer, with `size 300 300` it reported 300x300, and with the `float on` line removed it was tiled at 918x498 (`.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt`, `10-cases.txt`; the 200x200 control ran a separate build of the stand-in, `.ufo/waves/round-43/w2/CritOracleClaim/findings.md`). In that oracle, for a client that asks for no size, the rule is the origin of 420x500; the real gkeep app was not run.

## §5 Today's census on the host

**OBS** S296 - the pinned dump holds four mapped clients and none is floating, for example `"class": "chromium", "floating": false,` (host-clients-r43.json:50-51); no object has the class `org.omarchy.gkeep`.

**UNK** No gkeep window was open when the dump was taken, so this host session has not been seen to give gkeep 420x500; `tools/mado-geometry.py` answers `NO_MATCHING_CLIENT` today (`.ufo/waves/round-43/receipts/live-geometry-host.txt`) and is the read-only check to run while gkeep is open.

Census (recomputed by the C2 counter from the three own-work receipts):

host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$
host clients total=4 floating=0 gkeep=0
gkeep request default_size=420x500 application_id=org.omarchy.gkeep

## What this entry does not establish

- The current (drawn) size of a gkeep window at any moment on the host; the GOAL is what every read verb reports.
- What happens while the window stays mapped (a user resize, a monitor change, a later rule reload): the floating branch quoted above runs inside `mapWindow`, whose `m_firstMap` flag is set on every map and cleared at its end (`Window.cpp:2079`, `:2513` in the pinned copy), so an unmap and remap re-applies the rule; nothing in the pins re-evaluates it while the window stays mapped (`.ufo/waves/round-43/w2/CritEntryInf/findings.md` F2).
- Behaviour on any Hyprland other than 0.56.2 at `efb5099`.
