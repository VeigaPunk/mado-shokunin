#!/usr/bin/env python3
"""K1RootOnly — mado round 26 C1 control, shape: ROOT-ONLY READER.

Shape (registration.md, C1 controls): parse ONLY DIR/.config/hypr/hyprland.conf; never follow
`source =`; apply its `animation =` / `bezier =` lines with simple last-wins rules over Hyprland's
default table, embedded below from a live `hyprctl animations -j` (Hyprland v0.56.2 = efb50993,
via .ufo/waves/round-26/harness/oracle.py on a tree whose only config file is an empty
.config/hypr/hyprland.conf). No variables, no validation.

"Last wins" and the per-line effect are Hyprland's legacy-config semantics for a *well-formed*
line, as observed through the oracle (see w1/reports/K1RootOnly.md):
  enabled field == 1 (Hyprland's `parseInt(...) == 1`) -> the node takes speed/bezier/style;
  any other enabled field -> Hyprland's disable branch: enabled=false, speed=1, bezier "default";
  `bezier = name, x0, y0, x1, y1` replaces or adds `name`.
Both keys are accepted at root level and inside an `animations { ... }` block (hyprlang category),
so braces are ignored; `#` starts a comment; whitespace around `=` and `,` is free.
Because the shape forbids validation, every well-shaped animation/bezier line is applied even where
Hyprland would have rejected it (unknown node or bezier, bad speed, short bezier): values are coerced
leniently (float parse or 1.0 for speed, 0.0 for a missing bezier point, unknown nodes are created).
Reported numbers round like Hyprland's `{:.2f}` over a C++ float (float32) value.

Usage: python3 -I K1RootOnly.py --home DIR   -> JSON [nodes, beziers] in `hyprctl animations -j` shape.
"""
import argparse
import json
import re
import struct
import sys

DEFAULT_JSON = r"""[[{"bezier":"","enabled":true,"name":"specialWorkspaceOut","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"workspacesIn","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"layersIn","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"fadeDpms","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"windowsMove","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"fadeGlow","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"zoomFactor","overridden":false,"speed":0.0,"style":""},{"bezier":"default","enabled":false,"name":"shadowangle","overridden":true,"speed":1.0,"style":""},{"bezier":"","enabled":true,"name":"specialWorkspace","overridden":false,"speed":0.0,"style":""},{"bezier":"default","enabled":false,"name":"glowangle","overridden":true,"speed":1.0,"style":""},{"bezier":"","enabled":true,"name":"fadeSwitch","overridden":false,"speed":0.0,"style":""},{"bezier":"default","enabled":false,"name":"borderangle","overridden":true,"speed":1.0,"style":""},{"bezier":"","enabled":true,"name":"fadeOut","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"fade","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"border","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"specialWorkspaceIn","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"workspaces","overridden":false,"speed":0.0,"style":""},{"bezier":"default","enabled":true,"name":"global","overridden":true,"speed":8.0,"style":""},{"bezier":"linear","enabled":true,"name":"__internal_fadeCTM","overridden":true,"speed":5.0,"style":""},{"bezier":"","enabled":true,"name":"workspacesOut","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"layersOut","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"windowsIn","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"windowsOut","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"layers","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"fadeIn","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"fadePopups","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"fadeShadow","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"fadeLayers","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"windows","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"fadeLayersIn","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"fadeLayersOut","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"fadeDim","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"fadePopupsIn","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"monitorAdded","overridden":false,"speed":0.0,"style":""},{"bezier":"","enabled":true,"name":"fadePopupsOut","overridden":false,"speed":0.0,"style":""}],[{"X0":0.0,"X1":1.0,"Y0":0.0,"Y1":1.0,"name":"linear"},{"X0":0.0,"X1":0.15,"Y0":0.75,"Y1":1.0,"name":"default"}]]"""

ANIM_RE = re.compile(r"^\s*animation\s*=\s*(.*)$")
BEZ_RE = re.compile(r"^\s*bezier\s*=\s*(.*)$")


def f32(x):
    """C++ float (std::stof target), so `{:.2f}` rounding matches Hyprland's float arithmetic."""
    return struct.unpack("f", struct.pack("f", x))[0]


def r2(x):
    """Hyprland prints with `{:.2f}`; json gives the parsed double back."""
    return float("%.2f" % f32(x))


def fnum(text, fallback):
    try:
        return float(text.strip())
    except (TypeError, ValueError):
        return fallback


def load_default():
    nodes, beziers = json.loads(DEFAULT_JSON)
    return ({n["name"]: dict(n) for n in nodes}, {b["name"]: dict(b) for b in beziers})


def apply_animation(node_map, value):
    fields = [f.strip() for f in value.split(",")]
    name = fields[0]
    if not name:
        return
    enabled_field = fields[1] if len(fields) > 1 else ""
    enabled = enabled_field == "1"
    if not enabled:
        node_map[name] = {"name": name, "overridden": True, "bezier": "default", "enabled": False,
                          "speed": 1.0, "style": ""}
        return
    speed = r2(fnum(fields[2], 1.0)) if len(fields) > 2 else 1.0
    bezier = fields[3] if len(fields) > 3 else ""
    style = fields[4] if len(fields) > 4 else ""
    node_map[name] = {"name": name, "overridden": True, "bezier": bezier, "enabled": True,
                      "speed": speed, "style": style}


def apply_bezier(bez_map, value):
    fields = [f.strip() for f in value.split(",")]
    name = fields[0]
    if not name:
        return
    pts = [r2(fnum(fields[i], 0.0)) if len(fields) > i else 0.0 for i in (1, 2, 3, 4)]
    bez_map[name] = {"name": name, "X0": pts[0], "Y0": pts[1], "X1": pts[2], "Y1": pts[3]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", required=True)
    a = ap.parse_args()
    nodes, beziers = load_default()
    path = a.home.rstrip("/") + "/.config/hypr/hyprland.conf"
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        text = ""
    for raw in text.split("\n"):
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        m = ANIM_RE.match(line)
        if m:
            apply_animation(nodes, m.group(1))
            continue
        m = BEZ_RE.match(line)
        if m:
            apply_bezier(beziers, m.group(1))
    out = [[nodes[k] for k in sorted(nodes)], [beziers[k] for k in sorted(beziers)]]
    sys.stdout.write(json.dumps(out, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
