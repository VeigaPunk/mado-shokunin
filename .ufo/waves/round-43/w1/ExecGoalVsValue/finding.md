# Goal versus current size — what `hyprctl clients -j` `size` is while a window animates

Seat `ExecGoalVsValue`, mado round 43, inline v1 wave `w1` (2026-10-26). Lane repo
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`.
Inputs: the frozen registration (`.ufo/waves/round-43/registration.md`) and the pre-fetched receipts
`S290`–`S299`. Claim C1 (`PRED-C1-r42`, `tools/mado-geometry.py`) compares a rule's `size W H` with the
compositor's `clients -j` `size`; C1's docstring is its contract
(`quality/counters/c1-r42-geometry.py:1-120`, read-only). This seat establishes whose number that is.

Every quote below is verbatim from a file pinned in `pins/` (sha256 in `pins/SHA256SUMS`), and
`verify-quotes.py` re-checks all 69 ledger lines and every pin hash: `verify-quotes.txt` ends
`quotes=69 fails=0` / `checksummed=22 uncovered=[]` / `VERIFY: PASS`. Tags: Hyprland `v0.56.2` =
`efb50993780079460b0cbed1363e2166a2de1d9f`; hyprutils `v0.14.2` =
`a21e87b878e72ee5dfd375899e8b2ad0d0c4c0e1` (host reports system hyprutils 0.14.2,
`pins/host-getoption.txt`).

Claim tags: **[SOURCE]** read from a pin; **[OBSERVED]** produced by a command this seat ran today;
**[INFERENCE]** derived here, not directly observed.

## 0. Answer in four lines

1. `clients -j` `size` is `w->size(GEOMETRIC_GOAL)` → `m_realSize->goal()` → `m_Goal`: the animation
   **goal**, i.e. the last geometry the compositor assigned/configured toward, never the interpolated
   value. **[SOURCE]**
2. Goal and current differ whenever an assignment is in flight (`operator=` sets goal, current
   interpolates); at window open on this host the style is `popin 87%`, so the first frame's current
   size is 87 % of the goal while the goal is already the rule's full size. **[SOURCE + host config; the
   87 % arithmetic is INFERENCE]**
3. No `hyprctl` read verb exposes the current size. `clients`/`activewindow` report the goal,
   `getprop` reports rule-applicator properties only (no `size`), `getoption` reports config. The
   current value is used only inside the compositor's renderer. **[SOURCE]**
4. Therefore a C1 `AGREE` says *the compositor's target equals the rule's `W H`* — not that the
   pixels on screen are that size, and not that the rule caused it. During a popin the screen can show
   365×435 while `clients -j` says 420×500 for the same window. **[SOURCE + INFERENCE]**

## 1. The accessor chain behind `clients -j` `size`

The JSON field is declared in the shared window formatter (`getWindowData`, used by both `clients`
and `activewindow`), format string `"size": [{}, {}],` at **hyprctl.cpp:395**; the value arguments are
`sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x),` and the `.y` counterpart at
**hyprctl.cpp:427-428**. The neighbouring `at` field is the same goal accessor for position
(**hyprctl.cpp:426**). `clientsRequest` only filters unmapped windows
(`if (!w->m_isMapped && !g_pHyprCtl->m_currentRequestParams.all)`, **hyprctl.cpp:464**), then calls the
same formatter, so `clients -j` is that formatter — `registerCommand(SHyprCtlCommand{"clients", true, clientsRequest});`
(**hyprctl.cpp:2007**).

`CWindow` inherits the geometric interface (`class CWindow : public virtual IView, public virtual CGeometricMovableAnimated`,
**window.hpp:116**; the override is `virtual Vector2D      size(eGeometricValueType) const override;`,
**geometric-movable-animated.hpp:12**). The implementation maps the enum onto the animated variable:

- `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` — **geometric-movable-animated.cpp:19**
- `case IGeometric::GEOMETRIC_CURRENT: return m_realSize->value();` — **geometric-movable-animated.cpp:20**

`m_realSize` is a Hyprland alias of hyprutils' `CGenericAnimatedVariable<Vector2D, SAnimationContext>`
(pins `helpers-animated-variable.hpp`; created with initial `(0, 0)` under the `windowsIn` config at
**window.cpp:111**). In hyprutils 0.14.2:

- `const VarType& goal() const {` / `return m_Goal;` — **hyprutils-animated-variable-0.14.2.hpp:217-218**
- the starting value is horizon-wide `m_Goal  = initialValue;` — **hyprutils-animated-variable-0.14.2.hpp:181**
- `operator=` is what moves the goal: `m_Goal  = v;` / `m_Begun = m_Value;` — **…hpp:244-245**
- `setValueAndWarp` sets both: `m_Goal             = v;` / `m_Begun            = v;` — **…hpp:265-266**
- the tick only moves the value: `m_Value          = m_Begun + (DELTA * STEP.value);` — **…hpp:287**

So `GEOMETRIC_GOAL` returns `m_Goal`, whose writers are `operator=` (assignment = start an animation
to the new goal) and `setValueAndWarp` (assignment that also snaps the current value). It is not
derived from the current value at read time.

**What the goal means operationally:** it is the geometry the compositor configures the client
toward. For Wayland clients `sendWindowSize` reports the goal, not the current value:
`return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);` (**window.cpp:1687**, the
non-X11 branch of `realToReportSize`) and `const auto REPORTSIZE = realToReportSize();`
(**window.cpp:1741**, then `m_xdgSurface->m_toplevel->setSize(REPORTSIZE)` at :1753). The goal is
therefore "what the client is being told to be", while the current value is what the renderer draws.

**SUPPORTS C1** by naming its comparison target precisely; **ATTACKS** the reading "the number is the
window's size right now".

## 2. When goal and current differ, and whether the goal is the rule's size at the first frame

The animated variable has three fields (`m_Value`, `m_Goal`, `m_Begun`): an assignment stores the new
goal and the old value as the animation start (quotes at hpp:244-245), and each tick interpolates
`m_Value` between `m_Begun` and `m_Goal` (hpp:287). They are equal at construction (hpp:181), and the
tick short-circuits to a warp when they already coincide or animation is off:
`if (warp || av.value() == av.goal()) {` / `av.warp(true, false);` (**animation-manager.cpp:44-45**).
They differ exactly while an assignment is in flight — at open (`windowsIn`), at layout/rule resizes
and moves (`windowsMove` is installed after the open animation by
`animvar->setConfig(Config::animationTree()->getAnimationPropertyConfig("windowsMove"));`,
**window.cpp:2042**, inside `setVector2DAnimToMove`, **window.cpp:2037**; both nodes exist:
`m_animationTree.createNode("windowsIn", "windows");` **animation-tree.cpp:35** and
`…createNode("windowsMove", "windows");` **animation-tree.cpp:37**).

### Is the goal already the rule's size at the first frame? On the open path, yes.

Order inside `mapWindow` (all in pinned `window.cpp`):

1. `m_firstMap      = true;` — **window.cpp:2079** (before any layout call).
2. `g_layoutManager->newTarget(m_target, m_workspace->m_space);` — **window.cpp:2383**; the algorithm
   dispatches by float state (`if (SHOULD_FLOAT) {` / `m_floating->newTarget(target);`,
   **algorithm.cpp:33-35**), so a floating window reaches the floating algorithm's `newTarget`.
3. There the rule's size is read and written into the target box:
   `if (WINDOW->m_ruleApplicator->static_.size) {` (**floating-algorithm.cpp:55**),
   `windowGeometry.w = COMPUTED->x;` (**…:60**), `windowGeometry.h = COMPUTED->y;` (**…:61**), then
   `target->setPositionGlobal(windowGeometry);` (**…:96**).
4. `m_box = box;` (**target.cpp:11**) and `CWindowTarget::setPositionGlobal` calls `updatePos`, which
   for a mapped floating window runs `m_window->setBox(m_box.logicalBox);` (**window-target.cpp:71**;
   the mapped guard is `if (!validMapped(m_window)) {` at **window-target.cpp:63**).
5. `setBox` writes the animated variables: `*m_realSize     = x.size();` —
   **geometric-movable-animated.cpp:45** (in `void CGeometricMovableAnimated::setBox(const CBox& x) {`,
   **…:43**), i.e. `operator=`, i.e. `m_Goal = rule size` (hpp:244).
6. `layoutTarget()->recalc();` — **window.cpp:2520** re-applies the same box before the animation is
   armed; `m_realSize->setConfig(…getAnimationPropertyConfig("windowsIn"));` — **window.cpp:2524**;
   `m_animationController.apply(m_animationController.animateIn());` — **window.cpp:2526**.

`animateIn` starts from the goal on both ends (`ctx.size.from = m_parent->size(Desktop::View::IGeometric::GEOMETRIC_GOAL);`,
`ctx.size.to   = m_parent->size(Desktop::View::IGeometric::GEOMETRIC_GOAL);`, **window-animation-controller.cpp:160-161**)
and then the style rewrites *only the start*: for the popin family
`const auto ENDSIZE  = (GOALSIZE * minPerc).clamp({5, 5}, {GOALSIZE.x, GOALSIZE.y});`
(**window-animation-controller.cpp:39**), `ctx.size.from = ENDSIZE;` (**…:43**). `apply` commits it as
`m_parent->sizeAnimation()->setValueAndWarp(ctx.size.from);` (**…:190**) followed by
`m_parent->resize(ctx.size.to);` (**…:194**). So the animation's *from* is a fraction of the goal and
its *to* is the goal; the rule's size is the goal before the first animated frame is drawn.

The style is the host's, not a code default: the effective `windowsIn` line on this host is
`animation = windowsIn, 1, 4.1, easeOutQuint, popin 87%` (**omarchy-looknfeel-80-96.txt**, original
line 95), with animations on — `enabled = yes, please :)` (original line 82) and
`{"option": "animations:enabled", "int": 1, "set": true }` (**host-getoption.txt**, `[OBSERVED]`
today). It is reached before the user's own include
(`source = ~/.local/share/omarchy/default/hypr/looknfeel.conf`, **host-config-chain.txt** original
line 10, sourced at hyprland.conf:10); the user's own `animations` block at
`~/.config/hypr/looknfeel.conf:25-27` contains only comments, and the theme/toggle files carry no
animation line (no-output grep recorded in **host-config-chain.txt**). `[INFERENCE]`: the style is
resolved from `positionAnimation()->getStyle()` (**window-animation-controller.cpp:124**), so it is
the `windowsIn` style above.

**Concrete host arithmetic** `[INFERENCE]`: the gkeep rule is `windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$`
(`fetch/host-gkeep.conf:4`, `S297`); `420·0.87 = 365.4`, `500·0.87 = 435`, both above the 5 px floor.
So for the first frames of a gkeep open the screen composits a 365.4×435 window while `clients -j`
already answers `[420, 500]`. Wall-clock duration is the `windowsIn` curve (speed 4.1, easeOutQuint);
this seat did not measure it.

Not every style separates the two numbers: `slide` keeps the size at the goal
(`ctx.size.from = GOALSIZE;` / `ctx.size.to   = GOALSIZE;`, **window-animation-controller.cpp:71-72**),
and `gnomed` starts at zero height (`const auto GNOMESZ  = Vector2D{GOALSIZE.x, 0.F};`,
**…:55**; `ctx.size.from = GNOMESZ;`, **…:62**), so the pixel-versus-goal gap is style-dependent. It is
present on this host only because the host's `windowsIn` style is `popin 87%`.

Two conditions on "the goal is the rule's size at the first frame":
(a) the window must be floating when the target is created — a tiled target goes to
`m_tiled->newTarget(target)`, where the `static_.size` branch is not reached, so a tiled window's goal
is the layout's box; and (b) it must be the first map
(`if (target->window() && target->window()->m_firstMap)`, **floating-algorithm.cpp:49**), since
`m_firstMap` is cleared after the open (**window.cpp:2513**). A later `windowrule` re-application is not
this path.

**SUPPORTS C1** that `AGREE` is well defined and stable (the goal does not wobble during the
animation, because the animation moves only `m_Value`); **ATTACKS** "AGREE at the first frame proves
the pixels are already the rule's size".

## 3. Does any read verb expose the current value?

No window read verb does.

- `clients` and `activewindow` share `getWindowData`, whose `at` and `size` are the **goal**
  (hyprctl.cpp:426-428, formatter at :395; `clientsRequest` at :464-467). `[SOURCE]`
- `getprop` exposes rule-applicator properties. The property ladder has `max_size` and `min_size`
  only — `} else if (PROP == "max_size")` (**hyprctl.cpp:1561**), `else if (PROP == "min_size")`
  (**…:1563**) — which are rule/config values from `m_ruleApplicator`, not geometry; anything else
  falls through to `return "prop not found";` (**…:1644**). `getprop` is registered read-only at
  `registerCommand(SHyprCtlCommand{"getprop", false, dispatchGetProp});` (**…:2032**). `[SOURCE]`
  There is no `size` or `at` property to ask for.
- `getoption` reports configuration (`animations:enabled` above; `animations:windowsIn` answers
  `no such option` because animation nodes are not config options, `host-getoption.txt`). `[OBSERVED]`
- `layers` reports layer surfaces, not windows; `monitors` reports monitor boxes; the remaining
  commands in the registered list (`workspaces`, `devices`, `binds`, `version`, …) carry no window
  geometry. The registered command set is visible in the pinned file (e.g.
  `registerCommand(SHyprCtlCommand{"clients", true, clientsRequest});`, hyprctl.cpp:2007). `[SOURCE]`
- The current value is consumed by the renderer: `const auto                       REALSIZE   = pWindow->size(Desktop::View::IGeometric::GEOMETRIC_CURRENT);`
  (**renderer.cpp:566**, with position on :562), i.e. only inside the compositor's draw path.
  `[SOURCE]`

One non-geometry escape hatch exists and is not a read verb: `eval`/`repl` evaluate code, and only
under the Lua config manager (`return "eval is only supported with the lua config manager";`,
**hyprctl.cpp:1112**; registered at :2042-2043). It is outside this round's allowed verb list and was
not used; the host's config chain is hyprlang `.conf` files (S310).

So a reader of the permitted read verbs sees the goal and never the interpolated size; the current
size is exactly "what is on screen", and it is not addressable over the request socket.

**SUPPORTS** the statement that the pixel truth is outside C1's input; **ATTACKS** any plan to
"poll the current size with `hyprctl`" — there is no such verb in this version.

## 4. Consequence for a reader that compares a rule's size with `clients -j`

- `AGREE` = the compositor's goal equals the rule's `W H`. Because `sendWindowSize` reports the goal
  to the client (window.cpp:1687,1741), AGREE is a statement about the **configured target**, the
  number the compositor will keep asking the client to fill — a real, checkable fact, but a fact about
  intent.
- It is **not** a statement about pixels on screen while an assignment is in flight. On this host the
  open animation is `popin 87%`: for its duration the rendered size is below the goal (365×435 vs
  420×500 for gkeep `[INFERENCE]`), and `clients -j` answers the goal throughout. A tool that samples
  once cannot see this gap; it can only print AGREE.
- It is **not** a statement that the rule caused the number. The goal can equal the rule's `W H`
  because the client asked for the same size (gkeep's `set_default_size(420, 500)`, `S299`), because a
  later assignment produced it, or because a different rule/layout wrote it. `AGREE` is consistency,
  not attribution.
- It is **not** a statement that the goal is current: after any later resize the goal leads the
  animation again; a sample taken then is the new target, not the settled size.
- Nothing about this creates a false `DIFFER` during an animation: the animation moves only the
  current value, so a sampled `clients -j` stays at the goal. The failure mode is the opposite —
  **premature AGREE** relative to the screen — plus a blind spot for a stuck or wrong animation
  (e.g. a popin that never reaches its goal is invisible to the join).
- For a **tiled** window the rule's `size` is not consulted on this path at all (the `static_.size`
  branch lives in the floating algorithm), so `TILED` is the honest verdict; a goal there is the
  layout's box (all four current host windows are tiled at 1720×1414 with `"floating": false`,
  **host-clients-r43.json:6**, `S298`). `[SOURCE/OBSERVED]`

For C1's contract this is consistent: the docstring already declares that whether Hyprland applies a
rule's size to a live window is a compositor fact the counter does not score. This finding sharpens
the residual: even the *reported* number is a goal, so a host receipt built from `clients -j` is
evidence about the goal, never about the hosted pixels.

## 5. Registry rows proposed (append-only; ids S300+)

Suggested ids; anchors and sha256 are the durable part (other seats also propose from S300+).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S300 | hyprutils — animated variable core — https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/include/hyprutils/animation/AnimatedVariable.hpp | code | A | The three-value animation model behind every Hyprland geometry accessor | include/hyprutils/animation/AnimatedVariable.hpp:181 initial value, :208-223 value/goal/begun accessors, :225-250 operator= sets goal and begun, :253-261 setValue, :264-270 setValueAndWarp, :274-292 update interpolation @ tag v0.14.2 commit a21e87b878e72ee5dfd375899e8b2ad0d0c4c0e1, 10677 B sha256 960660cf41fb4ecf56bfa269d316c06b499e0d915fd6c8faeb7782ca324e5bcb | goal is a stored target, value is the interpolated field; assignment starts an animation, setValueAndWarp snaps both — the semantics `GEOMETRIC_GOAL`/`_CURRENT` inherit | mined | 2026-10-26 | on-release | .ufo/waves/round-43/w1/ExecGoalVsValue/finding.md |
| S301 | Hyprland v0.56.2 — window open path — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp | code | A | When the rule's size becomes the goal and what the client is configured with | src/desktop/view/Window.cpp:111 size var created under windowsIn, :1687 and :1741 sendWindowSize reports the goal, :2037-2042 windowsMove installed after the open, :2079 firstMap set, :2383 newTarget at map, :2513 firstMap cleared, :2520 recalc, :2524 windowsIn config, :2526 animateIn applied @ commit efb50993780079460b0cbed1363e2166a2de1d9f, 124226 B sha256 d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded | the goal the join reads is also the configure target; the rule's size is in it before the first animated frame; the open animation is the only writer of the current size at first map | mined | 2026-10-26 | on-release | .ufo/waves/round-43/w1/ExecGoalVsValue/finding.md |
| S302 | Hyprland v0.56.2 — window animation controller — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/animationControllers/WindowAnimationController.cpp | code | A | How the open animation separates start value from goal | src/desktop/view/animationControllers/WindowAnimationController.cpp:36-49 popin math (GOALSIZE times percent, 5 px floor), :123-149 style selection from positionAnimation style or an animation rule, :155-169 animateIn from/to both GEOMETRIC_GOAL, :188-195 apply sets current to from and resize()s to the goal @ commit efb5099…, 6589 B sha256 9a8c3c2961a1a55fca7b8783e1c3b808b424291e832bf4cdf88ed7a73e5bab08 | the animation start is a fraction of the goal; the goal end is the rule's size, so clients -j is already final while the window grows | mined | 2026-10-26 | on-release | .ufo/waves/round-43/w1/ExecGoalVsValue/finding.md |
| S303 | Hyprland v0.56.2 — geometric movable animated interface — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/types/GeometricMovableAnimated.hpp | code | A | The class that answers size(GOAL/CURRENT) and owns the animated variables | src/desktop/view/types/GeometricMovableAnimated.hpp:11-13 the three accessors, :21-22 positionAnimation/sizeAnimation, :29-30 m_realPosition/m_realSize @ commit efb5099…, 1097 B sha256 8dcf6e86a78eb0e4bd2c71a289329d8ffef7ca400cf6971dd4e744ba38499394 | size(GEOMETRIC_GOAL) is a member read of m_realSize; the interface has no other source for geometry | mined | 2026-10-26 | on-release | .ufo/waves/round-43/w1/ExecGoalVsValue/finding.md |
| S304 | Hyprland v0.56.2 — renderer window pass — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/render/Renderer.cpp | code | A | Which value the compositor composites | src/render/Renderer.cpp:562 position GEOMETRIC_CURRENT for the render pos, :566 size GEOMETRIC_CURRENT into textureBox, :567 the 5 px floor @ commit efb5099…, 143211 B sha256 9af8a74e7dc42ba3c5532303b9bb4ee7c350d4cef2f2c8984e41f2a01b3bdd22 | the pixels use the current value, so the goal reported by clients -j and the rendered size are different fields during an animation | mined | 2026-10-26 | on-release | .ufo/waves/round-43/w1/ExecGoalVsValue/finding.md |
| S305 | Hyprland v0.56.2 — layout algorithm dispatch — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/layout/algorithm/Algorithm.cpp | code | A | Which targets reach the floating rule-size branch | src/layout/algorithm/Algorithm.cpp:30-40 addTarget branches on target->floating() to m_floating->newTarget or m_tiled->newTarget, :62-78 moveTarget with reposition @ commit efb50993780079460b0cbed1363e2166a2de1d9f, 8422 B sha256 fe4a129a6402ba86a65d2f9750f96b509c420bd0295124b636f4ee5facdd3428 | a tiled target never reaches the windowrule size branch, so its goal is layout geometry — the ground for TILED refusing AGREE | mined | 2026-10-26 | on-release | .ufo/waves/round-43/w1/ExecGoalVsValue/finding.md |
| S306 | Hyprland v0.56.2 — animation manager — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/animation/AnimationManager.cpp + …/src/animation/AnimationManager.hpp | code | A | How variables are created and ticked | src/animation/AnimationManager.hpp:28-51 createAnimation stores the initial value and context, src/animation/AnimationManager.cpp:42-51 updateVariable warps when value equals goal or warp is forced, else interpolates @ commit efb5099…, 16288 B sha256 8c37cd0d1e972e8789468fdf063456a6a40ed17d482b898b0639a6d2a1fa7985 and 2638 B sha256 e7834aef3b0f3259a109e5407c27bd31d5ad8ed05b698e4726e5972bacd479fa | a variable with animations off (or already settled) has value equal to goal; only a live assignment separates them | mined | 2026-10-26 | on-release | .ufo/waves/round-43/w1/ExecGoalVsValue/finding.md |
| S307 | Hyprland v0.56.2 — animation tree nodes — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/animation/AnimationTree.cpp | code | A | The node names geometry animations bind to | src/config/shared/animation/AnimationTree.cpp:35-37 createNode windowsIn/windowsOut/windowsMove under windows, :61-67 the built-in root configs @ commit efb5099…, 3483 B sha256 313ed20167618dfe163fceee8753e9a49d8ef356bc3f580963e07039839e7bae | windowsIn is the open-time size config and windowsMove the post-open one — the two configs a size animation can run under | mined | 2026-10-26 | on-release | .ufo/waves/round-43/w1/ExecGoalVsValue/finding.md |
| S308 | Hyprland v0.56.2 — Hyprland's alias of the hyprutils variable — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/helpers/AnimatedVariable.hpp | code | B | Which upstream type Hyprland's PHLANIMVAR names | src/helpers/AnimatedVariable.hpp:68 the CAnimatedVariable alias of Hyprutils::Animation::CGenericAnimatedVariable, :70-74 PHLANIMVAR and PHLANIMVARREF @ commit efb5099…, 2028 B sha256 6c8db9a2a55eac3f1463918b39a2a36bd641c8ea1c33e74414d64fe891aaea3a | the goal()/value() semantics quoted from hyprutils are the ones Hyprland actually uses | mined | 2026-10-26 | on-release | .ufo/waves/round-43/w1/ExecGoalVsValue/finding.md |
| S309 | Host animation option receipt — own-work, 2026-10-26 — .ufo/waves/round-43/w1/ExecGoalVsValue/pins/host-getoption.txt | own-work | A | The host's live animation switch and its version/library record | whole file, 900 B sha256 c206e8539637e766c5cc9827a5a4afec283b398afe759fad985ef564c5b61eee; commands hyprctl version and hyprctl getoption animations:enabled -j, run 2026-10-26, read verbs only | animations are on (int 1) on this host, so the goal and current values are not collapsed by a global disable; per-node animation styles are not getoption options | mined | 2026-10-26 | 90d | .ufo/waves/round-43/w1/ExecGoalVsValue/finding.md |
| S310 | Omarchy default animation config and the host include chain — own-work, 2026-10-26 — pins/omarchy-looknfeel-80-96.txt and pins/host-config-chain.txt | own-work | A | The host's effective windowsIn motion | omarchy looknfeel.conf:82 animations enabled, :94 windows node, :95 animation = windowsIn, 1, 4.1, easeOutQuint, popin 87%, :96 windowsOut; hyprland.conf:10 sources the omarchy looknfeel before the user file at :19; user looknfeel.conf:25-27 has only comments; theme/toggle grep is empty, 840 B sha256 a5d2c473282ab01a92bef5773b56b1910107bb0b8e2ab4eabd0fa393a4ed860d and 4936 B sha256 0243d71787db7aa68dd9956b6ef7273168091e51d55fafcf847754a93f85a365 | on this host a new window's size starts at 87 percent of its goal, so clients -j reports the final rule size while the screen shows the smaller box | mined | 2026-10-26 | on-change | .ufo/waves/round-43/w1/ExecGoalVsValue/finding.md |
| S311 | Hyprland v0.56.2 — window class declaration — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.hpp | code | B | The inheritance that routes CWindow size() to the animated accessor | src/desktop/view/Window.hpp:116 class CWindow inherits CGeometricMovableAnimated, :148 target member @ commit efb5099…, 23988 B sha256 1f60b8ff0bc6b5a48af5c03cb2cac1108db677efc70b4424b56ef6f1f2d1cc81 | no window-specific size override exists; the geometry comes from the animated base | mined | 2026-10-26 | on-release | .ufo/waves/round-43/w1/ExecGoalVsValue/finding.md |

## 6. Risks, unverified, and what this does not establish

- **`sc<int>` is unverified.** The formatter wraps the goal components in `sc<int>` (hyprctl.cpp:427-428);
  the definition was not found in `src/macros.hpp`, `src/defines.hpp`, `src/helpers/MiscFunctions.hpp`
  or `src/SharedDefs.hpp` (all opened, not pinned, not quoted). I therefore do **not** claim how a
  fractional goal renders (truncation vs rounding). The tool's contract already requires integral
  JSON, so this only matters for a fractional rule size or scale.
- **No live gkeep window was observed.** No gkeep window is open (S298 has four tiled clients), and
  host input/dispatch is out of scope for this seat, so the 87 % first-frame claim is derived from
  code plus the host config chain, not captured on a running gkeep. The oracle harness was not used;
  the source path is complete without it, but a nested-compositor capture would settle the arithmetic.
- **Animation duration/timing not measured.** Only the separation of goal and current is claimed;
  wall-clock numbers are not.
- **Config inheritance for `windowsMove` not verified.** The host sets the `windows` node, not
  `windowsMove` (S310); whether/which style the child inherits was not checked in hyprutils'
  animation tree. The claim only needs that resizes animate under some `windowsMove` config, which
  window.cpp:2042 sets.
- **No claims about rule attribution.** This seat says nothing about whether the `size` rule is the
  thing that wrote the goal; that is C2's territory (owner of S290-S299 and the entry).
- **No file outside this seat's directory was edited**; the counters, controls, registration and
  fetch receipts were read only.

## 7. Reproduction

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w1/ExecGoalVsValue
python3 verify-quotes.py            # -> VERIFY: PASS (64 quotes, 21 pin hashes)
sha256sum -c <(sed 's|  |  pins/|' pins/SHA256SUMS)   # from the seat dir
hyprctl version                     # Hyprland 0.56.2 @ efb5099…, hyprutils 0.14.2
hyprctl getoption animations:enabled -j
```
