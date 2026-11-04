#!/usr/bin/env python3
"""mado round 78 — generate the frozen C1 case set for the margined band model.

Each case is a declaration + a captured layer reply + a captured monitor reply, plus the
verdict the r78 model must return. The expectations are derived from the two measured
contributors, never from a run of the tool:

  * gtk-layer-shell 0.10.1 `layer_surface_update_auto_exclusive_zone`: for a horizontal bar
    (left and right anchors agree, top and bottom disagree) the auto zone is the allocation
    height plus the margin of each *unanchored* vertical edge.
  * Hyprland v0.56.2 `applyExclusive`: the exclusive zone plus the anchored edge's margin is
    added to the usable box on that edge.

Waybar anchors a top bar TOP|LEFT|RIGHT and a bottom bar BOTTOM|LEFT|RIGHT, so the band is
`height + margin.top + margin.bottom` (and `width + margin.left + margin.right` transposed).
The box arithmetic is Hyprland's `arrangeLayerArray`.

Usage: python3 make-cases-r78.py --out c1-cases-r78.json
"""
import argparse
import json


def mon(name, w, h, reserved, scale=1.0, transform=0):
    return {"name": name, "width": w, "height": h, "reserved": list(reserved),
            "scale": scale, "transform": transform}


def entry(x, y, w, h, namespace="waybar", pid=4242):
    return {"namespace": namespace, "x": x, "y": y, "w": w, "h": h, "alpha": 1.0, "pid": pid}


def layers(monitor, level, entries):
    levels = {"0": [], "1": [], "2": [], "3": []}
    levels[str(level)] = entries
    return {monitor: {"levels": levels}}


M1 = mon("M1", 3440, 1440, [0, 26, 0, 0])
M1_1920 = mon("M1", 1920, 1080, [0, 30, 0, 0])
M1_1080 = mon("M1", 1920, 1080, [0, 0, 0, 30])

CASES = [
    # name, config, layers, monitors, monitor selection, expectation
    ("host-top",
     {"position": "top", "layer": "top", "height": 26, "margin": 0},
     layers("M1", 2, [entry(0, 0, 3440, 26)]),
     [M1], None,
     {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 26, "expected": 26, "verdict": "CLEAN"}),
    ("bottom-bar",
     {"position": "bottom", "layer": "top", "height": 30},
     layers("M1", 2, [entry(0, 1050, 1920, 30)]),
     [M1_1080], None,
     {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 30, "expected": 30, "verdict": "CLEAN"}),
    ("top-margin-int",
     {"position": "top", "layer": "top", "height": 30, "margin": 4},
     layers("M1", 2, [entry(4, 4, 1912, 30)]),
     [mon("M1", 1920, 1080, [0, 38, 0, 0])], None,
     {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 38, "expected": 38, "verdict": "CLEAN"}),
    ("top-margin-css-2",
     {"position": "top", "layer": "top", "height": 30, "margin": "4 8"},
     layers("M1", 2, [entry(8, 4, 1904, 30)]),
     [mon("M1", 1920, 1080, [0, 38, 0, 0])], None,
     {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 38, "expected": 38, "verdict": "CLEAN"}),
    ("top-margin-asym",
     {"position": "top", "layer": "top", "height": 30, "margin-top": 10, "margin-bottom": 2},
     layers("M1", 2, [entry(0, 10, 1920, 30)]),
     [mon("M1", 1920, 1080, [0, 42, 0, 0])], None,
     {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 42, "expected": 42, "verdict": "CLEAN"}),
    ("bottom-margin",
     {"position": "bottom", "layer": "top", "height": 30, "margin": 8},
     layers("M1", 2, [entry(8, 1042, 1904, 30)]),
     [mon("M1", 1920, 1080, [0, 0, 0, 46])], None,
     {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 46, "expected": 46, "verdict": "CLEAN"}),
    ("left-margin",
     {"position": "left", "layer": "top", "width": 40, "margin": 6},
     layers("M1", 2, [entry(6, 6, 40, 1428)]),
     [mon("M1", 3440, 1440, [52, 0, 0, 0])], None,
     {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 52, "expected": 52, "verdict": "CLEAN"}),
    ("right-margin",
     {"position": "right", "layer": "top", "width": 36, "margin": 5},
     layers("M1", 2, [entry(3399, 5, 36, 1430)]),
     [mon("M1", 3440, 1440, [0, 0, 46, 0])], None,
     {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 46, "expected": 46, "verdict": "CLEAN"}),
    ("right-zero-margin",
     {"position": "right", "layer": "top", "width": 40},
     layers("M1", 2, [entry(1880, 0, 40, 1080)]),
     [mon("M1", 1920, 1080, [0, 0, 40, 0])], None,
     {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 40, "expected": 40, "verdict": "CLEAN"}),
    ("layer-bottom",
     {"position": "top", "layer": "bottom", "height": 28},
     layers("M1", 1, [entry(0, 0, 1920, 28)]),
     [mon("M1", 1920, 1080, [0, 28, 0, 0])], None,
     {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 28, "expected": 28, "verdict": "CLEAN"}),
    ("output-exclusion",
     {"position": "top", "layer": "top", "height": 24, "output": "!M2"},
     layers("M1", 2, [entry(0, 0, 3440, 24)]),
     [mon("M1", 3440, 1440, [0, 24, 0, 0]), mon("M2", 1920, 1080, [0, 0, 0, 0])], "M1",
     {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 24, "expected": 24, "verdict": "CLEAN"}),
    ("output-excluded",
     {"position": "top", "layer": "top", "height": 26, "output": "!M1"},
     layers("M1", 2, [entry(0, 0, 3440, 26)]),
     [M1], None,
     {"rc": 3, "box": "NOT_ON_MONITOR", "reserved": "NOT_APPLIED", "verdict": "NO_BAR"}),
    ("width-with-margins",
     {"position": "top", "layer": "top", "height": 26, "width": 800, "margin": 4},
     layers("M1", 2, [entry(1320, 4, 800, 26)]),
     [mon("M1", 3440, 1440, [0, 34, 0, 0])], None,
     {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 34, "expected": 34, "verdict": "CLEAN"}),
    ("exclusive-false",
     {"position": "top", "layer": "top", "height": 26, "exclusive": False},
     layers("M1", 2, [entry(0, 0, 3440, 26)]),
     [mon("M1", 3440, 1440, [0, 0, 0, 0])], None,
     {"rc": 0, "box": "MATCH", "reserved": "NOT_APPLIED", "band": 0, "verdict": "CLEAN"}),
    ("second-consumer",
     {"position": "top", "layer": "top", "height": 26, "margin": 4},
     layers("M1", 2, [entry(4, 4, 3432, 26)]),
     [mon("M1", 3440, 1440, [0, 60, 0, 0])], None,
     {"rc": 0, "box": "MATCH", "reserved": "GT", "band": 60, "expected": 34, "verdict": "CLEAN"}),
    ("reserved-differ",
     {"position": "top", "layer": "top", "height": 26, "margin": 4},
     layers("M1", 2, [entry(4, 4, 3432, 26)]),
     [mon("M1", 3440, 1440, [0, 26, 0, 0])], None,
     {"rc": 1, "box": "MATCH", "reserved": "DIFFER", "band": 26, "expected": 34, "verdict": "DIFFER"}),
    ("dynamic-cross",
     {"position": "top", "layer": "top", "height": 0},
     layers("M1", 2, []),
     [M1], None,
     {"error": True, "rc": 3}),
    ("negative-margin-refused",
     {"position": "top", "layer": "top", "height": 26, "margin": "-2 0"},
     layers("M1", 2, [entry(0, -2, 3440, 26)]),
     [mon("M1", 3440, 1440, [0, 24, 0, 0])], None,
     {"error": True, "rc": 3}),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    cases = []
    for name, config, layer_reply, monitors, monitor, expect in CASES:
        cases.append({"name": name, "config": config, "layers": layer_reply,
                      "monitors": monitors, "monitor": monitor, "expect": expect})
    payload = {"protocol": "mado-c1-r78-v1", "cases": cases}
    with open(args.out, "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote %s: cases=%d" % (args.out, len(cases)))


if __name__ == "__main__":
    main()
