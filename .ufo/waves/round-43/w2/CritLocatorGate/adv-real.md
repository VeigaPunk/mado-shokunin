# adversarial matrix against check-locators.py, using the round-43 pins as receipts

Each numbered line is one attack. The expected verdict is in the line's own text so the run output can be
diffed against it by eye; `.ufo/waves/round-43/w2/CritLocatorGate/adv-real.out` holds the checker's answer.

A1 FALSE-OK shared tokens: the goal box comes from `size` at `Hyprland-HyprCtl.cpp:394-395,412-413`.  [expect OK]
A2 FALSE-OK short tokens: the window handle is `w->x` at `Hyprland-Target.cpp:10`.  [expect NOFRAG]
A3 FALSE-OK wrapped locator: the goal is `m_realSize->goal()`
(`Hyprland-GeometricMovableAnimated.cpp:999`).  [expect NOFRAG on line 6 above]
A4 FALSE-OK no fragment: the goal accessor is at Hyprland-GeometricMovableAnimated.cpp:999.  [expect NOFRAG]
A5 FALSE-OK numbers: the client asks for `window.set_default_size(640, 720)` at `gkeep-ui-excerpt.py:33-34`.  [expect OK]
A6 FALSE-OK numbers in the rule: the host rule is `windowrule = size 900 1000, match:class ^(org.omarchy.gkeep)$` at `host-gkeep.conf:4`.  [expect OK]
A7 FALSE-MISS qualification: the accessor is `w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL)` at `Hyprland-GeometricMovableAnimated.cpp:19`.  [expect MISS]
A8 negative control, abbreviation passes: the goal is `w->size(GEOMETRIC_GOAL)` at `Hyprland-HyprCtl.cpp:427-428`.  [expect OK]
A9 FALSE-OK reordered quote: the accessors are `m_realSize->value(); case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal()` at `Hyprland-GeometricMovableAnimated.cpp:19-20`.  [expect OK]
A10 FALSE-OK bogus ranges ride along: the goal is `m_realSize->goal()` at `Hyprland-GeometricMovableAnimated.cpp:0,9999,19`.  [expect OK]
A11 FALSE-OK reversed range widens: the goal is `m_realSize->goal()` at `Hyprland-GeometricMovableAnimated.cpp:19-1`.  [expect OK]
A12 FALSE-OK unchecked receipt name: the C1 measurement is `fixtures=37/37 tool=present` at `receipts/c1-after-data.txt:1`.  [expect SKIP, no LOC line]
A13 unscanned dot path: the live run is `NO_MATCHING_CLIENT` at `.ufo/waves/round-43/receipts/live-geometry-host.txt:1`.  [expect no LOC line at all]
