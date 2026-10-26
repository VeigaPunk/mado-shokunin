# Lessons — mado, round 44

## Gate

GATE S164 receipt=.ufo/waves/round-44/fetch/Hyprland-Window.cpp sha256=d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded quote="return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);"
GATE S298 receipt=.ufo/waves/round-44/fetch/Hyprland-XDGShell.cpp sha256=d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0 quote="m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);"
GATE S299 receipt=.ufo/waves/round-44/fetch/xdg-shell.xml sha256=7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df quote="The width and height arguments specify a hint to the window about how its surface should be resized"
GATE S300 receipt=.ufo/waves/round-44/fetch/gdktoplevel-wayland.c sha256=0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe quote="wayland_surface->next_layout.configured_width = width;"
GATE S301 receipt=.ufo/waves/round-44/fetch/gkeep-ui.py sha256=07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a quote="window.set_decorated(False) window.set_default_size(420, 500)"
ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md as corpus/knowledge/hyprland-gkeep-size-request-r44.md
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-rendered-geometry-record-r13.md reason=its decisive receipt is a round-13 journal sweep at a package path that does not exist in this lane, and its Window.cpp half is superseded by held S164; flip if a journal sweep is committed inside this lane and re-shows the map-time line
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-rendered-geometry-record-r14.md reason=one whole-journal sweep outside this lane carries the entire absence claim, and no pinned source of this round touches the journal; flip if the sweep is re-run and committed under this lane's receipts
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-geometry-never-recorded-r15.md reason=its corpus-wide absence claim rests on an artifacts sweep at a package path, which is a different ground from the size-request chain; flip if a lane-committed sweep over this lane's own artifacts reproduces it
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-rendered-geometry-chain-r9.md reason=its two distinctive links need the GTK default-size documentation page and the window-rules wiki, neither pinned this round, and its round-9 receipts are absent from this lane; flip if both pages are pinned and each gets a row

Receipts: the five pre-wave pins (`fetch/`, mode 100644, sha256 equal to `receipts/fetch-sha256.txt`; PRED-C2-r44-v2 clause d now pins the
held S164 receipt too). URLs (opened 2026-10-26): S164 `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/view/Window.cpp`
(held row, `opened 2026-10-23`); S298 `…/efb50993…/src/protocols/XDGShell.cpp`; S299
`https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/stable/xdg-shell/xdg-shell.xml`; S300
`https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c`; S301
`https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py`. Locators the entry carries, computed
by the counter's `quote_at`: `Hyprland-Window.cpp:1687`, `Hyprland-XDGShell.cpp:455`, `xdg-shell.xml:1150`, `gdktoplevel-wayland.c:681`,
`gkeep-ui.py:475` (the S301 quote spans 475-476). The scribe draft's alternative quotes (S164 at :1752, S298 at :354, S301 at :476) were
not used: the L1 draft's quotes are the ones the positive control P was frozen with (`receipts/ctl-c2-v2.txt`).

Rejected staged material, with reasons and flips, is in the REFUSE lines above and the ledger below; the r12 claims the pins refute are
listed in the entry's "What the staged predecessor said" section (w1/ScoutStagedResidue, w1/CritAssimilation).

C1's three grounding pins (`fetch-c1/`) carry no GATE line: no registry row cites them; their sha256 are in `receipts/fetch-sha256.txt`.
