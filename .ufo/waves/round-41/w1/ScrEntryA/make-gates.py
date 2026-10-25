#!/usr/bin/env python3
"""Emit the exact `## Gate` lines for the C2 entry's cited ids, with the sha256
of each receipt, and verify each line against the counter's GATE_RE + norm.

S037's receipt is this seat's capture; the line it emits names the path the L1
must commit it at (.ufo/waves/round-41/fetch/xdph-installed-version.txt).
"""
import hashlib
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FETCH = os.path.join(LANE, ".ufo", "waves", "round-41", "fetch")
OUT = os.path.join(HERE, "gates.txt")

GATE_RE = re.compile(r'^GATE (S\d{3,}) receipt=(\S+) sha256=([0-9a-f]{64}) '
                     r'quote="(.+)"\s*$')

ROWS = [
    ("S283", ".ufo/waves/round-41/fetch/focus-grab-v1.xml",
     os.path.join(FETCH, "focus-grab-v1.xml"),
     "This interface restricts input focus to a specified whitelist of surfaces"),
    ("S284", ".ufo/waves/round-41/fetch/Hyprland-FocusGrab.cpp",
     os.path.join(FETCH, "Hyprland-FocusGrab.cpp"),
     "m_grab->m_keyboard = true;"),
    ("S285", ".ufo/waves/round-41/fetch/quickshell-grab.cpp",
     os.path.join(FETCH, "quickshell-grab.cpp"),
     "the protocol will always send cleared() when the grab is deactivated,"),
    ("S286", ".ufo/waves/round-41/fetch/xdph-PortalManager.cpp",
     os.path.join(FETCH, "xdph-PortalManager.cpp"),
     "Got interface: {} (ver {})"),
    ("S287", ".ufo/waves/round-41/fetch/issue-565.html",
     os.path.join(FETCH, "issue-565.html"),
     "Tried to set workspace silent rule to a nofocus window!"),
    ("S288", ".ufo/waves/round-41/fetch/protocols-README.md",
     os.path.join(FETCH, "protocols-README.md"),
     "for grabbing input focus, primarily for complex context menus"),
    ("S289", ".ufo/waves/round-41/fetch/xdph-journal.txt",
     os.path.join(FETCH, "xdph-journal.txt"),
     "Got interface: hyprland_focus_grab_manager_v1 (ver 1)"),
    ("S037", ".ufo/waves/round-41/fetch/xdph-installed-version.txt",
     os.path.join(HERE, "s037-installed-version.txt"),
     "%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2"),
]


def norm(text):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text,
                  flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def main():
    lines, bad = [], 0
    for sid, path, local, quote in ROWS:
        raw = open(local, "rb").read()
        digest = hashlib.sha256(raw).hexdigest()
        line = 'GATE %s receipt=%s sha256=%s quote="%s"' % (
            sid, path, digest, quote)
        m = GATE_RE.match(line)
        ok = (m is not None and len(raw) >= 512
              and 3 <= len(quote.split()) <= 25
              and norm(quote) in norm(raw.decode("utf-8", "replace")))
        bad += not ok
        print("%-5s bytes=%6d words=%2d line_ok=%d"
              % (sid, len(raw), len(quote.split()), ok))
        lines.append(line)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote %s (%d lines, %d bad)" % (OUT, len(lines), bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
