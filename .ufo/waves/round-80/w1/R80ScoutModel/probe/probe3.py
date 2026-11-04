#!/usr/bin/env python3
"""Third probe pass: corrections + the schema-default and protocol-default classes."""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
TOOL = os.path.join(LANE, "tools", "mado-barfoot.py")
ROOT = "/fast/scratch/hyaku/mado-r80/R80ScoutModel/probe3"


def levels(*per_level):
    return {"levels": {str(i): e for i, e in enumerate(per_level)}}


def layer(ns, x, y, w, h):
    return {"address": "0x1", "x": x, "y": y, "w": w, "h": h, "alpha": 1.0,
            "namespace": ns, "pid": 4242}


def mon(name="M1", w=1000, h=800, reserved=(0, 0, 0, 0), x=None, y=None):
    m = {"name": name, "width": w, "height": h, "reserved": list(reserved),
         "scale": 1.0, "transform": 0}
    if x is not None:
        m["x"] = x
    if y is not None:
        m["y"] = y
    return m


def run(label, config, layers, monitors, surfaces=None, rules=None):
    d = os.path.join(ROOT, label)
    os.makedirs(d, exist_ok=True)
    paths = {}
    for key, value in (("config", config), ("layers", layers), ("monitors", monitors)):
        p = os.path.join(d, key + ".json")
        with open(p, "w") as fh:
            json.dump(value, fh, indent=1)
        paths[key] = p
    argv = [sys.executable, "-I", TOOL, "--config", paths["config"],
            "--layers", paths["layers"], "--monitors", paths["monitors"]]
    if rules is not None:
        p = os.path.join(d, "rules.conf")
        with open(p, "w") as fh:
            fh.write(rules)
        argv += ["--rules", p]
    if surfaces is not None:
        p = os.path.join(d, "surfaces.json")
        with open(p, "w") as fh:
            json.dump(surfaces, fh)
        argv += ["--surfaces", p]
    proc = subprocess.run(argv, cwd=LANE, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True)
    print("### %s  (rc=%d)" % (label, proc.returncode))
    for line in proc.stdout.splitlines():
        print("   " + line)
    if proc.stderr.strip():
        print("   STDERR: " + proc.stderr.strip())
    print()
    return proc.returncode, proc.stdout


BAR = {"position": "top", "layer": "top", "height": 26}

# 15c. a surface arranged AFTER an auto/dynamic one: the box diverges, not just the band
run("15c-auto-dynamic-later-surface",
    BAR,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 126, 1000, 674),
                   layer("note", 0, 900, 200, 100)])},
    [mon(reserved=(0, 0, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 0,
               "margins": {"top": 100}, "exclusive": "auto"},
              {"namespace": "note", "level": 3, "anchor": ["bottom", "right"],
               "width": 200, "height": 100, "exclusive": 0}])

# 22b. exclusive -1 with a same-edge static, corrected live rows
run("22b-minus-one-static",
    dict(BAR, **{"margin": 4}),
    {"M1": levels([layer("wall", 800, 700, 200, 100)], [],
                  [layer("waybar", 4, 4, 952, 26)], [])},
    [mon(reserved=(0, 34, 40, 0))],
    surfaces=[{"namespace": "wall", "level": 0, "anchor": ["bottom", "right"],
               "width": 200, "height": 100, "exclusive": -1}],
    rules="monitor = M1, 1000x800@60, 0x0, 1\nmonitor = M1, addreserved, 0, 0, 0, 40\n")

# 24b. bar plus a left column, corrected live rows
run("24b-bar-plus-left-column",
    dict(BAR, **{"margin": 4}),
    {"M1": levels([], [], [layer("waybar", 4, 4, 992, 26)],
                  [layer("dock", 0, 34, 50, 766)])},
    [mon(reserved=(50, 34, 0, 0))],
    surfaces=[{"namespace": "dock", "level": 3, "position": "left", "width": 50,
               "exclusive": 50}])

# 28. protocol-invalid declaration: width 0 with a singleton horizontal anchor
run("28-invalid-dynamic-width",
    BAR,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("odd", 0, 26, 1000, 40)])},
    [mon(reserved=(0, 26, 0, 0))],
    surfaces=[{"namespace": "odd", "level": 3, "anchor": ["top"], "height": 40,
               "exclusive": 0}])

# 29. an extra declared WITHOUT `exclusive`: schema default "auto" vs protocol default 0
run("29-default-exclusive-is-auto",
    BAR,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 26, 1000, 40)])},
    [mon(reserved=(0, 26, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 40}])

# 30. anchor absent on an extra: POSITION_ANCHORS triplet, zone auto
run("30-anchor-absent-auto",
    BAR,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 26, 1000, 40)])},
    [mon(reserved=(0, 66, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 40, "exclusive": 40}])
