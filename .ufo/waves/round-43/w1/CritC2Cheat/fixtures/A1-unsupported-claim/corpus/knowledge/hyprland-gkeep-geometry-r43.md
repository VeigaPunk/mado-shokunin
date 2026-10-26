# The gkeep window geometry

source: S050 - held parser
source: S290 - receipt
source: S291 - receipt
source: S292 - receipt
source: S293 - receipt
source: S294 - receipt
source: S295 - receipt
source: S296 - receipt
source: S297 - receipt
source: S298 - receipt
source: S299 - receipt
verified-at: 2026-10-26
recheck: 90d

**OBS** S050 handlers and gradients keep the previous angle (S050.txt:1).
**OBS** S290 return re2::RE2::FullMatch(other, *m_regex) != m_negative; (Hyprland-RegexMatchEngine.cpp:16).
**OBS** S291 the compositor applies every rule size to the live client at once, and the client never resizes itself again (static_.size = expr;, Hyprland-WindowRuleApplicator.cpp:426).
**OBS** S292 windowGeometry.w = COMPUTED->x; (Hyprland-DefaultFloatingAlgorithm.cpp:60).
**OBS** S293 m_box = box; (Hyprland-Target.cpp:11).
**OBS** S294 if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) { m_window->setBox(m_box.logicalBox); (Hyprland-WindowTarget.cpp:70).
**OBS** S295 *m_realSize = x.size(); (Hyprland-GeometricMovableAnimated.cpp:45).
**OBS** S296 "size": [{}, {}], (Hyprland-HyprCtl.cpp:395).
**OBS** S297 windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$ (host-gkeep.conf:4).
**OBS** S298 "mapped": true, "class": "chromium", "floating": false, (host-clients-r43.json:49).
**OBS** S299 window.set_default_size(420, 500) self.board = Board(window) (gkeep-ui-excerpt.py:33).

host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$
host clients total=4 floating=0 gkeep=0
gkeep request default_size=420x500 application_id=org.omarchy.gkeep

