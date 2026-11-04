#!/usr/bin/env python3
"""Fourth probe pass: the later-surface box divergence under an auto/dynamic neighbour."""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
TOOL = os.path.join(LANE, "tools", "mado-barfoot.py")
ROOT = "/fast/scratch/hyaku/mado-r80/R80ScoutModel/probe4"


def levels(*per_level):
    return {"levels": {str(i): e for i, e in enumerate(per_level)}}


def layer(ns, x, y, w, h):
    return {"address": "0x1", "x": x, "y": y, "w": w, "h": h, "alpha": 1.0,
            "namespace": ns, "pid": 4242}


def mon(reserved=(0, 0, 0, 0)):
    return {"name": "M1", "width": 1000, "height": 800, "reserved": list(reserved),
            "scale": 1.0, "transform": 0}


def run(label, config, layers, monitors, surfaces):
    d = os.path.join(ROOT, label)
    os.makedirs(d, exist_ok=True)
    paths = {}
    for key, value in (("config", config), ("layers", layers), ("monitors", monitors)):
        p = os.path.join(d, key + ".json")
        with open(p, "w") as fh:
            json.dump(value, fh, indent=1)
        paths[key] = p
    p = os.path.join(d, "surfaces.json")
    with open(p, "w") as fh:
        json.dump(surfaces, fh)
    argv = [sys.executable, "-I", TOOL, "--config", paths["config"],
            "--layers", paths["layers"], "--monitors", paths["monitors"],
            "--surfaces", p]
    proc = subprocess.run(argv, cwd=LANE, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True)
    print("### %s  (rc=%d)" % (label, proc.returncode))
    for line in proc.stdout.splitlines():
        print("   " + line)
    print()
    return proc.returncode, proc.stdout


BAR = {"position": "top", "layer": "top", "height": 26}

# 15d. later top-anchored surface: the real usable box starts at y=800, the model's at y=26
run("15d-auto-dynamic-later-top",
    BAR,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 126, 1000, 674),
                   layer("note", 0, 800, 200, 100)])},
    [mon(reserved=(0, 0, 0, 0))],
    [{"namespace": "panel", "level": 3, "height": 0, "margins": {"top": 100},
      "exclusive": "auto"},
     {"namespace": "note", "level": 3, "anchor": ["top", "left"], "width": 200,
      "height": 100, "exclusive": 0}])

# 03b. vertical half-tie: height larger than the bounds by 1, both vertical anchors
run("03b-vertical-half-tie",
    BAR,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 300, -1, 400, 775)])},
    [mon(reserved=(0, 26, 0, 0))],
    [{"namespace": "panel", "level": 3, "anchor": ["top", "bottom"], "width": 400,
      "height": 775, "exclusive": 0}])
