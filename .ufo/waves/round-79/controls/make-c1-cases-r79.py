#!/usr/bin/env python3
"""Build the round-79 C1 control set.

The successor set carries the frozen eighteen round-78 cases byte-identically (asserted by
the counter against the round-78 file) and adds five cases on the ground round 78 left as
`NOT_MODELLED`: the static `monitor = NAME, addreserved, TOP, BOTTOM, LEFT, RIGHT` band
composed under the bar's own contribution.

Every expectation is derived from the sources, not from a tool run:
  * expected band = static[edge] + (extent inside the usable box + opposite margin);
  * the box is arranged inside the usable box (monitor box minus the static reserve);
  * `exclusive: false` prints the would-be band but reports `reserved=NOT_APPLIED`;
  * the newest rule for the selector is the static reserve (`addreserved` sets the slot,
    a positional rule replaces it, another selector never touches it);
  * a `source =` line refuses the join (`stage=model`), because a sourced file is not
    followed.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROUND = os.path.dirname(HERE)
R78 = os.path.join(os.path.dirname(ROUND), "round-78", "controls", "c1-cases-r78.json")
OUT = os.path.join(HERE, "c1-cases-r79.json")


def monitor(name="M1", width=3440, height=1440, reserved=(0, 26, 0, 0)):
    return {"name": name, "width": width, "height": height, "reserved": list(reserved),
            "scale": 1.0, "transform": 0}


def layers(box, namespace="waybar"):
    x, y, w, h = box
    return {"M1": {"levels": {"0": [], "1": [], "2": [
        {"namespace": namespace, "x": x, "y": y, "w": w, "h": h, "alpha": 1.0, "pid": 4242}],
        "3": []}}}


NEW = [
    {
        "name": "static-composed",
        "config": {"position": "top", "layer": "top", "height": 26, "margin": 4},
        "rules": "monitor = M1, 3440x1440@100, 0x0, 1\n"
                  "monitor = M1, addreserved, 26, 0, 0, 0\n",
        "layers": layers((4, 30, 3432, 26)),
        "monitors": [monitor(reserved=(0, 60, 0, 0))],
        "monitor": None,
        "expect": {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 60,
                   "expected": 60, "verdict": "CLEAN"},
    },
    {
        "name": "static-other-edge",
        "config": {"position": "top", "layer": "top", "height": 26},
        "rules": "monitor = M1, 3440x1440@100, 0x0, 1\n"
                  "monitor = M1, addreserved, 0, 0, 40, 0\n",
        "layers": layers((40, 0, 3400, 26)),
        "monitors": [monitor(reserved=(40, 26, 0, 0))],
        "monitor": None,
        "expect": {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 26,
                   "expected": 26, "verdict": "CLEAN"},
    },
    {
        "name": "static-exclusive-false",
        "config": {"position": "top", "layer": "top", "height": 26, "exclusive": False},
        "rules": "monitor = M1, 3440x1440@100, 0x0, 1\n"
                  "monitor = M1, addreserved, 26, 0, 0, 0\n",
        "layers": layers((0, 26, 3440, 26)),
        "monitors": [monitor(reserved=(0, 26, 0, 0))],
        "monitor": None,
        "expect": {"rc": 0, "box": "MATCH", "reserved": "NOT_APPLIED", "band": 26,
                   "expected": 52, "verdict": "CLEAN"},
    },
    {
        "name": "static-last-wins",
        "config": {"position": "top", "layer": "top", "height": 26},
        "rules": ("monitor = M1, 3440x1440@100, 0x0, 1\n"
                  "monitor = M1, addreserved, 10, 0, 0, 0\n"
                  "monitor = M1, addreserved, 26, 0, 0, 0\n"
                  "monitor = M2, addreserved, 5, 0, 0, 0\n"),
        "layers": layers((0, 26, 3440, 26)),
        "monitors": [monitor(reserved=(0, 52, 0, 0)), monitor("M2", 1920, 1080, (0, 0, 0, 0))],
        "monitor": "M1",
        "expect": {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 52,
                   "expected": 52, "verdict": "CLEAN"},
    },
    {
        "name": "static-source-refused",
        "config": {"position": "top", "layer": "top", "height": 26},
        "rules": "source = ~/.config/hypr/other.conf\n",
        "layers": layers((0, 0, 3440, 26)),
        "monitors": [monitor()],
        "monitor": None,
        "expect": {"error": True, "rc": 3, "stage": "model"},
    },
]


def main():
    with open(R78) as fh:
        held = json.load(fh)
    carried = held["cases"]
    if len(carried) != 18:
        raise SystemExit("round-78 set carries %d cases, expected 18" % len(carried))
    names = {case["name"] for case in carried}
    for case in NEW:
        if case["name"] in names:
            raise SystemExit("duplicate case name %r" % case["name"])
    control = {
        "protocol": "mado-c1-r79-v1",
        "carried": "round-78 controls/c1-cases-r78.json, byte-identical prefix",
        "cases": carried + NEW,
    }
    with open(OUT, "w") as fh:
        json.dump(control, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("WROTE %s cases=%d carried=%d new=%d" % (OUT, len(control["cases"]), len(carried),
                                                   len(NEW)))


if __name__ == "__main__":
    main()
