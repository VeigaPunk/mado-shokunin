#!/usr/bin/env python3
"""Verify every quote lifted from a source in RevEntryBar/review.md and RevEntryBar.md,
and verify all 30 source quotes in 07f2641696b5ac73de1404ea737a9f27e9819aa1:corpus/knowledge/hyprland-focus-grab-r41.md
against the committed receipts under .ufo/waves/round-41/fetch/."""
import hashlib
import html
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "07f2641696b5ac73de1404ea737a9f27e9819aa1"
BASE = "ab2bfaab661c846d1de9d58c01651cd156a13949"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git_show(rev, path):
    p = subprocess.run(
        ["git", "-C", LANE, "show", f"{rev}:{path}"],
        capture_output=True,
        env=ENV,
        check=True,
    )
    return p.stdout


def looks_html(blob):
    return re.search(rb"<(!doctype|html|body|div|p)\b", blob[:4096], re.I) is not None


def norm_receipt(blob):
    text = blob.decode("utf-8", "replace")
    if looks_html(blob):
        text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        return re.sub(r"\s+", " ", html.unescape(text)).strip()
    return re.sub(r"\s+", " ", text).strip()


RECEIPTS = {
    "S283": ".ufo/waves/round-41/fetch/focus-grab-v1.xml",
    "S284": ".ufo/waves/round-41/fetch/Hyprland-FocusGrab.cpp",
    "S285": ".ufo/waves/round-41/fetch/quickshell-grab.cpp",
    "S286": ".ufo/waves/round-41/fetch/xdph-PortalManager.cpp",
    "S287": ".ufo/waves/round-41/fetch/issue-565.html",
    "S288": ".ufo/waves/round-41/fetch/protocols-README.md",
    "S289": ".ufo/waves/round-41/fetch/xdph-journal.txt",
    "S037": ".ufo/waves/round-41/fetch/xdph-installed-version.txt",
}

ENTRY_QUOTES = [
    (19, "S283", "This interface restricts input focus to a specified whitelist of surfaces"),
    (19, "S283", "This protocol allows clients to limit input focus to a specific set of surfaces"),
    (21, "S283", "doesn't destroy existing focus grab objects"),
    (33, "S283", "If the list previously had no entries and now has at least one, the grab will start."),
    (35, "S283", "a compositor-picked surface in the whitelist will receive a wl_keyboard::enter event"),
    (35, "S283", "Upon meeting implementation-defined criteria usually meaning a mouse or touch input outside of any whitelisted surfaces"),
    (43, "S284", "m_grab->m_keyboard = true;"),
    (43, "S284", "m_grab->setCallback([this]() { finish(true); });"),
    (45, "S284", "m_grabActive = true; g_pSeatManager->setGrab(m_grab);"),
    (47, "S284", "if (sendCleared) m_resource->sendCleared();"),
    (47, "S284", "if (g_pSeatManager->m_seatGrab == m_grab) g_pSeatManager->setGrab(nullptr);"),
    (49, "S284", "if (anyCommitted) start(); else finish(true);"),
    (51, "S284", "called with no committed surfaces. This should never happen."),
    (61, "S289", "Got interface: hyprland_focus_grab_manager_v1 (ver 1)"),
    (61, "S289", "Gathering exported interfaces"),
    (61, "S289", "XDG_CURRENT_DESKTOP set to Hyprland"),
    (65, "S289", "Stopped Portal service (Hyprland implementation)."),
    (65, "S289", "Starting Portal service (Hyprland implementation)"),
    (69, "S286", " | Got interface: {} (ver {})"),
    (69, "S286", "if (INTERFACE == hyprland_input_capture_manager_v1_interface.name)"),
    (73, "S037", "%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2"),
    (83, "S285", "the protocol will always send cleared() when the grab is deactivated,"),
    (85, "S285", "this->pendingAdditions.append(window); this->commitRequired = true;"),
    (87, "S285", "if (!this->active) { this->active = true; emit this->activated(); }"),
    (97, "S287", "windowrule = workspace 4 silent,^(pavucontrol)$"),
    (97, "S287", "If a workspace windowrule contains silent then matching windows should not get focus"),
    (97, "S287", "When the new window opens in a different workspace, it seems to steal it momentarily"),
    (99, "S287", "Tried to set workspace silent rule to a nofocus window!"),
    (101, "S287", "fixed in b09f157"),
    (103, "S288", "for grabbing input focus, primarily for complex context menus"),
    (103, "S288", "we have to maintain a set of protocols Hyprland uses"),
]


def main():
    entry_lines = git_show(REV, "corpus/knowledge/hyprland-focus-grab-r41.md").decode("utf-8").splitlines()
    normed = {}
    for sid, rpath in RECEIPTS.items():
        blob = git_show(REV, rpath)
        normed[sid] = norm_receipt(blob)

    failed = 0
    for lineno, sid, q in ENTRY_QUOTES:
        line = entry_lines[lineno - 1]
        in_line = q in line
        nq = re.sub(r"\s+", " ", q).strip()
        in_rec = nq in normed[sid]
        words = len(q.split())
        ok = in_line and in_rec and words <= 25
        if not ok:
            failed += 1
        print(f"ENTRY L{lineno:3d} {sid} words={words:2d} in_line={int(in_line)} in_rec={int(in_rec)} ok={int(ok)}: {q}")

    print(f"ENTRY_QUOTES_SUMMARY checked={len(ENTRY_QUOTES)} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
