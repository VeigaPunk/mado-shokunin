#!/usr/bin/env python3
"""Recompute every locator this seat cites by grepping the receipt bytes; fail loudly on drift.
Receipts grepped: the lane's read-only pins (round-44 fetch/), this seat's fixture copies, and
the frozen counter.  Writes verify-quotes.txt next to itself."""
import os
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SEAT = LANE + "/.ufo/waves/round-44/w1/CritC2Cheat"
FETCH = LANE + "/.ufo/waves/round-44/fetch/"

# (file, expected 1-based line, quote) - every source quote the report lifts
PINS = [
    (FETCH + "Hyprland-Window.cpp", 1687,
     "return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);"),
    (FETCH + "Hyprland-Window.cpp", 1732, "void CWindow::sendWindowSize(bool force) {"),
    (FETCH + "Hyprland-XDGShell.cpp", 455,
     "m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);"),
    (FETCH + "gdktoplevel-wayland.c", 681,
     "wayland_surface->next_layout.configured_width = width;"),
    (FETCH + "gkeep-ui.py", 476, "window.set_default_size(420, 500)"),
    (FETCH + "xdg-shell.xml", 1150,
     "The width and height arguments specify a hint to the window"),
]
# (file, expected line, forged text) - the seat's own fixture bytes
FORGED = [
    (SEAT + "/fixtures/F1-CLAIM-INVERSION-entry.md", 52,
     "always adopts the configured size exactly"),
    (SEAT + "/fixtures/F2-FORGED-PIN-entry.md", 30,
     "never notifies an xdg client of a size change"),
    (SEAT + "/fixtures/F2-FORGED-PIN-entry.md", 32,
     "hyprland sendWindowSize xdg_setSize=0 x11_configure=0"),
    (SEAT + "/fixtures/F3-LOCATION-DRIFT-rows.md", 3, "/raw/1.48/stable/xdg-shell/xdg-shell.xml"),
    (SEAT + "/fixtures/F3-LOCATION-DRIFT-rows.md", 5, "0000000000000000000000000000000000000000"),
    (SEAT + "/fixtures/F4-SIZE-REQUEST-PROSE-entry.md", 60,
     "set_size_request(420, 500)"),
    (SEAT + "/fixtures/F5-DEFAULT-SIZE-PROSE-entry.md", 60, "set_default_size(800, 600)"),
    (SEAT + "/fixtures/F4-SIZE-REQUEST-PROSE-entry.md", 58,
     "gkeep client default_size=420x500 size_request_calls=0"),
    (SEAT + "/fixtures/F4-SIZE-REQUEST-PROSE-entry.md", 32,
     "hyprland sendWindowSize xdg_setSize=1 x11_configure=1"),
    (SEAT + "/fixtures/F5-DEFAULT-SIZE-PROSE-entry.md", 58,
     "gkeep client default_size=420x500 size_request_calls=0"),
    (SEAT + "/fixtures/F5-DEFAULT-SIZE-PROSE-entry.md", 32,
     "hyprland sendWindowSize xdg_setSize=1 x11_configure=1"),
    (SEAT + "/fixtures/F6-OVERCLAIM-TABLE-entry.md", 48,
     "No client may differ from the configure"),
    (SEAT + "/fixtures/F6-OVERCLAIM-TABLE-entry.md", 46,
     "| Does a client have to adopt the configured size? | yes, always | OBS |"),
    (SEAT + "/fixtures/F8-REGISTRY-ANCHOR-LIE-rows.md", 4,
     "the configured size is mandatory for every client"),
    (SEAT + "/fixtures/F9-REGISTRY-ANCHOR-OUT-OF-RANGE-rows.md", 4,
     "gdktoplevel-wayland.c:9999-10005"),
]
# frozen counter anchors for the defect claims
COUNTER = [
    (LANE + "/quality/counters/c2-r44-gkeep-size-request.py", 496, "pin_ok = True"),
    (LANE + "/quality/counters/c2-r44-gkeep-size-request.py", 497, "if i in new_ids:"),
    (LANE + "/quality/counters/c2-r44-gkeep-size-request.py", 603,
     "used = set(os.path.basename(gates[i][0][0]) for i in receipts)"),
    (LANE + "/quality/counters/c2-r43-gkeep-entry.py", 417, "if i in new_ids:"),
]


def check(path, line, needle):
    text = open(path, encoding="utf-8", errors="replace").read().split("\n")
    got = text[line - 1] if 0 < line <= len(text) else ""
    hits = [i + 1 for i, l in enumerate(text) if needle in l]
    ok = needle in got and hits == [line]
    return ok, "%s:%d %s quote=%r hits=%s" % (
        os.path.relpath(path, LANE), line, "OK" if ok else "DRIFT", needle[:60], hits)


def main():
    bad = 0
    out = []
    for path, line, needle in PINS + FORGED + COUNTER:
        ok, msg = check(path, line, needle)
        bad += not ok
        out.append(msg)
    gate = open(SEAT + "/fixtures/F2-FORGED-PIN-gates.md", encoding="utf-8").read()
    line = next(l for l in gate.split("\n") if l.startswith("GATE S164 "))
    pin_sha = "d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded"
    swapped = pin_sha not in line
    out.append("F2 gate S164 carries the pin sha: %s -> %r" % (not swapped, line[:150]))
    bad += not swapped
    out.append("VERDICT: %s (%d checks, %d failures)" % (
        "PASS" if not bad else "FAIL", len(out) - 1, bad))
    open(SEAT + "/verify-quotes.txt", "w").write("\n".join(out) + "\n")
    print("\n".join(out))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
