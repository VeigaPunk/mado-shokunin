#!/usr/bin/env python3
"""Corrected / second-round probes for R80ScoutModel (same scratch dir)."""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
TOOL = os.path.join(LANE, "tools", "mado-barfoot.py")
ROOT = "/fast/scratch/hyaku/mado-r80/R80ScoutModel/probe2"


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

# 01b. origin, corrected live entry and band (bar band 34 + panel 40 = 74)
run("01b-origin",
    dict(BAR, **{"margin": 4}),
    {"M2": levels([], [], [layer("waybar", 1924, 4, 1912, 26)],
                  [layer("panel", 1920, 34, 1920, 40)])},
    [mon("M2", 1920, 1080, reserved=(0, 74, 0, 0), x=1920, y=0)],
    surfaces=[{"namespace": "panel", "level": 3, "height": 40}])

# 13b. a band on an edge no declared surface touches
run("13b-phantom-band-other-edge",
    BAR,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 26, 1000, 40)])},
    [mon(reserved=(10, 66, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 40, "exclusive": 40}])

# 14b/14c. same level, equal order: declaration order matching vs reversed
_reply = {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                       [layer("a", 0, 26, 1000, 30), layer("b", 0, 56, 1000, 40)])}
run("14b-order-tie-in-reply-order",
    BAR, _reply, [mon(reserved=(0, 96, 0, 0))],
    surfaces=[{"namespace": "a", "level": 3, "height": 30, "exclusive": 30},
              {"namespace": "b", "level": 3, "height": 40, "exclusive": 40}])
run("14c-order-tie-reversed",
    BAR, _reply, [mon(reserved=(0, 96, 0, 0))],
    surfaces=[{"namespace": "b", "level": 3, "height": 40, "exclusive": 40},
              {"namespace": "a", "level": 3, "height": 30, "exclusive": 30}])

# 15b. gtk auto zone on a dynamic height, source-derived band (collapse to 0)
run("15b-auto-dynamic-source-band",
    BAR,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 126, 1000, 674)])},
    [mon(reserved=(0, 0, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 0,
               "margins": {"top": 100}, "exclusive": "auto"}])

# 16b. gtk auto zone on a dynamic width, source-derived band (collapse to 0)
run("16b-auto-dynamic-width-source-band",
    {"position": "left", "layer": "top", "width": 40},
    {"M1": levels([], [], [layer("waybar", 0, 0, 40, 800)],
                  [layer("panel", 44, 0, 956, 800)])},
    [mon(reserved=(0, 0, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "position": "left", "width": 0,
               "margins": {"left": 4}, "exclusive": "auto"}])

# 22. exclusive -1 with a static reserve: bounds is the FULL monitor box
run("22-minus-one-with-static",
    dict(BAR, **{"margin": 4}),
    {"M1": levels([], [], [layer("waybar", 44, 4, 912, 26)],
                  [layer("wall", 800, 700, 200, 100)])},
    [mon(reserved=(40, 34, 0, 0))],
    surfaces=[{"namespace": "wall", "level": 0, "anchor": ["bottom", "right"],
               "width": 200, "height": 100, "exclusive": -1}],
    rules="monitor = M1, 1000x800@60, 0x0, 1\nmonitor = M1, addreserved, 0, 0, 0, 40\n")

# 24. excluded column: does the bar's own band survive a left/right extra?
run("24-bar-plus-side-columns",
    dict(BAR, **{"margin": 4}),
    {"M1": levels([], [], [layer("waybar", 4, 4, 992, 26)],
                  [layer("dock", 0, 0, 50, 800)])},
    [mon(reserved=(50, 34, 0, 0))],
    surfaces=[{"namespace": "dock", "level": 3, "position": "left", "width": 50,
               "exclusive": 50}])

# 25. declared surface whose live entry carries the default 0,0,0,0 geometry
run("25-unmapped-live-entry",
    BAR,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 0, 0, 0)])},
    [mon(reserved=(0, 26, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 40, "exclusive": 0}])

# 26. non-exclusive bar plus an exclusive extra
run("26-nonexclusive-bar-plus-extra",
    {"position": "top", "layer": "top", "height": 26, "exclusive": False},
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 0, 1000, 40)])},
    [mon(reserved=(0, 40, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 40, "exclusive": 40}])

# 27. auto zone with a POSITIVE opposite margin (covered formula path)
run("27-auto-opposite-margin",
    BAR,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 26, 1000, 40)])},
    [mon(reserved=(0, 76, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 40,
               "margins": {"bottom": 10}, "exclusive": "auto"}])
