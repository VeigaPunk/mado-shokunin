#!/usr/bin/env python3
"""Build the frozen C1 case set for round 81: the thirty-three round-80 cases carried
unchanged, then six cases on the four reachable classes round 80 named NOT_MODELLED
(`corpus/knowledge/bar-footprint-composition-r80.md` §11). Every expectation below is
derived from the cited source arithmetic, not from a tool run.

Writes `.ufo/waves/round-81/controls/c1-cases-r81.json` next to this generator.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
R80 = os.path.join(LANE, ".ufo/waves/round-80/controls/c1-cases-r80.json")
OUT = os.path.join(HERE, "c1-cases-r81.json")

MONITOR = {"name": "M1", "width": 1000, "height": 800, "reserved": [0, 26, 0, 0],
           "scale": 1.0, "transform": 0}
CONFIG = {"height": 26, "layer": "top", "position": "top"}


def entry(namespace, y, h, w=1000, x=0, level=2):
    return {"namespace": namespace, "x": x, "y": y, "w": w, "h": h, "alpha": 1.0,
            "pid": 4242}


def layers(top, *rest):
    levels = {"0": [], "1": [], "2": [], "3": []}
    levels["2"] = [entry("waybar", 0, 26)]
    for level, rows in rest:
        levels[str(level)] = rows
    return {"M1": {"levels": levels}}


def expect(**kw):
    base = {"rc": 0, "box": "MATCH", "boxes": "MATCH,MATCH", "reserved": "EQ",
            "band": 26, "expected": 26, "attributed": 26, "gt": "0,26,0,0",
            "attr": "0,26,0,0", "ls": "VALID", "verdict": "CLEAN"}
    base.update(kw)
    return base


NEW = [
    # 1. CBox::round on an odd overflow past a negative tie (hyprutils Box.cpp:51-63):
    #    x = 0 + (1000/2 - 1001/2) = -0.5 -> round -> -1; w = round(-0.5 + 1001 + 1) = 1002.
    {
        "name": "overflow-tie-negative",
        "config": dict(CONFIG),
        "monitors": [dict(MONITOR)],
        "layers": layers(None, (3, [entry("panel", 363, 100, 1002, -1, 3)])),
        "surfaces": [{"namespace": "panel", "level": 3, "anchor": ["left", "right"],
                      "width": 1001, "height": 100, "exclusive": 0}],
        "monitor": None,
        "expect": expect(attr_ns={"waybar": "top:26"}),
    },
    # 2. auto on a dynamic band height (0): gtk-layer-shell reads current_allocation
    #    (layer-surface.c:276-286), which this join has no input for; a named refusal,
    #    never a zero band.
    {
        "name": "auto-dynamic-band-refused",
        "config": dict(CONFIG),
        "monitors": [dict(MONITOR)],
        "layers": layers(None, (3, [entry("panel", 26, 774)])),
        "surfaces": [{"namespace": "panel", "level": 3, "height": 0, "exclusive": "auto"}],
        "monitor": None,
        "expect": {"error": True, "rc": 3, "stage": "model"},
    },
    # 3. corner anchor + exclusive edge: gtk's auto is gated on
    #    (left == right) ^ (top == bottom) (layer-surface.c:269-288), so a corner pair
    #    sends no zone and the explicit edge matches nothing.
    {
        "name": "auto-corner-edge",
        "config": dict(CONFIG),
        "monitors": [dict(MONITOR)],
        "layers": layers(None, (3, [entry("panel", 26, 100, 200, 0, 3)])),
        "surfaces": [{"namespace": "panel", "level": 3, "anchor": ["top", "left"],
                      "exclusiveEdge": "top", "width": 200, "height": 100,
                      "exclusive": "auto"}],
        "monitor": None,
        "expect": expect(attr_ns={"waybar": "top:26"}),
    },
    # 4. all four anchors: both gates true, so gtk sends no zone; the box centres
    #    at (1000-200)/2 = 400 and (774-100)/2 + 26 = 363 (Renderer.cpp:2613, :2626).
    {
        "name": "auto-all-four-edge",
        "config": dict(CONFIG),
        "monitors": [dict(MONITOR)],
        "layers": layers(None, (3, [entry("panel", 363, 100, 200, 400, 3)])),
        "surfaces": [{"namespace": "panel", "level": 3,
                      "anchor": ["top", "bottom", "left", "right"],
                      "exclusiveEdge": "top", "width": 200, "height": 100,
                      "exclusive": "auto"}],
        "monitor": None,
        "expect": expect(attr_ns={"waybar": "top:26"}),
    },
    # 5. a parallel pair [top, bottom]: left == right (both false) and top == bottom,
    #    so both gates are true and no zone is sent even with an explicit edge.
    {
        "name": "auto-parallel-edge",
        "config": dict(CONFIG),
        "monitors": [dict(MONITOR)],
        "layers": layers(None, (3, [entry("panel", 363, 100, 200, 400, 3)])),
        "surfaces": [{"namespace": "panel", "level": 3, "anchor": ["top", "bottom"],
                      "exclusiveEdge": "top", "width": 200, "height": 100,
                      "exclusive": "auto"}],
        "monitor": None,
        "expect": expect(attr_ns={"waybar": "top:26"}),
    },
    # 6. the vertical gate: a single left anchor is horizontal-false, vertical-true, so
    #    the zone is the allocation width 40 (left anchored, right margin 0). Level 1
    #    arranges first, so the bar's box starts at x=40 and the attribution vector
    #    carries the left band (Renderer.cpp:2673-2700, applyExclusive :2544-2573).
    {
        "name": "auto-left-dock",
        "config": dict(CONFIG),
        "monitors": [dict(MONITOR)],
        "layers": layers(None, (1, [entry("dock", 0, 800, 40, 0, 1)]),
                         (2, [entry("waybar", 0, 26, 960, 40)])),
        "surfaces": [{"namespace": "dock", "level": 1, "anchor": ["left"],
                      "width": 40, "height": 0, "exclusive": "auto"}],
        "monitor": None,
        "expect": expect(attr="40,26,0,0",
                         attr_ns={"dock": "left:40", "waybar": "top:26"}),
    },
]


def main():
    with open(R80) as fh:
        carried = json.load(fh)["cases"]
    assert len(carried) == 33, len(carried)
    cases = carried + NEW
    with open(OUT, "w") as fh:
        json.dump({"lane": "mado", "round": 81, "cases": cases}, fh, indent=1,
                  sort_keys=True)
        fh.write("\n")
    print("wrote %s: %d cases (33 carried + %d new)" % (OUT, len(cases), len(NEW)))


if __name__ == "__main__":
    main()
