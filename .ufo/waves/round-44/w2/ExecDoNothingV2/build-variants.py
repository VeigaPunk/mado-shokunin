#!/usr/bin/env python3
"""Build the shape-keeping do-nothing entry variants from the landed entry.

Landed entry: e4678921:corpus/knowledge/hyprland-gkeep-size-request-r44.md
Each variant keeps only the shapes the two predicates count; the sentences that
carry the claim's content are either deleted (MIN), replaced by false ones
(MINFALSE), or the clause-j surface citations are collapsed to whole-file
ranges (WIDE). Nothing outside the seat dir is written.
"""
import os
import subprocess

REV = "e46789213830597348fe96a351ae004d10587385"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "variants")
os.makedirs(OUT, exist_ok=True)

raw = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (REV, ENTRY)],
                     capture_output=True, check=True).stdout.decode("utf-8")
landed = raw.split("\n")
if landed and landed[-1] == "":
    landed = landed[:-1]
header = landed[:12]          # title .. assimilated-from (landed 1-12)
assert header[0].startswith("# After the box")
assert sum(1 for l in header if l.startswith("source:")) == 5
assert [l.split(":")[0] for l in header].count("verified-at") and (
    sum(1 for l in header if l.startswith("verified-at:")) == 1)
CENSUS_HY = "hyprland sendWindowSize xdg_setSize=1 x11_configure=1"
CENSUS_GK = ("gkeep client default_size=420x500 size_request_calls=0 "
             "application_id=org.omarchy.gkeep")
Q = {
    "S164": "return m_realSize->goal().clamp(Vector2D{0, 0}, Math::VECTOR2D_MAX);",
    "S298": "m_resource->sendConfigure(m_pendingApply.size.x, m_pendingApply.size.y, &arr);",
    "S299": ("The width and height arguments specify a hint to the window about "
             "how its surface should be resized"),
    "S300": "wayland_surface->next_layout.configured_width = width;",
    "S301": "window.set_decorated(False) window.set_default_size(420, 500)",
}

# ---- MIN: landed header verbatim, section skeleton kept, claim lines trimmed
# to (quote, computed locator, surface locator), census lines, nothing else.
MIN_BODY = [
    "## \u00a71 What the compositor reports",
    "## \u00a72 The configure",
    "## \u00a73 What the protocol lets the client do",
    "## \u00a74 What GTK 4.24.1 does with it",
    "## \u00a75 What gkeep declares",
    "",
    "",
    "",
    # S164 + surfaces report-size, send, x11, ack (Window.cpp L 1685/1732/1751/1514)
    "**OBS** S164 - report size (Hyprland-Window.cpp:1685-1699): `" + Q["S164"] +
    "` (Hyprland-Window.cpp:1687); sendWindowSize (Hyprland-Window.cpp:1732-1753);"
    " the X11 path (Hyprland-Window.cpp:1751); the ack handler"
    " (Hyprland-Window.cpp:1514-1526).",
    CENSUS_HY,
    # S298 + surfaces setsize (354), configure (455)
    "**OBS** S298 - setSize (Hyprland-XDGShell.cpp:354-358) and the deferred"
    " sendConfigure (Hyprland-XDGShell.cpp:455): `" + Q["S298"] +
    "` (Hyprland-XDGShell.cpp:455).",
    # S299 + surfaces zero (1154), ack_configure (560)
    "**OBS** S299 - the zero width or height case (xdg-shell.xml:1154-1157) and the"
    " ack_configure request (xdg-shell.xml:560): `" + Q["S299"] +
    "` (xdg-shell.xml:1150).",
    # S300 + surfaces gtk-store (681), gtk-constrain (525), gtk-0x0 (647)
    "**OBS** S300 - the configured-size store (gdktoplevel-wayland.c:681): `" +
    Q["S300"] + "` (gdktoplevel-wayland.c:681), the minimum-size constraint"
    " (gdktoplevel-wayland.c:523-528), the 0x0 case (gdktoplevel-wayland.c:647).",
    # S301 + surface gkeep-id (449)
    "**OBS** S301 - gkeep's application_id line (gkeep-ui.py:449) and its default"
    " size: `" + Q["S301"] + "` (gkeep-ui.py:475).",
    CENSUS_GK,
]

# ---- MINFALSE: the same shapes, every sentence around them false
MINFALSE_BODY = [
    "## \u00a71 What the compositor reports",
    "## \u00a72 The configure",
    "## \u00a73 What the protocol lets the client do",
    "## \u00a74 What GTK 4.24.1 does with it",
    "## \u00a75 What gkeep declares",
    "",
    "",
    "",
    "**OBS** S164 - the report size (Hyprland-Window.cpp:1685-1699) is the monitor"
    " box and Hyprland forces every mapped client to it; sendWindowSize"
    " (Hyprland-Window.cpp:1732-1753) therefore binds the window; the X11 path"
    " (Hyprland-Window.cpp:1751) is the only path a GTK 4 Wayland client takes;"
    " the ack handler (Hyprland-Window.cpp:1514-1526) stores the size the client"
    " chose: `" + Q["S164"] + "` (Hyprland-Window.cpp:1687).",
    CENSUS_HY,
    "**OBS** S298 - setSize (Hyprland-XDGShell.cpp:354-358) lets the client choose"
    " the size and the deferred sendConfigure (Hyprland-XDGShell.cpp:455) is a"
    " request the client may refuse: `" + Q["S298"] +
    "` (Hyprland-XDGShell.cpp:455).",
    "**OBS** S299 - a zero width or height (xdg-shell.xml:1154-1157) means the"
    " compositor picks the size, and the ack_configure request"
    " (xdg-shell.xml:560) carries the client's preferred size: `" + Q["S299"] +
    "` (xdg-shell.xml:1150).",
    "**OBS** S300 - GTK drops the configured size (gdktoplevel-wayland.c:681)"
    " unless it is below the minimum: `" + Q["S300"] +
    "` (gdktoplevel-wayland.c:681); the minimum-size constraint"
    " (gdktoplevel-wayland.c:523-528) is never applied and the 0x0 case"
    " (gdktoplevel-wayland.c:647) never occurs.",
    "**OBS** S301 - gkeep declares no default size and asks for one through a"
    " widget size request (gkeep-ui.py:449), and its application_id is unset: `" +
    Q["S301"] + "` (gkeep-ui.py:475).",
    CENSUS_GK,
]

# ---- WIDE: minimal header, clause j collapsed to one line of whole-file ranges
WIDE_BODY = [""] * 11 + [
    "Locators (whole files): report size sendWindowSize X11 ack"
    " (Hyprland-Window.cpp:1-3000); setSize configure"
    " (Hyprland-XDGShell.cpp:1-2000); zero ack_configure (xdg-shell.xml:1-3000);"
    " configured minimum 0x0 (gdktoplevel-wayland.c:1-2000); application_id"
    " (gkeep-ui.py:1-500).",
    "S164 `" + Q["S164"] + "` (Hyprland-Window.cpp:1687).",
    "S298 `" + Q["S298"] + "` (Hyprland-XDGShell.cpp:455).",
    "S299 `" + Q["S299"] + "` (xdg-shell.xml:1150).",
    "S300 `" + Q["S300"] + "` (gdktoplevel-wayland.c:681).",
    "S301 `" + Q["S301"] + "` (gkeep-ui.py:475).",
    CENSUS_HY,
    CENSUS_GK,
]

# ---- WIDE2: the same whole-file ranges folded onto the five quote lines
WIDE2_BODY = [""] * 11 + [
    "S164 report size sendWindowSize X11 ack (Hyprland-Window.cpp:1-3000): `" +
    Q["S164"] + "` (Hyprland-Window.cpp:1687).",
    "S298 setSize configure (Hyprland-XDGShell.cpp:1-2000): `" + Q["S298"] +
    "` (Hyprland-XDGShell.cpp:455).",
    "S299 zero ack_configure (xdg-shell.xml:1-3000): `" + Q["S299"] +
    "` (xdg-shell.xml:1150).",
    "S300 configured minimum 0x0 (gdktoplevel-wayland.c:1-2000): `" +
    Q["S300"] + "` (gdktoplevel-wayland.c:681).",
    "S301 application_id (gkeep-ui.py:1-500): `" + Q["S301"] +
    "` (gkeep-ui.py:475).",
    CENSUS_HY,
    CENSUS_GK,
]


def write(name, lines):
    text = "\n".join(lines) + "\n"
    path = os.path.join(OUT, name)
    with open(path, "w") as fh:
        fh.write(text)
    for k, l in enumerate(lines):
        if "Hyprland-Window.cpp:1685-1699" in l or "Locators (whole files)" in l:
            assert k >= 20, (name, k)
    print("%s: %d lines" % (name, len(lines)))
    return path


write("min.md", header + MIN_BODY)
write("minfalse.md", header + MINFALSE_BODY)
write("wide.md", header[:9] + WIDE_BODY)
write("wide2.md", header[:9] + WIDE2_BODY)
