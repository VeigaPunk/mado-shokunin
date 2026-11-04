#!/usr/bin/env python3
"""Generate `.ufo/waves/round-80/controls/c1-cases-r80.json`.

The first twenty-three cases are the round-79 frozen set, carried unchanged. The nine
new cases declare a second layer surface (or a third arrangement rule) and their
expectations are derived by hand from Hyprland 0.56.2:

* `Renderer.cpp:2673-2700` arranges every level in order against a *running* usable
  box, resets `RESERVED_DYNAMIC_TYPE_LS`, and adds one `CReservedArea{ORIGINAL, usable}`.
* `Renderer.cpp:2587-2671` places each surface's box against the current bounds, skips an
  empty box, and calls `applyExclusive` after placing it.
* `Renderer.cpp:2529-2586` matches the top/bottom/left/right rules in that order on
  `(exclusiveEdge == singular || anchor == singular || anchor == triplet)` and
  `zone + margin(edge) > 0`, then moves the positive axis (top/left) and/or shrinks.
* `ReservedArea.cpp:9-31` zeroes the whole area when the child box is empty or not
  contained in the parent.
"""

import json
import os

BASE = ".ufo/waves/round-79/controls/c1-cases-r79.json"
OUT = ".ufo/waves/round-80/controls/c1-cases-r80.json"

M = {"name": "M1", "width": 1000, "height": 800, "scale": 1.0, "transform": 0}


def monitor(reserved):
    item = dict(M)
    item["reserved"] = reserved
    return [item]


def levels(*entries):
    reply = dict((str(index), []) for index in range(4))
    for level, items in entries:
        reply[str(level)] = items
    return {"M1": {"levels": reply}}


def entry(namespace, box, pid=4242):
    x, y, w, h = box
    return {"namespace": namespace, "x": x, "y": y, "w": w, "h": h, "alpha": 1.0, "pid": pid}


def case(name, config, layer_entries, reserved, surfaces, expect):
    return {
        "name": name,
        "config": config,
        "layers": levels(*layer_entries),
        "monitors": monitor(reserved),
        "surfaces": surfaces,
        "monitor": None,
        "expect": expect,
    }


TOP_BAR = {"position": "top", "layer": "top", "height": 26}

CASES = [
    # A. a later level is arranged against the box the earlier level already shrank
    case("overlay-compose-top", dict(TOP_BAR),
         [(2, [entry("waybar", (0, 0, 1000, 26))]),
          (3, [entry("panel", (0, 26, 1000, 40))])],
         [0, 66, 0, 0],
         [{"namespace": "panel", "level": 3, "height": 40}],
         {"rc": 0, "box": "MATCH", "boxes": "MATCH,MATCH", "reserved": "EQ",
          "band": 66, "expected": 66, "attributed": 66, "gt": "0,66,0,0",
          "attr": "0,66,0,0", "ls": "VALID", "verdict": "CLEAN",
          "attr_ns": {"waybar": "top:26", "panel": "top:40"}}),
    # B. an earlier level moves the bar's own box (the running bounds, not the original)
    case("bottom-level-first", dict(TOP_BAR),
         [(1, [entry("panel", (0, 0, 1000, 40))]),
          (2, [entry("waybar", (0, 40, 1000, 26))])],
         [0, 66, 0, 0],
         [{"namespace": "panel", "level": 1, "height": 40}],
         {"rc": 0, "box": "MATCH", "boxes": "MATCH,MATCH", "reserved": "EQ",
          "band": 66, "expected": 66, "attributed": 66, "gt": "0,66,0,0",
          "attr": "0,66,0,0", "ls": "VALID", "verdict": "CLEAN",
          "attr_ns": {"panel": "top:40", "waybar": "top:26"}}),
    # C. same level: the surface with the higher rule order is arranged first, and its
    #    anchored margin is part of the zone (30 + margin top 6 = 36)
    case("same-level-order", dict(TOP_BAR),
         [(2, [entry("waybar", (0, 36, 1000, 26)), entry("panel", (0, 6, 1000, 30))])],
         [0, 62, 0, 0],
         [{"namespace": "panel", "level": 2, "order": 10, "height": 30, "exclusive": 30,
           "margins": {"top": 6}}],
         {"rc": 0, "box": "MATCH", "boxes": "MATCH,MATCH", "reserved": "EQ",
          "band": 62, "expected": 62, "attributed": 62, "gt": "0,62,0,0",
          "attr": "0,62,0,0", "ls": "VALID", "verdict": "CLEAN",
          "attr_ns": {"panel": "top:36", "waybar": "top:26"}}),
    # D. an exclusive edge matching the anchor selects the top rule for a top|right mask
    case("exclusive-edge-matched", dict(TOP_BAR),
         [(2, [entry("waybar", (0, 0, 1000, 26))]),
          (3, [entry("panel", (800, 26, 200, 100))])],
         [0, 56, 0, 0],
         [{"namespace": "panel", "level": 3, "height": 100, "width": 200,
           "anchor": ["top", "right"], "exclusive": 30, "exclusiveEdge": "top"}],
         {"rc": 0, "box": "MATCH", "boxes": "MATCH,MATCH", "reserved": "EQ",
          "band": 56, "expected": 56, "attributed": 56, "gt": "0,56,0,0",
          "attr": "0,56,0,0", "ls": "VALID", "verdict": "CLEAN",
          "attr_ns": {"waybar": "top:26", "panel": "top:30"}}),
    # E. the same mask with no exclusive edge matches no rule: the zone reserves nothing
    case("anchor-unmatched", dict(TOP_BAR),
         [(2, [entry("waybar", (0, 0, 1000, 26))]),
          (3, [entry("panel", (800, 26, 200, 100))])],
         [0, 26, 0, 0],
         [{"namespace": "panel", "level": 3, "height": 100, "width": 200,
           "anchor": ["top", "right"], "exclusive": 30}],
         {"rc": 0, "box": "MATCH", "boxes": "MATCH,MATCH", "reserved": "EQ",
          "band": 26, "expected": 26, "attributed": 26, "gt": "0,26,0,0",
          "attr": "0,26,0,0", "ls": "VALID", "verdict": "CLEAN",
          "attr_ns": {"waybar": "top:26", "panel": "none:0"}}),
    # F. exclusive -1 is arranged against the full monitor box and reserves nothing
    case("overlay-unexclusive-full", dict(TOP_BAR),
         [(2, [entry("waybar", (0, 0, 1000, 26))]),
          (3, [entry("panel", (800, 700, 200, 100))])],
         [0, 26, 0, 0],
         [{"namespace": "panel", "level": 3, "height": 100, "width": 200,
           "anchor": ["bottom", "right"], "exclusive": -1}],
         {"rc": 0, "box": "MATCH", "boxes": "MATCH,MATCH", "reserved": "EQ",
          "band": 26, "expected": 26, "attributed": 26, "gt": "0,26,0,0",
          "attr": "0,26,0,0", "ls": "VALID", "verdict": "CLEAN"}),
    # G. a zone larger than the axis voids the whole layer reserve (the area guard)
    case("ls-area-invalid", dict(TOP_BAR),
         [(2, [entry("waybar", (0, 0, 1000, 26))]),
          (3, [entry("panel", (0, 26, 1000, 100))])],
         [0, 0, 0, 0],
         [{"namespace": "panel", "level": 3, "height": 100, "exclusive": 2000}],
         {"rc": 0, "box": "MATCH", "boxes": "MATCH,MATCH", "reserved": "EQ",
          "band": 0, "expected": 0, "attributed": 2026, "gt": "0,0,0,0",
          "attr": "0,2026,0,0", "ls": "INVALID", "verdict": "CLEAN"}),
    # H. zone + margin at zero fails the > 0 guard: the surface reserves nothing
    case("negative-margin-skip", dict(TOP_BAR),
         [(2, [entry("waybar", (0, 0, 1000, 26))]),
          (3, [entry("panel", (0, 14, 1000, 100))])],
         [0, 26, 0, 0],
         [{"namespace": "panel", "level": 3, "height": 100, "exclusive": 12,
           "margins": {"top": -12}}],
         {"rc": 0, "box": "MATCH", "boxes": "MATCH,MATCH", "reserved": "EQ",
          "band": 26, "expected": 26, "attributed": 26, "gt": "0,26,0,0",
          "attr": "0,26,0,0", "ls": "VALID", "verdict": "CLEAN",
          "attr_ns": {"waybar": "top:26", "panel": "none:0"}}),
    # I. an empty arranged box is skipped: no box, no zone
    case("empty-box-skip", dict(TOP_BAR),
         [(2, [entry("waybar", (0, 0, 1000, 26))]), (3, [])],
         [0, 26, 0, 0],
         [{"namespace": "panel", "level": 3, "height": 0, "margins": {"top": 1000}}],
         {"rc": 0, "box": "MATCH", "boxes": "MATCH,SKIP", "reserved": "EQ",
          "band": 26, "expected": 26, "attributed": 26, "gt": "0,26,0,0",
          "attr": "0,26,0,0", "ls": "VALID", "verdict": "CLEAN"}),
    # J. exclusive -1 against the full box, on a monitor whose bottom is also reserved:
    #    full_box y = 700, the post-arrangement usable box y = 660 (the mutant reads 660)
    case("full-box-vs-usable", dict(TOP_BAR),
         [(1, [entry("dock", (0, 760, 1000, 40))]),
          (2, [entry("waybar", (0, 0, 1000, 26))]),
          (3, [entry("panel", (800, 700, 200, 100))])],
         [0, 26, 0, 40],
         [{"namespace": "dock", "level": 1, "position": "bottom", "height": 40},
          {"namespace": "panel", "level": 3, "height": 100, "width": 200,
           "anchor": ["bottom", "right"], "exclusive": -1}],
         {"rc": 0, "box": "MATCH", "boxes": "MATCH,MATCH,MATCH", "reserved": "EQ",
          "band": 26, "expected": 26, "attributed": 26, "gt": "0,26,0,40",
          "attr": "0,26,0,40", "ls": "VALID", "verdict": "CLEAN",
          "attr_ns": {"dock": "bottom:40", "waybar": "top:26"}}),
]


def main():
    with open(BASE) as fh:
        carried = json.load(fh)["cases"]
    for new in CASES:
        if any(old["name"] == new["name"] for old in carried):
            raise SystemExit("case name collision: %s" % new["name"])
    control = {
        "round": 80,
        "claim": "C1-r80: the composition of two exclusive layer surfaces",
        "carried": BASE,
        "cases": carried + CASES,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(control, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("cases=%d carried=%d new=%d -> %s"
          % (len(control["cases"]), len(carried), len(CASES), OUT))


if __name__ == "__main__":
    main()
