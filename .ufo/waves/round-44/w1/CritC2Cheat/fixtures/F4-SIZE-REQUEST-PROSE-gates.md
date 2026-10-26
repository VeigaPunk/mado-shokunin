# round 44 - lessons

## Gate

GATE S164 receipt=.ufo/waves/round-44/fetch/Hyprland-Window.cpp sha256=d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded quote="return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);"
GATE S298 receipt=.ufo/waves/round-44/fetch/Hyprland-XDGShell.cpp sha256=d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0 quote="m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);"
GATE S299 receipt=.ufo/waves/round-44/fetch/xdg-shell.xml sha256=7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df quote="The width and height arguments specify a hint to the window about how its surface should be resized"
GATE S300 receipt=.ufo/waves/round-44/fetch/gdktoplevel-wayland.c sha256=0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe quote="wayland_surface->next_layout.configured_width = width;"
GATE S301 receipt=.ufo/waves/round-44/fetch/gkeep-ui.py sha256=07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a quote="window.set_decorated(False) window.set_default_size(420, 500)"

ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md as corpus/knowledge/hyprland-gkeep-size-request-r44.md
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-geometry-never-recorded-r15.md reason=the journal route is superseded by the pinned client path until a pinned journal receipt exists
