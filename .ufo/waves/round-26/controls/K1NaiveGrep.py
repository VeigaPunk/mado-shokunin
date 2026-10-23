#!/usr/bin/env python3
"""C1 NAIVE GREP control: blind walk-order assignments over oracle defaults.

This deliberately does not follow source directives, expand variables, remove
inline comments, or validate directives. Defaults came from the frozen oracle
on a minimal tree; values mirror animations -j's two-decimal float formatting.
"""
import argparse
import json
import os
import re
import struct

DEFAULTS = json.loads(r'''[[{"name":"specialWorkspaceOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"workspacesIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"layersIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeDpms","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"windowsMove","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeGlow","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"zoomFactor","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"shadowangle","overridden":true,"bezier":"default","enabled":false,"speed":1.0,"style":""},{"name":"specialWorkspace","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"glowangle","overridden":true,"bezier":"default","enabled":false,"speed":1.0,"style":""},{"name":"fadeSwitch","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"borderangle","overridden":true,"bezier":"default","enabled":false,"speed":1.0,"style":""},{"name":"fadeOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fade","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"border","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"specialWorkspaceIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"workspaces","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"global","overridden":true,"bezier":"default","enabled":true,"speed":8.0,"style":""},{"name":"__internal_fadeCTM","overridden":true,"bezier":"linear","enabled":true,"speed":5.0,"style":""},{"name":"workspacesOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"layersOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"windowsIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"windowsOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"layers","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadePopups","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeShadow","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeLayers","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"windows","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeLayersIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeLayersOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadeDim","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadePopupsIn","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"monitorAdded","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""},{"name":"fadePopupsOut","overridden":false,"bezier":"","enabled":true,"speed":0.0,"style":""}],[{"name":"linear","X0":0.0,"Y0":0.0,"X1":1.0,"Y1":1.0},{"name":"default","X0":0.0,"Y0":0.75,"X1":0.15,"Y1":1.0}]]''')
DIRECTIVE = re.compile(r"(animation|bezier)\s*=\s*(.*)")


def number(token):
    try:
        value = struct.unpack("f", struct.pack("f", float(token)))[0]
        return float(format(value, ".2f"))
    except (ValueError, OverflowError):
        return token


def resolve(home):
    nodes = {row["name"]: dict(row) for row in DEFAULTS[0]}
    beziers = {row["name"]: dict(row) for row in DEFAULTS[1]}
    for directory, _, filenames in os.walk(home):
        for filename in filenames:
            path = os.path.join(directory, filename)
            if not os.path.isfile(path):
                continue
            with open(path, encoding="utf-8", errors="replace") as stream:
                for line in stream:
                    if line.lstrip().startswith("#"):
                        continue
                    match = DIRECTIVE.search(line)
                    if match is None:
                        continue
                    kind, raw = match.groups()
                    fields = [part.strip() for part in raw.split(",")]
                    fields += [""] * max(0, 5 - len(fields))
                    name = fields[0]
                    if kind == "bezier":
                        beziers[name] = dict(zip(
                            ("name", "X0", "Y0", "X1", "Y1"),
                            [name] + [number(value) for value in fields[1:5]],
                        ))
                    else:
                        enabled = fields[1].lower() in ("1", "true", "yes", "on")
                        nodes[name] = {
                            "name": name,
                            "overridden": True,
                            "bezier": fields[3] if enabled else "default",
                            "enabled": enabled,
                            "speed": number(fields[2]) if enabled else 1.0,
                            "style": fields[4] if enabled else "",
                        }
    return [list(nodes.values()), list(beziers.values())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", required=True)
    args = parser.parse_args()
    print(json.dumps(resolve(args.home)))


if __name__ == "__main__":
    main()
