#!/usr/bin/env python3
"""Verify, from the pinned receipts, that each forged sentence is false.

Every check prints the receipt line number it recomputed (never a typed locator).
Output is the receipt evidence-false-lines.txt in this seat directory.
"""
import os
import re
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
CLONE = "/fast/scratch/hyaku/mado-r44/CritC2V2Forgery/clone"
FETCH = os.path.join(CLONE, ".ufo/waves/round-44/fetch")


def lines(name):
    with open(os.path.join(FETCH, name), encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


def find(name, needle, start=1):
    for n, l in enumerate(lines(name), 1):
        if n >= start and needle in l:
            return n
    return 0


def main():
    out = []

    def rec(label, name, needle, expect, start=1):
        n = find(name, needle, start)
        ok = n == expect
        out.append("%-4s %-22s %s:%-4d (expected %d) %s" % (
            "PASS" if ok else "FAIL", label, name, n, expect, needle[:90]))
        return ok

    allok = True
    # F1 / F2 claims and the receipt line that refutes each
    allok &= rec("report-size-not-goal", "Hyprland-Window.cpp",
                 "return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);", 1687)
    allok &= rec("x11-clamp-1x1", "Hyprland-Window.cpp",
                 "REPORTSIZE = m_realSize->goal().clamp(Vector2D{1, 1}", 1691)
    allok &= rec("sendWindowSize-early-return", "Hyprland-Window.cpp",
                 "if (!force && m_pendingReportedSize == REPORTSIZE", 1743)
    allok &= rec("x11-configure-call", "Hyprland-Window.cpp",
                 "m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE});", 1751)
    allok &= rec("onAck-body", "Hyprland-Window.cpp",
                 "void CWindow::onAck(uint32_t serial) {", 1514)
    allok &= rec("onAck-writes-ackedSize", "Hyprland-Window.cpp",
                 ".ackedSize          = m_pendingSizeAck->second;", 1526)
    allok &= rec("setSize-stores-pending", "Hyprland-XDGShell.cpp",
                 "m_pendingApply.size = size;", 355)
    allok &= rec("sendConfigure-reached", "Hyprland-XDGShell.cpp",
                 "m_resource->sendConfigure(m_pendingApply.size.x", 455)
    allok &= rec("zero-means-client-decides", "xdg-shell.xml",
                 "If the width or height arguments are zero, it means the client", 1154)
    allok &= rec("ack_configure-request", "xdg-shell.xml",
                 '<request name="ack_configure">', 560)
    allok &= rec("gtk-stores-configured", "gdktoplevel-wayland.c",
                 "wayland_surface->next_layout.configured_width = width;", 681)
    allok &= rec("gtk-constrain-call", "gdktoplevel-wayland.c",
                 "gdk_surface_constrain_size (&wayland_toplevel->geometry_hints,", 525)
    allok &= rec("gtk-0x0-saved", "gdktoplevel-wayland.c",
                 "saved_size = (width == 0 && height == 0);", 647)
    allok &= rec("gkeep-application-id", "gkeep-ui.py",
                 'application_id="org.omarchy.gkeep",', 449)
    allok &= rec("gkeep-window-build", "gkeep-ui.py",
                 "window.set_decorated(False)", 475)
    allok &= rec("gkeep-default-size", "gkeep-ui.py",
                 "window.set_default_size(420, 500)", 476)

    ui = "\n".join(lines("gkeep-ui.py"))
    n = ui.count("set_size_request(")
    ok = n == 0
    allok &= ok
    out.append("%-4s gkeep-min-request-calls set_size_request( count = %d (census says 0; "
               "so 'asks the toolkit for a minimum window size' is false)" % (
                   "PASS" if ok else "FAIL", n))

    # F4 / F4b: every cited range is the whole file, so the anchor line is inside it by construction
    for name, anchor, L in (
            ("Hyprland-Window.cpp", "Vector2D CWindow::realToReportSize() {", 1685),
            ("Hyprland-XDGShell.cpp", "m_resource->sendConfigure(m_pendingApply.size.x", 455),
            ("xdg-shell.xml", "If the width or height arguments are zero, it means the client", 1154),
            ("gdktoplevel-wayland.c", "wayland_surface->next_layout.configured_width = width;", 681),
            ("gkeep-ui.py", 'application_id="org.omarchy.gkeep",', 449)):
        ln = find(name, anchor)
        print_ok = ln == L
        allok &= print_ok
        out.append("%-4s range-covers %-24s lines=%d anchor=%d" % (
            "PASS" if print_ok else "FAIL", name, len(lines(name)) - 1, ln))

    print("\n".join(out))
    print("VERIFY: %s" % ("PASS" if allok else "FAIL"))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
