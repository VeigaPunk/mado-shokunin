#!/usr/bin/env python3
# Verify every gate quote in the focus-grab entry against re-fetched source bytes.
# Exact byte-substring vs whitespace-normalized (newlines/collapsed runs -> single space).
import os, re

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/w2/ExecReopenSources"
FRESH = os.path.join(SEAT, "fresh")
REC = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/fetch"

# row -> (fresh file, receipt file)
FILES = {
    "S283": ("focus-grab-v1.xml", "focus-grab-v1.xml"),
    "S284": ("FocusGrab.cpp", "Hyprland-FocusGrab.cpp"),
    "S285": ("grab.cpp", "quickshell-grab.cpp"),
    "S286": ("PortalManager.cpp", "xdph-PortalManager.cpp"),
    "S287": ("issue-565.html", "issue-565.html"),
    "S288": ("protocols-README.md", "protocols-README.md"),
    "S289": ("xdph-journal.txt", "xdph-journal.txt"),
}

def load(p):
    with open(p, "rb") as f:
        return f.read().decode("utf-8", errors="replace")

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def find_lines(text, q):
    return [i for i, ln in enumerate(text.splitlines(), 1) if q in ln]

QUOTES = [
    ("S283", "This interface restricts input focus to a specified whitelist of surfaces"),
    ("S283", "This protocol allows clients to limit input focus to a specific set of surfaces"),
    ("S283", "doesn't destroy existing focus grab objects"),
    ("S283", "If the list previously had no entries and now has at least one, the grab will start."),
    ("S283", "a compositor-picked surface in the whitelist will receive a wl_keyboard::enter event"),
    ("S283", "Upon meeting implementation-defined criteria usually meaning a mouse or touch input outside of any whitelisted surfaces"),
    ("S284", "m_grab->m_keyboard = true;"),
    ("S284", "m_grab->setCallback([this]() { finish(true); });"),
    ("S284", "m_grabActive = true; g_pSeatManager->setGrab(m_grab);"),
    ("S284", "if (sendCleared) m_resource->sendCleared();"),
    ("S284", "if (g_pSeatManager->m_seatGrab == m_grab) g_pSeatManager->setGrab(nullptr);"),
    ("S284", "if (anyCommitted) start(); else finish(true);"),
    ("S284", "called with no committed surfaces. This should never happen."),
    ("S285", "the protocol will always send cleared() when the grab is deactivated,"),
    ("S285", "this->pendingAdditions.append(window); this->commitRequired = true;"),
    ("S285", "if (!this->active) { this->active = true; emit this->activated(); }"),
    ("S286", 'Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);'),
    ("S286", "if (INTERFACE == hyprland_input_capture_manager_v1_interface.name)"),
    ("S289", "Got interface: hyprland_focus_grab_manager_v1 (ver 1)"),
    ("S289", "Gathering exported interfaces"),
    ("S289", "XDG_CURRENT_DESKTOP set to Hyprland"),
    ("S289", "Starting Portal service (Hyprland implementation)"),
    ("S289", "Stopped Portal service (Hyprland implementation)."),
    ("S289", "-- Boot"),
    ("S288", "for grabbing input focus, primarily for complex context menus"),
    ("S288", "we have to maintain a set of protocols Hyprland uses"),
    ("S287", "windowrule = workspace 4 silent,^(pavucontrol)$"),
    ("S287", "If a workspace windowrule contains silent then matching windows should not get focus"),
    ("S287", "When the new window opens in a different workspace, it seems to steal it momentarily"),
    ("S287", "Tried to set workspace silent rule to a nofocus window!"),
    ("S287", "fixed in b09f157"),
]

print(f"{'row':6} {'words':5} {'exact':6} {'normalized':10} {'fresh_lines'}")
for row, q in QUOTES:
    ff, rf = FILES[row]
    words = len(q.split())
    fresht = load(os.path.join(FRESH, ff))
    qn = norm(q)
    tn = norm(fresht)
    exact = q in fresht
    normok = qn in tn
    fl = find_lines(fresht, q) if exact else find_lines(fresht, qn) or (find_lines(tn, qn) and [])
    print(f"{row:6} {words:<5} {str(exact):6} {str(normok):10} {str(fl)}")
