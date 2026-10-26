#!/usr/bin/env python3
"""Apply the L1 draft (entry, rows, lesson Gate, README row) to a lane checkout at DIR."""
import hashlib, re, sys, os
D = sys.argv[1]
L1 = os.environ.get("L1DRAFT", "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/l1-draft")
F = ".ufo/waves/round-44/fetch/"
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"
def sha(p): return hashlib.sha256(open(os.path.join(D, F + p), "rb").read()).hexdigest()
def size(p): return os.path.getsize(os.path.join(D, F + p))
C = "efb50993780079460b0cbed1363e2166a2de1d9f"
rows = [
 ("S298", "Hyprland v0.56.2 xdg-shell protocol implementation - the toplevel's setSize and the configure it defers - https://raw.githubusercontent.com/hyprwm/Hyprland/%s/src/protocols/XDGShell.cpp" % C,
  "code", "A", "How the compositor turns a size into an xdg_toplevel.configure event",
  "src/protocols/XDGShell.cpp (receipt Hyprland-XDGShell.cpp:354-358 setSize, Hyprland-XDGShell.cpp:443-462 scheduleStateApplication and its sendConfigure) @ tag v0.56.2 commit %s, %d B sha256:%s; receipt %sHyprland-XDGShell.cpp" % (C, size("Hyprland-XDGShell.cpp"), sha("Hyprland-XDGShell.cpp"), F),
  "setSize stores the size as pending state and returns the next configure serial; a deferred callback sends one configure carrying the pending size and states"),
 ("S299", "wayland-protocols 1.49 xdg-shell protocol XML - xdg_toplevel.configure - https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/stable/xdg-shell/xdg-shell.xml",
  "spec", "A", "What a configure size obliges a client to do (the host's wayland-protocols 1.49-1)",
  "stable/xdg-shell/xdg-shell.xml (xdg-shell.xml:1144-1172 xdg_toplevel event configure, xdg-shell.xml:560-590 xdg_surface request ack_configure) @ tag 1.49, %d B sha256:%s; receipt %sxdg-shell.xml" % (size("xdg-shell.xml"), sha("xdg-shell.xml"), F),
  "The configure width and height are a hint for the window geometry; zero leaves the dimension to the client; the states say how to read the size"),
 ("S300", "GTK 4.24.1 Wayland toplevel - configure handling and layout - https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c",
  "code", "A", "How a GTK 4 client on Wayland stores and applies a configured size (the host's gtk4 1:4.24.1-1)",
  "gdk/wayland/gdktoplevel-wayland.c (gdktoplevel-wayland.c:444-545 compute_size, gdktoplevel-wayland.c:606-700 handle_configure) @ tag 4.24.1, %d B sha256:%s; receipt %sgdktoplevel-wayland.c" % (size("gdktoplevel-wayland.c"), sha("gdktoplevel-wayland.c"), F),
  "A non-zero configured size becomes the next surface size plus shadow margins, constrained by the minimum-size hints; a 0x0 configure leaves the size GTK computes"),
 ("S301", "gkeep application window - the full ui.py at gkeep 133b867 - https://raw.githubusercontent.com/VeigaPunk/gkeep/133b86717a02548aeaff3f1411bf301d936c5308/gkeep/ui.py",
  "code", "A", "What size the gkeep client itself declares, and what it does not",
  "gkeep/ui.py (gkeep-ui.py:446-480 GkeepApp with application_id at gkeep-ui.py:449 and the window at gkeep-ui.py:474-476; gkeep-ui.py:80-91 the button.ink CSS) @ commit 133b86717a02548aeaff3f1411bf301d936c5308, %d B sha256:%s; receipt %sgkeep-ui.py" % (size("gkeep-ui.py"), sha("gkeep-ui.py"), F),
  "gkeep declares an undecorated window with a 420x500 default size and no size request; its only min-width/min-height belong to a button style"),
]
src = open(os.path.join(D, "corpus/SOURCES.md")).read()
lines = src.split("\n")
# S164 used-by extension (cells 1-9 unchanged)
for k, l in enumerate(lines):
    if re.match(r"^\| S164 \|", l):
        cells = l.split("|")
        assert cells[11].strip() == "corpus/knowledge/rule-attribution-r24.md", cells[11]
        cells[11] = " corpus/knowledge/rule-attribution-r24.md, %s " % ENTRY
        lines[k] = "|".join(cells)
last = max(k for k, l in enumerate(lines) if re.match(r"^\| S\d{3,} \|", l))
new = ["| %s | %s | %s | %s | %s | %s | %s | mined | 2026-10-26 | on-release | %s |" % (i, s, kd, t, sc, an, te, ENTRY) for (i, s, kd, t, sc, an, te) in rows]
for r in new: assert r.count("|") == 12, r
lines[last + 1:last + 1] = new
open(os.path.join(D, "corpus/SOURCES.md"), "w").write("\n".join(lines))
quotes = {
 "S164": ("Hyprland-Window.cpp", "return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);"),
 "S298": ("Hyprland-XDGShell.cpp", "m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);"),
 "S299": ("xdg-shell.xml", "The width and height arguments specify a hint to the window about how its surface should be resized"),
 "S300": ("gdktoplevel-wayland.c", "wayland_surface->next_layout.configured_width = width;"),
 "S301": ("gkeep-ui.py", "window.set_decorated(False) window.set_default_size(420, 500)"),
}
gate = ["## Gate", ""]
for i, (f, q) in quotes.items():
    gate.append('GATE %s receipt=%s%s sha256=%s quote="%s"' % (i, F, f, sha(f), q))
gate += ["", "ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md as " + ENTRY,
         "REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-rendered-geometry-record-r13.md reason=the journal route rests on log sweeps no pinned source of this round grounds; flip when a pinned Hyprland log path is opened"]
os.makedirs(os.path.join(D, "corpus/lessons"), exist_ok=True)
open(os.path.join(D, "corpus/lessons/round-44.md"), "w").write("# round 44 (positive control draft)\n\n" + "\n".join(gate) + "\n")
os.makedirs(os.path.join(D, "corpus/knowledge"), exist_ok=True)
open(os.path.join(D, ENTRY), "w").write(open(os.path.join(L1, "entry.md")).read())
rd = open(os.path.join(D, "corpus/README.md")).read().split("\n")
k = max(i for i, l in enumerate(rd) if l.startswith("| `knowledge/hyprland-gkeep-geometry-r43.md`"))
rd.insert(k + 1, "| `knowledge/hyprland-gkeep-size-request-r44.md` (MADO-R44-1, round 44; assimilation of the gkeep residue, successor to the staged `gkeep-client-size-request-r12`) | draft | S164, S298-S301 |")
open(os.path.join(D, "corpus/README.md"), "w").write("\n".join(rd))
print("applied")
