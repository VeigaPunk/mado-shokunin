#!/usr/bin/env python3
"""Probe candidate Gate quotes against PRED-C2-r44's own parsers (read-only)."""
import importlib.util, os, re, sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
C = os.path.join(LANE, "quality/counters/c2-r44-gkeep-size-request.py")
spec = importlib.util.spec_from_file_location("c2", C)
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

F = os.path.join(LANE, ".ufo/waves/round-44/fetch/")
FILES = {
    "S164": "Hyprland-Window.cpp",
    "S298": "Hyprland-XDGShell.cpp",
    "S299": "xdg-shell.xml",
    "S300": "gdktoplevel-wayland.c",
    "S301": "gkeep-ui.py",
}
raw = {i: open(F + n, "rb").read() for i, n in FILES.items()}

CANDS = {
 "S164": "if (m_isX11 && m_xwaylandSurface) m_xwaylandSurface->configure({REPORTPOS, REPORTSIZE}); else if (m_xdgSurface && m_xdgSurface->m_toplevel) m_pendingSizeAcks.emplace_back(m_xdgSurface->m_toplevel->setSize(REPORTSIZE), REPORTSIZE.floor());",
 "S298": "m_pendingApply.size = size; scheduleStateApplication(); return m_owner->scheduleConfigure();",
 "S299": "The width and height arguments specify a hint to the window about how its surface should be resized in window geometry coordinates.",
 "S300": "wayland_toplevel->next_layout.size_is_fixed = fixed_size; wayland_surface->next_layout.configured_width = width; wayland_surface->next_layout.configured_height = height;",
 "S301": "window = Gtk.ApplicationWindow(application=self, title=\"gkeep\") window.set_decorated(False) window.set_default_size(420, 500)",
}

fails = 0
for i, q in CANDS.items():
    qn = re.sub(r"\s+", " ", q)
    at = c2.quote_at(raw[i], qn)
    occ = c2.occurrences(raw[i], qn)
    code = c2.quote_in_code(raw[i], qn, FILES[i])
    words = len(qn.split())
    others = [j for j in raw if j != i and qn in c2.norm_receipt(raw[j])]
    ok = (at is not None and len(occ) == 1 and code and 3 <= words <= 25
          and not others)
    fails += 0 if ok else 1
    print("%s file=%s line=%s occ=%d code=%d words=%d others=%s ok=%d"
          % (i, FILES[i], at, len(occ), code, words, others, ok))
    print("    q=%s" % qn)

ok, want = c2.host_census(set(raw), {}, {}, raw, [])
# host_census needs gates mapping id -> [(path,digest,quote)]; build it
gates = {i: [(".ufo/waves/round-44/fetch/" + n, "", "")] for i, n in FILES.items()}
ok2, want2 = c2.host_census(set(raw), {}, gates, raw, [])
print("host_census gates-ok=%d lines=%s" % (ok2, want2))
for w in want2:
    print("CENSUS: " + w)
sys.exit(1 if fails else 0)
