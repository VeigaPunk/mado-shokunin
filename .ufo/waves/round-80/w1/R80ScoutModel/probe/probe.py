#!/usr/bin/env python3
"""R80ScoutModel probe harness: run the frozen r80-v1 tool on synthetic composition
fixtures and print the exact rows. Read-only; writes only under this scratch dir."""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
TOOL = os.path.join(LANE, "tools", "mado-barfoot.py")
ROOT = "/fast/scratch/hyaku/mado-r80/R80ScoutModel/probe"


def levels(*per_level):
    out = {}
    for i, entries in enumerate(per_level):
        out[str(i)] = entries
    return {"levels": out}


def layer(ns, x, y, w, h):
    return {"address": "0x1", "x": x, "y": y, "w": w, "h": h, "alpha": 1.0,
            "namespace": ns, "pid": 4242}


def mon(name="M1", w=1000, h=800, reserved=(0, 0, 0, 0), x=None, y=None, scale=1.0,
        transform=0):
    m = {"name": name, "width": w, "height": h, "reserved": list(reserved),
         "scale": scale, "transform": transform}
    if x is not None:
        m["x"] = x
    if y is not None:
        m["y"] = y
    return m


def run(label, config, layers, monitors, surfaces=None, rules=None, monitor=None):
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
            json.dump(surfaces, fh, indent=1)
        argv += ["--surfaces", p]
    if monitor is not None:
        argv += ["--monitor", monitor]
    proc = subprocess.run(argv, cwd=LANE, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True)
    print("### %s  (rc=%d)" % (label, proc.returncode))
    for line in proc.stdout.splitlines():
        print("   " + line)
    if proc.stderr.strip():
        print("   STDERR: " + proc.stderr.strip().replace("\n", " | "))
    print()
    return proc.returncode, proc.stdout


BAR26 = {"position": "top", "layer": "top", "height": 26}

# 1. monitor layout origin, composition path
run("01-origin",
    dict(BAR26, **{"margin": 4}),
    {"M2": levels([], [], [layer("waybar", 1924, 4, 1912, 26)], [])},
    [mon("M2", 1920, 1080, reserved=(0, 66, 0, 0), x=1920, y=0)],
    surfaces=[{"namespace": "panel", "level": 3, "height": 40}])

# 2. static on the SAME edge as the bar plus a second exclusive surface
run("02-origin-static-same-edge",
    dict(BAR26, **{"margin": 4}),
    {"M2": levels([], [], [layer("waybar", 1924, 30, 1912, 26)],
                  [layer("panel", 1920, 60, 1920, 40)])},
    [mon("M2", 1920, 1080, reserved=(0, 100, 0, 0), x=1920, y=0)],
    surfaces=[{"namespace": "panel", "level": 3, "height": 40}],
    rules="monitor = M2, 1920x1080@60, 1920x0, 1\nmonitor = M2, addreserved, 26, 0, 0, 0\n")

# 3. box wider than the bounds (odd difference): double-then-round vs integer centring
run("03-cross-overflow-odd",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", -1, 363, 1002, 100)])},
    [mon(reserved=(0, 26, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "anchor": ["left", "right"],
               "width": 1001, "height": 100, "exclusive": 0}])

# 4. two surfaces of one namespace on one level
run("04-same-namespace-twice",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 26, 1000, 40), layer("panel", 0, 66, 1000, 40)])},
    [mon(reserved=(0, 106, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 40, "exclusive": 40}])

# 5. an EXCLUSIVE surface whose box is empty: continue before applyExclusive
run("05-exclusive-empty-box",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)], [])},
    [mon(reserved=(0, 26, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "anchor": ["left", "right"],
               "height": 100, "margins": {"left": 900, "right": 900},
               "exclusive": 30}])

# 6. zone 0 (not -1): arranged against the running usable box
run("06-zone-zero-top",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("note", 800, 26, 200, 100)])},
    [mon(reserved=(0, 26, 0, 0))],
    surfaces=[{"namespace": "note", "level": 3, "anchor": ["top", "right"],
               "width": 200, "height": 100, "exclusive": 0}])

# 7. zone -2 (not -1): bounds is the usable box, no reserve
run("07-zone-minus-two",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("note", 0, 26, 200, 100)])},
    [mon(reserved=(0, 26, 0, 0))],
    surfaces=[{"namespace": "note", "level": 3, "anchor": ["top", "left"],
               "width": 200, "height": 100, "exclusive": -2}])

# 8. all-four anchors with an exclusive edge: the protocol says "treated as zero"
run("08-allfour-edge",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 400, 350, 200, 100)])},
    [mon(reserved=(0, 56, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3,
               "anchor": ["top", "bottom", "left", "right"], "width": 200,
               "height": 100, "exclusive": 30, "exclusiveEdge": "top"}])

# 9. all-four anchors, no edge
run("09-allfour-noedge",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 400, 350, 200, 100)])},
    [mon(reserved=(0, 26, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3,
               "anchor": ["top", "bottom", "left", "right"], "width": 200,
               "height": 100, "exclusive": 30}])

# 10. corner anchor + exclusive edge on the other corner edge -> left band
run("10-corner-left-edge",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 26, 200, 100)])},
    [mon(reserved=(30, 26, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "anchor": ["top", "left"],
               "width": 200, "height": 100, "exclusive": 30, "exclusiveEdge": "left"}])

# 11. triplet anchor + a different exclusiveEdge: the triplet rule wins
run("11-triplet-edge-ignored",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 26, 1000, 40)])},
    [mon(reserved=(0, 66, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 40, "exclusive": 40,
               "exclusiveEdge": "left"}])

# 12. non-exclusive surface at a LOWER level than the exclusive pass
run("12-nonexclusive-lower-level",
    BAR26,
    {"M1": levels([layer("bg", 0, 700, 100, 100)], [],
                  [layer("waybar", 0, 0, 1000, 26)], [])},
    [mon(reserved=(0, 26, 0, 0))],
    surfaces=[{"namespace": "bg", "level": 0, "anchor": ["bottom", "left"],
               "width": 100, "height": 100, "exclusive": 0}])

# 13. a band on an edge no declared surface touches
run("13-phantom-band-other-edge",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)], [])},
    [mon(reserved=(10, 26, 0, 0))],
    surfaces=[])

# 14. same level, equal order: declaration order reversed against the reply order
run("14-order-tie-reversed",
    BAR26,
    {"M1": levels([], [], [layer("a", 0, 0, 1000, 30), layer("b", 0, 30, 1000, 40)],
                  [])},
    [mon(reserved=(0, 96, 0, 0))],
    surfaces=[{"namespace": "b", "level": 2, "height": 40, "exclusive": 40},
              {"namespace": "a", "level": 2, "height": 30, "exclusive": 30}])

# 15. auto zone on a surface whose band size is dynamic (allocation != 0)
run("15-auto-dynamic-height",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 30, 1000, 770)])},
    [mon(reserved=(0, 796, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 0,
               "margins": {"top": 4}, "exclusive": "auto"}])

# 16. auto zone on a vertical surface with a dynamic width
run("16-auto-dynamic-width",
    {"position": "left", "layer": "top", "width": 40},
    {"M1": levels([], [], [layer("waybar", 0, 0, 40, 800)],
                  [layer("panel", 40, 0, 960, 800)])},
    [mon(reserved=(1000, 0, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "position": "left", "width": 0,
               "margins": {"left": 4}, "exclusive": "auto"}])

# 17. explicit left/right attribution in the composition path
run("17-explicit-left-right",
    dict(BAR26, **{"margin": 4}),
    {"M1": levels([], [], [layer("waybar", 4, 4, 992, 26)],
                  [layer("dock", 0, 0, 50, 800), layer("tray", 950, 0, 50, 800)])},
    [mon(reserved=(50, 34, 50, 0))],
    surfaces=[{"namespace": "dock", "level": 3, "position": "left", "width": 50,
               "height": 0, "exclusive": "auto"},
              {"namespace": "tray", "level": 3, "position": "right", "width": 50,
               "height": 0, "exclusive": "auto"}])

# 18. a band that exactly consumes the axis (usable.h == 0)
run("18-exact-zero-axis",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 26, 1000, 774)])},
    [mon(reserved=(0, 0, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 774, "exclusive": 774}])

# 19. waybar with an explicit width: waybar anchors a singleton, the tool a triplet
run("19-bar-fixed-width",
    {"position": "top", "layer": "top", "height": 26, "width": 800, "margin": 4},
    {"M1": levels([], [], [layer("waybar", 100, 4, 800, 26)], [])},
    [mon(reserved=(0, 34, 0, 0))])

# 20. zone plus a negative anchored margin whose sum stays positive
run("20-negative-margin-positive",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 0, 16, 1000, 100)])},
    [mon(reserved=(0, 46, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "height": 100, "margins": {"top": -10},
               "exclusive": 30}])

# 21. exclusive surface with an auto zone and a corner anchor (gtk sends nothing)
run("21-auto-corner-edge",
    BAR26,
    {"M1": levels([], [], [layer("waybar", 0, 0, 1000, 26)],
                  [layer("panel", 800, 26, 200, 100)])},
    [mon(reserved=(0, 26, 0, 0))],
    surfaces=[{"namespace": "panel", "level": 3, "anchor": ["top", "right"],
               "width": 200, "height": 100, "exclusive": "auto",
               "exclusiveEdge": "top"}])
