#!/usr/bin/env python3
"""K1NoValidation — mado round 26 C1 control, shape: NO-VALIDATION READER.

Shape (round-26 registration, C1 controls: "no-validation reader (source graph and variables,
accepts every line)"; L1 item text): follow the source graph from
DIR/.config/hypr/hyprland.conf (`source =`, `~`, globs, in read order), expand `$variables`,
strip `#` comments, honour `animations { }` category blocks, and apply every `animation =` /
`bezier =` line in order with last-wins over the embedded default table. No validation is
performed: unknown node names are added, unknown beziers are accepted, and every field is
copied as written (enabled as bool, speed as float, bezier/style raw).

The default table below is Hyprland v0.56.2's own `animations -j` for a tree whose only config
file is `.config/hypr/hyprland.conf` with no animation directive, captured once through the
frozen `.ufo/waves/round-26/harness/oracle.py` (35 nodes, 2 beziers; `/fast/scratch` probe, not
the operator's live table).

Deliberate shape limits, stated so the receipt is interpretable:
  * fields that Hyprland does not copy verbatim (a disabled animation, a non-1 enabled field,
    float32/two-decimal reporting) are copied raw here and will not match;
  * lines Hyprland rejects (unknown node/bezier, bad speed, short bezier) are applied here;
  * a written field overwrites the current row value; an absent field leaves it unchanged.

Usage: python3 -I K1NoValidation.py --home DIR   -> JSON [nodes, beziers].
"""
import argparse
import glob
import json
import os
import re

NODE_NAMES = [
    "global", "windows", "windowsIn", "windowsOut", "windowsMove", "layers", "layersIn",
    "layersOut", "fade", "fadeIn", "fadeOut", "fadeSwitch", "fadeShadow", "fadeDim",
    "fadeLayers", "fadeLayersIn", "fadeLayersOut", "fadePopups", "fadePopupsIn",
    "fadePopupsOut", "fadeDpms", "fadeGlow", "border", "borderangle", "glowangle",
    "shadowangle", "workspaces", "workspacesIn", "workspacesOut", "specialWorkspace",
    "specialWorkspaceIn", "specialWorkspaceOut", "zoomFactor", "monitorAdded",
    "__internal_fadeCTM",
]
SPECIAL = {
    "global": ("default", True, 8.0),
    "borderangle": ("default", False, 1.0),
    "glowangle": ("default", False, 1.0),
    "shadowangle": ("default", False, 1.0),
    "__internal_fadeCTM": ("linear", True, 5.0),
}
DEFAULT_BEZIERS = [
    {"name": "linear", "X0": 0.0, "Y0": 0.0, "X1": 1.0, "Y1": 1.0},
    {"name": "default", "X0": 0.0, "Y0": 0.75, "X1": 0.15, "Y1": 1.0},
]

VAR_REF = re.compile(r"\$[A-Za-z0-9_]+")
VAR_DEF = re.compile(r"^\$([A-Za-z0-9_]+)\s*=\s*(.*)$")


def default_nodes():
    rows = []
    for name in NODE_NAMES:
        if name in SPECIAL:
            bezier, enabled, speed = SPECIAL[name]
            rows.append({"name": name, "overridden": True, "bezier": bezier,
                         "enabled": enabled, "speed": speed, "style": ""})
        else:
            rows.append({"name": name, "overridden": False, "bezier": "",
                         "enabled": True, "speed": 0.0, "style": ""})
    return rows


class Reader:
    def __init__(self, home):
        self.home = home
        self.nodes = {row["name"]: row for row in default_nodes()}
        self.beziers = {row["name"]: dict(row) for row in DEFAULT_BEZIERS}
        self.variables = {}
        self.stack = []

    def run(self):
        root = os.path.join(self.home, ".config/hypr/hyprland.conf")
        self.read_file(root, 0)
        return [list(self.nodes.values()), list(self.beziers.values())]

    def expand(self, text):
        for _ in range(32):
            new = VAR_REF.sub(lambda m: self.variables.get(m.group(0), m.group(0)), text)
            if new == text:
                return text
            text = new
        return text

    def read_file(self, path, depth):
        if depth > 100:
            return
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                text = handle.read()
        except OSError:
            return
        for raw in text.split("\n"):
            line = raw.split("#", 1)[0]
            if not line.strip():
                continue
            match = VAR_DEF.match(line.strip())
            if match:
                self.variables["$" + match.group(1)] = self.expand(match.group(2).strip())
                continue
            line = self.expand(line).strip()
            if line.startswith("}"):
                if self.stack:
                    self.stack.pop()
                continue
            if line.endswith("{"):
                self.stack.append(line[:-1].strip())
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip()
            if key == "source":
                self.source(value, depth)
            elif key in ("animation", "bezier") and (not self.stack or "animations" in self.stack):
                if key == "animation":
                    self.animation(value)
                else:
                    self.bezier(value)

    def source(self, pattern, depth):
        if pattern == "~":
            pattern = self.home
        elif pattern.startswith("~/"):
            pattern = self.home + pattern[1:]
        elif not os.path.isabs(pattern):
            pattern = os.path.join(self.home, pattern)
        for path in sorted(glob.glob(pattern)):
            if os.path.isfile(path):
                self.read_file(path, depth + 1)

    def animation(self, value):
        fields = [field.strip() for field in value.split(",")]
        name = fields[0]
        if not name:
            return
        row = self.nodes.get(name)
        if row is None:
            row = {"name": name, "overridden": True, "bezier": "", "enabled": True,
                   "speed": 0.0, "style": ""}
            self.nodes[name] = row
        else:
            row["overridden"] = True
        if len(fields) > 1 and fields[1]:
            token = fields[1].lower()
            if token in ("true", "yes", "on"):
                row["enabled"] = True
            elif token in ("false", "no", "off"):
                row["enabled"] = False
            else:
                try:
                    row["enabled"] = int(fields[1]) != 0
                except ValueError:
                    pass
        if len(fields) > 2 and fields[2]:
            try:
                row["speed"] = float(fields[2])
            except ValueError:
                pass
        if len(fields) > 3:
            row["bezier"] = fields[3]
        if len(fields) > 4:
            row["style"] = ",".join(fields[4:]).strip()

    def bezier(self, value):
        fields = [field.strip() for field in value.split(",")]
        name = fields[0]
        if not name:
            return
        points = []
        for index in range(1, 5):
            token = fields[index] if len(fields) > index else ""
            try:
                points.append(float(token))
            except ValueError:
                points.append(0.0)
        self.beziers[name] = {"name": name, "X0": points[0], "Y0": points[1],
                              "X1": points[2], "Y1": points[3]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", required=True)
    args = parser.parse_args()
    print(json.dumps(Reader(args.home).run()))


if __name__ == "__main__":
    main()
