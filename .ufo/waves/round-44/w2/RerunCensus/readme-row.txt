== README index rows for the new note at data rev
72:| `knowledge/hyprland-gkeep-size-request-r44.md` (MADO-R44-1, round 44; assimilation of the gkeep-theme residue, successor path to the held excerpt S297) | What happens after Hyprland sets the gkeep window's box: the compositor takes the real box and reports it (`CWindow::sendWindowSize` calls `realToReportSize`, `Hyprland-Window.cpp:1732` and `:1741`), hands it to the client as an xdg toplevel configure (`setSize` stores the pending size and calls `scheduleConfigure`, `Hyprland-XDGShell.cpp:354-357` and `:629-643`) or as an X11 configure (`Hyprland-Window.cpp:1751`), and queues the configure serial on its pending-size-ack list, cleared by `onAck` (`Hyprland-Window.cpp:1514-1521`); xdg-shell 1.49 calls the configure width and height "a hint to the window" that a client need only acknowledge (`xdg-shell.xml:1144-1165`, ack at `:1163`), GTK 4.24.1's Wayland toplevel applies the configured size through `gdk_wayland_toplevel_update_size` (`gdktoplevel-wayland.c:513-536`), and gkeep 133b867 declares `set_default_size(420, 500)` under `application_id="org.omarchy.gkeep"` with zero `set_size_request` calls (`gkeep-ui.py:449`, `:476`). No client was run and no socket was opened; the ack round-trip and the drawn size stay UNK. | S164, S298, S299, S300, S301 |
314:  and no size request ([size request](knowledge/hyprland-gkeep-size-request-r44.md), rows S164 plus S298-S301).
== README coverage-map header
== note presence/size
8746
== index rows total
61
