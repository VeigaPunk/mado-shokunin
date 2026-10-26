#!/usr/bin/env python3
"""Verify the ten C2 REAL-table quotes against the pinned fetch receipts.

For each id, locate the whitespace-collapsed quote in its receipt bytes
(same normalization as .ufo/waves/round-43/ctl/run-c2-controls.py:line_of),
print id / file / 1-based line where the quote starts, and assert the quote
occurs at word boundaries (start: prev char not word; end: next char not word).
Also assert each quote is <= 25 words. Output is a receipt.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FETCH = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/fetch"

REAL = {
    "S290": ("Hyprland-RegexMatchEngine.cpp",
             "return re2::RE2::FullMatch(other, *m_regex) != m_negative;"),
    "S291": ("Hyprland-WindowRuleApplicator.cpp", "static_.size = expr;"),
    "S292": ("Hyprland-DefaultFloatingAlgorithm.cpp",
             "windowGeometry.w = COMPUTED->x;"),
    "S293": ("Hyprland-Target.cpp", "m_box = box;"),
    "S294": ("Hyprland-WindowTarget.cpp",
             "if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) { m_window->setBox(m_box.logicalBox);"),
    "S295": ("Hyprland-GeometricMovableAnimated.cpp", "*m_realSize = x.size();"),
    "S296": ("Hyprland-HyprCtl.cpp", '"size": [{}, {}],'),
    "S297": ("host-gkeep.conf",
             "windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$"),
    "S298": ("host-clients-r43.json",
             '"mapped": true, "class": "chromium", "floating": false,'),
    "S299": ("gkeep-ui-excerpt.py",
             "window.set_default_size(420, 500) self.board = Board(window)"),
}

def line_of(data, quote):
    flat, where = [], []
    prev = True
    for ln, line in enumerate(data.split("\n"), 1):
        for ch in line + "\n":
            if ch.isspace():
                if not prev:
                    flat.append(" ")
                    where.append(ln)
                    prev = True
            else:
                flat.append(ch)
                where.append(ln)
                prev = False
    k = "".join(flat).find(re.sub(r"\s+", " ", quote))
    return where[k] if k >= 0 else None

def word_bounded(data, quote):
    nq = re.sub(r"\s+", " ", quote)
    flat = re.sub(r"\s+", " ", data)
    for m in re.finditer(re.escape(nq), flat):
        s, e = m.start(), m.end()
        before_ok = s == 0 or not (flat[s - 1].isalnum() or flat[s - 1] == "_")
        after_ok = e == len(flat) or not (flat[e].isalnum() or flat[e] == "_")
        if before_ok and after_ok:
            return True
    return False

ok = True
for i, (fn, q) in sorted(REAL.items()):
    data = open(os.path.join(FETCH, fn), encoding="utf-8", errors="replace").read()
    ln = line_of(data, q)
    nw = len(q.split())
    bounded = word_bounded(data, q)
    good = ln is not None and bounded and nw <= 25
    ok &= bool(good)
    print("%s %s:%s words=%d bounded=%s %s" % (
        i, fn, ln, nw, bounded, "OK" if good else "FAIL"))

print("ALL=OK" if ok else "ALL=FAIL")
sys.exit(0 if ok else 1)
