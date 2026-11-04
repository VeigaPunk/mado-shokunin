#!/usr/bin/env python3
"""Build the frozen round-77 bar-footprint case set (c1-cases-r77.json).

Run once before the freeze; the generated JSON is the frozen control. This script
writes only the path named by --out. It is evidence, not part of the counter.
"""

import argparse
import json


def layer(ns, x, y, w, h):
    return {"namespace": ns, "x": x, "y": y, "w": w, "h": h, "alpha": 1.0, "pid": 4242}


def layers(monitor, by_level):
    levels = {str(i): [] for i in range(4)}
    for level, entries in by_level.items():
        levels[str(level)] = entries
    return {monitor: {"levels": levels}}


def monitor(name="M1", width=3440, height=1440, reserved=(0, 26, 0, 0)):
    return {
        "id": 1,
        "name": name,
        "description": "fixture",
        "make": "fixture",
        "model": "fixture",
        "serial": "fixture",
        "width": width,
        "height": height,
        "refreshRate": 99.997,
        "x": 0,
        "y": 0,
        "activeWorkspace": {"id": 1, "name": "1"},
        "specialWorkspace": {"id": 0, "name": ""},
        "reserved": list(reserved),
        "scale": 1.0,
        "transform": 0,
        "focused": True,
        "dpmsStatus": True,
        "vrr": False,
    }


CASES = [
    {
        "name": "host-top",
        "config": {"position": "top", "layer": "top", "height": 26, "margin": 0, "exclusive": True},
        "layers": layers("M1", {2: [layer("waybar", 0, 0, 3440, 26)]}),
        "monitors": [monitor()],
        "expect": {"rc": 0, "box": "MATCH", "reserved": "EQ", "verdict": "CLEAN"},
    },
    {
        "name": "bottom-bar",
        "config": {"position": "bottom", "layer": "top", "height": 30},
        "layers": layers("M1", {2: [layer("waybar", 0, 1050, 1920, 30)]}),
        "monitors": [monitor(width=1920, height=1080, reserved=(0, 0, 0, 30))],
        "expect": {"rc": 0, "box": "MATCH", "reserved": "EQ", "verdict": "CLEAN"},
    },
    {
        "name": "css-margins",
        "config": {"position": "top", "layer": "top", "height": 30, "margin": "4 8"},
        "layers": layers("M1", {2: [layer("waybar", 8, 4, 1904, 30)]}),
        "monitors": [monitor(width=1920, height=1080, reserved=(0, 34, 0, 0))],
        "expect": {"rc": 3, "box": "MATCH", "reserved": "NOT_MODELLED", "verdict": "UNMODELLED"},
    },
    {
        "name": "exclusive-false",
        "config": {"position": "top", "layer": "top", "height": 26, "exclusive": False},
        "layers": layers("M1", {2: [layer("waybar", 0, 0, 3440, 26)]}),
        "monitors": [monitor(reserved=(0, 0, 0, 0))],
        "expect": {"rc": 0, "box": "MATCH", "reserved": "NOT_APPLIED", "verdict": "CLEAN"},
    },
    {
        "name": "drift-box",
        "config": {"position": "top", "layer": "top", "height": 26},
        "layers": layers("M1", {2: [layer("waybar", 0, 0, 3440, 28)]}),
        "monitors": [monitor(reserved=(0, 28, 0, 0))],
        "expect": {"rc": 1, "box": "DIFFER", "reserved": "GT", "verdict": "DIFFER"},
    },
    {
        "name": "drift-reserved",
        "config": {"position": "top", "layer": "top", "height": 26},
        "layers": layers("M1", {2: [layer("waybar", 0, 0, 3440, 26)]}),
        "monitors": [monitor(reserved=(0, 0, 0, 0))],
        "expect": {"rc": 1, "box": "MATCH", "reserved": "DIFFER", "verdict": "DIFFER"},
    },
    {
        "name": "declared-level-miss",
        "config": {"position": "top", "layer": "top", "height": 26},
        "layers": layers("M1", {1: [layer("waybar", 0, 0, 3440, 26)]}),
        "monitors": [monitor()],
        "expect": {"rc": 3, "box": "NO_LAYER", "reserved": "NOT_CHECKED", "verdict": "NO_LAYER"},
    },
    {
        "name": "two-monitors",
        "config": {"position": "top", "layer": "top", "height": 24, "output": "M2"},
        "layers": {
            "M1": {"levels": {"0": [], "1": [], "2": [layer("waybar", 0, 0, 1920, 26)], "3": []}},
            "M2": {"levels": {"0": [], "1": [], "2": [layer("waybar", 0, 0, 2560, 24)], "3": []}},
        },
        "monitors": [
            monitor(name="M1", width=1920, height=1080, reserved=(0, 26, 0, 0)),
            monitor(name="M2", width=2560, height=1440, reserved=(0, 24, 0, 0)),
        ],
        "monitor": "M2",
        "expect": {"rc": 0, "box": "MATCH", "reserved": "EQ", "verdict": "CLEAN"},
    },
    {
        "name": "output-excluded",
        "config": {"position": "top", "layer": "top", "height": 26, "output": "!M1"},
        "layers": layers("M1", {2: [layer("waybar", 0, 0, 3440, 26)]}),
        "monitors": [monitor()],
        "expect": {"rc": 3, "box": "NOT_ON_MONITOR", "reserved": "NOT_APPLIED", "verdict": "NO_BAR"},
    },
    {
        "name": "left-vertical",
        "config": {"position": "left", "layer": "top", "width": 40},
        "layers": layers("M1", {2: [layer("waybar", 0, 0, 40, 1080)]}),
        "monitors": [monitor(width=1920, height=1080, reserved=(40, 0, 0, 0))],
        "expect": {"rc": 0, "box": "MATCH", "reserved": "EQ", "verdict": "CLEAN"},
    },
    {
        "name": "wrong-edge-band",
        "config": {"position": "top", "layer": "top", "height": 26},
        "layers": layers("M1", {2: [layer("waybar", 0, 0, 3440, 26)]}),
        "monitors": [monitor(reserved=(26, 0, 0, 0))],
        "expect": {"rc": 1, "box": "MATCH", "reserved": "DIFFER", "verdict": "DIFFER"},
    },
    {
        "name": "centred-width",
        "config": {"position": "top", "layer": "top", "height": 26, "width": 800},
        "layers": layers("M1", {2: [layer("waybar", 1320, 0, 800, 26)]}),
        "monitors": [monitor()],
        "expect": {"rc": 0, "box": "MATCH", "reserved": "EQ", "verdict": "CLEAN"},
    },
    {
        "name": "no-waybar-layer",
        "config": {"position": "top", "layer": "top", "height": 26},
        "layers": layers("M1", {0: [layer("wallpaper", 0, 0, 3440, 1440)]}),
        "monitors": [monitor()],
        "expect": {"rc": 3, "box": "NO_LAYER", "reserved": "NOT_CHECKED", "verdict": "NO_LAYER"},
    },
    {
        "name": "malformed-layers",
        "config": {"position": "top", "layer": "top", "height": 26},
        "layers_raw": "{not json",
        "monitors": [monitor()],
        "expect": {"rc": 2, "error": True, "stage": "setup"},
    },
    {
        "name": "per-side-margin",
        "config": {"position": "top", "layer": "top", "height": 26, "margin-top": 4, "margin-left": 8},
        "layers": layers("M1", {2: [layer("waybar", 8, 4, 3432, 26)]}),
        "monitors": [monitor(reserved=(0, 30, 0, 0))],
        "expect": {"rc": 3, "box": "MATCH", "reserved": "NOT_MODELLED", "verdict": "UNMODELLED"},
    },
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    with open(args.out, "w") as fh:
        json.dump({"version": "r77-v1", "cases": CASES}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote %d cases to %s" % (len(CASES), args.out))


if __name__ == "__main__":
    main()
