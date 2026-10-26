#!/usr/bin/env python3
"""CritEntryClient (round 44, w2) locator/quote verifier.

Every locator this seat cites is computed here from the bytes: the five round-44 pins under
.ufo/waves/round-44/fetch/ (hashes compared to receipts/fetch-sha256.txt) plus four GTK 4.24.1
files this seat fetched into its own directory (provenance in EXTRA below, hashes printed).

Run: python3 check.py   -> prints the computed locator for every cited line and quote,
exit 0 iff every assertion holds. Log: verify.log.
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
FETCH = os.path.join(LANE, ".ufo/waves/round-44/fetch")

# name -> relative path. Pins under FETCH, this seat's extra GTK files beside this script.
FILES = {
    "xdg-shell.xml": os.path.join(FETCH, "xdg-shell.xml"),
    "gdktoplevel-wayland.c": os.path.join(FETCH, "gdktoplevel-wayland.c"),
    "gkeep-ui.py": os.path.join(FETCH, "gkeep-ui.py"),
    "Hyprland-Window.cpp": os.path.join(FETCH, "Hyprland-Window.cpp"),
    "Hyprland-XDGShell.cpp": os.path.join(FETCH, "Hyprland-XDGShell.cpp"),
    "gtkwindow.c": os.path.join(HERE, "gtkwindow.c"),
    "gdksurface.c": os.path.join(HERE, "gdksurface.c"),
    "gdktoplevelsize.c": os.path.join(HERE, "gdktoplevelsize.c"),
    "gtkapplicationwindow.c": os.path.join(HERE, "gtkapplicationwindow.c"),
}

# url provenance of this seat's extra fetches (GTK tag 4.24.1); hashes are printed, not asserted here
EXTRA_URL = "https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/{}/{}"

# (file, first, last, substring required on one of those lines, why)
CHECKS = [
    # --- xdg-shell 1.49: the state texts that bind the configured size -------------------------
    ("xdg-shell.xml", 839, 847, 'entry name="maximized"', "maximized state entry"),
    ("xdg-shell.xml", 841, 843, "must be obeyed by the client", "maximized: size mandatory"),
    ("xdg-shell.xml", 851, 855, "cannot resize beyond it", "fullscreen: size is a maximum"),
    ("xdg-shell.xml", 860, 863, "cannot resize beyond it", "resizing: size is a maximum"),
    ("xdg-shell.xml", 1150, 1152, "hint to the window", "plain configure: size is a hint"),
    ("xdg-shell.xml", 1151, 1152, "window geometry", "hint is in window geometry coordinates"),
    ("xdg-shell.xml", 1154, 1157, "should decide its own window dimension", "zero dimension -> client"),
    ("xdg-shell.xml", 1159, 1161, "states listed in the event", "states interpret the size"),
    ("xdg-shell.xml", 560, 560, '<request name="ack_configure">', "ack_configure request"),
    ("xdg-shell.xml", 595, 595, 'name="serial" type="uint"', "ack_configure's only argument"),
    ("xdg-shell.xml", 1166, 1166, "must send an ack_configure", "ack is required"),
    ("xdg-shell.xml", 1144, 1144, '<event name="configure">', "xdg_toplevel.configure"),
    ("xdg-shell.xml", 157, 157, '<request name="set_size">', "set_size is xdg_positioner's, not toplevel's"),
    ("xdg-shell.xml", 950, 950, 'name="set_max_size"', "toplevel has set_max_size"),
    ("xdg-shell.xml", 990, 990, 'name="set_min_size"', "toplevel has set_min_size"),
    # --- GTK 4.24.1 gdktoplevel-wayland.c ------------------------------------------------------
    ("gdktoplevel-wayland.c", 490, 490, "gdk_toplevel_layout_get_resizable", "resizable branch"),
    ("gdktoplevel-wayland.c", 492, 494, "gearometry" if False else "geometry.min_width = size.min_width", "min-only hints"),
    ("gdktoplevel-wayland.c", 494, 494, "GDK_HINT_MIN_SIZE", "min-only mask"),
    ("gdktoplevel-wayland.c", 496, 501, "geometry.max_width = geometry.min_width = size.width", "non-resizable: min=max=natural"),
    ("gdktoplevel-wayland.c", 500, 500, "GDK_HINT_MAX_SIZE", "non-resizable mask"),
    ("gdktoplevel-wayland.c", 505, 511, "shadow", "shadow capture"),
    ("gdktoplevel-wayland.c", 518, 521, "shadow_left", "configured size plus shadows"),
    ("gdktoplevel-wayland.c", 523, 528, "should_constrain", "constrain gate"),
    ("gdktoplevel-wayland.c", 525, 528, "gdk_surface_constrain_size", "constrain call"),
    ("gdktoplevel-wayland.c", 530, 530, "gdk_wayland_toplevel_update_size", "size applied"),
    ("gdktoplevel-wayland.c", 532, 537, "size_is_fixed", "one-shot clear"),
    ("gdktoplevel-wayland.c", 539, 547, "gdk_surface_constrain_size", "0x0 else branch also constrains"),
    ("gdktoplevel-wayland.c", 633, 637, "GDK_TOPLEVEL_STATE_MAXIMIZED", "fixed_size states"),
    ("gdktoplevel-wayland.c", 637, 637, "is_resizing", "fixed_size includes resizing"),
    ("gdktoplevel-wayland.c", 647, 647, "saved_size = (width == 0 && height == 0)", "0x0 recognised"),
    ("gdktoplevel-wayland.c", 656, 660, "saved_width", "0x0 after fixed state restores saved size"),
    ("gdktoplevel-wayland.c", 664, 668, "should_constrain = TRUE", "non-0x0 asks for constraint"),
    ("gdktoplevel-wayland.c", 671, 674, "is_resizing", "0x0 while resizing also asks"),
    ("gdktoplevel-wayland.c", 677, 677, "should_constrain = FALSE", "restored saved size not constrained"),
    ("gdktoplevel-wayland.c", 680, 682, "size_is_fixed", "fixed flag and latch"),
    ("gdktoplevel-wayland.c", 684, 690, "configured_width = 0", "no-size branch resets"),
    ("gdktoplevel-wayland.c", 692, 692, "surface_geometry_dirty = TRUE", "layout requested"),
    ("gdktoplevel-wayland.c", 743, 744, "XDG_TOPLEVEL_STATE_RESIZING", "resizing state -> is_resizing"),
    ("gdktoplevel-wayland.c", 746, 760, "GDK_TOPLEVEL_STATE_TILED", "per-edge tiled -> TILED"),
    ("gdktoplevel-wayland.c", 1301, 1306, "shadow_left", "hints exported with shadows subtracted"),
    ("gdktoplevel-wayland.c", 1333, 1334, "set_min_size", "min/max exported to the protocol"),
    ("gdktoplevel-wayland.c", 197, 212, "gdk_wayland_toplevel_save_size", "save_size"),
    ("gdktoplevel-wayland.c", 202, 205, "GDK_TOPLEVEL_STATE_MAXIMIZED", "save_size refuses while fixed"),
    ("gdktoplevel-wayland.c", 210, 211, "saved_width = surface->width", "saved size strips shadows"),
    ("gdktoplevel-wayland.c", 456, 457, "surface_geometry_dirty", "layout pass gate"),
    ("gdktoplevel-wayland.c", 489, 490, "wayland_toplevel->layout", "layout carried into the pass"),
    ("gdktoplevel-wayland.c", 648, 655, "maximize or fullscreen", "GTK's own intent comment for 0x0"),
    ("gdktoplevel-wayland.c", 1857, 1857, "gdk_toplevel_layout_copy (layout)", "present stores the layout"),
    ("gdktoplevel-wayland.c", 1861, 1865, "surface_geometry_dirty = TRUE", "present re-requests a layout"),
    # --- GTK 4.24.1 support files (this seat's fetches) ----------------------------------------
    ("gdksurface.c", 1596, 1611, "CLAMP (width, min_width, max_width)", "constrain = clamp"),
    ("gdksurface.c", 1602, 1606, "GDK_HINT_MAX_SIZE", "max only when the mask carries it"),
    ("gdktoplevelsize.c", 112, 120, "Sets the minimum size of the toplevel", "min is a toplevel min"),
    ("gdktoplevelsize.c", 170, 173, "geometry_width -= size->shadow.left", "bounds are shadow-adjusted"),
    ("gtkwindow.c", 1837, 1837, "priv->resizable = TRUE;", "GtkWindow default resizable"),
    ("gtkwindow.c", 4056, 4056, "gdk_toplevel_layout_set_resizable (layout, priv->resizable)", "resizable reaches the layout"),
    ("gtkwindow.c", 4182, 4183, "!priv->decorated", "decorated FALSE -> no shadow"),
    ("gtkwindow.c", 4206, 4206, "{0, 0, 0, 0}", "shadow zeroed"),
    ("gtkwindow.c", 4463, 4463, "gdk_toplevel_size_set_min_size", "min comes from the widget tree"),
    ("gtkwindow.c", 4456, 4461, "INCLUDE_CSD_SIZE", "min is CSD-inclusive"),
    ("gtkwindow.c", 5864, 5864, "Windows are user resizable by default", "documented default"),
    # --- gkeep 133b867 -------------------------------------------------------------------------
    ("gkeep-ui.py", 474, 474, "Gtk.ApplicationWindow", "the one toplevel"),
    ("gkeep-ui.py", 475, 475, "window.set_decorated(False)", "undecorated"),
    ("gkeep-ui.py", 476, 476, "window.set_default_size(420, 500)", "the only size it declares"),
    ("gkeep-ui.py", 449, 449, 'application_id="org.omarchy.gkeep"', "application id"),
    ("gkeep-ui.py", 80, 80, "button.ink {", "the min-width/min-height rule's selector"),
    ("gkeep-ui.py", 87, 88, "min-height: 30px;", "child style min-height"),
    ("gkeep-ui.py", 88, 88, "min-width: 72px;", "child style min-width"),
    # --- Hyprland efb5099 ----------------------------------------------------------------------
    ("Hyprland-Window.cpp", 1514, 1514, "void CWindow::onAck(uint32_t serial)", "onAck"),
    ("Hyprland-Window.cpp", 1515, 1515, "e.first <= serial", "newest pair not after the ack"),
    ("Hyprland-Window.cpp", 1521, 1521, "erase_if", "drops that pair and every older one"),
    ("Hyprland-Window.cpp", 1526, 1526, "ackedSize", "writes the stored size"),
    ("Hyprland-Window.cpp", 184, 184, "onAck(d)", "ack listener"),
    ("Hyprland-XDGShell.cpp", 150, 150, "CXDGToplevelResource::CXDGToplevelResource", "toplevel constructor"),
    ("Hyprland-XDGShell.cpp", 176, 181, "XDG_TOPLEVEL_STATE_TILED_LEFT", "tiled states pushed at construction"),
    ("Hyprland-XDGShell.cpp", 177, 180, "push_back", "four per-edge tiled states"),
    ("Hyprland-XDGShell.cpp", 361, 361, "m_pendingApply.states", "states list is a member"),
    ("Hyprland-XDGShell.cpp", 443, 443, "scheduleStateApplication", "state application"),
    ("Hyprland-XDGShell.cpp", 452, 455, "sendConfigure(m_pendingApply.size.x", "states copied into every configure"),
    ("Hyprland-XDGShell.cpp", 354, 358, "setSize", "setSize"),
    ("Hyprland-XDGShell.cpp", 455, 455, "sendConfigure", "deferred configure"),
]

# (file, quote, asserted start line or None) - whitespace-normalized, word-bounded occurrences
QUOTES = [
    ("xdg-shell.xml", "The window geometry specified in the configure event must be obeyed by the client", 841),
    ("xdg-shell.xml", "the client cannot resize beyond it", None),
    ("xdg-shell.xml", "The width and height arguments specify a hint to the window about how its surface should be resized", 1150),
    ("xdg-shell.xml", "The width and height arguments specify a hint to the window about how its surface should be resized in window geometry coordinates", 1150),
    ("xdg-shell.xml", "If the width or height arguments are zero, it means the client should decide its own window dimension", 1154),
    ("gdktoplevel-wayland.c", "geometry.max_width = geometry.min_width = size.width", 498),
    ("gdktoplevel-wayland.c", "width = wayland_toplevel->saved_width", 658),
    ("gdktoplevel-wayland.c", "wayland_surface->next_layout.configured_width = width;", 681),
    ("gdktoplevel-wayland.c", "gdk_surface_constrain_size (&wayland_toplevel->geometry_hints,", 525),
    ("gkeep-ui.py", "window.set_decorated(False) window.set_default_size(420, 500)", 475),
    ("gtkwindow.c", "priv->resizable = TRUE;", 1837),
    ("gtkwindow.c", "Windows are user resizable by default", 5864),
    ("gdksurface.c", "width = CLAMP (width, min_width, max_width)", 1610),
    ("gdktoplevelsize.c", "The minimum size corresponds to the limitations the toplevel can be shrunk", 114),
]

# (file, needle, expected count) - absence/occurrence facts
COUNTS = [
    ("gkeep-ui.py", "set_size_request(", 0),
    ("gkeep-ui.py", "set_resizable", 0),
    ("gkeep-ui.py", "Gtk.ApplicationWindow", 1),   # exactly one construction
    ("gtkapplicationwindow.c", "resizable", 0),     # GtkApplicationWindow does not change the default
    ("Hyprland-XDGShell.cpp", "XDG_TOPLEVEL_STATE_TILED", 4),          # four pushes, nothing else
    ("Hyprland-XDGShell.cpp", "std::erase(m_pendingApply.states", 5),  # maximized, fullscreen, activated, resizing, suspended: never tiled
    ("Hyprland-XDGShell.cpp", "m_pendingApply =", 0),                  # the struct is never reset wholesale
    ("Hyprland-XDGShell.cpp", "states.clear", 0),                      # the list is never cleared
]


def collapse(text):
    out, lines, prev = [], [], True
    for ln, line in enumerate(text.split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    out.append(" ")
                    lines.append(ln)
                    prev = True
            else:
                out.append(ch)
                lines.append(ln)
                prev = False
    return "".join(out), lines


def occurrences(blob, nq):
    text = blob.decode("utf-8", "replace")
    flat, lines = collapse(text)
    isw = lambda c: c.isalnum() or c == "_"
    out, start = [], 0
    while True:
        k = flat.find(nq, start)
        if k < 0:
            return out
        before = flat[k - 1] if k > 0 else " "
        after = flat[k + len(nq)] if k + len(nq) < len(flat) else " "
        if not (isw(nq[0]) and isw(before)) and not (isw(nq[-1]) and isw(after)):
            out.append((lines[k], lines[k + len(nq) - 1]))
        start = k + 1


def main():
    raw = {}
    for name, path in FILES.items():
        with open(path, "rb") as fh:
            raw[name] = fh.read()
    print("== file hashes ==")
    for name in sorted(raw):
        print("  %s  %s" % (hashlib.sha256(raw[name]).hexdigest(), name))
    print("  gtkwindow.c url          " + EXTRA_URL.format("gtk", "gtkwindow.c"))
    print("  gdksurface.c url         " + EXTRA_URL.format("gdk", "gdksurface.c"))
    print("  gdktoplevelsize.c url    " + EXTRA_URL.format("gdk", "gdktoplevelsize.c"))
    print("  gtkapplicationwindow.c   " + EXTRA_URL.format("gtk", "gtkapplicationwindow.c"))

    pinfile = os.path.join(LANE, ".ufo/waves/round-44/receipts/fetch-sha256.txt")
    pins = {}
    with open(pinfile) as fh:
        for line in fh:
            parts = line.split()
            if len(parts) >= 2 and re.fullmatch(r"[0-9a-f]{64}", parts[0]):
                pins[os.path.basename(parts[2])] = parts[0]
    print("\n== pins vs receipts/fetch-sha256.txt ==")
    bad = 0
    for name in ("Hyprland-Window.cpp", "Hyprland-XDGShell.cpp", "gdktoplevel-wayland.c", "gkeep-ui.py", "xdg-shell.xml"):
        got = hashlib.sha256(raw[name]).hexdigest()
        ok = got == pins.get(name)
        bad += 0 if ok else 1
        print("  %s %s" % ("PIN-OK " if ok else "PIN-BAD", name))

    print("\n== line assertions ==")
    lines = {n: b.decode("utf-8", "replace").split("\n") for n, b in raw.items()}
    fails = 0
    for name, a, b, sub, why in CHECKS:
        span = lines[name][a - 1:b]
        hit = any(sub in l for l in span)
        if not hit:
            fails += 1
            print("  FAIL %s:%d-%d  %-52s (%s)" % (name, a, b, sub, why))
            for k, l in enumerate(span, a):
                print("       %d: %s" % (k, l))
        else:
            where = [a + i for i, l in enumerate(span) if sub in l]
            print("  OK   %s:%s  %s" % (name, ",".join(map(str, where)), why))
    print("  line assertions=%d fails=%d" % (len(CHECKS), fails))

    print("\n== quotes (whitespace-normalized, word-bounded) ==")
    qfails = 0
    for name, q, want in QUOTES:
        hits = occurrences(raw[name], q)
        spans = ["%d" % a if a == b else "%d-%d" % (a, b) for a, b in hits]
        ok = bool(hits) and (want is None or any(a == want for a, _ in hits))
        qfails += 0 if ok else 1
        print("  %s %s:%s  words=%d  %r" % ("OK  " if ok else "FAIL", name, ",".join(spans), len(q.split()), q))
    print("  quotes=%d fails=%d" % (len(QUOTES), qfails))

    print("\n== occurrence / absence facts ==")
    cfails = 0
    for name, needle, want in COUNTS:
        got = raw[name].decode("utf-8", "replace").count(needle)
        ok = got == want
        cfails += 0 if ok else 1
        print("  %s %-24s %-24r got=%d want=%d" % ("OK  " if ok else "FAIL", name, needle, got, want))

    print("\nRESULT pins_bad=%d line_fails=%d quote_fails=%d count_fails=%d" % (bad, fails, qfails, cfails))
    return 0 if (bad + fails + qfails + cfails) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
