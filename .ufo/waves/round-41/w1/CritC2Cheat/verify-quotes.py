#!/usr/bin/env python3
"""Check the genuine quotes the GENUINE-PROXY entry uses: each occurs in its
own frozen fetch file and in exactly one of the nine (the T5 feasibility test).

Quotes are <= 25 words, located at the file named in each row. Uses the frozen
counter's own normalizer (tags/scripts stripped, entities decoded, whitespace
collapsed).
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FETCH = os.path.join(LANE, ".ufo", "waves", "round-41", "fetch")
spec = importlib.util.spec_from_file_location(
    "c2r41", os.path.join(LANE, "quality", "counters",
                          "c2-r41-focus-entry.py"))
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

Q = {
    "focus-grab-v1.xml":
        "This protocol allows clients to limit input focus to a specific set "
        "of surfaces",
    "Hyprland-FocusGrab.cpp":
        "CFocusGrab::refocusKeyboard called with no committed surfaces",
    "quickshell-grab.cpp":
        "bool FocusGrab::isActive() const { return this->active; }",
    "xdph-PortalManager.cpp":
        "Screencopy not started: compositor doesn't support "
        "zwlr_screencopy_v1",
    "protocols-README.md":
        "for grabbing input focus, primarily for complex context menus",
    "xdph-journal.txt":
        "Got interface: hyprland_focus_grab_manager_v1 (ver 1)",
}
texts = {}
for fn in os.listdir(FETCH):
    with open(os.path.join(FETCH, fn), encoding="utf-8", errors="replace") as fh:
        texts[fn] = c2.norm(fh.read())
bad = 0
for own, q in Q.items():
    nq = c2.norm(q)
    hits = sorted(fn for fn, t in texts.items() if nq in t)
    ok = hits == [own] and 3 <= len(q.split()) <= 25
    bad += not ok
    print("QUOTE %-24s words=%2d hits=%s ok=%d"
          % (own, len(q.split()), ",".join(hits), ok))
print("QUOTE_CHECK quotes=%d unique_ok=%d/%d" % (len(Q), len(Q) - bad, len(Q)))
sys.exit(0 if not bad else 1)
