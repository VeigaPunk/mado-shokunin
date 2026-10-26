# The size of the gkeep window, end to end: a host rule, an anchored match, an expression the floating algorithm consumes, an animated goal, and the number `hyprctl` prints

source: S290 - hyprwm/Hyprland v0.56.2 src/desktop/rule/matchEngine/RegexMatchEngine.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f - the whole-string RE2 matcher and its `negative:` prefix
source: S291 - hyprwm/Hyprland v0.56.2 src/desktop/rule/windowRule/WindowRuleApplicator.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f - where a matching rule's effects are stored: `static_.size` as an expression, `static_.floating` as a bool
source: S292 - hyprwm/Hyprland v0.56.2 src/layout/algorithm/floating/default/DefaultFloatingAlgorithm.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f - the only site in these receipts that consumes `static_.size`
source: S293 - hyprwm/Hyprland v0.56.2 src/layout/target/Target.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f - `ITarget::setPositionGlobal`, the target's box storage
source: S294 - hyprwm/Hyprland v0.56.2 src/layout/target/WindowTarget.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f - the window target: box to window, size to client
source: S295 - hyprwm/Hyprland v0.56.2 src/desktop/view/types/GeometricMovableAnimated.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f - `size(GEOMETRIC_GOAL)` is the animation goal, not the current value
source: S296 - hyprwm/Hyprland v0.56.2 src/debug/HyprCtl.cpp @ efb50993780079460b0cbed1363e2166a2de1d9f - the `clients -j` emitter and the value it prints as `size`
source: S297 - own-work: `~/.config/hypr/gkeep.conf` byte copy, saved at .ufo/waves/round-43/fetch/host-gkeep.conf (sha256 3726e488…)
source: S298 - own-work: `hyprctl clients -j` reduced to address/mapped/class/floating/size/at/monitor, saved at .ufo/waves/round-43/fetch/host-clients-r43.json (sha256 21db902e…)
source: S299 - own-work: `~/Projects/gkeep/gkeep/ui.py` lines 446-488 (end of file) at 133b867, saved at .ufo/waves/round-43/fetch/gkeep-ui-excerpt.py (sha256 3695b788…)
verified-at: 2026-10-26
recheck: 90d - re-pull the seven pinned files at v0.56.2 and re-read the host rule file and one `hyprctl clients -j` dump; a Hyprland tag after v0.56.2 or a gkeep release is the earlier trigger
ground: what determines the size of the host's gkeep window, end to end - the rule text an operator writes, the expression the floating algorithm consumes, the box two targets store, and the animated goal one command prints
assimilated-from: merge/mado/knowledge/corpus/knowledge/gkeep-rendered-geometry-chain-r9.md (the chain this entry sources end to end; the staged round-9-14 files rest on artifacts this round did not re-fetch and are listed with reasons in `corpus/lessons/round-43.md` § Gate)
Lane: mado-shokunin. Round: 43.

## §1 The host's rule text

**OBS** S297 - the host declares three rules for one class, quoted here as one contiguous span: `windowrule = float on, match:class ^(org.omarchy.gkeep)$ windowrule = center on, match:class ^(org.omarchy.gkeep)$ windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$` (`host-gkeep.conf:2`). The file's own first line is a comment: the desktop's floating-window tag would size this window at 875×600, so the rule exists to override it.

host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$

**INF** The three effects are the whole declaration: a float effect, a centre effect and a size effect, each matched by the same `match:class` regex, and nothing in the file names a monitor, a workspace or a title. `Basis:` the three lines and the absence of any other `windowrule` in S297.

## §2 The match: an anchored RE2 over the whole class string

**OBS** S290 - `return re2::RE2::FullMatch(other, *m_regex) != m_negative;` (`Hyprland-RegexMatchEngine.cpp:16`). The constructor keeps the regex in a `re2::RE2` and, for a string starting `negative:`, strips nine characters and sets a flag that inverts the result; `match` returns the inversion of `RE2::FullMatch`.

**INF** Because the engine uses `FullMatch`, a rule matches only when the pattern consumes the entire class string, so the host's `^(org.omarchy.gkeep)$` anchors are redundant under this engine and a bare `org.omarchy.gkeep` would match the same class. `Basis:` S290's single `match` expression.

**UNK** Which string is handed to `match` as the class. The receipts hold the matcher and the applicator that calls it, not the window's class getter, so whether the compared value is the Wayland app id or an X11 `WM_CLASS` is not established here.

## §3 The effects: an expression and a bool, reset on every pre-read

**OBS** S291 - the size effect stores the rule's value as a `Math::SExpressionVec2` rather than a pair of integers: `if (expr.empty()) static_.size.reset(); else static_.size = expr;` (`Hyprland-WindowRuleApplicator.cpp:423`). The same switch stores the float effect in `static_.floating` (`Hyprland-WindowRuleApplicator.cpp:390`), and `readStaticRules` clears `static_` before it iterates the registry (line 487), applying `applyStaticRule` to every matching window rule in registry order (lines 492-509).

**INF** With more than one matching rule the last one applied owns the value, because each match overwrites the same struct fields in one loop. With the host's single rule per class the order does not matter. `Basis:` S291's `readStaticRules` loop.

**INF** The size is a static effect: the dynamic switch in the same file has cases for rounding, opacity, max/min size, border size and the rest, but no case for the size effect, so a rule's size is read at pre-read time and not re-applied by the dynamic path. `Basis:` S291's two switches.

## §4 The consumption: one site, first map, floating only

**OBS** S292 - the floating algorithm evaluates the stored expression at first map: `if (WINDOW->m_ruleApplicator->static_.size) { const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);` (`Hyprland-DefaultFloatingAlgorithm.cpp:55`). The computed x and y become `windowGeometry.w` and `windowGeometry.h` (lines 60-61) and the position animation is warped to the same vector (line 64); the whole block is inside `if (target->window() && target->window()->m_firstMap)` (line 49), and when the target reports no desired geometry the algorithm starts from `DEFAULT_SIZE = {640, 400}` (line 16) centred on the work area (line 36). The centre effect then centres the computed box on the work area (lines 79-84).

**INF** The rule's size therefore cannot reach a tiled window and cannot reach a window after its first map: the branch is in the floating algorithm's `newTarget` and gated on `m_firstMap`. `Basis:` S292's `newTarget` structure, S291's float effect (§3).

**UNK** Whether a window that is floated *after* its first map ever passes through this block again. Nothing in these receipts shows a re-entry, and no live window was toggled this round.

## §5 The storage and the configure

**OBS** S293 - the box the algorithm computed is stored on the target, rounded on both boxes: `void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) { m_box = box; m_box.logicalBox.round(); m_box.visualBox.round();` (`Hyprland-Target.cpp:10`).

**OBS** S294 - for a floating window that is not fullscreen, the target's logical box becomes the window's box and the client is sent a size: `if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) { m_window->setBox(m_box.logicalBox); if (CONFIGURECLIENT) m_window->sendWindowSize();` (`Hyprland-WindowTarget.cpp:70`). The tiled path is a separate branch that computes gaps, single-window ratio padding, pseudo size and the `misc:size_limits_tiled` clamp, and also calls `sendWindowSize` (line 256).

**INF** Two stores and one message separate the number from the pixels: the rule's expression becomes the target's box (S293), the window's box copies that logical box (S294), and `sendWindowSize` is the only path in these receipts that tells the client a size. `Basis:` S293 and S294.

**UNK** What the configure actually carries and whether the client honours it. `sendWindowSize`'s body is not in this round's receipts, and no gkeep window was open to observe a configure exchange.

## §6 The reported variable: the animation goal

**OBS** S295 - the animated geometry answers GOAL and CURRENT from different places: `Vector2D CGeometricMovableAnimated::size(eGeometricValueType t) const { switch (t) { case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal(); case IGeometric::GEOMETRIC_CURRENT: return m_realSize->value();` (`Hyprland-GeometricMovableAnimated.cpp:17`). `setBox` assigns the incoming position and size to the two animation variables (lines 43-46), and `finishAnimation` warps both (lines 48-51).

**OBS** S296 - the clients JSON prints the goal, not the current value: `sc<int>(w->position(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x), sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), w->m_workspace ? w->workspaceID() : WORKSPACE_INVALID,` (`Hyprland-HyprCtl.cpp:427`). The same pair appears again in the text-format branch further down the file, so the choice is a property of the emitter and not of the JSON path alone.

**INF** The `size` field of `hyprctl clients -j` is where the window is going, not where it is drawn: while a size animation is in flight the goal can differ from the current box, and the entry's "reported size" and "rendered size" are therefore different quantities. `Basis:` S295's GOAL/CURRENT split and S296's argument.

**UNK** Whether any animation was in flight at the 2026-10-26 capture. The dump holds four tiled clients at 1720×1414 and no gkeep window (§8), so no transition was observed.

## §7 The client's own request

**OBS** S299 - gkeep asks GTK for its size when it builds the window: `window = Gtk.ApplicationWindow(application=self, title="gkeep") window.set_decorated(False) window.set_default_size(420, 500)` (`gkeep-ui-excerpt.py:31`). The same excerpt declares `application_id="org.omarchy.gkeep"` (line 6) and calls `set_default_size` exactly once, inside `do_activate`, on the first activation only.

gkeep request default_size=420x500 application_id=org.omarchy.gkeep

**INF** The request and the rule agree numerically, and the agreement is deliberate on both sides: the app asks for 420×500 and the host's rule overrides the desktop's 875×600 tag size with the same 420×500 (§1). `Basis:` S299's single `set_default_size`, S297's rule and comment.

**UNK** What the client's first commit actually contains. A GTK default size is a request to the windowing layer, and whether it reaches the compositor as an initial surface size or as a hint the compositor then overrides is not in these receipts.

## §8 What is and is not observed today

**OBS** S298 - the host's dump holds four mapped clients, all tiled: `"mapped": true, "class": "Alacritty", "floating": false,` (`host-clients-r43.json:4`). Each of the four reports 1720×1414 at monitor 0; no client's class matches the rule's regex.

host clients total=4 floating=0 gkeep=0

**UNK** The size a gkeep window takes on this host. No client of that class was open at capture, so no receipt in this wave holds a gkeep `size` value: 420×500 is the declared rule and the client's request, and this entry does not claim a window was ever observed at that size.

**INF** A join of the two sides is therefore untestable today on this host: the rule is declared, the client's request is declared, the code path between them is sourced, and the one observation that would close the chain - a mapped gkeep client's reported `size` - is absent from the only dump this round pinned. `Basis:` S297, S298, S299.

## §9 The decision table

| question | where the answer lives | state |
|---|---|---|
| What does this host declare for the gkeep class? | S297: float, centre, `size 420 500`, one regex (§1) | OBS |
| How is `match:class` evaluated? | S290: `RE2::FullMatch`, invertible by a `negative:` prefix (§2) | OBS |
| Which string is matched against? | not in these receipts (§2) | UNK |
| Where does the rule's size go? | S291: `static_.size`, a `SExpressionVec2`, reset per pre-read (§3) | OBS |
| Does the size need a floating window? | S292: consumed in the floating algorithm's `newTarget`, under `m_firstMap` (§4) | INF |
| Where is the computed box stored? | S293 target box, S294 window box (§5) | OBS |
| What does the client get told? | S294 `sendWindowSize`; the configure's bytes are unread (§5) | INF for the call, UNK for the contents |
| What does `hyprctl clients -j` print as `size`? | S295 + S296: the GOAL size, cast to int (§6) | OBS |
| What does the client ask for? | S299: `set_default_size(420, 500)` under `org.omarchy.gkeep` (§7) | OBS |
| Is a gkeep window open on this host today? | S298: four clients, none floating, none matching (§8) | OBS |
| What size does a gkeep window actually take? | no receipt in the wave holds one (§8) | UNK |
| Would a second matching rule change the size? | S291: the last applied match wins, but no second rule exists here (§3) | INF |

## §10 What this does not license

- No gkeep window was observed, at 420×500 or at any size. The number in this entry is declared twice (§1, §7), never measured (§8).
- The configure path is unread: `sendWindowSize`'s body is not in the receipts, so "the client is 420×500" does not follow even when a window opens; it follows only from a reported `size` on a mapped gkeep client.
- `hyprctl clients -j` reports the animation goal (§6). Any future measurement of this window must say whether the animation had settled, and a mid-transition value is not the rendered size.
- The size branch is a first-map branch in the floating algorithm (§4). This entry says nothing about a window that is tiled when it maps and floated afterwards.
- The rule file copy is one file, read as bytes (§1). Other host rule files - the desktop's stock rules included - are not in this entry's receipts, so "this is the only rule for this class" is a statement about this file only.
- The census is one dump on one day (§8): four clients, none floating. It is not a claim that no gkeep window has ever opened on this host.
