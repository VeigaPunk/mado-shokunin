#!/usr/bin/env python3
"""Check every quote the C2 entry carries against the receipt it names, using
the counter's own normalisation (PRED-C2-r41-v1 `norm`).

GATE rows are the strings ScrRowsDraft's row block fixes (one per cited id);
OBS rows are secondary quotes the entry also carries. Exit 0 iff every quote
occurs in its receipt's normalized text, is 3..25 words, and no two ids share
a GATE quote.
"""
import hashlib
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FETCH = os.path.join(LANE, ".ufo", "waves", "round-41", "fetch")

QUOTES = [
    ("S283", "focus-grab-v1.xml", "GATE",
     "This interface restricts input focus to a specified whitelist of surfaces"),
    ("S283", "focus-grab-v1.xml", "OBS",
     "This protocol allows clients to limit input focus to a specific set of surfaces"),
    ("S283", "focus-grab-v1.xml", "OBS",
     "a compositor-picked surface in the whitelist will receive a wl_keyboard::enter event"),
    ("S283", "focus-grab-v1.xml", "OBS",
     "Upon meeting implementation-defined criteria usually meaning a mouse or touch input outside of any whitelisted surfaces"),
    ("S283", "focus-grab-v1.xml", "OBS",
     "If the list previously had no entries and now has at least one, the grab will start."),
    ("S283", "focus-grab-v1.xml", "OBS",
     "doesn't destroy existing focus grab objects"),
    ("S284", "Hyprland-FocusGrab.cpp", "GATE", "m_grab->m_keyboard = true;"),
    ("S284", "Hyprland-FocusGrab.cpp", "OBS",
     "m_grab->setCallback([this]() { finish(true); });"),
    ("S284", "Hyprland-FocusGrab.cpp", "OBS",
     "m_grabActive = true; g_pSeatManager->setGrab(m_grab);"),
    ("S284", "Hyprland-FocusGrab.cpp", "OBS",
     "if (sendCleared) m_resource->sendCleared();"),
    ("S284", "Hyprland-FocusGrab.cpp", "OBS",
     "if (g_pSeatManager->m_seatGrab == m_grab) g_pSeatManager->setGrab(nullptr);"),
    ("S284", "Hyprland-FocusGrab.cpp", "OBS",
     "if (anyCommitted) start(); else finish(true);"),
    ("S284", "Hyprland-FocusGrab.cpp", "OBS",
     "called with no committed surfaces. This should never happen."),
    ("S285", "quickshell-grab.cpp", "GATE",
     "the protocol will always send cleared() when the grab is deactivated,"),
    ("S285", "quickshell-grab.cpp", "OBS",
     "this->pendingAdditions.append(window); this->commitRequired = true;"),
    ("S285", "quickshell-grab.cpp", "OBS",
     "if (!this->active) { this->active = true; emit this->activated(); }"),
    ("S286", "xdph-PortalManager.cpp", "GATE", "Got interface: {} (ver {})"),
    ("S286", "xdph-PortalManager.cpp", "OBS",
     "if (INTERFACE == hyprland_input_capture_manager_v1_interface.name)"),
    ("S287", "issue-565.html", "GATE",
     "Tried to set workspace silent rule to a nofocus window!"),
    ("S287", "issue-565.html", "OBS",
     "If a workspace windowrule contains silent then matching windows should not get focus"),
    ("S287", "issue-565.html", "OBS",
     "When the new window opens in a different workspace, it seems to steal it momentarily"),
    ("S287", "issue-565.html", "OBS", "fixed in b09f157"),
    ("S288", "protocols-README.md", "GATE",
     "for grabbing input focus, primarily for complex context menus"),
    ("S288", "protocols-README.md", "OBS",
     "we have to maintain a set of protocols Hyprland uses"),
    ("S289", "xdph-journal.txt", "GATE",
     "Got interface: hyprland_focus_grab_manager_v1 (ver 1)"),
    ("S289", "xdph-journal.txt", "OBS", "Gathering exported interfaces"),
    ("S289", "xdph-journal.txt", "OBS", "XDG_CURRENT_DESKTOP set to Hyprland"),
    ("S289", "xdph-journal.txt", "OBS",
     "Starting Portal service (Hyprland implementation)"),
    ("S289", "xdph-journal.txt", "OBS",
     "Stopped Portal service (Hyprland implementation)."),
    ("S037", os.path.join(HERE, "s037-installed-version.txt"), "GATE",
     "%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2"),
]


def norm(text):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def main():
    blobs = {}
    bad = 0
    gate = {}
    for sid, rel, kind, quote in QUOTES:
        path = rel if os.path.isabs(rel) else os.path.join(FETCH, rel)
        if path not in blobs:
            with open(path, "rb") as fh:
                raw = fh.read()
            blobs[path] = norm(raw.decode("utf-8", "replace"))
            print("receipt %-32s %7d B sha256 %s"
                  % (os.path.basename(path), len(raw),
                     hashlib.sha256(raw).hexdigest()))
        words = len(quote.split())
        hit = norm(quote) in blobs[path]
        if kind == "GATE":
            dup = gate.setdefault(sid, quote) != quote
        else:
            dup = quote in [q for (s, _, k, q) in QUOTES
                            if k == "GATE" and s != sid]
        ok = hit and 3 <= words <= 25 and not dup
        bad += not ok
        print("%-5s %-4s %-24s words=%2d occurs=%d dup=%d %s"
              % (sid, kind, os.path.basename(path), words, hit, dup,
                 "OK" if ok else "FAIL"))
    ids = sorted({s for s, _, k, _ in QUOTES if k == "GATE"})
    print("ids=%d quotes=%d failed=%d" % (len(ids), len(QUOTES), bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
