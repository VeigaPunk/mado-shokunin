# ExecGoalVsValue — w1 report (round 43, 2026-10-26)

**Status: complete.** Goal established: `hyprctl clients -j` `size` is the animation **goal**, not the
current size; the goal is already the rule's size on the first frame of a floating first map, while on
this host the pixels start at 87 % of it (`popin 87%`); no read verb exposes the current value.

Deliverable: `.ufo/waves/round-43/w1/ExecGoalVsValue/finding.md` (27 KB) with 16 pinned upstream source files and
4 own-work host receipts, `pins/SHA256SUMS`, and `verify-quotes.py` →
`verify-quotes.txt`: `quotes=69 fails=0` / `checksummed=22 uncovered=[]` / `VERIFY: PASS`.

## What was asked and what was found

1. **Accessor.** `clients -j` shares `getWindowData` with `activewindow`; the field is
   `sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x/.y)` (pins
   `hyprctl.cpp:395,427-428`) → `CGeometricMovableAnimated::size` returns `m_realSize->goal()`
   (`geometric-movable-animated.cpp:19`) → hyprutils `goal()` returns `m_Goal`
   (`hyprutils-animated-variable-0.14.2.hpp:217-218`). `m_Goal` is written by `operator=` (`:244-245`)
   and `setValueAndWarp` (`:265-266`); the tick writes only `m_Value` (`:287`). The same goal is what
   the compositor configures the client with (`window.cpp:1687,1741`).
2. **Goal vs current.** They differ exactly while an assignment is in flight: `m_Goal = v;
   m_Begun = m_Value` at assignment, interpolation per tick. At open, the rule's size reaches the
   target box in `newTarget` (`floating-algorithm.cpp:55-61,96`; only when `m_firstMap`,
   `window.cpp:2079,2383`) → `setBox` → `*m_realSize = x.size()` (`geometric-movable-animated.cpp:45`)
   → goal set, **before** `animateIn` is applied (`window.cpp:2520,2524,2526`). `animateIn` starts
   from the goal (controller `:160-161`); the popin style rewrites only the start to
   `GOALSIZE * minPerc` (`:39,43`), then `apply` does `setValueAndWarp(from)` + `resize(to=goal)`
   (`:190,194`). So the goal is the rule size at the first frame; the current value starts below it.
   Host style: `animation = windowsIn, 1, 4.1, easeOutQuint, popin 87%` (omarchy looknfeel:95, sourced
   at hyprland.conf:10; user file only comments), animations on (`getoption …enabled` = 1).
   Gkeep arithmetic `[INFERENCE]`: 420×500 rule → first frames at 365.4×435 while `clients -j`
   already says 420×500. `slide`/`gnomed` styles behave differently (`:71-72`, `:55,62`).
3. **Current value on the read surface: none.** `clients`/`activewindow` = goal
   (`hyprctl.cpp:426-428`); `getprop` exposes only rule-applicator props (`max_size`/`min_size`,
   `:1561,1563`; else `"prop not found"` `:1644`); `getoption` is config; `layers` is layer surfaces.
   The renderer is the only consumer of `GEOMETRIC_CURRENT` (`renderer.cpp:566`, pos `:562`).
   `eval`/`repl` evaluate Lua code and only under the Lua config manager (`hyprctl.cpp:1112`); not a
   geometry read, outside the round's allowed verbs, unused.
4. **Consequence for C1.** `AGREE` = the compositor's target equals the rule's `W H`; it is not a
   statement about pixels on screen during an assignment, not attribution to the rule (a client may
   request the same size; later assignments move the goal), and not a settled-size claim. Animations
   never cause a false `DIFFER` here (the animation moves only the current value); the blind spot is
   a **premature AGREE** (and a stuck animation is invisible to the join). Tiled windows never reach
   the rule-size branch (`algorithm.cpp:33-35`), so `TILED` stands. Host census today: 4 tiled clients,
   none floating (S298).

## Registry rows proposed (append-only; ids are proposals)

S300 hyprutils AnimatedVariable.hpp (v0.14.2, a21e87b) · S301 Window.cpp · S302
WindowAnimationController.cpp · S303 GeometricMovableAnimated.hpp · S304 Renderer.cpp · S305
Algorithm.cpp · S306 AnimationManager.cpp/.hpp · S307 AnimationTree.cpp · S308
helpers/AnimatedVariable.hpp · S309 own-work host getoption receipt · S310 own-work omarchy
`windowsIn` config + include chain · S311 Window.hpp. Full 11-column rows with anchors and sha256 in
`finding.md` §5. S292–S298 were reused (byte-identical to the fetch receipts); ids above S300 may
collide with other seats — the integrator assigns finals.

## Evidence retained (all inside the seat dir)

- `pins/` — 16 upstream files at their exact tags (sha256 in `pins/SHA256SUMS`), 4 own-work host
  receipts (`host-getoption.txt`, `omarchy-looknfeel-80-96.txt`, `host-config-chain.txt`,
  `host-clients-r43.json`), `quotes.tsv` (69 quotes), `MANIFEST.md` (provenance table).
- `verify-quotes.py` + `verify-quotes.txt` — verbatim-line + hash check, `VERIFY: PASS`.
- `finding.md` — the four answers, the map-order trace, the style nuance, the read-surface census.

## Risks / not established

- `sc<int>` semantics unverified (definition not located in macros/defines/MiscFunctions/SharedDefs);
  no claim about fractional-goal rendering.
- No live gkeep window observed (none open; dispatch/input out of scope); the 87 % first-frame value is
  code + host config, marked `[INFERENCE]`; animation wall time not measured.
- `windowsMove` style inheritance from the `windows` node not checked in hyprutils' animation tree.
- Nothing here establishes attribution (whether the `size` rule wrote the goal) — C2's ground.
- No file outside this seat's dir and this report was written; counters/controls/registration/fetch
  receipts read only. Scratch dir `/fast/scratch/hyaku/mado-r43/ExecGoalVsValue` removed.

## Tooling

No installs (no package transaction, no network tool added; `curl`/`python3`/`hyprctl` already present).
Host verbs used: `hyprctl version`, `hyprctl getoption animations:enabled -j`,
`hyprctl getoption animations:windowsIn -j`, `hyprctl getoption animations:windowsMove -j` (the latter
two answer `no such option`). No dispatch/keyword/reload/setprop, no input injection, no compositor
connection of our own.
