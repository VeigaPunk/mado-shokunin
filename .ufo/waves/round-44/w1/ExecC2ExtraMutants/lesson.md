# Lessons — mado, round 44

Round intent: registration `.ufo/waves/round-44/registration.md` (freeze `e2289516a9a857f55cda7be635933e89b931c3da`, base
`6a1a90528fe533cadee506a9fa3e9d13d15cc41f`, the round-43 tip after its non-author closure commit). Host `2026-10-26`, Hyprland 0.56.2
(`efb50993780079460b0cbed1363e2166a2de1d9f`), gtk4 1:4.24.1-1, wayland-protocols 1.49-1.

C1 (operability) extends `tools/mado-geometry.py` with the two window states the round-43 tool ignored. C2 (coverage) admits the client-side
half of the gkeep chain: the configure the compositor sends after it has written the box, what xdg-shell allows the client to do with it, what
GTK does with it, and what gkeep itself declares.

## Gate

GATE S164 receipt=.ufo/waves/round-44/fetch/Hyprland-Window.cpp sha256=d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded quote="const auto REPORTSIZE = realToReportSize();"
GATE S298 receipt=.ufo/waves/round-44/fetch/Hyprland-XDGShell.cpp sha256=d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0 quote="m_stateUpdate = g_pEventLoopManager->doLaterLock([this] { configure(); });"
GATE S299 receipt=.ufo/waves/round-44/fetch/xdg-shell.xml sha256=7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df quote="This configure event asks the client to resize its toplevel surface or to change its state."
GATE S300 receipt=.ufo/waves/round-44/fetch/gdktoplevel-wayland.c sha256=0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe quote="if (saved_size && !fixed_size && was_fixed_size)"
GATE S301 receipt=.ufo/waves/round-44/fetch/gkeep-ui.py sha256=07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a quote="window.set_default_size(420, 500) self.board = Board(window)"

ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md as corpus/knowledge/hyprland-gkeep-size-request-r44.md
REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-geometry-never-recorded-r15.md reason=its journal route never names the configure the client receives, so the size it calls unobservable is in fact sent and acked; flip once a pinned source shows the configure skipped for a mapped window

## Assimilation ledger (theme: the gkeep client-side residue; package `merge/mado/`, read-only)

The staged `gkeep-client-size-request-r12.md` is the admitted predecessor: its `sendWindowSize` -> `setSize` -> `scheduleConfigure` chain is
re-derived at the pinned Hyprland commit, and it is extended on the client end (protocol text, GTK handler, the app's own declaration).
