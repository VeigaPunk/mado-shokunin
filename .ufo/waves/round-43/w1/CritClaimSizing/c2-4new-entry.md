# The gkeep window geometry

source: S293 - receipt
source: S297 - receipt
source: S298 - receipt
source: S299 - receipt
verified-at: 2026-10-26
recheck: 90d

**OBS** S293 m_box = box; (Hyprland-Target.cpp:11).
**OBS** S297 windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$ (host-gkeep.conf:4).
**OBS** S298 "mapped": true, "class": "chromium", "floating": false, (host-clients-r43.json:49).
**OBS** S299 window.set_default_size(420, 500) self.board = Board(window) (gkeep-ui-excerpt.py:33).

host rules size=420x500 float=on center=on class=^(org.omarchy.gkeep)$
host clients total=4 floating=0 gkeep=0
gkeep request default_size=420x500 application_id=org.omarchy.gkeep
