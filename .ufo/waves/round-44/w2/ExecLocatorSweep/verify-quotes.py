#!/usr/bin/env python3
"""verify-quotes.py - every quote this report lifts is asserted at its cited line.

Reads the pinned receipts under the lane's round-44 fetch dirs and checks that
the exact quoted text occurs on exactly the line number the report prints.
Exit 0 = every quote located; 1 = a quote is not on its cited line.
"""
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = LANE + "/.ufo/waves/round-44/fetch/"
FETCH_C1 = LANE + "/.ufo/waves/round-44/fetch-c1/"

# (receipt path, cited line, quoted text as the report prints it)
QUOTES = [
    (FETCH + "xdg-shell.xml", 1150, "The width and height arguments specify a hint to the window"),
    (FETCH + "xdg-shell.xml", 1151, "about how its surface should be resized in window geometry"),
    (FETCH + "xdg-shell.xml", 1163, "The states are sent as an array of 32-bit unsigned integers in"),
    (FETCH + "xdg-shell.xml", 1166, "Clients must send an ack_configure in response to this event. See"),
    (FETCH + "gkeep-ui.py", 475, "window.set_decorated(False)"),
    (FETCH + "gkeep-ui.py", 476, "window.set_default_size(420, 500)"),
    (FETCH + "gkeep-ui.py", 449, 'application_id="org.omarchy.gkeep",'),
    (FETCH + "Hyprland-XDGShell.cpp", 354, "uint32_t CXDGToplevelResource::setSize(const Vector2D& size) {"),
    (FETCH + "Hyprland-XDGShell.cpp", 455, "m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);"),
    (FETCH + "Hyprland-Window.cpp", 1751, "m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE});"),
    (FETCH + "Hyprland-Window.cpp", 1865, "m_wlSurface->resource()->m_current.ackedSize;"),
    (FETCH + "gdktoplevel-wayland.c", 633, "fixed_size ="),
    (FETCH + "gdktoplevel-wayland.c", 637, "is_resizing;"),
    (FETCH_C1 + "Hyprland-FullscreenHandler.cpp", 191, "if (TARGET_INTERNAL_MODE == FSMODE_FULLSCREEN) {"),
    (FETCH_C1 + "Hyprland-FullscreenHandler.cpp", 194, "LAYOUT_TARGET->setPositionGlobal(MONBOX);"),
    (FETCH_C1 + "Hyprland-FullscreenHandler.cpp", 195, "} else if (TARGET_INTERNAL_MODE == FSMODE_MAXIMIZED) {"),
    (FETCH_C1 + "Hyprland-FullscreenHandler.cpp", 198, "LAYOUT_TARGET->setPositionGlobal(WORKAREA);"),
    (FETCH_C1 + "Hyprland-FullscreenHandler.cpp", 131, "target->rememberFloatingSize(target->position().size());"),
    (FETCH_C1 + "Hyprland-HyprCtl.cpp", 394, '"at": [{}, {}],'),
    (FETCH_C1 + "Hyprland-HyprCtl.cpp", 412, '"fullscreenHandler": "{}",'),
]

fail = 0
for path, lineno, text in QUOTES:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    line = lines[lineno - 1] if 0 <= lineno - 1 < len(lines) else ""
    ok = text in line
    if not ok:
        fail += 1
    print("QUOTE %s:%d %s text=%r" % (path.rsplit("/", 1)[-1], lineno,
                                      "FOUND" if ok else "ABSENT", text))
print("VERIFY_QUOTES: quotes=%d absent=%d" % (len(QUOTES), fail))
sys.exit(1 if fail else 0)
