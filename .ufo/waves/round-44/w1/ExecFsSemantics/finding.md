# C1 premise, grounded in Hyprland v0.56.2: what `clients -j` reports for a maximized or fullscreen client

Seat `ExecFsSemantics`, round 44 w1. Question asked: ground C1's premise — for a client whose `clients -j`
`fullscreen` value is 1 or 2, the reported `size` (`at`) says nothing about the window rule's `size W H`.
Revision: `efb50993780079460b0cbed1363e2166a2de1d9f` (tag v0.56.2, `hyprctl version` in
`receipts/host-read.txt`). Every locator below is computed (`grep -n`) and stored in
`receipts/greps.txt`; `verify-quotes.py` re-derives file:line from the pinned bytes and checks the
needle is in that line **and** in the receipt. Pins: `pins/` (sha256 in `pins/SHA256SUMS.txt`).

## Short answer

**The premise holds**, with one wording correction: the *default* fullscreen handler replaces the box with
the monitor box (mode 2) or the workspace work area (mode 1); the **scrolling layout's** handler replaces
neither — it sizes a layout column instead. In all three cases the reported box is a monitor / work-area /
column quantity, never the rule's size, so BADSIZE|FULLSCREEN|MAXIMIZED|… is the right order and the
round-43 DIFFER on a fullscreen gkeep window is a false report.

Verdicts per question: (1) no, the internal mode is only 0, 1 or 2; (2) yes — the *goal* box becomes the monitor box
(mode 2) or the work area (mode 1) in the same call that reports it; (3) yes, `m_isFloating` survives
fullscreen, so round 43 says DIFFER (floating) or TILED (tiled), never a rule verdict; (4) on exit the
remembered **size** is restored around the work-area centre (position is not remembered); (5) one real
divergence from "monitor box / work area" — layout-managed (scrolling) targets — and no state where the
reported box is still the rule's box.

## (1) Can `.internal` be anything other than 0, 1, 2? No.

The type is a closed `int8_t` enum with three values, and there is no `FSMODE_MAX` enumerator (the header
comment "List of FSMODE_MAX windows", `FullscreenController.hpp:109`, is shorthand for FSMODE_MAXIMIZED).

- `enum eFullscreenMode : int8_t {` — `.ufo/waves/round-44/fetch-c1/Hyprland-FullscreenController.hpp:12`;
  `FSMODE_NONE = 0,` `:13`, `FSMODE_MAXIMIZED,` `:14`, `FSMODE_FULLSCREEN,` `:15` (implicit 1, 2).
- Every raw-int entry is clamped before it can be stored:
  `internal = std::clamp(internal.value(), sc<eFullscreenMode>(0), FSMODE_FULLSCREEN);` —
  `pins/Hyprland-FullscreenController.cpp:294` and the same for `client` `:296`;
  `internalMode = std::clamp(internalMode, sc<Fullscreen::eFullscreenMode>(0), Fullscreen::FSMODE_FULLSCREEN);`
  — `pins/Hyprland-ConfigActions.cpp:294` (`:295` for client, applied before `NEW_MODES` is built at `:299`).
- The two raw-int sources both pass through those clamps: `dispatch fullscreenstate N M` parses
  `internalMode = std::stoi(std::string(ARGS[0]));` (`pins/Hyprland-DispatcherTranslator.cpp:197`), casts at
  `:203`/`:204`, then `Actions::fullscreenWindow` clamps; the `fullscreenstate` window rule casts
  `.internal = sc<Fullscreen::eFullscreenMode>(m_ruleApplicator->static_.fullscreenStateInternal.value_or(0)),`
  (`.ufo/waves/round-44/fetch/Hyprland-Window.cpp:2198`) and its value reaches the handler only via
  `setFullscreenMode` (clamped). The remaining cast sites are bit-masks of already-enum values
  (`Window.cpp:2469`, `:2471`).
- Stores into the map are only enum values: `ITR->second.internal = mode;`
  (`fetch-c1/Hyprland-FullscreenHandler.cpp:139`), `m_fsTargets.emplace(target, SFullscreenMode{.internal = mode});`
  (`:137`), `:135` (NONE), and the scrolling twin (`pins/Hyprland-ScrollingFullscreenHandler.cpp:260-264`).
- The report is an integer by construction: `sc<uint8_t>(Fullscreen::controller()->getFullscreenModes(w).internal)`
  — `fetch-c1/Hyprland-HyprCtl.cpp:431` (JSON) and `:451` (text). A `uint8_t` cast of the three enum values renders as an
  integer; `bool`/float/`"2"`/`3`/`-1` cannot come out of this code. The counter's defensive reading
  (anything not an int 1/2 → 0) is therefore right about the type and unreachable in this source for the
  values 3, -1, true, 2.0.

## (2) Does the GEOMETRIC_GOAL box become the monitor box / work area? Yes, for the default handler.

Chain, all in one synchronous call from `setWindowFullscreenModeInternal` → `requestFullscreen`:

1. `requestFullscreen` rejects a target with no workspace/monitor:
   `if (!request.target || !request.target->window() || !request.target->workspace() || !request.target->workspace()->m_monitor)`
   — `fetch-c1/Hyprland-FullscreenHandler.cpp:88`.
2. Mode 2 (fullscreen): `const CBox MONBOX = MONITOR->logicalBox();` `:192`, then
   `LAYOUT_TARGET->setPositionGlobal(MONBOX);` `:194`. Mode 1 (maximized):
   `const CBox WORKAREA = WORKSPACE->m_space->workArea(target->floating());` `:196`, then
   `LAYOUT_TARGET->setPositionGlobal(WORKAREA);` `:198`. Only when `TARGET_INTERNAL_MODE == FSMODE_NONE`
   does it return without touching the box (`:182`) — a non-FS window is untouched, by design.
3. `ITarget::setPositionGlobal` stores the box and rounds it (`pins/Hyprland-LayoutTarget.cpp:10`, `:12`);
   `CWindowTarget::setPositionGlobal` then calls `updatePos(flags)` (`pins/Hyprland-WindowTarget.cpp:37`, `:39`).
4. Default-handled FS branch: `m_window->setBox(m_box.logicalBox);` (mode 2, `:94`) and
   `m_window->setBox({visualBox.pos() + RESERVED.topLeft, visualBox.size() - (RESERVED.topLeft + RESERVED.bottomRight)});`
   (mode 1, `:105` — work area minus the window's reserved extents).
5. `setBox` writes the animated size variable: `*m_realSize = x.size();`
   (`pins/Hyprland-GeometricMovableAnimated.cpp:45`), and the animated-variable assignment sets the **goal**:
   `m_Goal = v;` (`pins/hyprutils-0.14.2-AnimatedVariable.hpp:244`, `goal()` at `:217`; host hyprutils
   0.14.2 ≈ the pinned `HYPRUTILS_MINIMUM_VERSION 0.14.0`, `pins/Hyprland-CMakeLists.txt:150`).
6. `hyprctl clients` prints exactly that goal:
   `sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x)` `fetch-c1/Hyprland-HyprCtl.cpp:427`
   (`:428` y; the `at` pair at `:426`-`:427` is the same goal position). Report is of the goal, not the
   animating current value, so no animation lag is observable.

Work area, for the record, is the monitor box minus reserved space minus the out/float gaps
(`CConfigValue<Config::IComplexConfigValue>("general:gaps_out")` `Space.cpp:87`,
`("general:float_gaps")` `:88`):
`auto workArea = m_parent->m_monitor->logicalBoxMinusReserved();` (`pins/Hyprland-Space.cpp:85`),
`m_workArea = workArea;` `:105`, `return floating ? m_floatingWorkArea : m_workArea;` `:110`.

So a live gkeep window (420x500 rule, monitor 3440x1440, reserved top 26 in `receipts/host-read.txt`) would
report `size` = 3440x1440 (mode 2) or ≈3440x1414-minus-gaps (mode 1) — the round-43 tool compares that to
420x500 and prints DIFFER.

## (3) Is the floating flag kept while fullscreen? Yes.

Nothing in the fullscreen path writes it. In the whole pin set the flag has three writers:
`m_window->m_isFloating = x;` inside `void CWindowTarget::setFloating(bool x)` (`pins/Hyprland-WindowTarget.cpp:291`,
`:285`) — reached from the toggle-floating dispatch (`Space.cpp` → `toggleTargetFloating`), target swaps, and
`changeFloatingMode` — plus the two map-time sites `m_isFloating = true;`
(`fetch/Hyprland-Window.cpp:2130`, XWayland wants-float) and
`m_isFloating = m_ruleApplicator->static_.floating.value_or(m_isFloating);` (`:2191`, the `float` rule).
`w->m_target->setFloating(m_target->floating());` (`Group.cpp:133`) only copies the group's own flag to members.

The code proves the flag stays set by *testing* it instead of clearing it — the non-FS floating branch is
guarded against fullscreen rather than entered by clearing the flag:
`if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) {`
(`pins/Hyprland-WindowTarget.cpp:70`). Same in the controller:
`if (window->m_isFloating && WINDOW_FS_MODE.internal == FSMODE_NONE && mode != FSMODE_NONE)` (damage only).
Consequence: round 43 never emits TILED for a floating FS client (it emits DIFFER — the false report), and a
*tiled* FS client stays `floating:false` and gets TILED (true but useless) — which is exactly why the new
verdicts must be tested before TILED.

## (4) What happens to the rule's box on exit?

Entering, only for a floating window, only when the new mode is not NONE and the window is not already FS,
the current box size is remembered:
`if (target->window() && target->window()->m_isFloating && mode != FSMODE_NONE && !isFullscreen(target))` /
`target->rememberFloatingSize(target->position().size());` (`fetch-c1/Hyprland-FullscreenHandler.cpp:130`, `:131`)
— at that moment the box is still the rule's box.

Exiting (mode NONE): `setTargetSizeAndPosition` returns at the mode test without writing the box
(`fetch-c1/Hyprland-FullscreenHandler.cpp:182`); for a floating window the controller then re-centres:
`if (mode == FSMODE_NONE && window->m_isFloating)` (`pins/Hyprland-FullscreenController.cpp:478`) →
`ALGORITHM->recenter(window->layoutTarget());` `:480` → `const auto LAST = t->lastFloatingSize();`
(`pins/Hyprland-FloatingAlgorithm.cpp:21`) and
`t->setPositionGlobal({m_parent->space()->workArea().middle() - LAST / 2.F, LAST});` `:26`.

So the **size** comes back (the rule's size for a rule-sized floating window) but the **position** is the
work-area centre, not the pre-fullscreen position — only the size is remembered. A tiled window remembers
nothing; its box returns to the layout on recalc. The default floating algorithm's `newTarget` — reached from
`void CLayoutManager::newTarget(SP<ITarget> target, SP<CSpace> space) {` (`LayoutManager.cpp:19`) — re-reads the
`size` rule only when a target is added, not on exit. After exit `fullscreen` is 0 again, so
AGREE/DIFFER become meaningful — the verdict pair is consistent in both directions.

## (5) Any state with internal 1 or 2 but the reported box still the rule's? No; one layout diverges from "monitor box / work area".

Considered, with the pinned evidence:

| State | Box replaced? | Evidence |
|---|---|---|
| floating fullscreen (mode 2) | yes → rounded monitor logical box | `FullscreenHandler.cpp:192,194`; `WindowTarget.cpp:94` |
| floating maximized (mode 1) | yes → work area minus reserved | `FullscreenHandler.cpp:196,198`; `WindowTarget.cpp:105` |
| tiled fullscreen/maximized, non-scrolling layout | yes, same default handler (handler name is DEFAULT → not layout-managed) | `if (DEFAULT_FS_HANDLER->isFullscreen(window->m_target) || DEFAULT_FS_HANDLER->getFullscreenModes(window->m_target).client != FSMODE_NONE)` (`FullscreenController.cpp:258`) keeps the DEFAULT handler name; `WindowTarget.cpp:89` guard `FSMODES.internal != Fullscreen::FSMODE_NONE && !Fullscreen::controller()->layoutManagedFS(m_self->window())` |
| **tiled FS/maximize in the scrolling layout** | box replaced, but from the **column geometry**, not monitor/work area | `ScrollingFullscreenHandler.cpp:301-303` (the signature then an empty body — "We don't need to do anything explicitly here…" `:302`, `:306-308`); column width `currentCol->setColumnWidth(fullscreenColumnWidth());` `:197` (monitor/usable ratio) vs `currentCol->setColumnWidth(1.F);` `:232` (maximize); applied through the "Layout handled FS" branch `WindowTarget.cpp:114-133` (`setBox(visualBox)` `:123`, minus reserved `:128`) |
| group fullscreen | current member yes (group box); non-current members **internal 0** with the group box pushed to them | `FullscreenHandler.cpp:41-44` ("A window group's FS modes are considered to be owned by its current window"); `pins/Hyprland-WindowGroupTarget.cpp:34` `w->m_target->setPositionGlobal(m_box, flags);` |
| hidden / non-visible workspace | yes — no visibility test in the path | `grep -c isHidden` = 0 in both `WindowTarget.cpp` and `FullscreenHandler.cpp` (receipt) |
| work-area change while FS | may keep a *stale* work-area box (re-application skipped) | `if (!Fullscreen::controller()->m_windowPosSettingQueued)` + then returns early (`WindowTarget.cpp:84-85`); the flag is set by the FS path at `FullscreenHandler.cpp:193,197,233,252` |
| no mapped/workspace/monitor | mode is not *stored* either, so internal stays 0 | `FullscreenController.cpp:430`, `WindowTarget.cpp:63` (early returns before the mode is stored) |

No row yields internal ∈ {1,2} with the rule's box. The scrolling rows are the correction to the
registration / reference-docstring sentence "a maximized window's box to the work area and a fullscreen
window's box to the monitor box": that is the default handler; under `layout:scrolling` the handler is a
no-op and a tiled maximize reports the column (usable-area width), a tiled fullscreen the monitor-wide
column. The verdicts are unaffected — neither is the rule — but the sentence is not the whole mechanism.

**One asymmetry worth recording** (does not break C1 because TILED precedes AGREE/DIFFER, and because it is
the opposite direction): a tiled window with a `size` rule is *pseudo*-tiled — the rule's size becomes the
pseudo size, `m_target->setPseudoSize(*COMPUTED);` (`fetch/Hyprland-Window.cpp:2408`) — so part of a
pseudo-tiled window's reported size is rule-derived. It can never be reported as AGREE/DIFFER (TILED wins),
and it can only be reported MAXIMIZED/FULLSCREEN when the compositor really is in that mode, where the box
has been replaced.

## Verdict

Evidence **supports** FULLSCREEN/MAXIMIZED meaning "the reported size says nothing about the rule", and
supports putting both before TILED (a tiled window keeps `floating:false` while FS) and before
AGREE/DIFFER (the box has been replaced). It also supports `fsmode` = JSON integer 1/2 only: the field is a
`uint8_t` cast of a three-valued enum whose every raw-int ingress is clamped to [0,2]. The only defect
routed to the L1 is documentation, not behaviour: the mechanism sentence in `registration.md` and in the
reference docstring is exact for the default handler and wrong for `layout:scrolling` (no contract clause
scores prose, so `PRED-C1-r44` is unaffected).

## Limits (declared, not measured)

- Source-only ground: at reading time the host had **no** client with `fullscreen` 1 or 2
  (`receipts/host-read.txt`: three mapped clients, all `0 0`), and this seat may not dispatch or open a
  Wayland client, so the live box is not observed — that stays C1's declared residual.
- `m_Goal = v` semantics are read from the *installed* hyprutils 0.14.2 header
  (`pins/hyprutils-0.14.2-AnimatedVariable.hpp`), not from a hyprutils git pin: the pinned commit only
  requires `HYPRUTILS_MINIMUM_VERSION 0.14.0` (`pins/Hyprland-CMakeLists.txt:150`).
- The pin set is the files this question needed plus the tree listing (`pins/tree.json`, 1028 blobs); a
  writer of `m_isFloating` or of a handler map outside that set is not excluded by exhaustiveness, only by
  the files read. No sandbox/plugin path was examined (`hyprpm` plugins can call the public controller).
