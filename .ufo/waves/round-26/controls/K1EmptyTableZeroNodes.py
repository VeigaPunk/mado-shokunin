#!/usr/bin/env python3
"""mado round-26 C1 control, shape ALL-EMPTY (variant B, the strongest form of the shape).

Prints the 35 animation-node names Hyprland v0.56.2's animation tree contains, each with every
field at its zero value (overridden false, bezier "", enabled true, speed 0, style ""), and an
empty bezier list. The names were observed once from Hyprland itself through
`.ufo/waves/round-26/harness/oracle.py` on a snapshot of the four config roots (see
controls/K1EmptyTable.txt, "NAME ORIGIN"); they are constants of the animation tree, not a table:
no file under DIR is opened and no value is carried.

CLI matches the tool: `python3 -I K1EmptyTableZeroNodes.py --home DIR` -> JSON `[nodes, beziers]`.
"""
import argparse
import json
import sys

# Hyprland v0.56.2 animation tree: 34 configured nodes + the internal CTM fade node.
NAMES = [
    "__internal_fadeCTM", "border", "borderangle", "fade", "fadeDim", "fadeDpms", "fadeGlow",
    "fadeIn", "fadeLayers", "fadeLayersIn", "fadeLayersOut", "fadeOut", "fadePopups",
    "fadePopupsIn", "fadePopupsOut", "fadeShadow", "fadeSwitch", "global", "glowangle", "layers",
    "layersIn", "layersOut", "monitorAdded", "shadowangle", "specialWorkspace",
    "specialWorkspaceIn", "specialWorkspaceOut", "windows", "windowsIn", "windowsMove",
    "windowsOut", "workspaces", "workspacesIn", "workspacesOut", "zoomFactor",
]
ZERO = {"overridden": False, "bezier": "", "enabled": True, "speed": 0.0, "style": ""}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", required=True)
    ap.parse_args()
    nodes = [dict(name=n, **ZERO) for n in NAMES]
    sys.stdout.write(json.dumps([nodes, []]) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
