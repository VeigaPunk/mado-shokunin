== README.md:72 cells (split on |)
cell1: 
cell2:  `knowledge/hyprland-gkeep-size-request-r44.md` (MADO-R44-1, round 44; assimilation of the gkeep-theme residue, successor path to the held excerpt S297) 
cell3:  What happens after Hyprland sets the gkeep window's box: the compositor takes the real box and reports it (`CWindow::sendWindowSize` calls `realToReportSize`, `Hyprland-Window.cpp:1732` and `:1741`), hands it to the client as an xdg toplevel configure (`setSize` stores the pending size and calls `scheduleConfigure`, `Hyprland-XDGShell.cpp:354-357` and `:629-643`) or as an X11 configure (`Hyprland
cell4:  S164, S298, S299, S300, S301 
cell5: 
